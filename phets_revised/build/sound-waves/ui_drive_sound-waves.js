/* ============ UI drive test for sound-waves.html =========================== *
 * DOM-stub pattern, the harness head taken unchanged from
 * build/waves-intro/ui_drive_waves-intro.js (which carries the innerHTML ->
 * textContent fix).  The five room views animate, so every idle-first test
 * PAUSES the clock first; the analysis view never animates.  Four custom
 * pointer actions (PhET's speaker button, the listener, the second speaker and
 * PhET's ruler), every tab, every visible slider at its ends, every checkbox,
 * every chip, every button, the keys, resize, the tone's audio layer against a
 * stub AudioContext, and reset-all against a fully disturbed state.           */
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
    clip:P, fillRect(x,y,w,h){ops.push(['r',x,y,w,h,String(st.fillStyle)]);}, strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
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
/* a stub AudioContext: the tone's samples are computed by the sim, so the harness can check
   exactly what would be played without any audio hardware */
const ALOG={ctx:0,buffers:[],started:0,stopped:0,gain:null,last:null};
globalThis.AudioContext=function(){
  ALOG.ctx++;
  this.sampleRate=44100; this.state='running'; this.currentTime=0; this.destination={};
  this.createGain=()=>{ const g={gain:{value:-1},connect(){}}; ALOG.gain=g; return g; };
  this.createBuffer=(ch,len,sr)=>{ const d=new Float32Array(len);
    const b={length:len,sampleRate:sr,numberOfChannels:ch,getChannelData:()=>d}; ALOG.buffers.push(b); return b; };
  this.createBufferSource=()=>{ const s={buffer:null,loop:false,connect(){},
    start(){ ALOG.started++; ALOG.last=s; },stop(){ ALOG.stopped++; }}; return s; };
  this.resume=()=>{};
};
let TNOWU=0;
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(needle){ const out=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') out.push(c2);
    walk(ch); } };
  walk(NODESU.panel); return out[0]||null; }
/* a finder that matches on a label must take the VISIBLE control: several groups are hidden
   per view and a hidden row would otherwise be driven instead (Known-bad) */
function sliderU(needle){ const all=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===needle) all.push(ch);
    walk(ch); } };
  walk(NODESU.panel);
  const shown=all.filter(r=>!r.hidden);
  return (shown[0]||all[0]||{children:[]}).children[1]||null; }
function rowOf(inp){ let hit=null; const walk=n=>{ for(const ch of n.children||[]){ if(ch.children&&ch.children.indexOf(inp)>=0) hit=ch; walk(ch); } }; walk(NODESU.panel); return hit; }
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
function isShown(el){ const chain=[];
  const walk=p=>{ for(const ch of p.children||[]){ if(ch===el) return true; if(walk(ch)){ chain.push(ch); return true; } } return false; };
  walk(NODESU.panel); if(el.hidden) return false; for(const c of chain) if(c.hidden) return false; return true; }
const RO=()=>NODESU.readout.innerHTML;
function tab(i){ NODESU.tabs.children[i].fire('click'); }
function pause(){ if(ST.running) keyU(' '); }

function boxU(){ const M=buildModel(), G=boxGeo(RECU,1400,820,M); return {M,G,sq:G.sq}; }
function screenXY(sq,x,y){ return {clientX:mx(sq,x),clientY:my(sq,y)}; }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.panel.children.length===10,'the control panel has its ten groups ('+NODESU.panel.children.length+')');
uok(RO().length>400,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0&&(NODESU.eqbar.innerHTML||'').indexOf('&lambda; = v/f')>=0,
    'the equation bar carries λ = v/f, no NaN');
