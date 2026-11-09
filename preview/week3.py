# Week 3: full worked ID3 proof-of-concept.
from pathlib import Path
R=Path(__file__).resolve().parent
experience="https://experience-ai.org/ro/units/foundations-of-ai-11-14"
ioai="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf"
pol="https://github.com/OlimpiadaAI/szkolenia"
interactive="https://interactiveml.org/tree"

course=r"""
<section class="summary"><h2>Course summary</h2>
<p>Decision trees make predictions by asking a sequence of questions. This lesson builds a categorical ID3 tree using eight training examples, rather than treating the algorithm as a black box. The key idea is <strong>information gain</strong>: at each node, choose the question that most reduces uncertainty about the target label. We then examine how a greedy algorithm constructs a tree and what perfect training accuracy does and does not establish.</p>
<p><strong>Outcomes:</strong> interpret nodes, edges and leaves; calculate binary entropy and weighted conditional entropy; compare information gain; manually build a small ID3 tree; trace predictions and identify an incomplete-training counterexample.</p>
<p class="understated">Teaching note: 20 minutes can introduce the worked root split; students can study the full derivation separately. Prior mathematical material is optional—only fractions and logarithms are introduced as needed.</p>
</section>
<nav class="toc"><strong>Contents</strong><ul>
<li><a href="#tree">3.1. What a decision tree computes</a></li>
<li><a href="#data">3.2. The complete training example</a></li>
<li><a href="#entropy">3.3. Entropy and information gain</a></li>
<li><a href="#id3">3.4. Building the ID3 tree</a></li>
<li><a href="#limits">3.5. Generalisation, ID3 and CART</a></li>
</ul></nav>

<section id="tree"><h2>3.1. What a decision tree computes</h2>
<p>A <strong>decision tree</strong> is a program whose internal nodes ask questions about an input, whose branches correspond to answers, and whose leaves produce decisions. For example: is the sky rainy? If yes, do not hold an outdoor demonstration. If no, another question might be needed.</p>
<p>In a hand-written rule system, the developer chooses the tree. In machine learning, a tree-building algorithm chooses questions from labelled training examples. The finished tree is still a simple program: the learning happened when the questions and leaves were selected.</p>
<pre><code>def predict_example(sky, wind, temperature):
    if sky == "rainy":
        return "no"
    if wind == "calm":
        return "yes"
    if temperature == "warm":
        return "yes"
    return "no"
</code></pre>
<p>The program above will eventually be the <em>result</em> of our learning process; we have displayed it early to make clear what kind of object ID3 is trying to construct.</p>
<p class="source-line">Teaching sequence: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 4: Decision Trees</a> — distinguish a rule-based tree from a tree learned from data.</p>
</section>

<section id="data"><h2>3.2. The complete training example</h2>
<p>A school plans a fictional outdoor activity. Each past case has three categorical features: <em>sky</em> (sunny/rainy), <em>wind</em> (calm/windy), and <em>temperature</em> (warm/cold). The target label <em>go</em> means whether the activity should take place outdoors, according to our synthetic training examples.</p>
<table><caption>Table 3.1 — Eight labelled examples; every feature combination appears once</caption>
<thead><tr><th>#</th><th>Sky</th><th>Wind</th><th>Temperature</th><th>Go?</th></tr></thead><tbody>
<tr><td>1</td><td>sunny</td><td>calm</td><td>warm</td><td>yes</td></tr>
<tr><td>2</td><td>sunny</td><td>calm</td><td>cold</td><td>yes</td></tr>
<tr><td>3</td><td>sunny</td><td>windy</td><td>warm</td><td>yes</td></tr>
<tr><td>4</td><td>sunny</td><td>windy</td><td>cold</td><td>no</td></tr>
<tr><td>5</td><td>rainy</td><td>calm</td><td>warm</td><td>no</td></tr>
<tr><td>6</td><td>rainy</td><td>calm</td><td>cold</td><td>no</td></tr>
<tr><td>7</td><td>rainy</td><td>windy</td><td>warm</td><td>no</td></tr>
<tr><td>8</td><td>rainy</td><td>windy</td><td>cold</td><td>no</td></tr>
</tbody></table>
<p>We have three <em>yes</em> examples and five <em>no</em> examples. Our goal is to find the first question that separates these labels well. We will use the same table throughout the theory, interactive activity, Colab notebook and Advanced problem set.</p>
<p class="source-line">Relevant specification: <a href="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf">IOAI classical machine-learning syllabus, decision trees</a>. The eight-row dataset above is an original teaching example.</p>
</section>

<section id="entropy"><h2>3.3. Entropy and information gain</h2>
<h3>3.3.1. Measuring uncertainty</h3>
<p>If all examples in a group have the same label, we are certain which label should be predicted for that group. If the labels are evenly split, uncertainty is greater. A common numerical measure is <strong>Shannon entropy</strong>.</p>
<div class="math">H(Y) = − ∑ pᵢ log₂(pᵢ)</div>
<p>For two classes with proportions <em>p</em> and <em>1 − p</em>, entropy is zero when either class has proportion one, and equals one bit at 50:50. We define <em>0 log₂ 0 = 0</em>.</p>
<div class="example"><span class="example-title">Worked calculation A — Entropy of the complete dataset.</span>
<p>The class frequencies are 3/8 and 5/8. Therefore:</p>
<div class="math">H(Y) = −(3/8)log₂(3/8) − (5/8)log₂(5/8) ≈ 0.9544 bits.</div>
<p>The result is close to one bit because the dataset is relatively mixed.</p>
</div>
<h3>3.3.2. Information gain of a question</h3>
<p>To evaluate a candidate question, split the dataset into its possible answers, calculate the entropy of each subset, then average those entropies weighted by the number of examples. The decrease in entropy is the <strong>information gain</strong>.</p>
<div class="math">Gain(Y, X) = H(Y) − ∑<sub>v</sub> (|S<sub>v</sub>|/|S|) H(Y | X = v).</div>
<div class="example"><span class="example-title">Worked calculation B — Should the root ask about sky?</span>
<p>The four sunny examples contain three yes and one no, so their entropy is approximately 0.8113. The four rainy examples are all no, so their entropy is zero.</p>
<div class="math">H(Y | sky) = (4/8)(0.8113) + (4/8)(0) = 0.4056.</div>
<div class="math">Gain(Y, sky) = 0.9544 − 0.4056 = 0.5488 bits.</div>
<p>Asking about sky reduces uncertainty by approximately 0.5488 bits.</p></div>
<h3>3.3.3. Compare every candidate root</h3>
<p>Wind divides the data into a calm group containing two yes and two no, and a windy group containing one yes and three no. Their weighted entropy is approximately 0.9056, so the gain is only 0.0488 bits. Temperature produces the same result.</p>
<table><caption>Table 3.2 — Candidate root questions</caption><thead><tr><th>Question</th><th>Weighted entropy after split</th><th>Gain</th></tr></thead><tbody>
<tr><td>Sky</td><td>0.4056</td><td><strong>0.5488</strong></td></tr>
<tr><td>Wind</td><td>0.9056</td><td>0.0488</td></tr>
<tr><td>Temperature</td><td>0.9056</td><td>0.0488</td></tr></tbody></table>
<p>We choose <strong>sky</strong> because its information gain is largest. The next question is chosen again, but only within the remaining impure branch.</p>
<p class="source-line">Further explanation: <a href="https://github.com/OlimpiadaAI/szkolenia">Polish AI Olympiad training</a> · <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI: decision trees</a>.</p>
</section>

<section id="id3"><h2>3.4. Constructing the ID3 tree</h2>
<h3>3.4.1. The recursive idea</h3>
<ol><li>If a node contains only one label, stop and create a leaf.</li>
<li>Otherwise calculate the gain of each unused categorical feature.</li>
<li>Choose the feature with the highest gain.</li>
<li>Create one branch for each observed value of that feature, and repeat.</li>
<li>If no features remain, use the majority label.</li></ol>
<p>This is a greedy algorithm: it makes the best immediate split according to its local criterion, not an exhaustive search over all possible trees.</p>
<h3>3.4.2. Continue the sunny branch</h3>
<p>The rainy branch already contains only no answers. The sunny branch still contains three yes and one no, entropy 0.8113. Within this subset, splitting by wind gives a calm group containing two yes answers, and a windy group containing one yes and one no. The weighted entropy is 0.5, so the gain is 0.3113 bits.</p>
<p>Temperature gives the same gain. With the fixed feature order (sky, wind, temperature), we choose wind in a tie. The calm branch becomes a yes leaf. For sunny and windy cases, temperature distinguishes warm → yes from cold → no.</p>
<figure class="figure">
<svg viewBox="0 0 705 355" role="img" aria-label="The learned ID3 tree first tests sky. Rainy leads to no. Sunny tests wind. Calm leads to yes. Windy tests temperature: warm means yes, cold means no.">
<g stroke="#777" fill="none" stroke-width="1.5">
<path d="M351 70 L162 135"/><path d="M351 70 L505 135"/>
<path d="M505 190 L405 250"/><path d="M505 190 L590 250"/>
<path d="M590 294 L520 325"/><path d="M590 294 L663 325"/>
</g>
<g font-family="Georgia,serif" text-anchor="middle" fill="#222">
<rect x="293" y="25" width="116" height="45" fill="#fff" stroke="#777"/><text x="351" y="52" font-size="17">Sky?</text>
<text x="230" y="100" font-size="13" fill="#666">rainy</text><text x="448" y="100" font-size="13" fill="#666">sunny</text>
<rect x="109" y="135" width="106" height="45" fill="#fff" stroke="#777"/><text x="162" y="163" font-size="16">No</text>
<rect x="446" y="145" width="118" height="45" fill="#fff" stroke="#777"/><text x="505" y="172" font-size="16">Wind?</text>
<text x="426" y="216" font-size="13" fill="#666">calm</text><text x="560" y="216" font-size="13" fill="#666">windy</text>
<rect x="352" y="250" width="106" height="45" fill="#fff" stroke="#777"/><text x="405" y="279" font-size="16">Yes</text>
<rect x="528" y="250" width="125" height="45" fill="#fff" stroke="#777"/><text x="590" y="279" font-size="15">Temperature?</text>
<text x="525" y="312" font-size="12" fill="#666">warm</text><text x="663" y="312" font-size="12" fill="#666">cold</text>
<text x="510" y="346" font-size="16">Yes</text><text x="663" y="346" font-size="16">No</text>
</g></svg>
<figcaption>Figure 3.1 — One complete tree consistent with all eight examples. There are three internal question nodes.</figcaption>
</figure>
<p class="lab-note">The diagram is a static representation of the result. The <a href="/preview/w3/lab/">Laboratory</a> contains a clickable information-gain demonstration and the full runnable ID3 implementation.</p>
</section>

<section id="limits"><h2>3.5. Generalisation, stopping and other tree algorithms</h2>
<h3>3.5.1. Perfect training fit is not a guarantee</h3>
<p>The tree classifies every row in Table 3.1 correctly. But imagine we had not observed the sunny/windy/cold case. A different tree might still fit all the remaining examples while giving an incorrect answer for that unseen combination. This is not a bug in Python; it is a limitation of what the supplied data can establish.</p>
<h3>3.5.2. ID3 is not the same thing as CART</h3>
<p>Classical ID3 chooses categorical tests using information gain and can create a branch for each category. The interactive tree demonstration used in the lab visualises <strong>CART</strong>, which commonly makes binary splits and can handle numerical thresholds. The shared intuition—reducing disorder—is valuable, but we should not claim the two implementations are identical.</p>
<h3>3.5.3. How to avoid misleading conclusions</h3>
<p>Large trees may fit noise, and the best greedy split is not necessarily part of the smallest possible global tree. In Week 4 we will introduce evaluation on held-out examples, error tables and the distinction between fitting and generalising.</p>
<p class="source-line">Bibliography: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 4</a> · <a href="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf">IOAI syllabus</a> · <a href="https://interactiveml.org/tree">Interactive CART visualisation</a>.</p>
</section>
"""
page(3,"course","Decision trees and information gain","From a labelled table to a complete categorical ID3 tree, step by step.",course)

