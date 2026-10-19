
/* ============ UI drive test for gases-intro.html =========================== *
 * DOM-stub harness taken from build/gas-properties/ui_drive_gas-properties.js
 * (which carries the Known-bad fix that innerHTML must strip tags into
 * textContent, or every chip built with html: reads as missing).  Three
 * canvas drags (the left-wall grip, the lid knob, the pump handle), a heater
 * that springs back, PhET's hold-constant chips and their enabling, the P-V
 * view sharing the Laws gas, and the four-law sweep: every action must move
 * the picture THROUGH the frame loop from a proven-idle baseline. */
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
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.panel.children.length>=9,'the control panel has its groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(/11\.[5-9] atm/.test(NODESU.readout.innerHTML),'the readout prints the gauge near 11.7 atm (100 heavy, 300 K, 10 nm)');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');
uok(NODESU.panel.textContent.indexOf('Gases Intro')>=0,'… and it names Gases Intro');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[40,40,36,30];
const sigsU={};
for(let i=0;i<4;i++){
  RECU=makeRecU(); tabU(i);
  const nd=gasCount(worldOf(ST.view).g);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(RECU.arcs>=nd,'tab '+i+' draws every one of its '+nd+' disks ('+RECU.arcs+' arcs)');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');

/* ---- the clock ---- */
tabU(0); playU();
RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
uok(gA.length>50&&gB.length>50&&gA!==gB,'running: two frames draw DIFFERENT pictures (the disks move)');
{ const t0=worldOf('intro').g.t; pumpU(24); uok(Math.abs(worldOf('intro').g.t-t0-24*GAS.DT_FRAME)<1e-9,'24 frames advance the model 1 ps (1/24 ps each)'); }
pauseU();
for(let i=0;i<4;i++){ tabU(i); idleU('tab '+i+' paints nothing while paused'); }
{ tabU(0); const t0=worldOf('intro').g.t; keyU('s'); uok(Math.abs(worldOf('intro').g.t-t0-0.2)<1e-12,'s steps exactly 0.2 ps (PhET’s MODEL_TIME_STEP)'); idleU('and the loop is idle again'); }
{ keyU(' '); uok(ST.running===true,'space runs'); keyU(' '); uok(ST.running===false,'space pauses'); }

/* ---- drag 1: the left-wall grip (PhET pauses the screen; the wall does no work) ---- */
tabU(0); idleU('the box idles before the wall drag');
{ const w=worldOf('intro'), g=w.g, G=geoU(), T1=g.T, W1=g.W;
  const hx=G.handle.x+G.handle.w/2, hy=G.handle.y+G.handle.h/2;
  NODESU.scene.fire('pointerdown',{clientX:hx,clientY:hy});
  uok(DRAG.what==='wall','pointer-down ON the wall grip grabs it');
  uok(w.dragW===W1,'the drag starts from the current width');
  /* the grab ALONE must repaint: the grip turns magenta.  The recorder does
     not capture styles, so assert that a frame was DRAWN (ops emitted from a
     proven-quiet loop), not that the geometry moved. */
  RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>50,'the grab alone repaints through the loop ('+RECU.ops.length+' ops)');
  idleU('… and then the loop is idle again (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:hx+80,clientY:hy,buttons:1});
  uok(w.dragW<W1-500,'moving right narrows the box being dragged ('+w.dragW+' pm)');
  uok(g.W===W1,'… but the model width waits for the release (PhET pauses and redistributes)');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again');
  const dragged=w.dragW;
  uok(dragged===Math.min(15000,Math.max(5000,Math.round((W1-80/G.s)/10)*10)),'the dragged width follows the pointer to 10 pm ('+dragged+')');
  { playU(); const t0=g.t; pumpU(5); uok(g.t===t0,'while the wall is held the model is paused (PhET), even with time running');
    RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','… and a grip held still with time running costs no frames'); pauseU();
    keyU('s'); uok(g.t===t0,'… and the step key does not step it either'); }
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(g.W===dragged,'release: the width is now '+g.W+' pm');
  uok(Math.abs(g.T-T1)<1e-9,'the wall did no work: T unchanged');
  /* PhET spreads the particles over the new width on release; without that
     the narrowed box leaves them outside its own left wall */
  { let outsideU=0; for(let i=0;i<g.n;i++) if(!g.out[i]&&g.x[i]-gasRad(g,i)<g.left-1e-9) outsideU++;
    uok(outsideU===0,'… and every disk was spread into the new width, none left outside ('+outsideU+')'); }
  uok(NODESU.readout.innerHTML.indexOf(fmt(g.W/1000,2)+' nm')>=0,'the readout followed the drag');
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:G.xR-30,clientY:G.yB-30});
  uok(DRAG.what===null,'a pointer-down inside the box grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }
/* drag 2: the lid knob */
idleU('idle before the lid drag');
{ const g=worldOf('intro').g, G=geoU(), k=G.lidKnob, o0=gasOpening(g);
  uok(o0===0,'the lid starts closed');
  NODESU.scene.fire('pointerdown',{clientX:k.x+k.w/2,clientY:k.y+k.h/2}); uok(DRAG.what==='lid','pointer-down on the lid knob grabs it');
  idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:k.x+k.w/2-120,clientY:k.y+k.h/2,buttons:1});
  uok(Math.abs(gasOpening(g)-120/G.s)<=1,'dragging the knob 120 px left opens a gap of exactly 120 px in pm ('+gasOpening(g)+')');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'and the view repainted through the loop');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'released');
  playU(); pumpU(120); pauseU();
  uok(gasCount(g,0)<100||gasOutside(g)>0,'with the lid open, particles leave ('+gasCount(g,0)+' left, '+gasOutside(g)+' escaping)');
  gasSetLid(g,gasMaxLid(g)); uok(gasOpening(g)===0,'closed again'); keyU('r'); }
