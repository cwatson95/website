/* ============ UI drive test for beers-law-lab.html ======================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js via
 * build/ph-scale/ui_drive_ph-scale.js, which carries the innerHTML -> textContent
 * fix the shared tools/ui_drive.js still lacks, and runs every chip label
 * through the sim's own plain() because chips are built with html:).
 *
 * The frame loop here animates only while something is pouring, draining,
 * evaporating or falling, so every idle-first test shuts all of those AND
 * pumps until the model itself says it has stopped, then proves the loop
 * quiet before acting.  Three custom pointer actions are covered: the
 * concentration meter's probe, the cuvette's draggable right wall (with
 * PhET's snap on release) and the detector's probe.  Every tab, every
 * visible slider at its ends, every checkbox, every chip, every button, the
 * keys, resize, and reset-all against a fully disturbed state.
 * ========================================================================= */
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
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h,String(st.fillStyle)]);},
    strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
    fillText(t,x,y){ops.push(['t',String(t),Math.round(x),Math.round(y)]);}, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||'');
      return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
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
    fire(k,ev){ for(const f of (this._h[k]||[]))
      f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  let _html='';
  /* a browser reports the DECODED text; the shared stub only strips tags, which makes
     every entity-bearing chip label unfindable and the sweep over it vacuous */
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },
    set(v){ _html=''+v; e.textContent=plain(''+v); }});
  return e;
}
const NODESU={};
for(const id of ['scene','panel','tabs','readout','eqbar','tag','hint','errbox','sub'])
  NODESU[id]=mkElU(id==='scene'?'canvas':'div'), NODESU[id].id=id;
globalThis.document={readyState:'complete',getElementById:id=>NODESU[id]||null,createElement:mkElU,
  createTextNode:t=>({nodeType:3,textContent:''+t,children:[]}),addEventListener(){}};
const WINHU={}; let RAFU=null;
globalThis.window={devicePixelRatio:1,addEventListener(k,f){ (WINHU[k]=WINHU[k]||[]).push(f); },
  requestAnimationFrame(f){ RAFU=f; return 1; }};
globalThis.requestAnimationFrame=f=>{ RAFU=f; return 1; };

let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle)
      for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
/* match the WHOLE label, never a substring (Known-bad, build_lagr) */
function sliderU(needle){ const all=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) all.push(ch);
    walk(ch); } };
  walk(NODESU.panel);
  const shown=all.filter(r=>!r.hidden);
  return (shown[0]||all[0]||{children:[]}).children[1]||null; }
function rowOf(inp){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.children&&ch.children.indexOf(inp)>=0) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
/* the chip finder checks the row's ARITY as well as the text (Known-bad, lenses.html) */
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity)
      for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function isShown(el){ const chain=[];
  const walk=p=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
/* the loop animates while anything is pouring, draining, evaporating OR falling: shut
   every source and then pump until the model itself says it has stopped */
function quiet(){
  for(const nm of ['shake the solid in (0.005 mol a grain)',
                   'squeeze the dropper (0.05 L/s of stock)',
                   'the water faucet runs (0.25 L/s)',
                   'the drain is open (0.25 L/s)']){
    const cb=findLabelledU(nm); if(cb&&cb.checked){ cb.checked=false; cb.fire('change'); } }
  const ev=sliderU('evaporation, L/s'); if(ev&&+ev.value!==0){ ev.value='0'; ev.fire('input'); }
  const run=findLabelledU('time runs'); if(run&&!run.checked){ run.checked=true; run.fire('change'); }
  for(let i=0;i<600&&BK.parts.length;i++) pumpU(1);
}
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]',label+' ('+RECU.ops.length+' ops)'); }
function bkU(){ return layoutFor(RECU,1400,820).bk; }
function cvU(){ return cuvetteLayout(RECU,1400,820); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===TABS.length,TABS.length+' view tabs were built');
uok(NODESU.panel.children.length===(SHOW_BEERS?10:7),
    'the control panel has its groups ('+NODESU.panel.children.length+')');
uok(RO().length>400,'the readout rendered ('+RO().length+' chars)');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar carries no NaN');
uok((NODESU.eqbar.innerHTML||'').indexOf('C = n/V')>=0,'and carries the beaker’s law');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,
    'the panel carries the PhET credit line');
uok((NODESU.panel.textContent||'').indexOf('beers-law-lab_en.html')>=0,
    'and names the original it was read from');
