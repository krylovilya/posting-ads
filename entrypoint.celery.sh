#!/bin/bash

cd /server && python -m celery -A config.celery worker --loglevel=info
