#!/usr/bin/env python3
"""Self-contained, school-level JupyterLite workbooks for Weeks 4–7."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def lines(s):return [line+'\n' for line in s.strip('\n').split('\n')]
def create(week,slug,title,description,sections,challenge):
 cells=[dict(cell_type='markdown',metadata={},source=lines('# '+title+'\n\n'+description+
   '\n\n**How to work:** (1) Predict the numerical output, (2) run the code in order, (3) change one input, and (4) explain the difference. The examples work in browser-only JupyterLite.'))]
 for label,code in sections:
  compile(code,slug,'exec')
  cells.append(dict(cell_type='markdown',metadata={},source=lines('## '+label)))
  cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=lines(code)))
 cells.append(dict(cell_type='markdown',metadata={},source=lines('## Independent challenge\n\n'+challenge)))
 path=ROOT/f'w{week}/lab/notebooks/{slug}.ipynb';path.parent.mkdir(parents=True,exist_ok=True)
 nb=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python (Pyodide)',language='python',name='python'),language_info=dict(name='python')),nbformat=4,nbformat_minor=5)
 path.write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
 print('Created',path.relative_to(ROOT),'cells',len(cells))
def code(s):return s.strip('\n')
def s1(s):return s

# Week 4
review_id3=code("""
from math import log2
def entropy(positive,negative):
    n=positive+negative
    return -sum((c/n)*log2(c/n) for c in (positive,negative) if c)
before=entropy(6,6)
after=4/12*entropy(4,0)+4/12*entropy(2,2)+4/12*entropy(0,4)
print("Starting entropy",before,"After Sky",after,"Information gain",before-after)
""")
review_kmeans=code("""
points={"A":(-1,0),"B":(1,0),"C":(0,1),"D":(3,0),"E":(3,1)}
centres=[(-1,0),(3,1)]
def squared_distance(p,q):return (p[0]-q[0])**2+(p[1]-q[1])**2
groups=[[],[]]
for name,p in points.items():
    k=min(range(2),key=lambda i:squared_distance(p,centres[i]))
    groups[k].append(name)
new_centres=[]
for names in groups:
    xs=[points[name][0] for name in names]; ys=[points[name][1] for name in names]
    new_centres.append((sum(xs)/len(xs),sum(ys)/len(ys)))
print("Groups:",groups,"Updated centres:",new_centres)
print("Old J:",sum(squared_distance(points[name],centres[k]) for k,names in enumerate(groups) for name in names))
print("New J:",sum(squared_distance(points[name],new_centres[k]) for k,names in enumerate(groups) for name in names))
""")
review_knn=code("""
labelled=[((1,1),"A"),((1,2),"A"),((2,1),"A"),
          ((4,4),"B"),((4,5),"B"),((5,4),"B")]
q=(2,2); k=3
ranked=sorted(((squared_distance(q,p),label,p) for p,label in labelled))
nearest=ranked[:k]
from collections import Counter
print("Three nearest:",nearest)
print("KNN predicted class:",Counter(label for _,label,_ in nearest).most_common(1)[0][0])
""")
review_test=code("""
actual=["yes","yes","yes","no","no","no"]
predicted=["yes","yes","no","no","no","yes"]
tp=sum(a=="yes" and p=="yes" for a,p in zip(actual,predicted))
tn=sum(a=="no" and p=="no" for a,p in zip(actual,predicted))
fp=sum(a=="no" and p=="yes" for a,p in zip(actual,predicted))
fn=sum(a=="yes" and p=="no" for a,p in zip(actual,predicted))
print("TP, TN, FP, FN:",tp,tn,fp,fn)
print("Held-out accuracy:",(tp+tn)/len(actual))
""")
create(4,'w4-revision-checkpoints','Week 4 — revision checkpoints',
 'Rebuild the school-activity ID3 split and the exact five-point K-means example from memory. These are the Week 2 and Week 3 datasets.',
 [('1. Recompute information gain',review_id3),('2. Rebuild K-means',review_kmeans),('3. Preview labelled KNN',review_knn),('4. Evaluate six predictions',review_test)],
 'Change one known label in the test list and recompute accuracy. Write why this does not change the training of a model.')
create(4,'w4-revision-assessment','Week 4 — independent revision assessment',
 'Use the same mathematical definitions with new questions. The code is a scaffold, not a replacement for hand calculations.',
 [('1. Load the arithmetic helpers',review_id3),
  ('2. Compare an uninformative feature',code("""print("Information gain for two balanced children:",entropy(6,6)-
 (6/12*entropy(3,3)+6/12*entropy(3,3)))
