# Python Up Burrito Command References

Virtualenv and virtualenvwrapper will let you define isolated Python runtime environments without harming the root or system python installation. This comes in handy when deploying several python applications and you want to isolate the different environments. Typically this is needed when runtime dependencies differ between frameworks or libraries in different applications.

Virtualenv Burrito enables with one command, have a working Python virtualenv + virtualenvwrapper environment.

You should have Python 2.7.10 (As of Mar 2018) compiled and ready to use as an alternative binary.

## Installing Python 2.7.x Latest as a system alternative

Installing the latest python binary as a system alternative is important because you do not want to break the operating system dependency chain. Installing as an alt-binary will allow for the latest to be mixed into `virutalenv` while living side-by-side with the system version.

* Centos: https://gist.github.com/shadowbq/57e194fb2331a3cdb0dae6231c1611e2 
* Debian/Ubuntu: https://gist.github.com/subsetpark/367f0d3fde503a1e481c

## Get started

Note: This is an online installer and you must understand the danger of piping into $Shell`.

`$> curl -sL https://raw.githubusercontent.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL`

## Install Test workspace

`$> mkvirtualenv --python=python2.7 robust`

Look inside the new `virutalenv robust`

```shell
$> workon robust

(robust)$> pip list
argparse (1.2.1)
pbr (0.10.0)
pip (1.5.6)
setuptools (5.4)
stevedore (1.1.0)
virtualenv (1.11.6)
virtualenv-clone (0.2.5)
virtualenvwrapper (4.3.1)
wsgiref (0.1.2)
```

Exit test ENV

``` shell
(robust)$>deactivate
$>
```

List the Available Python Virtual Environments

```shell
$> lsvirtualenv
robust
===
test-1
======
```


Blow away test ENV

```shell
$> rmvirtualenv robust
Removing robust...
```

## References

* For more on Python Virtualenv Burrito [https://github.com/brainsik/virtualenv-burrito]
* For more on Puthon Virutalenv & Virtualenvwrapper [http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html]
* Dangers of Piping to the shell [https://www.seancassidy.me/dont-pipe-to-your-shell.html]
* Centos more indepth: https://danieleriksson.net/2017/02/08/how-to-install-latest-python-on-centos/
