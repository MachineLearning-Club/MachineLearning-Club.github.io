#!/usr/bin/env python3
from pathlib import Path
from html import escape as E
import re
R=Path(__file__).resolve().parents[1]
s=(R/"scripts/generate_curriculum.py").read_text()
lines=s.split('DATA = """',1)[1].split('""".strip()',1)[0].strip().splitlines()
tasks=s.split('TASKS = """',1)[1].split('""".strip()',1)[0].strip().splitlines()
data={}
for line in lines:
    n,date,title,desc,co,lab,home,adv=line.split("|")
    data[int(n)]=dict(date=date,title=title,desc=desc,course=co.split(";"),lab=lab.split(";"),homework=home.split(";"),advanced=adv.split(";"))
for line in tasks:
    n,lab,home,adv=line.split("|")
    data[int(n)].update(lab_tasks=lab.split(";"),homework_tasks=home.split(";"),advanced_tasks=adv.split(";"))
def ul(rows,tag="ul"):return "<"+tag+">"+"".join("<li>"+E(x)+"</li>" for x in rows)+"</"+tag+">"
def nav(n,k):
    return '<nav class="lesson-nav" aria-label="Week '+str(n)+' materials">'+''.join('<a href="/w'+str(n)+'/'+key+'/"'+(' aria-current="page"' if key==k else '')+'>'+label+'</a>' for key,label in [('course','Course'),('lab','Laboratory'),('homework','Homework'),('advanced','Advanced')])+'</nav>'
questions=[
"Compare a fixed timer with a model trained to label images. How could you tell the difference?",
"Compute the mean of 2, 4, 4 and 6 and compare entropy in a 3:1 versus 2:2 split.",
"Calculate information gain for two categorical root-split candidates on a tiny dataset.",
"Construct a confusion matrix from eight predictions and calculate accuracy.",
"Calculate distances from (2,3) to (2,5), (4,3) and (5,7). Which neighbours are closest?",
"Assign points to two centres and calculate updated K-Means centroids.",
"For y = 6.2x + 5.1, predict y at x = 20 and calculate an example residual.",
"Multiply a 3 by 3 image patch by an edge kernel and sum the products.",
"Evaluate a step neuron with inputs (1,0), weights (2,-1) and bias -0.5.",
"Sketch a vision classifier followed by a decision rule. Where should uncertain predictions go?",
"Calculate mean absolute error for a naive demand forecast against actual values.",
"What checks establish whether a language model's confident factual claim is supported?",
"Select an input, target, baseline and validation metric for an example competition problem.",
"A model improves on one data split and worsens on another. How would you test the improvement?",
"Explain a final project in three minutes: problem, data, baseline, score and failure case."
]
for n,v in data.items():
 for k,label in [('course','Course'),('lab','Laboratory'),('homework','Homework'),('advanced','Advanced')]:
    if n==1 and k in ('course','lab'):continue
    h=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Week {n} · {E(v["title"])} · {label}</title><link rel="stylesheet" href="/assets/site.css"></head>
<body><header class="site"><a class="brand" href="/">Machine Learning Club</a>
<p class="site-subtitle">Seven Hills International School · 2026–2027</p>
<p><a href="/">← All weeks</a></p></header>
<main class="shell"><p class="lesson-meta">Week {n} · {E(v["date"])} · {label}</p>
<h1>{E(v["title"])}</h1><p>{E(v["desc"])}</p>
{nav(n,k)}
<section><h2>{label} objectives</h2>{ul(v[k])}</section>
'''
    if k=="course":
        h+='<section><h2>On-paper exercise</h2><p>'+E(questions[n-1])+'</p><p>Show your reasoning, then check it with a small program or a prepared notebook.</p></section>\n'
    else:
        kind={'lab':'Lab activities','homework':'Homework exercises','advanced':'Optional advanced challenges'}[k]
        h+='<section><h2>'+kind+'</h2>'+ul(v[k+'_tasks'],"ol")+'</section>\n'
        if k=="lab":h+='<section><h2>What to record</h2><p>Record a worked example, a tested result and one limitation. Use PRIMM: Predict, Run, Investigate, Modify, Make.</p></section>'
        if k=="homework":h+='<section><h2>Submission</h2><p>Include your reasoning, calculations or output, and one limitation.</p></section>'
        if k=="advanced":h+='<section><h2>Reporting</h2><p>State a hypothesis, compare results and explain what your evidence supports.</p></section>'
    h+='<nav class="lesson-pagination" aria-label="Other weeks">'
    if n>1:h+=f'<a href="/w{n-1}/{k}/">← Week {n-1}</a>'
    if n<15:h+=f'<a href="/w{n+1}/{k}/">Week {n+1} →</a>'
    h+='</nav></main><footer class="site">Machine Learning Club · Seven Hills International School</footer></body></html>\n'
    (R/f'w{n}/{k}/index.html').write_text(h,encoding="utf-8")
for k in ('course','lab'):
 p=R/f'w1/{k}/index.html'
 h=p.read_text()
 h=re.sub(r'<nav class="module-nav" aria-label="Week 1 materials"', '<nav class="curriculum-nav" aria-label="Week 1 materials"', h)
 if '../classic.css' not in h:
  h=h.replace('<link rel="stylesheet" href="../week1.css">','<link rel="stylesheet" href="../week1.css">\n  <link rel="stylesheet" href="../classic.css">',1)
 assert h.count('class="curriculum-nav"')==1
 p.write_text(h)
print("Simplified all 58 generated lesson pages and repaired Week 1 nav.")
