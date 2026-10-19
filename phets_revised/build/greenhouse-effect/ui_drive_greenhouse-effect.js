/* ============ UI drive test for greenhouse-effect.html ==================== *
 * DOM-stub pattern (lineage: projects/simulations/build_buoy/ui_drive_bu.js via
 * build/waves-intro/ui_drive_waves-intro.js, which carries the innerHTML ->
 * textContent fix the shared tools/ui_drive.js still lacks).  The three sky
 * views animate — the ground and the sheets are integrated every frame — so
 * every idle-first test PAUSES the clock and proves the loop quiet before it
 * acts.  One custom pointer action (PhET's flux-meter sensor), every tab, every
 * visible slider at its ends, every checkbox, every chip, every button, the
 * keys, resize, and reset-all against a fully disturbed state.                */
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
    fill(){ if(c._p&&c._p.length) ops.push(['f',String(st.fillStyle)].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h,String(st.fillStyle)]);},
    strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
    fillText(t,x,y){ops.push(['t',String(t),Math.round(x),Math.round(y)]);}, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||'');
      return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
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
    fire(k,ev){ for(const f of (this._h[k]||[]))
      f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
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
/* match the WHOLE label, never a substring: sliderU('absorb') would find both "absorbing
   sheets" and "infrared absorbance" (Known-bad, build_lagr/ui_drive_lp.js) */
function sliderU(needle){ const all=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) all.push(ch);
    walk(ch); } };
  walk(NODESU.panel);
  const shown=all.filter(r=>!r.hidden);
  return (shown[0]||all[0]||{children:[]}).children[1]||null; }
function rowOf(inp){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.children&&ch.children.indexOf(inp)>=0) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
/* the chip finder checks the row's ARITY as well as the text (Known-bad, lenses.html) */
function chipU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity)
      for(const c of ch.children) if(c.textContent===label) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+' ('+RECU.ops.length+' ops)'); }
function isShown(el){ const chain=[];
  const walk=p=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
function pause(){ if(ST.running) keyU(' '); }
/* the window geometry the scene itself uses, so a pointer test hits what is drawn */
function winU(){ return skyLayout(RECU,1400,820,buildModel(),CAP_WAVES,CAP_WAVES_S); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built');
uok(NODESU.panel.children.length===7,'the control panel has its seven groups ('+NODESU.panel.children.length+')');
uok(RO().length>400,'the readout rendered ('+RO().length+' chars)');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&
    (NODESU.eqbar.innerHTML||'').indexOf('a<sub>i</sub>/(2 &minus; a<sub>i</sub>)')>=0,
    'the equation bar carries the law, no NaN');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,
    'the panel carries the PhET credit line');
uok((NODESU.panel.textContent||'').indexOf('greenhouse-effect_en.html 1.3.13')>=0,
    'and names the original it was read from');
{ const bad=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(['LABEL','BUTTON','H3'].indexOf(ch.tagName)>=0&&entReU.test(ch.textContent||''))
      bad.push(ch.tagName+': '+ch.textContent);
    walk(ch); } };
  walk(NODESU.panel);
  uok(!bad.length,'no HTML entity reaches a label, button or heading as literal text'+(bad.length?' ('+bad[0]+')':'')); }

/* ---- every tab draws, differently, cleanly ---- */
pause();
/* about 70 % of what each tab emits at 1400 x 820 on its first draw; measured with
   UI_DIAG (python3 jsrun.py ui_drive_greenhouse-effect.js osa diag) */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[60,40,50,40,40];
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while paused / static');
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');

