
/* ================================================================== *
 *  the container scene: one layout shared by the drawing and the      *
 *  pointer (the handles), the box to scale, the instruments           *
 * ================================================================== */
const SCENE={
  ideal:   {maxW:GAS.WMAX, gauges:true, pump:true, heater:true, ruler:true, nPlots:2, plotFrac:0.28},
  explore: {maxW:GAS.WMAX, gauges:true, pump:true, heater:true, ruler:true, nPlots:2, plotFrac:0.32},
  energy:  {maxW:GAS.WDEF, gauges:true, pump:true, heater:true, ruler:true, nPlots:2, plotFrac:0.44},
  diffusion:{maxW:GAS.DIFF_W, gauges:false, pump:false, heater:false, ruler:true, nPlots:1, plotFrac:0.28, below:22},
  pressure:{maxW:GAS.WDEF, gauges:false, pump:false, heater:false, ruler:false, nPlots:2, plotFrac:0.46},
  equil:   {maxW:GAS.WDEF, gauges:false, pump:false, heater:false, ruler:false, nPlots:3, plotFrac:0.50}
};
const CAPS={};
/* the house #hint is HTML (bottom: 11px, 11px type) over the canvas's bottom
   left corner, and the capture cannot see it: every caption here ends HINT_H
   higher, clear of it (the trap the wave-on-a-string build found) */
