/* ============ UI drive test for buoyancy-basics.html ============================= *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js
 * -> build/wave-on-a-string/ui_drive_wave-on-a-string.js).
 * The three sim-specific thresholds: chip rows are addressed by GROUP and row
 * index (7 materials twice, 6 fluids, 3 places, 3 set modes, 27 grid
 * materials); the panel has 9 groups; 13 inputs (10 sliders, 3 checkboxes).
 * Every drag runs THROUGH the frame loop from a proven-idle baseline, and
 * every reset is checked against a sentinel. */
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
const GBLOCK=0, GFLUID=1, GSCALES=2, GSET=3, GDEPTH=4, GGRID=5, GDRAW=6;
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
  for(const gi of [GFLUID,GSCALES,GSET,GGRID]) for(const r of [0,1]){
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
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the pool|the sets|the faces|the scale|float or sink',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===9,'the control panel has its 9 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('40.0 %')>=0,'the readout prints wood\'s 40.0 % submerged off the model');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.matA==='wood'&&ST.massA===2&&ST.fluid==='water'&&ST.where==='floor'&&ST.two===false,
    'PhET\'s start: one wood block, 2 kg, in water, on the pool floor');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[40,40,30,30,60];
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

/* ---- the fluid chips move everything ---- */
tabU(0);
{
  const merc=chipG(GFLUID,0,'mercury',6); uok(!!merc,'found the mercury chip in the 6-fluid row');
  const before=buildModel(ST).blocks[0].pct;
  RECU=makeRecU(); merc.fire('click');
  uok(ST.fluid==='mercury','mercury selected');
  uok(RECU.ops.length>30,'and the view redrew at once ('+RECU.ops.length+' ops)');
  const M=buildModel(ST);
  uok(Math.abs(M.blocks[0].pct-2.94269)<1e-4,'wood is 2.94 % under in mercury (derive)');
  uok(M.blocks[0].pct<before,'much less of it than in water');
  uok(NODESU.readout.innerHTML.indexOf('13593')>=0,'the readout prints mercury\'s 13593 kg/m3');
  /* aluminium floats in mercury — the headline of the screen */
  chipG(GBLOCK,0,'aluminium',7).fire('click');
  const M2=buildModel(ST);
  uok(M2.blocks[0].mode==='float','aluminium FLOATS in mercury');
  uok(Math.abs(M2.blocks[0].pct-19.8632)<1e-3,'19.86 % of it under (derive)');
  chipG(GFLUID,0,'water',6).fire('click');
  uok(buildModel(ST).blocks[0].mode==='rest','and rests on the floor in water');
  chipG(GBLOCK,0,'wood',7).fire('click');
  uok(Math.abs(ST.massA-2)<1e-12,'back to PhET\'s 2 kg of wood');
}

/* ---- the material chips drive PhET's mass/volume coupling ---- */
{
  const mat=chipG(GBLOCK,0,'aluminium',7);
  mat.fire('click');
  uok(ST.matA==='aluminum'&&Math.abs(ST.volAL-5)<1e-12&&Math.abs(ST.massA-13.5)<1e-12,
      '5 L of aluminium is 13.5 kg, the volume kept');
  const ms=sliderU('mass, kg'), vs=sliderU('volume, L');
  uok(!!ms&&!!vs,'found the mass and volume sliders');
  ms.value='27'; ms.fire('input');
  uok(Math.abs(ST.volAL-10)<1e-9,'27 kg of aluminium is exactly 10 L (PhET\'s ceiling)');
  uok(valOfU('volume, L')==='10.00 L','and the volume row READS 10.00 L ('+valOfU('volume, L')+')');
  uok((tagTextU(GBLOCK)||'').indexOf('2.70')>=0,'the tag names aluminium\'s 2.70 kg slider floor');
  chipG(GBLOCK,0,'custom',7).fire('click');
  vs.value='8'; vs.fire('input'); ms.value='4'; ms.fire('input');
  uok(Math.abs(rhoOf(ST,'A')-500)<1e-9,'custom: 4 kg in 8 L is 500 kg/m3');
  chipG(GBLOCK,0,'wood',7).fire('click');
  vs.value='5'; vs.fire('input');
  uok(Math.abs(ST.volAL-5)<1e-12&&Math.abs(ST.massA-2)<1e-12,'back to PhET\'s 5 L of wood, 2 kg');
}

