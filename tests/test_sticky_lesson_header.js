/* The complete two-row lesson navigation stays visible without covering anchors. */
const assert=require('node:assert/strict');
const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const BASE='http://127.0.0.1:8877';
const samplePages=[
 '/w1/course/','/w2/course/','/w3/lab/','/w7/advanced/',
 '/w8/course/','/w10/quiz/','/w12/lab/','/w15/course/'
];
const browserConfig={executablePath:'/usr/bin/chromium',headless:true,
  args:['--no-sandbox','--disable-dev-shm-usage']};
(async()=>{
 const browser=await puppeteer.launch(browserConfig);
 try{
  const page=await browser.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  for(const viewport of [{width:390,height:844},{width:820,height:800},{width:1280,height:840}]){
   await page.setViewport(viewport);
   for(const path of samplePages){
    const response=await page.goto(BASE+path,{waitUntil:'networkidle0',timeout:20000});
    assert.ok([200,304].includes(response.status()),path+' HTTP '+response.status());
    const before=await page.evaluate(()=>{
      const header=document.querySelector('.lesson-header');
      const tabs=header?.querySelector('.lesson-tabs');
      const topbar=header?.querySelector('.lesson-topbar');
      return {
       sticky:getComputedStyle(header).position,
       top:parseFloat(getComputedStyle(header).top),
       headerHeight:header.getBoundingClientRect().height,
       measured:parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--lesson-header-height')),
       scrollPadding:parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop),
       tabs:tabs?.getBoundingClientRect().height,
       topbar:topbar?.getBoundingClientRect().height,
       horizontal:document.documentElement.scrollWidth-document.documentElement.clientWidth
      };
    });
    assert.equal(before.sticky,'sticky',path+' not sticky');
    assert.equal(before.top,0,path+' sticky offset should be zero');
    assert.ok(before.tabs>20&&before.topbar>28,path+' missing nav row');
    assert.ok(Math.abs(before.measured-before.headerHeight)<2,path+' measured height incorrect');
    assert.ok(before.scrollPadding>before.headerHeight+8,path+' inadequate scroll offset');
    assert.ok(before.horizontal<=6,path+' overflow '+before.horizontal);
    // Short quiz pages may not naturally have enough scroll distance; extend
    // the test document only to exercise the pinned state consistently.
    await page.evaluate(()=>{
      document.body.style.minHeight='max(1800px, 220vh)';
      window.scrollTo({top:720,behavior:'instant'});
    });
    await page.waitForFunction(()=>window.scrollY>300,{timeout:3000});
    const after=await page.evaluate(()=>{
      const header=document.querySelector('.lesson-header');
      const tabs=header.querySelector('.lesson-tabs').getBoundingClientRect();
      const topbar=header.querySelector('.lesson-topbar').getBoundingClientRect();
      const container=header.getBoundingClientRect();
      return {top:container.top,bottom:container.bottom,height:container.height,
        topbarTop:topbar.top,tabsBottom:tabs.bottom,
        scrolled:header.classList.contains('is-scrolled')};
    });
    assert.ok(Math.abs(after.top)<1.5,path+' header not pinned '+JSON.stringify(after));
    assert.ok(after.topbarTop>=-1.5&&after.tabsBottom<=after.bottom+1.5,
      path+' navigation row clipped '+JSON.stringify(after));
    assert.ok(after.scrolled,path+' no scrolled state');
   }
   console.log('STICKY TWO-ROW HEADER PASS',viewport.width,'px',samplePages.length,'page types');
  }
  // Explicitly exercise a real table-of-contents link.
  await page.setViewport({width:390,height:844});
  await page.goto(BASE+'/w2/course/',{waitUntil:'networkidle0'});
  // The table of contents is collapsed by default on mobile.
  await page.$eval('.toc-panel',el=>{el.open=true;});
  await page.click('.toc-panel a[href="#w2-entropy"]');
  await page.waitForFunction(()=>{
    const target=document.querySelector('#w2-entropy');
    const header=document.querySelector('.lesson-header');
    const gap=target.getBoundingClientRect().top-header.getBoundingClientRect().bottom;
    return location.hash==='#w2-entropy' && gap>=4 && gap<100;
  },{timeout:5000});
  const result=await page.evaluate(()=>({
    hash:location.hash,
    target:Math.round(document.querySelector('#w2-entropy').getBoundingClientRect().top),
    bottom:Math.round(document.querySelector('.lesson-header').getBoundingClientRect().bottom)
  }));
  console.log('ANCHOR OFFSETS PASS',result);
  // Print output should not retain the screen's sticky navigation.
  await page.emulateMediaType('print');
  assert.equal(await page.$eval('.lesson-header',el=>getComputedStyle(el).display),'none');
  await page.emulateMediaType('screen');
  // Nothing on the homepage should acquire the sticky lesson nav.
  await page.goto(BASE+'/',{waitUntil:'domcontentloaded'});
  assert.equal(await page.$('.lesson-header'),null,'homepage must not show a lesson header');
  assert.deepEqual(errors,[],'JS errors: '+errors.join(' | '));
  console.log('PRINT + HOMEPAGE + ERROR CHECKS PASS');
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
