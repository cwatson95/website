
/* ============ UI drive test for magnet-and-compass.html =================== *
 * DOM-stub pattern (the family's; lineage tools/ui_drive.js via build_buoy).  Nothing
 * moves here once the needle has settled, so every action is fired from a PROVEN-IDLE
 * baseline and must repaint through the frame loop.  The sim-specific thresholds:
 * 5 tabs, 7 panel groups, 12 inputs.                                                  */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };
const uclose=(a,b,t,n)=>uok(Math.abs(a-b)<=t,n+' ['+a+' vs '+b+']');

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
    appendChild(c){ this.children.push(c); c.parentEl=this;
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
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0,deltaY:0},ev||{})); },
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
function groupU(title){
  for(const g of NODESU.panel.children){ const h3=(g.children[0]&&g.children[0].tagName==='H3')?g.children[0]:null;
    if(h3&&(h3.textContent||'')===title&&!g.hidden) return g; }
  return null;      /* a group this view hides is not this view's control */
}
function findIn(root,pred){ let hit=null; const walk=n=>{ for(const ch of n.children||[]){ if(pred(ch)) hit=hit||ch; walk(ch); } }; walk(root); return hit; }
function cbU(group,label){ const g=groupU(group); if(!g) return null;
  const lab2=findIn(g,ch=>ch.tagName==='LABEL'&&(ch.textContent||'')===label);
  return lab2?findIn(lab2,c=>c.tagName==='INPUT'):null; }
function sliderU(group,label){ const g=groupU(group); if(!g) return null;
  const row=findIn(g,ch=>ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label);
  return row?row.children[1]:null; }
function chipU(label){ return findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&ch.className.indexOf('chip')===0&&(ch.textContent||'')===label); }
function clickBtnU(label){ const b=findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&ch.className===''&&(ch.textContent||'')===label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(4); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+(geomU(RECU)==='[]'?'':' (painted '+RECU.ops.length+' ops)')); }
/* pump until the page is demonstrably still, then assert it */
function settleU(label,maxF){
  maxF=maxF||2000; let i=0;
  for(;i<maxF;i++){ RECU=makeRecU(); pumpU(1); if(RECU.ops.length===0) break; }
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]',label+' (still after '+i+' frames)'+(geomU(RECU)==='[]'?'':', painted '+RECU.ops.length+' ops'));
}
function frameU(n){ RECU=makeRecU(); pumpU(n||3); return geomU(RECU); }
const roU=()=>NODESU.readout.innerHTML;
const downU=(x,y)=>NODESU.scene.fire('pointerdown',{clientX:x,clientY:y});
const moveU=(x,y)=>NODESU.scene.fire('pointermove',{clientX:x,clientY:y,buttons:1});
const upU=()=>NODESU.scene.fire('pointerup',{});
const mapU=()=>screenGeo(RECU,1400,820,ST.view).map;

/* ---------------- boot ---------------- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===5,'five view tabs were built ('+NODESU.tabs.children.length+')');
uok(NODESU.panel.children.length===7,'the control panel has its 7 groups ('+NODESU.panel.children.length+')');
uok(roU().length>300,'the readout rendered');
uok(NODESU.eqbar.innerHTML.indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>50,'the equation bar rendered');
uok(ST.view==='bar'&&ST.pct===75,'it opens on the bar magnet at 75 %, as PhET does');
uok(roU().indexOf(fmtField(225,'G'))>=0,'the readout prints the strength off the model (225.00 G)');

/* ---------------- every tab draws, differently, cleanly ---------------- */
const FLOORSU=[643,96,48,52,76];     /* 80 % of what each view emits (measured on the family's engine: 804, 120, 60, 66, 95) */
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  uok(NODESU.tabs.children[i].className==='active','tab '+i+' is marked active');
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');
NODESU.tabs.children[0].fire('click');
idleU('the bar magnet view, with the needle settled, paints nothing while idle');

