
/* ================================================================== *
 *  this file's drawing layer: stacked function panels, the two tools, *
 *  and the first two views                                            *
 * ================================================================== */
/* the house #hint sits at bottom:11px on top of the last line of a caption
   anchored at H - 12, and the canvas capture cannot see it because the hint
   is HTML.  Every caption here is laid out in H - HINT_H instead
   (Known-bad, found by the wave-on-a-string build). */
const HINT_H=18;
const GEO={view:null,fb:null,fmap:null,scrubs:[],panels:[]};

/* sigf() writes its exponent as "x10^-14"; on a canvas that is eight literal
   characters sitting next to panel titles that use real superscripts.  sigS()
   is the same number with the exponent in Unicode. */
function sigS(x,n){
  return sigf(x,n).replace(/\^(-?\d+)$/,function(m,d){ return supNum(d); });
}
/* tick labels follow the tick SPACING, not a fixed decimal count */
function tickFmt(ticks){
  let g=Infinity;
  for(let i=1;i<ticks.length;i++) g=Math.min(g,Math.abs(ticks[i]-ticks[i-1]));
  if(!isFinite(g)||g<=0) return v=>sigf(v,3);
  let dd=0;
  while(dd<6&&Math.abs(Math.round(g*Math.pow(10,dd))-g*Math.pow(10,dd))>1e-6*Math.max(1,g*Math.pow(10,dd))) dd++;
  return v=>fmt(Math.abs(v)<1e-6*g?0:v,dd);
}
/* thin a tick list until its labels are at least minGap apart ON SCREEN.  A
   fixed tick count is wrong for a stack of four panels: at 560x380 each one is
   about 34 px tall and five y labels land on top of each other ("-2" on "-1",
   found by the inline layout sweep).  The spacing is computed from the tick
   step and the box, not guessed. */
function thinTicks(t,lo,hi,px,minGap){
  if(t.length<2) return t;
  const sp=Math.abs(px*(t[1]-t[0])/((hi-lo)||1));
  if(sp>=minGap) return t;
  const k=Math.max(2,Math.ceil(minGap/Math.max(sp,1e-9)));
  const out=t.filter((v,i)=>i%k===0);
  return out.length?out:[t[0]];
}
function axesT(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=Object.assign({},opt||{});
  /* thin whatever list ends up being drawn, SUPPLIED OR GENERATED: the grid
     view hands in its own decade ticks and at 560x380 they collided
     ("10^-14" on "10^-12"), which a thinner applied only to the generated
     list could not see. */
  o.xticks=thinTicks(o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6),
                     Math.min(xlo,xhi),Math.max(xlo,xhi),b.w,34);
  o.yticks=thinTicks(o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||4),
                     Math.min(ylo,yhi),Math.max(ylo,yhi),b.h,16);
  if(!o.xfmt) o.xfmt=tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt=tickFmt(o.yticks);
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
}
/* a panel title in the colour of the curve it names, registered in the label
   registry the same way axesR registers its own */
function panelTitle(ctx,b,txt,col){
  const t=plain(txt);
  ctx.font='italic 13px Georgia, serif';
  ctx.textAlign='left'; ctx.textBaseline='bottom';
  ctx.fillStyle=col||COL.text;
  ctx.fillText(t,b.x,b.y-9);
  LABELS.push([b.x,b.y-9-13*1.15,b.x+t.length*13*0.52,b.y-9]);
}
function mapFor(b,xlo,xhi,ylo,yhi){
  return {X:x=>b.x+b.w*(x-xlo)/(xhi-xlo),
          Y:y=>b.y1-b.h*(y-ylo)/(yhi-ylo),
          wx:px=>xlo+(xhi-xlo)*(px-b.x)/b.w,
          wy:py=>ylo+(yhi-ylo)*(b.y1-py)/b.h,
          xlo,xhi,ylo,yhi,b};
}
/* PhET's Grid checkbox: a unit grid over the panel, under everything else */
function unitGrid(ctx,b,map,stepX,stepY){
  ctx.save(); ctx.strokeStyle='#141926'; ctx.lineWidth=1;
  ctx.beginPath();
  for(let x=Math.ceil(map.xlo/stepX)*stepX;x<=map.xhi+1e-9;x+=stepX){
    const X=map.X(x); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1);
  }
  for(let y=Math.ceil(map.ylo/stepY)*stepY;y<=map.yhi+1e-9;y+=stepY){
    const Y=map.Y(y); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y);
  }
  ctx.stroke(); ctx.restore();
}
function zeroLine(ctx,b,map){
  if(map.ylo>0||map.yhi<0) return;
  const Y=map.Y(0);
  ctx.save(); ctx.strokeStyle=COL.zero; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); ctx.stroke(); ctx.restore();
}
/* a curve drawn in runs, split at the nodes flagged as corners.  PhET's
   "Discontinuities" control chooses whether the runs are joined by a dashed
   line or simply left apart; the default (no line) is the honest one for a
   derivative that genuinely has two different one-sided limits. */