print("Why this split is unhelpful: both child distributions match the parent.")""")),
  ('3. Contrast unsupervised grouping with voting',review_kmeans),
  ('4. Make a held-out report',review_test)],
 'Before running each cell, write the expected number. Include a one-paragraph distinction between classification and clustering.')

# Week 5
image_data=code("""
from IPython.display import display, SVG
image=[
 [230,180,230,190,230],
 [220,40,55,50,220],
 [230,60,230,65,230],
 [220,55,40,60,220],
 [230,220,230,220,230]]
def display_grid(grid,title):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="420" height="355"><rect width="420" height="355" fill="white"/>'
    svg+=f'<text x="12" y="25" font-size="17">{title}</text>'
    for r,row in enumerate(grid):
        for c,value in enumerate(row):
            value=max(0,min(255,int(round(value))))
            x=50+c*61;y=40+r*56
            ink="white" if value<128 else "#1b3546"
            svg+=f'<rect x="{x}" y="{y}" width="56" height="51" fill="rgb({value},{value},{value})" stroke="#667b8b"/>'
            svg+=f'<text x="{x+28}" y="{y+30}" text-anchor="middle" font-size="14" fill="{ink}">{value}</text>'
    display(SVG(svg+"</svg>"))
display_grid(image,"Original invented 5×5 worksheet")
""")
image_threshold=code("""
def threshold_image(grid,t):
    return [[0 if v<t else 255 for v in row] for row in grid]
for t in (55,128,200):
    transformed=threshold_image(image,t)
    count=sum(v==0 for row in transformed for v in row)
    print("T =",t,"black pixels =",count)
    display_grid(transformed,"Threshold "+str(t))
""")
image_rgb=code("""
rgb=(120,180,240)
mean=sum(rgb)/3
weighted=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
print("RGB =",rgb,"simple mean =",mean,"weighted grayscale =",round(weighted,3))
""")
image_kernels=code("""
patch=[[0,0,0],[0,255,255],[0,255,255]]
mean=sum(map(sum,patch))/9
kernel=[[0,-2,0],[-2,8,-2],[0,-2,0]]
response=sum(patch[r][c]*kernel[r][c] for r in range(3) for c in range(3))
clipped=max(0,min(255,response))
print("3x3 mean",round(mean,4),"sharpening response",response,"clipped display",clipped)
""")
image_full=code("""
def mean3(grid):
    n=len(grid);m=len(grid[0])
    def clamp(v,lo,hi):return max(lo,min(hi,v))
    return [[round(sum(grid[clamp(r+dr,0,n-1)][clamp(c+dc,0,m-1)]
                       for dr in (-1,0,1) for dc in (-1,0,1))/9)
             for c in range(m)] for r in range(n)]
display_grid(image,"Original image")
display_grid(mean3(image),"Mean 3×3; replicated borders")
""")
create(5,'w5-pixels-grayscale','Week 5 — pixels, colour and threshold',
 'Work with a synthetic 5×5 grayscale image and a single RGB pixel. The methods are adapted from the uploaded UAIC Vision Lab 1–2.',
 [('1. Read a grid and plot it',image_data),('2. Make a binary image',image_threshold),('3. RGB conversion rules',image_rgb)],
 'Change exactly one source pixel to 0. Run the threshold experiment again, record which outputs changed, and explain any unexpected dark speck.')
create(5,'w5-kernels','Week 5 — neighbourhood filters',
 'Compare a mean filter with the unnormalised sharpening kernel given in UAIC Vision Lab 1. Boundary handling is explicit.',
 [('1. Load the source image',image_data),('2. Calculate two 3×3 responses by hand',image_kernels),
  ('3. Smooth a complete image with replicated edges',image_full)],
 'Find a border pixel where zero padding and edge replication give different means. Show both calculations and explain which convention you used.')

# Week 6
perceptron_table=code("""
examples=[(0,0,0),(1,0,0),(0,1,0),(1,1,1)]
def activation(z):return int(z>=0)
def predict(x1,x2,w1,w2,b):
    return activation(w1*x1+w2*x2+b)
