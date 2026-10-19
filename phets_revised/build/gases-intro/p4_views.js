
/* ================================================================== *
 *  this sim's scene table, its captions, and the hooks the shared     *
 *  scene layer (p4s_scene.js) asks about                              *
 * ================================================================== */
const SCENE={
  intro: {maxW:GAS.WMAX, gauges:true, pump:true, heater:true, ruler:true, nPlots:2, plotFrac:0.28},
  laws:  {maxW:GAS.WMAX, gauges:true, pump:true, heater:true, ruler:true, nPlots:2, plotFrac:0.28},
  pv:    {maxW:GAS.WMAX, gauges:true, pump:true, heater:true, ruler:true, nPlots:1, plotFrac:0.42},
  sweep: {maxW:GAS.WMAX, gauges:true, pump:false, heater:false, ruler:true, nPlots:2, plotFrac:0.40}
};
/* PhET's Intro screen has no Hold Constant panel, so its wall and lid are
   always free; on the Laws screen (and the P-V view, which is the same gas)
   PhET disables the wall when V or P↕V is held and the lid when T is held.
   The sweep drives the wall itself, so nothing there is draggable. */
function wallDraggable(M){ const g=M.g;
  return (M.view==='intro')||((M.view==='laws'||M.view==='pv')&&g.hold!=='volume'&&g.hold!=='pressureV'); }
function lidDraggable(M){ const g=M.g;
  return !!(g.lid&&g.lid.on)&&M.view!=='sweep'&&!((M.view==='laws'||M.view==='pv')&&g.hold==='temperature'); }
/* PhET pauses the Ideal screen while the wall is dragged and spreads the
   particles over the new width on release: no work is done */
function dragPauses(M){ return M.view!=='sweep'; }
function heaterLocked(M){ const g=M.g;
  return (M.view==='laws'||M.view==='pv')&&(g.hold==='temperature'||g.hold==='pressureT'); }
function scaleBar(){ return false; }          /* PhET's tick scale belongs to Diffusion */
function dividerShown(){ return false; }      /* … and so does the divider */
function rulerOn(M){ return M.st.showWidth; }
function wallVelocity(){ return false; }      /* no working wall on these screens */
function counterOn(){ return true; }

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
  const v=M.view;
  if(v==='intro') return ['Drawn to scale: the box is '+fmt(GAS.WMIN/1000,0)+'–'+fmt(GAS.WMAX/1000,0)+' nm wide, 8.75 nm tall and 4 nm deep; every disk is drawn at its true radius (heavy 125 pm, light 87.5 pm). Drag the grip on the left wall (the sim pauses, as PhET’s does), the knob on the lid, or the pump handle. The thermometer spans PhET’s 0–1000 K, the dial its 0–20,000 kPa. Left: the gauge against time. Right: the wall-hit rate the counter measures, against kinetic theory (orange, dashed without Z).',
                         'To scale; drag the wall grip, the lid knob or the pump handle.',
                         'To scale; drag the wall grip, the lid knob or the pump handle. A taller window adds the gauge and hit-rate traces.'];
  if(v==='laws') return ['The same box with PhET’s Hold Constant panel. Left: the two quantities that are free to move. Right: the one the hold is keeping still, as a departure from its value when the hold was engaged (parts per million) — flat means the controller did its job. A hold PhET cannot honour (T in an empty box, P past the container’s 5–15 nm range) drops back to Nothing and raises its Oops.',
                         'PhET’s Laws screen: hold one of P, V, T and watch the other two.',
                         'PhET’s Laws screen: hold one of P, V, T. A taller window adds the traces.'];
  if(v==='pv') return ['The same gas as the Laws screen, drawn as one point on the pressure–volume plane. The orange hyperbolas are isotherms at '+ISO_T.join(', ')+' K for the '+M.N+' disks now in the box (they move when you pump); the green line is the path this gas has actually taken, and the magenta dot is where it is. Volume is the full 3-D V = width × 8.75 nm × 4 nm, so the axis is linear in the width.',
                       'The Laws gas as a point on the P–V plane, over its isotherms.',
                       'The Laws gas on the P–V plane. A taller window draws the isotherms and the path.'];
  return ['The four named laws, measured by running this simulation. Each sweep engages PhET’s hold, steps the controlled variable to five targets, waits 2 ps, then counts wall hits for '+fmt(M.st.sWin,0)+' ps. Left: the law, measured points (green) on the exact line (orange) — exact because PhET DEFINES P = NkT/V, so what is being tested is the controller, not the law. Right: the wall-hit rate, which is not defined into existence: error bars are √n/t.',
          'The four laws, swept by the simulation: the law, and the hit rate.',
          'The four laws, swept by the simulation. A taller window adds the plots.'];
}

