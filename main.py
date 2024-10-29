import os
import json
from datetime import datetime
from syftbox.lib import Client, SyftPermission


def should_run(output_file_path: str) -> bool:
    INTERVAL = 600
    if not os.path.exists(output_file_path):
        return True

    last_modified_time = datetime.fromtimestamp(os.path.getmtime(output_file_path))
    time_diff = datetime.now() - last_modified_time

    if time_diff.total_seconds() >= INTERVAL:
        return True
    return False


def main():
    # Prepare output file path
    client_config = Client.load()
    output_folder = client_config.datasite_path / "app_pipelines" / "timestamp_recorder"
    output_file_path = output_folder / "last_check_in.json"

    if not should_run(output_file_path):
        print("Skipping logged in checkin, not enough time has passed.")
        return

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Timestamp JSON
    timestamp_data = {"last_check_in": datetime.now().isoformat()}

    # Write timestamp to output file
    with open(output_file_path, "w") as f:
        json.dump(timestamp_data, f, indent=2)

    # Ensure permission file exists
    permission = SyftPermission.mine_with_public_read(email=client_config.email)
    permission.ensure(output_folder)

    print(f"Timestamp has been written to {output_file_path}")


if __name__ == "__main__":
    main()
