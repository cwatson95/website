
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/gravity-force-lab/refvals.txt, the printed output   *
 *  of derive.py (scipy.constants CODATA 2022, solve_ivp and brentq    *
 *  for the fall, the full 100 x 100 mass-pair enumeration), read in   *
 *  full.                                                              *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    Object.assign(ST,DEFAULTS,over); simReset();
    if(over.release){ startRun(ST); for(let k=0;k<(over.frames||0);k++) runStep(); }
    try{ return fn(); } finally{ Object.assign(ST,stSave); simReset(); }
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  eq(mix('rgb(10,20,30)','#ffffff',0),'rgb(10,20,30)','mix() accepts its own output');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  eq(logTicks(0,10).length,0,'logTicks refuses a non-positive bound');
  eq(symRound(2.5),3,'symRound(2.5) = 3'); eq(symRound(-2.5),-3,'symRound(-2.5) = -3, halves away from zero (Math.round gives -2)');
  eq(symRound(-2.4),-2,'symRound(-2.4) = -2'); eq(symRound(14.499999999999998),14,'a hair under a half rounds down');
  eq(supText(-11),'⁻¹¹','superscript digits');
  /* the default force sits on a rounding tie at 12 decimals: the model's own
     double G m1 m2 / r^2 is 1.6685749999999998e-7 and reads ...857, the retyped
     literal 1.668575e-7 is one ulp over the tie and reads ...858 — so the pin is
     taken off the model's double, as derive.py does */
  eq(decGrouped(forceMag(TRACK.C,100,400,4),12),'0.000 000 166 857','PhET decimal grouping of the model\'s force (derive)');
  eq(decGrouped(1.668575e-7,12),'0.000 000 166 858','the literal is on the other side of the tie');
  eq(sciText(1.668575e-7,2),'1.67 × 10⁻⁷','PhET scientific (derive: 1.67 x 10^-7)'); eq(sciText(3.2,2),'3.20','no power of ten at exponent 0');
  eq(forceValueText(0,'sci',12),'0.000 000 000 000','a zero force stays decimal in scientific mode (PhET)');
  eq(sciHTML(1.668575e-7,4),'1.669 &times; 10<sup>-7</sup>','the readout form');

  /* ---------- A. the constants, against absolute numbers ---------- */
  eq(G_N,6.6743e-11,'G = 6.6743e-11 m^3 kg^-1 s^-2 (scipy CODATA 2022)');
  eq(G_PHET,6.67408e-11,'PhET\'s G = 6.67408e-11 (CODATA 2014, read from its build)');
  rel(G_N/G_PHET-1,3.296334476044e-05,1e-9,'G / G_PhET - 1 (derive)');
  eq(RHO_S,150,'PhET density 150 kg/m^3'); eq(R_CONST,0.5,'PhET constant radius 0.5 m');
  eq(TRACK.q,0.1,'the 0.1-m grid'); eq(TRACK.perM,10,'10 counts per metre'); eq(TRACK.iL,-50,'track from -5 m'); eq(TRACK.iR,50,'to +5 m');
  eq(TRACK.sep,0.1,'0.1 m between surfaces'); eq(TRACK.C,-G_N,'masses attract: C = -G');
  eq(M_MIN,10,'masses from 10 kg'); eq(M_MAX,1000,'to 1000 kg'); eq(M_STEP,10,'in 10-kg steps'); eq(G0,9.80665,'standard gravity, exact');
  eq(FALL_FRAMES,600,'a run is 600 frames');

  /* ---------- B. the radii ---------- */
  for(const [m,r] of [[10,0.2515397995802],[100,0.5419260701393],[400,0.8602540138281],[1000,1.167544324941]])
    rel(sphereRadius(m,false),r,1e-12,'radius of '+m+' kg at 150 kg/m^3 (derive)');
  rel(scaledRadius(78.53981633974,150),0.5,1e-12,'78.54 kg is the mass whose scaled radius is 0.5 m (derive)');
  eq(sphereRadius(1000,true),0.5,'constant size: 0.5 m whatever the mass');
  rel(4/3*PI*Math.pow(sphereRadius(400,false),3)*RHO_S,400,1e-12,'the scaled sphere really has its mass at 150 kg/m^3');

  /* ---------- C. the no-overlap rule ---------- */
  for(const [m1,m2,cs,n] of [[100,400,false,15],[1000,1000,false,24],[10,10,false,6],[100,400,true,11],[1000,400,false,21],
                            [100,1000,false,18],[1000,1000,true,11],[200,200,false,15],[500,500,false,20],[140,940,false,18]])
    eq(pairSteps(m1,m2,cs),n,'closest centres for '+m1+'/'+m2+(cs?' (constant size)':'')+' in 0.1-m steps (derive)');
  { /* every pair the sliders can reach, both modes: the snapped rule never lets them touch */
    for(const cs of [false,true]){
      let gmin=9, at=null, nmax=0;
      for(let m1=M_MIN;m1<=M_MAX;m1+=M_STEP) for(let m2=M_MIN;m2<=M_MAX;m2+=M_STEP){
        const n=pairSteps(m1,m2,cs), g=n/TRACK.perM-sphereRadius(m1,cs)-sphereRadius(m2,cs);
        if(g<gmin){ gmin=g; at=[m1,m2]; } nmax=Math.max(nmax,n); }
      if(!cs){ rel(gmin,0.05004309588792,1e-9,'smallest gap over all 10000 scaled pairs (derive)'); ok(at[0]===140&&at[1]===940,'at 140 and 940 kg (derive)'); eq(nmax,24,'max closest distance 2.4 m (derive)'); }
      else { rel(gmin,0.1,1e-12,'constant size: the gap is always 0.1 m'); eq(nmax,11,'and the centres 1.1 m (derive)'); }
      ok(gmin>0,(cs?'constant':'scaled')+' size: the spheres never touch'); } }

  /* ---------- D. the push rule, through the actions ---------- */
  const SC=[['a default, m1 -> 1000',{i1:-30,i2:10},()=>setMass(ST,1,1000),[-30,10]],
            ['b m2 -> 1000 at 1.5 m',{i1:-30,i2:-15},()=>setMass(ST,2,1000),[-33,-15]],
            ['c m1 on the left wall, m2 -> 1000',{i1:-50,i2:-35},()=>setMass(ST,2,1000),[-50,-32]],
            ['d m2 on the right wall, m1 -> 1000',{i1:35,i2:50},()=>setMass(ST,1,1000),[29,50]],
            ['e constant size off, 1000/1000 at 1.1 m',{i1:-6,i2:5,m1:1000,m2:1000,cs:true},()=>setConstSize(ST,false),[-19,5]]];
  for(const [nm,over,act,want] of SC) withState(over,()=>{ act(); ok(ST.i1===want[0]&&ST.i2===want[1],'push rule '+nm+' -> '+ST.i1+', '+ST.i2+' (derive '+want+')'); });
  eq(settlePair(0,5,10,-50,50,1)[1],10,'settlePair pushes body 2 when body 1 grew'); eq(settlePair(0,5,10,-50,50,2)[0],-5,'and body 1 when body 2 grew');
  eq(settlePair(40,50,15,-50,50,1)[0],35,'body 2 against the right end: body 1 moves instead');
  eq(settlePair(-50,-40,15,-50,50,2)[1],-35,'body 1 against the left end: body 2 moves instead');
  withState({},()=>{ setMass(ST,1,1234); eq(ST.m1,1000,'a mass is clamped to 1000 kg'); setMass(ST,2,3); eq(ST.m2,10,'and to 10 kg');
    setMass(ST,2,456); eq(ST.m2,460,'and ROUNDED to 10 kg (456 -> 460: floor would give 450)'); });

  /* ---------- E. dragging ---------- */
  withState({},()=>{
    setPos(ST,1,3); eq(ST.i1,-5,'dragging m1 at x = 3 stops it 1.5 m short of m2 (x = -0.5)');
    setPos(ST,2,-2); eq(ST.i2,10,'m2 cannot be dragged through m1 either (stays at 1.0: the closest is 1.0 now)');
    setPos(ST,2,7); eq(ST.i2,50,'past the right end: held at +5 m');
    setPos(ST,1,-9); eq(ST.i1,-50,'past the left end: held at -5 m');
    setPos(ST,1,-3.04); eq(ST.i1,-30,'-3.04 snaps to -3.0'); setPos(ST,1,-3.06); eq(ST.i1,-31,'-3.06 snaps to -3.1');
    eq(dragSteps(TRACK,1,0.26,-30,10,15),-5,'dragSteps clamps body 1 at i2 - n'); eq(dragSteps(TRACK,2,-2.6,-30,10,15),-15,'and body 2 at i1 + n');
    eq(dragSteps(TRACK,2,-0.26,-30,10,15),-3,'inside the allowed range a drag is only snapped'); });

  /* ---------- F. the force ---------- */
  withState({},()=>{
    const L=labModel(ST);
    rel(L.Fmag,1.668575e-07,1e-12,'F at the defaults: 100 kg, 400 kg, 4 m (derive)');
    rel(L.F1,1.668575e-07,1e-12,'the force on m1 points +x, toward m2'); rel(L.F2,-1.668575e-07,1e-12,'the force on m2 points -x, toward m1');
    close(L.F1+L.F2,0,1e-22,'Newton\'s third law, from two independent evaluations');
    rel(L.Fr2,2.66972e-06,1e-12,'F r^2 = G m1 m2 (derive)'); rel(L.Fphet,1.66852e-07,1e-12,'PhET\'s G gives 1.66852e-7 (derive)');
    rel(L.wtKg*1e9,17.0147298007,1e-10,'the weight of 17.01 micrograms (derive)');
    eq(L.r,4,'r = 4.0 m'); rel(L.gap,4-0.5419260701393-0.8602540138281,1e-12,'the gap between surfaces'); rel(L.dmin,1.5,1e-15,'closest allowed 1.5 m');
    eq(L.lab1,'Force on m₁ by m₂ = 0.000 000 166 857 N','the canvas label, decimal (derive)');
    eq(L.lab2,'Force on m₂ by m₁ = 0.000 000 166 857 N','both labels read the same magnitude'); });
  withState({fmode:'sci'},()=>eq(labModel(ST).lab1,'Force on m₁ by m₂ = 1.67 × 10⁻⁷ N','scientific notation (derive: 1.67 x 10^-7)'));
  withState({fmode:'hid'},()=>eq(labModel(ST).lab1,'Force on m₁ by m₂','hidden: the label keeps no value'));
  rel(withState({m1:10,m2:10,i1:-50,i2:50},()=>labModel(ST).Fmag),6.6743e-11,1e-12,'the weakest pull: 10 kg, 10 kg, 10 m (derive)');
  eq(withState({m1:10,m2:10,i1:-50,i2:50},()=>labModel(ST).lab1),'Force on m₁ by m₂ = 0.000 000 000 067 N','its decimal label (derive)');
  rel(withState({m1:1000,m2:1000,i1:-12,i2:12},()=>labModel(ST).Fmag),1.158732638889e-05,1e-12,'the strongest, scaled: 1000 kg each, 2.4 m (derive)');
  eq(withState({m1:1000,m2:1000,i1:-12,i2:12},()=>labModel(ST).lab1),'Force on m₁ by m₂ = 0.000 011 587 326 N','its decimal label (derive)');
  rel(withState({m1:1000,m2:1000,i1:-6,i2:5,cs:true},()=>labModel(ST).Fmag),5.515950413223e-05,1e-12,'the strongest, constant size: 1.1 m (derive)');
  eq(withState({i1:-30,i2:40},()=>labModel(ST).lab1),'Force on m₁ by m₂ = 0.000 000 054 484 N','7 m apart (derive)');
  eq(withState({i1:-30,i2:40,fmode:'sci'},()=>labModel(ST).lab1),'Force on m₁ by m₂ = 5.45 × 10⁻⁸ N','7 m apart, scientific (derive)');
  close(forceOn(-1,1,1,0,2,1),0.25,1e-15,'forceOn: a unit attraction at 2 pulls body 1 by +1/4');
  close(forceOn(1,1,1,0,2,1),-0.25,1e-15,'and a unit repulsion pushes it by -1/4');
  close(forceOn(1,1,1,0,2,2),0.25,1e-15,'while body 2 is pushed by +1/4');

  /* ---------- G. the inverse square ---------- */
  withState({view:'inv'},()=>{
    const M=buildModel(), I=M.I;
    for(const [r,F] of [[1.5,1.186542222222e-06],[2,6.6743e-07],[4,1.668575e-07],[8,4.1714375e-08],[10,2.66972e-08]])
      rel(forceMag(TRACK.C,100,400,r),F,1e-12,'F at '+r+' m (derive)');
    rel(I.F2r,4.1714375e-08,1e-12,'F at 2r (derive)'); rel(M.L.Fmag/I.F2r,4,1e-12,'doubling r quarters F');
    close(I.slope,-2,1e-9,'the log-log slope measured off the model is -2');
    let flat=0; for(const v of I.lin.Fr2) flat=Math.max(flat,Math.abs(v/2.66972e-06-1));
    ok(flat<1e-12,'F r^2 is flat at G m1 m2 over the whole reachable range (worst '+flat.toExponential(2)+')');
    rel(I.prod,2.66972e-06,1e-12,'the law\'s constant G m1 m2 (derive)');
    rel(I.lin.F3r2[0]/I.lin.F3r2[100],10/1.5,1e-12,'the inverse-cube comparison falls as 1/r');
    rel(I.lin.F3r2[0],7.119253333333e-06,1e-12,'and passes through the live point: F r^3 / d_min (derive)');
    rel(I.lo,0.5*1.402180083967,1e-12,'the log-log window opens at half the touching distance'); eq(I.hi,20,'and closes at twice the track');
    rel(I.Fnear,1.186542222222e-06,1e-12,'F at the closest allowed distance (derive)'); rel(I.Ffar,2.66972e-08,1e-12,'and at the far end (derive)'); });

  /* ---------- H. the mass product ---------- */
  withState({view:'prod'},()=>{
    const P=buildModel().P;
    rel(P.k,4.1714375e-12,1e-12,'k = G/r^2 at 4 m (derive)'); eq(P.levels.length,12,'twelve 1-2-5 contour levels (derive)');
    rel(P.levels[0],5e-10,1e-12,'first 5e-10 N (derive)'); rel(P.levels[11],2e-6,1e-12,'last 2e-6 N (derive)');
    for(const C of P.contours){ const i=40; rel(forceMag(TRACK.C,C.m1s[i],C.m2s[i],4),C.F,1e-12,'a point on the '+sciPlain(C.F,1)+' N contour feels that force'); }
    rel(P.dFdm1,4.1714375e-12*400,1e-12,'dF/dm1 = G m2/r^2'); rel(P.dFdm2,4.1714375e-12*100,1e-12,'dF/dm2 = G m1/r^2');
    eq(P.nBlocked,0,'at 4 m no pair is too big');
    rel(P.slopeSc,1.397940008672,1e-10,'strongest-pull log slope, real size (derive)'); rel(P.slopeCs,2,1e-12,'constant size: exactly 2 (derive)');
    for(const [m,sc,cs] of [[10,1.853972222222e-08,5.515950413223e-09],[100,4.634930555556e-07,5.515950413223e-07],[500,4.1714375e-06,1.378987603306e-05],[1000,1.158732638889e-05,5.515950413223e-05]]){
      rel(fmaxEqual(m,false),sc,1e-12,'F max, two '+m+'-kg spheres, real size (derive)'); rel(fmaxEqual(m,true),cs,1e-12,'constant size (derive)'); }
    const mm=1000, rt=2*sphereRadius(mm,false);
    rel(forceMag(TRACK.C,mm,mm,rt),1.224049491735e-05,1e-12,'touching 1000-kg spheres (derive)');
    rel(forceMag(TRACK.C,mm,mm,rt),G_N*Math.pow(mm,4/3)*Math.pow(4*PI*RHO_S/3,2/3)/4,1e-12,'= G m^(4/3)(4 pi rho/3)^(2/3)/4'); });
  withState({view:'prod',i1:-10,i2:10},()=>{ const P=buildModel().P; eq(P.nBlocked,3148,'at 2.0 m: 3148 pairs too big (derive)'); eq(P.edge[99],310,'the lightest blocked partner of 1000 kg is 310 kg (derive)'); });
  withState({view:'prod',i1:-8,i2:7},()=>{ const P=buildModel().P; eq(P.nBlocked,8323,'at 1.5 m: 8323 pairs (derive)'); eq(P.edge[99],20,'1000 kg blocks every partner above 10 kg (derive)'); });

  /* ---------- I. let them go ---------- */
  { const F=fallModel(100,400,-3,1,false);
    eq(F.r0,4,'released 4 m apart'); rel(F.rc,1.402180083967,1e-12,'contact at r1 + r2 (derive)'); rel(F.tau,30966.14372415,1e-12,'sqrt(r0^3 / 2GM) (derive)');
    rel(F.tc,43795.84797766,1e-11,'contact after 43795.8 s (derive closed form)'); rel(F.tc,43795.84797801,1e-10,'= scipy solve_ivp integrating both bodies (derive CHECK)');
    rel(F.tff,48641.50481689,1e-12,'the full fall to r = 0 (derive)'); rel(F.xcm,0.2,1e-15,'the centre of mass (derive)'); rel(F.clock,43795.84797766/10,1e-11,'the clock factor: the run is 10 s');
    close(fallTime(F.r0,F.r0,F.GM),0,1e-12,'t(r0) = 0'); rel(fallTime(1e-12,F.r0,F.GM),F.tff,1e-6,'t(0) = pi/2 sqrt(r0^3/2GM)');
    const want={150:[10948.96199441,3.87364903867,-2.898919230965,0.9747298077411,1.866345282634e-05,-4.665863206584e-06],
                300:[21897.92398883,3.476916945367,-2.581533556296,0.8953833890741,4.008215105956e-05,-1.002053776489e-05],
                450:[32846.88598324,2.739115751617,-1.991292601288,0.7478231503221,7.011247047384e-05,-1.752811761846e-05],
                600:[43795.84797766,1.402180083967,-0.9217440672229,0.4804360168057,0.0001406583365317,-3.516458413292e-05]};
    for(const k in want){ const w=want[k], s=fallState(F,k/FALL_FRAMES*F.tc);
      rel(s.t,w[0],1e-12,'frame '+k+': t (derive)'); rel(s.r,w[1],1e-10,'frame '+k+': r (derive brentq)');
      rel(s.x1,w[2],1e-9,'frame '+k+': x1 (derive solve_ivp)'); rel(s.x2,w[3],1e-9,'frame '+k+': x2 (derive solve_ivp)');
      rel(s.v1,w[4],1e-8,'frame '+k+': v1 (derive)'); rel(s.v2,w[5],1e-8,'frame '+k+': v2 (derive)');
      close(F.m1*s.v1+F.m2*s.v2,0,1e-18,'frame '+k+': the momenta cancel'); rel((F.m1*s.x1+F.m2*s.x2)/F.M,0.2,1e-12,'frame '+k+': the centre of mass has not moved'); }
    const s1=fallState(F,F.tc); rel(Math.abs(s1.rdot),0.0001758229206646,1e-10,'closing speed at contact (derive)');
    rel(F.m1*s1.v1,0.01406583365317,1e-10,'momentum at contact (derive)');
    /* the independent route: RK4 on BOTH bodies, each pushed by forceOn — Newton's third law is an output */
    let y=[-3,1,0,0]; const N=4000, dt=F.tc/N;
    const f=z=>{ const a1=forceOn(TRACK.C,100,400,z[0],z[1],1)/100, a2=forceOn(TRACK.C,100,400,z[0],z[1],2)/400; return [z[2],z[3],a1,a2]; };
    let rMid=null, pmax=0;
    for(let i=0;i<N;i++){ const k1=f(y), k2=f(y.map((v,j)=>v+dt/2*k1[j])), k3=f(y.map((v,j)=>v+dt/2*k2[j])), k4=f(y.map((v,j)=>v+dt*k3[j]));
      y=y.map((v,j)=>v+dt*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6);
      pmax=Math.max(pmax,Math.abs(100*y[2]+400*y[3])); if(i===N/2-1) rMid=y[1]-y[0]; }
    rel(rMid,fallState(F,F.tc/2).r,1e-10,'RK4 on both bodies agrees with the closed form at t_c/2');
    rel(y[1]-y[0],F.rc,1e-8,'and reaches contact at t_c'); ok(pmax<1e-16,'total momentum stays zero in the RK4 run ('+pmax.toExponential(1)+')');
    let lo=F.rc+1e-9, prev=fallTime(lo,F.r0,F.GM), mono=true;
    for(let i=1;i<=200;i++){ const r=F.rc+(F.r0-F.rc)*i/200, t=fallTime(r,F.r0,F.GM); if(t>prev) mono=false; prev=t; }
    ok(mono,'t(r) decreases monotonically from contact to release (the bisection needs it)'); }
  { const F=fallModel(100,400,-3,1,true);
    eq(F.rc,1,'constant size: contact at 1 m'); rel(F.tc,45836.40343911,1e-11,'constant-size contact time (derive)');
    rel(fallState(F,150/FALL_FRAMES*F.tc).r,3.8614578575,1e-10,'frame 150 (derive)'); rel(fallState(F,450/FALL_FRAMES*F.tc).r,2.599600027411,1e-10,'frame 450 (derive)');
    rel(Math.abs(fallState(F,F.tc).rdot),0.0002237347760184,1e-10,'closing speed at contact (derive)'); }
  { const F=fallModel(1000,10,-5,5,false);
    rel(F.tc,132071.4676861,1e-11,'1000 kg and 10 kg, 10 m apart: contact time (derive)'); rel(F.xcm,-4.90099009901,1e-11,'the centre of mass sits by the heavy one (derive)');
    const s=fallState(F,F.tc); rel(s.v1,2.826961696628e-06,1e-9,'the heavy sphere barely moves (derive)'); rel(s.v2,-0.0002826961696628,1e-9,'the light one does the falling (derive)');
    rel(fallState(F,300/FALL_FRAMES*F.tc).r,8.449150409963,1e-10,'frame 300 (derive)'); }
  withState({view:'fall'},()=>{ const M=buildModel(); rel(M.perF,5e-7,1e-12,'the fall\'s force arrows: 1 m = 5e-7 N (derive ladder)'); rel(M.perV,5e-5,1e-12,'its velocity arrows: 1 m = 5e-5 m/s (derive ladder)');
    eq(M.run,false,'before release nothing runs'); eq(M.fs.r,4,'and the spheres sit at r0'); });
  withState({view:'fall',release:true,frames:300},()=>{ const M=buildModel(); eq(RUN.frame,300,'300 frames stepped'); rel(M.fs.r,3.476916945367,1e-10,'the model run is at the frame-300 separation (derive)'); ok(!M.done,'not yet touching'); });
  withState({view:'fall',release:true,frames:700},()=>{ const M=buildModel(); eq(RUN.frame,600,'the run stops at frame 600'); ok(M.done,'touching'); rel(M.fs.r,1.402180083967,1e-12,'at r1 + r2'); ok(!runStep(),'no further steps'); });
  rel(arrowStep(9,-10),1e-7,1e-12,'arrow ladder step 9 = 1e-7 N/m (derive)'); rel(arrowStep(0,-10),1e-10,1e-12,'step 0 (derive)'); rel(arrowStep(17,-10),5e-5,1e-12,'step 17 (derive)');
  rel(arrowStep(10,-10),2e-7,1e-12,'step 10: the ladder\'s 2 rung (derive)');
  eq(hms(43795.84797766),'12 h 10 min','the contact time reads 12 h 10 min'); eq(hms(59.6),'1 min 00 s','hms carries a rounded 60 s into the minute'); eq(hms(5),'5 s','and seconds alone');

  /* ---------- J. the models, the readouts, the scene ---------- */
  for(const [v] of TABS) for(const over of [{},{cs:true},{m1:1000,m2:10,i1:-50,i2:50},{fmode:'hid'},{release:true,frames:600}]){
    const M=withState(Object.assign({view:v},over),()=>buildModel());
    const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over)); }
  { const ro=withState({view:'lab'},()=>readoutHTML(buildModel()));
    ok(ro.indexOf('1.669 &times; 10<sup>-7</sup> N')>=0,'the lab readout prints F = 1.669e-7 N off the model');
    ok(ro.indexOf('17.0 &micro;g')>=0,'and the 17.0-microgram weight'); ok(ro.indexOf('1.66852 &times; 10<sup>-7</sup>')>=0,'and PhET\'s 1.66852e-7');
    const rf=withState({view:'fall'},()=>readoutHTML(buildModel())); ok(rf.indexOf('12 h 10 min')>=0,'the fall readout prints the 12 h 10 min contact time');
    const ri=withState({view:'inv'},()=>readoutHTML(buildModel())); ok(ri.indexOf('4.000000')>=0,'the inverse-square readout prints F(r)/F(2r) = 4.000000');
    const rp=withState({view:'prod'},()=>readoutHTML(buildModel())); ok(rp.indexOf('1.398')>=0,'the product readout prints the 1.398 slope'); }
  { const shot=makeShot(1100,712); const S=makeScene({getContext:()=>shot});
    Object.assign(ST,DEFAULTS); simReset();
    ok(!S.step(),'the lab has no clock'); ST.view='fall'; ok(!S.step(),'the fall idles until release');
    ok(startRun(ST),'release starts a run'); ok(S.step(),'then a frame advances'); eq(RUN.frame,1,'by one frame');
    ST.running=false; ok(!S.step(),'paused: no frame'); ST.running=true; ok(S.step(),'resumed');
    ST.view='inv'; ok(!S.step(),'another view does not step the fall');
    /* the pointer: the spheres and the ruler in the lab */
    Object.assign(ST,DEFAULTS); simReset();
    let LS=labSpec(buildModel()), Gm=labGeo(shot,S.W,S.H,LS);
    ok(S.pointer('down',Gm.X(-3),Gm.yT),'pointer-down on m1 grabs it'); eq(DRAG.what,1,'it is m1');
    S.pointer('move',Gm.X(-2),Gm.yT); eq(ST.i1,-20,'dragging m1 by 1 m moves it to -2.0 m');
    S.pointer('move',Gm.X(4),Gm.yT); eq(ST.i1,-5,'and it stops 1.5 m short of m2');
    ok(S.pointer('up',0,0),'pointer-up releases'); eq(DRAG.what,null,'nothing dragged');
    ok(S.pointer('down',Gm.X(1)+0.5*Gm.s,Gm.yT),'grabbing m2 off-centre'); S.pointer('move',Gm.X(3)+0.5*Gm.s,Gm.yT); eq(ST.i2,30,'keeps the grab offset: m2 to 3.0 m'); S.pointer('up',0,0);
    LS=labSpec(buildModel()); Gm=labGeo(shot,S.W,S.H,LS);
    const g=Gm.ruler; ok(S.pointer('down',(g.x0+g.x1)/2,g.y0+10),'pointer-down on the ruler grabs it'); eq(DRAG.what,'ruler','it is the ruler');
    S.pointer('move',(g.x0+g.x1)/2+2*Gm.s,g.y0+10); eq(ST.rulerI,-30,'the ruler moves 2 m (snapped)');
    S.pointer('move',(g.x0+g.x1)/2+2*Gm.s,g.y0-400); rel(Gm.Y(ST.rulerY),Gm.ruler.ryLo,1e-9,'held below the arrow rows'); S.pointer('up',0,0);
    ok(!S.pointer('down',Gm.b.x+2,Gm.b.y+2),'a pointer-down on empty stage grabs nothing');
    ST.view='inv'; ok(!S.pointer('down',Gm.X(-3),Gm.yT),'the other views ignore the pointer'); ST.view='lab';
    rulerToM1(ST); eq(ST.rulerI,ST.i1,'ruler to m1: its zero on the centre of m1'); eq(ST.rulerY,0,'with its tick edge on the centre line');
    rulerHome(ST); eq(ST.rulerI,-50,'ruler home: zero at -5 m'); eq(ST.rulerY,null,'at its home height');
    setRuler(ST,-20,0); eq(ST.rulerI,-100,'the ruler stops half a ruler left of the track'); setRuler(ST,20,0); eq(ST.rulerI,50,'and at the right end');
    Object.assign(ST,stSave); simReset(); }

  /* ---------- K. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['lab default',{view:'lab'},6],['lab constant size',{view:'lab',cs:true,m1:1000,m2:10},6],['lab scientific',{view:'lab',fmode:'sci'},6],
    ['lab hidden',{view:'lab',fmode:'hid'},6],['lab heavy close',{view:'lab',m1:1000,m2:1000,i1:-12,i2:12},6],['lab light far',{view:'lab',m1:10,m2:10,i1:-50,i2:50},6],
    ['lab arrows tiny',{view:'lab',arrowK:17},6],['lab arrows huge',{view:'lab',arrowK:0},6],['lab ruler measuring',{view:'lab',rulerI:-30,rulerY:0},6],
    ['lab no distance',{view:'lab',showDist:false},6],['lab at the walls',{view:'lab',i1:-50,i2:50,m1:1000,m2:1000},6],
    ['inv default',{view:'inv'},5],['inv heavy close',{view:'inv',m1:1000,m2:1000,i1:-12,i2:12},5],['inv light far',{view:'inv',m1:10,m2:10,i1:-50,i2:50},5],['inv constant',{view:'inv',cs:true},5],
    ['prod default',{view:'prod'},3],['prod blocked',{view:'prod',i1:-10,i2:10},4],['prod constant',{view:'prod',cs:true,i1:-6,i2:5,m1:1000,m2:1000},3],['prod light',{view:'prod',m1:10,m2:20},3],
    ['fall idle',{view:'fall'},6],['fall running',{view:'fall',release:true,frames:300},6],['fall touching',{view:'fall',release:true,frames:600},6],
    ['fall constant',{view:'fall',cs:true,release:true,frames:450},6],['fall heavy light',{view:'fall',m1:1000,m2:10,i1:-50,i2:50,release:true,frames:400},6],
  ];
  layoutSweep(ok,withState,CONFIGS,SIZES);

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
