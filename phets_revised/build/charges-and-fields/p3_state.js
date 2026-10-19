
/* ================================================================== *
 *  state, presets, the per-view model, readout, eqbar, tag            *
 * ================================================================== */
const TABS=[['plane','the plane'],['lines','field lines'],['land','the landscape'],['super','superposition'],['far','the far field']];
const COL={pos:'#b8ec4c', neg:'#cd35c4', ref:'#e8843a', struct:'#5ac8e0', live:'#f2f4f8', dim:'#8b93a6',
           edge:'#242a3a', plane:'#0b1020', bin:'#10131b', binEdge:'#3a4152', arrow:'#e9ecf2',
           grid:'#141b2a', gridMaj:'#1f2940', zero:'#1a2233'};
const RO_W=300;
const S3=Math.sqrt(3);
function qCol(q){ return q>0?COL.pos:COL.neg; }
/* the presets (PhET opens on an empty plane; the default here is the dipole
   so the first view has something to show — "empty" gives PhET's start) */
const PRESETS=[
  {id:'empty',name:'empty',ch:[]},
  {id:'single',name:'one charge',ch:[{x:0,y:0,q:1}]},
  {id:'dipole',name:'dipole',ch:[{x:-0.5,y:0,q:-1},{x:0.5,y:0,q:1}]},
  {id:'like',name:'like pair',ch:[{x:-0.5,y:0,q:1},{x:0.5,y:0,q:1}]},
  {id:'quad',name:'quadrupole',ch:[{x:0.5,y:0.5,q:1},{x:-0.5,y:0.5,q:-1},{x:-0.5,y:-0.5,q:1},{x:0.5,y:-0.5,q:-1}]},
  {id:'triangle',name:'triangle',ch:[{x:0,y:0.75,q:1},{x:-0.75*S3/2,y:-0.375,q:1},{x:0.75*S3/2,y:-0.375,q:1}]},
  {id:'rows',name:'two rows',ch:[-1.5,-1,-0.5,0,0.5,1,1.5].map(x=>({x,y:1,q:1})).concat([-1.5,-1,-0.5,0,0.5,1,1.5].map(x=>({x,y:-1,q:-1})))},
];
function presetCharges(id){ const p=PRESETS.find(o=>o.id===id); return p?p.ch.map(c=>({x:c.x,y:c.y,q:c.q})):[]; }
function clone(o){ return JSON.parse(JSON.stringify(o)); }
const DEFAULTS={view:'plane', preset:'dipole', charges:presetCharges('dipole'),
  /* PhET's check boxes and their defaults: field on, the rest off */
  showE:true, dirOnly:false, showV:false, showVals:false, showGrid:false,
  /* the tools: the voltage sensor out with one equipotential plotted, one
     E-field sensor on the plane, the tape in its box */
  showVS:true, showTape:false, vs:{x:1.5,y:0.9}, esens:[{x:-1.8,y:1.2}], tape:{ax:-2.8,ay:1.9,bx:-0.8,by:1.9},
  eqSeeds:[{x:1.5,y:0.9}],
  nLines:16, famDV:4, showFam:true, showNulls:true,
  /* the landscape's clip: 20 V, half of PhET's colour saturation, so a dipole's
     relief shows at the first look (at 40 V it was two thin spikes) */
  vcap:20, camTheta:-1.05, camPhi:0.62, camZoom:1, landEq:true,
  probe:{x:0.6,y:0.9}, farTheta:30};
