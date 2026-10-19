
/* ============ UI drive test for molecule-shapes.html ======================= *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build/wave-on-a-string).
 * The three sim-specific thresholds: the chip rows are found by exact label AND
 * arity (the molecule list, real/model); the panel has 9 groups; 6 inputs (the
 * rho slider and 5 checkboxes).  Every drag, the wheel and a slider are tested
 * THROUGH the frame loop from a proven-idle baseline; every reset against a
 * sentinel.  Shared with molecule-shapes-basics through VARIANT.              */
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
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:1,deltaY:0},ev||{})); },
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
/* pump until three frames in a row draw nothing (or give up after max) */
function settleU(max){ let quiet=0, n=0; while(quiet<3&&n<(max||4000)){ RECU=makeRecU(); pumpU(1); n++; quiet=RECU.ops.length?0:quiet+1; } return n; }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
function sliderU(label){ let hit=null;   /* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity) for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function tabIndex(k){ return TABS.findIndex(t=>t[0]===k); }
function dragU(x0,y0,x1,y1){ NODESU.scene.fire('pointerdown',{clientX:x0,clientY:y0}); NODESU.scene.fire('pointermove',{clientX:x1,clientY:y1}); NODESU.scene.fire('pointerup',{}); }
function idleProofU(label){ settleU(); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+': the loop is idle first'); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===TABS.length,TABS.length+' view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')===TABS.map(t=>t[1]).join('|'),'the tabs are lower-case noun phrases: '+NODESU.tabs.children.map(b=>b.textContent).join(', '));
const NGROUPS=VARIANT==='basics'?8:9, NINPUTS=VARIANT==='basics'?2:6;
uok(NODESU.panel.children.length===NGROUPS,'the control panel has its '+NGROUPS+' groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>40,'the equation bar rendered');
uok(/Remake of PhET Interactive Simulations/.test(NODESU.panel.children[NGROUPS-2].textContent)&&/CC-BY 4\.0/.test(NODESU.panel.children[NGROUPS-2].textContent),'the credit line is on the panel');

/* ---- the opening molecule relaxes, then the loop goes quiet ---- */
{ const n=settleU(); uok(n<1500,'PhET\'s opening two bonds settle in '+n+' frames'); uok(!LIVE.anim,'and the flow stops');
  uok(Math.abs(angleDeg(LIVE.groups[0].u,LIVE.groups[1].u)-180)<1e-9,'into a straight line'); }
{ RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','with nothing moving an idle frame paints nothing'); }

/* ---- every tab draws, and draws something different ---- */
const sigsU=new Set();
for(let i=0;i<TABS.length;i++){ RECU=makeRecU(); tabU(i);
  /* floor 15: the smallest honest picture, PhET's two-bond opening molecule, is 23 ops */
  uok(RECU.ops.length>15,'tab '+i+' ('+TABS[i][1]+') drew content ('+RECU.ops.length+' ops)');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i); sigsU.add(geomU(RECU)); settleU(); }
uok(sigsU.size===TABS.length,'every tab draws a different picture ('+sigsU.size+'/'+TABS.length+')');
tabU(0); settleU();

/* ---- the orbit: each axis alone, two real drawings through the frame loop ---- */
for(const [nm,dx,dy] of [['horizontal',220,0],['vertical',0,150]]){
  RECU=makeRecU(); keyU('r'); const base=geomU(RECU);   /* reset first: phi is clamped at +-1.45 */
  uok(base.length>100,nm+': the reset repaints at once');
  idleProofU(nm+' drag');
  /* the down and the move are pumped SEPARATELY: each has to mark the frame dirty
     on its own, or one masks the other (pointer-up calls refresh, which draws) */
  NODESU.scene.fire('pointerdown',{clientX:40,clientY:640});
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>100,nm+': a pointer-down repaints through the loop');
  idleProofU(nm+' after the down');
  NODESU.scene.fire('pointermove',{clientX:40+dx,clientY:640+dy});
  RECU=makeRecU(); pumpU(1); const after=geomU(RECU);
  uok(after.length>100,nm+': the move alone repaints through the loop');
  uok(after!==base,'a purely '+nm+' drag moves the drawing');
  NODESU.scene.fire('pointerup',{});
}
{ keyU('r'); settleU(); const t0=ST.camTheta, p0=ST.camPhi; dragU(40,640,140,640); uok(ST.camTheta!==t0&&ST.camPhi===p0,'horizontal turns theta only');
  dragU(40,640,40,700); uok(ST.camPhi!==p0,'vertical turns phi'); keyU('r'); uok(ST.camTheta===DEFAULTS.camTheta&&ST.camPhi===DEFAULTS.camPhi,'r resets the camera'); }

