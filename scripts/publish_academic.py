#!/usr/bin/env python3
"""Publish the reviewed 15-week programme using the academic white design.

The Week 1 and Week 2 long-form lessons are migrated from the former /preview
proof of concept. Later weeks are editorial outlines until individually reviewed.
Run only this generator to regenerate published pages.
"""
from pathlib import Path
from html import escape
import json, re, shutil

ROOT=Path(__file__).resolve().parents[1]
# Each unit: title | course themes ; separated | laboratory activities ; separated |
# mandatory ; homework ; research | advanced investigations ; separated
RAW="""What Is AI? Rules and Learning|Classical programming and explicit rules;Artificial intelligence and search;Machine learning from data;Supervised, unsupervised and reinforcement learning;Natural language processing|Quick, Draw! and Teachable Machine;Compare rules, search and learned classifiers|Build a visual Python thermostat;Train a supplied ID3 component on labelled heating decisions;Repair a smart-home application that compares the two approaches|State transitions;Constraint satisfaction;Generalisation
Probabilistic Learning and Iterative Dichotomiser 3 (ID3)|Uncertainty and frequency;Shannon entropy;Information gain;Recursive categorical ID3;Predictions and limitations|Explore entropy with class sliders;Build and visualise a categorical ID3 tree|Calculate information gain;Apply ID3 to a second dataset;Handle missing and unseen feature values|Recursive construction;Overfitting and stopping;Worked calculations
ID3 Extensions and Introduction to K-Means|Numerical attributes and thresholds;Training and test data;Unsupervised learning;Distances and centroids;K-Means iteration|Compare decision tree depths;Experiment with K-Means clusters|Evaluate a learned tree on unseen records;Work through two centroid updates;Compare initial centroids|Tree stopping strategies;K-Means objective function;Centroid calculations
K-Means and K-Nearest Neighbours|Clustering versus classification;Distance between data points;K-Means centroid updates;KNN classification by voting;Feature scaling and choosing K|Use K-Means and KNN side by side;Move points and change K|Calculate neighbour distances;Complete a KNN implementation;Investigate feature scaling|KNN decision boundaries;Distance metrics;K-Means convergence
Working with Images as Input|Pixels and grids;RGB and grayscale;Multidimensional NumPy arrays;Reading and resizing images;Thresholds brightness and contrast|Use a pixel-grid editor;Change images with NumPy|Modify individual pixels;Build an image transformation pipeline;Make a pixel-matrix editor|Matrices and channels;Transforms;Computational cost
Computer Vision Techniques|Image recognition;Kernels and filters;Convolution;Edge detection;Handcrafted versus learned features|Change an image kernel;Apply blur and edge detection|Calculate convolution outputs;Compare filters;Invent and explain a filter|Padding and stride;Spatial locality;Convolution mathematics
Predicting Handwriting|Handwriting as pixel data;Classification labels;Training and testing;Confusion matrices;Misclassification and robustness|Draw digits in a browser recogniser;Train a small prepared handwriting classifier|Test digits;Improve preprocessing;Analyse noisy examples|Image features;Classification mathematics;Confusion matrices
Perceptron and Neural Networks|The computational neuron;Weights and bias;Activation functions;Linear classification;Feed-forward networks|TensorFlow Playground;Adjust weights and bias in a neuron|Calculate a perceptron output;Train a small supplied model;Study linear inseparability|Linear boundaries;Perceptron updates;XOR
Backpropagation in Neural Networks|Predictions and errors;Loss functions;Gradient descent;The chain rule;Backpropagation and training loops|Explore a loss function;Visualise gradient descent and loss history|Update one model parameter;Compare learning rates;Implement a simplified backward step|Partial derivatives;Computational graphs;Worked backpropagation
Generative Pre-Trained Transformers (GPT)|Tokens and numerical text;Embeddings;Transformers;Attention;Next-token prediction;Limits and reliability|Try a tokenizer;Explore Transformer Explainer;Compare next-token baselines|Tokenise short passages;Compare generator outputs;Fact-check generated answers|Vectors and similarity;Attention scores;Generation mathematics
Object-Oriented Programming|Objects and classes;Attributes and constructors;Methods;Composition;Encapsulation and interfaces|Build sensor agent and controller objects;Reuse a classifier as an object|Implement a Python class;Combine classes in a simulation;Refactor procedural code|Object invariants;Interfaces;Design trade-offs
Software Engineering: Architecture, Workflows and Pipelines|User stories and requirements;Data-to-prediction pipelines;Testing and debugging;Modular architecture;Git and GitHub;Reproducibility|Build a small ML application;Experiment with visual Git operations|Draw an AI pipeline;Improve and document an app;Add tests and a component|Architecture patterns;Testing strategies;Reproducible experiments
FIICode I: Building the First Solution|Read a problem specification;Explore data;Define metrics;Choose a baseline;Plan the team|Start a competition-style project;Implement a baseline|Explain a dataset;Deliver a baseline;Compare alternatives|Competition reasoning;Baseline analysis;Selected IOAI problems
FIICode II: Improving the Solution|Find prediction errors;Engineer features;Tune hyperparameters;Compare models fairly;Measure performance;Integrate improvements|Continue the FIICode project;Evaluate controlled changes|Explain model errors;Implement a measured improvement;Research a larger alternative|Optimisation;Ablations;Experiment design
FIICode III: Mock Hackathon|Finish and test the application;Write documentation;Demonstrate behaviour;Present limitations;Reflect on decisions|Present final projects;Test peers' applications|Submit a working project;Write a technical report and demonstration;Extend the project|Selected IOAI and ONIA exercises;Worked solutions;Further-study directions"""
W=[]
for line in RAW.splitlines():
    t,c,l,h,a=line.split("|")
    W.append(dict(title=t,course=c.split(";"),lab=l.split(";"),hw=h.split(";"),advanced=a.split(";")))
