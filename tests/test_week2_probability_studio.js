/* Probability-first ID3 studio is calculated from the twelve displayed records. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const BASE='http://127.0.0.1:8877';
(async()=>{
const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,
 args:['--no-sandbox','--disable-dev-shm-usage']});
try{
const page=await browser.newPage(),errors=[];
page.on('pageerror',err=>errors.push(err.message));
for(const width of [390,820,1280]){
 await page.setViewport({width,height:900});
 const response=await page.goto(BASE+'/w2/course/',{waitUntil:'networkidle0'});
 assert.ok([200,304].includes(response.status()));
 const state=await page.evaluate(()=>{
  const root=document.querySelector('[data-id3-probability]');
  return {
   root:!!root,
   rows:document.querySelectorAll('#w2-data tbody tr').length,
   cases:root?.querySelectorAll('.id3-prob-tile').length,
   branches:root?.querySelectorAll('[data-id3-prob-branches] .id3-prob-branch').length,
   gain:root?.querySelector('[data-id3-prob-gain]').textContent,
   tempBroken:document.documentElement.scrollWidth-document.documentElement.clientWidth,
   math:!!root?.querySelector('[data-id3-prob-formula]'),
   toc:!!document.querySelector('.toc-panel a[href="#id3-probability"]'),
   original:!!document.querySelector('[data-id3-playground] .id3-controls')
  };
 });
 assert.ok(state.root&&state.math&&state.toc&&state.original,JSON.stringify(state));
 assert.equal(state.rows,12);
 assert.equal(state.cases,12);
 assert.equal(state.branches,3);
 assert.ok(state.gain.includes('0.667'));
 assert.ok(state.tempBroken<=5,'Horizontal overflow '+width+': '+JSON.stringify(state));
 console.log('RESPONSIVE ID3 PROBABILITY STUDIO PASS',width);
}
await page.setViewport({width:1280,height:900});
await page.goto(BASE+'/w2/course/',{waitUntil:'networkidle0'});
const num=await page.evaluate(()=>{
 const p=window.MLClubID3Probability;
 return {count:p.rows.length,root:p.entropy(p.rows),
  sky:p.rootGains.sky,wind:p.rootGains.wind,temperature:p.rootGains.temperature,
  cloudy:p.rows.filter(r=>r.sky==='cloudy').length,
  cloudyWind:p.gain(p.rows.filter(r=>r.sky==='cloudy'),'wind'),
  cloudyTemperature:p.gain(p.rows.filter(r=>r.sky==='cloudy'),'temperature')
 };
});
assert.equal(num.count,12);assert.equal(num.root,1);
assert.ok(Math.abs(num.sky-2/3)<1e-10);
assert.ok(Math.abs(num.wind-(1-(-(2/3*Math.log2(2/3)+1/3*Math.log2(1/3)))))<1e-10);
assert.ok(Math.abs(num.temperature)<1e-10);
assert.equal(num.cloudy,4);
assert.equal(num.cloudyWind,1);
assert.equal(num.cloudyTemperature,0);
console.log('DATA-DERIVED EXACT ENTROPIES & GAINS PASS',num);
async function snapshot(){
 return page.evaluate(()=>({
  selected:[...document.querySelectorAll('[data-id3-prob-feature]')].filter(b=>b.getAttribute('aria-pressed')==='true').map(b=>b.dataset.id3ProbFeature),
  branchNames:[...document.querySelectorAll('[data-id3-prob-branches] .id3-prob-branch-head strong')].map(e=>e.textContent),
  before:document.querySelector('[data-id3-prob-before]').textContent,
  after:document.querySelector('[data-id3-prob-after]').textContent,
  gain:document.querySelector('[data-id3-prob-gain]').textContent,
  gauge:[...document.querySelectorAll('.id3-prob-gauge>span')].map(e=>parseFloat(e.style.width)),
  original:document.querySelector('[data-id3-feature][aria-pressed=true]').dataset.id3Feature,
  rank:[...document.querySelectorAll('.id3-prob-rank')].map(e=>e.textContent.trim())
 }));
}
const sky=await snapshot();
assert.deepEqual(sky.selected,['sky']);assert.equal(sky.original,'sky');
assert.deepEqual(sky.branchNames,['sky = sunny','sky = cloudy','sky = rainy']);
assert.ok(sky.after.includes('0.333')&&sky.gain.includes('0.667'));
assert.ok(Math.abs(sky.gauge[0]-33.333)<.003&&Math.abs(sky.gauge[1]-66.667)<.003);
assert.ok(sky.rank[0].includes('Sky')&&sky.rank[1].includes('Wind')&&sky.rank[2].includes('Temperature'));
await page.click('[data-id3-prob-feature="wind"]');
let val=await snapshot();
assert.equal(val.original,'wind');
assert.ok(val.after.includes('0.918')&&val.gain.includes('0.082'),JSON.stringify(val));
assert.equal(val.branchNames.length,2);
await page.click('[data-id3-feature="temperature"]');
val=await snapshot();
assert.equal(val.original,'temperature');
assert.deepEqual(val.selected,['temperature']);
assert.ok(val.after.includes('1.000')&&val.gain.includes('0.000'),JSON.stringify(val));
await page.click('[data-id3-prob-select="sky"]');
val=await snapshot();
assert.equal(val.original,'sky');assert.ok(val.after.includes('0.333'));
const local=async()=>page.evaluate(()=>({
 score:document.querySelector('.id3-prob-local-score').textContent,
 groups:[...document.querySelectorAll('.id3-prob-local-grid .id3-prob-branch-head strong')].map(e=>e.textContent),
 selected:[...document.querySelectorAll('[data-id3-prob-cloudy]')].find(b=>b.getAttribute('aria-pressed')==='true').dataset.id3ProbCloudy
}));
let l=await local();assert.equal(l.selected,'wind');
assert.ok(l.score.includes('Gain = 1.000 bits'));
assert.deepEqual(l.groups,['wind = calm','wind = windy']);
await page.click('[data-id3-prob-cloudy="temperature"]');
l=await local();assert.equal(l.selected,'temperature');
assert.ok(l.score.includes('H(after) = 1.000 bits')&&l.score.includes('Gain = 0.000 bits'));
assert.deepEqual(l.groups,['temperature = warm','temperature = cold']);
await page.click('[data-id3-prob-cloudy="wind"]');
assert.ok((await local()).score.includes('Gain = 1.000 bits'));
const caution=await page.$eval('.id3-prob-caveat',e=>e.textContent);
assert.ok(caution.includes('not proof')&&caution.includes('training dataset'));
console.log('BUTTON SYNC, WEIGHTED VISUALS, AND CONDITIONAL GAIN PASS');
assert.deepEqual(errors,[],'Browser errors: '+errors.join(' | '));
console.log('ALL WEEK 2 PROBABILITY STUDIO TESTS PASS');
}finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
