/* ============ UI drive test for ph-scale-basics.html ============================ *
 * GENERATED from build/ph-scale/ui_drive_ph-scale.js by make_ui.py, so the half
 * the two sims share cannot drift.  DOM-stub pattern (lineage:
 * projects/simulations/build_buoy/ui_drive_bu.js via
 * build/greenhouse-effect/ui_drive_greenhouse-effect.js, which carries the
 * innerHTML -> textContent fix the shared tools/ui_drive.js still lacks).  Two
 * extra things here: the stub's innerHTML setter runs the text through the
 * sim's own plain(), because every chip label is built with html: and a browser
 * would report the DECODED text (without it, chipU("PhET's rule") finds
 * nothing and the whole law sweep silently tests nothing); and the frame loop
 * only animates while a faucet is open, so every idle-first test closes them
 * and proves the loop quiet before it acts.  One custom pointer action (PhET's
 * pH-meter probe), every tab, every visible slider at its ends, every
 * checkbox, every chip, every button, the keys, resize, and reset-all against
 * a fully disturbed state.                                                   */
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
/* match the WHOLE label, never a substring: sliderU('volume') would find both
   "volume, L" and "liquid poured, L" if either were shortened (Known-bad, build_lagr) */
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
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+' ('+RECU.ops.length+' ops)'); }
function isShown(el){ const chain=[];
  const walk=p=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
/* the loop only animates while a faucet is open: shut them before any idle proof */
function quiet(){ for(const nm of ['the dropper pours (0.05 L/s)','the water faucet runs (0.25 L/s)',
                                   'the drain is open (0.25 L/s)']){
  const cb=findLabelledU(nm); if(cb&&cb.checked){ cb.checked=false; cb.fire('change'); } } }
function bkU(){ return layoutFor(RECU,1400,820).bk; }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===TABS.length,TABS.length+' view tabs were built');
uok(NODESU.panel.children.length===6,'the control panel has its six groups ('+NODESU.panel.children.length+')');
uok(RO().length>300,'the readout rendered ('+RO().length+' chars)');
uok(RO().indexOf('mol/L')<0&&RO().indexOf('molecules')<0,
    'and carries no concentration, as PhET\u2019s Basics does not');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&
    (NODESU.eqbar.innerHTML||'').indexOf('10<sup>&minus;pH</sup>')>=0,
    'the equation bar carries the law, no NaN');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,
    'the panel carries the PhET credit line');
uok((NODESU.panel.textContent||'').indexOf('ph-scale-basics_en.html 1.7.5')>=0,
    'and names the original it was read from');
uok((NODESU.panel.textContent||'').indexOf('Merck Manual')>=0&&
    (NODESU.panel.textContent||'').indexOf('Approximate pH of Foods')>=0,
    'and cites both sources of the measured ranges');
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
   UI_DIAG (python3 jsrun.py ui_drive_ph-scale.js osa diag) */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[590, 78, 60, 780];
const sigsU={};
for(let i=0;i<TABS.length;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing with the faucets shut');
}
uok(new Set(Object.values(sigsU)).size===TABS.length,'every tab draws a different picture');

/* ---- the clock: PhET's dropper, faucet and drain ---- */
tab(0);
{ clickButtonU('empty');
  uok(vTotal()===0,'"empty" empties the beaker');
  uok(RO().indexOf('probe is out')>=0,'and the meter says its probe is out rather than printing a pH');
  const dp=findLabelledU('the dropper pours (0.05 L/s)');
  RECU=makeRecU(); dp.checked=true; dp.fire('change');
  uok(ST.pourSolute,'the dropper is running');
  pumpU(60);
  uok(Math.abs(ST.vSolute-PHET.DROPPER_FLOW)<1e-9,
      'sixty frames put in exactly PhET"s 0.05 L ('+fmt(ST.vSolute,4)+' L)');
  uok(RECU.ops.length>60,'and the loop repaints as it pours ('+RECU.ops.length+' ops)');
  const wf=findLabelledU('the water faucet runs (0.25 L/s)');
  wf.checked=true; wf.fire('change'); pumpU(60);
  uok(Math.abs(ST.vWater-PHET.FAUCET_FLOW)<1e-9,'and the faucet 0.25 L (PhET)');
  const phWas=beakerPH();
  dp.checked=false; dp.fire('change'); wf.checked=false; wf.fire('change');
  const dr=findLabelledU('the drain is open (0.25 L/s)');
  dr.checked=true; dr.fire('change'); pumpU(30);
  uok(Math.abs(beakerPH()-phWas)<1e-9,'draining does not move the pH — it removes solution');
  uok(vTotal()<0.29,'while emptying the beaker ('+fmt(vTotal(),3)+' L)');
  dr.checked=false; dr.fire('change');
  /* pause */
  const rn=findLabelledU('time runs');
  keyU(' '); uok(!ST.running,'space pauses the clock');
  uok(rn.checked===false,'and the checkbox follows');
  dp.checked=true; dp.fire('change');
  const held=vTotal(); pumpU(60);
  uok(vTotal()===held,'paused, the dropper pours nothing');
  idleU('paused: nothing is painted');
  RECU=makeRecU(); clickButtonU('one step');
  uok(vTotal()>held,'"one step" advances one frame even while paused');
  uok(!ST.running,'and leaves the clock paused');
  uok(RECU.ops.length>20,'and repaints at once ('+RECU.ops.length+' ops)');
  keyU(' '); uok(ST.running,'space starts it again');
  dp.checked=false; dp.fire('change');
  clickButtonU('autofill 0.5 L');
  uok(Math.abs(vTotal()-PHET.AUTOFILL_VOLUME)<1e-12&&ST.vWater===0,
      'autofill puts back PhET"s 0.5 L of the liquid alone');
  keyU('e'); uok(vTotal()===0,'the e key empties');
  keyU('a'); uok(Math.abs(vTotal()-PHET.AUTOFILL_VOLUME)<1e-12,'and a autofills'); }

