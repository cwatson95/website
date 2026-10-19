
/* ================================================================== *
 *  the six views                                                      *
 * ================================================================== */

/* the arrow scale: pixels per pN, chosen from 4 eps/sigma so an arrow at the
   bottom of the well is legible and the wall's arrows clip rather than fill
   the stage.  Printed on the canvas, always. */
function arrowScale(P,bw){
  const ref=pN(4*P.eps/P.sig);
  return Math.max(0.2,0.20*bw/Math.max(ref,1e-9));
}

/* ---------------- A. the two atoms (PhET's screen) ---------------- */
function drawAtoms(ctx,W,H,M){
  const P=M.P, L=M.L, st=M.st;
  reserveReadout(W,H);
  const G=atomsGeom(ctx,W,H,M);
  drawCaption(ctx,G.L);
  const band=G.band, gb=G.gb;

  /* the line the atoms sit on */
  ctx.beginPath();
  ctx.moveTo(band.x,band.cy+G.rA+3); ctx.lineTo(band.x+band.w,band.cy+G.rA+3);
  ctx.strokeStyle='#1b2030'; ctx.lineWidth=1; ctx.stroke();

  const x0=G.X(0), x1=G.X(L.r);
  /* the tie line from the movable atom down to its point on the curve */
  ctx.beginPath(); ctx.moveTo(x1,band.cy); ctx.lineTo(x1,gb.y1);
  ctx.strokeStyle=rgba(COL.live,0.30); ctx.lineWidth=1; ctx.setLineDash([3,4]);
  ctx.stroke(); ctx.setLineDash([]);

  drawAtom(ctx,x0,band.cy,G.rA,P.A.col,P.A.sym,false);
  drawAtom(ctx,x1,band.cy,G.rB,P.B.col,P.B.sym,false);
  /* PhET's push-pin on the fixed atom */
  if(P.pinned&&G.rA>8){
    const px=x0-G.rA*0.62, py=band.cy-G.rA*0.62;
    ctx.beginPath(); ctx.arc(px,py,4,0,TAU); ctx.fillStyle='#d8dbe4'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(px,py); ctx.lineTo(px+7,py+9);
    ctx.strokeStyle='#d8dbe4'; ctx.lineWidth=2; ctx.stroke();
  }

  /* The potential is drawn BEFORE the band's labels, not after, so that its
     title is already in the label registry when the force labels look for a
     slot — otherwise a label placed under the movable atom lands on it. */
  const A=drawWellPanel(ctx,gb,M,{xlo:G.xLo,xhi:G.xHi,
    title:titleFor(gb,'the Lennard-Jones potential of the pair','V(r)')});

  /* the names next, so the force labels dodge them rather than the other way */
  lab(ctx,W,H,band.x,band.y+9,P.A.name+(P.pinned?' (pinned)':' (free)'),
      rgba(P.A.col,0.9),LAB_FONT,'left');
  lab(ctx,W,H,band.x+band.w,band.y+9,P.B.name+' — drag it',
      rgba(P.B.col,0.9),LAB_FONT,'right');

  /* the force arrows, PhET's three modes.  A force of 1e-12 pN is zero: say
     so rather than printing a number that is pure cancellation.  Both labels
     go ABOVE the atom, where the graph title below cannot reach them. */
  const px=G.apx;
  const fTxt=f=>Math.abs(f)<1e-6?'≈ 0':sigf(Math.abs(f),3);
  if(st.forces!=='hidden'){
    const ay=band.cy;
    if(st.forces==='total'){
      forceArrow(ctx,x1,ay,pN(L.F),px,COL.pos,G.arrowCap);
      lab(ctx,W,H,x1,ay-G.rB-13,'total force '+fTxt(pN(L.F))+' pN',COL.pos,LAB_FONT,'center');
    } else {
      forceArrow(ctx,x1,ay-11,pN(L.Frep),px,COL.rep,G.arrowCap);
      forceArrow(ctx,x1,ay+11,-pN(L.Fatt),px,COL.att,G.arrowCap);
      lab(ctx,W,H,x1,ay-G.rB-27,'repulsive '+fTxt(pN(L.Frep))+' pN',COL.rep,LAB_FONT,'center');
      lab(ctx,W,H,x1,ay-G.rB-13,'attractive '+fTxt(pN(L.Fatt))+' pN',COL.att,LAB_FONT,'center');
    }
  }
  polyline(ctx,gb,[L.r,L.r],[A.ylo,A.yhi],A.xlo,A.xhi,A.ylo,A.yhi,rgba(COL.live,0.55),1.2,[4,4]);
  if(L.V/P.eps>=A.ylo&&L.V/P.eps<=A.yhi) dot(ctx,A.Xof(L.r),A.Yof(L.V/P.eps),5,COL.live,'#fff',1.2);
  /* at the TOP of the box: down by the axis they are pushed into the x-tick
     labels whenever sigma and r_min are close on screen (found at 560 px by
     the layout sweep, on the oxygen pair) */
  lab(ctx,W,H,A.Xof(P.sig),gb.y+13,'σ',COL.struct,LAB_FONT,'center');
  lab(ctx,W,H,A.Xof(P.rmin),gb.y+13,'r_min',COL.struct,LAB_FONT,'center');
  lab(ctx,W,H,gb.x+5,A.Yof(-1)-10,'−ε',COL.struct,LAB_FONT,'left');

  /* the honest note: the drawn-atom factor and the arrow scale */
  drawNoteIf(ctx,G.note);
  return G;
}

