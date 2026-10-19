
/* ================================================================== *
 *  state, actions, the per-view models, readout / eqbar / tag         *
 * ================================================================== */
const TABS=[['atoms','the two atoms'],['well','the well'],['motion','the motion'],
            ['small','small oscillations'],['pairs','the atom pairs'],['steppers','the integrator']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#cfd4de', bg:'#070b18', rep:'#e8705f', att:'#5f8fe8',
           kin:'#b8ec4c', pot:'#5ac8e0', tot:'#e8e8f0'};
const RO_W=300;                     /* the floating readout's footprint */
/* the drawn r window, in units of sigma.  0.72 sigma is V = 227 eps, steep
   enough to look like a wall and finite enough to plot. */
const R_LO_FAC=0.72, R_HI_FAC=3.2;
/* PhET's ForceDisplayMode: HIDDEN (its default), TOTAL, COMPONENTS */
const FORCE_MODES=[['hidden','hidden'],['total','total force'],['components','components']];
/* the frame clock: 2 ps of model time per second of wall clock, so a neon
   pair oscillates about once a second.  PhET's own Slow is half speed. */
const PS_PER_SEC=2.0, SLOW_FACTOR=0.35, DT_INT=1.5e-3;   /* ps */
const TRAIL_MAX=900;

const DEFAULTS={view:'atoms', pair:'NeNe', lit:false, pinned:true, forces:'hidden',
  adjSig:PHET_ADJ_SIGMA, adjEps:PHET_ADJ_EPSILON,
  r:345.71831087929,                       /* r_min of PhET's neon pair (derive) */
  v:0, running:false, slow:false, t:0,
  rel:10, v0f:0,                           /* release offset (pm) and speed (fraction of escape) */
  dtIdx:2, stepper:'verlet', showLit:true, showHarm:true, amp:10};
const ST=Object.assign({},DEFAULTS);
let TRAIL=[];                              /* [t, r, K, V] of the live motion */
function simReset(){ TRAIL=[]; }

/* ---- actions ------------------------------------------------------------- */
function pairOf(st){ return pairParams(st.pair, st.lit, {sig:st.adjSig, eps:st.adjEps}); }
function rBounds(st){ const p=pairOf(st); return [R_LO_FAC*p.sig, R_HI_FAC*p.sig]; }
function setSep(st,r){ const b=rBounds(st); st.r=clamp(r,b[0],b[1]); st.v=0; TRAIL=[]; }
/* PhET's Return Atom button and its resetMovableAtomPos: back to the minimum,
   at rest. */
function returnAtom(st){ st.r=rMin(pairOf(st).sig); st.v=0; st.t=0; st.running=false; TRAIL=[]; }
function setPair(st,key){ st.pair=key; returnAtom(st); }
function setLit(st,on){ st.lit=!!on; returnAtom(st); }
function setPinned(st,on){ st.pinned=!!on; st.v=0; st.t=0; TRAIL=[]; }
/* PhET snaps both adjustable sliders to multiples of 5 and clamps to its own
   MIN/MAX; and it moves the atom back to the new minimum when sigma changes. */
function setAdjSig(st,s){
  st.adjSig=clamp(Math.round(s/5)*5,PHET_MIN_SIGMA,PHET_MAX_SIGMA);
  if(st.pair==='Adj') returnAtom(st);
}
function setAdjEps(st,e){
  st.adjEps=clamp(Math.round(e/5)*5,PHET_MIN_EPSILON,PHET_MAX_EPSILON);
  if(st.pair==='Adj'){ const b=rBounds(st); st.r=clamp(st.r,b[0],b[1]); }
}
/* the motion view's release: r_min + rel, with v0f of the escape speed */
function releaseAtom(st){
  const P=pairInfo(st);
  st.r=clamp(rMin(P.sig)+st.rel,P.rLo,P.rHi);
  st.v=st.v0f*escapeSpeed(st.r,P.sig,P.eps,P.mu);
  st.t=0; TRAIL=[]; st.running=true;
}

