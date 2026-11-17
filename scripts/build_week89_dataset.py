#!/usr/bin/env python3
"""Build a reproducible, stratified classroom subset of the UCI Optical Recognition digits.
Canonical input is the 1,797-example scikit-learn digits.csv.gz distribution.
We create a NEW internal train/test split; this is not the original UCI partition.
Pure Python, no NumPy/scikit-learn runtime dependency.
"""
import csv
import gzip
import json
import random
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/week89/digits-original.csv.gz"
OUT=ROOT/"assets/data"
OUT.mkdir(exist_ok=True,parents=True)
with gzip.open(SOURCE, "rt", newline="") as f:
    original=[[int(item) for item in row] for row in csv.reader(f)]
assert len(original)==1797 and all(len(row)==65 for row in original)
assert all(0<=v<=16 for row in original for v in row[:64])
by_digit={d:[] for d in range(10)}
for i,row in enumerate(original):
    by_digit[row[-1]].append(i)
rng=random.Random(20261116)
train_idx=[]
test_idx=[]
for d,indices in by_digit.items():
    rng.shuffle(indices)
    train_idx+=indices[:60]
    test_idx+=indices[60:80]
rng.shuffle(train_idx)
rng.shuffle(test_idx)
assert len(set(train_idx+test_idx))==800
train=[{"id":i,"y":original[i][-1],"x":original[i][:64]} for i in train_idx]
test=[{"id":i,"y":original[i][-1],"x":original[i][:64]} for i in test_idx]
dataset={
 "source":"Alpaydin & Kaynak (1998), UCI Optical Recognition of Handwritten Digits, via scikit-learn digits.csv.gz",
 "doi":"10.24432/C50P49",
 "license":"CC BY 4.0",
 "source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 "split":"Deterministic stratified classroom subsample (seed 20261116): 60 train and 20 held-out examples of each of 10 digits, selected from scikit-learn's 1797 rows. Not the original UCI train/test split.",
 "rows_total":1797,"train":train,"test":test
}
(OUT/"week89-digits.json").write_text(json.dumps(dataset,separators=(",",":"),ensure_ascii=False)+"\n")
with (OUT/"week89-digits.csv").open("w",newline="") as f:
    writer=csv.writer(f,lineterminator="\n")
    writer.writerow(["id","split","digit"]+[f"pixel_{r}_{c}" for r in range(8) for c in range(8)])
    for split,records in [("train",train),("test",test)]:
        for item in records:writer.writerow([item["id"],split,item["y"],*item["x"]])
def distance(a,b, threshold=0):
    return sum((x-y)**2 for x,y in zip(a,b)) if threshold==0 else sum(((16 if x>=threshold else 0)-(16 if y>=threshold else 0))**2 for x,y in zip(a,b))
def predict(example,k,threshold=0):
    near=sorted(((distance(example["x"],row["x"],threshold),row["y"],row["id"]) for row in train),key=lambda v:(v[0],v[2]))[:k]
    totals={}
    for dist,digit,_ in near:
        if digit not in totals:totals[digit]=[0,0,0]
        totals[digit][0]+=1;totals[digit][1]+=dist
    # majority, then smallest total distance, then smallest digit for deterministic ties
    return min(totals,key=lambda digit:(-totals[digit][0],totals[digit][1],digit))
def evaluate(k,threshold=0):
    predictions=[predict(x,k,threshold) for x in test]
    confusion=[[0]*10 for _ in range(10)]
    for record,y in zip(test,predictions):confusion[record["y"]][y]+=1
    return sum(y==rec["y"] for y,rec in zip(predictions,test)), confusion
for k in (1,3,5):
    correct,mat=evaluate(k)
    print(f"k={k}: {correct}/200 correct ({correct/2:.1f}%). Matrix diagonal={sum(mat[i][i] for i in range(10))}")
print("Source SHA",dataset["source_sha256"],"JSON bytes",(OUT/"week89-digits.json").stat().st_size)
