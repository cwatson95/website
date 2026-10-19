
/* ================================================================== *
 *  the plane's geometry, shared by the plane, field-lines and          *
 *  superposition views: 8 m x 5 m at EQUAL aspect (a configuration of  *
 *  charges is a shape), left of the readout, under a measured caption  *
 * ================================================================== */
function planeGeo(ctx,W,H,capFull,capShort){
  const narrow=isNarrow(W), left=16, right=narrow?W-16:W-RO_W-40, top=stageTop();
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H,capFull,capShort,capW,top+220);
  const aw=right-left, ah=Math.max(60,fit.capY-14-top);
  const s=Math.min(aw/(PLANE.x1-PLANE.x0),ah/(PLANE.y1-PLANE.y0));
  const w=s*(PLANE.x1-PLANE.x0), hh=s*(PLANE.y1-PLANE.y0);
  const b=box(left+(aw-w)/2,top+(ah-hh)/2,w,hh);
  const map=worldFitUp(b,{xmin:PLANE.x0,xmax:PLANE.x1,ymin:PLANE.y0,ymax:PLANE.y1},0);
  return {b,map,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,left};
}
function chargePx(map){ return Math.max(6,CHARGE_R*map.s); }
/* lab() on a translucent pad: a value printed over arrows, lines or the voltage
   map stays legible (white on white was unreadable over "direction only") */
