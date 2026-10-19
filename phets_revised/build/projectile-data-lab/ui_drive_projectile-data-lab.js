
/* ============ UI drive test for projectile-data-lab.html ================== *
 * DOM-stub pattern (lineage: build_buoy/ui_drive_bu.js, via the gas-properties
 * remake).  The one canvas drag is the interval tool — its two edges and its
 * middle — and it must move the picture THROUGH the frame loop from a
 * proven-idle baseline (time paused, loop drained, idle frame drew nothing).
 * Chip rows are found by their data-key, never by a label: six of them are
 * labelled 1..6 and a match-by-word finder would drive the wrong one. */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,arcs:0,rects:0,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},
    lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);},
    arc(x,y,r){c.arcs++; c._p&&c._p.push([x,y,r]);},
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){c.rects++; ops.push(['r',Math.round(x),Math.round(y),Math.round(w),Math.round(h)]);},
    strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
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
    _h:{},className:'',id:'',value:'0',checked:false,hidden:false,disabled:false,
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
  /* the stub must derive textContent from innerHTML, because a real browser
     does and a chip built with h(tag,{html:...}) otherwise reports an EMPTY
     label (drum_head Known-bad) */
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
/* chip rows are found by the data-key the sim stamps on them */
function chipsU(key){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch['data-key']===key) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(key,label){ const r=chipsU(key); if(!r) return null;
  for(const c of r.children) if((c.textContent||'')===label) return c;
  return null; }
function buttonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(label){ const b=buttonU(label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+(geomU(RECU)==='[]'?'':' ('+RECU.ops.length+' ops)')); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const cb=findLabelledU('time runs'); if(cb.checked){ cb.checked=false; cb.fire('change'); } }
function playU(){ const cb=findLabelledU('time runs'); if(!cb.checked){ cb.checked=true; cb.fire('change'); } }
/* the interval tool's geometry, recomputed the way the sim does */
function histBoxU(){
  const M=buildModel(), ph=measCaption(M,'1.00');
  return labStage(RECU,1400,820,ph.full,ph.short,{histFrac:0.46,fieldWant:fieldWantH(M)}).hist;
}
function xOfU(v){ const b=histBoxU(); return b.x+b.w*v/PDL.FIELD; }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.panel.children.length>=12,'the control panel has its groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(/46\.530 m/.test(NODESU.readout.innerHTML),'the readout prints launcher 1’s exact mean, 46.530 m');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');
uok(NODESU.hint.textContent.length>10,'the hint line is set');

/* ---- every tab draws, differently, cleanly ---- */
/* floors at ~75 % of what each tab emits at its defaults (measured: 129, 208,
   157, 178, 41, 27 ops); the field views also draw one arc per landed shot,
   so the substance is floored on that too rather than on the op count alone */
const FLOORSU=[96,155,117,133,30,20];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
tabU(0);
{ const F=curField(ST);
  RECU=makeRecU(); tabU(0);
  uok(RECU.arcs>=F.landed.length,'the field draws a marker for every one of its '+F.landed.length+' landed shots ('+RECU.arcs+' arcs)');
  uok(NODESU.readout.innerHTML.indexOf('>'+F.landed.length+' landed')>=0
      ||NODESU.readout.innerHTML.indexOf(F.landed.length+' landed')>=0,'and the readout counts them');
}

/* ---- the clock and the launcher ---- */
playU();
tabU(0); idleU('with nothing in flight the loop is idle');
{ const F=curField(ST), n0=F.landed.length;
  keyU(' ');
  uok(F.firing===true,'space starts the launcher');
  pumpU(2);
  uok(F.air.length===1,'one projectile is in the air');
  uok(F.firing===false,'and in single mode the launcher stops itself');
  RECU=makeRecU(); pumpU(1); const a=geomU(RECU); RECU=makeRecU(); pumpU(1); const b=geomU(RECU);
  uok(a.length>50&&b.length>50&&a!==b,'while it flies, two frames draw DIFFERENT pictures');
  const T=F.air[0].T;
  pumpU(Math.ceil(T*60)+4);
  uok(F.air.length===0&&F.landed.length===n0+1,'it lands, and the field has one more shot');
  const p=F.landed[F.landed.length-1];
  uok(Math.abs(p.x-pdlRange(p.v,p.ang,F.cfg.h))<1e-12,'it landed exactly where the closed form says');
  uok(Math.abs(p.t-p.T)<1e-12,'and its clock stopped at the flight time');
  idleU('and the loop goes quiet again');
}
{ /* continuous fire: one every 0.7 s (PhET's minimum), and stop stops it */
  chipU('mode','continuous').fire('click');
  const F=curField(ST), n0=F.landed.length+F.air.length;
  keyU(' '); uok(F.firing===true,'continuous mode: space starts it');
  pumpU(Math.round(0.7*60*3)+6);
  const made=F.landed.length+F.air.length-n0;
  uok(made>=3&&made<=5,'about one shot every 0.7 s ('+made+' in 2.1 s)');
  keyU(' '); uok(F.firing===false,'space again stops it');
  pumpU(300);
  uok(F.air.length===0,'and the last of them lands');
  chipU('mode','single').fire('click');
}
{ const F=curField(ST); keyU('c');
  uok(F.landed.length===0&&F.air.length===0,'c clears the field');
  RECU=makeRecU(); tabU(0);
  uok(RECU.ops.some(o=>o[0]==='t'&&/0 landed/.test(o[1]))||NODESU.readout.innerHTML.indexOf('0 landed')>=0,
      'and the readout says so');
  clickU('+50 at once');
  uok(F.landed.length===50,'+50 at once fills it again');
  uok(F.air.length===0,'without any of them passing through the air');
}
{ keyU('p'); uok(ST.running===false,'p pauses'); keyU('p'); uok(ST.running===true,'p runs again'); }