function plotRuns(ctx,b,xs,ys,map,col,lw,breaks,dashJoin){
  const n=Math.min(xs.length,ys.length);
  const cuts=[];
  for(const i of (breaks||[]).slice().sort((p,q)=>p-q))
    if(i>0&&i<n-1&&cuts[cuts.length-1]!==i) cuts.push(i);
  const sub=(a,z)=>{
    polyline(ctx,b,xs.subarray?xs.subarray(a,z+1):xs.slice(a,z+1),
             ys.subarray?ys.subarray(a,z+1):ys.slice(a,z+1),
             map.xlo,map.xhi,map.ylo,map.yhi,col,lw);
  };
  let start=0;
  for(let k=0;k<=cuts.length;k++){
    const end=(k<cuts.length)?cuts[k]:(n-1);
    if(end>start) sub(start,end);
    if(k<cuts.length){
      const i=cuts[k];
      if(dashJoin)
        polyline(ctx,b,[xs[i],xs[i+1]],[ys[i],ys[i+1]],
                 map.xlo,map.xhi,map.ylo,map.yhi,col,1,[3,3]);
      start=i+1;
    }
  }
  return cuts.length;
}
/* the indices of the derivative CELLS on either side of a flagged corner: the
   jump lives between cell i-1 and cell i for a corner at node i */
function breakCells(corners){
  const out=[];
  for(const c of corners) if(c.i>0&&c.i<NPTS-1) out.push(c.i-1);
  return out;
}
/* the gap between the first two ticks of a range, with a fallback, so a unit
   grid can never ask for a step of undefined */
function tickStep(lo,hi,n){
  const t=ticksFor(lo,hi,n||4);
  return (t.length>1&&isFinite(t[1]-t[0])&&t[1]>t[0])?(t[1]-t[0]):Math.max(1e-9,(hi-lo)/4);
}
/* a scrubber: PhET's draggable vertical line with a handle at the top */
function scrub(ctx,W,H,b,map,x,col,label,kind){
  const X=clamp(map.X(x),b.x,b.x1);
  ctx.save();
  ctx.strokeStyle=col; ctx.lineWidth=1.4; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle=col;
  ctx.beginPath();
  ctx.moveTo(X,b.y+9); ctx.lineTo(X-5,b.y); ctx.lineTo(X+5,b.y); ctx.closePath();
  ctx.fill();
  ctx.restore();
  /* through lab(), so the label REGISTERS its box: drawn raw it collided with
     the values readout in the lab view at 860x560, which the layout audit
     found and the label registry would have dodged */
  /* above the frame, not inside it: inside, the label lies on whatever curve
     happens to pass there (it sat on the tangent line in every default view) */
  if(label)
    lab(ctx,W,H,X+(X>b.x1-40?-4:4),b.y-6,label,col,SM_FONT,X>b.x1-40?'right':'left','bottom');
  GEO.scrubs.push({kind,X,b});
}
/* the area tool: every cell painted in one of two colours, split at its zero
   crossing, so what is drawn IS what the readout counted */
