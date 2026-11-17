#!/usr/bin/env python3
"""Package a no-dependencies offline practice app and publish a linked overview."""
import json
import re
import shutil
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"projects/study-space"
data=json.loads((ROOT/"assets/data/fiicode-study-space.json").read_text())
README="""# Study Space Challenge — independent classroom practice

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
"""
(HERE/"README.md").write_text(README,encoding="utf-8")
shutil.copyfile(ROOT/"assets/fiicode-practice.js",HERE/"app.js")
shutil.copyfile(ROOT/"assets/fiicode-practice.css",HERE/"app.css")
offline=(r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Study Space Challenge — Offline demo</title>
<link rel="stylesheet" href="app.css">
<style>body{font-family:system-ui,-apple-system,sans-serif;color:#1d303e;max-width:980px;padding:24px;margin:auto;line-height:1.55}
h1{font-weight:660;letter-spacing:-.03em}a{color:#245e83}a:focus-visible{outline:3px solid #86b7dc}
header{border-bottom:1px solid #ddd;margin-bottom:22px}
</style><script defer src="app.js"></script></head><body>
<header><h1>Study Space Challenge</h1><p>Offline classroom practice • Fully synthetic data</p></header>
<main><p>The 240 labelled examples do not represent actual room conditions or official FiiCode judging.
The prediction comes from the 150 synthetic training records; validation uses 45 additional records.</p>
<div data-fiicode-widget></div>
<h2>Getting started</h2>
<p>Change inputs and k, inspect the nearest neighbours, and count validation mistakes.
For the final test and confusion matrix run <code>python evaluate.py</code> in this folder.
See README.md for assumptions and limitations.</p></main>
<script type="application/json" id="study-space-data">'''+
 json.dumps(data,ensure_ascii=True,separators=(",",":"))+
 r'''</script></body></html>''')
(HERE/"app.html").write_text(offline,encoding="utf-8")
old=(ROOT/"w12/course/index.html").read_text(encoding="utf-8")
body=r'''<main class="lesson-content week89-academic ss-academic">
<p class="eyebrow">Machine Learning Club · One connected practice project</p>
<h1>Study Space Challenge</h1>
<p>One problem develops through Weeks 12–15: dataset inspection, a baseline,
a working application, measured improvement and a reproducible hand-off.</p>
<p><strong>Independent practice, not official FiiCode material.</strong> All 240
examples are synthetic and do not measure the suitability of actual rooms.</p>
<table class="teaching-data"><tr><th>Stage</th><th>Evidence produced</th><th>Lesson</th></tr>
<tr><td>12 · Define</td><td>Data, splits, baseline 15/45</td><td><a href="/w12/course/">Week 12</a></td></tr>
<tr><td>13 · Build</td><td>Real k-NN, interface and input checks</td><td><a href="/w13/course/">Week 13</a></td></tr>
<tr><td>14 · Improve</td><td>Validation 41/45, confusion matrix and ablation</td><td><a href="/w14/course/">Week 14</a></td></tr>
<tr><td>15 · Hand off</td><td>Frozen k=1, final 38/45 and runnable tests</td><td><a href="/w15/course/">Week 15</a></td></tr></table>
<div class="ss-resource-links">
<a href="/projects/study-space/study-space-starter.zip" download>Download complete offline project ZIP</a>
<a href="/projects/study-space/data/train.csv" download>Training CSV</a>
<a href="/projects/study-space/data/validation.csv" download>Validation CSV</a>
<a href="/w15/quiz/">20-point review rubric</a></div>
<h2>Try a real classifier</h2><div data-fiicode-widget></div>
<h2>Repeat the experiment with Python</h2>
<pre><code>python evaluate.py
python -m unittest test_project.py -v
python evaluate.py --predict 35 40 4 1 60</code></pre>
<p>The ZIP includes an offline app.html and four standalone notebooks.
All scores concern fixed synthetic examples, not real students.</p>
<p><a href="/projects/">Back to projects</a> · <a href="/guides/github-ai/">GitHub guide</a>
· <a href="/guides/notebooks/">Notebook guide</a></p></main>'''
new,num=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:body,old,count=1,flags=re.S)
assert num==1
new=new.replace('<title>','<title>Study Space Challenge — ',1)
(HERE/"index.html").write_text(new,encoding="utf-8")
with zipfile.ZipFile(HERE/"study-space-starter.zip","w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
    for name in ("README.md","model.py","evaluate.py","test_project.py","app.html","app.js","app.css"):
        zf.write(HERE/name,arcname="study-space/"+name)
    for f in sorted((HERE/"data").glob("*.csv")):
        zf.write(f,arcname="study-space/data/"+f.name)
    for week in (12,13,14,15):
        f=ROOT/f"w{week}/lab/notebooks/study-space-week{week}.ipynb"
        zf.write(f,arcname="study-space/notebooks/"+f.name)
print("Packaged offline app, source, data, four notebooks; ZIP size", (HERE/"study-space-starter.zip").stat().st_size)
