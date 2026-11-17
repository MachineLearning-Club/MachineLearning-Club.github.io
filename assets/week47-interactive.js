/* Weeks 4–7: original dependency-free interactive school demonstrations. */
(()=>{'use strict';
const one=(s,root=document)=>root.querySelector(s),all=(s,root=document)=>[...root.querySelectorAll(s)];
const fmt=(x,d=3)=>Number(x.toFixed(d)).toString(),step=z=>Number(z>=0),sigmoid=z=>1/(1+Math.exp(-z));
const SVG='http://www.w3.org/2000/svg';
function makeSvg(svg,markup){svg.innerHTML=markup;}
const points=[{name:'A1',x:1,y:1,cls:'A'},{name:'A2',x:1,y:2,cls:'A'},{name:'A3',x:2,y:1,cls:'A'},{name:'B1',x:4,y:4,cls:'B'},{name:'B2',x:4,y:5,cls:'B'},{name:'B3',x:5,y:4,cls:'B'}];
// Week 4: K-nearest neighbours preview, with movable query coordinates.
for(const root of all('[data-revision-knn]')){
 const kSelect=one('[data-revision-k]',root),out=one('[data-revision-results]',root);
 if(!kSelect||!out)continue;
 const control=document.createElement('div');control.className='live-controls';
 control.innerHTML='<label>New point Q, x <input type="range" min="0" max="6" step=".5" value="2" data-qx></label>'+
   '<label>New point Q, y <input type="range" min="0" max="6" step=".5" value="2" data-qy></label>';
 const img=document.createElement('svg');img.setAttribute('viewBox','0 0 600 320');img.setAttribute('role','img');img.setAttribute('aria-label','Six labelled training points and a movable query point');
 control.append(img);root.insertBefore(control,out);
 const qx=one('[data-qx]',root),qy=one('[data-qy]',root);
 function render(){
  const x=+qx.value,y=+qy.value,k=+kSelect.value;
  const ranked=points.map(p=>({...p,d2:(x-p.x)**2+(y-p.y)**2})).sort((a,b)=>a.d2-b.d2||a.name.localeCompare(b.name));
  const near=ranked.slice(0,k),votes={A:near.filter(p=>p.cls==='A').length,B:near.filter(p=>p.cls==='B').length};
  const choice=votes.A===votes.B?'Tie (ask for a rule)':votes.A>votes.B?'A':'B';
  const px=v=>42+v*80,py=v=>285-v*43;
  let s='<rect x="20" y="10" width="560" height="300" fill="#fff" stroke="#d9e4eb"/>';
  for(let i=0;i<=6;i++){s+='<line x1="'+px(i)+'" y1="20" x2="'+px(i)+'" y2="300" stroke="#e6edf1"/><line x1="30" y1="'+py(i)+'" x2="565" y2="'+py(i)+'" stroke="#e6edf1"/>';}
  for(const p of points){
   const active=near.some(v=>v.name===p.name);
   if(active)s+='<line x1="'+px(x)+'" y1="'+py(y)+'" x2="'+px(p.x)+'" y2="'+py(p.y)+'" stroke="#7e9db1" stroke-dasharray="5 4"/>';
   s+='<circle cx="'+px(p.x)+'" cy="'+py(p.y)+'" r="'+(active?12:9)+'" fill="'+(p.cls==='A'?'#587fa4':'#c68b5c')+'" stroke="'+(active?'#253b4e':'white')+'" stroke-width="2"/>';
   s+='<text x="'+(px(p.x)+14)+'" y="'+(py(p.y)-11)+'" font-size="14" fill="#2c475e">'+p.name+'</text>';
  }
  s+='<circle cx="'+px(x)+'" cy="'+py(y)+'" r="13" fill="#fff" stroke="#222" stroke-width="3"/><text x="'+(px(x)+17)+'" y="'+(py(y)+18)+'" font-size="15">Q</text>';
  makeSvg(img,s);
  const evidence={query:{x,y},k,neighbours:near.map(p=>({name:p.name,cls:p.cls,d2:p.d2})),votes,prediction:choice};
  root.dataset.knnEvidence=JSON.stringify(evidence);
  root.dispatchEvent(new CustomEvent('mlclub:knn-update',{detail:evidence}));
  out.innerHTML='<p>Q = ('+fmt(x,1)+', '+fmt(y,1)+') · nearest '+k+' labels: <strong>'+near.map(p=>p.cls).join(', ')+'</strong> · votes A='+votes.A+', B='+votes.B+' · prediction: <strong>'+choice+'</strong></p>'+
   '<p class="understated">Sorted squared distances: '+ranked.map(p=>p.name+': '+fmt(p.d2,2)).join(' · ')+'</p>';
 }
 [kSelect,qx,qy].forEach(input=>input.addEventListener('input',render));render();
}
// Week 4: true six-example confusion calculation with 3 positives and 3 negatives.
for(const root of all('[data-confusion-demo]')){
 const fp=one('[data-fp]',root),fn=one('[data-fn]',root),out=one('[data-confusion-output]',root);
 if(!fp||!fn||!out)continue;
 function render(){const Fp=+fp.value,Fn=+fn.value,Tp=3-Fn,Tn=3-Fp,accuracy=(Tp+Tn)/6;
  const evidence={tp:Tp,tn:Tn,fp:Fp,fn:Fn,total:6};
  root.dataset.confusionEvidence=JSON.stringify(evidence);
  root.dispatchEvent(new CustomEvent('mlclub:confusion-update',{detail:evidence}));
  out.innerHTML='<strong>TP='+Tp+', TN='+Tn+', FP='+Fp+', FN='+Fn+'</strong> · correct '+(Tp+Tn)+'/6 · accuracy <strong>'+fmt(accuracy*100,1)+'%</strong>.'+
   '<p class="understated">Three actual positives and three actual negatives stay fixed as the two error counts change.</p>';}
 fp.addEventListener('input',render);fn.addEventListener('input',render);render();
}
// Week 5: native clickable pixels and honest border-replicating 3x3 average.
const originalPixels=[
 [230,180,230,190,230],[220,40,55,50,220],
 [230,60,230,65,230],[220,55,40,60,220],[230,220,230,220,230]];
for(const root of all('[data-pixel-lab]')){
 let data=originalPixels.map(r=>r.slice()),mode='original';
 const grid=one('[data-pixel-grid]',root),thr=one('[data-pixel-threshold]',root),value=one('[data-pixel-value]',root),summary=one('[data-pixel-narrative]',root);
 function filtered(r,c){
  const v=data[r][c];
  if(mode==='original')return v;
  if(mode==='threshold')return v<+thr.value?0:255;
  let sum=0;for(let dr=-1;dr<=1;dr++)for(let dc=-1;dc<=1;dc++){
   const rr=Math.max(0,Math.min(4,r+dr)),cc=Math.max(0,Math.min(4,c+dc));
   sum+=data[rr][cc];
  }return Math.round(sum/9);
 }
 function render(){
  value.textContent=thr.value;grid.replaceChildren();grid.setAttribute('data-mode',mode);
  let dark=0;
  for(let r=0;r<5;r++)for(let c=0;c<5;c++){
   const out=filtered(r,c);dark+=out<128?1:0;
   const button=document.createElement('button');button.type='button';button.className='pixel-cell';
   button.textContent=String(out);button.title='Row '+r+', column '+c+': original '+data[r][c]+'. Click to cycle the source value.';
   button.setAttribute('aria-label',button.title);
   button.style.background='rgb('+out+','+out+','+out+')';button.style.color=out<128?'#fff':'#172b3b';
   button.addEventListener('click',()=>{
    const cycle=[0,40,90,160,220,255],current=data[r][c];
    data[r][c]=cycle.find(v=>v>current)??cycle[0];render();
   });
   grid.append(button);
  }
  all('[data-pixel-mode]',root).forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.pixelMode===mode)));
  summary.textContent='Mode: '+({original:'original intensities',threshold:'threshold ('+thr.value+')',mean:'3×3 mean (replicate edge pixels)'}[mode])+'. '+dark+' of 25 output pixels have intensity below 128. Click any square to alter the underlying original image.';
 }
 all('[data-pixel-mode]',root).forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.pixelMode;render();}));
 const reset=one('[data-pixel-reset]',root);reset?.addEventListener('click',()=>{mode='original';data=originalPixels.map(r=>r.slice());thr.value=128;render();});
 thr.addEventListener('input',render);render();
}
// Week 5: three RGB sliders and two precisely distinguished grayscale conversions.
for(const root of all('[data-rgb-demo]')){
 const fields=all('[data-rgb]',root),preview=one('[data-rgb-preview]',root),out=one('[data-rgb-output]',root);
 function render(){
  const get=key=>+one('[data-rgb="'+key+'"]',root).value,r=get('r'),g=get('g'),b=get('b');
  const arithmetic=(r+g+b)/3,luminance=.2126*r+.7152*g+.0722*b;
  preview.style.background='rgb('+r+','+g+','+b+')';
  out.innerHTML='<code>RGB('+r+', '+g+', '+b+')</code> · arithmetic mean <strong>'+fmt(arithmetic,2)+'</strong> · weighted grayscale <strong>'+fmt(luminance,2)+'</strong>.';
 }
 fields.forEach(input=>input.addEventListener('input',render));render();
}
// Week 6: parameter-dependent line and four corner predictions.
for(const root of all('[data-perceptron-demo]')){
 const svg=one('svg',root),out=one('[data-perceptron-summary]',root),tbody=one('[data-perceptron-rows]',root),inputs=all('[data-weight]',root);
 const samples=[[0,0,0],[1,0,0],[0,1,0],[1,1,1]];
 const px=x=>185+(x+.25)*210,py=y=>289-(y+.25)*174;
 function render(){
  const vals={};inputs.forEach(input=>vals[input.dataset.weight]=+input.value);
  const {w1,w2,b}=vals;
  let art='<rect x="95" y="12" width="545" height="335" fill="white" stroke="#dce6ec"/>';
  for(let v=0;v<=1;v++){art+='<line x1="'+px(v)+'" y1="20" x2="'+px(v)+'" y2="337" stroke="#e8edf2"/><line x1="105" y1="'+py(v)+'" x2="630" y2="'+py(v)+'" stroke="#e8edf2"/>';}
  if(Math.abs(w2)>.000001){const a=(-b-w1*(-.25))/w2,c=(-b-w1*1.25)/w2;
   art+='<line x1="'+px(-.25)+'" y1="'+py(a)+'" x2="'+px(1.25)+'" y2="'+py(c)+'" stroke="#2a668b" stroke-width="3"/>';
  }else if(Math.abs(w1)>.000001){let x=-b/w1;art+='<line x1="'+px(x)+'" y1="15" x2="'+px(x)+'" y2="345" stroke="#2a668b" stroke-width="3"/>';}
  let errors=0;
  tbody.innerHTML=samples.map(([x,y,target])=>{
   const z=w1*x+w2*y+b,p=step(z);errors+=Number(p!==target);
   art+='<circle cx="'+px(x)+'" cy="'+py(y)+'" r="12" fill="'+(p?'#528a6c':'#c18a61')+'" stroke="'+(p===target?'#fff':'#a12d2d')+'" stroke-width="3"/>'+
    '<text x="'+(px(x)+15)+'" y="'+(py(y)-14)+'" font-size="13">('+x+','+y+')</text>';
   return '<tr><td>('+x+', '+y+')</td><td>'+fmt(z,2)+'</td><td>'+p+'</td><td>'+target+'</td></tr>';
  }).join('');
  makeSvg(svg,art);
  out.textContent='z='+fmt(w1,2)+'x₁ + '+fmt(w2,2)+'x₂ + ('+fmt(b,2)+'). '+errors+' / 4 training rows currently misclassified.';
 }
 inputs.forEach(i=>i.addEventListener('input',render));
 one('[data-perceptron-reset]',root)?.addEventListener('click',()=>{inputs.forEach(i=>i.value={w1:1,w2:1,b:-1.5}[i.dataset.weight]);render();});
 render();
}
// Week 6: explicit online perceptron learning with per-example diagnostics.
for(const root of all('[data-perceptron-train]')){
 const examples=[[0,0,0],[1,0,0],[0,1,0],[1,1,1]];
 const rate=one('[data-train-rate]',root),output=one('[data-train-output]',root);
 let w1=0,w2=0,b=-1,index=0,history=[];
 function report(){output.textContent=
  'Learning rate η = '+rate.value+'\\nCurrent weights: w₁='+fmt(w1,2)+', w₂='+fmt(w2,2)+', bias='+fmt(b,2)+'\\n'+
  'Errors on four AND examples: '+examples.filter(([x,y,t])=>step(w1*x+w2*y+b)!==t).length+
  '\\n'+history.slice(-12).join('\\n');
 }
 function oneStep(){
  const [x,y,t]=examples[index%4],prediction=step(w1*x+w2*y+b),e=t-prediction,eta=+rate.value;
  w1+=eta*e*x;w2+=eta*e*y;b+=eta*e;
  history.push('#'+(index+1)+' input ('+x+','+y+') target '+t+' predicted '+prediction+
    ' error '+e+' → ('+fmt(w1,2)+', '+fmt(w2,2)+', '+fmt(b,2)+')');
  index++;report();
 }
 one('[data-train-step]',root)?.addEventListener('click',oneStep);
 one('[data-train-epoch]',root)?.addEventListener('click',()=>{for(let i=0;i<4;i++)oneStep();});
 one('[data-train-reset]',root)?.addEventListener('click',()=>{w1=0;w2=0;b=-1;index=0;history=[];report();});
 rate.addEventListener('input',report);report();
}
// Week 7: every hidden calculation of a Boolean XOR network.
for(const root of all('[data-xor-demo]')){
 const x1=one('[data-xor-x1]',root),x2=one('[data-xor-x2]',root),svg=one('svg',root),out=one('[data-xor-explain]',root);
 function render(){
  const a=+x1.value,b=+x2.value,z1=a+b-.5,z2=a+b-1.5,h1=step(z1),h2=step(z2),zo=h1-2*h2-.5,y=step(zo);
  let art='<rect width="720" height="340" fill="#fff"/>';
  for(const [x,y1,x2,y2,label] of [
    [110,90,350,85,'+1'],[110,90,350,235,'+1'],
    [110,250,350,85,'+1'],[110,250,350,235,'+1'],
    [390,85,595,160,'+1'],[390,235,595,160,'−2']]){
    art+='<line x1="'+x+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="#a4bdce" stroke-width="2"/>';
  }
  const nodes=[[100,90,'x₁='+a],[100,250,'x₂='+b],[365,85,'OR='+h1],[365,235,'AND='+h2],[604,160,'ŷ='+y]];
  for(const [x,y0,label] of nodes){art+='<circle cx="'+x+'" cy="'+y0+'" r="41" fill="#f6fafc" stroke="#7294aa" stroke-width="2"/>'+
   '<text x="'+x+'" y="'+(y0+4)+'" text-anchor="middle" font-size="15" fill="#234a65">'+label+'</text>';}
  makeSvg(svg,art);
  out.innerHTML='Input ('+a+', '+b+'): <code>OR: '+fmt(z1,1)+' → '+h1+
   '</code>; <code>AND: '+fmt(z2,1)+' → '+h2+
   '</code>; <code>output: '+fmt(zo,1)+' → '+y+
   '</code>. Expected XOR='+Number(a!==b)+'.';
 }
 [x1,x2].forEach(s=>s.addEventListener('change',render));render();
}
// Week 7: staged sigmoid forward, loss, gradient and parameter update.
for(const root of all('[data-gradient-demo]')){
 const input=one('[data-gradient-rate]',root),out=one('[data-gradient-output]',root);
 let stage=0;
 function render(){
  const eta=+input.value,pred=.5,loss=.125,grad=-.125,updated=eta*.125;
  const y2=sigmoid(updated),l2=.5*(1-y2)**2;
  const messages=[
   '<strong>1. Forward pass:</strong> w=0, x=1, b=0 → z=0 → ŷ=σ(0)=0.5.',
   '<strong>2. Loss:</strong> ½×(target−prediction)² = ½×(1−0.5)² = 0.125.',
   '<strong>3. Gradient:</strong> (0.5−1)×0.5×(1−0.5)×1 = −0.125.',
   '<strong>4. Update:</strong> new w = 0−'+fmt(eta,2)+'×(−0.125) = '+fmt(updated,4)+
    '. New output '+fmt(y2,5)+'; new loss '+fmt(l2,6)+' (old 0.125).'
  ];
  out.innerHTML='<p>Step '+(stage+1)+' of 4 · learning rate η='+fmt(eta,2)+'</p><p>'+messages[stage]+'</p>';
  const next=one('[data-gradient-next]',root);if(next)next.disabled=stage===3;
 }
 one('[data-gradient-next]',root)?.addEventListener('click',()=>{stage=Math.min(3,stage+1);render();});
 one('[data-gradient-reset]',root)?.addEventListener('click',()=>{stage=0;render();});
 input.addEventListener('input',render);render();
}
})();