uok((NODESU.panel.textContent||'').indexOf('10.25039/CIE.DS.xvudnb9b')>=0,
    'and cites the CIE table by its DOI');
uok((NODESU.panel.textContent||'').indexOf('No molar-absorptivity literature value could be sourced')>=0,
    'and says plainly that no literature eps could be sourced');
{ const bad=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(['LABEL','BUTTON','H3'].indexOf(ch.tagName)>=0&&entReU.test(ch.textContent||''))
      bad.push(ch.tagName+': '+ch.textContent);
    walk(ch); } };
  walk(NODESU.panel);
  uok(!bad.length,'no HTML entity reaches a label, button or heading as literal text'+(bad.length?' ('+bad[0]+')':'')); }

/* ---- every tab draws, differently, cleanly ---- */
quiet();
/* about 70 % of what each tab emits at 1400 x 820 on its first draw; measured with
   UI_DIAG (python3 jsrun.py ui_drive_beers-law-lab.js osa diag) */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS
  :(SHOW_BEERS?[36,49,780,91,56,106]:[39,56,55,106]);
const sigsU={};
for(let i=0;i<TABS.length;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing with everything shut');
}
uok(new Set(Object.values(sigsU)).size===TABS.length,'every tab draws a different picture');

/* ---- the clock: PhET's five mechanisms ---- */
tab(0);
{ clickButtonU('empty');
  uok(BK.V===0&&BK.n===0,'"empty" empties the beaker');
  uok(RO().indexOf('probe is out')>=0,'and the meter says its probe is out');
  const wf=findLabelledU('the water faucet runs (0.25 L/s)');
  RECU=makeRecU(); wf.checked=true; wf.fire('change');
  uok(ST.faucet,'the water faucet is running');
  pumpU(60);
  uok(Math.abs(BK.V-PHET.FAUCET_FLOW)<1e-9,
      'sixty frames put in exactly PhET’s 0.25 L ('+fmt(BK.V,4)+' L)');
  uok(RECU.ops.length>60,'and the loop repaints as it fills ('+RECU.ops.length+' ops)');
  uok(BK.n===0,'water alone brings no solute');
  wf.checked=false; wf.fire('change');
  /* the shaker: PhET's one grain a frame, 1/200 mol each, counted when it lands */
  const sh=findLabelledU('shake the solid in (0.005 mol a grain)');
  uok(!!sh&&isShown(sh),'the shaker box is on show in the solid form');
  sh.checked=true; sh.fire('change');
  pumpU(60);
  uok(BK.parts.length>0,'grains are in the air');
  const dispensed=BK.led.shaker+BK.led.flying;
  uok(Math.abs(dispensed-60*MOLE_PER_PARTICLE)<1e-12,
      'sixty frames dispensed sixty grains, 0.005 mol each ('+fmt(dispensed,4)+' mol)');
  sh.checked=false; sh.fire('change');
  for(let i=0;i<400&&BK.parts.length;i++) pumpU(1);
  uok(BK.parts.length===0,'and every one of them lands');
  uok(Math.abs(BK.n-dispensed)<1e-12,'delivering exactly what was dispensed');
  uok(Math.abs(bkLedgerResidual(BK).n)<1e-15,'with the mole ledger closed');
  /* the dropper lives on the other form */
  const form=chipU('solution',2);
  uok(!!form,'the two solute forms are a chip row');
  form.fire('click');
  uok(ST.form==='solution','the solution form is selected');
  uok(!isShown(findLabelledU('shake the solid in (0.005 mol a grain)')),
      'which hides the shaker box');
  const dp=findLabelledU('squeeze the dropper (0.05 L/s of stock)');
  uok(isShown(dp),'and shows the dropper box');
  const nWas=BK.n, vWas=BK.V;
  dp.checked=true; dp.fire('change'); pumpU(60);
  uok(Math.abs(BK.V-vWas-PHET.DROPPER_FLOW)<1e-9,'a second of the dropper adds 0.05 L (PhET)');
  uok(Math.abs(BK.n-nWas-soluteById(ST.solute).stock*PHET.DROPPER_FLOW)<1e-9,
      'carrying the stock’s own moles');
  dp.checked=false; dp.fire('change');
  chipU('solid',2).fire('click');
  /* the drain does not move the concentration */
  const cWas=bkConc(BK);
  const dr=findLabelledU('the drain is open (0.25 L/s)');
  dr.checked=true; dr.fire('change'); pumpU(30);
  uok(Math.abs(bkConc(BK)-cWas)<1e-9,'draining does not move the concentration');
  uok(BK.V<vWas+PHET.DROPPER_FLOW,'while it empties the beaker');
  dr.checked=false; dr.fire('change');
  /* evaporation does */
  clickButtonU('fill 1 L');
  const ev=sliderU('evaporation, L/s');
  uok(!!ev,'the evaporator is a slider');
  ev.value=String(PHET.EVAPORATION_MAX); ev.fire('input');
  const c0=bkConc(BK), n0=BK.n;
  pumpU(60);
  uok(Math.abs(BK.n-n0)<1e-12,'evaporating removes no solute at all');
  uok(bkConc(BK)>c0||n0===0,'and raises the concentration when there is solute in it');
  uok(Math.abs(BK.V-(1-PHET.EVAPORATION_MAX))<1e-9,'taking exactly 0.25 L of water a second');
  ev.value='0'; ev.fire('input');
  /* pause */
  const rn=findLabelledU('time runs');
  keyU(' '); uok(!ST.running,'space pauses the clock');
  uok(rn.checked===false,'and the checkbox follows');
  const wf2=findLabelledU('the water faucet runs (0.25 L/s)');
  wf2.checked=true; wf2.fire('change');
  const held=BK.V; pumpU(60);
  uok(BK.V===held,'paused, the faucet delivers nothing');
  idleU('paused: nothing is painted');
  RECU=makeRecU(); clickButtonU('one step');
  uok(BK.V!==held||BK.V>=PHET.VOL_MAX,'"one step" advances one frame even while paused');
  uok(!ST.running,'and leaves the clock paused');
  uok(RECU.ops.length>20,'and repaints at once ('+RECU.ops.length+' ops)');
  keyU(' '); uok(ST.running,'space starts it again');
  wf2.checked=false; wf2.fire('change');
  keyU('e'); uok(BK.V===0,'the e key empties');
  keyU('f'); uok(Math.abs(BK.V-PHET.VOL_MAX)<1e-12,'and f fills'); }

