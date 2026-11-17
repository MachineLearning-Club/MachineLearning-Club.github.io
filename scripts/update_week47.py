#!/usr/bin/env python3
"""Authoritative generator for teacher-authored Weeks 4–7.
Preserve site-wide header, tab links, footer, and minimalist styles."""
from pathlib import Path
from html import escape
import re
ROOT=Path(__file__).resolve().parents[1]
TITLES={
 4:'Revision: Supervised and Unsupervised Learning',
 5:'Computer Vision: Images as Data',
 6:'Perceptrons: A First Learning Neuron',
 7:'Neural Networks and Training'}
LABELS=dict(course='Course',lab='Laboratory',homework='Homework',advanced='Advanced')
SUBMISSION="""<div class="submission-form" data-submission-week="{week}">
 <label>Student name<input type="text" class="student-name" maxlength="90" autocomplete="name" placeholder="First name, last name"></label>
 <label class="file-drop">Choose your files<input class="submission-files" type="file" accept=".ipynb,.py,.csv,.pdf,.zip,.txt" multiple></label>
 <p class="submission-selected" aria-live="polite">No file selected.</p>
 <button type="button" class="prepare-submission">Download named submission</button>
 <p class="submission-status" aria-live="polite"></p>
 <p class="understated">This prepares a named ZIP locally; it does not send anything to the teacher.</p>
</div>"""
for week,title in TITLES.items():
 for kind in LABELS:
  path=ROOT/f'w{week}/{kind}/index.html'
  fragment=(ROOT/f'data/week47/w{week}_{kind}.html').read_text(encoding='utf-8')
  if kind=='lab':
   fragment=fragment.replace(
     '<section id="submission" class="submission-drop"><h2>Submission</h2>',
     '<section id="submission" class="submission-drop"><h2>Submission</h2>'+SUBMISSION.format(week=week))
  main='<main class="lesson-content week23-academic week47-academic'+(' course-lesson' if kind=='course' else '')+'">'
  main+='<p class="eyebrow">Week '+str(week).zfill(2)+' · '+LABELS[kind]+'</p>'
  main+='<h1>'+escape(title)+'</h1>'
  if kind=='course':main+='<p class="deck">A carefully explained path from concrete examples to mathematics, algorithms and independent reasoning.</p>'
  elif kind=='lab':main+='<p class="deck">Predict, experiment, run code and defend your conclusion.</p>'
  main+=fragment
  main+='<nav class="week-bottom-links" aria-label="Other learning activities">'
  for key,label in (*LABELS.items(),('quiz','Quiz')):
   main+=f'<a href="/w{week}/{key}/">{label}</a>'
  main+='</nav></main>'
  old=path.read_text(encoding='utf-8')
  new,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,old,count=1,flags=re.S)
  assert count==1,(week,kind)
  for css in ('course-interactive.css','week23.css','week47.css','learning-transfers.css'):
   tag=f'<link rel="stylesheet" href="/assets/{css}">'
   if tag not in new:new=new.replace('</head>',tag+'</head>',1)
  for js in ('week23-interactive.js','week47-interactive.js'):
   tag=f'<script defer src="/assets/{js}"></script>'
   if tag not in new:new=new.replace('</head>',tag+'</head>',1)
  path.write_text(new,encoding='utf-8')
  print('Updated',path.relative_to(ROOT),'bytes',len(main))
