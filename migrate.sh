#!/bin/bash -l

set -e

export WORKON_HOME=~/venvs
source /usr/local/bin/virtualenvwrapper.sh
workon katana
python /home/katana/katana/manage.py migrate
