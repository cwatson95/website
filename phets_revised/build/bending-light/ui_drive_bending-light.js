
/* ============ UI drive test for bending-light.html ======================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/molecule-polarity).
 * The three sim-specific thresholds: the chip rows are found by arity AND
 * position (media 7 x 4 rows, prisms 5, polarisation 3 x 2 rows, bow order 2);
 * the panel has 8 groups; 24 inputs (11 sliders, 13 checkboxes).  Every drag
 * and the wave clock are tested THROUGH the frame loop from a proven-idle
 * baseline, and each asserts that the drawing MOVED -- exercising an
 * interaction is not testing it (Known-bad).                                 */
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
    clip:P, fillRect(x,y,w,h){ops.push(['r',Math.round(x),Math.round(y),Math.round(w),Math.round(h)]);},
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
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},
      clientX:0,clientY:0,pointerId:1,buttons:1,deltaY:0},ev||{})); },
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
function settleU(max){ let quiet=0, n=0; while(quiet<3&&n<(max||4000)){ RECU=makeRecU(); pumpU(1); n++; quiet=RECU.ops.length?0:quiet+1; } return n; }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function checkU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipsU(arity){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='chips'&&ch.children.length===arity) out.push(ch); walk(ch); } };
  walk(NODESU.panel); return out; }
/* match the WHOLE label and the row's arity: a substring finder hits the wrong
   control, and four of these rows carry the same seven names (Known-bad) */
function chipIn(row,label){ for(const c of row.children) if(c.textContent===label) return c; return null; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function tabIndex(k){ return TABS.findIndex(t=>t[0]===k); }
function dragU(x0,y0,x1,y1){ NODESU.scene.fire('pointerdown',{clientX:x0,clientY:y0});
  NODESU.scene.fire('pointermove',{clientX:x1,clientY:y1}); NODESU.scene.fire('pointerup',{}); }
/* the down and the move ONLY: the pointerup handler calls refresh(), which
   draws unconditionally, so a repaint measured after a whole drag cannot tell
   whether the MOVE marked the loop dirty (the resetCam Known-bad, one handler
   further on).  The repaint has to be measured between the move and the up. */
function dragHoldU(x0,y0,x1,y1){ NODESU.scene.fire('pointerdown',{clientX:x0,clientY:y0});
  NODESU.scene.fire('pointermove',{clientX:x1,clientY:y1}); }
function dropU(){ NODESU.scene.fire('pointerup',{}); }
function forceDrawU(){ RECU=makeRecU(); tabU(tabIndex(ST.view)); return geomU(RECU); }
function idleProofU(label){ settleU(); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+': the loop is idle first'); }
function animOff(){ ST.anim=false; const cb=checkU('run the clock'); if(cb&&cb.checked){ cb.checked=false; cb.fire('change'); } }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===TABS.length,TABS.length+' view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')===TABS.map(t=>t[1]).join('|'),
    'the tabs are lower-case noun phrases: '+NODESU.tabs.children.map(b=>b.textContent).join(', '));