/* ---- the interval tool: the one thing on the canvas you can drag ---- */
tabU(2); pauseU();
idleU('the measures view idles while paused');
{ const b=histBoxU(), y=b.y+10;
  const e1=ST.e1, e2=ST.e2;
  NODESU.scene.fire('pointerdown',{clientX:xOfU(e1),clientY:y});
  uok(DRAG.what==='e1','pointer-down on the left edge grabs it');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:xOfU(30),clientY:y,buttons:1});
  uok(Math.abs(ST.e1-30)<0.1,'dragging it to 30 m moves the edge there ('+ST.e1+')');
  uok(ST.e2===e2,'and leaves the other edge alone');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'the drag repaints THROUGH the frame loop (the dirty flag)');
  idleU('and the loop goes idle again');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(NODESU.readout.innerHTML.indexOf('30.0, 60.0 m')>=0,'the readout followed the drag');
  /* the right edge */
  NODESU.scene.fire('pointerdown',{clientX:xOfU(ST.e2),clientY:y});
  uok(DRAG.what==='e2','pointer-down on the right edge grabs that one');
  NODESU.scene.fire('pointermove',{clientX:xOfU(80),clientY:y,buttons:1});
  uok(Math.abs(ST.e2-80)<0.1,'and it follows the pointer ('+ST.e2+')');
  NODESU.scene.fire('pointerup',{});
  /* the middle: both edges move, the width is kept */
  const w0=ST.e2-ST.e1;
  NODESU.scene.fire('pointerdown',{clientX:xOfU((ST.e1+ST.e2)/2),clientY:y});
  uok(DRAG.what==='mid','pointer-down in the middle grabs the whole window');
  NODESU.scene.fire('pointermove',{clientX:xOfU(50),clientY:y,buttons:1});
  uok(Math.abs((ST.e2-ST.e1)-w0)<0.2,'sliding it keeps the width ('+fmt(ST.e2-ST.e1,1)+' vs '+fmt(w0,1)+')');
  uok(Math.abs((ST.e1+ST.e2)/2-50)<0.3,'and centres it where the pointer is');
  NODESU.scene.fire('pointerup',{});
  /* a miss grabs nothing and paints nothing */
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:10,clientY:60});
  uok(DRAG.what===null,'a pointer-down away from the tool grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties');
  NODESU.scene.fire('pointerup',{});
  /* the tool is not draggable when it is hidden */
  const cbI=findLabelledU('interval tool'); cbI.checked=false; cbI.fire('change');
  NODESU.scene.fire('pointerdown',{clientX:xOfU(ST.e1),clientY:y});
  uok(DRAG.what===null,'with the interval tool switched off there is nothing to grab');
  NODESU.scene.fire('pointerup',{}); cbI.checked=true; cbI.fire('change');
}
{ /* the percentage it reports is the count, and it agrees with the model */
  ST.e1=0; ST.e2=100;
  const M=buildModel();
  uok(Math.abs(M.frac-1)<1e-12,'the whole field holds 100 % of the data');
  ST.e1=40; ST.e2=60;
  const M2=buildModel(), xs=M2.xs;
  let k=0; for(const x of xs) if(x>=40&&x<=60) k++;
  uok(Math.abs(M2.frac-k/xs.length)<1e-12,'and the reported fraction is that count over n');
}

