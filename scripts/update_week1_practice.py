#!/usr/bin/env python3
"""Refresh authored Week 1 laboratory, probability homework and advanced exercises.

Preserves the existing mandatory homework assignment, full advanced exercises,
and global site navigation, while replacing only the reviewed teaching content.
"""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]

def insert_assets(page, styles=(), scripts=()):
    additions=[]
    for style in styles:
        asset=f'<link rel="stylesheet" href="/assets/{style}">'
        if asset not in page:additions.append(asset)
    for script in scripts:
        asset=f'<script defer src="/assets/{script}"></script>'
        if asset not in page:additions.append(asset)
    if additions:
        page=page.replace('</head>',''.join(additions)+'</head>',1)
    return page

def replace_main(page,contents,css_class):
    opening='<main class="lesson-content week1-foundations '+css_class+'">'
    output,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda m:opening+contents+'</main>',page,count=1,flags=re.S)
    assert count==1
    return output

lab=root/'w1/lab/index.html'
html=lab.read_text()
fragment=(root/'data/week1_lab_active.html').read_text()
html=replace_main(html,fragment,'lab-lesson')
html=insert_assets(html,
  styles=('course-interactive.css','week1-foundations.css','week1-lab-experiments.css','learning-transfers.css'),
  scripts=('week1-lab-experiments.js',))
html=html.replace('AI Tools — Exploration Laboratory','AI Experiments — Laboratory')
html=html.replace('Explore several real AI systems, compare what they do, and record where they succeed or fail. No coding required.',
  'Explore public AI experiments and run prepared, account-free Python notebooks.')
lab.write_text(html)

home=root/'w1/homework/index.html'
html=home.read_text()
mandatory=re.search(r'<section><h2>Mandatory .*?</section>',html,flags=re.S)
if mandatory is None:raise AssertionError('Missing original eight-scenario mandatory homework section')
fragment=(root/'data/week1_probability_homework.html').read_text()
contents=('<p class="eyebrow">Week 01 · Homework</p>'
  '<h1>Choose the Method &amp; Probability Practice</h1>'
  '<p class="deck">Recognise the right computational approach and practise probability using clear formulas.</p>'
  +mandatory.group(0)+fragment)
html=replace_main(html,contents,'homework-probability')
html=insert_assets(html,styles=('week1-foundations.css','week1-probability.css','learning-transfers.css'),
                   scripts=('week1-probability.js',))
home.write_text(html)

advanced=root/'w1/advanced/index.html'
html=advanced.read_text()
match=re.search(r'<main\b[^>]*>(.*?)</main>',html,flags=re.S)
if match is None:raise AssertionError('Missing advanced main')
body=match.group(1)
marker='<section><h2>Connection to machine learning</h2>'
i=body.find(marker)
if i<0:raise AssertionError('Missing original advanced connection heading')
body=body[:i].split('<section id="weighted-probabilities">')[0]+(root/'data/week1_advanced_additions.html').read_text()+body[i:]
html=replace_main(html,body,'advanced-probability')
html=insert_assets(html,styles=('week1-foundations.css','week1-probability.css'),
                   scripts=('week1-probability.js',))
advanced.write_text(html)
print('Updated Week 1 lab, homework and advanced without removing mandatory tasks or prior advanced exercises.')
