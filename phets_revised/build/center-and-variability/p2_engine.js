
/* ================================================================== *
 *  the engine: PhET's statistics, exactly, and the kickers behind     *
 *  them.  Every convention here is read out of PhET's published       *
 *  build (docs/phets/center-and-variability_en.html, v1.2.6) and is   *
 *  named in the comment above the function that implements it.        *
 *  Cross-checked line by line against derive.py, whose printed output  *
 *  is refvals.txt and whose numbers arrive as REF (p7a_refs.js).      *
 * ================================================================== */

/* --- PhET's constants (its values, read from the build) ------------------ */
const CAV={
  /* PHYSICAL_RANGE = new Range(1, 15): every kick lands on an integer metre,
     and a dragged ball takes roundSymmetric(physicalRange.constrainValue(x)) */
  VMIN:1, VMAX:15,
  /* VARIABILITY_DRAG_RANGE = new Range(0, 16): the travel of the interval
     tool's handles and of the pointer, which are continuous */
  DRAG_LO:0, DRAG_HI:16,
  /* MAX_KICKS_VALUES; the Median screen is capped at 15 */
  MAX_KICKS:[5,10,15,20,25,30],
  MAX_KICKS_MEDIAN:[5,10,15],
  /* "Need at least five kicks" — quartiles are null below five */
  MIN_KICKS_IQR:5,
  /* VARIABILITY_MEASURE_DECIMAL_POINTS = 1, and the MAD is rounded to 0.1 */
  MAD_STEP:0.1,
  /* the predict-median thumb has roundToInterval: 0.5; predict-mean has null */
  MEDIAN_SNAP:0.5,
  /* the box plot's outlier fence, the standard 1.5 x IQR (PhET's Outliers
     checkbox: "Shows outliers on the boxplot as markings rather than being
     included in the whisker") */
  FENCE:1.5,
  /* kick weights, verbatim from the build.  k4 is BUILT from k3 by the
     reversal PhET performs (rightSkewedData.slice().reverse()), so the
     mirror relation is code rather than a coincidence of two typed arrays. */
  K1:[0,0,0,1,3,12,20,32,20,12,3,1,0,0,0],
  K2:[3,5,10,10,25,32,45,65,45,32,25,10,10,5,3],
  K3:[10,25,45,30,18,12,10,5,4,4,4,4,4,4,4],
  /* a kick's flight: PhET picks the DISTANCE first and animates a ball to it,
     so the arc is a drawing device and not a launch model.  0.9 s at 1 m
     stretching to 1.5 s at 15 m, and the apex is a fixed fraction of the
     distance — stated on the canvas, never used in a statistic. */
  T_FLY:[0.9,1.5], APEX:0.42, STACK_T:0.25
};
CAV.K4=CAV.K3.slice().reverse();
CAV.W={k1:CAV.K1,k2:CAV.K2,k3:CAV.K3,k4:CAV.K4};
/* PhET's four jerseys on the Variability screen: Green 1, Blue 2, Red 3,
   Yellow 4 (its accessible names) */
const KICKERS=[{id:'k1',n:1,jersey:'green',name:'kicker 1'},
               {id:'k2',n:2,jersey:'blue',name:'kicker 2'},
               {id:'k3',n:3,jersey:'red',name:'kicker 3'},
               {id:'k4',n:4,jersey:'yellow',name:'kicker 4'}];

/* --- PhET's rounding, bit for bit ---------------------------------------
   dot.Utils.roundSymmetric(x) = (x<0?-1:1)*Math.round(Math.abs(x)), i.e. half
   AWAY FROM ZERO, which is not what Math.round alone does for a negative
   number.  roundToInterval(v,i) = toFixedNumber(roundSymmetric(v/i)*i,
   numberOfDecimalPlaces(i)).  The "half" cases are decided by the binary
   value, not the decimal one: 0.35/0.1 is 3.4999999999999996 and rounds DOWN
   while 0.25/0.1 is exactly 2.5 and rounds up.  derive.py pins all of them. */
