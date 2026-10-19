/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/density/refvals.txt, the printed output *
 *  of derive.py — an independent Python solve of the same physics,     *
 *  with scipy.brentq on the force balance, a 4000-strip face integral  *
 *  and a 2000-point perimeter sum — read in full.                      *
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
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  const clearMemo=()=>{ MEMO.pool=MEMO.sets=MEMO.mystery=MEMO.mv=MEMO.line=null; };
  function withState(over,fn){
    const keep=Object.assign({},ST);
    Object.assign(ST,DEFAULTS,over); clearMemo();
    try{ fn(); } finally { Object.assign(ST,keep); clearMemo(); }
  }

  /* ---------- A. the scaffold ---------- */
  close(90*DEG,PI/2,1e-15,'DEG converts degrees INTO radians (90 DEG = pi/2)');
  ok((()=>{ try{ toRgb('not a colour'); return false; }catch(e){ return true; } })(),'toRgb throws rather than returning black');
  eq(mix('#000000','#ffffff',0.5),'rgb(128,128,128)','mix blends hex');
  eq(toRgb(mix('#000000','#ffffff',0.5)).join(','),'128,128,128','mix() output is a legal mix() input');
  eq(plain('&rsquo;'),'’','plain decodes a named entity');
  eq(plain('&#955;'),'λ','plain decodes a NUMERIC entity (Known-bad: wave_fronts)');
  eq(plain('<b>x</b>'),'x','plain strips tags');
  eq(sigf(0,3),'0','sigf(0)');

  /* ---------- B. the pool, PhET's bounds (derive) ---------- */
  close(POOL_H,0.41666666666666663,1e-17,'POOL_H = 0.15/0.9/0.4 (derive)');
  close(A_POOL,0.36000000000000004,1e-17,'A_POOL (derive)');
  close(V_POOL,0.14999999999999999,1e-17,'V_POOL = 150 L (derive)');
  eq(VF0,0.1,'PhET starts the pool with 100 L');
  close(SCALE_V,0.0018,1e-18,'the scale displaces 1.8 L (PhET)');
  close(poolLevel([],[],RHO_WATER,VF0),-0.1388888888888889,1e-15,'the bare level, bisected (derive)');
  close(poolLevel([],[],RHO_WATER,VF0),-POOL_H+VF0/A_POOL,1e-15,'and it equals the closed form');
  close(0.001/A_POOL,0.0027777777777777775,1e-18,'one litre is 2.78 mm of level (derive)');

  /* ---------- C. the cube ---------- */
  close(cubeSide(0.005),0.17099759466766973,1e-17,'a 5 L cube is 17.0998 cm on a side (derive)');
  for(const V of [0.001,0.005,0.01,0.216]) rel(Math.pow(cubeSide(V),3),V,1e-15,'cubeSide inverts the cube of V at '+V+' L');
  eq(cubeBelow(0.005,-0.4,0.4),0.005,'cubeBelow saturates at V EXACTLY, not at s^3');
  ok(cubeSide(0.005)*cubeSide(0.005)*cubeSide(0.005)!==0.005,'and s*s*s does NOT equal V, which is why it has to');
  eq(cubeBelow(0.005,-0.4,-0.5),0,'nothing below a surface under the block');
  close(cubeBelow(0.005,0,cubeSide(0.005)/2),0.005/2,1e-17,'half under is half the volume');

  /* ---------- D. Archimedes, closed form vs scipy ---------- */
  close(floatDraft(0.005,400,1000),0.068399037867067886,1e-17,'the wood draft, closed form (derive)');
  close(floatDraft(0.005,400,1000),0.068399037867067872,2e-17,'and scipy.brentq on the force balance (scipy)');
  close(floatDraft(0.005,400,1000)/cubeSide(0.005),0.39999999999999997,1e-15,'d/s = rho_b/rho_f (derive)');
  eq(submergedFraction(400,1000),0.4,'submerged fraction 0.4');
  eq(submergedFraction(2700,1000),1,'a denser block is completely under');
  close(riseFloating(2,1000),0.0055555555555555549,1e-17,'a floating 2 kg block raises the level 5.56 mm (derive)');
  close(riseSunk(0.005),0.013888888888888888,1e-17,'a sunk 5 L block raises it 13.9 mm (derive)');
  ok(Math.abs(riseFloating(2,1000)-riseSunk(0.005))>0.008,'and the two laws are NOT the same number');
  /* the same rise, taken from the solver rather than from the law */
  {
    const bare=poolLevel([],[],RHO_WATER,VF0);
    const f1=solvePool([{V:0.005,rho:400}],RHO_WATER);
    close(f1.yw-bare,riseFloating(2,RHO_WATER),1e-15,'the solved rise equals m/(rho_f A) for a floater');
    const s1=solvePool([{V:0.005,rho:2700}],RHO_WATER);
    close(s1.yw-bare,riseSunk(0.005),1e-15,'and V/A for a sunk block');
  }

  /* the three default configurations (derive) */
  {
    const BA={V:2/400,rho:400}, BB={V:13.5/2700,rho:2700};
    const w=solvePool([BA],RHO_WATER);
    close(w.yw,-0.13333333333333336,1e-15,'wood alone: the level (derive)');
    eq(w.blocks[0].mode,'float','wood floats');
    close(w.blocks[0].Vsub*LITERS,2,1e-13,'and displaces 2 L (derive)');
    close(w.blocks[0].yb,-0.20173237120040124,1e-15,'its bottom sits at -0.2017 m (derive)');
    close(w.blocks[0].Fb,19.6,1e-13,'upthrust 19.6 N = its weight (derive)');
    close(w.blocks[0].W,19.6,1e-13,'weight 19.6 N');
    eq(w.blocks[0].N,0,'a floating block does not touch the floor');
    const a=solvePool([BB],RHO_WATER);
    close(a.yw,-0.12499999999999997,1e-15,'aluminium alone: the level (derive)');
    eq(a.blocks[0].mode,'rest','aluminium sinks');
    close(a.blocks[0].Fb,49,1e-13,'upthrust 49 N (derive)');
    close(a.blocks[0].N,83.3,1e-12,'the floor takes 83.3 N (derive)');
    close(a.blocks[0].N,(2700-1000)*G*0.005,1e-12,'= (rho_b - rho_f) g V');
    const b=solvePool([BA,BB],RHO_WATER);
    close(b.yw,-0.11944444444444444,1e-15,'both blocks: the level (derive)');
    close(b.blocks[0].yb,-0.18784348231151232,1e-15,'the floater rides higher with the other block in (derive)');
    close(b.yw-w.yw,riseSunk(0.005),1e-15,'adding the sunk block raised it by exactly V/A');
  }

  /* ---------- E. the three awkward cases ---------- */
  {
    const r=solvePool([{V:0.005,rho:2700}],RHO_WATER).blocks[0];
    eq(r.frac,1,'denser than the fluid: the submerged fraction is EXACTLY 1');
    close(r.N,83.300000000000011,1e-12,'and N = 83.3 N (derive)');
    ok(r.N>0,'the floor pushes up, never down');
    const n=solvePool([{V:0.005,rho:1000}],RHO_WATER).blocks[0];
    eq(n.frac,1,'exactly neutral: completely submerged');
    close(n.N,0,1e-12,'and the floor takes nothing (derive)');
    close(apparentWeight(0.005,1000,1000),0,1e-13,'a spring scale reads zero on a neutral block (derive)');
    /* neutral at EVERY depth: the hand force does not change while it is under */
    const h1=solvePool([{V:0.005,rho:1000,held:-0.30}],RHO_WATER).blocks[0];
    close(h1.Vsub*LITERS,5,1e-12,'held at -0.30 m it is fully under (derive)');
    close(h1.hand,0,1e-12,'and the hand force is zero (derive)');
    const h2=solvePool([{V:0.005,rho:1000,held:-0.34}],RHO_WATER).blocks[0];
    close(h2.hand,h1.hand,1e-12,'neutral buoyancy: the same at a second depth, so no depth is preferred');
    /* the floor only pushes on a block that is ON it: a held block and a block
       out of the pool both have N = 0, whatever W - Fb happens to be */
    const hb=solvePool([{V:0.005,rho:400,held:-0.25}],RHO_WATER).blocks[0];
    eq(hb.N,0,'a HELD block is not touching the floor: N = 0');
    ok(Math.abs(hb.hand)>1,'while the hand really is carrying something ('+fmt(hb.hand,2)+' N)');
    const ob=solvePool([{V:0.005,rho:2700,inPool:false}],RHO_WATER).blocks[0];
    eq(ob.mode,'out','a block out of the pool is out');
    eq(ob.Vsub,0,'displaces nothing');
    eq(ob.N,0,'and gets no contact force from a floor it is not on');
    close(ob.W,2700*0.005*G,1e-12,'its weight is unchanged');
    const h3=solvePool([{V:0.005,rho:1000,held:-0.25}],RHO_WATER).blocks[0];
    close(h3.Vsub*LITERS,3.5361220296589657,1e-12,'part out, it displaces 3.536 L (derive)');
    close(h3.hand,14.346004109342132,1e-11,'and the hand carries 14.35 N (derive)');
    ok(h3.hand>h1.hand+1,'which is more than when it is under — the upthrust is still growing');
    /* wider than the pool's free surface */
    const wideV=0.216, sw=cubeSide(wideV);
    ok(sw*sw>=A_POOL-1e-12,'the test block really does span the pool ('+fmt(sw*sw,3)+' m2 vs '+fmt(A_POOL,3)+')');
    const wr=solvePool([{V:wideV,rho:3000}],RHO_WATER);
    close(wr.yw,0.46111111111111103,1e-14,'a body spanning the pool: the fluid stands ABOVE it (derive)');
    close(wr.yw,-POOL_H+sw+VF0/A_POOL,1e-14,'= -H + s + Vf/A, the closed form');
    eq(wr.blocks[0].frac,1,'and it is completely submerged');
    const wf=solvePool([{V:wideV,rho:400}],RHO_WATER);
    close(wf.blocks[0].yb,-0.1388888888888889,1e-14,'a spanning FLOATER rides on all of the fluid (derive)');
    close(wf.blocks[0].yb,-POOL_H+VF0/A_POOL,1e-14,'= -H + Vf/A');
    close(wf.yw,0.1011111111111111,1e-14,'with the surface at its own draft above that (derive)');
  }

  /* ---------- E2. the pool scale, and N >= 0 as a property ---------- */
  {
    /* the pool scale is part of the shared engine (buoyancy-basics puts one in
       the pool): a solid standing in the fluid displaces it like anything else */
    const obs=[{a:SCALE_W*SCALE_D,y0:-POOL_H+0.5*(POOL_H-SCALE_H),h:SCALE_H}];
    const scTop=obs[0].y0+SCALE_H;
    close(scTop,-0.17833333333333332,1e-15,'the pool scale sits at -0.1783 m at half height (derive)');
    const bare=solvePool([],RHO_WATER,[]), withSc=solvePool([],RHO_WATER,obs);
    close(withSc.yw-bare.yw,SCALE_V/A_POOL,1e-14,'the scale alone raises the level by its own 1.8 L / A');
    close(obstacleVolume(obs,scTop),SCALE_V,1e-18,'once the fluid covers it, it displaces exactly 1.8 L');
    close(obstacleVolume(obs,scTop+1),SCALE_V,1e-18,'and no more, however deep the fluid goes');
    close(obstacleVolume(obs,obs[0].y0+SCALE_H/2),SCALE_V/2,1e-18,'half covered, half of it');
    eq(obstacleVolume(obs,obs[0].y0-0.01),0,'below it, nothing');
    const so=solvePool([{V:13.5/2700,rho:2700,support:scTop}],RHO_WATER,obs);
    close(so.yw,-0.12995986441149004,1e-12,'a block on the pool scale: the level (derive)');
    close(so.blocks[0].N,118.43840164373687,1e-10,'and the scale reads 118.44 N (derive)');
    close(13.5*G,132.30000000000001,1e-12,'the same block weighed in air reads 132.3 N (derive)');
    ok(so.blocks[0].N<13.5*G,'under water it reads less, by the weight of the water it pushes aside');
    close(13.5*G-so.blocks[0].N,RHO_WATER*G*so.blocks[0].Vsub,1e-12,'exactly');
    /* N >= 0 is physics, not a clamp */
    let minN=1e9, nRest=0, nZero=0;
    for(const rho of [100,400,919,1000,1000.0001,2700,19320])
      for(const VL of [1,3,5.5,10])
        for(const Vf of [0.004,0.02,0.1,0.14]){
          const r=solvePool([{V:VL/LITERS,rho:rho}],RHO_WATER,[],Vf).blocks[0];
          if(r.mode==='rest'){ nRest++; minN=Math.min(minN,r.N); if(r.N===0) nZero++; }
        }
    ok(nRest>=40,'the sweep reaches '+nRest+' resting configurations');
    ok(minN>=0,'a resting block is never pulled DOWN by the floor: min N = '+minN.toExponential(2));
    ok(nZero>=4,'and exactly-neutral blocks reach N = 0 exactly ('+nZero+' of them)');
  }

  /* ---------- F. G is non-decreasing, so the bisection is legitimate ---------- */
  {
    const bl=[{V:2/400,rho:400},{V:13.5/2700,rho:2700}];
    let worst=0, prev=-1e18;
    for(let k=0;k<=4000;k++){
      const y=-POOL_H+k*(POOL_H+0.8)/4000, g=netFluid(y,bl,[],RHO_WATER);
      worst=Math.min(worst,g-prev); prev=g;
    }
    ok(worst>=-1e-15,'G is non-decreasing over 4001 levels (derive: True) [worst step '+worst.toExponential(2)+']');
    /* and the DISPLACED VOLUME is continuous across the float/rest switch: at
       the level where the floating draft just reaches the floor the resting
       branch gives s^2 d and the floating branch V rho_b/rho_f, and those are
       the same number.  The SLOPE of G does jump there, from A - s^2 to A,
       which is the right behaviour and is asserted too. */
    const bw={V:0.005,rho:400}, s=cubeSide(0.005), yswitch=-POOL_H+s*0.4;
    const below=blockState(bw,yswitch-1e-12,RHO_WATER), above=blockState(bw,yswitch+1e-12,RHO_WATER);
    eq(below.mode,'rest','just below the switch the block is resting');
    eq(above.mode,'float','and just above it is floating');
    /* the residual is exactly s^2 x the probe offset, which is a much stronger
       statement than "small": a discontinuity would not scale with the probe */
    close(above.Vsub-below.Vsub,s*s*1e-12,1e-16,'the displaced volume is continuous across the switch (gap = s^2 eps)');
    const below2=blockState(bw,yswitch-1e-10,RHO_WATER);
    close(above.Vsub-below2.Vsub,s*s*1e-10,1e-15,'and the gap grows exactly 100x when the probe does');
    const gp=(netFluid(yswitch+2e-7,[bw],[],RHO_WATER)-netFluid(yswitch+1e-7,[bw],[],RHO_WATER))/1e-7;
    const gm=(netFluid(yswitch-1e-7,[bw],[],RHO_WATER)-netFluid(yswitch-2e-7,[bw],[],RHO_WATER))/1e-7;
    rel(gp,A_POOL,1e-5,'above the switch G rises at A_pool (the block takes no more water)');
    rel(gm,A_POOL-s*s,1e-5,'below it at A_pool - s^2 (the block is still filling)');
  }

  /* ---------- G. the upthrust, taken from the pressure on the faces ---------- */
  {
    const st=solvePool([{V:0.005,rho:2700}],RHO_WATER), yw=st.yw, yb=st.blocks[0].yb;
    const F=cubeFaceForces(0.005,yb,yw,RHO_WATER);
    close(F.net,49.000000000000014,1e-12,'submerged: bottom minus top face = 49 N (derive)');
    rel(F.net,RHO_WATER*G*0.005,1e-15,'and that IS rho_f g V, to 1e-15 relative');
    eq(F.sideSum,0,'the two opposite side faces cancel exactly (derive: 0)');
    /* the side force pinned against an ABSOLUTE number: a 4000-strip integral
       of p over one face, which is exact because p is linear in y */
    close(F.side,59.078173683917754,1e-9,'one side face carries 59.0782 N (derive, 4000 strips)');
    close(F.side,RHO_WATER*G*(yw-yb-cubeSide(0.005)/2)*cubeSide(0.005)*cubeSide(0.005),1e-12,
          '= rho g (depth of the face centre) x face area');
    ok(F.side>F.net,'and it is BIGGER than the upthrust — it only cancels because there are two of it');
    /* partly submerged, the same statement with the wetted strip only */
    {
      const stp=solvePool([{V:0.005,rho:400}],RHO_WATER), s=cubeSide(0.005);
      const Fp=cubeFaceForces(0.005,stp.blocks[0].yb,stp.yw,RHO_WATER), dsub=stp.yw-stp.blocks[0].yb;
      close(Fp.side,RHO_WATER*G*(dsub/2)*s*dsub,1e-12,'part submerged: the side force is rho g (d/2) s d');
      close(Fp.side,RHO_WATER*G*s*dsub*dsub/2,1e-12,'which is half of what a uniform pressure would give');
    }
    const stf=solvePool([{V:0.005,rho:400}],RHO_WATER), ywf=stf.yw, ybf=stf.blocks[0].yb;
    const F2=cubeFaceForces(0.005,ybf,ywf,RHO_WATER);
    close(F2.net,19.600000000000009,1e-12,'floating: only the bottom face is wet, 19.6 N (derive)');
    rel(F2.net,RHO_WATER*G*stf.blocks[0].Vsub,1e-14,'= rho_f g V_sub');
    rel(F2.net,400*0.005*G,1e-14,'and it equals the weight, which is why it floats');
    eq(F2.pTop,0,'the top face is dry');
    /* the 2-D polygon route: per-edge closed form against a 2000-point sum */
    const poly=cubePoly(0.005,ybf,0), sub=clipBelow(poly,ywf);
    const E=edgeForces(sub,ywf,RHO_WATER), fine=finePerimeter(sub,ywf,RHO_WATER,2000);
    close(E.tot[0],0,1e-12,'the polygon integral: the horizontal parts cancel (derive: 0)');
    close(E.tot[1],114.62149533794438,1e-11,'and the vertical parts sum to 114.62 N/m (derive)');
    rel(E.tot[1],RHO_WATER*G*polyArea(sub),1e-14,'= rho g A_sub, per unit depth');
    rel(fine[1],E.tot[1],1e-6,'a 2000-point perimeter sum agrees with the closed form');
    close(fine[0],0,1e-9,'and finds no horizontal force either');
    /* the resultant acts through the centroid of the submerged area */
    const C=polyCentroid(sub);
    close(C[0],0,1e-15,'the centre of buoyancy is on the axis of a symmetric block');
  }

  /* ---------- H. PhET's data, read out of its build ---------- */
  eq(MAT.water.phet,1000,'PhET water 1000');
  eq(MAT.wood.phet,400,'PhET wood 400');
  eq(MAT.ice.phet,919,'PhET ice 919 (handbook 916.7)');
  eq(MAT.aluminum.phet,2700,'PhET aluminium 2700');
  eq(MAT.gold.phet,19320,'PhET gold 19320');
  eq(MAT.lead.phet,11342,'PhET lead 11342');
  eq(MAT.mercury.phet,13593,'PhET mercury 13593');
  eq(MAT.styrofoam.phet,150,'PhET styrofoam 150');
  eq(MAT.platinum.phet,21450,'PhET platinum 21450');
  eq(MAT.glass.phet,MAT.aluminum.phet,'PhET reuses aluminium’s 2700 for glass');
  eq(G,9.8,'PhET runs at g = 9.8, not 9.80665');
  ok(Math.abs(G-G_STD)>0.006,'and the file knows the difference');
  eq(DENSITY_TABLE.length,13,'the Density mystery table has 13 materials');
  eq(new Set(DENSITY_TABLE.map(k=>MAT[k].phet)).size,13,'all thirteen densities are distinct, so the table CAN identify');
  eq(BUOY_FLUIDS.length,6,'six Buoyancy fluids');
  eq(SIMPLE_MATS.length,6,'six Intro materials');
  eq(MATERIALS.filter(m=>m.ref===null).length,6,'six materials have no handbook row, and the file says so');
  /* the CAPTION and the INFO paragraph both state that count and name the six;
     prose is invisible to every other assertion, so it is pinned here */
  eq(MV_CAP_FULL.indexOf('six')>=0,true,'the mass-volume caption says "six"');
  for(const m of MATERIALS.filter(x=>x.ref===null))
    ok(INFO.mv.indexOf(m.name)>=0||MV_CAP_FULL.indexOf(m.name)>=0||readoutHTML(mvModel(Object.assign({},DEFAULTS,{view:'mv'})),Object.assign({},DEFAULTS,{view:'mv'})).indexOf('no row')>=0,
       m.name+' is accounted for where the six are described');
  for(const nm of ['styrofoam','concrete','PVC','glass'])
    ok(INFO.mv.indexOf(nm)>=0,'the info paragraph names '+nm+', one of PhET’s four teaching choices');
  /* the mass slider's enabled range, PhET's rule */
  close(massRangeFor(400,false)[0],0.4,1e-15,'wood: the mass slider starts at 0.4 kg (derive)');
  close(massRangeFor(400,false)[1],4,1e-15,'and stops at 4 kg (derive)');
  close(massRangeFor(2700,false)[1],27,1e-15,'aluminium reaches exactly PhET’s 27 kg ceiling (derive)');
  close(massRangeFor(150,false)[0],0.15,1e-15,'styrofoam starts at 0.15 kg (derive)');
  eq(massRangeFor(0,true)[0],0.5,'custom starts at PhET’s 0.5 kg');
  eq(massRangeFor(19320,false)[1],27,'gold would be clipped at 27 kg, which is why the Intro list stops at aluminium');

  /* ---------- H2. PhET's mass/volume coupling, in the model ---------- */
  {
    const s2=Object.assign({},DEFAULTS);
    setMat(s2,'A','aluminum'); setVol(s2,'A',5);
    close(s2.massA,13.5,1e-12,'5 L of aluminium is 13.5 kg');
    close(rhoOf(s2,'A'),2700,1e-12,'and its density is PhET’s 2700');
    setMass(s2,'A',27);
    close(s2.volAL,10,1e-12,'27 kg of aluminium is exactly 10 L (PhET’s ceiling)');
    setMass(s2,'A',2);
    close(s2.massA,2.7,1e-12,'asking for 2 kg is refused: 1 L of aluminium is 2.7 kg');
    close(s2.volAL,1,1e-12,'and the volume sits on its floor');
    setVol(s2,'A',4);
    close(s2.massA,10.8,1e-12,'4 L of aluminium is 10.8 kg — the volume drives the mass');
    setMat(s2,'A','wood');
    close(s2.volAL,4,1e-12,'switching material keeps the VOLUME');
    close(s2.massA,1.6,1e-12,'and rebuilds the mass: 4 L of wood is 1.6 kg');
    setMat(s2,'A','custom'); setVol(s2,'A',8);
    close(s2.massA,1.6,1e-12,'custom: moving the volume leaves the mass alone');
    close(rhoOf(s2,'A'),200,1e-12,'and the density follows, rho = m/V = 200');
    setMass(s2,'A',4);
    close(s2.volAL,8,1e-12,'and moving the mass leaves the volume alone');
    close(rhoOf(s2,'A'),500,1e-12,'4 kg in 8 L is 500 kg/m3');
    ok(rhoOf(s2,'A')!==8/4*LITERS,'the density is m/V, not V/m');
    setMass(s2,'A',0.1);
    close(s2.massA,MMIN_CUSTOM,1e-12,'custom has its own 0.5 kg floor (PhET)');
    /* switching to a material whose mass would leave 0.1-27 kg moves the volume */
    const s3=Object.assign({},DEFAULTS); setMat(s3,'A','custom'); setVol(s3,'A',10);
    setMat(s3,'A','aluminum');
    close(s3.volAL,10,1e-12,'10 L of aluminium still fits under 27 kg');
    const s4=Object.assign({},DEFAULTS); setVol(s4,'A',10); setMat(s4,'A','styrofoam');
    close(s4.massA,1.5,1e-12,'10 L of styrofoam is 1.5 kg');
    close(s4.volAL,10,1e-12,'and 10 L it stays');
    /* every material, every slider position, stays legal */
    let bad=0;
    for(const id of SIMPLE_MATS.concat(['custom'])) for(const V of [1,2.5,5,7.5,10]) for(const m of [0.1,1,5,13.5,27]){
      const s5=Object.assign({},DEFAULTS); setMat(s5,'A',id); setVol(s5,'A',V); setMass(s5,'A',m);
      const rng=massRangeFor(id==='custom'?0:MAT[id].phet,id==='custom');
      if(s5.volAL<VMIN_L-1e-12||s5.volAL>VMAX_L+1e-12) bad++;
      if(s5.massA<rng[0]-1e-12||s5.massA>rng[1]+1e-12) bad++;
      if(id!=='custom'&&Math.abs(s5.massA-MAT[id].phet*s5.volAL/LITERS)>1e-12) bad++;
    }
    eq(bad,0,'175 material x volume x mass settings all stay inside PhET’s ranges and keep m = rho V');
  }

  /* ---------- I. the Compare sets ---------- */
  {
    eq(DEFAULTS.sameMass,5,'the Compare screen opens at PhET’s 5 kg');
    eq(DEFAULTS.sameVolL,5,'5 L');
    eq(DEFAULTS.sameRho,500,'and 500 kg/m3');
    const m=compareBlocks(DENS_CUBES,'mass',5,0.005,500);
    eq(m.map(b=>Math.round(b.rho)).join(','),'500,1000,2000,4000','same mass 5 kg -> 500, 1000, 2000, 4000 (derive)');
    const v=compareBlocks(DENS_CUBES,'volume',5,0.005,500);
    eq(v.map(b=>Math.round(b.rho)).join(','),'1600,1200,800,400','same volume 5 L -> 1600, 1200, 800, 400 (derive)');
    const d=compareBlocks(DENS_CUBES,'density',5,0.005,500);
    eq(d.map(b=>fmt(b.rho*b.V,2)).join(','),'3.00,2.00,1.00,0.50','same density 500 -> 3, 2, 1, 0.5 kg (derive)');
    const sm=solvePool(m,RHO_WATER);
    close(sm.yw,-0.100694444444,1e-11,'same mass: the level (derive)');
    eq(sm.blocks.map(b=>b.mode).join(','),'float,rest,rest,rest','one floats; the 1000 block is exactly neutral (derive)');
    eq(sm.blocks[1].N,0,'and presses on the floor with nothing at all');
    const sv=solvePool(v,RHO_WATER);
    close(sv.yw,-0.0944444444444,1e-11,'same volume: the level (derive)');
    eq(sv.blocks.map(b=>b.mode).join(','),'rest,rest,float,float','two of four float (derive)');
    const sd=solvePool(d,RHO_WATER);
    close(sd.yw,-0.120833333333,1e-11,'same density: the level (derive)');
    eq(sd.blocks.map(b=>fmt(b.frac,4)).join(','),'0.5000,0.5000,0.5000,0.5000','every one floats to the same fraction, whatever its size (derive)');
  }

  /* ---------- J. the mystery: identification, and the floating trap ---------- */
  {
    /* PhET's three sets, pinned block by block (derive) — the identification
       alone does not pin them, because a block can be moved a per cent and
       still name the same material */
    const PINS={
      'set 1':[['A',19.305,5.5,3510],['B',0.4,1,400],['C',19.32,1,19320],['D',5,5,1000],['E',2.8,7,400]],
      'set 2':[['A',18,1.5873015873015872,11340],['B',10.8,4,2700],['C',2.7,1,2700],
               ['D',18,4,4500],['E',44.8,5,8960]],
      'set 3':[['A',2.85,3,950],['B',6,6,1000],['C',23.4,3,7800],['D',2,5,400],
               ['E',6,6.315789473684211,950]],
    };
    for(const sn in PINS){
      const rows=mysterySet(sn,1);
      for(const [tag,m,VL,rho] of PINS[sn]){
        const r=rows.find(z=>z.tag===tag);
        ok(!!r,sn+' has a block '+tag);
        if(!r) continue;
        rel(r.m,m,1e-14,sn+' '+tag+': mass '+m+' kg (derive)');
        rel(r.V*LITERS,VL,1e-14,sn+' '+tag+': volume '+fmt(VL,4)+' L (derive)');
        rel(r.rho,rho,1e-15,sn+' '+tag+': density '+rho+' (PhET)');
      }
    }
    let worstErr=0, worstGap=1e9, nSet=0;
    for(const sn of ['set 1','set 2','set 3']){
      withState({view:'mystery',mset:sn,submerge:true},()=>{
        const M=buildModel(ST); nSet++;
        eq(M.rows.length,5,sn+' has five blocks');
        eq(M.nWrong,0,sn+': every block is identified from the printed numbers');
        worstErr=Math.max(worstErr,M.worstErr); worstGap=Math.min(worstGap,M.worstGap);
      });
    }
    eq(nSet,3,'all three fixed sets were checked');
    rel(worstErr,0.00169711,2e-4,'worst reading error over the fifteen blocks: 0.17 % (derive)');
    rel(worstGap,0.0330436,2e-4,'smallest gap to the runner-up: 3.30 % (derive)');
    ok(worstGap>10*worstErr,'the margin is an order of magnitude wider than the error, so the naming is safe');
    /* PhET's set 2 A is 11340 where the table's lead is 11342 — a real 0.018 % mismatch */
    withState({view:'mystery',mset:'set 2',submerge:true,reveal:true},()=>{
      const r=buildModel(ST).rows.find(z=>z.tag==='A');
      eq(r.truth,'lead','set 2 A is lead');
      rel(r.rho,11340,1e-15,'PhET builds it at 11340, not the table’s 11342');
      ok(Math.abs(r.rho-MAT.lead.phet)/MAT.lead.phet<3e-4,'which is 0.018 % away and does not spoil the identification');
      eq(r.guess,'lead','and it still reads as lead');
    });
    /* the trap: left floating, every floater measures as water */
    withState({view:'mystery',mset:'set 1',submerge:false},()=>{
      const M=buildModel(ST);
      const floaters=M.rows.filter(r=>r.rho<RHO_WATER);
      ok(floaters.length>=2,'set 1 has floating blocks ('+floaters.length+')');
      for(const r of floaters){
        rel(r.rhoRead,RHO_WATER,2e-3,'a floating block left alone measures as WATER ('+r.tag+')');
        eq(r.guess,'water','so the table names it water');
        ok(!r.ok,'and the identification is wrong');
      }
      ok(M.nWrong>=2,'left alone, '+M.nWrong+' of 5 come out wrong');
      const sunk=M.rows.filter(r=>r.rho>RHO_WATER);
      for(const r of sunk) ok(r.ok,'a sinking block is unaffected ('+r.tag+')');
    });
    /* the shuffled set: every table material at every whole litre, as PhET draws them */
    let bad=0, we=0, wg=1e9;
    for(const k of DENSITY_TABLE) for(let L=1;L<=10;L++){
      const m=MAT[k].phet*L/LITERS, id=identify(disp2(m),L);
      if(id.id!==k) bad++;
      we=Math.max(we,id.err); wg=Math.min(wg,id.gap);
    }
    eq(bad,0,'all 130 material x whole-litre combinations are identified (derive: 0 misidentified)');
    rel(we,0.00240385,2e-4,'worst error over the 130: 0.24 % (derive)');
    rel(wg,0.0315789,2e-4,'smallest gap over the 130: 3.16 % (derive)');
    /* the shuffled draw is reproducible and legal */
    const s1=shuffledMystery(7), s2=shuffledMystery(7), s3=shuffledMystery(8);
    eq(s1.map(b=>b.truth).join(','),s2.map(b=>b.truth).join(','),'the shuffled set is reproducible from its seed');
    ok(s1.map(b=>b.truth).join(',')!==s3.map(b=>b.truth).join(','),'and a new seed draws a different set');
    /* a WITHOUT-replacement draw has to be checked over many seeds: one seed
       can look distinct by luck even when the draw replaces */
    let dupM=0, dupV=0, outV=0, wrongHi=0, notId=0, nSeed=0;
    for(let sd=1;sd<=200;sd++){
      const s=shuffledMystery(sd*2654435761>>>0||1); nSeed++;
      if(new Set(s.map(b=>b.truth)).size!==5) dupM++;
      if(new Set(s.map(b=>Math.round(b.V*LITERS))).size!==5) dupV++;
      if(!s.every(b=>b.V*LITERS>=1-1e-9&&b.V*LITERS<=10+1e-9)) outV++;
      if(s.filter(b=>b.V*LITERS>=7).length!==2) wrongHi++;
      for(const b of s) if(identify(disp2(b.m),disp2(b.V*LITERS)).id!==b.truth) notId++;
    }
    eq(nSeed,200,'200 shuffled sets were drawn');
    eq(dupM,0,'never twice the same material in one set (a with-replacement draw repeats in ~60 % of sets)');
    eq(dupV,0,'never twice the same volume');
    eq(outV,0,'every volume inside PhET’s 1-10 L');
    eq(wrongHi,0,'always exactly two from PhET’s 7-10 L draw');
    eq(notId,0,'and all 1000 blocks are identifiable from their printed numbers');
  }

  /* ---------- K. the models: every view, every preset, finite and clean ---------- */
  const PRESETS=[
    ['default',{}],
    ['two blocks',{view:'pool',two:true}],
    ['custom heavy',{view:'pool',matA:'custom',massA:27,volAL:1}],
    ['custom light',{view:'pool',matA:'custom',massA:0.5,volAL:10}],
    ['styrofoam min',{view:'pool',matA:'styrofoam',massA:0.15,volAL:1}],
    ['aluminium max',{view:'pool',matA:'aluminum',massA:27,volAL:10}],
    ['held under',{view:'pool',holdA:-POOL_H}],
    ['held aloft',{view:'pool',holdA:0.03}],
    ['sets mass lo',{view:'sets',setMode:'mass',sameMass:1}],
    ['sets mass hi',{view:'sets',setMode:'mass',sameMass:10}],
    ['sets volume',{view:'sets',setMode:'volume',sameVolL:10}],
    ['sets density lo',{view:'sets',setMode:'density',sameRho:100}],
    ['sets density hi',{view:'sets',setMode:'density',sameRho:2000}],
    ['mystery 2',{view:'mystery',mset:'set 2',mpick:'E'}],
    ['mystery 3 reveal',{view:'mystery',mset:'set 3',reveal:true,mpick:'C'}],
    ['mystery floating',{view:'mystery',mset:'set 1',submerge:false}],
    ['shuffled',{view:'mystery',mset:'shuffled',seed:12345}],
    ['mv gold',{view:'mv',mvMat:'gold'}],
    ['mv no ref',{view:'mv',mvMat:'pyrite',showRef:false}],
    ['line mercury',{view:'line',lineFluid:'mercury'}],
    ['line gasoline',{view:'line',lineFluid:'gasoline'}],
    ['line neutral',{view:'line',lineFluid:'water',matA:'custom',massA:5,volAL:5}],
  ];
  const badRe=/NaN|undefined|Infinity/;
  for(const [nm,over] of PRESETS) withState(over,()=>{
    let err=null, M=null;
    try{ M=buildModel(ST); }catch(e){ err=e; }
    ok(!err,nm+': the model builds'+(err?': '+(err.stack||err):''));
    if(err) return;
    const ro=readoutHTML(M,ST), eqb=eqbarHTML(M,ST), tg=tagHTML(M,ST);
    ok(!badRe.test(ro),nm+': the readout has no NaN/undefined');
    ok(!badRe.test(eqb),nm+': the equation bar is clean');
    ok(!badRe.test(tg),nm+': the tag is clean');
    ok(ro.length>200,nm+': the readout has substance');
    /* a non-finite-safe formatter makes a "no NaN" check vacuous, so pin a
       number only this configuration can supply (Known-bad, sbs_parent_law) */
    if(ST.view==='pool') ok(ro.indexOf(fmt(M.blocks[0].m,2)+' kg')>=0,nm+': the readout prints the model’s own mass');
    if(ST.view==='line') ok(ro.indexOf(fmt(100*M.frac,2)+' %')>=0,nm+': the readout prints the model’s own submerged fraction');
  });
  /* no slider combination produces a non-finite result */
  {
    let nf=0, n=0;
    for(const mat of MAT_LIST.map(o=>o.id)) for(const mL of [1,5.5,10]) for(const kg of [0.1,5,27]){
      const s2=Object.assign({},DEFAULTS,{view:'pool',matA:mat}); setVol(s2,'A',mL); setMass(s2,'A',kg);
      MEMO.pool=null;
      const M=poolModel(s2); n++;
      for(const b of M.blocks) if(!isFinite(b.m)||!isFinite(b.Vsub)||!isFinite(b.Fb)||!isFinite(M.yw)||b.Vsub<-1e-15||b.Vsub>b.V+1e-15) nf++;
    }
    eq(nf,0,'no combination of material, mass and volume gives a non-finite or illegal state ('+n+' swept)');
    clearMemo();
  }

  /* ---------- L. the drag ---------- */
  {
    const canvas={getContext:()=>makeShot(1180,740),getBoundingClientRect:()=>({left:0,top:0,width:1180,height:740}),
                  classList:{add(){},remove(){},contains(){return true;}},setPointerCapture(){}};
    const S=makeScene(canvas);
    withState({view:'pool'},()=>{
      const ctx=makeShot(S.W,S.H), M=buildModel(ST), G2=poolGeo(ctx,S.W,S.H,M), map=G2.map, bk=M.blocks[0];
      ok(!S.pointer('down',10,10),'a pointer-down away from every block grabs nothing');
      ok(S.pointer('down',map.X(bk.x),map.Y(bk.yb+bk.s/2)),'pointer-down on block A grabs it');
      eq(DRAG.what,'A','and it is block A that is held');
      const y0=bk.yb;
      ok(S.pointer('move',map.X(bk.x),map.Y(bk.yb+bk.s/2)+40),'the move is accepted');
      close(ST.holdA,y0-40/map.s,1e-9,'the block follows the pointer, keeping the grab offset');
      MEMO.pool=null;
      const M2=buildModel(ST);
      eq(M2.blocks[0].mode,'held','and the model says it is held');
      ok(M2.blocks[0].Vsub>bk.Vsub,'pushed down, it displaces more');
      ok(M2.yw>M.yw,'so the level rises');
      ok(M2.blocks[0].hand<0,'and the hand has to PUSH DOWN on a floater');
      ok(S.pointer('up',0,0),'pointer-up releases');
      eq(ST.holdA,null,'and the block is let go');
      MEMO.pool=null;
      close(buildModel(ST).yw,M.yw,1e-12,'released, everything returns to where it was');
      ok(!S.pointer('down',map.X(bk.x),map.Y(-POOL_H-0.05)),'a pointer-down in the floor grabs nothing');
    });
    withState({view:'sets'},()=>ok(!S.pointer('down',400,300),'the sets view ignores the pointer'));
    withState({view:'mv'},()=>ok(!S.pointer('down',400,300),'the plane view ignores the pointer'));
    withState({view:'line'},()=>ok(!S.pointer('down',400,300),'the waterline view ignores the pointer'));
    eq(S.step(),false,'nothing in this sim animates: step() never advances anything');
  }

  /* ---------- L2. the force arrows carry ONE length scale ---------- */
  withState({view:'pool',two:true},()=>{
    const M=buildModel(ST), FS=forceScale(M.blocks), len=FS.len, Fref=FS.Fref;
    const A=forceLengths(M.blocks[0],FS), B=forceLengths(M.blocks[1],FS);
    rel(Fref,M.blocks[1].W,1e-15,'the longest force is the aluminium block\u2019s weight');
    rel(A.W/B.W,M.blocks[0].W/M.blocks[1].W,1e-12,'the two weights\u2019 arrows are in the ratio of the weights');
    rel(A.Fb/B.Fb,M.blocks[0].Fb/M.blocks[1].Fb,1e-12,'and so are the two upthrusts\u2019');
    rel(A.W/A.Fb,M.blocks[0].W/M.blocks[0].Fb,1e-12,'within one block too');
    rel(B.W,len,1e-12,'the longest arrow is exactly the available length');
    rel(B.extra,len*M.blocks[1].N/Fref,1e-12,'the contact arrow is on the same scale');
    close(len,0.10349879733383488,1e-15,'the arrow length IS the room the tightest block leaves (0.1035 m)');
    ok(len<0.13-1e-6,'which is less than the 0.13 m ceiling, so the room is really doing the work');
    close(len,M.blocks[1].yb+M.blocks[1].s/2-(-POOL_H-0.018),1e-15,'= the sunk block\u2019s centre above the floor');
  });
  /* the reference force must be the BIGGEST, not the last block's: put the
     heavy block first, where a loop that overwrites instead of maximising
     would come out with the light one */
  withState({view:'pool',two:true,matA:'aluminum',massA:13.5,volAL:5,matB:'wood',massB:2,volBL:5},()=>{
    const M=buildModel(ST), FS=forceScale(M.blocks);
    rel(M.blocks[0].W,132.3,1e-12,'block A is now the heavy one');
    rel(M.blocks[1].W,19.6,1e-12,'and block B the light one');
    close(FS.Fref,132.3,1e-12,'the reference force is still 132.3 N, the LARGEST');
    const A=forceLengths(M.blocks[0],FS), B=forceLengths(M.blocks[1],FS);
    rel(A.W,FS.len,1e-12,'so the heavy block gets the full-length arrow');
    ok(B.W<A.W*0.2,'and the light one a short one ('+fmt(B.W/A.W,3)+' of it)');
    close(holdCeiling(cubeSide(0.005)),0.03700240533233027,1e-15,
          'the hold ceiling leaves a 5 L block\u2019s top exactly at the top of the world');
    close(holdCeiling(cubeSide(0.005))+cubeSide(0.005)+0.012,POOL_YTOP,1e-15,'which is what it is for');
    ok(holdCeiling(cubeSide(0.01))<holdCeiling(cubeSide(0.001)),'a bigger block cannot be lifted as high');
  });

  /* ---------- L3. the draft panel draws the fraction it prints ---------- */
  {
    /* The defect this pins: at a tank depth of 0.95 s a RESTING block drawn on
       the tank floor had its top above the surface, so the panel showed it
       half out while the readout beside it said 100 % under, and the dimension
       line measured that false draft.  Asserted both ways — the drawn draft
       equals the model's submerged fraction, AND the old depth is shown to
       still break it, so the constant cannot quietly go back. */
    const CASES=[['water',{},'float'],['water',{matA:'brick'},'rest'],
                 ['mercury',{},'float'],['water',{matA:'custom',massA:5,volAL:5},'rest'],
                 ['gasoline',{matA:'styrofoam',volAL:10},'float'],
                 ['water',{matA:'aluminum',volAL:10},'rest']];
    for(const [fl,over,want] of CASES) withState(Object.assign({view:'line',lineFluid:fl},over),()=>{
      const M=buildModel(ST);
      eq(M.blk.mode,want,fl+'/'+(over.matA||'wood')+': the block '+(want==='float'?'floats':'rests'));
      for(const hpx of [120,250,400]){
        const D=draftGeom(M,hpx);
        rel(D.drawnFrac,M.frac,1e-12,fl+'/'+(over.matA||'wood')+' at '+hpx+' px: the DRAWN draft is the printed fraction');
        ok(D.ytop<=0+1e-12||M.blk.mode==='float',
           fl+'/'+(over.matA||'wood')+' at '+hpx+' px: a fully submerged block is drawn entirely under the surface');
        ok(D.yb>=D.ybot0-1e-12,'and never below the tank floor');
        ok(D.ytop<=D.ytop0+1e-12,'nor above the top of the panel');
      }
    });
    /* the reintroduced defect must still fail: a 0.95 s tank puts a resting
       block's top above the surface, and the drawn fraction then lies */
    withState({view:'line',lineFluid:'water',matA:'brick'},()=>{
      const M=buildModel(ST), s=M.side, hpx=250;
      const shallowBot=-0.95*s, scB=hpx/(0.55*s-shallowBot);
      const ybB=shallowBot+6/scB, ytopB=ybB+s, ysubB=Math.min(ytopB,0);
      ok(ytopB>0,'the old 0.95 s tank really did put the block’s top above the surface');
      ok(Math.abs((ysubB-ybB)/s-M.frac)>0.05,
         'and its drawn fraction was wrong by '+fmt(Math.abs((ysubB-ybB)/s-M.frac),3)+', which is the bug');
      eq(M.frac,1,'while the model said, and still says, 1');
    });
  }

  /* ---------- M. layout sweep: every view drawn at four sizes ---------- */
  const SIZES=[[1400,820],[1180,740],[900,600],[620,420]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const SWEEP=[
    ['pool default',{view:'pool'},6],
    ['pool two',{view:'pool',two:true},8],
    ['pool held',{view:'pool',holdA:-POOL_H},6],
    ['pool no forces',{view:'pool',forces:false},5],
    ['pool custom',{view:'pool',matA:'custom',massA:10,volAL:2},6],
    ['sets mass',{view:'sets',setMode:'mass'},8],
    ['sets volume',{view:'sets',setMode:'volume'},8],
    ['sets density',{view:'sets',setMode:'density',sameRho:1800},8],
    ['mystery 1',{view:'mystery',mset:'set 1'},9],
    ['mystery 2',{view:'mystery',mset:'set 2',mpick:'D'},9],
    ['mystery floating',{view:'mystery',mset:'set 1',submerge:false},9],
    ['shuffled',{view:'mystery',mset:'shuffled',seed:99},9],
    ['mv wood',{view:'mv'},3],
    ['mv gold',{view:'mv',mvMat:'gold'},3],
    ['mv no ref',{view:'mv',showRef:false},3],
    ['line water',{view:'line'},4],
    ['line mercury',{view:'line',lineFluid:'mercury'},4],
    ['line sinking',{view:'line',matA:'brick'},4],
  ];
  for(const [nm,over,minFills] of SWEEP) for(const [W,H] of SIZES) withState(over,()=>{
    const c=makeShot(W,H); let err=null;
    try{ drawView(c,W,H,buildModel(ST),ST); }catch(e){ err=e; }
    ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
    if(err) return;
    const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
    ok(fills.length>=minFills&&texts.length>=3,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+')');
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

  /* the canvas carries no letter subscripts (there is no Unicode subscript f,
     and the rasteriser's font does not have all of the ones that exist) */
  {
    const c=makeShot(1180,740);
    let bads=[];
    for(const v of TABS.map(t=>t[0])) withState({view:v},()=>{
      drawView(c,1180,740,buildModel(ST),ST);
    });
    for(const o of c.ops) if(o.op==='text'&&/[ₐ-ₜᵢ-ᵪ]/.test(o.t)) bads.push(o.t);
    eq(bads.length,0,'no letter subscripts reach the canvas (greenhouse-effect Known-bad)'+(bads.length?': '+bads[0]:''));
  }

  Object.assign(ST,stSave); clearMemo();
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
