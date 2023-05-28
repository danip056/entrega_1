#!/bin/sh
cd /usr/src/dsc_app/backend/;alembic -c ./v1/alembic_prod.ini upgrade head;uvicorn main:app --reload --host 0.0.0.0 --port 8080