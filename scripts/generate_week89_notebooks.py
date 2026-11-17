#!/usr/bin/env python3
"""Self-contained Week 8/9 Python notebooks. No scikit-learn/NumPy dependency."""
import base64,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=json.loads((ROOT/'assets/data/week89-digits.json').read_text())
pack=base64.b85encode(zlib.compress(json.dumps({'train':src['train'],'test':src['test']},separators=(',',':')).encode(),9)).decode()
load='''import base64, zlib, json
DATA = %r
records = json.loads(zlib.decompress(base64.b85decode(DATA)).decode())
training, testing = records["train"], records["test"]
print("Loaded",len(training),"training images and",len(testing),"held-out test images.")
''' % pack
functions='''def squared_distance(a,b,threshold=0):
    if threshold:
        a = [16 if v>=threshold else 0 for v in a]
        b = [16 if v>=threshold else 0 for v in b]
    return sum((x-y)**2 for x,y in zip(a,b))

def nearest(image,k=3,threshold=0):
    distances=[(squared_distance(image,row["x"],threshold),row["id"],row["y"]) for row in training]
    distances.sort()
    chosen=distances[:k]
    votes={}
    for d,_,y in chosen:
        if y not in votes:votes[y]=[0,0]
        votes[y][0]+=1
        votes[y][1]+=d
    answer=min(votes,key=lambda y:(-votes[y][0],votes[y][1],y))
    return answer,chosen

def evaluate(k=3,threshold=0):
    confusion=[[0]*10 for _ in range(10)]
    guesses=[]
    for row in testing:
        predicted,_=nearest(row["x"],k,threshold)
        guesses.append(predicted)
        confusion[row["y"]][predicted]+=1
    correct=sum(pred==row["y"] for pred,row in zip(guesses,testing))
    return correct,confusion,guesses

def show_image(values):
    shades=" .:-=+*#%@"
    for i in range(8):
        print("".join(shades[round(v/16*(len(shades)-1))] for v in values[8*i:8*(i+1)]))
'''
def cell(kind,txt,hidden=False):
    c=dict(cell_type=kind,metadata={},source=[s+'\n' for s in txt.strip().split('\n')])
    if kind=='code':
        c.update(execution_count=None,outputs=[])
        if hidden:c['metadata']['jupyter']={'source_hidden':True}
    return c
