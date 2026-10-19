
/* ================================================================== *
 *  view 3: the reflections — one pulse, three ends, the images        *
 * ================================================================== */
const REFL_CAP_FULL='One pulse, A high and w long, goes into three strings at once, with no damping. Green is the lattice; this view moves in whole '
  +'steps, so every frame is a lattice level. Orange is d’Alembert with an image: the incident pulse (dashed) runs on past the end into the mirror '
  +'world (shaded), its image (dotted) runs back out, and their sum (the orange halo) goes through every bead. The clamp needs y = 0, so its image is inverted; '
  +'the ring needs zero slope, so its image is upright, mirrored about bead 59½; the open end has no image at all.';
const REFL_CAP_SHORT='One pulse, three ends, no damping: green lattice on orange d’Alembert-with-images. Fixed inverts, loose does not, open absorbs.';
const REFL_XHI=LSTR+2.2;
function reflGeo(ctx,W,H){
  const narrow=isNarrow(W), left=62, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,REFL_CAP_FULL,REFL_CAP_SHORT,capW,stageTop()+30+300);
  const top=stageTop()+30, avail=fit.capY-40-top, gap=30, h=Math.max(40,(avail-2*gap-18)/3);
  const strips=[0,1,2].map(k=>box(left,top+18+k*(h+gap),right-left,h));
  return {fit,strips,narrow};
}
/* the incident and reflected parts along the whole drawn range, mirror world included */
function reflCurves(end,A,w,v,t,n){
  const Lr=end==='fixed'?LSTR:LLOOSE, sr=end==='fixed'?-1:1, f=tau=>A*tri(tau/w);
  const xs=[], inc=[], ref=[], sum=[];
  for(let k=0;k<=n;k++){
    const x=REFL_XHI*k/n; xs.push(x);
    let a=0, b=0, rt=1;
    if(end==='none') a=f(t-x/v);
    else for(let m=0;m<1000;m++){
      const t1=t-(2*m*Lr+x)/v, t2=t-(2*(m+1)*Lr-x)/v;
      if(t1<=0&&t2<=0) break;
      a+=rt*f(t1); b+=rt*sr*f(t2); rt*=-sr;
    }
    inc.push(a); ref.push(b); sum.push(x<=(end==='none'?LSTR:Lr)?a+b:NaN);
  }
  return {xs,inc,ref,sum,Lr};
}
function drawRefl(ctx,W,H,M){
  const st=M.st, G=reflGeo(ctx,W,H), A=Math.max(st.amp,0.05), ylo=-2.3*A, yhi=2.3*A, t=M.tR;
  const TITLES={fixed:['fixed end: y₆₀ = 0, so the image comes back inverted','fixed end'],
                loose:['loose end: y₆₀ = y₅₉, so the image comes back upright','loose end'],
                none:['no end: y₆₀ follows y₅₉ one step late, and nothing comes back','no end']};
  ENDS.forEach((e,k)=>{
    const b=G.strips[k], last=k===2, C=reflCurves(e,st.amp,st.pw,M.v,t,360), R=M.sum[e];
    const XL=b.x+b.w*(e==='none'?LSTR:C.Lr)/REFL_XHI;
    ctx.fillStyle='#0d1322'; ctx.fillRect(XL,b.y,b.x1-XL,b.h);
    axesT(ctx,b,0,REFL_XHI,ylo,yhi,{title:titleFor(b,TITLES[e][0]+(isFinite(R.r)?'  (r = '+fmt(R.r,3)+')':''),TITLES[e][1]),
      xticks:last?undefined:[],yticks:[-2*A,-A,0,A,2*A].filter(v=>Math.abs(v)<=2.3*A),yfmt:v=>fmt(v,2),xlab:last?'x, cm (the string ends at 7.5 cm; shaded: the mirror world)':undefined,ylab:k===1?'y, cm':undefined});
    ctx.save(); ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(XL,b.y); ctx.lineTo(XL,b.y1); ctx.strokeStyle=COL.live; ctx.lineWidth=1.2; ctx.stroke(); ctx.restore();
    polyline(ctx,b,C.xs,C.inc,0,REFL_XHI,ylo,yhi,COL.ref,1.1,[6,4]);
    if(e!=='none') polyline(ctx,b,C.xs,C.ref,0,REFL_XHI,ylo,yhi,COL.ref,1.1,[2,3]);
    /* the exact sum lies exactly under the lattice, so it is drawn as an opaque orange halo round it */
    polyline(ctx,b,C.xs,C.sum,0,REFL_XHI,ylo,yhi,shade(COL.ref,0.55),6);
    const L=M.lats[e], xs=[], ys=[]; for(let i=0;i<=NSEG;i++){ xs.push(i*DX); ys.push(L.cur[i]); }
    polyline(ctx,b,xs,ys,0,REFL_XHI,ylo,yhi,COL.pos,1.6);
    const r=Math.max(1.6,Math.min(3.2,b.w/REFL_XHI*DX*0.36));
    ctx.beginPath(); for(let i=0;i<=NSEG;i++){ const X=b.x+b.w*xs[i]/REFL_XHI, Y=b.y1-b.h*(ys[i]-ylo)/(yhi-ylo); if(Y>=b.y&&Y<=b.y1){ ctx.moveTo(X+r,Y); ctx.arc(X,Y,r,0,TAU); } }
    ctx.fillStyle=COL.pos; ctx.fill();
  });
  const b0=G.strips[0], sx=b0.w/REFL_XHI, sy=b0.h/(yhi-ylo);
  lab(ctx,W,H,b0.x1-4,b0.y-9,'step '+M.n+' of '+M.loop+'   vertical ×'+sigf(sy/sx,2),COL.dim,SM_FONT,'right','bottom');
  caption(ctx,b0.x,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  view 4: the standing waves — the response sweep and the build-up   *
 * ================================================================== */
const STAND_CAP_FULL='Top: how hard the string answers the oscillator — the largest steady amplitude anywhere on it, over the driving amplitude A, against '
  +'the frequency (log scale). Green is this damping, exactly; dashed orange is no damping, which diverges at every resonance fₙ (cyan ticks). '
  +'Drag across the top panel to set f. Bottom: the lattice driven from rest at f (green) growing into the exact steady state, whose envelope '
  +'±|Yᵢ| is orange; the vertical scale is stretched by the printed factor.';
const STAND_CAP_SHORT='Top: the steady response against f (drag to set f). Bottom: the string from rest (green) inside the exact envelope (orange).';
function standGeo(ctx,W,H){
  const narrow=isNarrow(W), left=64, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,STAND_CAP_FULL,STAND_CAP_SHORT,capW,stageTop()+30+260);
  const top=stageTop()+34, avail=fit.capY-top-44, gap=58;
  const th=Math.max(60,Math.floor((avail-gap)*0.46));
  return {fit,tb:box(left,top+14,right-left,th),bb:box(left,top+14+th+gap,right-left,Math.max(50,avail-th-gap-14)),narrow};
}
function freqAt(tb,x){ return Math.round(clamp((x-tb.x)/tb.w,0,1)*FMAX*100)/100; }
function drawStand(ctx,W,H,M){
  const st=M.st, G=standGeo(ctx,W,H), tb=G.tb, bb=G.bb, R=M.resp;
  let pk=1; for(const g of R.gb) if(isFinite(g)) pk=Math.max(pk,g);
  const ly1=Math.log10(Math.min(1000,Math.max(3,1.6*pk))), ly0=Math.log10(0.5);
  const yt=[0,1,2,3].filter(v=>v<=ly1+1e-9);
  axesT(ctx,tb,0,FMAX,ly0,ly1,{title:titleFor(tb,'the steady response: largest |Y| on the string over A, against the driving frequency','largest |Y|/A against f'),
    xlab:'driving frequency f, Hz',ylab:'|Y|max / A',yticks:yt,yfmt:v=>String(Math.round(Math.pow(10,v)))});
  const lg=a=>a.map(g=>isFinite(g)&&g>0?Math.log10(g):NaN);
  polyline(ctx,tb,R.fs,lg(R.gb),0,FMAX,ly0,ly1,COL.pos,1.7);
  polyline(ctx,tb,R.fs,lg(R.g0),0,FMAX,ly0,ly1,COL.ref,1.1,[5,4]);
  if(!R.fn.length) lab(ctx,W,H,tb.x+tb.w/2,tb.y+tb.h*0.35,'no end: nothing comes back to pile up, so there are no resonances — the response is flat at A',COL.dim,LAB_FONT,'center','middle');
  ctx.beginPath();
  for(const f of R.fn){ const X=tb.x+tb.w*f/FMAX; ctx.moveTo(X,tb.y); ctx.lineTo(X,tb.y+8); }
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.4; ctx.stroke();
  R.fn.forEach((f,k)=>{ if(R.fn.length<=12||k%2===0) lab(ctx,W,H,tb.x+tb.w*f/FMAX,tb.y+10,String(k+1),COL.struct,SM_FONT,'center','top'); });
  const Xf=tb.x+tb.w*st.freq/FMAX, gA=M.Smax/Math.max(st.amp,1e-300);
  ctx.save(); ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(Xf,tb.y); ctx.lineTo(Xf,tb.y1); ctx.strokeStyle=rgba(COL.live,0.7); ctx.lineWidth=1; ctx.stroke(); ctx.restore();
  if(st.amp>0&&isFinite(gA)) marker(ctx,tb,0,FMAX,ly0,ly1,st.freq,Math.log10(Math.max(gA,1)),COL.live);
  /* the string */
  const ym=Math.max(0.05,1.15*Math.max(M.Smax,M.latMax));
  axesT(ctx,bb,0,LSTR,-ym,ym,{title:titleFor(bb,'the string at '+fmt(st.freq,2)+' Hz: the lattice from rest inside the exact envelope','the string at '+fmt(st.freq,2)+' Hz'),
    xlab:'x, cm',ylab:'y, cm',yticks:sparseTicks(-ym,ym,bb.h)});
  const xs=[], up=[], dn=[], ys=[]; for(let i=0;i<=NSEG;i++){ xs.push(i*DX); up.push(M.env[i]); dn.push(-M.env[i]); ys.push(M.y[i]); }
  ctx.beginPath();
  for(let i=0;i<=NSEG;i++){ const X=bb.x+bb.w*xs[i]/LSTR, Y=bb.y1-bb.h*(clamp(up[i],-ym,ym)+ym)/(2*ym); if(i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); }
  for(let i=NSEG;i>=0;i--){ const X=bb.x+bb.w*xs[i]/LSTR, Y=bb.y1-bb.h*(clamp(dn[i],-ym,ym)+ym)/(2*ym); ctx.lineTo(X,Y); }
  ctx.closePath(); ctx.fillStyle=rgba(COL.ref,0.1); ctx.fill();
  polyline(ctx,bb,xs,up,0,LSTR,-ym,ym,COL.ref,1.2); polyline(ctx,bb,xs,dn,0,LSTR,-ym,ym,COL.ref,1.2);
  polyline(ctx,bb,xs,ys,0,LSTR,-ym,ym,COL.pos,1.6);
  { const r=Math.max(1.6,Math.min(3.2,bb.w/LSTR*DX*0.36)); ctx.beginPath();
    for(let i=0;i<=NSEG;i++){ const X=bb.x+bb.w*xs[i]/LSTR, Y=bb.y1-bb.h*(ys[i]+ym)/(2*ym); if(Y>=bb.y&&Y<=bb.y1){ ctx.moveTo(X+r,Y); ctx.arc(X,Y,r,0,TAU); } }
    ctx.fillStyle=COL.pos; ctx.fill(); }
  ctx.beginPath();
  for(const i of M.nodes){ const X=bb.x+bb.w*i*DX/LSTR, Y=bb.y1-bb.h*0.5; ctx.moveTo(X,Y-6); ctx.lineTo(X,Y+6); }
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.6; ctx.stroke();
  const sx=bb.w/LSTR, sy=bb.h/(2*ym);
  lab(ctx,W,H,bb.x1-4,bb.y-9,'vertical ×'+sigf(sy/sx,2)+'   step '+M.n+' from rest',COL.dim,SM_FONT,'right','bottom');
  if(!(M.b>0)) lab(ctx,W,H,bb.x+6,bb.y+6,'no damping: nothing takes energy out, so at a resonance the amplitude grows without end',COL.ref,SM_FONT,'left','top');
  caption(ctx,tb.x,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  view 5: the dispersion — the lattice, the continuum, a bead chain  *
 * ================================================================== */
const DISP_CAP_FULL='Left: frequency against wavenumber across the whole zone (kΔx from 0 to π: two beads a wavelength at the edge). Orange dashed is the '
  +'continuous string, ω = vk. Green is the lattice at Courant number α = vΔt/Δx (PhET runs at α = 1, on the orange line). Violet is a '
  +'real chain of beads on springs, ω = (2v/Δx) sin(kΔx/2), the α → 0 limit. Right: phase (dashed) and group (solid) speed over v. '
  +'Bottom: one triangular pulse after 5.4 cm on each; only the α = 1 lattice keeps its shape.';
const DISP_CAP_NARROW='Top: frequency against wavenumber across the zone. Orange dashed is the continuous string, ω = vk; green is the lattice at Courant '
  +'number α (PhET’s α = 1 lies on the orange line); violet is a real bead chain, the α → 0 limit. Bottom: one triangular pulse after '
  +'5.4 cm on each; only the α = 1 lattice keeps its shape. (The speeds panel needs a wider window.)';
const DISP_CAP_SHORT='ω(k): continuum (orange), the lattice at α (green; PhET’s α = 1 is exact), a bead chain (violet); below, the pulse after 5.4 cm.';
function dispGeo(ctx,W,H){
  const narrow=isNarrow(W), left=64, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,narrow?DISP_CAP_NARROW:DISP_CAP_FULL,DISP_CAP_SHORT,capW,stageTop()+30+280);
  const top=stageTop()+34, avail=fit.capY-top-44, gapV=58, gapH=74;
  const th=Math.max(70,Math.floor((avail-gapV)*0.55)), span=right-left;
  if(narrow) return {fit,narrow,wb:box(left,top+14,span,th),sb:null,pb:box(left,top+14+th+gapV,span,Math.max(50,avail-th-gapV-14))};
  const w1=Math.floor((span-gapH)*0.55);
  return {fit,narrow,wb:box(left,top+14,w1,th),sb:box(left+w1+gapH,top+14,span-w1-gapH,th),pb:box(left,top+14+th+gapV,span,Math.max(50,avail-th-gapV-14))};
}
function drawDisp(ctx,W,H,M){
  const D=M.D, st=M.st, G=dispGeo(ctx,W,H), wb=G.wb, sb=G.sb, pb=G.pb, PI1=Math.PI;
  axesT(ctx,wb,0,PI1,0,PI1*1.04,{title:titleFor(wb,'ωΔx/v against kΔx, the whole zone','ω(k)'),xlab:'kΔx, rad per bead',ylab:'ωΔx / v',
    xticks:[0,0.5,1,1.5,2,2.5,3],yticks:[0,1,2,3]});
  polyline(ctx,wb,D.K,D.chain,0,PI1,0,PI1*1.04,COL.chain,1.6);
  polyline(ctx,wb,D.K,D.om,0,PI1,0,PI1*1.04,COL.pos,1.8);
  polyline(ctx,wb,D.K,D.cont,0,PI1,0,PI1*1.04,COL.ref,1.3,[6,4]);      /* on top: at a = 1 it lies ON the green */
  if(isFinite(D.kOsc)) marker(ctx,wb,0,PI1,0,PI1*1.04,D.kOsc,omegaNorm(D.kOsc,D.a,D.ba),COL.live);
  legendAuto(ctx,wb,[[COL.pos,'lattice, α = '+fmt(D.a,2)],[COL.ref,'continuum, ω = vk'],[COL.chain,'bead chain (α → 0)'],[COL.live,'the oscillator, '+fmt(st.freq,2)+' Hz']]);
  if(sb){
    axesT(ctx,sb,0,PI1,0,1.15,{title:titleFor(sb,'phase and group speed over v','speeds / v'),xlab:'kΔx',ylab:'speed / v',xticks:[0,1,2,3],yticks:[0,0.25,0.5,0.75,1],yfmt:v=>fmt(v,2)});
    const vpc=D.K.map(k=>k>0?2*Math.sin(k/2)/k:1);
    polyline(ctx,sb,D.K,vpc,0,PI1,0,1.15,COL.chain,1.2,[4,3]);
    polyline(ctx,sb,D.K,D.vgChain,0,PI1,0,1.15,COL.chain,1.6);
    polyline(ctx,sb,D.K,D.vp,0,PI1,0,1.15,COL.pos,1.2,[4,3]);
    polyline(ctx,sb,D.K,D.vg,0,PI1,0,1.15,COL.pos,1.8);
    polyline(ctx,sb,[0,PI1],[1,1],0,PI1,0,1.15,COL.ref,1.2,[6,4]);
  }
  const Ap=Math.max(st.amp,0.05), plo=-0.4*Ap, phi=1.18*Ap, xs=[];
  for(let i=0;i<=NSEG;i++) xs.push(i*DX);
  axesT(ctx,pb,0,LSTR,plo,phi,{title:titleFor(pb,'one pulse, undamped, after its centre has run '+fmt(D.xcen,2)+' cm, on each','the pulse after '+fmt(D.xcen,2)+' cm'),
    xlab:'x, cm',ylab:'y, cm',yticks:sparseTicks(plo,phi,pb.h)});
  const xf=[], yf=[]; for(let k=0;k<=600;k++){ const x=LSTR*k/600; xf.push(x); yf.push(st.amp*tri((D.P.t-x/D.v)/st.pw)); }
  polyline(ctx,pb,xs,D.Pc.y.slice(0,NSEG+1),0,LSTR,plo,phi,COL.chain,1.6);
  polyline(ctx,pb,xs,D.P.y.slice(0,NSEG+1),0,LSTR,plo,phi,COL.pos,1.7);
  polyline(ctx,pb,xf,yf,0,LSTR,plo,phi,COL.ref,1.2,[5,4]);             /* on top, dashed: at a = 1 the lattice is under it */
  const r=2.2;
  ctx.beginPath(); for(let i=0;i<=NSEG;i++){ const X=pb.x+pb.w*xs[i]/LSTR, Y=pb.y1-pb.h*(D.P.y[i]-plo)/(phi-plo); if(Y>=pb.y&&Y<=pb.y1){ ctx.moveTo(X+r,Y); ctx.arc(X,Y,r,0,TAU); } }
  ctx.fillStyle=COL.pos; ctx.fill();
  legendAuto(ctx,pb,[[COL.ref,'exact: the triangle moved at v (dashed)'],[COL.pos,'the lattice at α = '+fmt(D.a,2)],[COL.chain,'the bead chain']]);
  caption(ctx,wb.x,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='str') drawStr(ctx,W,H,M);
  else if(M.view==='xt') drawXT(ctx,W,H,M);
  else if(M.view==='refl') drawRefl(ctx,W,H,M);
  else if(M.view==='stand') drawStand(ctx,W,H,M);
  else drawDisp(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of dtWall seconds: the live string in views 1-2, each demo in its own view */
  S.step=function(dtWall){
    if(!ST.running) return false;
    const dts=(dtWall||0)*simFactor(ST);
    if(!(dts>0)) return false;
    const v=ST.view;
    if(v==='str'||v==='xt'){ liveAdvance(ST,dts); return true; }
    if(v==='refl') return reflAdvance(ST,dts)>0;
    if(v==='stand'){ standAdvance(ST,dts); return true; }
    return false;
  };
  /* the pointer: the wrench, the pulse generator and PhET's three tools on the string;
     the frequency on the standing waves' response panel */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const ctx=canvas.getContext('2d');
    if(ST.view==='str'){
      const G=strGeo(ctx,S.W,S.H,buildModel()), map=G.map, wx=map.wx(x), wy=map.wy(y), l=G.lim;
      if(type==='down'){
        if(ST.stopwatch){ const r=swRect(map,ST,S.W,S.H); if(x>=r.x&&x<=r.x+r.w&&y>=r.y&&y<=r.y+r.h){ DRAG.what='sw'; DRAG.ox=x-r.x; DRAG.oy=y-r.y; return true; } }
        if(ST.rulers){
          if(inRect(wx,wy,rulerVRect(ST))){ DRAG.what='rv'; DRAG.ox=ST.rvX-wx; DRAG.oy=ST.rvY-wy; return true; }
          if(inRect(wx,wy,rulerHRect(ST))){ DRAG.what='rh'; DRAG.ox=ST.rhX-wx; DRAG.oy=ST.rhY-wy; return true; }
        }
        if(ST.refline&&Math.abs(y-map.Y(ST.refY))<=7&&wx>=-0.6&&wx<=LSTR+0.4){ DRAG.what='ref'; DRAG.oy=ST.refY-wy; return true; }
        if(ST.mode==='manual'&&inRect(wx,wy,wrenchRect(LIVE.wr))){ DRAG.what='wrench'; DRAG.oy=LIVE.wr-wy; LIVE.arrows=false; return true; }
        if(ST.mode==='pulse'&&inRect(wx,wy,GEN_RECT)){ const sent=sendPulse(ST); if(sent) ST.running=true; return sent; }
        return false;
      }
      if(type==='move'){
        if(DRAG.what==='wrench'){ LIVE.wr=clamp(wy+DRAG.oy,-AMAX,AMAX); ST.running=true; return true; }   /* PhET: the wrench also presses play */
        if(DRAG.what==='rh'){ ST.rhX=clamp(wx+DRAG.ox,l[0]-RULER_H+0.6,l[1]-0.6); ST.rhY=clamp(wy+DRAG.oy,l[2]+0.5,l[3]); return true; }
        if(DRAG.what==='rv'){ ST.rvX=clamp(wx+DRAG.ox,l[0],l[1]-0.5); ST.rvY=clamp(wy+DRAG.oy,l[2]-RULER_V+0.6,l[3]-0.6); return true; }
        if(DRAG.what==='ref'){ ST.refY=clamp(wy+DRAG.oy,l[2]+0.05,l[3]-0.05); return true; }
        if(DRAG.what==='sw'){ ST.swX=map.wx(clamp(x-DRAG.ox,0,S.W-SW_W)); ST.swY=map.wy(clamp(y-DRAG.oy,0,S.H-SW_H)); return true; }
      }
      return false;
    }
    if(ST.view==='stand'){
      const tb=standGeo(ctx,S.W,S.H).tb;
      if(type==='down'){ if(x>=tb.x&&x<=tb.x1&&y>=tb.y&&y<=tb.y1){ DRAG.what='freq'; ST.freq=freqAt(tb,x); return true; } return false; }
      if(type==='move'&&DRAG.what==='freq'){ ST.freq=freqAt(tb,x); return true; }
    }
    return false;
  };
  return S;
}
