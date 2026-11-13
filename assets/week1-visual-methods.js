/* Week 1: elements inside the diagrams are the controls. The models are illustrative teaching examples. */
(() => {
"use strict";
const $=(q,root=document)=>root.querySelector(q);
const $$=(q,root=document)=>[...root.querySelectorAll(q)];
const svg=(content)=>'<svg viewBox="0 0 300 155" role="group" aria-label="Interactive model diagram" class="interactive-model-svg">'+content+'</svg>';
const line=(x1,y1,x2,y2,stroke="#99b2c2",width=2)=>'<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+stroke+'" stroke-width="'+width+'"/>';
const circle=(x,y,r,fill,extra="")=>'<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+fill+'" stroke="#5b88a5" stroke-width="2" '+extra+'/>';
const txt=(x,y,value,size=13)=>'<text x="'+x+'" y="'+y+'" font-size="'+size+'" fill="#355a72" text-anchor="middle" pointer-events="none">'+value+'</text>';
const toggleElement=(el,fn,label)=>{
  el.setAttribute("role","button");el.setAttribute("tabindex","0");el.setAttribute("aria-label",label);
  el.classList.add("graphic-control");
  el.addEventListener("click",fn);
  el.addEventListener("keydown",event=>{if(event.key==="Enter"||event.key===" "){event.preventDefault();fn();}});
};
const setOut=(card,message)=>{const out=$("[data-method-output]",card);if(out)out.textContent=message;};
const cards=Object.fromEntries($$("[data-model-interactive]").map(card=>[card.dataset.method,card]));
const stage=(kind,body)=>{const root=$("[data-method-stage]",cards[kind]);root.innerHTML=body;return root;};

if(cards.vision){
  const card=cards.vision;
  const root=stage("vision",'<div class="cv-microgrid" role="group" aria-label="Five by five editable pixels"></div><div class="cv-micro-output"><strong data-cv-result></strong><span>Tap the squares to change the image</span></div>');
  const grid=$(".cv-microgrid",root);
  const initial=["00100","00100","00100","00100","00100"].join("").split("").map(x=>x==="1");
  const states=[...initial], buttons=[];
  function render(){
    buttons.forEach((b,i)=>{b.classList.toggle("on",states[i]);b.setAttribute("aria-pressed",String(states[i]));});
    const inColumn=[2,7,12,17,22].filter(i=>states[i]).length;
    const others=states.filter((on,i)=>on&&i%5!==2).length;
    const seen=inColumn>=4&&others<=4;
    $("[data-cv-result]",root).textContent=seen?"Vertical stroke":"Other pattern";
    setOut(card,(seen?"Vertical stroke recognised.":"Pattern not recognised.")+" Active pixels: "+states.filter(Boolean).length+"/25.");
  }
  states.forEach((_,i)=>{
    const b=document.createElement("button");b.type="button";b.className="cv-pixel";b.setAttribute("aria-label","Toggle image pixel row "+(Math.floor(i/5)+1)+" column "+(i%5+1));
    b.addEventListener("click",()=>{states[i]=!states[i];render();});
    grid.appendChild(b);buttons.push(b);
  });
  render();
}

if(cards.linear){
  const card=cards.linear;
  const delta=[0,0,0,0,0],xs=[1,2,3,4,5],ys=[2,3,4,5,6];
  function render(){
    const values=ys.map((y,i)=>y+delta[i]); const xMean=3, yMean=values.reduce((a,b)=>a+b,0)/5;
    const slope=xs.reduce((s,x,i)=>s+(x-xMean)*(values[i]-yMean),0)/10;
    const intercept=yMean-3*slope;
    const X=x=>27+x*38, Y=y=>130-y*13;
    let body=line(20,135,285,135)+"<path d='M22 18V136' fill='none' stroke='#a0b5c4' stroke-width='2'/>";
    body+='<path d="M'+X(0.5)+' '+Y(intercept+slope*.5)+'L'+X(6.3)+' '+Y(intercept+slope*6.3)+'" fill="none" stroke="#467eaa" stroke-width="3"/>';
    body+=xs.map((x,i)=>circle(X(x),Y(values[i]),9,"#b78761",'data-point="'+i+'"')).join("");
    body+=circle(X(6),Y(intercept+slope*6),5,"#4c85ab")+txt(255,149,"Next x=6",11);
    const root=stage("linear",svg(body));
    $$("[data-point]",root).forEach((node,i)=>toggleElement(node,()=>{delta[i]=delta[i]===0?2:0;render();},"Move observation "+(i+1)));
    setOut(card,"Fitted line: predict "+(intercept+slope*6).toFixed(2)+" when x = 6.");
  }
  render();
}

if(cards.perceptron){
  const card=cards.perceptron, inputs=[1,0,1],pos=[32,79,126];
  function render(){
    const sum=inputs.reduce((a,b)=>a+b,0),out=sum>=2?1:0;
    let body=pos.map(y=>line(67,y,196,79,inputs[pos.indexOf(y)]?"#427f9f":"#c8d3db")).join("");
    body+=line(222,79,273,79,out?"#448b6b":"#a2b6c4",3);
    body+=pos.map((y,i)=>circle(48,y,18,inputs[i]?"#a9d1e3":"#edf2f5",'data-input="'+i+'"')+txt(48,y+5,"x"+(i+1),13)).join("");
    body+=circle(209,79,24,out?"#b9ddc7":"#edf3f7")+txt(209,85,"Σ",19)+txt(272,73,String(out),18)+txt(155,145,"Sum "+sum+" / threshold 2",12);
    const root=stage("perceptron",svg(body));
    $$("[data-input]",root).forEach((node,i)=>toggleElement(node,()=>{inputs[i]=1-inputs[i];render();},"Toggle input "+(i+1)));
    setOut(card,"Inputs ["+inputs.join(", ")+"] give sum "+sum+" → output "+out+".");
  }render();
}

if(cards.network){
  const card=cards.network,inputs=[1,0];
  function render(){
    const hidden=[inputs[0]||inputs[1]?1:0,inputs[0]&&inputs[1]?1:0,inputs[1]?1:0];
    const output=hidden[0]&&hidden[1]?1:0;
    const ip=[43,111],hp=[25,77,129],op=[77];
    let body="";
    ip.forEach((yi,i)=>hp.forEach(yh=>{body+=line(60,yi,147,yh,inputs[i]?"#7baac5":"#d6dfe5",inputs[i]?2.5:1.3);}));
    hp.forEach((yh,i)=>{body+=line(169,yh,260,77,hidden[i]?"#7baac5":"#d6dfe5",hidden[i]?2.5:1.3);});
    body+=ip.map((y,i)=>circle(49,y,17,inputs[i]?"#94c4e1":"#f0f4f7",'data-input="'+i+'"')+txt(49,y+4,"x"+(i+1),12)).join("");
    body+=hp.map((y,i)=>circle(158,y,15,hidden[i]?"#8bb8d2":"#eef3f7")).join("");
    body+=circle(271,77,18,output?"#83b99c":"#eef3f7")+txt(271,82,output?"1":"0",14);
    body+=txt(151,153,"Illustrative activations",11);
    const root=stage("network",svg(body));
    $$("[data-input]",root).forEach((node,i)=>toggleElement(node,()=>{inputs[i]=1-inputs[i];render();},"Toggle neural network input "+(i+1)));
    setOut(card,"Input signals change hidden nodes and the illustrative binary output "+output+".");
  }render();
}

if(cards.forest){
  const card=cards.forest,votes=[1,0,1];
  function render(){
    const yes=votes.reduce((a,b)=>a+b,0),winner=yes>=2?"YES":"NO";
    let body="";
    votes.forEach((vote,i)=>{
      const x=55+i*95;
      body+='<g data-tree="'+i+'" class="svg-tree-vote">';
      body+=line(x,35,x,68,vote?"#4b8d72":"#bb916e",2.5)+line(x,68,x-27,86,vote?"#4b8d72":"#bb916e",2.5)+line(x,68,x+27,86,vote?"#4b8d72":"#bb916e",2.5);
      body+=circle(x,32,15,vote?"#a6d2bd":"#f2daca")+circle(x-27,89,8,vote?"#a6d2bd":"#f2daca")+circle(x+27,89,8,vote?"#a6d2bd":"#f2daca")+txt(x,36,String(i+1),12);
      body+=txt(x,119,vote?"YES":"NO",13);
      body+='</g>';
    });
    body+=txt(150,147,"Majority → "+winner+" ("+yes+"/3 YES)",14);
    const root=stage("forest",svg(body));
    $$("[data-tree]",root).forEach((g,i)=>toggleElement(g,()=>{votes[i]=1-votes[i];render();},"Toggle tree "+(i+1)+" vote"));
    setOut(card,yes+" out of 3 trees vote YES; forest prediction: "+winner+".");
  }render();
}

if(cards.kmeans){
  const card=cards.kmeans;
  const base=[[40,48],[60,86],[88,59],[105,105],[188,42],[214,67],[235,91],[256,110]];
  const switched=Array(8).fill(false);
  function render(){
    const points=base.map(([x,y],i)=>[switched[i]?300-x:x,y]);
    const assignments=points.map(([x])=>x<150?0:1);
    const groups=[0,1].map(group=>points.filter((_,i)=>assignments[i]===group));
    const centres=groups.map((g,i)=>g.length?[
      g.reduce((s,p)=>s+p[0],0)/g.length,
      g.reduce((s,p)=>s+p[1],0)/g.length
    ]:[i?230:70,75]);
    let body=line(150,11,150,139,"#e0e8ee",1.5);
    body+=points.map(([x,y],i)=>circle(x,y,8,assignments[i]===0?"#6d9fc0":"#c79b75",'data-point="'+i+'"')).join("");
    centres.forEach(([x,y],i)=>{
      body+=line(x-13,y,x+13,y,i?"#b67e56":"#467f9f",3)+line(x,y-13,x,y+13,i?"#b67e56":"#467f9f",3);
    });
    body+=txt(150,149,groups[0].length+" blue / "+groups[1].length+" ochre",12);
    const root=stage("kmeans",svg(body));
    $$("[data-point]",root).forEach((node,i)=>toggleElement(node,()=>{switched[i]=!switched[i];render();},"Move point "+(i+1)+" to the other side"));
    setOut(card,"Assign to the nearest of two fixed seeds, then recalculate each group's centre (the + marks).");
  }render();
}
if(cards.hierarchical){
  const card=cards.hierarchical, labels=["A","B","C","D"];let current=-1;
  function render(){
    const branch=current>=0?(current<2?0:1):-1;
    let body='';
    body+='<path d="M38 107V73H106V107M72 73V34H220V73M186 107V73H254V107M220 73V34" stroke="#a7bbc9" stroke-width="3" fill="none"/>';
    if(branch===0)body+='<path d="M38 107V73H106V107M72 73V34" stroke="#4f86aa" stroke-width="5" fill="none"/>';
    if(branch===1)body+='<path d="M186 107V73H254V107M220 73V34" stroke="#bd8d64" stroke-width="5" fill="none"/>';
    [38,106,186,254].forEach((x,i)=>{
      body+=circle(x,107,10,current===i?"#b5d9eb":"#eff4f7",'data-leaf="'+i+'"')+txt(x,130,labels[i],13);
    });
    body+=txt(150,151,branch<0?"Tap a leaf to trace its group":branch===0?"Pair (A, B)":"Pair (C, D)",12);
    const root=stage("hierarchical",svg(body));
    $$("[data-leaf]",root).forEach((node,i)=>toggleElement(node,()=>{current=i===current?-1:i;render();},"Select hierarchy leaf "+labels[i]));
    setOut(card,branch<0?"Choose a leaf to identify its nearby partner.":"Leaf "+labels[current]+" belongs to the ("+(branch===0?"A,B":"C,D")+") pair.");
  }render();
}
if(cards.reinforcement){
  const card=cards.reinforcement;let pos=0,reward=0;
  function render(){
    let body="";
    for(let i=0;i<9;i++){
      const row=Math.floor(i/3),col=i%3,x=39+col*80,y=12+row*43,wall=i===4,goal=i===8;
      const fill=pos===i?"#a7c9e0":wall?"#f3e4d9":goal?"#dcf0df":"#f7fafc";
      body+='<g data-cell="'+i+'" class="rl-svg-cell"><rect x="'+x+'" y="'+y+'" width="64" height="35" rx="2" fill="'+fill+'" stroke="#b5cbd9"/>'+txt(x+32,y+23,pos===i?"●":wall?"×":goal?"★":"",18)+'</g>';
    }
    body+=txt(150,152,"Total reward "+reward,13);
    const root=stage("reinforcement",svg(body)+'<button type="button" class="method-reset">Reset agent</button>');
    $$("[data-cell]",root).forEach((node,i)=>toggleElement(node,()=>{
      if(i===pos)return;
      const dist=Math.abs(Math.floor(i/3)-Math.floor(pos/3))+Math.abs(i%3-pos%3);
      if(dist!==1){setOut(card,"Choose an adjacent square; the agent can move only one step.");return;}
      if(i===4){reward-=2;setOut(card,"Blocked square: reward −2. Select another adjacent square.");render();return;}
      pos=i;reward+=i===8?10:-1;render();
    },"Move agent to grid cell "+(i+1)));
    $(".method-reset",root).addEventListener("click",()=>{pos=0;reward=0;render()});
    setOut(card,pos===8?"Reached the goal: +10 reward. Try Reset.":"Select an adjacent square; reach ★ while avoiding ×.");
  }render();
}
if(cards.generation){
  const card=cards.generation;
  const samples=[
    ["Describe","A small tree grows beside a stream."],
    ["Summarise","The passage discusses a tree and a stream."],
    ["Translate","Un arbre pousse près d'un ruisseau."]
  ];
  const root=stage("generation",'<div class="gen-picture"><div class="gen-prompt-options" role="group" aria-label="Choose a sample prompt"></div><div class="gen-output"><strong>Prepared example output</strong><p data-gen-text></p></div></div>');
  const group=$(".gen-prompt-options",root),buttons=[];
  samples.forEach(([label],i)=>{
    const b=document.createElement("button");b.type="button";b.textContent=label;
    b.addEventListener("click",()=>choose(i));
    group.appendChild(b);buttons.push(b);
  });
  function choose(i){
    buttons.forEach((button,j)=>button.setAttribute("aria-pressed",String(i===j)));
    $("[data-gen-text]",root).textContent=samples[i][1];
    setOut(card,"This is a prepared illustration of "+samples[i][0].toLowerCase()+", not a live generative model.");
  }
  choose(0);
}

const camera=$("[data-camera-system]");
if(camera){
 const grid=$("[data-camera-pixels]",camera),buttons=[],state=Array(49).fill(false);
 const blank=()=>Array(49).fill(false);
 const obstacle=()=>{
   const s=blank();
   for(let r=2;r<=4;r++)for(let c=2;c<=4;c++)s[r*7+c]=true;
   s[1*7+3]=true;s[5*7+3]=true;
   return s;
 };
 const first=obstacle();
 function apply(values){values.forEach((x,i)=>state[i]=x);render();}
 function render(){
   buttons.forEach((b,i)=>{b.classList.toggle("on",state[i]);b.setAttribute("aria-pressed",String(state[i]));});
   const count=state.filter(Boolean).length,detected=count>=8;
   $("[data-camera-class]",camera).textContent=detected?"Obstacle":"Clear";
   const action=$("[data-camera-action]",camera);
   action.textContent=detected?"STOP":"GO";
   action.classList.toggle("stop",detected);
   $$("[data-network-nodes] circle",camera).forEach((node,i)=>{
     node.setAttribute("fill",(i<3?count>i*3:i<6?count>(i-3)*4:detected)?"#83b3ce":"#eff4f7");
   });
 }
 for(let i=0;i<49;i++){
   const btn=document.createElement("button");btn.type="button";btn.className="camera-pixel";
   btn.setAttribute("aria-label","Toggle camera pixel row "+(Math.floor(i/7)+1)+" column "+(i%7+1));
   btn.addEventListener("click",()=>{state[i]=!state[i];render();});grid.appendChild(btn);buttons.push(btn);
 }
 $$("[data-camera-preset]",camera).forEach(button=>button.addEventListener("click",()=>{
   const which=button.dataset.cameraPreset;
   apply(which==="empty"?blank():obstacle());
 }));
 apply(first);
}
})();
