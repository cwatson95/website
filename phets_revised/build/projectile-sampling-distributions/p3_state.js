
/* ================================================================== *
 *  state: four views — PhET's one screen, its thumbnail row at full   *
 *  size, the parent distribution the samples come from, and the       *
 *  theorem that ties the two together                                 *
 * ================================================================== */
const TABS=[['field','the field'],['sizes','the four sample sizes'],
            ['parent','one launch'],['clt','the limit theorem']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', sky:'#0a1020', ground:'#141d16', bar:'#6c9cff',
           /* the six mystery launchers keep their own colour slots rather than
              borrowing a role colour, and none of them is the reference
              orange the σ/√n curve owns */
           lau:['#e6c84a','#4fb0c6','#d76a9b','#7fc97f','#9b8ee0','#59a6d8'],
           sizes:['#6c9cff','#38c6b4','#b8ec4c','#a98ae8']};
const RO_W=300;
const MODES=[{id:'single',name:'single'},{id:'continuous',name:'continuous'}];
const BINW_LIST=PDL.BINW.map(w=>({id:w,name:w+' m'}));
const LAU_LIST=LAUNCHERS.map(l=>({id:l.n,name:''+l.n}));
const SIZE_LIST=PDL.SIZES.map(n=>({id:n,name:'n = '+n}));
/* PhET's zoom ladder, plus an auto rung at the front: PhET opens at its
   widest and lets the user zoom in, but a default that draws 24 samples
   against a ceiling of 50 leaves the histogram a sliver at the bottom of an
   empty panel, and a default that hides the data is a defect, not a
   preference.  Auto picks the tightest rung of PhET's OWN ladder that holds
   the tallest bin. */
const ZOOM_LIST=[{id:-1,name:'auto'}].concat(PDL.ZOOM_MAX.map((z,i)=>({id:i,name:'0–'+z})));
/* PhET's rungs are built for a full 200 samples, so its tightest (0–25) still
   leaves two dozen samples a sliver along the bottom.  The auto rung carries
   a finer ladder below PhET's, stepped so the axis does not jitter as the
   samples arrive; every rung PhET offers is still reachable by hand. */
const ZOOM_FINE=[4,6,8,10,15,20];
function autoZoom(maxCount){
  const want=Math.max(4,Math.ceil(maxCount*1.15));
  for(const z of ZOOM_FINE) if(z>=want) return z;
  for(let i=PDL.ZOOM_MAX.length-1;i>=0;i--) if(PDL.ZOOM_MAX[i]>=want) return PDL.ZOOM_MAX[i];
  return PDL.ZOOM_MAX[0];
}
const SEEDS={field:5101,sizes:5201,parent:5301,clt:5401};

const DEFAULTS={view:'field', running:true, speedUp:false,
  /* the field (PhET's Sampling screen) */
  pLau:1, pN:5, mode:'single', binW:PDL.BINW_DEF, zoom:-1,
  showSe:true, paths:true, blocks:false, showAng:false, showSpd:false,
  /* the four sample sizes */
  sLau:1, sM:60,
  /* one launch */
  xLau:1, xN:300, showDensity:true,
  /* the limit theorem */
  cLau:1, cM:400, showNormal:true};
const ST=Object.assign({},DEFAULTS);

