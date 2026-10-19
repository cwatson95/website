
/* ============ UI drive test for generator.html ============================ *
 * DOM-stub pattern (the family's; lineage tools/ui_drive.js via build_buoy).  With the
 * faucet shut nothing moves, so every action is fired from a PROVEN-IDLE baseline and
 * must repaint through the frame loop; with it open the loop itself must turn the wheel.
 * The sim-specific thresholds: 6 tabs, 9 panel groups, 16 inputs.                     */
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
uok(NODESU.tabs.children.length===6,'six view tabs were built ('+NODESU.tabs.children.length+')');
uok(NODESU.panel.children.length===9,'the control panel has its 9 groups ('+NODESU.panel.children.length+')');
uok(roU().length>300,'the readout rendered');
uok(NODESU.eqbar.innerHTML.indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>50,'the equation bar rendered');
uok(ST.view==='gen'&&ST.flow===0&&ST.N===2&&ST.area===50,'it opens on the generator with the faucet closed, as PhET does');
uok(roU().indexOf(fmtField(225,'G'))>=0,'the readout prints the strength off the model (225.00 G)');

/* ---------------- every tab draws, differently, cleanly ---------------- */
const FLOORSU=[672,72,144,96,48,76];   /* 80 % of what each view emits (measured: 840, 91, 181, 121, 60, 95) */
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  uok(NODESU.tabs.children[i].className==='active','tab '+i+' is marked active');
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
NODESU.tabs.children[0].fire('click');
idleU('the generator, faucet closed and needle settled, paints nothing while idle');

/* ---------------- the faucet is what makes it a generator ---------------- */
{ const s=sliderU('the water','faucet'); uok(!!s,'found the faucet slider');
  settleU('still before the faucet is opened');
  const texts0=frameU(); uok(texts0==='[]','and the still page emits nothing at all');
  RECU=makeRecU(); s.value='100'; s.fire('input');
  uok(ST.flow===100,'the faucet opens to 100 %');
  uok(RECU.ops.length>50,'and the view redraws at once');
  const th0=ST.th, e0=genReadings(genState(ST)).emf;
  pumpU(30);
  uok(ST.th!==th0,'pumping frames turns the wheel: the loop steps the model itself');
  const R=genReadings(genState(ST));
  uclose(R.rpm,genRPM({N:2,area:50,strength:75,flow:100}),1e-12,'at the speed the drag rule gives ('+fmt(R.rpm,2)+' RPM)');
  uok(roU().indexOf(fmt(R.rpm,2))>=0,'which the readout prints');
  uok(Math.abs(R.emf)>0,'and the coil has an EMF while it turns');
  /* the bulb: it lights only while the wheel turns */
  RECU=makeRecU(); pumpU(2);
  uok(RECU.ops.length>0,'the page keeps repainting while the water runs');
  s.value='0'; s.fire('input');
  settleU('close the faucet and everything comes to a stop');
  uclose(genReadings(genState(ST)).emf,0,0,'with no EMF at all, however strong the magnet');
  uok(genReadings(genState(ST)).Phi!==0,'though the flux through the coil is still there: it is its CHANGE that drives a current');
  RECU=makeRecU(); NODESU.tabs.children[0].fire('click');
  const shut=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/faucet is closed/.test(shut),'and the screen says so, rather than sitting there doing nothing without a word'); }
{ /* the strength slider: the EMF follows it, and at zero the screen says why */
  const s=sliderU('the water','faucet'); s.value='100'; s.fire('input');
  const p=sliderU('the bar magnet','strength');
  const e1=Math.abs(genReadings(genState(ST)).emf);
  p.value='40'; p.fire('input');
  const e2=Math.abs(genReadings(genState(ST)).emf);
  uok(e2<e1||e1===0,'a weaker magnet gives a smaller EMF');
  RECU=makeRecU(); p.value='0'; p.fire('input');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/no field/.test(texts),'at strength 0 the screen says there is no field rather than drawing an empty stage');
  p.value='75'; p.fire('input'); s.value='0'; s.fire('input'); settleU('and it settles again'); }

