
/* ---- this sim's own drawing helpers ------------------------------------------------------------- */
const DRAG={what:null,off:0};
const TITLE_FONT='italic 13px Georgia, serif';
/* a label with a dark pad under it, placed by the same shift-or-drop search as lab() */
function labPad(ctx,W,H,x,y,txt,col,font,align,base){
  const f=font||SM_FONT, al=align||'left', bl=base||'middle';
  const t=plain(txt), fs=parseFloat(f.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  for(const dy of [0,16,-16,32,-32]){
    let X=x, Y=y+dy;
    if(al==='left') X=clamp(X,2,W-w-2); else if(al==='right') X=clamp(X,w+2,W-2); else X=clamp(X,w/2+2,W-w/2-2);
    Y=clamp(Y,hh,H-hh);
    const lx=al==='center'?X-w/2:(al==='right'?X-w:X);
    const ly=bl==='top'?Y:(bl==='middle'?Y-hh/2:(bl==='bottom'?Y-hh:Y-hh*0.8));
    const bx=[lx,ly,lx+w,ly+hh];
    if(labFits(bx)){
      LABELS.push(bx);
      ctx.fillStyle='rgba(7,11,24,0.82)'; ctx.fillRect(lx-3,ly-1,w+6,hh+2);
      ctx.fillStyle=col; ctx.font=f; ctx.textAlign=al; ctx.textBaseline=bl; ctx.fillText(t,X,Y);
      return true;
    }
  }
  return false;
}
/* does the segment (x0,y0)-(x1,y1) cross the box [l,t,r,b]?  Liang–Barsky, exact */
function segHitsBox(x0,y0,x1,y1,bx){
  let t0=0,t1=1; const dx=x1-x0, dy=y1-y0;
  for(const [p,q] of [[-dx,x0-bx[0]],[dx,bx[2]-x0],[-dy,y0-bx[1]],[dy,bx[3]-y0]]){
    if(p===0){ if(q<0) return false; continue; }
    const t=q/p;
    if(p<0){ if(t>t1) return false; if(t>t0) t0=t; } else { if(t<t0) return false; if(t<t1) t1=t; }
  }
  return t0<=t1;
}
/* a label at the first candidate [x, y, align, baseline] whose box stays on the canvas, clears every
   registered label AND crosses no recorded curve segment; if none does, lab() at the first.  Call it
   after the curves it must avoid are drawn.  pad: a dark backing box. */
function labAvoid(ctx,W,H,cands,txt,col,font,pad,extra){
  const f=font||SM_FONT, t=plain(txt), fs=parseFloat(f.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  for(const [x,y,al,bl] of cands){
    const lx=al==='center'?x-w/2:(al==='right'?x-w:x), ly=bl==='top'?y:(bl==='middle'?y-hh/2:(bl==='bottom'?y-hh:y-hh*0.8));
    const bx=[lx,ly,lx+w,ly+hh];
    if(bx[0]<2||bx[2]>W-2||bx[1]<0||bx[3]>H||!labFits(bx)) continue;
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4) hit=segHitsBox(POLY_SEGS[i],POLY_SEGS[i+1],POLY_SEGS[i+2],POLY_SEGS[i+3],bx);
    if(extra) for(let i=0;i<extra.length&&!hit;i+=4) hit=segHitsBox(extra[i],extra[i+1],extra[i+2],extra[i+3],bx);
    if(hit) continue;
    LABELS.push(bx);
    if(pad){ ctx.fillStyle='rgba(7,11,24,0.82)'; ctx.fillRect(lx-3,ly-1,w+6,hh+2); }
    ctx.fillStyle=col; ctx.font=f; ctx.textAlign=al; ctx.textBaseline=bl; ctx.fillText(t,x,y);
    return true;
  }
  const c=cands[0];
  return pad ? labPad(ctx,W,H,c[0],c[1],txt,col,f,c[2],c[3]) : lab(ctx,W,H,c[0],c[1],txt,col,f,c[2],c[3]);
}
/* an axis maximum from PhET's ladders, printed as the ladder value: 3, 0.75, 100, 5.12×10⁻⁵ */
function axisMax(v){ return v>=1e-3 ? String(+v.toPrecision(4)) : sci(v,4).replace(/(\.\d*?)0+×/,'$1×').replace('.×','×'); }
function diamond(ctx,x,y,r,fill,stroke){
  ctx.beginPath(); ctx.moveTo(x,y-r); ctx.lineTo(x+r,y); ctx.lineTo(x,y+r); ctx.lineTo(x-r,y); ctx.closePath();
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1; ctx.stroke(); }
}
function line(ctx,x0,y0,x1,y1,col,lw,dash){
  ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.strokeStyle=col; ctx.lineWidth=lw||1;
  if(dash) ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
}
function arrowH(ctx,x,y,dir,len,col){          /* a small horizontal arrow from x toward dir */
  const x1=x+dir*len;
  ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x1,y); ctx.moveTo(x1,y); ctx.lineTo(x1-dir*5,y-4); ctx.moveTo(x1,y); ctx.lineTo(x1-dir*5,y+4);
  ctx.strokeStyle=col; ctx.lineWidth=1.6; ctx.stroke();
}
/* tick labels whose decimals follow the tick SPACING (Known-bad: a fixed fmt(t,2) crowds a panel) */
function decFor(step){ return Math.max(0,Math.min(8,-Math.floor(Math.log10(step)+1e-9))); }
function linTicks(lo,hi,want){ const t=ticksFor(lo,hi,want); const step=t.length>1?t[1]-t[0]:Math.abs(hi-lo)||1; return {t,dec:decFor(step)}; }
/* the power axis: plain numbers inside 0.01 … 10⁴, otherwise a common ×10ⁿ in the axis title */
function powerAxis(ymax,want){
  const e=(ymax<0.01||ymax>=1e4)?Math.floor(Math.log10(ymax)):0, sc=Math.pow(10,e);
  const tk=linTicks(0,ymax/sc,want);
  return {e,sc,t:tk.t.map(v=>v*sc),fmt:v=>(v/sc).toFixed(tk.dec)};
}
function starPath(ctx,cx,cy,ro,ri,n){
  ctx.beginPath();
  for(let i=0;i<2*n;i++){ const r=i%2?ri:ro, a=-PI/2+i*PI/n, x=cx+r*Math.cos(a), y=cy+r*Math.sin(a);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y); }
  ctx.closePath();
}
/* PhET's star: a nine-pointed star (outer 35, inner 20 px) in the photometer colour, behind it a flat
   halo disc of radius 5 + 47.5 r and opacity 0.3 r (PhET's values), all scaled by s */
