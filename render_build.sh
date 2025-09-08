#!/usr/bin/env bash
# exit on error
set -o errexit

pipenv install

flask db init
flask db migrate -m "Initial migration"

pipenv run upgrade