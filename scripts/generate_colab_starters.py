#!/usr/bin/env python3
"""Generate 15 self-contained, editable, school-safe Colab notebooks.

These notebooks intentionally use small synthetic/public datasets and CPU-only
NumPy/Pandas/scikit-learn. They are runnable in a standard Colab environment.
"""
import json, ast
from pathlib import Path
root=Path(__file__).resolve().parents[1]
weeks=[]
for p in ("weeks_01_05.json","weeks_06_10.json","weeks_11_15.json"):
    weeks+=json.loads((root/"data"/p).read_text())
code={}
code[1]=r"""
import numpy as np
from collections import Counter
# A tiny synthetic dataset: colour intensity and object width.
X = np.array([[0.2, 1.0],[0.3, 0.8],[0.1,1.1],[0.9,2.0],[1.0,2.2],[0.8,1.8]])
y = np.array(['A','A','A','B','B','B'])
centres = {label: X[y == label].mean(axis=0) for label in np.unique(y)}
def predict(features):
    distances = {label: np.linalg.norm(features-centre) for label, centre in centres.items()}
    return min(distances, key=distances.get)
test = np.array([[0.2,0.9],[0.9,2.1],[0.5,1.4]])
for x in test: print(x, "->", predict(x))
# TODO: Add three new tests, vary a feature and describe a failure.
"""
code[2]=r"""
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
values = np.array([2, 4, 4, 6, 7, 8])
labels = np.array(['yes','yes','yes','no','no','no'])
print("Mean:", values.mean(), "Median:", np.median(values))
def entropy(items):
    counts = np.array(list(Counter(items).values()), dtype=float)
    probabilities = counts / counts.sum()
    return float(-(probabilities * np.log2(probabilities)).sum())
print("Label counts:", Counter(labels))
print("Entropy:", entropy(labels))
plt.hist(values, bins=4); plt.title("Numeric feature distribution"); plt.show()
# TODO: add records and recalculate the entropy.
"""
code[3]=r"""
import numpy as np
from collections import Counter
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import OrdinalEncoder
# Weather/outdoor labels; encode categories ONLY for the illustrative sklearn tree.
X = np.array([['sunny','hot'],['sunny','mild'],['rain','mild'],['rain','hot'],
              ['sunny','hot'],['rain','mild'],['sunny','mild'],['rain','hot']])
y = np.array([0,1,1,0,0,1,1,0])
def entropy(y):
    counts = np.array(list(Counter(y).values()), dtype=float)
    p = counts/counts.sum()
    return float(-(p*np.log2(p)).sum())
def information_gain(feature, y):
    conditional = 0
    for value in set(feature):
        subset = y[feature == value]
        conditional += len(subset)/len(y)*entropy(subset)
    return entropy(y)-conditional
for j, label in enumerate(['weather','temperature']):
    print(label, "information gain:", round(information_gain(X[:,j],y),4))
enc=OrdinalEncoder(); xt=enc.fit_transform(X)
model=DecisionTreeClassifier(criterion='entropy',max_depth=2,random_state=1).fit(xt,y)
print(export_text(model,feature_names=['weather','temperature']))
# TODO: change labels; recompute gains. Note: sklearn CART is not ID3.
"""
code[4]=r"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
rng=np.random.default_rng(4)
X=rng.normal(size=(120,2))
y=(X[:,0]+0.5*X[:,1]>0).astype(int)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,random_state=7,stratify=y)
for depth in [1,2,5,None]:
    model=DecisionTreeClassifier(max_depth=depth,random_state=3).fit(Xtr,ytr)
    pred=model.predict(Xte)
    print("depth:",depth,"train:",round(model.score(Xtr,ytr),3),"test:",round(accuracy_score(yte,pred),3))
    print(confusion_matrix(yte,pred), "precision:",round(precision_score(yte,pred),3),
          "recall:",round(recall_score(yte,pred),3))
# TODO: change depth, add noise and explain a disagreement.
"""
code[5]=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X=np.array([[1,10],[2,9],[2,11],[7,2],[8,3],[9,2],[4,6],[6,4]])
y=np.array([0,0,0,1,1,1,0,1])
query=np.array([[5,5]])
print("Euclidean distances:",np.round(np.linalg.norm(X-query,axis=1),2))
for k in [1,3,5]:
    m=make_pipeline(StandardScaler(),KNeighborsClassifier(n_neighbors=k)).fit(X,y)
    print("k",k,"prediction",m.predict(query)[0])
plt.scatter(X[:,0],X[:,1],c=y,cmap="coolwarm");plt.scatter(query[:,0],query[:,1],marker="x",s=150)
plt.title("KNN examples");plt.show()
# TODO: change k and query location. Show one manual vote.
"""
code[6]=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
X=np.array([[0,0],[0,1],[1,0],[5,5],[5,6],[6,5]],dtype=float)
centres=np.array([[0,0],[6,6]],dtype=float)
for step in range(2):
    dist=np.linalg.norm(X[:,None,:]-centres[None,:,:],axis=2)
    labels=dist.argmin(axis=1)
    centres=np.array([X[labels==k].mean(axis=0) for k in range(2)])
    print("step",step+1,"labels:",labels,"centres:",centres)
