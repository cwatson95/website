/* ======= UI drive test for geometric-optics.html ========================= *
 * DOM-stub pattern; the plumbing below (recorder, element stub, pump, the
 * label/chip finders) is build/density/ui_drive_density.js verbatim, which is
 * tools/ui_drive.js with the Known-bad fixes folded in: innerHTML sets
 * textContent, chip rows are addressed by GROUP and index rather than by a
 * substring, and every repaint test starts from a PROVEN-IDLE baseline.
 * The three sim-specific thresholds live in the body: the panel has 8 groups,
 * 21 inputs (14 sliders, 7 checkboxes), and the chip rows have arities
 * 2 (lens surface), 2 (focal-length control), 3 (mirror surface), 5 (object)
 * and 4 (ray mode).  This sim has NO animation and NO camera, so the drag
 * test drags the OBJECT and asserts both that the state moved and that the
 * picture did. */
ObjC.import('Foundation');

let UPASS=0, UFAIL=0;
const uok=(c,n)=>{ if(c) UPASS++; else { UFAIL++; console.log('UI FAIL — '+n); } };

function makeRecU(){
  const ops=[]; const st={font:'10px x',textAlign:'left',textBaseline:'alphabetic'};
  const P=()=>{};
  const c={ops,
    save:P,restore:P,setTransform:P,translate:P,rotate:P,scale:P,setLineDash:P,
    beginPath(){ c._p=[]; },moveTo(x,y){ c._p&&c._p.push([x,y]); },
    lineTo(x,y){ c._p&&c._p.push([x,y]); },closePath:P,
    rect(x,y,w,h){ c._p&&c._p.push([x,y],[x+w,y+h]); },
    arc(x,y,r){ c._p&&c._p.push([x,y,r]); },
    fill(){ if(c._p&&c._p.length) ops.push(['f'].concat(c._p.flat())); },
    stroke(){ if(c._p&&c._p.length) ops.push(['s'].concat(c._p.flat())); },
    clip:P, fillRect(x,y,w,h){ ops.push(['r',x,y,w,h]); },
    strokeRect(x,y,w,h){ ops.push(['R',x,y,w,h]); }, clearRect:P,
    fillText(t,x,y){ ops.push(['t',String(t),Math.round(x),Math.round(y)]); }, strokeText:P,
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||''); return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
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
    classList:{_on:{},add(c){ this._on[c]=1; },remove(c){ delete this._on[c]; },
               toggle(c){ this._on[c]?delete this._on[c]:this._on[c]=1; },contains(c){ return !!this._on[c]; }},
    getBoundingClientRect(){ return {left:0,top:0,width:1180,height:740}; },
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
function findLabelledU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.tagName==='LABEL'&&(ch.textContent||'')===needle) for(const c2 of ch.children||[]) if(c2.tagName==='INPUT') hit=c2;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* the WHOLE label (Known-bad: substring lookups hit the wrong row) */
function sliderU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch.children[1];
    walk(ch); } };
  walk(NODESU.panel); return hit; }
function valOfU(label){ const r=rowU(label); return r?(r.children[2].textContent||''):null; }
/* the panel's own textContent is frozen at appendChild time, so a .tag whose
   innerHTML is rewritten by syncPanel has to be read off the element itself */
function tagTextU(gi){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='tag') hit=ch; walk(ch); } };
  walk(NODESU.panel.children[gi]); return hit?(hit.textContent||''):null; }
function rowU(label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel); return hit; }
/* group-scoped versions: the lens group and the mirror group BOTH carry a
   'focal length', a 'radius R' and a 'diameter D' slider, so a whole-panel
   walk returns the mirror's every time (Known-bad: a finder that matches on a
   label finds the wrong control).  Everything below addresses them by group. */
function rowG(gi,label){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){
    if(ch.className==='sliderrow'&&ch.children[0]&&(ch.children[0].textContent||'')===label) hit=ch;
    walk(ch); } };
  walk(NODESU.panel.children[gi]); return hit; }
function sliderG(gi,label){ const r=rowG(gi,label); return r?r.children[1]:null; }
function valG(gi,label){ const r=rowG(gi,label); return r?(r.children[2].textContent||''):null; }
/* Chip rows are addressed by GROUP and by their index inside it, never by the
   label alone and not even by label + arity: this sim's lens group carries TWO
   2-chip rows (the surface and the focal-length control) and a label-only
   search takes the last one (Known-bad: a finder that matches on a word finds
   the wrong control).  The group indices are declared in the body. */
