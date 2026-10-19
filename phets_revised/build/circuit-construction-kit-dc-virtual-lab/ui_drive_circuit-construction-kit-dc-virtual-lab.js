/* ======= UI drive test for circuit-construction-kit-dc-virtual-lab.html ======= *
 * DOM-stub pattern (lineage: tools/ui_drive.js via build_buoy/ui_drive_bu.js and
 * build/charges-and-fields, whose stub derives textContent from innerHTML).
 * The lab animates its charges whenever current flows and "show current" is on,
 * so every repaint assertion first switches that off (or uses an analysis view)
 * and PROVES the loop idle before acting.  The circuit is BUILT here by dragging
 * parts out of the toolbox and dropping their ends on each other, through the
 * canvas's own pointer events and the real frame loop.  The shared harness's
 * three sim-specific thresholds: 5 tabs, 8 panel groups, 11 inputs.          */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };
const ueq=(a,b,n)=>uok(a===b,n+' ['+a+' vs '+b+']');
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
/* pump real frames: the only path on which the dirty flag matters */
function pumpU(n){ for(let i=0;i<(n||1);i++){ const f=RAFU; if(!f) return; RAFU=null; TNOWU+=16; f(TNOWU); } }
function keyU(k){ for(const f of (WINHU.keydown||[])) f({key:k,preventDefault(){}}); }
function findLabelledU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* whole-label match (Known-bad: a substring lookup hit the wrong control) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
const sliderInU=label=>{ const r=sliderU(label); return r?r.children[1]:null; };
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
function frameU(){ RECU=makeRecU(); pumpU(3); return geomU(RECU); }
const roU=()=>NODESU.readout.innerHTML;
const downU=(x,y)=>NODESU.scene.fire('pointerdown',{clientX:x,clientY:y});
const moveU=(x,y)=>NODESU.scene.fire('pointermove',{clientX:x,clientY:y,buttons:1});
const upU=()=>NODESU.scene.fire('pointerup',{});
const GU=()=>labGeo(1400,820,ST);
const toolU=k=>{ const it=GU().tb.items.find(q=>q.key===k); return [it.x+it.w/2,it.y+it.h/2]; };
const w2sU=(x,y)=>{ const m=GU().map; return [m.X(x),m.Y(y)]; };
const vxU=id=>{ const v=vById(ST.circ,id); return w2sU(v.x,v.y); };
/* a full drag through the canvas's handlers: press, two moves, release */
function dragU(p,q){ downU(p[0],p[1]); moveU((p[0]+q[0])/2,(p[1]+q[1])/2); moveU(q[0],q[1]); upU(); }
function tapU(p){ downU(p[0],p[1]); upU(); }

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
ueq(NODESU.tabs.children.length,5,'five view tabs were built');
ueq(NODESU.panel.children.length,8,'the control panel has its 8 groups');
uok(roU().length>300,'the readout rendered');
uok(NODESU.eqbar.innerHTML.indexOf('NaN')<0&&NODESU.eqbar.innerHTML.length>50,'the equation bar rendered');
uok(ST.view==='lab'&&ST.preset==='bulb'&&ST.circ.els.length===8,'it opens on the lab with one bulb');
uok(roU().indexOf(fmtRes(solutionOf(ST).law.kcl))>=0,'the readout reports the current law\'s residual off the model');
uok(findLabelledU('show current').checked&&!findLabelledU('values').checked&&findLabelledU('labels').checked,'PhET\'s defaults: current on, values off, labels on');
uok(chipU('lifelike',2).className==='chip on'&&chipU('electrons',2).className==='chip on'&&chipU('zoom 1×',3).className==='chip on','lifelike, electrons, zoom 1 (PhET)');

/* ---- every tab draws, differently, cleanly; the analysis views idle ---- */
const FLOORSU=[180,80,40,40,18];      /* ~65 % of what each view emits on the default one-bulb circuit (graph 118, superposition 27 measured) */
const sigsU={};
for(let i=0;i<5;i++){
  RECU=makeRecU(); NODESU.tabs.children[i].fire('click');
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  ueq(NODESU.tabs.children[i].className,'active','tab '+i+' is marked active');
  sigsU['t'+i]=sigU(RECU);
  if(i>0) idleU('tab '+i+' paints nothing while idle (an analysis view never animates)');
}
uok(new Set(Object.values(sigsU)).size===5,'every tab draws a different picture');

