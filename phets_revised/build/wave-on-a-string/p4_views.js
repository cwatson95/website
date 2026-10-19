
/* ================================================================== *
 *  view 1: the string — PhET's screen, drawn at true aspect           *
 * ================================================================== */
const STR_EXT={xmin:-2.62,xmax:8.35,ymin:-YHALF,ymax:YHALF};   /* the left margin holds the vertical ruler clear of the driver */
const SW_W=128, SW_H=48;                 /* the stopwatch, px */
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it */
const HINT_H=18;
/* tick labels follow the tick SPACING, not a fixed decimal count (Known-bad: fmt(t,2)
   prints 318.00 whatever the range, and six of those do not fit a narrow panel) */
function tickFmt(ticks){
  let g=Infinity; for(let i=1;i<ticks.length;i++) g=Math.min(g,Math.abs(ticks[i]-ticks[i-1]));
  if(!isFinite(g)||g<=0) return v=>sigf(v,3);
  let d=0; while(d<6&&Math.abs(Math.round(g*Math.pow(10,d))-g*Math.pow(10,d))>1e-6*Math.max(1,g*Math.pow(10,d))) d++;
  return v=>fmt(Math.abs(v)<1e-12?0:v,d);
}
function axesT(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=Object.assign({},opt||{});
  if(o.xticks===undefined) o.xticks=ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  if(o.yticks===undefined) o.yticks=ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||5);
  if(!o.xfmt) o.xfmt=tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt=tickFmt(o.yticks);
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
}
function mapLim(map,b){ return [map.wx(b.x),map.wx(b.x1),map.wy(b.y1),map.wy(b.y)]; }
function inLim(x,y,l){ return x>=l[0]&&x<=l[1]&&y>=l[2]&&y<=l[3]; }
function beadR(s){ return Math.max(2.2,0.0625*s*0.92); }   /* PhET's bead radius is 5 model units = 0.0625 cm */

function strCaption(M,sTxt){
  const st=M.st;
  const mode={manual:'Drag the wrench up and down (or use the arrow keys) and a kink runs down the string.',
              osc:'The oscillator’s pin goes round at f; the yoke turns its circle into A sin 2πft at bead 0.',
              pulse:'Click the generator (or press p) for one triangular pulse, A high and w long.'}[st.mode];
  const end={fixed:'The clamp holds bead 60 at zero, so every reflection comes back inverted.',
             loose:'The ring slides on its pole, so reflections come back upright (about bead 59½).',
             none:'Past bead 60 the string runs on out of the window and nothing comes back.'}[st.end];
  return {full:'True aspect: 1 cm = '+sTxt+' px on both axes. 61 beads 1.25 mm apart make 7.5 cm of string; every tenth bead is magenta. '+mode+' '+end,
          short:'True aspect, 1 cm = '+sTxt+' px. '+mode};
}
function strGeo(ctx,W,H,M){
  const narrow=isNarrow(W), left=18, right=narrow?W-18:W-RO_W-40;
  const ph=strCaption(M,'000');
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,ph.full,ph.short,capW,stageTop()+30+180);
  const top=stageTop()+30, b=box(left,top,right-left,Math.max(120,fit.capY-12-top));
  const map=worldFitUp(b,STR_EXT,0);
  return {b,map,fit,full:fit.txt===ph.full,narrow,lim:mapLim(map,b)};
}
/* hit rectangles, world cm (the stopwatch is a pixel box anchored in the world) */
function wrenchRect(y0){ return [-1.5,0.28,y0-0.34,y0+0.34]; }
const GEN_RECT=[-1.5,-0.3,-0.5,0.5];
function rulerHRect(st){ return [st.rhX-0.12,st.rhX+RULER_H+0.12,st.rhY-0.5,st.rhY]; }
function rulerVRect(st){ return [st.rvX,st.rvX+0.5,st.rvY-0.12,st.rvY+RULER_V+0.12]; }
function swRect(map,st,W,H){ return {x:clamp(map.X(st.swX),0,W-SW_W),y:clamp(map.Y(st.swY),0,H-SW_H),w:SW_W,h:SW_H}; }
function inRect(x,y,r){ return x>=r[0]&&x<=r[1]&&y>=r[2]&&y<=r[3]; }

