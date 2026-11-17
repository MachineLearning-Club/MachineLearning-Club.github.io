/* End-to-end browser checks for the linked FiiCode practice project. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const url='http://127.0.0.1:8877';
async function main(){
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,
    args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),issues=[];
  page.on('pageerror',e=>issues.push(e.message));
  const kinds=['course','lab','homework','advanced','quiz'];
  for(const width of [390,820,1280]){
    await page.setViewport({width,height:840});
    for(const w of [12,13,14,15]){
      for(const kind of kinds){
        const path='/w'+w+'/'+kind+'/';
        const response=await page.goto(url+path,{waitUntil:'domcontentloaded',timeout:15000});
        assert.equal(response.status(),200,path+' status');
        const info=await page.evaluate(()=>({
          fullWidth:document.documentElement.scrollWidth,
          clientWidth:document.documentElement.clientWidth,
          heading:!!document.querySelector('main h1'),
          footer:!!document.querySelector('footer.mlclub-footer'),
          brokenAssets:[...document.querySelectorAll('link[rel=stylesheet]')].filter(x=>!x.href).length,
        }));
        assert.ok(info.heading&&info.footer,'page chrome '+path);
        assert.ok(info.fullWidth<=info.clientWidth+5,
          'Document overflow '+path+' '+width+' '+JSON.stringify(info));
      }
    }
    console.log('RESPONSIVE PASS 20 pages width '+width);
  }
  await page.setViewport({width:1280,height:900});
  for(const path of ['/w12/lab/','/w13/course/','/w14/lab/','/w15/course/','/projects/study-space/']){
    await page.goto(url+path,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>document.querySelector('[data-prediction]') &&
      document.querySelector('[data-prediction]').textContent!=='Loading…',{timeout:12000});
    const pred=await page.$eval('[data-prediction]',el=>el.textContent);
    assert.equal(pred,'GOOD','default prediction '+path);
    await page.click('[data-evaluate]');
    let metrics=await page.$eval('[data-metrics]',el=>el.textContent);
    assert.ok(metrics.includes('39/45'),'k=3 validation '+path);
    await page.$eval('select[name=k]',el=>{el.value='1';el.dispatchEvent(new Event('input',{bubbles:true}))});
    await page.click('[data-evaluate]');
    metrics=await page.$eval('[data-metrics]',el=>el.textContent);
    assert.ok(metrics.includes('41/45'),'k=1 validation '+path);
    await page.$eval('input[name=occupancy]',el=>{el.value='95';el.dispatchEvent(new Event('input',{bubbles:true}))});
    await page.$eval('input[name=noise]',el=>{el.value='83';el.dispatchEvent(new Event('input',{bubbles:true}))});
    await page.$eval('input[name=wifi]',el=>{el.value='1';el.dispatchEvent(new Event('input',{bubbles:true}))});
    const newPrediction=await page.$eval('[data-prediction]',el=>el.textContent);
    assert.equal(newPrediction,'AVOID','updated profile '+path);
    const counts=await page.evaluate(async()=>{
      const data=await (await fetch('/assets/data/fiicode-study-space.json')).json();
      const P=window.StudySpacePractice;
      return [1,3,5,7].map(k=>P.evaluate(data.data.train,data.data.validation,k).correct);
    });
    assert.deepEqual(counts,[41,39,39,41],'JS vs Python scores');
    console.log('INTERACTIVE MODEL PASS '+path);
  }
  // Can read the ZIP's app.html directly from disk with no HTTP or fetch.
  await page.goto('file:///home/admin/projects/machinelearning-club/projects/study-space/app.html',{waitUntil:'load'});
  await page.waitForSelector('[data-prediction]',{timeout:10000});
  assert.equal(await page.$eval('[data-prediction]',e=>e.textContent),'GOOD','offline app');
  await page.click('[data-evaluate]');
  assert.ok((await page.$eval('[data-metrics]',e=>e.textContent)).includes('39/45'),'offline evaluation');
  console.log('OFFLINE APP PASS');
  for(const w of [12,13,14]){
    await page.goto(url+'/w'+w+'/quiz/',{waitUntil:'domcontentloaded'});
    await page.waitForSelector('.quiz-start-button',{timeout:15000});
    await page.click('.quiz-start-button');
    await page.waitForSelector('.weekly-quiz-card');
    const prompt=await page.$eval('.weekly-quiz-card h3',e=>e.textContent);
    assert.ok(prompt.length>20,'quiz question '+w);
    const bank=await (await page.evaluate(async w=>(await (await fetch('/quiz/data/week-'+String(w).padStart(2,'0')+'.json')).json()),w)).questions;
    assert.equal(bank.length,10);
    console.log('QUIZ PASS '+w);
  }
  await page.goto(url+'/w15/quiz/',{waitUntil:'domcontentloaded'});
  assert.ok((await page.$eval('main',e=>e.textContent)).includes('20-point rubric'));
  await page.goto(url+'/quiz/',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('#quiz-rows tr',{timeout:12000});
  const hub=await page.$eval('#quiz-rows',e=>e.textContent);
  assert.ok(hub.includes('Study Space Challenge') && hub.includes('Project review'));
  console.log('RUBRIC AND HUB PASS');
  assert.deepEqual(issues,[],'runtime exceptions: '+issues.join(', '));
  console.log('ALL STUDY SPACE BROWSER TESTS PASS');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e.stack);process.exit(1)});
