#!/usr/bin/env python3
"""Make Weeks 2 and 3 genuinely accessible within one pre-university lesson.

The Core uses counting, grouping and arithmetic averages.
Information gain/logarithms and the sum-of-squares derivation remain available
as optional explanations, rather than gatekeeping the main experiment.
Canonical lesson fragments are the source of truth for generated pages.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
MISSION={
 2: '''<div class="learning-intention"><p class="learning-intention-label">One-hour learning goal</p>
<p>By the end, you should be able to explain how a <strong>decision tree</strong> learns a sequence of questions from examples.</p>
<ol><li><strong>Recognise:</strong> identify what we know (sky, wind, temperature) and what we want to predict (go or stay).</li>
<li><strong>Experiment:</strong> compare three questions by grouping the 12 example days.</li>
<li><strong>Explain:</strong> choose a helpful question and follow a path to an answer.</li></ol>
<p><strong>Not required for the core lesson:</strong> logarithms and calculating information gain in bits. Those are optional extensions.</p></div>''',
 3: '''<div class="learning-intention"><p class="learning-intention-label">One-hour learning goal</p>
<p>By the end, you should be able to explain how <strong>K-means</strong> makes groups of nearby points <em>without knowing correct class labels</em>.</p>
<ol><li><strong>Recognise:</strong> describe five points and two starting centres.</li>
<li><strong>Experiment:</strong> place each point with a nearby centre, then move each centre to its group's average.</li>
<li><strong>Explain:</strong> show why the centres moved and how to decide when to stop.</li></ol>
<p><strong>Not required for the core lesson:</strong> proving why squared-distance error decreases. The numerical derivation is optional.</p></div>'''
}
BRIDGE={
 2: '''<p class="learning-before-experiment"><strong>Before interacting:</strong> imagine sorting 12 recorded days by one question: <em>Is it sunny, cloudy or rainy?</em> In which groups would you already know the yes/no answer? Use the visible records to decide before you consider any formula.</p>''',
 3: '''<p class="learning-before-experiment"><strong>Before interacting:</strong> imagine placing a shared meeting point in the middle of a few nearby locations. Would you leave it at the first point, or move it closer to the group's middle? Watch the two centre markers as the algorithm repeats that idea.</p>'''
}
for week in (2,3):
 path=ROOT/f"data/week23/w{week}_course.html"
 text=path.read_text(encoding="utf-8")
 start=f'<section class="chapter-section" id="w{week}-problem"><h2>'
 pattern=rf'(<section class="chapter-section" id="w{week}-problem"><h2>.*?</h2>)'
 if 'learning-intention-label' not in text:
  text,n=re.subn(pattern,lambda m:m.group(1)+"\n"+MISSION[week],text,count=1,flags=re.S)
  assert n==1,(week,'learning goals')
 target='<div class="decision-playground" data-id3-playground' if week==2 else '<div data-kmeans-demo'
 if 'learning-before-experiment' not in text:
  assert text.count(target)==1,(week,'experiment')
  text=text.replace(target,BRIDGE[week]+"\n"+target,1)
 if week==2:
  text=text.replace('2.4. Entropy — giving a number to uncertainty',
                    '2.4. How mixed are the answers? (Entropy)')
  pattern=r'(<div class="worked"><h3>Fully worked — information gain of Sky</h3>.*?</div>)'
  match=re.search(pattern,text,re.S)
  assert match,(week,'math derivation missing')
  if 'discovery-math' not in text:
   text=text[:match.start()]+(
    '<details class="discovery-math"><summary>Optional mathematics: calculate information gain with logarithms</summary>'
    +match.group(1)+'</details>')+text[match.end():]
  text=text.replace('The other features have information gains of approximately <strong>0.082</strong> (wind) and <strong>0</strong> (temperature). Therefore, ID3 chooses <strong>Sky</strong> first.',
   'Without calculating logarithms, we can already see that Sky leaves fewer mixed groups. For those exploring the mathematics: the other features have information gains of approximately <strong>0.082</strong> (wind) and <strong>0</strong> (temperature), while Sky has 0.667. Therefore, ID3 chooses <strong>Sky</strong> first.')
  text=text.replace('<li>Reproduce <code>IG(sky)=2/3</code> with weights and branch entropies.</li>',
                    '<li>Explain why Sky is the strongest question by counting clear-answer groups. <em>Optional:</em> reproduce <code>IG(sky)=2/3</code>.</li>')
 else:
  text=text.replace('<p>We measure the total squared distance of every point from its assigned centroid. Call this <strong>J</strong> or the <strong>within-cluster sum of squares</strong>.</p>',
  '<p>We want group centres to sit <strong>closer to the points that belong to them</strong>. The interactive bars compare how far apart everything is, before and after the move. For a more precise comparison, mathematicians add the <em>squared distances</em> to produce a score called <strong>J</strong>. Smaller is better for this specific exercise.</p>')
  math_start='<div class="concept-formula"><span>Objective function</span>'
  if 'class="discovery-math"' not in text:
   m=re.search(r'(<div class="concept-formula"><span>Objective function</span>.*?</div>\s*<div class="worked"><h3>Numerical comparison from the source example</h3>.*?</div>)',text,re.S)
   assert m,(week,'objective math section')
   text=text[:m.start()]+('<details class="discovery-math"><summary>Optional mathematics: measure improvement with squared distances</summary>'
                         +m.group(1)+'</details>')+text[m.end():]
 path.write_text(text,encoding="utf-8")
 print('Pedagogical core and optional mathematics published:',path.relative_to(ROOT))
