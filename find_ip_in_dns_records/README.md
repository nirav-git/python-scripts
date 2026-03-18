# Find IP in DNS Records

Search for a specific IP address across all managed domains in DNS Made Easy.

## Prerequisites

```bash
pip install requests
```

## Setup

Update `API_KEY` and `API_SECRET` in the script with your DNS Made Easy API credentials.

## Usage

```bash
python find_ip_in_dns_records.py --ip <ip_address>
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--ip` | Yes | — | Target IP address to search for |

## Example

```bash
python find_ip_in_dns_records.py --ip 10.0.0.1
```
