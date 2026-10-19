/* ============ UI drive test for waves-intro.html ========================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js via
 * build/wave-interference/ui_drive_wave-interference.js, which carries the
 * innerHTML -> textContent fix).  The three medium views animate, so every
 * idle-first test PAUSES the clock first; the three-media view never animates.
 * Three custom pointer actions (PhET's generator button, a tape end, a wave-
 * meter probe), every tab, every visible slider at its ends, every checkbox,
 * every chip, every button, the keys, resize, the tone's audio layer against a
 * stub AudioContext, and reset-all against a fully disturbed state.           */
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
    fill(){ if(c._p&&c._p.length) ops.push(['f',String(st.fillStyle)].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h,String(st.fillStyle)]);}, strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
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
const textsU=c=>c.ops.filter(o=>o[0]==='t').map(o=>o[1]);
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
/* a stub AudioContext: the tone's samples are computed by the sim, so the harness can check
   exactly what would be played without any audio hardware */
const ALOG={ctx:0,buffers:[],started:0,stopped:0,gain:null,last:null};
globalThis.AudioContext=function(){
  ALOG.ctx++;
  this.sampleRate=44100; this.state='running'; this.currentTime=0; this.destination={};
  this.createGain=()=>{ const g={gain:{value:-1},connect(){}}; ALOG.gain=g; return g; };
  this.createBuffer=(ch,len,sr)=>{ const d=new Float32Array(len);
    const b={length:len,sampleRate:sr,numberOfChannels:ch,getChannelData:()=>d}; ALOG.buffers.push(b); return b; };
  this.createBufferSource=()=>{ const s={buffer:null,loop:false,connect(){},
    start(){ ALOG.started++; ALOG.last=s; },stop(){ ALOG.stopped++; }}; return s; };
  this.resume=()=>{};
};
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
/* three sliders are labelled "amplitude", one per medium, and only the current view's is on
   show: take the VISIBLE one (Known-bad: a finder that matches on a label finds the wrong
   control when several share it) */
function sliderU(needle){ const all=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) all.push(ch);
    walk(ch); } };
  walk(NODESU.panel);
  const shown=all.filter(r=>!r.hidden);
  return (shown[0]||all[0]||{children:[]}).children[1]||null; }
function rowOf(inp){ let hit=null; const walk=n=>{ for(const ch of n.children||[]){ if(ch.children&&ch.children.indexOf(inp)>=0) hit=ch; walk(ch); } }; walk(NODESU.panel); return hit; }
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
function isShown(el){ const chain=[];
  const walk=p=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
function pause(){ if(ST.running) keyU(' '); }
function genU(){ const M=buildModel(), G=latGeo(RECU,1400,820,M); return {G,g:genGeo(G.sq,M.L.R),sq:G.sq}; }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.panel.children.length===7,'the control panel has its seven groups ('+NODESU.panel.children.length+')');
uok(RO().length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').indexOf('&lambda; = v/f')>=0,'the equation bar carries λ = v/f, no NaN');
uok(RO().indexOf('2.64 cm')>=0,'the readout prints the water wavelength 2.64 cm off the model');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
/* every control built from TEXT NODES (labels, buttons, chips, headings) must carry literal
   glyphs: a browser renders an entity written there verbatim.  The .tag and .src blocks are
   set through innerHTML, where entities are correct — and the stub does not decode them, so
   they are deliberately not walked here. */
{ const bad=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(['LABEL','BUTTON','H3'].indexOf(ch.tagName)>=0&&entReU.test(ch.textContent||'')) bad.push(ch.tagName+': '+ch.textContent);
    walk(ch); } };
  walk(NODESU.panel);
  uok(!bad.length,'no HTML entity reaches a label, button or heading as literal text'+(bad.length?' ('+bad[0]+')':'')); }

/* ---- every tab draws, differently, cleanly ---- */
pause();
/* 70 % of what each tab emits at 1400 x 820 on its FIRST draw, which is a tank with no waves in
   it yet — a floor taken from a running tank would punish a view for starting honestly, and one
   taken from a field's colour classes would punish these views for batching (TABOPS 16, 18, 21,
   135 with UI_DIAG set; run: python3 jsrun.py ui_drive_waves-intro.js osa nosuite diag) */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[11,12,14,94];
const sigsU={};
for(let i=0;i<4;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while paused / static');
}
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');

