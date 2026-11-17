#!/usr/bin/env python3
"""Build Weeks 12–15 from linked, factual teaching material and a single practice project.

This script replaces ONLY the page body and adds the supporting practice assets,
preserving the school's established navigation, typography and footer.
"""
from html import escape
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
TITLES={
 12:"FiiCode I: Read the Challenge and Establish a Baseline",
 13:"FiiCode II: Build a Working Application",
 14:"FiiCode III: Improve, Measure and Test",
 15:"FiiCode IV: Reproduce, Present and Hand Off",
}
TEACHER={
 12:("Define the prediction problem; audit 240 synthetic examples; establish a 15/45 baseline.",
     "0–10 introduce the use case; 10–23 identify five features and labels; 23–39 inspect CSV; 39–51 measure the baseline; 51–60 discuss leakage."),
 13:("Explain the processing pipeline; trace one k-NN prediction; connect model output to a UI.",
     "0–12 draw the pipeline; 12–27 trace distance and votes; 27–45 use the interactive app; 45–55 test invalid inputs; 55–60 identify a limitation."),
 14:("Compare candidates fairly on validation data; read a confusion matrix; report one error.",
     "0–10 recall baseline; 10–25 compare k values; 25–42 error-analysis experiment; 42–53 controlled ablation; 53–60 freeze a setting."),
 15:("Run a single final test with frozen settings; demonstrate and communicate reproducibility.",
     "0–13 freeze configuration; 13–25 reveal hold-out results; 25–45 demonstrate application and tests; 45–55 peer review; 55–60 hand-off.")
}
def section(id,title,body):
 return f'<section class="chapter-section" id="{id}"><h2>{title}</h2>{body}</section>'
def intro(week,kind):
 summary,timing=TEACHER[week]
 return (f'<details class="teacher-guide"><summary>Teacher Guide '
         f'<span class="teacher-guide-hint">One 60-minute session; core + optional Research</span></summary>'
         f'<div class="teacher-guide-body"><h2>Learning outcome</h2><p>{summary}</p>'
         f'<h3>Teaching sequence</h3><p>{timing}</p>'
         '<p><strong>Core:</strong> reproducible observations, one experiment and an explanation in ordinary language. '
         '<strong>Research (3p):</strong> additional mathematics, model investigation or application engineering. '
         'All features and labels in this project are synthetic; do not infer student traits or real room conditions.</p>'
         '</div></details>')
NOTE=('<p class="understated"><strong>Independent preparation project:</strong> these are deliberately '
      'simulated examples for practising data analysis and software engineering. '
      'They are <strong>not</strong> official FiiCode rules, datasets, judging criteria or submissions.</p>')
def resource_links(week):
 name=f"study-space-week{week}.ipynb"
 return ('<div class="ss-resource-links">'
         f'<a href="/jupyter/lab/index.html?path={name}">Open Week {week} notebook in JupyterLite</a>'
         f'<a href="/w{week}/lab/notebooks/{name}" download>Download notebook (.ipynb)</a>'
         '<a href="/projects/study-space/study-space-starter.zip" download>Download complete project ZIP</a>'
         '<a href="/projects/study-space/">Practice project overview</a>'
         '</div>')
def widget():
 return '<div data-fiicode-widget><p>Loading the classroom experiment…</p></div>'
def sidebar(sections,week):
 links=''.join(f'<li><a href="#{sid}">{escape(title)}</a></li>' for sid,title,_ in sections)
 return f'<aside class="course-sidebar"><nav class="toc" aria-label="Week {week} contents"><details open class="toc-panel"><summary>Contents</summary><ul>{links}</ul></details></nav></aside>'
def page_content(week,sections):
 return (intro(week,"course")+
   '<div class="course-layout">'+sidebar(sections,week)+
   '<article class="course-article">'+NOTE+
   ''.join(section(*s) for s in sections)+
   '<section class="page-bibliography"><h2>References and onward work</h2><ul>'
   '<li><a href="/guides/python/">Python guide</a> — short programs and readable outputs.</li>'
   '<li><a href="/guides/notebooks/">Notebooks guide</a> — run and save work independently.</li>'
   '<li><a href="/guides/github-ai/">GitHub and Codespaces</a> — real repository, commits and deployment.</li>'
   '<li><a href="/guides/kaggle/">Kaggle competitions guide</a> — generic example, not a confirmed FiiCode platform.</li>'
   '</ul></section></article></div>')
