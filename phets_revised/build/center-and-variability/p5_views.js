
/* ================================================================== *
 *  view C — the spread (PhET's Variability screen)                    *
 * ================================================================== */
const SP_CAP_FULL='PhET&rsquo;s Variability screen. One measure at a time, drawn on the data that made it. The RANGE is a bar between the two most extreme kicks and knows nothing about the rest. The IQR is the box of a box-and-whisker: Q1 and Q3 by PhET&rsquo;s exclusive median-of-halves rule, whiskers out to the furthest kick inside 1.5 &times; IQR, and anything past that marked as an outlier. The MAD is every kick&rsquo;s own distance from the mean, averaged &mdash; the ticks under the line are those distances. The interval tool counts what falls between its two handles, both ends included, as PhET&rsquo;s does.';
const SP_CAP_SHORT='PhET&rsquo;s Variability screen: range, interquartile range and mean absolute deviation, each drawn on the kicks that made it.';
function viewSpread(ctx,W,H,M,st){
  const L=cavLayout(ctx,W,H,SP_CAP_FULL,SP_CAP_SHORT,0.42,30,fieldWantH(M.xs),plotWantH(M.maxK));
  drawField(ctx,L.field,M,st,W,H);
  const geom=drawNumberLine(ctx,L.plot,'kick distance (metres) — '+st.vMeasure.toUpperCase());
  const d=drawDots(ctx,geom,L.plot,M.xs,'dot',{view:'spread',
    mark:(i,v)=>{
      if(st.vMeasure==='iqr'&&M.box&&st.vOutliers&&(v<M.box.lowFence||v>M.box.highFence)) return COL.rng;
      if(st.vMeasure==='range'&&M.stat.n&&(v===M.stat.min||v===M.stat.max)) return COL.rng;
      return null;
    }});
  geom.top0=d.top-6;
  const S=M.stat, map=geom.map;
  if(st.vShow&&S.n){
    if(st.vMeasure==='range'&&S.range!==null){
      const y=geom.ly+NL_BAR;
      ctx.strokeStyle=COL.rng; ctx.lineWidth=2.2;
      ctx.beginPath(); ctx.moveTo(map.X(S.min),y); ctx.lineTo(map.X(S.max),y); ctx.stroke();
      for(const v of [S.min,S.max]){
        ctx.beginPath(); ctx.moveTo(map.X(v),y-6); ctx.lineTo(map.X(v),y+6); ctx.stroke();
      }
      lab(ctx,W,H,(map.X(S.min)+map.X(S.max))/2,geom.ly+NL_LAB2,
          'range = '+fmt(S.max,0)+' − '+fmt(S.min,0)+' = '+fmt(S.range,0)+' m',COL.rng,SM_FONT,'center','middle');
    } else if(st.vMeasure==='iqr'&&M.box){
      const B=M.box, y=geom.ly+NL_BAR+8, hh=11;
      const wl=st.vOutliers?B.whiskLo:B.min, wh=st.vOutliers?B.whiskHi:B.max;
      ctx.strokeStyle=COL.iqr; ctx.lineWidth=1.6;
      ctx.beginPath();
      ctx.moveTo(map.X(wl),y); ctx.lineTo(map.X(B.q1),y);
      ctx.moveTo(map.X(B.q3),y); ctx.lineTo(map.X(wh),y);
      ctx.moveTo(map.X(wl),y-7); ctx.lineTo(map.X(wl),y+7);
      ctx.moveTo(map.X(wh),y-7); ctx.lineTo(map.X(wh),y+7);
      ctx.stroke();
      ctx.fillStyle=rgba(COL.iqr,0.18);
      ctx.fillRect(map.X(B.q1),y-hh,map.X(B.q3)-map.X(B.q1),2*hh);
      ctx.strokeStyle=COL.iqr; ctx.lineWidth=1.6;
      ctx.strokeRect(map.X(B.q1)+0.5,y-hh+0.5,map.X(B.q3)-map.X(B.q1),2*hh);
      ctx.strokeStyle=COL.med; ctx.lineWidth=2.2;
      ctx.beginPath(); ctx.moveTo(map.X(B.median),y-hh); ctx.lineTo(map.X(B.median),y+hh); ctx.stroke();
      if(st.vOutliers) for(const o of B.outliers)
        dot(ctx,map.X(o),y,3.4,'#0b0f1a',COL.rng,1.5);
      lab(ctx,W,H,map.X(B.q1),geom.ly+NL_LAB2,'Q1 '+fmt(B.q1,1),COL.iqr,SM_FONT,'center','middle');
      lab(ctx,W,H,map.X(B.q3),geom.ly+NL_LAB2,'Q3 '+fmt(B.q3,1),COL.iqr,SM_FONT,'center','middle');
      lab(ctx,W,H,(map.X(B.q1)+map.X(B.q3))/2,geom.ly+NL_LAB2+16,
          'IQR = '+fmt(B.q3,1)+' − '+fmt(B.q1,1)+' = '+fmt(B.iqr,1)+' m'
          +(st.vOutliers&&B.outliers.length?'  · '+B.outliers.length+' outlier'+(B.outliers.length>1?'s':''):''),
          COL.iqr,SM_FONT,'center','middle');
    } else if(st.vMeasure==='mad'){
      const y=geom.ly+NL_BAR, mx=map.X(S.mean);
      ctx.strokeStyle=rgba(COL.mad,0.55); ctx.lineWidth=1.2;
      for(const v of M.xs){
        ctx.beginPath(); ctx.moveTo(map.X(v),y-5); ctx.lineTo(map.X(v),y+5); ctx.stroke();
      }
      ctx.strokeStyle=COL.mad; ctx.lineWidth=2.2;
      ctx.beginPath();
      ctx.moveTo(mx-S.madExact*map.s,y+11); ctx.lineTo(mx+S.madExact*map.s,y+11);
      ctx.moveTo(mx-S.madExact*map.s,y+6); ctx.lineTo(mx-S.madExact*map.s,y+16);
      ctx.moveTo(mx+S.madExact*map.s,y+6); ctx.lineTo(mx+S.madExact*map.s,y+16);
      ctx.stroke();
      meanFulcrum(ctx,geom,S.mean,COL.mean,null,W,H);
      lab(ctx,W,H,mx,geom.ly+NL_LAB2+16,'MAD = '+fmt(S.madExact,3)+' m each side of the mean  ·  PhET prints '+fmt(S.madPhet,1),
          COL.mad,SM_FONT,'center','middle');
    }
  }
  /* PhET refuses quartiles below five kicks and shows 'IQR = ?'; say so on
     the canvas too, or the view reads as broken rather than as honest */
  if(st.vShow&&st.vMeasure==='iqr'&&!M.box)
    lab(ctx,W,H,(L.plot.x+L.plot.x1)/2,geom.ly+NL_LAB2,
        S.n?('IQR = ?  —  PhET needs at least five kicks, and this field has '+S.n)
           :'IQR = ?  —  no kicks yet.  Press kick 1 or kick 5.',
        COL.iqr,CAP_FONT,'center','middle');
  if(st.vShow&&st.vMeasure!=='iqr'&&!S.n)
    lab(ctx,W,H,(L.plot.x+L.plot.x1)/2,geom.ly+NL_LAB2,
        st.vMeasure.toUpperCase()+' = ?  —  no kicks yet.  Press kick 1 or kick 5.',
        COL.dim,CAP_FONT,'center','middle');
  if(st.vMean&&S.mean!==null&&st.vMeasure!=='mad')
    meanFulcrum(ctx,geom,S.mean,COL.mean,'mean '+fmt(S.mean,2),W,H);
  /* the interval tool: a block between two handles, both ends counted */
  if(st.vInterval){
    const a=map.X(M.iv.lo), b2=map.X(M.iv.hi);
    ctx.fillStyle=rgba(COL.live,0.13); ctx.fillRect(a,geom.top0,b2-a,geom.ly-geom.top0);
    ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
    ctx.beginPath();
    ctx.moveTo(a,geom.top0); ctx.lineTo(a,geom.ly);
    ctx.moveTo(b2,geom.top0); ctx.lineTo(b2,geom.ly);
    ctx.stroke();
    dot(ctx,a,geom.top0,4.5,COL.live,'#fff',1);
    dot(ctx,b2,geom.top0,4.5,COL.live,'#fff',1);
    lab(ctx,W,H,(a+b2)/2,geom.top0-11,
        M.iv.count+' of '+S.n+' = '+fmt(100*M.iv.frac,1)+'% in ['+fmt(M.iv.lo,1)+', '+fmt(M.iv.hi,1)+']',
        COL.live,SM_FONT,'center','middle');
  }
  /* the pointer hangs from the top of the plot and points DOWN at the line,
     as PhET's does.  Its first draft sat in the band below, where its
     triangle covered a tick label and its text landed inside the IQR box —
     a fill, which the label registry cannot see. */
  if(st.vPointer){
    const X=map.X(st.vPtr);
    ctx.strokeStyle=COL.struct; ctx.lineWidth=1.4;
    ctx.beginPath(); ctx.moveTo(X,geom.top0); ctx.lineTo(X,geom.ly-2); ctx.stroke();
    downTriangle(ctx,X,geom.ly-1,5,COL.struct);
    lab(ctx,W,H,X,geom.top0-11,'pointer '+fmt(st.vPtr,1)+' m',COL.struct,SM_FONT,'center','middle');
  }
  cavCaption(ctx,L);
  return L;
}

