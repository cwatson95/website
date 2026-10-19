
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
function boot(){
  const canvas=document.getElementById('scene');
  const panel=document.getElementById('panel');
  const tabsEl=document.getElementById('tabs');
  const roEl=document.getElementById('readout');
  const eqEl=document.getElementById('eqbar');
  const tagEl=document.getElementById('tag');
  const hintEl=document.getElementById('hint');
  const errEl=document.getElementById('errbox');
  const S=makeScene(canvas), st=S.st;
  let dirty=false;

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  /* every chip row carries a data-key: the UI harness matches on THAT and not
     on a label, because six of these rows are labelled 1..6 and a
     match-by-word finder would drive the wrong one (lenses.html Known-bad) */
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips','data-key':key});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(c.disabled) return;
        st[key]=o.id; if(onPick) onPick(o);
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},lab2); }

  const reFld=()=>{ const w=worldOf('field'), F=w.fields[st.fld-1];
    F.cfg=cfgMystery(st.lau); F.lau=st.lau; fieldClear(F); };
  const reSrc=()=>{ const w=worldOf('sources'); w.F.cfg=cfgCustom(st); fieldClear(w.F); };
  const reMeas=()=>{ const w=worldOf('measures');
    w.F.cfg=st.mSrc==='custom'?cfgCustom(st):cfgMystery(st.mLau); fieldClear(w.F); };
  const reExact=()=>{ const w=worldOf('exact'); w.F.cfg=cfgMystery(st.xLau,st.xOrient);
    fieldClear(w.F); fieldBatch(w.F,st.xN); };

  /* ---- the field (Variability) ---- */
  const gFld=h('div',{class:'grp'},h('h3',null,'the field'));
  gFld.appendChild(h('div',{class:'tag'},'field (each keeps its own shots):'));
  gFld.appendChild(chipRow(FIELD_LIST,'fld',()=>{ st.lau=worldOf('field').fields[st.fld-1].lau; }));
  gFld.appendChild(h('div',{class:'tag'},'mystery launcher on this field:'));
  gFld.appendChild(chipRow(LAU_LIST,'lau',reFld));
  const fldTag=h('div',{class:'tag'}); gFld.appendChild(fldTag);

  /* ---- the custom launcher (Sources, and Measures when custom) ---- */
  const gSrc=h('div',{class:'grp'},h('h3',null,'the custom launcher'));
  gSrc.appendChild(h('div',{class:'tag'},'mechanism (it sets the speed spread):'));
  gSrc.appendChild(chipRow(MECH_CHIPS,'mech',()=>{ reSrc(); reMeas(); }));
  gSrc.appendChild(slider('stab','angle stability',0,1,0.05,v=>fmt(pdlSdOfStab(v),2)+'° sd',()=>{ reSrc(); reMeas(); }));
  gSrc.appendChild(h('div',{class:'tag'},'projectile (it scales the mean speed):'));
  gSrc.appendChild(chipRow(TYPE_CHIPS,'ptype',()=>{ reSrc(); reMeas(); }));
  gSrc.appendChild(h('div',{class:'tag'},'launcher orientation:'));
  gSrc.appendChild(chipRow(ORIENT_CHIPS,'orient',()=>{ reSrc(); reMeas(); }));
  const srcTag=h('div',{class:'tag'}); gSrc.appendChild(srcTag);

  /* ---- the measures ---- */
  const gMeas=h('div',{class:'grp'},h('h3',null,'the launcher'));
  gMeas.appendChild(chipRow(SRC_CHIPS,'mSrc',reMeas));
  gMeas.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gMeas.appendChild(chipRow(LAU_LIST,'mLau',reMeas));
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},checkbox('showMean','mean'),checkbox('showSd','standard deviation'),
    checkbox('showValues','values'),checkbox('showInterval','interval tool')));
  gShow.appendChild(slider('e1','interval from',0,PDL.FIELD,0.1,v=>fmt(v,1)+' m'));
  gShow.appendChild(slider('e2','interval to',0,PDL.FIELD,0.1,v=>fmt(v,1)+' m'));
  const measTag=h('div',{class:'tag'}); gShow.appendChild(measTag);

  /* ---- the sampling ---- */
  const gSamp=h('div',{class:'grp'},h('h3',null,'the sampling'));
  gSamp.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gSamp.appendChild(chipRow(LAU_LIST,'pLau'));
  gSamp.appendChild(h('div',{class:'tag'},'sample size:'));
  gSamp.appendChild(chipRow(SIZE_LIST,'pN'));
  gSamp.appendChild(h('div',{class:'checks'},checkbox('showSe','show the standard error')));
  gSamp.appendChild(h('div',{class:'btnrow'},
    button('+20 samples',()=>{ const F=sampField(st); sampleBatch(F,st.pN,20); }),
    button('clear',()=>{ const F=sampField(st); fieldClear(F); })));
  const sampTag=h('div',{class:'tag'}); gSamp.appendChild(sampTag);

  /* ---- the exact law ---- */
  const gExact=h('div',{class:'grp'},h('h3',null,'the exact law'));
  gExact.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gExact.appendChild(chipRow(LAU_LIST,'xLau',reExact));
  gExact.appendChild(h('div',{class:'tag'},'launcher orientation:'));
  gExact.appendChild(chipRow(ORIENT_CHIPS,'xOrient',reExact));
  gExact.appendChild(slider('xN','launches drawn',50,PDL.MAX_PROJ,50,v=>fmt(v,0),reExact));
  gExact.appendChild(h('div',{class:'checks'},checkbox('showDensity','the exact density'),
    checkbox('showDelta','PhET’s delta-method normal')));
  const exactTag=h('div',{class:'tag'}); gExact.appendChild(exactTag);

  /* ---- the limit theorem ---- */
  const gClt=h('div',{class:'grp'},h('h3',null,'the limit theorem'));
  gClt.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gClt.appendChild(chipRow(LAU_LIST,'cLau'));
  gClt.appendChild(slider('cM','samples at each n',100,2000,100,v=>fmt(v,0)));
  gClt.appendChild(h('div',{class:'checks'},checkbox('showNormal','σ/√n, the theorem')));
  const cltTag=h('div',{class:'tag'}); gClt.appendChild(cltTag);

  /* ---- the histogram (shared by the four PhET screens) ---- */
  const gHist=h('div',{class:'grp'},h('h3',null,'the histogram'));
  gHist.appendChild(chipRow(BINSTRAT,'binStrat'));
  gHist.appendChild(h('div',{class:'tag'},'bin width:'));
  gHist.appendChild(chipRow(BINW_LIST,'binW'));
  gHist.appendChild(h('div',{class:'tag'},'total bins (width = 100/bins):'));
  gHist.appendChild(chipRow(NBINS_LIST,'nBins'));
  gHist.appendChild(h('div',{class:'checks'},checkbox('blocks','blocks, one per projectile'),
    checkbox('paths','paths'),checkbox('showAng','launch angle'),checkbox('showSpd','launch speed')));
  const histTag=h('div',{class:'tag'}); gHist.appendChild(histTag);

  /* ---- firing ---- */
  const gFire=h('div',{class:'grp'},h('h3',null,'firing'));
  gFire.appendChild(chipRow(MODES,'mode'));
  const fireBtn=h('button',{onclick:()=>{ S.fire(); syncPanel(); dirty=true; refresh(); }},'launch');
  gFire.appendChild(h('div',{class:'btnrow'},fireBtn,
    button('+50 at once',()=>{ const F=curField(st); if(F) fieldBatch(F,50); }),
    button('clear',()=>{ const F=curField(st); if(F) fieldClear(F); })));
  const fireTag=h('div',{class:'tag'}); gFire.appendChild(fireTag);

  /* ---- time ---- */
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs'),
    checkbox('speedUp','×6 (PhET’s fast)')));
  gRun.appendChild(h('div',{class:'btnrow'},button('reset this view',()=>{ resetView(); })));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Projectile Data Lab (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s constants (g = 9.81, the 100 m field, the 12 m raised launcher, the 0.2&ndash;5&deg; angle spreads, the three mechanisms, the six mystery launchers, the sample sizes and the bin widths) are read from its published build; '
      +'everything else is derived and pinned in selfTest to build/projectile-data-lab/derive.py (the exact moments by a 96-node Gauss&ndash;Legendre rule against scipy and a Monte Carlo, the density, bit-exact mulberry32, and every sample statistic against numpy).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the mathematics'),h('div',{id:'phys'}));
  [gFld,gSrc,gMeas,gShow,gSamp,gExact,gClt,gHist,gFire,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetView(){
    const v=st.view;
    for(const k in DEFAULTS) if(k!=='view') st[k]=DEFAULTS[k];
    st.view=v;
    resetWorld(v);
    if(v==='sampling') resetWorld('sampling');
  }
  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const v=st.view;
    gFld.hidden=(v!=='field');
    gSrc.hidden=!(v==='sources'||(v==='measures'&&st.mSrc==='custom'));
    gMeas.hidden=(v!=='measures');
    gShow.hidden=!(v==='measures');
    gSamp.hidden=(v!=='sampling');
    gExact.hidden=(v!=='exact');
    gClt.hidden=(v!=='clt');
    gHist.hidden=!(v==='field'||v==='sources'||v==='measures');
    gFire.hidden=!(v==='field'||v==='sources'||v==='measures'||v==='sampling');
    gRun.hidden=(v==='clt'||v==='exact');
    /* the bin-width and total-bins rows: only the one the strategy selects is
       live, and the other is dimmed — a control that is live but ignored is
       worse than no control (Known-bad) */
    const byW=st.binStrat==='binWidth';
    const bwRow=CHIPROWS.find(c=>c[2]==='binW')[0], nbRow=CHIPROWS.find(c=>c[2]==='nBins')[0];
    [].forEach.call(bwRow.children,b=>{ b.disabled=!byW; b.style.opacity=byW?'1':'0.4'; });
    [].forEach.call(nbRow.children,b=>{ b.disabled=byW; b.style.opacity=byW?'0.4':'1'; });
    const mysteryLive=(v!=='measures')||st.mSrc==='mystery';
    const mlRow=CHIPROWS.find(c=>c[2]==='mLau')[0];
    [].forEach.call(mlRow.children,b=>{ b.disabled=!mysteryLive; b.style.opacity=mysteryLive?'1':'0.4'; });
    const F=curField(st);
    fireBtn.textContent=F&&F.firing?'stop':(fieldMode(st)==='continuous'?'launch continuously':'launch');
    for(const k in rows) rows[k].sync();
    const M0=buildModel();
    fldTag.innerHTML='Changing a field&rsquo;s launcher clears it: a histogram of two launchers&rsquo; shots is not the distribution of anything. PhET keeps the mixed data; this does not.';
    srcTag.innerHTML='PhET&rsquo;s stabiliser runs backwards: stability 1 is the TIGHTEST launcher (0.2&deg;), stability 0 the loosest (5&deg;).';
    measTag.innerHTML='The interval tool can also be dragged on the canvas &mdash; either edge, or its middle to slide the whole window.';
    sampTag.innerHTML='At most '+PDL.MAX_SAMPLES+' samples a field, as PhET allows; each (launcher, n) pair keeps its own.';
    exactTag.innerHTML='The orange curve is computed from the two input Gaussians, not fitted to the bars.';
    cltTag.innerHTML='More samples narrow the error bars as 1/&radic;M; they do not narrow the distributions.';
    histTag.innerHTML='PhET bins by floor(x/w)&middot;w, so a bin is [k w, (k+1) w) &mdash; the left edge is included.';
    fireTag.innerHTML=(F&&F.landed.length>=PDL.MAX_PROJ)?'this field is full ('+PDL.MAX_PROJ+', PhET&rsquo;s limit)'
      :'space launches &middot; <b>c</b> clears &middot; <b>p</b> pauses &middot; 1&ndash;6 switch views';
    runTag.innerHTML='A shot takes '+fmt(pdlFlight(M0.cfg.meanSpeed*M0.cfg.mult,M0.cfg.meanAng,M0.cfg.h),2)
      +' s to land; continuous fire waits '+fmt(PDL.LAUNCH_GAP,1)+' s between shots (PhET&rsquo;s minimum).';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='measures'?'drag the interval tool’s edges or its middle · space launches · 1–6 switch views'
        :'space launches · c clears · 1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncPanel(); dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); S.fire(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='p'){ st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='c'){ const F=curField(st); if(F) fieldClear(F); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ resetView(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0;
  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        if(advanced&&frameN%8===0){ const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  field:'Six launchers, deliberately unequal. Each one throws a cannonball at a mean speed and a mean angle, and each one wobbles: the mechanism inside it scatters the speed, and how well it is braced scatters the angle. Fire one shot and you learn almost nothing; fire forty and the histogram under the field starts to have a shape. That shape is not an accident of the sampling &mdash; it is a fixed thing, the same for every run of this launcher, and <b>the exact law</b> computes it outright. Launcher 5 is the tightest (±0.2 m/s, ±0.2°) and launcher 6 the loosest (±1.2 m/s, ±5°); the field markers are every 10 m, as PhET&rsquo;s are.',
  sources:'Two dials, two sources of spread. The mechanism &mdash; spring, pressure or explosion &mdash; fixes the mean launch speed and how much it varies (23 ± 0.5, 24 ± 0.2, 25 ± 1.2 m/s, PhET&rsquo;s values). The angle stabiliser fixes how much the angle varies, from ±5° when it is off to ±0.2° when it is fully on. The panels below draw those two Gaussians; the histogram above is what the trajectory makes of them. Two things are worth trying. Set the orientation to 45° and the angle spread stops mattering almost entirely, because ∂x/∂θ = 2v²cos2θ/g vanishes there. Swap the cannonball for a pumpkin and everything scales by 1.1 in speed, 1.21 in distance &mdash; the spread grows with the mean, which is why a wider histogram is not automatically a worse launcher.',
  measures:'Now measure it. The mean x̄ is the balance point of the data; the standard deviation s is the root-mean-square distance from it, and PhET divides by n − 1 rather than n &mdash; the readout shows both so the difference is visible instead of assumed. The interval tool is the third measurement: drag its edges (on the canvas or with the sliders) and it counts what fraction of the shots lie between them, both ends included. Put it at x̄ ± s and you should capture around two thirds; at x̄ ± 2s, around ninety-five per cent &mdash; but only around, because the landing distance is not exactly normal. It is mildly skewed, and <b>the exact law</b> says by how much.',
  sampling:'A sample is n launches, and the only number kept from it is its mean. Those means go into their own histogram, and it is much narrower than the one below the field: averaging cancels. How much narrower is the whole content of the screen. The four thumbnails are the same launcher at n = 2, 5, 15 and 40, drawn on one axis, and the orange bar on each is σ/√n computed from the exact law rather than measured. The mean of the sample means stays put &mdash; averaging does not bias anything &mdash; and only the width moves.',
  exact:'The histogram is data; the orange curve is not. PhET&rsquo;s mechanism is two independent Gaussians pushed through one formula, so the distribution of the landing distance is a closed problem: for every distance r there is a speed v*(r, θ) that reaches it from each angle θ, and the density is the integral of f<sub>θ</sub>(θ) f<sub>v</sub>(v*) over the angles, divided by how fast the distance changes with speed. That integral is evaluated here on eight panels of the same 96-node rule that gives the exact mean and standard deviation &mdash; at a fixed r only the angles whose v* lands within a few standard deviations of the mean speed contribute, so the integrand is a spike and one panel of the rule rings around it by up to 29 % &mdash; and derive.py checks it against scipy and against eight million simulated launches. The two panels below make the point that shortcuts cost something: the no-jitter mean v²sin2θ/g is up to 1.5 % high, and PhET&rsquo;s own delta-method spread up to 0.7 % low.',
  clt:'The central limit theorem, measured rather than illustrated. Take '+DEFAULTS.cM+' samples at each of the four sample sizes and look at the four distributions of the sample mean: they sit on the same centre and narrow as 1/√n. The orange curves are normals of standard deviation σ/√n with σ from the exact law &mdash; nothing is fitted. The log–log panel below turns the claim into a straight line of slope −½, and each measured point carries the spread it is entitled to, σ<sub>n</sub>√((κ<sub>n</sub>+2)/4M), so "they agree" has an error bar attached. The second half of the theorem is the shape: one launch is skewed, and the skewness of the mean falls as 1/√n too.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const TRAJ='<h4>the trajectory (PhET&rsquo;s closed forms)</h4>'
  +EQ(1,'y(t) = h + v sin&theta; t &minus; '+FR('1','2')+' g t&sup2; = 0 &nbsp;&rArr;&nbsp; T = '+FR('v sin&theta; + &radic;(v&sup2;sin&sup2;&theta; + 2gh)','g'))
  +EQ(2,'x = v cos&theta; T = '+FR('v cos&theta;','g')+'(v sin&theta; + &radic;(v&sup2;sin&sup2;&theta; + 2gh)) &nbsp;&rarr;&nbsp; '+FR('v&sup2; sin2&theta;','g')+' <span class="rm">when h = 0</span>')
  +EQ(3,'<span class="rm">from a height the best angle is</span> cos2&theta;* = '+FR('g h','v&sup2; + g h')+' &nbsp;<span class="rm">(39.76&deg; at 23 m/s from 12 m)</span>');
const DERIV={
  field:TRAJ
    +'<p>g = 9.81 m/s&sup2;, the field is 100 m, the raised launcher is 12 m up, and there is no air resistance at all &mdash; PhET&rsquo;s values. The landing distance therefore depends on the launch speed and the launch angle and on nothing else, which is exactly what makes its distribution computable.</p>'
    +'<div class="cite">pins: both closed forms against a brentq root of y(t) = 0 (1e-16) and a marched trajectory (1e-11), and the maximum-range angle against a numerical argmax &mdash; derive.py</div>',
  sources:'<h4>two sources, one spread</h4>'
    +EQ(1,'v ~ N(m&middot;&mu;<sub>v</sub>, &sigma;<sub>v</sub>&sup2;) <span class="rm">re-drawn while v &le; 0</span>, &nbsp; &theta; ~ N(&mu;<sub>&theta;</sub>, &sigma;<sub>&theta;</sub>&sup2;) <span class="rm">re-drawn while outside (0&deg;, 90&deg;)</span>')
    +EQ(2,'&part;x/&part;v = '+FR('2v sin2&theta;','g')+', &nbsp; &part;x/&part;&theta; = '+FR('2v&sup2; cos2&theta;','g')+' &nbsp;&rArr;&nbsp; &sigma;<sub>x</sub>&sup2; &asymp; (&part;x/&part;v)&sup2;&sigma;<sub>v</sub>&sup2; + (&part;x/&part;&theta;)&sup2;&sigma;<sub>&theta;</sub>&sup2;')
    +EQ(3,'&sigma;<sub>&theta;</sub> = 0.2&deg; + 4.8&deg;(1 &minus; <span class="rm">stability</span>) &nbsp;<span class="rm">(PhET&rsquo;s linear map, running backwards)</span>')
    +'<p>[2] is PhET&rsquo;s own estimate &mdash; its Sampling thumbnails set their x-range from exactly this expression. It is the first-order approximation; the view <b>the exact law</b> measures what it costs.</p>'
    +'<div class="cite">pins: the stabiliser map at five settings against derive.py; both of [2]&rsquo;s coefficients against a central difference of the range itself, at four angles; and the 45&deg; cancellation, where the angle coefficient is exactly zero and 45&deg; is the range&rsquo;s stationary point</div>',
  measures:'<h4>PhET&rsquo;s three statistics</h4>'
    +EQ(1,'x&#772; = '+FR('1','n')+' &Sigma; x<sub>i</sub>, &nbsp; s&sup2; = '+FR('1','n &minus; 1')+' &Sigma;(x<sub>i</sub> &minus; x&#772;)&sup2;, &nbsp; SE = s/&radic;n')
    +EQ(2,'<span class="rm">bin(x) = </span>&lfloor;x/w&rfloor;&middot;w &nbsp;&rArr;&nbsp; <span class="rm">bin k is</span> [k w, (k+1) w)')
    +EQ(3,'<span class="rm">interval tool:</span> '+FR('#{ i : a &le; x<sub>i</sub> &le; b }','n')+' &nbsp;<span class="rm">(both ends closed)</span>')
    +'<p>s is null below two projectiles, as PhET returns null. The n and n&minus;1 conventions differ by &radic;(n/(n&minus;1)), which is 1.0010 at n = 500 and 1.41 at n = 2 &mdash; the readout prints both.</p>'
    +'<div class="cite">pins: the mean, median, both standard deviations, the standard error and every bin count at every bin width, against numpy on the SAME 500 landing distances &mdash; the same mulberry32 stream, whose integer arithmetic is bit-identical in both languages &mdash; derive.py</div>',
  sampling:'<h4>the sampling distribution of the mean</h4>'
    +EQ(1,'E[x&#772;] = &mu;, &nbsp; var(x&#772;) = '+FR('&sigma;&sup2;','n')+' &nbsp;&rArr;&nbsp; sd(x&#772;) = '+FR('&sigma;','&radic;n'))
    +EQ(2,'<span class="rm">skew(x&#772;) = skew(x)/&radic;n, &nbsp; excess kurtosis(x&#772;) = &kappa;/n</span>')
    +'<p>Both hold for any n and any parent distribution with the moments, independently of the central limit theorem &mdash; the theorem is the further statement that the SHAPE goes normal. The thumbnails draw the second; the first is already exact at n = 2.</p>'
    +'<div class="cite">pins: the 200-sample reference run (the same stream as derive.py), its mean, sd and median against numpy &mdash; derive.py</div>',
  exact:'<h4>the density of the landing distance</h4>'
    +EQ(1,'f<sub>X</sub>(r) = &int; f<sub>&theta;</sub>(&theta;) '+FR('f<sub>v</sub>(v*(r,&theta;))','|&part;x/&part;v|(v*,&theta;)')+' d&theta;, &nbsp; x(v*(r,&theta;), &theta;) = r')
    +EQ(2,'&part;x/&part;v = '+FR('cos&theta;','g')+'&#91;2v sin&theta; + '+FR('2v&sup2;sin&sup2;&theta; + 2gh','&radic;(v&sup2;sin&sup2;&theta; + 2gh)')+'&#93; &gt; 0 &nbsp;<span class="rm">(so v* is unique)</span>')
    +EQ(3,'<span class="rm">h = 0:</span> E[x<sup>k</sup>] = '+FR('E[v<sup>2k</sup>] E[sin<sup>k</sup>2&theta;]','g<sup>k</sup>')+', &nbsp; E[e<sup>ia&theta;</sup>] = e<sup>ia&mu; &minus; a&sup2;&sigma;&sup2;/2</sup>')
    +EQ(4,'E[sin2&theta;] = sin2&mu; &middot; e<sup>&minus;2&sigma;&sup2;</sup> &nbsp;&rArr;&nbsp; <span class="rm">angle jitter always SHORTENS the mean range</span>')
    +'<p>[4] is the reason launcher 2 averages 50.084 m where v&sup2;sin2&theta;/g says 50.849 m. Note also that a launcher at 30&deg; and the same launcher at 60&deg; have the SAME distribution of distance: sin2&theta; is symmetric about 45&deg;, and so is the 0&ndash;90&deg; truncation. The flight times differ; the histograms do not.</p>'
    +'<div class="cite">pins: the 96&times;96 rule against scipy&rsquo;s adaptive quadrature (1e-15), against 8e6 simulated launches, and against the closed form of the untruncated model (which differs by 5.5e-8 m &mdash; that is what the re-draws are worth) &mdash; derive.py</div>',
  clt:'<h4>the theorem, with an error bar</h4>'
    +EQ(1,'sd(x&#772;<sub>n</sub>) = &sigma;/&radic;n &nbsp;<span class="rm">exactly, for every n</span>')
    +EQ(2,'<span class="rm">a standard error measured over M samples has sd</span> &asymp; '+FR('&sigma;','&radic;n')+' &radic;('+FR('&kappa;<sub>n</sub> + 2','4M')+'), &nbsp; &kappa;<sub>n</sub> = &kappa;/n')
    +EQ(3,'skew(x&#772;<sub>n</sub>) = skew(x)/&radic;n &nbsp;&rArr;&nbsp; <span class="rm">'+fmt(-0.098047,3)+' at n = 1, '+fmt(-0.098047/Math.sqrt(40),4)+' at n = 40</span>')
    +'<p>[2] is the delta method applied to s&sup2;, and it is where the tolerance in the self-test comes from: a claim that two numbers agree is worth nothing without the spread of the one that was measured.</p>'
    +'<div class="cite">pins: &sigma;/&radic;n at the four sizes; 2000-sample reference runs at each, each within its own sd &mdash; derive.py</div>'
};
