
/* ============ UI drive test for gas-properties.html ======================= *
 * DOM-stub pattern (lineage: build_buoy/ui_drive_bu.js).  Three canvas drags
 * (the left-wall grip, the lid knob, the pump handle), a heater that springs
 * back, the hold-constant chips and their enabling, and a running clock:
 * every action must move the picture THROUGH the frame loop from a
 * proven-idle baseline (time paused, loop drained, idle frame drew nothing). */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,arcs:0,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},
    lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);},
    arc(x,y,r){c.arcs++; c._p&&c._p.push([x,y,r]);},
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
const entReU=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
function assertCleanU(rec,label){
  let bad=null;
  for(const o of rec.ops) if(o[0]==='t'){
    if(entReU.test(o[1])){ bad='entity/tag "'+String(o[1]).slice(0,40)+'"'; break; }
    if(/NaN|undefined/.test(o[1])){ bad='NaN/undefined "'+String(o[1]).slice(0,40)+'"'; break; } }
  uok(!bad,label+' text ops clean'+(bad?' ('+bad+')':''));
}
let RECU=makeRecU();
function mkElU(tag){
  const e={tagName:(tag||'div').toUpperCase(),children:[],style:{},dataset:{},
    _h:{},className:'',id:'',value:'0',checked:false,hidden:false,disabled:false,textContent:'',
    appendChild(c){ this.children.push(c); c.parentEl=this;
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
  let _html='', _txt='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },set(v){ _html=''+v; _txt=(''+v).replace(/<[^>]*>/g,''); }});
  Object.defineProperty(e,'textContent',{get(){ return _txt; },set(v){ _txt=''+v; }});
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
/* whole-label match (lagrange_points Known-bad: a substring finds the wrong row) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(label){ const b=buttonU(label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function geoU(){ return viewGeo(RECU,1400,820,buildModel()); }
function pauseU(){ const cb=findLabelledU('time runs'); if(cb.checked){ cb.checked=false; cb.fire('change'); } }
function playU(){ const cb=findLabelledU('time runs'); if(!cb.checked){ cb.checked=true; cb.fire('change'); } }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.panel.children.length>=12,'the control panel has its groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(/11\.[5-9] atm/.test(NODESU.readout.innerHTML),'the readout prints the gauge near 11.7 atm (100 heavy, 300 K, 10 nm)');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');

/* ---- every tab draws, differently, cleanly (floors from the t = 0 emission) ---- */
/* floors at ~80 % of what each tab emits at t = 0 (43, 68, 134, 16, 37, 39
   ops), and the disks must all be drawn: batching many disks into one fill is
   deliberate, so the substance is floored on the arcs the fills carry */
const FLOORSU=[34,54,107,13,30,31];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  const nd=gasCount(worldOf(ST.view).g);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(RECU.arcs>=nd,'tab '+i+' draws every one of its '+nd+' disks ('+RECU.arcs+' arcs)');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- the clock: running, frames differ; paused, every view idles ---- */
tabU(0); playU();
RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
uok(gA.length>50&&gB.length>50&&gA!==gB,'running: two frames draw DIFFERENT pictures (the disks move)');
{ const t0=worldOf('ideal').g.t; pumpU(24); uok(Math.abs(worldOf('ideal').g.t-t0-24*GAS.DT_FRAME)<1e-9,'24 frames advance the model 1 ps (1/24 ps each)'); }
pauseU();
for(let i=0;i<6;i++){ tabU(i); idleU('tab '+i+' paints nothing while paused'); }
{ tabU(0); const t0=worldOf('ideal').g.t; keyU('s'); uok(Math.abs(worldOf('ideal').g.t-t0-0.2)<1e-12,'s steps exactly 0.2 ps (PhET’s MODEL_TIME_STEP)'); idleU('and the loop is idle again'); }
{ keyU(' '); uok(ST.running===true,'space runs'); keyU(' '); uok(ST.running===false,'space pauses'); }

/* ---- drag 1: the left-wall grip in the gas-law view (PhET pauses; no work) ---- */
tabU(0); idleU('the gas law idles before the wall drag');
{ const w=worldOf('ideal'), g=w.g, G=geoU(), T1=g.T, W1=g.W;
  const hx=G.handle.x+G.handle.w/2, hy=G.handle.y+G.handle.h/2;
  NODESU.scene.fire('pointerdown',{clientX:hx,clientY:hy});
  uok(DRAG.what==='wall','pointer-down ON the wall grip grabs it');
  uok(w.dragW===W1,'the Ideal wall drag starts from the current width');
  idleU('the grab’s own repaint has drained (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:hx+80,clientY:hy,buttons:1});
  uok(w.dragW<W1-500,'moving right narrows the box being dragged ('+w.dragW+' pm)');
  uok(g.W===W1,'… but the model width waits for the release (PhET pauses and redistributes)');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again');
  const dragged=w.dragW;
  uok(dragged===Math.min(15000,Math.max(5000,Math.round((W1-80/G.s)/10)*10)),'the dragged width follows the pointer to 10 pm ('+dragged+')');
  { playU(); const t0=g.t; pumpU(5); uok(g.t===t0,'while the Ideal wall is held the model is paused (PhET), even with time running');
    RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','… and a grip held still with time running costs no frames (the loop idles)'); pauseU();
    keyU('s'); uok(g.t===t0,'… and the step key does not step it either (model.md: paused while resizing)'); }
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(g.W===dragged,'release: the width is now '+g.W+' pm'); uok(Math.abs(g.T-T1)<1e-9,'the Ideal wall did no work: T unchanged');
  uok(NODESU.readout.innerHTML.indexOf(fmt(g.W/1000,2)+' nm')>=0,'the readout followed the drag');
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:G.xR-30,clientY:G.yB-30});
  uok(DRAG.what===null,'a pointer-down inside the box grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }
/* drag 2: the lid knob */
idleU('idle before the lid drag');
{ const g=worldOf('ideal').g, G=geoU(), k=G.lidKnob, o0=gasOpening(g);
  uok(o0===0,'the lid starts closed');
  NODESU.scene.fire('pointerdown',{clientX:k.x+k.w/2,clientY:k.y+k.h/2}); uok(DRAG.what==='lid','pointer-down on the lid knob grabs it');
  idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:k.x+k.w/2-120,clientY:k.y+k.h/2,buttons:1});
  uok(Math.abs(gasOpening(g)-120/G.s)<=1,'dragging the knob 120 px left opens a gap of exactly 120 px in pm ('+gasOpening(g)+' vs '+(120/G.s).toFixed(1)+')');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'and the view repainted through the loop');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'released');
  uok(!gasHoldAllowed(g,'temperature'),'with the lid open, hold T is disabled');
  const tc=chipU('Temperature (T)',5); uok(!!tc&&tc.disabled===true,'… and its chip is disabled on the panel');
  gasSetLid(g,gasMaxLid(g)); uok(gasOpening(g)===0,'closed again'); }
