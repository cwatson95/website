
/* ============ UI drive test for energy-forms-and-changes.html ============== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js ->
 * build/wave-on-a-string/ui_drive_wave-on-a-string.js).  The three
 * sim-specific thresholds: chip rows are found by exact label AND arity (5
 * presets, 4 sources, 2 converters, 4 users, 5 pairs, 2 materials, 2 speeds);
 * the panel has 6 groups; 13 inputs (8 sliders, 5 checkboxes).  Every drag
 * is tested THROUGH the frame loop from a proven-idle baseline (paused), and
 * every reset against a sentinel. */
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
function sliderRowU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function parentOfU(target){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch===target) hit=n; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const rc=findLabelledU('time runs'); if(rc.checked){ rc.checked=false; rc.fire('change'); } }
function playU(){ const rc=findLabelledU('time runs'); if(!rc.checked){ rc.checked=true; rc.fire('change'); } }
function setSliderU(label,v){ const s=sliderU(label); s.value=String(v); s.fire('input'); return s; }
function benchMapU(){ return benchGeo(makeRecU(),1400,820).map; }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the bench|the systems|the heat ledger|the energy flow|equilibrium','the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===6,'the control panel has its 6 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(NODESU.readout.innerHTML.indexOf('6 chunks')>=0&&NODESU.readout.innerHTML.indexOf('34 chunks')>=0,'PhET’s start: 6 chunks in the iron, 34 in the water');
uok(ST.view==='bench'&&ST.running===true&&ST.lev0===0&&ST.lev1===0,'PhET’s start: the bench, playing, burners off');

/* ---- every tab draws, differently, cleanly (floors from the t = 0 emission) ---- */
const FLOORSU=[60,60,40,20,40];
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  uok((NODESU.eqbar.innerHTML||'').length>60&&(NODESU.readout.innerHTML||'').indexOf('NaN')<0,'tab '+i+': the equation bar and readout rendered, no NaN');
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');

/* ---- a live but ignored control is hidden (Known-bad) ---- */
const visU=g=>{ let n=g; return n&&!n.hidden; };
{ tabU(0); uok(visU(parentOfU(sliderRowU('left burner')))&&!visU(parentOfU(sliderRowU('water flow'))),'the bench shows its burners and hides the chain');
  tabU(1); uok(!visU(parentOfU(sliderRowU('left burner')))&&visU(parentOfU(sliderRowU('water flow'))),'the systems view shows the chain and hides the burners');
  uok(sliderRowU('pedalling').hidden===true&&sliderRowU('water flow').hidden===false,'only the faucet’s slider shows while the faucet is the source');
  uok(sliderRowU('clouds').hidden&&sliderRowU('teapot burner').hidden,'the sun’s and the teapot’s sliders are hidden');
  tabU(4); uok(visU(parentOfU(sliderRowU('hot block')))&&!visU(parentOfU(sliderRowU('left burner'))),'equilibrium shows the pair only'); }

/* ---- paused, every view idles; equilibrium idles even while time runs ---- */
pauseU(); uok(ST.running===false,'the "time runs" box pauses');
for(let i=0;i<5;i++){ tabU(i); idleU('tab '+i+' paints nothing while paused'); }
playU(); tabU(4); idleU('equilibrium is static: nothing to paint while time runs');

/* ---- the bench runs through the frame loop ---- */
tabU(0);
{ const s=setSliderU('left burner',1); uok(ST.lev0===1,'the left burner slider sets heat 1');
  chipU('heat the iron',5).fire('click'); uok(ST.preset==='heat'&&chainOf(BENCH,0)[0]===2,'the “heat the iron” preset puts the iron on the left burner');
  uok(ST.lev0===1,'and lights it');
  /* 5000 W needs a second for one 5019-J chunk to cross: pump 2.5 s between the frames */
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU), rA=NODESU.readout.innerHTML; pumpU(150); RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
  uok(gA.length>50&&gB.length>50&&gA!==gB,'two pumped frames 2.5 s apart draw DIFFERENT pictures (chunks arrive in the iron)');
  uok(NODESU.readout.innerHTML!==rA,'and the readout moves on (the iron’s temperature)');
  uok(BENCH.steps>15,'the bench stepped through the loop ('+BENCH.steps+')');
  uok(NODESU.readout.innerHTML.indexOf('5.00 kW into the iron')>=0,'the readout reports the burner’s 5.00 kW into the iron'); }
