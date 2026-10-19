
/* ================================================================== *
 *  view 3: the measures — PhET's Measures screen                      *
 * ================================================================== */
function measCaption(M,rTxt){
  const S=M.stat;
  const conv=S.n>1?' At n = '+S.n+' the two standard-deviation conventions differ by a factor '+fmt(Math.sqrt(S.n/(S.n-1)),4)+'; PhET reports the n − 1 one, and so does the readout.'
                  :' PhET returns no standard deviation below two projectiles, and neither does this.';
  return {full:'The same field, now measured. The magenta rule is the sample mean x̄, the green bar spans x̄ ± s, and the interval tool (drag either edge, or its middle) reports the percentage of the landed shots between them — PhET counts both ends closed.'+conv
            +' The dashed orange rule is where the exact law puts the mean: the sample chases it and never quite sits on it.'+aspectNote(rTxt),
          short:'x̄ (magenta), x̄ ± s (green), and the interval tool’s percentage.'+conv+aspectNote(rTxt)};
}
function drawMeasuresView(ctx,W,H,M){
  const ph=measCaption(M,'1.00');
  const L=labStage(ctx,W,H,ph.full,ph.short,{histFrac:0.46,fieldWant:fieldWantH(M)});
  const map=drawField(ctx,L.field,M);
  const hm=drawHist(ctx,L.hist,M);
  if(M.st.showValues){
    /* PhET's "Values": the individual landing distances, printed on the field.
       Only as many as fit without colliding — the label registry decides. */
    let n=0;
    for(const p of M.F.landed.slice().reverse()){
      if(n>=20) break;
      if(lab(ctx,W,H,map.X(p.x),map.y0-16,fmt(p.x,1),'#9aa2b4','9.5px -apple-system, sans-serif','center','bottom')) n++;
    }
    lab(ctx,W,H,L.field.x1-4,L.field.y+11,n+' of '+M.stat.n+' values fit',COL.dim,SM_FONT,'right','middle');
  }
  drawMeasures(ctx,W,H,L.hist,M,hm);
  if(M.st.showInterval) drawInterval(ctx,W,H,L.hist,M,hm);
  const cap=measCaption(M,fmt(map.ratio,2));
  caption(ctx,L.left,L.capY,L.capTxt===ph.full?cap.full:cap.short,L.capW,'#767e92',CAP_FONT);
  return {map,hm,L};
}

/* ================================================================== *
 *  view 4: the sampling — PhET's Sampling screen                      *
 * ================================================================== */
