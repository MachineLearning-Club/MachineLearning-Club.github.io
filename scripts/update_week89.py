#!/usr/bin/env python3
"""Apply researched, authored Weeks 8–9 to existing site chrome.
The generic publisher intentionally skips these pages. The script is idempotent.
"""
from pathlib import Path
from html import escape
import re
from site_footer import site_footer
ROOT=Path(__file__).resolve().parents[1]
TITLES={8:"Revision: Computer Vision and Neural Networks",9:"Mid-Term Evaluation"}
LABELS=dict(course="Course",lab="Laboratory",homework="Homework",advanced="Advanced",quiz="Quiz")
SUBMISSION='''<div class="submission-form" data-submission-week="{week}">
 <label>Student name<input type="text" class="student-name" maxlength="90" autocomplete="name" placeholder="First name, last name"></label>
 <label class="file-drop">Choose your files<input class="submission-files" type="file" accept=".ipynb,.py,.csv,.pdf,.zip,.txt" multiple></label>
 <p class="submission-selected" aria-live="polite">No file selected.</p>
 <button type="button" class="prepare-submission">Download named submission</button>
 <p class="submission-status" aria-live="polite"></p>
 <p class="understated">Creates a named ZIP locally. Does not send files to the school.</p>
</div>'''
WIDGET=(ROOT/"data/week89/digit_widget.html").read_text()
for week,title in TITLES.items():
 for kind,label in LABELS.items():
    file=ROOT/f"w{week}/{kind}/index.html"
    if kind=="quiz":
        fragment=f'''<section><h2>Five-minute practice knowledge check</h2>
<p>This question bank reviews what you can practise in Week {week}. It is public, not a confidential or official school grade. Results are stored in this browser only.</p>
<div id="weekly-quiz" data-week="{week}" aria-live="polite"><p>Loading quiz…</p></div></section>'''
    else:
        fragment=(ROOT/f"data/week89/w{week}_{kind}.html").read_text()
        fragment=fragment.replace('<!-- WEEK89_DIGIT_WIDGET -->',WIDGET)
        if kind=="lab":
            fragment,count=re.subn(r'(<section id="submission"[^>]*>\s*<h2>[^<]*</h2>)',
                    lambda m:m.group(1)+SUBMISSION.format(week=week),fragment,count=1)
            assert count==1,(week,kind,"No submission section")
    main='<main class="lesson-content week23-academic week47-academic week89-academic'+(' course-lesson' if kind=="course" else '')+'">'
    main+=f'<p class="eyebrow">Week {week:02} · {label}</p><h1>{escape(title)}</h1>'
    if kind=="course":main+='<p class="deck">A practical, evidence-based bridge between model intuition, mathematical reasoning, and executable evaluation.</p>'
    elif kind=="lab":main+='<p class="deck">Predict first. Run the model. Change one setting. Examine genuine mistakes.</p>'
    main+=fragment
    main+='<nav class="week-bottom-links" aria-label="Other learning activities">'
    for k,v in LABELS.items():main+=f'<a href="/w{week}/{k}/">{v}</a>'
    main+='</nav></main>'
    original=file.read_text()
    html,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,original,count=1,flags=re.S)
    assert count==1,(week,kind,"No main")
    for stylesheet in ("course-interactive.css","week89.css"):
        tag=f'<link rel="stylesheet" href="/assets/{stylesheet}">'
        if tag not in html:html=html.replace("</head>",tag+"</head>",1)
    scripts=["weekly-quiz.js"] if kind=="quiz" else (["week89-interactive.js"] if kind in ("course","lab") else [])
    for name in scripts:
        tag=f'<script defer src="/assets/{name}"></script>'
        if tag not in html:html=html.replace("</head>",tag+"</head>",1)
    # Do not leave legacy quiz script outside main.
    assert html.count('id="weekly-quiz"')==(1 if kind=="quiz" else 0)
    file.write_text(html)
    print("Authored",file.relative_to(ROOT))
# Printable, noninteractive public practice test. It reuses the live evaluation brief
# but is not positioned as a secure school exam.
printer=ROOT/"data/week89/practical_print.html"
output=ROOT/"w9/lab/practical-print.html"
src=printer.read_text()
html=('<!doctype html><html lang="en"><head><meta charset="utf-8">'
'<meta name="viewport" content="width=device-width,initial-scale=1">'
'<title>Week 9 · Practical assessment · Printable sheet</title>'
'<meta name="description" content="Print-friendly public practice assessment: handwritten digit classifier, 20 points.">'
'<link rel="stylesheet" href="/assets/academic.css">'
'<link rel="stylesheet" href="/assets/week89.css">'
'<link rel="stylesheet" href="/assets/site-footer.css">'
'<style>@media print{.sheet-note,.site.mlclub-footer{display:none!important}body{max-width:none!important} .sheet{margin:0!important;padding:0!important} .answer-space{min-height:45px}}'
'body{max-width:850px;margin:30px auto;padding:0 22px;font-family:Georgia,serif}'
'.sheet section{margin:26px 0;border-top:1px solid #d8e2e9;padding:12px 0}'
'.answer-space{min-height:55px;border-bottom:1px solid #ccd9e1;display:block}'
'.sheet h1{font-size:1.65rem;font-weight:500}'
'.sheet small{color:#62788a}'
'</style></head><body><main class="sheet"><p class="sheet-note"><a href="/w9/lab/">← Return to the interactive assessment</a> · Print with Ctrl+P</p>'
+src+'</main>'+site_footer()+'</body></html>')
output.write_text(html)
print("Authored",output.relative_to(ROOT))
