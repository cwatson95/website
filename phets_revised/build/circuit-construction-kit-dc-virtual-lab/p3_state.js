/* ================================================================== *
 *  state, the model of each view, readout, equation bar, tag           *
 * ================================================================== */
const TABS=[['lab','the lab'],['graph','nodes and branches'],['power','the power budget'],
            ['thev','the rest of the circuit'],['super','one battery at a time']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', text:'#cfd4de', dim:'#8b93a6',
           faint:'#6f7789', edge:'#242a3a', panel:'#10131b', panelEdge:'#2a2f3d', ink:'#e9ecf2', bg:'#070b18',
           fire:'#e8843a', fire2:'#f2c14e', probeRed:'#d9534f', probeBlack:'#232838'};
const RO_W=306;
const PRESET_NAMES={empty:'empty',bulb:'one bulb',series:'series',parallel:'parallel',bridge:'Wheatstone bridge',
                    twobat:'two batteries',short:'short circuit'};
function clone(o){ return JSON.parse(JSON.stringify(o)); }
/* PhET's defaults: lifelike, current shown as electrons, labels on, values
   off, zoom 1, real bulbs off, the thinnest wire and the stiffest battery.
   PhET opens on an empty bench; this opens on one bulb so every view has a
   circuit to show ("empty" gives PhET's start). */
const DEFAULTS={view:'lab', preset:'bulb', circ:presetCircuit('bulb'),
  rho:RHO_MIN, rbat:BATT_R_MIN, realBulbs:false,
  look:'lifelike', showCurrent:true, carrier:'electrons', showLabels:true, showValues:false,
  zoom:1, sel:null, selV:null, thevEl:null,
  vm:{on:false, bx:0, by:215, rx:51, ry:100, kx:-51, ky:100},
  am:{on:false, bx:250, by:175, px:150, py:20},
  phase:{}, clock:0};
const ST=clone(DEFAULTS);
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function resetState(over){ Object.assign(ST,clone(DEFAULTS),over?clone(over):{}); for(const k in MEMO) delete MEMO[k]; }
function applyPreset(st,key){ st.preset=key; st.circ=presetCircuit(key); st.sel=null; st.selV=null; st.thevEl=null; st.phase={}; }
function globOf(st){ return {rho:st.rho,rbat:st.rbat}; }
function circKey(st){ return JSON.stringify([st.circ.verts,st.circ.els,st.rho,st.rbat]); }
/* every edit to the circuit passes through here: the preset chip lets go */
function circuitEdited(st){ st.preset='custom'; }
function solutionOf(st){
  let sol=memo('sol',circKey(st),()=>solveCircuit(st.circ,globOf(st)));
  /* a fuse that blew during that solve changed the circuit: key it again */
  if(sol.trips.length) sol=memo('sol',circKey(st),()=>solveCircuit(st.circ,globOf(st)));
  return sol;
}
/* the part the analysis views look from: the selection if it is in the
   circuit, else the first bulb, resistor or household object, else the
   first part that is not a wire */
function focusElement(st,SOL){
  const want=st.thevEl!==null?st.thevEl:st.sel;
  if(want!==null&&SOL.onK.has(want)) return want;
  for(const e of st.circ.els) if(SOL.onK.has(e.id)&&(isBulb(e.type)||['resistor','xresistor','pencil','tpencil','eraser','bill'].indexOf(e.type)>=0)) return e.id;
  for(const e of st.circ.els) if(SOL.onK.has(e.id)&&e.type!=='wire') return e.id;
  return null;
}
function elName(e){ return e?TYPES[e.type].name:''; }
/* a short unique tag for a part: its name and its number of that kind */
function elTag(C,e){ let n=0; for(const x of C.els){ if(x.type===e.type) n++; if(x===e) break; }
  return TYPES[e.type].name+(countType(C,e.type)>1?' '+n:''); }

