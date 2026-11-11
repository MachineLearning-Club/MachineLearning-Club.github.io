#!/usr/bin/env python3
"""The single source of publication for ML Club's reviewed 3 + 6 + 6 curriculum.

Public site: static, accessibility-minded HTML/CSS. Never implies a backend
upload, secure quiz authentication, or confirmed school times.
"""
from pathlib import Path
from html import escape as E
import json, re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
W = []
for filename in ("outline_v3_01_05.json","outline_v3_06_10.json","outline_v3_11_15.json"):
    W += json.loads((ROOT/"data"/filename).read_text())
assert len(W)==15 and [w["n"] for w in W]==list(range(1,16))
for w in W:
    w["sections"]=[({"title":sec[0],"problem":sec[1],"concept":sec[2],"example":sec[3],"steps":sec[4],"code":sec[5]} if isinstance(sec,list) else sec) for sec in w["sections"]]

KINDS=[("course","Course"),("lab","Laboratory"),("homework","Homework"),("advanced","Advanced"),("quiz","Quiz")]
MODULES=[
    ("I","Foundations of Artificial Intelligence",1,3),
    ("II","Machine Learning and Neural Networks",4,9),
    ("III","Generative AI and Software Engineering",10,15)
]
REGISTRY=json.loads((ROOT/"data/bibliography.json").read_text())
REGISTRY.update({
 "MSAI":["Microsoft AI for Beginners — selected lessons","https://github.com/microsoft/AI-For-Beginners"],
 "MSML":["Microsoft ML for Beginners — selected lessons","https://github.com/microsoft/ML-For-Beginners"],
 "OECD":["European Commission / OECD AI Literacy Framework","https://www.oecd.org/en/publications/empowering-learners-for-the-age-of-ai_65cd27d4-en.html"],
 "JUP":["JupyterLite — browser-only notebooks","https://jupyterlite.github.io/demo/lab/"],
 "TM":["Google Teachable Machine","https://teachablemachine.withgoogle.com/"],
 "EA":["Experience AI — school activities and worksheets","https://experience-ai.org/ro/units/foundations-of-ai-11-14"],
 "ON":["Romanian AI Olympiad — training resources","https://www.olimpiada-ai.ro/ro/resurse"],
 "SG":["Singapore G3 Computing syllabus","https://isomer-user-content.by.gov.sg/334/4320fbe7-b9d7-4024-ab0b-b2d42a9cd8c9/K349_y27_sy.pdf"]
})
assert all(s in REGISTRY for w in W for s in w["sources"])
PFA="BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ"
SCHOOL_LINK="https://sevenhills.ro/"
SCHOOLS=json.loads((ROOT/"data/schools.json").read_text())["partners"]
assert len(SCHOOLS)>=1
OWNER_LINK="https://github.com/dbxdrgsl"
ORG_LINK="https://github.com/MachineLearning-Club"

def a(url,title):
    extra=' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
    return '<a href="'+E(url,quote=True)+'"'+extra+'>'+E(title)+'</a>'

def page_start(title,styles="/assets/academic.css",extra=""):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<meta name="description" content="'+E(title,quote=True)+'">'
      '<title>'+E(title)+' · Machine Learning Club</title>'
      '<link rel="stylesheet" href="'+styles+'"><link rel="stylesheet" href="/assets/v3.css">'+extra+'</head><body>')

def footer():
    return ('<footer class="site"><span>Independent educational project operated by '
      +a(OWNER_LINK,PFA)+'</span> · '+a(ORG_LINK,"GitHub organisation")+'</footer>')

def tabs(n,current=None):
    return '<nav class="lesson-tabs" aria-label="Week '+str(n)+' materials">'+''.join(
       '<a href="/w'+str(n)+'/'+key+'/"'+(' aria-current="page"' if current==key else '')+'>'+label+'</a>'
       for key,label in KINDS
    )+'</nav>'

