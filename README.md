##Setup

Install virtualenvwrapper if not already present:

[http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation)

Find out where python3 lives:

`which python3`

Setup a development virtualenv:

`mkvirtualenv --python=/path/to/python3 lol_stats2_dev`

Install dependencies:

`pip install -r requirements/development.txt`

There is a requirements file for each environment; it is recommended that you create a
virtualenv for each one (e.g. using production.txt will not install debugging packages).

virtualenvwrapper provides hooks for pre- and post- activation and deactivation of
each virtualenv under `$VIRTUAL_ENV/bin` (by default this is in ~/.virtualenvs).
It is recommended that you add the following to the development virtualenv
"postactivate" script:

`export DJANGO_SETTINGS_MODULE="lol_stats2.settings.development"`

and "predeactivate" script:

`unset DJANGO_SETTINGS_MODULE`

You can follow suit for each virtualenv (production, staging, etc).

Executing `manage.py runserver` should now reflect the environment-specific settings
when starting up.

You may also configure your SECRET_KEY environment variables via "postactivate" and
"predeactivate" scripts.
