
/* ================================================================== *
 *  the shared picture: a 100 m field with a launcher on it, and the   *
 *  histogram of landing distance under it on the SAME x axis — which  *
 *  is PhET's layout and the whole point of the screen                 *
 * ================================================================== */
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it */
const HINT_H=18;
/* the room a panel needs below itself: ticks only, and ticks plus an x title */
const AX_PAD=22, AX_PAD_LAB=38;
/* tick labels follow the tick SPACING, not a fixed decimal count (Known-bad:
   fmt(t,2) prints 318.00 whatever the range, and six of those do not fit) */
function tickFmt(ticks){
  let g=Infinity; for(let i=1;i<ticks.length;i++) g=Math.min(g,Math.abs(ticks[i]-ticks[i-1]));
  if(!isFinite(g)||g<=0) return v=>sigf(v,3);
  let d=0; while(d<6&&Math.abs(Math.round(g*Math.pow(10,d))-g*Math.pow(10,d))>1e-6*Math.max(1,g*Math.pow(10,d))) d++;
  return v=>fmt(Math.abs(v)<1e-12?0:v,d);
}
function axesT(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=Object.assign({},opt||{});
  /* a 10.5 px label is 12 px tall and up to ~48 px wide, so the tick count is
     capped by the panel: a 52 px histogram asked for four y ticks and drew
     them 13 px apart, which the layout sweep caught as an overlap */
  const nyMax=Math.max(2,Math.floor(b.h/26)), nxMax=Math.max(2,Math.floor(b.w/56));
  if(o.xticks===undefined) o.xticks=ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),Math.min(o.nx||6,nxMax));
  if(o.yticks===undefined) o.yticks=ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),Math.min(o.ny||5,nyMax));
  if(!o.xfmt) o.xfmt=tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt=tickFmt(o.yticks);
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
  const tw=t=>plain(t).length*10.5*0.52, th=12;
  for(const t of o.xticks){
    const X=b.x+b.w*(t-xlo)/(xhi-xlo||1);
    if(X<b.x-0.5||X>b.x1+0.5) continue;
    const w=tw(o.xfmt(t)); LABELS.push([X-w/2,b.y1+5,X+w/2,b.y1+5+th]);
  }
  for(const t of o.yticks){
    const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1);
    if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    const w=tw(o.yfmt(t)); LABELS.push([b.x-6-w,Y-th/2,b.x-6,Y+th/2]);
  }
  if(o.xlab){ const w=tw(o.xlab); LABELS.push([b.x+b.w/2-w/2,b.y1+21,b.x+b.w/2+w/2,b.y1+21+th]); }
}
function pl(ctx,b,xs,ys,xlo,xhi,ylo,yhi,col,lw,dash){ polyline(ctx,b,xs,ys,xlo,xhi,ylo,yhi,col,lw,dash); }
/* legendAuto records its text box in LEGEND_RECTS (for the curve check) but
   NOT in LABELS, so a note drawn afterwards has no idea it is there and lands
   on it.  Register it. */
function legendReg(ctx,b,items){
  const r=legendAuto(ctx,b,items);
  if(r) LABELS.push([r.x,r.y,r.x1,r.y1]);
  return r;
}
/* logTicks() gives whole decades only, and this axis spans 1.1 of them: it
   returned ONE tick and the panel had no scale.  1-2-5 per decade instead. */
function logTicks125(lo,hi){
  if(!(lo>0)||!(hi>0)||!isFinite(lo)||!isFinite(hi)) return [];
  const out=[];
  for(let e=Math.floor(Math.log10(lo))-1;e<=Math.ceil(Math.log10(hi))+1;e++)
    for(const m of [1,2,5]){ const v=m*Math.pow(10,e); if(v>=lo*0.999&&v<=hi*1.001) out.push(v); }
  return out.sort((a,b)=>a-b);
}