/* ---- the clock: PhET's event rate, and only on a medium view ---- */
tab(0); keyU(' '); uok(ST.running,'space starts the clock');
{ const n0=RUNS.water.n; RECU=makeRecU(); pumpU(60);
  uok(RUNS.water.n-n0>=35&&RUNS.water.n-n0<=37,'sixty frames advance the tank 36 steps at PhET’s 20·111/61 per second ('+(RUNS.water.n-n0)+')');
  uok(RECU.ops.length>60,'and the loop repaints as it runs');
  chipU('slow',2).fire('click'); const n1=RUNS.water.n; pumpU(60);
  uok(RUNS.water.n-n1>=17&&RUNS.water.n-n1<=19,'slow runs at half that ('+(RUNS.water.n-n1)+')');
  chipU('normal',2).fire('click'); uok(chipU('normal',2).className==='chip on','the normal chip lights');
  keyU(' '); uok(!ST.running,'space pauses'); const n2=RUNS.water.n; pumpU(20); uok(RUNS.water.n===n2,'paused: no steps');
  idleU('paused: the tank paints nothing');
  const cb=findLabelledU('time runs'); uok(!!cb&&cb.checked===false,'the "time runs" box follows the key');
  RECU=makeRecU(); clickButtonU('one step'); uok(RUNS.water.n===n2+1,'one step is exactly one lattice step');
  uok(RECU.ops.length>20,'and repaints at once');
  tab(3); const n3=RUNS.water.n; ST.running=true; pumpU(20); uok(RUNS.water.n===n3,'the three-media view does not run the tank');
  ST.running=false; tab(0); }
runFor('water',200);

/* ---- a slider with the full treatment: proven idle, fire, drawn at once ---- */
idleU('idle before the slider test');
{ const s=sliderU('frequency (drip rate), Hz'); uok(!!s&&isShown(s),'the water frequency slider is on show');
  RECU=makeRecU(); s.value='0.9'; s.fire('input');
  uok(Math.abs(ST.f_water-0.9)<1e-12&&Math.abs(RUNS.water.f-0.9)<1e-12,'it sets 0.9 Hz on the run');
  uok(RECU.ops.length>30,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(RO().indexOf('1.83 cm')>=0,'the readout follows: λ = 1.65/0.9 = 1.83 cm');
  uok(RUNS.water.lat.u.some(v=>v!==0),'a new water frequency keeps the waves (PhET)');
  const a=sliderU('amplitude'); uok(!!a&&isShown(a),'the amplitude slider is on show');
  a.value='3'; a.fire('input'); uok(RUNS.water.A===3,'amplitude 3 reaches the run');
  a.value='8'; a.fire('input'); }

/* ---- custom action 1: PhET's generator button, through the frame loop ---- */
{ idleU('idle before the button');
  const {g}=genU();
  uok(sourceActive(RUNS.water),'the source is running');
  NODESU.scene.fire('pointerdown',{clientX:g.btn.x,clientY:g.btn.y});
  uok(!sourceActive(RUNS.water),'a click on the generator’s button switches the source off');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'and the picture is repainted through the loop');
  NODESU.scene.fire('pointerup',{});
  idleU('drained (proven idle)');
  NODESU.scene.fire('pointerdown',{clientX:g.btn.x,clientY:g.btn.y});
  uok(sourceActive(RUNS.water)&&RUNS.water.phi===0,'clicking again switches it on and restarts the phase');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU)!==gA&&geomU(RECU).length>200,'which draws a DIFFERENT picture');
  NODESU.scene.fire('pointerup',{});
  keyU('p'); uok(!sourceActive(RUNS.water),'the p key presses the same button');
  keyU('p'); uok(sourceActive(RUNS.water),'and again'); }

