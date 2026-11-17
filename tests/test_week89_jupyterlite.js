const p=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
(async()=>{const b=await p.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});try{
 for(const [name,url] of [
 ['w8','http://127.0.0.1:8877/jupyter/lab/index.html?path=digits-revision.ipynb'],
 ['w9','http://127.0.0.1:8877/jupyter/lab/index.html?path=digits-practical.ipynb']
 ]){
  const context=await b.createBrowserContext();
  const page=await context.newPage();await page.setViewport({width:1320,height:900});
  const res=await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForSelector('.jp-Notebook',{timeout:50000});
  await page.waitForFunction(expected=>document.querySelectorAll('.jp-Notebook .jp-Cell').length>=expected,{timeout:40000},name==='w8'?16:14);
  const state=await page.evaluate(()=>({title:document.title,tabs:[...document.querySelectorAll('.lm-DockPanel-tabBar .lm-TabBar-tabLabel')].map(x=>x.textContent.trim()),cells:document.querySelectorAll('.jp-Cell').length,notebook:document.querySelector('.jp-Notebook')?.textContent.slice(0,280)}));
  console.log('OPENED',name,res.status(),JSON.stringify(state));
  if(state.cells<(name==='w8'?16:14)||!state.notebook.includes('Week '+(name==='w8'?8:9)))throw Error('Notebook contents unavailable '+name);
  await page.screenshot({path:'/tmp/mlclub-'+name+'-jupyterlite.png'});
  await context.close();
 }
}finally{await b.close()}})().catch(e=>{console.error(e.stack);process.exit(1)});
