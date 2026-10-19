
/* ============ UI drive test for gravity-force-lab.html ==================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js,
 * itself from build_cycloid).  Three pointer interactions in the lab (either
 * sphere, the ruler) and one button-started run (the fall).  Every view must
 * paint NOTHING while idle, and every action must move the picture through
 * the frame loop from a proven-idle baseline (Known-bad: a helper that sets
 * the dirty flag masks the flag the next test checks).                      */
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
  /* innerHTML is a setter that strips tags into textContent, as a browser does
     (Known-bad: the shared stub never derived textContent from innerHTML) */
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
/* match whole labels, and a chip row by its arity too (Known-bad: a substring
   finder hits the wrong control) */
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
uok(NODESU.tabs.children.length===4,'four view tabs were built');
uok(NODESU.panel.children.length===5,'the control panel has its five groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').indexOf('1.669 &times; 10<sup>-7</sup> N')>=0,'the readout prints F = 1.669e-7 N off the model');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').length>100,'the equation bar rendered, no NaN');
uok((NODESU.tag.innerHTML||'').indexOf('r = 4.0 m')>=0,'the tag names the distance');

/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[40,40,40,40];
const sigsU={};
for(let i=0;i<4;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===4,'every tab draws a different picture');
for(let i=0;i<4;i++){ NODESU.tabs.children[i].fire('click'); idleU('tab '+i+' paints nothing while idle'); }

/* ---- the lab: the labels follow the chips ---- */
NODESU.tabs.children[0].fire('click');
uok(ST.view==='lab','on the lab');
{ RECU=makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(textsU(RECU).indexOf('Force on m₁ by m₂ = 0.000 000 166 857 N')>=0,'the lab draws PhET\'s decimal label');
  const sc=chipU('scientific notation',3); uok(!!sc,'found the scientific chip');
  RECU=makeRecU(); sc.fire('click'); uok(ST.fmode==='sci','scientific selected');
  uok(textsU(RECU).indexOf('Force on m₁ by m₂ = 1.67 × 10⁻⁷ N')>=0,'and the canvas label switches at once');
  const hc=chipU('hidden',3); RECU=makeRecU(); hc.fire('click');
  uok(textsU(RECU).indexOf('Force on m₁ by m₂')>=0&&textsU(RECU).every(t=>t.indexOf('Force on m₁ by m₂ =')<0),'hidden: the label keeps no value');
  chipU('decimal notation',3).fire('click'); uok(ST.fmode==='dec','back to decimal'); }

/* ---- the REAL drags: m1, from a proven-idle baseline ---- */
idleU('the lab idles before the drag');
{ const G=labG(), X=G.X(ST.i1/10), Y=G.yT;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y});
  uok(DRAG.what===1,'pointer-down ON m1 grabs it');
  idleU('the grab\'s own repaint has drained (proven-idle baseline)');
  RECU=makeRecU(); pumpU(1); const before=geomU(RECU);
  uok(before==='[]','and the loop is quiet');
  NODESU.scene.fire('pointermove',{clientX:X+1.2*G.s,clientY:Y,buttons:1});
  uok(ST.i1===-18,'the move put m1 at -1.8 m ('+ST.i1+')');
  RECU=makeRecU(); pumpU(1); const moved=geomU(RECU);
  uok(moved.length>50,'the move repaints THROUGH the frame loop (dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointermove',{clientX:X+9*G.s,clientY:Y,buttons:1});
  uok(ST.i1===-5,'dragged at m2 it stops 1.5 m short ('+ST.i1+')');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(NODESU.tag.innerHTML.indexOf('r = 1.5 m')>=0,'the tag followed the drag: r = 1.5 m');
  uok(NODESU.readout.innerHTML.indexOf('1.187 &times; 10<sup>-6</sup> N')>=0,'and the readout F = 1.187e-6 N (G x 40000 / 2.25; the default 1.669e-7 cannot supply it)'); }
/* m2 the other way, and its geometry must differ from the m1 drag's */
idleU('idle before m2');
{ const G=labG(), X=G.X(ST.i2/10), Y=G.yT;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what===2,'pointer-down on m2 grabs it');
  idleU('proven idle');
  NODESU.scene.fire('pointermove',{clientX:X+3*G.s,clientY:Y,buttons:1}); uok(ST.i2===40,'m2 moved to 4.0 m ('+ST.i2+')');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'repainted through the loop');
  NODESU.scene.fire('pointerup',{}); }