/* ---------------- B. the well ---------------- */
function drawWell(ctx,W,H,M){
  const P=M.P, L=M.L, st=M.st;
  reserveReadout(W,H);
  const Lo=stageLayoutH(ctx,W,H,WELL_CAP_FULL,WELL_CAP_SHORT,2,0.44,1);
  drawCaption(ctx,Lo);
  /* fit each axis to the structure it contains: past 2.45 sigma the well is
     flat and the panel is all tail (diffraction Known-bad) */
  const lo=0.80*P.sig, hi=2.45*P.sig;
  const C=wellCurve(P,280,lo,hi);
  const note='σ = '+fmt(P.sig,1)+' pm, where V crosses zero   ·   r_min = 2^(1/6) σ = '
    +fmt(P.rmin,1)+' pm, where V = −ε and the force vanishes   ·   the strongest pull is at '
    +'(26/7)^(1/6) σ = '+fmt(P.rF,1)+' pm, the inflection of V, and is '
    +sigf(-pN(ljF(P.rF,P.sig,P.eps)),3)+' pN   ·   the force panel is scaled to the '
    +'ATTRACTION, so its repulsive wall runs off the top of the box';
  const N=noteFit(ctx,noteLimit(Lo),Lo.main,note,
    'σ = '+fmt(P.sig,1)+' pm, r_min = '+fmt(P.rmin,1)+' pm, strongest pull at '
    +fmt(P.rF,1)+' pm'), mb=N.b;
  const A=drawWellPanel(ctx,mb,{P,C},{xlo:lo,xhi:hi,ylo:-1.32,yhi:2.4,
    title:titleFor(mb,'V(r) — the well, with its three exact landmarks','V(r)')});
  polyline(ctx,mb,[L.r,L.r],[A.ylo,A.yhi],A.xlo,A.xhi,A.ylo,A.yhi,rgba(COL.live,0.5),1.2,[4,4]);
  if(L.V/P.eps>=A.ylo&&L.V/P.eps<=A.yhi) dot(ctx,A.Xof(L.r),A.Yof(L.V/P.eps),5,COL.live,'#fff',1.2);
  if(P.rF<hi) polyline(ctx,mb,[P.rF,P.rF],[A.ylo,A.yhi],A.xlo,A.xhi,A.ylo,A.yhi,
                       rgba(COL.ref,0.35),1,[2,3]);
  /* the three landmarks are named at the TOP of the panel, on their own
     dashed rules: down at the axis they sit among the tick labels */
  lab(ctx,W,H,A.Xof(P.sig),mb.y+13,'σ',COL.struct,LAB_FONT,'center');
  lab(ctx,W,H,A.Xof(P.rmin),mb.y+13,'r_min',COL.struct,LAB_FONT,'center');
  lab(ctx,W,H,A.Xof(P.rF),mb.y+13,'r_F',COL.ref,LAB_FONT,'center');
  lab(ctx,W,H,mb.x+5,A.Yof(-1)-11,'−ε',COL.struct,LAB_FONT,'left');
  drawNoteIf(ctx,N);

  /* the force */
  const fb=Lo.bottom[0];
  if(fb){
    const fs=C.fs.map(pN), reps=C.reps.map(pN), atts=C.atts.map(pN);
    /* the repulsive wall is thirty times the deepest pull, so an axis fitted to
       it hides the attraction entirely: fit the ATTRACTIVE extreme and let the
       wall run off the top, which the note says it does */
    let fmin=0;
    for(let i=0;i<fs.length;i++) fmin=Math.min(fmin,fs[i]);
    const fhi=-3.2*1.45*fmin, flo=noCornerTick(1.45*fmin,fhi,nyFor(fb));
    /* a hair of x margin, so the leftmost x-tick label is not in the same
       corner as the lowest y-tick label — axes() draws both and neither knows
       about the other (found by the layout sweep on sigma = 500 pm) */
    const xlo=lo-0.06*(hi-lo);
    axesR(ctx,fb,xlo,hi,flo,fhi,{xlab:'r, pm',ylab:'F(r), pN',nx:nxFor(fb),ny:nyFor(fb),
      xfmt:t=>fmt(t,0),yfmt:t=>sigf(t,2),
      title:titleFor(fb,'F(r) = −dV/dr','F(r)')});
    polyline(ctx,fb,[xlo,hi],[0,0],xlo,hi,flo,fhi,'#3a4152',1,[3,4]);
    if(st.forces==='components'){
      polyline(ctx,fb,C.xs,reps,xlo,hi,flo,fhi,COL.rep,1.4);
      polyline(ctx,fb,C.xs,atts,xlo,hi,flo,fhi,COL.att,1.4);
    }
    polyline(ctx,fb,C.xs,fs,xlo,hi,flo,fhi,COL.pos,2);
    polyline(ctx,fb,[P.rmin,P.rmin],[flo,fhi],xlo,hi,flo,fhi,rgba(COL.struct,0.5),1,[2,3]);
    polyline(ctx,fb,[P.rF,P.rF],[flo,fhi],xlo,hi,flo,fhi,rgba(COL.ref,0.5),1,[2,3]);
    marker(ctx,fb,xlo,hi,flo,fhi,L.r,clamp(pN(L.F),flo,fhi),COL.live);
    const items=[[COL.pos,'F = −dV/dr']];
    if(st.forces==='components'){ items.push([COL.rep,'48εσ¹²/r¹³']); items.push([COL.att,'−24εσ⁶/r⁷']); }
    items.push([COL.ref,'strongest pull, (26/7)^(1/6) σ']);
    regLegend(legendAuto(ctx,fb,items));
  }

  /* the residual: closed form against a numerical derivative of V */
  const rb=Lo.bottom[1];
  if(rb){
    const xs=[],ys=[];
    for(let i=0;i<=100;i++){
      const r=lo+(hi-lo)*i/100;
      const scale=24*P.eps/r;
      xs.push(r);
      ys.push(Math.max(1e-18,Math.abs(ljF(r,P.sig,P.eps)-numForce(r,P.sig,P.eps))/scale));
    }
    /* the floor is -18.4, not -18: a tick exactly on the frame puts its label
       in the same corner as the leftmost x-tick label (the sweep found this at
       sigma = 500 pm, where the x axis also starts on a round number) */
    const yl=-18.4, yh=-11.8, rxlo=lo-0.06*(hi-lo);
    axesR(ctx,rb,rxlo,hi,yl,yh,{xlab:'r, pm',ylab:'log₁₀ |ΔF| / (24ε/r)',nx:nxFor(rb),ny:nyFor(rb),
      xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0),
      title:titleFor(rb,'the force really is minus the derivative','residual')});
    polyline(ctx,rb,xs,ys.map(v=>Math.log10(v)),rxlo,hi,yl,yh,COL.ref,1.6);
    polyline(ctx,rb,[rxlo,hi],[Math.log10(2.220446049250313e-16),Math.log10(2.220446049250313e-16)],
             rxlo,hi,yl,yh,rgba(COL.dim,0.6),1,[3,4]);
    lab(ctx,W,H,rb.x+7,rb.y+12,'dashed: one double-precision epsilon',COL.dim,SM_FONT,'left');
  }
}