/* ---- the wheel, from a proven-quiet baseline (resetCam re-arms dirty) ---- */
{ RECU=makeRecU(); keyU('r'); const base=geomU(RECU); idleProofU('wheel');
  NODESU.scene.fire('wheel',{deltaY:-400}); RECU=makeRecU(); pumpU(1); const g=geomU(RECU);
  uok(g.length>100,'the wheel repaints through the loop'); uok(g!==base,'and the zoomed picture differs'); uok(ST.zoom>1,'zoom went up'); keyU('r'); uok(ST.zoom===1,'r resets the zoom'); settleU(); }

/* ---- dragging a pair: grab, move, the drawing moves; let go, it slides back ---- */
{ keyU('r'); settleU(); RECU=makeRecU(); tabU(0); settleU();
  const p=PICK.find(q=>LIVE.groups[q.i].order>0); uok(!!p,'a bond atom is on the pick list');
  const base=(()=>{ RECU=makeRecU(); S_draw(); return geomU(RECU); })();   /* the baseline BEFORE the idle proof: a tab click re-arms dirty */
  idleProofU('pair drag');
  const u0=LIVE.groups[p.i].u.slice();
  NODESU.scene.fire('pointerdown',{clientX:p.x,clientY:p.y}); uok(LIVE.held===p.i,'pointer-down on the atom grabs it');
  NODESU.scene.fire('pointermove',{clientX:p.x+70,clientY:p.y-50});
  RECU=makeRecU(); pumpU(1); const g=geomU(RECU);
  uok(g.length>100&&g!==base,'the pair drag moves the drawing through the loop');
  uok(angleDeg(u0,LIVE.groups[p.i].u)>4,'the atom follows the pointer ('+fmt(angleDeg(u0,LIVE.groups[p.i].u),1)+'°)');
  NODESU.scene.fire('pointerup',{}); uok(LIVE.held===-1,'pointer-up lets go');
  const n=settleU(); uok(n>5,'it slides back over '+n+' frames');
  uok(Math.abs(angleDeg(LIVE.groups[0].u,LIVE.groups[1].u)-180)<1e-8,'to the straight line'); }
function S_draw(){ tabU(tabIndex('model')); }