/* the ruler: x, then y, separately */
idleU('idle before the ruler');
{ const G=labG(), g=G.ruler, X=(g.x0+g.x1)/2, Y=g.y0+10;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); uok(DRAG.what==='ruler','pointer-down on the ruler grabs it');
  idleU('proven idle');
  RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:X+2*G.s,clientY:Y,buttons:1}); pumpU(1);
  uok(ST.rulerI===-30,'a purely horizontal drag slides the ruler 2 m ('+ST.rulerI+')'); const gx=geomU(RECU); uok(gx.length>50,'and repaints');
  idleU('idle again');
  const y0=ST.rulerY; RECU=makeRecU(); NODESU.scene.fire('pointermove',{clientX:X+2*G.s,clientY:Y-60,buttons:1}); pumpU(1);
  uok(ST.rulerI===-30&&ST.rulerY>y0+0.5,'a purely vertical drag lifts it without sliding it ('+fmt(ST.rulerY,3)+' m)');
  uok(geomU(RECU)!==gx&&geomU(RECU).length>50,'and the picture moved again');
  NODESU.scene.fire('pointerup',{}); }
/* a miss grabs nothing and paints nothing */
idleU('idle before the miss');
{ const G=labG(); NODESU.scene.fire('pointerdown',{clientX:G.b.x+3,clientY:G.b.y+3}); uok(DRAG.what===null,'a pointer-down on empty stage grabs nothing');
  NODESU.scene.fire('pointermove',{clientX:G.b.x+80,clientY:G.b.y+40,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }
/* the other views ignore the pointer — pressed exactly where m1 sits in the
   lab, so a missing view guard would grab it (a click on empty stage could not
   tell) */
for(const t of [1,2,3]){ const G=labG(), X=G.X(ST.i1/10), Y=G.yT;
  NODESU.tabs.children[t].fire('click'); idleU('tab '+t+' idles');
  const i1=ST.i1; NODESU.scene.fire('pointerdown',{clientX:X,clientY:Y}); NODESU.scene.fire('pointermove',{clientX:X-2*G.s,clientY:Y,buttons:1});
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]'&&ST.i1===i1&&DRAG.what===null,'tab '+t+' ignores the pointer, even over m1\'s lab position'); NODESU.scene.fire('pointerup',{}); }

/* ---- sliders repaint at once, through the rules ---- */
NODESU.tabs.children[0].fire('click'); idleU('idle before the sliders');
{ const s=sliderU('mass m₁, kg'); uok(!!s,'found the m1 slider'); RECU=makeRecU(); s.value='1000'; s.fire('input');
  uok(ST.m1===1000,'m1 = 1000 kg'); uok(RECU.ops.length>=30,'and the lab redrew at once ('+RECU.ops.length+' ops; the lab emits ~44)');
  uok(NODESU.readout.innerHTML.indexOf('1000 kg, 400 kg')>=0,'the readout has the new mass'); }
{ const s=sliderU('centre x₁, m'); s.value='3.7'; s.fire('input'); uok(ST.i1===ST.i2-pairSteps(ST.m1,ST.m2,ST.cs),'the x1 slider is held clear of m2 by the rule');
  uok(parseFloat(s.value)===ST.i1/10,'and the slider springs back to where the rule held it ('+s.value+')'); }
{ ST.i1=-30; ST.i2=-17; ST.m1=100; ST.m2=100; ST.cs=true;         /* 1.3 m apart, 0.5-m spheres */
  const cb=checkU('constant size (0.5 m)'); uok(!!cb,'found the constant-size checkbox'); cb.checked=true; cb.fire('change'); uok(ST.cs===true,'constant size on');
  const s=sliderU('mass m₂, kg'); s.value='1000'; s.fire('input'); uok(ST.m2===1000&&ST.i1===-30&&ST.i2===-17,'constant size: a heavier m2 is no bigger, nothing moves');
  cb.checked=false; cb.fire('change'); uok(ST.cs===false,'constant size off');
  uok(ST.i2===-17&&ST.i1===-35,'the spheres grew to 1.8 m apart: m1 was pushed left to -3.5 m, m2 held (PhET\'s update order: m2 changed last) ['+ST.i1+', '+ST.i2+']'); }
{ const s=sliderU('arrow scale'); uok(!!s,'found the arrow-scale slider'); RECU=makeRecU(); s.value='12'; s.fire('input');
  uok(ST.arrowK===12,'arrow scale step 12'); uok(textsU(RECU).some(t=>t.indexOf('1 m of arrow = 1 × 10⁻⁶ N')>=0),'the canvas prints the new arrow scale'); }
{ const cb=checkU('the distance between centres'); uok(!!cb,'found the distance checkbox');
  const hasDist=()=>textsU(RECU).some(t=>t.indexOf('r = 1.8 m between centres')>=0);
  RECU=makeRecU(); cb.checked=false; cb.fire('change'); uok(ST.showDist===false&&!hasDist(),'no distance label when it is off');
  RECU=makeRecU(); cb.checked=true; cb.fire('change'); uok(ST.showDist===true&&hasDist(),'and "r = 1.8 m between centres" is back when it is on'); }
{ ST.rulerI=-50; ST.rulerY=null; idleU('idle before the ruler buttons');
  RECU=makeRecU(); uok(clickU('ruler to m₁'),'found "ruler to m₁"'); uok(ST.rulerI===ST.i1&&ST.rulerY===0,'the ruler zero sits on m1\'s centre');
  uok(geomU(RECU).length>50,'and the lab repainted at once');
  uok(clickU('ruler home'),'found "ruler home"'); uok(ST.rulerI===-50&&ST.rulerY===null,'and home puts it back'); }