/* ---- the lab moves by itself while current flows, and stops when told ---- */
NODESU.tabs.children[0].fire('click'); pumpU(3);
{ RECU=makeRecU(); pumpU(1); const g1=geomU(RECU); RECU=makeRecU(); pumpU(1); const g2=geomU(RECU);
  uok(g1.length>50&&g2.length>50&&g1!==g2,'with current on, every frame repaints and the charges have moved');
  const cb=findLabelledU('show current'); cb.checked=false; cb.fire('change'); ueq(ST.showCurrent,false,'show current off');
  idleU('with the current hidden the lab is still');
  NODESU.tabs.children[1].fire('click'); idleU('the graph view is still');
  cb.checked=true; cb.fire('change'); idleU('and stays still even with the current shown');
  NODESU.tabs.children[0].fire('click'); pumpU(2); RECU=makeRecU(); pumpU(1); uok(geomU(RECU).length>50,'back in the lab, the charges run again');
  cb.checked=false; cb.fire('change'); }

/* ---- build a circuit by hand, from an empty bench ---- */
chipU('empty',7).fire('click'); ueq(ST.circ.els.length,0,'the empty chip clears the bench (PhET\'s start)');
idleU('the empty bench idles');
{ RECU=makeRecU(); pumpU(2); }
{ const g0=frameU(); idleU('proven idle before the first drag');
  const p=toolU('battery'); downU(p[0],p[1]); uok(DRAG.what==='el'&&ST.circ.els.length===1,'pressing the toolbox\'s battery picks a battery up');
  idleU('the pick-up\'s own repaint has drained (proven-idle baseline)');
  const q=w2sU(0,100); moveU(q[0],q[1]); const g1=frameU(); uok(g1.length>50&&g1!==g0,'dragging it repaints THROUGH the frame loop, and the picture moved');
  idleU('and goes idle again'); upU(); uok(DRAG.what===null,'release');
  const b=ST.circ.els[0]; uclose(vById(ST.circ,b.a).x,-51,1e-9,'the battery lies where it was dropped');
  uok(roU().indexOf('none on the bench')<0&&roU().indexOf('1 (0 wires)')>=0,'the readout counts it'); }
