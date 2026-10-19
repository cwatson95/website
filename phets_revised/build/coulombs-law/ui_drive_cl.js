
/* ============ UI drive test for coulombs-law.html ========================= *
 * DOM-stub pattern (lineage: build/gravity-force-lab/ui_drive_gfl.js, from
 * projects/simulations/build_buoy).  Two scale screens with their own state,
 * each with three pointer interactions (either charge, the ruler); nothing
 * runs on a clock, so every view must paint NOTHING while idle, and every
 * action must move the picture through the frame loop from a proven-idle
 * baseline.                                                                  */
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

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.panel.children.length===6,'the control panel has its six groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').indexOf('319.6 N')>=0,'the readout prints |F| = 319.6 N off the model');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').length>100,'the equation bar rendered, no NaN');
uok((NODESU.tag.innerHTML||'').indexOf('r = 3.0 cm')>=0,'the tag names the distance');

/* ---- every tab draws, differently, cleanly, and idles ---- */
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=30,'tab '+i+' emits at least 30 ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');
for(let i=0;i<5;i++){ NODESU.tabs.children[i].fire('click'); idleU('tab '+i+' paints nothing while idle'); }

/* ---- the macro screen: the labels follow the two checkboxes ---- */
NODESU.tabs.children[0].fire('click'); uok(ST.view==='macro','on the macro scale');
{ RECU=makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(textsU(RECU).indexOf('Force on q₁ by q₂ = 319.557 N')>=0,'the macro screen draws PhET\'s decimal label');
  const sc=checkU('scientific notation'); uok(!!sc&&sc.checked===false,'scientific notation starts off on the macro screen');
  RECU=makeRecU(); sc.checked=true; sc.fire('change'); uok(ST.mSci===true,'turned on');
  uok(textsU(RECU).indexOf('Force on q₁ by q₂ = 3.20 × 10² N')>=0,'and the canvas label switches at once');
  const fv=checkU('force values'); RECU=makeRecU(); fv.checked=false; fv.fire('change'); uok(ST.mForce===false,'force values off');
  uok(textsU(RECU).indexOf('Force on q₁ by q₂')>=0&&textsU(RECU).every(t=>t.indexOf('Force on q₁ by q₂ =')<0),'the label keeps no value');
  uok(sc.disabled===true,'and scientific notation is greyed out, as PhET does');
  sc.checked=false; sc.fire('change'); uok(ST.mSci===true,'a greyed-out checkbox changes nothing');
  fv.checked=true; fv.fire('change'); uok(sc.disabled===false&&ST.mForce===true,'force values back on re-enables it');
  sc.checked=false; sc.fire('change'); uok(ST.mSci===false,'and it works again'); }

/* ---- the REAL drags, macro: q1, from a proven-idle baseline ---- */
idleU('the macro screen idles before the drag');
{ const G=labG(), X=G.X(ST.mi1/10), Y=G.yT;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what===1,'pointer-down ON q1 grabs it');
  idleU('the grab has drained (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:X+0.5*G.s,clientY:Y,buttons:1});
  uok(ST.mi1===-5,'the move put q1 at -0.5 cm ('+ST.mi1+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointermove',{clientX:X+8*G.s,clientY:Y,buttons:1}); uok(ST.mi1===6,'dragged onto q2 it stops 14 mm short ('+ST.mi1+')');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(NODESU.tag.innerHTML.indexOf('r = 1.4 cm')>=0,'the tag followed the drag: r = 1.4 cm');
  uok(NODESU.readout.innerHTML.indexOf('1467 N')>=0,'and the readout |F| = 1467 N (the model\'s F at 1.4 cm)'); }
idleU('idle before q2');
{ const G=labG(), X=G.X(ST.mi2/10), Y=G.yT;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what===2,'pointer-down on q2 grabs it'); idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:X+2*G.s,clientY:Y,buttons:1}); uok(ST.mi2===40,'q2 moved to 4.0 cm ('+ST.mi2+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'repainted through the loop'); NODESU.scene.fire('pointerup',{}); }
idleU('idle before the ruler');
{ const G=labG(), g=G.ruler, X=(g.x0+g.x1)/2, Y=g.y0+10;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what==='ruler','pointer-down on the ruler grabs it'); idleU('proven idle');
  RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:X+2*G.s,clientY:Y,buttons:1}); pumpU(1);
  uok(ST.mRulerI===-30,'a purely horizontal drag slides the ruler 2 cm ('+ST.mRulerI+')'); const gx=geomU(RECU); uok(gx.length>50,'and repaints');
  idleU('idle again');
  const y0=ST.mRulerY; RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:X+2*G.s,clientY:Y-50,buttons:1}); pumpU(1);
  uok(ST.mRulerI===-30&&ST.mRulerY>y0+0.3,'a purely vertical drag lifts it without sliding it'); uok(geomU(RECU)!==gx&&geomU(RECU).length>50,'and the picture moved again');
  NODESU.scene.fire('pointerup',{}); }
