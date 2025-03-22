#!/bin/bash

set -x
set -e

# Force consistent and minimal locale
export LANG=C
export LC_ALL=C

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Initialize pyenv
eval "$("$PYENV_ROOT/bin/pyenv" init -)"

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