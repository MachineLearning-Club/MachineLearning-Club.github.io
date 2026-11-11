/* Lightweight, inline per-week practice quiz (no backend or accounts). */
(() => {
'use strict';
const root=document.getElementById('weekly-quiz');
if(!root)return;
const n=Number(root.dataset.week),path='/quiz/data/week-'+String(n).padStart(2,'0')+'.json';
const key='mlclub.weekly-quiz.practice.v1.'+n;
const make=(tag,text,cls)=>{
 const e=document.createElement(tag);if(text!==undefined)e.textContent=text;
 if(cls)e.className=cls;return e;
};
const correct=(actual,expected)=>actual.length===expected.length&&expected.every(x=>actual.includes(x));
const read=()=>{try{return JSON.parse(localStorage.getItem(key)||'[]');}catch(_){return [];}};
const write=records=>{try{localStorage.setItem(key,JSON.stringify(records));}catch(_){}};
let bank=null,view='start',index=0,answers=[],endAt=0,timer=null,record=null;
const mmss=t=>String(Math.floor(t/60)).padStart(2,'0')+':'+String(t%60).padStart(2,'0');
const reset=()=>{root.replaceChildren();};
const button=(label,action,cls)=>{
 const b=make('button',label,cls||'');b.type='button';b.addEventListener('click',action);return b;
};
function score(){
 return bank.questions.reduce((total,q,i)=>total+(correct(answers[i]||[],q.correct)?q.points:0),0);
}
function start(){
 view='quiz';index=0;answers=bank.questions.map(()=>[]);endAt=Date.now()+bank.durationSeconds*1000;
 timer=setInterval(tick,500);render();
}
function tick(){
 const time=root.querySelector('[data-remaining]');
 if(view!=='quiz'||!time)return;
 const left=Math.max(0,Math.ceil((endAt-Date.now())/1000));
 time.textContent=mmss(left);
 if(!left)submit(true);
}
function intro(){
 reset();
 const old=read();
 const p=make('p','10 questions · 5 minutes · 10 points. Choose one or several answers. After submitting, you can inspect the correct choices and explanations.','quiz-catalogue-note');
 root.append(p);
 const line=make('div',null,'quiz-inline-start');
 line.append(button('Start Week '+n+' quiz',start,'quiz-start-button'));
 root.append(line);
 if(old.length){
   const recent=old[old.length-1];
   root.append(make('p','Previous local attempt: '+recent.score+' / '+recent.maximum+' points. This result is stored only in this browser.','understated'));
   root.append(button('Review previous attempt',()=>{record=recent;answers=recent.answers;index=0;view='review';render();}));
 }
 root.append(make('p','Practice only. Answer keys are publicly available in this static site; these are not official school grades. Email delivery and authenticated submissions are not enabled.','understated'));
}
function render(){
 if(view==='start')return intro();
 reset();
 const heading=make('div',null,'quiz-progress-row');
 heading.append(make('span','Question '+(index+1)+' / '+bank.questions.length),make('strong',view==='quiz'?'Time left: ':'Review · Score: '+record.score+' / '+record.maximum));
 if(view==='quiz'){const span=make('span','','quiz-timer');span.dataset.remaining='';heading.append(span);}
 root.append(heading);
 const nav=make('div',null,'quiz-choices');
 bank.questions.forEach((q,i)=>{
   const b=button(String(i+1),()=>{index=i;render();},i===index?'active':'');
   b.setAttribute('aria-label','Go to question '+(i+1));
   if(answers[i]?.length)b.title='Answered';
   nav.append(b);
 });
 root.append(nav);
 const q=bank.questions[index];
 const card=make('section',null,'weekly-quiz-card');
 const heading2=make('div',null,'quiz-progress-row');
 heading2.append(make('strong','#'+(index+1)+' / '+bank.questions.length),make('span',q.points+' point'));
 card.append(heading2);
 const question=make('div',null,'quiz-question');
 question.append(make('p',q.topic,'eyebrow'),make('h3',q.prompt));
 question.append(make('p',q.type==='multiple'?'Select ALL correct answers.':'Select one answer.','understated'));
 const choices=make('div',null,'quiz-option-list');
 q.options.forEach((option,i)=>{
   const label=make('label',null,'quiz-option');
   const input=document.createElement('input');
   input.type=q.type==='multiple'?'checkbox':'radio';
   input.name='week-quiz-answer';input.value=String(i);input.checked=answers[index].includes(i);
   input.disabled=view==='review';
   if(view==='review'&&q.correct.includes(i))label.classList.add('correct');
   if(view==='review'&&input.checked&&!q.correct.includes(i))label.classList.add('incorrect');
   input.addEventListener('change',()=>{
     if(view!=='quiz')return;
     if(q.type==='single'){answers[index]=[i];}
     else if(input.checked)answers[index]=[...new Set([...answers[index],i])];
     else answers[index]=answers[index].filter(x=>x!==i);
     const b=nav.children[index];b.title='Answered';
   });
   label.append(input,make('span',String.fromCharCode(65+i)+'. '+option));
   choices.append(label);
 });
 question.append(choices);
 if(view==='review'){
   const expl=make('div',null,'quiz-answer-explanation');
   expl.append(make('strong',correct(answers[index],q.correct)?'Correct · '+q.points+' point':'Correct selection: '+q.correct.map(i=>String.fromCharCode(65+i)).join(', ')));
   expl.append(make('p',q.explanation));
   question.append(expl);
 }
 card.append(question);root.append(card);
 const controls=make('div',null,'quiz-controls');
 const prev=button('← Previous',()=>{index--;render();});prev.disabled=index===0;
 const next=button('Next →',()=>{index++;render();});next.disabled=index>=bank.questions.length-1;
 controls.append(prev,next);
 if(view==='quiz')controls.append(button('Submit answers',()=>submit(false),'quiz-submit-button'));
 else controls.append(button('Close review',()=>{view='start';render();}));
 root.append(controls);
 if(view==='quiz'){
   root.append(make('p',answers.filter(a=>a.length).length+' of '+bank.questions.length+' questions answered. The timer continues while this page is open.','understated'));
   tick();
 }
}
function submit(timedOut){
 if(view!=='quiz')return;
 const skipped=answers.filter(a=>!a.length).length;
 if(!timedOut&&skipped&& !confirm('You have '+skipped+' unanswered question(s). Submit anyway?'))return;
 if(timer){clearInterval(timer);timer=null;}
 record={week:n,score:score(),maximum:bank.maximumPoints,
  submitted:new Date().toISOString(),answers:answers.map(a=>[...a]),timedOut:!!timedOut};
 const history=read();history.push(record);write(history.slice(-20));
 view='review';index=0;render();
 const notice=make('p','Submitted: '+record.score+' / '+record.maximum+' points. Review the questions or download a local copy of your score.','quiz-sum');
 root.prepend(notice);
 const download=button('Download result (.txt)',()=>{
   const text='Machine Learning Club — Week '+n+'\nDate: '+record.submitted+'\nScore: '+record.score+' / '+record.maximum+'\nThis is a local practice result, not an official grade.\n';
   const url=URL.createObjectURL(new Blob([text],{type:'text/plain'}));
   const a=document.createElement('a');a.href=url;a.download='MLC_Week_'+String(n).padStart(2,'0')+'_result.txt';
   a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
 notice.append(document.createTextNode(' '),download);
}
async function load(){
 try{
  const response=await fetch(path,{cache:'no-store'});
  if(response.status===404){root.replaceChildren(make('p','The quiz will be published after the lesson content has been reviewed.','understated'));return;}
  if(!response.ok)throw Error('Could not load the question bank.');
  bank=await response.json();
  if(bank.week!==n||!Array.isArray(bank.questions)||bank.questions.length!==10)throw Error('Incorrect quiz bank format.');
  intro();
 }catch(error){root.replaceChildren(make('p','Quiz unavailable: '+error.message,'understated'));}
}
window.addEventListener('pagehide',()=>{if(timer)clearInterval(timer);});
load();
})();