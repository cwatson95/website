
/* ================================================================== *
 *  the pieces every view draws: the pressure field, the air parcels,  *
 *  the speakers, the wall and its image source, the listener, PhET's  *
 *  ruler and stopwatch, and the two graphs                            *
 * ================================================================== */
const NLEV=49, HALF=24;                  /* 49 contrast classes, ambient on the middle one */
function levelOf(v){ const t=v/U_FULL; return Math.round(((t<-1?-1:(t>1?1:t))+1)*HALF); }
let LEVEL_COLS=null;
function levelCols(){
  if(LEVEL_COLS) return LEVEL_COLS;
  const out=[];
  for(let q=0;q<NLEV;q++) out.push(mix(COL.air0,COL.air1,q/(NLEV-1)));
  return LEVEL_COLS=out;
}
/* one fill per contrast class, runs merged along each row, pixel-snapped.  Cells
   the wall hides are not drawn at all — PhET leaves them blank too. */
function drawField(ctx,sq,M){
  const V=LAT.VIS, g=M.g, v=g.v, mk=g.mask, cols=levelCols(), cs=sq.w/V;
  const full=(g.nfront===V*V);
  ctx.fillStyle=full?cols[HALF]:COL.off; ctx.fillRect(sq.x,sq.y,sq.w,sq.h);
  const rects=[]; for(let q=0;q<NLEV;q++) rects.push([]);
  let nCells=0;
  const cls=q=>mk[q]?levelOf(v[q]):-1;
  for(let j=0;j<V;j++){
    const row=j*V, y0=Math.round(sq.y+j*cs), y1=Math.round(sq.y+(j+1)*cs);
    let i=0;
    while(i<V){
      const q=cls(row+i);
      let e=i+1;
      while(e<V&&cls(row+e)===q) e++;
      if(q>=0&&!(full&&q===HALF)){ rects[q].push(Math.round(sq.x+i*cs),y0,Math.round(sq.x+e*cs),y1); nCells+=e-i; }
      i=e;
    }
  }
  for(let q=0;q<NLEV;q++){ const r=rects[q]; if(!r.length) continue;
    ctx.beginPath(); for(let k=0;k<r.length;k+=4) ctx.rect(r[k],r[k+1],r[k+2]-r[k],r[k+3]-r[k+1]);
    ctx.fillStyle=cols[q]; ctx.fill(); }
  return nCells;
}
/* a label over the pressure field needs its own dark backing: the field's ambient is a
   mid grey, and orange or green on it is unreadable */
function labOver(ctx,W,H,x,y,txt,col,align){
  const t=plain(txt), w=t.length*10.5*0.56+10;
  const lx=(align==='right')?x-w+5:((align==='center')?x-w/2:x-5);
  ctx.fillStyle='rgba(7,11,24,.74)'; ctx.fillRect(lx,y-8,w,16);
  return lab(ctx,W,H,x,y,txt,col,SM_FONT,align||'left');
}
function cellPx(sq,i){ return sq.x+(i+0.5)*sq.w/LAT.VIS; }
function mx(sq,x){ return sq.x+sq.w*x/AIR.W; }             /* model metres -> screen */
function my(sq,y){ return sq.y+sq.h*y/AIR.W; }
/* the marked parcel is deliberately NOT the middle one: the listener stands there */
const PARC_MARK=12*(PARC_N+1)+6;
function drawParcels(ctx,sq,M){
  const P=M.parcels, cs=sq.w/LAT.VIS, MARK=PARC_MARK, onField=(ST.look!=='particles');
  ctx.beginPath();
  for(let q=0;q<P.length;q++){
    if(q===MARK||!P[q][2]) continue;
    const x=sq.x+(P[q][0]+0.5)*cs, y=sq.y+(P[q][1]+0.5)*cs;
    if(x<sq.x||x>sq.x1||y<sq.y||y>sq.y1) continue;
    ctx.moveTo(x+2.1,y); ctx.arc(x,y,2.1,0,TAU);
  }
  ctx.fillStyle=onField?'#101520':'#d6dae4'; ctx.fill();
  const c=P[MARK];
  if(c&&c[2]) dot(ctx,sq.x+(c[0]+0.5)*cs,sq.y+(c[1]+0.5)*cs,3.4,COL.struct,onField?'#0b0e16':'#ffffff',1.4);
}
/* PhET's loudspeaker, drawn outside the box on its own row, its cone magenta
   while the source is running */
