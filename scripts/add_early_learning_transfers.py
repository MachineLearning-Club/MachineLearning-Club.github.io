#!/usr/bin/env python3
"""Make the conceptual transitions in Weeks 1–7 explicit.

Each week gets an independently checkable Course derivation, a Laboratory
transfer exercise, and a concrete Homework evidence contract. The canonical
source fragments remain authoritative for Weeks 2–7. Re-running this script
is safe (stable ids, no duplicate inserts).
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

COURSE={
1:('1 → 2 · From conditional probability to labelled examples', '''
<p>In this week's die exercise, the faces are equally likely. Knowing the face is even changes the sample space from ten faces to five: <code>P(X = 2 | X is even) = 1/5</code>. That is an example of <strong>conditioning on information</strong>, not learning from a dataset.</p>
<p>In Week 2 we will count observed <em>label frequencies</em> instead. If six recorded decisions are yes and six are no, the estimated proportions in that classroom dataset are <code>p(yes)=6/12</code> and <code>p(no)=6/12</code>. A decision tree searches for a question that makes the answers less mixed.</p>
<div class="transfer-worked"><strong>Predict before revealing</strong><p>If a question separates twelve labelled examples into three equal groups with counts <code>[4 yes, 0 no]</code>, <code>[2 yes, 2 no]</code>, and <code>[0 yes, 4 no]</code>, which group is hardest to predict?</p>
<details><summary>Check the reasoning</summary><p>The middle group is split evenly, so a label cannot be chosen from this subset more reliably than a 50–50 guess using only its class frequencies. The other two groups are pure. This motivates <a href="/w2/course/#w2-entropy">entropy and information gain in Week 2</a>: before the split, entropy is 1 bit; after this split its weighted average is 1/3 bit.</p></details></div>
<p class="transfer-limitation">A conditional probability on a fair die and a class proportion in an invented school diary are different sources of probabilities. Neither automatically proves a prediction about future real pupils.</p>
'''),
2:('2 → 3 · What changes when the labels disappear?', '''
<p>ID3 can choose <code>Sky</code> as its root because the twelve activity examples have known yes/no answers. On just the four <code>cloudy</code> records, there are two yes (both calm) and two no (both windy). Asking about <code>Wind</code> separates them perfectly.</p>
<div class="transfer-worked"><strong>Calculate on the correct subset</strong><p>Before the question, the cloudy subset has entropy <code>H(2/4, 2/4) = 1 bit</code>. Wind creates two pure two-row branches: <code>H(after)=2/4·0 + 2/4·0 = 0</code>. Therefore <code>IG(Wind | Sky=cloudy)=1 bit</code>.</p>
<details><summary>Why is this different from the global gain for Wind?</summary><p>The global <code>IG(Wind) ≈ 0.082</code> uses all twelve rows. The conditional gain above uses only the four cloudy rows. The group and its label counts have changed; comparing the two values as though they came from the same subset is an error.</p></details></div>
<p><strong>Remove the yes/no column.</strong> The features now describe days, but we have no correct target to predict. ID3's supervised training contract is unavailable. We could instead group examples by similarity, but those groups do <strong>not</strong> magically mean safe versus unsafe weather. <a href="/w3/course/#w3-problem">Week 3 introduces unsupervised K-means</a> for precisely that distinction.</p>
'''),
3:('3 → 4 · A cluster is not a class label', '''
<p>In the five-point example, the first assignment gives group 1 = {A, B, C} and group 2 = {D, E}. Their updated means are <code>μ₁=(0,1/3)</code> and <code>μ₂=(3,1/2)</code>. What have we actually improved?</p>
<div class="transfer-worked"><strong>Compute the total squared error</strong><p>In group 1, the three squared distances to <code>(0,1/3)</code> are <code>10/9, 10/9, 4/9</code>; together they sum to <code>8/3</code>. In group 2, the distances are <code>1/4, 1/4</code>; together they sum to <code>1/2</code>. Total: <code>J = 8/3 + 1/2 = 19/6 ≈ 3.167</code>, down from the initial value <code>7</code>.</p>
<details><summary>Does a lower J tell us which points are “good”?</summary><p>No. J measures distances to group centres, not whether a named label is correct. The points carried no correct class labels. A smaller objective is evidence about clustering compactness on these five points, not supervised prediction accuracy.</p></details></div>
<p>In <a href="/w4/course/#r-knn">Week 4, k-nearest neighbours (k-NN)</a> uses labelled training examples to vote on a new label. K-means uses <strong>K centres</strong> to form unlabelled groups. They may both use distances, but their inputs and goals are different.</p>
'''),
4:('4 → 5 · Decide what your features actually are', '''
<p>Consider three different tasks. An ID3 tree answers a question from <em>categorical labelled</em> examples; K-means groups <em>unlabelled</em> coordinates; k-NN votes with <em>labelled</em> neighbours. Merely plotting points does not tell us which of these is appropriate.</p>
<div class="transfer-worked"><strong>Read the evidence, not just the headline percentage</strong><p>Suppose a six-case classifier has <code>TP=2</code>, <code>TN=2</code>, <code>FP=1</code>, and <code>FN=1</code>. The accuracy is <code>(2+2)/(2+2+1+1)=4/6 ≈ 66.7%</code>. Precision for the positive class is <code>2/(2+1)=2/3</code>; recall is also <code>2/(2+1)=2/3</code>.</p>
<details><summary>Why isn't “66.7% accuracy” enough?</summary><p>It comes from just six cases; it does not establish performance on other samples. The confusion counts identify what types of errors occurred, while a percentage alone conceals them.</p></details></div>
<p>Next, suppose the input is a 5×5 grayscale image. The features are the <strong>25 pixel values</strong>, not a label such as “handwriting” supplied by the computer. <a href="/w5/course/#cv-question">Week 5 first investigates image representation and transformations</a>; later, Week 8 actually evaluates a learned digit classifier.</p>
'''),
5:('5 → 6 · A pixel transformation is not a trained classifier', '''
<p>A threshold is a rule written directly by the programmer. For a grayscale value <code>v</code> and threshold <code>T=128</code>, the result is black (0) when <code>v &lt; 128</code>, otherwise white (255). This transformation operates on each intensity even if no training labels exist.</p>
<div class="transfer-worked"><strong>Predict the boundary exactly</strong><p>Apply the threshold to <code>[30, 100, 127, 128, 220, 255]</code>. You should obtain <code>[0, 0, 0, 255, 255, 255]</code>. The value 128 itself becomes white, because the rule uses strict <code>&lt;</code>, not <code>≤</code>.</p>
<details><summary>What information was lost?</summary><p>Values 30, 100 and 127 are now indistinguishable. Removing apparent background may help readability, but the same threshold could erase faint writing. We must compare to a specified purpose, not call the output universally better.</p></details></div>
<p>A later <em>classifier</em> can receive pixel values as inputs and learn weights from labelled examples. That differs from applying an explicitly chosen pixel threshold. In <a href="/w6/course/#p-question">Week 6</a> we study one simple trainable model, the perceptron, using just two inputs so every weight is visible.</p>
'''),
6:('6 → 7 · Why one straight line is not enough', '''
<p>The AND model with <code>w₁=1</code>, <code>w₂=1</code> and <code>b=−1.5</code> produces weighted sums <code>−1.5, −0.5, −0.5, 0.5</code> for inputs <code>(0,0), (0,1), (1,0), (1,1)</code>. With the convention <code>step(z)=1</code> when <code>z≥0</code>, the predictions are <code>0,0,0,1</code>.</p>
<div class="transfer-worked"><strong>Compare AND with XOR</strong><p>XOR instead requires <code>0,1,1,0</code> on the same four inputs. One line cannot isolate the two opposite positive corners from the two opposite negative corners, so no single two-input threshold perceptron represents all four XOR labels correctly.</p>
<details><summary>Why not just train the perceptron longer?</summary><p>Changing weights still produces a linear boundary. The limitation is the model's expressive form, not simply insufficient training steps. A hidden layer can combine multiple line-like decisions into a nonlinear overall rule.</p></details></div>
<p><a href="/w7/course/#n-forward">Week 7</a> demonstrates XOR using hidden neurons. Its first example uses <strong>manually supplied weights</strong> to establish representation; a separate smooth-neuron example demonstrates <strong>learning by gradient descent</strong>.</p>
'''),
7:('7 → 8 · Tracing a network is not measuring its accuracy', '''
<p>For the hand-constructed XOR network, input <code>(1,1)</code> activates the OR hidden neuron and the AND hidden neuron. The output sum is <code>1 − 2·1 − 0.5 = −1.5</code>, hence its threshold output is <code>0</code>, as XOR requires. Those XOR weights were <strong>given</strong> to the model; this calculation is a forward pass, not evidence that gradient descent learned XOR.</p>
<div class="transfer-worked"><strong>Trace one genuine gradient step in the separate example</strong><p>For a sigmoid neuron with input <code>x=1</code>, target <code>t=1</code>, initial <code>w=b=0</code>, the prediction is <code>0.5</code>, squared loss <code>½(1−0.5)²=0.125</code> and gradient <code>−0.125</code>. With learning rate <code>η=0.4</code>, update <code>w←0−0.4(−0.125)=0.05</code>.</p>
<details><summary>Does decreasing that loss prove the model can read handwriting?</summary><p>No. It demonstrates a change on one artificial training example. Digit recognition needs labelled image data, a defined model and predictions on examples kept separate from training. <a href="/w8/course/">Week 8</a> tests a real k-NN digit classifier and inspects misclassified examples.</p></details></div>
<p><strong>Transfer question:</strong> if an image is 8×8 grayscale, how many pixel features describe it? Answer: 64. A correct digit label is an additional target, not one of those 64 pixel features.</p>
''')
}
LAB={
1:('Prepare for ID3', 'Use any six hypothetical yes/no choices and write a frequency table. Then make another choice that divides them into subgroups. Record group sizes and yes/no counts; you do not need to calculate entropy yet.', 'A labelled table, counts for each subgroup, and one sentence explaining why a pure group is easy to predict.'),
2:('Prepare for K-means','Copy the outdoor-activity data without the Go? column. State whether ID3 can still learn the same yes/no target; then propose a purely descriptive grouping task instead.','The missing target identified explicitly, a possible similarity rule, and one limitation of the resulting groups.'),
3:('Prepare for the comparison week','For the five delivery points, write down both updated centroids and calculate the 19/6 squared-error total. Then explain why you cannot report label accuracy without true labels.','The two means, the 8/3 + 1/2 calculation, and an explicit distinction between clustering error and classification accuracy.'),
4:('Prepare for computer vision','Imagine replacing a 2D coordinate with the 25 numbers of a 5×5 grayscale image. Identify which are observed features and what extra information would be required for a supervised handwriting classifier.','Feature count 25, an example target label, and one way to keep test images separate from training.'),
5:('Prepare for perceptrons','Apply a threshold at 128 to six input values: 30, 100, 127, 128, 220, 255. Compare this fixed transformation with a hypothetical classifier that learns from labelled images.','The six transformed values, the boundary convention, and a sentence distinguishing hand-written rules from trained weights.'),
6:('Prepare for neural networks','Trace AND and XOR on all four binary inputs. Identify all three cases where the displayed AND perceptron disagrees with XOR, then explain why no single straight-line boundary can classify all four XOR cases correctly.','An explicit four-row truth table, three mismatch cases, and a boundary-shape explanation.'),
7:('Prepare for the digit-classifier evaluation','Run the XOR forward pass and the separate one-weight training step in the starter notebook. Predict what additional evidence a 64-pixel digit classifier would need before claiming accuracy.','One supplied-weight trace, the observed +0.05 gradient update, and a proposed held-out test with correct/incorrect counts.')
}
HOMEWORK={
1:('A six-row labelled observation table plus one subgroup count; explain why your conditional die calculation does not establish real-classroom frequencies.'),
2:('The original labelled example, your cloudy-subset Wind gain (1 bit) and one paragraph on why removing labels changes the task.'),
3:('The A–E cluster assignments, both updated means, the total squared error 19/6 and a sentence contrasting K-means with k-NN.'),
4:('A confusion table with TP=2, TN=2, FP=1, FN=1, the 4/6 score and an example of 25 pixel features versus a supervised label.'),
5:('A six-value threshold trace with the 128 boundary identified, plus one plausible failure mode (for example faint writing disappearing).'),
6:('A four-row AND/XOR comparison, your perceptron weighted sums and the reason one linear separator cannot represent XOR.'),
7:('A supplied XOR forward-pass trace, the separate sigmoid update from 0 to +0.05, and a held-out evaluation plan for an 8×8 digit classifier.')
}
def section(week,kind):
 if kind=="course":
    title,body=COURSE[week]
    return (f'<section class="chapter-section learning-transfer" id="learning-transfer-w{week}">'
            f'<p class="transfer-kicker">Concept transfer · Week {week} to Week {week+1}</p>'
            f'<h2>{title}</h2>{body}</section>')
 if kind=="lab":
    title,task,evidence=LAB[week]
    return (f'<section class="lab-step learning-transfer" id="learning-transfer-lab-w{week}">'
            '<p class="transfer-kicker">Last 5 minutes · Transfer ticket</p>'
            f'<h2>{title}</h2><p>{task}</p>'
            f'<p class="transfer-evidence"><strong>Carry forward:</strong> {evidence}</p>'
            f'<p><a href="/w{week}/course/#learning-transfer-w{week}">Review the worked connection</a> '
            f'· <a href="/w{week+1}/course/">Preview the next course</a></p></section>')
 if kind=="homework":
    return (f'<section class="learning-transfer transfer-homework" id="learning-transfer-homework-w{week}">'
            '<p class="transfer-kicker">Evidence and reproducibility</p>'
            '<h2>What a reviewer should be able to reproduce</h2>'
            f'<p>{HOMEWORK[week]}</p>'
            '<p>Record your input, calculation or code, output, and one limitation. '
            'Do not hand in only a screenshot or percentage without the data that produced it. '
            f'<a href="/w{week}/lab/#learning-transfer-lab-w{week}">See the laboratory transfer ticket</a>.</p>'
            '</section>')
 raise ValueError(kind)
def insert(path,week,kind,anchor):
 text=path.read_text(encoding="utf-8")
 marker=f'id="learning-transfer-{"lab-" if kind=="lab" else "homework-" if kind=="homework" else ""}w{week}"'
 if marker in text:
    print("Already there",path.relative_to(ROOT));return
 if text.count(anchor)!=1:
    raise ValueError(f"{path}: expected one anchor {anchor!r}, got {text.count(anchor)}")
 text=text.replace(anchor,section(week,kind)+'\n'+anchor,1)
 if kind=="course" and week==1:
    needle='<li><a href="#five">1.5. Distributions and expected value</a></li>'
    assert text.count(needle)==1
    text=text.replace(needle,needle+f'\n<li><a href="#learning-transfer-w{week}">From probability to supervised learning</a></li>',1)
 tag='<link rel="stylesheet" href="/assets/learning-transfers.css">'
 if week==1 and tag not in text:text=text.replace('</head>',tag+'</head>',1)
 path.write_text(text,encoding="utf-8")
 print("Inserted",path.relative_to(ROOT))
for week in range(1,8):
 for kind in ("course","lab","homework"):
    if week==1:path=ROOT/f"w1/{kind}/index.html"
    else:path=ROOT/("data/week23" if week in (2,3) else "data/week47")/f"w{week}_{kind}.html"
    if kind=="lab":
        text=path.read_text(encoding="utf-8")
        # The lab has a submission section; it is a natural final teaching checkpoint.
        candidates=['<section id="submission"','<section class="submission-drop" id="submission"',
                    '<section id="submission" class="submission-drop"']
        matches=[c for c in candidates if c in text]
        if not matches:raise ValueError(f"No submission anchor in {path}")
        anchor=matches[0]
    else:
        text=path.read_text(encoding="utf-8")
        match=re.search(r'<section(?=[^>]*class="[^"]*page-bibliography)[^>]*>',text)
        if not match:raise ValueError(f"No bibliography in {path}")
        anchor=match.group(0)
    insert(path,week,kind,anchor)
print("All 21 learning-transfer sections built")

# The new course section must also be discoverable in the on-page table of contents.
for week in range(2,8):
    path=ROOT/("data/week23" if week in (2,3) else "data/week47")/f"w{week}_course.html"
    text=path.read_text(encoding="utf-8")
    href=f'href="#learning-transfer-w{week}"'
    if href in text:continue
    assert 'class="course-sidebar"' in text and '</ul>' in text
    entry=f'<li><a {href}>Transfer to Week {week+1}</a></li>'
    text=text.replace('</ul>',entry+'</ul>',1)
    path.write_text(text,encoding="utf-8")
    print("Updated course contents",week)

# Week 1's lab and homework have independent canonical fragment files. Keep
# those in sync, so update_week1_practice.py does not remove the transfer work.
for kind,source_name,anchor in [
    ("lab","week1_lab_active.html",'<section id="submission"'),
    ("homework","week1_probability_homework.html",'<section class="page-bibliography"')
]:
    published=(ROOT/f"w1/{kind}/index.html").read_text(encoding="utf-8")
    src=ROOT/"data"/source_name
    text=src.read_text(encoding="utf-8")
    section_id=f"learning-transfer-{'lab-' if kind=='lab' else 'homework-'}w1"
    if f'id="{section_id}"' not in text:
        match=re.search(
            rf'<section class="[^"]*learning-transfer[^"]*" id="{section_id}">.*?</section>',
            published,flags=re.S
        )
        if not match:raise ValueError(f"Missing published Week 1 {kind} transfer")
        if text.count(anchor)!=1:raise ValueError(f"Week 1 {kind} source anchor not unique")
        text=text.replace(anchor,match.group(0)+'\n'+anchor,1)
    if kind=="lab" and 'href="#learning-transfer-lab-w1"' not in text:
        text=text.replace('<li><a href="#submission">Submission</a></li>',
            '<li><a href="#learning-transfer-lab-w1">Transfer to Week 2</a></li>'
            '<li><a href="#submission">Submission</a></li>',1)
    src.write_text(text,encoding="utf-8")
    print("Synchronized canonical Week 1",kind)
# Laboratory transfer exercises are discoverable from each notebook TOC.
for week in range(2,8):
    path=ROOT/("data/week23" if week in (2,3) else "data/week47")/f"w{week}_lab.html"
    text=path.read_text(encoding="utf-8")
    href=f'href="#learning-transfer-lab-w{week}"'
    if href in text:continue
    assert '<aside class="course-sidebar"' in text and '</ul>' in text
    text=text.replace('</ul>',f'<li><a {href}>Transfer to Week {week+1}</a></li></ul>',1)
    path.write_text(text,encoding="utf-8")
    print("Updated lab contents",week)