dragU(toolU('bulb'),w2sU(0,-60)); dragU(toolU('wire'),w2sU(100,20)); dragU(toolU('wire'),w2sU(-100,20));
ueq(ST.circ.els.map(e=>e.type).join(','),'battery,bulb,wire,wire','battery, bulb and two wires on the bench');
{ const [bat,bulb,w1,w2]=ST.circ.els;
  idleU('idle before joining ends');
  const g0=frameU(); idleU('proven idle');
  downU(...w2sU(50,20)); ueq(DRAG.what,'vert','pressing a wire\'s end grabs the end');
  idleU('grab drained'); moveU(...w2sU(55,96)); const g1=frameU(); uok(g1!==g0,'dragging the end repaints through the loop');
  const tgt=dropTarget(ST.circ,[DRAG.vid]); uok(tgt&&tgt.dst===bat.b,'while it is within reach, the + terminal is the drop target the ring marks'); upU();
  ueq(w1.a,bat.b,'released within 30 units of the + terminal, the wire joins it');
  dragU(w2sU(150,20),w2sU(46,-52)); ueq(w1.b,bulb.b,'its other end joins the bulb');
  dragU(w2sU(-50,20),w2sU(-55,-66)); ueq(w2.b,bulb.a,'the second wire joins the bulb');
  idleU('idle before closing the loop'); const ro0=roU();
  dragU(w2sU(-150,20),w2sU(-47,93)); ueq(w2.a,bat.a,'and closes the loop at the - terminal');
  uok(roU()!==ro0,'closing the loop changed the readout');
  const SOL=solutionOf(ST), I=Math.abs(SOL.I.get(bulb.id));
  const Rw=wireR(elLength(ST.circ,w1),RHO_MIN)+wireR(elLength(ST.circ,w2),RHO_MIN);
  uclose(I,9/(1e-4+10+Rw),1e-14,'the hand-built loop carries E/(r + R + wires)');
  ueq(SOL.loops,1,'one loop'); uok(roU().indexOf(fmtRes(SOL.law.kcl))>=0,'and the readout checks Kirchhoff on it');
  /* tap the bulb: selected, its slider live */
  tapU(w2sU(0,-60)); ueq(ST.sel,bulb.id,'a tap on the bulb selects it');
  uok(!sliderU('resistance, &Omega;').hidden&&sliderU('voltage, V').hidden&&sliderU('current rating, A').hidden,'its resistance slider is shown, the others are not');
  uok(roU().indexOf(fmtI(I))>=0,'the readout shows the selected bulb\'s current ('+fmtI(I)+')');
  idleU('idle before the resistance slider');
  const s=sliderInU('resistance, &Omega;'); RECU=makeRecU(); s.value='20'; s.fire('input');
  uok(RECU.ops.length>100,'the slider repaints at once ('+RECU.ops.length+' ops)'); ueq(bulb.R,20,'the bulb is now 20 ohm');
  uclose(Math.abs(solutionOf(ST).I.get(bulb.id)),9/(1e-4+20+Rw),1e-14,'and the current fell to E/(r + 20 + wires)');
  /* the battery: voltage, reverse */
  tapU(w2sU(0,100)); ueq(ST.sel,bat.id,'a tap on the battery selects it'); uok(!sliderU('voltage, V').hidden,'its voltage slider appears');
  uok(sliderU('resistance, &Omega;').hidden&&sliderU('current rating, A').hidden,'and the resistance and rating sliders go (a live but ignored control is worse than none)');
  const sv=sliderInU('voltage, V'); sv.value='4.5'; sv.fire('input'); ueq(bat.E,4.5,'4.5 V');
  uclose(Math.abs(solutionOf(ST).I.get(bulb.id)),4.5/(1e-4+20+Rw),1e-14,'the current halves');
  const Ib=solutionOf(ST).I.get(bulb.id); uok(clickU('reverse'),'the reverse button'); uclose(solutionOf(ST).I.get(bulb.id),-Ib,1e-15,'reverses every current');
  /* values on the canvas */
  const cv=findLabelledU('values'); cv.checked=true; cv.fire('change'); RECU=makeRecU(); pumpU(2); NODESU.tabs.children[0].fire('click');
  uok(textsU(RECU).indexOf('20.0 Ω')>=0&&textsU(RECU).indexOf('4.5 V')>=0,'values on: the bulb and the battery are labelled 20.0 Ω and 4.5 V');
  /* schematic, and back */
  idleU('idle before the look chips'); const gl=frameU(); idleU('proven idle');
  RECU=makeRecU(); chipU('schematic',2).fire('click'); const gs=geomU(RECU); uok(gs.length>50&&gs!==gl,'schematic redraws every part as a symbol'); ueq(ST.look,'schematic','schematic');
  uok(chipU('schematic',2).className==='chip on'&&chipU('lifelike',2).className==='chip','the clicked chip lights and the other goes dark');
  chipU('lifelike',2).fire('click'); ueq(ST.look,'lifelike','and back to lifelike');
  /* zoom: chips and the wheel */
  chipU('zoom 1.6×',3).fire('click'); ueq(ST.zoom,1.6,'zoom 1.6'); chipU('zoom 1×',3).fire('click');
  /* the baseline is a real drawing at zoom 1, not an idle frame (Known-bad: a
     repaint always differs from an empty capture) */
  idleU('idle before the wheel'); RECU=makeRecU(); NODESU.tabs.children[0].fire('click'); const gz=geomU(RECU); idleU('proven idle after the forced draw');
  NODESU.scene.fire('wheel',{deltaY:-100}); ueq(ST.zoom,1.6,'the wheel zooms in'); const gz2=frameU();
  uok(gz.length>50&&gz2.length>50&&gz2!==gz,'and the zoomed bench repaints through the loop, differently from the same bench at zoom 1');
  NODESU.scene.fire('wheel',{deltaY:120}); ueq(ST.zoom,1,'and back out'); }

