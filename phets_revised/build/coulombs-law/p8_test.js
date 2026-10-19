
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/coulombs-law/refvals.txt, the printed output of     *
 *  derive.py (scipy.constants CODATA 2022), read in full.             *
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
    Object.assign(ST,DEFAULTS,over);
    try{ return fn(); } finally{ Object.assign(ST,stSave); }
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  eq(symRound(-2.5),-3,'symRound(-2.5) = -3, halves away from zero'); eq(symRound(14.499999999999998),14,'a hair under a half rounds down');
  eq(tickNum(-2),'−2','tick numbers carry a true minus'); eq(tickNum(0.5000000000000001),'0.5','and no floating-point tail');

  /* ---------- A. the constants, against absolute numbers ---------- */
  eq(EPS0,8.8541878188e-12,'eps0 (scipy CODATA 2022)'); rel(K_E,8987551786.170797,1e-15,'k = 1/(4 pi eps0) (derive)');
  eq(E_CH,1.602176634e-19,'e, exact since 2019'); eq(G_N,6.6743e-11,'G (CODATA 2022)');
  eq(M_E,9.1093837139e-31,'m_e (CODATA 2022)'); eq(M_P,1.67262192595e-27,'m_p (CODATA 2022)'); eq(A0,5.29177210544e-11,'the Bohr radius (CODATA 2022)');
  eq(K_PHET,8987551e3,'PhET\'s k, 8.987551e9'); eq(E_PHET,1.6021766208e-19,'PhET\'s e, CODATA 2014');
  rel(K_E/K_PHET-1,8.747330593195e-08,1e-6,'k / k_PhET - 1 (derive)'); rel(E_CH/E_PHET-1,8.238791870951e-09,1e-6,'e / e_PhET - 1 (derive)');
  eq(Q_MAX,10,'charges within +-10 units');
  const TM=TRACKS.macro, TA=TRACKS.atomic;
  eq(TM.R,0.00675,'macro radius 6.75 mm (PhET)'); eq(TM.q,0.001,'macro grid 1 mm'); eq(TM.perM,1000,'1000 counts per metre'); eq(TM.sep,0.001,'macro gap 1 mm asked for');
  eq(TM.iL,-50,'macro track from -5 cm'); eq(TM.iR,50,'to +5 cm'); eq(TM.qSI,1e-6,'microcoulombs'); eq(TM.uPerM,100,'centimetres'); eq(TM.places,3,'3 decimals (PhET)');
  eq(TA.R,9.5e-13,'atomic radius 0.95 pm (PhET)'); eq(TA.q,1e-12,'atomic grid 1 pm'); eq(TA.perM,1e12,'1e12 counts per metre'); eq(TA.sep,1e-13,'atomic gap 0.1 pm');
  eq(TA.iL,-50,'atomic track from -50 pm'); eq(TA.iR,50,'to +50 pm'); eq(TA.qSI,E_CH,'charge in e'); eq(TA.uPerM,1e12,'picometres'); eq(TA.places,9,'9 decimals (PhET)');
  eq(TM.C,K_E,'like charges repel: C = +k'); eq(TA.C,K_E,'on both scales');

  /* ---------- B. PhET's closest distances, floating point and all ---------- */
  eq(chargeSteps(TM),14,'macro: 6.75 + 6.75 + 1 mm = 14.4999... snaps DOWN to 14 mm (derive)');
  eq(chargeSteps(TA),2,'atomic: 0.95 + 0.95 + 0.1 pm = 2 pm (derive)');
  rel(14/TM.perM-2*TM.R,0.0005,1e-9,'so the macro gap is 0.5 mm, half what PhET asks for (derive)');
  rel(2/TA.perM-2*TA.R,1e-13,1e-9,'and the atomic gap 0.1 pm (derive)');
  /* a stated property, not a blind spot: with PhET's numbers the gap it asks for
     changes nothing on either screen — 13.5 mm without it also rounds (half away
     from zero) to 14, and 1.9 pm to 2 — so dropping it is an equivalent mutant
     here (it is caught in gravity-force-lab, where the gap matters) */
  eq(symRound((2*TM.R)/TM.q),chargeSteps(TM),'macro: the closest distance is 14 mm with or without the gap');
  eq(symRound((2*TA.R)/TA.q),chargeSteps(TA),'atomic: 2 pm with or without the gap');
  rel(arrowStep(13,ARROW_E0.macro),200,1e-12,'the macro arrow scale starts at 200 N per cm (ladder step 13)');
  rel(arrowStep(15,ARROW_E0.atomic),1e-7,1e-12,'the atomic one at 1e-7 N per pm (step 15)');
  withState({},()=>{ rel(screenModel(ST,'macro').per,200,1e-12,'the macro model carries it'); rel(screenModel(ST,'atomic').per,1e-7,1e-12,'and the atomic model'); });

  /* ---------- C. the forces ---------- */
  const MAC=[[-4,8,-10,20,319.5573968416,'319.557','3.20 × 10²'],[10,10,-7,7,-4585.485605189,'4585.486','4.59 × 10³'],
             [1,-1,-50,50,0.8987551786171,'0.899','8.99 × 10⁻¹'],[5,5,-10,20,-249.6542162825,'249.654','2.50 × 10²'],[-10,10,-7,7,4585.485605189,'4585.486','4.59 × 10³']];
  for(const [q1,q2,i1,i2,F1,dec,sci] of MAC) withState({mq1:q1,mq2:q2,mi1:i1,mi2:i2},()=>{
    const L=screenModel(ST,'macro'), tag='macro '+q1+'/'+q2+' uC at '+i1+'/'+i2+' mm: ';
    rel(L.F1,F1,1e-12,tag+'force on q1 (derive)'); rel(L.F2,-F1,1e-12,tag+'force on q2 (derive)'); close(L.F1+L.F2,0,1e-9,tag+'equal and opposite, from two evaluations');
    rel(L.Fmag,Math.abs(F1),1e-12,tag+'|F| (derive)'); eq(decGrouped(L.Fmag,3),dec,tag+'PhET decimal (derive)'); eq(sciText(L.Fmag,2),sci,tag+'PhET scientific (derive)');
    eq(L.kind,q1*q2<0?'attract':'repel',tag+(q1*q2<0?'unlike signs attract':'like signs repel'));
    ok(q1*q2<0?L.F1>0:L.F1<0,tag+(q1*q2<0?'q1 is pulled toward q2 (+x)':'q1 is pushed away from q2 (-x)')); });
  withState({},()=>{ const L=screenModel(ST,'macro');
    rel(L.kq,-0.2876016571575,1e-12,'macro k q1 q2 at the defaults (derive)'); rel(L.Fphet,319.5573688889,1e-12,'PhET\'s readout with its k (derive)');
    eq(L.lab1,'Force on q₁ by q₂ = 319.557 N','the macro label, decimal (derive)'); eq(L.lab2,'Force on q₂ by q₁ = 319.557 N','both labels the same magnitude');
    rel(L.r,0.03,1e-15,'3 cm apart'); rel(L.gap,0.0165,1e-12,'1.65 cm between surfaces'); rel(L.dmin,0.014,1e-15,'closest 1.4 cm'); });
  const ATO=[[-2,4,-20,20,1.153538775389e-06,'0.000 001 154','1.15 × 10⁻⁶'],[10,10,-1,1,-0.005767693876946,'0.005 767 694','5.77 × 10⁻³'],
             [1,-1,-50,50,2.307077550778e-08,'0.000 000 023','2.31 × 10⁻⁸'],[3,3,-20,20,-1.297731122313e-06,'0.000 001 298','1.30 × 10⁻⁶']];
  for(const [q1,q2,i1,i2,F1,dec,sci] of ATO) withState({aq1:q1,aq2:q2,ai1:i1,ai2:i2},()=>{
    const L=screenModel(ST,'atomic'), tag='atomic '+q1+'/'+q2+' e at '+i1+'/'+i2+' pm: ';
    rel(L.F1,F1,1e-12,tag+'force on q1 (derive)'); rel(L.F2,-F1,1e-12,tag+'force on q2 (derive)'); close(L.F1+L.F2,0,1e-20,tag+'equal and opposite');
    eq(decGrouped(L.Fmag,9),dec,tag+'PhET decimal (derive)'); eq(sciText(L.Fmag,2),sci,tag+'PhET scientific (derive)'); });
  withState({},()=>{ const L=screenModel(ST,'atomic');
    rel(L.kq,-1.845662040623e-27,1e-12,'atomic k q1 q2 (derive)'); rel(L.Fphet,1.153538655478e-06,1e-12,'PhET\'s readout with its k and e (derive)');
    eq(L.lab1,'Force on q₁ by q₂ = 1.15 × 10⁻⁶ N','the atomic label, scientific by default (derive)'); eq(L.mode,'sci','the atomic screen starts scientific (PhET)');
    rel(L.acc,1.153538775389e-06/1.67262192595e-27,1e-12,'the pull on a proton as an acceleration'); });
  withState({mForce:false},()=>eq(screenModel(ST,'macro').lab1,'Force on q₁ by q₂','force values off: the label keeps no value'));
  withState({mSci:true},()=>eq(screenModel(ST,'macro').lab1,'Force on q₁ by q₂ = 3.20 × 10² N','macro in scientific notation (derive)'));
  withState({mq1:0},()=>{ const L=screenModel(ST,'macro'); eq(L.Fmag,0,'a zero charge: no force'); eq(L.kind,'none','and no direction'); eq(L.lab1,'Force on q₁ by q₂ = 0.000 N','labelled 0.000 N'); });
  withState({aq2:0},()=>eq(screenModel(ST,'atomic').lab1,'Force on q₁ by q₂ = 0.000 000 000 N','a zero force stays decimal in scientific mode (PhET)'));

  /* ---------- D. the actions ---------- */
  withState({},()=>{
    setCharge(ST,'macro',1,14); eq(ST.mq1,10,'a charge is clamped to +10'); setCharge(ST,'macro',2,-12); eq(ST.mq2,-10,'and to -10');
    setCharge(ST,'atomic',1,2.6); eq(ST.aq1,3,'charge is ROUNDED to whole units (2.6 -> 3)');
    eq(ST.mi1,-10,'a new charge moves nothing (fixed radius)'); eq(ST.mi2,20,'on either side');
    setPosCL(ST,'macro',1,0.02); eq(ST.mi1,6,'dragging q1 onto q2 stops it 14 mm short'); setPosCL(ST,'macro',2,-0.05); eq(ST.mi2,20,'q2 held: the closest is now 14 mm from q1 at 6 mm');
    setPosCL(ST,'macro',2,0.0104); eq(ST.mi2,20,'10.4 mm is inside q1\'s exclusion: held at 6 + 14 = 20 mm');
    setPosCL(ST,'macro',2,0.0414); eq(ST.mi2,41,'41.4 mm snaps to 41 mm'); setPosCL(ST,'macro',2,0.0416); eq(ST.mi2,42,'41.6 mm snaps to 42 mm');
    setPosCL(ST,'macro',1,-0.09); eq(ST.mi1,-50,'held at the left end, -5 cm');
    setPosCL(ST,'atomic',1,2e-11); eq(ST.ai1,18,'atomic q1 dragged onto q2 stops 2 pm short');
    setPosCL(ST,'atomic',2,9e-11); eq(ST.ai2,50,'atomic q2 held at +50 pm');
    rulerToQ1(ST,'macro'); eq(ST.mRulerI,ST.mi1,'ruler to q1'); eq(ST.mRulerY,0,'tick edge on the centre line');
    rulerHomeCL(ST,'macro'); eq(ST.mRulerI,-50,'ruler home'); eq(ST.mRulerY,null,'at its home height');
    setRulerCL(ST,'atomic',-1e-9,0); eq(ST.aRulerI,-100,'the atomic ruler stops half a ruler left of the track');
    setRulerCL(ST,'atomic',1e-9); eq(ST.aRulerI,50,'and at the right end'); eq(ST.aRulerY,0,'a y left undefined keeps the height'); });

  /* ---------- E. the inverse square ---------- */
  for(const [w,over,F0,Ft,F2,kq,lo,hi,F3] of [['macro',{scale:'macro'},1467.355393661,28.76016571575,79.88934921041,0.2876016571575,0.00675,0.2,0.6162892653374],
      ['atomic',{scale:'atomic'},0.0004614155101557,1.845662040623e-07,2.883846938473e-07,1.845662040623e-27,9.5e-13,2e-10,3.691324081245e-26]])
    withState(Object.assign({view:'inv'},over),()=>{ const I=buildModel().I, tag='inverse square, '+w+': ';
      rel(I.Fnear,F0,1e-12,tag+'F at the closest distance (derive)'); rel(I.Ffar,Ft,1e-12,tag+'F across the track (derive)'); rel(I.F2r,F2,1e-12,tag+'F at 2r (derive)');
      rel(I.prod,kq,1e-12,tag+'|k q1 q2| (derive)'); rel(I.lo,lo,1e-12,tag+'window from half the touching distance (derive)'); rel(I.hi,hi,1e-12,tag+'to twice the track (derive)');
      rel(I.lin.F3r2[0],F3,1e-12,tag+'the inverse-cube comparison through the live point (derive)');
      close(I.slope,-2,1e-9,tag+'log-log slope -2');
      let flat=0; for(const v of I.lin.Fr2) flat=Math.max(flat,Math.abs(v/kq-1)); ok(flat<1e-12,tag+'|F| r^2 flat to '+flat.toExponential(1)); });
  withState({view:'inv',mq1:0},()=>{ const I=buildModel().I; eq(I.prod,0,'a zero charge: the law\'s constant is zero'); });

  /* ---------- F. the charge product ---------- */
  for(const [w,ku,f0,f1] of [['macro',9.986168651301,10,500],['atomic',1.441923469236e-07,2e-07,1e-05]])
    withState({view:'prod',scale:w},()=>{ const P=buildModel().P, L=buildModel().L, tag='charge product, '+w+': ';
      rel(P.ku,ku,1e-12,tag+'|F| per unit^2 of product (derive)'); eq(P.levels.length,6,tag+'six contour levels (derive)');
      rel(P.levels[0],f0,1e-12,tag+'first level (derive)'); rel(P.levels[5],f1,1e-12,tag+'last level (derive)');
      for(const C of P.contours){ const i=30; rel(ku*C.xs[i]*C.ys[i],C.F,1e-12,tag+'a point on the '+sciPlain(C.F,1)+' N contour feels it'); }
      rel(P.F2s[40],forceOn(K_E,L.q1,10*L.T.qSI,L.x1,L.x2,2),1e-12,tag+'the q2 line ends at q2 = +10');
      close(P.F2s[20],0,1e-30,tag+'and crosses zero at q2 = 0'); rel(P.F1s[40],-P.F2s[40],1e-12,tag+'the force on q1 mirrors it');
      rel(P.Fps[40],ku*100,1e-12,tag+'the product line: +100 units^2 pushes q2 by ku x 100');
      ok(P.Fps[0]<0&&P.Fps[40]>0,tag+'negative products attract, positive repel');
      rel(P.dFdq2,ku*L.Q1,1e-12,tag+'dF2/dq2 = ku q1'); });
  withState({view:'prod',mq1:0},()=>eq(buildModel().P.live.c,0,'a zero charge has no live contour'));

  /* ---------- G. electricity and gravity ---------- */
  withState({view:'grav'},()=>{ const E=buildModel().E;
    rel(E.ratioEP,2.268661431486e+39,1e-11,'k e^2 / (G m_e m_p) (derive)'); rel(E.ratioPP,1.235551631585e+36,1e-11,'two protons (derive)'); rel(E.ratioEE,4.165608752511e+42,1e-11,'two electrons (derive)');
    rel(E.FeA0,8.238723503832e-08,1e-11,'Coulomb at the Bohr radius (derive)'); rel(E.FgA0,3.631535049475e-47,1e-11,'gravity there (derive)');
    rel(E.FeA0/E.FgA0,E.ratioEP,1e-12,'the ratio at the Bohr radius is the ratio');
    rel(E.Fe[0]/E.Fg[0],E.ratioEP,1e-12,'and at a femtometre'); rel(E.Fe[90]/E.Fg[90],E.ratioEP,1e-12,'and at a metre: distance cancels');
    rel(E.mEq,65643.66647458,1e-11,'equal masses for the macro defaults (derive)'); rel(E.rhoEq,50955715297.57,1e-11,'their density in 6.75-mm spheres (derive)');
    rel(E.ms[50]/1000,11604.27042653*10/1000,1e-11,'per microcoulomb sqrt(k/G) x 1e-6 C, times 10 at 100 uC^2 (derive)');
    rel(forceMag(G_N,E.mEq,E.mEq,0.03),319.5573968416,1e-12,'and those masses really pull 319.557 N at 3 cm (derive)');
    rel(E.Fa0,1.153538775389e-06,1e-12,'the atomic pair at 40 pm (derive)'); eq(E.prodM,32,'|q1 q2| = 32 uC^2'); });
  rel(ratioEG(M_E,M_P),2.268661431486e+39,1e-11,'ratioEG (derive)'); rel(equalMass(1e-6,1e-6),11604.27042653,1e-11,'equalMass per microcoulomb (derive)');

  /* ---------- H. the models, the readouts, the scene ---------- */
  for(const [v] of TABS) for(const over of [{},{scale:'atomic'},{mq1:0,aq1:0},{mForce:false,aForce:false},{mq1:10,mq2:10,mi1:-7,mi2:7}]){
    const M=withState(Object.assign({view:v},over),()=>buildModel());
    const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over)); }
  { const rm=withState({view:'macro'},()=>readoutHTML(buildModel()));
    ok(rm.indexOf('319.6 N')>=0,'the macro readout prints |F| = 319.6 N off the model'); ok(rm.indexOf('attract (unlike signs)')>=0,'and says attract');
    ok(rm.indexOf('1.40 cm (a 0.50 mm gap)')>=0,'and the 1.40-cm closest distance with its 0.50-mm gap');
    ok(rm.indexOf('319.5574 N')>=0,'and PhET\'s 319.5574 N');
    const ra=withState({view:'atomic'},()=>readoutHTML(buildModel())); ok(ra.indexOf('1.154 &times; 10<sup>-6</sup> N')>=0,'the atomic readout prints 1.154e-6 N');
    ok(ra.indexOf('6.90 &times; 10<sup>20</sup> m/s&sup2;')>=0,'and the 6.90e20 m/s^2 on a proton');
    const rg=withState({view:'grav'},()=>readoutHTML(buildModel())); ok(rg.indexOf('2.269 &times; 10<sup>39</sup>')>=0,'the gravity readout prints the 2.269e39 ratio');
    ok(rg.indexOf('65.6 tonnes each')>=0,'and the 65.6-tonne equal masses');
    const rr=withState({view:'macro',mq1:5,mq2:5},()=>readoutHTML(buildModel())); ok(rr.indexOf('repel (like signs)')>=0,'like charges read repel'); }
  { const shot=makeShot(1100,712); const S=makeScene({getContext:()=>shot});
    Object.assign(ST,DEFAULTS);
    ok(!S.step(),'nothing here runs on a clock');
    for(const w of ['macro','atomic']){
      ST.view=w; Object.assign(ST,DEFAULTS); ST.view=w;
      const p=PRE[w], u=TRACKS[w].uPerM;
      let LS=labSpec(buildModel()), Gm=labGeo(shot,S.W,S.H,LS);
      const X1=Gm.X(LS.bodies[0].x);
      ok(S.pointer('down',X1,Gm.yT),w+': pointer-down on q1 grabs it'); eq(DRAG.what,1,w+': it is q1');
      const step=w==='macro'?0.5:5;                              /* 0.5 cm, 5 pm */
      S.pointer('move',X1+step*Gm.s,Gm.yT); eq(ST[p+'i1'],w==='macro'?-5:-15,w+': the drag moves q1 by half a unit of the ruler');
      S.pointer('move',X1+60*step*Gm.s,Gm.yT); eq(ST[p+'i1'],ST[p+'i2']-chargeSteps(TRACKS[w]),w+': and stops at PhET\'s closest distance');
      ok(S.pointer('up',0,0),w+': released');
      LS=labSpec(buildModel()); Gm=labGeo(shot,S.W,S.H,LS);
      /* the hit radius, pinned from both sides: grabbed 0.6 of a radius off
         centre (a dead-centre press cannot see the radius at all), and missed
         just outside it */
      { const X2=Gm.X(LS.bodies[1].x), Rp=Math.max(8,LS.bodies[1].r*Gm.s)+4;
        ok(S.pointer('down',X2+0.6*LS.bodies[1].r*Gm.s,Gm.yT),w+': q2 grabbed 0.6 of a radius off centre'); eq(DRAG.what,2,w+': it is q2'); S.pointer('up',0,0);
        ok(!S.pointer('down',X2+Rp+2,Gm.yT)&&DRAG.what===null,w+': a press 2 px outside the hit radius misses'); }
      const g=Gm.ruler; ok(S.pointer('down',(g.x0+g.x1)/2,g.y0+10),w+': the ruler grabs'); eq(DRAG.what,'ruler',w+': it is the ruler');
      S.pointer('move',(g.x0+g.x1)/2+2*(w==='macro'?1:10)*Gm.s,g.y0+10); eq(ST[p+'RulerI'],w==='macro'?-30:-30,w+': the ruler slides two major ticks');
      S.pointer('up',0,0);
      ok(!S.pointer('down',Gm.b.x+2,Gm.b.y+2),w+': empty stage grabs nothing'); }
    ST.view='inv'; ok(!S.pointer('down',300,300),'the analysis views ignore the pointer'); ST.view='grav'; ok(!S.pointer('down',300,300),'all of them');
    Object.assign(ST,stSave); }

  /* ---------- I. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['macro default',{view:'macro'},6],['macro scientific',{view:'macro',mSci:true},6],['macro hidden',{view:'macro',mForce:false},6],
    ['macro repel',{view:'macro',mq1:5,mq2:5},6],['macro zero',{view:'macro',mq1:0},6],['macro close',{view:'macro',mq1:10,mq2:-10,mi1:-7,mi2:7},6],
    ['macro far',{view:'macro',mq1:1,mq2:-1,mi1:-50,mi2:50},6],['macro ruler on q1',{view:'macro',mRulerI:-10,mRulerY:0},6],['macro arrows huge',{view:'macro',mArrowK:6},6],
    ['atomic default',{view:'atomic'},6],['atomic decimal',{view:'atomic',aSci:false},6],['atomic close',{view:'atomic',aq1:10,aq2:10,ai1:-1,ai2:1},6],
    /* floors from what each draws: at 560 px an atomic charge is a 4-px ball with
       no highlight and a tick for an arrow (4 fills); a zero charge in the
       inverse-square view is the background and a sentence saying why (1) */
    ['atomic far',{view:'atomic',aq1:1,aq2:-1,ai1:-50,ai2:50},4],['atomic zero',{view:'atomic',aq2:0},4],['atomic ruler on q1',{view:'atomic',aRulerI:-20,aRulerY:0},4],
    ['inv macro',{view:'inv'},5],['inv atomic',{view:'inv',scale:'atomic'},5],['inv repel close',{view:'inv',mq1:10,mq2:10,mi1:-7,mi2:7},5],['inv zero',{view:'inv',mq1:0},1],
    ['prod macro',{view:'prod'},5],['prod atomic',{view:'prod',scale:'atomic'},5],['prod repel',{view:'prod',mq1:7,mq2:3},5],['prod zero',{view:'prod',mq1:0},5],
    ['grav default',{view:'grav'},5],['grav zero',{view:'grav',aq1:0,mq1:0},5],['grav big',{view:'grav',mq1:10,mq2:10,aq1:10,aq2:-10,ai1:-1,ai2:1},5],
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