/* ---- custom action 2: the tape measure, dragged through the frame loop ---- */
{ const cb=findLabelledU('tape measure'); uok(!!cb,'found the tape measure box'); cb.checked=true; cb.fire('change');
  uok(ST.tape&&RO().indexOf('tape measure')>=0,'the tape measure shows in the readout');
  idleU('idle before the tape drag');
  const {sq}=genU(), a=TOOLS.tape[0];
  NODESU.scene.fire('pointerdown',{clientX:sq.x+a[0]*sq.w,clientY:sq.y+a[1]*sq.h});
  uok(DRAG.what==='tape0','pointer-down on the tape’s end grabs it');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'the grab repaints through the loop');
  idleU('and drains (proven idle)');
  NODESU.scene.fire('pointermove',{clientX:sq.x+0.1*sq.w,clientY:sq.y+0.3*sq.h,buttons:1});
  uok(Math.abs(TOOLS.tape[0][0]-0.1)<1e-12&&Math.abs(TOOLS.tape[0][1]-0.3)<1e-12,'the end follows the pointer');
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU); uok(gB.length>200&&gB!==gA,'the move repaints a DIFFERENT picture through the loop');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  const L=Math.hypot(TOOLS.tape[1][0]-0.1,TOOLS.tape[1][1]-0.3)*10;
  uok(RO().indexOf(sigf(L,3)+' cm')>=0,'the readout prints the new length '+sigf(L,3)+' cm');
  idleU('idle before the miss');
  NODESU.scene.fire('pointerdown',{clientX:sq.x+0.93*sq.w,clientY:sq.y+0.07*sq.h}); uok(DRAG.what===null,'empty water grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and paints nothing'); NODESU.scene.fire('pointerup',{}); }

/* ---- custom action 3: a wave-meter probe ---- */
{ const cb=findLabelledU('wave meter'); cb.checked=true; cb.fire('change'); uok(ST.meter,'wave meter on');
  idleU('idle before the probe drag');
  const {G,sq}=genU(), p=TOOLS.probes[1];
  uok(!!G.mb,'the meter’s chart has room at 1400 x 820');
  NODESU.scene.fire('pointerdown',{clientX:sq.x+p[0]*sq.w,clientY:sq.y+p[1]*sq.h}); uok(DRAG.what==='probe1','a probe grabs');
  pumpU(1); idleU('drained');
  NODESU.scene.fire('pointermove',{clientX:sq.x+0.8*sq.w,clientY:sq.y+0.6*sq.h,buttons:1});
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200,'the probe drag repaints through the loop');
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(TOOLS.probes[1][0]-0.8)<1e-12,'the probe moved');
  const R=RUNS.water, t0=R.trace.length; ST.running=true; pumpU(30); ST.running=false;
  uok(R.trace.length>t0&&R.trace[R.trace.length-1].length===3,'running, the meter records both probes each step'); }

/* ---- the stopwatch ---- */
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change');
  const R=RUNS.water; R.watch.t=0; clickButtonU('start / stop the stopwatch'); uok(R.watch.on,'start');
  ST.running=true; const n0=R.n; pumpU(30); ST.running=false;
  uok(Math.abs(R.watch.t-(R.n-n0)*R.dt)<1e-12,'the stopwatch counts the steps’ physical time');
  clickButtonU('start / stop the stopwatch'); uok(!R.watch.on,'stop');
  const t=R.watch.t; ST.running=true; pumpU(10); ST.running=false; uok(R.watch.t===t,'stopped, it holds');
  RECU=makeRecU(); clickButtonU('zero the stopwatch'); uok(R.watch.t===0,'zero');
  uok(textsU(RECU).some(s=>s.indexOf('stopwatch 0')===0),'and the canvas shows it'); }

/* ---- water: the side view; pulses; clear ---- */
{ runFor('water',120); idleU('idle before side view');
  RECU=makeRecU(); chipU('side view',2).fire('click'); uok(ST.look==='side','side view');
  const gs=geomU(RECU); uok(gs.length>200,'the side view draws');
  uok(textsU(RECU).some(s=>s.indexOf('Side view')>=0||s.indexOf('side view')>=0),'and says it is not to scale with the tank');
  chipU('top view',2).fire('click'); uok(ST.look==='top','back to the top view');
  chipU('pulse',2).fire('click'); uok(ST.wave==='pulse','pulse mode');
  uok(!sourceActive(RUNS.water),'which stops the source, as PhET’s disturbance-type switch does');
  clickButtonU('clear the waves'); uok(RUNS.water.lat.u.every(v=>v===0),'clear the waves empties the lattice');
  clickButtonU('press the source button'); uok(RUNS.water.pulse.on,'the button fires a pulse');
  ST.running=true; pumpU(200); ST.running=false;
  uok(!RUNS.water.pulse.on&&RUNS.water.lat.u.some(v=>Math.abs(v)>0.05),'it ends after one period and its ring travels on');
  keyU('r'); uok(RUNS.water.lat.u.every(v=>v===0),'r clears');
  chipU('continuous',2).fire('click'); uok(ST.wave==='cont','back to continuous');
  clickButtonU('press the source button'); uok(sourceActive(RUNS.water),'and the button starts it again'); }

