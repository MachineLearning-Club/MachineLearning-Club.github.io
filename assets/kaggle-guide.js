/* Three-row CSV exercise. Not an official Kaggle competition submission. */
(()=>{'use strict';
const root=document.querySelector('[data-kaggle-demo]');if(!root)return;
const fields=[...root.querySelectorAll('[data-prediction]')],preview=root.querySelector('[data-kaggle-preview]');
const csv=()=>['PassengerId,Survived',...fields.map(f=>f.dataset.prediction+','+f.value)].join('\n')+'\n';
function update(){preview.textContent=csv();}
fields.forEach(f=>f.addEventListener('change',update));update();
root.querySelector('[data-download-practice]').addEventListener('click',()=>{
 const blob=new Blob([csv()],{type:'text/csv;charset=utf-8'});
 const url=URL.createObjectURL(blob);
 const link=document.createElement('a');link.href=url;link.download='practice_only.csv';
 document.body.append(link);link.click();link.remove();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
})();