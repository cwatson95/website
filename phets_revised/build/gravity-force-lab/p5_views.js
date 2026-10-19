
/* ================================================================== *
 *  captions                                                           *
 * ================================================================== */
const LAB_CAP_FULL='Two uniform spheres on a frictionless track: PhET’s lab. Drag either sphere, or the ruler; the sliders set the masses '
  +'and the positions. The green arrows are the force on each sphere — always the same size, always opposite — drawn to the arrow scale '
  +'printed below, and the labels read it in PhET’s decimal or scientific notation. Positions snap to PhET’s 0.1-m grid, and the centres '
  +'never come closer than the two radii plus about 0.1 m, so the spheres never touch.';
const LAB_CAP_SHORT='Drag the spheres or the ruler. Green: the force on each, equal and opposite, to the printed arrow scale.';
const INV_CAP_FULL='The force between the spheres against the distance between their centres, at the current masses. On log–log axes an '
  +'inverse-square law is a straight line of slope −2; the solid part is what PhET’s track allows, the orange band the distances at which '
  +'the spheres would overlap, the paler band PhET’s gap between surfaces. Lower left: the same force on linear axes. Lower right: F r², '
  +'which an inverse-square law keeps flat at G m₁m₂ — the dashed curve is what an inverse-cube law through the same point would do.';
const INV_CAP_SHORT='F against r: slope −2 on log–log axes; F r² stays flat at G m₁m₂.';
const PROD_CAP_FULL='Every pair of masses at the current distance: F = (G/r²) m₁m₂, so each contour — one force — is a hyperbola '
  +'m₁m₂ = F r²/G. The magenta dot is the live pair and the magenta curve the pairs that feel the same force; where the spheres would be '
  +'too big to sit this far apart the plane is shaded. Lower left: the force against one mass with the other held — straight lines through '
  +'the origin. Lower right: the strongest pull two equal masses can reach, at their closest allowed distance: m² for constant-size spheres, '
  +'about m^(4/3) for real ones, because the heavier sphere is also the bigger one.';
const PROD_CAP_SHORT='F over (m₁, m₂): hyperbolas m₁m₂ = F r²/G. Below: F linear in each mass, and the strongest reachable pull.';
const FALL_CAP_FULL='What the lab’s forces would do if the track let go: released from rest, the spheres fall together. Their momenta stay '
  +'equal and opposite, so the centre of mass (cyan) never moves and the lighter sphere covers more of the gap; the dashed circles are where '
  +'they started. Green arrows are the forces, magenta the velocities, each to its own printed scale, fixed for the run so both grow as the '
  +'spheres close. The separation follows the exact free-fall law and the run stops at contact, where the model ends. Lower left: both '
  +'positions and the centre of mass against time. Lower right: the separation.';
const FALL_CAP_SHORT='Released from rest: the centre of mass stays put and the lighter sphere moves more; they touch at the printed time.';

/* ================================================================== *
 *  view: the mass product                                             *
 * ================================================================== */
