const puppeteer=require('/usr/lib/node_modules/@wonderwhy-er/desktop-commander/node_modules/puppeteer');
const fs=require('fs');
const path=require('path');
const assert=(v,msg)=>{if(!v)throw Error(msg)};
const base='http://127.0.0.1:8877';
(async()=>{
 const b=await puppeteer.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const page=await b.newPage();const pages=['/','/w1/course/','/w4/course/','/w5/lab/','/w7/advanced/','/w15/course/','/timetable/','/resources/','/guides/python/','/quiz/','/w1/slides/'];
 for(const width of [390,820,1280]){
  await page.setViewport({width,height:900});
  for(const sitepath of pages){
   const response=await page.goto(base+sitepath,{waitUntil:'networkidle0',timeout:25000});
   assert([200,304].includes(response.status()),'Bad status '+sitepath);
   const result=await page.evaluate(()=>{
    const f=document.querySelector('footer.site.mlclub-footer');
    if(!f)return null;
    const rect=f.getBoundingClientRect(),grid=f.querySelector('.mlclub-footer-grid').getBoundingClientRect();
    const anchors=[...f.querySelectorAll('a')].map(a=>({label:a.textContent.trim(),href:a.getAttribute('href')}));
    return {
      label:f.getAttribute('aria-label'),
      visible:getComputedStyle(f).display!=='none',
      gridColumns:getComputedStyle(f.querySelector('.mlclub-footer-grid')).gridTemplateColumns,
      width:document.documentElement.scrollWidth,
      viewport:document.documentElement.clientWidth,
      footerW:rect.width,
      footerLeft:rect.left,
      footerRight:rect.right,
      gridRight:grid.right,
      anchors,
      legal:f.querySelector('.mlclub-footer-bottom')?.textContent.trim()
    };
   });
   assert(result!==null,'Missing footer '+sitepath);
   assert(result.visible,'Hidden footer '+sitepath);
   assert(result.width<=result.viewport+4,'Horizontal overflow '+sitepath+' '+width+' '+JSON.stringify(result));
   assert(result.footerLeft>=-2&&result.footerRight<=result.viewport+2,'Footer exceeds viewport '+sitepath+' '+width);
   assert(result.label==='Machine Learning Club footer','Accessibility label wrong');
   const links=Object.fromEntries(result.anchors.map(x=>[x.label,x.href]));
   for(const [name,url] of Object.entries({'Dragoș-Andrei Bobu':'https://dragosandreibobu.github.io/','All lessons':'/','Timetable':'/timetable/','Bibliography':'/resources/','Weekly quizzes':'/quiz/','GitHub organisation':'https://github.com/MachineLearning-Club','Website source':'https://github.com/MachineLearning-Club/MachineLearning-Club.github.io','Seven Hills International School':'https://sevenhills.ro/','Personal website':'https://dragosandreibobu.github.io/'})){
     assert(links[name]===url,'Missing or wrong link '+name+' on '+sitepath+' got '+links[name]);
   }
   assert(result.legal.includes('BOBU DRAGOȘ-ANDREI PERSOANĂ FIZICĂ AUTORIZATĂ'),'Legal operator not present');
   if(width===390&&['/','/w4/course/','/quiz/'].includes(sitepath))await page.screenshot({path:'/tmp/mlclub-footer-'+(sitepath==='/'?'home':sitepath==='/quiz/'?'quiz':'course')+'-mobile.png',fullPage:true});
   if(width===1280&&sitepath==='/')await page.screenshot({path:'/tmp/mlclub-footer-home-desktop.png',fullPage:true});
   console.log('PASS',width,sitepath,result.anchors.length,'links');
  }
 }
 console.log('FOOTER RESPONSIVE + LINK VALIDATION PASSED');
 }finally{await b.close();}
})().catch(e=>{console.error(e.stack);process.exit(1)});
