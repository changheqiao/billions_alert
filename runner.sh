#!/usr/bin/env bash
APP="runner"
linux_user="app"
os=`uname`
BASE="/home/app/www/billions_alert"
TAG=$@

if [[ "${os}"x = "Darwin"x ]]; then
    BASE=`pwd`
    venv="${BASE}/venv"
    export PYENV_ROOT="${BASE}/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    source ${venv}/bin/activate
elif [[ "${os}"x  = "Linux"x ]]; then
    BASE=`pwd`
    venv="${BASE}/venv"
    source ${venv}/bin/activate
    export PYENV_ROOT="${venv}"
fi

python -u start_web.py