for x1,x2,target in examples:
    z=x1+x2-1.5
    print((x1,x2),"weighted sum",z,"prediction",activation(z),"target",target)
""")
perceptron_one=code("""
w1,w2,b=0.0,0.0,-1.0
x1,x2,target=1,1,1
rate=1.0
predicted=predict(x1,x2,w1,w2,b)
error=target-predicted
w1+=rate*error*x1;w2+=rate*error*x2;b+=rate*error
print("Error =",error,"updated w1, w2, b:",(w1,w2,b))
print("New prediction for same example:",predict(x1,x2,w1,w2,b))
""")
perceptron_loop=code("""
def train(dataset,rate=0.5,epochs=25):
    w1=w2=0.0;b=-1.0
    trace=[]
    for epoch in range(1,epochs+1):
        changes=0
        for x1,x2,target in dataset:
            prediction=predict(x1,x2,w1,w2,b)
            diff=target-prediction
            changes+=int(diff!=0)
            w1+=rate*diff*x1
            w2+=rate*diff*x2
            b+=rate*diff
        trace.append((epoch,changes,round(w1,3),round(w2,3),round(b,3)))
        if changes==0:break
    return (w1,w2,b),trace
weights,trace=train(examples,rate=0.5)
for row in trace:print("epoch, mistakes, w1, w2, bias:",row)
print("Final predictions:",[predict(x,y,*weights) for x,y,_ in examples])
""")
perceptron_boundary=code("""
from IPython.display import display, SVG
def draw_boundary(w1,w2,b,title):
    def x(a):return 70+(a+.3)*250
    def y(a):return 360-(a+.3)*230
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="435"><rect width="600" height="435" fill="white"/>'
    svg+='<text x="20" y="25" font-size="17">'+title+'</text>'
    if w2:
        x0,x1=-.3,1.3
        svg+=f'<line x1="{x(x0)}" y1="{y((-b-w1*x0)/w2)}" x2="{x(x1)}" y2="{y((-b-w1*x1)/w2)}" stroke="#477f9e" stroke-width="3"/>'
    for a,c,target in examples:
        sx,sy=x(a),y(c);color="#5c8e72" if target else "#bd8862"
        svg+=f'<circle cx="{sx}" cy="{sy}" r="12" fill="{color}"/>'
        svg+=f'<text x="{sx+16}" y="{sy-7}" font-size="13">({a},{c})</text>'
    display(SVG(svg+"</svg>"))
draw_boundary(1,1,-1.5,"AND decision boundary")
draw_boundary(1,1,-0.5,"OR decision boundary")
""")
create(6,'w6-perceptron-trace','Week 6 — perceptron training trace',
 'Binary input/target convention 0 or 1 and activation step(z)=1 for z>=0. This is a school-level adaptation of Ciortuz §6.1.2.',
 [('1. Compute one truth table',perceptron_table),('2. Trace exactly one update',perceptron_one),('3. Train on all four examples',perceptron_loop)],
 'Retrain with learning rate 0.2. Compare the number of epochs and final predictions with the original trace. Next try XOR labels [0,1,1,0].')
create(6,'w6-separator-experiment','Week 6 — the geometry of one neuron',
 'A linear separator divides the feature plane. This notebook draws AND and OR boundaries and investigates why XOR is different.',
 [('1. Define targets and the activation',perceptron_table),('2. Draw two boundaries',perceptron_boundary),
  ('3. Attempt a contradictory XOR grouping',code("""xor=[(0,0,0),(1,0,1),(0,1,1),(1,1,0)]
print("XOR examples",xor)
print("Midpoint positive",(0.5,0.5),"midpoint negative",(0.5,0.5))
print("A single linear separator cannot strictly separate both diagonals.")"""))],
 'Prove the XOR contradiction by assuming one open half-plane contains the two positive points and examining their midpoint.')

# Week 7
xor_values=code("""
def step(z):return int(z>=0)
def forward_xor(x1,x2):
    h_or=step(x1+x2-.5)
    h_and=step(x1+x2-1.5)
    output=step(h_or-2*h_and-.5)
    return h_or,h_and,output
for x1,x2 in [(0,0),(1,0),(0,1),(1,1)]:
    print("inputs",(x1,x2),"hidden/output",forward_xor(x1,x2),"target",int(x1!=x2))
