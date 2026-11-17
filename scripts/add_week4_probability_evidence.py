#!/usr/bin/env python3
"""Keep Week 4 classification evidence connected to Week 1 probability.

The voting displays use the existing six-point nearest-neighbour experiment;
the confusion matrix uses the existing fixed 3+3 test-label counts. Neither
claims training-vote fractions are calibrated probabilities.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/week47/w4_course.html'
s=p.read_text(encoding='utf-8')
knn='''<div class="revision-prob-studio" data-knn-vote-panel>
<span class="revision-prob-kicker">Evidence studio · What does K out of K mean?</span>
<h3>Why a unanimous vote is not a guarantee</h3>
<p>Move the new point Q, and change K in the experiment above. We will display <strong>which labelled neighbours voted</strong> and how their votes add up. Their vote fraction is <em>not automatically a calibrated probability</em> of a correct prediction.</p>
<div class="rev-votes-list" data-rev-neighbour-votes role="list" aria-label="Labels of the selected nearest neighbours"></div>
<div class="rev-vote-count"><strong data-rev-vote-result>3 A, 0 B</strong><span data-rev-vote-fraction>3/3 votes for A</span></div>
<div class="rev-vote-stacked" role="img" aria-label="Proportions of nearest neighbours belonging to class A and B"><span data-rev-vote-a></span><span data-rev-vote-b></span></div>
<p data-rev-vote-explain class="rev-prob-feedback" role="status" aria-live="polite"></p>
<details class="rev-prob-explain"><summary>Why does 3/3 not mean a 100% chance of being correct?</summary><p>The neighbours are a small selected subset of a fictional training set. We need a sufficiently representative, separate labelled evaluation set to measure prediction reliability. Distance, sample quality and the choice of K matter; a vote ratio by itself is not a measured probability that a future label will match.</p></details>
</div>'''
confusion='''<div class="revision-prob-studio" data-confusion-evaluation-panel>
<span class="revision-prob-kicker">Probability and evaluation · Conditions go in two directions</span>
<h3>Precision and recall ask different questions</h3>
<p>This is a <strong>synthetic six-case test exercise</strong>, not a model's measured performance in a real school. Change the false-positive and false-negative sliders above, and compare the proportions in the confusion table.</p>
<div class="rev-confusion-table-wrap"><table class="rev-confusion-table">
<caption>Actual labels in rows, predicted labels in columns</caption>
<thead><tr><th scope="col">Actual / predicted</th><th scope="col">YES</th><th scope="col">NO</th></tr></thead>
<tbody>
<tr><th scope="row">YES</th><td class="rev-confusion-correct"><strong data-rev-tp>2</strong><small>TP · correct YES</small></td><td class="rev-confusion-mistake"><strong data-rev-fn>1</strong><small>FN · missed YES</small></td></tr>
<tr><th scope="row">NO</th><td class="rev-confusion-mistake"><strong data-rev-fp>1</strong><small>FP · false alarm</small></td><td class="rev-confusion-correct"><strong data-rev-tn>2</strong><small>TN · correct NO</small></td></tr>
</tbody></table></div>
<div class="rev-confusion-metrics">
<div><span>Precision · P(actual YES | predicted YES)</span><strong data-rev-precision>2/3 = 66.7%</strong><small data-rev-precision-note>Of all YES predictions, how many were correct?</small></div>
<div><span>Recall · P(predicted YES | actual YES)</span><strong data-rev-recall>2/3 = 66.7%</strong><small>Of all actual YES cases, how many were found?</small></div>
</div>
<p class="rev-prob-feedback"><strong>Week 1 connection:</strong> the event after the vertical bar is the condition we know. Reversing the condition gives a different question, just as with Bayes' theorem. Precision and recall are conditional proportions <em>in this test set</em>, not proof of future reliability.</p>
</div>'''
if 'data-knn-vote-panel' not in s:
    key='<p><strong>Potential confusion:</strong> the letter K occurs in both names'
    assert s.count(key)==1
    s=s.replace(key,knn+'\n'+key,1)
if 'data-confusion-evaluation-panel' not in s:
    key='<details><summary>Why should this tiny percentage not be reported as a reliable real-world accuracy?</summary>'
    assert s.count(key)==1
    s=s.replace(key,confusion+'\n'+key,1)
p.write_text(s,encoding='utf-8')
print('Updated canonical Week 4 with voting evidence and conditional evaluation.')
