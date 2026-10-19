
/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) come from REF, emitted from build/charges-and-fields/     *
 *  refvals.txt, the printed output of derive.py (scipy brentq on      *
 *  rays, quad, solve_ivp, fsolve), read in full.                      *
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
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,rot:Math.abs(Mx[1])>1e-9,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
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
function brightness(css){ const c=toRgb(css); return Math.max(c[0],c[1],c[2]); }

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=clone(ST);
  function withState(over,fn){ resetState(over); try{ return fn(); } finally{ resetState(stSave); } }
  const PRE=id=>presetCharges(id);
  const ORD=['single','dipole','like','quad','triangle','rows'];

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(brightness(shade(mix(COL.zero,COL.pos,0.5),0.9))>60,'mix() output is a legal mix() input (a two-stage blend is not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  close(90*DEG,PI/2,1e-15,'DEG converts degrees INTO radians (90 DEG = pi/2)');
  { const c=clipSeg(-1,0.5,2,0.5,{x0:0,x1:1,y0:0,y1:1}); ok(!!c&&Math.abs(c[0])<1e-15&&Math.abs(c[2]-1)<1e-15,'clipSeg cuts a crossing segment at both edges'); ok(clipSeg(2,2,3,3,{x0:0,x1:1,y0:0,y1:1})===null,'and drops one that misses'); }
  close(wrapPi(3*PI/2),-PI/2,1e-15,'wrapPi folds 270° to -90°');

  /* ---------- 1. constants ---------- */
  eq(EPS0,8.8541878188e-12,'eps0, CODATA 2022 (NIST), verbatim');
  rel(KNC,REF.KNC,1e-15,'k = 1/(4 pi eps0) in V m/nC (derive)'); rel(K_SI,REF.K_SI,1e-15,'k in N m^2/C^2 (derive)');
  rel(KNC/K_PHET,REF.KNC_OVER_KPHET,1e-15,'k / PhET\'s 9 = 0.99862: PhET reads 0.14 % high (derive)');
  eq(SENSOR_M_PER_VM,REF.PHET_M[0],'sensor arrow 15 px per V/m at 128 px/m = 0.1171875 m per V/m (PhET\'s value)');
  eq(ARROW_LEN,REF.PHET_M[1],'field arrow 40 px = 0.3125 m (PhET\'s value)'); eq(CHARGE_R,REF.PHET_M[2],'charge radius 12 px = 0.09375 m (PhET\'s value)');
  ok(PLANE.x1-PLANE.x0===8&&PLANE.y1-PLANE.y0===5,'the plane is 8 m x 5 m (PhET WIDTH, HEIGHT)');
  ok(BIN.x0===-1.25&&BIN.x1===1.25&&BIN.y0===-2.3&&BIN.y1===-1.7,'the bin, PhET\'s enclosure bounds');
  ok(ARROW_DX===0.5&&MAP_DX===0.1&&V_SAT===40&&E_SAT===5&&EQ_REFUSE===0.03,'the grids, the saturations and the no-seed radius (PhET\'s values)');
  rel(potentialAt(PRE('single'),1,0),REF.PHET_V1M[1],1e-15,'+1 nC at 1 m reads 8.99 V here (derive); PhET reads '+REF.PHET_V1M[0]);

  /* ---------- 2. the fields ---------- */
  for(const nm of ORD){ const ch=PRE(nm);
    REF.VE[nm].forEach((r,i)=>{ const p=REF.PROBE[i], f=fieldAt(ch,p[0],p[1]), R=sensorReading(ch,p[0],p[1]), tag=nm+' probe '+i+': ';
      rel(f.V,r[0],2e-14,tag+'V (derive)'); rel(potentialAt(ch,p[0],p[1]),r[0],2e-14,tag+'potentialAt agrees');
      rel(f.ex,r[1],3e-14,tag+'Ex (derive)'); rel(f.ey,r[2],3e-14,tag+'Ey (derive)'); rel(R.mag,r[3],2e-14,tag+'|E| (derive)'); close(R.ang,r[4],1e-10,tag+'direction, degrees (derive)'); }); }
  /* an independent route to E inside the suite: central differences of V */
  for(const nm of ORD){ const ch=PRE(nm); let worst=0, wj=0;
    for(const p of REF.PROBE){ const h2=1e-5, f=fieldAt(ch,p[0],p[1]);
      const gx=-(potentialAt(ch,p[0]+h2,p[1])-potentialAt(ch,p[0]-h2,p[1]))/(2*h2), gy=-(potentialAt(ch,p[0],p[1]+h2)-potentialAt(ch,p[0],p[1]-h2))/(2*h2);
      worst=Math.max(worst,Math.hypot(gx-f.ex,gy-f.ey)/Math.hypot(f.ex,f.ey));
      const j=jacAt(ch,p[0],p[1]), fp=fieldAt(ch,p[0]+h2,p[1]), fm=fieldAt(ch,p[0]-h2,p[1]), fq=fieldAt(ch,p[0],p[1]+h2), fn=fieldAt(ch,p[0],p[1]-h2);
      const sc=Math.max(Math.abs(j[0]),Math.abs(j[1]),Math.abs(j[2]));
      wj=Math.max(wj,Math.abs((fp.ex-fm.ex)/(2*h2)-j[0])/sc,Math.abs((fp.ey-fm.ey)/(2*h2)-j[1])/sc,Math.abs((fq.ex-fn.ex)/(2*h2)-j[1])/sc,Math.abs((fq.ey-fn.ey)/(2*h2)-j[2])/sc); }
    ok(worst<1e-7,nm+': E = -grad V by central differences ('+worst.toExponential(2)+')'); ok(wj<1e-7,nm+': the Jacobian against differences of E ('+wj.toExponential(2)+')'); }
  { const ch=PRE('rows'), p=[0.3,0.2]; let V=0, ex=0, ey=0; for(const c of ch){ const f=fieldAt([c],p[0],p[1]); V+=f.V; ex+=f.ex; ey+=f.ey; }
    const f=fieldAt(ch,p[0],p[1]); rel(f.V,V,1e-14,'superposition: V of 14 charges = the sum of 14 singles'); rel(f.ey,ey,1e-14,'and so is Ey'); rel(f.ex,ex,1e-13,'and Ex'); }
  for(const r of [0.1,1,3.7,40]){ const ch=[{x:0.3,y:-0.2,q:-1}];
    rel(potentialAt(ch,0.3+r,-0.2)*r,-KNC,1e-15,'a point charge: r V = k q at r = '+r); const f=fieldAt(ch,0.3,-0.2+r); rel(f.ey*r*r,-KNC,1e-14,'and r^2 E = k q, pointing toward the negative charge'); eq(f.ex,0,'with no sideways part'); }
  { const f=fieldAt(PRE('single'),2,0); rel(f.ex,KNC/4,1e-15,'|E| at 2 m from +1 nC = k/4 (absolute)'); }
  /* Laplace: V_xx + V_yy + V_zz = 0 at a point in the plane, with V_zz = -k sum q/r^3 */
  { const ch=PRE('triangle'), p=[0.9,-0.4], j=jacAt(ch,p[0],p[1]); let vzz=0; for(const c of ch) vzz+=-KNC*c.q/Math.pow(Math.hypot(p[0]-c.x,p[1]-c.y),3);
    const hz=1e-4, V3=z=>{ let s=0; for(const c of ch) s+=c.q/Math.sqrt((p[0]-c.x)*(p[0]-c.x)+(p[1]-c.y)*(p[1]-c.y)+z*z); return KNC*s; };
    rel((V3(hz)-2*V3(0)+V3(-hz))/(hz*hz),vzz,1e-6,'V_zz by differences out of the plane matches -k sum q/r^3');
    close(-j[0]-j[2]+vzz,0,1e-12*Math.abs(vzz),'and V_xx + V_yy + V_zz = 0: the field is a 3-D Coulomb field held in a plane'); }

  /* ---------- 3. PhET's display grids and encodings ---------- */
  { const ch=PRE('dipole'), G=vmapGrid(ch); eq(G.nx,80,'voltage cells: 80 across'); eq(G.ny,50,'and 50 down');
    rel(G.v[0],potentialAt(ch,-3.95,-2.45),1e-15,'the first cell centre is (-3.95, -2.45)'); rel(G.v[49*80+79],potentialAt(ch,3.95,2.45),1e-15,'the last is (3.95, 2.45)');
    const A=arrowGrid(ch); eq(A.nx,16,'arrows: 16 across'); eq(A.ny,10,'and 10 down'); ok(A.a[0].x===-3.75&&A.a[0].y===-2.25,'at 0.5-m cell centres from (-3.75, -2.25)');
    rel(A.a[5*16+9].mag,Math.hypot(fieldAt(ch,0.75,0.25).ex,fieldAt(ch,0.75,0.25).ey),1e-15,'an arrow carries |E| at its centre'); }
  eq(arrowAlpha(5,false),1,'arrow opacity saturates at 5 V/m (PhET)'); eq(arrowAlpha(2,false),0.4,'2 V/m is 40 % opaque'); eq(arrowAlpha(20,false),1,'and stays 1 above');
  eq(arrowAlpha(0.01,true),1,'direction only: every arrow with a direction is opaque'); eq(arrowAlpha(0,true),0,'but a zero field draws no arrow');
  eq(vLevel(20),0.5,'the voltage colour is half saturated at 20 V'); eq(vLevel(-40),1,'and full at -40 V'); eq(vLevel(Infinity),1,'a cell on a charge saturates'); eq(vLevel(NaN),0,'NaN (coincident +q, -q) reads as zero');
  eq(vSafe(Infinity),1e6,'vSafe caps +infinity'); eq(vSafe(NaN),0,'and zeroes NaN');
  { const b1=brightness(vCellColour(4)), b2=brightness(vCellColour(20)), b3=brightness(vCellColour(40)); ok(b1<b2&&b2<b3,'cell brightness rises with |V| ('+b1+' < '+b2+' < '+b3+')');
    eq(vCellColour(0.5),null,'below half a level no cell is drawn'); ok(toRgb(vCellColour(30))[1]>toRgb(vCellColour(30))[2],'V > 0 is green'); ok(toRgb(vCellColour(-30))[2]>toRgb(vCellColour(-30))[1],'V < 0 is magenta'); }

  /* ---------- 4. equipotentials ---------- */
  for(const nm in REF.LOOP){
    const L0=REF.LOOP[nm], ch=PRE(L0.pre), tag='loop '+nm+': ';
    const F=traceEquipotential(ch,L0.seed[0],L0.seed[1],{hmax:0.002,hmin:0.0005,c:0.02}), D=traceEquipotential(ch,L0.seed[0],L0.seed[1]);
    rel(F.V0,L0.V0,1e-15,tag+'V0 at the seed (derive)');
    ok(F.closed&&D.closed,tag+'closes on itself (fine and default steps)'); ok(F.gap<0.002&&D.gap<0.05,tag+'the closing chord is shorter than a step ('+fmt(D.gap,4)+' m)');
    let w=0; for(const p of D.pts) w=Math.max(w,Math.abs(potentialAt(ch,p[0],p[1])-D.V0)); ok(w<1e-12*Math.abs(D.V0),tag+'every vertex on the level set ('+w.toExponential(2)+' V)');
    rel(Math.abs(polyArea(F.pts)),L0.A,5e-5,tag+'area at 2-mm steps vs the polar-brentq area (derive)'); rel(polyLength(F.pts,true),L0.L,2e-5,tag+'perimeter vs the polar quadrature (derive)');
    const eF=Math.abs(Math.abs(polyArea(F.pts))-L0.A), eD=Math.abs(Math.abs(polyArea(D.pts))-L0.A);
    ok(eD<2e-3*L0.A,tag+'the default-step polygon is within 0.2 % in area'); ok(eD>20*eF,tag+'and its error is the O(h^2) chord deficit: 2-mm steps cut it '+fmt(eD/eF,0)+'x');
  }
  { const F=traceEquipotential(PRE('single'),1,0,{hmax:0.002,hmin:0.0005,c:0.02}); let w=0; for(const p of F.pts) w=Math.max(w,Math.abs(Math.hypot(p[0],p[1])-1));
    ok(w<1e-14,'a single charge\'s equipotential is the circle r = 1 ('+w.toExponential(2)+')'); rel(REF.CIRCLE[0],PI,1e-15,'and the polar route returned pi (derive CHECK)'); }
  { const F=traceEquipotential(PRE('dipole'),0.9,0,{hmax:0.002,hmin:0.0005,c:0.02}); let xm=Infinity, ym=-Infinity; for(const p of F.pts){ xm=Math.min(xm,p[0]); ym=Math.max(ym,p[1]); }
    close(xm,REF.LOOP.dipole_09.xmin,2e-6,'the dipole loop crosses the axis at x = 0.1907 (derive)'); rel(REF.DIPOLE09_AXIS_LEFT,REF.LOOP.dipole_09.xmin,1e-12,'(derive: two routes agree)');
    close(ym,REF.LOOP.dipole_09.ymax,2e-6,'and its top is y = 0.3693 (derive)'); }
  { const D=traceEquipotential(PRE('dipole'),0,0.7); let mx=0, y0=Infinity, y1=-Infinity; for(const p of D.pts){ mx=Math.max(mx,Math.abs(p[0])); y0=Math.min(y0,p[1]); y1=Math.max(y1,p[1]); }
    ok(D.ok&&!D.closed,'the dipole\'s V = 0 equipotential does not close'); eq(D.exits.join(','),'box,box','it leaves the traced region at both ends'); eq(mx,0,'and is the bisector x = 0 exactly'); ok(y0<-4.4&&y1>4.4,'running the full height'); close(D.V0,0,1e-15,'at V = 0'); }
  { const T=traceEquipotential(PRE('like'),0,0); ok(!T.ok&&/E = 0/.test(T.why),'refused at the like pair\'s null: no single equipotential');
    ok(!traceEquipotential(PRE('like'),0.52,0).ok,'refused within 3 cm of a charge (PhET)'); ok(traceEquipotential(PRE('like'),0.5+0.031,0).ok,'accepted at 3.1 cm');
    ok(!traceEquipotential([],1,1).ok,'refused on an empty plane'); }
  withState({preset:'dipole'},()=>{
    ST.eqSeeds=[]; ST.vs={x:1.5,y:0.9}; ok(plotEquipotential(ST).ok&&ST.eqSeeds.length===1,'plot adds a seed at the sensor');
    ST.vs={x:0.51,y:0}; ok(!plotEquipotential(ST).ok&&ST.eqSeeds.length===1,'a refused plot adds nothing');
    ST.vs={x:1.5,y:0.9}; for(let k=0;k<MAX_EQ+3;k++){ ST.vs.x=1+0.01*k; plotEquipotential(ST); } eq(ST.eqSeeds.length,MAX_EQ,'at most '+MAX_EQ+' lines: the oldest go first');
    ST.showVS=false; ok(!plotEquipotential(ST).ok,'no plot with the sensor in its box');
    ST.eqSeeds=[{x:1.5,y:0.9}]; moveCharge(ST,0,-0.6,0); eq(ST.eqSeeds.length,0,'moving a charge clears the equipotentials (PhET)');
    ST.eqSeeds=[{x:1.5,y:0.9}]; addCharge(ST,2,2,1); eq(ST.eqSeeds.length,0,'adding one clears them'); ST.eqSeeds=[{x:1.5,y:0.9}]; removeCharge(ST,2); eq(ST.eqSeeds.length,0,'and so does removing one');
    ST.eqSeeds=[{x:1.5,y:0.9}]; applyPreset(ST,'quad'); eq(ST.eqSeeds.length,0,'and picking a preset'); eq(ST.charges.length,4,'which sets its charges');
    for(let k=0;k<MAX_CHARGES+5;k++) addCharge(ST,0,0,1); eq(ST.charges.length,MAX_CHARGES,'at most '+MAX_CHARGES+' charges'); });

  /* ---------- 5. field lines ---------- */
  REF.DIPLINE.forEach(([ad,psi0,psiE,arr])=>{
    const a=ad*DEG, ch=PRE('dipole'), x0=0.5+R_SEED*Math.cos(a), y0=R_SEED*Math.sin(a), tag='dipole line at '+ad+'°: ';
    rel(psiAxisX(ch,x0,y0),psi0,1e-13,tag+'Psi at the seed (derive)');
    const L=traceFieldLine(ch,x0,y0,1,{c:0.02}); eq(L.end,'charge',tag+'ends on a charge'); eq(L.hit,0,tag+'the negative one');
    let dp=0; for(const p of L.pts) dp=Math.max(dp,Math.abs(psiAxisX(ch,p[0],p[1])-psi0)); ok(dp<1e-9,tag+'Psi conserved along it ('+dp.toExponential(2)+')');
    const e=L.pts[L.pts.length-1]; close(Math.atan2(e[1],-(e[0]+0.5))/DEG,arr,1e-3,tag+'arrives at the same angle from the far axis (derive)');
    const Ld=traceFieldLine(ch,x0,y0,1); let dd=0; for(const p of Ld.pts) dd=Math.max(dd,Math.abs(psiAxisX(ch,p[0],p[1])-psi0)); ok(dd<1e-6,tag+'default steps hold Psi to 1e-6 ('+dd.toExponential(2)+')');
    let tg=0; for(let k=1;k<Ld.pts.length;k++){ const p=Ld.pts[k-1], q=Ld.pts[k], m=[(p[0]+q[0])/2,(p[1]+q[1])/2], f=fieldAt(ch,m[0],m[1]), d=Math.hypot(q[0]-p[0],q[1]-p[1]);
      tg=Math.max(tg,Math.abs(((q[0]-p[0])*f.ey-(q[1]-p[1])*f.ex)/(d*Math.hypot(f.ex,f.ey)))); }
    ok(tg<2e-3,tag+'every drawn segment runs along E ('+tg.toExponential(2)+' rad)'); });
  REF.LIKELINE.forEach(([ad,thF,thP,th1000])=>{
    const a=ad*DEG, ch=PRE('like'), x0=0.5+R_SEED*Math.cos(a), y0=R_SEED*Math.sin(a), tag='like-pair line at '+ad+'°: ';
    const L=traceFieldLine(ch,x0,y0,1,{c:0.02,rEsc:1000}), e=L.pts[L.pts.length-1], th=Math.atan2(e[1],e[0])/DEG;
    eq(L.end,'escape',tag+'escapes'); close(th,th1000,1e-5,tag+'direction at 1000 m (derive solve_ivp)');
    close(th,Math.acos(psiAxisX(ch,x0,y0)/2)/DEG,3e-5,tag+'= acos(Psi/2): the exact asymptote from the seed\'s flux (to (a/r)^2)'); close(thP,Math.acos(psiAxisX(ch,x0,y0)/2)/DEG,1e-9,tag+'(derive agrees)');
    close(Math.acos((1+Math.cos(a))/2)/DEG,thF,1e-12,tag+'the charge-surface formula cos th = (1 + cos a)/2 (derive)'); ok(Math.abs(th-thF)<0.01,tag+'the 2-cm seed moves it by O(r_s^2) only'); });
  { const ch=PRE('single'); let w=0; for(let k=0;k<16;k++){ const a=(k+0.5)*TAU/16, L=traceFieldLine(ch,R_SEED*Math.cos(a),R_SEED*Math.sin(a),1);
      for(const p of L.pts) w=Math.max(w,Math.abs(wrapPi(Math.atan2(p[1],p[0])-a))); }
    ok(w<1e-12,'a single charge\'s lines are radial ('+w.toExponential(2)+' rad)'); }
  const LINECOUNT={single:[16,0,16,0],dipole:[16,16,0,0],like:[32,0,32,0],quad:[32,32,0,0],triangle:[48,0,46,2],rows:[112,112,0,0]};
  for(const nm of ORD){ const ch=PRE(nm), F=fieldLines(ch,16), w=LINECOUNT[nm], tag=nm+' lines: ';
    eq(F.lines.length,w[0],tag+'16 per charge of the majority sign'); eq(F.ends,w[1],tag+'ending on charges'); eq(F.escapes,w[2],tag+'escaping'); eq(F.nulls,w[3],tag+'ending at a null'); eq(F.stalls,0,tag+'none run out of steps');
    let bad=0; for(const L of F.lines){ const s=ch[L.from]; if(Math.abs(Math.hypot(L.pts[0][0]-s.x,L.pts[0][1]-s.y)-R_SEED)>1e-12) bad++; if(L.end==='charge'&&Math.sign(ch[L.hit].q)!==-F.sgn) bad++; }
    eq(bad,0,tag+'every line starts on a seeded charge and any that ends on a charge ends on one of the other sign'); }
  ok(fieldLines(PRE('rows'),16).lines.every(L=>L.end==='charge'),'a NEUTRAL plane: every line that starts on a charge ends on one (the two rows, 112 of 112)');
  { const F=fieldLines(PRE('dipole'),16); eq(F.sgn,1,'a neutral plane is traced from its positive charges, along E'); ok(F.lines.every(L=>PRE('dipole')[L.from].q>0),'every line starts on the + charge'); }
  /* the step heuristic, pinned: a point charge's Jacobian has Frobenius norm sqrt(5) k q/r^3 whatever the
     direction (the trace of J^2 is invariant), so the length scale is exactly r/sqrt(5) */
  for(const [x,y] of [[1,0],[0.8,0.6],[-0.3,1.2]]) rel(lengthScale([{x:0,y:0,q:1}],x,y),Math.hypot(x,y)/Math.sqrt(5),1e-14,'length scale r/sqrt(5) at ('+x+', '+y+')');
  { const rows=PRE('rows'), j=jacAt(rows,0,0); ok(Math.hypot(j[0],j[1],j[2])<1e-12*KNC,'between the rows grad E vanishes at the centre (the field is uniform to first order)');
    eq(lengthScale(rows,0,0),1,'so there the other bound binds: the 1-m distance to the nearest charge'); rel(lengthScale(rows,0.2,0.3),Math.hypot(0.2-0,0.3-1),1e-15,'and at (0.2, 0.3) too'); }
  /* the evenly spaced family: every level from -40 to 40 V, and marching squares on the level to under a centimetre */
  { const ch=PRE('dipole'), fam=equipotentialFamily(ch,4), lv=fam.map(f=>f.V).sort((a,b)=>a-b);
    eq(lv.length,21,'equipotentials every 4 V: 21 levels, -40 ... 40'); eq(lv[0],-40,'from -40 V'); eq(lv[20],40,'to +40 V'); ok(lv.indexOf(0)>=0,'with V = 0');
    let worst=0, n=0; for(const f of fam) for(let k=0;k<f.segs.length;k+=2){ const x=f.segs[k], y=f.segs[k+1]; if(nearestCharge(ch,x,y).r<0.4) continue;
      const g=fieldAt(ch,x,y); worst=Math.max(worst,Math.abs(g.V-f.V)/Math.hypot(g.ex,g.ey)); n++; }
    ok(n>500&&worst<0.005,'contour points more than 40 cm from a charge lie within '+fmt(worst*1000,2)+' mm of their level ('+n+' points)');
    eq(equipotentialFamily(ch,10).length,9,'every 10 V: -40 ... 40 is 9 levels'); }
  { const F=fieldLines(PRE('triangle'),16), N=F.lines.filter(L=>L.end==='null'); ok(N.length===2&&N.every(L=>Math.hypot(L.pts[L.pts.length-1][0],L.pts[L.pts.length-1][1])<1e-3),
    'the triangle\'s two captured lines end at the centre, the in-plane minimum'); }
  { const ch=[{x:-0.5,y:0,q:1},{x:0.5,y:0,q:-1},{x:0,y:1.5,q:-1}], F=fieldLines(ch,8);
    eq(F.sgn,-1,'a net negative plane is traced from its negative charges, against E'); eq(F.lines.length,16,'8 from each of the two');
    ok(F.lines.every(L=>L.end!=='charge'||ch[L.hit].q>0),'and the lines that end on a charge end on the positive one'); ok(F.ends>0&&F.escapes>0,'some end on it, some come in from infinity'); }
  eq(fieldLines([],16).lines.length,0,'no charges, no lines');

  /* ---------- 6. null points ---------- */
  for(const nm of ORD){ const N=findNulls(PRE(nm)); eq(N.length,REF.NULLCOUNT[nm],nm+': '+REF.NULLCOUNT[nm]+' null points on the plane (derive fsolve)');
    (REF.NULL[nm]||[]).forEach(r=>{ const m=N.find(n=>Math.hypot(n.x-r[0],n.y-r[1])<1e-6); ok(!!m,nm+' null at ('+fmt(r[0],5)+', '+fmt(r[1],5)+') found (derive)');
      if(m){ close(m.x,r[0],1e-9,nm+' null x (derive)'); close(m.y,r[1],1e-9,nm+' null y (derive)'); rel(m.V,r[2],1e-10,nm+' V there (derive)'); eq(m.kind,r[3],nm+' its kind (derive)');
        close(m.lap,r[4],1e-8*Math.max(1,Math.abs(r[4])),nm+' in-plane Laplacian (derive)'); } }); }
  { const N=findNulls(PRE('triangle')), s=N.filter(n=>n.kind==='saddle');
    ok(s.every(n=>Math.abs(Math.hypot(n.x,n.y)+REF.TRI_SADDLE_Y)<1e-9),'the triangle\'s saddles sit 0.21354 m from the centre (derive brentq on E_y)');
    const m=N.find(n=>n.kind==='min'); ok(!!m&&m.lap>0,'its centre is an in-plane minimum of V');
    const j=jacAt(PRE('triangle'),0,0); let vzz=0; for(const c of PRE('triangle')) vzz+=-KNC*c.q/Math.pow(Math.hypot(c.x,c.y),3);
    ok(vzz<0&&Math.abs(-j[0]-j[2]+vzz)<1e-10,'and a maximum along z (V_zz = '+fmt(vzz,2)+'): Earnshaw holds in 3-D'); }
  rel(findNulls(PRE('like'))[0].V,REF.LIKE_SADDLE_V,1e-14,'the like pair\'s saddle is at V = 4k (derive)'); rel(REF.LIKE_SADDLE_V,4*KNC,1e-15,'4k, absolute');
  eq(findNulls([{x:0,y:0,q:1}]).length,0,'one charge has no null');

  /* ---------- 7. multipoles and the far field ---------- */
  for(const nm of ORD){ const M=moments(PRE(nm)), r=REF.MOM[nm], tag=nm+' moments: ';
    close(M.c[0],r[0],1e-15,tag+'centre x (derive)'); close(M.c[1],r[1],1e-15,tag+'centre y (derive)'); eq(M.Q,r[2],tag+'Q (derive)');
    close(M.p[0],r[3],1e-14,tag+'p_x (derive)'); close(M.p[1],r[4],1e-14,tag+'p_y (derive)'); close(M.Qxx,r[5],1e-14,tag+'Q_xx (derive)'); close(M.Qxy,r[6],1e-14,tag+'Q_xy (derive)'); close(M.Qyy,r[7],1e-14,tag+'Q_yy (derive)');
    for(const td in REF.SER[nm]){ const th=(+td)*DEG, cs=seriesCoeffs(PRE(nm),th,4), tc=tensorCoeffs(M,th), want=REF.SER[nm][td];
      for(let l=0;l<5;l++) close(cs[l],want[l],1e-12*Math.max(1,Math.abs(want[l])),nm+' c'+l+' at '+td+'° (derive Legendre)');
      for(let l=0;l<3;l++) close(cs[l],tc[l],1e-12*Math.max(1,Math.abs(tc[l])),nm+' c'+l+' at '+td+'°: Legendre route = tensor route'); } }
  { const p=legendreP(3,0.3); close(p[2],(3*0.09-1)/2,1e-16,'P2(0.3) = (3x^2 - 1)/2'); close(p[3],(5*0.027-0.9)/2,1e-16,'P3(0.3) = (5x^3 - 3x)/2'); }
  /* every charged preset has sum(q y) = 0 (and single, like, triangle sum(q x) = 0), so a
     wrongly computed centre of charge still came out 0 for all of them and a mutant that
     dropped the division survived the first sweep: an asymmetric set with Q = 2 */
  { const A=[{x:0.3,y:0.8,q:1},{x:-0.4,y:-0.2,q:1},{x:1.1,y:-0.6,q:1},{x:-0.9,y:0.5,q:-1}], M=moments(A), r=REF.ASYM_MOM;
    close(M.c[0],r[0],1e-15,'asymmetric Q = 2: centre of charge x (derive)'); close(M.c[1],r[1],1e-15,'y (derive)'); eq(M.Q,r[2],'Q = 2 (derive)');
    ok(Math.hypot(M.p[0],M.p[1])<1e-14,'about the centre of charge the dipole moment vanishes (its defining property)');
    close(M.Qxx,r[5],1e-14,'Q_xx (derive)'); close(M.Qxy,r[6],1e-14,'Q_xy (derive)'); close(M.Qyy,r[7],1e-14,'Q_yy (derive)');
    const cs=seriesCoeffs(A,30*DEG,4); for(let l=0;l<5;l++) close(cs[l],REF.ASYM_SER30[l],1e-12*Math.max(1,Math.abs(REF.ASYM_SER30[l])),'asymmetric set: c'+l+' at 30° (derive)'); }
  for(const nm in REF.SERIES_CONV){ const R=REF.SERIES_CONV[nm], ch=PRE(nm), M=moments(ch), th=137*DEG, cs=seriesCoeffs(ch,th,60);
    close(M.dmax,R.dmax,1e-15,nm+': farthest charge (derive)'); let s=0; for(let l=0;l<=60;l++) s+=cs[l]/Math.pow(R.r,l+1);
    rel(s,R.exact,1e-12,nm+': the 61-term series at 2 d_max sums to the exact V (derive)'); rel(potentialAt(ch,M.c[0]+R.r*Math.cos(th),M.c[1]+R.r*Math.sin(th)),R.exact,1e-14,nm+': exact V there (derive)'); }
  for(const nm in REF.FAR){ const R=REF.FAR[nm], F=farField(PRE(nm),R.th), tag=nm+' far field at '+R.th+'°: ';
    eq(F.l0,R.l0,tag+'leading order '+ORDER_NAME[R.l0]); eq(F.m,2,tag+'the next order is two down'); rel(F.cs[F.l0],R.limit,1e-12,tag+'c_l0 (derive)');
    rel(F.lim,R.rich,1e-12,tag+'r^(l+1) V taken to its limit by Richardson (derive)'); rel(F.lim,R.limit,nm==='triangle'?5e-7:nm==='rows'?1e-7:1e-8,tag+'= the exact coefficient: the limit taken numerically');
    rel(F.rate,R.rate,1e-7,tag+'approach rate (f(50) - c)/(f(100) - c) (derive; a ratio of 1e-4 differences, so 1e-7)'); ok(Math.abs(F.rate-4)<0.07,tag+'~4: the error falls as 1/r^2');
    const k50=F.rs.findIndex(r=>r>=50); ok(Math.abs(F.ratio[k50]-1)<3e-3&&Math.abs(F.ratio[0]-1)>Math.abs(F.ratio[k50]-1),tag+'the plotted ratio settles on 1'); }
  rel(REF.FAR.dipole.limit,REF.DIPOLE_CLOSED,1e-15,'the dipole limit is k p cos(theta) in closed form (derive)'); rel(REF.FAR.quad.limit,REF.QUAD_CLOSED,1e-14,'the square quadrupole\'s is 1.5 k sin(2 theta) (derive)');
  { const F=farField(PRE('dipole'),90); eq(F.l0,null,'along the dipole\'s bisector V = 0: no leading order'); eq(F.lim,null,'and no limit'); }
  { const F=farField(PRE('quad'),0); eq(F.l0,null,'the square quadrupole along x: V = 0 identically (it is odd under y -> -y)'); eq(F.cs.every(c=>Math.abs(c)<1e-12),true,'every coefficient vanishes (derive: SER quad 0)'); }
  { const F=farField(PRE('quad'),45); eq(F.l0,2,'along the diagonal the quadrupole leads'); rel(F.cs[2],1.5*KNC,1e-14,'with c2 = 1.5 k sin(90°), absolute'); }
  { const F=farField([],30); eq(F.l0,null,'no charges: nothing to expand'); }

  /* ---------- 8. the tape: int E.dl = V(A) - V(B) ---------- */
  for(const nm in REF.TAPE){ const R=REF.TAPE[nm], ch=PRE(nm), T=tapeModel(ch,{ax:R.A[0],ay:R.A[1],bx:R.B[0],by:R.B[1]}), I=lineIntegralE(ch,R.A[0],R.A[1],R.B[0],R.B[1],40);
    rel(T.L,R.L,1e-15,nm+' tape length (derive)'); rel(T.cm,100*R.L,1e-15,nm+' in centimetres'); rel(T.dV,R.dV,1e-13,nm+' V(A) - V(B) (derive)'); rel(I,R.int,1e-12,nm+' the line integral of E (derive quad)'); rel(I,T.dV,1e-12,nm+': it equals V(A) - V(B), E = -grad V'); }
  { let w14=0, w16=0; for(let k=0;k<8;k++){ w14+=GL8.w[k]*Math.pow(GL8.x[k],14); w16+=GL8.w[k]*Math.pow(GL8.x[k],16); }
    rel(w14,2/15,1e-14,'8-point Gauss-Legendre integrates x^14 exactly');
    rel(2/17-w16,Math.pow(2,17)*Math.pow(40320,4)/(17*Math.pow(20922789888000,2)),1e-9,'and misses x^16 by exactly 2^17 (8!)^4/(17 (16!)^2) = 4.65e-5: degree 15'); }

  /* ---------- 9. superposition ---------- */
  { const C=contributions(PRE('rows'),0.3,0.2);
    REF.SUP.forEach(r=>{ const c=C[r[0]]; rel(c.V,r[1],1e-14,'charge '+r[0]+' at the probe: V_i (derive)'); rel(c.ex,r[2],1e-13,'E_i x (derive)'); rel(c.ey,r[3],1e-13,'E_i y (derive)'); });
    const W=superWaterfall(C); rel(W.total,REF.SUPSUM[0],1e-14,'the waterfall ends at V (derive)'); rel(W.total,REF.SUPDIRECT[0],1e-13,'= V computed directly (derive)');
    let sx=0, sy=0; for(const c of C){ sx+=c.ex; sy+=c.ey; } rel(sx,REF.SUPDIRECT[1],1e-12,'the chain of E_i closes on E_x (derive)'); rel(sy,REF.SUPDIRECT[2],1e-13,'and E_y (derive)');
    const P=sensorReading(PRE('rows'),0.3,0.2), sc=superScale(C,P); let mx=0, ax=0, ay=0; for(const c of C){ ax+=c.ex; ay+=c.ey; mx=Math.max(mx,Math.hypot(ax,ay)*sc); }
    ok(mx<=1.4+1e-12&&Math.hypot(P.ex,P.ey)*sc<=1.4+1e-12,'one arrow scale: the chain\'s farthest point is at most 1.4 m out'); }
  eq(superScale(contributions(PRE('single'),0,0),sensorReading(PRE('single'),0,0)),null,'a probe on a charge has no finite scale');
  /* the scale follows the longest thing in the chain, which is a single TERM only where the
     terms cancel (the rows' and the dipole's chains never do, so they could not tell a
     total-only scale apart): near the like pair's midpoint the nearer charge's 55 V/m
     outruns the 31.5 V/m total */
  { const ch=PRE('like'), C=contributions(ch,0.1,0.05), P=sensorReading(ch,0.1,0.05), sc=superScale(C,P);
    const big=Math.max.apply(null,C.map(c=>Math.hypot(c.ex,c.ey)));
    ok(big>1.5*P.mag,'near the like pair\'s midpoint one term outruns the total ('+fmt(big,1)+' vs '+fmt(P.mag,1)+' V/m)');
    rel(big*sc,1.4,1e-12,'and it sets the scale: the longest arrow is exactly 1.4 m'); }
  { const ch=PRE('rows'), f=fieldAt(ch,0,0); rel(f.ey,REF.ROWS_E0[1],1e-14,'between the rows E points from + to - (derive)'); ok(Math.abs(f.ex)<1e-13,'with no sideways part at the centre');
    REF.ROWS_UNIF.forEach(([x,r])=>{ const e=fieldAt(ch,x,0); rel(Math.hypot(e.ex,e.ey)/Math.hypot(f.ex,f.ey),r,1e-13,'|E(x,0)|/|E(0,0)| at x = '+x+' (derive)'); }); }

  /* ---------- 10. the landscape ---------- */
  eq(landHeight(Infinity,40),1.25,'a positive charge\'s peak is clipped at the top, 1.25 m (absolute)'); eq(landHeight(-Infinity,40),-LAND_HZ,'a negative one\'s well at the bottom');
  eq(landHeight(20,40),LAND_HZ/2,'20 V of 40 is half height'); eq(landHeight(NaN,40),0,'NaN draws flat');
  { const G=landGrid(PRE('dipole'),40); eq(G.nx,64,'64 x 40 quads'); eq(G.v[20*65+36],Infinity,'the dipole\'s + charge sits on vertex (36, 20)');
    eq(G.z[20*65+36],LAND_HZ,'so its height is the cap'); ok(G.clipped>2&&G.clipped<200,'a few vertices are clipped ('+G.clipped+')');
    rel(G.z[10*65+50],landHeight(potentialAt(PRE('dipole'),2.25,-1.25),40),1e-15,'a vertex carries the clipped V at its point'); }
  for(const [th,ph] of [[-1.05,0.62],[0.3,1.45],[2.5,0.1],[-2.9,0.9]]){
    const b=box(40,60,900,600), C=landCamera(b,{camTheta:th,camPhi:ph,camZoom:1}); let inside=true, slack=Infinity;
    for(const x of [PLANE.x0,PLANE.x1]) for(const y of [PLANE.y0,PLANE.y1]) for(const z of [-LAND_HZ,LAND_HZ]){ const q=C.P([x,y,z]);
      if(!q){ inside=false; continue; } inside=inside&&q.x>=b.x+0.05*b.w-1e-6&&q.x<=b.x+0.95*b.w+1e-6&&q.y>=b.y+0.05*b.h-1e-6&&q.y<=b.y+0.95*b.h+1e-6;
      slack=Math.min(slack,q.x-(b.x+0.05*b.w),(b.x+0.95*b.w)-q.x,q.y-(b.y+0.05*b.h),(b.y+0.95*b.h)-q.y); }
    ok(inside,'the landscape camera at '+th+', '+ph+' puts all 8 corners of the box inside 90 % of the panel');
    ok(slack<0.05,'and fits it tightly (one corner within '+fmt(slack,3)+' px of the margin)');
    const C2=landCamera(b,{camTheta:th,camPhi:ph,camZoom:2}); rel(C2.cam.dist,C.cam.dist/2,1e-15,'zoom 2 halves the distance'); }

  /* ---------- 10b. the rounding floor: a cancelled sum reads zero ---------- */
  { const ch=PRE('dipole'), n=[Math.cos(90*DEG),Math.sin(90*DEG)], rs=farField(ch,90).rs;
    const raw=rs.map(r=>potentialAt(ch,r*n[0],r*n[1])), nz=raw.filter(v=>v!==0), worst=Math.max.apply(null,raw.map(Math.abs));
    ok(nz.length>0&&worst<1e-13,'on the far-field ray at 90° (x = r cos 90° = 6e-17 r) the plain sum leaves rounding residue at '+nz.length+' samples (up to '+worst.toExponential(2)+' V)');
    ok(rs.every(r=>potentialClean(ch,r*n[0],r*n[1])===0),'the clean sum is exactly 0 at every one: the terms cancelled below 1e-12 of their size');
    eq(potentialClean(ch,0.5,0),Infinity,'on a charge it is still infinite'); rel(potentialClean(ch,1.3,0.7),REF.VE.dipole[0][0],2e-14,'and elsewhere it is V (derive)');
    const T=traceEquipotential(ch,0,0.7); eq(T.V0c,0,'the bisector equipotential is labelled 0 V');
    const R=sensorReading(PRE('like'),0,0); eq(R.mag,0,'a sensor on the like pair\'s null reads 0 V/m'); eq(R.ang,0,'with no direction'); ok(!R.over,'and no dash');
    const F=farField(ch,90); ok(F.Vs.every(v=>v===0),'along the bisector every far-field sample is exactly 0'); eq(farRange(F),null,'so the log plot has nothing to draw, and says so');
    eq(tapeModel(PRE('dipole'),{ax:0,ay:1,bx:0,by:-2}).dV,0,'reads V(A) - V(B) = 0 exactly'); }
  { LABELS=[]; const c=makeShot(800,600), n0=c.ops.length; ok(labPad(c,800,600,100,100,'12.3 V/m','#fff',SM_FONT,'center'),'labPad places a label');
    eq(LABELS.length,1,'and registers its box'); ok(c.ops[n0].op==='fill'&&c.ops[n0+1].op==='text','the pad is drawn before the text');
    ok(!labPad(c,800,600,100,100,'12.3 V/m','#fff',SM_FONT,'center')||LABELS.length===2,'a second label at the same place shifts or drops'); LABELS=[]; }

  /* ---------- 11. sensors ---------- */
  { const R=sensorReading(PRE('single'),1e-4,0); ok(R.over,'a sensor 0.1 mm from a charge reads a dash (> 1e6 V/m, PhET)'); ok(!sensorReading(PRE('single'),0.01,0).over,'at 1 cm it reads (9e4 V/m)');
    const E0=sensorReading([],1,1); eq(E0.mag,0,'an empty plane has no field'); eq(E0.V,0,'and no potential'); }

  /* ---------- 12. the scene: pointer and wheel, headless ---------- */
  withState({},()=>{
    const shot=makeShot(1400,820), S=makeScene({getContext:()=>shot}); S.W=1400; S.H=820;
    const map=pointerMap(shot,S.W,S.H,'plane'), c1=ST.charges[1];
    ok(S.pointer('down',map.X(c1.x),map.Y(c1.y)),'pointer-down on a charge grabs it'); eq(DRAG.what,'charge','it is a charge');
    ST.eqSeeds=[{x:1.5,y:0.9}];
    ok(S.pointer('move',map.X(1.2),map.Y(0.7)),'a move drags it'); close(ST.charges[1].x,1.2,1e-12,'to x = 1.2'); close(ST.charges[1].y,0.7,1e-12,'and y = 0.7'); eq(ST.eqSeeds.length,0,'clearing the equipotentials'); eq(ST.preset,'custom','and the preset');
    S.pointer('move',map.X(9),map.Y(9)); ok(ST.charges[1].x===PLANE.x1&&ST.charges[1].y===PLANE.y1,'a charge stays on the plane'); S.pointer('up',0,0); eq(DRAG.what,null,'released');
    const n0=ST.charges.length;
    ok(S.pointer('down',map.X(-0.75),map.Y(BIN_GLYPH_Y)),'pointer-down on the +1 nC source'); eq(ST.charges.length,n0+1,'creates a charge'); eq(ST.charges[n0].q,1,'a positive one');
    S.pointer('move',map.X(-2),map.Y(1)); S.pointer('up',0,0); eq(ST.charges.length,n0+1,'dragged out, it stays'); close(ST.charges[n0].x,-2,1e-12,'where it was dropped');
    ST.eqSeeds=[{x:1.5,y:0.9}];
    S.pointer('down',map.X(0),map.Y(BIN_GLYPH_Y)); eq(ST.charges[n0+1].q,-1,'the -1 nC source makes a negative charge'); S.pointer('up',0,0);
    eq(ST.charges.length,n0+1,'dropped back unmoved, it is gone'); eq(ST.eqSeeds.length,1,'and a click on the bin clears nothing');
    S.pointer('down',map.X(-2),map.Y(1)); S.pointer('move',map.X(0),map.Y(-2)); S.pointer('up',0,0); eq(ST.charges.length,n0,'a charge dragged into the bin is removed');
    const ne=ST.esens.length; S.pointer('down',map.X(0.75),map.Y(BIN_GLYPH_Y)); eq(ST.esens.length,ne+1,'the sensor source makes an E-field sensor');
    S.pointer('move',map.X(2.5),map.Y(-1)); S.pointer('up',0,0); close(ST.esens[ne].x,2.5,1e-12,'dropped on the plane'); S.pointer('down',map.X(2.5),map.Y(-1)); S.pointer('move',map.X(0.2),map.Y(-2.1)); S.pointer('up',0,0); eq(ST.esens.length,ne,'and dragged back into the bin, removed');
    ST.eqSeeds=[]; const g=vsGeo(map,ST,S.W,S.H);
    ok(S.pointer('down',g.plot.x+3,g.plot.y+3),'the sensor\'s plot button'); eq(ST.eqSeeds.length,1,'plots an equipotential'); eq(DRAG.what,null,'without starting a drag');
    ok(S.pointer('down',g.clear.x+3,g.clear.y+3),'its clear button'); eq(ST.eqSeeds.length,0,'clears them');
    ok(S.pointer('down',g.X,g.Y)&&DRAG.what==='vs','grabbing the crosshair drags the sensor'); S.pointer('move',map.X(-1),map.Y(1.5)); S.pointer('up',0,0); close(ST.vs.x,-1,1e-9,'the sensor followed'); close(ST.vs.y,1.5,1e-9,'in y too');
    ST.showTape=true; ok(S.pointer('down',map.X(ST.tape.ax),map.Y(ST.tape.ay))&&DRAG.what==='tapeA','the tape\'s end A'); S.pointer('move',map.X(-3),map.Y(0)); S.pointer('up',0,0); ok(ST.tape.ax===-3&&ST.tape.ay===0,'moves');
    const mx=(ST.tape.ax+ST.tape.bx)/2, my=(ST.tape.ay+ST.tape.by)/2, t0=clone(ST.tape);
    ok(S.pointer('down',map.X(mx),map.Y(my))&&DRAG.what==='tape','grabbing the tape\'s middle'); S.pointer('move',map.X(mx+0.5),map.Y(my)); S.pointer('up',0,0);
    close(ST.tape.ax-t0.ax,0.5,1e-9,'moves both ends'); close(ST.tape.bx-t0.bx,0.5,1e-9,'together');
    ok(!S.pointer('down',map.X(3.5),map.Y(-2.2)),'empty plane grabs nothing');
    ST.view='super'; const ms=pointerMap(shot,S.W,S.H,'super');
    ok(S.pointer('down',ms.X(ST.probe.x),ms.Y(ST.probe.y))&&DRAG.what==='probe','the probe'); S.pointer('move',ms.X(-1),ms.Y(-1)); S.pointer('up',0,0); close(ST.probe.x,-1,1e-9,'follows the pointer');
    ST.view='lines'; const ml=pointerMap(shot,S.W,S.H,'lines'); const c0=ST.charges[0];
    ok(S.pointer('down',ml.X(c0.x),ml.Y(c0.y))&&DRAG.what==='charge','charges drag in the field-lines view'); S.pointer('up',0,0);
    { const nb=ST.charges.length; S.pointer('down',ml.X(-0.75),ml.Y(BIN_GLYPH_Y)); S.pointer('up',0,0); eq(ST.charges.length,nb,'but it has no bin to take charges from'); }
    { const nb=ST.charges.length, c=ST.charges[0]; S.pointer('down',ml.X(c.x),ml.Y(c.y)); S.pointer('move',ml.X(0),ml.Y(-2)); S.pointer('up',0,0);
      eq(ST.charges.length,nb,'nor one to drop them into: a charge left where the bin would be stays'); close(ST.charges[0].y,-2,1e-9,'where it was dropped'); }
    ST.view='land'; const th=ST.camTheta, ph=ST.camPhi;
    ok(S.pointer('down',400,300),'the landscape grabs the camera'); S.pointer('move',500,340); ok(ST.camTheta<th&&ST.camPhi>ph,'a drag turns and raises it'); S.pointer('up',0,0);
    const z=ST.camZoom; ok(S.wheel(-300)&&ST.camZoom>z,'the wheel zooms in');
    ST.view='far'; ok(!S.pointer('down',400,300),'the far-field view ignores the pointer'); ok(!S.wheel(-300),'and the wheel'); ST.view='plane'; ok(!S.wheel(-300),'the wheel only zooms the landscape');
    S.resetCam(); eq(ST.camTheta,DEFAULTS.camTheta,'reset puts the camera back');
  });

  /* ---------- 13. readouts ---------- */
  const PCONF=[{},{preset:'empty',charges:[]},{preset:'triangle',charges:PRE('triangle')},{preset:'rows',charges:PRE('rows'),showTape:true},{preset:'single',charges:PRE('single'),vs:{x:0,y:0}}];
  const panels=over=>withState(over,()=>{ const M=buildModel(); return readoutHTML(M)+eqbarHTML(M)+tagHTML(M); });
  for(const [v] of TABS) for(const over of PCONF){
    const html=panels(Object.assign({view:v},over));
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over).slice(0,40)); }
  { const h1=panels({}); ok(h1.indexOf(sigf(potentialAt(PRE('dipole'),1.5,0.9),3)+' V')>=0,'the plane readout prints the voltage sensor\'s V off the model');
    const R=sensorReading(PRE('dipole'),-1.8,1.2); ok(h1.indexOf(sigf(R.mag,3)+' V/m at '+fmt(R.ang,1))>=0,'and the E-field sensor\'s reading'); }
  ok(panels({view:'far'}).indexOf(sigf(REF.FAR.dipole.rich,6))>=0,'the far-field readout prints the Richardson limit');
  ok(panels({view:'lines',preset:'rows',charges:PRE('rows')}).indexOf('<td class="v good">112</td>')>=0,'the lines readout counts 112 lines ending on charges');

  /* ---------- 14. layout sweep: every view x configuration x size ---------- */
  const lcg=(()=>{ let s=12345; return ()=>{ s=(s*1103515245+12345)%2147483648; return s/2147483648; }; })();
  const many=[]; for(let k=0;k<MAX_CHARGES;k++) many.push({x:-3.6+7.2*lcg(),y:-1.5+3.8*lcg(),q:k%2?1:-1});
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['plane default',{}],['plane empty',{preset:'empty',charges:[],eqSeeds:[]}],
    ['plane all on',{preset:'rows',charges:PRE('rows'),showV:true,showVals:true,showGrid:true,showTape:true,eqSeeds:[{x:1.5,y:0.9},{x:2.6,y:0}],esens:[{x:-1.8,y:1.2},{x:3,y:-1.5}]}],
    ['plane dir only',{preset:'triangle',charges:PRE('triangle'),dirOnly:true,showVals:true,eqSeeds:[{x:0,y:0.05}]}],
    ['plane 40 charges',{preset:'custom',charges:many,showV:true,eqSeeds:[]}],
    ['plane sensor low',{vs:{x:3.5,y:-2.4},showVals:true,eqSeeds:[]}],['plane sensor on charge',{vs:{x:0.5,y:0},esens:[{x:-0.5,y:0}],showVals:true,eqSeeds:[]}],
    ['lines dipole',{view:'lines'}],['lines rows 32',{view:'lines',preset:'rows',charges:PRE('rows'),nLines:32}],['lines triangle',{view:'lines',preset:'triangle',charges:PRE('triangle')}],
    ['lines like no fam',{view:'lines',preset:'like',charges:PRE('like'),showFam:false}],['lines empty',{view:'lines',preset:'empty',charges:[]}],['lines 40',{view:'lines',preset:'custom',charges:many,nLines:4}],
    ['land dipole',{view:'land'}],['land rows 10 V',{view:'land',preset:'rows',charges:PRE('rows'),vcap:10}],['land triangle 100 V',{view:'land',preset:'triangle',charges:PRE('triangle'),vcap:100,camPhi:1.5}],
    ['land low zoomed',{view:'land',camPhi:0.05,camZoom:3}],['land empty',{view:'land',preset:'empty',charges:[],camZoom:0.4}],
    ['super dipole',{view:'super'}],['super rows',{view:'super',preset:'rows',charges:PRE('rows')}],['super on charge',{view:'super',probe:{x:0.5,y:0}}],
    ['super corner',{view:'super',probe:{x:3.95,y:2.45}}],['super empty',{view:'super',preset:'empty',charges:[]}],
    ['far dipole',{view:'far'}],['far bisector',{view:'far',farTheta:90}],['far quad axis',{view:'far',preset:'quad',charges:PRE('quad'),farTheta:0}],
    ['far rows',{view:'far',preset:'rows',charges:PRE('rows'),farTheta:60}],['far single',{view:'far',preset:'single',charges:PRE('single')}],['far empty',{view:'far',preset:'empty',charges:[]}],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      /* a sparse view is honest when it says why (Known-bad: an op floor punishes that) */
      ok((fills.length>=3&&texts.length>=1)||texts.some(t=>/no charges/.test(t.t)),nm+' '+W+'x'+H+' draws substance or says why ('+fills.length+' fills)');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null; const flat=texts.filter(t=>!t.rot);
      for(let i2=0;i2<flat.length&&!hit;i2++) for(let j2=i2+1;j2<flat.length;j2++){
        const a=flat[i2].bb,b=flat[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>0.5&&oy>0.5){ hit='"'+flat[i2].t.slice(0,22)+'" vs "'+flat[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    });
  }

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
