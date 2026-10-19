
/* ================================================================== *
 *  state, the curve itself, the per-view model, readout, equation bar *
 * ================================================================== */
const TABS=[['deriv','the derivative'],['integ','the integral'],['lab','the lab'],
            ['corner','the corners'],['ftc','the theorem'],['grid','the grid']];
const COL={f:'#b8ec4c', d:'#cd35c4', dd:'#e8843a', I:'#5ac8e0',
           exact:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', warn:'#e8843a', pred:'#e8843a',
           zero:'#39405a', phet:'#8b93a6',
           areaPos:'#5ac8e0', areaNeg:'#e8843a'};
const RO_W=300;
const NOTATIONS=[{id:'lagrange',name:'Lagrange'},{id:'leibniz',name:'Leibniz'}];
const VARIABLES=[{id:'x',name:'x'},{id:'t',name:'t'}];
const DISCONTS=[{id:'noLine',name:'no line'},{id:'dashedLine',name:'dashed line'}];
/* the grid view's refinement ladder, as multiples of PhET's own 1251 cells */
const GRID_MULTS=[0.25,0.5,1,2,4,8];

const DEFAULTS={view:'deriv', mode:'hill', width:W_DEF, height:1.5, placeX:5.0,
                xT:3.2, xA:5.0, xR:5.0,
                tangent:true, area:false, refLine:false, grid:true, values:false,
                notation:'lagrange', variable:'x', discont:'noLine',
                predict:false, showF:true,
                refShape:'triangle', refW:2.0, refX:5.0, refY:1.5, cornerSel:0,
                gridMult:2, phetOp:false};
const ST=Object.assign({},DEFAULTS);

/* the curve lives outside ST, because Object.assign would alias the array and
   a reset would then write through to the defaults (the same trap the fourier
   remake's amplitude arrays hit). */
let CURVE=new Float64Array(NPTS), CFLAG=new Uint8Array(NPTS);
let PRED=new Float64Array(NPTS),  PFLAG=new Uint8Array(NPTS);
let SAVED=new Float64Array(NPTS), SFLAG=new Uint8Array(NPTS);
let UNDO=[];                       /* PhET keeps MAX_UNDO of these */
let CVER=0;                        /* bumped on every change: the memo key */

function activeF(){ return ST.predict?PRED:CURVE; }
function activeC(){ return ST.predict?PFLAG:CFLAG; }
function setActive(f,c){
  if(ST.predict){ PRED=f; PFLAG=c; } else { CURVE=f; CFLAG=c; }
  CVER++;
}
function saveCurve(){
  SAVED=activeF().slice(); SFLAG=activeC().slice();
  UNDO.push([activeF().slice(),activeC().slice()]);
  while(UNDO.length>MAX_UNDO) UNDO.shift();
}
function applyShape(mode,w,x,y){
  const out=manipulate(SAVED,SFLAG,mode,w,x,y);
  setActive(out.f,out.c);
}
function doSmooth(){
  saveCurve();
  const out=smoothCurve(activeF());
  setActive(out.f,new Uint8Array(NPTS));     /* PhET: every point becomes smooth */
}
function doErase(){ saveCurve(); setActive(new Float64Array(NPTS),new Uint8Array(NPTS)); }
function doUndo(){
  if(!UNDO.length) return false;
  const [f,c]=UNDO.pop();
  setActive(f,c);
  return true;
}
/* PhET opens on a flat line and asks you to draw.  A flat line makes every one
   of these six views blank, which this collection treats as a defect rather
   than a preference, so the file opens with a hill and a triangle already laid
   down -- one shape with a derivative everywhere and one with three corners.
   "erase" gives PhET's empty curve exactly. */
const DEF_RECIPE=[['hill',2.0,3.2,1.6],['triangle',2.4,6.8,-1.2]];
function buildDefaultCurve(){
  let f=new Float64Array(NPTS), c=new Uint8Array(NPTS);
  for(const [mode,w,x,y] of DEF_RECIPE){
    const out=manipulate(f,c,mode,w,x,y);
    f=out.f; c=out.c;
  }
  return {f,c};
}
function resetAll(){
  const v=ST.view;
  Object.assign(ST,DEFAULTS);
  ST.view=v;
  const d=buildDefaultCurve();
  CURVE=d.f; CFLAG=d.c;
  PRED=new Float64Array(NPTS); PFLAG=new Uint8Array(NPTS);
  SAVED=CURVE.slice(); SFLAG=CFLAG.slice();
  UNDO=[]; CVER++;
}

