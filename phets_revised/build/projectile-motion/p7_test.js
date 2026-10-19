
/* ================================================================== *
 *  selfTest — headless verification.  Every reference labelled        *
 *  (derive), (twin) or (scipy) is R('<label>'): a line of             *
 *  build/projectile-motion/refvals.txt, the printed output of          *
 *  derive.py, pulled into REF by gen_refs.py — never retyped.          *
 * ================================================================== */
function R(label){ if(!(label in REF)) throw new Error('no reference "'+label+'"'); return REF[label]; }
/* the display-list recorder for the inline layout sweep (buoyancy.html's
   makeShot; named apart from tools/recorder.js's makeRecorder, Known-bad) */
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
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    Object.assign(ST,DEFAULTS,over); SCENE_VIEWS.forEach(scnReset); DRAG.what=null;
    try{ return fn(); } finally{ Object.assign(ST,stSave); SCENE_VIEWS.forEach(scnReset); DRAG.what=null; }
  }
  const rho0=airDensity(0), kS=dragK(5,0.8,0.47,rho0);
  const kOf=id=>{ const o=objById(id); return dragK(o.m,o.d,o.cd,rho0); };

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'ticksFor collapses an inverted range, which is why axes() sorts it');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame, in x');
    POLY_SEGS=[]; polyline(stub,bb,[0.5,0.5],[-1,2],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[1]-bb.y1)<1e-9&&Math.abs(POLY_SEGS[3]-bb.y)<1e-9,'and in y');
    POLY_SEGS=[]; }
  close(90*DEG,PI/2,1e-15,'DEG converts degrees INTO radians'); close((PI/2)*RAD,90,1e-13,'RAD converts back');
  eq(tickFmt([0,0.5,1])(0.5),'0.5','tick labels take their decimals from the spacing (0.5)'); eq(tickFmt([0,5,10])(5),'5','(5)');
  eq(tickFmt([0,0.02,0.04])(0.02),'0.02','(0.02)'); eq(tickFmt([-0.2,0,0.2])(-1e-17),'0.0','a float residue does not print as -0.0');
  eq(sigf(21.41764684391,4),'21.42','sigf rounds to four figures');

  /* ---------- 1. PhET's values ---------- */
  eq(G_EARTH,9.81,"PhET's g");
  const WANT={cannonball:[17.6,0.18,0.47],tankShell:[42,0.15,0.06],golfBall:[0.05,0.04,0.25],baseball:[0.15,0.07,0.35],
    football:[0.41,0.17,0.05],pumpkin:[5,0.37,0.6],human:[70,0.5,0.6],piano:[400,2.2,1.2],car:[2000,2,0.55]};
  eq(OBJECTS.map(o=>o.id).join(),'cannonball,tankShell,golfBall,baseball,football,pumpkin,human,piano,car',"PhET's nine projectiles, in its menu order");
  for(const o of OBJECTS){ const w=WANT[o.id]; ok(o.m===w[0]&&o.d===w[1]&&o.cd===w[2],"PhET's "+o.id+': mass, diameter, drag coefficient'); }
  ok(CUSTOM.m===100&&CUSTOM.d===1&&CUSTOM.cd===0.47&&CUSTOM.cdR.join()==='0.04,1,0.01',"PhET's custom projectile");
  ok(SCREEN_OBJ.m===5&&SCREEN_OBJ.d===0.8&&SCREEN_OBJ.cd===0.47&&SCREEN_OBJ.mR.join()==='1,10,1'&&SCREEN_OBJ.dR.join()==='0.1,1,0.1',"the Vectors and Drag screens' sphere and its ranges");
  ok(objById('cannonball').mR.join()==='1,31,0.01'&&objById('piano').mR.join()==='50,1000,1'&&objById('car').dR.join()==='0.5,3,0.1'
     &&objById('human').dR.join()==='0.1,1.5,0.1'&&CUSTOM.mR.join()==='1,5000,0.01',"PhET's Lab ranges per projectile");
  { let threw=false; try{ objById('lava'); }catch(e){ threw=true; } ok(threw,'an unknown projectile throws'); }
  ok(LIM.h.join()==='0,15'&&LIM.th.join()==='-90,90'&&LIM.v0.join()==='0,30'&&LIM.alt.join()==='0,5000'&&LIM.g.join()==='5,20'&&LIM.cd.join()==='0.04,1',"PhET's slider ranges");
  ok(TARGET_X0===15&&TARGET_W===3&&DOT===0.1&&BIG_DOT_EVERY===10&&MAX_FLYING===3&&MAX_TRAJ===5&&SLOW===0.33&&ZOOM.join()==='0.25,2',"PhET's target, dots, limits, slow motion and zoom");
  ok(DEFAULTS.i_obj==='pumpkin'&&DEFAULTS.i_h===10&&DEFAULTS.i_th===0&&DEFAULTS.i_v0===15&&!DEFAULTS.i_air,"PhET's Intro defaults");
  ok(DEFAULTS.l_obj==='cannonball'&&!DEFAULTS.l_air&&DEFAULTS.l_h===0&&DEFAULTS.l_th===80&&DEFAULTS.l_v0===18&&DEFAULTS.l_g===9.81,"PhET's Lab defaults");
  ok(DEFAULTS.v_air&&DEFAULTS.v_m===5&&DEFAULTS.v_d===0.8&&DEFAULTS.d_cd===0.47&&DEFAULTS.d_alt===0&&DEFAULTS.v_th===80&&DEFAULTS.d_v0===18,"PhET's Vectors and Drag defaults");

  /* ---------- 2. the air and the drag constants ---------- */
  for(const a of [0,100,1000,2500,5000]) rel(airDensity(a),R('rho_nasa('+a+' m)'),1e-12,'NASA Glenn air density at '+a+' m (derive)');
  for(const a of [0,1000,5000]) rel(isaDensity(a),R('rho_isa('+a+' m)'),1e-12,'ISA density at '+a+' m (derive)');
  rel(airDensity(0)/isaDensity(0)-1,R('nasa/isa - 1 at 0 m'),1e-8,'the fit sits 0.13 % above the ISA at sea level (derive)');
  rel(airDensity(5000)/isaDensity(5000)-1,R('nasa/isa - 1 at 5000 m'),1e-8,'and 0.21 % above it at 5 km (derive)');
  { let mono=true; for(let a=0;a<5000;a+=100) if(!(airDensity(a+100)<airDensity(a))) mono=false; ok(mono,'the density falls at every 100-m step'); }
  for(const o of OBJECTS.concat([CUSTOM])){ const k=dragK(o.m,o.d,o.cd,rho0);
    rel(k,R('k['+o.id+'] (1/m)'),1e-12,'k = rho C_d A/2m for '+o.id+' (derive)');
    rel(terminalSpeed(G_EARTH,k),R('v_t['+o.id+'] = sqrt(2mg/(rho Cd A)) (m/s)'),1e-12,'terminal speed of '+o.id+' (derive)');
    rel(terminalSpeed(G_EARTH,k),Math.sqrt(2*o.m*G_EARTH/(rho0*o.cd*PI*o.d*o.d/4)),1e-13,'sqrt(g/k) = sqrt(2mg/(rho C_d A)) for '+o.id); }
  rel(kS,R('k[screen] (1/m)'),1e-12,'the sphere: k (derive)');
  rel(terminalSpeed(G_EARTH,dragK(5,0.8,0.47,airDensity(5000))),R('v_t[screen] at 5000 m'),1e-12,'the sphere at 5 km: v_t (derive)');
  eq(terminalSpeed(9.81,0),Infinity,'no terminal speed in vacuum');

  /* ---------- 3. vacuum: closed forms, and the integrator reproduces them ---------- */
  const VAC=[[10,0,15,9.81],[0,45,30,9.81],[15,80,30,20],[0,80,18,9.81],[5,-30,20,5],[15,90,12,9.81],[7,-90,4,9.81],
             [0,30,0,9.81],[12,0,0,9.81],[0,-20,10,9.81],[15,38.5,25,9.81]];
  for(const c of VAC){ const V=vacuum(c[0],c[1],c[2],c[3]), tag='vac h='+c[0]+' th='+c[1]+' v0='+c[2]+' g='+c[3];
    for(const [key,val] of [['T',V.T],['R',V.R],['H',V.H],['vL',V.vL]]){ const r=R(tag+' '+key);
      if(Math.abs(r)<1e-9) close(val,r,1e-12,tag+' '+key+' (derive)'); else rel(val,r,1e-12,tag+' '+key+' (derive)'); }
    const ta=R(tag+' ta');
    if(ta===null) ok(V.apex===null,tag+': no apex (launched level or down)');
    else { rel(V.apex.t,ta,1e-12,tag+' apex time (derive)'); const xa=R(tag+' xa'); if(Math.abs(xa)<1e-9) close(V.apex.x,xa,1e-12,tag+' apex x (derive)'); else rel(V.apex.x,xa,1e-12,tag+' apex x (derive)'); }
    if(V.vL>0) rel(V.angL,R(tag+' angL'),1e-12,tag+' landing angle (derive)'); else ok(isNaN(V.angL),tag+': no landing angle at rest');
    rel(V.vL,Math.sqrt(c[2]*c[2]+2*c[3]*c[0]),1e-13,tag+': landing speed = sqrt(v0^2 + 2gh), energy');
  }
  for(const [h0,v0,g] of [[0,18,9.81],[10,15,9.81],[15,30,5]]){ const O=vacuumOptimum(h0,v0,g), tag='h='+h0+' v0='+v0+' g='+g;
    rel(O.th,R('vac optimum angle (deg) '+tag),1e-12,'vacuum best angle, '+tag+' (derive)'); rel(O.R,R('vac max range '+tag),1e-12,'vacuum best range, '+tag+' (derive)');
    rel(vacuum(h0,O.th,v0,g).R,O.R,1e-12,'the range at the best angle is R*, '+tag);
    ok(vacuum(h0,O.th+0.5,v0,g).R<O.R&&vacuum(h0,O.th-0.5,v0,g).R<O.R,'and half a degree either side is shorter, '+tag); }
  { let worst=0, n=0;
    for(const h0 of [0,3.3,15]) for(const th of [-90,-47,-10,0,1,33,45,72,90]) for(const v0 of [0,0.7,18,30]) for(const g of [5,9.81,20]){
      const F=flight({h:h0,th,v0},{g,k:0}), V=vacuum(h0,th,v0,g); n++;
      for(const [a,b] of [[F.T,V.T],[F.R,V.R],[F.H,V.H],[F.vL,V.vL]]) worst=Math.max(worst,Math.abs(a-b)/Math.max(1,Math.abs(b))); }
    ok(worst<1e-11,'the integrator at k = 0 reproduces the vacuum closed forms over '+n+' launches (worst '+worst.toExponential(2)+')'); }
  { const F=flight({h:0,th:-20,v0:10},{g:9.81,k:0}); ok(F.T===0&&F.R===0&&F.landI===0,'fired into the ground from h = 0: it lands at once'); }
  { const F=flight({h:0,th:30,v0:0},{g:9.81,k:0}); ok(F.T===0&&isNaN(F.angL),'no speed, no height: nothing flies and there is no landing angle'); }
  /* the envelope, asserted on the fan the view DRAWS (Known-bad: assert tangency on the objects drawn) */
  for(const x of [5,10,20,28]){ rel(envelopeY(x,4,16,9.81),R('envelope x='+x+': y_env'),1e-12,'the parabola of safety at x = '+x+' (derive)');
    rel(Math.atan(16*16/(9.81*x))*RAD,R('envelope x='+x+': tangent angle (deg)'),1e-12,'the shot that touches it there (derive)'); }
  { const h0=4, v0=16, g=9.81, Ostar=vacuumOptimum(h0,v0,g).th; let above=0, far=0, near=0;
    for(let a=0;a<=90;a+=FAN_STEP){ const VP=vacuumPath(h0,a,v0,g,90); let gap=-Infinity;
      for(let i=0;i<VP.xs.length;i++){ const d=VP.ys[i]-envelopeY(VP.xs[i],h0,v0,g); gap=Math.max(gap,d); if(d>1e-9) above++; }
      if(a>=Ostar){ if(gap>-0.02*v0*v0/(2*g)) near++; else far++; } else if(!(gap<0)) far++; }
    eq(above,0,'no point of any drawn vacuum shot rises above the envelope');
    eq(far,0,'the steep shots (above the best angle) touch it, the flat ones land before they can'); ok(near>=6,'('+near+' shots touch it)'); }

  /* ---------- 4. quadratic drag: the twin (1e-12) and scipy DOP853 (1e-9) ---------- */
  const CASES=[];
  for(const o of OBJECTS) CASES.push(['intro '+o.id,10,0,15,9.81,kOf(o.id)]);
  for(const o of OBJECTS) CASES.push(['45deg '+o.id,0,45,25,9.81,kOf(o.id)]);
  CASES.push(['drag default',0,80,18,9.81,kS],['drag default 5000 m',0,80,18,9.81,dragK(5,0.8,0.47,airDensity(5000))],
    ['lab custom g=5',3,35,22,5,dragK(100,1,0.47,rho0)],['lab custom g=20',3,35,22,20,dragK(100,1,0.47,rho0)],
    ['extreme m=1 d=3 Cd=1 g=20',15,60,30,20,dragK(1,3,1,rho0)],['down -30 pumpkin',5,-30,20,9.81,kOf('pumpkin')]);
  let worstS=0;
  for(const [tag,h0,th,v0,g,k] of CASES){
    const F=flight({h:h0,th,v0},{g,k});
    for(const [key,val] of [['T',F.T],['R',F.R],['H',F.H],['vL',F.vL],['angL',F.angL],['W',F.W]]){
      rel(val,R('twin '+tag+' '+key),2e-12,'twin '+tag+' '+key);
      const sr=R('scipy '+tag+' '+key); rel(val,sr,1e-9,'scipy '+tag+' '+key); worstS=Math.max(worstS,Math.abs(val-sr)/Math.abs(sr)); }
    eq(F.steps,R('twin '+tag+' steps'),'twin '+tag+': the same number of steps');
    const ta=R('twin '+tag+' ta');
    if(ta===null) ok(F.apex===null,tag+': no apex'); else { rel(F.apex.t,ta,2e-12,'twin '+tag+' apex time'); rel(F.apex.x,R('twin '+tag+' xa'),2e-12,'twin '+tag+' apex x');
      rel(F.apex.t,R('scipy '+tag+' ta'),1e-9,'scipy '+tag+' apex time'); }
    if(F.T>0.5){ const i=F.dots[5]; close(F.t[i],0.5,1e-15,tag+': the fifth dot is at 0.5 s');
      rel(F.x[i],R('twin '+tag+' x(0.5 s)'),2e-12,'twin '+tag+' x(0.5 s)'); rel(F.y[i],R('twin '+tag+' y(0.5 s)'),2e-12,'twin '+tag+' y(0.5 s)');
      rel(F.vx[i],R('twin '+tag+' vx(0.5 s)'),2e-12,'twin '+tag+' vx(0.5 s)'); rel(F.vy[i],R('twin '+tag+' vy(0.5 s)'),2e-12,'twin '+tag+' vy(0.5 s)'); }
  }
  ok(worstS<1e-10,'the worst disagreement with scipy over '+CASES.length+' flights is '+worstS.toExponential(2)+' (derive measured 2.8e-11)');
  { let neg=0, cnt=0; for(const id of ['golfBall','pumpkin','piano']) for(const th of [-60,0,30,60,85]){ const F=flight({h:15,th,v0:30},{g:9.81,k:kOf(id)}); cnt++;
      for(const v of F.vx) if(v<0) neg++; }
    const X=flight({h:15,th:60,v0:30},{g:20,k:dragK(1,3,1,rho0)}); for(const v of X.vx) if(v<0) neg++;
    eq(neg,0,'the horizontal velocity never turns negative (PhET clamps it; the exact solution never needs to)'); }

  /* ---------- 5. the exact hodograph: an in-page route sharing no code with the integrator ---------- */
  for(let i=0;i<10;i++){ close(GL10.xs[i],R('GL10 node '+i),2e-13,'Gauss-Legendre node '+i+' by Newton = numpy leggauss'); close(GL10.ws[i],R('GL10 weight '+i),2e-13,'weight '+i); }
  for(const ph of [60,30,0,-30,-60]){ const P=hodoTXY(ph*DEG,80*DEG,18,0,9.81,kS), tg='hodo drag-default phi='+ph;
    rel(P.t,R(tg+' t'),1e-11,tg+': t by Gauss-Legendre = scipy quad'); rel(P.x,R(tg+' x'),1e-11,tg+': x'); rel(P.y,R(tg+' y'),1e-11,tg+': y');
    rel(hodoU(ph*DEG,80*DEG,18*Math.cos(80*DEG),9.81,kS),R(tg+' u'),1e-12,tg+': u(phi), closed form'); }
  const HC=[['drag default',0,80,18,9.81,kS],['45deg pumpkin',0,45,25,9.81,kOf('pumpkin')],['45deg baseball',0,45,25,9.81,kOf('baseball')],
            ['lab custom g=5',3,35,22,5,dragK(100,1,0.47,rho0)],['down -30 pumpkin',5,-30,20,9.81,kOf('pumpkin')],['intro golfBall',10,0,15,9.81,kOf('golfBall')]];
  for(const [tag,h0,th,v0,g,k] of HC){ const HL=hodoLanding({h:h0,th,v0},{g,k}), F=flight({h:h0,th,v0},{g,k});
    rel(HL.T,R('hodo '+tag+' T'),1e-10,'hodograph '+tag+': time of flight (derive quad)'); rel(HL.R,R('hodo '+tag+' R'),1e-10,'hodograph '+tag+': range (derive quad)');
    rel(HL.vL,R('hodo '+tag+' vL'),1e-10,'hodograph '+tag+': landing speed'); rel(HL.angL,R('hodo '+tag+' landing angle (deg)'),1e-10,'hodograph '+tag+': landing angle');
    rel(F.R,HL.R,1e-10,tag+': the integrator and the hodograph agree on the range'); rel(F.T,HL.T,1e-10,tag+': and on the time');
    if(th>0){ const A=hodoTXY(0,th*DEG,v0,h0,g,k); rel(F.apex.t,A.t,1e-10,tag+': apex time, two routes'); rel(F.apex.y,A.y,1e-10,tag+': apex height, two routes');
      rel(F.vx[F.apexI],hodoU(0,th*DEG,v0*Math.cos(th*DEG),g,k),1e-10,tag+': the speed at the apex is u(0)'); } }
  { const ph=-89.999*DEG, u=hodoU(ph,80*DEG,18*Math.cos(80*DEG),9.81,kS); rel(u*Math.tan(ph),-terminalSpeed(9.81,kS),1e-6,'the exact hodograph ends at (0, -v_t)'); ok(u<1e-2,'with u -> 0'); }
  eq(hodoU(0.3,0.3,7,9.81,0),7,'in vacuum u never changes (the hodograph is a vertical line)');

  /* ---------- 6. vertical launches with drag: closed forms ---------- */
  for(const [tag,m,d,cd,h0,v0,g] of [['screen obj up 18',5,0.8,0.47,0,18,9.81],['pumpkin up 30 from 15',5,0.37,0.6,15,30,9.81],['human up 20 from 5, g=5',70,0.5,0.6,5,20,5]]){
    const k=dragK(m,d,cd,rho0), F=flight({h:h0,th:90,v0},{g,k});
    rel(terminalSpeed(g,k),R('vertical '+tag+' v_t'),1e-12,'vertical '+tag+': v_t (derive)');
    rel(F.T,R('vertical '+tag+' T'),1e-10,'vertical '+tag+': T = (v_t/g)[atan(v0/v_t) + acosh(exp(gH/v_t^2))] (derive)');
    rel(F.H,R('vertical '+tag+' H'),1e-11,'vertical '+tag+': H = h + (v_t^2/2g) ln(1 + v0^2/v_t^2) (derive)');
    rel(F.vL,R('vertical '+tag+' v_land'),1e-10,'vertical '+tag+': v_land = v_t sqrt(1 - exp(-2gH/v_t^2)) (derive)');
    rel(F.apex.t,R('vertical '+tag+' t_apex'),1e-10,'vertical '+tag+': t_apex = (v_t/g) atan(v0/v_t) (derive)'); }
  { const F=flight({h:0,th:-90,v0:0},{g:9.81,k:kS},{cliff:true,tEnd:20});
    for(const [t,j] of [[0.5,5],[1,10],[2,20],[5,50],[10,100],[20,200]]){ const i=F.dots[j];
      close(F.t[i],t,1e-12,'the drop: dot '+j+' is at '+t+' s');
      rel(F.vy[i],R('drop screen obj v('+t+' s)'),1e-10,'the drop: v = -v_t tanh(g t/v_t) at '+t+' s (derive)');
      rel(-F.y[i],R('drop screen obj fall('+t+' s)'),1e-10,'the drop: (v_t^2/g) ln cosh(g t/v_t) at '+t+' s (derive)'); }
    close(Math.abs(F.vy[F.dots[200]])/terminalSpeed(9.81,kS)-1,R('twin drop (cliff) |vy(20)|/v_t - 1'),1e-12,'after 20 s the fall is within 1.1e-9 of the terminal speed (derive)');
    ok(F.landI<0,'a drop from the cliff edge is never recorded as a landing'); }

  /* ---------- 7. drag -> 0 recovers vacuum, at the first-order rate ---------- */
  for(const [h0,th,v0] of [[0,45,25],[10,0,15],[15,60,20]]){ const tag='h='+h0+' th='+th+' v0='+v0, L={h:h0,th,v0};
    const R0=vacuum(h0,th,v0,9.81).R, rk=k=>(flight(L,{g:9.81,k}).R-R0)/k, d=R('dR/dk at k=0 (perturbation quad) '+tag);
    rel(flight(L,{g:9.81,k:0}).R,R0,1e-12,'k = 0 is the vacuum range, '+tag);
    const r4=rk(1e-4), r5=rk(1e-5), r45=rk(5e-5);
    rel(r4,R('twin (R(1e-4)-R0)/1e-4 '+tag),1e-8,'(R(1e-4) - R0)/1e-4, '+tag+' (twin)'); rel(r5,R('twin (R(1e-5)-R0)/1e-5 '+tag),1e-8,'(R(1e-5) - R0)/1e-5, '+tag+' (twin)');
    const ratio=(r4-d)/(r5-d); ok(ratio>9.5&&ratio<10.5,'the departure from dR/dk shrinks tenfold per decade of k: linear approach, '+tag+' (ratio '+fmt(ratio,3)+')');
    rel(2*r45-r4,d,1e-4,'Richardson 2r(k/2) - r(k) reaches the perturbation integral dR/dk, '+tag+' (derive quad)'); }

  /* ---------- 8. invariances and the ledger ---------- */
  { const k1=dragK(2,0.4,0.47,rho0), k2=dragK(8,0.8,0.47,rho0); rel(k1,k2,1e-15,'mass enters only through k: 4x the mass and 2x the diameter give the same k');
    rel(flight({h:5,th:40,v0:25},{g:9.81,k:k1}).R,flight({h:5,th:40,v0:25},{g:9.81,k:k2}).R,1e-13,'and the same flight'); }
  { const a=withState({view:'intro',i_obj:'golfBall'},()=>predicted('intro').R), b=withState({view:'intro',i_obj:'piano'},()=>predicted('intro').R);
    eq(a,b,'without air a golf ball and a piano fly the same range, exactly');
    const c=withState({view:'intro',i_obj:'golfBall',i_air:true},()=>predicted('intro').R), d2=withState({view:'intro',i_obj:'piano',i_air:true},()=>predicted('intro').R);
    ok(Math.abs(c-d2)>0.1,'with air they part'); }
  for(const [tag,h0,th,v0,g,k] of [['drag default',0,80,18,9.81,kS],['extreme',15,60,30,20,dragK(1,3,1,rho0)],['lab custom g=5',3,35,22,5,dragK(100,1,0.47,rho0)]]){
    const Lr=ledgerResidual(flight({h:h0,th,v0},{g,k}));
    ok(Lr.worst<1e-9*Lr.e0,'the energy ledger v^2/2 + g y + w holds to '+Lr.worst.toExponential(2)+' J/kg of '+fmt(Lr.e0,1)+', '+tag); }
  { const r0=flight({h:0,th:80,v0:18},{g:9.81,k:kS}).R, r1=flight({h:0,th:80,v0:18},{g:9.81,k:dragK(5,0.8,0.47,airDensity(2500))}).R, r2=flight({h:0,th:80,v0:18},{g:9.81,k:dragK(5,0.8,0.47,airDensity(5000))}).R;
    ok(r0<r1&&r1<r2,'thinner air at altitude, longer range ('+fmt(r0,3)+' < '+fmt(r1,3)+' < '+fmt(r2,3)+' m)'); }
  { const a=vacuum(0,45,20,5).R, b=vacuum(0,45,20,10).R; rel(a,2*b,1e-14,'in vacuum from the ground the range scales as 1/g'); }

  /* ---------- 9. the best angle with drag: golden section against scipy ---------- */
  for(const [tag,h0,v0,g,k] of [['baseball v0=30',0,30,9.81,kOf('baseball')],['golfBall v0=30',0,30,9.81,kOf('golfBall')],
      ['drag default v0=18',0,18,9.81,kS],['pumpkin from 10 v0=15',10,15,9.81,kOf('pumpkin')]]){
    const O=optimumAngle({h:h0,v0},{g,k});
    close(O.th,R('optimum '+tag+' angle (deg)'),2e-3,'best angle with drag, '+tag+' (scipy minimize_scalar)');
    rel(O.R,R('optimum '+tag+' range'),1e-10,'best range with drag, '+tag+' (scipy)');
    rel(rangeAt({h:h0,v0},{g,k},R('optimum '+tag+' angle (deg)')),R('twin range at that angle '+tag),1e-11,'the range at scipy\'s angle, '+tag+' (twin)');
    ok(O.th<vacuumOptimum(h0,v0,g).th,'the air pulls the best angle below the vacuum one, '+tag); }
  { const O=optimumAngle({h:10,v0:15},{g:9.81,k:1e-12}), V=vacuumOptimum(10,15,9.81); close(O.th,V.th,1e-4,'the golden section at k -> 0 finds tan th* = v0/sqrt(v0^2 + 2gh)');
    const O0=optimumAngle({h:10,v0:15},{g:9.81,k:0}); ok(O0.th===V.th&&O0.R===V.R,'and at k = 0 it IS the closed form'); }

  /* ---------- 10. a change of air in mid-flight ---------- */
  { const F=flight({h:0,th:80,v0:18},{g:9.81,k:kS}), i=F.dots[8];
    rel(F.t[i],R('node t'),1e-15,'the 0.8-s node'); rel(F.x[i],R('node x'),2e-12,'node x (twin)'); rel(F.y[i],R('node y'),2e-12,'node y (twin)');
    rel(F.vx[i],R('node vx'),2e-12,'node vx (twin)'); rel(F.vy[i],R('node vy'),2e-12,'node vy (twin)');
    const G=continueFlight(F,0.8,{g:9.81,k:0});
    rel(G.T,R('closed form from the node'),1e-12,'air off at 0.8 s: it lands when the vacuum parabola from the node says (derive)');
    rel(G.R,R('closed form range'),1e-12,'and where (derive)'); rel(G.T,R('continuation (vacuum) landing time'),1e-12,'(twin)');
    let same=true; for(let j=0;j<=i;j++) if(G.t[j]!==F.t[j]||G.x[j]!==F.x[j]) same=false; ok(same,'the path up to the node is kept');
    ok(G.apex&&G.apex.t>0.8,'the new apex is after the node');
    ok(G.dots.length===Math.floor(G.T/DOT+1e-9)+1&&G.dots.every((d,j)=>Math.abs(G.t[d]-j*DOT)<1e-12),'and a dot every 0.1 s from launch to the new landing');
    const G5=continueFlight(F,0.8,{g:5,k:kS}); rel(G5.T,R('continuation (gravity 5) landing time'),1e-11,'gravity 5 at 0.8 s: landing time (twin)'); rel(G5.R,R('continuation (gravity 5) range'),1e-11,'and range (twin)'); }
  withState({view:'vectors'},()=>{
    ok(fire('vectors'),'fire on the vectors view'); SCN.vectors.t=0.8; ST.v_air=false;
    eq(retarget('vectors'),1,'switching the air off re-routes the one projectile in flight');
    const tr=SCN.vectors.trajs[0]; ok(tr.changed,'its path is marked changed'); rel(tr.F.T,R('closed form from the node'),1e-12,'and it now lands on the vacuum parabola from the 0.8-s node (derive)');
    advance('vectors',3); eq(flyingCount('vectors'),0,'and lands'); rel(SCN.vectors.score.x,R('closed form range'),1e-12,'at the range the closed form gives'); });
  withState({view:'vectors'},()=>{
    fire('vectors'); SCN.vectors.t=0.3; ok(fire('vectors'),'a second, identical shot 0.3 s later'); eq(SCN.vectors.trajs.length,1,'joins the same path (PhET)');
    SCN.vectors.t=0.8; ST.v_air=false; eq(retarget('vectors'),2,'the air goes: both projectiles are re-routed');
    eq(SCN.vectors.trajs.length,2,'the one behind splits onto a path of its own'); ok(SCN.vectors.trajs.every(t=>t.changed),'both paths are marked changed');
    const t0=SCN.vectors.trajs[0], t1=SCN.vectors.trajs[1];
    ok(t0.projs.length===1&&t0.projs[0].t0===0,'the furthest projectile keeps the original path (PhET)');
    rel(t0.F.T,R('closed form from the node'),1e-12,'which now bends at its 0.8-s node (derive)');
    ok(t1.projs[0].t0===0.3&&t1.F.T>t0.F.T,'the one behind flies on from its own 0.5-s node, and lands later');
    ok(fire('vectors')&&SCN.vectors.trajs.length===3,'a changed path takes no new shots: the next one starts a path'); });
  withState({view:'vectors'},()=>{
    /* the guard only matters once the conditions are RESTORED: then the new shot's key equals the changed path's */
    fire('vectors'); SCN.vectors.t=0.8; ST.v_air=false; retarget('vectors'); advance('vectors',4); eq(flyingCount('vectors'),0,'the bent shot lands');
    ST.v_air=true; eq(launchKey('vectors',ST),SCN.vectors.trajs[0].key,'air back on: the next shot\'s conditions equal the bent path\'s original ones');
    ok(fire('vectors'),'fire the identical shot'); eq(SCN.vectors.trajs.length,2,'it starts a path of its own: a path bent in mid-air never takes new shots (PhET changedInMidAir)');
    ok(!SCN.vectors.trajs[1].changed&&SCN.vectors.trajs[1].F.T===predicted('vectors').T,'the new path is the plain shot in air'); });

  /* ---------- 11. playback ---------- */
  { const F=flight({h:0,th:80,v0:18},{g:9.81,k:kS});
    for(const i of [0,100,500,F.landI]){ const S=stateAt(F,F.t[i]); ok(S.x===F.x[i]&&S.y===F.y[i],'playback at node '+i+' is the node'); }
    let worst=0; for(const i of [10,300,900,1400]){ const tm=0.5*(F.t[i]+F.t[i+1]), S=stateAt(F,tm);
      const P=rk4s([F.x[i],F.y[i],F.vx[i],F.vy[i],F.w[i]],tm-F.t[i],9.81,kS); worst=Math.max(worst,Math.abs(S.x-P[0]),Math.abs(S.y-P[1])); }
    ok(worst<1e-9,'Hermite playback between nodes matches a fresh RK4 step to '+worst.toExponential(2)+' m');
    const E=stateAt(F,F.T+1); ok(E.x===F.R&&E.y===0,'after landing, playback holds the landing point'); }

  /* ---------- 12. the scene: fire, land, score, limits, probe, tape ---------- */
  withState({view:'intro'},()=>{
    const v='intro', sc=SCN.intro;
    ok(fire(v),'fire'); eq(sc.trajs.length,1,'one path'); eq(flyingCount(v),1,'one in the air');
    sc.t=0.2; ok(fire(v),'an identical shot'); eq(sc.trajs.length,1,'joins the same path'); eq(sc.trajs[0].projs.length,2,'two projectiles on it');
    sc.t=0.4; ok(fire(v),'a third'); ok(!fire(v),'a fourth is refused: three in the air (PhET)'); eq(flyingCount(v),3,'three in the air');
    advance(v,1.5); eq(flyingCount(v),0,'all land'); eq(sc.trajs[0].projs.length,1,'only the latest landed projectile stays on the path (PhET)');
    eq(sc.trajs[0].projs[0].t0,0.4,'and it is the last one fired');
    ok(sc.score&&sc.score.stars===0,'21.4 m against a target at 15 m: missed');
    ST.i_tgt=21.4; fire(v); advance(v,1.6); eq(sc.score.stars,3,'target moved to 21.4 m: three stars');
    ST.i_tgt=20.5; fire(v); advance(v,1.6); eq(sc.score.stars,2,'at 20.5 m (0.92 off): two'); ST.i_tgt=20.1; fire(v); advance(v,1.6); eq(sc.score.stars,1,'at 20.1 m (1.32 off): one');
    for(let a=10;a<=70;a+=10){ ST.i_th=a; fire(v); advance(v,4); }
    eq(sc.trajs.length,MAX_TRAJ,'seven different shots keep the last five paths (PhET)');
    erase(v); ok(sc.trajs.length===0&&sc.score===null,'erase clears the paths and the score'); });
  eq(starsFor(15.5,15),3,'0.5 m off: three stars (<= W/6)'); eq(starsFor(15.5000001,15),2,'just past W/6: two');
  eq(starsFor(16,15),2,'1 m off: two (<= W/3)'); eq(starsFor(16.0000001,15),1,'just past W/3: one'); eq(starsFor(13.5,15),1,'1.5 m short: one (<= W/2)'); eq(starsFor(13.4999999,15),0,'past W/2: none');
  withState({view:'intro',probe:true,tape:true},()=>{
    const v='intro', sc=SCN.intro; fire(v); sc.t=0.55;
    sc.probe={x:7.5,y:10-0.5*9.81*0.25}; let P=probeRead(v); ok(P&&P.t===0.5,'the probe on the 0.5-s dot reads t = 0.5 s');
    rel(P.x,7.5,1e-12,'range 7.5 m (vacuum: 15 m/s x 0.5 s)'); rel(P.y,10-0.5*9.81*0.25,1e-12,'height 10 - g t^2/2');
    sc.probe={x:15*0.8,y:10-0.5*9.81*0.64}; ok(probeRead(v)===null,'a dot the flight has not reached yet is not readable');
    advance(v,1.2); P=probeRead(v); ok(P&&Math.abs(P.t-0.8)<1e-12,'once the flight has passed it, it is');
    sc.probe={x:3,y:3}; ok(probeRead(v)===null,'far from the path the probe reads nothing');
    sc.probe={x:vacuum(10,0,15,9.81).R,y:0}; P=probeRead(v); ok(P&&P.land,'at the landing it reads the landing');
    close(probeRadius(),0.45,1e-15,'the probe senses 0.45 m at zoom 1'); ST.zoom=2; close(probeRadius(),0.225,1e-15,'0.225 m at zoom 2: the same 12.6 px'); ST.zoom=1;
    eq(tapeLength(v),10,'the tape starts 10 m long'); sc.tape={x0:0,y0:0,x1:3,y1:4}; eq(tapeLength(v),5,'a 3-4-5 tape reads 5 m'); });
  withState({view:'lab',l_air:true,l_obj:'custom',l_m:100,l_d:1,l_cd:0.47},()=>{ const F=predicted('lab');
    rel(F.R,flight({h:0,th:80,v0:18},{g:9.81,k:dragK(100,1,0.47,rho0)}).R,1e-15,'the lab fires what its sliders say'); fire('lab');
    SCN.lab.t=0.5; ST.l_g=20; retarget('lab'); ok(SCN.lab.trajs[0].F.T<F.T,'raising gravity mid-flight brings it down sooner'); });

  /* ---------- 13. the scene object: the clock, the pointer, the wheel ---------- */
  { const shot=makeShot(1100,712), S=makeScene({getContext:()=>shot}); S.W=1100; S.H=712;
    Object.assign(ST,DEFAULTS); SCENE_VIEWS.forEach(scnReset);
    ok(!S.step(),'nothing in the air: the frame does not repaint'); fire('intro'); ok(S.step(),'a projectile in the air: it does');
    { const ta=SCN.intro.t; S.step(); close(SCN.intro.t-ta,FRAME_DT,1e-15,'one frame is 1/60 s'); }
    { ST.speed='slow'; const ta=SCN.intro.t; S.step(); close(SCN.intro.t-ta,FRAME_DT*SLOW,1e-15,'slow motion advances x 0.33'); }
    ST.speed='normal'; ST.running=false; const t1=SCN.intro.t; ok(!S.step()&&SCN.intro.t===t1,'paused: no step'); ST.running=true;
    ST.view='env'; const t2=SCN.intro.t; ok(!S.step()&&SCN.intro.t===t2,'on an analysis view no scene clock runs');
    ok(!S.pointer('down',300,300),'the analysis views take no pointer'); const z0=ST.zoom; ok(!S.wheel(-300)&&ST.zoom===z0,'nor the wheel (the zoom is untouched)');
    Object.assign(ST,DEFAULTS); SCENE_VIEWS.forEach(scnReset);
    const M=buildModel(), G=sceneGeo(shot,S.W,S.H,M), map=G.map;
    /* aim: grab the barrel two thirds along, drag to 45 degrees above the pivot */
    const bx=G.piv[0]+0.66*(G.muz[0]-G.piv[0]), by=G.piv[1]+0.66*(G.muz[1]-G.piv[1]);
    ok(S.pointer('down',bx,by),'pointer-down on the barrel grabs it'); eq(DRAG.what,'barrel','it is the barrel');
    S.pointer('move',map.X(5),map.Y(10+5)); eq(ST.i_th,45,'dragging to (5, 15) aims at 45°');
    S.pointer('move',map.X(-3),map.Y(12)); eq(ST.i_th,90,'dragging behind the cannon stops at 90°'); ok(S.pointer('up',0,0),'release');
    ST.i_th=0; const M2=buildModel(), G2=sceneGeo(shot,S.W,S.H,M2);
    ok(S.pointer('down',G2.piv[0],(G2.piv[1]+map.Y0)/2),'pointer-down on the pedestal grabs it'); eq(DRAG.what,'height','it is the height');
    S.pointer('move',G2.piv[0],(G2.piv[1]+map.Y0)/2-2*map.s); close(ST.i_h,12,1e-12,'dragging up 2 m raises the cannon to 12 m');
    S.pointer('move',G2.piv[0],-5000); eq(ST.i_h,15,'and it stops at 15 m'); S.pointer('up',0,0);
    ok(S.pointer('down',map.X(15),map.Y0-2),'pointer-down on the target grabs it'); eq(DRAG.what,'target','it is the target');
    S.pointer('move',map.X(18),map.Y0-2); close(ST.i_tgt,18,1e-12,'the target follows to 18 m'); S.pointer('up',0,0);
    ok(!S.pointer('down',map.X(25),map.Y(15)),'a pointer-down in the empty sky grabs nothing');
    ST.tape=true; ok(S.pointer('down',map.X(10),map.Y(0)),'the tape tip'); eq(DRAG.what,'tip','is the tip');
    S.pointer('move',map.X(12),map.Y(3)); close(SCN.intro.tape.x1,12,1e-9,'the tip follows (x)'); close(SCN.intro.tape.y1,3,1e-9,'(y)'); S.pointer('up',0,0);
    ST.probe=true; ok(S.pointer('down',map.X(8),map.Y(4)),'the probe'); eq(DRAG.what,'probe','is the probe');
    S.pointer('move',map.X(9),map.Y(2)); close(SCN.intro.probe.x,9,1e-9,'the probe follows'); S.pointer('up',0,0); eq(DRAG.what,null,'released');
    ok(S.wheel(-200)&&ST.zoom>1,'the wheel zooms in on a scene'); for(let i=0;i<30;i++) S.wheel(-500); eq(ST.zoom,2,'up to PhET\'s 2'); ok(!S.wheel(-500),'and no further');
    for(let i=0;i<60;i++) S.wheel(500); eq(ST.zoom,0.25,'down to PhET\'s 0.25');
    Object.assign(ST,stSave); SCENE_VIEWS.forEach(scnReset); DRAG.what=null; }

  /* ---------- 13b. arrows are cut at the scene box, and the cut is marked ---------- */
  { const pts=[]; const stub={beginPath(){},moveTo(x,y){ pts.push([x,y]); },lineTo(x,y){ pts.push([x,y]); },closePath(){},stroke(){},fill(){},
      set strokeStyle(v){}, set fillStyle(v){}, set lineWidth(v){}, set lineCap(v){}};
    const bb=box(0,0,100,100);
    eq(arrowPx(stub,50,50,0,30,'#fff',2,bb),true,'an arrow inside the box is drawn whole, with its head');
    pts.length=0; eq(arrowPx(stub,50,90,0,40,'#fff',2,bb),'clipped','an arrow leaving the box is cut');
    ok(Math.abs(pts[1][1]-100)<1e-12&&Math.abs(pts[1][0]-50)<1e-12,'exactly at the box edge');
    ok(Math.abs(pts[2][0]-pts[3][0])>7&&pts[2][1]===pts[3][1],'and the cut is marked by a bar across it, not a head');
    eq(arrowPx(stub,150,50,10,0,'#fff',2,bb),false,'an arrow starting outside is not drawn'); }
  { const Qt=withState({view:'hodo',a_obj:'tankShell'},()=>buildModel().Hodo), Qb=withState({view:'hodo'},()=>buildModel().Hodo);
    ok(!Qt.reach&&Qb.reach,'terminal speed within reach (3 v_t/g <= 25 s): the baseball yes, the 796-m/s tank shell no');
    close(Qt.tEnd,Math.ceil((1.5*Qt.F.T+0.5)/DOT-1e-9)*DOT,1e-12,'so the tank shell flies on only to 1.5 T + 0.5 s');
    close(Qb.tEnd,Math.ceil((Qb.F.T+3*Qb.vt/9.81)/DOT-1e-9)*DOT,1e-12,'and the baseball to T + 3 v_t/g, where the speed is within 1 % of v_t');
    const Cb=Qb.C, vEnd=Math.hypot(Cb.vx[Cb.t.length-1],Cb.vy[Cb.t.length-1]); ok(vEnd/Qb.vt>0.99&&vEnd/Qb.vt<1,'(it is: '+fmt(vEnd/Qb.vt,4)+' of v_t)'); }

  /* ---------- 14. the models, the readouts ---------- */
  const PANELS=[['intro',{}],['intro',{i_air:true,probe:true,tape:true}],['vectors',{}],['drag',{d_alt:5000}],['lab',{l_obj:'custom',l_air:true}],
                ['lab',{i_v0:0,l_v0:0,l_h:0}],['env',{}],['env',{a_air:false}],['env',{a_v0:0}],['hodo',{}],['hodo',{a_air:false}],['hodo',{a_th:90}],['hodo',{a_obj:'tankShell'}]];
  for(const [v,over] of PANELS){ const html=withState(Object.assign({view:v},over),()=>{ if(isScene(v)){ fire(v); advance(v,0.3); } const M=buildModel(); return readoutHTML(M)+eqbarHTML(M)+tagHTML(M); });
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over)); }
  ok(withState({view:'intro'},()=>readoutHTML(buildModel())).indexOf('21.42 m')>=0,'the launch readout prints the pumpkin\'s 21.42 m off the model');
  ok(withState({view:'drag'},()=>readoutHTML(buildModel())).indexOf('6.686 m')>=0,'the drag readout prints the sphere\'s 6.686 m');
  rel(withState({view:'drag',d_alt:5000},()=>predicted('drag').R),R('twin drag default 5000 m R'),2e-12,'the drag view at 5 km flies the 5-km air (twin)');
  rel(withState({view:'lab',l_obj:'custom',l_m:5,l_d:0.8,l_cd:0.47,l_air:true,l_alt:5000},()=>predicted('lab').R),R('twin drag default 5000 m R'),2e-12,'and so does the lab (twin)');
  ok(withState({view:'env'},()=>readoutHTML(buildModel())).indexOf('42.59&deg;')>=0,'the envelope readout prints the baseball\'s best angle, 42.59°');
  { const Q=withState({view:'hodo'},()=>buildModel().Hodo); rel(Q.F.vL,R('twin analysis baseball 45 30 vL'),2e-12,'the hodograph view\'s landing speed (twin)');
    ok(withState({view:'hodo'},()=>readoutHTML(buildModel())).indexOf(sigf(R('twin analysis baseball 45 30 vL'),4))>=0,'and its readout prints it'); }
  { const Q=withState({view:'hodo'},()=>buildModel().Hodo); rel(Q.HL.R,Q.F.R,1e-10,'the hodograph view\'s two routes agree');
    ok(Q.led.worst<1e-9*Q.led.e0,'its ledger stays flat over the cliff flight too'); ok(Q.C.t[Q.C.t.length-1]>=Q.tEnd-1e-9,'the cliff flight runs to its end'); }
  { const Q=withState({view:'env'},()=>buildModel().Env); rel(Q.opt.th,R('optimum baseball v0=30 angle (deg)'),2e-5,'the envelope view\'s best angle (scipy)');
    rel(Q.best.R,Q.opt.R,1e-12,'and it draws the shot at that angle'); eq(Q.fan.length,13,'thirteen shots in the fan');
    rel(Q.Rs[Q.ths.indexOf(44)],flight({h:0,th:44,v0:30},{g:9.81,k:kOf('baseball')}).R,1e-15,'the R(theta) curve is made of real flights'); }

  /* ---------- 15. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const flyAt=(v,t)=>{ fire(v); advance(v,t); };
  const CONFIGS=[
    ['intro default',{view:'intro'},null,6],
    ['intro air, all vectors, in flight',{view:'intro',i_air:true,i_vt:true,i_vc:true,i_at:true,i_ac:true},v=>flyAt(v,0.6),8],
    ['intro golf ball, probe and tape',{view:'intro',i_obj:'golfBall',probe:true,tape:true},v=>{ flyAt(v,2); SCN[v].probe={x:7.5,y:8.77}; },8],
    ['intro zoomed out, five paths',{view:'intro',zoom:0.25,i_h:0,i_v0:30,i_air:true},v=>{ for(const a of [15,30,45,60,75,85]){ ST.i_th=a; flyAt(v,5); } },8],
    ['intro zoom 2, cannon at 15 m, down',{view:'intro',zoom:2,i_h:15,i_th:-45},null,5],
    ['vectors default strobe',{view:'vectors'},null,8],
    ['vectors components and force, in flight',{view:'vectors',v_mode:'components',v_frc:true},v=>flyAt(v,1.0),8],
    ['drag default',{view:'drag'},null,7],
    ['drag streamlined at 5 km',{view:'drag',d_cd:0.04,d_alt:5000},null,7],
    ['drag blunt light, vectors in flight',{view:'drag',d_cd:1,d_d:1,d_m:1,d_th:45,d_vel:true,d_frc:true},v=>flyAt(v,0.5),8],
    ['lab default',{view:'lab'},null,6],
    ['lab custom extreme',{view:'lab',l_obj:'custom',l_m:1,l_d:3,l_cd:1,l_air:true,l_g:20,l_h:15,l_th:60,l_v0:30},v=>flyAt(v,3),6],
    ['lab piano g 20 landed',{view:'lab',l_obj:'piano',l_m:400,l_d:2.2,l_cd:1.2,l_air:true,l_g:20},v=>flyAt(v,5),7],
    ['env default',{view:'env'},null,4],
    ['env air off',{view:'env',a_air:false},null,3],
    ['env from 15 m at 5 m/s',{view:'env',a_h:15,a_v0:5},null,4],
    ['env no speed',{view:'env',a_v0:0},null,1],
    ['hodo default',{view:'hodo'},null,4],
    ['hodo air off',{view:'hodo',a_air:false},null,3],
    ['hodo sphere 80',{view:'hodo',a_obj:'sphere',a_th:80,a_v0:18},null,4],
    ['hodo no cliff',{view:'hodo',o_cliff:false},null,4],
    ['hodo vertical',{view:'hodo',a_th:90},null,3],
    ['hodo tank shell',{view:'hodo',a_obj:'tankShell'},null,3],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,setup,minFills] of CONFIGS) withState(over,()=>{
    if(setup) setup(over.view);
    for(const [W,H] of SIZES){
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(fills.length>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,24)+'" vs "'+texts[j2].t.slice(0,24)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    } });

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