/* drag 3: the pump handle: a full stroke pumps 50 */
idleU('idle before the pump');
{ const g=worldOf('ideal').g, G=geoU(), hnd=G.pumpHandle, n0=gasCount(g,0);
  NODESU.scene.fire('pointerdown',{clientX:hnd.x+hnd.w/2,clientY:hnd.y+hnd.h/2}); uok(DRAG.what==='pump','pointer-down on the pump handle grabs it');
  idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:hnd.x+hnd.w/2,clientY:hnd.y+hnd.h/2+G.pump.travel+30,buttons:1});
  uok(gasCount(g,0)===n0+50,'a full stroke pumps 50 heavy disks ('+n0+' → '+gasCount(g,0)+')');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'the pump stroke repaints through the loop');
  NODESU.scene.fire('pointerup',{});
  uok(ST.nH===gasCount(g,0),'the heavy slider follows the pump ('+ST.nH+')');
  const lc=chipU('light',2); lc.fire('click'); uok(ST.pump==='light','the pump now pumps light');
  const G2=geoU(), h2=G2.pumpHandle;
  NODESU.scene.fire('pointerdown',{clientX:h2.x+h2.w/2,clientY:h2.y+h2.h/2}); NODESU.scene.fire('pointermove',{clientX:h2.x+h2.w/2,clientY:h2.y+h2.h/2-200,buttons:1});
  NODESU.scene.fire('pointerup',{}); uok(gasCount(g,1)===0,'pulling the handle UP pumps nothing');
  chipU('heavy',2).fire('click'); }

