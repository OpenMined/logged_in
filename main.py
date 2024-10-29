import os
import json
from datetime import datetime
from syftbox.lib import Client, SyftPermission


def should_run() -> bool:
    INTERVAL = 600  # 10 minutes
    timestamp_file = "./script_timestamps/logged_in_checkin_last_run"
    os.makedirs(os.path.dirname(timestamp_file), exist_ok=True)

    now = datetime.now().timestamp()
    time_diff = INTERVAL  # default to running if no file exists
    if os.path.exists(timestamp_file):
        try:
            with open(timestamp_file, "r") as f:
                last_run = int(f.read().strip())
                time_diff = now - last_run
        except (FileNotFoundError, ValueError):
            print(f"Unable to read timestamp file: {timestamp_file}")

    if time_diff >= INTERVAL:
        with open(timestamp_file, "w") as f:
            f.write(f"{int(now)}")
        return True
    return False


def main():
    if not should_run():
        print("Skipping logged in checkin, not enough time has passed.")
        return

    # Load the client configuration
    client_config = Client.load()

    # Timestamp JSON
    timestamp_data = {"last_check_in": datetime.now().isoformat()}

    # Prepare output folders
    output_folder = client_config.datasite_path / "app_pipelines" / "timestamp_recorder"
    os.makedirs(output_folder, exist_ok=True)

    # Write timestamp to output file
    output_file_path = output_folder / "last_check_in.json"
    with open(output_file_path, "w") as f:
        json.dump(timestamp_data, f, indent=2)

    # Ensure permission file exists
    permission = SyftPermission.mine_with_public_read(email=client_config.email)
    permission.ensure(output_folder)

    print(f"Timestamp has been written to {output_file_path}")


if __name__ == "__main__":
    main()
