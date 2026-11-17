/* Week 02 probability-to-ID3 visual bridge.
 * All counts and scores are computed from the published twelve-row diary.
 * No cloned hidden dataset or predefined gains. Zero probabilities contribute
 * zero to entropy by continuous extension of p log2(p).
 */
(()=>{
'use strict';
const $=(selector,root=document)=>root.querySelector(selector);
const $$=(selector,root=document)=>[...root.querySelectorAll(selector)];
const el=(tag,className,text)=>{
 const n=document.createElement(tag);
 if(className)n.className=className;
 if(text!==undefined)n.textContent=text;
 return n;
};
const studio=$('[data-id3-probability]');
const playground=$('[data-id3-playground]');
const diary=$('#w2-data .teaching-data tbody');
if(!studio||!playground||!diary)return;
const records=$$('tr',diary).map(tr=>{
 const cols=$$('td',tr).map(td=>td.textContent.trim().toLowerCase());
 if(cols.length!==5)throw Error('The ID3 diary needs five columns');
 return {id:Number(cols[0]),sky:cols[1],wind:cols[2],
         temperature:cols[3],label:cols[4]};
});
if(records.length!==12||new Set(records.map(r=>r.id)).size!==12 ||
    records.some(r=>!['yes','no'].includes(r.label)))
 throw Error('Expected twelve unique, binary-labelled diary records');
const entropy=rows=>{
 if(!rows.length)return 0;
 const p=rows.filter(row=>row.label==='yes').length/rows.length;
 return p<=0||p>=1?0:-p*Math.log2(p)-(1-p)*Math.log2(1-p);
};
const split=(rows,feature)=>{
 const groups=new Map();
 rows.forEach(row=>{
  if(!groups.has(row[feature]))groups.set(row[feature],[]);
  groups.get(row[feature]).push(row);
 });
 return [...groups.entries()];
};
const after=(rows,feature)=>split(rows,feature).reduce((sum,[name,group])=>
 sum+(group.length/rows.length)*entropy(group),0);
const infoGain=(rows,feature)=>entropy(rows)-after(rows,feature);
const fmt=n=>(Math.abs(n)<0.0005?0:n).toFixed(3);
const percent=n=>(n*100).toFixed(0)+'%';
const labels={sky:'Sky',wind:'Wind',temperature:'Temperature'};
const rootEntropy=entropy(records);
const gains=Object.fromEntries(Object.keys(labels).map(name=>[name,infoGain(records,name)]));
if(Math.abs(rootEntropy-1)>1e-10)throw Error('Diary root entropy has changed; inspect lesson');
function makeTile(label){
 const tile=el('span','id3-prob-tile '+(label==='yes'?'is-yes':'is-no'),label==='yes'?'✓':'×');
 tile.title=label==='yes'?'Recorded YES':'Recorded NO';
 tile.setAttribute('role','listitem');
 tile.setAttribute('aria-label',label==='yes'?'YES label':'NO label');
 return tile;
}
const labelsRoot=$('[data-id3-prob-total]',studio);
records.forEach(row=>labelsRoot.append(makeTile(row.label)));
const numYes=records.filter(row=>row.label==='yes').length;
$('[data-id3-prob-root-ratio]',studio).textContent=
 numYes+'/'+records.length+' YES, '+(records.length-numYes)+'/'+records.length+' NO';
$('[data-id3-prob-root-h]',studio).textContent='H = '+fmt(rootEntropy)+' bit';
function branchCard(name,group,feature,total){
 const yes=group.filter(row=>row.label==='yes').length;
 const no=group.length-yes;
 const p=yes/group.length;
 const localH=entropy(group);
 const contribution=localH*group.length/total;
 const card=el('article','id3-prob-branch');
 card.dataset.branch=name;
 const head=el('div','id3-prob-branch-head');
 head.append(el('strong',null,feature+' = '+name));
 head.append(el('span','id3-prob-size',group.length+'/'+total+' records'));
 card.append(head);
 const splitbar=el('div','id3-prob-pair-bar');
 splitbar.setAttribute('role','img');
 splitbar.setAttribute('aria-label',yes+' YES and '+no+' NO of '+group.length+' records');
 const yesBar=el('span','id3-prob-yesbar');
 const noBar=el('span','id3-prob-nobar');
 yesBar.style.width=percent(p);
 noBar.style.width=percent(1-p);
 splitbar.append(yesBar,noBar);
 const ratio=el('p','id3-prob-branch-ratio',
   'P(YES | '+name+') = '+yes+'/'+group.length+' = '+percent(p));
 const stats=el('div','id3-prob-branch-stats');
 stats.append(el('span',null,'Entropy: '+fmt(localH)+' bits'));
 stats.append(el('span',null,'Weighted part: '+
     group.length+'/'+total+' × '+fmt(localH)+' = '+fmt(contribution)));
 const explanation=el('small',null,localH<0.0001?
   'Pure answers: no label uncertainty within this group.':
   Math.abs(p-.5)<0.0001?
    'Half YES, half NO: maximal binary-label uncertainty.':
    'Unequal YES/NO proportions: some uncertainty remains.');
 card.append(splitbar,ratio,stats,explanation);
 return card;
}
function render(feature){
 const groups=split(records,feature);
 const afterH=after(records,feature);
 const gain=infoGain(records,feature);
 const target=$('[data-id3-prob-branches]',studio);
 target.replaceChildren(...groups.map(([name,rows])=>branchCard(name,rows,feature,records.length)));
 $('[data-id3-prob-before]',studio).textContent=fmt(rootEntropy)+' bits';
 $('[data-id3-prob-after]',studio).textContent=fmt(afterH)+' bits';
 $('[data-id3-prob-gain]',studio).textContent=fmt(gain)+' bits';
 const remaining=100*(afterH/rootEntropy);
 $('[data-id3-prob-remaining]',studio).style.width=remaining.toFixed(4)+'%';
 $('[data-id3-prob-learned]',studio).style.width=(100-remaining).toFixed(4)+'%';
 $('[data-id3-prob-conclusion]',studio).textContent=feature==='sky'?
   'Sky is the best first question in this diary. It creates two pure groups and leaves only the cloudy group mixed.':
   feature==='wind'?
   'Wind leaves both large groups mixed. Despite being useful later inside cloudy days, it removes very little uncertainty at the root.':
   'Temperature makes two equally mixed groups, so it removes no uncertainty at all.';
 $$('[data-id3-prob-feature]',studio).forEach(button=>button.setAttribute(
  'aria-pressed',String(button.dataset.id3ProbFeature===feature)));
 const formula=groups.map(([name,rows])=>
  '('+rows.length+'/'+records.length+') × '+fmt(entropy(rows))).join(' + ');
 $('[data-id3-prob-formula]',studio).textContent=
  'H(after | '+feature+') = '+formula+' = '+fmt(afterH)+' bits. '+
  'IG('+feature+') = H(before) − H(after) = '+fmt(rootEntropy)+' − '+fmt(afterH)+
  ' = '+fmt(gain)+' bits.';
 const ranks=$('[data-id3-prob-ranking]',studio);
 ranks.replaceChildren(...Object.keys(labels).sort((a,b)=>gains[b]-gains[a]).map((name,i)=>{
  const button=el('button','id3-prob-rank');
  button.type='button';
  button.dataset.id3ProbSelect=name;
  button.setAttribute('aria-pressed',String(name===feature));
  const title=el('span','id3-prob-rank-name',(i+1)+'. '+labels[name]);
  const barbox=el('span','id3-prob-rank-bar');
  const bar=el('i');
  bar.style.width=(100*gains[name]/rootEntropy).toFixed(3)+'%';
  barbox.append(bar);
  const val=el('strong',null,fmt(gains[name])+' bits');
  button.append(title,barbox,val);
  button.addEventListener('click',()=>{
   const original=$('[data-id3-feature="'+name+'"]',playground);
   if(original)original.click();
   else render(name);
  });
  return button;
 }));
}
function showCloudy(feature){
 const rows=records.filter(r=>r.sky==='cloudy');
 if(rows.length!==4)throw Error('The cloudy subset should have four examples');
 const before=entropy(rows),afterH=after(rows,feature),gain=infoGain(rows,feature);
 const output=$('[data-id3-prob-cloudy-output]',studio);
 output.replaceChildren();
 const headline=el('p','id3-prob-local-score',
  'Only 4 cloudy rows · H(before) = '+fmt(before)+' bits · H(after) = '+
  fmt(afterH)+' bits · Gain = '+fmt(gain)+' bits');
 const grid=el('div','id3-prob-local-grid');
 split(rows,feature).forEach(([name,group])=>
   grid.append(branchCard(name,group,feature,rows.length)));
 output.append(headline,grid);
 output.append(el('p','id3-prob-local-message',feature==='wind'?
   'Wind separates calm [2 YES, 0 NO] from windy [0 YES, 2 NO]. It eliminates all uncertainty inside the cloudy branch.':
   'Temperature divides into warm and cold, but both contain one YES and one NO. The uncertainty stays at 1 bit.'));
 $$('[data-id3-prob-cloudy]',studio).forEach(button=>button.setAttribute(
   'aria-pressed',String(button.dataset.id3ProbCloudy===feature)));
}
$$('[data-id3-prob-feature]',studio).forEach(button=>button.addEventListener('click',()=>{
 const original=$('[data-id3-feature="'+button.dataset.id3ProbFeature+'"]',playground);
 if(original)original.click();
}));
$$('[data-id3-feature]',playground).forEach(button=>
 button.addEventListener('click',()=>render(button.dataset.id3Feature)));
$$('[data-id3-prob-cloudy]',studio).forEach(button=>button.addEventListener('click',()=>
 showCloudy(button.dataset.id3ProbCloudy)));
render('sky');
showCloudy('wind');
// Pure numerical helpers available for transparent browser regression tests.
window.MLClubID3Probability=Object.freeze({
 entropy:rows=>entropy(rows),
 gain:(rows,feature)=>infoGain(rows,feature),
 rows:records.map(row=>({...row})),
 rootGains:{...gains}
});
})();
