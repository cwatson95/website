
/* ================================================================== *
 *  state, actions, the per-view models, readout / eqbar / tag         *
 * ================================================================== */
const TABS=[['macro','macro scale'],['atomic','atomic scale'],['inv','the inverse square'],
            ['prod','the charge product'],['grav','electricity and gravity']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           text:'#cfd4de', bg:'#070b18', plus:'#e8705f', minus:'#5f8fe8', zero:'#6b7285', ruler:'#c9b458'};
const RO_W=300;                                   /* the floating readout's footprint (stageLayout reserves it) */
/* the force-arrow ladders: macro in N per cm of arrow (1e-2 ... 5e4), atomic in N per pm (1e-12 ... 5e-6) */
const ARROW_E0={macro:-2,atomic:-12}, ARROW_KMAX=20;
const PRE={macro:'m',atomic:'a'};
const SCREENS=['macro','atomic'];

/* PhET's defaults: macro -4 uC at -1 cm and +8 uC at +2 cm, decimal readout;
   atomic -2e at -20 pm and +4e at +20 pm, scientific readout */
const DEFAULTS={view:'macro', scale:'macro', showDist:true,
  mq1:-4, mq2:8, mi1:-10, mi2:20, mRulerI:-50, mRulerY:null, mForce:true, mSci:false, mArrowK:13,
  aq1:-2, aq2:4, ai1:-20, ai2:20, aRulerI:-50, aRulerY:null, aForce:true, aSci:true, aArrowK:15};
const ST=Object.assign({},DEFAULTS);
function simReset(){}                             /* nothing here runs on a clock */

/* ---- actions: every change goes through PhET's rules -------------------------
   The charges have a fixed radius, so a new charge never pushes anything:
   only dragging meets the no-overlap rule. */
function setCharge(st,w,k,v){ st[PRE[w]+'q'+k]=clamp(Math.round(v),-Q_MAX,Q_MAX); }
function setPosCL(st,w,k,x){
  const p=PRE[w], T=TRACKS[w];
  st[p+'i'+k]=dragSteps(T,k,x,st[p+'i1'],st[p+'i2'],chargeSteps(T));
}
function setRulerCL(st,w,x0,y){
  const p=PRE[w], T=TRACKS[w];
  st[p+'RulerI']=clamp(symRound(x0*T.perM),T.iL-(T.iR-T.iL)/2,T.iR);
  if(y!==undefined) st[p+'RulerY']=y;
}
function rulerHomeCL(st,w){ st[PRE[w]+'RulerI']=TRACKS[w].iL; st[PRE[w]+'RulerY']=null; }
function rulerToQ1(st,w){ st[PRE[w]+'RulerI']=st[PRE[w]+'i1']; st[PRE[w]+'RulerY']=0; }

/* ---- the models ---------------------------------------------------------------- */
function qText(q,w){ const s=q>0?'+':(q<0?'−':''); return w==='macro'?s+Math.abs(q)+' µC':s+Math.abs(q)+'e'; }
function screenModel(st,w){
  const p=PRE[w], T=TRACKS[w], n=chargeSteps(T);
  const Q1=st[p+'q1'], Q2=st[p+'q2'], i1=st[p+'i1'], i2=st[p+'i2'];
  const q1=Q1*T.qSI, q2=Q2*T.qSI, x1=posOf(T,i1), x2=posOf(T,i2), r=(i2-i1)/T.perM;
  const F1=forceOn(T.C,q1,q2,x1,x2,1), F2=forceOn(T.C,q1,q2,x1,x2,2), Fmag=forceMag(T.C,q1,q2,r);
  const mode=st[p+'Force']?(st[p+'Sci']?'sci':'dec'):'hid';
  const kind=Q1*Q2<0?'attract':(Q1*Q2>0?'repel':'none');
  /* what PhET's own constants would print: its k, and on the atomic screen its e */
  const eP=w==='macro'?1e-6:E_PHET, Fphet=Math.abs(K_PHET*Q1*eP*Q2*eP)/(r*r);
  return {w,T,Q1,Q2,q1,q2,i1,i2,x1,x2,r,n,dmin:n/T.perM,gap:r-2*T.R,F1,F2,Fmag,kq:T.C*q1*q2,kind,mode,Fphet,
          rulerI:st[p+'RulerI'],rulerY:st[p+'RulerY'],arrowK:st[p+'ArrowK'],per:arrowStep(st[p+'ArrowK'],ARROW_E0[w]),
          acc:Fmag/M_P,
          lab1:forceLabel('q₁','q₂',F1,mode,T.places),lab2:forceLabel('q₂','q₁',F2,mode,T.places)};
}
function invModel(L){ return invSample(L.T.C,L.q1,L.q2,L.r,2*L.T.R,L.dmin,(L.T.iR-L.T.iL)/L.T.perM); }
/* the charge product: |F| contours over the (q1, q2) plane in the screen's own
   charge units, and the two straight lines — F on q2 as q2 changes sign, and
   the force against the product itself */
