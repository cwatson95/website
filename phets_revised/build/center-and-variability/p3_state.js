
/* ================================================================== *
 *  state: six views — PhET's three screens, then the three questions  *
 *  they raise and do not answer (which quartile rule, why the mean    *
 *  balances, and what the kicker's own weights say in the long run)   *
 * ================================================================== */
const TABS=[['kicks','the kicks'],['meanmed','mean and median'],['spread','the spread'],
            ['conv','which quartile'],['balance','the balance point'],['longrun','the long run']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', sky:'#0a1020', grass:'#16241a', line:'#3b455c',
           /* one colour slot per measure — never a borrowed role colour */
           med:'#f0b429', mean:'#6c9cff', iqr:'#38c6b4', rng:'#d76a9b', mad:'#9b8ee0',
           ball:'#e6eaf2',
           /* PhET's four jerseys: Green 1, Blue 2, Red 3, Yellow 4 */
           kick:['#7fc97f','#5b9bd5','#d9534f','#e6c84a'],
           /* the six quartile conventions in the comparison view */
           conv:['#b8ec4c','#e8843a','#38c6b4','#cd35c4','#6c9cff','#d76a9b']};
const RO_W=300;

/* the seeds the page opens on.  derive.py draws the SAME kicks from the same
   seeds (REF.seeds / REF.open), and selfTest asserts every one of them —
   including the two that were SEARCHED for rather than picked: the
   conventions view must open on a data set where the conventions actually
   disagree, and the balance view on one where the mean is a clear metre from
   the median, or each view hides the thing it exists to show. */
const SEEDS={kicks:31771, meanmed:31772, spread:31773, conv:31933, balance:31866, longrun:31790};

const KICK_LIST=KICKERS.map(k=>({id:k.id,name:''+k.n}));
const MAXK_LIST=CAV.MAX_KICKS.map(v=>({id:v,name:''+v}));
const MAXK_MED_LIST=CAV.MAX_KICKS_MEDIAN.map(v=>({id:v,name:''+v}));
const PLOT_LIST=[{id:'dot',name:'dot plot'},{id:'line',name:'line plot'}];
const MEASURES=[{id:'range',name:'range'},{id:'iqr',name:'IQR'},{id:'mad',name:'MAD'}];
const LONG_N=[10,50,200,1000,5000];
const LONG_LIST=LONG_N.map(v=>({id:v,name:''+v}));

const DEFAULTS={view:'kicks', running:true,
  /* the kicks (PhET's Median screen) */
  mKick:'k3', mMax:15, mMedian:true, mSort:false, mPlot:'dot',
  mPredict:false, mPredVal:6,
  /* mean and median (PhET's Mean & Median screen) */
  aKick:'k4', aMax:15, aMean:true, aMedian:true, aPlot:'dot',
  aPredMean:false, aPredMeanVal:9, aPredMed:false, aPredMedVal:9,
  /* the spread (PhET's Variability screen) */
  vKick:'k3', vMax:15, vMeasure:'iqr', vShow:true, vMean:false, vOutliers:true,
  vInterval:false, vH1:4, vH2:9, vPointer:false, vPtr:7,
  /* which quartile */
  cKick:'k2', cN:12,
  /* the balance point */
  bKick:'k3', bN:11, bMove:15, bLoss:true,
  /* the long run */
  lKick:'k3', lN:1000, lBands:true};
const ST=Object.assign({},DEFAULTS);

/* ---- the worlds ---------------------------------------------------------
   PhET keeps one scene per kicker on the Variability screen and one on each
   of the other two, and the data stay put when you switch back.  Same here:
   a field is made when it is first asked for, keyed by view and kicker. */
