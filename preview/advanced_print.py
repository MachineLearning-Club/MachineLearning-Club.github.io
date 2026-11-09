"""Print-first advanced sheets (HTML and PDF), each paired with editable LaTeX source."""
from pathlib import Path
R=Path(__file__).resolve().parent
def sheet(n,title,subtitle,text):
    head='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Advanced sheet · Week '''+str(n)+'''</title>
<link rel="stylesheet" href="/preview/assets/poc.css">
</head><body class="printpage"><header class="site print-controls">
<a href="/preview/w'''+str(n)+'''/advanced/">← Advanced page</a> ·
<a href="week-'''+str(n).zfill(2)+('-reasoning.pdf' if n==1 else '-id3.pdf')+'''">PDF</a></header>
<main><p class="eyebrow">Machine Learning Club · Advanced Exercises · Week '''+str(n)+'''</p>
<h1>'''+title+'''</h1><p>'''+subtitle+'''</p>
<hr>
'''
    tail='''<footer class="site">Machine Learning Club · Seven Hills International School · November 2026</footer>
</main></body></html>'''
    (R/f'w{n}/advanced/print.html').write_text(head+text+tail,encoding='utf-8')

sheet(1,"What can examples actually prove?",
      "Progressive reasoning about generalisation, alternative rules and missing observations.",
r"""
<section><h2>Preliminaries and notation</h2>
<p>Let an input be a pair of Boolean features <em>x</em>, <em>y</em> (each is either 0 or 1). A classifier returns a Boolean label 0 or 1. A <strong>training sample</strong> is a finite collection of labelled inputs. A classifier is <strong>consistent</strong> with a sample if it gives the supplied label on every observed input.</p>
<p>We make no assumptions about the classifier's behaviour on inputs missing from the sample. Ordinary truth tables and pseudocode are sufficient to solve every problem.</p></section>

<section class="problem"><h2>Worked Example A — Two perfect models</h2>
<p>Consider the observed examples <strong>(0,0) → 0</strong> and <strong>(1,1) → 1</strong>. Two proposed classifiers are</p>
<pre><code>def model_a(x, y): return x
def model_b(x, y): return y
</code></pre>
<p>Both are correct on every available training example. Evaluate both on the entire finite input space:</p>
<table><thead><tr><th>x</th><th>y</th><th>model_a</th><th>model_b</th><th>Training example?</th></tr></thead>
<tbody><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>yes</td></tr>
<tr><td>0</td><td>1</td><td>0</td><td>1</td><td>no</td></tr>
<tr><td>1</td><td>0</td><td>1</td><td>0</td><td>no</td></tr>
<tr><td>1</td><td>1</td><td>1</td><td>1</td><td>yes</td></tr></tbody></table>
<div class="worked"><p><strong>Solution and conclusion.</strong> Both models have 100% training accuracy. However, they disagree on two unseen inputs. Therefore perfect agreement with the training data does <strong>not</strong> logically determine the true classifier outside the observed sample.</p></div></section>

<section class="problem"><h2>Problem 1 — How many models are possible?</h2>
<p>A binary classifier is allowed to choose independently between labels 0 and 1 on each of the four possible inputs. The labels of (0,0) and (1,1) are fixed by the training sample above.</p>
<ol type="a"><li>How many different classifiers remain consistent with the two observations?</li>
<li>Explain your count without enumerating all 16 possible classifiers.</li>
<li>What happens if one of the two unobserved cases is also labelled?</li></ol>
<div class="worked"><p><strong>Selected solution.</strong> Two inputs remain unobserved. Each may independently receive 0 or 1; hence there are 2 × 2 = <strong>4</strong> consistent classifiers. One additional correctly labelled distinct input leaves one unobserved case and thus <strong>2</strong> consistent classifiers. This counting argument assumes there are no other restrictions on the class of possible models.</p></div></section>

<section class="problem"><h2>Problem 2 — The smallest distinguishing example</h2>
<p>Assume the only possible true classifiers are model_a and model_b from Worked Example A.</p>
<ol type="a"><li>Choose one unobserved input that distinguishes the two hypotheses.</li>
<li>Explain how learning its correct label lets you reject one of the two hypotheses.</li>
<li>Why would a single such example <em>not</em> establish correctness if many other hypotheses were possible?</li></ol>
<p class="understated"><strong>Hint:</strong> Look for a row in the truth table with unequal predictions.</p></section>

<section class="problem"><h2>Problem 3 — An irrelevant feature</h2>
<p>Add another Boolean input <em>z</em>, but suppose the real output is still determined solely by <em>x</em> and <em>y</em>.</p>
<ol type="a"><li>Give two records with different z values and identical x and y. What can you conclude about their labels?</li>
<li>A decision tree unnecessarily asks about z. Explain how a tree computing a function independent of z can be simplified to avoid tests of z.</li>
<li>Why might training data that are incomplete make a learner incorrectly conclude that z is important?</li></ol>
<p class="understated"><strong>Hint:</strong> For a truly irrelevant feature, changing only that feature cannot change the correct output.</p></section>

<section class="problem"><h2>Problem 4 — Generalisation requires an assumption</h2>
<p>Suppose a learner has seen every input except one, denoted <em>u</em>, and must now predict its label.</p>
<ol type="a"><li>Construct two target functions that give exactly the same labels on all observed inputs but opposite labels at u.</li>
<li>Use this construction to explain why no deterministic learner can be guaranteed to predict the label of every unseen u correctly without assumptions about the target function.</li>
<li>Give a practical example of an additional assumption that could make learning useful.</li></ol>
<p class="understated"><strong>Hint:</strong> Start from any proposed target function and flip its value only at u.</p></section>

<section><h2>Observations for further study</h2>
<p>A model is neither automatically wrong nor automatically reliable because some inputs were omitted. Generalisation becomes possible when we make useful assumptions: similar inputs often have related labels, the training data are representative, and the feature representation captures information relevant to the target. These are assumptions to investigate, not logical consequences of perfect training accuracy.</p>
<p>For additional practice: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI — Bias in, bias out</a>. Optional computational assistance: enumerate the four inputs in Python and compare the two models.</p></section>
""")

