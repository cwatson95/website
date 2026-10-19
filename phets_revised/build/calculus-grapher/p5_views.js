
/* ================================================================== *
 *  views 3-6, the dispatch and the scene                              *
 * ================================================================== */

/* ---- view 3: the lab (PhET's Lab and Advanced screens) ------------ */
function labCap(M){
  const S=M.live, st=M.st;
  const full='All four curves at once, which is PhET’s Lab screen: the integral of f on top, then f, '
    +'then its first and second derivatives. The reference line runs through all four, and the readout '
    +'gives the four numbers where it stands. Notice what happens at a corner of f: the first derivative '
    +'jumps and the second derivative has a spike. The spike is not a value — the second derivative of '
    +'a corner is a delta function — and its height here is the slope jump divided by the cell width, '
    +'so it grows without limit as the grid is refined while the AREA under it stays fixed.'
    +(st.predict?' Predict is on: the upper f panel carries your sketch in orange, while the other '
      +'panels — and the tangent, which measures f and not your sketch — keep showing the '
      +'real one.':'');
  const short='PhET’s Lab screen: ∫f, f, f′ and f″ with one reference line through all four.';
  return {full,short};
}
function drawLab(ctx,W,H,M){
  const S=M.live, SH=M.shape, T=M.tools, st=M.st;
  const cap=labCap(M);
  const L=panelStack(ctx,W,H,4,cap.full,cap.short);
  const bI=L.bs[0], bF=L.bs[1], bD=L.bs[2], bD2=L.bs[3];
  const mI=mapFor(bI,XMIN,XMAX,-M.yI,M.yI), mF=mapFor(bF,XMIN,XMAX,-M.yF,M.yF);
  const mD=mapFor(bD,XMIN,XMAX,-M.yD,M.yD), mD2=mapFor(bD2,XMIN,XMAX,-M.yD2,M.yD2);
  GEO.view='lab'; GEO.fb=bF; GEO.fmap=mF;
  GEO.panels=[[bI,mI],[bF,mF],[bD,mD],[bD2,mD2]];

  const set=[[bI,mI,M.yI,COL.I,cName('I'),S.F,XG,null],
             [bF,mF,M.yF,COL.f,cName('f'),SH.f,XG,null],
             [bD,mD,M.yD,COL.d,cName('d'),S.d,XMID,breakCells(S.corners)],
             [bD2,mD2,M.yD2,COL.dd,cName('dd'),S.d2,XG,null]];
  for(let k=0;k<set.length;k++){
    const [b,m,ymax,col,name,ys,xs,brk]=set[k];
    if(st.grid) unitGrid(ctx,b,m,1,tickStep(-ymax,ymax));
    /* one shared x axis for the whole stack: only the bottom panel is labelled */
    axesT(ctx,b,XMIN,XMAX,-ymax,ymax,k===3?xAxisOpt():{xfmt:()=>''});
    panelTitle(ctx,b,name,col);
    zeroLine(ctx,b,m);
    if(k===1&&st.predict&&st.showF)
      polyline(ctx,b,XG,S.f,m.xlo,m.xhi,m.ylo,m.yhi,COL.f,1.5,[6,4]);
    if(brk&&brk.length) plotRuns(ctx,b,xs,ys,m,col,1.7,brk,st.discont==='dashedLine');
    else polyline(ctx,b,xs,ys,m.xlo,m.xhi,m.ylo,m.yhi,
                  (k===1&&st.predict)?COL.pred:col,1.9);
    if(st.refLine) scrub(ctx,W,H,b,m,st.xR,COL.struct,k===0?(VAR()+' = '+fmt(st.xR,2)):null,'R');
  }
  if(st.tangent){ tangentLine(ctx,bF,mF,T.tan,0.9); scrub(ctx,W,H,bF,mF,st.xT,COL.live,null,'T'); }
  if(st.area){ areaFill(ctx,bF,mF,S.f,clamp(st.xA,XMIN,XMAX)); scrub(ctx,W,H,bF,mF,st.xA,COL.live,null,'A'); }
  if(st.values){
    const at=[[bI,mI,integAt(S.f,S.F,st.xR)],[bF,mF,valueAt(S.f,st.xR)],
              [bD,mD,S.d[cellAt(st.xR)]],[bD2,mD2,S.d2[idxAt(st.xR)]]];
    for(const [b,m,v] of at)
      lab(ctx,W,H,clamp(m.X(st.xR),b.x,b.x1)+7,clamp(m.Y(v),b.y+6,b.y1-6),
          fmt(v,3),COL.text,SM_FONT,'left','middle');
  }
  /* the note lives inside the f" panel, so it only goes in when that panel has
     the room: at 560x380 it landed on the panel's own "2" tick label, and the
     label registry cannot dodge an axis tick because axes() does not register
     one.  The caption says the same thing at every size. */
  if(!L.narrow&&bD2.h>=60){
    /* the SPIKE, measured off the curve -- the earlier version printed the
       axis maximum, which is the range the panel was fitted to and not a
       height anything reaches */
    let pk=0;
    for(let i=0;i<S.d2.length;i++) pk=Math.max(pk,Math.abs(S.d2[i]));
    lab(ctx,W,H,bD2.x+6,bD2.y+11,'largest f″ here '+sigS(pk,4)
        +' = slope jump / Δx, Δx = '+DX,COL.dim,SM_FONT,'left','top');
  }
  drawStackCaption(ctx,L);
}

