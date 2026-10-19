
/* ====== UI drive test for masses-and-springs-basics.html ================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js
 * -> build/wave-on-a-string/ui_drive_wave-on-a-string.js).
 * The sim-specific thresholds: the panel has 9 groups; 17 inputs (9 sliders,
 * 8 checkboxes); five chip rows, TWO of which have the same arity and the same
 * labels (the two mass racks), so they are found by arity AND row index, never
 * by label alone (Known-bad: a finder that matches on a word finds the wrong
 * control).  Every drag is taken through the frame loop from a proven-idle
 * baseline, and every reset is checked against a sentinel. */
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
function sliderU(label){ let hit=null;   /* the WHOLE label, and every label here is unique */
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function sliderRowU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* a control is only really visible if neither its row NOR any group above it is
   hidden: syncPanel hides whole groups, so testing the row alone tests nothing */
function visU(label){ let seen=false;
  const walk=(n,hid)=>{ for(const ch of n.children||[]){
    const h2=hid||ch.hidden===true;
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label){ if(!h2) seen=true; }
    walk(ch,h2); } };
  walk(NODESU.panel,false); return seen; }
/* the two mass racks have the SAME arity and the SAME labels, so a chip is
   found by (arity, row index, exact label) — never by label alone */
function chipRowsU(arity){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='chips'&&ch.children.length===arity) out.push(ch); walk(ch); } };
  walk(NODESU.panel); return out; }
function chipU(label,arity,row){
  const rows=chipRowsU(arity), r=rows[row||0]; if(!r) return null;
  for(const c of r.children) if(c.textContent===label) return c;
  return null; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+(geomU(RECU)==='[]'?'':' ('+RECU.ops.length+' ops)')); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const rc=findLabelledU('time runs'); if(rc.checked){ rc.checked=false; rc.fire('change'); } }
function playU(){ const rc=findLabelledU('time runs'); if(!rc.checked){ rc.checked=true; rc.fire('change'); } }
function mapU(v){ const L=layoutFor(RECU,SU.W,SU.H,v||ST.view); return stageMap(buildModel(),L.main); }

/* ---- boot ---- */
let bootErrU=null, SU=null;
try{ SU=boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the stretch|the bounce|the lab|the period law|the damping|the energy','the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===9,'the control panel has its 9 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('40.83 cm')>=0,'the readout prints mg/k = 40.83 cm off the model (250 g, 6 N/m, Earth)');
uok((NODESU.readout.innerHTML||'').indexOf('14.2')>=0,'and PhET\'s Planet X value');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.view==='str'&&ST.body==='earth'&&ST.k1===6&&ST.mass1==='m250'&&ST.damping===0.7,'PhET\'s start: Stretch, Earth, 6 N/m, 250 g, damping 0.7');
uok((NODESU.hint.textContent||'').indexOf('drag a mass')>=0,'the hint names the drag');

/* ---- every tab draws, differently, cleanly (floors from the t = 0 emission) ---- */
const FLOORSU=[40,40,40,55,55,40];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- switching a tab restores PhET's own damping for that screen ---- */
tabU(1); uok(ST.view==='bnc'&&ST.damping===0,'the Bounce screen sets damping 0, as PhET does');
{ const ds=sliderU('b, N s/m'); ds.value='0.42'; ds.fire('input'); uok(ST.damping===0.42,'the damping slider moves it');
  tabU(0); uok(ST.damping===0.7,'and the Stretch screen puts it back to PhET\'s 0.7');
  tabU(2); uok(ST.damping===0,'the Lab screen to 0'); }

/* ---- paused, every live view idles; the analysis views idle while running --- */
pauseU(); uok(ST.running===false,'the "time runs" box pauses');
for(let i=0;i<3;i++){ tabU(i); pauseU(); idleU('tab '+i+' paints nothing while paused'); }
playU(); for(const i of [3,4]){ tabU(i); idleU('tab '+i+' is static: nothing to paint while time runs'); }