def toolbar(n,kind):
    choices=''.join('<option value="'+str(i)+'"'+(' selected' if i==n else '')+'>Week '+str(i).zfill(2)+' — '+E(w["title"])+'</option>' for i,w in enumerate(W,1))
    prev=a(f'/w{n-1}/{kind}/',f'← Week {n-1}') if n>1 else a('/','← All weeks')
    next_=a(f'/w{n+1}/{kind}/',f'Week {n+1} →') if n<15 else a('/','All weeks →')
    return ('<header class="lesson-header">'
      '<div class="lesson-topbar">'+a('/','Machine Learning Club')+
      '<label class="week-picker">Go to week <select data-week-picker data-kind="'+E(kind)+'" aria-label="Select a week">'+choices+'</select></label>'
      '<nav class="week-arrows" aria-label="Week navigation">'+prev+' <span>·</span> '+next_+'</nav></div>'
      +tabs(n,kind)+'</header>')

def week_start(w,kind):
    n=w["n"]; kind_label=dict(KINDS)[kind]
    return (page_start(w["title"]+" — "+kind_label,extra='<script defer src="/assets/academic-ui.js"></script>')
       +toolbar(n,kind)
       +'<main class="lesson-content"><p class="eyebrow">Week '+str(n).zfill(2)+' · '+kind_label+'</p>'
       +'<h1>'+E(w["title"])+'</h1>'
       +'<p class="deck">'+E(w["subtitle"])+'</p>')

def week_end(w):
    n=w["n"]
    return ('<nav class="week-bottom-links" aria-label="Other learning activities">'
       +''.join(a('/w'+str(n)+'/'+k+'/',label) for k,label in KINDS)+'</nav>'
       +'</main>'+footer()+'</body></html>')

def bibliography(w,short=False):
    sources=w["sources"][:3] if short else w["sources"]
    links=[]
    for sid in sources:
        title,url=REGISTRY[sid][:2]
        typ=('Teacher/advanced reference' if sid in ("IO","POL","IO25","IO26","ON") else "Student / teacher reference")
        links.append('<li>'+a(url,title)+' <span class="reference-note">— '+typ+'</span></li>')
    return '<section class="page-bibliography"><h2>Bibliography</h2><ul>'+''.join(links)+'</ul></section>'

def one_source(w,index=0):
    sid=w["sources"][index%len(w["sources"])]
    name,url=REGISTRY[sid][:2]
    return '<p class="source-line">Read alongside this topic: '+a(url,name)+'.</p>'

def list_html(items,ordered=True):
    tag='ol' if ordered else 'ul'
    return '<'+tag+'>'+''.join('<li>'+E(v)+'</li>' for v in items)+'</'+tag+'>'