const NGROUPS=8, NINPUTS=24;
uok(NODESU.panel.children.length===NGROUPS,'the control panel has its '+NGROUPS+' groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>40,'the equation bar rendered');
{ const credit=NODESU.panel.children[NGROUPS-2].textContent;
  uok(/Remake of PhET Interactive Simulations/.test(credit)&&/CC-BY 4\.0/.test(credit),'the credit line is on the panel');
  uok(/build 1\.2\.5/.test(credit),'and it names the PhET build every constant came from');
  uok(/CIE 1931/.test(credit),'and where the colours came from'); }
{ const media=chipsU(7);
  uok(media.length===4,'the four seven-substance chip rows are there ('+media.length+')');
  uok(chipsU(5).length===1,'and the five prism prototypes');
  uok(chipsU(3).length===2,'and the two three-way polarisation rows');
  uok(chipsU(2).length===1,'and the two bow orders'); }

/* ---- the default state is PhET's ---- */
uok(ST.angDeg===45,'the sim opens at PhET’s 45 degrees of incidence');
uok(ST.topSub==='air'&&ST.botSub==='water','with air over water, as PhET’s Intro screen does');
uok(ST.envSub==='air'&&ST.prismSub==='glass','and air around glass on the prism screen');
uok(ST.lamNm===650,'and the laser at PhET’s reference 650 nm');

/* ---- every tab draws, and draws something different ---- */
{ animOff();
  const sigs=[];
  for(let i=0;i<TABS.length;i++){
    RECU=makeRecU(); tabU(i);
    uok(RECU.ops.length>15,'tab '+i+' ('+TABS[i][1]+') drew content ('+RECU.ops.length+' ops)');
    uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
    assertCleanU(RECU,'tab '+i);
    uok((NODESU.readout.innerHTML||'').length>200,'tab '+i+' rendered a readout');
    uok(!/NaN|undefined/.test(NODESU.readout.innerHTML+NODESU.eqbar.innerHTML+NODESU.tag.innerHTML),
        'tab '+i+' readout, eqbar and tag are clean');
    sigs.push(geomU(RECU));
  }
  uok(new Set(sigs).size===TABS.length,'every tab draws a different picture ('+new Set(sigs).size+'/'+TABS.length+')');
}

/* ---- dragging the laser must MOVE the geometry, through the frame loop ---- */
for(const v of ['bound','wave']){
  keyU('r'); animOff(); tabU(tabIndex(v));
  idleProofU('the laser drag in "'+v+'"');
  const before=forceDrawU(), a0=ST.angDeg;
  /* the laser body is registered in PICKS by the last draw; grab it there */
  const pick=PICKS.filter(p=>p.kind==='laser')[0];
  uok(!!pick,'the last draw registered the laser as draggable in "'+v+'"');
  if(pick){
    /* forceDrawU() is a tab click, and setView sets dirty itself: the next
       pumped frame would repaint whatever the move did (the resetCam
       Known-bad).  Drain it and prove idleness again before acting. */
    idleProofU('after the baseline draw in "'+v+'"');
    dragHoldU(pick.x,pick.y,pick.x+180,pick.y+40);
    RECU=makeRecU(); pumpU(3);
    uok(geomU(RECU).length>50,'the MOVE marks the frame loop dirty in "'+v+'"');
    dropU();
    uok(Math.abs(ST.angDeg-a0)>1,'and the angle of incidence really changed ('+a0+' -> '+ST.angDeg+')');
    const after=forceDrawU();
    uok(after!==before&&after.length>50,'and the drawing followed in "'+v+'"');
  }
}
/* the drag is clamped into PhET's range rather than running past it */
{ keyU('r'); animOff(); tabU(tabIndex('bound'));
  const pick=PICKS.filter(p=>p.kind==='laser')[0];
  if(pick){ dragU(pick.x,pick.y,pick.x+4000,pick.y+4000);
    uok(ST.angDeg>=0&&ST.angDeg<=89.9,'a wild drag still leaves the angle in [0, 89.9] ('+ST.angDeg+')'); }
  keyU('r');
}
/* dragging the beam in the prism view moves the beam, not the angle */
{ keyU('r'); animOff(); tabU(tabIndex('prism'));
  idleProofU('the beam drag');
  const before=forceDrawU(), y0=ST.beamY, a0=ST.angDeg;
  const pick=PICKS.filter(p=>p.kind==='beam')[0];
  uok(!!pick,'the prism view registers its laser as draggable');
  if(pick){
    idleProofU('after the baseline draw in the prism view');
    dragHoldU(pick.x,pick.y,pick.x,pick.y-120);
    RECU=makeRecU(); pumpU(3);
    uok(geomU(RECU).length>50,'the MOVE marks the frame loop dirty in the prism view');
    dropU();
    const y1=ST.beamY;
    uok(Math.abs(y1-y0)>0.5,'the beam height changed ('+y0+' -> '+y1+')');
    uok(ST.angDeg===a0,'and the boundary angle did not');
    uok(forceDrawU()!==before,'and the drawing followed');
    /* it must FOLLOW the pointer, not merely differ from the default: a
       mutant that pins it to a constant passes a one-position test */
    const p2=PICKS.filter(p=>p.kind==='beam')[0];
    dragU(p2.x,p2.y,p2.x,p2.y+200);
    uok(Math.abs(ST.beamY-y1)>0.5,'a second drag moves it again ('+y1+' -> '+ST.beamY+')');
    uok(ST.beamY<y1,'and downward on the canvas means downward in the world');
  }
  keyU('r');
}
/* the dragging state is what lets a captured pointer keep dragging after the
   button reading goes to zero; without it the move handler returns early */
{ keyU('r'); animOff(); tabU(tabIndex('bound'));
  const pick=PICKS.filter(p=>p.kind==='laser')[0];
  const a0=ST.angDeg;
  NODESU.scene.fire('pointermove',{clientX:pick.x+150,clientY:pick.y+40,buttons:0});
  uok(ST.angDeg===a0,'a hover with no button pressed changes nothing');
  NODESU.scene.fire('pointerdown',{clientX:pick.x,clientY:pick.y});
  uok(NODESU.scene.classList.contains('dragging'),'pointerdown puts the canvas in the dragging state');
  NODESU.scene.fire('pointermove',{clientX:pick.x+150,clientY:pick.y+40,buttons:0});
  uok(Math.abs(ST.angDeg-a0)>1,'and then a captured move DOES swing the laser ('+ST.angDeg+')');
  dropU();
  uok(!NODESU.scene.classList.contains('dragging'),'and pointerup leaves that state');
  keyU('r'); animOff();
}
/* a view that ignores the pointer must really ignore it -- test the
   CONSEQUENCE, not the immediate frame (Known-bad) */
{ keyU('r'); animOff(); tabU(tabIndex('fres'));
  const a0=ST.angDeg, before=forceDrawU();
  dragU(300,300,600,420);
  uok(ST.angDeg===a0,'a drag on the plot views changes nothing');
  uok(forceDrawU()===before,'and the picture is identical');
}

/* ---- the wave clock runs, and stops ---- */
{ keyU('r'); tabU(tabIndex('wave'));
  const cb=checkU('run the clock');
  uok(!!cb,'found the wave clock checkbox');
  uok(cb.checked,'and it starts on, as PhET’s wave view does');
  const ph0=ST.phase;
  RECU=makeRecU(); pumpU(4);
  uok(geomU(RECU).length>50,'with the clock on the loop repaints every frame');
  uok(ST.phase!==ph0,'and the phase advanced ('+ph0+' -> '+ST.phase+')');
  const p1=ST.phase; pumpU(3);
  uok(ST.phase!==p1,'and keeps advancing');
  cb.checked=false; cb.fire('change');
  settleU(); RECU=makeRecU(); pumpU(4);
  uok(geomU(RECU)==='[]','with the clock off the loop paints nothing');
  const p2=ST.phase; pumpU(4);
  uok(ST.phase===p2,'and the phase is frozen');
  /* the clock only runs on the wave view */
  cb.checked=true; cb.fire('change'); tabU(tabIndex('bound'));
  const p3=ST.phase; settleU(); pumpU(6);
  uok(ST.phase===p3,'the clock does not run on the other views');
  keyU('r'); animOff();
}
/* the phase really changes the picture */
{ tabU(tabIndex('wave')); animOff();
  const a=forceDrawU(); ST.phase=PI; clearMemo();
  const b=forceDrawU();
  uok(a!==b,'moving the clock forward half a cycle redraws the field');
  ST.phase=0; clearMemo(); keyU('r'); animOff();
}
/* a slider must repaint, from a proven-idle baseline */
{ tabU(tabIndex('bound')); animOff(); idleProofU('the angle slider');
  const inp=sliderU('angle of incidence');
  uok(!!inp,'found the angle-of-incidence slider');
  RECU=makeRecU(); inp.value='70'; inp.fire('input');
  uok(RECU.ops.length>10,'driving it repaints immediately ('+RECU.ops.length+' ops)');
  uok(Math.abs(ST.angDeg-70)<1e-9,'and sets the angle to 70 degrees');
}
/* total internal reflection really removes the transmitted ray */
{ keyU('r'); animOff(); tabU(tabIndex('bound'));
  const media=chipsU(7);
  chipIn(media[0],'water').fire('click');          /* above = water */
  chipIn(media[1],'air').fire('click');            /* below = air   */
  const inp=sliderU('angle of incidence');
  inp.value='30'; inp.fire('input');
  const M1=buildModel(ST);
  uok(isFinite(M1.b.th2),'water over air at 30 degrees still transmits');
  const before=forceDrawU();
  inp.value='70'; inp.fire('input');
  const M2=buildModel(ST);
  uok(!isFinite(M2.b.th2)&&M2.b.tir,'at 70 degrees it is past the critical angle');
  uok(M2.b.R===1,'and the whole beam comes back (R = 1 exactly)');
  uok(forceDrawU()!==before,'and the picture changed');
  uok(/otal internal reflection/.test(NODESU.readout.innerHTML),'the readout says so');
  keyU('r'); animOff();
}
/* a mystery substance refuses to print its index */
{ tabU(tabIndex('bound'));
  const media=chipsU(7);
  chipIn(media[1],'Mystery A').fire('click');
  uok(/Mystery A or B/.test(NODESU.readout.innerHTML),'a mystery medium hides its index in the readout');
  uok(!/2\.419/.test(NODESU.readout.innerHTML),'and does not leak the number anywhere in it');
  chipIn(media[1],'water').fire('click');
  uok(/1\.333/.test(NODESU.readout.innerHTML),'while an ordinary one prints it');
  keyU('r'); animOff();
}
/* the custom-index slider appears only when custom is chosen */
{ tabU(tabIndex('bound'));
  const media=chipsU(7);
  const before=sliderU('custom n below');
  uok(!!before,'the custom-index slider exists');
  chipIn(media[1],'custom').fire('click');
  uok(ST.botSub==='custom','choosing custom sets the substance');
  before.value='2.0'; before.fire('input');
  uok(Math.abs(ST.botN-2.0)<1e-9,'and the slider sets the index');
  uok(Math.abs(buildModel(ST).b.n2-indexOf(2.0,650))<1e-12,'which the model uses');
  keyU('r'); animOff();
}
/* the prism chips all trace */
{ tabU(tabIndex('prism'));
  const row=chipsU(5)[0];
  for(const c of row.children){
    RECU=makeRecU(); c.fire('click');
    uok(RECU.ops.length>6,'prism "'+c.textContent+'" draws ('+RECU.ops.length+' ops)');
    assertCleanU(RECU,'prism '+c.textContent);
    const P=buildModel(ST).prism;
    uok(P.bundles[0].tr.segs.length>=2,'and traces at least two segments for '+c.textContent);
    uok(P.bundles[0].tr.steps<=PHET.maxSteps,'and stops inside PhET’s step limit for '+c.textContent);
  }
  keyU('r'); animOff();
}
/* white light really fans out */
{ tabU(tabIndex('prism'));
  const single=buildModel(ST).prism.bundles.length;
  const cb=checkU('white light'); uok(!!cb,'found the white-light checkbox');
  cb.checked=true; cb.fire('change');
  const white=buildModel(ST).prism.bundles.length;
  uok(white===single*WHITE_WL.length,'white light traces '+WHITE_WL.length+' wavelengths ('+white+')');
  const cb2=checkU('five rays (PhET’s fan)'); uok(!!cb2,'found the five-ray checkbox');
  cb2.checked=true; cb2.fire('change');
  uok(buildModel(ST).prism.bundles.length===white*5,'and PhET’s fan multiplies that by five');
  keyU('r'); animOff();
}
/* the partial reflections really add segments */
{ tabU(tabIndex('prism'));
  const n0=buildModel(ST).prism.bundles[0].tr.segs.length;
  const cb=checkU('partial reflections'); uok(!!cb,'found the partial-reflections checkbox');
  cb.checked=true; cb.fire('change');
  const n1=buildModel(ST).prism.bundles[0].tr.segs.length;
  uok(n1>n0,'switching the partial reflections on adds branches ('+n0+' -> '+n1+')');
  keyU('r'); animOff();
}
/* the bow order chips change the bow */
{ tabU(tabIndex('bow'));
  const row=chipsU(2)[0];
  const a1=buildModel(ST).bow.angStar;
  chipIn(row,'2 (secondary)').fire('click');
  uok(ST.bowK===2,'the secondary chip sets k = 2');
  const a2=buildModel(ST).bow.angStar;
  uok(Math.abs(a2-50.79)<0.1,'and the bow radius becomes 50.79 degrees ('+a2+')');
  uok(Math.abs(a1-42.13)<0.1,'while the primary was 42.13 ('+a1+')');
  chipIn(row,'1 (primary)').fire('click');
  uok(ST.bowK===1,'and back again');
  keyU('r'); animOff();
}

/* ---- every control can be driven, in every view ---- */
{ let err=null;
  try{
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===NINPUTS,'the panel has its '+NINPUTS+' inputs ('+inputs.length+')');
    let nSlide=0,nCheck=0;
    for(const inp of inputs){
      if(inp.type==='checkbox'){ nCheck++; inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      nSlide++;
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); }
    }
    uok(nSlide===11&&nCheck===13,'11 sliders and 13 checkboxes ('+nSlide+'/'+nCheck+')');
    for(let v=0;v<TABS.length;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v);
      uok(NODESU.errbox.style.display!=='block','tab '+v+' survived the control sweep');
      animOff(); settleU(200); }
    for(const f of (WINHU.resize||[])) f();
    uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ err=e; }
  uok(!err,'control sweep completes'+(err?': '+(err.stack||err):''));
  keyU('r'); animOff();
}
/* ---- every chip in every row, in every view ---- */
{ let err=null;
  try{
    for(let v=0;v<TABS.length;v++){
      tabU(v); animOff();
      for(const cw of chipsU(7).concat(chipsU(5)).concat(chipsU(3)).concat(chipsU(2)))
        for(const c of cw.children){
          RECU=makeRecU(); c.fire('click');
          uok(NODESU.errbox.style.display!=='block','chip "'+c.textContent+'" in tab '+v+' raised no error');
        }
      keyU('r'); animOff();
    }
  }catch(e){ err=e; }
  uok(!err,'every chip clicks in every view'+(err?': '+(err.stack||err):''));
}

