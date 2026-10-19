
/* ================================================================== *
 *  dispatch, the scene, boot — the control panel, the tabs, the keys  *
 *  and the frame loop                                                 *
 * ================================================================== */
const CREDIT='Remake of PhET Interactive Simulations&rsquo; pH Scale (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.';
const BEAKER_VIEWS={beaker:1, particles:1};

function layoutFor(rc,W,H){
  return ST.view==='particles'?beakerLayout(rc,W,H,CAP_PART,CAP_PART_S)
                              :beakerLayout(rc,W,H,CAP_BEAKER,CAP_BEAKER_S);
}
function drawView(rc,W,H,M){
  POLY_SEGS=[]; LEGEND_RECTS=[]; LABELS=[];
  /* The floating readout covers the top-right of the stage — about 336 px wide and up to
     548 tall — and it is HTML, so nothing on the canvas can see it.  Register it as an
     occupied label box so lab() dodges it (Known-bad: text placed at the top right of a
     plot box is text placed underneath the readout). */
  if(W>=900) LABELS.push([W-336,0,W,Math.min(548,H)]);
  rc.fillStyle='#070b18'; rc.fillRect(0,0,W,H);
  const m=M||buildModel();
  if(m.view==='beaker') viewBeaker(rc,W,H,m);
  else if(m.view==='particles') viewParticles(rc,W,H,m);
  else if(m.view==='graph') viewGraph(rc,W,H,m);
  else if(m.view==='my') viewMy(rc,W,H,m);
  else if(m.view==='dilution') viewDilution(rc,W,H,m);
  else viewScale(rc,W,H,m);
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
      if(!BEAKER_VIEWS[ST.view]) return false;
      const rc=canvas.getContext('2d');
      const L=layoutFor(rc,S.W,S.H), bk=L.bk;
      if(kind==='down'){
        const px=bkX(bk,PROBE.x), py=bkY(bk,PROBE.y);
        /* the probe body is 10 x 23 px; the grab box is a little larger than it */
        if(Math.abs(x-px)<=11&&y>=py-24&&y<=py+12){ DRAG.what='probe'; return true; }
        return false;
      }
      if(kind==='move'&&DRAG.what==='probe'){
        const p=bkFromCanvas(bk,x,y);
        PROBE.x=clamp(p.x,-0.25,1.25);
        PROBE.y=clamp(p.y,-0.20,1.30);
        return true;
      }
      if(kind==='up'&&DRAG.what){ DRAG.what=null; return true; }
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
  function slider(key,lab2,lo,hi,step2,fmtf,setf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:ST[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=ST[key]; val.textContent=plain(fmtf(ST[key])); };
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
        onclick:()=>{ ST[key]=o.id; if(onPick) onPick(o); syncChips(); syncPanel();
                      dirty=true; refresh(); }}));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel();
    dirty=true; refresh(); }},lab2); }

  /* the liquid */
  const gLiq=h('div',{class:'grp'},h('h3',null,'the liquid in the dropper'));
  gLiq.appendChild(chipRow(SOLUTE_LIST,'solute'));
  const liqTag=h('div',{class:'tag'}); gLiq.appendChild(liqTag);

  /* the beaker */
  const gBk=h('div',{class:'grp'},h('h3',null,'the beaker'));
  gBk.appendChild(slider('vSolute','liquid poured, L',0,PHET.BEAKER_VOLUME,0.005,
    v=>fmt(v,2)+' L',setSolute));
  gBk.appendChild(slider('vWater','water added, L',0,PHET.BEAKER_VOLUME,0.005,
    v=>fmt(v,2)+' L',setWater));
  gBk.appendChild(h('div',{class:'checks'},
    checkbox('pourSolute','the dropper pours (0.05 L/s)'),
    checkbox('pourWater','the water faucet runs (0.25 L/s)'),
    checkbox('drain','the drain is open (0.25 L/s)'),
    checkbox('running','time runs')));
  gBk.appendChild(h('div',{class:'btnrow'},
    button('autofill 0.5 L',()=>autofill()),
    button('empty',()=>emptyBeaker()),
    button('one step',()=>{ const w=ST.running; ST.running=true; stepFrame(); ST.running=w; })));
  const bkTag=h('div',{class:'tag'}); gBk.appendChild(bkTag);

  /* the dilution law */
  const gLaw=h('div',{class:'grp'},h('h3',null,'the dilution law'));
  gLaw.appendChild(chipRow(LAW_LIST,'law'));
  const lawTag=h('div',{class:'tag'}); gLaw.appendChild(lawTag);

  /* my solution */
  const gMy=h('div',{class:'grp'},h('h3',null,'my solution'));
  gMy.appendChild(slider('ph','pH',PHET.PH_MIN,PHET.PH_MAX,0.01,v=>fmt(v,2)));
  gMy.appendChild(slider('vMy','volume, L',PHET.MY_VOL_MIN,PHET.BEAKER_VOLUME,0.01,
    v=>fmt(v,2)+' L'));
  const myTag=h('div',{class:'tag'}); gMy.appendChild(myTag);

  /* the graph */
  const gGr=h('div',{class:'grp'},h('h3',null,'the graph'));
  gGr.appendChild(chipRow(UNIT_LIST,'units'));
  gGr.appendChild(chipRow(SCALE_LIST,'scaleKind'));
  gGr.appendChild(slider('linExp','linear top, 10^',PHET.LIN_EXP_MIN,PHET.LIN_EXP_MAX,1,
    v=>'8e'+fmt(v,0)));
  const grTag=h('div',{class:'tag'}); gGr.appendChild(grTag);

  /* what to show */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'),
    h('div',{class:'checks'},
      checkbox('ratio','the dot ratio, in the beaker'),
      checkbox('counts','the molecule counts')));

  const gRun=h('div',{class:'grp'},h('div',{class:'btnrow'},
    button('reset all',()=>{ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
      PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; DRAG.what=null; })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:CREDIT+' PhET&rsquo;s constants (the twelve liquids and their pH values and colours, the beaker&rsquo;s 1.2 L, the flow rates, the graph&rsquo;s decades, the particle rule, the colour law&rsquo;s 0.25 stop) were read from the minified original, docs/phets/ph-scale_en.html 1.7.6, and are cited as PhET&rsquo;s. Chemistry: K<sub>w</sub> = 1.00&times;10<sup>&minus;14</sup> at 25 &deg;C by convention, N<sub>A</sub> = 6.02214076&times;10<sup>23</sup> (SI 2019, exact; PhET uses 6.023&times;10<sup>23</sup>). Measured pH ranges, four of the twelve: blood 7.37&ndash;7.43 (Merck Manual Professional, &ldquo;Acid-Base Regulation&rdquo;, J. L. Lewis III); orange juice 3.30&ndash;4.19, milk 6.40&ndash;6.80, chicken broth 5.80 (FDA, &ldquo;Approximate pH of Foods and Food Products&rdquo;). No range could be sourced for the other eight and none was invented. Every reference value is a line of build/ph-scale/refvals.txt, the output of derive.py.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the chemistry'),h('div',{id:'phys'}));
  const GROUPS=[gLiq,gBk,gLaw,gMy,gGr,gShow,gRun,gInfo,gPhys];
  GROUPS.forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS)
      [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===ST[key]?' on':''));
  }
  function syncPanel(){
    const v=ST.view;
    const beakerish=(v==='beaker'||v==='particles'||v==='graph');
    gLiq.hidden=!(beakerish||v==='dilution'||v==='scale'||v==='liquids');
    gBk.hidden=!beakerish;
    gLaw.hidden=!(beakerish||v==='dilution');
    gMy.hidden=(v!=='my');
    gGr.hidden=(v!=='graph');
    gShow.hidden=(v!=='particles');
    if(rows.linExp) rows.linExp.row.hidden=(ST.scaleKind!=='linear');
    for(const k in rows) rows[k].sync();
    liqTag.innerHTML=v==='dilution'
      ? 'the chip picks which stock solution the curves are drawn for'
      : 'PhET&rsquo;s twelve, with PhET&rsquo;s pH values. Four of them carry a measured range with a source; the other eight do not, and the scale view draws that difference.';
    bkTag.innerHTML='the beaker holds '+fmt(PHET.BEAKER_VOLUME,1)+' L, so pushing one volume past the brim pushes the other down. <b>space</b> runs/pauses &nbsp; <b>a</b> autofills &nbsp; <b>e</b> empties &nbsp; 1&ndash;'+TABS.length+' switch views';
    lawTag.innerHTML=ST.law==='phet'
      ? 'PhET&rsquo;s rule: mix the MAJORITY ion linearly and take a log. It never re-solves, so water&rsquo;s own autoionisation is counted on one side and dropped on the other.'
      : 'exact: average the net strong acid C = [H<sub>3</sub>O<sup>+</sup>] &minus; [OH<sup>&minus;</sup>], whose moles are conserved, then re-solve [H<sub>3</sub>O<sup>+</sup>] &minus; K<sub>w</sub>/[H<sub>3</sub>O<sup>+</sup>] = C.';
    myTag.innerHTML='PhET&rsquo;s range is &minus;1 to 15 and its volume 0.01 to 1.2 L. Nothing is mixed here; the concentrations are read straight off the pH.';
    grTag.innerHTML=ST.scaleKind==='linear'
      ? 'the linear scale can hold one pair of numbers at a time &mdash; that is the lesson, not a limitation of the drawing'
      : 'PhET&rsquo;s logarithmic scale runs from 10<sup>&minus;16</sup> to 10<sup>2</sup> mol/L, eighteen decades';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=BEAKER_VIEWS[ST.view]
        ? 'drag the meter probe in and out of the liquid · space pauses · a autofills · 1–'+TABS.length+' switch views'
        : '1–'+TABS.length+' switch views';
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
    else if(e.key==='a'){ autofill(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='e'){ emptyBeaker(); syncPanel(); dirty=true; refresh(); }
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
  beaker:'PhET\'s Macro screen. Pick a liquid, squeeze the dropper, and the beaker fills with it; open the tap and it dilutes; open the drain and it empties without changing its pH at all, because draining removes solution and not solute. The meter reads only when its probe is in the liquid — drag it out and it says so rather than inventing a number, which is what a real meter measuring air would tell you. The one thing worth watching is how little the pH moves as you dilute: orange juice at pH 3.5 poured to 0.1 L and then filled to the brim ends at 4.58, because twelve times less acid is only 1.08 units of pH, and pH is a logarithm. Every liquid here is modelled as a strong acid or base of PhET\'s stated pH — fully dissociated, unbuffered. That is PhET\'s model too, and it is a fiction for blood, which is a bicarbonate buffer and hardly moves.',
  particles:'The same beaker with the ions drawn, which is PhET\'s Micro screen. Two numbers are worth separating here. The DOTS are a drawing rule: fifty of each at pH 7, scaling with the true concentration inside pH 6 to 8, and outside that window the minority is ramped up to three thousand while the majority is held down, because the real ratio cannot be drawn. At pH 13 the picture shows 457 hydroxide for every hydronium; the truth is a million million to one. The MOLECULE COUNTS, which the readout prints and the tick box puts on the canvas, are real: 7.23 × 10^16 hydronium ions in 1.2 L of neutral water, which is a hundred million billion of them, and it is that number — not the dots — that makes "pure water" a chemically busy place.',
  graph:'PhET\'s concentration graph, and the reason it defaults to a logarithmic scale. Water sits at 55 mol/L. The two ions, at neutrality, sit at 10^-7. That is more than eight decades between them, and at the ends of the scale the gap opens to eighteen. Switch to the linear scale and watch what happens: whichever ion is in the minority simply disappears, and the water goes off the top unless the exponent is wound all the way up. That failure is the lesson. The other thing to try is the units switch: moles instead of moles per litre multiplies all three bars by the volume, which moves them together and leaves every ratio — and the pH — exactly where it was. Concentration is what sets the pH; how much of it you have is a different question.',
  my:'PhET\'s third screen, where you set the pH directly instead of mixing anything. The two concentrations then follow from one definition and one equilibrium constant, and they are not independent: their product is Kw at every setting, so on logarithmic axes the whole of chemistry available at 25 °C is a single straight line of slope −1. The marker slides along it and cannot come off. That is a stronger statement than "pH + pOH = 14" looks: it says that fixing one ion fixes the other, and that a solution cannot be made both strongly acidic and rich in hydroxide. The volume slider changes the molecule counts and nothing else — the marker does not move, because concentration is intensive.',
  dilution:'This is the view that decides whether a pH simulation is honest. Diluting is mixing, mixing conserves MOLES, and the thing whose moles are conserved is the net strong acid C = [H3O+] − [OH−] — a difference of analytical concentrations, in which the spectator ions cancel. Water carries exactly none of it. So dilute f-fold and C is divided by exactly f; then the pH comes from re-solving the water equilibrium, [H3O+] − Kw/[H3O+] = C, which is what stops a diluted acid from ever crossing neutrality. The dashed line is the tempting shortcut of averaging the pH, and it is wrong by up to 4.4 units. PhET does something much better but not exact: it mixes the majority ion linearly, which counts water\'s autoionisation on one side and drops it on the other. Its error peaks at about 0.095 pH near pH 5 and 9, and vanishes both undiluted and at infinite dilution.',
  scale:'The twelve liquids on the scale they belong to, and underneath, what that scale actually is. Each step of one pH unit is a factor of ten in the hydronium concentration and a factor of ten the other way in the hydroxide, so on a logarithmic axis the two are straight lines of slope ∓1 crossing at pH 7. Everything else on the picture follows from that crossing. The orange bars are measured ranges — real ones, from the sources named at the foot of the panel — and there are only four of them, because those are the four that could be sourced cleanly here. PhET\'s value falls inside all four, which is a small but genuine check on its data. The other eight liquids are drawn with no bar at all rather than given a range that nobody measured.'
};
function FR2(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV_CORE={
  ions:'<h4>the two ions</h4>'
    +EQ(1,'['+H3O+'] = 10<sup>&minus;pH</sup>, &nbsp; ['+H3O+']['+OHM+'] = K<sub>w</sub> = 1.00&times;10<sup>&minus;14</sup> <span class="rm">at 25 &deg;C</span>')
    +EQ(2,'&rArr; &nbsp; ['+OHM+'] = K<sub>w</sub>/['+H3O+'], &nbsp; pH + pOH = 14')
    +EQ(3,'n = cV <span class="rm">mol</span>, &nbsp; N = n N<sub>A</sub>, &nbsp; N<sub>A</sub> = 6.02214076&times;10<sup>23</sup> <span class="rm">(exact, SI)</span>')
    +'<p>[2] is written as a division on purpose. PhET spells it 10<sup>&minus;(14&minus;pH)</sup>, and pH &minus; 14 is inexact in a double whenever pH &lt; 7 &mdash; 5.8 &minus; 14 needs one bit more than a double carries &mdash; so that spelling is out by up to 2.1&times;10<sup>&minus;15</sup> while the division is out by 2.1&times;10<sup>&minus;16</sup> and keeps the product at K<sub>w</sub> to a rounding.</p>'
    +'<div class="cite">pins: both concentrations against 50-digit decimal over the whole scale and at its ends; the product; PhET&rsquo;s spelling measured against this one &mdash; derive.py</div>',
  dilution:'<h4>what actually dilutes</h4>'
    +EQ(1,'C &equiv; ['+H3O+'] &minus; ['+OHM+'] = &minus;2&radic;K<sub>w</sub> sinh[ln10 (pH &minus; 7)]')
    +EQ(2,'C = (C<sub>1</sub>V<sub>1</sub> + C<sub>2</sub>V<sub>2</sub>)/(V<sub>1</sub>+V<sub>2</sub>) &nbsp;&rarr;&nbsp; <span class="rm">with water,</span> C = C<sub>0</sub>V<sub>0</sub>/V')
    +EQ(3,'['+H3O+'] &minus; K<sub>w</sub>/['+H3O+'] = C &nbsp;&rArr;&nbsp; pH = 7 &minus; asinh[C/(2&radic;K<sub>w</sub>)]/ln10')
    +'<p>C is a difference of ANALYTICAL concentrations &mdash; the spectator ions cancel out of the charge balance &mdash; so its moles are conserved and it volume-averages, which neither the pH nor either ion does. [3] is the water autoionisation PhET&rsquo;s rule leaves out. It is solved twice here: the asinh above, and the stable branch of the quadratic root. The textbook root (C + &radic;(C&sup2;+4K<sub>w</sub>))/2 cancels for every base &mdash; 3.6&times;10<sup>&minus;5</sup> at pH 13, 8.0&times;10<sup>&minus;4</sup> at 14, <span class="warn">11 %</span> at 15 &mdash; so C &lt; 0 takes 2K<sub>w</sub>/(&radic;(C&sup2;+4K<sub>w</sub>) &minus; C) instead.</p>'
    +'<div class="cite">pins: the mixing law against a Decimal mole ledger and a scipy brentq root; C scaled by exactly f under f-fold dilution; both roots against each other; the naive root asserted STILL bad so the branch cannot be deleted &mdash; derive.py</div>',
  phet:'<h4>PhET&rsquo;s rule, and the size of the gap</h4>'
    +EQ(1,'<span class="rm">acid:</span> pH = &minus;log<sub>10</sub>'+FR2('10<sup>&minus;pH<sub>1</sub></sup>V<sub>1</sub> + 10<sup>&minus;7</sup>V<sub>2</sub>','V<sub>1</sub>+V<sub>2</sub>')+' &nbsp; <span class="rm">base:</span> 14 + log<sub>10</sub>'+FR2('10<sup>pH<sub>1</sub>&minus;14</sup>V<sub>1</sub> + 10<sup>&minus;7</sup>V<sub>2</sub>','V<sub>1</sub>+V<sub>2</sub>'))
    +EQ(2,'max |exact &minus; PhET| = <span class="hl">0.0948</span> pH <span class="rm">at pH 4.91, 0.015 L in 1.2 L</span>')
    +EQ(3,'max |exact &minus; averaged pH| = <span class="warn">4.42</span> pH')
    +'<p>PhET mixes the majority ion and never re-solves, so water&rsquo;s own autoionisation is counted on one side and dropped on the other. The error vanishes undiluted and at infinite dilution and peaks in between, and it is an ODD function about pH 7 because C(14&minus;pH) = &minus;C(pH) and the two branches mirror each other. Averaging the pH is a different order of wrong.</p>'
    +'<div class="cite">pins: the worst gap swept over pH &minus;1..15 &times; 0.015..1.2 L; the odd symmetry to 1e-12; both degenerate limits exact &mdash; derive.py</div>',
  phet_draw:'<h4>PhET&rsquo;s drawing rules</h4>'
    +EQ(1,'<span class="rm">dots</span> = round(50 &times; c / 10<sup>&minus;7</sup>) <span class="rm">inside</span> 6 &le; pH &le; 8, <span class="rm">floor 5</span>')
    +EQ(2,'<span class="rm">outside: minority ramps to</span> 3000 <span class="rm">at the ends of</span> [&minus;1, 15]<span class="rm">, majority saturates</span>')
    +EQ(3,'<span class="rm">colour:</span> water &rarr; stop <span class="rm">over</span> r &le; 0.25, <span class="rm">stop</span> &rarr; stock <span class="rm">over</span> r &gt; 0.25, &nbsp; r = V<sub>solute</sub>/V')
    +'<p>Both are reimplemented from the arithmetic in the minified original and cited as PhET&rsquo;s. [1]&ndash;[2] is a compression, and the canvas prints the compression factor: at pH 13 the drawn ratio is 457:1 against a true 10<sup>12</sup>:1.</p>'
    +'<div class="cite">pins: the dot counts at pH 7, 6, 8, 1, 13, 15 and &minus;1; the colour law at r = 0, 0.25 and 1, with and without a colour stop &mdash; derive.py</div>'
};
const DERIV={
  beaker:DERIV_CORE.ions+DERIV_CORE.dilution,
  particles:DERIV_CORE.phet_draw+DERIV_CORE.ions,
  graph:DERIV_CORE.ions,
  my:DERIV_CORE.ions,
  dilution:DERIV_CORE.dilution+DERIV_CORE.phet,
  scale:DERIV_CORE.ions+DERIV_CORE.phet
};
