
/* ================================================================== *
 *  the lattice drawing shared with wave-interference: extracted BY    *
 *  NAME and unchanged from build/wave-interference/p4_views.js —      *
 *  the 49 colour classes and the field (one fill per class, runs      *
 *  merged, pixel-snapped), the positions of PhET's 21 x 21 air        *
 *  parcels, the tape measure and the probes.  make_parts.py; nothing  *
 *  retyped.  Their dependencies (COL, U_FULL, TOOLS, lenU) are        *
 *  defined in p3_state.js, with the same names and meanings.          *
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
function cellX(sq,R,i){ return sq.x+(i-R.lat.pad+0.5)*sq.w/LAT.VIS; }
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
