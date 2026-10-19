
/* ================================================================== *
 *  boot — the control panel, the tabs, the keys and the frame loop    *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Greenhouse Effect (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';

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
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:ST.view===k?'active':'',
    onclick:()=>setView(k)},lab2)); });

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
    inp.addEventListener('change',()=>{ ST[key]=inp.checked; if(onchg) onchg();
      syncPanel(); dirty=true; refresh(); });
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

  /* the atmosphere (PhET's concentration panel) */
  const gAtm=h('div',{class:'grp'},h('h3',null,'greenhouse gas'));
  const modeChips=chipRow(MODE_LIST,'mode'); gAtm.appendChild(modeChips);
  gAtm.appendChild(slider('conc','concentration c',0,1,0.005,v=>fmt(v,3)));
  const dateChips=chipRow(DATE_LIST,'date'); gAtm.appendChild(dateChips);
  gAtm.appendChild(h('div',{class:'checks'},checkbox('cloud','a cloud (reflects 12.5 %)')));
  const atmTag=h('div',{class:'tag'}); gAtm.appendChild(atmTag);

  /* the layer-model controls */
  const gLay=h('div',{class:'grp'},h('h3',null,'the sheets'));
  gLay.appendChild(slider('nLayers','absorbing sheets',0,GH.N_LM,1,v=>fmt(v,0)));
  gLay.appendChild(slider('absorb','infrared absorbance',GH.ABS_MIN,GH.ABS_MAX,0.05,v=>fmt(v,2)));
  gLay.appendChild(slider('intensity','solar intensity',GH.INT_MIN,GH.INT_MAX,0.25,
    v=>fmt(100*v,0)+' % of our sun'));
  gLay.appendChild(slider('albedo','surface albedo',GH.ALB_MIN,GH.ALB_MAX,0.05,v=>fmt(v,2)));
  const kirchBox=h('div',{class:'checks'},checkbox('kirch','sheet temperatures by Kirchhoff'));
  gLay.appendChild(kirchBox);
  const layTag=h('div',{class:'tag'}); gLay.appendChild(layTag);

  /* what to show */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(chipRow(UNIT_LIST,'unit'));
  const showChecks=h('div',{class:'checks'},
    checkbox('balance','energy balance at the top'),
    checkbox('flux','the flux meter'),
    checkbox('sheets','the sheet altitudes'),
    checkbox('morePhotons','more photons'));
  gShow.appendChild(showChecks);
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  /* time */
  const gTime=h('div',{class:'grp'},h('h3',null,'the sun and the clock'));
  gTime.appendChild(h('div',{class:'checks'},
    checkbox('sun','the sun shines',()=>{ if(!ST.sun) resetPhotons(); }),
    checkbox('running','time runs')));
  gTime.appendChild(h('div',{class:'btnrow'},
    button('one step',()=>{ const wasRun=ST.running; ST.running=true; stepFrame(); ST.running=wasRun; }),
    button('jump to equilibrium',()=>settle())));
  gTime.appendChild(h('div',{class:'btnrow'},
    button('cold start',()=>{ resetThermal(); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
      PROBE.z=PROBE0.z; DRAG.what=null; resetThermal(); syncChips(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:CREDIT+' PhET&rsquo;s constants (the sun&rsquo;s 343.6 W/m&sup2;, the albedos, the twelve sheets, a = 0.85&thinsp;c&thinsp;e<sup>&minus;z/8400&nbsp;m</sup>, the four dates and their CO<sub>2</sub>/CH<sub>4</sub>/N<sub>2</sub>O, the cloud&rsquo;s 12.5 %, the heat capacities) were read from the minified original, docs/phets/greenhouse-effect_en.html 1.3.13, and are cited as PhET&rsquo;s. Physics: &sigma; from scipy&rsquo;s CODATA (and from 2&pi;&#8309;k&#8308;/15h&sup3;c&sup2;), the 2015 IAU solar constant 1361 W/m&sup2;, Earth&rsquo;s Bond albedo 0.30, the conventional 288 K surface. Every reference value is a line of build/greenhouse-effect/refvals.txt, the output of derive.py.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gAtm,gLay,gShow,gTime,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS)
      [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view, conc=(v==='waves'||v==='photons'||v==='record'), lay=(v==='layers'||v==='ladder');
    gAtm.hidden=!conc; gLay.hidden=!lay;
    rows.conc.row.hidden=(ST.mode!=='value');
    dateChips.hidden=(ST.mode!=='date');
    rows.cb_cloud.row.hidden=(ST.mode!=='value');
    rows.cb_morePhotons.row.hidden=(v!=='photons');
    rows.cb_balance.row.hidden=!SKY_VIEWS[v];
    rows.cb_flux.row.hidden=!SKY_VIEWS[v];
    rows.cb_sheets.row.hidden=!SKY_VIEWS[v];
    showChecks.hidden=!SKY_VIEWS[v];
    kirchBox.hidden=(v!=='layers');
    gTime.hidden=!SKY_VIEWS[v];
    for(const k in rows) rows[k].sync();
    atmTag.innerHTML=ST.mode==='date'
      ? 'PhET&rsquo;s four dates set c to 0.625, 0.7147, 0.7182 and 0.7446. Those five numbers are a teaching fit, quoted here as PhET&rsquo;s; the ice age also switches the ground to its glaciated albedo, 0.225.'
      : 'c sets every sheet at once: a<sub>i</sub> = 0.85&thinsp;c&thinsp;e<sup>&minus;z<sub>i</sub>/8400&nbsp;m</sup>, so the lowest sheet does most of the work and the top one is nearly transparent.';
    layTag.innerHTML=(v==='ladder')
      ? 'these two set the magenta marker on the right-hand panel'
      : 'PhET&rsquo;s sheet absorbs a fraction a and radiates a full &sigma;T<sup>4</sup> each way. Kirchhoff&rsquo;s law would have it radiate a&thinsp;&sigma;T<sup>4</sup>; the fluxes are identical either way and the sheet temperatures differ by a<sup>&minus;1/4</sup>.';
    showTag.innerHTML=v==='photons'
      ? 'PhET draws one photon in five; &ldquo;more photons&rdquo; draws them all. The walk is seeded, so the picture repeats exactly.'
      : 'the flux meter&rsquo;s sensor is the magenta bar on the window &mdash; drag it up and down.';
    timeTag.innerHTML='the ground and the sheets are integrated with PhET&rsquo;s own heat capacities from a cold start; it takes about thirty seconds to settle. <b>space</b> runs/pauses &nbsp; <b>s</b> the sun &nbsp; <b>e</b> jumps to equilibrium &nbsp; 1&ndash;5 switch views';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=SKY_VIEWS[ST.view]
        ? 'drag the magenta flux sensor · space pauses · s switches the sun · 1–5 switch views'
        : '1–5 switch views';
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
    else if(e.key==='s'){ ST.sun=!ST.sun; if(!ST.sun) resetPhotons(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='e'){ settle(); dirty=true; refresh(); }
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
  waves:'The whole greenhouse effect in one picture. Sunlight arrives as visible light, and the gases that matter here — carbon dioxide, methane, nitrous oxide — are very nearly transparent to it, so it goes straight past them and warms the ground. The ground, being warm rather than hot, radiates back in the infrared, and to that the same gases are not transparent at all. Each sheet in the stack catches a fraction of it, warms, and radiates away exactly what it caught — but half of that goes back down. The ground therefore has to supply more than the sunlight alone would demand, and "more radiated" means "hotter". Set the concentration by hand, or pick one of PhET\'s four dates and watch the thermometer move. Nothing about the picture is a metaphor: the brightness of each infrared band is the flux the exact solution carries at that height, and it steps down by F·a/(2−a) every time it crosses a sheet.',
  photons:'The same physics, one photon at a time, because a flux is only a way of counting photons. Yellow ones fall from the sun; most are absorbed by the ground and a few bounce off it — that fraction is the albedo. Red ones leave the ground at a rate set by its temperature, and each time one crosses a sheet it is absorbed with probability a. It waits there and is then sent off again, up or down at even odds, having entirely forgotten which way it came. Some photons cross the whole stack at the first attempt; some are turned back and swallowed by the ground; the rest wander. The chance that any one of them ever reaches space is not a simulation result but a number you can write down — it is the flux ratio F/σTₛ⁴ — and the panel puts the measured fraction from twenty thousand seeded walks beside it. That is the sense in which the picture and the equation are the same thing.',
  layers:'PhET\'s Layer Model screen, with the metaphor made literal: panes of glass, transparent to sunlight and absorbing to infrared. Add one and the surface warms; add a second and it warms again, but by less. The arrows carry the actual fluxes. The reason the model closes is written along them: every sheet radiates away exactly what it absorbs, so the NET upward flux is the same at every height and must equal what the sun delivers — which leaves the upward flux itself stepping down by F·a/(2−a) at each sheet, and the ground having to supply all those steps at once. Turn the absorbance down and each sheet loses its grip fast: a pane that lets a tenth through is much more than a tenth worse. One honest footnote, which the tick box shows: PhET\'s sheet absorbs a fraction a but radiates a full σT⁴ each way, which is not Kirchhoff\'s law. It makes no difference whatever to the fluxes — only to the temperature you would write on each pane.',
  ladder:'One line runs through every screen of this sim. Because each sheet radiates away what it absorbs, the upward flux steps down by F·a/(2−a) at each of them, so the surface must radiate σTₛ⁴ = F[1 + Σ aᵢ/(2−aᵢ)]. For perfectly absorbing sheets that bracket is exactly N + 1, and the fourth root of it is the famous ladder: one sheet is 2^(1/4) = 1.19 times the bare effective temperature, four sheets 5^(1/4) = 1.50, twelve sheets only 13^(1/4) = 1.90. Radiation is a fourth-power law, and that is why a runaway is hard: doubling the trapping does not double the temperature. The right-hand panel is the other half — how much a sheet is worth when it is not perfect. The real Earth sits at about two thirds of one perfect sheet, or a single pane with a ≈ 0.78, which is a reasonable thing to know about the planet.',
  record:'Where PhET\'s numbers come from, and what they are worth. Everything that turns a greenhouse-gas concentration into an absorbance is a fit: aᵢ = 0.85·c·e^(−z/8400 m) on twelve sheets, with the four dates mapped to c = 0.625, 0.7147, 0.7182 and 0.7446. There is no spectroscopy in it — no line strengths, no bands, no overlap, no water vapour — and the honest way to present it is to say so and then solve it exactly, which is what the curve is. Doing that shows what PhET tuned and what it did not. The absolute level is about 8.5 K above the real Earth: PhET\'s 1750 is 296.5 K against the observed 288 K. The differences, though, are good — the ice age comes out 6.3 K colder than 1750 against about 6 K observed, and 2020 comes out 1.3 K warmer against about 1.2 K observed. That is a defensible teaching choice, and it is the kind of thing a reader should be told rather than left to discover.'
};
function FR2(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  waves:'<h4>the stack, solved</h4>'
    +EQ(1,'U<sub>i</sub> = (1&minus;a<sub>i</sub>)U<sub>i&minus;1</sub> + J<sub>i</sub>, &nbsp; D<sub>i&minus;1</sub> = (1&minus;a<sub>i</sub>)D<sub>i</sub> + J<sub>i</sub>, &nbsp; 2J<sub>i</sub> = a<sub>i</sub>(U<sub>i&minus;1</sub> + D<sub>i</sub>)')
    +EQ(2,'&rArr; &nbsp; U<sub>i</sub> &minus; D<sub>i</sub> = F <span class="rm">at every height</span> &nbsp;&rArr;&nbsp; U<sub>i</sub> = U<sub>i&minus;1</sub> &minus; F '+FR2('a<sub>i</sub>','2 &minus; a<sub>i</sub>'))
    +EQ(3,'&sigma;T<sub>s</sub><sup>4</sup> = U<sub>0</sub> = F[1 + &Sigma;<sub>i</sub> a<sub>i</sub>/(2 &minus; a<sub>i</sub>)], &nbsp; F = (1&minus;&alpha;)S')
    +'<p>[2] is the whole trick: each sheet emits exactly what it absorbs, so the net upward flux has nowhere to go and is the same at every level &mdash; and at the top, where nothing comes down, it equals F. Putting D<sub>i</sub> = U<sub>i</sub> &minus; F back into [1] leaves a first-order recursion with no unknowns in it. PhET&rsquo;s concentration screens put twelve sheets at z<sub>i</sub> = 50i/13 km with a<sub>i</sub> = 0.85&thinsp;c&thinsp;e<sup>&minus;z<sub>i</sub>/8400 m</sup>.</p>'
    +'<div class="cite">pins: the closed form against a dense linear solve of [1] over 151 stacks; energy balance at every sheet, the ground and the top to 1e-9 W/m&sup2;; a march of PhET&rsquo;s own layer ODE to the same answer &mdash; derive.py</div>',
  photons:'<h4>the random walk, and why it gives the same number</h4>'
    +EQ(1,'p<sub>i</sub> = [(1&minus;a<sub>i</sub>) + a<sub>i</sub>/2]&thinsp;p<sub>i+1</sub> + (a<sub>i</sub>/2)&thinsp;q<sub>i&minus;1</sub>, &nbsp; q<sub>i</sub> = [(1&minus;a<sub>i</sub>) + a<sub>i</sub>/2]&thinsp;q<sub>i&minus;1</sub> + (a<sub>i</sub>/2)&thinsp;p<sub>i+1</sub>')
    +EQ(2,'p<sub>N+1</sub> = 1 <span class="rm">(space)</span>, &nbsp; q<sub>0</sub> = 0 <span class="rm">(the ground absorbs all infrared)</span>')
    +EQ(3,'p<sub>1</sub> = '+FR2('F','&sigma;T<sub>s</sub><sup>4</sup>')+' = '+FR2('1','1 + &Sigma;<sub>i</sub> a<sub>i</sub>/(2 &minus; a<sub>i</sub>)'))
    +'<p>[3] is not an approximation and not a coincidence. In the steady state the ground radiates &sigma;T<sub>s</sub><sup>4</sup> and exactly F of it leaves the planet, so the escape fraction of a photon <em>is</em> the flux ratio. The sim solves [1]&ndash;[2] as a linear system, and separately walks twenty thousand photons with a 32-bit generator whose stream Python reproduces bit for bit; the two agree to within the binomial error of the sample.</p>'
    +'<div class="cite">pins: the Markov solution against F/&sigma;T<sub>s</sub><sup>4</sup> at four stacks; the Monte Carlo against it within 4&sigma;; the up/down split at 1/2; the generator&rsquo;s first six values &mdash; derive.py</div>',
  layers:'<h4>one sheet, and PhET&rsquo;s convention</h4>'
    +EQ(1,'<span class="rm">N sheets, all absorbance a:</span> &nbsp; &sigma;T<sub>s</sub><sup>4</sup> = F[1 + N a/(2&minus;a)] &nbsp;&rarr;&nbsp; F(N+1) <span class="rm">at</span> a = 1')
    +EQ(2,'<span class="rm">PhET:</span> J<sub>i</sub> = &sigma;T<sub>i</sub><sup>4</sup> <span class="rm">with</span> a<sub>i</sub>(U+D) = 2&sigma;T<sub>i</sub><sup>4</sup>; &nbsp; <span class="rm">Kirchhoff:</span> J<sub>i</sub> = a<sub>i</sub>&sigma;T<sub>i</sub><sup>4</sup> <span class="rm">with</span> a<sub>i</sub>(U+D) = 2a<sub>i</sub>&sigma;T<sub>i</sub><sup>4</sup>')
    +EQ(3,'<span class="rm">both give</span> J<sub>i</sub> = a<sub>i</sub>(U+D)/2 &nbsp;&rArr;&nbsp; <span class="rm">identical fluxes,</span> T<sub>Kirchhoff</sub> = a<sup>&minus;1/4</sup>T<sub>PhET</sub>')
    +'<p>[3] is worth stating because it looks as though it should matter and does not. What leaves a sheet is set by what it absorbs, whatever the emissivity; the emissivity only decides what temperature the sheet has to sit at to emit that much. PhET&rsquo;s temperatures are therefore too low by a<sup>&minus;1/4</sup> &mdash; 19 % at a = 0.5, 50 % at a = 0.2 &mdash; while every flux, and the surface temperature, are right. The tick box shows both.</p>'
    +'<div class="cite">pins: the a<sup>&minus;1/4</sup> ratio at three absorbances; the ladder at every N from 0 to 12; the law at 24 (N, a) pairs; PhET&rsquo;s heat capacities and the integrator&rsquo;s stability bound &mdash; derive.py</div>',
  ladder:'<h4>why the fourth root</h4>'
    +EQ(1,'&sigma;T<sub>s</sub><sup>4</sup> = F(N+1) &nbsp;&rArr;&nbsp; T<sub>s</sub> = T<sub>eff</sub>(N+1)<sup>1/4</sup>, &nbsp; T<sub>eff</sub> = (F/&sigma;)<sup>1/4</sup>')
    +EQ(2,'<span class="rm">Earth:</span> F = (1&minus;&alpha;)S<sub>0</sub>/4 = 238.175 W/m&sup2; &nbsp;&rArr;&nbsp; T<sub>eff</sub> = 254.578 K, &nbsp; <span class="rm">observed</span> 288 K')
    +EQ(3,'&Sigma; = (288/254.578)<sup>4</sup> &minus; 1 = 0.638 &nbsp;&rArr;&nbsp; <span class="rm">one sheet at</span> a = 2&Sigma;/(1+&Sigma;) = 0.779')
    +'<p>[2] uses the 2015 IAU nominal solar irradiance and the textbook Bond albedo 0.30; NASA&rsquo;s 0.306 moves T<sub>eff</sub> to 254.03 K. The factor of 4 is geometry: the Earth intercepts &pi;R&sup2; of the beam and radiates from 4&pi;R&sup2;. [3] is the honest summary of the real atmosphere in this model&rsquo;s language &mdash; two thirds of one perfect pane &mdash; and it is why a stack of twelve is a teaching device and not a planet.</p>'
    +'<div class="cite">pins: &sigma; from scipy&rsquo;s CODATA and from 2&pi;&#8309;k&#8308;/15h&sup3;c&sup2;; T<sub>eff</sub> at both albedos; the ladder at N = 0&hellip;12 and the law at 24 (N, a) pairs &mdash; derive.py</div>',
  record:'<h4>PhET&rsquo;s fit, and what it is worth</h4>'
    +EQ(1,'a<sub>i</sub> = 0.85&thinsp;c&thinsp;e<sup>&minus;z<sub>i</sub>/8400 m</sup>, &nbsp; z<sub>i</sub> = 50i/13 km, &nbsp; i = 1&hellip;12')
    +EQ(2,'c = 0.625 / 0.7147 / 0.7182 / 0.7446 &nbsp;&rarr;&nbsp; T<sub>s</sub> = 290.19 / 296.48 / 296.64 / 297.81 K')
    +EQ(3,'&Delta;T<sub>ice age</sub> = &minus;6.29 K <span class="rm">(observed &minus;6 K)</span>, &nbsp; &Delta;T<sub>2020</sub> = +1.32 K <span class="rm">(observed +1.2 K)</span>')
    +'<p>[1] is a shape, not a spectrum: an exponential in altitude with the 8.4 km scale height of the atmosphere itself, scaled by a single number. That the answer sits 8.5 K above the real Earth is the price; that [3] comes out right is what PhET bought with it. One independent check that this file really does reproduce PhET&rsquo;s model rather than a look-alike: the hottest state its concentration screens can reach is 309.13 K by this solve, and PhET hard-codes 309 K as its thermometer&rsquo;s expected maximum.</p>'
    +'<div class="cite">pins: the four dates&rsquo; absorbances and temperatures; the concentration sweep with and without the cloud; the hottest and coldest reachable states; the cloud&rsquo;s 0.125 &mdash; derive.py</div>'
};