/* ---------------- dragging the magnet, the compass and the meter ---------------- */
{ /* the compass goes away first, so the repaint can only come from the pointer handler; and
     the magnet is grabbed by its north END, where a lost offset or a shrunken hit box shows */
  const cc=cbU('tools','compass'); cc.checked=false; cc.fire('change');
  settleU('with the compass away the page is still');
  const map=mapU(), X=map.X(ST.bar.x+MAG_B*0.8), Y=map.Y(ST.bar.y-MAG_R*0.6), g0=frameU();
  const before=ST.bar.x, roBefore=roU();
  downU(X,Y); uok(DRAG.what==='bar','pointer-down on the magnet\'s north end grabs it');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  moveU(X+90,Y-30);
  uclose(ST.bar.x,before+90/map.s,1e-9,'the magnet moved by 90 px worth of millimetres, the grab offset kept');
  uclose(ST.bar.y,333+30/map.s,1e-9,'and up by 30');
  const g1=frameU(); uok(g1.length>50&&g1!==g0,'the drag repaints through the frame loop, from the handler\'s own dirty flag');
  upU(); uok(DRAG.what===null,'pointer-up lets go');
  uok(roU()!==roBefore,'and the readout followed the magnet');
  cc.checked=true; cc.fire('change'); LIVE.barRot=null; }
{ const map=mapU(); settleU('the page settles with the compass back');
  const X=map.X(ST.barC.x), Y=map.Y(ST.barC.y);
  downU(X,Y); uok(DRAG.what==='barC','the compass grabs');
  moveU(X-140,Y-60); upU();
  uclose(ST.barC.x,625-140/map.s,1e-9,'the compass moved with the pointer');
  const g=frameU(); uok(g.length>50,'and its needle is swinging: the loop repaints');
  let n=0; while(n<2000&&stepLive(1/60)) n++;
  uok(n<2000,'it settles again after '+fmt(n/60,2)+' s');
  const B=meterReading(barMagnet(ST),ST.barC.x,ST.barC.y);
  uok(Math.abs(wrapPi(LIVE.barRot.phi-Math.atan2(B.By,B.Bx)))<1e-3,'pointing along the field where it now is'); }
{ const cb=cbU('tools','field meter'); uok(!!cb&&!cb.checked,'the field meter starts in its box (PhET)');
  cb.checked=true; cb.fire('change'); uok(ST.barMeter,'ticking it brings the meter out');
  const rd=meterReading(barMagnet(ST),ST.barM.x,ST.barM.y);
  uok(roU().indexOf(fmtField(rd.B,'G'))>=0,'the readout prints its |B| off the model');
  settleU('still before the meter drag');
  const map=mapU(), G=meterBodyBox(map,ST.barM.x,ST.barM.y);
  downU(G.X,G.Y); uok(DRAG.what==='barM','the meter\'s crosshair grabs');
  moveU(map.X(430),map.Y(420)); upU();
  uclose(ST.barM.x,430,1e-9,'it moved to where the pointer put it');
  const rd2=meterReading(barMagnet(ST),430,420);
  uok(roU().indexOf(fmtField(rd2.B,'G'))>=0,'and the reading changed with it ('+fmtField(rd2.B,'G')+')');
  uok(Math.abs(rd2.B-rd.B)>0.01,'to a genuinely different field'); }
{ settleU('still before the flip');
  const rd=meterReading(barMagnet(ST),ST.barM.x,ST.barM.y);
  RECU=makeRecU(); uok(clickBtnU('flip polarity'),'the flip button exists and fires');
  uok(RECU.ops.length>50,'the flip repaints at once');
  const rd2=meterReading(barMagnet(ST),ST.barM.x,ST.barM.y);
  uclose(rd2.Bx,-rd.Bx,1e-12,'the field at the meter is reversed');
  uok(Math.abs(LIVE.barRot.om)>0,'and the needle has been kicked off the unstable equilibrium (PhET does the same)');
  let n=0; while(n<3000&&stepLive(1/60)) n++;
  const atC=meterReading(barMagnet(ST),ST.barC.x,ST.barC.y);
  uok(n<3000,'the needle turns round and settles, after '+fmt(n/60,2)+' s');
  uok(Math.abs(wrapPi(LIVE.barRot.phi-Math.atan2(atC.By,atC.Bx)))<1e-3,'pointing along the reversed field at the compass');
  clickBtnU('flip polarity'); uclose(ST.bar.ang,0,1e-12,'flipping again restores it'); }
{ const s=sliderU('the bar magnet','strength'); uok(!!s,'found the strength slider');
  settleU('still before the slider'); RECU=makeRecU(); s.value='0'; s.fire('input');
  uok(ST.pct===0,'strength 0 %'); uok(RECU.ops.length>20,'the view redrew at once');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/strength 0: no field/.test(texts),'and it says there is no field rather than drawing an empty stage');
  uok(roU().indexOf(fmtField(0,'G'))>=0,'the readout reads 0 G');
  s.value='100'; s.fire('input'); uok(ST.pct===100&&roU().indexOf(fmtField(300,'G'))>=0,'at 100 % it is PhET\'s 300 G');
  s.value='75'; s.fire('input'); }
{ const cb=cbU('the bar magnet','see inside'); RECU=makeRecU(); cb.checked=true; cb.fire('change');
  const a=RECU.ops.length; uok(ST.seeInside&&a>50,'see inside redraws the magnet with its inner field');
  RECU=makeRecU(); cb.checked=false; cb.fire('change'); uok(RECU.ops.length!==a,'and switching it off changes the picture back');
  const e=cbU('the bar magnet','Earth'); RECU=makeRecU(); e.checked=true; e.fire('change');
  uok(ST.earth&&RECU.ops.length>50,'the Earth draws');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/geographic N/.test(texts),'labelled with the geographic north at the magnet\'s south pole');
  uok(findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&(ch.textContent||'')==='flip Earth')!==null,'and the flip button becomes "flip Earth" (PhET)');
  e.checked=false; e.fire('change'); }
{ const cb=cbU('the bar magnet','magnetic field (B)'); RECU=makeRecU(); cb.checked=false; cb.fire('change');
  uok(RECU.ops.length<200,'hiding the field takes the needles away ('+RECU.ops.length+' ops)');
  cb.checked=true; cb.fire('change'); }
{ chipU('T (tesla)').fire('click'); uok(ST.units==='T','tesla');
  uok(roU().indexOf('× 10^')>=0,'the readout switches to scientific tesla');
  chipU('G (gauss)').fire('click'); }

