#!/usr/bin/env python3
"""Bias Hunter: audit group fairness in a simple hiring dataset."""
import csv
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).with_name("hiring_bias_data.csv")
QUALIFIED_THRESHOLD = 70
FOUR_FIFTHS_RULE = 0.80


def load_rows(path=DATA):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["qualification_score"] = float(row["qualification_score"])
        row["model_decision"] = int(row["model_decision"])
    return rows


def audit(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row["group"]].append(row)

    metrics = {}
    for group, items in sorted(groups.items()):
        selection_rate = sum(r["model_decision"] for r in items) / len(items)
        avg_score = sum(r["qualification_score"] for r in items) / len(items)
        qualified = [r for r in items if r["qualification_score"] >= QUALIFIED_THRESHOLD]
        qualified_selection_rate = (
            sum(r["model_decision"] for r in qualified) / len(qualified) if qualified else 0.0
        )
        metrics[group] = {
            "n": len(items),
            "selection_rate": selection_rate,
            "avg_score": avg_score,
            "qualified_n": len(qualified),
            "qualified_selection_rate": qualified_selection_rate,
        }

    rates = [m["selection_rate"] for m in metrics.values()]
    disparate_impact_ratio = min(rates) / max(rates) if max(rates) else 0.0
    flagged = disparate_impact_ratio < FOUR_FIFTHS_RULE
    return metrics, disparate_impact_ratio, flagged


def main():
    rows = load_rows()
    metrics, di, flagged = audit(rows)

    print("=== Bias Hunter Report ===")
    for group, m in metrics.items():
        print(f"{group}: n={m['n']}, selection_rate={m['selection_rate']:.1%}, "
              f"avg_qualification={m['avg_score']:.1f}, "
              f"qualified_selection_rate={m['qualified_selection_rate']:.1%}")

    print(f"\nDisparate impact ratio: {di:.3f}")
    if flagged:
        print("BIAS FLAG: selection-rate ratio is below the 0.80 four-fifths heuristic.")
    else:
        print("No selection-rate disparity flagged by the four-fifths heuristic.")

    print("\nSuggested mitigation:")
    print("1. Remove protected-group attributes and obvious proxies from model features.")
    print("2. Rebalance/reweight training examples so qualified groups receive comparable influence.")
    print("3. Tune the decision threshold on validation data while monitoring group-wise selection and TPR.")
    print("4. Re-run this audit after mitigation and keep the fairness report with the model card.")


if __name__ == "__main__":
    main()
