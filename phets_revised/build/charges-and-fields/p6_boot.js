
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
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  /* a slider on one coordinate of an object in the state (the probe) */
  function slider2(obj,key,lab2,lo,hi,step2,fmtf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[obj][key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[obj][key]; val.textContent=fmtf(st[obj][key]); };
    inp.addEventListener('input',()=>{ st[obj][key]=parseFloat(inp.value); val.textContent=fmtf(st[obj][key]); syncPanel(); dirty=true; refresh(); });
    rows[obj+'.'+key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; },inp};
    return el;
  }
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(onPick) onPick(o); else st[key]=o.id;
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const btn=(txt,fn)=>h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},txt);

  const gCh=h('div',{class:'grp'},h('h3',null,'the charges'));
  const presetChips=chipRow(PRESETS,'preset',o=>applyPreset(st,o.id)); gCh.appendChild(presetChips);
  const chTag=h('div',{class:'tag'}); gCh.appendChild(chTag);

  let lastPlot=null;          /* the last plot's verdict, so a refusal says why */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},checkbox('showE','electric field'),checkbox('dirOnly','direction only'),checkbox('showV','voltage'),
    checkbox('showVals','values'),checkbox('showGrid','grid'),checkbox('showVS','voltage sensor'),checkbox('showTape','tape measure')));
  gShow.appendChild(h('div',{class:'btnrow'},btn('plot equipotential',()=>{ lastPlot=plotEquipotential(st); }),btn('clear equipotentials',()=>{ st.eqSeeds=[]; })));
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  const gLines=h('div',{class:'grp'},h('h3',null,'field lines'));
  gLines.appendChild(slider('nLines','lines per charge',4,32,2,v=>fmt(v,0)));
  gLines.appendChild(slider('famDV','equipotentials every, V',1,10,1,v=>fmt(v,0)+' V'));
  gLines.appendChild(h('div',{class:'checks'},checkbox('showFam','equipotentials'),checkbox('showNulls','null points')));
  const linesTag=h('div',{class:'tag'}); gLines.appendChild(linesTag);

  const gLand=h('div',{class:'grp'},h('h3',null,'the landscape'));
  gLand.appendChild(slider('vcap','clip at ±, V',10,100,5,v=>fmt(v,0)+' V'));
  gLand.appendChild(slider('camTheta','azimuth',-PI,PI,0.01,v=>fmt(v/DEG,0)+'°'));
  gLand.appendChild(slider('camPhi','elevation',0.05,1.5,0.01,v=>fmt(v/DEG,0)+'°'));
  gLand.appendChild(h('div',{class:'checks'},checkbox('landEq','plotted equipotentials')));
  gLand.appendChild(h('div',{class:'btnrow'},btn('reset the camera',()=>{ S.resetCam(); })));
  const landTag=h('div',{class:'tag'}); gLand.appendChild(landTag);

  const gSup=h('div',{class:'grp'},h('h3',null,'the probe'));
  gSup.appendChild(slider2('probe','x','probe x, m',PLANE.x0,PLANE.x1,0.01,v=>fmt(v,2)));
  gSup.appendChild(slider2('probe','y','probe y, m',PLANE.y0,PLANE.y1,0.01,v=>fmt(v,2)));
  const supTag=h('div',{class:'tag'}); gSup.appendChild(supTag);

  const gFar=h('div',{class:'grp'},h('h3',null,'the ray'));
  gFar.appendChild(slider('farTheta','direction',-180,180,1,v=>fmt(v,0)+'°'));
  const farTag=h('div',{class:'tag'}); gFar.appendChild(farTag);

  const gReset=h('div',{class:'grp'},h('h3',null,'start again'));
  gReset.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; resetState({view:v}); DRAG.what=null; })));
  const keysTag=h('div',{class:'tag'}); gReset.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Charges and Fields (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'Measured: &epsilon;<sub>0</sub> = 8.8541878188&times;10<sup>&minus;12</sup> F/m (CODATA 2022, NIST), the only measured number. '
      +'PhET&rsquo;s values (read from its 1.0.67 build): the 8 m &times; 5 m plane and its bin, the 0.5-m arrow and 0.1-m voltage grids, the &plusmn;40 V and 5 V/m '
      +'saturations, 15 px per V/m at 128 px/m for the sensor arrows, no equipotential within 3 cm of a charge; PhET&rsquo;s k is 9 V&middot;m/nC. '
      +'Everything else is exact superposition, pinned in selfTest to build/charges-and-fields/derive.py (scipy brentq, solve_ivp, fsolve, quad).'}));
  [gCh,gShow,gLines,gLand,gSup,gFar,gReset,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){
    [].forEach.call(presetChips.children,(b,i)=>b.className='chip'+(PRESETS[i].id===st.preset?' on':''));
  }
  function syncPanel(){
    const v=st.view;
    gShow.hidden=(v!=='plane'); gLines.hidden=(v!=='lines'); gLand.hidden=(v!=='land'); gSup.hidden=(v!=='super'); gFar.hidden=(v!=='far');
    /* a control that is live but ignored is worse than none: dim what does nothing */
    rows.cb_dirOnly.inp.disabled=!st.showE; rows.famDV.inp.disabled=!st.showFam;
    for(const k in rows) rows[k].sync();
    chTag.innerHTML=st.preset==='custom'?'your own arrangement: '+st.charges.length+' charge'+(st.charges.length===1?'':'s'):'drag the charges in the plane, field-lines and superposition views';
    showTag.innerHTML=lastPlot&&!lastPlot.ok?'<span class="r">cannot plot: '+lastPlot.why+'</span>':'the sensor&rsquo;s plot button (or <b>e</b>) traces the equipotential through its crosshair; <b>c</b> clears them';
    linesTag.innerHTML='lines from the majority sign; equipotentials from a 4-cm grid, up to &plusmn;'+V_SAT+' V';
    landTag.innerHTML='drag to orbit, scroll to zoom, <b>r</b> resets the camera';
    supTag.innerHTML='drag P, or the charges, on the plane';
    farTag.innerHTML='the ray starts at the expansion centre (orange &times; in the inset)';
    keysTag.innerHTML='<b>1</b>&ndash;<b>5</b> switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='plane'?'drag charges and sensors from the bin · e plots, c clears · 1–5 switch views'
        :st.view==='land'?'drag to orbit · scroll to zoom · r resets the camera · 1–5 switch views'
        :st.view==='far'?'turn the ray with the slider · 1–5 switch views':'drag the charges · 1–5 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); syncChips(); syncPanel(); roEl.innerHTML=readoutHTML(S.model()); dirty=true; }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncChips(); syncPanel(); roEl.innerHTML=readoutHTML(S.model()); tagEl.innerHTML=tagHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncChips(); dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  canvas.addEventListener('wheel',e=>{ e.preventDefault(); if(S.wheel(e.deltaY)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); } },{passive:false});

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key==='e'){ lastPlot=plotEquipotential(st); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='c'){ st.eqSeeds=[]; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ S.resetCam(); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  /* nothing here moves by itself: the loop paints only what a handler marked */
  function frameLoop(){
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  plane:'This is PhET&rsquo;s screen. Every charge on the plane is a point charge of one nanocoulomb, and every reading is the exact sum of what each '
    +'charge would do alone: a potential k q/r and a field k q/r&sup2; that points away from a positive charge and toward a negative one. The arrows '
    +'show the direction of the field everywhere at once and their brightness shows its strength, fading out below 5 V/m, so the field of a lone charge '
    +'visibly dies away with distance; tick <b>direction only</b> to see the pattern without the fading. The voltage map colours each 10-cm cell by the '
    +'potential. Put the voltage sensor anywhere and press <b>plot</b>: the curve it draws joins every point at the same potential, and it crosses the '
    +'arrows at right angles everywhere, because moving along it takes no work. The E-field sensors read the size and direction of the field at a point, '
    +'and the tape measures distances and, here, the potential difference between its two ends.',
  lines:'Faraday&rsquo;s way of seeing a field. A field line runs along E everywhere, so it starts on a positive charge and ends on a negative one, and '
    +'the equipotentials cross it at right angles. Where equally spaced equipotentials crowd together the field is strong, because the same step in '
    +'potential happens over a shorter distance. The orange marks are the null points, where the fields of the charges cancel exactly: between two like '
    +'charges it is a saddle of the potential, and lines run toward it and turn away. These are ordinary three-dimensional charges held in a plane, so the '
    +'plane is a slice through their field. That is why the number of lines reaching a charge is not proportional to its charge, and why three equal '
    +'charges make a point at their centre where the lines in the plane run in and stop: the potential there is a minimum within the plane, the field '
    +'turns out of the plane along z, and a positive charge confined to the plane would sit there stably. Along z the same point is a maximum, so Earnshaw&rsquo;s '
    +'theorem, which forbids a stable equilibrium in free space, is not broken.',
  land:'The voltage map, stood up as a landscape. Height is potential, so a positive charge is a peak whose sides fall as 1/r and a negative charge is a '
    +'well. The electric field is minus the gradient of the potential: at every point it points straight downhill, along the steepest descent, and its '
    +'size is the steepness. A positive test charge released on this surface would run downhill and a negative one would climb. Two like charges make two '
    +'peaks with a saddle between them, the null point of the field-lines view. The equipotentials you plot on the plane appear here as horizontal loops '
    +'at their own height: an equipotential is a contour line of this map. The peaks are infinitely high at the charges themselves, so the surface is '
    +'clipped at the height you choose, and the clip is printed on the canvas.',
  super:'The principle of superposition is the whole model. The field of several charges is the vector sum of the fields each would make alone, and the '
    +'potential is the ordinary sum of their potentials. Drag the probe and watch the chain: every arrow points along the line from its charge, away from '
    +'a positive one and toward a negative one, its length falls off as the inverse square of the distance, and laid head to tail the arrows land exactly '
    +'on the total field. The potential adds without directions, only with signs. So the two sums behave very differently: on the perpendicular bisector '
    +'of a dipole the potential is exactly zero while the field is not, and midway between two like charges the field is zero while the potential is not.',
  far:'From far away any set of charges looks simple. Beyond the farthest charge the potential along a ray is exactly a power series in 1/r, the Legendre '
    +'expansion of each charge&rsquo;s 1/|r &minus; d|: the 1/r term is the net charge, the 1/r&sup2; term the dipole moment, the 1/r&sup3; term the '
    +'quadrupole moment, and so on. The first term that does not vanish takes over at large distance, which is why a net charge falls off as 1/r, a '
    +'neutral pair as 1/r&sup2; and a square of alternating charges as 1/r&sup3;, the slope of the line on these log axes. The limit is also taken '
    +'numerically: r<sup>&ell;+1</sup> V(r) at 50 m and 100 m, extrapolated to infinite distance, agrees with the exact coefficient to between six and ten '
    +'digits, depending on how quickly the next order dies away (the readout prints both). '
    +'Point the ray where the leading moment has no component, along the perpendicular bisector of a dipole, and a different order takes over, or none does.',
};