const HINT_H=18;
function viewGeo(ctx,W,H,M){
  const o=SCENE[M.view], g=M.g, narrow=isNarrow(W);
  const Lx=24, Rres=narrow?16:RO_W+34;
  const cap=captionFor(M);
  /* a scene with its gauges needs ~300 px above the caption, or it takes the
     short caption (the narrow-stage rule: the long caption must not squeeze the
     box until its instruments hang off the canvas) */
  let fit=fitCaption(ctx,W,H-HINT_H,cap[0],cap[1],W-Lx-Rres,stageTop()+(o.gauges?330:230));
  const top=stageTop()+(o.gauges?102:30);
  const nP=narrow?Math.min(1,o.nPlots):o.nPlots;
  /* the caption must describe what is drawn: when the plots do not fit, the
     no-plots caption says what a taller window adds */
  if(nP>0&&!(fit.capY-top>300)){ const c=capFit(ctx,W,H-HINT_H,cap[2],fit.capW); fit={capY:c.capY,txt:cap[2],capW:fit.capW}; }
  let sceneBottom=fit.capY-14, plots=[];
  if(nP>0&&fit.capY-top>300){
    const rowH=Math.max(130,Math.floor((fit.capY-top)*o.plotFrac));
    const rowTop=fit.capY-16-rowH;
    const right=(rowTop<480&&!narrow)?W-Rres:W-26, span=right-Lx, gut=58, pw=(span-gut*nP)/nP;
    for(let i=0;i<nP;i++) plots.push(box(Lx+gut+i*(pw+gut),rowTop+28,pw,rowH-28-40));
    sceneBottom=rowTop-6;
  }
  const below=(o.ruler?26:6)+(o.heater?44:0)+(o.below||0);
  const pumpW=o.pump?84:10;
  const availW=Math.max(60,W-Lx-Rres-pumpW), availH=Math.max(40,sceneBottom-below-top);
  const s=Math.max(0.002,Math.min(availW/o.maxW,availH/g.H));
  /* the instruments hang left of the right wall: keep 170 px for them */
  const xR=Lx+Math.max(o.maxW*s,o.gauges?170:0), yB=top+g.H*s;
  const G={s, xR, yT:top, yB, X:x=>xR+x*s, Y:y=>yB-y*s, wx:X=>(X-xR)/s, wy:Y=>(yB-Y)/s, narrow};
  const wDraw=(M.view==='ideal'&&M.w.dragW!==null)?M.w.dragW:g.W;
  G.xL=xR-wDraw*s; G.wDraw=wDraw;
  G.handle={x:G.xL-16,y:(top+yB)/2-22,w:11,h:44};
  if(g.lid&&g.lid.on){ const oL=g.left-GAS.WALL+g.lid.width; G.lidX=G.X(oL); G.lidKnob={x:G.X(oL)-30,y:top-15,w:26,h:11}; }
  if(o.pump){
    const bh=Math.min(150,Math.max(60,0.55*(yB-top))), bx=xR+34;
    G.pump={x:bx,y:yB-bh,w:24,h:bh,travel:0.55*bh};
    const hy=G.pump.y-10-G.pump.travel*(1-M.w.pump.h);
    G.pumpHandle={x:bx-16,y:hy-8,w:56,h:10};
  }
  if(o.gauges){
    G.gauge={cx:xR-40,cy:top-52,R:Math.min(34,0.45*(top-stageTop()-20))};
    G.thermo={x:xR-128,yb:top-8,h:Math.min(74,top-stageTop()-26)};
  }
  if(o.heater) G.heater={x:G.X(-GAS.WMIN)+8,y:yB+(o.ruler?26:8),w:GAS.WMIN*s-16,h:30};
  G.plots=plots; G.capY=fit.capY; G.capTxt=fit.txt; G.capW=fit.capW; G.Lx=Lx;
  return G;
}
function captionFor(M){
  const v=M.view;
  if(v==='ideal') return ['Drawn to scale: the box is '+fmt(GAS.WMIN/1000,0)+'–'+fmt(GAS.WMAX/1000,0)+' nm wide, 8.75 nm tall and 4 nm deep; every disk is drawn at its true radius (heavy 125 pm, light 87.5 pm). Drag the grip on the left wall (the sim pauses, as PhET’s does), the knob on the lid, or the pump handle. The thermometer spans PhET’s 0–1000 K; the dial its 0–20,000 kPa, past which the lid blows off.',
                         'To scale; drag the wall grip, the lid knob or the pump handle.',
                         'To scale; drag the wall grip, the lid knob or the pump handle. A taller window adds the P and T traces.'];
  if(v==='explore') return ['Drawn to scale. Here the left wall does work: drag its grip and it follows at no more than the speed limit (PhET’s is 800 m/s, faster than sound in the heavy gas), bouncing each disk it meets elastically (v′ = 2u − v); the magenta arrow is its velocity, 0.12 px per m/s. Left: T against the width since the push began, with the adiabat of these hard disks (orange) and of points, T·w = const (dashed). Right: T over the hard-disk adiabat — 1 when the push is slow enough to be reversible.',
                            'To scale; the wall does work (v′ = 2u − v). Left: T against w with the adiabats; right: T over the hard-disk adiabat.',
                            'To scale; the wall does work (v′ = 2u − v). A taller window adds the adiabat plots.'];
  if(v==='energy') return ['PhET’s histograms: 19 bins (170 m/s, 1.33 zJ wide), each count averaged over 1 ps of frames. Bars are all the particles; the outlines are the heavy and light alone; the orange curves are the 2-D Maxwell–Boltzmann counts N·P(bin) at the thermometer’s temperature, kT₂ = (3/2)kT.',
                           'PhET’s 1-ps histograms against 2-D Maxwell–Boltzmann (orange).',
                           'To scale. A taller window adds PhET’s speed and energy histograms.'];
  if(v==='diffusion') return ['Drawn to scale: 16 nm by 8.75 nm; the scale bar is 1 nm a tick. Remove the divider and the species mix; the triangles under the box are each species’ centre of mass, the arrows over the divider its flow rate (particles/ps, 300-frame average). The plot tracks both centres of mass.',
                              'To scale; remove the divider and watch the centres of mass.',
                              'To scale; remove the divider. A taller window adds the centres-of-mass trace.'];
  if(v==='pressure') return ['Each wall hit delivers 2m v⊥; summed over time and divided by the wall’s area (its height × PhET’s 4-nm depth) it is the pressure the wall feels. Left: that running average against PhET’s gauge NkT/V (orange, dashed) and the kinetic-theory value (orange). Right: Z = the measured push over the ideal 2-D gas’s, against the exact hard-disk virial series.',
                             'Wall pressure: measured (green) vs PhET’s gauge and kinetic theory (orange).',
                             'The walls count momentum. A taller window adds the wall-pressure and Z plots; the readout has the numbers.'];
  return ['Left: the energy histogram (all disks, fraction per zJ, log scale) against the Boltzmann law e^(−E/kT₂) (orange). Middle: Boltzmann’s H, the relative entropy of that histogram, with its sampling floor (K−1)/2N. Right: each species’ mean energy over the mean — equipartition when both reach 1.',
          'Relaxation to Maxwell–Boltzmann and equipartition.',
          'A taller window adds the energy law, Boltzmann’s H and equipartition; the readout has the numbers.'];
}

