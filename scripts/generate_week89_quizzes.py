#!/usr/bin/env python3
"""Reviewed practice banks for the Week 8 review and Week 9 practical evaluation.
These are ungraded five-minute knowledge checks, not confidential school exams.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BANKS={
8:("Revision: Computer Vision and Neural Networks",[
("Pixels","What describes one handwritten image in the Week 8 experiment?",["8 numbers from 0 to 255","64 numbers from 0 to 16","One text string containing the digit","Three RGB channel averages"],[1],"An 8×8 grid contains 64 block-activity counts, each between 0 and 16."),
("Training and testing","What was kept out of training when building the classifier?",["200 different labelled images","Only the number zero","All 600 training images","The teacher's handwritten notes"],[0],"Two hundred images were withheld so we can evaluate on examples not used in the model's neighbour search."),
("Supervised learning","Why is predicting handwritten digits supervised learning?",["It has no examples","It receives known digit labels for its training images","It only groups images without labels","It uses a human-written threshold without learning"],[1],"The training images each have a known target digit, and predictions use those labelled examples."),
("Nearest neighbours","With k=3, a k-nearest-neighbour classifier does what?",["Creates three clusters from unlabelled images","Selects three closest labelled training examples to vote","Uses three neural layers","Tests each digit three times then memorises the answer"],[1],"k is the number of labelled neighbours voting, not the number of unsupervised clusters."),
("Distance","For Q=(2,1) and A=(2,4), what is squared Euclidean distance?",["3","6","9","16"],[2],"(2-2)^2+(1-4)^2 = 0+9 = 9."),
("Voting","The nearest training labels are 8, 1 and 8. What is the 3-NN prediction?",["1","8","The mean 5.67","Undetermined because digits cannot be voted on"],[1],"Two votes go to digit 8 and one to digit 1."),
("Accuracy","If 196 of 200 held-out predictions are correct, what is accuracy?",["1%","2%","98%","196%"],[2],"196/200=0.98, or 98% correct on that specific subset."),
("Errors","Which observation is a genuine error in the model's default test?",["A 1 incorrectly predicted as 8","A pixel that has intensity 16","A model using 64 features","A properly withheld image"],[0],"Held-out example 17 is truly a 1 but is predicted as an 8 with k=3."),
("Interpreting results","Select ALL statements supported by an evaluation of 200 held-out images.",["The result concerns those specific 200 examples","The model will be correct on every camera photo","Its test errors should be examined","A 98% test score guarantees 98% calibrated confidence for each answer"],[0,2],"A finite held-out result supports limited empirical claims. It does not establish universal accuracy or calibrated probabilities."),
("Preprocessing","Select ALL sensible rules for a fair comparison of a pixel threshold.",["Keep the test examples fixed","Secretly replace all incorrect predictions with known answers","Compare results before and after the threshold change","Report any changed score without its dataset denominator"],[0,2],"A controlled experiment changes one feature-processing choice while retaining the same examples and reporting the denominator.")
]),
9:("Mid-Term Evaluation — practice knowledge check",[
("Algorithm selection","You need to switch a fan on whenever temperature exceeds 26 °C. What's the simplest first solution?",["A K-means model","An ordinary if statement","A ten-layer neural network","A random classifier"],[1],"A precise deterministic rule needs no training data or learned model."),
("Algorithm selection","You have delivery coordinates without any correct group labels. What is the relevant first learning method?",["Unsupervised clustering","Supervised classification with ID3","Predicting a known digit","A language model as the only option"],[0],"K-means can group unlabelled spatial examples."),
("Labels and features","In the digit recognition experiment, what is the target label?",["A pixel intensity from 0 to 16","The original row ID","The handwritten digit 0–9","The number of test examples"],[2],"The target is which digit the image represents; 64 pixel values are features."),
("Leakage","What happens if a classifier uses the known test labels to choose nearest neighbours?",["It gives a more independent test","It leaks answers into the model, invalidating independent evaluation","It automatically discovers meaningful clusters","It makes the image physically larger"],[1],"Test labels may only be consulted after predictions for evaluation."),
("Calculations","With 196 correct and 4 incorrect out of 200 tests, what is the error rate?",["2%","4%","98%","200%"],[0],"4/200 = 0.02 = 2%."),
("Model comparison","On the same 200-image test subset, k=3 gets 196 correct and k=5 gets 195. How many percentage points separate their accuracies?",["0.05","0.5","1.0","5.0"],[1],"98.0% minus 97.5% equals 0.5 percentage points."),
("Confusion matrix","Where do incorrect predictions appear in a confusion matrix with actual labels as rows and predicted labels as columns?",["Only on the diagonal","In off-diagonal cells","Only in row zero","They are excluded from the matrix"],[1],"The diagonal records a correct label. Off-diagonal counts show which labels are confused."),
("Reproducibility","Which information is necessary to reproduce the classroom classifier?",["Dataset split, distance function, k and preprocessing","Only its website colours","Only the name of the pupil","Only the score without numerator"],[0],"Data, settings and evaluation procedure must be specified."),
("Claim checking","Select ALL defensible statements about 196/200 correct results.",["This score applies to the fixed held-out classroom subset","Every person's handwriting is now guaranteed readable","Four of these particular test digits were misclassified","The system has 98% confidence in every individual prediction"],[0,2],"Report the sample and denominator; do not generalise beyond the observed data."),
("Fair evaluation","Select ALL good evaluation habits.",["Choose settings on validation data and reserve a final test set","Explain at least one failure","Use the test answers to train the model, then claim independent accuracy","Publish only a percentage and hide the denominator"],[0,1],"Separating training, model selection and final evaluation reduces bias; honest error analysis matters.")
])
}
for week,(title,rows) in BANKS.items():
    questions=[]
    for i,(topic,prompt,options,correct,explanation) in enumerate(rows,1):
        assert len(options)==4 and len(correct) in (1,2)
        questions.append(dict(id=f"w{week}q{i}",topic=topic,prompt=prompt,options=options,correct=correct,
            type="single" if len(correct)==1 else "multiple",points=1,explanation=explanation))
    result=dict(week=week,title=title,durationSeconds=300,maximumPoints=10,
      status="Draft practice quiz; teacher review required",
      instructions="Ten publicly answerable practice questions from the Course and Laboratory. Results remain only in your browser; not an official exam grade.",
      questions=questions)
    out=ROOT/f"quiz/data/week-{week:02}.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print("Updated",out.relative_to(ROOT),len(questions),"questions")
