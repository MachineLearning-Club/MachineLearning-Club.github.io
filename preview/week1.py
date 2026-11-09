# Week 1: complete proof-of-concept pages.
from pathlib import Path
R=Path(__file__).resolve().parent
def S(url,title,note=""):return source(url,title,note)
curr="https://experience-ai.org/ro/units/foundations-of-ai-11-14"
google="https://experiments.withgoogle.com/collection/ai"
quick="https://quickdraw.withgoogle.com/"
teachable="https://teachablemachine.withgoogle.com/"
cbse="https://cbseacademic.nic.in/web_material/Curriculum26/publication/srsec/AI_Student_HandbookXI.pdf"
pyml="https://www.pyml.ro/machine-learning-lectii-online-in-python.php"

course=r"""
<section class="summary">
<h2>Course summary</h2>
<p>A computer can perform intelligent-looking tasks by following rules written by a programmer, or by learning patterns from examples. This course explains the difference, introduces features and labels, and shows how a model turns training data into a prediction. The emphasis is not on the complexity of modern AI, but on understanding what an algorithm does and what its output can reasonably mean.</p>
<p><strong>By the end:</strong> distinguish rules from learned predictions; identify input features, training labels and output; explain training versus testing; recognise why a confident or correct-looking prediction may still be wrong.</p>
<p class="understated">Suggested class use: 15 minutes for the central ideas, then the Laboratory. This electronic course contains additional examples for independent reading.</p>
</section>
<nav class="toc" aria-label="Contents"><strong>Contents</strong>
<ul><li><a href="#one">1.1. Programs, rules and AI</a></li>
<li><a href="#two">1.2. Learning from examples</a></li>
<li><a href="#three">1.3. Training, prediction and testing</a></li>
<li><a href="#four">1.4. A complete small numerical model</a></li>
<li><a href="#five">1.5. Mistakes, confidence and responsibility</a></li></ul></nav>

<section id="one">
<h2>1.1. Programs, rules and AI</h2>
<p>Consider a program that switches on a light when the measured brightness falls below a fixed threshold. It may be useful, but the rule is explicitly supplied by its programmer. Nothing in the example requires the machine to learn from earlier observations.</p>
<pre><code>def turn_on_light(brightness):
    return brightness &lt; 300
</code></pre>
<p><span class="defined">Rule-based system:</span> a system whose decisions follow a set of conditions or procedures explicitly defined in advance. <span class="defined">Machine learning:</span> a family of methods that estimate useful patterns or parameters from data rather than requiring a separate programmer-written rule for every situation.</p>
<p>Artificial intelligence is a broader field. It also includes search, planning, reasoning, language technologies and approaches that may or may not involve learning. Consequently, not every automated system uses ML, and not every AI system is a neural network.</p>
<div class="example"><span class="example-title">Worked comparison.</span>
<ul><li><strong>Heating controller:</strong> switch on below 18°C — a fixed rule.</li>
<li><strong>Learned thermostat:</strong> estimate tomorrow's demand using past measurements — a prediction model.</li>
<li><strong>Route planner:</strong> search possible routes under constraints — planning, which does not automatically imply ML.</li></ul></div>
<p class="source-line">Read: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 1 — What is AI?</a> · <a href="https://cbseacademic.nic.in/web_material/Curriculum26/publication/srsec/AI_Student_HandbookXI.pdf">CBSE Class XI AI Handbook, introductory unit</a>.</p>
</section>

<section id="two">
<h2>1.2. Learning from examples</h2>
<p>A model is trained using examples. Each example contains information about the object or situation. In <span class="defined">supervised learning</span>, the examples also contain an answer, called the <span class="defined">target</span> or <span class="defined">label</span>. In classification, the model predicts a category; in regression, it predicts a numerical value.</p>
<h3>1.2.1. Features and labels</h3>
<p>Suppose a fictional sensor sorts two kinds of classroom demonstration objects. It measures two properties: size and reflectance, both on arbitrary numerical scales. A teacher labels each example as class A or B.</p>
<table><caption>Table 1.1 — Synthetic training examples</caption><thead><tr><th>Object</th><th>Size</th><th>Reflectance</th><th>Label</th></tr></thead>
<tbody><tr><td>1</td><td>2.0</td><td>2.0</td><td>A</td></tr><tr><td>2</td><td>2.0</td><td>3.0</td><td>A</td></tr><tr><td>3</td><td>3.0</td><td>2.0</td><td>A</td></tr><tr><td>4</td><td>7.0</td><td>7.0</td><td>B</td></tr><tr><td>5</td><td>7.0</td><td>8.0</td><td>B</td></tr><tr><td>6</td><td>8.0</td><td>7.0</td><td>B</td></tr></tbody></table>
<p>Here, <em>size</em> and <em>reflectance</em> are the features. The values A/B are training labels. The machine does not automatically understand the names: it only uses the information represented in the table.</p>
<h3>1.2.2. Three families of learning</h3>
<p><strong>Supervised learning:</strong> examples have target answers, such as A/B. <strong>Unsupervised learning:</strong> data have no supplied target categories, and the algorithm may instead discover groups. <strong>Reinforcement learning:</strong> an agent explores actions and learns from rewards or other feedback. These approaches solve different kinds of problems; they are not competing names for the same method.</p>
<p class="source-line">Read: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 2 — How computers learn</a> · <a href="https://www.pyml.ro/machine-learning-lectii-online-in-python.php">pyml.ro, Romanian Python and ML course</a>.</p>
</section>

<section id="three">
<h2>1.3. Training, prediction and testing</h2>
<p>We should keep three processes conceptually separate:</p>
<ol><li><strong>Training:</strong> compute a model from labelled examples.</li><li><strong>Inference:</strong> give the model a new input and obtain a predicted category.</li><li><strong>Testing:</strong> compare predictions with independent, known answers that were not used to fit the model.</li></ol>
<figure class="figure">
<svg viewBox="0 0 710 100" role="img" aria-label="Training examples lead to a trained model. A new example is supplied to the trained model, which produces a prediction.">
<rect x="5" y="22" width="158" height="54" rx="2" fill="white" stroke="#777"/><text x="84" y="42" text-anchor="middle" font-size="15">Labelled examples</text><text x="84" y="61" text-anchor="middle" font-size="12" fill="#555">Training data</text>
<path d="M170 49H242" stroke="#777" stroke-width="1.5"/><path d="M236 44l8 5-8 5" fill="none" stroke="#777"/>
<rect x="247" y="22" width="136" height="54" rx="2" fill="white" stroke="#777"/><text x="315" y="43" text-anchor="middle" font-size="15">Trained model</text><text x="315" y="61" text-anchor="middle" font-size="12" fill="#555">Learned pattern</text>
<path d="M390 49H463" stroke="#777" stroke-width="1.5"/><path d="M457 44l8 5-8 5" fill="none" stroke="#777"/>
<rect x="469" y="22" width="116" height="54" rx="2" fill="white" stroke="#777"/><text x="527" y="43" text-anchor="middle" font-size="15">Prediction</text><text x="527" y="61" text-anchor="middle" font-size="12" fill="#555">A or B</text>
<text x="315" y="12" text-anchor="middle" font-size="11" fill="#666">Training</text><text x="437" y="85" text-anchor="middle" font-size="11" fill="#666">New input →</text>
</svg><figcaption>Figure 1.1 — A simplified model-development pipeline. Training and inference are different steps.</figcaption>
</figure>
<p>If we test only on the training examples, the accuracy may look perfect even when the algorithm has memorised misleading details. A model may also learn from a biased selection of examples. For a classroom experiment, a separate test set and a short log of mistakes are more useful than a single impressive prediction.</p>
<p class="source-line">Read: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lessons 2–3 — How computers learn / Bias in, bias out</a>.</p>
</section>

<section id="four">
<h2>1.4. A complete small numerical model</h2>
<p>We will not attempt to reproduce the image model behind Quick, Draw! in the first session. Instead, we can train a tiny transparent classifier that makes the idea of a learned parameter visible.</p>
<h3>1.4.1. Learn class prototypes</h3>
<p>For each class, calculate the average of its feature values. The average pair becomes the class <span class="defined">prototype</span>. From Table 1.1, the two prototypes are approximately A = (2.33, 2.33) and B = (7.33, 7.33).</p>
<h3>1.4.2. Predict from the nearest prototype</h3>
<p>For an unseen input (2.5, 2.2), compare its straight-line distance to A and B. It is much closer to A, so the model predicts A. The Python function below performs the same operation; its class prototypes were calculated from training examples.</p>
<pre><code>from math import dist

prototypes = {"A": (2.33, 2.33), "B": (7.33, 7.33)}

def predict(size, reflectance):
    point = (size, reflectance)
    return min(prototypes, key=lambda name: dist(point, prototypes[name]))

print(predict(2.5, 2.2))  # A
</code></pre>
<p><strong>Important distinction:</strong> this is a nearest-<em>prototype</em> model, not a neural network, and not a reproduction of Google's classifier. It exists to expose the training–prediction mechanism in a few lines.</p>
<div class="example"><span class="example-title">Check your understanding.</span> What happens if we add many misleading training examples to class A? Will its learned prototype move? Could that change a prediction on the same test point?</div>
<p class="source-line">Practice: <a href="https://teachablemachine.withgoogle.com/">Google Teachable Machine</a> · <a href="/preview/w1/lab/">Week 1 laboratory notebook</a>.</p>
</section>

<section id="five">
<h2>1.5. Mistakes, confidence and responsibility</h2>
<p>A model may predict a class even when it has never seen a similar input. For example, the nearest-prototype program still returns A or B for a sample far outside the observed range. That is not evidence the result is dependable.</p>
<p>A classification system may display a <em>confidence</em> score. In many systems this is a model-dependent score, not a guarantee of correctness. We should not confuse an output with an explanation, and we should not trust a demonstration simply because it succeeds on the teacher's first example.</p>
<ol><li>Were the training examples varied enough?</li><li>What is different about the failed examples?</li><li>Was the test example genuinely unseen?</li><li>Does the system process personal data, faces or voices?</li></ol>
<p>For the school lab, use ordinary objects and synthetic data. Do not upload images of classmates or any personally identifying information.</p>
<p class="source-line">Read: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Lesson 3 — Bias in, bias out</a> · <a href="https://www.unesco.org/en/articles/ai-competency-framework-students">UNESCO AI Competency Framework for Students</a>.</p>
</section>

<section><h2>Bibliography and further study</h2>
<ol><li><a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Raspberry Pi Foundation &amp; Google DeepMind, Experience AI: Foundations of AI</a>, Lessons 1–3 (free teacher resources; access conditions vary).</li>
<li><a href="https://cbseacademic.nic.in/web_material/Curriculum26/publication/srsec/AI_Student_HandbookXI.pdf">CBSE, Class XI AI Student Handbook</a>, introductory AI and data units.</li>
<li><a href="https://www.pyml.ro/machine-learning-lectii-online-in-python.php">pyml.ro, Python &amp; Machine Learning for high-school students</a>.</li></ol></section>
"""
page(1,"course","What is artificial intelligence?","Rules, examples, learning, prediction and the limits of a model.",course)

