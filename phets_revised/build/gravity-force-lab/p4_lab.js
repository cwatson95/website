
/* ================================================================== *
 *  the lab (shared by both sims): the track, the bodies, the force    *
 *  arrows, the distance line, the ruler, the scale row.  Everything   *
 *  it draws comes from a descriptor LS built per sim, so the drawing  *
 *  never reads the state (source: build/gravity-force-lab/p4_lab.js)  *
 * ================================================================== */
const LAB_ROW=38, RULER_H=34, RULER_INSET=8, NOTE_LH=13;
/* The house #hint (HTML: left 14 px, bottom 11 px, 11-px text) sits exactly on
   the last line of a caption that stageLayout anchors to the canvas bottom
   (capY = H - 12 - 14 lines), and the display-list capture cannot see it
   because the hint is not canvas.  Every view here lays out to H - HINT_H, and
   the layout sweep asserts no canvas text enters the hint's corner
   (phets_revised Known-bad candidate from wave-on-a-string). */
const HINT_H=18;
function stageLayoutH(ctx,W,H,capFull,capShort,nB,frac,nBN){ return stageLayout(ctx,W,H-HINT_H,capFull,capShort,nB,frac,nBN); }
/* the scale row's note at its longest (both warnings on), so the layout can
   reserve its lines before knowing which arrows are clipped */
function labNote(LS,clipped,tiny){
  let s=LS.legend.text+' (drawn to scale)   ·   '+LS.arrowText;
  if(clipped) s+='   ·   ≫ an arrow runs off the stage';
  if(tiny) s+='   ·   an arrow under a pixel is a tick';
  if(LS.legend.note) s+='   ·   '+LS.legend.note;
  return s;
}
function labGeo(ctx,W,H,LS,Lin){
  const L=Lin||stageLayoutH(ctx,W,H,LS.capFull,LS.capShort,0,0,0);
  const b=L.main, xa=LS.xL-LS.rmax-LS.pad, xb=LS.xR+LS.rmax+LS.pad, sW=b.w/(xb-xa);
  /* the note starts after the scale bar, whose longest is at the width-limited
     scale: wrap to what is left then, so the lines reserved are never too few */
  const noteW=Math.max(120,b.w-LS.legend.len*sW-12);
  const noteLines=wrapText(ctx,labNote(LS,true,true),noteW,SM_FONT).length, scaleH=NOTE_LH*noteLines+8;
  /* px that do not scale with the world: two arrow rows, the distance row (or
     the name labels alone), a view's extra row, the ruler at home, the note */
  const FX=(2*LAB_ROW+10)+(LS.dimRow?54:22)+(LS.extra||0)+(LS.ruler?RULER_H+6:0)+scaleH;
  const s=Math.min(sW,Math.max(1,(b.h-FX)/(2*LS.rmax)));
  const ox=b.x+(b.w-(xb-xa)*s)/2-xa*s;
  /* spare height: the band sits a third of the way down, not glued to the top */
  const off=Math.max(0,(b.h-FX-2*LS.rmax*s)*0.33);
  const top=b.y+off;
  /* below the largest sphere: its name (to +16), the distance line at +28, its
     label (to +49), and the ruler's home tick edge at +54 */
  const yT=top+2*LAB_ROW+10+LS.rmax*s, yBot=yT+LS.rmax*s, yDim=yBot+28;
  const X=x=>ox+x*s, Y=y=>yT-y*s;
  let ruler=null;
  if(LS.ruler){
    const R=LS.ruler, home=(LS.dimRow?yDim+26:yBot+20);
    const ryLo=yT-LS.rmax*s, ryHi=Math.max(ryLo,b.y1-scaleH-RULER_H-6);
    const ry=clamp((R.y===null||R.y===undefined)?home:Y(R.y),ryLo,ryHi);
    ruler={x0:X(R.x0)-RULER_INSET,x1:X(R.x0+R.len)+RULER_INSET,y0:ry,y1:ry+RULER_H,home,ryLo,ryHi};
  }
  return {L,b,s,ox,yT,yBot,yDim,X,Y,wx:X2=>(X2-ox)/s,wy:Y2=>(yT-Y2)/s,noteW,noteLines,
          rows:[{lab:top+LAB_ROW+10,arrow:top+LAB_ROW+28},{lab:top+10,arrow:top+28}],ruler,yScale:b.y1-8};
}
/* a force arrow on a row: length |F| / per display units; returns what was drawn */
function labArrow(ctx,G,xc,F,per,yRow,col){
  const lenPx=Math.abs(F)/per*G.s, dir=F>0?1:-1, X0=G.X(xc);
  const room=dir>0?G.b.x1-4-X0:X0-(G.b.x+4);
  const clipped=lenPx>room, Lp=Math.max(0,Math.min(lenPx,room));
  if(F===0||Lp<1.5){
    ctx.strokeStyle=col; ctx.lineWidth=1.5; ctx.beginPath(); ctx.moveTo(X0,yRow-4); ctx.lineTo(X0,yRow+4); ctx.stroke();
    return {lenPx,clipped:false,tiny:F!==0,Lp,dir,X0};
  }
  const hl=Math.min(11,Lp*0.45), hw=Math.min(7,Math.max(3,hl*0.6)), sw=2.2, X1=X0+dir*Lp;
  ctx.beginPath();
  ctx.moveTo(X0,yRow-sw/2); ctx.lineTo(X1-dir*hl,yRow-sw/2); ctx.lineTo(X1-dir*hl,yRow-hw);
  ctx.lineTo(X1,yRow); ctx.lineTo(X1-dir*hl,yRow+hw); ctx.lineTo(X1-dir*hl,yRow+sw/2); ctx.lineTo(X0,yRow+sw/2); ctx.closePath();
  ctx.fillStyle=col; ctx.fill();
  POLY_SEGS.push(X0,yRow,X1,yRow);
  if(clipped){      /* it runs off the stage: an orange double chevron where it is cut */
    ctx.strokeStyle=COL.ref; ctx.lineWidth=1.6;
    for(const o of [0,6]){ ctx.beginPath(); ctx.moveTo(X1-dir*(o+10),yRow-7); ctx.lineTo(X1-dir*(o+4),yRow); ctx.lineTo(X1-dir*(o+10),yRow+7); ctx.stroke(); }
  }
  return {lenPx,clipped,tiny:false,Lp,dir,X0};
}
/* a body: filled disc, a lighter rim, a highlight, and the centre dot PhET
   marks (or, for a charge, its sign) */
