/* ============ UI drive test for blackbody-spectrum.html =================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js, which carries the
 * innerHTML -> textContent fix).  Nothing in this sim animates, so EVERY view must paint nothing
 * while idle, and every action must repaint through the frame loop from a proven-idle baseline.
 * Two pointer drags (the thermometer, the Graph Values point), one slider, five checkboxes, four
 * preset chips, eight buttons, the keys.                                                         */
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
        else if(want==='#phys'&&ch.id==='phys') out.push(ch);
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
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
function sliderU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) hit=ch.children[1];
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
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
const RO=()=>NODESU.readout.innerHTML;

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.panel.children.length===7,'the control panel has its seven groups ('+NODESU.panel.children.length+')');
uok(RO().length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').indexOf('Planck')>=0,'the equation bar carries Planck’s law, no NaN');
uok(RO().indexOf('6.42×10⁷')>=0,'the readout prints sigma T^4 = 6.42x10^7 W/m^2 off the model');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');

/* ---- every tab draws, differently, cleanly, and then idles ---- */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[147,372,63,63,51];   /* 70 % of what each tab emits at 1400 x 820 (TABOPS 210, 532, 91, 91, 73) */
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while idle (nothing here animates)');
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');

/* ---- the thermometer, dragged through the frame loop from a proven-idle baseline ---- */
NODESU.tabs.children[0].fire('click');
idleU('the spectrum idles before the drag');
{ const g=specGeo(RECU,1400,820,buildModel()), th=g.th;
  uok(!!th,'the thermometer is laid out at 1400 x 820');
  const X=th.x+6;
  NODESU.scene.fire('pointerdown',{clientX:X,clientY:thermoY(th,3000)});
  uok(DRAG.what==='thermo'&&ST.T===3000,'pointer-down on the thermometer at 3000 K grabs it and sets 3000 K ('+ST.T+')');
  uok(Math.abs(ST.gvNm-peakNm(3000))<1e-9,'and sends Graph Values to the new peak');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200,'the grab itself repaints through the loop (T jumped to 3000 K)');
  idleU('the grab’s own repaint has drained (proven-idle baseline)');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:thermoY(th,9950),buttons:1});
  uok(ST.T===9950,'the move set 9950 K ('+ST.T+')');
  RECU=makeRecU(); pumpU(2); const gA=geomU(RECU);
  uok(gA.length>200,'the move repaints THROUGH the frame loop (the dirty flag)');
  idleU('and goes idle again');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:thermoY(th,9950)+1,buttons:1});
  RECU=makeRecU(); pumpU(2); uok(geomU(RECU)==='[]','a move inside the same 50-K step changes nothing and paints nothing');
  NODESU.scene.fire('pointermove',{clientX:X,clientY:thermoY(th,6000),buttons:1});
  RECU=makeRecU(); pumpU(2); const gB=geomU(RECU); uok(ST.T===6000&&gB.length>200&&gB!==gA,'a second move draws a DIFFERENT picture (6000 K)');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(RO().indexOf('6000 K')>=0,'the readout followed the drag');
  uok(sliderU('T, kelvin').value==6000,'and so did the panel slider');
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:g.b.x+g.b.w*0.9,clientY:g.b.y+30});
  uok(DRAG.what===null,'a pointer-down on empty plot grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties'); NODESU.scene.fire('pointerup',{}); }

/* ---- Graph Values: switch it on, drag the point along the curve ---- */
{ const cb=findLabelledU('graph values'); uok(!!cb,'found the graph values checkbox');
  ST.gvNm=1234;                                  /* a sentinel off the peak, set IMMEDIATELY before the action */
  RECU=makeRecU(); cb.checked=true; cb.fire('change');
  uok(ST.gv===true&&Math.abs(ST.gvNm-peakNm(ST.T))<1e-9,'graph values on re-centres the point on the peak (PhET), from a sentinel at 1234 nm');
  uok(textsU(RECU).some(t=>t.indexOf('MW/m²/µm')>=0&&t.indexOf('µm,')>=0),'the point’s value label is drawn');
  uok(RO().indexOf('graph values')>=0,'the readout lists the graph values');
  idleU('idle before the point drag');
  const M=buildModel(), b=specGeo(RECU,1400,820,M).b, gx=b.x+b.w*ST.gvNm/M.S.xmax, gy=b.y1-b.h*M.S.gv.M/M.S.ymax;
  NODESU.scene.fire('pointerdown',{clientX:gx,clientY:gy});
  uok(DRAG.what==='gv','pointer-down ON the point grabs it');
  idleU('proven idle after the grab');
  NODESU.scene.fire('pointermove',{clientX:b.x+b.w/3,clientY:gy,buttons:1});
  uok(Math.abs(ST.gvNm-M.S.xmax/3)<1e-6,'the point moved to a third of the axis ('+ST.gvNm.toFixed(3)+' nm)');
  RECU=makeRecU(); pumpU(2); uok(geomU(RECU).length>200,'and the view repainted through the loop');
  uok(ST.gvCue===true,'the cue arrows stay up during the drag');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null&&ST.gvCue===false,'released; the cue arrows go, as PhET’s do');
  uok(RO().indexOf(um(M.S.xmax/3))>=0,'the readout prints the dragged wavelength');
  const s=sliderU('T, kelvin'); s.value='4000'; s.fire('input');
  uok(Math.abs(ST.gvNm-peakNm(4000))<1e-9,'a new temperature sends the point back to the peak (PhET)'); }

