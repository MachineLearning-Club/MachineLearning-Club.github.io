const puppeteer = require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const path = '/home/admin/projects/mlc-site-update-2026/quiz/';
const base='http://127.0.0.1:8765';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage();
  await page.setViewport({width:1350,height:900,deviceScaleFactor:1});
  page.on('dialog', async dialog=>await dialog.accept());
  const exceptions=[];
  page.on('pageerror',e=>exceptions.push(e.message));
  await page.goto(base+'/quiz/',{waitUntil:'networkidle0'});
  await page.evaluate(()=>localStorage.clear());
  await page.reload({waitUntil:'networkidle0'});
  const rows=await page.$$eval('#quiz-rows tr',a=>a.length);
  if(rows!==15)throw Error('Expected 15 week rows, got '+rows);
  console.log('Catalogue: 15 rows');
  await page.screenshot({path:'/tmp/mlclub-quiz-dashboard.png'});
  await page.click('#take-test');
  if(!(await page.$eval('#access-dialog',e=>e.open)))throw Error('Access form not visible');
  await page.type('#access-input','TEST-INVALID');
  await page.click('#access-form button[type=submit]');
  let error=await page.$eval('#access-error',e=>e.textContent);
  if(!error.includes('No demo quiz'))throw Error('Access validation failed');
  await page.$eval('#access-input',el=>{el.value='MLC02';});
  await page.click('#access-form button[type=submit]');
  await page.waitForSelector('#question-dialog[open]',{timeout:5000});
  if(!(await page.$eval('#review-explanation',e=>e.hidden)))throw Error('Answers leaked during test');
  const qText=await page.$eval('#question-text',e=>e.textContent);
  if(!qText.toLowerCase().includes('decision tree'))throw Error('Week2 first question missing');
  await page.screenshot({path:'/tmp/mlclub-quiz-exam.png'});
  const fs=require('fs');
  const bank=JSON.parse(fs.readFileSync(path+'data/week-02.json','utf8'));
  for(let i=0;i<10;i++){
    await page.evaluate(index=>document.querySelectorAll('#question-nav button')[index].click(),i);
    const q=bank.questions[i];
    for(const answer of q.correct){
      await page.evaluate(a=>document.querySelectorAll('#answers input')[a].click(),answer);
    }
    const n=await page.$eval('#answered-index',x=>x.textContent);
    if(!n.includes((i+1)+' / 10'))throw Error('Answer count off at '+i+': '+n);
  }
  await page.click('#finish-test');
  await page.waitForSelector('#summary-dialog[open]',{timeout:5000});
  const score=await page.$eval('#summary-points',e=>e.textContent);
  if(score!=='10 / 10')throw Error('Scoring mismatch '+score);
  console.log('Perfect-score 10/10 submission');
  await page.screenshot({path:'/tmp/mlclub-quiz-result.png'});
  await page.click('#review-now');
  await page.waitForSelector('#question-dialog[open]',{timeout:5000});
  if(await page.$eval('#review-explanation',e=>e.hidden))throw Error('Review not visible');
  const reviewScore=await page.$eval('#exam-status',e=>e.textContent);
  if(!reviewScore.includes('10 / 10'))throw Error('Review score missing');
  await page.click('#close-test');
  const results=await page.$$eval('#history-rows tr',a=>a.length);
  if(results!==1)throw Error('Missing history');
  await page.reload({waitUntil:'networkidle0'});
  const persisted=await page.$eval('#history-rows',e=>e.textContent);
  if(!persisted.includes('10 / 10'))throw Error('Local persistence missing');
  console.log('History persisted across reload');
  await page.click('#take-test');
  await page.$eval('#access-input',e=>{e.value='MLC03';});
  await page.click('#access-form button[type=submit]');
  await page.waitForSelector('#question-dialog[open]',{timeout:5000});
  await page.click('#next-question');
  await page.click('#finish-test');
  await page.waitForSelector('#summary-dialog[open]',{timeout:5000});
  const scoreUnanswered=await page.$eval('#summary-points',e=>e.textContent);
  if(scoreUnanswered!=='0 / 10')throw Error('Unanswered scoring incorrect');
  await page.click('#review-now');
  const rationale=await page.$eval('#review-explanation',e=>e.textContent);
  if(!rationale.includes('Correct selection:'))throw Error('Explanations not shown');
  await page.click('#close-test');
  await page.screenshot({path:'/tmp/mlclub-quiz-history.png'});
  console.log('Unanswered 0/10 scoring, correct review feedback');
  const finalRows=await page.$$eval('#history-rows tr',a=>a.length);
  if(finalRows!==2)throw Error('Expected two saved attempts');
  for(const width of [375,768,1350]){
    await page.setViewport({width,height:850});
    await page.goto(base+'/quiz/',{waitUntil:'networkidle0'});
    const w=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth}));
    if(w.scroll>w.client+1)throw Error('Horizontal overflow '+width+': '+JSON.stringify(w));
    console.log('Viewport',width,'PASS');
  }
  if(exceptions.length)throw Error('Page JS errors: '+exceptions.join('; '));
  console.log('ALL QUIZ TESTS PASS');
  await page.close();
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1);});
