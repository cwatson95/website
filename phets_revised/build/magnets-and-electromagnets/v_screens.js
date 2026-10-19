
/* ================================================================== *
 *  PhET's screens: the play area is PhET's layout box, 1024 x 618 mm  *
 *  (1 PhET px = 1 mm), fitted beside the floating readout             *
 * ================================================================== */
const SCREEN_CAP={};
/* #bar */
SCREEN_CAP.bar=['The needles are PhET’s field display: one every 40 mm pointing along B, their brightness PhET’s mapping 2(|B|/300 G)^(1/2.7), not |B| itself. The compass and meter are drawn at PhET’s sizes. The field is exact (a uniformly magnetised cylinder); the compass is a modelled damped rotor.',
  'Needles every 40 mm along B; brightness is PhET’s display mapping of |B|. Field exact, compass modelled.'];
/* #endbar */
/* #emag */
SCREEN_CAP.em=['Needles every 40 mm along B, brightness PhET’s mapping of |B|. Each loop is a thin filament on the drawn wire’s centre line; the loops are drawn as ellipses only for perspective. Electrons: one lap per second at full current (a picture of the current, not its drift speed).',
  'Needles every 40 mm along B; loops drawn in perspective; electron speed not to scale.'];
/* #endemag */
function screenGeo(ctx,W,H,key){
  const narrow=isNarrow(W), top=stageTop()+22, left=10, right=narrow?W-10:W-RO_W-34;
  const capW=Math.max(280,Math.min(W-148,right-left-20));
  const fit=fitCaption(ctx,W,H-HINT_H,SCREEN_CAP[key][0],SCREEN_CAP[key][1],capW,top+240);
  const b=box(left,top,right-left,Math.max(120,fit.capY-10-top));
  const map=worldFitUp(b,{xmin:0,xmax:LAYOUT_W,ymin:0,ymax:LAYOUT_H},0);
  const world=box(map.X(0),map.Y(LAYOUT_H),LAYOUT_W*map.s,LAYOUT_H*map.s);
  return {b,map,world,capY:fit.capY,capTxt:fit.txt,capW,left:Math.max(left,world.x)};
}
function screenBack(ctx,W,H,G){
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#090e1c'; ctx.fillRect(G.world.x,G.world.y,G.world.w,G.world.h);
  frame(ctx,G.world,'#1a2032');
}
function screenCaption(ctx,G){ caption(ctx,G.left,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT); }

/* #bar */
/* ---------------- the bar magnet screen ---------------- */
function drawBarScreen(ctx,W,H,M){
  const st=ST, G=screenGeo(ctx,W,H,'bar'), map=G.map;
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  screenBack(ctx,W,H,G);
  if(st.barMeter){ const mb=meterBodyBox(map,st.barM.x,st.barM.y); LABELS.push([mb.bx,mb.by,mb.bx+mb.bw,mb.by+mb.bh]); }
  if(st.earth) drawEarth(ctx,map,M.src);
  if(st.barField&&M.src.S>0) drawNeedleField(ctx,map,needleGrid(M.src,0,0,LAYOUT_W,LAYOUT_H));
  drawBarMagnet(ctx,map,M.src,{seeInside:st.seeInside});
  if(M.src.S===0) lab(ctx,W,H,map.X(M.src.x),map.Y(M.src.y+MAG_R+22),'strength 0: no field',COL.dim,SM_FONT,'center','middle');
  if(st.barCompass) drawCompass(ctx,map,st.barC.x,st.barC.y,M.rot.phi);
  if(st.barMeter) drawFieldMeter(ctx,map,st.barM.x,st.barM.y,M.meter,st.units);
  screenCaption(ctx,G);
  return G;
}
/* #endbar */
/* #emag */
/* ---------------- the electromagnet screen ---------------- */
function emParts(st,map){
  const xs=coilLoopsX(st.loops), sp=emSupplyPos(st);
  /* the coil's two ends, taken a little outside the outermost turns so a single loop still
     shows two leads rather than one line */
  return {xs, sp, left:[st.em.x+xs[0]-10, st.em.y-COIL_A*0.72], right:[st.em.x+xs[xs.length-1]+10, st.em.y-COIL_A*0.72]};
}
function drawEMScreen(ctx,W,H,M){
  const st=ST, G=screenGeo(ctx,W,H,'em'), map=G.map, P=emParts(st,map);
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  screenBack(ctx,W,H,G);
  if(st.emMeter){ const mb=meterBodyBox(map,st.emM.x,st.emM.y); LABELS.push([mb.bx,mb.by,mb.bx+mb.bw,mb.by+mb.bh]); }
  if(st.emField&&M.src.I!==0) drawNeedleField(ctx,map,needleGrid(M.src,0,0,LAYOUT_W,LAYOUT_H));
  drawCoilHalf(ctx,map,P.xs,st.em.x,st.em.y,COIL_A,WIRE_R*2,'back');
  /* leads to the supply */
  const term=M.sup.kind==='dc'?drawBattery(ctx,map,P.sp.x,P.sp.y,M.V):drawACSupply(ctx,map,P.sp.x,P.sp.y,M.V,AC_VMAX*st.acPk/100,acFreq(M.sup)*LIVE.emT);
  ctx.beginPath();
  for(const [end,t] of [[P.left,term.left],[P.right,term.right]]){
    ctx.moveTo(map.X(end[0]),map.Y(end[1])); ctx.lineTo(map.X(end[0]),t[1]); ctx.lineTo(t[0],t[1]);
  }
  ctx.strokeStyle=COL.copper; ctx.lineWidth=Math.max(1.5,4*map.s); ctx.lineJoin='round'; ctx.stroke();
  drawCoilHalf(ctx,map,P.xs,st.em.x,st.em.y,COIL_A,WIRE_R*2,'front');
  if(st.electrons&&M.src.I!==0) drawElectrons(ctx,map,P.xs,st.em.x,st.em.y,COIL_A,LIVE.ePhase,4);
  if(st.emCompass) drawCompass(ctx,map,st.emC.x,st.emC.y,M.rot.phi);
  if(st.emMeter) drawFieldMeter(ctx,map,st.emM.x,st.emM.y,M.meter,st.units);
  if(M.src.I===0) lab(ctx,W,H,map.X(st.em.x),map.Y(st.em.y+COIL_A+24),'no current: no field',COL.dim,SM_FONT,'center','middle');
  screenCaption(ctx,G);
  return G;
}

