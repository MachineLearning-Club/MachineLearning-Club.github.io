# Study Space Challenge — independent classroom practice

**Not an official FiiCode problem, dataset, submission or scoring rubric.**
This self-contained Machine Learning Club project contains only synthetic examples.
It collects no data about actual students, school rooms or persons.

## Problem and data

Input: occupancy percentage (0–100); illustrative noise level (20–95);
Wi-Fi strength (1–5); power outlets available (0 or 1); desired study duration
(15–120 minutes). Output: avoid, consider, or good.

These are fabricated suitability labels based on overlapping artificial
profiles, not independently verified opinions or physical properties.
Dataset generator: scripts/build_fiicode_data.py in the website repository.
Random seed: 20261117. The complete 240 rows have unique IDs and features,
balanced labels (80 per class). No duplicate rows cross partitions.

| Split | Rows | Per class | Purpose |
| --- | ---: | ---: | --- |
| Train | 150 | 50 | Store labelled examples for k-NN |
| Validation | 45 | 15 | Compare k; choose one setting |
| Final test | 45 | 15 | Report one frozen result |

The ID column is not a feature. All CSVs and labels are public educational
fixtures. The hold-out is not a secret competition leaderboard.

## Run (Python standard library only)

Unzip, open a terminal in the study-space folder, then:

    python evaluate.py
    python evaluate.py --predict 35 40 4 1 60
    python -m unittest test_project.py -v

No pip installation, accounts, credentials or network access are necessary.
For the offline browser UI open app.html directly from disk. It includes
the training and validation data within the page, so file:// works.
The online demo is https://machinelearning-club.github.io/projects/study-space/

## Prediction algorithm

Five features in this order: occupancy, noise, wifi, outlets, minutes.
Scaled weighted squared distance uses scales (100,60,4,1,100) and
fixed weights (1,1,0.7,0.30,0.15). A sample is compared with all
150 training rows, sorted by distance then synthetic ID. Its k nearest
labelled examples vote. Ties use summed distance, then alphabetical
class order. Allowed k values are 1, 3, 5, 7.

Validation reference scores:
  Constant baseline: 15/45 (33.3%), predicts avoid
  k=1: 41/45 (91.1%); k=3: 39/45; k=5: 39/45; k=7: 41/45.
Model selected by validation: k=1 (smaller k on equal scores).
Final hold-out: 38/45 (84.4%), matrix actual rows and predicted columns:
  avoid    15 0 0
  consider  0 12 3
  good      0 4 11

These classroom percentages cannot establish real-world accuracy. No final
test results were used in selecting k, and the browser evaluation tool
intentionally reports validation only.

## Four-week learning sequence

Week 12: define output, audit dataset and establish baseline.
Week 13: build k-NN, inspect a prediction and implement an interface.
Week 14: compare k on validation, inspect errors and ablate one feature.
Week 15: freeze k, evaluate once and demonstrate reproducibility.

Four independent standard-Python notebooks are included in notebooks/.
Weeks 12–14 do not embed the final test examples, unlike Week 15.

## Student hand-off checklist

Provide executable source, a concise specification, fixed splits and
random seed, a validation comparison, one documented error, final
evaluation results, tests and a limitation statement. A GitHub repository
and meaningful commits may be used, but the school collection endpoint
must be configured separately. Downloading this ZIP does not submit it.

## Sources

Machine Learning Club Weeks 12–15 and the public source repository.
The preparation concepts are generic; no official FiiCode requirements
have been represented as established competition rules.
