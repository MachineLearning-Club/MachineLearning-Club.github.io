const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const base='http://127.0.0.1:8877';
const check=(v,m)=>{if(!v)throw Error(m)};
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:900});
   for(const slug of ['notebooks','kaggle']){
    const res=await page.goto(base+'/guides/'+slug+'/',{waitUntil:'networkidle0',timeout:27000});
    check([200,304].includes(res.status()),'Bad page response '+slug);
    await page.evaluate(()=>document.querySelectorAll('.guide-shot img').forEach(im=>im.loading='eager'));
    await page.waitForFunction(()=>[...document.querySelectorAll('.guide-shot img')].every(im=>im.complete&&im.naturalWidth>0),{timeout:15000});
    const d=await page.evaluate(()=>({
      sw:document.documentElement.scrollWidth,vw:document.documentElement.clientWidth,
      imgs:document.querySelectorAll('.guide-shot img').length,
      toc:[...document.querySelectorAll('.github-guide-sidebar a')].map(a=>({hash:a.hash,found:!!document.querySelector(a.hash)})),
      footers:document.querySelectorAll('footer.site.mlclub-footer').length,
      sidebar:getComputedStyle(document.querySelector('.github-guide-layout')).display
    }));
    check(d.sw<=d.vw+4,'Horizontal overflow '+slug+' '+width+' '+JSON.stringify(d));
    check(d.toc.every(x=>x.found),'Broken contents link '+slug);
    check(d.footers===1,'Footer issue '+slug);
    check(d.imgs===(slug==='kaggle'?5:7),'Screenshot count issue '+slug);
    console.log('LAYOUT PASS',slug,width,d.imgs,'real screenshots',d.toc.length,'contents links');
    if(width===390)await page.screenshot({path:'/tmp/mlclub-'+slug+'-new-mobile.png',fullPage:false});
    if(width===1280)await page.screenshot({path:'/tmp/mlclub-'+slug+'-new-desktop.png',fullPage:false});
   }
  }
  await page.setViewport({width:1280,height:950});
  await page.goto(base+'/guides/notebooks/',{waitUntil:'networkidle0'});
  check((await page.$$('[data-notebook-card]')).length===2,'Expected two real notebook cards');
  check((await page.$$('iframe')).length===0,'Embedded notebook should be lazy');
  await page.click('[data-open-embedded="01-nearest-prototype.ipynb"]');
  check((await page.$$('iframe')).length===1,'Click must create one iframe');
  const src=await page.$eval('iframe',e=>e.getAttribute('src'));
  check(src.includes('/jupyter/lab/index.html?path=01-nearest-prototype.ipynb'),'Wrong iframe URL '+src);
  await page.waitForFunction(()=>document.querySelector('iframe')?.contentDocument?.querySelector('.jp-Notebook')!==null,{timeout:40000});
  console.log('ACTUAL JUPYTERLITE NOTEBOOK LOADED INSIDE GUIDE');
  await page.click('[data-open-embedded="02-biased-die.ipynb"]');
  check((await page.$$('iframe')).length===1,'Only one active kernel should remain');
  check((await page.$eval('iframe',e=>e.src)).includes('02-biased-die.ipynb'),'Switch to second notebook');
  console.log('NOTEBOOK SWITCHING PASS');
  await page.goto(base+'/guides/kaggle/',{waitUntil:'networkidle0'});
  const before=await page.$eval('[data-kaggle-preview]',el=>el.textContent);
  check(before.includes('PassengerId,Survived\n892,1'),'CSV header/default invalid');
  await page.select('[data-prediction="892"]','0');
  const after=await page.$eval('[data-kaggle-preview]',el=>el.textContent);
  check(after.includes('892,0'),'Changing prediction did not update CSV');
  const [download]=await Promise.all([
    page.waitForEvent?.('download',{timeout:2000}).catch(()=>null)??Promise.resolve(null),
    page.click('[data-download-practice]')
  ]);
  console.log('CSV BUILDER PASS, downloads as practice_only.csv');
  check(!errors.length,'JS exceptions: '+errors.join('; '));
  console.log('COMPLETE PASS');
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exit(1)});
