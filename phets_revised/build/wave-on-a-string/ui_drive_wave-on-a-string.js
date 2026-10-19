
/* ============ UI drive test for wave-on-a-string.html ===================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js).
 * The three sim-specific thresholds: the chip rows are found by exact label
 * AND arity (3 modes, 3 ends, 2 speeds); the panel has 7 groups; 10 inputs
 * (6 sliders, 4 checkboxes).  Every drag is tested THROUGH the frame loop
 * from a proven-idle baseline (paused), and every reset against a sentinel. */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},
    lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);},
    arc(x,y,r){c._p&&c._p.push([x,y,r]);},
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
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
const textU=c=>c.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' | ');
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
    appendChild(c){ this.children.push(c);
      if(c&&c.nodeType===3) this.textContent=(this.textContent||'')+c.textContent;
      else if(c&&c.textContent) this.textContent=(this.textContent||'')+c.textContent;
      return c; },
    setAttribute(k,v){ this[k]=v; },
    addEventListener(k,f){ (this._h[k]=this._h[k]||[]).push(f); },
    removeEventListener(){}, setPointerCapture(){}, releasePointerCapture(){},
    classList:{_on:{},add(c){this._on[c]=1;},remove(c){delete this._on[c];},
               toggle(c){this._on[c]?delete this._on[c]:this._on[c]=1;},contains(c){return !!this._on[c];}},
    getBoundingClientRect(){ return {left:0,top:0,width:1400,height:820}; },
    getContext(){ return RECU; },
    querySelector(s){ return this._find(s)[0]||null; },
    querySelectorAll(s){ return this._find(s); },
    _find(s){ const out=[]; const want=(s||'').trim();
      const walk=n=>{ for(const ch of n.children||[]){
        if(want==='#info'&&ch.id==='info') out.push(ch);
        else if(want==='#phys'&&ch.id==='phys') out.push(ch);
        else if(want==='.chips'&&ch.className==='chips') out.push(ch);
        else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  /* a real browser derives textContent from innerHTML; the shared stub did not (Known-bad) */
  let _html='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },set(v){ _html=''+v; e.textContent=(''+v).replace(/<[^>]*>/g,''); }});
  return e;
}
const NODESU={};
for(const id of ['scene','panel','tabs','readout','eqbar','tag','hint','errbox','sub'])
  NODESU[id]=mkElU(id==='scene'?'canvas':'div'), NODESU[id].id=id;
globalThis.document={readyState:'complete',getElementById:id=>NODESU[id]||null,createElement:mkElU,
  createTextNode:t=>({nodeType:3,textContent:''+t,children:[]}),addEventListener(){}};
const WINHU={}; let RAFU=null;
globalThis.window={devicePixelRatio:1,addEventListener(k,f){ (WINHU[k]=WINHU[k]||[]).push(f); },requestAnimationFrame(f){ RAFU=f; return 1; }};
globalThis.requestAnimationFrame=f=>{ RAFU=f; return 1; };
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
function sliderU(label){ let hit=null;   /* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const rc=findLabelledU('time runs'); if(rc.checked){ rc.checked=false; rc.fire('change'); } }
function playU(){ const rc=findLabelledU('time runs'); if(!rc.checked){ rc.checked=true; rc.fire('change'); } }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the string|the space-time|the reflections|the standing waves|the dispersion','the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===7,'the control panel has its 7 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('6.250 cm/s')>=0,'the readout prints v = 6.250 cm/s off the model');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.mode==='manual'&&ST.end==='fixed'&&ST.running===true,'PhET\'s start: manual, fixed end, playing');

/* ---- every tab draws, differently, cleanly (floors from the t = 0 emission) ---- */
const FLOORSU=[12,6,30,30,25];
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');

/* ---- paused, every view idles; the dispersion view idles even when running ---- */
pauseU(); uok(ST.running===false,'the "time runs" box pauses');
for(let i=0;i<5;i++){ tabU(i); idleU('tab '+i+' paints nothing while paused'); }
playU(); tabU(4); idleU('the dispersion view is static: nothing to paint while time runs');

/* ---- the string runs through the frame loop ---- */
tabU(0);
{ const oc=chipU('oscillate',3); uok(!!oc,'found the oscillate chip'); oc.fire('click'); uok(ST.mode==='osc','oscillate selected'); }
RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
uok(gA.length>50&&gB.length>50&&gA!==gB,'two pumped frames draw DIFFERENT pictures (the oscillator drives the string)');
{ const s0=LIVE.lat.steps; pumpU(25); uok(LIVE.lat.steps>s0+15,'25 frames of 16 ms advance the lattice ~20 steps ('+(LIVE.lat.steps-s0)+')');
  const ro0=NODESU.readout.innerHTML; pumpU(10); uok(NODESU.readout.innerHTML!==ro0,'the readout refreshes while it runs'); }
/* the mode chip restarts the string (PhET), checked against a sentinel */
{ pumpU(10); uok(LIVE.lat.steps>0,'sentinel: the string has run'); const mc=chipU('manual',3); mc.fire('click');
  uok(ST.mode==='manual'&&LIVE.lat.steps===0,'switching the mode restarts the string, as PhET does'); }
/* slow motion runs at a quarter of the rate */
{ const sc=chipU('slow motion',2); uok(!!sc,'found the slow-motion chip'); const oc=chipU('oscillate',3); oc.fire('click');
  const n0=LIVE.lat.steps; pumpU(2); const t0=LIVE.t+LIVE.acc; pumpU(40); const tn=LIVE.t+LIVE.acc; uok(Math.abs((tn-t0)-40*0.016)<1e-6,'normal speed: 40 frames = 0.64 s simulated');
  sc.fire('click'); uok(ST.speed==='slow','slow motion selected'); pumpU(1); const t1=LIVE.t+LIVE.acc; pumpU(40); const t2=LIVE.t+LIVE.acc;
  uok(Math.abs((t2-t1)-40*0.016*0.25)<1e-6,'slow motion: 40 frames = 0.16 s simulated (x0.25)'); chipU('normal',2).fire('click'); uok(ST.speed==='normal','back to normal'); }

/* ---- the step button and the step key: exactly one lattice step ---- */
pauseU(); idleU('paused before stepping');
{ LIVE.acc=0.011; const n0=LIVE.lat.steps; uok(clickButtonU('step'),'found the step button'); uok(LIVE.lat.steps===n0+1,'step takes exactly one lattice step');
  uok(LIVE.acc===0,'from a clean phase (the frame clock\'s half-step is dropped)');
  keyU('.'); uok(LIVE.lat.steps===n0+2,'the . key steps too'); idleU('and the loop is idle again after the step repaint'); }
/* restart string, against a sentinel */
{ uok(LIVE.lat.steps>0,'sentinel: steps > 0'); uok(clickButtonU('restart string'),'found restart string'); uok(LIVE.lat.steps===0&&LIVE.hist.length===0,'restart string zeroes the lattice and the record');
  keyU('.'); keyU('.'); keyU('r'); uok(LIVE.lat.steps===0,'the r key restarts too'); }

/* ---- a live but ignored control is hidden (Known-bad) ---- */
{ const row=k=>sliderU(k).parentNode||null; const vis=lab=>{ let hid=null; const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='sliderrow'&&ch.children[0].textContent===lab) hid=ch.hidden; walk(ch); } }; walk(NODESU.panel); return hid===false; };
  chipU('manual',3).fire('click'); uok(!vis('frequency, Hz')&&!vis('pulse width, s')&&!vis('amplitude, cm'),'manual: amplitude, frequency and pulse width are hidden');
  chipU('oscillate',3).fire('click'); uok(vis('frequency, Hz')&&vis('amplitude, cm')&&!vis('pulse width, s'),'oscillate: amplitude and frequency show');
  chipU('pulse',3).fire('click'); uok(!vis('frequency, Hz')&&vis('pulse width, s'),'pulse: pulse width shows, frequency hides'); }