/* ---- the clock: PhET's own thermal relaxation ---- */
tab(0);
{ clickButtonU('cold start');
  uok(TH.conc.Tg===GH.TMIN_NIGHT,'a cold start puts the ground at PhET’s 245 K night floor');
  keyU(' '); uok(ST.running,'space starts the clock');
  const t0=TH.conc.Tg; RECU=makeRecU(); pumpU(60);
  uok(TH.conc.Tg>t0+15,'sixty frames warm the ground by more than 15 K ('+fmt(TH.conc.Tg-t0,2)+' K)');
  uok(Math.abs(TH.conc.t-1)<1e-9,'and advance the model clock by exactly one second');
  uok(RECU.ops.length>60,'and the loop repaints as it runs ('+RECU.ops.length+' ops)');
  keyU(' '); uok(!ST.running,'space pauses');
  const t1=TH.conc.Tg; pumpU(20); uok(TH.conc.Tg===t1,'paused: the ground holds');
  idleU('paused: nothing is painted');
  RECU=makeRecU(); clickButtonU('one step');
  uok(TH.conc.Tg!==t1,'"one step" advances one frame even while paused');
  uok(!ST.running,'and leaves the clock paused');
  uok(RECU.ops.length>20,'and repaints at once ('+RECU.ops.length+' ops)');
  RECU=makeRecU(); clickButtonU('jump to equilibrium');
  const s=solveClosed(concAbsorbance(concNow(),GH.N_CONC),
                      (1-concAlbedo())*GH.S_SUN*(ST.cloud?1-CLOUD_REFL:1));
  uok(Math.abs(TH.conc.Tg-s.Tg)<1e-9,'"jump to equilibrium" lands exactly on the closed form');
  uok(RECU.ops.length>20,'and repaints');
  keyU('e'); uok(Math.abs(TH.conc.Tg-s.Tg)<1e-9,'the e key does the same');
  clickButtonU('cold start'); uok(TH.conc.Tg===GH.TMIN_NIGHT&&PH.list.length===0,
    '"cold start" resets the temperature and empties the photons'); }

/* ---- the sun ---- */
{ clickButtonU('jump to equilibrium'); const warm=TH.conc.Tg;
  keyU('s'); uok(!ST.sun,'s switches the sun off');
  uok(buildModel().S.F===0,'and no flux is absorbed');
  ST.running=true; pumpU(400); ST.running=false;
  uok(TH.conc.Tg<warm,'the ground cools with the sun off ('+fmt(TH.conc.Tg,1)+' K)');
  uok(TH.conc.Tg>=GH.TMIN_NIGHT-1e-9,'but never below PhET’s 245 K night floor');
  keyU('s'); uok(ST.sun,'s switches it back on');
  clickButtonU('jump to equilibrium');
  uok(Math.abs(TH.conc.Tg-warm)<1e-9,'and the equilibrium is the one it left'); }

/* ---- a slider with the full treatment: proven idle, fire, drawn at once ---- */
pause();
idleU('idle before the concentration slider');
{ const s=sliderU('concentration c'); uok(!!s&&isShown(s),'the concentration slider is on show');
  RECU=makeRecU(); s.value='1'; s.fire('input');
  uok(ST.conc===1,'it sets c = 1');
  uok(RECU.ops.length>40,'and the view redrew at once ('+RECU.ops.length+' ops)');
  clickButtonU('jump to equilibrium');
  uok(RO().indexOf('309.13')>=0||RO().indexOf('35.98')>=0||RO().indexOf('96.76')>=0,
      'the readout follows to the hottest reachable state');
  s.value='0'; s.fire('input'); clickButtonU('jump to equilibrium');
  const bare=teff((1-GH.ALB_MEADOW)*GH.S_SUN);
  uok(Math.abs(TH.conc.Tg-bare)<1e-9,'at c = 0 the ground is a bare rock at its effective temperature');
  s.value='0.5'; s.fire('input'); }