/* ---- the slider repaints at once; the preset chips ---- */
idleU('idle before the slider test');
{ const s=sliderU('T, kelvin'); uok(!!s,'found the temperature slider');
  RECU=makeRecU(); s.value='7250'; s.fire('input');
  uok(ST.T===7250,'the slider set 7250 K'); uok(RECU.ops.length>100,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(RO().indexOf('7250 K')>=0,'the readout followed');
  for(const [nm,T] of [['Earth',250],['Light Bulb',3000],['Sirius A',9950],['Sun',5800]]){
    const c=chipU(nm,4); uok(!!c,'found the '+nm+' chip'); c.fire('click');
    uok(ST.T===T,nm+' sets '+T+' K'); uok(c.className==='chip on','and lights its chip');
    uok(RO().indexOf(nm)>=0,'the readout names '+nm); }
  uok(chipU('Earth',4).className==='chip','the other chips go dark'); }

/* ---- labels and intensity ---- */
{ const cl=findLabelledU('labels'), ci=findLabelledU('intensity'); uok(!!cl&&!!ci,'found the labels and intensity checkboxes');
  idleU('idle before labels');
  RECU=makeRecU(); cl.checked=true; cl.fire('change'); uok(ST.labels===true,'labels on');
  const tl=textsU(RECU); uok(tl.indexOf('Visible')>=0&&tl.indexOf('Ultraviolet')>=0&&tl.indexOf('Infrared')>=0,'the band names are drawn');
  RECU=makeRecU(); ci.checked=true; ci.fire('change'); uok(ST.inten===true,'intensity on');
  uok(textsU(RECU).some(t=>t.indexOf('area σT⁴')===0),'the area label is drawn'); uok(RO().indexOf('class="v good">6.42×10⁷')>=0,'and the readout highlights sigma T^4');
  cl.checked=false; cl.fire('change'); RECU=makeRecU(); pumpU(1); ci.checked=false; ci.fire('change'); uok(!ST.labels&&!ST.inten,'both off again'); }

/* ---- saved curves ---- */
{ const eb=buttonU('erase saved'); uok(!!eb&&eb.disabled===true,'erase is disabled with nothing saved');
  uok(clickButtonU('save curve'),'save curve'); uok(SAVED.length===1&&SAVED[0]===5800,'the Sun is saved'); uok(eb.disabled===false,'erase is enabled');
  chipU('Light Bulb',4).fire('click'); clickButtonU('save curve'); chipU('Sirius A',4).fire('click'); clickButtonU('save curve');
  uok(SAVED.join(',')==='3000,9950','PhET keeps the two newest ('+SAVED.join(',')+')');
  uok(RO().indexOf('newer (solid)')>=0&&RO().indexOf('older (dashed)')>=0,'the readout lists both');
  idleU('idle with saved curves');
  RECU=makeRecU(); clickButtonU('erase saved'); uok(SAVED.length===0&&eb.disabled===true,'erase clears them and disables itself'); uok(RECU.ops.length>100,'and repaints'); }

/* ---- zoom, both ladders, and fit ---- */
{ chipU('Sun',4).fire('click'); idleU('idle before zoom');
  const zi=buttonU('λ: zoom in'), zo=buttonU('λ: zoom out'), pi=buttonU('power: zoom in'), po=buttonU('power: zoom out'), fb=buttonU('fit the axes');
  uok(!!zi&&!!zo&&!!pi&&!!po&&!!fb,'found the five zoom buttons');
  uok(fb.disabled===true,'fit is disabled: the Sun is already framed');
  RECU=makeRecU(); zi.fire('click'); uok(ST.ix===1&&RECU.ops.length>100,'λ zoom in: 1.5 µm, repainted');
  zi.fire('click'); uok(ST.ix===0&&zi.disabled===true,'down to 0.75 µm, where zoom-in disables');
  for(let k=0;k<6;k++) zo.fire('click'); uok(ST.ix===6&&zo.disabled===true,'out to 48 µm, where zoom-out disables');
  RECU=makeRecU(); pi.fire('click'); uok(ST.iy===9&&RECU.ops.length>50,'power zoom in: 20');
  uok(RO().indexOf('0&ndash;20 MW')>=0||RO().indexOf('0–20 MW')>=0,'the readout prints the new axis');
  for(let k=0;k<12;k++) pi.fire('click'); uok(ST.iy===0&&pi.disabled===true,'down to 1.024e-5, where zoom-in disables');
  for(let k=0;k<12;k++) po.fire('click'); uok(ST.iy===12&&po.disabled===true,'up to 2500, where zoom-out disables');
  uok(fb.disabled===false,'fit is enabled when the axes are off');
  chipU('Earth',4).fire('click'); fb.fire('click'); uok(ST.ix===6&&ST.iy===1,'fit the axes frames the Earth: 48 um x 5.12e-5');
  uok(fb.disabled===true,'and then disables'); uok(RO().indexOf('11.59 µm')>=0,'the Earth’s peak, 11.59 um, is in the readout'); }

/* ---- the other views: the older laws' checkboxes; the pointer is ignored off the spectrum ---- */
NODESU.tabs.children[4].fire('click'); idleU('the limits view idles');
{ const cr=findLabelledU('Rayleigh–Jeans (1900–05)'), cw=findLabelledU('Wien’s approximation (1896)'); uok(!!cr&&!!cw,'found the two older-law checkboxes');
  RECU=makeRecU(); pumpU(1); cr.checked=false; cr.fire('change'); const g1=geomU(RECU);
  uok(ST.rj===false&&g1.length>100,'Rayleigh–Jeans off, repainted');
  RECU=makeRecU(); cw.checked=false; cw.fire('change'); const g2=geomU(RECU);
  uok(ST.wien===false&&g2!==g1,'Wien off draws a different picture');
  cr.checked=true; cr.fire('change'); cw.checked=true; cw.fire('change'); uok(ST.rj&&ST.wien,'both back on'); }
NODESU.tabs.children[2].fire('click'); idleU('the peak view idles');
NODESU.scene.fire('pointerdown',{clientX:100,clientY:600}); NODESU.scene.fire('pointermove',{clientX:100,clientY:300,buttons:1});
RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]'&&DRAG.what===null,'the peak view ignores the pointer, as designed'); NODESU.scene.fire('pointerup',{});

