
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
  /* every chip row carries a data-key: four of them are labelled 1..6 and a
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
  const reParent=()=>{ const w=worldOf('parent'); w.F.cfg=cfgMystery(st.xLau);
    fieldClear(w.F); fieldBatch(w.F,st.xN); };

  /* ---- the launcher and the sample size (PhET's Sampling screen) ---- */
  const gSamp=h('div',{class:'grp'},h('h3',null,'the sampling'));
  gSamp.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gSamp.appendChild(chipRow(LAU_LIST,'pLau'));
  gSamp.appendChild(h('div',{class:'tag'},'sample size:'));
  gSamp.appendChild(chipRow(SIZE_LIST,'pN'));
  gSamp.appendChild(h('div',{class:'checks'},checkbox('showSe','σ/√n and the measured spread')));
  gSamp.appendChild(h('div',{class:'btnrow'},
    button('+20 samples',()=>{ const F=curField(st); sampleBatch(F,st.pN,20); }),
    button('clear',()=>{ const F=curField(st); fieldClear(F); })));
  const sampTag=h('div',{class:'tag'}); gSamp.appendChild(sampTag);

  /* ---- the four sample sizes ---- */
  const gSizes=h('div',{class:'grp'},h('h3',null,'the four sample sizes'));
  gSizes.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gSizes.appendChild(chipRow(LAU_LIST,'sLau'));
  gSizes.appendChild(slider('sM','samples at each n',20,200,20,v=>fmt(v,0),
    ()=>{ resetWorld('sizes'); }));
  gSizes.appendChild(h('div',{class:'checks'},checkbox('showNormal','σ/√n, the theorem')));
  const sizesTag=h('div',{class:'tag'}); gSizes.appendChild(sizesTag);

  /* ---- one launch ---- */
  const gParent=h('div',{class:'grp'},h('h3',null,'one launch'));
  gParent.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gParent.appendChild(chipRow(LAU_LIST,'xLau',reParent));
  gParent.appendChild(slider('xN','launches drawn',50,PDL.MAX_PROJ,50,v=>fmt(v,0),reParent));
  gParent.appendChild(h('div',{class:'checks'},checkbox('showDensity','the exact density')));
  const parentTag=h('div',{class:'tag'}); gParent.appendChild(parentTag);

  /* ---- the limit theorem ---- */
  const gClt=h('div',{class:'grp'},h('h3',null,'the limit theorem'));
  gClt.appendChild(h('div',{class:'tag'},'mystery launcher:'));
  gClt.appendChild(chipRow(LAU_LIST,'cLau'));
  gClt.appendChild(slider('cM','samples at each n ',100,2000,100,v=>fmt(v,0)));
  const cltTag=h('div',{class:'tag'}); gClt.appendChild(cltTag);

  /* ---- the histogram ---- */
  const gHist=h('div',{class:'grp'},h('h3',null,'the histogram'));
  gHist.appendChild(h('div',{class:'tag'},'bin width (PhET&rsquo;s list for this sim):'));
  gHist.appendChild(chipRow(BINW_LIST,'binW'));
  gHist.appendChild(h('div',{class:'tag'},'vertical scale, samples:'));
  gHist.appendChild(chipRow(ZOOM_LIST,'zoom'));
  gHist.appendChild(h('div',{class:'checks'},checkbox('blocks','blocks, one per sample'),
    checkbox('paths','paths'),checkbox('showAng','launch angle'),checkbox('showSpd','launch speed')));
  const histTag=h('div',{class:'tag'}); gHist.appendChild(histTag);

  /* ---- firing ---- */
  const gFire=h('div',{class:'grp'},h('h3',null,'firing'));
  gFire.appendChild(chipRow(MODES,'mode'));
  const fireBtn=h('button',{onclick:()=>{ S.fire(); syncPanel(); dirty=true; refresh(); }},'launch');
  gFire.appendChild(h('div',{class:'btnrow'},fireBtn));
  /* +50 at once only means anything on the parent view, where a launch IS the
     datum; on the sampling screen the datum is a whole sample */
  const batchRow=h('div',{class:'btnrow'},
    button('+50 launches',()=>{ const F=curField(st); if(F) fieldBatch(F,50); }));
  gFire.appendChild(batchRow);
  const fireTag=h('div',{class:'tag'}); gFire.appendChild(fireTag);

  /* ---- time ---- */
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs'),
    checkbox('speedUp','×6 (PhET’s fast)')));
  gRun.appendChild(h('div',{class:'btnrow'},button('reset this view',()=>{ resetView(); })));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Projectile Sampling Distributions (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s constants (g = 9.81, the 100 m field, the 0.2&ndash;5&deg; angle spreads, the three mechanisms, the six mystery launchers, the sample sizes, the bin widths and the 200-sample ceiling) are read from its published build; '
      +'everything else is derived and pinned in selfTest to build/projectile-sampling-distributions/derive.py (the exact moments by a 96-node Gauss&ndash;Legendre rule against scipy and a Monte Carlo, bit-exact mulberry32, and every sample statistic against numpy).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the mathematics'),h('div',{id:'phys'}));
  [gSamp,gSizes,gParent,gClt,gHist,gFire,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetView(){
    const v=st.view;
    for(const k in DEFAULTS) if(k!=='view') st[k]=DEFAULTS[k];
    st.view=v; resetAllWorlds();
  }
  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const v=st.view;
    gSamp.hidden=(v!=='field');
    gSizes.hidden=(v!=='sizes');
    gParent.hidden=(v!=='parent');
    gClt.hidden=(v!=='clt');
    gHist.hidden=(v==='clt');
    gFire.hidden=!(v==='field'||v==='parent');
    batchRow.hidden=(v!=='parent');
    gRun.hidden=!(v==='field'||v==='parent');
    /* the vertical-scale chips only mean anything on the screen that uses
       them: a live control that is ignored is worse than no control */
    const zoomLive=(v==='field');
    const zr=CHIPROWS.find(c=>c[2]==='zoom')[0];
    [].forEach.call(zr.children,b=>{ b.disabled=!zoomLive; b.style.opacity=zoomLive?'1':'0.4'; });
    const F=curField(st);
    fireBtn.textContent=F&&F.firing?'stop':(st.mode==='continuous'
      ?(v==='parent'?'launch continuously':'sample continuously'):(v==='parent'?'launch':'take a sample'));
    if(rows.cb_blocks) rows.cb_blocks.row.hidden=(v==='clt');
    for(const k in rows) rows[k].sync();
    const M0=buildModel();
    sampTag.innerHTML='At most '+PDL.MAX_SAMPLES+' samples a field, as PhET allows; each (launcher, n) pair keeps its own.';
    sizesTag.innerHTML='More samples sharpen the four measured spreads; they do not narrow the distributions.';
    parentTag.innerHTML='The orange curve is computed from the two input Gaussians, not fitted to the bars.';
    cltTag.innerHTML='The error bars shrink as 1/&radic;M &mdash; that is the tolerance, not the theorem.';
    histTag.innerHTML='PhET bins by floor(x/w)&middot;w, so a bin is [k w, (k+1) w). This sim&rsquo;s widths are 0.5, 1, 2 and 5 m, and it has no total-bins setting.';
    fireTag.innerHTML=(F&&F.samples&&F.samples.length>=PDL.MAX_SAMPLES)?'this field is full ('+PDL.MAX_SAMPLES+' samples, PhET&rsquo;s limit)'
      :'space launches &middot; <b>c</b> clears &middot; <b>p</b> pauses &middot; 1&ndash;4 switch views';
    runTag.innerHTML='A shot takes '+fmt(pdlFlight(M0.cfg.meanSpeed,M0.cfg.meanAng,M0.cfg.h),2)
      +' s to land; a sample of '+st.pN+' takes about '+fmt(st.pN*Math.max(PDL.LAUNCH_GAP*0.5,pdlFlight(M0.cfg.meanSpeed,M0.cfg.meanAng,M0.cfg.h)),1)+' s.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='field'||st.view==='parent')
        ?'drag the launcher up and down to change launcher · space launches · 1–4 switch views'
        :'space launches · c clears · 1–4 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncChips(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncChips(); syncPanel(); dirty=true; refresh(); } };
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
  field:'PhET&rsquo;s whole sim, in one screen. Pick a launcher and a sample size, fire a sample, and watch what survives it: not the n landing distances, but their single mean. That mean is one dot in the histogram below, and the histogram is far narrower than the landing distances that made it &mdash; averaging cancels. How much narrower is the only question the screen asks, and it has an exact answer: σ/√n, with σ the standard deviation of one launch, known outright from the launcher&rsquo;s own mechanism (see <b>one launch</b>). The orange bar across the top of the histogram is that exact σ/√n; the green bar under it is the spread the samples have actually shown so far, which wanders toward it. Drag the launcher itself to change launchers without leaving the field.',
  sizes:'PhET&rsquo;s thumbnail row, at a size you can read. The same launcher, the same number of samples, four sample sizes, and &mdash; the part that matters &mdash; one axis for all four. Nothing about the centre changes: E[x̄] = μ for every n, exactly, and averaging never biases anything. Only the width moves, and it moves as 1/√n: four times the sample halves the spread. Notice that n = 2 is already narrower than a single launch by √2, with no theorem involved at all.',
  parent:'Where σ comes from. Every standard error on the other views is σ/√n, and σ belongs to the parent: the distribution of one launch. PhET launches with two independent Gaussians &mdash; a speed and an angle &mdash; pushed through x = (v cosθ/g)(v sinθ + √(v²sin²θ + 2gh)), so that distribution is a closed problem, not something to be sampled. The orange curve is it, computed on eight panels of a 96-node quadrature rather than fitted to the bars (at a fixed distance only the angles whose v* lands within a few standard deviations of the mean speed contribute, so the integrand is a spike and one panel of the rule rings around it &mdash; by 29 % at launcher 2); the bars are however many launches the slider asks for. It is not a normal: it is skewed, and its tails are not Gaussian tails. That is exactly what makes the central limit theorem worth stating.',
  clt:'The theorem has two halves and they are usually run together. The width half &mdash; sd(x̄) = σ/√n &mdash; is exact for every n and every parent with a variance, and it follows from independence alone; no theorem is needed and none is used. The shape half is the theorem: whatever the parent looks like, the mean of n of them approaches a normal. For mystery launcher 1 the parent is skewed by −0.098 and the mean of 40 by −0.0155; every launcher has its own pair, and the readout and the caption carry the live ones. The panels below hold the first half to account: the measured standard errors against σ/√n on log axes, and then the same four residuals in units of the spread a measured standard error is entitled to, so that "they agree" comes with an error bar.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  field:'<h4>the sampling distribution of the mean</h4>'
    +EQ(1,'x&#772; = '+FR('1','n')+' &Sigma;<sub>i=1</sub><sup>n</sup> x<sub>i</sub>, &nbsp; E[x&#772;] = &mu;, &nbsp; var(x&#772;) = '+FR('&sigma;&sup2;','n'))
    +EQ(2,'<span class="rm">PhET&rsquo;s bins:</span> &lfloor;x/w&rfloor;&middot;w, &nbsp; w &isin; {0.5, 1, 2, 5} m &nbsp;<span class="rm">(this sim; the data lab adds 10)</span>')
    +EQ(3,'<span class="rm">the measured spread:</span> s = &radic;('+FR('&Sigma;(x&#772;<sub>k</sub> &minus; &lang;x&#772;&rang;)&sup2;','M &minus; 1')+'), &nbsp; sd(s) &asymp; '+FR('&sigma;','&radic;n')+'&radic;('+FR('&kappa;<sub>n</sub>+2','4M')+'))')
    +'<p>[1] needs only independence, so it is exact at n = 2. The tolerance in [3] is what makes a comparison between s and σ/√n a statement rather than an impression.</p>'
    +'<div class="cite">pins: reference sampling runs at all four sizes, the same bit-exact stream as the page, against numpy&rsquo;s mean, sd (both conventions), median and bin counts &mdash; derive.py</div>',
  sizes:'<h4>four sizes, one axis</h4>'
    +EQ(1,FR('sd(x&#772;<sub>n&#8322;</sub>)','sd(x&#772;<sub>n&#8321;</sub>)')+' = &radic;('+FR('n&#8321;','n&#8322;')+') &nbsp;&rArr;&nbsp; <span class="rm">2 &rarr; 40 narrows by</span> &radic;20 = 4.472')
    +EQ(2,'E[x&#772;<sub>n</sub>] = &mu; <span class="rm">for every n &mdash; the centre is fixed by construction</span>')
    +'<p>Drawing them on separate axes would make all four look the same, which is the one thing they are not. The shared axis is the content of the view.</p>'
    +'<div class="cite">pins: σ/√n at each size from the exact law; each measured spread inside its own sampling sd &mdash; derive.py</div>',
  parent:'<h4>the parent, exactly</h4>'
    +EQ(1,'v ~ N(&mu;<sub>v</sub>, &sigma;<sub>v</sub>&sup2;) <span class="rm">re-drawn while v &le; 0</span>, &nbsp; &theta; ~ N(&mu;<sub>&theta;</sub>, &sigma;<sub>&theta;</sub>&sup2;) <span class="rm">re-drawn while outside (0&deg;, 90&deg;)</span>')
    +EQ(2,'f<sub>X</sub>(r) = &int; f<sub>&theta;</sub>(&theta;) '+FR('f<sub>v</sub>(v*(r,&theta;))','|&part;x/&part;v|(v*,&theta;)')+' d&theta;, &nbsp; x(v*(r,&theta;), &theta;) = r')
    +EQ(3,'<span class="rm">h = 0:</span> E[x<sup>k</sup>] = '+FR('E[v<sup>2k</sup>] E[sin<sup>k</sup>2&theta;]','g<sup>k</sup>')+', &nbsp; E[sin2&theta;] = sin2&mu; e<sup>&minus;2&sigma;&sup2;</sup>')
    +'<p>Both truncations sit six standard deviations out or more; derive.py measures what they are worth (5.5&times;10<sup>&minus;8</sup> m on the mean at worst), which is what lets the closed form of [3] stand beside the quadrature.</p>'
    +'<div class="cite">pins: the 96&times;96 rule against scipy&rsquo;s adaptive quadrature (1e-15) and 6e6 simulated launches; the density integrated to 1 and to the exact mean &mdash; derive.py</div>',
  clt:'<h4>the two halves of the theorem</h4>'
    +EQ(1,'sd(x&#772;<sub>n</sub>) = &sigma;/&radic;n &nbsp;<span class="rm">exactly, for every n and every parent with a variance</span>')
    +EQ(2,'skew(x&#772;<sub>n</sub>) = '+FR('skew(x)','&radic;n')+', &nbsp; &kappa;(x&#772;<sub>n</sub>) = '+FR('&kappa;(x)','n')+' &nbsp;&rArr;&nbsp; <span class="rm">the shape goes normal</span>')
    +EQ(3,'<span class="rm">a measured SE over M samples has sd</span> &asymp; '+FR('&sigma;','&radic;n')+' &radic;('+FR('&kappa;<sub>n</sub> + 2','4M')+'))')
    +'<p>[1] is algebra; [2] is the theorem. Keeping them apart is the point of this view: a sim that only shows the widths narrowing has demonstrated [1] and called it [2].</p>'
    +'<div class="cite">pins: 2000-sample reference runs at each size, each within its own sd of σ/√n; the skewness law at all four sizes &mdash; derive.py</div>'
};
