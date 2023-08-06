############
collectd-eos
############

Collectd plugin to collect EOS_ metrics.
Connects to a mgm instance using eos client and publishes node, fs and space metrics.

Collectd config section example::

    <Plugin python>
        Import collectd_eos
        <Module collectd_eos>
            instance example root://eos.example
            instance another root://another.eos.instance.example
            instance third root://third.mgm.intance.example
            interval 60
            eos_client_command ssh client.host.example eos
        </Module>
    </Plugin>

- **instance** expects 2 values:

  - EOS instance name / plugin instance name
  - EOS MGM URL

- **interval** overrides the default collection interval

- **eos_client_command** is used when there is no eos client on the collectd node,
  and ssh or docker are needed to run eos, especially during plugin development

If there are no instances defined in config and $EOS_MGM_URL is set,
it is used as the default url with the instance name set to the hostname portion.

If there are no instances defined in config and $EOS_MGM_URL is unset,
the current hostname is used as the instance name and url.

*******
Testing
*******

Test in virutalenv::

    virtualenv venv
    . venv/bin/activate
    pip install -r build-requirements.txt -r test-requirements.txt
    pip install -e .
    pytest
    python setup.py sdist bdist_wheel
    twine check dist/*
    tox

Use collectd.conf or collectd.docker.conf for functional testing: does the plugin cope with real metrics?

On a host with eos::

    $ collectd -Tf -C collectd.conf

Docker can be used for the eos client::

    $ docker run --name eos_client --rm -itd gitlab-registry.cern.ch/dss/eos:4.4.10
    <container id output>
    $ docker exec -it eos_client kinit <username>@CERN.CH
    <password prompt>
    $ collectd -Tf -C collectd.docker.conf
    <check collectd log for errors>
    $ docker stop eos_client

.. _EOS: https://eos.web.cern.ch/

