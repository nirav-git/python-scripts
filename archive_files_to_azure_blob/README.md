# Archive Files to Azure Blob Storage

Sync and archive local files to Azure Blob Storage with retention-based filtering and optional source deletion.

## Prerequisites

```bash
pip install azure-storage-blob
```

## Usage

```bash
python archive_files_to_azure_blob.py --container <name> --connection-string "<conn_str>" --source <path> [options]
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--container` | Yes | — | Blob container name |
| `--connection-string` | Yes | — | Azure Storage connection string |
| `--source` | Yes | — | Local directory to archive |
| `--retention` | No | `0` | Skip files modified within this many days |
| `--delete` | No | `false` | Remove local files after upload |
| `--workers` | No | `10` | Number of concurrent upload threads |

## Example

```bash
python archive_files_to_azure_blob.py \
  --container myarchive \
  --connection-string "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;" \
  --source /data/logs \
  --retention 30 \
  --delete \
  --workers 5
```
