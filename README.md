Robust ATD CLI tools
================

"Robust" is a set of tools to leverage the CLI of the Intel Security ATD appliance.

## Important

This is *not a supported or official application of Intel Security*. This work is based off of published documentation for integrating with the ATD REST API.

A modified Fork of atdcli.py (Carlos Munoz - 2014) is included.

## Install

```
$> pip install robust-atd
```

## PKG Download

```
$> mkvirtualenv robust
$> workon robust
$(robust)> wget https://github.com/shadowbq/robust-atd/archive/master.zip
$(robust)> unzip master.zip
$(robust)> cd master
$(robust)> pip install -r requirements.txt
$(robust)> python setup.py install
```

### Install Development

```
$(robust)> pip install -r devel-requirements.txt

```

## Example Outputs:

Using `robust` for submitting samples.

```
usage: robust.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -s
                 FILE_TO_UPLOAD -a ANALYZER_PROFILE [-v] [--version]

Robust Intel Security ATD Python CLI tool

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  -v, --verbosity      increase output verbosity
                             (default: None)
  -q, --quiet          (q)uiet all output
                             (default: False)


Authentication parameters:
  -u USER              (u)sername for the API of the ATD
                               (default: admin)
  -p PASSWORD          (p)assword for username
                               (default: password!)
  -i ATD IP            (i)p or hostname address of ATD
                               (default: atd.localhost.localdomain)
  -n                   do (n)ot verify the SSL certificate for the communications
                               (default: False)

Sample parameters:
  -s FILE_TO_UPLOAD    (s)ample or file to be analyzed
                               (default: None)
  -a ANALYZER_PROFILE  (a)nalyzer profile id to be used during analysis
                               (default: None)

Examples:
    robust.py -u admin -p password! -i atd.localhost.localdomain -s /usr/local/bin/file_to_scan -a 1
```

### Submitting a Sample

A sample can be submitted via cli with full flags, .robust configs, or interrupt passwords.

```shell
$(robust)> robust.py -u admin -p password! -i atd.localhost.localdomain -s /home/malware/non-malicious-container/putty_upx_7.exe
```

Using interupt passwords

```shell
$ robust-profiles.py -n -l
Password: <input password>
ATD profiles:  1
Profile id:  26
Name:  Win XP Down Select (Online)
OS: winXPsp3
Run all down selects?: Off
******************
```

### Pulling the Policy List

In order to submit a sample using `robust` you must identify the Analyzer Profile ID. `robust-profiles` assists in identifing the available profiles your user can submit to.

```
$(robust)> robust-profiles.py -n -l
ATD profiles:  10
Profile id:  1
Name:  Android
OS: android
Run All Selected?: Off
******************
Profile id:  26
Name:  Win XP Down Select (Online)
OS: winXPsp3
Run All Selected?: Off
******************
Profile id:  25
Name:  Windows XP Full Run (Offline)
OS: winXPsp3
Run All Selected?: On
******************
Profile id:  24
Name:  Windows XP Full Run (Online)
OS: winXPsp3
Run All Selected?: On
******************
```
### Managing Outputs

Using Unix Return codes with Quiet output flag

```
(robust)>$ robust.py -n -a 26 -s ./.samples/Morph.exe -q
(robust)>$ echo $?
2
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

## robust-watchdog

A tool that watches directory for changes and submits new files to ATD.

Example CLI
```
$> robust-watchdog -d <directoryToMonitor> -a <Analyzer profile> <<ADDITIONAL SUBMISSION FLAGS>>
```

Let it run in a shell and open another one or the file browser to create files in the /path/to/directory. Since the handler is printing the results, the output will reflect the flags chosen similar to `robust.py`:

```
(robust)$> robust-watchdog.py -a 26 -d ./ -n
.
.
```

## Development Tasks

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
