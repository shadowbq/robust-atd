Robust ATD CLI tools
================


[![GitHub release](https://img.shields.io/github/release/shadowbq/robust-atd.svg?style=for-the-badge)](https://github.com/shadowbq/robust-atd/releases)
[![license](https://img.shields.io/github/license/shadowbq/robust-atd.svg?style=for-the-badge)](/LICENSE)
[![GitHub Release Date](https://img.shields.io/github/release-date/shadowbq/robust-atd.svg?style=for-the-badge)](https://github.com/shadowbq/robust-atd/releases)
[![Code](https://img.shields.io/badge/Language-Python--2.7-ff69b4.svg?style=for-the-badge)](/README.md)


"Robust" is a set of tools to leverage the HTTPS REST API of the [McAfee Advanced Threat Detection](http://www.mcafee.com/us/products/advanced-threat-defense.aspx) 3.8 - 4.x appliance.

## Tools Overview

* `robust` : basic cli submission of a single piece of malware to a MATD server.
* `robust-profiles` : list the available MATD profiles
* `robust-search` : search MATD via MD5 for a report.
* `robust-watchdog` : monitor a directory for files and submit `multithreaded` to MATD
* `robust-convict` : submit `multithreaded` a directory filled with samples and sort into malicious, clean, error, etc.
* `robust-reporter` : parse offline the json files returned during large batch submissions.
* `robust-version-checker` : Check the MATD Server Version

## Important

This is *not a supported or official application of McAfee*. This work is based off of publicly available published documentation for integrating with the McAfee ATD REST API 3.6.x to 4.x

Official API Documentation is available here:

* https://support.mcafee.com/ServicePortal/faces/knowledgecenter?q=api&v=&p=Advanced+Threat+Defense

## McAfee ATD - Advanced Threat defense

McAfee ATD is a commercial grade enterprise security sandbox analysis appliance. It main function is to provide advanced detection for stealthy, zero-day malware. McAfee Advanced Threat Defense is available as an on-premises appliance or a virtual form factor, with support for both private and public cloud with availability in the Azure Marketplace.

* https://www.mcafee.com/us/products/advanced-threat-defense.aspx
* https://www.mcafee.com/us/resources/data-sheets/ds-advanced-threat-defense.pdf

## Install

Req: Python 2.7.x.

Bug #5: https://github.com/shadowbq/robust-atd/issues/5 - ~~`pip install robust-atd`~~

Note: Python 3.x is not supported.

### PKG Download & Manual Install Alternative

Note: `python setup.py install` will attempt to install dependencies from the internet via `pip`.

For offline runtime installation, please download the pip packages listed in the `requirements.txt`.

### Virutalenv

It is recommended to install virtualenv & virtualenvwrapper via `Virtualenv Burrito`.

See: [README_PYTHON_UP.md](/README_PYTHON_UP.md)

```
$> mkvirtualenv robust
$> workon robust
$(robust)> wget https://github.com/shadowbq/robust-atd/archive/master.zip
$(robust)> unzip master.zip
$(robust)> cd master
$(robust)> python setup.py install
```

-or-

```
$> mkvirtualenv --python=python2.7 robust
$> workon robust
$(robust)> pip install robust-atd
```

### Robust (DOT) Configuration file

Robust will use the `~\.robust` configuration file to load defaults into the scripts.

The configuration file is broken into multiple sections. If you use a section you must define all the settings in that section.

  * [auth]
  * [connection]
  * [convict]

It is recommended to set the file to `read-write` only for the current user, and remove all world `(-)rwx` permissions.

Authentication Section `[auth]` :

```shell
$(robust)> cat ~/.robust
[auth]
user: admin
password: password.
```

Connection Detail Section `[connection]` :

```shell
$(robust)> cat ~/.robust
[connection]
ip: atd.localhost.localdomain
skipssl: true
maxthreads: 15
```

Data Storage Section `[storage]`:

Note: Datastorage locations will be created if they do not exist.

```shell
$(robust)> cat ~/.robust
[storage]
severity: 3
cleandir: ~/robust/clean
dirtydir: ~/robust/dirty
reportdir: ~/robust/reports
errordir: ~/robust/errors
```

This file is expanded via the `os` module is compliant with windows user directories.


## Robust:

Using `robust` for submitting samples.

```
usage: robust.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -s
                 FILE_TO_UPLOAD -a ANALYZER_PROFILE [-v] [--version]

Robust McAfee ATD Python CLI tool

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
                               (default: password.)
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
    robust.py -u admin -p password. -i atd.localhost.localdomain -s /usr/local/bin/file_to_scan -a 1
```

### Submitting a Sample

A sample can be submitted via cli with full flags, `.robust` configuration file, or interrupt passwords.

```shell
$(robust)> robust.py -u admin -p password. -i atd.localhost.localdomain -s /home/malware/non-malicious-container/putty_upx_7.exe
```

Using interrupt (interactive) passwords:

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
## robust-version-checker

You can quickly test your connection settings in the CLI.

```
$(robust)> robust-version-checker.py -u robust -p password. -i atd.example.com -n
Connection successful...

Session Value:      g7aenj99pfp0gbrogfbqsd9085
User ID:            57
ATD ver:            4.2.2.16
ATD Box heartbeat:  1519939175
```

## robust-profiles

A tool designed to pull the *Analyzer Profile* policy list available to a specific user.

Pulling the Policy List - In order to submit a sample using `robust` you must identify the Analyzer Profile ID. `robust-profiles` assists in identifying the available profiles your user can submit samples to.

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

## robust-search

A tool designed to search and return reports for a specific md5 hash.

```shell
(robust)$> $ robust-search.py -m 2F7568342339CDB8321B52FF7BEBE661 -n
(Sample.exe:2F7568342339CDB8321B52FF7BEBE661) = 2: "Sample probably is suspicious"
```
### Help details

`robust-search` has the options `-w` and `-t` to collect the proper report on the submission.

```
usage: robust-search.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -m MD5
                        [-t {html,txt,xml,zip,json,ioc,stix,pdf,sample}]
                        [-w FILENAME] [--version] [-v | -q]

Robust McAfee ATD Python CLI tool

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbosity       increase output (v)erbosity
                        		(default: None)
  -q, --quiet           (q)uiet all output
                        		(default: False)

Authentication parameters:
  -u USER               (u)sername for the API of the ATD
                        		(default: admin)
  -p PASSWORD           (p)assword for username
                        		(default: password.)
  -i ATD IP             (i)p or hostname address of ATD
                        		(default: atd.localhost.localdomain)
  -n                    do (n)ot verify the SSL certificate for the communications
                        		(default: False)

Search parameters:
  -m MD5                (m)d5 32bit hash of the sample to search
                        		(default: None)

Reporting parameters:
  -t {html,txt,xml,zip,json,ioc,stix,pdf,sample}
                        (t)ype of report requested
                        		(default: None)
  -w FILENAME           (w)rite filename for saving the requested report
                        		(default: None)
```


## robust-watchdog

A tool that watches a directory recursively for any new files to submit.

Example CLI
```
usage: robust-watchdog.py [-h] -u USER [-p PASSWORD] -i ATD IP [-n] -a
                          ANALYZER_PROFILE -d DIRECTORY [-e] [-j MAXTHREADS]
                          [--version] [-v | -q]

Robust McAfee ATD Python CLI tool

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  -v, --verbosity      increase output (v)erbosity
                       		(default: None)
  -q, --quiet          (q)uiet all output
                       		(default: False)

Authentication parameters:
  -u USER              (u)sername for the API of the ATD
                       		(default: None)
  -p PASSWORD          (p)assword for username
                       		(default: None)
  -i ATD IP            (i)p or hostname address of ATD
                       		(default: None)
  -n                   do (n)ot verify the SSL certificate for the communications
                       		(default: False)

Watch parameters:
  -f                   (f)ollow and watch the directory for new files to submit
                          (default: True)
  -a ANALYZER_PROFILE  (a)nalyzer profile id to be used during analysis
                       		(default: None)
  -d DIRECTORY         (d)irectory to watch for events
                       		(default: None)
  -e                   (e)xisting files in directory will be submitted
                       		(default: False)
  -j MAXTHREADS        (j) max number of threads
                       		(default: 1)
```

Let it run in a shell and open another one or the file browser to create files in the /path/to/directory. Since the handler is printing the results, the output will reflect the flags chosen similar to `robust.py`:

The `-e` flag can be passed to cause all existing files in the directory (recurisively) to be submitted upon start.

```shell
(robust)$> robust-watchdog.py -a 26 -d ./ -n -e
.
...
.
.....
```

## robust-convict

`robust-convict` is a tool designed like `robust-watchdog` but its purpose is to help sort large directories of malware samples into directories, while downloading their corresponding reports.

Example Usage

```
robust-convict.py -n -a 26 -c ./tmp/clean/ -x ./tmp/dirty/ -r ./tmp/reports/ -z ./tmp/errors/ -d ./tmp/preprocess -j 10 -t zip -q
```

Options

```
usage: robust-convict.py [-h] [-u USER] [-p PASSWORD] [-i ATD IP] [-n] -a
                         ANALYZER_PROFILE -d DIRECTORY [-e] [-y SEVERITY]
                         [-c CLEANDIR] [-x DIRTYDIR] [-r REPORTDIR]
                         [-z ERRORDIR]
                         [-t {html,txt,xml,zip,json,ioc,stix,pdf,sample}]
                         [-j MAXTHREADS] [--version] [-v | -q]

Robust McAfee ATD Python CLI tool

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
                        		(default: ****<.robust>*****)
  -i ATD IP             (i)p or hostname address of ATD
                        		(default: atd.localhost.localdomain)
  -n                    do (n)ot verify the SSL certificate for the communications
                        		(default: True)

Watch parameters:
  -f                   (f)ollow and watch the directory for new files to submit
                          (default: False)
  -a ANALYZER_PROFILE   (a)nalyzer profile id to be used during analysis
                        		(default: None)
  -d DIRECTORY          (d)irectory to watch for events
                        		(default: None)
  -e                    (e)xisting files in directory will be submitted
                        		(default: False)
  -j MAXTHREADS         (j) max number of threads
                        		(default: 1)

Convict parameters:
  -y SEVERITY           (y) treat sample as dirty with this severity [0-5] or higher
                        		(default: 3)
  -c CLEANDIR           (c) move clean files to this directory
                        		(default: ~/robust/clean/)
  -x DIRTYDIR           (x) move processed dirty files to this directory
                        		(default: ~/robust/malware/)
  -r REPORTDIR          (r) save reports to this directory
                        		(default: ~/robust/reports/)
  -z ERRORDIR           (z) move error or skip files to this directory
                        		(default: ~/robust/errors/)
  -t {html,txt,xml,zip,json,ioc,stix,pdf,sample}
                        (t)ype of report requested
                        		(default: None)
```

## robust-reporter

`robust-reporter` is a tool designed to quickly summarize the downloaded `*.json` files in your 'reports' directory.

Options

```
usage: robust-reporter.py [-h] [-r REPORTDIR] [--version] [-v | -q]

Robust McAfee ATD Python CLI tool

optional arguments:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
  -v, --verbosity  increase output (v)erbosity
                   		(default: None)
  -q, --quiet      (q)uiet all output
                   		(default: False)

Reporter parameters:
  -r REPORTDIR     (r) reports are processed or stored using this directory
                   		(default: ~/robust/reports/)
```
Sample Run

```
$ robust-reporter.py
82344C9864B0F1D120C0D1AB7F7C54C3 (---) : Somewhat/probably is suspicious(Low-Medium) - 24sec
D012492123E4CF0CFB3A017A2E92C077 (Malware.Dynamic) : Malicious(High) - 194sec
DB273A97C54E3E23F411EA7C9B5A82DA (Malware.Dynamic) : Malicious (Medium) - 53sec
165A36C02B3FAAF4DE38F93A3DCB821B (---) : Somewhat/probably is suspicious(Low-Medium) - 36sec
D10195670651A40C46C22972CD839E89 (Artemis!D10195670651) : Malicious (Very High) - 32sec
8271093E0E78574428BBDDDA6F34A980 (Malware.Dynamic) : Malicious(High) - 192sec
86DAFA0262BF217F5344A3B057C0DB06 (Malware.Dynamic) : Malicious(High) - 193sec
8DA4CDC3E2EE16021F237EA7A043DA8E (Malware.Dynamic) : Malicious(High) - 191sec
```

## Tunning for Linux File Watchers

### iNotify Tuning Parameters

The inotify(7) subsystem has three important tunings that impact robust's directory watching.

```
/proc/sys/fs/inotify/max_user_instances impacts how many different root dirs you can watch.
/proc/sys/fs/inotify/max_user_watches impacts how many dirs you can watch across all watched roots.
/proc/sys/fs/inotify/max_queued_events impacts how likely it is that your system will experience a notification overflow.
```

You obviously need to ensure that `max_user_instances` and `max_user_watches` are set so that the system is capable of keeping track of your files.

`max_queued_events` is important to size correctly; if it is too small, the kernel will drop events and robust won't be able to report on them. Making this value bigger reduces the risk of this happening.

# Developers

## Install Development

```
$(robust)> pip install -r devel-requirements.txt

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

### Additional LICENSE information

A modified Fork of `atdcli.py` (Carlos Munoz - 2014).

https://pypi.python.org/pypi/atd

## VX Workshop Appliance Option

There is a fully operational Xubuntu 14.04 liveCD that includes:

* robust - https://github.com/shadowbq/robust-atd
* maltrieve - https://github.com/shadowbq/maltrieve
* vxcage - https://github.com/shadowbq/vxcage

It also includes

* hexeditors
* static analysis tools
* google chrome
* vmtools
* etc..

xubuntu-14.04.4-desktop-x86_64-VX-Workshop-0.4.iso (~ 1.2 GB)

Available to download with READMEs here: https://goo.gl/flcvew
