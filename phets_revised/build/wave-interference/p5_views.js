
/* ================================================================== *
 *  the far field, path difference, the lattice; dispatch; the scene   *
 * ================================================================== */
const AP_HALF=0.5;                                      /* the aperture panel spans +-0.5 mm */
function capsulePoly(ax,ay,bx,by,r,n){
  const dx=bx-ax, dy=by-ay, L=Math.hypot(dx,dy)||1e-12, a=Math.atan2(dy,dx), pts=[];
  for(let q=0;q<=n;q++){ const t=a-PI/2+PI*q/n; pts.push([bx+r*Math.cos(t),by+r*Math.sin(t)]); }
  for(let q=0;q<=n;q++){ const t=a+PI/2+PI*q/n; pts.push([ax+r*Math.cos(t),ay+r*Math.sin(t)]); }
  return pts;
}
function ellipsePoly(cx,cy,rx,ry,n){ const pts=[]; for(let q=0;q<n;q++){ const t=TAU*q/n; pts.push([cx+rx*Math.cos(t),cy+ry*Math.sin(t)]); } return pts; }
function fillPolyPx(ctx,pts,col){ ctx.beginPath(); pts.forEach((p,k)=>{ if(k===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); ctx.closePath(); ctx.fillStyle=col; ctx.fill(); }
/* the aperture at its true size (s = 1), as geometry: what the FFT sees, unmagnified */
function drawAperture(ctx,b,P){
  const X=x=>b.x+(x+AP_HALF)/(2*AP_HALF)*b.w, Y=y=>b.y+(y+AP_HALF)/(2*AP_HALF)*b.h, sc=b.w/(2*AP_HALF), open='#eef1f6';
  ctx.fillStyle='#000000'; ctx.fillRect(b.x,b.y,b.w,b.h);
  const id=P.ap;
  if(id==='ellipse'){ const ax=ellipseAxes(P,1); fillPolyPx(ctx,ellipsePoly(X(0),Y(0),ax[0]*sc,ax[1]*sc,72),open); }
  else if(id==='rect'){ ctx.fillStyle=open; ctx.fillRect(X(-P.recW/2),Y(-P.recH/2),P.recW*sc,P.recH*sc); }
  else if(id==='cs'){ const c=26*DIF.PX; fillPolyPx(ctx,ellipsePoly(X(-c),Y(-c),P.csD/2*sc,P.csD/2*sc,60),open);
    ctx.fillStyle=open; ctx.fillRect(X(c-P.csW/2),Y(c-P.csW/2),P.csW*sc,P.csW*sc); }
  else if(id==='disorder'){ const p=P.disP, f=P.disL/4*0.3*p;
    for(let a=0;a<4;a++) for(let q=0;q<4;q++){ const v=DISORDER_V[4*a+q];
      fillPolyPx(ctx,ellipsePoly(X((a-1.5)*p+f*v[0]),Y((q-1.5)*p+f*v[1]),P.disD/2*sc,P.disD/2*sc,36),open); } }
  else if(id==='figure'){ const H=P.figH, rot=P.figR*DEG, co=Math.cos(rot), si=Math.sin(rot);
    const tw=(u,v)=>[X(H*(u*co-v*si)),Y(H*(u*si+v*co))], hd=FIGURE.head;
    const hc=tw(hd[0],hd[1]); fillPolyPx(ctx,ellipsePoly(hc[0],hc[1],hd[2]*H*sc,hd[2]*H*sc,40),open);
    for(const c of FIGURE.caps){ const A=tw(c[0],c[1]), B=tw(c[2],c[3]); fillPolyPx(ctx,capsulePoly(A[0],A[1],B[0],B[1],c[4]*H*sc,10),open); } }
  else if(id==='gauss'){ for(const t of [0.1,0.3,0.5,0.7,0.9]){ const k=Math.sqrt(-2*Math.log(t));
    fillPolyPx(ctx,ellipsePoly(X(0),Y(0),k*P.gauSx*sc,k*P.gauSy*sc,64),mix('#000000',open,t)); } }
  else if(id==='slits'){ const n=Math.round(P.sltN), x0=-(n-1)/2*P.sltD; ctx.fillStyle=open;
    for(let q=0;q<n;q++) ctx.fillRect(X(x0+q*P.sltD-P.sltW/2),Y(-DIF.SLIT_H/2),P.sltW*sc,DIF.SLIT_H*sc); }
  frame(ctx,b,'#2a3040');
}
function patternLevel(F,m){ return ST.farMode==='phet'?phetDisplay(m,F.D.max):(F.D.max>0?(m/F.D.max)*(m/F.D.max):0); }
function drawPattern(ctx,b,F){
  ctx.fillStyle='#000000'; ctx.fillRect(b.x,b.y,b.w,b.h);
  if(!ST.laser){ frame(ctx,b,'#2a3040'); return 0; }
  const n=DIF.N, cs=b.w/n, K=32, top=specCss(ST.lam,1), rects=[]; for(let q=0;q<=K;q++) rects.push([]);
  let cells=0;
  for(let j=0;j<n;j++){ const y0=Math.round(b.y+j*cs), y1=Math.round(b.y+(j+1)*cs); let i=0;
    while(i<n){ const q=Math.round(K*clamp(patternLevel(F,F.D.mag[j*n+i]),0,1)); let e=i+1;
      while(e<n&&Math.round(K*clamp(patternLevel(F,F.D.mag[j*n+e]),0,1))===q) e++;
      if(q>0){ rects[q].push(Math.round(b.x+i*cs),y0,Math.round(b.x+e*cs),y1); cells+=e-i; }
      i=e; } }
  for(let q=1;q<=K;q++){ const r=rects[q]; if(!r.length) continue; ctx.beginPath();
    for(let k=0;k<r.length;k+=4) ctx.rect(r[k],r[k+1],r[k+2]-r[k],r[k+3]-r[k+1]); ctx.fillStyle=mix('#000000',top,q/K); ctx.fill(); }
  frame(ctx,b,'#2a3040');
  return cells;
}
function farGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,farCaption(M,true),farCaption(M,false),capW,top+220);
  const avail=fit.capY-18-top, cutH=Math.max(80,Math.min(190,Math.round(avail*0.28)));
  const usable=(narrow?W-26:W-RO_W-44)-56;
  /* the cut plot needs 70 px of its own plus its labels; where the stage is too short for that,
     it is dropped with a note and the two squares take the height instead (narrow-stage mode) */
  const withCut=avail-cutH-78>=90;
  const side=Math.floor(Math.max(90,Math.min(withCut?avail-cutH-78:avail-24,(usable-34)/2)));
  const ap=box(56,top+14,side,side), pat=box(56+side+34,top+14,side,side);
  const cy=pat.y1+50, cx1=(cy>486||narrow)?W-24:pat.x1;
  const G={ap,pat,capY:fit.capY,capTxt:fit.txt,capW:fit.capW};
  if(withCut&&fit.capY-44-cy>=70) G.cut=box(96,cy,Math.max(120,cx1-96),fit.capY-44-cy);
  return G;
}
function farCaption(M,full){
  const F=M.F;
  const base='Left: the aperture at its true size (1 mm across). Right: the far-field pattern, ±'+sigf(Math.asin(128*DIF.SIN_PER_BIN)/DEG,3)
    +'° across, '+(ST.farMode==='phet'?'brightness log(1 + |F|/100), PhET’s scale':'brightness |F|² (linear intensity)')+'.';
  if(!full) return base;
  return base+' The pattern is |FFT| of a 256 × 256 map of the aperture (4/3 mm, PhET’s grid), drawn '+sigf(F.s,3)
    +'× larger at this wavelength so every wavelength shares one angular scale. Below: the horizontal cut, FFT against '
    +(F.hasAna?'the closed form (orange)':'no closed form for this aperture')+', on a log scale.';
}
function drawFar(ctx,W,H,M){
  const G=farGeo(ctx,W,H,M), F=M.F;
  drawAperture(ctx,G.ap,F.P);
  const sb=0.1/(2*AP_HALF)*G.ap.w;
  ctx.fillStyle='#cfd4de'; ctx.fillRect(G.ap.x,G.ap.y-10,sb,3);
  lab(ctx,W,H,G.ap.x+sb+6,G.ap.y-9,'0.1 mm','#cfd4de',SM_FONT,'left');
  if(G.ap.w>=200) lab(ctx,W,H,G.ap.x1,G.ap.y-9,'the aperture','#aeb6c6','italic 12px Georgia, serif','right');
  drawPattern(ctx,G.pat,F);
  lab(ctx,W,H,G.pat.x,G.pat.y-9,titleFor(G.pat,'the pattern, '+fmt(ST.lam,0)+' nm','the pattern'),'#aeb6c6','italic 12px Georgia, serif','left');
  if(!ST.laser) lab(ctx,W,H,G.pat.x+G.pat.w/2,G.pat.y+G.pat.h/2,'the laser is off','#8b93a6',LAB_FONT,'center');
  /* the cut */
  if(!G.cut){ lab(ctx,W,H,G.ap.x,G.ap.y1+16,'the cut: needs a taller window','#8b93a6',SM_FONT,'left');
    drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW}); return G; }
  const c=G.cut, amax=Math.asin(128*DIF.SIN_PER_BIN)/DEG, ang=F.ks.map(k=>Math.asin(k*DIF.SIN_PER_BIN)/DEG);
  const lg=a=>a.map(v=>v>0?Math.log10(Math.max(v,1e-9)):NaN);
  axesR(ctx,c,-amax,amax,-4,0,{nx:8,yticks:[-4,-3,-2,-1,0],yfmt:t=>t===0?'1':'10'+['⁰','⁻¹','⁻²','⁻³','⁻⁴'][-t],
    xfmt:t=>fmt(t,1)+'°',title:titleFor(c,'the horizontal cut through the pattern, I / I(0)','the cut, I / I(0)'),xlab:'angle θ'});
  if(ST.laser){
    if(F.hasAna) polyline(ctx,c,ang,lg(F.ana),-amax,amax,-4,0,COL.ref,1.3);
    polyline(ctx,c,ang,lg(F.cut),-amax,amax,-4,0,COL.pos,1.6);
    if(F.zero!==null&&F.zero<1){ const z=Math.asin(F.zero)/DEG;
      for(const sg of [1,-1]) polyline(ctx,c,[sg*z,sg*z],[-4,0],-amax,amax,-4,0,COL.ref,1,[3,4]); }
    legendAuto(ctx,c,F.hasAna?[[COL.pos,'FFT of the drawn aperture'],[COL.ref,'closed form']]:[[COL.pos,'FFT of the drawn aperture']]);
  }
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ---- path difference ---- */
function pathGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,pathCaption(M,true),pathCaption(M,false),capW,top+200);
  const avail=fit.capY-24-top, plotW=narrow?110:170;
  /* 38 px under the map and the plot for the plot's axis labels */
  const mapW=Math.max(140,(narrow?W-26:W-RO_W-44)-56-plotW-40), mapH=Math.max(100,avail-38);
  const mb=box(56,top,mapW,mapH), pb=box(mb.x1+26,top,plotW,mapH);
  /* equal aspect: this is a shape (a family of hyperbolae) */
  const P=M.P, span=Math.max(1.2*P.L, 1.4*P.d*mapW/mapH);
  const x0=-0.1*span, x1=x0+span, halfY=span*mapH/mapW/2;
  return {mb,pb,x0,x1,y0:-halfY,y1:halfY,capY:fit.capY,capTxt:fit.txt,capW:fit.capW};
}
function pathCaption(M,full){
  const P=M.P;
  const base='Two in-phase sources '+fmt(P.d,2)+' λ apart; the screen (magenta) at '+fmt(P.L,1)+' λ. Equal scales on both axes.';
  if(!full) return base;
  return base+' Brightness: the interference factor I/(1/r₁ + 1/r₂) = 1 + 2 cos k(r₁ − r₂) √(r₁r₂)/(r₁ + r₂) of two 2-D cylindrical waves e^(ikr)/√r, so the fading with distance is divided out. '
    +'Orange: the nodal hyperbolae r₁ − r₂ = (m + ½)λ'+(ST.asym?'; dotted: their asymptotes d sin θ = (m + ½)λ':'')+'. Right: the intensity along the screen, exact (green) and Fraunhofer cos²(πd sin θ/λ) (dashed).';
}
function drawPath(ctx,W,H,M){
  const G=pathGeo(ctx,W,H,M), P=M.P, b=G.mb, k=P.k;
  const X=x=>b.x+(x-G.x0)/(G.x1-G.x0)*b.w, Y=y=>b.y+(y-G.y0)/(G.y1-G.y0)*b.h;
  ctx.fillStyle='#05070c'; ctx.fillRect(b.x,b.y,b.w,b.h);
  /* the intensity map, 24 classes, runs merged */
  const nx=Math.min(160,Math.max(40,Math.round(b.w/5))), ny=Math.max(20,Math.round(nx*b.h/b.w)), K=24, rects=[];
  for(let q=0;q<=K;q++) rects.push([]);
  for(let j=0;j<ny;j++){ const y=G.y0+(j+0.5)*(G.y1-G.y0)/ny, py0=Math.round(b.y+j*b.h/ny), py1=Math.round(b.y+(j+1)*b.h/ny);
    let i=0;
    const lev=ii=>{ const x=G.x0+(ii+0.5)*(G.x1-G.x0)/nx; return Math.round(K*clamp(fringeFactor(x,y,P.d,k)/2,0,1)); };
    let q=lev(0);
    while(i<nx){ let e=i+1, q2=0; while(e<nx&&(q2=lev(e))===q) e++;
      if(q>0) rects[q].push(Math.round(b.x+i*b.w/nx),py0,Math.round(b.x+e*b.w/nx),py1);
      i=e; if(i<nx) q=q2; } }
  for(let q=1;q<=K;q++){ const r=rects[q]; if(!r.length) continue; ctx.beginPath();
    for(let t=0;t<r.length;t+=4) ctx.rect(r[t],r[t+1],r[t+2]-r[t],r[t+3]-r[t+1]); ctx.fillStyle=shade(COL.pos,q/K); ctx.fill(); }
  /* hyperbolae and asymptotes */
  const xs=[]; for(let q=0;q<=120;q++) xs.push(G.x0+(G.x1-G.x0)*q/120);
  /* hyperY and farY are the pinned formulas (farY(d, D, x) is the asymptote x tan(theta)) */
  if(ST.hyp) for(const mn of P.mins) for(const sg of [1,-1])
    polyline(ctx,b,xs,xs.map(x=>sg*hyperY(P.d,mn.D,x)),G.x0,G.x1,G.y1,G.y0,COL.ref,1.3,[5,4]);
  if(ST.asym) for(const mn of P.mins) for(const sg of [1,-1])
    polyline(ctx,b,[0,G.x1],[0,sg*farY(P.d,mn.D,G.x1)],G.x0,G.x1,G.y1,G.y0,COL.struct,1,[2,4]);
  /* the screen and the sources */
  polyline(ctx,b,[P.L,P.L],[G.y0,G.y1],G.x0,G.x1,G.y1,G.y0,COL.live,2);
  for(const sg of [-1,1]) dot(ctx,X(0),Y(sg*P.d/2),4.5,'#ffffff');
  lab(ctx,W,H,X(0)+8,Y(-P.d/2)-10,'S₁','#ffffff',LAB_FONT,'left'); lab(ctx,W,H,X(0)+8,Y(P.d/2)+10,'S₂','#ffffff',LAB_FONT,'left');
  frame(ctx,b,'#2a3040');
  /* the screen plot, sharing the map's vertical axis */
  const c=G.pb, ys=[], ex=[], ff=[];
  for(let q=0;q<=300;q++){ const y=G.y0+(G.y1-G.y0)*q/300; ys.push(y); ex.push(twoSourceI(P.L,y,P.d,k)/P.I0); ff.push(twoSourceFar(P.L,y,P.d,k)); }
  axesR(ctx,c,0,1.1,G.y1,G.y0,{xticks:[0,0.5,1],yticks:[],xfmt:t=>fmt(t,1),title:'on the screen',xlab:'I / I(0)'});
  polyline(ctx,c,ff,ys,0,1.1,G.y1,G.y0,COL.ref,1.2,[4,3]);
  polyline(ctx,c,ex,ys,0,1.1,G.y1,G.y0,COL.pos,1.7);
  for(const mn of P.mins) for(const sg of [1,-1]){
    const yy=c.y+(sg*mn.y-G.y0)/(G.y1-G.y0)*c.h, yf=c.y+(sg*mn.yf-G.y0)/(G.y1-G.y0)*c.h;
    if(yy>c.y&&yy<c.y1){ ctx.beginPath(); ctx.moveTo(c.x,yy); ctx.lineTo(c.x+10,yy); ctx.strokeStyle=COL.ref; ctx.lineWidth=2; ctx.stroke(); }
    if(yf>c.y&&yf<c.y1){ ctx.beginPath(); ctx.moveTo(c.x1-10,yf); ctx.lineTo(c.x1,yf); ctx.strokeStyle=COL.struct; ctx.lineWidth=2; ctx.stroke(); } }
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ---- the lattice (analysis) ---- */
function latticeGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,narrow?latAnCaption(false):latAnCaption(true),latAnCaption(false),capW,top+220);
  const right=(narrow?W-26:W-RO_W-44), gut=70;
  if(narrow) return {panels:[box(64,top+10,Math.max(120,right-80),Math.max(80,fit.capY-60-top))],capY:fit.capY,capTxt:fit.txt,capW:fit.capW};
  const w1=(right-64-gut)/2, h1=Math.max(90,Math.min(0.42*(fit.capY-top),486-60-top));
  const y2=Math.max(top+h1+74,506), h2=Math.max(80,fit.capY-44-y2), w2=(W-24-64-gut)/2;
  return {panels:[box(64,top+10,w1,h1),box(64+w1+gut,top+10,w1,h1),box(64,y2,w2,h2),box(64+w2+gut,y2,w2,h2)],
          capY:fit.capY,capTxt:fit.txt,capW:fit.capW};
}
function latAnCaption(full){
  const base='PhET’s scheme at C = ½: the dispersion relation (top left), its phase and group speeds (top right)';
  if(!full) return 'The lattice’s dispersion relation at C = ½; the operating point of the chosen medium in magenta.';
  return base+', the reflection off the absorbing edge (bottom left) and the calibration against PhET’s fixed time step (bottom right). The magenta marks are the chosen medium and frequency; shaded bands are the three media’s ranges.';
}
function drawLatticeAnalysis(ctx,W,H,M){
  const G=latticeGeo(ctx,W,H,M), K=M.K, pn=G.panels;
  /* (a) the dispersion relation */
  { const b=pn[0], ks=[], ax=[], dg=[], co=[];
    for(let q=0;q<=160;q++){ const k=PI*q/160; ks.push(k); ax.push(latOmega(k,0)); dg.push(latOmega(k/Math.SQRT2,k/Math.SQRT2)); co.push(LAT.C*k); }
    axesR(ctx,b,0,PI,0,1.2,{nx:5,yticks:[0.3,0.6,0.9,1.2],xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,1),title:titleFor(b,'the dispersion relation, ωΔt against kΔx','ωΔt against kΔx'),xlab:'kΔx (radians per cell)',ylab:'ωΔt'});
    const kmin=TAU/cellsPerWave(K.S,K.S.fmin), kmax=TAU/cellsPerWave(K.S,K.S.fmax);
    ctx.fillStyle=rgba(COL.struct,0.12); ctx.fillRect(b.x+b.w*kmin/PI,b.y,b.w*(kmax-kmin)/PI,b.h);
    polyline(ctx,b,ks,co,0,PI,0,1.2,COL.ref,1.3,[5,4]);
    polyline(ctx,b,ks,dg,0,PI,0,1.2,COL.pos,1.4,[3,3]);
    polyline(ctx,b,ks,ax,0,PI,0,1.2,COL.pos,1.8);
    marker(ctx,b,0,PI,0,1.2,K.k,K.Om,COL.live);
    if(!G.panels[1]) { drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW}); return G; }
    legendAuto(ctx,b,[[COL.pos,'along an axis'],[COL.pos,'diagonal (dashed)'],[COL.ref,'continuum ω = ck']]); }
  /* (b) the speeds against cells per wavelength */
  { const b=pn[1], Ns=[], vp=[], vpd=[], vg=[], vgd=[];
    for(let q=0;q<=120;q++){ const N=Math.pow(10,Math.log10(4)+(Math.log10(100)-Math.log10(4))*q/120), k=TAU/N, Om=omegaStep(N), kd=latK(Om,PI/4);
      Ns.push(Math.log10(N)); vp.push(latPhaseSpeed(k,0)/LAT.C); vg.push(latGroupSpeed(k,0)/LAT.C); vpd.push(latPhaseSpeed(kd,PI/4)/LAT.C); vgd.push(latGroupSpeed(kd,PI/4)/LAT.C); }
    const lx=[Math.log10(4),2];
    axesR(ctx,b,lx[0],lx[1],0.8,1.04,{xticks:[Math.log10(5),1,Math.log10(20),Math.log10(50),2],xfmt:t=>sigf(Math.pow(10,t),2),yticks:[0.8,0.85,0.9,0.95,1],yfmt:t=>fmt(t,2),
      title:titleFor(b,'phase and group speed / c, against cells per wavelength','speeds / c'),xlab:'cells per wavelength (log)'});
    const bands=[];
    for(const id of SCENE_IDS){ const S=SCENES[id], a=Math.log10(cellsPerWave(S,S.fmax)), c=Math.log10(cellsPerWave(S,S.fmin));
      ctx.fillStyle=rgba(COL.struct,id===K.S.id?0.2:0.07); ctx.fillRect(b.x+b.w*(a-lx[0])/(lx[1]-lx[0]),b.y,b.w*(c-a)/(lx[1]-lx[0]),b.h);
      bands.push([b.x+b.w*((a+c)/2-lx[0])/(lx[1]-lx[0]),S.name]); }
    polyline(ctx,b,[lx[0],lx[1]],[1,1],lx[0],lx[1],0.8,1.04,COL.ref,1.2,[5,4]);
    polyline(ctx,b,Ns,vpd,lx[0],lx[1],0.8,1.04,COL.pos,1.3,[3,3]); polyline(ctx,b,Ns,vp,lx[0],lx[1],0.8,1.04,COL.pos,1.8);
    polyline(ctx,b,Ns,vgd,lx[0],lx[1],0.8,1.04,COL.live,1.2,[3,3]); polyline(ctx,b,Ns,vg,lx[0],lx[1],0.8,1.04,COL.live,1.6);
    polyline(ctx,b,[Math.log10(K.Nl),Math.log10(K.Nl)],[0.8,1.04],lx[0],lx[1],0.8,1.04,COL.live,1,[2,3]);
    /* the legend first, registered, so the band names dodge it (legendAuto avoids curves, not labels) */
    const lb=legendAuto(ctx,b,[[COL.pos,'phase (dashed: diagonal)'],[COL.live,'group (dashed: diagonal)']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
    for(const [x,t] of bands) if(!lab(ctx,W,H,x,b.y+11,t,'#6f8fa0',SM_FONT,'center')) lab(ctx,W,H,x,b.y1-12,t,'#6f8fa0',SM_FONT,'center'); }
  /* (c) the edge */
  { const b=pn[2], th=[], r1=[], r2=[], rc=[];
    for(let q=0;q<=80;q++){ const a=q*DEG; th.push(q); r1.push(Math.log10(Math.max(1e-6,murReflection(K.k*Math.cos(a),K.k*Math.sin(a),1))));
      r2.push(Math.log10(Math.max(1e-6,murReflection(K.k*Math.cos(a),K.k*Math.sin(a),2)))); rc.push(Math.log10(Math.max(1e-6,(1-Math.cos(a))/(1+Math.cos(a))))); }
    axesR(ctx,b,0,80,-4,0,{nx:8,yticks:[-4,-3,-2,-1,0],yfmt:t=>t===0?'1':'10'+['⁰','⁻¹','⁻²','⁻³','⁻⁴'][-t],xfmt:t=>fmt(t,0)+'°',
      title:titleFor(b,'reflection |R| off the absorbing edge, at '+sigf(K.Nl,3)+' cells per wavelength','edge reflection |R|'),xlab:'angle of incidence'});
    polyline(ctx,b,th,rc,0,80,-4,0,COL.ref,1,[2,4]); polyline(ctx,b,th,r1,0,80,-4,0,COL.ref,1.4,[5,4]); polyline(ctx,b,th,r2,0,80,-4,0,COL.pos,1.8);
    legendAuto(ctx,b,[[COL.pos,'Mur, 2nd order (this engine)'],[COL.ref,'Mur, 1st order (dashed)']]); }
  /* (d) the calibration against PhET's fixed step */
  { const b=pn[3], S=K.S, fs=[], er=[];
    for(let q=0;q<=80;q++){ const f=S.fmin+(S.fmax-S.fmin)*q/80; fs.push(f*S.fMul); er.push(100*(phetLambda(S,f)/waveLen(S,f)-1)); }
    const lo=Math.min(-4,Math.floor(Math.min.apply(null,er))-0.5);
    axesR(ctx,b,S.fmin*S.fMul,S.fmax*S.fMul,lo,1,{nx:5,ny:4,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),
      title:titleFor(b,'wavelength error on the lattice, % ('+S.name+')','λ error, %'),xlab:'frequency, '+S.fUnit});
    polyline(ctx,b,[S.fmin*S.fMul,S.fmax*S.fMul],[0,0],S.fmin*S.fMul,S.fmax*S.fMul,lo,1,COL.pos,1.8);
    polyline(ctx,b,fs,er,S.fmin*S.fMul,S.fmax*S.fMul,lo,1,COL.ref,1.6);
    marker(ctx,b,S.fmin*S.fMul,S.fmax*S.fMul,lo,1,K.f*S.fMul,100*K.phetErr,COL.live);
    legendAuto(ctx,b,[[COL.pos,'this file: step solved per frequency'],[COL.ref,'PhET: one step per medium']]); }
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.L) return drawLatticeView(ctx,W,H,M);
  if(M.view==='far') return drawFar(ctx,W,H,M);
  if(M.view==='path') return drawPath(ctx,W,H,M);
  return drawLatticeAnalysis(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame: only the three lattice views have a clock */
  S.step=function(){ return LATTICE_VIEWS[ST.view]?clockFrame()>0:false; };
  /* the pointer: the tape ends, the probes and the barrier on the lattice views.
     (Path difference has no drag: its map is fitted to L, so a dragged screen
     line would stay put while the map rescaled under it — the slider sets L.) */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const ctx=canvas.getContext('2d');
    if(LATTICE_VIEWS[ST.view]){
      const M=buildModel(), G=latGeo(ctx,S.W,S.H,M), sq=G.sq, R=M.L.R;
      const fx=(x-sq.x)/sq.w, fy=(y-sq.y)/sq.h;
      if(type==='down'){
        const hits=[];
        if(ST.tape) TOOLS.tape.forEach((p,q)=>hits.push(['tape'+q,sq.x+p[0]*sq.w,sq.y+p[1]*sq.h]));
        if(ST.meter) TOOLS.probes.forEach((p,q)=>hits.push(['probe'+q,sq.x+p[0]*sq.w,sq.y+p[1]*sq.h]));
        for(const h2 of hits) if(Math.hypot(x-h2[1],y-h2[2])<10){ DRAG.what=h2[0]; return true; }
        if(ST.view==='slits'&&R.plane.barrier!=='none'){ const xb=cellX(sq,R,R.plane.bcol);
          if(Math.abs(x-xb)<10&&y>=sq.y&&y<=sq.y1+22){ DRAG.what='barrier'; return true; } }
        return false;
      }
      if(type==='move'){
        if(!DRAG.what) return false;
        if(DRAG.what==='barrier'){ const c=clamp(Math.round(R.lat.pad-0.5+fx*LAT.VIS),BCOL_MIN,BCOL_MAX); if(c===ST.bcol) return false; ST.bcol=c; return true; }
        const q=+DRAG.what.slice(-1), arr=DRAG.what.indexOf('tape')===0?TOOLS.tape:TOOLS.probes;
        arr[q]=[clamp(fx,0,1),clamp(fy,0,1)]; return true;
      }
      return false;
    }
    return false;
  };
  return S;
}
