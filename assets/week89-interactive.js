/* Weeks 8–9: deterministic k-nearest-neighbour classifier on actual UCI digit images.
   Data: 600 labelled training images + 200 held-out samples, each 8×8 integers 0–16.
   Both JS and the Python notebook share the same split; no remote model or API.
*/
(()=>{'use strict';
const rootNodes=[...document.querySelectorAll('[data-digit-lab]')];
if(!rootNodes.length)return;
const datasetPromise=fetch('/assets/data/week89-digits.json').then(r=>{if(!r.ok)throw Error('Dataset HTTP '+r.status);return r.json()});
const thresholded=(v,t)=>t===0?v:(v>=t?16:0);
function distance(a,b,t){
 let s=0;
 for(let j=0;j<64;j++){
  let delta=thresholded(a[j],t)-thresholded(b[j],t);
  s+=delta*delta;
 }
 return s;
}
function classify(x,train,k,t){
 const distances=train.map(row=>({d:distance(x,row.x,t),y:row.y,id:row.id,row}));
 distances.sort((a,b)=>a.d-b.d||a.id-b.id);
 const neighbours=distances.slice(0,k),votes=new Map();
 for(const v of neighbours){
  let score=votes.get(v.y)||{n:0,sum:0};
  score.n++;score.sum+=v.d;votes.set(v.y,score);
 }
 const ranked=[...votes.entries()].sort((a,b)=>b[1].n-a[1].n||a[1].sum-b[1].sum||a[0]-b[0]);
 return {predicted:ranked[0][0],neighbours,votes};
}
function getMetrics(data,k,t){
 const predicted=[],matrix=Array.from({length:10},()=>Array(10).fill(0));
 let correct=0;
 for(const item of data.test){
  const prediction=classify(item.x,data.train,k,t).predicted;
  predicted.push(prediction);
  matrix[item.y][prediction]++;
  if(prediction===item.y)correct++;
 }
 return {predicted,matrix,correct,total:data.test.length};
}
const cached=new Map();
function metrics(data,k,t){
 const id=k+':'+t;
 if(!cached.has(id))cached.set(id,getMetrics(data,k,t));
 return cached.get(id);
}
function el(tag,text,cls){
 const e=document.createElement(tag);
 if(text!==undefined&&text!==null)e.textContent=String(text);
 if(cls)e.className=cls;
 return e;
}
function drawGrid(target,values,interactive,onToggle){
 target.replaceChildren();
 for(let i=0;i<64;i++){
  const value=values[i];
  const cell=el(interactive?'button':'span',interactive?String(value):'','digit-cell');
  const tone=Math.round(248-(value/16)*204);
  cell.style.backgroundColor='rgb('+tone+','+Math.round(tone+6)+','+Math.round(tone+9)+')';
  cell.title='Row '+(Math.floor(i/8)+1)+', column '+(i%8+1)+': '+value+'/16';
  if(interactive){
   cell.type='button';cell.setAttribute('aria-label',cell.title+', click to increase pixel');
   cell.setAttribute('aria-pressed',value?'true':'false');
   cell.addEventListener('click',()=>onToggle(i));
  }
  target.append(cell);
 }
}
function drawConfusion(container,mat){
 container.replaceChildren();
 const table=el('table',null,'digit-matrix');
 const head=el('thead'),headrow=el('tr');headrow.append(el('th','Actual ↓ / predicted →'));
 for(let d=0;d<10;d++)headrow.append(el('th',d));
 head.append(headrow);table.append(head);
 const body=el('tbody');
 for(let actual=0;actual<10;actual++){
  const tr=el('tr');tr.append(el('th',actual));
  for(let prediction=0;prediction<10;prediction++){
   const td=el('td',mat[actual][prediction]);
   if(actual===prediction)td.classList.add('digit-diagonal');
   else if(mat[actual][prediction])td.classList.add('digit-error');
   td.title='Actual '+actual+', predicted '+prediction+': '+mat[actual][prediction]+' examples';
   tr.append(td);
  }
  body.append(tr);
 }
 table.append(body);container.append(table);
}
for(const root of rootNodes){
 const status=root.querySelector('[data-digit-status]');
 const grid=root.querySelector('[data-digit-grid]');
 const caseNumber=root.querySelector('[data-case-index]');
 const output=root.querySelector('[data-digit-output]');
 const near=root.querySelector('[data-digit-neighbours]');
 const kSel=root.querySelector('[data-k-select]');
 const tSel=root.querySelector('[data-threshold-select]');
 const evalButton=root.querySelector('[data-evaluate]');
 const evalOut=root.querySelector('[data-evaluation-output]');
 const matOut=root.querySelector('[data-digit-matrix]');
 const errorsOut=root.querySelector('[data-digit-errors]');
 const previous=root.querySelector('[data-previous-case]');
 const next=root.querySelector('[data-next-case]');
 const nextError=root.querySelector('[data-next-error]');
 const reset=root.querySelector('[data-reset-pixels]');
 let data=null,index=0,working=[],modified=false;
 const currentK=()=>Number(kSel?.value||3),currentT=()=>Number(tSel?.value||0);
 const loadCase=(i)=>{
  index=(i+data.test.length)%data.test.length;
  working=[...data.test[index].x];modified=false;
  if(caseNumber)caseNumber.value=index+1;
  render();
 };
 const render=()=>{
  if(!data)return;
  const item=data.test[index],result=classify(working,data.train,currentK(),currentT());
  if(grid)drawGrid(grid,working,true,idx=>{
   working[idx]=(working[idx]+4)%20;modified=true;render();
  });
  const match=result.predicted===item.y;
  if(output){
   output.replaceChildren();
   output.append(el('strong','Known digit: '+item.y+' · predicted: '+result.predicted));
   output.append(el('p',(match?'Correct on the original example. ':'Incorrect on the original example. ')+
      'Using k='+currentK()+' neighbours'+(currentT()?'; pixels thresholded at '+currentT():'; original grey levels')+'.'));
   output.append(el('small',modified?
     'You edited the pixels. This is now a new image; its displayed known label remains the original digit. Edited images are NOT included in the held-out accuracy.':
     'This original test image was excluded from the training examples; its label is shown only for checking the prediction.'));
  }
  if(near){
   near.replaceChildren();
   for(const n of result.neighbours){
    const box=el('div',null,'digit-neighbour');
    const preview=el('div',null,'digit-neighbour-grid');
    drawGrid(preview,n.row.x,false);
    box.append(preview,el('span','Digit '+n.y+' · d²='+n.d));
    near.append(box);
   }
  }
  if(status)status.textContent='Showing held-out example '+(index+1)+' / '+data.test.length+(modified?' (edited)':'');
 };
 const clearEval=()=>{
  if(evalOut)evalOut.textContent='Run the evaluation to count predictions for all 200 unmodified held-out images.';
  if(matOut)matOut.replaceChildren();
  if(errorsOut)errorsOut.replaceChildren();
 };
 const evaluate=()=>{
  if(!data)return;
  if(evalButton)evalButton.disabled=true;
  if(evalOut)evalOut.textContent='Evaluating all 200 previously withheld digits…';
  // Defer until the next paint so the UI reflects the action before computation.
  requestAnimationFrame(()=>setTimeout(()=>{
   const result=metrics(data,currentK(),currentT());
   const wrong=result.total-result.correct;
   if(evalOut)evalOut.textContent=result.correct+' / '+result.total+' correct ('+
    (100*result.correct/result.total).toFixed(1)+'% accuracy); '+wrong+
    ' incorrect. These are genuine held-out predictions on this fixed classroom subset.';
   if(matOut)drawConfusion(matOut,result.matrix);
   if(errorsOut){
    errorsOut.replaceChildren();
    const examples=result.predicted.map((v,i)=>({v,i})).filter(v=>v.v!==data.test[v.i].y);
    if(!examples.length)errorsOut.append(el('span','No misclassifications on this subset for these settings.'));
    for(const item of examples.slice(0,16)){
     const b=el('button','#'+(item.i+1)+': '+data.test[item.i].y+' → '+item.v);
     b.type='button';b.title='Inspect misclassified test example '+(item.i+1);
     b.addEventListener('click',()=>{loadCase(item.i);root.scrollIntoView({block:'nearest'});});
     errorsOut.append(b);
    }
    if(examples.length>16)errorsOut.append(el('span',' '+(examples.length-16)+' more errors not shown'));
   }
   if(evalButton)evalButton.disabled=false;
  },0));
 };
 datasetPromise.then(d=>{
  if(!Array.isArray(d.train)||d.train.length!==600||!Array.isArray(d.test)||d.test.length!==200)throw Error('Unexpected classroom dataset');
  data=d;
  if(caseNumber){caseNumber.min='1';caseNumber.max=String(d.test.length);caseNumber.step='1';}
  if(previous)previous.addEventListener('click',()=>loadCase(index-1));
  if(next)next.addEventListener('click',()=>loadCase(index+1));
  if(caseNumber)caseNumber.addEventListener('change',()=>loadCase(Math.max(0,Math.min(d.test.length-1,Number(caseNumber.value||1)-1))));
  if(reset)reset.addEventListener('click',()=>loadCase(index));
  for(const select of [kSel,tSel])if(select)select.addEventListener('change',()=>{clearEval();render();});
  if(nextError)nextError.addEventListener('click',()=>{
   const result=metrics(data,currentK(),currentT());
   let i=(index+1)%data.test.length;
   while(i!==index&&result.predicted[i]===data.test[i].y)i=(i+1)%data.test.length;
   if(result.predicted[i]!==data.test[i].y)loadCase(i);
   else if(status)status.textContent='There are no mistakes to inspect for these settings.';
  });
  if(evalButton)evalButton.addEventListener('click',evaluate);
  loadCase(0);
  clearEval();
 }).catch(e=>{
  if(status)status.textContent='Unable to load the digit examples: '+e.message+'. Try reloading or use the downloadable notebook.';
  if(evalButton)evalButton.disabled=true;
 });
}
})();