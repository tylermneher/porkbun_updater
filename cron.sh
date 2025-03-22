#!/bin/bash

set +x

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$HOME/.local/bin:$PATH"
eval "$("$PYENV_ROOT/bin/pyenv" init -)"

# Move to project directory
cd "$HOME/porkbun_updater" || {
  echo "[$(date)] Failed to cd into porkbun_updater" >> "$HOME/porkbun_updater/cron.log"
  exit 1
}

# Timestamp before running
echo "[$(date)] Starting DNS update" >> "$HOME/porkbun_updater/cron.log"

# Use full path to pdm and log both stdout and stderr
pdm run python porkbun_updater/main.py set-dns-record-by-type --record-type A >> "$HOME/porkbun_updater/cron.log" 2>&1

# Timestamp after running
echo "[$(date)] DNS update finished" >> "$HOME/porkbun_updater/cron.log"