function chipsInU(gi,rowIdx){
  const out=[];
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='chips') out.push(ch); walk(ch); } };
  walk(NODESU.panel.children[gi]);
  return out[rowIdx||0]||null;
}
function chipG(gi,rowIdx,label,arity){
  const row=chipsInU(gi,rowIdx);
  if(!row||(arity!==undefined&&row.children.length!==arity)) return null;
  for(const c of row.children) if(c.textContent===label) return c;
  return null;
}
function buttonU(needle){ let hit=null;
  const walk=n=>{ for(const ch of n.children||[]){ if(ch.tagName==='BUTTON'&&(ch.textContent||'')===needle) hit=ch; walk(ch); } };
  walk(NODESU.panel); return hit; }
function clickButtonU(needle){ const b=buttonU(needle); if(b) b.fire('click'); return !!b; }
function idleU(label){ pumpU(3); RECU=makeRecU(); pumpU(3); uok(geomU(RECU)==='[]',label); }
function tabU(i){ NODESU.tabs.children[i].fire('click'); }

/* ---- boot ---- */
const GLENS=0, GMIR=1, GOBJ=2, GRAYS=3, GDRAW=4, GREAL=5, GINFO=6, GPHYS=7;
let bootErrU=null;
try{ boot(); }catch(e){ bootErrU=e; }
uok(!bootErrU,'boot() completes without throwing'+(bootErrU?': '+(bootErrU.stack||bootErrU):''));
uok(NODESU.errbox.style.display!=='block','no error captured after boot');
uok(NODESU.tabs.children.length===6,'six view tabs were built ('+NODESU.tabs.children.length+')');
uok(NODESU.tabs.children.map(b=>b.textContent).join('|')
    ==='the lens bench|the mirror bench|the conjugate curve|the lens maker|the guides|the real lens',
    'the tabs are lower-case noun phrases');
uok(NODESU.panel.children.length===8,'the control panel has its 8 groups ('+NODESU.panel.children.length+')');
uok((NODESU.readout.innerHTML||'').length>300,'the readout rendered');
uok((NODESU.eqbar.innerHTML||'').indexOf('NaN')<0,'the equation bar has no NaN');
uok((NODESU.readout.innerHTML||'').indexOf('151.11')>=0,
    'the readout prints d_i = 151.11 cm off the model (derive)');
uok((NODESU.readout.innerHTML||'').indexOf('80.00')>=0,'and the 80 cm focal length PhET starts with');
uok(NODESU.panel.textContent.indexOf('Remake of PhET Interactive Simulations')>=0,
    'the panel carries the PhET credit line');
uok(ST.lensSurface==='convex'&&ST.fControl==='indirect'&&ST.lensR===80&&ST.lensN===1.5&&ST.lensD===80,
    'PhET\'s start: a convex lens, indirect focal-length model, R = 80, n = 1.5, D = 80');
uok(ST.objX===-170&&ST.objY===27&&ST.rays==='marginal','and its framed object at (-170, 27), marginal rays');

/* ---- every tab draws, differently, cleanly, and then settles ----
   The floors are DERIVED from what each view emits, not copied: the bench
   batches a whole lens or ray into one fill/stroke, so an op count alone
   punishes it for batching while letting a nearly-blank view through.  Floor
   what the operations CARRY as well (pascals_triangle Known-bad).  Measured
   at 1180 x 740: ops 43/41/96/70/58/93, path numbers 332/324/2072/906/416/656. */
const FLOORSU=[30,28,60,45,40,60];
const PATHFLOORU=[230,220,1400,600,280,450];
const pathNumsU=c=>c.ops.reduce((a,o)=>a+(o[0]==='t'?0:o.length-1),0);
const sigsU={};
for(let i=0;i<6;i++){
  RECU=makeRecU(); tabU(i);
  uok(RECU.ops.length>=FLOORSU[i],'tab '+i+' emits at least '+FLOORSU[i]+' ops ('+RECU.ops.length+')');
  uok(pathNumsU(RECU)>=PATHFLOORU[i],'tab '+i+' carries at least '+PATHFLOORU[i]
      +' path numbers ('+pathNumsU(RECU)+')');
  uok(NODESU.errbox.style.display!=='block','tab '+i+' drew without error');
  assertCleanU(RECU,'tab '+i);
  sigsU['t'+i]=sigU(RECU);
}
uok(new Set(Object.values(sigsU)).size===6,'every tab draws a different picture');
for(let i=0;i<6;i++){ tabU(i); idleU('tab '+i+' paints nothing once it has settled'); }

