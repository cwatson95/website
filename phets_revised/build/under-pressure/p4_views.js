
/* ================================================================== *
 *  the pool stage, shared by the four scene views, then view A and B  *
 * ================================================================== */
/* every layout reserves HINT_H at the bottom: the house #hint is HTML at
   bottom:11px and the canvas capture cannot see it, so a caption anchored at
   H - 12 would sit underneath it (Known-bad, wave-on-a-string).  The caption's
   own band is registered too, so a stage label near the bottom dodges it. */
function layout(ctx,W,H,full,short,nB,frac,nBn){
  const L=stageLayout(ctx,W,H-HINT_H,full,short,nB,frac,nBn);
  LABELS.push([L.left-2,L.capY-5,L.left+L.capW+2,H-HINT_H-6]);
  return L;
}
/* a label that must be drawn where it is: painted unconditionally AND
   registered, so every dodging lab() after it moves aside */
function labFixed(ctx,x,y,txt,col,font,align,base){
  ctx.fillStyle=col; ctx.font=font;
  ctx.textAlign=align||'center'; ctx.textBaseline=base||'middle';
  const t=plain(txt), fs=parseFloat(font.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  const lx=align==='right'?x-w:(align==='left'?x:x-w/2);
  const ly=base==='top'?y:(base==='bottom'?y-hh:y-hh/2);
  LABELS.push([lx,ly,lx+w,ly+hh]);
  ctx.fillText(t,x,y);
}
/* axes(), with the TICK LABELS, the axis names and the title registered */
function axesReg(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=opt||{};
  axes(ctx,b,xlo,xhi,ylo,yhi,o);
  const fw=(s,px)=>plain(''+s).length*px*0.52;
  const xt=o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  const yt=o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||5);
  for(const t of xt){ const X=b.x+b.w*(t-xlo)/(xhi-xlo||1);
    if(X<b.x-0.5||X>b.x1+0.5) continue;
    const w=fw(o.xfmt?o.xfmt(t):fmt(t,2),10.5);
    LABELS.push([X-w/2,b.y1+5,X+w/2,b.y1+5+10.5*1.15]); }
  for(const t of yt){ const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1);
    if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    const w=fw(o.yfmt?o.yfmt(t):fmt(t,2),10.5);
    LABELS.push([b.x-6-w,Y-6.04,b.x-6,Y+6.04]); }
  if(o.xlab){ const w=fw(o.xlab,11); LABELS.push([b.x+b.w/2-w/2,b.y1+21,b.x+b.w/2+w/2,b.y1+33.65]); }
  if(o.ylab){ const w=fw(o.ylab,11); LABELS.push([b.x-52.65,b.y+b.h/2-w/2,b.x-40,b.y+b.h/2+w/2]); }
  if(o.title){ const w=fw(o.title,13); LABELS.push([b.x,b.y-23.95,b.x+w,b.y-9]); }
}
/* legendAuto() records its box in LEGEND_RECTS, which lab() does not consult,
   so a note placed in "the empty corner" landed on the legend.  Register it. */
function legendReg(ctx,b,items){
  const r=legendAuto(ctx,b,items);
  if(r) LABELS.push([r.x,r.y,r.x1,r.y1]);
  return r;
}
/* a wide stage drawing a nearly square picture at equal aspect wastes most of
   its width, so the pool takes the left and one analysis panel the right */
function splitMain(L,W,fracLeft,nRight){
  const b=L.main;
  if(isNarrow(W)||nRight<1) return {pool:b,rows:[]};
  const gut=66, wl=Math.round(b.w*fracLeft);
  const pool=box(b.x,b.y,Math.max(120,wl-gut/2),b.h);
  const rx=b.x+wl+gut/2, rw=Math.max(150,b.x1-rx);
  const rows=[], slot=b.h/nRight;
  for(let i=0;i<nRight;i++) rows.push(box(rx,b.y+i*slot+26,rw,Math.max(60,slot-64)));
  return {pool:pool,rows:rows};
}

