#!/usr/bin/env python3
from pathlib import Path
from html import escape as E
from html.parser import HTMLParser
import re

# week | date | title | description | course objectives | lab objectives | homework objectives | advanced objectives
# Separate objectives with semicolons. Each page gets its own measurable objectives.
DATA = """
1|2 Dec 2026|What Is AI? Rules and Learning|Rules versus learned patterns, training examples, classification and confidence.|Distinguish programmed rules from machine learning;Explain features labels and training examples;Interpret classifier confidence cautiously|Identify the method behind everyday software;Train a two-class image classifier;Test predictions on unseen examples|Classify software examples using evidence;Describe one model misclassification|Investigate changing backgrounds and lighting;Compare confidence with measured accuracy
2|9 Dec 2026|Mathematics for Machine Learning|Statistics, probability and information theory on small labelled datasets.|Calculate means medians and frequencies;Use basic and conditional probabilities;Explain entropy as label uncertainty|Summarise a labelled dataset;Calculate two class probabilities;Compare entropy across distributions|Show statistical calculations;Explain a biased-sample example|Implement binary entropy in Python;Explore information gained by a feature
3|16 Dec 2026|Decision Trees: ID3|Decision-making by splitting categorical data using information gain.|Identify nodes branches and leaves;Calculate entropy and information gain;Choose and justify an ID3 root split|Compute candidate split scores;Draw a two-level decision tree;Trace new samples through the tree|Show a complete root-gain calculation;Predict labels from a hand-built tree|Explore depth versus overfitting;Compare information gain with another criterion
4|13 Jan 2027|Numeric Splits and Evaluation|Continuous features, unseen data, accuracy and confusion matrices.|Choose numeric thresholds;Separate train validation and test samples;Calculate accuracy and interpret confusion matrices|Try threshold candidates;Evaluate a held-out sample;Explain false positives and negatives|Construct a confusion matrix;Explain why training score is not enough|Calculate precision and recall;Investigate tree pruning and leakage
5|20 Jan 2027|K-Nearest Neighbours|Measure similarity and classify by voting among neighbours.|Compute Euclidean distance in 2D;Apply majority vote for a chosen K;Explain scaling and K selection|Locate nearest neighbours;Compare K=1 and K=3 predictions;Run a scikit-learn KNN notebook|Calculate distances and votes;Discuss misleading feature scales|Compare weighted voting;Tune K with cross-validation
6|27 Jan 2027|K-Means Clustering|Find unlabelled groups through repeated centroid updates.|Distinguish classification from clustering;Assign points to nearest centres;Calculate centroid updates|Perform two manual K-Means iterations;Plot clusters and centres;Compare starting centres|Show assignments and centroid arithmetic;Identify a case where K-Means fails|Compare inertia across K;Test multiple random initialisations
7|3 Feb 2027|Linear Regression|Fit a straight line to predict numbers and measure errors.|Interpret slope and intercept;Compute predictions and residuals;Explain squared error and extrapolation|Plot measurements;Fit a line in Python;Calculate residuals and MSE|Solve line and residual questions;Explain correlation versus causation|Simulate gradient descent;Compare simple and overfit models
8|10 Feb 2027|Computer Vision|Pixels as arrays, spatial filtering and image features.|Read grayscale pixel matrices;Calculate a 3×3 filter output;Distinguish filtering from classification|Inspect image pixel values;Apply an edge filter;Compare before-and-after images|Calculate filter outputs on paper;Explain lighting-related failures|Investigate padding effects;Compare blur and edge kernels
9|17 Feb 2027|Perceptrons and Neural Networks|Weighted sums, bias, activation and layered networks.|Compute a weighted sum and bias;Apply a step activation;Describe input hidden and output layers|Calculate neuron outputs;Adjust weights to change decisions;Inspect an interactive network|Solve weighted-sum exercises;Draw a labelled network|Explore a gradient weight update;Explain the XOR limitation of one perceptron
10|3 Mar 2027|Integrated AI Systems I|Combine vision, prediction, decision rules and user feedback.|Draw stages of an AI pipeline;Explain propagated model errors;Select a human-review fallback|Assemble image-to-action components;Log intermediate predictions;Test novel inputs|Diagram interfaces and dependencies;Specify edge-case tests|Tune review thresholds;Compare component and whole-system accuracy
11|10 Mar 2027|Integrated AI Systems II|Forecasting, clustering and communicating model quality.|Separate data cleaning from modelling;Choose a forecast evaluation metric;Explain chronological validation|Clean a small time-series dataset;Compare naive and regression baselines;Create a prediction dashboard|Document a baseline and metric;Explain a forecast limitation|Use lagged features safely;Test rolling validation splits
12|17 Mar 2027|Language Models and Trust|LLMs, hallucinations, verification, model cards and project scoping.|Explain next-token prediction;Distinguish fluency from reliable evidence;Outline the AI project cycle|Compare two prompts;Fact-check generated claims;Define a project goal and metric|Keep a verification log;Write a concise project brief|Design a reliability rubric;Write a lightweight model card
13|24 Mar 2027|FIICode: Baselines and Metrics|Turn a competition task into reproducible measurable experiments.|Identify the target and evaluation metric;Explain baseline models;Avoid leakage in validation|Inspect a dataset;Train a first baseline;Record a reproducible score|Document an experiment setup;Identify leakage risks|Compare multiple baselines;Assess stability across validation splits
14|31 Mar 2027|FIICode: Error Analysis and Tuning|Prioritise experiments based on observed weaknesses.|Group important model errors;Distinguish features from hyperparameters;Compare experiments fairly|Inspect difficult cases;Change one model variable;Create a score comparison table|Report two controlled experiments;Explain test-set overuse|Perform feature ablations;Analyse runtime and robustness
15|7 Apr 2027|FIICode: Mock Hackathon|Demonstrate a complete solution and defend its limitations.|Explain the full pipeline;Present baseline score and limitations;Prioritise evidence-based improvements|Run a reproducible demonstration;Test normal and unusual cases;Collect peer feedback|Complete a README and results summary;Reflect on model decisions|Stress-test noisy inputs;Reproduce results in a clean environment
""".strip()
TASKS = """
1|Use the existing interactive matching exercise to distinguish fixed rules from learned methods;Train a Teachable Machine image classifier with two everyday objects;Test five previously unseen images and log predictions|Classify three digital tools with a short justification;Write a five-row prediction log with one failure analysis|Change lighting or background and compare outputs;Train with imbalanced class examples to investigate shortcuts
2|Compute frequency counts and means by hand;Plot the same data with Python;Change one label and remeasure uncertainty|Show mean median and probability calculations for a tiny dataset;Explain how a biased sample affects a probability estimate|Plot binary entropy from p=0 to p=1;Investigate a feature with many unique values
3|Count labels and calculate candidate information gains;Draw the best root split and a second level;Fit a comparison tree in scikit-learn and explain differences|Work through all root information-gain calculations;Trace four unseen examples through your diagram|Compare trees with different maximum depths;Investigate a split that perfectly memorises an ID
4|Try midpoints between sorted numeric values;Evaluate predictions on a holdout;Analyse a false-positive and false-negative example|Complete a ten-row confusion matrix;Explain two forms of data leakage|Compare precision and recall on imbalanced data;Evaluate a pruned and unpruned tree
5|Plot labelled points and calculate three nearest distances;Predict classes with K=1 and K=3;Compare unscaled and standardised features in Python|Complete a distance and vote table;Explain why units of measurement matter|Test weighted neighbours;Choose K using training-fold validation
6|Assign six coordinates to two given centroids;Recalculate means for two iterations;Plot centre movement using Python|Show assignments and updated centroids;Explain why elongated clusters are difficult|Plot inertia against different K values;Compare random seeds for consistency
7|Plot temperature and sales observations;Fit a linear regression model;Compute residuals and compare in-range versus extrapolated predictions|Calculate predictions residuals and squared errors;Describe a confounding variable|Implement several gradient updates for a slope;Compare linear and polynomial model test error
8|Read a tiny grayscale array;Calculate one 3×3 edge-filter result by hand;Use OpenCV to visualise a filtered image|Calculate the output at two pixel positions;Describe two environmental causes of recognition failure|Implement NumPy filtering;Compare different border padding choices
9|Calculate four binary perceptron outputs;Change one weight and observe changes;Test a neural-network playground|Complete weighted-sum and activation calculations;Draw a two-layer network diagram|Study one loss-gradient update;Demonstrate why XOR cannot use one linear boundary
10|Join an image classifier to a recommendation rule;Log intermediate model outputs and decisions;Test blurry or unknown inputs with a human-review fallback|Draw the pipeline and label three interfaces;Write five unit or end-to-end test scenarios|Select a review threshold using held-out data;Compare accuracy with manual-review workload
11|Clean chronological demand data;Compare a naive mean with linear regression;Plot actual versus predicted demand with MAE|Write a one-page model card;Explain why time-aware splitting matters|Use past-value lagged features;Compare expanding-window validation with fixed split
12|Try a vague prompt and a structured prompt;Verify two factual model claims with trusted references;Draft target data baseline and metric for a project|Record a three-example prompt and verification log;Write a scoped one-page project proposal|Build a rubric for grounded responses;Document misuse and limitations in a model card
13|Use the official challenge when available or a practice dataset;Create a data dictionary and evaluation strategy;Fit a baseline and save parameters and score|Write a reproducible baseline report;Propose two controlled improvements|Try different sensible baselines;Quantify variation across valid splits
14|Inspect the worst model mistakes;Change a single feature or parameter;Compare score runtime and difficult cases|Maintain an experiment table;Explain two remaining weaknesses|Remove a feature group to test its contribution;Repeat experiments on multiple validation splits
15|Run the full model from setup notes;Present the baseline model and failure case in three minutes;Collect feedback and prioritise fixes|Complete README assumptions and result table;Reflect on the most informative experiments|Test missing noisy and unfamiliar inputs;Repeat setup in a fresh environment with pinned dependencies
""".strip()
lessons=[]
for line in DATA.splitlines():
    p=line.split("|")
    assert len(p)==8,(len(p),p[0])
    n,date,title,intro,course,lab,hw,advanced=p
    lessons.append(dict(n=int(n),date=date,title=title,intro=intro,course=course.split(";"),lab=lab.split(";"),homework=hw.split(";"),advanced=advanced.split(";")))
