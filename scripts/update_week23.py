#!/usr/bin/env python3
"""Publish authored Weeks 2–3 without changing the shared navigation or other weeks."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
for week,title in [
 (2,'Supervised Learning: ID3'),
 (3,'Unsupervised Learning: K-Means')
]:
 for kind in ('course','lab','homework','advanced'):
  file=root/f'w{week}/{kind}/index.html'
  page=file.read_text(encoding='utf-8')
  source=root/f'data/week23/w{week}_{kind}.html'
  fragment=source.read_text(encoding='utf-8')
  default_end='<nav class="week-bottom-links" aria-label="Other learning activities">'+''.join(
   '<a href="/w'+str(week)+'/'+key+'/">'+name+'</a>' for key,name in [
    ('course','Course'),('lab','Laboratory'),('homework','Homework'),
    ('advanced','Advanced'),('quiz','Quiz')])+ '</nav>'
  main='<main class="lesson-content week23-academic'+(' course-lesson' if kind=='course' else '')+'">'
  main+='<p class="eyebrow">Week '+f'{week:02}'+' · '+dict(course='Course',lab='Laboratory',homework='Homework',advanced='Advanced')[kind]+'</p>'
  main+='<h1>'+title+'</h1>'
  if kind=='course':
   main+='<p class="deck">The algorithm built from a real problem, one decision at a time.</p>'
  elif kind=='lab':
   main+='<p class="deck">Predict, interact, run Python and explain the result.</p>'
  main+=fragment+default_end+'</main>'
  page,num=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,page,count=1,flags=re.S)
  assert num==1,(week,kind)
  for css in ('course-interactive.css','week23.css','learning-transfers.css'):
   tag='<link rel="stylesheet" href="/assets/'+css+'">'
   if tag not in page:page=page.replace('</head>',tag+'</head>',1)
  tag='<script defer src="/assets/week23-interactive.js"></script>'
  if tag not in page:page=page.replace('</head>',tag+'</head>',1)
  file.write_text(page,encoding='utf-8')
  print('Updated',file.relative_to(root),len(main),'characters')
