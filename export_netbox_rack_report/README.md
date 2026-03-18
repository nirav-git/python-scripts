# Export NetBox Rack Report

Export a CSV report of rack groups, racks, and devices from NetBox filtered by site.

## Prerequisites

```bash
pip install requests
```

## Usage

```bash
python export_netbox_rack_report.py --url <netbox_url> --token <api_token> --sites <site1> <site2> [options]
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--url` | Yes | — | NetBox base URL (e.g. `https://netbox.example.com`) |
| `--token` | Yes | — | NetBox API token |
| `--sites` | Yes | — | One or more site names to include in the report |
| `--output` | No | `rack_group_report.csv` | Output CSV filename |

## Example

```bash
python export_netbox_rack_report.py \
  --url https://netbox.example.com \
  --token abc123 \
  --sites DC1 DC2 DC3 \
  --output my_report.csv
```
