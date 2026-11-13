
/* Week 1: ten-sided dice, conditional probability, distributions, and method diagrams. */
(() => {
  "use strict";
  const q=(s,root=document)=>root.querySelector(s);
  const probability=q("[data-d10-probability]");
  if(probability){
    const grid=q("[data-d10-cells]",probability);
    const select=q("[data-d10-guess]",probability);
    const checkbox=q("[data-d10-even]",probability);
    const fraction=q("[data-d10-fraction]",probability);
    const reason=q("[data-d10-reason]",probability);
    const formula=q("[data-d10-formula-label]",probability);
    const cells=[];
    for(let face=1;face<=10;face++){
      const el=document.createElement("span");
      el.textContent=String(face);
      el.className="d10-face";
      grid.appendChild(el);
      cells.push(el);
    }
    function render(){
      const chosen=Number(select.value);
      const onlyEven=checkbox.checked;
      let possible=0,favourable=0;
      cells.forEach((el,i)=>{
        const face=i+1;
        const eligible=!onlyEven||face%2===0;
        const match=eligible&&face===chosen;
        possible+=eligible?1:0;
        favourable+=match?1:0;
        el.classList.toggle("eligible",eligible);
        el.classList.toggle("excluded",!eligible);
        el.classList.toggle("hit",match);
        el.setAttribute("aria-label","Face "+face+(eligible?" still possible":" excluded")+(match?", guessed face":""));
      });
      formula.textContent=onlyEven?"Conditional probability (given even)":"Unconditional probability";
      fraction.textContent=favourable+" / "+possible+" = "+(100*favourable/possible).toFixed(0)+"%";
      reason.textContent=onlyEven
        ?chosen%2===0
          ?"The even-number condition leaves five outcomes. Your guessed face is one of them."
          :"The condition rules out odd faces, so your guess is impossible."
        :"One guessed face out of ten equally likely possibilities.";
      grid.setAttribute("aria-label",possible+" possible faces, "+favourable+" favourable");
    }
    select.addEventListener("change",render);
    checkbox.addEventListener("change",render);
    render();
  }
  document.querySelectorAll("[data-model-card]").forEach(card=>{
    const button=q(".model-diagram-toggle",card);
    const note=q("[data-model-note]",card);
    if(!button||!note)return;
    button.addEventListener("click",()=>{
      const active=!card.classList.contains("is-demonstrating");
      card.classList.toggle("is-demonstrating",active);
      button.setAttribute("aria-pressed",String(active));
      q(".model-diagram-action",button).textContent=active?"Reset diagram":"Explore diagram";
      note.hidden=!active;
    });
  });
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
    data.probs.forEach((p,i)=>{
      const x=52+i*47.0;
      const h=p*scale;
      const bar=make("rect",{x,y:base-h,width:31,height:h,fill:selected==="fair"?"#79a4bc":selected==="loaded"?(i===0?"#bf8659":"#89acc0"):(i===0||i===9?"#bd895b":"#89acc0"),rx:2});
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
    const values=q("[data-die-values]",demo);
    values.replaceChildren();
    data.probs.forEach((prob,i)=>{
      const cell=document.createElement("div"),label=document.createElement("span"),val=document.createElement("strong");
      label.textContent="Face "+(i+1);
      val.textContent=(100*prob).toFixed(0)+"%";
      cell.append(label,val);values.appendChild(cell);
    });
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