/* ---- the two beaker sliders ---- */
quiet(); idleU('idle before the beaker sliders');
{ const ns=sliderU('solute amount, mol'), vs=sliderU('solution volume, L');
  uok(!!ns&&isShown(ns)&&!!vs&&isShown(vs),'both beaker sliders are on show');
  RECU=makeRecU(); ns.value='2'; ns.fire('input');
  uok(Math.abs(BK.n-2)<1e-12,'the solute slider sets 2 mol');
  uok(RECU.ops.length>40,'and the view redrew at once ('+RECU.ops.length+' ops)');
  vs.value='0.5'; vs.fire('input');
  uok(Math.abs(BK.V-0.5)<1e-12,'and the volume slider 0.5 L');
  uok(Math.abs(bkConc(BK)-Math.min(soluteById(ST.solute).cSat,4))<1e-12,
      'so the meter reads n/V, capped at saturation');
  uok(RO().indexOf(fmt(bkConc(BK),PHET.DEC_CONC))>=0,'and the readout prints it');
  ns.value='7'; ns.fire('input'); vs.value='0.005'; vs.fire('input');
  uok(bkSaturated(BK),'7 mol in 5 mL is saturated');
  uok(RO().indexOf('Saturated!')>=0,'and the readout says so');
  uok(bkPrecip(BK)>0,'with solid on the bottom');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf('Saturated!')>=0,'the beaker itself is labelled Saturated!'); }
  vs.value='0'; vs.fire('input');
  uok(bkConc(BK)===0,'an empty beaker reads zero rather than dividing by zero');
  uok(RO().indexOf('NaN')<0,'and the readout has no NaN in it');
  ns.value='0'; ns.fire('input'); vs.value='0.5'; vs.fire('input'); }

