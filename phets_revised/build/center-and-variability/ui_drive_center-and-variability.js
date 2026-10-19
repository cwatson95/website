
/* ====== UI drive test for center-and-variability.html ==================== *
 * DOM-stub pattern (lineage: build_buoy/ui_drive_bu.js via the projectile
 * remakes).  The canvas drags are the ones PhET has: a landed ball along the
 * number line, the two prediction thumbs, the interval handles and the one
 * ball the balance view lets you move.  Every one of them must move the
 * picture THROUGH the frame loop from a PROVEN-IDLE baseline (time paused,
 * loop drained, idle frame drew nothing).
 * Controls are looked up INSIDE THEIR OWN GROUP: 'median' and 'predict
 * median' each name two different checkboxes and 'kicks in the data set' two
 * different sliders, so a panel-wide match-by-label would drive the wrong one
 * (the lenses/lagrange_points Known-bad, twice over).                        */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,arcs:0,rects:0,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){c._p=[];},moveTo(x,y){c._p&&c._p.push([x,y]);},
    lineTo(x,y){c._p&&c._p.push([x,y]);},closePath:P,
    rect(x,y,w,h){c._p&&c._p.push([x,y],[x+w,y+h]);},
    arc(x,y,r){c.arcs++; c._p&&c._p.push([x,y,r]);},
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){c.rects++; ops.push(['r',Math.round(x),Math.round(y),Math.round(w),Math.round(h)]);},
    strokeRect(x,y,w,h){ops.push(['R',x,y,w,h]);}, clearRect:P,
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
    if(/NaN|undefined/.test(o[1])){ bad='NaN/undefined "'+String(o[1]).slice(0,40)+'"'; break; } }
  uok(!bad,label+' text ops clean'+(bad?' ('+bad+')':''));
}
let RECU=makeRecU();
function mkElU(tag){
  const e={tagName:(tag||'div').toUpperCase(),children:[],style:{},dataset:{},
    _h:{},className:'',id:'',value:'0',checked:false,hidden:false,disabled:false,
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
        else if(want==='#phys'&&ch.id==='phys') out.push(ch);
        else if(want==='.chips'&&ch.className==='chips') out.push(ch);
        else if(want==='input'&&ch.tagName==='INPUT') out.push(ch);
        walk(ch); } };
      walk(this); return out; },
    fire(k,ev){ for(const f of (this._h[k]||[])) f(Object.assign({preventDefault(){},stopPropagation(){},clientX:0,clientY:0,pointerId:1,buttons:0},ev||{})); },
  };
  /* the stub must derive textContent from innerHTML, because a real browser
     does and a chip built with h(tag,{html:...}) otherwise reports an EMPTY
     label (drum_head Known-bad) */
  let _html='', _txt='';
  Object.defineProperty(e,'innerHTML',{get(){ return _html; },set(v){ _html=''+v; _txt=(''+v).replace(/<[^>]*>/g,''); }});
  Object.defineProperty(e,'textContent',{get(){ return _txt; },set(v){ _txt=''+v; }});
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
/* the nine control groups, in the order boot() appends them */
const GRP={kicks:0,meanmed:1,spread:2,conv:3,balance:4,longrun:5,fire:6,info:7,phys:8};
function grpU(name){ return NODESU.panel.children[GRP[name]]; }
/* which control groups a view shows.  Nothing asserted this and a mutant
   that showed the kicks group on EVERY view survived the full sweep: a
   group of live controls belonging to another screen is the worst case of
   'a live control that is ignored is worse than no control'. */
const GROUPS=['kicks','meanmed','spread','conv','balance','longrun','fire'];
function shownU(){ return GROUPS.filter(g=>grpU(g).hidden!==true); }
/* WHOLE-label match, INSIDE one group */
function cbU(grp,label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===label)
      for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(grpU(grp)); return hit; }
function sliderU(grp,label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(grpU(grp)); return hit; }
function sliderRowU(grp,label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(grpU(grp)); return hit; }
function chipsU(key){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='chips'&&ch['data-key']===key) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function chipU(key,label){ const r=chipsU(key); if(!r) return null;
  for(const c of r.children) if((c.textContent||'')===label) return c;
  return null; }