def notebook(week,title,sections):
    intro=f'''# {title}

**Source:** E. Alpaydin & C. Kaynak (1998), Optical Recognition of Handwritten Digits, UCI ML Repository, DOI https://doi.org/10.24432/C50P49 (CC BY 4.0). Retrieved from scikit-learn's digits.csv.gz, which contains 1,797 original rows.

**Fixed educational subset:** 600 labelled training images (60 per digit) and 200 held-out images (20 per digit), from a new deterministic split with seed 20261116. This is not the original UCI train/test partition.

Each handwritten digit is an 8×8 image of 64 measurements, integers from 0 to 16. The compressed dataset below is embedded inside this notebook, so the notebook needs no downloads, API credentials, external libraries or accounts. Run all cells in order; do not edit the hidden test labels.
'''
    cells=[cell('markdown',intro),cell('code',load,True),
           cell('markdown','## A genuine nearest-neighbour classifier\n\nFor each new image, calculate 64 squared pixel differences to each labelled training image, sort distances, then take a majority vote over k neighbours. Tie-break by smaller total squared distance and then by smaller label.'),
           cell('code',functions)]
    for header,story,code in sections:
        compile(code,header,'exec')
        cells.extend([cell('markdown','## '+header+'\n\n'+story),cell('code',code)])
    nb={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python (Pyodide)','language':'python','name':'python'},'language_info':{'name':'python'}},'nbformat':4,'nbformat_minor':5}
    filename='digits-revision.ipynb' if week==8 else 'digits-practical.ipynb'
    dest=ROOT/f'w{week}/lab/notebooks/{filename}'
    dest.parent.mkdir(exist_ok=True,parents=True)
    dest.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
    target=ROOT/f'jupyter/files/{filename}'
    target.parent.mkdir(exist_ok=True,parents=True)
    target.write_bytes(dest.read_bytes())
    print('Generated',dest.relative_to(ROOT),len(cells),'cells',dest.stat().st_size,'bytes')
notebook(8,'Week 8 — handwritten-digit classification',[
 ('1. Read a real image','The first held-out digit was excluded from training. Inspect its 8×8 values.', '''item=testing[0]
print("Example #1: original row ID",item["id"],"known label",item["y"])
show_image(item["x"])
pred,near=nearest(item["x"],3)
print("Predicted:",pred,"nearest (d², ID, label):",near)'''),
 ('2. Evaluate original images','Record your prediction first. With k=3 and no threshold, the model correctly identifies 196 of 200 held-out examples.', '''K=3
THRESHOLD=0
correct,matrix,guesses=evaluate(K,THRESHOLD)
print(f"k={K}, threshold={THRESHOLD}: {correct}/200 = {correct/2:.1f}%")
assert correct==196'''),
 ('3. Investigate one mistake','Held-out example #17 has a known digit label different from its predicted label.', '''bad=testing[16]
p,near=nearest(bad["x"],k=3)
print("Known",bad["y"],"predicted",p,"neighbours",near)
show_image(bad["x"])'''),
 ('4. Change one thing','Choose K=1 or K=5, or use a pixel threshold of 8, while keeping exactly the same examples.', '''K=5
THRESHOLD=0
correct_new,new_matrix,new_guesses=evaluate(K,THRESHOLD)
print(f"k={K}, threshold={THRESHOLD}: {correct_new}/200")
print("Change relative to baseline:",correct_new-196)'''),
 ('5. Confusion matrix','Rows = actual digit, columns = predicted digit. Every row must sum to 20.', '''for d,values in enumerate(new_matrix):
    print(f"{d}:", " ".join(f"{n:2d}" for n in values), "total",sum(values))
assert all(sum(row)==20 for row in new_matrix)'''),
 ('6. Your conclusion','Add a Markdown cell with a table of configurations, one observed failure, and a limited numerical claim. Save a copy and download the .ipynb.', '''print("Next: report tested settings, correct count, observed error and limitation.")''')
])
notebook(9,'Week 9 — 20-point practical evaluation',[
 ('Part A — algorithm choice (5 points)','In a Markdown cell justify a fixed rule for a thermostat, supervised classification for labelled digits and clustering for unlabelled delivery coordinates.', '''print("Input: 64 pixels; expected output: an integer label 0..9")
print("Add your Part A explanations in a Markdown cell.")'''),
 ('Part B — trace one prediction (5 points)','Inspect held-out image #17; record actual and predicted labels and three neighbours with distances.', '''item=testing[16]
prediction,near=nearest(item["x"],k=3)
print("Actual:",item["y"],"predicted:",prediction)
for distance,original_id,label in near:
    print("squared distance",distance,"training ID",original_id,"known label",label)
show_image(item["x"])'''),
 ('Part C — compare two classifiers (6 points)','Use the same held-out examples for k=3 and k=5, with no pixel threshold. Do not edit labels.', '''c3,matrix3,preds3=evaluate(k=3,threshold=0)
c5,matrix5,preds5=evaluate(k=5,threshold=0)
print("k=3",c3,"/200 =",f"{c3/2:.1f}%")
print("k=5",c5,"/200 =",f"{c5/2:.1f}%")
assert c3==196 and c5==195
print("Difference in correct results:",c3-c5)'''),
 ('Part D — report evidence and limitations (4 points)','Locate actual mistakes, then in Markdown write a supported result, one failure, one limitation and one next action.', '''errors=[(i+1,row["y"],label) for i,(row,label) in enumerate(zip(testing,preds3))
        if row["y"]!=label]
print("Wrong predictions (test index, real label, predicted):")
for entry in errors:print(entry)
assert len(errors)==4'''),
 ('Your submission','Save Notebook As… if the original is read-only, then File → Download. Add report.txt or a Markdown answer section for Parts A–D. This is a public practice assessment.', '''print("Ready for an evidence-based Part A–D report.")''')
])
