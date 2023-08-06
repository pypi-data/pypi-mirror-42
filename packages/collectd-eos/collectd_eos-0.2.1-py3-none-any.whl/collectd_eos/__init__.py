import collectd
import os
import socket
import subprocess
from collections import defaultdict

# python 3 moved urlparse
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

PLUGIN_NAME = 'eos'

CONFIG_DEFAULT_MGM_URL = None  # use $EOS_MGM_URL or current host
CONFIG_DEFAULT_INTERVAL = -1  # use collectd default
CONFIG_DEFAULT_EOS_CLIENT_COMMAND = ("eos",)


def _parse_em_line(line):
    return dict([key_val.split("=") for key_val in line.split()])


def _eos_command(mgm_url, command, eos_client_command):
    process = subprocess.Popen(eos_client_command + ("-b", "-r", "0", "0", mgm_url, command), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    try:
        stdout = stdout.decode('utf-8')  # decode bytes in python3 only
    except AttributeError:
        pass
    return [line for line in stdout.split('\n') if line.strip()]  # return stdout lines that are not whitespace only


def _type_cast(value, T, min_value=None):
    try:
        return T(value)
    except ValueError:
        return min_value - 1 if min_value else -1


def _extract_data(data_dict, dataset):
    return [_type_cast(data_dict[ds_name], float if ds_type == collectd.DS_TYPE_GAUGE else int, ds_min)
            for ds_name, ds_type, ds_min, ds_max in dataset]


def _parse_dataset(type_instance_list, dataset, meta_keys=None):
    ds_names = [ds[0] for ds in dataset]
    for instance_dict in type_instance_list:
        data = _extract_data(instance_dict, dataset)
        if meta_keys is None:
            metadata = dict([(k, v) for k, v in instance_dict.items() if k not in ds_names])
        else:
            metadata = dict([(k, instance_dict[k]) for k in meta_keys if k in instance_dict])
        yield data, metadata


def _read_one_command(val, url, command, type_instance_key, client_command, extra_metadata=set(), meta_keys=None):
    dataset_name = "eos_" + command
    command_string = command + " ls -m"
    instance_list = [_parse_em_line(line) for line in _eos_command(url, command_string, client_command)]
    dataset = collectd.get_dataset(dataset_name)
    for data, metadata in _parse_dataset(instance_list, dataset, meta_keys):
        metadata.update(extra_metadata)
        val.dispatch(type=dataset_name, values=data, type_instance=metadata[type_instance_key], meta=metadata)


def read_callback(data):
    name, url, interval, client_command = data
    val = collectd.Values(plugin=PLUGIN_NAME, plugin_instance=name)
    if interval > 0:
        val.interval = interval
    version_lines = _eos_command(url, 'version -m', client_command)
    version_combined_line = " ".join(version_lines)
    version_data = _parse_em_line(version_combined_line)
    _read_one_command(val, url, 'node', 'hostport', client_command, version_data)
    _read_one_command(val, url, 'fs', 'id', client_command, version_data)
    _read_one_command(val, url, 'space', 'name', client_command, version_data)


def _parse_config_node(conf):
    for node in conf.children:
        if node.children:
            collectd.warning("Unexpected config block {0}, ignoring".format(node.key))
            continue
        yield node.key.lower(), node.values


def _parse_config_keys(key_value_list):
    instances = []
    intervals = []
    commands = []
    for key, values in key_value_list:
        if key == 'instance':
            instances.append(values)
        elif key == 'interval':
            intervals.append(values)
        elif key == 'eos_client_command':
            commands.append(values)
        else:
            collectd.warning("Unexpected config key: {0}, ignoring".format(key))
    return instances, intervals, commands


def _check_instance(values):
    if len(values) != 2:
        raise collectd.CollectdError("Instance expects 2 values: instance_name, mgm_url. Found values: {0}".
                                     format(values))
    return values


def _check_instances(instances):
    url_count = defaultdict(int)
    name_count = defaultdict(int)
    for name, url in instances:
        name_count[name] += 1
        url_count[url] += 1
        if name_count[name] > 1:
            raise collectd.CollectdError("Plugin instance names must be unique, found reused: {0}".format(name))
        if url_count[url] > 1:
            collectd.warning("Instance {0} mgm_url already seen: {1}".format(name, url))
    return instances


def _parse_interval(intervals):
    if len(intervals) == 0:
        return CONFIG_DEFAULT_INTERVAL
    elif len(intervals) == 1:
        val = intervals[0]
        if len(val) != 1:
            raise collectd.CollectdError("Interval key expects 1 value, found: {0}".format(val))
        return intervals[0][0]
    else:
        raise collectd.CollectdError(
            "Found {0} interval keys in config, expecting no more than one".format(len(intervals)))


def _parse_client_command(commands):
    if len(commands) == 0:
        return CONFIG_DEFAULT_EOS_CLIENT_COMMAND
    elif len(commands) == 1:
        val = commands[0]
        if not val:
            raise collectd.CollectdError("Config key eos_client_command key must not be empty.")
        return val
    else:
        raise collectd.CollectdError(
            "Found {0} eos_client_command keys in config, expecting no more than one".format(len(commands)))


def _get_default_instance():
    if 'EOS_MGM_URL' in os.environ:
        url = os.environ['EOS_MGM_URL']
        name = urlparse(url).hostname
        if name is None:
            collectd.warning("Failed to extract instance hostname from EOS_MGM_URL: {0}".format(url))
            name = url
    else:
        name = socket.getfqdn()
        url = "root://" + name
    return name, url


def configure_callback(conf):
    config = _parse_config_node(conf)
    instance_vals, interval_vals, command_vals = _parse_config_keys(config)
    instances = _check_instances([_check_instance(vals) for vals in instance_vals])
    if not instances:
        instances = [_get_default_instance()]
    interval = _parse_interval(interval_vals)
    client_command = _parse_client_command(command_vals)
    for name, url in instances:
        collectd.info('Plugin {plugin}: Configured instance {instance} with mgm_url={url}, '
                      'interval={interval}, eos_client_command={command}'.format(
            plugin=PLUGIN_NAME, instance=name, url=url, interval=interval, command=client_command))
        kwargs = dict(callback=read_callback, data=(name, url, interval, client_command),
                      name=name)
        if interval > 0:
            kwargs['interval'] = interval
        collectd.register_read(**kwargs)


collectd.register_config(configure_callback)