/* ---- the custom action: PhET's concentration probe, dragged through the loop ---- */
{ tab(0); quiet();
  sliderU('solute amount, mol').value='1'; sliderU('solute amount, mol').fire('input');
  sliderU('solution volume, L').value='0.8'; sliderU('solution volume, L').fire('input');
  idleU('idle before the probe drag');
  const b=bkU();
  const px=bkX(b,PROBE.x), py=bkY(b,PROBE.y);
  /* NOT on the probe's exact pixel: a hit test narrowed to zero still catches an exactly
     centred click, so the grab is fired 7 px off centre */
  NODESU.scene.fire('pointerdown',{clientX:px+7,clientY:py-8});
  uok(DRAG.what==='probe','pointer-down 7 px from the probe grabs it');
  NODESU.scene.fire('pointerup',{});
  NODESU.scene.fire('pointerdown',{clientX:px+80,clientY:py-8});
  uok(DRAG.what===null,'but 80 px away does not');
  NODESU.scene.fire('pointerup',{});
  /* the pointerUP handler calls refresh() and re-arms `dirty`, so the next pumped frame
     repaints whether or not the GRAB did anything (Known-bad: anything that forces a draw
     between an idle proof and the action re-arms the flag) */
  idleU('idle again before the grab itself');
  NODESU.scene.fire('pointerdown',{clientX:px+7,clientY:py-8});
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
  uok(gA.length>400,'the grab repaints through the frame loop');
  idleU('and drains (proven idle)');
  /* sideways first, then up: one axis at a time, so a frozen axis cannot hide */
  const xWant=bkX(b,0.25);
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:py,buttons:1});
  uok(Math.abs(PROBE.x-0.25)<0.01,'the probe follows the pointer sideways ('+fmt(PROBE.x,3)+')');
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
  uok(gB.length>400&&gB!==gA,'and the sideways move repaints a DIFFERENT picture');
  idleU('idle again');
  const yWant=bkY(b,0.95);
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:yWant,buttons:1});
  uok(Math.abs(PROBE.y-0.95)<0.01,'and vertically ('+fmt(PROBE.y,3)+')');
  RECU=makeRecU(); pumpU(1); const gC=geomU(RECU);
  uok(gC.length>400&&gC!==gB,'the vertical move repaints a different picture again');
  uok(!probeInSolution()&&RO().indexOf('probe is out')>=0,
      'lifted above the surface the meter stops reading, and says so');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf('probe out of the solution')>=0,'and the meter face says so too');
    uok(textsU(RECU).indexOf('—')>=0,'with a dash where the number was'); }
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:bkY(b,0.1),buttons:1});
  uok(probeInSolution(),'dipped again it reads');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf(fmt(bkConc(BK),PHET.DEC_CONC))>=0,
        'and the meter face prints the concentration'); }
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:bkY(b,3),buttons:1});
  uok(PROBE.y<=1.3001,'dragged far above the beaker it clamps');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  idleU('idle before the miss');
  NODESU.scene.fire('pointerdown',{clientX:bkX(b,0.5),clientY:bkY(b,0.5)});
  uok(DRAG.what===null,'the middle of the liquid grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and paints nothing');
  NODESU.scene.fire('pointerup',{});
  PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; }

/* ---- the nine solutes ---- */
{ tab(0); quiet();
  uok(!!chipU('drink mix',9)&&!!chipU('sodium chloride',9),'the nine solutes are a chip row');
  for(const s of SOLUTES){
    const ch=chipU(s.name,9);
    uok(!!ch,'chip for '+s.name);
    if(!ch) continue;
    ch.fire('click');
    uok(ST.solute===s.id,s.name+' is selected');
    uok(BK.n===0,'and choosing it empties the solute (PhET)');
    sliderU('solute amount, mol').value='1'; sliderU('solute amount, mol').fire('input');
    sliderU('solution volume, L').value='1'; sliderU('solution volume, L').fire('input');
    uok(Math.abs(bkConc(BK)-Math.min(s.cSat,1))<1e-12,
        'and 1 mol in 1 L of it reads min(1, Csat) = '+fmt(Math.min(s.cSat,1),3));
  }
  chipU('drink mix',9).fire('click'); }

/* ---- the meter's units, and the beaker's ---- */
{ tab(0); quiet();
  sliderU('solute amount, mol').value='1'; sliderU('solute amount, mol').fire('input');
  sliderU('solution volume, L').value='1'; sliderU('solution volume, L').fire('input');
  uok(!!chipU('mol/L',2)&&!!chipU('%',2),'the meter has both unit chips');
  const before=RO();
  chipU('%',2).fire('click');
  uok(ST.meterUnits==='percent','mass percent is selected');
  uok(RO()!==before,'and the readout changes');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf('%')>=0,'the meter face shows a per cent sign'); }
  chipU('mol/L',2).fire('click');
  uok(!!chipU('mL',2),'the beaker has a millilitre chip');
  chipU('mL',2).fire('click');
  uok(ST.beakerUnits==='milliliters','millilitres are selected');
  uok(RO().indexOf('mL')>=0,'and the readout switches to them');
  chipU('L',2).fire('click');
  const sa=findLabelledU('show solute amount'), sv=findLabelledU('show solution volume');
  RECU=makeRecU(); sa.checked=true; sa.fire('change');
  uok(textsU(RECU).some(s=>s.indexOf('Solute Amount:')===0),
      'the solute-amount box writes PhET’s label on the beaker');
  sa.checked=false; sa.fire('change');
  RECU=makeRecU(); sv.checked=true; sv.fire('change');
  uok(RECU.ops.length>20,'the solution-volume box redraws');
  sv.checked=false; sv.fire('change'); }

