# Data APIs — MLH Global Hack Week: Data

This mini-project fetches live Pokémon data from the public PokéAPI and stores it in a local SQLite database.

## What it demonstrates

- Calling a public REST API over HTTPS
- Parsing JSON responses
- Creating a database/table automatically
- Persisting API data in SQLite
- Updating existing records with an UPSERT
- Querying and printing stored records

## Run

```bash
python data_apis.py
```

By default it fetches Pokémon IDs 1, 4, 7, 25 and 39. You can also pass IDs or names:

```bash
python data_apis.py pikachu eevee charizard
```

The script creates `pokemon.db` in the same folder and stores the Pokémon ID, name, height, weight, base experience, types and fetch timestamp.

No API key and no third-party Python package are required.
