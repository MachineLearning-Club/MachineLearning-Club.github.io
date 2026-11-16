/* Guide-only enhancements. The instructions and screenshots still work without JS. */
(()=>{'use strict';
const username=document.querySelector('[data-gh-username]');
const output=document.querySelector('[data-gh-url]');
const copyUrl=document.querySelector('[data-copy-url]');
const makeUrl=()=>{const name=username?.value.trim().replace(/^@/,'')||'';return /^[a-z\d](?:[a-z\d-]{0,37}[a-z\d])?$/i.test(name)?'https://'+name+'.github.io/my-first-ai-site/':null;};
if(username&&output){
 const update=()=>{const url=makeUrl();output.textContent=url||'https://USERNAME.github.io/my-first-ai-site/';username.setAttribute('aria-invalid',String(!!username.value&&!url));};
 username.addEventListener('input',update);update();
}
const announce=(button,message)=>{const before=button.textContent;button.textContent=message;setTimeout(()=>button.textContent=before,1800);};
async function copyText(value,button){
 if(!value){announce(button,'Enter a valid username');return;}
 try{await navigator.clipboard.writeText(value);announce(button,'Copied');}
 catch(e){announce(button,'Select and copy the text');}
}
if(copyUrl){copyUrl.addEventListener('click',()=>copyText(makeUrl(),copyUrl));}
document.querySelectorAll('[data-copy]').forEach(button=>{
 button.addEventListener('click',()=>{const value=document.getElementById(button.dataset.copy)?.textContent||'';copyText(value,button);});
});
})();