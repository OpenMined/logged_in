#!/bin/bash

echo "Running logged in checkin."
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one..."
    uv venv .venv
    echo "Virtual environment created successfully."
    uv pip install syftbox 
else
    echo "Virtual environment already exists."
fi
uv run python main.py
