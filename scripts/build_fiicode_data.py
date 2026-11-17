#!/usr/bin/env python3
"""Rebuild a deterministic, explicitly synthetic three-class study-space dataset.

Educational simulation, not student records and not an official FIICode dataset.
Changing the generator changes the benchmark: do not quietly overwrite scores.
"""
from pathlib import Path
import csv
import json
import random
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "projects/study-space/data"
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20261117
rng = random.Random(SEED)
FEATURES = ("occupancy", "noise", "wifi", "outlets", "minutes")
LABELS = ("avoid", "consider", "good")
SIZES = {"train": 50, "validation": 15, "test": 15}
PROFILES = {
    "avoid": ((62,100),(60,87),(1,3),0.25),
    "consider": ((34,82),(43,69),(2,4),0.55),
    "good": ((7,59),(29,54),(3,5),0.80),
}
records = {split: [] for split in SIZES}
seen = set()
next_id = 1
for label in LABELS:
    occ, noise, wifi, outlet_prob = PROFILES[label]
    generated = []
    while len(generated) < sum(SIZES.values()):
        item = {
            "occupancy": rng.randint(*occ),
            "noise": rng.randint(*noise),
            "wifi": rng.randint(*wifi),
            "outlets": int(rng.random() < outlet_prob),
            "minutes": rng.choice((30,45,60,90,120)),
        }
        signature = tuple(item[key] for key in FEATURES)
        if signature in seen:
            continue
        seen.add(signature)
        item["id"] = f"SS{next_id:03d}"
        item["label"] = label
        next_id += 1
        generated.append(item)
    rng.shuffle(generated)
    cursor = 0
    for split, size in SIZES.items():
        records[split].extend(generated[cursor:cursor+size])
        cursor += size

for split, rows in records.items():
    rng.shuffle(rows)
    path = OUT / f"{split}.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("id", *FEATURES, "label"))
        writer.writeheader()
        writer.writerows(rows)
    assert Counter(r["label"] for r in rows) == {
        label: SIZES[split] for label in LABELS
    }
    print(split, len(rows), dict(Counter(r["label"] for r in rows)))
assert len(seen) == 240
payload = {
    "name": "Study Space Challenge (synthetic classroom practice)",
    "notice": "Artificial labelled examples; no real student or classroom measurements; not a FIICode task or dataset.",
    "seed": SEED,
    "features": [
        {"name": "occupancy", "unit": "%", "range": [0,100]},
        {"name": "noise", "unit": "illustrative dB", "range": [20,95]},
        {"name": "wifi", "unit": "signal levels", "range": [1,5]},
        {"name": "outlets", "unit": "available (0/1)", "range": [0,1]},
        {"name": "minutes", "unit": "study duration", "range": [15,120]},
    ],
    "labels": list(LABELS),
    "data": records,
}
(ROOT / "assets/data/fiicode-study-space.json").write_text(
    json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Dataset ready: 240 unique examples; 150 train / 45 validation / 45 test")
