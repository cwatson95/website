
/* ================================================================== *
 *  the scene, the dispatch, boot                                      *
 * ================================================================== */
function drawView(ctx,W,H,M){
  if(M.view==='gen') return drawGenScreen(ctx,W,H,M);
  if(M.view==='flux') return drawFluxView(ctx,W,H,M);
  if(M.view==='face') return drawFaceView(ctx,W,H,M);
  if(M.view==='lines') return drawLinesView(ctx,W,H,M);
  if(M.view==='axis') return drawAxisView(ctx,W,H,M);
  return drawNeedleView(ctx,W,H,M);
}
function makeScene(canvas){
  const S={canvas,W:1400,H:820,st:ST};
  S.ctx=()=>canvas&&canvas.getContext?canvas.getContext('2d'):null;
  S.model=()=>buildModel();
  S.draw=()=>{ drawView(canvas.getContext('2d'),S.W,S.H,buildModel()); };
  S.step=dt=>stepLive(dt);
  S.pointer=(type,x,y)=>screenPointer(type,x,y,S.W,S.H,S.ctx());
  return S;
}
/* the magnet is bolted to the wheel, so flipping its polarity is half a turn of the wheel */
function flipMagnet(st){
  st.th=wrap2pi(st.th+Math.PI);
  if(LIVE.genRot){ LIVE.genRot.om+=FLIP_KICK; LIVE.genRot.rest=false; }
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
  const S=makeScene(canvas), st=S.st;
  let dirty=false;
  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg,tr,itr){
    const toS=tr||(v=>v), toP=itr||(v=>v);
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:toP(st[key])});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=toP(st[key]); val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=toS(parseFloat(inp.value)); val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; },inp};
    return el;
  }
  const chipRows=[];
  function chipRow(list,key){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{ wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
      st[key]=o.id; syncPanel(); dirty=true; refresh(); }},o.name)); });
    chipRows.push({el:wrapEl,list,key}); return wrapEl;
  }
  const btn=(txt,fn)=>h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},txt);

  const gWater=h('div',{class:'grp'},h('h3',null,'the water'));
  gWater.appendChild(slider('flow','faucet',0,100,5,v=>fmt(v,0)+' %'));
  const waterTag=h('div',{class:'tag'}); gWater.appendChild(waterTag);

  const gBar=h('div',{class:'grp'},h('h3',null,'the bar magnet'));
  gBar.appendChild(slider('pct','strength',0,100,5,v=>fmt(v,0)+' %'));
  gBar.appendChild(h('div',{class:'btnrow'},btn('flip polarity',()=>flipMagnet(st))));
  gBar.appendChild(h('div',{class:'checks'},checkbox('genField','magnetic field (B)'),checkbox('seeInside','see inside')));

  const gCoil=h('div',{class:'grp'},h('h3',null,'the pickup coil'));
  gCoil.appendChild(slider('N','loops',1,PICK_NMAX,1,v=>fmt(v,0)));
  gCoil.appendChild(slider('area','loop area',PICK_AMIN_PCT,100,5,v=>fmt(v,0)+' %'));
  gCoil.appendChild(chipRow([{id:'bulb',name:'light bulb'},{id:'volt',name:'voltmeter'}],'indicator'));
  gCoil.appendChild(h('div',{class:'checks'},checkbox('electrons','electrons')));
  const coilTag=h('div',{class:'tag'}); gCoil.appendChild(coilTag);

  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('genCompass','compass',()=>{ LIVE.genRot=null; }),checkbox('genMeter','field meter')));
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},checkbox('bound','bound current on the magnet'),checkbox('axisH','μ₀H inside the magnet'),
    checkbox('phetCmp','PhET’s sample points')));
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  const gNd=h('div',{class:'grp'},h('h3',null,'the needle'));
  gNd.appendChild(slider('ndB','|B|',Math.log10(0.05),Math.log10(S_MAX),0.01,v=>sigf(v,3)+' G',null,p=>+Math.pow(10,p).toPrecision(3),v=>Math.log10(v)));
  gNd.appendChild(slider('ndRel','released at',1,179,1,v=>fmt(v,0)+'°'));
  gNd.appendChild(slider('ndDamp','damping γ',0,10,0.1,v=>fmt(v,1)+' /s'));
  const ndTag=h('div',{class:'tag'}); gNd.appendChild(ndTag);

  const gPref=h('div',{class:'grp'},h('h3',null,'units'));
  gPref.appendChild(chipRow([{id:'G',name:'G (gauss)'},{id:'T',name:'T (tesla)'}],'units'));
  gPref.appendChild(h('h3',null,'current flow'));
  gPref.appendChild(chipRow([{id:'electron',name:'electron'},{id:'conventional',name:'conventional'}],'flowConv'));
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('run','animate')));
  gRun.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; resetState({view:v}); DRAG.what=null; for(const k in MEMO) delete MEMO[k]; })));
  const keysTag=h('div',{class:'tag'}); gRun.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Generator (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'Measured: &mu;<sub>0</sub> = 1.25663706127&times;10<sup>&minus;6</sup> N/A&sup2; (CODATA 2022, NIST), the only measured number. '
      +'PhET&rsquo;s values (read from its 1.0.7 build): the 250 &times; 50 bar (a cylinder, MathCAD model of strength 1 G), 0&ndash;300 G, 75 % at start; the pickup coil&rsquo;s '
      +'1&ndash;4 loops and 20&ndash;100 % of 70685 mm&sup2;; 60 RPM at full flow and the drag rule; the full-scale EMF 1.2&times;10<sup>5</sup> G&middot;mm&sup2;/frame at 25 frames/s; '
      +'the 40-px needle grid and its 2(|B|/300 G)<sup>1/2.7</sup> brightness; the compass constants; the 1024 &times; 618 layout and the objects&rsquo; places. '
      +'Everything else is computed, pinned in selfTest to build/magnets-and-electromagnets/derive.py (scipy dblquad, quad, brentq, solve_ivp).'}));
  const groups={gen:[gWater,gBar,gCoil,gTools],flux:[gWater,gBar,gCoil],face:[gBar,gCoil,gShow],
                lines:[gBar,gShow],axis:[gBar,gShow],needle:[gNd]};
  [gWater,gBar,gCoil,gTools,gShow,gNd,gPref,gRun,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncPanel(){
    const v=st.view;
    for(const g of [gWater,gBar,gCoil,gTools,gShow,gNd]) g.hidden=groups[v].indexOf(g)<0;
    /* a control that is live but ignored is worse than none: dim what does nothing here */
    rows.cb_bound.inp.disabled=(v!=='lines'); rows.cb_axisH.inp.disabled=(v!=='axis'); rows.cb_phetCmp.inp.disabled=(v!=='face');
    rows.cb_electrons.inp.disabled=(v!=='gen'); rows.cb_seeInside.inp.disabled=(v!=='gen'); rows.cb_genField.inp.disabled=(v!=='gen');
    for(const k in rows) rows[k].sync();
    for(const c of chipRows) [].forEach.call(c.el.children,(b,i)=>b.className='chip'+(st[c.key]===c.list[i].id?' on':''));
    const R=genReadings(genState(st));
    waterTag.innerHTML=st.flow?'the wheel turns at '+fmt(R.rpm,1)+' RPM &mdash; '+(R.omega?sigf(2*Math.PI/R.omega,3)+' s per turn':'&mdash;')
      :'the faucet is closed: the magnet is still, so there is no EMF however strong it is';
    coilTag.innerHTML='N &times; area sets both the EMF and PhET&rsquo;s drag on the wheel ('+fmt(R.drag,4)+' here)';
    toolTag.innerHTML='drag the compass and the meter; the magnet is bolted to the wheel';
    showTag.innerHTML=v==='face'?'PhET samples B every '+fmt(PHET_SP,0)+' mm along the coil&rsquo;s vertical diameter'
      :(v==='lines'?'the bound current is the surface current a solenoid would carry to make this field'
                   :'&mu;<sub>0</sub>H = B &minus; &mu;<sub>0</sub>M inside the magnet, and points the other way');
    ndTag.innerHTML='critical damping at |B| = &gamma;&sup2;/4&kappa; = '+sigf(st.ndDamp*st.ndDamp/(4*KAPPA),3)+' G';
    keysTag.innerHTML='<b>1</b>&ndash;<b>6</b> switch views, <b>space</b> pauses, <b>f</b> flips the magnet';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='gen'?'open the faucet, then drag the tools · ':'')+'space pauses · 1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    if(canvas.setPointerCapture) canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!DRAG.what) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key===' '){ if(e.preventDefault) e.preventDefault(); st.run=!st.run; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='f'){ flipMagnet(st); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let last=null;
  function frameLoop(ts){
    const dt=(last===null)?0:Math.min(0.05,Math.max(0,(ts-last)/1000)); last=ts;
    if(st.run&&dt>0&&S.step(dt)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  gen:'This is PhET&rsquo;s Generator screen. Water from the faucet turns a wheel, the wheel carries a bar magnet round with it, and a coil of wire sits beside it. Nothing about the magnet itself makes a current: it is the CHANGE in the flux through the coil that drives one, which is Faraday&rsquo;s law, &#8496; = &minus;N d&Phi;/dt. Close the faucet and the bulb goes out at once, however strong the magnet is and however close it stands. The flux here is the real area integral of the field over the coil&rsquo;s disc, worked out for every angle of the magnet, and the EMF is its derivative times the wheel&rsquo;s angular speed: twice the loops or twice the speed gives twice the EMF. More loops and a bigger coil also drag on the wheel and slow it, as they do in PhET (and, for a different reason, in a real generator: the current you draw is paid for by the thing turning the shaft). The bulb&rsquo;s brightness and the voltmeter&rsquo;s needle are both the EMF against PhET&rsquo;s full scale.',
  flux:'The flux through the coil as the magnet turns is not a sine wave. A point dipole far away would give one &mdash; the single cosine drawn in orange &mdash; but this magnet is close enough that the coil sees its ends, so the flux is flatter on top and steeper in between, and the odd harmonics of the series carry the difference. (Only odd ones appear: half a turn reverses the magnet, so &Phi;(&theta; + &pi;) = &minus;&Phi;(&theta;), and the flux is even in &theta; because the magnet is symmetric about its axis, which kills every sine term too.) The EMF below is exactly &minus;N&omega; d&Phi;/d&theta;, so it vanishes where the flux is flat &mdash; with the magnet in line with the coil&rsquo;s axis, and again across it &mdash; and peaks where the flux falls fastest. For a cosine that would be at 90&deg;; here it is well before that, and the marked peak angle moves as the coil is made bigger.',
  face:'The flux through one loop is an integral over its whole disc, and the disc stands perpendicular to the page: most of it is off the page, where the field is weaker than it is in the plane. Green shows the average of B<sub>x</sub> round the ring at each radius, which is what the area integral weights; cyan shows B<sub>x</sub> along the coil&rsquo;s vertical diameter in the page, which is the line PhET samples (its dots, every 5 mm, each weighted by the chord it stands on). The two agree at the centre and part company towards the rim, so PhET&rsquo;s estimate of the flux comes out high &mdash; by about a tenth for the smallest coil and half again for the largest, plotted below. Nothing here is a criticism of the sim: PhET&rsquo;s EMF is deliberately a relative number against its own full scale, and a fast line sample is the sensible choice for it. This page does the integral instead, so the volts it prints are volts.',
  lines:'Field lines follow the field. Because the magnet is symmetric about its axis and the page contains that axis, every line drawn here is an exact field line, traced by small steps along B. They are spaced so that the same flux runs between each neighbouring pair when the lines are spun round the axis into tubes, which is why they crowd where the field is strong. Every B line is a closed loop: it leaves the north face, curls round, returns into the south face and runs back through the magnet to where it started, because magnetic field lines never begin or end. The dots and crosses on the magnet&rsquo;s long sides mark the bound current that circulates round its surface: a solenoid carrying the same current per unit length makes exactly the same field, inside and out. This is the magnet the wheel carries, drawn upright in its own frame.',
  axis:'Along the axis the field is elementary: it is half of &mu;<sub>0</sub>M times the difference between two cosines, one for each pole face. It is strongest at the centre, 0.981 of &mu;<sub>0</sub>M for this long thin bar, and exactly half as strong at each face, and it passes through the faces without a break. The other field, H, does not: inside the magnet &mu;<sub>0</sub>H is B minus &mu;<sub>0</sub>M, so it jumps by &mu;<sub>0</sub>M at each face and points backwards inside, from the north pole to the south pole. Far from the magnet both fall away as the point dipole, drawn in orange &mdash; and it is that same falling-off, sampled over the coil&rsquo;s face, that decides how much flux the coil catches.',
  needle:'A compass needle is a small magnet on a pivot, and in a field it behaves like a pendulum: the torque pulling it back is proportional to the sine of its angle from the field, so it swings, and friction makes the swings die away. This view releases the needle at an angle and integrates its motion, using PhET&rsquo;s constants for the needle&rsquo;s response to the field and its damping. For small swings the solution is the damped oscillator, drawn in orange; at large angles the needle lingers near the top of its swing and the period grows, exactly as for a pendulum, by the factor given by the complete elliptic integral. The period of small swings is 2&pi;/&radic;(&kappa;|B|), so it halves when the field is four times stronger: timing a swinging magnet is how Gauss first measured the strength of the Earth&rsquo;s field in 1832. On the generator screen the same rotor rides the turning field, and lags it.'
};