function labBody(ctx,G,bd){
  const X=G.X(bd.x), Y=G.yT, R=Math.max(1.5,bd.r*G.s);
  ctx.beginPath(); ctx.arc(X,Y,R,0,TAU); ctx.fillStyle=bd.fill; ctx.fill();
  ctx.strokeStyle=bd.rim; ctx.lineWidth=1.2; ctx.stroke();
  if(R>6){ ctx.beginPath(); ctx.arc(X-0.32*R,Y-0.32*R,0.28*R,0,TAU); ctx.fillStyle=mix(bd.fill,'#ffffff',0.35); ctx.fill(); }
  /* a charge's sign is a symbol, stroked rather than typeset: as text it would
     be a label the ruler's numbers collide with when the ruler lies across it */
  if(bd.sign&&R>7){ const a=Math.min(10,R*0.4);
    ctx.strokeStyle='#ffffff'; ctx.lineWidth=clamp(R*0.07,1.5,3.2); ctx.beginPath(); ctx.moveTo(X-a,Y); ctx.lineTo(X+a,Y);
    if(bd.sign==='+'){ ctx.moveTo(X,Y-a); ctx.lineTo(X,Y+a); } ctx.stroke(); }
  else if(!bd.sign){ ctx.beginPath(); ctx.arc(X,Y,2,0,TAU); ctx.fillStyle='#0b0e16'; ctx.fill(); }
}
/* the ruler: a translucent strip, tick edge on top, drawn over the bodies and
   cut at the stage box (a ruler slid past the track would otherwise run under
   the floating readout).  Its numbers go in the label registry, so the names
   drawn after it step around them. */
