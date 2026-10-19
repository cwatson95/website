
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Wave Interference (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';
const DISORDER_NAMES=['none','a little','some','more','lots'];
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
  TABS.forEach(([k,lab])=>{ tabsEl.appendChild(h('button',{class:ST.view===k?'active':'',onclick:()=>setView(k)},lab)); });

  const rows={};
  function slider(key,lab,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:ST[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab),inp,val);
    const sync=()=>{ inp.value=ST[key]; val.textContent=plain(fmtf(ST[key])); };
    inp.addEventListener('input',()=>{ ST[key]=parseFloat(inp.value);
      val.textContent=plain(fmtf(ST[key])); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=ST[key];
    const el=h('label',null,inp,lab);
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
  function button(lab,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},lab); }
  const cur=()=>RUNS[ST.view]||null;

  /* the medium and the source */
  const gScene=h('div',{class:'grp'},h('h3',null,'the medium'));
  gScene.appendChild(chipRow(SCENE_LIST,'scene'));
  const gSrc=h('div',{class:'grp'},h('h3',null,'the source'));
  const FR={water:[0.005,'drip rate, Hz'],sound:[0.001,'tone, Hz'],light:[0.0005,'frequency, THz']};
  for(const id of SCENE_IDS){ const Sc=SCENES[id];
    gSrc.appendChild(slider('f_'+id,FR[id][1],Sc.fmin,Sc.fmax,FR[id][0],v=>sigf(v*Sc.fMul,4)+(id==='light'?' ('+fmt(Sc.v/v,0)+' nm)':''))); }
  gSrc.appendChild(slider('amp_tank','amplitude',0,10,0.1,v=>fmt(v,1)));
  gSrc.appendChild(slider('amp_two','amplitude, both sources',0,10,0.1,v=>fmt(v,1)));
  gSrc.appendChild(slider('amp_slits','amplitude, plane wave',0,10,0.1,v=>fmt(v,1)));
  const waveChips=chipRow(WAVE_LIST,'wave'); gSrc.appendChild(waveChips);
  const pulseBtn=h('div',{class:'btnrow'},button('fire a pulse',()=>{ const R=syncRun(ST.view); if(R) firePulse(R); }));
  gSrc.appendChild(pulseBtn);
  const srcChecks=h('div',{class:'checks'},checkbox('src1','top source on'),checkbox('src2','bottom source on'));
  gSrc.appendChild(srcChecks);
  const planeCheck=h('div',{class:'checks'},checkbox('planeOn','plane-wave generator on'));
  gSrc.appendChild(planeCheck);
  const srcTag=h('div',{class:'tag'}); gSrc.appendChild(srcTag);

  /* the geometry: the two sources, the barrier */
  const gGeo=h('div',{class:'grp'},h('h3',null,'the geometry'));
  const SEPR={water:[0.05,'separation, cm (water)'],sound:[1,'separation, cm (sound)'],light:[10,'separation, nm']};
  for(const id of SCENE_IDS){ const Sc=SCENES[id];
    gGeo.appendChild(slider('sep_'+id,SEPR[id][1],Sc.sepMin,Sc.sepMax,SEPR[id][0],v=>sigf(v,3)+' '+Sc.unit)); }
  const barrierChips=chipRow(BARRIER_LIST,'barrier'); gGeo.appendChild(barrierChips);
  const WR={water:[0.05,'slit width, cm (water)'],sound:[1,'slit width, cm (sound)'],light:[10,'slit width, nm']};
  const DR={water:[0.05,'slit separation, cm (water)'],sound:[1,'slit separation, cm (sound)'],light:[10,'slit separation, nm']};
  for(const id of SCENE_IDS){ const Sc=SCENES[id];
    gGeo.appendChild(slider('slitW_'+id,WR[id][1],Sc.slitWMin,Sc.slitWMax,WR[id][0],v=>sigf(v,3)+' '+Sc.unit));
    gGeo.appendChild(slider('slitD_'+id,DR[id][1],Sc.slitDMin,Sc.slitDMax,DR[id][0],v=>sigf(v,3)+' '+Sc.unit)); }
  gGeo.appendChild(slider('bcol','barrier position',BCOL_MIN,BCOL_MAX,1,v=>{ const Sc=SCENES[ST.scene]; return sigf((v-LAT.PAD+0.5)*sceneDx(Sc),3)+' '+Sc.unit; }));
  const geoTag=h('div',{class:'tag'}); gGeo.appendChild(geoTag);

  /* what to show */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  const lookChips=chipRow(SIDE_LIST,'look'); gShow.appendChild(lookChips);
  const soundChips=chipRow(SOUNDVIEW_LIST,'soundView'); gShow.appendChild(soundChips);
  const lightChecks=h('div',{class:'checks'},checkbox('screen','screen'),checkbox('inten','intensity graph'));
  gShow.appendChild(lightChecks);
  const showChecks=h('div',{class:'checks'},checkbox('graph','graph of the centre line'),checkbox('nodal','nodal lines (r₁ − r₂ = (m + ½)λ)'),
    checkbox('theory','theory: Rayleigh–Sommerfeld and Fraunhofer'));
  gShow.appendChild(showChecks);

  /* the tools */
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('tape','tape measure'),checkbox('watch','stopwatch'),checkbox('meter','wave meter')));
  const watchBtns=h('div',{class:'btnrow'},
    button('start / stop the stopwatch',()=>{ const R=cur(); if(R) R.watch.on=!R.watch.on; }),
    button('zero the stopwatch',()=>{ const R=cur(); if(R){ R.watch.t=0; } }));
  gTools.appendChild(watchBtns);
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  /* time */
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(chipRow(SPEED_LIST,'speed'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gTime.appendChild(h('div',{class:'btnrow'},
    button('one step',()=>{ const R=syncRun(ST.view); if(R) runStep(R); }),
    button('clear the waves',()=>{ const R=syncRun(ST.view); if(R) runClear(R); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  /* the far field */
  const gFar=h('div',{class:'grp'},h('h3',null,'the aperture and the laser'));
  gFar.appendChild(h('div',{class:'checks'},checkbox('laser','laser on')));
  gFar.appendChild(slider('lam','wavelength, nm',DIF.LAMMIN,DIF.LAMMAX,1,v=>fmt(v,0)+' nm'));
  gFar.appendChild(chipRow(AP_LIST,'ap'));
  const mm=v=>fmt(v,3)+' mm', R2=SLIDER_RANGE;
  const fsl=(k,lab,step2,f)=>gFar.appendChild(slider(k,lab,R2[k][0],R2[k][1],step2,f));
  fsl('ellD','diameter',0.005,mm); fsl('ellE','eccentricity',0.01,v=>fmt(v,2));
  fsl('recW','width',0.005,mm); fsl('recH','height',0.005,mm);
  fsl('csD','circle diameter',0.005,mm); fsl('csW','square width',0.005,mm);
  fsl('disD','circle diameter, disorder',0.005,mm); fsl('disP','lattice spacing',0.005,mm);
  fsl('disL','disorder',1,v=>DISORDER_NAMES[Math.round(v)]);
  fsl('figH','figure height',0.005,mm); fsl('figR','rotation',1,v=>fmt(v,0)+'°');
  fsl('gauSx','σ across',0.001,mm); fsl('gauSy','σ up',0.001,mm);
  fsl('sltN','number of slits',1,v=>fmt(v,0));
  fsl('sltW','slit width, far field',0.005,mm); fsl('sltD','slit separation, far field',0.005,mm);
  gFar.appendChild(chipRow(FARMODE_LIST,'farMode'));
  const farTag=h('div',{class:'tag'}); gFar.appendChild(farTag);

  /* path difference */
  const gPath=h('div',{class:'grp'},h('h3',null,'two sources, in wavelengths'));
  gPath.appendChild(slider('pd','separation d / λ',0.3,8,0.05,v=>fmt(v,2)));
  gPath.appendChild(slider('pL','screen distance L / λ',1,60,0.5,v=>fmt(v,1)));
  gPath.appendChild(h('div',{class:'checks'},checkbox('hyp','nodal hyperbolae'),checkbox('asym','their asymptotes')));

  /* the lattice */
  const gLat=h('div',{class:'grp'},h('h3',null,'the lattice'));
  gLat.appendChild(slider('latTh','direction θ for the readout',0,45,1,v=>fmt(v,0)+'°'));

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
      TOOLS.tape=JSON.parse(JSON.stringify(TOOLS0.tape)); TOOLS.probes=JSON.parse(JSON.stringify(TOOLS0.probes));
      resetRuns(); syncChips(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:CREDIT+' Measured: nothing — every number is PhET&rsquo;s (read from the minified original, cited as PhET&rsquo;s values in the header) or exact and pinned to build/wave-interference/derive.py (numpy twin, scipy). Colour: the CIE 1931 table.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gScene,gSrc,gGeo,gShow,gTools,gTime,gFar,gPath,gLat,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS) [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view, lat=!!LATTICE_VIEWS[v], sc=ST.scene;
    gScene.hidden=!(lat||v==='lattice');
    gSrc.hidden=!(lat||v==='lattice');
    for(const id of SCENE_IDS) rows['f_'+id].row.hidden=(id!==sc);
    for(const w of ['tank','two','slits']) rows['amp_'+w].row.hidden=(w!==v);
    waveChips.hidden=!(v==='tank'||v==='two');
    pulseBtn.hidden=!((v==='tank'||v==='two')&&ST.wave==='pulse');
    srcChecks.hidden=(v!=='two'); planeCheck.hidden=(v!=='slits'); srcTag.hidden=(v==='lattice');
    gGeo.hidden=!(v==='two'||v==='slits');
    for(const id of SCENE_IDS){ rows['sep_'+id].row.hidden=!(v==='two'&&id===sc);
      rows['slitW_'+id].row.hidden=!(v==='slits'&&id===sc&&ST.barrier!=='none');
      rows['slitD_'+id].row.hidden=!(v==='slits'&&id===sc&&ST.barrier==='two'); }
    barrierChips.hidden=(v!=='slits'); rows.bcol.row.hidden=!(v==='slits'&&ST.barrier!=='none');
    gShow.hidden=!lat;
    lookChips.hidden=!(lat&&sc==='water'); soundChips.hidden=!(lat&&sc==='sound'); lightChecks.hidden=!(lat&&sc==='light');
    rows.cb_nodal.row.hidden=(v!=='two'); rows.cb_theory.row.hidden=!(v==='two'||v==='slits');
    gTools.hidden=!lat; gTime.hidden=!lat;
    gFar.hidden=(v!=='far');
    const ap=ST.ap, show=(k,on)=>{ rows[k].row.hidden=!on; };
    show('ellD',ap==='ellipse'); show('ellE',ap==='ellipse'); show('recW',ap==='rect'); show('recH',ap==='rect');
    show('csD',ap==='cs'); show('csW',ap==='cs'); show('disD',ap==='disorder'); show('disP',ap==='disorder'); show('disL',ap==='disorder');
    show('figH',ap==='figure'); show('figR',ap==='figure'); show('gauSx',ap==='gauss'); show('gauSy',ap==='gauss');
    show('sltN',ap==='slits'); show('sltW',ap==='slits'); show('sltD',ap==='slits');
    gPath.hidden=(v!=='path'); gLat.hidden=(v!=='lattice');
    for(const k in rows) rows[k].sync();
    const R=cur();
    srcTag.innerHTML=v==='slits'?'PhET&rsquo;s plane wave: 0.21 &times; the amplitude, set on every cell left of the barrier'
      :(ST.wave==='pulse'?'a pulse is one period of the drive, then the source lets go':'the source cell is driven at 1.2 &times; the amplitude (PhET&rsquo;s values)');
    geoTag.innerHTML=v==='two'?'the sources sit on whole cells: the separation used is the nearest even number of cells'
      :'drag the barrier by its arrow; slits are the cells whose centres lie inside them';
    toolTag.innerHTML='drag the tape&rsquo;s ends and the probes on the picture'+(R&&ST.watch?(R.watch.on?' &middot; the stopwatch is running':' &middot; the stopwatch is stopped'):'');
    timeTag.innerHTML='space runs/pauses &nbsp; <b>r</b> clears the waves &nbsp; <b>p</b> fires a pulse &nbsp; 1&ndash;6 switch views';
    farTag.innerHTML=APERTURES.find(a=>a.id===ap).phet?(ap==='figure'?'PhET&rsquo;s waving girl is a photograph; this is a drawn figure':'one of PhET&rsquo;s five apertures')
      :'not in PhET: added for the closed-form check';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=LATTICE_VIEWS[ST.view]?'space pauses · r clears · drag the tools · 1–6 switch views':'1–6 switch views';
      infoEl.innerHTML=INFO[ST.view]||''; physEl.innerHTML=DERIV[ST.view]||'';
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
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); ST.running=!ST.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ const R=syncRun(ST.view); if(R){ runClear(R); dirty=true; refresh(); } }
    else if(e.key==='p'){ const R=syncRun(ST.view); if(R&&firePulse(R)){ dirty=true; refresh(); } }
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
      try{ S.draw(); if(advanced&&frameN%10===0){ const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); } }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  tank:'A ripple tank seen from above. A single source moves one cell of a 151 × 151 lattice up and down, and every other cell obeys the wave equation in its simplest discrete form: each step it accelerates toward the average of its four neighbours. That rule alone makes circular ripples spread from the source at a fixed speed, fading as 1/√r because their energy spreads round a growing circle. Choose water, sound or light: the lattice is the same, only the ruler and the clock change — 10 cm and seconds, 5 m and milliseconds, 5 µm and femtoseconds. Raise the frequency and the rings crowd together, because the speed is fixed and v = fλ. The tape measure, stopwatch and wave meter are there to check exactly that: measure a wavelength, time a period, multiply. For water, the side view shows the surface along the middle row; for sound, the air parcels crowd where the pressure is high; for light, the screen at the right edge collects the brightness.',
  two:'Two sources driven in step. Wherever the waves arrive together they add; wherever one arrives half a wavelength behind the other they cancel. The cancellation lines are the nodal lines, and each is a curve along which the path difference r₁ − r₂ is fixed at (m + ½)λ — a hyperbola with the two sources as its foci (dashed orange, drawn from the formula, not found in the picture). The lattice’s own nodal lines sit up to a cell or so outside them: a wave crossing the lattice obliquely has a slightly longer wavelength than one along an axis, and the two sources see each point at slightly different angles. Far away every hyperbola straightens into its asymptote, d sin θ = (m + ½)λ, which is the formula in the textbooks. Move the sources apart or raise the frequency and more nodal lines appear: one pair for every wavelength that fits into the separation. With light, the screen shows the fringes and the intensity graph compares them with the exact two-source formula.',
  slits:'A plane wave arrives from the left and meets a barrier. Only what passes the slits goes on, and — as Huygens said — every open cell of a slit acts as a new source. One slit spreads the light into a central band with dark bands at a sin θ = mλ; two slits add the two-source fringes inside that envelope, bright at d sin θ = mλ. The textbook formulas are far-field results and need the screen to be far compared with d²/λ. PhET’s light screen is not: at the default settings it sits about 2.5 µm behind slits 1.5 µm apart, where d²/λ is 4.4 µm. The intensity graph therefore compares the lattice with two predictions — the full Rayleigh–Sommerfeld sum over the open cells (solid orange), which the lattice follows to a few per cent, and the Fraunhofer formula (dashed), which it does not.',
  far:'The Fraunhofer, or far-field, pattern of an aperture is its two-dimensional Fourier transform, and that is how PhET computes it: a 256 × 256 picture of the aperture, a fast Fourier transform, the magnitude. Everything about diffraction is in that one sentence. A small hole makes a wide pattern; a circle makes the Airy rings, with the first dark ring at 1.22 λ/D; a rectangle makes a cross of sinc² fringes, wider along its narrow side; rotating the aperture rotates the pattern; a lattice of holes makes sharp spots, and disordering the lattice washes them into a halo whose shape is the pattern of a single hole. To keep one angular scale for every colour, PhET redraws the aperture magnified by λ₀/λ before the transform; the cut below the pictures is checked against the closed forms — Airy for the disc, sinc² for the rectangle, the Gaussian’s own transform — and the transform against a direct sum.',
  path:'The geometry behind the two-source pattern, with the wave equation taken out. A point in the plane is r₁ from one source and r₂ from the other; the waves arrive in antiphase where r₁ − r₂ is an odd number of half-wavelengths. A curve of constant difference in distance from two points is a hyperbola with those points as foci, so every nodal line is a hyperbola. Close to the sources the hyperbolae bend round them; far away each runs straight out along its asymptote, sin θ = Δ/d. That is why the far-field formula d sin θ = (m + ½)λ is only true far away: on a screen at distance L, the exact minima sit further out than the far-field ones by about ab/2L, and the difference matters when L is not large compared with d²/λ.',
  lattice:'Everything the first three views show rests on one rule — each cell moves toward the average of its neighbours — and this view shows what that rule does to a wave. On a lattice a wave with k cells per radian does not travel at exactly c: short waves lag, and they lag differently along the axes and along the diagonals. The dispersion relation sin²(ωΔt/2) = C²[sin²(kₓΔx/2) + sin²(k_yΔx/2)] says exactly how. PhET fixes one time step per medium, so its wavelengths come out 0.7 % to 3.2 % short; here the time step is solved from this relation at every frequency, so the wavelength and the period are exact along the lattice axes, and the residual error along the diagonals is the number printed in the readout. The edge of the lattice has to swallow waves rather than reflect them: Mur’s second-order boundary does it to 3 % up to 45°.'
};
function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  tank:'<h4>the lattice and its clock</h4>'
    +EQ(1,'u<sub>ij</sub><sup>n+1</sup> = 2u<sub>ij</sub><sup>n</sup> &minus; u<sub>ij</sub><sup>n&minus;1</sup> + C&sup2;(u<sub>i+1,j</sub> + u<sub>i&minus;1,j</sub> + u<sub>i,j+1</sub> + u<sub>i,j&minus;1</sub> &minus; 4u<sub>ij</sub>)<sup>n</sup>, &nbsp; C = '+FR('c&Delta;t','&Delta;x')+' = &frac12;')
    +EQ(2,'&Delta;x = W/111, &nbsp; N<sub>&lambda;</sub> = '+FR('v','f&Delta;x')+', &nbsp; &Omega; = &omega;&Delta;t = 2 asin(C sin(&pi;/N<sub>&lambda;</sub>)), &nbsp; &Delta;t = '+FR('&Omega;','2&pi;f'))
    +'<p>[2] is the dispersion relation solved for the step: a wave along an axis then has exactly N<sub>&lambda;</sub> cells per wavelength and exactly 2&pi;/&Omega; steps per period, so &lambda; = v/f and T = 1/f hold on the lattice, not just on paper. The source cell is set to 1.2 A sin(n&Omega;) after each step (PhET&rsquo;s 1.2); Mur&rsquo;s second-order condition on the outer ring absorbs what leaves.</p>'
    +'<div class="cite">pins: the numpy twin of the engine after 240 steps (water, one source), the calibration of all three media, the dispersion relation, Mur&rsquo;s |R| — derive.py</div>',
  two:'<h4>the nodal lines</h4>'
    +EQ(1,'r<sub>1</sub> &minus; r<sub>2</sub> = &Delta; &nbsp;&hArr;&nbsp; '+FR('y&sup2;','a&sup2;')+' &minus; '+FR('x&sup2;','b&sup2;')+' = 1, &nbsp; a = &Delta;/2, &nbsp; b&sup2; = d&sup2;/4 &minus; a&sup2;')
    +EQ(2,'&Delta; = (m + &frac12;)&lambda;, &nbsp; |&Delta;| &lt; d &nbsp;&rArr;&nbsp; <span class="rm">count</span> = 2&lceil;d/&lambda; &minus; &frac12;&rceil;')
    +EQ(3,'I &prop; '+FR('1','r<sub>1</sub>')+' + '+FR('1','r<sub>2</sub>')+' + '+FR('2 cos k(r<sub>1</sub> &minus; r<sub>2</sub>)','&radic;(r<sub>1</sub>r<sub>2</sub>)')+' &nbsp;<span class="rm">(each source e<sup>ikr</sup>/&radic;r)</span>')
    +'<p>The sources sit on whole cells, so the separation used is 2 round(s/2&Delta;x) &Delta;x, and the overlay uses that one. At steady state (two light sources, derive.py) the lattice&rsquo;s nodal lines lie 0.85 cells outside the hyperbolae on average, 1.4 at worst, always outward; the continuum formula [3] puts them within 0.08. The difference is the lattice&rsquo;s anisotropy: the phase is &int;k(&theta;)dr and k(&theta;) differs by about 1 % between the axis and the diagonal at 11 cells per wavelength.</p>'
    +'<div class="cite">pins: the twin with two sound sources after 240 steps; nodal counts; hyperbola and far-field screen positions; [3] at three points — derive.py</div>',
  slits:'<h4>the slits, near and far</h4>'
    +EQ(1,'<span class="rm">plane wave, left of the barrier:</span> u = 0.21 A sin(&Omega;n &minus; kx) &nbsp;<span class="rm">an exact lattice solution (derive.py: 5e-15)</span>')
    +EQ(2,'<span class="rm">Rayleigh&ndash;Sommerfeld (Dirichlet data on the barrier):</span> E(P) &prop; &Sigma;<sub>open</sub> '+FR('X','r')+' '+FR('e<sup>ikr</sup>','&radic;r'))
    +EQ(3,'<span class="rm">Fraunhofer:</span> I &prop; sinc&sup2;('+FR('&pi;a sin&theta;','&lambda;')+') cos&sup2;('+FR('&pi;d sin&theta;','&lambda;')+')')
    +'<p>At PhET&rsquo;s default the lattice screen follows [2] to 6 % (3 % rms) and misses [3] by 26 %: the first minimum is 10 rows from the centre on the lattice and in [2], 9 in [3].</p>'
    +'<div class="cite">pins: the twin with two light slits after 400 steps, its screen intensities; [2] and [3] at six rows; the steady-state comparison — derive.py</div>',
  far:'<h4>the transform</h4>'
    +EQ(1,'F(k<sub>1</sub>, k<sub>2</sub>) = &Sigma;<sub>i,j</sub> t<sub>ij</sub> e<sup>&minus;2&pi;i(k<sub>1</sub>i + k<sub>2</sub>j)/N</sup>, &nbsp; N = 256, &nbsp; &Delta;x = 1/192 mm')
    +EQ(2,'sin &theta; = k '+FR('&lambda;<sub>0</sub>','N&Delta;x')+' = 3.8328&times;10<sup>&minus;4</sup> k &nbsp;<span class="rm">(aperture drawn &times;&lambda;<sub>0</sub>/&lambda;, &lambda;<sub>0</sub> = 511.03 nm)</span>')
    +EQ(3,'<span class="rm">disc:</span> [2J<sub>1</sub>(v)/v]&sup2;, v = &pi;D sin&theta;/&lambda;; &nbsp; <span class="rm">rectangle:</span> sin(&pi;kM/N)/sin(&pi;k/N) &rarr; sinc; &nbsp; <span class="rm">Gaussian:</span> 2&pi;&sigma;<sub>x</sub>&sigma;<sub>y</sub>e<sup>&minus;2&pi;&sup2;&sigma;&sup2;f&sup2;</sup>')
    +'<p>The snapped rectangle transforms to the Dirichlet kernel exactly (1e-15); the sampled Gaussian to its continuous transform (5e-16); the drawn disc to the Airy pattern within 1.2&times;10<sup>&minus;3</sup> of the peak for k &le; 10, its first ring on bin 16 against the exact 16.26.</p>'
    +'<div class="cite">pins: eight apertures through numpy.fft.fft2 at six bins each; a direct DFT; J<sub>0</sub>, J<sub>1</sub>, sinc&sup2;, the Airy pattern against scipy — derive.py</div>',
  path:'<h4>the hyperbolae</h4>'
    +EQ(1,'y<sub>exact</sub> = a&radic;(1 + L&sup2;/b&sup2;), &nbsp; y<sub>far</sub> = L a/b = L tan(asin(&Delta;/d)), &nbsp; y<sub>exact</sub> &minus; y<sub>far</sub> &asymp; '+FR('ab','2L'))
    +EQ(2,'<span class="rm">far field when</span> L &#8811; d&sup2;/&lambda;')
    +'<div class="cite">pins: y<sub>exact</sub>, y<sub>far</sub> and r<sub>1</sub> &minus; r<sub>2</sub> on the hyperbola at four (d, &Delta;, L) — derive.py</div>',
  lattice:'<h4>the dispersion relation</h4>'
    +EQ(1,'sin&sup2;(&Omega;/2) = C&sup2;[sin&sup2;(k<sub>x</sub>/2) + sin&sup2;(k<sub>y</sub>/2)] &nbsp;&rArr;&nbsp; v<sub>g</sub> = &nabla;<sub>k</sub>&Omega; = '+FR('C&sup2;(sin k<sub>x</sub>, sin k<sub>y</sub>)','sin &Omega;'))
    +EQ(2,'<span class="rm">stable iff</span> 2C&sup2; &le; 1; &nbsp; <span class="rm">Mur:</span> u<sub>0</sub><sup>n+1</sup> = &minus;u<sub>1</sub><sup>n&minus;1</sup> + '+FR('C&minus;1','C+1')+'(u<sub>1</sub><sup>n+1</sup> + u<sub>0</sub><sup>n&minus;1</sup>) + '+FR('2','C+1')+'(u<sub>0</sub><sup>n</sup> + u<sub>1</sub><sup>n</sup>) + '+FR('C&sup2;','2(C+1)')+'&delta;<sub>y</sub>&sup2;(u<sub>0</sub> + u<sub>1</sub>)<sup>n</sup>')
    +'<p>Off the axes the group velocity is not parallel to k: at 30&deg; its size and its component along k differ in the fifth digit (derive.py).</p>'
    +'<div class="cite">pins: &Omega;(k), k(&Omega;, &theta;) by brentq, phase and group speeds, Mur |R| from the plane-wave ansatz (checked against a packet simulation to 2 %) — derive.py</div>'
};
