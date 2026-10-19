
/* ================================================================== *
 *  the histogram of sample MEANS, and the four views                  *
 * ================================================================== */
/* the field's aspect sentence — a fixed-width number, so a caption can be
   measured with a placeholder before the map that fills it in exists */
function aspectNote(rTxt){
  return ' The field’s vertical scale is ×'+rTxt+' of its horizontal (1.00 is true aspect, and anything less is the stage being too short for the trajectory).';
}
/* one sample-mean histogram.  `own` fits the panel to this n; without it the
   axis is the parent's, which is what makes the four sizes comparable. */
function drawMeanHist(ctx,b,M,means,size,opt){
  const o=opt||{}, E=M.exact, se=E.sd/Math.sqrt(size), w=o.w||M.binW;
  const half=o.own?Math.max(4.6*se,3*w):4.2*E.sd;
  const lo=E.mean-half, hi=E.mean+half;
  const H=pdlHistogram(means,w);
  const ymax=o.ymax||Math.max(4,Math.ceil(Math.max(4,H.max)*1.2));
  const col=o.col||COL.sizes[PDL.SIZES.indexOf(size)];
  axesT(ctx,b,lo,hi,0,ymax,{title:o.title,xlab:o.xlab,ylab:o.ylab,nx:o.nx||5,ny:3});
  const px=x=>b.x+b.w*(x-lo)/(hi-lo), py=y=>b.y1-b.h*y/ymax;
  const bw=b.w*w/(hi-lo);
  for(let i=0;i<H.counts.length;i++){
    const c=H.counts[i]; if(!c) continue;
    const X0=Math.max(b.x,px((H.lo+i)*w)), X1=Math.min(b.x1,px((H.lo+i+1)*w));
    if(X1<=X0) continue;
    if(M.st.blocks&&bw>=3.5&&c<=ymax&&b.h/ymax>=5){
      const cellH=b.h/ymax, gap=clamp(0.18*cellH,2.2,7), gx=Math.min(gap,(X1-X0)*0.3);
      for(let k=0;k<c;k++){ ctx.fillStyle=rgba(col,0.85);
        ctx.fillRect(X0+gx/2,py(k+1)+gap/2,X1-X0-gx,Math.max(1.5,cellH-gap)); }
    } else { ctx.fillStyle=rgba(col,0.75); ctx.fillRect(X0,py(c),X1-X0,b.y1-py(c)); }
    POLY_SEGS.push(X0,py(c),X1,py(c));
  }
  /* the exact sampling law: a normal of sd σ/√n, scaled to the counts — not
     a fit, and drawn only when there are enough samples for a shape */
  if(o.showNormal!==false&&means.length>2){
    const xs=[], ys=[];
    for(let i=0;i<=180;i++){ const x=lo+(hi-lo)*i/180; xs.push(x);
      ys.push(means.length*w*Math.exp(-0.5*Math.pow((x-E.mean)/se,2))/(se*Math.sqrt(2*Math.PI))); }
    pl(ctx,b,xs,ys,lo,hi,0,ymax,COL.ref,1.6);
  }
  if(o.showSe!==false){
    const a=px(E.mean-se), c=px(E.mean+se), y=b.y+9;
    ctx.strokeStyle=COL.ref; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(a,y); ctx.lineTo(c,y); ctx.moveTo(a,y-4); ctx.lineTo(a,y+4);
    ctx.moveTo(c,y-4); ctx.lineTo(c,y+4); ctx.stroke();
  }
  const mx=px(E.mean);
  ctx.strokeStyle=rgba(COL.ref,0.8); ctx.lineWidth=1.2; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(mx,b.y); ctx.lineTo(mx,b.y1); ctx.stroke(); ctx.setLineDash([]);
  /* the measured spread, so the comparison is a number and not an impression */
  if(o.showSe!==false&&means.length>2){
    const s1=pdlSd(means,1);
    const a2=px(E.mean-s1), c2=px(E.mean+s1), y2=b.y+20;
    ctx.strokeStyle=COL.pos; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(a2,y2); ctx.lineTo(c2,y2); ctx.moveTo(a2,y2-4); ctx.lineTo(a2,y2+4);
    ctx.moveTo(c2,y2-4); ctx.lineTo(c2,y2+4); ctx.stroke();
  }
  return {px,py,lo,hi,ymax,se};
}

/* ================================================================== *
 *  view 1: the field — PhET's Sampling screen                         *
 * ================================================================== */
