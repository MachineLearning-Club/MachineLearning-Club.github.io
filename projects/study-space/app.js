/* One original, inspectable nearest-neighbour experiment for Weeks 12–15.
 * Static, synthetic data only. No accounts, network writes or student tracking.
 * Its distance and vote rules mirror projects/study-space/model.py.
 */
(() => {
  'use strict';
  const FEATURES=['occupancy','noise','wifi','outlets','minutes'];
  const LABELS=['avoid','consider','good'];
  const SCALES=[100,60,4,1,100], WEIGHTS=[1,1,.7,.30,.15];
  function distance(a,b){
    return FEATURES.reduce((acc,key,i)=>acc+WEIGHTS[i]*Math.pow((Number(a[key])-Number(b[key]))/SCALES[i],2),0);
  }
  function predict(train,input,k=3){
    if(![1,3,5,7].includes(k)) throw new Error('Allowed neighbour counts: 1, 3, 5, 7');
    const selected=train.map(row=>({...row,distance:distance(row,input)}))
      .sort((a,b)=>a.distance-b.distance || a.id.localeCompare(b.id)).slice(0,k);
    const votes=Object.fromEntries(LABELS.map(c=>[c,selected.filter(row=>row.label===c)]));
    const ordered=LABELS.slice().sort((a,b)=>votes[b].length-votes[a].length ||
      votes[a].reduce((n,r)=>n+r.distance,0)-votes[b].reduce((n,r)=>n+r.distance,0) || a.localeCompare(b));
    return {label:ordered[0],neighbours:selected};
  }
  function evaluate(train,rows,k){
    const matrix=Object.fromEntries(LABELS.map(c=>[c,Object.fromEntries(LABELS.map(p=>[p,0]))]));
    let correct=0;const wrong=[];
    rows.forEach(row=>{const guess=predict(train,row,k).label;matrix[row.label][guess]++;
      if(guess===row.label)correct++;else wrong.push({id:row.id,actual:row.label,predicted:guess});});
    return {correct,total:rows.length,matrix,wrong};
  }
  function baseline(train,rows){
    const counts=Object.fromEntries(LABELS.map(c=>[c,train.filter(r=>r.label===c).length]));
    const most=LABELS.slice().sort((a,b)=>counts[b]-counts[a]||a.localeCompare(b))[0];
    return {label:most,correct:rows.filter(r=>r.label===most).length,total:rows.length};
  }
  window.StudySpacePractice={distance,predict,evaluate,baseline}; // For transparent reproducibility and automated checks.
  function node(tag,cls,text){
    const el=document.createElement(tag);
    if(cls)el.className=cls;
    if(text!=null)el.textContent=String(text);
    return el;
  }
  function render(root,data){
    const train=data.data.train,validation=data.data.validation;
    root.innerHTML=`
      <h3>Explore a supervised classifier</h3>
      <p class="ss-intro">All 240 examples are simulated. Change a study space, predict a label, then test a model on 45 separate validation examples. No information is collected.</p>
      <div class="ss-layout">
        <div class="ss-controls">
          <label>Seats occupied <output data-value="occupancy">35%</output><input name="occupancy" type="range" min="0" max="100" value="35"></label>
          <label>Noise (illustrative dB) <output data-value="noise">42</output><input name="noise" type="range" min="20" max="95" value="42"></label>
          <label>Wi-Fi signal (1–5) <output data-value="wifi">4</output><input name="wifi" type="range" min="1" max="5" value="4"></label>
          <label class="ss-checkbox"><input name="outlets" type="checkbox" checked> Power outlets available</label>
          <label>Study duration (minutes) <select name="minutes"><option>30</option><option>45</option><option selected>60</option><option>90</option><option>120</option></select></label>
          <label>Nearest neighbours (k) <select name="k"><option>1</option><option selected>3</option><option>5</option><option>7</option></select></label>
        </div>
        <div class="ss-result" aria-live="polite">
          <p class="ss-note">Prediction from labelled examples</p>
          <p class="ss-prediction" data-prediction>Loading…</p>
          <p data-votes class="ss-note"></p>
          <h4>Nearest training examples</h4>
          <ol class="ss-neighbours" data-neighbours></ol>
          <p class="ss-note">Smaller weighted squared distance means a closer match. A neighbour vote is not a calibrated probability.</p>
        </div>
      </div>
      <div class="ss-actions">
        <button type="button" data-evaluate>Evaluate on validation set</button>
        <button type="button" class="secondary" data-reset>Reset input</button>
      </div>
      <div class="ss-metrics" data-metrics role="status" aria-live="polite"></div>
      <p class="ss-note">The validation data are deliberately public for learning. Do not use the final test set to choose k. Scores here are not estimates of performance on actual school rooms.</p>
    `;
    const get=n=>root.querySelector('[name="'+n+'"]');
    const update=()=>{
      const input={};
      for(const f of FEATURES)input[f]=f==='outlets'?Number(get(f).checked):Number(get(f).value);
      for(const f of ['occupancy','noise','wifi'])root.querySelector('[data-value="'+f+'"]').textContent=
        String(input[f])+(f==='occupancy'?'%':'');
      const k=Number(get('k').value);
      const result=predict(train,input,k);
      root.querySelector('[data-prediction]').textContent=result.label.toUpperCase();
      const voteCounts=Object.fromEntries(LABELS.map(c=>[c,result.neighbours.filter(r=>r.label===c).length]));
      root.querySelector('[data-votes]').textContent=LABELS.map(c=>c+': '+voteCounts[c]).join(' · ');
      const list=root.querySelector('[data-neighbours]');list.replaceChildren();
      result.neighbours.forEach(r=>list.appendChild(node('li',null,r.id+' — '+r.label+' · d²='+r.distance.toFixed(4))));
    };
    root.querySelectorAll('input,select').forEach(el=>el.addEventListener('input',update));
    root.querySelector('[data-reset]').addEventListener('click',()=>{
      [['occupancy',35],['noise',42],['wifi',4],['minutes',60],['k',3]].forEach(([f,v])=>get(f).value=v);
      get('outlets').checked=true;
      update();
    });
    root.querySelector('[data-evaluate]').addEventListener('click',()=>{
      const k=Number(get('k').value);
      const base=baseline(train,validation),r=evaluate(train,validation,k);
      const area=root.querySelector('[data-metrics]');area.replaceChildren();
      area.appendChild(node('h4',null,'Validation results (same 45 labelled examples)'));
      area.appendChild(node('p',null,'Majority-class baseline: '+base.correct+'/'+base.total+
        ' ('+(100*base.correct/base.total).toFixed(1)+'%). k='+k+' model: '+r.correct+'/'+r.total+
        ' ('+(100*r.correct/r.total).toFixed(1)+'%).'));
      const table=node('table');table.setAttribute('aria-label','Actual labels in rows, predicted labels in columns');
      const hdr=node('tr');['Actual / predicted',...LABELS].forEach(t=>hdr.appendChild(node('th',null,t)));
      const head=node('thead');head.appendChild(hdr);table.appendChild(head);
      const body=node('tbody');LABELS.forEach(c=>{const tr=node('tr');tr.appendChild(node('th',null,c));
        LABELS.forEach(p=>tr.appendChild(node('td',null,r.matrix[c][p])));body.appendChild(tr);});
      table.appendChild(body);area.appendChild(table);
      area.appendChild(node('p','ss-note',r.wrong.length+' incorrect cases. Example: '+
        (r.wrong.length?r.wrong[0].id+' was '+r.wrong[0].actual+' but predicted '+r.wrong[0].predicted+'.':'none in this subset.')));
    });
    update();
  }
  document.querySelectorAll('[data-fiicode-widget]').forEach(root=>{
    root.classList.add('ss-studio');
    root.appendChild(node('p','ss-note','Loading the practice dataset…'));
    const embedded=document.getElementById('study-space-data');
    const load=embedded ? Promise.resolve().then(()=>JSON.parse(embedded.textContent)) :
      fetch('/assets/data/fiicode-study-space.json')
        .then(res=>{if(!res.ok)throw new Error('Dataset '+res.status);return res.json();});
    load.then(data=>render(root,data))
      .catch(err=>root.replaceChildren(node('p','ss-note',
        'This interactive example could not load ('+err.message+'). Use the downloadable Python project instead.')));
  });
})();