/* ---- the two volume sliders, with the brim clamp ---- */
quiet(); idleU('idle before the volume sliders');
{ const vs=sliderU('liquid poured, L'), vw=sliderU('water added, L');
  uok(!!vs&&isShown(vs)&&!!vw&&isShown(vw),'both volume sliders are on show');
  RECU=makeRecU(); vs.value='0.1'; vs.fire('input');
  uok(Math.abs(ST.vSolute-0.1)<1e-12,'the liquid slider sets 0.10 L');
  uok(RECU.ops.length>40,'and the view redrew at once ('+RECU.ops.length+' ops)');
  vw.value='1.1'; vw.fire('input');
  uok(Math.abs(vTotal()-PHET.BEAKER_VOLUME)<1e-12,'and the water slider fills it to the brim');
  const want=fmt(mixExact(soluteById(ST.solute).pH,0.1,PHET.WATER_PH,1.1),4);
  uok(RO().indexOf(want)>=0,'the readout prints the exact diluted pH, '+want);
  vs.value='1.2'; vs.fire('input');
  uok(ST.vWater===0&&Math.abs(ST.vSolute-1.2)<1e-12,
      'pushing the liquid to the brim pushes the water out');
  uok(Math.abs(beakerPH()-soluteById(ST.solute).pH)<1e-12,
      'and undiluted the meter reads the stock pH exactly');
  vw.value='1.2'; vw.fire('input');
  uok(ST.vSolute===0&&Math.abs(beakerPH()-7)<1e-12,'and a beaker of water alone is exactly pH 7');
  vs.value='0.5'; vs.fire('input'); vw.value='0'; vw.fire('input'); }