/* ---------------- the analysis views ---------------- */
NODESU.tabs.children[1].fire('click');
{ uok(ST.view==='lines','field lines');
  uok(/closed on themselves/.test(roU()),'the readout says the lines close');
  const bd=cbU('what to show','bound current on the magnet');
  uok(!!bd&&!bd.disabled&&bd.checked,'the bound-current box is live here');
  RECU=makeRecU(); bd.checked=false; bd.fire('change');
  uok(!ST.bound&&RECU.ops.length>50,'switching it off redraws'); bd.checked=true; bd.fire('change');
  uok(cbU('what to show','μ₀H inside the magnet').disabled,'the H box is dimmed in this view (it would do nothing)');
  idleU('the field-lines view is static'); }
NODESU.tabs.children[2].fire('click');
{ uok(ST.view==='axis','on the axis');
  const H=cbU('what to show','μ₀H inside the magnet'); uok(!H.disabled&&H.checked,'now the H box is the live one');
  RECU=makeRecU(); H.checked=false; H.fire('change'); uok(RECU.ops.length>20,'hiding it redraws'); H.checked=true; H.fire('change');
  uok(roU().indexOf(fmtField(225*solAxis(0,MAG_R,MAG_B),'G'))>=0,'the readout prints the centre field, 220.63 G');
  uok(roU().indexOf(fmt(solAxis(0,MAG_R,MAG_B),6))>=0,'and cos alpha itself'); }
NODESU.tabs.children[3].fire('click');
{ uok(ST.view==='far','the far field');
  uok(roU().indexOf(fmt(dipoleLimit('magnet',0,'axis').lim,10))>=0,'the readout prints the numerically taken dipole limit');
  uok(roU().indexOf(sigf(octCoef('magnet',0,'axis'),6))>=0,'and the octupole coefficient in closed form');
  uok(!sliderU('the bar magnet','strength'),'the magnet panel is not in this view');
  idleU('the far field is static'); }
NODESU.tabs.children[4].fire('click');
{ uok(ST.view==='needle','the needle');
  const B=sliderU('the needle','|B|'), rel2=sliderU('the needle','released at'), d=sliderU('the needle','damping γ');
  uok(!!B&&!!rel2&&!!d,'its three sliders are there');
  const T0=2*Math.PI/Math.sqrt(KAPPA*ST.ndB);
  uok(roU().indexOf(sigf(T0,4))>=0,'the readout prints the small-swing period');
  RECU=makeRecU(); B.value=String(Math.log10(80)); B.fire('input');
  uok(Math.abs(ST.ndB-80)<1,'the log slider sets |B| to about 80 G ('+ST.ndB+')');
  uok(RECU.ops.length>50,'and it redraws');
  const T1=2*Math.PI/Math.sqrt(KAPPA*ST.ndB);
  uok(roU().indexOf(sigf(T1,4))>=0&&T1<T0,'with a shorter period, '+sigf(T1,4)+' s: a stronger field swings it faster');
  d.value='0'; d.fire('input'); uok(ST.ndDamp===0,'the damping can be switched off');
  d.value='2'; d.fire('input'); B.value=String(Math.log10(5)); B.fire('input');
  uok(stepLive(1/60)===true,'this view animates its time cursor'); pumpU(4); }

