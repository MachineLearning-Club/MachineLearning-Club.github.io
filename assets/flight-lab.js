
/* Problem 42: ID3 on flight-delay marginal counts. All calculations are local. */
(() => {
  "use strict";
  const root=document.querySelector("[data-flight-demo]");
  if(!root)return;

  // Counts [delayed when Yes, not delayed when Yes, delayed when No, not delayed when No].
  const counts={
    Rain:[30,10,10,30],
    Wind:[25,15,15,25],
    Summer:[5,35,35,5],
    Winter:[20,10,20,30],
    Daytime:[20,20,20,20],
    Nighttime:[15,10,25,30]
  };
  const entropy=(a,b)=>{
    const sum=a+b;
    if(!sum)return 0;
    const parts=[a,b].filter(x=>x>0);
    return -parts.reduce((acc,x)=>acc+(x/sum)*Math.log2(x/sum),0);
  };
  const informationGain=([a,b,c,d])=>{
    const all=a+b+c+d;
    return entropy(a+c,b+d)
      -(a+b)/all*entropy(a,b)
      -(c+d)/all*entropy(c,d);
  };
  const correct=([a,b,c,d])=>Math.max(a,b)+Math.max(c,d);
  const select=root.querySelector("[data-flight-feature]");
  const gain=root.querySelector("[data-flight-gain]");
  const accuracy=root.querySelector("[data-flight-accuracy]");
  const feedback=root.querySelector("[data-flight-feedback]");
  const branch=(side,label,delayed,notDelayed)=>{
    root.querySelector("[data-flight-"+side+"-label]").textContent=select.value+" = "+label;
    const total=delayed+notDelayed;
    const stacked=root.querySelector("[data-flight-"+side+"-bar]");
    stacked.replaceChildren();
    const x=document.createElement("span");
    x.className="delayed";x.style.width=(100*delayed/total)+"%";
    const y=document.createElement("span");
    y.className="punctual";y.style.width=(100*notDelayed/total)+"%";
    stacked.append(x,y);
    stacked.setAttribute("aria-label",delayed+" delayed and "+notDelayed+" not delayed");
    root.querySelector("[data-flight-"+side+"-count]").textContent=
      delayed+" delayed · "+notDelayed+" not delayed";
  };
  function render(){
    const row=counts[select.value];
    branch("left","Yes",row[0],row[1]);
    branch("right","No",row[2],row[3]);
    gain.textContent=informationGain(row).toFixed(3)+" bits";
    const pct=100*correct(row)/80;
    accuracy.textContent=Number(pct.toFixed(2))+"%";
    feedback.textContent="Compare the two groups. Does "+select.value+
      " make their outcomes more predictable than the other attributes?";
  }
  select.addEventListener("change",render);
  root.querySelector("[data-flight-check]").addEventListener("click",()=>{
    const best=Object.keys(counts).sort((a,b)=>informationGain(counts[b])-informationGain(counts[a]))[0];
    const good=select.value===best;
    feedback.textContent=good?
      "Correct. Summer produces the largest information gain (about 0.4564 bits).":
      select.value+" is not the highest-gain attribute. Try Summer and compare its two groups.";
  });
  const reveal=root.querySelector("[data-flight-reveal]");
  const panel=root.querySelector("[data-flight-gains-panel]");
  reveal.addEventListener("click",()=>{
    panel.hidden=!panel.hidden;
    reveal.textContent=panel.hidden?"Compare all gains":"Hide all gains";
  });
  render();
})();
