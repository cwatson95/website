
/* ============ UI drive test for wave-interference.html ===================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js via
 * build/blackbody-spectrum, which carries the innerHTML -> textContent fix).
 * The three lattice views animate, so every idle-first test PAUSES the clock
 * first; the far field, path difference and the lattice view never animate.
 * Three custom drags (a tape end, a wave-meter probe, the barrier), every tab,
 * every visible slider at its ends, every checkbox, every chip, every button,
 * the keys, resize, and reset-all against a fully disturbed state.            */
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
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
function sliderU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
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
function isShown(el){ let n=el; const chain=[]; const walk=(p)=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
function pause(){ if(ST.running) keyU(' '); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.panel.children.length===12,'the control panel has its twelve groups ('+NODESU.panel.children.length+')');
uok(RO().length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').indexOf('&nabla;&sup2;u')>=0,'the equation bar carries the wave equation, no NaN');
uok(RO().indexOf('2.64 cm')>=0,'the readout prints the water wavelength 2.64 cm off the model');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');

/* ---- every tab draws, differently, cleanly (the lattice tabs at their first step) ---- */
pause();
/* 70 % of what each tab emits at 1400 x 820 on its first draw (TABOPS 10, 14, 12, 78, 62, 164):
   the fields batch thousands of cells into a few fills, so op counts are small by design */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[7,9,8,54,43,114];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while paused / static');
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- the clock: the lattice runs in the frame loop, and only there ---- */
tab(0); keyU(' '); uok(ST.running,'space starts the clock');
{ const n0=RUNS.tank.n; RECU=makeRecU(); pumpU(60);
  uok(RUNS.tank.n-n0>=35&&RUNS.tank.n-n0<=37,'sixty frames advance the tank 36 steps at PhET’s 20·111/61 per second ('+(RUNS.tank.n-n0)+')');
  uok(RECU.ops.length>60,'and the loop repaints as it runs');
  chipU('slow',2).fire('click'); const n1=RUNS.tank.n; pumpU(60);
  uok(RUNS.tank.n-n1>=17&&RUNS.tank.n-n1<=19,'slow runs at half that ('+(RUNS.tank.n-n1)+')');
  chipU('normal',2).fire('click'); uok(chipU('normal',2).className==='chip on','the normal chip lights');
  keyU(' '); uok(!ST.running,'space pauses'); const n2=RUNS.tank.n; pumpU(20); uok(RUNS.tank.n===n2,'paused: no steps');
  idleU('paused: the tank paints nothing');
  const cb=findLabelledU('time runs'); uok(!!cb&&cb.checked===false,'the "time runs" box follows the key');
  RECU=makeRecU(); clickButtonU('one step'); uok(RUNS.tank.n===n2+1,'one step is exactly one lattice step'); uok(RECU.ops.length>20,'and repaints at once');
  tab(3); const n3=RUNS.tank.n; ST.running=true; pumpU(20); uok(RUNS.tank.n===n3,'the far field does not run the tank'); ST.running=false; tab(0); }
/* march the tank to a filled state for the rest */
runFor('tank',200);

/* ---- a slider with the full treatment: proven idle, fire, drawn at once ---- */
idleU('idle before the slider test');
{ const s=sliderU('drip rate, Hz'); uok(!!s&&isShown(s),'the water drip-rate slider is on show');
  RECU=makeRecU(); s.value='0.9'; s.fire('input');
  uok(Math.abs(ST.f_water-0.9)<1e-12&&Math.abs(RUNS.tank.f-0.9)<1e-12,'it sets 0.9 Hz on the run'); uok(RECU.ops.length>30,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(RO().indexOf('1.83 cm')>=0,'the readout follows: lambda = 1.65/0.9 = 1.83 cm');
  uok(RUNS.tank.lat.u.some(v=>v!==0),'a new water frequency keeps the waves (PhET)'); }

/* ---- the tape measure, dragged through the frame loop from a proven-idle baseline ---- */
{ const cb=findLabelledU('tape measure'); uok(!!cb,'found the tape measure box'); cb.checked=true; cb.fire('change');
  uok(ST.tape&&RO().indexOf('tape measure')>=0,'the tape measure shows in the readout');
  idleU('idle before the tape drag');
  const G=latGeo(RECU,1400,820,buildModel()), sq=G.sq, a=TOOLS.tape[0];
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

/* ---- the wave meter: a probe dragged, its trace recorded ---- */
{ const cb=findLabelledU('wave meter'); cb.checked=true; cb.fire('change'); uok(ST.meter,'wave meter on');
  idleU('idle before the probe drag');
  const G=latGeo(RECU,1400,820,buildModel()), sq=G.sq, p=TOOLS.probes[1];
  uok(!!G.mb,'the meter’s chart has room at 1400 x 820');
  NODESU.scene.fire('pointerdown',{clientX:sq.x+p[0]*sq.w,clientY:sq.y+p[1]*sq.h}); uok(DRAG.what==='probe1','a probe grabs');
  pumpU(1); idleU('drained');
  NODESU.scene.fire('pointermove',{clientX:sq.x+0.8*sq.w,clientY:sq.y+0.6*sq.h,buttons:1});
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200,'the probe drag repaints through the loop'); NODESU.scene.fire('pointerup',{});
  uok(Math.abs(TOOLS.probes[1][0]-0.8)<1e-12,'the probe moved');
  const R=RUNS.tank, t0=R.trace.length; ST.running=true; pumpU(30); ST.running=false;
  uok(R.trace.length>t0&&R.trace[R.trace.length-1].length===3,'running, the meter records both probes each step');
  uok(textsU(RECU).length>0,'text drawn'); }

/* ---- the stopwatch ---- */
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change');
  const R=RUNS.tank; R.watch.t=0; clickButtonU('start / stop the stopwatch'); uok(R.watch.on,'start');
  ST.running=true; const n0=R.n; pumpU(30); ST.running=false;
  uok(Math.abs(R.watch.t-(R.n-n0)*R.dt)<1e-12,'the stopwatch counts the steps’ physical time');
  clickButtonU('start / stop the stopwatch'); uok(!R.watch.on,'stop'); const t=R.watch.t; ST.running=true; pumpU(10); ST.running=false; uok(R.watch.t===t,'stopped, it holds');
  RECU=makeRecU(); clickButtonU('zero the stopwatch'); uok(R.watch.t===0,'zero'); uok(textsU(RECU).some(s=>s.indexOf('stopwatch 0')===0),'and the canvas shows it'); }

/* ---- the media, the side view, the parcels, the screen ---- */
{ for(const [nm,id] of [['sound','sound'],['light','light'],['water','water']]){
    const c=chipU(nm,3); uok(!!c,'found the '+nm+' chip'); RECU=makeRecU(); c.fire('click');
    uok(ST.scene===id&&RUNS.tank.scene===id,nm+' is the medium'); uok(RUNS.tank.lat.u.every(v=>v===0),'and the lattice starts empty');
    uok(c.className==='chip on','its chip lights'); assertCleanU(RECU,nm); }
  uok(isShown(chipU('side view',2))&&!isShown(chipU('particles',3)),'water shows the top/side chips, not the sound ones');
  runFor('tank',120); idleU('idle before side view');
  RECU=makeRecU(); chipU('side view',2).fire('click'); uok(ST.look==='side','side view'); const gs=geomU(RECU); uok(gs.length>200,'the side view draws');
  chipU('top view',2).fire('click'); uok(ST.look==='top','back to the top view');
  chipU('sound',3).fire('click'); uok(isShown(chipU('particles',3))&&!isShown(chipU('side view',2)),'sound shows waves / particles / both, and no side view'); runFor('tank',120);
  RECU=makeRecU(); chipU('particles',3).fire('click'); const gp=geomU(RECU); RECU=makeRecU(); chipU('both',3).fire('click'); const gb=geomU(RECU);
  uok(gp!==gb&&gp.length>200,'particles and both draw different pictures'); chipU('waves',3).fire('click');
  chipU('light',3).fire('click'); uok(isShown(findLabelledU('screen'))&&isShown(findLabelledU('intensity graph')),'light shows the screen and intensity boxes');
  runFor('tank',150); RECU=makeRecU(); tab(0); uok(textsU(RECU).indexOf('intensity')>=0,'the intensity graph is drawn');
  const si=findLabelledU('intensity graph'); si.checked=false; si.fire('change'); RECU=makeRecU(); tab(0); uok(textsU(RECU).indexOf('intensity')<0,'intensity off: no graph');
  si.checked=true; si.fire('change'); chipU('water',3).fire('click'); }

/* ---- pulses ---- */
{ chipU('pulse',2).fire('click'); uok(ST.wave==='pulse'&&isShown(buttonU('fire a pulse')),'pulse mode shows the fire button');
  clickButtonU('clear the waves'); uok(RUNS.tank.lat.u.every(v=>v===0),'clear the waves empties the lattice');
  clickButtonU('fire a pulse'); uok(RUNS.tank.pulse.on,'the pulse fires'); ST.running=true; pumpU(200); ST.running=false;
  uok(!RUNS.tank.pulse.on&&RUNS.tank.lat.u.some(v=>Math.abs(v)>0.1),'it ends after a period and its ring travels');
  keyU('r'); uok(RUNS.tank.lat.u.every(v=>v===0),'r clears'); keyU('p'); uok(RUNS.tank.pulse.on,'p fires a pulse');
  chipU('continuous',2).fire('click'); uok(!isShown(buttonU('fire a pulse')),'continuous hides the fire button');
  RUNS.tank.pulse.on=false; keyU('p'); uok(!RUNS.tank.pulse.on,'p does nothing then (a continuous source refuses a pulse)'); }

/* ---- two sources ---- */
tab(1); pause();
{ uok(isShown(findLabelledU('top source on'))&&isShown(findLabelledU('bottom source on')),'the two-source tab shows its two source boxes');
  runFor('two',160); const R=RUNS.two;
  const cb=findLabelledU('bottom source on'); RECU=makeRecU(); cb.checked=false; cb.fire('change'); uok(!R.src[1],'the bottom source switches off'); uok(RECU.ops.length>60,'and repaints');
  cb.checked=true; cb.fire('change'); uok(R.src[1]&&R.phi>0,'back on, in phase with the running source');
  const s=sliderU('separation, cm (water)'); uok(isShown(s),'the separation slider is on show'); s.value='5'; s.fire('input');
  uok(Math.abs(R.sep-5)<1e-12&&RO().indexOf('nodal lines')>=0,'separation 5 cm reaches the run and the readout');
  const nl=findLabelledU('nodal lines (r₁ − r₂ = (m + ½)λ)'); RECU=makeRecU(); nl.checked=false; nl.fire('change'); const g0=geomU(RECU);
  RECU=makeRecU(); nl.checked=true; nl.fire('change'); const g1=geomU(RECU); uok(g1.length>g0.length,'the nodal hyperbolae add curves when on'); }

/* ---- the slits: barrier chips, and the barrier dragged ---- */
tab(2); pause();
{ const R=RUNS.slits; uok(isShown(chipU('two slits',3)),'the barrier chips are on show');
  chipU('two slits',3).fire('click'); uok(ST.barrier==='two'&&R.plane.barrier==='two','two slits'); runFor('slits',150);
  uok(isShown(sliderU('slit separation, cm (water)')),'two slits show the separation slider');
  chipU('one slit',3).fire('click'); uok(!isShown(sliderU('slit separation, cm (water)'))&&isShown(sliderU('slit width, cm (water)')),'one slit hides it');
  chipU('no barrier',3).fire('click'); uok(!isShown(sliderU('slit width, cm (water)'))&&!isShown(sliderU('barrier position')),'no barrier hides the slit sliders');
  chipU('two slits',3).fire('click'); runFor('slits',150);
  idleU('idle before the barrier drag');
  const G=latGeo(RECU,1400,820,buildModel()), sq=G.sq, x0=cellX(sq,R,ST.bcol);
  NODESU.scene.fire('pointerdown',{clientX:x0,clientY:sq.y1+12}); uok(DRAG.what==='barrier','pointer-down on the handle grabs the barrier');
  pumpU(1); idleU('drained');
  const m0=R.plane.m, left=R.lat.u[75*R.lat.nx+40];
  NODESU.scene.fire('pointermove',{clientX:sq.x+0.7*sq.w,clientY:sq.y1+12,buttons:1});
  uok(ST.bcol===Math.round(LAT.PAD-0.5+0.7*LAT.VIS),'the barrier follows to 0.7 of the width (column '+ST.bcol+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200,'the drag repaints through the loop');
  uok(R.plane.bcol===ST.bcol&&R.plane.m===m0&&R.lat.u[75*R.lat.nx+40]===left,'the plane wave keeps its progress (PhET clearRight)');
  NODESU.scene.fire('pointerup',{});
  const bp=sliderU('barrier position'); uok(+bp.value===ST.bcol,'the barrier slider follows the drag'); }

/* ---- the far field: every aperture chip, laser, brightness ---- */
tab(3);
{ const seen=new Set();
  for(const a of AP_LIST){ const c=chipU(a.name,7); uok(!!c,'found the '+a.name+' chip'); RECU=makeRecU(); c.fire('click');
    uok(ST.ap===a.id,a.name+' chosen'); seen.add(geomU(RECU)); assertCleanU(RECU,a.name);
    uok(NODESU.errbox.style.display!=='block',a.name+' drew without error'); }
  uok(seen.size===7,'every aperture draws a different picture');
  chipU('ellipse',7).fire('click');
  const s=sliderU('wavelength, nm'); RECU=makeRecU(); s.value='700'; s.fire('input'); uok(ST.lam===700,'700 nm');
  uok(RECU.ops.some(o=>o[0]==='f'&&/rgb\(\d+,0,/.test(o[1])),'the pattern turns red'); s.value=String(DIF.LAM0); s.fire('input');
  const lc=findLabelledU('laser on'); RECU=makeRecU(); lc.checked=false; lc.fire('change'); uok(textsU(RECU).indexOf('the laser is off')>=0,'laser off says so');
  lc.checked=true; lc.fire('change');
  RECU=makeRecU(); chipU('intensity |F|²',2).fire('click'); const gl=geomU(RECU); RECU=makeRecU(); chipU('PhET’s log brightness',2).fire('click');
  uok(gl!==geomU(RECU),'linear and PhET’s log brightness differ'); }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='tank','1 is the ripple tank'); keyU('4'); uok(ST.view==='far','4 is the far field'); keyU('6'); uok(ST.view==='lattice','6 is the lattice');
  keyU('9'); uok(ST.view==='lattice','9 is not a view'); keyU('5'); uok(ST.view==='path','5 is path difference'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length>=45,'the panel has its sliders and checkboxes ('+inputs.length+')');
  for(let v=0;v<6;v++){ tab(v); pause();
    for(const sc of (v<3||v===5?['water','sound','light']:['water'])){
      if(v<3||v===5){ chipU(sc,3).fire('click'); }
      let touched=0;
      for(const inp of inputs){
        if(!isShown(inp)) continue; touched++;
        if(inp.type==='checkbox'){ if(inp===findLabelledU('time runs')) continue; inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
        for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); }
        uok(NODESU.errbox.style.display!=='block','tab '+v+' '+sc+': '+(rowOf(inp)&&rowOf(inp).children[0]?rowOf(inp).children[0].textContent:'a slider')+' at its ends draws without error'); }
      uok(touched>=2,'tab '+v+' ('+sc+') has controls on show ('+touched+')');
      RECU=makeRecU(); tab(v); assertCleanU(RECU,'tab '+v+' '+sc+' after the sweep'); } }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

/* ---- the panel shows each view its own groups ---- */
{ const groups=NODESU.panel.children;
  tab(3); uok(groups[0].hidden===true&&groups[6].hidden===false&&groups[7].hidden===true,'the far field shows the aperture group, not the medium or path groups');
  tab(4); uok(groups[7].hidden===false&&groups[6].hidden===true,'path difference shows its own group');
  tab(5); uok(groups[8].hidden===false&&groups[0].hidden===false,'the lattice shows the medium and its own group');
  { const s=sliderU('direction θ for the readout'); s.value='10'; s.fire('input'); uok(RO().indexOf('&theta; = 10&deg;')>=0,'the θ slider reaches the readout'); } }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(0); pause();
  chipU('light',3).fire('click'); sliderU('frequency, THz').value='0.7'; sliderU('frequency, THz').fire('input');
  chipU('pulse',2).fire('click'); chipU('slow',2).fire('click');
  for(const nm of ['tape measure','stopwatch','wave meter','graph of the centre line']){ const c=findLabelledU(nm); c.checked=true; c.fire('change'); }
  TOOLS.tape[0]=[0.9,0.9]; TOOLS.probes[0]=[0.1,0.1]; ST.bcol=100; ST.barrier='none'; ST.ap='figure'; ST.lam=650; ST.pd=5; ST.latTh=7; ST.laser=false;
  runFor('tank',40);
  uok(ST.scene==='light'&&ST.wave==='pulse'&&ST.speed==='slow'&&ST.tape&&ST.meter&&!ST.laser,'the state is disturbed');
  idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true; for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]) same=false;
  uok(same,'reset all restores every default');
  uok(JSON.stringify(TOOLS)===JSON.stringify(TOOLS0),'and the tools’ positions');
  uok(RUNS.tank.scene==='water'&&RUNS.tank.n===0&&RUNS.tank.t===0,'and the runs (water, clock at zero)');
  uok(RECU.ops.length>=7,'reset repaints (a fresh, empty tank: '+RECU.ops.length+' ops)'); uok(findLabelledU('tape measure').checked===false,'the checkboxes follow');
  uok(chipU('water',3).className==='chip on'&&chipU('normal',2).className==='chip on','the chips follow');
  uok(Math.abs(+sliderU('drip rate, Hz').value-0.625)<1e-12,'the sliders follow');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
