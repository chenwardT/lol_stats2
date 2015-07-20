#!/bin/bash
# Stop workers.
celery multi stop default --logfile=log/%N.log --pidfile=%N.pid
celery multi stop match_ids --logfile=log/%N.log --pidfile=%N.pid
celery multi stop store --logfile=log/%N.log --pidfile=%N.pid