/* ---- the heater springs back; hold-constant chips ---- */
{ const s=sliderU('cool ← → heat'); uok(!!s,'found the heat slider'); const g=worldOf('ideal').g;
  s.value='1'; s.fire('input'); uok(ST.heat===1,'the heat slider sets +1');
  const T0=g.T; playU(); pumpU(24); uok(g.T>T0*1.05,'one second of full heat warms the gas ('+T0.toFixed(1)+' → '+g.T.toFixed(1)+' K)');
  s.fire('change'); uok(ST.heat===0,'released, the slider springs back to 0 (PhET’s snapToZero)'); pauseU(); }
{ const g=worldOf('ideal').g;
  chipU('Pressure ↕V',5).fire('click'); uok(g.hold==='pressureV','the P↕V chip holds pressure by moving the wall');
  const P0=g.P; const s=sliderU('cool ← → heat'); s.value='0.8'; s.fire('input'); playU(); pumpU(24); s.fire('change'); pauseU();
  uok(Math.abs(g.P/P0-1)<1e-5,'P↕V: heating left P at '+g.P.toFixed(2)+' kPa (started '+P0.toFixed(2)+')');
  uok(/V \/ T \(Charles\)/.test(NODESU.readout.innerHTML),'the readout shows the invariant P↕V keeps: V/T (Charles)');
  uok(NODESU.eqbar.innerHTML.indexOf('<span class="hl">P</span>')>=0,'the equation bar highlights the held P');
  chipU('Volume (V)',5).fire('click'); uok(g.hold==='volume','V held');
  const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.handle.x+5,clientY:G.handle.y+20}); uok(DRAG.what===null,'with V held the wall grip is gone'); NODESU.scene.fire('pointerup',{});
  chipU('Temperature (T)',5).fire('click'); uok(g.hold==='temperature','T held');
  uok(rows_disabled('cool ← → heat'),'holding T disables the heater');
  clickU('erase particles'); uok(g.hold==='nothing'&&g.oops==='temperatureEmpty','erasing while holding T: PhET’s Oops, hold released');
  pumpU(2); RECU=makeRecU(); tabU(0); uok(RECU.ops.some(o=>o[0]==='t'&&/Temperature cannot be held constant/.test(o[1])),'the Oops banner is on the canvas');
  uok(chipU('Pressure ↕V',5).disabled===true,'empty box: the P chips are disabled');
  const sH=sliderU('heavy (28 AMU)'); sH.value='100'; sH.fire('input'); uok(gasCount(g,0)===100,'the heavy slider refills 100');
  uok(g.oops===null,'any action clears the Oops'); }
function rows_disabled(label){ const s=sliderU(label); return !!s&&s.disabled===true; }