function cavRoundSym(x){ return (x<0?-1:1)*Math.round(Math.abs(x)); }
function cavDecPlaces(v){
  if(Math.floor(v)===v) return 0;
  const s=''+v;
  if(s.indexOf('e')>=0){
    const p=s.split('e'), m=p[0], e=+p[1];
    const c=m.indexOf('.')>=0?m.split('.')[1].length:0;
    return Math.max(c-e,0);
  }
  return s.split('.')[1].length;
}
function cavRoundToInterval(v,iv){
  return parseFloat((cavRoundSym(v/iv)*iv).toFixed(cavDecPlaces(iv)));
}

/* --- the statistics ------------------------------------------------------ */
function cavSorted(xs){ return xs.slice().sort((a,b)=>a-b); }
/* PhET getMedianObjectsFromSortedArray: the middle element for odd length,
   the two middle elements for even length, nothing for an empty list. */
function cavMiddle(a){
  const n=a.length;
  if(n%2===1) return [a[(n-1)/2]];
  if(n%2===0&&n>=2) return [a[(n-2)/2],a[n/2]];
  return [];
}
function cavMeanOf(a){ if(!a.length) return null; let s=0; for(const v of a) s+=v; return s/a.length; }
function cavMean(xs){ return cavMeanOf(xs); }
/* PhET CAVSoccerSceneModel.updateDataMeasures: the mean of the middle
   object(s) — so an even count gives the average of the two middle values. */
function cavMedian(xs){ return cavMeanOf(cavMiddle(cavSorted(xs))); }
function cavRange(xs){
  if(!xs.length) return null;
  let lo=xs[0],hi=xs[0];
  for(const v of xs){ if(v<lo) lo=v; if(v>hi) hi=v; }
  return hi-lo;
}
function cavMin(xs){ return xs.length?Math.min.apply(null,xs):null; }
function cavMax(xs){ return xs.length?Math.max.apply(null,xs):null; }
/* PhET VariabilitySceneModel.updateDataMeasures — the EXCLUSIVE
   median-of-halves rule (Moore & McCabe): the lower half is the first
   floor(n/2) values, the upper half the last floor(n/2), and for odd n the
   overall median belongs to neither.  Undefined below five kicks.
   derive.py proves (and 4000 random data sets confirm) that this is exactly
   Hyndman & Fan type 6 (Weibull) at odd n and type 5 (Hazen) at even n, and
   at even n it also coincides with Tukey's hinges. */
function cavQuartiles(xs){
  const a=cavSorted(xs), n=a.length;
  if(n<CAV.MIN_KICKS_IQR) return {q1:null,q3:null,iqr:null,lower:[],upper:[]};
  const t=Math.floor(n/2);
  const lower=a.slice(0,t), upper=a.slice(n%2!==0?t+1:t);
  const q1=cavMeanOf(cavMiddle(lower)), q3=cavMeanOf(cavMiddle(upper));
  return {q1,q3,iqr:q3-q1,lower,upper};
}
/* the exact mean absolute deviation about the mean */
function cavMadExact(xs){
  if(!xs.length) return null;
  const m=cavMean(xs);
  let s=0; for(const v of xs) s+=Math.abs(v-m);
  return s/xs.length;
}
/* PhET's DISPLAYED MAD: every deviation rounded to a tenth of a metre, the
   sum rounded to a tenth, the quotient rounded to a tenth.  Three roundings,
   so it can sit as much as 0.1 + 0.05/n from the exact value (derived and
   measured in derive.py: 0.1 m at worst over 8000 data sets). */
function cavMadPhet(xs){
  if(!xs.length) return null;
  const m=cavMean(xs);
  let s=0;
  for(const v of xs) s+=cavRoundToInterval(Math.abs(v-m),CAV.MAD_STEP);
  s=cavRoundToInterval(s,CAV.MAD_STEP);
  return cavRoundToInterval(s/xs.length,CAV.MAD_STEP);
}
function cavSd(xs,ddof){
  const d=ddof===undefined?0:ddof, n=xs.length;
  if(n<=d) return null;
  const m=cavMean(xs);
  let s=0; for(const v of xs){ const e=v-m; s+=e*e; }
  return Math.sqrt(s/(n-d));
}
/* the box plot.  The whiskers reach the furthest data point inside the
   1.5 x IQR fences; with the Outliers box off, PhET draws the whiskers to the
   extremes instead and marks nothing. */
