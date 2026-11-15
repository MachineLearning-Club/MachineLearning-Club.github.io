#!/usr/bin/env python3
"""Account-free ID3/K-means notebooks with complete synthetic data and graphs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
header='All data and code are prepared. **Run ▶ the code cells in order**. Change one number and rerun to investigate. JupyterLite uses Python in your browser; no account is required.'
def line(text):return [x+'\n' for x in text.strip('\n').splitlines()]
def notebook(title,description,code_blocks,extension):
    cells=[{'cell_type':'markdown','metadata':{},'source':line('# '+title+'\n\n'+description+'\n\n'+header)}]
    for label,code in code_blocks:
        compile(code,label,'exec')
        cells.append({'cell_type':'markdown','metadata':{},'source':line('## '+label)})
        cells.append({'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':line(code)})
    cells.append({'cell_type':'markdown','metadata':{},'source':line('## Try it yourself\n\n'+extension)})
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python (Pyodide)','language':'python','name':'python'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
weather_rows="""
from math import log2
from collections import Counter
columns=['sky','wind','temperature','go']
data=[
 ('sunny','calm','warm','yes'), ('sunny','calm','cold','yes'),
 ('sunny','windy','warm','yes'), ('sunny','windy','cold','yes'),
 ('cloudy','calm','warm','yes'), ('cloudy','calm','cold','yes'),
 ('cloudy','windy','warm','no'), ('cloudy','windy','cold','no'),
 ('rainy','calm','warm','no'), ('rainy','calm','cold','no'),
 ('rainy','windy','warm','no'), ('rainy','windy','cold','no')]
rows=[dict(zip(columns,row)) for row in data]
def entropy(values):
    counts=Counter(values); n=len(values)
    return -sum((v/n)*log2(v/n) for v in counts.values())
print('Records:',len(rows),'Known labels:',dict(Counter(row['go'] for row in rows)))
"""
ig_code="""
def gain(dataset,feature):
    before=entropy([row['go'] for row in dataset])
    remainder=0
    for value in sorted({row[feature] for row in dataset}):
        group=[row for row in dataset if row[feature]==value]
        yes=sum(row['go']=='yes' for row in group)
        h=entropy([row['go'] for row in group])
        print(feature,'=',value,'→ [',yes,'+,',len(group)-yes,'−], H =',round(h,3))
        remainder+=len(group)/len(dataset)*h
    return before-remainder
for f in columns[:-1]:
    print('Information gain for',f,'=',round(gain(rows,f),3),'bits')
"""
id3_code="""
from collections import Counter
def train(examples,features):
    labels=[row['go'] for row in examples]
    majority=sorted(Counter(labels).items(), key=lambda t:(-t[1],t[0]))[0][0]
    if len(set(labels))==1:return labels[0]
    if not features:return majority
    best=max(features,key=lambda f: gain_silent(examples,f))
    branches={}
    for value in sorted({row[best] for row in examples}):
        subset=[row for row in examples if row[best]==value]
        branches[value]=train(subset,[f for f in features if f!=best])
    return {'feature':best,'branches':branches,'fallback':majority}
def gain_silent(examples,feature):
    groups=[[r for r in examples if r[feature]==v]
            for v in sorted({r[feature] for r in examples})]
    return entropy([r['go'] for r in examples])-sum(
        len(group)/len(examples)*entropy([r['go'] for r in group]) for group in groups)
def predict(tree,example):
    path=[]
    while isinstance(tree,dict):
        feat=tree['feature']; value=example.get(feat)
        path.append(f'{feat} = {value}')
        if value not in tree['branches']:
            path.append('WARNING: unseen value, using majority fallback')
            return tree['fallback'],path
        tree=tree['branches'][value]
    path.append('predict '+tree)
    return tree,path
tree=train(rows,columns[:-1])
print('Learned tree:',tree)
for example in [
 {'sky':'cloudy','wind':'calm','temperature':'cold'},
 {'sky':'rainy','wind':'windy','temperature':'warm'},
 {'sky':'foggy','wind':'calm','temperature':'warm'}]:
 result,path=predict(tree,example)
 print(' → '.join(path),'→',result)
