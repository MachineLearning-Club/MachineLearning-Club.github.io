#!/usr/bin/env python3
"""Publish aligned, openly answerable Week 12–14 practice quizzes and Week 15 review rubric."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
# (topic, prompt, four alternatives, index(es) of correct choices, concise explanation)
BANKS={
12:[
("Prediction contract","What is the Study Space Challenge's target label?",["The numeric noise value","One of avoid, consider or good","A student's name","A room's street address"],[1],"The output is one of three synthetic suitability classes."),
("Feature dictionary","Which value is a feature rather than the target?",["Wi-Fi signal 1–5","The word 'good'","Validation accuracy","A confusion-matrix label"],[0],"Wi-Fi strength is one of five input measurements."),
("Dataset provenance","Which statement correctly describes the classroom dataset?",["It measures real pupils","It is an official FiiCode dataset","It is a reproducible synthetic simulation","It contains student account details"],[2],"The example is simulated and independent of the actual competition."),
("Training set","How many labelled training rows are available?",["45","150","2400","15"],[1],"The 240-row artificial dataset is split into 150 training, 45 validation and 45 test rows."),
("Validation","What is the validation set primarily used for?",["Choosing model settings","Publicly declaring a final independent score","Inventing actual labels","Proving what every real pupil prefers"],[0],"Validation is for model selection; the final test is reserved."),
("Baseline","The training class frequencies tie. How is the constant label selected?",["Randomly each time","By looking at test labels","Alphabetically among tied majority labels","Always the longest label"],[2],"All three training classes have 50 rows; alphabetical tie-break returns avoid."),
("Worked score","The constant baseline gets 15 of 45 validation labels right. What is its accuracy?",["15%","33.3%","45%","66.7%"],[1],"15÷45=1/3."),
("Leakage","Which action invalidates the independence of the final test?",["Writing down the random seed","Separating examples before training","Choosing k from final test results","Running an independent smoke test"],[2],"Final-test feedback must not be used to choose model settings."),
("Data integrity","Select ALL checks that help guard against unreliable splits.",["Check for duplicate input examples across splits","Verify feature ranges and required fields","Insert the test labels into training","Ignore missing values"],[0,1],"Duplicates and invalid fields can undermine the exercise."),
("Scope","Select ALL claims supported by this practice benchmark.",["It includes no real student records","Its three labels are artificially balanced","It is a validated school booking service","It establishes actual room comfort with known accuracy"],[0,1],"The data are synthetic and do not establish real-world service performance."),
],
13:[
("Pipeline","What happens immediately after entering a room profile in k-NN?",["A language model writes an essay","Distances to labelled training examples are computed","The validation set is permanently rewritten","The dataset is discarded"],[1],"Distances make it possible to select neighbours."),
("K meaning","If k=3, how many labelled neighbours vote?",["3","30","150","All 240"],[0],"The closest three training examples contribute votes."),
("Input units","Why does the distance formula scale each feature?",["To guarantee every prediction is correct","To compare measurements with different numeric ranges","To hide the dataset","To turn this into clustering"],[1],"Features have different units and ranges."),
("Worked distance","With scale 100 and weight 1, what is the squared-distance contribution of a 20-point occupancy difference?",["0.04","0.2","4","20"],[0],"(20/100)² = 0.04."),
("Training","What does this introductory k-NN model store?",["Only a trained neural-network weight tensor","150 labelled training rows","The final test answers as lookup rules","No examples at all"],[1],"This method compares new samples directly to stored labelled examples."),
("Voting","Labels among nearest neighbours are good, good, avoid. What is the majority vote?",["Avoid","Consider","Good","A numeric average"],[2],"Good receives two votes."),
("Input validation","How should the Python interface handle Wi-Fi strength 8?",["Quietly change it to 5","Accept it because numbers are valid","Raise a clear validation error","Retrain on the test set"],[2],"Wi-Fi must be an integer between 1 and 5."),
("Prediction interpretation","Which is true if all three nearest neighbours vote good?",["The prediction is 100% guaranteed","The votes support good but are not a calibrated probability","The classifier is unsupervised","There is no chance of label noise"],[1],"A vote fraction is not automatically calibrated confidence."),
("Separation of components","Select ALL good software engineering practices.",["Validate inputs independently of UI widgets","Separate prediction logic from the interface","Hardcode the correct test labels inside the predictor","Hide the distance calculation from tests"],[0,1],"The model should be independently testable and the UI should enforce clear contracts."),
("Reproducibility","Select ALL factors needed to reproduce a k-NN result.",["Fixed dataset split and feature values","Specified distance, k and tie-break","Just a screenshot of the percentage","An invented probability score"],[0,1],"Settings and data completely determine the deterministic classifier."),
],
14:[
("Validation comparison","Which k scores 41/45 on the supplied validation split?",["Only k=3","k=1 and k=7","Only k=5","Every possible k"],[1],"With the fixed settings k=1 and k=7 tie at 41/45."),
("Tie-break","The top validation scores tie at k=1 and k=7. Which k does the documented rule select?",["1","7","3","5"],[0],"Choose the smaller k when correct counts tie."),
("Accuracy","41 correct of 45 examples corresponds to approximately:",["41%","84.4%","91.1%","98%"],[2],"41/45 is about 91.1%."),
("Confusion matrix","Which cells count a correct prediction?",["Off-diagonal cells","Diagonal cells","Only the last column","Only cells containing zero"],[1],"True class and predicted class agree only on the diagonal."),
("Worked recall","With 13 correctly predicted good examples out of 15 actual good examples, recall(good) is:",["13/15","15/13","13/45","2/15"],[0],"Recall is true positives divided by all actual positives for that class."),
("Leakage","What should NOT influence k before the final evaluation?",["Fixed training features","Validation result counts","The final test labels","Documented tie-break rules"],[2],"Final-test scores must remain outside parameter selection."),
("Controlled ablation","In the Week 14 experiment, removing the Wi-Fi weight changes validation score from:",["41/45 to 39/45","15/45 to 45/45","38/45 to 45/45","39/45 to 41/45"],[0],"The reference ablation reduces correct predictions by two."),
("Fair comparison","Select ALL elements to keep fixed when comparing k values.",["Validation examples","Feature scaling and distance definition","Reported denominator","Predictions manually corrected using real labels"],[0,1,2],"A controlled comparison changes k rather than multiple factors."),
("Interpreting improvement","Which conclusion is supported by the Wi-Fi ablation?",["Wi-Fi always matters in real schools","On this validation split the chosen weighted model gets two more right","The final test is automatically improved","Wi-Fi caused the label to be correct"],[1],"Ablation supports a narrow observation, not universal generalisation."),
("Choice quality","Select ALL sound evaluation habits.",["Record both failures and successes","Freeze settings before the test","Keep trying weights on final test until score is highest","Report only a headline percent without denominator"],[0,1],"Document limits and preserve an untouched final evaluation."),
],
}
for week,rows in BANKS.items():
    assert len(rows)==10
    questions=[]
    for index,(topic,prompt,options,correct,explanation) in enumerate(rows,1):
        assert len(options)==4 and 1<=len(correct)<=3 and all(0<=n<4 for n in correct)
        questions.append(dict(id=f"w{week}q{index}",topic=topic,prompt=prompt,
              options=options,correct=correct,type="single" if len(correct)==1 else "multiple",
              points=1,explanation=explanation))
    payload={"week":week,"title":f"Week {week} — Study Space Challenge practice",
        "durationSeconds":300,"maximumPoints":10,
        "status":"Draft practice questions; teacher review required",
        "instructions":"Public self-assessment based on this week's lesson; not a confidential FiiCode examination.",
        "questions":questions}
    file=ROOT/f"quiz/data/week-{week:02d}.json"
    file.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    old=(ROOT/f"w{week}/quiz/index.html").read_text(encoding="utf-8")
    main=f'''<main class="lesson-content week89-academic ss-academic">
      <p class="eyebrow">Week {week} · Practice quiz</p>
      <h1>Study Space Challenge — Knowledge Check</h1>
      <section><h2>Five-minute practice quiz</h2>
      <p>Ten openly answerable questions, aligned with the Week {week} Course and Laboratory. Scores are local practice feedback, not official school or FiiCode grades.</p>
      <div id="weekly-quiz" data-week="{week}" aria-live="polite"><p>Loading quiz…</p></div></section>
      <nav class="week-bottom-links"><a href="/w{week}/course/">Course</a><a href="/w{week}/lab/">Laboratory</a><a href="/w{week}/homework/">Homework</a><a href="/w{week}/advanced/">Advanced</a></nav>
      </main>'''
    new,num=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,old,count=1,flags=re.S)
    assert num==1
    for tag in ('<link rel="stylesheet" href="/assets/week89.css">',
                '<script defer src="/assets/weekly-quiz.js"></script>'):
        if tag not in new: new=new.replace('</head>',tag+'</head>',1)
    # Remove legacy duplicate in-body script so the quiz only loads once.
    new=new.replace('<script defer src="/assets/weekly-quiz.js"></script><nav','<nav')
    (ROOT/f"w{week}/quiz/index.html").write_text(new,encoding="utf-8")
    print("Quiz ready",week)
# Week 15 is a practical 20-point assessment rather than an ordinary knowledge quiz.
old=(ROOT/'w15/quiz/index.html').read_text(encoding="utf-8")
main='''<main class="lesson-content week89-academic ss-academic">
<p class="eyebrow">Week 15 · Practical project review</p>
<h1>Study Space Challenge — Evidence and Review Rubric</h1>
<p>The final evaluation is a working application and reproducible project, not a timed multiple-choice quiz. This 20-point rubric is an independent classroom exercise, not an official FiiCode assessment.</p>
<table class="teaching-data"><thead><tr><th>Criterion</th><th>Maximum</th><th>Evidence required</th></tr></thead><tbody>
<tr><td>Problem and data contract</td><td>4</td><td>Five features, three labels, synthetic provenance, train/validation/test split</td></tr>
<tr><td>Working implementation</td><td>6</td><td>Interactive demo, Python model, input validation, inspectable neighbours</td></tr>
<tr><td>Evaluation and error analysis</td><td>6</td><td>Baseline, validation selection, 38/45 final score, confusion matrix, limitations</td></tr>
<tr><td>Reproducible hand-off</td><td>4</td><td>README, evaluation command, tests, independent reviewer can reproduce</td></tr>
<tr><th>Total</th><th>20</th><th>Evidence should be inspectable, not described without a working artifact</th></tr>
</tbody></table>
<section><h2>Individual review checklist</h2><p>Check each item as you examine the final work. These checks are local to this page; no score is collected or sent.</p>
<div class="guide-check-items">
<label><input type="checkbox"> The data origin and sample sizes are explicitly disclosed.</label>
<label><input type="checkbox"> I can reproduce 15/45 for the baseline and 41/45 for selected validation k=1.</label>
<label><input type="checkbox"> The application accepts five inputs and shows genuine training neighbours.</label>
<label><input type="checkbox"> Invalid inputs are handled without a misleading prediction.</label>
<label><input type="checkbox"> The final test was not used to choose k and reports 38/45.</label>
<label><input type="checkbox"> The confusion matrix and a failure case are included.</label>
<label><input type="checkbox"> Another student can run python evaluate.py without installing external libraries.</label>
<label><input type="checkbox"> The report avoids generalising synthetic results to real students.</label>
</div></section>
<p><a href="/projects/study-space/">Open project overview</a> · <a href="/w15/lab/">Prepare the final laboratory hand-off</a> · <a href="/projects/study-space/study-space-starter.zip" download>Download project ZIP</a></p>
<nav class="week-bottom-links"><a href="/w15/course/">Course</a><a href="/w15/lab/">Laboratory</a><a href="/w15/homework/">Homework</a><a href="/w15/advanced/">Advanced</a></nav>
</main>'''
new,num=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,old,count=1,flags=re.S)
assert num==1
for tag in ('<link rel="stylesheet" href="/assets/week89.css">',
            '<link rel="stylesheet" href="/assets/fiicode-practice.css">'):
    if tag not in new: new=new.replace('</head>',tag+'</head>',1)
new=new.replace('<script defer src="/assets/weekly-quiz.js"></script>','')
(ROOT/'w15/quiz/index.html').write_text(new,encoding="utf-8")
catalog_file=ROOT/'quiz/data/catalog.json'
catalog=json.loads(catalog_file.read_text(encoding="utf-8"))
catalog["notice"]="Practice quizzes available for Weeks 1–9 and 12–14. Week 15 is a project review; Weeks 10–11 question banks remain in development."
for item in catalog["quizzes"]:
    if item["week"] in (12,13,14):
        item.update(title=f"Study Space Challenge — Week {item['week']}",
                    subject={12:"Dataset, baseline and held-out splits",13:"k-NN, input validation and application",14:"Model selection, confusion matrices and ablation"}[item["week"]],
                    status="demo",durationMinutes=5,questionCount=10,maxPoints=10)
    if item["week"]==15:
        item.update(title="Study Space Challenge — Project review",subject="20-point reproducibility rubric, not a timed quiz",
                    status="review",durationMinutes=0,questionCount=None,maxPoints=20)
catalog_file.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Updated quiz catalogue and Week 15 rubric")