/* ---- the custom action: PhET's pH-meter probe, dragged through the loop ---- */
{ tab(0); quiet(); idleU('idle before the probe drag');
  const bk=bkU();
  const px=bkX(bk,PROBE.x), py=bkY(bk,PROBE.y);
  /* NOT on the probe's exact pixel: a hit test narrowed to zero still catches an exactly
     centred click, so the grab is fired 7 px off centre */
  NODESU.scene.fire('pointerdown',{clientX:px+7,clientY:py-8});
  uok(DRAG.what==='probe','pointer-down 7 px from the probe grabs it');
  NODESU.scene.fire('pointerup',{});
  NODESU.scene.fire('pointerdown',{clientX:px+60,clientY:py-8});
  uok(DRAG.what===null,'but 60 px away does not');
  NODESU.scene.fire('pointerup',{});
  /* the pointerUP handler calls refresh() and re-arms `dirty`, so the next pumped frame
     repaints whether or not the GRAB did anything — which is exactly how the grab's own
     dirty flag survived the first sweep (Known-bad: anything that forces a draw between
     an idle proof and the action re-arms the flag) */
  idleU('idle again before the grab itself');
  NODESU.scene.fire('pointerdown',{clientX:px+7,clientY:py-8});
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
  uok(gA.length>400,'the grab repaints through the frame loop');
  idleU('and drains (proven idle)');
  /* sideways first, then up: one axis at a time, so a frozen axis cannot hide */
  const xWant=bkX(bk,0.25);
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:py,buttons:1});
  uok(Math.abs(PROBE.x-0.25)<0.01,'the probe follows the pointer sideways ('+fmt(PROBE.x,3)+')');
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
  uok(gB.length>400&&gB!==gA,'and the sideways move repaints a DIFFERENT picture');
  idleU('idle again');
  const yWant=bkY(bk,0.80);
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:yWant,buttons:1});
  uok(Math.abs(PROBE.y-0.80)<0.01,'and vertically ('+fmt(PROBE.y,3)+')');
  RECU=makeRecU(); pumpU(1); const gC=geomU(RECU);
  uok(gC.length>400&&gC!==gB,'the vertical move repaints a different picture again');
  uok(!probeInLiquid()&&RO().indexOf('probe is out')>=0,
      'lifted above the surface the meter stops reading, and says so');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf('probe out of the liquid')>=0,'and the meter face says so too');
    uok(textsU(RECU).indexOf('—')>=0,'with a dash where the number was'); }
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:bkY(bk,0.1),buttons:1});
  uok(probeInLiquid(),'dipped again it reads');
  { RECU=makeRecU(); tab(0);
    uok(textsU(RECU).indexOf(phPlain(beakerPH()))>=0,'and the meter face prints the pH'); }
  NODESU.scene.fire('pointermove',{clientX:xWant,clientY:bkY(bk,3),buttons:1});
  uok(PROBE.y<=1.3001,'dragged far above the beaker it clamps');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  idleU('idle before the miss');
  NODESU.scene.fire('pointerdown',{clientX:bkX(bk,0.9),clientY:bkY(bk,0.5)});
  uok(DRAG.what===null,'empty glass grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and paints nothing');
  NODESU.scene.fire('pointerup',{});
  tab(2);
  NODESU.scene.fire('pointerdown',{clientX:px+7,clientY:py-8});
  uok(DRAG.what===null,'and a view with no beaker in it ignores the pointer entirely');
  NODESU.scene.fire('pointerup',{});
  tab(0); PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; }

/* ---- the twelve liquids ---- */
{ tab(0); quiet();
  uok(!!chipU('orange juice',12)&&!!chipU('drain cleaner',12),'the twelve liquids are a chip row');
  for(const s of SOLUTES){
    const ch=chipU(s.name,12);
    uok(!!ch,'chip for '+s.name);
    if(!ch) continue;
    ch.fire('click');
    uok(ST.solute===s.id,s.name+' is selected');
    clickButtonU('autofill 0.5 L');
    uok(Math.abs(beakerPH()-s.pH)<1e-12,'and undiluted it reads PhET"s pH '+s.pH);
  }
  chipU('orange juice',12).fire('click'); clickButtonU('autofill 0.5 L'); }

/* ---- the two dilution laws ---- */
{ /* chicken soup, not orange juice: the gap between the laws is an odd function about
     pH 7 that peaks near 5 and 9, so at pH 3.5 it is only 0.0015 and a test there would
     pass on a rule that had been quietly replaced by the exact one */
  chipU('chicken soup',12).fire('click');
  const vs=sliderU('liquid poured, L'), vw=sliderU('water added, L');
  vs.value='0.1'; vs.fire('input'); vw.value='1.1'; vw.fire('input');
  uok(!!chipU('exact (Kw)',2)&&!!chipU('PhET’s rule',2),'the two laws are chips');
  chipU('exact (Kw)',2).fire('click');
  const e=beakerPH();
  chipU('PhET’s rule',2).fire('click');
  const p=beakerPH();
  uok(ST.law==='phet','PhET"s rule is selected');
  uok(Math.abs(p-mixPhet(5.8,0.1,1.1))<1e-12,'and the model uses it');
  uok(Math.abs(e-p)>0.05,'the two laws differ here by '+fmt(Math.abs(e-p),4)+' pH');
  uok(RO().indexOf(fmt(e,4))>=0&&RO().indexOf(fmt(p,4))>=0,
      'and the readout prints both, side by side');
  chipU('exact (Kw)',2).fire('click');
  chipU('orange juice',12).fire('click');
  vs.value='0.5'; vs.fire('input'); vw.value='0'; vw.fire('input'); }


