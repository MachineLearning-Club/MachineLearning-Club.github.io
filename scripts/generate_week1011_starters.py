#!/usr/bin/env python3
"""Teacher-authored, account-free JupyterLite starters for Weeks 10 and 11."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def text(s):return [line+'\n' for line in s.strip().split('\n')]
def make(n,title,parts,challenge):
 cells=[dict(cell_type='markdown',metadata={},source=text('# '+title+'\n\nRun the cells in order. Before each run, predict the output. Change one input, then explain what changed. No API, key, installation, or personal information is needed.'))]
 for name,code in parts:
  compile(code,f'w{n}','exec')
  cells.append(dict(cell_type='markdown',metadata={},source=text('## '+name)))
  cells.append(dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=text(code)))
 cells.append(dict(cell_type='markdown',metadata={},source=text('## Independent challenge\n\n'+challenge)))
 book=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python (Pyodide)',language='python',name='python'),language_info=dict(name='python')),nbformat=4,nbformat_minor=5)
 dest=ROOT/f'w{n}/lab/starter.ipynb';dest.write_text(json.dumps(book,ensure_ascii=False,indent=2)+'\n')
 print('Updated',dest.relative_to(ROOT),len(cells),'cells')

make(10,'Week 10 — text, feeds and checking a claim',[
('1. Simplify a sentence into words (not real GPT token IDs)',r'''from collections import Counter
sentence="AI can help, but people must check."
words=[w.strip(".,!?").lower() for w in sentence.split()]
print("Classroom word split:",words)
print("Word counts:",Counter(words))'''),
('2. Change a toy feed ranking',r'''clicks={"science":5,"music":2}
ranked=sorted(clicks,key=clicks.get,reverse=True)
print("Ranked topics:",ranked)
# Change music clicks to 8, then predict the new order.'''),
('3. Verify a claim using deterministic arithmetic',r'''yes,no=12,8
percentage=100*yes/(yes+no)
print(f"{yes} yes votes out of {yes+no}: {percentage:.1f}%")
print("Was an invented claim of 80% correct?", percentage==80)''')],
'Set both click counts equal, observe the tie, and explain why it cannot reveal a person’s intentions. Then write a safe percentage(yes,no) function that handles zero votes.')

make(11,'Week 11 — a small, testable classroom monitor',[
('1. Name the data and the required behaviour',r'''examples=[(17,"HEAT ON"),(21,"HEAT OFF"),(None,"CHECK SENSOR")]
for value,expected in examples:
    print("Input",value,"must produce",expected)'''),
('2. Keep the sensor separate from a decision',r'''class Sensor:
    def __init__(self,value):self.value=value
    def read(self):return self.value

def decide(value):
    if value is None:return "CHECK SENSOR"
    return "HEAT ON" if value<19 else "HEAT OFF"

for value,expected in examples:
    result=decide(Sensor(value).read())
    print(value,"=>",result)
    assert result==expected'''),
('3. Test the exact boundary',r'''print("18 degrees:",decide(18))
print("19 degrees:",decide(19))
print("No reading:",decide(None))
assert decide(18)=="HEAT ON"
assert decide(19)=="HEAT OFF"
assert decide(None)=="CHECK SENSOR"''')],
'Change the threshold from 19 to 20. Update the boundary test, then explain which component changed. Write a meaningful commit message, even if you use only the account-free version simulator.')