lab=r"""
<section><h2>Laboratory objectives</h2><p>Experience an AI prediction, train a two-class model using ordinary objects, and inspect a much smaller Python model to see what learning actually changes.</p>
<p class="understated">In-class route: 10 min drawing · 15 min object classifier · 20 min notebook · 10 min comparisons · 5 min exit ticket.</p></section>
<section class="lab-step">
<h2>1. Explore — Quick, Draw!</h2>
<p>Play two or three rounds. Before finishing a sketch, watch the changing guesses. Record one correct and one incorrect guess. Do not assume it recognises the object in the same way a human does.</p>
<p class="launch"><a href="https://quickdraw.withgoogle.com/" target="_blank" rel="noopener noreferrer">Launch Quick, Draw! ↗</a></p>
<ol><li>Choose one drawing the system guessed quickly.</li><li>Choose one it failed to recognise.</li><li>Suggest a difference between the training sketches and yours.</li></ol>
<p class="source-line">Source: <a href="https://experiments.withgoogle.com/collection/ai">Experiments with Google — AI collection</a>.</p>
</section>
<section class="lab-step">
<h2>2. Experiment — Teachable Machine</h2>
<p>Use two ordinary classroom objects (for example, a pencil case and a notebook), not students' faces. Collect about ten different camera frames for each object. Train a model and test on a new background.</p>
<p class="launch"><a href="https://teachablemachine.withgoogle.com/" target="_blank" rel="noopener noreferrer">Launch Teachable Machine ↗</a></p>
<ol><li>Collect and label examples of A and B.</li><li>Train the image classifier.</li><li>Test each object at least three times on backgrounds that were <em>not</em> used for training.</li><li>Record the predicted class and whether it was correct. What changed?</li></ol>
<p class="lab-note">Teachable Machine uses a more complicated underlying model than the toy Python classifier. Do not try to interpret its displayed scores as calibrated probabilities.</p>
</section>
<section class="lab-step">
<h2>3. Inspect — your first Colab notebook</h2>
<p>Open the prepared notebook. It introduces two synthetic numerical features, labelled training examples and a transparent nearest-prototype classifier. Predict the output before you run each cell.</p>
<p><a href="https://colab.research.google.com/github/MachineLearning-Club/MachineLearning-Club.github.io/blob/main/preview/w1/lab/starter.ipynb" target="_blank" rel="noopener noreferrer">Open Week 1 notebook in Google Colab ↗</a> · <a href="starter.ipynb" download>Download notebook</a></p>
<div class="notebook-placeholder"></div>
<ol><li>Run the original notebook and find the learned class prototypes.</li><li>Move two training examples closer to the middle and retrain.</li><li>Identify at least one prediction that changed.</li><li>Test an input far from all training points. Explain what the prediction does <em>not</em> tell you.</li></ol>
</section>
<section><h2>4. Compare and reflect</h2>
<table><thead><tr><th>System</th><th>Input</th><th>What can change?</th></tr></thead><tbody>
<tr><td>Fixed threshold</td><td>Brightness number</td><td>Only the programmer-written threshold</td></tr>
<tr><td>Teachable Machine</td><td>Image</td><td>Model learned from supplied image examples</td></tr>
<tr><td>Club notebook</td><td>Two numbers</td><td>Prototypes calculated from data</td></tr></tbody></table>
<p><strong>Exit ticket:</strong> In two sentences, describe the difference between a programmer writing a rule and an algorithm learning from examples. Give one reason a model may fail on new data.</p>
</section>
"""
# Render the first code cell preview directly under the third step.
lab=lab.replace('<div class="notebook-placeholder"></div>',code_preview(1))
lab+='<script src="/preview/assets/experiment.js" defer></script>'
page(1,"lab","Experiencing artificial intelligence","Explore a real interactive system; then run, modify and explain a tiny transparent classifier.",lab)