/* ================================================================== *
 *  view D — which quartile                                            *
 * ================================================================== */
const CONV_CAP_FULL='Six conventions, one data set. Every statistics package computes quartiles, and they do not all compute the same ones: with an even count PhET&rsquo;s exclusive median-of-halves rule agrees with Tukey&rsquo;s hinges and with Hazen, and with an odd count it switches to Weibull and parts from Tukey. It never agrees with numpy&rsquo;s default (Excel&rsquo;s QUARTILE.INC) except by accident. The marks under the line are Q1 and Q3 under each rule; the panel counts how often the rules disagree as the number of kicks grows, computed on this page from the same generator and pinned to derive.py.';
const CONV_CAP_SHORT='Six quartile conventions on one data set: PhET&rsquo;s rule is Weibull at odd n and Hazen at even n, and never numpy&rsquo;s default.';
/* the disagreement sweep, computed here (400 data sets per n on a fixed seed)
   and asserted against derive.py's 3000-trial version to binomial tolerance */
const SWEEP_TRIALS=400, SWEEP_SEED=606121;
function convSweep(){
  if(WORLD.sweep) return WORLD.sweep;
  const rows=[];
  for(let n=CAV.MIN_KICKS_IQR;n<=30;n++){
    const r=cavRng(SWEEP_SEED+n);
    let dl=0,dt=0,dw=0;
    for(let k=0;k<SWEEP_TRIALS;k++){
      const xs=[];
      for(let i=0;i<n;i++) xs.push(CAV.VMIN+Math.floor(r.next()*(CAV.VMAX-CAV.VMIN+1)));
      const q=cavQuartiles(xs);
      const li=cavConvention(xs,'linear'), tu=cavConvention(xs,'tukey'), we=cavConvention(xs,'weibull');
      if(Math.abs(q.q1-li.q1)>1e-12||Math.abs(q.q3-li.q3)>1e-12) dl++;
      if(Math.abs(q.q1-tu.q1)>1e-12||Math.abs(q.q3-tu.q3)>1e-12) dt++;
      if(Math.abs(q.q1-we.q1)>1e-12||Math.abs(q.q3-we.q3)>1e-12) dw++;
    }
    rows.push({n,linear:dl/SWEEP_TRIALS,tukey:dt/SWEEP_TRIALS,weibull:dw/SWEEP_TRIALS});
  }
  WORLD.sweep=rows;
  return rows;
}
function viewConv(ctx,W,H,M,st){
  const L=cavLayout(ctx,W,H,CONV_CAP_FULL,CONV_CAP_SHORT,0.46);
  const mb=L.room?L.field:L.full;
  const geom=drawNumberLine(ctx,mb,'the data set — '+M.stat.n+' kicks ('+M.parity+')');
  const d=drawDots(ctx,geom,mb,M.xs,'dot',{view:'conv'});
  geom.top0=d.top-6;
  /* Q1 and Q3 under each convention, on their own rows so six marks at nearly
     the same place are all readable */
  const rowY=geom.ly+NL_BAR-2;
  M.conv.forEach((c,i)=>{
    const col=COL.conv[i];
    const a=geom.map.X(c.q1), b2=geom.map.X(c.q3);
    ctx.strokeStyle=col; ctx.lineWidth=1.6;
    const yy=rowY+i*4;
    ctx.beginPath(); ctx.moveTo(a,yy); ctx.lineTo(b2,yy); ctx.stroke();
    dot(ctx,a,yy,2.6,col,null,0); dot(ctx,b2,yy,2.6,col,null,0);
  });
  /* the legend has to name which colour is which rule, and the IQRs differ by
     less than a dot, so the panel below carries the numbers */
  legendAuto(ctx,mb,M.conv.map((c,i)=>[COL.conv[i],plain(c.name)+'  '+fmt(c.q1,2)+'–'+fmt(c.q3,2)]));
  if(!L.room){
    lab(ctx,W,H,mb.x+4,mb.y1-9,'narrow stage: the IQR bars and the disagreement sweep are not drawn',
        '#5d6578',SM_FONT,'left','middle');
    cavCaption(ctx,L);
    return L;
  }
  const half=Math.floor((L.plot.w-58)/2);
  const pb=box(L.plot.x,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  const sb=box(L.plot.x+half+58,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  /* left: the six IQRs as bars */
  const iqrs=M.conv.map(c=>c.iqr);
  const lo=0, hi=Math.max.apply(null,iqrs)*1.25+0.2;
  const SHORTC=['PhET','Tukey','Weibull','Hazen','linear','midpt'];
  axesQ(ctx,pb,lo,hi,0,M.conv.length,{nx:5,xfmt:t=>fmt(t,1),
    yticks:M.conv.map((c,i)=>i+0.5),yfmt:t=>SHORTC[Math.floor(t)]||'',
    xlab:'IQR (metres)',title:titleFor(pb,'the six IQRs of one data set','the six IQRs')});
  M.conv.forEach((c,i)=>{
    const y0=pb.y1-pb.h*(i+0.78)/M.conv.length, y1=pb.y1-pb.h*(i+0.22)/M.conv.length;
    const x1=pb.x+pb.w*(c.iqr-lo)/(hi-lo);
    ctx.fillStyle=rgba(COL.conv[i],c.id==='phet'?0.85:0.5);
    ctx.fillRect(pb.x,y1,Math.max(1,x1-pb.x),y0-y1);
    lab(ctx,W,H,x1+5,(y0+y1)/2,fmt(c.iqr,2),COL.conv[i],SM_FONT,'left','middle');
  });
  /* right: how often the rules disagree, against n */
  const sw=convSweep();
  axesQ(ctx,sb,CAV.MIN_KICKS_IQR,30,0,1,{nx:6,ny:5,
    xlab:'number of kicks n',ylab:'fraction that differ',
    yfmt:t=>fmt(t,1),xfmt:t=>fmt(t,0),
    title:titleFor(sb,'how often PhET’s rule differs','disagreement vs n')});
  const ns=sw.map(r=>r.n);
  polyline(ctx,sb,ns,sw.map(r=>r.linear),CAV.MIN_KICKS_IQR,30,0,1,COL.conv[4],1.8);
  polyline(ctx,sb,ns,sw.map(r=>r.tukey),CAV.MIN_KICKS_IQR,30,0,1,COL.conv[1],1.6);
  polyline(ctx,sb,ns,sw.map(r=>r.weibull),CAV.MIN_KICKS_IQR,30,0,1,COL.conv[2],1.6);
  legendAuto(ctx,sb,[[COL.conv[4],'vs numpy default (linear)'],
                     [COL.conv[1],'vs Tukey (zero at even n)'],
                     [COL.conv[2],'vs Weibull (zero at odd n)']]);
  lab(ctx,W,H,sb.x+4,sb.y1+34,SWEEP_TRIALS+' uniform data sets per n, this page’s own generator',
      '#5d6578',SM_FONT,'left','middle');
  cavCaption(ctx,L);
  return L;
}

/* ================================================================== *
 *  view E — the balance point                                         *
 * ================================================================== */
const BAL_CAP_FULL='Why the mean balances, and what it costs. Each estimator is the minimiser of its own loss: the mean of the squared distance and the median of the absolute distance, and neither is the minimiser of the other&rsquo;s. The left panel draws both losses against a trial centre c, each divided by its own minimum so the two fit one axis (the division is stated because it is a scale distortion). The right panel drags the last ball from 1 m to 15 m and records what each statistic does: the mean is a straight line of slope exactly 1/n, the median is a staircase that stops moving the moment the ball leaves the middle.';
const BAL_CAP_SHORT='The mean minimises the squared distance, the median the absolute distance &mdash; and only one of them follows a ball that runs away.';
function influenceRows(M,st){
  const base=drawsOf(SEEDS.balance,st.bKick,st.bN).slice();
  const out=[];
  for(let v=CAV.VMIN;v<=CAV.VMAX;v++){
    base[base.length-1]=v;
    out.push([v,cavMean(base),cavMedian(base)]);
  }
  return out;
}
function viewBalance(ctx,W,H,M,st){
  const L=cavLayout(ctx,W,H,BAL_CAP_FULL,BAL_CAP_SHORT,0.40);
  const mb=L.room?L.field:L.full;
  const geom=drawNumberLine(ctx,mb,'the data set — the last ball is yours to move');
  const d=drawDots(ctx,geom,mb,M.xs,'dot',{view:'balance',
    mark:(i)=>i===M.moved?COL.live:null});
  geom.top0=d.top-6;
  const S=M.stat, map=geom.map;
  /* the two moments, equal by the identity, at their own printed scale */
  const mom=momentBars(ctx,geom,mb,M.xs,S.mean);
  lab(ctx,W,H,mom.mx,geom.ly+NL_LAB2+16,
      'each side pulls '+fmt(mom.Mm.neg,3)+' m — equal, exactly  ·  bars at 1 m = '
      +fmt(mom.sc,1)+' px, not the number line’s scale',
      COL.ref,SM_FONT,'center','middle');
  meanFulcrum(ctx,geom,S.mean,COL.mean,'mean '+fmt(S.mean,3),W,H);
  medianMark(ctx,geom,S.median,COL.med,'median '+fmt(S.median,1),W,H);
  lab(ctx,W,H,mb.x+4,mb.y+13,
      'sum of (x_i − mean) = '+fmt(M.torque,12)+' m',COL.mean,SM_FONT,'left','middle');
  if(!L.room){
    lab(ctx,W,H,mb.x+4,mb.y1-9,'narrow stage: the loss curves and the influence panel are not drawn',
        '#5d6578',SM_FONT,'left','middle');
    cavCaption(ctx,L);
    return L;
  }
  const half=Math.floor((L.plot.w-58)/2);
  const pb=box(L.plot.x,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  const ib=box(L.plot.x+half+58,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  /* the two losses, each normalised by its own minimum */
  if(st.bLoss){
    const cs=[],sq=[],ab=[];
    const sqMin=cavSqLoss(M.xs,S.mean), abMin=cavAbsLoss(M.xs,S.median);
    for(let k=0;k<=160;k++){
      const c=XLO+(XHI-XLO)*k/160;
      cs.push(c); sq.push(cavSqLoss(M.xs,c)/sqMin); ab.push(cavAbsLoss(M.xs,c)/abMin);
    }
    const hi=Math.min(6,Math.max(2.2,Math.max.apply(null,ab)*1.08));
    axesQ(ctx,pb,XLO,XHI,1,hi,{nx:5,ny:4,xlab:'trial centre c (metres)',
      ylab:'loss / its own minimum',yfmt:t=>fmt(t,1),xfmt:t=>fmt(t,0),
      title:titleFor(pb,'each loss, divided by its own minimum','the two losses')});
    polyline(ctx,pb,cs,sq,XLO,XHI,1,hi,COL.mean,1.8);
    polyline(ctx,pb,cs,ab,XLO,XHI,1,hi,COL.med,1.8);
    marker(ctx,pb,XLO,XHI,1,hi,S.mean,1,COL.mean);
    marker(ctx,pb,XLO,XHI,1,hi,S.median,1,COL.med);
    legendAuto(ctx,pb,[[COL.mean,'sum of (x_i − c)², least at the mean'],
                       [COL.med,'sum of |x_i − c|, least at the median']]);
    lab(ctx,W,H,pb.x+4,pb.y1+34,'each curve is divided by its own minimum (×'
        +fmt(sqMin,1)+' and ×'+fmt(abMin,1)+') so one axis holds both',
        '#5d6578',SM_FONT,'left','middle');
  }
  /* the influence curve */
  const rows=influenceRows(M,st);
  const ylo=Math.min.apply(null,rows.map(r=>Math.min(r[1],r[2])))-0.6;
  const yhi=Math.max.apply(null,rows.map(r=>Math.max(r[1],r[2])))+0.6;
  axesQ(ctx,ib,CAV.VMIN,CAV.VMAX,ylo,yhi,{nx:5,ny:5,
    xlab:'where the last ball is (metres)',ylab:'statistic (metres)',
    yfmt:t=>fmt(t,1),xfmt:t=>fmt(t,0),
    title:titleFor(ib,'what one moved ball does','influence')});
  polyline(ctx,ib,rows.map(r=>r[0]),rows.map(r=>r[1]),CAV.VMIN,CAV.VMAX,ylo,yhi,COL.mean,1.8);
  polyline(ctx,ib,rows.map(r=>r[0]),rows.map(r=>r[2]),CAV.VMIN,CAV.VMAX,ylo,yhi,COL.med,1.8);
  marker(ctx,ib,CAV.VMIN,CAV.VMAX,ylo,yhi,st.bMove,S.mean,COL.live);
  legendAuto(ctx,ib,[[COL.mean,'mean, slope exactly 1/n = '+fmt(1/M.stat.n,4)],
                     [COL.med,'median, flat outside the middle']]);
  cavCaption(ctx,L);
  return L;
}

/* ================================================================== *
 *  view F — the long run                                              *
 * ================================================================== */
const LONG_CAP_FULL='The kicker&rsquo;s weights are published, so there is nothing to estimate here: the population mean, median, standard deviation and MAD are sums over fifteen numbers, and a sample can be judged against them rather than against another sample. The bars are the relative frequencies this page drew; the orange marks are the probabilities PhET&rsquo;s sampler implies, w(i)/&Sigma;w exactly. The running mean converges inside &plusmn;2&sigma;/&radic;n, which is a tolerance computed rather than chosen &mdash; and the sample MAD does not converge from below: whether it is biased up or down depends on whether &mu; lands on a whole metre.';
const LONG_CAP_SHORT='Frequencies against the kicker&rsquo;s own weights, and the running mean inside its &plusmn;2&sigma;/&radic;n band.';
function viewLong(ctx,W,H,M,st){
  const L=cavLayout(ctx,W,H,LONG_CAP_FULL,LONG_CAP_SHORT,0.46);
  const P=M.pop, N=M.stat.n;
  const mb=L.room?L.field:L.full;
  const fb=box(mb.x+10,mb.y+16,mb.w-20,Math.max(60,mb.h-42));
  const pmax=Math.max(Math.max.apply(null,P.p),Math.max.apply(null,M.counts)/N)*1.2;
  axesQ(ctx,fb,XLO,XHI,0,pmax,{nx:8,ny:5,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,2),
    xlab:'kick distance (metres)',ylab:'probability',
    title:titleFor(fb,N+' kicks against the kicker’s own weights','frequencies vs weights')});
  const map=nlMap(fb), bw=map.s*0.66;
  for(let i=0;i<M.counts.length;i++){
    const v=i+CAV.VMIN, f=M.counts[i]/N;
    const X=map.X(v), y0=fb.y1, y1=fb.y1-fb.h*f/pmax;
    ctx.fillStyle=rgba(COL.pos,0.55);
    ctx.fillRect(X-bw/2,y1,bw,y0-y1);
  }
  for(let i=0;i<P.p.length;i++){
    const X=map.X(i+CAV.VMIN), Y=fb.y1-fb.h*P.p[i]/pmax;
    ctx.strokeStyle=COL.ref; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(X-bw/2,Y); ctx.lineTo(X+bw/2,Y); ctx.stroke();
  }
  ctx.strokeStyle=COL.mean; ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
  ctx.beginPath(); ctx.moveTo(map.X(P.mean),fb.y); ctx.lineTo(map.X(P.mean),fb.y1); ctx.stroke();
  ctx.setLineDash([]);
  legendAuto(ctx,fb,[[rgba(COL.pos,0.55),'measured frequency'],
                     [COL.ref,'wᵢ/Σw, exactly'],
                     [COL.mean,'μ = '+fmt(P.mean,3)+' m']]);
  if(!L.room){
    lab(ctx,W,H,fb.x,fb.y1+38,'narrow stage: the running mean and the sample-vs-population panel are not drawn',
        '#5d6578',SM_FONT,'left','middle');
    cavCaption(ctx,L);
    return L;
  }
  const half=Math.floor((L.plot.w-58)/2);
  const tb=box(L.plot.x,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  const cb=box(L.plot.x+half+58,L.plot.y+10,half,Math.max(50,L.plot.h-26));
  /* the running mean inside its band */
  const band=st.lBands;
  const ylo=P.mean-3*P.sd/Math.sqrt(10), yhi=P.mean+3*P.sd/Math.sqrt(10);
  /* from the TENTH kick: below that the running mean is off this scale and
     the curve entered the box from the top, which reads as a broken plot */
  const LX0=1;
  axesQ(ctx,tb,LX0,Math.log10(N),ylo,yhi,{nx:4,ny:5,
    xlab:'kicks so far (log₁₀)',ylab:'running mean (metres)',
    xfmt:t=>fmt(Math.pow(10,t),0),yfmt:t=>fmt(t,1),
    title:titleFor(tb,'the running mean from the tenth kick, inside ±2σ/√n','the running mean')});
  if(band){
    const ks=[],up=[],dn=[];
    for(let k=0;k<=120;k++){
      const lg=Math.log10(10)+ (Math.log10(N)-1)*k/120;
      const n=Math.pow(10,lg);
      ks.push(lg); up.push(P.mean+2*P.sd/Math.sqrt(n)); dn.push(P.mean-2*P.sd/Math.sqrt(n));
    }
    polyline(ctx,tb,ks,up,LX0,Math.log10(N),ylo,yhi,COL.ref,1.3,[4,3]);
    polyline(ctx,tb,ks,dn,LX0,Math.log10(N),ylo,yhi,COL.ref,1.3,[4,3]);
  }
  polyline(ctx,tb,[LX0,Math.log10(N)],[P.mean,P.mean],LX0,Math.log10(N),ylo,yhi,COL.mean,1.3);
  polyline(ctx,tb,M.trace.map(r=>Math.log10(r[0])),M.trace.map(r=>r[1]),
           LX0,Math.log10(N),ylo,yhi,COL.pos,1.8);
  legendAuto(ctx,tb,[[COL.pos,'running mean'],[COL.mean,'μ'],[COL.ref,'±2σ/√n']]);
  /* sample against population, four statistics on one metre axis */
  const items=[['mean',M.stat.mean,P.mean,COL.mean],
               ['median',M.stat.median,P.median,COL.med],
               ['MAD',M.stat.madExact,P.mad,COL.mad],
               ['σ',M.stat.sd,P.sd,COL.rng]];
  const vlo=0, vhi=Math.max.apply(null,items.map(t=>Math.max(t[1],t[2])))*1.25+0.3;
  axesQ(ctx,cb,vlo,vhi,0,items.length,{nx:5,ny:1,yticks:[],xfmt:t=>fmt(t,0),
    xlab:'metres',title:titleFor(cb,'this sample against the population','sample vs population')});
  items.forEach((t,i)=>{
    const y=cb.y1-cb.h*(i+0.5)/items.length;
    const Xs=cb.x+cb.w*(t[1]-vlo)/(vhi-vlo), Xp=cb.x+cb.w*(t[2]-vlo)/(vhi-vlo);
    ctx.strokeStyle=rgba(t[3],0.45); ctx.lineWidth=1.2;
    ctx.beginPath(); ctx.moveTo(Xs,y); ctx.lineTo(Xp,y); ctx.stroke();
    dot(ctx,Xs,y,4,t[3],'#0b0f1a',1);
    ctx.strokeStyle=COL.ref; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(Xp,y-6); ctx.lineTo(Xp,y+6); ctx.stroke();
    lab(ctx,W,H,cb.x+4,y-11,plain(t[0])+'  '+fmt(t[1],3)+' vs '+fmt(t[2],3),t[3],SM_FONT,'left','middle');
  });
  lab(ctx,W,H,cb.x+4,cb.y1+34,'dot = this sample, orange bar = the population value',
      '#5d6578',SM_FONT,'left','middle');
  cavCaption(ctx,L);
  return L;
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  POLY_SEGS=[]; LEGEND_RECTS=[]; LABELS=[];
  ctx.setTransform(1,0,0,1,0,0);
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='kicks') return viewKicks(ctx,W,H,M,st);
  if(M.view==='meanmed') return viewMeanMed(ctx,W,H,M,st);
  if(M.view==='spread') return viewSpread(ctx,W,H,M,st);
  if(M.view==='conv') return viewConv(ctx,W,H,M,st);
  if(M.view==='balance') return viewBalance(ctx,W,H,M,st);
  return viewLong(ctx,W,H,M,st);
}
/* the layout a hit test needs, recomputed the way the view computes it */
function layoutOf(S,M){
  const ctx=S.measure(), W=S.W, H=S.H, st=M.st;
  if(M.view==='kicks') return cavLayout(ctx,W,H,KICKS_CAP_FULL,KICKS_CAP_SHORT,0.50,st.mSort?62:30,fieldWantH(M.xs),plotWantH(M.maxK));
  if(M.view==='meanmed') return cavLayout(ctx,W,H,MM_CAP_FULL,MM_CAP_SHORT,0.44,30,fieldWantH(M.xs),plotWantH(M.maxK));
  if(M.view==='spread') return cavLayout(ctx,W,H,SP_CAP_FULL,SP_CAP_SHORT,0.42,30,fieldWantH(M.xs),plotWantH(M.maxK));
  if(M.view==='conv') return cavLayout(ctx,W,H,CONV_CAP_FULL,CONV_CAP_SHORT,0.46);
  if(M.view==='balance') return cavLayout(ctx,W,H,BAL_CAP_FULL,BAL_CAP_SHORT,0.40);
  return cavLayout(ctx,W,H,LONG_CAP_FULL,LONG_CAP_SHORT,0.46);
}
/* the number line of the view that has one, and its geometry */
function plotGeomOf(S,M){
  const L=layoutOf(S,M);
  const raw=(M.view==='conv'||M.view==='balance')?L.field:L.plot;
  const b=(M.view==='conv'||M.view==='balance')&&!L.room?L.full:raw;
  const D=dotGeomOf(b,M.xs,M.view);
  return {L,b,map:D.map,ly:D.ly,dots:D};
}
const PRED_GRAB=14;
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.measure=()=>canvas.getContext('2d');
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel(),ST); };
  S.step=function(){ return ST.running?worldStep(ST,FRAME_DT):false; };
  S.kick=function(n){ return kickNow(ST,n); };
  /* what the pointer can grab, in the order it is tried */
  S.hit=function(x,y){
    const M=buildModel(), st=ST;
    if(st.view==='kicks'||st.view==='meanmed'||st.view==='spread'){
      const L=layoutOf(S,M);
      const G=fieldGeomOf(L.field,M.xs);
      const i=ballAt(M.xs,G,x,y);
      if(i>=0) return {what:'ball',idx:i,map:G.map};
      const g=plotGeomOf(S,M);
      if(st.view==='spread'&&st.vInterval&&y>=g.dots.top-16&&y<=g.ly+6){
        const d1=Math.abs(x-g.map.X(st.vH1)), d2=Math.abs(x-g.map.X(st.vH2));
        if(Math.min(d1,d2)<PRED_GRAB) return {what:d1<=d2?'h1':'h2',map:g.map};
      }
      /* the pointer is now drawn hanging from the top of the plot box down to
         the line, so its grab region is that whole column and not a band
         under the line (where it used to be drawn) */
      if(st.view==='spread'&&st.vPointer&&Math.abs(x-g.map.X(st.vPtr))<PRED_GRAB&&
         y>=g.b.y&&y<=g.ly+10)
        return {what:'ptr',map:g.map};
      if(st.view==='kicks'&&st.mPredict&&Math.abs(x-g.map.X(st.mPredVal))<PRED_GRAB&&Math.abs(y-g.ly-13)<22)
        return {what:'predMed',map:g.map};
      if(st.view==='meanmed'&&st.aPredMean&&Math.abs(x-g.map.X(st.aPredMeanVal))<PRED_GRAB&&Math.abs(y-g.ly+14)<22)
        return {what:'predMean',map:g.map};
      if(st.view==='meanmed'&&st.aPredMed&&Math.abs(x-g.map.X(st.aPredMedVal))<PRED_GRAB&&Math.abs(y-g.ly-14)<22)
        return {what:'predMed2',map:g.map};
      return null;
    }
    if(st.view==='balance'){
      const g=plotGeomOf(S,M);
      const G={map:g.map,gy:g.ly,rowH:g.dots.rowH,br:g.dots.r,stacks:g.dots.stacks};
      const i=ballAt(M.xs,G,x,y);
      if(i===M.moved) return {what:'move',map:g.map};
      return null;
    }
    return null;
  };
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(type==='down'){
      const h2=S.hit(x,y);
      if(!h2) return false;
      DRAG.what=h2.what; DRAG.idx=h2.idx; DRAG.map=h2.map;
      return true;
    }
    if(type==='move'&&DRAG.what){
      const v=DRAG.map.V(x), st=ST;
      if(DRAG.what==='ball'){
        const F=curField(st); if(!F) return false;
        const nv=cavSnapValue(v);
        if(F.xs[DRAG.idx]===nv) return false;
        F.xs[DRAG.idx]=nv; return true;
      }
      if(DRAG.what==='move'){
        const nv=cavSnapValue(v);
        if(st.bMove===nv) return false;
        st.bMove=nv; return true;
      }
      const cl=clamp(v,CAV.DRAG_LO,CAV.DRAG_HI);
      if(DRAG.what==='h1'){ if(st.vH1===cl) return false; st.vH1=cl; return true; }
      if(DRAG.what==='h2'){ if(st.vH2===cl) return false; st.vH2=cl; return true; }
      if(DRAG.what==='ptr'){ if(st.vPtr===cl) return false; st.vPtr=cl; return true; }
      /* PhET's predict-median thumb snaps to 0.5 m; predict-mean is continuous */
      if(DRAG.what==='predMed'){
        const s2=cavRoundToInterval(clamp(v,CAV.VMIN,CAV.VMAX),CAV.MEDIAN_SNAP);
        if(st.mPredVal===s2) return false; st.mPredVal=s2; return true;
      }
      if(DRAG.what==='predMed2'){
        const s2=cavRoundToInterval(clamp(v,CAV.VMIN,CAV.VMAX),CAV.MEDIAN_SNAP);
        if(st.aPredMedVal===s2) return false; st.aPredMedVal=s2; return true;
      }
      if(DRAG.what==='predMean'){
        const c2=clamp(v,CAV.VMIN,CAV.VMAX);
        if(st.aPredMeanVal===c2) return false; st.aPredMeanVal=c2; return true;
      }
    }
    return false;
  };
  return S;
}
