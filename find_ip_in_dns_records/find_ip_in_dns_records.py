# Search for a specific IP address across all domains in DNS Made Easy

import requests
import hmac
import hashlib
import argparse
from datetime import datetime, timezone

# Replace these with your actual API credentials
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
BASE_URL = "https://api.dnsmadeeasy.com/V2.0"


def generate_headers():
    timestamp = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    message = timestamp.encode("utf-8")
    signature = hmac.new(API_SECRET.encode("utf-8"), message, hashlib.sha1).hexdigest()

    headers = {
        "x-dnsme-apiKey": API_KEY,
        "x-dnsme-hmac": signature,
        "x-dnsme-requestDate": timestamp,
        "Accept": "application/json",
    }
    return headers


def get_domains():
    url = f"{BASE_URL}/dns/managed/"
    headers = generate_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"API Response for Domains: {response.status_code} - {response.text}")
        return []


def get_records(domain_id):
    url = f"{BASE_URL}/dns/managed/{domain_id}/records"
    headers = generate_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"API Response for Records: {response.status_code} - {response.text}")
        return []


def find_ip_in_records(target_ip):
    domains = get_domains()

    if not domains:
        print("No domains found or API request failed.")
        return

    for domain in domains:
        domain_id = domain["id"]
        domain_name = domain["name"]
        records = get_records(domain_id)

        for record in records:
            if record.get("type") == "A" and record.get("value") == target_ip:
                print(f"Found {target_ip} in {domain_name}")
                return

    print(f"IP {target_ip} not found in any domain records.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for an IP across DNS Made Easy domains")
    parser.add_argument("--ip", required=True, help="Target IP address to search for")
    args = parser.parse_args()

    find_ip_in_records(args.ip)
