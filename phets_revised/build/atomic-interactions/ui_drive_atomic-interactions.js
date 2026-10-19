
/* ====== UI drive test for atomic-interactions.html ======================= *
 * DOM-stub pattern; the stub, the recorder and the finders are taken verbatim
 * from build/coulombs-law/ui_drive_cl.js (lineage build/gravity-force-lab,
 * projects/simulations/build_buoy).  This sim has ONE pointer interaction —
 * dragging the movable atom along the r axis of the two-atoms view — and one
 * clock, which is off unless something releases the atom, so every view must
 * paint NOTHING while idle and every action must move the picture through the
 * frame loop from a proven-idle baseline.                                    *
 *                                                                            *
 * The three sim-specific thresholds the PLAYBOOK warns about are: the chip
 * rows are found by arity (7 pairs, 3 force modes), the panel has 9 groups,
 * and the input count is 9 (five sliders, four checkboxes).                  */
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
        else if(want==='.chips'&&ch.className==='chips') out.push(ch);
        else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
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
function checkU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
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
function labG(){ return labGeo(RECU,1400,820,labSpec(buildModel())); }

/* the geometry of the two-atoms view, rebuilt the way the sim rebuilds it */
function geomA(){ return atomsGeom(RECU,1400,820,buildModel()); }
/* every string the panel would show a reader: no entity may survive into one,
   because h() appends child strings as TEXT nodes and a browser then draws
   "PhET&rsquo;s" literally (the canvas rule, applied to the panel) */
function panelText(){
  const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'||ch.tagName==='BUTTON'||ch.tagName==='H3'||ch.tagName==='SPAN')
      out.push(ch.textContent||'');
    walk(ch); } };
  walk(NODESU.panel); walk(NODESU.tabs); return out;
}

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built ('+NODESU.tabs.children.length+')');
uok(NODESU.panel.children.length===9,'the control panel has its nine groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').indexOf('345.718')>=0,
    'the readout prints r_min = 345.718 pm off the model');
uok((NODESU.readout.innerHTML||'').indexOf('35.800')>=0,"and PhET's eps/k_B = 35.800 K");
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').length>100,
    'the equation bar rendered, no NaN');
uok((NODESU.tag.innerHTML||'').indexOf('r = 345.7 pm')>=0,'the tag names the separation');
uok((NODESU.hint.textContent||'').indexOf('drag')>=0,'the hint says what to drag');
{ let bad=null;
  for(const t of panelText()) if(/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test(t)){ bad=t; break; }
  uok(!bad,'no panel label carries a raw entity or tag'+(bad?' ("'+bad.slice(0,50)+'")':'')); }

/* ---- every tab draws, differently, cleanly, and then idles ---- */
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=30,'tab '+i+' emits at least 30 ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
for(let i=0;i<6;i++){ NODESU.tabs.children[i].fire('click'); idleU('tab '+i+' paints nothing while idle'); }

/* ---- PhET's seven pairs ---- */
NODESU.tabs.children[0].fire('click');
{ const row=(function(){ let hit=null;
    const walk=n=>{ for(const ch of n.children||[]){
      if(ch.className==='chips'&&ch.children.length===7) hit=ch; walk(ch); } };
    walk(NODESU.panel); return hit; })();
  uok(!!row,'found the seven-pair chip row');
  const seen=new Set();
  if(row) for(let i=0;i<row.children.length;i++){
    const chip=row.children[i];
    RECU=makeRecU(); chip.fire('click');
    uok(RECU.ops.length>=30,'pair "'+chip.textContent+'" draws ('+RECU.ops.length+' ops)');
    assertCleanU(RECU,'pair '+chip.textContent);
    seen.add(sigU(RECU));
    uok(Math.abs(ST.r-rMin(pairOf(ST).sig))<1e-9,
        'choosing "'+chip.textContent+'" returns the atom to the new r_min, as PhET does');
  }
  uok(seen.size===7,'all seven pairs draw different pictures ('+seen.size+')');
  uok(chipU('adjustable',7)!==null,'the adjustable pair is one of them');
  /* the two adjustable sliders appear ONLY for the adjustable pair */
  chipU('neon-neon',7).fire('click');
  uok(NODESU.panel.children[1].hidden===true,'the diameter/strength sliders are hidden for neon');
  chipU('adjustable',7).fire('click');
  uok(NODESU.panel.children[1].hidden===false,'...and shown for the adjustable pair');
  uok(checkU('literature ε, σ instead of PhET’s').disabled===true,
      'and the literature switch is greyed out there, because epsilon and sigma ARE the sliders');
  chipU('neon-neon',7).fire('click');
  uok(checkU('literature ε, σ instead of PhET’s').disabled===false,'re-enabled off it'); }

