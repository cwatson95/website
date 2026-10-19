
/* ================================================================== *
 *  state: the six views, their worlds (one per PhET screen, plus the  *
 *  two analysis views), the per-view model, readout, eqbar, tag       *
 * ================================================================== */
const TABS=[['field','the field'],['sources','the sources'],['measures','the measures'],
            ['sampling','the sampling'],['exact','the exact law'],['clt','the limit theorem']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', sky:'#0a1020', ground:'#141d16', bar:'#6c9cff',
           /* the six mystery launchers keep their own colour slots rather than
              borrowing a role colour (Known-bad: a new curve needs its own) */
           lau:['#e6c84a','#4fb0c6','#d76a9b','#7fc97f','#9b8ee0','#59a6d8'],
           /* the four sample sizes keep their own slots, none of them the
              reference orange the σ/√n curve owns */
           sizes:['#6c9cff','#38c6b4','#b8ec4c','#a98ae8']};
const RO_W=300;
const MODES=[{id:'single',name:'single'},{id:'continuous',name:'continuous'}];
const BINSTRAT=[{id:'binWidth',name:'bin width'},{id:'totalBins',name:'total bins'}];
const BINW_LIST=PDL.BINW.map(w=>({id:w,name:w+' m'}));
const NBINS_LIST=PDL.NBINS.map(n=>({id:n,name:''+n}));
const LAU_LIST=LAUNCHERS.map(l=>({id:l.n,name:''+l.n}));
const FIELD_LIST=[1,2,3,4,5,6].map(n=>({id:n,name:''+n}));
const SIZE_LIST=PDL.SIZES.map(n=>({id:n,name:'n = '+n}));
const MECH_CHIPS=MECH_LIST.map(m=>({id:m.id,name:m.name}));
const TYPE_CHIPS=PTYPES.map(t=>({id:t.id,name:t.name}));
const ORIENT_CHIPS=ORIENTS.map(o=>({id:o.id,name:o.name}));
const SRC_CHIPS=[{id:'mystery',name:'mystery'},{id:'custom',name:'custom'}];
const SEEDS={field:9101,sources:9201,measures:9301,sampling:9401,exact:9501,clt:9601};

const DEFAULTS={view:'field', running:true, speedUp:false,
  /* the field (Variability) */
  fld:1, lau:1, mode:'single', paths:true, showAng:false, showSpd:false,
  binStrat:'binWidth', binW:1, nBins:10, blocks:true,
  /* the sources */
  mech:'spring', stab:0.5, ptype:'cannonball', orient:'angle30', sMode:'single',
  /* the measures */
  mSrc:'mystery', mLau:2, showMean:true, showSd:true, showValues:false,
  showInterval:true, e1:PDL.INTERVAL[0], e2:PDL.INTERVAL[1],
  /* the sampling */
  pLau:1, pN:5, pMode:'single', showSe:true,
  /* the exact law */
  xLau:2, xOrient:'angle30', xN:300, showDensity:true, showDelta:true,
  /* the limit theorem */
  cLau:1, cM:400, showNormal:true};
const ST=Object.assign({},DEFAULTS);