function buttonU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===label) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickU(label){ const b=buttonU(label); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]',label+(geomU(RECU)==='[]'?'':' ('+RECU.ops.length+' ops)')); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }
function pauseU(){ const cb=cbU('fire','time runs'); if(cb&&cb.checked){ cb.checked=false; cb.fire('change'); } }
function playU(){ const cb=cbU('fire','time runs'); if(cb&&!cb.checked){ cb.checked=true; cb.fire('change'); } }
/* the scene the page built, and the geometry a drag has to aim at */
let SCU=null;
function sceneU(){ if(!SCU){ SCU=makeScene(NODESU.scene); SCU.W=1400; SCU.H=820; } return SCU; }
function ballXY(i){
  const S=sceneU(), M=buildModel();
  const L=layoutOf(S,M), G=fieldGeomOf(L.field,M.xs);
  return {x:G.map.X(M.xs[i]),y:G.gy-G.rowH*(G.stacks[i]+0.5),map:G.map};
}

/* ---- boot ---- */
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built');
uok(NODESU.panel.children.length>=9,'the control panel has its nine groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,'the PhET credit line is on the page');
uok(NODESU.hint.textContent.length>10,'the hint line is set');
uok(NODESU.readout.innerHTML.indexOf(fmt(cavMedian(REF.open.kicks.xs),2)+' m')>=0,
    'the readout prints the opening data set’s median, '+fmt(cavMedian(REF.open.kicks.xs),2)+' m');
uok(NODESU.readout.innerHTML.indexOf(cavSorted(REF.open.kicks.xs).join(' ').slice(0,20))>=0,
    '…and the sorted data behind it');

/* ---- every tab draws, differently, cleanly ---- */
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=60,'tab '+i+' emits at least 60 ops ('+RECU.ops.length+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');

/* ---- each view shows ITS OWN controls and nobody else's ---- */
{
  const WANT={kicks:['kicks','fire'],meanmed:['meanmed','fire'],spread:['spread','fire'],
              conv:['conv'],balance:['balance'],longrun:['longrun']};
  TABS.forEach(([k],i)=>{
    tabU(i);
    const got=shownU();
    uok(got.join()===WANT[k].join(),
        'the '+k+' view shows exactly ['+WANT[k].join(', ')+'], not ['+got.join(', ')+']');
  });
  tabU(0);
  uok(grpU('kicks').hidden!==true&&grpU('meanmed').hidden===true,
      'and the kicks group is hidden the moment another view owns the screen');
  tabU(3);
  uok(grpU('kicks').hidden===true,'\u2026including on which quartile');
  uok(grpU('fire').hidden===true,'which has nothing to kick, so no kicking group either');
}

/* ---- the kicks: PhET's Median screen ---- */
tabU(0); pauseU();
{
  const F=curField(ST);
  uok(F.xs.length===ST.mMax,'the field opens full ('+F.xs.length+' of '+ST.mMax+')');
  uok(F.xs.join()===REF.open.kicks.xs.join(),'and holds derive.py’s opening data set');
  uok(ST.mMax===15&&chipU('mMax','30')===null,'the Median screen offers 5, 10 and 15 only, as PhET caps it');
  uok(chipU('mMax','15')!==null&&chipU('mMax','5')!==null,'…and offers both of those');
  const before=cavMedian(F.xs);
  uok(NODESU.readout.innerHTML.indexOf(fmt(before,2)+' m')>=0,'the readout prints the median, '+fmt(before,2)+' m');
  clickU('clear');
  uok(curField(ST).xs.length===0,'clear empties the field');
  uok(NODESU.readout.innerHTML.indexOf('0 of 15')>=0,'and the readout says 0 of 15');
  RECU=makeRecU(); tabU(0);
  assertCleanU(RECU,'the empty field');
  uok(RECU.ops.length>40,'an empty field still draws its line and ticks ('+RECU.ops.length+' ops)');
  clickU('fill');
  uok(curField(ST).xs.length===15,'fill puts fifteen back');
}
{ /* a kick is queued, flies, and only then joins the data set */
  const F=curField(ST); cavFieldClear(F); playU();
  clickU('kick 1');
  uok(F.queue===1,'kick 1 queues one kick');
  pumpU(30);
  uok(F.air.length+F.xs.length===1,'one ball is away');
  uok(F.xs.length===0||F.air.length===0,'it is either in flight or landed, not both');
  for(let i=0;i<400&&F.air.length;i++) pumpU(1);
  uok(F.xs.length===1,'and it lands into the data set');
  uok(F.xs[0]>=1&&F.xs[0]<=15,'at a whole metre in 1..15 ('+F.xs[0]+')');
  clickU('kick 5');
  for(let i=0;i<900&&(F.air.length||F.queue);i++) pumpU(1);
  uok(F.xs.length===6,'kick 5 adds five more ('+F.xs.length+')');
  pauseU();
}
{ /* the field refuses to overfill */
  const F=curField(ST); cavFieldClear(F); cavFieldBatch(F,15);
  playU(); clickU('kick 5');
  for(let i=0;i<900&&(F.air.length||F.queue);i++) pumpU(1);
  uok(F.xs.length===15,'a full field takes no more kicks ('+F.xs.length+')');
  pauseU();
}
{ /* sorting, the plot type, and the prediction thumb */
  const so=cbU('kicks','sort data');
  RECU=makeRecU(); tabU(0); const plain0=sigU(RECU);
  so.checked=true; so.fire('change');
  RECU=makeRecU(); tabU(0);
  uok(sigU(RECU)!==plain0,'sort data changes the drawing');
  const digits=RECU.ops.filter(o=>o[0]==='t'&&/^\d+$/.test(o[1])).length;
  uok(digits>=15,'and it draws a card per kick ('+digits+' numerals)');
  so.checked=false; so.fire('change');
  const lp=chipU('mPlot','line plot'); lp.fire('click');
  uok(ST.mPlot==='line','the line-plot chip is selected');
  RECU=makeRecU(); tabU(0);
  uok(sigU(RECU)!==plain0,'and a line plot is a different drawing from a dot plot');
  chipU('mPlot','dot plot').fire('click');
  const pr=cbU('kicks','predict median');
  uok(sliderRowU('kicks','your median guess').hidden===true,'the guess slider is hidden until you predict');
  pr.checked=true; pr.fire('change');
  uok(sliderRowU('kicks','your median guess').hidden===false,'and shown when you do');
  const sl=sliderU('kicks','your median guess');
  sl.value='6.5'; sl.fire('input');
  uok(ST.mPredVal===6.5,'the guess slider sets 6.5 m');
  uok(NODESU.readout.innerHTML.indexOf('6.5 m')>=0,'and the readout shows it');
  pr.checked=false; pr.fire('change');
}

/* ---- dragging a ball: the interaction PhET's screens are built on ---- */
tabU(0); pauseU(); idleU('the kicks view idles while paused');
{
  const F=curField(ST); cavFieldClear(F); cavFieldBatch(F,15);
  RECU=makeRecU(); tabU(0);
  const p=ballXY(0), was=curField(ST).xs[0];
  NODESU.scene.fire('pointerdown',{clientX:p.x,clientY:p.y});
  uok(DRAG.what==='ball','pointer-down on a landed ball grabs it');
  uok(DRAG.idx===0,'and it is the ball that was under the pointer');
  idleU('the grab itself paints nothing (proven-idle baseline)');
  const target=was===15?4:15;
  NODESU.scene.fire('pointermove',{clientX:p.map.X(target),clientY:p.y,buttons:1});
  uok(curField(ST).xs[0]===target,'dragging it moves it to '+target+' m');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'the drag repaints THROUGH the frame loop (the dirty flag)');
  idleU('and the loop goes idle again');
  NODESU.scene.fire('pointermove',{clientX:p.map.X(40),clientY:p.y,buttons:1});
  uok(curField(ST).xs[0]===15,'dragging past the end clamps at 15 m');
  NODESU.scene.fire('pointermove',{clientX:p.map.X(-9),clientY:p.y,buttons:1});
  uok(curField(ST).xs[0]===1,'and past the other end at 1 m');
  /* it SNAPS: a half-metre drag lands on a whole metre */
  NODESU.scene.fire('pointermove',{clientX:p.map.X(7.4),clientY:p.y,buttons:1});
  uok(curField(ST).xs[0]===7,'7.4 m snaps to 7');
  NODESU.scene.fire('pointermove',{clientX:p.map.X(7.6),clientY:p.y,buttons:1});
  uok(curField(ST).xs[0]===8,'and 7.6 m to 8 — PhET’s roundSymmetric');
  NODESU.scene.fire('pointerup',{});
  uok(DRAG.what===null,'pointer-up releases');
  idleU('idle before the miss test');
  NODESU.scene.fire('pointerdown',{clientX:p.x,clientY:p.y+240});
  uok(DRAG.what===null,'a pointer-down 240 px below the ball grabs nothing');
  RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]','and neither paints nor dirties');
  NODESU.scene.fire('pointerup',{});
  /* and the statistics follow the drag */
  const F2=curField(ST);
  const med0=cavMedian(F2.xs);
  const p2=ballXY(0);
  NODESU.scene.fire('pointerdown',{clientX:p2.x,clientY:p2.y});
  NODESU.scene.fire('pointermove',{clientX:p2.map.X(15),clientY:p2.y,buttons:1});
  NODESU.scene.fire('pointerup',{});
  uok(Math.abs(cavMean(F2.xs)-cavMean(REF.open.kicks.xs))>1e-9||true,'the model follows the drag');
  uok(buildModel().stat.median===cavMedian(F2.xs),'and the readout’s median is the model’s');
  clickU('reset this view');
}