const SPK_W=46, SPK_H=34, BTN_R=9;
function speakerGeo(sq,M,k){
  const y=my(sq,M.speakers[k][1]), x1=sq.x-10, x0=x1-SPK_W;
  return {x0,x1,y,sx:mx(sq,M.speakers[k][0]),btn:{x:(x0+x1)/2,y:y+SPK_H/2+14,r:BTN_R}};
}
function drawSpeaker(ctx,W,H,sq,M,k){
  const g=speakerGeo(sq,M,k), on=M.active, x0=g.x0, x1=g.x1, y=g.y;
  const poly=pts=>{ ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); });
    ctx.closePath(); ctx.fill(); ctx.stroke(); };
  ctx.fillStyle='#161c2c'; ctx.strokeStyle=COL.struct; ctx.lineWidth=1.3;
  poly([[x0,y-9],[x0+16,y-9],[x0+16,y+9],[x0,y+9]]);                    /* the box */
  poly([[x0+16,y-7],[x1,y-15],[x1,y+15],[x0+16,y+7]]);                  /* the cone */
  /* the cone pushes forward with the drive, so the picture and the field agree */
  const push=clamp(M.R.val/(AIR.ampMax*LAT.AMP_CAL),-1,1)*5;
  ctx.beginPath(); ctx.moveTo(x1+push,y-15); ctx.lineTo(x1+push,y+15);
  ctx.strokeStyle=on?COL.live:'#3a4254'; ctx.lineWidth=2.2; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x1,y); ctx.lineTo(g.sx,y);
  ctx.strokeStyle=on?rgba(COL.live,0.7):'#3a4254'; ctx.lineWidth=1.4; ctx.stroke();
  dot(ctx,g.sx,y,4.5,on?COL.live:'#3a4254','#ffffff',1.2);
  if(k===0){
    dot(ctx,g.btn.x,g.btn.y,g.btn.r,on?COL.live:'#141a28',on?'#ffffff':COL.live,1.6);
    lab(ctx,W,H,g.btn.x,g.btn.y+g.btn.r+9,ST.wave==='pulse'?'fire':(on?'on':'off'),
        on?COL.live:'#8b93a6',SM_FONT,'center');
  }
}
/* the wall: the line itself, the solid it stands for, the image speaker, and the
   ray that goes speaker -> wall -> listener with its two equal angles */
