import os
import json
from datetime import datetime, UTC
from syft_core import Client
from syft_core.permissions import SyftPermission


def should_run(output_file_path: str) -> bool:
    INTERVAL = 300  # 5 minutes
    if not os.path.exists(output_file_path):
        return True

    last_modified_time = datetime.fromtimestamp(os.path.getmtime(output_file_path))
    time_diff = datetime.now() - last_modified_time

    if time_diff.total_seconds() >= INTERVAL:
        return True
    return False


def main():
    # Prepare output file path
    client = Client.load()
    output_folder = client.app_data("timestamp_recorder")
    output_file_path = output_folder / "last_check_in.json"

    if not should_run(output_file_path):
        print(f"Skipping check for {output_file_path}")
        return

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Timestamp JSON
    timestamp_data = {"last_check_in": datetime.now(UTC).isoformat()}

    # Write timestamp to output file
    with open(output_file_path, "w") as f:
        json.dump(timestamp_data, f, indent=2)

    # Ensure permission file exists
    permission = SyftPermission.mine_with_public_read(client, output_folder)
    permission.save(output_folder)

    print("Set checkin time to", timestamp_data["last_check_in"])


if __name__ == "__main__":
    main()
