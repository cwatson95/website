/* ================================================================== *
 *  view: the faces — where the upthrust comes from                    *
 * ================================================================== */
const FACES_CAP_FULL='Nothing pushes up on a submerged block except the fluid, and all the fluid does is press on every '
  +'face at p = ρ_f g d, d the depth. The cyan arrows are that pressure, drawn to scale. The four side faces cancel in '
  +'pairs exactly — whatever is pushed in on the left is pushed in on the right. The bottom face is lower than the top '
  +'by the block’s own height, so it is pressed harder by ρ_f g h, and times the face area that is ρ_f g V. That is '
  +'Archimedes, derived rather than asserted, and the readout prints how far the two routes differ. The panel beside it is '
  +'p against depth: a straight line, which is why the edge integral is exact.';
const FACES_CAP_SHORT='The hydrostatic pressure on the six faces: the sides cancel, and bottom minus top IS the upthrust.';

function drawFacesView(ctx,W,H,M,st){
  st=st||ST;
  const L=layout(ctx,W,H,FACES_CAP_FULL,FACES_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.55,2);
  /* the right column first, so its axes are registered before any stage label */
  if(SP.rows.length>1){
    /* the depth axis fits the depth the block is AT (Known-bad: fit each axis
       to the structure that axis contains) rather than a fixed 60 cm */
    const b1=SP.rows[0], dmax=Math.max(0.12,M.F.dBot*1.28);
    const pmax=M.rhoF*G*dmax;
    axesReg(ctx,b1,0,pmax/1000,-dmax*100,0,{title:titleFor(b1,'pressure against depth: a straight line','p against depth'),
      xlab:'pressure, kPa',ylab:'height below the surface, cm',nx:4,ny:5,
      xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,0)});
    polyline(ctx,b1,[0,pmax/1000],[0,-dmax*100],0,pmax/1000,-dmax*100,0,COL.struct,1.8);
    marker(ctx,b1,0,pmax/1000,-dmax*100,0,M.F.pBot/1000,-M.F.dBot*100,COL.pos);
    marker(ctx,b1,0,pmax/1000,-dmax*100,0,M.F.pTop/1000,-M.F.dTop*100,COL.ref);
    lab(ctx,W,H,b1.x+b1.w*(M.F.pBot/1000)/(pmax/1000)+8,b1.y1-b1.h*(dmax*100-M.F.dBot*100)/(dmax*100),
        'bottom '+sigf(M.F.pBot/1000,4)+' kPa',COL.pos,SM_FONT,'left');
    lab(ctx,W,H,b1.x+b1.w*(M.F.pTop/1000)/(pmax/1000)+8,b1.y1-b1.h*(dmax*100-M.F.dTop*100)/(dmax*100),
        'top '+sigf(M.F.pTop/1000,4)+' kPa',COL.ref,SM_FONT,'left');
    /* the two routes to the same force */
    const b2=SP.rows[1], gh=Math.max(M.F.Fbot,M.arch)*1.2;
    axesReg(ctx,b2,0,4,0,gh,{title:titleFor(b2,'the same force, two ways','two ways'),
      ylab:'newtons',nx:1,ny:5,xticks:[],yfmt:t=>fmt(t,0)});
    const bars=[[0.5,M.F.Fbot,COL.struct,'bottom'],[1.4,M.F.Ftop,COL.ref,'top'],
                [2.3,M.F.net,COL.pos,'net'],[3.2,M.arch,COL.live,'rho g V']];
    for(const bar of bars){
      const X=b2.x+b2.w*bar[0]/4, Wd=b2.w*0.6/4, Yv=b2.y1-b2.h*clamp(bar[1],0,gh)/gh;
      ctx.fillStyle=rgba(bar[2],0.55); ctx.fillRect(X,Yv,Wd,b2.y1-Yv);
      ctx.strokeStyle=bar[2]; ctx.lineWidth=1.2; ctx.strokeRect(X,Yv,Wd,b2.y1-Yv);
      lab(ctx,W,H,X+Wd/2,Yv-8,bar[3],bar[2],SM_FONT,'center');
    }
    lab(ctx,W,H,b2.x+b2.w/2,b2.y1+30,'net and rho g V differ by '+pct(M.resid),COL.pos,SM_FONT,'center');
  }
  /* the block, with the pressure on every face */
  const b=SP.pool, s=M.s;
  const ext={xmin:-1.5*s,xmax:1.5*s,ymin:M.yb-0.35*s,ymax:0.42*s};
  const map=worldFitUp(b,ext,0.01);
  frame(ctx,b,'#242a3a');
  lab(ctx,W,H,b.x,b.y-9,plain(titleFor(b,'the pressure on every face','the faces')),'#aeb6c6','italic 13px Georgia, serif','left','bottom');
  /* the fluid, filling the panel down from the free surface */
  ctx.fillStyle=rgba(fluidColor(st.fluid),0.20);
  ctx.fillRect(b.x+1,map.Y(0),b.w-2,b.y1-map.Y(0)-1);
  ctx.strokeStyle=rgba(fluidColor(st.fluid),0.9); ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(b.x+1,map.Y(0)); ctx.lineTo(b.x1-1,map.Y(0)); ctx.stroke();
  POLY_SEGS.push(b.x+1,map.Y(0),b.x1-1,map.Y(0));
  lab(ctx,W,H,b.x+8,map.Y(0)-11,'the free surface',fluidColor(st.fluid),SM_FONT,'left');
  const yt=M.yb+s;
  worldPoly(ctx,map,[[-s/2,M.yb],[s/2,M.yb],[s/2,yt],[-s/2,yt]],matColor(st.matA,M.rho),'#0b0f18',1.4);
  const ysub=Math.min(yt,0);
  worldPoly(ctx,map,[[-s/2,M.yb],[s/2,M.yb],[s/2,ysub],[-s/2,ysub]],rgba(COL.pos,0.16),null);
  /* pressure arrows: length proportional to p, one scale for the picture */
  const pRef=Math.max(M.F.pBot,1), aLen=0.30*s;
  const nS=7;
  for(let k=0;k<nS;k++){
    const t=(k+0.5)/nS, x=-s/2+s*t;
    if(M.yb<0) arrowW(ctx,map,[x,M.yb-aLen*M.F.pBot/pRef],[0,aLen*M.F.pBot/pRef],COL.struct,1.6);
    if(yt<0) arrowW(ctx,map,[x,yt+aLen*M.F.pTop/pRef],[0,-aLen*M.F.pTop/pRef],COL.struct,1.6);
  }
  for(let k=0;k<nS;k++){
    const t=(k+0.5)/nS, y=M.yb+Math.min(s,Math.max(0,ysub-M.yb))*t;
    if(y>=0) continue;
    const p=M.rhoF*G*(0-y), Lp=aLen*p/pRef;
    arrowW(ctx,map,[-s/2-Lp,y],[Lp,0],COL.struct,1.4);
    arrowW(ctx,map,[s/2+Lp,y],[-Lp,0],COL.struct,1.4);
  }
  /* every one of these sits OUTSIDE the block: the arrows are drawn from the
     faces outward, so the space beyond the arrow tips is the only clear room */
  const aPix=map.s*aLen;
  lab(ctx,W,H,map.X(0),map.Y(M.yb-aLen*M.F.pBot/pRef)+13,
      'the bottom is pressed hardest',COL.struct,SM_FONT,'center','top');
  lab(ctx,W,H,map.X(-s/2)-aPix-12,map.Y(M.yb+s*0.5),'the sides cancel',COL.struct,SM_FONT,'right');
  lab(ctx,W,H,map.X(0),map.Y(yt+(yt<0?aLen*M.F.pTop/pRef:0))-13,
      M.fullyUnder?'fully submerged':'the top is out of the fluid',
      M.fullyUnder?COL.pos:COL.ref,SM_FONT,'center','bottom');
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: the scale — the apparent weight, all the way down            *
 * ================================================================== */