const WORLD={fields:{},draws:{}};
function fieldSeed(view,kick){
  if(view==='spread') return SEEDS.spread+KICKERS.findIndex(k=>k.id===kick)+1;
  return SEEDS[view];
}
function fieldOf(view,kick,maxK,fill){
  const key=view+'/'+kick;
  let F=WORLD.fields[key];
  if(!F){
    F=cavField(fieldSeed(view,kick),kick,maxK);
    cavFieldBatch(F,fill===undefined?maxK:fill);
    WORLD.fields[key]=F;
  }
  if(F.max!==maxK){
    F.max=maxK;
    if(F.xs.length>maxK) F.xs=F.xs.slice(0,maxK);
  }
  return F;
}
function curField(st){
  if(st.view==='kicks') return fieldOf('kicks',st.mKick,st.mMax);
  if(st.view==='meanmed') return fieldOf('meanmed',st.aKick,st.aMax);
  if(st.view==='spread') return fieldOf('spread',st.vKick,st.vMax);
  return null;
}
function resetWorlds(){ WORLD.fields={}; WORLD.draws={}; }
/* the analysis views draw their own data sets, cached by (seed, kicker, n) */
function drawsOf(seed,kick,n){
  const key=seed+'/'+kick+'/'+n;
  if(!WORLD.draws[key]) WORLD.draws[key]=cavDrawSet(seed,CAV.W[kick],n);
  return WORLD.draws[key];
}

/* ---- the clock ---------------------------------------------------------- */
const FRAME_DT=1/60;
function worldStep(st,dt){
  const F=curField(st);
  if(!F) return false;
  return cavFieldStep(F,dt);
}
function kickNow(st,n){
  const F=curField(st);
  if(!F) return 0;
  F.queue+=n; F.sinceKick=CAV.STACK_T;
  return F.queue;
}

/* ---- the model each view and the readout read --------------------------- */
function statsOf(xs){
  const q=cavQuartiles(xs);
  return {n:xs.length, mean:cavMean(xs), median:cavMedian(xs),
          q1:q.q1, q3:q.q3, iqr:q.iqr,
          range:cavRange(xs), min:cavMin(xs), max:cavMax(xs),
          madExact:cavMadExact(xs), madPhet:cavMadPhet(xs),
          sd:cavSd(xs,0), sd1:cavSd(xs,1)};
}
function kickerOf(id){ return KICKERS.find(k=>k.id===id); }
function kickerIdx(id){ return KICKERS.findIndex(k=>k.id===id); }