/* ---- the stage split: a field strip on top, a histogram under it ---------- */
function labStage(ctx,W,H,capFull,capShort,opt){
  const o=opt||{};
  const narrow=isNarrow(W), left=54, right=narrow?W-22:W-RO_W-40;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+28;
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+200);
  const avail=Math.max(150,fit.capY-16-top);
  const out={narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,bottom:[],top,avail};
  /* axes() puts its x tick labels at b.y1 + 5 and its x axis title at
     b.y1 + 21, so a panel needs AX_PAD below it or the labels land in the
     caption — which is exactly how the first sweep failed */
  /* a narrow stage cannot carry a row of small panels: below 900 px the
     bottom row is dropped to one, or to none where it was a set of four
     (pupil_plane Known-bad — a 32 px panel with a 170 px legend is
     off-canvas by construction).  Every view checks L.bottom.length. */
  const nB=narrow?Math.min(o.nBottomNarrow===undefined?(o.nBottom>1?0:o.nBottom||0):o.nBottomNarrow,o.nBottom||0)
                 :(o.nBottom||0);
  let rowH=0;
  if(nB>0){
    rowH=Math.max(90,Math.floor(avail*0.30));
    const gut=Math.max(30,Math.min(50,(right-left)*0.055)), span=right-left, w=(span-gut*nB)/nB;
    for(let i=0;i<nB;i++) out.bottom.push(box(left+gut+i*(w+gut),top+avail-rowH+10,w,rowH-10-AX_PAD));
  }
  const bodyH=avail-(nB>0?rowH+14:0);
  if(o.histFrac===undefined){ out.main=box(left,top,right-left,Math.max(60,bodyH-AX_PAD_LAB)); return out; }
  /* from the bottom up: the x labels first, then the histogram, then whatever
     is left for the field — never the other way round */
  const inner=Math.max(100,bodyH-34-AX_PAD_LAB);
  let histH=Math.max(52,Math.round(inner*o.histFrac));
  let fh=inner-histH;
  /* a 30° trajectory tops out at 10 m over a 100 m field, so at true aspect it
     needs a tenth of the width and no more: giving it half the stage leaves
     two thirds of the picture as empty sky.  The view says how tall it wants
     to be; whatever it does not use goes to the histogram. */
  if(o.fieldWant){
    const want=o.fieldWant(right-left);
    if(want<fh){ histH=Math.min(inner-Math.max(90,want),Math.round(inner*0.62)); fh=inner-histH; }
  }
  if(fh<64){ fh=Math.max(40,Math.min(64,inner-40)); histH=inner-fh; }
  out.field=box(left,top,right-left,fh);
  out.hist=box(left,top+fh+34,right-left,histH);
  return out;
}
/* the field's own map: ONE scale for both axes wherever it fits (the picture
   is a trajectory, and a trajectory's shape is the thing being drawn), with
   the compression printed on the canvas when a narrow stage cannot afford it */
function fieldApex(cfg){
  return cfg.h+Math.pow(cfg.meanSpeed*cfg.mult*Math.sin((cfg.meanAng+2.5*cfg.sdAng)*Math.PI/180),2)/(2*PDL.G);
}
/* the field height that puts the trajectory at true aspect on a stage w wide */
function fieldWantH(M){ return w=>Math.max(4,fieldApex(M.cfg)*1.14)*(w/PDL.FIELD)+32; }
function fieldMap(b,M){
  const sx=b.w/PDL.FIELD;
  const apex=fieldApex(M.cfg);
  const ymax=Math.max(4,apex*1.14);
  const ground=Math.min(26,Math.max(12,b.h*0.14));
  const sy=Math.min(sx,(b.h-ground-6)/ymax);
  const y0=b.y1-ground;
  return {sx,sy,ratio:sy/sx,y0,ymax,ground,X:x=>b.x+sx*x,Y:y=>y0-sy*y,
          wx:X=>(X-b.x)/sx, wy:Y=>(y0-Y)/sy};
}
/* the six field markers PhET paints every 10 m (FIELD_LABEL_INCREMENT) */
function drawGround(ctx,b,map){
  ctx.fillStyle=COL.sky; ctx.fillRect(b.x,b.y,b.w,map.y0-b.y);
  ctx.fillStyle=COL.ground; ctx.fillRect(b.x,map.y0,b.w,b.y1-map.y0);
  ctx.strokeStyle='#2e3a46'; ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(b.x,map.y0+0.5); ctx.lineTo(b.x1,map.y0+0.5); ctx.stroke();
  ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='top';
  /* PhET numbers every 10 m; a narrow stage gets every 20 or 25 instead, so
     the labels never touch */
  const step=map.sx*10>=34?10:(map.sx*20>=34?20:25);
  for(let d=0;d<=PDL.FIELD;d+=10){
    const X=map.X(d);
    ctx.strokeStyle=d%50===0?'#4a5a66':'#2b343e'; ctx.lineWidth=d%50===0?1.4:1;
    ctx.beginPath(); ctx.moveTo(X,map.y0); ctx.lineTo(X,b.y1-11); ctx.stroke();
    if(d%step===0){ ctx.fillStyle='#78838f'; ctx.fillText(''+d,X,b.y1-10);
      /* registered, so a value label placed later dodges the marker rather
         than being shifted on top of it */
      const w=(''+d).length*10.5*0.52; LABELS.push([X-w/2,b.y1-10,X+w/2,b.y1+2]); }
  }
}
/* the launcher: a frame, a barrel at the mean angle, and (on the raised
   orientation) the 12 m tower PhET's model puts it on */
