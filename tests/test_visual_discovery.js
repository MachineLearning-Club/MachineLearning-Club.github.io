/* Verify new pre-university concept studios without changing core ID3/K-means algorithms. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const BASE='http://127.0.0.1:8877';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,
   args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:840});
   for(const week of [2,3]){
    const response=await page.goto(BASE+'/w'+week+'/course/',{waitUntil:'networkidle0'});
    assert.ok([200,304].includes(response.status()));
    const status=await page.evaluate(()=>{
      const root=document.querySelector('.discovery-studio');
      const objective=document.querySelector('.learning-intention');
      return {
       root:!!root,objective:!!objective,
       header:!!document.querySelector('.lesson-header'),
       horiz:document.documentElement.scrollWidth-document.documentElement.clientWidth,
       maths:!!document.querySelector('.discovery-math:not([open])'),
       stages:document.querySelectorAll('.discovery-stepper li').length,
       cases:document.querySelectorAll('.discovery-day').length
      };
    });
    assert.ok(status.root&&status.objective&&status.header&&status.maths,JSON.stringify({week,width,status}));
    assert.ok(status.horiz<=5,'Overflow '+JSON.stringify({week,width,status}));
    assert.equal(status.cases,week===2?12:0);
    assert.equal(status.stages,week===3?4:0);
    console.log('STUDIO LAYOUT PASS',week,width);
   }
  }
  await page.goto(BASE+'/w2/course/',{waitUntil:'networkidle0'});
  const inspect=()=>page.evaluate(()=>{
    const selected=document.querySelector('[data-id3-feature][aria-pressed=true]').dataset.id3Feature;
    const groups=[...document.querySelectorAll('.id3-group')].map(group=>({
      label:group.querySelector('strong')?.textContent,
      yes:group.querySelectorAll('.discovery-day.is-yes').length,
      no:group.querySelectorAll('.discovery-day.is-no').length
    }));
    const insight=document.querySelector('.discovery-summary')?.textContent;
    const gain=document.querySelector('[data-id3-gain]')?.textContent;
    return {selected,groups,insight,gain};
  });
  let data=await inspect();
  assert.equal(data.selected,'sky');
  assert.deepEqual(data.groups.map(g=>[g.yes,g.no]),[[4,0],[2,2],[0,4]]);
  assert.ok(data.insight.includes('2 of 3')&&data.gain.includes('0.667'));
  for(const [feature,pure,score] of [['wind','0 of 2','0.082'],['temperature','0 of 2','0 bits'],['sky','2 of 3','0.667']]){
    await page.click('[data-id3-feature="'+feature+'"]');
    await page.waitForFunction(f=>document.querySelector('.discovery-summary')?.textContent.includes(f),{},pure);
    data=await inspect();
    assert.equal(data.groups.reduce((a,g)=>a+g.yes+g.no,0),12,'Dataset count changed');
    assert.ok(data.insight.includes(pure)&&data.gain.includes(score),JSON.stringify(data));
  }
  await page.select('[data-discovery-choice]','wind');
  await page.click('[data-discovery-check]');
  assert.ok((await page.$eval('[data-discovery-feedback]',e=>e.textContent)).includes('Try Sky'));
  await page.select('[data-discovery-choice]','sky');
  await page.click('[data-discovery-check]');
  assert.ok((await page.$eval('[data-discovery-feedback]',e=>e.textContent)).includes('Correct'));
  console.log('ID3 12 OBSERVATIONS + REASONING CHALLENGE PASS');
  await page.goto(BASE+'/w3/course/',{waitUntil:'networkidle0'});
  assert.equal(await page.$eval('[data-kmeans-step-label]',e=>e.textContent),'Step 1 / 4');
  await page.click('[data-guess-centre="2"]');
  assert.ok((await page.$eval('[data-guess-feedback]',e=>e.textContent)).includes('centre 1'));
  await page.click('[data-guess-centre="1"]');
  assert.ok((await page.$eval('[data-guess-feedback]',e=>e.textContent)).includes('Correct'));
  for(let i=0;i<2;i++)await page.click('[data-kmeans-next]');
  await page.waitForFunction(()=>document.querySelector('[data-improved-number]')?.textContent==='3.17',{timeout:4000});
  let score=await page.evaluate(()=>({
    val:document.querySelector('[data-improved-number]').textContent,
    width:document.querySelector('[data-improved-meter]').style.width,
    markers:document.querySelectorAll('[data-centre-motion] circle').length,
    progress:[...document.querySelectorAll('.discovery-stepper li')].map(e=>e.classList.contains('is-current'))
  }));
  assert.deepEqual(score,{val:'3.17',width:'45.2%',markers:2,progress:[false,false,true,false]});
  await page.click('[data-kmeans-next]');
  assert.ok((await page.$eval('[data-cost-explain]',e=>e.textContent)).includes('55%'));
  await page.click('[data-kmeans-reset]');
  assert.equal(await page.$eval('[data-improved-number]',e=>e.textContent),'—');
  assert.equal(await page.$eval('[data-kmeans-step-label]',e=>e.textContent),'Step 1 / 4');
  console.log('K-MEANS VISIBLE MOVEMENT + COST COMPARISON PASS');
  assert.deepEqual(errors,[],'Browser JS errors '+errors.join(' | '));
  console.log('ALL VISUAL DISCOVERY TESTS PASSED');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