COURSES={
12:[
("w12-problem","12.1. Write a testable problem, not a slogan",r'''
<p>Imagine a school showing different rooms for independent study. Should a student consider a room with most seats taken, loud background noise and weak Wi-Fi? The answer depends on the circumstances; we cannot pretend there is one universal opinion. For this exercise a <strong>simulation</strong> assigns each room profile one of three classes: <code>avoid</code>, <code>consider</code>, or <code>good</code>.</p>
<div class="core-idea"><strong>The contract</strong><p>Input: five numerical descriptions of a hypothetical study space. Output: exactly one of three categorical labels. Success means predicting the supplied synthetic labels on data withheld from training.</p></div>
<table class="teaching-data"><thead><tr><th>Feature</th><th>Allowed values</th><th>Example</th></tr></thead><tbody>
<tr><td>Occupancy</td><td>0–100%</td><td>35%</td></tr><tr><td>Noise</td><td>20–95 (illustrative dB)</td><td>42</td></tr>
<tr><td>Wi-Fi</td><td>1–5 signal levels</td><td>4</td></tr><tr><td>Outlets</td><td>0 or 1</td><td>1</td></tr>
<tr><td>Duration</td><td>15–120 minutes</td><td>60</td></tr></tbody></table>
<p>The label is a judgement made for a fabricated classroom challenge, not a measured physical property. Predicting it is <strong>supervised classification</strong> because labelled examples are available. This differs from Week 3's unlabelled clustering and Week 11's deterministic sensor rules.</p>
'''),
("w12-dataset","12.2. Inspect what is actually in the file",r'''
<p>The complete source contains <strong>240 unique simulated examples</strong>, generated with the documented random seed <code>20261117</code>. Each label has 80 examples by construction. We separate them before choosing or evaluating a model:</p>
<table class="teaching-data"><tr><th>Partition</th><th>Rows</th><th>Role</th></tr>
<tr><td>Training</td><td>150 (50/class)</td><td>Examples available to the classifier</td></tr>
<tr><td>Validation</td><td>45 (15/class)</td><td>Compare candidate settings</td></tr>
<tr><td>Final test</td><td>45 (15/class)</td><td>One evaluation after settings are frozen</td></tr></table>
<p>Student data are not collected. An ID such as <code>SS024</code> identifies an artificial row, not a person. The CSV contains seven columns: ID, the five features, and the correct class label. A duplicate ID, missing feature or impossible value would indicate an input-quality problem. A duplicate example across partitions could also make evaluation misleading.</p>
<p>Because the dataset is intentionally balanced and constructed from three overlapping profiles, we cannot use the observed class frequencies to claim how often a real study space would be suitable.</p>
<p><a href="/projects/study-space/data/train.csv" download>Inspect training.csv</a> · <a href="/projects/study-space/data/validation.csv" download>Inspect validation.csv</a></p>
'''),
("w12-baseline","12.3. A minimal working prediction",r'''
<p>Before choosing a sophisticated model, construct a <strong>baseline</strong>. Here, the most frequent training class is chosen once and used for every prediction. There is a three-way tie: 50 <code>avoid</code>, 50 <code>consider</code>, 50 <code>good</code>. We resolve it alphabetically, so the constant predictor returns <code>avoid</code>.</p>
<div class="worked"><h3>Worked baseline evaluation</h3><p>The separate validation set contains 15 actual <code>avoid</code> cases among 45 rows. A constant <code>avoid</code> prediction therefore scores <strong>15/45 = 33.3%</strong>. We did not build a useful model, but we built a working, reproducible comparison point.</p></div>
<pre><code>from collections import Counter
labels = ["avoid"] * 50 + ["consider"] * 50 + ["good"] * 50
most_common = sorted(set(labels), key=lambda c: (-labels.count(c), c))[0]
print(most_common)  # avoid — fixed tie-break
</code></pre>
<p>An improvement must beat the baseline <em>on the same evaluation examples</em>. It is not meaningful to compare scores from different test sets and call the change an algorithmic improvement.</p>
'''),
("w12-splits","12.4. Keep model selection and final checking separate",r'''
<p>Training rows let the model learn or compare labelled examples. Validation rows help choose parameters. The final test rows are reserved until the choice is finished. If we repeatedly look at test scores and change parameters accordingly, the supposedly independent test becomes part of our design process.</p>
<div class="ss-evidence"><strong>Controlled experiment</strong><p>Keep the 45 validation examples fixed. Compare one constant baseline with one candidate classifier. Record both a numerator and a denominator; avoid claims like “the AI is accurate” without an explicit sample.</p></div>
<p>Our data and scripts are public educational materials: a determined pupil can read the final CSV. Therefore this is a <strong>teaching hold-out</strong>, not a secure competition leaderboard. A real competition needs independent evaluation data and organiser-defined rules.</p>
'''),
("w12-task","12.5. Your first deliverable",r'''
<p>Start from the same <a href="/projects/study-space/">Study Space Challenge project</a> that continues through Weeks 13–15. Download the complete ZIP or run the Week 12 notebook. Explain the five features, three labels, how the split was made, and why the constant baseline gives 15 correct answers.</p>
<p><strong>Exit ticket:</strong> What would count as one observation, what exactly are we predicting, and why is 33.3% not enough evidence of a useful application?</p>
''' + resource_links(12)),
],
13:[
("w13-pipeline","13.1. Assemble the smallest end-to-end system",r'''
<p>Week 12 supplied a problem, labelled rows and a working but weak baseline. Week 13 turns that into software with a visible input and a prediction the user can examine.</p>
<div class="process-overview">
<div class="process-row"><div class="process-label">Data</div><div><p class="process-steps">Load the fixed 150 training examples</p><p class="process-note">Five features plus one known label per row</p></div></div>
<div class="process-row"><div class="process-label">Distance</div><div><p class="process-steps">Compare a new room with each training row</p><p class="process-note">Scale features before computing weighted differences</p></div></div>
<div class="process-row"><div class="process-label">Vote</div><div><p class="process-steps">Choose k nearest labelled examples</p><p class="process-note">Majority vote, deterministic tie-break</p></div></div>
<div class="process-row"><div class="process-label">Interface</div><div><p class="process-steps">Display the result and its nearest neighbours</p><p class="process-note">A prediction is not a guarantee or calibrated probability</p></div></div>
</div>
<p>This is a legitimate supervised learning application. k-nearest neighbours (k-NN) does not need a separate numerical training loop: in this simple version it retains labelled examples and compares a new input to them.</p>
'''),
("w13-distance","13.2. Compute meaningful distances",r'''
<p>We cannot directly subtract “noise in dB” from “Wi-Fi signal levels” and treat the result as a single comparable unit. Instead each feature difference is divided by a scale, squared and weighted:</p>
<div class="concept-formula"><span>Weighted squared distance</span><strong>d²(x,y) = Σ wᵢ((xᵢ−yᵢ)/sᵢ)²</strong></div>
<p>Our fixed scales are <code>(100, 60, 4, 1, 100)</code> and weights are <code>(1, 1, 0.7, 0.30, 0.15)</code> in the order occupancy, noise, Wi-Fi, outlets, duration. They are documented educational design choices, not values learned from an external school dataset.</p>
<p>When k=3, three closest examples vote. Ties favour the class with the smaller sum of neighbour distances, then alphabetical class order. Distances and votes can be inspected in the working app below.</p>
'''),
("w13-app","13.3. Try the real browser application",r'''
<p>Predict the result before changing anything. Try a quiet, half-empty room and a noisy, crowded room. Change k from 3 to 1. The displayed neighbours and votes come from the published training CSV, not from a hardcoded decision tree.</p>
''' + widget() + '''
<p><strong>Explain the trace:</strong> Which three recorded examples contributed to your result? What changes when you increase k? Why doesn't “3 of 3 votes” imply 100% probability?</p>
'''),
("w13-contract","13.4. Input validation is part of the algorithm",r'''
<p>Software has to cope with incomplete or impossible observations: Wi-Fi strength 8 is invalid; a missing noise measurement cannot silently become 0 dB. Reject bad inputs with a visible explanation rather than secretly replacing them. Use only public, artificial examples in this practice application.</p>
<pre><code>def valid_wifi(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 &lt;= value &lt;= 5
assert valid_wifi(4)
assert not valid_wifi(8)
</code></pre>
<p>The classifier itself belongs in a separate module, not hidden inside event-handler code. The browser runs an equivalent JS implementation; the downloadable Python project is the reference for tests and the final evaluation.</p>
'''),
("w13-deliver","13.5. What makes the system usable?",r'''
<p>Deliver a small application that accepts five inputs, identifies invalid data, predicts one of the three classes, and displays evidence. A visible result is more valuable than a vague claim that a machine-learning library was called.</p>
<p><strong>Exit ticket:</strong> Trace the exact path from a changed Wi-Fi slider to a predicted label, then name one part that can be tested without running a browser.</p>
''' + resource_links(13)),
],
14:[
("w14-comparison","14.1. Decide what counts as an improvement",r'''
<p>Week 13 made a real prediction. Week 14 asks whether it works reliably on examples the classifier did not use as neighbours. We compare k=1, 3, 5 and 7 using exactly the same 45 validation examples, the same features and the same distance formula.</p>
<table class="teaching-data"><thead><tr><th>Method</th><th>Correct on validation</th><th>Accuracy</th></tr></thead><tbody>
<tr><td>Constant baseline</td><td>15/45</td><td>33.3%</td></tr>
<tr><td>k-NN, k=1</td><td>41/45</td><td>91.1%</td></tr><tr><td>k-NN, k=3</td><td>39/45</td><td>86.7%</td></tr>
<tr><td>k-NN, k=5</td><td>39/45</td><td>86.7%</td></tr><tr><td>k-NN, k=7</td><td>41/45</td><td>91.1%</td></tr></tbody></table>
<p>The chosen model uses <strong>k=1</strong>, the smaller value among the two tied best validation scores. This rule must be established and recorded before looking at the final test. Even the best validation accuracy is influenced by our choice from several candidates and should not be presented as an untouched final result.</p>
'''),
("w14-confusion","14.2. Inspect more than one headline percentage",r'''
<p>A confusion matrix shows <em>which</em> predictions are wrong, not just how many. Rows are true classes, and columns are predictions. The k=1 model produces the following table on validation:</p>
<table class="teaching-data"><thead><tr><th>Actual / predicted</th><th>Avoid</th><th>Consider</th><th>Good</th></tr></thead><tbody>
<tr><th>Avoid</th><td>13</td><td>2</td><td>0</td></tr>
<tr><th>Consider</th><td>0</td><td>15</td><td>0</td></tr>
<tr><th>Good</th><td>0</td><td>2</td><td>13</td></tr></tbody></table>
<p>The diagonal totals <code>13+15+13=41</code>. The four mistakes involve the <code>consider</code> class; there are no direct avoid-versus-good errors in these 45 examples. This observation is only about the small simulated validation set.</p>
<div class="worked"><h3>Worked recall calculation</h3><p>Recall for the actual <code>good</code> class is <code>13/15 ≈ 86.7%</code>: of 15 truly good simulated rooms, two were called consider. A different question—precision—would examine how many predicted-good rooms were actually good.</p></div>
'''),
("w14-experiment","14.3. Change one variable and inspect errors",r'''
<p>Select k and press <strong>Evaluate on validation set</strong>. The matrix is recomputed, not merely recoloured. Look for an example with the wrong prediction and compare its closest neighbours.</p>
''' + widget() + '''
<p><strong>Controlled ablation:</strong> the Week 14 notebook removes the Wi-Fi weight while keeping the same examples and k=1. The validation score falls from <strong>41/45 to 39/45</strong>. This supports only the observation that Wi-Fi helped this specific experiment; it does not establish causality or guarantee the feature will help elsewhere.</p>
'''),
("w14-leakage","14.4. How to lose fairness without noticing",r'''
<p>Suppose you try 100 combinations, keep the highest validation score and only report that best value. The selected score may be optimistic for fresh data. It is worse to change a model based on the final test: then the test is no longer independent of model selection. Record every model tried and reserve one final evaluation.</p>
<p>Also check that the same labelled example does not appear in both train and validation. An algorithm that memorises training records might look better than it really is if duplicates leak into evaluation.</p>
<details><summary>Research: why a bigger score can still be misleading</summary><p>Consider two datasets, one with only obvious cases and one with difficult, ambiguous cases. The same algorithm might score differently without any change in its implementation. A fair before/after experiment fixes the data and scoring procedure.</p></details>
'''),
("w14-freeze","14.5. Freeze one decision",r'''
<p>Your deliverable is a comparison table, one confusion matrix, one documented mistake, one ablation result, and a short note specifying <code>k=1</code> for the upcoming final demonstration. Do not examine the final test to improve this choice.</p>
<p><strong>Exit ticket:</strong> Explain why k=1 and k=7 tie for the best validation score yet do not necessarily make the same individual predictions.</p>
''' + resource_links(14)),
],
15:[
("w15-handoff","15.1. Present a complete project, not a screenshot",r'''
<p>At the end of four linked sessions there should be one reproducible system: a stated problem, an auditable dataset, a baseline, a working browser application, a tested Python implementation, comparisons on validation data, a frozen model, and a final evaluation.</p>
<p>The goal is not simply to show a large percentage. A reviewer should be able to open the repository, run <code>python evaluate.py</code>, reproduce the reported output and describe exactly what the application does. An application with no reproducible code or measured results is not ready for hand-off.</p>
'''),
("w15-final","15.2. Evaluate once on the final 45 examples",r'''
<p>After selecting k=1 exclusively from validation, evaluate the frozen implementation on the 45 reserved simulated test examples. The reproducible result is <strong>38/45 = 84.4%</strong>. The final confusion matrix is:</p>
<table class="teaching-data"><thead><tr><th>Actual / predicted</th><th>Avoid</th><th>Consider</th><th>Good</th></tr></thead><tbody>
<tr><th>Avoid</th><td>15</td><td>0</td><td>0</td></tr>
<tr><th>Consider</th><td>0</td><td>12</td><td>3</td></tr>
<tr><th>Good</th><td>0</td><td>4</td><td>11</td></tr></tbody></table>
<p>There are seven mistakes: three <code>consider → good</code> and four <code>good → consider</code>. The validation score was 91.1%, so even this simple classroom exercise illustrates why validation and final test performance may differ.</p>
<div class="ss-evidence"><strong>Report responsibly</strong><p>“On 45 reserved synthetic examples from the published classroom generator, the frozen k=1 classifier correctly labelled 38 examples.” Do not claim it recommends real rooms with 84.4% reliability.</p></div>
'''),
("w15-demo","15.3. Demonstrate the product and its limitations",r'''
<p>Ask another student to pick a room profile. Record the five input values, predicted class and contributing training examples. Compare the prediction to a stated preference. A disagreement can reveal that the generated labels are not universally correct, even when the algorithm is implemented perfectly.</p>
''' + widget() + '''
<p>A k-NN vote is an algorithmic result, not a guarantee of accessibility, comfort, educational benefit or safety. The app has no current information about actual buildings, timetable conflicts, energy use or disability accommodations. It must not silently present itself as a school service.</p>
'''),
("w15-quality","15.4. Test failures as carefully as success",r'''
<p>Verify input boundaries and source integrity: Wi-Fi 1 and 5 should be valid; 0 and 6 must be rejected by the Python contract. Every row must have all five features and the label must be one of the three advertised values. The baseline and k-NN tests must use exactly the expected split sizes.</p>
<p>Test one edge case (e.g., no power outlets), one typical case, and an invalid input. Explain what the user sees, and provide an unambiguous way to reproduce each observation.</p>
'''),
("w15-rubric","15.5. Evidence, review and next steps",r'''
<table class="teaching-data"><thead><tr><th>Criterion</th><th>Points</th><th>Evidence</th></tr></thead><tbody>
<tr><td>Problem and data contract</td><td>4</td><td>Features, labels, licensing/fictional origin and partitions documented</td></tr>
<tr><td>Working implementation</td><td>6</td><td>Browser demo plus executable Python, input checks and trace</td></tr>
<tr><td>Measurement and error analysis</td><td>6</td><td>Baseline, validation comparison, selected k, final score, confusion matrix, failures</td></tr>
<tr><td>Reproducible hand-off</td><td>4</td><td>README, commands, repeatable tests, no hidden credentials</td></tr>
<tr><th>Total</th><th>20</th><th>Practice project rubric, not official FiiCode marking</th></tr></tbody></table>
<p>Provide a runnable ZIP or repository, an evidence report and a 2–3 minute demonstration. Check that someone else can repeat the outcome without you explaining every step.</p>
''' + resource_links(15)),
],
}
LABS={
12:[
("l12-audit","1. Open and inspect the dataset",r'''
<p>Download <a href="/projects/study-space/data/train.csv" download>train.csv</a> and <a href="/projects/study-space/data/validation.csv" download>validation.csv</a>. The first line is the column header. Every record contains an ID, five features and the expected class. Count examples for each class and confirm that there are no duplicate IDs.</p>
<ol class="ss-steps"><li>Predict how many examples of each label exist in the training split.</li><li>Count them in Python, not by hand.</li><li>Check that each feature contains a valid numerical value.</li><li>Explain why this artificial sample does not measure real students' preferences.</li></ol>
<div class="worked"><h3>Expected auditable quantities</h3><p>150 training rows, 45 validation rows, 50 training examples per label, and 15 validation examples per label. A row ID identifies an artificial example, not a student.</p></div>
'''),
("l12-baseline","2. Run a true baseline",r'''
<p>Open the prepared notebook and execute the most-frequent-label classifier. It must choose its constant label using <strong>training labels only</strong>. Afterwards, evaluate on validation examples and record the numerator.</p>
''' + resource_links(12) + '''
<p>Expected reference result: the baseline predicts <code>avoid</code> and correctly labels <strong>15/45</strong> validation records. Try to explain this result before reading the notebook's output.</p>
'''),
("l12-preview","3. Preview what the classifier will become",r'''
<p>The same dataset powers this web experiment for the next three weeks. Use it to compare a quiet room and a crowded noisy room. Do not treat a predicted synthetic label as a real recommendation.</p>
''' + widget() + '''
<p><strong>Research (3p):</strong> invent three additional valid profiles and explain why your preferred room label might differ from the data generator's label. Give one way to collect consent-based real feedback in a future project, without recording personally identifying details.</p>
'''),
],
13:[
("l13-implementation","1. Build and trace a genuine k-NN prediction",r'''
<p>Run the Week 13 notebook. Examine the same five feature values for the new room and one training room. The notebook computes their weighted squared distance and identifies the closest labelled examples.</p>
''' + resource_links(13) + '''
<ol class="ss-steps"><li>Run the example with 35% occupancy, 42 noise, Wi-Fi 4, outlets 1 and 60 minutes.</li><li>Record the three nearest example IDs and their labels.</li><li>Change only k from 3 to 1, then to 5. Record which cases change and which remain stable.</li><li>Explain what it means for k-NN to “learn” from the training examples.</li></ol>
'''),
("l13-ui","2. Connect the classifier to an interface",r'''
<p>Use sliders and selectors to create two contrasting profiles. For each, write down the exact inputs, selected k, predicted class and one neighbour ID. The browser and notebook implement the same distance rule.</p>
''' + widget() + '''
<p>Try an invalid Wi-Fi value <code>8</code> in the Python input-validation task. It must raise a <code>ValueError</code>. The browser limits the selector to the allowed range, but the Python model must defend its own contract independently.</p>
'''),
("l13-review","3. Test the model and its UI separately",r'''
<p>For the program itself, test an expected <code>good</code> case, an expected <code>avoid</code> case and one invalid input. For the interface, check a change in the Wi-Fi or noise control and explain how the displayed neighbour ranking changes.</p>
<div class="ss-evidence"><strong>Deliverable:</strong> completed notebook, two input/output traces, and one deliberate invalid-input test. If using GitHub, include a commit whose message describes the functionality, not just “update”.</div>
<p><strong>Research (3p):</strong> add a simple UI reset or accessibility feature, document its expected behaviour and show one test.</p>
'''),
],
14:[
("l14-record","1. Compare candidate models before deciding",r'''
<p>Load the fixed 45 validation examples and calculate accuracy for k=1,3,5,7. Begin with a prediction: which k will be most accurate? Then run the actual code and compare against 15/45 for the constant baseline.</p>
''' + resource_links(14) + '''
<p><strong>Keep the split fixed.</strong> If you generate new validation examples after seeing scores, you are no longer doing a controlled before/after comparison.</p>
'''),
("l14-errors","2. Use the matrix to find a specific failure",r'''
<p>Change k and press <strong>Evaluate on validation set</strong>. Rows in the displayed matrix are actual classes and columns are predicted classes. Count how many predictions fall off the diagonal, and find a mistaken example.</p>
''' + widget() + '''
<p>For k=1, verify the diagonal is <code>13,15,13</code>. Calculate the recall of <code>good</code> and report your result with numerator and denominator.</p>
'''),
("l14-ablation","3. Remove one feature's influence",r'''
<p>In the notebook, set the Wi-Fi weight to zero without altering the dataset, k or remaining weights. Repeat validation. The reference experiment changes from <strong>41/45</strong> to <strong>39/45</strong>. Describe what changed and what did not.</p>
<p>Do not write “the Wi-Fi feature always improves recommendations.” The evidence is only an observed two-case difference on this public, synthetic validation set.</p>
<div class="ss-evidence"><strong>Deliverable:</strong> baseline comparison, k table, confusion matrix, error example, ablation table and the frozen setting k=1.</div>
<p><strong>Research (3p):</strong> compare recall across classes before and after ablation, and explain whether the model might be unequal across classes despite similar overall accuracy.</p>
'''),
],
15:[
("l15-freeze","1. Lock the configuration before reading final results",r'''
<p>Run the notebook. First choose k on validation with the stated rule: maximize correct predictions, then use the smaller k when tied. This selects <code>k=1</code>. Document the weights and data split, and <strong>do not change them</strong> when you run the final evaluation.</p>
''' + resource_links(15) + '''
<p>The notebook contains the public educational test split; the test is intentionally absent from the Week 12–14 notebooks.</p>
'''),
("l15-repro","2. Repeat the same result from an independent program",r'''
<p>Unzip the project and run <code>python evaluate.py</code> inside its folder. It needs no machine-learning package and prints validation comparisons, chosen k, final score and a confusion matrix. You should reproduce <strong>38/45 correct</strong> on the synthetic hold-out.</p>
<p>Then run <code>python evaluate.py --predict 35 40 4 1 60</code> to inspect a specific example. The five numbers correspond to occupancy, noise, Wi-Fi, outlets and duration, in that order.</p>
'''),
("l15-demonstration","3. Show the application to another person",r'''
<p>Ask a classmate to supply a valid artificial room profile. Predict the class in the interface below, inspect its closest neighbours, then explain why the result might be inappropriate for a real person.</p>
''' + widget() + '''
<p>Review the practical project using the <a href="/w15/quiz/">20-point hand-off checklist</a>. Record a failing test or limitation alongside the successful demonstration.</p>
'''),
("l15-submit","4. Hand off executable evidence",r'''
<p>Prepare the project ZIP, a short README, the executed Week 15 notebook, a screenshot of the working UI, the final 38/45 confusion matrix and a one-paragraph limitation. Include a meaningful GitHub commit if your team used the repository workflow.</p>
<div class="ss-evidence"><strong>Deliverable:</strong> reproducible application and a short demo; not a fabricated competition submission. The teacher's collection link, if configured, is separate from local ZIP preparation.</div>
<p><strong>Research (3p):</strong> define an ethical follow-up evaluation with genuinely collected and consented room feedback, including how you would keep the data independent of training.</p>
'''),
],
}
HOMEWORK={
12:[
("h12-m","Mandatory — inspect the dataset (1p)",r'''
<p>Use the supplied <code>train.csv</code> and <code>validation.csv</code>. Produce <code>audit.md</code> with a five-column feature dictionary: each feature's unit, allowed range and one sample value. Report total examples and label counts in both splits.</p>
<p><strong>Acceptance:</strong> exactly 150 training and 45 validation rows, split class counts of 50 and 15 respectively, and explicit acknowledgement that all examples are synthetic.</p>
'''),
("h12-h","Homework — implement a baseline (2p)",r'''
<p>Create <code>baseline.py</code> that reads the CSV, determines the most frequent training label and uses it to classify all 45 validation rows. Use alphabetical label order when training frequencies tie. Save the output in <code>baseline-report.txt</code>.</p>
<p><strong>Required output:</strong> <code>Constant prediction: avoid</code> and <code>Validation accuracy: 15/45</code>. Include a sentence explaining why this is a valid comparison even though the score is low.</p>
'''),
("h12-r","Research — controlled label imbalance (3p, optional)",r'''
<p>Create a <em>copy</em> of training data with a different class distribution; never overwrite the canonical dataset. Predict how the constant baseline's label and score would change, then measure it. Explain why comparing altered validation sets would be unfair.</p>
'''),
],
13:[
("h13-m","Mandatory — trace a prediction (1p)",r'''
<p>Use the fixed training data and the input <code>(occupancy=35, noise=42, wifi=4, outlets=1, minutes=60)</code>. In <code>prediction_examples.csv</code> record the input, k=3 predicted class and the three nearest neighbour IDs and labels.</p>
<p><strong>Acceptance:</strong> actual neighbours from the supplied data and the published weighted squared distance; no hardcoded output-only function.</p>
'''),
("h13-h","Homework — working application and tests (2p)",r'''
<p>Write or adapt <code>model.py</code> to expose <code>predict(sample, k)</code>. Show two contrasting room profiles and test one invalid input, such as Wi-Fi 8. Add <code>app_evidence.md</code> with a screenshot or precise reproduction steps for the browser interface.</p>
<p><strong>Required behaviour:</strong> predictions from training examples, deterministic tie handling, readable error for invalid input and an output label in <code>avoid/consider/good</code>.</p>
'''),
("h13-r","Research — accessibility improvement (3p, optional)",r'''
<p>Add one keyboard-accessible interaction or clearer numerical explanation to the application. Supply one test case and explain why the change improves usability without altering classifier mathematics.</p>
'''),
],
14:[
("h14-m","Mandatory — model comparison (1p)",r'''
<p>In <code>validation_report.md</code>, write a five-row table: constant baseline and k=1,3,5,7. Include correct counts and accuracy percentages for the same 45 validation examples.</p>
<p><strong>Acceptance:</strong> baseline 15/45 and k results 41/45, 39/45, 39/45, 41/45. State which setting is selected and why.</p>
'''),
("h14-h","Homework — investigate errors (2p)",r'''
<p>Save the k=1 validation confusion matrix as <code>confusion.csv</code> with actual classes in rows and predicted classes in columns. Calculate recall for each class, identify at least one wrong case and produce <code>ablation.md</code> comparing default weights with Wi-Fi weight 0.</p>
<p><strong>Acceptance:</strong> diagonal 13/15, 15/15, 13/15, and the Wi-Fi ablation score 39/45. Do not use final test labels to choose settings.</p>
'''),
("h14-r","Research — test the stability of the choice (3p, optional)",r'''
<p>Explain why the best k could change with a different validation split. Propose a repeated-split experiment while keeping one final hold-out independent. Distinguish parameter tuning from final evaluation.</p>
'''),
],
15:[
("h15-m","Mandatory — hand-off specification (1p)",r'''
<p>Submit a <code>README.md</code> with the problem, five features, three labels, synthetic origin, 150/45/45 split, instructions to run <code>python evaluate.py</code> and the fixed chosen setting k=1.</p>
<p><strong>Acceptance:</strong> a classmate can reproduce the result with the project ZIP and a normal Python installation, without API keys.</p>
'''),
("h15-h","Homework — tested final demo (2p)",r'''
<p>Deliver the working application and <code>evidence.md</code> documenting the final 38/45 result, confusion matrix, one case of failure, three software tests and one real limitation. Include a 2–3 minute demonstration plan and evidence that the tests ran.</p>
<p><strong>Acceptance:</strong> reproducible program, traceable measurements and no claims that the synthetic benchmark reflects actual classrooms. Use the <a href="/w15/quiz/">project rubric</a>.</p>
'''),
("h15-r","Research — follow-up evaluation design (3p, optional)",r'''
<p>Describe how a future school trial would collect consensual, anonymised feedback, distinguish subjective preferences and assess whether the system works under different conditions. No real personal or location data should be collected for this assignment.</p>
'''),
],
}
ADVANCED={
12:[
("a12-a","Proof A — the optimal constant classifier",r'''
<p>Let the training label counts be <code>n₀, n₁, n₂</code> with <code>n=n₀+n₁+n₂</code>. A predictor that always returns class <code>c</code> gets exactly <code>n_c</code> training predictions right. Therefore, among constant classifiers, choosing a class of maximum frequency is optimal on that dataset.</p>
<div class="worked"><strong>Proof</strong><p>Any constant predictor c has correct count n<sub>c</sub>, which cannot exceed max(n₀,n₁,n₂). Predicting a majority class achieves this upper bound. QED.</p></div>
<p><strong>Exercise:</strong> explain why this proof says nothing about whether the majority-class rule is optimal among <em>all</em> possible classifiers. Construct a dataset where a rule using Wi-Fi perfectly predicts a label but the constant predictor cannot.</p>
'''),
("a12-b","Proof B — the effect of intentionally balanced labels",r'''
<p>The training and validation sets have exactly the same number of examples for each of three classes. Any fixed single-class predictor therefore succeeds on precisely one third of the validation rows, regardless of which class it chooses.</p>
<p><strong>Exercise:</strong> if 90% of future inputs are of a single class, what would happen to the constant classifier's apparent accuracy? Why can't a class-balanced classroom validation result tell us how frequently a label occurs in a real school?</p>
'''),
("a12-c","Investigation C — how leakage invalidates an estimate",r'''
<p>Imagine copying ten validation rows into training and allowing a k=1 nearest-neighbour model to find those exact copies. Assuming each identical row has its original label and no conflicting duplicates, the copied cases can be trivially memorised.</p>
<p><strong>Exercise:</strong> identify the statistical assumption being violated. State a stronger splitting protocol and explain why separate IDs alone are not sufficient when two IDs describe the same original example.</p>
'''),
],
13:[
("a13-a","Derivation A — why we scale features",r'''
<p>The raw differences <code>occupancy=20</code>, <code>wifi=2</code> and <code>outlets=1</code> have unrelated units. A squared sum without scaling is dominated by features with large numeric ranges, not necessarily those carrying more information.</p>
<div class="concept-formula"><span>Fixed weighted squared distance</span><strong>d²(x,y) = Σ wᵢ ((xᵢ−yᵢ)/sᵢ)²</strong></div>
<p>Our scales are (100,60,4,1,100), with weights (1,1,0.7,0.3,0.15). For two profiles differing only by 20 occupancy points, the contribution is <code>(20/100)²=0.04</code>; if they differ by one Wi-Fi level, the contribution is <code>0.7×(1/4)² = 0.04375</code>.</p>
<p><strong>Exercise:</strong> calculate the contribution of a 10-dB noise difference. Then determine whether removing the Wi-Fi weight changes the distance of two rows with identical Wi-Fi strength.</p>
'''),
("a13-b","Proof B — nearest-neighbour order without square roots",r'''
<p>For nonnegative numbers a and b, <code>a &lt; b</code> if and only if <code>√a &lt; √b</code>, because the square-root function is strictly increasing. Therefore ranking by nonnegative squared distance produces the same neighbour order as ranking by its square root.</p>
<p><strong>Important distinction:</strong> squared Euclidean distance generally does not obey the triangle inequality, so it should not automatically be called a metric. Using it for ranking is still valid in this classifier.</p>
'''),
("a13-c","Investigation C — ties and deterministic prediction",r'''
<p>Suppose three nearest labels are avoid, good, consider: each has one vote. The model compares the total distance among neighbours of each label, then alphabetical label order if necessary. This makes two runs with identical data deterministic.</p>
<p><strong>Exercise:</strong> construct a tie where changing distance weights alters the selected class. Explain why this is a meaningful model change that must be documented before evaluation.</p>
'''),
],
14:[
("a14-a","Derivation A — why the matrix diagonal equals correct predictions",r'''
<p>Let <code>Mᵢⱼ</code> count validation rows with actual class i and predicted class j. A prediction is correct exactly when i=j, so correct predictions equal the sum of diagonal entries. Total predictions equal the sum of all entries.</p>
<div class="worked"><strong>Week 14 example</strong><p>For k=1, the matrix rows are [13,2,0], [0,15,0], [0,2,13]. Correct = <code>13+15+13=41</code>; total = <code>45</code>. Accuracy = <code>41/45 ≈ 91.1%</code>.</p></div>
<p><strong>Exercise:</strong> compute <code>recall(good)=13/15</code> and <code>precision(consider)=15/19</code>. Explain why these two quantities answer different questions.</p>
'''),
("a14-b","Investigation B — validation selection bias",r'''
<p>If you choose the model with the highest observed validation score among many candidates, you select not only true performance differences but also favourable sampling variation. The selected score can therefore be an optimistic estimate of new-data performance.</p>
<p><strong>Exercise:</strong> imagine two equally good classifiers evaluated on small random validation sets. Explain why one of them can still appear better by chance. Why is a further untouched hold-out necessary before reporting a final score?</p>
'''),
("a14-c","Experiment C — feature ablation",r'''
<p>An ablation repeats a controlled experiment after disabling one factor. In the fixed example, k=1 with Wi-Fi weight <code>0.7</code> gives 41/45 correct on validation. With Wi-Fi weight zero, the result is 39/45.</p>
<p>The observed two-case difference is <code>2/45 ≈ 4.4 percentage points</code> on this subset. It is not proof that Wi-Fi is universally helpful or that the original weighting is optimal.</p>
<p><strong>Exercise:</strong> record which individual errors changed after the ablation. Determine whether the change improved recall for every class.</p>
'''),
],
15:[
("a15-a","Derivation A — what 38/45 actually measures",r'''
<p>The final observed accuracy is <code>p̂ = 38/45 ≈ 0.8444</code>. Because just 45 simulated examples are evaluated, one additional error changes the score by <code>1/45 ≈ 2.22 percentage points</code>. The denominator matters as much as the percentage.</p>
<p><strong>Exercise:</strong> recompute accuracy if two additional samples were misclassified. Explain why an observed percentage is not an exact guarantee about future classrooms.</p>
'''),
("a15-b","Reasoning B — compare validation and final test honestly",r'''
<p>Validation: <code>41/45 ≈ 91.1%</code> for the selected k=1. Final test: <code>38/45 ≈ 84.4%</code>. The difference is <code>3/45 ≈ 6.67 percentage points</code>. These finite samples are different, and validation was also used to select k.</p>
<p><strong>Exercise:</strong> distinguish three explanations for a difference: sample variation, model selection bias and distribution shift. Which can you actually establish using only these two small classroom subsets?</p>
'''),
("a15-c","Investigation C — soundness of the testing claim",r'''
<p>Suppose all Python tests pass and the browser displays the same predictions. What follows? The implementation may be consistent with its written specification and the provided fixtures. It does <strong>not</strong> follow that the synthetic label convention is fair, that the physical input sensors are reliable, or that the programme works for all real users.</p>
<p><strong>Exercise:</strong> write a precise claim and a counterexample for each of three levels: code correctness, benchmark performance and usefulness in a real setting. Identify the additional evidence required for the last level.</p>
'''),
],
}
def lab_content(week,sections):
 s=(intro(week,'lab')+'<div class="course-layout">'+sidebar(sections+[("submission","Submission","")],week)
    +'<article class="course-article">'+NOTE
    +''.join(section(*entry) for entry in sections)
    +'<section class="chapter-section submission-drop" id="submission"><h2>Submission</h2>'
    '<p>Export the completed notebook and evidence. Select files below to create one named ZIP locally. '
    'This action does not send work to the teacher.</p>'
    f'<div class="submission-form" data-submission-week="{week}">'
    '<label>Student name<input type="text" class="student-name" placeholder="First name, last name" maxlength="90" autocomplete="name"></label>'
    '<label class="file-drop">Choose files<input class="submission-files" type="file" accept=".ipynb,.py,.csv,.pdf,.zip,.txt,.md" multiple></label>'
    '<p class="submission-selected" aria-live="polite">No file selected.</p>'
    '<button type="button" class="prepare-submission">Download named submission</button>'
    '<p class="submission-status" aria-live="polite"></p></div>'
    '<p class="understated">A separately configured teacher collection link may appear here. Until then, keep the ZIP; '
    'downloading is not handing in an assignment.</p></section>'
    '<section class="page-bibliography"><h2>Supporting resources</h2>'
    '<p><a href="/guides/notebooks/">Notebook guide</a> · '
    '<a href="/guides/github-ai/">GitHub guide</a> · <a href="/guides/kaggle/">Competition preparation guide</a></p>'
    '</section></article></div>')
 return s