"""
w2_vis="""
from IPython.display import display, SVG
svg='<svg xmlns="http://www.w3.org/2000/svg" width="740" height="410">'
svg+='<rect width="740" height="410" fill="white"/>'
def box(x,y,title,subtitle,color):
    return (f'<rect x="{x-64}" y="{y-22}" width="128" height="58" rx="5" '
            f'fill="{color}" stroke="#9cb3c1"/>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-size="15">{title}</text>'
            f'<text x="{x}" y="{y+21}" text-anchor="middle" font-size="12">{subtitle}</text>')
def join(x,y,x2,y2,word):
    return (f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#829eb0" stroke-width="2"/>'
            f'<text x="{(x+x2)/2}" y="{(y+y2)/2-7}" text-anchor="middle" font-size="12">{word}</text>')
svg+=box(370,48,'Sky?','6 yes / 6 no','#eef4f8')
for x,name,label,color in [
    (118,'sunny','YES','#e4f1e8'),
    (620,'rainy','NO','#f6e9e2')]:
    svg+=join(370,82,x,165,name)+box(x,190,label,'pure',color)
svg+=join(370,82,370,165,'cloudy')+box(370,190,'Wind?','2 yes / 2 no','#eef4f8')
svg+=join(370,225,272,309,'calm')+box(272,334,'YES','2 yes','#e4f1e8')
svg+=join(370,225,468,309,'windy')+box(468,334,'NO','2 no','#f6e9e2')
svg+='</svg>'
display(SVG(svg))
print('Every leaf contains only one label; temperature was never selected.')
"""
points="""
from IPython.display import display, SVG
points={'A':(-1,0),'B':(1,0),'C':(0,1),'D':(3,0),'E':(3,1)}
initial=[(-1,0),(3,1)]
def d2(a,b):return (a[0]-b[0])**2+(a[1]-b[1])**2
def assign(points,centres):
    return {name:min(range(len(centres)),key=lambda k:d2(point,centres[k]))
            for name,point in points.items()}
def update(points,assignment,old):
    result=[]
    for k in range(len(old)):
        group=[p for name,p in points.items() if assignment[name]==k]
        if not group:
            result.append(old[k]);continue
        result.append(tuple(sum(p[i] for p in group)/len(group) for i in range(2)))
    return result
def sse(points,assignment,centres):
    return sum(d2(p,centres[assignment[name]]) for name,p in points.items())
def show(points,assignment,centres,title):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="690" height="370"><rect width="690" height="370" fill="white"/>'
    colors=['#5985af','#c18355']
    def xy(p):return (160+(p[0]+1.5)*110,300-p[1]*145)
    for name,point in points.items():
        x,y=xy(point);c=colors[assignment[name]]
        svg+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="{c}"/>'
        svg+=f'<text x="{x+17:.1f}" y="{y-9:.1f}" font-size="17">{name}</text>'
    for k,c in enumerate(centres):
        x,y=xy(c)
        svg+=f'<path d="M{x-13} {y-13}L{x+13} {y+13}M{x-13} {y+13}L{x+13} {y-13}" stroke="{colors[k]}" stroke-width="5"/>'
    svg+=f'<text x="20" y="25" font-size="17">{title}</text></svg>'
    display(SVG(svg))
    print('Groups:',{k:[name for name in points if assignment[name]==k] for k in range(len(centres))})
    print('Centres:',centres,'J =',round(sse(points,assignment,centres),4))
"""
kmeans_steps="""
centres=list(initial)
for iteration in range(3):
    labels=assign(points,centres)
    show(points,labels,centres,f'Iteration {iteration}: assignments')
    updated=update(points,labels,centres)
    print('New centres:',updated,'J after update:',round(sse(points,labels,updated),4))
    if updated==centres:
        print('No further movement: converged.')
        break
    centres=updated
"""
delivery_data="""
from IPython.display import display, SVG
points={
 'A':(0,1),'B':(1,1),'C':(1,2),'D':(2,0),'E':(2,2),
 'F':(7,7),'G':(8,6),'H':(8,8),'I':(9,7),'J':(9,9)}
