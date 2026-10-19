
/* ================================================================== *
 *  view 4: the limit theorem                                          *
 * ================================================================== */
function cltCaption(M){
  const E=M.exact;
  return {full:'The theorem, measured. '+M.st.cM+' samples at each of n = 2, 5, 15 and 40, drawn as densities on one axis'
            +(M.st.showNormal
              ?'; the orange curves are normals of standard deviation σ/√n with σ = '+fmt(E.sd,3)+' m from the exact law, nothing fitted.'
              :'. The σ/√n normals are switched off, so the histograms stand alone — σ = '+fmt(E.sd,3)+' m from the exact law is still what the panels below measure against.')
            +' The left panel below puts the measured standard errors against σ/√n on log axes, where the law is a straight line of slope −½. On that axis the error bars are half a pixel long, so the right panel gives the same four residuals in units of their own sampling spread, σ_n√((κ_n+2)/4M). The width half of the theorem is exact at every n and needs no theorem at all; the shape half is the one to watch — a single launch is skewed by '
            +fmt(E.skew,3)+' and the mean of 40 by '+fmt(E.skew/Math.sqrt(40),4)+'.',
          short:M.st.cM+' samples at each n'+(M.st.showNormal?'; the orange curves are σ/√n, not fits.':'; the σ/√n normals are off.')};
}
function drawCltView(ctx,W,H,M){
  const ph=cltCaption(M);
  const L=labStage(ctx,W,H,ph.full,ph.short,{nBottom:2,nBottomNarrow:1});
  const b=L.main, E=M.exact;
  const lo=E.mean-4.4*E.sd, hi=E.mean+4.4*E.sd;
  let ymax=0;
  const built=M.sets.map(S=>{
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
    const xs=[], ys=[];
    for(let k=0;k<B.Hh.counts.length;k++){
      xs.push((B.Hh.lo+k)*B.w,(B.Hh.lo+k+1)*B.w); ys.push(B.d[k],B.d[k]);
    }
    pl(ctx,b,xs,ys,lo,hi,0,ymax,COL.sizes[i],1.5);
    if(M.st.showNormal){
      const gx=[], gy=[];
      for(let k=0;k<=220;k++){ const x=lo+(hi-lo)*k/220; gx.push(x);
        gy.push(Math.exp(-0.5*Math.pow((x-E.mean)/B.se,2))/(B.se*Math.sqrt(2*Math.PI))); }
      pl(ctx,b,gx,gy,lo,hi,0,ymax,COL.ref,1.2,[5,4]);
    }
  });
  legendReg(ctx,b,PDL.SIZES.map((n,i)=>[COL.sizes[i],'n = '+n+'  (SE '+fmt(built[i].S.sd,3)+' m)'])
    .concat(M.st.showNormal?[[COL.ref,'σ/√n, the theorem']]:[]));
  const p=L.bottom[0];
  if(!p){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); return {b,L}; }
  const nlo=1.4, nhi=60, slo=E.sd/Math.sqrt(nhi)*0.7, shi=E.sd/Math.sqrt(nlo)*1.35;
  axesT(ctx,p,Math.log10(nlo),Math.log10(nhi),Math.log10(slo),Math.log10(shi),
    {title:titleFor(p,'standard error, m, against sample size n (log–log: slope −½)','SE, m, against n (log–log)'),
     ylab:null,xticks:[2,5,15,40].map(Math.log10),xfmt:v=>fmt(Math.pow(10,v),0),
     yticks:logTicks125(slo,shi).map(Math.log10),yfmt:v=>sigf(Math.pow(10,v),2),ny:3});
  const lx=[], ly=[];
  for(let i=0;i<=60;i++){ const n=nlo*Math.pow(nhi/nlo,i/60); lx.push(Math.log10(n)); ly.push(Math.log10(E.sd/Math.sqrt(n))); }
  pl(ctx,p,lx,ly,Math.log10(nlo),Math.log10(nhi),Math.log10(slo),Math.log10(shi),COL.ref,1.8);
  built.forEach((B,i)=>{
    const X=p.x+p.w*(Math.log10(B.S.n)-Math.log10(nlo))/(Math.log10(nhi)-Math.log10(nlo));
    const Y=p.y1-p.h*(Math.log10(B.S.sd)-Math.log10(slo))/(Math.log10(shi)-Math.log10(slo));
    dot(ctx,X,Y,4,COL.sizes[i],'#0a0c12',1);
  });
  /* the residual panel: on the log axis the error bars are shorter than the
     dots, so the agreement is only visible in units of the tolerance itself */
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
  else if(M.view==='sizes') LAST_GEO=drawSizesView(ctx,W,H,M);
  else if(M.view==='parent') LAST_GEO=drawParentView(ctx,W,H,M);
  else LAST_GEO=drawCltView(ctx,W,H,M);
  return LAST_GEO;
}
/* the one thing on the canvas you can drag: the launcher's barrel on the two
   field views, which scrubs the launcher through 1..6 (PhET selects them with
   its radio buttons; dragging the barrel is this remake's own shortcut, and
   it is the drag the harness proves moves the picture) */
function launcherHit(S,x,y){
  const M=buildModel();
  if(M.view!=='field'&&M.view!=='parent') return null;
  const ctx=S.measure();
  const ph=M.view==='field'?fieldCaptionS(M,'1.00'):parentCaption(M);
  const L=labStage(ctx,S.W,S.H,ph.full,ph.short,
    {histFrac:M.view==='field'?0.52:0.56,fieldWant:fieldWantH(M)});
  const map=fieldMap(L.field,M);
  const X0=map.X(0), Y0=map.Y(M.cfg.h);
  if(Math.abs(x-X0)>44||y<Y0-44||y>Y0+16) return null;
  return {what:'launcher',X0,Y0};
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.measure=()=>canvas.getContext('2d');
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(){ return ST.running?worldStep(ST,viewDt(ST)):false; };
  S.fire=function(){ fireField(ST); };
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(type==='down'){
      const hit=launcherHit(S,x,y);
      if(!hit) return false;
      DRAG.what='launcher'; DRAG.yDown=y; DRAG.key=ST.view==='field'?'pLau':'xLau';
      DRAG.start=ST[DRAG.key];
      return true;
    }
    if(type==='move'&&DRAG.what==='launcher'){
      /* the barrel sweeps upward through the six launchers: 14 px each */
      /* measured from where the pointer went DOWN, not from the pivot: a
         grab eight pixels above the pivot would otherwise jump the launcher
         on before the pointer had moved at all */
      const n=clamp(Math.round(DRAG.start+(DRAG.yDown-y)/14),1,PDL.N_FIELDS);
      if(n===ST[DRAG.key]) return false;
      ST[DRAG.key]=n;
      if(DRAG.key==='xLau') resetWorld('parent');
      return true;
    }
    return false;
  };
  return S;
}