function fieldCaptionS(M,rTxt){
  const se=M.exact.sd/Math.sqrt(M.st.pN);
  return {full:'A sample is '+M.st.pN+' launches, and only one number survives it: the mean. That number joins the histogram below, and the histogram is NOT the histogram of landing distances — it is far narrower. With σ = '
            +fmt(M.exact.sd,3)+' m for one launch, the exact standard error at n = '+M.st.pN+' is σ/√n = '+fmt(se,3)
            +(M.mstat.n>1
              ?' m (the orange bar; the green bar below it is the spread actually measured so far).'
              :' m (the orange bar). The green bar beside it is the spread the samples themselves show, and one sample has no spread — it appears with the second.')+aspectNote(rTxt),
          short:'One dot per sample, and the dot is its mean: σ/√n = '+fmt(se,3)+' m at n = '+M.st.pN+'.'+aspectNote(rTxt)};
}
function drawFieldView(ctx,W,H,M){
  const ph=fieldCaptionS(M,'1.00');
  const L=labStage(ctx,W,H,ph.full,ph.short,{histFrac:0.52,fieldWant:fieldWantH(M)});
  const map=drawField(ctx,L.field,M,{showExactMean:true});
  const F=M.F;
  if(F.landed.length){
    const xs=F.landed.slice(-(F.size||1)).map(p=>p.x), m=pdlMean(xs);
    const X=map.X(m);
    ctx.strokeStyle=COL.live; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(X,map.y0+4); ctx.lineTo(X,map.y0-26); ctx.stroke();
    lab(ctx,W,H,X,map.y0-29,'x̄ = '+fmt(m,2)+' m',COL.live,LAB_FONT,'center','bottom');
  }
  drawMeanHist(ctx,L.hist,M,M.means,M.st.pN,{title:'the sample means, n = '+M.st.pN,
    xlab:'sample mean x̄, m',ylab:'samples',own:true,ymax:M.zoomMax,
    showNormal:M.st.showSe,showSe:M.st.showSe,nx:6});
  lab(ctx,W,H,L.hist.x1-4,L.hist.y+9,M.mstat.n+(M.mstat.n===1?' sample · bin ':' samples · bin ')+fmt(M.binW,2)+' m',COL.dim,SM_FONT,'right','middle');
  const cap=fieldCaptionS(M,fmt(map.ratio,2));
  caption(ctx,L.left,L.capY,L.capTxt===ph.full?cap.full:cap.short,L.capW,'#767e92',CAP_FONT);
  return {map,L};
}

/* ================================================================== *
 *  view 2: the four sample sizes — PhET's thumbnail row, full size    *
 * ================================================================== */
function sizesCaption(M,few){
  const E=M.exact;
  const note=few?' This stage is too narrow for four panels, so it shows the two ends of the range; a wider one shows all four.':'';
  return {full:'The same launcher at every sample size PhET offers, '+M.st.sM+' samples each, all of them on ONE axis. The centre never moves — averaging biases nothing — and the width falls as 1/√n: from σ = '
            +fmt(E.sd,3)+' m for a single launch to '+fmt(E.sd/Math.sqrt(40),3)+' m at n = 40, a factor of √40 = 6.32. The orange bar on each is σ/√n from the exact law; the green bar is the spread these '
            +M.st.sM+' samples actually show.'+note,
          short:'Sample sizes on one axis: the width falls as 1/√n, the centre does not move.'+note};
}
function drawSizesView(ctx,W,H,M){
  /* a narrow stage cannot carry four stacked panels: four 24 px boxes with
     their own titles and tick labels overrun the caption.  Show the two ends
     of the range instead, and say so. */
  const few=isNarrow(W);
  const sets=few?[M.sets[0],M.sets[M.sets.length-1]]:M.sets;
  const ph=sizesCaption(M,few);
  const L=labStage(ctx,W,H,ph.full,ph.short,{nBottom:0});
  const b=L.main, n=sets.length;
  /* each panel needs room for its own title above and its tick labels below,
     or panel i's ticks land in panel i+1's title — which is how the first
     layout sweep failed */
  const gap=10, titleH=24, tickH=20, slot=(b.h-gap*(n-1))/n;
  const boxH=Math.max(28,slot-titleH-tickH);
  sets.forEach((S,i)=>{
    const p=box(b.x,b.y+i*(slot+gap)+titleH,b.w,boxH);
    const k=PDL.SIZES.indexOf(S.n);
    drawMeanHist(ctx,p,M,S.means,S.n,{title:'n = '+S.n+'  ·  σ/√n = '+fmt(M.exact.sd/Math.sqrt(S.n),3)+' m',
      xlab:(i===n-1&&boxH>=46)?'sample mean x̄, m':null,ylab:null,w:M.binW,
      showNormal:M.st.showNormal,showSe:true,nx:7,col:COL.sizes[k]});
    lab(ctx,W,H,p.x1-4,p.y+9,'measured '+fmt(S.stat.sd1,3)+' m',COL.pos,SM_FONT,'right','middle');
  });
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
  return {b,L};
}

/* ================================================================== *
 *  view 3: one launch — the parent the samples come from              *
 * ================================================================== */
