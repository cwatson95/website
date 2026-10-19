
/* ================================================================== *
 *  drawing: the scene (PhET's four screens), shared geometry          *
 * ================================================================== */
const CAP_FONT='11.5px -apple-system, sans-serif';
const LAB_FONT='11px -apple-system, sans-serif';
const SM_FONT='10.5px -apple-system, sans-serif';
function isNarrow(W){ return W<900; }
const DRAG={what:null,dx:0,dy:0};
const SV=4, SA=5, SW=50, MIN_PX=6, STROBE=0.5;   /* px per m/s, px per m/s^2, weight in px, smallest body, strobe s */

function dot(ctx,x,y,r,fill,stroke,lw){
  ctx.beginPath(); ctx.arc(x,y,r,0,TAU);
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1.2; ctx.stroke(); }
}
function polyPx(ctx,pts,fill,stroke,lw){
  if(pts.length<2) return;
  ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); ctx.closePath();
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1; ctx.stroke(); }
}
/* an arrow in screen pixels; the head scales down on short arrows.  With a
   clip box it is cut where it leaves the box and the cut is marked with a
   bar instead of a head, so a clipped arrow cannot pass for a short one. */
function arrowPx(ctx,X,Y,dx,dy,col,lw,clip){
  const L=Math.hypot(dx,dy); if(!(L>=2.5)) return false;
  const ux=dx/L, uy=dy/L;
  if(clip){
    if(X<clip.x||X>clip.x1||Y<clip.y||Y>clip.y1) return false;
    let t=1;
    if(dx>0) t=Math.min(t,(clip.x1-X)/dx); else if(dx<0) t=Math.min(t,(clip.x-X)/dx);
    if(dy>0) t=Math.min(t,(clip.y1-Y)/dy); else if(dy<0) t=Math.min(t,(clip.y-Y)/dy);
    if(t<1){ const Xc=X+t*dx, Yc=Y+t*dy;
      ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(Xc,Yc); ctx.moveTo(Xc-4*uy,Yc+4*ux); ctx.lineTo(Xc+4*uy,Yc-4*ux);
      ctx.strokeStyle=col; ctx.lineWidth=lw||2; ctx.stroke(); return 'clipped'; }
  }
  const hh=Math.min(9,0.4*L), X1=X+dx, Y1=Y+dy;
  ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(X1-0.6*hh*ux,Y1-0.6*hh*uy);
  ctx.strokeStyle=col; ctx.lineWidth=lw||2; ctx.lineCap='round'; ctx.stroke(); ctx.lineCap='butt';
  polyPx(ctx,[[X1,Y1],[X1-hh*ux+0.45*hh*uy,Y1-hh*uy-0.45*hh*ux],[X1-hh*ux-0.45*hh*uy,Y1-hh*uy+0.45*hh*ux]],col,null);
  return true;
}
function starPts(cx,cy,R){
  const out=[];
  for(let i=0;i<10;i++){ const a=-PI/2+i*PI/5, r=i%2?R*0.42:R; out.push([cx+r*Math.cos(a),cy+r*Math.sin(a)]); }
  return out;
}
/* the drag-coefficient body, in its own frame (+x along the motion), cross-
   section radius r: an ellipsoidal streamlined body below the sphere's 0.47
   (tail 3.2 r long at C_d = 0.04), the sphere at 0.47, and above it a sphere
   with its FRONT cut flat, which reaches the flat-faced hemisphere at 1.17 */
