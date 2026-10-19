
/* ================================================================== *
 *  the stage: the ceiling, the springs, the masses, the lines, the    *
 *  ruler — and PhET's three screens drawn on it                       *
 * ================================================================== */
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it */
const HINT_H=18;
const RULER_L=0.80, RULER_W=0.12;       /* the drawn ruler, metres */

/* An axis whose tick COUNT follows the panel size and whose decimals follow the
   tick SPACING.  Both are Known-bad traps: six ticks in a 60 px box collide,
   and fmt(t,2) prints "0.00" five times over a 0.01 range. */
function decOf(ts){
  if(ts.length<2) return 2;
  const st=Math.abs(ts[1]-ts[0]);
  return clamp(Math.ceil(-Math.log10(st))+1,0,6);
}
function ax2(b,xlo,xhi,ylo,yhi,opt){
  const yt=sparseTicks(Math.min(ylo,yhi),Math.max(ylo,yhi),b.h);
  const xt=sparseTicks(Math.min(xlo,xhi),Math.max(xlo,xhi),b.w/2.4);
  const yd=decOf(yt), xd=decOf(xt);
  return Object.assign({yticks:yt,xticks:xt,yfmt:t=>fmt(t,yd),xfmt:t=>fmt(t,xd)},opt||{});
}
/* reserve a rectangle in the label registry so later lab() calls dodge it */
function regBox(x0,y0,x1,y1){ LABELS.push([x0,y0,x1,y1]); }


function xExtent(M){
  const xs=M.springs.map(s=>s.x);
  let lo=Math.min.apply(null,xs)-0.30, hi=Math.max.apply(null,xs)+0.30;
  if(M.st.ruler){ lo=Math.min(lo,M.st.rulerX-0.03); hi=Math.max(hi,M.st.rulerX+RULER_W+0.03); }
  return [lo,hi];
}
function lowestPoint(M){
  let lo=-0.06;
  for(const s of M.springs){ if(!s.on) continue;
    lo=Math.min(lo,s.bottom-HOOK_C-massHeight(s.m)-0.03); }
  if(M.st.ruler) lo=Math.min(lo,M.st.rulerY-RULER_L-0.02);
  if(M.st.movLine) lo=Math.min(lo,M.st.movY-0.02);
  return lo;
}
/* the stage is intrinsically tall and thin (PhET's own geometry: 1.47 m of
   ceiling over 0.3 m between the springs), so on a wide canvas it gets a
   narrow column of its own and the analysis panel sits BESIDE it rather than
   under it — stacked, the stage used a quarter of the width and the picture
   was mostly background. */
function splitLayout(ctx,W,H,v){
  const a=viewCaps(v);
  if(isNarrow(W)) return stageLayout(ctx,W,H-HINT_H,a[0],a[1],1,0.42,1);
  const left=56, right=W-RO_W-44, top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,a[0],a[1],capW,top+220);
  const bot=fit.capY-16;
  const stageW=clamp(Math.round(0.34*(right-left)),240,430);
  const px=left+stageW+72;
  return {narrow:false,left,right,capY:fit.capY,capTxt:fit.txt,capW,
          main:box(left,top,stageW,Math.max(120,bot-top)),
          bottom:[box(px,top+16,Math.max(170,right-px),Math.max(110,bot-top-54))]};
}
function stageMap(M,b){
  const xe=xExtent(M), ylo=lowestPoint(M);
  return worldFitUp(b,{xmin:xe[0],xmax:xe[1],ymin:ylo,ymax:CEILING_Y+0.09},0.01);
}
/* the hatched ceiling PhET hangs its springs from */
function drawCeiling(ctx,map,x0,x1){
  const Y=map.Y(CEILING_Y);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=2.4;
  ctx.beginPath(); ctx.moveTo(map.X(x0),Y); ctx.lineTo(map.X(x1),Y); ctx.stroke();
  POLY_SEGS.push(map.X(x0),Y,map.X(x1),Y);
  ctx.strokeStyle=rgba(COL.struct,0.4); ctx.lineWidth=1;
  for(let X=map.X(x0);X<map.X(x1);X+=9){
    ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(X+7,Y-7); ctx.stroke();
  }
}
function drawFloor(ctx,map,x0,x1){
  const Y=map.Y(FLOOR_Y);
  ctx.strokeStyle=rgba(COL.dim,0.55); ctx.lineWidth=1.4; ctx.setLineDash([]);
  ctx.beginPath(); ctx.moveTo(map.X(x0),Y); ctx.lineTo(map.X(x1),Y); ctx.stroke();
}
/* the coil: a helix whose pitch follows the length and whose line weight
   follows the spring constant, as PhET's OscillatingSpringNode does */