/* ---- the worlds ------------------------------------------------------------ */
const WORLD={};
function cfgMystery(n){
  const L=LAUNCHERS[n-1];
  return pdlConfig(L.mech,L.sdAng,'angle30','cannonball');
}
function makeWorld(view,st){
  if(view==='parent'){
    const F=fieldMake(SEEDS.parent,cfgMystery(st.xLau)); fieldBatch(F,st.xN);
    return {F};
  }
  if(view==='clt') return {sets:null};
  return {fields:{}};
}
function worldOf(view){ if(!WORLD[view]) WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetWorld(view){ WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetAllWorlds(){ for(const k in WORLD) delete WORLD[k]; }
/* PhET keeps one field per (launcher, sample size) — 24 of them, made when
   first asked for.  The thumbnail row uses its own set, so filling it cannot
   move the screen the user is firing on. */
function sampFieldOf(view,lau,n,fill){
  const w=worldOf(view), key=lau+'/'+n;
  if(!w.fields[key]){
    const F=fieldMake(SEEDS[view]+lau*100+n,cfgMystery(lau));
    F.size=n; F.lau=lau;
    sampleBatch(F,n,fill);
    w.fields[key]=F;
  }
  return w.fields[key];
}
function curField(st){
  if(st.view==='field') return sampFieldOf('field',st.pLau,st.pN,24);
  if(st.view==='parent') return worldOf('parent').F;
  return null;
}
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

/* ---- the clock ------------------------------------------------------------ */
const FRAME_DT=1/60;
function viewDt(st){ return FRAME_DT*(st.speedUp?PDL.TIME_SPEED_FAST:1); }
function worldStep(st,dt){
  const F=curField(st);
  if(!F) return false;
  let moved=fieldStep(F,dt);
  if(F.firing){
    if(st.view==='parent'){
      if(F.sinceLaunch>=PDL.LAUNCH_GAP){
        fieldLaunch(F); moved=true;
        if(st.mode==='single') F.firing=false;
        if(F.landed.length+F.air.length>=PDL.MAX_PROJ) F.firing=false;
      }
    } else {
      /* PhET's pace: the n launches are spread evenly over totalSampleTime
         and their flights overlap; the sample completes when the last lands */
      F.tSample+=dt;
      const step=sampleStep(F.size);
      while(F.launched<F.size&&F.tSample>=F.launched*step){ fieldLaunch(F); F.launched++; moved=true; }
      if(F.launched>=F.size&&F.air.length===0){
        const xs=F.landed.slice(-F.size).map(p=>p.x);
        F.sampleN++; F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs)});
        F.firing=st.mode==='continuous'&&F.samples.length<PDL.MAX_SAMPLES;
        if(F.firing) sampleStart(F); else { F.launched=0; F.tSample=0; }
        moved=true;
      }
    }
  }
  return moved||F.air.length>0;
}
function fireField(st){
  const F=curField(st); if(!F) return;
  if(st.view==='parent'){
    if(F.firing&&st.mode==='continuous'){ F.firing=false; return; }
    F.firing=true; F.sinceLaunch=PDL.LAUNCH_GAP; return;
  }
  if(F.firing){ F.firing=false; F.launched=0; F.tSample=0; return; }
  if(F.samples.length>=PDL.MAX_SAMPLES) return;
  F.firing=true; sampleStart(F);
}