function drawLauncher(ctx,map,M){
  const cfg=M.cfg, X0=map.X(0), Y0=map.Y(cfg.h);
  const col=M.lau?COL.lau[M.lau-1]:COL.struct;
  if(cfg.h>0){
    ctx.fillStyle='#233041'; ctx.fillRect(X0-7,Y0,14,map.y0-Y0);
    ctx.strokeStyle='#3b4a5c'; ctx.lineWidth=1; ctx.strokeRect(X0-7.5,Y0+0.5,15,map.y0-Y0);
  }
  const th=cfg.meanAng*Math.PI/180, L=Math.max(16,Math.min(34,map.sx*3.2));
  ctx.strokeStyle=col; ctx.lineWidth=5; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(X0,Y0); ctx.lineTo(X0+L*Math.cos(th),Y0-L*Math.sin(th)); ctx.stroke();
  ctx.lineCap='butt';
  /* the spread: the mean angle ± 2 sd, drawn as a fan so an unequal launcher
     announces itself before a single shot is fired */
  ctx.strokeStyle=rgba(col,0.35); ctx.lineWidth=1.2;
  for(const k of [-2,2]){
    const a=(cfg.meanAng+k*cfg.sdAng)*Math.PI/180;
    ctx.beginPath(); ctx.moveTo(X0,Y0); ctx.lineTo(X0+L*1.25*Math.cos(a),Y0-L*1.25*Math.sin(a)); ctx.stroke();
  }
  dot(ctx,X0,Y0,4.5,col,'#0a0c12',1.2);
}
/* one projectile's path, from the launcher to where it is now */
function drawPath(ctx,map,cfg,p,col,alpha,lw){
  const n=26, T=Math.min(p.t,p.T);
  const xs=[], ys=[];
  for(let i=0;i<=n;i++){
    const t=T*i/n;
    xs.push(p.v*Math.cos(p.ang*Math.PI/180)*t);
    ys.push(pdlHeight(p.v,p.ang,cfg.h,t));
  }
  ctx.beginPath();
  for(let i=0;i<=n;i++){ const X=map.X(xs[i]), Y=map.Y(Math.max(0,ys[i])); if(i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); }
  ctx.strokeStyle=rgba(col,alpha); ctx.lineWidth=lw||1.2; ctx.stroke();
}
/* the launch-angle and launch-speed flags: PhET marks each landed projectile
   with the value it flew at; here the marker carries a tick coloured on the
   house scalar ramp, with the range named in the caption */
