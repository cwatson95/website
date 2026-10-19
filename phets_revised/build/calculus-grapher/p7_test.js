/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/calculus-grapher/refvals.txt, the      *
 *  printed output of derive.py (numpy, scipy.special.erf,             *
 *  scipy.special.gammainc, scipy.integrate.quad), read in full        *
 *  through make_refs.py.                                              *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),
    name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  const cSave=CURVE.slice(), cfSave=CFLAG.slice(), pSave=PRED.slice(), pfSave=PFLAG.slice();
  function restore(){
    Object.assign(ST,stSave);
    CURVE=cSave.slice(); CFLAG=cfSave.slice();
    PRED=pSave.slice(); PFLAG=pfSave.slice();
    SAVED=CURVE.slice(); SFLAG=CFLAG.slice();
    UNDO=[]; CVER++;
  }
  function withState(over,fn){
    Object.assign(ST,DEFAULTS,over||{});
    const d=buildDefaultCurve();
    CURVE=d.f; CFLAG=d.c;
    if(over&&over._curve){ CURVE=over._curve.f; CFLAG=over._curve.c; }
    PRED=new Float64Array(NPTS); PFLAG=new Uint8Array(NPTS);
    if(over&&over._pred){ PRED=over._pred; }
    SAVED=CURVE.slice(); SFLAG=CFLAG.slice(); UNDO=[]; CVER++;
    try{ return fn(); } finally{ restore(); }
  }
  const zero=()=>new Float64Array(NPTS);
  const zeroC=()=>new Uint8Array(NPTS);
  const maxAbs=a=>{ let m=0; for(let i=0;i<a.length;i++) m=Math.max(m,Math.abs(a[i])); return m; };
  const maxDiff=(a,b)=>{ let m=0; const n=Math.min(a.length,b.length);
    for(let i=0;i<n;i++) m=Math.max(m,Math.abs(a[i]-b[i])); return m; };
  /* a deterministic generator, so a random-curve test is reproducible */
  function rng(seed){ let s=seed>>>0;
    return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }

  /* ---------- 0. the shared helpers cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,
     'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(mix('#070b18',mix('#b8ec4c','#cd35c4',0.5),1)!=='rgb(0,0,0)','mix() output is a legal mix() input');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,
       'polyline() clips a segment whose BOTH ends are outside the box');
    POLY_SEGS=[]; }
  ok(logTicks(0,10).length===0,'logTicks refuses a non-positive bound instead of looping for ever');

  /* ---------- 1. PhET's constants ---------- */
  eq(XMIN,REF.XMIN,"PhET's x range starts at (derive)");
  eq(XMAX,REF.XMAX,"PhET's x range ends at (derive)");
  eq(NPTS,REF.NPTS,"PhET's numberOfPoints (derive)");
  close(DX,REF.DX,1e-18,'and so dx (derive)');
  eq(TYPICAL_Y,REF.TYPICAL_Y,"PhET's TYPICAL_Y (derive)");
  close(SMOOTH_SIGMA,REF.SMOOTH_SIGMA,1e-18,"PhET's smoothingStandardDeviation (derive)");
  close(EDGE_SLOPE,REF.EDGE_SLOPE,1e-15,"PhET's edgeSlopeFactor (derive)");
  eq(MAX_TILT,REF.MAX_TILT,"PhET's maxTilt (derive)");
  eq(W_MIN,REF.W_MIN,"PhET's minimum shape width (derive)");
  eq(W_MAX,REF.W_MAX,"PhET's maximum shape width (derive)");
  eq(W_DEF,REF.W_DEF,"PhET's default shape width (derive)");
  eq(Y_MIN,REF.Y_MIN,"PhET's curve-manipulation y range, low (derive)");
  eq(Y_MAX,REF.Y_MAX,"PhET's curve-manipulation y range, high (derive)");
  eq(SLOPE_MAX,REF.SLOPE_MAX,"PhET's tangent gauge range (derive)");
  eq(AREA_MAX,REF.AREA_MAX,"PhET's area gauge range (derive)");
  eq(MAX_UNDO,REF.MAX_UNDO,"PhET's undo depth (derive)");
  eq(FREEFORM_W,REF.FREEFORM_W,"PhET's freeform click width (derive)");
  eq(BLEND_EPS,1e-8,"PhET's blend threshold");
  eq(SMOOTH_W,0.999,"PhET's smooth-point threshold");
  eq(REGION_ZERO,0.001,"PhET's isRegionZero tolerance");
  /* the grid itself */
  close(XG[0],XMIN,0,'the first node is at x = 0');
  close(XG[NPTS-1],XMAX,1e-12,'the last node is at x = 10');
  close(XMID[0],XMIN+DX/2,1e-18,'the first cell centre is half a cell in');
  eq(XMID.length,NPTS-1,'there is one cell fewer than there are nodes');
  eq(idxAt(3.2),400,'idxAt rounds to the nearest node');
  eq(idxAt(-5),0,'idxAt clamps below');
  eq(idxAt(99),NPTS-1,'idxAt clamps above');
  eq(cellAt(XMAX),NPTS-2,'cellAt at the right edge is the last cell');

  /* ---------- 2. the fundamental theorem, on random curves ---------- */
  { const R=rng(20260922);
    let e1=0,e2=0,e3=0;
    for(let t=0;t<6;t++){
      const f=new Float64Array(NPTS);
      for(let i=0;i<NPTS;i++) f[i]=0.7*(2*R()-1)+1.3*Math.sin(3*XG[i]);
      const d=derivOf(f), F=integOf(f);
      const back=integCells(d), fwd=derivOf(F);
      for(let i=0;i<NPTS;i++) e1=Math.max(e1,Math.abs(back[i]-(f[i]-f[0])));
      for(let i=0;i<NPTS-1;i++) e2=Math.max(e2,Math.abs(fwd[i]-0.5*(f[i]+f[i+1])));
      const g=new Float64Array(NPTS-1);
      for(let i=0;i<NPTS-1;i++) g[i]=2*R()-1;
      e3=Math.max(e3,maxDiff(derivOf(integCells(g)),g));
    }
    ok(e1<REF.FTC_BACK_TOL,'FTC: integrating the derivative returns f - f(0) ['+e1.toExponential(2)+']');
    ok(e2<REF.FTC_BACK_TOL,'FTC: differentiating the integral returns f at the cell midpoints ['
       +e2.toExponential(2)+']');
    ok(e3<REF.FTC_BACK_TOL,'FTC: and the cell integral inverts the cell derivative ['+e3.toExponential(2)+']');
    ok(e1>0&&e2>0,'... and both residuals are nonzero, so the test is measuring floating point, not a no-op');
  }
  /* PhET's pair is NOT inverse, and this is the identity it satisfies instead */
  { const R=rng(7777);
    let worst=0, away=0;
    for(let t=0;t<4;t++){
      const f=new Float64Array(NPTS);
      for(let i=0;i<NPTS;i++) f[i]=0.9*(2*R()-1);
      const pd=phetDeriv(integOf(f));
      for(let i=1;i<NPTS-1;i++){
        worst=Math.max(worst,Math.abs(pd[i]-0.25*(f[i-1]+2*f[i]+f[i+1])));
        away=Math.max(away,Math.abs(pd[i]-f[i]));
      }
    }
    ok(worst<REF.PHET_SMOOTHER_TOL,
       'PhET: its central difference of its trapezium integral IS the [1,2,1]/4 smoothing ['
       +worst.toExponential(2)+']');
    ok(away>0.1,'... and on a rough curve that is a long way from f ('+fmt(away,3)+')');
  }

  /* ---------- 3. erf and the quadrature ---------- */
  close(erf(0.25),REF.ERF_25,3e-15,'erf(0.25) (scipy)');
  close(erf(1.0),REF.ERF_100,3e-15,'erf(1.00) (scipy)');
  close(erf(2.0),REF.ERF_200,3e-15,'erf(2.00) (scipy)');
  close(erf(3.5),REF.ERF_350,3e-15,'erf(3.50) (scipy)');
  close(erf(-1.0),-REF.ERF_100,3e-15,'erf is odd');
  eq(erf(7),1,'erf saturates past 6, where 1 is right to 2e-17');
  { let s=0; for(let i=0;i<GL.ws.length;i++) s+=GL.ws[i];
    close(s,2,1e-14,'the Gauss-Legendre weights sum to the length of [-1,1]');
    let worst=0;
    for(let k=0;k<=2*GL.xs.length-1;k++){
      const got=quadGL(x=>Math.pow(x,k),0,1,1);
      worst=Math.max(worst,Math.abs(got-1/(k+1)));
    }
    ok(worst<1e-14,'... and a '+GL.xs.length+'-point rule is exact to degree '+(2*GL.xs.length-1)
       +' ['+worst.toExponential(2)+']');
    /* the falsifier: a 12-point rule is NOT exact on a function that is not a
       polynomial, and Runge's 1/(1+25x^2) over [-1,1] is the standard one.
       x^24 is the wrong falsifier -- its one-panel error is 5e-15, below the
       noise of the exactness test itself, so it would have proved nothing. */
    const runge=x=>1/(1+25*x*x), rExact=2*Math.atan(5)/5;
    ok(Math.abs(quadGL(runge,-1,1,1)-rExact)>1e-3,
       '... and NOT exact on Runge in one panel ['+fmt(quadGL(runge,-1,1,1)-rExact,5)+']');
    ok(Math.abs(quadGL(runge,-1,1,8)-rExact)<1e-13,
       '... while eight panels of it reach 1e-13, which is what cumExact leans on'); }

  /* ---------- 4. the five shapes against their closed forms ---------- */
  const SHAPES=[['hill',W_DEF,3.0,1.5],['triangle',W_DEF,4.0,1.5],['pedestal',3.0,5.0,1.2],
                ['parabola',2.5,6.0,-1.4],['sinusoid',2.0,5.0,1.0]];
  for(const [mode,w,x0,y] of SHAPES){
    const out=manipulate(zero(),zeroC(),mode,w,x0,y);
    const cf=shapeClosed(mode,w,x0,y);
    const d=derivOf(out.f), F=integOf(out.f), Gx=cumExact(cf,GRID);
    /* the two routes to the exact integral must agree where an elementary
       antiderivative exists; the pedestal has only the quadrature */
    if(mode!=='pedestal'){
      let worst=0;
      for(let i=0;i<NPTS;i+=17) worst=Math.max(worst,Math.abs(Gx[i]-cf.G(XG[i])));
      ok(worst<1e-12,mode+': Gauss-Legendre and the elementary antiderivative agree ['
         +worst.toExponential(2)+']');
    }
    let ed=0,eF=0;
    for(let i=0;i<NPTS-1;i++){
      const xm=XMID[i];
      let skip=Math.abs(cf.g(xm))<=1e-6*Math.abs(y);
      for(const b of cf.breaks) if(Math.abs(xm-b)<=2*DX) skip=true;
      if(!skip) ed=Math.max(ed,Math.abs(d[i]-cf.gp(xm)));
    }
    for(let i=0;i<NPTS;i++){
      let skip=false;
      for(const b of cf.breaks) if(Math.abs(XG[i]-b)<=2*DX) skip=true;
      if(!skip) eF=Math.max(eF,Math.abs(F[i]-Gx[i]));
    }
    rel(ed,REF['ERR_D_'+mode.toUpperCase()],2e-6,mode+": the derivative's error at PhET's grid (derive)");
    rel(eF,REF['ERR_I_'+mode.toUpperCase()],2e-6,mode+": the integral's error at PhET's grid (derive)");
    /* the sim's own value at the centre, and the total signed area */
    close(out.f[idxAt(x0)],REF['REFSHAPE_'+mode.toUpperCase()+'_PEAK'],1e-12,
          mode+' reaches its set height at its centre (derive)');
    close(F[NPTS-1],REF['REFSHAPE_'+mode.toUpperCase()+'_AREA'],1e-12,
          mode+': the total signed area the sim computes (derive)');
    rel(F[NPTS-1],REF['REFSHAPE_'+mode.toUpperCase()+'_AREA_EXACT'],2e-5,
        mode+': ... against the closed form for it (derive)');
  }
  /* the two shapes on which the operators are EXACT */
  { const out=manipulate(zero(),zeroC(),'triangle',W_DEF,4.0,1.5);
    const cf=shapeClosed('triangle',W_DEF,4.0,1.5), d=derivOf(out.f);
    let worst=0;
    for(let i=0;i<NPTS-1;i++){
      let skip=false;
      for(const b of cf.breaks) if(Math.abs(XMID[i]-b)<=1.01*DX) skip=true;
      if(!skip) worst=Math.max(worst,Math.abs(d[i]-cf.gp(XMID[i])));
    }
    ok(worst<1e-12,'a piecewise-LINEAR curve: the cell derivative is exact ['+worst.toExponential(2)+']');
    rel(worst,REF.TRI_D_EXACT,0.5,'... to the residual derive.py measured (derive)');
    const F=integOf(out.f);
    let wI=0;
    for(let i=0;i<NPTS;i++) wI=Math.max(wI,Math.abs(F[i]-cf.G(XG[i])));
    close(wI,REF.TRI_I_JUNCTION,1e-12,'the triangle keeps 1.6e-5 against the IDEAL triangle (derive)');
    ok(wI<=REF.TRI_I_BOUND*1.001,'... and that is the junction-cell bound 2 s dx^2 / 8, not a quadrature error');
  }
  { const w=2.5, x0=6.0, y=-1.4;
    const out=manipulate(zero(),zeroC(),'parabola',w,x0,y);
    const cf=shapeClosed('parabola',w,x0,y), d=derivOf(out.f), F=integOf(out.f);
    let worst=0;
    for(let i=0;i<NPTS-1;i++){
      let skip=false;
      for(const b of cf.breaks) if(Math.abs(XMID[i]-b)<=1.01*DX) skip=true;
      if(!skip) worst=Math.max(worst,Math.abs(d[i]-cf.gp(XMID[i])));
    }
    ok(worst<1e-12,'a QUADRATIC: the cell-centred difference is exact ['+worst.toExponential(2)+']');
    const ia=idxAt(REF.PAR_XA), ib=idxAt(REF.PAR_XB);
    const trap=F[ib]-F[ia], exact=cf.G(XG[ib])-cf.G(XG[ia]);
    close(trap-exact,REF.PAR_TRAP_ERR,1e-15,
          'the parabola trapezium error over [5.4, 6.4] (derive)');
    const em=DX*DX/12*(cf.gp(XG[ib])-cf.gp(XG[ia]));
    close(em,REF.PAR_EM_TERM,1e-15,'... equals +dx^2/12 [g\'(b) - g\'(a)] (derive)');
    close(trap-exact,em,1e-15,'... to 1e-15, because the expansion TERMINATES on a quadratic');
  }

  /* ---------- 5. the discretisation rate ---------- */
  for(const [mode,w,x0,y,key] of [['hill',W_DEF,3.0,1.5,'RATE_HILL'],
                                  ['sinusoid',2.0,5.0,1.0,'RATE_SINUSOID'],
                                  ['pedestal',3.0,5.0,1.2,'RATE_PEDESTAL']]){
    const a=gridError(mode,w,x0,y,(NPTS-1)*2+1);
    const b=gridError(mode,w,x0,y,(NPTS-1)*4+1);
    const r=a.ed/b.ed;
    rel(r,REF[key],1e-3,mode+': halving dx quarters the derivative error (derive)');
    ok(Math.abs(r-4)<0.31,'... which is second order, not first ('+fmt(r,4)+')');
    const rI=a.eF/b.eF;
    ok(Math.abs(rI-4)<0.6,mode+': and the integral error is second order too ('+fmt(rI,4)+')');
  }

  /* ---------- 6. corners, and the one-sided limits ---------- */
  { const w=W_DEF, x0=4.0, y=1.5;
    const out=manipulate(zero(),zeroC(),'triangle',w,x0,y);
    const d=derivOf(out.f), i0=idxAt(x0);
    close(d[i0-1],REF.TRI_SLOPE,1e-12,'triangle: the one-sided limit from the LEFT of the apex (derive)');
    close(d[i0],-REF.TRI_SLOPE,1e-12,'triangle: and from the RIGHT (derive)');
    close(d[i0-1]-d[i0],2*REF.TRI_SLOPE,1e-12,'... so the jump is twice the slope, and no value exists there');
    /* the second-difference spike: its INTEGRAL is the jump, exactly, because
       the sum telescopes.  This is the honest statement about a delta. */
    const d2=deriv2Of(out.f);
    let area=0;
    for(let i=i0-40;i<=i0+40;i++) area+=d2[i]*DX;
    close(area,REF.TRI_D2_AREA,1e-12,'int f" over 81 nodes about the apex is the slope jump (derive)');
    close(area,d[i0+40]-d[i0-41],1e-12,'... which is exactly what the telescoping sum says');
    close(maxAbs(d2),2*REF.TRI_SLOPE/DX,1e-9,'and the spike HEIGHT is that jump over dx');
    /* the junctions */
    /* the end convention has to be probed on a curve that is CURVED at the
       ends: on the triangle both ends are flat, so "d2[0] === d2[1]" holds
       whether the code copies the neighbour or writes a zero, and the mutant
       that writes a zero survived a 73-mutant sweep on exactly that. */
    { const wide=manipulate(zero(),zeroC(),'sinusoid',5.0,5.0,1.0);
      const dw=deriv2Of(wide.f);
      close(dw[0],REF.WIDE_SIN_D2_0,1e-9,'f" at the first node of a full-width sinusoid (derive)');
      close(dw[NPTS-1],REF.WIDE_SIN_D2_END,1e-9,'... and at the last (derive)');
      ok(Math.abs(dw[0])>0.01,'... and neither is zero, so "copies its neighbour" is being tested');
      ok(dw[0]===dw[1]&&dw[NPTS-1]===dw[NPTS-2],
         '... which is what they are: the neighbour, not an invented one'); }
    const cl=cornerList(out.c,d,24);
    ok(cl.length===3,'a triangle laid on an empty curve has three corners: apex and two junctions ['
       +cl.length+']');
    /* the apex is the middle one, and cornerList must read the two CLEAN cells
       either side of the flagged pair -- not an offset picked to suit it */
    { const ap=cl[1];
      eq(ap.a,i0,'the apex corner starts at the node PhET flagged');
      eq(ap.b,i0+1,'... and spans the pair it flagged');
      close(ap.left,REF.TRI_SLOPE,1e-12,'... so its left limit is the cell ending at that node');
      close(ap.right,-REF.TRI_SLOPE,1e-12,'... and its right limit the cell starting at the next');
      close(ap.jump,-2*REF.TRI_SLOPE,1e-12,'... and the jump is the difference'); }
    close(cl[0].x,REF.TRI_JUNCTION_L,2*DX,'the left junction sits where y/s says (derive)');
    close(cl[2].x,REF.TRI_JUNCTION_R,2*DX,'and the right one (derive)');
  }
  { const w=2.5, x0=6.0, y=-1.4;
    const out=manipulate(zero(),zeroC(),'parabola',w,x0,y);
    const d=derivOf(out.f);
    const jl=idxAt(REF.PAR_JUNCTION_L);
    close(Math.abs(d[jl+1]-d[jl-2]),REF.PAR_JUMP_MEAS,1e-9,
          'parabola: the jump measured across the left junction (derive)');
    ok(Math.abs(d[jl+1]-d[jl-2])<REF.PAR_JUMP,
       '... which falls SHORT of the closed form, because the corner lies inside a cell');
    { const s2=TYPICAL_Y*Math.pow(2/w,2), short=REF.PAR_JUMP-REF.PAR_JUMP_MEAS;
      ok(short>2*s2*DX&&short<4*s2*DX,
         '... by between 2 s dx and 4 s dx: the clean cells sit one to two cells off the corner ['
         +fmt(short/(2*s2*DX),3)+' cells]'); }
    ok(Math.abs(d[idxAt(x0)])<0.02,'and the parabola VERTEX is smooth: the slope there is zero');
  }
  { const out=manipulate(zero(),zeroC(),'hill',W_DEF,3.0,1.5);
    const d=derivOf(out.f);
    close(maxStep(d),REF.HILL_MAX_DSLOPE,1e-9,'hill: the largest step between neighbouring slopes (derive)');
    eq(cornerList(out.c,d,24).length,0,'... and it is flagged as having no corner at all');
    const p=manipulate(zero(),zeroC(),'pedestal',3.0,5.0,1.2);
    const dp=derivOf(p.f);
    close(maxStep(dp),REF.PED_MAX_DSLOPE,1e-9,'pedestal: the same (derive)');
    eq(cornerList(p.c,dp,24).length,0,'... and no corner either: the quartic join is C3');
    /* the real difference between a corner and a sharp smooth edge is not the
       SIZE of the slope step but how it behaves under refinement: a corner's
       step is the jump and does not move, a smooth edge's is g" dx and halves.
       (Comparing the two numbers at one grid gave 2 against 0.23, a factor of
       only 8.7, which is not a statement about anything.) */
    const g2=gridOf(2*(NPTS-1)+1);
    const t2=manipulate(new Float64Array(g2.n),new Uint8Array(g2.n),'triangle',W_DEF,4.0,1.5,g2);
    const p2=manipulate(new Float64Array(g2.n),new Uint8Array(g2.n),'pedestal',3.0,5.0,1.2,g2);
    const triStep2=maxStep(derivOf(t2.f,g2.n,g2.dx)), pedStep2=maxStep(derivOf(p2.f,g2.n,g2.dx));
    close(triStep2,REF.TRI_MAX_DSLOPE,1e-12,
          'refine the grid and the TRIANGLE\'s slope step does not move: it is the jump');
    rel(pedStep2,REF.PED_MAX_DSLOPE/2,0.02,
        '... while the PEDESTAL\'s halves, because it is g\'\' dx and there is no jump'); }
  /* the packet's WIDTH and its taper, at a width whose ends fall inside the
     domain and on a base that is not zero.  Every earlier sinusoid test used
     w = 2 on an empty curve, where the ends are off the domain and PhET drops
     the taper, so "seven half-periods -> five" and "lambda/8 -> lambda/4" both
     survived the first sweep without changing a single assertion. */
  { const wn=0.6, xn=5.0;
    const nar=manipulate(zero(),zeroC(),'sinusoid',wn,xn,1.0);
    const cf=shapeClosed('sinusoid',wn,xn,1.0);
    close(2*PI*wn/W_DEF,REF.SIN_NARROW_LAM,1e-12,'the narrow sinusoid period (derive)');
    close(cf.breaks[0],REF.SIN_NARROW_L,1e-12,'... its left end, seven half-periods wide (derive)');
    close(cf.breaks[1],REF.SIN_NARROW_R,1e-12,'... and its right end (derive)');
    rel(2*(cf.breaks[1]-cf.breaks[0])/REF.SIN_NARROW_LAM,7,2e-3,
        '... so the packet really is seven half-periods across');
    close(integOf(nar.f)[NPTS-1],REF.SIN_NARROW_AREA,1e-11,'... and the area it lays down (derive)');
    /* the taper only exists where there is something to blend into */
    const base=manipulate(zero(),zeroC(),'shift',1.0,5.0,1.0);
    close(base.f[0],1,1e-15,'a shift to 1.0 gives a constant curve to blend into');
    const tap=manipulate(base.f,base.c,'sinusoid',wn,xn,0.8);
    const it=idxAt(REF.SIN_TAPER_X);
    close(XG[it],REF.SIN_TAPER_X,1e-12,'the probe sits on a node inside the taper band (derive)');
    close(tap.f[it],REF.SIN_TAPER_F,1e-12,'and the cos-squared blend there (derive)');
    ok(Math.abs(tap.f[it]-1)>1e-3&&Math.abs(tap.f[it]-0.8*Math.cos(2*PI*(XG[idxAt(xn)]-XG[it])/REF.SIN_NARROW_LAM))>1e-3,
       '... which is neither the base nor the wave, so the taper is what is being measured');
    close(REF.SIN_TAPER_A,REF.SIN_NARROW_LAM/8,1e-12,'and the band is one eighth of a period (derive)');
  }
  { /* a sinusoid on an EMPTY curve loses its taper, so it ends in two corners */
    const out=manipulate(zero(),zeroC(),'sinusoid',0.5*2,5.0,1.0);
    const lam=2*PI*1.0/W_DEF;
    close(lam,REF.SIN_LAMBDA/2,1e-12,'the sinusoid period is 2 pi w / 2 (derive)');
    const w2=2.0;
    const o2=manipulate(zero(),zeroC(),'sinusoid',w2,5.0,1.0);
    const d2=derivOf(o2.f);
    ok(cornerList(o2.c,d2,24).length===0,
       'at w = 2 the packet is wider than the whole x range, so no end falls inside it');
    /* narrow it until both ends are inside */
    const o3=manipulate(zero(),zeroC(),'sinusoid',0.6,5.0,1.0);
    const d3=derivOf(o3.f);
    const cl=cornerList(o3.c,d3,24);
    ok(cl.length===2,'a narrow sinusoid ends in exactly two corners ['+cl.length+']');
    const k=2*PI/(2*PI*0.6/W_DEF);
    ok(Math.abs(Math.abs(cl[0].right)-k)<0.02*k||Math.abs(Math.abs(cl[0].left)-k)<0.02*k,
       '... and the slope there is y k = '+fmt(k,4)); }

  /* ---------- 7. the two tools ---------- */
  { const cur=buildDefaultCurve();
    const d=derivOf(cur.f), F=integOf(cur.f);
    let wt=0;
    for(const xq of [0.37,1.5,2.9,3.2,4.4,5.0,6.13,6.8,7.77,9.42]){
      const T=tangentAt(cur.f,d,xq);
      wt=Math.max(wt,Math.abs(T.slope-d[cellAt(xq)]));
      close(T.y0,cur.f[T.i],0,'the tangent line starts on the node at x = '+fmt(xq,2));
      close(T.y0+T.slope*DX,cur.f[T.i+1],1e-13,'... and reaches the next node exactly');
    }
    close(wt,REF.TANGENT_TOL,1e-15,'the tangent slope IS the derivative curve at the same x (derive)');
    /* valueAt's interpolation, pinned where the answer is known exactly: at a
       cell midpoint a straight segment reads the MEAN of its two nodes, which
       is the same quantity the fundamental-theorem check returns.  Without
       this the mutant that halved its parameter survived. */
    { let worst=0;
      for(let i=7;i<NPTS-1;i+=137) worst=Math.max(worst,Math.abs(valueAt(cur.f,XMID[i])-0.5*(cur.f[i]+cur.f[i+1])));
      ok(worst<1e-15,'valueAt at a cell midpoint is the mean of its two nodes ['+worst.toExponential(2)+']');
      close(valueAt(cur.f,XG[400]+0.25*DX),cur.f[400]+0.25*(cur.f[401]-cur.f[400]),1e-15,
            '... and a quarter of the way across, a quarter of the way up'); }
    let wa=0;
    for(const xq of [0.5,2.0,3.2,4.0,5.55,6.8,8.0,10.0]){
      const A=signedAreas(cur.f,xq), I=integAt(cur.f,F,xq);
      wa=Math.max(wa,Math.abs(A.net-I));
    }
    ok(wa<1e-11,'the split-at-zeros area equals the integral curve ['+wa.toExponential(2)+']');
    rel(wa,REF.AREA_TOL,20,'... to the residual derive.py measured (derive)');
    const A=signedAreas(cur.f,XMAX);
    close(A.pos,REF.DEF_AREA_POS,1e-11,'the shipped curve: area above the axis (derive)');
    close(A.neg,REF.DEF_AREA_NEG,1e-11,'the shipped curve: area below (derive)');
    close(A.net,REF.DEF_AREA_NET,1e-11,'the shipped curve: net signed area (derive)');
    close(A.pos-A.neg,F[NPTS-1],1e-11,'... and pos - neg is the integral at x = 10');
    ok(A.pos>0&&A.neg>0,'and both halves are really nonzero, so the split is being exercised');
  }
  /* the two-hill curve, whose halves nearly cancel */
  { const a=manipulate(zero(),zeroC(),'hill',2.0,2.5,1.2);
    const b=manipulate(a.f,a.c,'hill',2.0,7.0,-1.0);
    const A=signedAreas(b.f,XMAX);
    close(A.pos,REF.CROSS_POS,1e-9,'two-hill curve: the positive area (derive)');
    close(A.neg,REF.CROSS_NEG,1e-9,'two-hill curve: the negative area (derive)');
    close(A.net,REF.CROSS_NET,1e-9,'two-hill curve: the net (derive)');
  }

  /* ---------- 8. the shipped curve ---------- */
  { const cur=buildDefaultCurve();
    const d=derivOf(cur.f), F=integOf(cur.f), d2=deriv2Of(cur.f);
    close(maxAbs(cur.f),Math.max(Math.abs(REF.DEF_F_MAX),Math.abs(REF.DEF_F_MIN)),1e-12,
          'the shipped curve reaches its hill height (derive)');
    close(Math.max.apply(null,Array.from(d)),REF.DEF_D_MAX,1e-9,'its largest slope (derive)');
    close(Math.min.apply(null,Array.from(d)),REF.DEF_D_MIN,1e-9,'its smallest slope (derive)');
    close(F[NPTS-1],REF.DEF_I_END,1e-11,'its integral over the whole range (derive)');
    close(maxAbs(d2),REF.DEF_D2_MAX,1e-6,'and its f" spike at the triangle apex (derive)');
    for(const [x,fk,ik] of [[2.0,'DEF_F_AT_20','DEF_I_AT_20'],[3.2,'DEF_F_AT_32','DEF_I_AT_32'],
                            [5.0,'DEF_F_AT_50','DEF_I_AT_50'],[6.8,'DEF_F_AT_68','DEF_I_AT_68'],
                            [8.0,'DEF_F_AT_80','DEF_I_AT_80']]){
      close(cur.f[idxAt(x)],REF[fk],1e-12,'the shipped curve f('+fmt(x,1)+') (derive)');
      close(F[idxAt(x)],REF[ik],1e-11,'the shipped curve int_0^'+fmt(x,1)+' f (derive)');
    }
    close(d[idxAt(3.2)],REF.DEF_D_AT_32,1e-12,"the shipped curve's slope just right of the hill top (derive)");
  }

  /* ---------- 9. smoothing ---------- */
  { const ones=new Float64Array(NPTS).fill(1);
    const s=smoothCurve(ones);
    eq(s.taps,REF.SMOOTH_TAPS,'the smoothing kernel has PhET\'s number of taps each side (derive)');
    /* the normalisation cancels in acc/tot, so these two are the ONLY things
       that can pin PhET's 1/(sigma sqrt(2 pi)) and the 3-sigma window */
    close(s.w0,REF.SMOOTH_W0,1e-12,'... PhET\'s peak weight 1/(sigma sqrt(2 pi)) (derive)');
    close(s.tot,REF.SMOOTH_TOT,1e-11,'... and the sum of its '+(2*s.taps+1)+' sampled weights (derive)');
    /* the sum of a Gaussian sampled every dx out to K taps is the midpoint
       rule for its integral, so tot/w0 = sqrt(2 pi)(sigma/dx) erf((K+1/2)dx /
       (sigma sqrt2)) -- which pins the 3-sigma WINDOW as well as the spacing,
       and would move if either changed */
    rel(s.tot/s.w0,Math.sqrt(2*PI)*(SMOOTH_SIGMA/DX)*erf((s.taps+0.5)*DX/(SMOOTH_SIGMA*Math.SQRT2)),
        1e-3,'... and the weights sum to the midpoint rule for that Gaussian');
    ok(Math.abs(s.tot/s.w0-Math.sqrt(2*PI)*SMOOTH_SIGMA/DX)>0.02,
       '... but NOT to the untruncated integral: the 3-sigma cut is worth 0.3 %');
    close(maxDiff(s.f,ones),0,1e-15,'a constant survives smoothing exactly (the weights are renormalised)');
    const hill=manipulate(zero(),zeroC(),'hill',W_DEF,5.0,1.5);
    const sh=smoothCurve(hill.f);
    close(maxAbs(sh.f),REF.SMOOTH_HILL_PEAK,1e-12,'a w = 2 hill after one smoothing (derive)');
    close(maxAbs(sh.f)/1.5,REF.SMOOTH_HILL_RATIO,1e-12,'... and the peak ratio (derive)');
    ok(Math.abs(REF.SMOOTH_HILL_RATIO-REF.SMOOTH_GAUSS_RATIO)<3e-4,
       '... within 3e-4 of the untruncated-kernel prediction sig/sqrt(sig^2+sigs^2)');
    ok(REF.SMOOTH_HILL_RATIO!==REF.SMOOTH_GAUSS_RATIO,
       '... but NOT equal to it: the kernel is truncated at 3 sd and renormalised');
    let a0=0,a1=0;
    for(let i=0;i<NPTS;i++){ a0+=hill.f[i]*DX; a1+=sh.f[i]*DX; }
    ok(Math.abs(a1-a0)<1e-12,'and smoothing an interior bump preserves its area ['
       +Math.abs(a1-a0).toExponential(2)+']');
    const tri=manipulate(zero(),zeroC(),'triangle',W_DEF,5.0,1.5);
    const st2=smoothCurve(tri.f), dt=derivOf(st2.f), i0=idxAt(5.0);
    close(dt[i0-1],REF.SMOOTH_TRI_SLOPE,1e-9,'a smoothed triangle apex: the cell slope beside it (derive)');
    close(maxAbs(st2.f),REF.SMOOTH_TRI_PEAK,1e-9,'... and its rounded peak (derive)');
    ok(Math.abs(dt[i0-1])<0.1*REF.TRI_SLOPE,'smoothing really does round the corner off');
    /* PhET marks every point smooth after a smoothing, and the corner list has
       to follow, or the derivative panel keeps breaking where there is no
       longer a break */
    const triC=manipulate(zero(),zeroC(),'triangle',W_DEF,5.0,1.5);
    ok(cornerList(triC.c,derivOf(triC.f),24).length===3,'the triangle starts with three corners');
    { const sv=Object.assign({},ST); Object.assign(ST,DEFAULTS);
      CURVE=triC.f; CFLAG=triC.c; CVER++;
      doSmooth();
      ok(cornerList(CFLAG,derivOf(CURVE),24).length===0,'... and none of them survives a smoothing');
      Object.assign(ST,sv); } }

  /* ---------- 10. tilt, shift, freeform, undo ---------- */
  { const base=manipulate(zero(),zeroC(),'hill',2.0,3.0,1.0);
    const t=manipulate(base.f,base.c,'tilt',0,8.0,1.6);
    close(t.f[0],base.f[0],0,'tilt is pinned at the left edge');
    close(t.f[idxAt(8.0)],1.6,1e-13,'... and the dragged point lands on the pointer');
    const dd=derivOf(t.f), db=derivOf(base.f);
    let lo=1e9,hi=-1e9;
    for(let i=0;i<dd.length;i++){ const v=dd[i]-db[i]; lo=Math.min(lo,v); hi=Math.max(hi,v); }
    close(hi-lo,0,1e-12,'... and every cell slope changes by the SAME amount');
    close(0.5*(hi+lo),REF.TILT_SLOPE_ADD,1e-12,'... which is the slope it adds (derive)');
    const steep=manipulate(base.f,base.c,'tilt',0,0.04,2.0);
    close(maxDiff(steep.f,base.f),0,0,'tilt refuses a slope past PhET\'s maxTilt, leaving the curve alone');
    const s=manipulate(base.f,base.c,'shift',0,3.0,-0.5);
    close(maxDiff(derivOf(s.f),db),0,1e-12,'shift leaves every slope alone');
    close(s.f[0]-base.f[0],REF.SHIFT_DELTA,1e-13,'... and moves the curve by the offset it was given (derive)');
    let worst=0;
    const Fs=integOf(s.f), Fb=integOf(base.f);
    for(let i=0;i<NPTS;i++) worst=Math.max(worst,Math.abs((Fs[i]-Fb[i])-REF.SHIFT_DELTA*XG[i]));
    ok(worst<1e-11,'... and its integral gains exactly delta x x ['+worst.toExponential(2)+']');
  }
  { const f=zero(), c=zeroC();
    freeformStroke(f,c,3.0,1.0,null,null);
    close(f[idxAt(3.0)],1,0,'freeform sets the node it was given');
    freeformStroke(f,c,4.0,-0.5,3.0,1.0);
    close(f[idxAt(4.0)],-0.5,0,'... and the next one');
    /* 3.6 is a node (450) and 3.5 is not: idxAt(3.5) is 437.5 rounded UP to
       438, so the "midpoint" there is 0.244, not 0.25.  Probe a node. */
    close(f[idxAt(3.6)],0.1,1e-12,'... with a straight run between them');
    ok(Math.abs(derivOf(f)[idxAt(3.6)]-(-1.5))<1e-9,'so its slope there is the chord slope');
  }
  { withState({},()=>{
      const before=CURVE.slice();
      saveCurve();
      applyShape('hill',2,5,1.5);
      ok(maxDiff(CURVE,before)>0.1,'laying a shape down changes the curve');
      ok(doUndo(),'undo reports that it did something');
      close(maxDiff(CURVE,before),0,0,'... and puts the curve back');
      ok(!doUndo(),'a second undo on an empty stack reports nothing to do');
      for(let i=0;i<MAX_UNDO+7;i++){ saveCurve(); applyShape('hill',2,1+i*0.1,0.3); }
      eq(UNDO.length,MAX_UNDO,'the undo stack is capped at PhET\'s depth');
      doErase();
      close(maxAbs(CURVE),0,0,'erase gives PhET\'s empty curve');
      ok(doUndo(),'... and undo brings it back');
      ok(maxAbs(CURVE)>0,'... really back');
    }); }

  /* ---------- 11. PhET's blend threshold and the shape bookkeeping ---------- */
  { const flat=new Float64Array(NPTS).fill(0.5);
    const out=manipulate(flat,zeroC(),'hill',1.0,5.0,1.5);
    close(out.f[0],0.5,0,'far from a hill the saved value is kept UNCHANGED (PhET\'s 1e-8 cut)');
    const P=Math.exp(-Math.pow((XG[0]-5)/(1/(2*Math.sqrt(2))),2));
    ok(P<BLEND_EPS,'... and the weight out there really is below 1e-8 ['+P.toExponential(2)+']');
    close(out.f[idxAt(5.0)],1.5,1e-12,'at the centre the hill wins outright');
    const half=XG[idxAt(5.0+W_DEF/2)];
    const o2=manipulate(flat,zeroC(),'hill',W_DEF,5.0,1.5);
    const Ph=Math.exp(-8*Math.pow(half-5,2)/(W_DEF*W_DEF));
    close(o2.f[idxAt(5.0+W_DEF/2)],Ph*1.5+(1-Ph)*0.5,1e-12,
          'and half a width out it is the blend PhET writes, not the shape');
    close(Ph,Math.exp(-2),1e-12,'... where the weight is exp(-2) = 0.1353, the Gaussian at 2 sd');
  }
  { /* the hill IS a Gaussian of sd w/4, which is the claim worth pinning.
       w = 1.6 puts one sd at 0.4 = 50 cells, so the probe lands on a NODE:
       at w = 2 the sd is 62.5 cells and idxAt rounds, which reads 0.6017
       instead of 0.6065 and looks like a wrong constant. */
    const w=1.6, out=manipulate(zero(),zeroC(),'hill',w,5.0,1.0), sd=w/4;
    close(sd/DX,50,1e-12,'w = 1.6 puts one standard deviation exactly 50 cells out');
    close(out.f[idxAt(5.0+sd)],Math.exp(-0.5),1e-12,'the hill is exp(-1/2) one sd out, sd = w/4');
    close(out.f[idxAt(5.0+2*sd)],Math.exp(-2),1e-12,'and exp(-2) two sd out');
    close(out.f[idxAt(5.0-3*sd)],Math.exp(-4.5),1e-12,'and exp(-9/2) three sd the other way');
  }

  /* ---------- 12. every view x every configuration builds clean ---------- */
  { const CONFIGS=[];
    for(const [v] of TABS)
      for(const shape of SHAPE_MODES)
        CONFIGS.push({view:v,refShape:shape,mode:shape});
    CONFIGS.push({view:'deriv',mode:'tilt'},{view:'deriv',mode:'shift'},{view:'deriv',mode:'freeform'},
                 {view:'lab',predict:true,showF:false},{view:'lab',predict:true,showF:true},
                 {view:'integ',area:true,values:true},{view:'deriv',values:true,refLine:true},
                 {view:'corner',refShape:'hill'},{view:'corner',refShape:'pedestal'},
                 {view:'grid',gridMult:0},{view:'grid',gridMult:GRID_MULTS.length-1},
                 {view:'lab',notation:'leibniz',variable:'t'},{view:'deriv',discont:'dashedLine'},
                 {view:'ftc',_curve:{f:new Float64Array(NPTS),c:new Uint8Array(NPTS)}});
    let bad=null, nonFinite=null;
    for(const cfg of CONFIGS){
      withState(cfg,()=>{
        const M=buildModel();
        const ro=readoutHTML(M), eqs=eqbarHTML(M), tg=tagHTML(M);
        for(const [nm,s] of [['readout',ro],['equation bar',eqs],['tag',tg]]){
          if(/NaN|undefined|Infinity/.test(s)&&!bad) bad=cfg.view+'/'+(cfg.refShape||cfg.mode)+' '+nm;
        }
        for(const a of [M.live.f,M.live.d,M.live.F,M.live.d2])
          for(let i=0;i<a.length;i+=7) if(!isFinite(a[i])&&!nonFinite) nonFinite=cfg.view;
      });
    }
    ok(!bad,'every view x shape builds a clean readout, equation bar and tag ('+(bad||'ok')+')');
    ok(!nonFinite,'and no curve carries a non-finite value ('+(nonFinite||'ok')+')');
    ok(CONFIGS.length>=44,'the sweep covers '+CONFIGS.length+' configurations');
  }
  /* the empty curve is the one configuration whose residuals are EXACTLY zero,
     and the caption used to call that "floating-point rounding", put its
     largest value "at a corner" there was none of, and then say "and not
     zero" of a zero.  Three false sentences over a flat line. */
  withState({view:'ftc',_curve:{f:new Float64Array(NPTS),c:new Uint8Array(NPTS)}},()=>{
    const M=buildModel();
    eq(M.ftc.e1,0,'an empty curve: integrating its derivative is exactly f - f(0)');
    eq(M.ftc.e2,0,'... and differentiating its integral is exactly f');
    eq(M.ftc.ePhet,0,'... and PhET\'s pair costs exactly nothing on it, too');
    const cap=ftcCap(M);
    ok(cap.full.indexOf('empty')>=0&&cap.full.indexOf('rounding at')>=0,
       '... and the caption says so rather than calling zero a rounding error');
    ok(cap.full.indexOf('is at a corner')<0,'... and does not put a zero at a corner there are none of');
  });
  withState({view:'ftc'},()=>{
    const cap=ftcCap(buildModel());
    ok(cap.full.indexOf('empty')<0,'... while a drawn curve gets the measuring caption');
  });
  /* a tick far below the tick spacing prints as 0, not as -0 */
  { const f2=tickFmt([0,0.5,1]);
    ok(f2(-1e-13).indexOf('-')<0,'the tick formatter never prints -0 ['+f2(-1e-13)+']');
    eq(+f2(-1e-13),0,'... and prints a value below the spacing as zero');
    eq(+f2(0.5),0.5,'... and a real one as itself'); }

  /* a readout must contain an EXPECTED number, or "no NaN" is vacuous:
     fmt() renders NaN as an em dash (Known-bad, sbs_parent_law) */
  withState({view:'integ',area:true},()=>{
    const M=buildModel();
    const ro=readoutHTML(M);
    ok(ro.indexOf(fmt(M.tools.ar.net,4))>=0,'the readout really prints the net area it computed');
    ok(ro.indexOf('2.00')>=0||ro.indexOf(fmt(M.tools.ar.pos,4))>=0,'... and the positive half');
  });

  /* ---------- 13. the layout, at four sizes ---------- */
  { const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
    const SIZES=[[1400,820],[1100,700],[820,560],[560,380]];
    const CFG=[{view:'deriv'},{view:'integ',area:true},{view:'lab',refLine:true,values:true},
               {view:'corner',refShape:'triangle'},{view:'corner',refShape:'hill'},
               {view:'ftc'},{view:'grid'},{view:'lab',notation:'leibniz',variable:'t'}];
    let off=null, coll=null, ent=null, hint=null, thin=null, legx=null;
    for(const cfg of CFG){
      withState(cfg,()=>{
        for(const [W,H] of SIZES){
          const c=makeShot(W,H);
          drawView(c,W,H,buildModel());
          const texts=c.ops.filter(o=>o.op==='text');
          const fills=c.ops.filter(o=>o.op==='fill');
          if(fills.length+c.ops.length<12&&!thin) thin=cfg.view+' '+W+'x'+H;
          for(const t of texts){
            if(entRe.test(t.t)&&!ent) ent=cfg.view+' "'+String(t.t).slice(0,32)+'"';
            if(/NaN|undefined|Infinity/.test(t.t)&&!ent) ent=cfg.view+' "'+String(t.t).slice(0,32)+'"';
            if((t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1)&&!off)
              off=cfg.view+' '+W+'x'+H+' "'+String(t.t).slice(0,26)+'"';
            /* the house #hint (HTML, bottom:11px) owns the bottom-left corner */
            if(t.bb[0]<340&&t.bb[3]>H-27&&!hint)
              hint=cfg.view+' '+W+'x'+H+' "'+String(t.t).slice(0,26)+'"';
          }
          for(let i=0;i<texts.length&&!coll;i++) for(let j=i+1;j<texts.length;j++){
            const a=texts[i].bb, b=texts[j].bb;
            const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
            if(ox>3&&oy>3){ coll=cfg.view+' '+W+'x'+H+' "'+String(texts[i].t).slice(0,20)
                            +'" vs "'+String(texts[j].t).slice(0,20)+'"'; break; }
          }
          for(const r of LEGEND_RECTS){
            for(let i=0;i<POLY_SEGS.length&&!legx;i+=4){
              const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
              if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w) continue;
              if(Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
              legx=cfg.view+' '+W+'x'+H;
            }
          }
        }
      });
    }
    ok(!ent,'no entity, tag, NaN or undefined reaches the canvas ('+(ent||'ok')+')');
    ok(!off,'no canvas text runs off the stage ('+(off||'ok')+')');
    ok(!coll,'no two canvas text boxes overlap by more than 3 px ('+(coll||'ok')+')');
    ok(!hint,'nothing is drawn under the HTML hint line ('+(hint||'ok')+')');
    ok(!thin,'every view draws substance at every size ('+(thin||'ok')+')');
    ok(!legx,'no data curve runs through a legend ('+(legx||'ok')+')');
  }
  /* the canvas never carries a letter subscript: there is no Unicode subscript
     f at all and the rasteriser's font does not carry every one that exists */
  { withState({view:'lab',notation:'leibniz'},()=>{
      const c=makeShot(1400,820);
      drawView(c,1400,820,buildModel());
      let bad=null;
      for(const o of c.ops) if(o.op==='text'&&/[ₐ-ₜᵢ-ᵪ]/.test(o.t)) bad=o.t;
      ok(!bad,'no letter subscript on the canvas ('+(bad||'ok')+')');
    }); }

  /* ---------- 14. the scene's pointer arithmetic ---------- */
  { withState({view:'deriv',mode:'hill'},()=>{
      const S2=makeScene({getContext:()=>makeShot(1400,820)});
      S2.W=1400; S2.H=820; S2.draw();
      ok(!!GEO.fb&&!!GEO.fmap,'the derivative view records the f panel for the pointer');
      const b=GEO.fb, m=GEO.fmap;
      close(m.wx(m.X(4.2)),4.2,1e-9,'the panel map round-trips in x');
      close(m.wy(m.Y(0.8)),0.8,1e-9,'... and in y');
      const before=CURVE.slice();
      const px=m.X(6.0), py=m.Y(1.2);
      ok(S2.pointer('down',px,py),'a press on the f panel changes the curve');
      close(CURVE[idxAt(6.0)],1.2,1e-9,'... and puts the hill top under the pointer');
      ok(maxDiff(CURVE,before)>0.5,'... and it really moved');
      const mid=CURVE.slice();
      ok(S2.pointer('move',m.X(7.0),m.Y(-0.9)),'a drag moves it again');
      close(CURVE[idxAt(7.0)],-0.9,1e-9,'... to the new pointer position');
      ok(Math.abs(CURVE[idxAt(6.0)]-1.2)>0.5,
         '... from the SAVED curve, so the old hill is gone rather than stacked');
      ok(S2.pointer('up',0,0),'the release is reported');
      ok(!S2.drag,'... and clears the drag');
      /* the scrubber takes priority inside the same panel */
      S2.draw();
      const sc=GEO.scrubs.filter(s=>s.kind==='T')[0];
      ok(!!sc,'the tangent scrubber is recorded');
      const x0=ST.xT;
      ok(S2.pointer('down',sc.X+1,(sc.b.y+sc.b.y1)/2),'a press on the scrubber is taken by the scrubber');
      ok(ST.xT!==x0,'... and moves it');
      ok(S2.drag&&S2.drag.what==='scrub','... rather than starting a curve drag');
      S2.pointer('up',0,0);
    }); }
  /* the tangent gauge and the derivative curve are the same number, through
     the model rather than through a re-typed formula */
  withState({view:'deriv',xT:2.4},()=>{
    const M=buildModel();
    close(M.tools.tan.slope,M.live.d[cellAt(2.4)],0,'the gauge reads the derivative curve exactly');
  });
  withState({view:'integ',xA:4.4,area:true},()=>{
    const M=buildModel();
    ok(M.tools.areaMismatch<1e-12,'the area gauge and the integral curve agree ['
       +M.tools.areaMismatch.toExponential(2)+']');
  });

  /* ---------- 15. notation, variable, predict ---------- */
  withState({notation:'lagrange',variable:'x'},()=>{
    ok(cName('d')==='f′(x)','Lagrange notation is f′(x)');
    ok(nameD().indexOf('prime')>=0,'... and its HTML form uses the prime entity');
  });
  withState({notation:'leibniz',variable:'t'},()=>{
    ok(cName('d')==='df/dt','Leibniz notation with PhET\'s t variable is df/dt');
    ok(cName('dd')==='d²f/dt²','... and the second is d²f/dt²');
    ok(cName('I')==='∫ f dt','... and the integral carries the same variable');
  });
  { const p=new Float64Array(NPTS);
    withState({view:'lab',predict:true,_pred:p},()=>{
      const M=buildModel();
      ok(M.shape!==M.live,'with predict on, the shaped curve and f are different objects');
      close(maxAbs(M.shape.f),0,0,'... the prediction starts empty');
      ok(maxAbs(M.live.f)>1,'... while f is still there for the other panels');
      ok(M.predRms>0.1,'... and the readout scores the guess ('+fmt(M.predRms,3)+')');
    }); }

  /* ---------- 16. the grid study ---------- */
  withState({view:'grid',refShape:'hill',refW:2,refX:3,refY:1.5},()=>{
    const rows=gridStudy();
    eq(rows.length,GRID_MULTS.length,'the refinement ladder has '+GRID_MULTS.length+' rungs');
    for(let i=1;i<rows.length;i++)
      ok(rows[i].ed<rows[i-1].ed,'the derivative error falls from '+(rows[i-1].n-1)+' to '+(rows[i].n-1)+' cells');
    const r=rows[rows.length-2].ed/rows[rows.length-1].ed;
    ok(Math.abs(r-4)<0.2,'and the last halving quarters it ('+fmt(r,4)+')');
    const iP=GRID_MULTS.indexOf(1);
    eq(rows[iP].n,NPTS,"PhET's own grid is one of the rungs");
    rel(rows[iP].ed,REF.ERR_D_HILL,1e-6,"... and it reproduces derive.py's number there (derive)");
  });

  restore();
  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
