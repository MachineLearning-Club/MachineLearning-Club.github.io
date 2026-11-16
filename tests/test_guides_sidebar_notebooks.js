const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const base='http://127.0.0.1:8877';
const check=(v,m)=>{if(!v)throw Error(m)};
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,820,1280]){
   await page.setViewport({width,height:930});
   for(const key of ['python','notebooks']){
    const r=await page.goto(base+'/guides/'+key+'/',{waitUntil:'networkidle0',timeout:25000});
    check([200,304].includes(r.status()),'HTTP status '+key);
    if(key==='notebooks'){
      await page.evaluate(()=>document.querySelectorAll('.guide-shot img').forEach(im=>im.loading='eager'));
      await page.waitForFunction(()=>[...document.querySelectorAll('.guide-shot img')].every(im=>im.complete&&im.naturalWidth>0),{timeout:12000});
    }
    const state=await page.evaluate(()=>({
      sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,
      footer:document.querySelectorAll('.mlclub-footer').length,
      side:!!document.querySelector('.foundations-toc,.github-guide-sidebar'),
      toc:document.querySelectorAll('.foundations-toc a,.github-guide-sidebar a').length,
      imgs:document.querySelectorAll('.guide-shot img').length,
      allImages:[...document.querySelectorAll('.guide-shot img')].every(im=>im.naturalWidth>0),
      chapters:document.querySelectorAll('.foundations-group,.github-guide-step').length,
      layout:document.querySelector('.foundations-layout,.github-guide-layout')?getComputedStyle(document.querySelector('.foundations-layout,.github-guide-layout')).display:null,
      positions:document.querySelector('.foundations-toc,.github-guide-sidebar')?.getBoundingClientRect().toJSON()
    }));
    check(state.sw<=state.cw+4,'Overflow '+key+' width '+width+' '+JSON.stringify(state));
    check(state.footer===1&&state.side,'Missing shared footer/sidebar '+key);
    if(key==='notebooks')check(state.imgs===7&&state.allImages&&state.toc>=10&&state.chapters>=10,'Notebook tutorial '+JSON.stringify(state));
    if(key==='python')check(state.toc===21&&state.chapters>=3,'Python content/navigation '+JSON.stringify(state));
    if(width===390)await page.screenshot({path:'/tmp/mlc-'+key+'-mobile.png'});
    if(width===1280)await page.screenshot({path:'/tmp/mlc-'+key+'-desktop.png'});
    console.log('PAGE PASS',key,width,'navigation',state.toc,'screenshots',state.imgs,'layout',state.layout);
   }
  }
  await page.setViewport({width:1280,height:930});
  await page.goto(base+'/guides/python/',{waitUntil:'networkidle0'});
  await page.click('.foundations-toc a[href="#topic-18"]');
  const state=await page.evaluate(()=>({
    hash:location.hash,open:document.getElementById('topic-18').open,
    current:document.querySelector('.foundations-toc a[aria-current=location]')?.getAttribute('href')
  }));
  check(state.open&&state.current==='#topic-18','Python sidebar does not open corresponding lesson '+JSON.stringify(state));
  console.log('PYTHON ANCHOR OPENS THE MATCHING EXERCISE');
  await page.setViewport({width:390,height:930});
  await page.goto(base+'/guides/python/',{waitUntil:'networkidle0'});
  const collapsed=await page.$eval('.foundations-toc-details',e=>e.open);
  check(!collapsed,'Mobile contents should be collapsed initially');
  await page.click('.foundations-toc-details>summary');
  await page.click('.foundations-toc a[href="#topic-12"]');
  check(await page.$eval('#topic-12',e=>e.open),'Mobile anchor did not open exercise');
  console.log('MOBILE COLLAPSIBLE PYTHON CONTENTS PASS');
  await page.goto(base+'/guides/notebooks/',{waitUntil:'networkidle0'});
  const links=await page.$$eval('.github-guide-sidebar a',anchors=>anchors.map(a=>({href:a.hash,exists:!!document.querySelector(a.hash)})));
  check(links.every(link=>link.exists),'Broken notebook heading anchors '+JSON.stringify(links));
  check(!errors.length,'Browser JS errors '+errors.join('|'));
  console.log('ALL GUIDES AND ANNOTATIONS PASS');
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exit(1)});