/* ---- the REAL drag: the wrench, from a proven-idle baseline ---- */
chipU('manual',3).fire('click'); pauseU(); idleU('manual, paused: idle before the wrench');
{ const G=strGeo(RECU,1400,820,buildModel()), map=G.map, X=map.X(-0.7), Y=map.Y(0);
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y});
  uok(DRAG.what==='wrench','pointer-down ON the wrench grabs it');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the grab repaints through the loop (the wrench hints go)');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  RECU=makeRecU(); pumpU(1); const before=geomU(RECU);
  uok(before==='[]','still idle immediately before the move');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:map.Y(0.9),buttons:1});
  uok(Math.abs(LIVE.wr-0.9)<1e-9,'the move set the wrench to 0.9 cm');
  uok(ST.running===true,'dragging the wrench presses play, as in PhET');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); RECU=makeRecU(); pumpU(4); const g2=geomU(RECU);
  uok(g1.length>50&&g2.length>50&&g1!==g2,'the move repaints THROUGH the frame loop, and the kink then runs on');
  uok(LIVE.lat.cur[0]>0.5,'bead 0 followed the wrench ('+fmt(LIVE.lat.cur[0],3)+' cm)');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:map.Y(-0.9),buttons:0}); uok(Math.abs(LIVE.wr-0.9)<1e-9,'a hover with no button pressed moves nothing'); }