/* ---- the cuvette: two more custom drags ---- */
if(SHOW_BEERS){
  tab(1); quiet(); idleU('idle before the cuvette drags');
  const L=cvU();
  const xR=L.X(L.CUV0+cuvetteWidth());
  NODESU.scene.fire('pointerdown',{clientX:xR,clientY:L.axis});
  uok(DRAG.what==='cuvette','pointer-down on the right wall grabs it');
  RECU=makeRecU(); pumpU(1);
  uok(geomU(RECU).length>400,'the grab repaints through the frame loop');
  idleU('idle again, with the wall held');
  NODESU.scene.fire('pointermove',{clientX:xR+L.px*0.62,clientY:L.axis,buttons:1});
  uok(Math.abs(ST.cuvette-1.62)<0.01,'dragging widens it to 1.62 cm ('+fmt(ST.cuvette,3)+')');
  RECU=makeRecU(); pumpU(1);
  uok(geomU(RECU).length>400,'and the move repaints');
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(ST.cuvette-1.6)<1e-9,'and releasing snaps it to PhET’s 0.1 cm ('+fmt(ST.cuvette,3)+')');
  const snapBox=findLabelledU('snap the cuvette to 0.1 cm on release');
  snapBox.checked=false; snapBox.fire('change');
  NODESU.scene.fire('pointerdown',{clientX:L.X(L.CUV0+cuvetteWidth()),clientY:L.axis});
  NODESU.scene.fire('pointermove',{clientX:L.X(L.CUV0+cuvetteWidth())-L.px*0.23,clientY:L.axis,buttons:1});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(ST.cuvette-1.37)<0.01,'with snapping off the width is left where it was dropped');
  snapBox.checked=true; snapBox.fire('change');
  const sl=sliderU('path length l, cm');
  sl.value='1'; sl.fire('input');
  /* the detector probe */
  idleU('idle before the detector drag');
  const L2=cvU();
  const dx=L2.X(L2.CUV0+DET.x), dy=L2.axis;
  NODESU.scene.fire('pointerdown',{clientX:dx+6,clientY:dy-6});
  uok(DRAG.what==='detector','pointer-down on the detector grabs it');
  RECU=makeRecU(); pumpU(1); const dA=geomU(RECU);
  uok(dA.length>400,'the grab repaints');
  idleU('idle with the probe held');
  NODESU.scene.fire('pointermove',{clientX:L2.X(L2.CUV0+4.5),clientY:dy,buttons:1});
  uok(Math.abs(DET.x-4.5)<0.02,'it follows the pointer along the bench');
  RECU=makeRecU(); pumpU(1); const dB=geomU(RECU);
  uok(dB.length>400&&dB!==dA,'and the move repaints a different picture');
  uok(detectorInBeam(),'still in the beam');
  idleU('idle again');
  NODESU.scene.fire('pointermove',{clientX:L2.X(L2.CUV0+4.5),clientY:dy-L2.px*1.4,buttons:1});
  uok(Math.abs(DET.y-1.4)<0.02,'and vertically ('+fmt(DET.y,3)+' cm)');
  uok(!detectorInBeam(),'lifted out of the beam it stops reading');
  uok(RO().indexOf('out of the beam')>=0,'and the readout says so');
  RECU=makeRecU(); pumpU(1);
  uok(geomU(RECU).length>400,'the vertical move repaints too');
  NODESU.scene.fire('pointerup',{});
  DET.x=DET0.x; DET.y=DET0.y;
  /* the light, the detector mode, the wavelength */
  tab(1); quiet();
  const onBox=findLabelledU('the light is on');
  uok(detectorInBeam(),'the probe is back in the beam');
  onBox.checked=false; onBox.fire('change');
  uok(!ST.lightOn,'the light can be switched off');
  uok(RO().indexOf('the light is off')>=0,'and the readout says so');
  { RECU=makeRecU(); tab(1);
    uok(textsU(RECU).indexOf('source off')>=0,'and the source is labelled off'); }
  onBox.checked=true; onBox.fire('change');
  uok(!!chipU('absorbance',2)&&!!chipU('transmittance',2),'the detector has both modes');
  chipU('absorbance',2).fire('click');
  uok(ST.detector==='absorbance','absorbance is selected');
  { RECU=makeRecU(); tab(1);
    uok(textsU(RECU).indexOf('absorbance')>=0,'and the detector face says so');
    uok(textsU(RECU).indexOf(fmt(cuvetteModel().A,PHET.DEC_A))>=0,
        'and prints the absorbance it computed'); }
  chipU('transmittance',2).fire('click');
  /* preset vs variable */
  uok(!isShown(sliderU('wavelength, nm')),'the wavelength slider is hidden in preset mode');
  chipU('variable',2).fire('click');
  uok(ST.lightMode==='variable','variable is selected');
  uok(isShown(sliderU('wavelength, nm')),'which reveals the wavelength slider');
  const wl=sliderU('wavelength, nm');
  RECU=makeRecU(); wl.value='450'; wl.fire('input');
  uok(activeWavelength()===450,'the slider sets 450 nm');
  uok(RECU.ops.length>40,'and redrew at once');
  uok(Math.abs(cuvetteModel().eps-epsAt(ST.blSolution,450))<1e-12,
      'and eps follows the wavelength');
  chipU('preset',2).fire('click');
  uok(activeWavelength()===lambdaMaxOf(ST.blSolution),'preset returns it to lambda_max');
  /* the eight solutions */
  uok(!!chipU('potassium permanganate',8),'the eight solutions are a chip row');
  for(const d of BLSOLS){
    const nm=soluteById(d.solute).name;
    const ch=chipU(nm,8);
    uok(!!ch,'solution chip for '+nm);
    if(!ch) continue;
    ch.fire('click');
    uok(ST.blSolution===d.id,nm+' is selected');
    uok(Math.abs(ST.blConc-d.cDefault)<1e-18,'and its own default concentration comes with it');
    uok(activeWavelength()===lambdaMaxOf(d.id),'and the preset light moves to its peak');
    const M=cuvetteModel();
    uok(Math.abs(M.A-absorbance(M.eps,M.l,M.c))<1e-15,'A = eps l c at the new setting');
    uok(Math.abs(M.T-Math.pow(10,-M.A))<1e-15,'and T = 10^-A');
  }
  chipU('drink mix',8).fire('click');
  /* the concentration slider reaches both ends */
  const cs=sliderU('concentration');
  cs.value='0'; cs.fire('input');
  uok(ST.blConc===0,'the concentration slider reaches zero');
  uok(Math.abs(cuvetteModel().T-1)<1e-15,'where all the light gets through');
  uok(rampColor(ST.blSolution,0).join()===WATER_RGB.join(),'and the cuvette is water-coloured');
  cs.value='1'; cs.fire('input');
  uok(Math.abs(ST.blConc-blsById(ST.blSolution).cMax)<1e-18,'and full scale');
  uok(cuvetteModel().A>1.9,'where the absorbance is about 2 ('+fmt(cuvetteModel().A,3)+')');
  cs.value='0.25'; cs.fire('input');
}

