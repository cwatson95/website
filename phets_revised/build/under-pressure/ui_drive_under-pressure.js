/* ============ UI drive test for under-pressure.html ====================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_buoy/ui_drive_bu.js
 * -> build/buoyancy-basics/ui_drive_buoyancy-basics.js).
 * The three sim-specific thresholds: chip rows are addressed by GROUP and row
 * index (the mystery group alone carries THREE rows -- 2 modes, 3 letters,
 * 3 answers -- so a label-only finder would drive the wrong one); the panel
 * has 11 groups; there are 18 inputs (10 sliders, 8 checkboxes).
 * Every drag runs THROUGH the frame loop from a proven-idle baseline, one
 * axis at a time, and every reset is checked against a sentinel. */
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
/* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
function rowU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function sliderU(label){ const r=rowU(label); return r?r.children[1]:null; }
function valOfU(label){ const r=rowU(label); return r?(r.children[2].textContent||''):null; }
function checkU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* the .tag div of a group: its innerHTML is rewritten by syncPanel, so it has
   to be read off the element itself rather than off the panel's textContent */
function tagTextU(gi){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='tag') hit=ch; walk(ch); } };
  walk(NODESU.panel.children[gi]); return hit?(hit.textContent||''):null; }
/* Chip rows by GROUP and row index, never by label alone: the mystery group
   carries a 2-chip row and TWO 3-chip rows whose labels are both A/B/C, so a
   label search would silently drive the answer row instead of the pool row. */
const GFLUID=0, GWORLD=1, GPOOL=2, GGAUGE=3, GSTACK=4, GMY=5, GVES=6, GLINE=7, GUNIT=8, GINFO=9, GPHYS=10;
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
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(4); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function forceDrawU(){ RECU=makeRecU(); pumpU(3); return geomU(RECU); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built ('+NODESU.tabs.children.length+')');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')==='the pool|the shapes|the press|the mystery|the paradox|the column',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===11,'the control panel has its 11 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.hint.textContent||'').indexOf('1–6')>=0,'the hint names the six view keys');
{
  const inputs=NODESU.panel.querySelectorAll('input');
  const nSlide=inputs.filter(i=>i.type==='range').length, nCheck=inputs.filter(i=>i.type==='checkbox').length;
  uok(inputs.length===18,'the panel has its 18 inputs ('+inputs.length+')');
  uok(nSlide===10&&nCheck===8,'10 sliders and 8 checkboxes ('+nSlide+'/'+nCheck+')');
}

/* ---- every tab draws, and draws something different ---- */
{
  const sigs=[];
  for(let i=0;i<6;i++){
    RECU=makeRecU(); tabU(i);
    uok(RECU.ops.length>20,'tab '+i+' ('+NODESU.tabs.children[i].textContent+') drew content ('+RECU.ops.length+' ops)');
    uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
    assertCleanU(RECU,'tab '+i);
    uok((NODESU.readout.innerHTML||'').length>250,'tab '+i+' rendered a readout');
    uok((NODESU.eqbar.innerHTML||'').indexOf('<span class="lhs">')===0,'tab '+i+' rendered an equation bar');
    sigs.push(sigU(RECU));
  }
  uok(new Set(sigs).size===6,'every tab draws a different picture ('+new Set(sigs).size+'/6)');
}

/* ---- the gauges drag, through the frame loop, one axis at a time ---- *
 * Exercising a drag is not testing it (Known-bad): every check below takes a
 * baseline from a PROVEN-IDLE loop, fires one axis, and asserts the emitted
 * geometry moved AND that the state the handler owns moved with it. */
function gaugePos(tag){
  const m=stageMap(makeRecU(),1180,740,ST);
  if(!m) return null;
  return {X:m.X(tag==='A'?ST.gAx:ST.gBx),Y:m.Y(tag==='A'?ST.gAy:ST.gBy),map:m};
}
/* the press lands 8 px off the marker's centre ON PURPOSE: pressing dead on it
   makes the grab radius irrelevant (dx = dy = 0 passes any threshold), and a
   mutant that shrank the radius to zero survived the first run of this file */