idleU('idle before the miss');
{ const G=labG(); NODESU.scene.fire('pointerdown',{clientX:G.b.x+3,clientY:G.b.y+3}); uok(DRAG.what===null,'empty stage grabs nothing');
  NODESU.scene.fire('pointermove',{clientX:G.b.x+80,clientY:G.b.y+40,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }

/* ---- the atomic screen keeps its own state ---- */
const macroSnap=[ST.mi1,ST.mi2,ST.mRulerI];
NODESU.tabs.children[1].fire('click'); uok(ST.view==='atomic','on the atomic scale');
{ RECU=makeRecU(); NODESU.tabs.children[1].fire('click');
  uok(textsU(RECU).indexOf('Force on q₁ by q₂ = 1.15 × 10⁻⁶ N')>=0,'the atomic screen starts in scientific notation (PhET)');
  uok(checkU('scientific notation').checked===true,'and its checkbox says so'); }
idleU('the atomic screen idles');
{ const G=labG(), X=G.X(ST.ai1), Y=G.yT;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what===1,'pointer-down on the atomic q1 grabs it'); idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:X+7*G.s,clientY:Y,buttons:1}); uok(ST.ai1===-13,'q1 moved 7 pm ('+ST.ai1+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'repainted through the loop');
  NODESU.scene.fire('pointermove',{clientX:X+60*G.s,clientY:Y,buttons:1}); uok(ST.ai1===18,'and stops 2 pm short of q2');
  NODESU.scene.fire('pointerup',{}); }
uok(ST.mi1===macroSnap[0]&&ST.mi2===macroSnap[1]&&ST.mRulerI===macroSnap[2],'the macro screen\'s charges and ruler did not move');
{ const s=sliderU('arrow scale'); const k0=ST.mArrowK; RECU=makeRecU(); s.value='12'; s.fire('input');
  uok(ST.aArrowK===12&&ST.mArrowK===k0,'the arrow scale belongs to the screen it was moved on');
  uok(textsU(RECU).some(t=>t.indexOf('1 pm of arrow = 1 × 10⁻⁸ N')>=0),'and the canvas prints the new scale at once'); }
{ ST.aRulerI=-50; ST.aRulerY=null; idleU('idle before the ruler buttons');
  RECU=makeRecU(); uok(clickU('ruler to q₁'),'found "ruler to q₁"'); uok(ST.aRulerI===ST.ai1&&ST.aRulerY===0,'the atomic ruler zero sits on q1');
  uok(geomU(RECU).length>50,'and the screen repainted at once'); uok(ST.mRulerI===macroSnap[2],'the macro ruler stayed put');
  uok(clickU('ruler home'),'found "ruler home"'); uok(ST.aRulerI===-50&&ST.aRulerY===null,'and home puts it back'); }

/* the analysis views ignore the pointer — pressed where q1 sits on its screen */
for(const t of [2,3,4]){ NODESU.tabs.children[1].fire('click'); const G=labG(), X=G.X(ST.ai1), Y=G.yT;
  NODESU.tabs.children[t].fire('click'); idleU('tab '+t+' idles');
  const a1=ST.ai1, m1=ST.mi1; NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); NODESU.scene.fire('pointermove',{clientX:X-3*G.s,clientY:Y,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]'&&ST.ai1===a1&&ST.mi1===m1&&DRAG.what===null,'tab '+t+' ignores the pointer, even over q1\'s screen position'); NODESU.scene.fire('pointerup',{}); }