lab=r"""
<section><h2>Laboratory objectives</h2>
<p>Compare feature questions using information gain, distinguish the interactive CART demonstration from categorical ID3, and implement a small decision tree in Python without hiding the algorithm behind a library call.</p>
<p class="understated">Suggested hour: 8 min paper prediction · 12 min interactive · 23 min Colab · 12 min modification · 5 min conclusion.</p></section>
<section class="lab-step"><h2>1. Predict — before using a computer</h2>
<p>From the eight-row table in the <a href="/preview/w3/course/">Course</a>, count the number of yes/no answers. Guess which of sky, wind and temperature should be the first question and justify the guess using the labels.</p>
<p>Do not calculate every logarithm immediately. First describe what it means for a split to make a subset pure.</p>
</section>
<section class="lab-step">
<h2>2. Experiment — information gain</h2>
<p>The exercise below uses the <em>same</em> eight records from the Course. Select a candidate first question. The entropy and information gain are recalculated locally in your browser; no data is sent to a server.</p>
<div class="interactive" data-id3-explorer>
<fieldset><label for="attribute">Choose the first question</label>
<select id="attribute" data-id3-feature><option value="sky">Sky</option><option value="wind">Wind</option><option value="temperature">Temperature</option></select></fieldset>
<button type="button" data-id3-compute>Calculate information gain</button>
<output data-id3-result aria-live="polite">Select a feature and calculate its gain.</output>
<div data-id3-detail class="mini"></div>
</div>
<p>Then compare the result with a visual tree-building app. This external app illustrates <strong>CART</strong> rather than the categorical ID3 procedure we are calculating here.</p>
<p class="launch"><a href="https://interactiveml.org/tree" target="_blank" rel="noopener noreferrer">Launch interactive decision-tree visualiser ↗</a></p>
<p class="source-line">Teaching source: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 4 — Decision Trees</a>.</p>
</section>
<section class="lab-step"><h2>3. Inspect — your ID3 notebook</h2>
<p>Open the Colab notebook and compare its output against the hand calculations. The implementation uses ordinary Python dictionaries, counting, logarithms and recursion. It does not require scikit-learn or any verification software.</p>
<p><a href="https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/preview/w3/lab/starter.ipynb" target="_blank" rel="noopener noreferrer">Open ID3 notebook in Google Colab ↗</a> · <a href="starter.ipynb" download>Download notebook (.ipynb)</a></p>
<div class="notebook-placeholder"></div>
<ol><li>Compute and display the three candidate gains.</li><li>Run the tree-building function and inspect the nested dictionary.</li><li>Predict all eight rows and check the result.</li><li>Remove one record; predict the excluded combination. Explain why a mistake is possible even with perfect training accuracy.</li></ol>
</section>
<section><h2>4. Reflection</h2>
<p>Why does ID3 terminate immediately when a node contains only one class? What can happen if a training example is missing? Which parts of the tree were chosen by data rather than by a human writing the final rules?</p>
<p><strong>Exit ticket:</strong> Explain why sky is chosen as the root and give one reason the resulting model could still fail on new observations.</p></section>
"""
lab=lab.replace('<div class="notebook-placeholder"></div>',code_preview(3))
lab+='<script src="/preview/assets/experiment.js" defer></script>'
page(3,"lab","A decision tree built from data","Predict a split, calculate information gain, then build and test categorical ID3 in Colab.",lab)