/* ---- the custom action: PhET's flux-meter sensor, dragged through the loop ---- */
{ idleU('idle before the probe drag');
  const L=winU(), mp=skyMapOf(L.win), y0=mp.yOf(PROBE.z);
  /* NOT on the sensor's exact pixel: a hit test narrowed to zero still catches an exactly
     centred click, and that mutant survived a 90-mutant sweep until this moved 6 px off */
  NODESU.scene.fire('pointerdown',{clientX:L.win.x+40,clientY:y0+6});
  uok(DRAG.what==='probe','pointer-down 6 px from the sensor grabs it');
  NODESU.scene.fire('pointerup',{});
  NODESU.scene.fire('pointerdown',{clientX:L.win.x+40,clientY:y0+40});
  uok(DRAG.what===null,'but 40 px away does not');
  NODESU.scene.fire('pointerup',{});
  NODESU.scene.fire('pointerdown',{clientX:L.win.x+40,clientY:y0+6});
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
  uok(gA.length>400,'the grab repaints through the frame loop');
  idleU('and drains (proven idle)');
  const yWant=mp.yOf(40000);
  NODESU.scene.fire('pointermove',{clientX:L.win.x+40,clientY:yWant,buttons:1});
  uok(Math.abs(PROBE.z-40000)<1,'the sensor follows the pointer to 40 km ('+fmt(PROBE.z,0)+' m)');
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
  uok(gB.length>400&&gB!==gA,'the move repaints a DIFFERENT picture through the loop');
  uok(RO().indexOf('40.00 km')>=0,'and the readout prints the new altitude');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  /* the reading at the top of the atmosphere is the one the physics fixes */
  NODESU.scene.fire('pointerdown',{clientX:L.win.x+40,clientY:mp.yOf(40000)});
  NODESU.scene.fire('pointermove',{clientX:L.win.x+40,clientY:L.win.y-50,buttons:1});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(PROBE.z-GH.TOP)<1,'dragged past the top it clamps at 50 km');
  /* the sensor reads the LIVE model, so settle it first: at equilibrium the flux leaving
     the top of the atmosphere is exactly the sunlight the ground absorbed */
  clickButtonU('jump to equilibrium');
  { const M=buildModel(); uok(Math.abs(M.S.probe.D)<1e-9,'where nothing comes down');
    uok(Math.abs(M.S.probe.U-M.S.F)<1e-6,'and, settled, exactly F goes up'); }
  idleU('idle before the miss');
  NODESU.scene.fire('pointerdown',{clientX:L.win.x+40,clientY:mp.yOf(5000)});
  uok(DRAG.what===null,'empty sky grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and paints nothing');
  NODESU.scene.fire('pointerup',{});
  PROBE.z=20000; }

/* ---- the concentration panel: by value and by date ---- */
{ uok(!!chipU('by date',2)&&!!chipU('by concentration',2),'the two concentration modes are chips');
  chipU('by date',2).fire('click'); uok(ST.mode==='date','by date');
  uok(isShown(chipU('1750',4))&&!isShown(sliderU('concentration c')),
      'which shows the four dates and hides the slider');
  for(const [nm,c] of [['ice age',0.625],['1750',0.7147],['1950',0.7182],['2020',0.7446]]){
    chipU(nm,4).fire('click');
    uok(Math.abs(concNow()-c)<1e-12,nm+' is PhET’s c = '+c);
    clickButtonU('jump to equilibrium');
  }
  chipU('ice age',4).fire('click');
  uok(Math.abs(buildModel().S.albedo-GH.ALB_GLACIER)<1e-15,
      'the ice age puts the glaciated albedo on the ground (PhET)');
  chipU('1750',4).fire('click');
  uok(Math.abs(buildModel().S.albedo-GH.ALB_MEADOW)<1e-15,'and 1750 the green meadow');
  clickButtonU('jump to equilibrium');
  uok(RO().indexOf('23.33 °C')>=0,'the readout prints PhET’s 1750 surface, 23.33 °C');
  uok(RO().indexOf('277 ppm')>=0,'with PhET’s 277 ppm of CO2');
  chipU('kelvin',3).fire('click'); uok(ST.unit==='K','kelvin');
  uok(RO().indexOf('296.48 K')>=0,'which is 296.48 K');
  chipU('fahrenheit',3).fire('click');
  uok(RO().indexOf('74.00 °F')>=0,'and 74.00 °F');
  chipU('celsius',3).fire('click');
  chipU('by concentration',2).fire('click');
  uok(isShown(sliderU('concentration c'))&&!isShown(chipU('1750',4)),'back to the slider'); }

