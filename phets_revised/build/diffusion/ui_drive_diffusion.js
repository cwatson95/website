
/* ============ UI drive test for diffusion.html ============================= *
 * DOM-stub harness taken from build/gas-properties/ui_drive_gas-properties.js
 * (which carries the Known-bad fix that innerHTML must strip tags into
 * textContent, or every chip built with html: reads as missing).  Three
 * canvas drags (the left-wall grip, the lid knob, the pump handle), a heater
 * that springs back, the divider button, the two species'
 * spinner grids, and the mixing, flow and speed views: every action must move
 * the picture THROUGH the frame loop from a proven-idle baseline. */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,arcs:0,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},
    lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);},
    arc(x,y,r){c.arcs++; c._p&&c._p.push([x,y,r]);},
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
    if(/NaN|undefined/.test(o[1])){ bad='NaN/undefined "'+String(o[1]).slice(0,40)+'"'; break; } }
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
        else if(want==='#phys'&&ch.id==='phys') out.push(ch);
        else if(want==='.chips'&&ch.className==='chips') out.push(ch);
        else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  let _html='', _txt='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },set(v){ _html=''+v; _txt=(''+v).replace(/<[^>]*>/g,''); }});
  Object.defineProperty(e,'textContent',{get(){ return _txt; },set(v){ _txt=''+v; }});
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
/* whole-label match (lagrange_points Known-bad: a substring finds the wrong row) */
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
function buttonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(label){ const b=buttonU(label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function geoU(){ return viewGeo(RECU,1400,820,buildModel()); }
function pauseU(){ const cb=findLabelledU('time runs'); if(cb.checked){ cb.checked=false; cb.fire('change'); } }
function playU(){ const cb=findLabelledU('time runs'); if(!cb.checked){ cb.checked=true; cb.fire('change'); } }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.panel.children.length>=6,'the control panel has its groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(/centre of mass/.test(NODESU.readout.innerHTML),'the readout carries PhET’s Centre of Mass row');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');
uok(NODESU.panel.textContent.indexOf('Diffusion')>=0,'… and it names Diffusion');

/* ---- every tab draws, differently, cleanly ---- */
/* ~80 % of what each tab emits at t = 0 (44, 82, 16, 91); the flow view is
   the small one because both its panels are empty until the divider is out */
const FLOORSU=[35,65,13,72];
const sigsU={};
for(let i=0;i<4;i++){
  RECU=makeRecU(); tabU(i);
  const nd=gasCount(worldOf().g);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(RECU.arcs>=nd,'tab '+i+' draws every one of its '+nd+' disks ('+RECU.arcs+' arcs)');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');
uok(worldOf()===worldOf(),'all four views share one gas (PhET’s Diffusion is one screen)');

/* ---- the clock ---- */
tabU(0); playU();
RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
uok(gA.length>50&&gB.length>50&&gA!==gB,'running: two frames draw DIFFERENT pictures (the disks move)');
{ const t0=worldOf().g.t; pumpU(24); uok(Math.abs(worldOf().g.t-t0-24*GAS.DT_FRAME)<1e-9,'24 frames advance the model 1 ps'); }
pauseU();
for(let i=0;i<4;i++){ tabU(i); idleU('tab '+i+' paints nothing while paused'); }
{ tabU(0); const t0=worldOf().g.t; keyU('s'); uok(Math.abs(worldOf().g.t-t0-0.2)<1e-12,'s steps exactly 0.2 ps (PhET’s MODEL_TIME_STEP)'); idleU('and the loop is idle again'); }
{ keyU(' '); uok(ST.running===true,'space runs'); keyU(' '); uok(ST.running===false,'space pauses'); }
{ const c=chipU('slow',2); c.fire('click'); uok(ST.slow===true&&viewDt(ST)===GAS.DT_SLOW,'slow is PhET’s 0.3 ps a second');
  const t0=worldOf().g.t; keyU(' '); pumpU(10); keyU(' ');
  uok(Math.abs(worldOf().g.t-t0-10*GAS.DT_SLOW)<1e-9,'… and the clock really runs at it');
  chipU('normal',2).fire('click'); keyU('r'); }

/* ---- the only canvas drag: lifting the divider out ---- */
tabU(0); keyU('r'); idleU('the box idles before the divider drag');
{ const w=worldOf(), g=w.g;
  uok(g.divided===true,'the divider starts in');
  const G=geoU(), k=divKnobGeo(G,buildModel());
  uok(!!k,'the divider has a handle');
  NODESU.scene.fire('pointerdown',{clientX:k.x+k.w/2,clientY:k.y+k.h/2});
  uok(DRAG.what==='divider','pointer-down on the handle grabs it');
  /* the grab ALONE must repaint: the handle turns magenta.  The recorder does
     not capture styles, so assert that a frame was DRAWN (ops emitted from a
     proven-quiet loop), not that the geometry moved. */
  RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>=FLOORSU[0],'the grab alone repaints through the loop ('+RECU.ops.length+' ops, a full frame is '+FLOORSU[0]+'+)');
  idleU('… and then the loop is idle again (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:k.x+k.w/2,clientY:k.y+k.h/2-0.4*DIV_TRAVEL,buttons:1});
  uok(Math.abs(w.divLift-0.4)<1e-9,'a 40 % lift registers as 40 % ('+fmt(w.divLift,3)+')');
  uok(g.divided===true,'… and the divider is still IN: nothing below the full travel removes it');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'the lift repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointermove',{clientX:k.x+k.w/2,clientY:k.y+k.h/2-1.2*DIV_TRAVEL,buttons:1});
  uok(g.divided===false,'lifting the full travel takes the divider out');
  uok(ST.divided===false,'… and the panel follows');
  uok(DRAG.what===null&&w.divLift===0,'… and the drag ends there');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU).length>50,'the removal repaints through the loop');
  NODESU.scene.fire('pointerup',{});
  uok(divKnobGeo(geoU(),buildModel())===null,'with the divider out there is no handle to grab');
  NODESU.scene.fire('pointerdown',{clientX:G.xR-40,clientY:G.yB-30});
  uok(DRAG.what===null,'a pointer-down inside the box grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }

/* ---- the divider button, and what it does to the model ---- */
keyU('r'); tabU(0);
{ const w=worldOf(), g=w.g;
  uok(g.divided===true,'r restarts with the divider in');
  const c0=gasCOM(g,0), c1=gasCOM(g,1);
  uok(Math.abs(c0-REF.com1)<4*REF.comSd1,'particle 1’s COM starts at '+fmt(c0,0)+' pm, against −4025 (4 sd = '+fmt(4*REF.comSd1,0)+')');
  uok(Math.abs(c1-REF.com2)<4*REF.comSd2,'… and particle 2’s at '+fmt(c1,0)+' pm');
  uok(!!buttonU('remove divider'),'the button reads remove divider');
  clickU('remove divider');
  uok(g.divided===false,'it comes out'); uok(buttonU('reset divider')!==null,'and the button now offers to reset it');
  playU(); pumpU(1440); pauseU();
  uok(g.flow.dts.length>0,'the flow counter runs with the divider out');
  uok(Math.abs(gasCOM(g,0))<Math.abs(c0)*0.7,'after 60 ps particle 1’s COM has moved toward the middle ('+fmt(gasCOM(g,0),0)+' pm)');
  uok(gasCOM(g,1)<c1,'… and particle 2’s has too');
  clickU('reset divider');
  uok(g.divided===true&&g.t===0,'reset divider restarts the run (PhET regenerates both species)');
  uok(gasCount(g,0)===ST.d1n&&gasCount(g,1)===ST.d2n,'… at the slider counts');
  uok(Math.abs(gasCOM(g,0)-REF.com1)<4*REF.comSd1,'… back at −4025 pm'); }

/* ---- the species controls behave as PhET's do ---- */
{ const g=worldOf().g;
  const m=sliderU('mass, AMU'); m.value='16'; m.fire('input'); uok(g.species[0].m===16,'particle 1 mass 16 AMU');
  let one=true; for(let i=0;i<g.n;i++) if(g.sp[i]===0&&Math.abs(gasSpeed(g,i)-Math.sqrt(3*GAS.K*300/16))>1e-9) one=false;
  uok(one,'… and every particle 1 is reset to √(3kT/m), as PhET does');
  const r=sliderU('radius, pm '); r.value='200'; r.fire('input'); uok(g.species[1].r===200,'particle 2 radius 200 pm');
  const n=sliderU('number '); n.value='50'; n.fire('input'); uok(gasCount(g,1)===50,'particle 2 count 50');
  const T=sliderU('initial T, K '); T.value='500'; T.fire('input');
  uok(Math.abs(gasTemp(g,1)-500)<1e-9,'particle 2 starting temperature 500 K');
  uok(/T<sub>avg<\/sub>/.test(NODESU.readout.innerHTML),'PhET’s Data panel shows T_avg for each side');
  keyU('r'); }

/* ---- the presets ---- */
{ chipU('identical',4).fire('click');
  const g=worldOf().g;
  uok(g.species[0].m===g.species[1].m&&g.species[0].r===g.species[1].r,'the identical preset makes both species the same');
  uok(ST.d1m===28&&ST.d2m===28,'… at PhET’s own default 28 AMU');
  clickU('remove divider'); playU(); pumpU(2400); pauseU();
  uok(Math.abs(gasCOM(g,0))<1500,'… and they still mix: that is the entropy of mixing with nothing else going on ('+fmt(gasCOM(g,0),0)+' pm)');
  chipU('hot and cold',4).fire('click');
  const g2=worldOf().g;
  uok(Math.abs(gasTemp(g2,0)-500)<1e-9&&Math.abs(gasTemp(g2,1)-100)<1e-9,'the hot-and-cold preset starts them at 500 and 100 K');
  const want=REF.tCommon500_100;
  clickU('remove divider'); playU(); pumpU(2400); pauseU();
  uok(Math.abs(gasTemp(g2,0)-want)<0.1*want,'after 100 ps the hot gas has cooled to '+fmt(gasTemp(g2,0),0)+' K, near the common '+fmt(want,0));
  uok(Math.abs(gasTemp(g2,1)-want)<0.1*want,'… and the cold one has warmed to '+fmt(gasTemp(g2,1),0)+' K');
  chipU('big and small',4).fire('click');
  uok(worldOf().g.species[0].r===250&&worldOf().g.species[1].r===50,'the big-and-small preset');
  chipU('heavy and light',4).fire('click'); keyU('r'); }

/* ---- the mixing view: the profiles and the imbalance ---- */
tabU(1);
{ const w=worldOf(), g=w.g;
  const p0=profile(g);
  let leftOnly=true; for(let q=NPROF/2;q<NPROF;q++) if(p0[0][q]>0) leftOnly=false;
  uok(leftOnly,'divided: particle 1 is entirely in the left half of the profile');
  RECU=makeRecU(); tabU(1);
  const txt=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/slices/.test(txt)||/profile/.test(txt),'the profile panel is titled');
  uok(/imbalance/.test(txt)||/ΔN/.test(txt),'… and so is the imbalance panel');
  clickU('remove divider'); playU(); pumpU(1440); pauseU();
  const p1=profile(g), mean=gasCount(g,0)/NPROF;
  let chi2=0; for(let q=0;q<NPROF;q++) chi2+=(p1[0][q]-mean)*(p1[0][q]-mean)/mean;
  uok(chi2<2*NPROF,'after 60 ps the profile is flat to a χ² of '+fmt(chi2,1)+' on '+(NPROF-1)+' d.o.f.');
  const M=buildModel();
  uok(M.tauEff[0]>0&&M.tauDif[0]>M.tauEff[0],'the Fickian bound is longer than the effusion one ('+fmt(M.tauDif[0],0)+' vs '+fmt(M.tauEff[0],0)+' ps)');
  uok(/mean free path/.test(NODESU.readout.innerHTML),'the readout gives the mean free path');
  keyU('r'); }

