const p=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const base='http://127.0.0.1:8877',assert=(ok,msg)=>{if(!ok)throw Error(msg)};
(async()=>{
 const browser=await p.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const page=await browser.newPage();let errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const waits=['domcontentloaded','networkidle0'];
 if(!process.env.MLC_SKIP_LAYOUT){
 for(const width of [390,820,1280]){
  await page.setViewport({width,height:930});
  for(let w=4;w<=7;w++){
   for(const kind of ['course','lab','homework','advanced']){
    let res=await page.goto(base+'/w'+w+'/'+kind+'/',{waitUntil:'networkidle0',timeout:20000});
    const data=await page.evaluate(()=>({
     sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
     course:document.querySelectorAll('.chapter-section').length,
     toc:document.querySelectorAll('.course-sidebar .toc-panel a').length,
     teacher:!!document.querySelector('.teacher-guide'),
     problems:document.querySelectorAll('.advanced-problems article').length,
     form:!!document.querySelector('.submission-form'),
     signature:!!document.querySelector('.week47-academic')
    }));
    assert([200,304].includes(res.status()),'Response '+w+' '+kind+' '+res.status());
    assert(data.sw<=data.cw+4,'Overflow '+w+' '+kind+' '+width+' '+JSON.stringify(data));
    assert(data.signature,'Missing reviewed page signature '+w+' '+kind);
    if(kind==='course')assert(data.course>=5&&data.toc>=6&&data.teacher,'Incomplete Course '+w+' '+JSON.stringify(data));
    if(kind==='lab')assert(data.toc>=6&&data.form,'Incomplete laboratory '+w+' '+JSON.stringify(data));
    if(kind==='advanced')assert(data.problems===5,'Missing worked Advanced problems '+w);
    if(kind==='homework')assert((await page.$eval('main',n=>n.textContent)).includes('Mandatory (1p)'), 'Missing homework requirements '+w);
    if(width===390&&kind==='course')await page.screenshot({path:'/tmp/mlclub-w'+w+'-course-mobile.png'});
    if(width===1280&&kind==='lab')await page.screenshot({path:'/tmp/mlclub-w'+w+'-lab-desktop.png'});
   }
   console.log('Responsive pages PASS, Week '+w+', width '+width);
  }
 }
 }
 await page.setViewport({width:1280,height:930});
 await page.goto(base+'/w4/course/',{waitUntil:'networkidle0'});
 assert((await page.$eval('[data-revision-results]',el=>el.textContent)).includes('prediction: A'),'Initial KNN prediction wrong');
 await page.$eval('[data-qx]',el=>{el.value='5';el.dispatchEvent(new Event('input',{bubbles:true}))});
 await page.$eval('[data-qy]',el=>{el.value='5';el.dispatchEvent(new Event('input',{bubbles:true}))});
 assert((await page.$eval('[data-revision-results]',el=>el.textContent)).includes('prediction: B'),'Movable KNN query wrong');
 assert((await page.$eval('[data-confusion-output]',el=>el.textContent)).includes('66.7%'),'Confusion initial wrong');
 await page.$eval('[data-fp]',el=>{el.value='2';el.dispatchEvent(new Event('input',{bubbles:true}))});
 assert((await page.$eval('[data-confusion-output]',el=>el.textContent)).includes('50%'),'Confusion transition wrong');
 console.log('W4 interactive KNN and confusion metrics PASS');
 await page.goto(base+'/w5/course/',{waitUntil:'networkidle0'});
 const count=await page.$$eval('[data-pixel-grid] button',els=>els.length);assert(count===25,'Wrong number of pixel buttons: '+count);
 const rgb=await page.$eval('[data-rgb-output]',el=>el.textContent);assert(rgb.includes('171.58'),'Weighted grayscale incorrect '+rgb);
 await page.click('[data-pixel-mode=threshold]');
 await page.$eval('[data-pixel-threshold]',el=>{el.value='200';el.dispatchEvent(new Event('input',{bubbles:true}))});
 let out=await page.$eval('[data-pixel-narrative]',el=>el.textContent);assert(out.includes('10 of 25'), 'Pixel threshold count wrong: '+out);
 await page.$eval('[data-pixel-threshold]',el=>{el.value='128';el.dispatchEvent(new Event('input',{bubbles:true}))});
 out=await page.$eval('[data-pixel-narrative]',el=>el.textContent);assert(out.includes('8 of 25'),'Pixel reset threshold count wrong '+out);
 await page.click('[data-pixel-grid] button:first-child');assert((await page.$eval('[data-pixel-grid] button:first-child',el=>el.title)).includes('original 255'),'Clickable pixels not reacting');
 console.log('W5 pixel matrix, threshold and RGB PASS');
 await page.goto(base+'/w6/course/',{waitUntil:'networkidle0'});
 out=await page.$eval('[data-perceptron-summary]',el=>el.textContent);assert(out.includes('0 / 4'),'AND weights should have zero errors '+out);
 await page.$eval('[data-weight=b]',el=>{el.value='-0.5';el.dispatchEvent(new Event('input',{bubbles:true}))});
 out=await page.$eval('[data-perceptron-summary]',el=>el.textContent);assert(out.includes('2 / 4'),'OR weights should make 2 AND errors '+out);
 await page.click('[data-perceptron-reset]');
 assert((await page.$eval('[data-perceptron-summary]',el=>el.textContent)).includes('0 / 4'),'Reset failed');
 await page.click('[data-train-epoch]');assert((await page.$eval('[data-train-output]',el=>el.textContent)).includes('#4 input'),'Epoch step failed');
 console.log('W6 boundary, update, full epoch PASS');
 await page.goto(base+'/w7/course/',{waitUntil:'networkidle0'});
 await page.select('[data-xor-x1]','1');
 let xor=await page.$eval('[data-xor-explain]',el=>el.textContent);
 assert(xor.includes('output: 0.5 → 1')&&xor.includes('Expected XOR=1'),'XOR 1,0 failed '+xor);
 await page.select('[data-xor-x2]','1');
 xor=await page.$eval('[data-xor-explain]',el=>el.textContent);
 assert(xor.includes('output: -1.5 → 0')&&xor.includes('Expected XOR=0'),'XOR 1,1 failed '+xor);
 for(let i=0;i<3;i++)await page.click('[data-gradient-next]');
 let grad=await page.$eval('[data-gradient-output]',el=>el.textContent);
 assert(grad.includes('0.05')&&grad.includes('0.118829'),'Gradient numerical update wrong '+grad);
 console.log('W7 XOR diagram and sigmoid gradient PASS');
 for(let w=4;w<=7;w++){
  await page.goto(base+'/w'+w+'/lab/',{waitUntil:'networkidle0'});
  const links=await page.$$eval('a[href*="/jupyter/lab/index.html?path="]',nodes=>nodes.map(n=>n.getAttribute('href')));
  assert(links.length===2,'Missing prepared notebooks week '+w+' '+links);
  console.log('W'+w+' notebook links OK');
 }
 // Verify 4 draft quiz banks render through the existing quiz client.
 for(let w=4;w<=7;w++){
  await page.goto(base+'/w'+w+'/quiz/',{waitUntil:'networkidle0'});
  await page.waitForFunction(w=>document.querySelector('#weekly-quiz')?.textContent.includes('Start Week '+w+' quiz'),{timeout:15000},w);
  await page.click('.quiz-start-button');
  assert((await page.$eval('#weekly-quiz',el=>el.textContent)).includes('Question 1 / 10'),'Quiz did not start W'+w);
  console.log('W'+w+' quiz UI PASS');
 }
 assert(!errors.length,'Uncaught JS exceptions: '+errors.join(' | '));
 console.log('ALL WEEK 4-7 BROWSER INTERACTIONS PASS');
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exit(1)});
