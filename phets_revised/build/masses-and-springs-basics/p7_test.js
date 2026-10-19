
/* ================================================================== *
 *  selfTest — headless verification.  Every value labelled (derive)   *
 *  is a line of build/masses-and-springs-basics/refvals.txt, the      *
 *  printed output of derive.py (scipy solve_ivp, scipy quad, an RK4   *
 *  whose convergence order is measured, and the closed form), read    *
 *  in full.  The recording stub is the house one.                     *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0w=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    Object.assign(ST,DEFAULTS,clean); liveReset();
    /* clicking a tab is what applies PhET's per-screen damping, so a headless
       configuration has to do the same or it runs the Lab screen at 0.7 */
    if(clean.damping===undefined&&VIEW_DAMPING[ST.view]!==undefined) ST.damping=VIEW_DAMPING[ST.view];
    if(over._live&&liveViews(ST.view)) for(let i=0;i<over._live;i++) advance(ST,0.02);
    if(over._sw!==undefined){ LIVE.sw=over._sw; LIVE.swOn=true; }
    try{ return fn(); } finally{ Object.assign(ST,stSave); liveReset(); DRAG.what=null; }
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(mix('#070b18',mix('#b8ec4c','#cd35c4',0.5),1)!=='rgb(0,0,0)','mix() output is a legal mix() input (not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }

  /* ---------- 1. PhET's constants, pinned absolutely ---------- */
  eq(CEILING_Y,1.47,"PhET's ceiling"); eq(FLOOR_Y,0,"PhET's floor");
  eq(L0,0.5,"PhET's natural spring length"); eq(SHELF_H,0.02,"PhET's shelf height");
  eq(HOOK_H,0.037,"PhET's hook height"); eq(HOOK_C,0.0185,"PhET's hook centre");
  eq(KMIN,3,"PhET's spring constant floor"); eq(KMAX,12,"PhET's spring constant ceiling"); eq(KDEF,6,"PhET's default spring constant");
  eq(BMIN,0,"PhET's damping floor"); eq(BMAX,0.7,"PhET's damping ceiling"); eq(BDEF,0.3,"PhET's default damping");
  eq(GMIN,0,"PhET's gravity floor"); eq(GMAX,30,"PhET's gravity ceiling");
  eq(G_EARTH,9.8,"PhET's Earth"); eq(G_MOON,1.6,"PhET's Moon"); eq(G_JUPITER,24.8,"PhET's Jupiter");
  eq(G_PLANETX,14.2,"PhET's Planet X (its invented mystery value)");
  eq(G_EARTH_REAL,9.81,'the real Earth'); eq(G_MOON_REAL,1.62,'the real Moon'); eq(G_JUPITER_REAL,24.79,'the real Jupiter');
  eq(MASS_G_MIN,50,"PhET's lightest lab mass"); eq(MASS_G_MAX,300,"PhET's heaviest lab mass"); eq(MASS_G_DEF,100,"PhET's default lab mass");
  eq(SLOW,1/8,"PhET's slow-motion ratio"); eq(B_STRETCH,0.7,"the Stretch screen's damping");
  eq(B_BOUNCE,0,"the Bounce screen's damping"); eq(B_LAB,0,"the Lab screen's damping");
  eq(LEFT_SPRING_X,1,"PhET's left spring x"); eq(RIGHT_SPRING_X,1.3,"PhET's right spring x"); eq(SPRING_X,1.2,"PhET's lab spring x");
  eq(RACK.filter(r=>!r.myst&&r.m>0).map(r=>r.m).join(','),'0.05,0.1,0.25',"PhET's labelled rack");
  eq(RACK.filter(r=>r.myst).map(r=>r.m).join(','),'0.075,0.1,0.2',"PhET's mystery rack");
  eq(LAB_RACK.filter(r=>r.myst).map(r=>r.m).join(','),'0.18,0.12',"PhET's lab mystery masses");
  /* the mass-block size rule (derive) */
  rel(massRadius(0.05),0.035682482323055424,1e-15,'block radius at 50 g (derive)');
  rel(massRadius(0.10),0.050462650440403205,1e-15,'block radius at 100 g (derive)');
  rel(massRadius(0.25),0.07978845608028654,1e-15,'block radius at 250 g (derive)');
  rel(massHeight(0.30),0.21850968611841579,1e-15,'block height at 300 g (derive)');
  rel(massRadius(0.2)/massRadius(0.05),2,1e-15,'the block scales as the square root of the mass');

  /* ---------- 2. Hooke's law over everything the sim allows ---------- */
  eq(springForce(6,0.25),-1.5,'F = -k y');
  rel(yEq(0.25,6,G_EARTH),0.4083333333333334,1e-15,'250 g on 6 N/m, Earth (derive)');
  rel(yEq(0.25,6,G_MOON),0.06666666666666667,1e-15,'250 g on 6 N/m, Moon (derive)');
  rel(yEq(0.25,6,G_JUPITER),1.0333333333333334,1e-15,'250 g on 6 N/m, Jupiter (derive)');
  rel(yEq(0.25,6,G_PLANETX),0.5916666666666667,1e-15,'250 g on 6 N/m, Planet X (derive)');
  rel(yEq(0.10,3,G_EARTH),0.3266666666666667,1e-15,'100 g on 3 N/m, Earth (derive)');
  rel(yEq(0.10,12,G_EARTH),0.08166666666666668,1e-15,'100 g on 12 N/m, Earth (derive)');
  rel(yEq(0.30,12,G_JUPITER),0.62,1e-15,'300 g on 12 N/m, Jupiter (derive)');
  rel(yEq(0.075,9,G_PLANETX),0.11833333333333333,1e-15,'75 g on 9 N/m, Planet X (derive)');
  rel(yEq(0.18,6,G_EARTH),0.294,1e-15,'180 g on 6 N/m, Earth (derive)');
  rel(yEq(0.3,3,30),3.0,1e-15,'the largest extension the sim allows is 3.00 m (derive)');
  { let tot=0,mx=0,n=0;
    for(let i=50;i<=300;i++){ const m=i/1000;
      for(let k=3;k<=12;k++) for(const g of [G_MOON,G_EARTH,G_PLANETX,G_JUPITER]){
        const y=yEq(m,k,g); tot+=y; if(y>mx) mx=y; n++; } }
    eq(n,10040,'the (mass, spring, planet) grid has 10040 states');
    close(tot,3549.219863636362,1e-9,'sum of mg/k over the whole grid (derive)');
    close(mx,2.48,1e-15,'the largest mg/k on the grid (derive)'); }
  /* the two inversions the sim asks the reader to make */
  rel(gFromStretch(6,yEq(0.1,6,G_PLANETX),0.1),G_PLANETX,1e-15,'g = k y/m recovers Planet X (derive)');
  rel(mFromStretch(6,yEq(0.18,6,G_EARTH),G_EARTH),0.18,1e-15,'m = k y/g recovers the 180 g mystery mass');
  rel(yEq(0.25,6,G_EARTH)/yEq(0.25,12,G_EARTH),2,1e-15,'half the stiffness is twice the stretch');
  rel(yEq(0.25,6,G_EARTH)/yEq(0.05,6,G_EARTH),5,1e-15,'five times the mass is five times the stretch');

  /* ---------- 3. the closed form, in all three regimes ---------- */
  const CASES=[
    ['undamped 250 g on 6',0.25,6,0,0.08,0,
     [[0.1,0.07059047056533474,-0.184411635123033],[0.5,-0.06159245837999144,-0.25010569305199065],
      [1,0.014840773232274418,0.38511561224759117],[2,-0.07449378624670518,0.14288533673937562]]],
    ['100 g on 6 at b = 0.7',0.1,6,0.7,0.05,0,
     [[0.1,0.038525427222468434,-0.194979145395194],[0.5,-0.009622350432244927,0.023264159874715765],
      [1,0.0016713855119263703,-0.007691386638806669],[2,3.6151447780342915e-05,-0.0003761768881245891]]],
    ['50 g on 3 at b = 0.7 (zeta nearest 1)',0.05,3,0.7,0.06,0,
     [[0.1,0.04864766307341515,-0.17551122526739346],[0.5,0.0036510405712336723,-0.03265203098348571],
      [1,-7.398591449412565e-05,0.0001723625001069216],[2,8.297947254689328e-08,-3.0954556199583647e-07]]],
    ['300 g on 12 at b = 0.7, moving',0.3,12,0.7,0.04,-0.2,
     [[0.1,0.01615408560695363,-0.2586204624527365],[0.5,-0.022771016830434684,0.10742451340794086],
      [1,0.012943596324753219,-0.05754505950430216],[2,0.0041642995774548,-0.01636422882277377]]],
    ['critically damped',0.1,6,2*Math.sqrt(0.6),0.05,0,
     [[0.1,0.040894660511993086,-0.1382668903446304],[0.5,0.005066985199404945,-0.03119435162864973],
      [1,0.00018912425570916157,-0.001297450098042457],[2,1.5423409631409277e-07,-1.12225117127359e-06]]],
    ['overdamped, b = 3',0.1,6,3,0.05,0,
     [[0.1,0.04342964268979529,-0.08692701631547152],[0.5,0.018452150882428114,-0.03975999677955409],
      [1,0.006282684995787803,-0.013537724947346005],[2,0.0007283526162092788,-0.0015694304886517748]]]];
  for(const [nm,m,k,b,u0,v0,rows] of CASES){
    for(const [t,u,v] of rows){
      const r=prop(m,k,b,u0,v0,t);
      rel(r[0],u,2e-12,nm+': u at t = '+t+' (derive)');
      rel(r[1],v,2e-12,nm+': v at t = '+t+' (derive)');
    }
    /* the propagator is a one-parameter group: two steps equal one */
    const a=prop(m,k,b,u0,v0,1.3), c=prop(m,k,b,u0,v0,0.7), d=prop(m,k,b,c[0],c[1],0.6);
    close(a[0],d[0],1e-15,nm+': P(0.7)P(0.6) = P(1.3) in u');
    close(a[1],d[1],1e-14,nm+': P(0.7)P(0.6) = P(1.3) in v');
    /* and it satisfies the equation it claims to solve: a central difference
       of v against (-k u - b v)/m at a handful of times */
    for(const t of [0.13,0.61,1.41]){
      const hh=1e-5, p1=prop(m,k,b,u0,v0,t+hh), p2=prop(m,k,b,u0,v0,t-hh), p0=prop(m,k,b,u0,v0,t);
      /* an ABSOLUTE tolerance: dv/dt passes through zero every half period, so
         a relative one would be measuring the cancellation and not the solution */
      close((p1[1]-p2[1])/(2*hh),(-k*p0[0]-b*p0[1])/m,1e-5,nm+': the solution satisfies m u" + b u\' + k u = 0 at t = '+t);
      close((p1[0]-p2[0])/(2*hh),p0[1],1e-8,nm+': and v is du/dt at t = '+t);
    }
  }
  /* a SECOND, independent spelling of each regime — typing catcher */
  for(const [m,k,b,u0,v0] of [[0.1,6,0.35,0.05,-0.2],[0.25,6,0,0.08,0.1],[0.3,12,0.7,0.04,-0.2]]){
    const gam=gammaOf(m,b), wd=omegaD(m,k,b);
    const A=Math.sqrt(u0*u0+Math.pow((v0+gam*u0)/wd,2)), ph=Math.atan2((v0+gam*u0)/wd,u0);
    for(const t of [0.2,0.9,1.7]) rel(prop(m,k,b,u0,v0,t)[0],A*Math.exp(-gam*t)*Math.cos(wd*t-ph),1e-12,
      'underdamped: the amplitude-phase form agrees at t = '+t+' (m '+m+', b '+b+')');
  }
  { const m=0.1,k=6,b=3,u0=0.05,v0=0, gam=gammaOf(m,b), r=Math.sqrt(gam*gam-k/m);
    const s1=-gam+r, s2=-gam-r, c1=(v0-s2*u0)/(s1-s2), c2=(s1*u0-v0)/(s1-s2);
    rel(s1,-2.1547674213348706,1e-14,'overdamped slow root (derive)');
    rel(s2,-27.84523257866513,1e-14,'overdamped fast root (derive)');
    for(const t of [0.2,1.1]) rel(prop(m,k,b,u0,v0,t)[0],c1*Math.exp(s1*t)+c2*Math.exp(s2*t),1e-12,
      'overdamped: the two-exponential form agrees at t = '+t); }
  { const m=0.1,k=6,b=2*Math.sqrt(0.6),u0=0.05,v0=0.3, gam=gammaOf(m,b);
    for(const t of [0.05,0.4,1.3]) rel(prop(m,k,b,u0,v0,t)[0],Math.exp(-gam*t)*(u0+(v0+gam*u0)*t),1e-12,
      'critical: the (a + bt)e^(-gam t) form agrees at t = '+t); }
  /* The C/Sn series branch, asserted AT ITS JOIN from both sides.  The join sits
     at |s|t^2 = 1e-5, where the three-term series is still exact to 1.4e-18 and
     BOTH of its terms move the answer by far more than a rounding error: the
     tolerance below is 1e-14, against x^2/24 = 4.2e-12 of C and x^2/120 =
     8.3e-13 of Sn, so a wrong quadratic coefficient fails by 83x or more. */
  { const t=0.37, XJ=1e-5, sj=XJ/(t*t);
    for(const s of [sj*0.999,sj*1.001,-sj*0.999,-sj*1.001,0]){
      const r=CSn(s,t), C=s>0?Math.cos(Math.sqrt(s)*t):(s<0?Math.cosh(Math.sqrt(-s)*t):1);
      const Sn=s>0?Math.sin(Math.sqrt(s)*t)/Math.sqrt(s):(s<0?Math.sinh(Math.sqrt(-s)*t)/Math.sqrt(-s):t);
      rel(r[0],C,1e-14,'CSn: C agrees with the direct form across the join at s = '+s.toExponential(2));
      rel(r[1],Sn,1e-14,'CSn: Sn agrees with the direct form across the join at s = '+s.toExponential(2)); }
    /* and the quadratic terms are what that tolerance is pinning: state their
       size, measured off the series itself */
    const x=XJ*0.999, s2=x/(t*t);
    const r2=CSn(s2,t), C2=Math.cos(Math.sqrt(s2)*t), S2=Math.sin(Math.sqrt(s2)*t)/Math.sqrt(s2);
    rel(r2[0],C2,1e-15,'CSn: C at the top of the series branch');
    rel(r2[1],S2,1e-15,'CSn: Sn at the top of the series branch');
    const cQuad=Math.abs(x*x/24), sQuad=Math.abs(x*x/120);
    ok(cQuad>1e-13&&sQuad>1e-13,'the quadratic terms are worth '+cQuad.toExponential(2)+' and '+sQuad.toExponential(2)
       +' at the top of the branch, both far above a rounding error');
    ok(Math.abs(C2-(1-x/2))>1e-13&&Math.abs(S2/t-(1-x/6))>1e-13,'... and the two-term series is visibly wrong there');
    /* the invariance that made them untestable at the old join of 1e-8: there the
       quadratic terms are below half an ulp and the double is bit-identical */
    { const xo=1e-8;
      eq(1-xo/2+xo*xo/24,1-xo/2,'at |s|t^2 = 1e-8 the C quadratic term is below half an ulp (bit-identical)');
      eq(1-xo/6+xo*xo/120,1-xo/6,'and so is the Sn one: the old 1e-8 join could not test either'); } }
  eq(CSn(0,0.4)[1],0.4,'CSn at s = 0 exactly: Sn = t, where the direct quotient is 0/0');
  eq(CSn(0,0.4)[0],1,'CSn at s = 0 exactly: C = 1');
  { const r=CSn(9,0.5); rel(r[0],Math.cos(1.5),1e-15,'CSn takes the cosine branch above s = 0');
    rel(r[1],Math.sin(1.5)/3,1e-15,'CSn: Sn on the cosine branch');
    const q=CSn(-9,0.5); rel(q[0],Math.cosh(1.5),1e-15,'CSn takes the cosh branch below s = 0');
    rel(q[1],Math.sinh(1.5)/3,1e-15,'CSn: Sn on the cosh branch'); }

  /* ---------- 4. the integrator: RK4's order, measured ---------- */
  for(const [nm,m,k,b,u0,v0] of [['undamped',0.25,6,0,0.08,0],['damped',0.1,6,0.7,0.05,0],['overdamped',0.1,6,3,0.05,0]]){
    const ex=prop(m,k,b,u0,v0,2);
    let prev=null, orders=[];
    for(const n of [200,400,800,1600]){
      const r=rk4(m,k,b,u0,v0,2,n), e=Math.hypot(r[0]-ex[0],r[1]-ex[1]);
      if(prev!==null) orders.push(Math.log(prev/e)/Math.LN2);
      prev=e;
    }
    for(const o of orders) ok(o>3.9&&o<4.15,nm+': RK4 converges at order '+fmt(o,3)+' (derive: 4.00-4.10)');
    rel(prev,0,1,nm+': RK4 at 1600 steps is within 1e-10 of the propagator');
    ok(prev<1e-10,nm+': RK4 at 1600 steps agrees with the closed form to '+prev.toExponential(2));
  }
  rel(rk4(0.25,6,0,0.08,0,2,200)[0],prop(0.25,6,0,0.08,0,2)[0],1e-5,'RK4 at 200 steps is already within 1e-5');

  /* ---------- 5. the period ---------- */
  rel(omega0(0.25,6),4.898979485566356,1e-15,'w0 at 250 g on 6 N/m (derive)');
  rel(period0(0.25,6),1.282549830161864,1e-15,'T at 250 g on 6 N/m (derive)');
  rel(period0(0.1,6),0.8111557351947223,1e-15,'T at 100 g on 6 N/m (derive)');
  rel(period0(0.1,12),0.5735737209545476,1e-15,'T at 100 g on 12 N/m (derive)');
  rel(period0(0.05,3),0.8111557351947223,1e-15,'T at 50 g on 3 N/m equals 100 g on 6 (same m/k)');
  rel(period0(0.4,6)/period0(0.1,6),2,1e-15,'four times the mass is twice the period');
  rel(gammaOf(0.1,0.7),3.4999999999999996,1e-15,'gam = b/2m (derive)');
  rel(zetaOf(0.1,6,0.7),0.4518480570575319,1e-15,'zeta at 100 g on 6 N/m, b = 0.7 (derive)');
  rel(zetaOf(0.05,3,0.7),0.9036961141150638,1e-15,'zeta at 50 g on 3 N/m, b = 0.7 (derive)');
  rel(omegaD(0.1,6,0.7),6.910137480542628,1e-15,'w_d (derive)');
  rel(periodD(0.1,6,0.7),0.9092706657243222,1e-15,'T_d (derive)');
  rel(periodD(0.05,3,0.7),1.894451650198964,1e-15,'T_d at the most damped state the sim allows (derive)');
  rel(periodD(0.05,3,0.7)/period0(0.05,3),2.335496832484567,1e-14,'and it is 2.335 times the undamped period (derive)');
  rel(logDec(0.1,6,0.7),3.1824473300351275,1e-14,'the logarithmic decrement (derive)');
  rel(Math.exp(-logDec(0.1,6,0.7)),0.041484005733899036,1e-13,'4.1 % of the amplitude survives a period (derive)');
  rel(qFactor(0.1,6,0.7),1.1065666703449764,1e-14,'Q = 1/(2 zeta) (derive)');
  ok(!isFinite(qFactor(0.1,6,0)),'Q is infinite with no damping');
  ok(!isFinite(periodD(0.1,6,2*Math.sqrt(0.6))),'a critically damped spring has no period');
  /* the period MEASURED from the drawn motion, by bisecting for the crossings */
  { const zs=[zeroBetween(0.1,6,0,0.05,0,1e-12,0.5),zeroBetween(0.1,6,0,0.05,0,0.5,0.9),zeroBetween(0.1,6,0,0.05,0,0.9,1.3)];
    rel(zs[0],0.20278893379868057,1e-12,'first crossing, 100 g on 6 N/m (derive)');
    rel(zs[1],0.6083668013960417,1e-12,'second crossing (derive)');
    rel(zs[2],1.0139446689934029,1e-12,'third crossing (derive)'); }
  for(const [m,k,b,T,nm] of [[0.1,6,0,0.8111557351947223,'undamped'],[0.25,6,0,1.2825498301618643,'250 g'],
                             [0.1,12,0,0.5735737209545476,'stiff'],[0.1,6,0.35,0.8326848655149497,'damped'],
                             [0.05,3,0.7,1.8944516501989646,'heavily damped']]){
    rel(measurePeriod(m,k,b,0.05),T,1e-12,'the measured period, '+nm+' (derive)');
    rel(measurePeriod(m,k,b,0.05),periodD(m,k,b),1e-12,'the measured period equals 2 pi / w_d, '+nm);
    rel(measurePeriod(m,k,b,0.02),measurePeriod(m,k,b,0.09),1e-12,'the period does not depend on the amplitude, '+nm);
  }
  /* released from rest, v vanishes EXACTLY at whole half periods, and the
     amplitude is multiplied by e^(-delta/2) at each one */
  for(const [m,k,b] of [[0.1,6,0.35],[0.05,3,0.7],[0.3,12,0.7],[0.25,6,0]]){
    const Td=periodD(m,k,b), ld=logDec(m,k,b), u0=0.05;
    for(let n=1;n<=3;n++) close(prop(m,k,b,u0,0,n*Td/2)[1],0,1e-12,'v = 0 at n = '+n+' half periods (m '+m+', b '+b+')');
    for(let n=1;n<=3;n++) rel(Math.abs(prop(m,k,b,u0,0,n*Td/2)[0]),u0*Math.exp(-ld*n/2),1e-11,
      '|u| at turn '+n+' is u0 e^(-n delta/2) (m '+m+', b '+b+')');
    rel(Math.abs(prop(m,k,b,u0,0,Td)[0]/prop(m,k,b,u0,0,Td/2)[0]),Math.exp(-ld/2),1e-11,'consecutive turns differ by e^(-delta/2)');
  }
  rel(Math.abs(prop(0.1,6,0.35,0.05,0,periodD(0.1,6,0.35))[0]/prop(0.1,6,0.35,0.05,0,periodD(0.1,6,0.35)/2)[0]),0.48258449357063454,1e-12,
      'the peak ratio at b = 0.35 (derive)');
  rel(Math.abs(prop(0.05,3,0.7,0.06,0,periodD(0.05,3,0.7))[0]/prop(0.05,3,0.7,0.06,0,periodD(0.05,3,0.7)/2)[0]),0.0013193965899875686,1e-11,
      'the peak ratio at the most damped state (derive)');
  /* gravity moves the hanging point and NOT the period */
  { const Ts=[G_MOON,G_EARTH,G_PLANETX,G_JUPITER].map(()=>period0(0.1,6));
    for(const T of Ts) eq(T,0.8111557351947223,'the period is bit-identical on every planet (derive)');
    rel(yEq(0.1,6,G_JUPITER)/yEq(0.1,6,G_MOON),15.5,1e-14,'Jupiter stretches it 15.5 times as far as the Moon');
    rel(100*yEq(0.1,6,G_PLANETX),23.666666666666668,1e-13,'Planet X stretches it 23.67 cm (derive)'); }

  /* ---------- 6. the regimes the sim can reach ---------- */
  rel(bCrit(0.05,3),0.7745966692414834,1e-15,'the smallest critical damping over PhET\'s box (derive)');
  rel(bCrit(0.3,12),3.794733192202055,1e-15,'the largest critical damping over PhET\'s box (derive)');
  rel(BMAX/bCrit(0.05,3),0.9036961141150639,1e-15,'so zeta tops out at 0.9037 (derive)');
  rel(bCrit(0.05,3)/BMAX,1.1065666703449764,1e-14,'critical damping is 1.107 times the top of the slider (derive)');
  ok(bCrit(0.05,3)>BMAX,'PhET cannot reach critical damping at all');
  { let worst=0,n=0,anyOver=false;
    for(let i=50;i<=300;i+=5){ const m=i/1000;
      for(let k=3;k<=12;k++) for(let j=0;j<=14;j++){ const b=j*0.05;
        const z=zetaOf(m,k,b); if(z>worst) worst=z; if(z>=1) anyOver=true; n++; } }
    ok(n>=7000,'the reachability sweep covers '+n+' states');
    ok(!anyOver,'not one reachable state is critically or overdamped');
    rel(worst,0.9036961141150639,1e-15,'the worst zeta over the whole sweep is PhET\'s 0.9037'); }
  eq(zetaOf(0.1,6,2*Math.sqrt(0.6))===1,true,'b = 2 sqrt(km) is exactly zeta = 1');
  ok(discr(0.1,6,3)<0,'b = 3 N s/m is overdamped');
  ok(discr(0.1,6,0.7)>0,'b = 0.7 N s/m at 100 g on 6 N/m is underdamped');

  /* ---------- 7. energy ---------- */
  { const m=0.1,k=6,u0=0.05,v0=0.3, E=energyU(m,k,u0,v0);
    rel(E,0.012,1e-15,'E = 1/2 m v^2 + 1/2 k u^2 (derive)');
    const A=Math.sqrt(u0*u0+Math.pow(v0/omega0(m,k),2));
    rel(A,0.06324555320336758,1e-15,'the amplitude sqrt(u0^2 + (v0/w0)^2) (derive)');
    rel(0.5*k*A*A,E,1e-15,'and 1/2 k A^2 is the same energy');
    let worst=0;
    for(let i=1;i<=2000;i++){ const r=prop(m,k,0,u0,v0,i*0.01);
      worst=Math.max(worst,Math.abs(energyU(m,k,r[0],r[1])-E)/E); }
    ok(worst<3e-15,'undamped: the propagator holds the energy to '+worst.toExponential(2)+' over 2000 steps (derive 5.8e-16)');
    const rr=rk4(m,k,0,u0,v0,20,2000);
    rel(Math.abs(energyU(m,k,rr[0],rr[1])-E)/E,5.995482030979327e-06,2e-6,'RK4 drifts 6.0e-6 over the same 20 s (derive)'); }
  /* dE/dt = -b v^2, by central difference */
  for(const [m,k,b] of [[0.1,6,0.35],[0.25,6,0.7],[0.1,6,0]]){
    for(const t of [0.17,0.63]){
      const hh=1e-5, p1=prop(m,k,b,0.05,0,t+hh), p2=prop(m,k,b,0.05,0,t-hh), p0=prop(m,k,b,0.05,0,t);
      const dE=(energyU(m,k,p1[0],p1[1])-energyU(m,k,p2[0],p2[1]))/(2*hh);
      close(dE,-b*p0[1]*p0[1],1e-8,'dE/dt = -b v^2 at t = '+t+' (b '+b+')');
    } }
  /* the ledger with gravity: KE + PE_elastic + PE_gravity is constant, and the
     constant is -(mg)^2/2k */
  { const m=0.1,k=6,g=G_EARTH, ye=yEq(m,k,g), u0=0.08, ybot=swingBottom(m,k,g);
    rel(ybot,0.3266666666666667,1e-15,'the bottom of the swing, y_bot = 2mg/k (derive)');
    rel(gravOffset(m,k,g),0.24010000000000006,1e-14,'the constant 3(mg)^2/2k (derive)');
    rel(energyU(m,k,u0,0)+gravOffset(m,k,g),0.25930000000000003,1e-14,'the invariant of the ledger (derive)');
    rel(ledgerTotal(m,k,g),0.3201333333333334,1e-14,'the ledger total at the release, 2(mg)^2/k (derive)');
    rel(ledgerTotal(m,k,g),energyU(m,k,-ye,0)+gravOffset(m,k,g),1e-15,'... which is E(release) + the constant');
    rel(peGrav(m,g,0,ybot),0.32013333333333344,1e-13,'at the release gravity holds all of it (derive)');
    ok(peGrav(m,g,ybot,ybot)===0,'and none of it at the bottom');
    let worst=0, neg=false;
    for(let i=0;i<=400;i++){ const t=i*0.01, r=prop(m,k,0,u0,0,t), y=r[0]+ye;
      const S3=keOf(m,r[1])+peElastic(k,y)+peGrav(m,g,y,ybot);
      if(keOf(m,r[1])<0||peElastic(k,y)<0||peGrav(m,g,y,ybot)<-1e-15) neg=true;
      worst=Math.max(worst,Math.abs(S3-(energyU(m,k,u0,0)+gravOffset(m,k,g)))); }
    ok(worst<1e-15,'the three shares add to that constant to '+worst.toExponential(2)+' J over four seconds');
    ok(!neg,'and with this datum not one of them ever goes negative');
    const r2=prop(m,k,0,u0,0,0.2), y2=r2[0]+ye;
    rel(keOf(m,r2[1]),0.01919104096302817,1e-12,'KE at t = 0.2 s (derive)');
    rel(peElastic(k,y2),0.08173583492047881,1e-12,'the elastic share at t = 0.2 s (derive)');
    rel(peGrav(m,g,y2,ybot),0.1583731241164931,1e-12,'the gravitational share at t = 0.2 s (derive)'); }
  /* released from the unstretched end: the swing is exactly 2mg/k */
  for(const [m,k,g] of [[0.1,6,G_EARTH],[0.25,3,G_JUPITER],[0.05,12,G_MOON]]){
    const ye=yEq(m,k,g), r=prop(m,k,0,-ye,0,period0(m,k)/2);
    rel(r[0]+ye,2*ye,1e-14,'let go from y = 0, it reaches exactly 2mg/k (m '+m+', k '+k+')');
    close(r[1],0,1e-13,'and arrives there at rest'); }
  { const m=0.1,k=6,g=G_EARTH, ye=yEq(m,k,g), b=0.35, E0=energyU(m,k,-ye,0);
    rel(E0,0.08003333333333335,1e-14,'the starting energy is (mg)^2/2k');
    const r=prop(m,k,b,-ye,0,2);
    rel(E0-energyU(m,k,r[0],r[1]),E0*0.9992548613609622,2e-9,'the damper has taken 99.93 % by t = 2 s (derive)'); }
  { /* the thermal ledger of the run the energy view draws, at b = 0.35 and u0 = 0.08 */
    const m=0.1,k=6,b=0.35,u0=0.08, E0=energyU(m,k,u0,0);
    rel(E0,0.0192,1e-15,'E(0) = 1/2 k u0^2 (derive)');
    for(const [t,E] of [[0.5,0.004198777583040618],[1,0.0007141714312805042],[2,1.4306661869525964e-05]]){
      const r=prop(m,k,b,u0,0,t); rel(energyU(m,k,r[0],r[1]),E,1e-11,'E at t = '+t+' s (derive)'); } }

  /* ---------- 8. the stage geometry ---------- */
  rel(CEILING_Y-L0,0.97,1e-15,'the spring bottom at its natural length (derive)');
  { const t=coilPoints(1.2,CEILING_Y,0.5,40);
    eq(t[0][0],1.2,'the coil starts on the spring axis'); eq(t[0][1],CEILING_Y,'and at the ceiling');
    close(t[t.length-1][1],CEILING_Y-0.5,1e-15,'and ends exactly a spring length down');
    let mx=0; for(const p of t) mx=Math.max(mx,Math.abs(p[0]-1.2));
    /* an ABSOLUTE number, not COIL_R: comparing the measured width against the
       constant that produced it moves both sides together (Known-bad) */
    close(mx,0.045,1e-15,'the coil is 4.5 cm wide about the spring axis');
    close(coilPoints(1.2,CEILING_Y,0.5,200).reduce((a,p)=>Math.max(a,Math.abs(p[0]-1.2)),0),0.045,1e-15,
          '... at five times the sampling too'); }
  /* and the same constant, measured off the DRAWING: the display list the
     spring emits must span 2 x 4.5 cm about its axis, in pixels */
  { const shot=makeShot(900,700);
    const mp=worldFitUp(box(0,0,600,600),{xmin:0.7,xmax:1.7,ymin:0,ymax:1.6},0.01);
    LABELS=[]; POLY_SEGS=[];
    drawSpring(shot,mp,1.2,0.5,6,'#fff');
    let lo=Infinity,hi=-Infinity;
    for(let i=0;i<POLY_SEGS.length;i+=2){ const X=POLY_SEGS[i]; if(X<lo) lo=X; if(X>hi) hi=X; }
    ok(POLY_SEGS.length>=800,'the drawn coil records '+(POLY_SEGS.length/4)+' segments');
    rel(hi-lo,2*0.045*mp.s,1e-12,'the drawn coil spans 9.0 cm across, in pixels ('+fmt(hi-lo,2)+' px at '+fmt(mp.s,2)+' px/m)');
    rel((hi+lo)/2,mp.X(1.2),1e-9,'and is centred on the spring axis');
    POLY_SEGS=[]; }
  ok(coilWidth(KMAX)>coilWidth(KMIN),'a stiffer spring is drawn with a heavier wire');
  { const s=springModel(ST,{i:0,x:1,k:3,m:0.3,myst:false,name:'',label:''},24.8,0);
    LIVE.slot[0].y=2.48;
    const s2=springModel(ST,{i:0,x:1,k:3,m:0.3,myst:false,name:'',label:''},24.8,0);
    rel(s2.bottom,-1.51,1e-14,'300 g on 3 N/m on Jupiter hangs 1.51 m below the floor (derive)');
    ok(s2.floorBust,'and the model says so');
    LIVE.slot[0].y=0; ok(!springModel(ST,{i:0,x:1,k:6,m:0.1,myst:false,name:'',label:''},9.8,0).floorBust,'the default does not'); }

  /* ---------- 9. the live path: stepping, crossings, the traced period ---- */
  withState({view:'lab',kl:6,labMass:'adj',massG:100,body:'earth',damping:0},()=>{
    const ye=yEq(0.1,6,G_EARTH);
    close(LIVE.slot[2].y,0,1e-15,'the lab mass starts at the unstretched end');
    for(let i=0;i<400;i++) advance(ST,0.005);
    close(LIVE.t,2,1e-12,'400 steps of 5 ms is 2 s');
    const ex=prop(0.1,6,0,-ye,0,2);
    rel(LIVE.slot[2].y,ex[0]+ye,1e-13,'stepping 400 times equals one 2-second propagation');
    rel(LIVE.slot[2].v,ex[1],1e-13,'and so does the velocity');
    const T=tracedPeriod(2);
    rel(T,period0(0.1,6),1e-9,'the trace measures 2 pi sqrt(m/k) from the live crossings');
    ok(LIVE.slot[2].cross.length>=3,'it has recorded '+LIVE.slot[2].cross.length+' crossings');
    ok(LIVE.slot[2].hist.length===400,'and 400 history points');
  });
  withState({view:'lab',kl:9,massG:250,body:'jupiter',damping:0.4},()=>{
    for(let i=0;i<900;i++) advance(ST,0.004);
    rel(tracedPeriod(2),periodD(0.25,9,0.4),1e-8,'the trace measures the DAMPED period when there is damping');
  });
  withState({view:'bnc',k1:3,k2:12,mass1:'m250',mass2:'m50',damping:0},()=>{
    for(let i=0;i<300;i++) advance(ST,0.005);
    const M=buildModel();
    const e1=prop(0.25,3,0,-yEq(0.25,3,G_EARTH),0,1.5), e2=prop(0.05,12,0,-yEq(0.05,12,G_EARTH),0,1.5);
    rel(M.springs[0].y,e1[0]+yEq(0.25,3,G_EARTH),1e-13,'spring 1 follows its own closed form');
    rel(M.springs[1].y,e2[0]+yEq(0.05,12,G_EARTH),1e-13,'spring 2 follows its own closed form');
    ok(M.springs[0].T0!==M.springs[1].T0,'and the two springs keep different periods');
  });
  withState({view:'str'},()=>{
    /* gam = b/2m = 1.4 at 250 g and b = 0.7, so 12 s leaves e^(-16.8) = 5e-8 of it */
    for(let i=0;i<1200;i++) advance(ST,0.01);
    const M=buildModel();
    rel(M.springs[0].y,M.springs[0].ye,1e-6,'at the Stretch screen damping the mass has settled on mg/k after 12 s');
    close(M.springs[0].v,0,1e-6,'and stopped');
  });
  withState({view:'bnc',mass1:'none',mass2:'none'},()=>{
    for(let i=0;i<50;i++) advance(ST,0.01);
    const M=buildModel();
    ok(!M.springs[0].on&&M.springs[0].y===0,'an empty spring stays at its natural length');
  });
  /* slow motion is PhET's x1/8 */
  withState({view:'bnc',speed:'slow'},()=>{
    const S=makeScene({getContext:()=>makeShot(900,600)});
    S.step(0.08); close(LIVE.t,0.01,1e-15,'slow motion advances one eighth of the wall clock');
  });
  withState({view:'per'},()=>{
    const S=makeScene({getContext:()=>makeShot(900,600)});
    ok(S.step(0.02)===false,'the analysis views carry no clock');
  });

  /* ---------- 10. the model the panels are built from ---------- */
  const PRESETS=[{},{body:'moon'},{body:'jupiter'},{body:'planetX'},{body:'custom',gCustom:0},{body:'custom',gCustom:30},
                 {k1:3,k2:12},{mass1:'none',mass2:'none'},{mass1:'q200',mass2:'q75',reveal:true},{mass1:'q100',mass2:'q75'},
                 {labMass:'q180'},{labMass:'q120',reveal:true},{massG:50},{massG:300},{kl:3},{kl:12},
                 {damping:0},{damping:0.7},{zeta:0},{zeta:1},{zeta:2},{kA:3,mAg:50},{kA:12,mAg:300},
                 {ruler:true,movLine:true,stopwatch:true},{natLine:false,restLine:false,trace:false}];
  for(const [v] of TABS) for(const pre of PRESETS){
    withState(Object.assign({view:v},pre),()=>{
      const M=buildModel();
      const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M)+(INFO[v]||'')+(DERIV[v]||'');
      ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0,v+' panels are clean for '+JSON.stringify(pre));
      /* a non-finite-safe formatter makes the check above vacuous, so demand a
         number that must be there: the readout always names PhET's own 14.2 */
      ok(readoutHTML(M).indexOf('14.2')>=0,v+' readout names PhET\'s Planet X value');
      for(const s of M.springs){ if(!s.on) continue;
        ok(isFinite(s.ye)&&isFinite(s.T0)&&isFinite(s.y)&&isFinite(s.v)&&isFinite(s.E),v+' spring model finite for '+JSON.stringify(pre)); }
      if(v==='per'){ const P=M.per; ok(P.curves.every(c=>c.T.every(isFinite))&&isFinite(P.T0),'per model finite'); }
      if(v==='dmp'){ const D=M.dmp; ok(D.curves.every(c=>c.u.every(isFinite)),'dmp model finite'); }
      if(v==='eng'){ const E=M.eng; ok(E.TOT.every(isFinite)&&E.drift<1e-12,'eng ledger flat to '+E.drift.toExponential(2)); }
    });
  }
  withState({view:'eng',damping:0,kl:6,labMass:'adj',massG:100},()=>{
    const E=buildModel().eng;
    ok(E.drift<4e-16,'with no damping the four shares add to a constant to '+E.drift.toExponential(2)+' J');
    rel(E.Etot,energyU(0.1,6,-yEq(0.1,6,G_EARTH),0)+gravOffset(0.1,6,G_EARTH),1e-15,'and that constant is E0 - (mg)^2/2k');
  });
  withState({view:'eng',damping:0.4},()=>{
    const E=buildModel().eng;
    ok(E.TH[E.TH.length-1]>E.TH[0],'with damping the thermal share only grows');
    let mono=true; for(let i=1;i<E.TH.length;i++) if(E.TH[i]<E.TH[i-1]-1e-15) mono=false;
    ok(mono,'and it never goes down');
    ok(E.drift<1e-12,'the ledger still closes to '+E.drift.toExponential(2)+' J');
  });

  /* ---------- 10b. the same numbers, read off the BUILT model ----------
     (Known-bad: a test that re-derives the thing it is testing tests nothing —
     these read the objects the readout and the canvas are drawn from) */
  withState({view:'str'},()=>{
    const M=buildModel(), s0=M.springs[0], s1=M.springs[1];
    rel(s0.ye,0.4083333333333334,1e-15,'model: spring 1 resting extension (250 g, 6 N/m, Earth)');
    rel(s1.ye,0.08166666666666668,1e-15,'model: spring 2 resting extension (50 g, 6 N/m, Earth)');
    rel(s0.T0,1.282549830161864,1e-15,'model: spring 1 period');
    rel(s1.T0,0.5735737209545476,1e-15,'model: spring 2 period');
    rel(s0.bc,2.449489742783178,1e-15,'model: spring 1 critical damping');
    rel(s0.zeta,0.7/2.449489742783178,1e-15,'model: spring 1 zeta at the Stretch screen damping');
    rel(s0.E0,0.5*6*0.4083333333333334*0.4083333333333334,1e-15,'model: the energy of a release from the unstretched end');
    eq(M.g,9.8,'model: PhET\'s Earth gravity'); eq(M.gReal,9.81,'model: the real one beside it');
    rel(s0.bottom,CEILING_Y-L0,1e-15,'model: at t = 0 the spring is at its natural length');
    rel(s1.off,1.5*0.05*0.05*9.8*9.8/6,1e-15,'model: spring 2 gravitational offset 3(mg)^2/2k');
    rel(s0.ybot,2*0.4083333333333334,1e-15,'model: spring 1 swing bottom, 2mg/k');
    ok(s0.PEg>=0&&s1.PEg>=0,'model: the gravitational share starts non-negative');
  });
  withState({view:'per',kA:6,mAg:100,damping:0.7},()=>{
    const P=buildModel().per;
    rel(P.T0,0.8111557351947223,1e-15,'model: the period law view\'s T');
    rel(P.Td,periodD(0.1,6,0.7),1e-15,'model: and its damped period');
    rel(P.zMaxPhet,0.9036961141150639,1e-15,'model: the reachable zeta ceiling the shaded band uses');
    eq(P.planets.length,4,'model: four named gravities');
    eq(P.planets.map(x=>x.name).join(','),'Moon,Earth,Planet X,Jupiter','model: in PhET\'s own order');
    rel(P.planets[3].ye/P.planets[0].ye,24.8/1.6,1e-14,'model: Jupiter stretches it 15.5x the Moon');
    for(const pl of P.planets) eq(pl.T,P.T0,'model: '+pl.name+' shares the same period');
    for(const p2 of P.pts) rel(p2.T,p2.T0,1e-12,'model: the measured point at '+fmt(1000*p2.m,0)+' g sits on the curve');
    rel(P.curves[0].T[0],period0(MASS_G_MIN/1000,3),1e-15,'model: the k = 3 curve starts at 50 g');
  });
  withState({view:'dmp',kA:6,mAg:100,zeta:0.25},()=>{
    const D=buildModel().dmp;
    rel(D.bc,1.5491933384829668,1e-15,'model: 2 sqrt(km) at 100 g on 6 N/m');
    rel(D.bcMin,0.7745966692414834,1e-15,'model: the smallest 2 sqrt(km) the shaded box uses');
    rel(D.bcMax,3.794733192202055,1e-15,'model: and the largest');
    rel(D.zMax,0.9036961141150639,1e-15,'model: the reachable zeta ceiling');
    ok(D.reach,'model: zeta = 0.25 is inside PhET\'s damping range');
    rel(D.curves[0].b,0.25*1.5491933384829668,1e-15,'model: the drawn b is zeta x 2 sqrt(km)');
    eq(D.curves[1].z,1,'model: the second curve is critical');
    ok(D.curves[1].b>BMAX,'model: and it is beyond PhET\'s range');
    rel(D.ld,logDec(0.1,6,0.25*D.bc),1e-15,'model: the log decrement');
    for(let n=0;n<D.peaks.length;n++) rel(Math.abs(D.peaks[n].u),D.u0*Math.exp(-D.ld*n),1e-11,'model: peak '+n+' is u0 e^(-n delta)');
  });
  withState({view:'dmp',zeta:1.4},()=>{ const D=buildModel().dmp;
    ok(!D.reach,'model: zeta = 1.4 is beyond PhET\'s damping range');
    ok(!isFinite(D.Td)&&D.peaks.length===0,'model: and it has no turning points to count'); });

  /* ---------- 11. the pointer: the three things PhET lets you drag ------- */
  withState({view:'str',ruler:true,movLine:true},()=>{
    const shot=makeShot(1100,700), S=makeScene({getContext:()=>shot});
    S.W=1100; S.H=700;
    const M=buildModel(), L=layoutFor(shot,1100,700,'str'), map=stageMap(M,L.main);
    const s0=M.springs[0], r=massRectPx(map,s0);
    ok(S.pointer('down',(r.x+r.x1)/2,(r.y+r.y1)/2),'grab the hanging mass');
    eq(DRAG.what,'mass','the mass is what was grabbed'); eq(DRAG.sp,0,'and it is spring 1');
    const y0=LIVE.slot[0].y;
    S.pointer('move',(r.x+r.x1)/2,(r.y+r.y1)/2+40);
    rel(LIVE.slot[0].y-y0,40/map.s,1e-9,'it follows the pointer down, keeping the grab offset');
    LIVE.slot[0].v=0.7; S.pointer('up',0,0);
    eq(LIVE.slot[0].v,0,'letting go leaves it at rest, as PhET does');
    const lx=map.X(1.0), ly=map.Y(ST.movY);
    ok(S.pointer('down',lx,ly+2),'grab the movable line'); eq(DRAG.what,'movline','the movable line');
    S.pointer('move',lx,map.Y(0.5)+2); close(ST.movY,0.5,1e-9,'it follows to 0.5 m'); S.pointer('up',0,0);
    const rx=map.X(ST.rulerX+RULER_W/2), ry=map.Y(ST.rulerY-0.3);
    ok(S.pointer('down',rx,ry),'grab the ruler'); eq(DRAG.what,'ruler','the ruler');
    const rx0=ST.rulerX; S.pointer('move',rx+55,ry); rel(ST.rulerX-rx0,55/map.s,1e-9,'it follows the pointer sideways'); S.pointer('up',0,0);
    ok(!S.pointer('down',map.X(1.15),map.Y(1.40)),'empty stage grabs nothing');
  });
  withState({view:'str',ruler:false,movLine:false},()=>{
    const shot=makeShot(1100,700), S=makeScene({getContext:()=>shot}); S.W=1100; S.H=700;
    const M=buildModel(), L=layoutFor(shot,1100,700,'str'), map=stageMap(M,L.main);
    ok(!S.pointer('down',map.X(ST.rulerX+0.03),map.Y(ST.rulerY-0.3)),'a hidden ruler cannot be grabbed');
    ok(!S.pointer('down',map.X(1.0),map.Y(ST.movY)),'nor a hidden movable line');
  });
  for(const v of ['per','dmp','eng']) withState({view:v},()=>{
    const S=makeScene({getContext:()=>makeShot(1100,700)});
    ok(!S.pointer('down',400,300),'the '+v+' view ignores the pointer');
  });

  /* ---------- 12. the drawing: layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['str default',{view:'str'},60],['str settled',{view:'str',_live:300},60],
    ['str soft/stiff',{view:'str',k1:3,k2:12,mass1:'m250',mass2:'m50',_live:200},59],
    ['str jupiter',{view:'str',body:'jupiter',k1:3,mass1:'m250',_live:200},58],
    ['str moon tools',{view:'str',body:'moon',ruler:true,movLine:true,stopwatch:true,_sw:3.21,_live:150},144],
    ['str empty',{view:'str',mass1:'none',mass2:'none'},46],
    ['str mystery',{view:'str',mass1:'q200',mass2:'q75',_live:200},59],
    ['str through the floor',{view:'str',body:'custom',gCustom:30,k1:3,mass1:'m250',_live:200},56],
    ['bnc start',{view:'bnc'},51],['bnc mid',{view:'bnc',_live:90},53],
    ['bnc damped',{view:'bnc',damping:0.5,_live:200},55],
    ['bnc slow',{view:'bnc',speed:'slow',_live:60},53],
    ['lab default',{view:'lab',_live:200},47],['lab planetX',{view:'lab',body:'planetX',_live:250},50],
    ['lab heavy soft',{view:'lab',kl:3,massG:300,_live:300},56],
    ['lab light stiff damped',{view:'lab',kl:12,massG:50,damping:0.6,_live:250},44],
    ['lab mystery + tools',{view:'lab',labMass:'q180',ruler:true,movLine:true,trace:true,_live:250},138],
    ['lab zero g',{view:'lab',body:'custom',gCustom:0,_live:200},51],
    ['per default',{view:'per'},68],['per corner',{view:'per',kA:3,mAg:300,damping:0.7},66],
    ['per stiff light',{view:'per',kA:12,mAg:50,damping:0.7},68],
    ['dmp default',{view:'dmp'},62],['dmp critical',{view:'dmp',zeta:1},62],['dmp over',{view:'dmp',zeta:2},62],
    ['dmp tiny',{view:'dmp',zeta:0.02,kA:3,mAg:300},64],['dmp zero',{view:'dmp',zeta:0},62],
    ['eng undamped',{view:'eng',damping:0,_live:120},52],['eng damped',{view:'eng',damping:0.5,_live:120},52],
    ['eng moon',{view:'eng',body:'moon',damping:0.2,kl:12,massG:60,_live:80},56],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,minOps] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      /* floor the TOTAL ops, derived from what each configuration emits: a
         fill count punishes a view for batching and misses a blank one */
      ok(c.ops.length>=minOps&&texts.length>=3&&fills.length>=1,
         nm+' '+W+'x'+H+' draws substance ('+c.ops.length+' ops, floor '+minOps+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    });
  }

  Object.assign(ST,stSave); liveReset();
  const dt=(Date.now()-T0w)/1000;
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