/* ---- the measures overlay ---- */
{ const M=buildModel();
  for(const [lbl,key] of [['mean','showMean'],['standard deviation','showSd'],['values','showValues']]){
    const cb=findLabelledU(lbl); uok(!!cb,'found the '+lbl+' checkbox');
    cb.checked=true; cb.fire('change');
    RECU=makeRecU(); tabU(2);
    const txt=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
    if(key==='showMean') uok(/x̄ = /.test(txt),'the mean marker is labelled on the canvas');
    if(key==='showSd') uok(/n−1/.test(txt),'the standard-deviation bar names its convention');
    if(key==='showValues') uok(RECU.ops.filter(o=>o[0]==='t').length>20,'the values fill the field with numbers');
    cb.checked=false; cb.fire('change');
  }
  findLabelledU('mean').checked=true; findLabelledU('mean').fire('change');
  uok(NODESU.readout.innerHTML.indexOf(fmt(M.stat.sd1,4)+' m')>=0,'the readout prints the n−1 standard deviation');
  uok(NODESU.readout.innerHTML.indexOf(fmt(M.stat.sd0,4)+' m')>=0,'and the n one beside it');
}

/* ---- the launchers, the mechanisms, the orientations ---- */
tabU(0);
{ const F=curField(ST);
  clickU('+50 at once');
  const n0=F.landed.length; uok(n0>0,'the field has shots before the launcher changes');
  chipU('lau','6').fire('click');
  uok(ST.lau===6,'launcher 6 selected');
  const F2=curField(ST);
  uok(F2.landed.length===0,'changing a field’s launcher CLEARS it (a mixed histogram is not a distribution)');
  uok(Math.abs(F2.cfg.sdAng-5)<1e-12,'and the field now carries launcher 6’s 5° angle spread');
  clickU('+50 at once');
  const E6=pdlExact(F2.cfg);
  uok(NODESU.readout.innerHTML.indexOf(fmt(E6.sd,4)+' m')>=0,'the readout shows launcher 6’s exact σ = '+fmt(E6.sd,4)+' m');
  /* each field keeps its own shots */
  chipU('fld','2').fire('click');
  uok(ST.lau===worldOf('field').fields[1].lau,'switching field adopts that field’s launcher');
  chipU('fld','1').fire('click');
  uok(ST.lau===6,'and switching back restores the first field’s');
}
tabU(1);
{ const F=curField(ST);
  chipU('mech','explosion').fire('click');
  uok(F.cfg.meanSpeed===25&&F.cfg.sdSpeed===1.2,'the explosion mechanism is PhET’s 25 ± 1.2 m/s');
  uok(F.landed.length===0,'and changing it clears the field');
  const s=sliderU('angle stability'); uok(!!s,'found the angle-stability slider');
  s.value='1'; s.fire('input');
  uok(Math.abs(curField(ST).cfg.sdAng-0.2)<1e-12,'stability 1 gives PhET’s TIGHTEST 0.2° spread');
  s.value='0'; s.fire('input');
  uok(Math.abs(curField(ST).cfg.sdAng-5)<1e-12,'stability 0 gives the loosest 5°');
  s.value='0.5'; s.fire('input');
  chipU('ptype','pumpkin').fire('click');
  uok(Math.abs(curField(ST).cfg.mult-1.1)<1e-12,'a pumpkin carries PhET’s ×1.1 speed multiplier');
  chipU('orient','0° raised').fire('click');
  uok(curField(ST).cfg.h===12&&curField(ST).cfg.raised===true,'the raised launcher is 12 m up and exempt from the angle re-draw');
  clickU('+50 at once');
  let neg=0; for(const p of curField(ST).landed) if(p.ang<0) neg++;
  uok(neg>0,'… so some of its shots really do leave below the horizontal ('+neg+' of 50)');
  chipU('orient','45°').fire('click'); chipU('ptype','cannonball').fire('click'); chipU('mech','spring').fire('click');
  uok(curField(ST).cfg.meanAng===45,'45° selected');
}