/* ---------------- the pickup coil ---------------- */
{ const sN=sliderU('the pickup coil','loops'), sA=sliderU('the pickup coil','loop area');
  uok(!!sN&&!!sA,'the coil has its loops and area sliders');
  const f=sliderU('the water','faucet'); f.value='100'; f.fire('input');
  ST.th=0.5; const e1=genReadings(genState(ST)).emf;
  RECU=makeRecU(); sN.value='4'; sN.fire('input');
  uok(ST.N===4&&RECU.ops.length>50,'four loops redraw the coil');
  const e4=genReadings(genState(ST)).emf;
  const want=4*(1-genDrag(4,50,75))/(2*(1-genDrag(2,50,75)));
  uclose(e4/e1,want,1e-9,'and give 4/2 x (1-d4)/(1-d2) = '+fmt(want,4)+' times the EMF: the loops add, and drag');
  const r0=pickRadius(ST.area);
  RECU=makeRecU(); sA.value='100'; sA.fire('input');
  uok(ST.area===100&&pickRadius(100)>r0,'the area slider grows the coil ('+fmt(r0,1)+' to '+fmt(pickRadius(100),1)+' mm)');
  uok(roU().indexOf(fmt(pickRadius(100),1))>=0,'the readout prints its radius');
  sN.value='2'; sN.fire('input'); sA.value='50'; sA.fire('input'); }
{ /* bulb or voltmeter */
  uok(ST.indicator==='bulb','it starts with the bulb, as PhET does');
  RECU=makeRecU(); chipU('voltmeter').fire('click');
  uok(ST.indicator==='volt'&&RECU.ops.length>50,'the voltmeter chip swaps the indicator');
  uok(roU().indexOf('voltmeter needle')>=0,'and the readout names its needle');
  RECU=makeRecU(); chipU('light bulb').fire('click');
  uok(ST.indicator==='bulb'&&RECU.ops.length>50,'and back to the bulb'); }
{ const cb=cbU('the pickup coil','electrons');
  uok(!!cb&&cb.checked,'the electrons start on (PhET)');
  const f=sliderU('the water','faucet'); f.value='100'; f.fire('input');
  const p0=LIVE.ePhase; pumpU(10);
  uok(LIVE.ePhase!==p0,'and they move while a current runs');
  RECU=makeRecU(); cb.checked=false; cb.fire('change');
  const a=RECU.ops.length; uok(!ST.electrons&&a>50,'switching them off redraws the coil without them');
  cb.checked=true; cb.fire('change');
  f.value='0'; f.fire('input'); settleU('still again with the faucet shut'); }