/* ---- the bounce runs through the frame loop ---- */
tabU(1); playU();
RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
uok(gA.length>50&&gB.length>50&&gA!==gB,'two pumped frames draw DIFFERENT pictures (the springs are bouncing)');
{ const t0=LIVE.t; pumpU(25); uok(Math.abs((LIVE.t-t0)-25*0.016)<1e-9,'25 frames of 16 ms advance the clock 0.4 s ('+fmt(LIVE.t-t0,4)+')');
  const ro0=NODESU.readout.innerHTML; pumpU(10); uok(NODESU.readout.innerHTML!==ro0,'the readout refreshes while it runs'); }
/* the mass chip re-hangs THAT spring only, checked against a sentinel */
{ pumpU(20); uok(Math.abs(LIVE.slot[0].y)>1e-4&&Math.abs(LIVE.slot[1].y)>1e-4,'sentinel: both springs have moved');
  const y1=LIVE.slot[1].y;
  const c=chipU('100 g',7,0); uok(!!c,'found the 100 g chip of the FIRST rack'); c.fire('click');
  uok(ST.mass1==='m100'&&LIVE.slot[0].y===0,'it re-hangs spring 1 at the unstretched end');
  uok(LIVE.slot[1].y===y1,'and leaves spring 2 alone');
  const c2=chipU('none',7,1); uok(!!c2,'found the none chip of the SECOND rack'); c2.fire('click');
  uok(ST.mass2==='none'&&ST.mass1==='m100','the second rack drives mass2, not mass1');
  chipU('50 g',7,1).fire('click'); uok(ST.mass2==='m50','and spring 2 gets its 50 g back'); }
/* slow motion is PhET's x1/8 */
{ chipU('250 g',7,0).fire('click');
  const sc=chipU('slow motion',2,0); uok(!!sc,'found the slow-motion chip');
  pumpU(1); const t0=LIVE.t; pumpU(40); uok(Math.abs((LIVE.t-t0)-40*0.016)<1e-9,'normal speed: 40 frames = 0.64 s simulated');
  sc.fire('click'); uok(ST.speed==='slow','slow motion selected');
  pumpU(1); const t1=LIVE.t; pumpU(40); uok(Math.abs((LIVE.t-t1)-40*0.016/8)<1e-9,'slow motion: 40 frames = 0.08 s simulated (x1/8)');
  chipU('normal',2,0).fire('click'); uok(ST.speed==='normal','back to normal'); }

/* ---- the step button and the step key ---- */
pauseU(); idleU('paused before stepping');
{ const t0=LIVE.t; uok(clickButtonU('step'),'found the step button');
  uok(Math.abs((LIVE.t-t0)-0.02)<1e-12,'step advances exactly 20 ms');
  keyU('.'); uok(Math.abs((LIVE.t-t0)-0.04)<1e-12,'the . key steps too');
  idleU('and the loop is idle again after the step repaint'); }
/* let go again, against a sentinel */
{ LIVE.slot[0].y=0.31; LIVE.slot[0].v=0.7;
  uok(clickButtonU('let go again'),'found let go again');
  uok(LIVE.slot[0].y===0&&LIVE.slot[0].v===0&&LIVE.slot[0].hist.length===0,'it re-hangs the masses at the unstretched end and clears the trace');
  LIVE.slot[0].y=0.22; keyU('r'); uok(LIVE.slot[0].y===0,'the r key does it too'); }

