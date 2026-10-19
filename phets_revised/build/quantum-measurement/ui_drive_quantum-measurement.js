
/* ============ UI drive test for quantum-measurement.html ================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/wave-on-a-string).
 * The three sim-specific thresholds: chip rows are found by exact label AND
 * arity; the panel has 12 groups; 22 inputs (17 sliders, 5 checkboxes).
 * Every canvas interaction is tested THROUGH the frame loop from a
 * proven-idle baseline, one camera axis at a time, and every reset against
 * a sentinel.  No helper here is named run, sig or makeRecorder. */
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
  /* a real browser derives textContent from innerHTML; the shared stub did not (Known-bad) */
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
function sliderU(label){ const r=sliderRowU(label); return r?r.children[1]:null; }   /* the WHOLE label (Known-bad: substring hits) */
function chipU(label,arity){ let hit=null; walkU(ch=>{ if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c; }); return hit; }
/* a VISIBLE button: itself and every ancestor unhidden.  The first version
   checked the button alone, found "observe" in the hidden Bloch group while on
   the coins tab, and clicked the wrong experiment. */
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
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the coins|the photons|the spins|the Bloch sphere|the Born rule|the binomial','the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===12,'the control panel has its 12 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.view==='coins'&&ST.coinScene==='classical'&&COINS.classical.preparing,'PhET\'s start: the classical coin, being prepared');
uok((NODESU.readout.innerHTML||'').indexOf('0.50')>=0,'the readout prints the 0.50 bias off the model');

/* ---- every tab draws, differently, cleanly (floors from the t = 0 emission) ---- */
const FLOORSU=[10,40,30,60,60,50];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error'); assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
for(let i=0;i<6;i++){ tabU(i); idleU('tab '+i+' is idle when nothing moves'); }
uok(ST.view==='binom','the tab clicks set the view');

/* ================= the coins ================= */
tabU(0); idleU('coins idle');
{ const go=buttonU('send to measure'); uok(!!go,'found "send to measure"'); uok(!buttonU('new coin'),'"new coin" is hidden while preparing');
  uok(!buttonU('flip'),'no flip button while preparing (PhET: the test area is empty)');
  const n10=chipU('10',3); uok(!!n10,'found the 10-coin chip'); n10.fire('click'); uok(COINS.classical.set.n===10,'10 identical coins chosen while preparing');
  chipU('100',3).fire('click');
  go.fire('click'); uok(!COINS.classical.preparing,'sent to be measured'); uok(!!buttonU('new coin')&&!buttonU('send to measure'),'the buttons swap');
  uok(COINS.classical.single.state==='revealed'&&COINS.classical.set.kUp===100,'classical coins arrive showing the prepared face (all heads)');
  uok(chipU('100',3).parentNode.hidden===true,'the N chips hide once measuring (PhET)'); }
