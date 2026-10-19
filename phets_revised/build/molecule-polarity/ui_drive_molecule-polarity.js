
/* ============ UI drive test for molecule-polarity.html ===================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/molecule-shapes).
 * The three sim-specific thresholds: the chip rows are found by arity AND
 * label (surface 3, colour 2, field mode 2, molecules 19, real mode 2,
 * dipole direction 2); the panel has 11 groups; 13 inputs (7 sliders, 6
 * checkboxes).  Every drag, the wheel, the field animation and the bond-angle
 * drag are tested THROUGH the frame loop from a proven-idle baseline, and each
 * asserts that the drawing MOVED -- exercising an interaction is not testing
 * it (Known-bad).                                                            */
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
function chipU(label,arity){ for(const cw of chipsU(arity)) for(const c of cw.children) if(c.textContent===label) return c; return null; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function tabIndex(k){ return TABS.findIndex(t=>t[0]===k); }
function dragU(x0,y0,x1,y1){ NODESU.scene.fire('pointerdown',{clientX:x0,clientY:y0});
  NODESU.scene.fire('pointermove',{clientX:x1,clientY:y1}); NODESU.scene.fire('pointerup',{}); }
function forceDrawU(){ RECU=makeRecU(); tabU(tabIndex(ST.view)); return geomU(RECU); }
function idleProofU(label){ settleU(); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+': the loop is idle first'); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===TABS.length,TABS.length+' view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')===TABS.map(t=>t[1]).join('|'),
    'the tabs are lower-case noun phrases: '+NODESU.tabs.children.map(b=>b.textContent).join(', '));