/* ---- view 4: the corners ------------------------------------------ */
function cornerCap(M){
  const R=M.ref, st=M.st;
  if(!R.corners.length)
    return {full:'The '+st.refShape+' has no corner anywhere. PhET calls the hill and the pedestal '
      +'"smooth transitions" and it means it: the hill is a Gaussian, and the pedestal’s edge is '
      +'exp(−u⁴), whose value is 1 and whose first three derivatives all vanish where it meets '
      +'the plateau, so only the fourth derivative jumps there. The largest step between neighbouring '
      +'cell slopes anywhere on this curve is '+sigS(maxStep(R.d),3)+', and it halves with the grid, '
      +'which a corner’s never does.',
      short:'The '+st.refShape+' has no corner: the largest slope step is '+sigS(maxStep(R.d),3)+'.'};
  const c=R.corners[clamp(st.cornerSel,0,R.corners.length-1)];
  return {full:'A corner is a point where the two one-sided limits of the difference quotient exist and '
      +'are different, so the derivative does not. Here they are '+fmt(c.left,4)+' from the left and '
      +fmt(c.right,4)+' from the right, a jump of '+fmt(c.jump,4)+'. The lower panel zooms on '
      +'±25 cells about '+VAR()+' = '+fmt(c.x,3)+' — that is '+sigf(50*DX,2)+' wide, a magnification of '
      +sigf(XLEN/(50*DX),3)+'× — with the two one-sided rays drawn in orange, and the second '
      +'derivative under them on a scale of its own (its peak, '
      +sigS(1/Math.max(1e-12,cornerZoomScale(R)),4)+', is drawn at 0.42 of the panel), because that '
      +'peak is the slope jump divided by Δx and means nothing on f’s axis. '
      +cornerExactness(R,c),
    short:'One-sided limits '+fmt(c.left,3)+' and '+fmt(c.right,3)+', jump '+fmt(c.jump,3)+'.'};
}
/* the two numbers quoted are the EXACT one-sided limits of the drawn polyline.
   Whether they are also the ideal shape's limits depends on the shape: on a
   triangle the cells either side are straight and they are exact, on a curved
   one the nearest clean cell sits about 1.5 dx from the corner and the reading
   is short by the curvature times that.  Quoting four decimals without saying
   which case you are in is quoting a number past its precision. */
