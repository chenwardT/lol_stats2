#lol_stats2

_This is the data-harvesting, number-crunching, REST-serving backend.
The frontend can be found here: https://github.com/chenwardT/lol_stats2-frontend_

> "There is an epidemic failure within the game to understand what is really happening"
> 
> --Peter Brand (Jonah Hill), "Moneyball"

lol_stats2 is a website that aims to provide unique insight into the competitive
multiplayer game [League of Legends](http://leagueoflegends.com), developed by Riot Games.
Through querying the official [League of Legends API](http://developer.riotgames.com/)
it accesses match, player, and team data with the aim of finding patterns and making
distinctions that may not be apparent to players/spectators of the game.

##Background
The site is built on `Django`, a Python web framework.

API access is provided by [`RiotWatcher`](https://github.com/pseudonym117/Riot-Watcher).

Asynchronous jobs, such as fetching and analyzing data, are performed by `Celery`,
a distributed task queue. It is uses `RabbitMQ` as its broker and `Redis` as a result
store.
        
Stored data is exposed via [`Django-Rest-Framework`](http://www.django-rest-framework.org/)
with and consumed by a JS frontend.

This project and its author are not affiliated with Riot Games.

##Setup

###Virtual Environment
Install virtualenvwrapper if not already present:

[http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation]
(http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation)

Find out where python3 lives:

    which python3

Setup a development virtualenv:

    mkvirtualenv --python=/path/to/python3 lol_stats2_dev

Install dependencies:

    pip install -r requirements/development.txt

There is a requirements file for each environment; it is recommended that you create a
virtualenv for each one (e.g. using production.txt will not install debugging packages).

virtualenvwrapper provides hooks for pre- and post- activation and deactivation of
each virtualenv under `$VIRTUAL_ENV/bin` (by default this is in ~/.virtualenvs).
It is recommended that you add the following to the development virtualenv
"postactivate" script:

    export DJANGO_SETTINGS_MODULE="lol_stats2.settings.development"

and "predeactivate" script:

    unset DJANGO_SETTINGS_MODULE

You can follow suit for each virtualenv (production, staging, etc).

Executing `manage.py runserver` should now reflect the environment-specific settings
when starting up.

You should configure Django's `SECRET_KEY` and RiotWatcher's `RIOT_API_KEY` environment variables via 
"postactivate" and "predeactivate" scripts.

Additionally, `CELERY_ALWAYS_EAGER`, should be set in your testing
 virtualenv, otherwise Celery tasks won't be run against the test database! The value of the
 variable does not matter, but it must exist.

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
3 queues. This is likely to change as development progresses. See settings/base.py
for details.

Workers may be started independently due to an [issue](https://github.com/celery/celery/issues/1839)
with celery multi:

    celery -A lol_stats2 worker -l info -Q default -n default.%h
    celery -A lol_stats2 worker -l info -Q match_ids -n match_ids.%h
    celery -A lol_stats2 worker -l info -Q store -n store.%h

Alternatively, you may start (and restart!) workers via `workers_restart.sh` but
beware of `RuntimeError: Acquire on closed pool`, as it uses `celery multi`.

The celery monitor is optional, and listens on port 5555 by default:

    celery -A lol_stats2 flower

See [http://celery.readthedocs.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor](http://celery.readthedocs.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor).

Finally, the rabbitmq monitor (defaults; port: 15672, login: guest/guest) can be
enabled via:

    rabbitmq-plugins enable rabbitmq_management

This only needs to be run once and by default will start on boot.
  
See [https://www.rabbitmq.com/management.html](https://www.rabbitmq.com/management.html).

##Tests

Before running tests, ensure CELERY_ALWAYS_EAGER is set. See bottom of __Setup__ section.

Selenium tests use PyVirtualDisplay to run in a headless environment. PyVirtualDisplay in turn
requires Xvfb, Xephyr, or Xvnc to be installed.

To run tests:
```
./manage.py test
```
