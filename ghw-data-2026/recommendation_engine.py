#!/usr/bin/env python3
"""Small content-based movie recommender using only Python's standard library."""
from collections import Counter
from math import sqrt

MOVIES = {
    "The Matrix": {"sci-fi", "action"},
    "Blade Runner 2049": {"sci-fi", "drama"},
    "Arrival": {"sci-fi", "drama"},
    "John Wick": {"action", "thriller"},
    "Knives Out": {"mystery", "comedy"},
    "The Grand Budapest Hotel": {"comedy", "drama"},
    "Spirited Away": {"animation", "fantasy"},
    "Princess Mononoke": {"animation", "fantasy", "action"},
    "Interstellar": {"sci-fi", "drama"},
}

def vector(genres):
    return Counter(genres)

def cosine(a, b):
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = sqrt(sum(v*v for v in a.values()))
    nb = sqrt(sum(v*v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def recommend(liked, n=5):
    profile = Counter()
    for title in liked:
        profile.update(MOVIES[title])
    scored = []
    for title, genres in MOVIES.items():
        if title not in liked:
            scored.append((cosine(profile, vector(genres)), title))
    return sorted(scored, reverse=True)[:n]

if __name__ == "__main__":
    liked = ["The Matrix", "Arrival"]
    print("Liked:", ", ".join(liked))
    print("Recommendations:")
    for score, title in recommend(liked):
        print(f"  {score:.3f}  {title}")
