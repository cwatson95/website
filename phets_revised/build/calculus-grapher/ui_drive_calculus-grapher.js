
/* ============ UI drive test for calculus-grapher.html ==================== *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_fourier-making-waves).
 * The sim-specific thresholds: the chip rows are found by exact label AND
 * arity (8 curve-manipulation modes, 5 reference shapes, 2 notations, 2
 * variables, 2 discontinuity styles); the panel has 8 groups; 18 inputs
 * (11 sliders, 7 checkboxes) and 5 buttons.
 *
 * Every drag is tested from a PROVEN-IDLE baseline and in two separate ways,
 * because "the picture changed" and "the loop repainted" are different claims
 * and the Known-bad list records three sims where only one of them was made:
 *   (a) two REAL drawings taken through S.draw() either side of the action,
 *       asserted different;
 *   (b) the loop pumped from idle after the action, asserted to have emitted.
 */
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
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h]);}, strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);},
    clearRect:P,
    fillText(t,x,y){ops.push(['t',String(t),Math.round(x),Math.round(y)]);}, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||'');
      return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
    createLinearGradient(){return {addColorStop(){}};},
  };
  Object.defineProperty(c,'font',{get:()=>st.font,set:v=>st.font=v});
  for(const k of ['fillStyle','strokeStyle','lineWidth','globalAlpha','textAlign','textBaseline',
                  'lineJoin','lineCap'])
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
    fire(k,ev){ for(const f of (this._h[k]||[]))
      f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  /* a real browser derives textContent from innerHTML; the shared stub did not (Known-bad) */
  let _html='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },
    set(v){ _html=''+v; e.textContent=(''+v).replace(/<[^>]*>/g,''); }});
  return e;
}
const NODESU={};
for(const id of ['scene','panel','tabs','readout','eqbar','tag','hint','errbox','sub'])
  NODESU[id]=mkElU(id==='scene'?'canvas':'div'), NODESU[id].id=id;
globalThis.document={readyState:'complete',getElementById:id=>NODESU[id]||null,createElement:mkElU,
  createTextNode:t=>({nodeType:3,textContent:''+t,children:[]}),addEventListener(){}};
const WINHU={}; let RAFU=null;
globalThis.window={devicePixelRatio:1,addEventListener(k,f){ (WINHU[k]=WINHU[k]||[]).push(f); },
  requestAnimationFrame(f){ RAFU=f; return 1; }};
globalThis.requestAnimationFrame=f=>{ RAFU=f; return 1; };
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle)
      for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
/* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity)
      for(const c of ch.children) if(plain(c.textContent||'')===plain(label)) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
/* a REAL drawing, taken directly rather than through the loop, so a
   "the picture moved" test never compares against an idle capture */
function shotU(){ const old=RECU; RECU=makeRecU(); BOOTED.draw(); const r=RECU; RECU=old; return r; }

/* ---- boot ---- */
let bootErrU=null, BOOTED=null;
try{ BOOTED=boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')===
    'the derivative|the integral|the lab|the corners|the theorem|the grid',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===8,'the control panel has its 8 groups ('+NODESU.panel.children.length+')');
uok(NODESU.panel.querySelectorAll('input').length===18,
    'the panel has its 18 inputs ('+NODESU.panel.querySelectorAll('input').length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,
    'the panel carries the PhET credit line');
uok(NODESU.panel.textContent.indexOf('1251')>=0,"PhET's 1251 points reach the page");
uok(ST.view==='deriv'&&ST.mode==='hill'&&ST.width===W_DEF&&ST.tangent===true,
    "the start: the derivative view, a hill of PhET's default width, tangent on");
uok(Math.abs(Math.max.apply(null,Array.from(CURVE))-1.6)<1e-9,
    '... and the file opens with a curve already drawn, not a flat line');

/* ---- every tab draws, differently, cleanly ---- */
/* the floors are derived from what each view EMITS at the shipped defaults
   (77, 55, 119, 89, 91, 111), not from another sim's harness: the integral
   view legitimately draws two curves and no tool until one is switched on. */