function areaFill(ctx,b,map,f,xend){
  const y0=map.Y(0);
  ctx.save();
  const paint=(xa,ya,xb,yb)=>{
    const Xa=map.X(xa), Xb=map.X(xb);
    if(Xb<b.x-1||Xa>b.x1+1) return;
    ctx.beginPath();
    ctx.moveTo(clamp(Xa,b.x,b.x1),y0);
    ctx.lineTo(clamp(Xa,b.x,b.x1),clamp(map.Y(ya),b.y,b.y1));
    ctx.lineTo(clamp(Xb,b.x,b.x1),clamp(map.Y(yb),b.y,b.y1));
    ctx.lineTo(clamp(Xb,b.x,b.x1),y0);
    ctx.closePath();
    ctx.fillStyle=(ya+yb>=0)?rgba(COL.areaPos,0.28):rgba(COL.areaNeg,0.28);
    ctx.fill();
  };
  const last=cellAt(xend);
  for(let i=0;i<last;i++){
    const a=f[i], bb=f[i+1];
    if(a*bb<0){ const t=a/(a-bb);
      paint(XG[i],a,XG[i]+t*DX,0); paint(XG[i]+t*DX,0,XG[i+1],bb); }
    else paint(XG[i],a,XG[i+1],bb);
  }
  const t=(xend-XG[last])/DX;
  if(t>0){
    const a=f[last], bb=f[last]+t*(f[last+1]-f[last]);
    if(a*bb<0){ const tz=a/(a-bb);
      paint(XG[last],a,XG[last]+tz*t*DX,0); paint(XG[last]+tz*t*DX,0,xend,bb); }
    else paint(XG[last],a,xend,bb);
  }
  ctx.restore();
}
/* the tangent line, drawn as the cell's own chord extended both ways */
function tangentLine(ctx,b,map,T,halfLen){
  const xs=[T.x0-halfLen,T.x1+halfLen];
  const ys=[T.y0-T.slope*halfLen,T.y1+T.slope*halfLen];
  polyline(ctx,b,xs,ys,map.xlo,map.xhi,map.ylo,map.yhi,COL.live,1.6);
  const X=clamp(map.X(T.x),b.x,b.x1), Y=clamp(map.Y(T.y),b.y,b.y1);
  dot(ctx,X,Y,4,COL.live,'#fff',1.2);
}
/* PhET's two barometers, drawn as little vertical gauges beside a panel.
   Skipped on a narrow stage: there the panel already reaches within 24 px of
   the right edge, so the gauge lands ON the panel and its name label collides
   with the x-axis tick underneath it (the inline layout sweep found "slope"
   sitting on "10" at 560x380).  The number is in the scrubber label and in the
   readout either way. */
function barometer(ctx,W,H,x,y,hh,val,lo,hi,col,name){
  if(isNarrow(W)) return false;
  const w=13;
  ctx.save();
  frame(ctx,box(x,y,w,hh),'#242a3a');
  const Y0=y+hh*(hi-0)/(hi-lo);
  ctx.strokeStyle=COL.zero; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(x,Y0); ctx.lineTo(x+w,Y0); ctx.stroke();
  const v=clamp(val,lo,hi);
  const Y=y+hh*(hi-v)/(hi-lo);
  ctx.fillStyle=rgba(col,0.55);
  ctx.fillRect(x+1,Math.min(Y,Y0),w-2,Math.abs(Y-Y0));
  ctx.strokeStyle=col; ctx.lineWidth=2;
  ctx.beginPath(); ctx.moveTo(x,Y); ctx.lineTo(x+w,Y); ctx.stroke();
  ctx.restore();
  lab(ctx,W,H,x+w/2,y+hh+4,name,COL.dim,SM_FONT,'center','top');
  lab(ctx,W,H,x+w/2,y-3,fmt(val,2),col,SM_FONT,'center','bottom');
  return true;
}

/* ---- the stacked-panel layout -------------------------------------
   Laid out bottom-up from a MEASURED caption, and the caption is cut to the
   number of lines that leaves the panels their minimum height.  The earlier
   version took the caption's own height and then floored the panel height,
   which at 560x380 with four panels pushed the bottom panel's tick labels
   straight into the caption ("2" on "f on top, then f, th").  Nothing is
   guessed here: the line count, the 42 px for axes()'s hanging x label and the
   18 px the HTML #hint owns are all arithmetic. */
