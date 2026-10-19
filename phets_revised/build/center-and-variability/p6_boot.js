
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
  /* `dirty` asks the frame loop to repaint.  It is set ONLY by the two
     pointer handlers, which are the only ones that change the picture
     without calling refresh(); every other handler calls refresh(), which
     draws unconditionally, so a `dirty=true` beside it would ask for one
     extra identical frame and nothing else.  Twelve handlers had exactly
     that, and the mutation sweep found it: deleting the flag from a slider
     changed nothing any test could see, because the slider had already
     drawn.  A flag that means nothing on a path is worse than no flag. */
  let dirty=false;

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  /* Labels passed as TEXT CHILDREN of h() become text nodes, so an HTML
     entity in one would be drawn literally ('&plusmn;2&sigma;'), unlike the
     .tag divs below, which are set through innerHTML.  Text-child labels
     therefore use literal glyphs; the UI drive found the three that did not. */
  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  /* every chip row carries a data-key: six of them are labelled 1..4 and a
     match-by-word finder would drive the wrong one (lenses Known-bad) */
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips','data-key':key});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(c.disabled) return;
        st[key]=o.id; if(onPick) onPick(o);
        syncChips(); syncPanel(); refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); refresh(); }},lab2); }

  /* ---- the kicks (PhET's Median screen) ---- */
  const gK=h('div',{class:'grp'},h('h3',null,'the kicks'));
  gK.appendChild(h('div',{class:'tag'},'kicker (PhET’s four jerseys):'));
  gK.appendChild(chipRow(KICK_LIST,'mKick'));
  gK.appendChild(h('div',{class:'tag'},'max kicks (PhET caps this screen at 15):'));
  gK.appendChild(chipRow(MAXK_MED_LIST,'mMax'));
  gK.appendChild(h('div',{class:'tag'},'plot type (PhET’s preference):'));
  gK.appendChild(chipRow(PLOT_LIST,'mPlot'));
  gK.appendChild(h('div',{class:'checks'},checkbox('mMedian','median'),
    checkbox('mSort','sort data'),checkbox('mPredict','predict median')));
  gK.appendChild(slider('mPredVal','your median guess',CAV.VMIN,CAV.VMAX,CAV.MEDIAN_SNAP,v=>fmt(v,1)+' m'));
  const kTag=h('div',{class:'tag'}); gK.appendChild(kTag);

  /* ---- mean and median ---- */
  const gA=h('div',{class:'grp'},h('h3',null,'mean and median'));
  gA.appendChild(h('div',{class:'tag'},'kicker:'));
  gA.appendChild(chipRow(KICK_LIST,'aKick'));
  gA.appendChild(h('div',{class:'tag'},'max kicks:'));
  gA.appendChild(chipRow(MAXK_LIST,'aMax'));
  gA.appendChild(h('div',{class:'tag'},'plot type:'));
  gA.appendChild(chipRow(PLOT_LIST,'aPlot'));
  gA.appendChild(h('div',{class:'checks'},checkbox('aMean','mean (the fulcrum)'),
    checkbox('aMedian','median'),checkbox('aPredMean','predict mean'),
    checkbox('aPredMed','predict median')));
  gA.appendChild(slider('aPredMeanVal','your mean guess',CAV.VMIN,CAV.VMAX,0.01,v=>fmt(v,2)+' m'));
  gA.appendChild(slider('aPredMedVal','your median guess',CAV.VMIN,CAV.VMAX,CAV.MEDIAN_SNAP,v=>fmt(v,1)+' m'));
  const aTag=h('div',{class:'tag'}); gA.appendChild(aTag);

  /* ---- the spread ---- */
  const gV=h('div',{class:'grp'},h('h3',null,'the spread'));
  gV.appendChild(h('div',{class:'tag'},'kicker (each keeps its own field, as PhET does):'));
  gV.appendChild(chipRow(KICK_LIST,'vKick'));
  gV.appendChild(h('div',{class:'tag'},'max kicks:'));
  gV.appendChild(chipRow(MAXK_LIST,'vMax'));
  gV.appendChild(h('div',{class:'tag'},'measure:'));
  gV.appendChild(chipRow(MEASURES,'vMeasure'));
  gV.appendChild(h('div',{class:'checks'},checkbox('vShow','show the measure'),
    checkbox('vMean','mean'),checkbox('vOutliers','outliers'),
    checkbox('vInterval','interval tool'),checkbox('vPointer','pointer')));
  gV.appendChild(slider('vH1','interval from',CAV.DRAG_LO,CAV.DRAG_HI,0.1,v=>fmt(v,1)+' m'));
  gV.appendChild(slider('vH2','interval to',CAV.DRAG_LO,CAV.DRAG_HI,0.1,v=>fmt(v,1)+' m'));
  gV.appendChild(slider('vPtr','pointer at',CAV.DRAG_LO,CAV.DRAG_HI,0.1,v=>fmt(v,1)+' m'));
  const vTag=h('div',{class:'tag'}); gV.appendChild(vTag);

  /* ---- which quartile ---- */
  const gC=h('div',{class:'grp'},h('h3',null,'which quartile'));
  gC.appendChild(h('div',{class:'tag'},'kicker:'));
  gC.appendChild(chipRow(KICK_LIST,'cKick'));
  gC.appendChild(slider('cN','kicks in the data set',CAV.MIN_KICKS_IQR,30,1,v=>fmt(v,0)));
  const cTag=h('div',{class:'tag'}); gC.appendChild(cTag);

  /* ---- the balance point ---- */
  const gB=h('div',{class:'grp'},h('h3',null,'the balance point'));
  gB.appendChild(h('div',{class:'tag'},'kicker:'));
  gB.appendChild(chipRow(KICK_LIST,'bKick'));
  gB.appendChild(slider('bN','kicks in the data set',CAV.MIN_KICKS_IQR,25,1,v=>fmt(v,0)));
  gB.appendChild(slider('bMove','the last ball',CAV.VMIN,CAV.VMAX,1,v=>fmt(v,0)+' m'));
  gB.appendChild(h('div',{class:'checks'},checkbox('bLoss','the two loss curves')));
  const bTag=h('div',{class:'tag'}); gB.appendChild(bTag);

  /* ---- the long run ---- */
  const gL=h('div',{class:'grp'},h('h3',null,'the long run'));
  gL.appendChild(h('div',{class:'tag'},'kicker:'));
  gL.appendChild(chipRow(KICK_LIST,'lKick'));
  gL.appendChild(h('div',{class:'tag'},'kicks drawn:'));
  gL.appendChild(chipRow(LONG_LIST,'lN'));
  gL.appendChild(h('div',{class:'checks'},checkbox('lBands','the ±2σ/√n band')));
  const lTag=h('div',{class:'tag'}); gL.appendChild(lTag);

  /* ---- kicking ---- */
  const gFire=h('div',{class:'grp'},h('h3',null,'kicking'));
  gFire.appendChild(h('div',{class:'btnrow'},
    button('kick 1',()=>{ S.kick(1); }),
    button('kick 5',()=>{ S.kick(5); }),
    button('fill',()=>{ const F=curField(st); if(F) cavFieldBatch(F,F.max); })));
  gFire.appendChild(h('div',{class:'btnrow'},
    button('clear',()=>{ const F=curField(st); if(F) cavFieldClear(F); }),
    button('reset this view',()=>{ resetView(); })));
  gFire.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const fTag=h('div',{class:'tag'}); gFire.appendChild(fTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Center and Variability (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s conventions and constants (PHYSICAL_RANGE 1&ndash;15 m, VARIABILITY_DRAG_RANGE 0&ndash;16, MAX_KICKS_VALUES 5&ndash;30 with the Median screen capped at 15, the even-count median, the exclusive median-of-halves quartiles with their five-kick floor, the MAD rounded to a tenth three times over, the 0.5 m predict-median snap and the four kickers&rsquo; weight arrays) are read from its published build and cited as PhET&rsquo;s values. '
      +'Everything else is derived and pinned in selfTest to build/center-and-variability/derive.py, whose printed output is refvals.txt: every statistic against numpy on twenty-seven data sets including the degenerate ones, the quartile-convention equivalence on four thousand more, a chi-square of the sampler against the weights on a million draws each, and Monte-Carlo sampling laws.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the mathematics'),h('div',{id:'phys'}));
  [gK,gA,gV,gC,gB,gL,gFire,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetView(){
    const v=st.view;
    for(const k in DEFAULTS) if(k!=='view') st[k]=DEFAULTS[k];
    st.view=v; resetWorlds();
  }
  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const v=st.view;
    gK.hidden=(v!=='kicks');
    gA.hidden=(v!=='meanmed');
    gV.hidden=(v!=='spread');
    gC.hidden=(v!=='conv');
    gB.hidden=(v!=='balance');
    gL.hidden=(v!=='longrun');
    gFire.hidden=!(v==='kicks'||v==='meanmed'||v==='spread');
    /* a control that is live but ignored is worse than no control: the
       prediction sliders only exist while their checkbox is on, and the
       interval/pointer sliders only while their tool is out */
    if(rows.mPredVal) rows.mPredVal.row.hidden=!st.mPredict;
    if(rows.aPredMeanVal) rows.aPredMeanVal.row.hidden=!st.aPredMean;
    if(rows.aPredMedVal) rows.aPredMedVal.row.hidden=!st.aPredMed;
    if(rows.vH1) rows.vH1.row.hidden=!st.vInterval;
    if(rows.vH2) rows.vH2.row.hidden=!st.vInterval;
    if(rows.vPtr) rows.vPtr.row.hidden=!st.vPointer;
    for(const k in rows) rows[k].sync();
    const M0=buildModel();
    kTag.innerHTML='Balls land on whole metres and stack; drag one along the line to move it. PhET&rsquo;s Median screen offers 5, 10 or 15 kicks only.';
    aTag.innerHTML='The predict-median thumb snaps to half a metre and the predict-mean thumb does not &mdash; PhET&rsquo;s roundToInterval settings, 0.5 and null.';
    vTag.innerHTML='Quartiles need five kicks (&ldquo;Need at least five kicks&rdquo;); below that PhET reports IQR = ? and so does this.';
    cTag.innerHTML='At odd n PhET&rsquo;s rule IS Weibull; at even n it is Hazen, and Tukey&rsquo;s hinges join it there. It is never numpy&rsquo;s default on purpose.';
    bTag.innerHTML='Slope of the mean against the moved ball: exactly 1/n = '+fmt(1/Math.max(1,M0.stat.n),4)+' m per metre.';
    lTag.innerHTML='&sigma; = '+fmt(M0.pop.sd,4)+' m for this kicker, so &sigma;/&radic;n = '+fmt(M0.pop.sd/Math.sqrt(st.lN),4)+' m at '+st.lN+' kicks.';
    const F=curField(st);
    fTag.innerHTML=(F&&F.xs.length+F.air.length>=F.max)
      ?'the field is full ('+F.max+' kicks)'
      :'<b>space</b> kicks &middot; <b>k</b> kicks five &middot; <b>c</b> clears &middot; <b>p</b> pauses &middot; 1&ndash;6 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='kicks'||st.view==='meanmed'||st.view==='spread')
        ?'drag a ball along the line to move it · space kicks · 1–6 switch views'
        :(st.view==='balance'?'drag the magenta ball · 1–6 switch views'
                             :'1–6 switch views');
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncChips(); syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); S.kick(1); syncPanel(); refresh(); }
    else if(e.key==='k'){ S.kick(5); syncPanel(); refresh(); }
    else if(e.key==='p'){ st.running=!st.running; syncPanel(); refresh(); }
    else if(e.key==='c'){ const F=curField(st); if(F) cavFieldClear(F); syncPanel(); refresh(); }
    else if(e.key==='r'){ resetView(); syncChips(); syncPanel(); refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); refresh(); });

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
  kicks:'PhET&rsquo;s Median screen. A kicker sends balls down a field and each landing is recorded as a mark on a number line &mdash; which is all a dot plot is. Every distance is a whole metre between 1 and 15, so ties are the rule rather than the exception, and that is exactly where the median has to make a decision: with an even count there is no single middle value, so PhET takes the mean of the two middle ones and the median can land on a half metre that nothing was kicked to. Turn on <b>sort data</b> to see the cards in order with the middle one (or two) picked out in gold, and drag any ball along the line &mdash; it snaps to a whole metre, as PhET&rsquo;s does, and you can watch the median refuse to move until a ball crosses the middle.',
  meanmed:'PhET&rsquo;s Mean &amp; Median screen, with the mean drawn as what the word &ldquo;average&rdquo; hides: a balance point. The bars under the line are the signed deviations x<sub>i</sub> &minus; x&#772;, one per kick, and they cancel exactly &mdash; not nearly, exactly, because &Sigma;(x<sub>i</sub> &minus; x&#772;) = &Sigma;x<sub>i</sub> &minus; n&#183;(&Sigma;x<sub>i</sub>/n) is zero as algebra. The readout prints the sum to twelve decimals so you can see it is machine zero and not rounding. Then move one ball out to 15 m: the mean slides after it, by exactly one fifteenth of a metre per metre with fifteen kicks, while the median stays where it is. That is the whole difference between the two, and it is why an average income and a typical income are different questions.',
  spread:'PhET&rsquo;s Variability screen. Three measures, and the point of the screen is that they disagree about which kicker is most spread out. The <b>range</b> is made of two kicks and forgets the other thirteen, so one wild ball doubles it. The <b>IQR</b> is the width of the middle half &mdash; Q1 and Q3 by PhET&rsquo;s exclusive median-of-halves rule, which needs at least five kicks before it will say anything &mdash; and it does not move at all when an extreme ball moves further out; the box-and-whisker makes that visible, with anything beyond 1.5 &times; IQR marked as an outlier rather than swallowed by a whisker. The <b>MAD</b> counts every kick at its own distance from the mean, so it is between the two in robustness. The interval tool counts what lies between its handles, both ends included.',
  conv:'Quartiles are not one thing. Ask six pieces of software for Q1 and you can get six answers, because a quartile of a finite sample has to interpolate between order statistics and there is no agreement about how. PhET uses the exclusive median-of-halves rule: split the sorted data in half, throw the overall median away if the count is odd, and take the median of each half. Written as an order statistic that is h = (n+1)/4 when n is odd and h = n/4 + &frac12; when n is even &mdash; Hyndman &amp; Fan types 6 and 5, the Weibull and Hazen rules. derive.py proves that identity and checks it on four thousand data sets, including heavy-tie ones where conventions are most likely to coincide by accident. The right panel counts how often the rules actually differ, and the answer is: most of the time.',
  balance:'Two sentences that sound like definitions are really optimisation problems. The mean is the number that minimises &Sigma;(x<sub>i</sub> &minus; c)&sup2;, and the parallel-axis identity &Sigma;(x<sub>i</sub> &minus; c)&sup2; = &Sigma;(x<sub>i</sub> &minus; x&#772;)&sup2; + n(x&#772; &minus; c)&sup2; makes that exact: the second term is a parabola with its vertex at the mean and nothing else depends on c. The median is a number that minimises &Sigma;|x<sub>i</sub> &minus; c|, and because the absolute value has a corner the minimum can be a whole interval, which is why an even count leaves the median a choice. The right panel drags the last ball from one end of the field to the other: the mean is a straight line of slope 1/n and the median is a staircase that goes flat as soon as the ball is out of the middle. Robustness is that flatness.',
  longrun:'PhET&rsquo;s kickers are not mysteries: each one is a list of fifteen weights, and the sampler picks distance i with probability w<sub>i</sub>/&Sigma;w exactly. So the population mean, median, standard deviation and mean absolute deviation are sums over fifteen numbers, computed here rather than estimated, and the sample can be judged against them. The bars are what this page actually drew; the orange marks are the weights. The running mean is held to &plusmn;2&sigma;/&radic;n, a tolerance that comes from the sampling law and not from taste. One warning the picture carries: the sample MAD does not simply creep up to the population MAD. Because E|X &minus; c| has a kink wherever the distribution has an atom, a kicker whose mean lands on a whole metre (kickers 1 and 2, both centred on 8 m) is biased the other way &mdash; measured in derive.py, not assumed.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  kicks:'<h4>the median, and its even-count convention</h4>'
    +EQ(1,'x<sub>(1)</sub> &le; &hellip; &le; x<sub>(n)</sub>, &nbsp; median = x<sub>(k+1)</sub> <span class="rm">for n = 2k+1</span>')
    +EQ(2,'median = '+FR('x<sub>(k)</sub> + x<sub>(k+1)</sub>','2')+' <span class="rm">for n = 2k &mdash; PhET&rsquo;s rule, and the reason a median can be a half metre</span>')
    +EQ(3,'<span class="rm">a kicked distance:</span> P(x = i) = '+FR('w<sub>i</sub>','&Sigma;w')+', &nbsp; i = 1&hellip;15 <span class="rm">(exactly, from PhET&rsquo;s sampler)</span>')
    +'<p>[3] is not an approximation of the sampler &mdash; it is what the sampler does. The returned index is the first whose cumulative weight reaches S&#183;u with u uniform, so the probability of index i is w<sub>i</sub>/S.</p>'
    +'<div class="cite">pins: the median against numpy on 27 data sets including n = 1, all-equal, two-value and heavy-tie; the kicks bit-identical to the Python twin &mdash; derive.py</div>',
  meanmed:'<h4>the balance point</h4>'
    +EQ(1,'x&#772; = '+FR('1','n')+' &Sigma; x<sub>i</sub> &nbsp;&hArr;&nbsp; &Sigma;(x<sub>i</sub> &minus; x&#772;) = 0')
    +EQ(2,'<span class="rm">moving one ball by &delta;:</span> &Delta;x&#772; = '+FR('&delta;','n')+', &nbsp; &Delta;median = 0 <span class="rm">unless the ball crosses the middle</span>')
    +EQ(3,'<span class="rm">PhET&rsquo;s prediction thumbs:</span> median snaps to 0.5 m, mean does not <span class="rm">(roundToInterval 0.5 and null)</span>')
    +'<p>[1] is an identity, not a fit. The readout prints the left-hand side to twelve decimals; the sim asserts it is below 1e&minus;12 over every pinned data set, and the integer statement n&#183;&Sigma;x &minus; n&#183;&Sigma;x = 0 behind it is exact.</p>'
    +'<div class="cite">pins: &Sigma;(x<sub>i</sub> &minus; x&#772;) on 27 data sets; the 1/n influence slope at every one of the fifteen positions &mdash; derive.py</div>',
  spread:'<h4>three measures, one data set</h4>'
    +EQ(1,'range = x<sub>(n)</sub> &minus; x<sub>(1)</sub>, &nbsp; IQR = Q3 &minus; Q1, &nbsp; MAD = '+FR('1','n')+' &Sigma;|x<sub>i</sub> &minus; x&#772;|')
    +EQ(2,'<span class="rm">fences:</span> Q1 &minus; 1.5&#183;IQR, &nbsp; Q3 + 1.5&#183;IQR <span class="rm">&mdash; the whiskers stop at the furthest kick inside them</span>')
    +EQ(3,'<span class="rm">PhET prints</span> round<sub>0.1</sub>( round<sub>0.1</sub>(&Sigma; round<sub>0.1</sub>|x<sub>i</sub> &minus; x&#772;|) / n )')
    +'<p>[3] is three roundings, so PhET&rsquo;s displayed MAD can sit up to 0.1 + 0.05/n from the exact value &mdash; a ceiling that is derived rather than guessed, and reached (0.1 m) somewhere in eight thousand random data sets. The readout prints both.</p>'
    +'<div class="cite">pins: range, IQR and both MADs against numpy; the box plot&rsquo;s fences, whiskers and outliers on six data sets &mdash; derive.py</div>',
  conv:'<h4>which quartile</h4>'
    +EQ(1,'<span class="rm">PhET:</span> lower = x<sub>(1..&lfloor;n/2&rfloor;)</span>, &nbsp; upper = x<sub>(n&minus;&lfloor;n/2&rfloor;+1..n)</sub>, &nbsp; Q1 = med(lower), Q3 = med(upper)')
    +EQ(2,'&rArr; h<sub>Q1</sub> = '+FR('n+1','4')+' <span class="rm">n odd (Weibull, H&amp;F 6)</span>, &nbsp; '+FR('n','4')+' + &frac12; <span class="rm">n even (Hazen, H&amp;F 5)</span>')
    +EQ(3,'Q<sub>p</sub> = x<sub>(&lfloor;h&rfloor;)</sub> + (h &minus; &lfloor;h&rfloor;)&#183;(x<sub>(&lceil;h&rceil;)</sub> &minus; x<sub>(&lfloor;h&rfloor;)</sub>)')
    +'<p>[2] is proved by counting positions in each half and checked on four thousand data sets. At even n the exclusive and inclusive splits are the same split, so Tukey&rsquo;s hinges join in; at odd n they part. Neither matches numpy&rsquo;s default at any n.</p>'
    +'<div class="cite">pins: the equivalence at every n from 5 to 30, on uniform, heavy-tie and narrow data; the six conventions on two demonstration sets &mdash; derive.py</div>',
  balance:'<h4>each estimator is a minimiser</h4>'
    +EQ(1,'&Sigma;(x<sub>i</sub> &minus; c)&sup2; = &Sigma;(x<sub>i</sub> &minus; x&#772;)&sup2; + n(x&#772; &minus; c)&sup2; &nbsp;&rArr;&nbsp; <span class="rm">least at c = x&#772;, uniquely</span>')
    +EQ(2,FR('d','dc')+' &Sigma;|x<sub>i</sub> &minus; c| = #{x<sub>i</sub> &lt; c} &minus; #{x<sub>i</sub> &gt; c} &nbsp;&rArr;&nbsp; <span class="rm">zero on the median interval</span>')
    +EQ(3,'<span class="rm">influence of one ball:</span> '+FR('&part;x&#772;','&part;x<sub>n</sub>')+' = '+FR('1','n')+' <span class="rm">everywhere</span>, &nbsp; '+FR('&part;median','&part;x<sub>n</sub>')+' = 0 <span class="rm">outside the middle</span>')
    +'<p>[2] is why an even count leaves the median an interval to choose from and PhET takes its midpoint. [3] is what &ldquo;robust&rdquo; means, drawn rather than asserted.</p>'
    +'<div class="cite">pins: the parallel-axis identity at four offsets; the grid minimum of each loss; the influence table at all fifteen positions &mdash; derive.py</div>',
  longrun:'<h4>the kicker, exactly</h4>'
    +EQ(1,'&mu; = &Sigma; p<sub>i</sub> x<sub>i</sub>, &nbsp; &sigma;&sup2; = &Sigma; p<sub>i</sub>(x<sub>i</sub> &minus; &mu;)&sup2;, &nbsp; MAD<sub>pop</sub> = &Sigma; p<sub>i</sub>|x<sub>i</sub> &minus; &mu;| &nbsp; <span class="rm">p<sub>i</sub> = w<sub>i</sub>/&Sigma;w</span>')
    +EQ(2,'sd(x&#772;<sub>n</sub>) = '+FR('&sigma;','&radic;n')+' <span class="rm">exactly</span>, &nbsp; count<sub>i</sub> ~ Binomial(n, p<sub>i</sub>) <span class="rm">&mdash; the bars&rsquo; own error bars</span>')
    +EQ(3,'g(c) = E|X &minus; c| <span class="rm">is convex with</span> g&prime;(c) = 2F(c) &minus; 1 <span class="rm">&mdash; a KINK wherever there is an atom</span>')
    +'<p>[3] is the reason the sample MAD is biased up for kickers 1 and 2, whose mean is exactly 8 m, and down for kickers 3 and 4, whose means are 5.044 and 10.956 m. The sign was measured over 20000 Monte-Carlo samples at each of n = 5, 10, 15, 30; an earlier draft of derive.py asserted &ldquo;biased down at every n&rdquo; and was wrong.</p>'
    +'<div class="cite">pins: a chi-square of the sampler against each weight array on 10&#8310; draws; every bin within 4 binomial sd at n = 5000; &sigma;/&radic;n against 20000 Monte-Carlo samples &mdash; derive.py</div>'
};
