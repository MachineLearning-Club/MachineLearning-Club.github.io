/* Shared, dependency-free site interactions. */
(() => {
"use strict";
const by=(q,root=document)=>root.querySelector(q);
const all=(q,root=document)=>Array.from(root.querySelectorAll(q));
all('[data-week-picker]').forEach(select=>{
  select.addEventListener('change',()=>{
    const n=Number(select.value),kind=select.dataset.kind;
    if(n>=1&&n<=15&&['course','lab','homework','advanced','quiz'].includes(kind))location.href='/w'+n+'/'+kind+'/';
  });
});
const moduleSelect=by('#timetable-module');
if(moduleSelect)moduleSelect.addEventListener('change',()=>{
  all('.timetable-grid tbody tr').forEach(row=>{row.hidden=moduleSelect.value!=='all'&&row.dataset.module!==moduleSelect.value;});
});
const git=by('.git-simulator');
if(git){
  const editor=by('.git-code',git), log=by('.git-history',git),out=by('.git-output',git);
  const history=[{code:editor.value,text:'Initial project'}];
  const display=()=>{log.replaceChildren();history.forEach((item,i)=>{const li=document.createElement('li');li.textContent='Version '+i+': '+item.text;log.append(li);});};
  by('[data-git-test]',git).addEventListener('click',()=>{
    out.textContent=editor.value.includes('def predict')?'Code contains a predict function; now describe one example input/output to test.':'Check that your project still defines predict(x).';
  });
  by('[data-git-commit]',git).addEventListener('click',()=>{
    if(editor.value===history[history.length-1].code){out.textContent='Nothing changed since the previous commit.';return;}
    history.push({code:editor.value,text:'Saved edited code ('+editor.value.length+' characters)'});
    out.textContent='Saved version '+(history.length-1)+'. This is a simulated commit, stored only on this page.';display();
  });
  by('[data-git-undo]',git).addEventListener('click',()=>{
    editor.value=history[history.length-1].code;out.textContent='Restored last saved version.';
  });
  display();
}
const normaliseName=str=>str.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Za-z0-9 _-]/g,'').trim().replace(/[\s_]+/g,'_').slice(0,75);
const allowed=/\.(ipynb|py|csv|zip|txt)$/i;
const u16=(dv,offset,val)=>dv.setUint16(offset,val,true);
const u32=(dv,offset,val)=>dv.setUint32(offset,val>>>0,true);
const crcTable=Array.from({length:256},(_,n)=>{
  let c=n;for(let i=0;i<8;i++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0;
});
const crc32=bytes=>{
  let crc=0xffffffff;for(const v of bytes)crc=crcTable[(crc^v)&255]^(crc>>>8);
  return (crc^0xffffffff)>>>0;
};
function encodeZip(name,records){
  // ZIP with uncompressed stored files. Does not upload anything.
  const encoder=new TextEncoder();
  const files=[{name:'README.txt',bytes:encoder.encode(name)},...records];
  const parts=[],central=[];let offset=0;
  const now=new Date();
  const date=((Math.max(1980,now.getFullYear())-1980)<<9)|((now.getMonth()+1)<<5)|now.getDate();
  const time=(now.getHours()<<11)|(now.getMinutes()<<5)|Math.floor(now.getSeconds()/2);
  for(const item of files){
    const fname=encoder.encode(item.name),body=item.bytes,crc=crc32(body);
    const local=new Uint8Array(30+fname.length),v=new DataView(local.buffer);
    u32(v,0,0x04034b50);u16(v,4,20);u16(v,6,0);u16(v,8,0);u16(v,10,time);u16(v,12,date);
    u32(v,14,crc);u32(v,18,body.length);u32(v,22,body.length);u16(v,26,fname.length);u16(v,28,0);local.set(fname,30);
    parts.push(local,body);
    const c=new Uint8Array(46+fname.length),cv=new DataView(c.buffer);
    u32(cv,0,0x02014b50);u16(cv,4,20);u16(cv,6,20);u16(cv,8,0);u16(cv,10,0);u16(cv,12,time);u16(cv,14,date);
    u32(cv,16,crc);u32(cv,20,body.length);u32(cv,24,body.length);u16(cv,28,fname.length);
    u16(cv,30,0);u16(cv,32,0);u16(cv,34,0);u16(cv,36,0);u32(cv,38,0);u32(cv,42,offset);c.set(fname,46);
    central.push(c);offset+=local.length+body.length;
  }
  const centralSize=central.reduce((sum,item)=>sum+item.length,0);
  const end=new Uint8Array(22),ev=new DataView(end.buffer);
  u32(ev,0,0x06054b50);u16(ev,4,0);u16(ev,6,0);u16(ev,8,files.length);u16(ev,10,files.length);
  u32(ev,12,centralSize);u32(ev,16,offset);u16(ev,20,0);
  return new Blob([...parts,...central,end],{type:'application/zip'});
}
all('.submission-form').forEach(form=>{
  const input=by('.submission-files',form), student=by('.student-name',form),label=by('.file-drop',form),selected=by('.submission-selected',form),status=by('.submission-status',form);
  let chosen=[];
  const pick=files=>{
    chosen=Array.from(files).slice(0,6).filter(file=>allowed.test(file.name)&&file.size<=12*1024*1024);
    selected.textContent=chosen.length?chosen.map(f=>f.name+' ('+Math.round(f.size/1024)+' KB)').join(' · '):'No supported file selected (.ipynb, .py, .csv, .zip or .txt; ≤12 MB each).';
  };
  input.addEventListener('change',()=>pick(input.files));
  label.addEventListener('dragover',e=>{e.preventDefault();label.classList.add('dragover');});
  label.addEventListener('dragleave',()=>label.classList.remove('dragover'));
  label.addEventListener('drop',e=>{
    e.preventDefault();label.classList.remove('dragover');pick(e.dataTransfer.files);
  });
  by('.prepare-submission',form).addEventListener('click',async()=>{
    const studentName=normaliseName(student.value),week=Number(form.dataset.submissionWeek);
    if(studentName.length<3){status.textContent='Enter your first and last name before preparing the file.';status.classList.add('error');student.focus();return;}
    if(!chosen.length){status.textContent='Choose at least one supported file first.';status.classList.add('error');return;}
    status.classList.remove('error');
    status.textContent='Preparing a local ZIP file…';
    const records=await Promise.all(chosen.map(async file=>({name:file.name.replace(/[/\\]/g,'_'),bytes:new Uint8Array(await file.arrayBuffer())})));
    const readme='Machine Learning Club submission\nStudent: '+student.value.trim()+'\nWeek: '+week+'\nFiles: '+records.map(x=>x.name).join(', ')+'\nThis archive was prepared locally; it has NOT been uploaded.\n';
    const archive=encodeZip(readme,records);
    const url=URL.createObjectURL(archive);
    const a=document.createElement('a');
    a.href=url;a.download='MLC_Week_'+String(week).padStart(2,'0')+'_'+studentName+'.zip';
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    status.textContent='Downloaded a named ZIP. This does not upload it. Keep it until your teacher provides the collection link.';
  });
});
// A Dropbox File Request is only shown after a teacher configures a real URL.
fetch('/data/submissions.json').then(r=>r.ok?r.json():null).then(config=>{
  const url=typeof config?.request_url==='string'?config.request_url:'';
  if(!/^https:\/\/(?:www\.)?dropbox\.com\/request\/[A-Za-z0-9]+$/.test(url))return;
  all('.submission-form').forEach(form=>{
    const p=document.createElement('p'),link=document.createElement('a');
    link.href=url;link.target='_blank';link.rel='noopener noreferrer';
    link.textContent='Upload your prepared ZIP to the teacher’s Dropbox File Request';
    p.append(link);form.append(p);
  });
}).catch(()=>{});
all('.python-runner').forEach(widget=>{
  const editor=by('.py-source',widget),out=by('.py-output',widget),button=by('.run-python',widget);
  let worker=null;
  const stop=document.createElement('button');stop.type='button';stop.textContent='Stop';stop.hidden=true;stop.className='stop-python';
  button.after(stop);
  stop.addEventListener('click',()=>{if(worker)worker.terminate();worker=null;stop.hidden=true;button.disabled=false;out.textContent+='\\nStopped.';});
  button.addEventListener('click',()=>{
    if(worker){worker.terminate();worker=null;}
    out.textContent='Loading Python in this browser…';button.disabled=true;stop.hidden=false;
    worker=new Worker('/assets/python-worker.js');
    const current=worker;
    worker.onmessage=event=>{
      if(current!==worker)return;
      if(event.data.type==='ready')out.textContent='Running code…';
      if(event.data.type==='output')out.textContent=event.data.value;
      if(event.data.type==='done'){out.textContent=event.data.value||'(No output)';stop.hidden=true;button.disabled=false;worker.terminate();worker=null;}
      if(event.data.type==='error'){out.textContent='Python error: '+event.data.value;stop.hidden=true;button.disabled=false;worker.terminate();worker=null;}
    };
    worker.onerror=event=>{out.textContent='Python could not start. Check the internet connection and try again.';stop.hidden=true;button.disabled=false;worker.terminate();worker=null;};
    worker.postMessage({code:editor.value});
  });
});
})();