/* ---- the worlds ------------------------------------------------------------ */
const WORLD={};
function cfgMystery(n,orientId,typeId){
  const L=LAUNCHERS[n-1];
  return pdlConfig(L.mech,L.sdAng,orientId||'angle30',typeId||'cannonball');
}
function cfgCustom(st){
  return pdlConfig(st.mech,pdlSdOfStab(st.stab),st.orient,st.ptype);
}
function makeWorld(view,st){
  if(view==='field'){
    const w={fields:[]};
    for(let i=0;i<PDL.N_FIELDS;i++){
      const F=fieldMake(SEEDS.field+i,cfgMystery(i+1));
      F.lau=i+1;
      /* the fields open with data in them: a view that draws nothing is a
         defect in this collection, and the six unequal spreads are the
         point of the screen */
      fieldBatch(F,[40,40,40,40,40,40][i]);
      w.fields.push(F);
    }
    return w;
  }
  if(view==='sources'){
    const F=fieldMake(SEEDS.sources,cfgCustom(st)); fieldBatch(F,60);
    return {F};
  }
  if(view==='measures'){
    const F=fieldMake(SEEDS.measures,st.mSrc==='custom'?cfgCustom(st):cfgMystery(st.mLau));
    fieldBatch(F,80);
    return {F};
  }
  if(view==='sampling'){
    const w={fields:{}};
    return w;
  }
  if(view==='exact'){
    const F=fieldMake(SEEDS.exact,cfgMystery(st.xLau,st.xOrient)); fieldBatch(F,st.xN);
    return {F};
  }
  /* the limit theorem: M samples at each of the four sample sizes, drawn once
     from one stream so the four columns are comparable */
  const w={sets:null};
  return w;
}
function worldOf(view){ if(!WORLD[view]) WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetWorld(view){ WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetAllWorlds(){ for(const k in WORLD) delete WORLD[k]; }
/* the Sampling screen keeps one field per (launcher, sample size), as PhET
   does — 24 of them, made when first asked for */
function sampField(st){
  const w=worldOf('sampling'), key=st.pLau+'/'+st.pN;
  if(!w.fields[key]){
    const F=fieldMake(SEEDS.sampling+st.pLau*100+st.pN,cfgMystery(st.pLau));
    F.size=st.pN; sampleBatch(F,st.pN,30);
    w.fields[key]=F;
  }
  return w.fields[key];
}
function curField(st){
  if(st.view==='field') return worldOf('field').fields[st.fld-1];
  if(st.view==='sources') return worldOf('sources').F;
  if(st.view==='measures') return worldOf('measures').F;
  if(st.view==='sampling') return sampField(st);
  if(st.view==='exact') return worldOf('exact').F;
  return null;
}
/* the limit-theorem experiment: cM samples at each size, from one stream */
function cltSets(st){
  const w=worldOf('clt');
  if(w.sets&&w.lau===st.cLau&&w.M===st.cM) return w.sets;
  const cfg=cfgMystery(st.cLau), rng=pdlRng(SEEDS.clt+st.cLau);
  const sets=PDL.SIZES.map(n=>{
    const means=[];
    for(let k=0;k<st.cM;k++){
      let s=0;
      for(let i=0;i<n;i++){ const d=pdlDraw(rng,cfg); s+=pdlRange(d.v,d.ang,cfg.h); }
      means.push(s/n);
    }
    return {n,means,mean:pdlMean(means),sd:pdlSd(means,1)};
  });
  w.sets=sets; w.lau=st.cLau; w.M=st.cM; w.exact=pdlExact(cfg);
  return sets;
}

/* ---- the clock -------------------------------------------------------------
   one frame is 1/60 s of flight; PhET's "fast" is 6x (TIME_SPEED_FAST) */
const FRAME_DT=1/60;
function viewDt(st){ return FRAME_DT*(st.speedUp?PDL.TIME_SPEED_FAST||6:1); }
function fieldMode(st){ return st.view==='sources'?st.sMode:(st.view==='sampling'?st.pMode:st.mode); }
function worldStep(st,dt){
  const F=curField(st);
  if(!F) return false;
  let moved=fieldStep(F,dt);
  if(F.firing){
    if(st.view==='sampling'){
      /* PhET's pace: the n launches are spread evenly over totalSampleTime
         and their flights overlap; the sample completes when the last lands */
      F.tSample+=dt;
      const step=sampleStep(F.size);
      while(F.launched<F.size&&F.tSample>=F.launched*step){ fieldLaunch(F); F.launched++; moved=true; }
      if(F.launched>=F.size&&F.air.length===0){
        const xs=F.landed.slice(-F.size).map(p=>p.x);
        F.sampleN++; F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs)});
        F.firing=fieldMode(st)==='continuous'&&F.samples.length<PDL.MAX_SAMPLES;
        if(F.firing) sampleStart(F); else { F.launched=0; F.tSample=0; }
        moved=true;
      }
    } else if(F.sinceLaunch>=PDL.LAUNCH_GAP){
      fieldLaunch(F); moved=true;
      if(fieldMode(st)==='single') F.firing=false;
      if(F.landed.length+F.air.length>=PDL.MAX_PROJ) F.firing=false;
    }
  }
  return moved||F.air.length>0;
}
function fireField(st){
  const F=curField(st); if(!F) return;
  if(st.view==='sampling'){
    if(F.firing){ F.firing=false; F.launched=0; F.tSample=0; return; }
    if(F.samples.length>=PDL.MAX_SAMPLES) return;
    F.firing=true; sampleStart(F);
    return;
  }
  if(F.firing&&fieldMode(st)==='continuous'){ F.firing=false; return; }
  F.firing=true; F.sinceLaunch=PDL.LAUNCH_GAP;
}

