
/* ================================================================== *
 *  drawing: shared pieces, and the bench view                         *
 * ================================================================== */
/* the house #hint (HTML, bottom:11px, 11px type) sits on the last line of a
   bottom-anchored caption unless the caption ends HINT_H higher (the
   wave-on-a-string trap): every caption here does, and selfTest asserts it */
const HINT_H=18;
/* an energy chunk: a small square in its form's colour with an E drawn in
   strokes (text ops would flood the overlap audit) */
function drawChunk(ctx,x,y,s,form,alpha){
  const a=alpha===undefined?1:clamp(alpha,0,1); if(a<=0.02) return;
  const c=COL.form[form]||COL.form.thermal, h=s/2, k=s*0.22;
  ctx.beginPath();
  ctx.moveTo(x-h+k,y-h); ctx.lineTo(x+h-k,y-h); ctx.lineTo(x+h,y-h+k); ctx.lineTo(x+h,y+h-k);
  ctx.lineTo(x+h-k,y+h); ctx.lineTo(x-h+k,y+h); ctx.lineTo(x-h,y+h-k); ctx.lineTo(x-h,y-h+k); ctx.closePath();
  ctx.fillStyle=a<1?rgba(c,a):c; ctx.fill();
  ctx.beginPath();
  const ex=x-s*0.17, ew=s*0.36, ey=s*0.27;
  ctx.moveTo(ex+ew,y-ey); ctx.lineTo(ex,y-ey); ctx.lineTo(ex,y+ey); ctx.lineTo(ex+ew,y+ey);
  ctx.moveTo(ex,y); ctx.lineTo(ex+ew*0.8,y);
  ctx.strokeStyle=rgba('#0a0c12',0.8*a); ctx.lineWidth=Math.max(1,s*0.13); ctx.stroke();
}
/* time-axis tick labels with as many decimals as the spacing needs
   (Known-bad: a fixed fmt(t,2) prints "5.00" and crowds the axis) */
function tickFmt(lo,hi,want){
  const t=ticksFor(Math.min(lo,hi),Math.max(lo,hi),want||6), step=t.length>1?t[1]-t[0]:Math.abs(hi-lo)||1;
  const d=Math.max(0,Math.min(3,-Math.floor(Math.log10(step)+1e-9)));
  return v=>fmt(v,d);
}

/* ---- the bench's geometry: the world fitted left of the readout ---- */
const BENCH_CAP_FULL='Drawn to scale: the blocks are 4.5-cm cubes (their depth drawn obliquely, as PhET draws it), the beakers 8.5 cm across, the burners 7.5 cm. '
  +'Each red square is one energy chunk, 5019 J of thermal energy, drawn 1 cm across (not to scale); a body holds the count PhET’s map gives its energy, give or take one in transit. '
  +'Drag a body to stack it, set it on a burner or drop it in a beaker; drag a lever, or a thermometer out of the tray.';
const BENCH_CAP_SHORT='To scale except the energy chunks (5019 J each, drawn 1 cm across). Drag the bodies, the levers and the thermometers.';
const BENCH_EXT={xmin:-0.305,xmax:0.31,ymin:-0.02,ymax:0.29};
function benchGeo(ctx,W,H){
  const narrow=isNarrow(W), left=16, right=narrow?W-14:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left-20));
  const fit=fitCaption(ctx,W,H-HINT_H,BENCH_CAP_FULL,BENCH_CAP_SHORT,capW,stageTop()+30+240);
  const top=stageTop()+14, bottom=fit.capY-10;
  const bx=box(left,top,right-left,Math.max(120,bottom-top));
  const map=worldFitUp(bx,BENCH_EXT,0.004);
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,bx,map};
}
/* every box is drawn with its front face on the model's rectangle and its
   depth running up and to the right (PhET centres its cubes on the
   rectangle; the beakers here are drawn flat, so the front must sit on it) */
const DEPTH=2*PERSP;
function drawBox3(ctx,map,x0,y0,x1,y1,front,edge,lw){
  const d=DEPTH;
  worldPoly(ctx,map,[[x0,y1],[x1,y1],[x1+d,y1+d],[x0+d,y1+d]],mix(front,'#ffffff',0.2),null);
  worldPoly(ctx,map,[[x1,y0],[x1+d,y0+d],[x1+d,y1+d],[x1,y1]],mix(front,'#05070c',0.35),null);
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],front,null);
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1+d,y0+d],[x1+d,y1+d],[x0+d,y1+d],[x0,y1]],null,edge,lw);
}
/* the burner lever: a track on the burner's front, below the flames, the
   knob at the level (the pointer inverts leverPos through the same pair) */