for line in TASKS.splitlines():
    p=line.split("|")
    assert len(p)==4,(len(p),p[0])
    n,lab,hw,advanced=p
    l=lessons[int(n)-1]
    assert l["n"]==int(n)
    for key,value in [("lab_tasks",lab),("homework_tasks",hw),("advanced_tasks",advanced)]:
        l[key]=value.split(";")
assert [x["n"] for x in lessons]==list(range(1,16))
ROOT=Path.cwd()
def write(path,text):
    dst=ROOT/path
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(text,encoding="utf-8")

CSS = """
:root{--bg:#f4f5ef;--paper:#fffefa;--ink:#1d2b28;--muted:#586862;--forest:#204d42;--dark:#163b33;--line:#dce2d9;--mint:#dcebe1;--gold:#dca64d;font:16px/1.65 Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink)}
*{box-sizing:border-box}body{margin:0;background:var(--bg)}a{color:var(--forest);text-underline-offset:.2em}a:hover{color:#0b2922}a:focus-visible{outline:3px solid #bd821b;outline-offset:3px}
.skip{position:absolute;left:-200vw}.skip:focus{left:1rem;top:1rem;background:white;padding:.5rem;z-index:3}
header.site,.shell,footer.site{width:min(1080px,calc(100% - 2.5rem));margin:auto}header.site{padding:1.15rem 0;display:flex;justify-content:space-between;gap:1rem;align-items:center;flex-wrap:wrap}
.brand{font-weight:800;color:var(--ink);text-decoration:none}.brand small{display:block;font-size:.76rem;font-weight:400;color:var(--muted)}.topnav{display:flex;flex-wrap:wrap;gap:1.05rem;font-size:.9rem}
.hero{background:var(--dark);color:#f6faf7;border-radius:1.4rem;padding:clamp(1.5rem,5vw,3.5rem);margin:1rem 0 1.5rem}.hero h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.1;letter-spacing:-.045em;margin:.35rem 0}.hero p{max-width:800px;color:#e4eee8}.eyebrow{font-size:.77rem;color:#b9d9c7!important;text-transform:uppercase;letter-spacing:.12em;font-weight:750}
.meta{display:flex;flex-wrap:wrap;gap:.55rem}.pill{border:1px solid #809b8d;padding:.28rem .7rem;border-radius:999px;font-size:.79rem;color:#fff}
.block{margin:2.1rem 0}.block h2{font-size:clamp(1.4rem,3vw,1.9rem);line-height:1.2;letter-spacing:-.02em;margin:0 0 .8rem}.block>p,.note{color:var(--muted);max-width:820px}
.module-nav{display:flex;gap:.55rem;flex-wrap:wrap;margin:1.2rem 0 2rem}.module-nav a{padding:.55rem .9rem;border:1px solid var(--line);background:var(--paper);border-radius:.75rem;text-decoration:none;font-weight:650;font-size:.91rem}.module-nav a[aria-current=page]{background:var(--forest);border-color:var(--forest);color:white}
.objectives{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.7rem;list-style:none;padding:0;counter-reset:item}.objectives li{background:var(--forest);color:#fff;border-radius:.85rem;padding:1rem 1rem 1rem 2.8rem;counter-increment:item;position:relative;font-size:.94rem}.objectives li:before{content:counter(item);position:absolute;left:1rem;top:1rem;font-weight:800;color:#b7d9c7}
.panel,.card,.week{border:1px solid var(--line);background:var(--paper);border-radius:1rem;padding:1rem 1.25rem}.panel li{margin:.65rem 0}.callout{border-left:4px solid var(--gold);background:#fff8e9;border-radius:0 .7rem .7rem 0;padding:1rem 1.2rem}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:.8rem}.card h3{margin:.2rem 0 .5rem;font-size:1.03rem}.card p{color:var(--muted)}
.week{margin:.85rem 0}.week h3{font-size:1.12rem;margin:0}.week p{color:var(--muted);margin:.45rem 0}.date{font-size:.86rem;color:var(--muted)}.links{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.5rem;margin-top:.8rem}.links a{padding:.65rem .7rem;background:#f7faf6;border:1px solid var(--line);border-radius:.65rem;font-size:.87rem;text-decoration:none;font-weight:750}.links small{display:block;font-size:.78rem;font-weight:400;color:var(--muted);margin-top:.3rem;line-height:1.4}
.phase{border-top:1px solid var(--line);padding-top:1rem;margin:2.5rem 0}.phase>p{color:var(--muted)}.tablewrap{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:.75rem;border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--mint)}
footer.site{border-top:1px solid var(--line);font-size:.85rem;color:var(--muted);padding:1.5rem 0 2.5rem;margin-top:3rem}
@media(max-width:700px){.links{grid-template-columns:repeat(2,minmax(0,1fr))}.objectives{grid-template-columns:1fr}}
@media print{body{background:white}.hero{color:black;background:white;border:1px solid #888}.hero p,.eyebrow,.pill{color:black!important}.objectives li{background:white;color:black;border:1px solid #777}.objectives li:before{color:black}.topnav,.module-nav{display:none}.week,.panel,.card{break-inside:avoid}}
""".strip()
write("assets/site.css", CSS)