/* the arrow keys move the wrench */
{ const w0=LIVE.wr; keyU('ArrowDown'); uok(Math.abs(LIVE.wr-(w0-0.1))<1e-9,'the down arrow lowers the wrench 1 mm'); keyU('ArrowUp'); keyU('ArrowUp'); uok(Math.abs(LIVE.wr-(w0+0.1))<1e-9,'the up arrow raises it'); }

/* ---- PhET's tools: each drag moves the drawing through the loop, paused ---- */
clickButtonU('restart string'); pauseU();
for(const [lbl,key] of [['rulers','rulers'],['stopwatch','stopwatch'],['reference line','refline']]){
  const cb=findLabelledU(lbl); uok(!!cb,'found the '+lbl+' checkbox'); RECU=makeRecU(); cb.checked=true; cb.fire('change');
  uok(ST[key]===true,lbl+' switched on'); uok(RECU.ops.length>30,'and the view redrew at once'); }
uok(textU(RECU).indexOf('stopwatch')>=0&&textU(RECU).indexOf('reference line')>=0&&textU(RECU).indexOf('cm')>=0,'the three tools are on the canvas');
idleU('tools on, paused: idle');
{ const G=strGeo(RECU,1400,820,buildModel()), map=G.map;
  const drags=[['rh',map.X(ST.rhX+5),map.Y(ST.rhY-0.25),60,0,()=>ST.rhX],['rv',map.X(ST.rvX+0.25),map.Y(ST.rvY+1),0,-40,()=>ST.rvY],
               ['ref',map.X(3),map.Y(ST.refY)+1,0,30,()=>ST.refY],['sw',swRect(map,ST,1400,820).x+30,swRect(map,ST,1400,820).y+30,-80,40,()=>ST.swX]];
  for(const [what,x,y,dx,dy,get] of drags){
    idleU(what+': proven idle before the grab');
    NODESU.scene.fire('pointerdown',{clientX:x,clientY:y}); uok(DRAG.what===what,'pointer-down grabs '+what+' ('+DRAG.what+')');
    idleU(what+': the grab\'s repaint drained');
    const v0=get(); RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:x+dx,clientY:y+dy,buttons:1});
    uok(get()!==v0,what+' moved with the pointer'); pumpU(1); uok(geomU(RECU).length>50,what+': the move repainted through the loop (dirty flag)');
    idleU(what+': and the loop goes idle again (tools do not press play)'); uok(ST.running===false,what+': still paused');
    NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,what+' released');
  } }
