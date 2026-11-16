#!/usr/bin/env python3
"""Four draft practice quizzes based on the actual Weeks 4–7 examples."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def Q(p,options,correct,explanation,topic):
 return dict(prompt=p,options=options,correct=correct,explanation=explanation,topic=topic)
questions={
4:[
 Q('Which task has NO known class labels during training?',
   ['Predicting yes/no using ID3','Grouping five delivery coordinates using K-means','Using KNN to classify a labelled player','Checking whether a prediction matches a true class'],[1],'K-means uses numerical data without supplied target classes.','Learning families'),
 Q('The 12-row diary has six yes and six no labels. What is its binary entropy?',
   ['0 bits','1 bit','2 bits','6 bits'],[1],'Balanced binary outcomes have entropy 1 bit.','ID3'),
 Q('Sky creates three four-row groups with entropies 0, 1, and 0. What is the weighted entropy after splitting?',
   ['0','1/3 bit','2/3 bit','1 bit'],[1],'Each branch gets weight 4/12, so the sum is 1/3.','Weighted averages'),
 Q('What is the information gain of the Sky question?',
   ['0','1/3 bit','2/3 bit','1 bit'],[2],'1−1/3=2/3 ≈0.667 bits.','Information gain'),
 Q('K-means first groups A(-1,0), B(1,0), C(0,1). What is their mean?',
   ['(0,1/3)','(0,1)','(1,0)','(3,1/2)'],[0],'Average the coordinates independently.','Centroids'),
 Q('What happened to J in the Ciortuz five-point example after recomputing means?',
   ['It increased from 7 to 9','It decreased from 7 to 19/6','It remained 7','It became exactly zero'],[1],'The new within-cluster squared error is 19/6≈3.167.','K-means objective'),
 Q('For KNN, K=3 means what?',
   ['Three unlabeled clusters','Three known labels as outputs','Three nearest labelled training records vote','Three hidden layers'],[2],'KNN counts nearby labelled examples, unlike K-means which specifies cluster count.','KNN preview'),
 Q('Given TP=2, TN=2, FP=1 and FN=1, what is accuracy?',
   ['1/6','2/6','4/6','6/6'],[2],'Four of six predictions were correct: (TP+TN)/N=4/6.','Evaluation'),
 Q('Which statements about a six-example test are defensible?',
   ['It is useful for practising a confusion matrix','It cannot establish reliable real-world accuracy','It proves the model will generalise forever','It can replace collecting more diverse test records'],[0,1],'A tiny test is a teaching aid, not a strong estimate of deployment performance.','Evaluation limits'),
 Q('Which procedures require labelled training examples?',
   ['ID3 classification','K-nearest neighbour classification','Ordinary K-means clustering','Unlabelled geometric grouping'],[0,1],'ID3 and KNN are supervised; K-means is unsupervised.','Algorithm selection')
],
5:[
 Q('What does I[row][column] return for a grayscale image?',
   ['A whole neural network','The intensity at one pixel','A colour class label','The number of images in a folder'],[1],'An image can be represented as a 2D table of pixel intensities.','Pixels'),
 Q('How many channel values are in a 6-by-4 RGB image with three channels per pixel?',
   ['10','24','48','72'],[3],'6×4×3=72 values before compression or metadata.','Image dimensions'),
 Q('What is the simple channel average for RGB=(120,180,240)?',
   ['120','172','180','240'],[2],'(120+180+240)/3=180.','RGB means'),
 Q('Using 0.2126R+0.7152G+0.0722B, which result is closest for RGB=(120,180,240)?',
   ['85','128','172','240'],[2],'The weighted result is 171.576, approximately 172.','Weighted grayscale'),
 Q('With T=128, rule input<T→0 else 255, what happens to value 127?',
   ['0','127','128','255'],[0],'127 is below 128, so it becomes black.','Threshold'),
 Q('With T=128, how is intensity 128 classified?',
   ['0','1','128','255'],[3],'Equality belongs to the ≥ threshold branch, giving 255.','Threshold boundary'),
 Q('A 3×3 patch contains four values 255 and five zero. What is its mean, approximately?',
   ['0','113.3','127.5','255'],[1],'4×255/9≈113.333.','Mean filtering'),
 Q('Why must a filter define what happens at image boundaries?',
   ['Some neighbouring coordinates lie outside the image','All image borders must be black','Every 3×3 kernel has nine zero coefficients','Pixels have no coordinates'],[0],'Padding, replication and valid-only convolution produce different results.','Border convention'),
 Q('Which observations about filters are correct?',
   ['Smoothing can reduce isolated pixel noise','Smoothing may blur thin writing','Thresholding always preserves faint handwriting','Sharpening cannot amplify noise'],[0,1],'Processing trades noise removal against preservation of detail.','Quality trade-offs'),
 Q('A filter response equals 1020 but the output image stores 8-bit grayscale values. What must be specified?',
   ['A clipping or scaling convention','The number of hidden neurons','A K-means label','A gradient descent learning rate'],[0],'An 8-bit output stores only 0–255; the display rule matters.','Value range')
],
6:[
 Q('For a perceptron with two inputs, what is its weighted sum?',
   ['w1+x1+w2+x2','w1×x1+w2×x2+b','x1×x2 only','K nearest points'],[1],'A perceptron sums weighted features plus a bias.','Weighted sum'),
 Q('With step(z)=1 for z≥0, what is step(-0.5)?',
   ['-1','0','0.5','1'],[1],'Negative z maps to output 0.','Activation'),
 Q('For w1=w2=1,b=-1.5 and input (1,1), what is the output?',
   ['0','0.5','1','-1'],[2],'z=1+1−1.5=0.5 gives 1.','AND example'),
 Q('For the same weights and input (1,0), what is the output?',
   ['0','1','2','Unknown'],[0],'z=1+0−1.5=−0.5 gives 0.','AND example'),
 Q('Changing the bias to -0.5 with weights 1 and 1 implements which Boolean function?',
   ['AND','OR','XOR','NOT'],[1],'The outputs become 0,1,1,1 (OR).','Bias'),
 Q('A single two-input threshold perceptron has what kind of decision boundary?',
   ['Always a circle','A straight line when weights are not both zero','A random spiral','One independent tree for each feature'],[1],'The equation w1 x1+w2 x2+b=0 is linear.','Geometry'),
 Q('Initial weights (0,0), bias -1. Input (1,1) target 1 with eta=1. What are the new weights and bias?',
   ['(0,0,-1)','(1,1,0)','(-1,-1,-2)','(2,2,1)'],[1],'Mistake signal=1, so both weights and bias increase by 1.','Update'),
 Q('If target equals prediction, what is the perceptron mistake-update signal?',
   ['-1','0','0.5','1'],[1],'t−prediction=0; no change for that example.','Update rule'),
 Q('Why can one straight-line threshold perceptron not fit binary XOR exactly?',
   ['Positive and negative examples alternate on opposite corners','XOR has no targets','The algorithm needs seven clusters','It only works on images'],[0],'XOR is not linearly separable.','Limitations'),
 Q('Which statements are correct when interpreting perceptron training?',
   ['One corrected row does not guarantee all examples are correct','The training order and rate can affect the trace','Perceptrons automatically solve contradictory labels','A training epoch means one full pass through the examples'],[0,1,3],'Training is iterative; it can have multiple errors and epochs.','Training')
],
7:[
 Q('Why do hidden layers help with XOR?',
   ['They let simple intermediate decisions combine into a nonlinear overall rule','XOR has no input data','They eliminate the need for calculations','One straight line already solves XOR'],[0],'Two simple detectors for OR and AND can combine into XOR.','Architecture'),
 Q('For inputs (1,0), what are the hidden outputs OR and AND?',
   ['(0,0)','(1,0)','(0,1)','(1,1)'],[1],'OR=1 and AND=0.','Forward pass'),
 Q('For inputs (1,1), final XOR output should be:',
   ['0','0.5','1','2'],[0],'Both hidden detectors are true, and the output is 0.','XOR'),
 Q('What is the standard sigmoid output σ(0)?',
   ['0','0.25','0.5','1'],[2],'1/(1+exp(0))=1/2.','Activation'),
 Q('For target 1 and prediction 0.5, squared loss L=0.5(t−y)^2 equals:',
   ['0','0.125','0.25','0.5'],[1],'0.5×0.5²=0.125.','Loss'),
 Q('With w=0,x=1,b=0,target=1 and sigmoid, what is dL/dw?',
   ['−0.125','0','0.125','1'],[0],'(0.5−1)×0.5×(1−0.5)×1=−0.125.','Gradient'),
 Q('With learning rate η=0.4, what is the first updated weight?',
   ['−0.4','−0.05','0','0.05'],[3],'w_new=0−0.4×(−0.125)=0.05.','Gradient descent'),
 Q('During a forward pass through a neural network, in which direction are activations computed?',
   ['From input to output','From loss to input','Only within the bias','From a test set to a training set'],[0],'A forward pass calculates layer activations and then the loss.','Forward pass'),
 Q('Which statements correctly describe backpropagation?',
   ['It computes the sensitivity of loss to weights','Hidden-layer gradients depend on downstream weights','It requires a hidden neuron to be a decision tree','It means labels are never used'],[0,1],'Backpropagation applies the chain rule from output toward earlier layers.','Backward pass'),
 Q('Which of these is a valid interpretation of lower training loss?',
   ['The model fits the training example better','It does not prove generalisation to new images','It guarantees no overfitting','It makes a held-out test unnecessary'],[0,1],'Training loss improvement alone does not establish reliable performance on unseen data.','Evaluation')
]}
for week,items in questions.items():
 data=dict(week=week,title={4:'Revision: Supervised and Unsupervised Learning',5:'Computer Vision: Images as Data',
 6:'Perceptrons: A First Learning Neuron',7:'Neural Networks and Training'}[week],
 durationSeconds=300,maximumPoints=10,status='Draft practice quiz — teacher review required',
 instructions='Ten questions drawn from the worked examples in the Course and Laboratory. Some questions require selecting all correct answers. Exact matches earn one point.',
 questions=[])
 for i,entry in enumerate(items,1):
  assert len(entry['options'])==4 and all(j in (0,1,2,3) for j in entry['correct'])
  entry.update(id=f'w{week}q{i}',type='multiple' if len(entry['correct'])>1 else 'single',points=1)
  data['questions'].append(entry)
 dest=ROOT/f'quiz/data/week-{week:02}.json'
 dest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print('Generated',dest.relative_to(ROOT),len(items))