function panelStack(ctx,W,H,n,capFull,capShort){
  const narrow=isNarrow(W);
  /* 76 px of right margin, not 42: PhET's two gauges hang off the right-hand
     end of a panel, and the floating readout owns about 336 px of the stage
     there (Known-bad).  At 42 the gauge's own name label sat under it, which
     tools/audit.py reports and a reader cannot see.  The gutter is reserved
     whether or not a gauge is showing, so toggling one does not move the
     panels. */
  const left=60, right=narrow?W-24:W-RO_W-76;
  const capW=Math.max(280,Math.min(W-148,right-left));
  const top=stageTop()+32;
  /* 46 px of gutter, not 36: axes() puts a row of x tick labels 5 px under
     every panel and panelTitle() puts the next panel's name 24 px above it, so
     36 leaves a 5 px overlap ("2" on "the corner, magnifie").  The four-panel
     lab keeps 30 and suppresses the x labels on its top three instead, because
     all four of its panels share one x axis. */
  const gut=n>=4?30:46;
  const need=26*n+gut*(n-1)+42;                 /* the least the panels need */
  const maxLines=Math.max(1,Math.floor((H-HINT_H-12-top-need)/14));
  /* RESERVE the caption band rather than fitting it: these captions quote the
     corner count and the tangent slope, so their wrapped line count changes as
     the curve is dragged, and a layout derived from it MOVES THE PANELS under
     the pointer mid-drag.  (It did: the second half of a drag landed at the
     wrong y and the UI harness caught it.)  The band depends only on W, H and
     the panel count; a short caption simply leaves the rest of it blank. */
  const lines=Math.min(7,maxLines);
  let txt=capFull;
  if(wrapText(ctx,capFull,capW,CAP_FONT).length>lines) txt=capShort;
  let ls=wrapText(ctx,txt,capW,CAP_FONT);
  if(ls.length>lines){
    /* drop words until the ellipsis fits too: taking lines-1 and appending one
       is not enough when lines is 1 and the ellipsis wraps */
    let words=ls.slice(0,Math.max(1,lines)).join(' ').split(/\s+/);
    do{ words.pop(); txt=words.join(' ')+' \u2026'; ls=wrapText(ctx,txt,capW,CAP_FONT); }
    while(ls.length>lines&&words.length>1);
  }
  const capY=H-HINT_H-12-lines*14;
  const avail=capY-42-top;
  const hh=Math.max(26,(avail-gut*(n-1))/n);
  const bs=[];
  for(let i=0;i<n;i++) bs.push(box(left,top+i*(hh+gut),Math.max(120,right-left),hh));
  return {bs,capY,capTxt:txt,capW,left,right,narrow,lines};
}
function drawStackCaption(ctx,L){
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}
function xAxisOpt(extra){
  return Object.assign({xlab:VAR(),nx:6},extra||{});   /* PhET's Variable preference reaches the axis too */
}

/* ================================================================== *
 *  view 1: the derivative  (PhET's Derivative screen)                 *
 * ================================================================== */