const GROUND='#20242e', GROUND2='#171b23';
/* each fluid gets its own tint, so the density slider visibly changes the pool */
function fluidColour(rho){
  const t=clamp((rho-RHO_GASOLINE)/(RHO_HONEY-RHO_GASOLINE),0,1);
  return mix('#c9c04a',mix(COL.struct,'#c9962a',t>0.5?(t-0.5)*2:0),t<0.5?t*2:1);
}
function extentFor(scene){
  if(scene==='trapezoid') return {xmin:1.30,xmax:8.30,ymin:-POOL_H-0.12,ymax:0.62};
  /* the chamber's ymax only has to clear the tallest stack: the platform rests
     at y = -0.70 with nothing on it and the three masses are 1.00 m together,
     so 0.62 is ample and 1.35 was giving away a third of the picture */
  if(scene==='chamber')  return {xmin:1.25,xmax:8.35,ymin:-POOL_H-0.12,ymax:0.62};
  return {xmin:1.55,xmax:6.75,ymin:-POOL_H-0.12,ymax:0.62};
}
/* the cavity each scene cuts out of the ground, as world polygons */
function cavityPolys(scene){
  if(scene==='trapezoid'){
    /* ONE outline, not three overlapping ones: the channel bridges the two
       chambers along the floor, so the cavity is a single U with two prongs.
       Stroking three overlapping rectangles would draw the channel's top edge
       straight through both chambers. */
    const l0=tzLeft(0), l3=tzLeft(POOL_H), lb=tzLeft(TZ_CHAN.t1);
    const r0=tzRight(0), r3=tzRight(POOL_H), rb=tzRight(TZ_CHAN.t1);
    const yb=-POOL_H+TZ_CHAN.t1;
    return [[[l3[0],0],[l0[0],-POOL_H],[r0[1],-POOL_H],[r3[1],0],
             [r3[0],0],[rb[0],yb],[lb[1],yb],[l3[1],0]]];
  }
  if(scene==='chamber'){
    const R=(a,b,y0,y1)=>[[a,y1],[b,y1],[b,y0],[a,y0]];
    return [R(CH_LEFT.x0,CH_LEFT.x1,-POOL_H,CH_OPEN_BOT),
            R(CH_RIGHT.x0,CH_RIGHT.x1,-POOL_H,CH_OPEN_BOT),
            R(CH_LEFT.x1,CH_RIGHT.x0,-2.75,-2.25),
            R(CH_L_SHAFT.x0,CH_L_SHAFT.x1,CH_OPEN_BOT,0),
            R(CH_R_SHAFT.x0,CH_R_SHAFT.x1,CH_OPEN_BOT,0)];
  }
  return [[[SQ_X0,0],[SQ_X1,0],[SQ_X1,-POOL_H],[SQ_X0,-POOL_H]]];
}
/* the fluid, as world polygons, for a flat surface at ySurf */
function fluidPolys(scene,ySurf,P){
  if(scene==='trapezoid'){
    /* NON-OVERLAPPING pieces, so the drawn area times the out-of-page depth is
       exactly the model volume (selfTest asserts it).  Inside the floor
       channel the cross-section is one band running from the left chamber's
       left wall to the right chamber's right wall; above it the two chambers
       are separate. */
    const out=[];
    const tS=clamp(ySurf+POOL_H,0,POOL_H);
    if(tS<=0) return out;
    const tb=Math.min(tS,TZ_CHAN.t1), yb=-POOL_H+tb;
    out.push([[tzLeft(0)[0],-POOL_H],[tzRight(0)[1],-POOL_H],
              [tzRight(tb)[1],yb],[tzLeft(tb)[0],yb]]);
    if(tS>TZ_CHAN.t1){
      const l1=tzLeft(TZ_CHAN.t1), l2=tzLeft(tS), r1=tzRight(TZ_CHAN.t1), r2=tzRight(tS);
      const y1=-POOL_H+TZ_CHAN.t1;
      out.push([[l1[0],y1],[l1[1],y1],[l2[1],ySurf],[l2[0],ySurf]]);
      out.push([[r1[0],y1],[r1[1],y1],[r2[1],ySurf],[r2[0],ySurf]]);
    }
    return out;
  }
  if(scene==='chamber'){
    const R=(a,b,y0,y1)=>[[a,y1],[b,y1],[b,y0],[a,y0]];
    return [R(CH_LEFT.x0,CH_LEFT.x1,-POOL_H,CH_OPEN_BOT),
            R(CH_RIGHT.x0,CH_RIGHT.x1,-POOL_H,CH_OPEN_BOT),
            R(CH_LEFT.x1,CH_RIGHT.x0,-2.75,-2.25),
            R(CH_L_SHAFT.x0,CH_L_SHAFT.x1,CH_OPEN_BOT,P.yL),
            R(CH_R_SHAFT.x0,CH_R_SHAFT.x1,CH_OPEN_BOT,P.yR)];
  }
  if(ySurf<=-POOL_H) return [];
  return [[[SQ_X0,ySurf],[SQ_X1,ySurf],[SQ_X1,-POOL_H],[SQ_X0,-POOL_H]]];
}
/* the free-surface segments, drawn last so the waterline reads as a line */
function surfaceSegs(scene,ySurf,P){
  if(scene==='trapezoid'){
    const tS=clamp(ySurf+POOL_H,0,POOL_H);
    if(tS<=0) return [];
    if(tS<=TZ_CHAN.t1) return [[tzLeft(tS)[0],tzRight(tS)[1],ySurf]];
    const l=tzLeft(tS), r=tzRight(tS);
    return [[l[0],l[1],ySurf],[r[0],r[1],ySurf]];
  }
  if(scene==='chamber') return [[CH_L_SHAFT.x0,CH_L_SHAFT.x1,P.yL],[CH_R_SHAFT.x0,CH_R_SHAFT.x1,P.yR]];
  if(ySurf<=-POOL_H) return [];
  return [[SQ_X0,SQ_X1,ySurf]];
}