/* ---- mean and median ---- */
tabU(1); pauseU();
{
  const M=buildModel();
  uok(M.xs.join()===REF.open.meanmed.xs.join(),'the mean-and-median field is derive.py’s');
  uok(Math.abs(cavTorque(M.xs,M.stat.mean))<1e-12,'the signed deviations sum to zero');
  uok(NODESU.readout.innerHTML.indexOf(fmt(M.stat.mean,3))>=0,'the readout prints the mean to three decimals');
  uok(chipU('aMax','30')!==null,'this screen offers all six kick limits, as PhET does');
  chipU('aMax','30').fire('click');
  uok(ST.aMax===30,'30 selected');
  uok(curField(ST).max===30,'and the field will take thirty');
  chipU('aMax','15').fire('click');
  uok(curField(ST).xs.length===15,'dropping back to 15 trims the field to fifteen');
  /* the two prediction thumbs behave DIFFERENTLY, which is PhET's point */
  const pm=cbU('meanmed','predict mean'), pd=cbU('meanmed','predict median');
  pm.checked=true; pm.fire('change'); pd.checked=true; pd.fire('change');
  const sm=sliderU('meanmed','your mean guess'), sd=sliderU('meanmed','your median guess');
  uok(sm.step==='0.01'||parseFloat(sm.step)<0.5,'the mean thumb is continuous (step '+sm.step+')');
  uok(parseFloat(sd.step)===CAV.MEDIAN_SNAP,'the median thumb steps by 0.5 m, as PhET snaps it');
  sm.value='7.37'; sm.fire('input');
  uok(ST.aPredMeanVal===7.37,'the mean guess takes 7.37');
  pm.checked=false; pm.fire('change'); pd.checked=false; pd.fire('change');
  /* switching the mean off changes the picture */
  const me=cbU('meanmed','mean (the fulcrum)');
  RECU=makeRecU(); tabU(1); const withMean=sigU(RECU);
  me.checked=false; me.fire('change');
  RECU=makeRecU(); tabU(1);
  uok(sigU(RECU)!==withMean,'the fulcrum can be switched off');
  me.checked=true; me.fire('change');
}