/* ---- the moving wall: the grip resumes the clock and the wall does work ---- */
tabU(1); idleU('the moving wall idles while paused');
{ const w=worldOf('explore'), g=w.g, G=geoU(), W0=g.W, T0=g.T;
  NODESU.scene.fire('pointerdown',{clientX:G.handle.x+5,clientY:G.handle.y+20});
  uok(DRAG.what==='wall'&&ST.running===true,'grabbing the Explore wall starts the clock (PhET)');
  NODESU.scene.fire('pointermove',{clientX:G.handle.x+5+150,clientY:G.handle.y+20,buttons:1});
  uok(g.wantW<W0-2000,'the requested width follows the pointer ('+g.wantW+')');
  NODESU.scene.fire('pointerup',{});
  pumpU(2); uok(g.W<W0&&W0-g.W<=2*800*GAS.DT_FRAME+1e-9,'the wall heads in at no more than 800 m/s ('+(W0-g.W).toFixed(2)+' pm in 2 frames)');
  pumpU(200); uok(g.W===g.wantW,'and arrives'); uok(g.T>T0,'the squeezed gas is warmer ('+T0.toFixed(1)+' → '+g.T.toFixed(1)+' K)');
  uok(g.led.work>0,'the wall did positive work'); pauseU();
  uok(NODESU.readout.innerHTML.indexOf('work done by the wall')>=0,'the readout shows the work'); }

/* ---- the energy view: collisions, injection, histograms ---- */
tabU(2);
{ const g=worldOf('energy').g;
  const cc=findLabelledU('particle–particle collisions'); uok(!!cc&&cc.checked===true,'collisions on by default');
  cc.checked=false; cc.fire('change'); uok(g.collisions===false,'the checkbox switches collisions off');
  chipU('set to',2).fire('click'); uok(ST.injMode==='set','injection: set to');
  const it=sliderU('set to, K'); it.value='600'; it.fire('input'); uok(g.injectT===600,'the injection temperature is 600 K');
  const n0=gasCount(g,0); const sH=sliderU('heavy (28 AMU)'); sH.value=String(n0+20); sH.fire('input');
  let same=true; for(let i=0;i<g.n;i++) if(g.id[i]>g.nextId-21&&Math.abs(gasSpeed(g,i)-Math.sqrt(3*GAS.K*600/28))>1e-9) same=false;
  uok(same,'collisions off: 20 injected at 600 K all at one speed (no spread)');
  cc.checked=true; cc.fire('change'); chipU('match container',2).fire('click'); uok(g.injectT===null,'match container');
  uok(ST.zoom===5,'PhET’s default histogram scale is 0–100'); const z=chipU('0–200',7); z.fire('click'); uok(ST.zoom===4,'the histogram zoom chip');
  RECU=makeRecU(); tabU(2); const t2=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/speed/.test(t2)&&/kinetic energy/.test(t2),'both histograms drawn');
  const hh=findLabelledU('heavy histogram'); hh.checked=false; hh.fire('change'); uok(ST.histH===false,'heavy outline off'); hh.checked=true; hh.fire('change'); }

/* ---- diffusion ---- */
tabU(3);
{ const g=worldOf('diffusion').g;
  uok(g.divided===true,'divided at the start');
  clickU('remove divider'); uok(g.divided===false,'remove divider'); uok(buttonU('reset divider')!==null,'the button now reads reset divider');
  playU(); pumpU(60); pauseU();
  uok(g.flow.dts.length>0,'the flow counter runs with the divider out');
  const m=sliderU('mass, AMU'); m.value='16'; m.fire('input'); uok(g.species[0].m===16,'particle 1 mass 16 AMU');
  let one=true; for(let i=0;i<g.n;i++) if(g.sp[i]===0&&Math.abs(gasSpeed(g,i)-Math.sqrt(3*GAS.K*300/16))>1e-9) one=false; uok(one,'… every particle 1 reset to sqrt(3kT/m) (PhET)');
  const r=sliderU('radius, pm '); r.value='200'; r.fire('input'); uok(g.species[1].r===200,'particle 2 radius 200 pm');
  const n=sliderU('number '); n.value='50'; n.fire('input'); uok(gasCount(g,1)===50,'particle 2 count 50');
  clickU('reset divider'); uok(g.divided===true&&gasCount(g,0)===ST.d1n,'reset divider: PhET restarts');
  chipU('slow',2).fire('click'); uok(ST.slow===true&&viewDt(ST)===GAS.DT_SLOW,'slow: 0.3 ps a second');
  chipU('normal',2).fire('click');
  for(const lab of ['centre of mass','particle flow rate','scale']){ const cb=findLabelledU(lab); uok(!!cb,'found '+lab); cb.checked=!cb.checked; cb.fire('change'); cb.checked=!cb.checked; cb.fire('change'); } }