/* ---- the cloud ---- */
{ const cb=findLabelledU('a cloud (reflects 12.5 %)'); uok(!!cb&&isShown(cb),'the cloud box is on show');
  clickButtonU('jump to equilibrium'); const warm=TH.conc.Tg;
  cb.checked=true; cb.fire('change'); clickButtonU('jump to equilibrium');
  uok(TH.conc.Tg<warm,'a cloud cools the ground ('+fmt(warm-TH.conc.Tg,2)+' K)');
  uok(Math.abs(buildModel().S.F-(1-GH.ALB_MEADOW)*GH.S_SUN*(1-0.125))<1e-9,
      'by taking exactly 12.5 % of the sunlight');
  cb.checked=false; cb.fire('change'); }

/* ---- the photons ---- */
tab(1); pause();
{ uok(isShown(findLabelledU('more photons')),'the "more photons" box is on show for the photons view');
  clickButtonU('cold start'); clickButtonU('jump to equilibrium');
  ST.running=true; pumpU(240); ST.running=false;
  uok(PH.list.length>0,'four seconds of photons leaves some in flight ('+PH.list.length+')');
  uok(PH.emitted>50,'the ground has emitted infrared photons ('+PH.emitted+')');
  uok(PH.crossings>0&&PH.absorbed>0,'some have been absorbed by the sheets ('+PH.absorbed+' of '+PH.crossings+')');
  const M=buildModel();
  uok(Math.abs(M.S.pExact-M.S.s.esc)<1e-12,'the exact escape chance is the flux ratio');
  uok(Math.abs(M.S.mc.p-M.S.pExact)<4*Math.sqrt(M.S.pExact*(1-M.S.pExact)/M.S.mc.m),
      'and the 20000-walk Monte Carlo is within 4 sigma of it');
  const drawn0=M.S.counts.drawn;
  const cb=findLabelledU('more photons'); cb.checked=true; cb.fire('change');
  const M2=buildModel();
  uok(M2.S.counts.drawn>drawn0,'"more photons" draws more of them ('+drawn0+' -> '+M2.S.counts.drawn+')');
  uok(M2.S.counts.drawn===PH.list.length,'in fact all of them');
  cb.checked=false; cb.fire('change');
  /* the walk is seeded: the same run repeats exactly */
  const before=JSON.stringify(PH.list.map(p=>[p.x,p.y,p.vx,p.vy]));
  clickButtonU('cold start'); clickButtonU('jump to equilibrium');
  ST.running=true; pumpU(240); ST.running=false;
  uok(JSON.stringify(PH.list.map(p=>[p.x,p.y,p.vx,p.vy]))===before,
      'a seeded generator gives the same photons every run'); }

/* ---- the layer model ---- */
tab(2); pause();
{ uok(isShown(sliderU('absorbing sheets'))&&isShown(sliderU('infrared absorbance'))
      &&isShown(sliderU('solar intensity'))&&isShown(sliderU('surface albedo')),
      'the layer model shows its four sliders');
  uok(!isShown(sliderU('concentration c')),'and not the concentration slider');
  const n=sliderU('absorbing sheets'), a=sliderU('infrared absorbance'),
        i=sliderU('solar intensity'), al=sliderU('surface albedo');
  n.value='0'; n.fire('input'); clickButtonU('jump to equilibrium');
  uok(Math.abs(TH.lm.Tg-teff((1-ST.albedo)*GH.S_SUN*ST.intensity))<1e-9,
      'no sheets: the bare-rock temperature');
  n.value='3'; n.fire('input'); a.value='1'; a.fire('input'); clickButtonU('jump to equilibrium');
  uok(Math.abs(TH.lm.Tg-Math.pow(4,0.25)*teff((1-ST.albedo)*GH.S_SUN*ST.intensity))<1e-9,
      'three black sheets: exactly 4^(1/4) times it');
  i.value='2'; i.fire('input'); clickButtonU('jump to equilibrium');
  uok(Math.abs(TH.lm.Tg-Math.pow(4,0.25)*teff((1-ST.albedo)*GH.S_SUN*2))<1e-9,
      'two suns: the same ladder on a hotter rock');
  i.value='1'; i.fire('input');
  al.value='0.9'; al.fire('input'); clickButtonU('jump to equilibrium');
  uok(TH.lm.Tg>GH.TMIN_LM,'at albedo 0.9 the 125 K floor still does not bind ('+fmt(TH.lm.Tg,1)+' K)');
  al.value='0.3'; al.fire('input');
  a.value='0.5'; a.fire('input'); clickButtonU('jump to equilibrium');
  const M=buildModel();
  uok(Math.abs(M.S.Tsteady-teff((1-0.3)*GH.S_SUN)*Math.pow(1+3*0.5/1.5,0.25))<1e-9,
      'a = 0.5 follows the general law, not the black-sheet one');
  const kb=findLabelledU('sheet temperatures by Kirchhoff');
  uok(!!kb&&isShown(kb),'the Kirchhoff box is on show for the layer model');
  const t0=RO(); kb.checked=true; kb.fire('change');
  uok(RO()!==t0,'ticking it changes the sheet temperatures printed');
  uok(Math.abs(M.S.Skirch[0]/M.S.Ssteady[0]-Math.pow(0.5,-0.25))<1e-12,'by exactly a^(-1/4)');
  kb.checked=false; kb.fire('change');
  const before=buildModel().S.Tsteady;
  uok(Math.abs(before-M.S.Tsteady)<1e-12,'and no flux or surface temperature moved'); }