model=KMeans(n_clusters=2,random_state=5,n_init=10).fit(X)
print("sklearn centres:",model.cluster_centers_)
plt.scatter(X[:,0],X[:,1],c=model.labels_);plt.scatter(*model.cluster_centers_.T,marker="x",s=160)
plt.show()
# TODO: change initial centres and one point; explain instability.
"""
code[7]=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error
X=np.array([10,13,16,19,22,25],dtype=float).reshape(-1,1)
y=np.array([60,85,92,126,149,160],dtype=float)
model=LinearRegression().fit(X,y)
pred=model.predict(X)
print("slope",round(model.coef_[0],3),"intercept",round(model.intercept_,3))
print("MAE",round(mean_absolute_error(y,pred),3),"MSE",round(mean_squared_error(y,pred),3))
print("Prediction for x=20:",round(model.predict([[20]])[0],2))
plt.scatter(X[:,0],y,label="observed");plt.plot(X[:,0],pred,label="model")
plt.legend();plt.show()
# TODO: add an outlier and compare residuals.
"""
code[8]=r"""
import numpy as np
import matplotlib.pyplot as plt
image=np.array([[0,0,0,10,10],[0,0,0,10,10],[0,0,0,10,10],
                [0,0,0,10,10],[0,0,0,10,10]],dtype=float)
kernel=np.array([[-1,0,1],[-1,0,1],[-1,0,1]],dtype=float)
output=np.zeros((3,3))
for r in range(1,4):
    for c in range(1,4):
        output[r-1,c-1]=np.sum(image[r-1:r+2,c-1:c+2]*kernel)
print("Center result:",output[1,1])
fig,axes=plt.subplots(1,2,figsize=(6,3))
axes[0].imshow(image,cmap='gray');axes[0].set_title('Pixels')
axes[1].imshow(output,cmap='gray');axes[1].set_title('Filter output')
plt.show()
# TODO: replace kernel with a blur and calculate two cells manually.
"""
code[9]=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
X=np.array([[0,0],[0,1],[1,0],[1,1]])
y=np.array([0,1,1,0]) # XOR
def neuron(x,w,b):
    return int(np.dot(x,w)+b >= 0)
for x in X:print("simple neuron",x,neuron(x,np.array([2,-1]),-.5))
network=MLPClassifier(hidden_layer_sizes=(8,),activation="tanh",max_iter=4000,
                      learning_rate_init=.1,random_state=1)
network.fit(X,y)
print("XOR predictions:",network.predict(X),"true labels:",y)
plt.scatter(X[:,0],X[:,1],c=y,s=120);plt.title('XOR');plt.show()
# TODO: change hidden layer size and compare results.
"""
code[10]=r"""
import numpy as np
# Tiny synthetic "vision to action" pipeline with transparent rules.
images=np.array([
 [[0,0,0],[0,1,0],[0,0,0]],
 [[1,1,1],[1,1,1],[1,1,1]],
 [[0,0,0],[0,0,0],[0,0,0]]
],dtype=float)
def extract_feature(im):return im.mean()
def classify(feature):return "bright" if feature>=.5 else "dark"
def recommendation(label,confidence):
    if confidence<.6:return "Human review required"
    return "Check light source" if label=="bright" else "Inspect low lighting"
for i,im in enumerate(images):
    value=extract_feature(im)
    label=classify(value)
    confidence=min(1.0,abs(value-.5)*2)
    print(i,{"feature":round(value,3),"class":label,
             "confidence":round(confidence,2),
             "action":recommendation(label,confidence)})