/* ---- sliders repaint at once, and a sign flips the arrows ---- */
NODESU.tabs.children[0].fire('click'); idleU('idle before the sliders');
{ const s=sliderU('q₁, µC'); uok(!!s,'found the macro q1 slider'); const F0=screenModel(ST,'macro').F1;
  RECU=makeRecU(); s.value='4'; s.fire('input'); uok(ST.mq1===4,'q1 = +4 uC'); uok(RECU.ops.length>=30,'and the screen redrew at once ('+RECU.ops.length+' ops)');
  const F1=screenModel(ST,'macro').F1; uok(F0>0&&F1<0,'the sign change turned the force on q1 round');
  uok(NODESU.readout.innerHTML.indexOf('repel (like signs)')>=0,'the readout says repel'); }
{ const s=sliderU('x₁, cm'); s.value='3.9'; s.fire('input'); uok(ST.mi1===ST.mi2-14,'the x1 slider is held 14 mm clear of q2');
  uok(Math.abs(parseFloat(s.value)-ST.mi1/10)<1e-12,'and springs back to where the rule held it ('+s.value+')'); }
{ const s=sliderU('q₂, e'); uok(!!s,'found the atomic q2 slider'); s.value='-3'; s.fire('input'); uok(ST.aq2===-3&&ST.mq2===8,'it moves only the atomic charge'); }
{ const cb=checkU('the distance between centres'); uok(!!cb,'found the distance checkbox');
  const has=()=>textsU(RECU).some(t=>/^r = [0-9.]+ cm between centres$/.test(t));
  RECU=makeRecU(); cb.checked=false; cb.fire('change'); uok(ST.showDist===false&&!has(),'no distance label when it is off');
  RECU=makeRecU(); cb.checked=true; cb.fire('change'); uok(ST.showDist===true&&has(),'and it is back when it is on'); }

/* ---- the scale chips in the analysis views ---- */
NODESU.tabs.children[2].fire('click');
{ const ac=chipU('atomic scale',2); uok(!!ac,'found the atomic-scale chip'); RECU=makeRecU(); ac.fire('click'); uok(ST.scale==='atomic','atomic selected');
  uok(NODESU.tag.innerHTML.indexOf('(atomic)')>=0,'the inverse square now shows the atomic pair'); uok(RECU.ops.length>=30,'and redrew at once');
  uok(textsU(RECU).some(t=>t.indexOf('distance between centres r, pm')>=0),'with a picometre axis');
  NODESU.tabs.children[3].fire('click'); uok(NODESU.tag.innerHTML.indexOf('(atomic)')>=0,'the charge product follows the same choice');
  chipU('macro scale',2).fire('click'); uok(ST.scale==='macro','back to macro'); }

/* ---- keyboard ---- */
keyU('2'); uok(ST.view==='atomic','2 is the atomic scale'); keyU('5'); uok(ST.view==='grav','5 is electricity and gravity');
keyU('3'); uok(ST.view==='inv','3 is the inverse square'); keyU('1'); uok(ST.view==='macro','1 back to the macro scale');

/* ---- controls, resize, reset ---- */
let ctlErrU=null;
try{ const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===12,'the panel has its 9 sliders and 3 checkboxes ('+inputs.length+')');
  for(const inp of inputs){ if(inp.type==='checkbox'){ if(inp.disabled) continue; inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); } }
  for(const v of [0,1,2,3,4]){ RECU=makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU,'after the slider sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* reset all restores BOTH screens, rulers and notation included (disturbed first) */
  NODESU.tabs.children[1].fire('click');
  Object.assign(ST,{mq1:3,mq2:-9,mi1:-40,mi2:30,mRulerI:5,mRulerY:0.3,mForce:false,mSci:true,mArrowK:3,
                    aq1:7,aq2:7,ai1:-45,ai2:45,aRulerI:10,aRulerY:2,aForce:false,aSci:false,aArrowK:4,showDist:false,scale:'atomic'});
  uok(clickU('reset all'),'found reset all');
  let same=true; for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]) same=false;
  uok(same,'reset all restores every default on both screens'); uok(ST.view==='atomic','and keeps the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