/* COILS*20 points: 20 samples a turn puts one exactly on each quarter, so the
   drawn coil's widest point IS COIL_R and the display list can be measured
   against it (at 18 a turn the peak is never sampled and the extent is 0.985 of
   the radius, which is a fact about the sampling, not about the spring) */
function drawSpring(ctx,map,x,len,k,col){
  const pts=coilPoints(x,CEILING_Y,len,COILS*20);
  ctx.beginPath();
  for(let i=0;i<pts.length;i++){ const X=map.X(pts[i][0]), Y=map.Y(pts[i][1]);
    if(i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); }
  ctx.strokeStyle=col; ctx.lineWidth=coilWidth(k); ctx.lineJoin='round'; ctx.lineCap='round';
  ctx.stroke(); ctx.lineWidth=1;
  for(let i=1;i<pts.length;i++) POLY_SEGS.push(map.X(pts[i-1][0]),map.Y(pts[i-1][1]),map.X(pts[i][0]),map.Y(pts[i][1]));
}
/* PhET's mass block: a cylinder of its own size rule, hung from a hook */
function drawMass(ctx,map,x,topY,m,col,label,dragging){
  const r=massRadius(m), hh=massHeight(m);
  const X0=map.X(x-r), X1=map.X(x+r), Yt=map.Y(topY), Yb=map.Y(topY-hh);
  ctx.beginPath(); ctx.moveTo(map.X(x),map.Y(topY+HOOK_H)); ctx.lineTo(map.X(x),Yt);
  ctx.strokeStyle=COL.coil; ctx.lineWidth=1.6; ctx.stroke();
  ctx.fillStyle=shade(col,dragging?0.95:0.62); ctx.fillRect(X0,Yt,X1-X0,Yb-Yt);
  ctx.strokeStyle=dragging?'#fff':shade(col,1); ctx.lineWidth=dragging?2:1.3;
  ctx.strokeRect(X0,Yt,X1-X0,Yb-Yt);
  POLY_SEGS.push(X0,Yt,X1,Yt,X1,Yt,X1,Yb,X1,Yb,X0,Yb,X0,Yb,X0,Yt);
  if(label&&Yb-Yt>13&&X1-X0>plain(label).length*6.2){
    ctx.fillStyle='#0a0c12'; ctx.font='bold 11px -apple-system, sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(plain(label),(X0+X1)/2,(Yt+Yb)/2);
    const lw=plain(label).length*11*0.52;
    regBox((X0+X1)/2-lw/2,(Yt+Yb)/2-6.3,(X0+X1)/2+lw/2,(Yt+Yb)/2+6.3); }
}
function massTopY(s){ return s.bottom-HOOK_C; }
function massRectPx(map,s){
  const r=massRadius(s.m), top=massTopY(s);
  return {x:map.X(s.x-r),y:map.Y(top),x1:map.X(s.x+r),y1:map.Y(top-massHeight(s.m))};
}
/* a dashed rule across the stage with a right-hand label */
function ruleLine(ctx,map,W,H,x0,x1,y,col,txt){
  const Y=map.Y(y);
  ctx.strokeStyle=col; ctx.lineWidth=1.3; ctx.setLineDash([7,5]);
  ctx.beginPath(); ctx.moveTo(map.X(x0),Y); ctx.lineTo(map.X(x1),Y); ctx.stroke(); ctx.setLineDash([]);
  if(txt) lab(ctx,W,H,map.X(x0),Y-4,txt,col,SM_FONT,'left','bottom');
}
function drawRuler(ctx,map,W,H,st){
  const x=st.rulerX, yTop=st.rulerY;
  const X0=map.X(x), X1=map.X(x+RULER_W), Yt=map.Y(yTop), Yb=map.Y(yTop-RULER_L);
  ctx.fillStyle='rgba(16,19,27,.92)'; ctx.fillRect(X0,Yt,X1-X0,Yb-Yt);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.strokeRect(X0,Yt,X1-X0,Yb-Yt);
  ctx.font='9px -apple-system, sans-serif'; ctx.textBaseline='middle';
  const numbered=(map.s*0.10>=18);          /* 10 cm must be 18 px before it is numbered */
  for(let c=0;c<=80;c++){
    const Y=map.Y(yTop-c/100);
    const major=(c%10===0), mid=(c%5===0);
    ctx.strokeStyle=rgba(COL.struct,major?0.9:0.45); ctx.lineWidth=major?1.2:0.8;
    ctx.beginPath(); ctx.moveTo(X0,Y); ctx.lineTo(X0+(major?(X1-X0)*0.55:(mid?(X1-X0)*0.35:(X1-X0)*0.2)),Y); ctx.stroke();
    /* the numbers sit OUTSIDE the ruler body: inside a 29 px scale they land
       on their own tick marks */
    if(major&&c>0&&numbered){ ctx.fillStyle=COL.struct; ctx.textAlign='left'; ctx.fillText(String(c),X1+3,Y);
      regBox(X1+3,Y-5.2,X1+3+String(c).length*4.7,Y+5.2); }
  }
  if(numbered){ ctx.fillStyle=COL.dim; ctx.textAlign='left'; ctx.textBaseline='bottom';
    ctx.font='9.5px -apple-system, sans-serif'; ctx.fillText('cm',X0,Yt-3);
    regBox(X0,Yt-14,X0+12,Yt-3); }
}
/* the whole stage, shared by the stretch, bounce and lab views */
function drawStageBox(ctx,W,H,M,b){
  const st=M.st, map=stageMap(M,b), xe=xExtent(M);
  /* the full-width rules start clear of the ruler, so their labels do not land
     on its scale */
  const rx=st.ruler?Math.max(xe[0]+0.05,st.rulerX+RULER_W+0.10):xe[0]+0.05;
  drawCeiling(ctx,map,xe[0]+0.02,xe[1]-0.02);
  drawFloor(ctx,map,xe[0]+0.02,xe[1]-0.02);
  lab(ctx,W,H,map.X(xe[0]+0.03),map.Y(FLOOR_Y)+11,'floor',COL.dim,SM_FONT,'left','top');
  for(const s of M.springs) drawSpring(ctx,map,s.x,CEILING_Y-(s.on?s.bottom:CEILING_Y-L0),s.k,COL.coil);
  for(let i=0;i<M.springs.length;i++){
    const s=M.springs[i], col=i===0?COL.mass1:COL.mass2;
    if(!s.on) continue;
    drawMass(ctx,map,s.x,massTopY(s),s.m,col,(s.myst&&!st.reveal)?'?':fmt(1000*s.m,0)+' g',
             DRAG.what==='mass'&&DRAG.sp===s.i);
  }
  if(st.ruler) drawRuler(ctx,map,W,H,st);
  /* the spring labels go ABOVE the ceiling: under it they lay on the coils */
  for(let i=0;i<M.springs.length;i++){
    const s=M.springs[i];
    lab(ctx,W,H,map.X(s.x),map.Y(CEILING_Y)-7,'k = '+fmt(s.k,0)+' N/m',COL.dim,LAB_FONT,'center','bottom');
  }
  if(st.natLine) ruleLine(ctx,map,W,H,rx,xe[1]-0.12,CEILING_Y-L0,COL.struct,'unstretched length');
  /* the resting-position lines are drawn per spring, short, so two springs of
     different stiffness do not paint one line over the other */
  /* the movable line is labelled BEFORE the resting lines so its label wins the
     space: its height is the thing the reader has set by hand, and the resting
     value is in the readout as well */
  if(st.movLine) ruleLine(ctx,map,W,H,rx,xe[1]-0.12,st.movY,COL.live,'movable line '+fmt(100*st.movY,1)+' cm');
  if(st.restLine) for(let i=0;i<M.springs.length;i++){
    const s=M.springs[i]; if(!s.on) continue;
    const y=CEILING_Y-L0-s.ye;
    ruleLine(ctx,map,W,H,s.x-0.15,s.x+0.15,y,COL.ref,null);
    /* the label hangs off the LEFT end of its line: on the line it lands on a
       block, and off the right it runs into the analysis panel beside the stage */
    lab(ctx,W,H,map.X(s.x-0.16)-4,map.Y(y),'resting '+sigf(100*s.ye,3)+' cm',
        COL.ref,SM_FONT,'right','middle');
  }
  const anyBust=M.springs.some(s=>s.on&&s.floorBust);   /* the block, not the spring end */
  if(anyBust) lab(ctx,W,H,map.X(xe[0]+0.03),map.Y(FLOOR_Y)+26,'below the floor — PhET too',COL.ref,SM_FONT,'left','top');
  lab(ctx,W,H,b.x+3,b.y+2,'true shape, '+sigf(map.s/100,3)+' px per cm',COL.dim,SM_FONT,'left','top');
  return map;
}
/* the height-against-time strip the bounce and lab views draw underneath */
function drawStrip(ctx,W,H,M,b,withTrace){
  /* the window is about four periods of the slowest spring, and it GROWS from
     the release rather than opening on six empty seconds */
  let Tm=1;
  for(const s of M.springs) if(s.on) Tm=Math.max(Tm,isFinite(s.Td)?s.Td:s.T0);
  const span=clamp(4*Tm,1.5,HWIN);
  const t1=Math.max(M.t,Math.min(span,1.4*Tm)), t0=Math.max(0,t1-span);
  let ymax=0.02;
  for(const s of M.springs) if(s.on) ymax=Math.max(ymax,2.05*s.ye,1.05*Math.abs(s.y));
  axesR(ctx,b,t0,t1,ymax,0,ax2(b,t0,t1,0,ymax,{xlab:'time, s',ylab:'extension, cm',
    yfmt:t=>fmt(100*t,0),title:titleFor(b,'the spring below its unstretched end','extension')}));
  for(let i=0;i<M.springs.length;i++){
    const s=M.springs[i], col=i===0?COL.mass1:COL.mass2;
    if(!s.on) continue;
    polyline(ctx,b,[t0,t1],[s.ye,s.ye],t0,t1,ymax,0,COL.ref,1.1,[6,4]);
    if(s.hist&&s.hist.length>1) polyline(ctx,b,s.ht,s.hist,t0,t1,ymax,0,col,1.7);
    marker(ctx,b,t0,t1,ymax,0,Math.min(M.t,t1),s.y,col);
  }
  polyline(ctx,b,[t0,t1],[0,0],t0,t1,ymax,0,rgba(COL.struct,0.5),1.1,[3,4]);
  { const items=[];
    for(let i=0;i<M.springs.length;i++){ const s=M.springs[i];
      if(s.on) items.push([i===0?COL.mass1:COL.mass2,s.label+', '+fmt(1000*s.m,0)+' g on '+fmt(s.k,0)+' N/m']); }
    items.push([COL.ref,'resting point, mg/k']);
    if(withTrace) items.push([COL.live,'the period trace']);
    legendAuto(ctx,b,items); }
  /* PhET's period trace: the crossings two apart are one whole period */
  if(withTrace&&M.springs[0].on){
    const c=M.springs[0].cross.filter(x=>x>=t0);
    for(const tc of c){
      const X=b.x+b.w*(tc-t0)/(t1-t0);
      ctx.strokeStyle=rgba(COL.live,0.85); ctx.lineWidth=1.2;
      ctx.beginPath(); ctx.moveTo(X,b.y1-10); ctx.lineTo(X,b.y1); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y+10); ctx.stroke();
    }
    const T=M.springs[0].Tmeas;
    if(isFinite(T)&&c.length>=3){
      const a=c[c.length-3], z=c[c.length-1];
      const Xa=b.x+b.w*(a-t0)/(t1-t0), Xz=b.x+b.w*(z-t0)/(t1-t0), Y=b.y+26;
      ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.moveTo(Xa,Y); ctx.lineTo(Xz,Y); ctx.stroke();
      lab(ctx,W,H,(Xa+Xz)/2,Y-9,'period trace: T = '+sigf(T,4)+' s',COL.live,SM_FONT,'center','bottom');
    }
  }
}
/* ---- view 1: the stretch ------------------------------------------ */
const STR_CAP_FULL='PhET&rsquo;s Stretch screen. Hang a mass on either spring and it settles where the spring&rsquo;s pull equals the weight, '
  +'at y = mg/k: the orange line. Twice the mass is twice the stretch; twice the spring constant is half of it. The springs are drawn at true '
  +'shape (no vertical exaggeration); the panel beside them is the same law as a straight line through the origin.';