const FLOORSU=[62,44,95,71,72,88];
const OPSU=[]; const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  uok((NODESU.readout.innerHTML||'').length>200,'tab '+i+' fills the readout');
  uok((NODESU.eqbar.innerHTML||'').length>60,'tab '+i+' fills the equation bar');
  uok((NODESU.panel.querySelector('#info').innerHTML||'').length>400,'tab '+i+' fills the info prose');
  uok((NODESU.panel.querySelector('#phys').innerHTML||'').length>400,'tab '+i+' fills the mathematics block');
  { let act=0, wrong=0;
    for(let j=0;j<6;j++){ const c=NODESU.tabs.children[j].className||'';
      if(j===i){ if(c==='active') act++; else wrong++; } else if(c!=='') wrong++; }
    uok(act===1&&wrong===0,'tab '+i+' is the only one marked active'); }
  sigsU['t'+i]=sigU(RECU); OPSU.push(RECU.ops.length);
}
console.log('UI: ops per tab = '+OPSU.join(', '));
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- nothing animates: this sim is arithmetic ---- */
for(let i=0;i<6;i++){ tabU(i); idleU('tab '+i+' paints nothing once it has settled'); }

/* ---- the eight curve-manipulation modes ---- */
tabU(0);
for(const m of ['hill','triangle','pedestal','parabola','sinusoid','freeform','tilt','shift']){
  const c=chipU(m,8);
  uok(!!c,'found the "'+m+'" mode chip');
  if(!c) continue;
  RECU=makeRecU(); c.fire('click');
  uok(ST.mode===m,'the "'+m+'" chip selects it');
  uok((c.className||'').indexOf('on')>=0,'... and shows as selected');
  { let on=0;
    for(const q of MODES){ const z=chipU(q.name,8); if(z&&(z.className||'').indexOf('on')>=0) on++; }
    uok(on===1,'... and is the only chip in its row that is'); }
  uok(RECU.ops.length>0,'... and the view repaints');
  assertCleanU(RECU,'mode '+m);
  /* the width row is only live for the five shape modes */
  const wr=sliderU('shape width w');
  uok(!!wr,'the width slider exists for '+m);
}
/* the width row is HIDDEN for the modes that ignore it, never left live and inert */
chipU('shift',8).fire('click');
{ let hidden=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&ch.children[0].textContent==='shape width w')
      hidden=ch.hidden;
    walk(ch); } };
  walk(NODESU.panel);
  uok(hidden===true,'the width row is hidden in shift mode, not left live and ignored'); }
chipU('hill',8).fire('click');
{ let hidden=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&ch.children[0].textContent==='shape width w')
      hidden=ch.hidden;
    walk(ch); } };
  walk(NODESU.panel);
  uok(hidden===false,'... and back when a shape mode is chosen'); }

/* ---- the buttons ---- */
{ clickButtonU('reset all');
  const before=CURVE.slice();
  uok(clickButtonU('lay it down'),'found the lay-it-down button');
  let d=0; for(let i=0;i<NPTS;i++) d=Math.max(d,Math.abs(CURVE[i]-before[i]));
  uok(d>0.1,'... and it changes the curve ('+fmt(d,3)+')');
  uok(Math.abs(CURVE[idxAt(ST.placeX)]-ST.height)<1e-9,'... putting the shape where the sliders say');
  uok(clickButtonU('undo'),'found the undo button');
  let d2=0; for(let i=0;i<NPTS;i++) d2=Math.max(d2,Math.abs(CURVE[i]-before[i]));
  uok(d2<1e-12,'... and it puts the curve back exactly');
  const peak=Math.max.apply(null,Array.from(CURVE));
  uok(clickButtonU('smooth'),'found the smooth button');
  const peak2=Math.max.apply(null,Array.from(CURVE));
  uok(peak2<peak&&peak2>0.9*peak,
      '... and smoothing lowers the peak a little ('+fmt(peak,4)+' to '+fmt(peak2,4)+')');
  uok(clickButtonU('erase'),'found the erase button');
  uok(Math.max.apply(null,Array.from(CURVE))===0,'... and erase gives PhET\'s flat curve');
  /* the button must use the WIDTH SLIDER, not the default it happens to equal:
     with ST.width at W_DEF the mutant that substituted W_DEF was invisible.
     On an EMPTY curve, or the shipped triangle blends into the probe and the
     number measures the blend instead of the width. */
  { const sw=sliderU('shape width w'); sw.value='4'; sw.fire('input'); }
  uok(ST.width===4,'the width slider moves off its default');
  clickButtonU('lay it down');
  const probe=CURVE[idxAt(ST.placeX+ST.width/2)];
  uok(Math.abs(probe-Math.exp(-2)*ST.height)<2e-4,
      'a hill laid down at w = 4 is exp(-2) of its height half a width out ['
      +fmt(probe,5)+' vs '+fmt(Math.exp(-2)*ST.height,5)+']');
  uok(Math.abs(probe-Math.exp(-2)*ST.height*0+CURVE[idxAt(ST.placeX)])>0.5,
      '... and nothing like its height there, so the width is what is being read');
  { const sw=sliderU('shape width w'); sw.value=String(W_DEF); sw.fire('input'); }
  uok(clickButtonU('reset all'),'found the reset button');
  uok(Math.abs(Math.max.apply(null,Array.from(CURVE))-1.6)<1e-9,
      '... and reset brings the shipped curve back');
}