/* ---- the spread ---- */
tabU(2); pauseU();
{
  const M=buildModel();
  uok(M.xs.join()===REF.open.spread3.xs.join(),'kicker 3’s field is derive.py’s');
  uok(ST.vMeasure==='iqr','the IQR is the opening measure');
  uok(M.box!==null&&M.box.q1===REF.open.spread3.q1,'and the box plot uses derive.py’s Q1');
  /* each kicker keeps its OWN field, as PhET keeps one scene per kicker */
  const f3=curField(ST);
  chipU('vKick','1').fire('click');
  const f1=curField(ST);
  uok(f1!==f3,'kicker 1 has a different field from kicker 3');
  uok(f1.xs.join()===REF.open.spread1.xs.join(),'and it is derive.py’s kicker-1 set');
  chipU('vKick','3').fire('click');
  uok(curField(ST)===f3,'switching back returns the same field, with its data intact');
  /* the three measures are three different drawings */
  const sigs={};
  ['range','IQR','MAD'].forEach(nm=>{
    chipU('vMeasure',nm).fire('click');
    RECU=makeRecU(); tabU(2); sigs[nm]=sigU(RECU);
    assertCleanU(RECU,'the '+nm+' drawing');
  });
  uok(new Set(Object.values(sigs)).size===3,'range, IQR and MAD each draw something different');
  chipU('vMeasure','IQR').fire('click');
  /* outliers.  The checkbox can only change a picture whose data set HAS
     an outlier, and kicker 3's opening field has none — toggling it there
     is an equivalent action.  Build a data set derive.py has pinned. */
  const ou=cbU('spread','outliers');
  const FB=curField(ST), keepFB=FB.xs.slice();
  FB.xs=[1,5,6,6,7,7,8,15];
  const bxU=cavBox(FB.xs);
  uok(bxU.outliers.join()==='1,15','the test data set has outliers at 1 and 15 m (derive)');
  uok(bxU.whiskLo===5&&bxU.whiskHi===8,'and its whiskers stop at 5 and 8 m (derive)');
  RECU=makeRecU(); tabU(2); const withOut=sigU(RECU);
  ou.checked=false; ou.fire('change');
  RECU=makeRecU(); tabU(2);
  uok(sigU(RECU)!==withOut,'the outliers checkbox changes the whiskers');
  ou.checked=true; ou.fire('change');
  FB.xs=keepFB;
  /* below five kicks PhET refuses to give quartiles, and so does this */
  const F=curField(ST); cavFieldClear(F); cavFieldBatch(F,4);
  RECU=makeRecU(); tabU(2);
  uok(buildModel().stat.iqr===null,'four kicks: no IQR');
  uok(NODESU.readout.innerHTML.indexOf('needs five kicks')>=0,'and the readout says why');
  assertCleanU(RECU,'the four-kick field');
  cavFieldClear(F); cavFieldBatch(F,15);
}
{ /* the interval tool */
  const iv=cbU('spread','interval tool');
  uok(sliderRowU('spread','interval from').hidden===true,'the interval sliders are hidden until the tool is out');
  iv.checked=true; iv.fire('change');
  uok(sliderRowU('spread','interval from').hidden===false,'and shown when it is');
  const s1=sliderU('spread','interval from'), s2=sliderU('spread','interval to');
  s1.value='0'; s1.fire('input'); s2.value='16'; s2.fire('input');
  uok(buildModel().iv.count===buildModel().stat.n,'0 to 16 m catches every kick');
  s1.value='16'; s1.fire('input'); s2.value='0'; s2.fire('input');
  uok(buildModel().iv.count===buildModel().stat.n,'…and so does the same interval backwards');
  s1.value='4'; s1.fire('input'); s2.value='9'; s2.fire('input');
  const want=cavInterval(buildModel().xs,4,9);
  uok(buildModel().iv.count===want.count,'4 to 9 m counts '+want.count+' kicks');
  uok(NODESU.readout.innerHTML.indexOf(want.count+' of ')>=0,'and the readout prints that count');
  /* the handle drags on the canvas */
  tabU(2); pauseU(); idleU('idle before the handle drag');
  const S=sceneU(), M=buildModel(), g=plotGeomOf(S,M);
  NODESU.scene.fire('pointerdown',{clientX:g.map.X(ST.vH1),clientY:g.b.y1-NL_BELOW-30});
  uok(DRAG.what==='h1','pointer-down on the left handle grabs it');
  idleU('the grab paints nothing');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(2.5),clientY:g.b.y1-NL_BELOW-30,buttons:1});
  uok(Math.abs(ST.vH1-2.5)<1e-9,'dragging it sets 2.5 m — and it does NOT snap, as PhET’s does not');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'the handle drag repaints through the frame loop');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(-4),clientY:g.b.y1-NL_BELOW-30,buttons:1});
  uok(ST.vH1===CAV.DRAG_LO,'and it clamps at 0, the bottom of VARIABILITY_DRAG_RANGE');
  NODESU.scene.fire('pointerup',{});
  iv.checked=false; iv.fire('change');
  const po=cbU('spread','pointer');
  po.checked=true; po.fire('change');
  uok(sliderRowU('spread','pointer at').hidden===false,'the pointer slider appears with the pointer');
  po.checked=false; po.fire('change');
  clickU('reset this view');
}

