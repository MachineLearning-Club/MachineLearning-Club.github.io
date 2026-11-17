/* Week 4: selected neighbours and confusion matrix are evidence, not confidence. */
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
   await page.setViewport({width,height:860});
   await page.goto(BASE+'/w4/course/',{waitUntil:'networkidle0'});
   const info=await page.evaluate(()=>({
    vote:!!document.querySelector('[data-knn-vote-panel]'),
    confusion:!!document.querySelector('[data-confusion-evaluation-panel]'),
    neighbourCount:document.querySelectorAll('.rev-neighbour').length,
    precision:document.querySelector('[data-rev-precision]')?.textContent,
    recall:document.querySelector('[data-rev-recall]')?.textContent,
    overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
    old:!!document.querySelector('[data-revision-knn] svg'),
    originalMetrics:!!document.querySelector('[data-confusion-output]')
   }));
   assert.ok(info.vote&&info.confusion&&info.old&&info.originalMetrics,JSON.stringify(info));
   assert.equal(info.neighbourCount,3);
   assert.equal(info.precision,'2/3 = 66.7%');
   assert.equal(info.recall,'2/3 = 66.7%');
   assert.ok(info.overflow<=5,'Overflow '+width+': '+JSON.stringify(info));
   console.log('W4 PROBABILITY RESPONSIVE PASS',width);
  }
  await page.setViewport({width:1280,height:900});
  await page.goto(BASE+'/w4/course/',{waitUntil:'networkidle0'});
  const readVotes=()=>page.evaluate(()=>({
   evidence:JSON.parse(document.querySelector('[data-revision-knn]').dataset.knnEvidence),
   count:document.querySelector('[data-rev-vote-result]').textContent,
   fraction:document.querySelector('[data-rev-vote-fraction]').textContent,
   tiles:document.querySelectorAll('.rev-neighbour').length,
   explain:document.querySelector('[data-rev-vote-explain]').textContent
  }));
  let vote=await readVotes();
  assert.equal(vote.evidence.prediction,'A');
  assert.deepEqual(vote.evidence.votes,{A:3,B:0});
  assert.equal(vote.tiles,3);
  assert.ok(vote.fraction.includes('3/3 votes for A'));
  assert.ok(vote.explain.includes('not a 100% guarantee'));
  await page.select('[data-revision-k]','5');
  vote=await readVotes();
  assert.equal(vote.tiles,5);
  assert.deepEqual(vote.evidence.votes,{A:3,B:2});
  assert.ok(vote.fraction.includes('3/5')&&vote.fraction.includes('60%'));
  await page.$eval('[data-qx]',el=>{el.value='5';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.$eval('[data-qy]',el=>{el.value='5';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.select('[data-revision-k]','3');
  vote=await readVotes();
  assert.equal(vote.evidence.prediction,'B');
  assert.deepEqual(vote.evidence.votes,{A:0,B:3});
  assert.ok(vote.fraction.includes('3/3 votes for B'));
  console.log('KNN VOTE COUNTS AND UNCALIBRATED SHARE PASS');
  const readConfusion=()=>page.evaluate(()=>({
   evidence:JSON.parse(document.querySelector('[data-confusion-demo]').dataset.confusionEvidence),
   tp:document.querySelector('[data-rev-tp]').textContent,
   tn:document.querySelector('[data-rev-tn]').textContent,
   fp:document.querySelector('[data-rev-fp]').textContent,
   fn:document.querySelector('[data-rev-fn]').textContent,
   precision:document.querySelector('[data-rev-precision]').textContent,
   recall:document.querySelector('[data-rev-recall]').textContent,
   explanation:document.querySelector('[data-rev-precision-note]').textContent
  }));
  let stats=await readConfusion();
  assert.deepEqual(stats.evidence,{tp:2,tn:2,fp:1,fn:1,total:6});
  assert.deepEqual([stats.tp,stats.tn,stats.fp,stats.fn],['2','2','1','1']);
  await page.$eval('[data-fp]',el=>{el.value=3;el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.$eval('[data-fn]',el=>{el.value=0;el.dispatchEvent(new Event('input',{bubbles:true}));});
  stats=await readConfusion();
  assert.equal(stats.precision,'3/6 = 50.0%');
  assert.equal(stats.recall,'3/3 = 100.0%');
  await page.$eval('[data-fp]',el=>{el.value=0;el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.$eval('[data-fn]',el=>{el.value=3;el.dispatchEvent(new Event('input',{bubbles:true}));});
  stats=await readConfusion();
  assert.equal(stats.precision,'Undefined — no YES predictions');
  assert.equal(stats.recall,'0/3 = 0.0%');
  assert.ok(stats.explanation.includes('cannot be computed'));
  assert.deepEqual(errors,[],'Page errors '+errors.join(' | '));
  console.log('DIRECTIONAL CONDITIONAL METRICS + ZERO DENOMINATOR PASS');
  console.log('ALL WEEK 4 PROBABILITY EVIDENCE TESTS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