function drawProd(ctx,W,H,M){
  const L=M.L, P=M.P;
  const Lo=stageLayoutH(ctx,W,H,PROD_CAP_FULL,PROD_CAP_SHORT,2,0.36,1);
  const b=Lo.main, mx=M_MAX;
  const px=m=>b.x+b.w*m/mx, py=m=>b.y1-b.h*m/mx;
  /* the pairs too big to sit r apart: one batched fill of column rectangles */
  if(P.nBlocked>0){
    ctx.beginPath();
    P.edge.forEach((e,i)=>{ if(e===null) return; const m1=M_MIN+i*M_STEP;
      const x0=px(Math.max(0,m1-M_STEP/2)), x1=px(Math.min(mx,m1+M_STEP/2)), y0=py(mx), y1=py(Math.max(0,e-M_STEP/2));
      ctx.rect(x0,y0,x1-x0,y1-y0); });
    ctx.fillStyle='rgba(232,132,58,0.16)'; ctx.fill();
  }
  /* PhET's masses start at 10 kg: the strips below are out of reach */
  ctx.fillStyle='rgba(139,147,166,0.10)';
  ctx.fillRect(b.x,b.y,px(M_MIN)-b.x,b.h); ctx.fillRect(b.x,py(M_MIN),b.w,b.y1-py(M_MIN));
  axesT(ctx,b,0,mx,0,mx,{title:titleFor(b,'the force over every pair of masses at r = '+fmt(L.r,1)+' m: hyperbolas m₁m₂ = F r²/G','F over (m₁, m₂)'),
    xlab:'m₁, kg',ylab:'m₂, kg',nx:5,ny:5,xfmt:v=>fmt(v,0),yfmt:v=>fmt(v,0)});
  for(const C of P.contours)
    polyline(ctx,b,C.m1s,C.m2s,0,mx,0,mx,C.decade?rgba(COL.pos,0.85):rgba(COL.pos,0.38),C.decade?1.5:1);
  for(const C of P.contours){ if(!C.decade) continue; const d=Math.sqrt(C.c);
    if(d>30&&d<mx*0.92) lab(ctx,W,H,px(d)+6,py(d)-6,sciPlain(C.F,1)+' N',COL.pos,SM_FONT,'left','bottom'); }
  polyline(ctx,b,P.live.m1s,P.live.m2s,0,mx,0,mx,COL.live,1.4,[5,4]);
  marker(ctx,b,0,mx,0,mx,L.m1,L.m2,COL.live);
  /* above the marker: the live hyperbola runs up-left and down-right of it,
     so the upper right is the one quadrant it never crosses */
  labBeside(ctx,W,H,b,px(L.m1),py(L.m2)-8,'F = '+sciPlain(L.Fmag,3)+' N',COL.live,'bottom');
  if(P.nBlocked>0) lab(ctx,W,H,b.x1-8,b.y+14,'shaded: too big to sit '+fmt(L.r,1)+' m apart ('+P.nBlocked+' of 10000 pairs)',COL.ref,SM_FONT,'right');
  const [bl,br]=lowerPanels(Lo);
  if(bl){
    /* the force against one mass, the other held: straight lines through the origin */
    const yh=Math.max(P.k*L.m2*mx,P.k*L.m1*mx)*1.08, ax=powAxis(yh,'F','N');
    axesT(ctx,bl,0,mx,0,yh,{title:titleFor(bl,'F against one mass, the other held: straight lines','F against one mass'),xlab:'the varied mass, kg',ylab:ax.lab,nx:5,ny:nyFor(bl.h),
      xfmt:v=>fmt(v,0),yfmt:ax.fmt});
    /* sampled finely although straight: the legend placer tests each segment's
       bounding box, and one segment's box would cover the whole panel */
    const mg=[], f1=[], f2=[]; for(let i=0;i<=50;i++){ const m=mx*i/50; mg.push(m); f1.push(P.k*L.m2*m); f2.push(P.k*L.m1*m); }
    polyline(ctx,bl,mg,f1,0,mx,0,yh,COL.b1,1.8);
    polyline(ctx,bl,mg,f2,0,mx,0,yh,COL.b2,1.8);
    marker(ctx,bl,0,mx,0,yh,L.m1,L.Fmag,COL.live); marker(ctx,bl,0,mx,0,yh,L.m2,L.Fmag,COL.live);
    legendAuto(ctx,bl,[[COL.b1,'m₁ varied, m₂ = '+fmt(L.m2,0)+' kg'],[COL.b2,'m₂ varied, m₁ = '+fmt(L.m1,0)+' kg']]);
  }
  if(br){
    /* the strongest pull of two equal masses: log-log, both size modes */
    const lo=Math.min(P.fsc[0],P.fcs[0]), hi=Math.max(P.fsc[P.fsc.length-1],P.fcs[P.fcs.length-1]);
    const X0=1, X1=3, Y0=Math.log10(lo)-0.2, Y1=Math.log10(hi)+0.2;
    axesT(ctx,br,X0,X1,Y0,Y1,{title:titleFor(br,'the strongest pull of two equal masses, log–log','strongest pull'),xlab:'m, kg',ylab:'F max, N',
      xticks:[1,Math.log10(20),Math.log10(50),2,Math.log10(200),Math.log10(500),3],yticks:logYTicks(Math.pow(10,Y0),Math.pow(10,Y1),br.h),xfmt:powLabel,yfmt:powLabel});
    const lx=P.ms.map(Math.log10);
    polyline(ctx,br,lx,P.fcs.map(Math.log10),X0,X1,Y0,Y1,COL.ref,1.6,[5,4]);
    polyline(ctx,br,lx,P.fsc.map(Math.log10),X0,X1,Y0,Y1,COL.pos,2);
    const mh=Math.max(L.m1,L.m2);
    marker(ctx,br,X0,X1,Y0,Y1,Math.log10(mh),Math.log10(P.FmaxHere),COL.live);
    legendAuto(ctx,br,[[COL.ref,'constant size: slope '+fmt(P.slopeCs,2)],[COL.pos,'real size: slope '+fmt(P.slopeSc,2)]]);
  }
  drawCaption(ctx,Lo);
}

