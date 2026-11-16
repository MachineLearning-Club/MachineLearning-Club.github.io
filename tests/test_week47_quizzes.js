const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const fs=require('fs'),base='http://127.0.0.1:8877';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const page=await browser.newPage();page.on('dialog',async dialog=>await dialog.accept());
 for(let week=4;week<=7;week++){
  const bank=JSON.parse(fs.readFileSync(__dirname+'/../quiz/data/week-'+String(week).padStart(2,'0')+'.json','utf8'));
  await page.goto(base+'/quiz/',{waitUntil:'networkidle0'});
  await page.click('#take-test');
  await page.$eval('#access-input',(element,code)=>{element.value=code;},'MLC'+String(week).padStart(2,'0'));
  await page.click('#access-form button[type=submit]');
  await page.waitForSelector('#question-dialog[open]',{timeout:10000});
  for(let i=0;i<10;i++){
   await page.evaluate(index=>document.querySelectorAll('#question-nav button')[index].click(),i);
   const answer=bank.questions[i].correct;
   for(const index of answer)await page.evaluate(j=>document.querySelectorAll('#answers input')[j].click(),index);
  }
  await page.click('#finish-test');
  await page.waitForSelector('#summary-dialog[open]',{timeout:10000});
  const score=await page.$eval('#summary-points',el=>el.textContent);
  if(score!=='10 / 10')throw Error('Week '+week+' quiz score '+score);
  await page.click('#review-now');
  await page.waitForSelector('#question-dialog[open]',{timeout:10000});
  if(await page.$eval('#review-explanation',el=>el.hidden))throw Error('Week '+week+' explanation hidden');
  await page.click('#close-test');
  console.log('Week '+week+' complete quiz 10/10 with review PASS');
 }
 }finally{await browser.close();}
})().catch(error=>{console.error(error.stack);process.exit(1)});