/* ---- the container ------------------------------------------------------------ */
function drawContainer(ctx,G,M){
  const g=M.g, s=G.s, wt=Math.max(2,GAS.WALL*s);
  /* the interior */
  ctx.fillStyle=COL.box; ctx.fillRect(G.xL,G.yT,G.xR-G.xL,G.yB-G.yT);
  ctx.strokeStyle=COL.wall; ctx.lineWidth=wt; ctx.lineCap='square';
  /* left wall, floor, right wall */
  ctx.beginPath(); ctx.moveTo(G.xL-wt/2,G.yT); ctx.lineTo(G.xL-wt/2,G.yB+wt/2); ctx.lineTo(G.xR+wt/2,G.yB+wt/2); ctx.lineTo(G.xR+wt/2,G.yT); ctx.stroke();
  /* the top: the lid over [left, openingLeft], the rest open to the right inset */
  if(g.lid){
    if(g.lid.on){
      const lt=Math.max(3,GAS.LID_THICK*s);
      ctx.fillStyle=COL.lid; ctx.fillRect(G.xL-wt,G.yT-lt,G.lidX-G.xL+wt,lt);
    }
    /* the fixed part of the top between the opening and the right wall */
    ctx.beginPath(); ctx.moveTo(G.X(gasOpenRight()),G.yT-wt/2); ctx.lineTo(G.xR+wt/2,G.yT-wt/2); ctx.stroke();
  } else { ctx.beginPath(); ctx.moveTo(G.xL-wt/2,G.yT-wt/2); ctx.lineTo(G.xR+wt/2,G.yT-wt/2); ctx.stroke(); }
  if(g.divided||M.view==='diffusion'){
    const dx=G.X(g.dividerX), dw=Math.max(2,GAS.DIVIDER*s);
    if(g.divided){ ctx.fillStyle=COL.wall; ctx.fillRect(dx-dw/2,G.yT,dw,G.yB-G.yT); }
    else { ctx.strokeStyle='rgba(90,200,224,0.35)'; ctx.lineWidth=1; ctx.setLineDash([4,5]); ctx.beginPath(); ctx.moveTo(dx,G.yT); ctx.lineTo(dx,G.yB); ctx.stroke(); ctx.setLineDash([]); }
  }
  ctx.lineCap='butt';
}
function drawParticles(ctx,G,g,dim){
  for(const k of [0,1]){
    const R=Math.max(1.3,g.species[k].r*G.s);
    ctx.beginPath(); let any=false;
    for(let i=0;i<g.n;i++){ if(g.sp[i]!==k) continue;
      const X=G.X(g.x[i]), Y=G.Y(g.y[i]); ctx.moveTo(X+R,Y); ctx.arc(X,Y,R,0,TAU); any=true; }
    if(any){ ctx.globalAlpha=dim?0.5:1; ctx.fillStyle=k?COL.light:COL.heavy; ctx.fill(); ctx.globalAlpha=1; }
  }
}
function drawHandles(ctx,G,M){
  const g=M.g, v=M.view;
  const wallOK=(v==='ideal'&&g.hold!=='volume'&&g.hold!=='pressureV')||v==='explore';
  if(wallOK){ const h=G.handle; ctx.fillStyle=DRAG.what==='wall'?COL.live:'#8a97ad'; ctx.fillRect(h.x,h.y,h.w,h.h);
    ctx.strokeStyle='#070b18'; ctx.lineWidth=1; for(let q=1;q<4;q++){ ctx.beginPath(); ctx.moveTo(h.x+2,h.y+q*h.h/4); ctx.lineTo(h.x+h.w-2,h.y+q*h.h/4); ctx.stroke(); } }
  const lidOK=g.lid&&g.lid.on&&!(v==='ideal'&&g.hold==='temperature');
  if(lidOK){ const k=G.lidKnob; ctx.fillStyle=DRAG.what==='lid'?COL.live:'#b8c4d8'; ctx.fillRect(k.x,k.y,k.w,k.h); }
}
function drawPump(ctx,G,M){
  const P=G.pump, H=G.pumpHandle, k=M.st.pump==='light'?1:0;
  /* the hose, from the pump's foot into the right wall at the entry height */
  const ey=G.Y(GAS.ENTRY_Y);
  ctx.strokeStyle='#6b7690'; ctx.lineWidth=4; ctx.beginPath(); ctx.moveTo(P.x+P.w/2,P.y+P.h); ctx.lineTo(P.x+P.w/2,P.y+P.h+8);
  ctx.lineTo(G.xR+18,P.y+P.h+8); ctx.lineTo(G.xR+18,ey); ctx.lineTo(G.xR+3,ey); ctx.stroke();
  ctx.fillStyle='#2a3346'; ctx.fillRect(P.x,P.y,P.w,P.h);
  ctx.strokeStyle='#5a6782'; ctx.lineWidth=1; ctx.strokeRect(P.x+0.5,P.y+0.5,P.w-1,P.h-1);
  /* the shaft and the handle */
  ctx.fillStyle='#8a97ad'; ctx.fillRect(P.x+P.w/2-2,H.y+H.h,4,Math.max(0,P.y-H.y-H.h));
  ctx.fillStyle=DRAG.what==='pump'?COL.live:'#b8c4d8'; ctx.fillRect(H.x,H.y,H.w,H.h);
  /* the species it pumps */
  dot(ctx,P.x+P.w/2,P.y+P.h-14,6,k?COL.light:COL.heavy,'#070b18',1);
}
function drawThermometer(ctx,G,M,W,H){
  const t=G.thermo, g=M.g, T=g.T;
  const f=T===null?0:Math.min(1,Math.max(0,T/1000));
  ctx.fillStyle='#1b2130'; ctx.fillRect(t.x-5,t.yb-t.h,10,t.h);
  ctx.fillStyle=COL.heat; ctx.fillRect(t.x-3,t.yb-f*(t.h-4),6,f*(t.h-4));
  dot(ctx,t.x,t.yb,7,COL.heat,'#5a6782',1);
  ctx.strokeStyle='#5a6782'; ctx.lineWidth=1; ctx.strokeRect(t.x-5.5,t.yb-t.h-0.5,11,t.h);
  lab(ctx,W,H,t.x-12,t.yb-t.h/2,fmtT(T,M.st),COL.pos,'11px -apple-system, sans-serif','right','middle');
}
function drawGauge(ctx,G,M,W,H){
  const d=G.gauge, g=M.g, a0=0.75*PI, a1=2.25*PI;
  ctx.beginPath(); ctx.arc(d.cx,d.cy,d.R,0,TAU); ctx.fillStyle='#10141f'; ctx.fill(); ctx.strokeStyle='#5a6782'; ctx.lineWidth=1.5; ctx.stroke();
  ctx.beginPath(); ctx.arc(d.cx,d.cy,d.R-4,a0,a1); ctx.strokeStyle='#2a3346'; ctx.lineWidth=3; ctx.stroke();
  for(let q=0;q<=4;q++){ const a=a0+(a1-a0)*q/4; ctx.beginPath(); ctx.moveTo(d.cx+(d.R-9)*Math.cos(a),d.cy+(d.R-9)*Math.sin(a));
    ctx.lineTo(d.cx+(d.R-3)*Math.cos(a),d.cy+(d.R-3)*Math.sin(a)); ctx.strokeStyle='#8b93a6'; ctx.lineWidth=1; ctx.stroke(); }
  const f=Math.min(1,Math.max(0,(g.pOn?g.gaugeP:0)/GAS.P_MAX)), a=a0+(a1-a0)*f;
  ctx.beginPath(); ctx.moveTo(d.cx,d.cy); ctx.lineTo(d.cx+(d.R-7)*Math.cos(a),d.cy+(d.R-7)*Math.sin(a)); ctx.strokeStyle=COL.live; ctx.lineWidth=2; ctx.stroke();
  /* the pipe down to the box */
  ctx.fillStyle='#3a4458'; ctx.fillRect(d.cx-3,d.cy+d.R,6,Math.max(0,G.yT-d.cy-d.R-4));
  lab(ctx,W,H,d.cx+d.R+6,d.cy,g.pOn?fmtP(g.gaugeP,M.st):'—',COL.pos,'11px -apple-system, sans-serif','left','middle');
}
function drawHeater(ctx,G,M,W,H){
  const h=G.heater, a=M.st.heat, g=M.g;
  const locked=M.view==='ideal'&&(g.hold==='temperature'||g.hold==='pressureT');
  ctx.fillStyle='#161c2a'; ctx.fillRect(h.x,h.y,h.w,h.h);
  if(a!==0&&!locked){ ctx.globalAlpha=Math.min(1,0.25+0.75*Math.abs(a)); ctx.fillStyle=a>0?COL.heat:COL.cool; ctx.fillRect(h.x+3,h.y+3,h.w-6,h.h-6); ctx.globalAlpha=1; }
  ctx.strokeStyle='#5a6782'; ctx.lineWidth=1; ctx.strokeRect(h.x+0.5,h.y+0.5,h.w-1,h.h-1);
  const txt=locked?(h.w>130?'held by the model':'held'):(a>0?'heating':(a<0?'cooling':(h.w>150?'heat / cool (the panel)':'heat / cool')));
  lab(ctx,W,H,h.x+h.w/2,h.y+h.h/2,txt,a!==0&&!locked?'#070b18':COL.dim,'10.5px -apple-system, sans-serif','center','middle');
}
function drawRuler(ctx,G,M,W,H){
  const y=G.yB+(M.view==='diffusion'?22:14), g=M.g;
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1;
  if(M.view==='diffusion'){
    /* PhET's Scale: a bar with a tick every nanometre */
    ctx.beginPath(); ctx.moveTo(G.xL,y); ctx.lineTo(G.xR,y);
    for(let x=0;x>=-g.W-1e-6;x-=1000){ ctx.moveTo(G.X(x),y-4); ctx.lineTo(G.X(x),y+(x%5000===0?5:2)); }
    ctx.stroke(); lab(ctx,W,H,G.xL,y+11,'1 nm per tick',COL.dim,'10.5px -apple-system, sans-serif','left','middle');
    return;
  }
  ctx.beginPath(); ctx.moveTo(G.xL,y); ctx.lineTo(G.xR,y);
  ctx.moveTo(G.xL,y-5); ctx.lineTo(G.xL,y+5); ctx.moveTo(G.xR,y-5); ctx.lineTo(G.xR,y+5); ctx.stroke();
  lab(ctx,W,H,(G.xL+G.xR)/2,y+10,fmt(G.wDraw/1000,2)+' nm',COL.struct,'11px -apple-system, sans-serif','center','middle');
}
function drawTools(ctx,G,M,W,H){
  const st=M.st, g=M.g; let x=G.Lx, y=stageTop()+6;
  if(st.showWatch){
    ctx.fillStyle='#10141f'; ctx.fillRect(x,y,118,30); ctx.strokeStyle='#3a4458'; ctx.lineWidth=1; ctx.strokeRect(x+0.5,y+0.5,117,29);
    lab(ctx,W,H,x+8,y+15,fmt(g.watch.t,2)+' ps',g.watch.on?COL.live:'#cfd4de','12px "SF Mono", Menlo, monospace','left','middle');
    x+=128;
  }
  if(st.showCounter&&M.view!=='energy'){
    ctx.fillStyle='#10141f'; ctx.fillRect(x,y,150,30); ctx.strokeStyle='#3a4458'; ctx.lineWidth=1; ctx.strokeRect(x+0.5,y+0.5,149,29);
    const f=g.counter.t/g.counter.period;
    ctx.fillStyle=COL.pos; ctx.fillRect(x+3,y+25,Math.max(0,144*f),3);
    lab(ctx,W,H,x+8,y+12,g.counter.count+' wall hits',g.counter.on?COL.live:'#cfd4de','12px "SF Mono", Menlo, monospace','left','middle');
  }
}
function oopsGeo(ctx,G,M){
  if(!M.g.oops) return null;
  const txt=GAS_OOPS[M.g.oops]||M.g.oops, w=Math.max(160,Math.min(360,G.xR-G.xL-20)), ls=wrapText(ctx,txt,w-24,'12px -apple-system, sans-serif');
  const bh=ls.length*16+18, bx=(G.xL+G.xR)/2-w/2, by=Math.max(stageTop(),(G.yT+G.yB)/2-bh/2);
  return {w,ls,bh,bx,by};
}
function drawOops(ctx,G,M,W,H){
  const O=oopsGeo(ctx,G,M); if(!O) return;
  const {w,ls,bh,bx,by}=O;
  ctx.fillStyle='rgba(10,12,18,.92)'; ctx.fillRect(bx,by,w,bh); ctx.strokeStyle=COL.ref; ctx.lineWidth=1.5; ctx.strokeRect(bx,by,w,bh);
  ctx.fillStyle=COL.ref; ctx.font='12px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='top';
  ls.forEach((l,i)=>ctx.fillText(l,bx+w/2,by+9+i*16));
}
function drawWallVelocity(ctx,G,M){
  const u=M.g.u; if(!M.st.showWallVel||u===0) return;
  const y=(G.yT+G.yB)/2, L=Math.max(-120,Math.min(120,u*0.12));
  const X0=G.xL, X1=G.xL+L;
  ctx.strokeStyle=COL.live; ctx.lineWidth=2.5; ctx.beginPath(); ctx.moveTo(X0,y); ctx.lineTo(X1,y);
  const d=L>0?1:-1; ctx.moveTo(X1,y); ctx.lineTo(X1-8*d,y-5); ctx.moveTo(X1,y); ctx.lineTo(X1-8*d,y+5); ctx.stroke();
}
function drawScene(ctx,W,H,M,G){
  const o=SCENE[M.view];
  const O=oopsGeo(ctx,G,M); if(O) LABELS.push([O.bx,O.by,O.bx+O.w,O.by+O.bh]);
  drawContainer(ctx,G,M);
  drawParticles(ctx,G,M.g,M.view==='ideal'&&M.w.dragW!==null);
  if(BOXVIEWS[M.view]) drawHandles(ctx,G,M);
  if(o.pump) drawPump(ctx,G,M);
  if(o.gauges){ drawThermometer(ctx,G,M,W,H); drawGauge(ctx,G,M,W,H); }
  if(o.heater) drawHeater(ctx,G,M,W,H);
  if(o.ruler&&(M.view!=='diffusion'?M.st.showWidth:M.st.dScale)) drawRuler(ctx,G,M,W,H);
  if(BOXVIEWS[M.view]) drawTools(ctx,G,M,W,H);
  if(M.view==='explore') drawWallVelocity(ctx,G,M);
  if(!M.g.lid||M.g.lid.on||!BOXVIEWS[M.view]) {}
  else lab(ctx,W,H,G.X(M.g.left)+6,G.yT-12,'the lid is off',COL.ref,'11px -apple-system, sans-serif','left','middle');
}
function sceneCaption(ctx,G){ caption(ctx,G.Lx,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT); }

