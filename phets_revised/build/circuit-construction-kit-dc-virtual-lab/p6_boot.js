/* ================================================================== *
 *  boot -- panel, tabs, handlers, frame loop                          *
 * ================================================================== */
const LOG_RHO=[Math.log10(RHO_MIN),Math.log10(RHO_MAX)];
const LOG_RBAT=[Math.log10(BATT_R_MIN),Math.log10(BATT_R_MAX)];
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
  /* a slider on a value held in the state; get/set map it both ways */
  function slider(key,lab2,lo,hi,step2,get,set,fmtf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.innerHTML=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); val.innerHTML=fmtf(get()); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,get,set){
    const inp=h('input',{type:'checkbox'}); inp.checked=get();
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ set(inp.checked); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=get(); },inp};
    return el;
  }
  const chipRows=[];
  function chipRow(list,isOn,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{ wrapEl.appendChild(h('button',{class:'chip'+(isOn(o)?' on':''),onclick:()=>{ onPick(o); syncPanel(); dirty=true; refresh(); }},o.name)); });
    chipRows.push({el:wrapEl,list,isOn});
    return wrapEl;
  }
  const btn=(txt,fn)=>h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},txt);
  const selEl=()=>st.sel!==null?elById(st.circ,st.sel):null;

  /* the circuit: presets */
  const gCirc=h('div',{class:'grp'},h('h3',null,'the circuit'));
  gCirc.appendChild(chipRow(PRESET_ORDER.map(k=>({id:k,name:PRESET_NAMES[k]})),o=>st.preset===o.id,o=>{ applyPreset(st,o.id); DRAG.what=null; }));
  const circTag=h('div',{class:'tag'}); gCirc.appendChild(circTag);

  /* the selected part */
  const gSel=h('div',{class:'grp'},h('h3',null,'the selected part'));
  const selTag=h('div',{class:'tag'}); gSel.appendChild(selTag);
  gSel.appendChild(slider('volt','voltage, V',0,120,0.1,()=>{ const e=selEl(); return e&&isBattery(e.type)?e.E:9; },
    v=>{ const e=selEl(); if(e&&isBattery(e.type)){ e.E=v; circuitEdited(st); } },v=>fmt(v,selEl()&&selEl().type==='xbattery'?0:1)+' V'));
  gSel.appendChild(slider('res','resistance, &Omega;',0,120,0.1,()=>{ const e=selEl(); return e&&e.R!==undefined?e.R:10; },
    v=>{ const e=selEl(); if(e&&isEditable(e.type)&&e.R!==undefined){ e.R=v; circuitEdited(st); } },v=>fmt(v,selEl()&&TYPES[selEl().type].dp===0?0:1)+' &Omega;'));
  gSel.appendChild(slider('rating','current rating, A',0.5,20,0.1,()=>{ const e=selEl(); return e&&e.type==='fuse'?e.rating:4; },
    v=>{ const e=selEl(); if(e&&e.type==='fuse'){ e.rating=v; circuitEdited(st); } },v=>fmt(v,1)+' A'));
  const bDel=btn('delete',()=>{ const e=selEl(); if(e){ deleteElement(st.circ,e.id); st.sel=null; circuitEdited(st); } });
  const bRev=btn('reverse',()=>{ const e=selEl(); if(e&&isBattery(e.type)){ reverseBattery(st.circ,e.id); circuitEdited(st); } });
  const bSw=btn('toggle the switch',()=>{ const e=selEl(); if(e&&e.type==='switch'){ e.closed=!e.closed; circuitEdited(st); } });
  const bFuse=btn('repair the fuse',()=>{ const e=selEl(); if(e&&e.type==='fuse'){ e.tripped=false; circuitEdited(st); } });
  const bSplit=btn('split the junction',()=>{ if(st.selV!==null){ splitVertex(st.circ,st.selV); st.selV=null; circuitEdited(st); } });
  gSel.appendChild(h('div',{class:'btnrow'},bDel,bRev,bSw)); gSel.appendChild(h('div',{class:'btnrow'},bFuse,bSplit));

  /* how the lab looks */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(chipRow([{id:'lifelike',name:'lifelike'},{id:'schematic',name:'schematic'}],o=>st.look===o.id,o=>{ st.look=o.id; }));
  gShow.appendChild(h('div',{class:'checks'},checkbox('cur','show current',()=>st.showCurrent,v=>{ st.showCurrent=v; })));
  gShow.appendChild(chipRow([{id:'electrons',name:'electrons'},{id:'conventional',name:'conventional'}],o=>st.carrier===o.id,o=>{ st.carrier=o.id; }));
  gShow.appendChild(h('div',{class:'checks'},checkbox('labels','labels',()=>st.showLabels,v=>{ st.showLabels=v; }),
    checkbox('values','values',()=>st.showValues,v=>{ st.showValues=v; })));
  gShow.appendChild(chipRow(ZOOMS.map(z=>({id:z,name:'zoom '+z+'×'})),o=>st.zoom===o.id,o=>{ st.zoom=o.id; }));

  /* PhET's advanced panel */
  const gAdv=h('div',{class:'grp'},h('h3',null,'advanced'));
  gAdv.appendChild(slider('rho','wire resistivity',LOG_RHO[0],LOG_RHO[1],0.01,()=>Math.log10(st.rho),
    v=>{ st.rho=Math.pow(10,v); if(Math.abs(v-LOG_RHO[0])<1e-9) st.rho=RHO_MIN; if(Math.abs(v-LOG_RHO[1])<1e-9) st.rho=RHO_MAX; },v=>sigf(Math.pow(10,v),2)+' &Omega;m'));
  gAdv.appendChild(slider('rbat','battery resistance',LOG_RBAT[0],LOG_RBAT[1],0.01,()=>Math.log10(st.rbat),
    v=>{ st.rbat=Math.pow(10,v); if(Math.abs(v-LOG_RBAT[0])<1e-9) st.rbat=BATT_R_MIN; if(Math.abs(v-LOG_RBAT[1])<1e-9) st.rbat=BATT_R_MAX; },v=>sigf(Math.pow(10,v),2)+' &Omega;'));
  gAdv.appendChild(h('div',{class:'checks'},checkbox('real','add real bulbs',()=>st.realBulbs,v=>{ st.realBulbs=v; })));
  const advTag=h('div',{class:'tag'}); gAdv.appendChild(advTag);

  /* the meters */
  const gMet=h('div',{class:'grp'},h('h3',null,'meters'));
  gMet.appendChild(h('div',{class:'checks'},checkbox('vm','voltmeter',()=>st.vm.on,v=>{ st.vm.on=v; }),
    checkbox('am','non-contact ammeter',()=>st.am.on,v=>{ st.am.on=v; })));
  const metTag=h('div',{class:'tag'}); gMet.appendChild(metTag);

  /* the part the rest of the circuit is seen from */
  const gFoc=h('div',{class:'grp'},h('h3',null,'the part to look from'));
  const stepFocus=d=>{ const SOL=S.model().sol, list=st.circ.els.filter(e=>SOL.onK.has(e.id)&&e.type!=='wire');
    if(!list.length) return; const cur=focusElement(st,SOL), j=list.findIndex(e=>e.id===cur);
    st.thevEl=list[((j<0?0:j+d)%list.length+list.length)%list.length].id; };
  gFoc.appendChild(h('div',{class:'btnrow'},btn('previous part',()=>stepFocus(-1)),btn('next part',()=>stepFocus(1))));
  const focTag=h('div',{class:'tag'}); gFoc.appendChild(focTag);

  const gReset=h('div',{class:'grp'},h('h3',null,'start again'));
  gReset.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; resetState({view:v}); DRAG.what=null; })));
  const keysTag=h('div',{class:'tag'}); gReset.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Circuit Construction Kit: DC - Virtual Lab (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'PhET&rsquo;s values, read from its 1.5.2 build: every part&rsquo;s length, value and range; wire resistivity 10<sup>&minus;10</sup>&ndash;0.0168 &Omega;m through a 5&times;10<sup>&minus;4</sup> m&sup2; section at 0.5 mm per unit; '
      +'battery resistance 10<sup>&minus;4</sup>&ndash;10 &Omega;; 1.1&times;10<sup>&minus;10</sup> &Omega; for a zero; the fuse&rsquo;s 0.06/rating; the brightness rule; the real bulb&rsquo;s law; fire at 15 A; the 30-unit snap and 11.2-unit probe radius; '
      +'charges 25 units/s per ampere under a speed limit. Household objects as in 1.5.2 (eraser and dollar bill 10<sup>6</sup> &Omega;; PhET&rsquo;s model notes say 10<sup>9</sup>). '
      +'No measured constants are needed. Every solution is pinned in selfTest to build/circuit-construction-kit-dc-virtual-lab/derive.py, which solves the same circuits exactly, in rational arithmetic.'}));
  [gCirc,gSel,gShow,gAdv,gMet,gFoc,gReset,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){ for(const r of chipRows) [].forEach.call(r.el.children,(b,i)=>b.className='chip'+(r.isOn(r.list[i])?' on':'')); }
  function syncPanel(){
    const v=st.view, e=selEl();
    if(st.sel!==null&&!e) st.sel=null;
    if(st.selV!==null&&!vById(st.circ,st.selV)) st.selV=null;
    gSel.hidden=(v!=='lab'); gShow.hidden=(v!=='lab'); gAdv.hidden=(v!=='lab'); gMet.hidden=(v!=='lab'); gFoc.hidden=(v!=='thev');
    /* only the controls that act on the selection are shown, with its ranges */
    const T=e?TYPES[e.type]:null;
    rows.volt.row.hidden=!(e&&isBattery(e.type)); rows.res.row.hidden=!(e&&isEditable(e.type)&&e.R!==undefined); rows.rating.row.hidden=!(e&&e.type==='fuse');
    if(e&&isBattery(e.type)){ rows.volt.inp.min=T.lo; rows.volt.inp.max=T.hi; rows.volt.inp.step=T.step; }
    if(e&&e.R!==undefined&&isEditable(e.type)){ rows.res.inp.min=T.lo; rows.res.inp.max=T.hi; rows.res.inp.step=T.step; }
    bDel.hidden=!e; bRev.hidden=!(e&&isBattery(e.type)); bSw.hidden=!(e&&e.type==='switch'); bFuse.hidden=!(e&&e.type==='fuse');
    bFuse.disabled=!(e&&e.type==='fuse'&&e.tripped);
    const vv=st.selV!==null?vById(st.circ,st.selV):null;
    bSplit.hidden=!(vv&&elsAt(st.circ,vv.id).length>=2);
    for(const k in rows) rows[k].sync();
    syncChips();
    circTag.innerHTML=st.preset==='custom'?'your own circuit: '+st.circ.els.length+' part'+(st.circ.els.length===1?'':'s'):'drag any part in the lab to make it your own';
    selTag.innerHTML=e?'<b>'+elTag(st.circ,e)+'</b>'+(e.type==='switch'?(e.closed?' &mdash; closed':' &mdash; open'):'')+(e.type==='fuse'&&e.tripped?' &mdash; <span class="r">blown</span>':'')
      :(vv?'a joint of '+elsAt(st.circ,vv.id).length+' part'+(elsAt(st.circ,vv.id).length===1?'':'s'):'tap a part in the lab to edit it; tap a joint to split it');
    advTag.innerHTML='100 units of wire: <b>'+plain(fmtR(wireR(100,st.rho)))+'</b>; every battery: r = <b>'+plain(fmtR(st.rbat))+'</b>';
    metTag.innerHTML='drag a meter out of the toolbox, or tick it here; drag its probes onto the circuit, drop it back on the toolbox to put it away';
    const SOL=S.model().sol, f=focusElement(st,SOL), fe=f!==null?elById(st.circ,f):null;
    focTag.innerHTML=fe?'looking from the <b>'+elTag(st.circ,fe)+'</b>':'no part in the circuit';
    keysTag.innerHTML='<b>1</b>&ndash;<b>5</b> switch views &middot; <b>delete</b> removes the selected part &middot; <b>x</b> splits the selected joint';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='lab'?'drag parts from the toolbox · drop an end on an end · tap to select · 1–5 switch views'
        :st.view==='thev'?'choose the part in the lab, or step through with the buttons · 1–5 switch views':'1–5 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); syncPanel(); refresh(); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!DRAG.what||DRAG.what==='none') return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  canvas.addEventListener('wheel',e=>{ e.preventDefault(); if(S.wheel(e.deltaY)){ syncPanel(); dirty=true; refresh(); } },{passive:false});

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if((e.key==='Delete'||e.key==='Backspace')&&st.sel!==null){ deleteElement(st.circ,st.sel); st.sel=null; circuitEdited(st); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='x'&&st.selV!==null){ if(splitVertex(st.circ,st.selV)){ st.selV=null; circuitEdited(st); } syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  /* the loop paints when a handler marked it dirty, and every frame while
     charges are moving in the lab */
  function frameLoop(){
    try{ if(S.step()) dirty=true; }catch(e){ fail(e); }
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  lab:'This is PhET&rsquo;s bench. Drag a part out of the toolbox, then drag one of its ends onto the end of another part: within 30 units the dashed ring '
    +'shows where it will join, and on release the two ends become one joint. A wire stretches to follow its ends; a battery, a bulb or a resistor keeps its '
    +'length and swings about its other end. Tap a part to select it and edit it in the panel (a switch opens or closes when tapped), tap a joint and split it with the button that appears, '
    +'and drop a part back on the toolbox to put it away. The circuit is solved again after every change, and nothing in the solution is approximate: '
    +'every node&rsquo;s voltage and every branch&rsquo;s current come out of one linear system, built from Kirchhoff&rsquo;s current law at each node and each part&rsquo;s '
    +'own law v<sub>a</sub> &minus; v<sub>b</sub> = R i &minus; E, and the readout checks both of Kirchhoff&rsquo;s laws on the answer. The moving charges show the '
    +'current, 25 units a second per ampere as in PhET, as electrons drifting against it or as conventional positive charge. Bulbs glow by PhET&rsquo;s '
    +'brightness rule, a battery or a resistor carrying 15 A catches fire, and a fuse blows when its rating is passed. Try the household objects: the coin '
    +'and the paper clip are conductors, the pencil&rsquo;s graphite is 25 ohms, and the eraser and the dollar bill are insulators of a million ohms.',
  graph:'A circuit is a graph. Every joint is a node and every part is a branch between two nodes, wires included, since a wire has resistance and PhET&rsquo;s '
    +'solver keeps it. A spanning tree (cyan) reaches every node without closing a loop; each remaining branch (dashed) closes exactly one loop through the '
    +'tree, which is why a circuit of B branches, N nodes and C separate pieces has exactly B &minus; N + C independent loops. Kirchhoff saw this in 1847. '
    +'Modified nodal analysis writes one equation for each node (the current law: what flows in flows out) and one for each branch (its own law), and '
    +'solves for a voltage at every node but one reference in each piece and a current in every branch. The matrix is that system cell by cell: the '
    +'incidence matrix A in the top right, its transpose on the left, the resistances down the diagonal. Keeping every current as an unknown (PhET keeps '
    +'only the batteries&rsquo; and the zero-ohm parts&rsquo;) makes the current law a row of the system, so it holds to rounding error; the strip below measures '
    +'both laws on the solution itself.',
  power:'Energy balances exactly in a circuit, and here it balances to the last bit. Each battery&rsquo;s EMF does work E i on the charge it drives; each '
    +'resistance, the battery&rsquo;s own internal resistance included, turns i&sup2;R into heat. Tellegen&rsquo;s theorem says why the two must agree: for any '
    +'branch currents that obey the current law and any branch voltages that come from node potentials, the sum of v i over all the branches is zero, '
    +'whatever the parts are. The waterfall climbs by each EMF&rsquo;s share and steps down by each loss, and lands back on zero. Below is PhET&rsquo;s rule for '
    +'how bright a bulb looks: logarithmic in its power and full at 2 kW, so a 10-ohm bulb on a 9-volt battery, taking 8.1 W, glows at about a fifth.',
  thev:'Pick any part and look back into the rest of the circuit through its two terminals. Th&eacute;venin&rsquo;s theorem says that whatever is there acts '
    +'exactly like one EMF V<sub>th</sub> behind one resistance R<sub>th</sub>: V<sub>th</sub> is the voltage across the gap with the part taken out, and '
    +'R<sub>th</sub> is the resistance between the two terminals with every battery&rsquo;s EMF set to zero. So the rest of the circuit has a straight-line '
    +'characteristic, v = V<sub>th</sub> &minus; R<sub>th</sub> i (orange); the part has its own (green); and the circuit sits where they cross, which '
    +'reproduces the full solution exactly. The same two numbers answer the designer&rsquo;s question: a load takes V<sub>th</sub>&sup2;R/(R<sub>th</sub> + R)&sup2;, '
    +'largest when R = R<sub>th</sub>, which is why a battery&rsquo;s internal resistance limits what it can deliver. A real bulb&rsquo;s characteristic is curved, and '
    +'the crossing is then a graphical solution of a non-linear circuit.',
  super:'A circuit of batteries and resistors is linear: double every EMF and every current doubles. So the currents several batteries drive together are '
    +'the sum of the currents each would drive alone, with the others&rsquo; EMFs set to zero and their internal resistances left in place. Each row builds '
    +'one part&rsquo;s current from those single-battery contributions and lands exactly on the full solution. With two batteries pushing against each other '
    +'some contributions point backwards, and a part can carry less current than either battery would give it alone. Real bulbs are not linear, so in a '
    +'circuit with one they are frozen at their present resistance, and the picture decomposes that operating point.',
};