function flagRange(xs,key){
  let lo=Infinity, hi=-Infinity;
  for(const p of xs){ const v=p[key]; if(v<lo) lo=v; if(v>hi) hi=v; }
  if(!isFinite(lo)) return null;
  if(hi-lo<1e-9){ lo-=0.5; hi+=0.5; }
  return [lo,hi];
}
function drawField(ctx,b,M,opt){
  const o=opt||{}, st=M.st, map=fieldMap(b,M), cfg=M.cfg;
  drawGround(ctx,b,map);
  const col=M.lau?COL.lau[M.lau-1]:COL.struct;
  /* the landed projectiles */
  const key=st.showAng?'ang':(st.showSpd?'v':null);
  const rng=key?flagRange(M.F.landed,key):null;
  const r=Math.max(2,Math.min(4.2,map.sx*0.38));
  for(const p of M.F.landed){
    const X=map.X(p.x), Y=map.y0;
    if(key&&rng){
      const t=clamp((p[key]-rng[0])/(rng[1]-rng[0]),0,1);
      ctx.strokeStyle=neonCss(t); ctx.lineWidth=1.4;
      ctx.beginPath(); ctx.moveTo(X,Y-2); ctx.lineTo(X,Y-2-9*(0.35+0.65*t)); ctx.stroke();
    }
    dot(ctx,X,Y-r*0.6,r,rgba(col,0.5),null);
  }
  /* the paths, then the airborne projectiles */
  if(st.paths) for(const p of M.F.landed.slice(-14)) drawPath(ctx,map,cfg,p,col,0.16,1);
  for(const p of M.F.air){
    if(st.paths) drawPath(ctx,map,cfg,p,COL.live,0.85,1.5);
    const X=map.X(p.v*Math.cos(p.ang*Math.PI/180)*p.t), Y=map.Y(Math.max(0,pdlHeight(p.v,p.ang,cfg.h,p.t)));
    dot(ctx,X,Y,4,COL.live,'#fff',1);
  }
  drawLauncher(ctx,map,M);
  /* the exact mean, drawn on the field itself */
  if(o.showExactMean!==false){
    const X=map.X(M.exact.mean);
    ctx.strokeStyle=rgba(COL.ref,0.8); ctx.lineWidth=1.3; ctx.setLineDash([5,4]);
    ctx.beginPath(); ctx.moveTo(X,b.y+6); ctx.lineTo(X,map.y0); ctx.stroke(); ctx.setLineDash([]);
    /* an unlabelled dashed rule in the same family of colours as the shots is
       a question, not an answer */
    lab(ctx,b.x1+2,b.y1+2,X+5,b.y+8,'μ = '+fmt(M.exact.mean,2)+' m, exact',COL.ref,SM_FONT,'left','top');
  }
  return map;
}
/* the histogram: PhET's two representations, blocks (one square per
   projectile) and bars (one rectangle per bin), on the field's own x axis */
function drawHist(ctx,b,M,opt){
  const o=opt||{}, st=M.st, w=M.binW, H=o.hist||M.hist;
  const ymaxRaw=Math.max(4,H.max);
  const ymax=o.ymax||Math.ceil(ymaxRaw*1.18);
  const xlo=0, xhi=o.xhi===undefined?PDL.FIELD:o.xhi, xlo2=o.xlo===undefined?0:o.xlo;
  axesT(ctx,b,xlo2,xhi,0,ymax,{title:o.title||'landing distance, metres',
    xlab:o.xlab===undefined?'x, m':o.xlab, ylab:o.ylab===undefined?'count':o.ylab, nx:o.nx||6, ny:4});
  const px=x=>b.x+b.w*(x-xlo2)/(xhi-xlo2), py=y=>b.y1-b.h*y/ymax;
  const bw=Math.max(1.5,b.w*w/(xhi-xlo2));
  for(let i=0;i<H.counts.length;i++){
    const c=H.counts[i]; if(!c) continue;
    const x0=(H.lo+i)*w;
    const X=px(x0);
    if(X+bw<b.x-1||X>b.x1+1) continue;
    const col=o.col||COL.pos;
    if(st.blocks&&bw>=3.5&&c<=ymax&&b.h/ymax>=5){
      /* PhET's "blocks" representation: one cell per projectile.  The gap
         between cells is a FRACTION of the cell, not a fixed 1.2 px — at a
         40 px cell a hairline gap reads as one solid bar, which is the bar
         representation wearing the other one's name. */
      const cellH=b.h/ymax, gap=clamp(0.18*cellH,2.2,7), gx=Math.min(gap,bw*0.3);
      for(let k=0;k<c;k++){
        const Y=py(k+1);
        ctx.fillStyle=rgba(col,0.82);
        ctx.fillRect(Math.max(b.x,X)+gx/2,Y+gap/2,Math.min(bw-gx,b.x1-X-gx),Math.max(1.5,cellH-gap));
      }
      POLY_SEGS.push(Math.max(b.x,X),py(c),Math.min(b.x1,X+bw),py(c));
    } else {
      ctx.fillStyle=rgba(col,0.72);
      const X0=Math.max(b.x,X), X1=Math.min(b.x1,X+bw);
      if(X1>X0){ ctx.fillRect(X0,py(c),X1-X0,b.y1-py(c)); POLY_SEGS.push(X0,py(c),X1,py(c)); }
    }
  }
  return {px,py,ymax};
}
/* the mean marker, the ±1 sd bar and the values, as PhET's DataMeasuresOverlay
   draws them — on the histogram, above the bars */