/* ---- the pair, fully resolved ------------------------------------------- */
function pairInfo(st){
  const spec=PAIR_BY_KEY[st.pair], pp=pairOf(st);
  const A=ATOM[spec.a], B=ATOM[spec.b];
  const epsE=pp.eps*K_TO_E;
  const mu=effMass(A.m,B.m,st.pinned);
  const sig=pp.sig;
  /* PhET draws each atom at its van der Waals radius; the adjustable pair is
     drawn at sigma/2, which is what PhET does when its diameter slider moves. */
  const rA=spec.key==='Adj'?sig/2:A.r, rB=spec.key==='Adj'?sig/2:B.r;
  return {key:spec.key, label:spec.label, A, B, rA, rB, sig, epsK:pp.eps, eps:epsE,
          lit:pp.lit, src:pp.src, mu, muPin:B.m, muMov:A.m*B.m/(A.m+B.m),
          pinned:st.pinned, rmin:rMin(sig), k:ljK(sig,epsE),
          omega:ljOmega(sig,epsE,mu), period:ljPeriod(sig,epsE,mu),
          rLo:R_LO_FAC*sig, rHi:R_HI_FAC*sig,
          /* the separation at which the attraction is strongest: V''(r) = 0,
             i.e. (sigma/r)^6 = 7/26, r = (26/7)^(1/6) sigma */
          rF:sig*Math.pow(26/7,1/6)};
}

/* ---- the live state of the pair ----------------------------------------- */
function liveModel(st){
  const P=pairInfo(st), r=st.r;
  const V=ljV(r,P.sig,P.eps), F=ljF(r,P.sig,P.eps);
  const K=0.5*P.mu*st.v*st.v, E=K+V;
  const tp=turningPoints(E,P.sig,P.eps);
  return {P, r, V, F, K, E,
          Frep:ljRepulsive(r,P.sig,P.eps), Fatt:ljAttractive(r,P.sig,P.eps),
          bound:E<0, tp, vEsc:escapeSpeed(r,P.sig,P.eps,P.mu),
          period:(E<0&&tp&&isFinite(tp.rOut))?periodQuad(E,P.sig,P.eps,P.mu):Infinity,
          /* PhET draws the atoms at their van der Waals radii; when sigma is
             far below the sum of those radii the spheres overlap at the bottom
             of the well, which the oxygen pair does badly. */
          overlap:(P.rA+P.rB)-P.rmin};
}

/* ---- the curves each view needs ----------------------------------------- */
function wellCurve(P,n,lo,hi){
  const xs=[],ys=[],fs=[],reps=[],atts=[];
  const a=lo===undefined?P.rLo:lo, b=hi===undefined?P.rHi:hi;
  for(let i=0;i<=n;i++){
    const r=a+(b-a)*i/n;
    xs.push(r); ys.push(ljV(r,P.sig,P.eps)/P.eps);
    fs.push(ljF(r,P.sig,P.eps)); reps.push(ljRepulsive(r,P.sig,P.eps));
    atts.push(-ljAttractive(r,P.sig,P.eps));
  }
  return {xs,ys,fs,reps,atts};
}

/* the motion view: the trace so far, the turning points, the phase curve */
function motionModel(st){
  const L=liveModel(st), P=L.P;
  const ph={rs:[],vs:[]};
  if(L.bound&&L.tp&&isFinite(L.tp.rOut)){
    const n=120;
    for(let i=0;i<=n;i++){
      const r=L.tp.rIn+(L.tp.rOut-L.tp.rIn)*i/n;
      const ke=Math.max(L.E-ljV(r,P.sig,P.eps),0);
      ph.rs.push(r); ph.vs.push(Math.sqrt(2*ke/P.mu));
    }
  }
  /* the separatrix E = 0: the orbit that just escapes */
  const sep={rs:[],vs:[]};
  for(let i=0;i<=120;i++){
    const r=P.sig+(P.rHi-P.sig)*i/120;
    const ke=Math.max(-ljV(r,P.sig,P.eps),0);
    sep.rs.push(r); sep.vs.push(Math.sqrt(2*ke/P.mu));
  }
  return {L,ph,sep,trail:TRAIL};
}

/* small oscillations: the harmonic fit, and how fast the true period leaves it.
   Landau's coefficient for the LJ well is exactly 91/4 (derive.py derives V2,
   V3, V4 and checks them by 90-digit finite differences). */