function cornerExactness(R,c){
  const a=Math.max(c.a-2,0), b=Math.min(c.b+1,R.d.length-1);
  const curv=Math.max(Math.abs(R.d[Math.max(a,0)]-R.d[Math.max(a-1,0)]),
                      Math.abs(R.d[b]-R.d[Math.min(b+1,R.d.length-1)]))/DX;
  if(curv<1e-9)
    return 'The curve is straight on both sides here, so those two limits are exact — they are '
      +'read off cells that lie wholly on one side of the corner.';
  return 'The curve is CURVED on at least one side, so the clean cells sit about 1.5 Δx from the '
    +'corner and the readings fall short of the ideal shape’s limits by roughly '
    +sigS(curv*1.5*DX,2)+'. A corner’s position is known to one cell; its limits are not.';
}
function cornerZoomScale(R){
  let m=0;
  for(let i=0;i<R.d2.length;i++) m=Math.max(m,Math.abs(R.d2[i]));
  return m>0?1/m:1;
}
function drawCorner(ctx,W,H,M){
  const R=M.ref, st=M.st;
  const cap=cornerCap(M);
  const L=panelStack(ctx,W,H,3,cap.full,cap.short);
  const bF=L.bs[0], bD=L.bs[1], bZ=L.bs[2];
  const yF=rangeOf(R.f,1.0), yD=rangeOf(R.d,1.0);
  const mF=mapFor(bF,XMIN,XMAX,-yF,yF), mD=mapFor(bD,XMIN,XMAX,-yD,yD);
  GEO.view='corner'; GEO.fb=null; GEO.fmap=null; GEO.panels=[[bF,mF],[bD,mD]];

  if(st.grid){ unitGrid(ctx,bF,mF,1,tickStep(-yF,yF)); unitGrid(ctx,bD,mD,1,tickStep(-yD,yD)); }
  axesT(ctx,bF,XMIN,XMAX,-yF,yF,{});
  axesT(ctx,bD,XMIN,XMAX,-yD,yD,{});
  panelTitle(ctx,bF,cName('f')+'  —  '+st.refShape,COL.f);
  panelTitle(ctx,bD,cName('d'),COL.d);
  zeroLine(ctx,bF,mF); zeroLine(ctx,bD,mD);
  polyline(ctx,bF,XG,R.f,mF.xlo,mF.xhi,mF.ylo,mF.yhi,COL.f,2.0);
  plotRuns(ctx,bD,XMID,R.d,mD,COL.d,1.9,breakCells(R.corners),st.discont==='dashedLine');

  const sel=R.corners.length?clamp(st.cornerSel,0,R.corners.length-1):-1;
  R.corners.forEach((c,k)=>{
    const X=mF.X(c.x);
    if(X<bF.x-1||X>bF.x1+1) return;
    const on=(k===sel);
    ctx.strokeStyle=on?COL.warn:rgba(COL.warn,0.35);
    ctx.lineWidth=on?1.6:1;
    ctx.setLineDash([4,4]);
    ctx.beginPath(); ctx.moveTo(X,bF.y); ctx.lineTo(X,bF.y1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(mD.X(c.x),bD.y); ctx.lineTo(mD.X(c.x),bD.y1); ctx.stroke();
    ctx.setLineDash([]);
  });

  /* the zoom */
  if(sel<0){
    /* no corner to zoom on, so the panel answers the question instead: the
       STEP between neighbouring cell slopes, everywhere.  Repeating the
       derivative here (which the first draft did) is a panel that says
       nothing -- this one shows what "no jump" looks like as a number. */
    const sx=new Float64Array(NPTS-2), sy=new Float64Array(NPTS-2);
    let mx=0, mi=0;
    for(let i=1;i<NPTS-1;i++){
      sx[i-1]=XG[i]; sy[i-1]=Math.abs(R.d[i]-R.d[i-1]);
      if(sy[i-1]>mx){ mx=sy[i-1]; mi=i-1; }
    }
    const ytop=Math.max(mx*1.35,1e-9);
    const mZ=mapFor(bZ,XMIN,XMAX,0,ytop);
    axesT(ctx,bZ,XMIN,XMAX,0,ytop,xAxisOpt({yfmt:v=>sigf(v,2)}));
    panelTitle(ctx,bZ,'the step between neighbouring cell slopes',COL.d);
    polyline(ctx,bZ,sx,sy,mZ.xlo,mZ.xhi,mZ.ylo,mZ.yhi,COL.d,1.6);
    dot(ctx,clamp(mZ.X(sx[mi]),bZ.x,bZ.x1),clamp(mZ.Y(mx),bZ.y,bZ.y1),4,COL.live,'#fff',1.2);
    if(bZ.h>=60)
      lab(ctx,W,H,bZ.x+8,bZ.y+12,'largest step '+sigS(mx,3)+' at '+VAR()+' = '+fmt(sx[mi],3)
          +'  \u2014  a corner would put the whole jump into ONE step',COL.f,SM_FONT,'left','top');
  } else {
    const c=R.corners[sel];
    const half=25*DX;
    const xa=c.x-half, xb=c.x+half;
    let lo=1e9,hi=-1e9;
    for(let i=Math.max(0,c.i-26);i<=Math.min(NPTS-1,c.i+26);i++){ lo=Math.min(lo,R.f[i]); hi=Math.max(hi,R.f[i]); }
    const pad=Math.max(1e-6,(hi-lo)*0.35);
    const mZ=mapFor(bZ,xa,xb,lo-pad,hi+pad);
    axesT(ctx,bZ,xa,xb,lo-pad,hi+pad,xAxisOpt({nx:4}));
    panelTitle(ctx,bZ,'the corner, magnified '+sigf(XLEN/(2*half),3)+'×',COL.f);
    /* the second derivative on its own scale, drawn first so f sits over it */
    const sc=cornerZoomScale(R)*(hi+pad-lo+pad)*0.42;
    const zx=[], zy=[];
    for(let i=Math.max(1,c.i-26);i<=Math.min(NPTS-2,c.i+26);i++){ zx.push(XG[i]); zy.push(R.d2[i]*sc+(lo-pad*0.4)); }
    polyline(ctx,bZ,zx,zy,mZ.xlo,mZ.xhi,mZ.ylo,mZ.yhi,COL.dd,1.4);
    polyline(ctx,bZ,XG,R.f,mZ.xlo,mZ.xhi,mZ.ylo,mZ.yhi,COL.f,2.2);
    /* the one-sided rays: exactly the two limits, drawn from the corner */
    const y0=R.f[c.i];
    polyline(ctx,bZ,[xa,c.x],[y0-c.left*half,y0],mZ.xlo,mZ.xhi,mZ.ylo,mZ.yhi,COL.exact,1.6,[5,4]);
    polyline(ctx,bZ,[c.x,xb],[y0,y0+c.right*half],mZ.xlo,mZ.xhi,mZ.ylo,mZ.yhi,COL.exact,1.6,[5,4]);
    dot(ctx,mZ.X(c.x),mZ.Y(y0),4,COL.live,'#fff',1.2);
    lab(ctx,W,H,mZ.X(c.x)-10,bZ.y+13,'left '+fmt(c.left,3),COL.exact,SM_FONT,'right','top');
    lab(ctx,W,H,mZ.X(c.x)+10,bZ.y+13,'right '+fmt(c.right,3),COL.exact,SM_FONT,'left','top');
    /* only where the panel has room: on a 26 px panel the registry shifts this
       label down onto the panel's own x tick row, which is worse than not
       drawing it (the caption carries the same sentence at every size) */
    if(!L.narrow&&bZ.h>=60)
      lab(ctx,W,H,bZ.x+8,bZ.y+13,cName('dd')+', peak '+sigS(1/Math.max(1e-12,cornerZoomScale(R)),4)
          +', drawn at 0.42 of the panel',COL.dd,SM_FONT,'left','top');
  }
  drawStackCaption(ctx,L);
}

/* ---- view 5: the theorem ------------------------------------------ */
function ftcCap(M){
  const F=M.ftc;
  if(Math.max(F.e1,F.e2,F.ePhet)===0)
    return {full:'The curve is empty, so every one of these residuals is exactly zero and there is '
        +'nothing to measure: a flat line is its own integral\u2019s derivative in any arithmetic, and '
        +'PhET\u2019s pair returns it too, because the [1,2,1]/4 average of a constant is that constant. '
        +'Draw something on the derivative or the lab view and the two panels below fill in \u2014 the '
        +'first with rounding at 10\u207b\u00b9\u2075, the second with the O(\u0394x\u00b2) that '
        +'PhET\u2019s node-centred derivative of its trapezium integral costs.',
      short:'The curve is empty, so every residual is exactly zero: draw something.'};
  return {full:'The top panel has three curves on it and you can see one, because differentiating the '
      +'integral of f returns f and integrating the derivative of f returns f minus f(0). Not to a '
      +'tolerance — the largest residual anywhere on the grid is '+sigS(Math.max(F.e1,F.e2),2)
      +', which is floating-point rounding over '+(NPTS-1)+' cells. The middle panel is those residuals '
      +'multiplied by 10¹⁵ so they can be seen at all. The bottom panel is what PhET’s own '
      +'pair does on the same curve: its node-centred derivative of its trapezium integral is exactly the '
      +'[1,2,1]/4 smoothing of f (that identity holds to '+sigS(F.e3,2)+' here), which differs from f by '
      +sigS(F.ePhet,3)+'. Second order in Δx, perfectly reasonable, and not zero.',
    short:'d/dx ∫f = f and ∫f′ = f − f(0), residual '+sigS(Math.max(F.e1,F.e2),2)+'.'};
}
function drawFtc(ctx,W,H,M){
  const S=M.live, F=M.ftc, st=M.st;
  const cap=ftcCap(M);
  const L=panelStack(ctx,W,H,3,cap.full,cap.short);
  const b1=L.bs[0], b2=L.bs[1], b3=L.bs[2];
  const m1=mapFor(b1,XMIN,XMAX,-M.yF,M.yF);
  GEO.view='ftc'; GEO.fb=b1; GEO.fmap=m1; GEO.panels=[[b1,m1]];

  if(st.grid) unitGrid(ctx,b1,m1,1,tickStep(-M.yF,M.yF));
  axesT(ctx,b1,XMIN,XMAX,-M.yF,M.yF,{});
  panelTitle(ctx,b1,'f, and the two round trips',COL.f);
  zeroLine(ctx,b1,m1);
  polyline(ctx,b1,XG,S.f,m1.xlo,m1.xhi,m1.ylo,m1.yhi,COL.f,2.6);
  polyline(ctx,b1,XMID,F.fwd,m1.xlo,m1.xhi,m1.ylo,m1.yhi,COL.exact,1.4,[6,4]);
  const backShift=new Float64Array(NPTS);
  for(let i=0;i<NPTS;i++) backShift[i]=F.back[i]+S.f[0];
  polyline(ctx,b1,XG,backShift,m1.xlo,m1.xhi,m1.ylo,m1.yhi,COL.I,1.2,[2,4]);
  legendAuto(ctx,b1,[[COL.f,'f'],[COL.exact,'d/d'+VAR()+' ∫f, at the midpoints'],
                     [COL.I,'∫f′ + f(0)']]);

  const sc=1e15;
  let ym=1e-30;
  for(let i=0;i<NPTS;i++) ym=Math.max(ym,Math.abs(F.r1[i]*sc));
  for(let i=0;i<NPTS-1;i++) ym=Math.max(ym,Math.abs(F.r2[i]*sc));
  ym=Math.max(ym*1.2,1);
  const m2=mapFor(b2,XMIN,XMAX,-ym,ym);
  axesT(ctx,b2,XMIN,XMAX,-ym,ym,{});
  panelTitle(ctx,b2,'the two residuals, ×10¹⁵',COL.dim);
  zeroLine(ctx,b2,m2);
  const r1s=new Float64Array(NPTS), r2s=new Float64Array(NPTS-1);
  for(let i=0;i<NPTS;i++) r1s[i]=F.r1[i]*sc;
  for(let i=0;i<NPTS-1;i++) r2s[i]=F.r2[i]*sc;
  polyline(ctx,b2,XG,r1s,m2.xlo,m2.xhi,m2.ylo,m2.yhi,COL.I,1.2);
  polyline(ctx,b2,XMID,r2s,m2.xlo,m2.xhi,m2.ylo,m2.yhi,COL.exact,1.2);
  lab(ctx,W,H,b2.x1-8,b2.y+12,'one ulp of f is '+sigS(2.22e-16*Math.max(1,M.yF)*sc,2)+' on this scale',
      COL.dim,SM_FONT,'right','top');

  /* an axis fitted to a residual that is identically zero degenerates into
     five ticks all reading 0 (and one reading -0); give it a real range and
     say what is going on instead */
  const flat=(F.ePhet===0);
  const yp=flat?1:F.ePhet*1.25;
  const m3=mapFor(b3,XMIN,XMAX,-yp,yp);
  axesT(ctx,b3,XMIN,XMAX,-yp,yp,xAxisOpt());
  panelTitle(ctx,b3,'PhET’s pair: its D(∫f) − f',COL.phet);
  zeroLine(ctx,b3,m3);
  const pr=new Float64Array(NPTS);
  for(let i=1;i<NPTS-1;i++) pr[i]=F.pd[i]-S.f[i];
  pr[0]=pr[1]; pr[NPTS-1]=pr[NPTS-2];
  polyline(ctx,b3,XG,pr,m3.xlo,m3.xhi,m3.ylo,m3.yhi,COL.phet,1.5);
  lab(ctx,W,H,b3.x+8,b3.y+12,
      flat?'identically zero on a flat curve: the [1,2,1]/4 average of a constant IS that constant'
          :('= (Δ'+VAR()+')² f″/4; its largest value here, '+sigS(F.ePhet,3)
             +', is at a corner, where f″ is not a function'),
      COL.phet,SM_FONT,'left','top');
  drawStackCaption(ctx,L);
}

/* ---- view 6: the grid --------------------------------------------- */
function gridCurveErr(){
  return memo('griderr',refKey()+'|'+ST.gridMult,()=>{
    const mult=GRID_MULTS[clamp(ST.gridMult,0,GRID_MULTS.length-1)];
    const n=Math.round((NPTS-1)*mult)+1;
    const g=gridOf(n);
    const out=manipulate(new Float64Array(n),new Uint8Array(n),ST.refShape,ST.refW,ST.refX,ST.refY,g);
    const cf=shapeClosed(ST.refShape,ST.refW,ST.refX,ST.refY,g);
    const d=derivOf(out.f,n,g.dx), F=integOf(out.f,n,g.dx), Gx=cumExact(cf,g);
    const xm=new Float64Array(n-1), ed=new Float64Array(n-1);
    for(let i=0;i<n-1;i++){ xm[i]=g.x[i]+g.dx/2; ed[i]=d[i]-cf.gp(xm[i]); }
    const eF=new Float64Array(n);
    for(let i=0;i<n;i++) eF[i]=F[i]-Gx[i];
    return {n,dx:g.dx,xm,ed,eF,x:g.x,f:out.f,cf};
  });
}
/* the caption has to follow the SHAPE.  "both fall by a factor of four" is
   simply false for the triangle and the parabola -- on those the cell
   derivative is exact and what is left is two junction cells -- and a caption
   that contradicts the picture beside it is the defect this collection keeps
   finding by looking at the PNG. */
function gridCap(M){
  const rows=M.study, st=M.st;
  const r=rows[clamp(st.gridMult,0,rows.length-1)];
  const head='The top panel is the '+st.refShape+' as the sim stores it, with the closed form drawn '
    +'over it; they are the same curve. The middle panel is the error the grid costs: the cell '
    +'derivative minus g′ at the cell midpoints, at '+(r.n-1)+' cells. The bottom panel is that '
    +'error against the number of cells, magenta for the derivative and cyan for the integral, with a '
    +'dashed slope −2 guide. PhET’s own grid, '+(NPTS-1)+' cells, carries the two rings. ';
  const exact=(st.refShape==='triangle')
    ? 'This shape is piecewise LINEAR, so the cell derivative is exact: the magenta line sits at '
      +'10⁻¹³ and the two spikes in the middle panel are the only departures — the '
      +'cells the junctions fall inside. The integral error is those same two cells, worth '
      +'sδ(Δx−δ)/2 each, so it does not fall smoothly at all: it collapses to '
      +'rounding at 2500 cells, where the junctions land exactly on nodes.'
    : (st.refShape==='parabola')
      ? 'This shape is QUADRATIC, so a cell-centred difference is exact on it and the trapezium error '
        +'is the Euler–Maclaurin term with nothing left over. What the middle panel shows is the '
        +'two junction cells, and neither line here is a convergence rate.'
      : 'Both lines fall by a factor of four for every halving of Δx, which is the claim worth '
        +'making — the number itself means nothing without the rate.';
  return {full:head+exact,
    short:'The error of both operators against the number of cells, with a slope −2 guide.'};
}
function drawGrid(ctx,W,H,M){
  const R=M.ref, st=M.st, rows=M.study;
  const E=gridCurveErr();
  const cap=gridCap(M);
  const L=panelStack(ctx,W,H,3,cap.full,cap.short);
  const b1=L.bs[0], b2=L.bs[1], b3=L.bs[2];
  GEO.view='grid'; GEO.fb=null; GEO.fmap=null; GEO.panels=[];

  const yF=rangeOf(R.f,1.0);
  const m1=mapFor(b1,XMIN,XMAX,-yF,yF);
  if(st.grid) unitGrid(ctx,b1,m1,1,tickStep(-yF,yF));
  axesT(ctx,b1,XMIN,XMAX,-yF,yF,{});
  panelTitle(ctx,b1,st.refShape+': stored, and its closed form',COL.f);
  zeroLine(ctx,b1,m1);
  const gx=[], gy=[];
  for(let i=0;i<NPTS;i+=3){ gx.push(XG[i]); gy.push(R.cf.g(XG[i])); }
  polyline(ctx,b1,XG,R.f,m1.xlo,m1.xhi,m1.ylo,m1.yhi,COL.f,2.4);
  polyline(ctx,b1,gx,gy,m1.xlo,m1.xhi,m1.ylo,m1.yhi,COL.exact,1.3,[6,4]);
  legendAuto(ctx,b1,[[COL.f,'what the sim stores'],[COL.exact,'the closed form']]);

  let em=1e-30;
  for(let i=0;i<E.ed.length;i++) em=Math.max(em,Math.abs(E.ed[i]));
  em=Math.max(em*1.2,1e-12);
  const m2=mapFor(b2,XMIN,XMAX,-em,em);
  axesT(ctx,b2,XMIN,XMAX,-em,em,{yfmt:v=>v===0?'0':sigS(v,1)});
  panelTitle(ctx,b2,'f′ − g′ at the cell midpoints, '+(E.n-1)+' cells',COL.d);
  zeroLine(ctx,b2,m2);
  polyline(ctx,b2,E.xm,E.ed,m2.xlo,m2.xhi,m2.ylo,m2.yhi,COL.d,1.4);
  lab(ctx,W,H,b2.x1-8,b2.y+12,'Δ'+VAR()+' = '+sigS(E.dx,3),COL.dim,SM_FONT,'right','top');

  const lx=rows.map(r=>Math.log10(r.n-1));
  const ly1=rows.map(r=>Math.log10(Math.max(r.ed,1e-18)));
  const ly2=rows.map(r=>Math.log10(Math.max(r.eF,1e-18)));
  const xa=Math.min.apply(null,lx)-0.15, xb=Math.max.apply(null,lx)+0.15;
  const ya=Math.min(Math.min.apply(null,ly1),Math.min.apply(null,ly2))-0.4;
  const yb=Math.max(Math.max.apply(null,ly1),Math.max.apply(null,ly2))+0.4;
  const m3=mapFor(b3,xa,xb,ya,yb);
  axesT(ctx,b3,xa,xb,ya,yb,{xlab:'cells',
    xticks:lx,
    xfmt:v=>String(Math.round(Math.pow(10,v))),
    yticks:logTicks(Math.pow(10,ya),Math.pow(10,yb)).map(Math.log10),
    yfmt:v=>'10'+supNum(Math.round(v))});
  panelTitle(ctx,b3,'error against cells, log–log',COL.dim);
  /* the slope -2 guide, anchored on PhET's own grid */
  const iP=GRID_MULTS.indexOf(1);
  const gy0=ly1[iP], gx0=lx[iP];
  polyline(ctx,b3,[xa,xb],[gy0-2*(xa-gx0),gy0-2*(xb-gx0)],xa,xb,ya,yb,COL.struct,1,[4,4]);
  polyline(ctx,b3,lx,ly1,xa,xb,ya,yb,COL.d,1.9);
  polyline(ctx,b3,lx,ly2,xa,xb,ya,yb,COL.I,1.9);
  for(let k=0;k<rows.length;k++){
    dot(ctx,m3.X(lx[k]),m3.Y(ly1[k]),3,COL.d,null,0);
    dot(ctx,m3.X(lx[k]),m3.Y(ly2[k]),3,COL.I,null,0);
  }
  dot(ctx,m3.X(lx[iP]),m3.Y(ly1[iP]),5.5,null,COL.live,2);
  dot(ctx,m3.X(lx[iP]),m3.Y(ly2[iP]),5.5,null,COL.live,2);
  legendAuto(ctx,b3,[[COL.d,'max |f′ − g′|'],[COL.I,'max |∫f − G|'],
                     [COL.struct,'slope −2']]);
  /* bottom-LEFT: on a falling log-log pair the bottom right is where both
     curves end up, and the label sat on the cyan one */
  lab(ctx,W,H,b3.x+8,b3.y1-10,'the rings are PhET’s '+(NPTS-1)+' cells',COL.live,SM_FONT,'left','bottom');
  drawStackCaption(ctx,L);
}
function supNum(n){
  const S={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴',
           '5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
  return String(n).split('').map(c=>S[c]||c).join('');
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  POLY_SEGS=[]; LABELS=[]; LEGEND_RECTS=[];
  GEO.view=null; GEO.fb=null; GEO.fmap=null; GEO.scrubs=[]; GEO.panels=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  const v=M.view;
  if(v==='deriv') drawDeriv(ctx,W,H,M);
  else if(v==='integ') drawInteg(ctx,W,H,M);
  else if(v==='lab') drawLab(ctx,W,H,M);
  else if(v==='corner') drawCorner(ctx,W,H,M);
  else if(v==='ftc') drawFtc(ctx,W,H,M);
  else drawGrid(ctx,W,H,M);
}

function makeScene(canvas){
  const S={st:ST,W:1200,H:760,canvas,
    model:buildModel,
    draw(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); },
    step(){ return false; },              /* nothing here animates: the sim is arithmetic */
    drag:null,
    /* the scrubbers first, then the curve: a press inside the f panel that
       lands on a scrubber must move the scrubber, not redraw the curve */
    hitScrub(x,y){
      let best=null;
      for(const s of GEO.scrubs){
        if(y<s.b.y-6||y>s.b.y1+6) continue;
        const dd=Math.abs(x-s.X);
        if(dd<=9&&(!best||dd<best.d)) best={d:dd,kind:s.kind,b:s.b};
      }
      return best;
    },
    setScrub(kind,x,b){
      const t=clamp((x-b.x)/b.w,0,1);
      const v=XMIN+XLEN*t;
      const key=kind==='T'?'xT':(kind==='A'?'xA':'xR');
      if(Math.abs(ST[key]-v)<1e-12) return false;
      ST[key]=v;
      return true;
    },
    pointer(kind,x,y){
      if(kind==='up'){
        const was=S.drag;
        S.drag=null;
        return !!was;
      }
      if(kind==='down'){
        S.drag=null;
        const hs=S.hitScrub(x,y);
        if(hs){ S.drag={what:'scrub',kind:hs.kind,b:hs.b}; return S.setScrub(hs.kind,x,hs.b); }
        if(GEO.fb&&GEO.fmap&&x>=GEO.fb.x-4&&x<=GEO.fb.x1+4&&y>=GEO.fb.y-4&&y<=GEO.fb.y1+4){
          saveCurve();
          const wx=clamp(GEO.fmap.wx(x),XMIN,XMAX), wy=GEO.fmap.wy(y);
          /* the map is captured HERE and reused for the whole gesture: the
             panel's y range is fitted to the curve, so re-reading it every
             move would re-base the drag against a picture the drag itself
             changed */
          S.drag={what:'curve',px:wx,py:wy,map:GEO.fmap};
          return S.applyAt(wx,wy,null,null);
        }
        return false;
      }
      if(!S.drag) return false;
      if(S.drag.what==='scrub') return S.setScrub(S.drag.kind,x,S.drag.b);
      if(!S.drag.map) return false;
      const wx=clamp(S.drag.map.wx(x),XMIN,XMAX), wy=S.drag.map.wy(y);
      const px=S.drag.px, py=S.drag.py;
      S.drag.px=wx; S.drag.py=wy;
      return S.applyAt(wx,wy,px,py);
    },
    /* one shape laid down from the SAVED curve, exactly as PhET does it: the
       snapshot is taken once per drag and every move re-applies the shape to
       it, so a drag moves one hill rather than stacking hundreds. */
    applyAt(x,y,px,py){
      const yy=clamp(y,Y_MIN,Y_MAX);       /* PhET: CURVE_MANIPULATION_Y_RANGE */
      if(ST.mode==='freeform'){
        const f=activeF().slice(), c=activeC().slice();
        if(px===null||px===undefined) freeformStroke(f,c,x,yy,null,null);
        else freeformStroke(f,c,x,yy,px,clamp(py,Y_MIN,Y_MAX));
        if(px===null||px===undefined){
          const out=manipulate(f,c,'hill',FREEFORM_W,x,yy);
          setActive(out.f,out.c);
        } else setActive(f,c);
        return true;
      }
      applyShape(ST.mode,ST.width,x,yy);
      return true;
    },
    /* the panel button: the same operation without a pointer, so the sim is
       usable (and testable) from the controls alone */
    place(){
      saveCurve();
      if(ST.mode==='freeform'){
        const f=activeF().slice(), c=activeC().slice();
        const out=manipulate(f,c,'hill',FREEFORM_W,ST.placeX,ST.height);
        setActive(out.f,out.c);
      } else applyShape(ST.mode,ST.width,ST.placeX,ST.height);
    }};
  return S;
}
