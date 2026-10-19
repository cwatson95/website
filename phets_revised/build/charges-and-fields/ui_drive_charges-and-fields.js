
/* ============ UI drive test for charges-and-fields.html =================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js via build_buoy/ui_drive_bu.js,
 * whose stub derives textContent from innerHTML).  Nothing in this sim moves by
 * itself, so every view must paint NOTHING while idle, and every action must
 * repaint through the frame loop from a proven-idle baseline: the charge drag,
 * the bin, the sensors, the plot button, the tape, the probe, the camera (one
 * axis at a time) and the wheel.  The three sim-specific thresholds of the
 * shared harness are set here: 5 tabs, 8 panel groups, 18 inputs.          */
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
/* pump real frames: the only path on which the dirty flag matters */
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* whole-label match (Known-bad: a substring lookup hit the wrong control) */
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
function clickButtonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); if(hit) hit.fire('click'); return !!hit; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function frameU(){ RECU=makeRecU(); pumpU(3); return geomU(RECU); }
const roU=()=>NODESU.readout.innerHTML;
const downU=(x,y)=>NODESU.scene.fire('pointerdown',{clientX:x,clientY:y});
const moveU=(x,y)=>NODESU.scene.fire('pointermove',{clientX:x,clientY:y,buttons:1});
const upU=()=>NODESU.scene.fire('pointerup',{});
const planeMapU=()=>planeGeo(RECU,1400,820,PLANE_CAP_FULL,PLANE_CAP_SHORT).map;

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.panel.children.length===8,'the control panel has its 8 groups ('+NODESU.panel.children.length+')');
uok(roU().length>300,'the readout rendered');
uok(NODESU.eqbar.innerHTML.indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>50,'the equation bar rendered');
uok(roU().indexOf(sigf(potentialAt(presetCharges('dipole'),1.5,0.9),3)+' V')>=0,'the readout prints the voltage sensor\'s reading off the model');
uok(ST.view==='plane'&&ST.preset==='dipole'&&ST.charges.length===2,'it opens on the plane with the dipole');

/* ---- every tab draws, differently, cleanly; and idles ---- */
const FLOORSU=[160,75,2000,40,65];      /* ~80 % of what each view emits at boot (measured: 204, 96, 2587, 53, 82) */
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  uok(NODESU.tabs.children[i].className==='active','tab '+i+' is marked active');
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while idle (nothing moves by itself)');
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');
uok(ST.showE===true&&findLabelledU('electric field').checked===true,'the field arrows start on (PhET\'s default)');
uok(findLabelledU('voltage').checked===false&&findLabelledU('values').checked===false&&findLabelledU('grid').checked===false,'voltage, values and grid start off (PhET)');

/* ---- the plane: drag a charge, from a proven-idle baseline ---- */
NODESU.tabs.children[0].fire('click');
idleU('the plane idles before the drag');
{ const map=planeMapU(), c=ST.charges[1], X=map.X(c.x), Y=map.Y(c.y), g0=frameU(), before=JSON.stringify(ST.charges);
  const V0=roU();
  downU(X,Y); uok(DRAG.what==='charge'&&DRAG.k===1,'pointer-down ON the positive charge grabs it');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  moveU(X+66,Y-40); uok(JSON.stringify(ST.charges)!==before,'the move moved the charge');
  close2(ST.charges[1].x,0.5+66/map.s,1e-9,'by 66 px worth of metres');
  const g1=frameU(); uok(g1.length>50&&g1!==g0,'the move repaints THROUGH the frame loop, and the picture changed');
  idleU('and goes idle again'); upU(); uok(DRAG.what===null,'pointer-up releases');
  uok(roU()!==V0,'the readout followed the drag'); uok(ST.eqSeeds.length===0,'moving a charge cleared the plotted equipotential (PhET)');
  uok(ST.preset==='custom'&&chipU('dipole',7).className==='chip','the preset chip lets go: this is now a custom arrangement'); }
