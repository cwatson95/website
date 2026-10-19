
/* ================================================================== *
 *  state, the per-view model, readout, equation bar, tag              *
 * ================================================================== */
const TABS=[['bar','the bar magnet'],['em','the electromagnet'],['lines','field lines'],['axis','on the axis'],['far','the far field'],['needle','the needle']];
const COL={north:'#b8ec4c', south:'#cd35c4', needleS:'#7d8596', ref:'#e8843a', struct:'#5ac8e0', live:'#f2f4f8', dim:'#8b93a6',
           copper:'#c9905c', electron:'#8fd3ff', bound:'#5ac8e0', edge:'#242a3a', grid:'#141b2a'};
const RO_W=300;
function clone(o){ return JSON.parse(JSON.stringify(o)); }
const DEFAULTS={view:'bar', units:'G', flowConv:'electron', run:true,
  /* the bar magnet screen, PhET's defaults: 75 %, the field shown, the compass out, the meter away */
  bar:{x:430,y:333,ang:0}, pct:75, barField:true, seeInside:false, earth:false, barCompass:true, barMeter:false,
  barC:{x:625,y:218}, barM:{x:125,y:218},
  /* the electromagnet screen, PhET's defaults: 4 loops on the battery at +10 V (AC: 50 %, 50 %) */
  em:{x:400,y:218}, loops:4, supply:'dc', dcV:10, acPk:50, acFp:50, emField:true, electrons:true, emCompass:true, emMeter:false,
  emC:{x:625,y:218}, emM:{x:125,y:218},
  /* the analysis views */
  src:'magnet', bound:true, axisH:true, ndB:5, ndRel:60, ndDamp:2};
const ST=clone(DEFAULTS);
const LIVE={t:0, emT:0, ePhase:0, ndT:0, barRot:null, emRot:null};
function resetLive(){ LIVE.t=0; LIVE.emT=0; LIVE.ePhase=0; LIVE.ndT=0; LIVE.barRot=null; LIVE.emRot=null; }
function resetState(over){ Object.assign(ST,clone(DEFAULTS),over?clone(over):{}); resetLive(); }

/* the sources the screens hold */
function barMagnet(st){ return {kind:'magnet',x:st.bar.x,y:st.bar.y,ang:st.bar.ang,S:S_MAX*st.pct/100}; }
function emSupply(st){ return st.supply==='dc'?{kind:'dc',V:st.dcV}:{kind:'ac',pk:st.acPk,fp:st.acFp}; }
function emCoil(st,t){ return {kind:'coil',x:st.em.x,y:st.em.y,N:st.loops,I:supplyCurrent(emSupply(st),t)}; }
function emSupplyPos(st){ return {x:st.em.x,y:st.em.y-130}; }
/* the compass rotors: aligned with the field when first needed (PhET initialises the needle so) */
function rotorFor(key,src,p){
  if(!LIVE[key]){ const B=sourceField(src,p.x,p.y,0); LIVE[key]={phi:Math.atan2(B[1],B[0]),om:0,W:0,rest:true}; }
  return LIVE[key];
}
/* advance the live clocks; returns true if anything moved (the frame loop repaints on it) */
function stepLive(dt){
  const st=ST; let moved=false;
  dt=Math.min(dt,0.05);
  if(st.view==='bar'&&st.barCompass){
    const src=barMagnet(st), r=rotorFor('barRot',src,st.barC), B=sourceField(src,st.barC.x,st.barC.y,0);
    moved=rotorTick(r,()=>B,dt)||moved;
  }
  if(st.view==='em'){
    const sup=emSupply(st), I0=supplyCurrent(sup,LIVE.emT);
    if(sup.kind==='ac'&&sup.pk>0){ LIVE.emT+=dt; moved=true; }
    const I1=supplyCurrent(sup,LIVE.emT);
    if(st.electrons&&I1!==0){ LIVE.ePhase+=electronSpeed(I1)*dt*(st.flowConv==='electron'?1:-1);   /* I > 0 runs DOWN the front halves, so electrons climb them */ moved=true; }
    if(st.emCompass){
      const t0=LIVE.emT-(sup.kind==='ac'&&sup.pk>0?dt:0), r=rotorFor('emRot',emCoil(st,t0),st.emC);
      moved=rotorTick(r,t=>sourceField(emCoil(st,t0+t),st.emC.x,st.emC.y,0),dt)||moved;
    }
    if(I0!==I1) moved=true;
  }
  if(st.view==='needle'){ LIVE.ndT+=dt; if(LIVE.ndT>needleWindow(st)) LIVE.ndT=0; moved=true; }
  return moved;
}
/* one frame of a rotor; at rest (within 1e-4 rad and 1e-3 rad/s of a steady field) it stops,
   so a settled page draws nothing */
