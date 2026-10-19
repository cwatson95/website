
/* ================================================================== *
 *  the flow: the measured crossing and collision rates against theory *
 * ================================================================== */
function drawFlow(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g;
  drawScene(ctx,W,H,M,G);
  if(G.plots.length){
    const b=G.plots[0], h=M.w.hist;
    if(g.divided||!g.flow||!g.flow.dts.length){ emptyPanel(ctx,W,H,b,'take the divider out: nothing crosses while it is in'); }
    else {
      /* the four measured rates now, and the four theory values, as a
         grouped comparison against the swept side counts */
      const items=[];
      for(const k of [0,1]) for(const [dir,nm] of [[0,'→ left'],[1,'→ right']]){
        const meas=dir?g.flow.rateR[k]:g.flow.rateL[k];
        /* crossings to the right come from the LEFT side, and vice versa */
        const th=M.flowTh[k][dir?0:1];
        items.push({lab:'particle '+(k+1)+' '+nm, meas, th, col:k?COL.light:COL.heavy});
      }
      let hi=0; for(const it of items) hi=Math.max(hi,it.meas,it.th||0);
      hi=Math.max(hi*1.3,0.5);
      axesR(ctx,b,0,4,0,hi,{title:titleFor(b,'crossings per ps: measured (bars) against n ⟨vx⁺⟩ (H − 2r) (orange)','the flow rates'),
        ylab:'particles/ps',xticks:[],yticks:sparseTicks(0,hi,b.h),xfmt:()=>'',yfmt:tickFmt(0,hi,b.h)});
      items.forEach((it,i)=>{
        const x0=b.x+b.w*(i+0.18)/4, bw=b.w*0.64/4;
        const Yv=v=>b.y1-b.h*clamp(v,0,hi)/hi;
        ctx.fillStyle=rgba(it.col,0.55); ctx.fillRect(x0,Yv(it.meas),bw,b.y1-Yv(it.meas));
        if(it.th!==null){ ctx.strokeStyle=COL.ref; ctx.lineWidth=2;
          ctx.beginPath(); ctx.moveTo(x0-2,Yv(it.th)); ctx.lineTo(x0+bw+2,Yv(it.th)); ctx.stroke(); }
        lab(ctx,W,H,x0+bw/2,b.y1+11,it.lab,it.col,SM_FONT,'center','middle');
      });
      keyText(ctx,W,H,b,'300-frame average · theory from the counts on each side',COL.dim,'tl');
      /* Honest about WHY the bars and the orange marks differ while the gas is
         still settling: the bars are a 12.5-ps average of a changing state,
         and a particle that has just crossed is still beside the line and
         often crosses straight back — both push the count above the flux a
         uniform half would give. */
      keyAt(ctx,W,H,b.x+6,b.y+24,titleFor(b,'they differ while the sides are still changing (see the caption)',
        'still changing — see the caption'),COL.dim,'left');
    }
  }
  if(G.plots.length>1){
    const b=G.plots[1], P=M.pairMe;
    if(!P||P.n<1){ emptyPanel(ctx,W,H,b,'run the clock: the collisions start counting'); }
    else {
      const hi=Math.max(P.rate+3*P.sd,M.pairTh||0)*1.25;
      axesR(ctx,b,0,1,0,hi,{title:titleFor(b,'pair collisions per ps: measured over the last '+fmt(P.t,1)+' ps, against Σⱼ nⱼ 2(rᵢ+rⱼ) ⟨v_rel⟩','pair collisions/ps'),
        ylab:'collisions/ps',xticks:[],yticks:sparseTicks(0,hi,b.h),xfmt:()=>'',yfmt:tickFmt(0,hi,b.h)});
      const X=b.x+b.w*0.5, Yv=v=>b.y1-b.h*clamp(v,0,hi)/hi;
      if(M.pairTh!==null) polyline(ctx,b,[0.32,0.68],[M.pairTh,M.pairTh],0,1,0,hi,COL.ref,2);
      ctx.strokeStyle=COL.pos; ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(X,Yv(P.rate-P.sd)); ctx.lineTo(X,Yv(P.rate+P.sd));
      ctx.moveTo(X-8,Yv(P.rate-P.sd)); ctx.lineTo(X+8,Yv(P.rate-P.sd));
      ctx.moveTo(X-8,Yv(P.rate+P.sd)); ctx.lineTo(X+8,Yv(P.rate+P.sd)); ctx.stroke();
      dot(ctx,X,Yv(P.rate),5,COL.pos,'#070b18',1);
      if(M.pairTh!==null) keyAt(ctx,W,H,b.x+b.w*0.70,Yv(M.pairTh),'theory '+fmt(M.pairTh,1),COL.ref,'left');
      keyAt(ctx,W,H,b.x+b.w*0.30,Yv(P.rate),fmt(P.rate,1)+' ± '+fmt(P.sd,1),COL.pos,'right');
      keyText(ctx,W,H,b,P.n+' collisions counted',COL.dim,'tl');
      /* The theory uses the BOX-AVERAGE density n = N/WH.  While the gas is
         still bunched in one half the disks meet each other where they
         actually are, which is denser, and the measured rate runs above it —
         60 % above with one species 15 ps after the divider came out.  Say so
         rather than let the reader read it as a wrong formula. */
      if(M.pairTh&&Math.abs(P.rate-M.pairTh)>3*P.sd)
        keyAt(ctx,W,H,b.x+6,b.y+24,titleFor(b,'not uniform yet: theory uses the box-average density',
          'not uniform yet'),COL.ref,'left');
    }
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  the speeds: PhET's spike relaxing to Maxwell-Boltzmann             *
 * ================================================================== */
function drawSpeeds(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g;
  drawScene(ctx,W,H,M,G);
  if(G.plots.length){
    const b=G.plots[0], xmax=SPD_NB*SPD_BW;
    const c=[gasBinCounts(g,0,SPD_BW,SPD_NB,false),gasBinCounts(g,1,SPD_BW,SPD_NB,false)];
    let ymax=4; for(const k of [0,1]) for(const v of c[k]) if(v>ymax) ymax=v;
    ymax*=1.25;
    axesR(ctx,b,0,xmax,0,ymax,{title:titleFor(b,'speed, m/s ('+SPD_NB+' bins of '+SPD_BW+' m/s) against 2-D Maxwell–Boltzmann','the speed histograms'),
      xlab:'speed, m/s',ylab:'particles',xticks:sparseTicks(0,xmax,b.w),yticks:sparseTicks(0,ymax,b.h),
      xfmt:tickFmt(0,xmax,b.w),yfmt:v=>fmt(v,0)});
    const bw=b.w/SPD_NB;
    for(const k of [0,1]){
      ctx.fillStyle=rgba(k?COL.light:COL.heavy,0.45);
      for(let q=0;q<SPD_NB;q++){ const v=c[k][q]; if(v<=0) continue;
        const hgt=Math.min(1,v/ymax)*b.h; ctx.fillRect(b.x+q*bw+1,b.y1-hgt,bw-2,hgt); }
    }
    if(M.st.showMB) for(const k of [0,1]){
      const T=M.Tsp[k], nk=gasCount(g,k); if(T===null||!nk) continue;
      const e=mbBinCounts(nk,g.species[k].m,T), xs=[], ys=[];
      for(let q=0;q<SPD_NB;q++){ xs.push((q+0.5)*SPD_BW); ys.push(e[q]); }
      polyline(ctx,b,xs,ys,0,xmax,0,ymax,COL.ref,1.6);
    }
    keyText(ctx,W,H,b,'particle 1 blue · 2 red · Maxwell–Boltzmann orange',COL.dim,'tl');
  }
  if(G.plots.length>1){
    const b=G.plots[1], h=M.w.hist;
    const refs=[];
    for(const k of [0,1]){
      const T=M.Tsp[k]; if(T===null) continue;
      refs.push({y:mbRmsSpeed(g.species[k].m,gasKT2(T)),col:COL.ref,dash:[5,4],lw:1.2});
      refs.push({y:mbMeanSpeed(g.species[k].m,gasKT2(T)),col:COL.ref,lw:1.6});
    }
    plotSeries(ctx,W,H,b,'mean speed: from PhET’s one speed √(3kT/m) (dashed) down to ⟨v⟩ = √(πkT₂/2m) (solid)','mean speeds, m/s',
      h.map(r=>r[0]),[{ys:h.map(r=>r[7]===null?NaN:r[7]),col:COL.heavy},{ys:h.map(r=>r[8]===null?NaN:r[8]),col:COL.light}],
      {refs,y0:0,xlab:'t, ps',note:h.length<2?'run the clock':null});
    keyText(ctx,W,H,b,'√(3kT/m) dashed · ⟨v⟩ solid · the drop is √(π/4) = 0.8862',COL.ref,'ml');
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='box') drawBox(ctx,W,H,M);
  else if(M.view==='mixing') drawMixing(ctx,W,H,M);
  else if(M.view==='flow') drawFlow(ctx,W,H,M);
  else drawSpeeds(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(){
    if(!ST.running) return false;
    const changed=worldStep(worldOf(),ST,viewDt(ST));
    if(changed&&S.onCounts) S.onCounts();
    return true;
  };
  /* PhET's step button: one model step of MODEL_TIME_STEP = 0.2 ps */
  S.stepOnce=function(){ worldStep(worldOf(),ST,GAS.STEP); if(S.onCounts) S.onCounts(); };
  /* the only canvas gesture: lift the divider out (PhET's Remove Divider) */
  S.pointer=function(type,x,y){
    const M=buildModel(), w=M.w;
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; w.divLift=0; return had; }
    const ctx=canvas.getContext('2d'), G=viewGeo(ctx,S.W,S.H,M);
    const k=divKnobGeo(G,M);
    if(type==='down'){
      if(k&&x>=k.x-6&&x<=k.x+k.w+6&&y>=k.y-6&&y<=k.y+k.h+6){ DRAG.what='divider'; DRAG.y0=y; w.divLift=0; return true; }
      return false;
    }
    if(type==='move'&&DRAG.what==='divider'){
      w.divLift=clamp((DRAG.y0-y)/DIV_TRAVEL,0,1);
      if(w.divLift>=1&&M.g.divided){ removeDivider(w,ST); DRAG.what=null; w.divLift=0; }
      return true;
    }
    return false;
  };
  return S;
}