const ST=clone(DEFAULTS);
function resetState(over){ Object.assign(ST,clone(DEFAULTS),over?clone(over):{}); for(const k in MEMO) delete MEMO[k]; }
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---- edits to the charges (every one clears the plotted equipotentials,
   as PhET's do: a line belongs to the charges it was traced in) ---- */
function applyPreset(st,id){ st.preset=id; st.charges=presetCharges(id); st.eqSeeds=[]; }
function addCharge(st,x,y,q){ if(st.charges.length>=MAX_CHARGES) return -1; st.charges.push({x,y,q}); st.preset='custom'; st.eqSeeds=[]; return st.charges.length-1; }
function moveCharge(st,k,x,y){ const c=st.charges[k]; if(!c) return false; c.x=clamp(x,PLANE.x0,PLANE.x1); c.y=clamp(y,PLANE.y0,PLANE.y1); st.preset='custom'; st.eqSeeds=[]; return true; }
function removeCharge(st,k){ if(k<0||k>=st.charges.length) return false; st.charges.splice(k,1); st.preset='custom'; st.eqSeeds=[]; return true; }
function inBin(x,y){ return x>=BIN.x0&&x<=BIN.x1&&y>=BIN.y0&&y<=BIN.y1; }
/* the voltage sensor's "plot" button: refused on an empty plane, within 3 cm
   of a charge and at a null (the tracer says why) */
function plotEquipotential(st){
  if(!st.showVS) return {ok:false,why:'the voltage sensor is in its box'};
  const t=traceEquipotential(st.charges,st.vs.x,st.vs.y);
  if(!t.ok) return t;
  if(st.eqSeeds.length>=MAX_EQ) st.eqSeeds.shift();
  st.eqSeeds.push({x:st.vs.x,y:st.vs.y});
  return t;
}

function buildModel(){
  const st=ST, ch=st.charges, key=chargeKey(ch), view=st.view;
  let npos=0, nneg=0; for(const c of ch){ if(c.q>0) npos++; else nneg++; }
  const M={view,st,ch,key,Q:netCharge(ch),n:ch.length,npos,nneg};
  M.vsR=st.showVS?sensorReading(ch,st.vs.x,st.vs.y):null;
  M.esR=st.esens.map(s=>sensorReading(ch,s.x,s.y));
  M.tape=st.showTape?tapeModel(ch,st.tape):null;
  M.eq=memo('eq',key+'|'+JSON.stringify(st.eqSeeds),()=>st.eqSeeds.map(s=>traceEquipotential(ch,s.x,s.y)));
  if(view==='plane'){
    M.vmap=st.showV?memo('vmap',key,()=>vmapGrid(ch)):null;
    M.arrows=st.showE?memo('arrows',key,()=>arrowGrid(ch)):null;
  }
  if(view==='lines'){
    M.FL=memo('fl',key+'|'+st.nLines,()=>fieldLines(ch,st.nLines));
    M.fam=st.showFam?memo('fam',key+'|'+st.famDV,()=>equipotentialFamily(ch,st.famDV)):null;
    M.nulls=memo('nulls',key,()=>findNulls(ch));
  }
  if(view==='land') M.land=memo('land',key+'|'+st.vcap,()=>landGrid(ch,st.vcap));
  if(view==='super'){ M.contrib=contributions(ch,st.probe.x,st.probe.y); M.probe=sensorReading(ch,st.probe.x,st.probe.y); }
  if(view==='far') M.far=memo('far',key+'|'+st.farTheta,()=>farField(ch,st.farTheta));
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function fV(v){ return isFinite(v)?sigf(v,3)+' V':'&mdash; (on a charge)'; }
function fE(m){ return isFinite(m)?sigf(m,3)+' V/m':'&mdash;'; }
function fQ(q){ return (q>0?'+':q<0?'&minus;':'')+fmt(Math.abs(q),0)+' nC'; }
function fXY(x,y){ return '('+fmt(x,2)+', '+fmt(y,2)+') m'; }
function sensorText(R){ return R.over?'&mdash; (on a charge)':R.mag>0?fE(R.mag)+' at '+fmt(R.ang,1)+'&deg;':'0 V/m, no direction'; }
function chargesRows(M){
  return hd('the charges')+rrow('on the plane',M.n+(M.n?' ('+M.npos+' positive, '+M.nneg+' negative)':''))
    +rrow('net charge Q',fQ(M.Q),M.Q===0&&M.n?'good':'');
}
function readoutHTML(M){
  const st=ST;
  let s='<div class="rname">charges and fields<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  s+=chargesRows(M);
  if(M.view==='plane'){
    s+=hd('the voltage sensor');
    s+=M.vsR?rrow('at '+fXY(st.vs.x,st.vs.y),fV(M.vsR.V),'good'):rrow('in its box','&mdash;');
    s+=hd('E-field sensors');
    if(!M.esR.length) s+=rrow('none on the plane','drag one from the bin');
    M.esR.slice(0,4).forEach((R,i)=>{ s+=rrow('#'+(i+1)+' '+fXY(st.esens[i].x,st.esens[i].y),sensorText(R)); });
    if(M.esR.length>4) s+=rrow('and '+(M.esR.length-4)+' more','');
    if(M.tape) s+=hd('the tape')+rrow('length',fmt(M.tape.cm,1)+' cm')+rrow('V(A) &minus; V(B)',fV(M.tape.dV));
    s+=hd('equipotentials');
    s+=M.eq.length?rrow(M.eq.length+' plotted',M.eq.slice(-4).map(e=>e.ok?sigf(e.V0c,3)+' V':'&mdash;').join(', ')):rrow('none plotted','press plot on the sensor');
  }
  else if(M.view==='lines'){
    const F=M.FL;
    s+=hd('field lines');
    if(!M.n) s+=rrow('no charges','nothing to trace');
    else { s+=rrow('traced from the',F.sgn>0?'positive charges':'negative charges')+rrow('lines',F.lines.length)
        +rrow('end on a charge',F.ends,'good')+rrow('run off past 10 km',F.escapes)+rrow('end at a null',F.nulls,F.nulls?'bad':''); }
    s+=hd('null points, E = 0');
    if(!M.nulls.length) s+=rrow('none on the plane','&mdash;');
    M.nulls.slice(0,5).forEach(N=>{ s+=rrow(fXY(N.x,N.y),(N.kind==='saddle'?'saddle':N.kind==='min'?'in-plane minimum':'in-plane maximum')+', '+fV(N.V)); });
    if(M.nulls.length>5) s+=rrow('and '+(M.nulls.length-5)+' more','');
    if(st.showFam) s+=hd('equipotentials')+rrow('every',fmt(st.famDV,0)+' V to &plusmn;'+V_SAT+' V');
  }
  else if(M.view==='land'){
    const Ld=M.land;
    s+=hd('the surface')+rrow('height',fmt(LAND_HZ,2)+' m = '+fmt(st.vcap,0)+' V')+rrow('clipped at','&plusmn;'+fmt(st.vcap,0)+' V')
      +rrow('vertices clipped',Ld.clipped+' of '+((Ld.nx+1)*(Ld.ny+1)),Ld.clipped?'bad':'');
    s+=hd('camera')+rrow('azimuth, elevation',fmt(st.camTheta/DEG,0)+'&deg;, '+fmt(st.camPhi/DEG,0)+'&deg;')+rrow('zoom',fmt(st.camZoom,2)+'&times;');
    if(M.eq.length) s+=hd('level cuts')+rrow(M.eq.length+' plotted equipotentials',M.eq.slice(-4).map(e=>e.ok?sigf(e.V0c,3)+' V':'&mdash;').join(', '));
  }
  else if(M.view==='super'){
    const P=M.probe, C=M.contrib;
    let sv=0, sx=0, sy=0; for(const c of C){ sv+=c.V; sx+=c.ex; sy+=c.ey; }
    s+=hd('the probe at '+fXY(st.probe.x,st.probe.y))+rrow('V = &Sigma; V<sub>i</sub>',fV(P.V),'good')+rrow('|E|, direction',sensorText(P),'good');
    if(C.length){ s+=rrow('|&Sigma;E<sub>i</sub> &minus; E|',sigf(Math.hypot(sx-P.ex,sy-P.ey),2)+' V/m');
      s+=hd('each charge (first '+Math.min(C.length,6)+')');
      C.slice(0,6).forEach(c=>{ s+=rrow('#'+(c.i+1)+' '+fQ(c.q)+', r = '+fmt(c.r,2)+' m',(isFinite(c.V)?sigf(c.V,3):'&mdash;')+' V, '+fE(Math.hypot(c.ex,c.ey))); }); }
  }
  else {
    const F=M.far, Mo=F.M;
    s+=hd('the moments about '+fXY(Mo.c[0],Mo.c[1]))+rrow('Q',fQ(Mo.Q))+rrow('p = &Sigma; q d',sigf(Math.hypot(Mo.p[0],Mo.p[1]),3)+' nC&middot;m')
      +rrow('Q<sub>xx</sub>, Q<sub>xy</sub>, Q<sub>yy</sub>',sigf(Mo.Qxx,3)+', '+sigf(Mo.Qxy,3)+', '+sigf(Mo.Qyy,3)+' nC&middot;m&sup2;')
      +rrow('farthest charge, d<sub>max</sub>',fmt(Mo.dmax,3)+' m');
    s+=hd('along the ray at '+fmt(F.th,0)+'&deg;');
    for(let l=0;l<4;l++) s+=rrow('c<sub>'+l+'</sub> ('+ORDER_NAME[l]+')',M.n?sigf(F.cs[l],4)+' V&middot;m'+(l?'<sup>'+(l+1)+'</sup>':''):'&mdash;',F.l0===l?'good':'');
    if(F.l0!==null) s+=rrow('leading order',ORDER_NAME[F.l0]+', V &prop; 1/r'+(F.l0?'<sup>'+(F.l0+1)+'</sup>':''))
      +rrow('lim r<sup>'+(F.l0+1)+'</sup>V, numerically',sigf(F.lim,6),'good')+rrow('c<sub>'+F.l0+'</sub>, exact',sigf(F.cs[F.l0],6));
    else s+=rrow('leading order',M.n?'none: V = 0 along this ray':'no charges','bad');
  }
  s+='</table><div class="note">k = 1/4&pi;&epsilon;<sub>0</sub> = '+sigf(KNC,6)+' V&middot;m/nC from the CODATA 2022 &epsilon;<sub>0</sub>; PhET uses 9, so its readings run 0.14 % higher. Everything else is exact superposition, pinned in selfTest to build/charges-and-fields/derive.py.</div>';
  return s;
}

function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='plane') return E('<span class="hl">V(r) = k &Sigma; q<sub>i</sub> / |r &minus; r<sub>i</sub>|</span> &nbsp;&middot;&nbsp; <span class="hl">E = &minus;&nabla;V = k &Sigma; q<sub>i</sub> (r &minus; r<sub>i</sub>) / |r &minus; r<sub>i</sub>|&sup3;</span> &nbsp;&middot;&nbsp; k = 1/4&pi;&epsilon;<sub>0</sub> = 8.988 V&middot;m/nC',
    'each charge adds a 1/r potential and a 1/r&sup2; field; the voltage map, the arrows and every sensor are these two sums, evaluated exactly');
  if(M.view==='lines') return E('<span class="hl">dr/ds = E/|E|</span> <span class="rm">(a field line)</span> &nbsp;&middot;&nbsp; V(r) = V<sub>0</sub> <span class="rm">(an equipotential)</span> &nbsp;&rArr;&nbsp; <span class="hl2">t&#770;<sub>V</sub> &middot; E = 0</span>',
    'lines follow E and cross every equipotential at a right angle; equally spaced equipotentials crowd where the field is strong');
  if(M.view==='land') return E('<span class="hl">E = &minus;&nabla;V</span> &nbsp;&middot;&nbsp; |E| = <span class="rm">the steepest slope of</span> V(x, y) &nbsp;&middot;&nbsp; V = V<sub>0</sub> <span class="rm">is a level cut</span>',
    'the field points straight downhill on the potential landscape, and is as strong as the slope is steep');
  if(M.view==='super') return E('<span class="hl">E(P) = &Sigma;<sub>i</sub> E<sub>i</sub>(P)</span> &nbsp;&middot;&nbsp; <span class="hl2">V(P) = &Sigma;<sub>i</sub> V<sub>i</sub>(P)</span> &nbsp;&middot;&nbsp; E<sub>i</sub> = k q<sub>i</sub> (P &minus; r<sub>i</sub>)/|P &minus; r<sub>i</sub>|&sup3;',
    'fields add as vectors, head to tail; potentials add as signed numbers');
  return E('<span class="hl">V(c + r n&#770;) = &Sigma;<sub>&ell;</sub> c<sub>&ell;</sub> / r<sup>&ell;+1</sup></span>, &nbsp; c<sub>&ell;</sub> = k &Sigma; q<sub>i</sub> d<sub>i</sub><sup>&ell;</sup> P<sub>&ell;</sub>(cos &gamma;<sub>i</sub>) &nbsp;&middot;&nbsp; c<sub>0</sub> = kQ, &nbsp;c<sub>1</sub> = k p&middot;n&#770;, &nbsp;c<sub>2</sub> = &frac12;k n&#770;&middot;Q&middot;n&#770;',
    'far away only the lowest non-vanishing moment survives: a net charge falls as 1/r, a neutral pair as 1/r&sup2;, a square of four as 1/r&sup3;');
}
function tagHTML(M){
  const st=ST, pn=(PRESETS.find(p=>p.id===st.preset)||{name:'your charges'}).name;
  if(M.view==='plane') return '<b>the plane</b> — '+pn+(M.n?', '+M.n+' charge'+(M.n>1?'s':''):'');
  if(M.view==='lines') return '<b>field lines</b> — '+pn+', '+st.nLines+' per charge';
  if(M.view==='land') return '<b>the landscape</b> — '+pn+', clipped at &plusmn;'+fmt(st.vcap,0)+' V';
  if(M.view==='super') return '<b>superposition</b> — '+pn+', the probe at '+fXY(st.probe.x,st.probe.y);
  return '<b>the far field</b> — '+pn+', the ray at '+fmt(st.farTheta,0)+'&deg;';
}