/* a Richardson-extrapolated central difference of V, used ONLY as the
   independent route to the force (never to draw the physics) */
function numForce(r,sig,eps){
  const h=r*1e-4;
  const d=hh=>(ljV(r+hh,sig,eps)-ljV(r-hh,sig,eps))/(2*hh);
  return -(4*d(h/2)-d(h))/3;
}
function numVpp(r,sig,eps){
  const h=r*1e-3;
  const d=hh=>(ljV(r+hh,sig,eps)-2*ljV(r,sig,eps)+ljV(r-hh,sig,eps))/(hh*hh);
  return (4*d(h/2)-d(h))/3;
}

/* ---------------- C. the motion ---------------- */
function drawMotion(ctx,W,H,M){
  const P=M.P, L=M.L, st=M.st, MO=M.MO;
  reserveReadout(W,H);
  const Lo=stageLayoutH(ctx,W,H,MOTION_CAP_FULL,MOTION_CAP_SHORT,2,0.42,1);
  drawCaption(ctx,Lo);
  const b=Lo.main;
  const Twin=isFinite(L.period)?clamp(4*L.period,2,40):12;
  const t1=Math.max(Twin,st.t), t0=t1-Twin;
  let rlo=P.rmin-1,rhi=P.rmin+1;
  if(L.tp){ rlo=Math.min(rlo,L.tp.rIn); rhi=Math.max(rhi,isFinite(L.tp.rOut)?L.tp.rOut:P.rHi); }
  for(const p of MO.trail){ if(p[0]<t0) continue; rlo=Math.min(rlo,p[1]); rhi=Math.max(rhi,p[1]); }
  const pad=0.08*(rhi-rlo)+2; rlo-=pad; rhi+=pad;
  rhi=Math.min(rhi,P.rHi*1.15);
  axesR(ctx,b,t0,t1,rlo,rhi,{xlab:'time t, ps',ylab:'separation r, pm',nx:nxFor(b),ny:nyFor(b),
    xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,0),
    title:titleFor(b,'r(t) — the movable atom in the well','r(t)')});
  polyline(ctx,b,[t0,t1],[P.rmin,P.rmin],t0,t1,rlo,rhi,rgba(COL.struct,0.45),1,[3,4]);
  if(L.bound&&L.tp){
    polyline(ctx,b,[t0,t1],[L.tp.rIn,L.tp.rIn],t0,t1,rlo,rhi,rgba(COL.ref,0.75),1.2,[5,4]);
    if(isFinite(L.tp.rOut))
      polyline(ctx,b,[t0,t1],[L.tp.rOut,L.tp.rOut],t0,t1,rlo,rhi,rgba(COL.ref,0.75),1.2,[5,4]);
  }
  if(MO.trail.length>1){
    const ts=MO.trail.map(p=>p[0]), rs=MO.trail.map(p=>p[1]);
    polyline(ctx,b,ts,rs,t0,t1,rlo,rhi,COL.pos,1.8);
  }
  if(st.t>=t0) marker(ctx,b,t0,t1,rlo,rhi,st.t,clamp(L.r,rlo,rhi),COL.live);
  /* build the legend from what was emitted: an unbound orbit has no turning
     points and an untouched view has no trace, and naming either would be a
     false statement about the picture (adiabatic_expansion Known-bad) */
  { const it=[];
    if(MO.trail.length>1) it.push([COL.pos,'r(t), velocity Verlet']);
    if(L.bound&&L.tp) it.push([COL.ref,'turning points (exact)']);
    it.push([COL.struct,'r_min']);
    regLegend(legendAuto(ctx,b,it)); }
  if(!MO.trail.length)
    lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.72,'press release, or play, to set it going',COL.dim,CAP_FONT,'center');

  /* the ledger */
  const eb=Lo.bottom[0];
  if(eb){
    const es=MO.trail.filter(p=>p[0]>=t0);
    /* fitted to the three curves, not to the whole well: K only ever reaches
       E + eps, which at a 10-pm release is 0.025 eps */
    let elo=Math.min(L.V/P.eps,L.E/P.eps), ehi=Math.max(L.K/P.eps,L.E/P.eps,0);
    for(const p of es){ elo=Math.min(elo,p[3]/P.eps,(p[2]+p[3])/P.eps);
      ehi=Math.max(ehi,(p[2]+p[3])/P.eps,p[2]/P.eps); }
    const epad=0.10*(ehi-elo)+0.01; elo-=epad; ehi+=epad;
    axesR(ctx,eb,t0,t1,elo,Math.min(ehi,4),{xlab:'t, ps',ylab:'energy / ε',nx:nxFor(eb),ny:nyFor(eb),
      xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,1),
      title:titleFor(eb,'the energy ledger — K, V and their sum','energy')});
    if(es.length>1){
      const ts=es.map(p=>p[0]);
      polyline(ctx,eb,ts,es.map(p=>p[2]/P.eps),t0,t1,elo,ehi,COL.kin,1.5);
      polyline(ctx,eb,ts,es.map(p=>p[3]/P.eps),t0,t1,elo,ehi,COL.pot,1.5);
      polyline(ctx,eb,ts,es.map(p=>(p[2]+p[3])/P.eps),t0,t1,elo,ehi,COL.tot,2);
    }
    polyline(ctx,eb,[t0,t1],[L.E/P.eps,L.E/P.eps],t0,t1,elo,ehi,rgba(COL.tot,0.35),1,[3,4]);
    /* nothing has been released yet: there are no curves to name */
    if(es.length>1)
      regLegend(legendAuto(ctx,eb,[[COL.kin,'K = ½μṙ²'],[COL.pot,'V(r)'],[COL.tot,'E = K + V']]));
    else lab(ctx,W,H,eb.x+eb.w/2,eb.y+eb.h*0.5,'nothing released yet',COL.dim,SM_FONT,'center');
  }

  /* the phase portrait */
  const pb=Lo.bottom[1];
  if(pb){
    /* the orbit, not the separatrix, sets the frame: the separatrix reaches
       hundreds of m/s at the wall and would squash every bound orbit to a line.
       It is clipped by polyline, which is what the dashed curve leaving the top
       of the box means. */
    let vmax=Math.abs(st.v);
    for(const v of MO.ph.vs) vmax=Math.max(vmax,v);
    if(!(vmax>0)) vmax=Math.max.apply(null,MO.sep.vs)*0.25;
    vmax*=1.45;
    const rOut=(L.tp&&isFinite(L.tp.rOut))?L.tp.rOut:P.rHi;
    const plo=P.sig*0.88, phi=clamp(1.25*rOut,1.4*P.sig,P.rHi);
    axesR(ctx,pb,plo,phi,-vmax,vmax,{xlab:'r, pm',ylab:'dr/dt, m/s',nx:nxFor(pb),ny:nyFor(pb),
      xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0),
      title:titleFor(pb,'the phase portrait and the E = 0 separatrix','phase')});
    polyline(ctx,pb,MO.sep.rs,MO.sep.vs,plo,phi,-vmax,vmax,rgba(COL.ref,0.8),1.3,[4,4]);
    polyline(ctx,pb,MO.sep.rs,MO.sep.vs.map(v=>-v),plo,phi,-vmax,vmax,rgba(COL.ref,0.8),1.3,[4,4]);
    if(MO.ph.rs.length){
      polyline(ctx,pb,MO.ph.rs,MO.ph.vs,plo,phi,-vmax,vmax,COL.pos,1.6);
      polyline(ctx,pb,MO.ph.rs,MO.ph.vs.map(v=>-v),plo,phi,-vmax,vmax,COL.pos,1.6);
    }
    marker(ctx,pb,plo,phi,-vmax,vmax,clamp(L.r,plo,phi),clamp(st.v,-vmax,vmax),COL.live);
    { const it=[];
      /* at E = -eps exactly the "orbit" is the fixed point at the bottom of
         the well: the polyline is zero length and nothing green is drawn, so
         the legend must not name it */
      if(MO.ph.rs.length&&L.tp&&(L.tp.rOut-L.tp.rIn)>0.02) it.push([COL.pos,'this orbit (closed)']);
      it.push([COL.ref,'E = 0, the separatrix']);
      it.push([COL.live,L.bound?'the atom now':'the atom now — unbound, no closed orbit']);
      regLegend(legendAuto(ctx,pb,it)); }
  }
}

