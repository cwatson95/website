
/* ================================================================== *
 *  P against V — the Laws screen's gas as a point on the P-V plane    *
 * ================================================================== */
function pvRange(M){
  const g=M.g, V0=GAS.WMIN*g.H*g.D/1e9, V1=GAS.WMAX*g.H*g.D/1e9;
  let hi=Math.max(M.P,M.N&&M.T?gasPressureOf(M.N,M.T,GAS.WMIN*g.H*g.D):0);
  for(const r of M.w.trace) if(isFinite(r[4])&&r[4]>hi) hi=r[4];
  /* an empty box has no pressure at all, and auto-ranging on nothing gives a
     0.01 atm axis that means nothing: fall back to the scale the default gas
     would set, so the plane still reads as the plane */
  if(!(hi>0)) hi=gasPressureOf(100,GAS.T0,GAS.WMIN*g.H*g.D);
  return {V0,V1,P1:hi*1.15};
}
function drawPV(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  reseedTrace(M);
  drawScene(ctx,W,H,M,G);
  if(G.plots.length){
    const b=G.plots[0], g=M.g, R=pvRange(M), atm=M.st.unitP!=='kPa', cv=v=>atm?v*GAS.ATM_PER_KPA:v;
    const y1=cv(R.P1);
    axesR(ctx,b,R.V0,R.V1,0,y1,{title:titleFor(b,M.N?'the state on the pressure–volume plane, over the isotherms of these '+M.N+' disks'
        :'the pressure–volume plane — there is no gas in the box yet','P against V'),
      xlab:'V, nm³',ylab:'P, '+(atm?'atm':'kPa'),
      xticks:sparseTicks(R.V0,R.V1,b.w),yticks:sparseTicks(0,y1,b.h),
      xfmt:tickFmt(R.V0,R.V1,b.w),yfmt:tickFmt(0,y1,b.h)});
    /* the isotherms: P = NkT/V for the disks now in the box */
    if(M.N){
      for(const T of ISO_T){
        const iso=pvIsotherm(M.N,T,R.V0,R.V1,80), xs=iso.xs, ys=iso.ys.map(cv);
        polyline(ctx,b,xs,ys,R.V0,R.V1,0,y1,COL.ref,1.3);
        /* Label the isotherm where it first comes inside the box.  A hot
           isotherm may only clip the top right corner, and the label then has
           to hang to the LEFT of its entry point or it falls off the canvas —
           without that the hottest curve was drawn with no label at all. */
        let li=-1;
        for(let i=0;i<xs.length;i++) if(ys[i]<=y1*0.94){ li=i; break; }
        if(li<0) for(let i=0;i<xs.length;i++) if(ys[i]<=y1){ li=i; break; }
        if(li>=0){
          const right=li>xs.length*0.85;
          lab(ctx,W,H,b.x+b.w*(xs[li]-R.V0)/(R.V1-R.V0)+(right?-5:5),b.y1-b.h*ys[li]/y1-8,
              T+' K',COL.ref,SM_FONT,right?'right':'left','middle');
        }
      }
    }
    /* the path this gas has taken, and where it is now */
    const tr=M.w.trace.filter(r=>isFinite(r[4])&&r[4]>0);
    if(tr.length>1) polyline(ctx,b,tr.map(r=>r[3]*g.H*g.D/1e9),tr.map(r=>cv(r[4])),R.V0,R.V1,0,y1,COL.pos,1.8);
    else emptyNote(ctx,W,H,b,M.N?'run the clock, then hold something and heat or squeeze'
      :'pump some gas in, then hold something and heat or squeeze');
    if(M.N&&isFinite(M.P)) marker(ctx,b,R.V0,R.V1,0,y1,M.V,cv(M.P),COL.live);
    /* every isotherm falls from the top left to the bottom right and the 1000 K
       one clips the top right corner, so the bottom left — under the coldest
       isotherm — is the only corner that is always clear */
    keyText(ctx,W,H,b,'isotherms orange · the path green · now magenta',COL.dim,'bl');
  }
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  the four laws — swept by running the simulation                    *
 * ================================================================== */
/* the exact response the law demands at the swept value x, built from the
   base state the sweep started in (N0, T0, W0 and the pressure then) */
function sweepExactY(S,x,g){
  const V0=S.W0pm*g.H*g.D;
  if(S.law==='boyle')   return gasPressureOf(S.N0,S.T0,x*1e9);
  if(S.law==='charles') return S.N0*GAS.K*x/(S.P0/GAS.P_SCALE)/1e9;
  if(S.law==='gay')     return gasPressureOf(S.N0,x,V0);
  return (S.P0/GAS.P_SCALE)*V0/(x*GAS.K);
}
/* the state the gas is in at the swept value x: [N, T, W] */
function sweepStateAt(S,x,g){
  const V0=S.W0pm*g.H*g.D;
  if(S.law==='boyle')   return [S.N0,S.T0,x*1e9/(g.H*g.D)];
  if(S.law==='charles') return [S.N0,x,S.N0*GAS.K*x/(S.P0/GAS.P_SCALE)/(g.H*g.D)];
  if(S.law==='gay')     return [S.N0,x,S.W0pm];
  return [x,(S.P0/GAS.P_SCALE)*V0/(x*GAS.K),S.W0pm];
}
/* which corner each law's plots leave free (Boyle and Avogadro decay away from
   the top right; Charles and Gay-Lussac rise away from the top left) */
const SWEEP_KEY={boyle:'tr', avo:'tr', charles:'tl', gay:'tl'};
function sweepXRange(S,g){
  if(S.law==='boyle')   return [GAS.WMIN*g.H*g.D/1e9,GAS.WMAX*g.H*g.D/1e9];
  if(S.law==='avo')     return [S.targets[0]*0.85,S.targets[S.targets.length-1]*1.08];
  const lo=Math.min.apply(null,S.targets), hi=Math.max.apply(null,S.targets);
  return [lo-(hi-lo)*0.12,hi+(hi-lo)*0.12];
}
function drawSweep(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g, S=M.S, L=lawOf(M.st.law);
  drawScene(ctx,W,H,M,G);
  if(!G.plots.length){ sceneCaption(ctx,G); return; }
  if(!S){
    emptyPanel(ctx,W,H,G.plots[0],'press “run the sweep” to measure '+L.name+'’s law');
    if(G.plots.length>1) emptyPanel(ctx,W,H,G.plots[1],'the wall-hit rate is measured at each step');
    sceneCaption(ctx,G); return;
  }
  const atm=M.st.unitP!=='kPa', cvP=v=>atm?v*GAS.ATM_PER_KPA:v;
  const yIsP=(S.law==='boyle'||S.law==='gay');
  const cv=v=>yIsP?cvP(v):v;
  const xr=sweepXRange(S,g);
  /* ---- the law ---- */
  {
    const b=G.plots[0];
    const xs=[], ys=[];
    for(let i=0;i<=120;i++){ const x=xr[0]+(xr[1]-xr[0])*i/120; if(x<=0) continue; xs.push(x); ys.push(cv(sweepExactY(S,x,g))); }
    let lo=Infinity, hi=-Infinity;
    for(const v of ys) if(isFinite(v)){ if(v<lo) lo=v; if(v>hi) hi=v; }
    for(const p of S.pts){ const v=cv(p.y); if(v<lo) lo=v; if(v>hi) hi=v; }
    if(!(hi>lo)){ lo=0; hi=1; }
    const pad=0.10*(hi-lo), y0=Math.max(0,lo-pad), y1=hi+pad;
    const XL={boyle:'V, nm³',charles:'T, K',gay:'T, K',avo:'N, particles'}[S.law];
    const YL={boyle:'P, '+(atm?'atm':'kPa'),charles:'V, nm³',gay:'P, '+(atm?'atm':'kPa'),avo:'T, K'}[S.law];
    axesR(ctx,b,xr[0],xr[1],y0,y1,{title:titleFor(b,L.name+'’s law: the measured points on the exact line '+L.inv+' = constant',L.name+'’s law'),
      xlab:XL,ylab:YL,xticks:sparseTicks(xr[0],xr[1],b.w),yticks:sparseTicks(y0,y1,b.h),
      xfmt:tickFmt(xr[0],xr[1],b.w),yfmt:tickFmt(y0,y1,b.h)});
    polyline(ctx,b,xs,ys,xr[0],xr[1],y0,y1,COL.ref,1.8);
    for(const p of S.pts) marker(ctx,b,xr[0],xr[1],y0,y1,p.x,cv(p.y),COL.pos);
    if(!S.done&&S.targets[S.i]!==undefined){
      const xn=S.law==='boyle'?S.targets[S.i]*g.H*g.D/1e9:S.targets[S.i];
      polyline(ctx,b,[xn,xn],[y0,y1],xr[0],xr[1],y0,y1,COL.live,1,[3,4]);
    }
    /* Boyle and Avogadro fall left-to-right, Charles and Gay-Lussac rise, so
       there is no one corner that is clear for all four: put the key in the
       corner the curve is running away from. */
    keyText(ctx,W,H,b,'exact orange · measured green',COL.dim,SWEEP_KEY[S.law]);
  }
  /* ---- the wall-hit rate, which nothing defines into existence ---- */
  if(G.plots.length>1){
    const b=G.plots[1];
    const xs=[], th=[], id=[];
    for(let i=0;i<=120;i++){ const x=xr[0]+(xr[1]-xr[0])*i/120; if(x<=0) continue;
      const st2=sweepStateAt(S,x,g), c=[Math.round(st2[0]),0], rad=[g.species[0].r,g.species[1].r], ms=[g.species[0].m,g.species[1].m];
      const a=hitRateOf(c,rad,ms,st2[2],g.H,st2[1],true), bqq=hitRateOf(c,rad,ms,st2[2],g.H,st2[1],false);
      xs.push(x); th.push(a===null?NaN:a); id.push(bqq===null?NaN:bqq); }
    let lo=Infinity, hi=-Infinity;
    for(const arr of [th,id]) for(const v of arr) if(isFinite(v)){ if(v<lo) lo=v; if(v>hi) hi=v; }
    for(const p of S.pts) if(p.rate!==null){ const e=Math.sqrt(p.n)/p.t;
      if(p.rate-e<lo) lo=p.rate-e; if(p.rate+e>hi) hi=p.rate+e; }
    if(!(hi>lo)){ lo=0; hi=1; }
    const y0=Math.max(0,lo-0.12*(hi-lo)), y1=hi+0.12*(hi-lo);
    const XL={boyle:'V, nm³',charles:'T, K',gay:'T, K',avo:'N, particles'}[S.law];
    axesR(ctx,b,xr[0],xr[1],y0,y1,{title:titleFor(b,'wall hits per ps: measured (√n/t bars) against 2 n Z ⟨v⟩/π (a + b)','wall hits/ps'),
      xlab:XL,ylab:'hits/ps',xticks:sparseTicks(xr[0],xr[1],b.w),yticks:sparseTicks(y0,y1,b.h),
      xfmt:tickFmt(xr[0],xr[1],b.w),yfmt:tickFmt(y0,y1,b.h)});
    polyline(ctx,b,xs,id,xr[0],xr[1],y0,y1,COL.ref,1.2,[5,4]);
    polyline(ctx,b,xs,th,xr[0],xr[1],y0,y1,COL.ref,1.8);
    for(const p of S.pts){
      if(p.rate===null) continue;
      const e=Math.sqrt(p.n)/p.t, X=b.x+b.w*(p.x-xr[0])/(xr[1]-xr[0]);
      const Yv=v=>b.y1-b.h*(clamp(v,y0,y1)-y0)/(y1-y0);
      ctx.strokeStyle=COL.pos; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.moveTo(X,Yv(p.rate-e)); ctx.lineTo(X,Yv(p.rate+e));
      ctx.moveTo(X-4,Yv(p.rate-e)); ctx.lineTo(X+4,Yv(p.rate-e));
      ctx.moveTo(X-4,Yv(p.rate+e)); ctx.lineTo(X+4,Yv(p.rate+e)); ctx.stroke();
      marker(ctx,b,xr[0],xr[1],y0,y1,p.x,p.rate,COL.pos);
    }
    if(!S.pts.length) emptyNote(ctx,W,H,b,'counting…');
    keyText(ctx,W,H,b,'with Z solid · Z = 1 dashed',COL.ref,SWEEP_KEY[S.law]);
  }
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='intro') drawIntro(ctx,W,H,M);
  else if(M.view==='laws') drawLaws(ctx,W,H,M);
  else if(M.view==='pv') drawPV(ctx,W,H,M);
  else drawSweep(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of model time; false when nothing moves (paused, or the wall
     being dragged, which PhET pauses) */
  S.step=function(){
    if(!ST.running) return false;
    const w=worldOf(ST.view);
    if(ST.view!=='sweep'&&w.dragW!==null) return false;
    const changed=worldStep(w,ST,viewDt());
    if(changed&&S.onCounts) S.onCounts();
    return true;
  };
  /* PhET's step button: one model step of MODEL_TIME_STEP = 0.2 ps */
  S.stepOnce=function(){ const w=worldOf(ST.view); worldStep(w,ST,GAS.STEP); if(S.onCounts) S.onCounts(); };
  S.pointer=function(type,x,y){
    const M=buildModel(), w=M.w, g=M.g;
    if(type==='up'){
      const had=DRAG.what!==null;
      if(DRAG.what==='wall'&&w.dragW!==null){
        gasResize(g,w.dragW,true); w.dragW=null; g.counter.on=false; gasRefresh(g);
      }
      DRAG.what=null; return had;
    }
    const ctx=canvas.getContext('2d'), G=viewGeo(ctx,S.W,S.H,M);
    const inR=r=>r&&x>=r.x-5&&x<=r.x+r.w+5&&y>=r.y-5&&y<=r.y+r.h+5;
    if(type==='down'){
      g.oops=null;
      if(wallDraggable(M)&&inR(G.handle)){ DRAG.what='wall'; DRAG.off=x-G.xL; w.dragW=g.W; return true; }
      if(lidDraggable(M)&&inR(G.lidKnob)){ DRAG.what='lid'; DRAG.off=x-G.lidX; return true; }
      if(G.pumpHandle&&inR(G.pumpHandle)){ DRAG.what='pump'; DRAG.y0=y; DRAG.h0=w.pump.h; return true; }
      return false;
    }
    if(type==='move'){
      if(DRAG.what==='wall'){ w.dragW=clamp(Math.round(-G.wx(x-DRAG.off)/10)*10,g.wRange[0],g.wRange[1]); return true; }
      if(DRAG.what==='lid'){ gasSetLid(g,G.wx(x-DRAG.off)-(g.left-GAS.WALL)); return true; }
      if(DRAG.what==='pump'){
        /* a full stroke down pumps 50 (PhET's numberOfParticlesPerPumpAction) */
        const hNew=clamp(DRAG.h0+(y-DRAG.y0)/G.pump.travel,0,1), dh=hNew-w.pump.h;
        if(dh>0){ w.pump.acc+=dh*50; const k=Math.floor(w.pump.acc+1e-9);
          if(k>0){ w.pump.acc-=k; gasInject(g,ST.pump==='light'?1:0,k); if(!ST.running) gasRefresh(g); if(S.onCounts) S.onCounts(); } }
        w.pump.h=hNew; return true;
      }
    }
    return false;
  };
  return S;
}