/* drag 3: the pump handle: a full stroke pumps 50 */
idleU('idle before the pump');
{ const g=worldOf('intro').g, G=geoU(), hnd=G.pumpHandle, n0=gasCount(g,0);
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
  chipU('heavy',2).fire('click'); keyU('r'); }

/* ---- the Intro screen has NO hold-constant panel (PhET: hasHoldConstantFeature false) ---- */
tabU(0);
{ let holdVisible=false;
  for(const g2 of NODESU.panel.children) if((g2.textContent||'').indexOf('hold constant')>=0&&!g2.hidden) holdVisible=true;
  uok(!holdVisible,'the Intro screen hides the Hold Constant group'); }
tabU(1);
{ let holdVisible=false;
  for(const g2 of NODESU.panel.children) if((g2.textContent||'').indexOf('hold constant')>=0&&!g2.hidden) holdVisible=true;
  uok(holdVisible,'the Laws screen shows it'); }

/* ---- the heater springs back; hold-constant chips ---- */
tabU(0);
{ const s=sliderU('cool ← → heat'); uok(!!s,'found the heat slider'); const g=worldOf('intro').g;
  s.value='1'; s.fire('input'); uok(ST.heat===1,'the heat slider sets +1');
  const T0=g.T; playU(); pumpU(24); uok(g.T>T0*1.05,'one second of full heat warms the gas ('+T0.toFixed(1)+' → '+g.T.toFixed(1)+' K)');
  s.fire('change'); uok(ST.heat===0,'released, the slider springs back to 0 (PhET’s snapToZero)'); pauseU(); keyU('r'); }
tabU(1);
{ const g=worldOf('laws').g;
  chipU('Pressure ↕V',5).fire('click'); uok(g.hold==='pressureV','the P↕V chip holds pressure by moving the wall');
  const P0=g.P; const s=sliderU('cool ← → heat'); s.value='0.8'; s.fire('input'); playU(); pumpU(24); s.fire('change'); pauseU();
  uok(Math.abs(g.P/P0-1)<1e-5,'P↕V: heating left P at '+g.P.toFixed(2)+' kPa (started '+P0.toFixed(2)+')');
  uok(/V \/ T \(Charles\)/.test(NODESU.readout.innerHTML),'the readout shows the invariant P↕V keeps: V/T (Charles)');
  uok(NODESU.eqbar.innerHTML.indexOf('<span class="hl">P</span>')>=0,'the equation bar highlights the held P');
  chipU('Volume (V)',5).fire('click'); uok(g.hold==='volume','V held');
  const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.handle.x+5,clientY:G.handle.y+20}); uok(DRAG.what===null,'with V held the wall grip is gone'); NODESU.scene.fire('pointerup',{});
  chipU('Temperature (T)',5).fire('click'); uok(g.hold==='temperature','T held');
  uok(sliderDisabledU('cool ← → heat'),'holding T disables the heater');
  clickU('erase particles'); uok(g.hold==='nothing'&&g.oops==='temperatureEmpty','erasing while holding T: PhET’s Oops, hold released');
  pumpU(2); RECU=makeRecU(); tabU(1); uok(RECU.ops.some(o=>o[0]==='t'&&/Temperature cannot be held constant/.test(o[1])),'the Oops banner is on the canvas');
  uok(chipU('Pressure ↕V',5).disabled===true,'empty box: the P chips are disabled');
  const sH=sliderU('heavy (28 AMU)'); sH.value='100'; sH.fire('input'); uok(gasCount(g,0)===100,'the heavy slider refills 100');
  uok(g.oops===null,'any action clears the Oops'); keyU('r'); }
