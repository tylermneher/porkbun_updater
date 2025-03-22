#!/bin/bash

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$("$PYENV_ROOT/bin/pyenv" init -)"

# Move to project directory
cd "$HOME/porkbun_updater" || exit 1

# Timestamp
echo "[$(date)] Starting DNS update" >> "$HOME/porkbun_updater/cron.log"

# Run your command with pdm, log stdout and stderr
pdm run python porkbun_updater/main.py set-dns-record-by-type --record-type A >> "$HOME/porkbun_updater/cron.log" 2>&1

# Completion marker
echo "[$(date)] DNS update finished" >> "$HOME/porkbun_updater/cron.log"