idleU('arrived: idle');
{ /* a flip runs through the frame loop for PhET's 1 s, then the loop goes idle */
  uok(clickU('flip'),'found flip'); uok(COINS.classical.single.state==='preparing','flipping');
  uok(buttonU('flip').disabled===true,'the buttons are disabled while it flips');
  RECU=makeRecU(); pumpU(1); const a=geomU(RECU); RECU=makeRecU(); pumpU(1); const b=geomU(RECU);
  uok(a.length>50&&b.length>50&&a!==b,'two pumped frames of a flip draw DIFFERENT pictures (the coin spins)');
  pumpU(70); uok(COINS.classical.single.state==='hidden','after 1 s the face is hidden under the cup');
  uok(buttonU('flip').disabled===false,'and the buttons come back (the loop resyncs the panel)');
  idleU('the flip is over: idle');
  uok(clickU('reveal'),'found reveal'); uok(COINS.classical.single.state==='revealed','revealed'); uok(!!buttonU('hide'),'the button now says hide');
  clickU('hide'); uok(COINS.classical.single.state==='hidden','hidden again');
  clickU('flip and reveal'); pumpU(70); uok(COINS.classical.single.state==='revealed','flip and reveal ends revealed');
  uok(COINS.classical.single.nObs===2,'two reveals recorded'); }
{ /* the canvas: clicking the single coin reveals or hides it, repainted through the loop */
  idleU('proven idle before the coin click');
  const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.single.cx,clientY:G.single.cy}); NODESU.scene.fire('pointerup',{});
  uok(COINS.classical.single.state==='hidden','clicking the coin hides it');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'and the click repainted through the loop (dirty flag)'); idleU('then idle');
  NODESU.scene.fire('pointerdown',{clientX:G.C.x+G.C.w/2,clientY:G.C.y+G.C.h/2}); NODESU.scene.fire('pointerup',{});
  uok(COINS.classical.set.state==='hidden','clicking the set hides the set'); pumpU(2);
  clickU('reveal all'); uok(COINS.classical.set.state==='revealed','reveal all');
  clickU('flip all'); pumpU(70); uok(COINS.classical.set.state==='hidden','flip all hides a fresh set');
  clickU('flip and reveal all'); pumpU(70); uok(COINS.classical.set.state==='revealed','flip and reveal all');
  uok(NODESU.readout.innerHTML.indexOf('z = (k')>=0,'the readout shows the set\'s z-score once revealed'); }
{ /* the bias slider, and the preference */
  const s=sliderU('P(heads)'); uok(!!s,'found the P(heads) slider'); s.value='0.73'; s.fire('input'); uok(Math.abs(COINS.classical.p-0.75)<1e-12,'the bias snaps to 0.75 (steps of 0.05, PhET)');
  clickU('new coin'); uok(COINS.classical.preparing,'new coin returns to preparing');
  uok(checkU('classical coins start hidden',true),'found the start-hidden preference'); clickU('send to measure');
  uok(COINS.classical.single.state==='hidden','with it on, the coins arrive under the cup (PhET preference)'); checkU('classical coins start hidden',false); clickU('new coin');
  chipU('tails',2).fire('click'); uok(COINS.classical.init==='tails','prepared tails'); clickU('send to measure'); uok(COINS.classical.set.kUp===0,'and they arrive tails'); clickU('new coin'); }
{ /* the quantum coin: its own scene, observe collapses, reprepare restores */
  const q=chipU('quantum “coin”',2); uok(!!q,'found the quantum chip'); q.fire('click'); uok(ST.coinScene==='quantum','the quantum scene');
  uok(!!sliderU('P(↑) = |α|²'),'its slider is labelled P(up) = |alpha|^2'); uok(chipU('↑',2)&&!chipU('heads',2).parentNode.hidden===false,'basis-state chips replace the orientation chips');
  chipU('↑',2).fire('click'); uok(COINS.quantum.p===1,'the up basis state sets |alpha|^2 = 1'); chipU('↓',2).fire('click'); uok(COINS.quantum.p===0,'down sets 0');
  setSliderU('P(↑) = |α|²',0.5); uok(quantumInit(COINS.quantum.p)==='superposition','between, a superposition');
  clickU('send to measure'); uok(COINS.quantum.single.state==='ready','a quantum coin arrives ready: no face');
  uok(!!buttonU('observe')&&!!buttonU('reprepare')&&!!buttonU('reprepare and observe'),'the quantum buttons: observe, reprepare, reprepare and observe');
  const s0=COINS.quantum.R.s; clickU('observe'); uok(COINS.quantum.R.s!==s0&&COINS.quantum.single.state==='revealed','observing collapses it (a draw)');
  const v=COINS.quantum.single.vals[0]; clickU('hide'); clickU('observe'); uok(COINS.quantum.single.vals[0]===v,'hide and observe again: the same face');
  clickU('reprepare'); pumpU(70); uok(COINS.quantum.single.state==='ready','reprepared: ready again');
  clickU('reprepare and observe all'); pumpU(70); uok(COINS.quantum.set.state==='revealed','reprepare and observe all');
  clickU('new coin'); chipU('classical coin',2).fire('click'); }

