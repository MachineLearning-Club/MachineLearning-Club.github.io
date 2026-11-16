const p=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const assert=(b,m)=>{if(!b)throw new Error(m)};
(async()=>{
const browser=await p.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const width of [390,768,1280]){
  await page.setViewport({width,height:850,deviceScaleFactor:1});
  const res=await page.goto('http://127.0.0.1:8877/guides/github-ai/',{waitUntil:'networkidle0',timeout:25000});
  assert([200,304].includes(res.status()),'HTTP '+res.status());
  await page.evaluate(()=>document.querySelectorAll('.guide-shot img').forEach(im=>im.loading='eager'));
  await page.waitForFunction(()=>[...document.querySelectorAll('.guide-shot img')].every(im=>im.complete&&im.naturalWidth>0),{timeout:13000});
  const data=await page.evaluate(()=>({
   w:document.documentElement.scrollWidth,vw:document.documentElement.clientWidth,
   images:[...document.querySelectorAll('.guide-shot img')].map(im=>({src:im.getAttribute('src'),ok:im.complete&&im.naturalWidth>0,alt:im.alt})),
   links:[...document.querySelectorAll('.github-guide-sidebar a')].map(a=>({href:a.hash,found:!!document.querySelector(a.hash)})),
   chapters:[...document.querySelectorAll('.github-guide-step')].map(x=>x.id),
   footers:document.querySelectorAll('footer.site.mlclub-footer').length,
   pageTitle:document.title,
   headings:document.querySelectorAll('h2').length
  }));
  assert(data.w<=data.vw+4,'Horizontal overflow '+width+' '+JSON.stringify(data));
  assert(data.images.length===13,'Expected 13 screenshots, got '+data.images.length);
  assert(data.images.every(x=>x.ok&&x.alt.length>28),'Missing screenshot '+JSON.stringify(data.images.filter(x=>!x.ok)));
  assert(data.links.every(x=>x.found),'Broken guide contents link');
  assert(data.footers===1,'Site footer duplicate');
  assert(data.chapters.length>=11,'Chapters missing');
  console.log('LAYOUT PASS',width,'screenshots',data.images.length,'sections',data.chapters.length);
  if(width===390){await page.screenshot({path:'/tmp/mlclub-guide-mobile-top.png',fullPage:false});
   await page.$eval('#gg-agent',e=>e.scrollIntoView());await page.screenshot({path:'/tmp/mlclub-guide-mobile-agent.png'});
  }
  if(width===1280){await page.screenshot({path:'/tmp/mlclub-guide-desktop-top.png',fullPage:false});
   await page.$eval('#gg-agent',e=>e.scrollIntoView());await page.screenshot({path:'/tmp/mlclub-guide-desktop-agent.png'});
  }
 }
 await page.setViewport({width:1280,height:850});
 await page.goto('http://127.0.0.1:8877/guides/github-ai/',{waitUntil:'networkidle0'});
 await page.$eval('[data-gh-username]',e=>{e.value='mlclubstudent';e.dispatchEvent(new Event('input',{bubbles:true}))});
 let u=await page.$eval('[data-gh-url]',e=>e.textContent);
 assert(u==='https://mlclubstudent.github.io/my-first-ai-site/','Wrong project URL '+u);
 await page.$eval('[data-gh-username]',e=>{e.value='invalid space';e.dispatchEvent(new Event('input',{bubbles:true}))});
 assert((await page.$eval('[data-gh-username]',e=>e.getAttribute('aria-invalid')))==='true','Username validation missing');
 console.log('LIVE URL GENERATOR PASS');
 const starter=await page.goto('http://127.0.0.1:8877/guides/github-ai/starter/',{waitUntil:'networkidle0'});
 assert(starter.status()===200,'Starter HTTP status '+starter.status());
 for(let i=0;i<3;i++)await page.click('[data-price="5"]');
 assert((await page.$eval('#total',e=>e.textContent))==='15','Cart total after 3 clicks wrong');
 await page.click('[data-price="4"]');
 assert((await page.$eval('#total',e=>e.textContent))==='19','Coffee + tea wrong');
 await page.click('#reset');
 assert((await page.$eval('#total',e=>e.textContent))==='0','Reset failed');
 assert(!errors.length,'Browser errors '+errors.join('; '));
 console.log('STARTER INTERACTIVE CART PASS / NO JS EXCEPTIONS');
}finally{await browser.close()}
})().catch(e=>{console.error(e.stack);process.exit(1)});
