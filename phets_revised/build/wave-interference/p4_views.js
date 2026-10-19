
/* ================================================================== *
 *  the lattice views: the field, the side view, the sound parcels,    *
 *  the sources and the barrier, the tools, the charts                 *
 * ================================================================== */
const NLEV=49, HALF=24;                                  /* 49 colour classes, zero on the middle one */
function levelOf(v){ const t=v/U_FULL; return Math.round(((t<-1?-1:(t>1?1:t))+1)*HALF); }
const LEVEL_CACHE={};
function levelCols(scene,lam){
  const key=scene+'|'+(scene==='light'?fmt(lam,2):'');
  if(LEVEL_CACHE[key]) return LEVEL_CACHE[key];
  const out=[], top=scene==='light'?specCss(lam,1):null;
  for(let q=0;q<NLEV;q++){ const f=q/(NLEV-1);
    out.push(scene==='water'?mix(COL.water0,COL.water1,f):(scene==='sound'?mix('#000000','#f2f2f2',f):mix('#000000',top,f))); }
  return LEVEL_CACHE[key]=out;
}
/* the field as colour classes: one fill per class, horizontal runs merged,
   edges snapped to whole pixels so abutting runs leave no seams; light's
   cells the wave has not reached are black (PhET's visited mask) */
function drawField(ctx,sq,R){
  const L=R.lat, pad=L.pad, nx=L.nx, u=L.u, vis=L.vis, light=R.scene==='light';
  const lam=waveLen(SCENES[R.scene],R.f), cols=levelCols(R.scene,lam), cs=sq.w/LAT.VIS;
  ctx.fillStyle=light?'#000000':cols[HALF]; ctx.fillRect(sq.x,sq.y,sq.w,sq.h);
  const rects=[]; for(let q=0;q<NLEV;q++) rects.push([]);
  let nCells=0;
  for(let j=0;j<LAT.VIS;j++){
    const row=(pad+j)*nx+pad, y0=Math.round(sq.y+j*cs), y1=Math.round(sq.y+(j+1)*cs);
    let i=0;
    while(i<LAT.VIS){
      const q=(light&&!vis[row+i])?-1:levelOf(u[row+i]);
      let e=i+1;
      while(e<LAT.VIS&&((light&&!vis[row+e])?-1:levelOf(u[row+e]))===q) e++;
      if(q>=0&&(light||q!==HALF)){ rects[q].push(Math.round(sq.x+i*cs),y0,Math.round(sq.x+e*cs),y1); nCells+=e-i; }
      i=e;
    }
  }
  for(let q=0;q<NLEV;q++){ const r=rects[q]; if(!r.length) continue;
    ctx.beginPath(); for(let k=0;k<r.length;k+=4) ctx.rect(r[k],r[k+1],r[k+2]-r[k],r[k+3]-r[k+1]);
    ctx.fillStyle=cols[q]; ctx.fill(); }
  return nCells;
}
/* PhET's side view (water): the surface along the centre row, the water below */
function drawSide(ctx,sq,R){
  const L=R.lat, pad=L.pad, nx=L.nx, mid=(L.ny-1)/2, cs=sq.w/LAT.VIS;
  const yb=sq.y+0.52*sq.h, hs=0.16*sq.h/U_FULL;
  ctx.fillStyle='#03060d'; ctx.fillRect(sq.x,sq.y,sq.w,sq.h);
  const pts=[[sq.x,sq.y1]];
  for(let i=0;i<LAT.VIS;i++){ const v=clamp(L.u[mid*nx+pad+i],-2.5*U_FULL,2.5*U_FULL); pts.push([sq.x+(i+0.5)*cs,yb-hs*v]); }
  pts.push([sq.x1,sq.y1]);
  ctx.beginPath(); pts.forEach((p,k)=>{ if(k===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); ctx.closePath();
  ctx.fillStyle=mix(COL.water0,'#1d5f96',0.55); ctx.fill();
  ctx.beginPath(); for(let k=1;k<pts.length-1;k++){ if(k===1) ctx.moveTo(pts[k][0],pts[k][1]); else ctx.lineTo(pts[k][0],pts[k][1]); }
  ctx.strokeStyle=COL.water1; ctx.lineWidth=1.6; ctx.stroke();
  /* the dripper over the source and a drop that lands at each crest of the drive */
  const xs=sq.x+(srcCol(L)-pad+0.5)*cs;
  ctx.fillStyle='#6b7285'; ctx.fillRect(xs-9,sq.y+6,18,14); ctx.fillRect(xs-3,sq.y+20,6,8);
  if(R.cont||R.pulse.on){ const ph=((R.phi/TAU)%1+1)%1, yd=sq.y+32+ph*(yb-sq.y-40);
    ctx.beginPath(); ctx.arc(xs,yd,3.2,0,TAU); ctx.fillStyle=COL.water1; ctx.fill(); }
}
/* air parcels on PhET's 21 x 21 grid, pushed along grad p: for one frequency the
   displacement is xi = grad p / (rho omega^2), so parcels crowd where p is high.
   Scaled so the largest push is 0.3 of their spacing. */
function parcelPositions(R){
  const S=SCENES[R.scene], L=R.lat, nx=L.nx, k=TAU/R.Nl, KD=0.3*(LAT.VIS/20)/(k*U_FULL), out=[];
  for(let a=0;a<=20;a++) for(let b=0;b<=20;b++){
    const x=a*S.W/20, y=b*S.W/20, X=cellOfX(R,x), Y=cellOfX(R,y);
    const i=clamp(Math.round(X),1,nx-2), j=clamp(Math.round(Y),1,L.ny-2), q=j*nx+i;
    const gx=(L.u[q+1]-L.u[q-1])/2, gy=(L.u[q+nx]-L.u[q-nx])/2;
    out.push([X+KD*gx,Y+KD*gy]);
  }
  return out;
}
function drawParcels(ctx,sq,R){
  const P=parcelPositions(R), cs=sq.w/LAT.VIS, pad=R.lat.pad;
  ctx.beginPath();
  for(let q=0;q<P.length;q++){ if(q===220) continue;
    const x=sq.x+(P[q][0]-pad+0.5)*cs, y=sq.y+(P[q][1]-pad+0.5)*cs;
    if(x<sq.x||x>sq.x1||y<sq.y||y>sq.y1) continue;
    ctx.moveTo(x+2.1,y); ctx.arc(x,y,2.1,0,TAU); }
  ctx.fillStyle='#d6dae4'; ctx.fill();
  const c=P[220]; dot(ctx,sq.x+(c[0]-pad+0.5)*cs,sq.y+(c[1]-pad+0.5)*cs,3.4,COL.live);
}
function cellX(sq,R,i){ return sq.x+(i-R.lat.pad+0.5)*sq.w/LAT.VIS; }
function modelToPx(sq,S,x,y){ return [sq.x+x/S.W*sq.w, sq.y+y/S.W*sq.h]; }
function drawSources(ctx,sq,R){
  if(R.mode==='plane'){
    ctx.fillStyle=R.plane.on?COL.struct:'#3a4254'; ctx.fillRect(sq.x-9,sq.y,6,sq.h);
    return;
  }
  const rows=runSourceRows(R), cs=sq.w/LAT.VIS;
  rows.forEach((j,s)=>{ const x=cellX(sq,R,srcCol(R.lat)), y=sq.y+(j-R.lat.pad+0.5)*cs, on=R.src[s];
    dot(ctx,x,y,5,on?COL.live:'#3a4254','#ffffff',1.2); });
}
function drawBarrier(ctx,sq,R){
  const P=R.plane; if(P.barrier==='none') return;
  const cs=sq.w/LAT.VIS, x=cellX(sq,R,P.bcol), w=Math.max(4,cs), pad=R.lat.pad;
  let j=pad; ctx.fillStyle=COL.barrier;
  while(j<pad+LAT.VIS){
    if(slitOpen(R,j)){ j++; continue; }
    let e=j+1; while(e<pad+LAT.VIS&&!slitOpen(R,e)) e++;
    ctx.fillRect(x-w/2,sq.y+(j-pad)*cs,w,(e-j)*cs); j=e;
  }
  /* the handle (PhET's green double arrow): drag it to move the barrier */
  const yh=sq.y1+13;
  ctx.beginPath(); ctx.moveTo(x-16,yh); ctx.lineTo(x+16,yh);
  ctx.moveTo(x-16,yh); ctx.lineTo(x-10,yh-4); ctx.moveTo(x-16,yh); ctx.lineTo(x-10,yh+4);
  ctx.moveTo(x+16,yh); ctx.lineTo(x+10,yh-4); ctx.moveTo(x+16,yh); ctx.lineTo(x+10,yh+4);
  ctx.strokeStyle=COL.live; ctx.lineWidth=2; ctx.stroke();
}
function drawTape(ctx,W,H,sq,S,M){
  const a=TOOLS.tape[0], b=TOOLS.tape[1];
  const A=[sq.x+a[0]*sq.w,sq.y+a[1]*sq.h], B=[sq.x+b[0]*sq.w,sq.y+b[1]*sq.h];
  ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]); ctx.strokeStyle='#f1e7b0'; ctx.lineWidth=2; ctx.stroke();
  dot(ctx,A[0],A[1],5,COL.live,'#ffffff',1); dot(ctx,B[0],B[1],5,COL.live,'#ffffff',1);
  lab(ctx,W,H,(A[0]+B[0])/2,Math.min(A[1],B[1])-12,lenU(M.tapeLen,S),'#f1e7b0',LAB_FONT,'center');
}
function drawProbes(ctx,sq){
  TOOLS.probes.forEach((p,q)=>{ const x=sq.x+p[0]*sq.w, y=sq.y+p[1]*sq.h, c=q===0?COL.pos:COL.live;
    ctx.beginPath(); ctx.arc(x,y,7,0,TAU); ctx.strokeStyle=c; ctx.lineWidth=2; ctx.stroke(); dot(ctx,x,y,2,c); });
}
function nodalOverlay(ctx,sq,R,S){
  const rows=runSourceRows(R), dx=sceneDx(S), d=(rows[1]-rows[0])*dx, lam=waveLen(S,R.f);
  const xs0=xOfCell(R,srcCol(R.lat)), yc=S.W/2, n=48;
  let drawn=0;
  /* hyperY is the pinned formula; the drawing never re-derives it */
  for(let m=0;(m+0.5)*lam<d;m++){
    const D=(m+0.5)*lam;
    for(const sg of [1,-1]){
      const xs=[], ys=[];
      for(let q=0;q<=n;q++){ const x=S.W*q/n; xs.push(x); ys.push(yc+sg*hyperY(d,D,x-xs0)); }
      polyline(ctx,sq,xs,ys,0,S.W,S.W,0,COL.ref,1.3,[5,4]); drawn++;
    }
  }
  return drawn;
}
function slitRays(ctx,sq,R,S){
  const P=R.plane; if(P.barrier!=='two') return 0;
  const g=slitCells(R), dx=sceneDx(S), d=g.d*dx, lam=waveLen(S,R.f), xb=xOfCell(R,P.bcol), yc=S.W/2;
  let n=0;
  for(let m=-6;m<=6;m++){ const s=m*lam/d; if(Math.abs(s)>=1) continue;
    const th=Math.asin(s), L=2*S.W; polyline(ctx,sq,[xb,xb+L*Math.cos(th)],[yc,yc+L*Math.sin(th)],0,S.W,S.W,0,COL.ref,1,[3,5]); n++; }
  return n;
}

