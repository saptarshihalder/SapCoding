# Global Hack Week: Data — Challenge Projects

Small, runnable projects for the September 2026 MLH Global Hack Week: Data challenges. All three use Python's standard library, so they run without installing packages.

## 1. Password Hashing

`password_hashing.py` is a tiny registration/login application. It salts each password with a random 16-byte salt, derives the stored hash with PBKDF2-HMAC-SHA256 (310,000 iterations), and verifies logins with constant-time comparison. Plaintext passwords are never stored.

```bash
python password_hashing.py register demo "correct horse battery staple"
python password_hashing.py login demo "correct horse battery staple"
```

## 2. Recommendation Engine

`recommendation_engine.py` builds a simple content profile from liked movie genres and ranks unseen movies using cosine similarity.

```bash
python recommendation_engine.py
```

## 3. Automated Data Scrub

`data_scrubber.py` takes deliberately messy CSV data and automatically:

- normalizes names and email addresses;
- parses several date formats into ISO dates;
- fills missing/invalid ages with the median valid age;
- removes duplicate records;
- writes a clean analysis-ready CSV.

The repository includes both `messy_people.csv` and the resulting `clean_people.csv`.

```bash
python data_scrubber.py
```

## Verification

The scripts were executed locally before being committed. The recommender produced ranked recommendations, the scrubber reduced the 5-row messy sample to 4 cleaned rows, and the authentication demo was tested with both successful and failed logins.