/* #endemag */
/* ---------------- pointer handling on the screens ---------------- */
function clampWorld(p,mx,my){ p.x=clamp(p.x,mx,LAYOUT_W-mx); p.y=clamp(p.y,my,LAYOUT_H-my); }
function hitMeter(map,p,X,Y){ const G=meterBodyBox(map,p.x,p.y); return Math.hypot(X-G.X,Y-G.Y)<=G.r+4||(X>=G.bx&&X<=G.bx+G.bw&&Y>=G.by-4&&Y<=G.by+G.bh); }
function hitCompass(map,p,X,Y){ return Math.hypot(X-map.X(p.x),Y-map.Y(p.y))<=42*map.s+4; }
/* what each screen offers the pointer, in the order it is tried: the tools first, the source
   last, each with the margin its own body needs when it is dragged to an edge.  A screen this
   page does not carry registers nothing (family.py strips the entries it has no screen for). */
const DRAG_CANDS={};
/* #bar */
function hitMagnet(map,m,X,Y){ const L=magnetLocal(m,map.wx(X),map.wy(Y),0); return Math.abs(L.u)<=MAG_B+4/map.s&&L.rho<=MAG_R+4/map.s; }
DRAG_CANDS.bar=(st,map,X,Y)=>[{k:'barM',on:st.barMeter,hit:p=>hitMeter(map,p,X,Y),mx:10,my:10},
                     {k:'barC',on:st.barCompass,hit:p=>hitCompass(map,p,X,Y),mx:10,my:10},
                     {k:'bar',on:true,hit:p=>hitMagnet(map,p,X,Y),mx:MAG_B*0.2,my:MAG_R}];
/* #endbar */
/* #emag */
function hitCoil(st,map,X,Y){
  const wx=map.wx(X), wy=map.wy(Y), xs=coilLoopsX(st.loops), sp=emSupplyPos(st);
  if(wx>=st.em.x+xs[0]-COIL_A*COIL_TILT-12&&wx<=st.em.x+xs[xs.length-1]+COIL_A*COIL_TILT+12&&Math.abs(wy-st.em.y)<=COIL_A+12) return true;
  return Math.abs(wx-sp.x)<=66&&Math.abs(wy-sp.y)<=34;
}
DRAG_CANDS.em=(st,map,X,Y)=>[{k:'emM',on:st.emMeter,hit:p=>hitMeter(map,p,X,Y),mx:10,my:10},
                             {k:'emC',on:st.emCompass,hit:p=>hitCompass(map,p,X,Y),mx:10,my:10},
                             {k:'em',on:true,hit:()=>hitCoil(st,map,X,Y),mx:90,my:COIL_A+50}];
/* #endemag */
function screenPointer(type,X,Y,W,H,ctx0){
  const st=ST, make=DRAG_CANDS[st.view];
  if(type==='up'){ const was=!!DRAG.what; DRAG.what=null; return was; }
  if(!make) return false;
  const ctx=ctx0||makeMeasureCtx(), G=screenGeo(ctx,W,H,st.view), map=G.map;
  if(type==='down'){
    for(const c of make(st,map,X,Y)){
      if(!c.on) continue;
      const p=st[c.k];
      if(c.hit(p)){ DRAG.what=c.k; DRAG.dx=map.wx(X)-p.x; DRAG.dy=map.wy(Y)-p.y; DRAG.mx=c.mx; DRAG.my=c.my; return true; }
    }
    return false;
  }
  if(type==='move'&&DRAG.what){
    const p=st[DRAG.what]; if(!p) return false;
    p.x=map.wx(X)-DRAG.dx; p.y=map.wy(Y)-DRAG.dy;
    clampWorld(p,DRAG.mx,DRAG.my);
    /* the needle needs no waking here: rotorTick compares it with the field at the compass's
       present place every frame, so a drag that changes either wakes it by itself (the
       rest = false lines that stood here were provably redundant -- the mutation sweep found
       them equivalent, which is how dead code announces itself) */
    return true;
  }
  return false;
}
/* a measuring context for layout outside a draw (the caption's height sets the play area) */
function makeMeasureCtx(){
  const st={font:'10px sans-serif'};
  return {get font(){ return st.font; }, set font(v){ st.font=v; },
    measureText(t){ const m=/(\d+(?:\.\d+)?)px/.exec(st.font||''); return {width:(''+t).length*(m?parseFloat(m[1]):10)*0.52}; }};
}