/* ---- a small time-series plot ------------------------------------------------- */
/* An auto-ranged axis must never be narrower than its endpoints' rounding:
   the shared ticksFor() steps t += step, and when the span is ~1e-16 of the
   values (two species' energy ratios that are 1 to rounding) t never advances
   and the loop spins for ever.  Widen any such range before asking for ticks. */
function niceRange(lo,hi){
  const sc=Math.max(Math.abs(lo),Math.abs(hi),1e-300);
  if(!(hi-lo>1e-9*sc)){ const m=(lo+hi)/2, d=Math.max(0.05*Math.abs(m),1e-6); return [m-d,m+d]; }
  return [lo,hi];
}
function plotSeries(ctx,W,H,b,title,short,xs,series,opt){
  opt=opt||{};
  let x0=Infinity, x1=-Infinity, y0=opt.y0, y1=opt.y1;
  for(const x of xs) if(isFinite(x)){ if(x<x0) x0=x; if(x>x1) x1=x; }
  if(!isFinite(x0)){ x0=0; x1=1; }
  if(opt.x0!==undefined) x0=opt.x0; if(opt.x1!==undefined) x1=opt.x1;
  if(!(x1>x0)) x1=x0+1;
  if(y0===undefined||y1===undefined){
    let lo=Infinity, hi=-Infinity;
    for(const S of series) for(const v of S.ys) if(isFinite(v)){ if(v<lo) lo=v; if(v>hi) hi=v; }
    for(const r of (opt.refs||[])) if(isFinite(r.y)){ if(r.y<lo) lo=r.y; if(r.y>hi) hi=r.y; }
    if(!(hi>lo)){ lo=isFinite(lo)?lo-1:0; hi=isFinite(hi)?hi+1:1; }
    const pad=0.08*(hi-lo); if(y0===undefined) y0=lo-pad; if(y1===undefined) y1=hi+pad;
  }
  [x0,x1]=niceRange(x0,x1); [y0,y1]=niceRange(y0,y1);
  axesR(ctx,b,x0,x1,y0,y1,{title:titleFor(b,title,short||title),xlab:opt.xlab,ylab:opt.ylab,
    xticks:sparseTicks(x0,x1,b.w),yticks:sparseTicks(y0,y1,b.h),xfmt:tickFmt(x0,x1,b.w),yfmt:tickFmt(y0,y1,b.h)});
  for(const r of (opt.refs||[])) if(isFinite(r.y)) polyline(ctx,b,[x0,x1],[r.y,r.y],x0,x1,y0,y1,r.col||COL.ref,r.lw||1.4,r.dash);
  for(const S of series){
    if(xs.length>1) polyline(ctx,b,xs,S.ys,x0,x1,y0,y1,S.col,S.lw||1.7,S.dash);
    else if(xs.length===1&&isFinite(S.ys[0])) marker(ctx,b,x0,x1,y0,y1,xs[0],S.ys[0],S.col);
  }
  if(opt.note) plotNote(ctx,W,H,b,opt.note);
  return {x0,x1,y0,y1};
}
/* a note in the middle of a plot, on a patch of the canvas ground so a
   reference line through the middle (the diffusion plot's dashed zero) does
   not strike it through */