/* ---------------- D. small oscillations ---------------- */
function drawSmall(ctx,W,H,M){
  const P=M.P, S=M.SM;
  reserveReadout(W,H);
  const Lo=stageLayoutH(ctx,W,H,SMALL_CAP_FULL,SMALL_CAP_SHORT,1,0.44,1);
  drawCaption(ctx,Lo);
  const note='ω = √(V″(r_min)/μ) = '+sigf(P.omega,4)+' rad/ps, so T = '+sigf(P.period,4)+' ps'
    +'   ·   μ = '+sigf(P.mu,4)+' u ('
    +(P.pinned?'the left atom is pinned, so μ is the movable atom’s own mass'
              :'both atoms move, so μ = m₁m₂/(m₁+m₂)')
    +')   ·   the vertical axis is the height above the bottom of the well, in units of '
    +'the energy the atom was released with, so both turning points sit at exactly 1';
  const N=noteFit(ctx,noteLimit(Lo),Lo.main,note,
    'ω = '+sigf(P.omega,4)+' rad/ps, T = '+sigf(P.period,4)+' ps, μ = '
    +sigf(P.mu,4)+' u'), b=N.b;
  /* the height above the floor of the well, in units of the release energy:
     a zoomed absolute V/eps axis needs six decimals and its tick labels then
     run into the rotated axis title (found by the layout sweep). */
  const scale=Math.max(S.E/P.eps+1,1e-12);
  const yv=v=>(v+1)/scale;
  const ys=S.ys.map(yv), hs=S.hs.map(yv);
  let ylo=0, yhi=1;
  for(let i=0;i<ys.length;i++){ ylo=Math.min(ylo,ys[i],hs[i]); yhi=Math.max(yhi,ys[i],hs[i]); }
  yhi=Math.min(yhi,8);
  const pad=0.09*(yhi-ylo); ylo-=pad; yhi+=pad;
  axesR(ctx,b,S.lo,S.hi,ylo,yhi,{xlab:'separation r, pm',ylab:'(V + ε) / (E + ε)',
    nx:nxFor(b),ny:nyFor(b),
    xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,2),
    title:titleFor(b,'the bottom of the well and the parabola through it','the well bottom')});
  polyline(ctx,b,S.xs,hs,S.lo,S.hi,ylo,yhi,COL.ref,1.8,[5,4]);
  polyline(ctx,b,S.xs,ys,S.lo,S.hi,ylo,yhi,COL.pos,2);
  polyline(ctx,b,[P.rmin,P.rmin],[ylo,yhi],S.lo,S.hi,ylo,yhi,rgba(COL.struct,0.45),1,[2,3]);
  if(S.tp&&isFinite(S.tp.rOut)){
    polyline(ctx,b,[S.lo,S.hi],[1,1],S.lo,S.hi,ylo,yhi,rgba(COL.live,0.6),1.2,[4,4]);
    [S.tp.rIn,S.tp.rOut].forEach(r=>{
      if(r>=S.lo&&r<=S.hi) marker(ctx,b,S.lo,S.hi,ylo,yhi,r,1,COL.live); });
  }
  regLegend(legendAuto(ctx,b,[[COL.pos,'V(r)'],[COL.ref,'the parabola ½V″(r_min)(r−r_min)²'],
                    [COL.live,'E and its turning points']]));
  drawNoteIf(ctx,N);

  const pb=Lo.bottom[0];
  if(pb&&S.as.length>2){
    const xl=Math.log10(S.as[0]), xh=Math.log10(S.as[S.as.length-1]);
    const yl=-9, yh=0.6;
    axesR(ctx,pb,xl,xh,yl,yh,{xlab:'log₁₀ amplitude a, pm',ylab:'log₁₀ (T/T₀ − 1)',
      nx:nxFor(pb),ny:nyFor(pb),
      xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,0),
      title:titleFor(pb,'how fast the period leaves 2π/ω — and Landau’s law for it','T(a)/T₀ − 1')});
    const lx=S.as.map(a=>Math.log10(a));
    /* the two agree, so the measured curve covers the prediction: draw the
       prediction WIDE and sparsely dashed so it reads as beads either side of
       the green (the four-colour-fan lesson: when N things coincide, say so) */
    polyline(ctx,pb,lx,S.pred.map(v=>Math.log10(Math.max(v,1e-30))),xl,xh,yl,yh,COL.ref,5,[3,9]);
    polyline(ctx,pb,lx,S.ex.map(v=>Math.log10(Math.max(v,1e-30))),xl,xh,yl,yh,COL.pos,1.8);
    if(S.aNow>0&&isFinite(S.Tnow))
      marker(ctx,pb,xl,xh,yl,yh,clamp(Math.log10(S.aNow),xl,xh),
             clamp(Math.log10(Math.max(S.Tnow/P.period-1,1e-30)),yl,yh),COL.live);
    regLegend(legendAuto(ctx,pb,[[COL.pos,'the quadrature'],[COL.ref,'(91/4) a²/r_min² — under it'],
                                 [COL.live,'the slider']]));
  }
}

