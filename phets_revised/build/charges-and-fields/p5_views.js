
/* ================================================================== *
 *  view: the landscape — V(x, y) as a height surface                  *
 * ================================================================== */
function landCap(st){
  return 'The potential V(x, y) over the plane drawn as a height: '+fmt(LAND_HZ,2)+' m of height for every '+fmt(st.vcap,0)+' V, so the peaks over the positive '
    +'charges and the wells under the negative ones are clipped flat at ±'+fmt(st.vcap,0)+' V (a point charge’s 1/r would climb forever). The field is minus the '
    +'slope: E points straight downhill and is strongest where the surface is steepest. The cyan loops are the equipotentials plotted on the plane, lifted '
    +'to their own height and drawn over the surface — its level cuts. Drag to orbit, scroll to zoom.';
}
const LAND_CAP_SHORT='V(x, y) as height, clipped at the cap; E points straight downhill. Drag to orbit, scroll to zoom.';
function landCamera(b,st){ return boxCamera(b,st.camTheta,st.camPhi,landFitDist(b,st.camTheta,st.camPhi)/st.camZoom,[0,0,0]); }
function inPanel(b,q){ return !!q&&q.x>=b.x&&q.x<=b.x1&&q.y>=b.y&&q.y<=b.y1; }
function landQuadColour(zm,sh){ return shade(mix(COL.zero,zm>=0?COL.pos:COL.neg,Math.min(1,Math.abs(zm)/LAND_HZ)),sh); }
function drawLand(ctx,W,H,M){
  const st=M.st, Ld=M.land, L=stageLayout(ctx,W,H,landCap(st),LAND_CAP_SHORT,0,0,0), b=L.main;
  frame(ctx,b,COL.edge);
  const C=landCamera(b,st), nx=Ld.nx, ny=Ld.ny, n1=nx+1, dx=(PLANE.x1-PLANE.x0)/nx, dy=(PLANE.y1-PLANE.y0)/ny;
  const gx=i=>PLANE.x0+dx*i, gy=j=>PLANE.y0+dy*j;
  const P=new Array(n1*(ny+1));
  for(let j=0;j<=ny;j++) for(let i=0;i<=nx;i++) P[j*n1+i]=C.P([gx(i),gy(j),Ld.z[j*n1+i]]);
  /* the quads, the level-cut segments and the charge markers are painted in ONE
     depth sort, so the near rim of a well hides the negative charge at its bottom
     and a peak hides the far side of a loop; segments and markers are biased 5 cm
     toward the eye so they do not fight the quad they lie on */
  const light=v3.norm([-0.4,0.5,0.75]), quads=[];
  for(let j=0;j<ny;j++) for(let i=0;i<nx;i++){
    const a=P[j*n1+i], bq=P[j*n1+i+1], c=P[(j+1)*n1+i+1], d=P[(j+1)*n1+i];
    /* a quad with any corner off the panel is dropped whole, never clamped
       (Known-bad: a clamped mesh paints a false wall); zoomed in, the surface is cropped */
    if(!inPanel(b,a)||!inPanel(b,bq)||!inPanel(b,c)||!inPanel(b,d)) continue;
    const z00=Ld.z[j*n1+i], z10=Ld.z[j*n1+i+1], z01=Ld.z[(j+1)*n1+i], z11=Ld.z[(j+1)*n1+i+1];
    const nrm=v3.norm([-(z10-z00+z11-z01)/(2*dx),-(z01-z00+z11-z10)/(2*dy),1]);
    quads.push({z:(a.z+bq.z+c.z+d.z)/4,pts:[a,bq,c,d],col:landQuadColour((z00+z10+z01+z11)/4,0.55+0.45*Math.max(0,v3.dot(nrm,light)))});
  }
  const items=quads;
  /* the plotted equipotentials at their own height: the level cuts */
  if(st.landEq) for(const E of M.eq){
    if(!E.ok||!(Math.abs(E.V0)<st.vcap)) continue;
    const z=landHeight(E.V0,st.vcap), pts=E.pts.filter(p=>p[0]>=PLANE.x0&&p[0]<=PLANE.x1&&p[1]>=PLANE.y0&&p[1]<=PLANE.y1);
    if(E.closed&&pts.length===E.pts.length) pts.push(pts[0]);
    let prev=null;
    for(const p of pts){ const q=C.P([p[0],p[1],z]); if(!inPanel(b,q)){ prev=null; continue; }
      if(prev&&Math.hypot(q.x-prev.x,q.y-prev.y)<40) items.push({seg:true,z:(q.z+prev.z)/2-0.05,a:prev,b2:q}); prev=q; }
  }
  /* the charges on their clipped plateaus, at the bottom of their wells */
  for(const c of M.ch){ const q=C.P([c.x,c.y,landHeight(c.q>0?Infinity:-Infinity,st.vcap)]); if(inPanel(b,q)) items.push({mark:true,z:q.z-0.05,x:q.x,y:q.y,q:c.q}); }
  items.sort((p,q)=>q.z-p.z);
  for(const it of items){
    if(it.seg){ ctx.beginPath(); ctx.moveTo(it.a.x,it.a.y); ctx.lineTo(it.b2.x,it.b2.y); ctx.strokeStyle=COL.struct; ctx.lineWidth=1.8; ctx.lineCap='round'; ctx.stroke(); ctx.lineCap='butt'; continue; }
    if(it.mark){ chargeGlyph(ctx,it.x,it.y,4.5,it.q); continue; }
    /* a quad: opaque and widened 0.4 px about its centroid, no seams (Known-bad) */
    const q=it, cx=(q.pts[0].x+q.pts[1].x+q.pts[2].x+q.pts[3].x)/4, cy=(q.pts[0].y+q.pts[1].y+q.pts[2].y+q.pts[3].y)/4;
    ctx.beginPath();
    q.pts.forEach((p,k)=>{ const ex=p.x-cx, ey=p.y-cy, e=Math.hypot(ex,ey)||1, X=p.x+0.4*ex/e, Y=p.y+0.4*ey/e; if(k) ctx.lineTo(X,Y); else ctx.moveTo(X,Y); });
    ctx.closePath(); ctx.fillStyle=q.col; ctx.fill();
  }
  /* the height scale: a vertical bar at the far corner, ticks in volts */
  const corner=[PLANE.x1,PLANE.y1], bot=C.P([corner[0],corner[1],-LAND_HZ]), top=C.P([corner[0],corner[1],LAND_HZ]);
  if(inPanel(b,bot)&&inPanel(b,top)){
    /* foreshortened (seen from above) the bar is short: then only its top is named */
    const longBar=Math.hypot(top.x-bot.x,top.y-bot.y)>=70;
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(bot.x,bot.y); ctx.lineTo(top.x,top.y); ctx.stroke();
    for(const f of (longBar?[-1,-0.5,0,0.5,1]:[1])){ const q=C.P([corner[0],corner[1],f*LAND_HZ]); if(!q) continue;
      ctx.beginPath(); ctx.moveTo(q.x-4,q.y); ctx.lineTo(q.x+4,q.y); ctx.stroke();
      lab(ctx,W,H,q.x+7,q.y,(f>0?'+':f<0?'−':'')+fmt(Math.abs(f*st.vcap),0)+' V',COL.struct,SM_FONT,'left'); }
  }
  /* the plane's outline at V = 0, and the axes named at their far ends */
  const o=[[PLANE.x0,PLANE.y0],[PLANE.x1,PLANE.y0],[PLANE.x1,PLANE.y1],[PLANE.x0,PLANE.y1],[PLANE.x0,PLANE.y0]].map(p=>C.P([p[0],p[1],0]));
  if(o.every(q=>inPanel(b,q))){ ctx.beginPath(); o.forEach((q,k)=>{ if(k) ctx.lineTo(q.x,q.y); else ctx.moveTo(q.x,q.y); }); ctx.strokeStyle=rgba(COL.dim,0.45); ctx.lineWidth=1; ctx.setLineDash([4,4]); ctx.stroke(); ctx.setLineDash([]); }
  const ex=C.P([PLANE.x1+0.35,PLANE.y0,0]), ey=C.P([PLANE.x0,PLANE.y1+0.35,0]);
  if(inPanel(b,ex)) lab(ctx,W,H,ex.x,ex.y,'x',COL.dim,SM_FONT,'center'); if(inPanel(b,ey)) lab(ctx,W,H,ey.x,ey.y,'y',COL.dim,SM_FONT,'center');
  lab(ctx,W,H,b.x+6,b.y+8,'V(x, y) as height — '+fmt(LAND_HZ,2)+' m = '+fmt(st.vcap,0)+' V, clipped at ±'+fmt(st.vcap,0)+' V ('+Ld.clipped+' of '+(n1*(ny+1))+' vertices)','#aeb6c6','italic 13px Georgia, serif','left','top');
  if(!M.n) lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.2,'no charges: the landscape is flat',COL.dim,LAB_FONT,'center');
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  view: superposition — the field at a probe as a vector sum          *
 * ================================================================== */