/* ---- the analysis views ---- */
if(SHOW_BEERS){
  tab(2); quiet();
  { RECU=makeRecU(); tab(2);
    const tx=textsU(RECU);
    uok(tx.some(s=>s.indexOf('λ max = ')===0),'the spectrum view marks lambda_max');
    uok(tx.some(s=>s.indexOf('A(λ) = ')===0),'and plots A against wavelength');
    assertCleanU(RECU,'the spectrum view');
    const all=findLabelledU('all eight at once, on a log scale');
    uok(isShown(all),'and offers all eight at once');
    RECU=makeRecU(); all.checked=true; all.fire('change');
    uok(ST.allSpectra,'the overlay is on');
    uok(RECU.ops.length>200,'and it redrew with every curve ('+RECU.ops.length+' ops)');
    { RECU=makeRecU(); tab(2);
      uok(textsU(RECU).some(s=>s.indexOf('log10 ε')>=0),'on a log scale, as it says'); }
    all.checked=false; all.fire('change'); }
  tab(3);
  { RECU=makeRecU(); tab(3);
    const tx=textsU(RECU);
    uok(tx.some(s=>s.indexOf('past 10 mM')===0),'the law view marks where the line stops being true');
    uok(tx.some(s=>s.indexOf('T = 10^-A')>=0),'and names the universal curve');
    assertCleanU(RECU,'the law view');
    uok(!!chipU('against l',2),'and can plot against the path length');
    chipU('against l',2).fire('click');
    uok(ST.lawX==='path','which is selected');
    RECU=makeRecU(); tab(3);
    uok(textsU(RECU).some(s=>s.indexOf('slope = εc')===0),'and names the slope it draws');
    chipU('against c',2).fire('click'); }
}
tab(SHOW_BEERS?4:1);
{ const i=SHOW_BEERS?4:1;
  RECU=makeRecU(); tab(i);
  const tx=textsU(RECU);
  uok(tx.some(s=>s.indexOf('C sat = ')===0),'the ledger view draws the saturation ceiling');
  uok(tx.some(s=>s.indexOf('in beaker ')===0),'and prints what is in the beaker');
  uok(RO().indexOf('residual')>=0,'the readout carries the residual');
  assertCleanU(RECU,'the ledger view'); }
