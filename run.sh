#!/bin/bash

export FLASK_APP=lmserver
export FLASK_ENV=development
export FLASK_RUN_PORT=8001
flask run --host 0.0.0.0
