#!/bin/bash

set +x

# Force a clean environment to prevent locale weirdness
export LANG=C
export LC_ALL=C

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$HOME/.local/bin:$PATH"
eval "$("$PYENV_ROOT/bin/pyenv" init -)"

# Move to project directory
cd "$HOME/porkbun_updater" || {
  echo "[$(date)] Failed to cd into porkbun_updater" >> "$HOME/porkbun_updater/cron.log"
  exit 1
}

# Log environment for debugging
echo "[$(date)] Starting DNS update" >> "$HOME/porkbun_updater/cron.log"
env >> "$HOME/porkbun_updater/cron.env.log"

# Run your command and capture stderr separately
~/.local/bin/pdm run python porkbun_updater/main.py set-dns-record-by-type --record-type A >> "$HOME/porkbun_updater/cron.log" 2>> "$HOME/porkbun_updater/cron.err.log"

echo "[$(date)] DNS update finished" >> "$HOME/porkbun_updater/cron.log"