#!/usr/bin/env python3
"""Publish reviewed pre-university Week 10–11 materials without changing site chrome."""
from pathlib import Path
from html import escape
import re
ROOT=Path(__file__).resolve().parents[1]
TITLES={10:'Generative AI: GPT, Data and Society',11:'Software Engineering Techniques'}
KINDS={'course':'Course','lab':'Laboratory','homework':'Homework','advanced':'Advanced'}
for week,title in TITLES.items():
 for kind,label in KINDS.items():
  path=ROOT/f'w{week}/{kind}/index.html'
  content=(ROOT/f'data/week1011/w{week}_{kind}.html').read_text(encoding='utf8')
  main='<main class="lesson-content week47-academic week1011-academic'+(' course-lesson' if kind=='course' else '')+'">'
  main+=f'<p class="eyebrow">Week {week:02} · {label}</p><h1>{escape(title)}</h1>'
  main+=content
  main+='<nav class="week-bottom-links" aria-label="Other learning activities">'
  for k,t in [*KINDS.items(),('quiz','Quiz')]:
   main+=f'<a href="/w{week}/{k}/">{t}</a>'
  main+='</nav></main>'
  old=path.read_text(encoding='utf8')
  new,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,old,count=1,flags=re.S)
  assert count==1,(path,'main not found')
  for css in ('course-interactive.css','week47.css','week1011.css'):
   tag=f'<link rel="stylesheet" href="/assets/{css}">'
   if tag not in new:new=new.replace('</head>',tag+'</head>',1)
  for js in ('week1011.js',):
   tag=f'<script defer src="/assets/{js}"></script>'
   if tag not in new:new=new.replace('</head>',tag+'</head>',1)
  path.write_text(new,encoding='utf8')
  print('Updated',path.relative_to(ROOT))
