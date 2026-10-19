/* ================================================================== *
 *  the pool stage (shared with density.html), then view A and view B  *
 * ================================================================== */
/* every layout reserves HINT_H at the bottom: the house #hint is HTML at
   bottom:11px and the canvas capture cannot see it, so a caption anchored at
   H - 12 would sit underneath it (Known-bad, wave-on-a-string).  The caption's
   own band is registered here too, so a stage label near the bottom dodges it
   instead of landing on the prose. */
function layout(ctx,W,H,full,short,nB,frac,nBn){
  const L=stageLayout(ctx,W,H-HINT_H,full,short,nB,frac,nBn);
  LABELS.push([L.left-2,L.capY-5,L.left+L.capW+2,H-HINT_H-6]);
  return L;
}
/* a label that must be drawn where it is (a tag inside its own block): painted
   unconditionally AND registered, so every dodging lab() after it moves aside */
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
/* the world the pool stage draws — wide enough for a scale standing on the
   ground to the left of the pool, and no higher than a lifted block reaches */
const POOL_YTOP=0.30;
function poolExtent(){ return {xmin:-0.76,xmax:0.60,ymin:-(POOL_H+0.05),ymax:POOL_YTOP}; }
function holdCeiling(s){ return POOL_YTOP-s-0.012; }
const GROUND='#20242e', GROUND2='#171b23';
/* a wide stage drawing a nearly square picture at equal aspect wastes two
   thirds of its width, so the pool takes the left and the panels stack right */
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
/* a scale standing on a surface: PhET's 0.15 x 0.06 m box with its reading */
function drawScale(ctx,W,H,map,x,ybase,text,col,onPost){
  const w=SCALE_W, hgt=SCALE_H;
  if(onPost){
    worldPoly(ctx,map,[[x-0.012,-POOL_H],[x+0.012,-POOL_H],[x+0.012,ybase],[x-0.012,ybase]],'#1b2028','#2e3644',1);
  }
  worldPoly(ctx,map,[[x-w/2,ybase],[x+w/2,ybase],[x+w/2,ybase+hgt],[x-w/2,ybase+hgt]],'#232936','#3d4658',1.4);
  labFixed(ctx,map.X(x),map.Y(ybase+hgt/2),text,col||COL.pos,'bold 12px -apple-system, sans-serif','center','middle');
  return ybase+hgt;
}
/* the pool seen from the front, in true proportion (a pool is a SHAPE) */
function drawPoolStage(ctx,W,H,b,yw,blocks,opt){
  opt=opt||{};
  const E=poolExtent(), map=worldFitUp(b,E,0.01), gy=E.ymin;
  worldPoly(ctx,map,[[E.xmin,gy],[-POOL_W/2,gy],[-POOL_W/2,0],[E.xmin,0]],GROUND,GROUND2,1);
  worldPoly(ctx,map,[[POOL_W/2,gy],[E.xmax,gy],[E.xmax,0],[POOL_W/2,0]],GROUND,GROUND2,1);
  worldPoly(ctx,map,[[-POOL_W/2,gy],[POOL_W/2,gy],[POOL_W/2,-POOL_H],[-POOL_W/2,-POOL_H]],GROUND,GROUND2,1);
  fluidRect(ctx,map,-POOL_W/2,POOL_W/2,-POOL_H,yw,rgba(fluidColor(opt.fluid),0.22));
  if(opt.bare!==undefined&&Math.abs(opt.bare-yw)>1e-6)
    seg(ctx,map,[-POOL_W/2,opt.bare],[POOL_W/2,opt.bare],rgba(COL.ref,0.75),1.2,[4,3]);
  for(const bk of blocks){
    const s=bk.s, x=bk.x, y0=bk.yb;
    worldPoly(ctx,map,[[x-s/2,y0],[x+s/2,y0],[x+s/2,y0+s],[x-s/2,y0+s]],bk.col,'#0b0f18',1.4);
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
/* each fluid gets its own tint, so a fluid chip visibly changes the pool */
function fluidColor(id){
  if(id==='mercury') return '#9aa3b4';
  if(id==='honey') return '#c9962a';
  if(id==='gasoline') return '#c9c04a';
  if(id==='oil') return '#9c8a34';
  if(id==='seawater') return '#3aa0b0';
  return COL.struct;
}
/* ONE arrow-length scale for the whole picture, with the reference force
   computed here so a draw call cannot make the arrows incomparable */
function forceScale(blocks){
  const ceil=POOL_YTOP-0.012, floor=-POOL_H-0.018;
  let room=1, Fref=1;
  for(const b of blocks){
    const cy=b.yb+b.s/2; room=Math.min(room,cy-floor,ceil-cy);
    Fref=Math.max(Fref,b.W,b.Fb,Math.abs(b.mode==='held'?b.hand:b.N));
  }
  return {len:Math.max(0.035,Math.min(0.13,room)),Fref:Fref};
}
/* the drawn length of each arrow, lifted OUT of the draw call so the one scale
   can be asserted (a quantity only the picture can check is in the wrong layer) */
function forceLengths(bk,FS){
  const Fref=FS.Fref, len=FS.len;
  const fr=f=>Math.min(Math.abs(f)/Math.max(Fref,1e-12),1);
  const extra=bk.mode==='held'?bk.hand:bk.N;
  return {W:len*fr(bk.W),Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};
}
/* PhET's three arrows: gravity down, buoyancy up, contact up */
function drawForces(ctx,W,H,map,bk,FS,opt){
  opt=opt||{};
  const cx=bk.x, s=bk.s, cy=bk.yb+s/2, A=forceLengths(bk,FS);
  arrowW(ctx,map,[cx-0.22*s,cy],[0,-A.W],COL.ref,2);
  arrowW(ctx,map,[cx+0.22*s,cy],[0,A.Fb],COL.pos,2);
  if(Math.abs(A.raw)>1e-9)
    arrowW(ctx,map,[cx+0.55*s+0.012,cy],[0,A.sign*A.extra],COL.live,2);
  if(!opt.labels) return;
  lab(ctx,W,H,map.X(cx-s/2)-8,map.Y(cy)-11,'gravity '+fmt(bk.W,1)+' N',COL.ref,SM_FONT,'right');
  lab(ctx,W,H,map.X(cx+s/2)+10,map.Y(cy)-11,'buoyancy '+fmt(bk.Fb,1)+' N',COL.pos,SM_FONT,'left');
  if(Math.abs(A.raw)>1e-9)
    lab(ctx,W,H,map.X(cx+s/2)+10,map.Y(cy)+11,(bk.mode==='held'?'hand ':'contact ')+fmt(Math.abs(A.raw),1)+' N',
        COL.live,SM_FONT,'left');
}

/* ================================================================== *
 *  view: the pool  (PhET's Explore screen)                            *
 * ================================================================== */
const EXP_CAP_FULL='PhET&rsquo;s Explore screen. One or two cubes in a '+fmt(POOL_W*100,0)+' × '+fmt(POOL_D*100,0)
  +' × '+fmt(POOL_H*100,1)+' cm pool holding '+fmt(VF0*LITERS,0)+' L of a fluid you choose, with the three forces '
  +'PhET draws: gravity down in orange, buoyancy up in green, and whatever the floor or the scale still has to take in '
  +'magenta. All three arrows are on ONE length scale, printed on the stage. Block A can stand on the pool floor, on the '
  +'scale in the pool, or on the scale on the ground &mdash; in air it weighs &rho;<sub>b</sub>gV, under the fluid it '
  +'presses down by exactly that less the weight of the fluid it pushed aside. Drag a block to hold it under or lift it clear.';
const EXP_CAP_SHORT='PhET&rsquo;s Explore screen: cubes in a chosen fluid, the three forces to one scale, and two '
  +'scales in newtons. Drag a block.';

function exploreGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,EXP_CAP_FULL,EXP_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.62,2);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent(),0.01)};
}
function drawForceBars(ctx,W,H,b,blocks,Fref){
  const n=blocks.length, gh=Fref*1.15;
  axesReg(ctx,b,0,n*3+1,0,gh,{title:titleFor(b,'gravity, buoyancy and contact','the forces'),
    ylab:'newtons',nx:1,ny:5,xticks:[],yfmt:t=>fmt(t,0)});
  blocks.forEach((bk,i)=>{
    const base=i*3+1;
    const bars=[[base,bk.W,COL.ref,'g'],[base+0.75,bk.Fb,COL.pos,'b'],
                [base+1.5,bk.mode==='held'?Math.abs(bk.hand):bk.N,COL.live,bk.mode==='held'?'hand':'c']];
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
/* the submerged fraction of block A against the fluid density, across PhET's
   six fluids — the same law the float-or-sink view draws, for one block */
function drawFluidStrip(ctx,W,H,b,M,st){
  const rho=M.blocks[0].rho, lo=300, hi=14500, lx=v=>Math.log10(v);
  axesReg(ctx,b,lx(lo),lx(hi),0,1.08,{title:titleFor(b,'how much of block A is under, in each fluid','in each fluid'),
    xlab:'fluid density, kg/m3 (log)',ylab:'fraction under',nx:1,ny:5,
    xticks:b.w<300?[lx(680),lx(13593)]:[lx(680),lx(1000),lx(1440),lx(13593)],
    xfmt:t=>fmt(Math.pow(10,t),0),yfmt:t=>fmt(t,2)});
  const xs=[], ys=[];
  for(let i=0;i<=200;i++){ const v=Math.pow(10,lx(lo)+(lx(hi)-lx(lo))*i/200); xs.push(lx(v)); ys.push(submergedFraction(rho,v)); }
  polyline(ctx,b,xs,ys,lx(lo),lx(hi),0,1.08,COL.pos,1.8);
  for(const f of BUOY_FLUIDS){
    const rf=MAT[f].phet, X=b.x+b.w*(lx(rf)-lx(lo))/(lx(hi)-lx(lo)), Y=b.y1-b.h*submergedFraction(rho,rf)/1.08;
    const here=(f===st.fluid);
    dot(ctx,X,Y,here?5:3,here?COL.live:COL.pos,'#0b0f18',1);
    if(here) lab(ctx,W,H,X,Y-10,MAT[f].name,COL.live,SM_FONT,'center','bottom');
  }
  /* the block's own density, where the curve reaches 1 */
  const Xr=b.x+b.w*(lx(clamp(rho,lo,hi))-lx(lo))/(lx(hi)-lx(lo));
  ctx.strokeStyle=rgba(COL.ref,0.7); ctx.lineWidth=1.1; ctx.setLineDash([4,3]);
  ctx.beginPath(); ctx.moveTo(Xr,b.y); ctx.lineTo(Xr,b.y1); ctx.stroke(); ctx.setLineDash([]);
  /* a block lighter than the axis floor is drawn ON the floor, and the label
     says so rather than letting the dashed line be read as the axis */
  lab(ctx,W,H,Xr+6,b.y+12,'rho_b = '+sigf(rho,4)+(rho<lo?' (off the axis)':''),COL.ref,SM_FONT,'left');
}
function drawExploreView(ctx,W,H,M,st){
  st=st||ST;
  const G2=exploreGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  if(SP.rows.length>1){
    drawFluidStrip(ctx,W,H,SP.rows[0],M,st);
    drawForceBars(ctx,W,H,SP.rows[1],M.blocks,forceScale(M.blocks).Fref);
  }
  const inPool=M.blocks.filter(b=>b.mode!=='out');
  const map=drawPoolStage(ctx,W,H,SP.pool,M.yw,inPool,{bare:M.bare,fluid:st.fluid});
  /* PhET's two scales */
  drawScale(ctx,W,H,map,SCALE_X,M.scaleY0,st.where==='poolscale'?fmt(M.poolReads,1)+' N':'0.0 N',
            st.where==='poolscale'?COL.pos:COL.dim,true);
  drawScale(ctx,W,H,map,GROUND_SCALE_X,0,st.where==='ground'?fmt(M.groundReads,1)+' N':'0.0 N',
            st.where==='ground'?COL.pos:COL.dim,false);
  lab(ctx,W,H,map.X(SCALE_X),map.Y(M.scaleY0)+13,'pool scale',COL.dim,SM_FONT,'center');
  /* a block standing on the ground scale is drawn on it */
  const out=M.blocks.find(b=>b.mode==='out');
  /* with a block on it the name goes UNDER the scale, where the block is not */
  lab(ctx,W,H,map.X(GROUND_SCALE_X),out?map.Y(0)+13:map.Y(SCALE_H)-12,'ground scale',COL.dim,SM_FONT,'center');
  if(out){
    worldPoly(ctx,map,[[out.x-out.s/2,SCALE_H],[out.x+out.s/2,SCALE_H],
                       [out.x+out.s/2,SCALE_H+out.s],[out.x-out.s/2,SCALE_H+out.s]],out.col,'#0b0f18',1.4);
    labFixed(ctx,map.X(out.x),map.Y(SCALE_H+out.s/2),out.tag,'#0b0f18','bold 13px -apple-system, sans-serif','center','middle');
  }
  if(st.forces){
    const FS=forceScale(inPool.length?inPool:M.blocks);
    for(const b of inPool) drawForces(ctx,W,H,map,b,FS,{labels:st.labels});
    lab(ctx,W,H,map.X(POOL_W/2)-6,map.Y(0.045),'arrows to one scale: the longest is '+fmt(FS.Fref,1)+' N',
        COL.dim,SM_FONT,'right');
  }
  lab(ctx,W,H,map.X(-POOL_W/2)+7,map.Y(-POOL_H+0.022),
      fmt((M.yw+POOL_H)*A_POOL*LITERS-SCALE_V*LITERS*(M.yw>M.scaleTop?1:0),1)+' L of '+MAT[st.fluid].name,
      fluidColor(st.fluid),LAB_FONT,'left');
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
const SETS_CAP_FULL='PhET&rsquo;s Compare screen: a brick and a piece of wood, held equal in one quantity at a time. '
  +'Equal MASS (PhET&rsquo;s 4 kg) means 2 L of brick against 10 L of wood &mdash; the same weight, and one of them floats. '
  +'Equal VOLUME (5 L) means 10 kg against 2 kg. Equal DENSITY means the same stuff in two sizes, and then they float to '
  +'exactly the same fraction of themselves, because the size cancels out of the floating law completely. The panel beside '
  +'the pool is the mass-volume plane, where a matched pair is a straight line: horizontal, vertical, or through the origin.';
const SETS_CAP_SHORT='PhET&rsquo;s Compare screen: a brick and a piece of wood matched in mass, volume or density.';

function setsGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,SETS_CAP_FULL,SETS_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.62,1);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent(),0.01)};
}
function drawSetsView(ctx,W,H,M,st){
  st=st||ST;
  const G2=setsGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  if(SP.rows[0]){
    const b1=SP.rows[0], xmax=VMAX_L*1.1, ymax=Math.max(12,Math.max.apply(null,M.blocks.map(b=>b.m))*1.3);
    axesReg(ctx,b1,0,xmax,0,ymax,{title:titleFor(b1,'the two blocks in the mass-volume plane','mass and volume'),
      xlab:'volume, litres',ylab:'mass, kg',nx:6,ny:5,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
    polyline(ctx,b1,[0,xmax],[0,xmax*M.rhoF/LITERS],0,xmax,0,ymax,COL.ref,1.4,[5,4]);
    lab(ctx,W,H,b1.x1-8,b1.y1-b1.h*Math.min(ymax,xmax*M.rhoF/LITERS)/ymax-10,MAT[st.fluid].name,COL.ref,SM_FONT,'right');
    if(st.setMode==='mass') polyline(ctx,b1,[0,xmax],[st.sameMass,st.sameMass],0,xmax,0,ymax,COL.pos,1.6);
    else if(st.setMode==='volume') polyline(ctx,b1,[st.sameVolL,st.sameVolL],[0,ymax],0,xmax,0,ymax,COL.pos,1.6);
    else polyline(ctx,b1,[0,xmax],[0,xmax*st.sameRho/LITERS],0,xmax,0,ymax,COL.pos,1.6);
    M.blocks.forEach((bk,i)=>{
      marker(ctx,b1,0,xmax,0,ymax,bk.V*LITERS,bk.m,bk.col);
      lab(ctx,W,H,b1.x+b1.w*(bk.V*LITERS)/xmax+8,b1.y1-b1.h*bk.m/ymax-2,bk.tag+' '+M.names[i],bk.col,SM_FONT,'left');
    });
  }
  const map=drawPoolStage(ctx,W,H,SP.pool,M.yw,M.blocks,{fluid:st.fluid});
  drawScale(ctx,W,H,map,SCALE_X,M.scaleY0,'0.0 N',COL.dim,true);
  M.blocks.forEach((bk,i)=>{
    lab(ctx,W,H,map.X(bk.x),map.Y(bk.yb+bk.s)-11,fmt(bk.pct,0)+' % under',bk.mode==='float'?COL.pos:COL.ref,SM_FONT,'center');
  });
  if(st.forces){
    const FS=forceScale(M.blocks);
    for(const b of M.blocks) drawForces(ctx,W,H,map,b,FS,{labels:st.labels});
  }
  lab(ctx,W,H,map.X(-POOL_W/2)+7,map.Y(-POOL_H+0.022),MAT[st.fluid].name,fluidColor(st.fluid),LAB_FONT,'left');
  drawCaption(ctx,L);
}
