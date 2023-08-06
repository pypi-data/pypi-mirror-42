from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))
README = open(path.join(here, 'README.rst')).read()
CHANGELOG = open(path.join(here, 'CHANGELOG.rst')).read()

setup(
    name='collectd_eos',
    use_scm_version=True,
    description="Collectd plugin to monitor EOS MGM metrics.",
    long_description=README + CHANGELOG,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Monitoring",
    ],
    keywords='collectd eos storage monitoring',
    url='https://gitlab.cern.ch/ikadochn/collectd-eos',
    author='Ivan Kadochnikov',
    author_email='ivan.kadochikov@cern.ch',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[],
    include_package_data=True,
    zip_safe=True
)