function cavBox(xs){
  const q=cavQuartiles(xs);
  if(q.q1===null) return null;
  const lo=q.q1-CAV.FENCE*q.iqr, hi=q.q3+CAV.FENCE*q.iqr;
  const inl=xs.filter(v=>v>=lo&&v<=hi);
  const outs=cavSorted(xs.filter(v=>v<lo||v>hi));
  return {q1:q.q1,q3:q.q3,iqr:q.iqr,lowFence:lo,highFence:hi,
          whiskLo:cavMin(inl),whiskHi:cavMax(inl),outliers:outs,
          min:cavMin(xs),max:cavMax(xs),median:cavMedian(xs)};
}
/* the interval tool: PhET counts x >= lo && x <= hi, both ends closed, and
   the handles may be dragged past each other */
function cavInterval(xs,lo,hi){
  const a=Math.min(lo,hi), b=Math.max(lo,hi);
  let k=0; for(const v of xs) if(v>=a&&v<=b) k++;
  return {count:k,frac:xs.length?k/xs.length:0,lo:a,hi:b,width:b-a};
}

/* --- the other quartile conventions, for the conventions view ------------
   Hyndman & Fan types 4..9 written from their own h(n,p), not taken from a
   library, so that the equivalence claim is checked against an independent
   statement of the rule rather than against the thing it is claiming about. */
function cavQuantHF(xs,p,type){
  const a=cavSorted(xs), n=a.length;
  if(!n) return null;
  let h;
  if(type===4) h=n*p;
  else if(type===5) h=n*p+0.5;
  else if(type===6) h=(n+1)*p;
  else if(type===7) h=(n-1)*p+1;
  else if(type===8) h=(n+1/3)*p+1/3;
  else h=(n+0.25)*p+0.375;
  h=clamp(h,1,n);
  const lo=Math.floor(h), fr=h-lo, hi=Math.min(lo+1,n);
  return a[lo-1]+fr*(a[hi-1]-a[lo-1]);
}
/* Tukey's hinges: the INCLUSIVE median-of-halves rule — the overall median
   stays in both halves when n is odd. */
function cavTukey(xs){
  const a=cavSorted(xs), n=a.length;
  if(n<2) return {q1:null,q3:null};
  const t=Math.ceil(n/2);
  const med=b=>{ const k=b.length; return k%2?b[(k-1)/2]:0.5*(b[k/2-1]+b[k/2]); };
  return {q1:med(a.slice(0,t)),q3:med(a.slice(n-t))};
}
/* the conventions the view lays side by side.  'phet' is the sim's own rule;
   the rest are named by the library name a reader would meet them under. */
const CONVENTIONS=[
  {id:'phet',  name:'PhET (exclusive halves)', note:'the rule this sim uses'},
  {id:'tukey', name:'Tukey&rsquo;s hinges',    note:'inclusive halves'},
  {id:'weibull',name:'Weibull (H&amp;F 6)',    note:'Minitab, Excel QUARTILE.EXC'},
  {id:'hazen', name:'Hazen (H&amp;F 5)',       note:'h = np + &frac12;'},
  {id:'linear',name:'linear (H&amp;F 7)',      note:'numpy default, Excel QUARTILE.INC'},
  {id:'midpoint',name:'midpoint',              note:'halfway between the bracketing order statistics'}
];
function cavConvention(xs,id){
  if(id==='phet'){ const q=cavQuartiles(xs); return {q1:q.q1,q3:q.q3}; }
  if(id==='tukey') return cavTukey(xs);
  if(id==='midpoint'){
    const a=cavSorted(xs), n=a.length;
    if(!n) return {q1:null,q3:null};
    const mid=p=>{ const h=clamp((n-1)*p+1,1,n), lo=Math.floor(h), hi=Math.min(lo+1,n);
                   return h===lo?a[lo-1]:0.5*(a[lo-1]+a[hi-1]); };
    return {q1:mid(0.25),q3:mid(0.75)};
  }
  const t=id==='weibull'?6:(id==='hazen'?5:7);
  return {q1:cavQuantHF(xs,0.25,t),q3:cavQuantHF(xs,0.75,t)};
}

