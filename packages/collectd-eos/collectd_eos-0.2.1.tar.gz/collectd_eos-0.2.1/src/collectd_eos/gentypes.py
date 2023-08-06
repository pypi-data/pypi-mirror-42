#!/usr/bin/env python3

from sh import docker
from pprint import pprint


def is_float(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


def gen(command):
    stdout = docker.exec('eos_client', 'eos', '-b', '-r', '0', '0',
                         'root://eulake.cern.ch',
                         '{} ls -m'.format(command))
    data = [l for l in stdout.split('\n') if l]
    record = dict(eq.split('=') for eq in data[0].split())
    fields = [k for k, v in record.items() if is_float(v)]
    # pprint({f: record[f] for f in fields})
    fields = sorted([f for f in fields if f not in ('id', 'port')])
    print('eos_{command}\t{dataset}'.format(command=command,
                                            dataset=' '.join('{}:GAUGE:0:U'.format(f) for f in fields)))


gen('fs')
gen('space')
gen('node')
