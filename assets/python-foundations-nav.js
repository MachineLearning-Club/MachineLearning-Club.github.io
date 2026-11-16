/* Python foundations: use the same Contents-on-the-left navigation as the GitHub guide. */
(()=>{'use strict';
 const panel=document.querySelector('.foundations-toc-details');
 if(!panel)return;
 const links=[...panel.querySelectorAll('a[href^="#topic-"]')];
 let touched=false;
 const responsive=()=>{if(!touched)panel.open=!window.matchMedia('(max-width: 800px)').matches;};
 panel.addEventListener('toggle',()=>{if(document.readyState==='complete')touched=true;});
 responsive();
 const navigate=hash=>{
   const id=decodeURIComponent((hash||'').replace(/^#/,''));
   if(!/^topic-\d{2}$/.test(id))return;
   const lesson=document.getElementById(id);
   if(lesson&&lesson.tagName==='DETAILS'){
     lesson.open=true;
     links.forEach(a=>{if(a.hash==='#'+id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
   }
 };
 links.forEach(link=>link.addEventListener('click',()=>{
   navigate(link.hash);
   if(window.matchMedia('(max-width: 800px)').matches)panel.open=false;
   const lesson=document.getElementById(link.hash.slice(1));
   if(lesson)requestAnimationFrame(()=>lesson.scrollIntoView({block:'start'}));
 }));
 window.addEventListener('hashchange',()=>navigate(location.hash));
 navigate(location.hash);
})();