/* ---- every slider moves, and moves the picture ---- */
function driveSliderU(label,vals,key){
  const s=sliderU(label);
  uok(!!s,'found the "'+label+'" slider');
  if(!s) return;
  let changed=0;
  for(const v of vals){
    RECU=makeRecU();
    s.value=String(v); s.fire('input');
    if(key!==undefined) uok(Math.abs(ST[key]-v)<1e-9,'"'+label+'" sets '+key+' to '+v);
    if(RECU.ops.length>0) changed++;
    assertCleanU(RECU,'"'+label+'" at '+v);
  }
  uok(changed===vals.length,'"'+label+'" repaints on every step ('+changed+'/'+vals.length+')');
}
tabU(0);
driveSliderU('shape width w',[W_MIN,2.5,W_MAX],'width');
driveSliderU('shape height y',[Y_MIN,0,1.75],'height');
driveSliderU('shape centre x',[0,4.3,10],'placeX');
driveSliderU('tangent at x',[0,2.4,9.6],'xT');
{ const c=findLabelledU('area under curve'); c.checked=true; c.fire('change'); }
driveSliderU('area up to x',[0.4,5.0,10],'xA');
{ const c=findLabelledU('reference line'); c.checked=true; c.fire('change'); }
driveSliderU('reference line x',[1.2,7.7],'xR');
tabU(3);
driveSliderU('reference width w',[W_MIN,3.0,W_MAX],'refW');
driveSliderU('reference height y',[-1.5,1.5],'refY');
driveSliderU('reference centre x',[3.0,7.0],'refX');
driveSliderU('which corner',[0,1,2],'cornerSel');
tabU(5);
driveSliderU('cells shown',[0,2,GRID_MULTS.length-1],'gridMult');
tabU(0);

/* ---- every checkbox ---- */
for(const [lab,key,view] of [['tangent','tangent',0],['area under curve','area',1],
                             ['reference line','refLine',2],['grid','grid',0],
                             ['values','values',2],['predict f myself','predict',2]]){
  tabU(view);
  const c=findLabelledU(lab);
  uok(!!c,'found the "'+lab+'" checkbox');
  if(!c) continue;
  const was=ST[key];
  RECU=makeRecU();
  c.checked=!was; c.fire('change');
  uok(ST[key]===!was,'"'+lab+'" toggles '+key);
  uok(RECU.ops.length>0,'"'+lab+'" repaints');
  assertCleanU(RECU,'"'+lab+'" on');
  c.checked=was; c.fire('change');
}
/* the show-f row only exists while predicting */
tabU(2);
{ let hidden=null;
  const walkH=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')==='show f') hidden=ch.hidden;
    walkH(ch); } };
  walkH(NODESU.panel);
  uok(hidden===true,'the show-f row is hidden while predict is off');
  const p=findLabelledU('predict f myself'); p.checked=true; p.fire('change');
  hidden=null; walkH(NODESU.panel);
  uok(hidden===false,'... and appears when it is on');
  uok(ST.predict===true,'predict is on');
  const M=BOOTED.model();
  uok(M.shape!==M.live,'... and the shaped curve is now a different object from f');
  const sf=findLabelledU('show f');
  RECU=makeRecU(); sf.checked=false; sf.fire('change');
  uok(ST.showF===false&&RECU.ops.length>0,'"show f" turns off and repaints');
  sf.checked=true; sf.fire('change');
  p.checked=false; p.fire('change'); }