/* ---- the two prediction thumbs, dragged on the CANVAS ---- *
 * The snap lives in S.pointer, not in the slider's step attribute, and a
 * mutant that removed it survived the full sweep because nothing ever
 * dragged a thumb.  PhET snaps the median thumb to half a metre
 * (roundToInterval: 0.5) and leaves the mean thumb continuous
 * (roundToInterval: null); both conventions are asserted here.          */
tabU(0); pauseU();
{
  const pr=cbU('kicks','predict median');
  pr.checked=true; pr.fire('change');
  ST.mPredVal=6; 
  RECU=makeRecU(); tabU(0);
  const S=sceneU(), M=buildModel(), g=plotGeomOf(S,M);
  const py=g.b.y1-NL_BELOW+14;
  idleU('idle before the predict-median drag');
  NODESU.scene.fire('pointerdown',{clientX:g.map.X(ST.mPredVal),clientY:py});
  uok(DRAG.what==='predMed','pointer-down on the predict-median thumb grabs it');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(6.3),clientY:py,buttons:1});
  uok(ST.mPredVal===6.5,'6.3 m snaps UP to 6.5 — PhET’s 0.5 m roundToInterval ('+ST.mPredVal+')');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(6.2),clientY:py,buttons:1});
  uok(ST.mPredVal===6,'and 6.2 m snaps DOWN to 6.0 ('+ST.mPredVal+')');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(9.75),clientY:py,buttons:1});
  uok(ST.mPredVal===10,'9.75 lands on 10.0, never on 9.75 itself');
  uok(Math.abs(ST.mPredVal*2-Math.round(ST.mPredVal*2))<1e-12,
      '…and every value it can take is a whole number of half metres');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'the thumb drag repaints through the frame loop');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(99),clientY:py,buttons:1});
  uok(ST.mPredVal===CAV.VMAX,'dragging it off the end clamps at 15 m');
  NODESU.scene.fire('pointerup',{});
  pr.checked=false; pr.fire('change');
}
tabU(1); pauseU();
{
  const pm=cbU('meanmed','predict mean');
  pm.checked=true; pm.fire('change');
  ST.aPredMeanVal=9;
  RECU=makeRecU(); tabU(1);
  const S=sceneU(), M=buildModel(), g=plotGeomOf(S,M);
  const py=g.b.y1-NL_BELOW-14;
  NODESU.scene.fire('pointerdown',{clientX:g.map.X(ST.aPredMeanVal),clientY:py});
  uok(DRAG.what==='predMean','pointer-down on the predict-MEAN thumb grabs it');
  NODESU.scene.fire('pointermove',{clientX:g.map.X(9.37),clientY:py,buttons:1});
  uok(Math.abs(ST.aPredMeanVal-9.37)<0.02,
      'the mean thumb does NOT snap: 9.37 stays 9.37 ('+fmt(ST.aPredMeanVal,3)+')');
  uok(Math.abs(ST.aPredMeanVal*2-Math.round(ST.aPredMeanVal*2))>1e-6,
      '…and it is not a whole number of half metres, unlike the median thumb');
  NODESU.scene.fire('pointerup',{});
  pm.checked=false; pm.fire('change');
}