const LEVER_Y0=0.03, LEVER_DY=0.02;
function leverPos(k,l){ return {x:burnerX(k), y:LEVER_Y0+LEVER_DY*l}; }
function leverLevel(y){ return clamp((y-LEVER_Y0)/LEVER_DY,-1,1); }
function drawBurner(ctx,map,k,l,M){
  const x=burnerX(k), x0=x-BURNER_HALF, x1=x+BURNER_HALF;
  drawBox3(ctx,map,x0,0,x1,BURNER_TOP,'#121824',rgba(COL.struct,0.55),1.2);
  /* flame (heat) or ice (cool), sized by the level, inside the burner's mouth */
  if(l>0){
    for(let q=-1;q<=1;q++){ const cx=x+q*0.017, hh=0.006+0.012*l*(q===0?1:0.75), b0=BURNER_TOP-0.02;
      worldPoly(ctx,map,[[cx-0.008,b0],[cx+0.008,b0],[cx+0.003,b0+hh*0.6],[cx,b0+hh],[cx-0.003,b0+hh*0.6]],rgba('#ff8a2a',0.35+0.6*l),rgba('#ffd27a',0.9),1); }
  } else if(l<0){
    for(let q=-1;q<=1;q++){ const cx=x+q*0.018, s=0.004+0.004*(-l), b0=BURNER_TOP-0.021;
      worldPoly(ctx,map,[[cx-s,b0],[cx+s,b0],[cx+s,b0+2*s],[cx-s,b0+2*s]],rgba('#9fd8ff',0.35+0.5*(-l)),rgba('#dff3ff',0.9),1); }
  }
  const t0=leverPos(k,-1), t1=leverPos(k,1), kn=leverPos(k,l);
  seg(ctx,map,[t0.x,t0.y],[t1.x,t1.y],rgba(COL.struct,0.6),2);
  const X=map.X(kn.x), Y=map.Y(kn.y);
  ctx.beginPath(); ctx.rect(X-9,Y-4,18,8);
  ctx.fillStyle=l>0?'#ff8a2a':(l<0?'#7cc8ff':'#6f7789'); ctx.fill();
  ctx.strokeStyle=M&&M.dragLever===k?COL.live:'#e9edf5'; ctx.lineWidth=M&&M.dragLever===k?2:1; ctx.stroke();
}
function drawBlock(ctx,map,b,held){
  drawBox3(ctx,map,b.x-b.w/2,b.y,b.x+b.w/2,b.y+b.h,COL.body[b.mat],held?COL.live:rgba('#e9edf5',0.55),held?2:1);
}
function beakerTicks(ctx,map,b){
  const x=b.x-b.w/2+0.004;
  for(let q=1;q<=3;q++){ const y=b.y+q*b.h*0.95/3; seg(ctx,map,[x,y],[x+0.009,y],rgba('#cfd4de',0.45),1); }
}
function drawBeakerBack(ctx,map,b){
  const x0=b.x-b.w/2, x1=b.x+b.w/2, y0=b.y, y1=b.y+b.h, yf=b.y+b.h*b.f;
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],rgba('#1a2130',0.55),null);
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1,yf],[x0,yf]],mix('#0a0c12',COL.body[b.mat],0.55),null);
}
function drawBeakerFront(ctx,map,b,held){
  const x0=b.x-b.w/2, x1=b.x+b.w/2, y0=b.y, y1=b.y+b.h, yf=b.y+b.h*b.f, c=COL.body[b.mat];
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1,yf],[x0,yf]],rgba(c,0.16),null);
  seg(ctx,map,[x0,yf],[x1,yf],rgba(c,0.95),1.4);
  ctx.beginPath(); ctx.moveTo(map.X(x0),map.Y(y1)); ctx.lineTo(map.X(x0),map.Y(y0)); ctx.lineTo(map.X(x1),map.Y(y0)); ctx.lineTo(map.X(x1),map.Y(y1));
  ctx.strokeStyle=held?COL.live:rgba('#e9edf5',0.8); ctx.lineWidth=held?2.2:1.5; ctx.stroke();
  POLY_SEGS.push(map.X(x0),map.Y(y1),map.X(x0),map.Y(y0),map.X(x1),map.Y(y0),map.X(x1),map.Y(y1));
  beakerTicks(ctx,map,b);
  /* steam over a beaker within 10 K of boiling (PhET's steamingProportion) */
  const sp=steamProp(b);
  if(sp>0) for(let q=0;q<7;q++){ const f=(q+0.5)/7, cx=x0+b.w*(0.25+0.5*((q*0.618)%1)), cy=yf+(y1+0.035-yf)*f, r=0.005+0.004*f;
    worldPoly(ctx,map,ellipsePts(cx,cy,r,r*0.6,12),rgba('#e9edf5',(0.5-0.3*f)*sp+0.06),null); }
}
/* where a body's k-th owned chunk sits: a jittered grid on a block's front
   face, or in a beaker's liquid */
