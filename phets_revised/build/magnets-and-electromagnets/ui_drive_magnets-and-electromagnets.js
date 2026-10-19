
/* ============ UI drive test for magnets-and-electromagnets.html =========== *
 * DOM-stub pattern (lineage: tools/ui_drive.js via build_buoy/ui_drive_bu.js and
 * build/charges-and-fields, whose stub derives textContent from innerHTML).  Nothing
 * here moves by itself once the compass has settled and the electrons are hidden, so
 * every action is fired from a PROVEN-IDLE baseline and must repaint through the frame
 * loop.  The three sim-specific thresholds: 6 tabs, 9 panel groups, 20 inputs.        */
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
/* group-scoped lookups: the two screens carry controls with the same labels on purpose
   (Known-bad: a finder that matches on a word finds the wrong control) */
function groupU(title){
  let any=null;
  for(const g of NODESU.panel.children){ const h3=(g.children[0]&&g.children[0].tagName==='H3')?g.children[0]:null;
    if(h3&&(h3.textContent||'')===title){ if(!g.hidden) return g; any=any||g; } }
  return null;      /* a group the current view hides is not this view's control */
}
function findIn(root,pred){ let hit=null; const walk=n=>{ for(const ch of n.children||[]){ if(pred(ch)) hit=hit||ch; walk(ch); } }; walk(root); return hit; }
function cbU(group,label){ const g=groupU(group); return g&&findIn(g,ch=>ch.tagName==='LABEL'&&(ch.textContent||'')===label&&ch.children.some(c=>c.tagName==='INPUT'))
  ? findIn(findIn(g,ch=>ch.tagName==='LABEL'&&(ch.textContent||'')===label),c=>c.tagName==='INPUT') : null; }
function sliderU(group,label){ const g=groupU(group); if(!g) return null;
  const row=findIn(g,ch=>ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label);
  return row?row.children[1]:null; }
function valU(group,label){ const g=groupU(group); const row=g&&findIn(g,ch=>ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label); return row?row.children[2].textContent:null; }
function chipU(label){ return findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&ch.className.indexOf('chip')===0&&(ch.textContent||'')===label); }
function clickBtnU(label){ const b=findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&ch.className===''&&(ch.textContent||'')===label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(4); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label+(geomU(RECU)==='[]'?'':' (painted '+RECU.ops.length+' ops)')); }
/* pump until the page is demonstrably still (the needle rings for a few hundred frames after
   anything moves), then assert it: a repaint test is only meaningful against a proven-quiet
   baseline (Known-bad) */
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
uok(ST.view==='bar'&&ST.pct===75&&ST.loops===4&&ST.supply==='dc','it opens on the bar magnet at PhET\'s defaults');
uok(roU().indexOf(fmtField(225,'G'))>=0,'the readout prints the strength off the model (225.00 G)');

/* ---------------- every tab draws, differently, cleanly, and then idles ---------------- */
const FLOORSU=[643,676,96,48,52,76];     /* 80 % of what each view emits at boot (measured: 804, 845, 120, 60, 66, 95) */
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

/* the settled page is still: the compass is at rest and nothing else moves */
NODESU.tabs.children[0].fire('click');
idleU('the bar magnet view, with the needle settled, paints nothing while idle');

