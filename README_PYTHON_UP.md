# Python Up Burrito Command References

Get started

`$> curl -sL https://raw.githubusercontent.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL`

Install Test workspace

`$> mkvirtualenv robust`

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

* For more on Python Virtualenv Burrito [https://github.com/brainsik/virtualenv-burrito]
* For more on Puthon Virutalenv & Virtualenvwrapper [http://chrisstrelioff.ws/sandbox/2014/09/04/virtualenv_and_virtualenvwrapper_on_ubuntu_14_04.html]
