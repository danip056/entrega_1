#!/bin/sh
cd /usr/src/dsc_app/backend/;celery --app=v1.celery_config.celery_init:dsc_app worker -B --without-heartbeat --without-gossip --without-mingle --loglevel=INFO