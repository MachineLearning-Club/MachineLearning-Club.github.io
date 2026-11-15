#!/usr/bin/env python3
"""Create three account-free, one-click JupyterLite-ready Week 1 notebooks."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
target=root/'w1/lab/notebooks'
target.mkdir(parents=True,exist_ok=True)
examples=[
('01-nearest-prototype','Predict a category from learned examples',"""
from math import dist
from IPython.display import display, SVG

examples = {'A': [(2,2), (2,3), (3,2)], 'B': [(7,7),(7,8),(8,7)]}
centres = {label: tuple(sum(point[k] for point in points)/len(points) for k in range(2))
           for label,points in examples.items()}
new = (3.4,3.0) # Change this value and run again!
prediction = min(centres, key=lambda label: dist(new,centres[label]))
print('Learned class centres:',centres)
print('New example:',new,'→ prediction:',prediction)

def dot(x,y,colour,radius=9):
    return f'<circle cx="{50+x*45:.1f}" cy="{365-y*40:.1f}" r="{radius}" fill="{colour}"/>'
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="520" height="400">'
svg += '<rect width="520" height="400" fill="white"/>'
for label,points in examples.items():
    for x,y in points:svg+=dot(x,y,'#4d82ad' if label=='A' else '#bf8055')
for label,(x,y) in centres.items():
    svg+=f'<circle cx="{50+x*45:.1f}" cy="{365-y*40:.1f}" r="15" fill="none" stroke="#223e54" stroke-width="3"/>'
svg+=dot(*new,'#279b77',12)
svg+='<text x="10" y="18" font-size="15">Blue = A · Brown = B · Green = new point · Rings = learned centres</text></svg>'
display(SVG(svg))
"""),
('02-biased-die','Generate a histogram of a loaded die',"""
import random
from collections import Counter
from IPython.display import display, SVG

faces=[1,2,3,4,5,6]
weights=[1,1,1,1,1,5]   # Change the last weight to 1 for a fair die.
random.seed(11)
rolls=random.choices(faces,weights=weights,k=200)
counts=Counter(rolls)
mean=sum(rolls)/len(rolls)
print('Sample mean:',round(mean,2))
print('Observed counts:',dict(sorted(counts.items())))
svg='<svg xmlns="http://www.w3.org/2000/svg" width="650" height="330"><rect width="650" height="330" fill="white"/>'
for index,face in enumerate(faces):
    h=counts[face]*2.7
    x=55+index*95
    svg+=f'<rect x="{x}" y="{270-h:.1f}" width="62" height="{h:.1f}" fill="#628eb0"/>'
    svg+=f'<text x="{x+31}" y="290" text-anchor="middle" font-size="15">{face}</text>'
    svg+=f'<text x="{x+31}" y="{260-h:.1f}" text-anchor="middle" font-size="13">{counts[face]}</text>'
svg+='<text x="15" y="24" font-size="16">Number of occurrences of each face in 200 rolls</text></svg>'
display(SVG(svg))
"""),
('03-learn-thermostat','See a thermostat discover a rule from past decisions',"""
from IPython.display import display, SVG
temperatures=[16,17,18,20,21,23]
wanted_on=[1,1,1,0,0,0]
results=[]
for threshold in range(15,25):
    correct=sum(int(t<threshold)==y for t,y in zip(temperatures,wanted_on))
    results.append((threshold,correct))
best=max(results,key=lambda t:t[1])
print('Best threshold:',best[0],'°C')
print('Correct training decisions:',best[1],'/',len(temperatures))
print('A new 19°C reading predicts:','ON' if 19<best[0] else 'OFF')

svg='<svg xmlns="http://www.w3.org/2000/svg" width="680" height="320"><rect width="680" height="320" fill="white"/>'
for i,(threshold,correct) in enumerate(results):
    x=35+i*62
    h=correct*30
    svg+=f'<rect x="{x}" y="{270-h}" width="43" height="{h}" fill="{("#4b936e" if threshold==best[0] else "#7198b7")}"/>'
    svg+=f'<text x="{x+21}" y="289" text-anchor="middle" font-size="13">{threshold}</text>'
    svg+=f'<text x="{x+21}" y="{260-h}" text-anchor="middle" font-size="13">{correct}</text>'
svg+='<text x="15" y="22" font-size="16">How many training examples does each candidate threshold classify correctly?</text></svg>'
display(SVG(svg))
""")
]
def lines(text):return [s+'\n' for s in text.strip('\n').splitlines()]
for slug,title,code in examples:
    nb={
      'cells':[
        {'cell_type':'markdown','metadata':{},'source':lines(
          '# '+title+'\n\n'
          'All data are built in. **Press ▶ Run** (or Shift+Enter) on the code cell below to see the result. '
          'Change one number, then run again. No account is required in JupyterLite.\n\n'
          'This is a small educational experiment; do not upload private data.')},
        {'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':lines(code)},
        {'cell_type':'markdown','metadata':{},'source':lines(
          '### Try a modification\n\n'
          '1. Predict what will happen when you change one input.\n'
          '2. Change the value in the code cell and run it again.\n'
          '3. Explain which result changed and why.')}
      ],
      'metadata':{'kernelspec':{'display_name':'Python (Pyodide)','language':'python','name':'python'},
                   'language_info':{'name':'python'}},
      'nbformat':4,'nbformat_minor':5
    }
    for c in nb['cells']:
        if c['cell_type']=='code':
            compile(''.join(c['source']),str(target/slug),'exec')
    path=target/(slug+'.ipynb')
    path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
    print('Created',path)
