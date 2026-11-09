#!/usr/bin/env python3
"""Refresh minimalist syllabus and bibliography pages from the curated source mapping."""
from pathlib import Path
from html import escape as E
import json
R=Path(__file__).resolve().parents[1]
W=sum((json.loads((R/"data"/f"weeks_{lo:02}_{hi:02}.json").read_text()) for lo,hi in [(1,5),(6,10),(11,15)]),[])
base=(R/"scripts/generate_curriculum.py").read_text()
names={int(p[0]):p[2] for row in base.split('DATA = """',1)[1].split('""".strip()',1)[0].strip().splitlines() if (p:=row.split("|"))}
bib=json.loads((R/"data/bibliography.json").read_text())
def a(url,title):
 return '<a href="'+E(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+E(title)+'</a>'
def head(title):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)} · Machine Learning Club</title><link rel="stylesheet" href="/assets/site.css"></head><body><header class="site"><a class="brand" href="/">Machine Learning Club</a><p class="site-subtitle">Seven Hills International School · 2026–2027</p><p><a href="/">← All weeks</a></p></header><main class="shell"><h1>{E(title)}</h1>'''
def end():
 return '</main><footer class="site">Machine Learning Club · Seven Hills International School</footer></body></html>\n'
groups=[
 ("Stage I — ML foundations",range(1,10),"Introduce algorithms using small paper-solvable examples, then investigate the same mechanisms in interactive applications and Python.",["RO","PY","EA","CB","IO"]),
 ("Stage II — AI engineering",range(10,13),"Combine components into applications, evaluate reliable outputs, introduce Git/GitHub, and document privacy, uncertainty and limitations.",["CP","UN","EAP","GH"]),
 ("Stage III — competition projects",range(13,16),"Translate a task specification into a reproducible baseline, controlled improvements, and a working technical demonstration.",["IO","ON","IO26","POL"])]
s=head("Syllabus alignment")
s+='<p>This is a club-level synthesis, not a claim that every algorithm below is compulsory in every cited national syllabus. Romania’s optional secondary-school Machine Learning curriculum provides the main local technical reference; international frameworks supply ethics, AI engineering and competition extension.</p>'
for title,ids,description,refs in groups:
 s+='<section><h2>'+E(title)+'</h2><p>'+E(description)+'</p><p class="reference">Core references: '+' · '.join(a(bib[x][1],bib[x][0]) for x in refs)+'</p><ol>'
 for n in ids:
  w=W[n-1]
  s+='<li>'+a(f'/w{n}/course/',f'Week {n}: {names[n]}')+' — '+E(w["sections"][0][0])+'; '+E(w["sections"][1][0])+'; '+E(w["sections"][2][0])+'</li>'
 s+='</ol></section>'
s+='<section><h2>About syllabus granularity</h2><p>The Romanian programme directly describes Python, supervised/unsupervised learning, KNN, K-Means and linear regression. ID3 entropy, convolution internals, multilayer neural networks and Git workflows are treated as additional enrichment drawn from specialist learning resources and the IOAI syllabus.</p></section>'+end()
(R/"syllabus/index.html").write_text(s)
resource_groups=[
 ("Official curricula and competency frameworks",["RO","SG","UN","UA","IO"]),
 ("School textbooks, teacher guidance and practice",["PY","EA","EAP","CB","CP","POL"]),
 ("Interactive algorithm explanations and teaching webapps",["R2","TREE","KN","KM","OLS","KERNEL","TF","CD","TX","MI"]),
 ("Competitions, assessment tasks and software collaboration",["ON","ON26","IO25","IO26","KG","GH"])
]
s=head("Bibliography and teaching resources")
s+='<p>Curated sources used across the 15-week club. Individual Course, Laboratory, Homework and Advanced pages cite the sources most relevant to their own content. Links to third-party notebooks may require accounts or contain advanced material in Polish.</p>'
for title,keys in resource_groups:
 s+='<section><h2>'+E(title)+'</h2><ul>'
 for key in keys:
  if key in bib:
   s+='<li>'+a(bib[key][1],bib[key][0])+'</li>'
 s+='</ul></section>'
s+='<p class="note">Additional teacher materials, downloadable workbooks and the original national programmes remain owned by their respective publishers. Cite and adapt according to the relevant licence.</p>'+end()
(R/"resources/index.html").write_text(s)
print("Created syllabus crosswalk and referenced teaching bibliography.")
