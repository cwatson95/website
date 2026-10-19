
/* ================================================================== *
 *  boot — the control panel, the tabs, the keys, the frame loop and   *
 *  the tone's audio layer                                             *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Waves Intro (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';
/* the tone: the samples are computed in toneBuffer and played from a looped
   buffer, so what is heard is what the suite checks.  Everything here is
   guarded: there is no AudioContext under the headless harnesses. */
const AUDIO={ctx:null, src:null, gain:null, key:'', state:'off', buf:null};
function audioCtor(){
  if(typeof AudioContext!=='undefined') return AudioContext;
  if(typeof webkitAudioContext!=='undefined') return webkitAudioContext;
  return null;
}
function toneSync(){
  const want=toneOn();
  if(!want){
    if(AUDIO.src){ try{ AUDIO.src.stop(); }catch(e){} AUDIO.src=null; }
    AUDIO.key=''; AUDIO.state='off';
    return AUDIO.state;
  }
  const AC=audioCtor();
  if(!AC){ AUDIO.state='unavailable'; return AUDIO.state; }
  const p=toneParams(RUNS.sound), key=p.hz.toFixed(4)+'|'+p.level.toFixed(4);
  if(key===AUDIO.key&&AUDIO.src) return AUDIO.state;
  try{
    if(!AUDIO.ctx){ AUDIO.ctx=new AC(); AUDIO.gain=AUDIO.ctx.createGain(); AUDIO.gain.connect(AUDIO.ctx.destination); }
    const c=AUDIO.ctx;
    if(c.state==='suspended'&&c.resume) c.resume();
    const tb=toneBuffer(p.hz,1,c.sampleRate||TONE_SR);       /* the level rides on the gain, as PhET's does */
    const buf=c.createBuffer(1,tb.L,c.sampleRate||TONE_SR);
    buf.getChannelData(0).set(tb.data);
    if(AUDIO.src){ try{ AUDIO.src.stop(); }catch(e){} }
    const s=c.createBufferSource();
    s.buffer=buf; s.loop=true; s.connect(AUDIO.gain); s.start();
    AUDIO.src=s; AUDIO.buf=tb; AUDIO.gain.gain.value=p.level; AUDIO.key=key; AUDIO.state='playing';
  }catch(e){ AUDIO.state='unavailable'; }
  return AUDIO.state;
}

