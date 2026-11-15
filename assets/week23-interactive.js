/* Week 2 ID3 and Week 3 K-means: progressive textbook demonstrations. */
(() => {
"use strict";
const $$=(selector,scope=document)=>[...scope.querySelectorAll(selector)];
const $=(selector,scope=document)=>scope.querySelector(selector);
const htmlSafe=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const format=x=>Number(x).toFixed(3).replace(/0+$/,'').replace(/\.$/,'');
const weather=[
 ['sunny','calm','warm','yes'], ['sunny','calm','cold','yes'],
 ['sunny','windy','warm','yes'],['sunny','windy','cold','yes'],
 ['cloudy','calm','warm','yes'],['cloudy','calm','cold','yes'],
 ['cloudy','windy','warm','no'],['cloudy','windy','cold','no'],
 ['rainy','calm','warm','no'],['rainy','calm','cold','no'],
 ['rainy','windy','warm','no'],['rainy','windy','cold','no']];
function entropy(rows){
 if(!rows.length)return 0;
 let yes=rows.filter(r=>r[3]==='yes').length;
 return [yes/rows.length,1-yes/rows.length].reduce((sum,p)=>sum+(p? -p*Math.log2(p):0),0);
}
function groupsBy(column){
 const result=new Map();
 for(const row of weather){
  const value=row[column];
  if(!result.has(value))result.set(value,[]);
  result.get(value).push(row);
 }
 return [...result.entries()];
}
const featureCols={sky:0,wind:1,temperature:2};
for(const box of $$('[data-id3-playground]')){
 const buttons=$$('[data-id3-feature]',box),groups=$('[data-id3-groups]',box),results=$('[data-id3-gain]',box),maths=$('[data-id3-maths]',box);
 function render(feature){
  const parts=groupsBy(featureCols[feature]),initial=entropy(weather);
  const remainder=parts.reduce((sum,[_,rows])=>sum+rows.length/weather.length*entropy(rows),0);
  const gain=initial-remainder;
  buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.id3Feature===feature)));
  groups.innerHTML=parts.map(([value,rows])=>{
   const yes=rows.filter(r=>r[3]==='yes').length,no=rows.length-yes;
   return '<div class="id3-group"><strong>'+htmlSafe(value)+'</strong><small>['+yes+'+, '+no+'−] · '+rows.length+' examples</small>'+
     '<div class="id3-split-bar" role="img" aria-label="'+yes+' yes and '+no+' no">'+
      '<span class="positive" style="width:'+(100*yes/rows.length)+'%"></span>'+
      '<span class="negative" style="width:'+(100*no/rows.length)+'%"></span></div>'+
      '<small>Entropy: '+format(entropy(rows))+' bits</small></div>';
  }).join('');
  results.textContent='Initial entropy: '+format(initial)+' bits · Weighted entropy after asking: '+format(remainder)+' · Information gain: '+format(gain)+' bits.';
  maths.innerHTML='<p><code>H(after) = '+parts.map(([value,rows])=>'('+rows.length+'/12) × '+format(entropy(rows))).join(' + ')+' = '+format(remainder)+'</code></p>'+
   '<p><code>IG('+htmlSafe(feature)+') = '+format(initial)+' − '+format(remainder)+' = '+format(gain)+' bits</code>.</p>'+
   '<p>Compare this with another feature, then choose the largest information gain.</p>';
 }
 for(const button of buttons)button.addEventListener('click',()=>render(button.dataset.id3Feature));
 render('sky');
}
// Build ID3 tree with four pedagogical reveal states.
const node=(x,y,label,subtitle,colour='#ecf3f8')=>
 '<rect x="'+(x-69)+'" y="'+(y-24)+'" width="138" height="57" rx="4" fill="'+colour+'" stroke="#a8bdcc"/>'+
 '<text x="'+x+'" y="'+(y-1)+'" text-anchor="middle" class="graph-label">'+htmlSafe(label)+'</text>'+
 '<text x="'+x+'" y="'+(y+20)+'" text-anchor="middle" class="graph-small">'+htmlSafe(subtitle||'')+'</text>';
