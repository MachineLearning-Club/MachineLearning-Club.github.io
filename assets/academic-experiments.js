/* Small, local information gain explorer. */
(() => {
  const root = document.querySelector('[data-id3-explorer]');
  if (!root) return;
  const data = [
    ['sunny','calm','warm','yes'], ['sunny','calm','cold','yes'],
    ['sunny','windy','warm','yes'], ['sunny','windy','cold','no'],
    ['rainy','calm','warm','no'], ['rainy','calm','cold','no'],
    ['rainy','windy','warm','no'], ['rainy','windy','cold','no']
  ];
  const columns = ['sky','wind','temperature','go'];
  const rows = data.map(record=>Object.fromEntries(columns.map((column,i)=>[column,record[i]])));
  function entropy(records) {
    if (!records.length) return 0;
    const yes = records.filter(r=>r.go==='yes').length;
    const p = yes / records.length;
    return p===0 || p===1 ? 0 : -p*Math.log2(p) - (1-p)*Math.log2(1-p);
  }
  const choice = root.querySelector('[data-id3-feature]');
  const result = root.querySelector('[data-id3-result]');
  const details = root.querySelector('[data-id3-detail]');
  const calculate = () => {
    const feature = choice.value;
    const values = [...new Set(rows.map(r=>r[feature]))].sort();
    const groups = values.map(value=>({value, subset:rows.filter(r=>r[feature]===value)}));
    const remaining = groups.reduce((sum,g)=>sum + (g.subset.length/rows.length)*entropy(g.subset),0);
    const gain = entropy(rows)-remaining;
    result.textContent = 'Gain(' + feature + ') = ' + gain.toFixed(4) +
      ' bits. ' + (feature==='sky'?'This is the strongest first question.':'Compare with sky.');
    details.replaceChildren();
    for (const g of groups) {
      const p=document.createElement('p');
      const yes=g.subset.filter(r=>r.go==='yes').length;
      p.textContent=feature+' = '+g.value+': '+g.subset.length+' examples ('+
        yes+' yes, '+(g.subset.length-yes)+' no); entropy '+entropy(g.subset).toFixed(4)+'.';
      details.appendChild(p);
    }
  };
  root.querySelector('[data-id3-compute]').addEventListener('click',calculate);
  choice.addEventListener('change',calculate);
  calculate();
})();