function labRuler(ctx,W,H,G,LS){
  const R=LS.ruler, g=G.ruler, b=G.b;
  const x0=Math.max(g.x0,b.x-RULER_INSET), x1=Math.min(g.x1,b.x1);
  if(x1-x0<4) return;
  ctx.fillStyle=rgba(COL.ruler,0.22); ctx.fillRect(x0,g.y0,x1-x0,RULER_H);
  ctx.strokeStyle=rgba(COL.ruler,0.85); ctx.lineWidth=1; ctx.strokeRect(x0,g.y0,x1-x0,RULER_H);
  const nMaj=Math.round(R.len/R.major);
  ctx.strokeStyle=rgba('#f2e7a8',0.9); ctx.lineWidth=1;
  ctx.beginPath();
  for(let i=0;i<=nMaj;i++) for(let j=0;j<R.minorPer&&(j===0||i<nMaj);j++){
    const X=G.X(R.x0+(i+j/R.minorPer)*R.major), len=j===0?10:5;
    if(X<x0||X>x1) continue;
    ctx.moveTo(X,g.y0); ctx.lineTo(X,g.y0+len);
  }
  ctx.stroke();
  /* numbers under the major ticks (rows 11-21 px), the unit on a row of its own (22-32 px) */
  ctx.fillStyle='#efe6b4'; ctx.font='10px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='top';
  const step=(G.s*R.major<16)?2:1;              /* thin the numbers when the ticks crowd */
  for(let i=0;i<=nMaj;i+=step){ const X=G.X(R.x0+i*R.major), w=R.labels[i].length*5.2;
    if(X-w/2<x0||X+w/2>x1) continue;
    ctx.fillText(R.labels[i],X,g.y0+11); LABELS.push([X-w/2,g.y0+11,X+w/2,g.y0+22.5]); }
  ctx.textAlign='right'; ctx.fillStyle=rgba('#efe6b4',0.75);
  const ux=x1-4, uw=R.unit.length*5.2;
  if(ux-x0>uw+30){ ctx.fillText(R.unit,ux,g.y0+22); LABELS.push([ux-uw,g.y0+22,ux,g.y0+33.5]); }
}
function drawLab(ctx,W,H,LS,Lin){
  const G=labGeo(ctx,W,H,LS,Lin), b=G.b;
  /* the track: the centre line and its two ends */
  const XL=G.X(LS.xL), XR=G.X(LS.xR);
  ctx.strokeStyle=rgba(COL.struct,0.35); ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(XL,G.yT); ctx.lineTo(XR,G.yT); ctx.stroke();
  ctx.strokeStyle=rgba(COL.struct,0.6); ctx.lineWidth=1.4;
  ctx.beginPath(); ctx.moveTo(XL,G.yT-9); ctx.lineTo(XL,G.yT+9); ctx.moveTo(XR,G.yT-9); ctx.lineTo(XR,G.yT+9); ctx.stroke();
  POLY_SEGS.push(XL,G.yT,XR,G.yT);
  if(LS.under) LS.under(ctx,G);                  /* anything a view paints under the bodies */
  /* dashed guides from each body up to its arrow row (PhET's marker lines) */
  LS.bodies.forEach((bd,k)=>{
    const X=G.X(bd.x), row=G.rows[k];
    ctx.strokeStyle=rgba(bd.rim,0.55); ctx.lineWidth=1; ctx.setLineDash([4,4]);
    ctx.beginPath(); ctx.moveTo(X,G.yT-Math.max(1.5,bd.r*G.s)-2); ctx.lineTo(X,row.arrow+6); ctx.stroke(); ctx.setLineDash([]);
  });
  /* the arrows first, then their labels, so the labels sit on top */
  const arr=LS.bodies.map((bd,k)=>labArrow(ctx,G,bd.x,LS.F[k],LS.per,G.rows[k].arrow,COL.pos));
  LS.bodies.forEach((bd,k)=>{
    const t=plain(LS.labels[k]), w=t.length*11*0.52;
    const X=clamp(G.X(bd.x),b.x+w/2+2,b.x1-w/2-2);
    lab(ctx,W,H,X,G.rows[k].lab,t,'#e4e8f0',LAB_FONT,'center');
  });
  /* the bodies, the ruler over them, then the names, which step around the ruler's numbers */
  LS.bodies.forEach(bd=>labBody(ctx,G,bd));
  if(LS.over) LS.over(ctx,G);                    /* anything a view paints over the bodies */
  if(LS.ruler) labRuler(ctx,W,H,G,LS);
  LS.bodies.forEach(bd=>lab(ctx,W,H,G.X(bd.x),G.yT+Math.max(1.5,bd.r*G.s)+10,bd.name+'  '+bd.sub,'#aeb6c6',SM_FONT,'center'));
  /* the distance between centres */
  if(LS.showDist&&LS.dimRow){
    const X1=G.X(LS.bodies[0].x), X2=G.X(LS.bodies[1].x), y=G.yDim;
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2;
    ctx.beginPath(); ctx.moveTo(X1,y); ctx.lineTo(X2,y); ctx.moveTo(X1,y-5); ctx.lineTo(X1,y+5); ctx.moveTo(X2,y-5); ctx.lineTo(X2,y+5); ctx.stroke();
    POLY_SEGS.push(X1,y,X2,y);
    lab(ctx,W,H,(X1+X2)/2,y+9,LS.distText,COL.struct,SM_FONT,'center','top');
  }
  /* the scale row: a scale bar, the arrow scale, and anything an arrow could not
     show — wrapped to the width the layout reserved lines for */
  const yS=G.yScale, Lb=LS.legend.len*G.s, x0=b.x;
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.4;
  ctx.beginPath(); ctx.moveTo(x0,yS); ctx.lineTo(x0+Lb,yS); ctx.moveTo(x0,yS-4); ctx.lineTo(x0,yS+4); ctx.moveTo(x0+Lb,yS-4); ctx.lineTo(x0+Lb,yS+4); ctx.stroke();
  const lines=wrapText(ctx,labNote(LS,arr.some(a=>a.clipped),arr.some(a=>a.tiny)),G.noteW,SM_FONT);
  ctx.fillStyle='#8b93a6'; ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='middle';
  lines.forEach((ln,i)=>ctx.fillText(ln,x0+Lb+10,yS-(lines.length-1-i)*NOTE_LH));
  drawCaption(ctx,G.L);
  return {G,arr};
}
/* what the pointer is over, topmost first: the ruler (drawn last), then a body */
function labHit(G,LS,x,y){
  const g=G.ruler;
  if(g&&x>=Math.max(g.x0,G.b.x-RULER_INSET)&&x<=Math.min(g.x1,G.b.x1)&&y>=g.y0&&y<=g.y1) return 'ruler';
  let best=null, bd=1e9;
  LS.bodies.forEach((b2,k)=>{ const d=Math.hypot(x-G.X(b2.x),y-G.yT), R=Math.max(8,b2.r*G.s)+4;
    if(d<=R&&d<bd){ bd=d; best=k+1; } });
  return best;
}

