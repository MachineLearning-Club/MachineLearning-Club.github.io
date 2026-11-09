#!/usr/bin/env python3
import json, ast
from pathlib import Path
R=Path(__file__).resolve().parent
def cell(kind,text):
    d={"cell_type":kind,"metadata":{},"source":text.strip("\n").splitlines(keepends=True)}
    if kind=="code":ast.parse(text);d.update(execution_count=None,outputs=[])
    return d
def save(n,pairs):
    nb={"cells":[cell(k,v) for k,v in pairs],"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
    p=R/f"w{n}/lab/starter.ipynb"
    p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(json.dumps(nb,indent=1,ensure_ascii=False)+"\n",encoding="utf-8")
save(1,[
("markdown",r"""
# Week 1 — Your first learning system
Machine Learning Club · Laboratory

This is a deliberately tiny model. It is not Google's neural network. Start by exploring [Quick, Draw!](https://quickdraw.withgoogle.com/) and [Teachable Machine](https://teachablemachine.withgoogle.com/).
"""),
("markdown",r"""
## 1. A synthetic training dataset
Two sensors measure size and reflectance in arbitrary units. The class names A and B are supplied by the teacher. These measurements do not reliably identify real materials.
"""),
("code",r"""
training = [
    {"size": 2.0, "reflectance": 2.0, "label": "A"},
    {"size": 2.0, "reflectance": 3.0, "label": "A"},
    {"size": 3.0, "reflectance": 2.0, "label": "A"},
    {"size": 7.0, "reflectance": 7.0, "label": "B"},
    {"size": 7.0, "reflectance": 8.0, "label": "B"},
    {"size": 8.0, "reflectance": 7.0, "label": "B"},
]
print("Training examples:", len(training))
print("Classes:", sorted({row["label"] for row in training}))
for row in training: print(row)
"""),
("markdown",r"""
## 2. Training
A class prototype is the average feature pair for that class. Learning here means calculating these averages, rather than writing an explicit prediction rule for each input.
"""),
("code",r"""
classes = sorted({row["label"] for row in training})
prototypes = {}
for label in classes:
    rows = [row for row in training if row["label"] == label]
    size = sum(row["size"] for row in rows) / len(rows)
    reflectance = sum(row["reflectance"] for row in rows) / len(rows)
    prototypes[label] = (size, reflectance)
print("Learned prototypes:", prototypes)
"""),
("markdown",r"""
## 3. Predicting unseen observations
Compare a new sample to the prototypes by straight-line distance. The closest prototype wins. This is a nearest-prototype toy classifier, not the same algorithm as Teachable Machine.
"""),
("code",r"""
from math import dist
def predict(size, reflectance):
    sample = (size, reflectance)
    distances = {label: dist(sample, point) for label,point in prototypes.items()}
    label = min(distances, key=distances.get)
    return label, distances
for example in [(2.5,2.2),(7.5,7.5),(5.0,5.0)]:
    label, distances = predict(*example)
    print(example, "=>", label, {k:round(v,2) for k,v in distances.items()})
"""),
("markdown",r"""
## 4. Investigate and modify
Predict the result for (3,3) before running the next cell. Then change two examples, rerun the training cell and measure whether the result changes. Test an input far outside the training range (100,100); the model will predict even when it has no trustworthy evidence.

For Homework, reuse this notebook with a new supplied training dataset and explain the errors.
"""),
("code",r"""
print("Within the training range:", predict(3,3)[0])
print("Far outside the training range:", predict(100,100)[0])
""")])
save(3,[
("markdown",r"""
# Week 3 — ID3 decision trees
Machine Learning Club · Laboratory

This notebook implements categorical ID3. The linked interactive webapp visualises CART; it is related but not the same algorithm.

Goal: calculate entropy, select a root, build a tree and inspect an unseen case.
"""),
("markdown",r"""
## 1. Data
Three categorical features (sky, wind, temperature), one label (go). Every possible combination occurs once. Labels are deliberately synthetic.
"""),
("code",r"""
from collections import Counter
from math import log2
examples = [
    {"sky":"sunny","wind":"calm","temperature":"warm","go":"yes"},
    {"sky":"sunny","wind":"calm","temperature":"cold","go":"yes"},
    {"sky":"sunny","wind":"windy","temperature":"warm","go":"yes"},
    {"sky":"sunny","wind":"windy","temperature":"cold","go":"no"},
    {"sky":"rainy","wind":"calm","temperature":"warm","go":"no"},
    {"sky":"rainy","wind":"calm","temperature":"cold","go":"no"},
    {"sky":"rainy","wind":"windy","temperature":"warm","go":"no"},
    {"sky":"rainy","wind":"windy","temperature":"cold","go":"no"},
]
features = ["sky","wind","temperature"]
for i,row in enumerate(examples,1):print(i,row)
"""),
("markdown",r"""
## 2. Entropy and information gain
Shannon entropy is H(Y) = -sum(p_i * log2(p_i)). The definition extends continuously to probability zero. Information gain subtracts the weighted entropy after the split.
"""),
("code",r"""
def entropy(rows):
    if not rows:return 0.0
    counts = Counter(r["go"] for r in rows)
    total = len(rows)
    return -sum((v/total)*log2(v/total) for v in counts.values())

def gain(rows, feature):
    parent=entropy(rows)
    remainder=0.0
    for value in sorted({r[feature] for r in rows}):
        subset=[r for r in rows if r[feature]==value]
        remainder+=len(subset)/len(rows)*entropy(subset)
    return parent-remainder

print("Parent entropy",round(entropy(examples),4))
for f in features:print(f,"gain",round(gain(examples,f),4))
"""),
("markdown",r"""
## 3. Construct categorical ID3
At each impure node choose the remaining attribute with the largest information gain, and recurse on every observed category. If there are no remaining attributes, use the majority class. Ties use the original feature order.
"""),
("code",r"""
def majority(rows):
    return Counter(r["go"] for r in rows).most_common(1)[0][0]

def id3(rows, available):
    labels={r["go"] for r in rows}
    if len(labels)==1:return {"label":rows[0]["go"]}
    if not available:return {"label":majority(rows)}
    feature=max(available,key=lambda f:gain(rows,f))
    options={}
    for value in sorted({r[feature] for r in rows}):
        subset=[r for r in rows if r[feature]==value]
        options[value]=id3(subset,[f for f in available if f!=feature])
    return {"test":feature,"default":majority(rows),"branches":options}

def classify(tree,sample):
    while "label" not in tree:
        value=sample.get(tree["test"])
        tree=tree["branches"].get(value,{"label":tree["default"]})
    return tree["label"]

tree=id3(examples,features)
print("Tree",tree)
print("Training correct",sum(classify(tree,r)==r["go"] for r in examples),"/",len(examples))
"""),
("markdown",r"""
## 4. Experiment
Predict the three information gains before running. Why does the rainy branch terminate? Remove the sunny/windy/cold/no record, fit again, and predict the missing case. Does fitting all remaining examples guarantee a correct new prediction?
"""),
("code",r"""
heldout={"sky":"sunny","wind":"windy","temperature":"cold"}
reduced=[r for r in examples if any(r[f]!=heldout[f] for f in features)]
new_tree=id3(reduced,features)
print("Held-out prediction",classify(new_tree,heldout))
print("Original answer","no")
""")])
print("Created two executable notebook sources.")