const SUP_CAP_FULL='The probe (drag it, or drag the charges) sits in the field of every charge at once. From the probe, each charge’s own field is drawn head '
  +'to tail — green for a positive charge, pointing away from it, magenta for a negative one, pointing toward it — and the chain closes on the total field, in '
  +'white. All the arrows share one scale, printed on the plane. Below: the potential at the probe built up charge by charge; the terms are signed numbers, so '
  +'the running total rises and falls and ends at V.';
const SUP_CAP_SHORT='Each charge’s field at the probe, head to tail, closes on the total (white). Below: V built up term by term.';
function superGeo(ctx,W,H){
  const L=stageLayout(ctx,W,H,SUP_CAP_FULL,SUP_CAP_SHORT,1,0.30,1);
  const map=worldFitUp(L.main,{xmin:PLANE.x0,xmax:PLANE.x1,ymin:PLANE.y0,ymax:PLANE.y1},0);
  const pb=box(map.X(PLANE.x0),map.Y(PLANE.y1),(PLANE.x1-PLANE.x0)*map.s,(PLANE.y1-PLANE.y0)*map.s);
  return {L,map,pb};
}
/* the one arrow scale (m of plane per V/m): the longest thing in the chain (a
   single term, a partial sum or the total) is drawn 1.4 m long */