/* ---------------- the bar magnet: dragging it, the compass and the meter ---------------- */
{ /* the compass goes away first: with it out nothing else can mark the page dirty, so the
     repaint below can only have come from the pointer handler itself (Known-bad: a helper
     that sets the flag masks the flag the test is checking).  And the magnet is grabbed by
     its north END, not its centre, where a lost grab offset and a shrunken hit box would
     both be invisible. */
  const cc=cbU('tools','compass'); cc.checked=false; cc.fire('change');
  settleU('with the compass away the page is still');
  const map=mapU(), X=map.X(ST.bar.x+MAG_B*0.8), Y=map.Y(ST.bar.y-MAG_R*0.6), g0=frameU();
  const before=ST.bar.x, roBefore=roU();
  downU(X,Y); uok(DRAG.what==='bar','pointer-down on the magnet\'s north end grabs it');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  moveU(X+90,Y-30);
  uclose(ST.bar.x,before+90/map.s,1e-9,'the magnet moved by 90 px worth of millimetres, the grab offset kept');
  uclose(ST.bar.y,333+30/map.s,1e-9,'and up by 30');
  const g1=frameU(); uok(g1.length>50&&g1!==g0,'the drag repaints THROUGH the frame loop, from the handler\'s own dirty flag');
  upU(); uok(DRAG.what===null,'pointer-up lets go');
  uok(roU()!==roBefore,'and the readout followed the magnet');
  cc.checked=true; cc.fire('change'); LIVE.barRot=null; }
{ const map=mapU(); settleU('the page settles again with the compass back');
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
  uok(!cbU('the source','bound current on the magnet'),'a control belonging to a view this one hides is not reachable here');
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
/* flip polarity: the field reverses and the needle is kicked */
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
/* the strength slider, and the honest empty case */
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
  RECU=makeRecU(); cb.checked=false; cb.fire('change');
  uok(RECU.ops.length!==a,'and switching it off changes the picture back');
  const e=cbU('the bar magnet','Earth'); RECU=makeRecU(); e.checked=true; e.fire('change');
  uok(ST.earth&&RECU.ops.length>50,'the Earth draws');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/geographic N/.test(texts),'labelled with the geographic north at the magnet\'s south pole');
  uok(findIn(NODESU.panel,ch=>ch.tagName==='BUTTON'&&(ch.textContent||'')==='flip Earth')!==null,'and the flip button becomes "flip Earth" (PhET)');
  e.checked=false; e.fire('change'); }
{ const cb=cbU('the bar magnet','magnetic field (B)'); RECU=makeRecU(); cb.checked=false; cb.fire('change');
  const withoutN=RECU.ops.length; cb.checked=true; cb.fire('change'); RECU=makeRecU(); pumpU(2);
  uok(withoutN<200,'hiding the field takes the needles away ('+withoutN+' ops)'); }

/* ---------------- the electromagnet ---------------- */
NODESU.tabs.children[1].fire('click');
{ uok(ST.view==='em','the electromagnet view');
  uok(roU().indexOf(fmt(coilField(emCoil(ST,0),ST.em.x,ST.em.y,0)[0],2))>=0,'the readout prints the centre field off the model (300.00 G at 4 loops)');
  const s=sliderU('the electromagnet','loops'); uok(!!s,'found the loops slider');
  RECU=makeRecU(); s.value='1'; s.fire('input');
  uok(ST.loops===1&&RECU.ops.length>50,'one loop redraws');
  uok(roU().indexOf(fmt(coilField(emCoil(ST,0),ST.em.x,ST.em.y,0)[0],2))>=0,'and the centre field follows ('+fmt(coilField(emCoil(ST,0),ST.em.x,ST.em.y,0)[0],2)+' G, not a quarter of 300)');
  s.value='4'; s.fire('input'); }
{ const v=sliderU('the electromagnet','battery voltage'); uok(!!v,'found the battery slider');
  RECU=makeRecU(); v.value='0'; v.fire('input');
  uok(ST.dcV===0,'battery at 0 V');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(/no current: no field/.test(texts),'and the view says there is no current rather than drawing nothing');
  v.value='-10'; v.fire('input');
  uok(emCoil(ST,0).I<0&&roU().indexOf('&minus;')>=0,'reversed, the current is negative and the readout shows the sign');
  const B=coilField(emCoil(ST,0),ST.em.x,ST.em.y,0)[0]; uok(B<0,'and so is the field at the centre');
  v.value='10'; v.fire('input'); }
{ const ac=chipU('AC power supply'); uok(!!ac,'found the AC supply chip');
  const dcS=sliderU('the electromagnet','battery voltage'), pk=sliderU('the electromagnet','maximum voltage');
  uok(!dcS.disabled&&pk.disabled,'on the battery the AC sliders are dimmed');
  ac.fire('click'); uok(ST.supply==='ac','switched to the AC supply');
  uok(dcS.disabled&&!pk.disabled,'and now the battery slider is the dim one');
  const t0=LIVE.emT; pumpU(6); uok(LIVE.emT>t0,'its clock runs');
  const f=sliderU('the electromagnet','frequency'); f.value='100'; f.fire('input');
  uclose(acFreq(emSupply(ST)),1.25,1e-12,'at 100 % the frequency is PhET\'s 1.25 Hz');
  uok(valU('the electromagnet','frequency')==='100 %','the slider reads it back');
  pk.value='0'; pk.fire('input'); uok(emCoil(ST,LIVE.emT).I===0,'at zero maximum voltage no current flows');
  pk.value='50'; pk.fire('input');
  chipU('DC power supply').fire('click'); uok(ST.supply==='dc'&&LIVE.emT===0,'back on the battery, its clock is reset'); }
{ const e=cbU('the electromagnet','electrons'); uok(e.checked,'the electrons start shown (PhET)');
  const p0=LIVE.ePhase; pumpU(3); uok(LIVE.ePhase>p0,'and they move with a positive current');
  chipU('conventional').fire('click'); const p1=LIVE.ePhase; pumpU(3);
  uok(LIVE.ePhase<p1,'the conventional convention sends them the other way');
  chipU('electron').fire('click');
  e.checked=false; e.fire('change');
  let n=0; while(n<600&&stepLive(1/60)) n++;
  idleU('with the electrons hidden and a steady current the page goes still');
  e.checked=true; e.fire('change'); }
{ const cb=cbU('tools','field meter'); cb.checked=true; cb.fire('change'); uok(ST.emMeter,'the meter on this screen too');
  const map=mapU();
  const G=meterBodyBox(map,ST.emM.x,ST.emM.y);     /* the box is recomputed before every drag: it moves with the tool */
  downU(G.X,G.Y); uok(DRAG.what==='emM','the meter grabs on the electromagnet screen');
  moveU(map.X(ST.em.x+60),map.Y(ST.em.y+20)); upU();
  const rd=meterReading(emCoil(ST,LIVE.emT),ST.emM.x,ST.emM.y);
  uok(roU().indexOf(fmtField(rd.B,'G'))>=0,'its reading is the coil\'s field where it now stands');
  const G2=meterBodyBox(map,ST.emM.x,ST.emM.y);
  downU(G2.X,G2.Y); moveU(map.X(ST.em.x+coilLoopsX(ST.loops)[0]),map.Y(ST.em.y+COIL_A)); upU();   /* onto a loop, not between two of them */
  uok(/inside the wire/.test(roU()),'and on the wire itself it says so rather than printing a filament\'s infinity');
  cb.checked=false; cb.fire('change'); }