/* ---- the lens chips ---- */
tabU(0);
{
  const cx=chipG(GLENS,0,'convex lens',2), cc=chipG(GLENS,0,'concave lens',2);
  uok(!!cx&&!!cc,'found the two lens-surface chips in a row of exactly 2');
  RECU=makeRecU(); cc.fire('click');
  uok(RECU.ops.length>30,'clicking "concave lens" repaints ('+RECU.ops.length+' ops)');
  uok(ST.lensSurface==='concave','and the state followed');
  uok(lensFocal(ST)<0,'a concave lens has a NEGATIVE focal length');
  uok((NODESU.readout.innerHTML||'').indexOf('virtual')>=0,'its image is virtual, and the readout says so');
  uok((NODESU.readout.innerHTML||'').indexOf('54.40')>=0,
      'with d_i = -54.40 cm at PhET\'s default object (derive)');
  cx.fire('click');
  uok(ST.lensSurface==='convex'&&lensFocal(ST)>0,'and back to convex, f > 0');
}
/* PhET's two focal-length models, and the hand-off between them */
{
  const dir=chipG(GLENS,1,'set f directly',2), ind=chipG(GLENS,1,'set R and n',2);
  uok(!!dir&&!!ind,'found the two focal-length-control chips');
  uok(!!rowG(GLENS,'radius R')&&!rowG(GLENS,'radius R').hidden,'the indirect model shows the radius slider');
  uok(rowG(GLENS,'focal length').hidden,'and hides the focal-length slider');
  dir.fire('click');
  uok(ST.fControl==='direct','the direct model is selected');
  uok(!rowG(GLENS,'focal length').hidden&&rowG(GLENS,'radius R').hidden,'and the two sliders swap over');
  uok(Math.abs(ST.lensF-80)<1e-9,'switching carried |f| = 80 cm across from R = 80, n = 1.5');
  uok(Math.abs(lensIndex(ST)-1.5)<1e-12,'the direct model pins n at PhET\'s 1.5');
  uok(Math.abs(Math.abs(lensRadius(ST))-80)<1e-9,'so R = 2f(n-1) = f = 80 cm follows');
  ind.fire('click');
  uok(ST.fControl==='indirect'&&Math.abs(ST.lensR-80)<1e-9,'and back again, R = 80 cm');
  /* the same hand-off from a NON-default radius: at R = 80, n = 1.5 the value
     carried across is 80, which is also lensF's own default, so a hand-off that
     did nothing at all would look identical (Known-bad: test the configuration
     only the primary path can carry) */
  sliderG(GLENS,'radius R').value='120'; sliderG(GLENS,'radius R').fire('input');
  dir.fire('click');
  uok(Math.abs(ST.lensF-120)<1e-9,'R = 120 hands 120 cm to the direct model, not the default 80 ('
      +fmt(ST.lensF,2)+')');
  sliderG(GLENS,'focal length').value='40'; sliderG(GLENS,'focal length').fire('input');
  ind.fire('click');
  uok(Math.abs(ST.lensR-40)<1e-9,'and f = 40 hands 40 cm back to the indirect one ('
      +fmt(ST.lensR,2)+')');
  clickButtonU('reset all');
}
/* the radius slider really moves the focal length, and repaints immediately */
{
  idleU('idle before the radius slider');
  const s=sliderG(GLENS,'radius R');
  uok(!!s,'found the LENS radius slider (the mirror group has one of that name too)');
  const f0=lensFocal(ST);
  RECU=makeRecU(); s.value='120'; s.fire('input');
  uok(RECU.ops.length>30,'moving the radius repaints straight away ('+RECU.ops.length+' ops)');
  uok(Math.abs(lensFocal(ST)-120)<1e-9,'R = 120 at n = 1.5 gives f = 120 cm');
  uok(lensFocal(ST)!==f0,'which is not where it was');
  uok(valG(GLENS,'radius R')==='120 cm','and the slider prints its own value');
  uok(Math.abs(mirrorFocal(ST)-90)<1e-9,'and the MIRROR is untouched, still f = 90 cm');
  s.value='80'; s.fire('input');
}
/* the index slider moves it the other way */
{
  const s=sliderG(GLENS,'index n');
  uok(!!s,'found the index slider');
  s.value='1.8'; s.fire('input');
  uok(Math.abs(lensFocal(ST)-50)<1e-9,'n = 1.8 at R = 80 gives f = 50 cm (derive)');
  s.value='1.2'; s.fire('input');
  uok(Math.abs(lensFocal(ST)-200)<1e-9,'n = 1.2 gives f = 200 cm (derive)');
  s.value='1.5'; s.fire('input');
  uok(Math.abs(lensFocal(ST)-80)<1e-9,'and 1.5 puts it back at 80 cm');
}