function wallEnds(G){
  /* where the wall line meets the box, in model coordinates */
  const pts=[];
  const add=(x,y)=>{ if(x>=-1e-9&&x<=AIR.W+1e-9&&y>=-1e-9&&y<=AIR.W+1e-9) pts.push([x,y]); };
  if(Math.abs(G.dyh)>1e-12){ add(G.ax+(0-G.ay)*G.dxh/G.dyh,0); add(G.ax+(AIR.W-G.ay)*G.dxh/G.dyh,AIR.W); }
  if(Math.abs(G.dxh)>1e-12){ add(0,G.ay+(0-G.ax)*G.dyh/G.dxh); add(AIR.W,G.ay+(AIR.W-G.ax)*G.dyh/G.dxh); }
  if(pts.length<2) return null;
  let best=[pts[0],pts[1]], bd=-1;
  for(let i=0;i<pts.length;i++) for(let j=i+1;j<pts.length;j++){
    const d=Math.hypot(pts[i][0]-pts[j][0],pts[i][1]-pts[j][1]);
    if(d>bd){ bd=d; best=[pts[i],pts[j]]; }
  }
  return best;
}
function drawWall(ctx,W,H,sq,M){
  const G=M.G, e=wallEnds(G);
  if(!e) return;
  const A=[mx(sq,e[0][0]),my(sq,e[0][1])], B=[mx(sq,e[1][0]),my(sq,e[1][1])];
  ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]);
  ctx.strokeStyle=COL.wall; ctx.lineWidth=4; ctx.lineCap='butt'; ctx.stroke();
  ctx.lineWidth=1;
  /* hatching on the dead side, one short stroke per metre of wall */
  const n=Math.max(2,Math.round(Math.hypot(B[0]-A[0],B[1]-A[1])/13));
  const hx=G.nxh*9, hy=G.nyh*9;
  ctx.beginPath();
  for(let q=0;q<=n;q++){
    const t=q/n, X=A[0]+(B[0]-A[0])*t, Y=A[1]+(B[1]-A[1])*t;
    ctx.moveTo(X,Y); ctx.lineTo(X+hx,Y+hy);
  }
  ctx.strokeStyle=rgba(COL.wall,0.55); ctx.stroke();
}
function drawImageRay(ctx,W,H,sq,M){
  const Wl=M.wall, s=M.speakers[0], L=M.listener;
  if(!Wl) return;
  const im=Wl.image, IX=mx(sq,im[0]), IY=my(sq,im[1]);
  /* the image speaker, outside the box if the wall is far: clamped and labelled */
  const cx=clamp(IX,sq.x+4,sq.x1-4), cy=clamp(IY,sq.y+4,sq.y1-4), out=(cx!==IX||cy!==IY);
  ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(mx(sq,s[0]),my(sq,s[1])); ctx.lineTo(cx,cy);
  ctx.strokeStyle=rgba(COL.ref,0.5); ctx.lineWidth=1.2; ctx.stroke();
  ctx.setLineDash([]);
  dot(ctx,cx,cy,5.5,'#141a28',COL.ref,1.8);
  /* hang the label on whichever side has room INSIDE the box: pushed against the
     right edge it would otherwise run out over the listener's chart */
  const txt=out?'image speaker (off the box)':'image speaker';
  if(cx>sq.x1-150) labOver(ctx,W,H,cx-9,cy-10,txt,COL.ref,'right');
  else labOver(ctx,W,H,cx+9,cy-10,txt,COL.ref,'left');
  if(!Wl.bounce||!ST.listener) return;
  const Q=Wl.bounce, QX=mx(sq,Q[0]), QY=my(sq,Q[1]);
  const SX=mx(sq,s[0]), SY=my(sq,s[1]), LX=mx(sq,L.x), LY=my(sq,L.y);
  ctx.beginPath(); ctx.moveTo(SX,SY); ctx.lineTo(QX,QY); ctx.lineTo(LX,LY);
  ctx.strokeStyle=COL.pos; ctx.lineWidth=1.6; ctx.stroke();
  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(SX,SY); ctx.lineTo(LX,LY);
  ctx.strokeStyle=rgba(COL.struct,0.7); ctx.lineWidth=1.2; ctx.stroke();
  ctx.setLineDash([]);
  /* the normal at the bounce, and the two angles it makes */
  const nx0=M.G.nxh*26, ny0=M.G.nyh*26;
  ctx.beginPath(); ctx.moveTo(QX-nx0,QY-ny0); ctx.lineTo(QX+nx0*0.35,QY+ny0*0.35);
  ctx.strokeStyle=rgba('#ffffff',0.55); ctx.lineWidth=1; ctx.stroke();
  dot(ctx,QX,QY,3.2,COL.pos);
  /* keep the two angles INSIDE the box: with the wall laid flat the bounce sits on the
     floor of it, and a label hung below would land on the graph panel's title */
  const ay=(QY>sq.y1-30)?QY-13:QY+13;
  labOver(ctx,W,H,QX+7,ay,sigf(Wl.aIn/DEG,3)+'° = '+sigf(Wl.aOut/DEG,3)+'°',COL.pos,'left');
}
/* the listener: a head with one ear turned toward the sound */
function drawListener(ctx,W,H,sq,M){
  const L=M.listener, X=mx(sq,L.x), Y=my(sq,L.y);
  const loud=clamp(L.amp/U_FULL,0,1);
  ctx.beginPath(); ctx.arc(X,Y,9,0,TAU);
  ctx.fillStyle=rgba(COL.live,0.16+0.5*loud); ctx.fill();
  ctx.strokeStyle=COL.live; ctx.lineWidth=1.8; ctx.stroke();
  ctx.beginPath(); ctx.arc(X-3,Y,4.5,-1.1,1.1);
  ctx.strokeStyle='#ffffff'; ctx.lineWidth=1.3; ctx.stroke();
  if(!L.inFront) lab(ctx,W,H,X+13,Y,'in the shadow',COL.ref,SM_FONT,'left');
}
/* PhET's ruler: rigid, 5 m long, dragged by its body */
function rulerGeo(sq){
  const x0=mx(sq,TOOLS.ruler[0]), x1=mx(sq,TOOLS.ruler[0]+RULER_LEN), y=my(sq,TOOLS.ruler[1]);
  return {x0,x1,y,h:26};
}
/* the ruler's own rectangle, RESERVED before any overlay label is placed: its tick
   numbers are painted straight (they must stay on their ticks), so a label that lands
   on the ruler has nothing to dodge unless the rectangle is registered first */