/* ---------------- the tools ---------------- */
{ /* The compass is grabbed by its RIM, not its centre: a grab at the centre has no offset to
     lose, and a shrunken hit box still catches it.  (The family's sweep found exactly that.) */
  const map=mapU(), X=map.X(ST.genC.x+26), Y=map.Y(ST.genC.y+18);
  settleU('still before the compass drag');
  downU(X,Y); uok(DRAG.what==='genC','pointer-down on the compass\'s rim grabs it');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  moveU(X-140,Y-60);
  uclose(ST.genC.x,300-140/map.s,1e-9,'the compass moved by 140 px worth of millimetres, the grab offset kept');
  uclose(ST.genC.y,520+60/map.s,1e-9,'and up by 60');
  upU(); uok(DRAG.what===null,'pointer-up lets go');
  let n=0; while(n<2000&&stepLive(1/60)) n++;
  const B=meterReading(turbMagnet(ST),ST.genC.x,ST.genC.y);
  uok(n<2000&&Math.abs(wrapPi(LIVE.genRot.phi-Math.atan2(B.By,B.Bx)))<1e-3,'and the needle settles along the field where the compass now is'); }
{ const cb=cbU('tools','field meter'); uok(!!cb&&!cb.checked,'the field meter starts in its box (PhET)');
  cb.checked=true; cb.fire('change'); uok(ST.genMeter,'ticking it brings the meter out');
  const rd=meterReading(turbMagnet(ST),ST.genM.x,ST.genM.y);
  uok(roU().indexOf(fmtField(rd.B,'G'))>=0,'the readout prints its |B| off the model');
  /* the compass goes away for the meter's drag: it is the one thing on this screen that
     moves by itself, and its motion would repaint the page whatever the drag did */
  const cc=cbU('tools','compass'); cc.checked=false; cc.fire('change');
  settleU('still before the meter drag, with the compass away');
  const map=mapU(), G=meterBodyBox(map,ST.genM.x,ST.genM.y);
  const px=G.bx+18, py=G.by+12, x0=ST.genM.x, y0=ST.genM.y, g0=frameU();
  downU(px,py); uok(DRAG.what==='genM','the meter grabs by its body, away from its crosshair');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  moveU(px+90,py-30);
  uclose(ST.genM.x,x0+90/map.s,1e-9,'it moved by 90 px worth of millimetres, the grab offset kept');
  uclose(ST.genM.y,y0+30/map.s,1e-9,'and up by 30');
  const g1=frameU();
  uok(g1.length>50&&g1!==g0,'and THAT repaint can only come from the handler\'s own dirty flag: nothing else on the screen moves');
  upU();
  const rd2=meterReading(turbMagnet(ST),ST.genM.x,ST.genM.y);
  uok(roU().indexOf(fmtField(rd2.B,'G'))>=0,'the reading changed with it ('+fmtField(rd2.B,'G')+')');
  uok(Math.abs(rd2.B-rd.B)>0.01,'to a genuinely different field');
  /* put it away again: nothing may be grabbed where it stood */
  const pos={x:ST.genM.x,y:ST.genM.y};
  cb.checked=false; cb.fire('change');
  const G2=meterBodyBox(mapU(),pos.x,pos.y);
  downU(G2.X,G2.Y); uok(DRAG.what===null,'with the meter put away, nothing is grabbed where it stood'); upU();
  cb.checked=true; cb.fire('change'); cc.checked=true; cc.fire('change'); LIVE.genRot=null;
  /* the magnet is bolted to the wheel: the pointer cannot take it */
  const mx=mapU().X(TURB_X), my=mapU().Y(TURB_Y);
  downU(mx,my); uok(DRAG.what===null,'the magnet itself cannot be dragged: it rides the wheel'); upU(); }
{ settleU('still before the flip');
  const rd=meterReading(turbMagnet(ST),ST.genM.x,ST.genM.y);
  RECU=makeRecU(); uok(clickBtnU('flip polarity'),'the flip button exists and fires');
  uok(RECU.ops.length>50,'the flip repaints at once');
  const rd2=meterReading(turbMagnet(ST),ST.genM.x,ST.genM.y);
  uclose(rd2.Bx,-rd.Bx,1e-9,'the field at the meter is reversed');
  uok(Math.abs(LIVE.genRot.om)>0,'and the needle has been kicked off the unstable equilibrium (PhET does the same)');
  let n=0; while(n<3000&&stepLive(1/60)) n++;
  uok(n<3000,'the needle turns round and settles, after '+fmt(n/60,2)+' s');
  clickBtnU('flip polarity'); settleU('and settles again after the flip back'); }
{ const cb=cbU('the bar magnet','magnetic field (B)'); RECU=makeRecU(); cb.checked=false; cb.fire('change');
  uok(RECU.ops.length<250,'hiding the field takes the needles away ('+RECU.ops.length+' ops)');
  cb.checked=true; cb.fire('change');
  const si=cbU('the bar magnet','see inside'); RECU=makeRecU(); si.checked=true; si.fire('change');
  uok(ST.seeInside&&RECU.ops.length>50,'see inside redraws the magnet with its inner field');
  si.checked=false; si.fire('change'); }
{ chipU('T (tesla)').fire('click'); uok(ST.units==='T','tesla');
  uok(roU().indexOf('× 10^')>=0,'the readout switches to scientific tesla');
  chipU('G (gauss)').fire('click'); }
{ /* PhET's Current Flow preference: the drawn flow reverses, the physics does not */
  const f=sliderU('the water','faucet'); f.value='100'; f.fire('input');
  pumpU(6); const p0=LIVE.ePhase; pumpU(6); const d1=LIVE.ePhase-p0;
  RECU=makeRecU(); chipU('conventional').fire('click');
  uok(ST.flowConv==='conventional'&&RECU.ops.length>20,'the conventional-current chip takes');
  const p1=LIVE.ePhase; pumpU(6); const d2=LIVE.ePhase-p1;
  uok(d1*d2<0,'and the electrons run the other way ('+fmt(d1,4)+' then '+fmt(d2,4)+')');
  uok(Math.abs(genReadings(genState(ST)).emf)>0,'while the EMF is unchanged: it is a drawing preference');
  chipU('electron').fire('click'); f.value='0'; f.fire('input'); settleU('still again'); }

