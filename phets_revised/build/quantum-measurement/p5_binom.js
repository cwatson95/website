
/* ================================================================== *
 *  THE BINOMIAL view: N identical coins, over and over — shared       *
 * ================================================================== */
const BIN_DRAWS=2e6;            /* cap on M x N so a slider move stays interactive */
const RUN_LEN=10000;            /* the long run in the bottom panel */
const SPREAD_NS=[10,100,1000,10000], SPREAD_M=200;
/* Wilson-Hilferty: the chi-square quantile for display (pinned against scipy) */
function chi2Quantile(nu,z){ const a=2/(9*nu); return nu*Math.pow(1-a+z*Math.sqrt(a),3); }
const Z999=3.090232306167813;   /* the standard normal's 99.9 % point (scipy.stats.norm.ppf(0.999)) */
function binEffM(N,M){ return Math.max(1,Math.min(M,Math.floor(BIN_DRAWS/N))); }
/* the histogram window: +-5 sd around Np, binned to at most ~40 bars */
function binWindow(N,p){
  const sd=binomSD(N,p), mu=N*p;
  let lo=Math.max(0,Math.floor(mu-5*sd)-1), hi=Math.min(N,Math.ceil(mu+5*sd)+1);
  if(sd===0){ lo=Math.max(0,mu-2); hi=Math.min(N,mu+2); }
  const w=Math.max(1,Math.ceil((hi-lo+1)/40));
  return {lo,hi,w,nb:Math.ceil((hi-lo+1)/w)};
}
function binSpread(p,seed){
  return memo('binSpread',p+':'+seed,()=>SPREAD_NS.map((N,i)=>{ const r=repeatsRun(seed+1000+i,N,p,Math.min(SPREAD_M,Math.floor(1e6/N)));
    return {N, sd:Math.sqrt(r.v)/N, law:Math.sqrt(p*(1-p)/N), M:r.M}; }));
}
function binRun(p,seed){
  return memo('binRun',p+':'+seed,()=>{ const R=rngMake(seed+7777), f=new Float64Array(RUN_LEN); let k=0;
    for(let i=0;i<RUN_LEN;i++){ if(rngNext(R)<p) k++; f[i]=k/(i+1); } return f; });
}
function binomModel(st){
  const N=st.binN, p=st.binP, M=binEffM(N,st.binM), seed=st.binSeed;
  const r=memo('binRep',[N,p,M,seed].join(':'),()=>repeatsRun(seed,N,p,M));
  const m={N,p,M,Mask:st.binM,capped:M<st.binM,seed,r,mu:N*p,sd:binomSD(N,p)};
  m.sdMean=m.sd/Math.sqrt(M); m.zMean=m.sdMean>0?(r.mean-m.mu)/m.sdMean:NaN;
  m.q999=r.dof>0?chi2Quantile(r.dof,Z999):NaN;
  const W=binWindow(N,p); m.win=W;
  m.hObs=new Float64Array(W.nb); m.hPmf=new Float64Array(W.nb);
  for(let k=W.lo;k<=W.hi;k++){ const b=Math.floor((k-W.lo)/W.w); m.hObs[b]+=r.obs[k]/M; m.hPmf[b]+=binomPmf(N,k,p); }
  m.outside=0; for(let k=0;k<=N;k++) if(k<W.lo||k>W.hi) m.outside+=r.obs[k];
  m.spread=binSpread(p,seed); m.run=binRun(p,seed);
  return m;
}
function binomGeo(ctx,W,H,Cap){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?48:66;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(140,Math.min(narrow?220:330,avail*0.56));
  const wA=narrow?(rightTop-left)*0.56:Math.min(520,(rightTop-left)*0.55);
  const A=box(left,top+12,wA,upH-40);
  const B=box(A.x1+(narrow?50:76),top+12,Math.max(100,rightTop-(A.x1+(narrow?50:76))),upH-40);
  /* no floor: the long-run panel is skipped when it does not fit */
  const lowTop=top+upH+30, C=box(left,lowTop,Math.min(narrow?W-18-left:760,(narrow?W-18:W-26)-left),fit.capY-16-lowTop-26);
  return {narrow,top,left,fit,A,B,C};
}
/* run: whether the long-run panel is drawn (the caption names it only then) */
function binomCaption(M,run){
  const r=run!==false;
  const m=M.N, W=m.win;
  return {full:'Left: '+m.M+' sets of '+fmtN(m.N)+' coins at p = '+fmt(m.p,2)+', each set counted, against the exact binomial (orange)'+(W.w>1?'; bars are '+W.w+' counts wide':'')+'. Right: the spread of the fraction k/N falls as √(p(1−p)/N) — log–log axes, slope −½.'+(r?' Below: one run of '+fmtN(RUN_LEN)+' flips, its running fraction inside p ± 2σ (log n axis).':''),
          short:m.M+' sets of '+fmtN(m.N)+' against the binomial; the spread √(p(1−p)/N) (log–log)'+(r?'; one long run.':'.')};
}
/* the caption and the geometry together: the long-run panel is optional */
function binomLayout(ctx,W,H,M){ return layoutNamed(r=>binomCaption(M,r),Cap=>binomGeo(ctx,W,H,Cap),G=>G.C.h>=55); }
function drawBinom(ctx,W,H,M){
  const m=M.N, LY=binomLayout(ctx,W,H,M), Cap=LY.Cap, G=LY.G, A=G.A, B=G.B, C=G.C, Wn=m.win;
  /* the histogram against the pmf */
  let ymax=0; for(let i=0;i<Wn.nb;i++) ymax=Math.max(ymax,m.hObs[i],m.hPmf[i]); ymax=ymax>0?ymax*1.18:1;
  const xlo=Wn.lo-0.5, xhi=Wn.lo+Wn.nb*Wn.w-0.5;
  /* k is a count: integer ticks only, never a label on the corner at a half */
  const kt=ticksFor(Wn.lo,Wn.lo+Wn.nb*Wn.w-1,A.w<300?4:6).filter(v=>Math.abs(v-Math.round(v))<1e-9);
  axesT(ctx,A,xlo,xhi,0,ymax,{xticks:kt,xfmt:v=>String(Math.round(v)),yticks:ticksFor(0,ymax,A.h<120?2:4),xlab:'k, the number of '+(M.coinWordUp||'heads')+' in a set of '+fmtN(m.N),
    title:fitTitle(A,m.M+' sets of '+fmtN(m.N)+': counted, against the binomial','sets against the binomial')});
  const bw=A.w/Wn.nb;
  ctx.beginPath(); for(let i=0;i<Wn.nb;i++){ const h=m.hObs[i]; if(h>0){ const X=A.x+i*bw, Y=py(A,h,0,ymax); ctx.rect(X+bw*0.12,Y,bw*0.76,A.y1-Y); } }
  ctx.fillStyle=shade(COL.pos,0.8); ctx.fill();
  const cx=[], cy=[]; for(let i=0;i<Wn.nb;i++){ cx.push(Wn.lo+(i+0.5)*Wn.w-0.5); cy.push(m.hPmf[i]); }
  polyline(ctx,A,cx,cy,xlo,xhi,0,ymax,COL.ref,2);
  for(let i=0;i<Wn.nb;i++) mark(ctx,px(A,cx[i],xlo,xhi),py(A,cy[i],0,ymax),'o',COL.ref,2.4);
  vCursor(ctx,A,m.mu,xlo,xhi,COL.ref);
  legendAuto(ctx,A,[[COL.pos,'the sets, counted'],[COL.ref,'the exact binomial']]);
  if(m.outside>0) lab(ctx,W,H,A.x+4,A.y+10,m.outside+' sets fell outside ±5σ',COL.ref,SM_FONT,'left','middle');
  /* the spread law, log-log */
  const sp=m.spread, deg=m.p<=0||m.p>=1;
  if(deg){ frame(ctx,B,COL.edge); lab(ctx,W,H,B.x+B.w/2,B.y+B.h/2,'p = '+fmt(m.p,2)+': every set is the same, the spread is exactly 0',COL.dim,SM_FONT,'center','middle'); }
  else {
    const lo=Math.log10(Math.sqrt(m.p*(1-m.p)/10000))-0.4, hi=Math.log10(Math.sqrt(m.p*(1-m.p)/10))+0.35;
    axesT(ctx,B,1,4,lo,hi,{xticks:[1,2,3,4],xfmt:v=>'10'+['','¹','²','³','⁴'][v],yticks:ticksFor(Math.ceil(lo),Math.floor(hi),3).filter(v=>Math.abs(v-Math.round(v))<1e-9),yfmt:v=>'10'+(v<0?'⁻':'')+['⁰','¹','²','³','⁴','⁵'][Math.abs(Math.round(v))],
      xlab:'N (log)',title:fitTitle(B,'the spread of k/N: √(p(1−p)/N), slope −½','the spread, log–log')});
    polyline(ctx,B,[1,4],[Math.log10(Math.sqrt(m.p*(1-m.p)/10)),Math.log10(Math.sqrt(m.p*(1-m.p)/10000))],1,4,lo,hi,COL.ref,2);
    for(const s of sp) if(s.sd>0) mark(ctx,px(B,Math.log10(s.N),1,4),clamp(py(B,Math.log10(s.sd),lo,hi),B.y,B.y1),'o',COL.pos,4);
    lab(ctx,W,H,B.x+6,B.y1-12,'log–log',COL.faint,SM_FONT,'left','middle');
  }
  /* one long run */
  if(!G.panelOff&&C.h>=55){
    const n0=Math.log10(1), n1=Math.log10(RUN_LEN);
    axesT(ctx,C,n0,n1,0,1,{xticks:[0,1,2,3,4],xfmt:v=>['1','10','100','1000','10⁴'][v],yticks:C.h<100?[0,0.5,1]:[0,0.25,0.5,0.75,1],xlab:C.h>=95?'flips so far, n (log)':'',
      title:fitTitle(C,'one coin flipped '+fmtN(RUN_LEN)+' times: the running fraction, inside p ± 2√(p(1−p)/n)','one long run')});
    const xs=[], ys=[], fu=[], fd=[], fp=[];
    for(let i=0;i<RUN_LEN;i=i<100?i+1:Math.ceil(i*1.02)){ const n=i+1, sd=Math.sqrt(m.p*(1-m.p)/n); xs.push(Math.log10(n)); ys.push(m.run[i]); fu.push(m.p+2*sd); fd.push(m.p-2*sd); fp.push(m.p); }
    xs.push(n1); ys.push(m.run[RUN_LEN-1]); const sdE=Math.sqrt(m.p*(1-m.p)/RUN_LEN); fu.push(m.p+2*sdE); fd.push(m.p-2*sdE); fp.push(m.p);
    polyline(ctx,C,xs,fu,n0,n1,0,1,COL.ref,1.2,[5,4]); polyline(ctx,C,xs,fd,n0,n1,0,1,COL.ref,1.2,[5,4]); polyline(ctx,C,xs,fp,n0,n1,0,1,COL.ref,1.4);
    polyline(ctx,C,xs,ys,n0,n1,0,1,COL.pos,1.8);
    legendAuto(ctx,C,[[COL.pos,'the running fraction k/n'],[COL.ref,'p, and p ± 2σ (dashed)']]);
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function binomReadout(M){
  const m=M.N, r=m.r;
  return hd('the experiment')+rrow('N coins, bias p',fmtN(m.N)+', '+fmt(m.p,2))+rrow('sets M',m.M+(m.capped?' (capped at '+Math.floor(BIN_DRAWS/m.N)+')':''))+rrow('seed',String(m.seed))
    +hd('the law')+rrow('mean Np',sigf(m.mu,5))+rrow('sd &radic;(Np(1&minus;p))',sigf(m.sd,5))+rrow('sd of k/N',sigf(m.sd/m.N,4))
    +hd('the sets')+rrow('sample mean',sigf(r.mean,6),'good')+rrow('&nbsp;&nbsp;(mean &minus; Np)/(&sigma;/&radic;M)',isFinite(m.zMean)?fmt(m.zMean,2):'exact',Math.abs(m.zMean)>4?'bad':'')
    +rrow('sample variance',sigf(r.v,5))+rrow('&chi;&sup2; / dof',r.dof>0?fmt(r.chi,2)+' / '+r.dof:'&mdash;',r.dof>0&&r.chi>m.q999?'bad':'good')
    +rrow('99.9 % point (Wilson&ndash;Hilferty)',isFinite(m.q999)?fmt(m.q999,1):'&mdash;')
    +hd('one run of '+fmtN(RUN_LEN))+rrow('final fraction',fmt(m.run[RUN_LEN-1],4))+rrow('p &plusmn; 2&sigma;',fmt(m.p,2)+' &plusmn; '+fmt(2*Math.sqrt(m.p*(1-m.p)/RUN_LEN),4));
}
function binomEq(M){ return ['<span class="hl">P(k) = C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup></span> &nbsp;&middot;&nbsp; &lang;k&rang; = Np, &nbsp; &sigma;<sub>k</sub> = &radic;(Np(1&minus;p)), &nbsp; &sigma;<sub>k/N</sub> = &radic;(p(1&minus;p)/N)',
  'the fraction of heads settles on p, and its spread shrinks as one over the square root of the number of coins']; }
function binomTag(M){ const m=M.N; return '<b>the binomial</b> — '+m.M+' sets of N = '+fmtN(m.N)+' at p = '+fmt(m.p,2); }
const INFO_BINOM='Flip N identical coins and count the heads, k. Do it again and k changes; do it many times and the counts pile up into the binomial '
  +'distribution, C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup>, centred on Np with a spread &radic;(Np(1&minus;p)). The spread grows with N, but '
  +'more slowly than N does, so the FRACTION k/N tightens as &radic;(p(1&minus;p)/N): ten coins give a fraction good to about &plusmn;0.16, ten '
  +'thousand to &plusmn;0.005. That is why PhET&rsquo;s ten thousand coins look deterministic and its ten look like noise, and it is the same law '
  +'whether the coins are classical or quantum. The sets here are seeded, so every number is reproducible; the &chi;&sup2; against the exact '
  +'binomial should sit near its degrees of freedom. The bottom panel follows one long run of flips and watches its fraction wander '
  +'into the funnel p &plusmn; 2&radic;(p(1&minus;p)/n).';
const DERIV_BINOM='<h4>counting identical coins</h4>'
  +EQ(1,'P(k) = C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup>, &nbsp; ln n! = n ln n &minus; n + &frac12;ln 2&pi;n + '+FR('1','12n')+' &minus; &hellip;')
  +EQ(2,'&lang;k&rang; = Np, &nbsp; Var k = Np(1&minus;p), &nbsp; &sigma;<sub>k/N</sub> = &radic;(p(1&minus;p)/N)')
  +EQ(3,'&chi;&sup2; = &Sigma; (O<sub>b</sub> &minus; E<sub>b</sub>)&sup2;/E<sub>b</sub>, &nbsp; <span class="rm">bins merged until</span> E<sub>b</sub> &ge; 5')
  +'<p>ln n! is a table of summed logs to 30 and Stirling above it (truncation below 10<sup>&minus;16</sup>); it matches math.lgamma to 1 part in 10<sup>16</sup>, '
  +'and the pmf matches scipy to 10<sup>&minus;10</sup>. The tolerances in selfTest come from the variances: a sample mean within 4&sigma;/&radic;M, a '
  +'&chi;&sup2; below scipy&rsquo;s 99.9 % point.</p>'
  +'<div class="cite">pins: 1000 sets of 100 at p = 0.3, mean 29.951, &chi;&sup2; 34.07 / 23; 200 sets of 10 000 at 0.5, mean 4997.815, &chi;&sup2; 36.41 / 34; '
  +'3000 sets of 10 at 0.65, &chi;&sup2; 4.22 / 8 &mdash; derive.py</div>';