function rulerRect(sq){ const g=rulerGeo(sq); return [g.x0,g.y-g.h/2,g.x1,g.y+g.h/2]; }
function drawRuler(ctx,W,H,sq,M){
  const g=rulerGeo(sq);
  ctx.fillStyle='rgba(241,231,176,.93)'; ctx.fillRect(g.x0,g.y-g.h/2,g.x1-g.x0,g.h);
  ctx.strokeStyle='#8b7f4a'; ctx.lineWidth=1; ctx.strokeRect(g.x0,g.y-g.h/2,g.x1-g.x0,g.h);
  ctx.beginPath();
  for(let q=0;q<=RULER_LEN*4;q++){
    const X=g.x0+(g.x1-g.x0)*q/(RULER_LEN*4), big=(q%4===0);
    ctx.moveTo(X,g.y-g.h/2); ctx.lineTo(X,g.y-g.h/2+(big?11:6));
  }
  ctx.strokeStyle='#4a4430'; ctx.lineWidth=1; ctx.stroke();
  ctx.font='9.5px -apple-system, sans-serif'; ctx.fillStyle='#4a4430';
  ctx.textAlign='center'; ctx.textBaseline='top';
  /* PhET puts the unit where the last major tick label would go (unitsMajorTickIndex),
     which keeps the whole instrument inside its own rectangle.  How many wavelengths
     fit on it is in the readout, not painted beside the ruler: a caption hung under
     a draggable object has nowhere safe to go (it collided with the tick numbers). */
  for(let q=0;q<=RULER_LEN;q++)
    ctx.fillText(q<RULER_LEN?String(q):'m',g.x0+(g.x1-g.x0)*q/RULER_LEN,g.y-g.h/2+12);
}
/* the pressure along the speaker's row, in metres */
function drawAxisGraph(ctx,W,H,b,M){
  const V=LAT.VIS, g=M.g, xs=[], ys=[], j=clamp(M.rows[0]-M.R.lat.pad,0,V-1);
  for(let i=0;i<V;i++){ xs.push((i+0.5)*sceneDx()); ys.push(g.mask[j*V+i]?g.v[j*V+i]:NaN); }
  const Y=1.6*U_FULL;
  axesR(ctx,b,0,AIR.W,-Y,Y,{nx:6,ny:3,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1),
    title:titleFor(b,'pressure along the speaker’s row — one wavelength is '+lenM(M.lam),'pressure along the row'),
    xlab:'distance across the box, m'});
  polyline(ctx,b,xs,ys,0,AIR.W,-Y,Y,COL.pos,1.5);
  /* one wavelength, marked from the first crest past the source */
  const i0=Math.round(cellOfX(M.R,M.speakers[0][0]))-M.R.lat.pad;
  let cr=-1;
  for(let i=i0+3;i<V-2;i++) if(ys[i]>ys[i-1]&&ys[i]>=ys[i+1]&&ys[i]>0.15*U_FULL){ cr=i; break; }
  const px=x=>b.x+b.w*x/AIR.W;
  if(cr>0&&(cr+0.5)*sceneDx()+M.lam<AIR.W){
    const xa=px((cr+0.5)*sceneDx()), xb=px((cr+0.5)*sceneDx()+M.lam), ya=b.y+b.h*0.17;
    ctx.beginPath(); ctx.moveTo(xa,ya); ctx.lineTo(xb,ya);
    ctx.moveTo(xa,ya); ctx.lineTo(xa+6,ya-4); ctx.moveTo(xa,ya); ctx.lineTo(xa+6,ya+4);
    ctx.moveTo(xb,ya); ctx.lineTo(xb-6,ya-4); ctx.moveTo(xb,ya); ctx.lineTo(xb-6,ya+4);
    ctx.strokeStyle=COL.live; ctx.lineWidth=1.5; ctx.stroke();
    lab(ctx,W,H,(xa+xb)/2,ya-11,'λ = '+lenM(M.lam),COL.live,SM_FONT,'center');
  }
}
/* the listener's pressure against time, over the last few periods */
function drawTrace(ctx,W,H,b,M){
  const P=PROBE, n=P.count, Y=1.6*U_FULL, xs=[], ys=[];
  const win=P.n*M.dt;
  for(let q=0;q<n;q++){
    const idx=(P.head-n+q+2*P.n)%P.n;
    xs.push((q-n+1)*M.dt*1000); ys.push(P.buf[idx]);
  }
  axesR(ctx,b,-win*1000,0,-Y,Y,{nx:4,ny:3,xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,1),
    title:titleFor(b,'pressure at the listener over the last period','at the listener'),
    xlab:'time before now, ms'});
  polyline(ctx,b,xs,ys,-win*1000,0,-Y,Y,COL.live,1.6);
  const a=M.listener.amp;
  polyline(ctx,b,[-win*1000,0],[a,a],-win*1000,0,-Y,Y,COL.ref,1.2,[4,3]);
  polyline(ctx,b,[-win*1000,0],[-a,-a],-win*1000,0,-Y,Y,COL.ref,1.2,[4,3]);
  lab(ctx,W,H,b.x+5,b.y+11,'amplitude '+sigf(a,3),COL.ref,SM_FONT,'left');
}
/* the honest half of the Air Pressure screen: what removing the air does to the SPEED
   (nothing) and to the loudness (everything).  c = sqrt(gamma p / rho) and p and rho fall
   together at fixed temperature, so the orange line is flat across the whole slider. */