/* ---- the flow view: two measurements against kinetic theory ---- */
tabU(2);
{ const w=worldOf(), g=w.g;
  RECU=makeRecU(); tabU(2);
  uok(RECU.ops.some(o=>o[0]==='t'&&/divider/.test(o[1])),'with the divider in the flow view says nothing crosses');
  clickU('remove divider'); playU(); pumpU(720); pauseU();
  const M=buildModel();
  uok(g.flow.rateR[0]>0&&g.flow.rateL[1]>0,'both species are crossing');
  /* the 300-frame window holds only a handful of crossings per direction once
     the gases have equalised, so the bound has to be the Poisson one */
  const Twin=g.flow.dts.reduce((a,b)=>a+b,0);
  let worstZ=0, tested=0;
  for(const k of [0,1]) for(const dir of [0,1]){
    const meas=dir?g.flow.rateR[k]:g.flow.rateL[k], th=M.flowTh[k][dir?0:1];
    const n=meas*Twin;
    if(th>0.05&&n>=3){ tested++; worstZ=Math.max(worstZ,Math.abs(meas-th)/(th/Math.sqrt(n))); }
  }
  uok(tested>=3,tested+' of the four crossing rates had enough counts to test');
  uok(worstZ<4,'every one of them is within 4 σ of n⟨v_x⁺⟩(H−2r) (worst '+fmt(worstZ,2)+' σ)');
  const P=M.pairMe;
  uok(P&&P.n>500,'the rolling window has counted '+(P?P.n:0)+' pair collisions');
  uok(Math.abs(P.rate/M.pairTh-1)<0.15,'the pair-collision rate is within 15 % of Σⱼ nⱼ 2(rᵢ+rⱼ)⟨v_rel⟩ ('+fmt(P.rate,1)+' vs '+fmt(M.pairTh,1)+')');
  uok(/measured \/ theory/.test(NODESU.readout.innerHTML),'the readout compares them');
  keyU('r'); }