/* ---- the object chips and the ray-mode chips ---- */
{
  const row=chipsInU(GOBJ,0);
  uok(!!row&&row.children.length===5,'the object row has PhET\'s five choices');
  uok(row.children.map(c=>c.textContent).join('|')==='pencil|penguin|star|arrow|light',
      'named as PhET names them');
  for(const c of row.children){
    RECU=makeRecU(); c.fire('click');
    uok(RECU.ops.length>28,'object "'+c.textContent+'" draws ('+RECU.ops.length+' ops)');
    assertCleanU(RECU,'object '+c.textContent);
  }
  uok(ST.objKind==='light','the light source is selected last');
  uok(!rowG(GDRAW,'screen at x').hidden,'which reveals the projection-screen slider');
  uok((NODESU.readout.innerHTML||'').indexOf('light spot')>=0,'and the readout gains the light spot');
  chipG(GOBJ,0,'pencil',5).fire('click');
  uok(rowG(GDRAW,'screen at x').hidden,'and the slider hides again for a framed object');
}
{
  const row=chipsInU(GRAYS,0);
  uok(!!row&&row.children.length===4,'the ray row has PhET\'s four modes');
  uok(row.children.map(c=>c.textContent).join('|')==='marginal|principal|many|none',
      'marginal, principal, many, none');
  const counts={};
  for(const c of row.children){
    RECU=makeRecU(); c.fire('click');
    counts[c.textContent]=RECU.ops.length;
    assertCleanU(RECU,'rays '+c.textContent);
  }
  uok(counts['many']>counts['marginal'],'"many" emits more operations than "marginal" ('
      +counts['many']+' vs '+counts['marginal']+')');
  uok(counts['none']<counts['marginal'],'and "none" fewer ('+counts['none']+')');
  chipG(GRAYS,0,'many',4).fire('click');
  uok(ST.rays==='many','many rays selected');
  uok(tagTextU(GRAYS).indexOf('20')>=0,'the tag names PhET\'s ray count, 20 at this distance');
  chipG(GRAYS,0,'marginal',4).fire('click');
}

