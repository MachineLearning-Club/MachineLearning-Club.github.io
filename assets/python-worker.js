/* Browser-only, no-account Python. Runs code in an isolated worker. */
self.onmessage = async (event) => {
  const base="https://cdn.jsdelivr.net/pyodide/v0.28.3/full/";
  const code=String(event.data?.code||"");
  try {
    self.importScripts(base+"pyodide.js");
    if(typeof self.loadPyodide!=="function") throw new Error("Python loader unavailable");
    const py=await self.loadPyodide({indexURL:base});
    self.postMessage({type:"ready"});
    let output=[];
    py.setStdout({batched:line=>output.push(line)});
    py.setStderr({batched:line=>output.push(line)});
    await py.loadPackagesFromImports(code);
    const result=await py.runPythonAsync(code);
    if(result!==undefined&&result!==null&&result!==self.document)output.push(String(result));
    self.postMessage({type:"done",value:output.join("\n")});
  }catch(error){
    self.postMessage({type:"error",value:String(error.message||error)});
  }
};