if(!SHOW_BEERS){
  tab(2);
  RECU=makeRecU(); tab(2);
  const tx=textsU(RECU);
  uok(tx.some(s=>s.indexOf('drink mix')>=0),'the solutes view names the solutes');
  uok(tx.some(s=>s.indexOf('vs')>=0&&s.indexOf('mol/L')>=0),
      'and puts PhET’s saturation beside the source’s');
  assertCleanU(RECU,'the solutes view');
}
tab(TABS.length-1);
{ RECU=makeRecU(); tab(TABS.length-1);
  const tx=textsU(RECU);
  uok(tx.some(s=>s.indexOf('really transmits')>=0),'the colour view names what it computed');
  uok(tx.some(s=>s.indexOf('PhET’s interpolation')>=0),'and what PhET does instead');
  uok(RO().indexOf('worst channel gap')>=0,'the readout carries the worst gap');
  assertCleanU(RECU,'the colour view');
  uok(!!chipU('illuminant A',2),'the two illuminants are a chip row');
  const before=RO();
  chipU('illuminant A',2).fire('click');
  uok(ST.illum==='A','illuminant A is selected');
  uok(RO()!==before,'and the readout changes with it');
  uok(trueRGB(colourModel().id,1,0,'A').rgb.join()==='255,255,255',
      'an empty cuvette is still exactly white under it');
  chipU('equal energy',2).fire('click');
  if(!SHOW_BEERS){
    const pl=sliderU('path length, cm');
    uok(!!pl&&isShown(pl),'and a path length to look through');
    RECU=makeRecU(); pl.value='5'; pl.fire('input');
    uok(Math.abs(ST.colourPath-5)<1e-12,'the slider sets 5 cm');
    uok(RECU.ops.length>40,'and redrew at once');
    pl.value='0.2'; pl.fire('input');
  } }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='beaker','1 is the beaker');
  keyU(String(TABS.length)); uok(ST.view==='colour','the last digit is the colour view');
  keyU('9'); uok(ST.view==='colour','9 is not a view');
  keyU('2'); uok(ST.view===TABS[1][0],'2 is the second tab'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length>=(SHOW_BEERS?15:10),'the panel has its sliders and checkboxes ('+inputs.length+')');
  for(let v=0;v<TABS.length;v++){ tab(v); quiet();
    let touched=0;
    for(const inp of inputs){
      if(!isShown(inp)) continue; touched++;
      if(inp.type==='checkbox'){
        if(inp===findLabelledU('time runs')) continue;
        inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change');
        continue; }
      for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); }
      uok(NODESU.errbox.style.display!=='block','tab '+v+': '+
          (rowOf(inp)&&rowOf(inp).children[0]?rowOf(inp).children[0].textContent:'a slider')+
          ' at its ends draws without error'); }
    let chips=0;
    { const walk=n=>{ for(const ch of n.children||[]){
        if(ch.className==='chips'&&isShown(ch)) chips+=ch.children.length; walk(ch); } };
      walk(NODESU.panel); }
    uok(touched+chips>=2,'tab '+v+' has controls on show ('+touched+' inputs, '+chips+' chips)');
    RECU=makeRecU(); tab(v); assertCleanU(RECU,'tab '+v+' after the sweep'); }
  for(const f of (WINHU.resize||[])) f();
  uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