uok(RO().indexOf('0.624 m')>=0,'the readout prints λ = 343/550 = 0.624 m off the model');
uok(RO().indexOf('343.0 m/s')>=0,'and the speed of sound');
uok((NODESU.panel.textContent||'').indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
/* every control built from TEXT NODES (labels, buttons, chips, headings) must carry literal
   glyphs: a browser renders an entity written there verbatim.  The .tag and .src blocks are
   set through innerHTML, where entities are correct — and the stub does not decode them, so
   they are deliberately not walked here. */
{ const bad=[];
  const walk=n=>{ for(const ch of n.children||[]){
    if(['LABEL','BUTTON','H3'].indexOf(ch.tagName)>=0&&entReU.test(ch.textContent||'')) bad.push(ch.tagName+': '+ch.textContent);
    walk(ch); } };
  walk(NODESU.panel);
  uok(!bad.length,'no HTML entity reaches a label, button or heading as literal text'+(bad.length?' ('+bad[0]+')':'')); }

/* ---- every tab draws, differently, cleanly ---- */
pause();
/* 70 % of what each tab emits at 1400 x 820 on its FIRST draw, which is a room with no sound in
   it yet — a floor taken from a running room would punish a view for starting honestly, and one
   taken from a field's contrast classes would punish these views for batching */
const FLOORSU=(typeof UI_FLOORS!=='undefined')?UI_FLOORS:[13,13,20,22,14,40];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tab(i);
  if(typeof UI_DIAG!=='undefined') console.log('TABOPS '+i+' '+RECU.ops.length);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
  idleU('tab '+i+' paints nothing while paused / static');
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- the clock: the model time PhET's time scale asks for, and only on a room view ---- */
tab(0); keyU(' '); uok(ST.running,'space starts the clock');
{ const n0=RUN.n; RECU=makeRecU(); pumpU(60);
  const want=AIR.phetTimeScale/RUN.dt;
  uok(Math.abs((RUN.n-n0)-want)<=2,'sixty frames advance the room '+fmt(want,1)+' steps, PhET’s 4.84 ms of model time ('+(RUN.n-n0)+')');
  uok(Math.abs(RUN.t-n0*RUN.dt-AIR.phetTimeScale)<3*RUN.dt,'i.e. one wall second is 4.84 ms in the room');
  uok(RECU.ops.length>60,'and the loop repaints as it runs');
  chipU('slow',2).fire('click'); const n1=RUN.n; pumpU(60);
  uok(Math.abs((RUN.n-n1)-want/2)<=2,'slow runs at half that ('+(RUN.n-n1)+')');
  chipU('normal',2).fire('click'); uok(chipU('normal',2).className==='chip on','the normal chip lights');
  keyU(' '); uok(!ST.running,'space pauses'); const n2=RUN.n; pumpU(20); uok(RUN.n===n2,'paused: no steps');
  idleU('paused: the room paints nothing');
  const cb=findLabelledU('time runs'); uok(!!cb&&cb.checked===false,'the "time runs" box follows the key');
  RECU=makeRecU(); clickButtonU('one step'); uok(RUN.n===n2+1,'one step is exactly one lattice step');
  uok(RECU.ops.length>20,'and repaints at once');
  tab(5); const n3=RUN.n; ST.running=true; pumpU(20); uok(RUN.n===n3,'the analysis view does not run the room');
  ST.running=false; tab(0); }
runFor(240);

/* ---- a slider with the full treatment: proven idle, fire, drawn at once ---- */
idleU('idle before the slider test');
{ const s=sliderU('frequency'); uok(!!s&&isShown(s),'the frequency slider is on show');
  RECU=makeRecU(); s.value='1000'; s.fire('input');
  uok(ST.f===1000&&RUN.f===1000,'it sets 1000 Hz on the run');
  uok(RECU.ops.length>30,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(RO().indexOf('0.343 m')>=0,'the readout follows: λ = 343/1000 = 0.343 m');
  uok(RUN.lat.u.some(v=>v!==0),'a new frequency keeps the sound already in the room');
  s.value='550'; s.fire('input');
  const a=sliderU('amplitude'); uok(!!a&&isShown(a),'the amplitude slider is on show');
  a.value='3'; a.fire('input'); uok(RUN.A===3,'amplitude 3 reaches the run');
  a.value='5'; a.fire('input'); }

/* ---- custom action 1: PhET's speaker button, through the frame loop ---- */
{ idleU('idle before the button');
  const {M,sq}=boxU(), g=speakerGeo(sq,M,0);
  uok(sourceActive(RUN),'the speaker is running');
  NODESU.scene.fire('pointerdown',{clientX:g.btn.x,clientY:g.btn.y});
  uok(!sourceActive(RUN),'a click on the speaker’s button switches it off');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'and the picture is repainted through the loop');
  NODESU.scene.fire('pointerup',{});
  idleU('drained (proven idle)');
  NODESU.scene.fire('pointerdown',{clientX:g.btn.x,clientY:g.btn.y});
  uok(sourceActive(RUN)&&RUN.phi===0,'clicking again switches it on and restarts the phase');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU)!==gA&&geomU(RECU).length>200,'which draws a DIFFERENT picture');
  NODESU.scene.fire('pointerup',{});
  keyU('p'); uok(!sourceActive(RUN),'the p key presses the same button');
  keyU('p'); uok(sourceActive(RUN),'and again'); }

