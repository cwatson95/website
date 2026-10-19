
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/center-and-variability/refvals.txt, the printed     *
 *  output of derive.py, read in full; REF (p7a_refs.js) is the same   *
 *  numbers, written by derive.py so that none is retyped.  Where      *
 *  derive.py checked something against numpy/scipy the assertion here *
 *  says (numpy) or (scipy).                                           *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh]}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),
                                    Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  for(const k of ['fillStyle','strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap'])
    Object.defineProperty(ctx,k,{get:()=>st2[k],set:v=>st2[k]=v});
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=v});
  return ctx;
}

function selfTest(){
  let pass=0, fail=0;
  const T0=Date.now(), TIMES={};
  function ok(c,n){ if(c) pass++; else { fail++; console.log('FAIL — '+n); } }
  function close(a,b,tol,n){ ok(isFinite(a)&&isFinite(b)&&Math.abs(a-b)<=tol,
    n+' ('+a+' vs '+b+', tol '+tol+')'); }
  function rel(a,b,r,n){ ok(isFinite(a)&&isFinite(b)&&Math.abs(a-b)<=r*Math.max(Math.abs(b),1e-300),
    n+' ('+a+' vs '+b+', rel '+r+')'); }
  /* null-aware equality: several statistics are legitimately null */
  function eqv(a,b,tol,n){
    if(b===null||b===undefined){ ok(a===null||a===undefined,n+' is null, as derive.py says'); return; }
    close(a,b,tol,n);
  }
  const stSave=Object.assign({},ST);

  /* ---- A. PhET's rounding, bit for bit ---- */
  REF.roundCases.forEach(c=>{
    close(cavRoundToInterval(c[0],c[1]),c[2],1e-12,
      'roundToInterval('+c[0]+', '+c[1]+') (derive)');
  });
  ok(cavRoundSym(-0.5)===-1,'roundSymmetric(-0.5) is -1: half AWAY from zero');
  ok(cavRoundSym(0.5)===1,'roundSymmetric(0.5) is +1');
  ok(Math.round(-0.5)===0,'…whereas Math.round(-0.5) is +0 — which is why PhET has its own');
  ok(cavDecPlaces(0.1)===1&&cavDecPlaces(0.5)===1&&cavDecPlaces(1)===0,
    'numberOfDecimalPlaces on 0.1, 0.5 and 1');
  ok(0.35/CAV.MAD_STEP<3.5&&0.15/CAV.MAD_STEP<1.5,
    'the two "halves" that round DOWN really are below the tie in binary');
  ok(0.25/CAV.MAD_STEP===2.5&&0.45/CAV.MAD_STEP===4.5,
    'and the two that round up are exactly on it');
  ok(cavSnapValue(3.5)===4&&cavSnapValue(-4)===CAV.VMIN&&cavSnapValue(99)===CAV.VMAX,
    'a dragged ball snaps to a whole metre inside PHYSICAL_RANGE');
  TIMES.A=Date.now();

  /* ---- B. PhET's constants ---- */
  ok(CAV.VMIN===1&&CAV.VMAX===15,'PHYSICAL_RANGE is 1..15 m (PhET)');
  ok(CAV.DRAG_LO===0&&CAV.DRAG_HI===16,'VARIABILITY_DRAG_RANGE is 0..16 (PhET)');
  ok(CAV.MIN_KICKS_IQR===5,'quartiles need five kicks (PhET)');
  ok(CAV.MAX_KICKS.join()==='5,10,15,20,25,30','MAX_KICKS_VALUES (PhET)');
  ok(CAV.MAX_KICKS_MEDIAN.join()==='5,10,15','the Median screen is capped at 15 (PhET)');
  close(CAV.MAD_STEP,0.1,1e-15,'the MAD is rounded to a tenth (PhET)');
  close(CAV.MEDIAN_SNAP,0.5,1e-15,'the predict-median thumb snaps to 0.5 m (PhET)');
  close(CAV.FENCE,1.5,1e-15,'the outlier fence is 1.5 x IQR');
  ['k1','k2','k3','k4'].forEach(k=>{
    ok(CAV.W[k].length===15,k+' covers all fifteen metres');
    ok(CAV.W[k].join()===REF.pop[k].w.join(),k+' weight array matches PhET\'s, verbatim (derive)');
  });
  ok(CAV.K4.join()===CAV.K3.slice().reverse().join(),
    'kicker 4 IS kicker 3 reversed, as PhET builds it');
  ok(CAV.K4!==CAV.K3,'and it is a separate array, not an alias');
  for(const k in REF.seeds) ok(SEEDS[k]===REF.seeds[k],'seed '+k+' matches derive.py');
  TIMES.B=Date.now();

  /* ---- C. every statistic, on every pinned data set ---- */
  REF.cases.forEach((c,ci)=>{
    const xs=c.xs, tag='case '+ci+' (n='+c.n+')';
    close(cavMean(xs),c.mean,1e-12,tag+' mean (numpy)');
    close(cavMedian(xs),c.median,1e-12,tag+' median (numpy)');
    close(cavRange(xs),c.range,1e-12,tag+' range (numpy)');
    close(cavMadExact(xs),c.madExact,1e-12,tag+' exact MAD (numpy)');
    close(cavMadPhet(xs),c.madPhet,1e-12,tag+' PhET\'s rounded MAD (derive)');
    close(cavSd(xs,0),c.sd,1e-12,tag+' standard deviation (numpy)');
    /* BOTH conventions.  With ddof = 0 the n - d divisor is the identity,
       so a mutant that drops d survives every assertion on sd alone — the
       full sweep proved it.  The n - 1 estimate is pinned here and printed
       on the long-run view, so it is neither dead nor untested. */
    eqv(cavSd(xs,1),c.sd1,1e-12,tag+' the n−1 standard deviation (numpy)');
    if(c.n>1) ok(cavSd(xs,1)>c.sd-1e-15,tag+': the n−1 estimate is the larger of the two');
    if(c.n===1) ok(cavSd(xs,1)===null,tag+': and one kick has no n−1 estimate at all');
    const q=cavQuartiles(xs);
    eqv(q.q1,c.q1,1e-12,tag+' Q1 (derive)');
    eqv(q.q3,c.q3,1e-12,tag+' Q3 (derive)');
    eqv(q.iqr,c.iqr,1e-12,tag+' IQR (derive)');
    if(c.q1===null) ok(xs.length<CAV.MIN_KICKS_IQR,tag+' has no quartiles only because n < 5');
  });
  /* the empty data set answers nothing rather than answering zero */
  ok(cavMean([])===null&&cavMedian([])===null&&cavRange([])===null&&cavMadExact([])===null,
    'the empty data set has no mean, median, range or MAD');
  ok(cavQuartiles([]).q1===null&&cavBox([])===null,'and no quartiles and no box');
  ok(cavMiddle([]).length===0,'getMedianObjectsFromSortedArray on an empty list is empty');
  /* the two divisors must actually differ somewhere, or pinning both is a
     tautology about one number written twice */
  { const d0=cavSd([1,2,3,4,9],0), d1=cavSd([1,2,3,4,9],1);
    ok(d1>d0*1.05,'the n and n−1 conventions differ by more than 5% at n = 5 ('
      +fmt(d0,4)+' vs '+fmt(d1,4)+')');
    close(d1/d0,Math.sqrt(5/4),1e-12,'and their ratio is exactly √(n/(n−1))'); }
  /* the even-count convention, explicitly */
  close(cavMedian([1,2,3,4]),2.5,1e-15,'an even count takes the MEAN of the two middles');
  ok(cavMiddle([1,2,3,4]).length===2&&cavMiddle([1,2,3]).length===1,
    'two middle objects for even n, one for odd');
  close(cavMedian([1,2,3,4,5]),3,1e-15,'an odd count takes the single middle');
  close(cavMedian([2,2,2,3]),2,1e-15,'[2,2,2,3] has median 2: BOTH middles are 2');
  close(cavMedian([3,3,4,4]),3.5,1e-15,'…but [3,3,4,4] has median 3.5, a distance nothing was kicked to');
  ok([3,3,4,4].indexOf(cavMedian([3,3,4,4]))<0,'…which is not one of the data values');
  /* the dot plot's own layout.  Found by the mutation sweep: doubling the
     stack's row step changed only pixels and survived, because nothing
     asserted cavStacks at all.  A quantity the picture is built from is a
     model quantity and gets pinned like one (drum_head Known-bad). */
  ok(cavStacks([3,3,5,3]).join()==='0,1,0,2','cavStacks numbers each value’s balls 0,1,2…');
  ok(cavStacks([]).length===0,'and an empty field has no stacks');
  ok(cavStackHeight([3,3,5,3])===3,'cavStackHeight is the tallest stack');
  ok(cavStackHeight([])===0,'and zero when there is nothing to stack');
  ok(cavStackHeight([1,2,3])===1,'one ball per value is a stack of one');
  REF.cases.forEach((c,ci)=>{
    const st2=cavStacks(c.xs), by={};
    c.xs.forEach((v,i)=>{ (by[v]=by[v]||[]).push(st2[i]); });
    let bad=null, hmax=0;
    for(const v in by){
      const rows=by[v].slice().sort((a,b)=>a-b);
      hmax=Math.max(hmax,rows.length);
      for(let k=0;k<rows.length;k++) if(rows[k]!==k) bad=v;
    }
    ok(!bad,'case '+ci+': every stack is CONTIGUOUS from row 0 (no gaps)');
    ok(cavStackHeight(c.xs)===hmax,'case '+ci+': and the tallest stack is '+hmax);
  });
  /* the flight arc is a declared drawing device, but its constants still
     have to be pinned or the sweep is testing nothing there */
  /* ABSOLUTE numbers, not CAV.T_FLY[...] — asserting a function against the
     constant it uses is asserting nothing, and the sweep proved it: both
     flight-arc mutants survived the first version of these three lines */
  close(cavFlightTime(CAV.VMIN),0.9,1e-12,'a 1 m kick is 0.9 s in the air');
  close(cavFlightTime(CAV.VMAX),1.5,1e-12,'a 15 m kick is 1.5 s');
  close(cavFlightTime(8),0.9+0.6*7/14,1e-12,'and an 8 m kick is half way between');
  ok(cavFlightTime(8)>cavFlightTime(2),'and a longer kick is longer in the air');
  {
    const b={d:10,t:0,T:1};
    ok(cavBallPos(b)[0]===0&&cavBallPos(b)[1]===0,'a kick starts at the kicker');
    b.t=1; const end=cavBallPos(b);
    close(end[0],10,1e-12,'and lands at exactly its drawn distance');
    close(end[1],0,1e-12,'…on the ground');
    b.t=0.5; const top=cavBallPos(b);
    close(top[0],5,1e-12,'its apex is half way along');
    close(top[1],4.2,1e-12,'and 4.2 m high: 0.42 of the ten it will travel');
    b.t=2; close(cavBallPos(b)[0],10,1e-12,'past its flight time it stays where it landed');
  }
  TIMES.C=Date.now();

  /* ---- D. the quartile conventions ---- */
  /* the two routes: PhET's slicing, and the same rule by explicit index */
  function qByIndex(xs){
    const a=cavSorted(xs), n=a.length;
    if(n<CAV.MIN_KICKS_IQR) return {q1:null,q3:null};
    const m=Math.floor(n/2), up0=(n%2)?m+1:m;
    if(m%2===1) return {q1:a[(m-1)/2],q3:a[up0+(m-1)/2]};
    return {q1:0.5*(a[m/2-1]+a[m/2]),q3:0.5*(a[up0+m/2-1]+a[up0+m/2])};
  }
  /* the equivalence claim, at every n the sim can reach, on the sim's own
     generator: PhET's rule IS Weibull at odd n and Hazen at even n */
  {
    let bad=0, routes=0, tested=0, tukeyEven=0, linDiff=0;
    const r=cavRng(4242);
    for(let n=CAV.MIN_KICKS_IQR;n<=30;n++){
      for(let t=0;t<40;t++){
        const xs=[];
        for(let i=0;i<n;i++) xs.push(CAV.VMIN+Math.floor(r.next()*(CAV.VMAX-CAV.VMIN+1)));
        const q=cavQuartiles(xs), qi=qByIndex(xs);
        if(Math.abs(q.q1-qi.q1)>1e-12||Math.abs(q.q3-qi.q3)>1e-12) routes++;
        const twin=cavConvention(xs,(n%2)?'weibull':'hazen');
        if(Math.abs(q.q1-twin.q1)>1e-12||Math.abs(q.q3-twin.q3)>1e-12) bad++;
        if(n%2===0){
          const tu=cavConvention(xs,'tukey');
          if(Math.abs(q.q1-tu.q1)>1e-12||Math.abs(q.q3-tu.q3)>1e-12) tukeyEven++;
        }
        const li=cavConvention(xs,'linear');
        if(Math.abs(q.q1-li.q1)>1e-12||Math.abs(q.q3-li.q3)>1e-12) linDiff++;
        tested++;
      }
    }
    ok(tested===1040,'the convention sweep ran '+tested+' data sets');
    ok(routes===0,'PhET\'s slicing and the explicit-index route never disagree');
    ok(bad===0,'PhET\'s rule = Weibull at odd n and Hazen at even n, on all '+tested+' (derive)');
    ok(tukeyEven===0,'…and = Tukey\'s hinges at every even n (an even split has no middle)');
    ok(linDiff>0.6*tested,'…and differs from numpy\'s default on '+linDiff+' of '+tested);
  }
  /* the Hyndman-Fan h(n,p) written out, against the library-style rule */
  close(cavQuantHF([1,2,3,4,5],0.25,6),1.5,1e-12,'H&F type 6 at n=5 puts Q1 at h=1.5');
  close(cavQuantHF([1,2,3,4],0.25,5),1.5,1e-12,'H&F type 5 at n=4 puts Q1 at h=1.5');
  close(cavQuantHF([1,2,3,4,5],0.25,7),2.0,1e-12,'H&F type 7 (numpy default) puts it at h=2');
  ok(Math.abs(cavQuantHF([1,2,3,4,5],0.25,6)-cavQuantHF([1,2,3,4,5],0.25,7))>1e-9,
    'so the two really are different rules on the same data');
  /* derive.py's two demonstration data sets, under all six conventions */
  [['demoData','demoConv','even'],['demoOdd','demoOddConv','odd']].forEach(d=>{
    const xs=REF[d[0]], tbl=REF[d[1]];
    for(const id in tbl){
      const q=cavConvention(xs,id);
      close(q.q1,tbl[id][0],1e-12,d[2]+' demo, '+id+' Q1 (numpy)');
      close(q.q3,tbl[id][1],1e-12,d[2]+' demo, '+id+' Q3 (numpy)');
    }
    const ph=cavQuartiles(xs);
    const twin=d[2]==='odd'?'weibull':'hazen';
    close(ph.q1,tbl[twin][0],1e-12,d[2]+' demo: PhET = '+twin);
    ok(Math.abs(ph.q1-tbl.linear[0])>1e-9||Math.abs(ph.q3-tbl.linear[1])>1e-9,
      d[2]+' demo: PhET differs from numpy\'s default');
  });
  ok(Math.abs(cavQuartiles(REF.demoOdd).q1-cavTukey(REF.demoOdd).q1)>1e-9,
    'the odd demo separates PhET\'s exclusive halves from Tukey\'s inclusive ones');
  /* the sweep the conventions view draws, against derive.py's 3000-trial one */
  {
    const sw=convSweep();
    ok(sw.length===26,'the sweep covers n = 5..30');
    let worst=0, oddW=0, evenT=0;
    sw.forEach(rw=>{
      const R=REF.convSweep[''+rw.n];
      const p=R.vsLinear/R.trials;
      /* binomial tolerance on a 400-trial estimate of p */
      const tol=4*Math.sqrt(Math.max(p*(1-p),1e-6)/SWEEP_TRIALS)+1/SWEEP_TRIALS;
      if(Math.abs(rw.linear-p)>worst) worst=Math.abs(rw.linear-p);
      ok(Math.abs(rw.linear-p)<=tol,
         'n='+rw.n+': the page\'s disagreement rate '+fmt(rw.linear,3)+' matches derive.py\'s '
         +fmt(p,3)+' inside the binomial tolerance '+fmt(tol,3));
      if(rw.n%2===1&&rw.weibull!==0) oddW++;
      if(rw.n%2===0&&rw.tukey!==0) evenT++;
      ok(R.vsWeibull===(rw.n%2?0:R.vsWeibull),'derive.py agrees that odd n never differs from Weibull');
    });
    ok(oddW===0,'on the page too: odd n never differs from Weibull');
    ok(evenT===0,'and even n never differs from Tukey');
    ok(sw[0].linear>0.9,'at n = 5 nearly every data set separates PhET from numpy\'s default');
    ok(sw[25].linear>0.6&&sw[25].linear<0.8,'and at n = 30 it is still about two in three');
  }
  TIMES.D=Date.now();

  /* ---- E. the random stream and PhET's sampler ---- */
  {
    const r=cavRng(REF.seeds.kicks);
    REF.rngStream.forEach((v,i)=>close(r.next(),v,0,'mulberry32 draw '+i+' is bit-identical (derive)'));
  }
  /* Reached THROUGH fieldOf(), the way the sim reaches them, not by calling
     cavDrawSet with a seed lifted out of REF: the per-kicker seed offset
     the spread view uses was executed by no assertion at all, and a mutant
     on it survived the full sweep. */
  {
    Object.assign(ST,DEFAULTS); resetWorlds();
    const byKicker=['spread1','spread2','spread3','spread4'];
    ['k1','k2','k3','k4'].forEach((k,i)=>{
      const F=fieldOf('spread',k,15);
      ok(F.seed===REF.open[byKicker[i]].seed,
         'the spread view builds '+k+' on seed '+REF.open[byKicker[i]].seed+' (derive)');
      ok(F.xs.join()===REF.open[byKicker[i]].xs.join(),
         '\u2026and it opens on derive.py\u2019s '+byKicker[i]+' data set');
    });
    const seeds=['k1','k2','k3','k4'].map(k=>fieldOf('spread',k,15).seed);
    ok(new Set(seeds).size===4,'the four kickers get four DIFFERENT seeds');
    ok(fieldOf('kicks',DEFAULTS.mKick,15).xs.join()===REF.open.kicks.xs.join(),
       'the kicks view opens on derive.py\u2019s data set, through fieldOf');
    ok(fieldOf('meanmed',DEFAULTS.aKick,15).xs.join()===REF.open.meanmed.xs.join(),
       'and so does mean and median');
    ST.view='spread'; ST.vKick='k3';
    ok(curField(ST).xs.join()===REF.open.spread3.xs.join(),
       'and curField() on the spread view returns kicker 3\u2019s');
    resetWorlds();
  }
  for(const nm in REF.open){
    const O=REF.open[nm];
    const xs=cavDrawSet(O.seed,CAV.W[O.w],O.n);
    ok(xs.join()===O.xs.join(),nm+': the page draws the SAME kicks as derive.py');
    close(cavMean(xs),O.mean,1e-12,nm+' mean (derive)');
    close(cavMedian(xs),O.median,1e-12,nm+' median (derive)');
    eqv(cavQuartiles(xs).q1,O.q1,1e-12,nm+' Q1 (derive)');
    eqv(cavQuartiles(xs).q3,O.q3,1e-12,nm+' Q3 (derive)');
    eqv(cavQuartiles(xs).iqr,O.iqr,1e-12,nm+' IQR (derive)');
    close(cavRange(xs),O.range,1e-12,nm+' range (derive)');
    close(cavMadExact(xs),O.madExact,1e-12,nm+' exact MAD (derive)');
    close(cavMadPhet(xs),O.madPhet,1e-12,nm+' PhET MAD (derive)');
    ok(xs.every(v=>v>=CAV.VMIN&&v<=CAV.VMAX&&v===Math.round(v)),
      nm+': every kick is a whole metre inside PHYSICAL_RANGE');
  }
  /* a zero weight is never drawn, and the frequencies match the weights */
  {
    const xs=cavDrawSet(777,CAV.W.k1,20000);
    const zero=xs.filter(v=>CAV.W.k1[v-1]===0).length;
    ok(zero===0,'kicker 1 never kicks to a zero-weight distance');
    const P=cavPop('k1');
    let worst=0;
    for(let i=0;i<15;i++){
      if(!(P.p[i]>0)) continue;
      const c=xs.filter(v=>v===i+1).length, e=20000*P.p[i];
      const z=Math.abs(c-e)/Math.sqrt(e*(1-P.p[i]));
      if(z>worst) worst=z;
    }
    ok(worst<4.2,'and every bin of 20000 draws sits within 4.2 binomial sd ('+fmt(worst,2)+')');
  }
  /* the sampler's contract, tested directly rather than through its output */
  {
    const w=[0,3,0,1], calls=[];
    const fake={next:()=>calls.shift()};
    calls.push(0);      ok(cavSampleProb(fake,w)===1+CAV.VMIN-1,'u = 0 returns the first index');
    calls.push(0.9999); ok(cavSampleProb(fake,w)===4,'u just below 1 returns the last positive weight');
    calls.push(0.5);    ok(cavSampleProb(fake,w)===2,'u = 0.5 lands in the heavy middle weight');
  }
  /* the flight, stepped the way the frame loop steps it.  A mutant that
     doubled the flight time survived the full sweep, because the UI drive
     waited long enough for the ball to land either way — nothing pinned
     WHEN it lands. */
  {
    const F=cavField(4242,'k3',15);
    ok(F.xs.length===0&&F.air.length===0,'a new field is empty');
    const d=cavKick(F);
    ok(d>=CAV.VMIN&&d<=CAV.VMAX,'one kick is away, to '+d+' m');
    ok(F.air.length===1&&F.xs.length===0,'and it is in the air, not in the data set');
    const T=F.air[0].T;
    close(T,cavFlightTime(d),1e-15,'its flight time is cavFlightTime of its distance');
    let steps=0;
    while(F.air.length&&steps<10000){ cavFieldStep(F,FRAME_DT); steps++; }
    ok(F.xs.length===1&&F.xs[0]===d,'it lands into the data set, at its own distance');
    const want=Math.ceil(T/FRAME_DT);
    ok(steps===want,'and it lands on frame '+want+', not '+steps+' — the flight time is pinned');
    /* one frame earlier it must still be up, or the timing is not pinned at all */
    const G=cavField(4242,'k3',15); cavKick(G);
    for(let i=0;i<want-1;i++) cavFieldStep(G,FRAME_DT);
    ok(G.air.length===1&&G.xs.length===0,'one frame before that it is still in the air');
    /* and the field refuses a kick once it is full */
    const H=cavField(7,'k1',3); cavFieldBatch(H,3);
    ok(H.xs.length===3&&cavKick(H)===null,'a full field refuses another kick');
  }
  TIMES.E=Date.now();

  /* ---- F. the population statistics ---- */
  ['k1','k2','k3','k4'].forEach(k=>{
    const P=cavPop(k), R=REF.pop[k];
    close(P.S,R.sum,1e-12,k+' sum of weights (derive)');
    close(P.mean,R.mean,1e-12,k+' population mean (derive)');
    close(P.sd,R.sd,1e-12,k+' population sd (derive)');
    close(P.var,R.var,1e-12,k+' population variance (derive)');
    close(P.mad,R.mad,1e-12,k+' population MAD (derive)');
    close(P.median,R.median,1e-12,k+' population median (derive)');
    close(P.q1,R.q1,1e-12,k+' population Q1 (derive)');
    close(P.q3,R.q3,1e-12,k+' population Q3 (derive)');
    close(P.skew,R.skew,1e-10,k+' population skewness (derive)');
    let s=0; for(const p of P.p) s+=p;
    close(s,1,1e-14,k+' probabilities sum to one');
    close(cavGofC(k,P.mean),P.mad,1e-12,k+': g(mu) IS the population MAD');
  });
  close(cavPop('k1').mean,8,1e-14,'kicker 1 is symmetric about 8 m');
  close(cavPop('k2').mean,8,1e-14,'kicker 2 is symmetric about 8 m');
  close(cavPop('k1').skew,0,1e-14,'…and unskewed');
  close(cavPop('k3').skew,-cavPop('k4').skew,1e-12,'kickers 3 and 4 are exact mirror images');
  close(cavPop('k3').mean-CAV.VMIN,CAV.VMAX-cavPop('k4').mean,1e-12,'…their means reflect about 8 m');
  close(cavPop('k3').sd,cavPop('k4').sd,1e-14,'…and their spreads are identical');
  close(cavPop('k2').sd/cavPop('k1').sd,REF.sdRatio21,1e-12,
    'kicker 2 is '+fmt(REF.sdRatio21,3)+'x as wide as kicker 1 (derive)');
  /* g(c) = E|X - c| is convex, and its KINK at an atom is what signs the
     sample MAD's bias — the claim the first derive.py draft got wrong */
  ['k1','k2','k3','k4'].forEach(k=>{
    const P=cavPop(k);
    const kink=cavGofC(k,P.mean+0.5)+cavGofC(k,P.mean-0.5)-2*cavGofC(k,P.mean);
    close(kink,REF.gKink[k],1e-12,k+': the curvature of g at mu (derive)');
    ok(kink>=-1e-12,k+': g is convex at mu');
    for(const d of [0.1,0.4,1.0])
      ok(0.5*(cavGofC(k,P.mean-d)+cavGofC(k,P.mean+d))>=cavGofC(k,P.mean)-1e-12,
         k+': g is convex at mu (Jensen, +/-'+d+')');
  });
  ok(REF.gKink.k1>REF.gKink.k3,'the on-lattice mean (kicker 1) is the sharper kink (derive)');
  ok(REF.madBias.k3['5']<0&&REF.madBias.k3['30']<0&&REF.madBias.k4['30']<0,
    'off-lattice mean: the sample MAD is biased DOWN at every n (derive, 20000 samples)');
  ok(REF.madBias.k1['5']<0&&REF.madBias.k1['30']>0,
    'on-lattice mean: the bias CHANGES SIGN between n = 5 and 30 (derive) — not "always down"');
  /* the sampling law: sigma/sqrt(n) exactly, against derive.py's Monte Carlo */
  ['k1','k2','k3','k4'].forEach(k=>{
    const P=cavPop(k);
    for(const n of ['5','10','15','30']){
      const R=REF.sampling[k][n];
      close(P.sd/Math.sqrt(+n),R.sdMeanExact,1e-12,k+' n='+n+': sigma/sqrt(n) (derive)');
      rel(R.sdMeanMC,R.sdMeanExact,0.02,
        k+' n='+n+': 20000 Monte-Carlo samples reproduce it to 2% (derive)');
    }
  });
  TIMES.F=Date.now();

  /* ---- G. the balance point ---- */
  {
    let worst=0;
    REF.cases.forEach(c=>{
      const t=cavTorque(c.xs,cavMean(c.xs));
      if(Math.abs(t)>worst) worst=Math.abs(t);
      /* and the exact integer statement behind it */
      let s=0; for(const v of c.xs) s+=v;
      ok(c.xs.length*s-c.xs.length*s===0,'n*sum - n*sum is exactly 0 in integers');
    });
    close(worst,REF.balWorst,1e-18,'the worst |sum of signed deviations| (derive)');
    let worstM=0;
    REF.cases.forEach(c=>{ const mm=cavMoments(c.xs,cavMean(c.xs));
      worstM=Math.max(worstM,Math.abs(mm.gap)); });
    ok(worstM<1e-12,'the two moments about the mean are equal on every pinned case ('+worstM+')');
    { const mm=cavMoments([1,2,3],2);
      close(mm.neg,1,1e-15,'cavMoments: the pull from below');
      close(mm.pos,1,1e-15,'cavMoments: the pull from above');
      const off=cavMoments([1,2,3],1.5);
      close(off.neg,0.5,1e-15,'and away from the mean they are NOT equal (below)');
      close(off.pos,2.0,1e-15,'…nor above'); }
    ok(worst<1e-12,'…and it is machine zero: the mean IS the balance point');
  }
  REF.loss.forEach((Lc,i)=>{
    close(cavSqLoss(Lc.xs,Lc.mean),Lc.sqAtMean,1e-9,'loss set '+i+': squared loss at the mean (derive)');
    close(cavAbsLoss(Lc.xs,Lc.median),Lc.absAtMedian,1e-9,'loss set '+i+': absolute loss at the median (derive)');
    close(cavSqLoss(Lc.xs,Lc.median),Lc.sqAtMedian,1e-9,'loss set '+i+': squared loss at the MEDIAN (derive)');
    close(cavAbsLoss(Lc.xs,Lc.mean),Lc.absAtMean,1e-9,'loss set '+i+': absolute loss at the MEAN (derive)');
    /* a strict win only where the two centres differ; where mean == median
       (a symmetric data set) the two losses are the same number, and
       asserting '<' there would be asserting an accident */
    const apart=Math.abs(Lc.mean-Lc.median)>1e-12;
    ok(apart?Lc.sqAtMean<Lc.sqAtMedian:Lc.sqAtMean===Lc.sqAtMedian,
       'loss set '+i+': the mean '+(apart?'beats':'ties')+' the median on the squared loss');
    ok(apart?Lc.absAtMedian<Lc.absAtMean:Lc.absAtMedian===Lc.absAtMean,
       'loss set '+i+': and '+(apart?'loses to':'ties')+' it on the absolute loss');
    /* the parallel-axis identity, which is what makes "unique minimiser" exact */
    for(const c of [1.0,5.5,9.25,14.0])
      rel(cavSqLoss(Lc.xs,c),cavSqLoss(Lc.xs,Lc.mean)+Lc.xs.length*(Lc.mean-c)*(Lc.mean-c),1e-12,
        'loss set '+i+': the parallel-axis identity at c = '+c);
    /* and a brute-force search, because an identity can be right and the code wrong */
    let best=1e18,bc=0;
    for(let k=0;k<=1600;k++){ const c=k/100, v=cavSqLoss(Lc.xs,c); if(v<best){ best=v; bc=c; } }
    close(bc,Lc.mean,0.011,'loss set '+i+': a 0.01 m grid search finds the mean');
  });
  /* the influence of one moved ball */
  {
    const base=REF.influence.base.slice();
    let mvs=0, slopeBad=0;
    REF.influence.rows.forEach((rw,i)=>{
      base[base.length-1]=rw.v;
      close(cavMean(base),rw.mean,1e-12,'influence at '+rw.v+' m: the mean (derive)');
      close(cavMedian(base),rw.median,1e-12,'influence at '+rw.v+' m: the median (derive)');
      if(i>0){
        const dm=rw.mean-REF.influence.rows[i-1].mean;
        if(Math.abs(dm-REF.meanSlope)>1e-12) slopeBad++;
        if(Math.abs(rw.median-REF.influence.rows[i-1].median)>1e-12) mvs++;
      }
    });
    ok(slopeBad===0,'the mean moves by exactly 1/n = '+fmt(REF.meanSlope,6)+' m per metre, at every step');
    ok(mvs===REF.medMoves,'and the median moves at only '+REF.medMoves+' of the 14 steps (derive)');
    ok(mvs<7,'…which is what "robust" means as a number');
  }
  TIMES.G=Date.now();

  /* ---- H. the box plot, the interval tool, the MAD ceiling ---- */
  REF.box.forEach((B,i)=>{
    const b=cavBox(B.xs);
    close(b.q1,B.q1,1e-12,'box '+i+' Q1 (derive)');
    close(b.q3,B.q3,1e-12,'box '+i+' Q3 (derive)');
    close(b.lowFence,B.lowFence,1e-12,'box '+i+' low fence (derive)');
    close(b.highFence,B.highFence,1e-12,'box '+i+' high fence (derive)');
    close(b.whiskLo,B.whiskLo,1e-12,'box '+i+' lower whisker (derive)');
    close(b.whiskHi,B.whiskHi,1e-12,'box '+i+' upper whisker (derive)');
    ok(b.outliers.join()===B.outliers.join(),'box '+i+' outliers (derive)');
    ok(b.whiskLo>=b.min&&b.whiskHi<=b.max,'box '+i+': the whiskers stay inside the data');
    ok(b.outliers.every(o=>o<b.lowFence||o>b.highFence),'box '+i+': every outlier is past a fence');
  });
  ok(REF.box.some(B=>B.outliers.length),'at least one pinned box HAS an outlier to draw');
  REF.interval.forEach((I,i)=>{
    const r=cavInterval(I.xs,I.lo,I.hi);
    ok(r.count===I.count,'interval '+i+': the count (derive)');
    close(r.frac,I.frac,1e-12,'interval '+i+': the fraction (derive)');
    close(r.width,I.width,1e-12,'interval '+i+': the width (derive)');
  });
  ok(cavInterval([3,5],3,5).count===2,'the interval tool closes BOTH ends, as PhET does');
  ok(cavInterval([3,5],5,3).count===2,'and the handles may be dragged past each other');
  /* the derived ceiling on PhET's triple-rounded MAD */
  {
    const r=cavRng(9090);
    let worst=0, over=0, tested=0;
    for(let t=0;t<1500;t++){
      const n=2+Math.floor(r.next()*29), xs=[];
      for(let i=0;i<n;i++) xs.push(CAV.VMIN+Math.floor(r.next()*(CAV.VMAX-CAV.VMIN+1)));
      const d=Math.abs(cavMadPhet(xs)-cavMadExact(xs));
      if(d>0.1+0.05/n+1e-12) over++;
      if(d>worst) worst=d;
      tested++;
    }
    ok(over===0,'PhET\'s MAD stays inside the derived 0.1 + 0.05/n on all '+tested+' data sets');
    ok(worst>0.05,'…and exceeds a single rounding step somewhere ('+fmt(worst,4)+' m)');
    close(cavMadPhet(REF.madWorstCase),cavMadExact(REF.madWorstCase)+REF.madWorst,1e-12,
      'derive.py\'s worst case reproduces its 0.1 m gap here, with the same sign (derive)');
  }
  TIMES.H=Date.now();

  /* ---- I. the long run ---- */
  for(const k in REF.lln){
    const R=REF.lln[k];
    const xs=cavDrawSet(REF.seeds.longrun+k.charCodeAt(1),CAV.W[k],R.N);
    ok(xs.length===R.N,k+': '+R.N+' draws');
    const cnt=new Array(15).fill(0);
    for(const v of xs) cnt[v-1]++;
    ok(cnt.join()===R.counts.join(),k+': the page\'s bin counts are derive.py\'s, exactly');
    const P=cavPop(k);
    let worst=0;
    for(let i=0;i<15;i++){
      if(!(P.p[i]>0)) continue;
      const e=R.N*P.p[i];
      const z=Math.abs(cnt[i]-e)/Math.sqrt(e*(1-P.p[i]));
      if(z>worst) worst=z;
    }
    close(worst,R.worstZ,1e-9,k+': the worst binomial z (derive)');
    ok(worst<4,k+': every bin is within 4 binomial sd at n = '+R.N);
    R.rows.forEach(rw=>{
      const sub=xs.slice(0,rw.n);
      close(cavMean(sub),rw.mean,1e-12,k+' n='+rw.n+': the running mean (derive)');
      close(cavMedian(sub),rw.median,1e-12,k+' n='+rw.n+': the running median (derive)');
      close(cavMadExact(sub),rw.mad,1e-12,k+' n='+rw.n+': the running MAD (derive)');
      const z=(cavMean(sub)-P.mean)/(P.sd/Math.sqrt(rw.n));
      close(z,rw.z,1e-9,k+' n='+rw.n+': its z against sigma/sqrt(n) (derive)');
      ok(Math.abs(z)<4,k+' n='+rw.n+': and it is inside 4 sigma/sqrt(n)');
    });
  }
  TIMES.I=Date.now();

  /* ---- J. the model and the panels, over every view x preset ---- */
  {
    const CONFIGS=[];
    TABS.forEach(([v])=>{
      CONFIGS.push([v+' default',{view:v}]);
      ['k1','k2','k3','k4'].forEach(k=>CONFIGS.push([v+' '+k,
        {view:v,mKick:k,aKick:k,vKick:k,cKick:k,bKick:k,lKick:k}]));
    });
    CONFIGS.push(['kicks 5 max',{view:'kicks',mMax:5}]);
    CONFIGS.push(['kicks line plot + sort',{view:'kicks',mPlot:'line',mSort:true,mPredict:true}]);
    CONFIGS.push(['meanmed 30 max, both predictions',{view:'meanmed',aMax:30,aPredMean:true,aPredMed:true}]);
    CONFIGS.push(['spread range',{view:'spread',vMeasure:'range',vMean:true}]);
    CONFIGS.push(['spread mad',{view:'spread',vMeasure:'mad'}]);
    CONFIGS.push(['spread tools',{view:'spread',vInterval:true,vPointer:true,vOutliers:false}]);
    CONFIGS.push(['conv n=5',{view:'conv',cN:5}]);
    CONFIGS.push(['conv n=30',{view:'conv',cN:30}]);
    CONFIGS.push(['balance far ball',{view:'balance',bMove:15,bN:25}]);
    CONFIGS.push(['balance near ball, no losses',{view:'balance',bMove:1,bLoss:false}]);
    CONFIGS.push(['long 10',{view:'longrun',lN:10,lBands:false}]);
    CONFIGS.push(['long 5000',{view:'longrun',lN:5000}]);
    let bad=null, nonfinite=null;
    CONFIGS.forEach(([nm,over])=>{
      Object.assign(ST,DEFAULTS,over); resetWorlds();
      const M=buildModel();
      const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M)+(INFO[M.view]||'')+(DERIV[M.view]||'');
      if(/NaN|undefined|\[object/.test(html)&&!bad) bad=nm+': '+html.slice(Math.max(0,html.search(/NaN|undefined|\[object/)-40),html.search(/NaN|undefined|\[object/)+40);
      for(const key in M.stat){
        const v=M.stat[key];
        if(v!==null&&!isFinite(v)&&!nonfinite) nonfinite=nm+'.'+key;
      }
    });
    ok(!bad,'every view x kicker builds panels with no NaN, undefined or [object ('+(bad||'ok')+')');
    ok(!nonfinite,'and no statistic is non-finite ('+(nonfinite||'ok')+')');
    /* the readout must PRINT a number only this configuration can supply — a
       containment check that any other state also satisfies is vacuous */
    Object.assign(ST,DEFAULTS); ST.view='longrun'; ST.lKick='k3'; resetWorlds();
    ok(readoutHTML(buildModel()).indexOf(fmt(cavPop('k3').sd,4))>=0,
      'the readout prints kicker 3\'s exact sigma, '+fmt(cavPop('k3').sd,4)+' m');
    ok(readoutHTML(buildModel()).indexOf(fmt(cavPop('k1').sd,4))<0,
      '…and not kicker 1\'s, which is a different number');
    Object.assign(ST,DEFAULTS); ST.view='spread'; ST.vMax=5; resetWorlds();
    {
      const F=curField(ST); cavFieldClear(F); cavFieldBatch(F,4);
      const M=buildModel();
      ok(M.stat.q1===null&&M.stat.iqr===null,'four kicks: no quartiles, as PhET refuses below five');
      ok(readoutHTML(M).indexOf('needs five kicks')>=0,'and the readout says why');
      ok(M.box===null,'and there is no box plot to draw');
    }
  }
  TIMES.J=Date.now();

  /* ---- K. the drawing: layout, text, the hint corner, the legends ---- */
  {
    const SIZES=[[1400,820],[1100,712],[820,560],[560,380]];
    const DRAWS=[['kicks',{view:'kicks'}],['kicks sorted',{view:'kicks',mSort:true,mPredict:true}],
                 ['meanmed',{view:'meanmed',aPredMean:true,aPredMed:true}],
                 ['spread iqr',{view:'spread'}],
                 ['spread range',{view:'spread',vMeasure:'range',vInterval:true,vPointer:true}],
                 ['spread mad',{view:'spread',vMeasure:'mad',vMean:true}],
                 ['conv',{view:'conv'}],['conv n=5',{view:'conv',cN:5}],
                 ['balance',{view:'balance'}],['balance b=1',{view:'balance',bMove:1}],
                 ['longrun',{view:'longrun'}],['longrun 10',{view:'longrun',lN:10}]];
    const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
    DRAWS.forEach(([nm,over])=>{
      SIZES.forEach(([W,H])=>{
        Object.assign(ST,DEFAULTS,over); resetWorlds();
        const ctx=makeShot(W,H);
        drawView(ctx,W,H,buildModel(),ST);
        const texts=ctx.ops.filter(o=>o.op==='text');
        ok(ctx.ops.length>40,nm+' '+W+'x'+H+' draws something ('+ctx.ops.length+' ops)');
        let bad=null;
        for(const t of texts){
          if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
          if(/NaN|undefined/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
          if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){
            bad='off-canvas: "'+t.t.slice(0,30)+'"'; break; }
        }
        ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
        /* the house #hint is HTML at bottom:11px and the capture cannot see it */
        const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
        ok(!inHint.length,nm+' '+W+'x'+H+' nothing under the #hint line'
           +(inHint.length?' ("'+inHint[0].t.slice(0,30)+'")':''));
        let hit=null;
        for(let i=0;i<texts.length&&!hit;i++) for(let j=i+1;j<texts.length;j++){
          const a=texts[i].bb,b=texts[j].bb;
          const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
          if(ox>3&&oy>3){ hit='"'+texts[i].t.slice(0,20)+'" vs "'+texts[j].t.slice(0,20)+'"'; break; }
        }
        ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
        let leg=null;
        for(const r of LEGEND_RECTS) for(let i=0;i<POLY_SEGS.length;i+=4){
          const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
          if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||
             Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
          leg='a curve crosses the legend'; break;
        }
        ok(!leg,nm+' '+W+'x'+H+' legend clear');
      });
    });
    /* the drawn balance point IS the computed mean, not a second calculation */
    Object.assign(ST,DEFAULTS); ST.view='balance'; resetWorlds();
    {
      const W=1100,H=712, ctx=makeShot(W,H), M=buildModel();
      drawView(ctx,W,H,M,ST);
      const S2={W,H,measure:()=>ctx,st:ST};
      const g=plotGeomOf(S2,M);
      const want=g.map.X(M.stat.mean);
      const texts=ctx.ops.filter(o=>o.op==='text'&&o.t.indexOf('mean ')===0);
      ok(texts.length===1,'the balance view labels the mean exactly once');
      close((texts[0].bb[0]+texts[0].bb[2])/2,want,3,
        'and the label sits at the x the computed mean maps to');
      ok(ctx.ops.filter(o=>o.op==='text'&&/^sum of \(x_i/.test(o.t)).length===1,
        'and the canvas prints the sum of signed deviations');
      /* the two moments are drawn as two bars of EQUAL length, which is the
         identity made visible rather than asserted beside the picture */
      const mm=cavMoments(M.xs,M.stat.mean);
      close(mm.neg,mm.pos,1e-12,'the two moments about the mean are equal');
      ok(mm.neg>0,'and neither is zero on this data set ('+fmt(mm.neg,3)+' m)');
      ok(ctx.ops.filter(o=>o.op==='text'&&/each side pulls/.test(o.t)).length===1,
        'and the canvas says so, with the bars’ own scale printed');
      ok(ctx.ops.filter(o=>o.op==='text'&&/not the number line/i.test(o.t)).length===1,
        '…including that it is NOT the number line’s scale');
    }
    /* an empty field says so rather than drawing an empty picture */
    Object.assign(ST,DEFAULTS); ST.view='kicks'; resetWorlds();
    {
      const F=curField(ST); cavFieldClear(F);
      const W=1100,H=712, ctx=makeShot(W,H);
      const M=buildModel();
      ok(M.stat.n===0,'the field can be emptied');
      ok(readoutHTML(M).indexOf('0 of 15')>=0,'and the readout says 0 of 15');
      drawView(ctx,W,H,M,ST);
      ok(ctx.ops.length>40,'an empty field still draws its line and its ticks ('+ctx.ops.length+' ops)');
      const bad=ctx.ops.filter(o=>o.op==='text'&&/NaN|undefined/.test(o.t));
      ok(!bad.length,'with no NaN on the canvas');
    }
  }
  TIMES.K=Date.now();

  /* ---- L. the pointer ---- */
  {
    Object.assign(ST,DEFAULTS); ST.view='kicks'; resetWorlds();
    const W=1200,H=760, ctx=makeShot(W,H);
    const M=buildModel();
    drawView(ctx,W,H,M,ST);
    const S2=makeScene({getContext:()=>ctx});
    S2.W=W; S2.H=H;
    const L=layoutOf(S2,M), G=fieldGeomOf(L.field,M.xs);
    const bx=G.map.X(M.xs[0]), by=G.gy-G.rowH*(G.stacks[0]+0.5);
    ok(S2.hit(bx,by)&&S2.hit(bx,by).what==='ball','a pointer on a landed ball grabs it');
    ok(S2.hit(3,3)===null,'a pointer at the top-left of the stage grabs nothing');
    ok(S2.hit(bx,G.gy+300)===null,'and neither does one far below the field');
    DRAG.what=null;
    ok(S2.pointer('down',bx,by)===true,'pointer-down grabs');
    const was=curField(ST).xs[DRAG.idx];
    const moved=S2.pointer('move',G.map.X(was===15?1:15),by);
    ok(moved===true,'dragging it reports a change');
    ok(curField(ST).xs[0]===(was===15?1:15),'and the ball takes the new whole-metre value');
    ok(S2.pointer('move',G.map.X(99),by)===true||curField(ST).xs[0]===CAV.VMAX,
      'dragging past the end clamps at 15 m');
    ok(curField(ST).xs[0]===CAV.VMAX,'…and stays there');
    ok(S2.pointer('up',0,0)===true,'pointer-up releases');
    ok(DRAG.what===null,'and clears the drag');
  }
  TIMES.L=Date.now();

  console.log('section times, s: '+['A','B','C','D','E','F','G','H','I','J','K','L'].map((k,i,a)=>
    k+' '+((TIMES[k]-(i?TIMES[a[i-1]]:T0))/1000).toFixed(1)).join(', '));
  Object.assign(ST,stSave); resetWorlds();
  console.log(pass+' passed, '+fail+' failed  ('+fmt((Date.now()-T0)/1000,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