/* ---- the speeds view: PhET's spike relaxes ---- */
tabU(3);
{ const w=worldOf(), g=w.g;
  for(const k of [0,1]){
    const v0=gasMeanSpeedOf(g,k);
    uok(Math.abs(v0/mbRmsSpeed(g.species[k].m,gasKT2(300))-1)<1e-9,'species '+(k+1)+' starts at one speed, √(3kT/m)');
  }
  const cb=findLabelledU('Maxwell–Boltzmann curves'); uok(!!cb&&cb.checked===true,'the MB curves are on');
  RECU=makeRecU(); tabU(3); const nWith=RECU.ops.length;
  cb.checked=false; cb.fire('change'); RECU=makeRecU(); tabU(3);
  uok(RECU.ops.length<nWith,'switching them off draws less ('+RECU.ops.length+' vs '+nWith+')');
  cb.checked=true; cb.fire('change');
  clickU('remove divider'); playU(); pumpU(1440); pauseU();
  for(const k of [0,1]){
    const v=gasMeanSpeedOf(g,k), want=mbMeanSpeed(g.species[k].m,gasKT2(gasTemp(g,k)));
    uok(Math.abs(v/want-1)<0.05,'species '+(k+1)+'’s mean speed relaxed to √(πkT₂/2m) ('+fmt(v,0)+' vs '+fmt(want,0)+')');
    uok(v<mbRmsSpeed(g.species[k].m,gasKT2(gasTemp(g,k))),'… i.e. it FELL, by the √(π/4) the readout quotes');
  }
  uok(/11\.38 %/.test(NODESU.readout.innerHTML),'the readout quotes the 11.38 % drop');
  keyU('r'); }