/* ---- a switch, tapped ---- */
{ dragU(toolU('switch'),w2sU(0,230)); const sw=ST.circ.els[ST.circ.els.length-1]; ueq(sw.type,'switch','a switch on the bench'); ueq(sw.closed,false,'open, as PhET makes it');
  idleU('idle before the tap'); RECU=makeRecU(); NODESU.tabs.children[0].fire('click'); const g0=geomU(RECU); idleU('proven idle after the forced draw');
  RECU=makeRecU(); tapU(w2sU(0,230)); ueq(sw.closed,true,'a tap closes it'); const g1=geomU(RECU); uok(g1!==g0&&g1.length>50,'and the release repaints at once with the lever closed');
  idleU('then idles');
  uok(!buttonU('toggle the switch').hidden,'its toggle button is shown'); clickU('toggle the switch'); ueq(sw.closed,false,'the button opens it');
  /* into the toolbox: gone */
  const n=ST.circ.els.length; dragU(w2sU(0,230),toolU('coin')); ueq(ST.circ.els.length,n-1,'dragged onto the toolbox it is put away'); }

/* ---- delete, split, keys ---- */
{ const w1=ST.circ.els[2], A=vById(ST.circ,w1.a), B=vById(ST.circ,w1.b); tapU(w2sU((A.x+B.x)/2,(A.y+B.y)/2)); ueq(ST.sel,w1.id,'a tap on a wire selects it');
  uok(!buttonU('delete').hidden,'delete is offered'); clickU('delete'); uok(!elById(ST.circ,w1.id),'and removes the wire');
  ueq(solutionOf(ST).loops,0,'the loop is open');
  /* the joint by what it holds, not by a terminal name: the battery was
     reversed above, which swaps its a and b (an earlier draft split a joint
     that already held one part, and "x splits it" passed doing nothing) */
  const bat=ST.circ.els[0], jv=[bat.a,bat.b].find(v=>elsAt(ST.circ,v).length===2);
  uok(jv!==undefined,'the battery still has one joint of two parts');
  const lone=[bat.a,bat.b].find(v=>v!==jv); tapU(vxU(lone)); ueq(ST.selV,lone,'a tap on its lone end selects it');
  uok(buttonU('split the junction').hidden,'and no split is offered for an end holding one part');
  tapU(vxU(jv)); ueq(ST.selV,jv,'a tap on the two-part joint selects it');
  uok(!buttonU('split the junction').hidden,'and the split button is shown');
  const nv0=ST.circ.verts.length; keyU('x'); ueq(elsAt(ST.circ,jv).length,1,'x splits it'); ueq(ST.circ.verts.length,nv0+1,'into one more vertex');
  const k0=ST.circ.els.length; tapU(w2sU(0,-60)); keyU('Delete'); ueq(ST.circ.els.length,k0-1,'the delete key removes the selected part'); }

/* ---- a fuse that blows, and is repaired ---- */
chipU('short circuit',7).fire('click'); ueq(ST.preset,'short','the short-circuit chip');
uok(roU().indexOf('Fire')>=0,'the readout calls the fire');
{ tapU(w2sU(0,-40)); ueq(ST.sel,2,'select the top wire'); clickU('delete'); ueq(ST.circ.els.length,3,'and delete it');
  dragU(toolU('fuse'),w2sU(0,-44)); const f=ST.circ.els[ST.circ.els.length-1]; ueq(f.type,'fuse','a fuse dropped into the gap');
  uok(f.a===3||f.b===3||f.a===2||f.b===2,'joined at one end by the drop');
  const free=[f.a,f.b].find(v=>elsAt(ST.circ,v).length===1); uok(free!==undefined,'with one end still loose');
  const tgt=[2,3].find(v=>vById(ST.circ,v)&&elsAt(ST.circ,v).length===1); dragU(vxU(free),vxU(tgt));
  uok(f.tripped,'closing the short through a 4-A fuse blows it'); ueq(solutionOf(ST).Imax,0,'and nothing flows');
  uok(roU().indexOf('blown fuse')>=0,'the readout says so');
  tapU(w2sU(0,-40)); ueq(ST.sel,f.id,'select the fuse');
  uok(!sliderU('current rating, A').hidden&&!buttonU('repair the fuse').disabled,'its rating slider and repair button are live');
  const sr=sliderInU('current rating, A'); sr.value='20'; sr.fire('input'); ueq(f.rating,20,'rated 20 A');
  /* repair where it can be seen: a soft battery (10 ohm) drives only 0.9 A round the short */
  const sb=sliderInU('battery resistance'); sb.value=String(LOG_RBAT[1]); sb.fire('input'); uok(f.tripped,'softening the battery does not mend a blown fuse');
  clickU('repair the fuse'); uok(!f.tripped,'repaired, the 20-A fuse holds 0.9 A');
  uclose(Math.abs(solutionOf(ST).I.get(f.id)),9/(10+fuseR(20)+wireR(elLength(ST.circ,ST.circ.els[1]),RHO_MIN)+wireR(elLength(ST.circ,ST.circ.els[2]),RHO_MIN)),1e-12,'and carries E/(r + its 3 milliohm + wires)');
  uok(roU().indexOf('blown fuse')<0,'the readout stops calling it blown');
  sb.value=String(LOG_RBAT[0]); sb.fire('input'); uok(f.tripped,'back to the stiff battery, 600 A blows it again at once'); }

