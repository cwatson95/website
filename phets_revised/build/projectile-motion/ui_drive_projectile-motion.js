/* ============ UI drive test for projectile-motion.html ==================== *
 * DOM-stub pattern, adapted from tools/ui_drive.js (lineage build_buoy/
 * ui_drive_bu.js).  Its three sim-specific thresholds, re-derived here: the
 * chip-row finders match a row by its exact labels AND its arity, the panel-
 * group floor is this panel's 19 groups, and the input count is this panel's
 * own.  The stub's innerHTML is a setter that fills textContent (Known-bad:
 * the shared stub never does, so label lookups found nothing).  Every action
 * that must repaint is fired from a PROVEN-idle loop and asserted through
 * pumped frames, and the drags assert the drawing MOVED.                     */
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
        else if(want==='.chips'&&ch.className==='chips') out.push(ch);
        else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0,deltaY:0},ev||{})); },
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
function visibleU(n){ for(let p=n;p;p=p.parentEl) if(p.hidden) return false; return true; }
/* whole-label lookups (Known-bad: a substring lookup hits the wrong control) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label&&visibleU(ch)) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function checkU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label&&visibleU(ch)) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity&&visibleU(ch)) for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label&&visibleU(ch)) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function tagU(needle){ let hit=false;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='tag'&&visibleU(ch)&&(ch.textContent||'').indexOf(needle)>=0) hit=true; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(label){ const b=buttonU(label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function frameU(){ RECU=makeRecU(); pumpU(1); return geomU(RECU); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the launch|the vectors|the drag|the lab|the envelope|the hodograph','lower-case noun-phrase tab names');
uok(NODESU.panel.children.length===19,'the control panel has its 19 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(NODESU.readout.innerHTML.indexOf('21.42 m')>=0,'the readout prints the pumpkin\'s 21.42 m off the model');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[30,56,36,30,94,102];   /* ~85 % of the measured t = 0 emission: 35, 67, 43, 35, 110, 121 ops */
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' ('+NODESU.tabs.children[i].textContent+') emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU); console.log('tab '+i+' t=0 emission: '+RECU.ops.length+' ops');
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
for(let i=0;i<6;i++){ NODESU.tabs.children[i].fire('click'); idleU('tab '+i+' paints nothing while nothing flies'); }

/* ---- fire: the loop animates, the readout follows, the landing ends it ---- */
NODESU.tabs.children[0].fire('click'); idleU('the launch view idles before the shot');
uok(clickU('fire'),'found the fire button'); uok(flyingCount('intro')===1,'one projectile in the air');
{ const a=frameU(), b=frameU(); uok(a.length>50&&b.length>50&&a!==b,'two pumped frames draw DIFFERENT pictures (it flies)'); }
{ const ro0=NODESU.readout.innerHTML; pumpU(12); uok(NODESU.readout.innerHTML.indexOf('1 of 3')>=0,'the readout counts it in the air'); }
pumpU(90); uok(flyingCount('intro')===0,'after 1.4 s it has landed'); uok(NODESU.readout.innerHTML.indexOf('0 of 3')>=0,'the readout says so');
uok(NODESU.readout.innerHTML.indexOf('missed')>=0,'21.4 m is not the target at 15 m: missed');
idleU('landed: the loop is idle again');
/* three in the air, the fourth refused, the button disabled */
clickU('fire'); clickU('fire'); clickU('fire'); uok(flyingCount('intro')===3,'three in the air');
uok(buttonU('fire').disabled===true,'the fire button is disabled at three (PhET)'); clickU('fire'); uok(flyingCount('intro')===3,'and a fourth click does nothing');
pumpU(100); uok(flyingCount('intro')===0&&buttonU('fire').disabled===false,'once they land it is enabled again');
uok(clickU('erase'),'found erase'); uok(SCN.intro.trajs.length===0,'erase clears the paths');

/* ---- pause, slow motion, step ---- */
{ const rc=checkU('time runs'); uok(!!rc&&rc.checked===true,'time runs by default'); clickU('fire'); rc.checked=false; rc.fire('change');
  const t0=SCN.intro.t; pumpU(5); uok(SCN.intro.t===t0,'paused: the clock stands'); idleU('and nothing repaints');
  uok(clickU('step'),'found step'); uok(Math.abs(SCN.intro.t-t0-FRAME_DT)<1e-12,'step advances one frame');
  rc.checked=true; rc.fire('change'); const sl=chipU('slow (×0.33)',2); uok(!!sl,'found the slow chip'); sl.fire('click');
  const t1=SCN.intro.t; pumpU(1); uok(Math.abs(SCN.intro.t-t1-FRAME_DT*SLOW)<1e-12,'slow motion: 0.33 of a frame'); chipU('normal',2).fire('click'); pumpU(200); clickU('erase'); }