function drawAirPanel(ctx,W,H,b,M){
  const xs=[], vs=[], as=[];
  for(let q=0;q<=60;q++){
    const fr=q/60;
    xs.push(fr);
    vs.push(soundSpeedIdeal(GAS.T0)/soundSpeedIdeal(GAS.T0));    /* = 1 at every density */
    as.push(fr);                                                  /* p_amp / p_amp(1 atm) */
  }
  /* no y tick at 0: its label sits exactly where the x axis's own 0 goes, and the two
     collide in the corner at every panel size */
  axesR(ctx,b,0,1,0,1.12,{nx:5,yticks:[0.25,0.5,0.75,1],xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,2),
    title:titleFor(b,'take the air away: the speed does not move, the loudness does','speed and loudness'),
    xlab:'air density in the box, atm'});
  polyline(ctx,b,xs,as,0,1,0,1.12,COL.pos,1.8);
  polyline(ctx,b,xs,vs,0,1,0,1.12,COL.ref,1.8);
  const fr=M.air?M.air.frac:1;
  polyline(ctx,b,[fr,fr],[0,1.12],0,1,0,1.12,rgba(COL.live,0.7),1.2,[4,3]);
  marker(ctx,b,0,1,0,1.12,fr,fr,COL.live);
  const lb=legendAuto(ctx,b,[[COL.ref,'speed / its 1 atm value'],[COL.pos,'pressure amplitude / its 1 atm value']]);
  if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
  lab(ctx,W,H,b.x+b.w*fr+7,b.y+13,fr>0?sigf(dbOf(fr),3)+' dB':'silent',COL.live,SM_FONT,'left');
}