/* ---- the two scales ---- */
{
  const vis=lab2=>{ const r=rowU(lab2); return r&&r.hidden===false; };
  uok(vis('pool scale height'),'the pool-scale height slider is live on this view');
  const ps=chipG(GSCALES,0,'the pool scale',3); uok(!!ps,'found the 3-place chip row');
  RECU=makeRecU(); ps.fire('click');
  uok(ST.where==='poolscale','block A is on the pool scale');
  uok(RECU.ops.length>30,'the view redrew');
  const M=buildModel(ST);
  /* at PhET's half height the scale's top stands ABOVE where the wood would
     float, so the wood rests on it and presses with what the upthrust cannot
     carry — which is the scale doing its job, not a bug */
  uok(M.blocks[0].mode==='rest','at half height the scale holds the wood above its floating level');
  uok(M.poolReads>0&&M.poolReads<M.blocks[0].W,
      'so it presses with '+fmt(M.poolReads,2)+' N, less than its '+fmt(M.blocks[0].W,2)+' N weight');
  uok(Math.abs(M.blocks[0].W-M.poolReads-M.blocks[0].Fb)<1e-9,'and the difference is exactly the upthrust');
  { const hs0=sliderU('pool scale height'); hs0.value='0'; hs0.fire('input');
    const low=buildModel(ST);
    uok(low.blocks[0].mode==='float','dropped to the floor, the scale lets the wood float free');
    uok(low.poolReads===0,'and then it reads nothing at all');
    hs0.value='0.5'; hs0.fire('input'); }
  chipG(GBLOCK,0,'aluminium',7).fire('click');
  const M2=buildModel(ST);
  uok(M2.poolReads>0,'an aluminium block does press on it ('+fmt(M2.poolReads,2)+' N)');
  uok(Math.abs(M2.poolReads-118.43840164373687)<1e-8,'118.44 N, as derive.py has it');
  uok(M2.poolReads<13.5*G,'which is less than its 132.30 N in air');
  const hs=sliderU('pool scale height'); uok(!!hs,'found the pool-scale height slider');
  hs.value='0'; hs.fire('input');
  uok(Math.abs(poolScaleTop(ST)-(-POOL_H+SCALE_H))<1e-12,'at height 0 the scale stands on the floor');
  const low=buildModel(ST).poolReads;
  hs.value='1'; hs.fire('input');
  uok(Math.abs(poolScaleTop(ST))<1e-12,'at height 1 its top is level with the ground');
  const high=buildModel(ST);
  uok(high.blocks[0].mode==='out'||high.poolReads>low,
      'raised out of the fluid the block loses its buoyancy and presses harder ('+fmt(high.poolReads,1)+' vs '+fmt(low,1)+' N)');
  hs.value='0.5'; hs.fire('input');
  chipG(GSCALES,0,'the ground scale',3).fire('click');
  const M3=buildModel(ST);
  uok(ST.where==='ground','block A is on the ground scale');
  uok(M3.blocks[0].mode==='out','so it is out of the pool');
  uok(Math.abs(M3.groundReads-13.5*G)<1e-9,'and it reads its full 132.30 N in air');
  uok(M3.poolReads===0,'while the pool scale reads nothing');
  uok(Math.abs(M3.yw-poolLevel([],poolObstacles(ST),MAT.water.phet,VF0))<1e-12,'the pool is back to its bare level');
  chipG(GSCALES,0,'the pool floor',3).fire('click');
  chipG(GBLOCK,0,'wood',7).fire('click');
  const vs=sliderU('volume, L'); vs.value='5'; vs.fire('input');
}

/* ---- two blocks ---- */
{
  const vis=lab2=>{ const r=rowU(lab2); return r&&r.hidden===false; };
  uok(!vis('B mass, kg'),'with one block the B rows are hidden, not live and inert');
  uok(chipsInU(GBLOCK,1).hidden===true,'and so is block B\'s material chip row');
  const cb=findLabelledU('two blocks'); uok(!!cb,'found the two-blocks checkbox');
  RECU=makeRecU(); cb.checked=true; cb.fire('change');
  uok(ST.two===true&&vis('B mass, kg'),'two blocks switched on and the B rows appear');
  uok(chipsInU(GBLOCK,1).hidden===false,'with its material chips');
  uok(RECU.ops.length>30,'the stage redrew');
  uok(NODESU.readout.innerHTML.indexOf('block B')>=0,'the readout grew a block-B section');
  const y0=buildModel(ST).yw;
  cb.checked=false; cb.fire('change');
  uok(buildModel(ST).yw<y0-1e-4,'taking block B out drops the level');
}

