import sys

import pytest
import subprocess
from mock import Mock, patch, call


class CollectdError(Exception):
    pass


@pytest.fixture
def collectd_eos():
    collectd = Mock(spec=['register_config', 'register_read', 'get_dataset', 'Values', 'info', 'warning'],
                    CollectdError=CollectdError)
    with patch.dict(sys.modules, {'collectd': collectd}):
        import collectd_eos
        yield collectd_eos


def test_parse_em_line(collectd_eos):
    assert collectd_eos._parse_em_line(
        "a=b number=123    this=that") == {'a': 'b', 'number': '123', 'this': 'that'}


def test_eos_command(collectd_eos, mocker):
    mocker.patch("subprocess.Popen", autospec=True,
                 return_value=mocker.Mock(spec=['communicate'],
                                          communicate=mocker.Mock(
                                              return_value=('process stdout\n \n\n a=b\nc=d  ', ''))))
    assert collectd_eos._eos_command("root://eos.example", "command arg1 -arg2", ('client', 'eos')) == [
        'process stdout', ' a=b', 'c=d  ']
    subprocess.Popen.assert_called_once_with(
        ("client", "eos", "-b", "-r", "0", "0", "root://eos.example", "command arg1 -arg2"), stdout=subprocess.PIPE)


def test_type_cast(collectd_eos):
    assert collectd_eos._type_cast('13', int) == 13
    assert collectd_eos._type_cast('13', float, 0) == 13
    assert collectd_eos._type_cast('13.4', int) == -1
    assert collectd_eos._type_cast('13.4', float) == 13.4
    assert collectd_eos._type_cast('1-3', int, 0) == -1
    assert collectd_eos._type_cast('1-3', float) == -1
    assert collectd_eos._type_cast('1-3', int, 4) == 3


def test_extract_data(collectd_eos):
    data = {'a': '1', 'b': '2', 'c': '3'}
    gauge = collectd_eos.collectd.DS_TYPE_GAUGE = 1
    counter = collectd_eos.collectd.DS_TYPE_COUNTER = 2
    dataset = [('a', gauge, 0, None), ('b', counter, None, 100)]
    assert collectd_eos._extract_data(data, dataset) == [1.0, 2]
    data = {'a': '1.2', 'b': '2.2', 'c': '3.2'}
    assert collectd_eos._extract_data(data, dataset) == [1.2, -1]
    data = {'a': '1', 'c': '3'}
    with pytest.raises(KeyError):
        collectd_eos._extract_data(data, dataset)


def test_parse_dataset(collectd_eos):
    instance_list = [{'a': '1', 'b': '2', 'c': '3'},
                     {'a': '1.2', 'b': '2.2', 'c': '3.2'}]
    gauge = collectd_eos.collectd.DS_TYPE_GAUGE = 1
    counter = collectd_eos.collectd.DS_TYPE_COUNTER = 2
    dataset = [('a', gauge, 0, None), ('b', counter, None, 100)]
    assert list(collectd_eos._parse_dataset(instance_list, dataset)) == [([1.0, 2], {'c': '3'}),
                                                                         ([1.2, -1], {'c': '3.2'})]
    assert list(collectd_eos._parse_dataset(instance_list, dataset, 'b')) == [([1.0, 2], {'b': '2'}),
                                                                              ([1.2, -1], {'b': '2.2'})]


def test_read_one_command(collectd_eos, mocker):
    mocker.patch("subprocess.Popen", autospec=True,
                 return_value=mocker.Mock(spec=['communicate'],
                                          communicate=mocker.Mock(
                                              return_value=('a=1.5 b=3 name=asdf  \n name=zzz a=2 b=4\n', ''))))
    gauge = collectd_eos.collectd.DS_TYPE_GAUGE = 1
    counter = collectd_eos.collectd.DS_TYPE_COUNTER = 2
    val = mocker.Mock(spec=['dispatch'])
    collectd_eos.collectd.get_dataset = mocker.Mock(return_value=([('a', gauge, 0, 100),
                                                                   ('b', counter, 0, None)]))
    collectd_eos._read_one_command(val, 'root://test.example', 'command', type_instance_key='name',
                                   client_command=('client', 'eos'), extra_metadata={'version': '13'})
    assert subprocess.Popen.mock_calls == [call(("client", "eos", "-b", "-r", "0", "0", "root://test.example",
                                                 "command ls -m"), stdout=subprocess.PIPE)]
    collectd_eos.collectd.get_dataset.assert_called_once_with('eos_command')
    assert val.mock_calls == [call.dispatch(type="eos_command", values=[1.5, 3], type_instance="asdf",
                                            meta={'version': '13', 'name': 'asdf'}),
                              call.dispatch(type="eos_command", values=[2.0, 4], type_instance="zzz",
                                            meta={'version': '13', 'name': 'zzz'})]