/* ---------------- E. the atom pairs ---------------- */
function drawPairs(ctx,W,H,M){
  const R=M.PR, st=M.st;
  reserveReadout(W,H);
  const Lo=stageLayoutH(ctx,W,H,PAIRS_CAP_FULL,PAIRS_CAP_SHORT,2,0.42,1);
  drawCaption(ctx,Lo);
  const note='every well is drawn at depth 1 so the SHAPES can be compared; the depths are the '
    +'bars below   ·   solid: PhET’s σ   ·   dashed: the literature’s σ, by '
    +'Lorentz–Berthelot for the mixed pairs   ·   the adjustable pair has no literature value';
  const N=noteFit(ctx,noteLimit(Lo),Lo.main,note,
    'the wells are drawn at depth 1: the depths are the bars below'), b=N.b;
  const xhi=520, ylo=-1.32, yhi=0.42;
  axesR(ctx,b,120,xhi,ylo,yhi,{xlab:'separation r, pm',ylab:'V(r) / ε',nx:nxFor(b),ny:nyFor(b),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1),
    title:titleFor(b,'every pair PhET offers — solid PhET, dashed the literature','the wells')});
  polyline(ctx,b,[120,xhi],[0,0],120,xhi,ylo,yhi,'#3a4152',1,[3,4]);
  polyline(ctx,b,[120,xhi],[-1,-1],120,xhi,ylo,yhi,rgba(COL.struct,0.30),1,[3,4]);
  const items=[];
  R.rows.forEach((row,i)=>{
    const c=neonCss(i/(R.rows.length-1));
    const xs=[],ys=[],ls=[],lys=[];
    for(let k=0;k<=200;k++){
      const r=120+(xhi-120)*k/200;
      xs.push(r); ys.push(ljV(r,row.sig,1));
      if(row.lsig!==undefined){ ls.push(r); lys.push(ljV(r,row.lsig,1)); }
    }
    polyline(ctx,b,xs,ys,120,xhi,ylo,yhi,c,1.7);
    if(st.showLit&&row.lsig!==undefined) polyline(ctx,b,ls,lys,120,xhi,ylo,yhi,c,1.2,[4,4]);
    items.push([c,row.label]);
  });
  const legR=legendAuto(ctx,b,items);
  regLegend(legR);
  /* with seven curves across one panel legendAuto correctly finds no clear
     corner and draws nothing; then nothing says which colour is which, so each
     well is named at its own minimum instead */
  if(!legR) R.rows.forEach((row,i)=>{
    const c=neonCss(i/(R.rows.length-1)), rm=rMin(row.sig);
    if(rm<120||rm>xhi) return;
    lab(ctx,W,H,b.x+b.w*(rm-120)/(xhi-120),
        b.y1-b.h*(-1-ylo)/(yhi-ylo)-12,row.key,c,SM_FONT,'center');
  });
  drawNoteIf(ctx,N);

  /* sigma bars */
  const sb=Lo.bottom[0];
  if(sb){
    const rows=R.rows.filter(r=>r.lsig!==undefined);
    const hi=Math.max.apply(null,rows.map(r=>Math.max(r.sig,r.lsig,r.rmin,r.lrmin)))*1.12;
    axesR(ctx,sb,-0.5,rows.length-0.5,0,hi,{ylab:'pm',nx:1,ny:nyFor(sb),
      xticks:[],yfmt:t=>fmt(t,0),
      title:titleFor(sb,'σ: PhET’s against the literature’s σ and r_min','σ')});
    rows.forEach((row,i)=>{
      const w=sb.w/rows.length*0.20;
      const X=x=>sb.x+sb.w*(x+0.5)/rows.length;
      const Y=v=>sb.y1-sb.h*v/hi;
      const bar=(dx,v,col)=>{ ctx.fillStyle=col; ctx.fillRect(X(i)+dx-w/2,Y(v),w,sb.y1-Y(v)); };
      bar(-w*1.1,row.sig,rgba(COL.pos,0.85));
      bar(0,row.lsig,rgba(COL.ref,0.85));
      bar(w*1.1,row.lrmin,rgba(COL.struct,0.85));
      lab(ctx,W,H,X(i),sb.y1+12,row.key,COL.dim,SM_FONT,'center','top');
    });
    regLegend(legendAuto(ctx,sb,[[COL.pos,'PhET σ'],[COL.ref,'literature σ'],[COL.struct,'literature r_min']]));
  }
  /* epsilon bars, on a log axis (oxygen is 1000 K) */
  const eb=Lo.bottom[1];
  if(eb){
    const rows=R.rows.filter(r=>r.leps!==undefined);
    const yl=Math.log10(20), yh=Math.log10(1400);
    axesR(ctx,eb,-0.5,rows.length-0.5,yl,yh,{ylab:'ε/k_B, K (log₁₀)',nx:1,ny:nyFor(eb),
      xticks:[],yfmt:t=>fmt(Math.pow(10,t),0),
      title:titleFor(eb,'ε: PhET’s against the literature’s','ε')});
    rows.forEach((row,i)=>{
      const w=eb.w/rows.length*0.26;
      const X=x=>eb.x+eb.w*(x+0.5)/rows.length;
      const Y=v=>eb.y1-eb.h*(Math.log10(v)-yl)/(yh-yl);
      const bar=(dx,v,col)=>{ ctx.fillStyle=col; ctx.fillRect(X(i)+dx-w/2,Math.min(Y(v),eb.y1),w,Math.max(0,eb.y1-Y(v))); };
      bar(-w*0.6,row.eps,rgba(COL.pos,0.85));
      bar(w*0.6,row.leps,rgba(COL.ref,0.85));
      lab(ctx,W,H,X(i),eb.y1+12,row.key,COL.dim,SM_FONT,'center','top');
    });
    regLegend(legendAuto(ctx,eb,[[COL.pos,'PhET ε'],[COL.ref,'literature ε']]));
  }
}

