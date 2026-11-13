
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
