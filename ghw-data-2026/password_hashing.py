#!/usr/bin/env python3
"""Tiny authentication demo using PBKDF2-HMAC-SHA256 password hashing."""
import hashlib
import hmac
import json
import secrets
import sys
from pathlib import Path

DB = Path(__file__).with_name("users.json")
ITERATIONS = 310_000

def load_users():
    if not DB.exists():
        return {}
    return json.loads(DB.read_text())

def save_users(users):
    DB.write_text(json.dumps(users, indent=2))

def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return salt.hex(), digest.hex()

def register(username, password):
    users = load_users()
    if username in users:
        raise SystemExit("User already exists.")
    salt, digest = hash_password(password)
    users[username] = {"salt": salt, "hash": digest, "iterations": ITERATIONS}
    save_users(users)
    print(f"Registered {username}. Password itself was never stored.")

def login(username, password):
    users = load_users()
    record = users.get(username)
    if not record:
        print("Login failed.")
        return False
    salt = bytes.fromhex(record["salt"])
    computed = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, record["iterations"]
    ).hex()
    ok = hmac.compare_digest(computed, record["hash"])
    print("Login successful." if ok else "Login failed.")
    return ok

def main():
    if len(sys.argv) != 4 or sys.argv[1] not in {"register", "login"}:
        raise SystemExit("Usage: python password_hashing.py [register|login] USERNAME PASSWORD")
    if sys.argv[1] == "register":
        register(sys.argv[2], sys.argv[3])
    else:
        login(sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
