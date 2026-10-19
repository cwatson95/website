
/* ================================================================== *
 *  selfTest — headless verification.  Every reference is a line of    *
 *  build/wave-interference/refvals.txt (derive.py's output, read in   *
 *  full), carried here in REF under its printed label: (twin) = the   *
 *  numpy repeat of the engine, (scipy)/(python) = computed outside.   *
 * ================================================================== */
const TEST_APS={ellipse_default:['ellipse',DIF.LAM0,{ellD:0.1,ellE:0}], ellipse_e08_650:['ellipse',650,{ellD:0.2,ellE:0.8}],
  rect_450:['rect',450,{recW:0.1,recH:0.2}], cs_default:['cs',DIF.LAM0,{csD:0.05,csW:0.05}],
  disorder_L2:['disorder',DIF.LAM0,{disD:0.05,disP:0.1,disL:2}], figure_600:['figure',600,{figH:0.2,figR:30}],
  gauss_default:['gauss',DIF.LAM0,{gauSx:0.03,gauSy:0.02}], slits_2:['slits',DIF.LAM0,{sltN:2,sltW:0.03,sltD:0.1}]};
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

  /* ---------- A. PhET's constants and the calibration (python) ---------- */
  rel(LAT.EVENT_RATE,ref('EVENT_RATE'),1e-15,'PhET event rate 20*111/61 (python)');
  rel(MUR1,ref('MUR1 MUR2A MUR2B',0),1e-15,'Mur 1st-order coefficient -1/3'); rel(MUR2A,ref('MUR1 MUR2A MUR2B',1),1e-15,'Mur 2/(C+1)'); rel(MUR2B,ref('MUR1 MUR2A MUR2B',2),1e-15,'Mur C^2/2(C+1)');
  eq(LAT.VIS,LAT.N-2*LAT.PAD,'111 visible cells = 151 - 2 x 20');
  let nCal=0;
  for(const id of SCENE_IDS){ const S=SCENES[id];
    rel(sceneDx(S),ref(id+' dx f0 lambda0',0),1e-15,id+' dx (python)'); rel(sceneF0(S),ref(id+' dx f0 lambda0',1),1e-15,id+' default f, mid-range (python)');
    rel(waveLen(S,sceneF0(S)),ref(id+' dx f0 lambda0',2),1e-14,id+' default wavelength (python)');
    for(const tag of ['fmin','f0','fmax']){ const k='  '+id+' '+tag+' f Nl Om dt period_steps', f=ref(k,0);
      rel(cellsPerWave(S,f),ref(k,1),1e-14,id+' '+tag+' cells per wavelength (python)'); rel(omegaStep(cellsPerWave(S,f)),ref(k,2),1e-14,id+' '+tag+' radians per step (python)');
      rel(stepDt(S,f),ref(k,3),1e-14,id+' '+tag+' time per step (python)'); rel(TAU/omegaStep(cellsPerWave(S,f)),ref(k,4),1e-14,id+' '+tag+' steps per period (python)');
      const kp='  '+id+' '+tag+' PhET lambda, PhET/true - 1';
      rel(phetLambda(S,f),ref(kp,0),1e-12,id+' '+tag+': PhET’s fixed step gives this wavelength (python)'); close(phetLambda(S,f)/waveLen(S,f)-1,ref(kp,1),1e-12,id+' '+tag+' PhET’s wavelength error'); nCal++; } }
  eq(nCal,9,'all nine calibration points checked');
  rel(SCENES.light.v/sceneF0(SCENES.light),DIF.LAM0,1e-14,'the light scene’s default wavelength IS the diffraction screen’s lambda0 = 511.034 nm');
  /* the calibration's claim, directly: sin(Om/2) = C sin(pi/Nl) is the axial dispersion relation */
  for(const id of SCENE_IDS){ const S=SCENES[id], f=0.37*S.fmin+0.63*S.fmax, Nl=cellsPerWave(S,f);
    close(latOmega(TAU/Nl,0),omegaStep(Nl),1e-15,id+': the solved step lies on the dispersion relation');
    rel(latK(omegaStep(Nl),0)*Nl,TAU,1e-12,id+': and inverts to exactly Nl cells per wavelength'); }

  /* ---------- B. the dispersion relation (python) ---------- */
  for(const k of refs('latOmega ')){ const a=num(k,/^latOmega (\S+) (\S+)$/); rel(latOmega(a[0],a[1]),ref(k),1e-14,k+' (python)'); }
  close(latOmega(PI,PI),PI/2,1e-15,'the highest frequency 2 asin(C sqrt 2) = pi/2 at C = 1/2, inside stability (2C^2 = 1/2 <= 1)');
  for(const k of refs('latK ')){ const a=num(k,/^latK Om=(\S+) th=(\S+)$/), th=a[1]*DEG, kk=latK(a[0],th);
    rel(kk,ref(k),1e-12,k+' (python brentq)'); close(latOmega(kk*Math.cos(th),kk*Math.sin(th)),a[0],1e-14,k+': round trip');
    const want=REF[Object.keys(REF).find(q=>q.indexOf('  speeds Om='+(k.split(' ')[1].slice(3))+' th='+a[1]+':')===0)];
    rel(latPhaseSpeed(kk,th),want[0],1e-12,'phase speed at '+k+' (python)'); rel(latGroupSpeed(kk,th),want[1],1e-12,'|grad Om| at '+k+' (python)');
    /* implemented twice: the closed-form group speed against a numerical derivative along k, where v_g is parallel to k */
    if(a[1]===0||a[1]===45){ const hh=1e-6, nd=(latOmega((kk+hh)*Math.cos(th),(kk+hh)*Math.sin(th))-latOmega((kk-hh)*Math.cos(th),(kk-hh)*Math.sin(th)))/(2*hh);
      rel(latGroupSpeed(kk,th),nd,1e-8,'closed-form group speed = dOm/dk numerically at '+k); }
    else ok(latGroupSpeed(kk,th)>want[2]*(1+1e-6),'at '+a[1]+'° the group velocity is NOT parallel to k: |grad Om| exceeds its component along k (python)'); }
  for(const k of refs('speeds Nl=')){ const a=num(k,/^speeds Nl=(\S+) th=(\S+) vp\/C vg\/C$/), th=a[1]*DEG;
    const kk=TAU/a[0];                          /* the label's Nl is the wavelength along th, in cells */
    rel(latPhaseSpeed(kk,th)/LAT.C,ref(k,0),1e-13,k+' phase (python)'); rel(latGroupSpeed(kk,th)/LAT.C,ref(k,1),1e-13,k+' group (python)'); }
  for(const k of refs('diagonal wavelength / axial at Nl=')){ const Nl=num(k,/Nl=(\S+)$/)[0];
    rel((TAU/latK(omegaStep(Nl),PI/4))/Nl,ref(k),1e-12,k+' (python brentq)'); }
  ok(latPhaseSpeed(TAU/8.436,0)<latPhaseSpeed(TAU/8.436,PI/4)&&latPhaseSpeed(TAU/8.436,PI/4)<LAT.C,'short waves lag, least along the diagonal');
  ok(isNaN(latK(PI/2,0)),'no axial wave carries Om = pi/2 (the axial branch tops out at pi/3): latK says so rather than inventing one');

  /* ---------- C. Mur's boundary (python) ---------- */
  for(const k of refs('murR ')){ const a=num(k,/^murR Nl=(\S+) th=(\S+) order1 order2$/), kk=TAU/a[0], th=a[1]*DEG;
    rel(murReflection(kk*Math.cos(th),kk*Math.sin(th),1),ref(k,0),1e-9,k+' first order (python)');
    rel(murReflection(kk*Math.cos(th),kk*Math.sin(th),2),ref(k,1),1e-9,k+' second order (python)'); }
  { const kk=TAU/2000, th=40*DEG, c1=(1-Math.cos(th))/(1+Math.cos(th));
    rel(murReflection(kk*Math.cos(th),kk*Math.sin(th),1),c1,1e-4,'long waves: Mur 1st order -> the continuum (1-cos)/(1+cos)');
    rel(murReflection(kk*Math.cos(th),kk*Math.sin(th),2),c1*c1,1e-3,'and 2nd order -> its square'); }

  /* ---------- D. the plane wave is an exact lattice solution ---------- */
  for(const thd of [0,45]){
    const Nl=11.345, Om=omegaStep(Nl), th=thd*DEG, k=thd===0?TAU/Nl:latK(Om,th), kx=k*Math.cos(th), ky=k*Math.sin(th), n=61, L=makeLattice(n,n,20);
    for(let j=0;j<n;j++) for(let i=0;i<n;i++){ L.u[j*n+i]=Math.sin(kx*i+ky*j); L.up[j*n+i]=Math.sin(kx*i+ky*j+Om); }
    for(let s=0;s<20;s++) latStep(L);
    let err=0; for(let j=21;j<40;j++) for(let i=21;i<40;i++) err=Math.max(err,Math.abs(L.u[j*n+i]-Math.sin(kx*i+ky*j-20*Om)));
    ok(err<1e-12,'an analytic plane wave at '+thd+'° stays exact on the lattice for 20 steps ('+err.toExponential(2)+'; python '+ref('plane wave th='+thd+', 20 steps, max interior error').toExponential(2)+')'); }

  /* ---------- E. the twin: the engine against numpy, operation for operation ---------- */
  function twinCheck(tag,R){
    const L=R.lat;
    for(const k of refs('TWIN '+tag+' u(')){ const a=num(k,/u\((\d+),(\d+)\)$/); close(L.u[a[1]*L.nx+a[0]],ref(k),1e-11+1e-11*Math.abs(ref(k)),k+' (twin)'); }
    let mx=0, s2=0, nv=0;
    for(let j=L.pad;j<L.pad+LAT.VIS;j++) for(let i=L.pad;i<L.pad+LAT.VIS;i++){ const v=L.u[j*L.nx+i]; mx=Math.max(mx,Math.abs(v)); s2+=v*v; }
    for(let q=0;q<L.vis.length;q++) nv+=L.vis[q];
    const km='TWIN '+tag+' max|u| visible, sum u^2 visible, visited cells', kt='TWIN '+tag+' t n phi';
    rel(mx,ref(km,0),1e-11,tag+' max |u| (twin)'); rel(s2,ref(km,1),1e-11,tag+' sum of u^2 (twin)'); eq(nv,ref(km,2),tag+' cells the wave has visited (twin)');
    rel(R.t,ref(kt,0),1e-13,tag+' physical time (twin)'); eq(R.n,ref(kt,1),tag+' steps'); rel(R.phi,ref(kt,2),1e-13,tag+' phase (twin)');
  }
  const Ta=makeRun('water','point',1); for(let s=0;s<240;s++) runStep(Ta); twinCheck('tank',Ta);
  const Tb=makeRun('sound','point',2); Tb.A=10; for(let s=0;s<240;s++) runStep(Tb); twinCheck('two',Tb);
  eq(runSourceRows(Tb).join(','),ref('TWIN two source rows',0)+','+ref('TWIN two source rows',1),'the two sound sources sit on rows 53 and 97 (twin)');
  { const k='source rows at the water and light defaults';
    eq(runSourceRows(makeRun('water','point',2)).join(','),ref(k,0)+','+ref(k,1),'water’s 3 cm is 16.65 cells: rows 58 and 92, rounded as PhET does (twin)');
    eq(runSourceRows(makeRun('light','point',2)).join(','),ref(k,2)+','+ref(k,3),'light’s 1500 nm likewise (twin)'); }
  const Tc=makeRun('light','plane',1); Tc.A=10; Tc.plane.barrier='two'; for(let s=0;s<400;s++) runStep(Tc); twinCheck('slits',Tc);
  { const open=[]; for(let j=0;j<Tc.lat.ny;j++) if(slitOpen(Tc,j)) open.push(j);
    const k='TWIN slits open rows: count first last'; eq(open.length,ref(k,0),'open rows (twin)'); eq(open[0],ref(k,1),'first open row'); eq(open[open.length-1],ref(k,2),'last open row');
    eq(screenWindow(Tc),ref('TWIN slits screen window'),'the screen averages over 92 steps = 4 whole periods of 22.9 (twin)');
    const I=screenIntensity(Tc);
    for(const r of [55,45,65,30,80,10]) rel(I[r],ref('TWIN slits screen I['+r+']'),1e-10,'screen intensity row '+r+' (twin)');
    let am=0; for(let r=0;r<I.length;r++) if(I[r]>I[am]) am=r; eq(am,ref('TWIN slits screen argmax, max',0),'the brightest row is the centre (twin)');
    close(I[45],I[65],1e-12*I[55],'and the pattern is symmetric'); }
  const Td=makeRun('water'); Td.cont=false; ok(firePulse(Td),'a pulse fires in pulse mode'); for(let s=0;s<150;s++) runStep(Td); twinCheck('pulse',Td);
  eq(Td.pulse.on?0:1,ref('TWIN pulse finished'),'the pulse ends after one period (twin)');
  const Te=makeRun('sound','plane',1); Te.A=10; Te.plane.barrier='one'; Te.plane.bcol=60; for(let s=0;s<300;s++) runStep(Te);
  for(const k of refs('TWIN oneslit u(')){ const a=num(k,/u\((\d+),(\d+)\)$/); close(Te.lat.u[a[1]*Te.lat.nx+a[0]],ref(k),1e-11+1e-11*Math.abs(ref(k)),k+' (twin)'); }
  { const open=[]; for(let j=0;j<Te.lat.ny;j++) if(slitOpen(Te,j)) open.push(j); const k='TWIN oneslit open rows: count first last';
    eq(open.length,ref(k,0),'one sound slit: 19 open rows (twin)'); eq(open[0],ref(k,1),'first'); eq(open[open.length-1],ref(k,2),'last'); }
  ok(!firePulse(Ta),'a continuous source refuses a pulse');

  /* ---------- F. two sources: the path difference (python) ---------- */
  for(const k of refs('nodalCount ')){ const x=num(k,/=(\S+)$/)[0]; eq(nodalCount(x),ref(k),k+' (python)'); }
  for(const k of refs('hyperY farY ')){ const a=num(k,/d=(\S+) Delta=(\S+) L=(\S+) /), y=hyperY(a[0],a[1],a[2]);
    rel(y,ref(k,0),1e-13,k+' exact (python)'); rel(farY(a[0],a[1],a[2]),ref(k,1),1e-13,k+' far field (python)');
    close(Math.hypot(a[2],y+a[0]/2)-Math.hypot(a[2],y-a[0]/2),a[1],1e-12,k+': the point on the screen really has r1 - r2 = Delta'); }
  { const a=hyperY(3.2,0.5,1000)-farY(3.2,0.5,1000), A=0.25, B=Math.sqrt(3.2*3.2/4-A*A);
    rel(a,A*B/(2*1000),1e-3,'far away the exact minimum sits ab/2L outside the far-field one'); }
  { const k='nodal lines vs the hyperbolae: crossings matched, lattice worst distance (cells), continuum 1/sqrt(r) worst, lattice mean outward shift';
    ok(ref(k,0)===10&&ref(k,1)<1.5&&ref(k,2)<0.1&&ref(k,3)>0.5,'python twin: the lattice’s nodal lines sit within 1.5 cells of the hyperbolae, all outward (the anisotropy), where the continuum 1/√r formula sits within 0.1'); }
  { const x=7, y=1.1, d=3.2, kk=TAU, r1=Math.hypot(x,y+d/2), r2=Math.hypot(x,y-d/2);
    close(fringeFactor(x,y,d,kk),1+2*Math.cos(kk*(r1-r2))*Math.sqrt(r1*r2)/(r1+r2),1e-14,'the interference factor is 1 + 2 cos k(r1-r2) sqrt(r1 r2)/(r1+r2)');
    const yh=hyperY(d,0.5,x); ok(fringeFactor(x,yh,d,kk)<0.01,'and nearly vanishes on the first nodal hyperbola'); }
  for(const k of refs('twoSourceI twoSourceFar ')){ const a=num(k,/x=(\S+) y=(\S+) d=(\S+) lam=(\S+)$/), kk=TAU/a[3];
    rel(twoSourceI(a[0],a[1],a[2],kk),ref(k,0),1e-12,k+' (python)'); close(twoSourceFar(a[0],a[1],a[2],kk),ref(k,1),1e-12,k+' far (python)'); }

  /* ---------- G. the slits' theory curves (python) ---------- */
  { const g=slitCells(Tc); eq(g.a,ref('slits effective a (cells) d (cells)',0),'each light slit is 11 cells (python)'); close(g.d,ref('slits effective a (cells) d (cells)',1),1e-12,'34 cells apart (python)');
    const th=screenTheory(Tc);
    for(const r of [55,45,65,30,80,10]){ rel(th.exact[r],ref('theory exact far ['+r+']',0),1e-10,'Rayleigh–Sommerfeld at row '+r+' (python)');
      rel(th.far[r],ref('theory exact far ['+r+']',1),1e-10,'Fraunhofer at row '+r+' (python)'); }
    const fm=a=>{ for(let r=56;r<a.length-1;r++) if(a[r]<a[r-1]&&a[r]<=a[r+1]) return r-55; return -1; };
    eq(fm(th.exact),ref('first minimum (rows above centre): lattice RS Fraunhofer',1),'the first minimum is 10 rows out in the Rayleigh–Sommerfeld sum (python)');
    eq(fm(th.far),ref('first minimum (rows above centre): lattice RS Fraunhofer',2),'and 9 in the Fraunhofer formula (python)');
    ok(ref('lattice screen vs Rayleigh-Sommerfeld, vs Fraunhofer after 1400 steps: max |diff|, rms',0)<0.07&&ref('lattice screen vs Rayleigh-Sommerfeld, vs Fraunhofer after 1400 steps: max |diff|, rms',2)>0.2,
       'python: at steady state the lattice screen follows Rayleigh–Sommerfeld to 7 % and misses Fraunhofer by more than 20 % (the header’s claim)'); }

  /* ---------- H. the far field (scipy, numpy) ---------- */
  rel(DIF.LAM0,ref('LAM0 PX SIN_PER_BIN',0),1e-15,'lambda0 = harmonic mean of 380 and 780 nm (python)'); rel(DIF.PX,ref('LAM0 PX SIN_PER_BIN',1),1e-15,'pixel = 1/192 mm');
  rel(DIF.SIN_PER_BIN,ref('LAM0 PX SIN_PER_BIN',2),1e-14,'one FFT bin is sin(theta) = 3.8328e-4 at every wavelength (python)');
  for(const k of refs('J1(')){ const x=num(k,/^J1\((\S+)\)/)[0];
    close(besselJ1(x),ref(k,0),2e-10,k+' J1 (scipy)'); close(besselJ0(x),ref(k,1),2e-10,k+' J0 (scipy)'); }
  close(besselJ1(J11),0,1e-12,'J1 vanishes at j11 = 3.8317 (scipy jn_zeros)');
  close(besselJ1(J_SPLIT-1e-9),besselJ1(J_SPLIT+1e-9),5e-10,'J1 is continuous across its series/asymptotic join, to its stated 1e-10 class');
  for(const k of refs('airy(')){ const x=num(k,/^airy\((\S+)\)/)[0]; close(airyI(x),ref(k),2e-10,k); }
  for(const k of refs('sinc2(')){ const x=num(k,/^sinc2\((\S+)\)/)[0]; close(sinc2(x),ref(k),1e-15,k+' (python)'); }
  for(const b of [9e-5,5e-5]){ const s=Math.sin(b)/b; close(sinc2(b),s*s,1e-15,'sinc2 series branch at '+b+' = the direct form'); const t=2*besselJ1(b)/b; close(airyI(b),t*t,1e-15,'Airy series branch at '+b+' = the direct form'); }
  ok(Math.abs(sinc2(0.5e-4)-(1-0.25e-8/3))<1e-18,'sinc2 series carries -b^2/3');
  for(const k of refs('gratingFactor(')){ const a=num(k,/^gratingFactor\((\S+),(\d+)\)$/); close(gratingFactor(a[0],a[1]),ref(k),1e-13,k+' (python)'); }
  close(gratingFactor(PI+1e-6,3),1-8*Math.pow(Math.sin(PI+1e-6),2)/3,1e-15,'grating factor series branch at g = pi + 1e-6');
  rel(DISORDER_V[0][0],ref('disorder vector 0',0),1e-14,'disorder offsets: Park–Miller draw 0 (python)'); rel(DISORDER_V[15][1],ref('disorder vector 15',1),1e-14,'draw 15 (python)');
  for(const q of DISORDER_V) ok(Math.hypot(q[0],q[1])<=1,'every disorder offset is inside the unit disc');
  /* the renderer and the transform: three apertures through the FFT, five by direct DFT at the pinned bins */
  const BINS=[[0,0],[3,0],[0,5],[7,4],[-11,2],[20,-13]];
  for(const name in TEST_APS){
    const spec=TEST_APS[name], P=Object.assign({ap:spec[0]},spec[2]), rend=renderAperture(P,spec[1]);
    let sum=0; for(let q=0;q<rend.t.length;q++) sum+=rend.t[q];
    rel(sum,ref('AP '+name+' lam sum(t) max|F|',1),1e-12,name+': the open area in pixels (numpy twin)');
    if(name==='ellipse_default'||name==='rect_450'||name==='gauss_default'){
      const D=diffract(rend.t), n=DIF.N, h=n/2;
      rel(D.max,ref('AP '+name+' lam sum(t) max|F|',2),1e-12,name+' max |F| (numpy)'); rel(D.dc,sum,1e-12,name+': F(0,0) is the open area');
      for(const [k1,k2] of BINS){ const lab2='AP '+name+' |F|('+k1+','+k2+')'; close(D.mag[(k2+h)*n+(k1+h)],ref(lab2),1e-11*D.max,lab2+' FFT (numpy)'); }
      rel(phetDisplay(D.mag[h*n+h+3],D.max),ref('AP '+name+' PhET display at (3,0)'),1e-12,name+': PhET’s log display (python)');
      if(name==='ellipse_default'){
        for(const [k1,k2] of [[3,0],[7,4]]){ const d=dft2At(rend.t,n,k1,k2); rel(Math.hypot(d[0],d[1]),D.mag[(k2+h)*n+(k1+h)],1e-11,'FFT = direct DFT at ('+k1+','+k2+')');
          rel(Math.hypot(d[0],d[1]),ref('direct DFT |F|('+k1+','+k2+')'),1e-11,'direct DFT = numpy’s direct sum ('+k1+','+k2+')'); }
        let dev=0; for(let k=0;k<=10;k++){ const I=Math.pow(D.mag[h*n+h+k]/D.dc,2), a=airyI(PI*0.1*k*DIF.SIN_PER_BIN/(DIF.LAM0*1e-6)); dev=Math.max(dev,Math.abs(I-a)); }
        rel(dev,ref('AP ellipse default: max |FFT cut - Airy| for k <= 10 (intensity)'),1e-8,'the drawn disc is the Airy pattern to 1.2e-3 for k <= 10 (python)'); ok(dev<1.5e-3,'…which is small');
        let am=12; for(let k=12;k<=20;k++) if(D.mag[h*n+h+k]<D.mag[h*n+h+am]) am=k;
        eq(am,ref('AP ellipse default: argmin of the cut over 12..20, its value',0),'the first dark ring falls on bin 16 (python)');
        rel(J11/(PI*0.1/(DIF.LAM0*1e-6))/DIF.SIN_PER_BIN,ref('AP ellipse default: Airy first zero at bin'),1e-12,'the exact first zero is at bin 16.26 (python)'); }
      if(name==='rect_450'){ eq(rend.iw,ref('AP rect iw ih',0),'rectangle snapped to 2 x 11 pixels (python)'); eq(rend.ih,ref('AP rect iw ih',1),'and 2 x 22');
        { const r0=renderAperture({ap:'rect',recW:0.1,recH:0.2},DIF.LAM0), k0='AP rect at LAM0 (0.1 x 0.2 mm): iw ih';
          eq(r0.iw,ref(k0,0),'at lambda0 the 0.1 mm side is 2 x 10 px (python)'); eq(r0.ih,ref(k0,1),'and the 0.2 mm side 2 x 19 px: 19.2 rounds DOWN, as PhET’s roundSymmetric does (python)');
          /* transposed, so the width carries the 19.2 (the width and the height are snapped by separate expressions) */
          const r1=renderAperture({ap:'rect',recW:0.2,recH:0.1},DIF.LAM0);
          eq(r1.iw,ref(k0,1),'a 0.2 mm WIDTH snaps to 2 x 19 px as well (python)'); eq(r1.ih,ref(k0,0),'and its 0.1 mm height to 2 x 10'); }
        for(const k1 of [1,5,13,40,127]){ const kD='AP rect Dirichlet k='+k1+' |F|(k,0), 2ih*|D|';
          rel(D.mag[h*n+h+k1],2*rend.ih*Math.abs(dirichlet(k1,2*rend.iw,n)),1e-12,'the snapped rectangle IS the Dirichlet kernel at k = '+k1);
          rel(2*rend.ih*Math.abs(dirichlet(k1,2*rend.iw,n)),ref(kD,1),1e-12,kD+' (python)'); }
        ok(Math.abs(D.mag[h*n+h+40]/D.dc-Math.sqrt(sinc2(PI*40*22/256)))>1e-3,'and it is NOT the continuous sinc out at k = 40 (the kernel’s sin(pi k/N) denominator)'); }
      if(name==='gauss_default'){ const s=DIF.LAM0/spec[1], sx=s*0.03/DIF.PX, sy=s*0.02/DIF.PX;
        for(const k1 of [0,4,9,17]){ const a=TAU*sx*sy*Math.exp(-2*PI*PI*sx*sx*(k1/n)*(k1/n)); rel(D.mag[h*n+h+k1],a,1e-12,'the sampled Gaussian transforms to 2 pi sx sy exp(-2 pi^2 sx^2 f^2) at k = '+k1); } }
    } else {
      const n=DIF.N;
      for(const [k1,k2] of BINS){ const d=dft2At(rend.t,n,k1,k2), lab2='AP '+name+' |F|('+k1+','+k2+')';
        close(Math.hypot(d[0],d[1]),ref(lab2),1e-11*sum,lab2+' direct DFT (numpy)'); }
    }
  }
  { /* the 1-D FFT against the O(N^2) sum on an incommensurate test signal */
    const n=64, re=new Float64Array(n), im=new Float64Array(n);
    for(let q=0;q<n;q++){ re[q]=Math.cos(0.7317*q)+0.3*Math.sin(2.213*q*q/n); im[q]=0.1*q/n; }
    const r2=Float64Array.from(re), i2=Float64Array.from(im); fftInPlace(r2,i2);
    let err=0; for(let k=0;k<n;k++){ let sr=0,si=0; for(let q=0;q<n;q++){ const a=-TAU*k*q/n; sr+=re[q]*Math.cos(a)-im[q]*Math.sin(a); si+=re[q]*Math.sin(a)+im[q]*Math.cos(a); }
      err=Math.max(err,Math.hypot(r2[k]-sr,i2[k]-si)); }
    ok(err<1e-12,'the radix-2 FFT equals the direct DFT on a 64-point test signal ('+err.toExponential(2)+')'); }
  { /* the analytic cut functions against their definitions */
    const P={ap:'ellipse',ellD:0.1,ellE:0}; close(fraunhoferCut(P,DIF.LAM0,0.004,null),airyI(PI*0.1*0.004/(DIF.LAM0*1e-6)),1e-15,'ellipse cut = Airy');
    const Pr={ap:'rect',recW:0.1,recH:0.2}, rr=renderAperture(Pr,450);
    close(fraunhoferCut(Pr,450,0.003,rr),sinc2(PI*(2*rr.iw*DIF.PX/rr.s)*0.003/(450e-6)),1e-15,'rectangle cut = sinc^2 of the SNAPPED width');
    const Pg={ap:'gauss',gauSx:0.03,gauSy:0.02}; close(fraunhoferCut(Pg,600,0.002,null),Math.exp(-Math.pow(TAU*0.03*0.002/600e-6,2)),1e-15,'Gaussian cut');
    const Ps={ap:'slits',sltN:3,sltW:0.03,sltD:0.1}; close(fraunhoferCut(Ps,500,0.002,null),sinc2(PI*0.03*0.002/500e-6)*gratingFactor(PI*0.1*0.002/500e-6,3),1e-15,'slits cut');
    eq(fraunhoferCut({ap:'cs',csD:0.05,csW:0.05},500,0.002,null),null,'circle & square has no closed form');
    close(firstZero(P,DIF.LAM0,null),J11*DIF.LAM0*1e-6/(PI*0.1),1e-18,'the Airy ring at j11 lambda/(pi D)');
    close(firstZero({ap:'slits',sltN:1,sltW:0.03,sltD:0.1},500,null),500e-6/0.03,1e-18,'one slit: lambda/a'); close(firstZero(Ps,500,null),500e-6/0.3,1e-18,'three slits: lambda/(3d)');
    /* each first zero is where its own cut vanishes, and the cut is still up at 0.9 of it */
    for(const [Q,lam,rd] of [[P,DIF.LAM0,null],[Pr,450,rr],[Ps,500,null],[{ap:'slits',sltN:1,sltW:0.03,sltD:0.1},500,null]]){
      const z=firstZero(Q,lam,rd); ok(fraunhoferCut(Q,lam,z,rd)<1e-12&&fraunhoferCut(Q,lam,0.9*z,rd)>1e-3,Q.ap+(Q.sltN?' N='+Q.sltN:'')+': the cut vanishes at firstZero and not before'); } }
  { /* the far-field cache follows the chosen aperture's own parameters */
    Object.assign(ST,DEFAULTS,{view:'far'}); const a0=farModel().open; ST.ellE=0.9; const a1=farModel().open;
    ok(a1<0.5*a0,'eccentricity 0.9 re-renders a thinner ellipse ('+fmt(a0,1)+' -> '+fmt(a1,1)+' px)');
    ST.recW=0.3; ok(farModel().open===a1,'a hidden rectangle slider does not re-render the ellipse'); Object.assign(ST,stSave); }

  /* ---------- I. colour (python, the CIE table) ---------- */
  eq(CIE1931.length,ref('CIE rows written'),'81 CIE rows, 380..780 nm every 5 (the CIE file)');
  for(const k of refs('specLinear(')){ const nm=num(k,/^specLinear\((\S+)\)$/)[0], c=specLinear(nm);
    for(let q=0;q<3;q++) close(c[q],ref(k,q),1e-12,k+' channel '+q+' (python)'); }
  { const w=[0.95047,1,1.08883], r=SRGB_M.map(row=>row[0]*w[0]+row[1]*w[1]+row[2]*w[2]);
    for(const v of r) close(v,1,2e-4,'the sRGB matrix takes D65 white to (1,1,1)'); }
  ok(/^rgb\(\d+,\d+,\d+\)$/.test(specCss(550,0.5)),'specCss is well formed');
  { const g=specCss(550,1).match(/\d+/g).map(Number); ok(g[1]>=250&&g[0]<100,'550 nm is green (brightness checked, not just syntax)');
    const r=specCss(650,1).match(/\d+/g).map(Number); ok(r[0]>=250&&r[1]<60,'650 nm is red');
    const z=specCss(650,0).match(/\d+/g).map(Number); ok(z[0]+z[1]+z[2]===0,'zero intensity is black'); }

  /* ---------- J. the runs, the clock, the controls' effect on the engine ---------- */
  { Object.assign(ST,DEFAULTS); resetRuns();
    ST.view='tank'; runFor('tank',100); const R=RUNS.tank; const e1=R.lat.u.reduce((a,v)=>a+v*v,0); ok(e1>1,'the tank has waves after 100 steps');
    ST.f_water=0.8; syncRun('tank'); ok(R.lat.u.reduce((a,v)=>a+v*v,0)===e1,'a new water frequency keeps the waves (PhET)'); close(R.f,0.8,0,'and takes the frequency');
    ST.scene='light'; syncRun('tank'); ok(R.scene==='light'&&R.lat.u.every(v=>v===0),'a new medium clears the lattice'); ok(R.t===0&&R.n===0,'and restarts its clock (new units)');
    runFor('tank',30); ST.f_light=0.5; syncRun('tank'); ok(R.lat.u.every(v=>v===0),'a new light frequency clears (PhET)');
    ST.scene='light'; ST.view='slits'; ST.barrier='two'; runFor('slits',120); const Rs=RUNS.slits, m0=Rs.plane.m;
    const left=Rs.lat.u[75*Rs.lat.nx+40]; ok(left!==0,'the plane wave is on the left of the barrier');
    ST.bcol=90; syncRun('slits'); ok(Rs.plane.m===m0&&Rs.lat.u[75*Rs.lat.nx+40]===left,'moving the barrier keeps the plane wave’s progress (PhET clearRight)');
    let right=0; for(let j=0;j<Rs.lat.ny;j++) for(let i=90;i<Rs.lat.nx;i++) right+=Math.abs(Rs.lat.u[j*Rs.lat.nx+i]); ok(right===0,'and wipes everything from the new barrier rightward');
    ST.slitW_light=800; syncRun('slits'); ok(Rs.plane.m===0,'a new slit width clears and restarts the plane wave');
    /* two sources stay in phase */
    ST.view='two'; ST.scene='water'; const R2=syncRun('two'); runFor('two',10); ST.src1=false; syncRun('two'); ST.src1=true; syncRun('two');
    ok(R2.phi>0,'switching one source back on while the other runs keeps the phase'); ST.src1=false; ST.src2=false; syncRun('two'); ST.src2=true; syncRun('two');
    close(R2.phi,0,0,'switching a source on alone restarts the phase at zero');
    /* the clock: PhET's 20 x 111/61 steps per second of wall time */
    Object.assign(ST,DEFAULTS); resetRuns(); ST.view='tank'; CLOCK.acc=0; let n1=0; for(let f=0;f<600;f++) n1+=clockFrame();
    ok(Math.abs(n1-600*FRAME_DT*LAT.EVENT_RATE)<1,'ten seconds at normal speed take 364 steps ('+n1+')');
    ST.speed='slow'; CLOCK.acc=0; let n2=0; for(let f=0;f<600;f++) n2+=clockFrame(); ok(Math.abs(n2-300*FRAME_DT*LAT.EVENT_RATE)<1,'slow takes half ('+n2+')');
    ST.running=false; eq(clockFrame(),0,'paused: no steps'); ST.view='far'; ST.running=true; eq(clockFrame(),0,'the far field has no clock');
    Object.assign(ST,stSave); resetRuns(); }
  { /* the stopwatch and the probes ride the run */
    Object.assign(ST,DEFAULTS); resetRuns(); ST.view='tank'; ST.meter=true; const R=syncRun('tank'); R.watch.on=true; runFor('tank',50);
    rel(R.watch.t,50*R.dt,1e-12,'the stopwatch counts physical time: 50 steps x dt'); eq(R.trace.length,50,'the wave meter recorded 50 samples');
    const p=TOOLS.probes[0], S=SCENES.water; close(R.trace[49][1],probeValue(R,p[0]*S.W,p[1]*S.W),1e-15,'its last sample is the probe’s current value');
    { const L=R.lat, i=40, j=70, x=xOfCell(R,i), y=xOfCell(R,j); close(probeValue(R,x,y),L.u[j*L.nx+i],1e-12,'a probe on a cell centre reads that cell'); }
    { /* off the cell centres, on a linear field, bilinear interpolation is exact */
      const R2=makeRun('water','point',1), L=R2.lat; for(let j=0;j<L.ny;j++) for(let i=0;i<L.nx;i++) L.u[j*L.nx+i]=0.3*i-0.7*j+2;
      const X=48.37, Y=91.81; close(probeValue(R2,xOfCell(R2,X),xOfCell(R2,Y)),0.3*X-0.7*Y+2,1e-10,'a probe between cells reads the linear field exactly (bilinear)'); }
    Object.assign(ST,stSave); resetRuns(); }
  { /* the parcels: displacement along +grad p, largest push 0.3 of their spacing on a plane wave */
    const R=makeRun('sound','plane',1); R.plane.barrier='none'; R.A=10; for(let s=0;s<260;s++) runStep(R);
    const P=parcelPositions(R); let mx=0; for(let q=0;q<P.length;q++){ const a=Math.floor(q/21), b=q%21, X0=cellOfX(R,a*SCENES.sound.W/20); mx=Math.max(mx,Math.abs(P[q][0]-X0)); }
    ok(mx<=0.3*LAT.VIS/20*1.001&&mx>0.2*LAT.VIS/20,'parcels move at most 0.3 of their spacing, and visibly ('+fmt(mx,3)+' cells)');
    const q=10*21+10, X=P[q][0], i0=Math.round(cellOfX(R,10*SCENES.sound.W/20)), g=(R.lat.u[75*R.lat.nx+i0+1]-R.lat.u[75*R.lat.nx+i0-1])/2;
    ok((X-cellOfX(R,10*SCENES.sound.W/20))*g>0,'a parcel moves UP the pressure gradient (crowding where p is high)'); }

  /* ---------- K. the readouts ---------- */
  const panelCases=[];
  for(const v of ['tank','two','slits']) for(const sc of SCENE_IDS) panelCases.push({view:v,scene:sc,tape:true,watch:true,meter:true,graph:true});
  panelCases.push({view:'slits',scene:'light',barrier:'none'},{view:'slits',scene:'water',barrier:'one'},{view:'two',scene:'light',src2:false});
  for(const a of AP_LIST) panelCases.push({view:'far',ap:a.id});
  panelCases.push({view:'far',laser:false},{view:'path'},{view:'path',pd:0.4},{view:'lattice'},{view:'lattice',scene:'light'});
  for(const c of panelCases){ Object.assign(ST,DEFAULTS,c); resetRuns(); if(LATTICE_VIEWS[c.view]) runFor(c.view,40);
    const M=buildModel(), html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+JSON.stringify(c)); }
  { Object.assign(ST,DEFAULTS); resetRuns(); const M=buildModel(); ok(readoutHTML(M).indexOf('2.64 cm')>=0,'the tank readout prints the water wavelength 2.64 cm off the model');
    ok(readoutHTML(M).indexOf('&minus;0.79 %')>=0,'and PhET’s −0.79 % wavelength error there (python)'); }
  { Object.assign(ST,DEFAULTS,{view:'lattice'}); const h2=readoutHTML(buildModel()); ok(h2.indexOf('0.22, 0.37, 2.9, 11 %')>=0,'the lattice readout prints Mur-2 |R| 0.22, 0.37, 2.9, 11 % for water (python)'); }
  { Object.assign(ST,DEFAULTS,{view:'far'}); const h2=readoutHTML(buildModel()); ok(h2.indexOf('0.357&deg;')>=0,'the far-field readout prints the Airy ring at 0.357°'); }
  { Object.assign(ST,DEFAULTS,{view:'slits',scene:'light',barrier:'two'}); resetRuns(); const h2=readoutHTML(buildModel()); const want=sigf(34*sceneDx(SCENES.light),3)+' nm'; ok(want==='1532 nm'&&h2.indexOf(want)>=0,'the slits readout prints the lattice’s 34-cell separation, 1532 nm, not the 1500 asked for'); }
  /* every slider at its ends: the models stay finite and the panels clean */
  { let nBad=0, nCase=0; const chk=(c,what)=>{ nCase++; if(!c){ nBad++; console.log('  non-finite or unclean: '+what); } };
    for(const sc of SCENE_IDS){ const S=SCENES[sc];
      for(const f of [S.fmin,S.fmax]) for(const v of ['tank','two','slits']){
        const over={view:v,scene:sc,A:10,barrier:'two',tape:true,meter:true,watch:true,graph:true}; over['f_'+sc]=f;
        over['sep_'+sc]=f===S.fmin?S.sepMin:S.sepMax; over['slitW_'+sc]=f===S.fmin?S.slitWMax:S.slitWMin; over['slitD_'+sc]=f===S.fmin?S.slitDMin:S.slitDMax;
        over.bcol=f===S.fmin?BCOL_MIN:BCOL_MAX; Object.assign(ST,DEFAULTS,over); resetRuns(); runFor(v,12);
        const M=buildModel(), h2=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
        chk(h2.indexOf('NaN')<0&&h2.indexOf('undefined')<0&&h2.indexOf('Infinity')<0&&RUNS[v].lat.u.every(isFinite)&&isFinite(M.L.dt)&&isFinite(M.L.phetErr),v+' '+sc+' f='+f); } }
    for(const a of AP_LIST){ const keys=AP_KEYS[a.id];
      for(const lam of [DIF.LAMMIN,DIF.LAMMAX]) for(const end of [0,1]){
        Object.assign(ST,DEFAULTS,{view:'far',ap:a.id,lam});
        for(const k of keys){ const r=SLIDER_RANGE[k]; ST[k]=end?r[1]:r[0]; }
        const M=buildModel(), F=M.F, h2=readoutHTML(M);
        chk(isFinite(F.D.max)&&F.D.max>0&&F.cut.every(isFinite)&&h2.indexOf('NaN')<0&&h2.indexOf('undefined')<0,a.id+' at '+(end?'max':'min')+', '+lam+' nm'); } }
    for(const [pd,pL] of [[0.3,1],[8,1],[0.3,60],[8,60]]){ Object.assign(ST,DEFAULTS,{view:'path',pd,pL}); const M=buildModel(), h2=readoutHTML(M);
      chk(M.P.mins.every(q=>isFinite(q.y)&&isFinite(q.yf))&&h2.indexOf('NaN')<0,'path d='+pd+' L='+pL); }
    ok(nBad===0,'every medium, frequency end, separation, slit and barrier end, every aperture at its parameter and wavelength ends, and path difference at its corners: finite and clean ('+nCase+' cases)'); }
  Object.assign(ST,stSave); resetRuns();

  /* ---------- L. the scene object ---------- */
  { const shot=makeShot(1100,712); const S=makeScene({getContext:()=>shot});
    Object.assign(ST,DEFAULTS); resetRuns(); CLOCK.acc=0;
    let adv=0; for(let f=0;f<5;f++) if(S.step()) adv++; ok(adv>=2,'the tank advances in the frame loop');
    ST.view='far'; ok(!S.step(),'the far field is static'); ST.view='path'; ok(!S.step(),'so is path difference'); ST.view='lattice'; ok(!S.step(),'and the lattice view');
    /* the pointer: a tape end, a probe, the barrier */
    ST.view='tank'; ST.tape=true; ST.meter=true;
    let G=latGeo(shot,S.W,S.H,buildModel()); const t0=TOOLS.tape[0];
    ok(S.pointer('down',G.sq.x+t0[0]*G.sq.w,G.sq.y+t0[1]*G.sq.h),'pointer-down on a tape end grabs it'); eq(DRAG.what,'tape0','the first end');
    S.pointer('move',G.sq.x+0.1*G.sq.w,G.sq.y+0.2*G.sq.h); close(TOOLS.tape[0][0],0.1,1e-12,'the end follows the pointer'); ok(S.pointer('up',0,0),'released');
    S.pointer('down',G.sq.x+TOOLS.probes[1][0]*G.sq.w,G.sq.y+TOOLS.probes[1][1]*G.sq.h); eq(DRAG.what,'probe1','a probe grabs'); S.pointer('move',G.sq.x+2*G.sq.w,G.sq.y-50);
    close(TOOLS.probes[1][0],1,0,'clamped to the tank'); close(TOOLS.probes[1][1],0,0,'at the top'); S.pointer('up',0,0);
    ok(!S.pointer('down',G.sq.x+0.93*G.sq.w,G.sq.y+0.07*G.sq.h),'empty water grabs nothing');
    ST.view='slits'; ST.barrier='one'; G=latGeo(shot,S.W,S.H,buildModel()); const R=RUNS.slits;
    ok(S.pointer('down',cellX(G.sq,R,ST.bcol),G.sq.y1+12),'pointer-down on the barrier handle grabs it');
    S.pointer('move',G.sq.x+0.25*G.sq.w,G.sq.y1+12); eq(ST.bcol,Math.round(LAT.PAD-0.5+0.25*LAT.VIS),'the barrier follows to a quarter of the way');
    S.pointer('move',G.sq.x-500,0); eq(ST.bcol,BCOL_MIN,'and stops at PhET’s tenth'); S.pointer('up',0,0);
    ST.view='far'; ok(!S.pointer('down',300,300),'the far field ignores the pointer'); ST.view='path'; ok(!S.pointer('down',300,300),'so does path difference');
    Object.assign(TOOLS,JSON.parse(JSON.stringify(TOOLS0))); Object.assign(ST,stSave); resetRuns(); }

  /* ---------- M. the layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const GROUPS=[
    [{view:'tank',scene:'water'},160,[{},{look:'side',graph:true},{tape:true,watch:true,meter:true,graph:true}]],
    [{view:'tank',scene:'sound'},160,[{soundView:'particles'},{soundView:'both',graph:true,meter:true}]],
    [{view:'tank',scene:'light'},160,[{},{tape:true,watch:true,meter:true,graph:true},{screen:false},{inten:false}]],
    [{view:'tank',scene:'water',wave:'pulse'},90,[{}]],
    [{view:'two',scene:'water'},160,[{},{nodal:false,look:'side'}]],
    [{view:'two',scene:'light'},200,[{},{graph:true,meter:true},{src2:false}]],
    [{view:'slits',scene:'light',barrier:'two'},260,[{},{graph:true,meter:true,tape:true}]],
    [{view:'slits',scene:'light',barrier:'none'},160,[{}]],
    [{view:'slits',scene:'sound',barrier:'one',bcol:40},200,[{},{graph:true}]],
    [{view:'slits',scene:'water',barrier:'two'},200,[{}]],
  ];
  const FAR=[{},{ap:'rect',recW:0.4,recH:0.04},{ap:'cs'},{ap:'disorder',disL:4},{ap:'figure',figR:45},{ap:'gauss'},{ap:'slits',sltN:5},{laser:false},{farMode:'lin',ap:'ellipse',ellE:0.9}];
  const OTHER=[{view:'path'},{view:'path',pd:0.4},{view:'path',pd:8,pL:3},{view:'path',pL:60,asym:false},{view:'lattice'},{view:'lattice',scene:'light'},{view:'lattice',scene:'sound'}];
  const CONFIGS=[];
  for(const [base,steps,vars] of GROUPS) vars.forEach((v,i)=>CONFIGS.push([base,steps,v,i===0]));
  for(const v of FAR) CONFIGS.push([Object.assign({view:'far'},v),0,{},true]);
  for(const v of OTHER) CONFIGS.push([v,0,{},true]);
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [base,steps,over,fresh] of CONFIGS){
    Object.assign(ST,DEFAULTS,base,over);
    if(fresh&&LATTICE_VIEWS[base.view]){ resetRuns(); if(base.wave==='pulse'){ const R=syncRun(base.view); firePulse(R); } runFor(base.view,steps); }
    const nm=JSON.stringify(Object.assign({},base,over));
    for(const [W,H] of SIZES){
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill'), rects=fills.reduce((a,o)=>a+(o.n||1),0);
      const strokes=c.ops.filter(o=>o.op==='stroke').length;
      /* floors on what the ops CARRY (rect sub-paths), per kind of view: the fields batch
         thousands of cells into a few fills; the lattice analysis is curves */
      const side=ST.look==='side'&&ST.scene==='water';
      const floor=base.view==='far'?(base.laser===false?4:30):(LATTICE_VIEWS[base.view]?(side?4:60):(base.view==='path'?20:0));
      ok(rects>=floor&&texts.length>=2&&(base.view!=='lattice'||strokes>=12),nm+' '+W+'x'+H+' draws substance ('+rects+' rects, '+strokes+' strokes, floor '+floor+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
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
