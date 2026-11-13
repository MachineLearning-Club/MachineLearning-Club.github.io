/* Week 1: transparent nearest-prototype model. No dependencies or data collection. */
(() => {
  "use strict";
  const root = document.querySelector("[data-prototype-demo]");
  if (!root) return;
  const initial = [
    {x:2, y:2, label:"A"}, {x:2, y:3, label:"A"}, {x:3, y:2, label:"A"},
    {x:7, y:7, label:"B"}, {x:7, y:8, label:"B"}, {x:8, y:7, label:"B"}
  ];
  const cloneTraining = () => initial.map(p => ({...p}));
  const mean = (items, label) => {
    const group = items.filter(p => p.label === label);
    return {
      x:group.reduce((sum, p) => sum + p.x, 0) / group.length,
      y:group.reduce((sum, p) => sum + p.y, 0) / group.length
    };
  };
  const train = items => ({A:mean(items,"A"), B:mean(items,"B")});
  const distance = (p, q) => Math.hypot(p.x - q.x, p.y - q.y);
  const fmt = v => Number(v).toFixed(2);
  const $ = sel => root.querySelector(sel);
  const grid = $("[data-chart-grid]");
  const boundary = $("[data-chart-boundary]");
  const connectors = $("[data-chart-distances]");
  const markers = $("[data-chart-points]");
  const prototypesGroup = $("[data-chart-prototypes]");
  const queryGroup = $("[data-chart-query]");
  const testX = $("[data-test-x]");
  const testY = $("[data-test-y]");
  const editSelect = $("[data-edit-point]");
  const editX = $("[data-edit-x]");
  const editY = $("[data-edit-y]");
  const prediction = $("[data-prediction]");
  const details = $("[data-result-details]");
  const learnedText = $("[data-learned-centroids]");
  const status = $("[data-experiment-status]");
  const NS = "http://www.w3.org/2000/svg";
  const left = 54, top = 18, width = 510, height = 305;
  const X = n => left + width * n / 10;
  const Y = n => top + height * (1 - n / 10);
  const svgEl = (tag, attrs, text) => {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k,v]) => el.setAttribute(k, String(v)));
    if (text !== undefined) el.textContent = text;
    return el;
  };
  let training = cloneTraining();
  let learned = train(training);
  let changed = false;
  let selected = 0;
  const query = () => ({x:Number(testX.value), y:Number(testY.value)});

  for (let i=0; i<=10; i+=2) {
    grid.append(
      svgEl("line",{x1:X(i), x2:X(i), y1:Y(0), y2:Y(10), stroke:"#e3e9ee"}),
      svgEl("line",{x1:X(0), x2:X(10), y1:Y(i), y2:Y(i), stroke:"#e3e9ee"}),
      svgEl("text",{x:X(i), y:343, "text-anchor":"middle", "font-size":12, fill:"#647482"},i),
      svgEl("text",{x:42, y:Y(i)+4, "text-anchor":"end", "font-size":12, fill:"#647482"},i)
    );
  }
  grid.append(
    svgEl("text",{x:310, y:370, "text-anchor":"middle", "font-size":13, fill:"#41586a"},"Size"),
    svgEl("text",{x:14, y:168, "text-anchor":"middle", "font-size":13, fill:"#41586a", transform:"rotate(-90 14 168)"},"Reflectance")
  );
  function drawBoundary() {
    boundary.replaceChildren();
    const a=learned.A, b=learned.B;
    const dx=b.x-a.x, dy=b.y-a.y;
    if (Math.abs(dx)+Math.abs(dy)<1e-8) return;
    // The perpendicular bisector satisfies dx*x + dy*y = c.
    const c=(b.x*b.x+b.y*b.y-a.x*a.x-a.y*a.y)/2;
    const hits=[];
    if (Math.abs(dy)>1e-9) {
      for (const x of [0,10]) {
        const y=(c-dx*x)/dy;
        if (y>=0 && y<=10) hits.push({x,y});
      }
    }
    if (Math.abs(dx)>1e-9) {
      for (const y of [0,10]) {
        const x=(c-dy*y)/dx;
        if (x>=0 && x<=10) hits.push({x,y});
      }
    }
    if (hits.length<2) return;
    let p=hits[0], q=hits[1], best=0;
    for (let i=0;i<hits.length;i++) {
      for (let j=i+1;j<hits.length;j++) {
        const d=distance(hits[i], hits[j]);
        if (d>best) {best=d; p=hits[i]; q=hits[j];}
      }
    }
    boundary.append(svgEl("line",{
      x1:X(p.x),y1:Y(p.y),x2:X(q.x),y2:Y(q.y),
      stroke:"#8b9eac","stroke-width":2,"stroke-dasharray":"7 6"
    }));
  }
  function draw() {
    const test=query();
    const aDist=distance(test,learned.A);
    const bDist=distance(test,learned.B);
    const result=aDist<=bDist?"A":"B";
    drawBoundary();
    connectors.replaceChildren();
    const nearest=learned[result];
    connectors.append(svgEl("line",{
      x1:X(test.x),y1:Y(test.y),x2:X(nearest.x),y2:Y(nearest.y),
      stroke:"#3f8478","stroke-width":1.8,"stroke-dasharray":"4 4"
    }));
    markers.replaceChildren();
    training.forEach((p,i)=>{
      const color=p.label==="A"?"#447aaa":"#bb824c";
      markers.append(svgEl("circle",{
        cx:X(p.x),cy:Y(p.y),r:i===selected?8:6,fill:color,
        stroke:i===selected?"#1e3344":"#fff","stroke-width":i===selected?2:1.5
      }));
      markers.append(svgEl("text",{
        x:X(p.x)+9,y:Y(p.y)-9,"font-size":11,fill:color
      },p.label+(i%3+1)));
    });
    prototypesGroup.replaceChildren();
    for (const label of ["A","B"]) {
      const p=learned[label],color=label==="A"?"#447aaa":"#bb824c";
      prototypesGroup.append(svgEl("circle",{
        cx:X(p.x),cy:Y(p.y),r:12,fill:"none",stroke:color,"stroke-width":2.8
      }));
    }
    queryGroup.replaceChildren(
      svgEl("circle",{
        cx:X(test.x),cy:Y(test.y),r:8.5,fill:"#267f71",stroke:"#fff","stroke-width":2
      }),
      svgEl("text",{
        x:X(test.x)+12,y:Y(test.y)-12,"font-size":14,"font-weight":"bold",fill:"#267f71"
      },"?")
    );
    prediction.textContent=result;
    details.textContent="Distance to A: "+fmt(aDist)+" · Distance to B: "+fmt(bDist);
    learnedText.textContent="Learned prototypes: A = ("+fmt(learned.A.x)+", "+fmt(learned.A.y)+
      "), B = ("+fmt(learned.B.x)+", "+fmt(learned.B.y)+")";
    $("[data-test-x-value]").textContent=Number(testX.value).toFixed(1);
    $("[data-test-y-value]").textContent=Number(testY.value).toFixed(1);
    $("[data-edit-x-value]").textContent=Number(editX.value).toFixed(1);
    $("[data-edit-y-value]").textContent=Number(editY.value).toFixed(1);
  }
  function syncSelected() {
    const p=training[selected];
    editX.value=String(p.x);
    editY.value=String(p.y);
    $("[data-selected-class]").textContent="Class "+p.label;
    draw();
  }
  [testX,testY].forEach(input=>input.addEventListener("input",draw));
  editSelect.addEventListener("change",()=>{
    selected=Number(editSelect.value);
    syncSelected();
  });
  [editX,editY].forEach(input=>input.addEventListener("input",()=>{
    training[selected].x=Number(editX.value);
    training[selected].y=Number(editY.value);
    changed=true;
    status.textContent="Training example changed. The model still uses its previous prototypes. Press Retrain model.";
    draw();
  }));
  $("[data-retrain]").addEventListener("click",()=>{
    learned=train(training);
    changed=false;
    draw();
    status.textContent="Model retrained using the edited examples. Compare its new prototypes and prediction.";
  });
  $("[data-reset-model]").addEventListener("click",()=>{
    training=cloneTraining();learned=train(training);changed=false;selected=0;
    editSelect.value="0";testX.value="2.5";testY.value="2.2";
    status.textContent="Original six examples and trained model restored.";
    syncSelected();
  });
  $("[data-try-middle]").addEventListener("click",()=>{
    testX.value="5";testY.value="5";draw();
    status.textContent=changed
      ?"Middle input selected. Edits to training examples only affect prediction after retraining."
      :"Middle input selected. Notice how near it is to the decision boundary.";
  });
  syncSelected();

  const toc=document.querySelector(".course-sidebar .toc-panel");
  if (toc) {
    const mobile=window.matchMedia("(max-width:680px)");
    const syncToc=()=>{toc.open=!mobile.matches;};
    syncToc();
    if (mobile.addEventListener) mobile.addEventListener("change",syncToc);
    toc.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener("click",()=>{
      if (mobile.matches) toc.open=false;
    }));
    const sectionIds=["one","two","three","four","five"];
    const sections=sectionIds.map(id=>document.getElementById(id)).filter(Boolean);
    const navLinks=sections.map(el=>toc.querySelector('a[href="#'+el.id+'"]'));
    let scheduled=false;
    const updateActive=()=>{
      scheduled=false;
      let index=0;
      sections.forEach((section,i)=>{
        if (section.getBoundingClientRect().top<=160) index=i;
      });
      navLinks.forEach((link,i)=>{
        if (!link) return;
        if (i===index) link.setAttribute("aria-current","location");
        else link.removeAttribute("aria-current");
      });
    };
    window.addEventListener("scroll",()=>{
      if (!scheduled) {
        scheduled=true;
        window.requestAnimationFrame(updateActive);
      }
    },{passive:true});
    updateActive();
  }
})();