const ANHARM_C=91/4;
function smallModel(st){
  const P=pairInfo(st);
  const A=clamp(st.amp,0.05,60);
  const half=Math.max(A*1.6,P.rmin*0.03);
  const lo=P.rmin-half, hi=P.rmin+half;
  const xs=[],ys=[],hs=[];
  for(let i=0;i<=160;i++){
    const r=lo+(hi-lo)*i/160, x=r-P.rmin;
    xs.push(r); ys.push(ljV(r,P.sig,P.eps)/P.eps);
    hs.push((-P.eps+0.5*P.k*x*x)/P.eps);
  }
  /* the sweep: amplitude a = (r_out - r_in)/2 against the fractional period
     excess, measured by the regularised quadrature */
  const as=[],ex=[],pred=[];
  for(let i=0;i<=26;i++){
    const Ai=0.02*Math.pow(60/0.02,i/26);
    const E=ljV(P.rmin+Ai,P.sig,P.eps);
    const tp=turningPoints(E,P.sig,P.eps);
    if(!tp||!isFinite(tp.rOut)) continue;
    const a=0.5*(tp.rOut-tp.rIn);
    const T=periodQuad(E,P.sig,P.eps,P.mu);
    if(!isFinite(T)) continue;
    as.push(a); ex.push(T/P.period-1); pred.push(ANHARM_C*a*a/(P.rmin*P.rmin));
  }
  const E=ljV(P.rmin+A,P.sig,P.eps), tp=turningPoints(E,P.sig,P.eps);
  const aNow=tp?0.5*(tp.rOut-tp.rIn):0;
  const Tnow=tp&&isFinite(tp.rOut)?periodQuad(E,P.sig,P.eps,P.mu):Infinity;
  return {P,A,lo,hi,xs,ys,hs,as,ex,pred,aNow,Tnow,tp,E,
          predNow:ANHARM_C*aNow*aNow/(P.rmin*P.rmin)};
}

/* the pairs view: every PhET pair's well, and the literature beside it */
function pairsModel(st){
  const rows=PAIRS.map(p=>{
    const phet=pairParams(p.key,false,{sig:st.adjSig,eps:st.adjEps});
    const row={key:p.key,label:p.label,a:p.a,b:p.b,
               sig:phet.sig,eps:phet.eps,rmin:rMin(phet.sig)};
    if(p.key!=='Adj'){
      const l=pairParams(p.key,true,{sig:st.adjSig,eps:st.adjEps});
      row.lsig=l.sig; row.leps=l.eps; row.lrmin=rMin(l.sig); row.lsrc=l.src;
      /* the literature TABLE's own r_min where it prints one */
      row.lrminTab=(p.a===p.b&&LIT[p.a].rmin)?LIT[p.a].rmin:null;
    }
    return row;
  });
  /* Lorentz-Berthelot applied to PhET's OWN like-pair values, against PhET's
     own mixed-pair rows */
  const lb=[['NeAr','Ne','Ar'],['NeO','Ne','O'],['ArO','Ar','O']].map(([k,a,b])=>{
    const pa=PAIR_BY_KEY[a+a], pb=PAIR_BY_KEY[b+b], p=PAIR_BY_KEY[k];
    return {key:k,sig:p.sig,eps:p.eps,lbSig:0.5*(pa.sig+pb.sig),
            lbEps:Math.sqrt(pa.eps*pb.eps),radSum:ATOM[a].r+ATOM[b].r};
  });
  /* the source table's own consistency: r_min/sigma must be 2^(1/6) */
  const tab=LIT_RMIN_TABLE.map(([nm,s,rm])=>({nm,s,rm,ratio:rm/s,err:Math.abs(rm/s-SIXRT2)}));
  /* corresponding states, from PhET's own critical points and the literature
     eps — both retrieved, neither remembered */
  const cs=['Ne','Ar','O'].map(a=>({a,Tc:PHET_CRIT[a],eps:LIT[a].eps,
                                    ratio:PHET_CRIT[a]/LIT[a].eps}));
  const csMean=cs.reduce((s,c)=>s+c.ratio,0)/cs.length;
  return {rows,lb,tab,cs,csMean,
          csSpread:(Math.max.apply(null,cs.map(c=>c.ratio))-
                    Math.min.apply(null,cs.map(c=>c.ratio)))/csMean};
}