/* ---- the histogram controls ---- */
tabU(0);
{ clickU('+50 at once');
  const M=buildModel(), n=M.stat.n;
  chipU('binW','5 m').fire('click');
  const M5=buildModel();
  uok(M5.binW===5,'the 5 m bin width is selected');
  let s=0; for(const c of M5.hist.counts) s+=c;
  uok(s===n,'and every shot is still in a bin');
  chipU('binW','0.5 m').fire('click');
  const Mh=buildModel();
  uok(Mh.hist.counts.length>=M5.hist.counts.length,'a narrower bin gives at least as many bins');
  chipU('binStrat','total bins').fire('click');
  uok(buildModel().binW===PDL.FIELD/ST.nBins,'the total-bins strategy sets the width to 100/bins');
  uok(chipU('binW','0.5 m').disabled===true,'and the bin-width chips go dead rather than staying live and ignored');
  chipU('nBins','50').fire('click');
  uok(Math.abs(buildModel().binW-2)<1e-12,'50 bins across 100 m is a 2 m width');
  chipU('binStrat','bin width').fire('click');
  uok(chipU('nBins','50').disabled===true,'and now the total-bins chips are the dead ones');
  chipU('binW','1 m').fire('click');
}
{ /* blocks and bars draw different pictures of the same data */
  RECU=makeRecU(); tabU(0); const blocks=sigU(RECU);
  const cb=findLabelledU('blocks, one per projectile'); cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(0); const bars=sigU(RECU);
  uok(blocks!==bars,'blocks and bars are different drawings');
  uok(RECU.rects>0,'the bar form fills rectangles');
  cb.checked=true; cb.fire('change');
}
{ for(const lbl of ['paths','launch angle','launch speed']){
    const cb=findLabelledU(lbl); uok(!!cb,'found the '+lbl+' checkbox');
    RECU=makeRecU(); tabU(0); const before=sigU(RECU);
    cb.checked=!cb.checked; cb.fire('change');
    RECU=makeRecU(); tabU(0);
    uok(sigU(RECU)!==before,'the '+lbl+' checkbox changes the picture');
    cb.checked=!cb.checked; cb.fire('change');
  }
}

/* ---- the sampling view ---- */
tabU(3);
{ const F=curField(ST);
  uok(F.samples.length>0,'the sampling field opens with samples in it');
  uok(F.samples[0].xs.length===ST.pN,'each sample holds n launches');
  const before=F.samples.length;
  clickU('+20 samples');
  uok(curField(ST).samples.length===before+20,'+20 samples adds twenty');
  const M=buildModel();
  uok(Math.abs(M.mstat.mean-pdlMean(M.means))<1e-12,'the readout’s mean of the sample means is that mean');
  chipU('pN','n = 40').fire('click');
  const M40=buildModel();
  uok(ST.pN===40,'n = 40 selected');
  uok(M40.F.size===40,'and its own field is the n = 40 one');
  const se40=M40.exact.sd/Math.sqrt(40), se5=M40.exact.sd/Math.sqrt(5);
  uok(Math.abs(se5/se40-Math.sqrt(8))<1e-12,'σ/√5 over σ/√40 is exactly √8');
  uok(NODESU.readout.innerHTML.indexOf(fmt(se40,4)+' m')>=0,'the readout prints σ/√40 = '+fmt(se40,4)+' m');
  chipU('pN','n = 5').fire('click');
  /* starting a sample by hand clears the last one off the field — the path
     only fireField takes, so it must be tested with shots ALREADY there */
  { const H=curField(ST); clickU('+20 samples'); playU();
    uok(H.landed.length===ST.pN,'the field is showing the last sample’s '+ST.pN+' shots');
    keyU(' ');
    uok(H.landed.length===0&&H.air.length===0,'space starts a new one and clears them');
    keyU(' '); H.firing=false; pauseU(); }
  /* a sample fires one projectile at a time and only then records its mean */
  const G=curField(ST); fieldClear(G); playU();
  keyU(' '); uok(G.firing===true,'space starts a sample');
  pumpU(4); uok(G.air.length+G.landed.length>=1,'the first projectile of it is away');
  uok(G.samples.length===0,'and no mean is recorded until the sample is complete');
  for(let i=0;i<900&&G.samples.length===0;i++) pumpU(1);
  uok(G.samples.length===1,'when the fifth lands, one mean is recorded');
  uok(Math.abs(G.samples[0].mean-pdlMean(G.samples[0].xs))<1e-12,'and it is the mean of those five');
  pauseU();
  const cb=findLabelledU('show the standard error');
  RECU=makeRecU(); tabU(3); const withSe=sigU(RECU);
  cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(3);
  uok(sigU(RECU)!==withSe,'the standard-error checkbox changes the picture');
  cb.checked=true; cb.fire('change');
  clickU('clear'); uok(curField(ST).samples.length===0,'clear empties the sampling field');
  clickU('+20 samples');
}