/* ---- custom action 2: the listener, dragged through the frame loop ---- */
{ uok(ST.listener,'the listener is on by default');
  idleU('idle before the listener drag');
  const {sq}=boxU(), L0=TOOLS.listener.slice();
  NODESU.scene.fire('pointerdown',screenXY(sq,L0[0],L0[1]));
  uok(DRAG.what==='listener','pointer-down on the listener grabs it');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'the grab repaints through the loop');
  idleU('and drains (proven idle)');
  NODESU.scene.fire('pointermove',Object.assign(screenXY(sq,7.5,2.5),{buttons:1}));
  uok(Math.abs(TOOLS.listener[0]-7.5)<1e-9&&Math.abs(TOOLS.listener[1]-2.5)<1e-9,'the listener follows the pointer');
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU); uok(gB.length>200&&gB!==gA,'the move repaints a DIFFERENT picture through the loop');
  NODESU.scene.fire('pointerup',{}); uok(DRAG.what===null,'pointer-up releases');
  uok(RO().indexOf('7.50 m, 2.50 m')>=0,'the readout prints where the listener now stands');
  /* the probe empties when the listener moves through a view change, not on a drag */
  runFor(60);
  uok(buildModel().listener.amp>0,'and it hears something there');
  idleU('idle before the miss');
  NODESU.scene.fire('pointerdown',screenXY(sq,9.7,0.3)); uok(DRAG.what===null,'empty air grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and paints nothing'); NODESU.scene.fire('pointerup',{});
  TOOLS.listener=L0; }

/* ---- custom action 3: PhET's ruler ---- */
{ const cb=findLabelledU('PhET’s 5 m ruler'); uok(!!cb,'found the ruler box'); cb.checked=true; cb.fire('change');
  uok(ST.ruler&&RO().indexOf('ruler, wavelengths on it')>=0,'the ruler shows in the readout');
  idleU('idle before the ruler drag');
  const {M,sq}=boxU(), r=rulerGeo(sq,M);
  NODESU.scene.fire('pointerdown',{clientX:(r.x0+r.x1)/2,clientY:r.y});
  uok(DRAG.what==='ruler','pointer-down on the ruler grabs it');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'the grab repaints through the loop');
  idleU('and drains');
  NODESU.scene.fire('pointermove',Object.assign(screenXY(sq,5,4),{buttons:1}));
  uok(Math.abs(TOOLS.ruler[0]-(5-RULER_LEN/2))<1e-9&&Math.abs(TOOLS.ruler[1]-4)<1e-9,'the ruler follows the pointer by its middle');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200&&geomU(RECU)!==gA,'the move repaints a DIFFERENT picture');
  NODESU.scene.fire('pointerup',{});
  RECU=makeRecU(); tab(1);
  uok(textsU(RECU).indexOf('m')>=0,'the ruler is labelled in metres, PhET’s way (the unit on the last tick)');
  uok(textsU(RECU).indexOf('0')>=0&&textsU(RECU).indexOf('4')>=0,'with its metre marks');
  cb.checked=false; cb.fire('change'); TOOLS.ruler=TOOLS0.ruler.slice(); }

/* ---- the stopwatch and the graph ---- */
{ const cb=findLabelledU('stopwatch'); cb.checked=true; cb.fire('change');
  CLOCK.watch=0; clickButtonU('start / stop the stopwatch'); uok(CLOCK.watchOn,'start');
  ST.running=true; const n0=RUN.n; pumpU(30); ST.running=false;
  uok(Math.abs(CLOCK.watch-(RUN.n-n0)*RUN.dt)<1e-12,'the stopwatch counts the steps’ physical time');
  clickButtonU('start / stop the stopwatch'); uok(!CLOCK.watchOn,'stop');
  const t=CLOCK.watch; ST.running=true; pumpU(10); ST.running=false; uok(CLOCK.watch===t,'stopped, it holds');
  RECU=makeRecU(); clickButtonU('zero it'); uok(CLOCK.watch===0,'zero');
  uok(textsU(RECU).some(s=>s.indexOf('stopwatch 0')===0),'and the canvas shows it');
  cb.checked=false; cb.fire('change');
  const gb=findLabelledU('graph along the speaker’s row'); gb.checked=true; gb.fire('change');
  RECU=makeRecU(); tab(0);
  uok(textsU(RECU).some(s=>s.indexOf('pressure along')>=0),'the graph along the row is drawn when asked for');
  uok(textsU(RECU).some(s=>s.indexOf('λ = 0.624 m')>=0),'and it marks one wavelength on it');
  gb.checked=false; gb.fire('change'); }