function drawMeasures(ctx,W,H,b,M,hm){
  const st=M.st, S=M.stat;
  if(S.mean===null) return;
  const yTop=b.y+10;
  if(st.showMean){
    const X=hm.px(S.mean);
    ctx.strokeStyle=COL.live; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke();
    lab(ctx,W,H,X,yTop,'x̄ = '+fmt(S.mean,2)+' m',COL.live,LAB_FONT,'center','bottom');
  }
  if(st.showSd&&S.sd1!==null){
    const a=hm.px(S.mean-S.sd1), c=hm.px(S.mean+S.sd1), y=yTop+16;
    ctx.strokeStyle=COL.pos; ctx.lineWidth=1.6;
    ctx.beginPath(); ctx.moveTo(a,y); ctx.lineTo(c,y);
    ctx.moveTo(a,y-5); ctx.lineTo(a,y+5); ctx.moveTo(c,y-5); ctx.lineTo(c,y+5); ctx.stroke();
    lab(ctx,W,H,(a+c)/2,y+12,'s = '+fmt(S.sd1,2)+' m (n−1)',COL.pos,SM_FONT,'center','top');
  }
}
/* the interval tool: two draggable edges and the percentage between them */
function intervalGeo(b,M,hm){
  const a=hm.px(M.st.e1), c=hm.px(M.st.e2);
  return {a,c,mid:(a+c)/2,y:b.y+6,yb:b.y1};
}
function drawInterval(ctx,W,H,b,M,hm){
  const G=intervalGeo(b,M,hm), a=Math.min(G.a,G.c), c=Math.max(G.a,G.c);
  ctx.fillStyle='rgba(205,53,196,.10)'; ctx.fillRect(a,b.y,c-a,b.h);
  ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
  for(const X of [G.a,G.c]){ ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke();
    ctx.fillStyle=COL.live; ctx.fillRect(X-4,b.y-7,8,8); }
  lab(ctx,W,H,(a+c)/2,b.y-11,fmt(Math.abs(M.st.e2-M.st.e1),1)+' m  ·  '+fmt(100*M.frac,1)+'%',
      COL.live,'italic 12px Georgia, serif','center','bottom');
}

/* ================================================================== *
 *  view 1: the field — PhET's Variability screen                      *
 * ================================================================== */
function aspectNote(rTxt){
  return ' The field’s vertical scale is ×'+rTxt+' of its horizontal (1.00 is true aspect, and anything less is the stage being too short for the trajectory).';
}
function fieldCaption(M,rTxt){
  const st=M.st, sc=aspectNote(rTxt);
  const flag=st.showAng?' Each landed shot carries a tick coloured by its launch angle.'
        :(st.showSpd?' Each landed shot carries a tick coloured by its launch speed.':'');
  return {full:'Six fields, six launchers, and the same 100 m of ground. Fire single shots or hold continuous fire; the histogram below shares the field’s x axis, so a bar sits under the shots that made it.'+sc+flag
            +' The dashed orange rule is the exact mean of this launcher’s law, not of the data.',
          short:'Field '+st.fld+', launcher '+M.lau+'.'+sc};
}
function drawFieldView(ctx,W,H,M){
  const ph=fieldCaption(M,'1.00');
  const L=labStage(ctx,W,H,ph.full,ph.short,{histFrac:0.42,fieldWant:fieldWantH(M)});
  /* the six fields as a strip of counts, so the screen's six-field structure
     is visible without switching between them.  Its box is RESERVED in the
     registry before the field draws, because the field's own labels are
     placed through lab() and would otherwise be shifted on top of it. */
  ctx.font=SM_FONT;
  const stripY=L.field.y+11;
  const strip=[]; let sx2=L.field.x+4;
  strip.push(['fields:','#78838f',sx2]); sx2+=42;
  M.fields.forEach((F,i)=>{
    const t=(i+1)+' ('+F.landed.length+')';
    strip.push([t,i+1===M.st.fld?COL.lau[F.lau-1]:'#4d5866',sx2]);
    sx2+=ctx.measureText(t).width+13;
  });
  LABELS.push([L.field.x+2,stripY-8,sx2,stripY+8]);
  const map=drawField(ctx,L.field,M);
  const hm=drawHist(ctx,L.hist,M);
  ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='middle';
  for(const [t,c,x2] of strip){ ctx.fillStyle=c; ctx.fillText(plain(t),x2,stripY); }
  const cap=fieldCaption(M,fmt(map.ratio,2));
  caption(ctx,L.left,L.capY,L.capTxt===ph.full?cap.full:cap.short,L.capW,'#767e92',CAP_FONT);
  lab(ctx,W,H,L.hist.x1-4,L.hist.y+9,'bin width '+fmt(M.binW,2)+' m',COL.dim,SM_FONT,'right','middle');
  return {map,hm,L};
}