/* --- the loss functions the balance view is about ------------------------
   sum (x-c)^2 is minimised at the MEAN and sum |x-c| at the MEDIAN; the
   first is the statement "the mean is the balance point" written as an
   extremum, and the parallel-axis identity
     sum (x-c)^2 = sum (x-xbar)^2 + n (xbar-c)^2
   makes it exact rather than numerical. */
function cavSqLoss(xs,c){ let s=0; for(const v of xs){ const d=v-c; s+=d*d; } return s; }
function cavAbsLoss(xs,c){ let s=0; for(const v of xs) s+=Math.abs(v-c); return s; }
/* the signed deviations from a point; they sum to zero exactly at the mean */
function cavDeviations(xs,c){ return xs.map(v=>v-c); }
function cavTorque(xs,c){ let s=0; for(const v of xs) s+=(v-c); return s; }
/* the two moments about a point: the total pull of the values below it and
   of those above.  At the MEAN they are equal, exactly — that is the whole
   content of "balance point", and it is a model quantity so that the
   drawing cannot compute a different one (drum_head Known-bad). */
function cavMoments(xs,c){
  let neg=0,pos=0;
  for(const v of xs){ if(v<c) neg+=c-v; else pos+=v-c; }
  return {neg,pos,gap:pos-neg};
}

/* --- the random stream ---------------------------------------------------
   mulberry32 (this collection's generator; PhET uses seedrandom) driven
   through PhET's OWN sampler.  Bit-identical to derive.py's twin: the page
   and the Python file generate the same kicks from the same seed. */
function cavRng(seed){
  let a=seed>>>0;
  return {
    next(){
      a=(a+0x6D2B79F5)>>>0;
      let t=Math.imul(a^(a>>>15),a|1);
      t=((t+Math.imul(t^(t>>>7),t|61))>>>0)^t;
      return ((t^(t>>>14))>>>0)/4294967296;
    }
  };
}
/* PhET Random.sampleProbabilities, plus valuesRange.min.  The returned index
   is the first i whose cumulative weight reaches S*u, so
   P(value = i + 1) = w[i]/S exactly — which is why every kicker's population
   mean, median, MAD and standard deviation below are closed numbers. */
function cavSampleProb(rng,w){
  let S=0; for(const v of w) S+=v;
  const t=S*rng.next();
  let s=0;
  for(let i=0;i<w.length;i++){ s+=w[i]; if(s>=t) return i+CAV.VMIN; }
  return w.length-1+CAV.VMIN;
}
function cavDrawSet(seed,w,n){
  const r=cavRng(seed), out=[];
  for(let i=0;i<n;i++) out.push(cavSampleProb(r,w));
  return out;
}

/* --- the exact population statistics of a kicker ------------------------- */
const POP_CACHE={};
function cavPop(key){
  if(POP_CACHE[key]) return POP_CACHE[key];
  const w=CAV.W[key];
  let S=0; for(const v of w) S+=v;
  const p=w.map(v=>v/S), xs=w.map((v,i)=>i+CAV.VMIN);
  let mean=0; for(let i=0;i<w.length;i++) mean+=p[i]*xs[i];
  let vr=0,mad=0,sk=0;
  for(let i=0;i<w.length;i++){
    const d=xs[i]-mean;
    vr+=p[i]*d*d; mad+=p[i]*Math.abs(d); sk+=p[i]*d*d*d;
  }
  /* the discrete quantile: the first value whose cumulative probability
     reaches the target.  When the CDF lands exactly on 1/2 the median is the
     midpoint of the two neighbouring support points, the usual convention. */
  const quant=target=>{
    let c=0;
    for(let i=0;i<w.length;i++){
      c+=p[i];
      if(c>=target-1e-15) return xs[i];
    }
    return xs[w.length-1];
  };
  let c=0, median=null;
  for(let i=0;i<w.length;i++){
    c+=p[i];
    if(c>=0.5-1e-15){
      median=xs[i];
      if(Math.abs(c-0.5)<1e-12){
        let nx=xs[i];
        for(let j=i+1;j<w.length;j++) if(p[j]>0){ nx=xs[j]; break; }
        median=0.5*(xs[i]+nx);
      }
      break;
    }
  }
  const out={key,w,S,p,xs,mean,var:vr,sd:Math.sqrt(vr),mad,median,
             q1:quant(0.25),q3:quant(0.75),skew:sk/Math.pow(vr,1.5)};
  POP_CACHE[key]=out;
  return out;
}
/* g(c) = E|X - c| for the population: convex, piecewise linear, with a kink
   at every atom.  The balance view draws it, and it is what makes the sample
   MAD's bias signed rather than always downward (derive.py C5). */