def diagram(w):
    kind=w["diagram"]
    n=w["n"]
    if kind in ("scatter","clusters"):
        pts = [(1.0,1.2,0),(2.0,1.6,0),(1.5,2.8,0),(7.0,7.0,1),(8.2,7.6,1),(7.5,8.6,1)]
        circles = []
        for x,y,g in pts:
            circles.append(f'<circle cx="{50+int(x*60)}" cy="{320-int(y*30)}" r="9" fill="{("#587ea8" if g==0 else "#b98463")}" opacity=".85"/>')
        more=('<circle cx="139" cy="270" r="13" stroke="#174a7e" fill="none" stroke-width="2"/>'
              '<circle cx="506" cy="88" r="13" stroke="#995c33" fill="none" stroke-width="2"/>' if kind=="clusters" else '')
        art='<path d="M35 18V345H670" stroke="#777" stroke-width="1.5" fill="none"/>'+''.join(circles)+more
        note="Two invented groups of points; centroid positions shown by rings." if kind=="clusters" else "A two-dimensional scatterplot: proximity can help classify, but labels must be supplied for KNN."
        return '<figure class="teaching-figure"><svg viewBox="0 0 710 360" role="img" aria-label="'+E(note,quote=True)+'">'+art+'</svg><figcaption>'+E(note)+'</figcaption></figure>'
    if kind=="pixels":
        vals=[[0,0,0,30,220,255,255,255],[0,0,50,120,200,255,255,255],[0,30,150,210,235,255,250,255],
              [0,70,210,240,255,245,245,255],[0,80,215,240,255,230,240,255],[0,70,150,200,240,255,255,255],
              [0,30,90,180,235,255,255,255],[0,0,0,70,195,255,255,255]]
        rects=''.join('<rect x="'+str(130+j*48)+'" y="'+str(15+i*38)+'" width="46" height="36" fill="rgb('+str(v)+','+str(v)+','+str(v)+')" stroke="#bbb"/>' for i,row in enumerate(vals) for j,v in enumerate(row))
        return '<figure class="teaching-figure"><svg viewBox="0 0 650 340" role="img" aria-label="8 by 8 grayscale pixel matrix, each square representing one intensity value">'+rects+'</svg><figcaption>Pixels are numerical measurements arranged in a grid.</figcaption></figure>'
    if kind=="bars":
        values=[("Baseline",68),("Revised",78),("Target",85)]
        art=''.join(f'<text x="35" y="{55+i*77}" font-size="18">{E(name)}</text><rect x="190" y="{35+i*77}" width="{val*4}" height="27" fill="#6687a7"/><text x="{207+val*4}" y="{56+i*77}" font-size="16">{val}%</text>' for i,(name,val) in enumerate(values))
        return '<figure class="teaching-figure"><svg viewBox="0 0 690 270" role="img" aria-label="Illustrative comparison of baseline score 68%, revised score 78% and target score 85%">'+art+'</svg><figcaption>Illustrative scores only. Real claims must be supported by evaluation data.</figcaption></figure>'
    if kind=="tree":
        return ('<figure class="teaching-figure"><svg viewBox="0 0 680 240" role="img" aria-label="A simple decision tree: Sky? Rainy leads to No, Sunny leads to Wind?">'
         '<g stroke="#999" fill="none" stroke-width="2"><path d="M340 54L160 136M340 54L515 136M515 158L450 213M515 158L580 213"/></g>'
         '<g fill="#fff" stroke="#666"><rect x="288" y="16" width="104" height="42"/><rect x="116" y="134" width="88" height="42"/><rect x="465" y="133" width="100" height="44"/></g>'
         '<g font-size="17" fill="#333" text-anchor="middle"><text x="340" y="43">Sky?</text><text x="160" y="162">No</text><text x="515" y="161">Wind?</text><text x="450" y="235">Yes</text><text x="590" y="235">No</text></g>'
         '<g font-size="13" fill="#777"><text x="223" y="90">rainy</text><text x="430" y="90">sunny</text></g></svg><figcaption>A decision tree makes a sequence of simple tests.</figcaption></figure>')
    if kind in ("network","perceptron"):
        sources=[(80,80),(80,195)]
        dests=[(320,57),(320,140),(320,223)] if kind=="network" else [(350,140)]
        output=[(560,140)]
        arcs=''.join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#b9c6d3" stroke-width="2"/>' for x1,y1 in sources for x2,y2 in dests)
        if kind=="network":arcs+=''.join(f'<line x1="{x1}" y1="{y1}" x2="{output[0][0]}" y2="{output[0][1]}" stroke="#b9c6d3" stroke-width="2"/>' for x1,y1 in dests)
        nodes=''.join(f'<circle cx="{x}" cy="{y}" r="25" fill="#fff" stroke="#6889a5" stroke-width="2"/>' for x,y in sources+dests+(output if kind=="network" else []))
        words='<g fill="#333" text-anchor="middle" font-size="17"><text x="80" y="86">x₁</text><text x="80" y="200">x₂</text>'
        if kind=="network": words+='<text x="560" y="146">ŷ</text>'
        else:words+='<text x="350" y="145">ŷ</text>'
        words+='</g>'
        return '<figure class="teaching-figure"><svg viewBox="0 0 680 280" role="img" aria-label="Input features connected by weighted lines to computational neurons">'+arcs+nodes+words+'</svg><figcaption>Weights connect inputs to computations; the output depends on learned parameters.</figcaption></figure>'
    stages=(
      ["Training data","Learning model","Prediction"] if n==1 else
      ["Input","Processing","Output"] if n<11 else
      ["Data","Validation + model","Usable result"])
    rectangles=[]
    for i,label in enumerate(stages):
        x=5+i*233
        rectangles.append(f'<rect x="{x}" y="27" width="212" height="76" rx="3" stroke="#9aafc1" fill="#f8fbff"/>'
          f'<text x="{x+106}" y="71" font-size="18" text-anchor="middle" fill="#2b4c6b">{E(label)}</text>')
        if i<2:rectangles.append(f'<path d="M{x+214} 65h18m-7 -6 7 6 -7 6" fill="none" stroke="#7e8b95" stroke-width="1.5"/>')
    return '<figure class="teaching-figure"><svg viewBox="0 0 710 135" role="img" aria-label="Input, processing, output pipeline">'+''.join(rectangles)+'</svg><figcaption>Trace information from the input through an algorithm to its result.</figcaption></figure>'

