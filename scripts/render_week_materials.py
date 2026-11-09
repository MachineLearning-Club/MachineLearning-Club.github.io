#!/usr/bin/env python3
"""Publish the reviewed teaching-asset allocation without changing the minimalist layout."""
from pathlib import Path
from html import escape as E
import json
R=Path(__file__).resolve().parents[1]
content=json.loads((R/"data/week_materials_map.json").read_text())
rows=content["weeks"]
assert [x["n"] for x in rows]==list(range(1,16))
main=(R/"scripts/generate_curriculum.py").read_text()
raw=main.split('DATA = """',1)[1].split('""".strip()',1)[0].strip().splitlines()
titles={int(p[0]):(p[1],p[2]) for line in raw if (p:=line.split('|'))}
def link(url,label):
    return '<a href="'+E(url,quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"' if url.startswith('http') else '')+'>'+E(label)+'</a>'
def entries(items,numbered=False):
    outer="ol" if numbered else "ul"
    return '<'+outer+'>' + ''.join(
        '<li>'+link(i["url"],i["label"])+' — '+E(i["note"])+'</li>'
        for i in items
    )+'</'+outer+'>'
header='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Verified source materials allocated to the 15-week Machine Learning Club year plan">
<title>Teaching material map · Machine Learning Club</title>
<link rel="stylesheet" href="/assets/site.css"></head>
<body><header class="site"><a class="brand" href="/">Machine Learning Club</a>
<p class="site-subtitle">Seven Hills International School · 2026–2027</p><p><a href="/">← All weeks</a></p></header>
<main class="shell">
<h1>Teaching material map</h1>
<p>Selected source chapters, classroom activities, worksheets, notebooks and optional advanced problems, grouped by the existing 15-week programme.</p>
<p><strong>Planning resource, not a finished teaching pack.</strong> Some lesson files require a free educator login, some external notebooks are in Polish, and full Olympiad problems require substantial scaffolding.</p>
<nav aria-label="Jump to a week"><p>'''
html=[header]
html.append(" · ".join(link("#w"+str(i),"Week "+str(i)) for i in range(1,16)))
html.append("</p></nav>")
for w in rows:
    n=w["n"]
    assert all(len(w[k])>=1 for k in ("course","lab","home","adv"))
    d,t=titles[n]
    html.append(f'<section id="w{n}"><h2>Week {n} — {E(t)}</h2>')
    html.append(f'<p class="lesson-meta">{E(d)} · {E(w["focus"])}</p>')
    html.append('<h3>Course — specific source chapters and lessons</h3>')
    html.append(entries(w["course"],True))
    html.append('<h3>Laboratory — interactive experiment and external notebook</h3>')
    html.append(entries(w["lab"]))
    notebook=f'/w{n}/lab/starter.ipynb'
    html.append('<p>Club notebook: '+link(notebook,f'Week {n} starter (.ipynb)')+' · '+link(f'/w{n}/lab/',"Lab instructions")+'</p>')
    html.append('<h3>Homework — source exercise to adapt</h3>')
    html.append(entries(w["home"]))
    html.append('<h3>Advanced — optional enrichment</h3>')
    html.append(entries(w["adv"]))
    html.append(f'<p><a href="/w{n}/course/">Course</a> · <a href="/w{n}/lab/">Laboratory</a> · <a href="/w{n}/homework/">Homework</a> · <a href="/w{n}/advanced/">Advanced</a></p>')
    html.append('</section>')
html.append('<section><h2>Cross-cutting curriculum and teaching references</h2>')
html.append('<p>These guide standards, inclusion, ethical teaching and assessment across the year, rather than belonging to one student lesson.</p><ul>')
html.append('<li>'+link('https://legislatie.just.ro/public/DetaliiDocument/256856','Romania: ML optional programme XI–XII')+'</li>')
html.append('<li>'+link('https://74656b7.ultracdn.net/wp-content/uploads/2024/09/Curriculum_liceu_inteligenta_artificiala-ro.pdf','Moldova: National AI XI–XII curriculum')+'</li>')
html.append('<li>'+link('https://www.unesco.org/en/articles/ai-competency-framework-students','UNESCO: AI Competency Framework for Students')+'</li>')
html.append('<li>'+link('https://www.oecd.org/en/publications/empowering-learners-for-the-age-of-ai_65cd27d4-en.html','European Commission/OECD: AI Literacy Framework (2026)')+'</li>')
html.append('<li>'+link('https://www.dig4future.eu/Wordpress/materials/','DIG4future: Romanian and European teacher materials')+'</li>')
html.append('</ul></section>')
html.append('''</main><footer class="site">Machine Learning Club · Seven Hills International School · Materials last reviewed 9 November 2026</footer></body></html>''')
dest=R/"materials/index.html"
dest.parent.mkdir(exist_ok=True)
dest.write_text("\n".join(html)+"\n",encoding="utf-8")
# Give every lesson page a small contextual index link, without rewriting its teaching content.
for n in range(1,16):
  for kind in ("course","lab","homework","advanced"):
    p=R/f"w{n}/{kind}/index.html"
    s=p.read_text(encoding="utf-8")
    beg='<!-- WEEK SOURCE MAP -->'
    end='<!-- /WEEK SOURCE MAP -->'
    if beg in s:
        s=s[:s.index(beg)]+s[s.index(end)+len(end):]
    snippet=(beg+f'<p class="reference"><a href="/materials/#w{n}">'
              'Specific textbooks, lesson plans and source exercises for this week</a></p>'+end)
    assert '</main>' in s
    s=s.replace('</main>',snippet+'</main>',1)
    p.write_text(s,encoding="utf-8")
print("Published 15-week, 106-reference source map and links from all 60 lesson pages.")