""")
xor_svg=code("""
from IPython.display import display, SVG
svg='<svg xmlns="http://www.w3.org/2000/svg" width="620" height="340"><rect width="620" height="340" fill="white"/>'
nodes=[(70,100,'x1'),(70,230,'x2'),(310,90,'OR'),(310,240,'AND'),(555,165,'XOR')]
for sx,sy,tx,ty in [(70,100,310,90),(70,100,310,240),(70,230,310,90),(70,230,310,240),(310,90,555,165),(310,240,555,165)]:
    svg+=f'<line x1="{sx}" y1="{sy}" x2="{tx}" y2="{ty}" stroke="#9fbacc" stroke-width="3"/>'
for x,y,label in nodes:
    svg+=f'<circle cx="{x}" cy="{y}" r="34" fill="#f5f9fc" stroke="#6387a1" stroke-width="2"/>'
    svg+=f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="17">{label}</text>'
svg+='</svg>'
display(SVG(svg))
print("Hidden detectors allow a decision boundary that a single threshold unit cannot express.")
""")
sigmoid_code=code("""
from math import exp
def sigmoid(z):return 1/(1+exp(-z))
def squared_loss(t,y):return 0.5*(t-y)**2
x,t,w,b=1.,1.,0.,0.
y=sigmoid(w*x+b)
grad=(y-t)*y*(1-y)*x
rate=.4
new_w=w-rate*grad
print("Starting output",y,"loss",squared_loss(t,y))
print("Gradient",grad,"new weight",new_w)
print("New output",sigmoid(new_w*x+b),"new loss",squared_loss(t,sigmoid(new_w*x+b)))
""")
backprop_functions=code("""
from math import exp
def sigmoid(z):return 1/(1+exp(-z))
def forward(w1,w2,x=1.,t=1.):
    hidden=sigmoid(w1*x);pred=sigmoid(w2*hidden)
    loss=0.5*(t-pred)**2
    return hidden,pred,loss
def derivatives(w1,w2,x=1.,t=1.):
    h,y,L=forward(w1,w2,x,t)
    delta=(y-t)*y*(1-y)
    grad2=delta*h
    grad1=delta*w2*h*(1-h)*x
    return grad1,grad2
w1=w2=1.
print("Hidden, output, loss:",forward(w1,w2))
print("Gradients for hidden weight and output weight:",derivatives(w1,w2))
""")
finite_difference=code("""
eps=0.001
base=forward(w1,w2)[2]
analytic_w1,analytic_w2=derivatives(w1,w2)
numeric_w2=(forward(w1,w2+eps)[2]-forward(w1,w2-eps)[2])/(2*eps)
print("Analytic output-weight gradient:",round(analytic_w2,7))
print("Numerical output-weight gradient:",round(numeric_w2,7))
print("Absolute difference:",abs(analytic_w2-numeric_w2))
""")
backprop_train=code("""
rate=0.5
for iteration in range(1,11):
    hidden,y,loss=forward(w1,w2)
    g1,g2=derivatives(w1,w2)
    # Simultaneous update: gradients computed at the same old weights.
    w1-=rate*g1
    w2-=rate*g2
    print("iteration",iteration,"output",round(y,5),"loss",round(loss,6),
          "w1",round(w1,4),"w2",round(w2,4))
print("Final loss:",round(forward(w1,w2)[2],6))
""")
create(7,'w7-xor-forward','Week 7 — forward pass through hidden neurons',
 'A worked two-layer Boolean network: teacher-provided weights implement XOR. This is representation, not a learned classifier.',
 [('1. Trace all four XOR examples',xor_values),('2. Visualise the two hidden detectors',xor_svg)],
 'Change the output threshold from −0.5 to +0.5 in the final step and identify which truth-table records stop being classified correctly.')
create(7,'w7-backprop-training','Week 7 — two-layer backpropagation from arithmetic',
 'A tiny differentiable network with one input, one sigmoid hidden neuron and one sigmoid output. This is a school-level special case of Ciortuz §6.1.3 problem 20.',
 [('1. Work a one-neuron gradient by hand',sigmoid_code),
  ('2. Define the two-layer network and chain-rule gradients',backprop_functions),
  ('3. Verify one gradient numerically',finite_difference),
  ('4. Train and record loss',backprop_train)],
 'Restart with rate 0.1; compare loss after ten steps against rate 0.5. Explain why one tiny training example is not enough to establish generalisation.')
