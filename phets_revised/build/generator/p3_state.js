
/* ================================================================== *
 *  state, the per-view model, readout, equation bar, tag              *
 *  (PhET's Generator screen, on the family's engine)                  *
 * ================================================================== */
const TABS=[['gen','the generator'],['flux','flux and EMF'],['face','the coil face'],
            ['lines','field lines'],['axis','on the axis'],['needle','the needle']];
const COL={north:'#b8ec4c', south:'#cd35c4', needleS:'#7d8596', ref:'#e8843a', struct:'#5ac8e0', live:'#f2f4f8', dim:'#8b93a6',
           copper:'#c9905c', bound:'#5ac8e0', edge:'#242a3a', grid:'#141b2a', water:'#3d7fa8', glass:'#ffe38a'};
const RO_W=300;
function clone(o){ return JSON.parse(JSON.stringify(o)); }
const DEFAULTS={view:'gen', units:'G', flowConv:'electron', run:true,
  /* PhET's defaults: the faucet closed, the magnet at 75 %, 2 loops, half area, the bulb */
  flow:0, pct:75, N:2, area:50, indicator:'bulb', th:0,
  genField:true, seeInside:false, electrons:true, genCompass:true, genMeter:false,
  genC:{x:300,y:520}, genM:{x:800,y:470},
  /* the analysis views */
  phetCmp:true, bound:true, axisH:true, ndB:5, ndRel:60, ndDamp:2};
const ST=clone(DEFAULTS);
const LIVE={t:0, ndT:0, genRot:null, ePhase:0};
function resetLive(){ LIVE.t=0; LIVE.ndT=0; LIVE.genRot=null; LIVE.ePhase=0; }
function resetState(over){ Object.assign(ST,clone(DEFAULTS),over?clone(over):{}); resetLive(); }

/* the turbine's magnet at its present angle, and the generator's settings in one object */
function turbMagnet(st,th){ return {kind:'magnet',x:TURB_X,y:TURB_Y,ang:(th===undefined?st.th:th),S:S_MAX*st.pct/100}; }
function genState(st){ return {N:st.N, area:st.area, flow:st.flow, strength:st.pct, th:st.th}; }
function wrap2pi(a){ a%=2*Math.PI; return a<0?a+2*Math.PI:a; }
/* the compass needle starts along the field, as PhET's does */
function rotorFor(key,src,p){
  if(!LIVE[key]){ const B=sourceField(src,p.x,p.y,0); LIVE[key]={phi:Math.atan2(B[1],B[0]),om:0,W:0,rest:true}; }
  return LIVE[key];
}
/* The water falls on the left of the wheel, so the magnet's angle INCREASES: omega =
   dtheta/dt > 0.  (PhET steps its own angle the other way, by -2 pi (flow/100)/25 per frame;
   the sign of omega only reverses the EMF.)  The clock is the page's, not PhET's 25 fps. */
function stepLive(dt){
  const st=ST; let moved=false;
  dt=Math.min(dt,0.05);
  if(st.view==='gen'){
    const g=genState(st), rpm=genRPM(g), om=2*Math.PI*rpm/60;
    const th0=st.th;
    if(om>0){ st.th=wrap2pi(st.th+om*dt); moved=true; }
    if(st.electrons){
      const R=genReadings(genState(st));
      if(Math.abs(R.norm)>1e-12){ LIVE.ePhase=(LIVE.ePhase+R.norm*dt*(st.flowConv==='electron'?1:-1)+1)%1; moved=true; }
    }
    if(st.genCompass){
      const r=rotorFor('genRot',turbMagnet(st),st.genC);
      /* the field at the compass while the magnet turns: the rotor integrates through it */
      const Bfun=t=>sourceField(turbMagnet(st,th0+om*(dt+t)),st.genC.x,st.genC.y,0);
      moved=rotorTick(r,Bfun,dt)||moved;
    }
  }
  if(st.view==='needle'){ LIVE.ndT+=dt; if(LIVE.ndT>needleWindow(st)) LIVE.ndT=0; moved=true; }
  return moved;
}
/* one frame of the rotor; at rest in a steady field it stops, so a settled page draws nothing */
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
function needleWindow(st){ const w0=Math.sqrt(KAPPA*st.ndB); return Math.max(4,Math.min(24,7*2*Math.PI/w0)); }
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
/* the analysis views see the same bar magnet, upright in its own frame */
function analysisSource(st){ return {kind:'magnet',N:0,unit:S_MAX*st.pct/100,label:'the turbine’s bar magnet'}; }

