/* Integration test: Week 10–11 knowledge checks are answerable quizzes. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const ROOT='http://127.0.0.1:8877';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,
   args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  for(const week of [10,11]){
    const response=await page.goto(ROOT+'/w'+week+'/quiz/',{waitUntil:'networkidle0'});
    assert.equal(response.status(),200);
    await page.waitForSelector('.quiz-start-button');
    const bank=await page.evaluate(async n=>(await (await fetch('/quiz/data/week-'+n+'.json')).json()),week);
    assert.equal(bank.week,week);
    assert.equal(bank.questions.length,10);
    assert.equal(bank.questions.reduce((sum,q)=>sum+q.points,0),10);
    assert.ok(bank.questions.every(q=>q.explanation.length>20 && q.options.length===4));
    await page.click('.quiz-start-button');
    for(let i=0;i<10;i++){
      await page.click('button[aria-label="Go to question '+(i+1)+'"]');
      const q=bank.questions[i];
      for(const option of q.correct){
        await page.evaluate(idx=>{
          const input=document.querySelector('.weekly-quiz-card input[value="'+idx+'"]');
          if(!input)throw new Error('No option '+idx);
          input.click();
        },option);
      }
    }
    await page.click('.quiz-submit-button');
    await page.waitForFunction(()=>document.querySelector('#weekly-quiz')?.textContent.includes('Submitted: 10 / 10'));
    const storage=await page.evaluate(n=>JSON.parse(localStorage.getItem('mlclub.weekly-quiz.practice.v1.'+n)||'[]'),week);
    assert.equal(storage.at(-1).score,10);
    await page.reload({waitUntil:'networkidle0'});
    assert.ok((await page.$eval('#weekly-quiz',el=>el.textContent)).includes('Previous local attempt: 10 / 10'));
    console.log('W'+week+' QUIZ 10/10 + RELOAD PASS');
  }
  await page.goto(ROOT+'/quiz/',{waitUntil:'networkidle0'});
  const catalog=await page.$eval('#quiz-rows',el=>el.textContent);
  assert.ok(catalog.includes('Language, Recommendations and Verification'));
  assert.ok(catalog.includes('Software Engineering: Components, Tests and Git'));
  const count=await page.$eval('#available-count',el=>el.textContent);
  assert.equal(Number(count),14);
  const status=await page.$eval('main',el=>el.textContent);
  assert.ok(status.includes('Weeks 1–14'));
  assert.deepEqual(errors,[],'Browser exceptions: '+errors.join(' | '));
  console.log('QUIZ HUB 14 AVAILABLE + NO SCRIPT ERRORS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