/* the whole pool picture: ground, cavity, fluid, grid, ruler */
function drawPool(ctx,W,H,b,scene,ySurf,rho,st,P){
  const E=extentFor(scene), map=worldFitUp(b,E,0.05);
  /* the ground: one slab, with the cavities cut out by painting them air */
  worldPoly(ctx,map,[[E.xmin,E.ymin],[E.xmax,E.ymin],[E.xmax,0],[E.xmin,0]],GROUND,GROUND2,1.2);
  const cav=cavityPolys(scene);
  for(const p of cav) worldPoly(ctx,map,p,COL.air,null);
  const col=fluidColour(rho);
  for(const p of fluidPolys(scene,ySurf,P)) worldPoly(ctx,map,p,rgba(col,0.30),null);
  for(const p of cav) worldPoly(ctx,map,p,null,rgba(COL.struct,0.55),1.3);
  for(const s of surfaceSegs(scene,ySurf,P)){
    ctx.beginPath(); ctx.moveTo(map.X(s[0]),map.Y(s[2])); ctx.lineTo(map.X(s[1]),map.Y(s[2]));
    ctx.strokeStyle=rgba(col,0.95); ctx.lineWidth=2; ctx.stroke();
    POLY_SEGS.push(map.X(s[0]),map.Y(s[2]),map.X(s[1]),map.Y(s[2]));
  }
  /* the ground line */
  seg(ctx,map,[E.xmin,0],[E.xmax,0],rgba('#5b6480',0.8),1.2);
  if(st.gridOn) drawGrid(ctx,W,H,map,E,st);
  if(st.rulerOn) drawRuler(ctx,W,H,map,E,st,scene);
  return map;
}
/* PhET's grid: horizontal lines through the pool, labelled in the chosen
   length unit, with the ground as the zero */