/* ---- the drags: from a proven-idle loop, the picture must MOVE ---- */
function dragTest(what,label,X0,Y0,X1,Y1,check){
  idleU(label+': idle before the grab');
  RECU=makeRecU(); NODESU.tabs.children[TABS.findIndex(t=>t[0]===ST.view)].fire('click'); const before=geomU(RECU);
  idleU(label+': idle again after the reference drawing');
  NODESU.scene.fire('pointerdown',{clientX:X0,clientY:Y0});
  uok(DRAG.what===what,label+': pointer-down grabs the '+what+' (got '+DRAG.what+')');
  idleU(label+': the grab\'s own repaint has drained');
  NODESU.scene.fire('pointermove',{clientX:X1,clientY:Y1,buttons:1});
  RECU=makeRecU(); pumpU(1); const after=geomU(RECU);
  uok(after.length>50,label+': the move repaints THROUGH the frame loop');
  uok(after!==before,label+': and the drawing moved');
  if(check) check();
  idleU(label+': idle after the move');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,label+': released');
}
NODESU.tabs.children[0].fire('click');
{ const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map, bx=G.piv[0]+0.66*(G.muz[0]-G.piv[0]), by=G.piv[1]+0.66*(G.muz[1]-G.piv[1]);
  dragTest('barrel','aim',bx,by,m.X(5),m.Y(15),()=>uok(ST.i_th===45,'the barrel dragged to (5, 15) aims at 45° ('+ST.i_th+')'));
  uok(NODESU.readout.innerHTML.indexOf('45&deg;')>=0||NODESU.readout.innerHTML.indexOf('45°')>=0,'the readout follows the aim'); }
{ const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map, yp=(G.piv[1]+m.Y0)/2;
  dragTest('height','raise',G.piv[0],yp,G.piv[0],yp-2*m.s,()=>uok(Math.abs(ST.i_h-12)<1e-9,'the pedestal dragged up 2 m stands at 12 m ('+ST.i_h+')')); }
{ const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map;
  dragTest('target','target',m.X(15),m.Y0-2,m.X(19),m.Y0-2,()=>uok(Math.abs(ST.i_tgt-19)<1e-9,'the target follows to 19 m ('+ST.i_tgt+')')); }
{ const cb=checkU('tape measure'); uok(!!cb,'found the tape checkbox'); cb.checked=true; cb.fire('change');
  const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map;
  dragTest('tip','tape',m.X(10),m.Y(0),m.X(13),m.Y(4),()=>uok(Math.abs(tapeLength('intro')-Math.sqrt(185))<1e-6,'the tape tip dragged to (13, 4) reads sqrt(185) = 13.60 m ('+fmt(tapeLength('intro'),3)+')')); }
{ const cb=checkU('data probe'); uok(!!cb,'found the probe checkbox'); cb.checked=true; cb.fire('change');
  const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map;
  dragTest('probe','probe',m.X(8),m.Y(4),m.X(6),m.Y(7),()=>uok(Math.abs(SCN.intro.probe.x-6)<1e-6&&Math.abs(SCN.intro.probe.y-7)<1e-6,'the probe follows to (6, 7)')); }
{ idleU('idle before the miss'); const G=sceneGeo(RECU,1400,820,buildModel()), m=G.map;
  NODESU.scene.fire('pointerdown',{clientX:m.X(25),clientY:m.Y(16)}); uok(DRAG.what===null,'a pointer-down in the empty sky grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }
/* the probe reads a real flight through the UI */
{ ST.i_th=0; ST.i_h=10; clickU('fire'); pumpU(120); SCN.intro.probe={x:7.5,y:10-0.5*9.81*0.25}; NODESU.tabs.children[0].fire('click');
  uok(NODESU.readout.innerHTML.indexOf('0.5000 s')>=0,'the probe on the 0.5-s dot reads 0.5000 s in the readout'); clickU('erase'); }

/* ---- the wheel: zooms a scene through the loop; the analysis views ignore it ---- */
idleU('idle before the wheel');
{ const z0=ST.zoom; NODESU.scene.fire('wheel',{deltaY:-240}); uok(ST.zoom>z0,'the wheel zooms in');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'and the loop repaints (dirty flag)'); idleU('then idles');
  uok(Math.abs(parseFloat(sliderU('zoom').value)-ST.zoom)<1e-9,'the zoom slider follows'); }
NODESU.tabs.children[4].fire('click'); idleU('the envelope idles');
{ const z0=ST.zoom; NODESU.scene.fire('wheel',{deltaY:-500}); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]'&&ST.zoom===z0,'the envelope ignores the wheel: no repaint, no stored zoom');
  NODESU.scene.fire('pointerdown',{clientX:500,clientY:300}); uok(DRAG.what===null,'and the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- a change of air mid-flight, through the UI (the vectors view) ---- */
NODESU.tabs.children[1].fire('click'); idleU('the vectors view idles');
{ clickU('fire'); pumpU(48); const T0=SCN.vectors.trajs[0].F.T; const cb=checkU('air resistance'); uok(!!cb&&cb.checked,'air resistance is on here');
  cb.checked=false; cb.fire('change'); const tr=SCN.vectors.trajs[0];
  uok(tr.changed&&tr.F.T<T0,'switching the air off mid-flight re-routes it from its node (lands sooner: '+fmt(tr.F.T,3)+' s < '+fmt(T0,3)+' s)');
  pumpU(250); uok(flyingCount('vectors')===0,'and it lands'); cb.checked=true; cb.fire('change'); clickU('erase'); }
{ const c=chipU('components',2); uok(!!c,'found the components chip'); c.fire('click'); uok(ST.v_mode==='components','components selected');
  const f=checkU('force'); f.checked=true; f.fire('change'); clickU('fire'); pumpU(30); RECU=makeRecU(); pumpU(1); assertCleanU(RECU,'vectors in flight');
  uok(RECU.ops.filter(o=>o[0]==='t'&&(o[1]==='mg'||o[1]==='vx'||o[1]==='ax')).length>=3,'the component arrows are labelled'); pumpU(200); clickU('erase'); }

/* ---- the lab: the object chips re-range the sliders; dead controls are disabled ---- */
NODESU.tabs.children[3].fire('click');
{ const pc=chipU('piano',10); uok(!!pc,'found the piano chip in the lab row'); pc.fire('click');
  uok(ST.l_m===400&&ST.l_d===2.2&&ST.l_cd===1.2,'the piano brings PhET\'s 400 kg, 2.2 m, 1.2');
  const ms=sliderU('mass'); uok(Math.abs(parseFloat(ms.min)-Math.log10(50))<1e-12&&Math.abs(parseFloat(ms.max)-3)<1e-12,'the mass slider spans the piano\'s 50..1000 kg (log)');
  uok(sliderU('drag coefficient').disabled===true,'C_d is not the piano\'s to change: disabled');
  uok(sliderU('altitude').disabled===true,'with no air the altitude is disabled');
  const air=checkU('air resistance'); air.checked=true; air.fire('change'); uok(sliderU('altitude').disabled===false,'air on: altitude live');
  uok(sliderU('drag coefficient').disabled===true,'with the air on the piano\'s C_d is still its own: disabled');
  chipU('custom',10).fire('click'); uok(sliderU('drag coefficient').disabled===false,'the custom projectile\'s C_d is live');
  ms.value=String(Math.log10(250)); ms.fire('input'); uok(Math.abs(ST.l_m-250)<1e-6,'the log mass slider sets 250 kg ('+ST.l_m+')'); }

/* ---- every control, every chip, every tab ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===49&&inputs.filter(x=>x.type==='checkbox').length===20,'the panel has its 29 sliders and 20 checkboxes ('+inputs.length+')');
  for(let tb=0;tb<6;tb++){ NODESU.tabs.children[tb].fire('click');
    for(const inp of inputs){ if(!visibleU(inp)||inp.disabled) continue;
      if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); }
      else { const lo=parseFloat(inp.min), hi=parseFloat(inp.max); for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
      uok(NODESU.errbox.style.display!=='block','tab '+tb+': a control drives without error'); }
    for(const g of NODESU.panel.children){ if(g.hidden) continue; for(const cw of g.querySelectorAll('.chips')) for(const ch of cw.children){ RECU=makeRecU(); ch.fire('click'); assertCleanU(RECU,'chip "'+ch.textContent+'" on tab '+tb); } }
  }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'the control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
/* a slider repaints at once (proven idle first) */
NODESU.tabs.children[2].fire('click'); idleU('the drag view idles');
{ const s=sliderU('drag coefficient'); RECU=makeRecU(); s.value='0.2'; s.fire('input'); uok(ST.d_cd===0.2,'C_d set to 0.2'); uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(tagU('streamlined'),'the panel names the shape (streamlined at C_d 0.2)'); }

/* ---- keyboard ---- */
keyU('1'); uok(ST.view==='intro','1: the launch'); keyU('f'); uok(flyingCount('intro')===1,'f fires'); keyU('e'); uok(SCN.intro.trajs.length===0,'e erases');
keyU(' '); uok(ST.running===false,'space pauses'); keyU(' '); uok(ST.running===true,'and resumes');
keyU('6'); uok(ST.view==='hodo','6: the hodograph'); keyU('5'); uok(ST.view==='env','5: the envelope');
/* ---- reset all ---- */
ST.i_h=3; ST.zoom=1.7; SCN.intro.tape.x1=2; uok(clickU('reset all'),'found reset all');
uok(ST.i_h===10&&ST.zoom===1&&SCN.intro.tape.x1===10&&ST.view==='env','reset all restores the defaults, the tools and the zoom, and keeps the view');
for(let i=0;i<6;i++){ RECU=makeRecU(); NODESU.tabs.children[i].fire('click'); assertCleanU(RECU,'after the sweep, tab '+i); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