function buildModel(){
  const st=ST, M={view:st.view, st};
  M.sol=solutionOf(st);
  M.scale=chargeScale(M.sol.Imax);
  M.vm=st.vm.on?voltmeterReading(st.circ,M.sol,[st.vm.rx,st.vm.ry],[st.vm.kx,st.vm.ky]):null;
  M.am=st.am.on?ammeterReading(st.circ,M.sol,st.am.px,st.am.py):null;
  M.sel=st.sel!==null?elById(st.circ,st.sel):null;
  M.focus=focusElement(st,M.sol);
  if(st.view==='thev'&&M.focus!==null) M.thev=memo('thev',circKey(st)+'|'+M.focus,()=>theveninOf(M.sol,M.focus));
  if(st.view==='super') M.sup=memo('sup',circKey(st),()=>superpose(M.sol));
  if(st.view==='power') M.bud=powerBudget(M.sol,st.circ);
  return M;
}
/* the power ledger: each EMF's E i, each resistance's i^2 R (a battery's own
   r included), and Tellegen's sum of (v_a - v_b) i over every branch */
function powerBudget(SOL,C){
  const src=[], sink=[];
  let gen=0, dis=0, tel=0, scale=0;
  SOL.net.br.forEach((e,k)=>{ const i=SOL.sol.i[k], u=SOL.sol.v[e.a]-SOL.sol.v[e.b];
    tel+=u*i; scale=Math.max(scale,Math.abs(u*i),Math.abs(e.E*i));
    if(e.kind==='B'){ src.push({el:e.el,P:e.E*i}); gen+=e.E*i; sink.push({el:e.el,P:i*i*e.R,internal:true}); dis+=i*i*e.R; }
    else { sink.push({el:e.el,P:i*i*e.R}); dis+=i*i*e.R; } });
  return {src,sink,gen,dis,tel,scale};
}

/* ================================================================== *
 *  number formats                                                     *
 * ================================================================== */
/* SI prefixes, written as literal glyphs (µ and the minus sign) so the same
   string serves the HTML readout and the canvas (Known-bad: &micro; is not in
   plain()'s table) */