function drawGrid(ctx,W,H,map,E,st){
  const u=UNITS[st.units], step=u.lenPer===1?0.5:FT_M;
  ctx.save();
  for(let k=0;k*step<=POOL_H+1e-9;k++){
    const y=-k*step;
    ctx.beginPath(); ctx.moveTo(map.X(E.xmin),map.Y(y)); ctx.lineTo(map.X(E.xmax),map.Y(y));
    ctx.strokeStyle=rgba('#5ac8e0',k%2===0?0.20:0.10); ctx.lineWidth=1; ctx.stroke();
    /* on the RIGHT: the ruler stands on the left and its own numbers were
       landing on the grid's */
    if(k%2===0&&k>0) lab(ctx,W,H,map.X(E.xmax)-4,map.Y(y)-7,fmt(toLen(k*step,st.units),u.lenPer===1?1:0)+' '+u.len,
                         rgba('#5ac8e0',0.75),SM_FONT,'right');
  }
  ctx.restore();
}
/* PhET's ruler: a stick standing beside the pool, in metres or feet */
function drawRuler(ctx,W,H,map,E,st,scene){
  const u=UNITS[st.units], step=u.lenPer===1?0.5:FT_M;
  const x0=E.xmin+0.10, w=0.34;
  worldPoly(ctx,map,[[x0,0.35],[x0+w,0.35],[x0+w,-POOL_H],[x0,-POOL_H]],'#2b3242','#586378',1.2);
  for(let k=0;k*step<=POOL_H+1e-9;k++){
    const y=-k*step, big=(k%2===0);
    seg(ctx,map,[x0,y],[x0+(big?w:w*0.5),y],rgba('#cfd4de',big?0.85:0.45),1);
    if(big) labFixed(ctx,map.X(x0+w)+3,map.Y(y),fmt(toLen(k*step,st.units),u.lenPer===1?1:0),
                     '#aeb6c6',SM_FONT,'left','middle');
  }
  labFixed(ctx,map.X(x0+w/2),map.Y(0.20),u.len,'#aeb6c6',SM_FONT,'center','middle');
}
/* a gauge: the probe dot at its world point and a readout box above it */
function drawGauge(ctx,W,H,map,x,y,G,tag,col,st){
  const X=map.X(x), Y=map.Y(y);
  const txt=G.out?'in the ground':(G.wet?pStr(G.p,st):pStr(G.p,st)+' air');
  ctx.save();
  ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(X,Y-19);
  ctx.strokeStyle=rgba(col,0.85); ctx.lineWidth=1.4; ctx.stroke();
  dot(ctx,X,Y,5,G.wet?col:COL.off,col,1.6);
  ctx.restore();
  /* the probe dot and its stem go into the label registry too: only the box
     was registered, so a stage label could land straight on the marker */
  LABELS.push([X-7,Y-21,X+7,Y+7]);
  const t=plain(tag+'  '+txt);
  ctx.font='bold 11.5px -apple-system, sans-serif';
  const bw=t.length*11.5*0.52+14, bh=19;
  /* the box dodges everything already registered -- two gauges at the same
     height used to stack their boxes on top of each other */
  const cands=[[X-bw/2,Y-19-bh],[X-bw/2,Y+19],[X+14,Y-bh/2],[X-bw-14,Y-bh/2],
               [X-bw/2,Y-19-bh-24],[X-bw/2,Y+19+24],[X+14,Y-bh-20],[X-bw-14,Y+20]];
  let bx=clamp(X-bw/2,2,W-bw-2), by=clamp(Y-19-bh,2,H-bh-2);
  for(const [px,py] of cands){
    const cx2=clamp(px,2,W-bw-2), cy2=clamp(py,2,H-bh-2);
    if(labFits([cx2,cy2,cx2+bw,cy2+bh])){ bx=cx2; by=cy2; break; }
  }
  ctx.fillStyle=rgba('#0a0c12',0.92); ctx.fillRect(bx,by,bw,bh);
  ctx.strokeStyle=rgba(col,0.8); ctx.lineWidth=1.2; ctx.strokeRect(bx+0.5,by+0.5,bw-1,bh-1);
  LABELS.push([bx,by,bx+bw,by+bh]);
  ctx.fillStyle=G.wet?col:COL.dim; ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(t,bx+bw/2,by+bh/2);
  return {x:bx,y:by,w:bw,h:bh};
}
/* the faucet and the drain, drawn as the fixtures they are (this file's
   control is a LEVEL, not a flow rate, so nothing is animated) */
