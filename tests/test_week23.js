const p=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const base='http://127.0.0.1:8877';
(async()=>{
 const b=await p.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const page=await b.newPage();const failures=[];page.on('pageerror',error=>failures.push(error.message));
 for(const width of [390,820,1280]){
  await page.setViewport({width,height:950});
  for(const week of [2,3]){
   for(const kind of ['course','lab','homework','advanced']){
    const response=await page.goto(base+'/w'+week+'/'+kind+'/',{waitUntil:'networkidle0'});
    const meta=await page.evaluate(()=>({
     width:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth,
     courses:document.querySelectorAll('.chapter-section').length,teacher:!!document.querySelector('.teacher-guide'),
     toc:document.querySelectorAll('.course-sidebar .toc-panel a').length,
     examples:document.querySelectorAll('.advanced-problems article').length,
     bibliography:!!document.querySelector('.page-bibliography'),
     week23:!!document.querySelector('.week23-academic')}));
    if(![200,304].includes(response.status())||meta.width>meta.viewport+4||!meta.bibliography||!meta.week23||
       (kind==='course'&&(meta.courses<6||!meta.teacher||meta.toc<7))||
       (kind==='lab'&&meta.toc<7)||(kind==='advanced'&&meta.examples<5)){
      throw Error('PAGE '+week+' '+kind+' '+width+' '+JSON.stringify(meta));}
    if(width===390&&kind==='course'&&(await page.$eval('.course-sidebar .toc-panel',el=>el.open)))throw Error('mobile TOC open');
    if(width===1280&&kind==='lab'&&!(await page.$eval('.course-sidebar .toc-panel',el=>el.open)))throw Error('desktop TOC closed');
    if(width===390&&kind==='course')await page.screenshot({path:'/tmp/mlclub-w'+week+'-course-mobile.png'});
    if(width===1280&&kind==='lab')await page.screenshot({path:'/tmp/mlclub-w'+week+'-lab-desktop.png'});
   }
   console.log('Responsive 4 pages: Week '+week+', width '+width+' PASS');
  }
 }
 await page.goto(base+'/w2/course/',{waitUntil:'networkidle0'});
 async function gain(button){await page.click('[data-id3-feature='+button+']');return await page.$eval('[data-id3-gain]',x=>x.textContent);}
 const sky=await gain('sky'),wind=await gain('wind'),temp=await gain('temperature');
 console.log('ID3 gains:',sky,wind,temp);
 if(!sky.includes('0.667')||!wind.includes('0.082')||!temp.includes('Information gain: 0 bits'))throw Error('ID3 gains wrong');
 await page.click('[data-id3-next]');await page.click('[data-id3-next]');await page.click('[data-id3-next]');
 const step=await page.$eval('[data-id3-step-label]',x=>x.textContent);
 if(step!=='Step 4 / 4')throw Error('ID3 progressive tree not working');
 console.log('ID3 progressive diagram PASS');
 await page.goto(base+'/w3/course/',{waitUntil:'networkidle0'});
 await page.click('[data-kmeans-next]');await page.click('[data-kmeans-next]');
 const result=await page.$eval('[data-kmeans-explain]',x=>x.textContent);
 if(!result.includes('19/6')||!result.includes('0,1/3'))throw Error('Kmeans update step incorrect: '+result);
 const groupNames=await page.$$eval('[data-kmeans-distance-rows] tr',rows=>rows.map(tr=>tr.cells[3].textContent));
 if(groupNames.join(',')!=='Cluster 1,Cluster 1,Cluster 1,Cluster 2,Cluster 2')throw Error('Grouping wrong: '+groupNames);
 await page.click('[data-kmeans-next]');
 const convergence=await page.$eval('[data-kmeans-explain]',x=>x.textContent);
 if(!convergence.includes('converged'))throw Error('Kmeans convergence step missing');
 console.log('K-means graph and distance table PASS');
 for(const w of [2,3]){
  await page.goto(base+'/w'+w+'/lab/',{waitUntil:'networkidle0'});
  const links=await page.$$eval('a[href*="/jupyter/lab/index.html?path="]',els=>els.map(el=>el.getAttribute('href')));
  if(links.length!==2)throw Error('Need 2 ready notebooks in W'+w+' not '+links.length);
  console.log('Week '+w+' prepared notebook launch links',links.join(' and '));
  await page.click('.python-runner .run-python');
  const expected=w===2?'information gain':'Cluster';
  await page.waitForFunction(value=>document.querySelector('.python-runner .py-output')?.textContent.includes(value),{timeout:55000},expected);
  const output=await page.$eval('.python-runner .py-output',el=>el.textContent);
  console.log('Week '+w+' inline Python output:',output.slice(0,110).replace(/\n/g,' | '));
 }
 if(failures.length)throw Error('JS errors '+failures.join(' | '));
 console.log('ALL WEEK 2/3 BROWSER TESTS PASSED');
 }finally{await b.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});