function labPad(ctx,W,H,x,y,txt,col,font,align,base){
  const f=font||LAB_FONT; ctx.font=f;
  const al=align||'left', bl=base||'middle', t=plain(txt), fs=parseFloat(f.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  const wp=Math.max(w,ctx.measureText(t).width);
  for(const dy of [0,16,-16,32,-32]){
    let X=x, Y=y+dy;
    if(al==='left') X=clamp(X,2,W-w-2); else if(al==='right') X=clamp(X,w+2,W-2); else X=clamp(X,w/2+2,W-w/2-2);
    Y=clamp(Y,hh,H-hh);
    const lx=al==='center'?X-w/2:(al==='right'?X-w:X), ly=bl==='top'?Y:(bl==='middle'?Y-hh/2:(bl==='bottom'?Y-hh:Y-hh*0.8));
    const bx=[lx,ly,lx+w,ly+hh];
    if(!labFits(bx)) continue;
    LABELS.push(bx);
    const px=al==='center'?X-wp/2:(al==='right'?X-wp:X);
    ctx.fillStyle='rgba(7,11,24,0.8)'; ctx.fillRect(px-3,ly-1,wp+6,hh+2);
    ctx.fillStyle=col||'#aeb6c6'; ctx.textAlign=al; ctx.textBaseline=bl; ctx.fillText(t,X,Y);
    return true;
  }
  return false;
}
function inBox(bx,x,y){ return x>=bx.x&&x<=bx.x1&&y>=bx.y&&y<=bx.y1; }
/* a charge: the disc in its sign's colour with the sign drawn as strokes */
function chargeGlyph(ctx,X,Y,r,q){
  ctx.beginPath(); ctx.arc(X,Y,r,0,TAU); ctx.fillStyle=qCol(q); ctx.fill();
  ctx.strokeStyle=shade(qCol(q),0.5); ctx.lineWidth=1; ctx.stroke();
  const a=r*0.55; ctx.strokeStyle='#0b1020'; ctx.lineWidth=Math.max(1.4,r*0.2);
  ctx.beginPath(); ctx.moveTo(X-a,Y); ctx.lineTo(X+a,Y); if(q>0){ ctx.moveTo(X,Y-a); ctx.lineTo(X,Y+a); } ctx.stroke();
}
function drawCharges(ctx,map,ch){ const r=chargePx(map); for(const c of ch) chargeGlyph(ctx,map.X(c.x),map.Y(c.y),r,c.q); }
/* an E-field sensor: PhET's 7-px ring */
function eSensorGlyph(ctx,X,Y){
  ctx.beginPath(); ctx.arc(X,Y,7,0,TAU); ctx.fillStyle='#0b1020'; ctx.fill(); ctx.strokeStyle=COL.live; ctx.lineWidth=1.6; ctx.stroke();
  ctx.beginPath(); ctx.arc(X,Y,2,0,TAU); ctx.fillStyle=COL.live; ctx.fill();
}
/* PhET's field-arrow proportions (ElectricFieldArrowShape): the whole arrow is
   L long and turns about a point 40 % from the tail; head L/4 long and L/2.5
   wide, tail L/5 wide */
function blockArrow(ctx,X,Y,ux,uy,L,col){
  const t0=-0.4*L, t1=0.6*L, hh=0.25*L, hw=0.2*L, tw=0.1*L, vx=-uy, vy=ux;
  const P=(s,w)=>[X+ux*s+vx*w,Y+uy*s+vy*w];
  const pts=[P(t0,tw),P(t1-hh,tw),P(t1-hh,hw),P(t1,0),P(t1-hh,-hw),P(t1-hh,-tw),P(t0,-tw)];
  ctx.beginPath(); ctx.moveTo(pts[0][0],pts[0][1]); for(let k=1;k<pts.length;k++) ctx.lineTo(pts[k][0],pts[k][1]); ctx.closePath();
  ctx.fillStyle=col; ctx.fill();
}
/* a line arrow in pixels; a double head marks one capped at its drawn maximum */
function arrowPx(ctx,X0,Y0,X1,Y1,col,lw,capped){
  const L=Math.hypot(X1-X0,Y1-Y0); if(L<2) return;
  const ux=(X1-X0)/L, uy=(Y1-Y0)/L, hh=Math.min(9,L*0.4);
  ctx.beginPath(); ctx.moveTo(X0,Y0); ctx.lineTo(X1,Y1);
  for(const back of (capped?[0,6]:[0])){ const Xh=X1-back*ux, Yh=Y1-back*uy;
    ctx.moveTo(Xh,Yh); ctx.lineTo(Xh-hh*ux+0.5*hh*uy,Yh-hh*uy-0.5*hh*ux);
    ctx.moveTo(Xh,Yh); ctx.lineTo(Xh-hh*ux-0.5*hh*uy,Yh-hh*uy+0.5*hh*ux); }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.6; ctx.stroke();
}
/* a world-space arrow clipped to the plane: the shaft by Liang-Barsky in data
   space (the recorder cannot see a canvas clip), the head only if the tip is on
   the plane */
function clipSeg(x0,y0,x1,y1,bx){
  let t0=0,t1=1; const dx=x1-x0, dy=y1-y0;
  for(const [p,q] of [[-dx,x0-bx.x0],[dx,bx.x1-x0],[-dy,y0-bx.y0],[dy,bx.y1-y0]]){
    if(p===0){ if(q<0) return null; continue; }
    const t=q/p; if(p<0){ if(t>t1) return null; if(t>t0) t0=t; } else { if(t<t0) return null; if(t<t1) t1=t; }
  }
  return [x0+t0*dx,y0+t0*dy,x0+t1*dx,y0+t1*dy,t1];
}
function arrowWorldClip(ctx,map,a,v,col,lw,bx){
  const c=clipSeg(a[0],a[1],a[0]+v[0],a[1]+v[1],bx||PLANE); if(!c) return false;
  if(c[4]>=1) arrowPx(ctx,map.X(c[0]),map.Y(c[1]),map.X(c[2]),map.Y(c[3]),col,lw);
  else { ctx.beginPath(); ctx.moveTo(map.X(c[0]),map.Y(c[1])); ctx.lineTo(map.X(c[2]),map.Y(c[3])); ctx.strokeStyle=col; ctx.lineWidth=lw||1.6; ctx.stroke(); }
  return true;
}

/* ---- the plane's layers ---- */
const VQ=32;      /* colour levels per sign for the voltage cells (PhET's colour is continuous) */
function vCellColour(V){ const lv=Math.round(vLevel(V)*VQ); return lv===0?null:shade(V>0?COL.pos:COL.neg,lv/VQ); }
function drawVmap(ctx,map,G){
  const cw=MAP_DX*map.s, buckets={};
  for(let j=0;j<G.ny;j++) for(let i=0;i<G.nx;i++){
    const V=G.v[j*G.nx+i], lv=Math.round(vLevel(V)*VQ); if(lv===0) continue;
    const k=(V>0?1:-1)*lv; (buckets[k]=buckets[k]||[]).push(i,j);
  }
  /* opaque, pre-mixed against the background, each cell widened by half a pixel:
     abutting cells then leave no antialiased seam (Known-bad: seams / corduroy) */
  for(const k in buckets){
    const kk=+k, a=buckets[k];
    ctx.beginPath();
    for(let n=0;n<a.length;n+=2){ const x=PLANE.x0+a[n]*MAP_DX, y=PLANE.y0+(a[n+1]+1)*MAP_DX; ctx.rect(map.X(x)-0.25,map.Y(y)-0.25,cw+0.5,cw+0.5); }
    ctx.fillStyle=shade(kk>0?COL.pos:COL.neg,Math.abs(kk)/VQ); ctx.fill();
  }
}
/* PhET's grid: minor lines every 0.1 m, major every 0.5 m, translucent so that
   over the voltage map they read as lines and not as a mosaic of dark tiles */
function drawGrid(ctx,map,b){
  ctx.lineWidth=1; ctx.strokeStyle='rgba(255,255,255,0.055)'; ctx.beginPath();
  for(let i=1;i<80;i++){ if(i%5===0) continue; const X=Math.round(map.X(PLANE.x0+i*0.1))+0.5; ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); }
  for(let j=1;j<50;j++){ if(j%5===0) continue; const Y=Math.round(map.Y(PLANE.y0+j*0.1))+0.5; ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); }
  ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,0.13)'; ctx.lineWidth=1.6; ctx.beginPath();
  for(let i=1;i<16;i++){ const X=map.X(PLANE.x0+i*0.5); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); }
  for(let j=1;j<10;j++){ const Y=map.Y(PLANE.y0+j*0.5); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); }
  ctx.stroke();
}
function drawArrows(ctx,map,G,dirOnly){
  const L=ARROW_LEN*map.s;
  for(const a of G.a){
    const al=arrowAlpha(a.mag,dirOnly);
    if(!(al>0.004)||!isFinite(a.mag)) continue;
    ctx.globalAlpha=al; blockArrow(ctx,map.X(a.x),map.Y(a.y),a.ex/a.mag,-a.ey/a.mag,L,COL.arrow);
  }
  ctx.globalAlpha=1;
}
/* the plotted equipotentials, clipped to the plane in data space */
function drawEqLines(ctx,W,H,G,M,vals){
  M.eq.forEach(E=>{ if(!E.ok) return;
    const xs=E.pts.map(p=>p[0]), ys=E.pts.map(p=>p[1]); if(E.closed){ xs.push(E.pts[0][0]); ys.push(E.pts[0][1]); }
    polyline(ctx,G.b,xs,ys,PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,COL.struct,1.6);
    if(vals) labPad(ctx,W,H,G.map.X(E.x0)+7,G.map.Y(E.y0)-10,sigf(E.V0c,3)+' V',COL.struct,SM_FONT,'left'); });
}
/* the bin: PhET's enclosure, with its three sources */
const BIN_SRC=[{kind:'pos',x:-0.75,label:'+1 nC'},{kind:'neg',x:0,label:'−1 nC'},{kind:'es',x:0.75,label:'sensors'}];
const BIN_GLYPH_Y=-1.93, BIN_LABEL_Y=-2.2;
function drawBin(ctx,W,H,map,M){
  const X0=map.X(BIN.x0), X1=map.X(BIN.x1), Y0=map.Y(BIN.y1), Y1=map.Y(BIN.y0);
  ctx.fillStyle=COL.bin; ctx.fillRect(X0,Y0,X1-X0,Y1-Y0);
  ctx.strokeStyle=COL.binEdge; ctx.lineWidth=1; ctx.strokeRect(X0+0.5,Y0+0.5,X1-X0-1,Y1-Y0-1);
  for(const s of BIN_SRC){
    const X=map.X(s.x), Y=map.Y(BIN_GLYPH_Y), full=s.kind==='es'?M.st.esens.length>=MAX_SENSORS:M.n>=MAX_CHARGES;
    ctx.globalAlpha=full?0.35:1;
    if(s.kind==='es') eSensorGlyph(ctx,X,Y); else chargeGlyph(ctx,X,Y,chargePx(map),s.kind==='pos'?1:-1);
    ctx.globalAlpha=1;
    lab(ctx,W,H,X,map.Y(BIN_LABEL_Y),s.label,COL.dim,SM_FONT,'center');
  }
}
/* an E-field sensor: the ring, its reading as an arrow at 15 px per V/m at
   128 px/m (PhET's scale, i.e. 0.117 m per V/m), capped at 2 m with a double
   head, and with "values" on, |E| and its direction above it */