hw=r"""
<p class="assignment-meta">Version 2026–2027 · Individual work · Adapt the Week 3 ID3 implementation</p>
<section><h2>Context</h2>
<p>A student club has to decide whether an equipment demonstration should be held in a courtyard or inside. Its archive contains examples with three categorical observations: sky (sunny/cloudy/rainy), wind (calm/windy) and temperature (warm/cold). Historical decisions were recorded as <strong>yes</strong> (outdoors) or <strong>no</strong> (indoors).</p>
<p>This is synthetic training data for an algorithm exercise, not a real outdoor-safety decision system.</p>
<p>Resources: <a href="/preview/w3/course/">Course</a> · <a href="/preview/w3/lab/">Laboratory</a> · <a href="/preview/w3/lab/starter.ipynb">Starter ID3 notebook</a> · <a href="club-events.csv" download>Club events dataset (12 records)</a>.</p><details class="notebook-preview"><summary>Provided Colab code: load the new dataset</summary><pre><code>from google.colab import files
files.upload()  # Upload club-events.csv
import csv
with open("club-events.csv", newline="") as f:
    all_rows = list(csv.DictReader(f))
# Next: reserve rows 4, 7 and 11; fit ID3 on the other rows.
</code></pre></details></section>
<section><h2>Mandatory <span class="point-value">(1p)</span></h2>
<ol><li>Load the new <a href="club-events.csv">dataset</a> into the ID3 notebook without changing the original algorithm.</li>
<li>Reserve the records with numbers <strong>4, 7 and 11</strong> for evaluation. Do not train on those three records.</li>
<li>Calculate the root information gains on the nine training records and select the best question.</li>
<li>Draw the learned tree, predict the three held-out answers, and report how many were correct.</li></ol></section>
<hr>
<section><h2>Homework <span class="point-value">(2p)</span></h2>
<ol><li>Add a function that prints the <em>decision path</em> for one prediction (for example, <code>sky = cloudy → wind = calm → yes</code>).</li>
<li>Handle an unseen category such as <code>sky = foggy</code> by reporting the fallback label and an explicit warning.</li>
<li>Compare the root question with the question chosen by a simple human rule. Explain whether both approaches give the same predictions on the evaluation records.</li>
<li>Include an explanation of one limitation of training on such a small dataset.</li></ol></section>
<hr>
<section><h2>Advanced — optional reading</h2>
<p><a href="/preview/w3/advanced/">Open the ID3 reasoning problem sheet</a>: minimal trees, irrelevant attributes, missing combinations, and why a learned tree is only as justified as the information available. No formal verifier is needed.</p></section>
<section class="submission"><h2>Submission</h2><p>Submit the modified Colab notebook or <code>.ipynb</code> file, a labelled tree diagram, and a short results table. GitHub remains optional until the engineering part of the course.</p></section>
"""
page(3,"homework","Assignment 03 — An explainable event planner","Transfer the ID3 algorithm to a new categorical dataset and trace its decisions.",hw)

