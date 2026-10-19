
/* ================================================================== *
 *  this sim's scene table, its captions, and the hooks the shared     *
 *  scene layer (p4s_scene.js) asks about                              *
 * ================================================================== */
const SCENE={
  box:    {maxW:GAS.DIFF_W, gauges:false, pump:false, heater:false, ruler:true, nPlots:1, plotFrac:0.30, below:22},
  mixing: {maxW:GAS.DIFF_W, gauges:false, pump:false, heater:false, ruler:true, nPlots:2, plotFrac:0.40, below:22},
  flow:   {maxW:GAS.DIFF_W, gauges:false, pump:false, heater:false, ruler:true, nPlots:2, plotFrac:0.40, below:22},
  speeds: {maxW:GAS.DIFF_W, gauges:false, pump:false, heater:false, ruler:true, nPlots:2, plotFrac:0.44, below:22}
};
/* PhET's Diffusion container is fixed at 16 nm and has no lid, no pump, no
   heater and no collision counter, so every one of these is off */
function wallDraggable(){ return false; }
function lidDraggable(){ return false; }
function dragPauses(){ return false; }
function heaterLocked(){ return false; }
function scaleBar(){ return true; }          /* PhET's Scale: a tick every nm */
function dividerShown(){ return true; }      /* dashed once the divider is out */
function rulerOn(M){ return M.st.dScale; }
function wallVelocity(){ return false; }
function counterOn(){ return false; }

/* An in-plot key or annotation, painted on a patch of the canvas ground first
   so a curve or a reference line running through it does not strike it through
   (the same trick plotNote uses).  Every in-plot label in this file goes
   through it: the display-list audit cannot see a line crossing text, and the
   rasterised PNGs showed three of them doing exactly that. */
function keyAt(ctx,W,H,x,y,txt,col,align){
  const t=plain(txt), w=t.length*10.5*0.52+8, right=align==='right';
  ctx.fillStyle='#070b18';
  ctx.fillRect(right?x-w-2:x-4,y-8,w+6,16);
  return lab(ctx,W,H,x,y,txt,col,SM_FONT,right?'right':'left','middle');
}
/* `where` picks the corner (or the middle of a side) the key sits in.  It has
   to be chosen per plot: the audit compares text with text, so a key sitting
   on the first 200 px of a curve is invisible to it, and the rasterised PNGs
   showed four of them doing exactly that.  Put the key where the data is not. */
function keyText(ctx,W,H,b,txt,col,where){
  const w=where||'tl', right=w[1]==='r';
  const y=w[0]==='b'?b.y1-10:(w[0]==='m'?b.y+b.h*0.45:b.y+10);
  return keyAt(ctx,W,H,right?b.x1-4:b.x+6,y,txt,col,right?'right':'left');
}

/* An empty panel still gets its frame: emptyNote alone leaves a sentence
   floating in blank canvas, which reads as a missing view rather than as a
   chart with nothing in it yet. */
function emptyPanel(ctx,W,H,b,txt){ frame(ctx,b,'#242a3a'); emptyNote(ctx,W,H,b,txt); }

function captionFor(M){
  const v=M.view, halfNm=fmt((M.g.W/4+M.g.dividerHalf/2)/1000,3);
  if(v==='box') return ['Drawn to scale: 16 nm by 8.75 nm by 4 nm deep, every disk at its true radius; the scale bar is 1 nm a tick. Remove the divider and the species mix. The triangles under the box are each species’ centre of mass — they start at ∓'+halfNm+' nm, exactly, whatever the radius — and the arrows across the middle, inside the box, are the flow rates (particles/ps, averaged over 300 frames as PhET does). Drag the handle on top of the divider to lift it out. The plot tracks both centres of mass.',
                        'To scale; remove the divider and watch the centres of mass.',
                        'To scale; remove the divider. A taller window adds the centres-of-mass trace.'];
  if(v==='mixing') return ['Left: how many of each species are in each of '+NPROF+' slices along the box, against the flat profile a fully mixed gas would have (orange). Right: the left–right imbalance ΔN/N falling with time, between the two limits that bracket it — the effusion model (orange, dashed), which assumes each half stays internally mixed, and the Fickian estimate (orange, solid) from D ≈ ⟨v⟩λ/2, which is an order-of-magnitude bound, not a prediction.',
                           'The concentration profiles and the imbalance, between its two limits.',
                           'To scale. A taller window adds the profiles and the imbalance.'];
  if(v==='flow') return ['Left: the measured crossing rate of each species each way (bars, blue and red), against the kinetic-theory flux n⟨vx⁺⟩(H − 2r) built from the counts on each side right now (orange). Expect them to differ while the gas is still settling, for two reasons: the bars are a 300-frame (12.5 ps) average of a state that is still changing, and a particle that has just crossed the line is still beside it and often crosses straight back, so the count exceeds the flux a uniform half would give. Right: the pair-collision rate against Σⱼ nⱼ 2(rᵢ+rⱼ)⟨v_rel⟩, with its √n counting error — and that uses the box-average density, so it too reads low while the gas is still bunched in one half. Nothing here is defined into existence: these are the numbers kinetic theory has to get right once the gas has spread.',
                         'The measured flow and collision rates against kinetic theory.',
                         'To scale. A taller window adds the flow and collision-rate comparisons.'];
  return ['PhET starts every particle at exactly √(3kT/m) — a spike, not a distribution. Left: the two species’ speed histograms ('+SPD_NB+' bins of '+SPD_BW+' m/s) with the 2-D Maxwell–Boltzmann counts at each species’ own measured temperature (orange). Right: the mean speeds against time, with the starting √(3kT/m) (dashed) and the Maxwell–Boltzmann ⟨v⟩ = √(πkT₂/2m) (solid) — the drop between them is exactly √(π/4) = 0.8862, at constant energy.',
          'The spike relaxing to Maxwell–Boltzmann, and the 11.38 % drop in ⟨v⟩.',
          'To scale. A taller window adds the speed histograms and the mean speeds.'];
}

