
/* ================================================================== *
 *  state, actions, the per-view models, readout / eqbar / tag         *
 * ================================================================== */
const TABS=[['lab','the lab'],['inv','the inverse square'],['prod','the mass product'],['fall','let them go']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           text:'#cfd4de', bg:'#070b18', b1:'#7e9be6', b2:'#e07e74', ruler:'#c9b458', vel:'#cd35c4'};
const RO_W=300;                       /* the floating readout's footprint (stageLayout reserves it) */
const G0=9.80665;                     /* standard gravity, exact by definition — only for "the weight of" */
const ARROW_E0=-10, ARROW_KMAX=17;    /* arrow scale ladder: 1e-10 ... 5e-5 N per metre of arrow */

const DEFAULTS={view:'lab', m1:100, m2:400, i1:-30, i2:10, cs:false,      /* PhET's defaults */
                fmode:'dec', arrowK:9, showDist:true, rulerI:-50, rulerY:null, running:true};
const ST=Object.assign({},DEFAULTS);

/* ---- the fall run: FALL_FRAMES frames from the lab's state at "release" ---- */
const RUN={active:false, frame:0, F:null};
function simReset(){ RUN.active=false; RUN.frame=0; RUN.F=null; }
function startRun(st){
  const L=labModel(st);
  RUN.F=fallModel(st.m1,st.m2,L.x1,L.x2,st.cs); RUN.frame=0; RUN.active=true; return true;
}
function runStep(){
  if(!RUN.active||RUN.frame>=FALL_FRAMES) return false;
  RUN.frame++; return true;
}

/* ---- actions: every change goes through PhET's rules, and stops a run ----- */
function setMass(st,k,m){
  const v=clamp(Math.round(m/M_STEP)*M_STEP,M_MIN,M_MAX);
  if(k===1) st.m1=v; else st.m2=v;
  const n=pairSteps(st.m1,st.m2,st.cs), p=settlePair(st.i1,st.i2,n,TRACK.iL,TRACK.iR,k);
  st.i1=p[0]; st.i2=p[1]; simReset();
}
/* the size mode changes both radii; PhET's radii update m1 first, so m2 is
   the body that "changed last" and m1 is the one pushed aside */
function setConstSize(st,cs){
  st.cs=!!cs;
  const n=pairSteps(st.m1,st.m2,st.cs), p=settlePair(st.i1,st.i2,n,TRACK.iL,TRACK.iR,2);
  st.i1=p[0]; st.i2=p[1]; simReset();
}
function setPos(st,k,x){
  const n=pairSteps(st.m1,st.m2,st.cs), i=dragSteps(TRACK,k,x,st.i1,st.i2,n);
  if(k===1) st.i1=i; else st.i2=i;
  simReset();
}
/* the ruler: its zero tick on the grid, anywhere from half a ruler left of the
   track to its right end (PhET's bounds); y is free (null = home) */
function setRuler(st,x0,y){
  st.rulerI=clamp(symRound(x0*TRACK.perM),TRACK.iL-(TRACK.iR-TRACK.iL)/2,TRACK.iR);
  if(y!==undefined) st.rulerY=y;
}
function rulerHome(st){ st.rulerI=TRACK.iL; st.rulerY=null; }
function rulerToM1(st){ st.rulerI=st.i1; st.rulerY=0; }

/* ---- the models -------------------------------------------------------------- */
function labModel(st){
  const r1=sphereRadius(st.m1,st.cs), r2=sphereRadius(st.m2,st.cs), n=pairSteps(st.m1,st.m2,st.cs);
  const x1=posOf(TRACK,st.i1), x2=posOf(TRACK,st.i2), r=(st.i2-st.i1)/TRACK.perM;
  const F1=forceOn(TRACK.C,st.m1,st.m2,x1,x2,1), F2=forceOn(TRACK.C,st.m1,st.m2,x1,x2,2);
  const Fmag=forceMag(TRACK.C,st.m1,st.m2,r);
  return {m1:st.m1,m2:st.m2,cs:st.cs,r1,r2,n,dmin:n/TRACK.perM,x1,x2,r,gap:r-r1-r2,F1,F2,Fmag,
          Fr2:Fmag*r*r,Gm1m2:G_N*st.m1*st.m2,wtKg:Fmag/G0,Fphet:G_PHET*st.m1*st.m2/(r*r),
          per:arrowStep(st.arrowK,ARROW_E0),
          lab1:forceLabel('m₁','m₂',F1,st.fmode,12),lab2:forceLabel('m₂','m₁',F2,st.fmode,12)};
}
/* the inverse-square view: the engine's shared sampler over this track */
function invModel(L){
  return invSample(TRACK.C,L.m1,L.m2,L.r,L.r1+L.r2,L.dmin,(TRACK.iR-TRACK.iL)/TRACK.perM);
}
/* the mass-product view: contour levels at the live distance, the two lines,
   and the strongest pull of two equal masses in each size mode */