function plotNote(ctx,W,H,b,txt){
  const w=plain(txt).length*11*0.52+10, x=b.x+b.w/2, y=b.y+b.h/2;
  ctx.fillStyle='#070b18'; ctx.fillRect(x-w/2,y-9,w,18);
  lab(ctx,W,H,x,y,txt,COL.dim,'11px -apple-system, sans-serif','center','middle');
}
function tickFmt(lo,hi,px){
  const t=sparseTicks(lo,hi,px); let d=Infinity; for(let i=1;i<t.length;i++) d=Math.min(d,t[i]-t[i-1]);
  const dec=!isFinite(d)||d>=1?0:Math.min(4,Math.ceil(-Math.log10(d)+1e-9));
  return v=>Math.abs(v)<1e-12?'0':v.toFixed(dec);
}
function emptyNote(ctx,W,H,b,txt){ plotNote(ctx,W,H,b,txt); }

/* ================================================================== *
 *  the gas law (PhET's Ideal screen)                                  *
 * ================================================================== */
function drawIdeal(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  drawScene(ctx,W,H,M,G);
  /* the seed point describes the state at t = 0, and edits made while paused
     (a resize, the pump, erase) move that state: re-seed it, so the lone
     marker never contradicts the readout beside it */
  if(M.w.trace.length===1&&M.g.t===0){ M.w.trace.length=0; idealRecord(M.w); }
  /* P and T against time, each in its own units: what the hold choice keeps flat */
  const tr=M.w.trace, t=[], P=[], T=[], st=M.st, atm=st.unitP!=='kPa', cel=st.unitT==='C';
  for(const r of tr){ t.push(r[0]); T.push(cel?r[1]-273.15:r[1]); P.push(atm?r[2]*GAS.ATM_PER_KPA:r[2]); }
  const note=t.length<2?'run the clock to trace it':null;
  if(G.plots.length) plotSeries(ctx,W,H,G.plots[0],'the gauge, '+(atm?'atm':'kPa')+' (PhET’s noise and 0.75-ps refresh)','P, '+(atm?'atm':'kPa'),t,
    [{ys:P,col:COL.live,lw:1.3}],{xlab:'t, ps',note});
  if(G.plots.length>1) plotSeries(ctx,W,H,G.plots[1],'the temperature, '+(cel?'°C':'K'),'T, '+(cel?'°C':'K'),t,
    [{ys:T,col:COL.pos}],{xlab:'t, ps',note});
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}
/* the gas-law trace: t, T, gauge P, width */
function idealRecord(w){ const g=w.g; w.trace.push([g.t,g.T===null?NaN:g.T,g.pOn?g.gaugeP:0,g.W]); if(w.trace.length>720) w.trace.splice(0,w.trace.length-720); }

