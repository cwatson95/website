
/* ============ UI drive test for quantum-coin-toss.html ==================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/wave-on-a-string ->
 * build/quantum-measurement).  The three sim-specific thresholds: chip rows by
 * exact label AND arity; 7 panel groups; 8 inputs (7 sliders, 1 checkbox).
 * Clicks and flips are tested THROUGH the frame loop from a proven-idle
 * baseline; buttons are found only when visible (ancestors included). */
ObjC.import('Foundation');
let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };
function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);}, arc(x,y,r){c._p&&c._p.push([x,y,r]);},
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); }, stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h]);}, strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
    fillText(t,x,y){ops.push(['t',String(t),Math.round(x),Math.round(y)]);}, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||''); return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
    createLinearGradient(){return {addColorStop(){}};},
  };
  Object.defineProperty(c,'font',{get:()=>st.font,set:v=>st.font=v});
  for(const k of ['fillStyle','strokeStyle','lineWidth','globalAlpha','textAlign','textBaseline','lineJoin','lineCap'])
    Object.defineProperty(c,k,{get:()=>st[k],set:v=>st[k]=v});
  return c;
}
const sigU=c=>JSON.stringify(c.ops).length+':'+c.ops.length;
const geomU=c=>JSON.stringify(c.ops.filter(o=>o[0]!=='t'));
const entReU=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
function assertCleanU(rec,label){
  let bad=null;
  for(const o of rec.ops) if(o[0]==='t'){
    if(entReU.test(o[1])){ bad='entity/tag "'+String(o[1]).slice(0,40)+'"'; break; }
    if(/NaN|undefined|Infinity/.test(o[1])){ bad='NaN/undefined "'+String(o[1]).slice(0,40)+'"'; break; } }
  uok(!bad,label+' text ops clean'+(bad?' ('+bad+')':''));
}
let RECU=makeRecU();
function mkElU(tag){
  const e={tagName:(tag||'div').toUpperCase(),children:[],style:{},dataset:{},
    _h:{},className:'',id:'',value:'0',checked:false,hidden:false,disabled:false,textContent:'',
    appendChild(c){ this.children.push(c); c.parentNode=this;
      if(c&&c.nodeType===3) this.textContent=(this.textContent||'')+c.textContent;
      else if(c&&c.textContent) this.textContent=(this.textContent||'')+c.textContent;
      return c; },
    setAttribute(k,v){ this[k]=v; },
    addEventListener(k,f){ (this._h[k]=this._h[k]||[]).push(f); },
    removeEventListener(){}, setPointerCapture(){}, releasePointerCapture(){},
    classList:{_on:{},add(c){this._on[c]=1;},remove(c){delete this._on[c];},toggle(c){this._on[c]?delete this._on[c]:this._on[c]=1;},contains(c){return !!this._on[c];}},
    getBoundingClientRect(){ return {left:0,top:0,width:1400,height:820}; },
    getContext(){ return RECU; },
    querySelector(s){ return this._find(s)[0]||null; }, querySelectorAll(s){ return this._find(s); },
    _find(s){ const out=[]; const want=(s||'').trim();
      const walk=n=>{ for(const ch of n.children||[]){
        if(want==='#info'&&ch.id==='info') out.push(ch); else if(want==='#phys'&&ch.id==='phys') out.push(ch);
        else if(want==='.chips'&&ch.className==='chips') out.push(ch); else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  let _html='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },set(v){ _html=''+v; e.textContent=(''+v).replace(/<[^>]*>/g,''); }});
  return e;
}
const NODESU={};
for(const id of ['scene','panel','tabs','readout','eqbar','tag','hint','errbox','sub']) NODESU[id]=mkElU(id==='scene'?'canvas':'div'), NODESU[id].id=id;
globalThis.document={readyState:'complete',getElementById:id=>NODESU[id]||null,createElement:mkElU,
  createTextNode:t=>({nodeType:3,textContent:''+t,children:[]}),addEventListener(){}};
const WINHU={}; let RAFU=null;
globalThis.window={devicePixelRatio:1,addEventListener(k,f){ (WINHU[k]=WINHU[k]||[]).push(f); },requestAnimationFrame(f){ RAFU=f; return 1; }};
globalThis.requestAnimationFrame=f=>{ RAFU=f; return 1; };
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function walkU(fn){ const w=n=>{ for(const ch of n.children||[]){ fn(ch); w(ch); } }; w(NODESU.panel); }
function findLabelledU(needle){ let hit=null; walkU(ch=>{ if(!hit&&ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2; }); return hit; }
function sliderRowU(label){ let hit=null; walkU(ch=>{ if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch; }); return hit; }
function sliderU(label){ const r=sliderRowU(label); return r?r.children[1]:null; }
function chipU(label,arity){ let hit=null; walkU(ch=>{ if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c; }); return hit; }
function buttonU(needle){ let hit=null;
  const w=(n,vis)=>{ for(const ch of n.children||[]){ const v=vis&&!ch.hidden; if(v&&ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; w(ch,v); } };
  w(NODESU.panel,true); return hit; }
function clickU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function animatesU(label){ pumpU(1); RECU=makeRecU(); pumpU(1); const a=geomU(RECU); RECU=makeRecU(); pumpU(1); const b=geomU(RECU);
  uok(a.length>50&&b.length>50&&a!==b,label+' (two consecutive animation frames, BOTH drawn, and different; the dirty repaint drained first)'); }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function setSliderU(label,v){ const s=sliderU(label); if(!s) return false; s.value=String(v); s.fire('input'); return true; }
function checkU(label,on){ const c=findLabelledU(label); if(!c) return false; if(c.checked!==on){ c.checked=on; c.fire('change'); } return true; }
function geoU(){ return viewGeo(RECU,1400,820,buildModel()); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the classical coin|the quantum coin|the binomial|the hidden difference','the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===7,'the control panel has its 7 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.view==='classical'&&COINS.classical.preparing,'PhET\'s start: the classical coin, being prepared');
const FLOORSU=[10,10,50,60], sigsU={};
for(let i=0;i<4;i++){ RECU=makeRecU(); tabU(i); uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error'); assertCleanU(RECU,'tab '+i); sigsU['t'+i]=sigU(RECU); }
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');
for(let i=0;i<4;i++){ tabU(i); idleU('tab '+i+' is idle when nothing moves'); }

/* ---- the classical coin ---- */
tabU(0); idleU('classical idle');
{ uok(!buttonU('flip'),'no flip button while preparing'); uok(chipU('↑',2).parentNode.hidden===true,'the basis chips are hidden on the classical tab');
  chipU('10',3).fire('click'); uok(COINS.classical.set.n===10,'10 identical coins chosen while preparing'); chipU('100',3).fire('click');
  uok(clickU('send to measure'),'found "send to measure"'); uok(!COINS.classical.preparing&&COINS.classical.single.state==='revealed','the coins arrive showing heads');
  idleU('arrived: idle');
  clickU('flip'); animatesU('a flip animates through the frame loop');
  uok(buttonU('flip').disabled===true,'the buttons are disabled while it flips'); pumpU(70);
  uok(COINS.classical.single.state==='hidden','after 1 s the face is hidden'); uok(buttonU('flip').disabled===false,'and the panel resyncs');
  idleU('the flip is over: idle');
  const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.single.cx,clientY:G.single.cy}); NODESU.scene.fire('pointerup',{});
  uok(COINS.classical.single.state==='revealed','clicking the coin reveals it'); RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the click repaints through the loop'); idleU('then idle');
  clickU('hide'); uok(COINS.classical.single.state==='hidden','hide'); clickU('reveal'); uok(COINS.classical.single.state==='revealed','reveal');
  clickU('flip and reveal'); pumpU(70); uok(COINS.classical.single.nObs>=3,'flip and reveal records another outcome');
  clickU('flip and reveal all'); pumpU(70); uok(COINS.classical.set.state==='revealed','flip and reveal all'); clickU('hide all'); uok(COINS.classical.set.state==='hidden','hide all');
  clickU('reveal all'); clickU('flip all'); pumpU(70); uok(COINS.classical.set.state==='hidden','flip all');
  setSliderU('P(heads)',0.33); uok(Math.abs(COINS.classical.p-0.35)<1e-12,'the bias snaps to 0.05');
  clickU('new coin'); uok(COINS.classical.preparing,'new coin'); checkU('classical coins start hidden',true); clickU('send to measure');
  uok(COINS.classical.single.state==='hidden','start hidden: the coins arrive under the cup'); checkU('classical coins start hidden',false); clickU('new coin');
  chipU('tails',2).fire('click'); clickU('send to measure'); uok(COINS.classical.set.kUp===0,'prepared tails, they arrive tails'); clickU('new coin'); chipU('heads',2).fire('click'); }
/* ---- the quantum coin ---- */
tabU(1); idleU('quantum idle');
{ uok(chipU('↑',2).parentNode.hidden===false&&chipU('heads',2).parentNode.hidden===true,'the quantum tab swaps the orientation chips for basis states');
  uok(!!sliderU('P(↑) = |α|²'),'its slider is P(up) = |alpha|^2'); uok(findLabelledU('classical coins start hidden').parentNode.parentNode.hidden===true,'and hides the classical preference (its row: input, label, row)');
  chipU('↑',2).fire('click'); uok(COINS.quantum.p===1,'up sets |alpha|^2 = 1'); setSliderU('P(↑) = |α|²',0.5); uok(quantumInit(COINS.quantum.p)==='superposition','0.5: a superposition');
  uok(COINS.classical.p===0.35,'and the classical scene kept its own bias (separate scenes, PhET)');
  clickU('send to measure'); uok(COINS.quantum.single.state==='ready','a quantum coin arrives unobserved');
  const s0=COINS.quantum.R.s; clickU('observe'); uok(COINS.quantum.R.s!==s0&&COINS.quantum.single.state==='revealed','observe collapses it (a draw)');
  const v=COINS.quantum.single.vals[0]; clickU('hide'); clickU('observe'); uok(COINS.quantum.single.vals[0]===v,'observed again: the same face');
  clickU('reprepare'); pumpU(70); uok(COINS.quantum.single.state==='ready','reprepared: unobserved again');
  idleU('proven idle before the click');
  const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.single.cx,clientY:G.single.cy}); NODESU.scene.fire('pointerup',{});
  uok(COINS.quantum.single.state==='revealed','clicking the quantum coin observes it'); RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'repainted through the loop');
  clickU('reprepare and observe all'); pumpU(70); uok(COINS.quantum.set.state==='revealed','reprepare and observe all'); clickU('new coin'); }
/* ---- the binomial and the hidden difference ---- */
tabU(2); idleU('binomial idle');
{ chipU('N = 10',3).fire('click'); uok(ST.binN===10,'N = 10'); setSliderU('bias p',0.65); setSliderU('sets M',3000); setSliderU('seed ',73);
  uok(ST.binP===0.65&&ST.binM===3000&&ST.binSeed===73,'the binomial sliders'); uok(NODESU.readout.innerHTML.indexOf('6.4983')>=0,'the readout prints the derive-pinned mean 6.4983'); }
tabU(3); idleU('hidden difference idle');
{ setSliderU('bias p = P(up)',0.5); setSliderU('coins of each kind',2000); setSliderU('seed',21);
  uok(ST.mixP===0.5&&ST.mixShots===2000&&ST.mixSeed===21,'the hidden-difference sliders'); uok(NODESU.readout.innerHTML.indexOf('1.000, ')<0&&NODESU.readout.innerHTML.indexOf('1.0000')>=0,'P(+x) = 1.0000 for the superposition at p = 1/2');
  idleU('slider repaints drained'); NODESU.scene.fire('pointerdown',{clientX:400,clientY:300}); RECU=makeRecU(); pumpU(2); uok(geomU(RECU)==='[]','the view ignores the pointer'); NODESU.scene.fire('pointerup',{}); }
/* ---- keyboard ---- */
keyU('1'); uok(ST.view==='classical','1 is the classical coin'); keyU('4'); uok(ST.view==='mix','4 the hidden difference'); keyU('2'); uok(ST.view==='quantum','2 the quantum coin');
/* ---- every control, every tab, resize, reset all against disturbed state ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===8,'the panel has its 7 sliders and 1 checkbox ('+inputs.length+')');
  for(let v=0;v<4;v++){ tabU(v);
    for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max); for(const x of [lo,hi,(lo+hi)/2]){ inp.value=String(x); inp.fire('input'); } }
    uok(NODESU.errbox.style.display!=='block','every input at its ends and middle draws without error on tab '+v);
    RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  tabU(1); ST.binN=10; ST.mixP=0.1; COINS.quantum.p=0.2; sceneStart(COINS.quantum); COINS.classical.init='tails';
  uok(clickU('reset all'),'found reset all');
  uok(ST.binN===100&&ST.mixP===0.7&&COINS.quantum.p===0.5&&COINS.quantum.preparing&&COINS.classical.init==='heads','reset all restores PhET\'s defaults and both scenes');
  uok(ST.view==='quantum','keeping the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
