
/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/under-pressure/refvals.txt, the        *
 *  printed output of build/under-pressure/derive.py, read in full     *
 *  (scipy.integrate.quad, scipy.optimize.brentq, a 400 000-strip      *
 *  Riemann sum).  Nothing here re-types a formula from p2_physics.js: *
 *  every pin is either an absolute number from that file or a second, *
 *  independent route computed here.                                   *
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
/* the signed area of a closed world polygon (shoelace) */
function polyAreaW(pts){
  let a=0;
  for(let i=0;i<pts.length;i++){ const p=pts[i], q=pts[(i+1)%pts.length];
    a+=p[0]*q[1]-q[0]*p[1]; }
  return Math.abs(a)/2;
}

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    const keep=Object.assign({},ST);
    Object.assign(ST,over); clearAll();
    try{ return fn(); } finally { Object.assign(ST,keep); clearAll(); }
  }

  /* ---------------- 1. the units, from their definitions --------------- */
  eq(PA_PER_ATM,101325,'1 atm is 101325 Pa by definition');
  close(LBF_N,4.4482216152604996,1e-12,'1 lbf = 4.4482216152605 N (derive)');
  close(PA_PER_PSI,6894.7572931683608,1e-9,'1 psi = 6894.7572931683608 Pa (derive)');
  close(PA_PER_ATM/PA_PER_PSI,14.69594877551345,1e-12,'1 atm = 14.69594877551345 psi (derive)');
  close(PA_PER_ATM/PA_PER_KPA,101.325,1e-12,'1 atm = 101.325 kPa exactly');
  close(1/FT_M,3.280839895013123,1e-12,'1 m = 3.280839895013123 ft (derive)');
  close(3/FT_M,9.8425196850393704,1e-12,'3 m = 9.8425196850393704 ft (derive)');
  /* a second route to the psi: build it from the atm and the printed ratio */
  close(PA_PER_PSI,PA_PER_ATM/14.69594877551345,1e-9,'the psi, reached back through the atm');
  /* PhET's rounded factors, and how far off they are */
  close(Math.abs(PA_PER_ATM*PHET_ATM_PER_PA-1),3.310e-6,1e-8,"PhET's atm factor is 3.31e-6 atm out (derive)");
  ok(Math.abs(PA_PER_ATM*PHET_PSI_PER_PA-PA_PER_ATM/PA_PER_PSI)>1e-5,"PhET's psi factor is measurably out");
  close(Math.abs(PHET_FT_PER_M-1/FT_M)*FT_M,1.52e-9,1e-10,"PhET's ft/m is 1.52e-9 relative out (derive)");
  {
    let worst=0;
    for(let i=0;i<=4000;i++){ const pa=i*1000;
      for(const u of ['metric','atmosphere','english']){
        const back=fromUnit(toUnit(pa,u),u);
        if(pa>0) worst=Math.max(worst,Math.abs(back-pa)/pa);
      } }
    ok(worst<1e-15,'every unit round trip over 0-4 MPa is exact to '+worst.toExponential(2)+' (derive: 1.434e-16)');
    close(worst,1.434e-16,2e-16,'the worst round-trip error matches derive');
  }
  eq(toUnit(PA_PER_ATM,'atmosphere'),1,'101325 Pa is exactly 1 atm');
  eq(toUnit(1000,'metric'),1,'1000 Pa is exactly 1 kPa');
  close(toLen(3,'english'),9.8425196850393704,1e-12,'the ruler in feet (derive)');
  eq(toLen(3,'metric'),3,'the ruler in metres is the identity');

  /* ---------------- 2. the air model ----------------------------------- */
  close(LAPSE,-12.233333333333333,1e-12,'the air lapse is -12.2333 Pa/m (derive)');
  eq(airP(0,G_EARTH,true),101325,'air at the ground on Earth is exactly 1 atm');
  close(airP(150,G_EARTH,true),99490,1e-9,"air at 150 m is PhET's 99490 Pa");
  close(airP(0,G_JUPITER,true),257448.21428571423,1e-7,'air at the ground on Jupiter (derive)');
  close(airP(2.5,G_EARTH,true),101294.41666666667,1e-8,'air at 2.5 m (derive)');
  eq(airP(0,G_EARTH,false),0,'the atmosphere switch removes the intercept exactly');
  eq(airP(-2,G_JUPITER,false),0,'...at every height and gravity');
  close(H_SCALE,8434.5098187745771,1e-8,'the isothermal scale height (derive)');
  close(airExact(150),99538.956704140233,1e-7,'the exact exponential at 150 m (derive)');
  {
    let worst=0;
    for(let i=0;i<=1000;i++){ const y=i*0.15; worst=Math.max(worst,Math.abs(airP(y,G_EARTH,true)-airExact(y))); }
    close(worst,48.956704140233342,1e-6,'linear vs exponential air, worst gap over 0-150 m (derive)');
    ok(worst/P_AIR_0<6e-4,'that is under 0.06 % of an atmosphere');
  }
  /* the scaling is linear in g, and exactly so */
  close(airP(0,2*G_EARTH,true),2*airP(0,G_EARTH,true),1e-9,'the air pressure scales exactly with g');

  /* ---------------- 3. the hydrostatic law ----------------------------- */
  const HP=[ /* fluid, gravity, depth, p with atmosphere, p without  (derive) */
    [700,3.71,0,38358.75,0],[700,3.71,1.5,42254.25,3895.5],[700,3.71,3,46149.75,7791],
    [700,9.8,0,101325,0],[700,9.8,1.5,111615,10290.000000000002],[700,9.8,3,121905,20580.000000000004],
    [700,24.9,0,257448.21428571423,0],[700,24.9,1.5,283593.2142857142,26145],[700,24.9,3,309738.2142857142,52290],
    [1000,3.71,0,38358.75,0],[1000,3.71,1.5,43923.75,5565],[1000,3.71,3,49488.75,11130],
    [1000,9.8,0,101325,0],[1000,9.8,1.5,116025,14700],[1000,9.8,3,130725,29400],
    [1000,24.9,0,257448.21428571423,0],[1000,24.9,1.5,294798.2142857142,37350],[1000,24.9,3,332148.2142857142,74700],
    [1420,3.71,0,38358.75,0],[1420,3.71,1.5,46261.050000000003,7902.2999999999993],[1420,3.71,3,54163.349999999999,15804.599999999999],
    [1420,9.8,0,101325,0],[1420,9.8,1.5,122199,20874.000000000004],[1420,9.8,3,143073,41748.000000000007],
    [1420,24.9,0,257448.21428571423,0],[1420,24.9,1.5,310485.2142857142,53037],[1420,24.9,3,363522.2142857142,106074]];
  for(const [rho,g,d,pa,pb] of HP){
    close(pressureAt(d,rho,g,0,true),pa,1e-7,'p(rho='+rho+', g='+g+', h='+d+') with the atmosphere (derive)');
    close(pressureAt(d,rho,g,0,false),pb,1e-7,'p(rho='+rho+', g='+g+', h='+d+') without it (derive)');
  }
  eq(HP.length,27,'all 3 fluids x 3 gravities x 3 depths are pinned');
  /* an INDEPENDENT route: integrate dp/dy = -rho g downward in 4000 slabs */
  for(const [rho,g,d] of [[700,3.71,3],[1000,9.8,1.5],[1420,24.9,3]]){
    let p=airP(0,g,true); const N=4000, dy=d/N;
    for(let i=0;i<N;i++) p+=rho*g*dy;
    rel(p,pressureAt(d,rho,g,0,true),5e-13,'p by slab integration, rho='+rho+' g='+g+' h='+d);
  }
  /* the surface reads exactly the air pressure, and zero without it */
  for(const rho of [700,1000,1420]) for(const g of [3.71,9.8,24.9]){
    eq(pressureAt(0,rho,g,0,true)-airP(0,g,true),0,'at h = 0 the gauge reads exactly the air ('+rho+', '+g+')');
    eq(pressureAt(0,rho,g,0,false),0,'...and exactly zero with the atmosphere off ('+rho+', '+g+')');
  }
  /* the slider corners in all three units (derive) */
  close(toUnit(pressureAt(3,700,3.71,0,true),'atmosphere'),0.45546262028127316,1e-12,'700/3.71/3 m in atm (derive)');
  close(toUnit(pressureAt(3,700,3.71,0,true),'english'),6.6934553368147229,1e-10,'700/3.71/3 m in psi (derive)');
  close(toUnit(pressureAt(3,700,24.9,0,true),'atmosphere'),3.0568785026964145,1e-12,'700/24.9/3 m in atm (derive)');
  close(toUnit(pressureAt(3,1420,3.71,0,true),'english'),7.8557297518895277,1e-10,'1420/3.71/3 m in psi (derive)');
  close(toUnit(pressureAt(3,1420,24.9,0,true),'atmosphere'),3.587685312466955,1e-12,'1420/24.9/3 m in atm (derive)');
  close(toUnit(pressureAt(3,1420,24.9,0,true),'english'),52.724439574676332,1e-9,'1420/24.9/3 m in psi (derive)');
  /* every leading factor pinned: halving rho halves the gauge term, not the air */
  {
    const a=pressureAt(2,1000,9.8,0,true)-airP(0,9.8,true);
    const b=pressureAt(2,500,9.8,0,true)-airP(0,9.8,true);
    rel(a,2*b,1e-14,'the gauge term is exactly linear in rho');
    const c=pressureAt(1,1000,9.8,0,false), d2=pressureAt(2,1000,9.8,0,false);
    rel(d2,2*c,1e-14,'and exactly linear in the depth');
  }
  /* the whole control space is finite, non-negative, and hits derive's max */
  {
    let n=0, lo=Infinity, hi=-Infinity, bad=0;
    for(let i=0;i<=20;i++) for(let j=0;j<=20;j++) for(let k=0;k<=12;k++) for(const atm of [true,false]){
      const rho=RHO_GASOLINE+i*(RHO_HONEY-RHO_GASOLINE)/20;
      const g=G_MARS+j*(G_JUPITER-G_MARS)/20;
      const v=pressureAt(k*POOL_H/12,rho,g,0,atm);
      if(!isFinite(v)||v<0) bad++;
      lo=Math.min(lo,v); hi=Math.max(hi,v); n++;
    }
    eq(n,11466,'the slider sweep is derive.py\'s 11466 combinations');
    eq(bad,0,'not one of them is non-finite or negative');
    eq(lo,0,'the smallest is exactly zero (no atmosphere, no depth)');
    close(hi,363522.2142857142,1e-7,'the largest is honey on Jupiter at 3 m (derive)');
  }

  /* ---------------- 4. the pools --------------------------------------- */
  close(SQ_W,3.7000000000000002,1e-12,'the square pool is 3.70 m across (PhET 2.3..6.0)');
  close(SQ_A,7.4000000000000004,1e-12,'its plan area is 7.40 m2 (derive)');
  close(SQ_VMAX,22.200000000000003,1e-10,'it holds 22.2 m3 = 22200 L (derive)');
  /* the trapezoid: the two tapers cancel, at EVERY height */
  {
    let worst=0;
    for(let i=0;i<=40;i++){ const t=POOL_H*i/40, l=tzLeft(t), r=tzRight(t);
      worst=Math.max(worst,Math.abs((l[1]-l[0])+(r[1]-r[0])-TZ_WSUM)); }
    ok(worst<1e-12,'the two chamber widths sum to '+TZ_WSUM+' m at 41 heights (worst '+worst.toExponential(2)+')');
    close(tzLeft(0)[1]-tzLeft(0)[0],3.1500000000000004,1e-12,'left chamber 3.15 m wide at the floor (derive)');
    close(tzLeft(POOL_H)[1]-tzLeft(POOL_H)[0],0.70000000000000018,1e-12,'and 0.70 m at the top (derive)');
    close(tzRight(0)[1]-tzRight(0)[0],0.69999999999999929,1e-12,'right chamber 0.70 m at the floor (derive)');
    close(tzRight(POOL_H)[1]-tzRight(POOL_H)[0],3.1500000000000004,1e-12,'and 3.15 m at the top (derive)');
    ok(Math.abs((tzLeft(0)[1]-tzLeft(0)[0])-(tzRight(0)[1]-tzRight(0)[0]))>2,
       'the two chambers are genuinely different shapes, not a symmetric pair');
  }
  close(TZ_WCHAN,5.1449999999999996,1e-12,'the floor band is 5.145 m wide (derive)');
  close(TZ_VCHAN,2.1608999999999994,1e-10,'the floor channel holds 2.1609 m3 (derive)');
  close(TZ_VMAX,23.643899999999995,1e-9,'the trapezoid pool holds 23.6439 m3 (derive)');
  close(tzVolume(0.1),1.0289999999999999,1e-12,'V(t = 0.1) (derive, quad)');
  close(tzVolume(0.21),2.1608999999999994,1e-10,'V(t = 0.21) (derive, quad)');
  close(tzVolume(1.0),8.2438999999999982,1e-10,'V(t = 1.0) (derive, quad)');
  close(tzVolume(2.5),19.793899999999997,1e-9,'V(t = 2.5) (derive, quad)');
  close(tzVolume(3.0),23.643899999999995,1e-9,'V(t = 3.0) (derive, quad)');
  /* the volume by an independent 20000-strip sum of the width */
  {
    const N=20000; let V=0;
    for(let i=0;i<N;i++) V+=tzWidth((i+0.5)*POOL_H/N)*(POOL_H/N)*DEPTH_OUT;
    rel(V,tzVolume(POOL_H),1e-4,'V(full) against a 20000-strip sum of the width');
  }
  for(const V of [1.0,TZ_VCHAN,5.0,TZ_VMAX]) rel(tzVolume(tzLevel(V)),V,1e-12,'volume <-> level round trip at V = '+fmt(V,4));
  eq(tzLevel(0),0,'an empty trapezoid pool has zero level');
  close(tzLevel(TZ_VMAX),POOL_H,1e-12,'a full one reaches the top');
  ok(tzWidth(0.1)>tzWidth(0.3),'the cross-section is wider inside the floor channel than above it');
  /* the channel really connects both chambers at every height of the band,
     and PhET's own 6.0 m channel really does NOT (the reason this file moved it) */
  {
    let connected=true, phetGap=0;
    for(let i=0;i<=40;i++){ const t=TZ_CHAN.t1*i/40;
      if(!(tzLeft(t)[1]>=TZ_CHAN.x0&&tzRight(t)[0]<=TZ_CHAN.x1)) connected=false;
      phetGap=Math.max(phetGap,tzRight(t)[0]-TZ_CHAN_PHET_X1); }
    ok(connected,'the floor channel meets both chambers at 41 heights of the band');
    close(phetGap,0.07,1e-9,"PhET's own channel leaves a 7 cm gap at the floor (derive)");
    ok(!tzInside(6.03,-2.99)===false,'a point in that sliver IS inside this pool');
    ok(tzInside(6.03,-2.99),'...explicitly');
  }

  /* ---------------- 5. Pascal, in the chamber pool --------------------- */
  eq(CH_A_L,1,'the small piston is exactly 1 m2 with the 2 m out-of-page depth');
  close(CH_A_R,4.5999999999999996,1e-12,'the large one is 4.6 m2 (derive)');
  close(CH_RATIO,4.5999999999999996,1e-12,'the area ratio is 4.6 (derive)');
  close(CH_REST,-0.7,1e-12,'both surfaces rest at y = -0.70 m (derive)');
  eq(CH_MASS_MAX,1000,"PhET's three masses come to 1000 kg");
  {
    const P=[[250,2450,0.25031246487962866,0.25,0.20561381043683782],
             [500,4900,0.50062492975925732,0.5,0.41122762087367565],
             [750,7350.0000000000009,0.75093739463888609,0.75000000000000011,0],
             [1000,9800,1.0012498595185146,1,0]];
    for(const [m,dp,dhOn,dhOff,dL] of P){
      const a=pascal(m,RHO_WATER,G_EARTH,true), b=pascal(m,RHO_WATER,G_EARTH,false);
      close(a.dp,dp,1e-8,'dp = F/A at M = '+m+' kg (derive)');
      close(a.dh,dhOn,1e-12,'dh with the atmosphere at M = '+m+' (derive)');
      close(b.dh,dhOff,1e-12,'dh without it at M = '+m+' (derive)');
      if(dL) close(a.dL,dL,1e-12,'the small side falls at M = '+m+' (derive)');
      /* the classical law is EXACT with the atmosphere off */
      rel(b.dh,m/(RHO_WATER*CH_A_L),1e-15,'atmosphere off: dh = M/(rho A1) exactly at M = '+m);
      /* volume conservation, off the returned displacements */
      rel(a.dL*CH_A_L,a.dR*CH_A_R,1e-12,'A1 dL = A2 dR at M = '+m);
      rel(a.Fout,a.Fin*CH_RATIO,1e-12,'F2 = (A2/A1) F1 at M = '+m);
      rel(a.Fin*a.dL,a.Fout*a.dR,1e-12,'the work is the same on both pistons at M = '+m);
    }
  }
  close(rhoEff(RHO_WATER,true),998.75170068027217,1e-10,'the effective density with the atmosphere (derive)');
  eq(rhoEff(RHO_WATER,false),RHO_WATER,'...and the fluid density without it');
  close(-LAPSE/G_EARTH,1.2482993197278909,1e-12,"the air density PhET's lapse implies (derive)");
  /* dh does not depend on g, either way */
  for(const g of [G_MARS,G_EARTH,G_JUPITER]){
    close(pascal(500,RHO_WATER,g,true).dh,0.50062492975925732,1e-12,'dh is independent of g, atmosphere on (g = '+g+', derive)');
    close(pascal(500,RHO_WATER,g,false).dh,0.5,1e-14,'dh is independent of g, atmosphere off (g = '+g+')');
    close(pascal(500,RHO_WATER,g,true).dp,500*g/CH_A_L,1e-9,'but dp does carry g (g = '+g+')');
  }
  close(pascal(500,RHO_WATER,G_EARTH,true).Fout,22540,1e-9,'500 kg gives 22540 N on the large piston (derive)');
  close(500*CH_RATIO,2300,1e-9,'500 kg on the small piston holds 2300 kg on the large one (derive)');
  /* where the small column bottoms out */
  for(const [rho,mmax] of [[700,852.17391304347825],[1000,1217.3913043478262],[1420,1728.695652173913]])
    close(pascal(1,rho,G_EARTH,false).Mmax,mmax,1e-9,'the shaft bottoms out at M = '+fmt(mmax,1)+' kg for rho = '+rho+' (derive)');
  ok(pascal(1000,RHO_GASOLINE,G_EARTH,false).capped,'1000 kg on gasoline does bottom the shaft out');
  ok(!pascal(1000,RHO_WATER,G_EARTH,false).capped,'1000 kg on water does not');
  eq(pascal(1000,RHO_GASOLINE,G_EARTH,false).dL,CH_WATER,'and the capped displacement is exactly the shaft depth');
  /* THE pin: the same point, reached down from each surface, must agree */
  {
    const CG=[[true,0,1000,118973.56333333334],[true,0,1420,126382.36333333334],
              [true,500,1000,119848.56333333334],[true,500,1420,127257.36333333334],
              [true,1000,1000,120723.56333333334],[false,0,1000,17640],
              [false,500,1000,18515],[false,500,1420,25923.800000000003],
              [false,1000,1000,19390],[false,0,1420,25048.800000000003]];
    let worst=0;
    for(const [atm,m,rho,pref] of CG){
      const P=pascal(m,rho,G_EARTH,atm), y=-2.5;
      const viaL=airP(P.yL,G_EARTH,atm)+P.dp+rho*G_EARTH*(P.yL-y);
      const viaR=airP(P.yR,G_EARTH,atm)+rho*G_EARTH*(P.yR-y);
      close(viaR,pref,1e-8,'p(y = -2.5) at M = '+m+', rho = '+rho+', atm '+atm+' (derive)');
      worst=Math.max(worst,Math.abs(viaL-viaR));
    }
    ok(worst<1e-9,'the two routes to that point agree to '+worst.toExponential(2)+' Pa over 10 settings');
  }
  /* chamberPressure() itself, off the model rather than a retyped formula */
  {
    const P=pascal(500,RHO_WATER,G_EARTH,true);
    const a=chamberPressure(3.0,-1.3,P,RHO_WATER,G_EARTH,true);   /* in the small shaft */
    const b=chamberPressure(6.5,-1.3,P,RHO_WATER,G_EARTH,true);   /* in the large shaft */
    const c=chamberPressure(2.0,-2.5,P,RHO_WATER,G_EARTH,true);   /* in the body */
    ok(a.wet&&b.wet&&c.wet,'all three chamber probes are in the fluid');
    eq(a.side,'left','the small-shaft probe knows which side it is on');
    eq(b.side,'right','and so does the large-shaft one');
    /* the SAME height in one connected fluid is the SAME pressure, however
       heavily one side is loaded -- that is what equilibrium means, and it is
       the reason the two surfaces sit at different heights at all */
    close(a.p,b.p,1e-9,'two probes at the same height read the same pressure, loaded or not');
    /* and the piston term is exactly what the surface offset pays for */
    close(P.dp,(airP(P.yR,G_EARTH,true)-airP(P.yL,G_EARTH,true))+RHO_WATER*G_EARTH*(P.yR-P.yL),1e-9,
          'the piston pressure is exactly (rho g + lambda) times the surface separation');
    ok(P.yR>P.yL,'and the loaded side is the LOWER surface');
    const above=chamberPressure(3.0,-0.2,P,RHO_WATER,G_EARTH,true);
    ok(!above.wet&&above.side==='air','above the depressed surface the shaft probe reads air');
    const out=chamberPressure(5.0,-1.0,P,RHO_WATER,G_EARTH,true);
    ok(!out.wet,'between the two shafts, above the chambers, there is no fluid');
  }

  /* ---------------- 6. the hydrostatic paradox ------------------------- */
  {
    const REF=[['straight',4.7999999999999998,47040,1,0],
               ['flared',8.4000000000000004,82320,0.5714285714285714,35280],
               ['tapered',3.0999999999999996,30379.999999999996,1.5483870967741937,-16660],
               ['stepped',7.1240000000000006,69815.200000000012,0.67377877596855684,22775.199999999946]];
    let worstResid=0, worstBrute=0;
    for(let i=0;i<VESSELS.length;i++){
      const s=vesselStats(VESSELS[i],RHO_WATER,G_EARTH,PAR_H), R=REF[i];
      eq(s.name,R[0],'vessel '+i+' is the '+R[0]);
      close(s.V,R[1],1e-12,R[0]+': volume (derive)');
      close(s.W,R[2],1e-9,R[0]+': weight (derive)');
      close(s.ratio,R[3],1e-12,R[0]+': F_base/W (derive)');
      close(s.Fwall,R[4],1e-8,R[0]+': the wall integral (derive)');
      close(s.Fbase,47040,1e-9,R[0]+': the base force is the SAME 47040 N (derive)');
      worstResid=Math.max(worstResid,s.resid);
      /* the same wall integral by a 20000-strip sum, computed independently */
      const bf=profWallVerticalSum(VESSELS[i].prof,PAR_H,RHO_WATER,G_EARTH,20000);
      worstBrute=Math.max(worstBrute,Math.abs(bf-s.Fwall)/Math.max(1,Math.abs(s.Fwall)));
    }
    ok(worstResid<1e-6,'F_wall,z = W - F_base for all four, worst '+worstResid.toExponential(2)+' N');
    ok(worstBrute<1e-9,'the closed-form wall integral matches a 20000-strip sum, worst rel '+worstBrute.toExponential(2));
    close(vesselStats(VESSELS[1],RHO_WATER,G_EARTH,PAR_H).V/vesselStats(VESSELS[2],RHO_WATER,G_EARTH,PAR_H).V,
          2.709677419354839,1e-12,'the heaviest holds 2.7097 times the lightest (derive)');
    /* the ratio is geometry alone: no fluid, no gravity in it */
    for(const [rho,g] of [[700,3.71],[1420,24.9],[1000,9.8]])
      for(let i=0;i<VESSELS.length;i++)
        rel(vesselStats(VESSELS[i],rho,g,PAR_H).ratio,REF[i][3],1e-12,
            'F/W for the '+REF[i][0]+' is independent of rho and g ('+rho+', '+g+', derive)');
    /* a straight vessel is the one case where the base DOES carry the weight */
    eq(vesselStats(VESSELS[0],RHO_WATER,G_EARTH,PAR_H).Fwall,0,'a straight wall has no vertical pressure on it at all');
    ok(vesselStats(VESSELS[1],RHO_WATER,G_EARTH,PAR_H).Fwall>0,'a flared vessel: the walls hold fluid up');
    ok(vesselStats(VESSELS[2],RHO_WATER,G_EARTH,PAR_H).Fwall<0,'a tapered one: the walls push down');
    /* and the volume against an independent 100000-strip sum */
    for(const v of VESSELS){
      const N=100000; let V=0;
      for(let i=0;i<N;i++) V+=profW(v.prof,(i+0.5)*PAR_H/N)*(PAR_H/N)*DEPTH_OUT;
      rel(V,profVolume(v.prof,PAR_H),2e-5,v.name+': volume against a 100000-strip sum');
    }
  }

  /* ---------------- 7. shape independence, across the scenes ----------- */
  {
    const ySurf=-POOL_H+1.5;
    for(const d of [0,0.5,1.0,1.5]){
      const p=pressureAt(d,RHO_WATER,G_EARTH,ySurf,true);
      close(p,[101343.35000000001,106243.35000000001,111143.35000000001,116043.35000000001][[0,0.5,1.0,1.5].indexOf(d)],
            1e-8,'the reading at depth '+d+' below a surface at y = -1.5 (derive)');
    }
    close(1000*SQ_A*1.5,11100,1e-9,'the square pool holds 11100 L at that level (derive)');
    close(1000*tzVolume(1.5),12093.9,1e-6,'the trapezoid holds 12093.9 L at the same level (derive)');
    close(tzVolume(1.5)/(SQ_A*1.5),1.0895405405405403,1e-12,'8.95 % more fluid, same reading (derive)');
  }

  /* ---------------- 8. the mystery scene ------------------------------- */
  {
    const d=1.5, ySurf=-1.5;
    const fr=[126315,113673,117495];
    for(let i=0;i<3;i++){
      close(pressureAt(d,MYSTERY_RHO[i],G_EARTH,ySurf,true)-airP(ySurf,G_EARTH,true)+airP(0,G_EARTH,true),
            fr[i],1e-6,'Fluid '+'ABC'[i]+' reads '+fr[i]+' Pa at 1.5 m below a surface at y = 0 (derive)');
      /* the inversion recovers PhET's value exactly */
      const p=pressureAt(d,MYSTERY_RHO[i],G_EARTH,0,true);
      rel(rhoFromReading(p,G_EARTH,d,0,true),MYSTERY_RHO[i],1e-12,'inverting for Fluid '+'ABC'[i]);
    }
    let sep=Infinity;
    for(let i=0;i<3;i++) for(let j=i+1;j<3;j++)
      sep=Math.min(sep,Math.abs(pressureAt(d,MYSTERY_RHO[i],G_EARTH,0,true)-pressureAt(d,MYSTERY_RHO[j],G_EARTH,0,true)));
    close(sep,3822,1e-9,'the closest pair of fluids is 3822 Pa apart at 1.5 m (derive)');
    const pl=[236785.71428571429,165749.99999999997,76955.357142857145];
    for(let i=0;i<3;i++){
      close(pressureAt(d,RHO_WATER,MYSTERY_G[i],0,true),pl[i],1e-7,'Planet '+'ABC'[i]+' reads (derive)');
      rel(gFromReading(pl[i],RHO_WATER,d,0,true),MYSTERY_G[i],1e-13,'inverting for Planet '+'ABC'[i]);
    }
    let sep2=Infinity;
    for(let i=0;i<3;i++) for(let j=i+1;j<3;j++) sep2=Math.min(sep2,Math.abs(pl[i]-pl[j]));
    close(sep2,71035.714285714319,1e-7,'the closest pair of planets is 71036 Pa apart (derive)');
    /* the worst case over every depth a gauge can reach */
    let wf=Infinity, wp=Infinity;
    for(let k=1;k<=60;k++){ const dd=k*0.05;
      for(let i=0;i<3;i++) for(let j=i+1;j<3;j++){
        wf=Math.min(wf,Math.abs(pressureAt(dd,MYSTERY_RHO[i],G_EARTH,0,true)-pressureAt(dd,MYSTERY_RHO[j],G_EARTH,0,true)));
        wp=Math.min(wp,Math.abs(pressureAt(dd,RHO_WATER,MYSTERY_G[i],0,true)-pressureAt(dd,RHO_WATER,MYSTERY_G[j],0,true)));
      } }
    close(wf,127.39999999999418,1e-8,'the fluids never come closer than 127.4 Pa over 0.05-3.00 m (derive)');
    close(wp,62335.714285714319,1e-7,'nor the planets closer than 62336 Pa (derive)');
    /* at EXACTLY zero depth the fluids are degenerate and the planets are not */
    for(let i=0;i<3;i++) for(let j=i+1;j<3;j++)
      eq(pressureAt(0,MYSTERY_RHO[i],G_EARTH,0,true)-pressureAt(0,MYSTERY_RHO[j],G_EARTH,0,true),0,
         'at the surface Fluid '+'ABC'[i]+' and '+'ABC'[j]+' read identically');
    let s0=Infinity;
    for(let i=0;i<3;i++) for(let j=i+1;j<3;j++) s0=Math.min(s0,Math.abs(airP(0,MYSTERY_G[i],true)-airP(0,MYSTERY_G[j],true)));
    close(s0,62035.714285714319,1e-7,'the planets differ by 62036 Pa even at the surface (derive)');
    /* and the model SAYS so */
    withState({view:'mystery',myMode:'fluid',myDepth:0,volFrac:0.5},()=>{
      const M=buildModel(ST);
      ok(M.degenerate,'the model reports a surface fluid reading as degenerate');
      ok(!isFinite(M.inv),'and refuses to name a density');
    });
    withState({view:'mystery',myMode:'planet',myDepth:0,volFrac:0.5},()=>{
      const M=buildModel(ST);
      ok(!M.degenerate&&isFinite(M.inv),'a surface reading still names a planet');
      rel(M.inv,MYSTERY_G[ST.myWhich],1e-12,'and names the right one');
    });
  }

  /* ---------------- 9. the column -------------------------------------- */
  close(RHO_GASOLINE*G_EARTH,6860.0000000000009,1e-9,'gasoline: slope rho g (derive)');
  close(RHO_WATER*G_EARTH,9800,1e-9,'water: slope rho g (derive)');
  close(RHO_HONEY*G_EARTH,13916.000000000002,1e-9,'honey: slope rho g (derive)');
  close(PA_PER_ATM/(RHO_WATER*G_EARTH),10.339285714285714,1e-12,"one atmosphere of water at PhET's 9.8 (derive)");
  close(PA_PER_ATM/(RHO_WATER*G_STD),10.332274527998859,1e-12,'...and at standard gravity (derive)');
  {
    /* the depth at which the reading is exactly 2 atm, against derive's brentq */
    const dd=(2*PA_PER_ATM-airP(0,G_EARTH,true))/(RHO_WATER*G_EARTH);
    close(dd,10.339285714285714,1e-12,'the depth of a 2 atm reading (derive, brentq)');
    rel(pressureAt(dd,RHO_WATER,G_EARTH,0,true),2*PA_PER_ATM,1e-14,'and it does read 2 atm there');
  }
  for(const [d,k,a,ps] of [[0,101.325,1,14.69594877551345],
                           [0.75,108.675,1.072538860103627,15.761976147830488],
                           [1.5,116.02500000000001,1.145077720207254,16.828003520147526],
                           [2.25,123.375,1.2176165803108809,17.894030892464563],
                           [3,130.72499999999999,1.2901554404145077,18.960058264781601]]){
    const p=pressureAt(d,RHO_WATER,G_EARTH,0,true);
    close(toUnit(p,'metric'),k,1e-9,'water on Earth at '+d+' m, in kPa (derive)');
    close(toUnit(p,'atmosphere'),a,1e-12,'...in atm (derive)');
    close(toUnit(p,'english'),ps,1e-10,'...in psi (derive)');
  }
  close(RHO_WATER*G_EARTH*10/PA_PER_ATM,0.9671848013816926,1e-12,'ten metres of water is 0.967 atm (derive)');

  /* ---------------- 10. the models, built, not retyped ----------------- */
  withState({view:'pool',rho:RHO_WATER,grav:G_EARTH,atmosphere:true,volFrac:0.5},()=>{
    const M=buildModel(ST);
    close(M.level,1.5,1e-12,'the pool model: half full is 1.5 m');
    close(M.ySurf,-1.5,1e-12,'...with the surface at y = -1.5');
    close(M.V,11.1,1e-12,'...holding 11.1 m3');
    close(M.pBot,116043.35000000001,1e-8,'...and 116043.35 Pa at the floor (derive)');
    close(M.pSurf,airP(-1.5,G_EARTH,true),1e-12,'...the surface reading is exactly the air there');
    close(M.mass,11100,1e-9,'...11100 kg of water');
    close(M.weight,11100*G_EARTH,1e-9,'...weighing rho g V');
    ok(M.Fbot>M.weight,'the floor carries more than the fluid, because the air stands on it too');
  });
  withState({view:'pool',atmosphere:false,volFrac:1},()=>{
    const M=buildModel(ST);
    rel(M.Fbot,M.weight,1e-12,'with the atmosphere off the floor carries exactly the weight of the fluid');
  });
  withState({view:'pool',gAx:3.0,gAy:-2.0,gBx:5.5,gBy:-2.0,volFrac:0.5},()=>{
    const M=buildModel(ST);
    ok(M.A.wet&&M.B.wet,'both gauges are in the fluid');
    eq(M.A.p-M.B.p,0,'two gauges at the same depth read EXACTLY the same');
    ok(M.sameDepth,'and the model says so');
  });
  /* THE number the sim exists to print: the gauge's own reading, at the
     sim's own default positions, against an absolute value.  Without this the
     probe could measure the depth upside down and every "the two agree"
     assertion would still pass, because both would be wrong together. */
  withState({view:'pool',volFrac:0.5},()=>{
    const M=buildModel(ST);
    eq(ST.gAy,-2.4,'the default gauges sit at y = -2.40');
    close(M.A.depth,0.9,1e-12,'which is 0.90 m below a surface at y = -1.50');
    close(M.A.p,110163.35000000001,1e-8,'and reads 110163.35 Pa (derive)');
    close(M.B.p,110163.35000000001,1e-8,'...and so does gauge B (derive)');
    close(toUnit(M.A.p,'metric'),110.16335000000001,1e-10,'= 110.16335 kPa (derive)');
    close(toUnit(M.A.p,'atmosphere'),1.0872277325437947,1e-12,'= 1.0872277325 atm (derive)');
    close(toUnit(M.A.p,'english'),15.977843064781245,1e-10,'= 15.977843065 psi (derive)');
    ok(M.A.p>M.pSurf,'a gauge below the surface reads MORE than the surface does');
  });
  withState({view:'pool',volFrac:0.5,gAy:-1.5},()=>{
    const M=buildModel(ST);
    eq(M.A.depth,0,'a gauge exactly at the surface is at zero depth');
    close(M.A.p,101343.35000000001,1e-8,'and reads the air there, 101343.35 Pa (derive)');
  });
  withState({view:'pool',volFrac:0.5,rho:RHO_HONEY,grav:G_JUPITER},()=>{
    close(buildModel(ST).A.p,289317.0382653061,1e-7,'the same gauge in honey on Jupiter (derive)');
  });
  withState({view:'pool',volFrac:0.5,atmosphere:false},()=>{
    close(buildModel(ST).A.p,8820,1e-9,'and with the atmosphere off, exactly rho g h = 8820 Pa (derive)');
  });
  /* PhET's six named values, pinned absolutely AND through the lists the UI
     reaches them by -- G_MARS survived a sweep because every assertion that
     touched it either passed the literal 3.71 or was invariant to it */
  eq(G_MARS,3.71,"PhET's Mars gravity");
  eq(G_EARTH,9.8,"PhET's Earth gravity");
  eq(G_JUPITER,24.9,"PhET's Jupiter gravity");
  eq(RHO_GASOLINE,700,"PhET's gasoline density");
  eq(RHO_WATER,1000,"PhET's water density");
  eq(RHO_HONEY,1420,"PhET's honey density");
  eq(G_TICKS.map(t=>t.g).join(','),'3.71,9.8,24.9','the gravity ticks are those three, in order');
  eq(FLUID_TICKS.map(f=>f.rho).join(','),'700,1000,1420','and the fluid ticks are those three');
  eq(G_RANGE[0],G_MARS,'the gravity slider starts at Mars');
  eq(G_RANGE[1],G_JUPITER,'...and ends at Jupiter');
  eq(RHO_RANGE[0],RHO_GASOLINE,'the density slider starts at gasoline');
  eq(RHO_RANGE[1],RHO_HONEY,'...and ends at honey');
  close(pressureAt(3,RHO_WATER,G_RANGE[0],0,true),49488.75,1e-8,
        'water at 3 m at the BOTTOM of the gravity slider (derive)');
  close(pressureAt(3,RHO_RANGE[0],G_EARTH,0,true),121905,1e-8,
        'the bottom of the density slider at 3 m (derive)');
  close(pressureAt(3,RHO_RANGE[1],G_RANGE[1],0,true),363522.2142857142,1e-6,
        'and both sliders at the top (derive)');
  /* what a gauge reads WHERE IT IS: air above the ground, nothing inside the
     solid ground, air in the empty part of the pool, fluid below the surface.
     PhET's getPressureAtCoords returns the air for any y > 0, and the first
     version of this file returned "no reading" there instead. */
  withState({view:'pool',gAx:1.8,gAy:-2.0,volFrac:0.5},()=>{
    const M=buildModel(ST);
    ok(M.A.out,'a gauge buried in the ground beside the pool has no reading');
    eq(M.A.p,0,'and reports zero rather than a pressure');
  });
  withState({view:'pool',gAx:1.8,gAy:0.35,volFrac:0.5},()=>{
    const M=buildModel(ST);
    ok(!M.A.out&&!M.A.wet&&M.A.air,'a gauge in the air BESIDE the pool reads the air');
    close(M.A.p,airP(0.35,G_EARTH,true),1e-12,'...at the air pressure of its own height');
    ok(M.A.p<airP(0,G_EARTH,true),'which is below the ground-level value, because the air thins');
  });
  withState({view:'pool',gAx:4,gAy:0.5,volFrac:0.5,atmosphere:false},()=>{
    const M=buildModel(ST);
    eq(M.A.p,0,'with the atmosphere off the air reads exactly zero');
  });
  withState({view:'press',gAx:4.8,gAy:-1.0,m500:true},()=>{
    const M=buildModel(ST);
    ok(M.A.out&&M.A.side==='ground','a chamber gauge in the wall between the shafts has no reading');
  });
  withState({view:'press',gAx:4.8,gAy:0.4,m500:true},()=>{
    const M=buildModel(ST);
    ok(!M.A.out&&M.A.side==='air','but above the ground it reads the air');
    close(M.A.p,airP(0.4,G_EARTH,true),1e-12,'...at its own height');
  });
  withState({view:'pool',gAx:4.0,gAy:-0.5,volFrac:0.5},()=>{
    const M=buildModel(ST);
    ok(!M.A.wet&&!M.A.out,'a gauge above the surface but inside the pool reads the air');
    close(M.A.p,airP(-0.5,G_EARTH,true),1e-12,'...and reads exactly the air pressure there');
  });
  withState({view:'shapes',volFrac:tzVolume(1.5)/TZ_VMAX,gAx:2.4,gAy:-2.2,gBx:6.6,gBy:-2.2},()=>{
    const M=buildModel(ST);
    close(M.level,1.5,1e-12,'the trapezoid pool is 1.5 m deep at this volume');
    close(1000*M.V,12093.9,1e-6,'holding 12093.9 L (derive)');
    ok(M.A.wet&&M.B.wet,'both trapezoid gauges are in the fluid');
    eq(M.dP,0,'one in each chamber at the same depth: the readings are identical');
    /* the two columns above the gauges, pinned to derive.py (each of which was
       checked there against scipy.integrate.quad to 1e-12) */
    close(M.colA,3.0951666666666684,1e-12,'the left column above the gauge is 3.0952 m3 (derive)');
    close(M.colB,2.2948333333333344,1e-12,'the right column is 2.2948 m3 (derive)');
    close(M.colA/M.colB,1.3487544483985767,1e-12,'a ratio of 1.3488 at this level (derive)');
    close(M.wSum,TZ_WSUM,1e-12,'the widths still sum to the constant');
  });
  /* deeper gauges in a shallower pool: the same reading, 2.83x the fluid */
  withState({view:'shapes',volFrac:tzVolume(0.5)/TZ_VMAX,gAx:2.4,gAy:-2.75,gBx:6.6,gBy:-2.75},()=>{
    const M=buildModel(ST);
    close(M.level,0.5,1e-12,'the pool is 0.5 m deep');
    ok(M.A.wet&&M.B.wet,'both gauges are still under');
    eq(M.dP,0,'and still read identically');
    close(M.colA,1.421875,1e-12,'with 1.4219 m3 over one (derive)');
    close(M.colB,0.50312499999999982,1e-12,'and 0.5031 m3 over the other (derive)');
    close(M.colA/M.colB,2.8260869565217401,1e-12,'2.826 times as much fluid, the same number on the gauge (derive)');
  });
  withState({view:'press',m500:true,m250a:false,m250b:false},()=>{
    const M=buildModel(ST);
    eq(M.M,500,'the platform carries the 500 kg mass');
    close(M.P.dp,4900,1e-9,'which adds 4900 Pa (derive)');
    close(M.liftable,2300,1e-9,'and would hold 2300 kg');
    ok(M.routeResid<1e-9,'the two routes to y = -2.5 agree in the built model');
  });
  withState({view:'press',m500:true,m250a:true,m250b:true},()=>{
    const M=buildModel(ST);
    eq(M.M,1000,'all three masses come to 1000 kg');
    close(M.P.dp,9800,1e-9,'adding 9800 Pa');
  });
  withState({view:'paradox',parDepth:PAR_H,rho:RHO_WATER,grav:G_EARTH},()=>{
    const M=buildModel(ST);
    eq(M.rows.length,4,'four vessels');
    let same=true;
    for(const r of M.rows) if(Math.abs(r.Fbase-M.rows[0].Fbase)>1e-9) same=false;
    ok(same,'and one base force between them');
    close(M.spread,2.709677419354839,1e-12,'with a 2.71 spread in weight (derive)');
    ok(M.worstResid<1e-9,'the wall integral matches its brute-force twin inside the model');
  });
  withState({view:'column',rho:RHO_WATER,grav:G_EARTH,colDepth:1.5},()=>{
    const M=buildModel(ST);
    close(M.here.p,116025,1e-9,'the column marker reads 116025 Pa at 1.5 m (derive)');
    close(M.psiPerAtm,14.69594877551345,1e-12,'and carries the exact psi per atm');
    eq(M.lines.length,3,"PhET's three named fluids are drawn");
  });

  /* ------------- 10b. the memo key is COMPLETE ------------------------- *
   * Every view caches its model under a key built from the state it reads.
   * If that key is complete then clearAll() is redundant everywhere, and the
   * mutants that delete it are equivalent BY CONSTRUCTION rather than by
   * accident -- which is a property worth stating rather than discovering
   * (Known-bad: a survivor that is an equivalent mutant is telling you the
   * code carries meaning its tests do not).  Both halves are asserted: the
   * memo really does cache, and every input that a view reads changes its
   * key. */
  {
    /* the memo is live: two calls with no change return the SAME object */
    for(const [v] of TABS) withState({view:v},()=>{
      ok(buildModel(ST)===buildModel(ST),'the '+v+' model is memoised (same object twice)');
    });
    /* and every input a view reads moves its key, WITHOUT clearAll() */
    const INPUTS={
      pool:[['rho',RHO_HONEY],['grav',G_MARS],['atmosphere',false],['volFrac',0.8],
            ['gAx',3.6],['gAy',-1.0],['gBx',4.4],['gBy',-2.9],['units','english']],
      shapes:[['rho',RHO_GASOLINE],['grav',G_JUPITER],['atmosphere',false],['volFrac',0.3],
              ['gAx',2.6],['gAy',-1.2],['gBx',6.9],['gBy',-2.8],['units','atmosphere']],
      press:[['rho',RHO_HONEY],['grav',G_MARS],['atmosphere',false],['m500',false],
             ['m250a',true],['m250b',true],['gAx',2.9],['gAy',-2.9],['gBx',6.9],['gBy',-2.9],['units','english']],
      mystery:[['myMode','planet'],['myWhich',2],['myGuess','2'],['myReveal',true],['myDepth',0.4],
               ['rho',RHO_HONEY],['grav',G_MARS],['atmosphere',false],['volFrac',0.9],['units','atmosphere']],
      paradox:[['rho',RHO_HONEY],['grav',G_MARS],['parDepth',0.6],['parPick','tapered'],
               ['units','english'],['atmosphere',false]],
      column:[['rho',RHO_GASOLINE],['grav',G_JUPITER],['atmosphere',false],['colDepth',2.2],
              ['colAll',false],['units','atmosphere']],
    };
    let blind=[];
    for(const v in INPUTS) for(const [k,val] of INPUTS[v]){
      let before=null, after=null;
      withState({view:v},()=>{ before=buildModel(ST); });
      /* NO clearAll() between the two: the key alone has to notice */
      withState(Object.assign({view:v},{[k]:val}),()=>{ after=buildModel(ST); });
      if(before===after) blind.push(v+'.'+k);
    }
    eq(blind.length,0,'every input each view reads is in that view\'s memo key'
       +(blind.length?': blind to '+blind.join(', '):''));
    /* the count, so a silently shortened table cannot pass */
    eq(Object.keys(INPUTS).reduce((t,v)=>t+INPUTS[v].length,0),51,'51 (view, input) pairs were checked');
  }

  /* ---------------- 11. the drawing agrees with the model -------------- */
  {
    /* the fluid polygons' area x the out-of-page depth IS the model volume */
    withState({view:'pool',volFrac:0.5},()=>{
      const M=buildModel(ST);
      let A=0; for(const p of fluidPolys('square',M.ySurf,null)) A+=polyAreaW(p);
      rel(A*DEPTH_OUT,M.V,1e-12,'the drawn square pool holds exactly the model volume');
    });
    for(const vf of [0.03,0.5,1]) withState({view:'shapes',volFrac:vf},()=>{
      const M=buildModel(ST);
      let A=0; for(const p of fluidPolys('trapezoid',M.ySurf,null)) A+=polyAreaW(p);
      rel(A*DEPTH_OUT,M.V,1e-9,'the drawn trapezoid holds the model volume at '+(100*vf)+' % full');
    });
    /* the chamber conserves its fluid as the load moves it about */
    {
      const P0=pascal(0,RHO_WATER,G_EARTH,true), P1=pascal(1000,RHO_WATER,G_EARTH,true);
      const area=P=>{ let A=0; for(const p of fluidPolys('chamber',null,P)) A+=polyAreaW(p); return A; };
      rel(area(P1),area(P0),1e-12,'the drawn chamber holds the same fluid loaded and unloaded');
      ok(Math.abs(P1.yL-P0.yL)>0.5,'...although the small surface really has moved '+fmt(Math.abs(P1.yL-P0.yL),3)+' m');
    }
    /* the surface segments sit at the surface */
    withState({view:'shapes',volFrac:0.5},()=>{
      const M=buildModel(ST);
      const ss=surfaceSegs('trapezoid',M.ySurf,null);
      eq(ss.length,2,'the trapezoid draws two free surfaces above the channel');
      for(const s of ss) eq(s[2],M.ySurf,'and both are at the model surface height');
    });
    /* the paradox vessels' drawn fluid polygon is the model volume */
    withState({view:'paradox',parDepth:1.4},()=>{
      const M=buildModel(ST);
      VESSELS.forEach((v,i)=>{
        rel(polyAreaW(fluidPoly(v.prof,PAR_H,M.H))*DEPTH_OUT,M.rows[i].V,1e-9,
            'the drawn '+v.name+' holds the model volume');
      });
    });
  }

  /* ---------------- 12. panels build clean, every view x preset -------- */
  {
    const badRe=/NaN|undefined|Infinity/;
    const entRe=/&#?[a-zA-Z0-9]+;|<\/?[a-zA-Z][^>]*>/;
    const PRESETS=[{},{atmosphere:false},{units:'atmosphere'},{units:'english'},
                   {rho:RHO_GASOLINE},{rho:RHO_HONEY},{grav:G_MARS},{grav:G_JUPITER},
                   {volFrac:0},{volFrac:1},{gridOn:true,rulerOn:true},
                   {m500:false,m250a:false,m250b:false},{m500:true,m250a:true,m250b:true},
                   {myMode:'planet',myWhich:2,myReveal:true},{myDepth:0},
                   {parPick:'tapered',parDepth:0.2},{colAll:false},
                   {gAx:1.6,gAy:0.4},{rho:RHO_GASOLINE,m500:true,m250a:true,m250b:true}];
    let nbad=0;
    for(const [v] of TABS) for(const P of PRESETS) withState(Object.assign({view:v},P),()=>{
      const M=buildModel(ST);
      /* no exception list: the pulsar Known-bad says reword the prose rather
         than weaken this check, and two strings were reworded for it */
      for(const s of [readoutHTML(M,ST),eqbarHTML(M,ST),tagHTML(M,ST),INFO[v]||'',DERIV[v]||'']){
        if(badRe.test(plain(s))) { nbad++; console.log('   panel: '+plain(s).slice(0,110)); }
      }
    });
    eq(nbad,0,'no NaN, undefined or Infinity in any panel, over '+(TABS.length*PRESETS.length)+' view x preset combinations');
    /* the readout must actually SAY a number no other row can supply, so the
       containment check is not vacuous (sbs_parent_law Known-bad) */
    withState({view:'pool',units:'metric',volFrac:0.5,rho:RHO_WATER,grav:G_EARTH},()=>{
      const s=plain(readoutHTML(buildModel(ST),ST));
      ok(s.indexOf('116.0')>=0,'the pool readout prints the floor pressure 116.0 kPa');
      ok(s.indexOf('9.800')>=0,'and rho g as 9.800 kPa/m');
    });
    withState({view:'column',units:'english',colDepth:3,rho:RHO_WATER,grav:G_EARTH},()=>{
      const s=plain(readoutHTML(buildModel(ST),ST));
      ok(s.indexOf('18.9601')>=0||s.indexOf('18.96')>=0,'the column readout prints 18.96 psi at 3 m');
      ok(s.indexOf('14.69594878')>=0,'and the exact psi per atm');
    });
    /* the entity/tag audit on the HTML panels is meaningless (they ARE html),
       so it runs on the CANVAS only -- below. */
    ok(entRe.test('&rho;'),'the entity regex is live (it must match &rho;)');
  }

  /* ---------------- 13. the layout, every view x size ------------------ */
  {
    const badRe=/NaN|undefined|Infinity/;
    const entRe=/&#?[a-zA-Z0-9]+;|<\/?[a-zA-Z][^>]*>/;
    const SIZES=[[1180,740],[1400,860],[820,560],[560,380]];
    /* the floors are MEASURED, not guessed: build/under-pressure/_out/
       tail_undef.js prints the fills and texts every configuration emits at
       all four sizes, and these are the minimum over the four, less one.  An
       op-count floor copied from another sim punishes this one for batching
       (Known-bad), and a floor of 3 texts would let a blank view pass. */
    const SWEEP=[
      ['pool',{view:'pool'},10,7],
      ['pool empty',{view:'pool',volFrac:0},9,7],
      ['pool full grid ruler',{view:'pool',volFrac:1,gridOn:true,rulerOn:true},11,14],
      ['pool no atmosphere',{view:'pool',atmosphere:false,units:'english'},10,8],
      ['pool gauge outside',{view:'pool',gAx:1.7,gAy:0.4},10,7],
      ['shapes',{view:'shapes'},12,9],
      ['shapes in the channel',{view:'shapes',volFrac:0.04},10,9],
      ['shapes full, atm units',{view:'shapes',volFrac:1,units:'atmosphere'},12,9],
      ['press empty',{view:'press',m500:false},16,7],
      ['press loaded',{view:'press',m500:true,m250a:true,m250b:true},19,8],
      ['press capped',{view:'press',rho:RHO_GASOLINE,m500:true,m250a:true,m250b:true},19,9],
      ['mystery fluid',{view:'mystery'},8,7],
      ['mystery surface',{view:'mystery',myDepth:0},8,8],
      ['mystery planet revealed',{view:'mystery',myMode:'planet',myWhich:2,myReveal:true},8,7],
      ['paradox',{view:'paradox'},12,35],
      ['paradox shallow',{view:'paradox',parDepth:0.2,parPick:'tapered'},12,36],
      /* the column's unit-scale panel drops to ONE scale on a short stage, so
         its narrow counts are legitimately much lower than its wide ones */
      ['column',{view:'column'},2,28],
      ['column psi, no atmosphere',{view:'column',units:'english',atmosphere:false,colAll:false},4,31],
    ];
    for(const [nm,over,minFills,minTexts] of SWEEP) for(const [W,H] of SIZES) withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel(ST),ST); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(fills.length>=minFills&&texts.length>=minTexts,
         nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills / '+texts.length+' texts, floors '+minFills+'/'+minTexts+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(badRe.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'"'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' nothing under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'")':''));
      let hit=null;
      for(let i=0;i<texts.length&&!hit;i++) for(let j=i+1;j<texts.length;j++){
        const a=texts[i].bb,b=texts[j].bb;
        const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i].t.slice(0,22)+'" vs "'+texts[j].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
    });
  }

  /* the canvas carries no letter subscripts (there is no Unicode subscript f,
     and the rasteriser's font does not have all of the ones that exist) */
  {
    const c=makeShot(1180,740);
    let bads=[];
    for(const v of TABS.map(t=>t[0])) withState({view:v},()=>{ drawView(c,1180,740,buildModel(ST),ST); });
    for(const o of c.ops) if(o.op==='text'&&/[ₐ-ₜᵢ-ᵪ]/.test(o.t)) bads.push(o.t);
    eq(bads.length,0,'no letter subscripts reach the canvas (greenhouse-effect Known-bad)'+(bads.length?': '+bads[0]:''));
  }

  Object.assign(ST,stSave); clearAll();
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