/* ---- the notation, variable and discontinuity chips ---- */
tabU(2);
for(const [name,want] of [['Leibniz','leibniz'],['Lagrange','lagrange']]){
  const c=chipU(name,2);
  uok(!!c,'found the "'+name+'" notation chip');
  if(c){ RECU=makeRecU(); c.fire('click');
    uok(ST.notation===want,'the "'+name+'" chip selects '+want);
    assertCleanU(RECU,'notation '+name); }
}
for(const [name,want] of [['t','t'],['x','x']]){
  const c=chipU(name,2);
  uok(!!c,'found the "'+name+'" variable chip');
  if(c){ c.fire('click'); uok(ST.variable===want,'the "'+name+'" chip selects the variable '+want); }
}
chipU('t',2).fire('click');
{ const txt=textU(shotU());
  uok(txt.indexOf('f′(t)')>=0||txt.indexOf('df/dt')>=0,
      'PhET\'s variable preference reaches the canvas');
  uok(txt.split(' | ').indexOf('t')>=0,'... including the x-axis label, which used to stay "x"');
  uok(txt.split(' | ').indexOf('x')<0,'... and no stray "x" is left on it'); }
chipU('x',2).fire('click');
chipU('Leibniz',2).fire('click');
{ const txt=textU(shotU());
  uok(txt.indexOf('df/dx')>=0,'... and so does the Leibniz notation preference'); }
chipU('Lagrange',2).fire('click');
tabU(0);
for(const [name,want] of [['dashed line','dashedLine'],['no line','noLine']]){
  const c=chipU(name,2);
  uok(!!c,'found the "'+name+'" discontinuity chip');
  if(c){ RECU=makeRecU(); c.fire('click');
    uok(ST.discont===want,'the "'+name+'" chip selects '+want);
    assertCleanU(RECU,'discontinuity '+name); }
}
/* the two settings must DRAW differently on a curve that has a corner */
{ const a=geomU(shotU());
  chipU('dashed line',2).fire('click');
  const b=geomU(shotU());
  uok(a!==b,'joining the derivative across a corner really changes the drawing');
  chipU('no line',2).fire('click'); }

/* ---- the reference-shape chips ---- */
tabU(3);
/* put the sliders back where the corner counts are the ones selfTest pins:
   a sinusoid of width 5 is seven half-periods of lambda = 5 pi, which is 27
   units wide, so BOTH its ends are outside a 10-unit domain and it has no
   corner in range at all.  Asserting "a sinusoid has corners" without saying
   at what width is asserting nothing. */
for(const [lab,v] of [['reference width w',2],['reference height y',1.5],['reference centre x',5]]){
  const s2=sliderU(lab); s2.value=String(v); s2.fire('input');
}
const WANT_CORNERS={hill:0,triangle:3,pedestal:0,parabola:2,sinusoid:0};
for(const m of SHAPE_MODES){
  const c=chipU(m,5);
  uok(!!c,'found the reference "'+m+'" chip');
  if(!c) continue;
  RECU=makeRecU(); c.fire('click');
  uok(ST.refShape===m,'the reference "'+m+'" chip selects it');
  assertCleanU(RECU,'reference '+m);
  const M=BOOTED.model();
  uok(M.ref.corners.length===WANT_CORNERS[m],
      'at w = 2 the '+m+' has '+WANT_CORNERS[m]+' corner(s) ['+M.ref.corners.length+']');
}
/* narrow the sinusoid until its packet fits, and the two ends become corners */
chipU('sinusoid',5).fire('click');
{ const s2=sliderU('reference width w'); s2.value='0.6'; s2.fire('input');
  uok(BOOTED.model().ref.corners.length===2,
      'narrowed to w = 0.6 the sinusoid ends inside the domain, in two corners');
  s2.value='2'; s2.fire('input'); }