/* ---- the bonding buttons (PhET's add, remove-last, remove all, six at most) ---- */
{ tabU(tabIndex('model')); settleU();
  uok(clickU('+ single')&&LIVE.groups.length===3,'+ single adds a bond');
  RECU=makeRecU(); pumpU(1); uok(RECU.ops.length>15,'and the flow repaints'); settleU();
  const a=LIVE.groups.map(g=>g.u); uok(Math.abs(angleDeg(a[0],a[1])-120)<1e-8,'three bonds settle at 120°');
  uok(clickU('+ double')&&clickU('+ triple'),'+ double, + triple');
  if(HAS_LP){ uok(clickU('+ lone pair'),'+ lone pair'); } else uok(clickU('+ single'),'+ single');
  uok(clickU('+ single')&&LIVE.groups.length===6,'six pairs'); uok(buttonU('+ single').disabled&&buttonU('+ triple').disabled,'every add button is disabled at six (PhET)');
  clickU('+ single'); uok(LIVE.groups.length===6,'a seventh does nothing'); settleU();
  uok(!buttonU('− double').disabled,'− double is live'); uok(clickU('− double')&&!LIVE.groups.some(g=>g.order===2),'− double takes the double bond off');
  uok(buttonU('− double').disabled,'and is disabled with none left');
  if(HAS_LP){ const box=findLabelledU('show lone pairs'); box.checked=false; box.fire('change'); uok(!ST.showLP,'lone pairs hidden');
    uok(buttonU('+ lone pair').disabled,'+ lone pair is dead while they are hidden (PhET)'); box.checked=true; box.fire('change'); }
  uok(clickU('remove all')&&LIVE.groups.length===0,'remove all'); uok(buttonU('remove all').disabled,'remove all is then disabled');
  settleU(); RECU=makeRecU(); tabU(tabIndex('model')); assertCleanU(RECU,'the empty model');
  uok(textU(RECU).indexOf('no pairs')>=0,'the empty view says why it is empty');
  clickU('+ single'); clickU('+ single'); settleU(); }

/* ---- a button whose action starts no motion must still repaint at once ----
   (the adding buttons hide this: they set the flow going, so the loop redraws anyway) */
{ tabU(tabIndex('model')); settleU(); dragU(40,640,150,660); settleU();
  const t0=ST.camTheta; RECU=makeRecU(); uok(clickU('reset view'),'found reset view');
  uok(RECU.ops.length>15,'the reset-view button repaints at once ('+RECU.ops.length+' ops)');
  uok(ST.camTheta===DEFAULTS.camTheta&&ST.camTheta!==t0,'and puts the camera back'); settleU(); }

/* ---- the rho slider: repaint from proven idle, and the molecule re-relaxes ---- */
if(HAS_LP){ tabU(tabIndex('model')); clickU('+ lone pair'); clickU('+ lone pair'); settleU();
  const sl=sliderU('lone-pair radius ρ'); uok(!!sl,'the rho slider');
  idleProofU('rho slider'); sl.value='1'; RECU=makeRecU(); sl.fire('input');
  uok(RECU.ops.length>15,'moving rho repaints at once'); uok(ST.rho===1,'rho = 1');
  settleU(); const b=LIVE.groups.filter(g=>g.order>0).map(g=>g.u);
  uok(Math.abs(angleDeg(b[0],b[1])-TET)<1e-8,'at rho = 1 water-like AX₂E₂ opens to the tetrahedral angle');
  sl.value='0.7'; sl.fire('input'); settleU(); const b2=LIVE.groups.filter(g=>g.order>0).map(g=>g.u);
  uok(Math.abs(angleDeg(b2[0],b2[1])-namedAngle('AX2E2',0.7))<1e-8,'and back to 105.07° at 0.70');
  for(const v of [sl.min,sl.max,'0.85']){ sl.value=String(v); sl.fire('input'); uok(NODESU.errbox.style.display!=='block','rho '+v+' without error'); }
  sl.value='0.7'; sl.fire('input'); settleU(); }

/* ---- the checkboxes: angles and the names reach the canvas ---- */
{ tabU(tabIndex('model')); settleU();
  const cb=findLabelledU('show bond angles'); uok(!!cb,'show bond angles');
  RECU=makeRecU(); cb.checked=true; cb.fire('change'); uok(/°/.test(textU(RECU)),'the angles appear on the canvas'); cb.checked=false; cb.fire('change');
  const mn=findLabelledU('molecule geometry'); RECU=makeRecU(); mn.checked=true; mn.fire('change'); uok(/molecule geometry: /.test(textU(RECU)),'the molecule geometry name appears');
  mn.checked=false; mn.fire('change');
  if(HAS_LP){ const en=findLabelledU('electron geometry'); RECU=makeRecU(); en.checked=true; en.fire('change'); uok(/electron geometry: /.test(textU(RECU)),'the electron geometry name appears'); en.checked=false; en.fire('change'); }
  settleU(); }

