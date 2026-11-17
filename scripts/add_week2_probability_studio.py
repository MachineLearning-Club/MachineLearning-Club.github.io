#!/usr/bin/env python3
"""Publish a probability-first ID3 bridge into the canonical Week 2 course.

The probability explorer derives its data from the *existing 12-row diary
table* on the published page, rather than from a second hidden dataset.
This authoring script is idempotent and does not alter the maths or labels.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'data/week23/w2_course.html'
text=source.read_text(encoding='utf-8')
block='''<div class="id3-probability-studio" id="id3-probability" data-id3-probability>
<span class="id3-prob-kicker">Probability studio · from Week 1 to Week 2</span>
<h3>What happens to uncertainty after we ask a question?</h3>
<p>In Week 1, a clue changed which outcomes were possible. Here, a question divides <strong>12 labelled records</strong> into smaller groups. We can use probability to describe how mixed the YES and NO answers are <em>before</em> and <em>after</em> the question.</p>
<div class="id3-prob-overview">
  <div class="id3-prob-before">
    <span class="id3-prob-stage">01 · Before asking</span>
    <strong>All 12 recorded days</strong>
    <div class="id3-prob-cases" data-id3-prob-total role="list" aria-label="All twelve fictional training labels"></div>
    <div class="id3-prob-measure"><span data-id3-prob-root-ratio>6/12 YES, 6/12 NO</span><strong data-id3-prob-root-h>H = 1 bit</strong></div>
    <p>How uncertain are the answers when we have not looked at a feature?</p>
  </div>
  <div class="id3-prob-direction" aria-hidden="true">→</div>
  <div class="id3-prob-after">
    <span class="id3-prob-stage">02 · Ask a question</span>
    <strong>Choose from the real diary</strong>
    <p>The feature buttons in Experiment 01 above change this calculation too. Or choose a question below.</p>
    <div class="id3-prob-feature-select" role="group" aria-label="Question for the information gain explorer">
      <button data-id3-prob-feature="sky" type="button" aria-pressed="true">Sky</button>
      <button data-id3-prob-feature="wind" type="button" aria-pressed="false">Wind</button>
      <button data-id3-prob-feature="temperature" type="button" aria-pressed="false">Temperature</button>
    </div>
  </div>
</div>
<div class="id3-prob-branches" data-id3-prob-branches aria-live="polite"></div>
<div class="id3-prob-equation" aria-live="polite">
  <div><small>BEFORE THE QUESTION</small><strong data-id3-prob-before>1.000 bits</strong></div>
  <span aria-hidden="true">−</span>
  <div><small>AFTER THE QUESTION</small><strong data-id3-prob-after>0.333 bits</strong></div>
  <span aria-hidden="true">=</span>
  <div class="id3-prob-outcome"><small>INFORMATION GAIN</small><strong data-id3-prob-gain>0.667 bits</strong></div>
</div>
<div class="id3-prob-gauge" role="img" aria-label="Before-split entropy divided into uncertainty remaining and information gained">
  <span data-id3-prob-remaining style="width:33.333%"></span><span data-id3-prob-learned style="width:66.667%"></span>
</div>
<div class="id3-prob-legend"><span><i class="remaining"></i> Uncertainty left</span><span><i class="learned"></i> Uncertainty removed by the question</span></div>
<p class="id3-prob-conclusion" data-id3-prob-conclusion role="status" aria-live="polite"></p>
<div class="id3-prob-gain-ranking">
  <h4>Compare all three questions</h4>
  <p>All three start from <strong>the same 12 examples</strong>. The largest information gain makes the most useful first question <em>according to ID3's greedy rule</em>.</p>
  <div data-id3-prob-ranking class="id3-prob-ranks" role="group" aria-label="Information gain of each candidate question"></div>
</div>
<details class="id3-prob-maths">
  <summary>Show the full weighted calculation for this question</summary>
  <p data-id3-prob-formula></p>
  <p>The weight of a group is its <strong>fraction of all records</strong>: four of twelve rows contribute weight 4/12 = 1/3. Weights need not be equal if group sizes differ.</p>
</details>
<div class="id3-prob-next">
  <h4>03 · Ask again, but only inside the cloudy group</h4>
  <p>After asking Sky, sunny and rainy already have pure answers. There are only <strong>four cloudy days</strong> left: two YES and two NO. Should we split <em>those four days</em> by Wind or Temperature?</p>
  <div class="id3-prob-local-controls" role="group" aria-label="Next question on four cloudy examples">
    <button data-id3-prob-cloudy="wind" type="button" aria-pressed="true">Wind</button>
    <button data-id3-prob-cloudy="temperature" type="button" aria-pressed="false">Temperature</button>
  </div>
  <div data-id3-prob-cloudy-output class="id3-prob-cloudy-results" aria-live="polite"></div>
  <p class="id3-prob-tip">The same feature can have different gain in different parts of a tree: <strong>Wind has small gain across all 12 rows, but perfect gain inside the four cloudy rows.</strong></p>
</div>
<p class="id3-prob-caveat"><strong>What these numbers do not say:</strong> A leaf containing 4/4 YES training records is not proof of a 100% chance that a future unfamiliar day will be suitable. These are <em>observed label proportions in a fictional training dataset</em>, not calibrated real-world probabilities or test accuracy.</p>
</div>'''
needle='<details><summary>Where do these numbers come from? (optional mathematics)</summary>'
if 'id="id3-probability"' not in text:
    assert text.count(needle)==1
    text=text.replace(needle,block+'\n'+needle,1)
tocneedle='<li><a href="#w2-tree">2.5. Build the tree</a></li>'
if 'href="#id3-probability"' not in text:
    assert text.count(tocneedle)==1
    text=text.replace(tocneedle,'<li><a href="#id3-probability">2.4 · Probability studio</a></li>'+tocneedle,1)
text=text.replace(
 '<p>Without calculating logarithms, we can already see that Sky leaves fewer mixed groups. For those exploring the mathematics: the other features have information gains of approximately <strong>0.082</strong> (wind) and <strong>0</strong> (temperature), while Sky has 0.667. Therefore, ID3 chooses <strong>Sky</strong> first.</p>',
 '<p>From the probabilities in the experiment: <strong>Sky leaves about 0.333 bits and removes 0.667 bits</strong> of the original 1 bit. Wind removes about 0.082 bits, and Temperature removes none. This is why ID3 chooses Sky first. You can verify each number by expanding the weighted calculation above.</p>'
)
text=text.replace(
 '<p><strong>Not required for the core lesson:</strong> logarithms and calculating information gain in bits. Those are optional extensions.</p>',
 '<p><strong>Mathematics during the lesson:</strong> fractions, conditional proportions, averages and information gain in bits are introduced visually. Computing the logarithms by hand is an optional extension; the numerical calculation remains available.</p>'
)
# Educator guidance: a genuine source of distinction between probability and accuracy.
text=text.replace(
 '<p><strong>Optional extension:</strong> greedy versus globally smallest trees (Ciortuz, solved problem 4). Not necessary for a first classifier.</p>',
 '<p><strong>Week 1 connection:</strong> pupils already know that probability changes when we receive information. Use the branch counts to distinguish P(YES | sunny)=4/4 from P(YES)=6/12 and introduce H(after) as a group-size-weighted uncertainty. Emphasise that a 4/4 training proportion is not a validated confidence probability.</p><p><strong>Optional extension:</strong> greedy versus globally smallest trees (Ciortuz, solved problem 4). Not necessary for a first classifier.</p>'
)
source.write_text(text,encoding='utf-8')
print('Updated canonical Week 2 course with responsive ID3 probability studio')
