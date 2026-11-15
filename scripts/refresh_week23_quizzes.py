#!/usr/bin/env python3
"""Practice-only quizzes aligned with Week 2/3 authored Course and Lab materials."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
def q(week,i,prompt,options,answers,explanation,topic):
    return {'id':f'w{week}q{i}','type':'multiple' if len(answers)>1 else 'single',
            'prompt':prompt,'options':options,'correct':answers,
            'explanation':explanation,'topic':topic,'points':1}
content={
2:[
('In the school outdoor-activity table, which column is the target label?',
 ['Sky','Wind','Go outside?','Temperature'],[2],'Go outside? is the known yes/no answer supplied for supervised training.','Features and labels'),
('Why is ID3 a supervised learning algorithm?',
 ['It receives labelled training records','It invents labels without examples','It requires photographs','It cannot use categorical features'],[0],'ID3 learns a tree from examples for which the correct labels are already known.','Supervised learning'),
('A decision-tree branch contains four yes labels and no no labels. What should ID3 do?',
 ['Make a yes leaf','Keep splitting every remaining feature','Replace the four labels with unknown','Call K-means'],[0],'The branch is pure; no further feature test is needed.','Stopping at a pure node'),
('The diary contains six yes and six no examples. What is the initial binary entropy?',
 ['0 bits','0.5 bits','1 bit','2 bits'],[2],'A balanced binary class distribution has maximal entropy of 1 bit.','Entropy intuition'),
('Sky creates three equally sized branches: [4+,0−], [2+,2−], [0+,4−]. What is the weighted entropy after splitting?',
 ['0','1/3 bit','2/3 bit','1 bit'],[1],'The branch entropies are 0, 1 and 0 with equal weights 4/12, giving 1/3.','Weighted entropy'),
('What is the information gain for Sky in the twelve-row diary?',
 ['0','1/3 bit','2/3 bit','1 bit'],[2],'Information gain = entropy before (1) − entropy after (1/3) = 2/3 ≈ 0.667.','Information gain'),
('Gains are Sky: 0.667, Wind: 0.082, Temperature: 0. Which question does greedy ID3 ask first?',
 ['Temperature','Wind','Sky','All equally informative'],[2],'Sky gives the greatest reduction in label uncertainty for these examples.','Selecting the root'),
('The learned tree receives sky=cloudy, wind=calm, temperature=cold. What is its prediction?',
 ['Yes','No','Both','Unknowable despite known branches'],[0],'The path is Sky=cloudy → Wind=calm → yes; temperature is not used by this tree.','Following a decision path'),
('Which statements are appropriate when evaluating the learned tree?',
 ['Keep test labels separate from training','Check predictions against withheld labels','100% training accuracy guarantees future accuracy','A new category is always handled correctly'],[0,1],'Evaluate on held-out records; training accuracy alone does not establish generalisation.','Training and testing'),
('A new input has sky=foggy, absent from the training table. Which behaviours are defensible?',
 ['Use a documented majority fallback and warn the user','Ask for human review','Claim the prediction is certain','Silently invent a foggy branch with perfect accuracy'],[0,1],'Unseen categories require an explicit fallback, additional data, or review—not an unsupported certainty.','Unseen data')
],
3:[
('You have delivery coordinates but no correct group labels. Which task is K-means designed for?',
 ['Supervised regression','Unsupervised clustering','Boolean equation solving','Sentence tokenisation'],[1],'K-means groups numerical observations without known cluster labels.','Learning families'),
('What does K=2 mean?',
 ['Two features','Two target labels supplied by the teacher','Two centroids / clusters requested','Two Python loops'],[2],'K is the chosen number of clusters.','K parameter'),
('For B(1,0), initial centroids μ₁=(-1,0), μ₂=(3,1), what are the squared distances?',
 ['2 and 5','4 and 5','5 and 4','4 and 9'],[1],'d²(B,μ₁)=(1+1)²=4; d²(B,μ₂)=(1−3)²+(0−1)²=5.','Distance calculation'),
('With the initial centroids A and E, which points join the first cluster?',
 ['A, B and C','A and E','D and E','All five'],[0],'A, B and C are nearest to μ₁; D and E to μ₂.','Assignment step'),
('What is the mean of A(-1,0), B(1,0), C(0,1)?',
 ['(-1,0)','(0,1/3)','(1,1/3)','(0,1)'],[1],'Average x=(-1+1+0)/3=0 and y=(0+0+1)/3=1/3.','Updating the first centroid'),
('The second cluster contains D(3,0), E(3,1). What is its new centroid?',
 ['(3,1/2)','(3,1)','(6,1)','(1.5,0.5)'],[0],'Average x=3 and average y=(0+1)/2=0.5.','Updating the second centroid'),
('The total squared error decreases from 7 to 19/6 after updating centroids. What does that indicate?',
 ['Assigned points are collectively closer in squared distance to their centres','All points now have the same labels','The number of points has changed','K became larger'],[0],'The within-cluster sum of squared distances has decreased.','Objective function'),
('Why does K-means use the arithmetic mean when updating a centroid?',
 ['The mean minimises the sum of squared distances within a fixed group','The mean always equals an existing point','The mean guarantees correct human labels','The mean does not depend on outliers'],[0],'For a fixed group, the average coordinate minimises squared Euclidean distance to its members.','Centroid and squared error'),
('Which steps describe an ordinary K-means iteration?',
 ['Assign each point to its closest current centroid','Update each centroid to its group average','Read known supervised class labels','Ask the student to calculate entropy'],[0,1],'An iteration alternates nearest-centroid assignment with arithmetic-mean updating.','Algorithm mechanics'),
('Which factors can change the quality or meaning of a K-means result?',
 ['Starting centroid positions','The chosen K','Outliers and feature units','The arbitrary name assigned to a cluster'],[0,1,2],'Initialisation, K, scale and outliers affect the geometry; renaming cluster 1 as cluster A does not.','Interpreting clusters')
]
}
for week,items in content.items():
    file=root/f'quiz/data/week-{week:02}.json'
    data=json.loads(file.read_text())
    data['status']='Draft practice quiz — teacher review required'
    data['durationSeconds']=300
    data['maximumPoints']=10
    data['instructions']='Ten questions about the examples taught this week. Select all correct choices where instructed; exact matches earn full credit.'
    data['questions']=[q(week,i,*item) for i,item in enumerate(items,1)]
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Aligned',file,':',len(data['questions']),'questions')