function buildModel(){
  const st=ST, view=st.view;
  const M={view,st};
  if(view==='kicks'){
    M.kick=st.mKick; M.F=curField(st); M.xs=M.F.xs.slice();
    M.plot=st.mPlot; M.maxK=st.mMax;
  } else if(view==='meanmed'){
    M.kick=st.aKick; M.F=curField(st); M.xs=M.F.xs.slice();
    M.plot=st.aPlot; M.maxK=st.aMax;
  } else if(view==='spread'){
    M.kick=st.vKick; M.F=curField(st); M.xs=M.F.xs.slice();
    M.plot='dot'; M.maxK=st.vMax;
    M.box=cavBox(M.xs);
    M.iv=cavInterval(M.xs,st.vH1,st.vH2);
  } else if(view==='conv'){
    M.kick=st.cKick; M.xs=drawsOf(SEEDS.conv,st.cKick,st.cN).slice(); M.plot='dot';
    M.conv=CONVENTIONS.map(c=>{
      const q=cavConvention(M.xs,c.id);
      return {id:c.id,name:c.name,note:c.note,q1:q.q1,q3:q.q3,
              iqr:(q.q1===null||q.q3===null)?null:q.q3-q.q1};
    });
    /* the disagreement is what the view is about, so it is a model quantity
       and not something the drawing works out for itself */
    const ph=M.conv[0];
    M.spreadQ1=Math.max.apply(null,M.conv.map(c=>c.q1))-Math.min.apply(null,M.conv.map(c=>c.q1));
    M.spreadQ3=Math.max.apply(null,M.conv.map(c=>c.q3))-Math.min.apply(null,M.conv.map(c=>c.q3));
    M.agrees=M.conv.filter(c=>c.id!=='phet'&&Math.abs(c.q1-ph.q1)<1e-12&&Math.abs(c.q3-ph.q3)<1e-12)
                   .map(c=>c.id);
    M.parity=(M.xs.length%2)?'odd':'even';
    M.twin=(M.xs.length%2)?'weibull':'hazen';
  } else if(view==='balance'){
    M.kick=st.bKick;
    const base=drawsOf(SEEDS.balance,st.bKick,st.bN).slice();
    base[base.length-1]=clamp(Math.round(st.bMove),CAV.VMIN,CAV.VMAX);
    M.xs=base; M.plot='dot'; M.moved=base.length-1;
    M.torque=cavTorque(M.xs,cavMean(M.xs));
    M.lossMean=cavSqLoss(M.xs,cavMean(M.xs));
    M.lossMedian=cavAbsLoss(M.xs,cavMedian(M.xs));
  } else {
    M.kick=st.lKick;
    M.xs=drawsOf(SEEDS.longrun,st.lKick,st.lN);
    M.plot='dot';
    M.counts=(()=>{ const c=new Array(CAV.VMAX-CAV.VMIN+1).fill(0);
                    for(const v of M.xs) c[v-CAV.VMIN]++; return c; })();
    M.trace=(()=>{
      const out=[]; let s=0;
      const step=Math.max(1,Math.floor(M.xs.length/240));
      for(let i=0;i<M.xs.length;i++){ s+=M.xs[i];
        if((i+1)%step===0||i===M.xs.length-1) out.push([i+1,s/(i+1)]); }
      return out;
    })();
  }
  M.pop=cavPop(M.kick);
  M.stat=statsOf(M.xs);
  M.kicker=kickerOf(M.kick);
  M.kcol=COL.kick[kickerIdx(M.kick)];
  /* the sampling law: what a sample of this size is entitled to.  Exact for
     the mean (sigma/sqrt(n)); measured by Monte Carlo in derive.py for the
     median, the MAD and the IQR, because on a 15-point lattice their
     asymptotics are not worth trusting. */
  M.seMean=M.stat.n?M.pop.sd/Math.sqrt(M.stat.n):null;
  M.zMean=(M.stat.n&&M.seMean)?(M.stat.mean-M.pop.mean)/M.seMean:null;
  return M;
}
/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function mfmt(x,n){ return (x===null||x===undefined||!isFinite(x))?'&mdash;':fmt(x,n===undefined?2:n)+' m'; }
function nfmt(x,n){ return (x===null||x===undefined||!isFinite(x))?'&mdash;':fmt(x,n===undefined?2:n); }
function kickerTitle(M){
  return M.kicker.name+' (' +M.kicker.jersey+' jersey), '+M.stat.n+' kick'+(M.stat.n===1?'':'s');
}
function centreRows(M){
  const S=M.stat;
  return hd('centre')
    +rrow('mean x&#772;',mfmt(S.mean,3),'good')
    +rrow('median',mfmt(S.median,2),'good');
}
function spreadRows(M){
  const S=M.stat;
  return hd('spread')
    +rrow('range = max &minus; min',S.range===null?'&mdash;':mfmt(S.range,0),'good')
    +rrow('Q1, Q3',S.q1===null?'&mdash; (needs five kicks)':fmt(S.q1,1)+', '+fmt(S.q3,1))
    +rrow('IQR = Q3 &minus; Q1',S.iqr===null?'&mdash;':mfmt(S.iqr,1),'good')
    +rrow('MAD, exactly',mfmt(S.madExact,4),'good')
    +rrow('MAD, PhET&rsquo;s rounding',mfmt(S.madPhet,1))
    +rrow('standard deviation &sigma;',mfmt(S.sd,3));
}
function popRows(M){
  const P=M.pop;
  return hd('the kicker, exactly (from its weights)')
    +rrow('population mean &mu;',mfmt(P.mean,4))
    +rrow('population median',mfmt(P.median,1))
    +rrow('population &sigma;',mfmt(P.sd,4))
    +rrow('population MAD',mfmt(P.mad,4))
    +rrow('skewness',nfmt(P.skew,3));
}
function readoutHTML(M){
  const st=M.st, S=M.stat;
  let s='<div class="rname">center and variability<small>'
        +TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  s+=hd(kickerTitle(M));
  if(M.view==='kicks'){
    s+=rrow('kicks on the field',S.n+' of '+M.maxK)
      +rrow('median',S.median===null?'&mdash;':mfmt(S.median,2),'good')
      +rrow('middle value'+(S.n%2?'':'s'),S.n?cavMiddle(cavSorted(M.xs)).join(', ')+' m':'&mdash;')
      +rrow('sorted',M.xs.length?cavSorted(M.xs).join(' ').slice(0,44):'&mdash;');
    if(st.mPredict) s+=rrow('your prediction',mfmt(st.mPredVal,1),
      Math.abs(st.mPredVal-(S.median===null?-99:S.median))<1e-9?'good':'bad');
    s+='</table><div class="note">With an even number of kicks the median is the mean of the two middle values &mdash; PhET&rsquo;s convention, and the one place a median has a choice to make. Drag a ball along the line to move it and watch which balls the median is actually resting on.</div>';
    return s;
  }
  if(M.view==='meanmed'){
    s+=rrow('kicks on the field',S.n+' of '+M.maxK)
      +centreRows(M)
      +rrow('mean &minus; median',S.n?mfmt(S.mean-S.median,3):'&mdash;')
      +rrow('&Sigma;(x<sub>i</sub> &minus; x&#772;)',S.n?nfmt(cavTorque(M.xs,S.mean),12):'&mdash;','good');
    if(st.aPredMean) s+=rrow('your mean prediction',mfmt(st.aPredMeanVal,1));
    if(st.aPredMed) s+=rrow('your median prediction',mfmt(st.aPredMedVal,1));
    s+=popRows(M);
    s+='</table><div class="note">The signed deviations from the mean sum to zero &mdash; that is what "balance point" means, and it is an identity, not an approximation. The median has no such property and does not move when a far ball moves further.</div>';
    return s;
  }
  if(M.view==='spread'){
    s+=rrow('kicks on the field',S.n+' of '+M.maxK)
      +spreadRows(M);
    if(M.box) s+=hd('the box plot')
      +rrow('whiskers',fmt(M.box.whiskLo,0)+' to '+fmt(M.box.whiskHi,0)+' m')
      +rrow('fences (1.5 &times; IQR)',fmt(M.box.lowFence,2)+', '+fmt(M.box.highFence,2))
      +rrow('outliers',M.box.outliers.length?M.box.outliers.join(', ')+' m':'none');
    if(st.vInterval) s+=hd('the interval tool')
      +rrow('from, to',fmt(M.iv.lo,1)+' to '+fmt(M.iv.hi,1)+' m')
      +rrow('width',mfmt(M.iv.width,1))
      +rrow('kicks inside',M.iv.count+' of '+S.n+' = '+fmt(100*M.iv.frac,1)+'%','good');
    s+='</table><div class="note">Three measures of the same thing and none of them agrees with the others about which kicker is widest. The IQR uses the middle half and ignores the tails; the range is made of the two most extreme kicks and nothing else; the MAD counts every kick, at its distance.</div>';
    return s;
  }
  if(M.view==='conv'){
    s+=rrow('kicks in the data set',S.n+' ('+M.parity+')')
      +hd('Q1 and Q3 under six conventions');
    M.conv.forEach(c=>{
      s+=rrow(plainish(c.name),fmt(c.q1,3)+', '+fmt(c.q3,3),c.id==='phet'?'good':'');
    });
    s+=hd('what that costs')
      +rrow('Q1 spread across conventions',mfmt(M.spreadQ1,3),M.spreadQ1>0?'bad':'good')
      +rrow('Q3 spread across conventions',mfmt(M.spreadQ3,3),M.spreadQ3>0?'bad':'good')
      +rrow('PhET&rsquo;s rule is identical to',M.agrees.length?M.agrees.join(', '):'none of the others');
    s+='</table><div class="note">PhET&rsquo;s exclusive median-of-halves rule is exactly Hyndman &amp; Fan type 6 (Weibull) when n is odd and type 5 (Hazen) when n is even &mdash; proved in derive.py and checked on four thousand data sets. At even n it also coincides with Tukey&rsquo;s hinges, because an even split has no middle value to argue about.</div>';
    return s;
  }
  if(M.view==='balance'){
    s+=rrow('kicks in the data set',S.n)
      +centreRows(M)
      +rrow('the moved ball',mfmt(st.bMove,0),'')
      +hd('the balance')
      +rrow('&Sigma;(x<sub>i</sub> &minus; x&#772;)',nfmt(M.torque,12),'good')
      +rrow('&Sigma;(x<sub>i</sub> &minus; x&#772;)&sup2;',nfmt(M.lossMean,4))
      +rrow('&Sigma;|x<sub>i</sub> &minus; median|',nfmt(M.lossMedian,4))
      +rrow('&Sigma;(x<sub>i</sub> &minus; median)&sup2;',nfmt(cavSqLoss(M.xs,S.median),4),'bad')
      +rrow('&Sigma;|x<sub>i</sub> &minus; x&#772;|',nfmt(cavAbsLoss(M.xs,S.mean),4),'bad');
    s+='</table><div class="note">Each estimator wins on its own loss and loses on the other&rsquo;s: the mean minimises the squared distance, the median the absolute distance. Drag the last ball across the field &mdash; the mean tracks it at exactly 1/n metres per metre, and the median stops moving as soon as the ball leaves the middle.</div>';
    return s;
  }
  s+=rrow('kicks drawn',S.n)
    +centreRows(M)
    +rrow('MAD, exactly',mfmt(S.madExact,4),'good')
    +rrow('standard deviation, the n convention',mfmt(S.sd,4),'good')
    +rrow('&hellip;and the n&minus;1 one',mfmt(S.sd1,4))
    +popRows(M)
    +hd('how close is close')
    +rrow('&sigma;/&radic;n',mfmt(M.seMean,4))
    +rrow('(x&#772; &minus; &mu;)/(&sigma;/&radic;n)',nfmt(M.zMean,3),Math.abs(M.zMean)<3?'good':'bad')
    +rrow('worst bin, in binomial sd',nfmt(longWorstZ(M),2),longWorstZ(M)<4?'good':'bad');
  s+='</table><div class="note">The kicker&rsquo;s weights are known, so &mu;, &sigma;, the population median and the population MAD are not estimated here &mdash; they are computed from the weights and the sample is judged against them, with a tolerance that comes from the sampling law rather than from taste.</div>';
  return s;
}
function longWorstZ(M){
  if(M.view!=='longrun'||!M.counts) return 0;
  const P=M.pop, N=M.xs.length;
  let worst=0;
  for(let i=0;i<M.counts.length;i++){
    if(!(P.p[i]>0)) continue;
    const e=N*P.p[i], sd=Math.sqrt(e*(1-P.p[i]));
    const z=Math.abs(M.counts[i]-e)/Math.max(sd,1e-12);
    if(z>worst) worst=z;
  }
  return worst;
}
function plainish(s){ return plain(s); }