/* ---- the flux meter and the other display boxes ---- */
tab(0); pause();
{ const fb=findLabelledU('the flux meter'); idleU('idle before the flux meter');
  RECU=makeRecU(); fb.checked=true; fb.fire('change');
  uok(ST.flux,'the flux meter is on');
  uok(textsU(RECU).some(s=>s.indexOf('the flux meter')>=0||s.indexOf('flux')>=0),
      'and a flux panel is drawn');
  const withFlux=RECU.ops.length;
  RECU=makeRecU(); fb.checked=false; fb.fire('change');
  uok(RECU.ops.length<withFlux,'switching it off draws less ('+RECU.ops.length+' vs '+withFlux+')');
  const bb=findLabelledU('energy balance at the top');
  RECU=makeRecU(); bb.checked=false; bb.fire('change');
  uok(!textsU(RECU).some(s=>s==='top of atmosphere'),'the energy-balance panel can be switched off');
  bb.checked=true; bb.fire('change');
  RECU=makeRecU(); tab(0);
  uok(textsU(RECU).some(s=>s==='top of atmosphere'),'and back on');
  const sb=findLabelledU('the sheet altitudes');
  RECU=makeRecU(); sb.checked=true; sb.fire('change');
  uok(RECU.ops.length>0&&ST.sheets,'the sheet altitudes draw');
  sb.checked=false; sb.fire('change'); }

/* ---- the analysis views ---- */
tab(3);
{ uok(isShown(sliderU('absorbing sheets')),'the ladder view keeps the sheet sliders (they set its marker)');
  uok(!isShown(findLabelledU('the flux meter')),'and drops the display boxes');
  RECU=makeRecU(); tab(3);
  uok(textsU(RECU).some(s=>s.indexOf('the ladder')>=0),'the ladder panel is titled');
  uok(textsU(RECU).some(s=>s.indexOf('the real Earth')>=0),'and names the real Earth');
  const before=RO();
  const a=sliderU('infrared absorbance'); a.value='0.3'; a.fire('input');
  uok(RO()!==before,'moving the absorbance changes the readout');
  assertCleanU(RECU,'the ladder'); }