const SCALE_CAP_FULL='A block hangs from a spring scale and is lowered into the pool. While it is entering, the submerged '
  +'volume grows and the reading falls in a straight line. The moment the top face goes under, V_sub stops growing and the '
  +'reading stops changing — flat for the rest of the descent, however deep, because the extra pressure on the bottom '
  +'face is matched exactly by the extra pressure on the top. The slight tilt of the entering leg is real: the fluid rises '
  +'as the block goes in, so the block meets the surface a little sooner than it would in a bottomless sea. If the block '
  +'floats the reading reaches zero and the string goes slack, which is marked.';
const SCALE_CAP_SHORT='Lowering a block on a spring scale: a straight fall while it enters, then flat once it is under.';

function scaleGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,SCALE_CAP_FULL,SCALE_CAP_SHORT,0,0,0);
  const SP=splitMain(L,W,0.52,1);
  return {L:L,SP:SP,map:worldFitUp(SP.pool,poolExtent(),0.01)};
}
function drawScaleView(ctx,W,H,M,st){
  st=st||ST;
  const G2=scaleGeo(ctx,W,H,M), L=G2.L, SP=G2.SP;
  if(SP.rows[0]){
    const b1=SP.rows[0], ymax=Math.max(1,M.W*1.15);
    axesReg(ctx,b1,0,1,0,ymax,{title:titleFor(b1,'what the spring scale reads, all the way down','the reading'),
      xlab:'how far it has been lowered',ylab:'newtons',nx:5,ny:5,
      xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,0)});
    polyline(ctx,b1,M.curve.map(c=>c[0]),M.curve.map(c=>Math.max(0,c[1])),0,1,0,ymax,COL.pos,2);
    /* the weight in air, as the reference the curve starts from */
    polyline(ctx,b1,[0,1],[M.W,M.W],0,1,0,ymax,COL.ref,1.3,[5,4]);
    lab(ctx,W,H,b1.x+8,b1.y1-b1.h*M.W/ymax-10,'its weight in air, '+fmt(M.W,1)+' N',COL.ref,SM_FONT,'left');
    if(M.full>0){
      polyline(ctx,b1,[0,1],[M.full,M.full],0,1,0,ymax,COL.struct,1.3,[4,3]);
      lab(ctx,W,H,b1.x1-8,b1.y1-b1.h*M.full/ymax-10,'fully under: '+fmt(M.full,1)+' N',COL.struct,SM_FONT,'right');
    } else {
      lab(ctx,W,H,b1.x1-8,b1.y+12,'it floats: the string goes slack',COL.live,SM_FONT,'right');
    }
    marker(ctx,b1,0,1,0,ymax,clamp(st.lowered,0,1),Math.max(0,M.read),COL.live);
  }
  /* the tank, the hanging block and the scale */
  const b=SP.pool;
  const map=drawPoolStage(ctx,W,H,b,M.yw,[{x:0,yb:M.yb,s:M.s,Vsub:M.Vsub,col:matColor(st.matA,M.rho),tag:'A'}],
                          {fluid:st.fluid});
  /* the string and a spring scale above the pool */
  const topY=POOL_YTOP-0.03;
  ctx.strokeStyle=COL.dim; ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(map.X(0),map.Y(topY)); ctx.lineTo(map.X(0),map.Y(M.yb+M.s)); ctx.stroke();
  POLY_SEGS.push(map.X(0),map.Y(topY),map.X(0),map.Y(M.yb+M.s));
  worldPoly(ctx,map,[[-0.10,topY],[0.10,topY],[0.10,topY+0.055],[-0.10,topY+0.055]],'#232936','#3d4658',1.4);
  labFixed(ctx,map.X(0),map.Y(topY+0.0275),fmt(M.read,2)+' N',M.slack?COL.live:COL.pos,
           'bold 12px -apple-system, sans-serif','center','middle');
  lab(ctx,W,H,map.X(0.11),map.Y(topY+0.0275),M.slack?'slack — it floats':'spring scale',
      M.slack?COL.live:COL.dim,SM_FONT,'left');
  lab(ctx,W,H,map.X(-POOL_W/2)+7,map.Y(-POOL_H+0.022),MAT[st.fluid].name,fluidColor(st.fluid),LAB_FONT,'left');
  lab(ctx,W,H,map.X(POOL_W/2)-7,map.Y(M.yw)+12,fmt(100*M.frac,1)+' % under',COL.pos,SM_FONT,'right');
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: float or sink — every material against every fluid           *
 * ================================================================== */
