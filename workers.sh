#!/bin/bash
# Start workers if they are not running, else restarts them.
celery multi restart default -A lol_stats2 -l info -Q default -c 1 --autoreload --logfile=log/%N.log --pidfile=%N.pid
celery multi restart match_ids -A lol_stats2 -l info -Q match_ids -c 1 --autoreload --logfile=log/%N.log --pidfile=%N.pid
celery multi restart store -A lol_stats2 -l info -Q store -c 1 --autoreload --logfile=log/%N.log --pidfile=%N.pid

# Tail all logs using django color scheme.
# multitail -s 4 -cS django log/default.log -cS django log/match_ids.log -cS django log/store.log -cS django log/debug.log

# ...or with uneven column sizes.
# multitail -sw 40,40,40,100 -cS django log/default.log -cS django log/match_ids.log -cS django log/store.log -cS django log/debug.log