tab(4);
{ RECU=makeRecU(); tab(4);
  const tx=textsU(RECU);
  uok(tx.indexOf('1750')>=0&&tx.indexOf('2020')>=0&&tx.indexOf('ice age')>=0,
      'the record view names PhET’s dates');
  uok(tx.indexOf('277')>=0&&tx.indexOf('413')>=0,'and prints their CO2 in the table');
  uok(RO().indexOf('+1.32 K')>=0||RO().indexOf('1.32')>=0,'the readout carries the 1750 to 2020 difference');
  assertCleanU(RECU,'the record'); }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='waves','1 is the waves'); keyU('3'); uok(ST.view==='layers','3 is the layers');
  keyU('5'); uok(ST.view==='record','5 is the record');
  keyU('9'); uok(ST.view==='record','9 is not a view');
  keyU('2'); uok(ST.view==='photons','2 is the photons'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length>=13,'the panel has its sliders and checkboxes ('+inputs.length+')');
  for(let v=0;v<5;v++){ tab(v); pause();
    let touched=0;
    for(const inp of inputs){
      if(!isShown(inp)) continue; touched++;
      if(inp.type==='checkbox'){
        if(inp===findLabelledU('time runs')) continue;
        inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change');
        continue; }
      for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); }
      uok(NODESU.errbox.style.display!=='block','tab '+v+': '+
          (rowOf(inp)&&rowOf(inp).children[0]?rowOf(inp).children[0].textContent:'a slider')+
          ' at its ends draws without error'); }
    uok(touched>=2,'tab '+v+' has controls on show ('+touched+')');
    RECU=makeRecU(); tab(v); assertCleanU(RECU,'tab '+v+' after the sweep'); }
  for(const f of (WINHU.resize||[])) f();
  uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
if(NODESU.errbox.style.display==='block') console.log('ERRBOX: '+String(NODESU.errbox.textContent).replace(/\n/g,' | '));

/* ---- the panel shows each view its own groups ---- */
{ const g=NODESU.panel.children;
  tab(0); uok(g[0].hidden===false&&g[1].hidden===true&&g[3].hidden===false,
    'a concentration view shows the gas group and the clock, not the sheets');
  tab(2); uok(g[0].hidden===true&&g[1].hidden===false,'the layer model shows the sheets, not the gas');
  tab(3); uok(g[1].hidden===false&&g[3].hidden===true,'the ladder keeps the sheets and drops the clock');
  tab(4); uok(g[0].hidden===false&&g[1].hidden===true,'the record keeps the gas group');
  tab(0); }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(2); pause();
  sliderU('absorbing sheets').value='3'; sliderU('absorbing sheets').fire('input');
  sliderU('infrared absorbance').value='0.3'; sliderU('infrared absorbance').fire('input');
  sliderU('solar intensity').value='2'; sliderU('solar intensity').fire('input');
  sliderU('surface albedo').value='0.9'; sliderU('surface albedo').fire('input');
  for(const nm of ['the flux meter','the sheet altitudes','sheet temperatures by Kirchhoff']){
    const c=findLabelledU(nm); c.checked=true; c.fire('change'); }
  const bb=findLabelledU('energy balance at the top'); bb.checked=false; bb.fire('change');
  ST.mode='date'; ST.date='y2020'; ST.cloud=true; ST.unit='F'; ST.morePhotons=true;
  PROBE.z=45000;
  ST.running=true; pumpU(120); ST.running=false;
  uok(ST.nLayers===3&&ST.absorb===0.3&&ST.intensity===2&&ST.albedo===0.9&&ST.flux&&ST.kirch&&!ST.balance,
      'the state is disturbed');
  uok(TH.lm.Tg!==GH.TMIN_LM,'and the model has run');
  idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true, firstBad='';
  for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]){ same=false; if(!firstBad) firstBad=k; }
  uok(same,'reset all restores every default'+(same?'':' (first: '+firstBad+')'));
  uok(PROBE.z===PROBE0.z,'and the flux sensor’s altitude');
  uok(TH.conc.Tg===GH.TMIN_NIGHT&&TH.lm.Tg===GH.TMIN_LM&&TH.conc.t===0,
      'and both thermal states, back at their cold starts');
  uok(PH.list.length===0&&PH.emitted===0,'and the photon population');
  uok(RECU.ops.length>=6,'reset repaints ('+RECU.ops.length+' ops)');
  uok(findLabelledU('the flux meter').checked===false,'the checkboxes follow');
  uok(chipU('by concentration',2).className==='chip on'&&chipU('celsius',3).className==='chip on',
      'the chips follow');
  uok(Math.abs(+sliderU('infrared absorbance').value-DEFAULTS.absorb)<1e-12,'the sliders follow');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
