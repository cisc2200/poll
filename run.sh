#!/bin/bash

python3 -m venv venv
. venv/bin/activate
export FLASK_ENV=development
flask run --host=0.0.0.0