function cdBody(cd,r){
  const pts=[];
  if(cd<=0.47){
    const L=3.2*r*(0.47-cd)/(0.47-0.04);
    for(let i=0;i<=24;i++){ const a=-PI/2+PI*i/24; pts.push([r*Math.cos(a),r*Math.sin(a)]); }
    for(let i=1;i<24;i++){ const a=PI/2+PI*i/24; pts.push([(r+L)*Math.cos(a),r*Math.sin(a)]); }
  } else {
    const c=r*Math.max(0,1-(cd-0.47)/(1.17-0.47)), a0=Math.acos(c/r);
    for(let i=0;i<=40;i++){ const a=a0+(TAU-2*a0)*i/40; pts.push([r*Math.cos(a),r*Math.sin(a)]); }
  }
  return pts;
}
function cdWord(cd){ return cd<0.3?'streamlined':(cd<0.45?'a rounded body':(cd<=0.49?'a sphere':(cd<0.8?'a sphere cut flat in front':'a flat-faced cup'))); }
function bodyPoly(shape,cd,R,ang){         /* body outline in pixels about (0,0), rotated to the motion */
  let pts;
  if(shape==='spheroid'){ pts=[]; for(let i=0;i<32;i++){ const a=TAU*i/32; pts.push([1.6*R*Math.cos(a),R*Math.sin(a)]); } }
  else if(shape==='shell'){ pts=[[2.2*R,0],[1.2*R,-R],[-1.4*R,-R],[-1.4*R,R],[1.2*R,R]]; }
  else if(shape==='box'){ pts=[[-1.1*R,-0.7*R],[1.1*R,-0.7*R],[1.1*R,0.7*R],[-1.1*R,0.7*R]]; ang=0; }
  else if(shape==='cd') pts=cdBody(cd,R);
  else { pts=[]; for(let i=0;i<24;i++){ const a=TAU*i/24; pts.push([R*Math.cos(a),R*Math.sin(a)]); } }
  const c=Math.cos(ang), s=Math.sin(ang);
  return pts.map(p=>[p[0]*c-p[1]*s, -(p[0]*s+p[1]*c)]);   /* world y up -> screen y down */
}

/* ---- the scene geometry: ONE function serves the drawing and the pointer ---- */
function sceneCaption(M,s){
  const P=M.P, st=ST, v=M.view, bits=[];
  bits.push('Scale 1 m = '+fmt(s,1)+' px (zoom ×'+fmt(st.zoom,2)+'), both axes; dots every 0.1 s, the large ones every second.');
  const dpx=P.d*s;
  if(dpx<MIN_PX) bits.push('The '+(isScene(v)&&(v==='intro'||v==='lab')?P.o.name:'sphere')+' ('+sigf(P.d*100,3)+' cm) is drawn '+MIN_PX+' px across, ×'+fmt(MIN_PX/dpx,1)+' its size.');
  if(vecOn(v)) bits.push('Arrows: velocity '+SV+' px per m/s, acceleration '+SA+' px per m/s², forces with the weight mg drawn '+SW+' px.');
  if(M.E.air&&(st.vacRef||v==='drag')) bits.push('Orange dashed: the same shot without air'+(v==='drag'?'; green dashed: this shot with it, before you fire':'')+'.');
  if(v==='intro') bits.push('Target '+TARGET_W+' m wide: three stars within 0.5 m, two within 1 m, one within 1.5 m.');
  return bits.join(' ');
}
function sceneGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+4;
  const full=sceneCaption(M,sceneScale(W,ST.zoom));
  const fit=fitCaption(ctx,W,H,full,'Scale 1 m = '+fmt(sceneScale(W,ST.zoom),1)+' px; dots every 0.1 s.',W-40,top+260);
  const b=box(14,top,W-28,fit.capY-12-top);
  const s=sceneScale(W,ST.zoom), X0=b.x+92, Y0=b.y1-28;
  const map={s,X0,Y0,X:x=>X0+s*x,Y:y=>Y0-s*y,wx:X=>(X-X0)/s,wy:Y=>(Y0-Y)/s};
  const L=M.L, th=L.th*DEG, Lb=clamp(2.0*s,36,72), wb=clamp(0.45*s,10,18);
  const piv=[map.X(0),map.Y(L.h)], muz=[piv[0]+Lb*Math.cos(th),piv[1]-Lb*Math.sin(th)];
  const pedW=Math.max(16,1.2*s);
  return {narrow,b,map,fit,piv,muz,Lb,wb,pedW,capY:fit.capY,capTxt:fit.txt,capW:fit.capW};
}
function sceneScale(W,zoom){ return (W-28-92-10)/36*zoom; }
function vecOn(v){
  const st=ST;
  if(v==='intro') return st.i_vt||st.i_vc||st.i_at||st.i_ac;
  if(v==='vectors') return st.v_vel||st.v_acc||st.v_frc;
  if(v==='drag') return st.d_vel||st.d_frc;
  return false;
}
/* which vectors a view shows: {vel, acc, frc, comp} */
function vecSet(v){
  const st=ST;
  if(v==='intro') return {velT:st.i_vt,velC:st.i_vc,accT:st.i_at,accC:st.i_ac,frcT:false,frcC:false};
  if(v==='vectors'){ const c=st.v_mode==='components';
    return {velT:st.v_vel&&!c,velC:st.v_vel&&c,accT:st.v_acc&&!c,accC:st.v_acc&&c,frcT:st.v_frc&&!c,frcC:st.v_frc&&c}; }
  if(v==='drag'){ const c=st.d_mode==='components';
    return {velT:st.d_vel&&!c,velC:st.d_vel&&c,accT:false,accC:false,frcT:st.d_frc&&!c,frcC:st.d_frc&&c}; }
  return {velT:false,velC:false,accT:false,accC:false,frcT:false,frcC:false};
}
/* the vectors at one state: velocity v, acceleration a = (-k|v|vx, -g-k|v|vy),
   gravity (0,-mg) and drag -mk|v|v, in pixels (screen y down) */