/* ---- the parcels ---- */
{ runFor(160); idleU('idle before the parcels');
  RECU=makeRecU(); chipU('air parcels',3).fire('click'); const gp=geomU(RECU);
  uok(ST.look==='particles','the air-parcels chip lights');
  RECU=makeRecU(); chipU('both',3).fire('click'); const gb2=geomU(RECU);
  uok(gp!==gb2&&gp.length>200,'parcels and both draw different pictures');
  chipU('pressure',3).fire('click'); uok(ST.look==='waves','back to the pressure picture'); }

/* ---- pulses and clear ---- */
{ chipU('pulse',2).fire('click'); uok(ST.wave==='pulse','pulse mode');
  uok(!sourceActive(RUN),'which stops the speaker, as PhET’s sound-mode switch does');
  clickButtonU('clear the sound'); uok(RUN.lat.u.every(v=>v===0),'clear the sound empties the lattice');
  clickButtonU('press the speaker button'); uok(RUN.pulse.on,'the button fires a pulse');
  ST.running=true; pumpU(200); ST.running=false;
  uok(!RUN.pulse.on&&RUN.lat.u.some(v=>Math.abs(v)>0.02),'it ends after one period and its ring travels on');
  keyU('r'); uok(RUN.lat.u.every(v=>v===0),'r clears');
  chipU('continuous',2).fire('click'); uok(ST.wave==='cont','back to continuous');
  clickButtonU('press the speaker button'); uok(sourceActive(RUN),'and the button starts it again'); }

/* ---- two speakers: the second one dragged, and the quiet lines ---- */
tab(2); pause(); runFor(400);
{ uok(isShown(sliderU('its height')),'the two-speaker view shows the second speaker’s height');
  uok(isShown(findLabelledU('the quiet hyperbolae'))&&!isShown(findLabelledU('the image speaker and the ray')),
      'and the hyperbolae box, not the wall’s');
  const M0=buildModel();
  uok(M0.two.orders.length===5,'at 550 Hz there are five quiet lines each side ('+M0.two.orders.length+')');
  uok(RO().indexOf('quiet lines each side')>=0,'the readout counts them');
  idleU('idle before the second speaker');
  const {M,sq}=boxU(), s2=speakerGeo(sq,M,1);
  NODESU.scene.fire('pointerdown',{clientX:(s2.x0+s2.x1)/2,clientY:s2.y});
  uok(DRAG.what==='spk2','pointer-down on the second speaker grabs it');
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU); uok(gA.length>200,'the grab repaints through the loop');
  idleU('and drains');
  NODESU.scene.fire('pointermove',Object.assign(screenXY(sq,1,8.4),{buttons:1}));
  uok(Math.abs(ST.spk2y-8.4)<1e-9,'the second speaker follows the pointer in y');
  RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>200&&geomU(RECU)!==gA,'and the pattern is redrawn');
  NODESU.scene.fire('pointerup',{});
  const M1=buildModel();
  uok(M1.two.d>M0.two.d&&M1.two.orders.length>M0.two.orders.length,
      'a wider separation makes more quiet lines ('+M0.two.orders.length+' → '+M1.two.orders.length+')');
  const s=sliderU('its height'); s.value=String(2*AIR.W/3); s.fire('input');
  uok(Math.abs(ST.spk2y-2*AIR.W/3)<1e-9,'the slider puts it back');
  RECU=makeRecU(); tab(2);
  uok(textsU(RECU).some(t=>t.indexOf('½λ')>=0),'the first quiet line is labelled on the picture');
  const nb=findLabelledU('the quiet hyperbolae'); nb.checked=false; nb.fire('change');
  RECU=makeRecU(); tab(2);
  uok(!textsU(RECU).some(t=>t.indexOf('½λ')>=0),'and switching them off removes it');
  nb.checked=true; nb.fire('change'); }

