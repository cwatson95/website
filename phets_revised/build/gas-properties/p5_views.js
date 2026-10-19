
/* ================================================================== *
 *  diffusion (PhET's Diffusion screen)                                *
 * ================================================================== */
function drawDiffusion(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g, st=M.st;
  drawScene(ctx,W,H,M,G);
  const mid=g.left+g.W/2;
  /* the centres of mass: a triangle under the box for each species */
  if(st.dCOM) for(const k of [0,1]){
    const c=M.com[k]; if(c===null) continue;
    const X=G.X(mid+c), y=G.yB+4;
    ctx.beginPath(); ctx.moveTo(X,y); ctx.lineTo(X-6,y+10); ctx.lineTo(X+6,y+10); ctx.closePath();
    ctx.fillStyle=k?COL.light:COL.heavy; ctx.fill();
  }
  /* the flow: arrows over the divider, length ~ rate (particles/ps) */
  if(st.dFlow&&!g.divided&&g.flow){
    const dx=G.X(g.dividerX);
    for(const k of [0,1]){
      const y=G.yT-12-k*12, col=k?COL.light:COL.heavy;
      for(const [rate,dir] of [[g.flow.rateL[k],-1],[g.flow.rateR[k],1]]){
        const L=Math.min(150,rate*10); if(L<1) continue;
        ctx.strokeStyle=col; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(dx,y); ctx.lineTo(dx+dir*L,y);
        ctx.moveTo(dx+dir*L,y); ctx.lineTo(dx+dir*(L-6),y-4); ctx.moveTo(dx+dir*L,y); ctx.lineTo(dx+dir*(L-6),y+4); ctx.stroke();
      }
    }
    lab(ctx,W,H,G.X(g.dividerX)+4,G.yT-38,'flow, 10 px per particle/ps',COL.dim,'10.5px -apple-system, sans-serif','left','middle');
  }
  if(G.plots.length){
    const b=G.plots[0], h=M.w.hist, half=g.W/2000;
    const hs=h.length?h:[[g.t,M.com[0],M.com[1]]];
    plotSeries(ctx,W,H,b,'centres of mass, nm from the middle (0 = mixed; ±'+fmt(half/2,0)+' nm = each half full)','centres of mass, nm',
      hs.map(r=>r[0]),[{ys:hs.map(r=>r[1]===null?NaN:r[1]/1000),col:COL.heavy},{ys:hs.map(r=>r[2]===null?NaN:r[2]/1000),col:COL.light}],
      {y0:-half/2-0.4,y1:half/2+0.4,refs:[{y:0,col:COL.ref,dash:[5,4],lw:1.2}],xlab:'t, ps',note:hs.length<2?'run the clock to trace the centres of mass':null});
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  the pressure: the momentum the walls receive                      *
 * ================================================================== */
function drawPressure(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g, P=M.pr;
  drawScene(ctx,W,H,M,G);
  const h=M.w.hist;
  if(G.plots.length){
    const b=G.plots[0], unitAtm=M.st.unitP!=='kPa', cv=v=>unitAtm?v*GAS.ATM_PER_KPA:v;
    const hs=h.length>1?h:[[0,NaN]];
    plotSeries(ctx,W,H,b,'pressure on the walls ('+(unitAtm?'atm':'kPa')+'), running average since the start','wall pressure, running',
      hs.map(r=>r[0]),[{ys:hs.map(r=>cv(r[1])),col:COL.pos}],
      {refs:[{y:cv(P.Pgauge),col:COL.ref,dash:[6,4],lw:1.3},{y:cv(P.predTh),col:COL.ref,lw:1.5}],xlab:'t, ps',x0:0,
       note:h.length<2?'run the clock: the walls start counting':null});
    lab(ctx,W,H,b.x+6,b.y+10,'gauge NkT/V dashed; ×(3/2)(W/(W−2r)) Z solid',COL.ref,'10.5px -apple-system, sans-serif','left','middle');
  }
  if(G.plots.length>1){
    const b=G.plots[1], r=g.species[0].r, a=g.W-2*r, bb=g.H-2*r;
    const xs=[], th=[], th1=[];
    for(let N=2;N<=600;N+=4){ const eta=N*Math.PI*r*r/(g.W*g.H), z1=hdZ1(N,2*r,a,bb);
      xs.push(eta); th1.push(1+z1); th.push(1+z1*(1+HD_B3_RATIO*hdB2(2*r)*N/(a*bb))); }
    const x1=0.36, y1=Math.max(2.0,(P.Zpair||1)*1.1);
    axesR(ctx,b,0,x1,0.9,y1,{title:titleFor(b,'Z = the walls’ push over the ideal 2-D gas’s, against the area fraction','Z against η'),
      xlab:'area fraction η',ylab:'Z',xticks:sparseTicks(0,x1,b.w),yticks:sparseTicks(0.9,y1,b.h),xfmt:tickFmt(0,x1,b.w),yfmt:tickFmt(0.9,y1,b.h)});
    polyline(ctx,b,[0,x1],[1,1],0,x1,0.9,y1,COL.struct,1,[4,4]);
    polyline(ctx,b,xs,th1,0,x1,0.9,y1,COL.ref,1.2,[5,4]);
    polyline(ctx,b,xs,th,0,x1,0.9,y1,COL.ref,1.6);
    if(P.Zpair!==null) marker(ctx,b,0,x1,0.9,y1,Math.min(x1,P.eta),Math.min(y1,Math.max(0.9,P.Zpair)),COL.live);
    lab(ctx,W,H,b.x+6,b.y+10,'B₂ only dashed, B₂ + B₃ solid; the ideal gas is Z = 1; the dot: this run',COL.ref,'10.5px -apple-system, sans-serif','left','middle');
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  equilibrium: from any start to Maxwell-Boltzmann                   *
 * ================================================================== */
function drawEquil(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g, h=M.w.hist;
  drawScene(ctx,W,H,M,G);
  const N=M.N;
  if(G.plots.length){
    const b=G.plots[0];
    /* the energy histogram in units of the mean: log10 of the fraction per unit */
    const kT2=N?gasEnergy(g)/N:1, xmax=6, nb=24, dw=xmax/nb, cnt=new Array(nb).fill(0);
    for(let i=0;i<g.n;i++){ if(g.out[i]) continue; const q=Math.floor(gasKE(g,i)/kT2/dw); if(q>=0&&q<nb) cnt[q]++; }
    const ylo=-3, yhi=0.5;
    axesR(ctx,b,0,xmax,ylo,yhi,{title:titleFor(b,'energy / mean energy: the fraction per unit, log scale','energy distribution (log)'),
      xlab:'E / ⟨E⟩',ylab:'density (log scale)',xticks:sparseTicks(0,xmax,b.w),yticks:[-3,-2,-1,0],xfmt:v=>fmt(v,0),yfmt:v=>v===0?'1':'10'+({'-1':'⁻¹','-2':'⁻²','-3':'⁻³'})[String(v)]});
    ctx.fillStyle='rgba(184,236,76,0.6)';
    for(let q=0;q<nb;q++){ if(!cnt[q]) continue; const d=cnt[q]/N/dw, ly=Math.log10(d);
      const Y=b.y1-b.h*(Math.min(yhi,ly)-ylo)/(yhi-ylo), X=b.x+b.w*q/nb; if(ly>ylo) ctx.fillRect(X+1,Y,b.w/nb-2,b.y1-Y); }
    const xs=[], ys=[]; for(let x=0;x<=xmax;x+=0.05){ xs.push(x); ys.push(Math.log10(Math.exp(-x))); }
    polyline(ctx,b,xs,ys,0,xmax,ylo,yhi,COL.ref,1.6);
  }
  const note=h.length<2?'run the clock':null;
  if(G.plots.length>1){
    const floor=M.eh.floor||0;
    plotSeries(ctx,W,H,G.plots[1],'Boltzmann’s H (relative entropy to e^(−E/kT₂)), with the sampling floor','Boltzmann’s H',h.map(r=>r[0]),
      [{ys:h.map(r=>r[1]===null?NaN:r[1]),col:COL.pos}],{refs:[{y:floor,col:COL.ref,dash:[5,4]}],y0:0,xlab:'t, ps',note});
  }
  if(G.plots.length>2) plotSeries(ctx,W,H,G.plots[2],'each species’ mean energy over the mean (equipartition = 1)','equipartition',h.map(r=>r[0]),
      [{ys:h.map(r=>r[2]===null?NaN:r[2]),col:COL.heavy},{ys:h.map(r=>r[3]===null?NaN:r[3]),col:COL.light}],{refs:[{y:1,col:COL.ref,dash:[5,4]}],xlab:'t, ps',note});
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='ideal') drawIdeal(ctx,W,H,M);
  else if(M.view==='explore') drawExplore(ctx,W,H,M);
  else if(M.view==='energy') drawEnergy(ctx,W,H,M);
  else if(M.view==='diffusion') drawDiffusion(ctx,W,H,M);
  else if(M.view==='pressure') drawPressure(ctx,W,H,M);
  else drawEquil(ctx,W,H,M);
}
function wallDraggable(M){ const g=M.g; return (M.view==='ideal'&&g.hold!=='volume'&&g.hold!=='pressureV')||M.view==='explore'; }
function lidDraggable(M){ const g=M.g; return BOXVIEWS[M.view]&&g.lid&&g.lid.on&&!(M.view==='ideal'&&g.hold==='temperature'); }
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of model time; false when nothing moves (paused, or the Ideal
     wall being dragged, which PhET pauses) */
  S.step=function(){
    if(!ST.running) return false;
    const w=worldOf(ST.view);
    if(ST.view==='ideal'&&w.dragW!==null) return false;
    const changed=worldStep(w,ST,viewDt(ST));
    if(changed&&S.onCounts) S.onCounts();
    return true;
  };
  /* PhET's step button: one model step of MODEL_TIME_STEP = 0.2 ps */
  S.stepOnce=function(){ const w=worldOf(ST.view); worldStep(w,ST,GAS.STEP); if(S.onCounts) S.onCounts(); };
  S.pointer=function(type,x,y){
    const M=buildModel(), w=M.w, g=M.g;
    if(type==='up'){
      const had=DRAG.what!==null;
      if(DRAG.what==='wall'&&M.view==='ideal'&&w.dragW!==null){
        gasResize(g,w.dragW,true); w.dragW=null; g.counter.on=false; gasRefresh(g);
      }
      DRAG.what=null; return had;
    }
    if(!BOXVIEWS[M.view]) return false;
    const ctx=canvas.getContext('2d'), G=viewGeo(ctx,S.W,S.H,M);
    const inR=r=>r&&x>=r.x-5&&x<=r.x+r.w+5&&y>=r.y-5&&y<=r.y+r.h+5;
    if(type==='down'){
      g.oops=null;
      if(wallDraggable(M)&&inR(G.handle)){ DRAG.what='wall'; DRAG.off=x-G.xL;
        if(M.view==='ideal') w.dragW=g.W; else ST.running=true; return true; }
      if(lidDraggable(M)&&inR(G.lidKnob)){ DRAG.what='lid'; DRAG.off=x-G.lidX; return true; }
      if(G.pumpHandle&&inR(G.pumpHandle)){ DRAG.what='pump'; DRAG.y0=y; DRAG.h0=w.pump.h; return true; }
      return false;
    }
    if(type==='move'){
      if(DRAG.what==='wall'){
        const wv=clamp(Math.round(-G.wx(x-DRAG.off)/10)*10,g.wRange[0],g.wRange[1]);
        if(M.view==='ideal') w.dragW=wv; else g.wantW=wv;
        return true;
      }
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