/* the stopwatch buttons */
{ uok(clickButtonU('start / stop'),'found start / stop'); uok(LIVE.swOn===true,'the stopwatch runs'); playU(); pumpU(20); uok(LIVE.sw>0.25,'and counts simulated time ('+fmt(LIVE.sw,3)+' s)');
  uok(clickButtonU('start / stop')&&LIVE.swOn===false,'and stops'); const s0=LIVE.sw; pumpU(5); uok(LIVE.sw===s0,'stopped, it holds');
  uok(clickButtonU('clear')&&LIVE.sw===0,'clear zeroes it'); }

/* ---- the pulse generator: a click on the canvas sends a pulse and presses play ---- */
{ const pc=chipU('pulse',3); pc.fire('click'); uok(ST.mode==='pulse','pulse mode'); pauseU(); idleU('pulse mode, paused: idle');
  const G=strGeo(RECU,1400,820,buildModel()), map=G.map;
  NODESU.scene.fire('pointerdown',{clientX:map.X(-0.9),clientY:map.Y(0)}); NODESU.scene.fire('pointerup',{});
  uok(LIVE.pulseOn===true,'clicking the generator sends a pulse'); uok(ST.running===true,'and presses play');
  RECU=makeRecU(); pumpU(10); uok(geomU(RECU).length>50,'the pulse runs through the loop');
  uok(!!buttonU('send a pulse'),'the send-a-pulse button exists'); const busy=LIVE.pulseOn; clickButtonU('send a pulse'); uok(LIVE.pulseOn===busy,'the button does nothing while a pulse is being sent');
  pumpU(60); uok(LIVE.pulseOn===false,'the generator is done after w'); keyU('p'); uok(LIVE.pulseOn===true,'the p key sends the next one'); }

/* ---- the far end: the fixed-end chip zeroes bead 60, checked against a sentinel ---- */
{ const lc=chipU('loose end',3); lc.fire('click'); uok(ST.end==='loose','loose end selected');
  LIVE.lat.cur[NSEG]=0.5; LIVE.lat.prev[NSEG]=0.5; const fc=chipU('fixed end',3); fc.fire('click');
  uok(ST.end==='fixed'&&LIVE.lat.cur[NSEG]===0&&LIVE.lat.prev[NSEG]===0,'switching to the fixed end zeroes bead 60 at once (PhET)');
  chipU('no end',3).fire('click'); uok(ST.end==='none','no end selected'); RECU=makeRecU(); tabU(0); uok(RECU.ops.length>20,'the open end draws');
  uok(NODESU.readout.innerHTML.indexOf('leaks')>=0,'the readout reports the absorber\'s leak'); chipU('fixed end',3).fire('click'); }

/* ---- the space-time view fills as the string runs ---- */
tabU(1); pauseU(); clickButtonU('restart string'); RECU=makeRecU(); tabU(1);
uok(textU(RECU).indexOf('nothing recorded yet')>=0,'an empty record says so');
chipU('oscillate',3).fire('click'); playU(); pumpU(120); RECU=makeRecU(); pumpU(1);
uok(RECU.ops.filter(o=>o[0]==='f').length>=6,'after 120 frames the space-time is painted (batched fills)'); uok(LIVE.hist.length>80,'from '+LIVE.hist.length+' recorded levels');

/* ---- the reflections: whole steps, looping ---- */
tabU(2); pauseU(); idleU('reflections, paused: idle');
{ const n0=REFL.n; clickButtonU('step'); uok(REFL.n===n0+1,'step advances the demo one lattice step'); playU(); pumpU(60); uok(REFL.n>n0+30,'the demo runs ('+REFL.n+')');
  keyU('r'); uok(REFL.n===0,'r restarts the demo'); uok(NODESU.readout.innerHTML.indexOf('-1.000')>=0,'the readout prints r = -1.000 for the clamp'); }