function parentCaption(M){
  const E=M.exact;
  return {full:'Before the samples, the parent. These are '+M.stat.n+' single launches'
            +(M.st.showDensity
              ?'; the orange curve is not fitted to them but computed from the two Gaussians PhET launches with, ∫f_θ(θ)f_v(v*(r,θ))/|∂x/∂v| dθ.'
              :', with the exact density switched off, so nothing here is fitted or computed — the bars are the data alone.')
            +' Its standard deviation is σ = '
            +fmt(E.sd,4)+' m, and that is the σ every standard error on the other views divides by √n. '
            +(Math.abs(E.skew)>0.05||Math.abs(E.kurt)>0.05
              ? 'It is also visibly not a normal: its skewness is '+fmt(E.skew,3)+' and its excess kurtosis '+fmt(E.kurt,3)+', which is why the limit theorem has anything to say.'
              : 'This launcher’s parent happens to be very nearly normal already — skewness '+fmt(E.skew,3)+', excess kurtosis '+fmt(E.kurt,3)+' — so there is little for the theorem to do here; launchers 2 and 6 are the ones with a shape to lose.'),
          short:'The parent distribution: σ = '+fmt(E.sd,4)+' m, skewness '+fmt(E.skew,3)+'.'
            +(M.st.showDensity?' The curve is computed, not fitted.':' Its exact density is switched off.')};
}
function drawParentView(ctx,W,H,M){
  const ph=parentCaption(M);
  const L=labStage(ctx,W,H,ph.full,ph.short,{histFrac:0.56,fieldWant:fieldWantH(M)});
  const map=drawField(ctx,L.field,M,{showExactMean:true});
  const b=L.hist, E=M.exact, w=M.binW;
  const lo=Math.max(0,E.mean-5*E.sd), hi=E.mean+5*E.sd;
  const xs=[], ys=[];
  { const C=pdlPdfCurve(M.cfg,lo,hi,200); xs.push.apply(xs,C.xs); ys.push.apply(ys,C.ys); }
  let ymax=0; for(const y of ys) ymax=Math.max(ymax,y);
  const dens=M.hist.counts.map(c=>c/Math.max(1,M.stat.n)/w);
  for(const d of dens) ymax=Math.max(ymax,d);
  ymax=Math.max(1e-6,ymax*1.2);
  axesT(ctx,b,lo,hi,0,ymax,{title:M.stat.n+(M.st.showDensity?' launches against the exact density':' launches'),
    xlab:'landing distance x, m',ylab:'density, 1/m',nx:6,ny:4});
  const px=x=>b.x+b.w*(x-lo)/(hi-lo), py=y=>b.y1-b.h*y/ymax;
  for(let i=0;i<M.hist.counts.length;i++){
    const c=M.hist.counts[i]; if(!c) continue;
    const X0=Math.max(b.x,px((M.hist.lo+i)*w)), X1=Math.min(b.x1,px((M.hist.lo+i+1)*w));
    if(X1<=X0) continue;
    ctx.fillStyle=rgba(COL.pos,0.55); ctx.fillRect(X0,py(dens[i]),X1-X0,b.y1-py(dens[i]));
    POLY_SEGS.push(X0,py(dens[i]),X1,py(dens[i]));
  }
  if(M.st.showDensity) pl(ctx,b,xs,ys,lo,hi,0,ymax,COL.ref,2);
  for(const [v,col,tx] of [[E.mean,COL.ref,'μ = '+fmt(E.mean,3)+' m'],
                           [M.stat.mean,COL.live,'x̄ = '+(M.stat.mean===null?'—':fmt(M.stat.mean,3)+' m')]]){
    if(v===null) continue;
    const X=px(v);
    ctx.strokeStyle=col; ctx.lineWidth=1.4; ctx.setLineDash(col===COL.ref?[5,4]:[]);
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,X,b.y+6,tx,col,SM_FONT,'center','top');
  }
  /* ±σ, so the number the other views divide is on the picture */
  const y=b.y+24;
  ctx.strokeStyle=COL.ref; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(px(E.mean-E.sd),y); ctx.lineTo(px(E.mean+E.sd),y);
  ctx.moveTo(px(E.mean-E.sd),y-4); ctx.lineTo(px(E.mean-E.sd),y+4);
  ctx.moveTo(px(E.mean+E.sd),y-4); ctx.lineTo(px(E.mean+E.sd),y+4); ctx.stroke();
  lab(ctx,W,H,px(E.mean+E.sd)+6,y,'μ ± σ',COL.ref,SM_FONT,'left','middle');
  legendReg(ctx,b,[[COL.pos,M.stat.n+' launches']].concat(M.st.showDensity?[[COL.ref,'the exact density']]:[]));
  const cap=parentCaption(M);
  caption(ctx,L.left,L.capY,L.capTxt===ph.full?cap.full:cap.short,L.capW,'#767e92',CAP_FONT);
  return {map,b,L};
}
