#!/usr/bin/python3

from fabric.api import env, run

env.user = 'ubuntu'
env.hosts = ['54.236.49.42', '100.25.204.17']

def list():
    run('ls ~/')