function superScale(C,P){
  let sx=0, sy=0, mx=Math.hypot(P.ex,P.ey);
  for(const c of C){ sx+=c.ex; sy+=c.ey; mx=Math.max(mx,Math.hypot(sx,sy),Math.hypot(c.ex,c.ey)); }
  return (isFinite(mx)&&mx>0)?1.4/mx:null;
}
function drawSuper(ctx,W,H,M){
  const st=M.st, G=superGeo(ctx,W,H), L=G.L, map=G.map, pb=G.pb, C=M.contrib, P=M.probe, pr=[st.probe.x,st.probe.y];
  ctx.fillStyle=COL.plane; ctx.fillRect(pb.x,pb.y,pb.w,pb.h);
  ctx.strokeStyle=COL.grid; ctx.lineWidth=1; ctx.beginPath();
  for(let i=1;i<16;i++){ const X=map.X(PLANE.x0+i*0.5); ctx.moveTo(X,pb.y); ctx.lineTo(X,pb.y1); }
  for(let j=1;j<10;j++){ const Y=map.Y(PLANE.y0+j*0.5); ctx.moveTo(pb.x,Y); ctx.lineTo(pb.x1,Y); }
  ctx.stroke(); frame(ctx,pb,'#2a3346');
  /* the line from each charge to the probe: the direction of its field there */
  for(const c of C){ const q=M.ch[c.i]; ctx.beginPath(); ctx.moveTo(map.X(q.x),map.Y(q.y)); ctx.lineTo(map.X(pr[0]),map.Y(pr[1]));
    ctx.strokeStyle=rgba(qCol(c.q),0.28); ctx.lineWidth=1; ctx.setLineDash([3,4]); ctx.stroke(); ctx.setLineDash([]); }
  drawCharges(ctx,map,M.ch);
  const sc=superScale(C,P);
  /* the chain may use the whole panel, not just the plane (at a corner of the
     plane the total pointed off it and vanished) */
  const vw={x0:map.wx(L.main.x),x1:map.wx(L.main.x1),y0:map.wy(L.main.y1),y1:map.wy(L.main.y)};
  if(!M.n) lab(ctx,W,H,pb.x+pb.w/2,pb.y+pb.h*0.3,'no charges: nothing to superpose',COL.dim,LAB_FONT,'center');
  else if(sc===null) lab(ctx,W,H,pb.x+pb.w/2,pb.y+pb.h*0.12,'the probe sits on a charge: its field there is unbounded',COL.ref,LAB_FONT,'center');
  else {
    let x=pr[0], y=pr[1];
    for(const c of C){ const v=[c.ex*sc,c.ey*sc]; arrowWorldClip(ctx,map,[x,y],v,qCol(c.q),1.5,vw); x+=v[0]; y+=v[1]; }
    arrowWorldClip(ctx,map,pr,[P.ex*sc,P.ey*sc],COL.live,2.8,vw);
    lab(ctx,W,H,pb.x1-6,pb.y1-10,'arrows: 1 m on the plane = '+sigf(1/sc,3)+' V/m','#aeb6c6',SM_FONT,'right');
    const tip=[pr[0]+P.ex*sc,pr[1]+P.ey*sc];
    if(tip[0]>=vw.x0&&tip[0]<=vw.x1&&tip[1]>=vw.y0&&tip[1]<=vw.y1) labPad(ctx,W,H,map.X(tip[0])+8,map.Y(tip[1])-8,'E = '+sigf(P.mag,3)+' V/m',COL.live,LAB_FONT,'left');
    else labPad(ctx,W,H,pb.x+pb.w/2,pb.y+14,'the total points off the panel: E = '+sigf(P.mag,3)+' V/m at '+fmt(P.ang,1)+'°',COL.live,SM_FONT,'center');
  }
  /* the probe */
  const X=map.X(pr[0]), Y=map.Y(pr[1]);
  ctx.beginPath(); ctx.arc(X,Y,8,0,TAU); ctx.strokeStyle=COL.live; ctx.lineWidth=1.6; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(X-12,Y); ctx.lineTo(X+12,Y); ctx.moveTo(X,Y-12); ctx.lineTo(X,Y+12); ctx.lineWidth=1; ctx.stroke();
  lab(ctx,W,H,X+12,Y+14,'P',COL.live,SM_FONT,'left');
  /* the potential, term by term: a signed waterfall (Known-bad: a stacked bar
     cannot draw a signed sum) */
  if(L.bottom.length){
    const bb=L.bottom[0], n=C.length;
    const ser=superWaterfall(C);
    if(!n||!ser.finite){ axesR(ctx,bb,0,1,-1,1,{title:titleFor(bb,'the potential at P, one charge at a time','V at P, term by term'),ylab:'volts',xticks:[],ny:3});
      lab(ctx,W,H,bb.x+bb.w/2,bb.y+bb.h/2,n?'the probe sits on a charge: V is unbounded':'no charges',COL.dim,SM_FONT,'center'); }
    else {
      const lo=ser.lo-0.08*(ser.hi-ser.lo||1), hi=ser.hi+0.08*(ser.hi-ser.lo||1), every=Math.max(1,Math.ceil((n+1)*18/bb.w));
      const xt=[]; for(let k=0;k<=n;k++) if(k%every===0||k===n) xt.push(k+0.5);
      axesR(ctx,bb,0,n+1,lo,hi,{title:titleFor(bb,'the potential at P, one charge at a time: running total, then V','V at P, term by term'),xlab:'charge number (last slot: the total V)',ylab:'volts',
        xticks:xt,xfmt:v=>{ const k=Math.round(v-0.5); return k===n?'V':String(k+1); },yticks:sparseTicks(lo,hi,bb.h),yfmt:v=>sigf(v,3)});
      const Xs=t=>bb.x+bb.w*t/(n+1), Yv=v=>bb.y1-bb.h*(v-lo)/(hi-lo);
      for(let k=0;k<n;k++){
        const a=ser.S[k], c=ser.S[k+1], x0=Xs(k+0.18), x1=Xs(k+0.82);
        ctx.fillStyle=rgba(qCol(C[k].q),0.8); ctx.fillRect(x0,Math.min(Yv(a),Yv(c)),x1-x0,Math.max(1,Math.abs(Yv(c)-Yv(a))));
        /* the leader to the next slot (the last one runs to the total's bar, which ends at the same height) */
        ctx.strokeStyle='#3a4152'; ctx.lineWidth=1; ctx.setLineDash([2,2]); ctx.beginPath(); ctx.moveTo(x1,Yv(c)); ctx.lineTo(Xs(k+1.18),Yv(c)); ctx.stroke(); ctx.setLineDash([]);
      }
      const xv0=Xs(n+0.18), xv1=Xs(n+0.82);
      ctx.fillStyle=COL.live; ctx.fillRect(xv0,Math.min(Yv(0),Yv(ser.total)),xv1-xv0,Math.max(1,Math.abs(Yv(ser.total)-Yv(0))));
      polyline(ctx,bb,[0,n+1],[0,0],0,n+1,lo,hi,'#3a4152',1,[2,3]);
      lab(ctx,W,H,Math.min(xv1+4,bb.x1-60),Yv(ser.total)+(ser.total>=0?-9:9),'V = '+sigf(ser.total,3)+' V',COL.live,SM_FONT,'left');
    }
  }
  drawCaption(ctx,L);
}
/* the running sums of the potential terms (a model function: the waterfall's
   numbers are assertable, Known-bad "a number computed inside a draw call") */