/* the integrator view: order and boundedness.  Cached on the pair, because the
   long runs are the only expensive thing in the file. */
const DT_LIST=[4e-3,2e-3,1e-3,5e-4,2.5e-4];
let STEP_CACHE={key:null,val:null};
function stepperModel(st){
  const P=pairInfo(st);
  const key=[P.sig,P.eps,P.mu].join('|');
  if(STEP_CACHE.key===key) return Object.assign({P},STEP_CACHE.val);
  const r0=P.rmin+10, E0=ljV(r0,P.sig,P.eps);
  /* the quadrature period, or the harmonic one if that orbit is not bound:
     every step count below is derived from it, so it has to be finite */
  let T=periodQuad(E0,P.sig,P.eps,P.mu);
  if(!(T>0)||!isFinite(T)) T=P.period;
  const kinds=['verlet','symplectic','forward'];
  const curves={};
  kinds.forEach(k=>{
    const es=DT_LIST.map(dt=>energyExcursion(r0,0,P.sig,P.eps,P.mu,dt,
                                             Math.round(T/dt),k).worst);
    const lo=Math.log(es[0]/es[es.length-1])/Math.log(DT_LIST[0]/DT_LIST[DT_LIST.length-1]);
    curves[k]={es,order:lo};
  });
  /* the drift trace: |E(t)-E(0)|/eps sampled through 20 periods at 1e-3 ps */
  const dtD=1e-3, nPer=20;
  const nStep=Math.min(MAX_STEPS,Math.max(0,Math.round(nPer*T/dtD)||0));
  const every=Math.max(1,Math.round(nStep/240));
  const drift={};
  kinds.forEach(k=>{
    const step=STEPPERS[k], s=ljState(r0,0,P.sig,P.eps,P.mu);
    const e0=ljEnergy(s,P.sig,P.eps,P.mu), ts=[],ds=[];
    for(let i=0;i<nStep;i++){
      step(s,P.sig,P.eps,P.mu,dtD);
      if(i%every===0){ ts.push(s.t/T); ds.push(Math.abs(ljEnergy(s,P.sig,P.eps,P.mu)-e0)/P.eps); }
    }
    drift[k]={ts,ds,last:ds.length?ds[ds.length-1]:0};
  });
  const val={T,r0,E0,curves,drift,dts:DT_LIST,dtD,nPer};
  STEP_CACHE={key,val};
  return Object.assign({P},val);
}

function buildModel(){
  const st=ST, view=st.view, M={view,st};
  M.L=liveModel(st);
  M.P=M.L.P;
  if(view==='atoms'||view==='well') M.C=wellCurve(M.P,260);
  else if(view==='motion') M.MO=motionModel(st);
  else if(view==='small') M.SM=smallModel(st);
  else if(view==='pairs') M.PR=pairsModel(st);
  else if(view==='steppers') M.IT=stepperModel(st);
  return M;
}

/* ================================================================== *
 *  formatting                                                         *
 * ================================================================== */