function derivCap(M){
  const S=M.live, T=M.tools;
  const nc=S.corners.length;
  const full='Drag anywhere on the upper panel to shape f. The lower panel is its derivative, '
    +'drawn at the CELL MIDPOINTS: the curve you see is straight across each cell, so the '
    +'difference quotient there is the slope exactly, not an estimate. '
    +(nc?('This curve has '+nc+' corner'+(nc===1?'':'s')+', and the derivative simply stops and '
      +'restarts at each one — the two one-sided limits are both real and they differ.')
       :'This curve is smooth everywhere, so the derivative is one unbroken run.')
    +' The magenta line is the tangent, and its slope is the number the gauge on the right reads: '
    +fmt(T.tan.slope,3)+'.'
    +(M.st.predict?' Predict is on: the orange curve is your sketch, the dashed green one is f'
      +(M.st.showF?'':' (hidden)')+', and the derivative panel and the tangent both belong to f.':'');
  const short='Upper: f, which you drag. Lower: its derivative at the cell midpoints. Tangent slope '
    +fmt(T.tan.slope,3)+'.';
  return {full,short};
}
function drawDeriv(ctx,W,H,M){
  const S=M.live, SH=M.shape, T=M.tools, st=M.st;
  const cap=derivCap(M);
  const L=panelStack(ctx,W,H,2,cap.full,cap.short);
  const bF=L.bs[0], bD=L.bs[1];
  const mF=mapFor(bF,XMIN,XMAX,-M.yF,M.yF), mD=mapFor(bD,XMIN,XMAX,-M.yD,M.yD);
  GEO.view='deriv'; GEO.fb=bF; GEO.fmap=mF; GEO.panels=[[bF,mF],[bD,mD]];

  if(st.grid){ unitGrid(ctx,bF,mF,1,tickStep(-M.yF,M.yF));
               unitGrid(ctx,bD,mD,1,tickStep(-M.yD,M.yD)); }
  axesT(ctx,bF,XMIN,XMAX,-M.yF,M.yF,{});
  axesT(ctx,bD,XMIN,XMAX,-M.yD,M.yD,xAxisOpt());
  panelTitle(ctx,bF,cName('f'),COL.f);
  panelTitle(ctx,bD,cName('d'),COL.d);
  zeroLine(ctx,bF,mF); zeroLine(ctx,bD,mD);

  if(st.predict&&st.showF)
    polyline(ctx,bF,XG,S.f,mF.xlo,mF.xhi,mF.ylo,mF.yhi,COL.f,1.5,[6,4]);
  polyline(ctx,bF,XG,SH.f,mF.xlo,mF.xhi,mF.ylo,mF.yhi,st.predict?COL.pred:COL.f,2.0);
  plotRuns(ctx,bD,XMID,S.d,mD,COL.d,1.9,breakCells(S.corners),st.discont==='dashedLine');

  if(st.tangent){
    tangentLine(ctx,bF,mF,T.tan,1.1);
    scrub(ctx,W,H,bF,mF,st.xT,COL.live,'slope '+fmt(T.tan.slope,2),'T');
    scrub(ctx,W,H,bD,mD,st.xT,COL.live,null,'T');
    const X=clamp(mD.X(st.xT),bD.x,bD.x1), Y=clamp(mD.Y(T.tan.slope),bD.y,bD.y1);
    dot(ctx,X,Y,4,COL.live,'#fff',1.2);
    barometer(ctx,W,H,Math.min(bF.x1+8,W-40),bF.y+8,Math.max(40,bF.h-30),T.tan.slope,
              -SLOPE_MAX,SLOPE_MAX,COL.live,'slope');
  }
  if(st.refLine){ scrub(ctx,W,H,bF,mF,st.xR,COL.struct,null,'R'); scrub(ctx,W,H,bD,mD,st.xR,COL.struct,null,'R'); }
  if(st.values){
    const rt=mF.X(st.xT)>bF.x1-90;
    lab(ctx,W,H,mF.X(st.xT)+(rt?-8:8),mF.Y(valueAt(S.f,st.xT))-12,'f = '+fmt(valueAt(S.f,st.xT),3),
        COL.f,SM_FONT,rt?'right':'left','bottom');
    lab(ctx,W,H,mD.X(st.xT)+(rt?-8:8),mD.Y(T.tan.slope)-12,cName('d')+' = '+fmt(T.tan.slope,3),
        COL.d,SM_FONT,rt?'right':'left','bottom');
  }
  for(const c of S.corners.slice(0,12)){
    const X=mD.X(c.x);
    if(X<bD.x||X>bD.x1) continue;
    ctx.fillStyle=rgba(COL.warn,0.8);
    ctx.beginPath(); ctx.arc(X,bD.y1-4,2.6,0,TAU); ctx.fill();
  }
  drawStackCaption(ctx,L);
}

/* ================================================================== *
 *  view 2: the integral  (PhET's Integral screen)                     *
 * ================================================================== */
