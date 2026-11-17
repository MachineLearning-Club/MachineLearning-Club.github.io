const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const base='http://127.0.0.1:8877';const check=(v,m)=>{if(!v)throw Error(m)};
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try {
 const page=await browser.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 for(const width of [390,820,1280]){
  await page.setViewport({width,height:900});
  for(const n of [10,11]){
   for(const kind of ['course','lab','homework','advanced']){
    const r=await page.goto(base+'/w'+n+'/'+kind+'/',{waitUntil:'networkidle0',timeout:25000});
    const info=await page.evaluate(()=>({
     tw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
     css:!!document.querySelector('link[href*="week1011.css"]'),
     main:!!document.querySelector('main.week1011-academic'),
     bib:!!document.querySelector('.page-bibliography'),
     toc:document.querySelectorAll('.course-sidebar a').length,
     footer:!!document.querySelector('footer.site.mlclub-footer')
    }));
    check([200,304].includes(r.status()),'http '+n+kind);
    check(info.tw<=info.cw+4,'overflow '+n+'/'+kind+' '+width+' '+JSON.stringify(info));
    check(info.main&&info.css&&info.bib&&info.footer,'missing UI '+n+'/'+kind);
    if(kind==='course')check(info.toc>=5,'no contents nav '+n);
    if(kind==='lab')check(info.toc>=4,'no lab contents nav '+n);
    if(width===390&&kind==='course')await page.screenshot({path:'/tmp/mlc-w'+n+'-mobile-course.png',fullPage:true});
    if(width===1280&&kind==='course')await page.screenshot({path:'/tmp/mlc-w'+n+'-desktop-course.png',fullPage:true});
   }
   console.log('RESPONSIVE PASS week '+n+' width '+width);
  }
 }
 await page.setViewport({width:1280,height:900});
 await page.goto(base+'/w10/course/',{waitUntil:'networkidle0'});
 check((await page.$eval('[data-token-output]',el=>el.textContent)).includes('5 units'),'initial token count wrong');
 await page.$eval('[data-token-text]',el=>{el.value='Hello, AI!';el.dispatchEvent(new Event('input',{bubbles:true}))});
 check((await page.$eval('[data-token-output]',el=>el.textContent)).includes('4 units'),'tokenizer update failed');
 await page.click('[data-word=cloudy]');
 check((await page.$eval('[data-next-result]',el=>el.textContent)).includes('30%'),'toy next-token update failed');
 check((await page.$eval('[data-feed-result]',el=>el.textContent)).includes('Science ranks first'),'feed default');
 await page.$eval('[data-clicks=music]',el=>{el.value='8';el.dispatchEvent(new Event('input',{bubbles:true}))});
 check((await page.$eval('[data-feed-result]',el=>el.textContent)).includes('Music ranks first'),'feed ranking');
 console.log('W10 INTERACTIVE PASS');
 const strongInline=await page.$eval('.core-idea p strong',e=>getComputedStyle(e).display);
 check(strongInline==='inline','bold inline emphasis incorrectly styled as heading: '+strongInline);
 await page.goto(base+'/w11/course/',{waitUntil:'networkidle0'});
 check((await page.$eval('[data-pipeline-trace]',el=>el.textContent)).includes('HEAT ON'),'sensor default');
 await page.$eval('[data-temperature]',el=>{el.value='21';el.dispatchEvent(new Event('input',{bubbles:true}))});
 check((await page.$eval('[data-pipeline-trace]',el=>el.textContent)).includes('HEAT OFF'),'sensor rule');
 await page.click('[data-missing]');
 check((await page.$eval('[data-pipeline-trace]',el=>el.textContent)).includes('CHECK SENSOR'),'missing sensor check');
 console.log('W11 INTERACTIVE PASS');
 // Previously missing Week 10/11 file-selection/download workflow.
 const fs=require('fs');
 const sample='/tmp/mlc-week1011-submission.txt';
 fs.writeFileSync(sample,'A classroom-only notebook observation.\\n');
 for(const week of [10,11]){
  await page.goto(base+'/w'+week+'/lab/',{waitUntil:'networkidle0'});
  const formInfo=await page.evaluate(()=>({
   week:document.querySelector('.submission-form')?.dataset.submissionWeek,
   upload:!!document.querySelector('.submission-files'),
   download:!!document.querySelector('.prepare-submission'),
   guide:document.querySelector('#l11-git')?.textContent||''
  }));
  check(formInfo.week===String(week) && formInfo.upload && formInfo.download,'Missing submission controls '+week);
  if(week===11) check(formInfo.guide.includes('real GitHub') && formInfo.guide.includes('push'),'Outdated Git workflow');
  await page.type('.student-name','Test Student');
  await (await page.$('.submission-files')).uploadFile(sample);
  const chosen=await page.$eval('.submission-selected',e=>e.textContent);
  check(chosen.includes('mlc-week1011-submission.txt'),'file selection not reflected '+week);
  await page.click('.prepare-submission');
  await page.waitForFunction(()=>document.querySelector('.submission-status').textContent.includes('Downloaded a named ZIP'),{timeout:12000});
  check((await page.$eval('.submission-status',e=>e.textContent)).includes('does not upload'),'misleading delivery status '+week);
  console.log('WEEK '+week+' SUBMISSION UI PASS');
 }
 await page.goto(base+'/guides/github-ai/',{waitUntil:'networkidle0'});
 check((await page.$eval('#gg-sources',el=>el.textContent)).includes('GitHub Docs'),'GitHub Guide bibliography missing');
 await page.goto(base+'/resources/',{waitUntil:'networkidle0'});
 check((await page.$eval('main',el=>el.textContent)).includes('Gavriluț'),'Resource index bibliography missing');
 check(!errors.length,'JS exceptions '+JSON.stringify(errors));
 console.log('ALL WEEK 10-11 TESTS PASS');
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exit(1)});
