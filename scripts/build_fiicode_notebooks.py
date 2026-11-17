#!/usr/bin/env python3
"""Four standalone JupyterLite notebooks for one reproducible study-space project.

Weeks 12–14 embed train+validation; Week 15 additionally embeds final-test labels.
No imports beyond Python's standard library; the published CSVs are canonical.
"""
import base64
import json
import shutil
import zlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
dataset = json.loads((ROOT/'assets/data/fiicode-study-space.json').read_text())
data = dataset["data"]
base = '''import base64, zlib, json
payload=json.loads(zlib.decompress(base64.b85decode(PACK)).decode())
training=payload["train"]
validation=payload["validation"]
testing=payload.get("test", [])
print("Train",len(training),"Validation",len(validation),"Final test",len(testing))
'''
model = '''from collections import Counter
FEATURES=("occupancy","noise","wifi","outlets","minutes")
LABELS=("avoid","consider","good")
SCALES=(100,60,4,1,100)
WEIGHTS=(1,1,.7,.30,.15)
def distance(a,b,weights=WEIGHTS):
    return sum(w*((a[f]-b[f])/scale)**2
               for f,scale,w in zip(FEATURES,SCALES,weights))
def predict(sample,k=3,train=training,weights=WEIGHTS):
    if k not in (1,3,5,7): raise ValueError("Choose k=1,3,5,7")
    chosen=sorted(train,key=lambda row:(distance(row,sample,weights),row["id"]))[:k]
    votes=Counter(row["label"] for row in chosen)
    answer=min(LABELS,key=lambda label:(
      -votes[label],
      sum(distance(row,sample,weights) for row in chosen if row["label"]==label),
      label))
    return answer,chosen
def evaluate(rows,k=3,train=training,weights=WEIGHTS):
    confusion={label:{other:0 for other in LABELS} for label in LABELS}
    errors=[]
    for row in rows:
        guessed,_=predict(row,k,train,weights)
        confusion[row["label"]][guessed]+=1
        if guessed!=row["label"]: errors.append((row["id"],row["label"],guessed))
    return len(rows)-len(errors),confusion,errors
'''
sections = {
12: [
("Data dictionary and splits",
 """Features: occupancy (%) in 0–100; noise (illustrative dB); Wi-Fi strength 1–5; outlets 0/1; intended study duration (minutes). The label is avoid, consider or good. These labels were produced for an artificial practice dataset; they are not actual human preferences.

**Tasks:** count examples, check that IDs are unique, check class frequencies and write one reason this cannot establish real-world performance.""",
'''print("Example:",training[0])
print("Columns:",list(training[0]))
assert len(training)==150 and len(validation)==45
ids=[row["id"] for row in training+validation]
assert len(ids)==len(set(ids)), "Repeated IDs between train and validation"
for label in LABELS:
    print(label,"train",sum(r["label"]==label for r in training),
          "validation",sum(r["label"]==label for r in validation))
'''),
("Build the most-frequent-label baseline",
 """A baseline is a real predictive rule, even if it is simple. Keep validation separate: use the **training** labels to choose a fixed label, then use validation labels only to score it.

**Tasks:** explain why 15/45 correct is not impressive, and why a class-balanced practice split should not be treated as a natural population distribution.""",
'''counts=Counter(r["label"] for r in training)
baseline=min(LABELS,key=lambda label:(-counts[label],label))
correct=sum(r["label"]==baseline for r in validation)
print("Baseline predicts",baseline,"for every example")
print(f"Validation: {correct}/{len(validation)} = {correct/len(validation):.1%}")
assert correct==15
'''),
("Change one data assumption",
 """Choose one feature and describe whether it is a measurement, a subjective judgement or an artificial label. Write a clear problem statement with the exact expected output classes.""",
'''for f in FEATURES:
    values=[row[f] for row in training]
    print(f,"range",min(values),max(values))
print("Next: implement a classifier rather than predicting one label every time.")
'''),
],
13:[
("From five measurements to distance",
 """Each feature has different units, so we scale the differences before computing distance. The weights are a **design choice**; they were not learned from the validation/test labels. Predict whether an example is closer to training space A or B before running.""",
'''sample={"occupancy":35,"noise":42,"wifi":4,"outlets":1,"minutes":60}
print("First training comparison:",round(distance(sample,training[0]),5))
guess,chosen=predict(sample,k=3)
print("Prediction:",guess)
for row in chosen: print(row["id"],row["label"],round(distance(sample,row),5))
'''),
("Build a usable prediction function",
 """The method returns a class and the actual neighbours responsible for the vote. It can be connected to an interface, but it is not a probability estimate.

**Tasks:** try two different room profiles; predict the effect of changing k before running.""",
'''profiles=[
 {"occupancy":15,"noise":35,"wifi":5,"outlets":1,"minutes":60},
 {"occupancy":95,"noise":83,"wifi":1,"outlets":0,"minutes":60},
]
for item in profiles:
    for k in (1,3,5):
        print(item["occupancy"],item["noise"],"k",k,"->",predict(item,k)[0])
'''),
("Check input contracts",
 """An interface must reject invalid fields rather than silently treating them as observations. Define exact allowed ranges and try bad values.""",
'''def check_input(sample):
    ranges={"occupancy":(0,100),"noise":(20,95),"wifi":(1,5),
            "outlets":(0,1),"minutes":(15,120)}
    for key,(lo,hi) in ranges.items():
        if key not in sample or not isinstance(sample[key],int) or isinstance(sample[key],bool):
            raise ValueError("Missing or non-integer "+key)
        if not lo<=sample[key]<=hi: raise ValueError("Invalid "+key)
    return sample
assert check_input(profiles[0])
try:
    check_input({**profiles[0],"wifi":8})
except ValueError as error:
    print("Expected rejection:",error)
else:
    raise AssertionError("Invalid Wi-Fi signal was accepted")
'''),
],
14:[
("Compare k on the same validation examples",
 """Only validation data are used to choose k. To make a comparison fair, do not change the split or the scoring rule partway through.""",
'''scores={}
for k in (1,3,5,7):
    correct,matrix,errors=evaluate(validation,k)
    scores[k]=correct
    print(f"k={k}: {correct}/{len(validation)} ({correct/len(validation):.1%})")
best_k=min(scores,key=lambda k:(-scores[k],k))
print("Selected by validation only:",best_k)
assert scores=={1:41,3:39,5:39,7:41} and best_k==1
'''),
("Inspect a confusion matrix",
 """Rows are actual labels, columns are predictions. Diagonal entries are correct. A high overall score can hide different behaviour for the three classes.""",
'''correct,matrix,errors=evaluate(validation,best_k)
print("Actual / Predicted | avoid consider good")
for label in LABELS:
    print(f"{label:>9}       |",*[matrix[label][p] for p in LABELS])
for label in LABELS:
    total=sum(matrix[label].values())
    print("Recall",label,":",f"{matrix[label][label]}/{total}")
print("Some mistakes:",errors[:4])
assert sum(sum(x.values()) for x in matrix.values())==45
'''),
("Controlled ablation: remove Wi-Fi weight",
 """An ablation disables one factor to investigate whether it contributes useful information. This is an *investigation on validation*, not a final evaluation. Do not choose weights based on the final test examples.""",
'''without_wifi=(1,1,0,.30,.15)
original=evaluate(validation,best_k)[0]
ablated=evaluate(validation,best_k,weights=without_wifi)[0]
print("Validation original:",original,"without Wi-Fi:",ablated)
print("Difference:",ablated-original)
'''),
],
15:[
("Freeze the model before final evaluation",
 """Do not choose k on the final test. This notebook first repeats the Week 14 validation choice, then performs the final evaluation **once** with the selected setting.""",
'''scores={k:evaluate(validation,k)[0] for k in (1,3,5,7)}
best_k=min(scores,key=lambda k:(-scores[k],k))
print("Frozen k",best_k,"validation",scores)
assert best_k==1
'''),
("Final evaluation on unseen-to-training rows",
 """This test set has 45 different synthetic rows (15 of each label). All labels are public in the downloadable course bundle, so this is an **educational hold-out**, not a tamper-proof competition leaderboard.

**Tasks:** record the numerator, denominator, confusion matrix, and limitation. Do not claim the percentage applies to actual students or classrooms.""",
'''correct,matrix,errors=evaluate(testing,best_k)
print(f"Final: {correct}/{len(testing)} = {correct/len(testing):.1%}")
for label in LABELS:
    print(label,[matrix[label][p] for p in LABELS])
print("Example failure:",errors[0] if errors else "none")
assert correct==38 and len(testing)==45
'''),
("Reproducibility and hand-off checks",
 """A team hand-off must include source code, fixed data splits, random seed, settings, a README and evidence. A test should fail loudly when predictions or dataset invariants change.

**Tasks:** create a short README describing the app's purpose and limits; include screenshot evidence from the browser app; add one user-facing improvement and its test.""",
'''assert len(training)==150 and len(validation)==45 and len(testing)==45
assert len({r["id"] for r in training+validation+testing})==240
assert predict({"occupancy":35,"noise":40,"wifi":4,"outlets":1,"minutes":60},best_k)[0]=="good"
print("Smoke tests passed; prepare a project ZIP plus a short evidence report.")
'''),
],
}
def cell(kind,text):
    c={"cell_type":kind,"metadata":{},"source":[line+"\n" for line in text.strip().split("\n")]}
    if kind=="code": c.update(execution_count=None,outputs=[])
    return c