/* ================================================================== *
 *  view 2: the sources — PhET's Sources screen                        *
 * ================================================================== */
function srcCaption(M,rTxt){
  const cfg=M.cfg;
  const at45=Math.abs(cfg.meanAng-45)<1e-9;
  return {full:'Where does the spread come from? The mechanism sets the speed’s spread (spring ±0.5, pressure ±0.2, explosion ±1.2 m/s — PhET’s values) and the angle stabiliser sets the angle’s (0.2° to 5°). The two panels below are those two Gaussians; the histogram above is what they make of each other.'
            +(at45?' At 45° the angle term switches off to first order — ∂x/∂θ = 2v²cos2θ/g is zero there — so only the speed spread survives.':'')
            +' The projectile only scales the mean speed (×1, ×1.1, ×0.9), so a pumpkin flies further with the same fractional spread.'+aspectNote(rTxt),
          short:'The mechanism sets σ_v, the stabiliser sets σ_θ; the two panels below are those Gaussians.'+aspectNote(rTxt)};
}
function gaussPanel(ctx,b,mu,sd,title,xlab,col,marks){
  const lo=mu-4*sd, hi=mu+4*sd;
  const n=120, xs=[], ys=[];
  for(let i=0;i<=n;i++){ const x=lo+(hi-lo)*i/n; xs.push(x); ys.push(Math.exp(-0.5*Math.pow((x-mu)/sd,2))/(sd*Math.sqrt(2*Math.PI))); }
  let ymax=0; for(const y of ys) ymax=Math.max(ymax,y);
  axesT(ctx,b,lo,hi,0,ymax*1.2,{title,xlab,ylab:'density',nx:4,ny:3});
  pl(ctx,b,xs,ys,lo,hi,0,ymax*1.2,col,1.8);
  const px=x=>b.x+b.w*(x-lo)/(hi-lo);
  ctx.strokeStyle=rgba(col,0.55); ctx.lineWidth=1; ctx.setLineDash([4,3]);
  for(const k of [-1,1]){ const X=px(mu+k*sd); ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke(); }
  ctx.setLineDash([]);
  lab(ctx,b.x1+200,b.y1+200,px(mu),b.y+4,marks,col,SM_FONT,'center','top');
}
function drawSourcesView(ctx,W,H,M){
  const ph=srcCaption(M,'1.00');
  const L=labStage(ctx,W,H,ph.full,ph.short,{histFrac:0.44,nBottom:2,fieldWant:fieldWantH(M)});
  const map=drawField(ctx,L.field,M);
  const hm=drawHist(ctx,L.hist,M);
  const cfg=M.cfg, mu=cfg.meanSpeed*cfg.mult;
  if(L.bottom.length>=2){
    gaussPanel(ctx,L.bottom[0],mu,cfg.sdSpeed,'launch speed','v, m/s',COL.struct,
               'μ '+fmt(mu,2)+' ± '+fmt(cfg.sdSpeed,2));
    gaussPanel(ctx,L.bottom[1],cfg.meanAng,cfg.sdAng,'launch angle','θ, degrees',COL.bar,
               'μ '+fmt(cfg.meanAng,0)+'° ± '+fmt(cfg.sdAng,2)+'°');
  }
  const cap=srcCaption(M,fmt(map.ratio,2));
  caption(ctx,L.left,L.capY,L.capTxt===ph.full?cap.full:cap.short,L.capW,'#767e92',CAP_FONT);
  lab(ctx,W,H,L.hist.x1-4,L.hist.y+9,'bin width '+fmt(M.binW,2)+' m',COL.dim,SM_FONT,'right','middle');
  return {map,hm,L};
}
