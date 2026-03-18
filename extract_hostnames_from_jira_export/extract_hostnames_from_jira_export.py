# Extract hostnames matching a pattern from a Jira CSV export

import re
import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Extract hostnames from a Jira CSV export")
    parser.add_argument("--file", required=True, help="Path to Jira CSV export file")
    parser.add_argument("--pattern", default=r"\[Decom\] (\S+)", help="Regex pattern to extract hostname from Summary column")
    args = parser.parse_args()

    df = pd.read_csv(args.file)
    df["Hostname"] = df["Summary"].str.extract(args.pattern)

    unique_hostnames = df["Hostname"].dropna().unique()
    for hostname in unique_hostnames:
        print(hostname)


if __name__ == "__main__":
    main()