/* fast forward: x4 */
{ const n0=BENCH.steps; pumpU(30); const d1=BENCH.steps-n0;
  chipU('fast ×4',2).fire('click'); uok(ST.speed==='fast','fast ×4 selected');
  const n1=BENCH.steps; pumpU(30); const d4=BENCH.steps-n1;
  uok(d4>=3.5*d1&&d4<=4.5*d1,'x4 takes four times the steps per frame ('+d1+' then '+d4+')');
  chipU('normal',2).fire('click'); uok(ST.speed==='normal','back to normal'); }
/* the step button and the step key: exactly one step, paused */
pauseU(); idleU('paused before stepping');
{ const n0=BENCH.steps; uok(clickButtonU('step'),'found the step button'); uok(BENCH.steps===n0+1,'step takes exactly one 1/60-s step');
  keyU('.'); uok(BENCH.steps===n0+2,'the . key steps too'); idleU('and the loop is idle again after the step repaint'); }
/* the presets, each against a sentinel */
for(const P of BENCH_PRESETS){
  BENCH.t=99; const c=chipU(P.name,5); uok(!!c,'found the preset chip '+P.name); c.fire('click');
  uok(ST.preset===P.id&&BENCH.t===0,'the preset '+P.id+' resets the bench (sentinel t = 99 cleared)');
}
uok(chainOf(BENCH,2)[0]===2&&ST.lev0===1,'“boil the water” sets the water on the lit left burner');
chipU('hot iron into water',5).fire('click'); uok(Math.abs(bodyT(BENCH.bodies[0])-500)<1e-9&&chainOf(BENCH,0)[0]===4,'“hot iron into water”: a 500-K iron in the water');
/* the burners: the right slider, and linking */
{ chipU('PhET’s start',5).fire('click'); setSliderU('right burner',-0.5); uok(ST.lev1===-0.5,'the right burner cools at 0.5');
  const lk=findLabelledU('link heaters'); lk.checked=true; lk.fire('change'); uok(ST.link&&ST.lev1===ST.lev0,'linking the heaters sets the right to the left');
  setSliderU('left burner',0.3); uok(burnerLevels(ST)[1]===0.3,'linked, the left slider drives both'); setSliderU('right burner',-0.2); uok(ST.lev0===-0.2,'and the right drives the left');
  lk.checked=false; lk.fire('change'); uok(!ST.link,'unlinked'); setSliderU('left burner',0); setSliderU('right burner',0); }
/* energy symbols: the chunks go and come back */
{ tabU(0); pauseU(); const cb=findLabelledU('energy symbols'); uok(!!cb,'found the energy-symbols box');
  RECU=makeRecU(); tabU(0); const on=RECU.ops.length; cb.checked=false; cb.fire('change'); uok(ST.symBench===false,'energy symbols off');
  RECU=makeRecU(); tabU(0); const off=RECU.ops.length; uok(off<on-40,'hiding the symbols removes the chunks from the drawing ('+on+' to '+off+' ops)');
  cb.checked=true; cb.fire('change'); uok(ST.symBench===true,'and back on'); }

/* ---- the REAL drags on the bench, each from a proven-idle baseline ---- */
tabU(0); chipU('PhET’s start',5).fire('click'); pauseU(); idleU('bench, paused: idle before the lever');
{ const map=benchMapU(), kn=leverPos(0,0), X=map.X(kn.x), Y=map.Y(kn.y);
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what==='lever'&&DRAG.k===0,'pointer-down on the left lever grabs it');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the grab repaints through the loop'); idleU('the grab’s own repaint has drained');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:map.Y(0.03+0.02*0.8),buttons:1});
  uok(Math.abs(ST.lev0-0.8)<1e-9,'dragging the lever up sets heat 0.8');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); uok(g1.length>50,'the lever’s move repaints THROUGH the frame loop');
  uok(sliderU('left burner').value==='0.8'||Math.abs(parseFloat(sliderU('left burner').value)-0.8)<1e-9,'and the panel slider follows the lever');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases the lever');
  idleU('paused: the lever does not start time');
  setSliderU('left burner',0); }
