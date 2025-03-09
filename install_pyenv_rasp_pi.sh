#!/usr/bin/env bash

# Check if pyenv is already installed
if ! command -v pyenv &> /dev/null; then
  curl -fsSL https://pyenv.run | bash
fi

# Add pyenv to bashrc if not already added
if ! grep -q 'export PYENV_ROOT="$HOME/.pyenv"' ~/.bashrc; then
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
fi

if ! grep -q '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' ~/.bashrc; then
  echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
fi

if ! grep -q 'eval "$(pyenv init - bash)"' ~/.bashrc; then
  echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
fi

# Source bashrc to apply changes
source ~/.bashrc

# Check if Python 3.13 is already installed
if ! pyenv versions | grep -q '3.13'; then
  pyenv install 3.13
fi

# Set global Python version to 3.13
pyenv global 3.13

# Upgrade pip and install pdm
pip install --upgrade pip
pip install --upgrade pdm

pdm install