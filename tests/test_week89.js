const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const fs=require('fs');
const base='http://127.0.0.1:8877';
const assert=(v,m)=>{if(!v)throw Error(m)};
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage();
  const jsErrors=[];
  page.on('pageerror',e=>jsErrors.push(page.url()+': '+e.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:960,deviceScaleFactor:1});
   for(const week of [8,9]){
    for(const kind of ['course','lab','homework','advanced','quiz']){
     const url=base+'/w'+week+'/'+kind+'/';
     const res=await page.goto(url,{waitUntil:'networkidle0',timeout:28000});
     const state=await page.evaluate(()=>({
      width:document.documentElement.scrollWidth,
      viewport:document.documentElement.clientWidth,
      footer:document.querySelectorAll('footer.site.mlclub-footer').length,
      main:!!document.querySelector('main.week89-academic'),
      bib:!!document.querySelector('.page-bibliography')||!!document.querySelector('#weekly-quiz'),
      sidebar:document.querySelectorAll('.course-sidebar a').length,
      widget:document.querySelectorAll('[data-digit-lab]').length
     }));
     assert([200,304].includes(res.status()),'Bad HTTP '+week+kind);
     assert(state.width<=state.viewport+4,'Overflow '+week+kind+' '+width+' '+JSON.stringify(state));
     assert(state.footer===1&&state.main&&state.bib,'Missing page component '+week+kind);
     if(kind==='course')assert(state.sidebar>=7&&state.widget===1,'Missing course toc/demo '+week);
     if(kind==='lab')assert(state.sidebar>=7&&state.widget===1,'Missing lab toc/demo '+week);
     if(width===390&&kind==='course'){await page.$eval('[data-digit-lab]',e=>e.scrollIntoView({block:'start'}));await page.screenshot({path:'/tmp/mlclub-week'+week+'-mobile-widget.png'});}
     if(width===1280&&kind==='course')await page.screenshot({path:'/tmp/mlclub-week'+week+'-desktop-course.png'});
    }
    console.log('RESPONSIVE PASS week',week,width,'five pages');
   }
  }
  await page.setViewport({width:1280,height:900});
  await page.goto(base+'/w8/course/',{waitUntil:'networkidle0'});
  await page.waitForFunction(()=>document.querySelectorAll('[data-digit-grid] .digit-cell').length===64,{timeout:12000});
  assert((await page.$eval('[data-digit-output]',e=>e.textContent)).includes('Known digit: 2'),'Incorrect first label');
  assert((await page.$eval('[data-digit-neighbours]',e=>e.children.length))===3,'Missing three nearest neighbours');
  await page.click('[data-evaluate]');
  await page.waitForFunction(()=>document.querySelector('[data-evaluation-output]')?.textContent.includes('196 / 200'),{timeout:20000});
  console.log('REAL 200 DIGIT EVALUATION PASS');
  await page.select('[data-k-select]','5');
  await page.click('[data-evaluate]');
  await page.waitForFunction(()=>document.querySelector('[data-evaluation-output]')?.textContent.includes('195 / 200'),{timeout:20000});
  console.log('K=5 COMPARISON PASS');
  await page.select('[data-k-select]','3');
  await page.$eval('[data-case-index]',e=>{e.value=17;e.dispatchEvent(new Event('change',{bubbles:true}))});
  const mis=await page.$eval('[data-digit-output]',e=>e.textContent);
  assert(mis.includes('Known digit: 1 · predicted: 8'),'Incorrect nearest neighbour error '+mis);
  await page.click('[data-digit-grid] button:first-child');
  assert((await page.$eval('[data-digit-output]',e=>e.textContent)).includes('edited the pixels'),'Edit not communicated');
  await page.click('[data-reset-pixels]');
  assert(!(await page.$eval('[data-digit-output]',e=>e.textContent)).includes('edited the pixels'),'Pixel reset failed');
  console.log('INTERACTIVE EDIT/MISTAKE/RESET PASS');
  for(const week of [8,9]){
   await page.goto(base+'/w'+week+'/quiz/',{waitUntil:'networkidle0'});
   const start=await page.$('button.quiz-start-button');
   assert(start,'Quiz missing start button week '+week);
   await start.click();
   const choices=await page.$$('label.quiz-option input');
   assert(choices.length===4,'Quiz not displaying four choices');
   await page.click('label.quiz-option input:first-child');
   page.once('dialog',async dialog=>await dialog.accept());
   await page.click('button.quiz-submit-button');
   // just started; browser confirmation triggered by unanswered questions; see if app presents quiz review.
   await page.waitForFunction(()=>document.querySelector('.quiz-answer-explanation'),{timeout:6000});
   console.log('QUIZ RUNS & REVIEW PASS',week);
  }
  assert(!jsErrors.length,'JS errors '+JSON.stringify(jsErrors));
  console.log('ALL WEEK 8–9 BROWSER TESTS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