def course_content(w):
    n=w["n"]
    if n in (1,2):
        body=(ROOT/"data/legacy_content"/f'w{n}_course.html').read_text()
        if n==2:
            for i in range(1,6):
                body=body.replace(f'{3}.{i}.',f'{2}.{i}.')
        # Preserve long-form authored examples and correct theoretical distinctions.
        body+=diagram(w)
    else:
        body='<section class="scenario"><h2>Start with a problem</h2><p>'+E(w["scenario"])+'</p><p>Try to predict what a useful program should do before looking at its code.</p></section>'
        body+='<nav class="toc" aria-label="Course contents"><strong>Contents</strong>'+list_html([s["title"] for s in w["sections"]])+'</nav>'
        for i,s in enumerate(w["sections"],1):
            body+='<section class="topic-section" id="part'+str(i)+'"><h2>'+str(i)+'. '+E(s["title"])+'</h2>'
            body+='<p><strong>Real-life question.</strong> '+E(s["problem"])+'</p>'
            body+='<p>'+E(s["concept"])+'</p>'
            body+='<div class="worked"><strong>Worked example.</strong><p>'+E(s["example"])+'</p></div>'
            if i==2 or (i==3 and len(w["sections"])>=4):body+=diagram(w)
            body+='<pre><code>'+E(s["code"])+'</code></pre>'
            body+='<details class="lesson-details"><summary>Show the process step by step</summary>'+list_html(s["steps"])+'<p><strong>Try this:</strong> change one input or value in the code, then predict the new output before running.</p></details>'
            body+=one_source(w,i-1)+'</section>'
        body+='<section><h2>Check your understanding</h2><p>Explain the input, the processing step and the expected output for the problem at the start of this lesson. Then identify one case where the model or rule may fail.</p>'
        body+=a(f'/w{n}/lab/','Continue to the laboratory')+'</section>'
    return body+bibliography(w)

def lab_content(w):
    n=w["n"]
    intro='<section class="scenario"><h2>Lab challenge</h2><p>'+E(w["lab"]["context"])+'</p></section>'
    if n in (1,2):
        body=intro+(ROOT/"data/legacy_content"/f'w{n}_lab.html').read_text()
        body=re.sub(r'<p class="understated">.*?(In-class route|proof of concept).*?</p>','',body,flags=re.S|re.I)
    else:
        app=w["app"]
        body=intro+'<section><h2>1. Open an interactive experiment</h2><p>'+a(app["url"],'Launch '+app["title"])+'</p><p>Observe the example first. Predict one change before adjusting any parameter.</p></section>'
        body+='<section><h2>2. Run the guided Python experiment</h2>'+list_html(w["lab"]["steps"])+'</section>'
    body+='<section class="browser-python-section"><h2>Account-free Python practice</h2><p>Edit the small code example below and press Run Python. The program runs inside your browser; no login is required. The Python engine is loaded only when requested and needs an internet connection.</p>'
    example=w["sections"][0]["code"]
    body+='<div class="python-runner"><label for="py-code-'+str(n)+'">Editable Python code</label><textarea id="py-code-'+str(n)+'" class="py-source" spellcheck="false" rows="'+str(max(5,len(example.splitlines())+1))+'">'+E(example)+'</textarea><button type="button" class="run-python">Run Python</button><output class="py-output" aria-live="polite">Run your code to see the output.</output></div>'
    body+='<p class="tool-links">'+a("https://jupyterlite.github.io/demo/lab/","Open JupyterLite (no account)")+' · '+a(f'/w{n}/lab/starter.ipynb','Download the club notebook (.ipynb)')+' · '+a('/guides/notebooks/','Notebook step-by-step guide')+'</p>'
    body+='<p class="understated">To use the full notebook in JupyterLite, upload the downloaded file using its file browser; the inline runner above is for short Python exercises.</p></section>'
    body+='<section><h2>Research (3p) <span class="optional-mark">(optional)</span></h2><p>'+E(w["lab"]["research"])+'</p><details><summary>How to approach this investigation</summary><ol><li>Start from the working lab code.</li><li>Change one thing and keep a record of the original result.</li><li>Explain what the new result shows and where it might be misleading.</li></ol></details></section>'
    body+=submission_widget(n)
    return body+bibliography(w)

