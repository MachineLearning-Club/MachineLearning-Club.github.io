/* Visual discovery layer for early pre-university lessons.
 * It reads the outputs of existing, independently tested ID3 and K-means
 * demonstrations. It does not replace their data or numerical algorithms.
 */
(()=>{
'use strict';
const one=(selector,root=document)=>root.querySelector(selector);
const all=(selector,root=document)=>[...root.querySelectorAll(selector)];
const element=(tag,className,text)=>{
 const e=document.createElement(tag);
 if(className)e.className=className;
 if(text!=null)e.textContent=text;
 return e;
};
// WEEK 2 — Treat 12 labelled records as 12 visible days, not a formula.
for(const root of all('[data-id3-playground]')){
 const controls=one('.id3-controls',root);
 const groups=one('[data-id3-groups]',root);
 const gain=one('[data-id3-gain]',root);
 if(!controls||!groups||!gain)continue;
 root.classList.add('discovery-studio');
 const mission=element('div','discovery-mission');
 mission.innerHTML='<span class="discovery-eyebrow">Experiment 01 · Asking better questions</span>'+
 '<p><strong>Can one question make the answers clearer?</strong> Each small square below represents one of the 12 fictional school-day records. Green means <em>go outside</em>; orange means <em>stay inside</em>. Choose Sky, Wind or Temperature, then see how the records separate.</p>'+
 '<p class="discovery-action-hint">Try all three questions. The goal is not to memorise a formula, but to spot which question produces groups with a single answer.</p>';
 root.insertBefore(mission,controls);
 const explanation=element('div','discovery-summary');
 explanation.setAttribute('role','status');
 explanation.setAttribute('aria-live','polite');
 gain.parentNode.insertBefore(explanation,gain);
 const challenge=element('div','discovery-challenge');
 challenge.innerHTML='<p class="discovery-eyebrow">Your turn · Predict, then check</p>'+
 '<label>Which question would you ask <strong>first</strong> to build a short decision tree? '+
 '<select data-discovery-choice><option value="">Choose a feature…</option><option value="sky">Sky</option>'+
 '<option value="wind">Wind</option><option value="temperature">Temperature</option></select></label>'+
 '<button type="button" data-discovery-check>Check prediction</button>'+
 '<p data-discovery-feedback role="status" aria-live="polite"></p>';
 gain.insertAdjacentElement('afterend',challenge);
 const feedback=one('[data-discovery-feedback]',challenge);
 one('[data-discovery-check]',challenge).addEventListener('click',()=>{
   const answer=one('[data-discovery-choice]',challenge).value;
   feedback.className='';
   if(!answer){feedback.textContent='Choose a question first, then check your prediction.';return;}
   const correct=answer==='sky';
   feedback.classList.toggle('discovery-correct',correct);
   feedback.textContent=correct?
     'Correct. Sky produces two completely predictable groups (sunny and rainy). Only cloudy days still need another question.':
     'Try Sky again. Its sunny and rainy groups each contain only one answer; Wind and Temperature leave every group mixed.';
 });
 const narratives={
  sky:'Sky separates the days into three groups. Sunny is always YES; rainy is always NO. Only cloudy days need another question.',
  wind:'Wind creates two groups, but each still contains both YES and NO examples. The first question has not solved either group.',
  temperature:'Temperature creates two equally mixed groups. Here, it cannot help the tree decide YES versus NO.'
 };
 let last='';
 const render=()=>{
  const groupNodes=all('.id3-group',groups);
  if(!groupNodes.length)return;
  const feature=one('[data-id3-feature][aria-pressed="true"]',root)?.dataset.id3Feature||'sky';
  const counts=groupNodes.map(group=>{
    const label=one('strong',group)?.textContent||'';
    const text=one('small',group)?.textContent||'';
    const match=text.match(/\[(\d+)\+,\s*(\d+)[−-]\]/);
    if(!match)return null;
    const yes=Number(match[1]),no=Number(match[2]);
    if(!one('.discovery-cases',group)){
      const strip=element('div','discovery-cases');
      strip.setAttribute('role','list');
      strip.setAttribute('aria-label',label+': '+yes+' days with yes, '+no+' days with no');
      for(let i=0;i<yes+no;i++){
        const positive=i<yes;
        const tile=element('span','discovery-day '+(positive?'is-yes':'is-no'),positive?'✓':'×');
        tile.setAttribute('role','listitem');
        tile.title='Recorded day: '+(positive?'go outside':'stay inside');
        tile.setAttribute('aria-label',positive?'go outside':'stay inside');
        strip.append(tile);
      }
      group.insertBefore(strip,group.querySelector('.id3-split-bar')||null);
    }
    return {yes,no};
  });
  if(counts.some(c=>!c))return;
  const pure=counts.filter(c=>c.yes===0||c.no===0).length;
  const key=feature+':'+pure;
  if(key!==last){
    explanation.replaceChildren();
    const statistic=element('div','discovery-big-number',pure+' of '+counts.length);
    const body=element('div','discovery-summary-copy');
    body.append(element('strong',null,'groups already have a clear answer'));
    body.append(element('p',null,narratives[feature]));
    explanation.append(statistic,body);
    last=key;
  }
 };
 const observer=new MutationObserver(render);
 observer.observe(groups,{childList:true});
 render();
}
// WEEK 3 — The objective becomes a visible before/after, not an isolated J.
for(const root of all('[data-kmeans-demo]')){
 const label=one('[data-kmeans-step-label]',root);
 const svg=one('svg',root);
 if(!label||!svg)continue;
 root.classList.add('discovery-studio');
 const intro=element('div','discovery-mission');
 intro.innerHTML='<span class="discovery-eyebrow">Experiment 02 · Organise five locations</span>'+
 '<p><strong>Move two group centres closer to the points.</strong> Each coloured point is a location; each × marks a centre. K-means first assigns a point to its nearest centre, then moves each centre to the average of the group.</p>';
 root.insertBefore(intro,root.firstChild);
 const steps=element('ol','discovery-stepper');
 const labels=['Start','Assign','Move centres','Check again'];
 labels.forEach(t=>steps.append(element('li',null,t)));
 intro.insertAdjacentElement('afterend',steps);
 const challenge=element('div','discovery-challenge');
 challenge.innerHTML='<p class="discovery-eyebrow">Predict before pressing Next</p>'+
 '<p>Point <strong>B(1,0)</strong> is between the two starting centres. Which centre is nearer?</p>'+
 '<div class="discovery-choice-row"><button data-guess-centre="1" type="button">Centre 1</button>'+
 '<button data-guess-centre="2" type="button">Centre 2</button></div>'+
 '<p data-guess-feedback role="status" aria-live="polite"></p>';
 steps.insertAdjacentElement('afterend',challenge);
 all('[data-guess-centre]',challenge).forEach(button=>button.addEventListener('click',()=>{
   const correct=button.dataset.guessCentre==='1';
   all('[data-guess-centre]',challenge).forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
   const result=one('[data-guess-feedback]',challenge);
   result.className=correct?'discovery-correct':'';
   result.textContent=correct?
     'Correct. B is 2 units from centre 1 and about 2.24 from centre 2. It joins group 1.':
     'Look at the distance table: centre 1 is 2 units away, centre 2 is about 2.24. B joins group 1.';
 }));
 const score=element('div','discovery-cost');
 score.innerHTML='<div class="discovery-cost-header"><strong>How tightly grouped are the points?</strong>'+
 '<span data-cost-caption>First, assign the points to the nearest starting centre.</span></div>'+
 '<div class="discovery-score-row"><span>Starting centres</span><div class="discovery-meter"><i style="width:100%"></i></div>'+
 '<strong>7.00</strong></div>'+
 '<div class="discovery-score-row"><span>After moving</span><div class="discovery-meter improved">'+
 '<i data-improved-meter style="width:0%"></i></div><strong data-improved-number>—</strong></div>'+
 '<p data-cost-explain class="discovery-score-explain">We will measure the total squared distance from each location to its assigned centre. Smaller is better here.</p>';
 const explanation=one('[data-kmeans-explain]',root);
 explanation.insertAdjacentElement('afterend',score);
 const render=()=>{
   const match=label.textContent.match(/Step\s+(\d+)/);
   if(!match)return;
   const step=Number(match[1])-1;
   all('li',steps).forEach((item,i)=>{item.classList.toggle('is-current',step===i);item.classList.toggle('is-complete',step>i);});
   const ready=step>=2;
   one('[data-improved-number]',score).textContent=ready?'3.17':'—';
   one('[data-improved-meter]',score).style.width=ready?'45.2%':'0%';
   one('[data-cost-caption]',score).textContent=ready?'After the centres moved to their group averages.':
        step===0?'First, assign each point to its nearest starting centre.':
        'The first assignment has a total squared distance of 7.';
   one('[data-cost-explain]',score).textContent=step===3?
     'The total squared distance fell from 7 to about 3.17 — a reduction of roughly 55%. Rechecking did not change any group, so this run has converged.':
     step===2?
     'The total squared distance fell from 7 to about 3.17 — roughly 55% less. Next, check whether any point changes group with the new centres.':
     'Smaller means the points are closer to their assigned centre. The comparison appears after Step 3.';
   if(!ready||svg.querySelector('[data-centre-motion]'))return;
   const NS='http://www.w3.org/2000/svg';
   const layer=document.createElementNS(NS,'g');
   layer.setAttribute('data-centre-motion','');
   layer.setAttribute('aria-hidden','true');
   const x=v=>160+(v+1.5)*100,y=v=>326-v*154;
   const pairs=[[[ -1,0],[0,1/3]],[[3,1],[3,.5]]];
   pairs.forEach(([oldPos,newPos],i)=>{
     const fromX=x(oldPos[0]),fromY=y(oldPos[1]),toX=x(newPos[0]),toY=y(newPos[1]);
     const ghost=document.createElementNS(NS,'circle');
     for(const [key,value] of Object.entries({cx:fromX,cy:fromY,r:10,fill:'none',stroke:'#7b92a1','stroke-width':2,'stroke-dasharray':'4 3'}))ghost.setAttribute(key,value);
     layer.append(ghost);
     const line=document.createElementNS(NS,'line');
     for(const [key,value] of Object.entries({x1:fromX,y1:fromY,x2:toX,y2:toY,stroke:i===0?'#477eaa':'#be865e','stroke-width':3,'stroke-dasharray':'5 4'}))line.setAttribute(key,value);
     layer.append(line);
   });
   svg.append(layer);
 };
 new MutationObserver(render).observe(label,{childList:true,characterData:true,subtree:true});
 // Existing K-means renderer clears the SVG on each step. Re-attach motion
 // arrows only after its synchronous redraw, guarding against observer loops.
 new MutationObserver(()=>{
  if((label.textContent.match(/Step\s+(\d+)/)?.[1]||0)<3)return;
  if(svg.querySelector('[data-centre-motion]'))return;
  render();
 }).observe(svg,{childList:true});
 render();
}
})();