const GRABOFF=[8,6];
function dragFrom(X,Y,dx,dy){
  NODESU.scene.fire('pointerdown',{clientX:X+GRABOFF[0],clientY:Y+GRABOFF[1]});
  NODESU.scene.fire('pointermove',{clientX:X+GRABOFF[0]+dx,clientY:Y+GRABOFF[1]+dy,buttons:1});
  NODESU.scene.fire('pointerup',{});
}
tabU(0);
uok(!!stageMap(makeRecU(),1180,740,ST),'the pool view exposes a stage map for the pointer');
for(const [vi,vname] of [[0,'the pool'],[1,'the shapes'],[2,'the press']]){
  tabU(vi);
  clickButtonU('reset the gauges');
  for(const [axis,dx,dy] of [['horizontal',70,0],['vertical',0,60]]){
    idleU(vname+': the loop is idle before the '+axis+' drag');
    const before=forceDrawU();
    idleU(vname+': and idle again after the forced draw ('+axis+')');
    const p=gaugePos('A');
    const ax0=ST.gAx, ay0=ST.gAy, bx0=ST.gBx, by0=ST.gBy;
    RECU=makeRecU();
    dragFrom(p.X,p.Y,dx,dy);
    pumpU(3);
    const moved=geomU(RECU);
    uok(moved.length>50,vname+': a '+axis+' drag makes the frame loop repaint (dirty flag set)');
    uok(moved!==before,vname+': and the '+axis+' drag moved the drawing');
    if(axis==='horizontal'){
      uok(Math.abs(ST.gAx-ax0)>0.05,vname+': gauge A moved across ('+fmt(ST.gAx-ax0,3)+' m)');
      uok(Math.abs(ST.gAy-ay0)<1e-9,vname+': and not up or down');
    } else {
      uok(Math.abs(ST.gAy-ay0)>0.05,vname+': gauge A moved down ('+fmt(ST.gAy-ay0,3)+' m)');
      uok(Math.abs(ST.gAx-ax0)<1e-9,vname+': and not across');
    }
    uok(ST.gBx===bx0&&ST.gBy===by0,vname+': gauge B did not move with it');
  }
  /* gauge B is grabbed independently */
  clickButtonU('reset the gauges');
  {
    const p=gaugePos('B'), ax0=ST.gAx, ay0=ST.gAy;
    dragFrom(p.X,p.Y,-60,0); pumpU(3);
    uok(Math.abs(ST.gBx-DEFAULTS.gBx)>0.05,vname+': gauge B is draggable on its own');
    uok(ST.gAx===ax0&&ST.gAy===ay0,vname+': and gauge A stayed where it was');
  }
  /* a press far from either gauge grabs nothing and repaints nothing */
  clickButtonU('reset the gauges');
  idleU(vname+': idle before the empty-press test');
  {
    const ax0=ST.gAx, ay0=ST.gAy;
    RECU=makeRecU();
    dragFrom(6,6,40,40); pumpU(3);
    uok(geomU(RECU)==='[]',vname+': a press away from the gauges repaints nothing');
    uok(ST.gAx===ax0&&ST.gAy===ay0,'and moves nothing');
  }
}
/* The MOVE handler's own dirty flag, isolated.  pointerdown sets dirty too, so
   a down-then-move sequence repaints whether or not the move marks anything —
   two guards on one path make each other's mutant equivalent (Known-bad).
   Press, drain the flag, prove the loop is idle, and only THEN move. */
tabU(0);
clickButtonU('reset the gauges');
{
  const p=gaugePos('A');
  NODESU.scene.fire('pointerdown',{clientX:p.X+GRABOFF[0],clientY:p.Y+GRABOFF[1]});
  idleU('after the press alone, the loop goes quiet again');
  const ax0=ST.gAx;
  RECU=makeRecU();
  NODESU.scene.fire('pointermove',{clientX:p.X+GRABOFF[0]+80,clientY:p.Y+GRABOFF[1],buttons:1});
  pumpU(3);
  uok(geomU(RECU).length>50,'the MOVE alone marks the frame dirty and repaints');
  uok(Math.abs(ST.gAx-ax0)>0.05,'and it really moved the gauge');
  uok((NODESU.readout.innerHTML||'').length>300,'and the readout was rebuilt during the drag');
  NODESU.scene.fire('pointerup',{});
}
/* a press well away from a gauge must not grab it: the radius is load-bearing */
clickButtonU('reset the gauges');
{
  const p=gaugePos('A'), ax0=ST.gAx, ay0=ST.gAy;
  dragFrom(p.X+40,p.Y+40,60,0);
  uok(ST.gAx===ax0&&ST.gAy===ay0,'a press 40 px from the marker grabs nothing');
}
/* the drag clamps to the world: without the clamp a gauge leaves the stage */
clickButtonU('reset the gauges');
{
  const p=gaugePos('A'), E=extentFor(sceneOf(ST.view));
  dragFrom(p.X,p.Y,-4000,4000);
  uok(ST.gAx>=E.xmin-1e-9&&ST.gAx<=E.xmax+1e-9,'a drag far off the stage clamps x into the world');
  uok(ST.gAy>=E.ymin-1e-9&&ST.gAy<=E.ymax+1e-9,'and clamps y into the world');
  uok(Math.abs(ST.gAx-E.xmin)<1e-9,'landing exactly on the left edge');
  uok(Math.abs(ST.gAy-E.ymin)<1e-9,'and exactly on the floor');
  clickButtonU('reset the gauges');
}

