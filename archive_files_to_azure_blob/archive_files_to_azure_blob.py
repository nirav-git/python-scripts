# Sync and archive local files to Azure Blob Storage with retention-based filtering

import argparse
import os
import stat
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

from azure.storage.blob import BlobServiceClient


def upload_file(filepath, base_path, container, remove_after, cutoff):
    """Upload a single file to blob storage if it's older than the cutoff date."""
    if not filepath.is_file():
        return

    modified_at = datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc)
    relative_path = str(filepath.relative_to(base_path))

    if modified_at >= cutoff:
        log_action(filepath, modified_at, "Skipped")
        return

    blob = container.get_blob_client(relative_path)
    remote_modified = get_remote_timestamp(blob)

    if remote_modified >= modified_at:
        if remove_after:
            safe_delete(filepath, modified_at)
        return

    with open(filepath, "rb") as fh:
        blob.upload_blob(fh, overwrite=True)

    status = "Uploaded"
    if remove_after:
        if not safe_delete(filepath, modified_at):
            status = "Uploaded (delete failed)"

    log_action(filepath, modified_at, status)


def get_remote_timestamp(blob_client):
    """Return the last-modified time of a remote blob, or datetime.min if it doesn't exist."""
    try:
        return blob_client.get_blob_properties().last_modified
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def safe_delete(filepath, modified_at):
    """Attempt to remove a local file. Returns True on success."""
    try:
        filepath.chmod(stat.S_IWRITE)
        filepath.unlink()
        log_action(filepath, modified_at, "Deleted")
        return True
    except Exception:
        print(f"ERROR: could not delete {filepath}")
        return False


def log_action(filepath, modified_at, action):
    print({"file": str(filepath), "modified": str(modified_at), "action": action})


def main(config):
    client = BlobServiceClient.from_connection_string(config.connection_string)
    container = client.get_container_client(config.container)
    base = Path(config.source)
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=config.retention)

    print(f"Archiving files from: {base}")
    print(f"Cutoff date: {cutoff}")

    with ThreadPoolExecutor(max_workers=config.workers) as executor:
        for dirpath, _, filenames in os.walk(base):
            for fname in filenames:
                executor.submit(
                    upload_file,
                    Path(dirpath) / fname,
                    base,
                    container,
                    config.delete,
                    cutoff,
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Archive local files to Azure Blob Storage"
    )
    parser.add_argument("--container", required=True, help="Blob container name")
    parser.add_argument("--connection-string", required=True, help="Azure Storage connection string")
    parser.add_argument("--source", required=True, help="Local directory to archive")
    parser.add_argument("--retention", type=int, default=0, help="Skip files modified within this many days")
    parser.add_argument("--delete", action="store_true", help="Remove local files after upload")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent upload threads")
    args = parser.parse_args()

    start = time.time()
    main(args)
    print(f"Completed in {time.time() - start:.2f}s")