function meV(e){ return e*E_TO_MEV; }
function pN(f){ return f*F_TO_PN; }
function eK(e){ return e/K_TO_E; }                 /* energy -> eps/k_B in K   */
function sciPlain(x,n){
  if(!isFinite(x)) return '—';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x))), m=x/Math.pow(10,e);
  return fmt(m,n===undefined?2:n)+'×10'+supDigits(e);
}
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function supDigits(e){ return String(e).split('').map(c=>SUPS[c]||c).join(''); }
function sciHTML(x,n){
  if(!isFinite(x)) return '&mdash;';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x))), m=x/Math.pow(10,e);
  return fmt(m,n===undefined?3:n)+' &times; 10<sup>'+String(e).replace('-','&minus;')+'</sup>';
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function pairRows(M){
  const P=M.P, L=M.L;
  let s=hd('the pair &mdash; '+(P.lit?'literature':'PhET&rsquo;s')+' parameters')
    +rrow('&epsilon;/k<sub>B</sub>',sigf(P.epsK,5)+' K')
    +rrow('&epsilon;',sigf(meV(P.eps),4)+' meV')
    +rrow('&sigma;',sigf(P.sig,5)+' pm')
    +rrow('r<sub>min</sub> = 2<sup>1/6</sup>&sigma;',sigf(P.rmin,6)+' pm','good')
    +rrow('reduced mass &mu;',sigf(P.mu,5)+' u');
  s+=hd('where the atom is')
    +rrow('separation r',sigf(L.r,5)+' pm','good')
    +rrow('r / &sigma;',fmt(L.r/P.sig,4))
    +rrow('V(r)',sigf(meV(L.V),4)+' meV')
    +rrow('V(r) / &epsilon;',fmt(L.V/P.eps,4))
    +rrow('F(r) = &minus;dV/dr',sigf(pN(L.F),4)+' pN',L.F>0?'bad':'good')
    +rrow('',L.F>0?'repulsive':(L.F<0?'attractive':'zero &mdash; at the minimum'));
  return s;
}
function readoutHTML(M){
  const P=M.P, L=M.L, st=M.st;
  let s='<div class="rname">atomic interactions<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='atoms'){
    s+=pairRows(M);
    s+=hd('PhET&rsquo;s two halves')
      +rrow('repulsive, 48&epsilon;&sigma;<sup>12</sup>/r<sup>13</sup>',sigf(pN(L.Frep),4)+' pN')
      +rrow('attractive, 24&epsilon;&sigma;<sup>6</sup>/r<sup>7</sup>','&minus;'+sigf(pN(L.Fatt),4)+' pN')
      +rrow('their difference',sigf(pN(L.Frep-L.Fatt),4)+' pN','good');
    s+=hd('the drawn atoms')
      +rrow('radii (van der Waals)',fmt(P.rA,0)+', '+fmt(P.rB,0)+' pm')
      +rrow('they touch at',fmt(P.rA+P.rB,0)+' pm')
      +rrow('overlap at r<sub>min</sub>',L.overlap>0?fmt(L.overlap,0)+' pm':'none',L.overlap>0?'bad':'good');
  }
  else if(M.view==='well'){
    s+=pairRows(M);
    s+=hd('the three landmarks')
      +rrow('V(&sigma;)','0 exactly','good')
      +rrow('V(r<sub>min</sub>)','&minus;'+sigf(meV(P.eps),4)+' meV = &minus;&epsilon;','good')
      +rrow('F(r<sub>min</sub>)','0 exactly','good')
      +rrow('strongest pull at (26/7)<sup>1/6</sup>&sigma;',sigf(P.rF,5)+' pm')
      +rrow('and it is',sigf(pN(-ljF(P.rF,P.sig,P.eps)),4)+' pN');
  }
  else if(M.view==='motion'){
    const tp=L.tp;
    s+=pairRows(M);
    s+=hd('the motion')
      +rrow('speed |dr/dt|',sigf(Math.abs(st.v),4)+' m/s')
      +rrow('kinetic energy',sigf(meV(L.K),4)+' meV')
      +rrow('total E',sigf(meV(L.E),4)+' meV',L.bound?'good':'bad')
      +rrow('E / &epsilon;',fmt(L.E/P.eps,4))
      +rrow('bound?',L.bound?'yes &mdash; it oscillates':'no &mdash; it escapes',L.bound?'good':'bad');
    if(L.bound&&tp&&isFinite(tp.rOut)) s+=rrow('turning points',fmt(tp.rIn,1)+' &ndash; '+fmt(tp.rOut,1)+' pm')
      +rrow('period (quadrature)',sigf(L.period,5)+' ps','good')
      +rrow('2&pi;/&omega; (harmonic)',sigf(P.period,5)+' ps');
    else s+=rrow('escape speed at this r',sigf(L.vEsc,4)+' m/s');
    s+=rrow('clock t',fmt(st.t,3)+' ps');
  }
  else if(M.view==='small'){
    const S=M.SM;
    s+=hd('the harmonic limit')
      +rrow('V&Prime;(r<sub>min</sub>) = 72&epsilon;/(2<sup>1/3</sup>&sigma;&sup2;)',sigf(P.k,6)+' u/ps&sup2;','good')
      +rrow('&omega; = &radic;(V&Prime;/&mu;)',sigf(P.omega,6)+' rad/ps','good')
      +rrow('in SI',sciHTML(P.omega*1e12,4)+' rad/s')
      +rrow('T = 2&pi;/&omega;',sigf(P.period,6)+' ps','good')
      +rrow('&mu; (left atom '+(P.pinned?'pinned':'free')+')',sigf(P.mu,6)+' u')
      +rrow('the other choice would give',sigf(ljPeriod(P.sig,P.eps,P.pinned?P.muMov:P.muPin),6)+' ps');
    s+=hd('how far from harmonic')
      +rrow('release offset A',fmt(S.A,3)+' pm')
      +rrow('amplitude a = (r<sub>out</sub>&minus;r<sub>in</sub>)/2',sigf(S.aNow,5)+' pm')
      +rrow('true period',sigf(S.Tnow,6)+' ps')
      +rrow('T/T<sub>0</sub> &minus; 1',sciHTML(S.Tnow/P.period-1,3),'good')
      +rrow('(91/4) a&sup2;/r<sub>min</sub>&sup2;',sciHTML(S.predNow,3),'good');
  }
  else if(M.view==='pairs'){
    const R=M.PR;
    s+=hd('PhET&rsquo;s &sigma; is the literature r<sub>min</sub>');
    ['Ne','Ar'].forEach(a=>{
      const row=R.rows.find(r2=>r2.key===a+a);
      s+=rrow(ATOM[a].name+': PhET &sigma;',fmt(row.sig,1)+' pm')
        +rrow('&nbsp;&nbsp;literature &sigma;',fmt(row.lsig,1)+' pm ('+fmt(100*(row.sig/row.lsig-1),1)+'%)','bad')
        +rrow('&nbsp;&nbsp;literature r<sub>min</sub>',fmt(row.lrminTab,1)+' pm ('+fmt(100*(row.sig/row.lrminTab-1),1)+'%)','good');
    });
    s+=hd('the source table checks itself')
      +rrow('worst |r<sub>min</sub>/&sigma; &minus; 2<sup>1/6</sup>|',
            sciHTML(Math.max.apply(null,R.tab.map(t=>t.err)),2),'good');
    s+=hd('corresponding states')
      +rrow('mean kT<sub>c</sub>/&epsilon;',fmt(R.csMean,4),'good')
      +rrow('spread',fmt(100*R.csSpread,1)+'%');
  }
  else{
    const I=M.IT;
    s+=hd('one period at five step sizes')
      +rrow('velocity Verlet order',fmt(I.curves.verlet.order,4),'good')
      +rrow('symplectic Euler order',fmt(I.curves.symplectic.order,4))
      +rrow('forward Euler order',fmt(I.curves.forward.order,4));
    s+=hd('after '+I.nPer+' periods at &Delta;t = 1 fs')
      +rrow('Verlet |&Delta;E|/&epsilon;',sciHTML(I.drift.verlet.last,3),'good')
      +rrow('symplectic Euler',sciHTML(I.drift.symplectic.last,3),'good')
      +rrow('forward Euler',sciHTML(I.drift.forward.last,3),'bad');
    s+=hd('the run')
      +rrow('released at rest at',fmt(I.r0,2)+' pm')
      +rrow('its period',sigf(I.T,6)+' ps');
  }
  s+='</table><div class="note">'+(P.lit
    ? '<b>Literature</b> &epsilon;, &sigma; are live: '+P.src+'. '
    : '<b>PhET&rsquo;s</b> &epsilon;, &sigma; are live ('+P.src+', build 1.2.21). ')
    +'&epsilon; is quoted the way the literature quotes it, as &epsilon;/k<sub>B</sub> in kelvin. '
    +'k<sub>B</sub> and m<sub>u</sub>: CODATA 2022 through scipy.constants. Every closed form is '
    +'pinned in selfTest to build/atomic-interactions/derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='atoms') return E('<span class="hl">V(r) = 4&epsilon;[ (&sigma;/r)<sup>12</sup> &minus; (&sigma;/r)<sup>6</sup> ]</span>'
    +' &nbsp;&middot;&nbsp; V(&sigma;) = 0 &nbsp;&middot;&nbsp; <span class="hl2">V(2<sup>1/6</sup>&sigma;) = &minus;&epsilon;</span>',
    'the Lennard-Jones pair potential: an r⁻¹² wall from the electrons refusing to overlap, an r⁻⁶ pull from their correlated fluctuations');
  if(M.view==='well') return E('<span class="hl">F(r) = &minus;dV/dr = (24&epsilon;/r)[ 2(&sigma;/r)<sup>12</sup> &minus; (&sigma;/r)<sup>6</sup> ]</span>'
    +' &nbsp;&middot;&nbsp; F = 0 at r<sub>min</sub> &nbsp;&middot;&nbsp; F most negative at (26/7)<sup>1/6</sup>&sigma;',
    'the force is minus the slope of the curve: uphill to the left, downhill to the right, and flat exactly at the bottom');
  if(M.view==='motion') return E('<span class="hl">E = &frac12;&mu;(dr/dt)&sup2; + V(r)</span>'
    +' &nbsp;&middot;&nbsp; V(r) = E at the turning points &nbsp;&middot;&nbsp; u = (&sigma;/r)<sup>6</sup>: <span class="hl2">u<sub>in</sub> + u<sub>out</sub> = 1</span>',
    'the total energy is fixed, so the atom turns round wherever the curve rises to meet it — and with E ≥ 0 it never turns round at all');
  if(M.view==='small') return E('<span class="hl">&omega; = &radic;(V&Prime;(r<sub>min</sub>)/&mu;)</span>'
    +' &nbsp;&middot;&nbsp; V&Prime;(r<sub>min</sub>) = 72&epsilon;/(2<sup>1/3</sup>&sigma;&sup2;) &nbsp;&middot;&nbsp; '
    +'<span class="hl2">T(a) = T<sub>0</sub>[1 + (91/4) a&sup2;/r<sub>min</sub>&sup2;]</span>',
    'near the bottom every well is a parabola, so the period does not depend on amplitude — until it does, quadratically');
  if(M.view==='pairs') return E('<span class="hl">&sigma;<sub>AB</sub> = (&sigma;<sub>A</sub>+&sigma;<sub>B</sub>)/2</span>'
    +' &nbsp;&middot;&nbsp; <span class="hl2">&epsilon;<sub>AB</sub> = &radic;(&epsilon;<sub>A</sub>&epsilon;<sub>B</sub>)</span>'
    +' &nbsp;&middot;&nbsp; r<sub>min</sub>/&sigma; = 2<sup>1/6</sup> = 1.1225',
    'the Lorentz–Berthelot combining rules, which is how a mixed pair is usually guessed from two like pairs');
  return E('<span class="hl">max|E(t) &minus; E(0)| &prop; &Delta;t<sup>p</sup></span>'
    +' &nbsp;&middot;&nbsp; velocity Verlet p = 2 &nbsp;&middot;&nbsp; semi-implicit Euler p = 1 &nbsp;&middot;&nbsp; '
    +'<span class="hl2">symplectic &rArr; bounded</span>',
    'a symplectic stepper conserves a nearby energy exactly, so its error oscillates for ever instead of growing');
}
function tagHTML(M){
  const P=M.P, L=M.L;
  const who=P.label+' &mdash; &epsilon;/k'+'<sub>B</sub> '+sigf(P.epsK,4)+' K, &sigma; '+sigf(P.sig,4)+' pm'
    +' ('+(P.lit?'literature':'PhET')+')';
  if(M.view==='pairs') return '<b>the atom pairs</b> — PhET’s seven wells, and the literature beside them';
  if(M.view==='steppers') return '<b>the integrator</b> — '+P.label+', released 10 pm outside the minimum';
  return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b> — '+plain(who)
    +(M.view==='atoms'||M.view==='motion'?', r = '+fmt(L.r,1)+' pm':'');
}
