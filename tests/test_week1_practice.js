const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const BASE='http://127.0.0.1:8877';
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage();
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,850,1280]){
   await page.setViewport({width,height:900});
   await page.goto(BASE+'/w1/lab/',{waitUntil:'networkidle0'});
   const info=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth,
     sidebar:!!document.querySelector('.course-sidebar .toc-panel'),
     navCount:document.querySelectorAll('.course-sidebar a[href^="#"]').length,
     transfer:!!document.querySelector('.course-sidebar a[href="#learning-transfer-lab-w1"]'),
     intro:document.body.textContent.includes('Laboratory — explore AI in practice'),
     safe:document.body.textContent.includes('Use safe examples'),
     runner:document.querySelectorAll('.lab-mini-notebook .python-runner').length,
     prompt:!!document.querySelector('[data-coffee-prompt]'),
     links:[...document.querySelectorAll('.lab-lesson a[href^="https://"]')].every(a=>a.target==='_blank')}));
   if(info.width>info.viewport+3||!info.sidebar||info.navCount!==9||!info.transfer||info.intro||info.safe||info.runner!==3||!info.prompt||!info.links)
     throw Error('Lab '+width+' '+JSON.stringify(info));
   if(width===390&&await page.$eval('.toc-panel',x=>x.open))throw Error('Mobile TOC should start collapsed');
   if(width===1280&&!(await page.$eval('.toc-panel',x=>x.open)))throw Error('Desktop TOC should start open');
   await page.screenshot({path:'/tmp/mlclub-week1-lab-'+width+'.png'});
   console.log('Lab responsive '+width+' PASS');
  }
  await page.goto(BASE+'/w1/lab/',{waitUntil:'networkidle0'});
  await page.$eval('[data-theme]',el=>{el.value='starry library';el.dispatchEvent(new Event('input',{bubbles:true}));});
  const text=await page.$eval('[data-prompt-text]',e=>e.textContent);
  if(!text.includes('starry library')||!text.includes('Add to cart')||!text.includes('SIMULATES'))throw Error('Coffee prompt incorrect');
  console.log('AI website prompt PASS');
  for(const width of [390,1280]){
   await page.setViewport({width,height:900});
   await page.goto(BASE+'/w1/homework/',{waitUntil:'networkidle0'});
   const w=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth,
     mandatory:document.body.textContent.includes('8')||document.querySelector('.assignment-table tbody tr')?.length===8,
     formula:document.body.textContent.includes('P(R₂ | R₁) = 2/4'),
     optional:!!document.querySelector('#optional-probability'),
     distribution:document.querySelectorAll('[data-dist-choice]').length}));
   if(w.width>w.viewport+3||!w.formula||!w.optional||w.distribution!==5)throw Error('Homework '+width+' '+JSON.stringify(w));
   const choices=['bernoulli','binomial','uniform','poisson','normal'];
   await page.evaluate(values=>document.querySelectorAll('[data-dist-choice]').forEach((s,i)=>{s.value=values[i];}),choices);
   await page.click('[data-check-distributions]');
   const msg=await page.$eval('[data-distributions-result]',el=>el.textContent);
   if(!msg.includes('5 / 5'))throw Error('Distribution grading failed: '+msg);
   await page.$eval('[data-probability-slider]',el=>{el.value=25;el.dispatchEvent(new Event('input',{bubbles:true}));});
   const result=await page.$eval('[data-expected-result]',el=>el.textContent);
   if(!result.includes('0.25'))throw Error('Probability slider failed: '+result);
   console.log('Homework interactive '+width+' PASS');
  }
  await page.goto(BASE+'/w1/advanced/',{waitUntil:'networkidle0'});
  const labels=await page.$$eval('.advanced-problems article h3',a=>a.map(x=>x.textContent));
  if(labels.length!==9)throw Error('Expected original five + four advanced problems: '+labels.length);
  await page.$eval('[data-variance-slider]',el=>{el.value=25;el.dispatchEvent(new Event('input',{bubbles:true}));});
  const variance=await page.$eval('[data-variance-result]',el=>el.textContent);
  if(!variance.includes('2.50')||!variance.includes('18.75'))throw Error('Variance formula incorrect: '+variance);
  await page.click('[data-cov-mode=negative]');
  const negative=await page.$eval('[data-cov-result]',el=>el.textContent);
  if(!negative.includes('-0.25'))throw Error('Negative covariance wrong '+negative);
  await page.click('[data-cov-mode=zero]');
  const zero=await page.$eval('[data-cov-result]',el=>el.textContent);
  if(!zero.includes('0.00'))throw Error('Zero covariance wrong '+zero);
  await page.click('[data-cov-mode=positive]');
  const positive=await page.$eval('[data-cov-result]',el=>el.textContent);
  if(!positive.includes('0.25'))throw Error('Positive covariance wrong '+positive);
  await page.screenshot({path:'/tmp/mlclub-week1-advanced.png'});
  console.log('Advanced 9 problems + variance + covariance PASS');
  if(errors.length)throw Error('JS errors '+errors.join('; '));
  console.log('ALL WEEK 1 TESTS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});