def shell(title,summary):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(summary,quote=True)}"><title>{E(title)} · Machine Learning Club</title><link rel="stylesheet" href="/assets/site.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="site"><a class="brand" href="/">Machine Learning Club<small>Seven Hills International School · 2026–2027</small></a><nav class="topnav" aria-label="Site navigation"><a href="/">Programme</a><a href="/calendar/">Calendar</a><a href="/syllabus/">Syllabus</a><a href="/projects/">Projects</a><a href="/resources/">Resources</a></nav></header><main id="main" class="shell">'''
def finish():
    return '</main><footer class="site">Machine Learning Club · Seven Hills International School · Proposed dates subject to school confirmation.</footer></body></html>'
def ul(items, ordered=False):
    tag='ol' if ordered else 'ul'
    return f'<{tag}>'+''.join(f'<li>{E(x)}</li>' for x in items)+f'</{tag}>'
def weeklynav(l,current):
    return '<nav class="module-nav" aria-label="Week '+str(l['n'])+' materials">'+''.join(f'<a href="/w{l["n"]}/{k}/"'+(' aria-current="page"' if k==current else '')+f'>{label}</a>' for k,label in [('course','Course'),('lab','Laboratory'),('homework','Homework'),('advanced','Advanced')])+'</nav>'
def hero(eyebrow,title,desc,pills=()):
    return f'<section class="hero"><p class="eyebrow">{E(eyebrow)}</p><h1>{E(title)}</h1><p>{E(desc)}</p><div class="meta">'+''.join(f'<span class="pill">{E(x)}</span>' for x in pills)+'</div></section>'
def page(l,k):
    name={'course':'Course','lab':'Laboratory','homework':'Homework','advanced':'Advanced'}[k]
    html=shell(f'Week {l["n"]}: {name} — {l["title"]}',f'{name} objectives and activities for week {l["n"]} of Machine Learning Club')
    html+=hero(f'Week {l["n"]:02} · {name}',l['title'],l['intro'],[l['date'],'One weekly session · 60 minutes'])
    html+=weeklynav(l,k)
    html+='<section class="block"><h2>'+name+' learning objectives</h2><ol class="objectives">'+''.join(f'<li>{E(x)}</li>' for x in l[k])+'</ol></section>'
    if k=='course':
        html+='<section class="block"><h2>Concepts to explore</h2><div class="cards">'+''.join(f'<div class="card"><h3>Concept {i+1}</h3><p>{E(x)}</p></div>' for i,x in enumerate(l['course']))+'</div></section>'
        html+='<section class="block"><h2>Paper-based checkpoint</h2><div class="callout">Make a small worked example of this topic. Record the inputs, each intermediate step and the final result. Explain which assumptions make the result valid.</div></section>'
        html+='<section class="block"><h2>One-hour meeting structure</h2><p>5 minutes recap · 15 minutes explanation · 15 minutes manual practice · 20 minutes guided laboratory · 5 minutes exit ticket. Course and laboratory are parts of the same weekly hour, not separate sessions.</p></section>'
    elif k=='lab':
        html+='<section class="block"><h2>Guided laboratory tasks</h2><div class="panel">'+ul(l['lab_tasks'],True)+'</div><p>Work using PRIMM: Predict, Run, Investigate, Modify, Make. Starter code and AI assistance are allowed if you can explain the result.</p></section>'
        html+='<section class="block"><h2>Evidence to keep</h2><div class="callout">A concise worked calculation, a code/notebook result, and a written explanation of one error or limitation.</div></section>'
    elif k=='homework':
        html+='<section class="block"><h2>Homework tasks</h2><div class="panel">'+ul(l['homework_tasks'],True)+'</div></section>'
        html+='<section class="block"><h2>Submission checklist</h2>'+ul(['Show your reasoning, not just final answers.','Identify input data, output and one possible limitation.','Include a readable figure, table or notebook output where useful.'])+'</section>'
    else:
        html+='<section class="block"><h2>Optional advanced challenges</h2><div class="panel">'+ul(l['advanced_tasks'],True)+'</div></section>'
        html+='<section class="block"><h2>Evidence of deeper understanding</h2>'+ul(['State a testable hypothesis before changing a model.','Compare results using the same evaluation procedure.','Explain what the experiment supports and what remains uncertain.'])+'</section>'
    html+='<section class="block"><h2>Continue learning</h2><div class="module-nav"><a href="/">All 15 weeks</a>'
    if l['n']>1:html+=f'<a href="/w{l["n"]-1}/{k}/">← Previous week</a>'
    if l['n']<15:html+=f'<a href="/w{l["n"]+1}/{k}/">Next week →</a>'
    return html+'</div></section>'+finish()
for l in lessons:
    for k in ('course','lab','homework','advanced'):
        if l['n']==1 and k in ('course','lab'):continue
        write(f'w{l["n"]}/{k}/index.html',page(l,k))

# Retain detailed, functioning Week 1 pages; only adjust schedule and integrate new objectives.
for kind in ('course','lab'):
    path=ROOT/f'w1/{kind}/index.html'
    text=path.read_text(encoding='utf-8')
    text=text.replace('2 November 2026','2 December 2026')
    text=text.replace('About 55 minutes','Course reference · self-paced').replace('About 45 minutes','Lab reference · self-paced')
    nav=weeklynav(lessons[0],kind)
    if '<nav class="module-nav" aria-label="Week 1 materials">' not in text:
        text=text.replace('    <section class="section" aria-labelledby="'+('outcomes-title' if kind=='course' else 'method-title')+'">',nav+'\n    <section class="section" aria-labelledby="'+('outcomes-title' if kind=='course' else 'method-title')+'">',1)
    if kind=='course':
        if "Explain training labels" not in text:
            text=text.replace('<li>Use a problem’s output and available evidence to suggest an approach.</li>','<li>Use a problem’s output and available evidence to suggest an approach.</li><li>Explain training labels, predictions and what confidence does not guarantee.</li>')
        teacher='''<details class="teacher-notes"><summary>Teacher guide · 60-minute club session</summary><div class="teacher-content"><p>Use selected course sections and a short lab activity in the same 60-minute meeting. The full interactive course, laboratory and extended slides remain useful for self-paced study.</p><ol><li>00–05: rule versus learned prediction warm-up.</li><li>05–20: AI, ML, labels and confidence.</li><li>20–35: manual classification and evidence exercise.</li><li>35–55: selected matching cases and/or object-classifier demo.</li><li>55–60: exit ticket explaining one model failure.</li></ol></div></details>'''
    else:
        obj='<section class="section" aria-labelledby="lab-objectives"><div class="section-heading"><span class="section-number">00</span><div><h2 id="lab-objectives">Laboratory learning objectives</h2></div></div><ul class="outcomes">'+''.join(f'<li>{E(x)}</li>' for x in lessons[0]['lab'])+'</ul></section>'
        if 'id="lab-objectives"' not in text:
            text=text.replace('<section class="section" aria-labelledby="method-title">',obj+'\n<section class="section" aria-labelledby="method-title">',1)
        ext='''<section class="section" aria-labelledby="teachable"><div class="section-heading"><span class="section-number">05</span><div><h2 id="teachable">Extension: image classification with Teachable Machine</h2></div></div><div class="card"><p>Train a small image model at <a href="https://teachablemachine.withgoogle.com/">Teachable Machine</a> using two everyday objects. Do not collect classmates' faces, voices or private information.</p><ol><li>Collect varied labelled images of each object.</li><li>Train the model and test five unseen examples.</li><li>Record the predicted class, confidence and actual class.</li><li>Describe what happens when light or background changes.</li></ol><p>Confidence is not a guarantee of correctness.</p></div></section>'''
        if 'id="teachable"' not in text:
            text=text.replace('<details class="teacher-notes">',ext+'\n<details class="teacher-notes">',1)
        teacher='''<details class="teacher-notes"><summary>Teacher guide · 60-minute club session</summary><div class="teacher-content"><p>Use selected method-matching cards (around 10 minutes), then a short Teachable Machine object demo (around 10 minutes) during the last part of the one-hour session. The complete seven-card lab is a self-paced extension. Students should describe a predicted class, a confidence score and a failure case.</p></div></details>'''
    text,count=re.subn(r'<details class="teacher-notes">.*?</details>',teacher,text,count=1,flags=re.S)
    assert count==1,kind
    path.write_text(text,encoding='utf-8')