function boot(){
  const canvas=document.getElementById('scene');
  const panel=document.getElementById('panel');
  const tabsEl=document.getElementById('tabs');
  const roEl=document.getElementById('readout');
  const eqEl=document.getElementById('eqbar');
  const tagEl=document.getElementById('tag');
  const hintEl=document.getElementById('hint');
  const errEl=document.getElementById('errbox');
  const S=makeScene(canvas);
  let dirty=false;

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    ST.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===ST.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:ST.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:ST[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=ST[key]; val.textContent=plain(fmtf(ST[key])); };
    inp.addEventListener('input',()=>{ ST[key]=parseFloat(inp.value);
      val.textContent=plain(fmtf(ST[key])); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=ST[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ ST[key]=inp.checked; if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=ST[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(ST[key]===o.id?' on':''),onclick:()=>{
        ST[key]=o.id; if(onPick) onPick(o); syncChips(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},lab2); }
  const cur=()=>RUNS[ST.view]||null;

  /* the source */
  const gSrc=h('div',{class:'grp'},h('h3',null,'the source'));
  const FR={water:[0.005,'frequency (drip rate), Hz'],sound:[0.001,'frequency (pitch), Hz'],light:[0.0005,'frequency (colour), THz']};
  for(const id of SCENE_IDS){ const Sc=SCENES[id];
    gSrc.appendChild(slider('f_'+id,FR[id][1],Sc.fmin,Sc.fmax,FR[id][0],
      v=>sigf(v*Sc.fMul,4)+(id==='light'?' ('+fmt(Sc.v/v,0)+' nm)':''))); }
  for(const id of SCENE_IDS) gSrc.appendChild(slider('amp_'+id,'amplitude',0,10,0.1,v=>fmt(v,1)));
  const waveChips=chipRow(WAVE_LIST,'wave'); gSrc.appendChild(waveChips);
  const srcBtn=h('div',{class:'btnrow'},button('press the source button',()=>{ const R=syncRun(ST.view); if(R) pressSource(R); }));
  gSrc.appendChild(srcBtn);
  const srcTag=h('div',{class:'tag'}); gSrc.appendChild(srcTag);

  /* what to show */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  const lookChips=chipRow(SIDE_LIST,'look'); gShow.appendChild(lookChips);
  const soundChips=chipRow(SOUNDVIEW_LIST,'soundView'); gShow.appendChild(soundChips);
  const soundChecks=h('div',{class:'checks'},checkbox('tone','play tone',()=>toneSync())); gShow.appendChild(soundChecks);
  const lightChecks=h('div',{class:'checks'},checkbox('screen','screen'),checkbox('inten','intensity graph (not in PhET’s Waves Intro)'));
  gShow.appendChild(lightChecks);
  const showChecks=h('div',{class:'checks'},checkbox('graph','graph of the centre line'));
  gShow.appendChild(showChecks);
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  /* the tools */
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('tape','tape measure'),checkbox('watch','stopwatch'),checkbox('meter','wave meter')));
  gTools.appendChild(h('div',{class:'btnrow'},
    button('start / stop the stopwatch',()=>{ const R=cur(); if(R) R.watch.on=!R.watch.on; }),
    button('zero the stopwatch',()=>{ const R=cur(); if(R) R.watch.t=0; })));
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  /* time */
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(chipRow(SPEED_LIST,'speed'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gTime.appendChild(h('div',{class:'btnrow'},
    button('one step',()=>{ const R=syncRun(ST.view); if(R) runStep(R); }),
    button('clear the waves',()=>{ const R=syncRun(ST.view); if(R) runClear(R); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
      TOOLS.tape=JSON.parse(JSON.stringify(TOOLS0.tape)); TOOLS.probes=JSON.parse(JSON.stringify(TOOLS0.probes));
      resetRuns(); toneSync(); syncChips(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:CREDIT+' Measured: nothing by hand — every number is PhET&rsquo;s (read from the minified original and cited as PhET&rsquo;s values in the header) or computed and pinned to build/waves-intro/derive.py, whose twin reproduces the wave-interference engine&rsquo;s own pins. Colour: the CIE 1931 table.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gSrc,gShow,gTools,gTime,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS) [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view, med=!!MEDIA[v];
    for(const id of SCENE_IDS){
      rows['f_'+id].row.hidden=med&&(id!==v);
      rows['amp_'+id].row.hidden=(id!==v);
    }
    waveChips.hidden=!med; srcBtn.hidden=!med;
    gShow.hidden=!med; gTools.hidden=!med; gTime.hidden=!med;
    lookChips.hidden=(v!=='water'); soundChips.hidden=(v!=='sound');
    soundChecks.hidden=(v!=='sound'); lightChecks.hidden=(v!=='light');
    for(const k in rows) rows[k].sync();
    const R=cur();
    srcTag.innerHTML=med
      ? (ST.wave==='pulse'
          ? 'in pulse mode the button fires one period and pops back up' + (R&&R.pulse.on?' &mdash; <b>firing</b>':'')
          : 'the button switches the source on and off, and starts it from zero; the source cell is driven at 1.2 &times; the amplitude (PhET&rsquo;s value)')
      : 'each slider moves its own medium&rsquo;s marker on the plane below, and the lattice is measured again at that frequency';
    showTag.innerHTML=v==='light'
      ? 'PhET&rsquo;s Waves Intro shows the screen but never the intensity graph: it builds the panel with showIntensityCheckbox false'
      : (v==='sound' ? 'the tone is PhET&rsquo;s: 1000 f Hz at output level 0.3 A/10, playing only while the source runs'
                     : 'the graph is PhET&rsquo;s "Graph": the '+(SCENES[v]||SCENES.water).what+' along the middle row');
    toolTag.innerHTML='drag the tape&rsquo;s ends and the probes on the picture'+(R&&ST.watch?(R.watch.on?' &middot; the stopwatch is running':' &middot; the stopwatch is stopped'):'');
    timeTag.innerHTML='space runs/pauses &nbsp; <b>p</b> presses the source button &nbsp; <b>r</b> clears the waves &nbsp; 1&ndash;4 switch views';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=MEDIA[ST.view]?'press the source button · drag the tools · space pauses · 1–4 switch views'
                                       :'1–4 switch views';
      infoEl.innerHTML=INFO[ST.view]||''; physEl.innerHTML=DERIV[ST.view]||'';
      toneSync();
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); ST.running=!ST.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ const R=syncRun(ST.view); if(R){ runClear(R); dirty=true; refresh(); } }
    else if(e.key==='p'){ const R=syncRun(ST.view); if(R&&pressSource(R)){ dirty=true; refresh(); } }
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
    let advanced=false;
    try{ advanced=S.step(); }catch(e){ fail(e); }
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        if(advanced&&frameN%10===0){ const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); toneSync(); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  water:'A ripple tank seen from above. One cell of a 151 × 151 lattice is driven up and down, and every other cell obeys the wave equation in its simplest discrete form: each step it accelerates toward the average of its four neighbours. That one rule makes circular ripples that spread at a fixed speed and fade as 1/√r, because the energy that left the source is spread round a growing circle. Press the green button to start the dripper and press it again to stop it: the ripples already made carry on without it, which is what it means for a wave to leave its source. Raise the drip rate and the crests crowd together — the speed belongs to the water, so a faster drip can only mean a shorter wavelength, λ = v/f. The tape measure, the stopwatch and the wave meter are there for you to check exactly that: measure a crest-to-crest distance, time one bob of a probe, multiply. The side view shows the same wave as the height of the water along the middle row.',
  sound:'The same lattice, the same rule, a different ruler and clock: five metres across and milliseconds instead of ten centimetres and seconds. What the colour shows now is pressure — where the air is squeezed and where it is rarefied — and the wave runs at 343 m/s, twenty thousand times faster than the ripples on water. Switch to particles and the air itself appears: each parcel is pushed along the pressure gradient and crowds where the pressure is high, then returns. Nothing travels from the speaker to you except the squeeze; the parcels only jiggle, by less than a third of their spacing even here, where the displacement is drawn exaggerated. Turn on the tone and you hear the frequency you are watching, 220 to 440 Hz — an octave, and one whole octave of wavelength with it.',
  light:'The same lattice again, now five micrometres across and ticking in femtoseconds. The colour of the picture is the colour of the light, because for light the frequency IS the colour: 384 THz at the red end of the slider, 789 THz at the violet end, and the wavelength that goes with them, 780 nm down to 380 nm. The field itself oscillates far too fast for any detector to follow, so what a screen records is its mean square, averaged over many periods — that is the strip at the right-hand edge, drawn through PhET’s own brightness table. A single source spreads its light evenly in every direction, so the screen should simply fade from the middle outwards as 1/r; it nearly does, and where it ripples, the ripple is the light the tank’s own edges send back.',
  media:'Three screens of PhET’s Waves Intro, three media, and one equation: v = fλ. Plot wavelength against frequency on log scales and a fixed speed becomes a straight line of slope −1, so the three media are three parallel lines, separated by the ten orders of magnitude between a ripple and a light wave. The cyan stretch on each line is the range PhET’s own slider covers; the magenta ring is where you have set it. The green dot is not the formula at all — it is the wavelength measured on the running lattice, by fitting the drive’s own sine to every cell along the axis of the tank and taking the slope of the phase, exactly as the tape measure would. The strips below show those fits: the wave at steady state, the 1/√r envelope it must follow in two dimensions, and the wavelength the fit returns. It lands within about a tenth of a per cent of v/f — except at the very lowest drip rate, where the tank is barely a wavelength and a half long and the near field and the edges of the tank have their say.'
};
function FR2(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  water:'<h4>the lattice and its clock</h4>'
    +EQ(1,'u<sub>ij</sub><sup>n+1</sup> = 2u<sub>ij</sub><sup>n</sup> &minus; u<sub>ij</sub><sup>n&minus;1</sup> + C&sup2;(u<sub>i+1,j</sub> + u<sub>i&minus;1,j</sub> + u<sub>i,j+1</sub> + u<sub>i,j&minus;1</sub> &minus; 4u<sub>ij</sub>)<sup>n</sup>, &nbsp; C = '+FR2('c&Delta;t','&Delta;x')+' = &frac12;')
    +EQ(2,'&Delta;x = W/111, &nbsp; N<sub>&lambda;</sub> = '+FR2('v','f&Delta;x')+', &nbsp; &Omega; = &omega;&Delta;t = 2 asin(C sin(&pi;/N<sub>&lambda;</sub>)), &nbsp; &Delta;t = '+FR2('&Omega;','2&pi;f'))
    +'<p>[2] is the lattice&rsquo;s own dispersion relation solved for the time step, so a wave along an axis has exactly N<sub>&lambda;</sub> cells per wavelength and 2&pi;/&Omega; steps per period: &lambda; = v/f and T = 1/f hold on the lattice and not only on paper. PhET keeps one step per medium instead, which leaves its wavelengths 0.7 % to 3.2 % short (the readout prints the figure for the current setting). The source cell is set to 1.2 A sin(n&Omega;) after each step (PhET&rsquo;s 1.2), and pressing the button restarts that phase at zero, as PhET&rsquo;s resetPhase does.</p>'
    +'<div class="cite">pins: the engine&rsquo;s own twin (wave-interference refvals.txt, reproduced here to 1e-13), the calibration of all three media, the dispersion relation &mdash; derive.py</div>',
  sound:'<h4>pressure, and the air that carries it</h4>'
    +EQ(1,'p(r,t) &asymp; '+FR2('P<sub>0</sub>','&radic;r')+' sin(&omega;t &minus; kr), &nbsp; k = 2&pi;/&lambda;, &nbsp; v = f&lambda; = 343 m/s')
    +EQ(2,'&rho; &part;&sup2;&xi;/&part;t&sup2; = &minus;&nabla;p &nbsp;&rArr;&nbsp; <span class="rm">at one frequency</span> &nbsp; &xi; = '+FR2('&nabla;p','&rho;&omega;&sup2;'))
    +'<p>[2] is why the parcels crowd where the pressure is high and why they move along the wave rather than across it: sound in a gas is longitudinal. The drawing scales &xi; so that a wave at PhET&rsquo;s full colour moves a parcel 0.3 of the parcel spacing; beside the source, where the field is stronger than full colour, the push reaches about 0.4 of it, which is still well short of the spacing that would make the parcels cross. PhET instead gives each parcel a spring, a damper and a random jitter. The 1/&radic;r in [1] is the two-dimensional spreading law, which the analysis view measures.</p>'
    +'<div class="cite">pins: the twin at 0.2937 per ms after 300 steps; the parcels&rsquo; displacement; PhET&rsquo;s tone (1000 f Hz, level 0.3 A/10) and its looped buffer &mdash; derive.py</div>',
  light:'<h4>the screen</h4>'
    +EQ(1,'I(y) = &lang;E&sup2;&rang; = '+FR2('1','N')+' &Sigma;<sub>n</sub> u(y, t<sub>n</sub>)&sup2; &nbsp;<span class="rm">over a whole number of periods (PhET averages 90 steps)</span>')
    +EQ(2,'<span class="rm">PhET then smooths over 3 rows, averages over &plusmn;39, and maps through its brightness table:</span> &nbsp; 0 &rarr; 0, &nbsp; 0.00224 &rarr; 0.4, &nbsp; 0.0089 &rarr; 0.5, &nbsp; 0.0537 &rarr; 0.64, &nbsp; 0.134 &rarr; 0.74, &nbsp; 0.210 &rarr; 0.8, &nbsp; 1 &rarr; 1')
    +EQ(3,'<span class="rm">one source, two dimensions:</span> &nbsp; I(y) &prop; 1/r, &nbsp; r = &radic;(X&sup2; + y&sup2;)')
    +'<p>The measured profile follows [3] to within 9 %: a ripple of about one wavelength&rsquo;s period that the tank&rsquo;s edges reflect back (rms 2.0 % on PhET&rsquo;s 151 cells, 1.5 % on 401, 0.75 % on 601 &mdash; it is the edges), on a smooth tilt of about 6 % that is the square lattice&rsquo;s own anisotropy. PhET&rsquo;s &plusmn;39-row average smooths the ripple away, which is what the strip shows.</p>'
    +'<div class="cite">pins: the twin&rsquo;s screen after 400 steps, its window of 92 steps, the smoothing, the &plusmn;39 average and PhET&rsquo;s brightness at seven rows; the 1/r comparison on three lattice sizes &mdash; derive.py</div>',
  media:'<h4>v = f&lambda;, and measuring &lambda; on the lattice</h4>'
    +EQ(1,'&lambda; = v/f &nbsp;&rArr;&nbsp; log &lambda; = log v &minus; log f &nbsp;<span class="rm">(a line of slope &minus;1 for each medium)</span>')
    +EQ(2,'u(n) = a sin&phi;<sub>n</sub> + b cos&phi;<sub>n</sub> + c + d(n &minus; n&#772;) &nbsp;&rArr;&nbsp; A = &radic;(a&sup2;+b&sup2;), &nbsp; &psi; = atan2(b, a)')
    +EQ(3,'k = &minus; d&psi;/dr &nbsp;<span class="rm">over cells 30 to 100</span>, &nbsp; &lambda;<sub>measured</sub> = 2&pi;/k, &nbsp; A &prop; r<sup>&minus;1/2</sup>')
    +'<p>The constant and the drift in [2] absorb the wake of the switch-on, which in two dimensions dies away only as 1/&omega;t. The fit returns &lambda; to within 0.03 % (light), 0.08 % (water) and 0.15 % (sound) of v/f at PhET&rsquo;s default frequencies, and an envelope power of &minus;0.47 to &minus;0.54 against the &minus;&frac12; the spreading law demands. At water&rsquo;s 0.25 Hz it reads 1.6 % short: the phase of a two-dimensional wave is kr &minus; &pi;/4 &minus; 1/8kr, and that near field accounts for 0.46 % of it (scipy&rsquo;s Hankel function, fitted over the same cells); the rest is the tank &mdash; on a 401-cell lattice the same fit returns 0.49 %.</p>'
    +'<div class="cite">pins: the measurement at six settings (fit steps, &lambda;, the envelope power, amplitude and phase at five cells), the continuum near field, and the 401-cell comparison &mdash; derive.py</div>'
};