/* ---- this build's own view: the twelve liquids as a table ---- */
tab(1); quiet();
{ RECU=makeRecU(); tab(1);
  const tx=textsU(RECU);
  for(const s of SOLUTES) uok(tx.indexOf(s.name)>=0,'the table lists '+s.name);
  uok(tx.indexOf('4.58')>=0,'and prints orange juice’s diluted pH');
  uok(tx.indexOf('7.37–7.43')>=0,'and blood’s sourced range');
  uok(tx.filter(t=>t==='not sourced').length===8,
      'and says "not sourced" for exactly the eight that are not ('
      +tx.filter(t=>t==='not sourced').length+')');
  uok(tx.some(t=>t.indexOf('diluted 12x')>=0),'the diluted column is headed');
  assertCleanU(RECU,'the liquids table');
  /* the liquid chip highlights the row, so a different chip is a different picture.
     Compared on the GEOMETRY, not on sigU: length-plus-count is the same for two
     different rows of the same table, and the assertion passed on a view that had not
     changed at all. */
  const before=geomU(RECU);
  chipU('drain cleaner',12).fire('click');
  RECU=makeRecU(); tab(1);
  uok(geomU(RECU)!==before,'picking another liquid redraws the table');
  uok((NODESU.eqbar.innerHTML||'').indexOf('factor of ten')>=0,
      'and the equation bar carries this view’s own line');
  chipU('orange juice',12).fire('click'); }

/* ---- the two analysis views ---- */
tab(2);
{ RECU=makeRecU(); tab(2);
  const tx=textsU(RECU);
  uok(tx.some(s=>s.indexOf('exact: mix C')>=0),'the dilution view names the exact law');
  uok(tx.some(s=>s.indexOf('averaging the pH')>=0),'and the wrong one');
  uok(tx.some(s=>s.indexOf('odd about pH 7')>=0),'and states the symmetry it draws');
  uok(RO().indexOf('net acid C')>=0,'the readout carries the stock net acid');
  assertCleanU(RECU,'the dilution view');
  const before=RO();
  chipU('drain cleaner',12).fire('click');
  uok(RO()!==before,'switching the liquid redraws the curves'); }
tab(3);
{ RECU=makeRecU(); tab(3);
  const tx=textsU(RECU);
  uok(tx.some(s=>s.indexOf('MEASURED ranges')>=0),'the scale view names the measured ranges');
  uok(tx.indexOf('blood 7.4')>=0,'and places blood on the scale');
  uok(tx.some(s=>s.indexOf('one unit of pH is one decade')>=0),'and states what a pH unit is');
  uok(RO().indexOf('7.37&ndash;7.43')>=0,'the readout carries blood"s sourced range');
  assertCleanU(RECU,'the scale view'); }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='beaker','1 is the beaker');
  keyU('3'); uok(ST.view==='dilution','3 is dilution');
  keyU('4'); uok(ST.view==='scale','4 is the scale');
  keyU('9'); uok(ST.view==='scale','9 is not a view');
  keyU('2'); uok(ST.view==='liquids','2 is the liquids'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===6,'the panel has its two sliders and four checkboxes ('+inputs.length+')');
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
    /* the two analysis views carry chip rows and no sliders at all, so an input count
       is the wrong floor for them: count every control */
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

/* ---- the panel shows each view its own groups ---- */
{ const g=NODESU.panel.children;
  tab(0); uok(g[0].hidden===false&&g[1].hidden===false&&g[2].hidden===false,
    'the beaker shows the liquid, the beaker and the law');
  tab(1); uok(g[1].hidden===true&&g[2].hidden===false,
    'the liquids table keeps the law and drops the beaker');
  tab(2); uok(g[0].hidden===false&&g[1].hidden===true,'so does dilution');
  tab(3); uok(g[1].hidden===true&&g[2].hidden===true,
    'and the scale drops both');
  tab(0); }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(0); quiet();
  sliderU('liquid poured, L').value='0.1'; sliderU('liquid poured, L').fire('input');
  sliderU('water added, L').value='0.6'; sliderU('water added, L').fire('input');
  chipU('vomit',12).fire('click');
  chipU('PhET’s rule',2).fire('click');
  PROBE.x=0.15; PROBE.y=0.9;
  const dp=findLabelledU('the dropper pours (0.05 L/s)');
  dp.checked=true; dp.fire('change'); pumpU(30);
  uok(ST.solute==='vomit'&&ST.law==='phet'&&ST.pourSolute,'the state is disturbed');
  uok(ST.vSolute>0.1,'and the model has run');
  quiet(); idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true, firstBad='';
  for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]){ same=false; if(!firstBad) firstBad=k; }
  uok(same,'reset all restores every default'+(same?'':' (first: '+firstBad+')'));
  uok(PROBE.x===PROBE0.x&&PROBE.y===PROBE0.y,'and the probe"s position');
  uok(RECU.ops.length>=6,'reset repaints ('+RECU.ops.length+' ops)');
  uok(findLabelledU('the dropper pours (0.05 L/s)').checked===false,'the checkboxes follow');
  uok(chipU('orange juice',12).className==='chip on'&&chipU('exact (Kw)',2).className==='chip on',
      'the chips follow');
  uok(Math.abs(+sliderU('liquid poured, L').value-DEFAULTS.vSolute)<1e-12,'the sliders follow');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