/* ---- a live but ignored control is hidden (Known-bad) ---- */
{ const vis=visU;
  tabU(0); uok(vis('spring 1 strength, N/m')&&!vis('spring strength, N/m')&&!vis('spring constant k, N/m'),'stretch: the two-spring sliders show, the lab and analysis ones do not');
  uok(!vis('g, m/s²'),'the custom-g slider is hidden while a planet is picked');
  chipU('custom',5,0).fire('click'); uok(ST.body==='custom'&&vis('g, m/s²'),'picking custom shows it');
  chipU('Earth',5,0).fire('click'); uok(ST.body==='earth','back to Earth');
  tabU(2); uok(vis('spring strength, N/m')&&vis('mass, g')&&!vis('spring 1 strength, N/m'),'lab: its own spring and mass sliders show');
  chipU('? large',3,0).fire('click'); uok(ST.labMass==='q180'&&!vis('mass, g'),'a mystery mass hides the mass slider it would ignore');
  chipU('adjustable',3,0).fire('click'); uok(vis('mass, g'),'and the adjustable mass brings it back');
  tabU(3); uok(vis('spring constant k, N/m')&&vis('mass m, g')&&!vis('damping ratio ζ'),'the period law: k and m, no zeta');
  tabU(4); uok(vis('damping ratio ζ'),'the damping view: zeta shows');
  tabU(0); }

/* ---- the REAL drag: the hanging mass, from a proven-idle baseline ---- */
tabU(0); pauseU(); idleU('stretch, paused: idle before the grab');
{ const map=mapU('str'), M=buildModel(), r=massRectPx(map,M.springs[0]);
  const cx=(r.x+r.x1)/2, cy=(r.y+r.y1)/2;
  NODESU.scene.fire('pointerdown',{clientX:cx,clientY:cy});
  uok(DRAG.what==='mass'&&DRAG.sp===0,'pointer-down ON the mass grabs it ('+DRAG.what+'/'+DRAG.sp+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the grab repaints through the loop (the block goes white)');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU)==='[]','still idle immediately before the move');
  const y0=LIVE.slot[0].y;
  NODESU.scene.fire('pointermove',{clientX:cx,clientY:cy+40,buttons:1});
  uok(Math.abs((LIVE.slot[0].y-y0)-40/map.s)<1e-9,'the move pulled it down 40 px, keeping the grab offset');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  LIVE.slot[0].v=0.9; NODESU.scene.fire('pointerup',{});
  uok(DRAG.what===null,'pointer-up releases'); uok(LIVE.slot[0].v===0,'and leaves it at rest, as PhET does');
  const y1=LIVE.slot[0].y;
  NODESU.scene.fire('pointermove',{clientX:cx,clientY:cy-90,buttons:0});
  uok(LIVE.slot[0].y===y1,'a hover with no button pressed moves nothing');
  uok(!NODESU.scene.classList.contains('dragging'),'and the cursor class is cleared'); }
/* a dragged spring does not step while it is held */
{ playU(); const map=mapU('str'), M=buildModel(), r=massRectPx(map,M.springs[0]);
  NODESU.scene.fire('pointerdown',{clientX:(r.x+r.x1)/2,clientY:(r.y+r.y1)/2});
  const held=LIVE.slot[0].y, other=LIVE.slot[1].y; pumpU(8);
  uok(LIVE.slot[0].y===held,'a held mass does not move while the clock runs');
  uok(LIVE.slot[1].y!==other,'while the other spring keeps going');
  NODESU.scene.fire('pointerup',{}); pauseU(); }

/* ---- PhET's other two draggables: the ruler and the movable line ---- */
for(const [lbl,key] of [['movable line','movLine'],['ruler','ruler']]){
  const cb=findLabelledU(lbl); uok(!!cb,'found the '+lbl+' checkbox');
  RECU=makeRecU(); cb.checked=true; cb.fire('change');
  uok(ST[key]===true,lbl+' switched on'); uok(RECU.ops.length>30,'and the view redrew at once'); }
uok(textU(RECU).indexOf('movable line')>=0&&textU(RECU).indexOf('cm')>=0,'both tools are on the canvas');
idleU('tools on, paused: idle');
{ const map=mapU('str');
  const drags=[['movline',map.X(1.0),map.Y(ST.movY)+1,0,-35,()=>ST.movY],
               ['ruler',map.X(ST.rulerX+RULER_W/2),map.Y(ST.rulerY-0.3),48,0,()=>ST.rulerX]];
  for(const [what,x,y,dx,dy,get] of drags){
    idleU(what+': proven idle before the grab');
    NODESU.scene.fire('pointerdown',{clientX:x,clientY:y}); uok(DRAG.what===what,'pointer-down grabs '+what+' ('+DRAG.what+')');
    idleU(what+': the grab\'s repaint drained');
    const v0=get(); RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:x+dx,clientY:y+dy,buttons:1});
    uok(Math.abs(get()-v0-(dx?dx/map.s:-dy/map.s))<1e-9,what+' moved with the pointer by the right amount');
    pumpU(1); uok(geomU(RECU).length>50,what+': the move repainted through the loop (dirty flag)');
    idleU(what+': and the loop goes idle again'); uok(ST.running===false,what+': still paused');
    NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,what+' released');
  } }
