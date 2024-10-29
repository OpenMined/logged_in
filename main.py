import os
import json
from datetime import datetime
from syftbox.lib import Client, SyftPermission


def main():
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