/* ---- the fall: release, motion through the loop, pause, stop ---- */
clickU('reset all');
NODESU.tabs.children[3].fire('click'); uok(ST.view==='fall','on let them go');
idleU('the fall idles before release');
uok(NODESU.readout.innerHTML.indexOf('12 h 10 min')>=0,'the readout predicts contact after 12 h 10 min');
uok(clickU('release'),'found the release button'); uok(RUN.active&&RUN.frame===0,'the run started');
RECU=makeRecU(); pumpU(1); const fA=geomU(RECU);
RECU=makeRecU(); pumpU(1); const fB=geomU(RECU);
uok(fA.length>50&&fB.length>50&&fA!==fB,'two pumped frames draw DIFFERENT pictures (the spheres close)');
{ const ro0=NODESU.readout.innerHTML; pumpU(12); uok(NODESU.readout.innerHTML!==ro0,'the readout refreshes during the run'); uok(NODESU.readout.innerHTML.indexOf('falling')>=0,'and says falling'); }
{ const tr=checkU('time runs'); uok(!!tr&&tr.checked===true,'time runs by default'); tr.checked=false; tr.fire('change'); idleU('paused, the run does not advance');
  const f0=RUN.frame; pumpU(5); uok(RUN.frame===f0,'the frame count holds while paused'); keyU(' '); uok(ST.running===true,'space resumes');
  RECU=makeRecU(); pumpU(2); uok(geomU(RECU).length>50&&RUN.frame===f0+2,'and the spheres move again'); }
pumpU(700); uok(RUN.frame===600,'the run stops at contact (frame 600)'); uok(NODESU.readout.innerHTML.indexOf('touching')>=0,'the readout says touching');
uok(NODESU.tag.innerHTML.indexOf('touching')>=0,'and so does the tag');
idleU('after contact the loop idles');
/* again at a different frame phase: the readout refreshes every tenth frame,
   and a run whose last step happened to land on one would hide a readout that
   is never told the run ended (the two final frame counts differ by 3 mod 10) */
keyU('r'); pumpU(3); uok(clickU('release'),'release for the second phase'); pumpU(700);
uok(RUN.frame===600&&NODESU.readout.innerHTML.indexOf('touching')>=0&&NODESU.tag.innerHTML.indexOf('touching')>=0,'the second run also ends saying touching');
keyU('r'); uok(RUN.active===false,'r resets the run'); idleU('and the loop idles');
uok(clickU('release'),'release again'); pumpU(10); uok(clickU('stop & reset')&&!RUN.active,'stop & reset ends it');
{ uok(clickU('release'),'release once more'); pumpU(5); const s=sliderU('mass m₁, kg'); s.value='500'; s.fire('input'); uok(!RUN.active,'a slider stops the run (the start state changed)'); }
{ uok(clickU('release'),'and again'); pumpU(5); NODESU.tabs.children[0].fire('click'); uok(!RUN.active,'leaving the view stops the run'); }

/* ---- keyboard ---- */
keyU('2'); uok(ST.view==='inv','2 is the inverse square'); keyU('3'); uok(ST.view==='prod','3 is the mass product');
keyU('4'); uok(ST.view==='fall','4 is let them go'); keyU('1'); uok(ST.view==='lab','1 back to the lab');
keyU(' '); uok(ST.running===false,'space pauses'); keyU(' '); uok(ST.running===true,'and resumes');

/* ---- controls, resize, reset ---- */
let ctlErrU=null;
try{ const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===8,'the panel has its 5 sliders and 3 checkboxes ('+inputs.length+')');
  for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
    const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
    for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','slider at '+v+' draws without error'); } }
  for(const v of [0,1,2,3]){ RECU=makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU,'after the slider sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* reset all must restore EVERY kind of state it claims to: masses, positions,
     size mode, notation, arrow scale, the ruler (disturbed first, Known-bad) */
  NODESU.tabs.children[0].fire('click');
  ST.m1=700; ST.m2=20; ST.i1=-40; ST.i2=30; ST.cs=true; ST.fmode='hid'; ST.arrowK=3; ST.rulerI=12; ST.rulerY=0.4; ST.showDist=false;
  uok(clickU('reset all'),'found reset all');
  uok(ST.m1===100&&ST.m2===400&&ST.i1===-30&&ST.i2===10&&ST.cs===false&&ST.fmode==='dec'&&ST.arrowK===9&&ST.rulerI===-50&&ST.rulerY===null&&ST.showDist===true,
      'reset all restores masses, positions, size, notation, arrows, ruler, distance');
  uok(ST.view==='lab','and keeps the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