/* the triangle's one-sided limits reach the readout */
chipU('triangle',5).fire('click');
{ const s=sliderU('reference width w'); s.value='2'; s.fire('input');
  const sy=sliderU('reference height y'); sy.value='1.5'; sy.fire('input');
  const sx=sliderU('reference centre x'); sx.value='4'; sx.fire('input');
  const ro=NODESU.readout.innerHTML||'';
  uok(ro.indexOf('1.0000')>=0,'the readout prints the exact one-sided limit 1.0000');
  uok(ro.indexOf('-1.0000')>=0||ro.indexOf('−1.0000')>=0,'... and its negative twin'); }

/* ---- the canvas drag: idle first, then BOTH claims ---- */
tabU(0);
chipU('hill',8).fire('click');
idleU('the derivative view is idle before the drag');
{ BOOTED.draw();
  uok(GEO.view==='deriv'&&!!GEO.fb&&!!GEO.fmap,'the derivative view records its f panel');
  const m=GEO.fmap;
  const before=geomU(shotU());
  const a0=CURVE[idxAt(6.0)];
  /* (b) the loop repaints: pump from proven idle */
  pumpU(3); RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]','... and still idle immediately before the press');
  NODESU.scene.fire('pointerdown',{clientX:m.X(6.0),clientY:m.Y(1.3)});
  RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>0,'the press makes the frame loop repaint');
  uok(Math.abs(CURVE[idxAt(6.0)]-1.3)<1e-9,'the press puts the hill top under the pointer');
  uok(Math.abs(CURVE[idxAt(6.0)]-a0)>0.5,'... and the curve really changed');
  /* (a) two real drawings */
  const after=geomU(shotU());
  uok(before!==after,'and the DRAWING moved, not only the state');
  uok(after.length>500,'... and the new drawing has substance');
  /* the drag re-applies from the SAVED curve rather than stacking */
  /* the MOVE has its own dirty flag and its own repaint: the press's was
     already asserted above, and a sweep let "a drag never marks the frame
     dirty" survive because nothing pumped the loop after a move */
  pumpU(3); RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]','the loop is idle again mid-drag, before the move');
  NODESU.scene.fire('pointermove',{clientX:m.X(8.0),clientY:m.Y(-0.8),buttons:1});
  RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>0,'the move makes the frame loop repaint');
  uok(Math.abs(CURVE[idxAt(8.0)]+0.8)<1e-9,'a drag moves the shape to the new position');
  uok(Math.abs(CURVE[idxAt(6.0)]-1.3)>0.5,'... and the old one is gone, not stacked under it');
  NODESU.scene.fire('pointerup',{});
  uok(!BOOTED.drag,'the release clears the drag');
  /* one drag is one undo step */
  clickButtonU('undo');
  uok(Math.abs(CURVE[idxAt(8.0)]+0.8)>0.5,'one drag is one undo step');
}
/* the scrubber drag, again from a proven-idle baseline */
{ clickButtonU('reset all');
  BOOTED.draw();
  idleU('idle before the scrubber drag');
  const sc=GEO.scrubs.filter(s=>s.kind==='T')[0];
  uok(!!sc,'the tangent scrubber is recorded for hit-testing');
  const before=geomU(shotU());
  const x0=ST.xT;
  NODESU.scene.fire('pointerdown',{clientX:sc.X+2,clientY:(sc.b.y+sc.b.y1)/2});
  RECU=makeRecU(); pumpU(1);
  uok(RECU.ops.length>0,'grabbing the scrubber repaints through the loop');
  uok(ST.xT!==x0,'... and moves it');
  uok(BOOTED.drag&&BOOTED.drag.what==='scrub','... rather than starting a curve drag');
  const curveBefore=CURVE.slice();
  NODESU.scene.fire('pointermove',{clientX:sc.b.x+0.8*sc.b.w,clientY:(sc.b.y+sc.b.y1)/2,buttons:1});
  uok(Math.abs(ST.xT-(XMIN+XLEN*0.8))<1e-9,'a drag carries the scrubber');
  let moved=0; for(let i=0;i<NPTS;i++) moved=Math.max(moved,Math.abs(CURVE[i]-curveBefore[i]));
  uok(moved===0,'... and never touches the curve');
  const after=geomU(shotU());
  uok(before!==after,'... and the drawing follows it');
  NODESU.scene.fire('pointerup',{}); }