/* ---- sound: the parcels and PhET's tone (against the stub AudioContext) ---- */
tab(1); pause();
{ uok(isShown(chipU('particles',3))&&!isShown(chipU('side view',2)),'sound shows waves / particles / both, and no side view');
  runFor('sound',150);
  RECU=makeRecU(); chipU('particles',3).fire('click'); const gp=geomU(RECU);
  RECU=makeRecU(); chipU('both',3).fire('click'); const gb=geomU(RECU);
  uok(gp!==gb&&gp.length>200,'particles and both draw different pictures');
  chipU('waves',3).fire('click');
  /* the tone plays only while the clock runs (PhET's enableControlProperties), so start it */
  keyU(' '); uok(ST.running,'the clock is running for the tone tests');
  const st0=ALOG.started, cb=findLabelledU('play tone'); uok(!!cb&&isShown(cb),'the play-tone box is on show');
  cb.checked=true; cb.fire('change');
  uok(AUDIO.state==='playing'&&ALOG.started===st0+1,'ticking it starts a tone');
  const tb=toneBuffer(1000*RUNS.sound.f,1,44100);
  uok(ALOG.buffers[ALOG.buffers.length-1].length===tb.L,'the buffer holds a whole number of cycles ('+tb.L+' samples, '+tb.m+' cycles)');
  uok(Math.abs(ALOG.gain.gain.value-0.3*RUNS.sound.A/10)<1e-12,'at PhET’s output level 0.3 A/10');
  uok(ALOG.last.loop===true,'and loops');
  { const s=sliderU('frequency (pitch), Hz'), st1=ALOG.started, sp1=ALOG.stopped;
    s.value='0.4'; s.fire('input');
    uok(ALOG.started===st1+1&&ALOG.stopped===sp1+1,'moving the pitch slider swaps the buffer');
    uok(Math.abs(ALOG.buffers[ALOG.buffers.length-1].length-toneBuffer(400,1,44100).L)<1,'for the new pitch'); }
  /* the clock stays RUNNING from here to the end of the tone tests: a tone that is already
     silent cannot be shown to be stopped by anything else (the dual of a proven-idle baseline) */
  { const sp=ALOG.stopped; keyU(' '); uok(!ST.running&&AUDIO.state==='off'&&ALOG.stopped===sp+1,'pausing the clock stops the tone');
    keyU(' '); uok(ST.running&&AUDIO.state==='playing','and starting it again resumes it'); }
  { const sp=ALOG.stopped; clickButtonU('press the source button');
    uok(!sourceActive(RUNS.sound)&&AUDIO.state==='off'&&ALOG.stopped===sp+1,'switching the source off stops the tone (PhET’s button1Pressed)');
    clickButtonU('press the source button'); uok(AUDIO.state==='playing','and on starts it'); }
  { const sp=ALOG.stopped; tab(0); uok(AUDIO.state==='off'&&ALOG.stopped===sp+1,'leaving the sound view stops it'); tab(1);
    uok(AUDIO.state==='playing','coming back starts it'); }
  findLabelledU('play tone').checked=false; findLabelledU('play tone').fire('change');
  uok(AUDIO.state==='off','and unticking the box stops it'); }

/* ---- light: the screen, the intensity graph ---- */
tab(2); pause();
{ uok(isShown(findLabelledU('screen'))&&isShown(findLabelledU('intensity graph (not in PhET’s Waves Intro)')),
      'light shows the screen and intensity boxes');
  uok(!isShown(chipU('particles',3))&&!isShown(chipU('side view',2)),'and neither the sound nor the water chips');
  runFor('light',260);
  RECU=makeRecU(); tab(2); const withScr=RECU.ops.length;
  const sc=findLabelledU('screen'); sc.checked=false; sc.fire('change');
  RECU=makeRecU(); tab(2); uok(RECU.ops.length<withScr,'switching the screen off draws less');
  sc.checked=true; sc.fire('change');
  const si=findLabelledU('intensity graph (not in PhET’s Waves Intro)'); si.checked=true; si.fire('change');
  RECU=makeRecU(); tab(2); uok(textsU(RECU).indexOf('intensity')>=0,'the intensity graph is drawn when asked for');
  uok(RO().indexOf('brightness')>=0,'and the readout carries the screen’s brightness');
  si.checked=false; si.fire('change'); }

