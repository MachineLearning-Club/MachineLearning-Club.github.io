#!/usr/bin/env python3
"""Publish curriculum-aligned public practice quizzes for Weeks 10 and 11.

Questions are based on the current Course, Laboratory, and Homework sources.
They are five-minute student practice, not confidential graded assessments.
"""
from html import escape
from pathlib import Path
import json
import re
ROOT=Path(__file__).resolve().parents[1]
# topic, question, exactly four options, correct indices, answer explanation
BANKS={
  10:("Generative AI: Language, Recommendations and Verification",[
    ("Tokens","Which statement best describes real language-model tokens?",[
      "Each token is always exactly one English word",
      "Tokens may represent whole words, parts of words, punctuation or other units",
      "A token is always one pixel",
      "A token is a verified fact"
    ],[1],"Tokenisation maps input text to a sequence of units. Our on-page splitter is a deliberately simplified demonstration."),
    ("Toy splitting","The classroom toy splits 'AI can help students!' into which sequence?",[
      "AI, can, help, students, !",
      "One token containing the entire sentence",
      "One token per letter, always",
      "Five numeric probabilities, with no text units"
    ],[0],"In the lesson's simplified representation punctuation is separated from the words; this is not a claim about a real GPT tokenizer."),
    ("Prediction","A toy model assigns 60% to 'blue' after 'Today the sky looks ...'. What does that mean?",[
      "The sky is certainly blue right now",
      "The model has checked the weather",
      "'blue' is the highest-scoring illustrated continuation among the three given choices",
      "A 60% chance that all model-generated sentences are true"
    ],[2],"The displayed numbers are illustrative candidate preferences, not verified statements about the world."),
    ("Clicks","A toy recommender has 5 science clicks and 2 music clicks. Which topic ranks first?",[
      "Science","Music","They always tie","The system needs pupil names to decide"
    ],[0],"In this teaching example the larger click count ranks ahead."),
    ("Meaning of clicks","Why is a single click an incomplete measure of someone's preference?",[
      "Clicks are always random",
      "A person may click because of curiosity, surprise or disagreement",
      "Clicks contain the entire person's biography",
      "A click guarantees the content is accurate"
    ],[1],"An interaction is evidence of behaviour; motives are not known from that signal alone."),
    ("Verification","A newsletter says 80% voted yes. The tally is 12 yes and 8 no. What percentage is correct?",[
      "12%","20%","60%","80%"
    ],[2],"12/(12+8)=12/20=0.60=60%. The draft must be corrected."),
    ("Claim and evidence","Which is the independent evidence for the newsletter vote claim?",[
      "How fluent the AI wording sounds",
      "The original anonymous tally of yes and no",
      "The model's confidence in its own wording",
      "The length of the generated sentence"
    ],[1],"Compare the claim with the actual original count, not a generated paraphrase."),
    ("Data protection","Which actions are appropriate when using AI-assisted writing? Select ALL.",[
      "Review and correct important factual claims before publishing",
      "Paste classmates' passwords to provide context",
      "Use anonymous or invented data in classroom examples",
      "Publish an AI draft without reading it"
    ],[0,2],"Verification and minimal-data handling are part of a responsible workflow."),
    ("Agent permissions","What distinguishes a text suggestion from an authorised automated action?",[
      "Any generated sentence automatically grants permission to publish",
      "A tool-using program must have explicit permission to perform its action",
      "A chatbot message is identical to a sent email",
      "Checking permissions makes code unable to run"
    ],[1],"Generating a suggested message is not the same as being authorised to send or publish it."),
    ("Model limits","Which statements follow from the Week 10 exercises? Select ALL.",[
      "Our tokenizer and feed ranker are classroom demonstrations, not real platform implementations",
      "The largest next-word score is not proof that the sentence is true",
      "Real GPT models always use the exact split from the demo",
      "A persuasive claim needs no independent evidence"
    ],[0,1],"Do not conflate illustrative toy systems with operational production models or treat plausibility as truth.")
  ]),
  11:("Software Engineering: Components, Tests and Git",[
    ("Requirements","For the fictional classroom sensor, which description is a testable requirement?",[
      "The program should be intelligent",
      "If the reading is missing, display CHECK SENSOR",
      "The UI should feel modern",
      "Every result should sound confident"
    ],[1],"A requirement should identify observable behaviour for a specified condition."),
    ("Rule","With the original threshold 19°C, what should the program display at 17°C?",[
      "HEAT OFF","CHECK SENSOR","HEAT ON","No message can ever be shown"
    ],[2],"The program returns HEAT ON for values below 19°C."),
    ("Boundary","With 'HEAT ON if value < 19 else HEAT OFF', what should 19°C produce?",[
      "HEAT ON","HEAT OFF","CHECK SENSOR","The sensor object is deleted"
    ],[1],"The comparison is strictly less than 19, so the boundary value produces HEAT OFF."),
    ("Missing reading","Which is the expected output when the sensor returns None?",[
      "HEAT ON","HEAT OFF","CHECK SENSOR","None must be treated as 0°C"
    ],[2],"The program checks for missing data before comparing temperatures."),
    ("Pipeline","Which is the correct sequence of the four-stage classroom flow?",[
      "Display → Decide → Check → Sensor",
      "Sensor → Check → Decide → Display",
      "Commit → Sensor → Login → Train",
      "Random guess → Label → Delete"
    ],[1],"The reading is checked, a decision is made, and then a message is shown."),
    ("Objects","In the Week 11 Python example, what is Sensor(17)?",[
      "A class definition","An object instantiated from Sensor","A Git repository","A neural network"
    ],[1],"Sensor is the class, and Sensor(17) creates one object with its own stored reading."),
    ("Tests","What is the purpose of assert decide(None) == 'CHECK SENSOR'?",[
      "To prove all possible programs are correct",
      "To compare actual behaviour with a stated expectation",
      "To train the model on a test label",
      "To change the sensor hardware"
    ],[1],"An assertion checks a specified test case and fails if the result differs."),
    ("Controlled change","After changing the threshold from 19 to 20, which test would detect the changed boundary?",[
      "decide(19) == 'HEAT ON'",
      "decide(None) == 'HEAT ON'",
      "decide(19) == 'CHECK SENSOR'",
      "Every temperature is converted to a string before comparison"
    ],[0],"At 19, the old rule returned HEAT OFF but the revised threshold-20 rule returns HEAT ON. This test distinguishes the versions."),
    ("Version control","Which actions are part of the real GitHub workflow? Select ALL.",[
      "Review the code diff before committing",
      "Choose a meaningful commit message and push the commit",
      "Share passwords publicly in the repository",
      "Claim files are on GitHub even if they were never pushed"
    ],[0,1],"Version history should include reviewed, intentionally committed changes that reach the repository."),
    ("Engineering responsibility","Which statements are supported by the sensor example? Select ALL.",[
      "Input checking can be tested independently of the display",
      "A passing three-case test proves all possible real sensors are safe",
      "Small components make it easier to isolate a fault",
      "A Git commit replaces the need to test code"
    ],[0,2],"Components and tests aid reasoning, but finite checks do not prove universal physical-system correctness.")
  ])
}
for week,(title,questions) in BANKS.items():
    assert len(questions)==10
    converted=[]
    for i,(topic,prompt,options,correct,explanation) in enumerate(questions,1):
        assert len(options)==4 and len(correct) in (1,2) and len(set(correct))==len(correct)
        assert all(0<=j<4 for j in correct)
        converted.append(dict(id=f"w{week}q{i}",topic=topic,prompt=prompt,options=options,
                              correct=correct,type="single" if len(correct)==1 else "multiple",
                              points=1,explanation=explanation))
    result=dict(week=week,title=title,durationSeconds=300,maximumPoints=10,
        status="Draft practice questions; teacher review required",
        instructions="Open practice based on the published course and lab. Local scores are not official grades.",
        questions=converted)
    path=ROOT/f"quiz/data/week-{week:02}.json"
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    source=ROOT/f"w{week}/quiz/index.html"
    original=source.read_text(encoding="utf-8")
    main=(f'<main class="lesson-content week47-academic week1011-academic">'
      f'<p class="eyebrow">Week {week} · Practice Quiz</p>'
      f'<h1>{escape(title)}</h1>'
      f'<section><h2>Five-minute knowledge check</h2>'
      '<p>Ten questions from this week’s Course and Laboratory. Public answer review and '
      'local practice results only; this is not an official school assessment.</p>'
      f'<div id="weekly-quiz" data-week="{week}" aria-live="polite"><p>Loading quiz…</p></div></section>'
      '<nav class="week-bottom-links" aria-label="Other learning activities">'
      +''.join(f'<a href="/w{week}/{kind}/">{name}</a>' for kind,name in
               [('course','Course'),('lab','Laboratory'),('homework','Homework'),('advanced','Advanced')])
      +'</nav></main>')
    new,count=re.subn(r'<main\b[^>]*>.*?</main>',lambda _:main,original,count=1,flags=re.S)
    assert count==1
    new=new.replace('<script defer src="/assets/weekly-quiz.js"></script>','')
    for tag in ('<link rel="stylesheet" href="/assets/week1011.css">',
                '<link rel="stylesheet" href="/assets/week89.css">',
                '<script defer src="/assets/weekly-quiz.js"></script>'):
        if tag not in new:new=new.replace('</head>',tag+'</head>',1)
    source.write_text(new,encoding="utf-8")
catalog=ROOT/"quiz/data/catalog.json"
info=json.loads(catalog.read_text(encoding="utf-8"))
info["notice"]="Public five-minute practice quizzes are available for Weeks 1–14; Week 15 uses a practical 20-point project rubric."
for row in info["quizzes"]:
    if row["week"] in BANKS:
        row.update(title=BANKS[row["week"]][0],
             subject={
               10:"Toy token sequences · Feed ranking · Verifying factual claims",
               11:"Sensor pipeline · Input checks · Assertions · Git workflow"
             }[row["week"]],
             status="demo",durationMinutes=5,questionCount=10,maxPoints=10)
catalog.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
hub=ROOT/"quiz/index.html"
old=hub.read_text(encoding="utf-8")
old=old.replace(
 "Practice quizzes are available for Weeks 1–9 and 12–14; Week 15 has a separate practical project rubric. Each available quiz has ten questions, five minutes and a scored answer review after submission. Weeks 10–11 are still being prepared.",
 "Practice quizzes are available for Weeks 1–14; Week 15 has a separate practical project rubric. Each quiz has ten questions, five minutes and a scored answer review after submission.")
hub.write_text(old,encoding="utf-8")
print("Published 20 questions for Weeks 10–11 and updated the quiz catalogue")
