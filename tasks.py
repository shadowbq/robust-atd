import importlib
import os
from invoke import run, task
import invoke

@task
def clean(docs=False, bytecode=True, extra=''):
    """ Clean up docs, bytecode, and extras """
    patterns = ['build', 'dist', '*.egg-info', 'pyclient.log']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/**/*.pyc')
        patterns.append('**/*.pyc')
        patterns.append('./*.pyc')
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        print ("Clearing rm -rf %s" % pattern)
        run("rm -rf %s" % pattern)

@task
def smell():
    """ Run flake8 PeP8 tests """
    run("flake8 ratd")

@task
def codestats():
    """ Run flake8 PeP8 tests for code stats """
    run("flake8 ratd --statistics -qq")

@task
def build(docs=False):
    """ Build the setup.py """
    run("python setup.py build")
    if docs:
        run("sphinx-build docs docs/_build")

@task(pre=[clean], post=[codestats])
def test():
    """ Run Unit tests """
    run("cd ratd && nosetests --rednose test/tests.py test/test_clitools.py")

@task
def release(version):
    """``version`` should be a string like '0.4' or '1.0'."""
    invoke.run("git tag -a robust-atd-{0} -m \"robust-atd {0} release\"".format(version))
    invoke.run("git push --tags")

    invoke.run("python setup.py sdist")
    invoke.run("python setup.py sdist bdist_wheel")

# Publish to pypi
# @task
# def publish(version)
    # invoke.run("twine upload -r pypi dist/robust-atd-{0}*".format(version))