/* ================================================================== *
 *  the moving wall (PhET's Explore screen)                            *
 * ================================================================== */
function drawExplore(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  drawScene(ctx,W,H,M,G);
  const w=M.w, tr=w.trace;
  if(G.plots.length){
    const b=G.plots[0];
    const pts=tr.filter(r=>isFinite(r[1]));
    const T0=w.T0||300, W0=w.W0||GAS.WDEF, g=M.g;
    let T1=T0*2.2, Tlo=T0*0.35;
    for(const r of pts){ if(r[1]>T1) T1=r[1]*1.05; if(r[1]<Tlo) Tlo=r[1]*0.95; }
    [Tlo,T1]=niceRange(Tlo,T1);
    const xs=[], ad=[], hdc=[], cnt=[M.nH,M.nL], rad=[g.species[0].r,g.species[1].r];
    for(let x=GAS.WMIN;x<=GAS.WMAX;x+=200){ xs.push(x/1000); ad.push(T0*W0/x); hdc.push(T0*hdAdiabatRatio(cnt,rad,W0,x,g.H,32)); }
    axesR(ctx,b,GAS.WMIN/1000,GAS.WMAX/1000,Tlo,T1,{title:titleFor(b,'T against width: the hard-disk adiabat (orange), points T·w = const (dashed)','T against w'),
      xlab:'w, nm',ylab:'T, K',xticks:sparseTicks(5,15,b.w),yticks:sparseTicks(Tlo,T1,b.h),xfmt:v=>fmt(v,0),yfmt:tickFmt(Tlo,T1,b.h)});
    polyline(ctx,b,xs,ad,GAS.WMIN/1000,GAS.WMAX/1000,Tlo,T1,COL.ref,1.2,[5,4]);
    polyline(ctx,b,xs,hdc,GAS.WMIN/1000,GAS.WMAX/1000,Tlo,T1,COL.ref,1.6);
    if(pts.length>1) polyline(ctx,b,pts.map(r=>r[0]/1000),pts.map(r=>r[1]),GAS.WMIN/1000,GAS.WMAX/1000,Tlo,T1,COL.pos,1.6);
    if(isFinite(M.T)) marker(ctx,b,GAS.WMIN/1000,GAS.WMAX/1000,Tlo,T1,M.g.W/1000,Math.min(T1,Math.max(Tlo,M.T)),COL.live);
  }
  if(G.plots.length>1){
    const b=G.plots[1];
    const pts=tr.filter(r=>isFinite(r[1]));
    if(pts.length<2) emptyNote(ctx,W,H,b,'push the wall to trace T against its adiabat');
    else {
      const g=M.g, cnt=[M.nH,M.nL], rad=[g.species[0].r,g.species[1].r];
      plotSeries(ctx,W,H,b,'T over the hard-disk adiabat since the push began (1 = reversible)','T / T adiabat',pts.map(r=>r[2]),
        [{ys:pts.map(r=>r[1]/(w.T0*hdAdiabatRatio(cnt,rad,w.W0,r[0],g.H,16))),col:COL.pos}],{refs:[{y:1,col:COL.ref,dash:[5,4]}],xlab:'t, ps'});
    }
  }
  sceneCaption(ctx,G);
}

