const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
   const paths=['/preview/','/preview/w1/course/','/preview/w1/lab/','/preview/w1/homework/','/preview/w1/advanced/','/preview/w3/course/','/preview/w3/lab/','/preview/w3/homework/','/preview/w3/advanced/'];
   for(const width of [360,768,1280]){
      const page=await browser.newPage();await page.setViewport({width,height:900});
      for(const path of paths){
        const response=await page.goto('http://127.0.0.1:8765'+path,{waitUntil:'domcontentloaded'});
        const test=await page.evaluate(()=>{
          const nav=document.querySelector('.lesson-tabs');
          const links=nav?[...nav.querySelectorAll('a')].map(a=>a.getBoundingClientRect()):[];
          let overlap=false;
          for(let i=0;i<links.length;i++)for(let j=i+1;j<links.length;j++)
           if(links[i].left<links[j].right&&links[j].left<links[i].right&&links[i].top<links[j].bottom&&links[j].top<links[i].bottom)overlap=true;
          return {overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+2,
            overlaps:overlap,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,
            links:links.length,title:document.title};
        });
        if(![200,304].includes(response.status())||test.overflow||test.overlaps||!test.font.includes('Georgia')||test.background!='rgb(255, 255, 255)'||(path!='/preview/'&&test.links!==4))
          throw Error(JSON.stringify({width,path,status:response.status(),test}));
        console.log(width,path,'OK');
      }
      await page.close();
   }
   const page=await browser.newPage();
   await page.goto('http://127.0.0.1:8765/preview/w3/lab/',{waitUntil:'domcontentloaded'});
   const gainA=await page.$eval('[data-id3-result]',el=>el.textContent);
   await page.select('[data-id3-feature]','wind');
   const gainB=await page.$eval('[data-id3-result]',el=>el.textContent);
   if(!gainA.includes('0.5488')||!gainB.includes('0.0488')) throw Error('Gain explorer wrong: '+gainA+' '+gainB);
   console.log('Interactive ID3 gain verified',gainA,gainB);
   await page.close();
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