/* ---- the checkboxes, units, keyboard ---- */
tabU(0);
{ for(const lab of ['centre of mass','particle flow rate','scale']){
    const cb=findLabelledU(lab); uok(!!cb,'found '+lab);
    RECU=makeRecU(); tabU(0); const on=RECU.ops.length;
    cb.checked=false; cb.fire('change'); RECU=makeRecU(); tabU(0);
    uok(RECU.ops.length<=on,lab+' off draws no more than on ('+RECU.ops.length+' vs '+on+')');
    cb.checked=true; cb.fire('change'); }
  const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change'); uok(ST.showWatch===true,'the stopwatch shows');
  clickU('stopwatch start / stop'); playU(); pumpU(24); pauseU();
  uok(Math.abs(worldOf().g.watch.t-1)<1e-9,'it counted 1 ps'); clickU('reset'); uok(worldOf().g.watch.t===0,'and resets');
  chipU('°C',2).fire('click'); uok(/°C/.test(NODESU.readout.innerHTML),'°C in the readout'); chipU('K',2).fire('click'); }
keyU('3'); uok(ST.view==='flow','3 switches to the flow view'); keyU('1'); uok(ST.view==='box','1 back');
{ const g=worldOf().g; clickU('remove divider'); keyU('r');
  uok(worldOf().g.divided===true,'r restarts the experiment'); }

/* ---- every control, chips, resize ---- */
let ctlErrU=null;
try{
  for(let t=0;t<4;t++){ tabU(t);
    const inputs=NODESU.panel.querySelectorAll('input');
    for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
    pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
    RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===14,'the panel has its 8 sliders and 6 checkboxes ('+inputs.length+')');
  for(const g2 of NODESU.panel.children){ const cws=g2.querySelectorAll('.chips'); for(const cw of cws) for(const ch of cw.children) ch.fire('click'); }
  uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
