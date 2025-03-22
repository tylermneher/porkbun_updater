#!/bin/bash

# Setup pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Move to project directory
cd "$HOME/porkbun_updater" || exit 1

# Run your command with pdm
pdm run python porkbun_updater/main.py set-dns-record-by-type --record-type A