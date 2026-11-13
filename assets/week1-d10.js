
/* Week 1: ten-sided dice, conditional probability, distributions, and method diagrams. */
(() => {
  "use strict";
  const q=(s,root=document)=>root.querySelector(s);
  const probability=q("[data-d10-probability]");
  if(probability){
    const grid=q("[data-d10-cells]",probability);
    const fraction=q("[data-d10-fraction]",probability);
    const reason=q("[data-d10-reason]",probability);
    const label=q("[data-d10-formula-label]",probability);
    const modes=[...probability.querySelectorAll("[data-d10-mode]")];
    const faces=[];
    let chosen=4,mode="all";
    for(let n=1;n<=10;n++){
      const button=document.createElement("button");
      button.type="button";
      button.className="d10-number";
      button.textContent=String(n);
      button.setAttribute("aria-label","Guess face "+n);
      button.addEventListener("click",()=>{chosen=n;render()});
      grid.appendChild(button);
      faces.push(button);
    }
    function render(){
      const even=mode==="even";
      const eligible=even?5:10;
      const won=!even||chosen%2===0;
      const favorable=won?1:0;
      faces.forEach((button,index)=>{
        const number=index+1;
        button.classList.toggle("excluded",even&&number%2===1);
        button.classList.toggle("chosen",chosen===number);
        button.setAttribute("aria-pressed",String(chosen===number));
      });
      modes.forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.d10Mode===mode)));
      label.textContent=even?"After the clue: the result is even":"Before the clue";
      fraction.textContent=favorable+" in "+eligible+" · "+(100*favorable/eligible).toFixed(0)+"%";
      reason.textContent=even
       ?won?"Face "+chosen+" is one of the five remaining even outcomes.":"Face "+chosen+" is odd, so it is ruled out by the clue."
       :"Face "+chosen+" is one of ten equally likely outcomes.";
    }
    modes.forEach(button=>button.addEventListener("click",()=>{mode=button.dataset.d10Mode;render()}));
    render();
  }
  const demo=q("[data-die-demo]");
  if(!demo)return;
  const distributions={
    fair:{
      name:"Fair", probs:Array(10).fill(.10),
      explanation:"All ten faces are equally likely. E[X] = (1 + 2 + … + 10) / 10 = 5.50."
    },
    loaded:{
      name:"Loaded", probs:[.55,...Array(9).fill(.05)],
      explanation:"Face 1 is much more likely: E[X] = 1 × 0.55 + 0.05 × (2 + … + 10) = 3.25."
    },
    tricky:{
      name:"Tricky", probs:[.30,...Array(8).fill(.05),.30],
      explanation:"The extremes are favoured: E[X] = 0.30 × (1 + 10) + 0.05 × (2 + … + 9) = 5.50. The average hides the bias."
    }
  };
  const chart=q("[data-die-chart]",demo);
  const meanEl=q("[data-die-mean]",demo);
  const sumEl=q("[data-die-sum]",demo);
  const pmfEl=q("[data-die-pmf]",demo);
  const noteEl=q("[data-die-note]",demo);
  const sample=q("[data-die-observed]",demo);
  const svgNS="http://www.w3.org/2000/svg";
  const make=(tag,attrs,content)=>{
    const el=document.createElementNS(svgNS,tag);
    for(const [key,value] of Object.entries(attrs))el.setAttribute(key,String(value));
    if(content!==undefined)el.textContent=String(content);
    return el;
  };
  let selected="fair";
  function expected(probs){
    return probs.reduce((sum,p,i)=>sum+(i+1)*p,0);
  }
  function draw(){
    const data=distributions[selected];
    const base=241, scale=310;
    chart.replaceChildren();
    for(const tick of [0,.2,.4,.6]){
      const y=base-scale*tick;
      chart.appendChild(
        make("line",{x1:48,y1:y,x2:528,y2:y,stroke:tick===0?"#9db2c0":"#e0e9ee","stroke-width":tick===0?2:1}),
        make("text",{x:43,y:y+5,"text-anchor":"end","font-size":12,fill:"#6f8596"},tick.toFixed(1))
      );
    }
    const inspector=q("[data-die-values]",demo);
    function inspect(i){
      const probability=data.probs[i],face=i+1;
      inspector.textContent="Face "+face+": probability "+(100*probability).toFixed(0)+"% · contribution to E[X]: "+face+" × "+probability.toFixed(2)+" = "+(face*probability).toFixed(2)+".";
      chart.querySelectorAll("[data-face]").forEach(bar=>{
        const chosen=bar.dataset.face===String(face);
        bar.setAttribute("stroke",chosen?"#275b7a":"none");
        bar.setAttribute("stroke-width",chosen?"3":"0");
      });
    }
    data.probs.forEach((p,i)=>{
      const x=52+i*47.0;
      const h=p*scale;
      const bar=make("rect",{x,y:base-h,width:31,height:h,fill:selected==="fair"?"#79a4bc":selected==="loaded"?(i===0?"#bf8659":"#89acc0"):(i===0||i===9?"#bd895b":"#89acc0"),rx:2});
      bar.dataset.face=String(i+1);
      bar.setAttribute("role","button");
      bar.setAttribute("tabindex","0");
      bar.setAttribute("aria-label","Inspect face "+(i+1)+" probability");
      bar.style.cursor="pointer";
      bar.addEventListener("click",()=>inspect(i));
      bar.addEventListener("keydown",event=>{if(event.key==="Enter"||event.key===" "){event.preventDefault();inspect(i)}});
      bar.appendChild(make("title",{},"Face "+(i+1)+": "+(p*100).toFixed(0)+"%"));
      chart.appendChild(bar,
        make("text",{x:x+15.5,y:base-h-8,"text-anchor":"middle","font-size":16,fill:"#365d76"},(100*p).toFixed(0)+"%"),
        make("text",{x:x+15.5,y:base+23,"text-anchor":"middle","font-size":17,fill:"#486b83"},i+1)
      );
    });
    chart.appendChild(
      make("text",{x:285,y:295,"text-anchor":"middle","font-size":16,fill:"#59788a"},"Die face"),
      make("text",{x:14,y:145,transform:"rotate(-90 14 145)","text-anchor":"middle","font-size":16,fill:"#59788a"},"Probability")
    );
    inspect(0);
    const avg=expected(data.probs);
    if(Math.abs(data.probs.reduce((a,b)=>a+b,0)-1)>1e-8)throw new Error("Invalid PMF");
    meanEl.textContent=avg.toFixed(2);
    sumEl.textContent=Number((30*avg).toFixed(2)).toString();
    noteEl.textContent=data.explanation;
    pmfEl.textContent=selected==="fair"
      ?"P(X = x) = 0.10 for every face (uniform distribution)."
      :selected==="loaded"
        ?"P(X = 1) = 0.55, while P(X = 2…10) = 0.05 each."
        :"P(X = 1) = P(X = 10) = 0.30, while P(X = 2…9) = 0.05 each.";
    demo.querySelectorAll("[data-die-type]").forEach(button=>{
      button.setAttribute("aria-pressed",String(button.dataset.dieType===selected));
    });
    sample.hidden=true;
  }
  demo.querySelectorAll("[data-die-type]").forEach(button=>{
    button.addEventListener("click",()=>{
      selected=button.dataset.dieType;
      draw();
    });
  });
  q("[data-roll-30]",demo).addEventListener("click",()=>{
    const probs=distributions[selected].probs;
    const counts=Array(10).fill(0);
    let total=0;
    for(let roll=0;roll<30;roll++){
      const pick=Math.random();
      let cumulative=0,chosen=9;
      for(let i=0;i<10;i++){
        cumulative+=probs[i];
        if(pick<cumulative){chosen=i;break;}
      }
      counts[chosen]++;
      total+=chosen+1;
    }
    q("[data-observed-sum]",demo).textContent=String(total);
    q("[data-observed-mean]",demo).textContent=(total/30).toFixed(2);
    q("[data-observed-ones]",demo).textContent=counts[0]+" / 30";
    sample.hidden=false;
  });
  draw();
})();
