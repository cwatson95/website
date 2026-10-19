/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/buoyancy-basics/refvals.txt, which is  *
 *  build/density/derive.py's printed output: the two sims run ONE     *
 *  engine, so they are pinned against one independent Python solve    *
 *  (scipy.brentq on the force balance, a 4000-strip face integral, a  *
 *  2000-point perimeter sum), read in full.                           *
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
  const WATER=MAT.water.phet;
  function withState(over,fn){
    const keep=Object.assign({},ST);
    Object.assign(ST,DEFAULTS,over); clearAll();
    try{ fn(); } finally { Object.assign(ST,keep); clearAll(); }
  }

  /* ---------- A. the scaffold ---------- */
  close(90*DEG,PI/2,1e-15,'DEG converts degrees INTO radians (90 DEG = pi/2)');
  ok((()=>{ try{ toRgb('not a colour'); return false; }catch(e){ return true; } })(),'toRgb throws rather than returning black');
  eq(toRgb(mix('#000000','#ffffff',0.5)).join(','),'128,128,128','mix() output is a legal mix() input');
  eq(plain('&#955;'),'λ','plain decodes a NUMERIC entity (Known-bad: wave_fronts)');
  eq(plain('<b>x</b>'),'x','plain strips tags');
  for(const id of BUOY_FLUIDS) ok(/^#[0-9a-f]{6}$/i.test(fluidColor(id)),'fluidColor('+id+') is a hex colour');

  /* ---------- B. the pool and the scales, PhET's bounds (derive) ---------- */
  close(POOL_H,0.41666666666666663,1e-17,'POOL_H = 0.15/0.9/0.4 (derive)');
  close(A_POOL,0.36000000000000004,1e-17,'A_POOL (derive)');
  eq(VF0,0.1,'PhET starts the pool with 100 L');
  close(SCALE_V,0.0018,1e-18,'PhET’s scale is 0.15 x 0.06 x 0.2 m = 1.8 L');
  close(poolLevel([],[],WATER,VF0),-0.1388888888888889,1e-15,'the bare level, bisected (derive)');
  eq(G,9.8,'PhET runs at g = 9.8, not 9.80665');
  eq(BUOY_FLUIDS.length,6,'PhET’s six Buoyancy fluids');
  eq(BUOY_FLUIDS.map(f=>MAT[f].phet).join(','),'680,920,1000,1029,1440,13593','and their densities (PhET)');
  eq(MAT.gasoline.phet<MAT.oil.phet&&MAT.honey.phet<MAT.mercury.phet,true,'ordered lightest to heaviest');
  /* the pool scale, at PhET's initial half height */
  {
    const st={scaleH:0.5};
    close(poolScaleTop(st),-0.17833333333333332,1e-15,'the pool scale’s top at half height (derive)');
    close(poolScaleY0({scaleH:0}),-POOL_H,1e-15,'at 0 it stands on the floor');
    close(poolScaleTop({scaleH:1}),0,1e-15,'at 1 its top is level with the ground');
    const obs=poolObstacles(st);
    close(obstacleVolume(obs,poolScaleTop(st)),SCALE_V,1e-18,'covered, it displaces exactly 1.8 L');
    close(obstacleVolume(obs,poolScaleTop(st)+1),SCALE_V,1e-18,'and no more, however deep');
    eq(obstacleVolume(obs,poolScaleY0(st)-0.01),0,'below it, nothing');
    const bare=poolLevel([],[],WATER,VF0), withSc=poolLevel([],obs,WATER,VF0);
    close(withSc-bare,SCALE_V/A_POOL,1e-14,'the scale alone raises the level by its own volume / A');
  }

  /* ---------- C. Archimedes, closed form vs scipy (derive) ---------- */
  close(cubeSide(0.005),0.17099759466766973,1e-17,'a 5 L cube is 17.0998 cm on a side (derive)');
  close(floatDraft(0.005,400,1000),0.068399037867067886,1e-17,'the wood draft, closed form (derive)');
  close(floatDraft(0.005,400,1000),0.068399037867067872,2e-17,'and scipy.brentq on the force balance (scipy)');
  eq(cubeBelow(0.005,-0.4,0.4),0.005,'cubeBelow saturates at V EXACTLY, not at s^3');
  close(riseFloating(2,1000),0.0055555555555555549,1e-17,'a floating 2 kg block raises the level 5.56 mm (derive)');
  close(riseSunk(0.005),0.013888888888888888,1e-17,'a sunk 5 L block raises it 13.9 mm (derive)');
  {
    const w=solvePool([{V:2/400,rho:400}],WATER);
    close(w.yw,-0.13333333333333336,1e-15,'wood alone: the level (derive)');
    close(w.blocks[0].Fb,19.6,1e-13,'upthrust 19.6 N = its weight (derive)');
    const a=solvePool([{V:13.5/2700,rho:2700}],WATER);
    close(a.blocks[0].N,83.3,1e-12,'aluminium alone: the floor takes 83.3 N (derive)');
    const b=solvePool([{V:2/400,rho:400},{V:13.5/2700,rho:2700}],WATER);
    close(b.yw,-0.11944444444444444,1e-15,'both blocks: the level (derive)');
  }

  /* ---------- D. the awkward cases ---------- */
  {
    const r=solvePool([{V:0.005,rho:2700}],WATER).blocks[0];
    eq(r.frac,1,'denser than the fluid: the submerged fraction is EXACTLY 1');
    close(r.N,83.300000000000011,1e-12,'and N = 83.3 N (derive)');
    const n=solvePool([{V:0.005,rho:1000}],WATER).blocks[0];
    eq(n.frac,1,'exactly neutral: completely submerged');
    close(n.N,0,1e-12,'the floor takes nothing (derive)');
    close(apparentWeight(0.005,1000,1000),0,1e-13,'and a spring scale reads zero (derive)');
    const h1=solvePool([{V:0.005,rho:1000,held:-0.30}],WATER).blocks[0];
    const h2=solvePool([{V:0.005,rho:1000,held:-0.34}],WATER).blocks[0];
    close(h1.hand,0,1e-12,'a neutral block needs no hand at -0.30 m (derive)');
    close(h2.hand,h1.hand,1e-12,'nor at -0.34 m: no depth is preferred');
    const hb=solvePool([{V:0.005,rho:400,held:-0.25}],WATER).blocks[0];
    eq(hb.N,0,'a HELD block is not touching the floor: N = 0');
    ok(Math.abs(hb.hand)>1,'while the hand carries '+fmt(hb.hand,2)+' N');
    const ob=solvePool([{V:0.005,rho:2700,inPool:false}],WATER).blocks[0];
    eq(ob.mode,'out','a block out of the pool is out');
    eq(ob.Vsub,0,'displaces nothing'); eq(ob.N,0,'and gets no contact force');
    /* wider than the pool's free surface */
    const wideV=0.216, sw=cubeSide(wideV);
    ok(sw*sw>=A_POOL-1e-12,'the test block spans the pool ('+fmt(sw*sw,3)+' m2 vs '+fmt(A_POOL,3)+')');
    const wr=solvePool([{V:wideV,rho:3000}],WATER);
    close(wr.yw,0.46111111111111103,1e-14,'the fluid stands ABOVE a body that spans the pool (derive)');
    close(wr.yw,-POOL_H+sw+VF0/A_POOL,1e-14,'= -H + s + Vf/A');
    const wf=solvePool([{V:wideV,rho:400}],WATER);
    close(wf.blocks[0].yb,-POOL_H+VF0/A_POOL,1e-14,'and a spanning floater rides on all of it (derive)');
    /* N >= 0 is physics, not a clamp */
    let minN=1e9, nRest=0, nZero=0;
    for(const rho of [100,400,919,1000,1000.0001,2700,19320])
      for(const VL of [1,3,5.5,10])
        for(const Vf of [0.004,0.02,0.1,0.14]){
          const r2=solvePool([{V:VL/LITERS,rho:rho}],WATER,[],Vf).blocks[0];
          if(r2.mode==='rest'){ nRest++; minN=Math.min(minN,r2.N); if(r2.N===0) nZero++; }
        }
    ok(nRest>=40,'the sweep reaches '+nRest+' resting configurations');
    ok(minN>=0,'a resting block is never pulled DOWN by the floor (min N = '+minN.toExponential(2)+')');
    ok(nZero>=4,'and exactly-neutral blocks reach N = 0 exactly ('+nZero+')');
    /* G is non-decreasing, WITH the pool scale in the way */
    const obs=poolObstacles({scaleH:0.5}), bl=[{V:0.005,rho:400},{V:0.005,rho:2700}];
    let worst=0, prev=-1e18;
    for(let k=0;k<=4000;k++){
      const y=-POOL_H+k*(POOL_H+0.8)/4000, g=netFluid(y,bl,obs,WATER);
      worst=Math.min(worst,g-prev); prev=g;
    }
    ok(worst>=-1e-15,'G is non-decreasing over 4001 levels with the scale in the pool (worst step '+worst.toExponential(2)+')');
  }

  /* ---------- E. the faces: the upthrust taken the long way ---------- */
  {
    const st=solvePool([{V:0.005,rho:2700}],WATER), yw=st.yw, yb=st.blocks[0].yb;
    const F=cubeFaceForces(0.005,yb,yw,WATER);
    close(F.net,49.000000000000014,1e-12,'submerged: bottom minus top face = 49 N (derive)');
    rel(F.net,WATER*G*0.005,1e-15,'and that IS rho_f g V, to 1e-15 relative');
    eq(F.sideSum,0,'the two opposite side faces cancel exactly (derive: 0)');
    close(F.side,59.078173683917754,1e-9,'one side face carries 59.0782 N (derive, 4000 strips)');
    ok(F.side>F.net,'bigger than the upthrust — it cancels only because there are two of it');
    close(F.side,WATER*G*(yw-yb-cubeSide(0.005)/2)*cubeSide(0.005)*cubeSide(0.005),1e-12,
          '= rho g (depth of the face centre) x face area');
    const stf=solvePool([{V:0.005,rho:400}],WATER);
    const F2=cubeFaceForces(0.005,stf.blocks[0].yb,stf.yw,WATER);
    close(F2.net,19.600000000000009,1e-12,'floating: only the bottom face is wet, 19.6 N (derive)');
    eq(F2.pTop,0,'the top face is dry');
    /* a PARTLY submerged side face is wetted only over the strip below the
       surface, and the pressure there averages half the bottom's */
    {
      const sq=cubeSide(0.005), dsub=stf.yw-stf.blocks[0].yb;
      close(F2.side,WATER*G*(dsub/2)*sq*dsub,1e-12,'part submerged: the side force is rho g (d/2) s d');
      ok(F2.side<WATER*G*dsub*sq*sq*0.999,'far less than the whole face wetted to the waterline');
    }
    const poly=cubePoly(0.005,stf.blocks[0].yb,0), sub=clipBelow(poly,stf.yw);
    const E=edgeForces(sub,stf.yw,WATER), fine=finePerimeter(sub,stf.yw,WATER,2000);
    close(E.tot[0],0,1e-12,'the polygon integral: the horizontal parts cancel (derive: 0)');
    close(E.tot[1],114.62149533794438,1e-11,'and the vertical parts sum to 114.62 N/m (derive)');
    rel(fine[1],E.tot[1],1e-6,'a 2000-point perimeter sum agrees with the closed form');
    close(polyCentroid(sub)[0],0,1e-15,'the centre of buoyancy is on the axis of a symmetric block');
    /* the faces MODEL, as the view builds it */
    withState({view:'faces',facesDepth:0.45,matA:'brick',volAL:5},()=>{
      const M=buildModel(ST);
      ok(M.fullyUnder,'at 45 cm a 5 L cube is fully under');
      rel(M.F.net,M.arch,1e-14,'the face integral equals rho_f g V_sub');
      ok(M.resid<1e-14,'they differ by '+M.resid.toExponential(2));
      ok(M.resid2d<1e-14,'and the 2-D route by '+M.resid2d.toExponential(2));
      ok(M.fineResid<1e-6,'and the brute-force perimeter sum by '+M.fineResid.toExponential(2));
      close(M.F.pBot,WATER*G*0.45,1e-10,'p at the bottom is rho g x 45 cm');
      close(M.F.pTop,WATER*G*(0.45-cubeSide(0.005)),1e-10,'and at the top rho g x (45 cm - the side)');
      close(M.F.pBot-M.F.pTop,WATER*G*cubeSide(0.005),1e-10,'their difference is rho g x the side, whatever the depth');
    });
    withState({view:'faces',facesDepth:0.9,matA:'brick',volAL:5},()=>{
      const M=buildModel(ST);
      rel(M.F.net,M.arch,1e-14,'twice as deep, the net force is unchanged');
      close(M.F.net,49.000000000000014,1e-10,'still 49.0 N');
    });
    withState({view:'faces',facesDepth:0.10,matA:'brick',volAL:5},()=>{
      const M=buildModel(ST);
      ok(!M.fullyUnder,'at 10 cm the top of a 17.1 cm cube is out');
      eq(M.F.pTop,0,'so the top face is dry');
      rel(M.F.net,WATER*G*cubeBelow(0.005,-0.10,0),1e-14,'and the net force is rho g V_sub of the wetted part');
    });
  }

  /* ---------- F. the six fluids (derive) ---------- */
  {
    const PCT={gasoline:58.8235,oil:43.4783,water:40,seawater:38.8727,honey:27.7778,mercury:2.94269};
    for(const f of BUOY_FLUIDS){
      const rhoF=MAT[f].phet;
      const w=solvePool([{V:2/400,rho:400}],rhoF).blocks[0];
      rel(100*w.frac,PCT[f],1e-4,'wood is '+PCT[f]+' % under in '+f+' (derive)');
      eq(w.mode,'float','and it floats in '+f);
    }
    const alMerc=solvePool([{V:13.5/2700,rho:2700}],MAT.mercury.phet).blocks[0];
    rel(100*alMerc.frac,19.8632,1e-4,'aluminium is 19.86 % under in mercury (derive)');
    eq(alMerc.mode,'float','so aluminium FLOATS in mercury');
    const alWater=solvePool([{V:13.5/2700,rho:2700}],WATER).blocks[0];
    eq(alWater.mode,'rest','and rests on the floor in water');
    /* the pool scale reading (derive) */
    const obs=poolObstacles({scaleH:0.5}), top=poolScaleTop({scaleH:0.5});
    const so=solvePool([{V:13.5/2700,rho:2700,support:top}],WATER,obs);
    close(so.yw,-0.12995986441149004,1e-12,'a block on the pool scale: the level (derive)');
    close(so.blocks[0].N,118.43840164373687,1e-10,'the pool scale reads 118.44 N (derive)');
    close(13.5*G,132.30000000000001,1e-12,'the ground scale would read 132.30 N (derive)');
    close(13.5*G-so.blocks[0].N,WATER*G*so.blocks[0].Vsub,1e-12,
          'and the difference is exactly the weight of the fluid pushed aside');
  }

  /* ---------- F2. the two scales, off the explore model ---------- */
  withState({view:'explore',where:'poolscale',matA:'aluminum',massA:13.5,volAL:5},()=>{
    const M=buildModel(ST);
    eq(M.blocks[0].mode,'rest','on the pool scale the block rests on IT');
    close(M.blocks[0].yb,poolScaleTop(ST),1e-15,'its bottom is the scale\u2019s top, not the pool floor');
    ok(M.blocks[0].yb>-POOL_H+1e-6,'which is '+fmt(100*(M.blocks[0].yb+POOL_H),1)+' cm above the floor');
    close(M.poolReads,M.blocks[0].N,1e-15,'the pool scale reads the CONTACT force');
    ok(M.poolReads<M.blocks[0].W-1e-6,'less than the weight ('+fmt(M.poolReads,2)+' vs '+fmt(M.blocks[0].W,2)+' N)');
    close(M.blocks[0].W-M.poolReads,MAT.water.phet*G*M.blocks[0].Vsub,1e-12,'by exactly the upthrust');
    close(M.poolReads,118.43840164373687,1e-9,'118.44 N (derive)');
    eq(M.groundReads,0,'and the ground scale reads nothing');
  });
  withState({view:'explore',where:'ground',matA:'aluminum',massA:13.5,volAL:5},()=>{
    const M=buildModel(ST);
    eq(M.blocks[0].mode,'out','on the ground scale the block is out of the pool');
    eq(M.blocks[0].Fb,0,'so it has no buoyancy at all (PhET ignores air)');
    close(M.groundReads,132.30000000000001,1e-9,'the ground scale reads its full 132.30 N (derive)');
    close(M.groundReads,M.blocks[0].W,1e-15,'= its weight');
    eq(M.poolReads,0,'and the pool scale reads nothing');
    close(M.blocks[0].yb,SCALE_H,1e-15,'it stands on the scale\u2019s 6 cm platform');
  });
  withState({view:'explore',where:'floor',matA:'aluminum',massA:13.5,volAL:5},()=>{
    const M=buildModel(ST);
    close(M.blocks[0].yb,-POOL_H,1e-15,'on the pool floor its bottom IS the pool floor');
    eq(M.poolReads,0,'and neither scale reads anything');
    eq(M.groundReads,0,'at all');
  });

  /* ---------- G. the Compare screen, PhET's two blocks (derive) ---------- */
  {
    const m=compareBlocks(BB_CUBES,'mass',4,0.005,400);
    eq(m.map(b=>Math.round(b.rho)).join(','),'2000,400','same mass 4 kg -> brick 2000, wood 400 (derive)');
    eq(m.map(b=>fmt(b.V*LITERS,0)).join(','),'2,10','from 2 L and 10 L (PhET)');
    const v=compareBlocks(BB_CUBES,'volume',4,0.005,400);
    eq(v.map(b=>Math.round(b.rho)).join(','),'2000,400','same volume 5 L -> the same two densities (derive)');
    eq(v.map(b=>fmt(b.rho*b.V,0)).join(','),'10,2','from 10 kg and 2 kg (PhET)');
    const d=compareBlocks(BB_CUBES,'density',4,0.005,400);
    eq(d.map(b=>fmt(b.rho*b.V,0)).join(','),'2,4','same density 400 -> 2 kg and 4 kg (derive)');
    eq(DEFAULTS.sameMass,4,'the screen opens at PhET’s 4 kg');
    eq(DEFAULTS.sameVolL,5,'5 L'); eq(DEFAULTS.sameRho,400,'and the wood’s 400 kg/m3');
    const sm=solvePool(m,WATER);
    eq(sm.blocks.map(b=>b.mode).join(','),'rest,float','same mass: the brick sinks, the wood floats (derive)');
    const sv=solvePool(v,WATER);
    eq(sv.blocks.map(b=>b.mode).join(','),'rest,float','same volume: the same answer (derive)');
    const sd=solvePool(d,WATER);
    eq(sd.blocks.map(b=>fmt(b.frac,4)).join(','),'0.4000,0.4000','same density: both 40 % under, whatever the size (derive)');
  }

  /* ---------- H. PhET's mass/volume coupling, in the model ---------- */
  {
    const s2=Object.assign({},DEFAULTS);
    setMat(s2,'A','aluminum'); setVol(s2,'A',5);
    close(s2.massA,13.5,1e-12,'5 L of aluminium is 13.5 kg');
    setMass(s2,'A',27); close(s2.volAL,10,1e-12,'27 kg of aluminium is exactly 10 L (PhET’s ceiling)');
    setMass(s2,'A',2);  close(s2.massA,2.7,1e-12,'asking for 2 kg is refused: 1 L is 2.7 kg');
    setVol(s2,'A',4);   close(s2.massA,10.8,1e-12,'4 L of aluminium is 10.8 kg');
    setMat(s2,'A','wood'); close(s2.volAL,4,1e-12,'switching material keeps the VOLUME');
    close(s2.massA,1.6,1e-12,'and rebuilds the mass');
    setMat(s2,'A','custom'); setVol(s2,'A',8);
    close(s2.massA,1.6,1e-12,'custom: the volume moves alone');
    close(rhoOf(s2,'A'),200,1e-12,'and the density follows, rho = m/V');
    setMass(s2,'A',4); close(rhoOf(s2,'A'),500,1e-12,'4 kg in 8 L is 500 kg/m3');
    ok(rhoOf(s2,'A')!==8/4*LITERS,'the density is m/V, not V/m');
    close(massRangeFor(400,false)[1],4,1e-15,'wood’s mass slider stops at 4 kg (derive)');
    close(massRangeFor(2700,false)[1],27,1e-15,'aluminium reaches PhET’s 27 kg ceiling (derive)');
    eq(massRangeFor(19320,false)[1],27,'gold is CLIPPED at 27 kg, which is what makes 27 a ceiling');
    eq(massRangeFor(19320,false)[0],19.32,'while 1 L of gold, 19.32 kg, is still under it');
    let bad=0;
    for(const id of SIMPLE_MATS.concat(['custom'])) for(const V of [1,2.5,5,7.5,10]) for(const mm of [0.1,1,5,13.5,27]){
      const s5=Object.assign({},DEFAULTS); setMat(s5,'A',id); setVol(s5,'A',V); setMass(s5,'A',mm);
      const rng=massRangeFor(id==='custom'?0:MAT[id].phet,id==='custom');
      if(s5.volAL<VMIN_L-1e-12||s5.volAL>VMAX_L+1e-12) bad++;
      if(s5.massA<rng[0]-1e-12||s5.massA>rng[1]+1e-12) bad++;
      if(id!=='custom'&&Math.abs(s5.massA-MAT[id].phet*s5.volAL/LITERS)>1e-12) bad++;
    }
    eq(bad,0,'175 material x volume x mass settings stay inside PhET’s ranges and keep m = rho V');
  }

  /* ---------- I. the scale view: the reading, all the way down (derive) ---------- */
  withState({view:'scale',matA:'custom',massA:10,volAL:5,fluid:'water'},()=>{
    const M=buildModel(ST);
    close(M.rho,2000,1e-12,'a 5 L block of 10 kg is 2000 kg/m3');
    close(M.W,98,1e-12,'it weighs 98 N in air (derive)');
    close(M.full,49,1e-12,'and reads 49 N once fully under (derive)');
    /* out of the water, the reading is the whole weight */
    const c=M.curve;
    close(c[0][1],98,1e-10,'lowered 0, the scale reads its full weight');
    close(c[c.length-1][1],49,1e-10,'lowered 1, it reads the apparent weight');
    ok(c.every(p=>p[1]<=98+1e-9&&p[1]>=49-1e-9),'and never leaves that band');
    close(c[c.length-1][3],-POOL_H,1e-15,'lowered 1 really is the pool FLOOR, not somewhere above it');
    close(c[0][3],poolLevel([],[],MAT.water.phet,VF0)+0.02,1e-15,'and lowered 0 is 2 cm above the surface');
    close(loweredY({fluid:'water',lowered:1.5},M.s),loweredY({fluid:'water',lowered:1},M.s),1e-15,
          'a lowering past 1 is clamped to 1');
    close(loweredY({fluid:'water',lowered:-0.5},M.s),loweredY({fluid:'water',lowered:0},M.s),1e-15,
          'and below 0 to 0');
    /* monotone: the reading only ever falls */
    let mono=true;
    for(let i=1;i<c.length;i++) if(c[i][1]>c[i-1][1]+1e-9) mono=false;
    ok(mono,'the reading falls monotonically as the block goes in');
    /* the plateau: once V_sub is the whole volume the reading stops changing */
    const under=c.filter(p=>p[2]>=M.V-1e-12);
    ok(under.length>20,under.length+' of the 241 points are fully submerged');
    let flat=0;
    for(const p of under) if(Math.abs(p[1]-49)>1e-9) flat++;
    eq(flat,0,'and at every one of them the reading is 49 N exactly — depth does not matter');
    /* a floating block reaches zero and the string goes slack */
    withState({view:'scale',matA:'wood',volAL:5,fluid:'water',lowered:1},()=>{
      const F=buildModel(ST);
      ok(F.full<0,'a wood block’s apparent weight is negative: it would float');
      close(F.read,0,1e-12,'so the spring reads zero');
      ok(F.slack,'and the model says the string is slack');
    });
    withState({view:'scale',matA:'aluminum',volAL:5,fluid:'mercury',lowered:1},()=>{
      const F=buildModel(ST);
      ok(F.slack,'aluminium in mercury: slack too');
      /* the block is being HELD on the floor here, so its own free-floating
         fraction is the thing to pin, not the held one */
      rel(100*submergedFraction(F.rho,F.rhoF),19.8632,1e-4,'left alone it would float 19.86 % under (derive)');
      eq(F.frac,1,'held on the floor it is of course completely under');
    });
  });

  /* ---------- J. float or sink ---------- */
  withState({view:'fluids'},()=>{
    const M=buildModel(ST);
    eq(M.rows.length,27,'27 materials (every one PhET carries except air)');
    eq(M.cols.length,6,'6 fluids');
    eq(M.nCells,162,'162 combinations');
    let mono=true;
    for(let i=1;i<M.rows.length;i++) if(M.rows[i].phet<M.rows[i-1].phet) mono=false;
    ok(mono,'the rows are ordered by density');
    /* every cell agrees with the law, computed a second way */
    let bad=0;
    M.rows.forEach((m,i)=>M.cols.forEach((f,j)=>{
      const c=M.grid[i][j];
      if(c.floats!==(m.phet<f.rho)) bad++;
      if(Math.abs(c.frac-Math.min(1,m.phet/f.rho))>1e-15) bad++;
      if(c.floats&&Math.abs(c.frac-m.phet/f.rho)>1e-15) bad++;
    }));
    eq(bad,0,'all 162 cells agree with min(1, rho_b/rho_f)');
    eq(M.mercuryFloats,23,'23 of the 27 float in mercury');
    eq(M.rows.filter(m=>m.phet>=MAT.mercury.phet).map(m=>m.id).join(','),'mercury,tantalum,gold,platinum',
       'the four that do not are mercury itself, tantalum, gold and platinum');
    ok(MAT.lead.phet<MAT.mercury.phet,'lead (11342) DOES float in mercury (13593)');
    ok(MAT.gold.phet>MAT.mercury.phet,'gold (19320) does not');
    eq(M.gasolineFloats,2,'only 2 float in gasoline');
    ok(M.rows.filter(m=>m.phet<MAT.gasoline.phet).map(m=>m.id).join(',')==='styrofoam,wood',
       'styrofoam and wood');
    ok(M.nFloat>0&&M.nFloat<M.nCells,M.nFloat+' of 162 combinations float');
    /* the CAPTION makes a claim about which materials do not float in mercury,
       and prose is invisible to every other assertion here: it said "except
       tantalum and platinum" for a build, which is wrong by two entries */
    const sinkers=M.rows.filter(m=>m.phet>=MAT.mercury.phet&&m.id!=='mercury').map(m=>m.id);
    eq(sinkers.join(','),'tantalum,gold,platinum','three solids do not float in mercury');
    for(const id of sinkers)
      ok(FLU_CAP_FULL.indexOf(MAT[id].name)>=0,'the caption names '+MAT[id].name+' as one of them');
    for(const id of ['silver','lead','copper'])
      ok(FLU_CAP_FULL.indexOf('except')<0||FLU_CAP_FULL.split('except')[1].split(';')[0].indexOf(MAT[id].name)<0,
         'and does not name '+MAT[id].name+', which floats');
    const gasFloat=M.rows.filter(m=>m.phet<MAT.gasoline.phet).map(m=>m.id);
    eq(gasFloat.join(','),'styrofoam,wood','two materials float in gasoline');
    for(const id of gasFloat) ok(FLU_CAP_FULL.indexOf(MAT[id].name)>=0,'the caption names '+MAT[id].name+' too');
  });

  /* ---------- K. the models: every view, every preset, finite and clean ---------- */
  const PRESETS=[
    ['default',{}],
    ['two blocks',{view:'explore',two:true}],
    ['mercury',{view:'explore',fluid:'mercury'}],
    ['gasoline two',{view:'explore',fluid:'gasoline',two:true}],
    ['on the pool scale',{view:'explore',where:'poolscale'}],
    ['on the ground scale',{view:'explore',where:'ground'}],
    ['pool scale low',{view:'explore',where:'poolscale',scaleH:0}],
    ['pool scale high',{view:'explore',where:'poolscale',scaleH:1}],
    ['held under',{view:'explore',holdA:-POOL_H}],
    ['custom heavy',{view:'explore',matA:'custom',massA:27,volAL:1}],
    ['sets mass',{view:'sets',setMode:'mass'}],
    ['sets volume',{view:'sets',setMode:'volume',sameVolL:10}],
    ['sets density',{view:'sets',setMode:'density',sameRho:3000}],
    ['sets honey',{view:'sets',fluid:'honey'}],
    ['faces shallow',{view:'faces',facesDepth:0.05}],
    ['faces deep',{view:'faces',facesDepth:0.9,matA:'brick'}],
    ['faces mercury',{view:'faces',fluid:'mercury'}],
    ['scale start',{view:'scale',lowered:0}],
    ['scale end',{view:'scale',lowered:1,matA:'brick'}],
    ['scale mercury',{view:'scale',fluid:'mercury',matA:'aluminum'}],
    ['fluids gold',{view:'fluids',gridMat:'gold'}],
    ['fluids styrofoam',{view:'fluids',gridMat:'styrofoam'}],
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
    /* pin a number only this configuration can supply (Known-bad: a
       non-finite-safe formatter makes a "no NaN" check vacuous) */
    if(ST.view==='explore') ok(ro.indexOf(fmt(M.blocks[0].pct,1)+' %')>=0,nm+': the readout prints the model’s own % submerged');
    if(ST.view==='faces') ok(ro.indexOf(fmt(M.F.net,2)+' N')>=0,nm+': the readout prints the model’s own net face force');
    if(ST.view==='scale') ok(ro.indexOf(fmt(M.read,2)+' N')>=0,nm+': the readout prints the model’s own reading');
  });
  /* no slider combination gives a non-finite or illegal state */
  {
    let nf=0, n=0;
    for(const mat of MAT_LIST.map(o=>o.id)) for(const mL of [1,5.5,10]) for(const kg of [0.1,5,27])
      for(const f of ['gasoline','water','mercury']){
        const s2=Object.assign({},DEFAULTS,{view:'explore',matA:mat,fluid:f});
        setVol(s2,'A',mL); setMass(s2,'A',kg);
        clearAll();
        const M=exploreModel(s2); n++;
        for(const b of M.blocks) if(!isFinite(b.m)||!isFinite(b.Vsub)||!isFinite(b.Fb)||!isFinite(M.yw)
                                    ||b.Vsub<-1e-15||b.Vsub>b.V+1e-15||b.N<-1e-12) nf++;
      }
    eq(nf,0,'no combination of material, mass, volume and fluid gives an illegal state ('+n+' swept)');
    clearAll();
  }

  /* ---------- L. the drag, and the arrow scale ---------- */
  {
    const canvas={getContext:()=>makeShot(1180,740),getBoundingClientRect:()=>({left:0,top:0,width:1180,height:740}),
                  classList:{add(){},remove(){},contains(){return true;}},setPointerCapture(){}};
    const S=makeScene(canvas);
    withState({view:'explore'},()=>{
      const ctx=makeShot(S.W,S.H), M=buildModel(ST), G2=exploreGeo(ctx,S.W,S.H,M), map=G2.map, bk=M.blocks[0];
      ok(!S.pointer('down',10,10),'a pointer-down away from every block grabs nothing');
      ok(S.pointer('down',map.X(bk.x),map.Y(bk.yb+bk.s/2)),'pointer-down on block A grabs it');
      eq(DRAG.what,'A','and it is block A that is held');
      const y0=bk.yb;
      ok(S.pointer('move',map.X(bk.x),map.Y(bk.yb+bk.s/2)+40),'the move is accepted');
      close(ST.holdA,y0-40/map.s,1e-9,'the block follows the pointer, keeping the grab offset');
      MEMO.explore=null;
      const M2=buildModel(ST);
      eq(M2.blocks[0].mode,'held','the model says it is held');
      ok(M2.blocks[0].Vsub>bk.Vsub,'pushed down, it displaces more');
      ok(M2.yw>M.yw,'so the level rises');
      ok(M2.blocks[0].hand<0,'and the hand has to PUSH DOWN on a floater');
      S.pointer('move',map.X(bk.x),map.Y(bk.yb)+4000);
      close(ST.holdA,-POOL_H,1e-12,'dragged through the floor, the hold stops AT the floor');
      S.pointer('move',map.X(bk.x),map.Y(bk.yb)-4000);
      close(ST.holdA,0.30-cubeSide(0.005)-0.012,1e-15,'lifted, it stops where its top reaches the top of the world');
      close(holdCeiling(cubeSide(0.005))+cubeSide(0.005)+0.012,POOL_YTOP,1e-15,'which is what the ceiling is for');
      ok(S.pointer('up',0,0),'pointer-up releases');
      eq(ST.holdA,null,'and the block is let go');
      MEMO.explore=null;
      close(buildModel(ST).yw,M.yw,1e-12,'released, everything returns to where it was');
    });
    withState({view:'explore',where:'ground'},()=>{
      const ctx=makeShot(S.W,S.H), M=buildModel(ST), G2=exploreGeo(ctx,S.W,S.H,M), map=G2.map, bk=M.blocks[0];
      eq(bk.mode,'out','on the ground scale the block is out of the pool');
      ok(!S.pointer('down',map.X(bk.x),map.Y(bk.yb+bk.s/2)),'and cannot be grabbed out there');
      close(M.groundReads,bk.W,1e-12,'the ground scale reads its full weight');
      eq(M.poolReads,0,'and the pool scale reads nothing');
    });
    for(const v of ['sets','faces','scale','fluids'])
      withState({view:v},()=>ok(!S.pointer('down',400,300),'the '+v+' view ignores the pointer'));
    eq(S.step(),false,'nothing in this sim animates: step() never advances anything');
    /* ONE arrow scale, asserted off the model rather than off the picture */
    withState({view:'explore',two:true,matA:'aluminum',massA:13.5,volAL:5,matB:'wood',massB:2,volBL:5},()=>{
      const M=buildModel(ST), FS=forceScale(M.blocks);
      rel(M.blocks[0].W,132.3,1e-12,'block A is the heavy one');
      close(FS.Fref,132.3,1e-12,'the reference force is the LARGEST, 132.3 N');
      const A=forceLengths(M.blocks[0],FS), B=forceLengths(M.blocks[1],FS);
      rel(A.W,FS.len,1e-12,'so the heavy block gets the full-length arrow');
      rel(A.W/B.W,M.blocks[0].W/M.blocks[1].W,1e-12,'and the two are in the ratio of the weights');
      rel(A.Fb/A.W,M.blocks[0].Fb/M.blocks[0].W,1e-12,'within one block too');
      close(FS.len,0.10349879733383488,1e-15,'the arrow length IS the room the tightest block leaves (0.1035 m)');
      ok(FS.len<0.13-1e-6,'which is below the 0.13 m ceiling, so the room is doing the work');
      close(FS.len,M.blocks[0].yb+M.blocks[0].s/2-(-POOL_H-0.018),1e-15,
            '= the sunk block\u2019s centre above the floor');
      ok(holdCeiling(cubeSide(0.01))<holdCeiling(cubeSide(0.001)),'a bigger block cannot be lifted as high');
    });
  }

  /* ---------- M. layout sweep: every view drawn at four sizes ---------- */
  const SIZES=[[1400,820],[1180,740],[900,600],[620,420]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const SWEEP=[
    ['explore default',{view:'explore'},6],
    ['explore two',{view:'explore',two:true},8],
    ['explore mercury',{view:'explore',fluid:'mercury',two:true},8],
    ['explore poolscale',{view:'explore',where:'poolscale'},7],
    ['explore ground',{view:'explore',where:'ground'},7],
    ['explore held',{view:'explore',holdA:-POOL_H},6],
    ['explore no forces',{view:'explore',forces:false},6],
    ['sets mass',{view:'sets',setMode:'mass'},7],
    ['sets volume',{view:'sets',setMode:'volume'},7],
    ['sets density',{view:'sets',setMode:'density',sameRho:2500},7],
    ['faces deep',{view:'faces',facesDepth:0.6},4],
    ['faces shallow',{view:'faces',facesDepth:0.08},4],
    ['faces mercury',{view:'faces',fluid:'mercury',facesDepth:0.5},4],
    ['scale start',{view:'scale',lowered:0},5],
    ['scale mid',{view:'scale',lowered:0.6},5],
    ['scale end',{view:'scale',lowered:1,matA:'brick'},5],
    ['fluids wood',{view:'fluids'},20],
    ['fluids gold',{view:'fluids',gridMat:'gold'},20],
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