function rotorTick(r,Bfun,dt){
  const B=Bfun(0), th=Math.atan2(B[1],B[0]), mg=Math.hypot(B[0],B[1]);
  if(!(mg>0)) return false;
  const off=wrapPi(r.phi-th);
  const steady=(()=>{ const B2=Bfun(dt); return B2[0]===B[0]&&B2[1]===B[1]; })();
  if(r.rest&&Math.abs(off)<1e-4&&steady) return false;
  r.rest=false;
  rotorAdvance(r,Bfun,0,dt);
  if(steady&&Math.abs(wrapPi(r.phi-th))<1e-4&&Math.abs(r.om)<1e-3){ r.phi=th; r.om=0; r.rest=true; }
  return true;
}
/* electrons: one lap of a loop per second at full current (a picture of the current's size and
   sense only: the real drift in a wire is a fraction of a millimetre per second) */
function electronSpeed(I){ return I/I_MAX; }
function needleWindow(st){ const w0=Math.sqrt(KAPPA*st.ndB); return Math.max(4,Math.min(24,7*2*Math.PI/w0)); }

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* the field-lines / axis / far views look at one source: the bar magnet at its strength, or
   the electromagnet at its present current */
function analysisSource(st){
  if(st.src==='magnet') return {kind:'magnet',N:0,unit:S_MAX*st.pct/100,label:'the bar magnet'};
  const I=supplyCurrent(emSupply(st),LIVE.emT);
  return {kind:'coil',N:st.loops,unit:coilGaussPerUnit(I),I,label:'the electromagnet'};
}

function buildModel(){
  const st=ST, v=st.view, M={view:v,st};
  if(v==='bar'){
    M.src=barMagnet(st);
    M.rot=st.barCompass?rotorFor('barRot',M.src,st.barC):null;
    M.meter=st.barMeter?meterReading(M.src,st.barM.x,st.barM.y):null;
    M.atCompass=meterReading(M.src,st.barC.x,st.barC.y);
  } else if(v==='em'){
    M.sup=emSupply(st); M.V=supplyVoltage(M.sup,LIVE.emT); M.src=emCoil(st,LIVE.emT);
    M.rot=st.emCompass?rotorFor('emRot',M.src,st.emC):null;
    M.meter=st.emMeter?meterReading(M.src,st.emM.x,st.emM.y):null;
    M.inWire=st.emMeter&&inWire(M.src,st.emM.x,st.emM.y);
    M.atCompass=meterReading(M.src,st.emC.x,st.emC.y);
    M.Bc=coilField(M.src,st.em.x,st.em.y,0)[0];
  } else if(v==='lines'||v==='axis'||v==='far'){
    M.as=analysisSource(st);
    if(v==='lines') M.fl=fieldLinesFor(M.as.kind,M.as.N);
    if(v==='far') M.far=memo('far',M.as.kind+M.as.N,()=>({ax:dipoleLimit(M.as.kind,M.as.N,'axis'),eq:dipoleLimit(M.as.kind,M.as.N,'bis'),
      oa:octMeasured(M.as.kind,M.as.N,'axis'),oe:octMeasured(M.as.kind,M.as.N,'bis')}));
  } else if(v==='needle'){
    M.nd=memo('needle',[st.ndB,st.ndRel,st.ndDamp].join('|'),()=>needleRun(st.ndB,st.ndRel*D2R,st.ndDamp,needleWindow(st)));
  }
  return M;
}