function chunkSlot(b,k){
  const beaker=b.kind==='beaker', m=beaker?0.008:0.006;
  const x0=b.x-b.w/2+m, x1=b.x+b.w/2-m, y0=b.y+0.006, y1=(beaker?b.y+b.h*b.f:b.y+b.h)-0.006;
  const cols=beaker?8:4, col=k%cols, row=Math.floor(k/cols), rows=Math.max(1,Math.ceil((beaker?48:28)/cols));
  const jx=((k*0.61803)%1-0.5)*0.35, jy=((k*0.41421)%1-0.5)*0.35;
  return [x0+(x1-x0)*(col+0.5+jx)/cols, y0+(y1-y0)*((row%rows)+0.5+jy)/rows];
}
function inboundOf(B){ const n=[0,0,0,0]; for(const f of B.flights) if(isBodyRef(f.dst)) n[f.dst]++; return n; }
function drawOwnChunks(ctx,map,B,i,sz,inbound){
  const b=B.bodies[i], settled=Math.max(0,B.own[i]-inbound[i]);
  for(let k=0;k<settled;k++){ const p=chunkSlot(b,k); drawChunk(ctx,map.X(p[0]),map.Y(p[1]),sz,'thermal',1); }
}
function drawFlights(ctx,map,B,sz,inbound){
  const seen=[0,0,0,0];
  for(const f of B.flights){
    const u=smoothstep(clamp(f.t/f.dur,0,1)), anchor=f.air;
    let a, z, alpha=1;
    if(isBodyRef(f.src)) a=chunkSlot(B.bodies[f.src],Math.max(0,B.own[f.src]));
    else if(f.src==='A'){ const b=B.bodies[anchor]; a=[b.x,b.y+b.h+0.09]; }
    else a=[burnerX(+f.src[1]),BURNER_TOP-0.012];
    if(isBodyRef(f.dst)){ const own=B.own[f.dst]-inbound[f.dst]+seen[f.dst]; seen[f.dst]++; z=chunkSlot(B.bodies[f.dst],Math.max(0,own)); }
    else if(f.dst==='A'){ const b=B.bodies[anchor]; z=[b.x+0.01,b.y+b.h+0.1]; alpha=1-u*0.9; }
    else z=[burnerX(+f.dst[1]),BURNER_TOP-0.012];
    if(f.src==='A') alpha=0.1+0.9*u;
    drawChunk(ctx,map.X(a[0]+(z[0]-a[0])*u),map.Y(a[1]+(z[1]-a[1])*u),sz,'thermal',alpha);
  }
}
function drawThermo(ctx,W,H,map,B,k,M,live){
  const th=B.therm[k], p=thermoTip(B,th);
  const X=map.X(p.x), Y=map.Y(p.y), hpx=THERMO_H*map.s, w=Math.max(5,0.0055*map.s);
  const r=M&&!th.tray?M.therm[k]:null, T=r?r.T:T_ROOM;
  ctx.beginPath(); ctx.rect(X-w/2,Y-hpx,w,hpx-w*0.6); ctx.fillStyle='#e9edf5'; ctx.fill();
  ctx.strokeStyle=live?COL.live:'#aeb6c6'; ctx.lineWidth=live?2:1; ctx.stroke();
  const frac=r?clamp((T-T_FREEZE)/(700-T_FREEZE),0,1):0.05, hcol=(hpx-w*1.4)*frac;
  ctx.beginPath(); ctx.rect(X-w/4,Y-w*0.8-hcol,w/2,hcol); ctx.fillStyle='#e0453a'; ctx.fill();
  dot(ctx,X,Y-w*0.3,w*0.75,'#e0453a',live?COL.live:'#aeb6c6',1);
  if(r){
    const what=typeof r.what==='number'?COL.body[B.bodies[r.what].mat]:(r.what==='air'?'#5a6275':'#e9edf5');
    ctx.beginPath(); ctx.moveTo(X+w*0.6,Y-w*0.3); ctx.lineTo(X+w*0.6+7,Y-w*0.3-5); ctx.lineTo(X+w*0.6+7,Y-w*0.3+5); ctx.closePath(); ctx.fillStyle=what; ctx.fill();
    lab(ctx,W,H,X+w+10,Y-hpx+6,'#'+(k+1)+' '+fmt(kelvinC(T),1)+' °C','#e9edf5',SM_FONT,'left','middle');
  }
}
function drawBench(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  const G=benchGeo(ctx,W,H), map=G.map, B=M.B;
  reserveCaption(G.left+4,G.capY,G.capTxt,G.capW,ctx);
  /* the bench top and PhET's six spots */
  const gx0=BENCH_EXT.xmin+0.004, gx1=BENCH_EXT.xmax-0.004;
  worldPoly(ctx,map,[[gx0,-0.012],[gx1,-0.012],[gx1,0],[gx0,0]],'#10151f',null);
  seg(ctx,map,[gx0,0],[gx1,0],rgba(COL.struct,0.55),1.2);
  SPOTS.forEach((x,k)=>{ if(k===2||k===3) return; seg(ctx,map,[x-0.02,-0.004],[x+0.02,-0.004],rgba(COL.struct,0.35),1); });
  worldPoly(ctx,map,[[TRAY.x0,TRAY.y0],[TRAY.x1,TRAY.y0],[TRAY.x1,TRAY.y1],[TRAY.x0,TRAY.y1]],'#0d121c',rgba(COL.struct,0.5),1);
  lab(ctx,W,H,map.X(TRAY.x1)+8,map.Y(TRAY.y1)+8,'thermometers','#8b93a6',SM_FONT,'left','middle');
  for(let k=0;k<2;k++) drawBurner(ctx,map,k,M.lev[k],M);
  /* painter's order, back to front: each beaker's liquid and its chunks, the
     blocks and theirs (in front of a liquid they sit in), then the beakers'
     translucent fronts and glass */
  const held=B.held?B.held.group[0]:-1, sz=clamp(0.0095*map.s,7,13), sym=M.st.symBench, inb=inboundOf(B);
  for(const i of [2,3]){ drawBeakerBack(ctx,map,B.bodies[i]); if(sym) drawOwnChunks(ctx,map,B,i,sz*0.9,inb); }
  const blocks=[0,1].sort((a,b)=>B.bodies[a].y-B.bodies[b].y);
  for(const i of blocks){ drawBlock(ctx,map,B.bodies[i],held===i); if(sym) drawOwnChunks(ctx,map,B,i,sz,inb); }
  for(const i of [2,3]) drawBeakerFront(ctx,map,B.bodies[i],held===i);
  if(sym) drawFlights(ctx,map,B,sz,inb);
  /* labels: each block on its top face, each beaker over its glass */
  for(const i of [0,1]){ const b=B.bodies[i]; lab(ctx,W,H,map.X(b.x+PERSP),map.Y(b.y+b.h+PERSP),MAT_NAME[b.mat],'#e9edf5',SM_FONT,'center','middle'); }
  for(const i of [2,3]){ const b=B.bodies[i]; lab(ctx,W,H,map.X(b.x),map.Y(b.y+b.h)-9,MAT_NAME[b.mat],rgba(COL.body[b.mat],1),SM_FONT,'center','middle'); }
  for(let k=0;k<2;k++){ const l=M.lev[k]; lab(ctx,W,H,map.X(burnerX(k)),map.Y(-0.012)+10,(k?'right':'left')+': '+levText(l),l>0?'#ffb070':(l<0?'#9fd8ff':'#8b93a6'),SM_FONT,'center','middle'); }
  for(let k=0;k<4;k++) drawThermo(ctx,W,H,map,B,k,M,M.dragThermo===k);
  caption(ctx,G.left+4,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
  return G;
}