/* ================================================================== *
 *  the box (PhET's Intro screen) and the laws (PhET's Laws screen)    *
 * ================================================================== */
/* The seed point describes the state at t = 0, and an edit made while paused
   (a resize, the pump, erase) moves that state: re-seed it, or the lone marker
   on the plot contradicts the readout beside it.  (The same fix the
   gas-properties remake needed on its Ideal screen.) */
function reseedTrace(M){
  if(M.w.trace.length===1&&M.g.t===0){ M.w.trace.length=0; traceRecord(M.w); }
}
/* the traces, in the units the chips ask for */
function traceSeries(M){
  const st=M.st, atm=st.unitP!=='kPa', cel=st.unitT==='C';
  const t=[], P=[], T=[], V=[];
  for(const r of M.w.trace){ t.push(r[0]); T.push(cel?r[1]-273.15:r[1]); P.push(atm?r[2]*GAS.ATM_PER_KPA:r[2]); V.push(r[3]*M.g.H*M.g.D/1e9); }
  return {t,P,T,V,atm,cel};
}
function drawIntro(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  reseedTrace(M);
  drawScene(ctx,W,H,M,G);
  const S=traceSeries(M), note=S.t.length<2?'run the clock to trace it':null;
  if(G.plots.length) plotSeries(ctx,W,H,G.plots[0],'the gauge, '+(S.atm?'atm':'kPa')+' (PhET’s noise and 0.75-ps refresh)','P, '+(S.atm?'atm':'kPa'),
    S.t,[{ys:S.P,col:COL.live,lw:1.3}],{xlab:'t, ps',note});
  if(G.plots.length>1) drawHitPlot(ctx,W,H,G.plots[1],M);
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}
/* the measured wall-hit rate against kinetic theory, the one number on this
   screen that PhET's definitions do not force */