def submission_widget(n):
    return ('<section id="submission" class="submission-drop"><h2>Submit your laboratory work</h2><p>Type your name, then drop or choose your <code>.ipynb</code>, <code>.py</code>, <code>.csv</code> or <code>.zip</code> file. You can prepare a clearly named file for the teacher.</p>'
      '<div class="submission-form" data-submission-week="'+str(n)+'"><label>Student name<input type="text" class="student-name" placeholder="First name, last name" maxlength="90" autocomplete="name"></label>'
      '<label class="file-drop">Drop a file here or choose one<input class="submission-files" type="file" accept=".ipynb,.py,.csv,.zip,.txt" multiple></label>'
      '<p class="submission-selected" aria-live="polite">No file selected.</p>'
      '<button type="button" class="prepare-submission">Download named submission</button>'
      '<p class="submission-status" aria-live="polite"></p></div>'
      '<p class="understated">Uploads are not enabled yet. This prepares files locally; it does not send them to the teacher. When a teacher-approved Dropbox File Request is configured, its collection link appears here. Until then, keep the ZIP locally.</p></section>')

def homework_content(w):
    n=w["n"]
    body='<section class="scenario"><h2>Real-life situation</h2><p>'+E(w["homework"]["context"])+'</p></section>'
    if n in (1,2):
        legacy=(ROOT/"data/legacy_content"/f'w{n}_homework.html').read_text()
        legacy=re.sub(r'<section><h2>Context</h2>.*?</section>','',legacy,flags=re.S)
        legacy=re.sub(r'<p class="assignment-meta">.*?</p>','',legacy,flags=re.S)
        body+=legacy
    else:
        body+='<section><h2>Mandatory <span class="point-value">(1p)</span></h2><p>'+E(w["homework"]["mandatory"])+'</p><details><summary>Suggested starting steps</summary><ol><li>Open the Week '+str(n)+' Laboratory and run the prepared code.</li><li>Identify the relevant input and output.</li><li>Change the smallest amount of code needed to solve the situation.</li></ol></details></section>'
        body+='<section><h2>Homework <span class="point-value">(2p)</span></h2><p>'+E(w["homework"]["homework"])+'</p></section>'
        body+='<section><h2>What to submit</h2><p>Use the laboratory submission area to prepare a named notebook or Python file. Add one screenshot, output table or short explanation of what changed.</p>'+a(f'/w{n}/lab/#submission','Go to the laboratory submission area')+'</section>'
    return body+bibliography(w)

def advanced_content(w):
    n=w["n"]
    if n in (1,2):
        body=(ROOT/"data/legacy_content"/f'w{n}_advanced.html').read_text()
    else:
        body='<section><h2>A closer look at the algorithm</h2><p>'+E(w["sections"][0]["concept"])+'</p>'+diagram(w)+'</section>'
        body+='<section><h2>Worked reasoning</h2><p>'+E(w["sections"][0]["example"])+'</p><details open><summary>One worked algorithmic trace</summary>'+list_html(w["sections"][0]["steps"])+'<p>'+E(w["sections"][1]["example"])+'</p></details></section>'
        for i,problem in enumerate(w["advanced"],1):
            body+='<section><h2>Problem '+str(i)+': '+E(problem)+'</h2>'
            body+='<p>Use the numerical or symbolic example from the Course. Write down the intermediate states before explaining the result.</p><details><summary>Hint</summary><p>'+E(w["sections"][min(i,len(w["sections"])-1)]["example"])+'</p></details></section>'
        body+='<p class="understated">These are optional paper-style reasoning exercises. A full printable booklet for this week will be developed after reviewing the classroom materials.</p>'
    return body+bibliography(w)

def render_quiz_placeholder(w):
    n=w["n"]
    return ('<section><h2>Weekly knowledge check</h2><p>Answer short questions about the concepts actually taught in Week '+str(n)+'. Quiz content is reviewed individually as the course is finalised.</p>'
       '<div id="weekly-quiz" data-week="'+str(n)+'" aria-live="polite"><p>Loading quiz…</p></div></section>'
       '<script defer src="/assets/weekly-quiz.js"></script>')