def homework_content(week,sections):
 return (intro(week,'homework')+NOTE+
     '<p>The same study-space dataset, baseline and application are used in every homework '
     'from Week 12 to Week 15. Submit evidence, not just a final number.</p>'
     '<div class="ss-resource-links"><a href="/projects/study-space/study-space-starter.zip" download>Project starter ZIP</a>'
     '<a href="/projects/study-space/">Problem and file layout</a></div>'
     +''.join(section(*entry) for entry in sections)
     +'<section class="page-bibliography"><h2>Delivery contract</h2><p>Produce the named files, '
     'record original and modified results, and export them through the corresponding '
     f'<a href="/w{week}/lab/#submission">Laboratory submission panel</a>. '
     'The named ZIP is prepared locally; teacher collection is a separate step.</p></section>')
def advanced_content(week,sections):
 return (intro(week,'advanced')+NOTE+
    '<p>Optional mathematical investigations. Read the Course before beginning; these proofs and '
    'derivations are not required to complete the 60-minute core lesson. '
    'Use your browser’s print command for a printable version.</p>'
    '<div class="course-layout">'+sidebar(sections,week)+'<article class="course-article">'
    +''.join(section(*entry) for entry in sections)
    +'<section class="page-bibliography"><h2>References and reproducibility</h2>'
    '<p>All numeric claims can be reproduced with '
    '<a href="/projects/study-space/">the same Python evaluation script and data</a>. '
    'For Python input, output and basic mathematical notation, consult the '
    '<a href="/guides/python/">club Python guide</a>.</p></section></article></div>')