/* ---- the model each view and the readout read ------------------------------ */
function statsOf(xs){
  return {n:xs.length, mean:pdlMean(xs), median:pdlMedian(xs),
          sd1:pdlSd(xs,1), sd0:pdlSd(xs,0), se:pdlSe(xs),
          min:xs.length?Math.min.apply(null,xs):null, max:xs.length?Math.max.apply(null,xs):null};
}
function buildModel(){
  const st=ST, view=st.view;
  const M={view,st};
  if(view==='field'){
    M.F=curField(st); M.lau=st.pLau; M.cfg=M.F.cfg; M.size=st.pN;
    M.means=sampleMeans(M.F); M.mstat=statsOf(M.means);
    M.xs=fieldXs(M.F); M.stat=statsOf(M.xs);
  } else if(view==='sizes'){
    M.lau=st.sLau; M.cfg=cfgMystery(st.sLau);
    M.sets=PDL.SIZES.map(n=>{
      const F=sampFieldOf('sizes',st.sLau,n,st.sM);
      const means=sampleMeans(F);
      return {n,F,means,stat:statsOf(means)};
    });
  } else if(view==='parent'){
    M.F=worldOf('parent').F; M.lau=st.xLau; M.cfg=M.F.cfg;
    M.xs=fieldXs(M.F); M.stat=statsOf(M.xs);
  } else {
    M.sets=cltSets(st); M.exact=worldOf('clt').exact; M.lau=st.cLau; M.cfg=cfgMystery(st.cLau);
  }
  M.exact=M.exact||pdlExact(M.cfg);
  M.binW=st.binW;
  if(M.xs) M.hist=pdlHistogram(M.xs,M.binW);
  M.zoomMax=st.zoom>=0?PDL.ZOOM_MAX[st.zoom]
    :autoZoom(M.means?pdlHistogram(M.means,M.binW).max:0);
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function mfmt(x,n){ return x===null||x===undefined||!isFinite(x)?'—':fmt(x,n===undefined?2:n)+' m'; }
function launcherLabel(M){ return 'mystery launcher '+M.lau+' ('+MECH[LAUNCHERS[M.lau-1].mech].name+')'; }
function readoutHTML(M){
  const st=M.st, E=M.exact;
  let s='<div class="rname">sampling distributions<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  s+=hd(launcherLabel(M))
    +rrow('mean launch speed',fmt(M.cfg.meanSpeed,2)+' &plusmn; '+fmt(M.cfg.sdSpeed,2)+' m/s')
    +rrow('launch angle',fmt(M.cfg.meanAng,0)+'&deg; &plusmn; '+fmt(M.cfg.sdAng,2)+'&deg;');
  s+=hd('one launch, exactly')
    +rrow('mean &mu;',mfmt(E.mean,3),'good')
    +rrow('standard deviation &sigma;',mfmt(E.sd,4),'good')
    +rrow('skewness, excess kurtosis',fmt(E.skew,4)+', '+fmt(E.kurt,4));
  if(M.view==='field'){
    const q=M.mstat, se=E.sd/Math.sqrt(st.pN);
    s+=hd('samples of n = '+st.pN)
      +rrow('samples completed',q.n+' of '+PDL.MAX_SAMPLES)
      +rrow('this sample&rsquo;s mean',M.F.samples.length?mfmt(M.F.samples[M.F.samples.length-1].mean,3):'—','good')
      +rrow('mean of the sample means',mfmt(q.mean,3),'good')
      +rrow('their standard deviation',mfmt(q.sd1,4),'good')
      +rrow('&sigma;/&radic;n, the standard error',mfmt(se,4))
      +rrow('their median',mfmt(q.median,3))
      +rrow('bin width',fmt(M.binW,2)+' m, scale 0&ndash;'+M.zoomMax+(st.zoom<0?' (auto)':''));
    s+='</table><div class="note">A sample contributes ONE point: its mean. '
      +(q.n>2?'At '+q.n+' samples the measured spread is '+fmt(q.sd1/se,3)+' of &sigma;/&radic;n; the sampling sd of that ratio is '+fmt(Math.sqrt(((E.kurt/st.pN)+2)/(4*q.n)),3)+'.'
             :'Two samples are not a distribution &mdash; fire more.')+'</div>';
    return s;
  }
  if(M.view==='sizes'){
    s+=hd(st.sM+' samples at each size');
    M.sets.forEach(S=>{
      const want=E.sd/Math.sqrt(S.n);
      s+=rrow('n = '+S.n+': measured spread',mfmt(S.stat.sd1,4),'good')
        +rrow('&nbsp;&nbsp;&sigma;/&radic;n',mfmt(want,4));
    });
    s+='</table><div class="note">One axis for all four, so the widths can be read against each other: every step up in n narrows the distribution by &radic;(n&#8322;/n&#8321;), and nothing else about it moves.</div>';
    return s;
  }
  if(M.view==='parent'){
    const S=M.stat;
    s+=hd(S.n+' single launches'+(M.F.air.length?' (+'+M.F.air.length+' in flight)':''))
      +rrow('mean x&#772;',mfmt(S.mean,3),'good')
      +rrow('median',mfmt(S.median,3),'good')
      +rrow('standard deviation s (n&minus;1)',mfmt(S.sd1,4),'good')
      +rrow('the n convention, for contrast',mfmt(S.sd0,4))
      +rrow('standard error s/&radic;n',mfmt(S.se,4))
      +rrow('smallest, largest',S.n?fmt(S.min,2)+', '+fmt(S.max,2)+' m':'—')
      +rrow('bin width',fmt(M.binW,2)+' m');
    s+='</table><div class="note">This is the parent the samples are drawn from. Its &sigma; is what every standard error on the other views divides by &radic;n &mdash; and it is known exactly, so nothing here is fitted.</div>';
    return s;
  }
  s+=hd(st.cM+' samples at each size');
  M.sets.forEach(S=>{
    const want=E.sd/Math.sqrt(S.n);
    const tol=want*Math.sqrt((E.kurt/S.n+2)/(4*st.cM));
    s+=rrow('n = '+S.n+': measured SE',mfmt(S.sd,4),'good')
      +rrow('&nbsp;&nbsp;&sigma;/&radic;n',mfmt(want,4))
      +rrow('&nbsp;&nbsp;difference, in its own sd',fmt((S.sd-want)/tol,2));
  });
  s+='</table><div class="note">The sampling sd of a standard error measured over M samples is &sigma;<sub>n</sub>&radic;((&kappa;<sub>n</sub>+2)/4M) with &kappa;<sub>n</sub> = &kappa;/n &mdash; the tolerance, computed rather than chosen.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='field') return E('x&#772; = <span class="hl">(1/n) &Sigma;<sub>i=1</sub><sup>n</sup> x<sub>i</sub></span> &nbsp;&rArr;&nbsp; E[x&#772;] = &mu;, &nbsp; <span class="hl2">sd(x&#772;) = &sigma;/&radic;n</span>',
    'one dot per sample, and the dot is its mean: the sampling distribution of the sample mean');
  if(M.view==='sizes') return E('sd(x&#772;<sub>n&#8322;</sub>)/sd(x&#772;<sub>n&#8321;</sub>) = <span class="hl">&radic;(n&#8321;/n&#8322;)</span> &nbsp;&middot;&nbsp; E[x&#772;<sub>n</sub>] = &mu; <span class="rm">for every n</span>',
    'four sample sizes on one axis: the centre never moves, only the width');
  if(M.view==='parent') return E('x = <span class="hl">(v cos&theta;/g)</span> (v sin&theta; + &radic;(v&sup2;sin&sup2;&theta; + 2gh)) &nbsp;&middot;&nbsp; h = 0: x = v&sup2; sin2&theta;/g',
    'one launch, one distance — and its whole distribution follows from the two Gaussians that made it');
  return E('sd(x&#772;<sub>n</sub>) = <span class="hl">&sigma;/&radic;n</span> <span class="rm">exactly, for every n</span> &nbsp;&middot;&nbsp; skew(x&#772;<sub>n</sub>) = skew(x)/&radic;n',
    'the width is not the theorem — independence alone gives it; the theorem is what happens to the shape');
}
function tagHTML(M){
  const p=t=>'<b>'+t+'</b> — ';
  if(M.view==='field') return p('the field')+'PhET&rsquo;s Sampling screen: samples of n = '+M.st.pN+' from launcher '+M.st.pLau;
  if(M.view==='sizes') return p('the four sample sizes')+'launcher '+M.st.sLau+', '+M.st.sM+' samples at each of n = 2, 5, 15, 40';
  if(M.view==='parent') return p('one launch')+'the parent distribution of launcher '+M.st.xLau+', against its exact density';
  return p('the limit theorem')+'the measured standard error against &sigma;/&radic;n';
}
