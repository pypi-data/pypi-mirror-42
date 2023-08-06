*********
Changelog
*********

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

0.2.1_ - 2019-02-28
===================

Added
-----

-   More testing
-   More documentation

Fixed
-----

-   Readme needed one more newline at the end to be used as the package description

Removed
-------

-   Python 2.6 support no longer promised, attempted, or tested.


0.2.0_ - 2019-02-27
===================

Added
-----

-   pyproject.toml to define build requirements as per PEP-518_
-   build-requirements.txt and build-requirements.26.txt to document build requirements
    in a more realistic, backwards-compatible way.

Changed
-------

-   Configuration section format. mgm_url key is removed
    EOS instances are now defined by the key "instance" which expects two values:

    *   instance name, must be unique,
        defines the collectd plugin instance name reported with the metrics
    *   mgm_url, the url eos client will query for data

Fixed
-----

-   Don't sent interval of -1 to collectd, it does not interpret it as default

0.1.0_ - 2019-02-26
===================

Added
-----

-   README.rst and CHANGELOG.rst
-   package sources src/collectd_eos
-   unit tests in tests/ and tox.ini
-   collectd.conf and collectd.docker.conf for testing with collectd
-   eos.types.db to define eos time-series datasets for collectd
-   LICENSE Apache 2

..  _Unreleased: https://gitlab.cern.ch/ikadochn/collectd-eos/compare/v0.2.1...develop
..  _0.2.1: https://gitlab.cern.ch/ikadochn/collectd-eos/compare/v0.2.0...v0.2.1
..  _0.2.0: https://gitlab.cern.ch/ikadochn/collectd-eos/compare/v0.1.0...v0.2.0
..  _0.1.0: https://gitlab.cern.ch/ikadochn/collectd-eos/tags/v0.1.0

..  _PEP-518: https://www.python.org/dev/peps/pep-0518/