# TODO: add a novel image and change the human-review threshold.
"""
code[11]=r"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
# Synthetic chronological daily demand: no future values in the features.
rng=np.random.default_rng(11)
day=np.arange(50)
demand=25+0.4*day+3*np.sin(day/4)+rng.normal(0,1.5,50)
df=pd.DataFrame({"day":day,"demand":demand})
df["lag1"]=df["demand"].shift(1)
df=df.dropna()
train=df.iloc[:34]; test=df.iloc[34:]
naive=np.repeat(train["demand"].mean(),len(test))
model=LinearRegression().fit(train[["day","lag1"]],train["demand"])
forecast=model.predict(test[["day","lag1"]])
print("Naive MAE:",mean_absolute_error(test["demand"],naive))
print("Regression MAE:",mean_absolute_error(test["demand"],forecast))
plt.plot(test["day"],test["demand"],label="actual");plt.plot(test["day"],forecast,label="forecast")
plt.legend();plt.show()
# TODO: remove lag1 and compare, preserving chronological split.
"""
code[12]=r"""
import pandas as pd
# The source text below is synthetic; do NOT regard it as externally fact-checked.
records=[
 {"claim":"The supplied table has 3 rows.","source":"Notebook data only","verdict":"supported","reason":"Count rows in the lab source"},
 {"claim":"Every confident AI answer is correct.","source":"Not demonstrated","verdict":"unsupported","reason":"Confidence is not evidence"},
 {"claim":"A proposed 2027 event will take place in May.","source":"No official confirmation supplied","verdict":"uncertain","reason":"Requires a dated official source"}
]
df=pd.DataFrame(records)
print(df.to_string(index=False))
print("Verdict counts:",df["verdict"].value_counts().to_dict())
# TODO: add three independently sourced claims and include actual URLs in 'source'.
# For privacy, never paste classmates' personal records or unapproved uploads.
"""
code[13]=r"""
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import pandas as pd
X,y=load_iris(return_X_y=True,as_frame=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=13)
baseline=DummyClassifier(strategy="most_frequent").fit(Xtr,ytr)
model=DecisionTreeClassifier(max_depth=2,random_state=13).fit(Xtr,ytr)
for name,m in [("dummy",baseline),("tree",model)]:
    prediction=m.predict(Xte)
    print(name,"accuracy:",round(accuracy_score(yte,prediction),3))
    print(confusion_matrix(yte,prediction))
print("Data schema:",list(X.columns))
# TODO: experiment with exactly one parameter; do not tune on final test.
"""
code[14]=r"""
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
X,y=load_iris(return_X_y=True,as_frame=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=13)
experiments=[]
for columns,depth,label in [
    (list(X.columns),2,"full-depth2"),
    (list(X.columns),3,"full-depth3"),
    (list(X.columns[:2]),2,"first-two-features")
]:
    m=DecisionTreeClassifier(max_depth=depth,random_state=13).fit(Xtr[columns],ytr)
    experiments.append({"experiment":label,"accuracy":accuracy_score(yte,m.predict(Xte[columns]))})
for e in experiments:print(e)
# TODO: change one variable only; compare errors on identical rows.
"""
code[15]=r"""
from sklearn.datasets import load_iris
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
import pandas as pd
X,y=load_iris(return_X_y=True,as_frame=True)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=15)
baseline=DummyClassifier(strategy="most_frequent").fit(Xtr,ytr)
final=DecisionTreeClassifier(max_depth=3,random_state=15).fit(Xtr,ytr)
print("Baseline:",accuracy_score(yte,baseline.predict(Xte)))
print("Model:",accuracy_score(yte,final.predict(Xte)))
print(classification_report(yte,final.predict(Xte)))
print("Five demonstration predictions:",final.predict(Xte.iloc[:5]))
# TODO: write a short model card and explain at least one mistaken prediction.
"""
assert len(code)==15
def nbcell(tp,source):
    d=dict(cell_type=tp,metadata={},source=[line+"\n" for line in source.strip().splitlines()])
    if tp=="code":d.update(execution_count=None,outputs=[])
    return d
for w in weeks:
    n=w["n"]
    introduction=f"""# Week {n:02} — {w["sections"][0][0]}
Machine Learning Club · Seven Hills International School

**Activity:** {w["app"][2]}

This is a short, runnable starter notebook. Study the related Course and interactive web application before changing the Python code.

**Learning tasks**
"""+"\n".join(f"{i+1}. {x}" for i,x in enumerate(w["lab"]))
    file={"cells":[nbcell("markdown",introduction),nbcell("code",code[n]),
                   nbcell("markdown","## Explain your experiment\n\n1. What was the input? What output did you predict?\n2. Change one value or parameter and rerun the notebook.\n3. Record a result, a failure or an assumption.\n4. Reuse the same code for your Homework, with new data. Do not upload personal student data.")],
          "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                      "language_info":{"name":"python"}},
          "nbformat":4,"nbformat_minor":5}
    dest=root/f"w{n}/lab/starter.ipynb";dest.write_text(json.dumps(file,ensure_ascii=False,indent=1),encoding="utf-8")
    for cell in file["cells"]:
        if cell["cell_type"]=="code":ast.parse("".join(cell["source"]))
print("Generated 15 syntactically valid Colab starter notebooks.")