/* ================================================================== *
 *  plot helpers shared by the analysis views                         *
 * ================================================================== */
function ticks125(lo,hi){
  const out=[]; if(!(lo>0)||!(hi>0)) return out;
  for(let e=Math.floor(Math.log10(lo))-1;e<=Math.ceil(Math.log10(hi));e++)
    for(const c of [1,2,5]){ const v=c*Math.pow(10,e); if(v>=lo*0.999&&v<=hi*1.001) out.push(v); }
  return out;
}
/* a tick number as its value reads, no padding zeros ("2", "0.5", not "2.00",
   "0.50") and a true minus sign */
function tickNum(v){ if(Math.abs(v)<1e-12) return '0'; return String(+v.toPrecision(3)).replace('-','−'); }
function powLabel(v){           /* a tick value from a log axis: 10ⁿ, or c×10ⁿ */
  const e=Math.floor(v+1e-9), c=Math.round(Math.pow(10,v-e));
  if(e>=-2&&e<=3) return tickNum(c*Math.pow(10,e));
  return (c===1?'':c+'×')+'10'+supText(e);
}
/* decades, or 1-2-5 when the span is short — unless the 1-to-2 step would be
   under 14 px on this panel, where the labels would stack (hpx: its height) */
function logYTicks(lo,hi,hpx){
  const d=logTicks(lo,hi);
  if(d.length>=3) return d.map(Math.log10);
  const t=ticks125(lo,hi);
  if(hpx&&hpx*Math.log10(2)/Math.log10(hi/lo)<14) return (d.length>=2?d:t.filter((v,i)=>i%3===0)).map(Math.log10);
  return t.map(Math.log10);
}
/* a linear axis in units of 10^p, so its tick labels stay short enough to
   clear the rotated axis title 40 px left of the frame */
