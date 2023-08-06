# python-pywana
[![Build Status](https://travis-ci.com/JM1/python-pywana.svg?branch=master)](https://travis-ci.com/JM1/python-pywana)

# Requirements

* Python 3.5+
* [Python 3 bindings for gobject-introspection libraries](https://pygobject.readthedocs.io/)
  (not packaged on PyPI, you need to install it from your distribution's repository - it's usually called python3-gi, python-gobject or pygobject)
* [GLib](https://developer.gnome.org/glib/) and [girepository](https://wiki.gnome.org/Projects/GObjectIntrospection)
* [dbus-python](https://pypi.org/project/dbus-python/)
* [psutil](https://pypi.org/project/psutil/)

# Howto

On [Debian Stretch](https://www.debian.org/releases/stretch/):
```sh
# Fetch dependencies
sudo apt-get install python3-pip python3-gi python3-dbus python3-psutil

# Install via PyPI
pip3 install --no-deps pywana
# option --no-deps is required because pip falsely assumes that dbus-python is
# not installed although it has been installed via debian package python3-dbus

# Execute
wana --help
```

# Build and upload package to PyPI manually
Ref.: 
 https://github.com/pypa/twine
 https://www.davidfischer.name/2012/05/signing-and-verifying-python-packages-with-pgp/

```sh
  
# Install python and build tools
sudo apt-get install python3 python3-pip
pip3 install twine

# Install project dependencies
# NOTE: libdbus-1-dev (>= 1.8) is required for building dbus-python
sudo apt-get install python3-dev libdbus-1-dev python3-gi
pip3 install -r requirements.txt
# instead of pip3 you can also install all required modules using your system package manager
sudo apt-get install python3-gi python3-dbus python3-psutil

# Create distributions
python3 setup.py build_all

# Sign distributions
gpg --detach-sign --armor dist/*

# Upload to Test PyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to PyPI:
twine upload dist/*
```

# Change PyPI password in .travis.yml
NOTE: [Travis CI does not allow for signing PyPI packages](https://github.com/travis-ci/dpl/issues/727)!
```sh
# Install Travis CI Client
# Ref.: 
#  https://github.com/travis-ci/travis.rb
#  https://docs.travis-ci.com/user/encryption-keys/
#  https://medium.com/@mikkokotila/deploying-python-packages-to-pypi-with-travis-works-9a6597781556
gem install travis
travis login --pro
# cd to git repo
travis encrypt --pro --add deploy.password
```