if '.curriculum-nav{' not in (ROOT/'w1/week1.css').read_text(encoding='utf-8'):
    with (ROOT/'w1/week1.css').open('a',encoding='utf-8') as f:
        f.write('\n.curriculum-nav{display:flex;gap:.6rem;flex-wrap:wrap;margin:1.2rem 0 2rem}.curriculum-nav a{padding:.55rem .9rem;border-radius:.65rem;border:1px solid var(--line);background:var(--surface);text-decoration:none;font-weight:700;font-size:.9rem}.curriculum-nav a[aria-current=page]{background:var(--forest);color:white}\n')

home=shell('2026–2027 programme','Fifteen weekly one-hour Machine Learning Club sessions, with course, lab, homework and advanced objectives.')
home+=hero('2026–27 · Machine Learning Club','Learn how machines learn.','Hands-on foundations, integrated AI systems and optional preparation for FIICode.', ['15 sessions · one hour each','Wednesdays 16:00–17:00 (proposed)','70 RON per session','Maximum 10 students'])
home+='<p class="note">Proposed dates from 2 December 2026 to 7 April 2027. The school calendar and final FIICode dates must be confirmed. <a href="https://forms.gle/Hk1vZM12i9vTF1zc9">Registration form</a>.</p>'
for start,end,title,description in [(1,9,'I · Foundations','Mathematics and individual models, first on paper and then in Python.'),(10,12,'II · Integrated AI Systems','Combine models, data pipelines, interfaces and responsible evaluation.'),(13,15,'III · FIICode Preparation','Build baselines, tune fairly and present reproducible projects.')]:
    home+=f'<section class="phase"><h2>{E(title)}</h2><p>{E(description)}</p>'
    for l in lessons[start-1:end]:
        home+=f'<article class="week"><h3>Week {l["n"]} — {E(l["title"])}</h3><div class="date">{E(l["date"])}</div><p>{E(l["intro"])}</p><div class="links">'
        for k,label in [('course','Course'),('lab','Laboratory'),('homework','Homework'),('advanced','Advanced')]:
            home+=f'<a href="/w{l["n"]}/{k}/">{label}<small>{E(l[k][0])}</small></a>'
        home+='</div>'
        if l['n']==1:home+='<p><a href="/w1/slides/">Existing Week 1 slides (PDF)</a> · <a href="/w1/lab/">Interactive matching activity</a></p>'
        home+='</article>'
    home+='</section>'