function drawVectors(ctx,X,Y,S,g,k,m,VS,dim,labels,W,H,clip){
  const sp=Math.sqrt(S.vx*S.vx+S.vy*S.vy), ax=-k*sp*S.vx, ay=-g-k*sp*S.vy, sf=SW/(m*g);
  const fdx=-m*k*sp*S.vx, fdy=-m*k*sp*S.vy;
  const a=dim?0.55:1, cv=dim?mix(COL.sky,COL.pos,a):COL.pos, ca=dim?mix(COL.sky,COL.live,a):COL.live, cf=dim?mix(COL.sky,COL.force,a):COL.force;
  const lw=dim?1.4:2.2, XF=X+5;       /* forces start 5 px to the side: mg and a_y are colinear */
  const A=(x0,y0,ddx,ddy,col)=>arrowPx(ctx,x0,y0,ddx,ddy,col,lw,clip);
  if(VS.velT){ A(X,Y,SV*S.vx,-SV*S.vy,cv); if(labels) lab(ctx,W,H,X+SV*S.vx+5,Y-SV*S.vy,'v',cv,SM_FONT); }
  if(VS.velC){ A(X,Y,SV*S.vx,0,cv); A(X,Y,0,-SV*S.vy,cv);
    if(labels){ lab(ctx,W,H,X+SV*S.vx+5,Y,'vx',cv,SM_FONT); lab(ctx,W,H,X+5,Y-SV*S.vy,'vy',cv,SM_FONT); } }
  if(VS.accT){ A(X,Y,SA*ax,-SA*ay,ca); if(labels) lab(ctx,W,H,X+SA*ax-8,Y-SA*ay+6,'a',ca,SM_FONT,'right'); }
  if(VS.accC){ A(X,Y,SA*ax,0,ca); A(X,Y,0,-SA*ay,ca);
    if(labels){ lab(ctx,W,H,X+SA*ax-10,Y+10,'ax',ca,SM_FONT); lab(ctx,W,H,X-6,Y-SA*ay,'ay',ca,SM_FONT,'right'); } }
  if(VS.frcT){ A(XF,Y,0,SW,cf); A(XF,Y,sf*fdx,-sf*fdy,cf);
    if(labels){ lab(ctx,W,H,XF+6,Y+SW,'mg',cf,SM_FONT); if(k>0) lab(ctx,W,H,XF+sf*fdx-6,Y-sf*fdy-8,'Fd',cf,SM_FONT,'right'); } }
  if(VS.frcC){ A(XF,Y,0,SW,cf); A(XF,Y,sf*fdx,0,cf); A(XF,Y,0,-sf*fdy,cf);
    if(labels){ lab(ctx,W,H,XF+6,Y+SW,'mg',cf,SM_FONT); if(k>0) lab(ctx,W,H,XF+sf*fdx-6,Y-10,'Fdx',cf,SM_FONT,'right'); } }
  return {ax,ay,fdx,fdy};
}
/* a projectile body at a state (true size, never under MIN_PX across) */
function drawBody(ctx,G,P,S,landed){
  const map=G.map, R=Math.max(MIN_PX,P.d*map.s)/2;
  const ang=Math.atan2(S.vy,S.vx), X=map.X(S.x), Y=landed?map.Y(0)-R*(P.o.shape==='box'?0.7:1):map.Y(S.y);
  const pts=bodyPoly(P.o.shape,P.cd,R,landed?0:ang).map(p=>[X+p[0],Y+p[1]]);
  polyPx(ctx,pts,P.o.fill,'#c9ced8',1);
  return [X,Y];
}
/* a path drawn up to time tMax, clipped to the scene box in world coordinates */
function drawPath(ctx,G,F,tMax,col,lw,dash){
  const b=G.b, m=G.map, n=F.t.length;
  let iEnd=nodeBefore(F,tMax);
  const step=Math.max(1,Math.ceil(iEnd/900)), xs=[], ys=[];
  for(let i=0;i<=iEnd;i+=step){ xs.push(F.x[i]); ys.push(F.y[i]); }
  if(xs.length&&(iEnd%step)){ xs.push(F.x[iEnd]); ys.push(F.y[iEnd]); }
  if(tMax<F.t[n-1]){ const S=stateAt(F,tMax); xs.push(S.x); ys.push(S.y); }
  polyline(ctx,b,xs,ys,m.wx(b.x),m.wx(b.x1),m.wy(b.y1),m.wy(b.y),col,lw,dash);
}
function drawDots(ctx,G,F,tMax,col){
  const m=G.map, b=G.b;
  for(const big of [false,true]){
    ctx.beginPath(); let any=false;
    F.dots.forEach((i,j)=>{
      if(F.t[i]>tMax+1e-12) return;
      const k=Math.round(F.t[i]/DOT); if((k%BIG_DOT_EVERY===0)!==big) return;
      const X=m.X(F.x[i]), Y=m.Y(F.y[i]); if(X<b.x||X>b.x1||Y<b.y||Y>b.y1) return;
      const r=big?3.3:1.65; ctx.moveTo(X+r,Y); ctx.arc(X,Y,r,0,TAU); any=true;
    });
    if(any){ ctx.fillStyle=mix(col,'#ffffff',0.6); ctx.fill(); }
  }
}