if(NODESU.errbox.style.display==='block') console.log('ERRBOX: '+String(NODESU.errbox.textContent).replace(/\n/g,' | '));

/* ---- one slider must prove it repaints, from a proven-quiet baseline ---- */
{ tab(0); quiet(); idleU('idle before the slider repaint test');
  const ns=sliderU('solute amount, mol');
  RECU=makeRecU(); ns.value='3'; ns.fire('input');
  uok(RECU.ops.length>40,'moving a slider repaints immediately ('+RECU.ops.length+' ops)');
  ns.value='0'; ns.fire('input'); }

/* ---- the panel shows each view its own groups ---- */
{ const g=NODESU.panel.children;
  tab(0); uok(g[0].hidden===false&&g[1].hidden===false&&g[2].hidden===false,
    'the beaker shows the solute, the beaker and the meter');
  if(SHOW_BEERS){
    tab(1); uok(g[1].hidden===true&&g[3].hidden===false,
      'the cuvette hides the beaker group and shows the bench');
    uok(g[2].hidden===true,'and the meter group with it — there is no meter on the bench');
    tab(2); uok(g[4].hidden===false,'the spectrum shows its own box');
    tab(3); uok(g[5].hidden===false,'the law shows its axis chips');
    tab(4); uok(g[1].hidden===false&&g[3].hidden===true,'the ledger is a beaker view again');
    uok(g[2].hidden===true,'but it has no meter either');
    tab(5); uok(g[6].hidden===false,'and the colour view shows the illuminants');
  } else {
    tab(1); uok(g[1].hidden===false,'the ledger is a beaker view');
    uok(g[2].hidden===true,'with the meter group hidden — the meter is on the beaker only');
    tab(2); uok(g[1].hidden===true,'the solutes view drops the beaker controls');
    tab(3); uok(g[3].hidden===false,'and the colour view shows the illuminants');
  }
  tab(0); }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(0); quiet();
  sliderU('solute amount, mol').value='3'; sliderU('solute amount, mol').fire('input');
  sliderU('solution volume, L').value='0.3'; sliderU('solution volume, L').fire('input');
  chipU('potassium permanganate',9).fire('click');
  chipU('%',2).fire('click'); chipU('mL',2).fire('click');
  chipU('solution',2).fire('click');
  ST.illum='A'; ST.lawX='path'; ST.allSpectra=true; ST.showAmount=true; ST.showVolume=true;
  if(SHOW_BEERS){ ST.blSolution='copperSulfate'; ST.lightMode='variable'; ST.wavelength=400;
                  ST.detector='absorbance'; ST.cuvette=1.7; ST.snap=false; }
  PROBE.x=0.15; PROBE.y=0.9; DET.x=5; DET.y=1.2;
  const dp=findLabelledU('squeeze the dropper (0.05 L/s of stock)');
  dp.checked=true; dp.fire('change'); pumpU(30);
  uok(ST.solute==='potassiumPermanganate'&&ST.meterUnits==='percent'&&ST.dropper,
      'the state is disturbed');
  uok(BK.n>0,'and the model has run');
  quiet(); idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true, firstBad='';
  for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]){ same=false; if(!firstBad) firstBad=k; }
  uok(same,'reset all restores every default'+(same?'':' (first: '+firstBad+')'));
  uok(BK.n===0&&Math.abs(BK.V-PHET.VOL_DEFAULT)<1e-12&&BK.parts.length===0,
      'and the beaker itself, which is not a slider value');
  uok(BK.led.shaker===0&&BK.led.dropper===0,'with the ledger started over');
  uok(PROBE.x===PROBE0.x&&PROBE.y===PROBE0.y,'and the meter probe’s position');
  uok(DET.x===DET0.x&&DET.y===DET0.y,'and the detector probe’s');
  uok(RECU.ops.length>=6,'reset repaints ('+RECU.ops.length+' ops)');
  uok(findLabelledU('show solute amount').checked===false,'the checkboxes follow');
  uok(chipU('drink mix',9).className==='chip on'&&chipU('mol/L',2).className==='chip on',
      'the chips follow');
  uok(Math.abs(+sliderU('solute amount, mol').value)<1e-12,'the sliders follow');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