function drawPlumbing(ctx,W,H,map,scene,st){
  const fx=(scene==='trapezoid')?3.19:2.70, dy=-POOL_H;
  worldPoly(ctx,map,[[fx-0.36,0.56],[fx-0.10,0.56],[fx-0.10,0.30],[fx-0.36,0.30]],'#2b3242','#586378',1.1);
  worldPoly(ctx,map,[[fx-0.13,0.44],[fx+0.16,0.44],[fx+0.16,0.30],[fx-0.13,0.30]],'#2b3242','#586378',1.1);
  const dx=(scene==='trapezoid')?7.10:5.60;
  worldPoly(ctx,map,[[dx-0.16,dy],[dx+0.16,dy],[dx+0.16,dy-0.16],[dx-0.16,dy-0.16]],'#2b3242','#586378',1.1);
  lab(ctx,W,H,map.X(fx)+18,map.Y(0.43),'faucet',COL.dim,SM_FONT,'left');
  lab(ctx,W,H,map.X(dx)+16,map.Y(dy-0.08),'drain',COL.dim,SM_FONT,'left');
}

/* ================================================================== *
 *  view A: the pool  (PhET's square pool scene)                       *
 * ================================================================== */
const POOL_CAP_FULL='PhET&rsquo;s square pool scene, drawn at true proportion: '+fmt(SQ_W,1)+' m across, '+fmt(POOL_H,0)
  +' m deep and '+fmt(DEPTH_OUT,0)+' m out of the page, so it holds '+fmt(SQ_VMAX*1000,0)+' L when full. The faucet and '
  +'the drain set the level; the two gauges read p = p_atm + ρgh at whatever point you drag them to, and read the air '
  +'above the surface and nothing at all outside the pool. Put both at the same depth and the two numbers are identical '
  +'to the last digit, however much fluid is standing over each of them. The strip on the right is the same law as a '
  +'line: intercept p_atm, slope ρg, and the two gauges on it.';
const POOL_CAP_SHORT='PhET&rsquo;s square pool at true proportion. Two gauges reading p = p_atm + ρgh, and the same law '
  +'drawn as a line of slope ρg.';

function pDepthPanel(ctx,W,H,b,M,st,marks,title){
  const u=UNITS[st.units];
  const pTop=toUnit(pressureAt(0,M.rho,M.g,M.ySurf===undefined?0:M.ySurf,st.atmosphere),st.units);
  const pBot=toUnit(pressureAt(POOL_H,M.rho,M.g,M.ySurf===undefined?0:M.ySurf,st.atmosphere),st.units);
  const xlo=0, xhi=Math.max(pBot*1.06,pTop+1e-6);
  axesReg(ctx,b,xlo,xhi,POOL_H,0,{nx:5,ny:4,xlab:'pressure, '+u.name,ylab:'depth, m',
    title:titleFor(b,title||'the law as a line: p = p_atm + ρgh','p against depth'),
    xfmt:t=>fmt(t,u.dp===3?2:(u.dp===1?0:1)),yfmt:t=>fmt(t,1)});
  /* the air-pressure intercept */
  polyline(ctx,b,[pTop,pTop],[0,POOL_H],xlo,xhi,POOL_H,0,rgba(COL.ref,0.85),1.4,[5,4]);
  lab(ctx,W,H,b.x+b.w*(pTop-xlo)/(xhi-xlo)+6,b.y+13,'p_atm',COL.ref,SM_FONT,'left');
  /* the law */
  const xs=[],ys=[];
  for(let i=0;i<=60;i++){ const d=POOL_H*i/60;
    xs.push(toUnit(pressureAt(d,M.rho,M.g,M.ySurf===undefined?0:M.ySurf,st.atmosphere),st.units)); ys.push(d); }
  polyline(ctx,b,xs,ys,xlo,xhi,POOL_H,0,COL.pos,1.8);
  /* the part of the axis the fluid actually occupies */
  const dMax=(M.level===undefined)?POOL_H:M.level;
  polyline(ctx,b,[xlo,xhi],[dMax,dMax],xlo,xhi,POOL_H,0,rgba(COL.struct,0.55),1.2,[3,3]);
  lab(ctx,W,H,b.x1-5,b.y1-b.h*(POOL_H-dMax)/POOL_H-11,'the floor',COL.struct,SM_FONT,'right');
  for(const m of marks){
    if(!m.G.wet) continue;
    marker(ctx,b,xlo,xhi,POOL_H,0,toUnit(m.G.p,st.units),m.G.depth,m.col);
    lab(ctx,W,H,b.x+b.w*(toUnit(m.G.p,st.units)-xlo)/(xhi-xlo)+9,b.y1-b.h*(POOL_H-m.G.depth)/POOL_H,
        m.tag,m.col,SM_FONT,'left');
  }
  /* the slope is quoted in the unit the axis is drawn in, not always in kPa */
  lab(ctx,W,H,b.x+4,b.y1-8,'slope ρg = '+sigf(toUnit(M.rho*M.g,st.units),4)+' '+u.name+'/m',
      COL.pos,SM_FONT,'left');
}

