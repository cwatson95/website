/* ================================================================== *
 *  view: the mystery  (PhET's Mystery screen)                         *
 * ================================================================== */
const MYS_CAP_FULL='PhET&rsquo;s Mystery screen. Five unlabelled blocks, a scale in kilograms and a pool with litre '
  +'marks: weigh one, measure the water it pushes aside, divide, and read the name off the table. The catch is real '
  +'physics and the switch below makes it &mdash; a FLOATING block pushes aside its own WEIGHT of water, not its own '
  +'volume, so left alone every floating block measures as water and the answer is wrong. Push it under and the '
  +'displaced volume is the block&rsquo;s volume. The axis below is density on a log scale: orange are the table’s '
  +'thirteen materials, magenta the five readings.';
const MYS_CAP_SHORT='PhET&rsquo;s Mystery screen: weigh, displace, divide, read the table. A floating block must be '
  +'pushed under first, or it measures as water.';

function mysGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,MYS_CAP_FULL,MYS_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.62,1);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent('wide'),0.01)};
}
/* a scale standing ON the ground at x, its platform from ybase up: PhET's
   0.15 x 0.06 m box with the reading on its face */
function drawScale(ctx,W,H,map,x,ybase,text,col){
  const w=SCALE_W, hgt=SCALE_H;
  worldPoly(ctx,map,[[x-w/2,ybase],[x+w/2,ybase],[x+w/2,ybase+hgt],[x-w/2,ybase+hgt]],'#232936','#3d4658',1.4);
  labFixed(ctx,map.X(x),map.Y(ybase+hgt/2),text,col||COL.pos,'bold 12px -apple-system, sans-serif','center','middle');
  return ybase+hgt;
}
function drawMysView(ctx,W,H,M,st){
  st=st||ST;
  const G2=mysGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  /* the density table as a VERTICAL log axis: the table's thirteen materials
     name the left of it, the five readings point at the right */
  const b1=SP.rows[0];
  if(b1){
    const lo=300, hi=23000, ly=v=>Math.log10(v);
    axesReg(ctx,b1,0,1,ly(lo),ly(hi),{title:titleFor(b1,'the table, and the five readings','the table'),
      ylab:'density, kg/m3 (log)',nx:1,ny:1,xticks:[],
      yticks:[ly(400),ly(1000),ly(3000),ly(8000),ly(20000)],yfmt:t=>fmt(Math.pow(10,t),0)});
    const Yof=v=>b1.y1-b1.h*(ly(clamp(v,lo,hi))-ly(lo))/(ly(hi)-ly(lo));
    for(const e of M.table){
      const Y=Yof(e.rho);
      ctx.strokeStyle=COL.ref; ctx.lineWidth=1.2;
      ctx.beginPath(); ctx.moveTo(b1.x,Y); ctx.lineTo(b1.x+b1.w*0.30,Y); ctx.stroke();
      lab(ctx,W,H,b1.x+b1.w*0.32,Y,e.name,COL.ref,SM_FONT,'left');
    }
    for(const r of M.rows){
      const Y=Yof(r.rhoRead);
      ctx.strokeStyle=r.ok?COL.live:COL.ref; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.moveTo(b1.x1,Y); ctx.lineTo(b1.x1-b1.w*0.22,Y); ctx.stroke();
      lab(ctx,W,H,b1.x1-b1.w*0.24,Y,r.tag,COL.live,LAB_FONT,'right');
    }
    lab(ctx,W,H,b1.x+b1.w/2,b1.y1+34,st.submerge?'every reading lands on a table entry':'the floaters have piled onto water',
        st.submerge?COL.pos:COL.ref,SM_FONT,'center');
  }
  const map=drawPoolStage(ctx,W,H,SP.pool,M.yw,M.blocks,{bare:M.bare,kind:'wide'});
  M.rows.forEach((r,i)=>{
    const bk=M.blocks[i];
    lab(ctx,W,H,map.X(bk.x),map.Y(bk.yb+bk.s)-11,fmt(r.VmeasL,2)+' L',r.ok?COL.pos:COL.ref,SM_FONT,'center');
  });
  /* the scale, standing on the ground to the left of the pool, with the picked
     block on its pan being weighed in air */
  const sx=-POOL_W/2-0.105;
  const top=drawScale(ctx,W,H,map,sx,0,fmt(M.pick.mDisp,2)+' kg');
  const ps=cubeSide(M.pick.V);
  worldPoly(ctx,map,[[sx-ps/2,top],[sx+ps/2,top],[sx+ps/2,top+ps],[sx-ps/2,top+ps]],M.pick.col,'#0b0f18',1.4);
  labFixed(ctx,map.X(sx),map.Y(top+ps/2),M.pick.tag,'#0b0f18','bold 13px -apple-system, sans-serif','center','middle');
  lab(ctx,W,H,map.X(sx),map.Y(top+ps)-12,'weighed in air',COL.dim,SM_FONT,'center');
  lab(ctx,W,H,map.X(POOL_W/2)-6,map.Y(POOL_YTOP_WIDE-0.025),
      st.submerge?'all five held under — the rise IS the volume':'left to themselves — a floater measures as water',
      st.submerge?COL.struct:COL.ref,LAB_FONT,'right');

  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: mass and volume                                              *
 * ================================================================== */
const MV_CAP_FULL='ρ = m/V is a ray through the origin, one per material, and the steeper it is the denser the '
  +'material. The cyan box is what PhET’s controls can reach: 1 to 10 litres and 0.1 to 27 kilograms, which is why '
  +'the Intro screen offers styrofoam through aluminium and not gold. Green is the density PhET runs on; orange, where '
  +'it exists, is the handbook value from Wikipedia&rsquo;s table. The bars below are the gap between them, and six '
  +'materials have no handbook row at all, which is said rather than filled in.';
const MV_CAP_SHORT='ρ = m/V, one ray per material; the cyan box is what PhET’s sliders reach. Green is '
  +'PhET&rsquo;s value, orange the handbook&rsquo;s.';

function drawMvView(ctx,W,H,M,st){
  st=st||ST;
  const L=layout(ctx,W,H,MV_CAP_FULL,MV_CAP_SHORT,2,0.36,1);
  const b=L.main, xmax=11, ymax=29;
  axesReg(ctx,b,0,xmax,0,ymax,{title:titleFor(b,'the mass-volume plane: one ray per material','mass and volume'),
    xlab:'volume, litres',ylab:'mass, kg',nx:6,ny:6,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  /* PhET's reachable box */
  const bx0=b.x+b.w*VMIN_L/xmax, bx1=b.x+b.w*VMAX_L/xmax;
  const by0=b.y1-b.h*MMAX/ymax, by1=b.y1-b.h*MMIN/ymax;
  ctx.strokeStyle=rgba(COL.struct,0.55); ctx.lineWidth=1.2; ctx.setLineDash([5,4]);
  ctx.strokeRect(bx0,by0,bx1-bx0,by1-by0); ctx.setLineDash([]);
  lab(ctx,W,H,bx1-6,by0+11,'PhET’s sliders',COL.struct,SM_FONT,'right');
  /* PhET's own Intro materials get a ray each; only the PICKED material gets
     its handbook ray beside it, because an unlabelled second family of dashed
     lines is a picture nobody can read */
  for(const p of M.pts){
    const isIntro=SIMPLE_MATS.indexOf(p.id)>=0, isPick=(p.id===st.mvMat);
    if(!isIntro&&!isPick) continue;
    const col=isPick?COL.live:COL.pos;
    polyline(ctx,b,[0,xmax],[0,xmax*p.rho/LITERS],0,xmax,0,ymax,col,isPick?2:1.5);
    const vEdge=Math.min(xmax,ymax*LITERS/p.rho), mEdge=vEdge*p.rho/LITERS;
    lab(ctx,W,H,b.x+b.w*vEdge/xmax-6,b.y1-b.h*mEdge/ymax-(vEdge<xmax?10:0),p.name,col,SM_FONT,'right');
    if(isPick&&st.showRef&&p.ref!==null&&Math.abs(p.ref-p.rho)>1e-9){
      polyline(ctx,b,[0,xmax],[0,xmax*p.ref/LITERS],0,xmax,0,ymax,COL.ref,1.6,[5,4]);
      const ve=Math.min(xmax,ymax*LITERS/p.ref), me=ve*p.ref/LITERS;
      lab(ctx,W,H,b.x+b.w*ve/xmax-6,b.y1-b.h*me/ymax-(ve<xmax?10:0),p.name+', handbook',COL.ref,SM_FONT,'right');
    }
  }
  if(st.showRef&&M.pick.ref===null)
    lab(ctx,W,H,b.x+10,b.y1-12,plain(M.pick.name)+' has no handbook row to draw',COL.ref,SM_FONT,'left');
  const Lv=M.live;
  marker(ctx,b,0,xmax,0,ymax,Lv.V,Lv.m,COL.live);
  lab(ctx,W,H,b.x+b.w*Lv.V/xmax+9,b.y1-b.h*Lv.m/ymax+1,'block A',COL.live,SM_FONT,'left');

  /* bottom left: PhET against the handbook */
  const b1=L.bottom[0];
  if(b1){
    const withRef=M.pts.filter(p=>p.ref!==null).slice().sort((a,b2)=>a.dRel-b2.dRel);
    const span=Math.max(0.15,Math.max.apply(null,withRef.map(p=>Math.abs(p.dRel)))*1.18);
    axesReg(ctx,b1,-100*span,100*span,0,withRef.length,{title:titleFor(b1,'PhET&rsquo;s value against the handbook&rsquo;s','PhET vs handbook'),
      xlab:'difference, per cent',nx:5,ny:1,yticks:[],xfmt:t=>fmt(t,0)});
    const zx=b1.x+b1.w*0.5;
    ctx.strokeStyle=rgba(COL.ref,0.8); ctx.lineWidth=1.2;
    ctx.beginPath(); ctx.moveTo(zx,b1.y); ctx.lineTo(zx,b1.y1); ctx.stroke();
    withRef.forEach((p,i)=>{
      const Y=b1.y1-b1.h*(i+0.5)/withRef.length, hh=Math.max(3,b1.h/withRef.length*0.6);
      const X=b1.x+b1.w*(100*p.dRel+100*span)/(200*span);
      ctx.fillStyle=rgba(Math.abs(p.dRel)>0.08?COL.ref:COL.pos,0.6);
      ctx.fillRect(Math.min(zx,X),Y-hh/2,Math.abs(X-zx),hh);
      if(Math.abs(p.dRel)>0.08) lab(ctx,W,H,X+(p.dRel>0?5:-5),Y,p.name,COL.ref,SM_FONT,p.dRel>0?'left':'right');
    });
    lab(ctx,W,H,b1.x+6,b1.y+11,'the other '+(M.pts.length-withRef.length)+' have no handbook row',COL.dim,SM_FONT,'left');
  }
  /* bottom right: every material on a log density axis */
  const b2=L.bottom[1];
  if(b2){
    const lo=100, hi=25000, lx=v=>Math.log10(v);
    axesReg(ctx,b2,lx(lo),lx(hi),0,1,{title:titleFor(b2,'every material PhET carries, by density','by density'),
      xlab:'density, kg/m3 (log)',nx:1,ny:1,yticks:[],
      xticks:[lx(150),lx(1000),lx(3000),lx(10000),lx(21450)],xfmt:t=>fmt(Math.pow(10,t),0)});
    const sorted=M.pts.slice().sort((a,b3)=>a.rho-b3.rho);
    sorted.forEach((p,i)=>{
      const X=b2.x+b2.w*(lx(clamp(p.rho,lo,hi))-lx(lo))/(lx(hi)-lx(lo));
      const isPick=(p.id===st.mvMat);
      ctx.strokeStyle=isPick?COL.live:rgba(COL.pos,0.8); ctx.lineWidth=isPick?2:1.1;
      ctx.beginPath(); ctx.moveTo(X,b2.y1); ctx.lineTo(X,b2.y1-b2.h*(0.35+0.45*(i%3)/2)); ctx.stroke();
      if(isPick||i%3===2) lab(ctx,W,H,X,b2.y1-b2.h*(0.38+0.45*(i%3)/2),p.name,isPick?COL.live:COL.pos,SM_FONT,'center','bottom');
    });
  }
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: the waterline                                                *
 * ================================================================== */
const LINE_CAP_FULL='A floating body displaces its own weight, so it settles at V_sub/V = ρ_b/ρ_f exactly &mdash; '
  +'the straight line on the left &mdash; and once the ratio reaches 1 there is nothing left to submerge and the line '
  +'stops dead. Past that kink the body sits on the floor and the floor takes the difference, N = (ρ_b − ρ_f)gV. '
  +'The fraction does not depend on the size, and for a cube the DRAFT is the same fraction of the side, which is '
  +'drawn to scale on the right. Three cases are marked: a block denser than the fluid, one exactly at neutral '
  +'buoyancy, and (in mercury) metals that float.';
const LINE_CAP_SHORT='V_sub/V = min(1, ρ_b/ρ_f), exactly: the floating law, with the kink where the body stops '
  +'floating and starts resting.';

/* The geometry of the draft panel, OUT of the draw call so it can be asserted.
   The block is drawn to scale VERTICALLY (that is what a draft is) and the
   fluid fills the panel, so the world is a height range rather than an
   equal-aspect box.  The tank must be DEEPER than the block: at -0.95 s a
   resting block sat on the floor with its top ABOVE the surface, so the panel
   showed it half out under a readout saying 100 % under, and the dimension
   line measured that false draft.  1.28 s clears a whole block plus its stand. */
function draftGeom(M,hpx){
  /* and TALLER than a block that barely dips in: styrofoam in gasoline floats
     with 78 % of its side above the surface, so 0.55 s of sky cut its top off */
  const s=M.side, ytop0=1.10*s, ybot0=-1.28*s;
  const sc=hpx/(ytop0-ybot0);
  const yb=M.blk.mode==='float'?-M.draft:ybot0+6/sc;
  const ytop=yb+s, ysub=Math.min(ytop,0);
  return {s:s,ytop0:ytop0,ybot0:ybot0,sc:sc,yb:yb,ytop:ytop,ysub:ysub,
          drawnDraft:ysub-yb, drawnFrac:(ysub-yb)/s};
}
function drawLineView(ctx,W,H,M,st){
  st=st||ST;
  const L=layout(ctx,W,H,LINE_CAP_FULL,LINE_CAP_SHORT,1,0.44,1);
  const b=L.main, xmax=3;
  axesReg(ctx,b,0,xmax,0,1.08,{title:titleFor(b,'the submerged fraction against the density ratio','the floating law'),
    xlab:'density ratio rho_b / rho_f',ylab:'submerged fraction',nx:6,ny:5,
    xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,2)});
  polyline(ctx,b,M.curve.map(p=>p[0]),M.curve.map(p=>p[1]),0,xmax,0,1.08,COL.pos,2);
  /* the kink, and the two regimes */
  const kx=b.x+b.w/xmax, ky=b.y1-b.h/1.08;
  ctx.strokeStyle=rgba(COL.struct,0.6); ctx.lineWidth=1; ctx.setLineDash([4,3]);
  ctx.beginPath(); ctx.moveTo(kx,b.y1); ctx.lineTo(kx,ky); ctx.stroke(); ctx.setLineDash([]);
  lab(ctx,W,H,kx-10,b.y1-b.h*0.30,'floats',COL.pos,LAB_FONT,'right');
  lab(ctx,W,H,kx+10,b.y1-b.h*0.22,'rests on the floor',COL.ref,LAB_FONT,'left');
  lab(ctx,W,H,kx,ky-12,'neutral: rho_b = rho_f',COL.live,SM_FONT,'center','bottom');
  /* Every material is a dot; the LABELS are thinned, because in mercury the
     whole table crowds into the first fifth of the axis and a stack of
     twenty-five overlapping names is not a picture.  The caption says so. */
  const sorted=M.rows.filter(r=>r.r<=xmax).slice().sort((a,c)=>a.r-c.r);
  let lastX=-1e9, nDrawn=0;
  for(const r of sorted){
    const X=b.x+b.w*r.r/xmax, Y=b.y1-b.h*r.frac/1.08;
    dot(ctx,X,Y,3,r.floats?COL.pos:COL.ref,'#0b0f18',1);
    if(X-lastX>=Math.max(34,b.w*0.045)||r.id===st.matA){
      if(lab(ctx,W,H,X,Y-9,r.name,r.floats?COL.pos:COL.ref,SM_FONT,'center','bottom')){ lastX=X; nDrawn++; }
    }
  }
  lab(ctx,W,H,b.x1-8,b.y1-12,nDrawn+' of '+sorted.length+' named; every one is a dot',COL.dim,SM_FONT,'right');
  marker(ctx,b,0,xmax,0,1.08,Math.min(M.r,xmax),M.frac,COL.live);
  lab(ctx,W,H,b.x+b.w*Math.min(M.r,xmax)/xmax+10,b.y1-b.h*M.frac/1.08,
      'block A in '+MAT[st.lineFluid].name,COL.live,LAB_FONT,'left');

  /* the block at its exact draft, to scale */
  const b1=L.bottom[0];
  if(b1){
    const D=draftGeom(M,b1.h);
    const s=M.side, ytop0=D.ytop0, ybot0=D.ybot0;
    const sc=D.sc, oy=b1.y+sc*ytop0;
    const mapY=y=>oy-sc*y, mapX=x=>b1.x+b1.w/2+sc*x;
    frame(ctx,b1,'#242a3a');
    lab(ctx,W,H,b1.x,b1.y-9,plain(titleFor(b1,'the same block, drawn at its exact draft','the draft')),'#aeb6c6','italic 13px Georgia, serif','left','bottom');
    ctx.fillStyle=rgba(COL.struct,0.17); ctx.fillRect(b1.x+1,mapY(0),b1.w-2,b1.y1-mapY(0)-1);
    ctx.fillStyle=GROUND; ctx.fillRect(b1.x+1,b1.y1-6,b1.w-2,5);
    const yb=D.yb, ytop=D.ytop, ysub=D.ysub;
    const px=x=>mapX(x), py=y=>mapY(y);
    const rectW=(x0,y0,x1,y1,fill,stroke)=>{
      ctx.beginPath(); ctx.moveTo(px(x0),py(y0)); ctx.lineTo(px(x1),py(y0));
      ctx.lineTo(px(x1),py(y1)); ctx.lineTo(px(x0),py(y1)); ctx.closePath();
      if(fill){ ctx.fillStyle=fill; ctx.fill(); }
      if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1.4; ctx.stroke(); }
    };
    rectW(-s/2,yb,s/2,ytop,matColor(st.matA,M.rhoB),'#0b0f18');
    rectW(-s/2,yb,s/2,ysub,rgba(COL.pos,0.18),null);
    ctx.strokeStyle=rgba(COL.struct,0.85); ctx.lineWidth=1.2;
    ctx.beginPath(); ctx.moveTo(b1.x+1,mapY(0)); ctx.lineTo(b1.x1-1,mapY(0)); ctx.stroke();
    POLY_SEGS.push(b1.x+1,mapY(0),b1.x1-1,mapY(0));
    /* the draft dimension, outside the block so it cannot be read as a crack */
    const dx=s*0.62;
    ctx.strokeStyle=COL.live; ctx.lineWidth=1.4;
    ctx.beginPath(); ctx.moveTo(px(dx),py(yb)); ctx.lineTo(px(dx),py(ysub)); ctx.stroke();
    const dPix=Math.abs(py(yb)-py(ysub));
    lab(ctx,W,H,px(dx)+8,(py(yb)+py(ysub))/2-(dPix<26?15:0),
        fmt(100*(ysub-yb),2)+' cm of '+fmt(100*s,2)+' cm',COL.live,SM_FONT,'left');
    lab(ctx,W,H,px(0),py(ytop)-11,fmt(100*M.frac,1)+' % under',COL.pos,LAB_FONT,'center');
    lab(ctx,W,H,b1.x+8,b1.y+12,M.neutral?'exactly neutral — no depth is preferred'
        :(M.blk.mode==='float'?'floating in '+MAT[st.lineFluid].name:'resting, the floor takes '+fmt(M.N,1)+' N'),
        M.neutral?COL.live:(M.blk.mode==='float'?COL.pos:COL.ref),SM_FONT,'left');
  }
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  dispatch, and the scene object                                     *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(st.view==='pool') drawPoolView(ctx,W,H,M,st);
  else if(st.view==='sets') drawSetsView(ctx,W,H,M,st);
  else if(st.view==='mystery') drawMysView(ctx,W,H,M,st);
  else if(st.view==='mv') drawMvView(ctx,W,H,M,st);
  else drawLineView(ctx,W,H,M,st);
}

function makeScene(canvas){
  const S={st:ST,W:1180,H:740};
  S.model=()=>buildModel(ST);
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel(ST),ST); };
  /* nothing animates: this sim solves the static problem exactly */
  S.step=function(){ return false; };
  /* the pointer: grab a block in the pool view and hold it where you like */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null;
      if(DRAG.what==='A') ST.holdA=null; else if(DRAG.what==='B') ST.holdB=null;
      DRAG.what=null; return had; }
    if(ST.view!=='pool') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(ST), G2=poolGeo(ctx,S.W,S.H,M), map=G2.map;
    if(type==='down'){
      for(let i=M.blocks.length-1;i>=0;i--){
        const bk=M.blocks[i], X0=map.X(bk.x-bk.s/2)-6, X1=map.X(bk.x+bk.s/2)+6;
        const Y0=map.Y(bk.yb+bk.s)-6, Y1=map.Y(bk.yb)+6;
        if(x>=X0&&x<=X1&&y>=Y0&&y<=Y1){ DRAG.what=bk.tag; DRAG.off=bk.yb-map.wy(y); return true; }
      }
      return false;
    }
    if(type==='move'&&(DRAG.what==='A'||DRAG.what==='B')){
      const sB=cubeSide((DRAG.what==='A'?ST.volAL:ST.volBL)/LITERS);
      const yb=clamp(map.wy(y)+DRAG.off,-POOL_H,holdCeiling(sB));
      if(DRAG.what==='A') ST.holdA=yb; else ST.holdB=yb;
      return true;
    }
    return false;
  };
  return S;
}