/* ---- the REAL drag, from a proven-idle baseline, through the frame loop ---- */
tabU(0);
idleU('the pool view is idle before the grab');
{
  const M=buildModel(ST), G2=exploreGeo(RECU,1180,740,M), map=G2.map, bk=M.blocks[0];
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
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+4000,buttons:1});
  uok(Math.abs(ST.holdA-(-POOL_H))<1e-12,'dragged through the floor, the hold stops AT the floor');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y-4000,buttons:1});
  uok(Math.abs(ST.holdA-(POOL_YTOP-cubeSide(0.005)-0.012))<1e-12,
      'lifted, it stops where its top reaches the top of the drawn world ('+ST.holdA+')');
  uok(buildModel(ST).blocks[0].Vsub===0,'up there it displaces nothing');
  NODESU.scene.fire('pointerup',{});
  uok(DRAG.what===null&&ST.holdA===null,'pointer-up lets go');
  uok(Math.abs(buildModel(ST).yw-before)<1e-12,'and everything returns to equilibrium');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:Y+45,buttons:0});
  uok(ST.holdA===null,'a hover with no button pressed moves nothing');
}
for(const i of [1,2,3,4]){ tabU(i); idleU('tab '+i+' idle'); NODESU.scene.fire('pointerdown',{clientX:400,clientY:300});
  NODESU.scene.fire('pointermove',{clientX:600,clientY:340,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','tab '+i+' ignores the pointer'); NODESU.scene.fire('pointerup',{}); }

/* ---- the sets ---- */
tabU(1);
{
  const vis=lab2=>{ const r=rowU(lab2); return r&&r.hidden===false; };
  uok(vis('same mass, kg')&&!vis('same volume, L'),'same mass: only its own slider is live');
  uok(NODESU.readout.innerHTML.indexOf('brick')>=0&&NODESU.readout.innerHTML.indexOf('wood')>=0,
      'the readout names PhET\'s brick and wood');
  RECU=makeRecU(); chipG(GSET,0,'same volume',3).fire('click');
  uok(ST.setMode==='volume'&&vis('same volume, L'),'same volume selected, the slider swapped');
  uok(RECU.ops.length>30,'the view redrew');
  const M=buildModel(ST);
  uok(M.blocks.map(b=>Math.round(b.rho)).join(',')==='2000,400','still 2000 and 400 kg/m3');
  chipG(GSET,0,'same density',3).fire('click');
  const ds=sliderU('same density'); ds.value='900'; ds.fire('input');
  uok(buildModel(ST).blocks.every(b=>Math.abs(b.pct-90)<1e-9),'at 900 both float 90 % under, whatever the size');
  ds.value='2500'; ds.fire('input');
  uok(buildModel(ST).blocks.every(b=>b.mode==='rest'),'at 2500 they both sink');
  ds.value='400'; ds.fire('input');
  chipG(GSET,0,'same mass',3).fire('click');
}

/* ---- the faces ---- */
tabU(2);
{
  uok(NODESU.panel.children[GSCALES].hidden===true,'the scales group is hidden on the faces view');
  uok(NODESU.panel.children[GSET].hidden===true,'and so is the set group');
  const ds=sliderU('the bottom face, m'); uok(!!ds,'found the depth slider');
  RECU=makeRecU(); ds.value='0.9'; ds.fire('input');
  uok(Math.abs(ST.facesDepth-0.9)<1e-9,'the block is 90 cm down');
  uok(RECU.ops.length>20,'the view redrew');
  const deep=buildModel(ST);
  ds.value='0.45'; ds.fire('input');
  const mid=buildModel(ST);
  uok(Math.abs(deep.F.net-mid.F.net)<1e-9,'twice as deep, the NET force is identical');
  uok(deep.F.pBot>mid.F.pBot*1.9,'even though the pressure on the bottom face has doubled');
  uok(deep.resid<1e-13&&mid.resid<1e-13,'and both agree with rho g V to '+deep.resid.toExponential(2));
  ds.value='0.08'; ds.fire('input');
  const shallow=buildModel(ST);
  uok(!shallow.fullyUnder,'at 8 cm the top of the block is out of the fluid');
  uok(shallow.F.pTop===0,'so the top face is dry');
  uok(shallow.F.net<mid.F.net,'and the net force is smaller');
  uok(NODESU.readout.innerHTML.indexOf('0.00 N')>=0,'the readout says the four sides sum to 0.00 N');
  ds.value='0.45'; ds.fire('input');
}

/* ---- the scale ---- */
tabU(3);
{
  const ls=sliderU('lowered'); uok(!!ls,'found the lowered slider');
  ls.value='0'; ls.fire('input');
  const top=buildModel(ST);
  uok(Math.abs(top.read-top.W)<1e-9,'lowered 0, the scale reads the full weight');
  RECU=makeRecU(); ls.value='1'; ls.fire('input');
  uok(RECU.ops.length>20,'the view redrew');
  const bot=buildModel(ST);
  uok(bot.slack,'a wood block floats: the string goes slack');
  uok(Math.abs(bot.read)<1e-12,'and the spring reads zero');
  chipG(GBLOCK,0,'brick',7).fire('click');
  const vs=sliderU('volume, L'); vs.value='5'; vs.fire('input');
  const brick=buildModel(ST);
  uok(Math.abs(brick.W-98)<1e-9,'a 5 L brick weighs 98 N in air');
  uok(Math.abs(brick.full-49)<1e-9,'and 49 N once under');
  uok(Math.abs(brick.read-49)<1e-9,'which is what it reads at the bottom');
  uok(NODESU.readout.innerHTML.indexOf('49.00 N')>=0,'the readout prints it');
  /* the plateau */
  const under=brick.curve.filter(p=>p[2]>=brick.V-1e-12);
  uok(under.length>20,under.length+' of the 241 curve points are fully submerged');
  uok(under.every(p=>Math.abs(p[1]-49)<1e-9),'and every one of them reads 49 N: depth does not matter');
  chipG(GBLOCK,0,'wood',7).fire('click'); vs.value='5'; vs.fire('input');
  ls.value='0.55'; ls.fire('input');
}

/* ---- float or sink ---- */
tabU(4);
{
  uok(chipG(GGRID,0,'gold',27),'found the 27-material grid chip row');
  RECU=makeRecU(); chipG(GGRID,0,'gold',27).fire('click');
  uok(ST.gridMat==='gold','gold picked');
  uok(RECU.ops.length>60,'the grid redrew ('+RECU.ops.length+' ops)');
  uok(NODESU.readout.innerHTML.indexOf('sinks')>=0,'gold sinks in something');
  const M=buildModel(ST);
  uok(M.nCells===162,'162 combinations');
  uok(M.mercuryFloats===23,'23 of 27 float in mercury');
  uok(M.gasolineFloats===2,'only 2 in gasoline');
  chipG(GGRID,0,'lead',27).fire('click');
  uok(NODESU.readout.innerHTML.indexOf('83.4 % under')>=0,'lead floats in mercury, 83.4 % under');
  chipG(GGRID,0,'wood',27).fire('click');
  uok(NODESU.panel.children[GFLUID].hidden===true,'the fluid group is hidden on this view: it shows every fluid at once');
}

/* ---- keyboard, resize, reset all against disturbed state ---- */
keyU('1'); uok(ST.view==='explore','1 is the pool');
keyU('5'); uok(ST.view==='fluids','5 float or sink');
keyU('3'); uok(ST.view==='faces','3 the faces');
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===13,'the panel has its 10 sliders and 3 checkboxes ('+inputs.length+')');
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
  chipG(GBLOCK,0,'brick',7).fire('click'); ST.two=true; ST.fluid='honey'; ST.where='ground';
  ST.scaleH=0.9; ST.setMode='density'; ST.facesDepth=0.8; ST.lowered=0.1; ST.gridMat='gold';
  ST.forces=false; ST.labels=false; ST.holdA=-0.3; ST.sameRho=2900;
  uok(ST.matA==='brick'&&ST.holdA===-0.3&&ST.fluid==='honey','sentinel: the state really is disturbed');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.matA==='wood'&&ST.massA===2&&ST.volAL===5&&ST.two===false,'reset all restores PhET\'s block');
  uok(ST.fluid==='water'&&ST.where==='floor'&&ST.scaleH===0.5,'and the fluid and the scales');
  uok(ST.setMode==='mass'&&ST.sameRho===400&&ST.facesDepth===0.45&&ST.lowered===0.55,'and the set, the depth and the lowering');
  uok(ST.gridMat==='wood'&&ST.forces===true&&ST.labels===true&&ST.holdA===null,'and the grid, the arrows and the hold');
  uok(ST.view==='explore','keeping the view');
  ST.matA='brick'; keyU('r'); uok(ST.matA==='wood','the r key resets too');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
