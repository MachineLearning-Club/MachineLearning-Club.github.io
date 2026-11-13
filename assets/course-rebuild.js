
/* Week 1 teaching visuals: button rule, exhaustive labelled decision tree, and K-means iteration. */
(() => {
  "use strict";

  // A programmed rule: the input button directly determines the output light.
  const lamp=document.querySelector("[data-lamp-demo]");
  if(lamp){
    const button=lamp.querySelector("[data-lamp-toggle]");
    const pressed=lamp.querySelector("[data-lamp-pressed]");
    const result=lamp.querySelector("[data-lamp-result]");
    const svg=lamp.querySelector("[data-lamp-svg]");
    let on=false;
    const render=()=>{
      lamp.classList.toggle("light-on",on);
      button.setAttribute("aria-pressed",String(on));
      button.textContent=on?"Release the button":"Press the button";
      pressed.textContent=on?"True":"False";
      result.textContent=on?"ON":"OFF";
      svg.setAttribute("aria-label","Lightbulb currently "+(on?"on":"off"));
    };
    button.addEventListener("click",()=>{on=!on;render();});
    render();
  }

  // A reference minimax solver labels every reachable X-to-move position.
  // A complete categorical decision tree (one test per board cell) memorises
  // those supervised examples and is validated on every reachable X state.
  const game=document.querySelector("[data-ttt-game]");
  if(game){
    const lines=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],
      [1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    const order=[4,0,2,6,8,1,3,5,7];
    const win=b=>{
      for(const [a,c,d] of lines){
        if(b[a]!=="." && b[a]===b[c] && b[c]===b[d])return b[a];
      }
      return null;
    };
    const over=b=>win(b)!==null || b.every(v=>v!==".");
    const terminalScore=b=>{
      const w=win(b);
      return w==="X"?1:w==="O"?-1:0;
    };
    const memo=new Map();
    function minimax(b,turn){
      if(over(b))return terminalScore(b);
      const key=b.join("");
      if(memo.has(key))return memo.get(key);
      let best=turn==="X"?-2:2;
      for(const i of order){
        if(b[i]!==".")continue;
        b[i]=turn;
        const s=minimax(b,turn==="X"?"O":"X");
        b[i]=".";
        best=turn==="X"?Math.max(best,s):Math.min(best,s);
        if(best===(turn==="X"?1:-1))break;
      }
      memo.set(key,best);
      return best;
    }
    function optimalMove(b){
      let best=-2,chosen=-1;
      for(const i of order){
        if(b[i]!==".")continue;
        b[i]="X";
        const s=minimax(b,"O");
        b[i]=".";
        if(s>best){best=s;chosen=i;}
      }
      return chosen;
    }
    const examples=[];
    const visited=new Set();
    function gather(b,turn){
      const key=b.join("");
      if(visited.has(key))return;
      visited.add(key);
      if(over(b))return;
      if(turn==="X")examples.push({cells:key,move:optimalMove(b)});
      for(const i of order){
        if(b[i]!==".")continue;
        b[i]=turn;
        gather(b,turn==="X"?"O":"X");
        b[i]=".";
      }
    }
    gather(Array(9).fill("."),"X");
    const tree={children:Object.create(null)};
    for(const example of examples){
      let node=tree;
      for(const cell of example.cells){
        node.children[cell]??={children:Object.create(null)};
        node=node.children[cell];
      }
      node.label=example.move;
    }
    const predict=b=>{
      let node=tree;
      for(const cell of b)node=node?.children?.[cell];
      return node?.label??-1;
    };
    // Compare the learned tree to the optimal minimax score, not merely
    // to the first move selected when several optimal moves are tied.
    let verified=0;
    for(const example of examples){
      const board=example.cells.split("");
      const move=predict(board);
      if(move<0 || board[move]!==".")throw new Error("Invalid trained game-tree leaf");
      const best=optimalMove(board);
      board[best]="X";
      const bestScore=minimax(board,"O");
      board[best]=".";
      board[move]="X";
      const predictedScore=minimax(board,"O");
      if(predictedScore!==bestScore)throw new Error("Nonoptimal game-tree decision");
      verified++;
    }
    const cells=Array.from(game.querySelectorAll("[data-ttt-cell]"));
    const status=game.querySelector("[data-ttt-status]");
    game.querySelector("[data-ttt-count]").textContent=String(examples.length);
    game.querySelector("[data-ttt-verified]").textContent=String(verified)+"/"+examples.length+" optimal";
    let board=Array(9).fill(".");
    let finished=false;

    const finishMessage=()=>{
      const w=win(board);
      if(w==="X"){finished=true;return "X wins. Try another game and a different strategy.";}
      if(w==="O"){finished=true;return "O wins. The decision tree failed its guarantee.";}
      if(board.every(c=>c!==".")){finished=true;return "Draw. You held the optimal tree to a draw.";}
      return null;
    };
    function redraw(){
      cells.forEach((button,i)=>{
        const v=board[i];
        button.textContent=v==="."?"":v;
        button.classList.toggle("player-o",v==="O");
        button.classList.toggle("player-x",v==="X");
        button.disabled=finished || v!==".";
        button.setAttribute("aria-label",
          ["Top-left","Top-middle","Top-right","Middle-left","Center","Middle-right","Bottom-left","Bottom-middle","Bottom-right"][i]+" cell: "+
          (v==="."?"empty":v));
      });
    }
    function modelTurn(){
      const action=predict(board);
      if(action<0 || board[action]!==".")throw new Error("Uncovered or invalid tic-tac-toe position");
      board[action]="X";
    }
    function reset(){
      board=Array(9).fill(".");
      finished=false;
      modelTurn();
      status.textContent="X moved first. Choose an empty square for O.";
      redraw();
    }
    cells.forEach((button,i)=>button.addEventListener("click",()=>{
      if(finished || board[i]!==".")return;
      board[i]="O";
      let msg=finishMessage();
      if(!msg){modelTurn();msg=finishMessage();}
      status.textContent=msg||"The decision tree responded. Your turn (O).";
      redraw();
    }));
    game.querySelector("[data-ttt-reset]").addEventListener("click",reset);
    reset();
  }

  // Fixed point positions across all three diagrams. Only one operation
  // changes between adjacent frames: assignment colours, then centres.
  const points=[
    {x:2,y:2},{x:2,y:3},{x:3,y:2},{x:3,y:3},
    {x:7,y:7},{x:7,y:8},{x:8,y:7},{x:8,y:8}
  ];
  const initialCentres=[{x:3,y:5},{x:6,y:5}];
  const sqdist=(p,q)=>(p.x-q.x)**2+(p.y-q.y)**2;
  const groups=points.map(p=>sqdist(p,initialCentres[0])<=sqdist(p,initialCentres[1])?0:1);
  const updatedCentres=[0,1].map(k=>{
    const group=points.filter((_,i)=>groups[i]===k);
    return {x:group.reduce((sum,p)=>sum+p.x,0)/group.length,
      y:group.reduce((sum,p)=>sum+p.y,0)/group.length};
  });
  const NS="http://www.w3.org/2000/svg";
  const element=(tag,attrs={},content)=>{
    const el=document.createElementNS(NS,tag);
    for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
    if(content!==undefined)el.textContent=String(content);
    return el;
  };
  document.querySelectorAll("[data-cluster-plot]").forEach(svg=>{
    const stage=svg.getAttribute("data-cluster-plot");
    const left=34, top=15, width=296, height=224;
    const X=x=>left+x*width/10,Y=y=>top+(10-y)*height/10;
    const col=["#437eaf","#bc864e"];
    for(let v=0;v<=10;v+=2){
      svg.append(
        element("line",{x1:X(v),y1:Y(0),x2:X(v),y2:Y(10),stroke:"#e2e8ed"}),
        element("line",{x1:X(0),y1:Y(v),x2:X(10),y2:Y(v),stroke:"#e2e8ed"}),
        element("text",{x:X(v),y:253,"text-anchor":"middle","font-size":10,fill:"#647989"},v),
        element("text",{x:27,y:Y(v)+3,"text-anchor":"end","font-size":10,fill:"#647989"},v)
      );
    }
    for(let i=0;i<points.length;i++){
      const p=points[i];
      svg.append(element("circle",{
        cx:X(p.x),cy:Y(p.y),r:7.5,
        fill:stage==="raw"?"#8495a1":col[groups[i]],
        stroke:"#fff","stroke-width":1.2
      }));
    }
    const centres=stage==="recentered"?updatedCentres:initialCentres;
    centres.forEach((p,i)=>{
      svg.append(
        element("circle",{cx:X(p.x),cy:Y(p.y),r:13,
          fill:"white",stroke:stage==="raw"?"#738998":col[i],
          "stroke-width":2.6}),
        element("path",{d:"M "+(X(p.x)-5)+" "+Y(p.y)+" h10 M "+X(p.x)+" "+(Y(p.y)-5)+" v10",
          fill:"none",stroke:stage==="raw"?"#738998":col[i],"stroke-width":2})
      );
    });
  });

  // Sticky active-section navigation for desktop, compact collapsible mobile TOC.
  const toc=document.querySelector(".course-sidebar .toc-panel");
  if(toc){
    const mobile=window.matchMedia("(max-width:680px)");
    const syncToc=()=>{toc.open=!mobile.matches;};
    syncToc();
    mobile.addEventListener?.("change",syncToc);
    toc.querySelectorAll('a[href^="#"]').forEach(link=>{
      link.addEventListener("click",()=>{if(mobile.matches)toc.open=false;});
    });
    const ids=["one","two","three","four","five"];
    const sections=ids.map(id=>document.getElementById(id)).filter(Boolean);
    const navLinks=sections.map(el=>toc.querySelector('a[href="#'+el.id+'"]'));
    let scheduled=false;
    const update=()=>{
      scheduled=false;
      let active=0;
      sections.forEach((section,i)=>{
        if(section.getBoundingClientRect().top<=160)active=i;
      });
      navLinks.forEach((link,i)=>{
        if(link){
          if(active===i)link.setAttribute("aria-current","location");
          else link.removeAttribute("aria-current");
        }
      });
    };
    window.addEventListener("scroll",()=>{
      if(!scheduled){scheduled=true;window.requestAnimationFrame(update);}
    },{passive:true});
    update();
  }
})();
