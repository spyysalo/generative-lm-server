#!/bin/bash

export FLASK_APP=lmserver
export FLASK_DEBUG=True
export FLASK_RUN_PORT=9099
flask run --host 0.0.0.0