/* ---- keys ---- */
{ const T0=ST.T; idleU('idle before the keys');
  keyU('ArrowUp'); uok(ST.T===T0+50,'up adds 50 K'); idleU('idle after the key’s repaint');
  RECU=makeRecU(); keyU('ArrowDown'); uok(ST.T===T0&&RECU.ops.length>=63,'down takes it back and repaints at once ('+RECU.ops.length+' ops)');
  keyU('ArrowDown'); uok(ST.T===Math.max(200,T0-50),'and down again (clamped at 200 K)');
  keyU('1'); uok(ST.view==='spec','1 is the spectrum'); keyU('5'); uok(ST.view==='limits','5 is the limits'); keyU('2'); uok(ST.view==='star','2 is the star');
  keyU('9'); uok(ST.view==='star','9 is not a view'); }

/* ---- every control at its extremes, then reset all against a fully disturbed state ---- */
let ctlErrU=null;
try{ const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===6,'the panel has its 1 slider and 5 checkboxes ('+inputs.length+')');
  for(const v of [0,1,2,3,4]){ NODESU.tabs.children[v].fire('click');
    for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); uok(NODESU.errbox.style.display!=='block','tab '+v+': slider at '+x+' draws without error'); } }
    assertCleanU(RECU,'after the control sweep, tab '+v); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* disturb EVERY kind of state reset claims to restore */
  NODESU.tabs.children[0].fire('click');
  sliderU('T, kelvin').value='700'; sliderU('T, kelvin').fire('input');
  clickButtonU('save curve'); clickButtonU('λ: zoom out'); clickButtonU('power: zoom in');
  for(const nm of ['graph values','labels','intensity']){ const c=findLabelledU(nm); c.checked=true; c.fire('change'); }
  ST.gvNm=1234; ST.gvCue=false; ST.rj=false; ST.wien=false;
  uok(ST.T===700&&SAVED.length===1&&ST.ix!==2&&ST.iy!==10&&ST.gv&&ST.labels&&ST.inten,'the state is disturbed');
  idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  uok(ST.T===5800&&ST.ix===2&&ST.iy===10&&!ST.gv&&!ST.labels&&!ST.inten&&ST.gvCue&&ST.rj&&ST.wien&&SAVED.length===0,'reset all restores every default');
  uok(Math.abs(ST.gvNm-peakNm(5800))<1e-9,'Graph Values back at the peak');
  uok(RECU.ops.length>100,'reset repaints'); uok(findLabelledU('labels').checked===false,'the checkboxes follow');
  uok(sliderU('T, kelvin').value==5800,'the slider follows'); uok(chipU('Sun',4).className==='chip on','the Sun chip lights');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