function drawScene(ctx,W,H,M){
  const G=sceneGeo(ctx,W,H,M), b=G.b, map=G.map, v=M.view, st=ST, sc=M.sc, L=M.L, E=M.E;
  if(!G.narrow) LABELS.push([W-RO_W-26,0,W,480]);        /* the floating readout */
  /* the ground, the target lying on it (flattened, at most 7 px), then the ruler over both */
  ctx.fillStyle=COL.ground; ctx.fillRect(b.x,G.map.Y0,b.w,b.y1-G.map.Y0);
  ctx.strokeStyle=COL.groundLine; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(b.x,map.Y0+0.5); ctx.lineTo(b.x1,map.Y0+0.5); ctx.stroke();
  const tg=M.tgt, Xc=map.X(tg), ry=clamp(0.3*map.s,3,7);
  for(const [f,c] of [[1,COL.ref],[2/3,'#2a1a10'],[1/3,COL.ref]]){ const rx=f*TARGET_W/2*map.s, pts=[];
    for(let i=0;i<36;i++){ const a=TAU*i/36; pts.push([Xc+rx*Math.cos(a),map.Y0-ry*Math.sin(a)*f]); }
    polyPx(ctx,pts,c,null); }
  const x0=Math.max(0,map.wx(b.x)), x1=map.wx(b.x1-24), xt=ticksFor(0,x1,Math.max(3,Math.floor((b.x1-map.X0)/90)));
  const xf=tickFmt(xt);
  ctx.strokeStyle=COL.groundLine; ctx.beginPath();
  for(const t of xt){ if(t<x0-1e-9) continue; const X=map.X(t); ctx.moveTo(X,map.Y0); ctx.lineTo(X,map.Y0+5); }
  ctx.stroke();
  for(const t of xt){ if(t<x0-1e-9) continue; lab(ctx,W,H,map.X(t),map.Y0+14,xf(t)+(t===xt[xt.length-1]?' m':''),'#6f7789',SM_FONT,'center'); }
  /* the analytic references */
  if(E.air&&(st.vacRef||v==='drag')){ const VP=vacuumPath(L.h,L.th,L.v0,E.g,160);
    polyline(ctx,b,VP.xs,VP.ys,map.wx(b.x),map.wx(b.x1),map.wy(b.y1),map.wy(b.y),COL.ref,1.3,[6,5]); }
  if(v==='drag') drawPath(ctx,G,M.pred,M.pred.T,rgba(COL.pos,0.7),1.3,[3,4]);
  /* the drag body, drawn large in the free column left of the cannon */
  if(v==='drag'){ const r=12, tail=M.P.cd<=0.47?3.2*r*(0.47-M.P.cd)/(0.47-0.04):0, cx=b.x+8+r+tail, cy=b.y+44;
    polyPx(ctx,cdBody(M.P.cd,r).map(p=>[cx+p[0],cy-p[1]]),SCREEN_OBJ.fill,'#c9ced8',1);
    arrowPx(ctx,b.x+52,cy+26,-22,0,COL.dim,1.2);
    lab(ctx,W,H,b.x+8,cy+26,'air',COL.dim,SM_FONT,'left');
    lab(ctx,W,H,b.x+8,cy+44,'Cd '+fmt(M.P.cd,2),COL.force,SM_FONT,'left'); }
  /* the strobe (the vectors view): the vectors every 0.5 s along this shot */
  if(v==='vectors'&&st.v_strobe&&M.pred.T>0){
    drawPath(ctx,G,M.pred,M.pred.T,rgba(COL.dim,0.55),1,[2,4]);
    const VS=vecSet(v);
    for(let t=STROBE;t<=M.pred.T+1e-9;t+=STROBE){ const S=stateAt(M.pred,t), X=map.X(S.x), Y=map.Y(S.y);
      if(X<b.x||X>b.x1||Y<b.y||Y>b.y1) continue;
      dot(ctx,X,Y,2.4,rgba(COL.force,0.6),null); drawVectors(ctx,X,Y,S,E.g,E.k,M.P.m,VS,true,false,W,H,b); }
  }
  /* the fired paths, oldest faintest */
  const n=sc.trajs.length;
  sc.trajs.forEach((tr,j)=>{
    const rank=n-1-j, a=[1,0.62,0.45,0.33,0.24][rank]||0.2, col=mix(COL.sky,COL.pos,a), lim=shownUntil(tr,sc.t);
    drawPath(ctx,G,tr.F,lim,col,rank===0?2:1.4);
    drawDots(ctx,G,tr.F,lim,col);
    if(rank===0&&tr.F.apex&&tr.F.apex.t<=lim){ const X=map.X(tr.F.apex.x), Y=map.Y(tr.F.apex.y);
      if(X>b.x&&X<b.x1&&Y>b.y&&Y<b.y1){ dot(ctx,X,Y,4,null,COL.pos,1.4); lab(ctx,W,H,X+8,Y-10,'apex '+sigf(tr.F.apex.y,3)+' m',COL.pos,SM_FONT); } }
    if(rank===0&&lim>=tr.F.T&&tr.F.T>0){ const X=map.X(tr.F.R); if(X>b.x&&X<b.x1) lab(ctx,W,H,X,map.Y0-16,'R = '+sigf(tr.F.R,4)+' m',COL.pos,SM_FONT,'center'); }
  });
  /* the target's label, and the stars of the last landing */
  { lab(ctx,W,H,Xc,map.Y0+28,'target '+fmt(tg,1)+' m',COL.ref,SM_FONT,'center');
    if(sc.score&&sc.score.stars>0) for(let i=0;i<3;i++) polyPx(ctx,starPts(Xc+(i-1)*20,map.Y0-ry-22,8),i<sc.score.stars?COL.star:null,COL.star,1.2);
  }
  /* the cannon: pedestal, body, barrel */
  { const pv=G.piv, pw=G.pedW;
    ctx.fillStyle=COL.cannon; ctx.fillRect(pv[0]-pw/2,pv[1],pw,map.Y0-pv[1]);
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.strokeRect(pv[0]-pw/2+0.5,pv[1]+0.5,pw-1,Math.max(0,map.Y0-pv[1]-1));
    const th=L.th*DEG, c=Math.cos(th), s=Math.sin(th), hw=G.wb/2;
    /* the barrel: pivot to muzzle along (cos th, -sin th) on screen, half-width hw across it */
    polyPx(ctx,[[pv[0]+hw*s,pv[1]+hw*c],[G.muz[0]+hw*s,G.muz[1]+hw*c],[G.muz[0]-hw*s,G.muz[1]-hw*c],[pv[0]-hw*s,pv[1]-hw*c]],
      COL.cannon2,COL.struct,1.2);
    dot(ctx,pv[0],pv[1],Math.max(8,0.35*map.s),COL.cannon,COL.struct,1.2);
    lab(ctx,W,H,pv[0]-pw/2-6,pv[1],fmt(L.h,1)+' m','#8b93a6',SM_FONT,'right');
    lab(ctx,W,H,G.muz[0]+10*c,G.muz[1]-10*s-2,fmt(L.th,0)+'°',COL.struct,SM_FONT,c>=0?'left':'right');
  }
  /* the projectiles: landed ones rest on the ground, flying ones carry vectors */
  const VS=vecSet(v); let labelled=false;
  for(let j=n-1;j>=0;j--){ const tr=sc.trajs[j];
    for(const p of tr.projs){
      const age=sc.t-p.t0, S=stateAt(tr.F,Math.min(age,tr.F.T));
      if(p.landed||age>=tr.F.T){ drawBody(ctx,G,tr.P,{x:tr.F.R,y:0,vx:1,vy:0},true); continue; }
      const XY=drawBody(ctx,G,tr.P,S,false);
      drawVectors(ctx,XY[0],XY[1],S,tr.E.g,tr.E.k,tr.P.m,VS,false,!labelled,W,H,b); labelled=true;
    } }
  /* the tools */
  if(st.tape){ const T=sc.tape, A=[map.X(T.x0),map.Y(T.y0)], B=[map.X(T.x1),map.Y(T.y1)];
    ctx.strokeStyle=COL.tape; ctx.lineWidth=2.4; ctx.beginPath(); ctx.moveTo(A[0],A[1]); ctx.lineTo(B[0],B[1]); ctx.stroke();
    dot(ctx,A[0],A[1],6,COL.tape,'#fff',1); dot(ctx,B[0],B[1],4.5,'#fff',COL.tape,1.6);
    lab(ctx,W,H,(A[0]+B[0])/2,(A[1]+B[1])/2-12,fmt(tapeLength(v),2)+' m',COL.tape,LAB_FONT,'center'); }
  if(st.probe){ const pr=sc.probe, X=map.X(pr.x), Y=map.Y(pr.y);
    dot(ctx,X,Y,10,null,COL.struct,1.6);
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(X-15,Y); ctx.lineTo(X-4,Y); ctx.moveTo(X+4,Y); ctx.lineTo(X+15,Y);
    ctx.moveTo(X,Y-15); ctx.lineTo(X,Y-4); ctx.moveTo(X,Y+4); ctx.lineTo(X,Y+15); ctx.stroke();
    const R=M.probe, txt=R?'t '+sigf(R.t,3)+' s · x '+sigf(R.x,3)+' m · y '+sigf(R.y,3)+' m':'probe: no dot here';
    ctx.font=SM_FONT; const w=ctx.measureText(txt).width+10;
    const bx=clamp(X+16,2,W-w-2), by=clamp(Y-34,2,H-20);
    if(labFits([bx,by,bx+w,by+18])){ ctx.fillStyle='rgba(10,12,18,.85)'; ctx.fillRect(bx,by,w,18); frame(ctx,box(bx,by,w,18),COL.struct);
      ctx.fillStyle=R?COL.force:COL.dim; ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillText(txt,bx+5,by+9); LABELS.push([bx,by,bx+w,by+18]); } }
  caption(ctx,20,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
  return G;
}