assert len(W)==15
D=ROOT/"data"/"curriculum_2026.json"
D.write_text(json.dumps({"status":"Working curriculum for teacher review","weeks":[dict(n=i+1,**w) for i,w in enumerate(W)]},indent=2,ensure_ascii=False)+"\n")
def tabs(n,active=""):
    labels=[("course","Course"),("lab","Laboratory"),("homework","Homework"),("advanced","Advanced")]
    s="".join(f'<a href="/w{n}/{k}/"'+(' aria-current="page"' if active==k else '')+f'>{name}</a>' for k,name in labels)
    return f'<nav class="lesson-tabs" aria-label="Week {n} learning materials">{s}<a href="/quiz/?week={n}">Quiz</a></nav>'
def top(n,kind):
    title=escape(W[n-1]["title"])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week {n} · {kind.title()} · Machine Learning Club</title><link rel="stylesheet" href="/assets/academic.css"></head><body><header class="site"><a class="site-name" href="/">Machine Learning Club</a><p class="site-sub">Seven Hills International School · 2026–2027</p><p class="breadcrumb"><a href="/">All lessons</a> / Week {n} / {kind.title()}</p></header><main><p class="eyebrow">Week {n:02} · {kind.title()}</p><h1>{title}</h1>{tabs(n,kind)}'''
def bottom(n):
    return f'''<nav class="lesson-pagination">{f'<a href="/w{n-1}/course/">← Week {n-1}</a>' if n>1 else ''}{f'<a href="/w{n+1}/course/">Week {n+1} →</a>' if n<15 else ''}</nav></main><footer class="site">Machine Learning Club · Seven Hills International School</footer></body></html>'''
def write(n,kind,body):
    p=ROOT/f"w{n}"/kind/"index.html";p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(top(n,kind)+body+bottom(n),encoding="utf-8")
def section(title,content):
    return f"<section><h2>{escape(title)}</h2><p>{escape(content)}</p></section>"
def make(n,k):
    w=W[n-1]
    if k=="course":
        toc="<ol>"+"".join(f'<li><a href="#s{i}">{escape(topic)}</a></li>' for i,topic in enumerate(w["course"],1))+"</ol>"
        body=section("Course summary",f"This lesson introduces {w['title'].lower()} through concrete problems, visual experiments and Python.")+f'<nav class="toc"><strong>Contents</strong>{toc}</nav>'
        for i,topic in enumerate(w["course"],1):
            body+=f'<section id="s{i}"><h2>{i}. {escape(topic)}</h2><p>Start by observing a practical example of {escape(topic.lower())}. Describe the input, the algorithm and the output, then compare what changes when an input is modified.</p></section>'
        body+=section("Hands-on continuation","Open the Laboratory for prepared experiments, editable code and the accompanying observation tasks.")
        body+=f'<p><a href="/w{n}/lab/">Continue to Laboratory</a></p>'
    elif k=="lab":
        body=section("Learning goals","Observe a working experiment, change a parameter, run a prepared Python example and explain the result.")
        for i,activity in enumerate(w["lab"],1):
            body+=section(f"{i}. {activity}","Predict the result, run the activity, modify one input and compare the observations.")
        body+=section("Browser notebook","The default environment is JupyterLite or a browser-hosted marimo notebook; any Colab link is optional. Download the starter notebook where available.")
        body+=f'<p><a href="/w{n}/lab/starter.ipynb" download>Starter notebook (if available)</a></p>'
    elif k=="homework":
        body=section("Context",f"Extend the example from the Week {n} laboratory into a small, demonstrable program.")
        for heading,task in zip(["Mandatory (1p)","Homework (2p)","Research (optional)"],w["hw"]):
            body+=section(heading,task)
        body+=section("Submission","Submit the notebook or source code and a short explanation of what changed and what you observed.")
    else:
        body=section("Advanced study","An optional technical booklet develops deeper concepts and progressively challenging exercises.")
        for i,a in enumerate(w["advanced"],1):
            body+=section(f"Problem {i}: {a}","Investigate the problem using a small fully specified example, show intermediate steps and justify the final result.")
        body+=section("Review status","This booklet is an editorial outline. Worked solutions and printable PDFs will be released after teacher review.")
    write(n,k,body)
# Preserve full authored preview cases in the published lesson paths; rehome the ID3
# case to Week 2 because the curriculum now introduces ID3 in that lesson.
for old,new in [(1,1),(3,2)]:
    for k in ["course","lab","homework","advanced"]:
        src=ROOT/"preview"/f"w{old}"/k
        if not src.exists(): continue
        dst=ROOT/f"w{new}"/k
        dst.mkdir(parents=True,exist_ok=True)
        for file in src.iterdir():
            if file.is_file(): shutil.copy2(file,dst/file.name.replace(f"week-{old:02}",f"week-{new:02}"))
        p=dst/"index.html"
        content=p.read_text()
        content=content.replace("/preview/assets/poc.css","/assets/academic.css").replace("/preview/assets/experiment.js","/assets/academic-experiments.js")
        content=content.replace(f"/preview/w{old}/",f"/w{new}/").replace("href=\"/preview/\"","href=\"/\"")
        content=content.replace("/main/preview/", "/main/").replace(f"week-{old:02}",f"week-{new:02}")
        content=content.replace("Two-week preview","All lessons").replace(f"Week {old}",f"Week {new}").replace(f"Week 0{old}",f"Week 0{new}")
        content=content.replace("</nav>",f'<a href="/quiz/?week={new}">Quiz</a></nav>',1)
        p.write_text(content)
        if (dst/"print.html").exists():
            pp=dst/"print.html";s=pp.read_text().replace("/preview/assets/poc.css","/assets/academic.css").replace(f"/preview/w{old}/",f"/w{new}/").replace(f"week-{old:02}",f"week-{new:02}");pp.write_text(s)
        for ext in ["ipynb","csv"]:
            for file in src.glob("*."+ext):
                shutil.copy2(file,dst/file.name)
(ROOT/"assets"/"academic.css").write_text(((ROOT/"preview/assets/poc.css").read_text() if (ROOT/"preview/assets/poc.css").exists() else (ROOT/"assets/academic.css").read_text().split("\n.week{margin:22px")[0])+ "\n.week{margin:22px 0 31px}.week h3{margin-bottom:4px}.week .lesson-tabs{margin:7px 0 23px}.lesson-pagination{border-top:1px solid #ddd;margin-top:42px;padding-top:15px;display:flex;justify-content:space-between}\n")
if (ROOT/"preview/assets/experiment.js").exists(): shutil.copy2(ROOT/"preview/assets/experiment.js",ROOT/"assets/academic-experiments.js")
# Render remaining lesson pages only as clearly labelled draft outlines.
for n in range(3,16):
    for kind in ("course","lab","homework","advanced"):make(n,kind)
modules=[("I","Foundations of Artificial Intelligence",1,3),("II","Machine Learning, Computer Vision and Neural Networks",4,9),("III","Generative AI, Software Engineering and FIICode",10,15)]
home='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Machine Learning Club</title><link rel="stylesheet" href="/assets/academic.css"></head><body><header class="site"><a class="site-name" href="/">Machine Learning Club</a><p class="site-sub">Seven Hills International School · 2026–2027</p><p><strong>Registration open.</strong> <a href="https://forms.gle/Hk1vZM12i9vTF1zc9">Register here</a></p></header><main><h1>Machine Learning Club</h1><p class="deck">Understand something → experiment with it → modify it → use it to solve a problem.</p><p>15 sessions across three modules, from algorithms and data to neural networks, software engineering and a final competition-style project.</p><section><h2>How to use this club</h2><p>Start with prepared Python examples and datasets. Laboratories are designed for direct browser experiments; GitHub is introduced later, not required to begin.</p></section>'''
for roman,name,start,end in modules:
    home+=f'<section><h2>Module {roman} — {escape(name)}</h2>'
    for n in range(start,end+1):home+=f'<article class="week"><h3>Week {n} — {escape(W[n-1]["title"])}</h3>{tabs(n)}</article>'
    home+="</section>"
