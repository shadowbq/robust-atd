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

## PKG Download Alternative

Note: python setup.py will attempt to install dependencies from the internet via `pip`.

```
$> mkvirtualenv robust
$> workon robust
$(robust)> wget https://github.com/shadowbq/robust-atd/archive/master.zip
$(robust)> unzip master.zip
$(robust)> cd master
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
$(robust)> robust-profiles.py -n -l
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

Using System Return codes with `-q` Quiet output flag. When the quiet flag is
used for submitting samples or searching reports the *severity* of the application
is returned as a system exit/return code. Negative return codes indicate *faults*
or failure during submission.

```
(robust)>$ robust.py -n -a 26 -s ./.samples/Sample.exe -q
(robust)>$ echo $?
2
```

Common Fault codes:

```
    -1 ---> Error connecting to the ATD Server
    -2 ---> Error uploading file to the ATD Server
    -3 ---> Analysis failed
    -4 ---> Error getting report
    -5 ---> Error Obtaining vmprofilelist
```

Malware ranking:
(If the severity level of the sample is 3 and above it is generally regarded a threat)
```
    N/A -> Sample did not run
    -1 --> Sample is white listed
    0 ---> No malicious activity detected (None)
    1 ---> Sample is slightly suspicious (Low)
    2 ---> Sample is somewhat/probably is suspicious
    3 ---> Sample is malicious (Medium)
    4 ---> Sample is malicious
    5 ---> Sample is malicious (Very High)
```

## Robust (DOT) FILE

Robust can use a `~\.robust` file to load defaults in the auth context

```shell
$(robust)> cat ~/.robust
[auth]
user: admin
password: password!
host: atd.localhost.localdomain
```

This file is expanded via the `os` module and maps to windows too.

## robust-watchdog

A tool that watches a directory recursively for any new files to submit.

Example CLI
```
$(robust)> usage: robust-watchdog.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -a
                          ANALYZER_PROFILE -d DIRECTORY [-e] [--version]
                          [-v | -q]
```

Let it run in a shell and open another one or the file browser to create files in the /path/to/directory. Since the handler is printing the results, the output will reflect the flags chosen similar to `robust.py`:

The `-e` flag can be passed to cause all existing files in the directory (recurisively) to be submitted upon start.

```shell
(robust)$> robust-watchdog.py -a 26 -d ./ -n -e
.
...
.
.....
````

## robust-search

A tool designed to search and return reports for a specific md5 hash.

```shell
(robust)$> $ robust-search.py -m 2F7568342339CDB8321B52FF7BEBE661 -n
(Sample.exe:2F7568342339CDB8321B52FF7BEBE661) = 2: "Sample probably is suspicious"
```

### Fetching Reporting data

robust-search has the options `-f` and `-t` to collect the proper report on the submission.

```
usage: robust-search.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -m MD5
                        [-t {html,txt,xml,zip,json,ioc,stix,pdf,sample}]
                        [-f FILENAME] [--version] [-v | -q]

Robust Intel Security ATD Python CLI tool

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbosity       increase output (v)erbosity
                        		(default: None)
  -q, --quiet           (q)uiet all output
                        		(default: False)

Authentication parameters:
  -u USER               (u)sername for the API of the ATD
                        		(default: robust)
  -p PASSWORD           (p)assword for username
                        		(default: P@ssword1!)
  -i ATD IP             (i)p or hostname address of ATD
                        		(default: atd.vanillasystem.com)
  -n                    do (n)ot verify the SSL certificate for the communications
                        		(default: False)

Search parameters:
  -m MD5                (m)d5 32bit hash of the sample to search
                        		(default: None)

Reporting parameters:
  -t {html,txt,xml,zip,json,ioc,stix,pdf,sample}
                        (t)ype of report requested
                        		(default: None)
  -f FILENAME           (f)ilename for saving the requested report
                        		(default: None)
```

## robust-convict

Example Usage

```
robust-convict.py -n -a 26 -c ./tmp/clean/ -x ./tmp/dirty/ -r ./tmp/reports/ -z ./tmp/errors/ -d ./tmp/preprocess -j 10 -t zip -q
```

Options

```shell
usage: robust-convict.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -a
                         ANALYZER_PROFILE -d DIRECTORY [-e] -c CLEANDIR -x
                         DIRTYDIR -r REPORTDIR -z ERRORDIR [-j MAXTHREADS]
                         [-t {html,txt,xml,zip,json,ioc,stix,pdf,sample}]
                         [--version] [-v | -q]

Robust Intel Security ATD Python CLI tool

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbosity       increase output (v)erbosity
                        		(default: None)
  -q, --quiet           (q)uiet all output
                        		(default: False)

Authentication parameters:
  -u USER               (u)sername for the API of the ATD
                        		(default: robust)
  -p PASSWORD           (p)assword for username
                        		(default: P@ssword1!)
  -i ATD IP             (i)p or hostname address of ATD
                        		(default: atd.vanillasystem.com)
  -n                    do (n)ot verify the SSL certificate for the communications
                        		(default: False)

Watch parameters:
  -a ANALYZER_PROFILE   (a)nalyzer profile id to be used during analysis
                        		(default: None)
  -d DIRECTORY          (d)irectory to watch for events
                        		(default: None)
  -e                    (e)xisting files in directory will be submitted
                        		(default: False)

Convict parameters:
  -c CLEANDIR           (c) move clean files to this directory
                        		(default: None)
  -x DIRTYDIR           (x) move processed dirty files to this directory
                        		(default: None)
  -r REPORTDIR          (r) save reports to this directory
                        		(default: None)
  -z ERRORDIR           (z) move error or skip files to this directory
                        		(default: None)
  -j MAXTHREADS         (j) max number of threads
                        		(default: None)
  -t {html,txt,xml,zip,json,ioc,stix,pdf,sample}
                        (t)ype of report requested
                        		(default: None)
```

## Development Tasks

```shell
(robust)$> invoke -l
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
Clearing rm -rf build
Clearing rm -rf dist
Clearing rm -rf *.egg-info
Clearing rm -rf pyclient.log
Clearing rm -rf **/**/*.pyc
Clearing rm -rf **/*.pyc
Clearing rm -rf ./*.pyc
...................
-----------------------------------------------------------------------------
19 tests run in 0.3 seconds (19 tests passed)
117     E501 line too long (97 > 79 characters)
7       F401 'ratd' imported but unused
1       F841 local variable 'rb_rtnv' is assigned to but never used
1       N802 function name should be lowercase
5       W601 .has_key() is deprecated, use 'in'
```