function sliderDisabledU(label){ const s=sliderU(label); return !!s&&s.disabled===true; }

/* ---- P against V is the SAME gas as the Laws screen ---- */
tabU(1);
{ const gL=worldOf('laws').g;
  tabU(2);
  uok(worldOf('pv').g===gL,'the P-V view shares the Laws screen’s gas, not a copy of it');
  uok(worldKey('pv')==='laws','… by construction (worldKey)');
  chipU('Temperature (T)',5).fire('click'); uok(gL.hold==='temperature','the hold panel works from the P-V view too');
  const W0=gL.W, T0=gL.T;
  for(const wd of [9000,8000,7000]){ gasResize(gL,wd,true); gasRefresh(gL); playU(); pumpU(12); }
  pauseU();
  uok(gL.W===7000,'squeezing at held T reached 7 nm');
  uok(Math.abs(gL.T/T0-1)<1e-9,'… with T unchanged (no work)');
  uok(Math.abs(gL.P*gL.W/(gasPressureOf(gasCount(gL),T0,W0*gL.H*gL.D)*W0)-1)<1e-9,'… and P V constant: Boyle, measured off the model');
  RECU=makeRecU(); tabU(2);
  const txt=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/nm³/.test(txt)&&/300 K/.test(txt),'the P-V view labels its volume axis and its isotherms');
  keyU('r'); }

/* ---- the four-law sweep ---- */
tabU(3);
{ uok(worldOf('sweep').sweep===null,'the sweep view starts idle');
  RECU=makeRecU(); tabU(3);
  uok(RECU.ops.some(o=>o[0]==='t'&&/run the sweep/.test(o[1])),'… and says so on the canvas');
  const win=sliderU('counting window, ps'); win.value='3'; win.fire('input'); uok(ST.sWin===3,'the counting window is 3 ps');
  uok(!!buttonU('run the sweep'),'the run button is there');
  clickU('run the sweep');
  const w=worldOf('sweep');
  uok(!!w.sweep&&!w.sweep.done,'the sweep started'); uok(ST.running===true,'… and started the clock');
  uok(buttonU('stop the sweep')!==null,'the button now offers to stop it');
  let n=0; while(w.sweep&&!w.sweep.done&&n<4000){ pumpU(1); n++; }
  uok(w.sweep.done,'the sweep finished in '+n+' animation frames');
  uok(w.sweep.pts.length===5,'it measured five points ('+w.sweep.pts.length+')');
  let worst=0; for(const p of w.sweep.pts) worst=Math.max(worst,Math.abs(p.inv/w.sweep.pts[0].inv-1));
  uok(worst<1e-6,'Boyle’s P V stayed flat to '+worst.toExponential(1));
  uok(w.sweep.pts.every(p=>p.rate>0),'every point measured a wall-hit rate');
  uok(/points measured/.test(NODESU.readout.innerHTML),'the readout counts them');
  RECU=makeRecU(); tabU(3); assertCleanU(RECU,'the finished sweep');
  uok(RECU.ops.some(o=>o[0]==='t'&&/Boyle/.test(o[1])),'the plot is titled Boyle’s law');
  chipU('Gay-Lussac',4).fire('click'); uok(ST.law==='gay'&&worldOf('sweep').sweep===null,'picking another law clears the sweep');
  clickU('run the sweep'); n=0;
  while(worldOf('sweep').sweep&&!worldOf('sweep').sweep.done&&n<4000){ pumpU(1); n++; }
  uok(worldOf('sweep').sweep.done,'Gay-Lussac ran too');
  const S=worldOf('sweep').sweep;
  uok(S.pts[4].P>S.pts[0].P*2.9,'… and P rose with T (600 K over 200 K: '+(S.pts[4].P/S.pts[0].P).toFixed(2)+'×)');
  /* the hit rate goes as √T, so 600 K over 200 K is √3 = 1.732 — but a 3-ps
     window counts only tens of hits, so the bound has to be the Poisson one
     (selfTest runs the rigorous version at 6 ps) */
  { const rr=S.pts[4].rate/S.pts[0].rate, sd=Math.sqrt(1/S.pts[4].n+1/S.pts[0].n);
    uok(Math.abs(rr/Math.sqrt(3)-1)<4*sd,'… and the walls are struck √3 = 1.732 times as often ('
      +rr.toFixed(2)+'× measured, 4 sd = '+(4*sd).toFixed(2)+' on '+S.pts[0].n+' and '+S.pts[4].n+' hits)');
    let worstZ=0; for(const p of S.pts) worstZ=Math.max(worstZ,Math.abs(p.rate-p.rateTh)/(Math.sqrt(p.n)/p.t));
    uok(worstZ<4,'… and every point is within 4 σ of kinetic theory (worst '+worstZ.toFixed(2)+' σ)'); }
  clickU('run the sweep'); uok(worldOf('sweep').sweep!==null,'run starts a fresh sweep when the last one finished');
  clickU('stop the sweep'); uok(worldOf('sweep').sweep===null,'and stop clears it'); pauseU(); }