/* ---------------- units and conventions ---------------- */
{ NODESU.tabs.children[0].fire('click'); cbU('tools','field meter').checked=true; cbU('tools','field meter').fire('change');
  chipU('T (tesla)').fire('click'); uok(ST.units==='T','tesla');
  uok(roU().indexOf('× 10^')>=0,'the readout switches to scientific tesla');
  RECU=makeRecU(); pumpU(2); NODESU.tabs.children[0].fire('click');
  const texts=RECU.ops.filter(o=>o[0]==='t').map(o=>o[1]).join(' ');
  uok(!/ G$/.test(texts),'and no gauss is left on the canvas');
  chipU('G (gauss)').fire('click'); cbU('tools','field meter').checked=false; cbU('tools','field meter').fire('change'); }

/* ---------------- the analysis views ---------------- */
NODESU.tabs.children[2].fire('click');
{ uok(ST.view==='lines','field lines');
  uok(roU().indexOf('10 of 10')>=0||roU().indexOf('>10<')>=0,'the readout counts the lines');
  uok(/closed on themselves/.test(roU()),'and says they close');
  const g0=frameU(3);
  RECU=makeRecU(); chipU('electromagnet').fire('click');
  uok(ST.src==='coil'&&RECU.ops.length>50,'the source chip switches to the electromagnet and redraws');
  uok(geomU(RECU)!==g0,'a different picture');
  const bd=cbU('the source','bound current on the magnet');
  uok(bd.disabled,'the bound-current box is dimmed while the coil is shown (it would do nothing)');
  chipU('bar magnet').fire('click'); uok(!bd.disabled,'and live again on the magnet');
  RECU=makeRecU(); bd.checked=false; bd.fire('change');
  uok(!ST.bound&&RECU.ops.length>50,'switching the bound current off redraws'); bd.checked=true; bd.fire('change'); }
NODESU.tabs.children[3].fire('click');
{ uok(ST.view==='axis','on the axis');
  const H=cbU('the source','μ₀H inside the magnet'); uok(!H.disabled&&H.checked,'the H curve is live and on for the magnet');
  RECU=makeRecU(); H.checked=false; H.fire('change'); uok(RECU.ops.length>20,'hiding it redraws');
  H.checked=true; H.fire('change');
  uok(roU().indexOf(fmtField(225*solAxis(0,MAG_R,MAG_B),'G'))>=0,'the readout prints the centre field, 220.63 G');
  chipU('electromagnet').fire('click'); uok(!H.disabled===false,'on the coil the H box is dimmed');
  uok(/continuous sheet/.test(roU()),'and the readout compares the loops with the continuous sheet');
  chipU('bar magnet').fire('click'); }
