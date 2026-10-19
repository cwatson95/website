
/* ============ UI drive test for fourier-making-waves.html ================= *
 * DOM-stub pattern (lineage: tools/ui_drive.js -> build_wave-on-a-string).
 * The sim-specific thresholds: the chip rows are found by exact label AND
 * arity (6 waveforms, 2 series, 3 domains, 4 convergence waveforms, 5 game
 * levels, 4 spacings, 2 packet domains); the panel has 8 groups; 14 inputs
 * (8 sliders, 6 checkboxes).  Every drag is tested THROUGH the frame loop
 * from a proven-idle baseline, and the amplitude bars are asserted to MOVE
 * the drawing, not merely the state. */
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
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
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
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const rc=findLabelledU('time runs'); if(rc.checked){ rc.checked=false; rc.fire('change'); } }
function playU(){ const rc=findLabelledU('time runs'); if(!rc.checked){ rc.checked=true; rc.fire('change'); } }


/* ---- boot ---- */
let bootErrU=null, BOOTED=null;
try{ BOOTED=boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')===
    'the harmonics|the convergence|the spectrum|the wave game|the wave packet|the transform pair',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===8,'the control panel has its 8 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('440')>=0||(NODESU.panel.textContent||'').indexOf('440')>=0,
    'PhET\'s 440 Hz reaches the page');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the panel carries the PhET credit line');
uok(ST.preset==='sinusoid'&&ST.series==='sin'&&ST.domain==='space'&&ST.N===11,
    'PhET\'s start: a sinusoid, sines, the space domain, all eleven harmonics');
uok(AMPS[0]===1&&AMPS[1]===0,'... with A1 = 1 and the rest zero');

/* the chip labels the sim decodes for the canvas are the ones the harness must
   match on: the DOM stub keeps innerHTML entities, a browser decodes them */
function chipFU(label,arity){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch.children.length===arity)
      for(const c of ch.children) if(plain(c.textContent||'')===plain(label)) hit=c;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* ---- every tab draws, differently, cleanly ---- */
const FLOORSU=[20,20,20,20,20,20];
const OPSU=[];
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  uok((NODESU.readout.innerHTML||'').length>200,'tab '+i+' fills the readout');
  uok((NODESU.eqbar.innerHTML||'').length>60,'tab '+i+' fills the equation bar');
  /* the selected tab must LOOK selected: nothing else in the harness reads the
     tab classes, and a setView that never sets them survived the sweep */
  { let act=0, wrong=0;
    for(let j=0;j<6;j++){ const c=NODESU.tabs.children[j].className||'';
      if(j===i){ if(c==='active') act++; else wrong++; } else if(c!=='') wrong++; }
    uok(act===1&&wrong===0,'tab '+i+' is the only one marked active'); }
  sigsU['t'+i]=sigU(RECU); OPSU.push(RECU.ops.length);
}
console.log('UI: ops per tab = '+OPSU.join(', '));
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- nothing animates unless the space & time domain is running ---- */
tabU(0);
for(let i=0;i<6;i++){ tabU(i); idleU('tab '+i+' paints nothing when nothing is running'); }

/* ---- the waveform chips fill the amplitudes from the closed forms ---- */
tabU(0);
for(const [name,arity] of [['sinusoid',6],['triangle',6],['square',6],['sawtooth',6],['wave packet',6]]){
  const c=chipFU(name,arity);
  uok(!!c,'found the '+name+' chip');
  if(!c) continue;
  c.fire('click');
  uok(ST.preset!=='custom','the '+name+' chip is a preset, not custom');
  uok((c.className||'').indexOf('on')>=0,'the '+name+' chip shows as selected');
  { let on=0;
    for(const p of PRESETS){ const q=chipFU(p.name,6); if(q&&(q.className||'').indexOf('on')>=0) on++; }
    uok(on===1,'and it is the only chip in its row that does'); }
  const want=presetAmps(ST.preset,ST.series,ST.N);
  let d=0; for(let i=0;i<NMAX;i++) d=Math.max(d,Math.abs(AMPS[i]-want[i]));
  uok(d<1e-15,'the '+name+' chip writes its closed form into the amplitudes');
}
/* PhET: picking a sawtooth while cosines are selected switches back to sines */
chipFU('cosines',2).fire('click');
uok(ST.series==='cos','the cosine chip selects cosines');
chipFU('sawtooth',6).fire('click');
uok(ST.series==='sin','choosing a sawtooth switches back to sines, as in PhET');
chipFU('square',6).fire('click');
chipFU('sines',2).fire('click');

