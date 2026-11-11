#!/usr/bin/env python3
"""Short, runnable 2026–27 club notebooks, matching the revised weekly titles."""
from pathlib import Path
import json,ast
ROOT=Path(__file__).resolve().parents[1]
weeks=[]
for name in ('outline_v3_01_05.json','outline_v3_06_10.json','outline_v3_11_15.json'):
    weeks.extend(json.loads((ROOT/'data'/name).read_text()))
S={}
S[3]=r'''
import numpy as np
import matplotlib.pyplot as plt

# Six courier pickup locations. There are no known class labels.
points=np.array([[1,1],[2,1],[2,2],[8,7],[8,8],[9,8]],dtype=float)
centres=np.array([[1,1],[9,8]],dtype=float)
for step in range(3):
    distances=np.linalg.norm(points[:,None,:]-centres[None,:,:],axis=2)
    groups=distances.argmin(axis=1)
    centres=np.array([points[groups==k].mean(axis=0) for k in range(2)])
    print("Iteration",step+1,": groups",groups.tolist(),"centres",centres.round(2).tolist())
plt.scatter(points[:,0],points[:,1],c=groups,cmap="coolwarm",s=70)
plt.scatter(centres[:,0],centres[:,1],marker="x",s=200,label="centres")
plt.title("Courier pickup zones");plt.legend();plt.show()
# Try different starting centres, then explain the change.
'''
S[4]=r'''
import numpy as np
import matplotlib.pyplot as plt
X=np.array([[1,2],[2,2],[2,3],[7,7],[8,7],[8,8]],float)
labels=np.array(["A","A","A","B","B","B"])
new=np.array([3,3],float)
distances=np.linalg.norm(X-new,axis=1)
for k in (1,3,5):
    nearest=np.argsort(distances)[:k]
    votes=labels[nearest]
    prediction=max(set(votes),key=lambda label:(sum(votes==label),label))
    print("K =",k,"neighbours =",votes.tolist(),"prediction =",prediction)
plt.scatter(X[:,0],X[:,1],c=(labels=="B").astype(int),cmap="coolwarm",s=90)
plt.scatter(new[0],new[1],marker="x",s=220,label="new member")
plt.title("Sports club classification");plt.legend();plt.show()
# Compare the KNN prediction with a K-Means grouping without labels.
'''
S[5]=r'''
import numpy as np
import matplotlib.pyplot as plt
# A tiny synthetic photographed worksheet.
image=np.array([[240,235,240,235,240],[236,60,55,50,235],
                [238,230,45,225,240],[240,235,48,235,240],
                [235,230,45,240,238]],dtype=np.uint8)
threshold=128
clean=np.where(image<threshold,0,255)
fig,axs=plt.subplots(1,2,figsize=(6,3))
axs[0].imshow(image,cmap="gray",vmin=0,vmax=255);axs[0].set_title("Before")
axs[1].imshow(clean,cmap="gray",vmin=0,vmax=255);axs[1].set_title("After threshold")
plt.show()
print("Central pixel:",image[2,2],"becomes",clean[2,2])
# Change threshold and check whether important ink disappears.
'''
S[6]=r'''
import numpy as np
import matplotlib.pyplot as plt
X=np.array([[1,1],[1,2],[2,1],[4,4],[4,5],[5,4]],float)
y=np.array([0,0,0,1,1,1])
weights=np.zeros(2);bias=0.0;rate=0.15
for epoch in range(8):
    mistakes=0
    for x,label in zip(X,y):
        predicted=int(np.dot(weights,x)+bias>=0)
        difference=label-predicted
        if difference:mistakes+=1
        weights+=rate*difference*x
        bias+=rate*difference
    print("Epoch",epoch+1,"errors",mistakes)
print("Learned weights",weights,"bias",bias)
plt.scatter(X[:,0],X[:,1],c=y,cmap="coolwarm",s=90)
plt.title("Toy recycling classifier");plt.show()
# Change the learning rate and explain whether training changes.
'''
S[7]=r'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
X=np.array([[0,0],[0,1],[1,0],[1,1]],dtype=float)
y=np.array([0,1,1,0])
model=MLPClassifier(hidden_layer_sizes=(8,),activation="tanh",
     max_iter=2000,learning_rate_init=.1,random_state=4)