/* the needle view's run: the rotor released at rel from a steady field along +x */
function needleRun(Bmag,rel,gam,Tw){
  const r={phi:rel,om:0,W:0}, Bv=[Bmag,0], n=600, dt=Tw/n, ts=[0], ph=[rel], E0=rotorEnergy(r,Bv);
  let maxLedger=0;
  for(let i=1;i<=n;i++){ rotorAdvance(r,()=>Bv,0,dt,KAPPA,gam); ts.push(i*dt); ph.push(r.phi);
    maxLedger=Math.max(maxLedger,Math.abs(rotorEnergy(r,Bv)+r.W-E0)); }
  const w0=Math.sqrt(KAPPA*Bmag), disc=w0*w0-gam*gam/4;
  const lin=ts.map(t=>linearNeedle(rel,w0,gam,t));
  /* measured period: successive downward zero crossings of phi */
  const zc=[]; for(let i=1;i<ph.length;i++) if(ph[i-1]>0&&ph[i]<=0) zc.push(ts[i-1]+(ts[i]-ts[i-1])*ph[i-1]/(ph[i-1]-ph[i]));
  return {Bmag,rel,gam,Tw,ts,ph,lin,w0,T0:2*Math.PI/w0,zeta:gam/(2*w0),under:disc>0,wd:disc>0?Math.sqrt(disc):NaN,
          Tbig:4*ellK(Math.cos(rel/2))/w0, Tmeas:zc.length>=2?zc[1]-zc[0]:NaN, ledger:maxLedger/E0, E0};
}
/* the small-angle solution of theta'' + gamma theta' + omega0^2 theta = 0, theta(0) = th0, theta'(0) = 0 */
function linearNeedle(th0,w0,gam,t){
  const d=w0*w0-gam*gam/4, e=Math.exp(-gam*t/2);
  if(d>0){ const wd=Math.sqrt(d); return th0*e*(Math.cos(wd*t)+gam/(2*wd)*Math.sin(wd*t)); }
  if(d<0){ const q=Math.sqrt(-d); return th0*e*(Math.cosh(q*t)+gam/(2*q)*Math.sinh(q*t)); }
  return th0*e*(1+gam*t/2);
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function fB(v){ return fmtField(v,ST.units); }
function fI(I){ return (I<0?'&minus;':'')+sigf(Math.abs(I),4)+' A'; }
function fPos(x,y){ return '('+fmt(x,0)+', '+fmt(y,0)+') mm'; }
function magMoment(S){ return S/G_PER_T/MU0*Math.PI*Math.pow(MAG_R*1e-3,2)*MAG_L*1e-3; }   /* A m^2 = M V */
function meterRows(rd,title,inw){
  if(!rd) return '';
  if(inw) return hd(title)+rrow('inside the wire','the filament field is not the wire&rsquo;s');
  return hd(title)+rrow('B',fB(rd.B),'good')+rrow('B<sub>x</sub>',fB(rd.Bx))+rrow('B<sub>y</sub>',fB(rd.By))+rrow('&theta;',fmtAngle(rd.ang));
}
function compassRows(r,atC){
  if(!r) return '';
  const lag=wrapPi(r.phi-Math.atan2(atC.By,atC.Bx))*R2D, T=2*Math.PI/Math.sqrt(KAPPA*atC.B);
  return hd('the compass')+rrow('|B| there',fB(atC.B))+rrow('needle off the field',fmt(lag,1)+'&deg;',Math.abs(lag)<0.5?'good':'')
    +rrow('its small-swing period',isFinite(T)?sigf(T,3)+' s':'&mdash;');
}
function readoutHTML(M){
  const st=ST, name=TABS.find(t=>t[0]===M.view)[1];
  let s='<div class="rname">magnets &amp; electromagnets<small>'+name+'</small></div><table>';
  if(M.view==='bar'){
    const S=M.src.S;
    s+=hd('the bar magnet')+rrow('strength &mu;<sub>0</sub>M',fB(S)+' ('+st.pct+' %)')+rrow('field at its centre',fB(S*solAxis(0,MAG_R,MAG_B)))
      +rrow('moment m = MV',sigf(magMoment(S),3)+' A&middot;m&sup2;')+rrow('north end points',fmt(((st.bar.ang*R2D)%360+360)%360,0)+'&deg;')
      +rrow('centre',fPos(st.bar.x,st.bar.y));
    s+=compassRows(M.rot,M.atCompass)+meterRows(M.meter,'the field meter');
  } else if(M.view==='em'){
    s+=hd('the coil')+rrow('centre',fPos(st.em.x,st.em.y))+rrow('loops',st.loops)+rrow(M.sup.kind==='dc'?'battery':'AC supply, now',(M.V<0?'&minus;':'')+fmt(Math.abs(M.V),2)+' V')
      +rrow('current I',fI(M.src.I))+rrow('field at its centre',fB(M.Bc),'good')+rrow('moment N I &pi;a&sup2;',sigf(Math.abs(M.src.I)*st.loops*Math.PI*Math.pow(COIL_A*1e-3,2),3)+' A&middot;m&sup2;');
    if(M.sup.kind==='ac') s+=rrow('peak, frequency',fmt(AC_VMAX*st.acPk/100,1)+' V, '+sigf(acFreq(M.sup),3)+' Hz');
    s+=compassRows(M.rot,M.atCompass)+meterRows(M.meter,'the field meter',M.inWire);
  } else if(M.view==='lines'){
    const F=M.fl, u=M.as.unit, okN=F.lines.filter(l=>l.ok).length;
    let wc=0; for(const l of F.lines) if(l.ok) wc=Math.max(wc,l.close);
    s+=hd(M.as.label)+rrow('lines each side',F.lines.length)+rrow('closed on themselves',okN+' of '+F.lines.length,okN===F.lines.length?'good':'bad')
      +rrow('worst closure',sigf(wc,2)+' mm')+rrow('flux through the middle',u?sigf(2*Math.PI*F.psiMax*Math.abs(u)*1e-10,3)+' Wb':'&mdash; (no field)')
      +rrow('between neighbours',u?sigf(2*Math.PI*F.psiMax*Math.abs(u)*1e-10/(F.lines.length+1),3)+' Wb':'&mdash;');
    s+=hd('where they cross the mid-plane outside')+F.lines.slice(-4).reverse().map((l,i)=>rrow('line '+(F.lines.length-i),fmt(l.rOut,1)+' mm')).join('');
  } else if(M.view==='axis'){
    const A=M.as;
    if(A.kind==='magnet'){ const S=A.unit;
      s+=hd('the bar magnet on its axis')+rrow('B at the centre',fB(S*solAxis(0,MAG_R,MAG_B)),'good')+rrow('B at a pole face',fB(S*solAxis(MAG_B,MAG_R,MAG_B)))
        +rrow('&mu;<sub>0</sub>H at the centre',fB(S*(solAxis(0,MAG_R,MAG_B)-1)))+rrow('jump of &mu;<sub>0</sub>H at a face',fB(S));
    } else { const u=A.unit;
      s+=hd('the coil on its axis')+rrow('loops, current',st.loops+', '+fI(A.I))+rrow('B at the centre',fB(u*coilRU(st.loops,0,0)[1]),'good')
        +rrow('continuous sheet, same N I',fB(u*solAxis(0,COIL_A,st.loops*COIL_PITCH/2)/COIL_PITCH));
    }
  } else if(M.view==='far'){
    const F=M.far, A=M.as, dip=A.kind==='magnet'?MAG_DIP:coilDip(A.N);
    s+=hd(A.label)+rrow('&mu;<sub>0</sub>m/4&pi;',A.unit?sigf(Math.abs(A.unit)*dip,4)+' G&middot;mm&sup3;':'&mdash; (no field)');
    s+=hd('r&sup3;B / dipole, as r &rarr; &infin;')+rrow('along the axis',fmt(F.ax.lim,10),'good')+rrow('on the bisector',fmt(F.eq.lim,10),'good');
    s+=hd('the approach, (ratio &minus; 1) r&sup2;')+rrow('axis, measured',sigf(F.oa,6)+' mm&sup2;')+rrow('axis, octupole closed form',sigf(octCoef(A.kind,A.N,'axis'),6)+' mm&sup2;')
      +rrow('bisector, measured',sigf(F.oe,6)+' mm&sup2;')+rrow('bisector, closed form',sigf(octCoef(A.kind,A.N,'bis'),6)+' mm&sup2;');
  } else {
    const N=M.nd;
    s+=hd('the rotor')+rrow('|B|',fB(N.Bmag))+rrow('&omega;<sub>0</sub> = &radic;(&kappa;|B|)',sigf(N.w0,4)+' rad/s')+rrow('small-swing period',sigf(N.T0,4)+' s','good')
      +rrow('damping ratio &zeta;',sigf(N.zeta,3),N.zeta<1?'':'bad')+rrow('released at',fmt(N.rel*R2D,0)+'&deg;');
    s+=hd('undamped, at this amplitude')+rrow('4K(sin &phi;<sub>0</sub>/2)/&omega;<sub>0</sub>',sigf(N.Tbig,5)+' s')+rrow('ratio to small swings',fmt(N.Tbig/N.T0,4));
    s+=hd('the integration')+rrow('first period, measured',isFinite(N.Tmeas)?sigf(N.Tmeas,5)+' s':'&mdash; (no second crossing)')+rrow('energy ledger error',sigf(N.ledger,2));
  }
  s+='</table><div class="note">'+noteFor(M)+'</div>';
  return s;
}
function noteFor(M){
  if(M.view==='bar'||M.view==='lines'||M.view==='axis'||M.view==='far')
    return 'The magnet is a uniformly magnetised cylinder, 250 mm &times; &oslash;50 mm, whose field is exactly that of a solenoid carrying its bound current (Derby &amp; Olbert&rsquo;s closed form). PhET&rsquo;s precomputed grid is a sampling of this same field. 1 PhET px = 1 mm here.';
  if(M.view==='em') return 'Each loop is a thin filament along the drawn wire, its field exact Biot&ndash;Savart (complete elliptic integrals). The current is scaled so that 4 loops at full current make PhET&rsquo;s 300 G at the centre.';
  return 'The compass is a damped rotor with PhET&rsquo;s constants: &kappa; = 6.25 G<sup>&minus;1</sup>s<sup>&minus;2</sup>, &gamma; = 2 s<sup>&minus;1</sup> (modelled, not measured).';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='bar') return E('<span class="hl">B = &mu;<sub>0</sub>(H + M)</span>, &nbsp;&nabla;&middot;B = 0 &nbsp;&rArr;&nbsp; <span class="hl2">B<sub>magnet</sub> = B<sub>solenoid</sub></span> with K = M &times; n&#770;',
    'a uniformly magnetised bar makes exactly the field of a solenoid carrying its bound surface current; the needles follow B');
  if(M.view==='em') return E('<span class="hl">B(r) = (&mu;<sub>0</sub>I/4&pi;) &#8750; dl &times; (r &minus; r&prime;)/|r &minus; r&prime;|&sup3;</span> &nbsp;&middot;&nbsp; on the axis <span class="hl2">B<sub>x</sub> = &Sigma;<sub>k</sub> &mu;<sub>0</sub>I a&sup2;/2(a&sup2; + (x &minus; x<sub>k</sub>)&sup2;)<sup>3/2</sup></span>',
    'Biot&ndash;Savart, loop by loop: the field grows with the current and the number of loops, and reverses with the current');
  if(M.view==='lines') return E('<span class="hl">dr/ds = B/|B|</span> &nbsp;&middot;&nbsp; <span class="hl2">&Psi;(&rho;, u) = &rho;A<sub>&phi;</sub> = const</span> along a line &nbsp;&middot;&nbsp; flux between neighbours 2&pi;&Delta;&Psi;',
    'B lines never end: each one leaves the north face, returns to the south face and runs back through the magnet');
  if(M.view==='axis') return E('<span class="hl">B<sub>x</sub>(x) = &frac12;&mu;<sub>0</sub>M [ (x+b)/&radic;((x+b)&sup2;+R&sup2;) &minus; (x&minus;b)/&radic;((x&minus;b)&sup2;+R&sup2;) ]</span> &nbsp;&middot;&nbsp; <span class="hl2">&mu;<sub>0</sub>H = B &minus; &mu;<sub>0</sub>M</span> inside',
    'on the axis the field is elementary; B is continuous at the pole faces, H jumps by M there and points backwards inside');
  if(M.view==='far') return E('<span class="hl">B &rarr; (&mu;<sub>0</sub>/4&pi;) [3(m&middot;r&#770;)r&#770; &minus; m]/r&sup3;</span> &nbsp;&middot;&nbsp; m = MV (magnet), N I &pi;a&sup2; (coil) &nbsp;&middot;&nbsp; <span class="hl2">B/B<sub>dip</sub> &minus; 1 &asymp; C/r&sup2;</span>',
    'far away every magnet is a point dipole; the first correction is the octupole, falling two powers of r faster');
  return E('<span class="hl">&phi;&Prime; = &kappa;|B| sin(&theta;<sub>B</sub> &minus; &phi;) &minus; &gamma;&phi;&prime;</span> &nbsp;&middot;&nbsp; <span class="hl2">T<sub>0</sub> = 2&pi;/&radic;(&kappa;|B|)</span> &nbsp;&middot;&nbsp; T(&phi;<sub>0</sub>) = 4K(sin &phi;<sub>0</sub>/2)/&omega;<sub>0</sub>',
    'a compass needle is a pendulum in the field: it swings faster in a stronger field, and its period measures |B|');
}
function tagHTML(M){
  const st=ST;
  if(M.view==='bar') return '<b>the bar magnet</b> — '+fB(S_MAX*st.pct/100)+(st.bar.ang?', flipped':'');
  if(M.view==='em') return '<b>the electromagnet</b> — '+st.loops+' loop'+(st.loops>1?'s':'')+', '+(st.supply==='dc'?'battery':'AC supply');
  if(M.view==='lines') return '<b>field lines</b> — '+M.as.label;
  if(M.view==='axis') return '<b>on the axis</b> — '+M.as.label;
  if(M.view==='far') return '<b>the far field</b> — '+M.as.label;
  return '<b>the needle</b> — |B| = '+fB(st.ndB)+', released at '+st.ndRel+'°';
}