def build(week):
    subset={k:data[k] for k in (("train","validation","test") if week==15 else ("train","validation"))}
    packed=base64.b85encode(zlib.compress(json.dumps(subset,separators=(",",":")).encode(),9)).decode()
    pack_cell="PACK="+repr(packed)+"\n"+base
    cells=[
      cell("markdown",f"# Week {week} — Study Space Challenge\n\n**Independent classroom practice; not an official FIICode problem.**\n\nDataset: 240 distinct synthetic examples generated with seed 20261117. Classes: avoid / consider / good; this is a deliberately balanced sample, not a real-world survey. The classifier and five feature units are documented in the project source. This notebook embeds the exact dataset split and requires only standard Python.\n\nRun each cell in order, change inputs, and write your conclusions in Markdown cells."),
      cell("code",pack_cell),
      cell("markdown","## The same k-NN algorithm in every lesson\n\nThe weighted squared distance is the sum of five scaled feature differences. Neighbours vote; ties are settled by summed distance and alphabetical label order. The default weights and all records remain unchanged across weeks."),
      cell("code",model)
    ]
    for title,description,code in sections[week]:
        compile(code,f"W{week} {title}","exec")
        cells.extend([cell("markdown","## "+title+"\n\n"+description),cell("code",code)])
    cells.append(cell("markdown","## Evidence to save\n\nRecord what you changed, the original and new outputs, and the denominator of any score. Explain at least one weakness. Export the completed .ipynb; your teacher will specify how to hand it in."))
    nb={"cells":cells,"metadata":{"kernelspec":{"display_name":"Python (Pyodide)","language":"python","name":"python"},"language_info":{"name":"python"}},"nbformat":4,"nbformat_minor":5}
    name=f"study-space-week{week}.ipynb"
    path=ROOT/f"w{week}/lab/notebooks/{name}"
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(nb,indent=2,ensure_ascii=False)+"\n")
    dest=ROOT/"jupyter/files"/name
    dest.parent.mkdir(exist_ok=True,parents=True)
    shutil.copy2(path,dest)
    print("Notebook:",name, "cells",len(cells))
for week in (12,13,14,15): build(week)