/* the analysis views own no pointer at all */
for(const [vi,vname] of [[3,'the mystery'],[4,'the paradox'],[5,'the column']]){
  tabU(vi);
  uok(!stageMap(makeRecU(),1180,740,ST),vname+': has no draggable stage');
  idleU(vname+': idle before the pointer test');
  RECU=makeRecU();
  dragFrom(300,300,80,40); pumpU(3);
  uok(geomU(RECU)==='[]',vname+': a drag on it repaints nothing');
}

/* ---- dragging a gauge deeper really raises the reading (physics through UI) ---- */
tabU(0);
clickButtonU('reset all');
{
  const readNum=()=>{ const m=/gauge A<\/td><td class="v good">([\d.]+) kPa/.exec(NODESU.readout.innerHTML||''); return m?parseFloat(m[1]):NaN; };
  const p0=readNum();
  uok(isFinite(p0),'the readout prints gauge A in kPa ('+p0+')');
  const p=gaugePos('A');
  dragFrom(p.X,p.Y,0,40); pumpU(3);
  const p1=readNum();
  uok(isFinite(p1)&&p1>p0+0.5,'dragging gauge A downward raises its reading ('+p0+' -> '+p1+' kPa)');
  uok(ST.gAy<DEFAULTS.gAy,'because the gauge really went deeper');
  clickButtonU('reset all');
}

/* ---- the buttons ---- */
tabU(0);
uok(!!buttonU('same depth'),'the same-depth button exists');
ST.gAy=-2.10; ST.gBy=-0.90; clickButtonU('same depth');
uok(ST.gBy===-2.10,'same depth puts gauge B at gauge A\'s height');
{
  const M=buildModel(ST);
  uok(M.A.wet&&M.B.wet&&M.A.p===M.B.p,'and the two readings are then exactly equal');
}
ST.gAx=1.9; ST.gAy=0.3; ST.gBx=7.9; ST.gBy=-2.9;
uok(ST.gAx===1.9&&ST.gBy===-2.9,'sentinel: the gauges really are moved');
uok(clickButtonU('reset the gauges'),'the reset-gauges button fires');
uok(ST.gAx===DEFAULTS.gAx&&ST.gAy===DEFAULTS.gAy&&ST.gBx===DEFAULTS.gBx&&ST.gBy===DEFAULTS.gBy,
    'and it restores all four gauge coordinates');

/* ---- every slider, at both ends and the middle, with a repaint pinned ---- *
 * A drive-every-control sweep that only asserts no-throw leaves every
 * slider's REPAINT unpinned (Known-bad), so one slider gets the full
 * proven-idle treatment and the rest are swept for errors and clean panels. */