idleU('proven idle before grabbing the iron');
{ const map=benchMapU(), b=BENCH.bodies[0], X=map.X(b.x), Y=map.Y(b.y+0.02);
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what==='body'&&BENCH.held&&BENCH.held.i===0,'pointer-down on the iron grabs it');
  idleU('the grab’s repaint drained (proven-idle baseline)');
  RECU=makeRecU(); pumpU(1); const before=geomU(RECU); uok(before==='[]','still idle immediately before the move');
  NODESU.scene.fire('pointermove',{clientX:map.X(0.1),clientY:map.Y(0.15),buttons:1});
  uok(Math.abs(BENCH.bodies[0].x-0.1)<1e-9&&Math.abs(BENCH.bodies[0].y-0.13)<1e-9,'the iron follows the pointer');
  RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); uok(g1.length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again (a drag does not press play)');
  NODESU.scene.fire('pointermove',{clientX:map.X(SPOTS[4]),clientY:map.Y(0.15),buttons:1}); RECU=makeRecU(); pumpU(1); const g2=geomU(RECU);
  uok(g2.length>50&&g2!==g1,'moving again moves the drawing again');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null&&BENCH.held===null,'pointer-up drops it');
  uok(chainOf(BENCH,0)[0]===4&&Math.abs(BENCH.bodies[0].y-0.001)<1e-12,'dropped over the water it lands inside, 1 mm up');
  NODESU.scene.fire('pointermove',{clientX:map.X(-0.2),clientY:map.Y(0.1),buttons:0}); uok(chainOf(BENCH,0)[0]===4,'a hover with no button pressed moves nothing'); }