/* ---- layout for the three lattice views ---- */
function latGeo(ctx,W,H,M){
  const R=M.L.R, light=R.scene==='light', narrow=isNarrow(W), top=stageTop()+30, v=M.view;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,latCaption(M,true),latCaption(M,false),capW,top+220);
  const avail=fit.capY-18-top;
  const showScr=light&&ST.screen, showI=light&&ST.inten;
  let gH=ST.graph?Math.max(64,Math.min(130,Math.round(avail*0.2))):0;
  const gGap=(v==='slits'?50:38);
  /* below the square: the graph and its axis labels, else the intensity graph's
     labels or the barrier's handle — measured, so nothing lands on the caption */
  const below=()=>Math.max(gH?gH+gGap+36:0, showI?38:0, v==='slits'?24:0);
  if(gH&&avail-below()<150) gH=0;               /* no room for the graph at this size: a note says so */
  const rightNeed=(showScr?40:0)+(showI?(narrow?120:190):0);
  const side=Math.max(100,Math.floor(Math.min(avail-below(), W-56-30-rightNeed, narrow?W:W*0.6)));
  const sq=box(56,top,side,side);
  const G={sq,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,narrow};
  let xr=sq.x1+14;
  if(showScr){ G.scr=box(xr,sq.y,22,sq.h); xr+=34; }
  if(showI){ G.ib=box(xr,sq.y,(narrow?100:160),sq.h); xr=G.ib.x1+16; }
  if(ST.graph&&gH) G.gb=box(sq.x,sq.y1+gGap,sq.w,gH);
  G.graphDropped=ST.graph&&!gH;
  /* the wave meter's chart goes below the floating readout (which reaches ~480 px) */
  if(ST.meter&&!narrow){
    const x0=Math.max(xr+44,sq.x1+60), y0=486+24, y1=fit.capY-40;
    if(W-24-x0>=150&&y1-y0>=60) G.mb=box(x0,y0,W-24-x0,y1-y0);
  }
  return G;
}
function latCaption(M,full){
  const L=M.L, R=L.R, S=L.S, v=M.view;
  const what={water:'water level',sound:'pressure',light:'electric field'}[R.scene];
  const base=S.name+': '+fmt(S.W,0)+' '+S.unit+' across, 111 lattice cells of '+sigf(L.dx,3)+' '+S.unit+'; colour is the '+what
    +' (±2.14 in lattice units is full colour, PhET’s scale).';
  if(!full) return base;
  let s=base;
  if(v==='tank') s+=' One source five cells in from the left edge; the waves leave through Mur’s absorbing boundary 20 cells beyond the frame.';
  if(v==='two') s+=' Two in-phase sources '+lenU(L.dEff,S)+' apart on the lattice'+(ST.nodal?'; the dashed orange lines are where r₁ − r₂ = (m + ½)λ':'')+'.';
  if(v==='slits') s+=' A plane wave from the left meets the barrier (drag its arrow)'+(ST.theory&&R.plane.barrier==='two'?'; orange rays are d sin θ = mλ from the midpoint':'')+'.';
  if(R.scene==='light'&&(ST.screen||ST.inten)) s+=' The screen is the last visible column; intensity is its mean square over whole periods'+(ST.theory&&v!=='tank'?', against the Rayleigh–Sommerfeld sum (orange) and the Fraunhofer formula (dashed)':'')+'.';
  if(R.scene==='sound'&&ST.soundView!=='waves') s+=' Air parcels are pushed along ∇p, exaggerated to ≤ 0.3 of their spacing.';
  if(ST.look==='side'&&R.scene==='water') s+=' Side view along the centre row: the height is the water level in lattice units, not to scale with the tank.';
  return s;
}
function drawLatticeView(ctx,W,H,M){
  const G=latGeo(ctx,W,H,M), sq=G.sq, R=M.L.R, S=M.L.S, v=M.view;
  if(R.scene==='water'&&ST.look==='side') drawSide(ctx,sq,R);
  else {
    const showWaves=!(R.scene==='sound'&&ST.soundView==='particles');
    if(showWaves) drawField(ctx,sq,R); else { ctx.fillStyle='#05070c'; ctx.fillRect(sq.x,sq.y,sq.w,sq.h); }
    if(R.scene==='sound'&&ST.soundView!=='waves') drawParcels(ctx,sq,R);
  }
  frame(ctx,sq,'#2a3040');
  if(v==='two'&&ST.nodal&&!(R.scene==='water'&&ST.look==='side')) nodalOverlay(ctx,sq,R,S);
  if(v==='slits'){ drawBarrier(ctx,sq,R); if(ST.theory&&!(R.scene==='water'&&ST.look==='side')) slitRays(ctx,sq,R,S); }
  drawSources(ctx,sq,R);
  /* PhET's scale bar and its time line */
  const sb=S.scaleLen/S.W*sq.w, yb=sq.y-10;
  ctx.fillStyle='#cfd4de'; ctx.fillRect(sq.x,yb-2,sb,3);
  lab(ctx,W,H,sq.x+sb+6,yb,S.scaleLen+' '+S.unit,'#cfd4de',SM_FONT,'left');
  const conv=sq.w<380?'':(S.tunit==='ms'?'  (1 ms = 10⁻³ s)':S.tunit==='fs'?'  (1 fs = 10⁻¹⁵ s)':'');
  lab(ctx,W,H,sq.x1,yb,(ST.running?'':'paused · ')+'t = '+sigf(R.t,3)+' '+S.tunit+conv,'#8b93a6',SM_FONT,'right');
  if(ST.tape) drawTape(ctx,W,H,sq,S,M.L);
  if(ST.meter) drawProbes(ctx,sq);
  if(ST.watch){ const t='stopwatch '+sigf(R.watch.t,4)+' '+S.tunit, tw=t.length*11*0.52+14;
    ctx.fillStyle='rgba(10,12,18,.8)'; ctx.fillRect(sq.x1-tw-6,sq.y+6,tw,20);
    lab(ctx,W,H,sq.x1-tw+1,sq.y+16,t,R.watch.on?COL.pos:'#cfd4de',LAB_FONT,'left'); }
  if(G.scr) drawScreenStrip(ctx,G.scr,M);
  if(G.ib) drawIntensity(ctx,W,H,G.ib,M);
  if(G.gb) drawCentreGraph(ctx,W,H,G.gb,M);
  if(G.mb) drawMeter(ctx,W,H,G.mb,M);
  /* notes on a translucent pad, legible over the field */
  const note=(y,t)=>{ ctx.fillStyle='rgba(7,11,24,.78)'; ctx.fillRect(sq.x+4,y-8,t.length*10.5*0.52+10,16); lab(ctx,W,H,sq.x+8,y,t,'#aeb6c6',SM_FONT,'left'); };
  /* short forms where the tank is narrow, so a note cannot run out past its right edge */
  const tight=sq.w<300;
  if(!G.mb&&ST.meter) note(sq.y1-12,tight?'meter: wider window':'wave meter: widen the window to see its chart');
  if(G.graphDropped) note(sq.y1-(ST.meter&&!G.mb?30:12),tight?'graph: taller window':'centre-line graph: needs a taller window');
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}
function drawScreenStrip(ctx,b,M){
  const L=M.L, I=L.I, lam=L.lam, rows=I.length, mx=L.Imax>0?L.Imax:1;
  ctx.fillStyle='#000000'; ctx.fillRect(b.x,b.y,b.w,b.h);
  const cs=b.h/rows, groups={};
  for(let r=0;r<rows;r++){ const q=Math.round(20*clamp(I[r]/mx,0,1)); if(q===0) continue; (groups[q]=groups[q]||[]).push(r); }
  for(const q in groups){ ctx.beginPath(); for(const r of groups[q]) ctx.rect(b.x,Math.round(b.y+r*cs),b.w,Math.round(b.y+(r+1)*cs)-Math.round(b.y+r*cs));
    ctx.fillStyle=specCss(lam,q/20); ctx.fill(); }
  frame(ctx,b,'#2a3040');
}
function drawIntensity(ctx,W,H,b,M){
  const L=M.L, I=L.I, S=L.S, rows=I.length, mx=L.Imax>0?L.Imax:1, ys=[], xs=[];
  for(let r=0;r<rows;r++){ ys.push((r+0.5)*S.W/rows); xs.push(I[r]/mx); }
  /* no y ticks: the vertical axis is the lattice's own, row for row */
  axesR(ctx,b,0,1.05,S.W,0,{xticks:[0,0.5,1],yticks:[],xfmt:t=>fmt(t,1),title:'intensity',xlab:'I / its peak'});
  if(L.th){ polyline(ctx,b,Array.from(L.th.far),ys,0,1.05,S.W,0,COL.ref,1.2,[4,3]); polyline(ctx,b,Array.from(L.th.exact),ys,0,1.05,S.W,0,COL.ref,1.4); }
  polyline(ctx,b,xs,ys,0,1.05,S.W,0,COL.pos,1.8);
}
function drawCentreGraph(ctx,W,H,b,M){
  const R=M.L.R, S=M.L.S, Lt=R.lat, mid=(Lt.ny-1)/2, xs=[], ys=[];
  for(let i=0;i<LAT.VIS;i++){ xs.push(xOfCell(R,Lt.pad+i)); ys.push(Lt.u[mid*Lt.nx+Lt.pad+i]); }
  const Y=1.5*U_FULL;
  axesR(ctx,b,0,S.W,-Y,Y,{nx:6,ny:3,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),title:titleFor(b,'the centre line: '+S.what+' along the middle row','the centre line'),xlab:'position, '+S.unit});
  polyline(ctx,b,xs,ys,0,S.W,-Y,Y,COL.pos,1.6);
}
function drawMeter(ctx,W,H,b,M){
  const R=M.L.R, S=M.L.S, tr=R.trace, win=2.5/S.fmin, t1=R.t, t0=Math.max(0,t1-win), Y=1.5*U_FULL;
  axesR(ctx,b,t0,t0+win,-Y,Y,{nx:5,ny:3,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),title:titleFor(b,'wave meter: the two probes against time','wave meter'),xlab:'time, '+S.tunit});
  for(let p=0;p<2;p++){ const xs=[], ys=[];
    for(const s of tr) if(s[0]>=t0&&s.length>p+1){ xs.push(s[0]); ys.push(s[p+1]); }
    polyline(ctx,b,xs,ys,t0,t0+win,-Y,Y,p===0?COL.pos:COL.live,1.5); }
}