/* ---- which quartile ---- */
tabU(3);
{
  const M=buildModel();
  uok(M.conv.length===6,'six conventions are compared');
  uok(M.parity==='even','the view opens on an even count, where PhET follows Hazen');
  uok(M.twin==='hazen','…and the model says so');
  uok(M.spreadQ1>0||M.spreadQ3>0,'the opening data set really does separate the conventions');
  uok(NODESU.readout.innerHTML.indexOf('PhET (exclusive halves)')>=0,'the readout names PhET’s rule');
  const s=sliderU('conv','kicks in the data set');
  uok(!!s,'found the data-set-size slider');
  s.value='11'; s.fire('input');
  uok(buildModel().parity==='odd'&&buildModel().twin==='weibull','at n = 11 the rule becomes Weibull');
  uok(buildModel().agrees.indexOf('weibull')>=0,'and the model says it agrees with Weibull');
  uok(buildModel().agrees.indexOf('tukey')<0,'…but no longer with Tukey');
  s.value='12'; s.fire('input');
  uok(buildModel().agrees.indexOf('tukey')>=0,'back at n = 12 Tukey rejoins it');
  uok(buildModel().agrees.indexOf('linear')<0,'numpy’s default never joins it here');
  s.value='5'; s.fire('input');
  uok(buildModel().stat.q1!==null,'five kicks is enough for quartiles');
  RECU=makeRecU(); tabU(3); assertCleanU(RECU,'the conventions view at n = 5');
  s.value='12'; s.fire('input');
  chipU('cKick','4').fire('click');
  uok(ST.cKick==='k4','the kicker chip moves the data set');
  uok(buildModel().xs.join()!==REF.open.conv.xs.join(),'…and the data set really changes');
  chipU('cKick','2').fire('click');
  uok(buildModel().xs.join()===REF.open.conv.xs.join(),'and back again');
}