function prodModel(L){
  const k=G_N/(L.r*L.r), levels=[];
  const Flo=k*M_MIN*M_MIN, Fhi=k*M_MAX*M_MAX;
  for(let e=Math.floor(Math.log10(Flo));e<=Math.ceil(Math.log10(Fhi));e++)
    for(const c of [1,2,5]){ const F=c*Math.pow(10,e); if(F>Flo*1.0001&&F<Fhi*0.9999) levels.push(F); }
  const ms=[], fsc=[], fcs=[];
  for(let m=M_MIN;m<=M_MAX;m+=M_STEP){ ms.push(m); fsc.push(fmaxEqual(m,false)); fcs.push(fmaxEqual(m,true)); }
  const slopeSc=Math.log10(fsc[fsc.length-1]/fsc[0])/Math.log10(M_MAX/M_MIN);
  const slopeCs=Math.log10(fcs[fcs.length-1]/fcs[0])/Math.log10(M_MAX/M_MIN);
  /* each contour m1 m2 = F / k, log-spaced in m1 where it lies inside [0, M_MAX]^2 */
  const contours=levels.map(F=>{ const c=F/k, a=c/M_MAX, m1s=[], m2s=[];
    for(let i=0;i<=80;i++){ const m1=a*Math.pow(M_MAX/a,i/80); m1s.push(m1); m2s.push(c/m1); }
    return {F,c,m1s,m2s,decade:Math.abs(Math.log10(F)-Math.round(Math.log10(F)))<1e-9}; });
  const live={c:L.m1*L.m2,m1s:[],m2s:[]};
  for(let i=0;i<=80;i++){ const m1=live.c/M_MAX*Math.pow(M_MAX*M_MAX/live.c,i/80); live.m1s.push(m1); live.m2s.push(live.c/m1); }
  /* the pairs on PhET's grid that could NOT sit this far apart in the current
     size mode: for each m1, the lightest blocked m2 (null: none) */
  const steps=Math.round(L.r*TRACK.perM), edge=[];
  let nBlocked=0;
  for(let m1=M_MIN;m1<=M_MAX;m1+=M_STEP){ let e=null;
    for(let m2=M_MIN;m2<=M_MAX;m2+=M_STEP) if(pairSteps(m1,m2,L.cs)>steps){ e=m2; break; }
    edge.push(e); if(e!==null) nBlocked+=(M_MAX-e)/M_STEP+1; }
  return {k,levels,Flo,Fhi,ms,fsc,fcs,slopeSc,slopeCs,dFdm1:k*L.m2,dFdm2:k*L.m1,contours,live,edge,nBlocked,
          FmaxHere:fmaxEqual(Math.max(L.m1,L.m2),L.cs)};
}
/* the fall's curves against time (they do not change during a run: memoised) */
let FALL_MEMO={key:'',val:null};
function fallCurves(F){
  const key=[F.m1,F.m2,F.x10,F.x20,F.rc].join('|');
  if(FALL_MEMO.key===key) return FALL_MEMO.val;
  const ts=[], x1s=[], x2s=[], rs=[];
  for(let i=0;i<=120;i++){ const s=fallState(F,F.tc*i/120); ts.push(s.t); x1s.push(s.x1); x2s.push(s.x2); rs.push(s.r); }
  FALL_MEMO={key,val:{ts,x1s,x2s,rs}};
  return FALL_MEMO.val;
}
/* the ladder step that draws a quantity q at no more than `room` display units */
function ladderFor(q,room,e0){ let k=0; while(k<60&&q/arrowStep(k,e0)>room) k++; return arrowStep(k,e0); }

function buildModel(){
  const st=ST, L=labModel(st);
  const M={view:st.view,st,L};
  if(st.view==='inv') M.I=invModel(L);
  if(st.view==='prod') M.P=prodModel(L);
  if(st.view==='fall'){
    M.Fa=RUN.active?RUN.F:fallModel(st.m1,st.m2,L.x1,L.x2,st.cs);
    M.run=RUN.active;
    M.fs=fallState(M.Fa,RUN.active?RUN.frame/FALL_FRAMES*M.Fa.tc:0);
    M.done=RUN.active&&RUN.frame>=FALL_FRAMES;
    M.Fc=fallCurves(M.Fa);
    /* the fall's own arrow scales, fixed for the run so the arrows grow as the
       spheres close: the contact force fits 4.5 m, the fastest speed 3 m */
    const s1=fallState(M.Fa,M.Fa.tc);
    M.perF=ladderFor(Math.abs(s1.F1),4.5,-12); M.perV=ladderFor(Math.max(Math.abs(s1.v1),Math.abs(s1.v2)),3,-9);
  }
  return M;
}