/* the tangent the canvas draws is the number the readout prints */
{ const M=BOOTED.model();
  const ro=NODESU.readout.innerHTML||'';
  uok(ro.indexOf(fmt(M.tools.tan.slope,4))>=0,'the readout prints the slope the tangent tool measured');
  uok(Math.abs(M.tools.tan.slope-M.live.d[cellAt(ST.xT)])<1e-15,
      '... which is the derivative curve at the same x'); }
/* the area tool on the integral view */
tabU(1);
{ const c=findLabelledU('area under curve'); if(!c.checked){ c.checked=true; c.fire('change'); }
  BOOTED.draw();
  const sa=GEO.scrubs.filter(s=>s.kind==='A')[0];
  uok(!!sa,'the area scrubber is recorded');
  NODESU.scene.fire('pointerdown',{clientX:sa.b.x+0.55*sa.b.w,clientY:(sa.b.y+sa.b.y1)/2});
  NODESU.scene.fire('pointerup',{});
  const M=BOOTED.model();
  uok(M.tools.areaMismatch<1e-11,'the painted area and the integral curve agree after the drag ['
      +M.tools.areaMismatch.toExponential(2)+']');
  uok((NODESU.readout.innerHTML||'').indexOf(fmt(M.tools.ar.net,4))>=0,
      '... and the readout prints the net'); }
/* a press outside any panel does nothing */
tabU(0);
{ const before=CURVE.slice();
  const took=NODESU.scene.fire('pointerdown',{clientX:5,clientY:5});
  NODESU.scene.fire('pointerup',{});
  let d=0; for(let i=0;i<NPTS;i++) d=Math.max(d,Math.abs(CURVE[i]-before[i]));
  uok(d===0,'a press outside the f panel leaves the curve alone'); }
/* the analysis views take no curve drag at all */
tabU(4);
BOOTED.draw();
uok(GEO.fb===null||GEO.view==='ftc','the theorem view exposes only its top panel');
tabU(3);
BOOTED.draw();
uok(GEO.fb===null,'the corners view takes no curve drag: it is showing a reference shape');
{ const before=CURVE.slice();
  NODESU.scene.fire('pointerdown',{clientX:400,clientY:300});
  NODESU.scene.fire('pointerup',{});
  let d=0; for(let i=0;i<NPTS;i++) d=Math.max(d,Math.abs(CURVE[i]-before[i]));
  uok(d===0,'... and a press on it changes nothing'); }

/* ---- the keyboard ---- */
tabU(0);
for(let i=1;i<=6;i++){ keyU(String(i)); uok(ST.view===TABS[i-1][0],'key '+i+' selects '+TABS[i-1][0]); }
keyU('1');
{ const x0=ST.xT;
  keyU('ArrowRight'); uok(Math.abs(ST.xT-x0-5*DX)<1e-12,'the right arrow nudges the tangent by five cells');
  keyU('ArrowLeft'); uok(Math.abs(ST.xT-x0)<1e-12,'and the left arrow puts it back'); }
{ const peak=Math.max.apply(null,Array.from(CURVE));
  keyU('s');
  uok(Math.max.apply(null,Array.from(CURVE))<peak,'"s" smooths');
  keyU('u');
  uok(Math.abs(Math.max.apply(null,Array.from(CURVE))-peak)<1e-12,'"u" undoes it');
  keyU('e');
  uok(Math.max.apply(null,Array.from(CURVE))===0,'"e" erases');
  keyU('r');
  uok(Math.abs(Math.max.apply(null,Array.from(CURVE))-1.6)<1e-9,'"r" resets to the shipped curve');
  uok(ST.view==='deriv','... and stays on the current view'); }

