
/* ================================================================== *
 *  dispatch, the scene, boot -- the control panel, the tabs, the keys *
 *  and the frame loop                                                 *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; '+PHET_TITLE+' (University of '
  +'Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';
const BEAKER_VIEWS={beaker:1};
const CUVETTE_VIEWS={cuvette:1};

function layoutFor(rc,W,H){
  return beakerLayout(rc,W,H,CAP_BEAKER,CAP_BEAKER_S);
}
function drawView(rc,W,H,M){
  POLY_SEGS=[]; LEGEND_RECTS=[]; LABELS=[];
  /* The floating readout covers the top-right of the stage -- about 336 px wide and up to
     548 tall -- and it is HTML, so nothing on the canvas can see it.  Register it as an
     occupied label box so lab() dodges it (Known-bad: text placed at the top right of a
     plot box is text placed underneath the readout). */
  if(W>=900) LABELS.push([W-336,0,W,Math.min(548,H)]);
  rc.fillStyle='#070b18'; rc.fillRect(0,0,W,H);
  const m=M||buildModel();
  if(m.view==='beaker') viewBeaker(rc,W,H,m);
  else if(m.view==='cuvette') viewCuvette(rc,W,H,m);
  else if(m.view==='spectrum') viewSpectrum(rc,W,H,m);
  else if(m.view==='law') viewLaw(rc,W,H,m);
  else if(m.view==='ledger') viewLedger(rc,W,H,m);
  else if(m.view==='solutes') viewSolutes(rc,W,H,m);
  else viewColour(rc,W,H,m);
}
function makeScene(canvas){
  const S={W:0,H:0,
    model(){ return buildModel(); },
    draw(){
      /* fetch the context INSIDE the draw: one cached at boot writes into a recorder the
         DOM-stub harness has already thrown away (Known-bad, polyhedra.html) */
      const rc=canvas.getContext('2d');
      drawView(rc,S.W,S.H,S.model());
    },
    step(){ return stepFrame(); },
    pointer(kind,x,y){
      const rc=canvas.getContext('2d');
      if(BEAKER_VIEWS[ST.view]){
        const b=layoutFor(rc,S.W,S.H).bk;
        if(kind==='down'){
          const px=bkX(b,PROBE.x), py=bkY(b,PROBE.y);
          /* the probe body is 14 x 26 px; the grab box is a little larger than it */
          if(Math.abs(x-px)<=12&&y>=py-30&&y<=py+10){ DRAG.what='probe'; return true; }
          return false;
        }
        if(kind==='move'&&DRAG.what==='probe'){
          const p=bkFromCanvas(b,x,y);
          PROBE.x=clamp(p.x,-0.25,1.25);
          PROBE.y=clamp(p.y,-0.20,1.30);
          return true;
        }
      } else if(CUVETTE_VIEWS[ST.view]){
        const L=cuvetteLayout(rc,S.W,S.H);
        if(kind==='down'){
          const xR=L.X(L.CUV0+cuvetteWidth());
          if(Math.abs(x-xR)<=9){ DRAG.what='cuvette'; DRAG.grabX=x; DRAG.grabW=cuvetteWidth();
                                 return true; }
          const dx=L.X(L.CUV0+DET.x), dy=L.axis-DET.y*L.px;
          const sensor=Math.max(8,SENSOR_HALF*L.px);
          if(Math.abs(x-dx)<=12&&Math.abs(y-dy)<=sensor+6){ DRAG.what='detector'; return true; }
          return false;
        }
        if(kind==='move'&&DRAG.what==='cuvette'){
          ST.cuvette=clamp(DRAG.grabW+(x-DRAG.grabX)/L.px,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);
          return true;
        }
        if(kind==='move'&&DRAG.what==='detector'){
          DET.x=clamp(L.cmOf(x)-L.CUV0,-0.4,L.BENCH_CM-L.CUV0);
          DET.y=clamp((L.axis-y)/L.px,-2.4,2.4);
          return true;
        }
      }
      if(kind==='up'&&DRAG.what){
        /* PhET snaps the cuvette's width when the DRAG ENDS, not while it is moving */
        if(DRAG.what==='cuvette') ST.cuvette=snapCuvette(ST.cuvette);
        DRAG.what=null; return true;
      }
      return false;
    }};
  return S;
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

  /* the MESSAGE as well as the stack: JavaScriptCore's Error.stack carries only the
     frames, so a harness that reads the box alone was told where and not what */
  function fail(e){ errEl.style.display='block';
    errEl.textContent=String(e&&e.message||e)+'\n'+String(e&&e.stack||''); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    ST.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===ST.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:ST.view===k?'active':'',
    onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,setf,getf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:getf?getf():ST[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ const v=getf?getf():ST[key]; inp.value=v; val.textContent=plain(fmtf(v)); };
    inp.addEventListener('input',()=>{
      const v=parseFloat(inp.value);
      if(setf) setf(v); else ST[key]=v;
      syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=ST[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ ST[key]=inp.checked; if(onchg) onchg();
      syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=ST[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(ST[key]===o.id?' on':''),html:o.name,
        onclick:()=>{ if(onPick) onPick(o); else ST[key]=o.id; syncChips(); syncPanel();
                      dirty=true; refresh(); }}));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel();
    dirty=true; refresh(); }},lab2); }

  /* the solute */
  const gSolute=h('div',{class:'grp'},h('h3',null,'the solute'));
  gSolute.appendChild(chipRow(SOLUTE_LIST,'solute',o=>setSoluteId(o.id)));
  const soluteTag=h('div',{class:'tag'}); gSolute.appendChild(soluteTag);

  /* how it goes in, and what else moves */
  const gBeaker=h('div',{class:'grp'},h('h3',null,'the beaker'));
  gBeaker.appendChild(chipRow(FORM_LIST,'form'));
  gBeaker.appendChild(h('div',{class:'checks'},
    checkbox('shaking','shake the solid in (0.005 mol a grain)'),
    checkbox('dropper','squeeze the dropper (0.05 L/s of stock)'),
    checkbox('faucet','the water faucet runs (0.25 L/s)'),
    checkbox('drain','the drain is open (0.25 L/s)'),
    checkbox('running','time runs')));
  gBeaker.appendChild(slider('evap','evaporation, L/s',0,PHET.EVAPORATION_MAX,0.005,
    v=>fmt(v,3)+' L/s'));
  gBeaker.appendChild(slider('nSet','solute amount, mol',PHET.SOLUTE_MOL_MIN,
    PHET.SOLUTE_MOL_MAX,0.01,v=>fmt(v,2)+' mol',setMoles,()=>BK.n));
  gBeaker.appendChild(slider('vSet','solution volume, L',PHET.VOL_MIN,PHET.VOL_MAX,0.005,
    v=>fmt(v,3)+' L',setVolume,()=>BK.V));
  gBeaker.appendChild(h('div',{class:'btnrow'},
    button('empty',()=>emptyBeaker()),
    button('fill 1 L',()=>fillBeaker()),
    button('one step',()=>{ const w=ST.running; ST.running=true; stepFrame(); ST.running=w; })));
  const beakerTag=h('div',{class:'tag'}); gBeaker.appendChild(beakerTag);

  /* the meter and the beaker's own labels (PhET's checkboxes and unit preferences) */
  const gMeter=h('div',{class:'grp'},h('h3',null,'the meter'));
  gMeter.appendChild(chipRow(METER_LIST,'meterUnits'));
  gMeter.appendChild(chipRow(BEAKER_UNIT_LIST,'beakerUnits'));
  gMeter.appendChild(h('div',{class:'checks'},
    checkbox('showAmount','show solute amount'),
    checkbox('showVolume','show solution volume')));

  /* the Beer's Law bench */
  const gBench=SHOW_BEERS?h('div',{class:'grp'},h('h3',null,'the cuvette')):null;
  if(gBench){
    gBench.appendChild(chipRow(BLS_LIST,'blSolution',o=>setBlSolution(o.id)));
    gBench.appendChild(slider('blConc','concentration',0,1,0.001,
      v=>plain(blConcStr(ST.blConc)),
      v=>{ ST.blConc=v*currentBls().cMax; },()=>ST.blConc/currentBls().cMax));
    gBench.appendChild(slider('cuvette','path length l, cm',PHET.CUVETTE_MIN,
      PHET.CUVETTE_MAX,0.01,v=>fmt(v,2)+' cm'));
    gBench.appendChild(h('div',{class:'checks'},
      checkbox('lightOn','the light is on'),
      checkbox('snap','snap the cuvette to 0.1 cm on release')));
    gBench.appendChild(chipRow(MODE_LIST,'lightMode',o=>{
      ST.lightMode=o.id;
      if(o.id==='preset') ST.wavelength=presetWavelength(); }));
    gBench.appendChild(slider('wavelength','wavelength, nm',LAM0,LAM1,1,
      v=>fmt(v,0)+' nm'));
    gBench.appendChild(chipRow(DET_LIST,'detector'));
    const benchTag=h('div',{class:'tag'}); gBench.appendChild(benchTag);
    gBench._tag=benchTag;
  }

  /* the spectrum view's one option */
  const gSpec=SHOW_BEERS?h('div',{class:'grp'},h('h3',null,'the spectrum'),
    h('div',{class:'checks'},checkbox('allSpectra','all eight at once, on a log scale'))):null;
  /* the law view's axis */
  const gLaw=SHOW_BEERS?h('div',{class:'grp'},h('h3',null,'the law')):null;
  if(gLaw) gLaw.appendChild(chipRow(LAWX_LIST,'lawX'));

  /* the colour view */
  const gCol=h('div',{class:'grp'},h('h3',null,'the colour'));
  gCol.appendChild(chipRow(ILLUM_LIST,'illum'));
  if(!SHOW_BEERS)
    gCol.appendChild(slider('colourPath','path length, cm',0.05,5,0.05,v=>fmt(v,2)+' cm'));
  const colTag=h('div',{class:'tag'}); gCol.appendChild(colTag);

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
      resetBeaker();
      PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; DET.x=DET0.x; DET.y=DET0.y; DRAG.what=null; })));

  const SRC_LINE=CREDIT+' PhET&rsquo;s constants &mdash; the nine solutes (molar mass, stock '
    +'concentration, saturation point, colour stops), the eight Beer&rsquo;s Law solutions, '
    +'the eight molar-absorptivity spectra at one value per nanometre, the beaker&rsquo;s 1 L, '
    +'the 0&ndash;7 mol and 0&ndash;1 L ranges, the 0.5&ndash;2 cm cuvette and its 0.1 cm snap, '
    +'the flow rates and every decimal-place count &mdash; were read out of the minified '
    +'original, '+PHET_SRC+', by build/beers-law-lab/extract_phet.py and written into this '
    +'file by make_data.py: none was typed by hand. Literature (Wikipedia chemical infoboxes, '
    +'fetched 2026-09-22, quoted to their own precision): sucrose 342.297 g/mol, 2.01 g/mL '
    +'(20 &deg;C); Co(NO<sub>3</sub>)<sub>2</sub> 182.943, 84.03 g/100 mL (0 &deg;C); '
    +'CoCl<sub>2</sub> 129.839, 52.9 g/100 mL (20 &deg;C); K<sub>2</sub>Cr<sub>2</sub>O<sub>7</sub> '
    +'294.182, 15.1 g/100 g; K<sub>2</sub>CrO<sub>4</sub> 194.189, 65.0 g/100 mL; '
    +'NiCl<sub>2</sub> 129.5994, 67.5 g/100 mL (25 &deg;C); CuSO<sub>4</sub> 159.60, 201 g/L '
    +'(20 &deg;C); KMnO<sub>4</sub> 158.032, 76 g/L (25 &deg;C); NaCl 58.44, 360 g/L '
    +'(25 &deg;C). No molar-absorptivity literature value could be sourced offline, so '
    +'PhET&rsquo;s spectra stand alone and are labelled as PhET&rsquo;s. Colour: the CIE 1931 '
    +'2&deg; observer, DOI 10.25039/CIE.DS.xvudnb9b (ISO/CIE 11664-1:2019), at one row per '
    +'nanometre. Every reference value the suite asserts is a line of '
    +'build/beers-law-lab/refvals.txt, the output of derive.py.';
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:SRC_LINE}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the chemistry'),h('div',{id:'phys'}));
  const GROUPS=[gSolute,gBeaker,gMeter];
  if(gBench) GROUPS.push(gBench);
  if(gSpec) GROUPS.push(gSpec);
  if(gLaw) GROUPS.push(gLaw);
  GROUPS.push(gCol,gRun,gInfo,gPhys);
  GROUPS.forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS)
      [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view;
    const beakerish=(v==='beaker'||v==='ledger');
    gSolute.hidden=!(beakerish||v==='solutes'||(!SHOW_BEERS&&v==='colour'));
    gBeaker.hidden=!beakerish;
    gMeter.hidden=(v!=='beaker');
    if(gBench) gBench.hidden=!(v==='cuvette'||v==='spectrum'||v==='law'||v==='colour');
    if(gSpec) gSpec.hidden=(v!=='spectrum');
    if(gLaw) gLaw.hidden=(v!=='law');
    gCol.hidden=(v!=='colour');
    if(rows.wavelength) rows.wavelength.row.hidden=(ST.lightMode!=='variable');
    if(rows.shaking) rows.shaking.row=rows.shaking.row;
    if(rows.cb_shaking) rows.cb_shaking.row.hidden=(ST.form!=='solid');
    if(rows.cb_dropper) rows.cb_dropper.row.hidden=(ST.form!=='solution');
    for(const k in rows) rows[k].sync();
    soluteTag.innerHTML='PhET&rsquo;s nine, with PhET&rsquo;s molar masses, stock '
      +'concentrations and saturation points. Changing the solute empties the beaker &mdash; '
      +'it cannot hold two at once, which is PhET&rsquo;s rule too.';
    beakerTag.innerHTML='the beaker holds '+fmt(PHET.BEAKER_VOLUME,0)+' L and the solute '
      +'stops at '+fmt(PHET.SOLUTE_MOL_MAX,0)+' mol, both PhET&rsquo;s. <b>space</b> '
      +'runs/pauses &nbsp; <b>e</b> empties &nbsp; <b>f</b> fills &nbsp; 1&ndash;'
      +TABS.length+' switch views';
    if(gBench&&gBench._tag)
      gBench._tag.innerHTML=(ST.lightMode==='preset'
        ? 'preset: the light sits at this solution&rsquo;s &lambda;<sub>max</sub>, '
          +fmt(presetWavelength(),0)+' nm, which is where the reading is most sensitive.'
        : 'variable: the wavelength is yours. Away from the peak &epsilon; falls and the '
          +'absorbance falls with it &mdash; the law still holds exactly, at the &epsilon; '
          +'of wherever you are.')
        +' Drag the cuvette&rsquo;s right wall to change l; it snaps to 0.1 cm on release '
        +'(PhET&rsquo;s cuvetteSnapInterval).';
    colTag.innerHTML='the swatches are the same solution at rising concentration: PhET&rsquo;s '
      +'interpolation, and what '+(SHOW_BEERS?'the cuvette':'that depth of it')+' really '
      +'transmits. No D65 spectrum could be sourced offline, so the two illuminants are equal '
      +'energy (flat by definition) and CIE standard illuminant A (the CIE&rsquo;s own formula).';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=BEAKER_VIEWS[ST.view]
        ? 'drag the meter probe in and out of the solution · space pauses · e empties · 1–'+TABS.length+' switch views'
        : (CUVETTE_VIEWS[ST.view]
           ? 'drag the cuvette’s right wall, or the detector probe · 1–'+TABS.length+' switch views'
           : '1–'+TABS.length+' switch views');
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); ST.running=!ST.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='e'){ emptyBeaker(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='f'){ fillBeaker(); syncPanel(); dirty=true; refresh(); }
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
        if(advanced&&frameN%10===0){ const M=S.model();
          roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  beaker:'PhET\'s Concentration screen. Pick a solute, shake it in as a solid or squeeze it in as a ready-made stock solution, and the meter reads n/V. Then take the ratio apart. Open the water faucet and the concentration falls with nothing removed at all — the moles have not moved, the volume has. Open the drain and it does not fall at all, because draining takes solution, and solution carries solute away in exactly the proportion it is already in. Turn the evaporator up and the concentration rises, for the same reason in reverse, until the water runs out of room and solid appears on the bottom. That last point is the only place the model stops being a ratio: past n = V·Csat the solution holds Csat and no more, and the difference sits there as a precipitate. Sodium chloride is the one worth trying if you want to see how little colour tells you: it saturates at 6.15 mol/L and is almost invisible the whole way.',
  cuvette:'PhET\'s Beer\'s Law screen. The light source makes one wavelength, the cuvette holds the solution, the detector measures what comes out, and the whole screen is one equation: A = εlc. Everything it can do moves one of those three letters. The concentration slider moves c; the cuvette\'s right wall moves l (drag it — it snaps to a tenth of a centimetre when you let go, which is PhET\'s own snapInterval); switching the source from preset to variable moves ε, because ε is a property of the wavelength and not of the solution alone. The reading that matters is the absorbance, and the reason is on the picture: the beam past the cuvette dims by exactly the transmittance, and transmittance is what multiplies when you stack two cuvettes, while absorbance is what adds. Two 1 cm cuvettes of the same solution transmit T² and absorb 2A.',
  spectrum:'The ε in A = εlc is not a number, it is a curve, and these are PhET\'s eight of them at one value per nanometre. The preset wavelength every screen opens at is simply the highest point of the curve — that is what λmax means, and it is found here by scanning the four hundred and one samples rather than by being told. Two things are worth noticing. First, the absorbance curve underneath has the same shape as ε, because l and c only scale it: the law is exact at every wavelength separately, and a spectrum is the same arithmetic asked four hundred times. Second, copper sulfate\'s peak is at the very last sample, 780 nm, because its real absorption band is in the infrared and PhET\'s table stops where the eye does. No literature molar absorptivity could be sourced offline for any of these, so they are labelled as PhET\'s digitised data and nothing further is claimed for them.',
  law:'The reason a spectrophotometer reports absorbance and not the transmittance it actually measures. A is linear in c and linear in l, so it plots as a straight line through the origin whose slope carries ε — double the concentration and you double the number. T is 10^-A, which is a curve in both, and reading a concentration off it means reading a logarithm by eye. The third panel is the strongest statement in the view: T against A is the same curve for every solution that has ever existed, because there is nothing in it but A. An absorbance of 1 is ten per cent through, 2 is one per cent, 3 is a thousandth; past about 3 a real instrument is measuring its own stray light rather than the sample. The shaded band on the first panel is where the straight line stops being true — a real solution\'s ε drifts above roughly ten millimolar — and it is a teaching bound rather than a measurement, so it is drawn as a band and named.',
  ledger:'A beaker simulation is a bookkeeping problem before it is a chemistry problem, so this view does the books. Every mole that the shaker or the dropper puts in, and every mole the drain takes out, is counted; what is left must be what is in the beaker, and the residual under the bars is how much of that is not true. It is zero — not small, zero — and the Python twin closes the same ledger exactly in rationals over a nine-hundred-frame script. The drain is the one that catches people out: it removes solution, so it carries solute at the DISSOLVED concentration, which past saturation is Csat and not n/V, and the solid on the bottom does not go down it. The curve is the evaporator\'s path: hold the moles fixed and C = n/V is a hyperbola, rising as the water goes, until the volume reaches n/Csat exactly — and from there the concentration cannot rise at all, so everything further comes out as solid.',
  solutes:'PhET\'s nine solutes against what can be found out about them. The molar masses are the literature\'s to five decimal places, which is the check that PhET\'s data came from somewhere real: the worst disagreement over all nine is 5.6 parts in a hundred thousand, and the "drink mix" turns out to carry sucrose\'s molar mass to a milligram per mole, so it is sugar. The saturation points are the interesting column. Four of them — potassium chromate, potassium permanganate, nickel(II) chloride and potassium dichromate — land within a per cent of a solubility quoted at or near room temperature. The rest differ, and every one of those differences is explained by the temperature the source happens to quote: cobalt(II) nitrate\'s infobox gives 0 °C and 90 °C and nothing in between, so its bar is low by a quarter and should be. Where a source could not be made to say what PhET\'s number says, the table prints both rather than choosing.',
  colour:'PhET colours its solutions by interpolating between fixed stops — a sensible drawing decision, and not a calculation. This view does the calculation beside it. The solution transmits 10^(-ε(λ)lc) at every wavelength; integrate that against the CIE 1931 observer\'s three colour-matching functions on the very grid the spectra are tabulated on, and you have the tristimulus of the light that comes out. Adapt it so the illuminant alone renders white, and an empty cuvette is exactly rgb(255,255,255). The two rows are the same solutions at the same concentrations, and they are not the same colours: the worst single channel differs by a third to nine-tenths of the full range. The sharpest difference is not brightness, though. PhET\'s ramp has no path length in it at all, so it draws a thin cuvette and a thick one identically, while the real thing changes as the light has further to go. Cobalt(II) nitrate is the clearest case: PhET calls it red, and the calculation makes it magenta, because its absorption band sits in the green.'
};
function FR2(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV_CORE={
  ledger:'<h4>the beaker, as arithmetic</h4>'
    +EQ(1,'C = <span class="rm">min</span>(C<sub>sat</sub>, n/V), &nbsp; '
        +'<span class="rm">solid</span> = max(0, n &minus; V C<sub>sat</sub>)')
    +EQ(2,'n = &Sigma; in &minus; &Sigma; out, &nbsp; V = V<sub>0</sub> + &Sigma; in &minus; &Sigma; out')
    +EQ(3,'<span class="rm">drain:</span> &Delta;n = &minus;C &Delta;V &nbsp; '
        +'<span class="rm">(C, not n/V &mdash; the solid stays)</span>')
    +'<p>Five mechanisms move the two numbers, in PhET&rsquo;s own order: the solvent faucet, '
    +'the drain, the dropper, the evaporator, the shaker. Each returns what ACTUALLY moved, '
    +'so a clamp at the brim or at the 7 mol ceiling cannot open a hole in the books. '
    +'Evaporating holds n and shrinks V, so C climbs the hyperbola n/V until V = n/C<sub>sat</sub>; '
    +'past that the concentration is pinned and the excess is solid.</p>'
    +'<div class="cite">pins: a 900-frame script through every mechanism, run in doubles and '
    +'in exact rationals &mdash; both ledgers close, the rational one identically and the '
    +'double one to 0.0 mol and 0.0 L, agreeing to 4.4e-15 &mdash; derive.py</div>',
  beer:'<h4>Beer&ndash;Lambert</h4>'
    +EQ(1,'A = &epsilon;(&lambda;) l c, &nbsp; &epsilon; <span class="rm">in</span> '
        +'L mol<sup>&minus;1</sup> cm<sup>&minus;1</sup>, l <span class="rm">in cm</span>, '
        +'c <span class="rm">in mol/L</span>')
    +EQ(2,'<span class="hl">T = 10<sup>&minus;A</sup></span>, &nbsp; '
        +'A = &minus;log<sub>10</sub> T')
    +EQ(3,'<span class="rm">two cuvettes:</span> T<sub>1</sub>T<sub>2</sub>, &nbsp; '
        +'A<sub>1</sub> + A<sub>2</sub>')
    +'<p>[2] is what makes A the useful quantity: transmittance multiplies along the beam and '
    +'absorbance adds, so a length and a concentration both enter A linearly and neither enters '
    +'T linearly. &epsilon; is a LOOKUP here, not an interpolation &mdash; PhET indexes its '
    +'table by floor(&lambda; &minus; 380), so 500.0 nm and 500.9 nm give the same number.</p>'
    +'<div class="cite">pins: A against 50-digit decimal over 8 solutions &times; 4 path '
    +'lengths &times; 4 concentrations (2.7e-16), T on the same A (4.7e-16), the round trip '
    +'(1.4e-16), and the ln10&middot;A amplification of the end-to-end error &mdash; derive.py</div>',
  extremes:'<h4>both ends of the detector</h4>'
    +EQ(1,'A = 0 &rArr; T = 1 <span class="rm">exactly</span>; &nbsp; A = 1 &rArr; 10 %; '
        +'&nbsp; A = 2 &rArr; 1 %; &nbsp; A = 3 &rArr; 0.1 %')
    +EQ(2,'10<sup>&minus;A</sup> <span class="rm">underflows a double at</span> '
        +'<span class="hl">A = 324</span>, <span class="rm">where T is exactly 0</span>')
    +EQ(3,'&minus;log<sub>10</sub>(0) = &infin; &nbsp; <span class="rm">&mdash; a reading of '
        +'zero cannot be inverted</span>')
    +'<p>Both ends are asserted rather than assumed. The largest absorbance this bench can '
    +'reach is about 4 (2 cm of a full-scale solution), where 1 part in 10<sup>4</sup> gets '
    +'through; a real instrument would have stopped being honest well before that.</p>'
    +'<div class="cite">pins: T at A = 0, 1, 2, 3, 10; the underflow found by search, not '
    +'assumed; and that the value just below it is still positive &mdash; derive.py</div>',
  colour:'<h4>the colour that comes out</h4>'
    +EQ(1,'T(&lambda;) = 10<sup>&minus;&epsilon;(&lambda;) l c</sup>')
    +EQ(2,'X = &Sigma; S(&lambda;) T(&lambda;) x&#772;(&lambda;) &Delta;&lambda; &nbsp; '
        +'<span class="rm">(and Y, Z), &Delta;&lambda; = 1 nm over 380&ndash;780</span>')
    +EQ(3,'<span class="rm">RGB</span><sub>lin</sub> = M<sub>sRGB</sub>X / '
        +'M<sub>sRGB</sub>X<sub>w</sub> &nbsp; <span class="rm">&rArr; the illuminant is '
        +'exactly white</span>')
    +'<p>The CIE table is on the same 1 nm grid as the spectra, so [2] interpolates nothing. '
    +'[3] is a von Kries adaptation carried out in the display&rsquo;s own primaries, which '
    +'needs no white-point constant and makes an empty cuvette rgb(255,255,255) under either '
    +'illuminant. PhET&rsquo;s own colour is <i>not</i> this: it is a straight line in RGB '
    +'between two stops, with no path length in it at all.</p>'
    +'<div class="cite">pins: white under both illuminants; the worst channel gap per solution '
    +'(68&ndash;219 of 255); saturated KMnO<sub>4</sub> through 5 mm transmits 3.2e-10 of the '
    +'light and renders black &mdash; derive.py</div>',
  phet:'<h4>PhET&rsquo;s own drawing rules</h4>'
    +EQ(1,'<span class="rm">Concentration screen:</span> water &rarr; mid at c<sub>mid</sub> '
        +'&rarr; max at C<sub>sat</sub>, <span class="rm">channel-wise, FLOORED</span>')
    +EQ(2,'<span class="rm">Beer&rsquo;s Law screen:</span> water <span class="rm">at</span> '
        +'c = 0, <span class="rm">then</span> lo &rarr; hi <span class="rm">over</span> '
        +'[0, c<sub>max</sub>]')
    +EQ(3,'<span class="rm">grains a frame</span> = round(max(1, r &times; 200 &times; '
        +'&Delta;t)), &nbsp; <span class="rm">solid drawn as</span> round(200 &times; '
        +'<span class="rm">moles</span>)')
    +'<p>Color.interpolateRGBA uses Math.floor, not a rounding, so halfway from (224,255,255) '
    +'to (255,225,225) is (239,240,240). [2] has a step at c = 0: the ramp jumps from water to '
    +'its low stop the instant any solute is present, which is PhET&rsquo;s and is drawn rather '
    +'than smoothed. [3]&rsquo;s bracket is 0.667 at 60 frames a second, and the ROUNDING takes '
    +'that to one grain a frame: the shaker delivers <span class="warn">0.30 mol/s</span> '
    +'against its own nominal 0.20. The max(1, &hellip;) floor does nothing there and starts to '
    +'bite above about 80 fps, where the same shaker delivers <span class="warn">0.60 '
    +'mol/s</span>. Only a whole-second step gives the nominal rate.</p>'
    +'<div class="cite">pins: both interpolations at their stops and midpoints; the floor; the '
    +'step at zero; the grain count at 0, 1e-9, 0.0026 and 0.5 mol &mdash; derive.py</div>',
  data:'<h4>PhET&rsquo;s numbers against the sources</h4>'
    +EQ(1,'C<sub>sat</sub> = s / M, &nbsp; <span class="rm">s in g/L, M in g/mol</span>')
    +EQ(2,'<span class="rm">worst molar-mass gap over the nine:</span> '
        +'<span class="hl">5.6 &times; 10<sup>&minus;5</sup></span> <span class="rm">relative</span>')
    +EQ(3,'<span class="rm">K</span><sub>2</sub><span class="rm">CrO</span><sub>4</sub> '
        +'3.350 <span class="rm">vs</span> 3.347, &nbsp; KMnO<sub>4</sub> 0.480 '
        +'<span class="rm">vs</span> 0.481, &nbsp; NiCl<sub>2</sub> 5.210 '
        +'<span class="rm">vs</span> 5.208')
    +'<p>Every conversion assumes a litre of water makes a litre of solution, which is the same '
    +'displaced-volume assumption PhET makes and is worth at most a few per cent here. The four '
    +'solutes whose sources quote a room-temperature solubility agree with PhET to under a per '
    +'cent. The rest do not, and each gap is the temperature: cobalt(II) nitrate&rsquo;s only '
    +'usable figure is at 0 &deg;C.</p>'
    +'<div class="cite">sources: the Wikipedia chemical infoboxes, fetched 2026-09-22 and quoted '
    +'to their own printed precision. No literature molar absorptivity could be obtained, and '
    +'none is invented.</div>'
};
const DERIV={
  beaker:DERIV_CORE.ledger+DERIV_CORE.phet,
  cuvette:DERIV_CORE.beer+DERIV_CORE.extremes,
  spectrum:DERIV_CORE.beer+DERIV_CORE.data,
  law:DERIV_CORE.beer+DERIV_CORE.extremes,
  ledger:DERIV_CORE.ledger+DERIV_CORE.data,
  solutes:DERIV_CORE.data+DERIV_CORE.ledger,
  colour:DERIV_CORE.colour+DERIV_CORE.phet
};