function drawHitPlot(ctx,W,H,b,M){
  const th=M.hitTh, id=M.hitId, r=M.hit;
  if(!r||r.n<1||th===null){ emptyPanel(ctx,W,H,b,'run the clock: the walls start counting'); return; }
  const hi=Math.max(th,id,r.rate+3*M.hitSd)*1.25, lo=0;
  axesR(ctx,b,0,1,lo,hi,{title:titleFor(b,'wall hits per ps: measured over the last '+fmt(r.t,1)+' ps, against kinetic theory','wall hits/ps'),
    ylab:'hits/ps',xticks:[],yticks:sparseTicks(lo,hi,b.h),xfmt:()=>'',yfmt:tickFmt(lo,hi,b.h)});
  const bar=(frac,v,col,lw,dash)=>polyline(ctx,b,[frac-0.13,frac+0.13],[v,v],0,1,lo,hi,col,lw||1.6,dash);
  bar(0.5,id,COL.ref,1.3,[5,4]);
  bar(0.5,th,COL.ref,1.8);
  /* the measurement and its Poisson error bar */
  const X=b.x+b.w*0.5, Yv=v=>b.y1-b.h*(clamp(v,lo,hi)-lo)/(hi-lo);
  ctx.strokeStyle=COL.pos; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(X,Yv(r.rate-M.hitSd)); ctx.lineTo(X,Yv(r.rate+M.hitSd));
  ctx.moveTo(X-7,Yv(r.rate-M.hitSd)); ctx.lineTo(X+7,Yv(r.rate-M.hitSd));
  ctx.moveTo(X-7,Yv(r.rate+M.hitSd)); ctx.lineTo(X+7,Yv(r.rate+M.hitSd)); ctx.stroke();
  dot(ctx,X,Yv(r.rate),5,COL.pos,'#070b18',1);
  /* clear of the bars, which span 0.37-0.63 of the box, and on a background
     patch so the bar itself does not strike the text through */
  keyAt(ctx,W,H,b.x+b.w*0.69,Yv(th),'theory, with Z',COL.ref,'left');
  keyAt(ctx,W,H,b.x+b.w*0.69,Yv(id),'Z = 1',COL.ref,'left');
  keyAt(ctx,W,H,b.x+b.w*0.31,Yv(r.rate),fmt(r.rate,2)+' ± '+fmt(M.hitSd,2),COL.pos,'right');
  keyText(ctx,W,H,b,r.n+' hits counted',COL.dim,'tl');
  /* Kinetic theory assumes the gas fills the box uniformly.  PhET's pump does
     not: it puts every new particle at one point, and until that batch has
     spread the measured rate is the rate of a clump.  Say so rather than let
     the reader think the theory is wrong. */
  if(M.hitSd&&Math.abs(r.rate-th)>3*M.hitSd)
    keyAt(ctx,W,H,b.x+6,b.y+24,titleFor(b,'measured and theory are '+fmt(Math.abs(r.rate-th)/M.hitSd,1)
      +' σ apart — the gas may not be uniform yet','not uniform yet: '+fmt(Math.abs(r.rate-th)/M.hitSd,1)+' σ'),COL.ref,'left');
}
function drawLaws(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  reseedTrace(M);
  drawScene(ctx,W,H,M,G);
  const S=traceSeries(M), g=M.g, note=S.t.length<2?'run the clock to trace it':null;
  if(G.plots.length){
    /* the two free quantities, each scaled to its own value at t = 0 so both
       fit one axis: the point of the screen is which one stays flat */
    const h=g.hold, series=[];
    const norm=arr=>{ const a=arr.find(v=>isFinite(v)&&v!==0); return a?arr.map(v=>v/a):arr; };
    const PkPa=M.w.trace.map(r=>r[4]), TT=M.w.trace.map(r=>r[1]), VV=M.w.trace.map(r=>r[3]*g.H*g.D/1e9);
    /* Each series gets its own DASH as well as its own colour, because two of
       them coincide exactly whenever a hold makes them proportional: P and T
       at held V (Gay-Lussac), T and V at held P (Charles).  Drawn solid they
       hide one another and the law becomes invisible. */
    if(h!=='pressureV'&&h!=='pressureT') series.push({ys:norm(PkPa),col:COL.live,lw:2,name:'P'});
    if(h!=='temperature') series.push({ys:norm(TT),col:COL.pos,lw:1.7,dash:[7,3],name:'T'});
    if(h!=='volume') series.push({ys:norm(VV),col:COL.struct,lw:1.5,dash:[2,4],name:'V'});
    plotSeries(ctx,W,H,G.plots[0],'the quantities that are free, each over its value at t = 0','the free quantities',
      S.t,series,{refs:[{y:1,col:COL.ref,dash:[5,4],lw:1.1}],xlab:'t, ps',note});
    const b=G.plots[0];
    let y=b.y+10;
    for(const s of series){ keyAt(ctx,W,H,b.x1-4,y,s.name,s.col,'right'); y+=13; }
    /* With P held, V/T is constant, so the two normalised curves are the SAME
       line — which is Charles's law, and worth saying rather than hiding one
       curve under the other (V is drawn dashed so both are visible). */
    const COINCIDE={pressureV:'T and V move together: that IS Charles’s law',
                    pressureT:'P and V move together at fixed T and N',
                    volume:'P and T move together: that IS Gay-Lussac’s law',
                    temperature:'P and V move oppositely: that IS Boyle’s law'};
    if(COINCIDE[h]&&series.length===2) keyText(ctx,W,H,b,COINCIDE[h],COL.dim,'tl');
    if(!series.length) emptyNote(ctx,W,H,b,'everything is held');
  }
  if(G.plots.length>1){
    const b=G.plots[1], h=g.hold;
    if(h==='nothing') emptyPanel(ctx,W,H,b,'hold one of P, V or T to watch it stay still');
    else {
      const inv=M.w.trace.map(r=>{ const V=r[3]*g.H*g.D/1e9, T=r[1], P=r[4];
        return h==='volume'?P/T:h==='temperature'?P*V:h==='pressureV'?V/T:M.N*T; });
      const base=inv.find(v=>isFinite(v)&&v!==0);
      const ppm=inv.map(v=>base?1e6*(v/base-1):NaN);
      let worst=0; for(const v of ppm) if(isFinite(v)) worst=Math.max(worst,Math.abs(v));
      /* Auto-ranging on a residual that is pure rounding gives an axis a
         thousandth of a ppm wide, whose four-decimal ticks all print as
         "-0.0000".  Below a thousandth of a ppm, fix the axis there instead:
         the trace is a flat line on zero and the ticks are readable. */
      const flat=worst<1e-4;
      plotSeries(ctx,W,H,b,'the held invariant, '+(M.inv?M.inv[0]:'')+', in parts per million of its first value','the invariant, ppm',
        S.t,[{ys:ppm,col:COL.pos}],{refs:[{y:0,col:COL.ref,dash:[5,4]}],xlab:'t, ps',note,
          y0:flat?-1e-3:undefined, y1:flat?1e-3:undefined});
      keyText(ctx,W,H,b,flat?'flat to '+worst.toExponential(1)+' ppm — the controller is exact to rounding'
        :'worst departure '+worst.toExponential(1)+' ppm (PhET rounds the held-P width to 5 decimals)',COL.dim,'tl');
    }
  }
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}