idleU('proven idle before the thermometer');
{ const map=benchMapU(), p=thermoTip(BENCH,BENCH.therm[2]), X=map.X(p.x), Y=map.Y(p.y+0.03);
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what==='therm'&&DRAG.k===2,'pointer-down on thermometer #3 grabs it');
  idleU('the grab’s repaint drained'); const x0=BENCH.therm[2].x;
  NODESU.scene.fire('pointermove',{clientX:map.X(SPOTS[1]),clientY:map.Y(0.05),buttons:1});
  uok(BENCH.therm[2].x!==x0,'the thermometer moved with the pointer'); RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'and repainted through the loop');
  NODESU.scene.fire('pointerup',{}); uok(BENCH.therm[2].att&&BENCH.therm[2].att.i===1,'dropped on the brick it sticks to the brick');
  RECU=makeRecU(); pumpU(1); tabU(0); uok(textU(RECU).indexOf('#3 22.9 °C')>=0,'and reads the brick’s 22.9 °C on the canvas');
  uok(NODESU.readout.innerHTML.indexOf('#1 in the brick')>=0,'the readout lists it in the brick'); }
{ tabU(1); pauseU(); idleU('systems idle'); NODESU.scene.fire('pointerdown',{clientX:400,clientY:400}); NODESU.scene.fire('pointermove',{clientX:600,clientY:340,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','the systems view ignores the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- the chain: every source, converter and user through the loop ---- */
tabU(1); playU();
{ RECU=makeRecU(); pumpU(1); const g0=geomU(RECU); pumpU(40); RECU=makeRecU(); pumpU(1); uok(geomU(RECU)!==g0,'the faucet chain animates through the loop');
  uok(SYS.steps>30,'the systems stepped ('+SYS.steps+')'); }
const sigSys={};
for(const [lab2,ar,key,id] of [['cyclist',4,'src','biker'],['faucet',4,'src','faucet'],['sun',4,'src','sun'],['teapot',4,'src','teapot'],
                              ['solar panel',2,'conv','panel'],['generator',2,'conv','generator'],
                              ['incandescent bulb',4,'user','incandescent'],['fluorescent bulb',4,'user','fluorescent'],['fan',4,'user','fan'],['beaker heater',4,'user','heater']]){
  const c=chipU(lab2,ar); uok(!!c,'found the chip '+lab2); RECU=makeRecU(); c.fire('click');
  uok(ST[key]===id&&SYS[key]===id,lab2+' selected'); uok(RECU.ops.length>40,lab2+': the view redrew at once'); assertCleanU(RECU,lab2);
  sigSys[lab2]=geomU(RECU);
}
uok(new Set(Object.values(sigSys)).size>=8,'the chain’s pictures differ element by element');
/* each source's own slider: shown for it alone, and it drives the chain */
{ chipU('sun',4).fire('click'); uok(!sliderRowU('clouds').hidden&&sliderRowU('water flow').hidden,'the sun shows the clouds slider only');
  chipU('solar panel',2).fire('click'); setSliderU('clouds',1); pumpU(3); uok(SYS.flows.srcOut===0,'full cloud: no sunlight reaches the panel (PhET)');
  setSliderU('clouds',0); pumpU(3); uok(Math.abs(SYS.flows.srcOut-MAXP)<1e-6,'no cloud: 10 kW reaches it');
  chipU('teapot',4).fire('click'); uok(!sliderRowU('teapot burner').hidden,'the teapot shows its burner slider'); uok(ST.clouds===0,'the sun’s control was reset when it was swapped out');
  setSliderU('teapot burner',1); pumpU(10); uok(SYS.kettle>0,'the teapot’s burner fills the kettle');
  chipU('generator',2).fire('click');
  chipU('cyclist',4).fire('click'); uok(!sliderRowU('pedalling').hidden,'the cyclist shows the pedalling slider'); uok(ST.heat===0,'the teapot’s control was reset');
  setSliderU('pedalling',1); pumpU(60); uok(SYS.omega>0,'pedalling turns the crank ('+fmt(SYS.omega,2)+' rad/s)');
  uok(buttonU('feed me')&&parentOfU(buttonU('feed me')).hidden,'feed me is hidden while he has food');
  SYS.food=1; pumpU(3); uok(SYS.food===0,'sentinel: the food runs out');
  pumpU(2); uok(!parentOfU(buttonU('feed me')).hidden,'feed me appears when the food is gone');
  uok(clickButtonU('feed me')&&Math.abs(SYS.food-FOOD0)<1e-9,'feed me refills 21 chunks'); pumpU(2); uok(parentOfU(buttonU('feed me')).hidden,'and hides again');
  const cb=findLabelledU('energy symbols (systems)'); RECU=makeRecU(); tabU(1); const on=RECU.ops.length;
  cb.checked=false; cb.fire('change'); RECU=makeRecU(); tabU(1); const off=RECU.ops.length; uok(ST.symSys===false&&off<on,'hiding the systems’ symbols removes the chunks ('+on+' to '+off+')');
  cb.checked=true; cb.fire('change');
  chipU('faucet',4).fire('click'); setSliderU('water flow',0.5); pumpU(40); uok(Math.abs(SYS.flows.srcIn-5000)<1e-6,'the faucet at 0.5 supplies 5 kW');
  uok(NODESU.readout.innerHTML.indexOf('in &minus; out &minus; lost &minus; stored')>=0,'the readout carries the chain’s ledger'); }
/* step on the systems */
{ pauseU(); idleU('systems paused'); const n0=SYS.steps; clickButtonU('step'); uok(SYS.steps===n0+1,'step advances the chain one 1/60 s'); keyU('.'); uok(SYS.steps===n0+2,'the . key too'); }

/* ---- the heat ledger and the energy flow draw what their models hold ---- */
{ tabU(2); playU(); chipU('heat the iron',5).fire('click'); pumpU(120); RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.filter(o=>o[0]==='s').length>=6,'the ledger view draws its curves while the bench runs');
  uok(NODESU.readout.innerHTML.indexOf('gained + took &minus; did')>=0,'the ledger readout prints the first law’s residual');
  uok(/drift [0-9.e-]+ J|drift 0 J/.test(NODESU.readout.textContent),'and the chunk identity’s drift for each body');
  tabU(3); RECU=makeRecU(); pumpU(1); uok(RECU.ops.filter(o=>o[0]==='f').length>=6,'the Sankey draws its bands');
  const fc=chipU('fan',4); fc.fire('click'); RECU=makeRecU(); pumpU(1); uok(textU(RECU).indexOf('wind')>=0,'with the fan, a wind band appears'); }

/* ---- equilibrium: every chip, both sliders, the room ---- */
tabU(4);
{ const sig=[];
  for(const P of EQ_PAIRS){ const c=chipU(P.name,5); uok(!!c,'found the pair chip '+P.name); RECU=makeRecU(); c.fire('click'); uok(ST.eqPair===P.id,P.name+' selected'); uok(RECU.ops.length>40,P.name+' drew'); sig.push(geomU(RECU)); assertCleanU(RECU,P.name); }
  uok(new Set(sig).size===5,'every pair draws a different picture');
  chipU('iron in water',5).fire('click'); RECU=makeRecU(); chipU('real materials',2).fire('click'); const gR=geomU(RECU);
  RECU=makeRecU(); chipU('PhET’s materials',2).fire('click'); const gP=geomU(RECU); uok(ST.eqMat==='phet'&&gR!==gP,'real and PhET materials draw different equilibria');
  RECU=makeRecU(); setSliderU('hot block',500); uok(ST.eqT1===500&&RECU.ops.length>40,'the hot block’s slider redraws at once');
  uok(NODESU.readout.innerHTML.indexOf(fmt((eqLinear('iron-water',500,296,'phet',true).Teq),2)+' K')>=0,'the readout prints the new T_eq');
  RECU=makeRecU(); setSliderU('its partner',280); uok(ST.eqT2===280&&RECU.ops.length>40,'the partner’s slider redraws');
  const rb=findLabelledU('the room takes heat'); RECU=makeRecU(); rb.checked=false; rb.fire('change'); uok(ST.eqAir===false,'the room shut out');
  uok(NODESU.readout.innerHTML.indexOf('insulated')>=0,'the readout says insulated'); rb.checked=true; rb.fire('change');
  playU(); idleU('equilibrium is static even while time runs'); }

/* ---- keyboard: views and play/pause ---- */
keyU('1'); uok(ST.view==='bench','1 is the bench'); keyU('5'); uok(ST.view==='eq','5 is equilibrium'); keyU('3'); uok(ST.view==='ledger','3 the heat ledger');
{ const r0=ST.running; keyU(' '); uok(ST.running===!r0,'space toggles play'); keyU(' '); uok(ST.running===r0,'and back'); }

/* ---- every control, every tab, resize, reset all against disturbed state ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===13,'the panel has its 8 sliders and 5 checkboxes ('+inputs.length+')');
  for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); } }
  for(let v=0;v<5;v++){ RECU=makeRecU(); tabU(v); pumpU(2); assertCleanU(RECU,'after the control sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb every kind of state reset all claims to restore */
  tabU(0); chipU('brick on iron, cooling',5).fire('click'); pumpU(30); BENCH.therm[0].tray=false;
  chipU('sun',4).fire('click'); chipU('solar panel',2).fire('click'); chipU('fan',4).fire('click'); chipU('fast ×4',2).fire('click');
  ST.symBench=false; ST.link=true; ST.eqPair='iron-oil'; ST.eqMat='real'; ST.eqT1=600; ST.eqAir=false; ST.clouds=0.5;
  uok(BENCH.steps>0&&SYS.src==='sun','sentinel: the bench has run and the chain is changed');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.src==='faucet'&&ST.conv==='generator'&&ST.user==='heater'&&SYS.src==='faucet'&&SYS.user==='heater','reset all restores the chain');
  uok(ST.speed==='normal'&&ST.symBench===true&&ST.link===false&&ST.lev1===0&&ST.preset==='start','and the bench’s controls');
  uok(BENCH.steps===0&&BENCH.therm[0].tray===true&&chainOf(BENCH,0)[0]===0,'and the bench itself, thermometers home');
  uok(ST.eqPair==='iron-water'&&ST.eqMat==='phet'&&ST.eqT1===380&&ST.eqAir===true,'and the pair');
  uok(ST.view==='bench','keeping the view');
  keyU('2'); BENCH.t=5; SYS.t=5; keyU('r'); uok(BENCH.t===0&&SYS.t===0,'the r key resets all (sentinels cleared)');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
