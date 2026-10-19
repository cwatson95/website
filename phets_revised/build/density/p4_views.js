/* ================================================================== *
 *  the pool stage, shared by three views, then view A and view B      *
 * ================================================================== */
/* every layout reserves HINT_H at the bottom: the house #hint is HTML at
   bottom:11px and the canvas capture cannot see it, so a caption anchored at
   H - 12 would sit underneath it (Known-bad, wave-on-a-string) */
function layout(ctx,W,H,full,short,nB,frac,nBn){
  const L=stageLayout(ctx,W,H-HINT_H,full,short,nB,frac,nBn);
  /* the caption is painted LAST but occupies the bottom band from the moment
     the layout is known, so its rectangle goes into the registry FIRST — a
     stage label placed near the bottom otherwise dodges nothing and lands on
     the prose (found at 620 x 420) */
  LABELS.push([L.left-2,L.capY-5,L.left+L.capW+2,H-HINT_H-6]);
  return L;
}
/* a label that must be drawn where it is (a tag inside its own block): it is
   painted unconditionally AND registered, so every dodging lab() after it
   moves out of its way instead of landing on top of it */
function labFixed(ctx,x,y,txt,col,font,align,base){
  ctx.fillStyle=col; ctx.font=font;
  ctx.textAlign=align||'center'; ctx.textBaseline=base||'middle';
  const t=plain(txt), fs=parseFloat(font.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  const lx=align==='right'?x-w:(align==='left'?x:x-w/2);
  const ly=base==='top'?y:(base==='bottom'?y-hh:y-hh/2);
  LABELS.push([lx,ly,lx+w,ly+hh]);
  ctx.fillText(t,x,y);
}
/* axes(), with the TICK LABELS, the axis names and the title registered.
   axesR registers only the title, which left every dodging label free to land
   on a tick (Known-bad: axes() draws its title outside any registry — the same
   argument applies to everything else it draws). */
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
/* the world the pool stage draws.  'wide' leaves room on the ground to the
   left for a scale with a block standing on it. */
/* The top of the world is only as high as a lifted block can reach (the drag
   is clamped to keep its top inside), because empty sky is height the picture
   could have spent on the pool: at ymax = 0.30 the drawn content filled 62 %
   of the box. */
const POOL_YTOP=0.22, POOL_YTOP_WIDE=0.30;
function poolExtent(kind){
  return kind==='wide'?{xmin:-0.72,xmax:0.60,ymin:-(POOL_H+0.05),ymax:POOL_YTOP_WIDE}
                      :{xmin:-0.58,xmax:0.58,ymin:-(POOL_H+0.05),ymax:POOL_YTOP};
}
/* the highest a block of side s may be held: its top stays inside the world */
function holdCeiling(s){ return POOL_YTOP-s-0.012; }
const GROUND='#20242e', GROUND2='#171b23';
/* A wide stage drawing a nearly square picture at equal aspect (which a pool
   must be — it is a SHAPE) wastes two thirds of its width, so the pool takes
   the left of the stage and the analysis panels stack down the right.  Below
   the narrow threshold the split collapses and only the pool is drawn. */
function splitMain(L,W,fracLeft,nRight){
  const b=L.main;
  if(isNarrow(W)||nRight<1) return {pool:b,rows:[]};
  const gut=70, wl=Math.round(b.w*fracLeft);
  const pool=box(b.x,b.y,Math.max(120,wl-gut/2),b.h);
  const rx=b.x+wl+gut/2, rw=Math.max(150,b.x1-rx);
  const rows=[], slot=b.h/nRight;
  for(let i=0;i<nRight;i++) rows.push(box(rx,b.y+i*slot+26,rw,Math.max(60,slot-70)));
  return {pool:pool,rows:rows};
}

/* the pool seen from the front, in true proportion (a pool is a SHAPE, so the
   two axes share one scale; the scale bar says what it is) */
function drawPoolStage(ctx,W,H,b,yw,blocks,opt){
  opt=opt||{};
  const E=poolExtent(opt.kind), map=worldFitUp(b,E,0.01);
  const gy=E.ymin;
  worldPoly(ctx,map,[[E.xmin,gy],[-POOL_W/2,gy],[-POOL_W/2,0],[E.xmin,0]],GROUND,GROUND2,1);
  worldPoly(ctx,map,[[POOL_W/2,gy],[E.xmax,gy],[E.xmax,0],[POOL_W/2,0]],GROUND,GROUND2,1);
  worldPoly(ctx,map,[[-POOL_W/2,gy],[POOL_W/2,gy],[POOL_W/2,-POOL_H],[-POOL_W/2,-POOL_H]],GROUND,GROUND2,1);
  /* the water */
  fluidRect(ctx,map,-POOL_W/2,POOL_W/2,-POOL_H,yw,rgba(COL.struct,0.17));
  if(opt.bare!==undefined&&Math.abs(opt.bare-yw)>1e-6)
    seg(ctx,map,[-POOL_W/2,opt.bare],[POOL_W/2,opt.bare],rgba(COL.ref,0.75),1.2,[4,3]);
  /* the blocks */
  for(const bk of blocks){
    const s=bk.s, x=bk.x, y0=bk.yb;
    if(bk.mode==='out') continue;
    worldPoly(ctx,map,[[x-s/2,y0],[x+s/2,y0],[x+s/2,y0+s],[x-s/2,y0+s]],bk.col,'#0b0f18',1.4);
    /* the part under water, restated in green — the quantity the sim computes */
    if(bk.Vsub>0){
      const ytop=Math.min(y0+s,yw);
      worldPoly(ctx,map,[[x-s/2,y0],[x+s/2,y0],[x+s/2,ytop],[x-s/2,ytop]],rgba(COL.pos,0.16),null);
    }
    if(bk.tag) labFixed(ctx,map.X(x),map.Y(y0+s/2),bk.tag,'#0b0f18','bold 13px -apple-system, sans-serif','center','middle');
    /* the block's own rectangle goes into the label registry: a force label
       painted over the block it belongs to is unreadable, and with two blocks
       26 px apart there is no room for one between them */
    LABELS.push([map.X(x-s/2),map.Y(y0+s),map.X(x+s/2),map.Y(y0)]);
  }
  return map;
}
/* ONE arrow-length scale for the whole picture (so two blocks' arrows really
   can be compared), chosen so that the longest arrow still fits between the
   pool floor and the top of the drawn world; the labels sit beside the block
   rather than at the arrow tips, which put them inside it. */
function forceScale(blocks,kind){
  const ceil=poolExtent(kind).ymax-0.012, floor=-POOL_H-0.018;
  let room=1, Fref=1;
  for(const b of blocks){
    const cy=b.yb+b.s/2; room=Math.min(room,cy-floor,ceil-cy);
    Fref=Math.max(Fref,b.W,b.Fb,Math.abs(b.mode==='held'?b.hand:b.N));
  }
  /* the reference force is computed HERE, with the length, so that a draw call
     cannot hand one block its own weight as the scale and quietly make the
     arrows incomparable */
  return {len:Math.max(0.035,Math.min(0.13,room)),Fref:Fref};
}
/* the drawn length of each arrow, lifted OUT of the draw call so the one
   scale can be asserted: a quantity only the picture can check is in the
   wrong layer (Known-bad, sbs_sims) */
function forceLengths(bk,FS){
  const Fref=FS.Fref, len=FS.len;
  const fr=f=>Math.min(Math.abs(f)/Math.max(Fref,1e-12),1);
  const extra=bk.mode==='held'?bk.hand:bk.N;
  return {W:len*fr(bk.W),Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};
}
function drawForces(ctx,W,H,map,bk,FS,opt){
  opt=opt||{};
  const cx=bk.x, s=bk.s, cy=bk.yb+s/2, A=forceLengths(bk,FS);
  arrowW(ctx,map,[cx-0.22*s,cy],[0,-A.W],COL.ref,2);
  arrowW(ctx,map,[cx+0.22*s,cy],[0,A.Fb],COL.pos,2);
  const extra=A.raw;
  if(Math.abs(extra)>1e-9)
    arrowW(ctx,map,[cx+0.55*s+0.012,cy],[0,A.sign*A.extra],COL.live,2);
  if(!opt.labels) return;
  lab(ctx,W,H,map.X(cx-s/2)-8,map.Y(cy)-11,'W '+fmt(bk.W,1)+' N',COL.ref,SM_FONT,'right');
  lab(ctx,W,H,map.X(cx+s/2)+10,map.Y(cy)-11,'Fb '+fmt(bk.Fb,1)+' N',COL.pos,SM_FONT,'left');
  if(Math.abs(extra)>1e-9)
    lab(ctx,W,H,map.X(cx+s/2)+10,map.Y(cy)+11,(bk.mode==='held'?'hand ':'N ')+fmt(Math.abs(extra),1)+' N',
        COL.live,SM_FONT,'left');
}

/* ================================================================== *
 *  view: the pool  (PhET's Intro screen)                              *
 * ================================================================== */
const POOL_CAP_FULL='PhET&rsquo;s Intro screen. One or two cubes in a '+fmt(POOL_W*100,0)+' × '+fmt(POOL_D*100,0)
  +' × '+fmt(POOL_H*100,1)+' cm pool holding '+fmt(VF0*LITERS,0)+' L of water. Pick the material and the '
  +'density is fixed, so mass and volume move together (m = ρV); pick <i>custom</i> and they come apart and the '
  +'density follows. The pool is drawn in true proportion &mdash; both axes at the same scale &mdash; and the green wash '
  +'is the submerged part, whose volume is what the upthrust weighs. The dashed orange line is where the water stood '
  +'before the blocks went in. Drag a block to hold it under or lift it clear; let go and it returns to equilibrium.';
const POOL_CAP_SHORT='PhET&rsquo;s Intro screen: cubes in a 100 L pool, true proportion, green = the submerged part, '
  +'dashed orange = the level before. Drag a block.';

function poolGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,POOL_CAP_FULL,POOL_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.60,2);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent(),0.01)};
}
/* the three forces as bars, one group per block */
function drawForceBars(ctx,W,H,b,blocks,Fref){
  const n=blocks.length, gh=Fref*1.15;
  axesReg(ctx,b,0,n*3+1,0,gh,{title:titleFor(b,'weight, upthrust, and what the floor takes','the forces'),
    ylab:'newtons',nx:1,ny:5,xticks:[],yfmt:t=>fmt(t,0)});
  blocks.forEach((bk,i)=>{
    const base=i*3+1;
    const bars=[[base,bk.W,COL.ref,'W'],[base+0.75,bk.Fb,COL.pos,'Fb'],
                [base+1.5,bk.mode==='held'?Math.abs(bk.hand):bk.N,COL.live,bk.mode==='held'?'hand':'N']];
    for(const bar of bars){
      const X=b.x+b.w*bar[0]/(n*3+1), Wd=b.w*0.6/(n*3+1);
      const Yv=b.y1-b.h*clamp(bar[1],0,gh)/gh;
      ctx.fillStyle=rgba(bar[2],0.55); ctx.fillRect(X,Yv,Wd,b.y1-Yv);
      ctx.strokeStyle=bar[2]; ctx.lineWidth=1.2; ctx.strokeRect(X,Yv,Wd,b.y1-Yv);
      lab(ctx,W,H,X+Wd/2,Yv-8,bar[3],bar[2],SM_FONT,'center');
    }
    lab(ctx,W,H,b.x+b.w*(base+0.75)/(n*3+1),b.y1+13,bk.tag,'#aeb6c6',LAB_FONT,'center');
  });
}
function drawPoolView(ctx,W,H,M,st){
  st=st||ST;
  const G2=poolGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  /* the right column goes FIRST so that its axis names and tick labels are in
     the registry before any stage label is placed; otherwise a stage label
     dodges nothing and lands on a neighbouring panel's ticks (Known-bad: a
     panel's tick gutter is part of its footprint) */
  if(SP.rows.length>1){
    const b1=SP.rows[0], maxL=24;
    const xs=[], ys=[];
    for(let i=0;i<=40;i++){ const q=maxL*i/40; xs.push(q); ys.push(100*(M.bare+POOL_H+q/LITERS/A_POOL)); }
    const ylo=100*(M.bare+POOL_H), yhi=ys[ys.length-1];
    axesReg(ctx,b1,0,maxL,ylo-0.4,yhi+0.4,{title:titleFor(b1,'the level rises by V/A','the level'),
      xlab:'litres pushed aside',ylab:'level above the floor, cm',nx:5,ny:5,
      xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
    polyline(ctx,b1,xs,ys,0,maxL,ylo-0.4,yhi+0.4,COL.pos,1.8);
    marker(ctx,b1,0,maxL,ylo-0.4,yhi+0.4,M.VfDisp*LITERS,100*(M.yw+POOL_H),COL.live);
    lab(ctx,W,H,b1.x1-6,b1.y+12,'slope 1/A = '+fmt(100/A_POOL/LITERS,3)+' cm per litre',COL.pos,SM_FONT,'right');
    drawForceBars(ctx,W,H,SP.rows[1],M.blocks,forceScale(M.blocks).Fref);
  }
  const map=drawPoolStage(ctx,W,H,SP.pool,M.yw,M.blocks,{bare:M.bare});
  if(st.forces){
    const FS=forceScale(M.blocks);
    for(const b of M.blocks) drawForces(ctx,W,H,map,b,FS,{labels:st.levels});
    lab(ctx,W,H,map.X(POOL_W/2)-6,map.Y(0.035),'arrows to one scale: the longest is '+fmt(FS.Fref,1)+' N',
        COL.dim,SM_FONT,'right');
  }
  /* the waterline, named INSIDE the water so a block above it cannot clash */
  lab(ctx,W,H,map.X(-POOL_W/2)+7,map.Y(-POOL_H+0.022),'water '+fmt((M.yw+POOL_H)*A_POOL*LITERS,1)+' L',COL.struct,LAB_FONT,'left');
  const x0=POOL_W/2-0.1;
  seg(ctx,map,[x0,-POOL_H-0.028],[x0+0.1,-POOL_H-0.028],COL.dim,1.4);
  lab(ctx,W,H,map.X(x0+0.05),map.Y(-POOL_H-0.028)+11,'10 cm',COL.dim,SM_FONT,'center');
  if(M.blocks.some(b=>b.mode==='held'))
    lab(ctx,W,H,map.X(0),map.Y(POOL_YTOP-0.015),'held — let go and it returns to equilibrium',COL.live,LAB_FONT,'center');

  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: the sets  (PhET's Compare screen)                            *
 * ================================================================== */
const SETS_CAP_FULL='PhET&rsquo;s Compare screen. Four blocks matched in one of the three quantities, with that '
  +'quantity on the slider and the other two forced by ρ = m/V. Matched in MASS the big ones are the light ones; '
  +'matched in VOLUME the big reading on the scale is the dense one; matched in DENSITY every one of them floats to '
  +'exactly the same fraction of its own side, whatever its size &mdash; which is the floating law with the size '
  +'divided out. The panel beside it is the mass-volume plane: a matched set is a straight line through it, horizontal, '
  +'vertical, or through the origin.';
const SETS_CAP_SHORT='PhET&rsquo;s Compare screen: four blocks matched in mass, volume or density, and the same four '
  +'as points in the mass-volume plane.';

function setsGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,SETS_CAP_FULL,SETS_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.60,1);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent(),0.01)};
}
function drawSetsView(ctx,W,H,M,st){
  st=st||ST;
  const G2=setsGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  const b1=SP.rows[0];
  if(b1){
    const xmax=VMAX_L*1.05, ymax=Math.max(12,Math.max.apply(null,M.blocks.map(b=>b.m))*1.25);
    axesReg(ctx,b1,0,xmax,0,ymax,{title:titleFor(b1,'the same four blocks in the mass-volume plane','mass and volume'),
      xlab:'volume, litres',ylab:'mass, kg',nx:6,ny:5,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
    /* water's ray, the reference that decides everything */
    polyline(ctx,b1,[0,xmax],[0,xmax*RHO_WATER/LITERS],0,xmax,0,ymax,COL.ref,1.4,[5,4]);
    lab(ctx,W,H,b1.x+b1.w*0.72,b1.y1-b1.h*(0.72*xmax*RHO_WATER/LITERS)/ymax-10,'water, 1 kg per litre',COL.ref,SM_FONT,'left');
    /* the line the matched set lies on */
    const set=M.blocks;
    if(st.setMode==='mass') polyline(ctx,b1,[0,xmax],[st.sameMass,st.sameMass],0,xmax,0,ymax,COL.pos,1.6);
    else if(st.setMode==='volume') polyline(ctx,b1,[st.sameVolL,st.sameVolL],[0,ymax],0,xmax,0,ymax,COL.pos,1.6);
    else polyline(ctx,b1,[0,xmax],[0,xmax*st.sameRho/LITERS],0,xmax,0,ymax,COL.pos,1.6);
    for(const bk of set){
      marker(ctx,b1,0,xmax,0,ymax,bk.V*LITERS,bk.m,bk.col);
      lab(ctx,W,H,b1.x+b1.w*(bk.V*LITERS)/xmax+8,b1.y1-b1.h*bk.m/ymax-2,bk.tag,bk.col,SM_FONT,'left');
    }
  }
  const map=drawPoolStage(ctx,W,H,SP.pool,M.yw,M.blocks,{});
  M.blocks.forEach(bk=>{
    lab(ctx,W,H,map.X(bk.x),map.Y(bk.yb+bk.s)-11,sigf(bk.rho,4),bk.mode==='float'?COL.pos:COL.ref,SM_FONT,'center');
  });
  lab(ctx,W,H,map.X(-POOL_W/2)+7,map.Y(-POOL_H+0.022),'water',COL.struct,LAB_FONT,'left');
  if(M.nNeutral>0)
    lab(ctx,W,H,map.X(0),map.Y(0.045),'one block is exactly water: it neither floats nor presses on the floor',COL.live,LAB_FONT,'center');

  drawCaption(ctx,L);
}