/* ---- real molecules: every chip, the Real / Model blend through the loop ---- */
{ tabU(tabIndex('real')); settleU();
  let n=0; for(const id of MOL_LIST){ const c=chipU(formulaText(id),MOL_LIST.length); if(!c) continue; RECU=makeRecU(); c.fire('click'); n++;
    uok(ST.mol===id,'chip '+id+' selects it'); uok(RECU.ops.length>15,id+' draws ('+RECU.ops.length+' ops)'); assertCleanU(RECU,id); }
  uok(n===MOL_LIST.length,'all '+MOL_LIST.length+' molecule chips found ('+n+')');
  if(HAS_LP){ chipU(formulaText('H2O'),MOL_LIST.length).fire('click'); settleU();
    idleProofU('real/model');
    chipU('model',2).fire('click'); uok(ST.realMode==='model','the model chip');
    const frames=settleU(); uok(frames>10,'the blend animates over '+frames+' frames'); uok(LIVE.realBlend===1,'and lands on the model');
    uok(/105\.1&deg;/.test(NODESU.readout.innerHTML)&&/104\.5&deg;/.test(NODESU.readout.innerHTML),'the readout lists measured 104.5° and model 105.1°');
    chipU('real',2).fire('click'); settleU(); uok(LIVE.realBlend===0,'the real chip blends back');
    const withLp=MOL_LIST.find(id=>REAL[id].olp>0); chipU(formulaText(withLp),MOL_LIST.length).fire('click'); settleU();
    const oc=findLabelledU('show outer lone pairs'); RECU=makeRecU(); oc.checked=true; oc.fire('change'); const withO=RECU.ops.length;
    oc.checked=false; oc.fire('change'); RECU=makeRecU(); tabU(tabIndex('real')); uok(withO>RECU.ops.length,'outer lone pairs add drawing ('+withO+' vs '+RECU.ops.length+')'); }
  settleU(); }

/* ---- the AXE table: a click builds the class; a drag turns them all ---- */
{ tabU(tabIndex('table')); settleU(); const cell=HIT.find(h=>h.x===3&&h.e===(HAS_LP?2:0))||HIT.find(h=>h.x===3);
  uok(!!cell,'the table has an AX₃ cell');
  NODESU.scene.fire('pointerdown',{clientX:cell.b.x+cell.b.w/2,clientY:cell.b.y+cell.b.h/2}); NODESU.scene.fire('pointerup',{});
  uok(ST.view==='model','a click switches to the model view'); const c=liveCounts(); uok(c.x===3&&c.e===(HAS_LP?2:0),'with the class built ('+c.x+','+c.e+')');
  uok(NODESU.tabs.children[tabIndex('model')].className==='active','and the model tab is lit');
  tabU(tabIndex('table')); settleU(); const t0=ST.camTheta; dragU(cell.b.x+4,cell.b.y+4,cell.b.x+80,cell.b.y+4);
  uok(ST.view==='table'&&ST.camTheta!==t0,'a drag on the table turns the shapes'); settleU(); }

/* ---- the squeeze: drag across the top panel sets rho, through the loop ---- */
if(HAS_LP){ tabU(tabIndex('squeeze')); settleU(); idleProofU('squeeze drag');
  const b=squeezeGeo(RECU,1400,820).top;
  NODESU.scene.fire('pointerdown',{clientX:b.x+b.w*0.5,clientY:b.y+b.h*0.5}); RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>15,'the rho drag repaints through the loop'); uok(Math.abs(ST.rho-0.85)<1e-12,'rho = 0.85 at mid-panel');
  NODESU.scene.fire('pointermove',{clientX:b.x+b.w*0.1,clientY:b.y+10}); uok(Math.abs(ST.rho-0.73)<1e-12,'dragging follows (0.73)');
  NODESU.scene.fire('pointermove',{clientX:b.x+b.w*0.37,clientY:b.y+10}); uok(Math.abs(ST.rho-0.81)<1e-12,'and snaps 0.8110 to the slider step 0.81'); NODESU.scene.fire('pointerup',{});
  uok(/ρ = 0\.81/.test(textU((()=>{ RECU=makeRecU(); tabU(tabIndex('squeeze')); return RECU; })())),'the canvas labels the new rho');
  sliderU('lone-pair radius ρ').value='0.7'; sliderU('lone-pair radius ρ').fire('input'); settleU(); }

