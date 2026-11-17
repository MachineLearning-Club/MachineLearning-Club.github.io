#!/usr/bin/env python3
"""Reproducible training, validation and final test of a small classroom classifier."""
import argparse
from model import load_csv, report, nearest, FEATURES, LABELS

def main():
    parser = argparse.ArgumentParser(description="Synthetic Study Space Challenge")
    parser.add_argument("--predict", nargs=5, type=int,
                        metavar=("OCCUPANCY","NOISE","WIFI","OUTLETS","MINUTES"))
    args = parser.parse_args()
    train = load_csv("train.csv")
    validation = load_csv("validation.csv")
    test = load_csv("test.csv")
    result = report(train, validation, test)
    print("STUDY SPACE CHALLENGE — synthetic classroom examples, not official competition data")
    print(f"Training: {len(train)}, validation: {len(validation)}, untouched test: {len(test)}")
    print(f"Majority-class baseline ({result['baseline_label']}): "
          f"{result['baseline_validation']}/{len(validation)} validation correct")
    for k, correct in result["scores"].items():
        print(f"k={k}: {correct}/{len(validation)} validation correct")
    print(f"Chosen k={result['chosen_k']} from validation only")
    test_result = result["test"]
    print(f"Final hold-out score: {test_result['correct']}/{test_result['total']} "
          f"({test_result['accuracy']:.1%}); NOT a real-world accuracy estimate")
    print("Confusion matrix (rows actual, columns predicted):")
    print("         " + " ".join(f"{l:>8}" for l in LABELS))
    for actual in LABELS:
        print(f"{actual:>8} " + " ".join(f"{test_result['matrix'][actual][p]:>8}" for p in LABELS))
    print("Example errors:", test_result["wrong"][:5])
    if args.predict:
        sample = dict(zip(FEATURES, args.predict))
        answer, neighbours = nearest(train, sample, result["chosen_k"])
        print("Custom prediction:", answer, "| neighbours (ID, class, d²):", neighbours)

if __name__ == "__main__":
    main()
