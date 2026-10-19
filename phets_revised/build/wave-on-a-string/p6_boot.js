
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
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS=[];
  function trackChips(g,list,key){ CHIPROWS.push([g,list,key]); }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); }

  /* PhET: switching the wave mode restarts the string; switching to the fixed end zeroes bead 60 */
  const gWave=h('div',{class:'grp'},h('h3',null,'the wave'));
  const modeChips=chipRow(MODE_LIST,'mode',(o,was)=>{ if(o.id!==was) liveRestart(); }); gWave.appendChild(modeChips); trackChips(gWave,MODE_LIST,'mode');
  const pulseBtn=h('div',{class:'btnrow'},btn('send a pulse',()=>{ if(sendPulse(st)) st.running=true; }));
  gWave.appendChild(pulseBtn);
  gWave.appendChild(slider('amp','amplitude, cm',0,AMAX,0.01,v=>fmt(v,2)+' cm'));
  gWave.appendChild(slider('freq','frequency, Hz',0,FMAX,0.01,v=>fmt(v,2)+' Hz'));
  gWave.appendChild(slider('pw','pulse width, s',WMIN,WMAX,0.01,v=>fmt(v,2)+' s'));
  const waveTag=h('div',{class:'tag'}); gWave.appendChild(waveTag);

  const gString=h('div',{class:'grp'},h('h3',null,'the string'));
  gString.appendChild(slider('damping','damping',0,1,0.01,v=>fmt(v,2)));
  gString.appendChild(slider('tension','tension (relative)',TMIN,TMAX,0.001,v=>fmt(v,3)));
  const endChips=chipRow(END_LIST,'end',o=>{ if(o.id==='fixed'){ LIVE.lat.cur[NSEG]=0; LIVE.lat.prev[NSEG]=0; } });
  gString.appendChild(endChips); trackChips(gString,END_LIST,'end');
  const stringTag=h('div',{class:'tag'}); gString.appendChild(stringTag);

  const restartView=()=>{ if(st.view==='refl') reflReset(st); else if(st.view==='stand') standReset(st); else liveRestart(); };
  const stepView=()=>{ if(st.view==='refl') reflStep(st); else if(st.view==='stand') standStep(st); else liveStepButton(st); };
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const speedChips=chipRow(SPEED_LIST,'speed'); gTime.appendChild(speedChips); trackChips(gTime,SPEED_LIST,'speed');
  gTime.appendChild(h('div',{class:'btnrow'},btn('step',stepView),btn('restart string',restartView),
    btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; liveRestart(); LIVE.sw=0; LIVE.swOn=false; LIVE.arrows=true;
      reflReset(st); standReset(st); syncChips(); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('rulers','rulers'),checkbox('stopwatch','stopwatch'),checkbox('refline','reference line')));
  const swBtns=h('div',{class:'btnrow'},btn('start / stop',()=>{ LIVE.swOn=!LIVE.swOn; }),btn('clear',()=>{ LIVE.sw=0; }));
  gTools.appendChild(swBtns);
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  const gLat=h('div',{class:'grp'},h('h3',null,'the lattice'));
  gLat.appendChild(slider('alpha','Courant number α',0.05,1,0.01,v=>fmt(v,2)));
  const latTag=h('div',{class:'tag'}); gLat.appendChild(latTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Wave on a String (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets. PhET&rsquo;s values (61 beads 0.125 cm apart, 50 steps a second at full tension, &beta; = 0.1 &times; damping, '
      +'the slider ranges, the end rules, the triangular pulse) are read from its build 1.2.4 and its doc/model.md; everything else is exact and pinned '
      +'in selfTest to build/wave-on-a-string/derive.py (d&rsquo;Alembert image series, numpy.roots, a dense and a tridiagonal solve, brute-force runs, scipy).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gWave,gString,gTime,gTools,gLat,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [g,list,key] of CHIPROWS){
      const cws=g.querySelectorAll('.chips');
      for(const cw of cws){
        if(cw.children.length!==list.length) continue;
        let match=0;
        for(let i=0;i<list.length;i++) if(cw.children[i].textContent===list[i].name) match++;
        if(match===list.length)
          [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
      }
    }
  }
  /* a row the view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view, live=(v==='str'||v==='xt');
    gWave.hidden=false; gString.hidden=false;
    modeChips.hidden=!live; pulseBtn.hidden=!(live&&st.mode==='pulse');
    rows.amp.row.hidden=live&&st.mode==='manual';
    rows.freq.row.hidden=!((live&&st.mode==='osc')||v==='stand'||v==='disp');
    rows.pw.row.hidden=!((live&&st.mode==='pulse')||v==='refl'||v==='disp');
    rows.damping.row.hidden=(v==='refl');
    endChips.hidden=!(live||v==='stand');
    gTime.hidden=(v==='disp');
    gTools.hidden=(v!=='str');
    swBtns.hidden=!st.stopwatch;
    gLat.hidden=(v!=='disp');
    for(const k in rows) rows[k].sync();
    waveTag.innerHTML=live?(st.mode==='manual'?'drag the wrench on the canvas (or &uarr; &darr;); PhET&rsquo;s wrench stops at &plusmn;1.3 cm'
      :st.mode==='osc'?'A sin 2&pi;ft at bead 0, rising first; the phase runs on when f changes'
      :'a triangle, A high and w long; click the generator, press p, or the button')
      :v==='refl'?'the pulse fed to all three strings':v==='stand'?'the oscillator driving the run; drag the top panel to set f':'the pulse in the bottom panel; f marks the oscillator on &omega;(k)';
    stringTag.innerHTML='v = '+fmt(speedOf(st.tension),3)+' cm/s, &Delta;t = '+sigf(1000*dtOf(st.tension),3)+' ms'+(v==='refl'?'; this view is undamped':'')
      +' &nbsp; (PhET&rsquo;s own slider, 0.2&ndash;0.8, would give '+(st.tension>=0.2?fmt(phetRate(st.tension)*DX,3)+' cm/s':'&mdash; below its range')+')';
    timeTag.innerHTML='space runs/pauses &nbsp; <b>.</b> steps &nbsp; <b>r</b> restarts &nbsp; 1&ndash;5 switch views'+(st.speed==='slow'?' &nbsp; slow motion: &times;0.25':'');
    toolTag.innerHTML='drag the rulers, the stopwatch and the reference line on the canvas';
    latTag.innerHTML='PhET runs at &alpha; = 1; below it the leapfrog is dispersive, and &alpha; &rarr; 0 is a bead chain';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='str'?(st.mode==='manual'?'drag the wrench':st.mode==='pulse'?'click the generator or press p':'the oscillator runs')+' · space pauses · 1–5 switch views'
        :st.view==='stand'?'drag the top panel to set f · space pauses · 1–5 switch views':'space pauses · 1–5 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
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
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ restartView(); dirty=true; refresh(); }
    else if(e.key==='.'){ stepView(); dirty=true; refresh(); }
    else if(e.key==='p'){ if(sendPulse(st)){ st.running=true; syncPanel(); dirty=true; refresh(); } }
    else if((e.key==='ArrowUp'||e.key==='ArrowDown')&&st.view==='str'&&st.mode==='manual'){
      e.preventDefault(); LIVE.wr=clamp(LIVE.wr+(e.key==='ArrowUp'?0.1:-0.1),-AMAX,AMAX); LIVE.arrows=false; st.running=true; syncPanel(); dirty=true; refresh(); }
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
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  str:'PhET&rsquo;s Wave on a String is a chain of 61 beads, and this is its model exactly. Each bead moves only up and down, and at every '
    +'step it goes to the sum of its two neighbours&rsquo; positions less its own previous position, with a little damping. That rule is the '
    +'wave equation on a lattice, and PhET runs it at the one time step where it is exact: the step in which a wave moves precisely one bead, '
    +'so the Courant number &alpha; = v&Delta;t/&Delta;x is 1. The tension therefore never changes the rule. It changes how often the rule is '
    +'applied, 10 to 50 times a second, and that is the wave speed v = &radic;(T/&mu;). Shake the wrench, or switch on the oscillator or the '
    +'pulse generator, and watch what the far end does with what arrives: the clamp sends it back upside down, the ring on its pole sends it '
    +'back upright, and with no end it simply leaves. Damping keeps the same fraction, e<sup>&minus;atanh &beta;</sup>, at every bead of travel, '
    +'whatever the tension.',
  xt:'d&rsquo;Alembert&rsquo;s solution of the wave equation says that any motion of a uniform string is two shapes sliding in opposite '
    +'directions at the wave speed: y = f(x &minus; vt) + g(x + vt). Plot the string&rsquo;s height against position and time and each shape '
    +'becomes a stripe whose tilt is set by v. This view records the string you are driving on the first tab, one row per lattice step, newest at the '
    +'top. On PhET&rsquo;s lattice the statement is exact rather than approximate: at &alpha; = 1 every level is y<sub>i</sub><sup>n</sup> = '
    +'F(n &minus; i) + G(n + i), two sequences shifted one bead per step, which is why the stripes are straight to the last pixel. Watch a pulse '
    +'reach the clamp: the green stripe turns back and comes out cyan, because the reflected wave is inverted. At the ring it keeps its colour; '
    +'with no end it leaves the picture.',
  refl:'Why does a fixed end invert a pulse and a loose end not? Extend the string past its end into an imaginary mirror world, and send '
    +'an image pulse in from the far side to meet the real one at the end. If the end must stay at zero, the image has to be the real pulse '
    +'upside down, so that the two cancel there; if the end must have zero slope, as a massless ring free to slide has, the image has to be '
    +'upright, so that their slopes cancel. Once the real pulse has run into the mirror world only the image is left on the string, and that '
    +'is the reflection. Here one pulse goes into three strings at once, and the green lattice sits on the orange image construction to the '
    +'last digit, because at &alpha; = 1 the lattice is the exact solution sampled at the beads. One detail shows: PhET&rsquo;s loose end is '
    +'the rule y<sub>60</sub> = y<sub>59</sub>, which puts the mirror half a bead in, at bead 59&frac12;, not at the ring.',
  stand:'The oscillator at bead 0 is also a wall: whatever comes back along the string is reflected there too, inverted, as from a clamp. '
    +'So a wave that fits a whole number of round trips arrives back in step with the next push, and the pushes add up. That is a resonance. '
    +'With a fixed far end it happens when the string holds a whole number of half wavelengths, f<sub>n</sub> = nv/2L; with a loose end, an '
    +'odd number of quarter wavelengths, f<sub>n</sub> = (2n &minus; 1)v/4L&prime;. The top panel is the exact steady answer of PhET&rsquo;s '
    +'lattice across PhET&rsquo;s 0&ndash;3 Hz: the biggest amplitude anywhere on the string, as a multiple of the driving amplitude. With no '
    +'damping it is infinite at every f<sub>n</sub>; with damping &beta; per step the peak is close to 1/(N&beta;), N = 60, so lowering the damping '
    +'sharpens the peaks. The bottom panel drives the lattice from rest and shows it growing into that steady state as the transient dies, '
    +'e<sup>&minus;n atanh &beta;</sup>. With no end the response is flat: nothing comes back to pile up.',
  disp:'A real chain of beads on springs is dispersive: short waves travel slower than long ones, and a wave two beads long does not travel '
    +'at all. Its frequency is &omega; = (2v/&Delta;x) sin(k&Delta;x/2), the violet curve, which bends away from the straight line of a '
    +'continuous string. PhET&rsquo;s string is drawn as beads but does not behave like a chain. It is the leapfrog lattice at Courant number 1, '
    +'whose dispersion relation sin(&omega;&Delta;t/2) = &alpha; sin(k&Delta;x/2) is exactly &omega; = vk when &alpha; = 1: the error of '
    +'stepping in time cancels the error of the beads, at every wavelength up to the zone edge. That is why a PhET pulse never spreads or '
    +'rings, however sharp it is. Lower &alpha; to see what a smaller time step would give: the green curve bends toward the chain, the '
    +'phase and group speeds fall, and the pulse sheds ripples behind it; &alpha; &rarr; 0 is the chain itself. Damping adds a little '
    +'dispersion of its own (the telegrapher&rsquo;s equation): waves longer than 2&pi;&Delta;x/&beta; are overdamped, 39 cm at PhET&rsquo;s '
    +'default, far longer than the string.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  str:'<h4>the lattice</h4>'
    +EQ(1,'(1+&beta;) y<sub>i</sub><sup>n+1</sup> = (&beta;&minus;1) y<sub>i</sub><sup>n&minus;1</sup> + 2(1&minus;&alpha;&sup2;) y<sub>i</sub><sup>n</sup> + &alpha;&sup2;(y<sub>i+1</sub><sup>n</sup> + y<sub>i&minus;1</sub><sup>n</sup>)')
    +EQ(2,'&alpha; = '+FR('v&Delta;t','&Delta;x')+' = 1 &nbsp;&rArr;&nbsp; (1+&beta;) y<sub>i</sub><sup>n+1</sup> = y<sub>i+1</sub><sup>n</sup> + y<sub>i&minus;1</sub><sup>n</sup> &minus; (1&minus;&beta;) y<sub>i</sub><sup>n&minus;1</sup>')
    +EQ(3,'<span class="rm">fixed</span> y<sub>60</sub> = 0, &nbsp; <span class="rm">loose</span> y<sub>60</sub> = y<sub>59</sub>, &nbsp; <span class="rm">no end</span> y<sub>60</sub><sup>n+1</sup> = y<sub>59</sub><sup>n</sup>')
    +EQ(4,'v = v<sub>max</sub>&radic;(T/T<sub>max</sub>) = 6.25 cm/s &times; &radic;(T/0.8), &nbsp; &Delta;t = &Delta;x/v')
    +EQ(5,'|z| = &radic;'+FR('1&minus;&beta;','1+&beta;')+' = e<sup>&minus;atanh &beta;</sup> <span class="rm">per step, decay length</span> &Delta;x/atanh &beta;')
    +'<p>PhET&rsquo;s own tension slider maps &radic;T linearly onto 10&ndash;50 steps a second, so its speed changes 5:1 over a 4:1 tension '
    +'range where &radic;T gives 2:1. The remake keeps the 5:1 speed range and makes it the law [4], so its slider runs 0.032&ndash;0.8. '
    +'PhET&rsquo;s damping is per step, so it fixes the loss per bead travelled [5], whatever the tension: 6.25 cm to e<sup>&minus;1</sup> at the default.</p>'
    +'<div class="cite">pins: v and &Delta;t at six tensions, PhET&rsquo;s map at 0.2, 0.5, 0.8; the arrival step and the centroid speed of a pulse; '
    +'|z| and the decay length &mdash; derive.py</div>',
  xt:'<h4>d&rsquo;Alembert, on the lattice</h4>'
    +EQ(1,'y<sub>tt</sub> = v&sup2; y<sub>xx</sub> &nbsp;&rArr;&nbsp; y = f(x &minus; vt) + g(x + vt)')
    +EQ(2,'y<sub>i</sub><sup>n</sup> = F(n &minus; i) + G(n + i): &nbsp; F(n&minus;i&minus;1) + F(n&minus;i+1) &minus; F(n&minus;1&minus;i) = F(n+1&minus;i) &nbsp;<span class="rm">exactly</span>')
    +'<p>At &alpha; = 1 and no damping any two lattice levels split exactly into a right-moving and a left-moving sequence, so the lattice carries '
    +'d&rsquo;Alembert&rsquo;s solution with no error at all; with damping each stripe fades by e<sup>&minus;atanh &beta;</sup> per bead.</p>'
    +'<div class="cite">the same rows are what the first tab draws; the record keeps '+HMAX+' levels</div>',
  refl:'<h4>the image construction</h4>'
    +EQ(1,'<span class="rm">fixed:</span> y = f(t &minus; x/v) &minus; f(t &minus; (2L &minus; x)/v) &nbsp;&rArr;&nbsp; y(L) = 0')
    +EQ(2,'<span class="rm">loose:</span> y = f(t &minus; x/v) + f(t &minus; (2L&prime; &minus; x)/v), &nbsp; L&prime; = (N &minus; &frac12;)&Delta;x &nbsp;&rArr;&nbsp; y<sub>N</sub> = y<sub>N&minus;1</sub>')
    +EQ(3,'<span class="rm">the driven end reflects inverted:</span> y = &Sigma;<sub>m</sub> (&plusmn;1)<sup>m</sup>[f(t &minus; (2mL + x)/v) &plusmn; f(t &minus; (2(m+1)L &minus; x)/v)]')
    +EQ(4,'<span class="rm">no end:</span> y<sub>N</sub><sup>n+1</sup> = y<sub>N&minus;1</sub><sup>n</sup> &nbsp; <span class="rm">is exact for</span> F(n &minus; i) <span class="rm">at &alpha; = 1: nothing comes back</span>')
    +'<p>Every image argument is a whole number of steps, 2N for the clamp and 2N &minus; 1 for the ring, so the series is exact on the lattice. '
    +'Putting the ring&rsquo;s mirror at bead 60 instead of 59&frac12; is wrong by 0.06 cm at the default pulse.</p>'
    +'<div class="cite">pins: max |lattice &minus; series| &lt; 1e&minus;13 (derive: 1e&minus;14) for all three ends at two parameter sets, one incommensurate; '
    +'bead values at chosen steps; the reflected extremes &minus;0.72, +0.72, 0 &mdash; derive.py</div>',
  stand:'<h4>the driven steady state</h4>'
    +EQ(1,'y<sub>i</sub><sup>n</sup> = Im(Y<sub>i</sub> e<sup>in&theta;</sup>), &nbsp; &theta; = 2&pi;f&Delta;t, &nbsp; Y<sub>i+1</sub> + Y<sub>i&minus;1</sub> = 2(cos &theta; + i&beta; sin &theta;) Y<sub>i</sub>')
    +EQ(2,'Y<sub>i</sub> = p&lambda;<sup>i</sup> + q&lambda;<sup>N&minus;i</sup>, &nbsp; &lambda;&sup2; &minus; 2C&lambda; + 1 = 0, |&lambda;| &lt; 1, &nbsp; Y<sub>0</sub> = A <span class="rm">and the end</span>')
    +EQ(3,'<span class="rm">fixed:</span> sin N&theta; = 0 &rArr; f<sub>n</sub> = '+FR('n','2N&Delta;t')+' = '+FR('nv','2L')+'; &nbsp; <span class="rm">loose:</span> cos(N&minus;&frac12;)&theta; = 0 &rArr; f<sub>n</sub> = '+FR('(2n&minus;1)v','4L&prime;'))
    +EQ(4,'<span class="rm">at a resonance</span> max|Y|/A &rarr; 1/(N&beta;) <span class="rm">as &beta; &rarr; 0</span>')
    +EQ(5,'<span class="rm">no end:</span> |r| = '+FR('|z&lambda; &minus; 1|','|&lambda;(&lambda; &minus; z)|')+' &asymp; '+FR('&beta;','2 sin &theta;'))
    +'<p>[2] is checked against a tridiagonal solve of the same equations and against a brute-force lattice run of thousands of steps; the three '
    +'agree to within 3e&minus;11. The absorber leaks: at the default 1.5 Hz and damping it sends back 5.4 %, which is PhET&rsquo;s own &ldquo;greatly '
    +'reduces but does not perfectly eliminate&rdquo;.</p>'
    +'<div class="cite">pins: six steady states (|Y| at four beads, Y<sub>30</sub>, the maximum), the peak heights 166.7 and 1666.7 at &beta; = 1e&minus;4 and 1e&minus;5, '
    +'the scipy-located peaks, the no-end reflection &mdash; derive.py</div>',
  disp:'<h4>the dispersion relation</h4>'
    +EQ(1,'y &prop; z<sup>n</sup>e<sup>ikx</sup>: &nbsp; (1+&beta;) z&sup2; &minus; 2(1 &minus; 2&alpha;&sup2; sin&sup2;(k&Delta;x/2)) z + (1&minus;&beta;) = 0')
    +EQ(2,'&beta; = 0: &nbsp; sin(&omega;&Delta;t/2) = &alpha; sin(k&Delta;x/2); &nbsp; &alpha; = 1 &rArr; &omega; = vk <span class="rm">for all</span> |k| &le; &pi;/&Delta;x')
    +EQ(3,'v<sub>g</sub> = '+FR('d&omega;','dk')+' = '+FR('&alpha; v sin k&Delta;x','&radic;(1&minus;&beta;&sup2;) sin &omega;&Delta;t'))
    +EQ(4,'&alpha; &rarr; 0: &nbsp; &omega; &rarr; (2v/&Delta;x) sin(k&Delta;x/2) <span class="rm">(the bead chain), error O(&alpha;&sup2;)</span>')
    +EQ(5,'&alpha; = 1: &nbsp; cos &omega;&Delta;t = cos k&Delta;x / &radic;(1&minus;&beta;&sup2;) &nbsp;<span class="rm">overdamped for</span> sin k&Delta;x &lt; &beta;')
    +'<p>The lattice at &alpha; &lt; 1 keeps the same physical damping, so its &beta; per step is &alpha;&beta;. The bead chain drawn is the same lattice at '
    +'&alpha; = 0.05, within 0.04 % (&alpha;&sup2;/6) of the continuous-time chain&rsquo;s &omega;(k).</p>'
    +'<div class="cite">pins: &theta; at six (k, &alpha;, &beta;) against numpy.roots, v<sub>g</sub> against a numerical derivative, the O(&alpha;&sup2;) approach to the chain '
    +'(error ratio 100.01), a cosine mode after 300 steps, the pulse on the long lattice at &alpha; = 1, 0.5, 0.05 &mdash; derive.py</div>',
};