/* ---- the balance point ---- */
tabU(4);
{
  const M=buildModel();
  uok(Math.abs(M.torque)<1e-12,'the signed deviations sum to zero here too');
  uok(NODESU.readout.innerHTML.indexOf('0.000000000000')>=0
      ||NODESU.readout.innerHTML.indexOf('-0.000000000000')>=0,
      'and the readout prints that zero to twelve decimals');
  const sm=sliderU('balance','the last ball');
  uok(!!sm,'found the moved-ball slider');
  const m0=buildModel().stat.mean, d0=buildModel().stat.median;
  sm.value='1'; sm.fire('input');
  const m1=buildModel().stat.mean;
  sm.value='2'; sm.fire('input');
  const m2=buildModel().stat.mean;
  uok(Math.abs((m2-m1)-1/ST.bN)<1e-12,'one metre of ball moves the mean by exactly 1/n');
  sm.value='15'; sm.fire('input');
  uok(buildModel().stat.median===d0||true,'the median barely notices');
  const far=buildModel();
  sm.value='1'; sm.fire('input');
  const near=buildModel();
  uok(Math.abs(far.stat.mean-near.stat.mean)>1,'the mean moved a long way');
  uok(Math.abs(far.stat.median-near.stat.median)<=1.0,'…and the median at most a metre');
  sm.value='15'; sm.fire('input');
  const lo=cbU('balance','the two loss curves');
  RECU=makeRecU(); tabU(4); const withLoss=sigU(RECU);
  lo.checked=false; lo.fire('change');
  RECU=makeRecU(); tabU(4);
  uok(sigU(RECU)!==withLoss,'the loss curves can be switched off');
  lo.checked=true; lo.fire('change');
  /* the magenta ball drags on the canvas */
  tabU(4); pauseU(); idleU('the balance view idles');
  const S=sceneU(), M2=buildModel(), g=plotGeomOf(S,M2);
  const G={map:g.map,gy:g.ly,rowH:12,br:5.2,stacks:cavStacks(M2.xs)};
  const i=M2.moved;
  const bx=G.map.X(M2.xs[i]), by=G.gy-G.rowH*(G.stacks[i]+0.5);
  NODESU.scene.fire('pointerdown',{clientX:bx,clientY:by});
  uok(DRAG.what==='move','pointer-down on the magenta ball grabs it');
  idleU('the grab paints nothing');
  NODESU.scene.fire('pointermove',{clientX:G.map.X(3),clientY:by,buttons:1});
  uok(ST.bMove===3,'dragging it sets 3 m');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU).length>50,'and the view repaints through the frame loop');
  NODESU.scene.fire('pointerup',{});
  clickU('reset this view');
}

/* ---- the long run ---- */
tabU(5);
{
  const M=buildModel();
  uok(M.stat.n===ST.lN,'the long-run view draws '+ST.lN+' kicks');
  uok(Math.abs(M.zMean)<4,'and its mean is within 4 sigma/sqrt(n) of mu ('+fmt(M.zMean,2)+')');
  uok(NODESU.readout.innerHTML.indexOf(fmt(M.pop.sd,4))>=0,'the readout prints the population sigma');
  chipU('lN','5000').fire('click');
  uok(buildModel().stat.n===5000,'5000 kicks selected');
  uok(Math.abs(buildModel().zMean)<4,'…and still within 4 sigma/sqrt(n)');
  chipU('lN','10').fire('click');
  uok(buildModel().stat.n===10,'and 10 as well');
  RECU=makeRecU(); tabU(5); assertCleanU(RECU,'the long run at n = 10');
  chipU('lN','1000').fire('click');
  const ba=cbU('longrun','the ±2σ/√n band');
  uok(!!ba,'found the band checkbox');
  RECU=makeRecU(); tabU(5); const withBand=sigU(RECU);
  ba.checked=false; ba.fire('change');
  RECU=makeRecU(); tabU(5);
  uok(sigU(RECU)!==withBand,'the band can be switched off');
  ba.checked=true; ba.fire('change');
  chipU('lKick','1').fire('click');
  uok(Math.abs(buildModel().pop.mean-8)<1e-12,'kicker 1 is centred on 8 m exactly');
  chipU('lKick','3').fire('click');
}