def test_read_callback(collectd_eos, mocker):
    val = collectd_eos.collectd.Values = Mock(spec=['dispatch'])
    gauge = collectd_eos.collectd.DS_TYPE_GAUGE = 1
    counter = collectd_eos.collectd.DS_TYPE_COUNTER = 2
    mocker.patch("subprocess.Popen", autospec=True,
                 return_value=mocker.Mock(spec=['communicate'],
                                          communicate=mocker.Mock(
                                              return_value=('a=1 b=2 c=3 name=asdf hostport=host:123 id=123', ''))))
    collectd_eos.collectd.get_dataset = mocker.Mock(return_value=([('a', gauge, 0, 100),
                                                                   ('b', counter, 0, None)]))
    collectd_eos.read_callback(('test', 'root://test.example', -1, ('client', 'eos')))
    # a and b are coming into meta from version_data
    # mock Popen better for a more realistic test
    assert val.mock_calls == [call(plugin=collectd_eos.PLUGIN_NAME, plugin_instance='test'),
                              call().dispatch(type='eos_node', type_instance='host:123', values=[1.0, 2],
                                              meta=dict(a='1', b='2', c='3',
                                                        name='asdf', hostport='host:123', id='123')),
                              call().dispatch(type='eos_fs', type_instance='123', values=[1.0, 2],
                                              meta=dict(a='1', b='2', c='3',
                                                        name='asdf', hostport='host:123', id='123')),
                              call().dispatch(type='eos_space', type_instance='asdf', values=[1.0, 2],
                                              meta=dict(a='1', b='2', c='3',
                                                        name='asdf', hostport='host:123', id='123'))
                              ]


class MockCollectdConfig(object):
    def __init__(self, *args):
        self.children = [Mock(spec=[], key=k, values=v, children=()) for k, v in args]


def test_parse_config_node(collectd_eos):
    conf = MockCollectdConfig(('a', [1, 2, 3]),
                              ('B', [1]),
                              ('A', [4, 5]))
    assert list(collectd_eos._parse_config_node(conf)) == [('a', [1, 2, 3]), ('b', [1]), ('a', [4, 5])]
    conf.children[1].children = ('something',)
    assert list(collectd_eos._parse_config_node(conf)) == [('a', [1, 2, 3]), ('a', [4, 5])]
    collectd_eos.collectd.warning.assert_called_once_with("Unexpected config block B, ignoring")


def test_parse_config_keys(collectd_eos):
    parse = collectd_eos._parse_config_keys
    warning = collectd_eos.collectd.warning
    assert parse([]) == ([], [], [])
    warning.assert_not_called()
    assert parse([('A', (1,))]) == ([], [], [])
    assert warning.mock_calls == [call("Unexpected config key: A, ignoring")]
    warning.reset_mock()
    assert parse(
        [('instance', ('a', 'b')), ('interval', [13])]) == ([('a', 'b')], [[13]], [])
    warning.assert_not_called()
    assert parse(
        [('instance', 'a'), ('instance', 'bbb'), ('instance', 'c')]) == (['a', 'bbb', 'c'], [], [])
    warning.assert_not_called()
    assert parse(
        [('instance', 'a'), ('eos_client_command', ('client', 'command'))]) == (['a'], [], [('client', 'command')])
    warning.assert_not_called()
    assert parse(
        [('wrong', 123), ('instance', 'a'), ('key', 'value'),
         ('eos_client_command', ('client', 'command')), ('instance_', 'asdf')]) == (['a'], [], [('client', 'command')])
    assert warning.mock_calls == [call("Unexpected config key: wrong, ignoring"),
                                  call("Unexpected config key: key, ignoring"),
                                  call("Unexpected config key: instance_, ignoring")]


def test_check_instance(collectd_eos):
    check = collectd_eos._check_instance
    CollectdError = collectd_eos.collectd.CollectdError
    assert check((1, 2)) == (1, 2)
    with pytest.raises(CollectdError,
                       match=r"Instance expects 2 values: instance_name, mgm_url. Found values: \(\)"):
        check(())
    with pytest.raises(CollectdError,
                       match=r"Instance expects 2 values: instance_name, mgm_url. Found values: \(1, 2, 3\)"):
        check((1, 2, 3))


