
/* ================================================================== *
 *  THE BORN RULE view: the half-angle, a middle measurement, a chain  *
 * ================================================================== */
const BORN_ANG=[0,15,30,45,60,75,90,105,120,135,150,165,180];
const CHAIN_NS=[1,2,3,4,6,8,12,16,24,32,48,64];
/* seeded counts through the SAME measurement functions the other views run:
   the spin through measureAlong, the photon through photonDecide */
function bornPoints(shots,seed){
  return memo('bornPts',shots+':'+seed,()=>BORN_ANG.map((a,i)=>{
    const us=bornSpinMC(seed+i,a,shots), hp=a<=90?bornPhotonMC(seed+100+i,a,shots):null;
    return {a, spin:us/shots, photon:hp===null?null:hp/shots, sdS:Math.sqrt(bornSpin(a)*(1-bornSpin(a))/shots), sdP:a<=90?Math.sqrt(bornPhoton(a)*(1-bornPhoton(a))/shots):null};
  }));
}
function bornChi2(pts,shots){
  /* each point against its law, in units of its own binomial sd; points whose
     law is exactly 0 or 1 carry no variance and are checked for exactness */
  let chi=0, dof=0, exact=true;
  for(const p of pts){
    const ls=bornSpin(p.a);
    if(p.sdS>1e-12){ chi+=Math.pow((p.spin-ls)/p.sdS,2); dof++; } else if(Math.abs(p.spin-ls)>1e-12) exact=false;
    if(p.photon!==null){ const lp=bornPhoton(p.a); if(p.sdP>1e-12){ chi+=Math.pow((p.photon-lp)/p.sdP,2); dof++; } else if(Math.abs(p.photon-lp)>1e-12) exact=false; }
  }
  return {chi,dof,exact};
}
function chainPoints(shots,seed){ return memo('chainPts',shots+':'+seed,()=>CHAIN_NS.map((N,i)=>({N,T:chainMC(seed+i,N,shots)/shots,sd:Math.sqrt(chainT(N)*(1-chainT(N))/shots)}))); }
function bornModel(st){
  const m={th:st.bornTh, al:st.bornAlpha, N:st.bornN, shots:st.bornShots, seed:st.bornSeed};
  m.pSpin=bornSpin(m.th); m.pPhoton=bornPhoton(m.th);
  m.pts=bornPoints(m.shots,m.seed); m.fit=bornChi2(m.pts,m.shots);
  m.midSpin=middleSpin(m.al); m.midPhoton=middlePhoton(m.al);
  m.T=chainT(m.N); m.Tasym=1-Math.PI*Math.PI/(4*m.N);
  m.chain=chainPoints(Math.min(m.shots,4000),m.seed+500);
  return m;
}
function bornGeo(ctx,W,H,Cap){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?50:66;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(140,Math.min(narrow?220:330,avail*0.56));
  const wA=narrow?(rightTop-left)*0.55:Math.min(540,(rightTop-left)*0.56);
  const A=box(left,top+12,wA,upH-40);
  const B=box(A.x1+(narrow?46:70),top+12,Math.max(100,rightTop-(A.x1+(narrow?46:70))),upH-40);
  /* no floor: the chain panel is skipped when it does not fit */
  const lowTop=top+upH+30, C=box(left,lowTop,Math.min(narrow?W-18-left:720,(narrow?W-18:W-26)-left),fit.capY-16-lowTop-26);
  return {narrow,top,left,fit,A,B,C};
}
/* chain: whether the chain panel is drawn (the caption names it only then) */
function bornCaption(M,chain){
  const m=M.O;
  return {full:'Left: a spin measured at an angle Θ from its state passes with cos²(Θ/2); a photon at θ from the analyser with cos²θ. Points: '+m.shots+' seeded shots per angle through the same code the other views run, ±1σ binomial bars; χ² = '+fmt(m.fit.chi,1)+' on '+m.fit.dof+'. Right: a middle measurement lets through what two crossed ones stop.'+(chain!==false?' Below: N magnets turning from up to down in equal steps each pass cos²(π/2N), and the chain, their product, climbs to 1.':''),
          short:'Spin cos²(Θ/2) against photon cos²θ; the middle measurement'+(chain!==false?'; the chain → 1.':'.')};
}
/* the caption and the geometry together: the chain panel is optional */
function bornLayout(ctx,W,H,M){ return layoutNamed(c=>bornCaption(M,c),Cap=>bornGeo(ctx,W,H,Cap),G=>G.C.h>=55); }
function drawBorn(ctx,W,H,M){
  const m=M.O, LY=bornLayout(ctx,W,H,M), Cap=LY.Cap, G=LY.G, A=G.A, B=G.B, C=G.C;
  /* the half-angle */
  axesT(ctx,A,0,180,0,1.02,{xticks:[0,30,60,90,120,150,180],yticks:[0,0.25,0.5,0.75,1],xlab:'angle between the state and the measurement (°)',
    title:fitTitle(A,'the half-angle: a spin cos²(Θ/2), a photon cos²θ','spin against photon')});
  const xs=[], ys=[], yp=[]; for(let a=0;a<=180;a++){ xs.push(a); ys.push(bornSpin(a)); yp.push(a<=90?bornPhoton(a):NaN); }
  polyline(ctx,A,xs,ys,0,180,0,1.02,COL.ref,2.2); polyline(ctx,A,xs,yp,0,180,0,1.02,COL.ref,1.6,[6,4]);
  for(const p of m.pts){ errBar(ctx,A,p.a,p.spin,p.sdS,0,180,0,1.02,COL.pos); mark(ctx,px(A,p.a,0,180),clamp(py(A,p.spin,0,1.02),A.y,A.y1),'o',COL.pos,3.6);
    if(p.photon!==null){ errBar(ctx,A,p.a,p.photon,p.sdP,0,180,0,1.02,COL.neg); mark(ctx,px(A,p.a,0,180),clamp(py(A,p.photon,0,1.02),A.y,A.y1),'d',COL.neg,3.4); } }
  vCursor(ctx,A,m.th,0,180);
  mark(ctx,px(A,m.th,0,180),py(A,m.pSpin,0,1.02),'o',COL.live,4.5);
  if(m.th<=90) mark(ctx,px(A,m.th,0,180),py(A,m.pPhoton,0,1.02),'d',COL.live,4.5);
  legendAuto(ctx,A,[[COL.ref,'cos²(Θ/2), spin (solid)'],[mix(COL.bg,COL.ref,0.75),'cos²θ, photon (dashed)'],[COL.pos,'spins, seeded'],[COL.neg,'photons, seeded (diamonds)']]);
  /* the middle measurement (to 0.4: the curves peak at 1/4, and the legend needs the headroom -- at 0.3 it found no spot at 1100 x 700 and vanished) */
  axesT(ctx,B,0,180,0,0.4,{xticks:[0,45,90,135,180],yticks:[0,0.1,0.2,0.3,0.4],xlab:'the middle one’s angle α (°)',
    title:fitTitle(B,'a middle measurement: z → α → −z, H → α → V','the middle measurement')});
  const ms=[], mp=[]; for(let a=0;a<=180;a++){ ms.push(middleSpin(a)); mp.push(middlePhoton(a)); }
  polyline(ctx,B,xs,ms,0,180,0,0.4,COL.ref,2.2); polyline(ctx,B,xs,mp,0,180,0,0.4,COL.ref,1.6,[6,4]);
  vCursor(ctx,B,m.al,0,180); mark(ctx,px(B,m.al,0,180),py(B,m.midSpin,0,0.4),'o',COL.live,4.2); mark(ctx,px(B,m.al,0,180),py(B,m.midPhoton,0,0.4),'d',COL.live,4);
  legendAuto(ctx,B,[[COL.ref,'spins: ¼ sin²α (solid)'],[mix(COL.bg,COL.ref,0.75),'photons: ¼ sin²2α (dashed)']]);
  /* the chain of N magnets */
  if(!G.panelOff&&C.h>=55){
    axesT(ctx,C,0,64,0,1.05,{xticks:[0,8,16,24,32,40,48,56,64],yticks:C.h<100?[0,1]:[0,0.25,0.5,0.75,1],xlab:C.h>=95?'N, magnets from +z to −z in equal steps':''});
    /* the title carries a real superscript, so it is rich text, registered */
    rich(ctx,C.x,C.y-9,C.w>=430?[['a chain of N magnets drags a spin from up to down: [cos²(π/2N)]',null],['N','sup'],[' → 1',null]]
                              :[['the chain: [cos²(π/2N)]',null],['N','sup']],13,'#aeb6c6','left',true);
    const cx=[], cy=[], ca=[]; for(let N=1;N<=64;N+=0.25){ cx.push(N); cy.push(Math.pow(Math.cos(Math.PI/(2*N)),2*N)); ca.push(1-Math.PI*Math.PI/(4*N)); }
    polyline(ctx,C,cx,cy,0,64,0,1.05,COL.ref,2.2); polyline(ctx,C,cx,ca,0,64,0,1.05,COL.faint,1.3,[4,4]);
    for(const p of m.chain){ errBar(ctx,C,p.N,p.T,p.sd,0,64,0,1.05,COL.pos); mark(ctx,px(C,p.N,0,64),clamp(py(C,p.T,0,1.05),C.y,C.y1),'o',COL.pos,3.4); }
    vCursor(ctx,C,m.N,0,64); mark(ctx,px(C,m.N,0,64),py(C,m.T,0,1.05),'o',COL.live,4.2);
    legendAuto(ctx,C,[[COL.ref,'the chain, exact'],[COL.faint,'1 − π²/4N (dashed)'],[COL.pos,'seeded chains ± 1σ']]);
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function bornReadout(M){
  const m=M.O;
  return hd('at &Theta; = '+fmt(m.th,0)+'&deg;')+rrow('spin: cos&sup2;(&Theta;/2)',fmt(m.pSpin,4),'good')+rrow('photon: cos&sup2;&Theta;',m.th<=90?fmt(m.pPhoton,4):'&mdash; (past 90&deg;)')
    +hd('the seeded points')+rrow('shots per angle',String(m.shots))+rrow('&chi;&sup2; / points',fmt(m.fit.chi,2)+' / '+m.fit.dof,m.fit.chi<3*m.fit.dof?'good':'bad')
    +rrow('the certain ones (0, 1)',m.fit.exact?'exact':'NOT exact',m.fit.exact?'good':'bad')
    +hd('a middle measurement at &alpha; = '+fmt(m.al,0)+'&deg;')+rrow('spins z &rarr; &alpha; &rarr; &minus;z: &frac14;sin&sup2;&alpha;',fmt(m.midSpin,4))+rrow('photons H &rarr; &alpha; &rarr; V: &frac14;sin&sup2;2&alpha;',fmt(m.midPhoton,4))
    +rrow('without it',fmt(0,0)+' (crossed)')
    +hd('a chain of N = '+m.N)+rrow('cos<sup>2N</sup>(&pi;/2N)',fmt(m.T,4),'good')+rrow('1 &minus; &pi;&sup2;/4N',fmt(m.Tasym,4));
}
function bornEq(M){ return ['<span class="hl">P = cos&sup2;(&Theta;/2)</span> <span class="rm">(spin)</span>, &nbsp; <span class="hl">cos&sup2;&theta;</span> <span class="rm">(photon)</span> &nbsp;&middot;&nbsp; P(z&rarr;&alpha;&rarr;&minus;z) = &frac14;sin&sup2;&alpha; &nbsp;&middot;&nbsp; T<sub>N</sub> = cos<sup>2N</sup>(&pi;/2N) &rarr; 1',
  'a spin needs twice the angle a photon does, and measurement in sequence multiplies: enough small steps drag a state anywhere']; }
function bornTag(M){ return '<b>the Born rule</b> — Θ = '+fmt(M.O.th,0)+'°, α = '+fmt(M.O.al,0)+'°, N = '+M.O.N; }
const INFO_BORN='Both of PhET&rsquo;s measuring devices obey the Born rule, but with different angles. A spin-&frac12; state whose Bloch vector is &Theta; away from a '
  +'magnet&rsquo;s axis passes with cos&sup2;(&Theta;/2); a photon polarized &theta; away from an analyser passes with cos&sup2;&theta;. The factor of two is '
  +'the whole difference between the Bloch sphere and a polariser: opposite spins are 180&deg; apart, crossed polarisations only 90&deg;. The points '
  +'are seeded counts through exactly the code the spins and photons views run, with binomial error bars, and a &chi;&sup2; that should be near the '
  +'number of points. Measurement in sequence multiplies: two crossed filters pass nothing, but a third between them lets a quarter through at '
  +'its best angle &mdash; 90&deg; for spins, 45&deg; for photons. Divide the turn from up to down into N small steps and the chain passes '
  +'cos<sup>2N</sup>(&pi;/2N), which climbs to 1 as 1 &minus; &pi;&sup2;/4N: enough measurements drag a state wherever you like.';
const DERIV_BORN='<h4>the half-angle and the chain</h4>'
  +EQ(1,'<span class="rm">spin:</span> |&lang;&uarr;<sub>n</sub>|&psi;&rang;|&sup2; = cos&sup2;(&Theta;/2), &nbsp; <span class="rm">photon:</span> |&lang;H|&theta;&rang;|&sup2; = cos&sup2;&theta;')
  +EQ(2,'P(z&rarr;&alpha;&rarr;&minus;z) = cos&sup2;(&alpha;/2) sin&sup2;(&alpha;/2) = &frac14;sin&sup2;&alpha;')
  +EQ(3,'P(H&rarr;&alpha;&rarr;V) = cos&sup2;&alpha; sin&sup2;&alpha; = &frac14;sin&sup2;2&alpha;')
  +EQ(4,'T<sub>N</sub> = [cos&sup2;(&pi;/2N)]<sup>N</sup> = 1 &minus; '+FR('&pi;&sup2;','4N')+' + O(N<sup>&minus;2</sup>)')
  +'<p>T<sub>1</sub> = 0 (one magnet straight to &minus;z passes nothing) and T<sub>2</sub> = &frac14; (a middle magnet along x). The approach to 1 is '
  +'O(1/N): (1 &minus; T<sub>100</sub>)/(1 &minus; T<sub>1000</sub>) = 9.89, and (1 &minus; T<sub>1000</sub>) &times; 4000/&pi;&sup2; = 0.9988.</p>'
  +'<div class="cite">pins: T<sub>N</sub> at nine N, the middle laws at five angles, and the seeded runs (a chain of 8: 3682 of 5000; the middle '
  +'magnet at 60&deg;: 955, the middle polariser: 928; spins at 60&deg;: 1467 of 2000, photons: 478) &mdash; derive.py</div>';
