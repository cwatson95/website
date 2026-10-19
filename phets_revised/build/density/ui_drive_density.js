/* ============ UI drive test for density.html ============================= *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js
 * -> build/wave-on-a-string/ui_drive_wave-on-a-string.js).
 * The three sim-specific thresholds: chip rows are found by exact label AND
 * arity (7 materials, 3 set modes, 4 mystery sets, 5 picks, 27 plane
 * materials, 6 fluids); the panel has 8 groups; 12 inputs (6 sliders,
 * 6 checkboxes).  Every drag runs THROUGH the frame loop from a proven-idle
 * baseline, and every reset is checked against a sentinel. */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){ c._p=[]; },moveTo(x,y){ c._p&&c._p.push([x,y]); },
    lineTo(x,y){ c._p&&c._p.push([x,y]); },closePath:P,
    rect(x,y,w,h){ c._p&&c._p.push([x,y],[x+w,y+h]); },
    arc(x,y,r){ c._p&&c._p.push([x,y,r]); },
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){ ops.push(['r',x,y,w,h]); },
    strokeRect(x,y,w,h){ ops.push(['R',x,y,w,h]); }, clearRect:P,
    fillText(t,x,y){ ops.push(['t',String(t),Math.round(x),Math.round(y)]); }, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||''); return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
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
    classList:{_on:{},add(c){ this._on[c]=1; },remove(c){ delete this._on[c]; },
               toggle(c){ this._on[c]?delete this._on[c]:this._on[c]=1; },contains(c){ return !!this._on[c]; }},
    getBoundingClientRect(){ return {left:0,top:0,width:1180,height:740}; },
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
function findLabelledU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function valOfU(label){ const r=rowU(label); return r?(r.children[2].textContent||''):null; }
/* the panel's own textContent is frozen at appendChild time, so a .tag whose
   innerHTML is rewritten by syncPanel has to be read off the element itself */
function tagTextU(gi){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='tag') hit=ch; walk(ch); } };
  walk(NODESU.panel.children[gi]); return hit?(hit.textContent||''):null; }
function rowU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* Chip rows are addressed by GROUP and by their index inside it, never by the
   label alone and not even by label + arity: the block group carries TWO
   7-chip material rows (A and B) and a label-only search takes the last one,
   which silently drives block B (Known-bad: a finder that matches on a word
   finds the wrong control). */
const GBLOCK=0, GSET=1, GMYS=2, GPLANE=3, GFLUID=4, GDRAW=5;
function chipsInU(gi,rowIdx){
  const out=[];
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='chips') out.push(ch); walk(ch); } };
  walk(NODESU.panel.children[gi]);
  return out[rowIdx||0]||null;
}
function chipG(gi,rowIdx,label,arity){
  const row=chipsInU(gi,rowIdx);
  if(!row||(arity!==undefined&&row.children.length!==arity)) return null;
  for(const c of row.children) if(c.textContent===label) return c;
  return null;
}
const chipU=(label,arity)=>{ /* kept for the single-row groups */
  for(const gi of [GSET,GMYS,GPLANE,GFLUID]) for(const r of [0,1]){
    const c=chipG(gi,r,label,arity); if(c) return c; }
  return null; };
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the pool|the sets|the mystery|mass and volume|the waterline',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===8,'the control panel has its 8 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('2.00 kg')>=0,'the readout prints block A\'s 2.00 kg off the model');
uok((NODESU.readout.innerHTML||'').indexOf('5.56 mm')>=0,'and the 5.56 mm rise the floating law gives');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.matA==='wood'&&ST.massA===2&&ST.matB==='aluminum'&&ST.massB===13.5&&ST.two===false,
    'PhET\'s start: one block, wood 2 kg, aluminium 13.5 kg behind it');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[40,40,40,40,30];
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');
for(let i=0;i<5;i++){ tabU(i); idleU('tab '+i+' paints nothing once it has settled'); }