function integCap(M){
  const T=M.tools;
  const full='The upper panel is the running integral of f, and the lower panel is f with the area '
    +'under it painted in: cyan where f is above the axis, orange where it is below, each cell split '
    +'at its own zero crossing. Drag the scrubber to move the upper limit. The two numbers must agree '
    +'and they do — the painted area comes to '+fmt(T.ar.pos,3)+' − '+fmt(T.ar.neg,3)+' = '
    +fmt(T.ar.net,3)+', and the integral curve reads '+fmt(T.Ia,3)+', a difference of '
    +sigS(T.areaMismatch,2)+'. They are computed by different arithmetic, so that is a check and not '
    +'a tautology.'
    +(M.st.predict?' Predict is on: the orange curve is your sketch and the integral above is f’s.':'');
  const short='Upper: the running integral. Lower: f with its signed area. Net '+fmt(T.ar.net,3)+'.';
  return {full,short};
}
function drawInteg(ctx,W,H,M){
  const S=M.live, SH=M.shape, T=M.tools, st=M.st;
  const cap=integCap(M);
  const L=panelStack(ctx,W,H,2,cap.full,cap.short);
  const bI=L.bs[0], bF=L.bs[1];
  const mI=mapFor(bI,XMIN,XMAX,-M.yI,M.yI), mF=mapFor(bF,XMIN,XMAX,-M.yF,M.yF);
  GEO.view='integ'; GEO.fb=bF; GEO.fmap=mF; GEO.panels=[[bI,mI],[bF,mF]];

  if(st.grid){ unitGrid(ctx,bI,mI,1,tickStep(-M.yI,M.yI));
               unitGrid(ctx,bF,mF,1,tickStep(-M.yF,M.yF)); }
  axesT(ctx,bI,XMIN,XMAX,-M.yI,M.yI,{});
  axesT(ctx,bF,XMIN,XMAX,-M.yF,M.yF,xAxisOpt());
  panelTitle(ctx,bI,cName('I'),COL.I);
  panelTitle(ctx,bF,cName('f'),COL.f);
  zeroLine(ctx,bI,mI); zeroLine(ctx,bF,mF);

  if(st.area) areaFill(ctx,bF,mF,S.f,clamp(st.xA,XMIN,XMAX));
  if(st.predict&&st.showF)
    polyline(ctx,bF,XG,S.f,mF.xlo,mF.xhi,mF.ylo,mF.yhi,COL.f,1.5,[6,4]);
  polyline(ctx,bF,XG,SH.f,mF.xlo,mF.xhi,mF.ylo,mF.yhi,st.predict?COL.pred:COL.f,2.0);
  polyline(ctx,bI,XG,S.F,mI.xlo,mI.xhi,mI.ylo,mI.yhi,COL.I,2.0);

  if(st.area){
    scrub(ctx,W,H,bF,mF,st.xA,COL.live,'area '+fmt(T.ar.net,2),'A');
    scrub(ctx,W,H,bI,mI,st.xA,COL.live,null,'A');
    const X=clamp(mI.X(st.xA),bI.x,bI.x1), Y=clamp(mI.Y(T.Ia),bI.y,bI.y1);
    dot(ctx,X,Y,4,COL.live,'#fff',1.2);
    barometer(ctx,W,H,Math.min(bI.x1+8,W-40),bI.y+8,Math.max(40,bI.h-30),T.ar.net,
              -AREA_MAX,AREA_MAX,COL.live,'area');
  }
  if(st.refLine){ scrub(ctx,W,H,bI,mI,st.xR,COL.struct,null,'R'); scrub(ctx,W,H,bF,mF,st.xR,COL.struct,null,'R'); }
  if(st.values){
    const rt=mI.X(st.xA)>bI.x1-90;
    lab(ctx,W,H,mI.X(st.xA)+(rt?-8:8),mI.Y(T.Ia)-12,'∫ = '+fmt(T.Ia,3),COL.I,SM_FONT,
        rt?'right':'left','bottom');
    lab(ctx,W,H,bF.x+7,bF.y+12,'+'+fmt(T.ar.pos,3)+'  −'+fmt(T.ar.neg,3),COL.dim,SM_FONT,'left','top');
  }
  drawStackCaption(ctx,L);
}