/* ---------------- flux and EMF ---------------- */
NODESU.tabs.children[1].fire('click');
{ uok(ST.view==='flux','flux and EMF');
  const pk=emfPeak(fluxSeries(pickRadius(ST.area)));
  uok(roU().indexOf(fmt(pk.th*R2D,2))>=0,'the readout prints the peak angle the engine finds ('+fmt(pk.th*R2D,2)+'°)');
  const texts=frameU(); uok(texts.length>100,'the view draws its two panels');
  /* a still page paints nothing, so the picture has to be asked for: redraw by re-entering
     the tab into a fresh recorder (Known-bad: pumping an idle loop records an empty frame) */
  RECU=makeRecU(); NODESU.tabs.children[1].fire('click');
  const drawn=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/full flow/.test(drawn),'with the faucet shut it says the EMF curve is the one full flow would give');
  const f=sliderU('the water','faucet'); RECU=makeRecU(); f.value='100'; f.fire('input');
  const drawn2=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/RPM/.test(drawn2)&&!/full flow/.test(drawn2),'and once it is open, the EMF at the speed it is really turning');
  f.value='0'; f.fire('input');
  uok(!cbU('tools','compass')&&!!cbU('the pickup coil','electrons'),
      'the tools group is hidden in this view, while the coil\'s is not'); }

/* ---------------- the coil face ---------------- */
NODESU.tabs.children[2].fire('click');
{ uok(ST.view==='face','the coil face');
  const rc=pickRadius(ST.area), r=fluxPhet1(ST.th,rc)/flux1(ST.th,rc);
  uok(roU().indexOf(fmt(100*(r-1),1))>=0,'the readout prints how far PhET\'s line sample stands from the area integral ('+fmt(100*(r-1),1)+' %)');
  const dots=cbU('what to show','PhET’s sample points');
  uok(!!dots&&!dots.disabled&&dots.checked,'the sample-point box is live here');
  RECU=makeRecU(); dots.checked=false; dots.fire('change');
  const a=RECU.ops.length; uok(!ST.phetCmp&&a>20,'switching the dots off redraws');
  RECU=makeRecU(); dots.checked=true; dots.fire('change');
  uok(RECU.ops.length>a,'and switching them back on draws more ops than without them');
  uok(cbU('what to show','bound current on the magnet').disabled,'the bound-current box is dimmed here (it would do nothing)');
  idleU('the coil-face view is static'); }

/* ---------------- the shared analysis views ---------------- */
NODESU.tabs.children[3].fire('click');
{ uok(ST.view==='lines','field lines');
  uok(/closed on themselves/.test(roU()),'the readout says the lines close');
  const bd=cbU('what to show','bound current on the magnet');
  uok(!!bd&&!bd.disabled&&bd.checked,'the bound-current box is live here');
  RECU=makeRecU(); bd.checked=false; bd.fire('change');
  uok(!ST.bound&&RECU.ops.length>50,'switching it off redraws'); bd.checked=true; bd.fire('change');
  idleU('the field-lines view is static'); }
NODESU.tabs.children[4].fire('click');
{ uok(ST.view==='axis','on the axis');
  const H=cbU('what to show','μ₀H inside the magnet'); uok(!H.disabled&&H.checked,'now the H box is the live one');
  RECU=makeRecU(); H.checked=false; H.fire('change'); uok(RECU.ops.length>20,'hiding it redraws'); H.checked=true; H.fire('change');
  uok(roU().indexOf(fmtField(225*solAxis(0,MAG_R,MAG_B),'G'))>=0,'the readout prints the centre field, 220.63 G'); }
NODESU.tabs.children[5].fire('click');
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
 * the loop never called step() at all (the mutation sweep found exactly that in this family).
 * Here the only thing that turns the wheel is the pump. */