/* ---- the wall ---- */
tab(3); pause(); runFor(400);
{ uok(isShown(sliderU('wall position'))&&isShown(sliderU('wall angle')),'the wall view shows PhET’s two wall sliders');
  const M=buildModel();
  uok(!!M.wall&&M.wall.bounce,'the ray from the speaker reaches the listener off the wall');
  uok(Math.abs(M.wall.aIn-M.wall.aOut)<1e-12,'and its two angles are equal ['+fmt(M.wall.aIn/DEG,3)+'°]');
  uok(RO().indexOf('incidence, reflection')>=0,'the readout prints both');
  uok(M.g.nfront<LAT.VIS*LAT.VIS,'the wall hides part of the room');
  const before=M.g.nfront;
  const sa=sliderU('wall angle'); sa.value=String(WALLR.amin); sa.fire('input');
  uok(buildModel().g.nfront>before,'laying the wall flat hides less of it');
  sa.value=String(WALLR.amax); sa.fire('input');
  uok(buildModel().g.nfront<before,'standing it upright hides more');
  sa.value=String(WALLR.a0); sa.fire('input');
  const sp=sliderU('wall position'); sp.value=String(WALLR.xmax); sp.fire('input');
  uok(buildModel().g.nfront>before,'and moving it away hides less');
  sp.value=String(WALLR.x0); sp.fire('input');
  RECU=makeRecU(); tab(3);
  uok(textsU(RECU).some(t=>t.indexOf('image speaker')>=0),'the image speaker is named on the picture');
  uok(textsU(RECU).some(t=>/^[\d.]+° = [\d.]+°$/.test(t)),'and the two equal angles are printed at the bounce');
  const ib=findLabelledU('the image speaker and the ray'); ib.checked=false; ib.fire('change');
  RECU=makeRecU(); tab(3);
  uok(!textsU(RECU).some(t=>t.indexOf('image speaker')>=0),'switching the overlay off removes them');
  ib.checked=true; ib.fire('change');
  /* a listener behind the wall hears nothing */
  const L0=TOOLS.listener.slice();
  TOOLS.listener=[9.5,9.5];
  const M2=buildModel();
  uok(!M2.listener.inFront&&M2.listener.u===0,'a listener behind the wall hears nothing at all');
  tab(3);                                      /* the readout only changes when the view refreshes */
  uok(RO().indexOf('no sound')>=0,'and the readout says so');
  TOOLS.listener=L0; }

/* ---- thin air ---- */
tab(4); pause(); runFor(200);
{ uok(isShown(sliderU('air density')),'the air view shows PhET’s density slider');
  const M0=buildModel();
  uok(Math.abs(M0.air.v-soundSpeedIdeal(GAS.T0))<1e-12,'the readout’s speed is the ideal-gas speed');
  uok(RO().indexOf('343.2')>=0,'which it prints to five figures');
  const s=sliderU('air density'); s.value='0.25'; s.fire('input');
  uok(ST.pressure===0.25&&RUN.pressure===0.25,'a quarter of an atmosphere reaches the run');
  const M1=buildModel();
  uok(Math.abs(M1.air.v-M0.air.v)<1e-12,'and the SPEED OF SOUND does not move');
  uok(Math.abs(M1.air.db+12.0412)<1e-3,'while the loudness falls 12.04 dB');
  runFor(200);
  uok(Math.abs(RUN.val)<=Math.abs(M0.R.A*LAT.AMP_CAL*0.25)+1e-12,'the drive itself is a quarter of what it was');
  s.value='0'; s.fire('input');
  runFor(60);
  uok(RUN.val===0,'a vacuum drives nothing');
  uok(RO().indexOf('silent')>=0,'and the readout says silent, not -Infinity dB');
  RECU=makeRecU(); tab(4); assertCleanU(RECU,'the vacuum');
  clickButtonU('back to 1 atm'); uok(ST.pressure===1,'the reset button puts the air back'); }