/* ---- the model each view and the readout read ------------------------------ */
function binWidthOf(st){ return st.binStrat==='binWidth'?st.binW:PDL.FIELD/st.nBins; }
/* a 1-2-5 step near x, for an axis whose bin width has to follow the data */
function niceStep(x){
  if(!(x>0)) return 1;
  const e=Math.pow(10,Math.floor(Math.log10(x))), n=x/e;
  return (n<1.5?1:n<3.5?2:n<7.5?5:10)*e;
}
function statsOf(xs){
  return {n:xs.length, mean:pdlMean(xs), median:pdlMedian(xs),
          sd1:pdlSd(xs,1), sd0:pdlSd(xs,0), se:pdlSe(xs),
          min:xs.length?Math.min.apply(null,xs):null, max:xs.length?Math.max.apply(null,xs):null};
}
function buildModel(){
  const st=ST, view=st.view;
  const M={view,st};
  if(view==='field'){
    const w=worldOf('field'); M.fields=w.fields; M.F=w.fields[st.fld-1];
    M.cfg=M.F.cfg; M.lau=M.F.lau;
  } else if(view==='sources'){
    M.F=worldOf('sources').F; M.cfg=M.F.cfg; M.lau=null;
  } else if(view==='measures'){
    M.F=worldOf('measures').F; M.cfg=M.F.cfg; M.lau=st.mSrc==='mystery'?st.mLau:null;
  } else if(view==='sampling'){
    M.F=sampField(st); M.cfg=M.F.cfg; M.lau=st.pLau;
    M.means=sampleMeans(M.F); M.mstat=statsOf(M.means);
  } else if(view==='exact'){
    M.F=worldOf('exact').F; M.cfg=M.F.cfg; M.lau=st.xLau;
  } else {
    M.sets=cltSets(st); M.exact=worldOf('clt').exact; M.lau=st.cLau; M.cfg=cfgMystery(st.cLau);
  }
  if(M.F){
    M.xs=fieldXs(M.F);
    M.stat=statsOf(M.xs);
    /* the exact-law view is about the SHAPE, and it does not show the bin
       chips, so its bins follow the distribution rather than whatever the
       other screens were last set to: a control the view hides must not
       still be deciding its picture */
    M.binW=view==='exact'?niceStep(pdlExact(M.cfg||cfgMystery(st.xLau,st.xOrient)).sd/4):binWidthOf(st);
    M.hist=pdlHistogram(M.xs,M.binW);
    M.frac=pdlFraction(M.xs,st.e1,st.e2);
  }
  if(M.cfg){
    M.exact=M.exact||pdlExact(M.cfg);
    const mu=M.cfg.meanSpeed*M.cfg.mult;
    M.naive=M.cfg.h>0?null:mu*mu*Math.sin(2*M.cfg.meanAng*Math.PI/180)/PDL.G;
    M.delta=M.cfg.h>0?null:pdlDeltaSd(mu,M.cfg.sdSpeed,M.cfg.meanAng,M.cfg.sdAng);
  }
  if(view==='exact') M.probIn=pdlProbIn(M.cfg,st.e1,st.e2,60);
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function mfmt(x,n){ return x===null||x===undefined||!isFinite(x)?'—':fmt(x,n===undefined?2:n)+' m'; }
function launcherLabel(M){
  if(M.lau) return 'mystery launcher '+M.lau+' ('+MECH[LAUNCHERS[M.lau-1].mech].name+')';
  return 'custom launcher ('+MECH[M.cfg.mech].name+')';
}
function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">projectile data lab<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='clt'){
    s+=hd('one launch, exactly')+rrow('launcher',M.lau)
      +rrow('mean &mu;',mfmt(M.exact.mean,3),'good')
      +rrow('standard deviation &sigma;',mfmt(M.exact.sd,4),'good')
      +rrow('skewness, excess kurtosis',fmt(M.exact.skew,4)+', '+fmt(M.exact.kurt,4));
    s+=hd(st.cM+' samples at each size');
    M.sets.forEach(S=>{
      const want=M.exact.sd/Math.sqrt(S.n);
      s+=rrow('n = '+S.n+': measured SE',mfmt(S.sd,4),'good')
        +rrow('&nbsp;&nbsp;&sigma;/&radic;n',mfmt(want,4))
        +rrow('&nbsp;&nbsp;difference, in its own sd',fmt((S.sd-want)/(want*Math.sqrt(((M.exact.kurt/S.n)+2)/(4*st.cM))),2));
    });
    s+='</table><div class="note">The sampling sd of a standard error measured over M samples is &sigma;<sub>n</sub>&radic;((&kappa;<sub>n</sub>+2)/4M), with &kappa;<sub>n</sub> = &kappa;/n the excess kurtosis of the mean &mdash; that is the tolerance, computed rather than chosen.</div>';
    return s;
  }
  const S=M.stat;
  s+=hd(launcherLabel(M))
    +rrow('mean launch speed',fmt(M.cfg.meanSpeed*M.cfg.mult,2)+' &plusmn; '+fmt(M.cfg.sdSpeed,2)+' m/s')
    +rrow('launch angle',fmt(M.cfg.meanAng,0)+'&deg; &plusmn; '+fmt(M.cfg.sdAng,2)+'&deg;')
    +rrow('launch height',fmt(M.cfg.h,0)+' m');
  s+=hd('the exact law behind it')
    +rrow('mean distance &mu;',mfmt(M.exact.mean,3),'good')
    +rrow('standard deviation &sigma;',mfmt(M.exact.sd,4),'good')
    +(M.naive===null?'':rrow('v&sup2; sin2&theta;/g (no jitter)',mfmt(M.naive,3)))
    +(M.delta===null?'':rrow('PhET&rsquo;s delta-method &sigma;',mfmt(M.delta,4)));
  if(M.view==='sampling'){
    const q=M.mstat;
    s+=hd('samples of n = '+st.pN)
      +rrow('samples completed',q.n+' of '+PDL.MAX_SAMPLES)
      +rrow('mean of the sample means',mfmt(q.mean,3),'good')
      +rrow('sd of the sample means',mfmt(q.sd1,4),'good')
      +rrow('&sigma;/&radic;n (the standard error)',mfmt(M.exact.sd/Math.sqrt(st.pN),4))
      +rrow('this sample&rsquo;s mean',M.F.samples.length?mfmt(M.F.samples[M.F.samples.length-1].mean,3):'—','good');
    s+='</table><div class="note">Each sample contributes ONE point to the histogram: its mean. The spread of those points is the standard error, and it shrinks as 1/&radic;n &mdash; see <b>the limit theorem</b>.</div>';
    return s;
  }
  s+=hd(S.n+' landed'+(M.F.air.length?' (+'+M.F.air.length+' in flight)':''))
    +rrow('mean x&#772;',mfmt(S.mean,3),'good')
    +rrow('median',mfmt(S.median,3),'good')
    +rrow('standard deviation s (n&minus;1)',mfmt(S.sd1,4),'good')
    +rrow('the n convention, for contrast',mfmt(S.sd0,4))
    +rrow('standard error s/&radic;n',mfmt(S.se,4))
    +rrow('smallest, largest',S.n?fmt(S.min,2)+', '+fmt(S.max,2)+' m':'—');
  if(M.view==='measures'||M.view==='exact'){
    s+=hd('the interval tool')
      +rrow('from, to',fmt(Math.min(st.e1,st.e2),1)+', '+fmt(Math.max(st.e1,st.e2),1)+' m')
      +rrow('width',mfmt(Math.abs(st.e2-st.e1),1))
      +rrow('of the data inside',fmt(100*M.frac,1)+'%','good')
      +(M.view==='exact'?rrow('the exact law says',fmt(100*M.probIn,1)+'%'):'');
  }
  s+=hd('the histogram')
    +rrow('bin width',fmt(M.binW,2)+' m'+(M.view==='exact'?' (&sigma;/4, rounded)'
      :(st.binStrat==='totalBins'?' (100/'+st.nBins+')':'')))
    +rrow('bins with data, tallest',M.hist.counts.length+', '+M.hist.max);
  s+='</table><div class="note">'+(S.n<2?'The standard deviation needs two projectiles: PhET returns nothing below that, and so does this.'
    :'PhET divides by n &minus; 1, not n; at n = '+S.n+' that is a factor '+fmt(Math.sqrt(S.n/(S.n-1)),5)+'. Both are shown so the difference is visible rather than assumed.')+'</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='field') return E('x = <span class="hl">(v cos&theta;/g)</span> (v sin&theta; + &radic;(v&sup2;sin&sup2;&theta; + 2gh)) &nbsp;&middot;&nbsp; h = 0: x = v&sup2; sin2&theta;/g',
    'one launch, one distance — the scatter in the histogram is the scatter in v and θ, nothing else');
  if(M.view==='sources') return E('&sigma;<sub>x</sub>&sup2; &asymp; <span class="hl">(&part;x/&part;v)&sup2; &sigma;<sub>v</sub>&sup2;</span> + <span class="hl2">(&part;x/&part;&theta;)&sup2; &sigma;<sub>&theta;</sub>&sup2;</span>, &nbsp; &part;x/&part;v = 2v sin2&theta;/g, &nbsp; &part;x/&part;&theta; = 2v&sup2; cos2&theta;/g',
    'two sources of variability: the mechanism sets σ_v, the angle stabiliser sets σ_θ — and at 45° the angle term switches off');
  if(M.view==='measures') return E('x&#772; = &Sigma;x<sub>i</sub>/n &nbsp;&middot;&nbsp; <span class="hl">s = &radic;(&Sigma;(x<sub>i</sub>&minus;x&#772;)&sup2;/(n&minus;1))</span> &nbsp;&middot;&nbsp; SE = s/&radic;n',
    'PhET’s conventions: the mean, the n − 1 standard deviation, and the interval tool’s count of x in [a, b]');
  if(M.view==='sampling') return E('x&#772; = <span class="hl">(1/n) &Sigma;<sub>i=1</sub><sup>n</sup> x<sub>i</sub></span> &nbsp;&rArr;&nbsp; E[x&#772;] = &mu;, &nbsp; <span class="hl2">sd(x&#772;) = &sigma;/&radic;n</span>',
    'one dot per sample, and the dot is its mean: the sampling distribution of the sample mean');
  if(M.view==='exact') return E('f<sub>X</sub>(r) = <span class="hl">&int; f<sub>&theta;</sub>(&theta;) f<sub>v</sub>(v*(r,&theta;)) / |&part;x/&part;v| d&theta;</span>, &nbsp; x(v*,&theta;) = r',
    'the density of the landing distance, computed from the two input Gaussians rather than sampled');
  return E('E[x&#772;] = &mu; &nbsp;&middot;&nbsp; <span class="hl">sd(x&#772;) = &sigma;/&radic;n</span> &nbsp;&middot;&nbsp; skew(x&#772;) = skew(x)/&radic;n',
    'the central limit theorem: the mean of n draws is centred on μ, narrower by √n, and closer to a normal');
}
function tagHTML(M){
  const p=t=>'<b>'+t+'</b> — ';
  if(M.view==='field') return p('the field')+'PhET&rsquo;s Variability screen: field '+M.st.fld+', '+launcherLabel(M);
  if(M.view==='sources') return p('the sources')+'PhET&rsquo;s Sources screen: '+MECH[M.cfg.mech].name+', angle &plusmn;'+fmt(M.cfg.sdAng,2)+'&deg;, '+M.cfg.type;
  if(M.view==='measures') return p('the measures')+'PhET&rsquo;s Measures screen: mean, standard deviation and the interval tool';
  if(M.view==='sampling') return p('the sampling')+'PhET&rsquo;s Sampling screen: samples of n = '+M.st.pN+' from launcher '+M.st.pLau;
  if(M.view==='exact') return p('the exact law')+'the density PhET&rsquo;s mechanism implies, against '+M.stat.n+' launches';
  return p('the limit theorem')+'the standard error against &sigma;/&radic;n at n = 2, 5, 15 and 40';
}