adv=r"""
<section><h2>Algorithmic reasoning exercises</h2>
<p>A small A4 exercise sheet inspired by the progression of Ciortuz's ID3 problems: start with a worked calculation; build a tree; justify a minimality claim; study an irrelevant attribute; and construct a counterexample using an incomplete training set.</p>
<p>Everything can be solved using an eight-row table, elementary calculations and pseudocode. Python is permitted only as a way to check a calculation or enumerate the finite cases.</p>
<p><a href="week-03-id3.pdf">Read exercise sheet (PDF)</a> · <a href="week-03-id3.tex">LaTeX source</a> · <a href="print.html">Accessible print version</a>.</p>
<iframe class="pdf-view" title="Week 3 advanced ID3 reasoning exercise PDF" src="week-03-id3.pdf"></iframe></section>
<section><h2>Connection with the course</h2>
<p>The Course teaches <em>how</em> ID3 picks a split; the Advanced questions ask <em>why</em> that choice works on this dataset and which stronger conclusions cannot be deduced from training accuracy alone. Reasoning—not installation or formal-verification tooling—is the objective.</p>
<p class="source-line">Study reference: <a href="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf">IOAI Decision Tree topics</a> · <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 4</a>.</p></section>
"""
page(3,"advanced","Advanced 03 — The structure of an ID3 tree","Worked examples, minimality arguments and counterexamples.",adv)
rows=["sky,wind,temperature,go"]
for sky in ("sunny","cloudy","rainy"):
    for wind in ("calm","windy"):
        for temp in ("warm","cold"):
            yes=(sky=="sunny") or (sky=="cloudy" and wind=="calm")
            rows.append(",".join((sky,wind,temp,"yes" if yes else "no")))
(R/"w3/homework/club-events.csv").write_text("\n".join(rows)+"\n",encoding="utf-8")
