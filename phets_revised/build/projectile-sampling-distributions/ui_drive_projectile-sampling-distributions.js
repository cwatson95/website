
/* ====== UI drive test for projectile-sampling-distributions.html ========= *
 * DOM-stub pattern (lineage: build_buoy/ui_drive_bu.js, via the data lab
 * remake).  The one canvas drag is the launcher barrel, which scrubs through
 * the six mystery launchers, and it must move the picture THROUGH the frame
 * loop from a proven-idle baseline (time paused, loop drained, idle frame
 * drew nothing).  Chip rows are found by their data-key, never by a label:
 * four of them are labelled 1..6 and a match-by-word finder would drive the
 * wrong one. */
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
function pauseU(){ const cb=findLabelledU('time runs'); if(cb&&cb.checked){ cb.checked=false; cb.fire('change'); } }
function playU(){ const cb=findLabelledU('time runs'); if(cb&&!cb.checked){ cb.checked=true; cb.fire('change'); } }
/* the launcher's pivot, recomputed the way the sim does */
function pivotU(){
  const M=buildModel();
  const ph=M.view==='field'?fieldCaptionS(M,'1.00'):parentCaption(M);
  const L=labStage(RECU,1400,820,ph.full,ph.short,
    {histFrac:M.view==='field'?0.52:0.56,fieldWant:fieldWantH(M)});
  const map=fieldMap(L.field,M);
  return {x:map.X(0),y:map.Y(M.cfg.h)};
}

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.panel.children.length>=9,'the control panel has its groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(/3\.1811 m/.test(NODESU.readout.innerHTML),'the readout prints launcher 1’s exact σ, 3.1811 m');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');
uok(NODESU.hint.textContent.length>10,'the hint line is set');

/* ---- every tab draws, differently, cleanly ---- */
/* floors at ~75 % of what each tab emits at its defaults (measured: 85, 147,
   425, 109 ops).  Derived from what this file emits, not copied from another
   sim's harness — an op-count floor borrowed from a busier sim punishes a
   view for being efficient (polyhedra Known-bad). */