function powAxis(hi,name,unit){
  const p=Math.floor(Math.log10(hi)+1e-9), d=Math.pow(10,p);
  return {fmt:v=>tickNum(v/d),lab:name+', '+(p===0?'':'10'+supText(p)+' ')+unit,p,d};
}
/* a label held inside a plot frame b (lab() alone only keeps it on the canvas,
   and a label that slides past the frame lands in the tick-label column) */
function labIn(ctx,W,H,b,x,y,txt,col,align,base){
  const w=plain(txt).length*10.5*0.52, fh=10.5*1.15, bl=base||'middle';
  const lo=align==='right'?b.x+2+w:(align==='center'?b.x+2+w/2:b.x+2);
  const hi=align==='right'?b.x1-2:(align==='center'?b.x1-2-w/2:b.x1-2-w);
  const ylo=bl==='top'?b.y+2:(bl==='bottom'?b.y+2+fh:b.y+2+fh/2);
  const yhi=bl==='top'?b.y1-2-fh:(bl==='bottom'?b.y1-2:b.y1-2-fh/2);
  return lab(ctx,W,H,clamp(x,lo,Math.max(lo,hi)),clamp(y,ylo,Math.max(ylo,yhi)),txt,col,SM_FONT,align,base);
}
/* fewer y ticks on a short panel, or their labels stack into each other */
function nyFor(h){ return h<90?2:(h<140?3:4); }
/* axesR, plus every tick label and both axis titles in the label registry:
   axes() registers nothing, so a label that lab() dodges out of its first
   spot can land on a tick number it cannot see (the standard_model trap,
   "axesT registers ticks") */
function axesT(ctx,b,xlo,xhi,ylo,yhi,opt){
  axesR(ctx,b,xlo,xhi,ylo,yhi,opt);
  const o=opt||{}, fs=10.5, fh=fs*1.15;
  const xt=o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  const yt=o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||5);
  for(const t of xt){ const X=b.x+b.w*(t-xlo)/(xhi-xlo||1); if(X<b.x-0.5||X>b.x1+0.5) continue;
    const w=plain(o.xfmt?o.xfmt(t):fmt(t,2)).length*fs*0.52; LABELS.push([X-w/2,b.y1+5,X+w/2,b.y1+5+fh]); }
  for(const t of yt){ const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1); if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    const w=plain(o.yfmt?o.yfmt(t):fmt(t,2)).length*fs*0.52; LABELS.push([b.x-6-w,Y-fh/2,b.x-6,Y+fh/2]); }
  if(o.xlab){ const w=plain(o.xlab).length*11*0.52; LABELS.push([b.x+b.w/2-w/2,b.y1+21,b.x+b.w/2+w/2,b.y1+21+11*1.15]); }
  if(o.ylab){ const w=plain(o.ylab).length*11*0.52; LABELS.push([b.x-40-11*1.15,b.y+b.h/2-w/2,b.x-40,b.y+b.h/2+w/2]); }
}
/* a label beside a point, on whichever side keeps it inside the frame */
function labBeside(ctx,W,H,b,x,y,txt,col,base){
  const w=plain(txt).length*10.5*0.52;
  if(x+10+w<=b.x1-2) return labIn(ctx,W,H,b,x+10,y,txt,col,'left',base);
  return labIn(ctx,W,H,b,x-10,y,txt,col,'right',base);
}
/* the lower panels of a plot view: both on a wide stage, the second alone on
   a narrow one (stageLayout keeps one bottom row there, so the main plot's
   axis labels keep their room above it) */