/* one turn of the wheel, sampled for the flux view: Phi(th) and the EMF that follows it */
function fluxCurve(st){
  const g=genState(st), rd=genReadings(g), ser=rd.ser, n=361, th=[], phi=[], emf=[], one=[], oneE=[];
  const a1=ser.a[1];
  for(let i=0;i<n;i++){
    const t=2*Math.PI*i/(n-1); th.push(t);
    phi.push(fluxOf(ser,t,g.N,rd.S));
    emf.push(emfOf(ser,t,g.N,rd.S,rd.omega));
    /* the first harmonic alone: the sinusoid a far-off magnet (a point dipole) would give */
    one.push(g.N*rd.S*a1*Math.cos(t)*WB_PER_G_MM2);
    oneE.push(g.N*rd.S*a1*rd.omega*Math.sin(t)*WB_PER_G_MM2);
  }
  const pk=emfPeak(ser);
  return {th,phi,emf,one,oneE,pk,rd,g,a1,
          emfPk:g.N*rd.S*pk.val*rd.omega*WB_PER_G_MM2, emf90:g.N*rd.S*pk.at90*rd.omega*WB_PER_G_MM2};
}
/* The coil face.  Both flux estimates are integrals over the radius once PhET's is folded
   about the centre (its samples come in pairs at +-y), so the two INTEGRANDS can be drawn on
   one axis and their areas are the two numbers:
     exact  e(s) = <B_x>(s) 2 pi s        PhET  p(s) = q(s) + q(-s),  q(y) = B_x(y,0) chord(y)
   Their difference is the whole of PhET's error, at any angle of the magnet. */
function faceIntegrands(th,rc,n){
  const s=[], ex=[], ph=[];
  for(let i=0;i<n;i++){ const y=rc*(2*i/(n-1)-1); s.push(y); ex.push(chordBx(th,y,rc)); ph.push(chordPhet(th,y,rc)); }
  return {s,ex,ph};
}
function faceCurve(st){
  const rd=genReadings(genState(st)), rc=rd.rc, C=faceIntegrands(st.th,rc,121);
  const exact=flux1(st.th,rc), phet=fluxPhet1(st.th,rc);
  const sp=[]; const m=Math.floor(rc/PHET_SP);
  for(let k=-m;k<=m;k++){ const y=k*PHET_SP; sp.push({s:y,p:chordPhet(st.th,y,rc)}); }
  /* the same comparison across the area slider, which is where the error really shows */
  const pcts=[], ratio=[];
  for(let p=PICK_AMIN_PCT;p<=100;p+=5){ const r=pickRadius(p); pcts.push(p); ratio.push(fluxPhet1(st.th,r)/flux1(st.th,r)); }
  return {rc,s:C.s,ex:C.ex,ph:C.ph,sp,exact,phet,ratio:phet/exact,pcts,ratios:ratio,rd};
}