/* ---- dragging the object: the state moves AND the picture moves ---- */
{
  tabU(0);
  clickButtonU('reset all');
  idleU('idle before the drag test');
  const x0=ST.objX, y0=ST.objY;
  RECU=makeRecU();
  NODESU.scene.fire('pointerdown',{clientX:0,clientY:0});
  pumpU(3);
  uok(geomU(RECU)==='[]','a pointerdown nowhere near the object does nothing at all');
  /* find the object on screen through the same geometry the view uses */
  const M0=buildModel(ST);
  const G0=benchGeo(makeRecU(),1180,740,M0,ST);
  const px=G0.map.X(x0), py=G0.map.Y(y0);
  idleU('still idle after the miss');
  /* Each flag on its own, and BEFORE the release: the pointer-up handler calls
     refresh(), which draws unconditionally, so a test that releases first
     cannot tell the move's dirty flag from the release's repaint.  Both flags
     survived a sweep until this was split. */
  RECU=makeRecU();
  NODESU.scene.fire('pointerdown',{clientX:px,clientY:py});
  pumpU(3);
  uok(RECU.ops.length>10,'a pointerdown ON the object repaints on its own ('+RECU.ops.length+' ops)');
  RECU=makeRecU(); pumpU(3);
  uok(geomU(RECU)==='[]','and the loop goes quiet again straight after it');
  RECU=makeRecU();
  NODESU.scene.fire('pointermove',{clientX:px-60,clientY:py+20,buttons:1});
  pumpU(3);
  const gDrag=geomU(RECU);
  uok(gDrag.length>60,'a pointermove repaints through the frame loop (its own dirty flag)');
  NODESU.scene.fire('pointerup',{});
  pumpU(3);
  uok(ST.objX<x0-5,'and the object really moved left in the model ('+fmt(x0,1)+' -> '+fmt(ST.objX,1)+')');
  uok(ST.objY<y0-1,'and down the screen ('+fmt(y0,1)+' -> '+fmt(ST.objY,1)+')');
  /* the repaint must show a MOVED object, not the same picture again: compare
     two FORCED draws, since an idle frame paints nothing and any repaint would
     differ from it trivially (Known-bad, three times over) */
  const forceU=()=>{ RECU=makeRecU(); tabU(0); return geomU(RECU); };
  clickButtonU('reset all');
  const before=forceU();
  NODESU.scene.fire('pointerdown',{clientX:px,clientY:py});
  NODESU.scene.fire('pointermove',{clientX:px+40,clientY:py,buttons:1});
  NODESU.scene.fire('pointerup',{});
  const after=forceU();
  uok(after!==before&&after.length>60,'a purely horizontal drag moves the drawn geometry');
  clickButtonU('reset all');
  const before2=forceU();
  NODESU.scene.fire('pointerdown',{clientX:px,clientY:py});
  NODESU.scene.fire('pointermove',{clientX:px,clientY:py-40,buttons:1});
  NODESU.scene.fire('pointerup',{});
  const after2=forceU();
  uok(after2!==before2&&after2.length>60,'and a purely vertical one does too');
  /* PhET's two constraints are enforced on the drag, not merely on the slider */
  clickButtonU('reset all');
  NODESU.scene.fire('pointerdown',{clientX:px,clientY:py});
  NODESU.scene.fire('pointermove',{clientX:px+4000,clientY:py-4000,buttons:1});
  NODESU.scene.fire('pointerup',{});
  uok(ST.objX<=-PHET.minObjectDist+1e-9,'a drag cannot push the object nearer than PhET\'s 40 cm ('
      +fmt(ST.objX,2)+')');
  uok(ST.objY<=PHET.maxOffAxis+1e-9,'nor further off-axis than its 100 cm ('+fmt(ST.objY,2)+')');
  clickButtonU('reset all');
  uok(ST.objX===-170&&ST.objY===27,'reset-all puts PhET\'s object back');
}
/* no view reads a wheel: the property, asserted, rather than a no-op method
   (Known-bad: a no-op nothing calls is dead code, not a design decision) */
{
  tabU(0);
  clickButtonU('reset all');
  idleU('idle before the wheel check');
  RECU=makeRecU();
  NODESU.scene.fire('wheel',{deltaY:-500});
  pumpU(3);
  uok(geomU(RECU)==='[]','the canvas has no wheel handler at all and the loop stays idle');
}

/* ---- the mirror bench ---- */
{
  tabU(1);
  const row=chipsInU(GMIR,0);
  uok(!!row&&row.children.length===3,'the mirror row has concave, convex and flat');
  uok(row.children.map(c=>c.textContent).join('|')==='concave|convex|flat','named as PhET names them');
  uok(!NODESU.panel.children[GMIR].hidden,'the mirror group is visible on the mirror bench');
  uok(NODESU.panel.children[GRAYS].hidden===false,'and so are the ray controls');
  uok(Math.abs(mirrorFocal(ST)-90)<1e-9,'a concave mirror of R = 180 has f = 90 cm');
  uok((NODESU.readout.innerHTML||'').indexOf('concave mirror')>=0,'the readout names it');
  const flat=chipG(GMIR,0,'flat',3);
  RECU=makeRecU(); flat.fire('click');
  uok(RECU.ops.length>30,'the flat mirror draws ('+RECU.ops.length+' ops)');
  uok(mirrorFocal(ST)===1e5,'PhET\'s flat mirror is f = 100 000 cm');
  uok(rowG(GMIR,'radius R').hidden,'and its radius control is hidden: a plane has none');
  uok((NODESU.readout.innerHTML||'').indexOf('1.0017')>=0,
      'the readout prints m = 1.0017 at d_o = 170 cm, not 1');
  chipG(GMIR,0,'convex',3).fire('click');
  uok(mirrorFocal(ST)<0,'a convex mirror diverges');
  chipG(GMIR,0,'concave',3).fire('click');
}

