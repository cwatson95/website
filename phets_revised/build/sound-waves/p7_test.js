
/* ================================================================== *
 *  selfTest — headless verification.  Every reference is a line of    *
 *  build/sound-waves/refvals.txt (derive.py's output, read in full),  *
 *  carried in REF under its printed label: (twin) = the numpy repeat  *
 *  of this engine, (python)/(scipy) = computed outside, (WI) = a line *
 *  derive.py checked against build/wave-interference/refvals.txt      *
 *  before printing it.                                                *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  function ref(label,i){ const v=REF[label]; if(!v) throw new Error('no reference line "'+label+'"'); return v[i||0]; }
  const stSave=Object.assign({},ST), toolSave=JSON.parse(JSON.stringify(TOOLS));

  /* ---------- A. PhET's constants and geometry (sound-waves_en.html 1.1.11) ---------- */
  eq(AIR.W,10,'PhET’s wave area is 1000 model units = 10 m');
  eq(AIR.v,343,'34.3 cm/ms = 343 m/s'); eq(AIR.fmin,100,'the slider starts at 100 Hz');
  eq(AIR.fmax,1000,'and ends at 1000 Hz'); eq(AIR.f0,550,'PhET’s initial 0.55 per ms');
  eq(AIR.ampMax,10,'PhET’s amplitude range 0 to 10'); eq(AIR.amp0,5,'and its initial 5');
  eq(LAT.AMP_CAL,1.2,'the source cell is driven at 1.2 x the amplitude (PhET’s value)');
  eq(LAT.C,0.5,'Courant number C = 1/2 (PhET’s WAVE_SPEED)');
  eq(LAT.PAD,20,'PhET’s 20-cell pad'); eq(LAT.VIS,LAT.N-2*LAT.PAD,'so 191 of 231 cells are visible');
  eq(U_FULL,2,'full contrast at 2 lattice units (PhET’s positive end)');
  close(ref("PhET's contrast: full white at u =, full black at u =, this sim's symmetric scale",1),-1.5,0,
        'PhET’s negative end is -1.5, which this sim does not copy');
  eq(AIR.phetMaxSoundDist,85,'PhET’s MAX_SOUND_DISTANCE is 85 cells, a taper this sim does not copy');
  rel(AIR.phetEventRate,ref('EVENT_RATE'),1e-15,'PhET’s event rate 20 x 111/61 (WI)');
  rel(AIR.phetTimeScale,ref('PhET time scale, s of model time per s of wall time, and the slow-motion factor'),1e-15,
      'PhET’s time scale, 4.8376 ms of model time per wall second (python)');
  rel(1/AIR.phetTimeScale,ref('PhET time scale, s of model time per s of wall time, and the slow-motion factor',1),1e-12,
      'so the clock runs 206.7 times slower than real (python)');
  rel(MUR1,ref('MUR1 MUR2A MUR2B',0),1e-15,'Mur -1/3 (WI)');
  rel(MUR2A,ref('MUR1 MUR2A MUR2B',1),1e-15,'Mur 4/3 (WI)');
  rel(MUR2B,ref('MUR1 MUR2A MUR2B',2),1e-15,'Mur 1/12 (WI)');
  { const R=makeRun(AIR.f0);
    rel(sceneDx(),ref('geometry: W, dx, source x, mid y',1),1e-15,'dx = 10 m / 191 (python)');
    rel(xOfCell(R,srcCol(R)),ref('geometry: W, dx, source x, mid y',2),1e-14,'the speaker is 1.806 m into the box (python)');
    rel(xOfCell(R,srcRow(R)),ref('geometry: W, dx, source x, mid y',3),1e-14,'and exactly half way up it (python)');
    eq(srcCol(R),ref('lattice: N, PAD, VIS, source column',3),'on lattice column 54');
    close(xOfCell(R,srcCol(R)),ref('PhET source x (viewToModelX of lattice column 40), m'),0.01,
          'which is within 5 mm of PhET’s own speaker position (python)'); }
  rel(WALLR.xmin,AIR.W/3,1e-15,'PhET’s wall runs from W/3'); rel(WALLR.xmax,2*AIR.W/3,1e-15,'to 2W/3');
  rel(WALLR.amin,0.1*PI,1e-15,'and leans from 18 degrees'); rel(WALLR.amax,0.5*PI,1e-15,'to 90');
  rel(WALLR.a0,PI/4,1e-15,'starting at 45');
  eq(AIR.phetListenerLambdaK,36,'PhET’s listener interference uses lambda = 36/f model units, not v/f');
  rel(AIR.phetListenerLambdaK*10/AIR.v,ref("PhET's listener wavelength over v/f"),1e-14,
      'which is 4.96 % longer than the real wavelength (python)');

  /* ---------- B. the lattice: the stencil, the dispersion relation, the calibration ------- */
  for(const k of Object.keys(REF)) if(k.indexOf('latOmega ')===0){
    const a=k.slice(9).split(' ').map(Number);
    rel(latOmega(a[0],a[1]),ref(k),1e-14,k+' (WI)');
  }
  close(latOmega(PI,PI),ref('lattice Omega max'),1e-15,'the highest frequency the lattice carries is 2 asin(C sqrt2) = pi/2 (WI)');
  /* the stencil itself, on an exact lattice plane wave — the same falsification derive.py does */
  for(const k of Object.keys(REF)) if(k.indexOf('plane-wave residual')===0){
    const m=/kx=(\S+) ky=(\S+)$/.exec(k), kx=+m[1], ky=+m[2], n=41;
    const Om=latOmega(kx,ky);
    rel(Om,ref(k,1),1e-14,'plane wave '+kx+','+ky+': Omega (python)');
    const L=makeLattice(n,n,0);
    for(let j=0;j<n;j++) for(let i=0;i<n;i++){
      const ph=kx*i+ky*j;
      L.up[j*n+i]=Math.sin(ph+Om); L.u[j*n+i]=Math.sin(ph);
    }
    latStep(L);
    let worst=0;
    for(let j=2;j<n-2;j++) for(let i=2;i<n-2;i++)
      worst=Math.max(worst,Math.abs(L.u[j*n+i]-Math.sin(kx*i+ky*j-Om)));
    ok(worst<1e-13,'the stencil reproduces the exact lattice plane wave '+kx+','+ky+' ['+worst.toExponential(2)+']');
  }
  for(const k of Object.keys(REF)) if(k.indexOf('omega_step(')===0){
    const Nl=+/omega_step\(([^)]+)\)/.exec(k)[1];
    rel(omegaStep(Nl),ref(k,0),1e-14,k+' (python)');
    rel(TAU/latK(omegaStep(Nl),0),ref(k,1),1e-12,'and 2 pi / latK inverts it back to '+Nl+' cells (python)');
  }
  let nCal=0;
  for(const f of [100,250,550,775,1000]){
    const kb='  '+f.toFixed(1)+' Hz: ';
    rel(waveLen(f),ref(kb+'lambda, cells per wavelength, Omega, dt, steps per period',0),1e-14,f+' Hz: lambda = v/f (python)');
    rel(cellsPerWave(f),ref(kb+'lambda, cells per wavelength, Omega, dt, steps per period',1),1e-14,f+' Hz: cells per wavelength (python)');
    rel(omegaStep(cellsPerWave(f)),ref(kb+'lambda, cells per wavelength, Omega, dt, steps per period',2),1e-14,f+' Hz: radians per step (python)');
    rel(stepDt(f),ref(kb+'lambda, cells per wavelength, Omega, dt, steps per period',3),1e-14,f+' Hz: time per step (python)');
    /* the calibration's own claim, at every setting */
    const Nl=cellsPerWave(f);
    close(latOmega(TAU/Nl,0),omegaStep(Nl),1e-15,f+' Hz: the solved step lies on the dispersion relation');
    rel(latK(omegaStep(Nl),0)*Nl,TAU,1e-12,f+' Hz: and inverts to exactly v/f along the axis');
    const ka=latK(omegaStep(Nl),0), kd=latK(omegaStep(Nl),PI/4);
    const ka2='  '+f.toFixed(1)+' Hz: axis lambda in cells, diagonal lambda in cells, diagonal/axis - 1';
    rel(TAU/ka,ref(ka2,0),1e-11,f+' Hz: the axis wavelength in cells (python)');
    rel(TAU/kd,ref(ka2,1),1e-11,f+' Hz: the diagonal wavelength in cells (python)');
    rel((TAU/kd)/(TAU/ka)-1,ref(ka2,2),1e-9,f+' Hz: the lattice’s anisotropy (python)');
    const ks='  '+f.toFixed(1)+' Hz: phase speed and group speed along the axis, in cells per step, against C = 1/2';
    rel(latPhaseSpeed(ka,0),ref(ks,0),1e-12,f+' Hz: phase speed in cells per step (python)');
    rel(latGroupSpeed(ka,0),ref(ks,1),1e-12,f+' Hz: group speed in cells per step (python)');
    const kp='  '+f.toFixed(1)+" Hz: PhET's fixed step on PhET's 151 lattice gives lambda, and lambda/(v/f) - 1";
    rel(phetLambda(f),ref(kp,0),1e-12,f+' Hz: PhET’s one step gives this wavelength (python)');
    close(phetLambda(f)/waveLen(f)-1,ref(kp,1),1e-12,f+' Hz: and this error');
    const kc='  '+f.toFixed(1)+" Hz: PhET's cells per wavelength on its own 111-cell view";
    rel(AIR.v/f/(AIR.W/AIR.phetVis),ref(kc),1e-13,f+' Hz: PhET’s own cells per wavelength (python)');
    const kw='  steps per second of wall time at '+f.toFixed(1)+' Hz';
    if(REF[kw]) rel(AIR.phetTimeScale/stepDt(f),ref(kw),1e-12,f+' Hz: lattice steps per second of wall time (python)');
    nCal++;
  }
  eq(nCal,5,'all five calibration settings checked');
  ok(phetLambda(1000)/waveLen(1000)-1<-0.12,'PhET’s single fixed step is more than 12 % short at 1000 Hz');
  ok(cellsPerWave(1000)>6&&AIR.v/1000/(AIR.W/AIR.phetVis)<4,
     'this lattice holds 6.55 cells per wavelength at 1000 Hz where PhET’s holds 3.81');
  /* Mur's reflection: the price of the absorbing edge (order 2 against order 1) */
  for(const th of [0,PI/6,PI/4,PI/3]){
    const k=latK(omegaStep(cellsPerWave(550)),th);
    const lb='  Mur |R| at 550.0 Hz, '+(th===0?'0.0':String(th))+' rad off normal (order 2, order 1)';
    if(REF[lb]===undefined) continue;
    rel(murReflection(k*Math.cos(th),k*Math.sin(th),2),ref(lb,0),1e-11,'Mur |R| order 2 at '+fmt(th/DEG,0)+' deg (python)');
    rel(murReflection(k*Math.cos(th),k*Math.sin(th),1),ref(lb,1),1e-11,'Mur |R| order 1 at '+fmt(th/DEG,0)+' deg (python)');
  }
  ok(murReflection(latK(omegaStep(cellsPerWave(550)),0),0,2)<0.02,'the absorbing edge sends back under 2 % at normal incidence');

  /* ---------- C. the source, the button and the pulse ---------- */
  { const R=makeRun(AIR.f0), L=R.lat, si=srcRow(R)*L.nx+srcCol(R);
    runStep(R); close(L.u[si],AIR.amp0*LAT.AMP_CAL*Math.sin(R.Om),1e-15,'after one step the source cell holds 1.2 A sin(Om)');
    for(let s=0;s<7;s++) runStep(R);
    close(R.lat.u[si],AIR.amp0*LAT.AMP_CAL*Math.sin(8*R.Om),1e-14,'and after eight, 1.2 A sin(8 Om)');
    ok(sourceActive(R),'a continuous source starts on (PhET starts it off; the header says so)');
    pressSource(R); ok(!sourceActive(R),'the button switches it off');
    let wrote=0;
    for(let s=0;s<5;s++){ runStep(R); if(R.val!==0) wrote++; }
    eq(wrote,0,'and then nothing more is written into the source cell');
    ok(Math.abs(R.lat.u[si])>1e-6,'though the wave already there goes on through it');
    pressSource(R); ok(sourceActive(R)&&R.phi===0,'pressing it again switches it on and restarts the phase at zero');
    setWaveMode(R,false); ok(!sourceActive(R)&&!R.cont,'switching to pulse leaves it armed and silent');
    ok(firePulse(R),'the button fires one pulse'); ok(!firePulse(R),'and is dead until that pulse finishes');
    let n=0; while(R.pulse.on&&n<400){ runStep(R); n++; }
    close(n,TAU/R.Om,1.5,'a pulse lasts exactly one period of the drive ['+n+' steps]');
    ok(firePulse(R),'and then the button works again'); }

  /* ---------- D. the twin: the lattice cell by cell ---------- */
  function twinRun(tag,f,steps,cfg){
    const R=makeRun(f);
    if(cfg&&cfg.pressure!==undefined) R.pressure=cfg.pressure;
    if(cfg&&cfg.pulse){ setWaveMode(R,false); firePulse(R); }
    for(let s=0;s<steps;s++) runStep(R);
    const L=R.lat, nx=L.nx;
    let hit=0;
    for(const k of Object.keys(REF)) if(k.indexOf('TWIN '+tag+' u(')===0){
      const m=/u\((\d+),(\d+)\)/.exec(k);
      rel(L.u[(+m[2])*nx+(+m[1])],ref(k),1e-11,k+' (twin)'); hit++;
    }
    eq(hit,10,'ten pinned cells for the '+tag+' run');
    let mx=0, sq=0, vis=0;
    for(let j=LAT.PAD;j<L.ny-LAT.PAD;j++) for(let i=LAT.PAD;i<L.nx-LAT.PAD;i++){
      const v=L.u[j*nx+i]; if(Math.abs(v)>mx) mx=Math.abs(v); sq+=v*v; if(L.vis[j*nx+i]) vis++;
    }
    const kk='TWIN '+tag+' max|u|, sum u^2, visited cells';
    rel(mx,ref(kk,0),1e-11,tag+': the largest |u| in the visible box (twin)');
    rel(sq,ref(kk,1),1e-10,tag+': the sum of u^2 over it (twin)');
    eq(vis,ref(kk,2),tag+': and the number of cells the wave has reached (twin)');
    const kt='TWIN '+tag+' t n phi';
    rel(R.t,ref(kt,0),1e-13,tag+': the physical time (twin)');
    eq(R.n,ref(kt,1),tag+': the number of steps (twin)');
    rel(R.phi,ref(kt,2),1e-13,tag+': and the drive’s phase (twin)');
    return R;
  }
  twinRun('mid',550,300);
  twinRun('high',1000,300);
  const Rpul=twinRun('pulse',550,200,{pulse:true});
  eq(Rpul.pulse.on?0:1,ref('TWIN pulse finished'),'the pulse has finished by step 200 (twin)');
  twinRun('thin',550,300,{pressure:0.25});
  /* the air-density law is exact, not approximate: the drive scales, so the whole field does */
  { const Ra=makeRun(550), Rb=makeRun(550); Rb.pressure=0.25;
    for(let s=0;s<220;s++){ runStep(Ra); runStep(Rb); }
    let worst=0;
    for(let q=0;q<Ra.lat.u.length;q++) worst=Math.max(worst,Math.abs(Rb.lat.u[q]-0.25*Ra.lat.u[q]));
    close(worst,ref('air density: max |u(p=0.25) - 0.25 u(p=1)| over the lattice after 220 steps'),1e-14,
          'quarter the air, exactly a quarter of the field, cell for cell (twin)');
    ok(worst<1e-13,'and that is exact, not approximate ['+worst.toExponential(2)+']');
    let ma=0,mb=0;
    for(let q=0;q<Ra.lat.u.length;q++){ ma=Math.max(ma,Math.abs(Ra.lat.u[q])); mb=Math.max(mb,Math.abs(Rb.lat.u[q])); }
    rel(mb/ma,ref('air density: max |u| at p = 1 and p = 0.25, and their ratio',2),1e-12,'the amplitude ratio is the density ratio (twin)'); }

  /* ---------- E. the composed pictures: one speaker, two, and the wall ---------- */
  { const R=makeRun(550);
    for(let s=0;s<400;s++) runStep(R);
    const L=R.lat, nx=L.nx, mid=srcRow(R), V=LAT.VIS, pad=L.pad;
    const hA=Math.round(ref("two sources: PhET's separation, the lattice's, in cells and m",1))/2;
    const g1=fieldGrid(R,'one',[mid],null);
    let n1=0;
    for(const k of Object.keys(REF)) if(k.indexOf('COMP one (')===0){
      const m=/\((\d+),(\d+)\)/.exec(k), i=+m[1], j=+m[2];
      rel(g1.v[(j-pad)*V+(i-pad)],ref(k),1e-11,k+' (twin)'); n1++;
    }
    eq(n1,6,'six pinned cells of the one-speaker picture');
    eq(g1.nfront,V*V,'and nothing is hidden');
    const g2=fieldGrid(R,'two',[mid-hA,mid+hA],null);
    for(const k of Object.keys(REF)) if(k.indexOf('COMP two (')===0){
      const m=/\((\d+),(\d+)\)/.exec(k), i=+m[1], j=+m[2];
      rel(g2.v[(j-pad)*V+(i-pad)],ref(k,0),1e-11,k+' (twin)');
    }
    /* the second speaker is a SHIFT, and that is exactly linear superposition */
    { let worst=0;
      for(let j=0;j<V;j++) for(let i=0;i<V;i++){
        const a=latAt(L,pad+i,pad+j+hA), b=latAt(L,pad+i,pad+j-hA);
        worst=Math.max(worst,Math.abs(g2.v[j*V+i]-(a+b)));
      }
      ok(worst===0,'the two-speaker picture is exactly the sum of two shifted copies ['+worst+']'); }
    const G=wallGeom(AIR.W/3,PI/4);
    const g3=fieldGrid(R,'wall',[mid],G);
    let nw=0, nblank=0;
    for(const k of Object.keys(REF)) if(k.indexOf('COMP wall (')===0){
      const m=/\((\d+),(\d+)\)/.exec(k), i=+m[1], j=+m[2];
      rel(g3.v[(j-pad)*V+(i-pad)],ref(k,0),1e-11,k+' (twin)');
      eq(g3.mask[(j-pad)*V+(i-pad)],ref(k,3),k+': drawn or hidden (twin)');
      nw++; if(!ref(k,3)) nblank++;
    }
    eq(nw,6,'six pinned cells of the reflected picture'); ok(nblank>=2,'two of them behind the wall');
    for(const k of Object.keys(REF)) if(k.indexOf('  wall xw = ')===0&&k.indexOf('visible cells in front')>0){
      const m=/xw = (\S+), angle = (\S+):/.exec(k);
      const gg=fieldGrid(R,'wall',[mid],wallGeom(+m[1],+m[2]));
      eq(gg.nfront,ref(k,0),'the wall at '+fmt(+m[1],2)+' m, '+fmt(+m[2]/DEG,0)+' deg hides all but this many cells (python)');
      rel(gg.nfront/(V*V),ref(k,1),1e-12,'  which is this fraction of the box (python)');
    }
    /* the bilinear point read the listener uses */
    for(const tag of ['one','two','wall']){
      const rows=(tag==='two')?[mid-hA,mid+hA]:[mid];
      for(const k of Object.keys(REF)) if(k.indexOf('FIELD '+tag+' at (')===0){
        const m=/\(([^,]+), ([^)]+)\)/.exec(k);
        rel(fieldAtModel(R,tag,rows,G,+m[1],+m[2]),ref(k),1e-11,k+' (twin)');
      }
    }
    /* the parcels */
    const gp=fieldGrid(R,'one',[mid],null), P=parcelPositions(R,gp);
    rel(PARC_PUSH*(V/PARC_N)/((TAU/R.Nl)*U_FULL),ref('parcels: the exaggeration KD, in cells per unit of gradient'),1e-13,
        'the parcels’ exaggeration KD (python)');
    for(const q of [0,100,220,440]){
      rel(P[q][0],ref('parcels: number '+q+' at',0),1e-10,'parcel '+q+' x (python)');
      rel(P[q][1],ref('parcels: number '+q+' at',1),1e-10,'parcel '+q+' y (python)');
    }
    { let push=0;
      for(let a=0;a<=PARC_N;a++) for(let b=0;b<=PARC_N;b++){
        const q=a*(PARC_N+1)+b;
        const i=clamp(Math.round(a*V/PARC_N),1,V-2), j=clamp(Math.round(b*V/PARC_N),1,V-2);
        push=Math.max(push,Math.abs(P[q][0]-i),Math.abs(P[q][1]-j));
      }
      rel(push,ref('parcels: the largest push, in cells and as a fraction of the spacing',0),1e-10,
          'the largest parcel push, in cells (python)');
      ok(push/(V/PARC_N)<0.5,'and it stays well under half the parcel spacing, so no two rows cross ['
         +fmt(push/(V/PARC_N),3)+']'); } }

  /* ---------- F. the wall: the mirror, the two angles, Fermat, and du/dn = 0 ---------- */
  { let wi2=0, wp=0, wd=0;
    for(const xw of [AIR.W/3,0.5*AIR.W,2*AIR.W/3]) for(const th of [0.1*PI,0.25*PI,PI/4,0.4*PI,0.5*PI]){
      const G=wallGeom(xw,th);
      for(const p of [[1,2],[4,7],[0.5,5],[3,9]]){
        const Q=wallMirror(G,p[0],p[1]), B=wallMirror(G,Q[0],Q[1]);
        wi2=Math.max(wi2,Math.abs(B[0]-p[0]),Math.abs(B[1]-p[1]));
        const F=wallFoot(G,p[0],p[1]);
        wp=Math.max(wp,Math.abs(p[0]+2*(F[0]-p[0])-Q[0]),Math.abs(p[1]+2*(F[1]-p[1])-Q[1]));
        wd=Math.max(wd,Math.abs(Math.abs(wallSide(G,p[0],p[1]))-Math.abs(wallSide(G,Q[0],Q[1]))));
      }
    }
    const kk="wall: mirror involution, PhET's projection form, distance to the wall (worst over 60)";
    ok(wi2<=Math.max(1e-14,ref(kk,0)*4),'mirroring twice is the identity ['+wi2.toExponential(2)+'] (python '+ref(kk,0).toExponential(2)+')');
    ok(wp<=Math.max(1e-14,ref(kk,1)*4),'and agrees with PhET’s own projection form ['+wp.toExponential(2)+']');
    ok(wd<=Math.max(1e-14,ref(kk,2)*4),'and keeps the distance to the wall ['+wd.toExponential(2)+']');
    let wa=0, wf=0, nray=0;
    const S=[xOfCell(RUN,srcCol(RUN)),xOfCell(RUN,srcRow(RUN))];
    for(const [xw,th] of [[AIR.W/3,PI/4],[0.5*AIR.W,0.3*PI],[2*AIR.W/3,0.15*PI],[AIR.W/3,0.5*PI]]){
      const G=wallGeom(xw,th), im=wallMirror(G,S[0],S[1]);
      for(const p of [[2,8.5],[3,7],[1,9],[4.5,9.5]]){
        if(wallSide(G,p[0],p[1])>=0) continue;
        const Q=wallBounce(G,S[0],S[1],p[0],p[1]);
        if(!Q) continue;
        const a1=angleToNormal(G,Q[0]-S[0],Q[1]-S[1]), a2=angleToNormal(G,p[0]-Q[0],p[1]-Q[1]);
        wa=Math.max(wa,Math.abs(a1-a2));
        wf=Math.max(wf,Math.abs(Math.hypot(Q[0]-S[0],Q[1]-S[1])+Math.hypot(p[0]-Q[0],p[1]-Q[1])
                                -Math.hypot(p[0]-im[0],p[1]-im[1])));
        nray++;
      }
    }
    const kr="wall: |angle of incidence - angle of reflection| and |SQ + QP - S'P| (worst over 14 rays)";
    eq(nray,14,'fourteen rays reach the wall and come back');
    ok(wa<1e-13,'the angle of incidence equals the angle of reflection ['+wa.toExponential(2)+'] (python '+ref(kr,0).toExponential(2)+')');
    ok(wf<1e-13,'and the reflected path is Fermat’s shortest ['+wf.toExponential(2)+']');
    /* one ray in full, against the printed one */
    for(const k of Object.keys(REF)) if(k.indexOf('  ray at xw = ')===0){
      const m=/xw = (\S+), th = (\S+) to \(([^,]+), ([^)]+)\)/.exec(k);
      const G=wallGeom(+m[1],+m[2]), Q=wallBounce(G,S[0],S[1],+m[3],+m[4]);
      rel(Q[0],ref(k,0),1e-11,k+': the wall point x (python)');
      rel(Q[1],ref(k,1),1e-11,k+': the wall point y (python)');
      rel(angleToNormal(G,Q[0]-S[0],Q[1]-S[1]),ref(k,2),1e-11,k+': the angle of incidence (python)');
      rel(angleToNormal(G,(+m[3])-Q[0],(+m[4])-Q[1]),ref(k,3),1e-11,k+': and of reflection (python)');
    }
    for(const k of Object.keys(REF)) if(k.indexOf('  image source for xw = ')===0){
      const m=/xw = (\S+), angle = (\S+) rad/.exec(k);
      const G=wallGeom(+m[1],+m[2]), im=wallMirror(G,S[0],S[1]);
      rel(im[0],ref(k,0),1e-11,k+': x (python)');
      rel(im[1],ref(k,1),1e-11,k+': y (python)');
      rel(Math.hypot(im[0]-S[0],im[1]-S[1]),ref(k,2),1e-11,k+': speaker to image (python)');
    }
    /* du/dn = 0 on the wall, on the field the sim really draws */
    { const R=makeRun(550);
      for(let s=0;s<700;s++) runStep(R);
      let worst=0;
      for(const [xw,th] of [[AIR.W/3,PI/4],[0.5*AIR.W,0.3*PI],[2*AIR.W/3,0.15*PI]]){
        const G=wallGeom(xw,th);
        for(const t of [-2,-1,0,1,2]){
          const px=G.ax+t*G.dxh, py=G.ay+t*G.dyh;
          if(!(px>0&&px<AIR.W&&py>0&&py<AIR.W)) continue;
          const hh=0.01;
          const f1=mirrorSum(R,G,px-hh*G.nxh,py-hh*G.nyh);
          const f2=mirrorSum(R,G,px+hh*G.nxh,py+hh*G.nyh);
          worst=Math.max(worst,Math.abs(f1-f2)/(2*hh)/Math.max(1e-9,Math.abs(f1)));
        }
      }
      const kn='wall: worst relative |du/dn| on the wall, from the drawn field (should be 0 by construction)';
      ok(worst<1e-9,'the drawn field has no flow through the wall ['+worst.toExponential(2)+'] (python '+ref(kn).toExponential(2)+')');
      ok(ref(kn)<1e-9,'and the twin agrees'); }
    /* the wall drawn on the box */
    for(const k of Object.keys(REF)) if(k.indexOf('  wall xw = ')===0&&k.indexOf('meets the box at')>0){
      const m=/xw = (\S+) angle = (\S+) meets/.exec(k);
      const e=wallEnds(wallGeom(+m[1],+m[2]));
      ok(!!e,k+': the wall meets the box');
      const got=[e[0][0],e[0][1],e[1][0],e[1][1]], wantv=[ref(k,0),ref(k,1),ref(k,2),ref(k,3)];
      let dmin=Math.min(Math.hypot(got[0]-wantv[0],got[1]-wantv[1])+Math.hypot(got[2]-wantv[2],got[3]-wantv[3]),
                        Math.hypot(got[0]-wantv[2],got[1]-wantv[3])+Math.hypot(got[2]-wantv[0],got[3]-wantv[1]));
      ok(dmin<1e-9,k+' (python) ['+dmin.toExponential(2)+']');
    } }

  /* ---------- G. two sources: the hyperbolae and the interference law ---------- */
  { const d=ref("two sources: PhET's separation, the lattice's, in cells and m",2);
    const dc=ref("two sources: PhET's separation, the lattice's, in cells and m",1);
    rel(dc*sceneDx(),d,1e-14,'the lattice’s own speaker separation (python)');
    for(const f of [100,550,1000]){
      const k='  '+f.toFixed(1)+' Hz: lambda, d/lambda, number of nodal lines each side';
      rel(waveLen(f),ref(k,0),1e-14,f+' Hz: lambda (python)');
      rel(d/waveLen(f),ref(k,1),1e-13,f+' Hz: d/lambda (python)');
      eq(nodeOrders(d,waveLen(f)).length,ref(k,2),f+' Hz: how many quiet lines each side (python)');
    }
    /* the closed form against a brute-force scan of |r1 - r2| — done here, not read */
    const lam=waveLen(550);
    let worst=0, nch=0;
    for(const m of nodeOrders(d,lam)) for(const y of [0.2,0.5,1,2,3]){
      const xc=nodeX(m,lam,d,y);
      if(!isFinite(xc)) continue;
      const g=x=>Math.abs(Math.hypot(x,y-d/2)-Math.hypot(x,y+d/2))-(m+0.5)*lam;
      let lo=1e-9, hi=60;
      if(g(lo)*g(hi)>0) continue;
      for(let it=0;it<200;it++){ const mm=0.5*(lo+hi); if(g(lo)*g(mm)<=0) hi=mm; else lo=mm; }
      worst=Math.max(worst,Math.abs(0.5*(lo+hi)-xc)); nch++;
    }
    eq(nch,16,'sixteen points on the quiet hyperbolae checked by bisection');
    ok(worst<1e-9,'the closed-form hyperbola IS the locus of |r1 - r2| = (m + 1/2) lambda ['+worst.toExponential(2)+']');
    /* nodeX and nodeY are inverses of one another */
    { let w2=0;
      for(const m of nodeOrders(d,lam)) for(const x of [0.5,2,5,9]){
        const y=nodeY(m,lam,d,x); if(!isFinite(y)) continue;
        w2=Math.max(w2,Math.abs(nodeX(m,lam,d,y)-x));
      }
      ok(w2<1e-9,'nodeX inverts nodeY ['+w2.toExponential(2)+']'); }
    for(const k of Object.keys(REF)) if(/^  m = \d+: asymptote angle/.test(k)){
      const m=+/m = (\d+)/.exec(k)[1];
      const a=(m+0.5)*lam/2, c=d/2, sl=a/Math.sqrt(c*c-a*a);
      rel(Math.atan(sl),ref(k,0),1e-12,'m = '+m+': the asymptote’s angle (python)');
      rel(nodeFarAngle(m,lam,d),ref(k,1),1e-12,'m = '+m+': and asin((m+1/2)lambda/d) (python)');
      close(Math.atan(sl)-nodeFarAngle(m,lam,d),0,1e-12,'m = '+m+': the two are the same statement');
    }
    /* the lattice's own nodal lines, against the hyperbola and against the anisotropic form */
    const Om=omegaStep(cellsPerWave(550));
    let worstH=0, worstA=0, nn=0;
    for(const k of Object.keys(REF)) if(/^  lattice node m = /.test(k)){
      const mm=/m = (\d+) at column (\d+)/.exec(k), m=+mm[1], col=+mm[2];
      const xm=(col-LAT.PAD+0.5)*sceneDx()-(LAT.SRC_OFF+0.5)*sceneDx();
      const yp=nodeY(m,lam,d,xm);
      rel(LAT.MID+yp/sceneDx(),ref(k,1),1e-9,k+': the hyperbola’s row (python)');
      worstH=Math.max(worstH,Math.abs(ref(k,2)));
      const kA='  node m = '+m+' at column '+col+" with the lattice's own k(theta): row, and measured - this";
      const ya=nodeYLattice(m,Om,d,xm,yp);
      rel(LAT.MID+ya/sceneDx(),ref(kA,0),1e-7,kA+' (python)');
      worstA=Math.max(worstA,Math.abs(ref(kA,1)));
      nn++;
    }
    eq(nn,10,'ten measured nodal points');
    /* latKofDir carries a unit conversion (cells to metres) and a direction.  The conversion
       is pinned against the calibration itself; the direction is SYMMETRIC about the diagonal
       on a square lattice, so swapping its two arguments provably cannot change anything —
       stated here rather than left as a blind spot (Known-bad list). */
    rel(latKofDir(Om,1,0),TAU/waveLen(550),1e-12,'k(theta) along the axis IS 2 pi / lambda, by the calibration');
    for(const [ax,ay] of [[3,4],[1,0],[2,5]])
      close(latKofDir(Om,ax,ay),latKofDir(Om,ay,ax),1e-12,
            'the square lattice is symmetric about its diagonal: k('+ax+','+ay+') = k('+ay+','+ax+')');
    ok(Math.abs(latKofDir(Om,1,1)-latKofDir(Om,1,0))>0.05,
       'but it is NOT isotropic: the diagonal carries a different wavenumber');
    rel(worstH,ref('two sources: worst |measured - hyperbola| over 10 nodes, in cells'),1e-12,
        'the lattice puts its quiet lines up to 2.45 cells outside the continuum hyperbolae (twin)');
    rel(worstA,ref('two sources: worst |measured - anisotropic prediction| over 10 nodes, in cells'),1e-12,
        'and the lattice’s own k(theta) accounts for all but 0.16 of a cell of that (twin)');
    ok(worstA<0.25&&worstH>1.5,'so the drift is the square lattice’s anisotropy, not noise');
    /* the two-source amplitude law */
    for(const k of Object.keys(REF)) if(/^  two speakers at \(/.test(k)){
      const m=/\(([^,]+), ([^)]+)\)/.exec(k);
      const hA=dc/2, sA=[(LAT.SRC_OFF+0.5)*sceneDx(),(LAT.MID+hA-LAT.PAD+0.5)*sceneDx()];
      const sB=[(LAT.SRC_OFF+0.5)*sceneDx(),(LAT.MID-hA-LAT.PAD+0.5)*sceneDx()];
      const px=+m[1], py=+m[2];
      const rA=Math.hypot(px-sA[0],py-sA[1]), rB=Math.hypot(px-sB[0],py-sB[1]);
      rel(rA-rB,ref(k,3),1e-11,k+': the path difference (python)');
    }
    rel(ref('two speakers: the lattice rows and the model y of each',2),(LAT.MID+dc/2-LAT.PAD+0.5)*sceneDx(),1e-13,
        'the lower speaker sits at this height (python)');
    { const w=ref('two speakers: worst |measured - predicted| over 7 points, textbook and with the lattice k');
      const wl=ref('two speakers: worst |measured - predicted| over 7 points, textbook and with the lattice k',1);
      ok(w<0.08&&wl<w,'the measured interference follows sqrt(A1^2+A2^2+2A1A2 cos dphi) to '+fmt(w,3)
         +' in lattice units, and better with the lattice’s own k ('+fmt(wl,3)+')'); }
    /* twoSourceAmp is the textbook law and nothing else */
    close(twoSourceAmp(1,1,0),2,1e-15,'two equal waves in phase give twice the amplitude');
    close(twoSourceAmp(1,1,PI),0,1e-15,'and exactly out of phase, nothing');
    close(twoSourceAmp(3,4,PI/2),5,1e-14,'a quarter cycle apart, they add in quadrature');
    close(twoSourceAmp(1,1,TAU/3),1,1e-15,'and a third of a cycle apart, they give one'); }

  /* ---------- H. the gas: what pressure does and does not change ---------- */
  rel(soundSpeedIdeal(GAS.T0),ref('ideal-gas sound speed at 20.00 C, sqrt(gamma R T / M)'),1e-13,
      'the ideal gas gives 343.235 m/s at 20.00 C (python)');
  rel(tempForSpeed(AIR.v),ref('temperature at which the ideal gas gives exactly 343 m/s, K and C'),1e-12,
      'and PhET’s 343 m/s is that formula at 292.75 K (python)');
  close(tempForSpeed(AIR.v)-273.15,ref('temperature at which the ideal gas gives exactly 343 m/s, K and C',1),1e-10,
        'which is 19.60 C (python)');
  rel(AIR.v/soundSpeedIdeal(GAS.T0)-1,ref('PhET 343 m/s against the 20 C ideal gas: ratio - 1'),1e-10,
      'so PhET is 0.068 % below the 20 C value (python)');
  { /* the speed does not depend on pressure — demonstrated, not asserted.  The labels are
       python's repr of the fraction, so they are spelled out rather than built from a number. */
    let spread=0;
    for(const [fr,tag] of [[1,'1.0'],[0.5,'0.5'],[0.1,'0.1'],[0.01,'0.01'],[1e-4,'0.0001']]){
      const rho=airDensity(fr), v=Math.sqrt(GAS.gamma*fr*GAS.pAtm/rho);
      const kg='  sound speed at p/p0 = '+tag+' (T = 20 C): rho, v';
      rel(rho,ref(kg,0),1e-12,'the density at '+tag+' atm (python)');
      rel(v,ref(kg,1),1e-12,'and the speed there (python)');
      spread=Math.max(spread,Math.abs(v-soundSpeedIdeal(GAS.T0)));
    }
    ok(spread<1e-9,'the speed of sound is the SAME at 1 atm and at 1e-4 atm ['+spread.toExponential(2)+']'); }
  rel(airDensity(1),ref('air density at 20 C 1 atm, kg/m^3'),1e-13,'air is 1.204 kg/m^3 at 20 C and 1 atm (python)');
  for(const [fr,tag] of [[1,'1.0'],[0.5,'0.5'],[0.25,'0.25'],[0.1,'0.1'],[0.01,'0.01']]){
    rel(dbOf(fr),ref('  air at '+tag+' atm: pressure amplitude ratio, intensity ratio, dB',2),1e-12,
        tag+' atm is this many decibels down (python)');
  }
  close(dbOf(0.1),-20,1e-12,'a tenth of the air is exactly 20 dB down');
  ok(!isFinite(dbOf(0)),'and no air at all is silence, not a number');
  rel(meanFreePath(1),ref('mean free path of air at 20 C 1 atm, m'),1e-13,'the mean free path is 65.7 nm at 1 atm (python)');
  for(const f of [100,550,1000]){
    const k='  Knudsen 1 at '+f.toFixed(1)+' Hz: lambda, and the fraction of an atmosphere where mfp = lambda';
    rel(waveLen(f),ref(k,0),1e-13,f+' Hz: lambda again (python)');
    rel(meanFreePath(1)/waveLen(f),ref(k,1),1e-12,f+' Hz: the atmosphere at which the mean free path is one wavelength (python)');
    rel(knudsen(ref(k,1),f),1,1e-12,f+' Hz: and Knudsen is 1 there');
  }
  ok(knudsen(1,1000)<1e-6,'at 1 atm a 1000 Hz sound is a continuum wave by six orders of magnitude');

  /* ---------- I. lambda measured on the lattice ---------- */
  { const km='measurement: lattice, source offset, settling steps, periods, fit window';
    eq(MEAS.N,ref(km,0),'the measurement tank is 181 cells'); eq(MEAS.SRC,ref(km,1),'the source 5 cells in');
    eq(MEAS.N0,ref(km,2),'after 470 settling steps'); eq(MEAS.PER,ref(km,3),'two whole periods are recorded');
    eq(MEAS.R0,ref(km,4),'and the fit runs from cell 30'); eq(MEAS.R1,ref(km,5),'to cell 120');
    let n=0, worst=0;
    for(const f of [100,325,550,775,1000]){
      const m=measureWave(f), kf='MEAS '+f.toFixed(1)+' Hz: ';
      eq(m.M,ref(kf+'fit steps M, cells of axis, lambda in cells, v/f in cells, ratio - 1',0),f+' Hz: the number of fitted steps (twin)');
      eq(m.nc,ref(kf+'fit steps M, cells of axis, lambda in cells, v/f in cells, ratio - 1',1),f+' Hz: the cells of axis (twin)');
      rel(m.lamCells,ref(kf+'fit steps M, cells of axis, lambda in cells, v/f in cells, ratio - 1',2),1e-9,f+' Hz: lambda in cells (twin)');
      rel(m.lam,ref(kf+'lambda measured and v/f, m',0),1e-9,f+' Hz: lambda in metres (twin)');
      rel(m.lam0,ref(kf+'lambda measured and v/f, m',1),1e-14,f+' Hz: against v/f');
      rel(m.pexp,ref(kf+'envelope power of r (1/sqrt r gives -0.5)'),1e-8,f+' Hz: the envelope’s power of r (twin)');
      ok(Math.abs(m.pexp+0.5)<0.05,f+' Hz: and it is the 1/sqrt(r) of a two-dimensional wave ['+fmt(m.pexp,3)+']');
      for(const c of [5,30,60,120]){
        rel(m.amp[c],ref(kf+'amplitude and unwrapped phase at cell '+c,0),1e-9,f+' Hz: the amplitude at cell '+c+' (twin)');
        rel(m.ph[c],ref(kf+'amplitude and unwrapped phase at cell '+c,1),1e-9,f+' Hz: and the phase there (twin)');
      }
      worst=Math.max(worst,Math.abs(m.err)); n++;
      if(f>=325) ok(Math.abs(m.err)<0.0006,f+' Hz: the lattice’s own wavelength IS v/f to 0.06 % ['+pct(m.err)+']');
    }
    eq(n,5,'five frequencies measured');
    ok(worst<0.004,'and the worst reading over the whole slider is 0.35 %, at 100 Hz, where the fit window holds 1.4 wavelengths');
    for(const f of [100,550,1000]){
      const k='  continuum Hankel phase over the same cells at '+f.toFixed(1)+' Hz: lambda/(v/f) - 1';
      ok(Math.abs(ref(k))<0.004,f+' Hz: the continuum 2-D near field alone would shift the reading by '+pct(ref(k))+' (scipy)');
    }
    /* unwrapPhase: both branches, which the outward wave alone never reaches */
    { const a=unwrapPhase([0,1,2,3]); close(a[3],3,1e-15,'unwrapPhase leaves a smooth run alone');
      const b=unwrapPhase([3,-3+TAU-TAU,0]); ok(isFinite(b[2]),'unwrapPhase handles a fall through pi');
      const up=unwrapPhase([0,-3,3]); close(up[2],-TAU+3,1e-14,'a jump UP by more than pi is a whole turn down');
      const dn=unwrapPhase([0,3,-3]); close(dn[2],TAU-3,1e-14,'and a jump DOWN by more than pi a whole turn up'); }
    /* lineSlope and solve4, against hand cases */
    { const xs=[0,1,2,3,4], ys=[1,3,5,7,9];
      close(lineSlope(xs,ys,0,4),2,1e-14,'lineSlope returns the slope of an exact line');
      const A=[[2,0,0,0],[0,3,0,0],[0,0,4,0],[0,0,0,5]];
      const x=solve4(A,[2,3,4,5]);
      close(x[0]+x[1]+x[2]+x[3],4,1e-14,'solve4 solves a diagonal system');
      const B=[[1,2,3,4],[2,3,4,1],[3,4,1,2],[4,1,2,3]];
      const y=solve4(B,[10,10,10,10]);
      let r2=0;
      for(let i=0;i<4;i++){ let s=0; for(let j=0;j<4;j++) s+=B[i][j]*y[j]; r2=Math.max(r2,Math.abs(s-10)); }
      ok(r2<1e-13,'and a dense one, with pivoting ['+r2.toExponential(2)+']'); } }

  /* ---------- J. the tone ---------- */
  for(const [hz,level] of [[550,0.15],[100,0.3],[1000,0.09]]){
    const tb=toneBuffer(hz,level,TONE_SR);
    const k='tone '+hz.toFixed(1)+' Hz at level '+level+': cycles, samples, looped frequency';
    eq(tb.m,ref(k,0),hz+' Hz: whole cycles in the buffer (python)');
    eq(tb.L,ref(k,1),hz+' Hz: samples (python)');
    rel(tb.hz,ref(k,2),1e-12,hz+' Hz: the frequency it actually loops at (python)');
    rel(tb.hz,hz,2e-4,hz+' Hz: which is the one asked for, to a part in 10^4');
    const k2='  tone '+hz.toFixed(1)+' Hz: sample[1], sample[17], sample[1000], upward zero crossings';
    rel(tb.data[1],ref(k2,0),1e-6,hz+' Hz: sample 1 (python)');
    rel(tb.data[17],ref(k2,1),1e-6,hz+' Hz: sample 17 (python)');
    rel(tb.data[1000],ref(k2,2),1e-6,hz+' Hz: sample 1000 (python)');
    let ups=0;
    for(let q=1;q<tb.L;q++) if(tb.data[q-1]<0&&tb.data[q]>=0) ups++;
    eq(ups,ref(k2,3),hz+' Hz: and its upward zero crossings (python)');
    close(tb.data[0],0,1e-12,hz+' Hz: the buffer starts at zero, so the loop has no click');
  }
  close(TONE_MAX,0.3,1e-15,'the tone\u2019s top output level is 0.3 (Waves Intro\u2019s PhET sound scene uses the same)');
  close(toneLevel('speaker',10,0),0.3,1e-15,'the tone is loudest at the top of the amplitude slider');
  close(toneLevel('speaker',0,5),0,1e-15,'and silent at the bottom');
  close(toneLevel('listener',10,U_FULL),TONE_MAX,1e-15,'with the listener chosen, full contrast is full level');
  close(toneLevel('listener',10,0),0,1e-15,'and a listener in a quiet place hears nothing');

  /* ---------- K. the listener ---------- */
  { const P=makeProbe(8);
    for(let q=0;q<8;q++) probePush(P,Math.sin(TAU*q/8));
    close(probeAmp(P),1,1e-12,'the probe turns a full period of a sine into its amplitude');
    probeResize(P,16); eq(P.count,0,'resizing the probe empties it');
    for(const k of Object.keys(REF)) if(/^  listener at \(7, 3\): factor at /.test(k)){
      const f=+/at (\S+) Hz/.exec(k)[1];
      const q1=ref('listener at (7, 3): r1, r2, dr, and dr/lambda at 550 Hz',0);
      const q2=ref('listener at (7, 3): r1, r2, dr, and dr/lambda at 550 Hz',1);
      rel(Math.abs(Math.cos(PI*(q1-q2)/waveLen(f))),ref(k),1e-12,k+' (python)');
    }
    const kk='two speakers at the lattice rows 83 and 147, listener at the centre: r1, r2, r1 - r2';
    close(ref(kk,2),0,1e-15,'a listener on the axis of symmetry has no path difference at all (python)');
    /* PhET's own listener law, for comparison: it uses 36/f model units */
    const dr=ref('listener at (7, 3): r1, r2, dr, and dr/lambda at 550 Hz',2);
    rel(phetListenerFactor(1,dr,550),Math.abs(Math.cos(PI*dr/(AIR.phetListenerLambdaK/550*100))),1e-15,
        'PhET’s listener factor is |cos(pi dr / (36/f))|');
    ok(Math.abs(phetListenerFactor(1,dr,550)-Math.abs(Math.cos(PI*dr/waveLen(550))))>0.05,
       'and it differs visibly from the same law with the real wavelength'); }

  /* ---------- L. the panels: every view x preset, clean, no NaN, nothing under the hint ---- */
  Object.assign(ST,DEFAULTS);
  resetAll();
  runFor(260);
  const PRESETS=[
    ['default',{}],
    ['quiet',{amp:0}],
    ['low',{f:100}],
    ['high',{f:1000,amp:10}],
    ['pulse',{wave:'pulse'}],
    ['parcels',{look:'particles',graph:true}],
    ['both + tools',{look:'both',ruler:true,watch:true,graph:true}],
    ['no listener',{listener:false}],
    ['vacuum',{pressure:0}],
    ['thin air',{pressure:0.08}],
    ['wall flat',{wallAng:WALLR.amin,wallX:WALLR.xmax}],
    ['wall upright',{wallAng:WALLR.amax,wallX:WALLR.xmin}],
    ['speaker 2 low',{spk2y:0.4}],
    ['no overlays',{nodes:false,image:false}]
  ];
  const SIZES=[[1400,820],[1100,712],[860,620]];
  { /* let the analysis view's cache fill before the sweep, so it is drawn complete */
    ST.view='law';
    for(let q=0;q<12;q++){ const M=buildModel(); if(!M.X.pending) break; }
  }
  let nPanels=0;
  for(const [vk] of TABS){
    for(const [pname,over] of PRESETS){
      Object.assign(ST,DEFAULTS,over); ST.view=vk;
      const M=buildModel();
      /* nothing non-finite anywhere in the model */
      let bad=null;
      const scan=(o,path,dep)=>{
        if(bad||dep>3) return;
        if(typeof o==='number'){ if(!isFinite(o)&&path.indexOf('mfp')<0&&path.indexOf('Kn')<0&&path.indexOf('db')<0) bad=path; return; }
        if(o&&typeof o==='object'&&!(o instanceof Float64Array)&&!(o instanceof Uint8Array))
          for(const k in o) scan(o[k],path+'.'+k,dep+1);
      };
      scan(M,vk+'/'+pname,0);
      ok(!bad,vk+' '+pname+': the model is finite'+(bad?' ('+bad+')':''));
      for(let q=0;q<M.g.v.length;q+=37) if(!isFinite(M.g.v[q])){ bad=bad||'grid'; }
      ok(!bad,vk+' '+pname+': and so is the field it draws');
      const ro=readoutHTML(M)+eqbarHTML(M)+tagHTML(M)+(INFO[vk]||'')+(DERIV[vk]||'');
      ok(!/NaN|undefined|Infinity/.test(ro),vk+' '+pname+': the readout, the equation bar and the prose build clean');
      nPanels++;
    }
  }
  eq(nPanels,TABS.length*PRESETS.length,'every view built at every preset');
  /* the drawing: text boxes, entities, collisions, and the bottom-left corner */
  for(const [vk] of TABS){
    for(const [pname,over] of [PRESETS[0],PRESETS[5],PRESETS[6],PRESETS[10]]){
      Object.assign(ST,DEFAULTS,over); ST.view=vk;
      for(const [W,H] of SIZES){
        const rc=makeShot(W,H);
        drawView(rc,W,H,buildModel());
        const nm=vk+' '+pname+' '+W+'x'+H;
        const texts=rc.ops.filter(o=>o.op==='text');
        ok(texts.length>0,nm+' draws some text');
        ok(rc.ops.filter(o=>o.op==='fill').length>0,nm+' draws something');
        let e=null;
        for(const t of texts){
          if(/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test(t.t)){ e='entity/tag "'+t.t.slice(0,40)+'"'; break; }
          if(/NaN|undefined|Infinity/.test(t.t)){ e='NaN "'+t.t.slice(0,40)+'"'; break; }
        }
        ok(!e,nm+' text ops clean'+(e?' ('+e+')':''));
        let off=null;
        for(const t of texts) if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ off='"'+t.t.slice(0,24)+'"'; break; }
        ok(!off,nm+' no text off the canvas'+(off?' '+off:''));
        let hit=null;
        for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
          const a=texts[i2].bb, b=texts[j2].bb;
          const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
          if(ox>0.5&&oy>0.5){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; }
        }
        ok(!hit,nm+' no text collisions ('+(hit||'ok')+')');
        /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner, and the
           display-list capture cannot see it because it is not canvas (wave-on-a-string) */
        const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
        ok(!inHint.length,nm+' nothing under the #hint line'
           +(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
        let leg=null;
        for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
          const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
          if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
          leg='a curve crosses the legend'; break;
        }
        ok(!leg,nm+' legend clear');
      }
    }
  }
  Object.assign(ST,stSave); Object.assign(TOOLS,JSON.parse(JSON.stringify(toolSave))); resetAll();

  /* ---------- M. the formatters ---------- */
  eq(supTxt(8),'⁸','supTxt turns 8 into a superscript eight');
  eq(supTxt(-7),'⁻⁷','and -7 into a superscript minus seven');
  eq(pow10(3),'10³','pow10(3) is the axis label 10^3');
  eq(pow10(-1),'10⁻¹','and pow10(-1) is 10^-1');
  eq(sciTxt(343,3),'343','an ordinary magnitude is left to sigf');
  eq(sciTxt(343,4),'343.0','which keeps the figures it was asked for');
  eq(sciTxt(1.9e-7,3),'1.90×10⁻⁷','a small one goes to the exponent form');
  eq(sciHTML(1.9e-7,3),'1.90&times;10<sup>-7</sup>','and sciHTML writes it as markup');
  eq(sciTxt(0,3),'0','zero is zero'); eq(sciHTML(1/0,3),'&infin;','and infinity says so');
  eq(plain('&lambda; = v/f'),'λ = v/f','plain() decodes the entities the canvas cannot');
  eq(plain('<b>p</b>&sub2;'.replace('&sub2;','&sup2;')),'p²','and strips the tags it cannot draw');

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