function drawStr(ctx,W,H,M){
  const st=M.st, G=strGeo(ctx,W,H,M), map=G.map, s=map.s, lim=G.lim, X=map.X, Y=map.Y;
  /* the equilibrium line */
  ctx.save(); ctx.setLineDash([4,5]); ctx.strokeStyle='#2a3142'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(X(0),Y(0)); ctx.lineTo(X(st.end==='none'?LSTR+0.66:LSTR),Y(0)); ctx.stroke(); ctx.restore();
  if(st.stopwatch){ const r=swRect(map,st,W,H); LABELS.push([r.x,r.y,r.x+r.w,r.y+r.h]); }   /* labels dodge the stopwatch */
  if(st.refline) drawRefLine(ctx,W,H,map,st);
  drawFarEnd(ctx,W,H,map,M,G);
  const xs=[], ys=[]; for(let i=0;i<=NSEG;i++){ xs.push(i*DX); ys.push(M.y[i]); }
  polyline(ctx,G.b,xs,ys,lim[0],lim[1],lim[2],lim[3],COL.pos,1.5);
  drawBeads(ctx,map,xs,ys,beadR(s),lim);
  drawDriver(ctx,W,H,map,M,lim);
  if(st.rulers){ drawRulerV(ctx,map,st.rvX,st.rvY,H); drawRulerH(ctx,map,st.rhX,st.rhY,W); }
  if(st.stopwatch) drawStopwatch(ctx,W,H,map,M);
  if(M.offScale) lab(ctx,W,H,G.b.x+6,G.b.y+6,'The string leaves the view: |y| = '+fmt(M.maxAbs,2)+' cm at bead '+M.maxAt+'; the view shows ±'+fmt(YHALF,1)+' cm.',COL.ref,LAB_FONT,'left','top');
  const cap=strCaption(M,fmt(s,0));
  caption(ctx,G.b.x,G.fit.capY,G.full?cap.full:cap.short,G.fit.capW,'#767e92',CAP_FONT);
}
function drawBeads(ctx,map,xs,ys,r,lim){
  for(const pass of [0,1]){
    ctx.beginPath(); let any=false;
    for(let i=0;i<xs.length;i++){
      if((i%10===0)!==(pass===1)||!inLim(xs[i],ys[i],lim)) continue;
      const X=map.X(xs[i]), Y=map.Y(ys[i]); ctx.moveTo(X+r,Y); ctx.arc(X,Y,r,0,TAU); any=true;
    }
    if(!any) continue;
    ctx.fillStyle=pass?COL.live:COL.pos; ctx.fill();
    ctx.strokeStyle=pass?'#5e1a5a':COL.bead2; ctx.lineWidth=0.8; ctx.stroke();
  }
}
function drawFarEnd(ctx,W,H,map,M,G){
  const st=M.st, X=map.X, Y=map.Y, s=map.s, xe=LSTR, yN=M.y[NSEG];
  if(st.end==='fixed'){
    const x0=X(xe)+beadR(s)*0.6, x1=X(xe+0.38), y0=Y(0.34), y1=Y(-0.34);
    ctx.fillStyle='#232a38'; ctx.fillRect(x0,y0,x1-x0,y1-y0);
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.strokeRect(x0,y0,x1-x0,y1-y0);
    ctx.beginPath(); for(let k=1;k<5;k++){ const yy=y0+(y1-y0)*k/5; ctx.moveTo(x0+2,yy); ctx.lineTo(x1-2,yy+(y1-y0)/10); }
    ctx.strokeStyle='#3d6f7e'; ctx.lineWidth=1; ctx.stroke();
  } else if(st.end==='loose'){
    const Xp=X(xe);
    ctx.beginPath(); ctx.moveTo(Xp,Y(-YHALF+0.3)); ctx.lineTo(Xp,Y(YHALF-0.3));
    ctx.strokeStyle=COL.struct; ctx.lineWidth=Math.max(2,0.05*s); ctx.stroke();
    ctx.fillStyle='#232a38'; ctx.fillRect(Xp-0.22*s,Y(-YHALF+0.3),0.44*s,0.12*s);
    if(Math.abs(yN)<=YHALF-0.2){
      ctx.beginPath(); ctx.arc(Xp,Y(yN),0.15*s,0,TAU);
      ctx.strokeStyle='#e9e9f0'; ctx.lineWidth=Math.max(1.6,0.035*s); ctx.stroke();
    }
  } else {
    /* the window: the string runs on and out; a fading, dotted continuation */
    const x0=X(xe+0.08), x1=X(xe+0.7), y0=Y(1.7), y1=Y(-1.7);
    ctx.save(); ctx.setLineDash([3,4]); ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.strokeRect(x0,y0,x1-x0,y1-y0); ctx.restore();
    const slope=(M.y[NSEG]-M.y[NSEG-1])/DX;
    for(let k=1;k<=5;k++){
      const xx=xe+k*0.11, yy=yN+slope*k*0.11;
      if(!inLim(xx,yy,G.lim)) continue;
      dot(ctx,X(xx),Y(yy),Math.max(1.2,beadR(s)*(1-k*0.13)),mix('#070b18',COL.pos,1-k*0.16),null);
    }
  }
}
function drawDriver(ctx,W,H,map,M,lim){
  const st=M.st, X=map.X, Y=map.Y, s=map.s, y0=M.y[0];
  if(st.mode==='manual'){
    const yc=clamp(y0,-AMAX,AMAX);
    ctx.fillStyle='#454b5a'; ctx.fillRect(X(-1.42),Y(yc+0.11),0.5*s,0.22*s);
    ctx.fillStyle='#6b7285'; ctx.fillRect(X(-0.92),Y(yc+0.09),0.74*s,0.18*s);
    ctx.strokeStyle='#aeb6c6'; ctx.lineWidth=1; ctx.strokeRect(X(-1.42),Y(yc+0.11),1.24*s,0.22*s);
    ctx.beginPath(); ctx.arc(X(0),Y(yc),0.18*s,0,TAU); ctx.strokeStyle='#c8ccd6'; ctx.lineWidth=Math.max(2,0.05*s); ctx.stroke();
    if(LIVE.arrows){ arrowW(ctx,map,[-0.8,yc+0.28],[0,0.5],COL.struct,2); arrowW(ctx,map,[-0.8,yc-0.28],[0,-0.5],COL.struct,2); }
  } else if(st.mode==='osc'){
    const xc=-0.95, A=st.amp, Rd=Math.max(0.3,A+0.12), ph=M.phaseNow;
    ctx.beginPath(); ctx.arc(X(xc),Y(0),Rd*s,0,TAU); ctx.fillStyle='#161c2c'; ctx.fill();
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.3; ctx.stroke();
    if(A>0.02){ ctx.save(); ctx.setLineDash([2,4]); ctx.beginPath(); ctx.arc(X(xc),Y(0),A*s,0,TAU); ctx.strokeStyle='#3a4152'; ctx.lineWidth=1; ctx.stroke(); ctx.restore(); }
    /* the scotch yoke: a rigid bar at the pin's height carries bead 0 */
    ctx.beginPath(); ctx.moveTo(X(xc-Rd-0.08),Y(y0)); ctx.lineTo(X(0),Y(y0)); ctx.strokeStyle='#8b93a6'; ctx.lineWidth=Math.max(2.5,0.06*s); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(X(-0.08),Y(-YHALF+0.5)); ctx.lineTo(X(-0.08),Y(YHALF-0.5)); ctx.strokeStyle='#2c4f5a'; ctx.lineWidth=1.2; ctx.stroke();
    dot(ctx,X(xc+A*Math.cos(ph)),Y(A*Math.sin(ph)),Math.max(3,0.07*s),COL.live,'#fff',1);
  } else {
    const r=GEN_RECT;
    ctx.fillStyle='#161c2c'; ctx.fillRect(X(r[0]),Y(r[3]),(r[1]-r[0])*s,(r[3]-r[2])*s);
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.strokeRect(X(r[0]),Y(r[3]),(r[1]-r[0])*s,(r[3]-r[2])*s);
    dot(ctx,X(-0.9),Y(0.05),Math.max(6,0.22*s),M.pulseOn?COL.live:COL.pos,'#e9e9f0',1.2);
    ctx.beginPath(); const gx=X(-0.9), gy=Y(0.05), gs=Math.max(3,0.1*s);
    ctx.moveTo(gx-gs,gy+gs*0.5); ctx.lineTo(gx,gy-gs*0.7); ctx.lineTo(gx+gs,gy+gs*0.5);
    ctx.strokeStyle='#10131b'; ctx.lineWidth=1.6; ctx.stroke();
    lab(ctx,W,H,X(-0.9),Y(-0.62),M.pulseOn?'sending':'pulse',M.pulseOn?COL.live:'#8b93a6',SM_FONT,'center','top');
    ctx.beginPath(); ctx.moveTo(X(-0.12),Y(-YHALF+0.5)); ctx.lineTo(X(-0.12),Y(YHALF-0.5)); ctx.strokeStyle='#2c4f5a'; ctx.lineWidth=1.2; ctx.stroke();
    ctx.fillStyle='#8b93a6'; ctx.fillRect(X(-0.2),Y(y0+0.07),0.2*s,0.14*s);
  }
}
function drawRulerH(ctx,map,x0,yTop,W){
  const s=map.s, X0=map.X(x0), Y0=map.Y(yTop), pad=0.12*s;
  ctx.fillStyle='rgba(18,22,31,0.9)'; ctx.fillRect(X0-pad,Y0,RULER_H*s+2*pad,0.5*s);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.strokeRect(X0-pad,Y0,RULER_H*s+2*pad,0.5*s);
  ctx.beginPath();
  for(let k=0;k<=RULER_H*10;k++){ const Xk=X0+k*0.1*s, l=(k%10===0?0.2:k%5===0?0.13:0.08)*s; ctx.moveTo(Xk,Y0); ctx.lineTo(Xk,Y0+l); }
  ctx.strokeStyle='#aeb6c6'; ctx.lineWidth=0.8; ctx.stroke();
  ctx.fillStyle='#cfd4de'; ctx.font='10px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='top';
  for(let c=0;c<=RULER_H;c++){ const Xc=X0+c*s; if(Xc>6&&Xc<W-6) ctx.fillText(String(c),Xc,Y0+0.22*s); }
  ctx.textAlign='left'; if(X0>0&&X0+40<W) ctx.fillText('cm',X0+Math.max(8,0.12*s),Y0+0.22*s);
}
function drawRulerV(ctx,map,xLeft,y0,H){
  const s=map.s, X0=map.X(xLeft), Yb=map.Y(y0), pad=0.12*s, x1=X0+0.5*s;
  ctx.fillStyle='rgba(18,22,31,0.9)'; ctx.fillRect(X0,Yb-RULER_V*s-pad,0.5*s,RULER_V*s+2*pad);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.strokeRect(X0,Yb-RULER_V*s-pad,0.5*s,RULER_V*s+2*pad);
  ctx.beginPath();
  for(let k=0;k<=RULER_V*10;k++){ const Yk=Yb-k*0.1*s, l=(k%10===0?0.2:k%5===0?0.13:0.08)*s; ctx.moveTo(x1,Yk); ctx.lineTo(x1-l,Yk); }
  ctx.strokeStyle='#aeb6c6'; ctx.lineWidth=0.8; ctx.stroke();
  ctx.fillStyle='#cfd4de'; ctx.font='10px -apple-system, sans-serif'; ctx.textAlign='left'; ctx.textBaseline='middle';
  for(let c=0;c<=RULER_V;c++){ const Yc=Yb-c*s-(c===0?0.08*s:0); if(Yc>6&&Yc<H-6) ctx.fillText(String(c),X0+0.06*s,Yc); }
}
function drawStopwatch(ctx,W,H,map,M){
  const r=swRect(map,M.st,W,H);
  ctx.fillStyle='#10131b'; ctx.fillRect(r.x,r.y,r.w,r.h);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.strokeRect(r.x,r.y,r.w,r.h);
  ctx.fillStyle='#8b93a6'; ctx.font='10px -apple-system, sans-serif'; ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillText('stopwatch',r.x+8,r.y+6);
  ctx.fillStyle='#e9e9f0'; ctx.font='italic 18px Georgia, serif'; ctx.fillText(fmt(M.sw,2)+' s',r.x+8,r.y+21);
  if(M.swOn) dot(ctx,r.x+r.w-12,r.y+12,4,COL.live,null);
}
function drawRefLine(ctx,W,H,map,st){
  const Yr=map.Y(st.refY), X0=map.X(-0.3), X1=map.X(LSTR+0.35);
  ctx.save(); ctx.setLineDash([7,5]); ctx.beginPath(); ctx.moveTo(X0,Yr); ctx.lineTo(X1,Yr);
  ctx.strokeStyle=COL.ref; ctx.lineWidth=1.4; ctx.stroke(); ctx.restore();
  ctx.fillStyle=COL.ref; ctx.fillRect(X0-9,Yr-4.5,9,9);
  lab(ctx,W,H,map.X(0.15),Yr-9,'reference line, '+fmt(st.refY,2)+' cm',COL.ref,SM_FONT,'left','bottom');
}

