// Static regression checks for the dataset mismatch identified in the audit.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const course=read('data/week23/w2_course.html');
const lab=read('data/week23/w2_lab.html');
const advanced=read('data/week23/w2_advanced.html');
const print=read('w2/advanced/print.html');
const tex=read('w2/advanced/week-02-id3.tex');
assert.match(course,/twelve labelled examples/);
assert.match(lab,/twelve-row activity diary/);
assert.match(advanced,/separate eight-case truth table/);
assert.match(print,/separate complete eight-row truth table/);
assert.match(print,/not the twelve-row activity diary/);
assert.match(tex,/separate, complete eight-row truth table/);
const ids=[...print.matchAll(/<tr><td>([1-4])<\/td>/g)].length;
assert.equal(ids,4,'Printed eight-row table begins with four explicit sunny examples');
for(let w of [10,11]){
 const html=read(`w${w}/lab/index.html`);
 assert.match(html,new RegExp('data-submission-week="'+w+'"'));
 assert.match(html,/class="student-name"/);
 assert.match(html,/class="submission-files"/);
 assert.match(html,/class="prepare-submission"/);
 assert.match(html,/Downloading is not submitting/);
}
assert.match(read('data/week1011/w11_lab.html'),/real GitHub and Codespaces tutorial/);
console.log('CONSISTENCY AND SUBMISSION CONTRACT PASS');
