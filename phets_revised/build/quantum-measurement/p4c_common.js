
/* ================================================================== *
 *  common drawing: role colours, the hint reservation, ticks, rich    *
 *  text (sup/sub on a canvas), coin faces, bars (shared by the family) *
 * ================================================================== */
/* green = the + outcome / the measured thing, violet = the - outcome, orange =
   the law (reference), magenta = the live marker, cyan = structure */
const COL={pos:'#b8ec4c', neg:'#9a7fd1', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', text:'#aeb6c6', edge:'#242a3a', faint:'#4a5165', bg:'#070b18'};
const RO_W=300;
/* the house #hint (HTML, bottom:11px, 11px type) sits on the last line of a
   caption anchored at H - 12, and the canvas capture cannot see it: every
   caption here ends HINT_H higher, and selfTest asserts the corner is clear */
const HINT_H=18;
/* fmt() without the negative zero: toFixed prints -6e-17 (-cos 90 deg in
   floating point) and a measured -0.0002 as "-0.000"; a value that rounds to
   zero prints unsigned.  p1_utils.js is a verbatim house extract, so the fix
   lives here, and selfTest's layout and panel sweeps reject any "-0.000". */
function fmt0(x,n){ const s=fmt(x,n); return /^-0(\.0*)?$/.test(s)?s.slice(1):s; }
/* tick labels follow the tick SPACING (Known-bad: a fixed decimal count
   collides in a narrow panel) */
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
function px(b,x,xlo,xhi){ return b.x+b.w*(x-xlo)/(xhi-xlo||1); }
function py(b,y,ylo,yhi){ return b.y1-b.h*(y-ylo)/(yhi-ylo||1); }
/* rich text on a canvas: runs of [text, 'sup'|'sub'|null]; returns the width.
   Registered with the label registry as one box. */
function richW(ctx,runs,fs){
  let w=0;
  for(const [t,k] of runs){ ctx.font=(k?(fs*0.72):fs)+'px Georgia, serif'; w+=ctx.measureText(plain(t)).width; }
  return w;
}
function rich(ctx,x,y,runs,fs,col,align,reg){
  const w=richW(ctx,runs,fs);
  let X=align==='center'?x-w/2:(align==='right'?x-w:x);
  if(reg) LABELS.push([X,y-fs*0.9,X+w,y+fs*0.35]);
  ctx.textAlign='left'; ctx.textBaseline='alphabetic';
  for(const [t,k] of runs){
    const f=k?fs*0.72:fs; ctx.font='italic '+f+'px Georgia, serif'; ctx.fillStyle=col||COL.text;
    const dy=k==='sup'?-fs*0.38:(k==='sub'?fs*0.22:0);
    ctx.fillText(plain(t),X,y+dy); X+=ctx.measureText(plain(t)).width;
  }
  return w;
}
/* an ellipse as an explicit polygon in device coordinates (Known-bad: the
   recorder has no ellipse() and does not carry a scaled arc through restore) */
function ellipsePath(ctx,cx,cy,rx,ry,n){
  n=n||40; ctx.beginPath();
  for(let i=0;i<=n;i++){ const a=TAU*i/n, x=cx+rx*Math.cos(a), y=cy+ry*Math.sin(a); if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y); }
  ctx.closePath();
}
/* an arrow glyph (up or down) as a polygon, h tall, centred on (cx, cy) */
function arrowGlyph(ctx,cx,cy,h,up,col,sx){
  const s=sx===undefined?1:sx, d=up?-1:1, hw=h*0.30*s, tw=h*0.10*s, hh=h*0.42;
  const tip=cy+d*h/2, base=cy-d*h/2, neck=tip-d*hh;
  ctx.beginPath();
  ctx.moveTo(cx,tip); ctx.lineTo(cx+hw,neck); ctx.lineTo(cx+tw,neck); ctx.lineTo(cx+tw,base);
  ctx.lineTo(cx-tw,base); ctx.lineTo(cx-tw,neck); ctx.lineTo(cx-hw,neck); ctx.closePath();
  ctx.fillStyle=col; ctx.fill();
}
/* a coin face.  kind: 'H'/'T' (classical), 'U'/'D' (quantum), 'S' a quantum
   superposition with P(up) = p (both arrows, each in proportion), 'hidden'
   (the cup), 'flip' (mid-flip: squashed by sx and showing side f).  The
   heads and up faces are green, tails and down violet (premixed, opaque). */