/* ================================================================== *
 *  view 2: the space-time — the string's recent past, t running up    *
 * ================================================================== */
const XT_CAP_FULL='Each row is one lattice step of the string you are driving (up to the last '+HMAX+'), newest at the top: green is up, cyan is down, '
  +'brighter is further from rest. A wave is a stripe whose tilt is set by v; the dashed orange lines are x ± vt = constant at the current speed, and every '
  +'stripe follows one. At the clamp a green stripe comes back cyan (inverted); at the ring it keeps its colour; with no end it simply leaves.';
const XT_CAP_SHORT='The string’s last '+HMAX+' steps, newest at the top: green up, cyan down. Stripes run along x ± vt (dashed).';
function xtGeo(ctx,W,H){
  const narrow=isNarrow(W), left=62, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,XT_CAP_FULL,XT_CAP_SHORT,capW,stageTop()+30+240);
  const top=stageTop()+34, avail=fit.capY-44-top;
  const sh=clamp(Math.round(avail*0.2),56,120);
  return {fit,sb:box(left,top+8,right-left,sh),mb:box(left,top+8+sh+34,right-left,Math.max(60,avail-sh-42)),narrow};
}
function drawXT(ctx,W,H,M){
  const G=xtGeo(ctx,W,H), sb=G.sb, mb=G.mb, v=M.v;
  const ym=Math.max(0.5,1.15*M.hmax);
  axesT(ctx,sb,0,LSTR,-ym,ym,{title:titleFor(sb,'the string now, y against x','the string now'),ylab:'y, cm',xticks:[],yticks:sparseTicks(-ym,ym,sb.h)});
  const xs=[], ys=[]; for(let i=0;i<=NSEG;i++){ xs.push(i*DX); ys.push(M.y[i]); }
  polyline(ctx,sb,xs,ys,0,LSTR,-ym,ym,COL.pos,1.5);
  const H0=M.hist, T0=M.histT, n=H0.length;
  const span=n>1?Math.max(T0[n-1]-T0[0]+M.dt,1e-6):HMAX*M.dt;
  axesT(ctx,mb,0,LSTR,-span,0,{title:n?titleFor(mb,'the last '+n+' lattice steps, time running up','the last '+n+' steps'):'the record, empty',xlab:'x, cm (bead 0 at the left)',ylab:'t − now, s'});
  if(n===0){ lab(ctx,W,H,mb.x+mb.w/2,mb.y+mb.h/2,'nothing recorded yet: the picture fills as the string runs',COL.dim,LAB_FONT,'center','middle'); }
  else {
    const NL=12, bins=[];
    for(let j=0;j<2*NL;j++) bins.push([]);
    const tNow=T0[n-1], cw=mb.w/NSEG;
    for(let k=0;k<n;k++){
      const tHi=T0[k]-tNow, tLo=tHi-(k>0?T0[k]-T0[k-1]:M.dt);
      const yTop=mb.y+mb.h*(-tHi)/span, yBot=Math.min(mb.y1,mb.y+mb.h*(-tLo)/span);
      if(yTop>=mb.y1) continue;
      const row=H0[k];
      for(let i=0;i<=NSEG;i++){
        const u=Math.min(1,Math.abs(row[i])/(M.hmax||1)), j=Math.floor(u*NL);
        if(j<1) continue;
        const xL=Math.max(mb.x,mb.x+(i-0.5)*cw), xR=Math.min(mb.x1,mb.x+(i+0.5)*cw);
        bins[(row[i]>0?0:NL)+Math.min(j,NL)-1].push(xL,yTop,xR-xL+0.6,yBot-yTop+0.6);
      }
    }
    for(let j=0;j<2*NL;j++){
      const r=bins[j]; if(!r.length) continue;
      ctx.beginPath(); for(let q=0;q<r.length;q+=4) ctx.rect(r[q],r[q+1],r[q+2],r[q+3]);
      const lev=((j%NL)+1.5)/NL;
      ctx.fillStyle=shade(j<NL?COL.pos:COL.dn,Math.pow(Math.min(1,lev),0.7)); ctx.fill();
    }
  }
  /* the characteristics at the current speed */
  const tc=LSTR/v;
  for(let c=-span-2*tc;c<=tc;c+=tc){
    polyline(ctx,mb,[0,LSTR],[c,c+tc],0,LSTR,-span,0,rgba(COL.ref,0.8),1,[5,5]);
    polyline(ctx,mb,[LSTR,0],[c,c+tc],0,LSTR,-span,0,rgba(COL.ref,0.8),1,[5,5]);
  }
  if(n&&M.hmax>0) lab(ctx,W,H,mb.x1-4,mb.y-9,'full colour = ±'+fmt(M.hmax,2)+' cm',COL.dim,SM_FONT,'right','bottom');
  caption(ctx,mb.x,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT);
}