/* ---- the meters ---- */
chipU('one bulb',7).fire('click');
{ const cvm=findLabelledU('voltmeter'); cvm.checked=true; cvm.fire('change'); ueq(ST.vm.on,true,'the voltmeter box puts it on the bench');
  uok(roU().indexOf(voltageText(REF.presets.bulb.v[1]-REF.presets.bulb.v[0]))>=0,'its default probes read the battery (9.00 V) in the readout');
  idleU('idle before the probe'); const g0=frameU(); idleU('proven idle');
  const G=GU(), vg=vmGeo(G,ST); downU(vg.red.T[0],vg.red.T[1]); ueq(DRAG.what,'vm-red','the red probe grabs');
  moveU(...w2sU(150,20)); const g1=frameU(); uok(g1!==g0,'dragging it repaints'); upU();
  uok(roU().indexOf(voltageText((REF.presets.bulb.v[2]+REF.presets.bulb.v[3])/2-REF.presets.bulb.v[0]))>=0,'on the middle of a wire it reads the interpolated voltage');
  dragU(vmGeo(GU(),ST).c,toolU('battery')); ueq(ST.vm.on,false,'dropped on the toolbox, it goes away');
  uok(!findLabelledU('voltmeter').checked,'and its box unticks');
  dragU(toolU('probe'),w2sU(260,120)); ueq(ST.am.on,true,'the non-contact ammeter comes out of the toolbox');
  const ag=amGeo(GU(),ST); dragU(ag.ring.c,w2sU(0,-60));
  const rd=buildModel().am; uok(rd&&rd.el===4,'its ring over the bulb reads the bulb'); uok(roU().indexOf(currentText(Math.abs(REF.presets.bulb.i['4']),false))>=0,'0.90 A in the readout');
  const cam=findLabelledU('non-contact ammeter'); cam.checked=false; cam.fire('change'); ueq(ST.am.on,false,'and its box puts it away'); }

/* ---- advanced: resistivity, battery resistance, real bulbs ---- */
{ const sr=sliderInU('wire resistivity'); sr.value=String(LOG_RHO[1]); sr.fire('input'); ueq(ST.rho,RHO_MAX,'the resistivity slider reaches PhET\'s 0.0168 ohm m exactly');
  uclose(Math.abs(solutionOf(ST).I.get(4)),REF.variants.bulb_rhomax.i['4'],1e-15,'and the one-bulb current drops to python\'s value for it');
  sr.value=String(LOG_RHO[0]); sr.fire('input'); ueq(ST.rho,RHO_MIN,'and back to 1e-10');
  const sb=sliderInU('battery resistance'); sb.value=String(Math.log10(2)); sb.fire('input'); uclose(ST.rbat,2,1e-12,'battery resistance 2 ohm');
  uclose(Math.abs(solutionOf(ST).I.get(4)),REF.variants.bulb_r2.i['4'],1e-12,'the current is python\'s for r = 2 ohm');
  sb.value=String(LOG_RBAT[0]); sb.fire('input'); ueq(ST.rbat,BATT_R_MIN,'back to 1e-4');
  const n0=GU().tb.items.length; const cr=findLabelledU('add real bulbs'); cr.checked=true; cr.fire('change');
  ueq(GU().tb.items.length,n0+1,'add real bulbs puts the real bulb in the toolbox');
  dragU(toolU('rbulb'),w2sU(0,240)); ueq(ST.circ.els[ST.circ.els.length-1].type,'rbulb','and one can be taken out');
  cr.checked=false; cr.fire('change'); }