/* ---------------- the frame loop drives the model ---------------- *
 * Everywhere else the tests step the clocks themselves, which would pass just as happily if
 * the loop never called step() at all (the mutation sweep found exactly that).  Here the only
 * thing that moves the needle is the pump. */
NODESU.tabs.children[0].fire('click');
settleU('still before the loop test');
{ clickBtnU('flip polarity');
  const phi0=LIVE.barRot.phi;
  pumpU(20);
  uok(LIVE.barRot.phi!==phi0,'pumping frames turns the needle: the loop steps the model itself');
  let i=0; for(;i<2000;i++){ RECU=makeRecU(); pumpU(1); if(RECU.ops.length===0) break; }
  const at=meterReading(barMagnet(ST),ST.barC.x,ST.barC.y);
  uok(i<2000&&Math.abs(wrapPi(LIVE.barRot.phi-Math.atan2(at.By,at.Bx)))<1e-3,'and it settles along the field under the loop alone, in '+fmt(i/60,2)+' s');
  clickBtnU('flip polarity'); settleU('and settles again after the flip back'); }

/* ---------------- keyboard, pause, resize ---------------- */
keyU('1'); uok(ST.view==='bar','1 goes to the bar magnet');
keyU('5'); uok(ST.view==='needle','5 to the needle');
keyU('2'); uok(ST.view==='lines','2 to the field lines');
keyU('1');
{ const a=ST.bar.ang; keyU('f'); uclose(ST.bar.ang,a+Math.PI,1e-12,'f flips the magnet'); keyU('f'); }
{ keyU(' '); uok(ST.run===false,'space pauses');
  NODESU.tabs.children[4].fire('click');
  idleU('and even the needle view is then still');
  keyU(' '); uok(ST.run===true,'space starts it again');
  uok(stepLive(1/60)===true,'and the clock runs'); NODESU.tabs.children[0].fire('click'); }
{ let rsErr=null; try{ for(const f of (WINHU.resize||[])) f({}); }catch(e){ rsErr=e; }
  uok(!rsErr,'the resize handler runs'+(rsErr?': '+rsErr:''));
  uok(NODESU.errbox.style.display!=='block','no error after resize'); }

/* ---------------- every control, every view ---------------- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===12,'the panel has its 4 sliders and 8 checkboxes ('+inputs.length+')');
  for(let v=0;v<5;v++){
    NODESU.tabs.children[v].fire('click');
    for(const inp of inputs){
      if(inp.disabled) continue;
      if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
      const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
      for(const x of [lo,hi,(lo+hi)/2]){ inp.value=String(x); inp.fire('input'); }
    }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every live control driven without error');
    RECU=makeRecU(); NODESU.tabs.children[v].fire('click'); assertCleanU(RECU,'view '+v+' after the sweep');
  }
  for(let v=0;v<5;v++){
    NODESU.tabs.children[v].fire('click');
    for(const nm of ['G (gauss)','T (tesla)']){ RECU=makeRecU(); chipU(nm).fire('click'); assertCleanU(RECU,'view '+v+', chip "'+nm+'"'); }
    uok(NODESU.errbox.style.display!=='block','view '+v+': the unit chips drew');
  }
  chipU('G (gauss)').fire('click');
  NODESU.tabs.children[0].fire('click');
  ST.bar={x:120,y:90,ang:Math.PI}; ST.pct=15; ST.barC={x:900,y:500}; ST.barM={x:800,y:100}; ST.barMeter=true; ST.seeInside=true; ST.earth=true;
  ST.units='T'; ST.bound=false; ST.axisH=false; ST.ndB=200; ST.ndRel=170; ST.ndDamp=9; ST.run=false; LIVE.ndT=3;
  uok(clickBtnU('reset all'),'found reset all');
  uok(ST.bar.x===430&&ST.bar.y===333&&ST.bar.ang===0&&ST.pct===75&&ST.barC.x===625&&!ST.barMeter&&!ST.seeInside&&!ST.earth,
      'it restores the magnet, its strength, the tools and the toggles');
  uok(ST.units==='G'&&ST.bound&&ST.axisH,'the units and the analysis toggles');
  uok(ST.ndB===5&&ST.ndRel===60&&ST.ndDamp===2&&ST.run===true&&LIVE.ndT===0,'the needle sliders and the clocks');
  uok(LIVE.barRot&&LIVE.barRot.rest,'with the needle back at rest along the field');
  uok(parseFloat(sliderU('the bar magnet','strength').value)===75&&cbU('the bar magnet','see inside').checked===false,'the controls show it');
  uok(ST.view==='bar','and it stays on the view you were looking at');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'the control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
