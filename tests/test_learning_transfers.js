/* Readable learning-transfer sections should survive rendering and work on phones. */
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const assert=require('node:assert/strict');
const BASE='http://127.0.0.1:8877';
(async()=>{
 const browser=await puppeteer.launch({
  executablePath:'/usr/bin/chromium',headless:true,
  args:['--no-sandbox','--disable-dev-shm-usage']
 });
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:900});
   for(let week=1;week<=7;week++){
    for(const kind of ['course','lab','homework']){
     const url=BASE+'/w'+week+'/'+kind+'/';
     const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:15000});
     assert.equal(response.status(),200,url);
     const marker=kind==='course'?'learning-transfer-w'+week:
       kind==='lab'?'learning-transfer-lab-w'+week:'learning-transfer-homework-w'+week;
     const info=await page.evaluate(marker=>{
      const section=document.getElementById(marker);
      return {
       exists:!!section,
       css:!!document.querySelector('link[href="/assets/learning-transfers.css"]'),
       heading:section?.querySelector('h2')?.textContent||'',
       horizontal:document.documentElement.scrollWidth-document.documentElement.clientWidth,
       source:!!document.querySelector('.lesson-content'),
       labTicket:!!section?.querySelector('.transfer-evidence'),
       worked:!!section?.querySelector('.transfer-worked'),
       review:!!section?.querySelector('a[href*="/course/#learning-transfer"]')
      };
     },marker);
     assert.ok(info.exists && info.css && info.source,'Section missing '+url+' '+JSON.stringify(info));
     assert.ok(info.heading.length>9,'Empty transfer heading '+url);
     assert.ok(info.horizontal<=5,'Horizontal overflow '+url+' '+width+' '+info.horizontal);
     if(kind==='lab')assert.ok(info.labTicket && info.review,'Lab transfer missing evidence '+url);
     if(kind==='course')assert.ok(info.worked,'Course lacks an inspectable worked example '+url);
     if(width===1280&&kind==='course'){
      const href='#learning-transfer-w'+week;
      assert.equal(await page.$eval('.toc-panel',(el,target)=>el.querySelectorAll('a[href="'+target+'"]').length,href),1);
      const detail='#learning-transfer-w'+week+' .transfer-worked details';
      assert.ok(await page.$(detail),'Missing answer reveal '+url);
      await page.$eval(detail,el=>el.open=true);
      assert.ok((await page.$eval(detail,el=>el.textContent)).length>110);
     }
    }
   }
   console.log('TRANSFER RESPONSIVE PASS: 21 pages at '+width+' px');
  }
  for(let week=1;week<=7;week++){
   await page.goto(BASE+'/w'+week+'/course/',{waitUntil:'networkidle0'});
   const text=await page.$eval('#learning-transfer-w'+week,el=>el.textContent);
   assert.ok(text.length>450,'Section too thin Week '+week);
   assert.ok(text.includes('Week '+(week+1)),'No forward conceptual link Week '+week);
  }
  const w6=await page.goto(BASE+'/w6/lab/',{waitUntil:'domcontentloaded'});
  assert.ok([200,304].includes(w6.status()));
  assert.ok((await page.$eval('#learning-transfer-lab-w6',el=>el.textContent)).includes('three'));
  await page.goto(BASE+'/w7/course/',{waitUntil:'domcontentloaded'});
  assert.ok((await page.$eval('#learning-transfer-w7',el=>el.textContent)).includes('0.05'));
  assert.deepEqual(errors,[],'JS exceptions: '+errors.join('; '));
  console.log('ALL TRANSFER CONTENT, LINKS, LAYOUT AND REVEAL CHECKS PASS');
 }finally{await browser.close();}
})().catch(err=>{console.error(err.stack);process.exit(1)});