/* ================================================================== *
 *  the divided box (PhET's Diffusion screen)                          *
 * ================================================================== */
/* PhET's container has nothing to drag — the width is fixed, there is no lid
   and no pump — so the only gesture here is PhET's own Remove Divider, given
   as a handle on top of the divider.  Lifting it the full travel takes the
   divider out; anything less snaps back.  The BAR is never drawn short while
   it is still in the model: a gap the particles do not use would be a lie. */
/* The handle sits just INSIDE the top of the container and lifts to just
   above it.  It cannot start higher: the scene begins at stageTop() + 30 and
   the tab bar owns everything above stageTop(), so 34 px is all the travel
   there is without drawing under the tabs. */
const DIV_TRAVEL=34;
function divKnobGeo(G,M){
  if(!M.g.divided) return null;
  const x=G.X(M.g.dividerX), lift=(M.w.divLift||0)*DIV_TRAVEL;
  return {x:x-16,y:G.yT+4-lift,w:32,h:12,cx:x,lift};
}
function drawDivKnob(ctx,W,H,G,M){
  const k=divKnobGeo(G,M); if(!k) return;
  ctx.strokeStyle='#5a6782'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(k.cx,G.yT+16); ctx.lineTo(k.cx,k.y+k.h); ctx.stroke();
  ctx.fillStyle=DRAG.what==='divider'?COL.live:'#b8c4d8'; ctx.fillRect(k.x,k.y,k.w,k.h);
  keyAt(ctx,W,H,k.x+k.w+6,k.y+k.h/2,k.lift>1?'lift it out ('+fmt(100*(M.w.divLift||0),0)+' %)':'drag me up',
        k.lift>1?COL.live:COL.dim,'left');
}
function drawBox(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g, st=M.st;
  drawScene(ctx,W,H,M,G);
  drawDivKnob(ctx,W,H,G,M);
  const mid=g.left+g.W/2;
  /* the centres of mass: a triangle under the box for each species */
  if(st.dCOM) for(const k of [0,1]){
    const c=M.com[k]; if(c===null) continue;
    const X=G.X(mid+c), y=G.yB+4;
    ctx.beginPath(); ctx.moveTo(X,y); ctx.lineTo(X-6,y+10); ctx.lineTo(X+6,y+10); ctx.closePath();
    ctx.fillStyle=k?COL.light:COL.heavy; ctx.fill();
  }
  /* The flow arrows: INSIDE the top of the box, not above it.  The scene
     starts at stageTop() + 30 and the tab bar owns everything above
     stageTop(), so arrows drawn over the container land under the tabs — the
     rasterised PNG showed them at y = 36 with the box top at 72. */
  if(st.dFlow&&!g.divided&&g.flow){
    const dx=G.X(g.dividerX);
    for(const k of [0,1]){
      const y=G.yT+14+k*13, col=k?COL.light:COL.heavy;
      for(const [rate,dir] of [[g.flow.rateL[k],-1],[g.flow.rateR[k],1]]){
        const L=Math.min(150,rate*10); if(L<1) continue;
        ctx.strokeStyle=col; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(dx,y); ctx.lineTo(dx+dir*L,y);
        ctx.moveTo(dx+dir*L,y); ctx.lineTo(dx+dir*(L-6),y-4); ctx.moveTo(dx+dir*L,y); ctx.lineTo(dx+dir*(L-6),y+4); ctx.stroke();
      }
    }
    keyAt(ctx,W,H,dx+8,G.yT+42,'flow, 10 px per particle/ps',COL.dim,'left');
  }
  if(G.plots.length){
    const b=G.plots[0], h=M.w.hist, half=(g.W/4+g.dividerHalf/2)/1000;
    plotSeries(ctx,W,H,b,'centres of mass, nm from the middle (0 = mixed; ∓'+fmt(half,3)+' nm = each half full)','centres of mass, nm',
      h.map(r=>r[0]),[{ys:h.map(r=>r[1]===null?NaN:r[1]/1000),col:COL.heavy},{ys:h.map(r=>r[2]===null?NaN:r[2]/1000),col:COL.light}],
      {y0:-half-0.5,y1:half+0.5,refs:[{y:0,col:COL.ref,dash:[5,4],lw:1.2},{y:-half,col:COL.ref,dash:[2,4],lw:1},{y:half,col:COL.ref,dash:[2,4],lw:1}],
       xlab:'t, ps',note:h.length<2?'run the clock to trace the centres of mass':null});
    /* the two traces start at the TOP and BOTTOM of this plot and converge on
       zero, so the only clear place is the middle, where the orange reference
       runs — and covering a reference is what plotNote already does */
    keyText(ctx,W,H,b,'particle 1 blue · particle 2 red',COL.dim,'ml');
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  the mixing: the profiles, and the imbalance between its two limits *
 * ================================================================== */
function drawMixing(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M), g=M.g;
  drawScene(ctx,W,H,M,G);
  if(G.plots.length){
    const b=G.plots[0], pr=profile(g);
    /* 1.35, not 1.2: the key sits in the top left and the profile can reach
       11 of 12 slices' worth in a half-mixed state */
    const nMax=Math.max(4,Math.max.apply(null,pr[0].concat(pr[1])))*1.35;
    axesR(ctx,b,0,g.W/1000,0,nMax,{title:titleFor(b,'how many of each species in each of '+NPROF+' slices, against a flat profile','the concentration profile'),
      xlab:'x across the box, nm',ylab:'particles per slice',
      xticks:sparseTicks(0,g.W/1000,b.w),yticks:sparseTicks(0,nMax,b.h),
      xfmt:tickFmt(0,g.W/1000,b.w),yfmt:v=>fmt(v,0)});
    const step=(arr,col)=>{ const xs=[],ys=[];
      for(let q=0;q<NPROF;q++){ xs.push(q*g.W/1000/NPROF,(q+1)*g.W/1000/NPROF); ys.push(arr[q],arr[q]); }
      polyline(ctx,b,xs,ys,0,g.W/1000,0,nMax,col,1.6); };
    step(pr[0],COL.heavy); step(pr[1],COL.light);
    for(const k of [0,1]){ const n=gasCount(g,k); if(!n) continue;
      polyline(ctx,b,[0,g.W/1000],[n/NPROF,n/NPROF],0,g.W/1000,0,nMax,COL.ref,1.2,[5,4]); }
    /* the divider line, so the profile can be read against the box above it */
    polyline(ctx,b,[g.W/2000,g.W/2000],[0,nMax],0,g.W/1000,0,nMax,COL.struct,1,[3,4]);
    keyText(ctx,W,H,b,'flat orange = fully mixed',COL.ref,'tl');
  }
  if(G.plots.length>1){
    const b=G.plots[1], h=M.w.hist;
    const t1=Math.max(1,h.length?h[h.length-1][0]:1);
    const xs=[], eff=[[],[]], dif=[[],[]];
    for(let i=0;i<=120;i++){ const t=t1*i/120; xs.push(t);
      for(const k of [0,1]){
        eff[k].push(M.tauEff[k]?Math.exp(-t/M.tauEff[k]):NaN);
        dif[k].push(M.tauDif[k]?Math.exp(-t/M.tauDif[k]):NaN); } }
    const y0=-0.25, y1=1.08;
    axesR(ctx,b,0,t1,y0,y1,{title:titleFor(b,'the left–right imbalance ΔN/N, between free flight and Fickian diffusion','the imbalance ΔN/N'),
      xlab:'t, ps',ylab:'ΔN / N',xticks:sparseTicks(0,t1,b.w),yticks:sparseTicks(y0,y1,b.h),
      xfmt:tickFmt(0,t1,b.w),yfmt:tickFmt(y0,y1,b.h)});
    polyline(ctx,b,[0,t1],[0,0],0,t1,y0,y1,COL.struct,1,[4,4]);
    polyline(ctx,b,xs,eff[0].map(Math.abs),0,t1,y0,y1,COL.ref,1.3,[5,4]);
    polyline(ctx,b,xs,dif[0].map(Math.abs),0,t1,y0,y1,COL.ref,1.7);
    if(h.length>1){
      polyline(ctx,b,h.map(r=>r[0]),h.map(r=>r[3]===null?NaN:Math.abs(r[3])),0,t1,y0,y1,COL.heavy,1.7);
      polyline(ctx,b,h.map(r=>r[0]),h.map(r=>r[4]===null?NaN:Math.abs(r[4])),0,t1,y0,y1,COL.light,1.7);
    } else emptyNote(ctx,W,H,b,'take the divider out and run the clock');
    /* every curve here starts at 1 (top left) and decays, so the bottom left
       is the one corner nothing passes through */
    keyText(ctx,W,H,b,'effusion dashed · Fickian solid (particle 1)',COL.ref,'bl');
  }
  sceneCaption(ctx,G);
}