/* ---- the pressure and equilibrium views ---- */
tabU(4);
{ const s=sliderU('heavy disks'); s.value='120'; s.fire('input'); const g=worldOf('pressure').g; uok(gasCount(g,0)===120,'the pressure view restarts with 120');
  playU(); pumpU(48); pauseU(); uok(g.imp.t>1.9,'the walls have been counting for 2 ps');
  uok(NODESU.readout.innerHTML.indexOf('the walls feel')>=0,'the readout compares the walls with the gauge');
  const cb=findLabelledU('particle–particle collisions'); }
tabU(5);
{ chipU('hot heavy, cold light',3).fire('click'); const w=worldOf('equil'); uok(ST.eStart==='split'&&w.hist.length===1,'the split start, fresh');
  const L=w.hist[0]; uok(L[2]>1.5&&L[3]<0.6,'heavy starts hot, light cold ('+L[2].toFixed(2)+', '+L[3].toFixed(2)+')');
  playU(); pumpU(240); pauseU(); const L2=w.hist[w.hist.length-1]; uok(Math.abs(L2[2]-1)<Math.abs(L[2]-1),'after 10 ps they are closer to equipartition ('+L2[2].toFixed(3)+')'); }

/* ---- sliders repaint at once; tools; units; keyboard ---- */
tabU(0); idleU('idle before the slider repaint test');
{ const s=sliderU('light (4 AMU)'); RECU=makeRecU(); s.value='30'; s.fire('input');
  uok(gasCount(worldOf('ideal').g,1)===30,'the light slider pumps 30'); uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)'); }
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change'); uok(ST.showWatch===true,'the stopwatch shows');
  clickU('stopwatch start / stop'); playU(); pumpU(24); pauseU(); const g=worldOf('ideal').g;
  uok(Math.abs(g.watch.t-1)<1e-9,'the stopwatch counted 1 ps'); clickU('reset'); uok(g.watch.t===0,'and resets');
  const cc=findLabelledU('collision counter'); cc.checked=true; cc.fire('change');
  chipU('5 ps',3).fire('click'); clickU('count wall hits'); playU(); pumpU(130); pauseU();
  uok(g.counter.on===false&&g.counter.t===5&&g.counter.count>0,'the counter ran 5 ps and stopped ('+g.counter.count+' wall hits)');
  chipU('°C',2).fire('click'); uok(/°C/.test(NODESU.readout.innerHTML),'°C in the readout'); chipU('K',2).fire('click');
  chipU('kPa',2).fire('click'); uok(/ kPa/.test(NODESU.readout.innerHTML),'kPa in the readout'); chipU('atm',2).fire('click');
  const nz=findLabelledU('pressure noise (PhET’s gauge jitter)'); nz.checked=false; nz.fire('change'); uok(g.noiseOn===false,'noise off'); nz.checked=true; nz.fire('change'); }
keyU('3'); uok(ST.view==='energy','3 switches to the energy view'); keyU('1'); uok(ST.view==='ideal','1 back');
{ const g=worldOf('ideal').g; gasRemove(g,0,10); keyU('r'); uok(gasCount(worldOf('ideal').g,0)===100,'r resets the view to its defaults'); }

/* ---- every control, chips, resize ---- */
let ctlErrU=null;
try{
  for(let t=0;t<6;t++){ tabU(t);
    const inputs=NODESU.panel.querySelectorAll('input');
    for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
    pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
    RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===30,'the panel has its 16 sliders and 14 checkboxes ('+inputs.length+')');
  for(const g2 of NODESU.panel.children){ const cws=g2.querySelectorAll('.chips'); for(const cw of cws) for(const ch of cw.children) ch.fire('click'); }
  uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