/* ---- the shared lab drawing reads a descriptor, not the state ---- */
function sphereFill(k,m,cs){
  const base=k===1?COL.b1:COL.b2;
  return cs?mix(COL.bg,base,0.3+0.7*m/M_MAX):base;     /* constant size: the colour carries the mass */
}
function labSpec(M){
  const L=M.L, st=M.st;
  return {capFull:LAB_CAP_FULL,capShort:LAB_CAP_SHORT,xL:TRACK.iL/TRACK.perM,xR:TRACK.iR/TRACK.perM,
    rmax:sphereRadius(M_MAX,false),pad:0.15,unit:'m',
    bodies:[{x:L.x1,r:L.r1,fill:sphereFill(1,L.m1,st.cs),rim:COL.b1,name:'m₁',sub:fmt(L.m1,0)+' kg',sign:''},
            {x:L.x2,r:L.r2,fill:sphereFill(2,L.m2,st.cs),rim:COL.b2,name:'m₂',sub:fmt(L.m2,0)+' kg',sign:''}],
    F:[L.F1,L.F2],per:L.per,labels:[L.lab1,L.lab2],
    arrowText:'force arrows: 1 m of arrow = '+sciPlain(L.per,1)+' N',
    showDist:st.showDist,distText:'r = '+fmt(L.r,1)+' m between centres',
    ruler:{x0:st.rulerI/TRACK.perM,y:st.rulerY,len:(TRACK.iR-TRACK.iL)/TRACK.perM,major:1,minorPer:5,
           labels:['0','1','2','3','4','5','6','7','8','9','10'],unit:'metres'},
    legend:{len:1,text:'1 m'},dimRow:true};
}
function invSpec(M){
  const L=M.L, I=M.I;
  return {I,r:L.r,F:L.Fmag,unit:'m',uPerM:1,pair:'m₁ = '+fmt(L.m1,0)+' kg, m₂ = '+fmt(L.m2,0)+' kg, attracting',
          gapText:'PhET’s gap',capFull:INV_CAP_FULL,capShort:INV_CAP_SHORT,prodName:'G m₁m₂'};
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function fN(x){ return sciHTML(x,4)+' N'; }
function readoutHTML(M){
  const st=M.st, L=M.L;
  let s='<div class="rname">gravity force lab<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  s+=hd('the spheres')+rrow('m<sub>1</sub>, m<sub>2</sub>',fmt(L.m1,0)+' kg, '+fmt(L.m2,0)+' kg')
    +rrow(st.cs?'radii (constant size)':'radii at 150 kg/m&sup3;',sigf(L.r1,3)+' m, '+sigf(L.r2,3)+' m');
  if(M.view==='lab'||M.view==='inv'||M.view==='prod'){
    s+=hd('the distance')+rrow('between centres, r',fmt(L.r,1)+' m','good')+rrow('between surfaces',sigf(L.gap,3)+' m')
      +rrow('closest PhET allows',fmt(L.dmin,1)+' m');
    s+=hd('the force')+rrow('F = G m<sub>1</sub>m<sub>2</sub>/r<sup>2</sup>',fN(L.Fmag),'good')
      +rrow('on m<sub>1</sub>, on m<sub>2</sub> (along +x)',sciHTML(L.F1,4)+', '+sciHTML(L.F2,4))
      +rrow('F r<sup>2</sup> = G m<sub>1</sub>m<sub>2</sub>',sciHTML(L.Fr2,4)+' N m&sup2;')
      +rrow('the weight of',sigf(L.wtKg*1e9,3)+' &micro;g on Earth');
  }
  if(M.view==='lab'){
    s+=hd('the drawing')+rrow('arrow scale',sciHTML(L.per,1)+' N per metre')+rrow('ruler zero at',fmt(st.rulerI/TRACK.perM,1)+' m');
  }
  else if(M.view==='inv'){
    const I=M.I;
    s+=hd('the law')+rrow('F at 2r',fN(I.F2r))+rrow('F(r) / F(2r)',fmt(L.Fmag/I.F2r,6),'good')
      +rrow('log-log slope at r',fmt(I.slope,6),'good')+rrow('reachable r',fmt(I.dmin,1)+' &ndash; '+fmt(I.rTrack,0)+' m')
      +rrow('F there',sciHTML(I.Fnear,3)+' &ndash; '+sciHTML(I.Ffar,3)+' N');
  }
  else if(M.view==='prod'){
    const P=M.P;
    s+=hd('the product')+rrow('m<sub>1</sub>m<sub>2</sub>',sigf(L.m1*L.m2,4)+' kg&sup2;')+rrow('F per kg of m<sub>1</sub>',fN(P.dFdm1))
      +rrow('F per kg of m<sub>2</sub>',fN(P.dFdm2))+rrow('strongest pull, two '+fmt(Math.max(L.m1,L.m2),0)+'-kg spheres',fN(P.FmaxHere));
    s+=hd('equal masses, 10 &rarr; 1000 kg')+rrow('F<sub>max</sub> slope, constant size',fmt(P.slopeCs,3))+rrow('F<sub>max</sub> slope, real size',fmt(P.slopeSc,3),'good');
  }
  else {
    const F=M.Fa, fs=M.fs;
    s+=hd('released at r<sub>0</sub> = '+fmt(F.r0,1)+' m')+rrow('they touch at r = r<sub>1</sub> + r<sub>2</sub>',sigf(F.rc,4)+' m')
      +rrow('after',hms(F.tc),'good')+rrow('closing speed then',sigf(Math.abs(fallState(F,F.tc).rdot)*1000,3)+' mm/s')
      +rrow('centre of mass (fixed)',sigf(F.xcm,4)+' m')+rrow('clock',sigf(F.clock,3)+'&times; real time');
    s+=hd(M.run?(M.done?'touching':'falling'):'not released')+rrow('t',hms(fs.t))+rrow('r',sigf(fs.r,5)+' m')
      +rrow('v<sub>1</sub>, v<sub>2</sub>',sciHTML(fs.v1,3)+', '+sciHTML(fs.v2,3)+' m/s')
      +rrow('m<sub>1</sub>v<sub>1</sub> + m<sub>2</sub>v<sub>2</sub>',sciHTML(F.m1*fs.v1+F.m2*fs.v2,2)+' kg m/s','good');
  }
  s+='</table><div class="note">G = 6.6743 &times; 10<sup>&minus;11</sup> m&sup3; kg<sup>&minus;1</sup> s<sup>&minus;2</sup> (CODATA 2022). '
    +'PhET uses 6.67408 &times; 10<sup>&minus;11</sup> (CODATA 2014), so its readout here would say '+sciHTML(L.Fphet,6)+' N. '
    +'Everything is pinned in selfTest to derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='lab') return E('<span class="hl">F = G m<sub>1</sub>m<sub>2</sub> / r<sup>2</sup></span> &nbsp;&middot;&nbsp; F<sub>on 1</sub> = &minus;F<sub>on 2</sub> &nbsp;&middot;&nbsp; G = 6.6743 &times; 10<sup>&minus;11</sup> m<sup>3</sup> kg<sup>&minus;1</sup> s<sup>&minus;2</sup>',
    'Newton’s law of gravitation: each sphere pulls the other with the same force, along the line between their centres');
  if(M.view==='inv') return E('F &prop; 1/r<sup>2</sup> &nbsp;&middot;&nbsp; log F = log(G m<sub>1</sub>m<sub>2</sub>) &minus; 2 log r &nbsp;&middot;&nbsp; <span class="hl">F r<sup>2</sup> = G m<sub>1</sub>m<sub>2</sub></span>',
    'double the distance and the force falls to a quarter: on log–log axes the law is a straight line of slope −2');
  if(M.view==='prod') return E('<span class="hl">F = (G / r<sup>2</sup>) m<sub>1</sub> m<sub>2</sub></span> &nbsp;&middot;&nbsp; F<sub>max</sub>(m) = G m<sup>2</sup> / d<sub>min</sub>(m)<sup>2</sup>, &nbsp; d<sub>min</sub> &asymp; 2(3m/4&pi;&rho;)<sup>1/3</sup>',
    'the force is proportional to each mass: every hyperbola m₁m₂ = const is one force — and heavier spheres are bigger, so they cannot get as close');
  return E('r&Prime; = &minus;G(m<sub>1</sub>+m<sub>2</sub>)/r<sup>2</sup> &nbsp;&middot;&nbsp; <span class="hl">t = &radic;(r<sub>0</sub><sup>3</sup>/2GM) [&radic;(x(1&minus;x)) + asin &radic;(1&minus;x)]</span>, &nbsp;x = r/r<sub>0</sub> &nbsp;&middot;&nbsp; m<sub>1</sub>v<sub>1</sub> + m<sub>2</sub>v<sub>2</sub> = 0',
    'released from rest the spheres fall together; the centre of mass never moves, so the lighter one covers more of the gap');
}
function tagHTML(M){
  const L=M.L;
  const base=' — m₁ '+fmt(L.m1,0)+' kg, m₂ '+fmt(L.m2,0)+' kg, r = '+fmt(L.r,1)+' m';
  if(M.view==='fall') return '<b>let them go</b>'+base+(M.run?(M.done?', touching':', falling'):'');
  return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b>'+base+(M.L.cs?', constant size':'');
}