/* ---- the material chips drive PhET's mass/volume coupling ---- */
tabU(0);
{
  const mat=chipG(GBLOCK,0,'aluminium',7); uok(!!mat,'found the aluminium chip in the 7-material row');
  RECU=makeRecU(); mat.fire('click');
  uok(ST.matA==='aluminum','aluminium selected');
  uok(Math.abs(ST.volAL-5)<1e-12,'the volume is kept at 5 L');
  uok(Math.abs(ST.massA-13.5)<1e-12,'and the mass follows it: 5 L of aluminium is 13.5 kg');
  uok(RECU.ops.length>30,'and the view redrew at once ('+RECU.ops.length+' ops)');
  const ms=sliderU('mass, kg'); uok(!!ms,'found the mass slider');
  ms.value='27'; ms.fire('input');
  uok(Math.abs(ST.massA-27)<1e-9&&Math.abs(ST.volAL-10)<1e-9,'27 kg of aluminium is exactly 10 L (PhET\'s ceiling)');
  /* only syncPanel() refreshes the OTHER slider's printed value and the
     mass-range note, so a handler that redraws without re-syncing leaves the
     panel showing a volume the model no longer has */
  uok(valOfU('volume, L')==='10.00 L','the volume row now READS 10.00 L ('+valOfU('volume, L')+')');
  uok(valOfU('mass, kg')==='27.00 kg','and the mass row 27.00 kg');
  uok((tagTextU(GBLOCK)||'').indexOf('2.70')>=0,'and the tag names aluminium\'s 2.70 kg slider floor ('+tagTextU(GBLOCK)+')');
  ms.value='2'; ms.fire('input');
  uok(Math.abs(ST.massA-2.7)<1e-9,'asking for 2 kg of aluminium is refused: 1 L is 2.7 kg, its slider floor');
  const vs=sliderU('volume, L'); uok(!!vs,'found the volume slider');
  vs.value='4'; vs.fire('input');
  uok(Math.abs(ST.volAL-4)<1e-9&&Math.abs(ST.massA-10.8)<1e-9,'4 L of aluminium is 10.8 kg');
  /* custom: the two come apart and the density follows */
  chipG(GBLOCK,0,'custom',7).fire('click');
  uok(ST.matA==='custom','custom selected');
  const m0=ST.massA, v0=ST.volAL;
  vs.value='8'; vs.fire('input');
  uok(Math.abs(ST.volAL-8)<1e-9&&Math.abs(ST.massA-m0)<1e-9,'custom: moving the volume leaves the mass alone');
  uok(Math.abs(rhoOf(ST,'A')-m0/0.008)<1e-6,'and the density follows, rho = m/V');
  ms.value='4'; ms.fire('input');
  uok(Math.abs(ST.massA-4)<1e-9&&Math.abs(ST.volAL-8)<1e-9,'and moving the mass leaves the volume alone');
  uok(Math.abs(rhoOf(ST,'A')-500)<1e-9,'4 kg in 8 L is 500 kg/m3');
  uok(NODESU.readout.innerHTML.indexOf('500.0')>=0,'which the readout prints');
  chipG(GBLOCK,0,'wood',7).fire('click');
  uok(ST.matA==='wood'&&Math.abs(ST.volAL-8)<1e-9&&Math.abs(ST.massA-3.2)<1e-9,'back to wood: 8 L keeps, the mass becomes 3.2 kg');
}

/* ---- two blocks, and the second block's rows appear with it ---- */
{
  const vis=lab2=>{ const r=rowU(lab2); return r&&r.hidden===false; };
  uok(!vis('B mass, kg'),'with one block the B rows are hidden, not live and inert');
  uok(chipsInU(GBLOCK,1).hidden===true,'and so is block B\'s material chip row');
  const cb=findLabelledU('two blocks'); uok(!!cb,'found the two-blocks checkbox');
  RECU=makeRecU(); cb.checked=true; cb.fire('change');
  uok(ST.two===true,'two blocks switched on');
  uok(vis('B mass, kg')&&vis('B volume, L'),'and the B rows appear');
  uok(chipsInU(GBLOCK,1).hidden===false,'with its material chips');
  uok(RECU.ops.length>30,'the stage redrew');
  uok(NODESU.readout.innerHTML.indexOf('block B')>=0,'the readout grew a block-B section');
  const y0=buildModel(ST).yw;
  cb.checked=false; cb.fire('change');
  uok(buildModel(ST).yw<y0-1e-4,'taking block B out drops the water level');
}