def make_week(w,kind):
    body=week_start(w,kind)
    if kind=="course":body+=course_content(w)
    elif kind=="lab":body+=lab_content(w)
    elif kind=="homework":body+=homework_content(w)
    elif kind=="advanced":body+=advanced_content(w)
    else:body+=render_quiz_placeholder(w)
    body+=week_end(w)
    path=ROOT/f'w{w["n"]}/{kind}/index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(body,encoding="utf-8")

def render_home():
    result=page_start("Machine Learning Club",extra='<script defer src="/assets/academic-ui.js"></script>')
    result+='<header class="homepage-header"><h1>Machine Learning Club</h1>'
    for partner in SCHOOLS:
        reg=partner.get("registration",{})
        result+='<div class="school-line"><span class="school-name">'+a(partner["website"],partner["name"])+          '</span><span class="year">'+E(partner["schoolYear"] )+'</span>'
        if reg.get("url"):
            result+='<span><strong>'+E(reg.get("label","Registration open"))+'.</strong> '+a(reg["url"],"Register here")+'</span>'
        if partner.get("timetable"):
            result+='<span>'+a(partner["timetable"],"Timetable")+'</span>'
        result+='</div>'
    result+='</header><main class="homepage-content">'
    for roman,name,first,last in MODULES:
        if first==4:
            result+='<section class="prerequisite"><h2>Before Module II — Running Python notebooks</h2><p>Learn what an <code>.ipynb</code> file is, how to upload it in JupyterLite, run cells in order, fix a small error and save your work.</p><p>'+a('/guides/notebooks/','Step-by-step notebook guide')+'</p></section>'
        if first==10:
            result+='<section class="prerequisite"><h2>Before Module III — Projects, Git and AI-assisted editing</h2><p>Begin with a guided Git version-history simulation; then explore managing a repository and using an AI code editor responsibly. Accounts are optional.</p><p>'+a('/guides/github-ai/','Beginner Git/GitHub and AI code editing guide')+'</p></section>'
        result+='<section class="module" id="module-'+roman.lower()+'"><h2>Module '+roman+' — '+E(name)+'</h2>'
        for n in range(first,last+1):
            w=W[n-1]
            result+='<article class="week"><h3>Week '+str(n)+' — '+E(w["title"])+'</h3>'+tabs(n)+'</article>'
        result+='</section>'
    result+='<section class="bibliography-entry"><h2>'+a('/resources/','Bibliography')+'</h2><p>Original syllabi, school textbooks, laboratories, problem collections and interactive tools.</p></section>'
    return result+'</main>'+footer()+'</body></html>'

def timetable():
    result=page_start("Seven Hills — ML Club timetable",extra='<script defer src="/assets/academic-ui.js"></script>')
    result+='<header class="timetable-head"><p>'+a('/','← Machine Learning Club')+'</p><h1>Timetable</h1><p>'+a(SCHOOL_LINK,"Seven Hills International School")+' · 2026–2027</p></header><main>'
    result+='<p class="understated">Session dates, time intervals, assigned groups and rooms will be announced by the school. This is an internal ML Club schedule, not an eOra system.</p>'
    result+='<div class="timetable-control"><label>School <select aria-label="School"><option selected>Seven Hills International School</option></select></label><label>Module <select id="timetable-module"><option value="all">All modules</option><option value="I">Module I</option><option value="II">Module II</option><option value="III">Module III</option></select></label></div>'
    result+='<div class="timetable-scroll"><table class="timetable-grid"><thead><tr><th>Week</th><th>Activity</th><th>Day / time</th><th>Group</th><th>Teacher</th><th>Room</th><th>Materials</th></tr></thead><tbody>'
    for w in W:
        n=w["n"]
        module="I" if n<=3 else "II" if n<=9 else "III"
        links=' · '.join(a(f'/w{n}/{kind}/',label) for kind,label in KINDS)
        result+='<tr data-module="'+module+'"><td><strong>'+str(n).zfill(2)+'</strong><div class="understated">Module '+module+'</div></td><td>'+E(w["title"])+'</td><td>To be announced</td><td><span class="unassigned">To be assigned</span></td><td>Dragoș-Andrei Bobu</td><td>To be announced</td><td>'+links+'</td></tr>'
    result+='</tbody></table></div><p class="understated">Future partner schools can be added as separate timetable views without altering lesson material links.</p></main>'+footer()+'</body></html>'
    return result