const MEMO={};
function memo(name,key,fn){
  const m=MEMO[name];
  if(m&&m.key===key) return m.val;
  const val=fn();
  MEMO[name]={key,val};
  return val;
}

/* ---- the four curves of whichever function is being shown --------- */
function curveSet(f,c){
  const d=derivOf(f), F=integOf(f), d2=deriv2Of(f);
  return {f,c,d,F,d2,corners:cornerList(c,d,24)};
}
/* the truth is always f.  PhET's Predict lets you sketch what you think f is
   while its derivative and integral graphs keep showing the REAL ones -- that
   is the whole exercise -- so the shaped curve and the differentiated curve
   are two different objects whenever predict is on. */
function liveSet(){
  return memo('live',String(CVER),()=>curveSet(CURVE,CFLAG));
}
function shapeSet(){
  if(!ST.predict) return liveSet();
  return memo('shape',String(CVER),()=>curveSet(PRED,PFLAG));
}
function predRms(){
  let s=0;
  for(let i=0;i<NPTS;i++){ const e=PRED[i]-CURVE[i]; s+=e*e; }
  return Math.sqrt(s/NPTS);
}
/* the analysis views work on ONE analytic shape laid on an empty curve, so
   the closed form they compare against is unambiguous */
function refKey(){ return [ST.refShape,ST.refW,ST.refX,ST.refY].join('|'); }
function refSet(){
  return memo('ref',refKey(),()=>{
    const out=manipulate(new Float64Array(NPTS),new Uint8Array(NPTS),
                         ST.refShape,ST.refW,ST.refX,ST.refY);
    const s=curveSet(out.f,out.c);
    s.cf=shapeClosed(ST.refShape,ST.refW,ST.refX,ST.refY);
    s.Gx=cumExact(s.cf,GRID);
    return s;
  });
}
/* the refinement study: the same shape on six grids, coarsest to finest */
function gridStudy(){
  return memo('gridstudy',refKey(),()=>{
    const rows=[];
    for(const m of GRID_MULTS){
      const n=Math.round((NPTS-1)*m)+1;
      rows.push(gridError(ST.refShape,ST.refW,ST.refX,ST.refY,n));
    }
    return rows;
  });
}
/* the fundamental theorem, measured on whatever curve is on screen */
function ftcSet(){
  return memo('ftc',String(CVER),()=>{
    const S=liveSet();
    const back=integCells(S.d);                  /* integrate the derivative */
    const fwd=derivOf(S.F);                      /* differentiate the integral */
    const mid=new Float64Array(NPTS-1);
    for(let i=0;i<NPTS-1;i++) mid[i]=0.5*(S.f[i]+S.f[i+1]);
    let e1=0,e2=0,e3=0;
    const r1=new Float64Array(NPTS), r2=new Float64Array(NPTS-1);
    for(let i=0;i<NPTS;i++){ r1[i]=back[i]-(S.f[i]-S.f[0]); e1=Math.max(e1,Math.abs(r1[i])); }
    for(let i=0;i<NPTS-1;i++){ r2[i]=fwd[i]-mid[i]; e2=Math.max(e2,Math.abs(r2[i])); }
    const pd=phetDeriv(S.F);
    for(let i=1;i<NPTS-1;i++)
      e3=Math.max(e3,Math.abs(pd[i]-0.25*(S.f[i-1]+2*S.f[i]+S.f[i+1])));
    /* what PhET's pair actually costs, on this curve: how far its
       differentiate-the-integral lands from f itself */
    let ePhet=0;
    for(let i=1;i<NPTS-1;i++) ePhet=Math.max(ePhet,Math.abs(pd[i]-S.f[i]));
    return {back,fwd,mid,r1,r2,e1,e2,e3,ePhet,pd};
  });
}

/* ---- the two tools ------------------------------------------------ */
function toolValues(S){
  const tan=tangentAt(S.f,S.d,clamp(ST.xT,XMIN,XMAX));
  const ar=signedAreas(S.f,clamp(ST.xA,XMIN,XMAX));
  const Ia=integAt(S.f,S.F,clamp(ST.xA,XMIN,XMAX));
  return {tan,ar,Ia,areaMismatch:Math.abs(ar.net-Ia)};
}

function rangeOf(a,floor){
  let m=floor===undefined?0.2:floor;
  for(let i=0;i<a.length;i++) if(isFinite(a[i])) m=Math.max(m,Math.abs(a[i]));
  const t=ticksFor(0,m*1.12,3);
  return Math.max(m*1.12,t[t.length-1]);
}