/* ---- the two analysis views ---- */
tabU(4);
{ const M=buildModel();
  uok(M.stat.n===ST.xN,'the exact-law view draws the number of launches its slider asks for');
  const s=sliderU('launches drawn'); s.value='500'; s.fire('input');
  uok(buildModel().stat.n===500,'moving that slider redraws the sample');
  s.value='300'; s.fire('input');
  chipU('xLau','3').fire('click');
  const E3=pdlExact(cfgMystery(3));
  uok(Math.abs(buildModel().exact.mean-E3.mean)<1e-12,'the launcher chip moves the exact law with it');
  uok(NODESU.readout.innerHTML.indexOf(fmt(E3.mean,3)+' m')>=0,'and the readout prints its mean, '+fmt(E3.mean,3)+' m');
  for(const lbl of ['the exact density','PhET’s delta-method normal']){
    const cb=findLabelledU(lbl); uok(!!cb,'found the '+lbl+' checkbox');
    RECU=makeRecU(); tabU(4); const before=sigU(RECU);
    cb.checked=!cb.checked; cb.fire('change');
    RECU=makeRecU(); tabU(4);
    uok(sigU(RECU)!==before,'the '+lbl+' checkbox changes the picture');
    cb.checked=!cb.checked; cb.fire('change');
  }
  chipU('xOrient','0° raised').fire('click');
  uok(buildModel().cfg.h===12,'the raised orientation reaches the exact-law view too');
  uok(buildModel().naive===null,'… where v²sin2θ/g does not apply and is not offered');
  chipU('xOrient','30°').fire('click'); chipU('xLau','2').fire('click');
}
tabU(5);
{ const M=buildModel();
  uok(M.sets.length===4,'the limit-theorem view builds four sample sizes');
  M.sets.forEach((S,i)=>{
    uok(S.means.length===ST.cM,'n = '+S.n+': '+ST.cM+' samples');
    const want=M.exact.sd/Math.sqrt(S.n);
    const tol=want*Math.sqrt((M.exact.kurt/S.n+2)/(4*ST.cM));
    uok(Math.abs(S.sd-want)<5*tol,'n = '+S.n+': the measured SE '+fmt(S.sd,4)+' sits within 5 of its own sampling sd of σ/√n = '+fmt(want,4));
  });
  const s=sliderU('samples at each n'); s.value='200'; s.fire('input');
  uok(buildModel().sets[0].means.length===200,'the samples-per-size slider rebuilds the experiment');
  s.value='400'; s.fire('input');
  chipU('cLau','4').fire('click');
  uok(Math.abs(buildModel().exact.mean-pdlExact(cfgMystery(4)).mean)<1e-12,'and the launcher chip moves it');
  const cb=findLabelledU('σ/√n, the theorem');
  RECU=makeRecU(); tabU(5); const before=sigU(RECU);
  cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(5);
  uok(sigU(RECU)!==before,'the theorem curves can be switched off');
  cb.checked=true; cb.fire('change');
  chipU('cLau','1').fire('click');
}

/* ---- a slider must repaint AT ONCE, not only on the next frame ---- */
tabU(2); pauseU(); idleU('idle before the slider repaint test');
{ const s=sliderU('interval from'); RECU=makeRecU();
  s.value='15'; s.fire('input');
  uok(Math.abs(ST.e1-15)<1e-9,'the interval-from slider sets 15 m');
  uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)');
  s.value='40'; s.fire('input');
}

/* ---- keyboard, reset, resize ---- */
keyU('4'); uok(ST.view==='sampling','4 switches to the sampling view');
keyU('1'); uok(ST.view==='field','1 comes back to the field');
{ chipU('lau','3').fire('click'); const before=ST.lau;
  keyU('r');
  uok(ST.lau===DEFAULTS.lau&&before===3,'r resets the view’s controls to their defaults');
  uok(curField(ST).landed.length>0,'and rebuilds its field with data in it');
}
{ /* every slider at min, max and mid on every tab, then every chip */
  let ctlErrU=null;
  try{
    for(let t=0;t<6;t++){ tabU(t);
      const inputs=NODESU.panel.querySelectorAll('input');
      for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
        const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
        for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
      pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
      RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===19,'the panel has its 5 sliders and 14 checkboxes ('+inputs.length+')');
    for(const g of NODESU.panel.children){ const cws=g.querySelectorAll('.chips');
      for(const cw of cws) for(const ch of cw.children) if(!ch.disabled) ch.fire('click'); }
    uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
    for(const f of (WINHU.resize||[])) f();
    uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ ctlErrU=e; }
  uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
}
/* and every tab still draws cleanly after all of that */
for(let i=0;i<6;i++){ RECU=makeRecU(); tabU(i); assertCleanU(RECU,'after the whole drive, tab '+i);
  uok(RECU.ops.length>15,'tab '+i+' still draws ('+RECU.ops.length+' ops)'); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
