
/* ================================================================== *
 *  the shared picture layer — EXTRACTED from                          *
 *  build/projectile-data-lab/p4_views.js by make_views.py, unchanged: *
 *  the stage layout, the field map (true aspect wherever it fits),    *
 *  PhET's 10 m markers, the launcher and its spread fan, the          *
 *  trajectories.                                                      *
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
