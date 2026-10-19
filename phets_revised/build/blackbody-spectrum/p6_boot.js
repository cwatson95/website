
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
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
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
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  function button(lab2,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},lab2); }

  /* the temperature: PhET's thermometer range and snap, and its four presets */
  const gTemp=h('div',{class:'grp'},h('h3',null,'the temperature'));
  gTemp.appendChild(slider('T','T, kelvin',T_MIN,T_MAX,T_SNAP,v=>fmt(v,0)+' K',()=>setT(st.T)));
  const presetRow=h('div',{class:'chips'});
  PRESETS.forEach(p=>presetRow.appendChild(h('button',{class:'chip',onclick:()=>{ setT(p.T); syncPanel(); dirty=true; refresh(); }},p.name)));
  gTemp.appendChild(presetRow);
  const tempTag=h('div',{class:'tag'}); gTemp.appendChild(tempTag);

  /* PhET's three checkboxes, its save and erase buttons, and its zoom buttons */
  const gGraph=h('div',{class:'grp'},h('h3',null,'the graph'));
  gGraph.appendChild(h('div',{class:'checks'},
    checkbox('gv','graph values',()=>setGraphValues(st.gv)),
    checkbox('labels','labels'),
    checkbox('inten','intensity')));
  const saveBtn=button('save curve',saveCurve), eraseBtn=button('erase saved',eraseSaved);
  gGraph.appendChild(h('div',{class:'btnrow'},saveBtn,eraseBtn));
  const graphTag=h('div',{class:'tag'}); gGraph.appendChild(graphTag);

  const gZoom=h('div',{class:'grp'},h('h3',null,'zoom'));
  const zxIn=button('λ: zoom in',()=>zoomX(-1)), zxOut=button('λ: zoom out',()=>zoomX(1));
  const zyIn=button('power: zoom in',()=>zoomY(-1)), zyOut=button('power: zoom out',()=>zoomY(1));
  const fitBtn=button('fit the axes',fitAxes);
  gZoom.appendChild(h('div',{class:'btnrow'},zxIn,zxOut));
  gZoom.appendChild(h('div',{class:'btnrow'},zyIn,zyOut));
  gZoom.appendChild(h('div',{class:'btnrow'},fitBtn));
  const zoomTag=h('div',{class:'tag'}); gZoom.appendChild(zoomTag);

  const gLim=h('div',{class:'grp'},h('h3',null,'the older laws'));
  gLim.appendChild(h('div',{class:'checks'},checkbox('rj','Rayleigh–Jeans (1900–05)'),checkbox('wien','Wien’s approximation (1896)')));

  const gReset=h('div',{class:'grp'},h('div',{class:'btnrow'},button('reset all',resetAll)));
  const keysTag=h('div',{class:'tag'}); gReset.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Blackbody Spectrum (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. h, c, k exact (SI 2019); the colour-matching functions '
      +'are the CIE&rsquo;s own 1931 table (DOI 10.25039/CIE.DS.xvudnb9b); PhET&rsquo;s values: the 200&ndash;11000 K range, '
      +'the presets, the zoom ladders, the band edges and the photometer. Everything else is derived and pinned in selfTest '
      +'to build/blackbody-spectrum/derive.py.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gTemp,gGraph,gZoom,gLim,gReset,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncPanel(){
    const v=st.view;
    gGraph.hidden=(v!=='spec'); gZoom.hidden=(v!=='spec'); gLim.hidden=(v!=='limits');
    for(const k in rows) rows[k].sync();
    [].forEach.call(presetRow.children,(b,i)=>b.className='chip'+(PRESETS[i].T===st.T?' on':''));
    eraseBtn.disabled=SAVED.length===0;
    zxIn.disabled=st.ix<=0; zxOut.disabled=st.ix>=ZOOM_X.length-1;
    zyIn.disabled=st.iy<=0; zyOut.disabled=st.iy>=ZOOM_Y.length-1;
    const f=fitZoom(st.T); fitBtn.disabled=(f[0]===st.ix&&f[1]===st.iy);
    const p=presetAt(st.T);
    tempTag.innerHTML=p?'PhET&rsquo;s preset: <b>'+p.name+'</b>, '+fmt(p.T,0)+' K':'snaps to 50 K, as PhET&rsquo;s thermometer does';
    graphTag.innerHTML='saved: '+(SAVED.length?SAVED.map(T=>fmt(T,0)+' K').join(', '):'none')+' (PhET keeps two)';
    zoomTag.innerHTML='&lambda; axis 0&ndash;'+axisMax(ZOOM_X[st.ix]/1000)+' &micro;m (&times;2 a click), power 0&ndash;'+axisMax(ZOOM_Y[st.iy])+' MW/m&sup2;/&micro;m (&times;5)';
    keysTag.innerHTML='<b>&uarr;</b>/<b>&darr;</b> change T by 50 K &nbsp; <b>1</b>&ndash;<b>5</b> switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='spec'?'drag the thermometer, or the Graph Values point · ↑↓ 50 K · 1–5 views':'↑↓ change T by 50 K · 1–5 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); tagEl.innerHTML=tagHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key==='ArrowUp'||e.key==='ArrowRight'){ e.preventDefault(); setT(st.T+T_SNAP); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='ArrowDown'||e.key==='ArrowLeft'){ e.preventDefault(); setT(st.T-T_SNAP); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  /* nothing here animates: a frame is drawn only when something marked the picture dirty */
  function frameLoop(){
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  spec:'A blackbody absorbs every wavelength that falls on it and, in equilibrium, radiates a spectrum fixed by its temperature '
    +'alone: Planck&rsquo;s law. The green curve is that spectrum, as power per square metre of surface per micrometre of '
    +'wavelength. Drag the thermometer, or use the slider, and three things move together: the peak slides to shorter '
    +'wavelengths (Wien&rsquo;s law, the orange diamond), the whole curve climbs (the area, shaded when <b>intensity</b> is on, '
    +'is &sigma;T<sup>4</sup>), and the star changes colour. The axes zoom as PhET&rsquo;s do, &times;2 in wavelength and &times;5 in '
    +'power: the Earth at 250 K peaks at 11.6 &micro;m, about a seven-millionth as high as the Sun (the peak goes as T<sup>5</sup>), so to see it you zoom far out in '
    +'wavelength and far in in power, or press <b>fit the axes</b>. <b>Graph values</b> puts a point on the curve that you drag '
    +'along it; like PhET&rsquo;s, it goes back to the peak whenever the temperature changes. <b>Save curve</b> keeps a curve '
    +'to compare against; PhET keeps two.',
  star:'What colour is a hot body? PhET&rsquo;s star answers with a photometer: it samples the curve at 650, 550 and 450 nm, '
    +'divides each by the largest of the three, and uses the results as the star&rsquo;s red, green and blue, dimmed below '
    +'3298 K by a ramp that starts at the Draper point, 798 K, where hot objects first visibly glow. The eye works differently: '
    +'each of its three cone types responds to a broad band, the bands overlap, and the CIE 1931 colour-matching functions '
    +'(the standard observer) turn a spectrum into a colour by integrating it against all three. The two answers agree on the '
    +'trend, red to orange to white to blue-white, but not in the detail: the photometer paints the Sun at 5800 K a faintly cyan '
    +'white where colorimetry says warm white, and paints a 3000 K filament a deeper orange than the eye sees. Three samples of a '
    +'smooth curve exaggerate its slope into saturated colour; broad, overlapping sensitivities average it back toward white. '
    +'Luminous efficacy says how much of the power the eye can use at all: 21 lm/W for the filament, 92 for the Sun, at most '
    +'95.4 lm/W, at 6628 K.',
  peak:'Planck&rsquo;s curve has one peak, where x = hc/&lambda;kT solves x = 5(1 &minus; e<sup>&minus;x</sup>): x = 4.965. The '
    +'peak wavelength is therefore inversely proportional to the temperature, &lambda;<sub>max</sub>T = b = 2.898 mm&middot;K '
    +'(Wien, 1893), and the peak height grows as T<sup>5</sup>. On log&ndash;log axes the whole family slides along a straight '
    +'line of slope &minus;5, the locus of the peaks. Divide each curve by its own peak and its wavelength by its own '
    +'&lambda;<sub>max</sub>, and every temperature collapses onto one shape: a blackbody spectrum has no free parameter but T. '
    +'One subtlety: where the peak is depends on what you plot against. Per unit frequency the same spectrum peaks at '
    +'x = 2.821, a wavelength 1.76 times longer than &lambda;<sub>max</sub>, so &ldquo;the Sun peaks in the green&rdquo; is true '
    +'only per unit wavelength.',
  total:'The area under Planck&rsquo;s curve is the total power a square metre of surface radiates: &sigma;T<sup>4</sup>, the '
    +'Stefan&ndash;Boltzmann law (Stefan from measurements in 1879, Boltzmann from thermodynamics in 1884). The fourth power is '
    +'steep: the Sun&rsquo;s surface at 5800 K sends 64 MW out of every square metre, about 290,000 times what the Earth at 250 K '
    +'radiates. On the right the same area is split into PhET&rsquo;s bands: a 3000 K filament puts 13 % of its power into the '
    +'visible and 87 % into the infrared, which is why an incandescent bulb is mostly a heater; the Sun puts 47 % into the '
    +'visible; Sirius A at 9950 K puts 44 % into the ultraviolet. The shares come from a closed-form series for the integral of '
    +'Planck&rsquo;s law, checked against direct quadrature.',
  limits:'Before Planck, two laws each fitted half the curve. Rayleigh and Jeans counted the standing waves in a cavity and gave '
    +'each one kT of energy, as classical equipartition demands; the result, 2&pi;ckT/&lambda;<sup>4</sup>, matches the long-wavelength '
    +'side and climbs without limit toward short wavelengths, so the total it predicts is infinite: the ultraviolet catastrophe. '
    +'Wien&rsquo;s 1896 law fits the short-wavelength side and fails at long ones. Planck&rsquo;s formula contains both. Where '
    +'hc/&lambda;kT is small, e<sup>x</sup> &minus; 1 &asymp; x and it becomes Rayleigh&ndash;Jeans; where it is large, the '
    +'&minus;1 is negligible and it becomes Wien&rsquo;s. At the peak Wien&rsquo;s law is already within 0.7 %, which is why the '
    +'displacement law was known before Planck; Rayleigh&ndash;Jeans is 29 times too high there.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  spec:'<h4>Planck&rsquo;s law, as PhET plots it</h4>'
    +EQ(1,'B<sub>&lambda;</sub>(T) = '+FR('2hc&sup2;','&lambda;<sup>5</sup>')+' '+FR('1','e<sup>hc/&lambda;kT</sup> &minus; 1')+' &nbsp;<span class="rm">W m<sup>&minus;2</sup> sr<sup>&minus;1</sup> m<sup>&minus;1</sup></span>')
    +EQ(2,'M<sub>&lambda;</sub> = &pi;B<sub>&lambda;</sub> = '+FR('c<sub>1</sub>','&lambda;<sup>5</sup> (e<sup>c<sub>2</sub>/&lambda;T</sup> &minus; 1)')+', &nbsp; c<sub>1</sub> = 2&pi;hc&sup2;, &nbsp; c<sub>2</sub> = hc/k')
    +EQ(3,'1 W m<sup>&minus;3</sup> = 10<sup>&minus;12</sup> MW m<sup>&minus;2</sup> &micro;m<sup>&minus;1</sup> &nbsp;<span class="rm">(PhET&rsquo;s axis unit)</span>')
    +'<p>The factor &pi; turns radiance into the power a flat surface sends into its whole hemisphere; PhET&rsquo;s model notes call it the spectral flux density, &ldquo;not dependent on steradians&rdquo;. '
    +'PhET&rsquo;s own constants are rounded: c<sub>1</sub> +4.0&times;10<sup>&minus;5</sup>, c<sub>2</sub> &minus;4.8&times;10<sup>&minus;6</sup>, &sigma; &minus;2.5&times;10<sup>&minus;7</sup>, b +3.6&times;10<sup>&minus;7</sup> against CODATA. This file derives every constant from the exact h, c and k.</p>'
    +'<div class="cite">pins: 78 values of M_&lambda; (13 wavelengths &times; 6 temperatures) against 50-digit decimal arithmetic, worst 7.5e-14 deep in the Wien tail; c&#8321;, c&#8322;, &sigma;, b and &nu;_max/T equal to scipy.constants; the fit-the-axes choice for every preset &mdash; derive.py</div>',
  star:'<h4>PhET&rsquo;s photometer</h4>'
    +EQ(1,'c<sub>k</sub> = &lfloor;255 &middot; min(1, r) &middot; M(&lambda;<sub>k</sub>) / max<sub>j</sub> M(&lambda;<sub>j</sub>)&rfloor;, &nbsp; &lambda;<sub>R,G,B</sub> = 650, 550, 450 nm, &nbsp; r = 0.02&radic;(T/K &minus; 798)')
    +EQ(2,'<span class="rm">halo:</span> radius 5 + 47.5 r px, &nbsp; opacity 0.3 r')
    +'<h4>CIE 1931 colorimetry</h4>'
    +EQ(3,'X = &int; M<sub>&lambda;</sub> x&#772;(&lambda;) d&lambda;, &nbsp; Y = &int; M<sub>&lambda;</sub> y&#772; d&lambda;, &nbsp; Z = &int; M<sub>&lambda;</sub> z&#772; d&lambda;, &nbsp; x = '+FR('X','X + Y + Z')+', y = '+FR('Y','X + Y + Z'))
    +EQ(4,'(R, G, B)<sub>lin</sub> = M<sub>sRGB</sub> (X/Y, 1, Z/Y) &nbsp;<span class="rm">negatives clipped, divided by the largest, then the sRGB curve</span>')
    +EQ(5,'&eta; = 683 lm/W &middot; '+FR('&int; M<sub>&lambda;</sub> y&#772; d&lambda;','&sigma;T<sup>4</sup>')+' &nbsp;<span class="rm">(luminous efficacy)</span>')
    +'<p>The sums run every 5 nm from 360 to 830 nm over the CIE&rsquo;s table; against the full 1-nm table they differ by under 2&times;10<sup>&minus;6</sup> in x and y. The chain is checked on the CIE&rsquo;s own Illuminant A: a Planck body at 2855.496 K reproduces its table to its printed precision and its chromaticity to 4&times;10<sup>&minus;8</sup>. '
    +'The analytic colour-matching fit the house sims use (Wyman, Sloan &amp; Shirley 2013) has a red tail that falls 12 to 60 times too fast beyond 700 nm; it puts a 1000 K body 0.011 off in x, which is why this file carries the table.</p>'
    +'<div class="cite">pins: the photometer at 11 temperatures, raw and floored, and the halo; x, y at 13 temperatures, the sRGB bytes, the efficacy and its maximum (95.43 lm/W at 6628 K), Illuminant A &mdash; derive.py</div>',
  peak:'<h4>Wien&rsquo;s displacement law</h4>'
    +EQ(1,'&part;M<sub>&lambda;</sub>/&part;&lambda; = 0 &nbsp;&rArr;&nbsp; x = 5(1 &minus; e<sup>&minus;x</sup>), &nbsp; x = hc/&lambda;kT &nbsp;&rArr;&nbsp; x&#8325; = 5 + W<sub>0</sub>(&minus;5e<sup>&minus;5</sup>) = 4.965114231744276')
    +EQ(2,'&lambda;<sub>max</sub> T = b = '+FR('hc','x&#8325; k')+' = 2.897771955&times;10<sup>&minus;3</sup> m K')
    +EQ(3,'M(&lambda;<sub>max</sub>) = K T<sup>5</sup>, &nbsp; K = '+FR('2&pi;k<sup>5</sup>x&#8325;<sup>5</sup>','h<sup>4</sup>c<sup>3</sup>(e<sup>x&#8325;</sup> &minus; 1)')+' = 1.28669415&times;10<sup>&minus;5</sup> W m<sup>&minus;3</sup> K<sup>&minus;5</sup>')
    +EQ(4,'M / M(&lambda;<sub>max</sub>) = u<sup>&minus;5</sup> '+FR('e<sup>x&#8325;</sup> &minus; 1','e<sup>x&#8325;/u</sup> &minus; 1')+', &nbsp; u = &lambda;/&lambda;<sub>max</sub> &nbsp;<span class="rm">— no T left in it</span>')
    +EQ(5,'&nu;<sub>max</sub> = x&#8323;kT/h, &nbsp; x&#8323; = 3(1 &minus; e<sup>&minus;x&#8323;</sup>) = 2.821439372, &nbsp; c/&nu;<sub>max</sub> = (x&#8325;/x&#8323;) &lambda;<sub>max</sub> = 1.760 &lambda;<sub>max</sub>')
    +'<div class="cite">pins: x&#8325; and x&#8323; against Lambert W and 50-digit Newton; b and &nu;_max/T against scipy.constants; &lambda;_max and the peak height at six temperatures; the peak found by a golden-section search on the curve itself; the half-maximum points 0.61323 and 1.81700 &mdash; derive.py</div>',
  total:'<h4>Stefan&ndash;Boltzmann</h4>'
    +EQ(1,'&int;<sub>0</sub><sup>&infin;</sup> M<sub>&lambda;</sub> d&lambda; = '+FR('2&pi;k<sup>4</sup>T<sup>4</sup>','h<sup>3</sup>c<sup>2</sup>')+' &int;<sub>0</sub><sup>&infin;</sup> '+FR('t<sup>3</sup> dt','e<sup>t</sup> &minus; 1')+' = '+FR('2&pi;<sup>5</sup>k<sup>4</sup>','15h<sup>3</sup>c<sup>2</sup>')+' T<sup>4</sup> = &sigma;T<sup>4</sup>')
    +'<h4>the share below a wavelength</h4>'
    +EQ(2,'F(x) = '+FR('15','&pi;<sup>4</sup>')+' &int;<sub>x</sub><sup>&infin;</sup> '+FR('t<sup>3</sup> dt','e<sup>t</sup> &minus; 1')+' = '+FR('15','&pi;<sup>4</sup>')+' &Sigma;<sub>n&ge;1</sub> e<sup>&minus;nx</sup> ('+FR('x<sup>3</sup>','n')+' + '+FR('3x<sup>2</sup>','n<sup>2</sup>')+' + '+FR('6x','n<sup>3</sup>')+' + '+FR('6','n<sup>4</sup>')+')')
    +EQ(3,'&int;<sub>0</sub><sup>x</sup> '+FR('t<sup>3</sup> dt','e<sup>t</sup> &minus; 1')+' = &Sigma;<sub>k&ge;0</sub> '+FR('B<sub>k</sub>','k!')+' '+FR('x<sup>k+3</sup>','k + 3')+' &nbsp;<span class="rm">(converges for x &lt; 2&pi;; used below x = 2)</span>')
    +'<p>A band from &lambda;<sub>1</sub> to &lambda;<sub>2</sub> holds F(hc/&lambda;<sub>2</sub>kT) &minus; F(hc/&lambda;<sub>1</sub>kT) of the total. The coefficients B<sub>k</sub>/k! are generated by dividing the power series of t/(e<sup>t</sup> &minus; 1), never typed; the two branches meet at x = 2, where each is good to 10<sup>&minus;16</sup>.</p>'
    +'<div class="cite">pins: &sigma;T&#8308; against scipy quad (4e-16) and against a 1024-point Gauss&ndash;Legendre rule in ln &lambda;; F at 17 values of x against quad, exact rationals and 50-digit series, on both sides of the join; the band shares of every preset &mdash; derive.py</div>',
  limits:'<h4>the two limits of Planck&rsquo;s law</h4>'
    +EQ(1,'x &#8810; 1: &nbsp; e<sup>x</sup> &minus; 1 &asymp; x &nbsp;&rArr;&nbsp; M<sub>&lambda;</sub> &rarr; 2&pi;ckT / &lambda;<sup>4</sup> &nbsp;<span class="rm">(Rayleigh&ndash;Jeans)</span>')
    +EQ(2,'x &#8811; 1: &nbsp; e<sup>x</sup> &minus; 1 &asymp; e<sup>x</sup> &nbsp;&rArr;&nbsp; M<sub>&lambda;</sub> &rarr; (2&pi;hc&sup2;/&lambda;<sup>5</sup>) e<sup>&minus;hc/&lambda;kT</sup> &nbsp;<span class="rm">(Wien)</span>')
    +EQ(3,'M<sub>RJ</sub>/M<sub>&lambda;</sub> = '+FR('e<sup>x</sup> &minus; 1','x')+' = 1 + '+FR('x','2')+' + '+FR('x<sup>2</sup>','6')+' + &hellip;, &nbsp; M<sub>W</sub>/M<sub>&lambda;</sub> = 1 &minus; e<sup>&minus;x</sup>')
    +EQ(4,'&int;<sub>0</sub><sup>&infin;</sup> 2&pi;ckT &lambda;<sup>&minus;4</sup> d&lambda; = &infin; &nbsp;<span class="rm">(the ultraviolet catastrophe)</span>')
    +'<p>Rayleigh&ndash;Jeans is within 1 % of Planck for x &lt; 0.019868 and Wien&rsquo;s law for x &gt; ln 100 = 4.6052; at the peak, x = 4.965, the ratios are 28.66 and 0.99302.</p>'
    +'<div class="cite">pins: both ratios at seven values of x, both routes (the laws divided, and the closed forms), the 1 % points, and the two-term Rayleigh&ndash;Jeans expansion at x = 10<sup>&minus;3</sup> &mdash; derive.py</div>',
};