/* ---- the REAL drag, from a proven-idle baseline, through the frame loop ---- */
tabU(0);
/* put the block back on PhET's default 5 L so the clamp can be pinned against
   an absolute number rather than against the same formula the sim uses */
{ const vs=sliderU('volume, L'); vs.value='5'; vs.fire('input');
  uok(Math.abs(ST.volAL-5)<1e-12&&Math.abs(ST.massA-2)<1e-12,'back to PhET\'s 5 L of wood, 2 kg'); }
idleU('the pool view is idle before the grab');
{
  const M=buildModel(ST), G2=poolGeo(RECU,1180,740,M), map=G2.map, bk=M.blocks[0];
  const X=map.X(bk.x), Y=map.Y(bk.yb+bk.s/2);
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y});
  uok(DRAG.what==='A','pointer-down ON block A grabs it');
  idleU('the grab itself painted nothing (proven-idle baseline before the move)');
  const before=buildModel(ST).yw;
  RECU=makeRecU();
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+45,buttons:1});
  uok(ST.holdA!==null,'the move set a hold height');
  pumpU(1); const g1=geomU(RECU);
  uok(g1.length>200,'the move repainted THROUGH the frame loop (the dirty flag)');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]','and then the loop goes quiet again');
  const held=buildModel(ST);
  uok(held.blocks[0].mode==='held','the model says the block is held');
  uok(held.yw>before+1e-5,'pushed under, it displaces more and the level rises');
  uok(held.blocks[0].hand<0,'and the hand has to push DOWN on a floater');
  RECU=makeRecU();
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+90,buttons:1});
  pumpU(1); const g2=geomU(RECU);
  uok(g2.length>200&&g2!==g1,'a second, deeper move draws a DIFFERENT picture');
  /* dragged far below the floor, the hold is clamped to the pool floor */
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+4000,buttons:1});
  uok(Math.abs(ST.holdA-(-POOL_H))<1e-12,'dragged through the floor, the hold stops AT the floor ('+ST.holdA+')');
  uok(buildModel(ST).blocks[0].yb>=-POOL_H-1e-12,'so the block never goes below the pool');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y-4000,buttons:1});
  uok(Math.abs(ST.holdA-0.03700240533233027)<1e-12,
      'and lifted, a 5 L block stops at 0.037 m, its top exactly at the top of the drawn world ('+ST.holdA+')');
  uok(ST.holdA+cubeSide(ST.volAL/LITERS)<=POOL_YTOP+1e-12,'so the block is never drawn off the stage');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+90,buttons:1});
  NODESU.scene.fire('pointerup',{});
  uok(DRAG.what===null&&ST.holdA===null,'pointer-up lets go');
  uok(Math.abs(buildModel(ST).yw-before)<1e-12,'and everything returns to equilibrium');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+45,buttons:0});
  uok(ST.holdA===null,'a hover with no button pressed moves nothing');
  uok(!NODESU.scene.fire('pointerdown',{clientX:5,clientY:5})&&DRAG.what===null,'a pointer-down in the corner grabs nothing');
  NODESU.scene.fire('pointerup',{});
}
/* lifting a block clear of the water */
{
  const M=buildModel(ST), G2=poolGeo(RECU,1180,740,M), map=G2.map, bk=M.blocks[0];
  NODESU.scene.fire('pointerdown',{clientX:map.X(bk.x),clientY:map.Y(bk.yb+bk.s/2)});
  NODESU.scene.fire('pointermove',{clientX:map.X(bk.x),clientY:map.Y(0.20),buttons:1});
  const up=buildModel(ST);
  uok(up.blocks[0].Vsub===0,'lifted clear of the water it displaces nothing');
  uok(Math.abs(up.blocks[0].hand-up.blocks[0].W)<1e-9,'and the hand carries its whole weight');
  uok(Math.abs(up.yw-poolLevel([],[],RHO_WATER,VF0))<1e-12,'the pool is back to its bare level');
  NODESU.scene.fire('pointerup',{});
}
/* the other four views ignore the pointer */
for(const i of [1,2,3,4]){ tabU(i); idleU('tab '+i+' idle'); NODESU.scene.fire('pointerdown',{clientX:400,clientY:300});
  NODESU.scene.fire('pointermove',{clientX:600,clientY:340,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','tab '+i+' ignores the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- the sets: three modes, one live slider each ---- */
tabU(1);
{
  const vis=lab2=>{ const r=rowU(lab2); return r&&r.hidden===false; };
  uok(vis('same mass, kg')&&!vis('same volume, L')&&!vis('same density'),'same mass: only its own slider is live');
  RECU=makeRecU(); chipU('same volume',3).fire('click');
  uok(ST.setMode==='volume','same volume selected');
  uok(vis('same volume, L')&&!vis('same mass, kg'),'and the slider swapped over');
  uok(RECU.ops.length>30,'the view redrew');
  uok(NODESU.readout.innerHTML.indexOf('1600')>=0,'the readout prints the 1600 kg/m3 the 8 kg block becomes');
  chipU('same density',3).fire('click');
  uok(ST.setMode==='density','same density selected');
  const ds=sliderU('same density'); uok(!!ds,'found the density slider');
  ds.value='900'; ds.fire('input');
  const M=buildModel(ST);
  uok(M.blocks.every(b=>Math.abs(b.frac-0.9)<1e-9),'at 900 every block floats 90 % under, whatever its size');
  ds.value='1800'; ds.fire('input');
  uok(buildModel(ST).blocks.every(b=>b.mode==='rest'&&b.frac===1),'at 1800 they all sink instead');
  ds.value='500'; ds.fire('input');
  chipU('same mass',3).fire('click');
  const ms=sliderU('same mass, kg'); ms.value='5'; ms.fire('input');
  uok(buildModel(ST).nNeutral===1,'at 5 kg exactly one block is exactly water');
  uok(NODESU.readout.innerHTML.indexOf('exactly water')>=0,'which the readout says in words');
}

/* ---- the mystery: the sets, the pick, the trap, the reveal, the shuffle ---- */
tabU(2);
{
  uok(chipU('set 1',4)&&chipU('shuffled',4),'found the 4-set chip row');
  uok(chipU('C',5),'and the 5-block pick row');
  RECU=makeRecU(); chipU('C',5).fire('click');
  uok(ST.mpick==='C','block C picked');
  uok(RECU.ops.length>30,'the view redrew');
  uok(NODESU.readout.innerHTML.indexOf('19.32 kg')>=0,'set 1 C weighs 19.32 kg on the scale');
  uok(NODESU.readout.innerHTML.indexOf('gold')>=0,'and the table names it gold');
  const rev=findLabelledU('reveal the answers'); uok(!!rev,'found the reveal checkbox');
  rev.checked=true; rev.fire('change');
  uok(NODESU.readout.innerHTML.indexOf('really')>=0,'reveal names the material it really is');
  rev.checked=false; rev.fire('change');
  /* the trap */
  const sub=findLabelledU('hold them under'); uok(!!sub,'found the hold-them-under checkbox');
  uok(ST.submerge===true,'it starts on');
  uok(buildModel(ST).nWrong===0,'held under, all five are identified');
  RECU=makeRecU(); sub.checked=false; sub.fire('change');
  const M=buildModel(ST);
  uok(M.nWrong>=2,'let float, '+M.nWrong+' of 5 come out wrong');
  uok(M.rows.filter(r=>r.rho<1000).every(r=>r.guess==='water'),'every floater measures as WATER');
  uok(RECU.ops.length>30,'and the view redrew to say so');
  uok(NODESU.readout.innerHTML.indexOf('lying to you')>=0,'the readout explains why');
  sub.checked=true; sub.fire('change');
  /* the shuffle */
  chipU('set 2',4).fire('click');
  const seed0=ST.seed;
  uok(clickButtonU('a new shuffle'),'found the new-shuffle button');
  uok(ST.mset==='shuffled'&&ST.seed!==seed0,'it switches to the shuffled set and advances the seed');
  const s1=buildModel(ST).rows.map(r=>r.truth).join(',');
  clickButtonU('a new shuffle');
  uok(buildModel(ST).rows.map(r=>r.truth).join(',')!==s1,'a second press draws a different set');
  uok(buildModel(ST).nWrong===0,'and the new set is identifiable too');
  chipU('set 1',4).fire('click');
}

/* ---- the plane: 27 materials, the handbook overlay ---- */
tabU(3);
{
  uok(chipU('gold',27),'found the 27-material plane chip row');
  RECU=makeRecU(); chipU('gold',27).fire('click');
  uok(ST.mvMat==='gold','gold picked');
  uok(RECU.ops.length>30,'the view redrew');
  uok(NODESU.readout.innerHTML.indexOf('19320')>=0,'the readout prints PhET\'s 19320');
  chipU('pyrite',27).fire('click');
  uok(NODESU.readout.innerHTML.indexOf('no row')>=0,'pyrite has no handbook row and the readout says so');
  chipU('styrofoam',27).fire('click');
  uok(NODESU.readout.innerHTML.indexOf('+100')>=0,'styrofoam is 100 % above the handbook value');
  const cb=findLabelledU('draw the handbook value too'); uok(!!cb,'found the handbook checkbox');
  RECU=makeRecU(); const g0=geomU(RECU); cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(3); const g1=geomU(RECU);
  cb.checked=true; cb.fire('change');
  RECU=makeRecU(); tabU(3); const g2=geomU(RECU);
  uok(g1!==g2,'switching the handbook rays off changes the picture');
}

/* ---- the waterline: six fluids ---- */
tabU(4);
{
  uok(chipU('mercury',6),'found the 6-fluid chip row');
  RECU=makeRecU(); chipU('mercury',6).fire('click');
  uok(ST.lineFluid==='mercury','mercury picked');
  uok(RECU.ops.length>30,'the view redrew');
  const M=buildModel(ST);
  uok(Math.abs(100*M.frac-2.94269)<1e-4,'wood is 2.94 % under in mercury');
  uok(M.blk.mode==='float','and it floats');
  chipU('gasoline',6).fire('click');
  uok(Math.abs(100*buildModel(ST).frac-58.8235)<1e-3,'and 58.82 % under in gasoline');
  chipU('water',6).fire('click');
  /* the neutral case, reached through the controls */
  tabU(0); chipG(GBLOCK,0,'custom',7).fire('click');
  const ms=sliderU('mass, kg'), vs=sliderU('volume, L');
  vs.value='5'; vs.fire('input'); ms.value='5'; ms.fire('input');
  tabU(4);
  uok(Math.abs(rhoOf(ST,'A')-1000)<1e-9,'5 kg in 5 L is exactly water');
  uok(buildModel(ST).neutral===true,'the model calls it neutral');
  uok(NODESU.readout.innerHTML.indexOf('Exactly neutral')>=0,'and the readout says so');
  uok(Math.abs(buildModel(ST).app)<1e-12,'a spring scale would read zero');
}

/* ---- keyboard, resize, reset all against disturbed state ---- */
keyU('1'); uok(ST.view==='pool','1 is the pool');
keyU('5'); uok(ST.view==='line','5 the waterline');
keyU('3'); uok(ST.view==='mystery','3 the mystery');
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===13,'the panel has its 7 sliders and 6 checkboxes ('+inputs.length+')');
  for(const inp of inputs){
    if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input');
      uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); }
  }
  for(let v=0;v<5;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb every kind of state reset all claims to restore, with a sentinel */
  tabU(0);
  chipG(GBLOCK,0,'brick',7).fire('click'); ST.two=true; ST.setMode='density'; ST.mset='set 3';
  ST.mpick='E'; ST.reveal=true; ST.submerge=false; ST.mvMat='gold'; ST.showRef=false;
  ST.lineFluid='honey'; ST.forces=false; ST.levels=false; ST.holdA=-0.3; ST.sameRho=1900;
  uok(ST.matA==='brick'&&ST.holdA===-0.3,'sentinel: the state really is disturbed');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.matA==='wood'&&ST.massA===2&&ST.volAL===5&&ST.two===false,'reset all restores PhET\'s block');
  uok(ST.setMode==='mass'&&ST.mset==='set 1'&&ST.mpick==='A'&&ST.submerge===true&&!ST.reveal,'and the set and the mystery');
  uok(ST.mvMat==='wood'&&ST.showRef===true&&ST.lineFluid==='water','and the plane and the fluid');
  uok(ST.forces===true&&ST.levels===true&&ST.holdA===null&&ST.sameRho===500,'and the drawing, the hold and the sliders');
  uok(ST.view==='pool','keeping the view');
  /* the r key does the same */
  ST.matA='brick'; keyU('r'); uok(ST.matA==='wood','the r key resets too');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