/* ---- the collision counter, tools, units, keyboard ---- */
tabU(0); keyU('r'); idleU('idle before the slider repaint test');
{ const s=sliderU('light (4 AMU)'); RECU=makeRecU(); s.value='30'; s.fire('input');
  uok(gasCount(worldOf('intro').g,1)===30,'the light slider pumps 30'); uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)'); keyU('r'); }
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change'); uok(ST.showWatch===true,'the stopwatch shows');
  clickU('stopwatch start / stop'); playU(); pumpU(24); pauseU(); const g=worldOf('intro').g;
  uok(Math.abs(g.watch.t-1)<1e-9,'the stopwatch counted 1 ps'); clickU('reset'); uok(g.watch.t===0,'and resets');
  uok(ST.showCounter===true,'the collision counter is on by default here');
  chipU('5 ps',3).fire('click'); clickU('count wall hits'); playU(); pumpU(130); pauseU();
  uok(g.counter.on===false&&g.counter.t===5&&g.counter.count>0,'the counter ran 5 ps and stopped ('+g.counter.count+' wall hits)');
  const th=hitRateTheory(g,true)*5;
  uok(Math.abs(g.counter.count-th)<4*Math.sqrt(th),'… and its count is kinetic theory’s '+th.toFixed(0)+' within 4√n');
  uok(/measured \/ theory/.test(NODESU.readout.innerHTML),'the readout compares the two');
  chipU('°C',2).fire('click'); uok(/°C/.test(NODESU.readout.innerHTML),'°C in the readout'); chipU('K',2).fire('click');
  chipU('kPa',2).fire('click'); uok(/ kPa/.test(NODESU.readout.innerHTML),'kPa in the readout'); chipU('atm',2).fire('click');
  const nz=findLabelledU('pressure noise (PhET’s gauge jitter)'); nz.checked=false; nz.fire('change'); uok(g.noiseOn===false,'noise off'); nz.checked=true; nz.fire('change'); }
keyU('3'); uok(ST.view==='pv','3 switches to the P-V view'); keyU('1'); uok(ST.view==='intro','1 back');
{ const g=worldOf('intro').g; gasRemove(g,0,10); keyU('r'); uok(gasCount(worldOf('intro').g,0)===100,'r resets the view to its defaults'); }

/* ---- every control, chips, resize ---- */
let ctlErrU=null;
try{
  for(let t=0;t<4;t++){ tabU(t);
    const inputs=NODESU.panel.querySelectorAll('input');
    for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
    pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
    RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===11,'the panel has its 6 sliders and 5 checkboxes ('+inputs.length+')');
  for(const g2 of NODESU.panel.children){ const cws=g2.querySelectorAll('.chips'); for(const cw of cws) for(const ch of cw.children) ch.fire('click'); }
  uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
