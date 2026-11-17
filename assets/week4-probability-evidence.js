/* Week 4: vote ratios and evaluation proportions are evidence, not guarantees.
 * No duplicate model. Consumes the exact state emitted by the existing
 * KNN and confusion-matrix exercises, including their current input values.
 */
(()=>{
'use strict';
const $=(q,root=document)=>root.querySelector(q);
const circle=(className,text)=>{
 const span=document.createElement('span');span.className=className;span.textContent=text;return span;
};
const knn=$('[data-revision-knn]');
const visual=$('[data-knn-vote-panel]');
if(knn&&visual){
 function render(detail){
  if(!detail)return;
  const {k,neighbours,votes,prediction}=detail;
  if(neighbours.length!==k||votes.A+votes.B!==k)throw Error('Invalid nearest-neighbour vote data');
  const list=$('[data-rev-neighbour-votes]',visual);
  list.replaceChildren();
  neighbours.forEach((item,i)=>{
   const node=document.createElement('div');
   node.className='rev-neighbour '+(item.cls==='A'?'is-a':'is-b');
   node.setAttribute('role','listitem');
   node.setAttribute('aria-label','Nearest '+(i+1)+': '+item.name+', class '+item.cls+
    ', squared distance '+item.d2);
   node.append(circle('rev-neighbour-class',item.cls));
   node.append(circle('rev-neighbour-name',item.name));
   node.append(circle('rev-neighbour-distance','d² = '+item.d2.toFixed(2)));
   list.append(node);
  });
  const winner=prediction==='A'||prediction==='B'?prediction:null;
  const win=winner?votes[winner]:Math.max(votes.A,votes.B);
  $('[data-rev-vote-result]',visual).textContent=votes.A+' A, '+votes.B+' B';
  $('[data-rev-vote-fraction]',visual).textContent=
    winner?win+'/'+k+' votes for '+winner+' ('+(100*win/k).toFixed(0)+'% of selected votes)':
    'Equal votes: a tie-breaking rule is required.';
  $('[data-rev-vote-a]',visual).style.width=(100*votes.A/k).toFixed(2)+'%';
  $('[data-rev-vote-b]',visual).style.width=(100*votes.B/k).toFixed(2)+'%';
  $('[data-rev-vote-explain]',visual).textContent=
    k===1?'K=1 uses one labelled training neighbour, not a probability estimate.':
    win===k?'All '+k+' selected neighbours agree on '+winner+
     '. This is still not a 100% guarantee for a new unseen case.':
    'The vote is split. A majority chooses the prediction, but the vote fraction is not a validated confidence score.';
 }
 knn.addEventListener('mlclub:knn-update',event=>render(event.detail));
 if(knn.dataset.knnEvidence)render(JSON.parse(knn.dataset.knnEvidence));
}
const confusion=$('[data-confusion-demo]');
const matrix=$('[data-confusion-evaluation-panel]');
if(confusion&&matrix){
 function render(data){
  const {tp,tn,fp,fn,total}=data;
  if(tp+tn+fp+fn!==total||tp+fn!==3||tn+fp!==3)throw Error('Confusion matrix totals inconsistent');
  for(const [key,val] of Object.entries({tp,tn,fp,fn})){
   $('[data-rev-'+key+']',matrix).textContent=String(val);
  }
  const predictedYes=tp+fp,actualYes=tp+fn;
  const precision=predictedYes>0?tp/predictedYes:null;
  const recall=tp/actualYes;
  $('[data-rev-precision]',matrix).textContent=precision===null?
    'Undefined — no YES predictions':tp+'/'+predictedYes+' = '+(100*precision).toFixed(1)+'%';
  $('[data-rev-recall]',matrix).textContent=
    tp+'/'+actualYes+' = '+(100*recall).toFixed(1)+'%';
  $('[data-rev-precision-note]',matrix).textContent=precision===null?
    'Precision cannot be computed when the model never predicts YES.':
    'Of '+predictedYes+' predicted YES cases, '+tp+' were actually YES.';
 }
 confusion.addEventListener('mlclub:confusion-update',event=>render(event.detail));
 if(confusion.dataset.confusionEvidence)render(JSON.parse(confusion.dataset.confusionEvidence));
}
})();
