# Extract Hostnames from Jira Export

Extract unique hostnames from a Jira CSV export based on a regex pattern applied to the Summary column.

## Prerequisites

```bash
pip install pandas
```

## Usage

```bash
python extract_hostnames_from_jira_export.py --file <csv_path> [--pattern <regex>]
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--file` | Yes | — | Path to the Jira CSV export file |
| `--pattern` | No | `\[Decom\] (\S+)` | Regex pattern to extract hostname from the Summary column |

## Example

```bash
python extract_hostnames_from_jira_export.py --file jira_export.csv

python extract_hostnames_from_jira_export.py --file jira_export.csv --pattern "\[Decom\] (DC1-\w+)"
```
