#!/usr/bin/env python3
"""Clean a messy CSV: normalize text/dates, fill missing ages, and remove duplicates."""
import csv
import statistics
import sys
from datetime import datetime
from pathlib import Path

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y")

def clean_name(value):
    return " ".join(value.strip().split()).title()

def clean_email(value):
    return value.strip().lower()

def clean_date(value):
    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return value

def scrub(src, dst):
    with open(src, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ages = [int(r["age"]) for r in rows if r.get("age", "").strip().isdigit()]
    fill_age = round(statistics.median(ages)) if ages else ""
    cleaned, seen = [], set()
    for row in rows:
        item = {
            "name": clean_name(row.get("name", "")),
            "email": clean_email(row.get("email", "")),
            "age": int(row["age"]) if row.get("age", "").strip().isdigit() else fill_age,
            "signup_date": clean_date(row.get("signup_date", "")),
        }
        key = (item["email"], item["signup_date"])
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(item)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "email", "age", "signup_date"])
        writer.writeheader()
        writer.writerows(cleaned)
    print(f"{len(rows)} input rows -> {len(cleaned)} clean rows: {dst}")

if __name__ == "__main__":
    src = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("messy_people.csv"))
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).with_name("clean_people.csv"))
    scrub(src, dst)