NODESU.tabs.children[0].fire('click');
settleU('still before the loop test');
{ const f=sliderU('the water','faucet'); f.value='60'; f.fire('input');
  const th0=ST.th, phi0=LIVE.genRot.phi;
  pumpU(40);
  const om=2*Math.PI*genRPM(genState(ST))/60;
  uok(ST.th!==th0,'pumping frames turns the wheel under the loop alone');
  uok(LIVE.genRot.phi!==phi0,'and drags the compass needle round with the field');
  uok(Math.abs(wrapPi(LIVE.genRot.phi-Math.atan2(meterReading(turbMagnet(ST),ST.genC.x,ST.genC.y).By,
        meterReading(turbMagnet(ST),ST.genC.x,ST.genC.y).Bx)))<Math.PI,'the needle chases the turning field, lagging it');
  f.value='0'; f.fire('input'); settleU('and everything stops when the water does'); }

/* ---------------- keyboard, pause, resize ---------------- */
keyU('1'); uok(ST.view==='gen','1 goes to the generator');
keyU('6'); uok(ST.view==='needle','6 to the needle');
keyU('3'); uok(ST.view==='face','3 to the coil face');
keyU('1');
{ const a=ST.th; keyU('f'); uclose(ST.th,wrap2pi(a+Math.PI),1e-12,'f flips the magnet'); keyU('f'); }
{ const f=sliderU('the water','faucet'); f.value='100'; f.fire('input');
  keyU(' '); uok(ST.run===false,'space pauses');
  idleU('and with the water running the page is still all the same');
  keyU(' '); uok(ST.run===true,'space starts it again');
  const th0=ST.th; pumpU(5); uok(ST.th!==th0,'and the wheel turns once more');
  f.value='0'; f.fire('input'); settleU('still with the faucet shut'); }
{ let rsErr=null; try{ for(const f of (WINHU.resize||[])) f({}); }catch(e){ rsErr=e; }
  uok(!rsErr,'the resize handler runs'+(rsErr?': '+rsErr:''));
  uok(NODESU.errbox.style.display!=='block','no error after resize'); }

/* ---------------- every control, every view ---------------- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===16,'the panel has its 7 sliders and 9 checkboxes ('+inputs.length+')');
  uok(NODESU.panel.querySelectorAll('.chips').length===3,'and its three chip rows: units, current flow, indicator');
  for(let v=0;v<6;v++){
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
  for(let v=0;v<6;v++){
    NODESU.tabs.children[v].fire('click');
    for(const nm of ['G (gauss)','T (tesla)','electron','conventional']){ RECU=makeRecU(); chipU(nm).fire('click'); assertCleanU(RECU,'view '+v+', chip "'+nm+'"'); }
    uok(NODESU.errbox.style.display!=='block','view '+v+': the unit chips drew');
  }
  chipU('G (gauss)').fire('click');
  NODESU.tabs.children[0].fire('click');
  ST.flow=80; ST.th=2.2; ST.pct=15; ST.N=4; ST.area=100; ST.indicator='volt'; ST.genC={x:900,y:500}; ST.genM={x:800,y:100};
  ST.genMeter=true; ST.seeInside=true; ST.electrons=false; ST.units='T'; ST.flowConv='conventional'; ST.bound=false; ST.axisH=false; ST.phetCmp=false;
  ST.ndB=200; ST.ndRel=170; ST.ndDamp=9; ST.run=false; LIVE.ndT=3; LIVE.ePhase=0.4;
  uok(clickBtnU('reset all'),'found reset all');
  uok(ST.flow===0&&ST.th===0&&ST.pct===75&&ST.N===2&&ST.area===50&&ST.indicator==='bulb','it restores the faucet, the wheel, the magnet and the coil');
  uok(ST.genC.x===300&&!ST.genMeter&&!ST.seeInside&&ST.electrons,'the tools and the toggles');
  uok(ST.units==='G'&&ST.flowConv==='electron'&&ST.bound&&ST.axisH&&ST.phetCmp,'the units, the flow preference and the analysis toggles');
  uok(ST.ndB===5&&ST.ndRel===60&&ST.ndDamp===2&&ST.run===true&&LIVE.ndT===0&&LIVE.ePhase===0,'the needle sliders and the clocks');
  uok(LIVE.genRot&&LIVE.genRot.rest,'with the needle back at rest along the field');
  uok(parseFloat(sliderU('the water','faucet').value)===0&&cbU('the bar magnet','see inside').checked===false,'the controls show it');
  uok(ST.view==='gen','and it stays on the view you were looking at');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'the control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
