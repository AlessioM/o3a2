import functools
import argparse
import subprocess
import os
from subprocess import CalledProcessError
from typing import cast
import sys

class step(object):
    """
    represents one step in a processing chain
    can have zero or more dependencies
    """
    done = []

    def __init__(self, *depends_on):
        self.depends_on = depends_on

    def __call__(self, step_func):

        @functools.wraps(step_func)
        def wrapper():
            for d in self.depends_on:
                if d not in step.done:
                    d() 
                    step.done.append(d)

            return step_func()

        return wrapper


class command(object):
    """
    represents one command exposed to the CLI
    can have an optional name, if None given, the name of the function is used
    """
    commands = {}

    def __init__(self, name=None):
        self.name = name

    def __call__(self, step_func):
        if self.name is None:
            self.name = step_func.__name__

        command.commands[self.name] = step_func

        @functools.wraps(step_func)
        def wrapper():
            return step_func()

        return wrapper


class foreach(object):
    """
    repeats the step for each item in the iterable given    
    """

    def __init__(self, parameters):
        self.parameters = parameters

    def __call__(self, step_func):
        @functools.wraps(step_func)
        def wrapper():
            return [step_func(p) for p in self.parameters]

        return wrapper


def run(cmd, cwd=None):
    if cwd is None:
        cwd = os.path.relpath(os.path.dirname(__file__))
    try:
        print(cmd)
        subprocess.run(cmd, check=True, cwd=cwd)
        print(cmd)
    except CalledProcessError as e:
        sys.exit(e.returncode)


def _get_parser():
    parser = argparse.ArgumentParser('build.py')    
    parser.add_argument('command', choices=sorted(command.commands.keys()))
    return parser


def o3a2():
    parser = _get_parser()
    args = parser.parse_args()
    command.commands[args.command]()    