function close2(a,b,t,n){ uok(Math.abs(a-b)<=t,n+' ['+a+' vs '+b+']'); }
/* the bin: a new charge, dragged out; one dropped back in */
idleU('idle before the bin');
{ const map=planeMapU(), n0=ST.charges.length;
  downU(map.X(0),map.Y(BIN_GLYPH_Y)); uok(ST.charges.length===n0+1&&ST.charges[n0].q===-1,'pointer-down on the −1 nC source makes a negative charge');
  moveU(map.X(-2.5),map.Y(1.4)); upU(); uok(ST.charges.length===n0+1,'dragged onto the plane, it stays');
  close2(ST.charges[n0].x,-2.5,1e-9,'where it was dropped'); RECU=makeRecU(); pumpU(2); uok(RECU.ops.length>50,'and the plane repainted');
  idleU('idle again');
  downU(map.X(-2.5),map.Y(1.4)); moveU(map.X(0.3),map.Y(-2.0)); upU(); uok(ST.charges.length===n0,'dragged back into the bin, it is removed');
  ST.eqSeeds=[{x:1.5,y:0.9}]; downU(map.X(-0.75),map.Y(BIN_GLYPH_Y)); upU(); uok(ST.charges.length===n0&&ST.eqSeeds.length===1,'a click on the bin makes and unmakes a charge and clears nothing'); }
/* the E-field sensor: from the bin, onto the plane, its reading */
{ const map=planeMapU(), ne=ST.esens.length;
  downU(map.X(0.75),map.Y(BIN_GLYPH_Y)); moveU(map.X(2.2),map.Y(-0.8)); upU();
  uok(ST.esens.length===ne+1,'an E-field sensor dragged out of the bin'); uok(roU().indexOf('#'+(ne+1)+' ')>=0,'appears in the readout');
  const R=sensorReading(ST.charges,ST.esens[ne].x,ST.esens[ne].y); uok(roU().indexOf(sigf(R.mag,3)+' V/m')>=0,'with its reading off the model'); }
/* the voltage sensor: its canvas buttons and its drag */
idleU('idle before the voltage sensor');
{ const map=planeMapU(); ST.eqSeeds=[]; const g=vsGeo(map,ST,1400,820);
  downU(g.plot.x+4,g.plot.y+4); upU(); uok(ST.eqSeeds.length===1,'the sensor\'s canvas plot button plots an equipotential');
  RECU=makeRecU(); pumpU(2); uok(RECU.ops.length>50,'and the plane repaints with it');
  downU(g.clear.x+4,g.clear.y+4); upU(); uok(ST.eqSeeds.length===0,'its clear button clears them');
  idleU('proven idle');
  downU(g.X,g.Y); uok(DRAG.what==='vs','grabbing the crosshair'); moveU(map.X(-1.2),map.Y(1.6)); upU();
  close2(ST.vs.x,-1.2,1e-9,'drags the voltage sensor'); uok(roU().indexOf(sigf(potentialAt(ST.charges,ST.vs.x,ST.vs.y),3)+' V')>=0,'and the readout reads V at its new place');
  keyU('e'); uok(ST.eqSeeds.length===1,'e plots there'); keyU('c'); uok(ST.eqSeeds.length===0,'c clears'); }
/* the tape: switch it on, drag an end, drag its body */
{ const cb=findLabelledU('tape measure'); uok(!!cb&&!cb.checked,'the tape starts in its box'); cb.checked=true; cb.fire('change'); uok(ST.showTape,'the tape is out');
  uok(roU().indexOf('cm')>=0,'the readout gives its length in centimetres');
  idleU('idle before the tape'); const map=planeMapU(), t=ST.tape;
  downU(map.X(t.bx),map.Y(t.by)); uok(DRAG.what==='tapeB','grabbing end B'); moveU(map.X(0.8),map.Y(1.9)); RECU=makeRecU(); pumpU(2); uok(RECU.ops.length>50,'the tape drag repaints'); upU();
  close2(ST.tape.bx,0.8,1e-9,'end B moved'); uok(roU().indexOf(fmt(100*Math.hypot(ST.tape.bx-ST.tape.ax,ST.tape.by-ST.tape.ay),1)+' cm')>=0,'and the length followed'); }