/* ---- PhET's Forces control ---- */
{ const hid=chipU('hidden',3), tot=chipU('total force',3), comp=chipU('components',3);
  uok(hid&&tot&&comp,'found the three force-display chips, PhET’s HIDDEN/TOTAL/COMPONENTS');
  ST.r=rMin(308)+40;
  /* Neither an op count nor a stroke count works here: the hidden state's note
     is a different sentence, so it wraps to a different number of lines, which
     changes the height of the graph below it and therefore its tick count.
     Look for the arrow ITSELF — a stroked path running along the band's centre
     line, which nothing else in this view draws. */
  const G0=geomA();
  const arrows=c=>c.ops.filter(o=>o[0]==='s'&&o.length>=7&&
    Math.abs(o[2]-G0.band.cy)<0.75&&Math.abs(o[4]-G0.band.cy)<0.75&&
    Math.abs(o[3]-o[1])>2).length;
  RECU=makeRecU(); hid.fire('click');
  const nHid=arrows(RECU), tHid=textsU(RECU).join(' ');
  RECU=makeRecU(); tot.fire('click'); const nTot=arrows(RECU);
  uok(textsU(RECU).some(t=>t.indexOf('total force')>=0),'TOTAL draws one labelled arrow');
  uok(tHid.indexOf('total force')<0,'...which HIDDEN does not');
  uok(nHid===0&&nTot===1,'HIDDEN draws no arrow on the band and TOTAL draws exactly one ('
      +nHid+', '+nTot+')');
  RECU=makeRecU(); comp.fire('click');
  const tC=textsU(RECU).join(' ');
  uok(tC.indexOf('repulsive')>=0&&tC.indexOf('attractive')>=0,
      'COMPONENTS labels PhET’s two halves separately');
  uok(RECU.ops.filter(o=>o[0]==='s'&&o.length>=7&&
      Math.abs(Math.abs(o[2]-G0.band.cy)-11)<0.75&&Math.abs(o[3]-o[1])>2).length===2,
      'and draws PhET’s two arrows, eleven pixels either side of the centre line');
  hid.fire('click'); }