function prodModel(L){
  const T=L.T, ku=K_E*T.qSI*T.qSI/(L.r*L.r), levels=[];
  const Flo=ku*1, Fhi=ku*Q_MAX*Q_MAX;
  for(let e=Math.floor(Math.log10(Flo));e<=Math.ceil(Math.log10(Fhi));e++)
    for(const c of [1,2,5]){ const F=c*Math.pow(10,e); if(F>Flo*1.0001&&F<Fhi*0.9999) levels.push(F); }
  const contours=levels.map(F=>{ const c=F/ku, a=c/Q_MAX, xs=[], ys=[];
    for(let i=0;i<=60;i++){ const x=a*Math.pow(Q_MAX/a,i/60); xs.push(x); ys.push(c/x); }
    return {F,c,xs,ys,decade:Math.abs(Math.log10(F)-Math.round(Math.log10(F)))<1e-9}; });
  const q2s=[], F2s=[], F1s=[];
  for(let i=0;i<=40;i++){ const Q=-Q_MAX+2*Q_MAX*i/40; q2s.push(Q);
    F2s.push(forceOn(T.C,L.q1,Q*T.qSI,L.x1,L.x2,2)); F1s.push(forceOn(T.C,L.q1,Q*T.qSI,L.x1,L.x2,1)); }
  const ps=[], Fps=[];
  for(let i=0;i<=40;i++){ const pr=-Q_MAX*Q_MAX+2*Q_MAX*Q_MAX*i/40; ps.push(pr); Fps.push(forceOn(T.C,pr*T.qSI,T.qSI,L.x1,L.x2,2)); }
  const cl=Math.abs(L.Q1*L.Q2), live={c:cl,xs:[],ys:[]};
  if(cl>0) for(let i=0;i<=60;i++){ const x=cl/Q_MAX*Math.pow(Q_MAX*Q_MAX/cl,i/60); live.xs.push(x); live.ys.push(cl/x); }
  return {ku,levels,contours,q2s,F2s,F1s,ps,Fps,live,prod:L.Q1*L.Q2,dFdq2:ku*L.Q1};
}
/* electricity against gravity: the hydrogen pair on log-log axes, the ratios,
   and the masses that would pull as hard as the macro charges */