def write_page(week,kind,body):
 file=ROOT/f"w{week}/{kind}/index.html"
 original=file.read_text(encoding="utf-8")
 main=(f'<main class="lesson-content week47-academic week89-academic ss-academic">'
       f'<p class="eyebrow">Week {week} · {kind.title()}</p>'
       f'<h1>{escape(TITLES[week])}</h1>'
       f'{body}'
       '<nav class="week-bottom-links" aria-label="Other learning activities">'
       +''.join(f'<a href="/w{week}/{k}/">{t}</a>' for k,t in (
         ('course','Course'),('lab','Laboratory'),('homework','Homework'),
         ('advanced','Advanced'),('quiz','Quiz / Review')))
       +'</nav></main>')
 updated,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,original,count=1,flags=re.S)
 assert count==1,file
 for name in ('course-interactive.css','week47.css','week89.css','fiicode-practice.css'):
    tag=f'<link rel="stylesheet" href="/assets/{name}">'
    if tag not in updated: updated=updated.replace('</head>',tag+'</head>',1)
 tag='<script defer src="/assets/fiicode-practice.js"></script>'
 if tag not in updated: updated=updated.replace('</head>',tag+'</head>',1)
 file.write_text(updated,encoding="utf-8")
 print("Published",file.relative_to(ROOT))
for week in (12,13,14,15):
 write_page(week,'course',page_content(week,COURSES[week]))
 write_page(week,'lab',lab_content(week,LABS[week]))
 write_page(week,'homework',homework_content(week,HOMEWORK[week]))
 write_page(week,'advanced',advanced_content(week,ADVANCED[week]))
