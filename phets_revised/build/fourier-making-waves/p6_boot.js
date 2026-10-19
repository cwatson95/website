
/* ================================================================== *
 *  boot — the control panel, the tabs, the handlers, the frame loop   *
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
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{
    tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2));
  });

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
  /* the amplitude row edits ampArray()[sel-1], not a key of ST, so it needs
     its own read-back: the preset chips and the canvas drag both move it */
  function ampRow(){
    const inp=h('input',{type:'range',min:-AMAX,max:AMAX,step:A_STEP,value:0});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,'amplitude A'),inp,val);
    const sync=()=>{ const stp=st.view==='game'?G_STEP:A_STEP;
      inp.setAttribute('step',stp); inp.value=ampArray()[st.sel-1];
      val.textContent=fmt(ampArray()[st.sel-1],2); };
    inp.addEventListener('input',()=>{ const stp=st.view==='game'?G_STEP:A_STEP;
      ampArray()[st.sel-1]=snapAmp(parseFloat(inp.value),stp);
      if(st.view!=='game') st.preset='custom';
      syncChips(); syncPanel(); dirty=true; refresh(); });
    rows.amp={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  /* a chip row REGISTERS ITSELF, so syncChips never has to find it again by
     matching label text: the DOM stub does not decode entities in innerHTML
     and a real browser does, so a text match would silently miss the rows
     whose labels carry a Greek letter (Known-bad: the drum_head harness). */
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),html:o.name,onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        syncChips(); syncPanel(); dirty=true; refresh(); }}));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},label); }

  /* ---- the waveform ---- */
  const gWave=h('div',{class:'grp'},h('h3',null,'the waveform'));
  const preChips=chipRow(PRESETS,'preset',(o,was)=>{
    if(o.id==='sawtooth'&&st.series==='cos') st.series='sin';    /* PhET: a sawtooth cannot be made of cosines */
    if(o.id!=='custom') applyPreset();
  });
  gWave.appendChild(preChips);
  const serChips=chipRow(SERIES_LIST,'series',()=>{
    if(st.preset==='sawtooth'&&st.series==='cos') st.series='sin';
    applyPreset();
  });
  gWave.appendChild(serChips);
  const domChips=chipRow(DOMAINS,'domain'); gWave.appendChild(domChips);
  gWave.appendChild(slider('N','harmonics kept',1,NMAX,1,v=>String(v)+' of '+NMAX,()=>{ if(st.preset!=='custom') applyPreset(); }));
  const convRow=slider('convM','terms kept M',1,128,1,v=>String(v));
  gWave.appendChild(convRow);
  const convChips=chipRow(PRESETS.filter(p=>hasIdeal(p.id)),'convPre');
  gWave.appendChild(convChips);
  const waveTag=h('div',{class:'tag'}); gWave.appendChild(waveTag);

  /* ---- one harmonic ---- */
  const gHarm=h('div',{class:'grp'},h('h3',null,'one harmonic'));
  gHarm.appendChild(slider('sel','harmonic n',1,NMAX,1,v=>String(v)));
  gHarm.appendChild(ampRow());
  const harmBtns=h('div',{class:'btnrow'},
    btn('zero them all',()=>{ setCurrent(new Array(NMAX).fill(0)); if(st.view!=='game') st.preset='custom'; }),
    btn('back to the preset',()=>{ if(st.preset==='custom') st.preset='square'; applyPreset(); }));
  gHarm.appendChild(harmBtns);
  const harmTag=h('div',{class:'tag'}); gHarm.appendChild(harmTag);

  /* ---- what to show ---- */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},
    checkbox('showHarm','the harmonics one by one'),
    checkbox('showInf','the infinite-harmonics waveform'),
    checkbox('caliper','the wavelength caliper')));
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  /* ---- time ---- */
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gTime.appendChild(h('div',{class:'btnrow'},
    btn('step',()=>S.stepOnce()),
    btn('t = 0',()=>{ st.t=0; }),
    btn('reset all',()=>{ resetAll(); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  /* ---- the game ---- */
  const gGame=h('div',{class:'grp'},h('h3',null,'the game'));
  const LEVELS=[]; for(let i=1;i<=N_LEVELS;i++) LEVELS.push({id:i,name:'level '+i});
  const lvlChips=chipRow(LEVELS,'level',o=>{ GAME.level=o.id; GAME.reset(); });
  gGame.appendChild(lvlChips);
  const gameBtns=h('div',{class:'btnrow'},
    btn('new waveform',()=>GAME.fresh()),
    btn('check answer',()=>{ GAME.check(); }),
    btn('show answer',()=>GAME.show()));
  gGame.appendChild(gameBtns);
  gGame.appendChild(h('div',{class:'btnrow'},btn('erase my amplitudes',()=>{ setGuess(new Array(NMAX).fill(0)); })));
  const gameTag=h('div',{class:'tag'}); gGame.appendChild(gameTag);

  /* ---- the packet ---- */
  const gPack=h('div',{class:'grp'},h('h3',null,'the packet'));
  gPack.appendChild(slider('wpK0','centre k0',WP_K0_MIN,WP_K0_MAX,0.01,v=>sigf(v/PI,3)+' π'));
  gPack.appendChild(slider('wpSk','width sigma_k',WP_SK_MIN,WP_SK_MAX,0.01,v=>sigf(v/PI,3)+' π'));
  const spList=[{id:0,name:'0 (continuous)'},{id:1,name:'&pi;/4'},{id:2,name:'&pi;/2'},{id:3,name:'&pi;'}];
  const spChips=chipRow(spList,'wpSp'); gPack.appendChild(spChips);
  const wdChips=chipRow(WPDOM_LIST,'wpDom'); gPack.appendChild(wdChips);
  const packChecks=h('div',{class:'checks'},checkbox('wpEnv','the envelope'),checkbox('wpWid','the width markers'));
  gPack.appendChild(packChecks);
  gPack.appendChild(slider('pairK1','spacing k1',PAIR_K1_MIN,PAIR_K1_MAX,0.01,v=>sigf(v,3)+' rad/m'));
  gPack.appendChild(slider('pairSk','packet width sigma_k',WP_SK_MIN,WP_SK_MAX,0.01,v=>sigf(v/PI,3)+' π'));
  const packTag=h('div',{class:'tag'}); gPack.appendChild(packTag);

  /* ---- prose ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Fourier: Making Waves (University of Colorado '
      +'Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values (11 harmonics, '
      +'amplitudes to &plusmn;1.5 in steps of 0.05 and 0.1, five game levels, f<sub>1</sub> = 440 Hz, L = 1 m, '
      +'T = 1000/440 ms, the wave-packet screen&rsquo;s k range 0&ndash;24&pi;, centre 9&pi;&ndash;15&pi;, width '
      +'&pi;&ndash;4&pi; and spacings 0, &pi;/4, &pi;/2, &pi;) are read out of its build 1.1.5 by '
      +'build/fourier-making-waves/derive.py. Everything else is mathematics, re-derived there with numpy and scipy '
      +'(quadrature against the waveforms themselves, scipy.special.sici, numpy.fft) and pinned in selfTest.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the mathematics'),h('div',{id:'phys'}));
  [gWave,gHarm,gShow,gTime,gGame,gPack,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row the view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view, disc=(v==='harm'||v==='spec');
    gWave.hidden=!(disc||v==='conv');
    preChips.hidden=!disc;
    serChips.hidden=!(disc||v==='conv');
    domChips.hidden=!disc;
    rows.N.row.hidden=!disc;
    convRow.hidden=(v!=='conv');
    convChips.hidden=(v!=='conv');
    gHarm.hidden=!(disc||v==='game');
    harmBtns.hidden=(v==='game');
    gShow.hidden=(v!=='harm');
    gTime.hidden=(v!=='harm');
    rows.cb_running.row.hidden=(st.domain!=='both');
    gGame.hidden=(v!=='game');
    gPack.hidden=!(v==='pack'||v==='pair');
    rows.wpK0.row.hidden=false;
    rows.wpSk.row.hidden=(v!=='pack');
    spChips.hidden=(v!=='pack');
    wdChips.hidden=(v!=='pack');
    packChecks.hidden=(v!=='pack');
    rows.pairK1.row.hidden=(v!=='pair');
    rows.pairSk.row.hidden=(v!=='pair');
    for(const k in rows) rows[k].sync();
    waveTag.innerHTML=v==='conv'
      ? 'the series is the exact one for this waveform; M is how many of its terms are kept'
      : 'choosing a waveform fills the eleven amplitudes from its closed form; moving one by hand makes it <b>custom</b>'
        +(st.preset==='sawtooth'?' &nbsp; a sawtooth is odd, so it cannot be built out of cosines':'');
    harmTag.innerHTML=v==='game'
      ? 'drag a bar on the canvas, or pick n here and set A &mdash; steps of '+fmt(G_STEP,1)+', as in PhET'
      : 'drag a bar on the canvas, or pick n here and set A &mdash; steps of '+fmt(A_STEP,2)+', as in PhET'
        +' &nbsp; &uarr; &darr; nudge it';
    showTag.innerHTML='the caliper is '+(st.domain==='time'?'T/n':'&lambda;<sub>n</sub> = L/n')+' wide for the harmonic n above; drag it along the sum';
    timeTag.innerHTML=st.domain==='both'
      ? 'PhET runs t at 1 ms of model time per second; its step button adds 0.05 ms &nbsp; <b>space</b> runs/pauses, <b>.</b> steps'
      : 't only matters in the space &amp; time domain &mdash; the other two are snapshots';
    gameTag.innerHTML='PhET&rsquo;s levels: 1 to 4 use that many harmonics, level 5 uses five or more of the eleven. '
      +'A guess counts only when every amplitude matches <b>exactly</b>.';
    packTag.innerHTML=v==='pack'
      ? 'PhET&rsquo;s four spacings, and 0 for the continuous limit; the packet repeats every 2&pi;/k<sub>1</sub>'
      : 'this view&rsquo;s spacing slider is not PhET&rsquo;s: it runs continuously so the repeats can be watched leaving';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='harm'||st.view==='game'||st.view==='spec')
        ? 'drag the amplitude bars · 1–6 switch views'
        : '1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); refresh(); }
    else if(S.drag) canvas.classList.add('dragging');
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='.'){ S.stepOnce(); dirty=true; refresh(); }
    else if(e.key==='r'){ resetAll(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='ArrowUp'||e.key==='ArrowDown'){
      e.preventDefault();
      const stp=st.view==='game'?G_STEP:A_STEP;
      ampArray()[st.sel-1]=snapAmp(ampArray()[st.sel-1]+(e.key==='ArrowUp'?stp:-stp),stp);
      if(st.view!=='game') st.preset='custom';
      syncChips(); syncPanel(); dirty=true; refresh();
    }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0, last=0;
  function frameLoop(tm){
    frameN++;
    const dtw=last?Math.min((tm-last)/1000,0.05):0; last=tm;
    const advanced=S.step(dtw);
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  applyPreset(); GAME.reset();
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  harm:'This is PhET&rsquo;s Discrete screen. Eleven sine waves, with wavelengths L, L/2, L/3 and so on down to L/11, '
    +'and nothing else: set their eleven amplitudes and the bottom panel is their sum. What is surprising is how far '
    +'that gets you. A square wave, a triangle, a sawtooth &mdash; all of them are sums of these same eleven curves '
    +'plus the ones beyond, and the amplitudes are not fitted, they are <b>calculated</b>: 4/&pi;n for the odd '
    +'harmonics of a square wave, 8/&pi;&sup2;n&sup2; for a triangle, 2/&pi;n alternating for a sawtooth. Press a '
    +'preset and watch the bars jump to those values. The switch from sines to cosines is a switch of symmetry: an '
    +'odd function needs sines, an even one needs cosines, and a sawtooth &mdash; odd about every point where it does '
    +'not jump &mdash; cannot be made of cosines at all, which is why PhET refuses that combination. The domain '
    +'switch changes only what the horizontal axis means. In <b>space</b> the sum is a photograph of a string; in '
    +'<b>time</b> it is what one point of that string does; in <b>space &amp; time</b> the whole pattern slides right '
    +'at one wavelength per period.',
  conv:'Keep the first M terms of a series and you get a curve that is close to the waveform &mdash; but how close, '
    +'and where does it fail? Everywhere the waveform is smooth, adding terms helps: the distance from it, measured '
    +'as an rms over a period, falls without limit, and the bottom-right panel is that fall on log axes. At a '
    +'<b>jump</b>, something else happens. The partial sum overshoots, and the overshoot does not shrink. Its height '
    +'tends to a fixed fraction of the jump, 8.949 %, discovered by Wilbraham in 1848 and rediscovered by Gibbs fifty '
    +'years later. What does shrink is the width of the ear: the first peak sits at u = &pi;/2M, so it slides in '
    +'towards the jump as M grows while keeping the same height. That is how both statements can be true at once &mdash; '
    +'the series converges in the mean, and fails to converge uniformly. Switch to the triangle to see the contrast: '
    +'it is continuous, so there is no jump, no ringing, and the partial sums never leave the waveform.',
  spec:'Two questions, one answer. First: where does the power in a waveform live? Parseval&rsquo;s theorem says it '
    +'is simply shared out among the harmonics &mdash; the mean of F&sup2; over a period equals &frac12;&Sigma;A<sub>n</sub>&sup2;, '
    +'with no cross terms at all, because sin nu and sin mu are orthogonal for n &ne; m. The readout computes it both '
    +'ways, once by summing squares of amplitudes and once by squaring the waveform and averaging 256 samples, and '
    +'they agree to the last digit a double can hold. Second: can you go backwards, from a waveform to its '
    +'amplitudes? Yes, and by the same orthogonality: multiply by sin nu, average, double. That is the discrete '
    +'Fourier transform, and the magenta rings on the bars are what it returns, computed by a radix-2 FFT and checked '
    +'against the direct sum it is a fast version of. Analysis and synthesis are inverse to each other, exactly.',
  game:'PhET&rsquo;s Wave Game. A waveform is drawn in magenta, built from some of the eleven harmonics with '
    +'amplitudes you cannot see; your job is to find them. Level 1 uses one harmonic, level 2 two, and level 5 uses '
    +'five or more. There is a real skill here, and it is not guessing: look at the period of the pattern to find '
    +'the lowest harmonic present, then at how sharp the corners are to judge how much of the high ones is in it. '
    +'Getting close is not the same as getting it right &mdash; PhET checks every one of the eleven amplitudes for an '
    +'exact match, and this file does the same. The readout shows two different measures of how wrong you are: the '
    +'worst single amplitude, and the rms difference between the two waveforms, which is Parseval applied to their '
    +'difference. A guess can look right and still be out by a harmonic whose amplitude is small.',
  pack:'PhET&rsquo;s Wave Packet screen, and the other half of Fourier&rsquo;s idea. So far every sum has been of '
    +'harmonics &mdash; whole-number multiples of one fundamental &mdash; and every sum has been periodic. Let the '
    +'spacing between components shrink and the sum stops repeating: it becomes a single pulse, a <b>wave packet</b>. '
    +'The amplitudes here are a Gaussian in k, centred on k<sub>0</sub> with standard deviation &sigma;<sub>k</sub>, and '
    +'the top panel is that Gaussian sampled at the component wave numbers. The bottom panel is their sum, and it is '
    +'a Gaussian too, of width &sigma;<sub>x</sub> = 1/&sigma;<sub>k</sub>. Widen the spectrum and the packet gets '
    +'shorter; narrow it and the packet stretches out. You cannot have both narrow, and the product of the two widths '
    +'is not merely bounded here &mdash; for a Gaussian it is exactly 1, which is why the Gaussian is the shape that '
    +'achieves the uncertainty bound.',
  pair:'A closer look at what the discrete sum really is. The obvious reading &mdash; that adding up components at '
    +'spacing k<sub>1</sub> <i>approximates</i> the integral over a continuous k &mdash; is not quite right, and the '
    +'exact statement is nicer. By Poisson&rsquo;s summation formula the sum over k<sub>n</sub> = n k<sub>1</sub> is '
    +'<b>exactly</b> the continuous packet, plus a copy of it at every multiple of &lambda;<sub>1</sub> = '
    +'2&pi;/k<sub>1</sub>. Nothing is lost and nothing is approximated; the copies are simply what a discrete spectrum '
    +'means. Widen the window to three metres and there they are, magenta ticks marking where they sit. Narrow the '
    +'spacing and they walk outward &mdash; in the limit k<sub>1</sub> &rarr; 0 they are infinitely far away and the '
    +'sum is the single packet. What is then left between the discrete and the continuous is only the Gaussian tail '
    +'that PhET&rsquo;s k range, 0 to 24&pi;, cuts off: about three parts in a hundred thousand, the orange floor in '
    +'the error plot.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  harm:'<h4>the series, and where the coefficients come from</h4>'
    +EQ(1,'F(u) = &Sigma;<sub>n=1</sub><sup>N</sup> A<sub>n</sub> sin(nu), &nbsp; u = 2&pi;x/L, &nbsp; 2&pi;t/T &nbsp;<span class="rm">or</span>&nbsp; 2&pi;(x/L &minus; t/T)')
    +EQ(2,'A<sub>n</sub> = '+FR('1','&pi;')+' &#8747;<sub>&minus;&pi;</sub><sup>&pi;</sup> f(u) sin(nu) du &nbsp;<span class="rm">(orthogonality)</span>')
    +EQ(3,'<span class="rm">square:</span> A<sub>n</sub> = 4/&pi;n <span class="rm">(n odd)</span>; &nbsp; <span class="rm">triangle:</span> (&minus;1)<sup>(n&minus;1)/2</sup> 8/&pi;&sup2;n&sup2;; &nbsp; <span class="rm">saw:</span> (&minus;1)<sup>n&minus;1</sup> 2/&pi;n')
    +EQ(4,'<span class="rm">wave packet:</span> A<sub>n</sub> = e<sup>&minus;(n&minus;c)&sup2;/2&sigma;&sup2;</sup>, &nbsp; c = (N+1)/2, &nbsp; &sigma; = N/5 &nbsp;<span class="rm">(PhET&rsquo;s table)</span>')
    +'<p>[3] is not quoted: derive.py puts sgn(sin u), (2/&pi;)asin(sin u) and u/&pi; through [2] with scipy quadrature '
    +'broken at every corner, and those closed forms come back to 2.5e&minus;13 &mdash; as do the coefficients of the '
    +'wrong parity, which come back <i>zero</i>. [4] is PhET&rsquo;s hard-coded table of 66 numbers; 65 of them are that '
    +'Gaussian to 5e&minus;7, PhET&rsquo;s own printed precision, and the odd one out (N = 10, n = 2 and its mirror) '
    +'reads 0.216255 where the Gaussian gives 0.216265.</p>'
    +'<div class="cite">pins: all five presets in both parities; the quadrature residual; PhET&rsquo;s table and its '
    +'one outlier; sums at chosen x and t &mdash; derive.py</div>',
  conv:'<h4>Gibbs, and the two kinds of convergence</h4>'
    +EQ(1,'S<sub>M</sub>&prime;(u) = '+FR('4','&pi;')+' &Sigma;<sub>m=1</sub><sup>M</sup> 2cos((2m&minus;1)u) = '+FR('4','&pi;')+' '+FR('sin 2Mu','sin u')+' &nbsp;&rArr;&nbsp; <span class="rm">first peak at</span> u = &pi;/2M')
    +EQ(2,'S<sub>M</sub>(&pi;/2M) = &Sigma;<sub>m</sub> '+FR('4','&pi;(2m&minus;1)')+' sin'+FR('(2m&minus;1)&pi;','2M')+' &rarr; '+FR('2','&pi;')+' &#8747;<sub>0</sub><sup>&pi;</sup> '+FR('sin v','v')+' dv')
    +EQ(3,'= '+FR('2','&pi;')+' Si(&pi;) = 1.1789797444721668 &nbsp;&rArr;&nbsp; <span class="rm">overshoot</span> = 0.0894899 &times; <span class="rm">the jump</span>')
    +EQ(4,'&#8214;f &minus; S<sub>M</sub>&#8214;&sup2; = &lang;f&sup2;&rang; &minus; &frac12;&Sigma;<sub>n&le;M</sub> A<sub>n</sub>&sup2; &rarr; 0 &nbsp;<span class="rm">(convergence in the mean)</span>')
    +'<p>[2] is a Riemann sum for [3] with step &pi;/2M, so the peak approaches the limit as O(1/M&sup2;) &mdash; measured '
    +'ratio 4.009 between M = 6, 12 and 24. [4] is exact and far better behaved than summing the tail: the square '
    +'wave&rsquo;s tail converges like 1/M, so a truncated tail sum at n = 60000 is still 1.8e&minus;5 short.</p>'
    +'<div class="cite">pins: the peak at M = 1, 2, 6, 50, 400 against a Brent-refined scan of a dense grid; the O(1/M&sup2;) '
    +'ratio; the rms errors; the triangle&rsquo;s peak staying below 1 &mdash; derive.py</div>',
  spec:'<h4>Parseval, and analysis</h4>'
    +EQ(1,'&lang;sin(nu) sin(mu)&rang; = &frac12;&delta;<sub>nm</sub>, &nbsp; &lang;cos(nu) cos(mu)&rang; = &frac12;&delta;<sub>nm</sub> &nbsp;<span class="rm">(n, m &ge; 1)</span>')
    +EQ(2,'&lang;F&sup2;&rang; = &Sigma;<sub>n,m</sub> A<sub>n</sub>A<sub>m</sub>&lang;&hellip;&rang; = &frac12; &Sigma;<sub>n</sub> A<sub>n</sub>&sup2;')
    +EQ(3,'A<sub>n</sub> = '+FR('2','N<sub>s</sub>')+' &Sigma;<sub>j=0</sub><sup>N<sub>s</sub>&minus;1</sup> F(2&pi;j/N<sub>s</sub>) sin(2&pi;nj/N<sub>s</sub>) &nbsp;<span class="rm">exact for</span> n &lt; N<sub>s</sub>/2')
    +EQ(4,'<span class="rm">radix-2 FFT:</span> A<sub>n</sub> = &minus;2 Im(&#8497;<sub>n</sub>)/N<sub>s</sub> &nbsp;<span class="rm">(sines)</span>, &nbsp; 2 Re(&#8497;<sub>n</sub>)/N<sub>s</sub> &nbsp;<span class="rm">(cosines)</span>')
    +'<p>[3] is a quadrature that is <i>exact</i>, not approximate: the trapezium rule on a periodic trigonometric '
    +'polynomial has no error at all once the grid resolves it, which is why the round trip closes to 1e&minus;15 and '
    +'not to some tolerance. The FFT of [4] is checked against [3] in JS and against numpy.fft in derive.py.</p>'
    +'<div class="cite">pins: Parseval for three presets and eight random amplitude sets in both parities; the round trip; '
    +'FFT versus direct DFT; the FFT refusing a length that is not a power of two &mdash; derive.py</div>',
  game:'<h4>the challenge, and how close counts</h4>'
    +EQ(1,'<span class="rm">level</span> &#8467; &le; 4: &#8467; <span class="rm">non-zero harmonics;</span> &nbsp; &#8467; = 5: <span class="rm">a random 5 to 11</span>')
    +EQ(2,'A<sub>n</sub> &#8712; {&plusmn;0.1, &plusmn;0.2, &hellip;, &plusmn;1.5} &nbsp;<span class="rm">(30 values, zero excluded)</span>')
    +EQ(3,'&#8214;guess &minus; answer&#8214; = &radic;(&frac12; &Sigma;<sub>n</sub> (A<sub>n</sub> &minus; A&#772;<sub>n</sub>)&sup2;) &nbsp;<span class="rm">(Parseval, on the difference)</span>')
    +'<p>[3] is why the rms number in the readout is honest but not the test: two amplitudes out by 0.1 each give the '
    +'same rms as one out by 0.14, and PhET scores neither. The challenge generator follows PhET&rsquo;s: choose the '
    +'slots at random, draw each amplitude uniformly in [&minus;1.5, 0), snap it to the 0.1 step, never let it be zero, '
    +'then flip the sign at random.</p>'
    +'<div class="cite">pins: the alphabet and its size; every generated challenge lands on the grid, has the right number '
    +'of non-zero harmonics and repeats for a given seed &mdash; selfTest, against derive.py&rsquo;s alphabet</div>',
  pack:'<h4>the Gaussian pair</h4>'
    +EQ(1,'A(k) = '+FR('1','&sigma;<sub>k</sub>&radic;(2&pi;)')+' e<sup>&minus;(k&minus;k<sub>0</sub>)&sup2;/2&sigma;<sub>k</sub>&sup2;</sup>, &nbsp; &#8747;A dk = 1')
    +EQ(2,'F(x) = &#8747;<sub>&minus;&infin;</sub><sup>&infin;</sup> A(k) cos(kx) dk = e<sup>&minus;&sigma;<sub>k</sub>&sup2;x&sup2;/2</sup> cos(k<sub>0</sub>x)')
    +EQ(3,'&sigma;<sub>x</sub> = 1/&sigma;<sub>k</sub> &nbsp;&rArr;&nbsp; &sigma;<sub>x</sub>&sigma;<sub>k</sub> = 1 &nbsp;<span class="rm">exactly (the Gaussian attains the bound)</span>')
    +EQ(4,'<span class="rm">envelope</span> = |F<sub>cos</sub> + iF<sub>sin</sub>| = e<sup>&minus;x&sup2;/2&sigma;<sub>x</sub>&sup2;</sup> = 1/&radic;e <span class="rm">at</span> x = &plusmn;&sigma;<sub>x</sub>')
    +'<p>[2] is the reason the drawn packet needs no numerical transform at all: the integral is done. [4] is why the '
    +'width markers sit at 1/&radic;e rather than at half height &mdash; that is the height at which the full width IS '
    +'twice the standard deviation, which is the quantity the uncertainty product is about.</p>'
    +'<div class="cite">pins: [2] against scipy quadrature over the whole line at five x and both parities; the product; '
    +'the envelope at &plusmn;&sigma;<sub>x</sub>; the sum of the plotted amplitudes &rarr; 1 &mdash; derive.py</div>',
  pair:'<h4>Poisson, and what a discrete spectrum costs</h4>'
    +EQ(1,'&Sigma;<sub>n&#8712;&#8484;</sub> k<sub>1</sub> A(nk<sub>1</sub>) cos(nk<sub>1</sub>x) = &Sigma;<sub>m&#8712;&#8484;</sub> F(x &minus; m&lambda;<sub>1</sub>), &nbsp; &lambda;<sub>1</sub> = 2&pi;/k<sub>1</sub>')
    +EQ(2,'<span class="rm">so the discrete sum is periodic:</span> F<sub>d</sub>(x + &lambda;<sub>1</sub>) = F<sub>d</sub>(x) <span class="rm">exactly</span>')
    +EQ(3,'<span class="rm">PhET keeps</span> 0 &le; k &le; 24&pi; <span class="rm">only:</span> &epsilon; &le; &frac12;erfc'+FR('k<sub>0</sub>','&sigma;<sub>k</sub>&radic;2')+' + &frac12;erfc'+FR('24&pi;&minus;k<sub>0</sub>','&sigma;<sub>k</sub>&radic;2'))
    +'<p>[1] is an identity, not an approximation, and it is what makes the picture honest: the copies are not an artefact '
    +'of the drawing, they are what the discrete spectrum <i>is</i>. [3] is the whole of the remaining difference &mdash; '
    +'6.3e&minus;5 at PhET&rsquo;s defaults, and the measured difference inside one period is 5.3e&minus;5, under it.</p>'
    +'<div class="cite">pins: [1] to 7e&minus;16 in Python and in JS; [2] to 6e&minus;15; the measured difference against '
    +'[3] at three spacings; the copy at x = &lambda;<sub>1</sub> reaching full height &mdash; derive.py</div>',
};