/* ================= the photons ================= */
tabU(1); idleU('photons idle');
{ const G=geoU(), map=G.map;
  NODESU.scene.fire('pointerdown',{clientX:map.X(-0.18),clientY:map.Y(0)}); NODESU.scene.fire('pointerup',{});
  uok(PHOT.single.photons.length===1,'clicking the laser emits a photon');
  animatesU('the photon flies through the frame loop');
  pumpU(90); uok(PHOT.single.nV+PHOT.single.nH===1,'and is counted once (after 1.167 s)'); idleU('then the bench is idle');
  const D=G.dial;
  NODESU.scene.fire('pointerdown',{clientX:D.cx+D.r*Math.cos(20*DEG),clientY:D.cy-D.r*Math.sin(20*DEG)});
  uok(ST.phPreset==='custom'&&ST.phCustom===20,'grabbing the dial sets a custom 20 deg');
  uok(PHOT.single.nV+PHOT.single.nH===0,'and clears the single-photon counts (PhET)');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); idleU('the grab\'s repaint drained');
  NODESU.scene.fire('pointermove',{clientX:D.cx+D.r*Math.cos(70*DEG),clientY:D.cy-D.r*Math.sin(70*DEG),buttons:1});
  uok(ST.phCustom===70,'dragging to 70 deg');
  RECU=makeRecU(); pumpU(1); const g2=geomU(RECU);
  uok(g2.length>50&&g2!==g1,'the drag repaints THROUGH the frame loop and moves the drawing');
  NODESU.scene.fire('pointerup',{}); idleU('released: idle');
  uok(!sliderRowU('custom angle').hidden,'the custom-angle slider shows for a custom angle');
  setSliderU('custom angle',30); uok(ST.phCustom===30,'the slider sets 30 deg');
  chipU('vertical (V)',5).fire('click'); uok(ST.phPreset==='vertical'&&sliderRowU('custom angle').hidden,'the V preset hides the custom slider');
  chipU('quantum',2).fire('click'); uok(ST.phBehavior==='quantum','quantum behaviour');
  clickU('emit a photon'); pumpU(90); uok(PHOT.single.nV===1,'a vertical photon always reaches V');
  chipU('horizontal (H)',5).fire('click'); clickU('emit a photon'); pumpU(90); uok(PHOT.single.nH===1&&PHOT.single.nV===0,'an H photon reaches H (and the new preset cleared the V count)');
  chipU('45°',5).fire('click'); chipU('unpolarized',5).fire('click'); uok(ST.phPreset==='unpolarized','unpolarized'); chipU('classical',2).fire('click');
  uok(NODESU.readout.innerHTML.indexOf('0.5000')>=0,'the unpolarized odds read 0.5000'); }
{ /* a beam: it animates continuously, slow motion slows it, the step and pause work */
  chipU('a beam',2).fire('click'); uok(ST.phMode==='many','the beam scene'); uok(!sliderRowU('photons per second').hidden,'the rate slider shows');
  pumpU(30); animatesU('the beam moves every frame');
  const t0=PHOT.many.t; pumpU(10); const dn=PHOT.many.t-t0;
  chipU('slow motion',2).fire('click'); const t1=PHOT.many.t; pumpU(10); const ds=PHOT.many.t-t1;
  uok(Math.abs(ds/dn-0.4)<1e-6,'slow motion runs at x0.4 (PhET): '+(ds/dn).toFixed(3)); chipU('normal',2).fire('click');
  uok(checkU('time runs',false),'found time runs'); idleU('paused, the beam is idle');
  const t2=PHOT.many.t; clickU('step'); uok(Math.abs(PHOT.many.t-t2-2/60)<1e-12,'step advances exactly 2/60 s (PhET)');
  keyU(' '); uok(ST.running===true,'space plays'); pumpU(80); uok(PHOT.many.avgV.value>0,'the V rate builds up');
  setSliderU('photons per second',0); pumpU(120); clickU('clear photon counts'); uok(PHOT.many.nV===0&&PHOT.many.avgV.value===0,'clear photon counts');
  chipU('one photon at a time',2).fire('click'); }

