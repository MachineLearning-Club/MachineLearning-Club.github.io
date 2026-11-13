/* Week 01 probability and information-theory experiments. No dependencies. */
(() => {
  "use strict";
  const dice=document.querySelector("[data-dice-demo]");
  if(dice){
    const grid=dice.querySelector("[data-dice-grid]");
    const condition=dice.querySelector("[data-dice-condition]");
    const result=dice.querySelector("[data-dice-result]");
    const explanation=dice.querySelector("[data-dice-explanation]");
    const cells=[];
    const isPrime=n=>[2,3,5,7,11].includes(n);
    for(let a=1;a<=6;a++){
      for(let b=1;b<=6;b++){
        const cell=document.createElement("span");
        const sum=a+b;
        cell.className="dice-cell";
        cell.textContent=a+","+b;
        cell.title="First die "+a+", second die "+b+"; sum "+sum;
        cell.dataset.sum=String(sum);
        grid.appendChild(cell);
        cells.push(cell);
      }
    }
    function render(){
      const prime=condition.value==="prime";
      let total=0,favourable=0;
      for(const cell of cells){
        const sum=Number(cell.dataset.sum);
        const possible=!prime || isPrime(sum);
        const hit=possible&&sum===11;
        cell.classList.toggle("possible",possible);
        cell.classList.toggle("hit",hit);
        if(possible)total++;
        if(hit)favourable++;
      }
      result.textContent=prime?"2 / 15 ≈ 0.1333":"2 / 36 = 1 / 18";
      explanation.textContent=prime
        ? "The prime-sum condition leaves 15 equally likely outcomes, including both ways to make 11."
        : "Only (5,6) and (6,5) are favourable among all 36 ordered outcomes.";
      grid.setAttribute("aria-label",total+" possible ordered dice outcomes, "+favourable+" highlighted ways to make a sum of 11");
    }
    condition.addEventListener("change",render);
    render();
  }
  const entropy=document.querySelector("[data-entropy-demo]");
  if(entropy){
    const slider=entropy.querySelector("[data-entropy-slider]");
    const pLabel=entropy.querySelector("[data-entropy-p]");
    const value=entropy.querySelector("[data-entropy-value]");
    const note=entropy.querySelector("[data-entropy-note]");
    const a=entropy.querySelector("[data-entropy-a]");
    const b=entropy.querySelector("[data-entropy-b]");
    const curve=entropy.querySelector("[data-entropy-curve]");
    const point=entropy.querySelector("[data-entropy-point]");
    const H=p=>{
      const term=x=>x===0?0:-x*Math.log2(x);
      return term(p)+term(1-p);
    };
    const x=p=>45+354*p;
    const y=p=>215-191*H(p);
    let d="";
    for(let i=0;i<=100;i++){
      const p=i/100;
      d+=(i===0?"M":"L")+x(p).toFixed(2)+" "+y(p).toFixed(2)+" ";
    }
    curve.setAttribute("d",d);
    function render(){
      const p=Number(slider.value)/100;
      pLabel.textContent=Math.round(p*100)+"%";
      value.textContent=H(p).toFixed(3)+" bits";
      a.style.width=(p*100)+"%";
      b.style.width=((1-p)*100)+"%";
      point.setAttribute("cx",String(x(p)));
      point.setAttribute("cy",String(y(p)));
      note.textContent=p===0||p===1
        ?"One outcome is certain, so there is no uncertainty."
        :p===0.5?"Both outcomes are equally likely: uncertainty is highest."
        :"One outcome is more likely, so entropy is below 1 bit.";
    }
    slider.addEventListener("input",render);
    render();
  }
})();