/* ---------------- F. the integrator ---------------- */
function drawSteppers(ctx,W,H,M){
  const I=M.IT, P=M.P;
  reserveReadout(W,H);
  const Lo=stageLayoutH(ctx,W,H,STEP_CAP_FULL,STEP_CAP_SHORT,0,0,0);
  drawCaption(ctx,Lo);
  const note=P.label+' released at rest '+fmt(I.r0-P.rmin,0)+' pm outside the minimum; one '
    +'period is '+sigf(I.T,4)+' ps   ·   both axes of both panels are log₁₀   ·   '
    +'values below 10⁻¹³ ε are clipped to the axis floor';
  const N=noteFit(ctx,noteLimit(Lo),Lo.main,note,
    P.label+', released 10 pm out; both axes log₁₀');
  /* Two stacked panels under ~110 px each put their rotated y-axis titles on
     top of one another, whatever the gap: a rotated title is as long as its
     text and it is centred on the panel.  On a narrow stage draw ONE panel —
     the boundedness one, which carries the point — and say why the other is
     missing (waveguides/pupil_plane Known-bad: give a view a narrow mode). */
  const split=splitRow(N.b,2,62);
  const tooShort=split[0].w===N.b.w&&split[0].h<110;
  const ob=tooShort?null:split[0], db=tooShort?N.b:split[1];
  const KIND=[['verlet',COL.pos,'velocity Verlet'],['symplectic',COL.struct,'semi-implicit Euler (PhET’s)'],
              ['forward',COL.ref,'forward Euler']];
  /* order */
  if(ob){
  const xl=Math.log10(I.dts[I.dts.length-1])-0.15, xh=Math.log10(I.dts[0])+0.15;
  let yl=0, yh=-20;
  KIND.forEach(([k])=>{ I.curves[k].es.forEach(v=>{ const l=Math.log10(Math.max(v,1e-30));
    yl=Math.min(yl,l); yh=Math.max(yh,l); }); });
  yl-=0.4; yh+=0.4;
  axesR(ctx,ob,xl,xh,yl,yh,{xlab:'log₁₀ Δt, ps',ylab:'log₁₀ max|ΔE| / ε',
    nx:nxFor(ob),ny:nyFor(ob),
    xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,0),
    title:titleFor(ob,'the order: energy error over one period against Δt','the order')});
  KIND.forEach(([k,c])=>{
    polyline(ctx,ob,I.dts.map(Math.log10),I.curves[k].es.map(v=>Math.log10(Math.max(v,1e-30))),
             xl,xh,yl,yh,c,1.8);
    I.dts.forEach((dt,i)=>{
      const X=ob.x+ob.w*(Math.log10(dt)-xl)/(xh-xl);
      const Y=ob.y1-ob.h*(Math.log10(Math.max(I.curves[k].es[i],1e-30))-yl)/(yh-yl);
      if(Y>=ob.y&&Y<=ob.y1) dot(ctx,X,Y,3,c,'#0a0c12',1);
    });
  });
  regLegend(legendAuto(ctx,ob,KIND.map(([k,c,n])=>[c,n+'  p = '+fmt(I.curves[k].order,2)])));
  }

  /* boundedness */
  let dyl=0,dyh=-20;
  KIND.forEach(([k])=>{ I.drift[k].ds.forEach(v=>{ const l=Math.log10(Math.max(v,1e-30));
    dyl=Math.min(dyl,l); dyh=Math.max(dyh,l); }); });
  dyl=Math.max(dyl,-13)-0.3; dyh+=0.5;
  axesR(ctx,db,0,I.nPer,dyl,dyh,{xlab:'time, in periods',ylab:'log₁₀ |E(t) − E(0)| / ε',
    nx:nxFor(db),ny:nyFor(db),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0),
    title:titleFor(db,'the boundedness: the same run at Δt = 1 fs','boundedness')});
  const ENDS=[];
  KIND.forEach(([k,c,nm])=>{
    const ys=I.drift[k].ds.map(v=>Math.log10(Math.max(v,1e-30)));
    polyline(ctx,db,I.drift[k].ts,ys,0,I.nPer,dyl,dyh,c,1.4);
    /* Each curve is tagged at its own end rather than relying on the legend:
       with three curves across a narrow panel legendAuto finds no clear corner
       and correctly draws nothing, and then nothing on the canvas says which
       line is which (the legend-entry-for-a-curve-not-drawn lesson, inverted). */
    const n=ys.length;
    if(n){
      const X=db.x+db.w*I.drift[k].ts[n-1]/I.nPer;
      const Y=db.y1-db.h*(ys[n-1]-dyl)/(dyh-dyl);
      if(Y>=db.y&&Y<=db.y1) dot(ctx,clamp(X,db.x,db.x1),Y,3.2,c,'#0a0c12',1);
      ENDS.push([k,c,nm,clamp(X,db.x,db.x1),Y]);
    }
  });
  const legD=legendAuto(ctx,db,KIND.map(([k,c,n])=>[c,n]));
  regLegend(legD);
  /* the end tags exist so a panel that could not place a legend still says
     which curve is which — with a legend they are redundant clutter */
  if(!legD) for(const [k,c,nm,X,Y] of ENDS)
    if(Y>=db.y&&Y<=db.y1) lab(ctx,W,H,X-8,Y,nm.split(' ')[0],c,SM_FONT,'right');
  const nb=ob?box(ob.x,ob.y,db.x1-ob.x,db.y1-ob.y):db;
  if(N.fits) drawNote(ctx,nb,N.txt);
  else if(!ob) lab(ctx,W,H,db.x,db.y-24,
    'the Δt panel needs a wider stage; its slopes are ' +
    KIND.map(([k,c,n])=>n.split(' ')[0]+' '+fmt(I.curves[k].order,2)).join(', '),
    COL.dim,SM_FONT,'left');
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='atoms') drawAtoms(ctx,W,H,M);
  else if(M.view==='well') drawWell(ctx,W,H,M);
  else if(M.view==='motion') drawMotion(ctx,W,H,M);
  else if(M.view==='small') drawSmall(ctx,W,H,M);
  else if(M.view==='pairs') drawPairs(ctx,W,H,M);
  else drawSteppers(ctx,W,H,M);
}