function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='kicks') return E(
    'median = <span class="hl">x<sub>(k+1)</sub></span> <span class="rm">n = 2k+1</span> &nbsp;&middot;&nbsp; <span class="hl">&frac12;(x<sub>(k)</sub> + x<sub>(k+1)</sub>)</span> <span class="rm">n = 2k</span>',
    'the middle of the sorted data — and the average of the two middles when there is no single middle');
  if(M.view==='meanmed') return E(
    'x&#772; = <span class="hl">(1/n) &Sigma; x<sub>i</sub></span> &nbsp;&hArr;&nbsp; <span class="hl2">&Sigma;(x<sub>i</sub> &minus; x&#772;) = 0</span>',
    'the mean is the point about which the signed deviations cancel: the balance point, exactly');
  if(M.view==='spread') return E(
    'range = <span class="hl">max &minus; min</span> &nbsp;&middot;&nbsp; IQR = <span class="hl">Q3 &minus; Q1</span> &nbsp;&middot;&nbsp; MAD = <span class="hl">(1/n) &Sigma;|x<sub>i</sub> &minus; x&#772;|</span>',
    'two kicks, the middle half, or every kick at its own distance — three answers to one question');
  if(M.view==='conv') return E(
    'Q<sub>p</sub> = <span class="hl">x<sub>(&lfloor;h&rfloor;)</sub> + (h &minus; &lfloor;h&rfloor;)(x<sub>(&lceil;h&rceil;)</sub> &minus; x<sub>(&lfloor;h&rfloor;)</sub>)</span>, &nbsp; h = <span class="hl2">(n+1)p</span> <span class="rm">n odd</span>, &nbsp; <span class="hl2">np + &frac12;</span> <span class="rm">n even</span>',
    "PhET's exclusive halves, written as an order statistic: Weibull at odd n, Hazen at even n");
  if(M.view==='balance') return E(
    '&Sigma;(x<sub>i</sub> &minus; c)&sup2; = <span class="hl">&Sigma;(x<sub>i</sub> &minus; x&#772;)&sup2; + n(x&#772; &minus; c)&sup2;</span> &nbsp;&rArr;&nbsp; <span class="hl2">the mean is the unique minimiser</span>',
    'the parallel-axis identity — and |·| in place of (·)² puts the minimum at the median instead');
  return E(
    'x&#772;<sub>n</sub> &rarr; <span class="hl">&mu; = &Sigma; p<sub>i</sub> x<sub>i</sub></span>, &nbsp; sd(x&#772;<sub>n</sub>) = <span class="hl2">&sigma;/&radic;n</span> &nbsp;<span class="rm">exactly, for every n</span>',
    "the kicker's weights are known, so the target is a number and not another estimate");
}
function tagHTML(M){
  const p=t=>'<b>'+t+'</b> &mdash; ';
  const k=M.kicker.name;
  if(M.view==='kicks') return p('the kicks')+'PhET&rsquo;s Median screen: '+k+', '+M.stat.n+' of '+M.maxK+' kicks, median '+(M.stat.median===null?'—':fmt(M.stat.median,1)+' m');
  if(M.view==='meanmed') return p('mean and median')+'PhET&rsquo;s Mean &amp; Median screen: '+k+', mean '+(M.stat.n?fmt(M.stat.mean,2):'—')+' m against median '+(M.stat.n?fmt(M.stat.median,1):'—')+' m';
  if(M.view==='spread') return p('the spread')+'PhET&rsquo;s Variability screen: '+k+', '+M.st.vMeasure.toUpperCase()+' = '+
    (M.st.vMeasure==='range'?(M.stat.range===null?'—':fmt(M.stat.range,0)):
     M.st.vMeasure==='iqr'?(M.stat.iqr===null?'—':fmt(M.stat.iqr,1)):fmt(M.stat.madExact,2))+' m';
  if(M.view==='conv') return p('which quartile')+'six conventions on one data set of '+M.stat.n+' ('+M.parity+'): PhET&rsquo;s rule is the '+M.twin+' one here';
  if(M.view==='balance') return p('the balance point')+'the last ball at '+fmt(M.st.bMove,0)+' m; mean '+fmt(M.stat.mean,3)+' m, median '+fmt(M.stat.median,1)+' m';
  return p('the long run')+M.stat.n+' kicks from '+k+' against its own weights, x&#772; &minus; &mu; = '+fmt(M.stat.mean-M.pop.mean,3)+' m';
}
