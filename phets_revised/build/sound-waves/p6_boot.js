
/* ================================================================== *
 *  boot — the control panel, the tabs, the keys, the frame loop and   *
 *  the tone's audio layer                                             *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Sound Waves (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';
/* the tone: the samples are computed in toneBuffer and played from a looped
   buffer, so what is heard is what the suite checks.  Everything here is
   guarded: there is no AudioContext under the headless harnesses. */
const AUDIO={ctx:null, src:null, gain:null, key:'', state:'off', buf:null};
function audioCtor(){
  if(typeof AudioContext!=='undefined') return AudioContext;
  if(typeof webkitAudioContext!=='undefined') return webkitAudioContext;
  return null;
}
function toneWanted(){ return ST.tone&&ST.running&&ST.view!=='law'&&sourceActive(RUN); }
function toneSync(M){
  if(!toneWanted()){
    if(AUDIO.src){ try{ AUDIO.src.stop(); }catch(e){} AUDIO.src=null; }
    AUDIO.key=''; AUDIO.state='off';
    return AUDIO.state;
  }
  const AC=audioCtor();
  if(!AC){ AUDIO.state='unavailable'; return AUDIO.state; }
  const hz=RUN.f, level=toneLevel(ST.toneMode,RUN.A,M?M.listener.amp:0);
  const key=hz.toFixed(4)+'|'+level.toFixed(4);
  if(key===AUDIO.key&&AUDIO.src) return AUDIO.state;
  try{
    if(!AUDIO.ctx){ AUDIO.ctx=new AC(); AUDIO.gain=AUDIO.ctx.createGain(); AUDIO.gain.connect(AUDIO.ctx.destination); }
    const c=AUDIO.ctx;
    if(c.state==='suspended'&&c.resume) c.resume();
    const tb=toneBuffer(hz,1,c.sampleRate||TONE_SR);      /* the level rides on the gain */
    const buf=c.createBuffer(1,tb.L,c.sampleRate||TONE_SR);
    buf.getChannelData(0).set(tb.data);
    if(AUDIO.src){ try{ AUDIO.src.stop(); }catch(e){} }
    const s=c.createBufferSource();
    s.buffer=buf; s.loop=true; s.connect(AUDIO.gain); s.start();
    AUDIO.src=s; AUDIO.buf=tb; AUDIO.gain.gain.value=level; AUDIO.key=key; AUDIO.state='playing';
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

  /* the speaker */
  const gSrc=h('div',{class:'grp'},h('h3',null,'the speaker'));
  gSrc.appendChild(slider('f','frequency',AIR.fmin,AIR.fmax,1,v=>fmt(v,0)+' Hz &middot; '+sigf(waveLen(v),3)+' m'));
  gSrc.appendChild(slider('amp','amplitude',0,AIR.ampMax,0.1,v=>fmt(v,1)));
  const modeChips=chipRow(MODE_LIST,'wave',()=>{ setWaveMode(RUN,ST.wave==='cont'); });
  gSrc.appendChild(modeChips);
  const srcBtn=h('div',{class:'btnrow'},button('press the speaker button',()=>{ pressSource(syncRun()); }));
  gSrc.appendChild(srcBtn);
  const srcTag=h('div',{class:'tag'}); gSrc.appendChild(srcTag);

  /* what to show */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(chipRow(LOOK_LIST,'look'));
  gShow.appendChild(h('div',{class:'checks'},
    checkbox('graph','graph along the speaker’s row'),
    checkbox('listener','the listener'),
    checkbox('ruler','PhET’s 5 m ruler'),
    checkbox('watch','stopwatch')));
  const extraChecks=h('div',{class:'checks'},
    checkbox('nodes','the quiet hyperbolae'),
    checkbox('image','the image speaker and the ray'));
  gShow.appendChild(extraChecks);
  gShow.appendChild(h('div',{class:'btnrow'},
    button('start / stop the stopwatch',()=>{ CLOCK.watchOn=!CLOCK.watchOn; }),
    button('zero it',()=>{ CLOCK.watch=0; })));
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  /* the second speaker */
  const gSecond=h('div',{class:'grp'},h('h3',null,'the second speaker'));
  gSecond.appendChild(slider('spk2y','its height',0.35,AIR.W-0.35,0.01,v=>sigf(v,3)+' m'));
  const secondTag=h('div',{class:'tag'}); gSecond.appendChild(secondTag);

  /* the wall */
  const gWall=h('div',{class:'grp'},h('h3',null,'the wall'));
  gWall.appendChild(slider('wallX','wall position',WALLR.xmin,WALLR.xmax,0.01,v=>sigf(v,3)+' m'));
  gWall.appendChild(slider('wallAng','wall angle',WALLR.amin,WALLR.amax,0.005,v=>fmt(v/DEG,1)+'&deg;'));
  const wallTag=h('div',{class:'tag'}); gWall.appendChild(wallTag);

  /* the air */
  const gAir=h('div',{class:'grp'},h('h3',null,'air density in the box'));
  gAir.appendChild(slider('pressure','air density',0,1,0.01,v=>fmt(v,2)+' atm'));
  gAir.appendChild(h('div',{class:'btnrow'},button('back to 1 atm',()=>{ ST.pressure=1; })));
  const airTag=h('div',{class:'tag'}); gAir.appendChild(airTag);

  /* audio */
  const gAudio=h('div',{class:'grp'},h('h3',null,'audio'),
    h('div',{class:'checks'},checkbox('tone','play the tone',()=>toneSync(null))));
  gAudio.appendChild(chipRow(TONE_LIST,'toneMode',()=>toneSync(null)));
  const audioTag=h('div',{class:'tag'}); gAudio.appendChild(audioTag);

  /* time */
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(chipRow(SPEED_LIST,'speed'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gTime.appendChild(h('div',{class:'btnrow'},
    button('one step',()=>{ syncRun(); stepOnce(); }),
    button('clear the sound',()=>{ runClear(syncRun()); PROBE.head=0; PROBE.count=0; })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ resetAll(); toneSync(null); syncChips(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:CREDIT+' Measured: nothing by hand &mdash; every number is PhET&rsquo;s (read from the minified original and cited as PhET&rsquo;s values in the header) or computed and pinned to build/sound-waves/derive.py. The gas constants are the exact SI values and the molar mass of standard dry air.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gSrc,gShow,gSecond,gWall,gAir,gAudio,gTime,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS) [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view, box=(v!=='law');
    /* the frequency slider stays on show in the analysis view: that view measures the
       lattice at whatever it is set to, and marks the setting on its plane */
    rows.amp.row.hidden=!box; modeChips.hidden=!box; srcBtn.hidden=!box;
    gShow.hidden=!box; gTime.hidden=!box; gAudio.hidden=!box;
    gSecond.hidden=(v!=='two'); gWall.hidden=(v!=='wall'); gAir.hidden=(v!=='air');
    rows.cb_nodes.row.hidden=(v!=='two');
    rows.cb_image.row.hidden=(v!=='wall');
    extraChecks.hidden=(v!=='two'&&v!=='wall');
    rows.cb_ruler.row.hidden=!box;
    rows.cb_watch.row.hidden=!box;
    for(const k in rows) rows[k].sync();
    srcTag.innerHTML=!box
      ? 'the plane below marks this setting, and measures the lattice at it &mdash; the five fixed frequencies are measured whatever the slider says'
      : (ST.wave==='pulse'
        ? 'in pulse mode the button fires one period and pops back up'+(RUN.pulse.on?' &mdash; <b>firing</b>':'')
        : 'the button switches the speaker on and off, and starts it from zero; the cell in front of the cone is driven at 1.2 &times; the amplitude (PhET&rsquo;s value). Changing the sound mode stops it, as PhET&rsquo;s does.');
    showTag.innerHTML=v==='two'
      ? 'the hyperbolae are drawn from |r&#8321; &minus; r&#8322;| = (m + &frac12;)&lambda;, not found on the picture &mdash; drag the listener onto one and watch the trace go flat'
      : (v==='wall' ? 'the image speaker is the reflection of the real one in the wall; the sound behind the wall is not drawn at all'
                    : 'drag the listener and the ruler on the picture');
    secondTag.innerHTML='PhET fixes both speakers to the same column and lets you slide the second one up and down; the lattice puts it on the nearest row, so the separation moves in steps of one cell ('+sigf(sceneDx()*100,3)+' cm)';
    wallTag.innerHTML='PhET&rsquo;s wall crosses the bottom edge at the position you set and leans back by the angle; at '+fmt(WALLR.amin/DEG,0)+'&deg; it lies almost flat along the floor and hides almost nothing';
    airTag.innerHTML='PhET scales its source by this number, and so does this sim &mdash; which is right for a cone of fixed velocity, p = &rho;cu. The speed of sound does not move at all.';
    audioTag.innerHTML='a sine at the frequency on the slider, from a buffer of whole cycles so it loops without a click'
      +(ST.toneMode==='listener'?'; its level follows the pressure amplitude the lattice holds at the listener':'; its level follows the amplitude slider, as PhET&rsquo;s does');
    timeTag.innerHTML='space runs/pauses &nbsp; <b>p</b> presses the speaker button &nbsp; <b>r</b> clears the sound &nbsp; 1&ndash;6 switch views';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=ST.view==='law'?'1–6 switch views'
        :'press the speaker button · drag the listener, the ruler and the second speaker · space pauses · 1–6 switch views';
      infoEl.innerHTML=INFO[ST.view]||''; physEl.innerHTML=DERIV[ST.view]||'';
      M.tone.on=(toneSync(M)==='playing');
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
    else if(e.key==='r'){ runClear(syncRun()); PROBE.head=0; PROBE.count=0; dirty=true; refresh(); }
    else if(e.key==='p'){ if(pressSource(syncRun())){ dirty=true; refresh(); } }
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
        if(advanced&&frameN%10===0){ const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); toneSync(M); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  intro:'A loudspeaker at the left of a room ten metres across, seen from above. The cell in front of its cone is pushed in and out, and every other cell of a 231 × 231 lattice obeys the wave equation in its simplest discrete form: each step it accelerates toward the average of its four neighbours. That one rule makes circular wavefronts that spread at a fixed speed — 343 metres a second, the speed the air sets — and fade as they go, because the energy that left the cone is spread round a growing circle. Press the green button to switch the speaker off: the sound already in the room carries on without it, which is what it means for a wave to leave its source. Raise the frequency and the crests crowd together; that is the whole of λ = v/f, because the speed belongs to the air and not to the speaker. Switch the picture to air parcels and you see what is really moving: each parcel jiggles back and forth about its own place, crowding where the pressure is high. Nothing travels from the cone to your ear except the squeeze.',
  measure:'The same room with PhET’s two instruments in it. The ruler is five metres long and rigid — lay it across the wavefronts and count how many fit, and you have measured the wavelength without being told it. The stopwatch runs in the sim’s own time, which is 207 times slower than real, so one period of a 550 Hz note lasts 1.82 ms of model time; start it, watch the listener’s trace go through one full swing, and stop it. Multiply the two and you get the speed of sound. The point of doing it at more than one frequency is that the answer does not change: the wavelength halves when the frequency doubles, and 343 m/s comes back every time.',
  two:'A second loudspeaker, in step with the first, and the room fills with a pattern of loud and quiet lines that neither speaker makes on its own. A place is quiet when the two paths to it differ by half a wavelength, or one and a half, or two and a half: |r₁ − r₂| = (m + ½)λ. That equation is the definition of a hyperbola with the two speakers as its foci, which is exactly what the orange curves are — and far from the speakers each one straightens into a ray at sin θ = (m + ½)λ/d, the two-slit condition. Drag the listener onto a quiet line and its trace flattens; drag it between them and the trace doubles in height. Move the second speaker and watch the whole pattern re-aim. Raise the frequency and more quiet lines appear, one for every extra half-wavelength that fits into the separation.',
  wall:'A hard wall, and the question of where the reflection comes from. The answer is the simplest in acoustics: reflect the speaker in the wall and the sound that comes back is the sound of that image speaker. It has to be — the wall is rigid, so no air crosses it, so ∂p/∂n = 0 there, and a field made of a source plus its mirror image satisfies that identically. Everything else follows. The ray that reaches the listener is the straight line from the image, bent at the wall, and the two angles it makes with the normal are therefore equal; its length is the shortest path from the speaker to the listener by way of the wall. And because the direct and reflected sound are two sources a fixed distance apart, the loud and quiet bands in front of the wall are the same hyperbolae as the two-speaker screen. Nothing is drawn behind the wall: this model has no diffraction round its edge.',
  air:'Take the air out of the box and the sound goes away — but it is worth being precise about what changes. The cone still moves; what falls is the pressure it can make, because a cone of fixed velocity radiates p = ρcu and ρ is what is being removed. Halve the density and you halve the pressure amplitude and the intensity, which is 6 dB; take it to a tenth and you lose 20 dB. What does not change at all is the SPEED. Sound in an ideal gas runs at √(γp/ρ), and pumping gas out lowers p and ρ together, so the ratio — and the speed — sits exactly where it was: 343 m/s at 1 atm, at 0.1 atm and at 0.001 atm, as long as the temperature is the same. The panel on the right says so with numbers. The honest limit of the model is at the bottom of the slider: a real gas stops carrying sound once its molecules travel a wavelength between collisions, which for a 1000 Hz note happens near 2×10⁻⁷ atm; this lattice keeps solving the wave equation all the way down to nothing.',
  law:'The claim λ = v/f, put to the test on the lattice that is drawing every other view. Each green dot is not the formula: it is a wavelength MEASURED on a fresh run — the lattice is driven at that frequency until it settles, two whole periods are recorded at every cell along the axis, and at each cell a least-squares fit against the drive’s own phase gives an amplitude and a phase. The slope of that phase is the wavenumber. It lands on the orange line to five figures over most of the slider, and drifts to about a third of a per cent at 100 Hz, where the fit window holds barely one and a half wavelengths. The left-hand panel puts that error beside PhET’s: PhET fixes one time step for the whole sim, which leaves its wavelengths 1.3 % short at the bottom of the slider and 12.8 % short at the top. The right-hand panel is why this lattice is bigger than PhET’s. A square lattice is not isotropic: a wave travelling along the diagonal is longer than one travelling along an axis, and a pulse travels slower than its own crests. Both grow as the wave gets coarser, so the size of the lattice is the price paid to keep them small.'
};
function FR2(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  intro:'<h4>the lattice and its clock</h4>'
    +EQ(1,'p<sub>ij</sub><sup>n+1</sup> = 2p<sub>ij</sub><sup>n</sup> &minus; p<sub>ij</sub><sup>n&minus;1</sup> + C&sup2;(p<sub>i+1,j</sub> + p<sub>i&minus;1,j</sub> + p<sub>i,j+1</sub> + p<sub>i,j&minus;1</sub> &minus; 4p<sub>ij</sub>)<sup>n</sup>, &nbsp; C = '+FR2('v&Delta;t','&Delta;x')+' = &frac12;')
    +EQ(2,'&Delta;x = W/191, &nbsp; N<sub>&lambda;</sub> = '+FR2('v','f&Delta;x')+', &nbsp; &Omega; = &omega;&Delta;t = 2 asin(C sin(&pi;/N<sub>&lambda;</sub>)), &nbsp; &Delta;t = '+FR2('&Omega;','2&pi;f'))
    +'<p>[2] is the lattice&rsquo;s own dispersion relation solved for the time step, so a wave along an axis has exactly N<sub>&lambda;</sub> cells per wavelength and 2&pi;/&Omega; steps per period: &lambda; = v/f and T = 1/f hold on the lattice and not only on paper. PhET keeps one step for the whole sim instead, which leaves its wavelengths 1.3 % to 12.8 % short (the readout prints the figure for the current setting). The cell in front of the cone is set to 1.2 A sin(n&Omega;) after each step (PhET&rsquo;s 1.2), and pressing the button restarts that phase at zero, as PhET&rsquo;s resetPhase does.</p>'
    +'<div class="cite">pins: the stencil on an exact lattice plane wave (5e-15), the calibration at five frequencies, the twin&rsquo;s field cell by cell &mdash; derive.py</div>',
  measure:'<h4>what the two instruments measure</h4>'
    +EQ(1,'<span class="hl">v = f&lambda;</span>, &nbsp; T = 1/f, &nbsp; v = 343 m/s &nbsp;<span class="rm">(PhET&rsquo;s value)</span>')
    +EQ(2,'v = &radic;(&gamma;RT/M) = 343.235 m/s <span class="rm">at 20.00 &deg;C</span>, &nbsp; 343 m/s <span class="rm">at 19.60 &deg;C</span>')
    +'<p>The speed is not a property of the speaker: it is &radic;(&gamma;RT/M) for the gas, with &gamma; = 7/5 for a diatomic ideal gas, R = 8.314462618 J mol&#8315;&sup1; K&#8315;&sup1; (exact since 2019) and M = 28.9647 g/mol for standard dry air. PhET&rsquo;s 343 m/s is that formula at 19.60 &deg;C, 0.068 % below the 20 &deg;C value. Measure &lambda; and T at any frequency on the slider and their product returns it.</p>'
    +'<div class="cite">pins: the ideal-gas speed at 20 &deg;C, the temperature that gives exactly 343, and the same speed from &radic;(&gamma;p/&rho;) &mdash; derive.py</div>',
  two:'<h4>where two speakers are quiet</h4>'
    +EQ(1,'|r&#8321; &minus; r&#8322;| = (m + &frac12;)&lambda; &nbsp;&hArr;&nbsp; '+FR2('y&sup2;','a&sup2;')+' &minus; '+FR2('x&sup2;','c&sup2; &minus; a&sup2;')+' = 1, &nbsp; a = '+FR2('(m+&frac12;)&lambda;','2')+', &nbsp; c = '+FR2('d','2'))
    +EQ(2,'<span class="rm">far away:</span> &nbsp; sin&theta;<sub>m</sub> = '+FR2('(m + &frac12;)&lambda;','d')+', &nbsp; <span class="rm">and there are as many lines as there are m with (m + &frac12;)&lambda; &lt; d</span>')
    +EQ(3,'A = &radic;(A&#8321;&sup2; + A&#8322;&sup2; + 2A&#8321;A&#8322;cos&Delta;&phi;), &nbsp; &Delta;&phi; = 2&pi;(r&#8321; &minus; r&#8322;)/&lambda;')
    +'<p>[1] is a hyperbola because a curve of constant difference of distances from two points IS one; the closed form agrees with root-solving |r&#8321; &minus; r&#8322;| directly to 6e-13, and the asymptote in [2] with the two-slit condition to 1e-16. On the lattice the measured quiet lines sit up to 2.5 cells outside those curves at 550 Hz &mdash; not noise: replacing the single &lambda; in [1] by the lattice&rsquo;s own k(&theta;), which is smaller off the axes, brings the prediction back to within 0.16 of a cell.</p>'
    +'<div class="cite">pins: the closed form against brentq, the asymptotes, ten measured nodal points with and without the lattice&rsquo;s k(&theta;), and [3] at seven places &mdash; derive.py</div>',
  wall:'<h4>a rigid wall is a mirror</h4>'
    +EQ(1,'&part;p/&part;n = 0 <span class="rm">on the wall</span> &nbsp;&hArr;&nbsp; p(P) = p<sub>S</sub>(P) + p<sub>S</sub>(P&prime;), &nbsp; P&prime; = <span class="rm">the mirror of P</span>')
    +EQ(2,'|P&prime; &minus; S| = |P &minus; S&prime;| &nbsp;&rArr;&nbsp; <span class="rm">the second term IS the field of the image source S&prime;</span>')
    +EQ(3,'<span class="hl">&theta;<sub>in</sub> = &theta;<sub>out</sub></span>, &nbsp; |SQ| + |QP| = |S&prime;P| &nbsp;<span class="rm">(Fermat: the shortest path by way of the wall)</span>')
    +'<p>[2] is the whole trick: mirroring is an isometry, so reading the one lattice at the mirror of a point gives exactly the field of a speaker at the mirror of the speaker. [3] then follows by geometry rather than by assumption, and the suite checks all three: the two angles agree to 3e-15, the path length to 5e-15, and the normal derivative of the drawn field on the wall to 5e-13. What this model does NOT have is diffraction round the wall&rsquo;s edge: behind it, nothing is drawn.</p>'
    +'<div class="cite">pins: the mirror map against PhET&rsquo;s own projection form, 14 rays, the Neumann condition on the running field &mdash; derive.py</div>',
  air:'<h4>what pressure does, and does not, change</h4>'
    +EQ(1,'c = &radic;('+FR2('&gamma;p','&rho;')+') = &radic;('+FR2('&gamma;RT','M')+') &nbsp;<span class="rm">&mdash; no p, no &rho;: the speed does not depend on how much gas there is</span>')
    +EQ(2,'p<sub>amp</sub> = &rho;cu &nbsp;&prop;&nbsp; &rho;, &nbsp; I = '+FR2('p<sub>amp</sub>&sup2;','2&rho;c')+' &prop; &rho;, &nbsp; <span class="hl">20 log&#8321;&#8320;(&rho;/&rho;&#8320;) dB</span>')
    +EQ(3,'&ell; = '+FR2('k<sub>B</sub>T','&radic;2 &pi;d&sup2;p')+' = 65.7 nm <span class="rm">at 1 atm</span>; &nbsp; &ell; = &lambda; <span class="rm">at</span> 1.9&times;10<sup>&minus;7</sup> <span class="rm">atm for 1000 Hz</span>')
    +'<p>[1] is why the wavefronts keep their spacing as the box empties and only fade. [2] is what the slider really does: it scales the drive, exactly as PhET&rsquo;s pressure property does, which is the right law for a cone of fixed velocity. [3] is where the model stops being physics: below about 10<sup>&minus;7</sup> atm a 1000 Hz sound is no longer a continuum wave at all, and this lattice goes on solving the wave equation anyway.</p>'
    +'<div class="cite">pins: the speed at five pressures (identical to 1e-15), the density, the decibels, the mean free path, and the twin&rsquo;s field scaling exactly with the density &mdash; derive.py</div>',
  law:'<h4>measuring &lambda; on the lattice</h4>'
    +EQ(1,'p(n) = a sin&phi;<sub>n</sub> + b cos&phi;<sub>n</sub> + c + d(n &minus; n&#772;) &nbsp;&rArr;&nbsp; A = &radic;(a&sup2;+b&sup2;), &nbsp; &psi; = atan2(b, a)')
    +EQ(2,'k = &minus; d&psi;/dr &nbsp;<span class="rm">over cells 30 to 120</span>, &nbsp; &lambda;<sub>measured</sub> = 2&pi;/k, &nbsp; A &prop; r<sup>&minus;1/2</sup>')
    +EQ(3,'<span class="rm">the square lattice:</span> &nbsp; sin&sup2;(&Omega;/2) = C&sup2;[sin&sup2;(k<sub>x</sub>/2) + sin&sup2;(k<sub>y</sub>/2)] &nbsp;&rArr;&nbsp; v<sub>g</sub> &ne; v<sub>p</sub>, &nbsp; &lambda;(45&deg;) &ne; &lambda;(0&deg;)')
    +'<p>The constant and the drift in [1] absorb the wake of the switch-on, which in two dimensions dies only as 1/&omega;t. The fit returns &lambda; to within 0.05 % of v/f from 325 Hz up and 0.35 % at 100 Hz, and an envelope power of &minus;0.46 to &minus;0.51 against the &minus;&frac12; a spreading two-dimensional wave must have. [3] is the lattice&rsquo;s own anisotropy, the reason this sim uses 231 cells rather than PhET&rsquo;s 151: at 1000 Hz PhET holds 3.81 cells per wavelength and this lattice 6.55.</p>'
    +'<div class="cite">pins: the measurement at five frequencies (&lambda;, the envelope power, the amplitude and phase at four cells), the continuum Hankel near field over the same cells, and the dispersion at five frequencies &mdash; derive.py</div>'
};
