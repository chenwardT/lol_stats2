#lol_stats2

##Setup

###Virtual Environment
Install virtualenvwrapper if not already present:

[http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation]
(http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation)

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

You may also configure your SECRET_KEY and RIOT_API_KEY environment variables via 
"postactivate" and "predeactivate" scripts.

###Database Caveat

Django does not create an index for the matches app's `ParticipantTimeline` model's
`participant` field despite `db_index=True` being set.

To account for this, the following will create the proper index in Postgres:
 
     CREATE INDEX matches_participanttimeline_idx
      ON matches_participanttimeline
      USING btree
      (participant_id);


##Celery

Celery is configured to use a locally hosted AMQP broker with a Redis result backend.
A single topic-type exchange, 'default', is configured to route messages to one of
3 queues. See settings/base.py for details.

Workers should be started independently due to an issue with celery multi:

`celery -A lol_stats2 worker -l info -Q default -n default.%h`

`celery -A lol_stats2 worker -l info -Q match_ids -n match_ids.%h`

`celery -A lol_stats2 worker -l info -Q store -n store.%h`

Alternatively, you may start (and restart!) workers via `workers_restart.sh` but
beware of `RuntimeError: Acquire on closed pool`, as it uses `celery multi`.

The celery monitor is optional, and listens on port 5555 by default:

`celery -A lol_stats2 flower`

See [http://celery.readthedocs.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor](http://celery.readthedocs.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor).

Finally, the rabbitmq monitor (defaults; port: 15672, login: guest/guest) can be
enabled via:

`rabbitmq-plugins enable rabbitmq_management`

This only needs to be run once and by default will start on boot.
  
See [https://www.rabbitmq.com/management.html](https://www.rabbitmq.com/management.html).

##Tests

If Selenium throws:

`selenium.common.exceptions.WebDriverException: Message: The browser appears to have 
exited before we could connect. If you specified a log_file in the FirefoxBinary
constructor, check it for details.`

...check the following things:

- You have a DISPLAY environment variable set (:0 by default):

    - `export DISPLAY=:0`

- X is running on that display.

- Someone may need to be logged into your X display manager.

Alternatively, you can use pyvirtualdisplay if you are running in a headless
configuration.