/* ---- the tone, against the stub AudioContext ---- */
tab(0); ST.running=true;
{ const st0=ALOG.started, cb=findLabelledU('play the tone'); uok(!!cb&&isShown(cb),'the play-tone box is on show');
  cb.checked=true; cb.fire('change');
  uok(AUDIO.state==='playing'&&ALOG.started===st0+1,'ticking it starts a tone');
  const tb=toneBuffer(RUN.f,1,44100), lastBuf=ALOG.buffers[ALOG.buffers.length-1];
  uok(!!lastBuf&&lastBuf.length===tb.L,'the buffer holds a whole number of cycles ('+tb.L+' samples, '+tb.m+' cycles)');
  uok(Math.abs(ALOG.gain.gain.value-TONE_MAX*RUN.A/AIR.ampMax)<1e-12,'at the level the amplitude slider asks for');
  uok(ALOG.last.loop===true,'and loops');
  { const s=sliderU('frequency'), st1=ALOG.started, sp1=ALOG.stopped;
    s.value='800'; s.fire('input');
    uok(ALOG.started===st1+1&&ALOG.stopped===sp1+1,'moving the frequency slider swaps the buffer');
    uok(Math.abs(ALOG.buffers[ALOG.buffers.length-1].length-toneBuffer(800,1,44100).L)<1,'for the new pitch');
    s.value='550'; s.fire('input'); }
  { const lv0=ALOG.gain.gain.value; chipU('at the listener',2).fire('click');
    uok(ST.toneMode==='listener','the listener chip lights');
    pumpU(4);
    uok(ALOG.gain.gain.value!==lv0,'and the level now follows what the listener hears');
    chipU('at the speaker',2).fire('click'); }
  /* the clock stays RUNNING here: a tone that is already silent cannot be shown to be
     stopped by anything else (the dual of a proven-idle baseline) */
  { const sp=ALOG.stopped; keyU(' '); uok(!ST.running&&AUDIO.state==='off'&&ALOG.stopped===sp+1,'pausing the clock stops the tone');
    keyU(' '); uok(ST.running&&AUDIO.state==='playing','and starting it again resumes it'); }
  { const sp=ALOG.stopped; clickButtonU('press the speaker button');
    uok(!sourceActive(RUN)&&AUDIO.state==='off'&&ALOG.stopped===sp+1,'switching the speaker off stops the tone');
    clickButtonU('press the speaker button'); uok(AUDIO.state==='playing','and on starts it'); }
  { const sp=ALOG.stopped; tab(5); uok(AUDIO.state==='off'&&ALOG.stopped===sp+1,'the analysis view stops it'); tab(0);
    uok(AUDIO.state==='playing','coming back starts it'); }
  findLabelledU('play the tone').checked=false; findLabelledU('play the tone').fire('change');
  uok(AUDIO.state==='off','and unticking the box stops it'); }
pause();

/* ---- the analysis view ---- */
tab(5);
{ for(let q=0;q<12;q++){ const M=buildModel(); if(!M.X.pending) break; NODESU.tabs.children[5].fire('click'); }
  const M=buildModel();
  uok(!M.X.pending,'the analysis view finishes measuring, one frequency per frame');
  uok(M.X.rows.filter(r=>r.m).length>=5,'and has all five of its measurements');
  for(const r of M.X.rows) if(r.m&&r.f>=325)
    uok(Math.abs(r.m.err)<0.0006,'measured on the lattice, '+r.f+' Hz gives λ within 0.06 % of v/f ('+pct(r.m.err)+')');
  uok(RO().indexOf('measured on the lattice')>=0,'the readout lists them');
  RECU=makeRecU(); tab(5);
  uok(textsU(RECU).indexOf('frequency f, Hz')>=0,'the plane is drawn against frequency');
  uok(textsU(RECU).some(t=>t.indexOf('PhET’s one fixed step')>=0),'with PhET’s own error beside it');
  uok(textsU(RECU).some(t=>t.indexOf('group speed')>=0),'and the lattice’s dispersion');
  assertCleanU(RECU,'the analysis view');
  const before=RO();
  const s=sliderU('frequency'); s.value='430'; s.fire('input');
  for(let q=0;q<4;q++){ const MM=buildModel(); if(!MM.X.pending) break; }
  uok(RO()!==before,'moving the frequency re-measures the lattice at the new setting');
  s.value='550'; s.fire('input'); }

/* ---- keys ---- */
{ keyU('1'); uok(ST.view==='intro','1 is the speaker'); keyU('3'); uok(ST.view==='two','3 is two speakers');
  keyU('6'); uok(ST.view==='law','6 is the analysis view');
  keyU('9'); uok(ST.view==='law','9 is not a view'); keyU('4'); uok(ST.view==='wall','4 is the wall'); }