const FLOORSU=[63,110,318,81];
const sigsU={};
for(let i=0;i<4;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');

/* ---- the sampling screen ---- */
tabU(0); pauseU();
{ const F=curField(ST);
  uok(F.samples.length>0,'the sampling field opens with samples in it');
  uok(F.samples[0].xs.length===ST.pN,'each sample holds n launches');
  uok(F.landed.length===ST.pN,'and the field shows the last one');
  const before=F.samples.length;
  clickU('+20 samples');
  uok(curField(ST).samples.length===before+20,'+20 samples adds twenty');
  const M=buildModel();
  uok(Math.abs(M.mstat.mean-pdlMean(M.means))<1e-12,'the readout’s mean of the sample means is that mean');
  uok(Math.abs(M.mstat.sd1-pdlSd(M.means,1))<1e-12,'and their spread is the n−1 standard deviation of them');
  clickU('clear');
  uok(curField(ST).samples.length===0,'clear empties the field');
  RECU=makeRecU(); tabU(0);
  uok(NODESU.readout.innerHTML.indexOf('0 of 200')>=0,'the readout says so');
  assertCleanU(RECU,'the empty sampling field');
  clickU('+20 samples');
}
{ /* starting a sample by hand clears the last one off the field — the path
     only fireField takes, so it must be tested with shots ALREADY there */
  const F=curField(ST); clickU('+20 samples'); playU();
  uok(F.landed.length===ST.pN,'the field is showing the last sample’s '+ST.pN+' shots');
  keyU(' ');
  uok(F.landed.length===0&&F.air.length===0,'space starts a new one and clears them');
  keyU(' '); F.firing=false; pauseU(); }
{ /* a sample fires one projectile at a time and only then records its mean */
  const F=curField(ST); fieldClear(F); playU();
  keyU(' '); uok(F.firing===true,'space starts a sample');
  pumpU(4); uok(F.air.length+F.landed.length>=1,'the first projectile of it is away');
  uok(F.air.length+F.landed.length<=2,'and ONLY the first: a new sample starts from an empty field');
  uok(F.samples.length===0,'and no mean is recorded until the sample is complete');
  RECU=makeRecU(); pumpU(1); const a=geomU(RECU); RECU=makeRecU(); pumpU(1); const b=geomU(RECU);
  uok(a.length>50&&b.length>50&&a!==b,'while it flies, two frames draw DIFFERENT pictures');
  for(let i=0;i<1200&&G_samples(F)===0;i++) pumpU(1);
  uok(F.samples.length===1,'when the last of the n lands, one mean is recorded');
  uok(Math.abs(F.samples[0].mean-pdlMean(F.samples[0].xs))<1e-12,'and it is the mean of that sample');
  uok(F.landed.length===ST.pN,'the field keeps the sample that made it');
  pauseU(); idleU('and the loop goes quiet again');
}
function G_samples(F){ return F.samples.length; }
{ /* continuous sampling runs until it is stopped */
  const F=curField(ST); fieldClear(F);
  chipU('mode','continuous').fire('click');
  playU(); keyU(' ');
  uok(F.firing===true,'continuous: space starts it');
  for(let i=0;i<2400&&F.samples.length<3;i++) pumpU(1);
  uok(F.samples.length>=3,'and it keeps going: '+F.samples.length+' samples');
  uok(F.landed.length+F.air.length<=ST.pN,'each new sample clears the last one’s shots off the field ('
      +(F.landed.length+F.air.length)+' of at most '+ST.pN+')');
  keyU(' '); uok(F.firing===false,'space again stops it');
  chipU('mode','single').fire('click'); pauseU();
}
{ const F=curField(ST);
  chipU('pN','n = 40').fire('click');
  uok(ST.pN===40,'n = 40 selected');
  uok(curField(ST).size===40,'and its own field is the n = 40 one');
  uok(curField(ST)!==F,'which is a DIFFERENT field from the n = 5 one, as PhET keeps them');
  const M=buildModel(), se40=M.exact.sd/Math.sqrt(40);
  uok(NODESU.readout.innerHTML.indexOf(fmt(se40,4)+' m')>=0,'the readout prints σ/√40 = '+fmt(se40,4)+' m');
  chipU('pN','n = 2').fire('click');
  const se2=buildModel().exact.sd/Math.sqrt(2);
  uok(Math.abs(se2/se40-Math.sqrt(20))<1e-12,'σ/√2 over σ/√40 is exactly √20');
  chipU('pN','n = 5').fire('click');
}
{ const M0=buildModel();
  chipU('pLau','6').fire('click');
  const E6=pdlExact(cfgMystery(6));
  uok(Math.abs(buildModel().exact.sd-E6.sd)<1e-12,'the launcher chip moves the exact law with it');
  uok(NODESU.readout.innerHTML.indexOf(fmt(E6.sd,4)+' m')>=0,'and the readout shows launcher 6’s σ = '+fmt(E6.sd,4)+' m');
  uok(E6.sd>M0.exact.sd*2,'… which is more than twice launcher 1’s');
  chipU('pLau','1').fire('click');
}
{ /* the histogram controls */
  chipU('binW','2 m').fire('click');
  uok(buildModel().binW===2,'the 2 m bin width is selected');
  const H=pdlHistogram(buildModel().means,2);
  let s=0; for(const c of H.counts) s+=c;
  uok(s===buildModel().mstat.n,'and every sample mean is still in a bin');
  chipU('binW','0.5 m').fire('click');
  uok(buildModel().binW===PDL.BINW_DEF,'0.5 m is PhET’s default for this sim');
  uok(chipU('binW','10 m')===null,'and there is no 10 m chip — that is the data lab’s');
  clickU('+20 samples');       /* the continuous test left the field nearly empty */
  const z=chipU('zoom','0–25'); uok(!!z,'found the vertical-scale chips'); z.fire('click');
  uok(z.disabled!==true,'they are live on the screen that uses them');
  uok(buildModel().zoomMax===25,'the scale chip sets the histogram ceiling');
  chipU('zoom','0–50').fire('click');
  const cb=findLabelledU('blocks, one per sample');
  RECU=makeRecU(); tabU(0); const bars=sigU(RECU);
  cb.checked=true; cb.fire('change');
  RECU=makeRecU(); tabU(0);
  uok(sigU(RECU)!==bars,'blocks and bars are different drawings');
  cb.checked=false; cb.fire('change');
  const se=findLabelledU('σ/√n and the measured spread');
  RECU=makeRecU(); tabU(0); const withSe=sigU(RECU);
  se.checked=false; se.fire('change');
  RECU=makeRecU(); tabU(0);
  uok(sigU(RECU)!==withSe,'the standard-error checkbox changes the picture');
  se.checked=true; se.fire('change');
}

/* ---- the launcher drag, the one thing on the canvas ---- */
tabU(0); pauseU(); idleU('the sampling view idles while paused');
{ const p=pivotU(), l0=ST.pLau;
  NODESU.scene.fire('pointerdown',{clientX:p.x,clientY:p.y-8});
  uok(DRAG.what==='launcher','pointer-down on the barrel grabs it');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:p.x,clientY:p.y-8-3*14,buttons:1});
  uok(ST.pLau===l0+3,'dragging up three notches steps three launchers on ('+ST.pLau+')');
  uok(DRAG.start===l0,'and it counts from the launcher it started on');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'the drag repaints THROUGH the frame loop (the dirty flag)');
  idleU('and the loop goes idle again');
  NODESU.scene.fire('pointermove',{clientX:p.x,clientY:p.y-8+9*14,buttons:1});
  uok(ST.pLau===1,'dragging far down clamps at launcher 1');
  NODESU.scene.fire('pointermove',{clientX:p.x,clientY:p.y-8-40*14,buttons:1});
  uok(ST.pLau===6,'and far up clamps at 6');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(NODESU.readout.innerHTML.indexOf('mystery launcher 6')>=0,'the readout followed the drag');
  chipU('pLau','1').fire('click');
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:p.x+200,clientY:p.y-8});
  uok(DRAG.what===null,'a pointer-down 200 px down the field grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties');
  NODESU.scene.fire('pointerup',{});
}