/* ---- the relaxation: the descent runs through the loop, a new start differs ---- */
{ tabU(tabIndex('model')); clickU('remove all'); for(let k=0;k<4;k++) clickU('+ single'); if(HAS_LP){ clickU('+ lone pair'); clickU('+ lone pair'); } else { clickU('+ single'); clickU('+ single'); } settleU();
  RECU=makeRecU(); tabU(tabIndex('relax')); const first=geomU(RECU);
  RECU=makeRecU(); pumpU(1); uok(RECU.ops.length>15,'the descent animates'); uok(RELAX.step>0,'and steps');
  const n=settleU(6000); uok(RELAX.done,'the descent finishes in '+n+' frames');
  uok(/reached|stuck/.test(NODESU.readout.innerHTML+textU((()=>{ RECU=makeRecU(); tabU(tabIndex('relax')); return RECU; })())),'and says where it ended');
  const s0=RELAX.seed; RECU=makeRecU(); clickU('new random start'); uok(RELAX.seed===s0+1&&RELAX.step===0,'new random start');
  uok(geomU(RECU)!==first,'a different start is a different picture'); keyU(' '); uok(RELAX.seed===s0+2,'space starts again'); settleU(6000); }

/* ---- keyboard, resize, every control without error ---- */
keyU('1'); uok(ST.view===TABS[0][0],'1 is '+TABS[0][1]); keyU(String(TABS.length)); uok(ST.view===TABS[TABS.length-1][0],TABS.length+' is '+TABS[TABS.length-1][1]); keyU('2'); uok(ST.view===TABS[1][0],'2 is '+TABS[1][1]);
{ let err=null;
  try{ const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===NINPUTS,'the panel has its '+NINPUTS+' inputs ('+inputs.length+')');
    for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max); for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
    for(let v=0;v<TABS.length;v++){ RECU=makeRecU(); tabU(v); assertCleanU(RECU,'after the control sweep, tab '+v); settleU(6000); }
    for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ err=e; }
  uok(!err,'control sweep completes'+(err?': '+(err.stack||err):'')); }

/* ---- reset all, against disturbed state of every kind ---- */
{ tabU(tabIndex('real')); ST.mol=MOL_LIST[MOL_LIST.length-1]; ST.showAngles=true; ST.showMolName=true; ST.camTheta=0.3; ST.camPhi=-0.9; ST.zoom=2;
  if(HAS_LP){ ST.rho=0.9; ST.realMode='model'; LIVE.realBlend=1; ST.showOuterLP=true; ST.showElName=true; }
  LIVE.groups=[]; RELAX.seed=7;
  uok(clickU('reset all'),'found reset all');
  uok(ST.mol===MOL_LIST[0]&&!ST.showAngles&&!ST.showMolName&&ST.rho===RHO_PHET&&ST.realMode==='real','reset all restores PhET\'s defaults');
  uok(ST.camTheta===DEFAULTS.camTheta&&ST.camPhi===DEFAULTS.camPhi&&ST.zoom===1,'and the camera');
  uok(LIVE.groups.length===2&&LIVE.realBlend===0&&RELAX.seed===0,'and the opening molecule, the blend and the start');
  uok(ST.view==='real','keeping the view'); settleU(); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