/* ---- keyboard ---- */
{ let err=null;
  try{ keyU('r'); animOff();
    for(let i=1;i<=TABS.length;i++){ keyU(String(i)); uok(ST.view===TABS[i-1][0],'key '+i+' shows '+TABS[i-1][1]); }
    const a0=ST.anim; keyU(' ');
    uok(ST.anim!==a0,'space toggles the wave clock');
    keyU(' '); uok(ST.anim===a0,'and back again');
  }catch(e){ err=e; }
  uok(!err,'keyboard shortcuts run'+(err?': '+(err.stack||err):''));
}

/* ---- reset all, against disturbed state of every kind ---- */
{ keyU('r'); tabU(tabIndex('prism'));
  ST.angDeg=12; ST.lamNm=402; ST.topSub='diamond'; ST.botSub='mysteryB'; ST.white=true;
  ST.pol='p'; ST.prismId='circle'; ST.prismSub='water'; ST.prismRot=95; ST.beamY=-4;
  ST.beamTilt=22; ST.manyRays=true; ST.showReflections=true; ST.bowK=2; ST.bowPol='s';
  ST.showNormal=false; ST.paintField=false; ST.phase=2.2; ST.anim=false;
  uok(clickU('reset all'),'found reset all');
  uok(ST.angDeg===45&&ST.lamNm===650,'reset all restores PhET’s angle and wavelength');
  uok(ST.topSub==='air'&&ST.botSub==='water'&&ST.pol==='s','and the media and the polarisation');
  uok(ST.prismId==='triangle'&&ST.prismSub==='glass'&&ST.prismRot===0,'and the prism');
  uok(ST.manyRays===false&&ST.showReflections===false&&ST.white===false,'and the ray options');
  uok(ST.bowK===1&&ST.bowPol==='unpol','and the rainbow');
  uok(ST.showNormal===true&&ST.paintField===true&&ST.anim===true,'and the drawing switches');
  uok(ST.view==='prism','keeping the view');
  animOff();
}
/* ---- the readout of every view x medium pair stays clean ---- */
{ let bad=null;
  const media=chipsU(7);
  for(let v=0;v<TABS.length;v++){ tabU(v); animOff();
    for(const top of ['air','water','glass','diamond','Mystery A','custom'])
      for(const bot of ['air','water','diamond','Mystery B']){
        chipIn(media[0],top).fire('click'); chipIn(media[1],bot).fire('click');
        if(/NaN|undefined|Infinity/.test(NODESU.readout.innerHTML+NODESU.eqbar.innerHTML))
          bad=bad||(TABS[v][0]+'/'+top+'/'+bot);
      } }
  uok(!bad,'no view or medium pair puts NaN in the panels ('+(bad||'ok')+')');
  keyU('r'); animOff();
}
/* ---- the info and physics blocks are filled for every view ---- */
{ const info=NODESU.panel.querySelector('#info'), phys=NODESU.panel.querySelector('#phys');
  uok(!!info&&!!phys,'the info and physics blocks exist');
  for(let v=0;v<TABS.length;v++){
    tabU(v); animOff();
    uok((info.innerHTML||'').length>300,'view '+TABS[v][1]+' has an info paragraph');
    uok((phys.innerHTML||'').length>300,'view '+TABS[v][1]+' has a physics derivation');
    uok(!/NaN|undefined/.test(info.innerHTML+phys.innerHTML),'and both are clean for '+TABS[v][1]);
  }
  keyU('r'); animOff();
}

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