/* ================= the spins ================= */
tabU(2); idleU('spins idle');
{ const G=geoU(), map=G.map;
  NODESU.scene.fire('pointerdown',{clientX:map.X(-0.5),clientY:map.Y(0)}); NODESU.scene.fire('pointerup',{});
  uok(SGS.parts.length===1,'clicking the source shoots a particle');
  animatesU('it flies through the frame loop');
  pumpU(420); uok(SGS.c[0].nU===1,'a +Z atom goes up in SGz'); idleU('then idle (after its 1.5-s rest at the end)'); }
{ const e3=chipU('3 [SGz, SGx]',7); uok(!!e3,'found experiment 3'); e3.fire('click'); uok(ST.sgExp==='e3','experiment 3');
  chipU('+X',3).fire('click'); uok(ST.sgSrc==='+X','a +X source');
  clickU('shoot a particle'); pumpU(300); uok(SGS.c[0].nU+SGS.c[0].nD===1&&SGS.c[1].nU+SGS.c[1].nD+SGS.c[2].nU+SGS.c[2].nD===1,'one particle, measured once at each stage');
  chipU('custom',7).fire('click'); uok(!sliderRowU('|α|² = P(↑z)').hidden&&chipU('+Z',3).parentNode.hidden,'custom: the |alpha|^2 slider replaces the source chips');
  idleU('custom: idle');
  const G=geoU(), D=G.disc;
  NODESU.scene.fire('pointerdown',{clientX:D.cx+D.r,clientY:D.cy}); uok(Math.abs(ST.sgA2-0.5)<1e-12,'grabbing the spin disc along x sets |alpha|^2 = 1/2');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); idleU('the grab repaint drained');
  NODESU.scene.fire('pointermove',{clientX:D.cx,clientY:D.cy-D.r,buttons:1}); uok(ST.sgA2===1,'dragging to +z sets 1');
  RECU=makeRecU(); pumpU(1); const g2=geomU(RECU); uok(g2.length>50&&g2!==g1,'the disc drag moves the drawing through the loop');
  NODESU.scene.fire('pointerup',{}); idleU('released');
  const c1=ST.sgC1, mg=sgMagnetBoxes(G.map,spinsModel(ST),ST)[0].b;
  NODESU.scene.fire('pointerdown',{clientX:mg.x+mg.w/2,clientY:mg.y+mg.h/2}); NODESU.scene.fire('pointerup',{}); uok(ST.sgC1!==c1,'clicking magnet 1 turns it');
  chipU('magnets 2, 3: x',2).fire('click'); uok(ST.sgC2==='x','the second stage turned to x'); chipU('magnet 1: z',2).fire('click'); uok(ST.sgC1==='z','magnet 1 back to z');
  setSliderU('|α|² = P(↑z)',0.3); uok(Math.abs(ST.sgA2-0.3)<1e-12,'the slider sets 0.3');
  uok(NODESU.readout.innerHTML.indexOf('0.300')>=0,'and the readout\'s P(up z) is exactly 0.300'); }
{ chipU('continuous',2).fire('click'); uok(ST.sgMode==='continuous','continuous'); uok(!sliderRowU('particle amount').hidden,'the amount slider shows');
  chipU('4 [SGz, SGz]',7).fire('click'); uok(!chipU('block ↑',2).parentNode.hidden,'the blocker chips show for a two-stage beam');
  chipU('block ↓',2).fire('click'); uok(ST.sgBlock==='down','block down'); setSliderU('particle amount',0.5);
  animatesU('the spin beam moves every frame');
  pumpU(300); uok(SGS.c[2].nU+SGS.c[2].nD===0&&SGS.c[1].nU>0,'with the down beam blocked only the upper magnet counts');
  uok(checkU('expected percentage',false),'found the expected-percentage box'); uok(checkU('expected percentage',true),'and back on');
  clickU('clear spin counts'); uok(SGS.c[0].nU===0,'clear spin counts');
  chipU('single particles',2).fire('click'); chipU('1 [SGz]',7).fire('click'); pumpU(400); }