const STR_CAP_SHORT='PhET&rsquo;s Stretch screen: a mass settles at y = mg/k, drawn at true shape.';
function drawStretch(ctx,W,H,M){
  const L=layoutFor(ctx,W,H,'str');
  const map=drawStageBox(ctx,W,H,M,L.main);
  const bb=L.bottom[0];
  if(bb){
    const ks=[M.springs[0].k,M.springs[1]?M.springs[1].k:M.springs[0].k];
    const mmax=MASS_G_MAX/1000, gg=M.g;
    let ymax=0.02; for(const k of ks) ymax=Math.max(ymax,mmax*gg/k*1.08);
    const xs=[]; for(let i=0;i<=40;i++) xs.push(mmax*i/40);
    axesR(ctx,bb,0,1000*mmax,0,100*ymax,ax2(bb,0,1000*mmax,0,100*ymax,{xlab:'mass, g',ylab:'extension, cm',
      title:titleFor(bb,'Hooke&rsquo;s law: the extension is a straight line through the origin','Hooke&rsquo;s law')}));
    for(let i=0;i<M.springs.length;i++){
      const s=M.springs[i], col=i===0?COL.mass1:COL.mass2;
      polyline(ctx,bb,xs.map(m=>1000*m),xs.map(m=>100*m*gg/s.k),0,1000*mmax,0,100*ymax,col,1.8);
      if(s.on) marker(ctx,bb,0,1000*mmax,0,100*ymax,1000*s.m,100*s.ye,COL.live);
    }
    legendAuto(ctx,bb,M.springs.map((s,i)=>[i===0?COL.mass1:COL.mass2,s.label+', k = '+fmt(s.k,0)+' N/m'])
      .concat([[COL.live,'what hangs there now']]));
    lab(ctx,W,H,bb.x1-6,bb.y1-8,'slope g/k = '+sigf(100*gg/M.springs[0].k,3)+' cm per 1000 g',COL.dim,SM_FONT,'right','bottom');
    if(M.springs.length>1&&M.springs[0].k===M.springs[1].k)
      lab(ctx,W,H,bb.x+8,bb.y1-8,'both springs are '+fmt(M.springs[0].k,0)+' N/m: the two lines coincide',COL.ref,SM_FONT,'left','bottom');
  }
  drawCaption(ctx,L);
}
/* ---- view 2: the bounce ------------------------------------------- */
const BNC_CAP_FULL='PhET&rsquo;s Bounce screen, with its damping off as PhET leaves it. Gravity only decides where the resting point is; about '
  +'that point the motion is the plain harmonic oscillator, so a mass let go from the unstretched end swings down exactly 2mg/k and back. '
  +'The strip beside it is the same two springs against time, with their resting points in orange.';