function gravModel(La,Lm){
  const rs=[], Fe=[], Fg=[], Fa=[];
  for(let i=0;i<=90;i++){ const r=Math.pow(10,-15+15*i/90); rs.push(r);
    Fe.push(forceMag(K_E,E_CH,E_CH,r)); Fg.push(forceMag(G_N,M_E,M_P,r)); Fa.push(forceMag(K_E,La.q1,La.q2,r)); }
  const ps=[], ms=[];
  for(let i=0;i<=50;i++){ const pr=Q_MAX*Q_MAX*i/50; ps.push(pr); ms.push(equalMass(Math.sqrt(pr)*1e-6,Math.sqrt(pr)*1e-6)); }
  const mEq=equalMass(Lm.q1,Lm.q2), V=4/3*PI*Math.pow(TRACKS.macro.R,3);
  return {rs,Fe,Fg,Fa,ratioEP:ratioEG(M_E,M_P),ratioPP:ratioEG(M_P,M_P),ratioEE:ratioEG(M_E,M_E),
          FeA0:forceMag(K_E,E_CH,E_CH,A0),FgA0:forceMag(G_N,M_E,M_P,A0),ps,ms,mEq,rhoEq:mEq/V,prodM:Math.abs(Lm.Q1*Lm.Q2),
          ra:La.r,Fa0:La.Fmag};
}

function buildModel(){
  const st=ST, view=st.view, M={view,st};
  if(view==='macro'||view==='atomic') M.L=screenModel(st,view);
  else if(view==='inv'||view==='prod'){ M.L=screenModel(st,st.scale); if(view==='inv') M.I=invModel(M.L); else M.P=prodModel(M.L); }
  else { M.La=screenModel(st,'atomic'); M.Lm=screenModel(st,'macro'); M.E=gravModel(M.La,M.Lm); }
  return M;
}