function sampCaption(M,rTxt){
  const se=M.exact.sd/Math.sqrt(M.st.pN);
  return {full:'A sample is n launches, and it contributes ONE point to the histogram: its mean. With n = '+M.st.pN
            +' the exact standard error is σ/√n = '+fmt(M.exact.sd,3)+'/√'+M.st.pN+' = '+fmt(se,3)
            +' m, against σ = '+fmt(M.exact.sd,3)+' m for a single shot. The four thumbnails below are the same launcher at every sample size, drawn on one axis so the narrowing is a picture rather than a claim — and each carries the sample size it belongs to.'+aspectNote(rTxt),
          short:'One dot per sample, and the dot is its mean: σ/√n = '+fmt(se,3)+' m at n = '+M.st.pN+'.'+aspectNote(rTxt)};
}
function drawSampleHist(ctx,b,M,F,size,opt){
  const o=opt||{}, means=sampleMeans(F);
  const se=M.exact.sd/Math.sqrt(size);
  /* the thumbnails share ONE axis (that is the comparison); the main panel
     fits its own n, or an n = 40 distribution is a sliver three pixels wide */
  const half=o.own?4.6*se:4.2*M.exact.sd;
  const lo=M.exact.mean-half, hi=M.exact.mean+half;
  const w=o.w||0.5;
  const H=pdlHistogram(means,w);
  const ymax=Math.max(4,Math.ceil(Math.max(4,H.max)*1.2));
  const col=o.col||COL.sizes[PDL.SIZES.indexOf(size)];
  axesT(ctx,b,lo,hi,0,ymax,{title:o.title,xlab:o.xlab,ylab:o.ylab,nx:o.nx||5,ny:3});
  const px=x=>b.x+b.w*(x-lo)/(hi-lo), py=y=>b.y1-b.h*y/ymax;
  const bw=b.w*w/(hi-lo);
  for(let i=0;i<H.counts.length;i++){
    const c=H.counts[i]; if(!c) continue;
    const X0=Math.max(b.x,px((H.lo+i)*w)), X1=Math.min(b.x1,px((H.lo+i+1)*w));
    if(X1<=X0) continue;
    ctx.fillStyle=rgba(col,0.75); ctx.fillRect(X0,py(c),X1-X0,b.y1-py(c));
    POLY_SEGS.push(X0,py(c),X1,py(c));
  }
  /* the exact sampling law: a normal of sd σ/√n scaled to the counts */
  if(o.showNormal!==false&&means.length>2){
    const xs=[], ys=[];
    for(let i=0;i<=160;i++){ const x=lo+(hi-lo)*i/160; xs.push(x);
      ys.push(means.length*w*Math.exp(-0.5*Math.pow((x-M.exact.mean)/se,2))/(se*Math.sqrt(2*Math.PI))); }
    pl(ctx,b,xs,ys,lo,hi,0,ymax,COL.ref,1.6);
  }
  if(o.showSe!==false){
    const a=px(M.exact.mean-se), c=px(M.exact.mean+se), y=b.y+9;
    ctx.strokeStyle=COL.ref; ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(a,y); ctx.lineTo(c,y); ctx.moveTo(a,y-4); ctx.lineTo(a,y+4);
    ctx.moveTo(c,y-4); ctx.lineTo(c,y+4); ctx.stroke();
  }
  const mx=px(M.exact.mean);
  ctx.strokeStyle=rgba(COL.ref,0.8); ctx.lineWidth=1.2; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(mx,b.y); ctx.lineTo(mx,b.y1); ctx.stroke(); ctx.setLineDash([]);
  return {px,py,lo,hi,ymax,se};
}
function drawSamplingView(ctx,W,H,M){
  const ph=sampCaption(M,'1.00');
  const L=labStage(ctx,W,H,ph.full+' (the four-sample-size row needs a wider stage than this one.)',
    ph.short+' (the four-sample-size row needs a wider stage than this one.)',
    {histFrac:0.44,nBottom:4,fieldWant:fieldWantH(M)});
  ph.full=ph.full+' (the four-sample-size row needs a wider stage than this one.)';
  const map=drawField(ctx,L.field,M,{showExactMean:true});
  /* the current sample's own mean, on the field */
  const F=M.F;
  if(F.landed.length){
    const xs=F.landed.slice(-(F.size||1)).map(p=>p.x), m=pdlMean(xs);
    const X=map.X(m);
    ctx.strokeStyle=COL.live; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(X,map.y0+4); ctx.lineTo(X,map.y0-26); ctx.stroke();
    lab(ctx,W,H,X,map.y0-29,'x̄ = '+fmt(m,2),COL.live,LAB_FONT,'center','bottom');
  }
  drawSampleHist(ctx,L.hist,M,F,M.st.pN,{title:'the sample means, n = '+M.st.pN,
    xlab:'sample mean x̄, m',ylab:'samples',w:Math.max(0.1,Math.round(M.exact.sd/Math.sqrt(M.st.pN)/3*4)/4),
    own:true,showNormal:M.st.showSe,showSe:M.st.showSe,nx:6});
  const w=worldOf('sampling');
  PDL.SIZES.forEach((n,i)=>{
    if(!L.bottom[i]) return;
    const key=M.st.pLau+'/'+n;
    let G=w.fields[key];
    if(!G){ G=fieldMake(SEEDS.sampling+M.st.pLau*100+n,cfgMystery(M.st.pLau)); G.size=n; sampleBatch(G,n,30); w.fields[key]=G; }
    drawSampleHist(ctx,L.bottom[i],M,G,n,{title:'n = '+n,xlab:null,ylab:null,w:1,
      showNormal:M.st.showSe,showSe:M.st.showSe,nx:3,col:COL.sizes[i]});
    lab(ctx,W,H,L.bottom[i].x+3,L.bottom[i].y1-9,'σ/√n = '+fmt(M.exact.sd/Math.sqrt(n),2)+' m',
        COL.ref,SM_FONT,'left','bottom');
  });
  const cap=sampCaption(M,fmt(map.ratio,2));
  caption(ctx,L.left,L.capY,(L.capTxt===ph.full?cap.full:cap.short)
    +(L.bottom.length?'':' (the four-sample-size row needs a wider stage than this one.)'),
    L.capW,'#767e92',CAP_FONT);
  void 0;
  return {map,L};
}

