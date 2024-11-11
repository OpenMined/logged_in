#!/bin/sh

set -e

if [ ! -d .venv ]; then
  uv venv
fi

. .venv/bin/activate

uv pip install --upgrade syftbox

echo "Running 'logged_in' with $(python3 --version) at '$(which python3)'"
python3 main.py

deactivate