write('index.html',home+finish())

cal=shell('Club calendar','Proposed Machine Learning Club meeting dates in 2026 and 2027.')
cal+=hero('Schedule','15 Wednesdays · 16:00–17:00','One-hour weekly lessons, excluding planned winter and February breaks.',['Dates proposed · subject to school confirmation'])
cal+='<section class="block"><h2>Dates and topics</h2><div class="tablewrap"><table><thead><tr><th>#</th><th>Date</th><th>Lesson</th></tr></thead><tbody>'
for l in lessons:
    if l['n']==4:cal+='<tr><td>—</td><td>Winter holiday</td><td>No weekly meeting between 16 December and 13 January</td></tr>'
    if l['n']==10:cal+='<tr><td>—</td><td>24 February 2027</td><td>Proposed February holiday break (confirm with the school)</td></tr>'
    cal+=f'<tr><td>{l["n"]}</td><td>{E(l["date"])}</td><td><a href="/w{l["n"]}/course/">{E(l["title"])}</a></td></tr>'
cal+='</tbody></table></div><p class="note">FIICode 2027 registration and final dates are not confirmed here. Additional finalist mentoring, if offered, would be outside the 15 regular meetings.</p></section>'
write('calendar/index.html',cal+finish())

sy=shell('Syllabus','15-session Machine Learning Club syllabus.')
sy+=hero('Syllabus','Explain it. Calculate it. Test it. Build it.','Every week includes learning outcomes in four parts: Course, Laboratory, Homework and optional Advanced.')
sy+='<section class="block"><h2>Learning progression</h2><div class="cards">'
for title,desc in [('By Week 3','Use probability and information gain to draw an ID3 tree.'),('By Week 6','Evaluate classifiers and apply KNN and K-Means by hand.'),('By Week 9','Fit a regression, work with image filters and evaluate a perceptron.'),('By Week 12','Describe and test a multicomponent system and verify claims from an LLM.'),('By Week 15','Demonstrate a reproducible project with a metric and clear limitations.')]:
    sy+=f'<article class="card"><h3>{E(title)}</h3><p>{E(desc)}</p></article>'