/* ================================================================== *
 *  the energy (PhET's Energy screen): the 1-ps histograms            *
 * ================================================================== */
/* the expected counts per PhET bin at the thermometer's temperature */
function mbBinCounts(Nk,m,kT2,energy){
  const out=[];
  for(let b=0;b<GAS.NBIN;b++){
    const lo=b*(energy?GAS.EBIN:GAS.SBIN), hi=lo+(energy?GAS.EBIN:GAS.SBIN);
    out.push(Nk*(energy?mbEnergyCdf(hi,kT2)-mbEnergyCdf(lo,kT2):mbSpeedCdf(hi,m,kT2)-mbSpeedCdf(lo,m,kT2)));
  }
  return out;
}
function drawHistogram(ctx,W,H,b,M,energy){
  const g=M.g, S=g.sampler, st=M.st, ymax=ZOOMS[st.zoom];
  const key=energy?'e':'s', c0=S.out[key+'0'], c1=S.out[key+'1'];
  const wBin=energy?GAS.EBIN*GAS.KG_PER_AMU*1e21:GAS.SBIN, xmax=GAS.NBIN*wBin;
  const title=energy?'kinetic energy, zJ (bins of 1.33 zJ)':'speed, m/s (bins of 170 m/s)';
  axesR(ctx,b,0,xmax,0,ymax,{title:titleFor(b,title+' — particles per bin, 1-ps average',energy?'kinetic energy':'speed'),
    xlab:energy?'KE, zJ':'speed, m/s',ylab:'particles',xticks:sparseTicks(0,xmax,b.w),yticks:sparseTicks(0,ymax,b.h),xfmt:tickFmt(0,xmax,b.w),yfmt:v=>fmt(v,0)});
  /* bars: all particles */
  ctx.fillStyle='rgba(184,236,76,0.55)';
  const bw=b.w/GAS.NBIN;
  let clipped=0;
  for(let q=0;q<GAS.NBIN;q++){
    const v=c0[q]+c1[q], hgt=Math.min(1,v/ymax)*b.h; if(v>ymax) clipped++;
    if(v>0) ctx.fillRect(b.x+q*bw+1,b.y1-hgt,bw-2,hgt);
  }
  const step=(arr,col,dash)=>{ const xs=[], ys=[];
    for(let q=0;q<GAS.NBIN;q++){ xs.push(q*wBin,(q+1)*wBin); ys.push(arr[q],arr[q]); }
    polyline(ctx,b,xs,ys,0,xmax,0,ymax,col,1.3,dash); };
  if(st.histH) step(c0,COL.heavy); if(st.histL) step(c1,COL.light);
  /* the 2-D Maxwell-Boltzmann counts (orange) */
  if(M.kT2){
    const e0=mbBinCounts(gasCount(g,0),g.species[0].m,M.kT2,energy), e1=mbBinCounts(gasCount(g,1),g.species[1].m,M.kT2,energy);
    const xs=[], ys=[];
    for(let q=0;q<GAS.NBIN;q++){ xs.push((q+0.5)*wBin); ys.push(e0[q]+e1[q]); }
    polyline(ctx,b,xs,ys,0,xmax,0,ymax,COL.ref,1.6);
  }
  if(clipped) lab(ctx,W,H,b.x1-4,b.y+10,clipped+' bar'+(clipped>1?'s':'')+' past the '+ymax+' zoom',COL.ref,'10.5px -apple-system, sans-serif','right','middle');
}
function drawEnergy(ctx,W,H,M){
  const G=viewGeo(ctx,W,H,M);
  drawScene(ctx,W,H,M,G);
  if(G.plots.length) drawHistogram(ctx,W,H,G.plots[0],M,false);
  if(G.plots.length>1) drawHistogram(ctx,W,H,G.plots[1],M,true);
  drawOops(ctx,G,M,W,H);
  sceneCaption(ctx,G);
}