function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of the clock.  dtFrame is model time; the integrator substeps at
     DT_INT so the step size never depends on the frame rate. */
  S.advance=function(dtFrame){
    const P=pairInfo(ST);
    let left=dtFrame;
    const s={r:ST.r,v:ST.v,a:ljF(ST.r,P.sig,P.eps)/P.mu,t:ST.t};
    while(left>1e-12){
      const dt=Math.min(DT_INT,left);
      stepVerlet(s,P.sig,P.eps,P.mu,dt);
      left-=dt;
      if(s.r<0.55*P.sig){ s.r=0.55*P.sig; s.v=Math.abs(s.v); }   /* the wall, stated on the canvas */
      if(s.r>6*P.sig){ ST.running=false; break; }
    }
    ST.r=s.r; ST.v=s.v; ST.t=s.t;
    const K=0.5*P.mu*s.v*s.v, V=ljV(s.r,P.sig,P.eps);
    TRAIL.push([s.t,s.r,K,V]);
    if(TRAIL.length>TRAIL_MAX) TRAIL.splice(0,TRAIL.length-TRAIL_MAX);
  };
  S.step=function(){
    if(!ST.running) return false;
    S.advance(PS_PER_SEC*(ST.slow?SLOW_FACTOR:1)/60);
    return true;
  };
  S.ended=function(){ return !ST.running; };
  /* the pointer: drag the movable atom, on the two-atoms view */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(ST.view!=='atoms') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(), G=atomsGeom(ctx,S.W,S.H,M);
    if(type==='down'){
      const dx=x-G.X(ST.r), dy=y-G.band.cy;
      const hit=Math.hypot(dx,dy)<=Math.max(12,G.rB)+4
        || (x>=G.gb.x&&x<=G.gb.x1&&y>=G.gb.y&&y<=G.gb.y1&&Math.abs(x-G.X(ST.r))<14);
      if(hit){ DRAG.what='atom'; DRAG.off=G.wx(x)-ST.r; ST.running=false; return true; }
      return false;
    }
    if(type==='move'&&DRAG.what==='atom'){ setSep(ST,G.wx(x)-DRAG.off); return true; }
    return false;
  };
  return S;
}
