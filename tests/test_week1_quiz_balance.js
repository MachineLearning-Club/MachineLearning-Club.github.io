/* Week 1 quiz should assess probability as strongly as AI foundations. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const base='http://127.0.0.1:8877';
  const response=await page.goto(base+'/w1/quiz/',{waitUntil:'networkidle0'});
  assert.ok([200,304].includes(response.status()));
  const bank=await page.evaluate(async()=>(await (await fetch('/quiz/data/week-01.json')).json()));
  assert.equal(bank.questions.length,10);
  assert.equal(bank.questions.filter(q=>q.topic==='AI foundations').length,5);
  assert.equal(bank.questions.filter(q=>q.topic!=='AI foundations').length,5);
  assert.equal(bank.maximumPoints,10);
  assert.ok(bank.questions.every(q=>q.explanation.length>45&&q.options.length===4));
  await page.waitForSelector('.quiz-start-button');
  await page.click('.quiz-start-button');
  for(let i=0;i<10;i++){
    await page.click('button[aria-label="Go to question '+(i+1)+'"]');
    for(const index of bank.questions[i].correct){
      await page.evaluate(idx=>{
       const option=document.querySelector('.weekly-quiz-card input[value="'+idx+'"]');
       if(!option)throw new Error('Missing question option '+idx);
       option.click();
      },index);
    }
  }
  await page.click('.quiz-submit-button');
  await page.waitForFunction(()=>document.querySelector('#weekly-quiz')?.textContent.includes('Submitted: 10 / 10'),{timeout:4500});
  const scores=await page.evaluate(()=>JSON.parse(localStorage.getItem('mlclub.weekly-quiz.practice.v1.1')||'[]'));
  assert.equal(scores.at(-1).score,10);
  await page.reload({waitUntil:'networkidle0'});
  assert.ok((await page.$eval('#weekly-quiz',el=>el.textContent)).includes('Previous local attempt: 10 / 10'));
  await page.goto(base+'/quiz/',{waitUntil:'networkidle0'});
  assert.ok((await page.$eval('#quiz-rows',el=>el.textContent)).includes('AI, Probability and Learning from Data'));
  assert.deepEqual(errors,[]);
  console.log('WEEK 1 QUIZ BALANCE + TEN CORRECT + PERSISTENCE + CATALOG PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