/* the stopwatch */
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change'); uok(ST.stopwatch===true,'the stopwatch is on');
  uok(clickButtonU('start / stop'),'found start / stop'); uok(LIVE.swOn===true,'it runs');
  playU(); pumpU(20); uok(LIVE.sw>0.25,'and counts simulated time ('+fmt(LIVE.sw,3)+' s)');
  uok(clickButtonU('start / stop')&&LIVE.swOn===false,'and stops'); const s0=LIVE.sw; pumpU(5); uok(LIVE.sw===s0,'stopped, it holds');
  uok(clickButtonU('clear')&&LIVE.sw===0,'clear zeroes it');
  cb.checked=false; cb.fire('change'); pauseU(); }

/* ---- a slider redraws at once, from a proven-idle baseline ---- */
tabU(0); pauseU(); idleU('before the slider');
{ const ks=sliderU('spring 1 strength, N/m'); RECU=makeRecU(); ks.value='12'; ks.fire('input');
  uok(ST.k1===12,'the spring-1 slider set k = 12 N/m');
  uok(RECU.ops.length>30,'and the view redrew immediately ('+RECU.ops.length+' ops)');
  uok(NODESU.readout.innerHTML.indexOf('20.42 cm')>=0,'the readout followed: 250 g on 12 N/m stretches 20.42 cm');
  ks.value='6'; ks.fire('input'); }

/* ---- the mystery masses and Planet X ---- */
tabU(2);
{ chipU('Planet X',5,0).fire('click'); uok(ST.body==='planetX','Planet X selected');
  RECU=makeRecU(); tabU(2);
  uok(NODESU.readout.innerHTML.indexOf('>?<')>=0,'its value is hidden behind a question mark');
  uok(NODESU.readout.innerHTML.indexOf('solve g = k y / m')>=0,'and the readout says how to get it');
  const rv=findLabelledU('reveal the hidden values'); uok(!!rv,'found the reveal checkbox');
  rv.checked=true; rv.fire('change'); uok(ST.reveal===true,'reveal is on');
  uok(NODESU.readout.innerHTML.indexOf('invented 14.2')>=0,'and the readout names PhET\'s 14.2 m/s2');
  rv.checked=false; rv.fire('change'); chipU('Earth',5,0).fire('click'); }

/* ---- the period trace measures the period on the lab screen ---- */
tabU(2); clickButtonU('let go again'); playU();
{ pumpU(120); const M=buildModel();
  uok(isFinite(M.springs[0].Tmeas),'the trace has measured a period ('+fmt(M.springs[0].Tmeas,5)+' s)');
  uok(Math.abs(M.springs[0].Tmeas-period0(0.1,6))<1e-9,'and it is 2 pi sqrt(m/k) to 1e-9');
  uok(NODESU.readout.innerHTML.indexOf('period measured from the trace')>=0,'the readout reports it'); pauseU(); }