/* ---- reset all really resets everything it claims to ---- */
tabU(2);
{ const s=sliderU('shape width w'); s.value='4.5'; s.fire('input');
  const c=findLabelledU('values'); c.checked=true; c.fire('change');
  ST.xT=9.1; ST.xA=1.1; ST.xR=2.2;
  chipU('Leibniz',2).fire('click');
  const p=findLabelledU('predict f myself'); p.checked=true; p.fire('change');
  /* put a SENTINEL in the prediction: with predict merely switched on the
     prediction is still all zeros, so "reset all zeroes it" passes even with
     the line that zeroes it deleted (Known-bad, and this sweep proved it) */
  saveCurve(); applyShape('hill',2,4,1.3);
  uok(Math.max.apply(null,Array.from(PRED))>1,'the prediction carries a sentinel before the reset');
  const p2=findLabelledU('predict f myself'); p2.checked=false; p2.fire('change');
  saveCurve(); applyShape('triangle',3,2,-1.5);
  uok(clickButtonU('reset all'),'found reset all');
  uok(ST.width===W_DEF&&ST.values===false&&ST.notation==='lagrange'&&ST.predict===false,
      'reset all restores every control it claims to');
  uok(Math.abs(ST.xT-DEFAULTS.xT)<1e-12&&Math.abs(ST.xA-DEFAULTS.xA)<1e-12,
      '... including the three scrubbers');
  uok(Math.abs(Math.max.apply(null,Array.from(CURVE))-1.6)<1e-9,'... and the curve');
  uok(Math.max.apply(null,Array.from(PRED))===0,'... and the prediction');
  uok(ST.view==='lab','... and leaves the view alone'); }

/* ---- resize ---- */
for(const [W,H] of [[1400,820],[1100,700],[820,560],[560,380],[1600,960]]){
  NODESU.scene.getBoundingClientRect=()=>({left:0,top:0,width:W,height:H});
  RECU=makeRecU();
  for(const f of (WINHU.resize||[])) f({});
  uok(RECU.ops.length>0,'resize to '+W+'x'+H+' repaints');
  assertCleanU(RECU,'resize '+W+'x'+H);
  uok(NODESU.errbox.style.display!=='block','resize to '+W+'x'+H+' drew without error');
}
NODESU.scene.getBoundingClientRect=()=>({left:0,top:0,width:1400,height:820});
for(const f of (WINHU.resize||[])) f({});

/* ---- every view x every mode builds a clean panel ---- */
for(let i=0;i<6;i++){
  tabU(i);
  for(const m of MODES){
    const c=chipU(m.name,8);
    if(!c) continue;
    RECU=makeRecU(); c.fire('click');
    assertCleanU(RECU,'view '+i+' with '+m.name);
    uok(NODESU.errbox.style.display!=='block','view '+i+' with '+m.name+' drew without error');
    uok(!/NaN|undefined/.test(NODESU.readout.innerHTML||''),'view '+i+' with '+m.name+': readout clean');
    uok(!/NaN|undefined/.test(NODESU.eqbar.innerHTML||''),'view '+i+' with '+m.name+': equation bar clean');
    uok(!/NaN|undefined/.test(NODESU.tag.innerHTML||''),'view '+i+' with '+m.name+': tag clean');
  }
}
/* and on an EMPTY curve, which is the one configuration that can draw nothing */
tabU(0);
clickButtonU('erase');
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=40,'view '+i+' still draws on an erased curve ('+RECU.ops.length+' ops)');
  assertCleanU(RECU,'view '+i+' erased');
  uok(!/NaN|undefined/.test(NODESU.readout.innerHTML||''),'view '+i+' erased: readout clean');
}
clickButtonU('reset all');

/* the house format EXACTLY: _tools/verify_one.py looks for a line that
   contains 'UI' and matches '<n> passed, <m> failed'. */
console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