/* ================================================================== *
 *  view: let them go                                                  *
 * ================================================================== */
function fallSpec(M,W,H){
  const F=M.Fa, fs=M.fs;
  const LS=labSpec(M);
  LS.capFull=FALL_CAP_FULL; LS.capShort=FALL_CAP_SHORT;
  LS.bodies[0].x=fs.x1; LS.bodies[1].x=fs.x2;
  LS.F=[fs.F1,fs.F2]; LS.per=M.perF;
  LS.labels=[forceLabel('m₁','m₂',fs.F1,'sci',12),forceLabel('m₂','m₁',fs.F2,'sci',12)];
  LS.arrowText='force arrows: 1 m = '+sciPlain(M.perF,1)+' N, velocity arrows (magenta): 1 m = '+sciPlain(M.perV,1)+' m/s';
  LS.ruler=null; LS.showDist=false; LS.dimRow=true; LS.extra=44;   /* the velocity row, its label, the clock line */
  LS.legend={len:1,text:'1 m'};
  LS.under=(ctx,G)=>{
    /* where they started (dashed), and the centre of mass, which never moves */
    [[F.x10,LS.bodies[0]],[F.x20,LS.bodies[1]]].forEach(([x,bd])=>{
      ctx.beginPath(); ctx.arc(G.X(x),G.yT,Math.max(1.5,bd.r*G.s),0,TAU); ctx.strokeStyle=rgba(bd.rim,0.45);
      ctx.lineWidth=1; ctx.setLineDash([4,4]); ctx.stroke(); ctx.setLineDash([]); });
    const Xc=G.X(F.xcm);
    ctx.strokeStyle=rgba(COL.struct,0.7); ctx.lineWidth=1; ctx.setLineDash([2,3]);
    ctx.beginPath(); ctx.moveTo(Xc,G.yT-G.s*LS.rmax); ctx.lineTo(Xc,G.yDim+12); ctx.stroke(); ctx.setLineDash([]);
  };
  LS.over=(ctx,G)=>{
    /* the centre-of-mass diamond goes OVER the bodies: it usually lies inside the heavier one */
    const Xc=G.X(F.xcm);
    ctx.beginPath(); ctx.moveTo(Xc,G.yT-6); ctx.lineTo(Xc+6,G.yT); ctx.lineTo(Xc,G.yT+6); ctx.lineTo(Xc-6,G.yT); ctx.closePath();
    ctx.fillStyle=COL.struct; ctx.fill(); ctx.strokeStyle='#070b18'; ctx.lineWidth=1; ctx.stroke();
    const yv=G.yDim+4;
    labArrow(ctx,G,fs.x1,fs.v1,M.perV,yv,COL.vel); labArrow(ctx,G,fs.x2,fs.v2,M.perV,yv,COL.vel);
    lab(ctx,W,H,G.X(F.xcm),G.yDim+22,'centre of mass',COL.struct,SM_FONT,'center','top');
  };
  return LS;
}
function drawFall(ctx,W,H,M){
  const F=M.Fa, fs=M.fs, C=M.Fc;
  /* narrow stage: the band alone — with a plot under it the band's fixed rows
     overflow a 157-px main box at 820 x 520 */
  const Lo=stageLayoutH(ctx,W,H,FALL_CAP_FULL,FALL_CAP_SHORT,2,0.36,0);
  const G=drawLab(ctx,W,H,fallSpec(M,W,H),Lo).G;
  const clock=M.run?(M.done?'touching after '+hms(F.tc):'t = '+hms(fs.t)+' of '+hms(F.tc)):'press "release": they would touch after '+hms(F.tc);
  lab(ctx,W,H,G.b.x+4,G.yDim+40,clock+'   ·   clock ×'+sigf(F.clock,3),M.done?COL.ref:COL.live,LAB_FONT,'left','top');
  const [bl,br]=lowerPanels(Lo), th=C.ts.map(t=>t/3600), T1=F.tc/3600, tn=fs.t/3600;
  if(bl){
    const ylo=Math.min(F.x10,F.x20)-0.3, yhi=Math.max(F.x10,F.x20)+0.3;
    axesT(ctx,bl,0,T1,ylo,yhi,{title:titleFor(bl,'the positions: the centre of mass never moves','positions'),xlab:'t, hours',ylab:'x, m',nx:5,ny:nyFor(bl.h),
      xfmt:tickNum,yfmt:tickNum});
    polyline(ctx,bl,[0,T1],[F.xcm,F.xcm],0,T1,ylo,yhi,COL.struct,1.2,[4,4]);
    polyline(ctx,bl,th,C.x1s,0,T1,ylo,yhi,COL.b1,1.8);
    polyline(ctx,bl,th,C.x2s,0,T1,ylo,yhi,COL.b2,1.8);
    polyline(ctx,bl,[tn,tn],[ylo,yhi],0,T1,ylo,yhi,rgba(COL.live,0.5),1);
    marker(ctx,bl,0,T1,ylo,yhi,tn,fs.x1,COL.live); marker(ctx,bl,0,T1,ylo,yhi,tn,fs.x2,COL.live);
    legendAuto(ctx,bl,[[COL.b1,'m₁, '+fmt(F.m1,0)+' kg'],[COL.b2,'m₂, '+fmt(F.m2,0)+' kg'],[COL.struct,'centre of mass']]);
  }
  if(br){
    const rhi=F.r0*1.08;
    axesT(ctx,br,0,T1,0,rhi,{title:titleFor(br,'the separation, to contact at r₁ + r₂ = '+sigf(F.rc,3)+' m','separation'),xlab:'t, hours',ylab:'r, m',nx:5,ny:nyFor(br.h),
      xfmt:tickNum,yfmt:tickNum});
    polyline(ctx,br,[0,T1],[F.rc,F.rc],0,T1,0,rhi,COL.ref,1.2,[4,4]);
    polyline(ctx,br,th,C.rs,0,T1,0,rhi,COL.pos,2);
    marker(ctx,br,0,T1,0,rhi,tn,fs.r,COL.live);
    lab(ctx,W,H,br.x+8,br.y1-br.h*(F.rc/rhi)-4,'contact',COL.ref,SM_FONT,'left','bottom');
  }
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='lab') drawLab(ctx,W,H,labSpec(M));
  else if(M.view==='inv') drawInverse(ctx,W,H,invSpec(M));
  else if(M.view==='prod') drawProd(ctx,W,H,M);
  else drawFall(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame: only a released fall moves anything (runStep carries the guard) */
  S.step=function(){ if(!ST.running||ST.view!=='fall') return false; return runStep(); };
  /* the step that reached contact: the readout must say so at once, not at the
     next tenth frame, which never comes because nothing advances after it */
  S.ended=function(){ return RUN.active&&RUN.frame>=FALL_FRAMES; };
  /* the pointer: the spheres and the ruler, in the lab only */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(ST.view!=='lab') return false;
    const ctx=canvas.getContext('2d'), LS=labSpec(buildModel()), G=labGeo(ctx,S.W,S.H,LS);
    if(type==='down'){
      const hit=labHit(G,LS,x,y);
      if(hit==='ruler'){ DRAG.what='ruler'; DRAG.off=G.wx(x)-LS.ruler.x0; DRAG.offY=y-G.ruler.y0; return true; }
      if(hit===1||hit===2){ DRAG.what=hit; DRAG.off=G.wx(x)-LS.bodies[hit-1].x; return true; }
      return false;
    }
    if(type==='move'){
      if(DRAG.what===1||DRAG.what===2){ setPos(ST,DRAG.what,G.wx(x)-DRAG.off); return true; }
      if(DRAG.what==='ruler'){ const y0=clamp(y-DRAG.offY,G.ruler.ryLo,G.ruler.ryHi); setRuler(ST,G.wx(x)-DRAG.off,G.wy(y0)); return true; }
    }
    return false;
  };
  return S;
}