const FLU_CAP_FULL='Floating is a comparison, not a property of a material. Every material PhET carries is a row, ordered '
  +'by density; every fluid it carries is a column. A green cell floats and the number is the fraction of it that is under, '
  +'which is exactly ρ_b/ρ_f; an orange cell sinks. Lead floats in mercury, and so does everything on the list except '
  +'gold, tantalum and platinum; in gasoline only styrofoam and wood do. The step from green to orange in each column is the neutral '
  +'line ρ_b = ρ_f, and there is nothing gradual about it — the fraction reaches 1 and stops.';
const FLU_CAP_SHORT='Every material against every fluid: green floats, orange sinks, and the number is ρ_b/ρ_f.';

function drawFluidsView(ctx,W,H,M,st){
  st=st||ST;
  const L=layout(ctx,W,H,FLU_CAP_FULL,FLU_CAP_SHORT,0,0,0);
  const b=L.main;
  const nR=M.rows.length, nC=M.cols.length;
  const leftPad=Math.min(120,b.w*0.16), topPad=26;
  const gx=b.x+leftPad, gy=b.y+topPad, gw=b.w-leftPad-8, gh=b.h-topPad-8;
  const cw=gw/nC, ch=gh/nR;
  lab(ctx,W,H,b.x,b.y-9,plain(titleFor(b,'every material against every fluid PhET carries','float or sink')),
      '#aeb6c6','italic 13px Georgia, serif','left','bottom');
  M.cols.forEach((f,j)=>{
    labFixed(ctx,gx+cw*(j+0.5),gy-9,f.name,COL.struct,SM_FONT,'center','bottom');
  });
  /* the row names are thinned by MEASURED spacing, the picked one first, so
     that at 27 rows in 250 px they never stack on one another */
  const pickY=(M.pi>=0)?gy+ch*M.pi+ch/2:-1e9;
  if(M.pi>=0) labFixed(ctx,gx-8,pickY,M.rows[M.pi].name,COL.live,SM_FONT,'right','middle');
  let lastY=-1e9, nNamed=(M.pi>=0)?1:0;
  M.rows.forEach((m,i)=>{
    const Y=gy+ch*i, isPick=(m.id===st.gridMat);
    if(!isPick&&Math.abs(Y+ch/2-lastY)>=12&&Math.abs(Y+ch/2-pickY)>=12){
      labFixed(ctx,gx-8,Y+ch/2,m.name,COL.dim,SM_FONT,'right','middle');
      lastY=Y+ch/2; nNamed++;
    }
    M.cols.forEach((f,j)=>{
      const c=M.grid[i][j], X=gx+cw*j;
      const col=c.neutral?COL.live:(c.floats?COL.pos:COL.ref);
      ctx.fillStyle=rgba(col,c.floats?0.15+0.45*(1-c.frac):0.30);
      ctx.fillRect(X+0.5,Y+0.5,cw-1,ch-1);
      if(isPick){ ctx.strokeStyle=COL.live; ctx.lineWidth=1.4; ctx.strokeRect(X+0.5,Y+0.5,cw-1,ch-1); }
      if(ch>=13&&cw>=44)
        labFixed(ctx,X+cw/2,Y+ch/2,c.floats?(c.frac>0.995?fmt(100*c.frac,1):fmt(100*c.frac,0))+'%':'sinks',
                 c.floats?'#0b0f18':'#1b1108','10px -apple-system, sans-serif','center','middle');
    });
  });
  frame(ctx,box(gx,gy,gw,gh),'#242a3a');
  lab(ctx,W,H,b.x1-4,b.y1+16,M.nFloat+' of '+M.nCells+' combinations float; '+nNamed+' of '+nR+' rows named',
      COL.pos,SM_FONT,'right');
  lab(ctx,W,H,gx,b.y1+16,'rows ordered by density, '+sigf(M.rows[0].phet,3)+' to '+sigf(M.rows[nR-1].phet,5)+' kg/m3',
      COL.dim,SM_FONT,'left');
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  dispatch, and the scene object                                     *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(st.view==='explore') drawExploreView(ctx,W,H,M,st);
  else if(st.view==='sets') drawSetsView(ctx,W,H,M,st);
  else if(st.view==='faces') drawFacesView(ctx,W,H,M,st);
  else if(st.view==='scale') drawScaleView(ctx,W,H,M,st);
  else drawFluidsView(ctx,W,H,M,st);
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
    if(ST.view!=='explore') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(ST), G2=exploreGeo(ctx,S.W,S.H,M), map=G2.map;
    if(type==='down'){
      for(let i=M.blocks.length-1;i>=0;i--){
        const bk=M.blocks[i];
        if(bk.mode==='out') continue;
        const X0=map.X(bk.x-bk.s/2)-6, X1=map.X(bk.x+bk.s/2)+6;
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
