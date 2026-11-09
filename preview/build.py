#!/usr/bin/env python3
"""Independent two-week proof of concept. Does not modify the production lessons.

Run from repository root: python3 preview/build.py
"""
from pathlib import Path
from html import escape as e
import json, runpy

ROOT=Path(__file__).resolve().parent
WEEKS={1:"What Is AI? Learning from examples",3:"Decision Trees and Information Gain (ID3)"}
TYPES=[("course","Course"),("lab","Laboratory"),("homework","Homework"),("advanced","Advanced")]

def href(url,title):
    return f'<a href="{e(url,quote=True)}">{e(title)}</a>'

def nav(week,selected):
    items=[]
    for k,title in TYPES:
        current=' aria-current="page"' if k==selected else ''
        items.append(f'<a href="/preview/w{week}/{k}/"{current}>{title}</a>')
    return '<nav class="lesson-tabs" aria-label="Week '+str(week)+' materials"> ' + ' '.join(items) + '</nav>'

def page(week,kind,title,dek,content,description=None):
    assert week in WEEKS and kind in dict(TYPES)
    label=dict(TYPES)[kind]
    h=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(description or dek,quote=True)}">
<title>Week {week}: {label} · Machine Learning Club</title>
<link rel="stylesheet" href="/preview/assets/poc.css">
</head>
<body>
<header class="site"><a class="site-name" href="/">Machine Learning Club</a>
<p class="site-sub">Seven Hills International School · 2026–2027</p>
<p class="breadcrumb">{href('/preview/','Two-week preview')} / Week {week} / {label}</p>
</header>
<main id="main">
<p class="eyebrow">Week {week:02} · {label}</p>
<h1>{e(title)}</h1>
<p class="deck">{e(dek)}</p>
{nav(week,kind)}
{content}
</main>
<footer class="site">Machine Learning Club · A teaching-material proof of concept, not the final weekly programme · {href('/preview/','Preview index')}</footer>
</body></html>
'''
    dest=ROOT/f'w{week}/{kind}/index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(h,encoding='utf-8')
    print(dest.relative_to(ROOT))

def source(url,title,context=""):
    return '<p class="source-line">Reference: '+href(url,title) + (' · '+context if context else '') + '</p>'

def preview_index():
    blocks='''<p class="eyebrow">Teaching material design · November 2026</p>
<h1>Two-week preview</h1>
<p>Two deliberately different teaching cases: Week 1 introduces what a model does through short experiments; Week 3 develops an algorithm on paper before running and modifying it in Python.</p>
<p>These preview pages do not replace the currently published weekly lessons.</p>'''
    for week,title,desc in [
        (1,WEEKS[1],"Accessible introduction · Google AI experiments · simple classification · data limitations"),
        (3,WEEKS[3],"Worked categorical ID3 algorithm · entropy/gain · interactive root selection · reasoning exercises")]:
        blocks+=f'<section><h2>Week {week} — {e(title)}</h2><p class="understated">{e(desc)}</p>'
        blocks+=nav(week,"")
        blocks+='</section>'
    blocks+='''<section><h2>The four recurring formats</h2><ol>
<li><strong>Course:</strong> self-contained electronic textbook; numbered sections, definitions, worked code examples, diagrams and bibliography alongside the topic.</li>
<li><strong>Laboratory:</strong> external interactive experience first, then guided Colab, experimentation and short reflection. Notebook code is previewed directly on the page.</li>
<li><strong>Homework:</strong> brief UAIC-style specification: Context, Mandatory (1p), Homework (2p), Submission. Each activity extends the lab project.</li>
<li><strong>Advanced:</strong> printable research-style problem collection, progressive algorithmic reasoning, worked examples and counterexamples. Python is optional, with no verification tools required.</li></ol></section>'''
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Two-week preview · Machine Learning Club</title>
<link rel="stylesheet" href="/preview/assets/poc.css"></head><body>
<header class="site"><a class="site-name" href="/">Machine Learning Club</a><p class="site-sub">Seven Hills International School · 2026–2027</p><p class="breadcrumb">{href('/','Main site')} / Preview</p></header>
<main>{blocks}</main><footer class="site">Machine Learning Club · Preview of two lesson formats</footer></body></html>'''
    (ROOT/'index.html').write_text(html,encoding='utf-8')

def code_preview(week,file="starter.ipynb"):
    path=ROOT/f'w{week}/lab/{file}'
    nb=json.loads(path.read_text(encoding='utf-8'))
    codes=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code']
    code=codes[0] if codes else ''
    # first code cell only, after student's concept explanation
    return '<details class="notebook-preview"><summary>Preview a real executable cell from the notebook</summary><pre><code>'+e(code)+'</code></pre></details>'

def make():
    preview_index()
    runpy.run_path(str(ROOT/'week1.py'),init_globals={'page':page,'href':href,'source':source,'code_preview':code_preview,'e':e})
    runpy.run_path(str(ROOT/'week3.py'),init_globals={'page':page,'href':href,'source':source,'code_preview':code_preview,'e':e})
    print("Built 2 × 4 preview pages.")
if __name__=="__main__":make()