/* ---- the domain chips ---- */
for(const [name,want] of [['time (t)','time'],['space & time','both'],['space (x)','space']]){
  const c=chipFU(name,3);
  uok(!!c,'found the "'+name+'" domain chip');
  if(c){ c.fire('click'); uok(ST.domain===want,'the "'+name+'" chip selects '+want); }
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
driveSliderU('harmonics kept',[1,3,7,11],'N');
driveSliderU('harmonic n',[1,5,11],'sel');
{ const s=sliderU('amplitude A');
  uok(!!s,'found the "amplitude A" slider');
  ST.sel=4; NODESU.tabs.children[0].fire('click');
  s.value='-1.13'; s.fire('input');
  uok(Math.abs(AMPS[3]+1.15)<1e-9,'the amplitude slider snaps to PhET\'s 0.05 step ['+AMPS[3]+']');
  uok(ST.preset==='custom','... and moving one by hand makes the waveform custom');
  s.value='2.4'; s.fire('input');
  uok(Math.abs(AMPS[3]-AMAX)<1e-12,'... and is clamped to +1.5'); }
chipFU('square',6).fire('click');

/* ---- every checkbox ---- */
for(const [lab,key] of [['the harmonics one by one','showHarm'],['the infinite-harmonics waveform','showInf'],
                        ['the wavelength caliper','caliper']]){
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

/* ---- the space & time domain runs through the frame loop ---- */
chipFU('space & time',3).fire('click');
uok(ST.domain==='both','the space & time domain is selected');
{ const rc=findLabelledU('time runs');
  uok(!!rc,'the "time runs" checkbox appears in the space & time domain');
  rc.checked=false; rc.fire('change');
  idleU('paused, the space & time view paints nothing');
  rc.checked=true; rc.fire('change');
  const t0=ST.t;
  RECU=makeRecU(); pumpU(1); const gA=geomU(RECU);
  RECU=makeRecU(); pumpU(1); const gB=geomU(RECU);
  uok(ST.t>t0,'the clock advances ('+fmt(ST.t,4)+' ms)');
  uok(gA.length>50&&gB.length>50&&gA!==gB,'two pumped frames draw DIFFERENT pictures (the pattern travels)');
  const dx=(ST.t-t0)*LWAVE/TPER;
  uok(dx>0,'and the pattern has moved '+fmt(dx,4)+' m');
  rc.checked=false; rc.fire('change'); }
/* the step button is PhET's 0.05 ms */
{ const t0=ST.t; uok(clickButtonU('step'),'found the step button');
  uok(Math.abs(ST.t-t0-0.05)<1e-12,'the step button advances t by PhET\'s 0.05 ms');
  uok(clickButtonU('t = 0'),'found the t = 0 button'); uok(ST.t===0,'... which rewinds the clock'); }
chipFU('space (x)',3).fire('click');

/* ---- the canvas drag: idle first, then assert the DRAWING moved ---- */
tabU(0);
chipFU('square',6).fire('click');
idleU('the harmonics view is idle before the drag');
{ const S=BOOTED;
  S.draw();
  uok(GEO.view==='harm'&&!!GEO.bars,'the harmonics view records its bar panel');
  const b=GEO.bars;
  RECU=makeRecU(); pumpU(3);
  const before=JSON.stringify(RECU.ops.filter(o=>o[0]!=='t'));
  const a0=AMPS[6];
  NODESU.scene.fire('pointerdown',{clientX:barX(b,7,ST.N),clientY:barY(b,-1.35,AMAX)});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(AMPS[6]+1.35)<1e-9,'a press on the seventh bar sets its amplitude ['+AMPS[6]+']');
  uok(AMPS[6]!==a0,'and it really changed');
  RECU=makeRecU(); pumpU(3);
  const after=JSON.stringify(RECU.ops.filter(o=>o[0]!=='t'));
  uok(after.length>50,'the frame after the drag drew something');
  uok(before!==after,'and the DRAWING moved, not only the state');
}
/* the caliper drag */
{ const c=findLabelledU('the wavelength caliper');
  c.checked=true; c.fire('change');
  const S=BOOTED; S.draw();
  const b=GEO.sum, x0=ST.calX;
  NODESU.scene.fire('pointerdown',{clientX:b.x+0.25*b.w,clientY:(b.y+b.y1)/2});
  uok(ST.calX!==x0,'a press on the sum panel moves the caliper');
  NODESU.scene.fire('pointermove',{clientX:b.x+0.8*b.w,clientY:(b.y+b.y1)/2,buttons:1});
  uok(Math.abs(ST.calX-(GEO.xa+(GEO.xb-GEO.xa)*0.8))<1e-9,'and a drag carries it');
  NODESU.scene.fire('pointerup',{});
  c.checked=false; c.fire('change'); }

/* ---- the convergence view ---- */
tabU(1);
driveSliderU('terms kept M',[1,2,11,64,128],'convM');
for(const [name,want] of [['triangle','triangle'],['sawtooth','sawtooth'],['sinusoid','sinusoid'],['square','square']]){
  const c=chipFU(name,4);
  uok(!!c,'found the convergence "'+name+'" chip');
  if(c){ RECU=makeRecU(); c.fire('click'); uok(ST.convPre===want,'the convergence "'+name+'" chip selects it');
         assertCleanU(RECU,'convergence '+name); }
}

/* ---- the game ---- */
tabU(3);
for(let L=1;L<=5;L++){
  const c=chipFU('level '+L,5);
  uok(!!c,'found the level '+L+' chip');
  if(!c) continue;
  RECU=makeRecU(); c.fire('click');
  uok(GAME.level===L,'the level '+L+' chip selects it');
  uok(nonZeroCount(GAME.answer)>=Math.min(L,5),'level '+L+' has at least '+Math.min(L,5)+' harmonics in the answer');
  uok(nonZeroCount(ampsNow())===0,'... and starts with the guess erased');
  assertCleanU(RECU,'game level '+L);
}
{ const a0=GAME.answer.join(',');
  uok(clickButtonU('new waveform'),'found the new-waveform button');
  uok(nonZeroCount(GAME.answer)>=1&&a0.length>0,'a new waveform is drawn and has harmonics in it');
  uok(clickButtonU('check answer'),'found the check button');
  uok(!GAME.solved,'an empty guess is not the answer');
  uok(clickButtonU('show answer'),'found the show-answer button');
  uok(GAME.solved&&gameMatches(ampsNow(),GAME.answer),'showing the answer fills the bars with it');
  uok(clickButtonU('check answer'),'check again');
  uok(GAME.score>=0,'the score is a number ('+GAME.score+')');
  uok(clickButtonU('erase my amplitudes'),'found the erase button');
  uok(nonZeroCount(ampsNow())===0,'... which zeroes the guess'); }
/* the game's bars move in 0.1 steps */
{ const S=BOOTED; S.draw();
  const b=GEO.bars;
  NODESU.scene.fire('pointerdown',{clientX:barX(b,2,NMAX),clientY:barY(b,0.73,AMAX)});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(GUESS[1]-0.7)<1e-9,'the game bars snap to 0.1 ['+GUESS[1]+']');
  uok(AMPS[1]!==0.7||ST.preset==='sinusoid','... into the GUESS array, not the Discrete one'); }