const ES_CAP_M=2;
function drawESensor(ctx,W,H,map,s,R,vals){
  const X=map.X(s.x), Y=map.Y(s.y);
  if(!R.over&&R.mag>0){
    const Lm=R.mag*SENSOR_M_PER_VM, capped=Lm>ES_CAP_M, L=Math.min(Lm,ES_CAP_M)*map.s;
    arrowPx(ctx,X,Y,X+L*R.ex/R.mag,Y-L*R.ey/R.mag,COL.live,2.2,capped);
  }
  eSensorGlyph(ctx,X,Y);
  if(vals){
    labPad(ctx,W,H,X,Y-25,R.over?'—':sigf(R.mag,3)+' V/m',COL.live,SM_FONT,'center');
    labPad(ctx,W,H,X,Y-12,R.over?'—':(R.mag>0?fmt(R.ang,1)+'°':'no direction'),COL.live,SM_FONT,'center');
  }
}
/* the voltage sensor: crosshair ring, and below it a panel with the reading
   and PhET's two buttons (plot an equipotential, clear them) */
function vsGeo(map,st,W,H){
  /* the panel hangs below the crosshair, and flips above it rather than leave
     the plane (it ran over the caption at the plane's bottom edge) */
  const X=map.X(st.vs.x), Y=map.Y(st.vs.y), r=Math.max(9,0.09*map.s), pw=132, ph=50;
  let py=Y+r+8; if(py+ph>Math.min(H-4,map.Y(PLANE.y0))) py=Y-r-8-ph;
  const px=clamp(X-pw/2,4,W-pw-4), bw=56, bh=18, by=py+ph-bh-6;
  return {X,Y,r,panel:box(px,py,pw,ph),plot:box(px+6,by,bw,bh),clear:box(px+pw-6-bw,by,bw,bh)};
}
function canvasButton(ctx,W,H,b,txt){
  ctx.fillStyle='#10131b'; ctx.fillRect(b.x,b.y,b.w,b.h);
  ctx.strokeStyle='#3a4152'; ctx.lineWidth=1; ctx.strokeRect(b.x+0.5,b.y+0.5,b.w-1,b.h-1);
  lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2,txt,'#cfd4de',SM_FONT,'center');
}
function drawVSensor(ctx,W,H,map,st,R){
  const g=vsGeo(map,st,W,H);
  ctx.beginPath(); ctx.arc(g.X,g.Y,g.r,0,TAU); ctx.strokeStyle=COL.live; ctx.lineWidth=1.8; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(g.X-g.r-5,g.Y); ctx.lineTo(g.X+g.r+5,g.Y); ctx.moveTo(g.X,g.Y-g.r-5); ctx.lineTo(g.X,g.Y+g.r+5);
  ctx.lineWidth=1; ctx.stroke();
  const P=g.panel;
  ctx.beginPath(); ctx.moveTo(g.X,P.y>g.Y?g.Y+g.r:g.Y-g.r); ctx.lineTo(clamp(g.X,P.x+6,P.x1-6),P.y>g.Y?P.y:P.y1); ctx.strokeStyle=rgba(COL.live,0.5); ctx.stroke();
  ctx.fillStyle='rgba(10,12,18,0.94)'; ctx.fillRect(P.x,P.y,P.w,P.h);
  ctx.strokeStyle='#3a4152'; ctx.strokeRect(P.x+0.5,P.y+0.5,P.w-1,P.h-1);
  lab(ctx,W,H,P.x+P.w/2,P.y+12,R?(isFinite(R.V)?sigf(R.V,3)+' V':'— (on a charge)'):'—','#ffffff','12px -apple-system, sans-serif','center');
  canvasButton(ctx,W,H,g.plot,'plot'); canvasButton(ctx,W,H,g.clear,'clear');
}
/* the tape: two ends, the length in centimetres (PhET's unit) */
function drawTape(ctx,W,H,map,t,T){
  const A=[map.X(t.ax),map.Y(t.ay)], B=[map.X(t.bx),map.Y(t.by)], L=Math.hypot(B[0]-A[0],B[1]-A[1]);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=2.2; ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]); ctx.stroke();
  if(L>1){ const ux=(B[0]-A[0])/L, uy=(B[1]-A[1])/L, n=Math.floor(T.L/0.1);
    ctx.lineWidth=1; ctx.beginPath();
    for(let k=1;k<=n;k++){ const d=k*0.1*map.s, big=k%5===0?6:3.5; ctx.moveTo(A[0]+ux*d-uy*big,A[1]+uy*d+ux*big); ctx.lineTo(A[0]+ux*d,A[1]+uy*d); }
    ctx.stroke();
    const mx=(A[0]+B[0])/2, my=(A[1]+B[1])/2, off=uy>0?1:-1;
    lab(ctx,W,H,mx+uy*14*off,my-ux*14*off,fmt(T.cm,1)+' cm',COL.struct,LAB_FONT,'center'); }
  for(const [P,nm] of [[A,'A'],[B,'B']]){ dot(ctx,P[0],P[1],5,'#0b1020',COL.struct,1.6); lab(ctx,W,H,P[0]+8,P[1]-9,nm,COL.struct,SM_FONT); }
}
/* PhET's "1 meter" scale, at (2, -2.2) m, shown with the grid and values */
function drawMeter(ctx,W,H,map){
  const Y=map.Y(-2.2), X0=map.X(2), X1=map.X(3);
  arrowPx(ctx,X0,Y,X1,Y,COL.live,1.4); arrowPx(ctx,X1,Y,X0,Y,COL.live,1.4);
  lab(ctx,W,H,(X0+X1)/2,Y+10,'1 meter',COL.live,SM_FONT,'center');
}

