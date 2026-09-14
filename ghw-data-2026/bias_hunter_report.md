# The Bias Hunter — Fairness Audit

This demo audits a synthetic hiring dataset to test whether a model favors one group over another.

## Results

| Group | Candidates | Selection rate | Avg. qualification | Qualified candidates (score >= 70) | Qualified selection rate |
|---|---:|---:|---:|---:|---:|
| Group_A | 10 | 70.0% | 76.4 | 7 | 100.0% |
| Group_B | 10 | 30.0% | 77.4 | 8 | 37.5% |

The overall disparate-impact ratio is **0.429** (30% / 70%), well below the common **0.80 four-fifths heuristic**, so the script flags a likely group disparity. This is especially notable because Group_B has a slightly higher average qualification score, yet a much lower selection rate.

## Proposed mitigation

1. Remove protected-group attributes and obvious proxy variables from model inputs where they are not legitimately required.
2. Rebalance or reweight training data so similarly qualified groups have comparable influence during training.
3. Tune the decision threshold on validation data while monitoring group-wise selection rates and true-positive rates.
4. Re-run the fairness audit after mitigation and include the results in the model card.

The included `bias_hunter.py` script computes these metrics automatically from `hiring_bias_data.csv`.