function cavGofC(key,c){
  const P=cavPop(key);
  let s=0; for(let i=0;i<P.xs.length;i++) s+=P.p[i]*Math.abs(P.xs[i]-c);
  return s;
}

/* --- a data set: the field, the kicks, the flight ------------------------ */
function cavField(seed,wkey,maxKicks){
  return {seed,wkey,max:maxKicks,rng:cavRng(seed),xs:[],air:[],kicked:0,
          queue:0,sinceKick:0,sorted:false};
}
function cavFieldClear(F){
  F.rng=cavRng(F.seed); F.xs=[]; F.air=[]; F.kicked=0; F.queue=0; F.sinceKick=0;
}
function cavFlightTime(d){
  const f=(d-CAV.VMIN)/(CAV.VMAX-CAV.VMIN);
  return CAV.T_FLY[0]+(CAV.T_FLY[1]-CAV.T_FLY[0])*clamp(f,0,1);
}
/* one kick: the distance comes from the kicker's weights, then a ball is
   animated to it.  Refuses once the field holds its maximum. */
function cavKick(F){
  if(F.xs.length+F.air.length>=F.max) return null;
  const d=cavSampleProb(F.rng,CAV.W[F.wkey]);
  F.air.push({d,t:0,T:cavFlightTime(d)});
  F.kicked++;
  return d;
}
function cavFieldBatch(F,n){
  let k=0;
  for(let i=0;i<n;i++){ if(F.xs.length+F.air.length>=F.max) break; F.xs.push(cavSampleProb(F.rng,CAV.W[F.wkey])); k++; }
  return k;
}
/* march the flights; a ball that lands joins the data set.  Returns true if
   anything moved, which is what the frame loop repaints on. */
function cavFieldStep(F,dt){
  let moved=false;
  if(F.queue>0){
    F.sinceKick+=dt;
    if(F.sinceKick>=CAV.STACK_T){
      F.sinceKick=0;
      if(cavKick(F)!==null){ F.queue--; moved=true; }
      else F.queue=0;
    }
  }
  if(F.air.length){
    const keep=[];
    for(const b of F.air){
      b.t+=dt;
      if(b.t>=b.T) F.xs.push(b.d); else keep.push(b);
    }
    if(keep.length!==F.air.length) moved=true;
    F.air=keep;
    moved=true;
  }
  return moved;
}
/* where a ball in flight is, in (metres, metres-above-the-line).  A parabola
   through (0,0) and (d,0) whose apex is APEX*d high — a drawing device, as
   PhET's is: the distance was drawn first. */
function cavBallPos(b){
  const u=clamp(b.t/b.T,0,1);
  return [b.d*u, 4*CAV.APEX*b.d*u*(1-u)];
}
/* the stack index of each landed ball, in landing order: this IS the dot
   plot, one dot per ball, stacked at its value. */
function cavStacks(xs){
  const seen={}, out=[];
  for(const v of xs){ const k=seen[v]||0; out.push(k); seen[v]=k+1; }
  return out;
}
function cavStackHeight(xs){
  const seen={}; let mx=0;
  for(const v of xs){ const k=(seen[v]||0)+1; seen[v]=k; if(k>mx) mx=k; }
  return mx;
}
/* a dragged ball takes roundSymmetric(constrain(x)) — integers only */
function cavSnapValue(x){ return clamp(cavRoundSym(x),CAV.VMIN,CAV.VMAX); }
