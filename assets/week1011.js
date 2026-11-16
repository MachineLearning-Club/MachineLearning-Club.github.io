/* Two deliberately small, deterministic school simulations. No accounts or APIs. */
(()=>{'use strict';
const all=(s,r=document)=>[...r.querySelectorAll(s)],one=(s,r=document)=>r.querySelector(s);
for(const root of all('[data-g10-tokens]')){
 const input=one('[data-token-text]',root),out=one('[data-token-output]',root);if(!input||!out)continue;
 function render(){
  const pieces=input.value.match(/[\p{L}\p{N}]+|[^\s]/gu)||[];
  out.replaceChildren();
  const summary=document.createElement('strong');summary.textContent='Classroom toy split: '+pieces.length+' units';
  const row=document.createElement('div');row.className='token-chips';
  for(const unit of pieces){const chip=document.createElement('span');chip.textContent=unit;row.append(chip);}
  out.append(summary,row);
 }
 input.addEventListener('input',render);render();
}
for(const root of all('[data-g10-next]')){
 const out=one('[data-next-result]',root),buttons=all('[data-word]',root);
 buttons.forEach(button=>button.addEventListener('click',()=>{
  buttons.forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
  out.textContent='“Today the sky looks '+button.dataset.word+'.” This word received '+Math.round(+button.dataset.score*100)+'% in our invented example. That does not verify today’s real weather.';
 }));
}
for(const root of all('[data-g10-feed]')){
 const inputScience=one('[data-clicks=science]',root),inputMusic=one('[data-clicks=music]',root),
  countScience=one('[data-count=science]',root),countMusic=one('[data-count=music]',root),
  bars=one('[data-feed-bars]',root),out=one('[data-feed-result]',root);
 if(!inputScience||!inputMusic||!bars)continue;
 function render(){
  const scores=[{name:'Science',value:+inputScience.value},{name:'Music',value:+inputMusic.value}];
  countScience.textContent=inputScience.value;countMusic.textContent=inputMusic.value;
  bars.replaceChildren();
  for(const s of scores){
   const line=document.createElement('div');line.className='feed-line';
   const name=document.createElement('span');name.textContent=s.name;
   const rail=document.createElement('div');rail.className='feed-rail';
   const bar=document.createElement('div');bar.className='feed-bar';bar.style.width=(s.value/8*100)+'%';rail.append(bar);
   const value=document.createElement('span');value.textContent=String(s.value);
   line.append(name,rail,value);bars.append(line);
  }
  const sorted=scores.slice().sort((a,b)=>b.value-a.value);
  out.textContent=sorted[0].value===sorted[1].value?'The two subjects are tied. A real service needs a tie-breaking rule.':
   sorted[0].name+' ranks first ('+sorted[0].value+' clicks versus '+sorted[1].value+'). A click is not proof of the user’s intentions.';
 }
 [inputScience,inputMusic].forEach(i=>i.addEventListener('input',render));render();
}
for(const root of all('[data-g11-pipeline]')){
 const temp=one('[data-temperature]',root),missing=one('[data-missing]',root),label=one('[data-temperature-label]',root),
  out=one('[data-pipeline-trace]',root);
 if(!temp||!missing||!out)continue;
 function render(){
  const t=+temp.value,isMissing=missing.checked;
  label.textContent=t+' °C';
  const messages=isMissing?[
   ['Sensor','No reading'],['Validate','Missing value detected'],['Decide','Do not use a temperature rule'],['Display','CHECK SENSOR']
  ]:[
   ['Sensor',t+' °C'],['Validate','Number received'],['Decide',t+' < 19 → '+String(t<19)],['Display',t<19?'HEAT ON':'HEAT OFF']
  ];
  out.replaceChildren();
  for(const [name,value] of messages){
   const item=document.createElement('div');item.className='pipeline-stage';
   const title=document.createElement('strong');title.textContent=name;
   const text=document.createElement('span');text.textContent=value;item.append(title,text);out.append(item);
  }
 }
 temp.addEventListener('input',render);missing.addEventListener('change',render);render();
}
})();