/* ================================================================== *
 *  view: the plane (PhET's screen)                                    *
 * ================================================================== */
const PLANE_CAP_FULL='Drag +1 nC and −1 nC charges and E-field sensors out of the bin; drop them back in it to take them away. '
  +'Arrows: the field at 0.5-m cell centres, all one length (0.31 m); their brightness follows |E| up to 5 V/m, or all are bright with “direction only”. '
  +'Voltage: 0.1-m cells, green for V > 0 and magenta for V < 0, saturating at ±40 V. The sensor arrow is 0.117 m per V/m (PhET’s scale), capped at 2 m (double head). '
  +'The voltage sensor’s plot traces the equipotential through its crosshair; moving a charge clears them.';
const PLANE_CAP_SHORT='Drag charges and sensors from the bin. Arrows: one length, brightness ∝ |E| to 5 V/m. Voltage saturates at ±40 V.';
function drawPlane(ctx,W,H,M){
  const G=planeGeo(ctx,W,H,PLANE_CAP_FULL,PLANE_CAP_SHORT), b=G.b, map=G.map, st=M.st;
  ctx.fillStyle=COL.plane; ctx.fillRect(b.x,b.y,b.w,b.h);
  if(M.vmap) drawVmap(ctx,map,M.vmap);
  if(st.showGrid) drawGrid(ctx,map,b);
  drawEqLines(ctx,W,H,G,M,st.showVals);
  if(M.arrows) drawArrows(ctx,map,M.arrows,st.dirOnly);
  frame(ctx,b,'#2a3346');
  drawBin(ctx,W,H,map,M);
  if(st.showTape) drawTape(ctx,W,H,map,st.tape,M.tape);
  drawCharges(ctx,map,M.ch);
  M.esR.forEach((R,i)=>drawESensor(ctx,W,H,map,st.esens[i],R,st.showVals));
  if(st.showVS) drawVSensor(ctx,W,H,map,st,M.vsR);
  if(st.showGrid&&st.showVals) drawMeter(ctx,W,H,map);
  if(!M.n) lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.28,'no charges on the plane: drag one out of the bin, or pick a preset',COL.dim,LAB_FONT,'center');
  caption(ctx,G.left,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  view: field lines                                                  *
 * ================================================================== */
const LINES_CAP_FULL='Field lines leave the charges of the majority sign (the positive ones when the plane is neutral) at equal angles and follow E; '
  +'each ends on a charge of the other sign, runs off past 10 km, or ends at a null. The plane is a slice through a 3-D field, so the number of lines '
  +'reaching a charge is not proportional to its charge, and a line can end where the field turns out of the plane. Cyan: equipotentials every ΔV '
  +'(dashed, V = 0), contoured on a 4-cm grid. Orange: the null points, where E = 0. Drag the charges.';
const LINES_CAP_SHORT='Lines follow E from the majority charges; cyan equipotentials every ΔV; orange, E = 0. A 3-D field, sliced.';
function drawFamily(ctx,map,fam){
  for(const f of fam){
    ctx.beginPath(); const s=f.segs;
    for(let k=0;k<s.length;k+=4){ ctx.moveTo(map.X(s[k]),map.Y(s[k+1])); ctx.lineTo(map.X(s[k+2]),map.Y(s[k+3])); }
    ctx.strokeStyle=rgba(COL.struct,f.V===0?0.75:0.42); ctx.lineWidth=1; if(f.V===0) ctx.setLineDash([4,4]); ctx.stroke(); ctx.setLineDash([]);
  }
}
/* the drawn polyline of a traced line: from the seed charge's centre to the
   capturing charge's centre, so a line visibly starts and ends on charges */
function linePolyline(M,L){
  const pts=[[M.ch[L.from].x,M.ch[L.from].y]].concat(L.pts);
  if(L.end==='charge') pts.push([M.ch[L.hit].x,M.ch[L.hit].y]);
  return pts;
}
function drawFieldLines(ctx,G,M){
  const b=G.b, map=G.map, spacing=1.1;
  for(const L of M.FL.lines){
    const pts=linePolyline(M,L), xs=pts.map(p=>p[0]), ys=pts.map(p=>p[1]);
    polyline(ctx,b,xs,ys,PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,rgba(COL.pos,0.85),1.3);
    /* arrowheads every ~1.1 m of line on the plane, clear of the charges */
    let acc=0.55;
    for(let k=1;k<pts.length;k++){
      const a=pts[k-1], c=pts[k], d=Math.hypot(c[0]-a[0],c[1]-a[1]); acc+=d;
      if(acc<spacing) continue;
      if(c[0]<PLANE.x0||c[0]>PLANE.x1||c[1]<PLANE.y0||c[1]>PLANE.y1||nearestCharge(M.ch,c[0],c[1]).r<0.3||!(d>0)) continue;
      acc=0;
      const ux=(c[0]-a[0])/d*M.FL.sgn, uy=-(c[1]-a[1])/d*M.FL.sgn, X=map.X(c[0]), Y=map.Y(c[1]);
      ctx.beginPath(); ctx.moveTo(X+ux*4.5,Y+uy*4.5); ctx.lineTo(X-ux*3-uy*3,Y-uy*3+ux*3); ctx.lineTo(X-ux*3+uy*3,Y-uy*3-ux*3); ctx.closePath();
      ctx.fillStyle=COL.pos; ctx.fill();
    }
  }
}
function drawNulls(ctx,W,H,map,nulls){
  for(const N of nulls){
    const X=map.X(N.x), Y=map.Y(N.y);
    ctx.strokeStyle=COL.ref; ctx.lineWidth=1.8; ctx.beginPath();
    if(N.kind==='saddle'){ ctx.moveTo(X-5,Y-5); ctx.lineTo(X+5,Y+5); ctx.moveTo(X-5,Y+5); ctx.lineTo(X+5,Y-5); }
    else { ctx.moveTo(X,Y-6); ctx.lineTo(X+6,Y); ctx.lineTo(X,Y+6); ctx.lineTo(X-6,Y); ctx.closePath(); }
    ctx.stroke();
    /* named one by one only when there are few (the two rows have twelve, and
       their labels piled onto the charges); the readout lists them all */
    if(nulls.length<=4) labPad(ctx,W,H,X+9,Y-9,N.kind==='saddle'?'saddle':'in-plane '+(N.kind==='min'?'minimum':'maximum'),COL.ref,SM_FONT,'left');
  }
}
function drawLines(ctx,W,H,M){
  const G=planeGeo(ctx,W,H,LINES_CAP_FULL,LINES_CAP_SHORT), b=G.b, map=G.map, st=M.st;
  ctx.fillStyle=COL.plane; ctx.fillRect(b.x,b.y,b.w,b.h);
  if(M.fam) drawFamily(ctx,map,M.fam);
  drawFieldLines(ctx,G,M);
  frame(ctx,b,'#2a3346');
  drawCharges(ctx,map,M.ch);
  if(st.showNulls) drawNulls(ctx,W,H,map,M.nulls);
  if(!M.n) lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.4,'no charges: pick a preset, or add charges on the plane',COL.dim,LAB_FONT,'center');
  else labPad(ctx,W,H,b.x+8,b.y+10,M.FL.lines.length+' lines from the '+(M.FL.sgn>0?'positive':'negative')+' charges: '+M.FL.ends+' end on charges, '
    +M.FL.escapes+' run off past 10 km'+(M.FL.nulls?', '+M.FL.nulls+' end at a null':'')+(M.nulls.length>4&&st.showNulls?'; orange: '+M.nulls.length+' nulls':''),'#aeb6c6',SM_FONT,'left','top');
  caption(ctx,G.left,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
}