/* ================= the Bloch sphere ================= */
tabU(3); idleU('Bloch idle');
{ /* the camera: two real drawings through the loop, one axis at a time, from home */
  keyU('r'); idleU('after r: idle');
  NODESU.scene.fire('pointerdown',{clientX:500,clientY:300}); RECU=makeRecU(); pumpU(1); const home=geomU(RECU);
  uok(home.length>200,'the grab repaints the spheres through the loop'); idleU('the grab repaint drained');
  const th0=CAM.theta, ph0=CAM.phi;
  NODESU.scene.fire('pointermove',{clientX:580,clientY:300,buttons:1}); RECU=makeRecU(); pumpU(1); const gH=geomU(RECU);
  uok(CAM.theta!==th0&&CAM.phi===ph0,'a horizontal drag turns theta only');
  uok(gH.length>200&&gH!==home,'and redraws the turned spheres THROUGH the loop');
  NODESU.scene.fire('pointerup',{}); keyU('r'); uok(CAM.theta===CAM_HOME.theta,'r resets the camera'); idleU('home again: idle');
  NODESU.scene.fire('pointerdown',{clientX:500,clientY:300}); RECU=makeRecU(); pumpU(1); const home2=geomU(RECU); idleU('drained');
  NODESU.scene.fire('pointermove',{clientX:500,clientY:360,buttons:1}); RECU=makeRecU(); pumpU(1); const gV=geomU(RECU);
  uok(CAM.phi!==ph0&&CAM.theta===CAM_HOME.theta,'a vertical drag turns phi only'); uok(gV.length>200&&gV!==home2,'and redraws through the loop');
  NODESU.scene.fire('pointerup',{}); idleU('released: idle');
  NODESU.scene.fire('pointermove',{clientX:700,clientY:100,buttons:0}); RECU=makeRecU(); pumpU(2); uok(geomU(RECU)==='[]','a hover with no button does nothing');
  keyU('r'); pumpU(2); }
{ uok(clickU('observe'),'found observe'); uok(BLO.phase==='observed'&&BLO.up+BLO.dn===1,'no field: observed at once'); uok(!!buttonU('reprepare'),'the button now reprepares');
  clickU('reprepare'); uok(BLO.phase==='prepared','reprepared');
  uok(checkU('magnetic field along z',true),'found the field box'); uok(!sliderRowU('delay, ns').hidden&&!sliderRowU('field B / B₀').hidden,'the field shows its strength and delay');
  uok(!!buttonU('start'),'with the field the button says start'); clickU('start'); uok(BLO.phase==='timing','timing');
  animatesU('the state precesses through the frame loop');
  pumpU(200); uok(BLO.phase==='observed','observed at the delay (0.75 ns = 3 s)'); uok(!!buttonU('reprepare'),'and the panel resynced');
  idleU('observed: idle');
  chipU('Y',3).fire('click'); for(let i=0;i<8;i++){ clickU('reprepare'); clickU('start'); pumpU(200); }
  uok(BLO.up===0&&BLO.dn===8,'+X measured along y after 0.75 ns: always down (the axis chip cleared the earlier count)');
  uok(NODESU.readout.innerHTML.indexOf('0.0000')>=0,'the readout says P(up) = 0.0000');
  chipU('× 10 atoms',2).fire('click'); clickU('start'); pumpU(200); uok(BLO.dn===18,'ten atoms at once, all down');
  chipU('X basis',3).fire('click'); uok(ST.bBasis==='X','the X basis'); checkU('show the global phase',true); uok(ST.bGlobal,'the global phase shown');
  setSliderU('field B / B₀',0.5); setSliderU('delay, ns',0.5); uok(ST.bStrength===0.5&&ST.bDelay===0.5,'strength and delay set'); uok(BLO.up+BLO.dn===0,'and the counts cleared (PhET)');
  chipU('+Z',6).fire('click'); uok(ST.bTheta===0,'the +Z preset'); setSliderU('polar angle θ',Math.PI/3); uok(ST.bPreset==='custom','a slider makes it custom');
  setSliderU('azimuth φ',Math.PI); uok(Math.abs(ST.bPhi-Math.PI)<1e-12,'phi set');
  clickU('clear atom counts'); clickU('reset the view'); checkU('magnetic field along z',false); chipU('× 1 atom',2).fire('click'); chipU('Z',3).fire('click'); }