const SI_PRE=[[1e9,'G'],[1e6,'M'],[1e3,'k'],[1,''],[1e-3,'m'],[1e-6,'µ'],[1e-9,'n'],[1e-12,'p']];
function siFmt(x,unit,sig){
  if(!isFinite(x)) return '—';
  if(x===0) return '0 '+unit;
  const a=Math.abs(x), n=sig||3;
  let p=SI_PRE[SI_PRE.length-1];
  for(const q of SI_PRE){ if(a>=q[0]){ p=q; break; } }
  let s=sigf(x/p[0],n);
  if(Math.abs(parseFloat(s))>=1000&&p[0]<1e9){ const q=SI_PRE[SI_PRE.indexOf(p)-1]; p=q; s=sigf(x/p[0],n); }
  return s.replace('-','−')+' '+p[1]+unit;
}
const SUP={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function pow10(e){ return '10'+String(e).split('').map(c=>SUP[c]).join(''); }
function fmtR(R){ return isFinite(R)?siFmt(R,'Ω'):'∞'; }
function fmtI(I){ return siFmt(I,'A'); }
function fmtV(V){ return siFmt(V,'V'); }
function fmtP(P){ return siFmt(P,'W'); }
/* a residual: its power of ten (a mantissa is noise at this level) */
function fmtRes(x){ if(!isFinite(x)) return '—'; if(x===0) return '0 (exact)';
  const e=Math.floor(Math.log10(x)); return (x/Math.pow(10,e)).toFixed(1)+'×'+pow10(e); }
/* PhET's value label for each part (Values checkbox) */
function valueText(e,SOL){
  const T=TYPES[e.type];
  if(isBattery(e.type)) return fmt(e.E,T.dp)+' V';
  if(e.type==='fuse') return fmt(fuseR(e.rating)*1000,1)+' mΩ ≤ '+fmt(e.rating,1)+' A';
  if(e.type==='rbulb') return fmt(SOL.R.get(e.id)||REAL_COLD,1)+' Ω';
  if(e.type==='wire'||e.type==='switch'||e.type==='ammeter') return '';
  if(T.dp!==undefined) return fmt(e.R,T.dp)+' Ω';
  return fmtR(e.R);
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function lawRows(SOL){
  const L=SOL.law, eps=Number.EPSILON;
  return rrow('current law, worst node',fmtRes(L.kcl),L.kcl<=8*eps?'good':'bad')
        +rrow('voltage law, worst loop',fmtRes(L.kvl),L.kvl<=8*eps?'good':'bad');
}
function census(SOL,C){
  const n=C.els.length;
  return rrow('parts',n?(n+' ('+countType(C,'wire')+' wire'+(countType(C,'wire')===1?'':'s')+')'):'none on the bench')
    +rrow('nodes, branches, pieces',SOL.nodes+', '+SOL.branches+', '+SOL.comps)
    +rrow('independent loops',SOL.loops);
}
function selRows(M){
  const e=M.sel, SOL=M.sol, C=M.st.circ;
  if(!e) return hd('selected part')+rrow('none','tap a part');
  const I=SOL.I.get(e.id), R=SOL.R.get(e.id), A=vById(C,e.a), B=vById(C,e.b);
  const same=SOL.comp.get(e.a)===SOL.comp.get(e.b);
  const u=same?SOL.V.get(e.a)-SOL.V.get(e.b):NaN;
  let s=hd('selected: '+elTag(C,e));
  if(isBattery(e.type)){ s+=rrow('EMF E, internal r',fmt(e.E,TYPES[e.type].dp)+' V, '+fmtR(M.st.rbat))
      +rrow('terminal voltage, + minus &minus;',same?fmtV(-u):'&mdash;')+rrow('current',fmtI(Math.abs(I)))
      +rrow('delivers E&middot;i',fmtP(e.E*I)); }
  else { const open=(e.type==='switch'&&!e.closed)||(e.type==='fuse'&&e.tripped);
    s+=rrow('resistance',open?(e.type==='switch'?'open':'blown'):fmtR(R))
      +rrow('voltage across',same?fmtV(Math.abs(u)):'&mdash;')+rrow('current',fmtI(Math.abs(I)))
      +rrow('power i&sup2;R',fmtP(I*I*(isFinite(R)?R:0)));
    if(isBulb(e.type)) s+=rrow('brightness (PhET&rsquo;s rule)',fmt(SOL.bright.get(e.id)||0,3),'good');
    if(e.type==='fuse') s+=rrow('rating',fmt(e.rating,1)+' A'+(e.tripped?' &mdash; blown':''),e.tripped?'bad':''); }
  if(SOL.fire.has(e.id)) s+=rrow('on fire','|I| &ge; 15 A','bad');
  return s;
}
function meterRows(M){
  const st=M.st; let s='';
  if(st.vm.on||st.am.on) s+=hd('meters');
  if(st.vm.on) s+=rrow('voltmeter, red &minus; black',voltageText(M.vm&&M.vm.V),M.vm&&M.vm.V!==null?'good':'');
  if(st.am.on) s+=rrow('non-contact ammeter',currentText(M.am?Math.abs(M.am.I):null,false),M.am?'good':'');
  const ams=st.circ.els.filter(e=>e.type==='ammeter');
  if(ams.length){ if(!(st.vm.on||st.am.on)) s+=hd('meters');
    ams.slice(0,3).forEach(e=>{ const r=seriesReading(st.circ,M.sol,e); s+=rrow(elTag(st.circ,e),currentText(r===null?null:Math.abs(r),true),r!==null?'good':''); }); }
  return s;
}
function readoutHTML(M){
  const st=M.st, SOL=M.sol, C=st.circ;
  let s='<div class="rname">circuit construction kit<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='lab'){
    s+=hd('the circuit')+census(SOL,C)+lawRows(SOL);
    s+=selRows(M)+meterRows(M);
    const notes=[];
    if(SOL.fire.size) notes.push('<b>Fire:</b> '+SOL.fire.size+' part'+(SOL.fire.size===1?'':'s')+' carrying 15 A or more.');
    const blown=C.els.filter(e=>e.type==='fuse'&&e.tripped).length;
    if(blown) notes.push('<b>'+blown+' blown fuse'+(blown===1?'':'s')+'</b>: select it and repair it.');
    if(st.showCurrent&&M.scale<1) notes.push(speedNote(M.scale));
    s+='</table>'+(notes.length?'<div class="note">'+notes.join(' ')+'</div>':'');
    s+='<div class="note">Solved by modified nodal analysis with every branch current an unknown; the laws are checked on the answer.</div>';
    return s;
  }
  if(M.view==='graph'){
    const n=SOL.nodes-SOL.comps;
    s+=hd('the graph')+rrow('nodes N',SOL.nodes)+rrow('branches B',SOL.branches)+rrow('connected pieces C',SOL.comps)
      +rrow('loops B &minus; N + C',SOL.loops,'good');
    s+=hd('the system')+rrow('node voltages (N &minus; C)',n)+rrow('branch currents (B)',SOL.branches)+rrow('unknowns',n+SOL.branches);
    s+=hd('on the answer')+lawRows(SOL)
      +rrow('largest node residual',fmtI(SOL.law.kclAbs))+rrow('largest loop residual',fmtV(SOL.law.kvlAbs));
    s+='</table><div class="note">Residuals are relative to the largest current and voltage in the piece they sit in; 8 &times; 2.2&times;10<sup>&minus;16</sup> is the pass mark.</div>';
    return s;
  }
  if(M.view==='power'){
    const B=M.bud;
    s+=hd('the ledger')+rrow('EMFs deliver &Sigma; E i',fmtP(B.gen),'good')+rrow('resistances take &Sigma; i&sup2;R',fmtP(B.dis),'good')
      +rrow('of which inside batteries',fmtP(B.sink.filter(x=>x.internal).reduce((a,x)=>a+x.P,0)))
      +rrow('Tellegen &Sigma; (v<sub>a</sub>&minus;v<sub>b</sub>) i',fmtRes(B.scale>0?Math.abs(B.tel)/B.scale:0)+' of the largest term',Math.abs(B.tel)<=64*Number.EPSILON*Math.max(B.scale,1e-300)*Math.max(1,SOL.branches)?'good':'bad');
    const bulbs=C.els.filter(e=>isBulb(e.type)&&SOL.onK.has(e.id));
    if(bulbs.length){ s+=hd('bulbs, PhET&rsquo;s brightness');
      bulbs.slice(0,4).forEach(e=>{ s+=rrow(elTag(C,e)+', '+fmtP(SOL.P.get(e.id)),fmt(SOL.bright.get(e.id),3)); }); }
    s+='</table><div class="note">Brightness b = ln(1 + 0.35 P)/ln(1 + 0.35&middot;2000), PhET&rsquo;s rule: full at 2 kW, 0.21 for 8.1 W.</div>';
    return s;
  }
  if(M.view==='thev'){
    const T=M.thev, e=M.focus!==null?elById(C,M.focus):null;
    if(!T){ s+=hd('the part')+rrow('none','the circuit has no part to look from')+'</table>'; return s; }
    s+=hd('seen from: '+elTag(C,e));
    if(T.open){ s+=rrow('the rest of the circuit','no path back')+rrow('current','0 A')+'</table><div class="note">This part is not in any loop: take it out and nothing else joins its two ends, so no current can flow through it.</div>'; return s; }
    s+=rrow('V<sub>th</sub>, part removed',fmtV(T.Voc))+rrow('R<sub>th</sub>, EMFs zeroed',fmtR(T.Rth))
      +rrow('short-circuit current V<sub>th</sub>/R<sub>th</sub>',fmtI(T.Voc/T.Rth));
    s+=hd('the operating point')+rrow('i = (V<sub>th</sub>+E)/(R<sub>th</sub>+R)',fmtI((T.Voc+T.E)/(T.Rth+T.R)),'good')+rrow('full solve',fmtI(T.i),'good');
    if(T.E===0) s+=rrow('P at R = R<sub>th</sub>',fmtP(T.Voc*T.Voc/(4*T.Rth)))+rrow('P now',fmtP(T.i*T.i*T.R));
    s+='</table><div class="note">'+(M.sol.realR.size?'Real bulbs are frozen at their present resistance: this is the tangent at the operating point. ':'')
      +'Choose the part in the lab (tap it), or step through the parts with the buttons.</div>';
    return s;
  }
  /* superposition */
  const Sp=M.sup;
  s+=hd('batteries')+rrow('in the circuit',Sp.bats.length);
  let worst=0; SOL.net.br.forEach((e,k)=>{ let t=0; for(const p of Sp.parts) t+=p[k]; worst=Math.max(worst,Math.abs(t-SOL.sol.i[k])); });
  const Isc=Math.max(SOL.Imax,1e-300);
  s+=rrow('&Sigma; of the parts &minus; full solve',fmtRes(Sp.bats.length?worst/Isc:0)+' of the largest current',worst<=64*Number.EPSILON*Isc?'good':'bad');
  Sp.bats.slice(0,4).forEach((kb,j)=>{ const e=SOL.net.br[kb].el; s+=rrow(elTag(C,e)+' alone drives',fmtI(Math.abs(Sp.parts[j][kb]))+' through itself'); });
  s+='</table><div class="note">Each battery alone: every other EMF set to zero, every internal resistance kept. Linear parts only'+(SOL.realR.size?' (real bulbs frozen at their present resistance)':'')+'.</div>';
  return s;
}
function eqbarHTML(M){
  if(M.view==='lab') return '<span class="lhs">&Sigma;&thinsp;i = 0</span> at every node &nbsp;&middot;&nbsp; <span class="lhs">&Sigma;&thinsp;&Delta;v = 0</span> round every loop &nbsp;&middot;&nbsp; <span class="hl">v<sub>a</sub> &minus; v<sub>b</sub> = R i &minus; E</span>'
    +'<span class="sm">Kirchhoff&rsquo;s two laws and each part&rsquo;s own law, solved together for the whole circuit; a battery is an EMF E behind an internal resistance r</span>';
  if(M.view==='graph') return '<span class="lhs">A i = 0</span>, &nbsp; <span class="lhs">A<sup>T</sup>v &minus; R i = &minus;E</span> &nbsp;&middot;&nbsp; <span class="hl">(N &minus; C) + B unknowns</span>'
    +'<span class="sm">A is the incidence matrix (a node&rsquo;s row: +1 where a branch leaves it, &minus;1 where one arrives); the first block is the current law, the second every branch&rsquo;s own law</span>';
  if(M.view==='power') return '<span class="lhs">&Sigma; E i</span> = <span class="hl">&Sigma; i&sup2; R</span> &nbsp;&middot;&nbsp; <span class="lhs">&Sigma; (v<sub>a</sub> &minus; v<sub>b</sub>) i = 0</span>'
    +'<span class="sm">Tellegen&rsquo;s theorem: any currents that obey the current law, times any voltages that come from potentials, sum to zero &mdash; so what the EMFs deliver is exactly what the resistances dissipate</span>';
  if(M.view==='thev') return '<span class="lhs">i</span> = <span class="hl">(V<sub>th</sub> + E) / (R<sub>th</sub> + R)</span> &nbsp;&middot;&nbsp; <span class="lhs">P = V<sub>th</sub>&sup2;R/(R<sub>th</sub> + R)&sup2;</span>, largest at <span class="hl2">R = R<sub>th</sub></span>'
    +'<span class="sm">Th&eacute;venin: seen from any two terminals, the rest of a linear circuit is one EMF behind one resistance</span>';
  return '<span class="lhs">i<sub>k</sub></span> = <span class="hl">&Sigma;<sub>j</sub> i<sub>k</sub><sup>(j)</sup></span>'
    +'<span class="sm">superposition: each branch current is the sum of the currents each battery would drive alone, the other EMFs set to zero and their internal resistances kept</span>';
}
function tagHTML(M){
  if(M.view==='lab') return '<b>the lab</b> &nbsp; drag parts out of the toolbox, drop an end on an end to join them';
  if(M.view==='graph') return '<b>nodes and branches</b> &nbsp; the circuit as a graph, and the matrix that solves it';
  if(M.view==='power') return '<b>the power budget</b> &nbsp; where each watt comes from and where it goes';
  if(M.view==='thev') return '<b>the rest of the circuit</b> &nbsp; one part&rsquo;s view of everything else';
  return '<b>one battery at a time</b> &nbsp; superposition';
}