function superWaterfall(C){
  const S=[0]; let lo=0, hi=0, finite=true;
  for(const c of C){ const v=S[S.length-1]+c.V; S.push(v); if(!isFinite(v)) finite=false; lo=Math.min(lo,v); hi=Math.max(hi,v); }
  return {S,total:S[S.length-1],lo,hi,finite};
}

/* ================================================================== *
 *  view: the far field — the multipole expansion along a ray          *
 * ================================================================== */
const FAR_CAP_FULL='The potential along a ray from the expansion centre (the centre of charge, or the middle of a neutral set), against distance on log axes. '
  +'Beyond the farthest charge the exact sum (green) is a series in 1/r whose first non-zero term (orange) takes over far away: a net charge falls as 1/r, '
  +'a neutral pair as 1/r², a square of four as 1/r³ — the slope of the line. Below left, the charges and the ray; below right, r^(ℓ+1) V(r) divided by the '
  +'exact coefficient c_ℓ settling on 1, the limit the readout also takes numerically. Turn the ray with the slider.';
const FAR_CAP_SHORT='|V| along the ray (green) and its leading multipole (orange); below, r^(ℓ+1) V / c_ℓ → 1.';
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function pow10Label(e){ return '10'+String(e).split('').map(ch=>SUPS[ch]||ch).join(''); }
function rPow(l0){ return l0===0?'r':'r'+String(l0+1).split('').map(ch=>SUPS[ch]||ch).join(''); }
function farRange(F){
  const ly=[]; for(let k=0;k<F.Vs.length;k++){ const a=Math.abs(F.Vs[k]); if(a>0&&isFinite(a)) ly.push(Math.log10(a)); }
  if(!ly.length) return null;
  const last=Math.abs(F.Vs[F.Vs.length-1]), ldl=F.l0===null?NaN:Math.abs(F.lead[F.lead.length-1]);
  let lo=Math.min(last>0?Math.log10(last):Infinity,ldl>0?Math.log10(ldl):Infinity);
  if(!isFinite(lo)) lo=Math.min.apply(null,ly);
  lo=Math.floor(lo-0.3); const hi=Math.min(Math.ceil(Math.max.apply(null,ly)+0.2),lo+14);
  return {lo,hi};
}
function drawFar(ctx,W,H,M){
  const F=M.far, st=M.st, L=stageLayout(ctx,W,H,FAR_CAP_FULL,FAR_CAP_SHORT,2,0.36,1), b=L.main;
  const xlo=Math.log10(FAR_RLO), xhi=Math.log10(FAR_RHI), lx=F.rs.map(r=>Math.log10(r));
  /* the axis starts at 0.1 m but ticks from 1 m: a tick on the left edge collided
     with the lowest y label in the corner */
  const xt=[0,1,2,3], xf=v=>v===0?'1 m':v===1?'10 m':v===2?'100 m':'1 km';
  const R=M.n?farRange(F):null;
  if(!R){
    axesR(ctx,b,xlo,xhi,-3,1,{title:titleFor(b,'the potential along the ray, log–log','|V| along the ray'),xlab:'distance r from the centre',ylab:'|V| (V)',xticks:xt,xfmt:xf,yticks:[-3,-2,-1,0,1],yfmt:pow10Label});
    lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2,M.n?'V = 0 all along this ray':'no charges on the plane: nothing to expand',COL.dim,LAB_FONT,'center');
  } else {
    const yt=[]; for(let e=R.lo;e<=R.hi;e++) yt.push(e);
    const every=Math.max(1,Math.ceil(yt.length*16/b.h)), ytt=yt.filter(e=>(e-R.lo)%every===0);
    axesR(ctx,b,xlo,xhi,R.lo,R.hi,{title:titleFor(b,'|V| along the ray at '+fmt(F.th,0)+'° — the exact sum and its leading multipole, log–log','|V| along the ray, log–log'),
      xlab:'distance r from the centre',ylab:'|V| (V)',xticks:xt,xfmt:xf,yticks:ytt,yfmt:pow10Label});
    const lv=F.Vs.map(v=>Math.abs(v)>0?Math.log10(Math.abs(v)):NaN);
    if(F.M.dmax>0){ const xd=Math.log10(F.M.dmax); polyline(ctx,b,[xd,xd],[R.lo,R.hi],xlo,xhi,R.lo,R.hi,rgba(COL.dim,0.6),1,[3,4]);
      if(xd>xlo) lab(ctx,W,H,b.x+b.w*(xd-xlo)/(xhi-xlo)+5,b.y1-12,'d_max = '+fmt(F.M.dmax,2)+' m: the series converges beyond',COL.dim,SM_FONT,'left'); }
    if(F.l0!==null) polyline(ctx,b,lx,F.lead.map(v=>Math.abs(v)>0?Math.log10(Math.abs(v)):NaN),xlo,xhi,R.lo,R.hi,COL.ref,1.4,[6,4]);
    polyline(ctx,b,lx,lv,xlo,xhi,R.lo,R.hi,COL.pos,1.8);
    /* the orange entry only when the orange curve was drawn (Known-bad: a legend
       entry for a curve that is not there is a false statement about the picture) */
    legendAuto(ctx,b,[[COL.pos,'|V|, the exact sum']].concat(F.l0===null?[]:[[COL.ref,'|c'+F.l0+'| / '+rPow(F.l0)+', the '+ORDER_NAME[F.l0]]]));
  }
  /* below left: the charges, the centre, the ray */
  if(L.bottom.length){
    const bb=L.bottom[0], Mo=F.M;
    let x0=Mo.c[0]-0.5, x1=Mo.c[0]+0.5, y0=Mo.c[1]-0.5, y1=Mo.c[1]+0.5;
    for(const c of M.ch){ x0=Math.min(x0,c.x); x1=Math.max(x1,c.x); y0=Math.min(y0,c.y); y1=Math.max(y1,c.y); }
    const pad=0.25*Math.max(x1-x0,y1-y0), mp=worldFitUp(bb,{xmin:x0-pad,xmax:x1+pad,ymin:y0-pad,ymax:y1+pad},0);
    frame(ctx,bb,COL.edge);
    lab(ctx,W,H,bb.x,bb.y-12,M.n?'the charges and the ray at '+fmt(F.th,0)+'°':'no charges','#aeb6c6','italic 13px Georgia, serif','left');
    const vw={x0:mp.wx(bb.x),x1:mp.wx(bb.x1),y0:mp.wy(bb.y1),y1:mp.wy(bb.y)};
    if(M.n){
      if(Mo.dmax>0) circleW(ctx,mp,Mo.c,Mo.dmax,rgba(COL.dim,0.5),1,[3,4]);
      const far=Math.max(vw.x1-vw.x0,vw.y1-vw.y0)*2, cl=clipSeg(Mo.c[0],Mo.c[1],Mo.c[0]+far*F.n[0],Mo.c[1]+far*F.n[1],vw);
      if(cl){ ctx.beginPath(); ctx.moveTo(mp.X(cl[0]),mp.Y(cl[1])); ctx.lineTo(mp.X(cl[2]),mp.Y(cl[3])); ctx.strokeStyle=COL.ref; ctx.lineWidth=1.4; ctx.stroke(); }
      for(const c of M.ch) chargeGlyph(ctx,mp.X(c.x),mp.Y(c.y),Math.max(4,Math.min(9,CHARGE_R*mp.s)),c.q);
      const X=mp.X(Mo.c[0]), Y=mp.Y(Mo.c[1]); ctx.strokeStyle=COL.ref; ctx.lineWidth=1.4; ctx.beginPath(); ctx.moveTo(X-4,Y-4); ctx.lineTo(X+4,Y+4); ctx.moveTo(X-4,Y+4); ctx.lineTo(X+4,Y-4); ctx.stroke();
    }
  }
  /* below right: r^(l+1) V(r) / c_l -> 1 */
  if(L.bottom.length>1){
    const bb=L.bottom[1];
    axesR(ctx,bb,xlo,xhi,0,2,{title:titleFor(bb,F.l0===null?'r^(ℓ+1) V / c_ℓ — no leading term':rPow(F.l0)+' V(r) / c'+F.l0+' → 1 (the limit, numerically)','the limit, numerically'),
      xlab:'distance r',xticks:xt,xfmt:xf,ny:4,yfmt:v=>fmt(v,1)});
    if(F.l0!==null){ polyline(ctx,bb,[xlo,xhi],[1,1],xlo,xhi,0,2,COL.ref,1.2,[4,4]); polyline(ctx,bb,lx,F.ratio,xlo,xhi,0,2,COL.pos,1.8);
      lab(ctx,W,H,bb.x1-6,bb.y1-10,'Richardson at 50, 100 m: '+sigf(F.lim/F.cs[F.l0],10),COL.pos,SM_FONT,'right'); }
    else lab(ctx,W,H,bb.x+bb.w/2,bb.y+bb.h/2,M.n?'V = 0 along this ray':'no charges',COL.dim,SM_FONT,'center');
  }
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='plane') drawPlane(ctx,W,H,M);
  else if(M.view==='lines') drawLines(ctx,W,H,M);
  else if(M.view==='land') drawLand(ctx,W,H,M);
  else if(M.view==='super') drawSuper(ctx,W,H,M);
  else drawFar(ctx,W,H,M);
}
function wrapPi(a){ return a-TAU*Math.floor((a+PI)/TAU); }
/* the geometry a pointer event is judged against (the same functions the
   drawing uses, so a hit test cannot drift from the picture) */