/* ---- the wave packet ---- */
tabU(4);
driveSliderU('centre k0',[WP_K0_MIN,12*PI,WP_K0_MAX],'wpK0');
driveSliderU('width sigma_k',[WP_SK_MIN,3*PI,WP_SK_MAX],'wpSk');
for(const [name,want] of [['0 (continuous)',0],['&pi;/4',1],['&pi;/2',2],['&pi;',3]]){
  const c=chipFU(name,4);
  uok(!!c,'found the spacing chip "'+plain(name)+'"');
  if(c){ RECU=makeRecU(); c.fire('click'); uok(ST.wpSp===want,'the spacing chip "'+plain(name)+'" selects '+want);
         assertCleanU(RECU,'spacing '+plain(name)); }
}
for(const [name,want] of [['time (&omega;, t)','time'],['space (k, x)','space']]){
  const c=chipFU(name,2);
  uok(!!c,'found the packet-domain chip "'+plain(name)+'"');
  if(c){ c.fire('click'); uok(ST.wpDom===want,'... and it selects '+want); }
}
for(const [lab,key] of [['the envelope','wpEnv'],['the width markers','wpWid']]){
  const c=findLabelledU(lab);
  uok(!!c,'found the "'+lab+'" checkbox');
  if(!c) continue;
  RECU=makeRecU(); c.checked=false; c.fire('change');
  uok(ST[key]===false,'"'+lab+'" turns off');
  assertCleanU(RECU,'"'+lab+'" off');
  c.checked=true; c.fire('change');
}

