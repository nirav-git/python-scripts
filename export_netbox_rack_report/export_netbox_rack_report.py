# export_netbox_rack_report.py
# Export a CSV report of rack groups, racks, and devices from NetBox filtered by site

import requests
import csv
import argparse

HEADERS = {}


def fetch_data(base_url, endpoint):
    """Fetch all paginated data from a NetBox API endpoint."""
    url = f"{base_url}/api/{endpoint}/"
    results = []
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        results.extend(data["results"])
        url = data.get("next")
    return results


def build_report(rack_groups, racks, devices, target_sites):
    """Build structured report data filtered by target sites."""
    output = []

    for site in target_sites:
        site_rack_groups = [rg for rg in rack_groups if rg["site"] and rg["site"]["name"] == site]
        for rg in site_rack_groups:
            output.append({
                "Site": site,
                "Rack Group": rg["name"],
                "Rack": None,
                "Device": None,
                "Details": rg.get("description", ""),
            })

            group_racks = [r for r in racks if r["group"] and r["group"]["id"] == rg["id"]]
            for rack in group_racks:
                output.append({
                    "Site": site,
                    "Rack Group": rg["name"],
                    "Rack": rack["name"],
                    "Device": None,
                    "Details": f"Role: {rack['role']['name']}" if rack["role"] else "",
                })

                rack_devices = [d for d in devices if d["rack"] and d["rack"]["id"] == rack["id"]]
                for device in rack_devices:
                    details = ""
                    if device["device_role"] and device["device_type"]:
                        details = f"Role: {device['device_role']['name']}, Type: {device['device_type']['model']}"
                    output.append({
                        "Site": site,
                        "Rack Group": rg["name"],
                        "Rack": rack["name"],
                        "Device": device["name"],
                        "Details": details,
                    })

    return output


def main():
    parser = argparse.ArgumentParser(description="Export NetBox rack group report to CSV")
    parser.add_argument("--url", required=True, help="NetBox base URL (e.g. https://netbox.example.com)")
    parser.add_argument("--token", required=True, help="NetBox API token")
    parser.add_argument("--sites", required=True, nargs="+", help="Site names to include in the report")
    parser.add_argument("--output", default="rack_group_report.csv", help="Output CSV filename")
    args = parser.parse_args()

    HEADERS["Authorization"] = f"Token {args.token}"

    rack_groups = fetch_data(args.url, "dcim/rack-groups")
    racks = fetch_data(args.url, "dcim/racks")
    devices = fetch_data(args.url, "dcim/devices")

    report = build_report(rack_groups, racks, devices, set(args.sites))

    with open(args.output, "w", newline="") as csvfile:
        fieldnames = ["Site", "Rack Group", "Rack", "Device", "Details"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report)

    print(f"Rack group report generated: {args.output}")


if __name__ == "__main__":
    main()