function lowerPanels(Lo){ return Lo.bottom.length===2?Lo.bottom:[null,Lo.bottom[0]||null]; }

/* ================================================================== *
 *  the inverse square (shared): F against r on log-log axes, on       *
 *  linear axes, and F r^2 — flat at the law's constant                *
 * ================================================================== */
const INV_BAND={over:'rgba(232,132,58,0.20)',gap:'rgba(232,132,58,0.09)',off:'rgba(139,147,166,0.10)'};
function drawInverse(ctx,W,H,IV){
  const I=IV.I, u=IV.uPerM, un=IV.unit, r=IV.r*u, F=IV.F;
  /* a zero charge: no force at any distance, and no line to put on log axes —
     say so, rather than let log10(0) = -Infinity reach the axis range */
  if(!(I.prod>0)){
    const L0=stageLayoutH(ctx,W,H,IV.capFull,IV.capShort,0,0,0), b0=L0.main;
    lab(ctx,W,H,b0.x+b0.w/2,b0.y+b0.h*0.4,'One charge is zero: there is no force at any distance, so there is no line to draw.',COL.ref,LAB_FONT,'center');
    lab(ctx,W,H,b0.x+b0.w/2,b0.y+b0.h*0.4+22,'Give both charges a value to see the inverse square.',COL.dim,SM_FONT,'center');
    drawCaption(ctx,L0); return;
  }
  const Lo=stageLayoutH(ctx,W,H,IV.capFull,IV.capShort,2,0.36,1);
  const b=Lo.main;
  /* ---- log-log over [rTouch/2, 2 rTrack] ---- */
  const xlo=I.lo*u, xhi=I.hi*u, Fmin=I.Fs[I.Fs.length-1], Fmax=I.Fs[0];
  const X0=Math.log10(xlo), X1=Math.log10(xhi), Y0=Math.log10(Fmin)-0.15, Y1=Math.log10(Fmax)+0.15;
  const px=x=>b.x+b.w*(Math.log10(x)-X0)/(X1-X0), py=f=>b.y1-b.h*(Math.log10(f)-Y0)/(Y1-Y0);
  const band=(a,c,col)=>{ const A=clamp(px(a),b.x,b.x1), C=clamp(px(c),b.x,b.x1); if(C>A){ ctx.fillStyle=col; ctx.fillRect(A,b.y,C-A,b.h); } return [A,C]; };
  const bOver=band(xlo,I.rTouch*u,INV_BAND.over), bGap=band(I.rTouch*u,I.dmin*u,INV_BAND.gap), bOff=band(I.rTrack*u,xhi,INV_BAND.off);
  axesT(ctx,b,X0,X1,Y0,Y1,{title:titleFor(b,'the force against the distance between centres, log–log: a straight line of slope −2','F against r, log–log'),
    xlab:'distance between centres r, '+un,ylab:'F, N',xticks:ticks125(xlo,xhi).map(Math.log10),yticks:logYTicks(Math.pow(10,Y0),Math.pow(10,Y1),b.h),
    xfmt:powLabel,yfmt:powLabel});
  const lx=[], ly=[], rx=[], ry=[];
  for(let i=0;i<I.rs.length;i++){ const lg=Math.log10(I.rs[i]*u), lf=Math.log10(I.Fs[i]);
    lx.push(lg); ly.push(lf); if(I.rs[i]>=I.dmin*(1-1e-12)&&I.rs[i]<=I.rTrack*(1+1e-12)){ rx.push(lg); ry.push(lf); } }
  polyline(ctx,b,lx,ly,X0,X1,Y0,Y1,rgba(COL.pos,0.55),1.3,[5,4]);
  polyline(ctx,b,rx,ry,X0,X1,Y0,Y1,COL.pos,2.2);
  /* the slope triangle: double r, and the model's own F at 2r (a quarter) */
  if(2*r<=xhi){
    polyline(ctx,b,[Math.log10(r),Math.log10(2*r),Math.log10(2*r)],[Math.log10(F),Math.log10(F),Math.log10(I.F2r)],X0,X1,Y0,Y1,COL.ref,1.2,[3,3]);
    lab(ctx,W,H,px(Math.SQRT2*r),py(F)-6,'×2 in r',COL.ref,SM_FONT,'center','bottom');
    labBeside(ctx,W,H,b,px(2*r)-4,py(Math.sqrt(F*I.F2r)),'÷'+fmt(F/I.F2r,2)+' in F',COL.ref);
  }
  marker(ctx,b,X0,X1,Y0,Y1,Math.log10(r),Math.log10(F),COL.live);
  const fits=(a,t)=>a[1]-a[0]>t.length*10.5*0.52+8;
  if(fits(bOver,'they would overlap')) lab(ctx,W,H,(bOver[0]+bOver[1])/2,b.y1-12,'they would overlap',COL.ref,SM_FONT,'center');
  if(fits(bGap,IV.gapText)) lab(ctx,W,H,(bGap[0]+bGap[1])/2,b.y1-28,IV.gapText,COL.ref,SM_FONT,'center');
  const offLab=fits(bOff,'off the track');
  if(offLab) lab(ctx,W,H,(bOff[0]+bOff[1])/2,b.y+14,'off the track',COL.dim,SM_FONT,'center');
  labIn(ctx,W,H,b,px(r)-10,py(F)+14,'r = '+sigf(r,3)+' '+un+',  F = '+sciPlain(F,3)+' N',COL.live,'right','top');
  lab(ctx,W,H,b.x1-8,b.y+(offLab?30:14),'slope at r: '+fmt(I.slope,4)+'   ·   '+IV.pair,COL.pos,SM_FONT,'right');
  /* ---- the lower panels, over the distances the track can hold ---- */
  const [bl,br]=lowerPanels(Lo), a=I.dmin*u, c=I.rTrack*u, xs=I.lin.rs.map(x=>x*u);
  if(bl){
    const yh=I.Fnear*1.08, ax=powAxis(yh,'F','N');
    axesT(ctx,bl,a,c,0,yh,{title:titleFor(bl,'the same force on linear axes, where the track allows','F against r'),xlab:'r, '+un,ylab:ax.lab,nx:5,ny:nyFor(bl.h),
      xfmt:tickNum,yfmt:ax.fmt});
    polyline(ctx,bl,xs,I.lin.Fs,a,c,0,yh,COL.pos,2);
    marker(ctx,bl,a,c,0,yh,r,F,COL.live);
  }
  if(br){
    const yh2=I.prod*1.7, ax=powAxis(yh2,'F r²','N m²');
    axesT(ctx,br,a,c,0,yh2,{title:titleFor(br,'F r² is flat: it is '+IV.prodName+' (dashed: an inverse cube)','F r² against r'),xlab:'r, '+un,ylab:ax.lab,nx:5,ny:nyFor(br.h),
      xfmt:tickNum,yfmt:ax.fmt});
    polyline(ctx,br,xs,I.lin.F3r2,a,c,0,yh2,COL.ref,1.3,[5,4]);
    polyline(ctx,br,xs,I.lin.Fr2,a,c,0,yh2,COL.pos,2);
    marker(ctx,br,a,c,0,yh2,r,F*IV.r*IV.r,COL.live);
    lab(ctx,W,H,br.x1-8,br.y1-br.h*(1.3/1.7),IV.prodName+' = '+sciPlain(I.prod,4)+' N m²',COL.pos,SM_FONT,'right','bottom');
  }
  drawCaption(ctx,Lo);
}