let ctlErrU=null;
try{
  tabU(0);
  idleU('idle before the slider-repaint test');
  {
    const s=sliderU('density ρ');
    uok(!!s,'found the density slider');
    RECU=makeRecU();
    s.value='1420'; s.fire('input'); pumpU(3);
    uok(geomU(RECU).length>50,'moving the density slider repaints immediately');
    uok(ST.rho===1420,'and the state followed it');
    uok((valOfU('density ρ')||'').indexOf('1420')>=0,'and the value readout followed it too');
    s.value='1000'; s.fire('input'); pumpU(3);
  }
  const SLIDERS=['density ρ','gravity g','faucet and drain','gauge A, across','gauge A, height',
                 'gauge B, across','gauge B, height','the gauge, depth','fluid depth','read it at'];
  for(const lb of SLIDERS){
    const s=sliderU(lb);
    uok(!!s,'found the slider "'+lb+'"');
    if(!s) continue;
    const lo=parseFloat(s.min), hi=parseFloat(s.max);
    for(const v of [lo,hi,(lo+hi)/2]){
      s.value=String(v); s.fire('input');
      uok(NODESU.errbox.style.display!=='block',lb+' at '+fmt(v,2)+' draws without error');
    }
  }
  const CHECKS=['atmosphere','grid','ruler','500 kg','250 kg','250 kg again','show the answer','the three named fluids'];
  for(const lb of CHECKS){
    const c=checkU(lb);
    uok(!!c,'found the checkbox "'+lb+'"');
    if(!c) continue;
    c.checked=!c.checked; c.fire('change');
    uok(NODESU.errbox.style.display!=='block','toggling "'+lb+'" draws without error');
    c.checked=!c.checked; c.fire('change');
  }
  /* the atmosphere switch is the one that changes the physics, not the picture */
  {
    tabU(0);
    const c=checkU('atmosphere');
    c.checked=false; c.fire('change');
    const M=buildModel(ST);
    uok(M.pSurf===0,'with the atmosphere off the surface reads exactly zero');
    uok(Math.abs(M.Fbot-M.weight)<1e-6,'and the floor carries exactly the weight of the fluid');
    c.checked=true; c.fire('change');
    uok(buildModel(ST).pSurf>1e5,'and switching it back restores an atmosphere');
  }
  /* every chip in every row, addressed by group and arity */
  const ROWS=[[GFLUID,0,3,['gasoline','water','honey']],
              [GWORLD,0,3,['Mars','Earth','Jupiter']],
              [GMY,0,2,['mystery fluid','mystery planet']],
              [GMY,1,3,['A','B','C']],
              [GMY,2,3,['A','B','C']],
              [GVES,0,4,['straight','flared','tapered','stepped']],
              [GUNIT,0,3,['kPa','atm','psi']]];
  for(const [gi,ri,ar,labels] of ROWS){
    const row=chipsInU(gi,ri);
    uok(!!row&&row.children.length===ar,'chip row '+gi+'.'+ri+' has its '+ar+' chips');
    for(const lb of labels){
      const chip=chipG(gi,ri,lb,ar);
      uok(!!chip,'chip "'+lb+'" is in row '+gi+'.'+ri);
      if(chip){ chip.fire('click');
        uok(NODESU.errbox.style.display!=='block','clicking "'+lb+'" draws without error'); }
    }
  }
  /* the chips really set what they claim to */
  chipG(GFLUID,0,'honey',3).fire('click'); uok(ST.rho===RHO_HONEY,'the honey chip sets 1420 kg/m3');
  chipG(GWORLD,0,'Jupiter',3).fire('click'); uok(ST.grav===G_JUPITER,'the Jupiter chip sets 24.9 m/s2');
  chipG(GFLUID,0,'water',3).fire('click'); chipG(GWORLD,0,'Earth',3).fire('click');
  /* the unit chips relabel the readout without moving the physics */
  {
    tabU(0);
    const pa=buildModel(ST).pBot;
    const seen={};
    for(const [lb,id] of [['kPa','metric'],['atm','atmosphere'],['psi','english']]){
      chipG(GUNIT,0,lb,3).fire('click');
      uok(ST.units===id,'the '+lb+' chip selects '+id);
      uok((NODESU.readout.innerHTML||'').indexOf(lb)>=0,'and the readout is labelled '+lb);
      seen[lb]=buildModel(ST).pBot;
    }
    uok(seen.kPa===pa&&seen.atm===pa&&seen.psi===pa,'and the pressure itself never moved');
    chipG(GUNIT,0,'kPa',3).fire('click');
  }
  /* a row a view ignores is HIDDEN, never left live and inert */
  const HIDE=[[0,[GSTACK,GMY,GVES,GLINE]],[1,[GSTACK,GMY,GVES,GLINE]],
              [2,[GPOOL,GMY,GVES,GLINE]],[3,[GGAUGE,GSTACK,GVES,GLINE]],
              [4,[GPOOL,GGAUGE,GSTACK,GMY,GLINE]],[5,[GPOOL,GGAUGE,GSTACK,GMY,GVES]]];
  for(const [vi,hidden] of HIDE){
    tabU(vi);
    for(const gi of hidden) uok(NODESU.panel.children[gi].hidden===true,
      'view '+vi+' hides panel group '+gi);
    uok(NODESU.panel.children[GUNIT].hidden!==true,'view '+vi+' keeps the unit chips');
    uok((tagTextU(GUNIT)||'').indexOf('101325')>=0,'view '+vi+': the unit tag names the exact atm');
  }
  tabU(2);
  uok(NODESU.panel.children[GSTACK].hidden!==true,'the press view shows the platform');
  uok((tagTextU(GSTACK)||'').indexOf('kPa')>=0,'and its tag prints the pressure the stack adds');
  tabU(3);
  uok(NODESU.panel.children[GMY].hidden!==true,'the mystery view shows the mystery group');
  /* the mystery group's two A/B/C rows are independent.  Both are set to a
     NON-default sentinel first, or "it did not change" would be vacuous: the
     chip sweep above has already clicked every chip in both rows. */
  chipG(GMY,1,'A',3).fire('click'); chipG(GMY,2,'C',3).fire('click');
  uok(ST.myWhich===0&&ST.myGuess==='2','sentinel: the two mystery rows start apart');
  chipG(GMY,1,'C',3).fire('click');
  uok(ST.myWhich===2,'the pool row picks which mystery is loaded');
  uok(ST.myGuess==='2','and leaves the answer row where it was');
  chipG(GMY,2,'B',3).fire('click');
  uok(ST.myGuess==='1'&&ST.myWhich===2,'the answer row picks the answer and leaves the pool alone');
  chipG(GMY,1,'A',3).fire('click'); chipG(GMY,2,'A',3).fire('click');
  /* every view still draws clean after the whole sweep */
  for(let v=0;v<6;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v);
    uok(RECU.ops.length>20,'after the control sweep, tab '+v+' still draws'); }
  /* keyboard */
  for(let k=1;k<=6;k++){ keyU(String(k)); uok(ST.view===TABS[k-1][0],'key '+k+' selects '+TABS[k-1][0]); }
  for(const f of (WINHU.resize||[])) f();
  uok(NODESU.errbox.style.display!=='block','resize handled');
  /* the reset disturbs EVERY kind of state it claims to restore, with a sentinel */
  tabU(0);
  ST.rho=1300; ST.grav=4.2; ST.atmosphere=false; ST.units='english'; ST.gridOn=true; ST.rulerOn=true;
  ST.volFrac=0.13; ST.gAx=1.8; ST.gAy=0.5; ST.gBx=8.0; ST.gBy=-2.95;
  ST.m500=false; ST.m250a=true; ST.m250b=true;
  ST.myMode='planet'; ST.myWhich=2; ST.myGuess='2'; ST.myReveal=true; ST.myDepth=0.2;
  ST.parDepth=0.4; ST.parPick='stepped'; ST.colDepth=2.7; ST.colAll=false;
  uok(ST.rho===1300&&ST.gAx===1.8&&ST.myReveal===true&&ST.colAll===false,'sentinel: the state really is disturbed');
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.rho===RHO_WATER&&ST.grav===G_EARTH&&ST.atmosphere===true&&ST.units==='metric','reset all restores the fluid and the world');
  uok(ST.gridOn===false&&ST.rulerOn===false&&ST.volFrac===0.5,'and the pool');
  uok(ST.gAx===DEFAULTS.gAx&&ST.gAy===DEFAULTS.gAy&&ST.gBx===DEFAULTS.gBx&&ST.gBy===DEFAULTS.gBy,'and the gauges');
  uok(ST.m500===true&&ST.m250a===false&&ST.m250b===false,'and the platform');
  uok(ST.myMode==='fluid'&&ST.myWhich===0&&ST.myGuess==='0'&&ST.myReveal===false&&ST.myDepth===1.5,'and the mystery');
  uok(ST.parDepth===2.0&&ST.parPick==='flared'&&ST.colDepth===1.5&&ST.colAll===true,'and the paradox and the line');
  uok(ST.view==='pool','keeping the view');
  ST.rho=1300; keyU('r'); uok(ST.rho===RHO_WATER,'the r key resets too');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
uok(NODESU.errbox.style.display!=='block','and nothing put an error on screen');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