sy+='</div></section><section class="block"><h2>Method</h2><div class="panel">'+ul(['5 min recap and motivation','15 min conceptual explanation','15 min worked exercise on paper','20 min guided PRIMM coding laboratory','5 min exit ticket or reflection'])+'</div></section>'
sy+='<section class="block"><h2>Weekly course objectives</h2><div class="panel">'+ul([f'Week {l["n"]}: {l["course"][0]}' for l in lessons],True)+'</div></section>'
write('syllabus/index.html',sy+finish())

pr=shell('Projects and FIICode','Integrated ML club projects and competition preparation.')
pr+=hero('Applied machine learning','Projects and FIICode','Projects begin as simple, evidence-based prototypes. Participation in competitions is optional.')
pr+='<section class="block"><h2>Project examples</h2><div class="cards">'
for title,desc in [('Recycling assistant','An image classifier plus rules and a human-review fallback for uncertain items.'),('Demand forecasting','Data cleaning, a simple baseline, a regression model and a clear error chart.'),('Ecosystem explorer','Environmental data, clustering, numeric predictions and a dashboard.')]:
    pr+=f'<article class="card"><h3>{E(title)}</h3><p>{E(desc)}</p></article>'
pr+='</div></section><section class="block"><h2>Competition preparation</h2><div class="panel">'+ul(['February: introduce FIICode, recruit interested students and verify official registration announcements.','March: respond to an official challenge if published; otherwise practise with a representative dataset.','24 March: establish an evaluation metric and baseline.','31 March: improve one component and analyse errors.','7 April: present and test a complete project.','April–May: optional additional mentoring if any students qualify for a final.'],True)+'</div><p class="note">The official FIICode 2027 schedule is not yet confirmed; these are preparation milestones, not announced contest dates.</p></section>'
write('projects/index.html',pr+finish())

