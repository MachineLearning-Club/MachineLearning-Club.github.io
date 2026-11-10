/* ML Club eQuiz · Frontend proof of concept.
 * It is not a secure exam system: answers and demo access codes are public JSON.
 * No accounts, passwords, grades or network submissions. Results live in localStorage.
 */
(() => {
  "use strict";

  const DATA_ROOT = "/quiz/data/";
  const STORAGE_KEY = "mlclub.equiz.demo.attempts.v1";
  const QUESTIONS = ["A","B","C","D"];
  const $ = (id) => document.getElementById(id);
  const state = {
    catalog: [], attempts: loadAttempts(), active: null, review: null,
    questionIndex: 0, timer: null, bankCache: new Map(), lastAttemptId: null
  };

  function loadAttempts() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(value) ? value.filter(x => x && Number.isInteger(x.week) && Array.isArray(x.answers)) : [];
    } catch (_) { return []; }
  }
  function persistAttempts() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state.attempts)); }
    catch (_) { $("load-error").hidden = false; $("load-error").textContent = "This browser could not save the score. The attempt remains visible until the page is closed."; }
  }
  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function cell(row, text, cls) {
    const td = element("td", text, cls);
    row.appendChild(td);
    return td;
  }
  function pad2(x) { return String(x).padStart(2,"0"); }
  function formatTime(seconds) {
    const n = Math.max(0, Math.ceil(seconds));
    return pad2(Math.floor(n / 60)) + ":" + pad2(n % 60);
  }
  function formatDate(iso) {
    const date = new Date(iso);
    return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString("en-GB", {year:"numeric",month:"short",day:"2-digit",hour:"2-digit",minute:"2-digit"});
  }
  function mostRecentScore(week) {
    return state.attempts.filter(x=>x.week===week).sort((a,b)=>new Date(b.submittedAt)-new Date(a.submittedAt))[0];
  }
  function renderCatalog() {
    const filter = $("filter").value.trim().toLowerCase();
    const tbody = $("quiz-rows");
    tbody.replaceChildren();
    let shown = 0;
    for (const quiz of state.catalog) {
      if (filter && ![quiz.week,quiz.title,quiz.subject].join(" ").toLowerCase().includes(filter)) continue;
      shown++;
      const row = element("tr");
      cell(row, pad2(quiz.week));
      const title = cell(row);
      const main = element("strong", quiz.title);
      title.appendChild(main);
      title.appendChild(element("span", quiz.subject, "topic"));
      cell(row, quiz.status === "demo" ? quiz.durationMinutes + " min" : "—");
      cell(row, quiz.status === "demo" ? quiz.questionCount : "—");
      cell(row, quiz.subject);
      const scoreCell = cell(row);
      const latest = mostRecentScore(quiz.week);
      if (latest) {
        const score = element("span", latest.score + " / " + quiz.maxPoints, "score " + (latest.score>=7?"good":"mid"));
        scoreCell.appendChild(score);
      } else {
        scoreCell.appendChild(element("span", quiz.status==="demo"?"Not taken":"Not available", "label-status "+(quiz.status==="demo"?"ready":"pending")));
      }
      const actionCell = cell(row);
      if (quiz.status==="demo") {
        const b = element("button","Take demo","button button-primary");
        b.type="button";
        b.setAttribute("aria-label","Open access code for Week "+quiz.week);
        b.addEventListener("click",()=>openAccess("MLC"+pad2(quiz.week)));
        actionCell.appendChild(b);
      } else {
        const label = element("span","Planned","label-status pending");
        label.title = "Question bank not approved yet";
        actionCell.appendChild(label);
      }
      tbody.appendChild(row);
    }
    if (!shown) {
      const row = element("tr");
      const td = cell(row,"No quizzes match your filter.");
      td.colSpan = 7;
      tbody.appendChild(row);
    }
    $("available-count").textContent = state.catalog.filter(x=>x.status==="demo").length;
    $("attempt-count").textContent = state.attempts.length;
    $("highest-score").textContent = state.attempts.length
      ? Math.max(...state.attempts.map(x=>x.score)) + " / 10" : "—";
  }
  function renderHistory() {
    const tbody = $("history-rows");
    tbody.replaceChildren();
    const attempts = [...state.attempts].sort((a,b)=>new Date(b.submittedAt)-new Date(a.submittedAt));
    for (const record of attempts) {
      const row = element("tr");
      cell(row,formatDate(record.submittedAt));
      cell(row,"Week " + pad2(record.week) + " · " + record.title);
      cell(row,formatTime(record.elapsedSeconds||0));
      cell(row,record.answers.filter(arr=>Array.isArray(arr)&&arr.length).length + " / " + record.answers.length);
      cell(row,record.score + " / " + record.maxPoints,"score " + (record.score>=7?"good":"mid"));
      const actionCell=cell(row);
      const button=element("button","View","button button-quiet");
      button.type="button";
      button.addEventListener("click",()=>showReview(record));
      actionCell.appendChild(button);
      tbody.appendChild(row);
    }
    if (!attempts.length) {
      const row = element("tr");
      const td = cell(row,"No attempts yet. Use Take a test to begin.");
      td.colSpan=6;tbody.appendChild(row);
    }
    $("export-results").disabled=!attempts.length;
  }
  function refresh() {renderCatalog();renderHistory();}

  function openAccess(prefill="") {
    $("access-input").value=prefill;
    $("access-error").hidden=true;
    $("access-dialog").showModal();
    $("access-input").focus();
    if(prefill) $("access-input").select();
  }
  async function loadBank(week) {
    if (state.bankCache.has(week)) return state.bankCache.get(week);
    const response = await fetch(DATA_ROOT+"week-"+pad2(week)+".json",{cache:"no-store"});
    if(!response.ok)throw new Error("Could not load the questions for Week "+week+".");
    const data=await response.json();
    if(data.week!==week||!Array.isArray(data.questions)||data.questions.length!==10)
      throw new Error("Invalid quiz data for Week "+week+".");
    state.bankCache.set(week,data);
    return data;
  }
  async function launch(week) {
    try {
      const bank=await loadBank(week);
      if($("access-dialog").open)$("access-dialog").close();
      stopTimer();
      state.review=null;
      state.questionIndex=0;
      const now=Date.now();
      state.active={
        week,bank,startedAt:new Date(now).toISOString(),endsAt:now+bank.durationSeconds*1000,
        answers:bank.questions.map(()=>[])
      };
      $("question-dialog").showModal();
      renderQuestion();
      state.timer=window.setInterval(tickTimer,250);
      tickTimer();
    } catch(error) {
      $("access-error").hidden=false;
      $("access-error").textContent=error.message;
    }
  }
  function tickTimer() {
    if(!state.active)return;
    const seconds=(state.active.endsAt-Date.now())/1000;
    const timer=$("time-remaining");
    timer.textContent=formatTime(seconds);
    timer.classList.toggle("urgent",seconds<=30);
    if(seconds<=0)finish(true);
  }
  function stopTimer() {
    if(state.timer!==null){clearInterval(state.timer);state.timer=null;}
  }
  function getView() {
    if(state.active)return {bank:state.active.bank,answers:state.active.answers,isReview:false,record:null};
    if(state.review)return {bank:state.review.bank,answers:state.review.record.answers,isReview:true,record:state.review.record};
    return null;
  }
  function selectedFor(index) {
    const view=getView();
    return view&&Array.isArray(view.answers[index])?view.answers[index]:[];
  }
  function equalSets(a,b) {
    if(a.length!==b.length)return false;
    const set=new Set(a);
    return b.every(x=>set.has(x));
  }
  function calculateScore(bank,answers) {
    return bank.questions.reduce((total,q,i)=>total+(equalSets(Array.isArray(answers[i])?answers[i]:[],q.correct)?q.points:0),0);
  }
  function renderQuestion() {
    const view=getView();
    if(!view)return;
    const {bank,isReview,record}=view;
    const index=state.questionIndex;
    const q=bank.questions[index];
    const selected=selectedFor(index);
    const count=bank.questions.length;
    $("test-title").textContent="Week "+pad2(bank.week)+" — "+bank.title;
    $("exam-status").textContent=isReview?"Review · "+record.score+" / "+record.maxPoints:"In progress";
    $("time-remaining").textContent=isReview?"Completed":formatTime((state.active.endsAt-Date.now())/1000);
    $("time-remaining").classList.toggle("urgent",!isReview&&(state.active.endsAt-Date.now())<=30000);
    $("question-index").textContent="Question "+(index+1)+" / "+count;
    $("answered-index").textContent=view.answers.filter(x=>Array.isArray(x)&&x.length).length+" / "+count+" answered";
    $("question-number").textContent="#"+(index+1)+" / "+count;
    $("question-topic").textContent=q.topic;
    $("question-text").textContent=q.prompt;
    $("selection-hint").textContent=q.type==="multiple"?"Select ALL correct answers.":"Select one answer.";
    const chip=$("question-points");
    const correct=isReview&&equalSets(selected,q.correct);
    chip.textContent=isReview?(correct?q.points+" p":"0 p"):q.points+" p";
    chip.className="points-chip"+(isReview?(correct?" correct":" wrong"):"");
    const answers=$("answers");
    answers.replaceChildren();
    q.options.forEach((option,choice)=>{
      const label=element("label",null,"answer"+(isReview?" disabled":""));
      const input=document.createElement("input");
      input.type=q.type==="multiple"?"checkbox":"radio";
      input.name="quiz-answer";
      input.value=String(choice);
      input.checked=selected.includes(choice);
      input.disabled=isReview;
      input.setAttribute("aria-label",QUESTIONS[choice]+": "+option);
      if(!isReview){
        input.addEventListener("change",()=>{
          if(!state.active)return;
          const a=state.active.answers[index];
          if(q.type==="single")state.active.answers[index]=[choice];
          else if(input.checked && !a.includes(choice))a.push(choice);
          else if(!input.checked)state.active.answers[index]=a.filter(x=>x!==choice);
          renderNav();
          $("answered-index").textContent=state.active.answers.filter(x=>x.length).length+" / "+count+" answered";
        });
      }
      const letter=element("span",QUESTIONS[choice]+".","letter");
      const text=element("span",option,"answer-text");
      label.append(input,letter,text);
      if(isReview){
        const isCorrect=q.correct.includes(choice);
        const wasSelected=selected.includes(choice);
        if(isCorrect)label.classList.add(wasSelected?"correct-option":"missed-option");
        else if(wasSelected)label.classList.add("incorrect-selected");
      }
      answers.appendChild(label);
    });
    const explanation=$("review-explanation");
    if(isReview) {
      explanation.hidden=false;
      explanation.replaceChildren(
        element("strong",correct?"Correct answer · "+q.points+" point":"Answer review · 0 points"),
        element("p","Correct selection: "+q.correct.map(i=>QUESTIONS[i]).join(", ")+". "+q.explanation)
      );
    } else {
      explanation.hidden=true;
      explanation.replaceChildren();
    }
    $("prev-question").disabled=index===0;
    $("jump-first").disabled=index===0;
    $("next-question").disabled=index===count-1;
    $("jump-last").disabled=index===count-1;
    $("finish-test").hidden=isReview;
    $("close-test").textContent=isReview?"Close review":"Exit";
    renderNav();
  }
  function renderNav() {
    const view=getView();
    if(!view)return;
    const nav=$("question-nav");
    nav.replaceChildren();
    view.bank.questions.forEach((q,i)=>{
      const button=element("button",String(i+1));
      button.type="button";
      const selected=Array.isArray(view.answers[i])?view.answers[i]:[];
      if(selected.length)button.classList.add("answered");
      if(view.isReview)button.classList.add(equalSets(selected,q.correct)?"correct":"wrong");
      if(i===state.questionIndex)button.classList.add("current");
      if(i===state.questionIndex)button.setAttribute("aria-current","step");
      button.setAttribute("aria-label","Question "+(i+1)+(selected.length?" answered":" unanswered"));
      button.addEventListener("click",()=>goToQuestion(i));
      nav.appendChild(button);
    });
  }
  function goToQuestion(index) {
    const view=getView();if(!view)return;
    state.questionIndex=Math.max(0,Math.min(view.bank.questions.length-1,index));
    renderQuestion();
    $("question-dialog").scrollTop=0;
  }
  function finish(timedOut=false) {
    const active=state.active;
    if(!active)return;
    const blanks=active.answers.filter(a=>!a.length).length;
    if(!timedOut&&blanks>0&&!window.confirm("You have "+blanks+" unanswered question(s). Submit anyway?"))return;
    stopTimer();
    const ended=Date.now();
    const record={
      id:"attempt-"+ended+"-"+Math.floor(Math.random()*100000),
      week:active.week,title:active.bank.title,startedAt:active.startedAt,
      submittedAt:new Date(ended).toISOString(),
      elapsedSeconds:Math.min(active.bank.durationSeconds,Math.max(0,Math.round((ended-new Date(active.startedAt).getTime())/1000))),
      answers:active.answers.map(a=>[...a].sort()),score:calculateScore(active.bank,active.answers),
      maxPoints:active.bank.maximumPoints,timedOut
    };
    state.attempts.push(record);
    state.active=null;
    state.lastAttemptId=record.id;
    $("question-dialog").close();
    persistAttempts();
    refresh();
    $("summary-points").textContent=record.score+" / "+record.maxPoints;
    $("summary-percent").textContent=Math.round(100*record.score/record.maxPoints)+"%";
    $("summary-description").textContent=(timedOut?"The five-minute time limit was reached. ":"")+
      "You answered "+record.answers.filter(a=>a.length).length+" of "+record.answers.length+" questions. Review the solutions below.";
    $("summary-dialog").showModal();
  }
  async function showReview(record) {
    try {
      const bank=await loadBank(record.week);
      state.active=null;stopTimer();
      state.review={record,bank};
      state.questionIndex=0;
      if($("summary-dialog").open)$("summary-dialog").close();
      $("question-dialog").showModal();
      renderQuestion();
    } catch (error) {
      alert("Could not load this attempt: "+error.message);
    }
  }
  function leaveQuestionDialog() {
    if(state.active) {
      if(!window.confirm("Exit this test without submitting? Your answers will be discarded."))return false;
      state.active=null;stopTimer();
    }
    if(state.review)state.review=null;
    $("question-dialog").close();
    refresh();
    return true;
  }
  function exportResults() {
    if(!state.attempts.length)return;
    const fields=["date","week","test","duration_seconds","answered","score","maximum_points","timed_out"];
    const rows=[fields,...state.attempts.map(a=>[
      a.submittedAt,a.week,a.title,a.elapsedSeconds,
      a.answers.filter(x=>x.length).length,a.score,a.maxPoints,a.timedOut
    ])];
    const csv=rows.map(row=>row.map(val=>'"'+String(val).replace(/"/g,'""')+'"').join(",")).join("\r\n")+"\r\n";
    const blob=new Blob(["\ufeff",csv],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;a.download="ml-club-demo-quiz-results.csv";
    document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  $("take-test").addEventListener("click",()=>openAccess());
  $("cancel-access").addEventListener("click",()=>$("access-dialog").close());
  $("access-form").addEventListener("submit",e=>{
    e.preventDefault();
    const code=$("access-input").value.trim().toUpperCase();
    const match=/^MLC(0[2-9]|1[0-5])$/.exec(code);
    if(!match){
      $("access-error").hidden=false;
      $("access-error").textContent="No demo quiz matches that code. Try MLC02 or MLC03.";
      return;
    }
    const week=Number(match[1]);
    const meta=state.catalog.find(q=>q.week===week);
    if(!meta||meta.status!=="demo"){
      $("access-error").hidden=false;
      $("access-error").textContent="Week "+week+" is scheduled, but its questions are not approved yet.";
      return;
    }
    launch(week);
  });
  $("filter").addEventListener("input",renderCatalog);
  $("export-results").addEventListener("click",exportResults);
  $("reset-local").addEventListener("click",()=>{
    if(!state.attempts.length)return;
    if(window.confirm("Delete all demo quiz results stored in this browser?")){
      state.attempts=[];persistAttempts();refresh();
    }
  });
  $("prev-question").addEventListener("click",()=>goToQuestion(state.questionIndex-1));
  $("next-question").addEventListener("click",()=>goToQuestion(state.questionIndex+1));
  $("jump-first").addEventListener("click",()=>goToQuestion(0));
  $("jump-last").addEventListener("click",()=>goToQuestion(9));
  $("finish-test").addEventListener("click",()=>finish(false));
  $("close-test").addEventListener("click",leaveQuestionDialog);
  $("question-dialog").addEventListener("cancel",event=>{event.preventDefault();leaveQuestionDialog();});
  $("summary-close").addEventListener("click",()=>$("summary-dialog").close());
  $("review-now").addEventListener("click",()=>{
    const record=state.attempts.find(a=>a.id===state.lastAttemptId);
    if(record)showReview(record);
  });

  async function init() {
    try {
      const response=await fetch(DATA_ROOT+"catalog.json",{cache:"no-store"});
      if(!response.ok)throw new Error("HTTP "+response.status);
      const data=await response.json();
      if(!Array.isArray(data.quizzes)||data.quizzes.length!==14)throw new Error("Invalid quiz catalogue");
      state.catalog=data.quizzes;
      refresh();
      const week=Number(new URLSearchParams(location.search).get("week"));
      if(week>=2&&week<=15)openAccess("MLC"+pad2(week));
    } catch(error) {
      $("load-error").hidden=false;
      $("load-error").textContent="Could not load the quiz catalogue: "+error.message;
      $("quiz-rows").replaceChildren(element("tr"));
      $("quiz-rows").firstChild.appendChild(element("td","Quiz data unavailable."));
    }
  }
  init();
})();