const NGROUPS=11, NINPUTS=13;
uok(NODESU.panel.children.length===NGROUPS,'the control panel has its '+NGROUPS+' groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>40,'the equation bar rendered');
{ const credit=NODESU.panel.children[NGROUPS-2].textContent;
  uok(/Remake of PhET Interactive Simulations/.test(credit)&&/CC-BY 4\.0/.test(credit),'the credit line is on the panel');
  uok(/CCCBDB/.test(credit),'and it names where the measured numbers came from'); }
{ RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','with the field off an idle frame paints nothing'); }

/* ---- every tab draws, and draws something different ---- */
{ const sigs=[];
  for(let i=0;i<TABS.length;i++){
    RECU=makeRecU(); tabU(i);
    uok(RECU.ops.length>20,'tab '+i+' ('+TABS[i][1]+') drew content ('+RECU.ops.length+' ops)');
    uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
    assertCleanU(RECU,'tab '+i);
    uok((NODESU.readout.innerHTML||'').length>200,'tab '+i+' rendered a readout');
    uok(!/NaN|undefined/.test(NODESU.readout.innerHTML+NODESU.eqbar.innerHTML+NODESU.tag.innerHTML),'tab '+i+' readout, eqbar and tag are clean');
    sigs.push(geomU(RECU));
  }
  uok(new Set(sigs).size===TABS.length,'every tab draws a different picture ('+new Set(sigs).size+'/'+TABS.length+')');
}

/* ---- drag must MOVE the geometry, through the frame loop, one axis at a time ---- */
tabU(tabIndex('two'));
for(const [nm,dx,dy] of [['horizontal',260,0],['vertical',0,190]]){
  keyU('r'); clickU('reset all'); tabU(tabIndex('two'));
  idleProofU('two atoms, '+nm+' drag');
  const before=forceDrawU();
  const ang0=ST.molAngle;
  dragU(200,200,200+dx,200+dy);
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'a '+nm+' drag marks the frame loop dirty');
  const after=forceDrawU();
  uok(after!==before&&after.length>50,'and the '+nm+' drag moved the molecule');
  uok(Math.abs(ST.molAngle-ang0)>1e-3,'the molecule angle really changed ('+ang0+' -> '+ST.molAngle+')');
}
/* the wheel: resetCam() sets dirty itself, so drain it and prove idleness first */
{ clickU('reset all'); tabU(tabIndex('two')); keyU('r'); idleProofU('the wheel test');
  const z0=ST.zoom;
  RECU=makeRecU(); NODESU.scene.fire('wheel',{deltaY:-500}); pumpU(3);
  uok(geomU(RECU).length>50,'the wheel marks the frame loop dirty');
  uok(ST.zoom>z0,'and the wheel zoomed in ('+z0+' -> '+ST.zoom+')');
  const zoomed=forceDrawU();
  ST.zoom=z0; const plain2=forceDrawU();
  uok(zoomed!==plain2,'the zoomed picture differs from the un-zoomed one');
}
/* the three-atoms drag on atom A changes the BOND ANGLE, not the molecule angle */
{ clickU('reset all'); tabU(tabIndex('three')); idleProofU('the bond-angle drag');
  const M=buildModel(), before=forceDrawU(), a0=Math.abs(normAngle(ST.angAB-ST.angBC,-PI));
  /* atom A is up-left of the centre at PhET's 150 deg with +y DOWN, so it is
     down-left on the canvas; grab it where the last draw put it */
  const pickA=PICKS.filter(p=>p.kind==='A')[0];
  uok(!!pickA,'the last draw registered atom A as draggable');
  if(pickA){
    dragU(pickA.x,pickA.y,pickA.x+70,pickA.y-70);
    const a1=Math.abs(normAngle(ST.angAB-ST.angBC,-PI));
    uok(Math.abs(a1-a0)>1e-3,'dragging atom A changed the bond angle ('+(a0*180/PI)+' -> '+(a1*180/PI)+' deg)');
    const after=forceDrawU();
    uok(after!==before,'and the drawing followed');
  }
}
/* the REAL view is the only one with a camera: a drag there must move it, and
   each axis separately (Known-bad: theta-frozen and phi-frozen both survived a
   sweep that only ever dragged a view with no camera in it) */
{ for(const [nm,dx,dy,key] of [['horizontal',240,0,'camTheta'],['vertical',0,170,'camPhi']]){
    clickU('reset all'); tabU(tabIndex('real')); keyU('r'); idleProofU('real molecules, '+nm+' drag');
    const before=forceDrawU(), v0=ST[key];
    dragU(210,210,210+dx,210+dy);
    RECU=makeRecU(); pumpU(3);
    uok(geomU(RECU).length>50,'a '+nm+' drag on the molecule marks the loop dirty');
    const after=forceDrawU();
    uok(after!==before&&after.length>50,'and the '+nm+' drag turned the molecule');
    uok(Math.abs(ST[key]-v0)>1e-4,'ST.'+key+' really changed ('+v0+' -> '+ST[key]+')');
  }
  clickU('reset all');
}
/* PhET's sliders snap to 0.2: an off-grid value must be constrained, not kept */
{ clickU('reset all'); tabU(tabIndex('three'));
  for(const [lab2,key] of [['atom A','enA'],['atom B','enB'],['atom C','enC']]){
    const inp=sliderU(lab2); uok(!!inp,'found the "'+lab2+'" slider');
    if(!inp) continue;
    inp.value='3.31'; inp.fire('input');
    uok(Math.abs(ST[key]-3.4)<1e-12,lab2+': 3.31 snapped to PhET\'s 0.2 grid (got '+ST[key]+')');
    inp.value='2.09'; inp.fire('input');
    uok(Math.abs(ST[key]-2.0)<1e-12,lab2+': 2.09 snapped down to 2.0 (got '+ST[key]+')');
  }
  clickU('reset all');
}

/* the vector-sum view: a drag on the top panel sets the bond angle */
{ clickU('reset all'); tabU(tabIndex('sum')); idleProofU('the sum drag');
  const a0=Math.abs(normAngle(ST.angAB-ST.angBC,-PI));
  dragU(500,200,700,200);
  const a1=Math.abs(normAngle(ST.angAB-ST.angBC,-PI));
  uok(Math.abs(a1-a0)>1e-3,'dragging the sum panel set the bond angle ('+(a1*180/PI).toFixed(1)+' deg)');
}
/* the field view: a drag sets the starting angle */
{ clickU('reset all'); tabU(tabIndex('field')); idleProofU('the field drag');
  const p0=ST.psi0; dragU(500,200,500,320);
  uok(Math.abs(ST.psi0-p0)>1,'dragging the field panel set the starting angle ('+p0+' -> '+ST.psi0+')');
}

/* ---- the field animation really turns the molecule, then stops ---- */
{ clickU('reset all'); tabU(tabIndex('two'));
  const enB=sliderU('atom B'); uok(!!enB,'found the atom-B electronegativity slider');
  if(enB){ enB.value='4'; enB.fire('input'); }
  const cb=checkU('electric field on'); uok(!!cb,'found the electric-field checkbox');
  uok(!cb.checked,'and PhET starts with the field off');
  const rotor=chipU('damped rotor',2); uok(!!rotor,'found the damped-rotor chip');
  if(rotor) rotor.fire('click');
  clickU('turn the molecule 150°');
  const psiStart=fieldPsi();
  uok(Math.abs(psiStart-150*PI/180)<1e-9,'the molecule starts 150 deg from alignment');
  cb.checked=true; cb.fire('change');
  const before=forceDrawU();
  RECU=makeRecU(); pumpU(5);
  uok(geomU(RECU).length>50,'with the field on the frame loop repaints');
  const n=settleU(20000);
  uok(n<20000,'the rotor settles in '+n+' frames');
  uok(FIELD.idle,'and the model says it is aligned');
  uok(Math.abs(fieldPsi())<1e-5,'with the dipole pointing at the positive plate ('+fieldPsi()+')');
  uok(forceDrawU()!==before,'the picture moved');
  /* PhET's own rule reaches the same place */
  clickU('turn the molecule 150°');
  const phet=chipU('PhET’s rule',2); uok(!!phet,'found the PhET-rule chip');
  if(phet) phet.fire('click');
  const n2=settleU(20000);
  uok(n2<20000&&FIELD.idle,'PhET\'s rule also settles ('+n2+' frames)');
  uok(Math.abs(fieldPsi())<1e-12,'and lands exactly on alignment');
  cb.checked=false; cb.fire('change');
}
/* a molecule with no dipole never turns, however long the field is on */
{ clickU('reset all'); tabU(tabIndex('two'));
  const a=sliderU('atom A'), b=sliderU('atom B');
  a.value='3'; a.fire('input'); b.value='3'; b.fire('input');
  const cb=checkU('electric field on'); cb.checked=true; cb.fire('change');
  const ang0=ST.molAngle; settleU(400);
  uok(ST.molAngle===ang0,'with no dipole the field never turns the molecule');
  cb.checked=false; cb.fire('change'); clickU('reset all');
}

/* ---- every control can be driven, in every view ---- */
{ let err=null;
  try{
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===NINPUTS,'the panel has its '+NINPUTS+' inputs ('+inputs.length+')');
    for(const inp of inputs){
      if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); }
    }
    for(let v=0;v<TABS.length;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v); settleU(6000); }
    for(const f of (WINHU.resize||[])) f();
    uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ err=e; }
  uok(!err,'control sweep completes'+(err?': '+(err.stack||err):''));
}
/* ---- every chip in every row, in every view ---- */
{ let err=null;
  try{
    clickU('reset all');
    for(let v=0;v<TABS.length;v++){
      tabU(v);
      for(const cw of chipsU(2).concat(chipsU(3))) for(const c of cw.children){
        RECU=makeRecU(); c.fire('click');
        uok(NODESU.errbox.style.display!=='block','chip "'+c.textContent+'" in tab '+v+' raised no error');
      }
    }
  }catch(e){ err=e; }
  uok(!err,'every preset chip clicks'+(err?': '+(err.stack||err):''));
  clickU('reset all');
}
/* ---- the nineteen molecules, in every view ---- */
{ let err=null;
  try{
    const rows=chipsU(19);
    uok(rows.length===1,'found the 19-molecule chip row');
    const row=rows[0];
    for(let v=0;v<TABS.length;v++){
      tabU(v);
      for(let i=0;i<row.children.length;i+=3){
        const chip=row.children[i];
        RECU=makeRecU(); chip.fire('click');
        uok(RECU.ops.length>=2,'view '+v+' draws something for '+chip.textContent);
        assertCleanU(RECU,'view '+v+', '+chip.textContent);
        uok(NODESU.errbox.style.display!=='block','and does not error for '+chip.textContent);
      }
    }
    /* every molecule, on the view that is about them */
    tabU(tabIndex('real'));
    for(const chip of row.children) for(const mode of ['basic','advanced']){
      chip.fire('click');
      const mc=chipU(mode,2); if(mc) mc.fire('click');
      RECU=makeRecU(); tabU(tabIndex('real'));
      uok(RECU.ops.length>20,chip.textContent+' ('+mode+') draws ('+RECU.ops.length+' ops)');
      assertCleanU(RECU,chip.textContent+' '+mode);
    }
  }catch(e){ err=e; }
  uok(!err,'every molecule in every view runs'+(err?': '+(err.stack||err):''));
}