/* ---- the checkboxes ---- */
{
  tabU(0);
  clickButtonU('reset all');
  const names=['Focal Points (F)','2F Points','Virtual Image','Labels','Second Point','Guides','ruler'];
  for(const nm of names){
    const cb=findLabelledU(nm);
    uok(!!cb,'found the "'+nm+'" checkbox');
    if(!cb) continue;
    const was=cb.checked;
    RECU=makeRecU(); cb.checked=!was; cb.fire('change');
    uok(RECU.ops.length>25,'toggling "'+nm+'" repaints ('+RECU.ops.length+' ops)');
    assertCleanU(RECU,'"'+nm+'" on');
    cb.checked=was; cb.fire('change');
  }
  /* the ones that must change the picture do */
  const flip=nm=>{ const cb=findLabelledU(nm); const w=cb.checked; cb.checked=!w; cb.fire('change'); return cb; };
  const forceU=()=>{ RECU=makeRecU(); tabU(0); return geomU(RECU); };
  const base=forceU();
  flip('2F Points');
  uok(forceU()!==base,'switching the 2F points on changes the drawing');
  flip('2F Points');
  flip('Guides');
  uok(forceU()!==base,'switching the guides on changes the drawing');
  uok(ST.showGuides===true,'and the state says so');
  flip('Guides');
  flip('Second Point');
  uok(!rowG(GOBJ,'second point').hidden,'the second point reveals its offset slider');
  uok(forceU()!==base,'and a second bundle of rays');
  flip('Second Point');
  uok(forceU()===base,'and turning them all off again restores the first picture');
}

/* ---- the view-dependent panel: a control this view ignores is HIDDEN ---- */
{
  tabU(2);                                   /* the conjugate curve */
  uok(!NODESU.panel.children[GLENS].hidden,'the lens group stays on the conjugate curve');
  uok(NODESU.panel.children[GMIR].hidden,'the mirror group is hidden there');
  uok(NODESU.panel.children[GRAYS].hidden,'and so are the ray controls');
  uok(rowG(GLENS,'diameter D').hidden,'the diameter does nothing to the conjugate curve, so it is hidden');
  uok(rowG(GOBJ,'height y').hidden,'and neither does the object height');
  uok(!rowG(GOBJ,'position x').hidden,'but the object distance is the axis, so it stays');
  tabU(5);                                   /* the real lens */
  uok(!NODESU.panel.children[GREAL].hidden,'the real-lens group appears on the real-lens view');
  uok(NODESU.panel.children[GOBJ].hidden,'and the object group goes: no object is imaged there');
  tabU(0);
  uok(NODESU.panel.children[GREAL].hidden,'the real-lens group goes away again');
}

/* ---- the analysis views answer their own sliders ---- */
{
  tabU(3);                                   /* the lens maker */
  const s=sliderG(GLENS,'index n');
  const before=(RECU=makeRecU(),tabU(3),geomU(RECU));
  RECU=makeRecU(); s.value='1.7'; s.fire('input');
  uok(RECU.ops.length>30,'the lens maker repaints when n moves');
  const after=(RECU=makeRecU(),tabU(3),geomU(RECU));
  uok(after!==before,'and the live point moved');
  s.value='1.5'; s.fire('input');
  /* the impossible lens: R = 40 with D = 120 has no sphere behind it */
  sliderG(GLENS,'radius R').value='40'; sliderG(GLENS,'radius R').fire('input');
  sliderG(GLENS,'diameter D').value='120'; sliderG(GLENS,'diameter D').fire('input');
  RECU=makeRecU(); tabU(3);
  uok(/could not|does not exist|no sphere/.test(textU(RECU)),
      'and when the sphere cannot carry the aperture the canvas says so');
  tabU(5);
  RECU=makeRecU(); tabU(5);
  uok(/cannot carry|no lens to trace|No lens/.test(textU(RECU)),
      'the real lens refuses to trace a lens that cannot exist, and says why');
  uok(RECU.ops.length>=3,'drawing a sentence rather than nothing ('+RECU.ops.length+' ops)');
  clickButtonU('reset all');
}
{
  tabU(5);
  const s=sliderG(GREAL,'stopped to');
  uok(!!s,'found the aperture-stop slider');
  const M1=buildModel(ST);
  s.value='0.3'; s.fire('input');
  const M2=buildModel(ST);
  uok(Math.abs(M2.lsaRim)<Math.abs(M1.lsaRim)/4,
      'stopping the lens down collapses the spherical aberration ('+sigf(M1.lsaRim,4)
      +' -> '+sigf(M2.lsaRim,4)+' cm)');
  uok(M2.stop<M1.stop,'because the traced bundle is narrower');
  const e=sliderG(GREAL,'edge thickness');
  e.value='10'; e.fire('input');
  uok(buildModel(ST).t>M2.t,'a thicker edge is a thicker lens');
  clickButtonU('reset all');
}
{
  tabU(4);                                   /* the guides */
  RECU=makeRecU(); tabU(4);
  const txt=textU(RECU);
  uok(/guides cross/.test(txt),'the guides view marks where the two arms cross');
  uok(/the image/.test(txt),'and where the image really is');
  uok(/miss/.test(txt),'and says by how much it misses');
  const M=buildModel(ST);
  uok(Math.abs(M.missPct-4.400838574610697)<1e-6,
      'which is 4.4008 % at PhET\'s defaults (derive)');
  uok(M.slopeMiss<1e-10,'while the slope construction misses by nothing');
}

