Robust ATD CLI tools
================

"Robust" is a set of tools to leverage the CLI of the Intel Security ATD appliance.

## Install

```
$> pip install robust-atd
```

## PKG Download

```
$> mkvirtualenv robust
$> workon robust
$(robust)> pip install -r requirements.txt
$(robust)> python setup.py install
```

### Install Development

```
$(robust)> pip install -r devel-requirements.txt

```

## Example Outputs:

Submitting a Sample

```shell
$(robust)> python robust.py -u admin -p password! -i atd.localhost.localdomain -s /home/malware/non-malicious-container/putty_upx_7.exe
```

## Robust (DOT) FILE

Robust can use a `~\.robust` file to load defaults in the auth context

```shell
$ cat ~/.robust
[auth]
user: admin
password: password!
host: atd.localhost.localdomain
```

This file is expanded via the `os` module and maps to windows too.

Example using `~/.robust`

```shell
python robust-policy.py -n -l
```

### Development Tasks

```shell
$ invoke -l
Available tasks:

  build       Build the setup.py
  clean       Clean up docs, bytecode, and extras
  codestats   Run flake8 PeP8 tests for code stats
  release     ``version`` should be a string like '0.4' or '1.0'.
  smell       Run flake8 PeP8 tests
  test        Run Unit tests

```

### Running the Test Suite

Nose is run via `invoke test`

```
$ invoke test
Clearing rm -rf build
Clearing rm -rf dist
Clearing rm -rf *.egg-info
Clearing rm -rf pyclient.log
Clearing rm -rf **/**/*.pyc
Clearing rm -rf **/*.pyc
Clearing rm -rf ./*.pyc
........
-----------------------------------------------------------------------------
8 tests run in 0.2 seconds (8 tests passed)
1       E121 continuation line under-indented for hanging indent
4       E122 continuation line missing indentation or outdented
8       E126 continuation line over-indented for hanging indent
2       E201 whitespace after '{'
2       E202 whitespace before '}'
27      E203 whitespace before ':'
12      E221 multiple spaces before operator
30      E228 missing whitespace around modulo operator
29      E231 missing whitespace after ','
10      E251 unexpected spaces around keyword / parameter equals
1       E265 block comment should start with '# '
7       E302 expected 2 blank lines, found 1
4       E303 too many blank lines (2)
2       E401 multiple imports on one line
76      E501 line too long (97 > 79 characters)
2       E703 statement ends with a semicolon
21      F401 'sys' imported but unused
1       F841 local variable 'auth_group' is assigned to but never used
1       N801 class names should use CapWords convention
1       N802 function name should be lowercase
3       N803 argument name should be lowercase
2       N806 variable in function should be lowercase
```