/* ---- the drag: the ONE pointer interaction, from a proven-idle baseline ---- */
NODESU.tabs.children[0].fire('click');
clickU('reset all');
NODESU.tabs.children[0].fire('click');
idleU('the two-atoms view idles before the drag');
{ const G=geomA(), X=G.X(ST.r), Y=G.band.cy, r0=ST.r;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y});
  uok(DRAG.what==='atom','pointer-down on the movable atom grabs it');
  /* the MOVE, not the up, is what has to repaint: pointerup calls refresh()
     unconditionally, so a test that pumps only after the up passes with the
     move handler's dirty flag deleted (the resetCam trap, on a drag) */
  pumpU(3); RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]','the loop is idle with the atom grabbed and unmoved');
  RECU=makeRecU();
  NODESU.scene.fire('pointermove',{clientX:X+120,clientY:Y});
  pumpU(3);
  const moved=geomU(RECU);
  NODESU.scene.fire('pointerup',{});
  uok(ST.r>r0+50,'dragging right increases the separation ('+fmt(r0,1)+' -> '+fmt(ST.r,1)+' pm)');
  uok(moved.length>50,'and the MOVE itself repaints through the frame loop');
  /* the discriminating test: a purely VERTICAL drag must NOT move it, because
     the separation is a one-dimensional coordinate.  A test that only checks
     "the picture changed" passes on a handler that reads the wrong axis. */
  idleU('idle again before the vertical drag');
  const r1=ST.r;
  const G2=geomA();
  NODESU.scene.fire('pointerdown',{clientX:G2.X(ST.r),clientY:G2.band.cy});
  NODESU.scene.fire('pointermove',{clientX:G2.X(ST.r),clientY:G2.band.cy+180});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(ST.r-r1)<1e-9,'a purely vertical drag leaves the separation alone');
  /* and the drag CLAMPS rather than letting the atom leave the axis */
  const G3=geomA();
  NODESU.scene.fire('pointerdown',{clientX:G3.X(ST.r),clientY:G3.band.cy});
  NODESU.scene.fire('pointermove',{clientX:G3.X(ST.r)+4000,clientY:G3.band.cy});
  NODESU.scene.fire('pointerup',{});
  /* absolute picometres, not R_HI_FAC*308: an assertion written in terms of
     the constant under test cannot see that constant move (the surviving
     "drawn r window" mutant) */
  uok(Math.abs(ST.r-985.60000000000002)<1e-9,'dragged off the end it stops at 985.6 pm');
  NODESU.scene.fire('pointerdown',{clientX:geomA().X(ST.r),clientY:G3.band.cy});
  NODESU.scene.fire('pointermove',{clientX:-4000,clientY:G3.band.cy});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(ST.r-221.75999999999999)<1e-9,'and at the other end, 221.76 pm');
  /* the pinned atom is not draggable, and the empty stage grabs nothing */
  clickU('reset all'); NODESU.tabs.children[0].fire('click');
  const G4=geomA();
  NODESU.scene.fire('pointerdown',{clientX:G4.X(0),clientY:G4.band.cy});
  uok(DRAG.what===null,'the PINNED atom does not grab');
  NODESU.scene.fire('pointerup',{});
  NODESU.scene.fire('pointerdown',{clientX:G4.band.x+3,clientY:G4.band.y+3});
  uok(DRAG.what===null,'and empty stage grabs nothing');
  NODESU.scene.fire('pointerup',{}); }
/* the other five views ignore the pointer entirely */
for(let i=1;i<6;i++){
  NODESU.tabs.children[i].fire('click');
  NODESU.scene.fire('pointerdown',{clientX:500,clientY:400});
  uok(DRAG.what===null,'view '+i+' ignores the pointer');
  NODESU.scene.fire('pointerup',{});
}
/* there is no wheel handler at all, and no view reads a zoom: test the
   CONSEQUENCE (a stored zoom appearing later), not the immediate frame */
NODESU.tabs.children[0].fire('click');
{ const before=(function(){ RECU=makeRecU(); NODESU.tabs.children[0].fire('click'); return geomU(RECU); })();
  NODESU.scene.fire('wheel',{deltaY:-600});
  NODESU.scene.fire('wheel',{deltaY:-600});
  NODESU.tabs.children[2].fire('click');
  RECU=makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(geomU(RECU)===before,'the wheel accumulates nothing: the picture is identical afterwards'); }

/* ---- the clock ---- */
clickU('reset all');
NODESU.tabs.children[2].fire('click');      /* the motion view */
uok(ST.view==='motion','on the motion view');
uok(ST.running===false,'and the clock is not running');
idleU('a paused motion view paints nothing');
{ uok(clickU('release'),'the release button exists');
  uok(ST.running===true,'and starts the clock');
  const t0=ST.t, r0=ST.r;
  RECU=makeRecU(); pumpU(20);
  uok(ST.t>t0,'pumped frames advance the clock ('+fmt(ST.t,3)+' ps)');
  uok(Math.abs(ST.r-r0)>0.2,'and move the atom');
  uok(geomU(RECU).length>50,'and repaint');
  uok(TRAIL.length===20,'exactly one trail sample per frame ('+TRAIL.length+')');
  /* the energy is conserved along the drawn trajectory, to the integrator */
  const P=pairInfo(ST), E=liveModel(ST).E, E0=ljV(rMin(P.sig)+ST.rel,P.sig,P.eps);
  uok(Math.abs(E-E0)<1e-5*Math.abs(E0),'the drawn trajectory conserves E to 1e-5');
  uok(clickU('play / pause'),'the play/pause button exists');
  uok(ST.running===false,'and stops it');
  const rStop=ST.r; pumpU(10);
  uok(ST.r===rStop,'paused, the frame loop does not move the atom');
  clickU('play / pause'); uok(ST.running===true,'and starts it again');
  /* the slow switch really slows the clock */
  clickU('release'); pumpU(10); const fast=ST.t;
  const sl=checkU('slow (PhET’s speed switch)');
  uok(!!sl,'found the slow checkbox');
  sl.checked=true; sl.fire('change');
  clickU('release'); pumpU(10);
  uok(Math.abs(ST.t/fast-0.35)<1e-9,'slow really is 0.35 of normal, absolutely');
  sl.checked=false; sl.fire('change');
  uok(clickU('return atom'),'the Return Atom button exists');
  uok(Math.abs(ST.r-rMin(308))<1e-9&&ST.v===0&&ST.running===false,
      'and puts the atom back at r_min, at rest, stopped — PhET’s resetMovableAtomPos'); }