def guide_start(title,intro):
    return (page_start(title,extra='<script defer src="/assets/academic-ui.js"></script>')+
      '<header class="guide-head"><p>'+a('/','← Machine Learning Club')+'</p><h1>'+E(title)+'</h1><p>'+E(intro)+'</p></header><main class="guide">')

def render_guides():
    body=guide_start("How to use a Python notebook","A short, accountless start before Module II.")
    body+='<section><h2>1. What is a .ipynb file?</h2><p>It is a notebook containing text, executable code cells and saved outputs. Each cell is a small experiment, not a separate program you must install.</p><pre><code>temperature = 18\nprint(temperature + 2)</code></pre><p>Predict the result (20), then run the cell.</p></section>'
    body+='<section><h2>2. Open an account-free editor</h2><ol><li>'+a('https://jupyterlite.github.io/demo/lab/','Open JupyterLite')+' in a recent browser.</li><li>Wait for the notebook environment to load. No account is required.</li><li>Download the starter <code>.ipynb</code> from your week’s Laboratory page.</li><li>Upload or drag the notebook into the JupyterLite file browser, then open it.</li></ol><p>JupyterLite stores files in this browser; a different device will not automatically have them.</p></section>'
    body+='<section><h2>3. Run and change cells</h2><ol><li>Click the first code cell and press <kbd>Shift</kbd> + <kbd>Enter</kbd>.</li><li>Read its output before editing anything.</li><li>Change one number, run the cell again and compare.</li><li>If a cell uses a variable from an earlier cell, run the earlier cell first.</li></ol><details><summary>Why does it say NameError?</summary><p>The variable may not yet exist in this running kernel. Restart and run the cells from the top in order.</p></details></section>'
    body+='<section><h2>4. Save and submit</h2><ol><li>Use JupyterLite’s download option to save the changed notebook to your computer.</li><li>Check that the file still ends with <code>.ipynb</code>.</li><li>Use the submission area on the Laboratory page to prepare a named file.</li><li>Upload it only to the teacher-approved collection location once announced.</li></ol><p><strong>Optional:</strong> '+a('https://colab.research.google.com/','Google Colab')+' requires a Google account to execute; it is not the club default.</p></section>'
    body+='</main>'+footer()+'</body></html>'
    path=ROOT/'guides/notebooks/index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
    body=guide_start("Git, GitHub and AI-assisted code editing","An introductory version-control guide before Module III.")
    body+='<section><h2>1. Why keep versions?</h2><p>You fix a bug, but your next edit breaks the program. A version history lets you identify the change and return to a working state.</p><p>The smallest cycle is <strong>edit → inspect → test → save a version</strong>.</p></section>'
    body+='<section><h2>2. Try a miniature Git workflow</h2><div class="git-simulator"><p>Use the controls to modify a simulated project and record two commits. It is a learning activity, not a real Git repository.</p><textarea rows="4" class="git-code" spellcheck="false">def predict(x):\n    return x > 10</textarea><div><button type="button" data-git-test>Test</button> <button type="button" data-git-commit>Commit current version</button> <button type="button" data-git-undo>Restore last commit</button></div><output class="git-output" aria-live="polite">Working tree has uncommitted text.</output><ol class="git-history"></ol></div></section>'
    body+='<section><h2>3. The equivalent real Git commands</h2><pre><code>git status\ngit add main.py\ngit commit -m "Add missing-input check"\ngit log --oneline</code></pre><p>A repository tracks project files. A commit records a state. A branch is a separate line of changes. A pull request proposes merging reviewed work.</p><p>Using '+a('https://github.dev/','github.dev')+' or '+a('https://vscode.dev/','vscode.dev')+' for reading/editing source may be possible without an account; publishing to GitHub requires an account and appropriate permissions. That remains optional for students.</p></section>'
    body+='<section><h2>4. Using an AI coding assistant responsibly</h2><p>Give the assistant a small goal and the relevant code, not an entire secret project.</p><div class="worked"><strong>Example instruction:</strong><p>“Explain this Python function to a beginner. Suggest one small improvement, show exactly which lines change, and give a test input that would fail before the change.”</p></div><ol><li>Read the proposed change before applying it.</li><li>Run the example and one new test yourself.</li><li>Save a new version only if the result is understood and correct.</li><li>Never paste classmates’ personal data, passwords, keys or private records into an AI tool.</li></ol></section>'
    body+='</main>'+footer()+'</body></html>'
    path=ROOT/'guides/github-ai/index.html';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)

