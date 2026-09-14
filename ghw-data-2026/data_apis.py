#!/usr/bin/env python3
"""MLH GHW Data: fetch public API data and store it in a database."""

import json
import sqlite3
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://pokeapi.co/api/v2/pokemon/{id_or_name}"
DB = Path(__file__).with_name("pokemon.db")


def fetch_pokemon(id_or_name):
    url = API.format(id_or_name=id_or_name)
    req = urllib.request.Request(url, headers={"User-Agent": "GHW-Data-APIs/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            height INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            base_experience INTEGER,
            types TEXT NOT NULL,
            fetched_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def store_pokemon(conn, data):
    types = ",".join(
        slot["type"]["name"]
        for slot in sorted(data["types"], key=lambda x: x["slot"])
    )
    fetched_at = datetime.now(timezone.utc).isoformat()

    conn.execute(
        """
        INSERT INTO pokemon
            (id, name, height, weight, base_experience, types, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            height = excluded.height,
            weight = excluded.weight,
            base_experience = excluded.base_experience,
            types = excluded.types,
            fetched_at = excluded.fetched_at
        """,
        (
            data["id"],
            data["name"],
            data["height"],
            data["weight"],
            data.get("base_experience"),
            types,
            fetched_at,
        ),
    )
    conn.commit()


def show_rows(conn):
    rows = conn.execute(
        "SELECT id, name, height, weight, base_experience, types, fetched_at "
        "FROM pokemon ORDER BY id"
    ).fetchall()
    print("\nStored records:")
    for row in rows:
        print(row)


def main():
    targets = sys.argv[1:] or ["1", "4", "7", "25", "39"]

    with sqlite3.connect(DB) as conn:
        init_db(conn)

        for target in targets:
            try:
                data = fetch_pokemon(target)
                store_pokemon(conn, data)
                print(f"Saved #{data['id']} {data['name']} from PokéAPI")
            except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as exc:
                print(f"Could not fetch {target}: {exc}")

        show_rows(conn)
        print(f"\nSQLite database: {DB}")


if __name__ == "__main__":
    main()