/* ---- the keyboard, the resize, and a full control sweep ---- */
{
  for(const k of ['1','2','3','4','5','6'])
    { keyU(k); uok(NODESU.errbox.style.display!=='block','key "'+k+'" switches view without error'); }
  uok(ST.view==='real','key 6 reaches the last view');
  keyU('1');
  uok(ST.view==='bench','and key 1 comes back');
  sliderG(GLENS,'radius R').value='45'; sliderG(GLENS,'radius R').fire('input');
  keyU('r');
  uok(ST.lensR===80,'"r" resets the controls');
  uok(ST.view==='bench','and keeps the view');
  let rsErr=null;
  try{ for(const f of (WINHU.resize||[])) f({}); }catch(e){ rsErr=e; }
  uok(!rsErr,'the resize handler runs'+(rsErr?': '+rsErr:''));
  uok(NODESU.errbox.style.display!=='block','still no error after resize');
}
{
  let ctlErrU=null;
  try{
    const inputs=NODESU.panel.querySelectorAll('input');
    uok(inputs.length===21,'the panel has its 21 inputs ('+inputs.length+')');
    let sliders=0,boxes=0;
    for(const inp of inputs) (inp.type==='checkbox')?boxes++:sliders++;
    uok(sliders===14&&boxes===7,'14 sliders and 7 checkboxes ('+sliders+'/'+boxes+')');
    for(let t=0;t<6;t++){
      tabU(t);
      for(const inp of inputs){
        if(inp.type==='checkbox'){ inp.checked=!inp.checked; inp.fire('change'); }
        else {
          for(const frac of [0,0.5,1]){
            inp.value=String(parseFloat(inp.min)+frac*(parseFloat(inp.max)-parseFloat(inp.min)));
            inp.fire('input');
          }
        }
      }
      RECU=makeRecU(); tabU(t);
      assertCleanU(RECU,'view '+t+' after the full control sweep');
      uok(RECU.ops.length>=3,'view '+t+' still draws after the sweep ('+RECU.ops.length+' ops)');
      uok(NODESU.errbox.style.display!=='block','view '+t+' survived the sweep');
      clickButtonU('reset all');
    }
  }catch(e){ ctlErrU=e; }
  uok(!ctlErrU,'control sweep completes'+(ctlErrU?': '+(ctlErrU.stack||ctlErrU):''));
}
{
  let chipErrU=null;
  try{
    for(let t=0;t<6;t++){
      tabU(t);
      for(const g of NODESU.panel.children){
        const rows=[];
        const walk=n=>{ for(const ch of n.children||[]){ if(ch.className==='chips') rows.push(ch); walk(ch); } };
        walk(g);
        for(const r of rows) for(const chip of r.children){
          RECU=makeRecU(); chip.fire('click');
          assertCleanU(RECU,'view '+t+' with "'+chip.textContent+'"');
          uok(NODESU.errbox.style.display!=='block','view '+t+', chip "'+chip.textContent+'" did not error');
        }
      }
      clickButtonU('reset all');
    }
  }catch(e){ chipErrU=e; }
  uok(!chipErrU,'every chip in every view can be clicked'+(chipErrU?': '+(chipErrU.stack||chipErrU):''));
}

console.log('UI: '+UPASS+' passed, '+UFAIL+' failed');
if(UFAIL>0) throw new Error(UFAIL+' UI failure(s)');