function drawPoolView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,POOL_CAP_FULL,POOL_CAP_SHORT,0,0);
  const S=splitMain(L,W,0.56,1);
  const map=drawPool(ctx,W,H,S.pool,'square',M.ySurf,M.rho,st,null);
  drawPlumbing(ctx,W,H,map,'square',st);
  /* the gauges go down FIRST so every prose label below dodges their boxes */
  drawGauge(ctx,W,H,map,st.gAx,st.gAy,M.A,'A',COL.live,st);
  drawGauge(ctx,W,H,map,st.gBx,st.gBy,M.B,'B',COL.pos,st);
  lab(ctx,W,H,map.X((SQ_X0+SQ_X1)/2),map.Y(M.ySurf)-13,
      fluidName(M.rho)+' · '+fmt(1000*M.V,0)+' L · '+fmt(M.level,2)+' m deep',
      fluidColour(M.rho),SM_FONT,'center');
  lab(ctx,W,H,map.X(SQ_X0),map.Y(-POOL_H)+15,
      'true proportion · '+fmt(DEPTH_OUT,0)+' m out of the page',COL.dim,SM_FONT,'left');
  if(!st.atmosphere) lab(ctx,W,H,map.X((SQ_X0+SQ_X1)/2),map.Y(0.42),'atmosphere OFF — gauge pressure only',
                         COL.ref,SM_FONT,'center');
  if(S.rows.length) pDepthPanel(ctx,W,H,S.rows[0],M,st,
    [{G:M.A,tag:'A',col:COL.live},{G:M.B,tag:'B',col:COL.pos}]);
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view B: the shapes  (PhET's trapezoid pool scene)                  *
 * ================================================================== */
const SHAPE_CAP_FULL='PhET&rsquo;s trapezoid pool: two chambers that taper in opposite directions, joined by a channel '
  +'along the floor. The left one is '+fmt(TZ_WTOP,2)+' m across at the top and '+fmt(TZ_WBOT,2)+' m at the bottom; the '
  +'right one is the same shape upside down. Put one gauge in each at the same depth and they read the same number, even '
  +'though the fluid standing above them differs by a factor of several — this is the hydrostatic paradox, and the panel '
  +'on the right shows why the level behaves so simply: the two widths are equal and opposite linear functions of height, '
  +'so they SUM to a constant '+fmt(TZ_WSUM,2)+' m. PhET&rsquo;s own floor channel stops 7 cm short of the right '
  +'chamber; this file closes that gap so the fluid is one connected body.';
const SHAPE_CAP_SHORT='PhET&rsquo;s trapezoid pool. Two opposite tapers, one level, one pressure at one depth — and two '
  +'widths that sum to a constant.';

function widthPanel(ctx,W,H,b,M,st){
  const xs=[],wl=[],wr=[],ws=[];
  for(let i=0;i<=60;i++){ const t=POOL_H*i/60, l=tzLeft(t), r=tzRight(t);
    xs.push(t); wl.push(l[1]-l[0]); wr.push(r[1]-r[0]); ws.push((l[1]-l[0])+(r[1]-r[0])); }
  const hi=TZ_WSUM*1.12;
  axesReg(ctx,b,0,POOL_H,0,hi,{nx:4,ny:4,xlab:'height above the floor, m',ylab:'width, m',
    title:titleFor(b,'the two chambers, and their constant sum','widths')});
  polyline(ctx,b,xs,wl,0,POOL_H,0,hi,COL.live,1.7);
  polyline(ctx,b,xs,wr,0,POOL_H,0,hi,COL.struct,1.7);
  polyline(ctx,b,xs,ws,0,POOL_H,0,hi,COL.pos,2.0);
  polyline(ctx,b,[M.level,M.level],[0,hi],0,POOL_H,0,hi,rgba(COL.ref,0.7),1.2,[4,3]);
  legendReg(ctx,b,[[COL.live,'left chamber'],[COL.struct,'right chamber'],
                    [COL.pos,'sum = '+fmt(TZ_WSUM,2)+' m']]);
  lab(ctx,W,H,b.x+b.w*M.level/POOL_H+6,b.y1-10,'the level',COL.ref,SM_FONT,'left');
}

function drawShapesView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,SHAPE_CAP_FULL,SHAPE_CAP_SHORT,0,0);
  const S=splitMain(L,W,0.58,1);
  const map=drawPool(ctx,W,H,S.pool,'trapezoid',M.ySurf,M.rho,st,null);
  drawPlumbing(ctx,W,H,map,'trapezoid',st);
  drawGauge(ctx,W,H,map,st.gAx,st.gAy,M.A,'A',COL.live,st);
  drawGauge(ctx,W,H,map,st.gBx,st.gBy,M.B,'B',COL.pos,st);
  /* PhET's own gap, marked where it is */
  seg(ctx,map,[TZ_CHAN_PHET_X1,-POOL_H],[TZ_CHAN_PHET_X1,-POOL_H+0.17],rgba(COL.ref,0.8),1.4,[3,2]);
  lab(ctx,W,H,map.X(TZ_CHAN_PHET_X1)+5,map.Y(-POOL_H+0.34),'PhET stops here',COL.ref,SM_FONT,'left');
  lab(ctx,W,H,map.X((tzLeft(M.level)[0]+tzLeft(M.level)[1])/2),map.Y(M.ySurf)-12,
      fmt(M.wLeft,2)+' m',COL.live,SM_FONT,'center');
  lab(ctx,W,H,map.X((tzRight(M.level)[0]+tzRight(M.level)[1])/2),map.Y(M.ySurf)-12,
      fmt(M.wRight,2)+' m',COL.struct,SM_FONT,'center');
  if(M.A.wet&&M.B.wet){
    seg(ctx,map,[tzLeft(0)[0],st.gAy],[tzRight(0)[1],st.gAy],rgba(COL.pos,0.30),1,[4,4]);
    lab(ctx,W,H,map.X(tzLeft(0)[0])+4,map.Y(st.gAy)+12,
        M.sameDepth?('same depth — the readings differ by '+(M.dP<1e-9?'nothing':fmt(M.dP,3)+' Pa'))
                   :('depths differ by '+fmt(Math.abs(M.A.depth-M.B.depth),3)+' m'),
        M.sameDepth?COL.pos:COL.ref,SM_FONT,'left');
  }
  lab(ctx,W,H,map.X(tzLeft(0)[0]),map.Y(-POOL_H)+15,
      'true proportion · '+fmt(DEPTH_OUT,0)+' m out of the page · holds '+fmt(1000*M.V,0)+' L',
      COL.dim,SM_FONT,'left');
  if(S.rows.length) widthPanel(ctx,W,H,S.rows[0],M,st);
  drawCaption(ctx,L);
}