home+='''<section><h2>Resources</h2><p><a href="/syllabus/">Syllabus</a> · <a href="/calendar/">Calendar</a> · <a href="/resources/">Resources</a> · <a href="/materials/">Teaching materials</a> · <a href="/quiz/">Weekly quizzes</a> · <a href="/projects/">Projects</a></p></section></main><footer class="site">Machine Learning Club · Seven Hills International School</footer></body></html>'''
(ROOT/"index.html").write_text(home)
# Do not serve outdated question banks as if they matched the revised courses.
catalog={"version":2,"notice":"Revised curriculum. Quizzes are under review before publication; existing prototype question banks are archived until remapped.","quizzes":[]}
for n,w in enumerate(W,1):
    catalog["quizzes"].append({"week":n,"id":f"mlc-{n:02}","title":w["title"],"subject":", ".join(w["course"][:3]),"status":"demo" if n in (2,3) else "planned","durationMinutes":5,"questionCount":10 if n in (2,3) else None,"maxPoints":10 if n in (2,3) else None})
(ROOT/"quiz/data/catalog.json").write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+"\n")
# Preserve old public site supporting pages but render them with the same academic CSS.
for p in [ROOT/"assets/site.css",ROOT/"w1/classic.css",ROOT/"w1/week1.css"]:
    p.write_text((ROOT/"assets/academic.css").read_text()+"\n.brand{color:#222}.lesson-nav{display:flex;flex-wrap:wrap;gap:18px;border-bottom:1px solid #ddd;padding-bottom:12px}.lesson-nav a[aria-current=page]{font-weight:bold}\n")
# Align the quiz introduction with Week 1 inclusion and current publication status.
q=ROOT/"quiz/index.html"
q.write_text(q.read_text().replace("Short knowledge checks beginning with Week 2.","Short weekly knowledge checks, including Week 1, will be published after teacher review.").replace("Questions for Weeks 2 and 3 are draft examples awaiting approval. Weeks 4–15 are planned but not yet written.","Weeks 2 and 3 contain draft practice quizzes; Weeks 1 and 4–15 await teacher review."))
# Remove every tracked preview artifact, including its endpoint.
if (ROOT/"preview").exists(): shutil.rmtree(ROOT/"preview")
print(f"Published {len(W)} weeks; removed /preview; migrated Week 1 and ID3 case (to Week 2).")
