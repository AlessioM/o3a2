from o3a2 import *
import os
import sys

PACKAGES = ["o3a2"]

@command()
@step()
def bootstrap_dev():
    run(["pip", "install", "-r", "requirements-dev.in"])

@command()
@step()
def freeze_dev():
    run(["pip-compile", "--allow-unsafe", "--generate-hashes", "requirements-dev.in"])

@command()
@step()
def setup_dev():
    run(["pip", "install", "-r", "requirements-dev.txt"])

@command()
@step()
@foreach(PACKAGES)
def lint(package):
    run(["pylint", package])

@command()
@step(setup_dev)
def install_editable():
    run(["pip", "install", "-e", "."])

if __name__ == "__main__":
    o3a2(os.path.dirname(os.path.abspath(sys.argv[0])))