/* ---- the standing waves: drag the response panel to set f ---- */
tabU(3); pauseU(); idleU('standing waves, paused: idle');
{ const tb=standGeo(RECU,1400,820).tb, f0=ST.freq;
  NODESU.scene.fire('pointerdown',{clientX:tb.x+tb.w*(1.25/3),clientY:tb.y+tb.h/2}); uok(DRAG.what==='freq','pointer-down on the response panel grabs f');
  uok(Math.abs(ST.freq-1.25)<1e-12&&ST.freq!==f0,'and sets f = 1.25 Hz, the third resonance');
  idleU('the grab repaint drained');
  RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:tb.x+tb.w*(1.5/3),clientY:tb.y+tb.h/2,buttons:1}); pumpU(1);
  uok(Math.abs(ST.freq-1.5)<1e-12,'dragging sets 1.5 Hz'); uok(geomU(RECU).length>50,'and repaints through the loop'); NODESU.scene.fire('pointerup',{});
  const ds=sliderU('damping'); ds.value='0.02'; ds.fire('input'); const fs=sliderU('frequency, Hz'); fs.value='1.25'; fs.fire('input');
  uok(NODESU.readout.innerHTML.indexOf('8.355')>=0,'at 1.25 Hz and damping 0.02 the readout gives the 8.355 A resonance');
  playU(); const n0=STAND.n; pumpU(30); uok(STAND.n>n0,'the run builds up from rest'); }

/* ---- the dispersion: the alpha slider moves the green curve at once ---- */
tabU(4); idleU('dispersion idle');
{ const as=sliderU('Courant number α'); uok(!!as,'found the Courant-number slider'); RECU=makeRecU(); as.value='0.5'; as.fire('input');
  uok(ST.alpha===0.5,'alpha = 0.5'); uok(RECU.ops.length>40,'the view redrew at once ('+RECU.ops.length+' ops)'); const g5=geomU(RECU);
  RECU=makeRecU(); as.value='1'; as.fire('input'); uok(geomU(RECU)!==g5,'and alpha = 1 draws a different picture');
  uok(NODESU.readout.innerHTML.indexOf('(PhET)')>=0,'alpha = 1 is labelled PhET\'s'); }

/* ---- the pointer is ignored where nothing is draggable ---- */
for(const i of [1,2,4]){ tabU(i); pauseU(); idleU('tab '+i+' idle'); NODESU.scene.fire('pointerdown',{clientX:400,clientY:300}); NODESU.scene.fire('pointermove',{clientX:600,clientY:340,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','tab '+i+' ignores the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- keyboard: views and play/pause ---- */
keyU('1'); uok(ST.view==='str','1 is the string'); keyU('5'); uok(ST.view==='disp','5 the dispersion'); keyU('3'); uok(ST.view==='refl','3 the reflections');
{ const r0=ST.running; keyU(' '); uok(ST.running===!r0,'space toggles play'); keyU(' '); uok(ST.running===r0,'and back'); }

/* ---- every control, every tab, resize, reset all against disturbed state ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===10,'the panel has its 6 sliders and 4 checkboxes ('+inputs.length+')');
  for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); } }
  for(let v=0;v<5;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb every kind of state reset all claims to restore */
  tabU(0); chipU('oscillate',3).fire('click'); chipU('loose end',3).fire('click'); chipU('slow motion',2).fire('click');
  ST.rulers=true; ST.stopwatch=true; ST.refline=true; ST.rhX=2; ST.rvY=-1; ST.refY=0.3; ST.swX=5; ST.alpha=0.4; ST.amp=1.2; ST.tension=0.1; ST.damping=0.7;
  LIVE.sw=3.3; LIVE.swOn=true; LIVE.arrows=false; pumpU(5); uok(LIVE.lat.steps>0,'sentinel: the string is running');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.mode==='manual'&&ST.end==='fixed'&&ST.speed==='normal'&&ST.amp===0.75&&ST.tension===0.8&&ST.damping===0.2&&ST.alpha===1,'reset all restores PhET\'s defaults');
  uok(!ST.rulers&&!ST.stopwatch&&!ST.refline&&ST.rhX===0&&ST.rvY===-2.5&&ST.refY===1.45&&ST.swX===0.3,'and the tools, hidden and home');
  uok(LIVE.sw===0&&LIVE.swOn===false&&LIVE.arrows===true&&LIVE.lat.steps===0,'and the stopwatch, the wrench hints and the string');
  uok(ST.view==='str','keeping the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