function buildModel(){
  const M={view:ST.view,st:ST};
  M.live=liveSet();                       /* f, and everything derived from it */
  M.shape=shapeSet();                     /* the curve the pointer edits */
  M.predRms=ST.predict?predRms():0;
  M.tools=toolValues(M.live);
  if(ST.view==='corner'||ST.view==='grid'){ M.ref=refSet(); }
  if(ST.view==='grid'){ M.study=gridStudy(); }
  if(ST.view==='ftc'){ M.ftc=ftcSet(); }
  const src=(ST.view==='corner'||ST.view==='grid')?M.ref:M.live;
  M.src=src;
  M.yF=Math.max(rangeOf(src.f,1.0),ST.predict?rangeOf(M.shape.f,1.0):0);
  M.yD=rangeOf(src.d,1.0);
  M.yI=rangeOf(src.F,1.0);
  M.yD2=rangeOf(src.d2,1.0);
  return M;
}

/* ---- notation ----------------------------------------------------- */
/* PhET's Notation preference (Lagrange f'(x) or Leibniz df/dx) and its
   Variable preference (x or t).  Both are real controls in its build. */
function VAR(){ return ST.variable; }
function nameF(){ return 'f('+VAR()+')'; }
function nameD(){
  return ST.notation==='leibniz'
    ? '<i>d</i>f/<i>d</i>'+VAR()
    : 'f&prime;('+VAR()+')';
}
function nameD2(){
  return ST.notation==='leibniz'
    ? '<i>d</i>&sup2;f/<i>d</i>'+VAR()+'&sup2;'
    : 'f&Prime;('+VAR()+')';
}
function nameI(){ return '&int;<sub>0</sub><sup>'+VAR()+'</sup> f d'+VAR(); }
/* the canvas versions: plain glyphs only, no markup and no letter subscripts
   (Known-bad: fillText draws '<sub>' as five characters, and there is no
   Unicode subscript for most letters) */
function cName(k){
  const v=VAR();
  if(k==='f') return 'f('+v+')';
  if(k==='d') return ST.notation==='leibniz'?('df/d'+v):('f′('+v+')');
  if(k==='dd') return ST.notation==='leibniz'?('d²f/d'+v+'²'):('f″('+v+')');
  return '∫ f d'+v;
}

/* ---- the readout -------------------------------------------------- */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function row(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function expo(v){
  if(!isFinite(v)) return '&mdash;';
  if(v===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(v)));
  return fmt(v/Math.pow(10,e),2)+'&times;10<sup>'+e+'</sup>';
}

