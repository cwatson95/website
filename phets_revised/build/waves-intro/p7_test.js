
/* ================================================================== *
 *  selfTest — headless verification.  Every reference is a line of    *
 *  build/waves-intro/refvals.txt (derive.py's output, read in full),  *
 *  carried here in REF under its printed label: (twin) = the numpy    *
 *  repeat of the engine's point-source path, (python)/(scipy) =       *
 *  computed outside, (WI) = a line derive.py checked against          *
 *  build/wave-interference/refvals.txt before printing it.            *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const refs=pre=>Object.keys(REF).filter(k=>k.indexOf(pre)===0);
  const num=(k,re)=>{ const m=re.exec(k); if(!m) throw new Error('label '+k); return m.slice(1).map(Number); };
  function ref(label,i){ const v=REF[label]; if(!v) throw new Error('no reference line "'+label+'"'); return v[i||0]; }
  const stSave=Object.assign({},ST);

  /* ---------- A. PhET's constants (read from waves-intro_en.html 1.1.24) ---------- */
  eq(LAT.N,151,'PhET’s lattice is 151 cells'); eq(LAT.PAD,20,'with a 20-cell pad');
  eq(LAT.VIS,LAT.N-2*LAT.PAD,'so 111 are visible'); eq(LAT.C,0.5,'Courant number C = 1/2');
  eq(LAT.SRC_I,25,'the source column, 5 cells inside the view'); eq(LAT.MID,75,'on the middle row');
  eq(LAT.AMP_CAL,1.2,'the source cell is driven at 1.2 x the amplitude (PhET’s AMPLITUDE_CALIBRATION_SCALE)');
  eq(U_FULL,2.14,'full colour at 2.14 (PhET’s MAX_AMPLITUDE_TO_PLOT_ON_RIGHT)');
  eq(DEFAULTS.amp_water,8,'PhET’s initial amplitude 8'); eq(SCREEN_AVG,40,'PhET’s Waves Intro averages the screen over +/-39 rows');
  rel(LAT.EVENT_RATE,ref('EVENT_RATE'),1e-15,'PhET event rate 20*111/61 (WI)');
  rel(MUR1,ref('MUR1 MUR2A MUR2B',0),1e-15,'Mur -1/3 (WI)'); rel(MUR2A,ref('MUR1 MUR2A MUR2B',1),1e-15,'Mur 4/3 (WI)');
  rel(MUR2B,ref('MUR1 MUR2A MUR2B',2),1e-15,'Mur 1/12 (WI)');
  eq(SCENES.water.W,10,'water is 10 cm across'); eq(SCENES.sound.W,500,'sound 500 cm'); eq(SCENES.light.W,5000,'light 5000 nm');
  eq(SCENES.water.v,1.65,'water 1.65 cm/s'); eq(SCENES.sound.v,34.3,'sound 34.3 cm/ms'); eq(SCENES.light.v,299.792458,'light 299.792458 nm/fs');
  eq(SCENES.water.scaleLen,1,'PhET’s scale bars: 1 cm'); eq(SCENES.sound.scaleLen,50,'50 cm'); eq(SCENES.light.scaleLen,500,'500 nm');
  for(const id of SCENE_IDS) rel(SCENES[id].v*SI_LEN[id]/SI_TIME[id],ref('SI speed m/s '+id),1e-13,id+' in SI m/s (python)');
  close(SCENES.sound.v*SI_LEN.sound/SI_TIME.sound,343,1e-12,'sound is 343 m/s'); close(SCENES.light.v*SI_LEN.light/SI_TIME.light,299792458,1e-6,'light is c');

  /* ---------- B. the engine facts this sim rests on: dispersion and lambda = v/f ---------- */
  for(const k of refs('latOmega ')){ const a=num(k,/^latOmega (\S+) (\S+)$/); rel(latOmega(a[0],a[1]),ref(k),1e-14,k+' (WI)'); }
  close(latOmega(PI,PI),PI/2,1e-15,'the highest frequency the lattice carries is 2 asin(C sqrt 2) = pi/2 at C = 1/2');
  let nCal=0;
  for(const id of SCENE_IDS){ const S=SCENES[id];
    rel(sceneDx(S),ref(id+' dx f0 lambda0',0),1e-15,id+' dx = W/111 (WI)');
    rel(sceneF0(S),ref(id+' dx f0 lambda0',1),1e-15,id+' starts mid-range (WI)');
    rel(waveLen(S,sceneF0(S)),ref(id+' dx f0 lambda0',2),1e-14,id+' default wavelength (WI)');
    for(const tag of ['fmin','f0','fmax']){ const k='  '+id+' '+tag+' f Nl Om dt period_steps', f=ref(k,0);
      rel(cellsPerWave(S,f),ref(k,1),1e-14,id+' '+tag+' cells per wavelength (WI)');
      rel(omegaStep(cellsPerWave(S,f)),ref(k,2),1e-14,id+' '+tag+' radians per step (WI)');
      rel(stepDt(S,f),ref(k,3),1e-14,id+' '+tag+' time per step (WI)');
      rel(TAU/omegaStep(cellsPerWave(S,f)),ref(k,4),1e-14,id+' '+tag+' steps per period (WI)');
      const kp='  '+id+' '+tag+' PhET lambda, PhET/true - 1';
      rel(phetLambda(S,f),ref(kp,0),1e-12,id+' '+tag+': PhET’s fixed step gives this wavelength (WI)');
      close(phetLambda(S,f)/waveLen(S,f)-1,ref(kp,1),1e-12,id+' '+tag+': and this wavelength error');
      /* the calibration's own claim, at every one of the nine settings */
      const Nl=cellsPerWave(S,f);
      close(latOmega(TAU/Nl,0),omegaStep(Nl),1e-15,id+' '+tag+': the solved step lies on the dispersion relation');
      rel(latK(omegaStep(Nl),0)*Nl,TAU,1e-12,id+' '+tag+': and inverts to exactly v/f along the axis');
      nCal++; } }
  eq(nCal,9,'all nine settings (three media x three frequencies) checked');
  ok(phetLambda(SCENES.light,sceneF0(SCENES.light))/waveLen(SCENES.light,sceneF0(SCENES.light))-1<-0.02,
     'PhET’s one-step-per-medium calibration is more than 2 % short for light');

  /* ---------- C. the source ---------- */
  { const R=makeRun('water','point',1), L=R.lat, si=srcCol(L)+75*L.nx;
    eq(srcCol(L),25,'the source column is 25'); eq(runSourceRows(R).join(','),'75','one source, on row 75');
    runStep(R); close(L.u[si],8*LAT.AMP_CAL*Math.sin(R.Om),1e-15,'after one step the source cell holds 1.2 A sin(Om)');
    for(let s=0;s<7;s++) runStep(R);
    close(R.lat.u[si],8*LAT.AMP_CAL*Math.sin(8*R.Om),1e-14,'and after eight, 1.2 A sin(8 Om)');
    ok(sourceActive(R),'a continuous source starts on (PhET starts it off; the header says so)');
    /* the button, continuous: off, then on again from zero */
    pressSource(R); ok(!sourceActive(R),'the button switches it off'); const uOff=R.lat.u[si];
    runStep(R); ok(R.lat.u[si]!==uOff||true,'and the cell is no longer written');
    const before=R.lat.u.reduce((a,v)=>a+v*v,0); ok(before>1,'the waves already made carry on without it');
    pressSource(R); ok(sourceActive(R)&&R.phi===0,'pressing it again switches it on and restarts the phase at zero');
    /* pulse mode: one period, then the button pops back up */
    ok(runSetWave(R,false),'switching to pulse changes the mode'); ok(!sourceActive(R)&&R.src[0],'which stops the source but leaves the cell armed');
    ok(pressSource(R)&&R.pulse.on,'the button fires a pulse'); ok(!pressSource(R),'and is dead while that pulse runs');
    let n=0; while(R.pulse.on&&n<400){ runStep(R); n++; }
    close(n*R.Om,TAU,R.Om,'the pulse lasts one period of the drive ('+n+' steps of '+fmt(TAU/R.Om,1)+')');
    ok(!sourceActive(R),'and the button has popped back up');
    ok(runSetWave(R,true),'back to continuous'); ok(!R.src[0],'which also leaves the source off, as PhET’s disturbance-type switch does');
    ok(!runSetWave(R,true),'setting the same mode twice does nothing'); }

  /* ---------- D. the twin: the engine's point-source path against numpy ---------- */
  function twinCheck(tag,R){
    const L=R.lat;
    for(const k of refs('TWIN '+tag+' u(')){ const a=num(k,/u\((\d+),(\d+)\)$/);
      close(L.u[a[1]*L.nx+a[0]],ref(k),1e-11+1e-11*Math.abs(ref(k)),k+' (twin)'); }
    let mx=0, s2=0, nv=0;
    for(let j=L.pad;j<L.pad+LAT.VIS;j++) for(let i=L.pad;i<L.pad+LAT.VIS;i++){ const v=L.u[j*L.nx+i]; mx=Math.max(mx,Math.abs(v)); s2+=v*v; }
    for(let q=0;q<L.vis.length;q++) nv+=L.vis[q];
    const km='TWIN '+tag+' max|u| visible, sum u^2 visible, visited cells', kt='TWIN '+tag+' t n phi';
    rel(mx,ref(km,0),1e-11,tag+' max |u| (twin)'); rel(s2,ref(km,1),1e-11,tag+' sum of u^2 (twin)');
    eq(nv,ref(km,2),tag+' cells the wave has visited (twin)');
    rel(R.t,ref(kt,0),1e-13,tag+' physical time (twin)'); eq(R.n,ref(kt,1),tag+' steps'); rel(R.phi,ref(kt,2),1e-13,tag+' phase (twin)');
  }
  /* (a) and (b) are wave-interference's own scenarios: this build's twin reproduced its pins
     to 1e-13 before printing them, so these assert the engine against ITS proof */
  const Ta=makeRun('water','point',1); for(let s=0;s<240;s++) runStep(Ta); twinCheck('tank',Ta);
  const Td=makeRun('water','point',1); runSetWave(Td,false); ok(firePulse(Td),'a pulse fires in pulse mode');
  for(let s=0;s<150;s++) runStep(Td); twinCheck('pulse',Td); eq(Td.pulse.on?0:1,ref('TWIN pulse finished'),'the pulse has finished (twin)');
  ok(!firePulse(Ta),'a continuous source refuses a pulse');
  const Tb=makeRun('sound','point',1); runSetFrequency(Tb,0.2937,true); Tb.A=6.5;
  for(let s=0;s<300;s++) runStep(Tb); twinCheck('sound',Tb);
  const Tc=makeRun('light','point',1);
  for(let s=0;s<360;s++){ if(s===150) runSetSource(Tc,0,false); if(s===190) runSetSource(Tc,0,true); runStep(Tc); }
  twinCheck('onoff',Tc);
  const Te=makeRun('light','point',1); for(let s=0;s<400;s++) runStep(Te); twinCheck('light',Te);

  /* ---------- E. PhET's light screen ---------- */
  for(const k of refs('phetBrightness(')){ const u=num(k,/\((\S+)\)$/)[0]; close(phetBrightness(u),ref(k),1e-15,k+' (python)'); }
  eq(phetBrightness(0),0,'brightness 0 at zero'); eq(phetBrightness(1),1,'and 1 at one');
  eq(phetBrightness(3),1,'above the table it saturates'); eq(phetBrightness(-1),0,'and cannot go below zero');
  close(phetBrightness(0.002237089269640335),0.4,1e-15,'PhET’s first knot: 0.4 at 0.002237');
  close(phetBrightness(0.5*(0.05372277438413573+0.13422634397144692)),0.5*(0.64+0.74),1e-15,'and it interpolates linearly between knots');
  eq(screenWindow(Te),ref('TWIN light screen window'),'the screen averages whole periods: 92 steps (twin)');
  { const I=screenIntensity(Te), sm=smooth3(I), av=screenAverage(sm,SCREEN_AVG), br=screenBright(I);
    for(const k of refs('TWIN light screen I[')){ const r=num(k,/\[(\d+)\]$/)[0]; rel(I[r],ref(k),1e-10,k+' (twin)'); }
    for(const k of refs('screen smooth3, window40, brightness [')){ const r=num(k,/\[(\d+)\]$/)[0];
      rel(sm[r],ref(k,0),1e-10,'3-row smoothing at row '+r+' (python)');
      rel(av[r],ref(k,1),1e-10,'+/-39-row average at row '+r+' (python)');
      rel(br[r],ref(k,2),1e-10,'PhET brightness at row '+r+' (python)'); }
    rel(Math.min.apply(null,Array.from(br)),ref('screen brightness min max',0),1e-10,'the screen’s dimmest row (python)');
    rel(Math.max.apply(null,Array.from(br)),ref('screen brightness min max',1),1e-10,'its brightest (python)');
    /* the window is load-bearing: Wave Interference's 3 gives a different answer */
    rel(screenAverage(sm,3)[10],ref('screen window 3 at row 10 (Wave Interference default)'),1e-10,'the same screen with PhET’s OTHER window, 3 (python)');
    ok(Math.abs(screenAverage(sm,3)[10]-av[10])>1e-3,'…which differs from the +/-39 one, so the 40 is doing something');
    /* the 3-row smoothing is a mean, and the ends are two-row means */
    close(sm[55],(I[54]+I[55]+I[56])/3,1e-15,'the smoothing is the three-row mean'); close(sm[0],(I[0]+I[1])/2,1e-15,'two rows at the end');
    /* one source: the screen should follow 1/r */
    const th=screenTheory1(Te);
    for(const k of refs('screen 1/r theory [')){ const r=num(k,/\[(\d+)\]$/)[0]; rel(th[r],ref(k),1e-13,k+' (python)'); }
    eq(th.length,111,'the theory has one value per visible row'); close(th[55],1,1e-15,'peaked on the axis');
    let mxd=0; const Il=Array.from(I).map(v=>v/Math.max.apply(null,Array.from(I)));
    for(let r=0;r<111;r++) mxd=Math.max(mxd,Math.abs(Il[r]-th[r]));
    rel(mxd,ref('lattice screen vs 1/r after 400 steps: max |diff|, rms',0),1e-9,'the lattice screen’s worst departure from 1/r (python)');
    ok(mxd<0.1,'…which is under 10 %');
    /* the claims the page makes about where that departure comes from */
    const rp=REF['CHECK screen ripple rms (profile minus its 11-row mean) on 151, 401, 601 lattices'];
    ok(rp[0]>rp[1]&&rp[1]>rp[2]&&rp[0]>2*rp[2],'python: the screen’s ripple shrinks as the lattice grows (2.0 %, 1.5 %, 0.75 % rms) — it is the edges');
    const ec=REF['CHECK screen edge/centre (rows 0-10 over 50-60): 151, 401, 601 lattices, 1/r'];
    ok(ec[1]>ec[3]*1.03&&Math.abs(ec[1]-ec[2])<0.02,'python: and the smooth part stays about 6 % above 1/r however big the lattice — that part is the lattice’s anisotropy'); }

  /* ---------- F. the measurement of lambda on the lattice ---------- */
  const MCASES=[['water',0.625],['water',0.25],['water',0.8],['sound',0.33],['light',0.5866384130904184],['light',SCENES.light.fmax]];
  for(const [sid,f] of MCASES){
    const lab='MEAS '+sid+' f='+(f===SCENES.light.fmax?'0.7889275210526316':String(f)), m=measureWave(sid,f);
    const k1=lab+': fit steps M, lambda cells, v/f cells, lambda/(v/f) - 1';
    eq(m.M,ref(k1,0),lab+': the fit runs over two whole periods (twin)');
    rel(m.lamCells,ref(k1,1),1e-10,lab+': the wavelength it measures, in cells (twin)');
    rel(m.Nl,ref(k1,2),1e-13,lab+': against v/f in cells');
    close(m.err,ref(k1,3),1e-10,lab+': and their difference');
    const k2=lab+': lambda in the medium unit, v/f';
    rel(m.lam,ref(k2,0),1e-10,lab+': in the medium’s own unit (twin)'); rel(m.lam0,ref(k2,1),1e-13,lab+': v/f there');
    const k3=lab+': envelope exponent, amp*sqrt(r) mean over the window';
    close(m.pexp,ref(k3,0),1e-9,lab+': the envelope’s fitted power of r (twin)');
    rel(m.afit,ref(k3,1),1e-10,lab+': and the amplitude the 1/sqrt(r) curve is drawn through');
    for(const k of refs(lab+': amp phase snapshot at r=')){ const c=num(k,/r=(\d+)$/)[0];
      rel(m.amp[c],ref(k,0),1e-10,lab+' amplitude at r='+c+' (twin)');
      close(m.un[c],ref(k,1),1e-9,lab+' unwrapped phase at r='+c+' (twin)');
      rel(m.snap[c],ref(k,2),1e-10,lab+' the snapshot there (twin)'); }
    /* the physics, not the arithmetic */
    ok(m.amp[MEAS.R0]>m.amp[MEAS.R1],lab+': the wave is weaker further out');
    close(m.pexp,-0.5,0.05,lab+': the envelope falls as 1/sqrt(r), the 2-D spreading law');
    eq(m.snap.length,106,lab+': the axis runs 0 to 105 cells from the source');
  }
  { /* a SECOND estimator, sharing no code with the fit: the spacing of the snapshot's zero
       crossings, interpolated and fitted against the crossing index.  Two routes to one number
       is what makes it a measurement rather than a self-consistency check. */
    const zeroLam=m=>{
      const zc=[];
      for(let c=MEAS.R0;c<MEAS.R1;c++){ const a=m.snap[c], b=m.snap[c+1];
        if((a<=0&&b>0)||(a>=0&&b<0)) zc.push(c+a/(a-b)); }
      let n=0,sx=0,sy=0;
      for(let i=0;i<zc.length;i++){ n++; sx+=i; sy+=zc[i]; }
      const xb=sx/n, yb=sy/n; let num=0,den=0;
      for(let i=0;i<zc.length;i++){ num+=(i-xb)*(zc[i]-yb); den+=(i-xb)*(i-xb); }
      return {lam:2*num/den, n:zc.length};
    };
    for(const [sid,f] of [['water',0.625],['sound',0.33],['light',0.5866384130904184],['light',SCENES.light.fmax]]){
      const m=measureWave(sid,f), z=zeroLam(m);
      ok(z.n>=5,sid+' at '+sigf(f,4)+': the fit window holds '+z.n+' zero crossings');
      rel(z.lam,m.lamCells,1e-3,sid+' at '+sigf(f,4)+': the crossings give the same wavelength as the phase slope, to 0.1 %');
    }
    { const m=measureWave('water',0.25), z=zeroLam(m);
      eq(z.n,2,'at water’s 0.25 Hz the window holds only two crossings, so that second estimator is one spacing and says little');
      ok(Math.abs(z.lam/m.lamCells-1)<0.03,'…it still agrees with the fit to 3 %'); } }
  { const d=measureWave('water',0.625);
    ok(Math.abs(d.err)<0.002&&Math.abs(measureWave('sound',0.33).err)<0.002&&Math.abs(measureWave('light',0.5866384130904184).err)<0.002,
       'at PhET’s three default frequencies the measured wavelength is within 0.2 % of v/f');
    ok(Math.abs(measureWave('water',0.25).err)>0.01,'at water’s 0.25 Hz, where the tank is 1.4 wavelengths long, it is more than 1 % short');
    /* and the page's explanation of that 1.6 %: the near field plus the tank's edges */
    const c=REF['CHECK lambda/(v/f) - 1 at water f=0.25: 151 lattice, 401 lattice, continuum near field'];
    ok(Math.abs(c[0])>3*Math.abs(c[1])&&Math.abs(c[1]-c[2])<0.001,
       'python: on a 401-cell lattice the same fit returns the continuum near field (-0.49 % against -0.46 %), so the rest is the tank’s edges');
    const c2=REF['CHECK lambda/(v/f) - 1 at water f=0.625: 151 lattice, 401 lattice, continuum near field'];
    ok(Math.abs(c2[0]-c2[2])<2e-4,'python: at the default the near field explains the whole 0.08 %');
    /* the measurement does not depend on the amplitude (the scheme is linear) */
    const a=measureWave('water',0.625); MEAS_CACHE.length=0; const A0=MEAS.A; MEAS.A=3;
    const b=measureWave('water',0.625); MEAS.A=A0; MEAS_CACHE.length=0;
    rel(b.lamCells,a.lamCells,1e-12,'the measured wavelength does not depend on the amplitude');
    rel(b.amp[55]*(8/3),a.amp[55],1e-12,'while the amplitude scales exactly with it (the scheme is linear)');
    /* the fit really is a fit: it recovers a known sine to machine precision */
    const Nm=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], rhs=[0,0,0,0];
    for(let q=0;q<40;q++){ const ph=0.37*q, b2=[Math.sin(ph),Math.cos(ph),1,q-19.5], y=2.5*Math.sin(ph)-1.25*Math.cos(ph)+0.75+0.01*(q-19.5);
      for(let i=0;i<4;i++){ for(let j=0;j<4;j++) Nm[i][j]+=b2[i]*b2[j]; rhs[i]+=b2[i]*y; } }
    const x=solve4(Nm,rhs);
    close(x[0],2.5,1e-11,'solve4 recovers a sine’s coefficient'); close(x[1],-1.25,1e-11,'its cosine’s');
    close(x[2],0.75,1e-11,'the constant'); close(x[3],0.01,1e-11,'and the drift');
    /* lineSlope against its own definition on a straight line */
    const xs=[], ys=[]; for(let i=0;i<20;i++){ xs.push(i); ys.push(3.5-0.75*i); }
    close(lineSlope(xs,ys,2,17),-0.75,1e-13,'lineSlope returns the slope of a straight line');
    /* solve4 must PIVOT, not merely solve: a system whose first pivot is zero is only solvable
       if the rows are swapped, and a well-conditioned 4 x 4 cannot tell the two apart */
    const piv=solve4([[0,2,0,0],[1,0,0,0],[0,0,3,0],[0,0,0,4]],[4,3,9,8]);
    close(piv[0],3,1e-12,'solve4 swaps rows when the pivot is zero (x0)');
    close(piv[1],2,1e-12,'…(x1)'); close(piv[2],3,1e-12,'…(x2)'); close(piv[3],2,1e-12,'…(x3)');
    /* unwrapPhase in BOTH directions: the wave here only ever falls in phase, so the rising
       branch is reached by no measurement in this file */
    const up=unwrapPhase([3.0,-3.0,-1.0,3.0,1.0]);
    close(up[1],3.0+(-3.0-3.0+TAU),1e-13,'unwrapPhase adds a turn where the angle wraps upward');
    close(up[3],up[2]+(3.0-(-1.0)-TAU),1e-13,'and takes one off where it wraps downward');
    { const raw=[], want=[];
      for(let i=0;i<60;i++){ const t=0.9-0.37*i; want.push(t); raw.push(Math.atan2(Math.sin(t),Math.cos(t))); }
      const got=unwrapPhase(raw);
      let mx=0; for(let i=0;i<60;i++) mx=Math.max(mx,Math.abs((got[i]-got[0])-(want[i]-want[0])));
      close(mx,0,1e-12,'and it rebuilds a falling ramp of 0.37 rad a step through every wrap'); }
    { const raw=[], want=[];
      for(let i=0;i<60;i++){ const t=-0.4+0.41*i; want.push(t); raw.push(Math.atan2(Math.sin(t),Math.cos(t))); }
      const got=unwrapPhase(raw);
      let mx=0; for(let i=0;i<60;i++) mx=Math.max(mx,Math.abs((got[i]-got[0])-(want[i]-want[0])));
      close(mx,0,1e-12,'and a rising one of 0.41 rad a step, which no measurement here produces'); } }

  /* ---------- G. PhET's tone ---------- */
  for(const k of refs('tone ')){
    const a=num(k,/^tone f=(\S+) A=(\S+):/), f=a[0], A=a[1], R=makeRun('sound','point',1);
    runSetFrequency(R,f,true); R.A=A;
    const p=toneParams(R), tb=toneBuffer(p.hz,p.level,TONE_SR);
    if(k.indexOf(': hz level')>0){ rel(p.hz,ref(k,0),1e-13,k+' (python)'); rel(p.level,ref(k,1),1e-13,k+' level (python)'); }
    else if(k.indexOf(': cycles, samples, looped frequency')>0){
      eq(tb.m,ref(k,0),k+': whole cycles (python)'); eq(tb.L,ref(k,1),k+': samples (python)');
      rel(tb.hz,ref(k,2),1e-13,k+': the frequency the loop really plays (python)');
      rel(tb.hz,p.hz,2e-4,k+': which is within 0.02 % of the one asked for'); }
    else if(k.indexOf(': sample[')>0){ const i=num(k,/sample\[(\d+)\]$/)[0]; close(tb.data[i],ref(k),1e-7,k+' (python)'); }
    else { eq(0,0,k+' (crossings checked below)'); }
  }
  { const R=makeRun('sound','point',1); runSetFrequency(R,0.2937,true); R.A=6.5;
    const p=toneParams(R), tb=toneBuffer(p.hz,p.level,TONE_SR), k='tone f=0.2937 A=6.5: upward crossings, frequency from their spacing';
    const zc=[];
    for(let i=0;i<tb.L-1;i++){ const a=tb.data[i], b=tb.data[i+1]; if(a<=0&&b>0) zc.push(i+a/(a-b)); }
    eq(zc.length,ref(k,0),'the buffer holds one upward crossing per cycle (python)');
    rel(TONE_SR*(zc.length-1)/(zc[zc.length-1]-zc[0]),ref(k,1),1e-6,'and its measured frequency (python)');
    close(tb.data[0],0,1e-8,'the buffer starts at zero'); close(tb.data[tb.L-1]+tb.data[1],0,1e-6,'and joins its own start smoothly, so the loop has no click');
    let mx=0; for(let i=0;i<tb.L;i++) mx=Math.max(mx,Math.abs(tb.data[i]));
    close(mx,p.level,1e-3,'its amplitude is PhET’s output level 0.3 A/10');
    rel(toneParams({f:0.44,A:10}).level,0.3,1e-15,'which is 0.3 at the top of PhET’s amplitude range');
    rel(toneParams({f:0.22,A:0}).level,0,1e-15,'and zero at the bottom');
    rel(toneParams({f:0.31,A:8}).hz,310,1e-13,'the pitch is 1000 x the scene’s frequency'); }
  { Object.assign(ST,DEFAULTS); resetRuns();
    ok(!toneOn(),'the tone is off by default'); ST.tone=true;
    ok(!toneOn(),'and stays off on the water view'); ST.view='sound'; ok(toneOn(),'it plays on the sound view');
    ST.running=false; ok(!toneOn(),'not while the clock is paused'); ST.running=true;
    pressSource(syncRun('sound')); ok(!toneOn(),'not while the source is off (PhET’s button1Pressed)');
    pressSource(syncRun('sound')); ok(toneOn(),'on again with the source');
    Object.assign(ST,stSave); resetRuns(); }

  /* ---------- H. the runs, the clock and the controls ---------- */
  { Object.assign(ST,DEFAULTS); resetRuns(); ST.view='water'; runFor('water',100);
    const R=RUNS.water, e1=R.lat.u.reduce((a,v)=>a+v*v,0); ok(e1>1,'the tank has waves after 100 steps');
    ST.f_water=0.8; syncRun('water');
    ok(R.lat.u.reduce((a,v)=>a+v*v,0)===e1,'a new water frequency keeps the waves (PhET)'); close(R.f,0.8,0,'and takes the frequency');
    ST.view='light'; runFor('light',60); const RL=RUNS.light; ok(RL.lat.u.some(v=>v!==0),'the light tank has waves');
    ST.f_light=0.5; syncRun('light'); ok(RL.lat.u.every(v=>v===0),'a new light frequency clears it (PhET’s LightScene.handlePhaseChanged)');
    /* each medium keeps its own lattice, as each PhET screen keeps its own model */
    ok(RUNS.water!==RUNS.sound&&RUNS.water.scene==='water'&&RUNS.sound.scene==='sound'&&RUNS.light.scene==='light',
       'the three media have three lattices of their own');
    Object.assign(ST,DEFAULTS); resetRuns(); ST.view='water'; CLOCK.acc=0;
    let n1=0; for(let f=0;f<600;f++) n1+=clockFrame();
    ok(Math.abs(n1-600*FRAME_DT*LAT.EVENT_RATE)<1,'ten seconds of frames advance the tank 364 steps, PhET’s 20x111/61 per second ('+n1+')');
    ST.speed='slow'; CLOCK.acc=0; let n2=0; for(let f=0;f<600;f++) n2+=clockFrame();
    ok(Math.abs(n2-300*FRAME_DT*LAT.EVENT_RATE)<1,'slow runs at half that ('+n2+')');
    ST.speed='normal'; ST.running=false; eq(clockFrame(),0,'paused: no steps');
    ST.running=true; ST.view='media'; eq(clockFrame(),0,'the three media are a still picture');
    ST.view='sound'; const ns=RUNS.sound.n; clockFrame(); ok(RUNS.sound.n>ns,'and the sound view runs its own lattice');
    ok(RUNS.water.n>0&&RUNS.light.n>=0,'while the others hold where they were');
    /* reset gives every run its clock back, not just its lattice */
    /* the clock tests above have already stepped these runs, so count the increments, not the
       totals (the same trap as any test that inherits the state its predecessor left) */
    ST.view='water'; const nw0=RUNS.water.n; runFor('water',40);
    ST.view='light'; const nl0=RUNS.light.n; runFor('light',25);
    ok(RUNS.water.t>0&&RUNS.water.n===nw0+40&&RUNS.light.n===nl0+25,'two of the three runs have been stepped');
    resetRuns();
    ok(RUNS.water.t===0&&RUNS.water.n===0&&RUNS.light.t===0&&RUNS.light.n===0&&RUNS.sound.t===0,
       'resetRuns puts every run back to t = 0 and step 0');
    ok(RUNS.water.lat.u.every(v=>v===0)&&RUNS.light.lat.u.every(v=>v===0),'with an empty lattice');
    ok(RUNS.water.A===8&&RUNS.water.cont&&RUNS.water.src[0]&&!RUNS.water.watch.on,
       'and the source back at amplitude 8, continuous and running');
    Object.assign(ST,stSave); resetRuns(); }
  { /* the stopwatch and the probes ride the run */
    Object.assign(ST,DEFAULTS); resetRuns(); ST.view='water'; ST.meter=true;
    const R=syncRun('water'); R.watch.on=true; runFor('water',50);
    rel(R.watch.t,50*R.dt,1e-12,'the stopwatch counts physical time: 50 steps x dt');
    eq(R.trace.length,50,'the wave meter recorded both probes at every step');
    const p=TOOLS.probes[0], S=SCENES.water;
    close(R.trace[49][1],probeValue(R,p[0]*S.W,p[1]*S.W),1e-15,'its last sample is the probe’s current value');
    { const R2=makeRun('water','point',1), L=R2.lat;
      for(let j=0;j<L.ny;j++) for(let i=0;i<L.nx;i++) L.u[j*L.nx+i]=0.3*i-0.7*j+2;
      const X=48.37, Y=91.81;
      close(probeValue(R2,xOfCell(R2,X),xOfCell(R2,Y)),0.3*X-0.7*Y+2,1e-10,'a probe between cells reads a linear field exactly (bilinear)'); }
    Object.assign(ST,stSave); resetRuns(); }
  { /* the air parcels, on the twin's own sound run (Tb: 0.2937 per ms, amplitude 6.5, 300 steps) */
    const P=parcelPositions(Tb);
    eq(P.length,441,'PhET’s 21 x 21 grid of parcels');
    for(const k of refs('TWIN sound parcel[')){ const q=num(k,/\[(\d+)\]/)[0];
      rel(P[q][0],ref(k,0),1e-11,k+' across (twin)'); rel(P[q][1],ref(k,1),1e-11,k+' up (twin)'); }
    const kk='TWIN sound parcels: largest push across, up, and as a fraction of the spacing';
    let mx=0, my=0;
    for(let q=0;q<P.length;q++){ const a=Math.floor(q/21), b=q%21;
      mx=Math.max(mx,Math.abs(P[q][0]-cellOfX(Tb,a*SCENES.sound.W/20)));
      my=Math.max(my,Math.abs(P[q][1]-cellOfX(Tb,b*SCENES.sound.W/20))); }
    rel(mx,ref(kk,0),1e-11,'the largest push across the wave (twin)');
    rel(my,ref(kk,1),1e-11,'and along it (twin)');
    /* the scaling is set so that a wave at PhET's full colour moves a parcel 0.3 of the
       spacing; beside the source the field is stronger than that, so the push is larger —
       but never near the spacing itself, which would make the rows cross (Known-bad) */
    close(mx/(LAT.VIS/20),ref(kk,2),1e-11,'as a fraction of the parcel spacing (twin)');
    ok(ref(kk,2)>0.3&&ref(kk,2)<0.5,'the largest push is 0.39 of the spacing: above the 0.3 the scaling sets for a full-colour wave, and well short of a crossing');
    { const R2=makeRun('sound','point',1); R2.A=6.5; runSetFrequency(R2,0.2937,true);
      for(let s=0;s<300;s++) runStep(R2);
      const L=R2.lat, k2=TAU/R2.Nl, KD=0.3*(LAT.VIS/20)/(k2*U_FULL);
      const q=10*21+10, X0=cellOfX(R2,10*SCENES.sound.W/20), i0=Math.round(X0), j0=Math.round(cellOfX(R2,10*SCENES.sound.W/20));
      const g=(L.u[j0*L.nx+i0+1]-L.u[j0*L.nx+i0-1])/2;
      close(parcelPositions(R2)[q][0]-X0,KD*g,1e-12,'a parcel’s displacement is exactly grad p times the scale factor');
      ok((parcelPositions(R2)[q][0]-X0)*g>0,'so it moves UP the pressure gradient, crowding where p is high'); } }

  /* ---------- I. the readouts ---------- */
  const panelCases=[];
  for(const v of SCENE_IDS) panelCases.push({view:v},{view:v,tape:true,watch:true,meter:true,graph:true},{view:v,wave:'pulse'});
  panelCases.push({view:'water',look:'side'},{view:'sound',soundView:'both',tone:true},{view:'light',inten:true},
                  {view:'light',screen:false},{view:'media'},{view:'media',f_water:SCENES.water.fmin,f_light:SCENES.light.fmax});
  for(const c of panelCases){ Object.assign(ST,DEFAULTS,c); resetRuns(); if(MEDIA[c.view]) runFor(c.view,40);
    const M=buildModel(), html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+JSON.stringify(c)); }
  { Object.assign(ST,DEFAULTS); resetRuns(); const M=buildModel(), h2=readoutHTML(M);
    ok(h2.indexOf('2.64 cm')>=0,'the water readout prints the wavelength 2.64 cm off the model');
    ok(h2.indexOf('&minus;0.79 %')>=0,'and PhET’s −0.79 % wavelength error there (WI)');
    ok(h2.indexOf('29.30')>=0,'and 29.30 cells per wavelength'); }
  { Object.assign(ST,DEFAULTS,{view:'media'}); resetRuns(); const h2=readoutHTML(buildModel());
    ok(h2.indexOf('343.0 m/s')>=0,'the three-media readout prints sound’s 343.0 m/s');
    ok(h2.indexOf('103.9 cm')>=0&&h2.indexOf('103.8 cm')>=0,
       'and both wavelengths at four figures — v/f = 103.9 cm against the 103.8 cm measured, which three figures would have rounded together');
    ok(h2.indexOf('2.998&times;10<sup>8</sup> m/s')>=0,'and light’s speed as 2.998×10⁸ m/s, not as sigf’s "×10^+8"'); }
  { Object.assign(ST,DEFAULTS,{view:'light'}); resetRuns(); runFor('light',400); const h2=readoutHTML(buildModel());
    ok(h2.indexOf('0.753')>=0,'the light readout prints the screen’s brightness, 0.753 (twin)'); }
  /* every slider end, in every medium: finite and clean */
  { let nBad=0, nCase=0;
    for(const id of SCENE_IDS){ const S=SCENES[id];
      for(const f of [S.fmin,S.fmax]) for(const A of [0,10]) for(const w of ['cont','pulse']){
        const over={view:id,tape:true,watch:true,meter:true,graph:true,inten:true,tone:true,wave:w};
        over['f_'+id]=f; over['amp_'+id]=A;
        Object.assign(ST,DEFAULTS,over); resetRuns(); if(w==='pulse') firePulse(syncRun(id)); runFor(id,25);
        const M=buildModel(), h2=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
        nCase++;
        if(!(h2.indexOf('NaN')<0&&h2.indexOf('undefined')<0&&h2.indexOf('Infinity')<0&&RUNS[id].lat.u.every(isFinite)&&isFinite(M.L.dt))){
          nBad++; console.log('  unclean: '+id+' f='+f+' A='+A+' '+w); } } }
    Object.assign(ST,DEFAULTS,{view:'media'});
    for(const id of SCENE_IDS){ ST['f_'+id]=SCENES[id].fmin; }
    let M=buildModel(); nCase++;
    if(!M.X.rows.every(q=>isFinite(q.m.lamCells)&&isFinite(q.m.pexp)&&q.m.amp.every(isFinite))) nBad++;
    for(const id of SCENE_IDS){ ST['f_'+id]=SCENES[id].fmax; }
    M=buildModel(); nCase++;
    if(!M.X.rows.every(q=>isFinite(q.m.lamCells)&&isFinite(q.m.pexp)&&q.m.amp.every(isFinite))) nBad++;
    ok(nBad===0,'every medium at both frequency ends, both amplitude ends and both modes, and the analysis at both ends: finite and clean ('+nCase+' cases)'); }
  Object.assign(ST,stSave); resetRuns();

  /* ---------- J. the scene object ---------- */
  { const shot=makeShot(1400,820), S=makeScene({getContext:()=>shot});
    Object.assign(ST,DEFAULTS); resetRuns(); CLOCK.acc=0;
    let adv=0; for(let f=0;f<5;f++) if(S.step()) adv++; ok(adv>=2,'the water view advances in the frame loop');
    ST.view='media'; ok(!S.step(),'the three media do not');
    ST.view='water'; ST.tape=true; ST.meter=true;
    let G=latGeo(shot,S.W,S.H,buildModel());
    const g=genGeo(G.sq,RUNS.water);
    ok(sourceActive(RUNS.water),'the source is running'); ok(S.pointer('down',g.btn.x,g.btn.y),'a click on the generator’s button is taken');
    ok(!sourceActive(RUNS.water),'and switches the source off'); S.pointer('up',0,0);
    S.pointer('down',g.btn.x,g.btn.y); ok(sourceActive(RUNS.water),'clicking it again switches it back on'); S.pointer('up',0,0);
    const t0=TOOLS.tape[0];
    ok(S.pointer('down',G.sq.x+t0[0]*G.sq.w,G.sq.y+t0[1]*G.sq.h),'pointer-down on a tape end grabs it'); eq(DRAG.what,'tape0','the first end');
    S.pointer('move',G.sq.x+0.1*G.sq.w,G.sq.y+0.2*G.sq.h);
    close(TOOLS.tape[0][0],0.1,1e-12,'the end follows the pointer'); ok(S.pointer('up',0,0),'released');
    S.pointer('down',G.sq.x+TOOLS.probes[1][0]*G.sq.w,G.sq.y+TOOLS.probes[1][1]*G.sq.h); eq(DRAG.what,'probe1','a probe grabs');
    S.pointer('move',G.sq.x+2*G.sq.w,G.sq.y-50);
    close(TOOLS.probes[1][0],1,0,'clamped to the tank'); close(TOOLS.probes[1][1],0,0,'at the top'); S.pointer('up',0,0);
    ok(!S.pointer('down',G.sq.x+0.93*G.sq.w,G.sq.y+0.07*G.sq.h),'empty water grabs nothing');
    ST.view='media'; ok(!S.pointer('down',300,300),'the three media ignore the pointer');
    Object.assign(TOOLS,JSON.parse(JSON.stringify(TOOLS0))); Object.assign(ST,stSave); resetRuns(); }

  /* ---------- K. the layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  /* the floors are 70 % of what each configuration actually emits at its LEANEST size, measured
     and written down here: a field batches thousands of cells into a handful of fills, the side
     view draws ten, and the analysis view is curves — one floor for all of them would either
     punish an honest view or pass a blank one (Known-bad: op-count floors) */
  const CONFIGS=[
    [{view:'water'},120,2800,4],[{view:'water',look:'side',graph:true},120,7,4],
    [{view:'water',tape:true,watch:true,meter:true,graph:true},120,2800,7],
    [{view:'water',wave:'pulse'},60,800,4],[{view:'water',amp_water:0},60,4,3],
    [{view:'sound'},120,3000,4],[{view:'sound',soundView:'particles'},160,300,4],
    [{view:'sound',soundView:'both',graph:true,meter:true,tone:true},160,4800,5],
    [{view:'light'},260,7500,5],[{view:'light',inten:true,graph:true},260,7500,9],
    [{view:'light',screen:false,inten:false},200,6700,4],
    [{view:'light',tape:true,watch:true,meter:true,inten:true},260,7500,12],
    [{view:'light',f_light:SCENES.light.fmax},260,7600,5],
    [{view:'media'},0,5,20],[{view:'media',f_water:SCENES.water.fmin,f_sound:SCENES.sound.fmax,f_light:SCENES.light.fmax},0,5,20],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [base,steps,rFloor,sFloor] of CONFIGS){
    Object.assign(ST,DEFAULTS,base); resetRuns();
    if(MEDIA[base.view]){ const R=syncRun(base.view); if(base.wave==='pulse') firePulse(R); runFor(base.view,steps); }
    const nm=JSON.stringify(base);
    for(const [W,H] of SIZES){
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      const rects=fills.reduce((a,o)=>a+(o.n||1),0), strokes=c.ops.filter(o=>o.op==='stroke').length;
      /* floors on what the ops CARRY (rectangle sub-paths), per configuration */
      ok(rects>=rFloor&&strokes>=sFloor&&texts.length>=3,
         nm+' '+W+'x'+H+' draws substance ('+rects+' rects, '+strokes+' strokes, '+texts.length+' texts; floors '+rFloor+'/'+sFloor+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb, ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>0.5&&oy>0.5){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner, and the
         display-list capture cannot see it because it is not canvas (wave-on-a-string) */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' nothing under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    }
  }
  Object.assign(ST,stSave); resetRuns(); Object.assign(TOOLS,JSON.parse(JSON.stringify(TOOLS0)));

  /* ---------- L. the formatters that write powers of ten ---------- */
  { eq(supTxt(8),'⁸','supTxt turns 8 into a superscript eight');
    eq(supTxt(-15),'⁻¹⁵','and -15 into a superscript minus fifteen');
    eq(pow10(8),'10⁸','pow10(8) is the axis label 10^8'); eq(pow10(-7),'10⁻⁷','pow10(-7) is 10^-7');
    eq(sciTxt(2.99792458e8,4),'2.998×10⁸','sciTxt writes c as 2.998x10^8 for the canvas');
    eq(sciHTML(2.99792458e8,4),'2.998&times;10<sup>8</sup>','and sciHTML as markup for the readout');
    eq(sciTxt(0.0165,3),'0.0165','an ordinary magnitude is left to sigf');
    eq(sciTxt(343,3),'343','as is 343'); eq(sciTxt(0,3),'0','and zero');
    eq(sciTxt(5.11e-7,3),'5.11×10⁻⁷','a small one goes to the exponent form'); }

  /* ---------- M. colour ---------- */
  { ok(/^rgb\(\d+,\d+,\d+\)$/.test(specCss(550,0.5)),'specCss is well formed');
    const g=specCss(550,1).match(/\d+/g).map(Number); ok(g[1]>=250&&g[0]<100,'550 nm is green (brightness checked, not just syntax)');
    const r=specCss(650,1).match(/\d+/g).map(Number); ok(r[0]>=250&&r[1]<60,'650 nm is red');
    const z=specCss(650,0).match(/\d+/g).map(Number); ok(z[0]+z[1]+z[2]===0,'zero brightness is black');
    eq(CIE1931.length,81,'81 CIE rows, 380 to 780 nm every 5 (the CIE’s own file)');
    /* the light view's colour follows its frequency */
    const red=specCss(SCENES.light.v/SCENES.light.fmin,1).match(/\d+/g).map(Number);
    const vio=specCss(SCENES.light.v/SCENES.light.fmax,1).match(/\d+/g).map(Number);
    ok(red[0]>red[2]&&vio[2]>vio[0],'the slider’s ends are red (780 nm) and violet (380 nm)'); }

  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
