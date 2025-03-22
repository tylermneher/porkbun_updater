#!/bin/bash

if [ -z "$HOME" ]; then
  echo "HOME is not set"
  exit 1
fi

if [ -e $HOME/.bashrc ]; then
  echo "Need a ~/.bashrc file initialized with pyenv"
  exit 1
fi

source $HOME/.bashrc
set -x
set -e

# Force consistent and minimal locale
export LANG=C
export LC_ALL=C

# Move to project dir
cd "$HOME/porkbun_updater" || exit 1

# Use the exact Python that PDM is using
VENV_PYTHON=$(pdm info --python)

# Log start
echo "[$(date)] Starting DNS update" > "$HOME/porkbun_updater/cron.log"

# Run the script directly with venv python
"$VENV_PYTHON" porkbun_updater/main.py set-dns-record-by-type --record-type A

# Log end
echo "[$(date)] DNS update finished" >> "$HOME/porkbun_updater/cron.log"