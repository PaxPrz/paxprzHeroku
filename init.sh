#!/bin/bash

source .venv/bin/activate

gunicorn --bind 0.0.0.0:9500 -w 2 app:app