function readoutHTML(M){
  const S=M.live, T=M.tools;
  let t='<div class="rname">'+({deriv:'the derivative',integ:'the integral',lab:'the lab',
      corner:'the corners',ftc:'the theorem',grid:'the grid'}[M.view])
    +'<small>'+({deriv:'PhET&rsquo;s Derivative screen',integ:'PhET&rsquo;s Integral screen',
      lab:'PhET&rsquo;s Lab and Advanced screens',corner:'where the derivative does not exist',
      ftc:'the fundamental theorem, measured',grid:'what the grid costs'}[M.view])+'</small></div><table>';
  if(M.view==='corner'||M.view==='grid'){
    const R=M.ref;
    t+=hd('the reference shape');
    t+=row('shape',ST.refShape);
    t+=row('width w',fmt(ST.refW,2));
    t+=row('height y',fmt(ST.refY,2));
    t+=row('centre '+VAR()+'<sub>0</sub>',fmt(XG[idxAt(ST.refX)],3));
    t+=row('corners found',String(R.corners.length),R.corners.length?'':'good');
  }
  if(M.view==='deriv'||M.view==='integ'||M.view==='lab'||M.view==='ftc'){
    t+=hd('the curve');
    t+=row('what you are shaping',ST.predict?'your prediction':'f');
    t+=row('mode',ST.mode);
    if(ST.mode!=='freeform'&&ST.mode!=='tilt'&&ST.mode!=='shift')
      t+=row('width w',fmt(ST.width,2));
    t+=row('f range',fmt(Math.min.apply(null,Array.from(S.f)),2)+' &hellip; '
      +fmt(Math.max.apply(null,Array.from(S.f)),2));
    t+=row(cName('d')+' range',fmt(Math.min.apply(null,Array.from(S.d)),2)+' &hellip; '
      +fmt(Math.max.apply(null,Array.from(S.d)),2));
    t+=row('corners',String(S.corners.length));
    if(ST.predict){
      t+=row('your prediction, rms off f',fmt(M.predRms,4),M.predRms<0.05?'good':'bad');
      t+=row('f itself is',ST.showF?'shown':'hidden');
    }
  }
  if(M.view==='deriv'||M.view==='lab'){
    t+=hd('slope of tangent');
    t+=row(VAR(),fmt(ST.xT,3));
    t+=row('f('+VAR()+')',fmt(valueAt(S.f,ST.xT),4));
    t+=row(cName('d'),fmt(T.tan.slope,4),Math.abs(T.tan.slope)>SLOPE_MAX?'bad':'good');
    t+=row('the line meets f at',fmt(T.tan.x0,3)+' and '+fmt(T.tan.x1,3));
  }
  if(M.view==='integ'||M.view==='lab'){
    t+=hd('net signed area');
    t+=row('up to '+VAR(),fmt(ST.xA,3));
    t+=row('above the axis','+'+fmt(T.ar.pos,4));
    t+=row('below the axis','&minus;'+fmt(T.ar.neg,4));
    t+=row('net',fmt(T.ar.net,4),Math.abs(T.ar.net)>AREA_MAX?'bad':'good');
    t+=row('the integral curve',fmt(T.Ia,4));
    t+=row('difference',expo(T.areaMismatch),T.areaMismatch<1e-10?'good':'bad');
  }
  if(M.view==='lab'){
    t+=hd('at the reference line');
    t+=row(VAR(),fmt(ST.xR,3));
    t+=row(cName('I'),fmt(integAt(S.f,S.F,ST.xR),4));
    t+=row('f',fmt(valueAt(S.f,ST.xR),4));
    t+=row(cName('d'),fmt(S.d[cellAt(ST.xR)],4));
    t+=row(cName('dd'),fmt(S.d2[idxAt(ST.xR)],3));
  }
  if(M.view==='corner'){
    const R=M.ref;
    t+=hd('one-sided limits');
    if(!R.corners.length){
      t+=row('this shape has','no corner','good');
      t+=row('largest slope step',expo(maxStep(R.d)));
    } else {
      for(let i=0;i<Math.min(R.corners.length,4);i++){
        const c=R.corners[i];
        t+=row(VAR()+' = '+fmt(c.x,3),'');
        t+=row('&nbsp; from the left',fmt(c.left,4));
        t+=row('&nbsp; from the right',fmt(c.right,4));
        t+=row('&nbsp; jump',fmt(c.jump,4),'bad');
      }
      if(R.corners.length>4) t+=row('and',String(R.corners.length-4)+' more');
    }
  }
  if(M.view==='ftc'){
    const F=M.ftc;
    t+=hd('the two residuals');
    t+=row('&int;'+cName('d')+' &minus; (f &minus; f(0))',expo(F.e1),F.e1<1e-11?'good':'bad');
    t+=row('d/d'+VAR()+' &int;f &minus; f at midpoints',expo(F.e2),F.e2<1e-11?'good':'bad');
    t+=hd('PhET&rsquo;s pair, on this curve');
    t+=row('its D(I(f)) &minus; [1,2,1]f/4',expo(F.e3),F.e3<1e-11?'good':'bad');
    t+=row('its D(I(f)) &minus; f',fmt(F.ePhet,6),'bad');
  }
  if(M.view==='grid'){
    const rows=M.study;
    t+=hd('error against the closed form');
    for(const r of rows){
      t+=row((r.n===NPTS?'<b>':'')+String(r.n-1)+' cells'+(r.n===NPTS?'</b>':''),
             expo(r.ed)+' / '+expo(r.eF));
    }
    t+=row('ratio, last halving',fmt(rows[rows.length-2].ed/rows[rows.length-1].ed,3),'good');
  }
  t+='</table>';
  if(M.view==='ftc')
    t+='<div class="note">Both residuals are floating-point noise, not a '
      +'tolerance: the staggered pair is inverse <b>by construction</b>. The last '
      +'row is what PhET&rsquo;s node-centred derivative of its own trapezium '
      +'integral costs &mdash; second order in dx, and real.</div>';
  else if(M.view==='corner')
    t+='<div class="note">A corner has no derivative. What exists are the two '
      +'one-sided limits, and on this grid they are read off cells that lie '
      +'entirely on one side, so for the triangle they are <b>exact</b>.</div>';
  else if(M.view==='grid')
    t+='<div class="note">The left number is max|f&prime; &minus; g&prime;| at the '
      +'cell midpoints, the right max|&int;f &minus; G| at the nodes. PhET&rsquo;s '
      +'own grid is the bold row.</div>';
  else
    t+='<div class="note">Drag on the f panel to shape the curve. The tangent '
      +'reads the slope of the cell it sits in; the area tool splits every cell '
      +'at its zero crossing and counts the halves separately, so it and the '
      +'integral curve agree by <b>arithmetic</b>, not by construction.</div>';
  return t;
}
function maxStep(d){
  let m=0;
  for(let i=1;i<d.length;i++) m=Math.max(m,Math.abs(d[i]-d[i-1]));
  return m;
}