const edge=(x1,y1,x2,y2,name)=>
 '<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="#8da9ba" stroke-width="2" fill="none"/>'+
 (name?'<text x="'+((x1+x2)/2)+'" y="'+((y1+y2)/2-8)+'" class="graph-small" text-anchor="middle">'+htmlSafe(name)+'</text>':'');
for(const box of $$('[data-id3-tree]')){
 let step=0;
 const svg=$('svg',box),label=$('[data-id3-step-label]',box),explanation=$('[data-id3-step-explanation]',box),prev=$('[data-id3-previous]',box),next=$('[data-id3-next]',box);
 const explanations=[
  'Start with [6+,6−]. The labels are evenly mixed. We need a question that divides the data.',
  'Sky makes three groups. Sunny is pure yes [4+,0−]; rainy is pure no [0+,4−]. Cloudy [2+,2−] still needs a question.',
  'Only four cloudy examples remain. Among them, Wind separates the two yes from the two no. Temperature cannot.',
  'The final ID3 tree has a Sky root and a Wind test only within the cloudy branch. Trace any new example down to a leaf.'
 ];
 function render(){
  let art='';
  art+=node(365,46,'Sky?','[6+,6−]');
  if(step>=1){
   art+=edge(365,79,115,158,'sunny')+edge(365,79,365,158,'cloudy')+edge(365,79,615,158,'rainy');
   art+=node(115,186,'YES','[4+,0−]','#e7f2eb');
   art+=node(365,186,step>=2?'Wind?':'mixed','[2+,2−]');
   art+=node(615,186,'NO','[0+,4−]','#f9eee8');
  }
  if(step>=2){
   art+=edge(365,219,262,309,'calm')+edge(365,219,468,309,'windy');
   art+=node(262,335,step===3?'YES':'[2+,0−]','[2+,0−]','#e7f2eb');
   art+=node(468,335,step===3?'NO':'[0+,2−]','[0+,2−]','#f9eee8');
  }
  svg.innerHTML=art;
  label.textContent='Step '+(step+1)+' / 4';
  explanation.textContent=explanations[step];
  prev.disabled=step===0;next.disabled=step===3;
 }
 prev.addEventListener('click',()=>{step=Math.max(0,step-1);render();});
 next.addEventListener('click',()=>{step=Math.min(3,step+1);render();});
 render();
}
// K-means replay exactly matches the five-point solved exercise in Ciortuz.
const locations=[['A',-1,0],['B',1,0],['C',0,1],['D',3,0],['E',3,1]];
const first=[[-1,0],[3,1]],updated=[[0,1/3],[3,1/2]];
const sq=(p,c)=>(p[1]-c[0])**2+(p[2]-c[1])**2;
const assign=(centres)=>locations.map(p=>sq(p,centres[0])<=sq(p,centres[1])?0:1);
const initialClusters=assign(first);
const colour=['#4e83ad','#c38960'];
for(const box of $$('[data-kmeans-demo]')){
 let step=0;
 const svg=$('svg',box),prev=$('[data-kmeans-back]',box),next=$('[data-kmeans-next]',box),reset=$('[data-kmeans-reset]',box),label=$('[data-kmeans-step-label]',box),explanation=$('[data-kmeans-explain]',box),rows=$('[data-kmeans-distance-rows]',box);
 const messages=[
  'Initial centroids: μ₁ = A(−1,0), μ₂ = E(3,1). Predict which centre is nearest to B and D before pressing Next.',
  'Assignment: A, B and C belong to cluster 1; D and E belong to cluster 2. Squared error with the initial centres is J=7.',
  'Update: average each cluster’s coordinates. The new centroids are μ₁=(0,1/3) and μ₂=(3,1/2). The cost falls to J=19/6 ≈ 3.167.',
  'Reassign with the new centroids: no point changes group. Both centroids stay in place, so this K-means run has converged.'
 ];
 const px=x=>160+(x+1.5)*100,py=y=>326-y*154;
 function render(){
  const centres=step>=2?updated:first;
  const membership=step===0?null:assign(centres);
  let art='<rect x="90" y="25" width="560" height="348" fill="#fbfcfd" stroke="#d7e1ea"/>';
  for(let n=-1;n<=4;n++){let x=px(n);art+='<line x1="'+x+'" y1="25" x2="'+x+'" y2="373" stroke="#edf2f5"/><text x="'+x+'" y="396" text-anchor="middle" class="graph-small">'+n+'</text>';}
  for(let n=0;n<=2;n++){let y=py(n);art+='<line x1="90" y1="'+y+'" x2="650" y2="'+y+'" stroke="#edf2f5"/><text x="78" y="'+(y+3)+'" text-anchor="end" class="graph-small">'+n+'</text>';}
  if(step>=1)for(let i=0;i<locations.length;i++){
   const p=locations[i],c=centres[membership[i]];
   art+='<line x1="'+px(p[1])+'" y1="'+py(p[2])+'" x2="'+px(c[0])+'" y2="'+py(c[1])+'" stroke="'+colour[membership[i]]+'" stroke-dasharray="4 5" opacity=".48"/>';
  }
  locations.forEach((p,i)=>{
   let fill=membership===null?'#748998':colour[membership[i]];
   art+='<circle cx="'+px(p[1])+'" cy="'+py(p[2])+'" r="11" fill="'+fill+'" stroke="#fff" stroke-width="2"/>'+
    '<text x="'+(px(p[1])+16)+'" y="'+(py(p[2])-12)+'" class="graph-label">'+p[0]+'</text>';
  });
  centres.forEach((c,i)=>{let x=px(c[0]),y=py(c[1]);
   art+='<path d="M'+(x-14)+' '+(y-14)+' L'+(x+14)+' '+(y+14)+' M'+(x-14)+' '+(y+14)+' L'+(x+14)+' '+(y-14)+'" stroke="'+colour[i]+'" stroke-width="5" stroke-linecap="round"/>'+
     '<text x="'+x+'" y="'+(y+30)+'" class="graph-small" text-anchor="middle">μ'+(i+1)+' ('+format(c[0])+', '+format(c[1])+')</text>';
  });
  svg.innerHTML=art;
  rows.innerHTML=locations.map((p,i)=>'<tr><th>'+p[0]+'</th><td>'+format(sq(p,centres[0]))+'</td><td>'+format(sq(p,centres[1]))+'</td><td>'+(membership===null?'Predict':('Cluster '+(membership[i]+1)))+'</td></tr>').join('');
  label.textContent='Step '+(step+1)+' / 4';
  explanation.textContent=messages[step];
  prev.disabled=step===0;next.disabled=step===3;
 }
 prev.addEventListener('click',()=>{step=Math.max(0,step-1);render();});
 next.addEventListener('click',()=>{step=Math.min(3,step+1);render();});
 reset.addEventListener('click',()=>{step=0;render();});
 render();
}
// The same active Contents sidebar from Week 1 works on both Course and Laboratory.
for(const layout of $$('.week23-academic .course-layout')){
 const nav=$('.toc-panel',layout);
 if(!nav)continue;
 const mq=matchMedia('(max-width:680px)');
 const sync=()=>{nav.open=!mq.matches;};
 sync();mq.addEventListener?.('change',sync);
 const links=$$('a[href^="#"]',nav),sections=links.map(link=>document.getElementById(link.getAttribute('href').slice(1)));
 links.forEach(link=>link.addEventListener('click',()=>{if(mq.matches)nav.open=false;}));
 let scheduled=false;
 const update=()=>{
  scheduled=false;let active=0;
  sections.forEach((section,i)=>{if(section&&section.getBoundingClientRect().top<=155)active=i;});
  links.forEach((link,i)=>{if(i===active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
 };
 addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(update);}},{passive:true});
 update();
}
})();