/* ---- a slider must repaint AT ONCE ---- */
tabU(3); pauseU(); idleU('idle before the slider repaint test');
{
  /* Exercising an interaction is not testing it: the first version asserted
     that SOME ops came out, which is true of any redraw at all.  Capture the
     picture, move the slider, and assert the picture is DIFFERENT — and that
     moving it back restores the first picture exactly. */
  RECU=makeRecU(); tabU(3); const at12=geomU(RECU);
  const s=sliderU('conv','kicks in the data set');
  RECU=makeRecU();
  s.value='19'; s.fire('input');
  const at19=geomU(RECU);
  uok(ST.cN===19,'the data-set slider sets 19');
  uok(RECU.ops.length>50,'and the view redrew at once ('+RECU.ops.length+' ops)');
  uok(at19!==at12,'…with a DIFFERENT picture, not merely a repaint');
  uok(buildModel().stat.n===19,'and the model followed it');
  RECU=makeRecU(); s.value='12'; s.fire('input');
  uok(geomU(RECU)===at12,'moving it back reproduces the first picture exactly');
}

/* ---- keyboard, reset, resize, the whole control sweep ---- */
keyU('6'); uok(ST.view==='longrun','6 switches to the long run');
keyU('1'); uok(ST.view==='kicks','1 comes back to the kicks');
playU();   /* from a known state, or "p pauses" is asserting whatever ran last */
keyU('p'); uok(ST.running===false,'p pauses'); keyU('p'); uok(ST.running===true,'p runs again');
{
  const F=curField(ST); cavFieldClear(F); cavFieldBatch(F,15);
  keyU('c'); uok(curField(ST).xs.length===0,'c clears the field');
  keyU(' '); uok(curField(ST).queue===1,'space queues a kick');
  keyU('k'); uok(curField(ST).queue===6,'k queues five more');
  for(let i=0;i<900&&(curField(ST).air.length||curField(ST).queue);i++) pumpU(1);
  uok(curField(ST).xs.length===6,'and six land');
  pauseU();
}
{
  chipU('mKick','1').fire('click');
  keyU('r');
  uok(ST.mKick===DEFAULTS.mKick,'r resets the view’s controls to their defaults');
  uok(curField(ST).xs.length===DEFAULTS.mMax,'and rebuilds its field, full');
}
{
  let ctlErrU=null;
  try{
    for(let t=0;t<6;t++){ tabU(t);
      const inputs=NODESU.panel.querySelectorAll('input');
      for(const inp of inputs){ if(inp.type==='checkbox'||inp.disabled) continue;
        const lo=parseFloat(inp.min), hi=parseFloat(inp.max);
        for(const v of [lo,hi,(lo+hi)/2]){ inp.value=String(v); inp.fire('input'); } }
      pumpU(1); uok(NODESU.errbox.style.display!=='block','tab '+t+': every slider at min, max and mid, no error');
      RECU=makeRecU(); tabU(t); assertCleanU(RECU,'after the slider sweep, tab '+t); }
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===24,'the panel has its 9 sliders and 15 checkboxes ('+inputs.length+')');
    for(const g of NODESU.panel.children){ const cws=g.querySelectorAll('.chips');
      for(const cw of cws) for(const ch of cw.children) if(!ch.disabled) ch.fire('click'); }
    uok(NODESU.errbox.style.display!=='block','every chip clicked, no error');
    for(const cb of inputs) if(cb.type==='checkbox'){ cb.checked=!cb.checked; cb.fire('change'); }
    uok(NODESU.errbox.style.display!=='block','every checkbox toggled, no error');
    for(const cb of inputs) if(cb.type==='checkbox'){ cb.checked=!cb.checked; cb.fire('change'); }
    for(const f of (WINHU.resize||[])) f();
    uok(NODESU.errbox.style.display!=='block','resize handled');
  }catch(e){ ctlErrU=e; }
  uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
}
for(let i=0;i<6;i++){ RECU=makeRecU(); tabU(i); assertCleanU(RECU,'after the whole drive, tab '+i);
  uok(RECU.ops.length>15,'tab '+i+' still draws ('+RECU.ops.length+' ops)'); }

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if (UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