/* ---- the equation bar --------------------------------------------- */
function eqbarHTML(M){
  const v=VAR();
  const D=nameD(), I=nameI();
  if(M.view==='deriv')
    return '<span class="lhs">'+D+'</span> = lim<sub>h&rarr;0</sub> '
      +'[ f('+v+'+h) &minus; f('+v+') ] / h &nbsp;=&nbsp; <span class="hl">'
      +'( f<sub>i+1</sub> &minus; f<sub>i</sub> ) / &Delta;'+v+'</span> on the cell '
      +v+'<sub>i</sub> &hellip; '+v+'<sub>i+1</sub>'
      +'<span class="sm">the drawn curve is straight across a cell, so that quotient '
      +'is not an approximation to the slope &mdash; it is the slope</span>';
  if(M.view==='integ')
    return '<span class="lhs">'+I+'</span> = &Sigma;<sub>i</sub> <span class="hl">'
      +'&frac12;( f<sub>i</sub> + f<sub>i+1</sub> ) &Delta;'+v+'</span> &nbsp;&mdash;&nbsp; '
      +'area above the axis <span class="hl2">minus</span> area below'
      +'<span class="sm">the trapezium rule is the exact area under a straight segment, '
      +'so the running sum is the exact area under the drawn curve</span>';
  if(M.view==='lab')
    return '<span class="lhs">'+I+'</span> &nbsp;&rarr;&nbsp; <span class="hl">f('+v+')</span> '
      +'&nbsp;&rarr;&nbsp; <span class="hl2">'+D+'</span> &nbsp;&rarr;&nbsp; '+nameD2()
      +'<span class="sm">each arrow is one differentiation; going the other way is one '
      +'integration and a constant</span>';
  if(M.view==='corner')
    return '<span class="lhs">'+D+'</span> exists only if &nbsp;'
      +'lim<sub>h&rarr;0<sup>&minus;</sup></sub> = lim<sub>h&rarr;0<sup>+</sup></sub>'
      +' &nbsp;&mdash;&nbsp; at a corner <span class="hl">they differ</span>'
      +'<span class="sm">so the derivative panel has a jump there and the second '
      +'derivative has a spike whose area is exactly that jump</span>';
  if(M.view==='ftc')
    return '<span class="lhs">d/d'+v+' &int;<sub>0</sub><sup>'+v+'</sup> f</span> = '
      +'<span class="hl">f('+v+')</span> &nbsp;&nbsp;and&nbsp;&nbsp; '
      +'<span class="lhs">&int;<sub>a</sub><sup>b</sup> '+D+'</span> = '
      +'<span class="hl2">f(b) &minus; f(a)</span>'
      +'<span class="sm">both hold here to 10<sup>&minus;12</sup>, which is rounding, not tolerance</span>';
  return '<span class="lhs">trapezium error</span> = +'
    +'<span class="hl">(&Delta;'+v+')&sup2;/12</span> [ g&prime;(b) &minus; g&prime;(a) ] &nbsp;&nbsp;'
    +'<span class="lhs">midpoint slope error</span> = <span class="hl2">(&Delta;'+v+')&sup2;/24</span> g&prime;&prime;&prime;'
    +'<span class="sm">halve &Delta;'+v+' and both fall by four &mdash; that ratio is the claim, not the number</span>';
}

/* ---- the canvas tag (top left) ------------------------------------ */
function tagHTML(M){
  const S=M.live;
  if(M.view==='corner'||M.view==='grid')
    return '<b>'+ST.refShape+'</b> &nbsp; w = '+fmt(ST.refW,2)+' &nbsp; y = '+fmt(ST.refY,2)
      +' &nbsp; on an empty curve';
  return '<b>'+(ST.predict?'predicting f':'f')+'</b> &nbsp; '+ST.mode
    +(SHAPE_MODES.indexOf(ST.mode)>=0?(' &nbsp; w = '+fmt(ST.width,2)):'')
    +' &nbsp; '+S.corners.length+' corner'+(S.corners.length===1?'':'s');
}