/* ================================================================== *
 *  view 5: the exact law — the density PhET's mechanism implies       *
 * ================================================================== */
function exactCaption(M){
  const naive=M.naive===null?'':' A launcher with no jitter at all would average v²sin2θ/g = '+fmt(M.naive,2)
    +' m; with it the mean is '+fmt(M.exact.mean,2)+' m. Two factors, pulling opposite ways: the angle spread shortens it (E[sin2θ] = sin2μ·e^(−2σ²), and the exponential is always below one) while the speed spread lengthens it (E[v²] = μ² + σ²). Launchers 3 and 5, whose speed spread beats their angle spread, land LONG of the no-jitter value.';
  return {full:'The histogram is '+M.stat.n+' launches in bins of '+fmt(M.binW,2)+' m (a quarter of σ, rounded — this view is about the shape, so its bins follow the distribution rather than PhET’s list); '
            +(M.st.showDensity
              ?'the orange curve is not a fit to it. It is the density the mechanism implies, ∫f_θ(θ)f_v(v*(r,θ))/|∂x/∂v| dθ, computed on eight panels of the same 96-node rule the exact mean and standard deviation come from — at a fixed r that integrand is a spike, and one panel of it rings by up to 29 %.'
              :'the exact density is switched off, so the bars stand on their own — the mean and standard deviation quoted beside them are still the exact ones, not the sample’s.')+naive
            +(M.naive===null
              ?' The two panels below would compare the exact mean and standard deviation against the two ground-launch shortcuts; from 12 m neither shortcut exists, and they say so rather than drawing an empty axis.'
              :' The two panels below run that comparison across all six mystery launchers: the mean against the no-jitter value, and the exact standard deviation against PhET’s own delta-method estimate.'),
          short:(M.st.showDensity?'The orange curve is the exact density, not a fit. ':'The exact density is switched off. ')+'Mean '+fmt(M.exact.mean,2)+' m, σ '+fmt(M.exact.sd,3)+' m.'};
}
function drawExactView(ctx,W,H,M){
  const ph=exactCaption(M);
  const L=labStage(ctx,W,H,ph.full,ph.short,{nBottom:2});
  const b=L.main;
  const E=M.exact, w=M.binW;
  const lo=Math.max(0,E.mean-5*E.sd), hi=E.mean+5*E.sd;
  const xs=[], ys=[];
  { const C=pdlPdfCurve(M.cfg,lo,hi,200); xs.push.apply(xs,C.xs); ys.push.apply(ys,C.ys); }
  let ymax=0; for(const y of ys) ymax=Math.max(ymax,y);
  const dens=M.hist.counts.map(c=>c/Math.max(1,M.stat.n)/w);
  for(const d of dens) ymax=Math.max(ymax,d);
  ymax*=1.2;
  axesT(ctx,b,lo,hi,0,ymax,{title:'the landing distance: '+M.stat.n+(M.st.showDensity?' launches against the exact density':' launches'),
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
  if(M.st.showDelta&&M.delta!==null){
    const gx=[], gy=[];
    for(let i=0;i<=200;i++){ const x=lo+(hi-lo)*i/200; gx.push(x);
      gy.push(Math.exp(-0.5*Math.pow((x-M.naive)/M.delta,2))/(M.delta*Math.sqrt(2*Math.PI))); }
    pl(ctx,b,gx,gy,lo,hi,0,ymax,COL.bar,1.4,[6,4]);
  }
  /* the exact mean and the sample mean */
  for(const [v,col,tx] of [[E.mean,COL.ref,'μ = '+fmt(E.mean,3)+' m'],
                           [M.stat.mean,COL.live,'x̄ = '+(M.stat.mean===null?'—':fmt(M.stat.mean,3)+' m')]]){
    if(v===null) continue;
    const X=px(v);
    ctx.strokeStyle=col; ctx.lineWidth=1.4; ctx.setLineDash(col===COL.ref?[5,4]:[]);
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,X,b.y+6,tx,col,SM_FONT,'center','top');
  }
  /* a legend row for a curve that is switched off is the caption fault in
     legend form: every row here names something actually drawn */
  legendReg(ctx,b,[[COL.pos,M.stat.n+' launches']]
    .concat(M.st.showDensity?[[COL.ref,'the exact density']]:[])
    .concat(M.st.showDelta&&M.delta!==null?[[COL.bar,'PhET’s delta-method normal']]:[]));
  /* below: the six launchers, mean and spread, exact against the shortcuts */
  const rows=LAUNCHERS.map(l=>{
    const cfg=cfgMystery(l.n,M.st.xOrient);
    const Ex=pdlExact(cfg), mu=cfg.meanSpeed*cfg.mult;
    return {n:l.n,Ex,naive:cfg.h>0?null:mu*mu*Math.sin(2*cfg.meanAng*Math.PI/180)/PDL.G,
            delta:cfg.h>0?null:pdlDeltaSd(mu,cfg.sdSpeed,cfg.meanAng,cfg.sdAng)};
  });
  if(L.bottom.length>=2){
    const noFlat='Both shortcuts are derived for a launch from the ground, where x = v²sin2θ/g. This orientation launches from '
      +fmt(PDL.RAISED_H,0)+' m, so neither applies and there is nothing to compare — pick a ground orientation to see them.';
    barDiff(ctx,L.bottom[0],rows,r=>r.Ex.mean,r=>r.naive,
      titleFor(L.bottom[0],'v²sin2θ/g against the exact mean, %','no-jitter mean, %'),
      '+ means the no-jitter value is too long',noFlat);
    barDiff(ctx,L.bottom[1],rows,r=>r.Ex.sd,r=>r.delta,
      titleFor(L.bottom[1],'PhET’s delta method against the exact σ, %','delta-method σ, %'),
      '+ means the delta method is too wide',noFlat);
  }
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
  return {b,px,py,L};
}
/* the shortcut against the exact value, launcher by launcher, as a SIGNED
   PERCENTAGE: drawn as two absolute bars the two differ by 0.05 % to 1.5 %
   and the panel says nothing at all.  Every bar top is pushed into POLY_SEGS
   so legendAuto dodges the bars, which are fills and are otherwise invisible
   to it. */
function barDiff(ctx,b,rows,fa,fb,title,note,why){
  let hi=0.2, any=false;
  for(const r of rows){ const v=fb(r); if(v!==null){ any=true; hi=Math.max(hi,Math.abs(100*(v/fa(r)-1))); } }
  hi*=1.3;
  /* a sparse panel is not a broken panel, but an empty axis with a legend
     over it IS: say why there is nothing to draw (pulsar Known-bad) */
  if(!any){
    ctx.fillStyle='#aeb6c6'; ctx.font='italic 13px Georgia, serif';
    ctx.textAlign='left'; ctx.textBaseline='top';
    ctx.fillText(plain(title),b.x,b.y);
    caption(ctx,b.x,b.y+22,why,b.w,'#767e92',CAP_FONT);
    return;
  }
  axesT(ctx,b,0.4,rows.length+0.6,-hi,hi,{title,ylab:null,xticks:rows.map(r=>r.n),ny:3});
  const px=x=>b.x+b.w*(x-0.4)/(rows.length+0.2), py=y=>b.y1-b.h*(y+hi)/(2*hi);
  const w=b.w/(rows.length+0.2)*0.42;
  ctx.strokeStyle='#3b4250'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(b.x,py(0)); ctx.lineTo(b.x1,py(0)); ctx.stroke();
  rows.forEach(r=>{
    const v=fb(r); if(v===null) return;
    const d=100*(v/fa(r)-1), X=px(r.n), Y=py(d), Y0=py(0);
    ctx.fillStyle=rgba(d>0?COL.ref:COL.struct,0.85);
    /* a bar 0.3 px tall is a bar nobody can see, and "no bar" reads as "no
       datum": every launcher keeps a visible stub and its number */
    const h1=Math.max(2,Math.abs(Y-Y0));
    ctx.fillRect(X-w/2,d>0?Y0-h1:Y0,w,h1);
    POLY_SEGS.push(X-w/2,Y0-h1,X+w/2,Y0-h1,X-w/2,Y0+h1,X+w/2,Y0+h1);
    lab(ctx,b.x1+2,b.y1+2,X,d>0?Y0-h1-3:Y0+h1+3,(d>0?'+':'')+fmt(d,2),
        d>0?COL.ref:COL.struct,'9.5px -apple-system, sans-serif','center',d>0?'bottom':'top');
  });
  legendReg(ctx,b,[[COL.ref,'the shortcut reads HIGH'],[COL.struct,'it reads LOW']]);
  lab(ctx,b.x1+2,b.y1+2,b.x+4,b.y+6,note,COL.dim,SM_FONT,'left','top');
}

/* ================================================================== *
 *  view 6: the limit theorem                                          *
 * ================================================================== */
function cltCaption(M){
  const E=M.exact;
  return {full:'Four sampling distributions from the same launcher: '+M.st.cM+' samples at each of n = 2, 5, 15 and 40, drawn as densities on one axis so their widths can be compared directly. '
            +(M.st.showNormal
              ?'The orange curves are normals of standard deviation σ/√n with σ = '+fmt(E.sd,3)+' m taken from the exact law, not fitted.'
              :'The σ/√n normals are switched off, so the histograms stand alone — σ = '+fmt(E.sd,3)+' m from the exact law is still what the panels below measure against.')
            +' The left panel below puts the measured standard errors against σ/√n on log axes, where the theorem is a straight line of slope −½. On that axis the error bars are half a pixel long, so the right panel gives the same four residuals in units of their own sampling spread, σ_n√((κ_n+2)/4M): agreement with an error bar attached rather than an impression.'
            +' One launch is skewed by '+fmt(E.skew,3)+'; at n = 40 that skewness is down to '+fmt(E.skew/Math.sqrt(40),4)+', which is the other half of the theorem.',
          short:M.st.cM+' samples at each n'+(M.st.showNormal?'; the orange curves are σ/√n, not fits.':'; the σ/√n normals are off.')};
}
function drawCltView(ctx,W,H,M){
  const ph=cltCaption(M);
  const L=labStage(ctx,W,H,ph.full,ph.short,{nBottom:2,nBottomNarrow:1});
  const b=L.main;
  const E=M.exact;
  const lo=E.mean-4.4*E.sd, hi=E.mean+4.4*E.sd;
  let ymax=0;
  const built=M.sets.map((S,i)=>{
    const w=Math.max(0.08,E.sd/Math.sqrt(S.n)/3);
    const Hh=pdlHistogram(S.means,w);
    const d=Hh.counts.map(c=>c/S.means.length/w);
    for(const v of d) ymax=Math.max(ymax,v);
    const se=E.sd/Math.sqrt(S.n);
    ymax=Math.max(ymax,1/(se*Math.sqrt(2*Math.PI)));
    return {S,w,Hh,d,se};
  });
  ymax*=1.14;
  axesT(ctx,b,lo,hi,0,ymax,{title:'the sample mean at four sample sizes, as densities',
    xlab:'sample mean x̄, m',ylab:'density, 1/m',nx:6,ny:4});
  built.forEach((B,i)=>{
    const col=COL.sizes[i];
    /* the measured distribution as a step outline */
    const xs=[], ys=[];
    for(let k=0;k<B.Hh.counts.length;k++){
      xs.push((B.Hh.lo+k)*B.w,(B.Hh.lo+k+1)*B.w); ys.push(B.d[k],B.d[k]);
    }
    pl(ctx,b,xs,ys,lo,hi,0,ymax,col,1.5);
    if(M.st.showNormal){
      const gx=[], gy=[];
      for(let k=0;k<=220;k++){ const x=lo+(hi-lo)*k/220; gx.push(x);
        gy.push(Math.exp(-0.5*Math.pow((x-E.mean)/B.se,2))/(B.se*Math.sqrt(2*Math.PI))); }
      pl(ctx,b,gx,gy,lo,hi,0,ymax,COL.ref,1.2,[5,4]);
    }
  });
  legendReg(ctx,b,PDL.SIZES.map((n,i)=>[COL.sizes[i],'n = '+n+'  (SE '+fmt(built[i].S.sd,3)+' m)'])
    .concat(M.st.showNormal?[[COL.ref,'σ/√n, the theorem']]:[]));
  /* the log-log panel */
  const p=L.bottom[0];
  if(!p){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); return {b,L}; }
  const nlo=1.4, nhi=60, slo=E.sd/Math.sqrt(nhi)*0.7, shi=E.sd/Math.sqrt(nlo)*1.35;
  axesT(ctx,p,Math.log10(nlo),Math.log10(nhi),Math.log10(slo),Math.log10(shi),
    {title:titleFor(p,'standard error, m, against sample size n (log–log: slope −½)','SE, m, against n (log–log)'),ylab:null,
     xticks:[2,5,15,40].map(Math.log10),xfmt:v=>fmt(Math.pow(10,v),0),
     yticks:logTicks125(slo,shi).map(Math.log10),yfmt:v=>sigf(Math.pow(10,v),2),ny:3});
  const lx=[], ly=[];
  for(let i=0;i<=60;i++){ const n=nlo*Math.pow(nhi/nlo,i/60); lx.push(Math.log10(n)); ly.push(Math.log10(E.sd/Math.sqrt(n))); }
  pl(ctx,p,lx,ly,Math.log10(nlo),Math.log10(nhi),Math.log10(slo),Math.log10(shi),COL.ref,1.8);
  built.forEach((B,i)=>{
    const X=p.x+p.w*(Math.log10(B.S.n)-Math.log10(nlo))/(Math.log10(nhi)-Math.log10(nlo));
    const Y=p.y1-p.h*(Math.log10(B.S.sd)-Math.log10(slo))/(Math.log10(shi)-Math.log10(slo));
    const tol=B.se*Math.sqrt((E.kurt/B.S.n+2)/(4*M.st.cM));
    const Y1=p.y1-p.h*(Math.log10(B.S.sd+tol)-Math.log10(slo))/(Math.log10(shi)-Math.log10(slo));
    const Y2=p.y1-p.h*(Math.log10(Math.max(1e-6,B.S.sd-tol))-Math.log10(slo))/(Math.log10(shi)-Math.log10(slo));
    ctx.strokeStyle=COL.sizes[i]; ctx.lineWidth=1.4;
    ctx.beginPath(); ctx.moveTo(X,Y1); ctx.lineTo(X,Y2); ctx.stroke();
    dot(ctx,X,Y,4,COL.sizes[i],'#0a0c12',1);
  });
  /* the residual panel: the error bars on the log axis are half a pixel long,
     so the agreement is only visible in units of the tolerance itself */
  const q=L.bottom[1];
  if(q){
    let hiz=3;
    const zs=built.map(B=>(B.S.sd-B.se)/(B.se*Math.sqrt((E.kurt/B.S.n+2)/(4*M.st.cM))));
    for(const z of zs) hiz=Math.max(hiz,Math.abs(z)*1.25);
    axesT(ctx,q,0.4,4.6,-hiz,hiz,{title:titleFor(q,'(measured SE − σ/√n) in units of its own sampling sd','the residual, in units of its sd'),
      ylab:null,xticks:[1,2,3,4],xfmt:v=>''+PDL.SIZES[v-1],ny:3});
    const qx=i=>q.x+q.w*(i+1-0.4)/4.2, qy=z=>q.y1-q.h*(z+hiz)/(2*hiz);
    for(const k of [-1,1]){ ctx.strokeStyle='rgba(232,132,58,.35)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(q.x,qy(k)); ctx.lineTo(q.x1,qy(k)); ctx.stroke(); }
    ctx.strokeStyle='#3b4250'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(q.x,qy(0)); ctx.lineTo(q.x1,qy(0)); ctx.stroke();
    zs.forEach((z,i)=>{ const X=qx(i);
      ctx.strokeStyle=COL.sizes[i]; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.moveTo(X,qy(0)); ctx.lineTo(X,qy(clamp(z,-hiz,hiz))); ctx.stroke();
      dot(ctx,X,qy(clamp(z,-hiz,hiz)),4,COL.sizes[i],'#0a0c12',1);
      POLY_SEGS.push(X,qy(0),X,qy(clamp(z,-hiz,hiz)));
    });
    lab(ctx,q.x1+2,q.y1+2,q.x+4,q.y+6,'the orange rules are ±1 sd',COL.dim,SM_FONT,'left','top');
  }
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
  return {b,L};
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
let LAST_GEO=null;
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='field') LAST_GEO=drawFieldView(ctx,W,H,M);
  else if(M.view==='sources') LAST_GEO=drawSourcesView(ctx,W,H,M);
  else if(M.view==='measures') LAST_GEO=drawMeasuresView(ctx,W,H,M);
  else if(M.view==='sampling') LAST_GEO=drawSamplingView(ctx,W,H,M);
  else if(M.view==='exact') LAST_GEO=drawExactView(ctx,W,H,M);
  else LAST_GEO=drawCltView(ctx,W,H,M);
  return LAST_GEO;
}
/* the interval tool is the one thing on the canvas you can drag; it lives on
   the measures view's histogram, and its geometry is recomputed from the same
   layout the drawing used (never cached, so a resize cannot desynchronise it) */
