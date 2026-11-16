/* Load one real JupyterLite .ipynb at a time, on explicit student action. */
(()=>{'use strict';
const examples=new Set(['01-nearest-prototype.ipynb','02-biased-die.ipynb']);
const controls=[...document.querySelectorAll('[data-open-embedded]')];
const close=(button)=>{
 const card=button.closest('[data-notebook-card]');const slot=card.querySelector('.embedded-notebook-frame');
 slot.querySelector('.iframe-scroll').replaceChildren();
 slot.hidden=true;button.textContent='Run inside this page';button.setAttribute('aria-expanded','false');
};
for(const button of controls){
 button.setAttribute('aria-expanded','false');
 button.addEventListener('click',()=>{
  const file=button.dataset.openEmbedded;
  if(!examples.has(file))return;
  const card=button.closest('[data-notebook-card]'),slot=card.querySelector('.embedded-notebook-frame');
  if(!slot.hidden){close(button);return;}
  for(const other of controls)if(other!==button)close(other);
  const container=slot.querySelector('.iframe-scroll'),status=slot.querySelector('.embedded-notebook-status');
  status.textContent='Opening the actual JupyterLite notebook…';
  const iframe=document.createElement('iframe');
  iframe.title='Runnable JupyterLite notebook — '+file;
  iframe.setAttribute('referrerpolicy','same-origin');
  iframe.src='/jupyter/lab/index.html?path='+encodeURIComponent(file);
  iframe.addEventListener('load',()=>{status.textContent='Notebook editor loaded. Click a code cell, then press Shift + Enter to run it. Use Open full screen if the editor is too small.';},{once:true});
  container.append(iframe);slot.hidden=false;
  button.textContent='Close embedded notebook';button.setAttribute('aria-expanded','true');
 });
}
})();