function pointerMap(ctx,W,H,view){
  if(view==='plane') return planeGeo(ctx,W,H,PLANE_CAP_FULL,PLANE_CAP_SHORT).map;
  if(view==='lines') return planeGeo(ctx,W,H,LINES_CAP_FULL,LINES_CAP_SHORT).map;
  if(view==='super') return superGeo(ctx,W,H).map;
  return null;
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.resetCam=function(){ ST.camTheta=DEFAULTS.camTheta; ST.camPhi=DEFAULTS.camPhi; ST.camZoom=DEFAULTS.camZoom; };
  /* the wheel zooms the landscape and nothing else */
  S.wheel=function(dy){ if(ST.view!=='land') return false; ST.camZoom=clamp(ST.camZoom*Math.exp(-dy*0.0012),0.4,3); return true; };
  S.pointer=function(type,x,y){
    const st=ST, v=st.view;
    if(type==='up'){
      const d=DRAG.what; DRAG.what=null; if(d===null) return false;
      /* the bin exists only on the plane: elsewhere a charge dropped where it would
         be stays put (it was silently deleted in the field-lines view) */
      if(d==='charge'&&v==='plane'){ const c=st.charges[DRAG.k]; if(c&&inBin(c.x,c.y)){ if(DRAG.fresh&&!DRAG.moved) st.charges.splice(DRAG.k,1); else removeCharge(st,DRAG.k); } }
      if(d==='es'){ const s=st.esens[DRAG.k]; if(s&&inBin(s.x,s.y)) st.esens.splice(DRAG.k,1); }
      return true;
    }
    if(v==='land'){
      if(type==='down'){ DRAG.what='cam'; DRAG.x=x; DRAG.y=y; DRAG.th=st.camTheta; DRAG.ph=st.camPhi; return true; }
      if(type==='move'&&DRAG.what==='cam'){ st.camTheta=wrapPi(DRAG.th-(x-DRAG.x)*0.008); st.camPhi=clamp(DRAG.ph+(y-DRAG.y)*0.008,0.05,1.5); return true; }
      return false;
    }
    const map=pointerMap(canvas.getContext('2d'),S.W,S.H,v); if(!map) return false;
    const wx=map.wx(x), wy=map.wy(y);
    if(type==='down'){
      DRAG.fresh=false; DRAG.moved=false;
      if(v==='plane'&&st.showVS){
        const g=vsGeo(map,st,S.W,S.H);
        if(inBox(g.plot,x,y)){ plotEquipotential(st); return true; }
        if(inBox(g.clear,x,y)){ st.eqSeeds=[]; return true; }
        if(Math.hypot(x-g.X,y-g.Y)<=g.r+5||inBox(g.panel,x,y)){ DRAG.what='vs'; DRAG.dx=st.vs.x-wx; DRAG.dy=st.vs.y-wy; return true; }
      }
      if(v==='plane') for(let k=st.esens.length-1;k>=0;k--) if(Math.hypot(x-map.X(st.esens[k].x),y-map.Y(st.esens[k].y))<=10){ DRAG.what='es'; DRAG.k=k; return true; }
      if(v==='super'&&Math.hypot(x-map.X(st.probe.x),y-map.Y(st.probe.y))<=12){ DRAG.what='probe'; return true; }
      const rp=Math.max(10,chargePx(map));
      for(let k=st.charges.length-1;k>=0;k--){ const c=st.charges[k];
        if(Math.hypot(x-map.X(c.x),y-map.Y(c.y))<=rp){ DRAG.what='charge'; DRAG.k=k; DRAG.dx=c.x-wx; DRAG.dy=c.y-wy; return true; } }
      if(v==='plane'&&st.showTape){
        const t=st.tape;
        if(Math.hypot(x-map.X(t.ax),y-map.Y(t.ay))<=9){ DRAG.what='tapeA'; return true; }
        if(Math.hypot(x-map.X(t.bx),y-map.Y(t.by))<=9){ DRAG.what='tapeB'; return true; }
        const c=clipSeg(t.ax,t.ay,t.bx,t.by,{x0:wx-6/map.s,x1:wx+6/map.s,y0:wy-6/map.s,y1:wy+6/map.s});
        if(c){ DRAG.what='tape'; DRAG.x=wx; DRAG.y=wy; DRAG.t0=Object.assign({},t); return true; }
      }
      if(v==='plane') for(const s of BIN_SRC){
        if(Math.hypot(x-map.X(s.x),y-map.Y(BIN_GLYPH_Y))>Math.max(12,chargePx(map)+3)) continue;
        if(s.kind==='es'){ if(st.esens.length>=MAX_SENSORS) return false; st.esens.push({x:s.x,y:BIN_GLYPH_Y}); DRAG.what='es'; DRAG.k=st.esens.length-1; return true; }
        if(st.charges.length>=MAX_CHARGES) return false;
        st.charges.push({x:s.x,y:BIN_GLYPH_Y,q:s.kind==='pos'?1:-1}); st.preset='custom';
        DRAG.what='charge'; DRAG.k=st.charges.length-1; DRAG.dx=0; DRAG.dy=0; DRAG.fresh=true; return true;
      }
      return false;
    }
    if(type==='move'){
      const px=clamp(wx,PLANE.x0,PLANE.x1), py=clamp(wy,PLANE.y0,PLANE.y1);
      if(DRAG.what==='charge'){ DRAG.moved=true; return moveCharge(st,DRAG.k,wx+DRAG.dx,wy+DRAG.dy); }
      if(DRAG.what==='es'){ const s=st.esens[DRAG.k]; if(!s) return false; s.x=px; s.y=py; return true; }
      if(DRAG.what==='vs'){ st.vs.x=clamp(wx+DRAG.dx,PLANE.x0,PLANE.x1); st.vs.y=clamp(wy+DRAG.dy,PLANE.y0,PLANE.y1); return true; }
      if(DRAG.what==='probe'){ st.probe.x=px; st.probe.y=py; return true; }
      if(DRAG.what==='tapeA'){ st.tape.ax=px; st.tape.ay=py; return true; }
      if(DRAG.what==='tapeB'){ st.tape.bx=px; st.tape.by=py; return true; }
      if(DRAG.what==='tape'){ const t0=DRAG.t0, ddx=wx-DRAG.x, ddy=wy-DRAG.y;
        const sx=clamp(ddx,PLANE.x0-Math.min(t0.ax,t0.bx),PLANE.x1-Math.max(t0.ax,t0.bx)), sy=clamp(ddy,PLANE.y0-Math.min(t0.ay,t0.by),PLANE.y1-Math.max(t0.ay,t0.by));
        st.tape.ax=t0.ax+sx; st.tape.bx=t0.bx+sx; st.tape.ay=t0.ay+sy; st.tape.by=t0.by+sy; return true; }
      return false;
    }
    return false;
  };
  return S;
}