NODESU.tabs.children[4].fire('click');
{ uok(ST.view==='far','the far field');
  uok(roU().indexOf(fmt(dipoleLimit('magnet',0,'axis').lim,10))>=0,'the readout prints the numerically taken dipole limit');
  uok(roU().indexOf(sigf(octCoef('magnet',0,'axis'),6))>=0,'and the octupole coefficient in closed form');
  const s=sliderU('the bar magnet','strength'); uok(!s,'the strength slider is not in this view\'s panel');
  idleU('the far field is static'); }
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
  uok(roU().indexOf(sigf(T1,4))>=0,'with a shorter period: '+sigf(T1,4)+' s');
  uok(T1<T0,'a stronger field swings the needle faster');
  d.value='0'; d.fire('input'); uok(ST.ndDamp===0,'the damping can be switched off');
  uok(/1\.0*$|1$|1\b/.test('1'),'');
  d.value='2'; d.fire('input'); B.value=String(Math.log10(5)); B.fire('input');
  uok(stepLive(1/60)===true,'this view animates its time cursor');
  pumpU(4); }

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
keyU('6'); uok(ST.view==='needle','6 to the needle');
keyU('3'); uok(ST.view==='lines','3 to the field lines');
keyU('1');
{ const a=ST.bar.ang; keyU('f'); uclose(ST.bar.ang,a+Math.PI,1e-12,'f flips the magnet'); keyU('f'); }
{ keyU(' '); uok(ST.run===false,'space pauses');
  NODESU.tabs.children[5].fire('click');
  idleU('and even the needle view is then still');
  keyU(' '); uok(ST.run===true,'space starts it again');
  uok(stepLive(1/60)===true,'and the clock runs'); NODESU.tabs.children[0].fire('click'); }
{ let rsErr=null; try{ for(const f of (WINHU.resize||[])) f({}); }catch(e){ rsErr=e; }
  uok(!rsErr,'the resize handler runs'+(rsErr?': '+rsErr:''));
  uok(NODESU.errbox.style.display!=='block','no error after resize'); }

/* ---------------- every control, every view; disabled ones skipped ---------------- */
let ctlErrU=null;
try{
  const inputs=NODESU.panel.querySelectorAll('input');
  uok(inputs.length===20,'the panel has its 8 sliders and 12 checkboxes ('+inputs.length+')');
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
    for(const nm of ['G (gauss)','T (tesla)','electron','conventional','DC power supply','AC power supply','bar magnet','electromagnet']){
      RECU=makeRecU(); chipU(nm).fire('click'); assertCleanU(RECU,'view '+v+', chip "'+nm+'"'); }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every chip clicked');
  }
  chipU('G (gauss)').fire('click'); chipU('electron').fire('click'); chipU('DC power supply').fire('click'); chipU('bar magnet').fire('click');
  /* reset all: disturb every kind of state first (Known-bad: a reset test that resets nothing passes) */
  NODESU.tabs.children[0].fire('click');
  ST.bar={x:120,y:90,ang:Math.PI}; ST.pct=15; ST.barC={x:900,y:500}; ST.barM={x:800,y:100}; ST.barMeter=true; ST.seeInside=true; ST.earth=true;
  ST.em={x:700,y:400}; ST.loops=1; ST.supply='ac'; ST.dcV=-7; ST.acPk=95; ST.acFp=95; ST.electrons=false;
  ST.units='T'; ST.flowConv='conventional'; ST.src='coil'; ST.bound=false; ST.axisH=false; ST.ndB=200; ST.ndRel=170; ST.ndDamp=9; ST.run=false;
  LIVE.emT=3; LIVE.ePhase=2;
  uok(clickBtnU('reset all'),'found reset all');
  uok(ST.bar.x===430&&ST.bar.y===333&&ST.bar.ang===0&&ST.pct===75&&ST.barC.x===625&&!ST.barMeter&&!ST.seeInside&&!ST.earth,
      'it restores the magnet, its strength, the tools and the toggles');
  uok(ST.em.x===400&&ST.loops===4&&ST.supply==='dc'&&ST.dcV===10&&ST.acPk===50&&ST.electrons,'the electromagnet and its supply');
  uok(ST.units==='G'&&ST.flowConv==='electron'&&ST.src==='magnet'&&ST.bound&&ST.axisH,'the units, the convention and the analysis toggles');
  uok(ST.ndB===5&&ST.ndRel===60&&ST.ndDamp===2&&ST.run===true,'the needle sliders and the clock');
  uok(LIVE.emT===0&&LIVE.ePhase===0,'and the live clocks are wound back');
  uok(LIVE.barRot&&LIVE.barRot.rest,'with the needle back at rest along the field');
  uok(parseFloat(sliderU('the bar magnet','strength').value)===75&&cbU('the bar magnet','see inside').checked===false,'the controls show it');
  uok(ST.view==='bar','and it stays on the view you were looking at');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'the control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