sheet(3,"Constructing and questioning an ID3 tree",
      "Worked entropy calculation, minimality, irrelevant attributes and unseen-case counterexamples.",
r"""
<section><h2>Preliminaries</h2>
<p>A categorical decision tree asks feature-value questions and returns a class label at a leaf. Its <strong>size</strong> will mean the number of internal decision nodes (questions), not the total number of nodes. We work with the same eight synthetic outdoor-activity examples as in Week 3 Course and Laboratory.</p>
<table><thead><tr><th>#</th><th>Sky</th><th>Wind</th><th>Temp.</th><th>Go?</th></tr></thead><tbody>
<tr><td>1</td><td>sunny</td><td>calm</td><td>warm</td><td>yes</td></tr>
<tr><td>2</td><td>sunny</td><td>calm</td><td>cold</td><td>yes</td></tr>
<tr><td>3</td><td>sunny</td><td>windy</td><td>warm</td><td>yes</td></tr>
<tr><td>4</td><td>sunny</td><td>windy</td><td>cold</td><td>no</td></tr>
<tr><td>5–8</td><td>rainy</td><td>both</td><td>both</td><td>no</td></tr>
</tbody></table>
<p>The final row stands for all four combinations of wind and temperature when sky is rainy. The dataset contains three yes and five no labels. Use the convention 0 log₂ 0 = 0.</p></section>

<section class="problem"><h2>Worked Example A — Choose the root question</h2>
<p>Entropy with probabilities pᵢ is H = −Σ pᵢ log₂ pᵢ. Information gain is the parent entropy minus the average entropy of the subsets created by a question.</p>
<div class="math">H(root) = −(3/8)log₂(3/8) − (5/8)log₂(5/8) ≈ 0.9544.</div>
<p>Splitting on sky gives four sunny cases (three yes, one no) and four rainy cases (all no). Therefore</p>
<div class="math">H(after sky) = (4/8)·0.8113 + (4/8)·0 = 0.4056.</div>
<div class="math">Gain(sky) = 0.9544 − 0.4056 = <strong>0.5488 bits.</strong></div>
<p>This is the best candidate root. In Problem 1, you must also justify why both alternatives are weaker.</p></section>

<section class="problem"><h2>Problem 1 — Compare candidate questions</h2>
<ol type="a"><li>For wind = calm and wind = windy, count the yes and no labels.</li>
<li>Calculate the entropy of both groups and the weighted entropy after splitting on wind.</li>
<li>Repeat for temperature = warm/cold, then compare all three information gains.</li></ol>
<div class="worked"><p><strong>Selected result.</strong> For wind, the two subsets contain (2 yes, 2 no) and (1 yes, 3 no). The weighted entropy is (1 + 0.8113)/2 = 0.9056, so the gain is approximately <strong>0.0488</strong>. Temperature has the same count distribution and gain. The sky gain 0.5488 is strictly larger.</p></div>
</section>

<section class="problem"><h2>Problem 2 — Finish the tree</h2>
<ol type="a"><li>Explain why the rainy branch can immediately become a no leaf.</li>
<li>Within the sunny branch, calculate the gain of wind and temperature.</li>
<li>If a tie is resolved in favour of wind, draw the complete tree.</li>
<li>Trace all eight training examples through it and count the decision nodes.</li></ol>
<p class="understated"><strong>Hint:</strong> The entropy of the sunny branch is about 0.8113. Splitting it on wind leaves a pure two-example group and a mixed two-example group, resulting in remaining entropy 0.5.</p>
<div class="worked"><p><strong>Selected result.</strong> Gain within the sunny branch is approximately 0.3113 for either remaining feature. One valid tree uses three internal decision nodes:</p>
<pre><code>if sky == "rainy": return "no"
if wind == "calm": return "yes"
if temperature == "warm": return "yes"
return "no"
</code></pre></div></section>

<section class="problem"><h2>Problem 3 — Is the tree minimal?</h2>
<p>Assume each internal node may ask only about one of sky, wind and temperature, and may branch on its observed categorical values.</p>
<ol type="a"><li>For each feature, find two records which differ only in that feature and have opposite labels.</li>
<li>Conclude that the target function genuinely depends on all three features.</li>
<li>Show that no tree with fewer than three internal decision nodes can represent the entire eight-row truth table exactly.</li></ol>
<div class="worked"><p><strong>Selected proof.</strong> Sky matters for fixed calm/cold: sunny→yes, rainy→no. Wind matters for sunny/cold: calm→yes, windy→no. Temperature matters for sunny/windy: warm→yes, cold→no. A tree with at most two decision nodes could ask about at most two distinct features, so at least one relevant feature could never influence its answer. It would be incorrect on a pair of the above witnesses. The construction in Problem 2 achieves three nodes, so <strong>three is necessary and sufficient.</strong></p></div></section>

<section class="problem page-break"><h2>Problem 4 — An irrelevant additional attribute</h2>
<p>Introduce a fourth Boolean feature, indoor-heating, but suppose it never affects the desired outdoor label once the other three features are known.</p>
<ol type="a"><li>Explain how a tree that unnecessarily branches on indoor-heating can be simplified without changing its prediction for any input.</li>
<li>Why does the claim require the feature to be truly irrelevant on the <em>entire input domain</em>, not merely on the observed examples?</li></ol>
<p class="understated"><strong>Hint:</strong> If the output is independent of this extra feature, replacing every test of it consistently by the same fixed branch preserves the target function.</p></section>

<section class="problem"><h2>Problem 5 — Incomplete data and a counterexample</h2>
<p>Remove only record 4 (sunny, windy, cold → no) from the training examples.</p>
<ol type="a"><li>Construct one tree consistent with all seven remaining rows that predicts no for the missing row.</li>
<li>Construct another tree consistent with the same seven rows that predicts yes for that row.</li>
<li>Explain why 100% training accuracy on seven examples is insufficient to choose between these models.</li></ol>
<p class="understated"><strong>Hint:</strong> The second tree may simply decide yes whenever sky is sunny. Every remaining sunny example has label yes.</p></section>

<section><h2>Final observation — Greedy is not globally optimal by definition</h2>
<p>ID3 chooses the feature with maximum information gain at the current node. Its definition does not compare every possible completed decision tree, so <strong>local gain does not by itself prove a globally minimum-size tree in general</strong>. In this particular eight-row example, however, Problem 3 provides a separate minimality proof.</p>
<p><strong>Optional computational assistant:</strong> Write a short Python loop to enumerate and compare the eight input combinations, but explain the minimality argument in words. The explanation itself is the essential result.</p>
<p>References: <a href="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf">IOAI classical-ML syllabus</a> · <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI — Decision Trees</a>.</p></section>
""")
print("Created print-friendly advanced pages.")
