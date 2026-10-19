
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
    clearMemo(); syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lb])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lb)); });

  const rows={};
  function slider(key,lb,lo,hi,step,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lb),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ const v=parseFloat(inp.value);
      if(onchg) onchg(v); else st[key]=v;
      clearMemo(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,input:inp}; sync(); return rowEl;
  }
  function checkbox(key,lb){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lb);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; clearMemo();
      syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was); clearMemo();
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); clearMemo(); syncPanel(); dirty=true; refresh(); }},label); }
  const KCHIPS=[{id:'1',name:'1 (primary)'},{id:'2',name:'2 (secondary)'}];

  /* ---- group 1: the light ---- */
  const gLight=h('div',{class:'grp'},h('h3',null,'the light'));
  gLight.appendChild(slider('lamNm','wavelength',PHET.lamMin,PHET.lamMax,1,v=>fmt(v,0)+' nm'));
  gLight.appendChild(h('div',{class:'checks'},checkbox('white','white light'),checkbox('laserOn','laser on')));
  gLight.appendChild(chipRow(POLS,'pol'));
  const lightTag=h('div',{class:'tag'}); gLight.appendChild(lightTag);

  /* ---- group 2: the two media (PhET's Intro and More Tools) ---- */
  const gMed=h('div',{class:'grp'},h('h3',null,'the two media'));
  gMed.appendChild(h('div',{class:'tag',html:'<b>above the boundary</b>'}));
  gMed.appendChild(chipRow(SUBS,'topSub'));
  gMed.appendChild(slider('topN','custom n above',PHET.nSliderLo,PHET.nCustom0,0.001,v=>fmt(v,4)));
  gMed.appendChild(h('div',{class:'tag',html:'<b>below the boundary</b>'}));
  gMed.appendChild(chipRow(SUBS,'botSub'));
  gMed.appendChild(slider('botN','custom n below',PHET.nSliderLo,PHET.nCustom0,0.001,v=>fmt(v,4)));
  gMed.appendChild(slider('angDeg','angle of incidence',0,89.9,0.1,v=>fmt(v,1)+'°'));
  const medTag=h('div',{class:'tag'}); gMed.appendChild(medTag);

  /* ---- group 3: the wave view ---- */
  const gWave=h('div',{class:'grp'},h('h3',null,'the wave'));
  gWave.appendChild(h('div',{class:'checks'},checkbox('anim','run the clock'),
    checkbox('paintField','paint the field'),checkbox('showEvanescent','show the evanescent tail')));
  gWave.appendChild(slider('waveSpeed','clock speed',0.25,3,0.25,v=>fmt(v,2)+'×'));
  const waveTag=h('div',{class:'tag'}); gWave.appendChild(waveTag);

  /* ---- group 4: the prism (PhET's Prisms screen) ---- */
  const gPri=h('div',{class:'grp'},h('h3',null,'the prism'));
  gPri.appendChild(chipRow(PRISMS,'prismId'));
  gPri.appendChild(h('div',{class:'tag',html:'<b>environment</b>'}));
  gPri.appendChild(chipRow(SUBS,'envSub'));
  gPri.appendChild(slider('envN','custom n, outside',PHET.nSliderLo,PHET.nCustom0,0.001,v=>fmt(v,4)));
  gPri.appendChild(h('div',{class:'tag',html:'<b>the prism itself</b>'}));
  gPri.appendChild(chipRow(SUBS,'prismSub'));
  gPri.appendChild(slider('prismN','custom n, prism',PHET.nSliderLo,PHET.nCustom0,0.001,v=>fmt(v,4)));
  gPri.appendChild(slider('prismRot','turn the prism',-180,180,1,v=>fmt(v,0)+'°'));
  gPri.appendChild(slider('beamY','beam height',-9,9,0.1,v=>fmt(v,1)));
  gPri.appendChild(slider('beamTilt','beam tilt',-45,45,0.5,v=>fmt(v,1)+'°'));
  gPri.appendChild(h('div',{class:'checks'},checkbox('manyRays','five rays (PhET’s fan)'),
    checkbox('showReflections','partial reflections'),checkbox('showNormals','normals at each face')));
  const priTag=h('div',{class:'tag'}); gPri.appendChild(priTag);

  /* ---- group 5: the drawing ---- */
  const gDraw=h('div',{class:'grp'},h('h3',null,'the drawing'));
  gDraw.appendChild(h('div',{class:'checks'},checkbox('showNormal','Normal'),
    checkbox('showAngles','Angles'),checkbox('showProtractor','Protractor'),
    checkbox('showMeter','intensity meter')));
  gDraw.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{
    const v=st.view; Object.assign(st,DEFAULTS); st.view=v; syncChips(); })));
  const drawTag=h('div',{class:'tag'}); gDraw.appendChild(drawTag);

  /* ---- group 6: the spectrum and the rainbow ---- */
  const gBow=h('div',{class:'grp'},h('h3',null,'the spectrum and the rainbow'));
  gBow.appendChild(slider('prismApex','prism apex angle',20,80,1,v=>fmt(v,0)+'°'));
  gBow.appendChild(h('div',{class:'tag',html:'<b>internal reflections in the drop</b>'}));
  gBow.appendChild(chipRow(KCHIPS,'bowKs',o=>{ st.bowK=parseInt(o.id,10); }));
  gBow.appendChild(chipRow(POLS,'bowPol'));
  gBow.appendChild(h('div',{class:'checks'},checkbox('bowRays','a dense fan of rays')));
  const bowTag=h('div',{class:'tag'}); gBow.appendChild(bowTag);

  /* ---- group 7: what you are looking at ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Bending Light (University of '
      +'Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s values &mdash; the substances and their indices at 650 nm, the 380&ndash;700 nm laser '
      +'range, the 1.000293&ndash;1.6 index slider, the dispersion model (a Sellmeier curve for BK7 blended '
      +'with Edlen&rsquo;s air), the s-polarised Fresnel powers its meter reads, the 0.005 and 0.001 power '
      +'floors, maxLightRaySteps = 50, MAX_ANGLE_IN_WAVE_MODE = 3.0194 rad, the 3&pi;/4 default laser '
      +'angle, the 62 &times; 43.4 red-wavelength world, the five prism prototypes and their vertices, and '
      +'the white-light set 400&ndash;690 nm in 10 nm steps &mdash; are read out of its build 1.2.5 '
      +'(docs/phets/bending-light_en.html). The Sellmeier coefficients are the published SCHOTT N-BK7 set '
      +'and the air coefficients are Edlen&rsquo;s; this file recomputes n<sub>d</sub> = 1.51680 and '
      +'V<sub>d</sub> = 64.17 from them and checks both. The colour of every wavelength comes from the CIE '
      +'1931 2&deg; observer (ISO/CIE 11664-1:2019, DOI 10.25039/CIE.DS.xvudnb9b), through '
      +'docs/phets_revised/build/blackbody-spectrum. Everything else is exact and pinned in selfTest to '
      +'build/bending-light/derive.py (scipy.minimize_scalar on the prism and the rainbow).'}));
  /* ---- group 8: the physics ---- */
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gLight,gMed,gWave,gPri,gDraw,gBow,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS){
      const cur=(key==='bowKs')?String(st.bowK):st[key];
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===cur?' on':''));
    }
  }
  /* a row this view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view;
    const mediaView=(v==='bound'||v==='wave'||v==='fres');
    gLight.hidden=false;
    rows.cb_white.row.hidden=!(v==='bound'||v==='prism'||v==='bow');
    rows.cb_laserOn.row.hidden=!(v==='bound'||v==='prism');
    gMed.hidden=!mediaView;
    rows.topN.row.hidden=(st.topSub!=='custom');
    rows.botN.row.hidden=(st.botSub!=='custom');
    gWave.hidden=(v!=='wave');
    gPri.hidden=(v!=='prism');
    rows.envN.row.hidden=(st.envSub!=='custom');
    rows.prismN.row.hidden=(st.prismSub!=='custom');
    gDraw.hidden=false;
    rows.cb_showNormal.row.hidden=(v!=='bound');
    rows.cb_showAngles.row.hidden=(v!=='bound');
    rows.cb_showMeter.row.hidden=(v!=='bound');
    rows.cb_showProtractor.row.hidden=!(v==='bound'||v==='prism');
    gBow.hidden=!(v==='spec'||v==='bow');
    rows.prismApex.row.hidden=(v!=='spec');
    rows.cb_bowRays.row.hidden=(v!=='bow');
    for(const k in rows) rows[k].sync();

    const B=boundaryModel(st);
    lightTag.innerHTML='PhET&rsquo;s laser runs '+PHET.lamMin+'&ndash;'+PHET.lamMax+' nm and its reference '
      +'wavelength is '+PHET.lamRed+' nm, where every substance has exactly the index it is named by. '
      +(st.white?'White light here is PhET&rsquo;s own set: '+WHITE_WL.length+' wavelengths, 400 to 690 nm '
        +'in tens.':'The colour drawn is the true colour of '+fmt(st.lamNm,0)+' nm.')
      +' The <b>polarisation</b> chips decide which Fresnel pair the meter and the ray brightness use; '
      +'PhET uses <b>s</b>.';
    medTag.innerHTML='PhET&rsquo;s own chooser offers air, water, glass, Mystery A, Mystery B and a custom '
      +'index; <b>diamond</b> is offered here because PhET ships the constant (2.419) even though its '
      +'chooser does not list it. PhET&rsquo;s custom slider stops at <b>1.6</b> while its custom substance '
      +'starts at <b>'+PHET.nCustom0+'</b>; this one reaches PhET&rsquo;s own starting value so that both '
      +'ends are usable. A mystery substance hides its index &mdash; that is the point of it. '
      +'Now: n<sub>1</sub> = '+fmt(B.n1,5)+', n<sub>2</sub> = '+fmt(B.n2,5)+', '
      +(isFinite(B.tc)?'&theta;<sub>c</sub> = '+fmt(B.tc*RAD,2)+'&deg;'
                      :'no critical angle (the light is entering the denser medium)')+'.';
    waveTag.innerHTML='The clock advances a fixed '+fmt(PHASE_STEP,4)+' rad of phase per frame, so the '
      +'headless suites and the captures are deterministic. PhET refuses angles past '
      +'MAX_ANGLE_IN_WAVE_MODE = 3.0194 rad in its wave view, i.e. within '
      +fmt(180-PHET.maxWaveAngle*RAD,2)+'&deg; of the boundary; this file draws them.';
    priTag.innerHTML='PhET&rsquo;s sixth prototype, the <b>diverging lens</b>, is not here: its two arc '
      +'radii could not be read unambiguously out of the minified build, and a guessed shape is not a '
      +'remake. The five that are here carry PhET&rsquo;s own vertices. Drag the laser body to move the '
      +'beam.';
    drawTag.innerHTML='1&ndash;6 switch views &nbsp; r resets &nbsp; space runs the wave clock';
    bowTag.innerHTML='The drop is water at the wavelength the light slider is set to ('
      +fmt(dropIndex(st.lamNm),5)+' relative to the air). One internal reflection gives the primary bow, two the '
      +'secondary; three would put a bow around the sun, not opposite it, which is why nobody sees it.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M,st);
      eqEl.innerHTML=eqbarHTML(M,st);
      tagEl.innerHTML=tagHTML(M,st);
      hintEl.textContent=((st.view==='bound'||st.view==='wave')?'drag the laser · ':
                          st.view==='prism'?'drag the laser · ':'')+'1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    /* the pointerDOWN does not change the drawing, so it does not mark the
       loop dirty: two flags on one path make each other's mutant equivalent
       (the buoyancy Known-bad), and the move handler is the one that owns
       the change */
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)) canvas.classList.add('dragging');
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model(),st); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key==='r'){ const v=st.view; Object.assign(st,DEFAULTS); st.view=v;
      clearMemo(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key===' '){ st.anim=!st.anim; clearMemo(); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  function frameLoop(tm){
    if(S.step()) dirty=true;
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  bound:'PhET&rsquo;s <b>Intro</b> screen. Swing the laser (drag its body) and watch three rays: the one '
   +'that came in, the one that bounced, and the one that got through. The bent one obeys '
   +'n<sub>1</sub>sin&theta;<sub>1</sub> = n<sub>2</sub>sin&theta;<sub>2</sub> exactly &mdash; it is solved, '
   +'not drawn to look right. What is worth watching is the <b>brightness</b>: the reflected ray is faint '
   +'at small angles and takes everything at grazing incidence, and when the light is trying to leave the '
   +'denser medium it disappears altogether past the critical angle. Turn on white light and the '
   +'transmitted ray becomes a fan, because every colour has its own index.',
  wave:'PhET&rsquo;s <b>wave</b> view, and the two meters from its <b>More Tools</b> screen. This is where '
   +'Snell&rsquo;s law comes from. A wave cannot tear: the crests on one side of the boundary have to meet '
   +'the crests on the other. The spacing they cut along the boundary is &lambda;/sin&theta;, so that '
   +'quantity must match &mdash; and since &lambda; = &lambda;<sub>0</sub>/n, matching it IS '
   +'n<sub>1</sub>sin&theta;<sub>1</sub> = n<sub>2</sub>sin&theta;<sub>2</sub>. The field is painted from '
   +'the exact s-polarised amplitudes, so the standing pattern above the boundary is real interference, not '
   +'decoration. Past the critical angle look below the line: the field does not stop there, it leaks in '
   +'and dies exponentially. That tail carries no power, and it is what frustrated total internal '
   +'reflection uses.',
  prism:'PhET&rsquo;s <b>Prisms</b> screen. Five shapes, at PhET&rsquo;s own sizes, traced properly: each '
   +'face is hit by solving for the intersection in closed form, and crossed with the vector form of '
   +'Snell&rsquo;s law. Nothing is scripted &mdash; where the geometry says the ray should trap itself it '
   +'does. Turn the triangle to find the <b>minimum deviation</b>, which is the classic way to measure a '
   +'refractive index; switch the prism to diamond and watch the triangle refuse to pass light at all, '
   +'because a 60&deg; apex is more than twice diamond&rsquo;s critical angle. White light disperses '
   +'because every wavelength takes its own path from the first face onward.',
  fres:'The <b>Fresnel equations</b>, which is what PhET&rsquo;s intensity meter is reading. They answer a '
   +'question Snell&rsquo;s law does not: not where the light goes, but how much. Two curves because there '
   +'are two polarisations, and they behave quite differently &mdash; R<sub>p</sub> falls to exactly zero '
   +'at Brewster&rsquo;s angle, where the reflected and refracted rays are at right angles and the dipoles '
   +'in the second medium have no way to radiate along the reflected direction. That is what polarising '
   +'sunglasses exploit. R<sub>s</sub> never vanishes. Past the critical angle both are exactly one, and '
   +'the interesting thing there is the <b>phase</b>, in the lower left panel.',
  spec:'<b>Dispersion</b>, and PhET&rsquo;s model of it. Every curve here is the same curve scaled: '
   +'PhET takes the Sellmeier index of BK7 glass, blends it with Edlen&rsquo;s formula for air, and picks '
   +'the blend so that the result passes through whatever index you named at 650 nm. For glass that is '
   +'nearly BK7 itself and is excellent; for diamond it is an extrapolation by a factor of nearly three '
   +'and should be read as a model, not a measurement. The coloured strip is not decoration &mdash; it is '
   +'the CIE 1931 colour of each wavelength, so the picture is honest about which part of the curve you '
   +'can see.',
  bow:'The <b>rainbow</b>, which is every piece of this file at once. Parallel light falls on a sphere of '
   +'water; each ray refracts in, bounces k times inside, and refracts out, and the total turn D depends '
   +'on where it struck. Nothing special happens at most impact parameters. But D has a minimum, and near '
   +'it a whole range of impact parameters leaves in almost the same direction &mdash; the rays pile up, '
   +'and that pile-up is the bow. Its angle depends on n, n depends on the wavelength, so the bow is '
   +'coloured. Two internal reflections give a second bow, fainter, reversed, and further out; between the '
   +'two there is no pile-up at all, which is the dark band Alexander of Aphrodisias noticed in the second '
   +'century.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const CONV='<h4>convention</h4><p>Every angle is measured from the <b>normal</b>, never from the surface. '
  +'The light arrives in medium 1 and leaves into medium 2; <i>s</i> polarisation has the electric field '
  +'perpendicular to the plane of incidence, <i>p</i> has it in that plane.</p>';

const DERIV={
  bound:CONV
   +'<h4>Snell&rsquo;s law</h4>'
   +EQ(1,'n<sub>1</sub> sin &theta;<sub>1</sub> = n<sub>2</sub> sin &theta;<sub>2</sub>')
   +'<p>It is not a fit and not an approximation: it is what you get by demanding that the phase be '
   +'continuous along the boundary. Solved as &theta;<sub>2</sub> = arcsin(n<sub>1</sub> sin '
   +'&theta;<sub>1</sub>/n<sub>2</sub>), it simply has no answer when the argument exceeds one.</p>'
   +'<h4>the critical angle</h4>'
   +EQ(2,'&theta;<sub>c</sub> = arcsin(n<sub>2</sub>/n<sub>1</sub>) &nbsp;&nbsp; (n<sub>2</sub> &lt; n<sub>1</sub>)')
   +'<p>At &theta;<sub>c</sub> exactly, &theta;<sub>2</sub> = 90&deg; and the transmitted ray grazes the '
   +'surface. <span class="ok">selfTest asserts that grazing to 0 and asserts R = 1 there.</span> Past it '
   +'there is no real &theta;<sub>2</sub> at all.</p>'
   +'<h4>the small-angle limit</h4>'
   +EQ(3,'&theta;<sub>2</sub> = (n<sub>1</sub>/n<sub>2</sub>)&theta;<sub>1</sub> &minus; '
        +FR('r &minus; r<sup>3</sup>','6')+'&theta;<sub>1</sub><sup>3</sup> + O(&theta;<sup>5</sup>)'
        +' , &nbsp; r = n<sub>1</sub>/n<sub>2</sub>')
   +'<p><span class="ok">The cubic coefficient is measured from the solver at four decreasing angles and '
   +'asserted against (r &minus; r&sup3;)/6 = 0.0617283950617 &mdash; a limit asserted by its RATE of '
   +'approach, not by its destination.</span></p>',
  wave:CONV
   +'<h4>where Snell&rsquo;s law comes from</h4>'
   +'<p>Inside a medium the frequency is unchanged and the speed is <i>c/n</i>, so</p>'
   +EQ(1,'&lambda; = '+FR('&lambda;<sub>0</sub>','n')+' , &nbsp;&nbsp; v = '+FR('c','n'))
   +'<p>A crest arriving at the boundary must leave as a crest. The spacing the crests cut ALONG the '
   +'boundary is therefore the same measured from either side:</p>'
   +EQ(2,FR('&lambda;<sub>1</sub>','sin &theta;<sub>1</sub>')+' = '
        +FR('&lambda;<sub>2</sub>','sin &theta;<sub>2</sub>'))
   +'<p>Put [1] into [2] and &lambda;<sub>0</sub> cancels, leaving Snell&rsquo;s law. '
   +'<span class="ok">Asserted to 1.8&times;10<sup>&minus;16</sup> over eight medium pairs.</span></p>'
   +'<h4>the field is continuous</h4>'
   +EQ(3,'1 + r<sub>s</sub> = t<sub>s</sub> , &nbsp;&nbsp; n<sub>1</sub>cos&theta;<sub>1</sub>(1 &minus; '
        +'r<sub>s</sub>) = n<sub>2</sub>cos&theta;<sub>2</sub> t<sub>s</sub>')
   +'<p>These two statements ARE the Fresnel equations; solving them gives r and t. '
   +'<span class="ok">Both are asserted to 4.4&times;10<sup>&minus;16</sup> over eight pairs and 86 '
   +'angles.</span></p>'
   +'<h4>past the critical angle</h4>'
   +EQ(4,'&kappa; = k<sub>0</sub>&radic;(n<sub>1</sub><sup>2</sup>sin<sup>2</sup>&theta;<sub>1</sub> '
        +'&minus; n<sub>2</sub><sup>2</sup>)')
   +'<p>cos&theta;<sub>2</sub> turns imaginary, so the transmitted wave becomes e<sup>&minus;&kappa;|y|</sup> '
   +'times a wave running ALONG the boundary. |r| = 1 exactly &mdash; no power crosses &mdash; but the '
   +'field is there, and a second surface brought within 1/&kappa; of the first will pick it up. '
   +'<span class="warn">PhET draws nothing below the boundary here.</span></p>',
  prism:CONV
   +'<h4>vector Snell</h4>'
   +EQ(1,'d&prime; = &eta;d + (&eta;c &minus; &radic;(1 &minus; &eta;<sup>2</sup>(1 &minus; '
        +'c<sup>2</sup>)))n&#770; , &nbsp; &eta; = n<sub>1</sub>/n<sub>2</sub>, c = &minus;d&middot;n&#770;')
   +'<p>The same law as [1] of the boundary view, written so that it can be applied to a face of any '
   +'orientation without ever forming an angle. The square root goes negative exactly when there is total '
   +'internal reflection, and the tracer reflects instead.</p>'
   +'<h4>the prism, in closed form</h4>'
   +EQ(2,'D = &theta;<sub>1</sub> + &theta;<sub>2</sub> &minus; A')
   +EQ(3,'n = '+FR('sin((A + D<sub>min</sub>)/2)','sin(A/2)'))
   +'<p>[3] is how a refractive index is measured with a spectrometer. '
   +'<span class="ok">The traced ray reproduces [2] to 2.5&times;10<sup>&minus;14</sup> degrees at four '
   +'entry angles and [3] to 6.4&times;10<sup>&minus;15</sup> degrees &mdash; which is the real test of '
   +'the intersection code, because the two routes share no arithmetic.</span></p>'
   +'<h4>when a prism cannot pass light at all</h4>'
   +'<p>At the second face the internal angle is A &minus; r<sub>1</sub>. If A &gt; 2&theta;<sub>c</sub> '
   +'there is no entry angle that keeps both faces below the critical angle. For diamond '
   +'2&theta;<sub>c</sub> = 48.85&deg;, so PhET&rsquo;s 60&deg; triangle traps every ray. '
   +'<span class="warn">That is physics, not a bug in the tracer.</span></p>',
  fres:CONV
   +'<h4>the Fresnel equations</h4>'
   +EQ(1,'r<sub>s</sub> = '+FR('n<sub>1</sub>c<sub>1</sub> &minus; n<sub>2</sub>c<sub>2</sub>',
                               'n<sub>1</sub>c<sub>1</sub> + n<sub>2</sub>c<sub>2</sub>')
        +' , &nbsp;&nbsp; r<sub>p</sub> = '+FR('n<sub>2</sub>c<sub>1</sub> &minus; n<sub>1</sub>c<sub>2</sub>',
                                               'n<sub>2</sub>c<sub>1</sub> + n<sub>1</sub>c<sub>2</sub>'))
   +'<p>with c<sub>i</sub> = cos&theta;<sub>i</sub>. The POWER fractions are R = |r|<sup>2</sup> and</p>'
   +EQ(2,'T = '+FR('n<sub>2</sub>c<sub>2</sub>','n<sub>1</sub>c<sub>1</sub>')+'|t|<sup>2</sup>')
   +'<p>The prefactor is not a convention: the transmitted beam is a different width and travels at a '
   +'different speed, and only with it does R + T come to 1. '
   +'<span class="ok">Asserted to 6.7&times;10<sup>&minus;16</sup> over eight pairs &times; 601 angles, '
   +'in both polarisations.</span></p>'
   +'<h4>Brewster&rsquo;s angle</h4>'
   +EQ(3,'&theta;<sub>B</sub> = arctan(n<sub>2</sub>/n<sub>1</sub>) , &nbsp;&nbsp; &theta;<sub>B</sub> + '
        +'&theta;<sub>2</sub> = 90&deg;')
   +'<p>The numerator of r<sub>p</sub> vanishes there and nowhere else. The second statement is the reason: '
   +'the reflected direction is exactly along the oscillation of the transmitted dipoles, and a dipole does '
   +'not radiate along its own axis. <span class="ok">Both are asserted &mdash; R<sub>p</sub> at '
   +'&theta;<sub>B</sub> is 0 to 9&times;10<sup>&minus;32</sup>, and &theta;<sub>B</sub> + '
   +'&theta;<sub>2</sub> = 90&deg; to 1.4&times;10<sup>&minus;14</sup>.</span></p>',
  spec:'<h4>the Sellmeier form</h4>'
   +EQ(1,'n<sup>2</sup>(&lambda;) = 1 + &Sigma;<sub>i</sub> '
        +FR('B<sub>i</sub>&lambda;<sup>2</sup>','&lambda;<sup>2</sup> &minus; C<sub>i</sub>'))
   +'<p class="cite">B = 1.03961212, 0.231792344, 1.01046945; C = 0.00600069867, 0.0200179144, '
   +'103.560653 &micro;m&sup2; &mdash; the published SCHOTT N-BK7 set, which is the set PhET carries.</p>'
   +'<p><span class="ok">Rather than trust it, this file recomputes the catalogue numbers from it: '
   +'n<sub>d</sub> = 1.5168000 against SCHOTT&rsquo;s 1.5168, and V<sub>d</sub> = 64.167 against 64.17. '
   +'Those two agreements validate the coefficients, the three Fraunhofer wavelengths and the evaluator at '
   +'once.</span></p>'
   +'<h4>air</h4>'
   +EQ(2,'n<sub>air</sub> = 1 + '+FR('0.05792105','238.0185 &minus; &sigma;<sup>2</sup>')+' + '
        +FR('0.00167917','57.362 &minus; &sigma;<sup>2</sup>')+' , &nbsp; &sigma; = 1/&lambda;[&micro;m]')
   +'<p class="cite">Edlen&rsquo;s standard air: 15 &deg;C, 101.325 kPa, dry, 0.03 % CO&#8322;. '
   +'It gives 1.0002771 at 589.3 nm against the published 1.0002765.</p>'
   +'<h4>PhET&rsquo;s blend</h4>'
   +EQ(3,'n(&lambda;) = s&middot;n<sub>BK7</sub>(&lambda;) + (1 &minus; s)&middot;n<sub>air</sub>(&lambda;)')
   +EQ(4,'s = '+FR('n<sub>ref</sub> &minus; n<sub>air</sub>(650)','n<sub>BK7</sub>(650) &minus; n<sub>air</sub>(650)'))
   +'<p>By construction n(650 nm) = n<sub>ref</sub> <b>exactly</b>, which selfTest checks for all six '
   +'substances. s = 0.9718 for glass, 0.6470 for water and <span class="warn">2.7589 for diamond</span> '
   +'&mdash; beyond a blend, an extrapolation.</p>',
  bow:'<h4>the deviation of one ray</h4>'
   +EQ(1,'D(&theta;) = 2&theta; &minus; 2(k+1) arcsin(sin&theta;/n) + k&pi;')
   +'<p>Refraction in turns the ray by &theta; &minus; &theta;<sub>r</sub>, each internal reflection by '
   +'&pi; &minus; 2&theta;<sub>r</sub>, and refraction out by &theta; &minus; &theta;<sub>r</sub> again.</p>'
   +'<h4>where the rays pile up</h4>'
   +EQ(2,'cos<sup>2</sup>&theta;<sub>i</sub> = '+FR('n<sup>2</sup> &minus; 1','k<sup>2</sup> + 2k'))
   +'<p>Set dD/d&theta; = 0 and use cos&theta; = n cos&theta;<sub>r</sub> d&theta;<sub>r</sub>/d&theta;. '
   +'<span class="ok">The closed form agrees with scipy&rsquo;s bounded minimiser to 3&times;10<sup>&minus;7</sup> '
   +'degrees for k = 1, 2 and 3, and the derivative there is 0 to machine precision.</span></p>'
   +'<h4>the numbers</h4>'
   +'<p>Water at 650 nm: &theta;<sub>i</sub> = 59.410&deg;, D = 137.922&deg;, bow radius '
   +'<b>42.078&deg;</b>. For k = 2: &theta;<sub>i</sub> = 71.843&deg;, radius <b>50.891&deg;</b>. '
   +'Alexander&rsquo;s band between them is 8.813&deg; wide. Violet to red spans 1.649&deg; on the '
   +'primary and 2.979&deg; the other way on the secondary.</p>'
   +'<h4>why it is faint, and polarised</h4>'
   +'<p>The internal bounce is at 40.22&deg;, below water&rsquo;s critical angle of 48.63&deg;, so it is a '
   +'PARTIAL reflection: R = 5.7 % unpolarised, and the whole path passes only 5.08 % of the incident '
   +'light. It is also close to Brewster&rsquo;s angle (36.88&deg;), where R<sub>p</sub> = 0.35 % against '
   +'R<sub>s</sub> = 11.1 % &mdash; which is why a rainbow is strongly polarised tangentially.</p>',
};