homework=r"""
<p class="assignment-meta">Version 2026–2027 · Individual work · A small notebook-based portfolio exercise</p>
<section><h2>Context</h2>
<p>A school makerspace is prototyping a demonstration sorter. Each sample is described by two synthetic sensor measurements, and the target label is A or B. The instructor supplies a second dataset with new measurements. Your goal is to reuse the laboratory classifier, not to create a new algorithm.</p>
<p>Resources: <a href="/preview/w1/course/">Course</a> · <a href="/preview/w1/lab/">Laboratory</a> · <a href="/preview/w1/lab/starter.ipynb">Starter notebook</a> · <a href="sorting-data.csv" download>New training dataset (CSV)</a> · <a href="sorting-test.csv" download>Evaluation dataset (CSV)</a>.</p><details class="notebook-preview"><summary>Provided Colab code: load the CSV files</summary><pre><code>from google.colab import files
files.upload()  # Upload sorting-data.csv and sorting-test.csv
import csv
with open("sorting-data.csv", newline="") as f:
    training = [{"size": float(r["size"]),
                 "reflectance": float(r["reflectance"]),
                 "label": r["label"]}
                for r in csv.DictReader(f)]
</code></pre></details>
</section>
<section><h2>Mandatory <span class="point-value">(1p)</span></h2>
<ol><li>Load the supplied <a href="sorting-data.csv">sorting-data.csv</a> instead of the six laboratory examples.</li>
<li>Calculate new class prototypes using the existing code.</li>
<li>Predict the classes in <a href="sorting-test.csv">sorting-test.csv</a> and report how many were correct.</li>
<li>Show the two learned prototypes and at least one worked distance calculation.</li></ol></section>
<hr>
<section><h2>Homework <span class="point-value">(2p)</span></h2>
<ol><li>Add a test that detects an input far away from <em>both</em> prototypes; print a warning rather than claiming the answer is reliable.</li>
<li>Make the classifier robust to an incomplete measurement (for example, missing reflectance) by rejecting the example with a clear explanation.</li>
<li>Compare the first six-example model against the new model on the same test examples, and record which answers changed.</li>
<li>Write a short explanation (approximately 100–150 words) of what the model learned and what it cannot infer about real materials.</li></ol></section>
<hr>
<section><h2>Advanced — optional reading</h2>
<p><a href="/preview/w1/advanced/">Open the reasoning exercise sheet</a>. The problems investigate whether successful predictions on known examples can establish a general rule. No additional programming tools are required.</p></section>
<section class="submission"><h2>Submission</h2>
<p>Submit one readable <code>.ipynb</code> file and a short <code>README.md</code> or text description with outputs, the number of correct predictions and the warning case. A GitHub account is <strong>not required</strong> in Week 1.</p></section>
"""
page(1,"homework","Assignment 01 — Learning from data","Extend an existing classifier using new examples and show its limits.",homework)

