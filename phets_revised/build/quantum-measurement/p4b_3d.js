
/* ================================================================== *
 *  the Bloch sphere in 3-D: z-up orbit camera and a wireframe sphere, *
 *  adapted from bloch_sphere.html (its camera, drawSphere, drawVec,   *
 *  drawPath3, dot3); the grid is batched into two strokes, near/far   *
 * ================================================================== */
const CAM_HOME={theta:0.6, phi:0.35};      /* x toward the viewer, y right, z up: all three axes >= 0.6 of full length (asserted) */
const CAM_DIST=5.2;
function camBasis3(theta,phi){
  const ct=Math.cos(theta), stt=Math.sin(theta), cp=Math.cos(phi), sp=Math.sin(phi);
  const dir=[ct*cp,stt*cp,sp], fwd=[-dir[0],-dir[1],-dir[2]];
  let right=[fwd[1]*1-fwd[2]*0, fwd[2]*0-fwd[0]*1, 0];            /* fwd x z */
  const rl=Math.hypot(right[0],right[1],right[2])||1; right=[right[0]/rl,right[1]/rl,right[2]/rl];
  const up=[right[1]*fwd[2]-right[2]*fwd[1], right[2]*fwd[0]-right[0]*fwd[2], right[0]*fwd[1]-right[1]*fwd[0]];
  return {dir,fwd,right,up};
}
/* perspective from CAM_DIST: the sphere's centre plane maps to radius pixR */
function sphereProj(cam,cx,cy,pixR){
  const B=camBasis3(cam.theta,cam.phi), k=pixR*CAM_DIST;
  const P=p=>{ const z=dot3v(p,B.fwd)+CAM_DIST; if(z<=0.05) return null;
    return [cx+k*dot3v(p,B.right)/z, cy-k*dot3v(p,B.up)/z, z]; };
  return {P, B, cx, cy, pixR, depth:p=>dot3v(p,B.fwd)};
}
/* the projected length of a unit vector: how much of it the camera sees */
function projLen(cam,v){ const B=camBasis3(cam.theta,cam.phi); const d=dot3v(v,B.dir); return Math.sqrt(Math.max(0,1-d*d)); }
function drawSphere(ctx,S3,o){
  o=o||{};
  const cx=S3.cx, cy=S3.cy, R=S3.pixR;
  ctx.beginPath(); ctx.arc(cx,cy,R*CAM_DIST/Math.sqrt(CAM_DIST*CAM_DIST-1),0,TAU);
  ctx.fillStyle='rgba(20,26,40,0.55)'; ctx.fill(); ctx.strokeStyle='#2b3346'; ctx.lineWidth=1.2; ctx.stroke();
  /* latitude and longitude circles, split into the half behind the centre
     plane (dim) and the half in front (brighter): two strokes in all */
  const NL=o.grid===false?0:40, far=[], near=[];
  const addCircle=(fn)=>{
    let prev=null, pf=null;
    for(let i=0;i<=NL;i++){ const p=fn(i/NL), q=S3.P(p); if(!q){ prev=null; continue; }
      const isFar=S3.depth(p)>0;
      if(prev&&pf===isFar) (isFar?far:near).push(prev[0],prev[1],q[0],q[1]);
      prev=q; pf=isFar; }
  };
  if(NL){
    for(let k=1;k<=5;k++){ const th=Math.PI*k/6, s=Math.sin(th), c=Math.cos(th); addCircle(u=>[s*Math.cos(TAU*u),s*Math.sin(TAU*u),c]); }
    for(let k=0;k<6;k++){ const ph=Math.PI*k/6; addCircle(u=>[Math.sin(TAU*u)*Math.cos(ph),Math.sin(TAU*u)*Math.sin(ph),Math.cos(TAU*u)]); }
  } else {
    /* no grid: the equator only, so a small sphere still reads as 3-D */
    const ne=40; let prev=null, pf=null;
    for(let i=0;i<=ne;i++){ const p=[Math.cos(TAU*i/ne),Math.sin(TAU*i/ne),0], q=S3.P(p); const isFar=S3.depth(p)>0;
      if(prev&&pf===isFar) (isFar?far:near).push(prev[0],prev[1],q[0],q[1]); prev=q; pf=isFar; }
  }
  for(const [arr,col] of [[far,'#1d2330'],[near,'#39435b']]){
    if(!arr.length) continue;
    ctx.beginPath(); for(let i=0;i<arr.length;i+=4){ ctx.moveTo(arr[i],arr[i+1]); ctx.lineTo(arr[i+2],arr[i+3]); }
    ctx.strokeStyle=col; ctx.lineWidth=1; ctx.stroke();
  }
  /* the axes, dashed, and their names */
  ctx.beginPath();
  for(const a of [[1,0,0],[0,1,0],[0,0,1]]){ const p=S3.P([-1.25*a[0],-1.25*a[1],-1.25*a[2]]), q=S3.P([1.25*a[0],1.25*a[1],1.25*a[2]]); if(p&&q){ ctx.moveTo(p[0],p[1]); ctx.lineTo(q[0],q[1]); } }
  ctx.strokeStyle='#3d465e'; ctx.lineWidth=1.1; ctx.setLineDash([4,3]); ctx.stroke(); ctx.setLineDash([]);
  if(R>44&&o.labels!==false){
    ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillStyle=COL.dim;
    for(const [a,n] of [[[1,0,0],'x'],[[0,1,0],'y'],[[0,0,1],'z']]){ const t=S3.P([1.42*a[0],1.42*a[1],1.42*a[2]]); if(t){ ctx.fillText(n,t[0],t[1]); LABELS.push([t[0]-5,t[1]-8,t[0]+5,t[1]+8]); } }
  }
}
function drawVec(ctx,S3,r,col,lw,label,side){
  const A=S3.P([0,0,0]), Bp=S3.P(r); if(!A||!Bp) return;
  ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(Bp[0],Bp[1]); ctx.strokeStyle=col; ctx.lineWidth=lw||2.6; ctx.stroke();
  const dx=Bp[0]-A[0], dy=Bp[1]-A[1], L=Math.hypot(dx,dy)||1, ux=dx/L, uy=dy/L, hs=Math.min(11,L*0.3);
  if(L>3){ ctx.beginPath(); ctx.moveTo(Bp[0],Bp[1]); ctx.lineTo(Bp[0]-hs*ux+hs*0.45*uy,Bp[1]-hs*uy-hs*0.45*ux); ctx.lineTo(Bp[0]-hs*ux-hs*0.45*uy,Bp[1]-hs*uy+hs*0.45*ux); ctx.closePath(); ctx.fillStyle=col; ctx.fill(); }
  else mark(ctx,Bp[0],Bp[1],'o',col,3);
  if(label){ const t=plain(label), w=t.length*12*0.52, left=side==='left';
    const X=left?Bp[0]-8-w:Bp[0]+6, Y=Bp[1]-3-12;
    let clear=true; for(const o of LABELS) if(X<o[2]&&X+w>o[0]&&Y<o[3]&&Y+13.8>o[1]){ clear=false; break; }
    if(clear){ ctx.fillStyle=col; ctx.font='italic 12px Georgia, serif'; ctx.textAlign='left'; ctx.textBaseline='top'; ctx.fillText(t,X,Y); LABELS.push([X,Y,X+w,Y+13.8]); } }
}
function drawPath3(ctx,S3,pts,col,lw,dash){
  ctx.beginPath(); let started=false;
  for(const p of pts){ const q=S3.P(p); if(!q){ started=false; continue; } if(!started){ ctx.moveTo(q[0],q[1]); started=true; } else ctx.lineTo(q[0],q[1]); }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.6; if(dash) ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
}
/* the polar and azimuthal angle indicators (PhET draws both) */
function drawAngles(ctx,S3,th,ph,col){
  const a=[], b=[];
  for(let i=0;i<=24;i++){ const t=th*i/24; a.push([0.36*Math.sin(t)*Math.cos(ph),0.36*Math.sin(t)*Math.sin(ph),0.36*Math.cos(t)]); }
  for(let i=0;i<=24;i++){ const f=ph*i/24; b.push([0.30*Math.cos(f),0.30*Math.sin(f),0]); }
  drawPath3(ctx,S3,a,col,1.3); drawPath3(ctx,S3,b,col,1.3);
}