/* sliders and checkboxes repaint at once (proven idle first) */
idleU('idle before the checkbox test');
{ const cb=findLabelledU('voltage'); RECU=makeRecU(); cb.checked=true; cb.fire('change'); uok(ST.showV===true,'voltage on');
  uok(RECU.ops.length>200,'the voltage map drew at once ('+RECU.ops.length+' ops)'); idleU('then idles');
  const e=findLabelledU('electric field'), d=findLabelledU('direction only'); e.checked=false; e.fire('change'); uok(d.disabled===true,'direction only is dimmed with the field off (it would do nothing)');
  e.checked=true; e.fire('change'); uok(d.disabled===false,'and live again with it on'); }

/* ---- field lines: a charge drag re-traces them ---- */
NODESU.tabs.children[1].fire('click'); { const c=chipU('two rows',7); c.fire('click'); uok(ST.preset==='rows'&&ST.charges.length===14,'the two-rows chip sets 14 charges'); }
uok(roU().indexOf('<td class="v good">112</td>')>=0,'the readout counts 112 lines ending on charges');
idleU('field lines idle');
{ const map=planeGeo(RECU,1400,820,LINES_CAP_FULL,LINES_CAP_SHORT).map, c=ST.charges[3], X=map.X(c.x), Y=map.Y(c.y), g0=frameU();
  downU(X,Y); uok(DRAG.what==='charge','a charge grabs in the field-lines view'); idleU('proven idle');
  moveU(X+30,Y+40); const g1=frameU(); uok(g1.length>50&&g1!==g0,'dragging it re-traces the lines through the loop'); upU(); }
{ const s=sliderU('lines per charge'); uok(!!s,'found the lines slider'); idleU('idle before the slider'); RECU=makeRecU(); s.value='8'; s.fire('input');
  uok(ST.nLines===8,'8 lines per charge'); uok(RECU.ops.length>100,'the view redrew at once'); }
{ const f=findLabelledU('equipotentials'), sp=sliderU('equipotentials every, V'); f.checked=false; f.fire('change'); uok(sp.disabled===true,'the spacing slider dims without the equipotentials');
  f.checked=true; f.fire('change'); uok(sp.disabled===false,'and wakes with them'); }

/* ---- the landscape: the camera, one axis at a time, and the wheel ---- */
NODESU.tabs.children[2].fire('click');
function landGeomU(){ RECU=makeRecU(); NODESU.tabs.children[2].fire('click'); return geomU(RECU); }
for(const [nm,dx,dy] of [['horizontal',180,0],['vertical',0,120]]){
  keyU('r'); idleU('the landscape is idle before a '+nm+' drag');
  const th=ST.camTheta, ph=ST.camPhi, before=landGeomU();
  idleU('proven idle after the forced draw');
  downU(500,300); moveU(500+dx,300+dy); RECU=makeRecU(); pumpU(3); const mid=geomU(RECU); upU();
  uok(mid.length>50,'a '+nm+' drag repaints through the frame loop');
  const after=landGeomU(); uok(after!==before,'a purely '+nm+' drag moves the geometry');
  if(dx){ uok(ST.camTheta!==th&&ST.camPhi===ph,'it turned the azimuth only'); } else { uok(ST.camPhi!==ph&&ST.camTheta===th,'it changed the elevation only'); }
}
keyU('r'); pumpU(3); idleU('the loop is idle before the wheel (reset marks dirty, so drain it)');
{ const z=ST.camZoom, g0=landGeomU(); idleU('proven idle');
  NODESU.scene.fire('wheel',{deltaY:-400}); RECU=makeRecU(); pumpU(3); const g1=geomU(RECU);
  uok(ST.camZoom>z,'the wheel zooms in'); uok(g1.length>50,'the wheel repaints through the loop'); uok(g1!==g0,'and the zoomed picture differs from the un-zoomed one');
  uok(roU().indexOf(fmt(ST.camZoom,2)+'&times;')>=0,'the readout followed the zoom'); }
{ const s=sliderU('clip at ±, V'); idleU('idle before the clip slider'); RECU=makeRecU(); s.value='10'; s.fire('input'); uok(ST.vcap===10&&RECU.ops.length>500,'clip at ±10 V redraws at once');
  uok(roU().indexOf('clipped at')>=0,'and the readout says where it is clipped'); }
{ const s=sliderU('azimuth'), s2=sliderU('elevation'); s.value='0.5'; s.fire('input'); s2.value='1.2'; s2.fire('input'); uok(ST.camTheta===0.5&&ST.camPhi===1.2,'the camera sliders set the angles'); }