rs=shell('Learning resources','Resources for Machine Learning Club lessons.')
rs+=hero('Resources','Tools, notebooks and reading','Use school-approved tools and avoid uploading identifiable student information.')
rs+='<section class="block"><h2>Recommended links</h2><div class="panel"><ul>'
for url,name,why in [('https://experience-ai.org/','Experience AI','Classroom activities'),('https://teachablemachine.withgoogle.com/','Teachable Machine','Train simple classification models'),('https://colab.research.google.com/','Google Colab','Python notebooks'),('https://scikit-learn.org/stable/','scikit-learn','KNN, K-Means, trees and regression'),('https://numpy.org/doc/stable/','NumPy','Numerical arrays'),('https://docs.opencv.org/','OpenCV','Image filtering'),('https://playground.tensorflow.org/','Neural Network Playground','Visualise a neural network')]:
    rs+=f'<li><a href="{url}">{E(name)}</a> — {E(why)}</li>'
rs+='</ul></div></section><section class="block"><h2>Local materials</h2><p><a href="/w1/slides/">Week 1 extended slides (PDF)</a> and the week-by-week objective pages linked on the homepage.</p></section>'
write('resources/index.html',rs+finish())

# Check that all 60 distinct learning-material URLs have corresponding files with objectives.
for l in lessons:
    for k in ('course','lab','homework','advanced'):
        content=(ROOT/f'w{l["n"]}/{k}/index.html').read_text(encoding='utf-8')
        assert '<html' in content and '</html>' in content, (l['n'],k)
        assert ('learning objectives' in content.lower() or 'by the end' in content.lower()), (l['n'],k)
for slug in ('calendar','syllabus','resources','projects'):
    assert (ROOT/slug/'index.html').exists()
assert len(list(ROOT.glob('w*/**/index.html')))==61  # 60 lesson pages + existing week-1 slides page
print('OK: 15 weeks, 60 objective pages, calendar, syllabus, projects, resources and existing slides.')

# Apply the original plain Georgia/white homepage layout after page generation.
import runpy
runpy.run_path(str(ROOT / "scripts/apply_classic_theme.py"))
