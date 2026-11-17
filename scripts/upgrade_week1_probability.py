#!/usr/bin/env python3
"""Improve Week 1 probability explanation and visuals without removing theory.

Source of truth: the authored w1/course/index.html. Retains the previously
developed sample-space, conditional, Bayes proof, PMF/PDF, expectation and
transfer sections; inserts three original interactive teaching studios.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"w1/course/index.html"
s=p.read_text(encoding="utf-8")
def add_once(anchor,content):
    global s
    if not anchor in s:
        raise ValueError("Missing original landmark "+anchor[:95])
    if s.count(anchor)!=1:
        raise ValueError("Ambiguous landmark "+anchor[:95])
    s=s.replace(anchor,content+anchor,1)

s=s.replace("<title>Rules, Learning, and Simple Models — Course · Machine Learning Club</title>",
  "<title>AI, Probability and Learning from Data — Course · Machine Learning Club</title>")
s=s.replace('content="Rules, Learning, and Simple Models — Course"',
  'content="AI methods, conditional probability, Bayes theorem, distributions and expected value — Course"')
s=s.replace('<h1>Rules, Learning, and Simple Models</h1>',
  '<h1>AI, Probability and Learning from Data</h1>')
s=s.replace('<p class="deck">Rules, learning families, probability and mathematical expectations.</p>',
  '<p class="deck">How machines use examples — and how probability helps us reason when an answer is uncertain.</p>')
intro=r'''<div class="lesson-prob-route" id="probability-route">
<strong>What you will discover in the first lesson</strong>
<p>We are studying both <em>computer science</em> and <em>probabilistic reasoning</em>. The point is not to memorise a list of AI types: it is to understand how programs represent inputs, make decisions and work with uncertainty.</p>
<ol>
<li><strong>AI as computation:</strong> distinguish rules, trained models and search, using the lamp and camera examples.</li>
<li><strong>Learning from examples:</strong> recognise features, labels and three learning settings.</li>
<li><strong>Probability:</strong> calculate chances by counting outcomes, then update them after a clue.</li>
<li><strong>Bayes' theorem:</strong> distinguish <code>P(A | B)</code> from <code>P(B | A)</code> through a class of 100 fictional pupils.</li>
<li><strong>Distributions and expectation:</strong> examine why two different dice may have the same average.</li>
</ol>
<p><strong>A practical 60-minute route:</strong> 10 minutes rules and data, 10 minutes model families, 12 minutes the die and conditional probability, 15 minutes the Bayes experiment, 10 minutes distributions and expectation, and 3 minutes connecting uncertainty to ID3. The other figures are available for independent exploration, not excluded from the course.</p>
</div>'''
if 'id="probability-route"' not in s:
    add_once('<div class="course-layout"><aside class="course-sidebar">',intro+"\n")
bayes=r'''<div class="prob-studio" data-bayes-studio>
<span class="prob-studio-eyebrow">Interactive thought experiment · Bayes' theorem</span>
<h4>Suppose you receive a correct answer. Did its author know, or guess?</h4>
<p>The numbers below are <strong>expected counts in an invented class of 100</strong>, not information about real students. We assume everyone who knows the answer gets it right and, on a true/false question, everyone who guesses has a 50% chance of being correct.</p>
<div class="prob-experiment-controls">
<label for="bayes-prior">How many already know the answer?
<input id="bayes-prior" data-bayes-prior type="range" min="0" max="100" step="10" value="60"></label>
<output for="bayes-prior" data-bayes-prior-value>60%</output>
</div>
<div class="prob-legend" aria-label="Legend for the 100 artificial cases">
<span><i></i> <output data-bayes-known-count>60</output> knew and correct</span>
<span class="is-lucky"><i></i> <output data-bayes-lucky-count>20</output> guessed correctly</span>
<span class="is-wrong"><i></i> <output data-bayes-wrong-count>20</output> guessed incorrectly</span>
</div>
<div class="bayes-grid" data-bayes-people role="list" aria-label="One hundred simulated cases"></div>
<div class="prob-action-row">
<button type="button" class="bayes-stage-button" data-bayes-keep data-bayes-stage="correct" aria-pressed="false">Show only correct answers</button>
<p class="prob-caption" data-bayes-outcome role="status" aria-live="polite">The class begins with 100 artificial cases.</p>
</div>
<div class="bayes-result">
<small>Among the <output data-bayes-correct-count>80</output> correct answers, how many came from knowledge?</small>
<strong data-bayes-posterior>75%</strong>
<code data-bayes-calculation>P(knew | correct) = 60 / (60 + 20) = 75%</code>
<p data-bayes-reasoning>P(correct | knew) and P(knew | correct) are not the same question.</p>
</div>
<div class="prob-check">
<strong>Check the direction of the condition</strong>
<label for="bayes-question">What information did we observe, and what are we trying to infer?</label>
<select id="bayes-question" data-bayes-choice>
<option value="">Choose…</option>
<option value="conditional">We know the answer is correct; we ask whether the pupil knew</option>
<option value="reverse">We know the pupil knew; we ask whether the answer is correct</option>
</select>
<button type="button" data-bayes-check>Check reasoning</button>
<p data-bayes-feedback role="status" aria-live="polite"></p>
</div>
</div>
'''
if 'data-bayes-studio' not in s:
    add_once('  <div class="academic-math compact"><math display="block"><mi>P</mi><mo>(</mo><mtext>Knew</mtext>',bayes)
observed=r'''<div class="die-observation-chart" data-die-frequency hidden>
<h4>How did the 30 simulated rolls compare with the actual probabilities?</h4>
<p>The expected average alone can hide differences in the distribution. Look at <strong>all ten face counts</strong>, not only the total or the frequency of face 1.</p>
<div class="die-frequency-board" data-die-frequency-bars role="img" aria-label="Observed count of each die face, with a marker for its expected count"></div>
<div class="die-legend"><span><i></i> Observed count in this sample</span>
<span><i class="mark"></i> Expected frequency if we repeated this model many times</span></div>
<p data-die-frequency-note role="status" aria-live="polite"></p>
</div>
'''
if 'data-die-frequency' not in s:
    # Insert the frequency display just after the original three sample metrics,
    # still inside the die demo that sends the sample event.
    marker='<div class="die-three-cases">'
    before,after=s.split(marker,1)
    loc=before.rfind('</div>')
    assert loc!=-1
    s=before[:loc]+observed+"\n"+before[loc:]+marker+after
bridge=r'''<div class="prob-studio prob-bridge-studio" data-uncertainty-studio>
<span class="prob-studio-eyebrow">Next lesson · Probability becomes a tool for learning</span>
<h4>When are the answers hard to predict?</h4>
<p>Imagine twelve <em>labelled</em> examples. Change how many say YES or NO. A decision tree looks for questions that separate mixed answers into more predictable groups.</p>
<div class="uncertainty-choices" role="group" aria-label="Select a labelled dataset">
<button type="button" data-uncertainty-kind="pure" aria-pressed="false">12 YES · 0 NO</button>
<button type="button" data-uncertainty-kind="skewed" aria-pressed="false">10 YES · 2 NO</button>
<button type="button" data-uncertainty-kind="balanced" aria-pressed="true">6 YES · 6 NO</button>
</div>
<div class="uncertainty-dots" data-uncertainty-dots role="list" aria-label="Twelve fictional training labels"></div>
<div class="uncertainty-outcome" role="status" aria-live="polite">
<strong data-uncertainty-degree>Maximum binary-label uncertainty</strong>
<output data-uncertainty-count>6 YES / 6 NO</output>
<p data-uncertainty-result></p>
</div>
<details class="prob-math-optional">
<summary>Calculate the uncertainty in bits (Shannon entropy)</summary>
<p data-uncertainty-math></p>
<p>In Week 2, ID3 uses this value to compare possible questions. <strong>Entropy computed from label frequencies is not the same operation as Bayes' theorem</strong>, although both rely on probability.</p>
</details>
<p><a href="/w2/course/#w2-entropy">Continue with ID3: compare questions by how much uncertainty they remove</a>.</p>
</div>
'''
if 'data-uncertainty-studio' not in s:
    add_once('<p class="transfer-limitation">',bridge+"\n")
if '<link rel="stylesheet" href="/assets/week1-probability-studio.css">' not in s:
    s=s.replace('</head>','<link rel="stylesheet" href="/assets/week1-probability-studio.css"></head>',1)
if '<script defer src="/assets/week1-probability-studio.js"></script>' not in s:
    s=s.replace('</head>','<script defer src="/assets/week1-probability-studio.js"></script></head>',1)
s=s.replace(
 'A probability describes how likely an event is. We start by counting equally likely outcomes, then learn what changes after receiving more information.',
 'A probability describes how likely an event is. We start by counting equally likely outcomes, then learn what changes after receiving more information. Many machine-learning methods express uncertainty using probabilities or scores; other models produce deterministic outputs. A numerical score is not automatically a well-calibrated probability.')
p.write_text(s,encoding="utf-8")
print('Updated Week 1 core course, added Bayes, observed PMF and ID3 uncertainty experiments.')