/* ---- the four sample sizes ---- */
tabU(1);
{ const M=buildModel();
  uok(M.sets.length===4,'four sets are built');
  M.sets.forEach(S=>uok(S.means.length===ST.sM,'n = '+S.n+': '+ST.sM+' samples'));
  /* the widths really do fall as 1/sqrt(n) */
  const a=M.sets[0].stat.sd1, d=M.sets[3].stat.sd1;
  uok(a/d>3&&a/d<6,'the n = 2 spread is '+fmt(a/d,2)+'× the n = 40 one (√20 = 4.47)');
  const s=sliderU('samples at each n'); uok(!!s,'found the samples slider');
  s.value='200'; s.fire('input');
  uok(buildModel().sets[0].means.length===200,'the slider rebuilds the experiment');
  s.value='60'; s.fire('input');
  chipU('sLau','5').fire('click');
  uok(Math.abs(buildModel().exact.sd-pdlExact(cfgMystery(5)).sd)<1e-12,'the launcher chip moves it');
  chipU('sLau','1').fire('click');
  /* a live control that is ignored is worse than no control: the vertical
     scale belongs to the sampling screen and nothing else reads it */
  uok(chipU('zoom','0–25').disabled===true,'the vertical-scale chips are DEAD on the four-sizes view');
  const cb=findLabelledU('σ/√n, the theorem');
  RECU=makeRecU(); tabU(1); const before=sigU(RECU);
  cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(1);
  uok(sigU(RECU)!==before,'the theorem curves can be switched off');
  cb.checked=true; cb.fire('change');
}

/* ---- one launch ---- */
tabU(2);
{ const M=buildModel();
  uok(M.stat.n===ST.xN,'the parent view draws the number of launches its slider asks for');
  const s=sliderU('launches drawn'); s.value='500'; s.fire('input');
  uok(buildModel().stat.n===500,'moving that slider redraws the sample');
  s.value='300'; s.fire('input');
  const E=buildModel().exact;
  uok(Math.abs(buildModel().stat.mean-E.mean)<4*E.sd/Math.sqrt(300),
      '300 launches average within 4 σ/√n of the exact mean');
  chipU('xLau','6').fire('click');
  uok(Math.abs(buildModel().exact.sd-pdlExact(cfgMystery(6)).sd)<1e-12,'the launcher chip moves the parent');
  chipU('xLau','1').fire('click');
  const cb=findLabelledU('the exact density');
  RECU=makeRecU(); tabU(2); const before=sigU(RECU);
  cb.checked=false; cb.fire('change');
  RECU=makeRecU(); tabU(2);
  uok(sigU(RECU)!==before,'the density can be switched off');
  cb.checked=true; cb.fire('change');
  /* the parent view fires single launches, not samples */
  const F=curField(ST); fieldClear(F); playU();
  keyU(' '); pumpU(3);
  uok(F.air.length+F.landed.length===1,'space launches ONE projectile here');
  for(let i=0;i<400&&F.air.length;i++) pumpU(1);
  uok(F.landed.length===1,'and it lands');
  uok(F.samples.length===0,'no sample is recorded on this view');
  pauseU(); clickU('+50 launches');
  uok(curField(ST).landed.length===51,'+50 launches adds fifty at once');
  uok(buttonU('+50 launches')!==null,'the +50 button is here on the parent view');
  keyU('c'); uok(curField(ST).landed.length===0,'c clears them');
  const s2=sliderU('launches drawn'); s2.value='300'; s2.fire('input');
}