/* grabbing the atom pauses the motion, as PhET's setMotionPaused does */
NODESU.tabs.children[0].fire('click');
clickU('release');
{ uok(ST.running===true,'running before the grab');
  const G=geomA();
  NODESU.scene.fire('pointerdown',{clientX:G.X(ST.r),clientY:G.band.cy});
  uok(ST.running===false,'grabbing the atom pauses the motion');
  NODESU.scene.fire('pointerup',{}); }

/* ---- the model switches ---- */
clickU('reset all');
NODESU.tabs.children[3].fire('click');      /* small oscillations */
{ const P0=pairInfo(ST);
  const pin=checkU('left atom pinned (PhET’s)');
  uok(!!pin&&pin.checked===true,'the left atom starts pinned, as PhET has it');
  RECU=makeRecU(); pin.checked=false; pin.fire('change');
  const P1=pairInfo(ST);
  uok(Math.abs(P1.mu-P0.mu/2)<1e-12,'unpinning halves mu for a like pair');
  uok(Math.abs(P1.period*Math.SQRT2-P0.period)<1e-12,'and shortens the period by exactly sqrt(2)');
  uok(RECU.ops.length>=30,'and the view redraws');
  pin.checked=true; pin.fire('change');
  const lit=checkU('literature ε, σ instead of PhET’s');
  uok(!!lit&&lit.checked===false,"and PhET's parameters are the default");
  RECU=makeRecU(); lit.checked=true; lit.fire('change');
  uok(Math.abs(pairInfo(ST).sig-278.9)<1e-9,'the literature switch puts sigma at 278.9 pm');
  uok(Math.abs(pairInfo(ST).epsK-35.7)<1e-9,'and eps/k_B at 35.7 K');
  uok((NODESU.readout.innerHTML||'').indexOf('Literature')>=0,'and the readout says which set is live');
  lit.checked=false; lit.fire('change');
  uok((NODESU.readout.innerHTML||'').indexOf('PhET&rsquo;s</b> &epsilon;')>=0,'and says so the other way round'); }

/* ---- every slider, and one of them proved to repaint immediately ---- */
clickU('reset all');
NODESU.tabs.children[3].fire('click');
{ const amp=sliderU('release offset A');
  uok(!!amp,'found the amplitude slider');
  idleU('the small-oscillation view idles before the slider test');
  RECU=makeRecU();
  amp.value='30'; amp.fire('input');
  uok(geomU(RECU).length>50,'moving a slider repaints at once (no waiting for a frame)');
  uok(Math.abs(ST.amp-30)<1e-9,'and the state followed it'); }
{ let ctlErrU=null;
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===9,'the panel has its nine inputs ('+inputs.length+')');
  try{
    for(let t=0;t<6;t++){
      NODESU.tabs.children[t].fire('click');
      for(const inp of inputs){
        if(inp.disabled) continue;
        if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); }
        else for(const f of [0,0.25,0.5,0.75,1]){
          inp.value=String(parseFloat(inp.min)+f*(parseFloat(inp.max)-parseFloat(inp.min)));
          inp.fire('input');
          RECU=makeRecU(); NODESU.tabs.children[t].fire('click');
          assertCleanU(RECU,'view '+t+' with '+inp.value);
        }
      }
    }
  }catch(e){ ctlErrU=e; }
  uok(!ctlErrU,'every control drives every view without throwing'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
  uok(NODESU.errbox.style.display!=='block','and none of them put an error on screen'); }

