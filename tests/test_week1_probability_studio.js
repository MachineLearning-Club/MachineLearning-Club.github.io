/* Verify Week 1 probability narrative, calculations and new interactive tools. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const BASE='http://127.0.0.1:8877/w1/course/';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,
   args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),issues=[];
  page.on('pageerror',e=>issues.push(e.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:840});
   const response=await page.goto(BASE,{waitUntil:'networkidle0',timeout:20000});
   assert.ok([200,304].includes(response.status()));
   const summary=await page.evaluate(()=>({
      present:!!document.querySelector('[data-bayes-studio]')&&
        !!document.querySelector('[data-uncertainty-studio]')&&
        !!document.querySelector('[data-die-frequency]'),
      tiles:document.querySelectorAll('.bayes-person').length,
      vertical:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      core:!!document.querySelector('.lesson-prob-route'),
      originalBayes:!!document.querySelector('.bayes-proof'),
      originalMethods:document.querySelectorAll('[data-model-interactive]').length,
      math:!!document.querySelector('.academic-math'),
      unchangedDice:!!document.querySelector('[data-d10-cells]'),
      sticky:getComputedStyle(document.querySelector('.lesson-header')).position
    }));
   assert.ok(summary.present&&summary.core&&summary.originalBayes&&summary.math&&summary.unchangedDice);
   assert.equal(summary.originalMethods,9);
   assert.equal(summary.tiles,100);
   assert.equal(summary.sticky,'sticky');
   assert.ok(summary.vertical<=5,'Horizontal overflow '+width+': '+summary.vertical);
   console.log('W1 RESPONSIVE + CONTENT PASS',width,'px');
  }
  await page.setViewport({width:1280,height:920});
  await page.goto(BASE,{waitUntil:'networkidle0'});
  async function state(){
   return await page.evaluate(()=>({
    classes:Object.fromEntries(['known','lucky','wrong'].map(c=>[c,document.querySelectorAll('.bayes-person.is-'+c).length])),
    posterior:document.querySelector('[data-bayes-posterior]').textContent,
    total:document.querySelector('[data-bayes-correct-count]').textContent,
    formula:document.querySelector('[data-bayes-calculation]').textContent,
    reason:document.querySelector('[data-bayes-reasoning]').textContent,
    filtered:document.querySelectorAll('.bayes-person.is-filtered').length
   }));
  }
  assert.deepEqual((await state()).classes,{known:60,lucky:20,wrong:20});
  assert.equal((await state()).posterior,'75%');
  await page.click('[data-bayes-keep]');
  assert.equal((await state()).filtered,20);
  await page.$eval('[data-bayes-prior]',el=>{el.value='40';el.dispatchEvent(new Event('input',{bubbles:true}));});
  let result=await state();
  assert.deepEqual(result.classes,{known:40,lucky:30,wrong:30});
  assert.equal(result.total,'70');
  assert.equal(result.posterior,'57.1%');
  assert.ok(result.formula.includes('40 / (40 + 30)'));
  assert.ok(result.reason.includes('P(correct | knew)'));
  await page.$eval('[data-bayes-prior]',el=>{el.value='0';el.dispatchEvent(new Event('input',{bubbles:true}));});
  result=await state();
  assert.equal(result.posterior,'0%');
  await page.$eval('[data-bayes-prior]',el=>{el.value='100';el.dispatchEvent(new Event('input',{bubbles:true}));});
  result=await state();
  assert.equal(result.posterior,'100%');
  await page.select('[data-bayes-choice]','reverse');
  await page.click('[data-bayes-check]');
  assert.ok((await page.$eval('[data-bayes-feedback]',e=>e.textContent)).includes('Check the order'));
  await page.select('[data-bayes-choice]','conditional');
  await page.click('[data-bayes-check]');
  assert.ok((await page.$eval('[data-bayes-feedback]',e=>e.textContent)).includes('Correct'));
  console.log('BAYES 0%,40%,60%,100% + CONDITIONAL REASONING PASS');
  await page.click('[data-die-type="tricky"]');
  assert.equal(await page.$eval('[data-die-mean]',e=>e.textContent),'5.50');
  await page.click('[data-roll-30]');
  const frequencies=await page.evaluate(()=>{
    const cols=[...document.querySelectorAll('.die-frequency-col')];
    return {visible:!document.querySelector('[data-die-frequency]').hidden,
      bars:cols.length,
      counted:cols.reduce((total,col)=>total+Number(col.querySelector('strong')?.textContent),0),
      expected:cols.map(col=>col.querySelector('.die-frequency-expected').style.bottom),
      note:document.querySelector('[data-die-frequency-note]').textContent};
  });
  assert.equal(frequencies.visible,true);
  assert.equal(frequencies.bars,10);
  assert.equal(frequencies.counted,30);
  assert.equal(frequencies.expected[0],frequencies.expected[9]);
  assert.ok(frequencies.note.includes('tricky distribution'));
  // Scroll to the centre before a pointer click: the sticky two-row header
  // otherwise overlaps controls near the top of Puppeteer's click viewport.
  await page.$eval('[data-die-type="loaded"]',el=>el.scrollIntoView({block:'center',behavior:'instant'}));
  await page.click('[data-die-type="loaded"]');
  assert.equal(await page.$eval('[data-die-frequency]',e=>e.hidden),true);
  await page.click('[data-roll-30]');
  const more=await page.evaluate(()=>[...document.querySelectorAll('.die-frequency-col')].map(el=>Number(el.querySelector('strong').textContent)));
  assert.equal(more.reduce((a,b)=>a+b,0),30);
  console.log('DIE SAMPLE 30 FREQUENCIES + PMF STATE RESET PASS');
  const expected={
   pure:{yes:12,no:0,degree:'No label uncertainty',entropy:0},
   skewed:{yes:10,no:2,degree:'Some label uncertainty',entropy:0.65},
   balanced:{yes:6,no:6,degree:'Maximum binary-label uncertainty',entropy:1}
  };
  for(const [name,check] of Object.entries(expected)){
   await page.click('[data-uncertainty-kind="'+name+'"]');
   const got=await page.evaluate(()=>({
    yes:document.querySelectorAll('.uncertainty-case.is-yes').length,
    no:document.querySelectorAll('.uncertainty-case.is-no').length,
    degree:document.querySelector('[data-uncertainty-degree]').textContent,
    entropy:document.querySelector('[data-uncertainty-math]').textContent
   }));
   assert.equal(got.yes,check.yes);
   assert.equal(got.no,check.no);
   assert.equal(got.degree,check.degree);
   assert.ok(got.entropy.includes(check.entropy.toFixed(3)+' bits'));
  }
  console.log('UNCERTAINTY 0,0.650,1 BIT + WEEK 2 TRANSFER PASS');
  assert.deepEqual(issues,[],'Page errors: '+issues.join(' / '));
  console.log('ALL WEEK 1 PROBABILITY STUDIO TESTS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