function drawStarGlyph(ctx,cx,cy,s,ph,halo){
  if(halo[1]>0){ ctx.beginPath(); ctx.arc(cx,cy,halo[0]*s,0,TAU); ctx.fillStyle='rgba('+ph.join(',')+','+fmt(halo[1],3)+')'; ctx.fill(); }
  starPath(ctx,cx,cy,35*s,20*s,9);
  ctx.fillStyle='rgb('+ph.join(',')+')'; ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,0.28)'; ctx.lineWidth=1; ctx.stroke();      /* so a cold, black star still shows */
}
/* PhET's photometer: three discs, B G R, each lit by one channel */
function drawBGR(ctx,W,H,xs,y,r,ph){
  const fills=['rgb(0,0,'+ph[2]+')','rgb(0,'+ph[1]+',0)','rgb('+ph[0]+',0,0)'], names=['B','G','R'];
  for(let i=0;i<3;i++){ dot(ctx,xs[i],y,r,fills[i],'rgba(255,255,255,0.28)',1); lab(ctx,W,H,xs[i],y+r+9,names[i],COL.dim,SM_FONT,'center','middle'); }
}

/* ================================================================== *
 *  view: the spectrum — PhET's screen                                 *
 * ================================================================== */
const STAR_SCALE=0.45;                          /* the star beside the thermometer, relative to PhET's size */
function specWarning(S){
  if(!S.peakIn) return 'The peak is at '+um(S.lm,3)+', beyond this axis: zoom the wavelength axis out, or fit the axes.';
  if(S.over) return 'The peak, '+sci(S.Mp,3)+' MW/m²/µm, is above this axis: zoom the power axis out, or fit the axes.';
  if(S.tiny) return 'The curve peaks at '+sci(S.Mp,3)+' MW/m²/µm, under 1 % of this axis: zoom the power axis in, or fit the axes.';
  return '';
}
function specCaption(M,W){
  const S=M.S, T=M.T, xs=axisMax(S.xmax/1000), ys=axisMax(S.ymax);
  let full='Planck’s curve for a blackbody at '+fmt(T,0)+' K (green): spectral power density M_λ = πB_λ against wavelength, both axes linear, '
    +'0–'+xs+' µm by 0–'+ys+' MW/m²/µm; the wavelength axis zooms ×2 a click (0.75–48 µm) and the power axis ×5 (1.024×10⁻⁵–2500). '
    +'The orange diamond is Wien’s peak, λ_max = b/T = '+um(S.lm)+'; the rainbow is the visible band, 380–780 nm.';
  if(M.st.inten) full+=' The green shade is the intensity: its whole area is σT⁴, and '+pct(S.win)+' of it lies inside this window.';
  if(SAVED.length) full+=' Orange: the saved curve'+(SAVED.length>1?'s, the newer solid.':'.');
  if(!isNarrow(W)) full+=' Left: drag the thermometer (it snaps to 50 K); the star wears PhET’s photometer colour, drawn at '+STAR_SCALE+' of PhET’s size.';
  const short='Planck’s curve at '+fmt(T,0)+' K, linear axes 0–'+xs+' µm × 0–'+ys+' MW/m²/µm; orange: Wien’s peak.';
  return [full,short];
}
function specGeo(ctx,W,H,M){
  const S=M.S, narrow=isNarrow(W), col=!narrow;
  const right=narrow?W-26:W-RO_W-44, left=col?232:66;
  const capLeft=col?190:56, capW=Math.max(260,Math.min(W-148,right-capLeft));
  const cap=specCaption(M,W), top=stageTop()+50;
  const fit=fitCaption(ctx,W,H,cap[0],cap[1],capW,top+200);
  const warn=specWarning(S);
  const bottom=fit.capY-16-38-(warn?18:0);
  const g={narrow,col,b:box(left,top,right-left,Math.max(60,bottom-top)),capY:fit.capY,capTxt:fit.txt,capW,capLeft,
           warn,warnY:fit.capY-10,star:null,th:null};
  if(col){
    /* the left column: the star and PhET's photometer at the top, the thermometer below.  Its geometry
       depends only on H — never on the caption — so a drag cannot move the scale under the pointer. */
    const st0=stageTop();
    if(H>=520){ g.star={cx:84,cy:st0+62,s:STAR_SCALE}; g.bgr={xs:[58,84,110],y:st0+132,r:8}; g.tlab={x:84,y:st0+170}; }
    const yTop=(g.star?st0+196:st0+34), bulbR=10, bulbY=H-40, yBot=bulbY-bulbR-2;
    if(!g.star) g.tlab={x:84,y:yTop-18};
    if(yBot-yTop>=120) g.th={x:104,w:12,yTop,yBot,bulbY,bulbR};
  }
  return g;
}
function thermoY(th,T){ return th.yBot-(th.yBot-th.yTop)*(T-T_MIN)/(T_MAX-T_MIN); }
function tempAtY(th,y){ return snapT(T_MIN+(th.yBot-y)/(th.yBot-th.yTop)*(T_MAX-T_MIN)); }
function drawThermo(ctx,W,H,g,T){
  const th=g.th, cx=th.x+th.w/2, fillCol=mix(COL.bg,COL.live,0.55), yT=thermoY(th,T);
  ctx.fillStyle=fillCol; ctx.fillRect(th.x+2,yT,th.w-4,th.bulbY-yT);                     /* the column */
  dot(ctx,cx,th.bulbY,th.bulbR,fillCol,rgba(COL.struct,0.75),1.5);                       /* the bulb */
  ctx.strokeStyle=rgba(COL.struct,0.75); ctx.lineWidth=1.5;
  ctx.strokeRect(th.x,th.yTop-6,th.w,th.yBot-th.yTop+6);                                  /* the tube */
  for(let TT=1000;TT<=T_MAX;TT+=1000){ const y=thermoY(th,TT); line(ctx,th.x,y,th.x+4,y,rgba(COL.struct,0.6),1); }
  for(const p of PRESETS){ const y=thermoY(th,p.T);
    line(ctx,th.x-9,y,th.x,y,COL.struct,1.5);
    lab(ctx,W,H,th.x-12,y,p.name,p.T===T?COL.live:COL.dim,SM_FONT,'right','middle'); }
  const tx=th.x+th.w+2;                                                                     /* the thumb */
  ctx.beginPath(); ctx.moveTo(tx,yT); ctx.lineTo(tx+14,yT-7); ctx.lineTo(tx+14,yT+7); ctx.closePath();
  ctx.fillStyle=COL.live; ctx.fill(); ctx.strokeStyle='#ffffff'; ctx.lineWidth=0.8; ctx.stroke();
}
function drawVisibleBand(ctx,b,xmaxNm){
  const lo=380, hi=Math.min(780,xmaxNm);
  if(!(hi>lo)) return null;
  const pxPerNm=b.w/xmaxNm, step=Math.max(1,Math.ceil(1.5/pxPerNm));
  for(let nm=lo;nm<hi;nm+=step){
    const x0=b.x+nm*pxPerNm, w=Math.min(step,hi-nm)*pxPerNm+0.6, c=nm+Math.min(step,hi-nm)/2;
    const css=cssOfLinear(monoLinear(c),monoLevel(c));
    ctx.fillStyle=mix(COL.bg,css,0.3); ctx.fillRect(x0,b.y,w,b.h);       /* the wash, premixed and opaque */
    ctx.fillStyle=css; ctx.fillRect(x0,b.y1-5,w,5);                       /* the strip on the axis */
  }
  return [b.x+lo*pxPerNm,b.x+hi*pxPerNm];
}
function drawSpec(ctx,W,H,M){
  const S=M.S, st=M.st, g=specGeo(ctx,W,H,M), b=g.b, xmx=S.xmax/1000, ymx=S.ymax;
  const X=x=>b.x+b.w*x/xmx, Y=y=>b.y1-b.h*y/ymx;
  /* the visible band, then the axes over it */
  SPEC_LAST.band=drawVisibleBand(ctx,b,S.xmax);
  const xt=linTicks(0,xmx,g.narrow?4:6), pa=powerAxis(ymx,g.narrow?4:5);
  axesR(ctx,b,0,xmx,0,ymx,{xticks:xt.t,yticks:pa.t.filter(v=>v>0),xfmt:v=>v.toFixed(xt.dec),yfmt:pa.fmt,
    xlab:'wavelength λ, µm   (1 µm = 1000 nm)',ylab:'M_λ, '+(pa.e?'×10'+supNum(pa.e)+' ':'')+'MW/m²/µm'});
  lab(ctx,W,H,b.x,b.y-26,g.narrow?'Planck’s law at '+fmt(M.T,0)+' K':'spectral power density of a blackbody at '+fmt(M.T,0)+' K',
      '#aeb6c6',TITLE_FONT,'left','bottom');
  /* PhET's band labels along the top: ticks at 10 nm, 380 nm, 780 nm and 100 µm; a name only where its band
     is ≥ 20 px (PhET's rule).  Drawn first, so they own the row above the frame. */
  SPEC_LAST.bands=[];
  if(st.labels){
    const edges=[10,380,780,1e5].filter(e=>e<=S.xmax), cuts=[0].concat(edges).concat([S.xmax]);
    for(const e of edges) line(ctx,X(e/1000),b.y,X(e/1000),b.y-7,COL.struct,1.2);
    for(let i=0;i<cuts.length-1;i++){
      const x0=X(cuts[i]/1000), x1=X(Math.min(cuts[i+1],S.xmax)/1000), wpx=x1-x0, bd=BANDS[i];
      if(wpx<20) continue;
      const full=bd.name.length*10.5*0.52+8<wpx, nm=full?bd.name:bd.short;
      if(nm.length*10.5*0.52+4<wpx&&lab(ctx,W,H,(x0+x1)/2,b.y-5,nm,COL.struct,SM_FONT,'center','bottom')) SPEC_LAST.bands.push(bd.id);
    }
  }
  /* the intensity: the area under the curve, clamped at the top of the axis */
  if(st.inten){
    ctx.beginPath(); ctx.moveTo(X(0),Y(0));
    for(let i=0;i<S.c.xs.length;i++) ctx.lineTo(X(S.c.xs[i]),Y(Math.min(S.c.ys[i],ymx)));
    ctx.lineTo(X(xmx),Y(0)); ctx.closePath(); ctx.fillStyle=rgba(COL.pos,0.2); ctx.fill();
  }
  /* the saved curves (older dashed), then the live one */
  for(const c of S.saved) polyline(ctx,b,c.c.xs,c.c.ys,0,xmx,0,ymx,COL.ref,1.8,c.newest?null:[7,5]);
  polyline(ctx,b,S.c.xs,S.c.ys,0,xmx,0,ymx,COL.pos,2.4);
  SPEC_LAST.curveTop=Math.min.apply(null,S.c.ys.map((v,i)=>S.c.xs[i]<=xmx?Y(Math.min(v,ymx)):b.y1));
  /* Graph Values: the magenta point on the curve, dashed to both axes; hidden past either axis, as PhET's.
     Drawn before the labels, which avoid its dashed lines (GVSEG) as well as the curves. */
  SPEC_LAST.gv=null; const GVSEG=[]; let gvLab=null;
  if(S.gv.on&&S.gv.inside){
    const gx=X(S.gv.nm/1000), gy=S.gv.above?b.y:Y(S.gv.M);
    line(ctx,gx,b.y1,gx,gy,COL.live,1.2,[4,4]); GVSEG.push(gx,b.y1,gx,gy);
    if(!S.gv.above){
      line(ctx,b.x,gy,gx,gy,COL.live,1.2,[4,4]); GVSEG.push(b.x,gy,gx,gy);
      if(S.gv.cue){ arrowH(ctx,gx+9,gy,1,15,COL.live); arrowH(ctx,gx-9,gy,-1,15,COL.live); }
      dot(ctx,gx,gy,5,COL.live,'#ffffff',1.2);
      SPEC_LAST.gv=[gx,gy];
    }
    const right=gx>b.x+b.w*0.62, al=right?'right':'left', dx=right?-12:12;
    gvLab={txt:um(S.gv.nm)+', '+sci(S.gv.M,3)+' MW/m²/µm',
           cands:S.gv.above?[[gx+dx,b.y+8,al,'top'],[gx+dx,b.y+26,al,'top']]:[[gx+dx,gy-14,al,'bottom'],[gx+dx,gy+12,al,'top'],[gx+dx,gy-30,al,'bottom']]};
    labAvoid(ctx,W,H,gvLab.cands,gvLab.txt,COL.live,SM_FONT,true);
  }
  /* Wien's peak; off the top, it is marked on the frame and labelled just inside it */
  SPEC_LAST.peak=null;
  if(S.peakIn){
    const px=X(S.lm/1000), py=S.over?b.y:Y(S.Mp), txt='λ_max = '+um(S.lm)+(S.over?'  (peak above the axis)':'');
    diamond(ctx,px,py,5,COL.ref,'#ffffff');
    labAvoid(ctx,W,H,S.over?[[px+9,b.y+8,'left','top'],[px-9,b.y+8,'right','top'],[px+9,b.y+26,'left','top']]
                           :[[px+9,py-10,'left','bottom'],[px-9,py-10,'right','bottom'],[px+10,py+8,'left','top'],[px+12,py-28,'left','bottom']],
             txt,COL.ref,SM_FONT,true,GVSEG);
    SPEC_LAST.peak=[px,py];
  }
  /* the saved curves' temperatures: at the peak, where the curve enters the top, or at the right edge */
  for(const c of S.saved){
    const txt=fmt(c.T,0)+' K'; let cands;
    if(c.lm<=S.xmax&&c.Mp<=ymx){ const px=X(c.lm/1000), py=Y(c.Mp); cands=[[px+8,py-6,'left','bottom'],[px-8,py-6,'right','bottom'],[px+8,py+6,'left','top']]; }
    else {
      const k=c.c.ys.findIndex(v=>v>ymx);
      if(k>0){ const px=X(c.c.xs[k]); cands=[[px+8,b.y+8,'left','top'],[px-8,b.y+8,'right','top'],[px+8,b.y+26,'left','top']]; }
      else { const py=Math.min(b.y1-10,Y(c.c.ys[c.c.ys.length-1])); cands=[[b.x1-6,py-6,'right','bottom'],[b.x1-6,py+6,'right','top']]; }
    }
    labAvoid(ctx,W,H,cands,txt,COL.ref,SM_FONT,true,GVSEG);
  }
  /* the intensity's label, inside the shaded area on the curve's right flank */
  if(st.inten){
    const hgt=Math.min(S.Mp,ymx), yy=v=>Math.min(b.y1-14,Y(v)), xx=v=>X(Math.min(v,0.8*S.xmax)/1000);
    const cands=S.peakIn?[[xx(2.2*S.lm),yy(0.25*hgt),'center','middle'],[xx(1.6*S.lm),yy(0.15*hgt),'center','middle'],[xx(3*S.lm),yy(0.1*hgt),'center','middle']]
                        :[[b.x+b.w*0.5,yy(0.2*Math.min(S.c.ys[S.c.ys.length-1],ymx)),'center','middle']];
    cands.push([b.x+b.w*0.5,b.y1-14,'center','middle']);
    labAvoid(ctx,W,H,cands,'area σT⁴ = '+sci(S.I,3)+' W/m²',COL.pos,SM_FONT,true,GVSEG);
  }
  if(g.warn) lab(ctx,W,H,g.capLeft,g.warnY-6,g.warn,COL.ref,SM_FONT,'left','bottom');
  caption(ctx,g.capLeft,g.capY,g.capTxt,g.capW,'#767e92',CAP_FONT);
  /* the left column */
  if(g.star){ drawStarGlyph(ctx,g.star.cx,g.star.cy,g.star.s,S.ph,S.halo); drawBGR(ctx,W,H,g.bgr.xs,g.bgr.y,g.bgr.r,S.ph); }
  if(g.col) lab(ctx,W,H,g.tlab.x,g.tlab.y,fmt(M.T,0)+' K',COL.live,'600 13px -apple-system, sans-serif','center','middle');
  if(g.th) drawThermo(ctx,W,H,g,M.T);
  SPEC_LAST.g=g;
}
/* what the last spectrum drawing put where — read by selfTest, never by the drawing itself */
const SPEC_LAST={};