/* ================= the Born rule and the binomial ================= */
tabU(4); idleU('Born idle');
{ const G=geoU(); NODESU.scene.fire('pointerdown',{clientX:G.A.x+G.A.w/2,clientY:G.A.y+20}); uok(ST.bornTh===90,'grabbing the half-angle panel sets Theta = 90');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); idleU('drained');
  NODESU.scene.fire('pointermove',{clientX:G.A.x+G.A.w/3,clientY:G.A.y+20,buttons:1}); uok(ST.bornTh===60,'dragging to 60');
  RECU=makeRecU(); pumpU(1); const g2=geomU(RECU); uok(g2.length>50&&g2!==g1,'the cursor drag moves the drawing through the loop');
  NODESU.scene.fire('pointerup',{});
  setSliderU('middle angle α',45); setSliderU('magnets in the chain',16); setSliderU('shots per point',500); setSliderU('seed',7);
  uok(ST.bornAlpha===45&&ST.bornN===16&&ST.bornShots===500&&ST.bornSeed===7,'the Born sliders'); }
tabU(5); idleU('binomial idle');
{ chipU('N = 10 000',3).fire('click'); uok(ST.binN===10000,'N = 10 000'); uok(NODESU.readout.innerHTML.indexOf('capped')>=0,'the readout says M is capped');
  setSliderU('bias p',0.35); setSliderU('sets M',400); setSliderU('seed ',9); uok(ST.binP===0.35&&ST.binM===400&&ST.binSeed===9,'the binomial sliders');
  idleU('the slider repaints drained');
  NODESU.scene.fire('pointerdown',{clientX:400,clientY:300}); RECU=makeRecU(); pumpU(2); uok(geomU(RECU)==='[]','the binomial view ignores the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- keyboard ---- */
keyU('1'); uok(ST.view==='coins','1 is the coins'); keyU('6'); uok(ST.view==='binom','6 the binomial'); keyU('4'); uok(ST.view==='bloch','4 the Bloch sphere');
{ const r0=ST.running; keyU(' '); uok(ST.running===!r0,'space toggles time'); keyU(' '); uok(ST.running===r0,'and back'); }

/* ---- every control, every tab, resize, reset all against disturbed state ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===22,'the panel has its 17 sliders and 5 checkboxes ('+inputs.length+')');
  for(let v=0;v<6;v++){ tabU(v);
    for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const x of [lo,hi,(lo+hi)/2]){ inp.value=String(x); inp.fire('input'); } }
    uok(NODESU.errbox.style.display!=='block','every input at its ends and middle draws without error on tab '+v);
    RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb every kind of state reset all claims to restore: controls, scenes, the camera */
  tabU(3); ST.bAxis='X'; ST.phCustom=15; ST.sgExp='e6'; ST.binN=10; COINS.classical.p=0.2; sceneStart(COINS.classical); CAM.theta=2.2; CAM.phi=-0.4; PHOT.single.nV=7; BLO.up=5;
  uok(clickU('reset all'),'found reset all');
  uok(ST.bAxis==='Z'&&ST.phCustom===45&&ST.sgExp==='e1'&&ST.binN===100,'reset all restores PhET\'s defaults');
  uok(COINS.classical.p===0.5&&COINS.classical.preparing&&PHOT.single.nV===0&&BLO.up===0,'and every scene');
  uok(CAM.theta===CAM_HOME.theta&&CAM.phi===CAM_HOME.phi,'and the camera'); uok(ST.view==='bloch','keeping the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
