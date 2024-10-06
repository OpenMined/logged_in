#!/bin/bash

# Create a directory to store timestamps
TIMESTAMP_DIR="./script_timestamps"
mkdir -p "$TIMESTAMP_DIR"

# Function to check if enough time has passed to run the task again
function should_run() {
    local section=$1
    local interval=$2
    local timestamp_file="$TIMESTAMP_DIR/${section}_last_run"

    if [ ! -f "$timestamp_file" ]; then
        return 0
    fi

    last_run=$(cat "$timestamp_file")
    current_time=$(date +%s)
    time_diff=$((current_time - last_run))

    if [ $time_diff -ge $interval ]; then
        return 0
    else
        return 1
    fi
}

# Function to update the timestamp for a section
function update_timestamp() {
    local section=$1
    local timestamp_file="$TIMESTAMP_DIR/${section}_last_run"
    date +%s > "$timestamp_file"
}

# Main function to run the logged in checkin
function run_logged_in_checkin() {
    local section="logged_in_checkin"
    local interval=300  # 5 minutes

    if should_run "$section" $interval; then
        echo "Running logged in checkin."
        python3 main.py
        echo "Logged in checkin completed."
        update_timestamp "$section"
    else
        echo "Skipping logged in checkin, not enough time has passed."
    fi
}

# Run the logged in checkin
run_logged_in_checkin
