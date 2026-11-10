#!/usr/bin/env python3
"""Render sourced outlines for all 15 weeks, retaining the original site's minimal design."""
from pathlib import Path
from html import escape as E
import json
root=Path(__file__).resolve().parents[1]
sources=json.loads((root/"data/bibliography.json").read_text())
raw=[]
for block in ("weeks_01_05.json","weeks_06_10.json","weeks_11_15.json"):
    raw+=json.loads((root/"data"/block).read_text())
assert [w["n"] for w in raw]==list(range(1,16))
# Base programme is the source of truth for public week titles and dates.
base=(root/"scripts/generate_curriculum.py").read_text(encoding="utf-8")
rows=base.split('DATA = """',1)[1].split('""".strip()',1)[0].strip().splitlines()
for line in rows:
    fields=line.split("|")
    n=int(fields[0]); raw[n-1]["title"]=fields[2]; raw[n-1]["date"]=fields[1]

labels={"course":"Course","lab":"Laboratory","homework":"Homework","advanced":"Advanced"}
phase={1:"ML foundations",10:"AI systems engineering",13:"Competition projects"}
def link(url,title):
    return '<a href="'+E(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+E(title)+'</a>'
def bib(refs):
    missing=[x for x in refs if x not in sources]
    if missing:raise ValueError(missing)
    return '<p class="reference"><span class="reference-label">References: </span>'+ ' · '.join(link(sources[r][1],sources[r][0]) for r in refs)+'</p>'
def bullets(items,tag="ul"):
    if isinstance(items,str):
        items=[part.strip() for part in items.split(';') if part.strip()]
    return '<'+tag+'>' + ''.join('<li>'+E(x)+'</li>' for x in items) + '</'+tag+'>'
def nav(n,current):
    return '<nav class="lesson-nav" aria-label="Week '+str(n)+' materials">' + ''.join('<a href="/w'+str(n)+'/'+k+'/"'+(' aria-current="page"' if k==current else '')+'>'+v+'</a>' for k,v in labels.items()) + '</nav>'
def head(w,k):
    n=w["n"]
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Syllabus-aligned {labels[k].lower()} outline for ML Club Week {n}.">
  <title>Week {n} — {labels[k]} · Machine Learning Club</title>
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <header class="site">
    <a class="brand" href="/">Machine Learning Club</a>
    <p class="site-subtitle">Seven Hills International School · 2026–2027</p>
    <p><a href="/">← All weeks</a></p>
  </header>
  <main class="shell">
    <p class="lesson-meta">Week {n} · {labels[k]}</p>
    <h1>{E(w["title"])}</h1>
    {nav(n,k)}
'''
def tail(w,k):
    n=w["n"]
    quiz_link = f'<p class="weekly-quiz"><a href="/quiz/?week={n}">Week {n} quiz</a> · 10 questions (if prepared)</p>' if n>=2 else ''
    return f'''  {quiz_link}
  <nav class="lesson-pagination" aria-label="Previous and next lessons">
    {('<a href="/w'+str(n-1)+'/'+k+'/">← Week '+str(n-1)+'</a>') if n>1 else ""}
    {('<a href="/w'+str(n+1)+'/'+k+'/">Week '+str(n+1)+' →</a>') if n<15 else ""}
  </nav>
  </main>
  <footer class="site">Machine Learning Club · Seven Hills International School</footer>
</body>
</html>
'''
def page(w,k):
    n=w["n"];s=head(w,k)
    if k=="course":
        s+='<p class="intro">A structured lecture outline based on existing school and Olympiad courses. Algorithmic enrichment is identified by its own references, not attributed to every national syllabus.</p>'
        for i,(title,items,refs) in enumerate(w["sections"],1):
            s+=f'<section><h2>{i}. {E(title)}</h2>'+bullets(items)+bib(refs)+'</section>\n'
        refs=[]
        for _,_,rs in w["sections"]:
            refs.extend([r for r in rs if r not in refs])
        s+='<section><h2>Source and syllabus alignment</h2><p>Primary curriculum anchors, textbook chapters and specialist enrichment references:</p>'+bib(refs)+'</section>'
    elif k=="lab":
        s+='<p class="intro">Every practical meeting includes an interactive webapp and a runnable Colab starter notebook. The external notebook is a source reference, not a required prerequisite.</p>'
        s+='<section><h2>1. Interactive webapp</h2><p>'+link(w["app"][1],w["app"][0])+'</p><p>'+E(w["app"][2])+'</p></section>'
        s+='<section><h2>2. Colab laboratory</h2>'
        s+='<p>'+link('https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/w'+str(n)+'/lab/starter.ipynb','Open Week '+str(n)+' starter notebook in Colab')+' · '+link('/w'+str(n)+'/lab/starter.ipynb','Download notebook (.ipynb)')+'</p>'
        s+=bullets(w["lab"],"ol")
        s+='<p class="note">A working starter notebook is supplied; students should modify the code and explain the result, not merely execute it.</p></section>'
        s+='<section><h2>3. Existing notebook to study</h2><p>'+link(w["external"][1],w["external"][0])+'</p><p>Additional reading. Open separately; third-party notebooks may be longer, in Polish or designed for more advanced students.</p></section>'
        s+='<section><h2>Sources</h2>'+bib(w["labRefs"])+'</section>'
    elif k=="homework":
        s+='<p class="intro">Required transfer task: reuse the laboratory notebook on a new input, dataset or test case, then explain your result.</p>'
        s+='<section><h2>Assignment</h2><p>'+E(w["hw"])+'</p></section>'
        s+='<section><h2>Starting materials</h2><p>'+link('https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/w'+str(n)+'/lab/starter.ipynb','Week '+str(n)+' laboratory Colab')+' · '+link('/w'+str(n)+'/lab/starter.ipynb','Notebook file')+'</p></section>'
        s+='<section><h2>Expected submission</h2>'+bullets(['Modified notebook (or GitHub repository from Week 10 onward)','Small table, figure or worked calculation showing the result','Your own explanation of an error, assumption or limitation'])+'</section>'
        s+='<section><h2>Sources</h2>'+bib(w["hwRefs"])+'</section>'
    else:
        s+='<p class="intro">Optional further exploration, intended for students who finish the required work or want competition-level practice.</p>'
        s+='<section><h2>Challenge</h2><p>'+E(w["adv"])+'</p></section>'
        s+='<section><h2>External tasks and training</h2><p>'+link('https://github.com/IOAI-official/IOAI-2026','IOAI 2026 official competition archive')+' · '+link('https://github.com/OlimpiadaAI/szkolenia','Polish AI Olympiad training notebooks')+'</p><p class="note">Olympiad originals are usually substantially harder than the club tasks. Choose a suitable subsection or use the supplied starter code.</p></section>'
        s+='<section><h2>Sources</h2>'+bib(w["advRefs"])+'</section>'
    s+=tail(w,k)
    return '\n'.join(line.rstrip() for line in s.splitlines()) + '\n'
for w in raw:
    for k in labels:
        f=root/f'w{w["n"]}/{k}/index.html'
        # Week 1 includes a long, working interactive course/lab with their own styles.
        # Keep them intact: add a source-rich outline before the existing content in a separate guide.
        if w["n"]==1 and k in ("course","lab"):
            continue
        f.write_text(page(w,k),encoding="utf-8")
# For Week 1 legacy course and lab, append compact source-backed references and links without replacing the interactive content.
for k in ("course","lab"):
    w=raw[0];f=root/f'w1/{k}/index.html';s=f.read_text()
    start='<!-- SOURCED OUTLINE START -->';end='<!-- SOURCED OUTLINE END -->'
    if start in s:
        s=s[:s.index(start)]+s[s.index(end)+len(end):]
    if k=="course":
        addition='<section class="section" aria-labelledby="course-bibliography-title"><div class="section-heading"><div><h2 id="course-bibliography-title">Curriculum topics and sources</h2></div></div>'
        for i,(t,items,refs) in enumerate(w["sections"],1):
            addition+='<h3>'+str(i)+'. '+E(t)+'</h3>'+bullets(items)+bib(refs)
        addition+='</section>'
    else:
        addition='<section class="section" aria-labelledby="week1-guided-lab"><div class="section-heading"><div><h2 id="week1-guided-lab">Colab laboratory and references</h2></div></div>'
        addition+='<p>'+link('https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/w1/lab/starter.ipynb','Week 1 starter notebook (Colab)')+'</p>'
        addition+=bullets(w["lab"],"ol")
        addition+='<p>'+link(w["external"][1],w["external"][0])+'</p>'+bib(w["labRefs"])+'</section>'
    s=s.replace('<footer class="page-footer">',start+addition+end+'<footer class="page-footer">',1)
    f.write_text(s)
# Make clear that the bibliography labels are plain inline links, no new visual styles.
css=root/'assets/site.css'
s=css.read_text()
s+='\n.reference{font-size:.89rem;color:#666;line-height:1.5;margin:8px 0 20px}.reference-label{color:#666}.intro{margin:12px 0 25px}.note{color:#666;font-size:.9rem}\n'
css.write_text(s)
css=root/'w1/classic.css'
s=css.read_text()+'\n.reference{font-size:.89rem;color:#666;line-height:1.5;margin:8px 0 20px}.reference-label{color:#666}\n'
css.write_text(s)
print("Rendered sourced curriculum for",len(raw),"weeks")