/* ---- the three media ---- */
tab(3);
{ uok(!isShown(sliderU('amplitude'))&&isShown(sliderU('frequency (drip rate), Hz'))&&isShown(sliderU('frequency (pitch), Hz')),
      'the analysis view shows all three frequency sliders and no amplitude');
  const before=RO(); RECU=makeRecU();
  const s=sliderU('frequency (colour), THz'); s.value=String(SCENES.light.fmax); s.fire('input');
  uok(RO()!==before,'moving light’s frequency re-measures the lattice');
  uok(RECU.ops.length>40,'and redraws ('+RECU.ops.length+' ops)');
  uok(RO().indexOf('380.0 nm')>=0,'the readout prints λ = 380.0 nm at the violet end');
  assertCleanU(RECU,'the three media');
  s.value=String(SCENES.light.fmin); s.fire('input'); uok(RO().indexOf('780.0 nm')>=0,'and 780.0 nm at the red end'); }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='water','1 is water'); keyU('3'); uok(ST.view==='light','3 is light');
  keyU('4'); uok(ST.view==='media','4 is the three media');
  keyU('9'); uok(ST.view==='media','9 is not a view'); keyU('2'); uok(ST.view==='sound','2 is sound'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length>=14,'the panel has its sliders and checkboxes ('+inputs.length+')');
  for(let v=0;v<4;v++){ tab(v); pause();
    let touched=0;
    for(const inp of inputs){
      if(!isShown(inp)) continue; touched++;
      if(inp.type==='checkbox'){ if(inp===findLabelledU('time runs')) continue;
        inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); }
      uok(NODESU.errbox.style.display!=='block','tab '+v+': '+(rowOf(inp)&&rowOf(inp).children[0]?rowOf(inp).children[0].textContent:'a slider')+' at its ends draws without error'); }
    uok(touched>=2,'tab '+v+' has controls on show ('+touched+')');
    RECU=makeRecU(); tab(v); assertCleanU(RECU,'tab '+v+' after the sweep'); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

/* ---- the panel shows each view its own groups ---- */
{ const groups=NODESU.panel.children;
  tab(0); uok(groups[1].hidden===false&&groups[2].hidden===false&&groups[3].hidden===false,'a medium view shows what-to-show, tools and time');
  tab(3); uok(groups[1].hidden===true&&groups[2].hidden===true&&groups[3].hidden===true&&groups[0].hidden===false,
              'the three-media view shows only the source group');
  tab(0); }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(2); pause();
  sliderU('frequency (colour), THz').value='0.7'; sliderU('frequency (colour), THz').fire('input');
  sliderU('amplitude').value='2'; sliderU('amplitude').fire('input');
  chipU('pulse',2).fire('click'); chipU('slow',2).fire('click');
  for(const nm of ['tape measure','stopwatch','wave meter','graph of the centre line','intensity graph (not in PhET’s Waves Intro)']){
    const c=findLabelledU(nm); c.checked=true; c.fire('change'); }
  const sc=findLabelledU('screen'); sc.checked=false; sc.fire('change');
  TOOLS.tape[0]=[0.9,0.9]; TOOLS.probes[0]=[0.1,0.1]; ST.look='side'; ST.soundView='both'; ST.tone=true;
  runFor('light',40); RUNS.light.watch.on=true;
  uok(ST.speed==='slow'&&ST.tape&&ST.meter&&ST.inten&&!ST.screen&&ST.wave==='pulse','the state is disturbed');
  idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true; for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]) same=false;
  uok(same,'reset all restores every default');
  uok(JSON.stringify(TOOLS)===JSON.stringify(TOOLS0),'and the tools’ positions');
  uok(RUNS.light.n===0&&RUNS.light.t===0&&RUNS.water.n===0&&!RUNS.light.watch.on,'and every run (all three clocks at zero, the stopwatch off)');
  uok(RUNS.light.A===8&&RUNS.light.cont&&RUNS.light.src[0],'and each source (amplitude 8, continuous, running)');
  uok(RECU.ops.length>=6,'reset repaints (a fresh, empty tank: '+RECU.ops.length+' ops)');
  uok(findLabelledU('tape measure').checked===false,'the checkboxes follow');
  uok(chipU('normal',2).className==='chip on'&&chipU('continuous',2).className==='chip on','the chips follow');
  uok(Math.abs(+sliderU('frequency (colour), THz').value-sceneF0(SCENES.light))<1e-12,'the sliders follow');
  uok(AUDIO.state==='off','and the tone is silent');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