function coinFace(ctx,cx,cy,r,kind,o){
  o=o||{};
  const sx=o.sx===undefined?1:Math.max(0.06,Math.abs(o.sx));
  if(kind==='hidden'){
    ellipsePath(ctx,cx,cy,r,r,36); ctx.fillStyle='#1a1f2c'; ctx.fill();
    ctx.strokeStyle='#5d6780'; ctx.lineWidth=Math.max(1.5,r*0.12); ctx.stroke();
    ctx.fillStyle='#8b93a6'; ctx.font='italic '+Math.round(r*1.05)+'px Georgia, serif';
    ctx.textAlign='center'; ctx.textBaseline='middle'; if(r>=7) ctx.fillText('?',cx,cy+r*0.04);
    return;
  }
  const up=(kind==='H'||kind==='U');
  const base=kind==='S'?mix(COL.neg,COL.pos,o.p):(up?COL.pos:COL.neg);
  ellipsePath(ctx,cx,cy,r*sx,r,36); ctx.fillStyle=shade(base,0.28); ctx.fill();
  ctx.strokeStyle=shade(base,0.85); ctx.lineWidth=Math.max(1,r*0.09); ctx.stroke();
  if(r<7) return;
  if(kind==='H'||kind==='T'){
    ctx.fillStyle=up?COL.pos:COL.neg; ctx.font='italic bold '+Math.round(r*1.1)+'px Georgia, serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    if(sx>0.55) ctx.fillText(up?'H':'T',cx,cy+r*0.05);
  } else if(kind==='U'||kind==='D') arrowGlyph(ctx,cx,cy,r*1.25,up,up?COL.pos:COL.neg,sx);
  else {
    /* a superposition: the up arrow at weight p and the down arrow at 1 - p,
       side by side, each premixed toward the coin's own fill */
    const bg=shade(base,0.28);
    arrowGlyph(ctx,cx-r*0.28*sx,cy,r*1.1,true,mix(bg,COL.pos,0.15+0.85*o.p),sx);
    arrowGlyph(ctx,cx+r*0.28*sx,cy,r*1.1,false,mix(bg,COL.neg,0.15+0.85*(1-o.p)),sx);
  }
}
/* a vertical error bar at data (x, y +- e), clipped to the box */
function errBar(ctx,b,x,y,e,xlo,xhi,ylo,yhi,col){
  const X=px(b,x,xlo,xhi); if(X<b.x-0.5||X>b.x1+0.5) return;
  const y0=clamp(py(b,y-e,ylo,yhi),b.y,b.y1), y1=clamp(py(b,y+e,ylo,yhi),b.y,b.y1);
  ctx.beginPath(); ctx.moveTo(X,y0); ctx.lineTo(X,y1); ctx.moveTo(X-3,y0); ctx.lineTo(X+3,y0); ctx.moveTo(X-3,y1); ctx.lineTo(X+3,y1);
  ctx.strokeStyle=col; ctx.lineWidth=1.2; ctx.stroke();
}
/* a point marker: 'o' filled circle or 'd' diamond (a second shape, never a
   hollow marker: Known-bad, one hollow convention per file) */
function mark(ctx,X,Y,shape,col,r){
  r=r||4; ctx.beginPath();
  if(shape==='d'){ ctx.moveTo(X,Y-r*1.2); ctx.lineTo(X+r*1.2,Y); ctx.lineTo(X,Y+r*1.2); ctx.lineTo(X-r*1.2,Y); ctx.closePath(); }
  else ctx.arc(X,Y,r,0,TAU);
  ctx.fillStyle=col; ctx.fill();
}
/* the magenta cursor on a plot, clipped to its box */
function vCursor(ctx,b,x,xlo,xhi,col){
  const X=px(b,x,xlo,xhi); if(X<b.x-0.5||X>b.x1+0.5) return;
  ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.strokeStyle=col||COL.live; ctx.lineWidth=1.3; ctx.setLineDash([4,3]); ctx.stroke(); ctx.setLineDash([]);
}
/* a bar's value, clear of the bar AND of the law's mark (yMark: the mark's
   pixel y; omit it when no mark is drawn).  Above the bar; else above the
   mark when the mark is the higher; else INSIDE the bar at its top, dark; else
   inside, under the mark.  A full bar hid its own green-on-green count, and a
   label set above its bar alone sat on the 0.5 mark when the bar stopped just
   short of it (28.1/s on a 0.47 bar): both looked at. */