model.fit(X,y)
print("XOR predictions:",model.predict(X).tolist())
print("Expected labels:",y.tolist())
plt.plot(model.loss_curve_);plt.xlabel("Iteration");plt.ylabel("Loss")
plt.title("Neural-network training");plt.show()
# Change the hidden layer width and plot the new loss curve.
'''
S[8]=r'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score,confusion_matrix
digits=load_digits()
Xtr,Xte,ytr,yte=train_test_split(digits.data/16.0,digits.target,test_size=.25,
                                random_state=8,stratify=digits.target)
model=MLPClassifier(hidden_layer_sizes=(30,),max_iter=250,random_state=8)
model.fit(Xtr,ytr)
pred=model.predict(Xte)
print("Accuracy:",round(accuracy_score(yte,pred),3))
print("First five actual/predicted:",list(zip(yte[:5],pred[:5])))
plt.imshow(Xte[0].reshape(8,8),cmap="gray");plt.title("One test digit");plt.show()
# Find a wrong prediction and inspect its image.
'''
S[9]=r'''
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,stratify=y,test_size=.3,random_state=9)
tree=DecisionTreeClassifier(max_depth=2,random_state=9).fit(Xtr,ytr)
pred=tree.predict(Xte)
print("Test accuracy:",round(accuracy_score(yte,pred),3))
print("Confusion matrix:\n",confusion_matrix(yte,pred))
# Explain: input features, target labels, chosen algorithm and one limitation.
'''
S[10]=r'''
from collections import Counter
text="We teach AI. AI can help students. Students must verify answers."
tokens=[token.strip(".,!?").lower() for token in text.split()]
counts=Counter(tokens)
print("Tokens:",tokens)
print("Most frequent:",counts.most_common(5))
# Toy recommender: a click is a weak signal, not a complete preference.
clicks={"sports":4,"music":2,"news":3}
print("Simple recommendation:",max(clicks,key=clicks.get))
# Discuss: how might the recommendation reinforce past behaviour?
'''
S[11]=r'''
class Sensor:
    def __init__(self,value): self.value=value
    def read(self): return self.value
class Controller:
    def decide(self,reading):
        if reading is None: return "CHECK SENSOR"
        return "HEAT ON" if reading<19 else "HEAT OFF"
class Dashboard:
    def display(self,message): print("Classroom status:",message)
sensor=Sensor(17)
controller=Controller()
Dashboard().display(controller.decide(sensor.read()))
# Change sensor.value and test None. Explain each object's responsibility.
'''
S[12]=r'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=12)
baseline=DummyClassifier(strategy="most_frequent").fit(Xtr,ytr)
pred=baseline.predict(Xte)
print("Baseline accuracy:",round(accuracy_score(yte,pred),3))
# A baseline is the smallest working comparison point.
'''
S[13]=r'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=12)
model=DecisionTreeClassifier(max_depth=2,random_state=13).fit(Xtr,ytr)
pred=model.predict(Xte)
print("Working classification pipeline:",round(accuracy_score(yte,pred),3))
print("Example predictions:",pred[:5].tolist())
# Validate inputs and package an easy-to-run demonstration.
'''
S[14]=r'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=12)
baseline=None
for depth in (1,2,3):
    model=DecisionTreeClassifier(max_depth=depth,random_state=14).fit(Xtr,ytr)
    score=accuracy_score(yte,model.predict(Xte))
    if baseline is None:baseline=score
    print("Depth:",depth,"test score:",round(score,3),"change:",round(score-baseline,3))
# This is a small demonstration. Don't repeatedly tune on final test data.
'''
S[15]=r'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
X,y=load_iris(return_X_y=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=15)
baseline=DummyClassifier(strategy="most_frequent").fit(Xtr,ytr)
final=DecisionTreeClassifier(max_depth=3,random_state=15).fit(Xtr,ytr)
print("Baseline:",round(accuracy_score(yte,baseline.predict(Xte)),3))
print("Final model:",round(accuracy_score(yte,final.predict(Xte)),3))
print(classification_report(yte,final.predict(Xte)))
# A hackathon submission also needs documentation, an input example and a demo.
'''
def cell(kind,value):
    value=value.strip("\n")
    d={"cell_type":kind,"metadata":{},"source":[line+"\n" for line in value.splitlines()]}
    if kind=="code":
        ast.parse(value)
        d.update(execution_count=None,outputs=[])
    return d
for w in weeks:
    n=w["n"]
    if n<3:continue
    code=S[n]
    intro=f'# Week {n} — {w["title"]}\n\n**Machine Learning Club · Laboratory**\n\n**Real-life situation:** {w["lab"]["context"]}\n\n1. Predict the outcome.\n2. Run the code in sequence.\n3. Change one value or parameter.\n4. Record the new output and explain its meaning.'
    notebook={"cells":[cell("markdown",intro),cell("code",code),
     cell("markdown","## What did you discover?\n\n"+'\n'.join(f'{i+1}. {step}' for i,step in enumerate(w["lab"]["steps"]))+
       "\n\n## Research (3p) — optional\n\n"+w["lab"]["research"]+
       "\n\n**Submission:** Download your edited notebook and prepare a named ZIP on this week's Laboratory page.")],
     "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                  "language_info":{"name":"python"}},
      "nbformat":4,"nbformat_minor":5}
    target=ROOT/f'w{n}/lab/starter.ipynb'
    target.write_text(json.dumps(notebook,indent=1,ensure_ascii=False)+'\n')
print("Generated 13 aligned student notebooks (Weeks 3–15), preserving Weeks 1–2.")
