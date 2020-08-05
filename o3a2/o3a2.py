""" over and over and over"""

import functools
import argparse
import subprocess
import os
from subprocess import CalledProcessError
import sys

class step(): # pylint: disable=invalid-name,too-few-public-methods
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


class command(): # pylint: disable=invalid-name,too-few-public-methods
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


class foreach(): # pylint: disable=invalid-name,too-few-public-methods
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
    """runs the given cmd in the given cwd
    will exit the script passing the exit code if cmd returns with non 0 exit code
    """
    if cwd is None:
        cwd = run.cwd
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
    except CalledProcessError as error:
        sys.exit(error.returncode)


def _get_parser():
    parser = argparse.ArgumentParser('build.py')
    parser.add_argument('command', choices=sorted(command.commands.keys()))
    return parser


def o3a2(base_dir=None):
    """execute all steps and their dependencies
    if base_dir is None all run commands will be executed from the directory this file is in
    """

    if base_dir is None:
        run.cwd = os.path.relpath(os.path.dirname(__file__))
    else:
        run.cwd = base_dir

    parser = _get_parser()
    args = parser.parse_args()
    command.commands[args.command]()