/* PhET's slider snapping survives the UI path, not just the model path */
clickU('reset all');
chipU('adjustable',7).fire('click');
{ const sg=sliderU('atom diameter σ'), ep=sliderU('interaction ε');
  uok(!!sg&&!!ep,'found the two adjustable sliders');
  sg.value='333'; sg.fire('input');
  uok(ST.adjSig===335,"the diameter snaps to PhET's 5 pm through the UI ("+ST.adjSig+')');
  ep.value='227'; ep.fire('input');
  uok(ST.adjEps===225,'and the strength does too ('+ST.adjEps+')');
  uok(Math.abs(ST.r-rMin(335))<1e-9,'and the atom sits at the new minimum'); }

/* ---- keyboard, resize, reset ---- */
clickU('reset all');
{ let keyErrU=null;
  try{ for(let i=1;i<=6;i++){ keyU(String(i)); uok(ST.view===TABS[i-1][0],'key '+i+' selects '+TABS[i-1][1]); } }
  catch(e){ keyErrU=e; }
  uok(!keyErrU,'the number keys run'+(keyErrU?': '+keyErrU:''));
  keyU('2');
  const run0=ST.running; keyU(' ');
  uok(ST.running===!run0,'space toggles the clock');
  keyU(' ');
  keyU('r');
  uok(ST.running===true&&Math.abs(ST.r-(rMin(308)+ST.rel))<1e-9,'r releases the atom');
  keyU('x'); uok(NODESU.errbox.style.display!=='block','an unbound key does nothing'); }
{ let rsErrU=null;
  try{ for(const f of (WINHU.resize||[])) f({}); }catch(e){ rsErrU=e; }
  uok(!rsErrU,'the resize handler runs'+(rsErrU?': '+rsErrU:''));
  uok(NODESU.errbox.style.display!=='block','still no error after resize'); }
{ /* reset must restore EVERY kind of state the button claims to: the pair, the
     switches, the sliders, the separation AND the clock (a reset test that
     leaves one of them alone passes with that one deleted) */
  chipU('argon-argon',7).fire('click');
  const pin=checkU('left atom pinned (PhET’s)'); pin.checked=false; pin.fire('change');
  const lit=checkU('literature ε, σ instead of PhET’s'); lit.checked=true; lit.fire('change');
  NODESU.tabs.children[2].fire('click');
  sliderU('release at r_min +').value='60'; sliderU('release at r_min +').fire('input');
  clickU('release'); pumpU(12);
  uok(ST.pair==='ArAr'&&ST.pinned===false&&ST.lit===true&&ST.t>0&&TRAIL.length>0,
      'the state really was disturbed before the reset');
  clickU('reset all');
  uok(ST.pair==='NeNe'&&ST.pinned===true&&ST.lit===false,'reset restores the pair and the switches');
  uok(Math.abs(ST.r-rMin(308))<1e-9&&ST.v===0,'and the separation and the speed');
  uok(ST.t===0&&TRAIL.length===0&&ST.running===false,'and the clock and its trail');
  uok(ST.rel===DEFAULTS.rel&&ST.amp===DEFAULTS.amp,'and every slider');
  uok(checkU('left atom pinned (PhET’s)').checked===true,'and the checkbox in the panel followed'); }

/* ---- every view x every pair, after a clean reset ---- */
{ let swErr=null;
  try{
    const row=(function(){ let hit=null;
      const walk=n=>{ for(const ch of n.children||[]){
        if(ch.className==='chips'&&ch.children.length===7) hit=ch; walk(ch); } };
      walk(NODESU.panel); return hit; })();
    for(let t=0;t<6;t++){
      NODESU.tabs.children[t].fire('click');
      for(let i=0;i<row.children.length;i++){
        row.children[i].fire('click');
        RECU=makeRecU(); NODESU.tabs.children[t].fire('click');
        uok(RECU.ops.length>=30,'view '+t+' x pair '+i+' draws ('+RECU.ops.length+' ops)');
        assertCleanU(RECU,'view '+t+' x pair '+i);
        uok(NODESU.errbox.style.display!=='block','view '+t+' x pair '+i+' without error');
      }
    }
  }catch(e){ swErr=e; }
  uok(!swErr,'the view x pair sweep completes'+(swErr?': '+(swErr.stack||swErr):'')); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
