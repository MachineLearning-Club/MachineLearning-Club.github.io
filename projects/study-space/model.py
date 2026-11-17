"""Study Space Challenge — simple, inspectable classification baseline.

All data are artificial, contain no student information, and are not from FiiCode.
No third-party Python packages are required.
"""
from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FEATURES = ("occupancy", "noise", "wifi", "outlets", "minutes")
LABELS = ("avoid", "consider", "good")
K_VALUES = (1, 3, 5, 7)
SCALES = (100.0, 60.0, 4.0, 1.0, 100.0)
WEIGHTS = (1.0, 1.0, 0.7, 0.30, 0.15)

def load_csv(name: str):
    with (HERE / "data" / name).open(newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))
    for row in records:
        for feature in FEATURES:
            row[feature] = int(row[feature])
    return records

def validate_row(row):
    for feature, low, high in zip(FEATURES, (0, 20, 1, 0, 15),
                                       (100, 95, 5, 1, 120)):
        if feature not in row or not isinstance(row[feature], int) or isinstance(row[feature], bool):
            raise ValueError(f"Missing or non-integer feature: {feature}")
        value = row[feature]
        if value < low or value > high:
            raise ValueError(f"Out-of-range {feature}: {value}")
    return row

def distance(a, b):
    return sum(weight * ((int(a[f])-int(b[f])) / scale)**2
               for f, scale, weight in zip(FEATURES, SCALES, WEIGHTS))

def baseline(train):
    counts = Counter(row["label"] for row in train)
    return sorted(LABELS, key=lambda label: (-counts[label], label))[0]

def nearest(train, sample, k=3):
    if k not in K_VALUES:
        raise ValueError(f"Choose k from {K_VALUES}")
    validate_row(sample)
    ranked = sorted(train, key=lambda item: (distance(item, sample), item["id"]))
    selected = ranked[:k]
    votes = Counter(item["label"] for item in selected)
    predicted = min(LABELS, key=lambda label: (
        -votes[label],
        sum(distance(item, sample) for item in selected if item["label"] == label),
        label,
    ))
    return predicted, [(item["id"], item["label"], round(distance(item, sample), 5))
                       for item in selected]

def evaluate(train, testing, k):
    matrix = {label: {p: 0 for p in LABELS} for label in LABELS}
    wrong = []
    for row in testing:
        prediction, _ = nearest(train, row, k)
        matrix[row["label"]][prediction] += 1
        if prediction != row["label"]:
            wrong.append((row["id"], row["label"], prediction))
    correct = len(testing) - len(wrong)
    return {"correct": correct, "total": len(testing),
            "accuracy": correct / len(testing), "matrix": matrix, "wrong": wrong}

def choose_k(train, validation):
    scores = {k: evaluate(train, validation, k)["correct"] for k in K_VALUES}
    best_k = min(K_VALUES, key=lambda k: (-scores[k], k))
    return best_k, scores

def report(train, validation, test):
    base = baseline(train)
    base_correct = sum(row["label"] == base for row in validation)
    chosen, scores = choose_k(train, validation)
    final = evaluate(train, test, chosen)
    return {"baseline_label": base, "baseline_validation": base_correct,
            "validation_total": len(validation), "scores": scores,
            "chosen_k": chosen, "test": final}
