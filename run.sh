#!/bin/sh
set -e

while true; do
    if [ ! -d ".venv" ]; then
        echo "Virtual environment not found. Creating one..."
        uv venv -p 3.12 .venv
        echo "Virtual environment created successfully."
    else
        echo "Virtual environment already exists."
    fi

    uv pip install -U syftbox

    . .venv/bin/activate

    echo "Running 'logged_in' with $(python3 --version) at '$(which python3)'"
    uv run python3 main.py

    deactivate

    echo "Sleeping for 10 seconds..."
    sleep 10
done

