/* Week 1 lab: active contents navigation and a safe prompt composer. */
(() => {
  "use strict";
  const root=document.querySelector(".lab-lesson");
  if(!root)return;
  const nav=root.querySelector(".course-sidebar .toc-panel");
  if(nav){
    const mq=matchMedia("(max-width:680px)");
    const sync=()=>{nav.open=!mq.matches;};
    sync();mq.addEventListener?.("change",sync);
    const links=[...nav.querySelectorAll('a[href^="#"]')];
    const sections=links.map(link=>document.getElementById(link.getAttribute("href").slice(1)));
    for(const link of links){
      link.addEventListener("click",()=>{if(mq.matches)nav.open=false;});
    }
    let queued=false;
    function refresh(){
      queued=false;
      let active=0;
      sections.forEach((s,i)=>{if(s&&s.getBoundingClientRect().top<=160)active=i;});
      links.forEach((link,i)=>{if(i===active)link.setAttribute("aria-current","location");else link.removeAttribute("aria-current");});
    }
    addEventListener("scroll",()=>{if(!queued){queued=true;requestAnimationFrame(refresh);}},{passive:true});
    refresh();
  }
  const box=root.querySelector("[data-coffee-prompt]");
  if(box){
    const theme=box.querySelector("[data-theme]"), color=box.querySelector("[data-color]"),
      character=box.querySelector("[data-character]"),text=box.querySelector("[data-prompt-text]"),
      state=box.querySelector("[data-prompt-status]"),copy=box.querySelector("[data-copy-prompt]");
    function value(el,fallback){return el.value.trim().slice(0,100)||fallback;}
    function update(){
      const t=value(theme,"cosy café"),c=value(color,"deep emerald green"),ch=value(character,"a friendly fox");
      text.textContent="Generate a complete, interactive, mobile-friendly HTML website for a coffee shop themed around "+t+". "+
        "Its brand identity colour is "+c+", and its recurring brand character is "+ch+". "+
        "Create a visually coherent homepage with a coffee menu showing item names and prices, working Add to cart "+
        "buttons, quantity controls, a cart showing the correct running total, and a Checkout button that "+
        "SIMULATES an order confirmation only. Use self-contained HTML, CSS, and JavaScript in one file; "+
        "do not use backend services, real payments, credit-card fields, accounts, or personal information. "+
        "The website should work on mobile and be usable through a keyboard. Include at least four menu items.";
      state.textContent="";
    }
    for(const input of [theme,color,character])input.addEventListener("input",update);
    copy.addEventListener("click",async()=>{
      try{await navigator.clipboard.writeText(text.textContent);state.textContent="Prompt copied.";}
      catch(_){
        const range=document.createRange();range.selectNodeContents(text);
        const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);
        state.textContent="Select and copy the highlighted prompt with Ctrl+C.";
      }
    });
    update();
  }
})();