# Two initial delivery hub locations. Change them and run again.
initial=[(0,1),(9,9)]
def d2(a,b):return (a[0]-b[0])**2+(a[1]-b[1])**2
def grouping(centres):
    return {name:min(range(2),key=lambda i:d2(p,centres[i])) for name,p in points.items()}
def update(centres,assignments):
    result=[]
    for i in range(2):
        group=[point for name,point in points.items() if assignments[name]==i]
        result.append(tuple(sum(p[j] for p in group)/len(group) for j in range(2)) if group else centres[i])
    return result
centres=list(initial)
for iteration in range(20):
    members=grouping(centres)
    newest=update(centres,members)
    print('Iteration',iteration+1, 'centres:',[(round(c[0],2),round(c[1],2)) for c in newest])
    if centres==newest:
        break
    centres=newest
members=grouping(centres)
error=sum(d2(point,centres[members[name]]) for name,point in points.items())
print('Final groups:',{i:[name for name in points if members[name]==i] for i in range(2)})
print('Final squared error:',round(error,3))
"""
delivery_plot="""
svg='<svg xmlns="http://www.w3.org/2000/svg" width="700" height="530"><rect width="700" height="530" fill="white"/>'
colours=['#4d84b2','#c28a55']
def xy(p):return (70+p[0]*53,460-p[1]*43)
for name,point in points.items():
    x,y=xy(point)
    svg+=f'<circle cx="{x}" cy="{y}" r="12" fill="{colours[members[name]]}"/>'
    svg+=f'<text x="{x+17}" y="{y-10}" font-size="15">{name}</text>'
for i,centre in enumerate(centres):
    x,y=xy(centre)
    svg+=f'<path d="M{x-13} {y-13}L{x+13} {y+13}M{x-13} {y+13}L{x+13} {y-13}" stroke="{colours[i]}" stroke-width="5"/>'
svg+='<text x="55" y="30" font-size="18">Ten synthetic delivery locations · two centroids marked ×</text></svg>'
display(SVG(svg))
print('Centroids can be mathematical coordinates; they need not be existing parcel locations.')
"""
books=[
 (2,'w2-id3-training','ID3 — learn from school activity data',
   'Supervised classification: known yes/no answers teach the tree which questions to ask.',
   [('1. See the training records',weather_rows),('2. Compare information gain',ig_code),('3. Train and test an ID3 tree',id3_code)],
   'Change one label in the data. Predict whether the information gains and the tree will change. Run the cells again.'),
 (2,'w2-id3-visual','Decision tree — a diagram built from labels',
   'An explanatory diagram of the same twelve-row school diary, with known outcomes.',
   [('1. Load the labelled diary',weather_rows),('2. Draw the finished tree',w2_vis)],
   'Before looking at the diagram, sketch its branches on paper. Explain why only cloudy needs a second question.'),
 (3,'w3-kmeans-steps','K-means — five points, every intermediate stage',
   'Adapted mathematically from Ciortuz, §7.1.2, problem 7: five points, two starting centres and squared error.',
   [('1. Define five locations, distances and a plot',points),('2. Execute the iterations and inspect graphs',kmeans_steps)],
   'Change the initial centres or add a point to the data. Does the algorithm still converge to the same grouping?'),
 (3,'w3-kmeans-deliveries','Delivery zones — cluster ten locations',
   'A larger original delivery-address dataset with two automatically computed collection zones.',
   [('1. Prepare ten labelled coordinates and train the groups',delivery_data),('2. Display the final scatterplot',delivery_plot)],
   'Change the two initial centres; save a new screenshot and compare the final clusters and cost.')
]
for week,slug,title,description,blocks,extension in books:
 folder=root/f'w{week}/lab/notebooks';folder.mkdir(parents=True,exist_ok=True)
 path=folder/(slug+'.ipynb')
 path.write_text(json.dumps(notebook(title,description,blocks,extension),indent=2,ensure_ascii=False)+'\n')
 print('Prepared',str(path.relative_to(root)))
