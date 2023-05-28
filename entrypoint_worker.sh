#!/bin/sh
cd /usr/src/dsc_app/backend/
python /usr/src/dsc_app/health_check.py &
python v1/pubsub.py