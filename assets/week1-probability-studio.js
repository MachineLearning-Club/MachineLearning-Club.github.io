/* Week 1 Probability Studio — original, dependency-free classroom experiments.
 * All counts here are expectations for a fictional class of 100, NOT measured
 * student data. The Bayesian model assumes known answers are always correct
 * and guesses on a true/false item succeed with probability one-half.
 */
(()=>{
'use strict';
const $=(q,root=document)=>root.querySelector(q);
const $$=(q,root=document)=>[...root.querySelectorAll(q)];
const node=(tag,className,text)=>{
 const el=document.createElement(tag);
 if(className)el.className=className;
 if(text!==undefined)el.textContent=text;
 return el;
};
function bayes(){
 const root=$('[data-bayes-studio]');if(!root)return;
 const knob=$('[data-bayes-prior]',root),value=$('[data-bayes-prior-value]',root),
   people=$('[data-bayes-people]',root),readout=$('[data-bayes-outcome]',root),
   detail=$('[data-bayes-reasoning]',root),keep=$('[data-bayes-keep]',root),
   challenge=$('[data-bayes-check]',root),feedback=$('[data-bayes-feedback]',root);
 let showOnlyCorrect=false;
 const tiles=[];
 for(let i=0;i<100;i++){
  const tile=node('span','bayes-person');
  tile.setAttribute('role','listitem');
  tiles.push(tile);people.append(tile);
 }
 function render(){
  const knows=Number(knob.value);
  const guesses=100-knows;
  const guessedCorrect=guesses/2,guessedWrong=guesses/2;
  const correct=knows+guessedCorrect;
  const posterior=correct?knows/correct:0;
  value.textContent=String(knows)+'%';
  let index=0;
  for(const [type,count,meaning] of [
   ['known',knows,'Knew answer and answered correctly'],
   ['lucky',guessedCorrect,'Guessed and answered correctly'],
   ['wrong',guessedWrong,'Guessed and answered incorrectly']
  ]){
   for(let j=0;j<count;j++){
    const tile=tiles[index++];
    tile.className='bayes-person is-'+type+(showOnlyCorrect&&type==='wrong'?' is-filtered':'');
    tile.textContent=type==='known'?'K':type==='lucky'?'✓':'×';
    tile.title=meaning;
    tile.setAttribute('aria-label',meaning);
   }
  }
  $$('.bayes-stage-button',root).forEach(b=>b.setAttribute('aria-pressed',
    String((b.dataset.bayesStage==='correct')===showOnlyCorrect)));
  const rounded=(posterior*100).toFixed(posterior*100%1===0?0:1);
  $('[data-bayes-known-count]',root).textContent=String(knows);
  $('[data-bayes-lucky-count]',root).textContent=String(guessedCorrect);
  $('[data-bayes-wrong-count]',root).textContent=String(guessedWrong);
  $('[data-bayes-correct-count]',root).textContent=String(correct);
  $('[data-bayes-posterior]',root).textContent=rounded+'%';
  $('[data-bayes-calculation]',root).textContent=
    'P(knew | correct) = '+knows+' / ('+knows+' + '+guessedCorrect+') = '+rounded+'%';
  readout.textContent=showOnlyCorrect?
    correct+' correct answers remain: '+knows+' from knowledge and '+guessedCorrect+
      ' from a successful guess. Incorrect answers are faded from the picture.':
    'We start with 100 fictional students: '+knows+' know the answer, '+guessedCorrect+
      ' guess correctly, and '+guessedWrong+' guess incorrectly.';
  detail.textContent=
    'P(correct | knew) = 100% in this model, but P(knew | correct) = '+rounded+
    '%. These are different conditional probabilities. A correct answer is evidence of knowledge, not proof.';
  keep.textContent=showOnlyCorrect?'Show everyone':'Show only correct answers';
  feedback.textContent='';
  feedback.className='';
 }
 knob.addEventListener('input',render);
 keep.addEventListener('click',()=>{
  showOnlyCorrect=!showOnlyCorrect;render();
 });
 challenge.addEventListener('click',()=>{
  const response=$('[data-bayes-choice]',root).value;
  if(!response){feedback.textContent='Choose an answer first.';return;}
  const correct=response==='conditional';
  feedback.className=correct?'is-correct':'';
  feedback.textContent=correct?
    'Correct. We observe that the answer was correct, then ask whether knowledge explains it. Reverse the conditioning and the question changes.':
    'Check the order: the information we are given is that the answer was correct. We want to infer whether it came from knowledge.';
 });
 render();
}
// Evidence is the actual simulated sample produced by the existing die
// code. Both the theory and the sample use its selected PMF.
function observedDistribution(){
 const root=$('[data-die-demo]');if(!root)return;
 const output=$('[data-die-frequency]',root);if(!output)return;
 const barboard=$('[data-die-frequency-bars]',root);
 const caption=$('[data-die-frequency-note]',root);
 function reset(){
  output.hidden=true;
  barboard.replaceChildren();
 }
 root.addEventListener('mlclub:die-type',reset);
 root.addEventListener('mlclub:die-roll',e=>{
  const {counts,probs,type}=e.detail;
  if(!Array.isArray(counts)||counts.length!==10||
      !Array.isArray(probs)||probs.length!==10)return;
  const total=counts.reduce((a,b)=>a+b,0);
  if(total<=0)return;
  barboard.replaceChildren();
  counts.forEach((count,i)=>{
   const col=node('div','die-frequency-col');
   const graph=node('div','die-frequency-track');
   const fill=node('span','die-frequency-fill');
   fill.style.height=(100*count/total/.65).toFixed(2)+'%';
   graph.append(fill);
   const expected=node('span','die-frequency-expected');
   expected.style.bottom=(100*probs[i]/.65).toFixed(2)+'%';
   graph.append(expected);
   const numerator=node('strong',null,String(count));
   const label=node('small',null,String(i+1));
   col.append(numerator,graph,label);
   col.setAttribute('aria-label','Face '+(i+1)+': '+count+' observed in '+total+
      ' rolls; expected about '+(total*probs[i]).toFixed(1)+' rolls');
   barboard.append(col);
  });
  output.hidden=false;
  caption.textContent='The blue bars show how often each face appeared in '+total+
    ' simulated rolls. The small horizontal markers show theoretical expected frequencies for the selected '+
    type+' distribution. A sample can differ from the model by chance.';
 });
}
// Link this lesson's probability ideas to ID3 without conflating entropy and Bayes.
function uncertainty(){
 const root=$('[data-uncertainty-studio]');if(!root)return;
 const tray=$('[data-uncertainty-dots]',root),result=$('[data-uncertainty-result]',root);
 const details=$('[data-uncertainty-math]',root);
 let active='balanced';
 const cases={
  pure:{yes:12,no:0,name:'all YES',message:'Every observed label is YES. There is no disagreement: a constant YES prediction fits these twelve examples.'},
  skewed:{yes:10,no:2,name:'mostly YES',message:'YES is common but not certain. Two observed answers disagree, so the group still contains uncertainty.'},
  balanced:{yes:6,no:6,name:'evenly split',message:'There are as many YES as NO observations. Knowing only the class frequency gives no preference for either answer.'}
 };
 const entropy=p=>(p===0||p===1)?0:-p*Math.log2(p)-(1-p)*Math.log2(1-p);
 function render(){
  const item=cases[active];
  tray.replaceChildren();
  for(let i=0;i<12;i++){
   const yes=i<item.yes;
   const tile=node('span','uncertainty-case '+(yes?'is-yes':'is-no'),yes?'✓':'×');
   tile.setAttribute('role','listitem');
   tile.setAttribute('aria-label',yes?'YES example':'NO example');
   tray.append(tile);
  }
  $$('[data-uncertainty-kind]',root).forEach(button=>button.setAttribute('aria-pressed',
    String(button.dataset.uncertaintyKind===active)));
  result.textContent=item.message;
  const p=item.yes/12;
  details.textContent='p(YES) = '+item.yes+'/12; p(NO) = '+item.no+
     '/12; H = −p log₂ p − (1−p) log₂(1−p) = '+entropy(p).toFixed(3)+
     ' bits (with 0 log₂ 0 defined as 0).';
  $('[data-uncertainty-count]',root).textContent=item.yes+' YES / '+item.no+' NO';
  $('[data-uncertainty-degree]',root).textContent=
    active==='pure'?'No label uncertainty':active==='balanced'?'Maximum binary-label uncertainty':'Some label uncertainty';
 }
 $$('[data-uncertainty-kind]',root).forEach(b=>b.addEventListener('click',()=>{
  active=b.dataset.uncertaintyKind;render();
 }));
 render();
}
bayes();
observedDistribution();
uncertainty();
})();