/* ---- every visible control on every tab, at its ends and middle ---- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length>=14,'the panel has its sliders and checkboxes ('+inputs.length+')');
  for(let v=0;v<6;v++){ tab(v); pause();
    let touched=0;
    for(const inp of inputs){
      if(!isShown(inp)) continue; touched++;
      if(inp.type==='checkbox'){ if(inp===findLabelledU('time runs')) continue;
        inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      for(const x of [inp.min,inp.max,(+inp.min+ +inp.max)/2]){ inp.value=String(x); inp.fire('input'); }
      uok(NODESU.errbox.style.display!=='block','tab '+v+': '+(rowOf(inp)&&rowOf(inp).children[0]?rowOf(inp).children[0].textContent:'a slider')+' at its ends draws without error'); }
    uok(v===5?touched===1:touched>=1,
        v===5?'the analysis view shows exactly one control, the frequency slider ('+touched+')'
             :'tab '+v+' has controls on show ('+touched+')');
    RECU=makeRecU(); tab(v); assertCleanU(RECU,'tab '+v+' after the sweep'); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

/* ---- the panel shows each view its own groups ---- */
{ const groups=NODESU.panel.children;
  tab(0); uok(groups[0].hidden===false&&groups[2].hidden===true&&groups[3].hidden===true&&groups[4].hidden===true,
              'the speaker view shows the source group and none of the three screen-specific ones');
  tab(2); uok(groups[2].hidden===false&&groups[3].hidden===true,'the two-speaker view shows only its own');
  tab(3); uok(groups[3].hidden===false&&groups[2].hidden===true,'the wall view shows only its own');
  tab(4); uok(groups[4].hidden===false&&groups[3].hidden===true,'the air view shows only its own');
  tab(5); uok(groups[0].hidden===false&&!isShown(sliderU('amplitude'))&&isShown(sliderU('frequency'))
              &&groups[1].hidden===true&&groups[6].hidden===true,
              'and the analysis view keeps the frequency slider and nothing else');
  tab(0); }

/* ---- reset all against a fully disturbed state ---- */
let rsErr=null;
try{ tab(3); pause();
  sliderU('frequency').value='840'; sliderU('frequency').fire('input');
  sliderU('amplitude').value='2'; sliderU('amplitude').fire('input');
  sliderU('wall angle').value=String(WALLR.amax); sliderU('wall angle').fire('input');
  chipU('pulse',2).fire('click'); chipU('slow',2).fire('click'); chipU('both',3).fire('click');
  for(const nm of ['PhET’s 5 m ruler','stopwatch','graph along the speaker’s row']){
    const c=findLabelledU(nm); c.checked=true; c.fire('change'); }
  const ib=findLabelledU('the image speaker and the ray'); ib.checked=false; ib.fire('change');
  TOOLS.listener=[9,1]; TOOLS.ruler=[6,2]; ST.pressure=0.3; ST.spk2y=1.2; ST.tone=true;
  runFor(40); CLOCK.watchOn=true; CLOCK.watch=1;
  uok(ST.speed==='slow'&&ST.ruler&&ST.watch&&ST.graph&&!ST.image&&ST.wave==='pulse','the state is disturbed');
  idleU('idle before reset');
  RECU=makeRecU(); uok(clickButtonU('reset all'),'found reset all');
  let same=true, firstBad='';
  for(const k in DEFAULTS) if(k!=='view'&&ST[k]!==DEFAULTS[k]){ same=false; firstBad=firstBad||k; }
  uok(same,'reset all restores every default'+(same?'':' ('+firstBad+')'));
  uok(JSON.stringify(TOOLS)===JSON.stringify(TOOLS0),'and the tools’ positions');
  uok(RUN.n===0&&RUN.t===0&&CLOCK.watch===0&&!CLOCK.watchOn,'and the room (the clock at zero, the stopwatch off)');
  uok(RUN.A===AIR.amp0&&RUN.cont&&RUN.on&&RUN.pressure===1,'and the speaker (amplitude 5, continuous, running, full air)');
  uok(RECU.ops.length>=6,'reset repaints (a fresh, silent room: '+RECU.ops.length+' ops)');
  uok(findLabelledU('PhET’s 5 m ruler').checked===false,'the checkboxes follow');
  uok(chipU('normal',2).className==='chip on'&&chipU('continuous',2).className==='chip on','the chips follow');
  uok(Math.abs(+sliderU('frequency').value-AIR.f0)<1e-12,'the sliders follow');
  uok(AUDIO.state==='off','and the tone is silent');
}catch(e){ rsErr=e; }
uok(!rsErr,'reset sweep completes'+(rsErr?': '+(rsErr.stack||rsErr):''));
uok(NODESU.errbox.style.display!=='block','no error on screen at the end');

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