/* ---- the analysis views ignore the pointer, and their sliders bite ---- */
for(const i of [3,4,5]){ tabU(i); idleU('tab '+i+' idle');
  NODESU.scene.fire('pointerdown',{clientX:500,clientY:300}); NODESU.scene.fire('pointermove',{clientX:640,clientY:360,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','tab '+i+' ignores the pointer'); NODESU.scene.fire('pointerup',{}); }
tabU(4);
{ const zs=sliderU('damping ratio ζ'); uok(!!zs,'found the zeta slider'); RECU=makeRecU(); zs.value='1';
  zs.fire('input'); uok(ST.zeta===1,'zeta = 1'); uok(RECU.ops.length>40,'the view redrew at once ('+RECU.ops.length+' ops)');
  const g1=geomU(RECU); RECU=makeRecU(); zs.value='1.8'; zs.fire('input');
  uok(geomU(RECU)!==g1,'and zeta = 1.8 draws a different picture');
  uok(NODESU.readout.innerHTML.indexOf('beyond its slider')>=0,'the readout says it is beyond PhET\'s range');
  zs.value='0.25'; zs.fire('input'); uok(NODESU.readout.innerHTML.indexOf('yes')>=0,'and inside it at zeta = 0.25'); }

/* ---- keyboard: views and play/pause ---- */
keyU('1'); uok(ST.view==='str','1 is the stretch'); keyU('6'); uok(ST.view==='eng','6 the energy'); keyU('3'); uok(ST.view==='lab','3 the lab');
{ const r0=ST.running; keyU(' '); uok(ST.running===!r0,'space toggles play'); keyU(' '); uok(ST.running===r0,'and back'); }

/* ---- every control, every tab, resize, reset all against disturbed state ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===17,'the panel has its 9 sliders and 8 checkboxes ('+inputs.length+')');
  for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); } }
  for(const r of chipRowsU(7)) for(const c of r.children){ c.fire('click'); uok(NODESU.errbox.style.display!=='block','rack chip '+c.textContent+' draws without error'); }
  for(const r of chipRowsU(5)) for(const c of r.children){ c.fire('click'); uok(NODESU.errbox.style.display!=='block','gravity chip '+c.textContent+' draws without error'); }
  for(const r of chipRowsU(3)) for(const c of r.children){ c.fire('click'); uok(NODESU.errbox.style.display!=='block','lab chip '+c.textContent+' draws without error'); }
  for(let v=0;v<6;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb every kind of state reset all claims to restore */
  tabU(0); chipU('? large',7,0).fire('click'); chipU('100 g',7,1).fire('click'); chipU('slow motion',2,0).fire('click');
  chipU('Jupiter',5,0).fire('click');
  ST.ruler=true; ST.movLine=true; ST.stopwatch=true; ST.rulerX=0.9; ST.rulerY=1.1; ST.movY=0.2;
  ST.k1=11; ST.k2=4; ST.kl=9; ST.massG=275; ST.zeta=1.7; ST.kA=4; ST.mAg=88; ST.reveal=true; ST.natLine=false; ST.trace=false;
  LIVE.sw=3.3; LIVE.swOn=true; playU(); pumpU(6); uok(Math.abs(LIVE.slot[0].y)>0,'sentinel: a spring has moved');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.mass1==='m250'&&ST.mass2==='m50'&&ST.body==='earth'&&ST.speed==='normal'&&ST.k1===6&&ST.k2===6&&ST.kl===6,'reset all restores PhET\'s defaults');
  uok(ST.massG===100&&ST.zeta===0.25&&ST.kA===6&&ST.mAg===100&&!ST.reveal&&ST.natLine&&ST.trace,'and the analysis and line settings');
  uok(!ST.ruler&&!ST.movLine&&!ST.stopwatch&&ST.rulerX===0.40&&ST.rulerY===1.44&&Math.abs(ST.movY-0.62)<1e-12,'and the tools, hidden and home');
  uok(LIVE.sw===0&&LIVE.swOn===false&&LIVE.t===0&&LIVE.slot[0].y===0,'and the stopwatch and the springs');
  uok(ST.damping===0.7,'with the Stretch screen\'s own damping');
  uok(ST.view==='str','keeping the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