const BNC_CAP_SHORT='PhET&rsquo;s Bounce screen: released from the unstretched end, the swing is exactly 2mg/k.';
function drawBounce(ctx,W,H,M){
  const L=layoutFor(ctx,W,H,'bnc');
  drawStageBox(ctx,W,H,M,L.main);
  if(L.bottom[0]) drawStrip(ctx,W,H,M,L.bottom[0],false);
  drawCaption(ctx,L);
}
/* ---- view 3: the lab ---------------------------------------------- */
const LAB_CAP_FULL='PhET&rsquo;s Lab screen: one spring, a mass slider and a gravity you can move from the Moon to Jupiter &mdash; or to Planet X, '
  +'whose value PhET hides. The period trace marks the spring crossing its resting point; two crossings apart is one whole period, and it is '
  +'2&pi;&radic;(m/k) whatever the gravity. Read the stretch off the ruler and g = k y/m gives Planet X away.';
const LAB_CAP_SHORT='PhET&rsquo;s Lab screen: the period trace measures 2&pi;&radic;(m/k), and the stretch gives the gravity away.';
function drawLab(ctx,W,H,M){
  const L=layoutFor(ctx,W,H,'lab');
  drawStageBox(ctx,W,H,M,L.main);
  if(L.bottom[0]) drawStrip(ctx,W,H,M,L.bottom[0],M.st.trace);
  drawCaption(ctx,L);
}