function buildModel(){
  const st=ST, v=st.view, M={view:v,st};
  if(v==='gen'){
    M.src=turbMagnet(st);
    M.g=genState(st);
    M.R=genReadings(M.g);
    M.rot=st.genCompass?rotorFor('genRot',M.src,st.genC):null;
    M.meter=st.genMeter?meterReading(M.src,st.genM.x,st.genM.y):null;
    M.atCompass=meterReading(M.src,st.genC.x,st.genC.y);
  } else if(v==='flux'){
    M.fx=memo('flux',[st.N,st.area,st.pct,st.flow,st.th].join('|'),()=>fluxCurve(st));
  } else if(v==='face'){
    M.fc=memo('face',[st.area,st.pct,st.th,st.N].join('|'),()=>faceCurve(st));
  } else if(v==='lines'||v==='axis'){
    M.as=analysisSource(st);
    if(v==='lines') M.fl=fieldLinesFor('magnet',0);
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
  const zc=[]; for(let i=1;i<ph.length;i++) if(ph[i-1]>0&&ph[i]<=0) zc.push(ts[i-1]+(ts[i]-ts[i-1])*ph[i-1]/(ph[i-1]-ph[i]));
  return {Bmag,rel,gam,Tw,ts,ph,lin,w0,T0:2*Math.PI/w0,zeta:gam/(2*w0),under:disc>0,wd:disc>0?Math.sqrt(disc):NaN,
          Tbig:4*ellK(Math.cos(rel/2))/w0, Tmeas:zc.length>=2?zc[1]-zc[0]:NaN, ledger:maxLedger/E0, E0};
}
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
function fPos(x,y){ return '('+fmt(x,0)+', '+fmt(y,0)+') mm'; }
function fV(v){ return sigf(v*1e3,3)+' mV'; }
function fWb(v){ return sigf(v,3)+' Wb'; }
function magMoment(S){ return S/G_PER_T/MU0*Math.PI*Math.pow(MAG_R*1e-3,2)*MAG_L*1e-3; }
function meterRows(rd,title){
  if(!rd) return '';
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
  let s='<div class="rname">generator<small>'+name+'</small></div><table>';
  if(M.view==='gen'){
    const R=M.R;
    s+=hd('the turbine')+rrow('water flow',fmt(st.flow,0)+' %')+rrow('drag of the coil',fmt(R.drag,4))
      +rrow('speed',fmt(R.rpm,2)+' RPM',R.rpm>0?'good':'')+rrow('the magnet points',fmt(wrap2pi(st.th)*R2D,0)+'&deg;')
      +rrow('strength &mu;<sub>0</sub>M',fB(R.S)+' ('+st.pct+' %)');
    s+=hd('the pickup coil')+rrow('loops N',st.N)+rrow('loop area',fmt(pickArea(st.area),0)+' mm&sup2; ('+st.area+' %)')
      +rrow('its radius',fmt(R.rc,1)+' mm')
      +rrow('&Phi; through all N',fWb(R.Phi))+rrow('EMF = &minus;N d&Phi;/dt',fV(R.emf),Math.abs(R.emf)>0?'good':'')
      +rrow(st.indicator==='bulb'?'bulb brightness':'voltmeter needle',
            st.indicator==='bulb'?fmt(100*Math.min(1,R.bulb),0)+' %':fmt(R.needle,1)+'&deg;');
    s+=compassRows(M.rot,M.atCompass)+meterRows(M.meter,'the field meter');
  } else if(M.view==='flux'){
    const F=M.fx;
    s+=hd('one turn of the wheel')+rrow('at '+fmt(F.rd.rpm,2)+' RPM',F.rd.omega>0?sigf(2*Math.PI/F.rd.omega,3)+' s per turn':'&mdash; (the wheel is still)')
      +rrow('&Phi; peak (N = '+F.g.N+')',fWb(Math.max.apply(null,F.phi.map(Math.abs))))
      +rrow('EMF peak',F.rd.omega>0?fV(Math.abs(F.emfPk)):'&mdash;',F.rd.omega>0?'good':'')
      +rrow('at magnet angle',fmt(F.pk.th*R2D,2)+'&deg;')
      +rrow('EMF at 90&deg;',F.rd.omega>0?fV(Math.abs(F.emf90)):'&mdash;')
      +rrow('90&deg; as a fraction of the peak',fmt(F.pk.at90/F.pk.val,4));
    s+=hd('the flux as a Fourier series, through all N')
      +[1,3,5,7].map(k=>rrow('a<sub>'+k+'</sub>',fWb(F.g.N*F.rd.S*F.rd.ser.a[k]*WB_PER_G_MM2))).join('')
      +rrow('a<sub>3</sub>/a<sub>1</sub>',fmt(F.rd.ser.a[3]/F.rd.ser.a[1],4));
  } else if(M.view==='face'){
    const C=M.fc;
    s+=hd('the coil face')+rrow('radius',fmt(C.rc,2)+' mm')+rrow('area',fmt(Math.PI*C.rc*C.rc,0)+' mm&sup2;')
      +rrow('&Phi; per loop, exact',fWb(C.exact*C.rd.S*WB_PER_G_MM2))
      +rrow('PhET&rsquo;s line sample',fWb(C.phet*C.rd.S*WB_PER_G_MM2))
      +rrow('its error',fmt(100*(C.ratio-1),1)+' %',Math.abs(C.ratio-1)>0.05?'bad':'');
    s+=hd('across the area slider')+rrow('at 20 %',fmt(100*(C.ratios[0]-1),1)+' %')
      +rrow('at 100 %',fmt(100*(C.ratios[C.ratios.length-1]-1),1)+' %')
      +rrow('sample points',C.sp.length)+rrow('their spacing',fmt(PHET_SP,0)+' mm');
  } else if(M.view==='lines'){
    const F=M.fl, u=M.as.unit, okN=F.lines.filter(l=>l.ok).length;
    let wc=0; for(const l of F.lines) if(l.ok) wc=Math.max(wc,l.close);
    s+=hd(M.as.label)+rrow('lines each side',F.lines.length)+rrow('closed on themselves',okN+' of '+F.lines.length,okN===F.lines.length?'good':'bad')
      +rrow('worst closure',sigf(wc,2)+' mm')+rrow('flux through the middle',u?sigf(2*Math.PI*F.psiMax*Math.abs(u)*WB_PER_G_MM2,3)+' Wb':'&mdash; (no field)')
      +rrow('between neighbours',u?sigf(2*Math.PI*F.psiMax*Math.abs(u)*WB_PER_G_MM2/(F.lines.length+1),3)+' Wb':'&mdash;');
    s+=hd('where they cross the mid-plane outside')+F.lines.slice(-4).reverse().map((l,i)=>rrow('line '+(F.lines.length-i),fmt(l.rOut,1)+' mm')).join('');
  } else if(M.view==='axis'){
    const S=M.as.unit;
    s+=hd('the bar magnet on its axis')+rrow('B at the centre',fB(S*solAxis(0,MAG_R,MAG_B)),'good')+rrow('B at a pole face',fB(S*solAxis(MAG_B,MAG_R,MAG_B)))
      +rrow('&mu;<sub>0</sub>H at the centre',fB(S*(solAxis(0,MAG_R,MAG_B)-1)))+rrow('jump of &mu;<sub>0</sub>H at a face',fB(S))
      +rrow('cos &alpha; = b/&radic;(b&sup2;+R&sup2;)',fmt(solAxis(0,MAG_R,MAG_B),6))
      +rrow('moment m = MV',S?sigf(magMoment(S),3)+' A&middot;m&sup2;':'&mdash;');
  } else {
    const N=M.nd;
    s+=hd('the rotor')+rrow('|B|',fB(N.Bmag))+rrow('&omega;<sub>0</sub> = &radic;(&kappa;|B|)',sigf(N.w0,4)+' rad/s')+rrow('small-swing period',sigf(N.T0,4)+' s','good')
      +rrow('damping ratio &zeta;',sigf(N.zeta,3),N.zeta<1?'':'bad')+rrow('released at',fmt(N.rel*R2D,0)+'&deg;');
    s+=hd('undamped, at this amplitude')+rrow('4K(sin &phi;<sub>0</sub>/2)/&omega;<sub>0</sub>',sigf(N.Tbig,5)+' s')+rrow('ratio to small swings',fmt(N.Tbig/N.T0,4));
    s+=hd('the integration')+rrow('first period, measured',isFinite(N.Tmeas)?sigf(N.Tmeas,5)+' s':'&mdash; (no second crossing)')+rrow('energy ledger error',sigf(N.ledger,2));
  }
  s+='</table><div class="note">'+(M.view==='needle'
    ?'The compass is a damped rotor with PhET&rsquo;s constants: &kappa; = 6.25 G<sup>&minus;1</sup>s<sup>&minus;2</sup>, &gamma; = 2 s<sup>&minus;1</sup> (modelled, not measured).'
    :'The magnet is a uniformly magnetised cylinder, 250 mm &times; &oslash;50 mm, whose field is exactly that of a solenoid carrying its bound current. &Phi; is the area integral of B<sub>x</sub> over the coil&rsquo;s disc (16 &times; 32 Gauss&ndash;Legendre), and the EMF is &minus;N &omega; d&Phi;/d&theta; from its Fourier series. 1 PhET px = 1 mm here.')+'</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='gen') return E('<span class="hl">&#8496; = &minus;N d&Phi;/dt</span> &nbsp;=&nbsp; <span class="hl2">&minus;N &omega; d&Phi;/d&theta;</span>, &nbsp; &Phi;(&theta;) = &int;<sub>disc</sub> B&middot;dA',
    'Faraday&rsquo;s law: it is the CHANGE of flux that drives the current, so a magnet at rest does nothing however strong it is');
  if(M.view==='flux') return E('<span class="hl">&Phi;(&theta;) = &sum;<sub>k odd</sub> a<sub>k</sub> cos k&theta;</span> &nbsp;&rArr;&nbsp; <span class="hl2">&#8496;(&theta;) = N&omega; &sum;<sub>k</sub> k a<sub>k</sub> sin k&theta;</span>',
    'the flux is even in the angle and reverses every half turn, so only odd harmonics survive; the EMF is their derivative, and peaks well before 90&deg;');
  if(M.view==='face') return E('<span class="hl">&Phi; = &int;<sub>0</sub><sup>r</sup> &#10216;B<sub>x</sub>&#10217;(s) 2&pi;s ds</span> &nbsp;&nbsp;vs&nbsp;&nbsp; <span class="hl2">&sum;<sub>k</sub> B<sub>x</sub>(0, y<sub>k</sub>) &middot; 2&radic;(r&sup2;&minus;y<sub>k</sub>&sup2;) &Delta;y</span>',
    'the flux is an AREA integral; sampling the field only along the coil&rsquo;s vertical diameter assumes it holds off the page, where it is weaker');
  if(M.view==='lines') return E('<span class="hl">dr/ds = B/|B|</span> &nbsp;&middot;&nbsp; <span class="hl2">&Psi;(&rho;, u) = &rho;A<sub>&phi;</sub> = const</span> along a line &nbsp;&middot;&nbsp; flux between neighbours 2&pi;&Delta;&Psi;',
    'B lines never end: each one leaves the north face, returns to the south face and runs back through the magnet');
  if(M.view==='axis') return E('<span class="hl">B<sub>x</sub>(x) = &frac12;&mu;<sub>0</sub>M [ (x+b)/&radic;((x+b)&sup2;+R&sup2;) &minus; (x&minus;b)/&radic;((x&minus;b)&sup2;+R&sup2;) ]</span> &nbsp;&middot;&nbsp; <span class="hl2">&mu;<sub>0</sub>H = B &minus; &mu;<sub>0</sub>M</span> inside',
    'on the axis the field is elementary; B is continuous at the pole faces, H jumps by M there and points backwards inside');
  return E('<span class="hl">&phi;&Prime; = &kappa;|B| sin(&theta;<sub>B</sub> &minus; &phi;) &minus; &gamma;&phi;&prime;</span> &nbsp;&middot;&nbsp; <span class="hl2">T<sub>0</sub> = 2&pi;/&radic;(&kappa;|B|)</span> &nbsp;&middot;&nbsp; T(&phi;<sub>0</sub>) = 4K(sin &phi;<sub>0</sub>/2)/&omega;<sub>0</sub>',
    'a compass needle is a pendulum in the field: it swings faster in a stronger field, and its period measures |B|');
}
function tagHTML(M){
  const st=ST;
  if(M.view==='gen') return '<b>the generator</b> — '+fmt(st.flow,0)+' % flow, '+st.N+' loop'+(st.N>1?'s':'')+', '+st.area+' % area';
  if(M.view==='flux') return '<b>flux and EMF</b> — over one turn of the wheel';
  if(M.view==='face') return '<b>the coil face</b> — the area integral against PhET’s line sample';
  if(M.view==='lines') return '<b>field lines</b> — the turbine’s bar magnet';
  if(M.view==='axis') return '<b>on the axis</b> — the turbine’s bar magnet';
  return '<b>the needle</b> — |B| = '+fB(st.ndB)+', released at '+st.ndRel+'°';
}
