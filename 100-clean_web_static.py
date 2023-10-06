#!/usr/bin/python3
# deletes out-of-date archives

from fabric.api import local, env, run, lcd, cd
import os

env.hosts = ['54.208.23.186', '18.234.80.12']
env.user = 'ubuntu'

def do_clean(number=0):
    try:
        number = int(number)
    except ValueError:
        return

    if number < 1:
        return

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm -f {{}}".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number + 1))