/* ---- the limit theorem ---- */
tabU(3);
{ const M=buildModel();
  uok(M.sets.length===4,'the limit-theorem view builds four sample sizes');
  M.sets.forEach(S=>{
    const want=M.exact.sd/Math.sqrt(S.n);
    const tol=want*Math.sqrt((M.exact.kurt/S.n+2)/(4*ST.cM));
    uok(Math.abs(S.sd-want)<5*tol,'n = '+S.n+': the measured SE '+fmt(S.sd,4)+' is within 5 sampling sd of σ/√n = '+fmt(want,4));
  });
  const s=sliderU('samples at each n '); uok(!!s,'found this view’s own samples slider');
  s.value='200'; s.fire('input');
  uok(buildModel().sets[0].means.length===200,'it rebuilds the experiment');
  s.value='400'; s.fire('input');
  chipU('cLau','4').fire('click');
  uok(Math.abs(buildModel().exact.mean-pdlExact(cfgMystery(4)).mean)<1e-12,'and the launcher chip moves it');
  chipU('cLau','1').fire('click');
  uok(buttonU('+20 samples')===null||chipsU('pLau').parentEl.hidden===true,'the sampling group is hidden here');
  tabU(0);
  { /* a control that is live but ignored is worse than no control: +50
       launches means nothing on a screen whose datum is a whole sample */
    let row=null;
    const walk=n=>{ for(const ch of n.children||[]){
      if(ch.tagName==='BUTTON'&&(ch.textContent||'')==='+50 launches') row=ch.parentEl; walk(ch); } };
    walk(NODESU.panel);
    uok(!!row&&row.hidden===true,'the +50-launches row is hidden on the sampling screen');
    tabU(2);
    uok(row.hidden===false,'and shown on the parent view'); }
  tabU(3);
}

/* ---- a slider must repaint AT ONCE ---- */
tabU(2); pauseU(); idleU('idle before the slider repaint test');
{ const s=sliderU('launches drawn'); RECU=makeRecU();
  s.value='150'; s.fire('input');
  uok(ST.xN===150,'the launches slider sets 150');
  uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)');
  s.value='300'; s.fire('input');
}

/* ---- keyboard, reset, resize, the whole control sweep ---- */
keyU('4'); uok(ST.view==='clt','4 switches to the limit theorem');
keyU('1'); uok(ST.view==='field','1 comes back to the field');
playU();   /* from a known state, or "p pauses" is asserting whatever ran last */
keyU('p'); uok(ST.running===false,'p pauses'); keyU('p'); uok(ST.running===true,'p runs again');
{ chipU('pLau','3').fire('click');
  keyU('r');
  uok(ST.pLau===DEFAULTS.pLau,'r resets the view’s controls to their defaults');
  uok(curField(ST).samples.length>0,'and rebuilds its field with samples in it');
}
{ let ctlErrU=null;
  try{
    for(let t=0;t<4;t++){ tabU(t);
      const inputs=NODESU.panel.querySelectorAll('input');
      for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
        const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
        for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
      pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
      RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===12,'the panel has its 3 sliders and 9 checkboxes ('+inputs.length+')');
    for(const g of NODESU.panel.children){ const cws=g.querySelectorAll('.chips');
      for(const cw of cws) for(const ch of cw.children) if(!ch.disabled) ch.fire('click'); }
    uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
    for(const f of (WINHU.resize||[])) f();
    uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ ctlErrU=e; }
  uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
}
for(let i=0;i<4;i++){ RECU=makeRecU(); tabU(i); assertCleanU(RECU,'after the whole drive, tab '+i);
  uok(RECU.ops.length>15,'tab '+i+' still draws ('+RECU.ops.length+' ops)'); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
