
/* Problem 40, Martian or Earthling: ID3 inference on the ten printed examples. */
(() => {
  "use strict";
  const root = document.querySelector("[data-mars-demo]");
  if (!root) return;

  const examples = [
    ["M","N","3","S","Y"],["M","Y","2","T","N"],["M","Y","3","T","N"],
    ["M","N","2","S","Y"],["M","Y","3","T","N"],["H","N","2","T","Y"],
    ["H","N","2","S","N"],["H","N","2","T","N"],["H","Y","2","S","N"],
    ["H","N","2","T","Y"]
  ];
  const fields = {};
  root.querySelectorAll("[data-mars-feature]").forEach(input => {
    fields[input.dataset.marsFeature] = input;
  });
  const result = root.querySelector("[data-mars-result]");
  const path = root.querySelector("[data-mars-path]");
  const training = root.querySelector("[data-mars-training]");
  const diagram = document.querySelector(".mars-tree");

  function decision(values) {
    const nodes=["root"],edges=[],trace=[];
    if (values.Legs === "3") {
      edges.push("root-3");nodes.push("leaf3");
      trace.push("Legs = 3");
      return {label:"M",nodes,edges,trace};
    }
    edges.push("root-2");nodes.push("green");
    trace.push("Legs = 2");
    if (values.Green === "N") {
      edges.push("green-N");nodes.push("heightN");trace.push("Green = N");
      if (values.Height === "T") {
        edges.push("heightN-T");nodes.push("leafNT");trace.push("Height = T");
        return {label:"H",nodes,edges,trace};
      }
      edges.push("heightN-S");nodes.push("smelly");trace.push("Height = S");
      if (values.Smelly === "N") {
        edges.push("smelly-N");nodes.push("leafNSN");trace.push("Smelly = N");
        return {label:"H",nodes,edges,trace};
      }
      edges.push("smelly-Y");nodes.push("leafNSY");trace.push("Smelly = Y");
      return {label:"M",nodes,edges,trace};
    }
    edges.push("green-Y");nodes.push("heightY");trace.push("Green = Y");
    if (values.Height === "S") {
      edges.push("heightY-S");nodes.push("leafYS");trace.push("Height = S");
      return {label:"H",nodes,edges,trace};
    }
    edges.push("heightY-T");nodes.push("leafYT");trace.push("Height = T");
    return {label:"M",nodes,edges,trace};
  }
  const classify = v=>decision({Green:v[1],Legs:v[2],Height:v[3],Smelly:v[4]}).label;
  const trainingCorrect = examples.filter(v=>classify(v)===v[0]).length;
  if(trainingCorrect!==examples.length) {
    console.error("The illustrative ID3 tree is not consistent with source data.");
    return;
  }
  const render = () => {
    const values = Object.fromEntries(Object.entries(fields).map(([k,input])=>[k,input.value]));
    const predicted=decision(values);
    result.textContent=(predicted.label==="M"?"M — Alien":"H — Human");
    result.classList.toggle("mars-m",predicted.label==="M");
    result.classList.toggle("mars-h",predicted.label==="H");
    path.textContent=predicted.trace.join(" → ")+" → "+(predicted.label==="M"?"Alien":"Human");
    const matched=examples.filter(row=>row[1]===values.Green && row[2]===values.Legs &&
      row[3]===values.Height && row[4]===values.Smelly);
    if(matched.length) {
      training.textContent="Matches "+matched.length+" labelled training "+(matched.length===1?"example":"examples")+".";
    } else {
      training.textContent="Unseen combination: the tree still gives a prediction, but its reliability is unknown.";
    }
    if(diagram) {
      diagram.querySelectorAll("[data-mars-node], [data-mars-edge]").forEach(el=>el.classList.remove("is-active"));
      for(const node of predicted.nodes)diagram.querySelector('[data-mars-node="'+node+'"]')?.classList.add("is-active");
      for(const edge of predicted.edges)diagram.querySelector('[data-mars-edge="'+edge+'"]')?.classList.add("is-active");
    }
  };
  for (const input of Object.values(fields))input.addEventListener("change",render);
  root.querySelector("[data-mars-reset]").addEventListener("click",()=>{
    const initial={Green:"N",Legs:"2",Height:"S",Smelly:"Y"};
    for(const [key,v] of Object.entries(initial))fields[key].value=v;
    render();
  });
  render();
  const viewport=document.querySelector(".mars-tree-scroll");
  const mobile=window.matchMedia("(max-width:680px)");
  function centreFirstQuestion(){
    if(!viewport || !mobile.matches)return;
    const diagramWidth=diagram?.getBoundingClientRect().width||940;
    viewport.scrollLeft=Math.max(0,(450/940)*diagramWidth-viewport.clientWidth/2);
  }
  centreFirstQuestion();
  mobile.addEventListener?.("change",centreFirstQuestion);
})();