def render_bibliography():
    groups=[
      ("School curricula",["RO","CB","SG","UN","OECD","UA"]),
      ("Course books, worksheets and guided laboratories",["EA","PY","CP","POL","MSAI","MSML"]),
      ("Interactive learning environments",["TM","KM","KN","KERNEL","TF","TX","CD","JUP"]),
      ("Competitions and collaborative engineering",["ON","IO","IO25","IO26","GH"])
    ]
    html=page_start("Bibliography",extra='<script defer src="/assets/academic-ui.js"></script>')
    html+='<header class="guide-head"><p>'+a('/','← Machine Learning Club')+'</p><h1>Bibliography</h1><p>Selected school syllabi, textbooks, problem collections, websites and learning platforms used in the 15-week programme.</p></header><main>'
    for title,ids in groups:
        html+='<section><h2>'+E(title)+'</h2><ul>'
        for sid in ids:
            if sid in REGISTRY:
                name,url=REGISTRY[sid][:2];html+='<li>'+a(url,name)+'</li>'
        html+='</ul></section>'
    html+='</main>'+footer()+'</body></html>'
    (ROOT/'resources/index.html').write_text(html)

def render_catalog():
    path=ROOT/'quiz/data/catalog.json'
    meta=json.loads(path.read_text())
    available={1,2,3}
    quizzes=[]
    for w in W:
        n=w["n"]
        quizzes.append(dict(week=n,id=f'mlc-{n:02}',title=w["title"],
            subject=" · ".join(s["title"] for s in w["sections"][:2]),
            status="demo" if n in available else "planned",
            durationMinutes=5,questionCount=10 if n in available else None,
            maxPoints=10 if n in available else None))
    path.write_text(json.dumps({"version":3,"notice":"Practice quizzes in Weeks 1–3; Weeks 4–15 will be authored after lesson-by-lesson approval.","quizzes":quizzes},indent=2)+"\n")

def patch_supporting():
    # Retire obsolete resource indexes instead of leaving conflicting week plans online.
    for rel,target,label in (
        ('syllabus/index.html','/','the current 15-week curriculum'),
        ('calendar/index.html','/timetable/','the Seven Hills timetable'),
        ('materials/index.html','/resources/','the bibliography')):
        html=page_start('Moved: '+label)
        html+='<main><p>'+a('/','← Machine Learning Club')+'</p><h1>Page moved</h1>'
        html+='<p>Find '+E(label)+' at '+a(target,label)+'.</p></main>'+footer()+'</body></html>'
        (ROOT/rel).write_text(html)
    path=ROOT/'projects/index.html'
    if path.exists():
        html=path.read_text()
        html=html.replace('Machine Learning Club · Seven Hills International School',
           'Machine Learning Club · independently operated by BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ')
        path.write_text(html)

def main():
    (ROOT/"data/curriculum_2026.json").write_text(json.dumps({
      "status":"Draft classroom materials; teacher approval required per lesson","modules":[{"number":a,"title":b,"weeks":[c,d]} for a,b,c,d in MODULES],
      "weeks":[{"n":w["n"],"title":w["title"],"course":[s["title"] for s in w["sections"]],
                "lab":w["lab"]["steps"],"homework":[w["homework"]["mandatory"],w["homework"]["homework"]],
                "research":w["lab"]["research"]} for w in W]},indent=2,ensure_ascii=False)+"\n")
    (ROOT/"index.html").write_text(render_home())
    for w in W:
        for kind,_ in KINDS:
            make_week(w,kind)
    target=ROOT/"timetable/index.html";target.parent.mkdir(parents=True,exist_ok=True);target.write_text(timetable())
    render_guides()
    render_bibliography()
    render_catalog()
    patch_supporting()
    print("Published 15 weeks × 5 pages, home, timetable, guides and bibliography.")
if __name__=="__main__":main()