const BAR_CLEAR=8;   /* > 7.14: half a 10.5px label box (6.04) plus half the 2.2px mark */
function barValY(yTop,yMark,b){
  const hasM=yMark!==null&&yMark!==undefined&&isFinite(yMark), gap=y=>hasM?Math.abs(y-yMark):Infinity;
  /* the places in order: above the bar, above a higher mark, inside the bar
     at its top, inside under the mark -- each only where it fits its box */
  const C=[[yTop-9,false],[hasM&&yMark<yTop?yMark-9:NaN,false],[yTop+10,true],[hasM?yMark+10:NaN,true]]
    .filter(([y,ins])=>isFinite(y)&&y>=b.y+8&&y<=b.y1-6&&(!ins||y>=yTop+6));
  for(const [y,ins] of C) if(gap(y)>=BAR_CLEAR) return {y,inside:ins};
  if(!C.length) return {y:yTop+10,inside:true};
  let best=C[0]; for(const c of C) if(gap(c[0])>gap(best[0])) best=c;     /* none clears: the widest gap */
  return {y:best[0],inside:best[1]};
}
function barVal(ctx,W,H,x,yTop,b,txt,col,yMark){
  const p=barValY(yTop,yMark,b);
  lab(ctx,W,H,x,p.y,txt,p.inside?'#0b0e16':col,SM_FONT,'center','middle');
}
/* a y for a one-line note ('nothing yet') in an empty bar box that clears
   every mark (pixel ys) by BAR_CLEAR: the top, then the middle, then the first
   clear line scanning down.  At the top alone it sat on a high mark (a custom
   spin state), caught by the layout check. */
function freeY(b,marks){
  const ok=y=>marks.every(m=>!isFinite(m)||Math.abs(y-m)>=BAR_CLEAR);
  if(ok(b.y+12)) return b.y+12;
  if(ok(b.y+b.h/2)) return b.y+b.h/2;
  for(let y=b.y+8;y<=b.y1-8;y++) if(ok(y)) return y;
  return b.y+12;
}
/* counts as people write them: 10 000, not 10000 */
function fmtN(n){ return n>=10000?String(n).replace(/(\d)(?=(\d{3})+$)/g,'$1 '):String(n); }
/* a panel title that fits its own panel (Known-bad: long titles overran) */
function fitTitle(b,longT,shortT){ return plain(longT).length*13*0.52+10>b.w?shortT:longT; }
/* the bottom-anchored caption, measured first, clear of the #hint line */
function capLayout(ctx,W,H,full,short,left,right,minTop){
  const capW=Math.max(260,Math.min(W-148,right-left));
  return fitCaption(ctx,W,H-HINT_H,full,short,capW,minTop);
}
function drawCap(ctx,left,fit){ caption(ctx,left,fit.capY,fit.txt,fit.capW,'#767e92',CAP_FONT); }
/* a caption names only the panels that are drawn.  Lay out with the caption
   that names the optional panel (capOf(true)); when the panel then does not
   fit, lay out again with the one that does not name it and keep the panel
   OFF, even if the shorter caption frees the room (the text already said
   nothing of it).  The Bloch caption named its fringe panel where 820 x 520
   skips it, looked at. */
function layoutNamed(capOf,geoOf,fits){
  let Cap=capOf(true), G=geoOf(Cap);
  if(!fits(G)){ Cap=capOf(false); G=geoOf(Cap); G.panelOff=true; }
  return {Cap,G};
}
/* a percentage bar pair: two vertical bars (+ outcome, - outcome) in box b,
   values as fractions of 1, labels under the bars, optional expected marks */
function barPair(ctx,b,f1,f2,lab1,lab2,expect1,opts){
  opts=opts||{};
  frame(ctx,b,COL.edge);
  const bw=Math.min(46,b.w*0.26), x1=b.x+b.w*0.30, x2=b.x+b.w*0.70;
  const H=b.h, y0=b.y1;
  const bar=(xc,f,col)=>{ if(!(f>0)) return; const hh=Math.min(1,f)*H; ctx.fillStyle=col; ctx.fillRect(xc-bw/2,y0-hh,bw,hh); };
  bar(x1,f1,COL.pos); bar(x2,f2,COL.neg);
  if(expect1!==null&&expect1!==undefined&&isFinite(expect1)){
    ctx.beginPath(); const e1=y0-expect1*H, e2=y0-(1-expect1)*H;
    ctx.moveTo(x1-bw/2-6,e1); ctx.lineTo(x1+bw/2+6,e1); ctx.moveTo(x2-bw/2-6,e2); ctx.lineTo(x2+bw/2+6,e2);
    ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
  }
  ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillStyle=COL.pos; ctx.fillText(plain(lab1),x1,b.y1+4); ctx.fillStyle=COL.neg; ctx.fillText(plain(lab2),x2,b.y1+4);
  if(opts.values){ ctx.font='10.5px -apple-system, sans-serif'; ctx.fillStyle=COL.text; ctx.textBaseline='bottom';
    ctx.fillText(opts.values[0],x1,Math.max(b.y+12,y0-Math.min(1,f1||0)*H-3)); ctx.fillText(opts.values[1],x2,Math.max(b.y+12,y0-Math.min(1,f2||0)*H-3)); }
  return {x1,x2,bw};
}