def test_check_instances(collectd_eos):
    check = collectd_eos._check_instances
    warning = collectd_eos.collectd.warning
    CollectdError = collectd_eos.collectd.CollectdError

    assert check([]) == []
    warning.assert_not_called()

    instances = [('a', 'url'), ('b', 'different'), ('A', 'other')]
    assert check(instances) == instances
    warning.assert_not_called()

    with pytest.raises(CollectdError, match="Plugin instance names must be unique, found reused: a"):
        instances = [('a', 'url'), ('b', 'different'), ('a', 'url'), ('b', 'url')]
        check(instances)
    warning.assert_not_called()

    with pytest.raises(CollectdError, match="Plugin instance names must be unique, found reused: a"):
        instances = [('a', 'url'), ('b', 'url'), ('c', 'url'), ('a', 'url')]
        check(instances)
    assert warning.mock_calls == [call("Instance b mgm_url already seen: url"),
                                  call("Instance c mgm_url already seen: url")]


def test_parse_interval(collectd_eos):
    parse = collectd_eos._parse_interval
    CollectdError = collectd_eos.collectd.CollectdError
    assert parse([]) == collectd_eos.CONFIG_DEFAULT_INTERVAL
    assert parse([(13,)]) == 13
    with pytest.raises(CollectdError, match=r"Interval key expects 1 value, found: \(1, 1, 1\)"):
        parse([(1, 1, 1)])
    with pytest.raises(CollectdError, match=r"Interval key expects 1 value, found: \(\)"):
        parse([()])
    with pytest.raises(CollectdError, match="Found 3 interval keys in config, expecting no more than one"):
        parse([(13,), (13,), (13,)])


def test_parse_client_command(collectd_eos):
    parse = collectd_eos._parse_client_command
    CollectdError = collectd_eos.collectd.CollectdError
    assert parse([]) == collectd_eos.CONFIG_DEFAULT_EOS_CLIENT_COMMAND
    assert parse([('eos',)]) == ('eos',)
    assert parse([('ssh', 'client.hostname.example', 'eos')]) == ('ssh', 'client.hostname.example', 'eos')
    with pytest.raises(CollectdError, match="Config key eos_client_command key must not be empty."):
        parse([()])
    with pytest.raises(CollectdError, match="Found 3 eos_client_command keys in config, expecting no more than one"):
        parse([('eos',), ('eos2',), ('ssh', 'host', 'eos')])


def test_get_default_instance(collectd_eos, mocker):
    get = collectd_eos._get_default_instance
    warning = collectd_eos.collectd.warning

    mocker.patch('socket.getfqdn', return_value='hostname.example')
    with patch.dict('os.environ', clear=True):
        assert get() == ('hostname.example', 'root://hostname.example')
        warning.assert_not_called()
    with patch.dict('os.environ', {'EOS_MGM_URL': 'root://hostname.from.env'}):
        assert get() == ('hostname.from.env', 'root://hostname.from.env')
        warning.assert_not_called()
    with patch.dict('os.environ', {'EOS_MGM_URL': 'http://hostname.from.env:1234/some/place'}):
        # probably ok not to check, eos client will fail later
        assert get() == ('hostname.from.env', 'http://hostname.from.env:1234/some/place')
        warning.assert_not_called()
    with patch.dict('os.environ', {'EOS_MGM_URL': 'invalid url'}):
        assert get() == ('invalid url', 'invalid url')
        assert warning.mock_calls == [call("Failed to extract instance hostname from EOS_MGM_URL: invalid url")]


def test_plugin_registration(collectd_eos):
    collectd_eos.collectd.register_config.assert_called_once_with(collectd_eos.configure_callback)


def test_configure_callback(collectd_eos, mocker):
    register_read = collectd_eos.collectd.register_read
    collectd_eos.configure_callback(MockCollectdConfig(('instance', ('test', 'root://test.example'))))
    assert register_read.mock_calls == [call(name='test',
                                             data=('test', 'root://test.example', -1, ('eos',)),
                                             callback=collectd_eos.read_callback)]
    register_read.reset_mock()

    collectd_eos.configure_callback(MockCollectdConfig(('instance', ('a', 'asdf')),
                                                       ('INSTANCE', ('z', 'zxcv')),
                                                       ('intErVal', (60,))))
    assert register_read.mock_calls == [call(name='a',
                                             data=('a', 'asdf', 60, ('eos',)),
                                             callback=collectd_eos.read_callback,
                                             interval=60,
                                             ),
                                        call(name='z',
                                             data=('z', 'zxcv', 60, ('eos',)),
                                             callback=collectd_eos.read_callback,
                                             interval=60,
                                             )]
    register_read.reset_mock()

    mocker.patch('socket.getfqdn', return_value='hostname.example')
    collectd_eos.configure_callback(MockCollectdConfig(('interval', (60,)), ))
    assert register_read.mock_calls == [call(name='hostname.example',
                                             data=('hostname.example', 'root://hostname.example', 60, ('eos',)),
                                             callback=collectd_eos.read_callback,
                                             interval=60)]