/* ---- keyboard ---- */
{ let err=null;
  try{ clickU('reset all');
    for(const k of ['1','2','3','4','5','6','r',' ']) keyU(k);
    uok(ST.field===true,'space toggles the electric field on');
    keyU(' '); uok(ST.field===false,'and off again');
    for(let i=1;i<=TABS.length;i++){ keyU(String(i)); uok(ST.view===TABS[i-1][0],'key '+i+' shows '+TABS[i-1][1]); }
  }catch(e){ err=e; }
  uok(!err,'keyboard shortcuts run'+(err?': '+(err.stack||err):''));
}

/* ---- reset all, against disturbed state of every kind ---- */
{ clickU('reset all'); tabU(tabIndex('real'));
  ST.enA=3.6; ST.enB=2.2; ST.enC=4; ST.mol='CHCl3'; ST.realMode='advanced'; ST.surface='potential';
  ST.surfColor='roygb'; ST.field=true; ST.zeta=2.4; ST.fieldE=1.9; ST.dipoleDir='negpos';
  ST.camTheta=0.3; ST.camPhi=-0.9; ST.zoom=2; ST.psi0=-40; setBondAngleDeg(37);
  uok(clickU('reset all'),'found reset all');
  uok(ST.enA===DEFAULTS.enA&&ST.enB===DEFAULTS.enB&&ST.enC===DEFAULTS.enC,'reset all restores PhET\'s electronegativities');
  uok(ST.mol===DEFAULTS.mol&&ST.realMode==='basic'&&ST.surface==='none'&&ST.surfColor==='rwb','and the molecule, the mode and the surface');
  uok(ST.field===false&&ST.zeta===DEFAULTS.zeta&&ST.fieldE===DEFAULTS.fieldE&&ST.dipoleDir==='posneg','and the field and the preference');
  uok(Math.abs(Math.abs(normAngle(ST.angAB-ST.angBC,-PI))*180/PI-120)<1e-9,'and PhET\'s 120 deg opening angle');
  uok(ST.camTheta===DEFAULTS.camTheta&&ST.camPhi===DEFAULTS.camPhi&&ST.zoom===1,'and the camera');
  uok(ST.view==='real','keeping the view');
  settleU();
}
/* ---- the readout of every view x molecule x mode stays clean ---- */
{ let bad=null;
  for(let v=0;v<TABS.length;v++){ tabU(v);
    for(const m of ['H2O','CO2','BH3','CHCl3']) for(const mode of ['basic','advanced']){
      ST.mol=m; ST.realMode=mode;
      const chip=chipU(m,19); if(chip) chip.fire('click');
      if(/NaN|undefined|Infinity/.test(NODESU.readout.innerHTML)) bad=bad||(TABS[v][0]+'/'+m+'/'+mode);
    } }
  uok(!bad,'no view, molecule or mode puts NaN in the readout ('+(bad||'ok')+')');
  clickU('reset all');
}

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