function intervalHit(S,x,y){
  const M=buildModel();
  if(M.view!=='measures'||!M.st.showInterval) return null;
  const ctx=S.measure();
  const ph=measCaption(M,'1.00'), L=labStage(ctx,S.W,S.H,ph.full,ph.short,{histFrac:0.46,fieldWant:fieldWantH(M)});
  const hm={px:v=>L.hist.x+L.hist.w*v/PDL.FIELD};
  const G=intervalGeo(L.hist,M,hm);
  if(y<L.hist.y-14||y>L.hist.y1+6) return null;
  const d1=Math.abs(x-G.a), d2=Math.abs(x-G.c), dm=Math.abs(x-G.mid);
  /* the pixel-to-metre map is (x - box.x) * per, NOT x * per: the histogram
     box starts 54 px in, and dropping that put every dragged edge 5.4 m out */
  const per=PDL.FIELD/L.hist.w, x0=L.hist.x, mx=(x-x0)*per;
  if(d1<=9&&d1<=d2) return {what:'e1',per,x0};
  if(d2<=9) return {what:'e2',per,x0};
  if(dm<=14&&Math.abs(M.st.e2-M.st.e1)>2) return {what:'mid',per,x0,off:mx-(M.st.e1+M.st.e2)/2};
  return null;
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.measure=()=>canvas.getContext('2d');
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(){
    if(!ST.running) return false;
    return worldStep(ST,viewDt(ST));
  };
  S.fire=function(){ fireField(ST); };
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(type==='down'){
      const hit=intervalHit(S,x,y);
      if(!hit) return false;
      DRAG.what=hit.what; DRAG.per=hit.per; DRAG.x0=hit.x0; DRAG.off=hit.off||0;
      DRAG.w0=ST.e2-ST.e1;
      return true;
    }
    if(type==='move'&&DRAG.what){
      const v=clamp((x-DRAG.x0)*DRAG.per,0,PDL.FIELD);
      if(DRAG.what==='e1') ST.e1=Math.round(v*10)/10;
      else if(DRAG.what==='e2') ST.e2=Math.round(v*10)/10;
      else {
        const c=clamp((x-DRAG.x0)*DRAG.per-DRAG.off,Math.abs(DRAG.w0)/2,PDL.FIELD-Math.abs(DRAG.w0)/2);
        ST.e1=Math.round((c-DRAG.w0/2)*10)/10; ST.e2=Math.round((c+DRAG.w0/2)*10)/10;
      }
      return true;
    }
    return false;
  };
  return S;
}