/* ---- superposition: the probe ---- */
NODESU.tabs.children[3].fire('click'); chipU('dipole',7).fire('click');
idleU('superposition idles');
{ const G=superGeo(RECU,1400,820), map=G.map, X=map.X(ST.probe.x), Y=map.Y(ST.probe.y), g0=frameU();
  downU(X,Y); uok(DRAG.what==='probe','grabbing the probe'); idleU('proven idle'); moveU(X-50,Y+30);
  const g1=frameU(); uok(g1.length>50&&g1!==g0,'dragging the probe re-draws the chain through the loop'); upU();
  uok(roU().indexOf(fXY(ST.probe.x,ST.probe.y))>=0,'the readout follows the probe'); }
{ const sx=sliderU('probe x, m'); sx.value='-2'; sx.fire('input'); uok(ST.probe.x===-2,'the probe slider moves it'); }

/* ---- the far field: the pointer and the wheel do nothing, the slider turns the ray ---- */
NODESU.tabs.children[4].fire('click'); idleU('the far field idles');
downU(400,300); moveU(500,340); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','the far-field view ignores the pointer, as designed'); upU(); idleU('idle');
NODESU.scene.fire('wheel',{deltaY:-400}); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and the wheel');
{ const s=sliderU('direction'); RECU=makeRecU(); s.value='90'; s.fire('input'); uok(ST.farTheta===90,'the ray turns to 90°'); uok(RECU.ops.length>20,'the view redrew');
  uok(roU().indexOf('V = 0 along this ray')>=0,'on the dipole\'s bisector the readout says V = 0'); s.value='30'; s.fire('input');
  uok(roU().indexOf(sigf(farField(ST.charges,30).lim,6))>=0,'at 30° it prints the numerically taken limit'); }

/* ---- keyboard ---- */
keyU('3'); uok(ST.view==='land','3 is the landscape'); keyU('1'); uok(ST.view==='plane','1 the plane'); keyU('5'); uok(ST.view==='far','5 the far field');

/* ---- every control: sliders at both ends and the middle, every checkbox, every chip ---- */
let ctlErrU=null;
try{ const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===18,'the panel has its 8 sliders and 10 checkboxes ('+inputs.length+')');
  for(let v=0;v<5;v++){ NODESU.tabs.children[v].fire('click');
    for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max); for(const x of [lo,hi,(lo+hi)/2]){ inp.value=String(x); inp.fire('input'); } }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every control driven without error'); }
  for(let v=0;v<5;v++){ NODESU.tabs.children[v].fire('click');
    for(const nm of ['empty','one charge','dipole','like pair','quadrupole','triangle','two rows']){ RECU=makeRecU(); chipU(nm,7).fire('click'); assertCleanU(RECU,'view '+v+', '+nm); }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every preset draws'); }
  { chipU('empty',7).fire('click'); uok(ST.charges.length===0,'empty clears the plane'); NODESU.tabs.children[0].fire('click'); RECU=makeRecU(); pumpU(1);
    uok(roU().indexOf('none on the plane')>=0||roU().indexOf('on the plane</td><td class="v">0')>=0,'the readout says the plane is empty'); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* reset all: disturb every kind of state first (Known-bad: a reset test that resets nothing passes) */
  chipU('triangle',7).fire('click'); ST.camTheta=1; ST.camZoom=2; ST.vs={x:-3,y:-2}; ST.showTape=true; ST.probe={x:3,y:2}; ST.farTheta=-120; ST.nLines=30;
  findLabelledU('grid').checked=true; findLabelledU('grid').fire('change');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.preset==='dipole'&&ST.charges.length===2&&ST.camTheta===DEFAULTS.camTheta&&ST.camZoom===1&&ST.vs.x===1.5&&!ST.showTape&&!ST.showGrid&&ST.probe.x===0.6&&ST.farTheta===30&&ST.nLines===16,
    'reset all restores the charges, the camera, the tools, the toggles and the sliders');
  uok(findLabelledU('grid').checked===false&&sliderU('lines per charge').value===16,'and the controls show it');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
