#!/usr/bin/env python3
"""Rebalance Week 1's 10-point quiz between AI and probability concepts.

Keep the five valid questions on computation and learning; use the other
five to assess conditional probability, Bayes, PMFs, and expectation.
All examples and numbers come from the authored Week 1 course.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
file=ROOT/'quiz/data/week-01.json'
bank=json.loads(file.read_text(encoding='utf-8'))
bank['title']='AI, Probability and Learning from Data'
bank['status']='Draft practice quiz; teacher review required'
bank['instructions']='Ten questions: five on AI and learning, five on probability and uncertain evidence. Multiple-choice items require every correct option. One point for an exact match.'
questions=bank['questions']
assert len(questions)==10 and all(questions[i]['id']==f'w1q{i+1}' for i in range(10))
questions[6]={
  'id':'w1q7','type':'single','topic':"Bayes' theorem",
  'prompt':'In the fictional class of 100, 60 know the true/false answer and the remaining 40 guess. If a correct answer is observed, what is P(knew | correct)?',
  'options':['60%','75%','80%','100%'],'correct':[1],
  'explanation':'All 60 who know answer correctly, and 20 of the 40 who guess are correct on average. Of the 80 correct answers, 60 came from knowledge: 60/80 = 75%.',
  'points':1
}
questions[8]={
  'id':'w1q9','type':'multiple','topic':'Conditional probability',
  'prompt':'Select ALL correct statements about the Week 1 Bayes experiment.',
  'options':[
    'In the simplified model, P(correct | knew) = 100%.',
    'P(knew | correct) always equals P(correct | knew).',
    'For the initial 60% who know, P(knew | correct) = 75%.',
    'A correct true/false answer proves the pupil knew.'
  ],'correct':[0,2],
  'explanation':'We assume someone who knows answers correctly, but some guesses are correct too. Reversing the given condition changes the probability.',
  'points':1
}
questions[9]={
  'id':'w1q10','type':'multiple','topic':'Probability distributions',
  'prompt':'Select ALL conclusions supported by the fair-versus-tricky ten-sided die experiments.',
  'options':[
    'The fair and tricky distributions both have expected value 5.5.',
    'Two different distributions can have the same expected value.',
    'If 30 rolls have average 5.5, the die must be fair.',
    'Every sample of 30 rolls must exactly match the probability distribution.'
  ],'correct':[0,1],
  'explanation':'The fair die is uniform; the tricky die favours 1 and 10. Both have the same mean 5.5, but their distributions differ, and finite samples vary.',
  'points':1
}
file.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog_file=ROOT/'quiz/data/catalog.json'
catalog=json.loads(catalog_file.read_text(encoding='utf-8'))
matches=[q for q in catalog['quizzes'] if q['week']==1]
assert len(matches)==1
matches[0]['title']='AI, Probability and Learning from Data'
matches[0]['subject']='AI foundations · Conditional probability · Bayes · Expected value · Distributions'
catalog_file.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
quiz_page=ROOT/'w1/quiz/index.html'
text=quiz_page.read_text(encoding='utf-8')
text=text.replace('Learning families, conditional probability, expected value and AI applications.',
 'Five questions on AI and learning, and five on conditional probability, Bayes, distributions and expected value.')
quiz_page.write_text(text,encoding='utf-8')
print('Week 1 quiz balanced: 5 AI and learning + 5 probability, 10 points total.')