/* ---- the shared lab drawing reads a descriptor, not the state ---- */
function chargeFill(Q){ if(Q===0) return COL.zero; return mix(COL.bg,Q>0?COL.plus:COL.minus,0.35+0.65*Math.abs(Q)/Q_MAX); }
function chargeRim(Q){ return Q===0?COL.dim:(Q>0?COL.plus:COL.minus); }
function labSpec(M){
  const L=M.L, T=L.T, u=T.uPerM, st=M.st, macro=L.w==='macro';
  return {capFull:macro?MACRO_CAP_FULL:ATOMIC_CAP_FULL,capShort:macro?MACRO_CAP_SHORT:ATOMIC_CAP_SHORT,
    xL:T.iL/T.perM*u,xR:T.iR/T.perM*u,rmax:T.R*u,pad:macro?0.2:2,unit:T.unit,
    bodies:[{x:L.x1*u,r:T.R*u,fill:chargeFill(L.Q1),rim:chargeRim(L.Q1),name:'q₁',sub:qText(L.Q1,L.w),sign:L.Q1>0?'+':(L.Q1<0?'−':'')},
            {x:L.x2*u,r:T.R*u,fill:chargeFill(L.Q2),rim:chargeRim(L.Q2),name:'q₂',sub:qText(L.Q2,L.w),sign:L.Q2>0?'+':(L.Q2<0?'−':'')}],
    F:[L.F1,L.F2],per:L.per,labels:[L.lab1,L.lab2],
    arrowText:'force arrows: 1 '+T.unit+' of arrow = '+sciPlain(L.per,1)+' N',
    showDist:st.showDist,distText:'r = '+fmt(L.r*u,macro?1:0)+' '+T.unit+' between centres',
    ruler:{x0:L.rulerI/T.perM*u,y:L.rulerY,len:(T.iR-T.iL)/T.perM*u,major:macro?1:10,minorPer:5,
           labels:macro?['0','1','2','3','4','5','6','7','8','9','10']:['0','10','20','30','40','50','60','70','80','90','100'],
           unit:macro?'centimetres':'picometres'},
    legend:macro?{len:1,text:'1 cm'}:{len:10,text:'10 pm',note:'1 picometre (pm) = 1 × 10⁻¹² m'},dimRow:true};
}
function invSpec(M){
  const L=M.L, T=L.T;
  return {I:M.I,r:L.r,F:L.Fmag,unit:T.unit,uPerM:T.uPerM,
          pair:'q₁ = '+qText(L.Q1,L.w)+', q₂ = '+qText(L.Q2,L.w)+(L.kind==='none'?', no force':(L.kind==='attract'?', attracting':', repelling')),
          gapText:'PhET’s gap',capFull:INV_CAP_FULL,capShort:INV_CAP_SHORT,prodName:'|k q₁q₂|'};
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function fN(x){ return sciHTML(x,4)+' N'; }
function qHTML(Q,w){ return (Q>0?'+':(Q<0?'&minus;':''))+Math.abs(Q)+(w==='macro'?' &micro;C':'e'); }
function lenHTML(x,T){ return sigf(x*T.uPerM,3)+' '+T.unit; }
/* the surface gap reads better one unit down: 0.50 mm, 0.10 pm */
function gapHTML(g,T){ return T.unit==='cm'?sigf(g*1000,2)+' mm':sigf(g*1e12,2)+' pm'; }
function screenRows(L){
  const T=L.T, u=T.uPerM;
  let s=hd(L.w==='macro'?'macro scale':'atomic scale')+rrow('q<sub>1</sub>, q<sub>2</sub>',qHTML(L.Q1,L.w)+', '+qHTML(L.Q2,L.w))
    +rrow('radius of each (PhET&rsquo;s)',lenHTML(T.R,T));
  s+=hd('the distance')+rrow('between centres, r',fmt(L.r*u,L.w==='macro'?1:0)+' '+T.unit,'good')+rrow('between surfaces',lenHTML(L.gap,T))
    +rrow('closest PhET allows',lenHTML(L.dmin,T)+' (a '+gapHTML(L.dmin-2*T.R,T)+' gap)');
  s+=hd('the force')+rrow('|F| = k|q<sub>1</sub>q<sub>2</sub>|/r<sup>2</sup>',fN(L.Fmag),'good')
    +rrow('on q<sub>1</sub>, on q<sub>2</sub> (along +x)',sciHTML(L.F1,4)+', '+sciHTML(L.F2,4))
    +rrow('the pair',L.kind==='none'?'no force: a charge is zero':(L.kind==='attract'?'attract (unlike signs)':'repel (like signs)'),L.kind==='none'?'bad':'')
    +rrow('k q<sub>1</sub>q<sub>2</sub>',sciHTML(L.kq,4)+' N m&sup2;');
  return s;
}
function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">coulomb&rsquo;s law<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='macro'||M.view==='atomic'){
    const L=M.L;
    s+=screenRows(L);
    if(L.w==='atomic') s+=rrow('on a proton, that is',sciHTML(L.acc,3)+' m/s&sup2;');
    s+=hd('the drawing')+rrow('arrow scale',sciHTML(L.per,1)+' N per '+L.T.unit)+rrow('ruler zero at',fmt(L.rulerI/L.T.perM*L.T.uPerM,L.w==='macro'?1:0)+' '+L.T.unit);
  }
  else if(M.view==='inv'){
    const L=M.L, I=M.I;
    s+=screenRows(L);
    s+=hd('the law')+rrow('|F| at 2r',fN(I.F2r))+rrow('F(r) / F(2r)',fmt(L.Fmag/I.F2r,6),'good')+rrow('log-log slope at r',fmt(I.slope,6),'good')
      +rrow('reachable r',lenHTML(I.dmin,L.T)+' &ndash; '+lenHTML(I.rTrack,L.T));
  }
  else if(M.view==='prod'){
    const L=M.L, P=M.P, un=L.w==='macro'?'&micro;C':'e';
    s+=screenRows(L);
    s+=hd('the product')+rrow('q<sub>1</sub>q<sub>2</sub>',P.prod+' '+un+'&sup2;',P.prod<0?'':'good')
      +rrow('|F| per '+un+'&sup2; of product',fN(P.ku))+rrow('dF<sub>2</sub>/dq<sub>2</sub>, per '+un,fN(P.dFdq2));
  }
  else {
    const E=M.E;
    s+=hd('electron and proton, any distance')+rrow('k e<sup>2</sup> / (G m<sub>e</sub>m<sub>p</sub>)',sciHTML(E.ratioEP,4),'good')
      +rrow('at the Bohr radius: electric',fN(E.FeA0))+rrow('gravitational',fN(E.FgA0))
      +rrow('two protons: k e<sup>2</sup>/(G m<sub>p</sub><sup>2</sup>)',sciHTML(E.ratioPP,4))+rrow('two electrons',sciHTML(E.ratioEE,4));
    s+=hd('the macro charges as masses')+rrow('|q<sub>1</sub>q<sub>2</sub>|',E.prodM+' &micro;C&sup2;')
      +rrow('equal masses pulling as hard',E.prodM>0?sigf(E.mEq/1000,3)+' tonnes each':'none needed (no force)','good')
      +rrow('in a 6.75-mm sphere, a density of',E.prodM>0?sciHTML(E.rhoEq,3)+' kg/m&sup3;':'&mdash;');
  }
  s+='</table><div class="note">k = 1/4&pi;&epsilon;<sub>0</sub> = 8.98755 &times; 10<sup>9</sup> N m&sup2; C<sup>&minus;2</sup> (CODATA 2022 &epsilon;<sub>0</sub>); '
    +'e = 1.602176634 &times; 10<sup>&minus;19</sup> C, exact. PhET uses k = 8.987551 &times; 10<sup>9</sup> and e = 1.6021766208 &times; 10<sup>&minus;19</sup>'
    +(M.L?', so its readout here would say '+sciHTML(M.L.Fphet,7)+' N':'')+'. Everything is pinned in selfTest to derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='macro'||M.view==='atomic') return E('<span class="hl">F = k q<sub>1</sub>q<sub>2</sub> / r<sup>2</sup></span> &nbsp;&middot;&nbsp; k = 1/4&pi;&epsilon;<sub>0</sub> = 8.988 &times; 10<sup>9</sup> N m<sup>2</sup> C<sup>&minus;2</sup> &nbsp;&middot;&nbsp; F<sub>on 1</sub> = &minus;F<sub>on 2</sub>',
    'Coulomb’s law: like charges repel, unlike charges attract, and the force falls as the square of the distance between centres');
  if(M.view==='inv') return E('|F| &prop; 1/r<sup>2</sup> &nbsp;&middot;&nbsp; log|F| = log|k q<sub>1</sub>q<sub>2</sub>| &minus; 2 log r &nbsp;&middot;&nbsp; <span class="hl">|F| r<sup>2</sup> = |k q<sub>1</sub>q<sub>2</sub>|</span>',
    'double the distance and the force falls to a quarter, on either scale: on log–log axes a straight line of slope −2');
  if(M.view==='prod') return E('<span class="hl">F = (k / r<sup>2</sup>) q<sub>1</sub>q<sub>2</sub></span> &nbsp;&middot;&nbsp; q<sub>1</sub>q<sub>2</sub> &gt; 0: repel &nbsp;&middot;&nbsp; q<sub>1</sub>q<sub>2</sub> &lt; 0: attract',
    'only the product of the charges matters: its sign is the direction, its size the strength');
  return E('<span class="hl">F<sub>e</sub> / F<sub>g</sub> = k e<sup>2</sup> / (G m<sub>e</sub> m<sub>p</sub>) = 2.27 &times; 10<sup>39</sup></span> &nbsp;&middot;&nbsp; m<sub>equal</sub> = &radic;(k|q<sub>1</sub>q<sub>2</sub>| / G)',
    'both forces fall as 1/r², so their ratio is the same at every distance — and it is enormous');
}
function tagHTML(M){
  if(M.view==='grav') return '<b>electricity and gravity</b> — the hydrogen pair, and the macro charges as masses';
  const L=M.L;
  return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b> — q₁ '+qText(L.Q1,L.w)+', q₂ '+qText(L.Q2,L.w)+', r = '+fmt(L.r*L.T.uPerM,L.w==='macro'?1:0)+' '+L.T.unit
    +(M.view==='inv'||M.view==='prod'?' ('+L.w+')':'');
}
