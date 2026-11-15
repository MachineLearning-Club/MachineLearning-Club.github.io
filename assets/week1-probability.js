/* Week 1 practice: live probability, expected value, variance and covariance. */
(() => {
 "use strict";
 const $=(selector,root=document)=>root.querySelector(selector);
 const pct=x=>Math.round(x*100)+"%";
 const fmt=x=>(Math.abs(x)<.00001?0:x).toFixed(2);
 const setBar=(node,p,base=185,max=160)=>{
   if(!node)return;
   const height=Math.max(0,Math.min(max,max*p));
   node.setAttribute("height",height.toFixed(1));
   node.setAttribute("y",(base-height).toFixed(1));
 };
 const distribution=document.querySelector("[data-probability-lab]");
 if(distribution){
   const slider=$("[data-probability-slider]",distribution);
   function render(){
     const p=Number(slider.value)/100;
     $("[data-p-label]",distribution).textContent=pct(p);
     setBar($("[data-bar-red]",distribution),p);
     setBar($("[data-bar-blue]",distribution),1-p);
     $("[data-prob-label-red]",distribution).textContent=pct(p);
     $("[data-prob-label-blue]",distribution).textContent=pct(1-p);
     $("[data-probability-result]",distribution).textContent="P(red) + P(blue) = "+fmt(p)+" + "+fmt(1-p)+" = 1.00";
     $("[data-expected-result]",distribution).textContent="Let X = 1 for red, 0 for blue. E[X] = 1×"+fmt(p)+" + 0×"+fmt(1-p)+" = "+fmt(p)+".";
   }
   slider.addEventListener("input",render);render();
 }
 const check=document.querySelector("[data-check-distributions]");
 if(check){
   check.addEventListener("click",()=>{
     const choices=[...document.querySelectorAll("[data-dist-choice]")];
     let score=0,answered=0;
     for(const choice of choices){
       if(choice.value)answered++;
       const good=choice.value===choice.dataset.correct;
       if(good)score++;
       choice.classList.toggle("choice-right",good);
       choice.classList.toggle("choice-wrong",choice.value!==""&&!good);
     }
     $("[data-distributions-result]").textContent="You matched "+score+" / "+choices.length+
       " situations correctly ("+answered+" answered)."+
       (score===choices.length?" Every choice is consistent with the described situation.":
       " Review the definitions: one trial, repeated trials, equally likely faces, counts per interval, or a bell-shaped measurement.");
   });
 }
 const variance=document.querySelector("[data-variance-visual]");
 if(variance){
   const slider=$("[data-variance-slider]",variance);
   function render(){
     const p=Number(slider.value)/100,mean=10*p,spread=100*p*(1-p);
     setBar($("[data-variance-bar-zero]",variance),1-p,205,160);
     setBar($("[data-variance-bar-ten]",variance),p,205,160);
     $("[data-variance-p]",variance).textContent=pct(p);
     $("[data-variance-label-zero]",variance).textContent=pct(1-p);
     $("[data-variance-label-ten]",variance).textContent=pct(p);
     const position=196+(436-196)*p,line=$("[data-variance-mean-line]",variance),
       label=$("[data-variance-mean-label]",variance);
     line.setAttribute("x1",position.toFixed(1));line.setAttribute("x2",position.toFixed(1));
     label.setAttribute("x",position.toFixed(1));label.textContent="Mean "+fmt(mean);
     $("[data-variance-result]",variance).textContent=
       "Mean E[X] = 0×"+fmt(1-p)+" + 10×"+fmt(p)+" = "+fmt(mean)+
       ". Variance = "+fmt(1-p)+"×(0−"+fmt(mean)+")² + "+fmt(p)+"×(10−"+fmt(mean)+")² = "+fmt(spread)+".";
   }
   slider.addEventListener("input",render);render();
 }
 const covariance=document.querySelector("[data-covariance-visual]");
 if(covariance){
   const buttons=[...covariance.querySelectorAll("[data-cov-mode]")];
   const pts=["a","b","c","d"].map(name=>$('[data-cov-point="'+name+'"]',covariance));
   function render(mode){
     const sets={positive:[.5,.5,0,0],negative:[0,0,.5,.5],zero:[.25,.25,.25,.25]};
     const weights=sets[mode]||sets.positive;
     pts.forEach((circle,i)=>{circle.style.opacity=weights[i]>0?"1":"0";circle.setAttribute("r",weights[i]===.5?16:11);});
     buttons.forEach(btn=>btn.setAttribute("aria-pressed",String(btn.dataset.covMode===mode)));
     const ex=.5,ey=.5,exy=weights[1];
     const cov=exy-ex*ey;
     const wording=mode==="positive"?"The variables tend to increase together.":
       mode==="negative"?"High X is paired with low Y.":"All four pairs are equally likely; these binary variables are independent.";
     $("[data-cov-result]",covariance).textContent=
       "E[X] = E[Y] = 0.50; E[XY] = "+fmt(exy)+"; covariance = "+fmt(exy)+" − (0.50×0.50) = "+fmt(cov)+". "+wording;
   }
   for(const button of buttons)button.addEventListener("click",()=>render(button.dataset.covMode));
   render("positive");
 }
})();