advanced=r"""
<section><h2>Reasoning exercises</h2>
<p>This sheet develops a single idea through small, related problems: <em>different models can agree on the training examples and disagree on an unseen example</em>. It uses truth tables, ordinary pseudocode and counterexamples; there is no formal verification software or installation.</p>
<p><a href="week-01-reasoning.pdf">Read the A4 exercise sheet (PDF)</a> · <a href="week-01-reasoning.tex">LaTeX source</a> · <a href="print.html">Accessible print version</a>.</p>
<iframe class="pdf-view" title="Week 1 advanced reasoning exercises PDF" src="week-01-reasoning.pdf"></iframe>
<p class="understated">The PDF contains one complete worked example, four progressive problems, hints and a selected worked solution. All exercises can be solved with a pencil and a four-row table.</p></section>
<section><h2>How this connects to the course</h2><p>The Laboratory asks why a learned prediction may fail. The Advanced sheet asks a more precise question: can the supplied examples logically rule out a competing model? The answer uses a concrete counterexample, not abstract proof machinery.</p>
<p class="source-line">Further reading: <a href="https://experience-ai.org/ro/units/foundations-of-ai-11-14">Experience AI, Bias in, bias out</a> · <a href="https://ioai-official.org/wp-content/uploads/2025/10/Syllabus.pdf">IOAI classical machine-learning foundations</a>.</p></section>
"""
page(1,"advanced","Advanced 01 — What data cannot prove","A progressive collection on generalisation, counterexamples and unobserved cases.",advanced)

(R/'w1/homework/sorting-data.csv').write_text(
"size,reflectance,label\n2,1,A\n2,2,A\n3,2,A\n3,3,A\n7,6,B\n7,7,B\n8,7,B\n8,8,B\n",encoding="utf-8")
(R/'w1/homework/sorting-test.csv').write_text(
"size,reflectance,label\n2.5,2.3,A\n7.4,7.2,B\n4.1,3.0,A\n7.8,6.0,B\n",encoding="utf-8")