/* ---- the transform pair ---- */
tabU(5);
driveSliderU('spacing k1',[PAIR_K1_MIN,1,PI,PAIR_K1_MAX],'pairK1');
driveSliderU('packet width sigma_k',[WP_SK_MIN,3*PI,WP_SK_MAX],'pairSk');

/* ---- the keyboard ---- */
for(let i=1;i<=6;i++){ keyU(String(i)); uok(ST.view===TABS[i-1][0],'key '+i+' selects '+TABS[i-1][0]); }
keyU('1');
/* start ON the 0.05 grid: from a preset value the first nudge SNAPS rather
   than adding a whole step, which is PhET's behaviour and not a bug */
{ ST.sel=3; AMPS[2]=0.5; const a0=AMPS[2];
  keyU('ArrowUp'); uok(Math.abs(AMPS[2]-a0-A_STEP)<1e-9,'the up arrow nudges the selected amplitude by 0.05 ['+AMPS[2]+']');
  keyU('ArrowDown'); uok(Math.abs(AMPS[2]-a0)<1e-9,'and the down arrow puts it back');
  AMPS[2]=0.4244131815783876;
  keyU('ArrowUp'); uok(Math.abs(AMPS[2]-0.45)<1e-9,'from off the grid it snaps to the grid instead ['+AMPS[2]+']'); }
{ const t0=ST.t; keyU('.'); uok(Math.abs(ST.t-t0-0.05)<1e-12,'the "." key steps the clock'); }
{ const r0=ST.running; keyU(' '); uok(ST.running===!r0,'space runs and pauses'); keyU(' '); }
keyU('r');
uok(ST.preset==='sinusoid'&&ST.N===11&&AMPS[0]===1,'"r" resets to PhET\'s start');
uok(ST.view==='harm','... and stays on the current view');

/* ---- reset all, and the resize ---- */
tabU(2);
{ ST.sel=9; const s=sliderU('amplitude A'); s.value='1.5'; s.fire('input');
  uok(AMPS[8]===1.5,'an amplitude was changed before the reset');
  uok(clickButtonU('reset all'),'found the reset button');
  uok(AMPS[8]===0&&ST.preset==='sinusoid','reset all puts PhET\'s start back');
  uok(ST.view==='spec','... and leaves the view alone'); }
for(const [W,H] of [[1400,820],[900,620],[700,520],[1600,960]]){
  NODESU.scene.getBoundingClientRect=()=>({left:0,top:0,width:W,height:H});
  RECU=makeRecU();
  for(const f of (WINHU.resize||[])) f({});
  uok(RECU.ops.length>0,'resize to '+W+'x'+H+' repaints');
  assertCleanU(RECU,'resize '+W+'x'+H);
  uok(NODESU.errbox.style.display!=='block','resize to '+W+'x'+H+' drew without error');
}
NODESU.scene.getBoundingClientRect=()=>({left:0,top:0,width:1400,height:820});
for(const f of (WINHU.resize||[])) f({});

/* ---- every view x every waveform builds a clean panel ---- */
for(let i=0;i<6;i++){
  tabU(i);
  for(const p of PRESETS){
    const c=chipFU(p.name,6);
    if(!c) continue;
    RECU=makeRecU(); c.fire('click');
    assertCleanU(RECU,'view '+i+' with '+p.name);
    uok(NODESU.errbox.style.display!=='block','view '+i+' with '+p.name+' drew without error');
    uok(!/NaN|undefined/.test(NODESU.readout.innerHTML||''),'view '+i+' with '+p.name+': readout clean');
    uok(!/NaN|undefined/.test(NODESU.eqbar.innerHTML||''),'view '+i+' with '+p.name+': equation bar clean');
    uok(!/NaN|undefined/.test(NODESU.tag.innerHTML||''),'view '+i+' with '+p.name+': tag clean');
  }
}

/* the house format EXACTLY: _tools/verify_one.py looks for a line that
   contains 'UI' and matches '<n> passed, <m> failed', and '459 UI checks
   passed, 0 failed' does not match it (the digits are not next to the word). */
console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
