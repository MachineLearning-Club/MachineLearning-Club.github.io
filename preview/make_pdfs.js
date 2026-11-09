const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
  for(const week of [1,3]){
   const page=await browser.newPage();
   await page.setViewport({width:900,height:1100,deviceScaleFactor:1});
   const base='http://127.0.0.1:8765/preview/w'+week+'/advanced/print.html';
   const response=await page.goto(base,{waitUntil:'networkidle0',timeout:15000});
   if(response.status()!==200)throw Error('Print page unavailable '+base+' status '+response.status());
   const title=await page.title();
   const target='/home/admin/projects/mlc-site-update-2026/preview/w'+week+'/advanced/week-'+String(week).padStart(2,'0')+(week===1?'-reasoning.pdf':'-id3.pdf');
   await page.pdf({path:target,format:'A4',printBackground:false,preferCSSPageSize:true,
                   displayHeaderFooter:false,margin:{top:'17mm',bottom:'17mm',left:'17mm',right:'17mm'}});
   console.log('Rendered',title,'=>',target);
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
