import importlib
import os
from invoke import task
import invoke

@task
def clean(ctx,docs=False, bytecode=True, extra=''):
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
        ctx.run("rm -rf %s" % pattern)

@task
def smell(ctx):
    """ Run flake8 PeP8 tests """
    ctx.run("flake8 ratd")

@task
def codestats(ctx):
    """ Run flake8 PeP8 tests for code stats """
    ctx.run("flake8 ratd --statistics -qq")

@task
def build(ctx, docs=False):
    """ Build the setup.py """
    ctx.run("python setup.py build")
    if docs:
        ctx.run("sphinx-build docs docs/_build")

@task(pre=[clean], post=[codestats])
def test(ctx):
    """ Run Unit tests """
    ctx.run("cd ratd && nosetests --rednose test/tests.py test/test_clitools.py")

@task
def release(ctx,version):
    """``version`` should be a string like '0.4' or '1.0'."""
    ctx.run("git tag -a robust-atd-{0} -m \"robust-atd {0} release\"".format(version))
    ctx.run("git push --tags")

    ctx.run("python setup.py sdist")
    ctx.run("python setup.py sdist bdist_wheel")

# Publish to pypi
# @task
# def publish(ctx,version)
    # ctx.run("twine upload -r pypi dist/robust-atd-{0}*".format(version))