/* ---- labels ---- */
{ NODESU.tabs.children[0].fire('click'); RECU=makeRecU(); pumpU(1); NODESU.tabs.children[0].fire('click'); const withL=textsU(RECU).filter(t=>t==='battery').length;
  const cl=findLabelledU('labels'); cl.checked=false; cl.fire('change'); RECU=makeRecU(); NODESU.tabs.children[0].fire('click');
  uok(withL>=1&&textsU(RECU).indexOf('battery')<0,'labels off hides the toolbox names'); cl.checked=true; cl.fire('change'); }

/* ---- the rest of the circuit: stepping the part ---- */
chipU('two batteries',7).fire('click'); NODESU.tabs.children[3].fire('click');
{ const f0=focusElement(ST,solutionOf(ST)); uok(!buttonU('next part').hidden,'the part stepper is shown in this view');
  idleU('the view idles'); RECU=makeRecU(); clickU('next part'); const f1=focusElement(ST,solutionOf(ST));
  uok(f1!==f0,'next part moves the view to another part'); uok(RECU.ops.length>20,'and redraws');
  clickU('previous part'); ueq(focusElement(ST,solutionOf(ST)),f0,'previous part comes back');
  uok(roU().indexOf(fmtV(theveninOf(solutionOf(ST),f0).Voc))>=0,'the readout prints that part\'s V_th off the model');
  idleU('proven idle (the buttons forced a draw)'); downU(400,300); moveU(500,340); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','the view ignores the pointer, as designed'); upU(); }

/* ---- keyboard ---- */
keyU('3'); ueq(ST.view,'power','3 is the power budget'); keyU('5'); ueq(ST.view,'super','5 superposition'); keyU('1'); ueq(ST.view,'lab','1 the lab');

/* ---- every control: sliders at both ends and the middle, every checkbox, every chip ---- */
let ctlErrU=null;
try{ const inputs=NODESU.panel.querySelectorAll('input');
  ueq(inputs.length,11,'the panel has its 5 sliders and 6 checkboxes');
  for(let v=0;v<5;v++){ NODESU.tabs.children[v].fire('click');
    for(const sel of [0,3,5]){ ST.sel=sel; ST.selV=null;
      for(const inp of inputs){ if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); inp.checked=!inp.checked; inp.fire('change'); continue; }
        const lo=parseFloat(inp.min), hi=parseFloat(inp.max); for(const x of [lo,hi,(lo+hi)/2]){ inp.value=String(x); inp.fire('input'); } } }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every control driven without error'); }
  for(let v=0;v<5;v++){ NODESU.tabs.children[v].fire('click');
    for(const nm of ['empty','one bulb','series','parallel','Wheatstone bridge','two batteries','short circuit']){ RECU=makeRecU(); chipU(nm,7).fire('click'); assertCleanU(RECU,'view '+v+', '+nm); }
    uok(NODESU.errbox.style.display!=='block','view '+v+': every preset draws'); }
  for(const nm of ['conventional','electrons']){ chipU(nm,2).fire('click'); ueq(ST.carrier,nm,'the '+nm+' chip'); }
  for(const f of (WINHU.resize||[])) f(); uok(NODESU.errbox.style.display!=='block','resize handled');
  /* reset all: disturb every kind of state first (Known-bad: a reset test that resets nothing passes) */
  NODESU.tabs.children[0].fire('click'); chipU('parallel',7).fire('click'); ST.look='schematic'; ST.zoom=0.5; ST.rho=RHO_MAX; ST.rbat=5; ST.realBulbs=true;
  ST.vm.on=true; ST.am.on=true; ST.carrier='conventional'; ST.showValues=true; ST.sel=3; ST.circ.els[5].R=77;
  uok(clickU('reset all'),'found reset all');
  uok(ST.preset==='bulb'&&ST.circ.els.length===8&&ST.look==='lifelike'&&ST.zoom===1&&ST.rho===RHO_MIN&&ST.rbat===BATT_R_MIN&&!ST.realBulbs&&!ST.vm.on&&!ST.am.on&&ST.carrier==='electrons'&&!ST.showValues&&ST.sel===null,
    'reset all restores the circuit, the look, the zoom, the wire, the batteries, the meters and the selection');
  uok(!findLabelledU('values').checked&&chipU('lifelike',2).className==='chip on'&&chipU('one bulb',7).className==='chip on','and the controls show it');
  ueq(ST.view,'lab','and keeps the view');
}catch(e){ ctlErrU=e; }
uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
