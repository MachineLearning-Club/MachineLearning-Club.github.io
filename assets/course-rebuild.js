
/* Week 1 teaching visuals: button rule, exhaustive labelled decision tree, and K-means iteration. */
(() => {
  "use strict";

  // A programmed rule: the input button directly determines the output light.
  const lamp=document.querySelector("[data-lamp-demo]");
  if(lamp){
    const button=lamp.querySelector("[data-lamp-toggle]");
    const pressed=lamp.querySelector("[data-lamp-pressed]");
    const result=lamp.querySelector("[data-lamp-result]");
    const svg=lamp.querySelector("[data-lamp-svg]");
    let on=false;
    const render=()=>{
      lamp.classList.toggle("light-on",on);
      button.setAttribute("aria-pressed",String(on));
      button.textContent=on?"Release the button":"Press the button";
      pressed.textContent=on?"True":"False";
      result.textContent=on?"ON":"OFF";
      svg.setAttribute("aria-label","Lightbulb currently "+(on?"on":"off"));
    };
    button.addEventListener("click",()=>{on=!on;render();});
    render();
  }

  // A small K-means exercise: six labelled points are named for reference,
  // not given target classes. Only assignments and centroid means are learned.
  const points=[
    {name:"A",x:1,y:1},{name:"B",x:1,y:2},{name:"C",x:2,y:1},
    {name:"D",x:6,y:5},{name:"E",x:7,y:5},{name:"F",x:6,y:6}
  ];
  const initialCentres=[{x:1,y:1},{x:7,y:5}];
  const sqdist=(a,b)=>(a.x-b.x)**2+(a.y-b.y)**2;
  const assign=centres=>points.map(p=>
    sqdist(p,centres[0])<=sqdist(p,centres[1])?0:1);
  const firstAssignments=assign(initialCentres);
  const updatedCentres=[0,1].map(group=>{
    const members=points.filter((_,i)=>firstAssignments[i]===group);
    return {
      x:members.reduce((sum,p)=>sum+p.x,0)/members.length,
      y:members.reduce((sum,p)=>sum+p.y,0)/members.length
    };
  });
  const secondAssignments=assign(updatedCentres);
  if(secondAssignments.some((group,i)=>group!==firstAssignments[i])){
    throw new Error("K-means teaching example did not converge");
  }
  const NS="http://www.w3.org/2000/svg";
  const element=(tag,attrs={},content)=>{
    const el=document.createElementNS(NS,tag);
    for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
    if(content!==undefined)el.textContent=String(content);
    return el;
  };
  document.querySelectorAll("[data-cluster-plot]").forEach(svg=>{
    const stage=svg.getAttribute("data-cluster-plot");
    const color=["#447eae","#c08a51"];
    const X=x=>38+x*287/8;
    const Y=y=>18+(7-y)*218/7;
    svg.replaceChildren();
    for(let x=0;x<=8;x+=2){
      svg.append(
        element("line",{x1:X(x),y1:Y(0),x2:X(x),y2:Y(7),stroke:"#e2e9ee"}),
        element("text",{x:X(x),y:253,"text-anchor":"middle",
          "font-size":10,fill:"#617786"},x)
      );
    }
    for(let y=0;y<=7;y++){
      if(y%2!==0 && y!==7)continue;
      svg.append(
        element("line",{x1:X(0),y1:Y(y),x2:X(8),y2:Y(y),stroke:"#e2e9ee"}),
        element("text",{x:29,y:Y(y)+3,"text-anchor":"end",
          "font-size":10,fill:"#617786"},y)
      );
    }
    svg.append(
      element("text",{x:185,y:269,"text-anchor":"middle","font-size":11,fill:"#566f80"},"x"),
      element("text",{x:13,y:128,transform:"rotate(-90 13 128)",
        "text-anchor":"middle","font-size":11,fill:"#566f80"},"y")
    );
    const assignments=stage==="stable"?secondAssignments:firstAssignments;
    const centres=stage==="raw"||stage==="assigned"?initialCentres:updatedCentres;
    points.forEach((point,index)=>{
      const fill=stage==="raw"?"#8397a5":color[assignments[index]];
      svg.append(
        element("circle",{cx:X(point.x),cy:Y(point.y),r:7.5,
          fill,stroke:"#fff","stroke-width":1.5}),
        element("text",{x:X(point.x)+11,y:Y(point.y)-10,
          "font-size":13,"font-weight":"600",fill:"#334f62"},point.name)
      );
    });
    centres.forEach((point,i)=>{
      svg.append(
        element("circle",{cx:X(point.x),cy:Y(point.y),r:15.5,
          stroke:color[i],"stroke-width":2.7,fill:"none"}),
        element("path",{d:"M"+(X(point.x)-5)+" "+Y(point.y)+"h10M"+X(point.x)+" "+(Y(point.y)-5)+"v10",
          fill:"none",stroke:color[i],"stroke-width":2}),
        element("text",{x:X(point.x),y:Y(point.y)+29,
          "font-size":10,"text-anchor":"middle",fill:color[i]},"C"+(i+1))
      );
    });
    if(stage==="stable"){
      svg.append(
        element("rect",{x:225,y:16,width:99,height:24,rx:4,
          fill:"#f0f6f2",stroke:"#b4c9b9"}),
        element("text",{x:274,y:32,"text-anchor":"middle",
          "font-size":11,fill:"#3c7954"},"Unchanged")
      );
    }
  });

  // Sticky active-section navigation for desktop, compact collapsible mobile TOC.
  const toc=document.querySelector(".course-sidebar .toc-panel");
  if(toc){
    const mobile=window.matchMedia("(max-width:680px)");
    const syncToc=()=>{toc.open=!mobile.matches;};
    syncToc();
    mobile.addEventListener?.("change",syncToc);
    toc.querySelectorAll('a[href^="#"]').forEach(link=>{
      link.addEventListener("click",()=>{if(mobile.matches)toc.open=false;});
    });
    const ids=["one","two","three","four","five"];
    const sections=ids.map(id=>document.getElementById(id)).filter(Boolean);
    const navLinks=sections.map(el=>toc.querySelector('a[href="#'+el.id+'"]'));
    let scheduled=false;
    const update=()=>{
      scheduled=false;
      let active=0;
      sections.forEach((section,i)=>{
        if(section.getBoundingClientRect().top<=160)active=i;
      });
      navLinks.forEach((link,i)=>{
        if(link){
          if(active===i)link.setAttribute("aria-current","location");
          else link.removeAttribute("aria-current");
        }
      });
    };
    window.addEventListener("scroll",()=>{
      if(!scheduled){scheduled=true;window.requestAnimationFrame(update);}
    },{passive:true});
    update();
  }
})();
