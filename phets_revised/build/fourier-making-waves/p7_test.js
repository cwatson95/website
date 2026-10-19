
/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/fourier-making-waves/refvals.txt, the  *
 *  printed output of derive.py (scipy quadrature against the          *
 *  waveforms themselves, scipy.special.sici, numpy.fft, a Brent-      *
 *  refined peak scan), read in full through make_refs.py.             *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST), ampSave=AMPS.slice(), guessSave=GUESS.slice();
  function restore(){ Object.assign(ST,stSave); setAmps(ampSave); setGuess(guessSave); }
  /* a configuration: plain keys go into ST, _amps into AMPS */
  function withState(over,fn){
    const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    Object.assign(ST,DEFAULTS,clean);
    if(over._amps) setAmps(over._amps); else applyPreset();
    if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
      GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
      setGuess(over._guess||(over.showAns?GAME.answer:new Array(NMAX).fill(0))); }
    try{ return fn(); } finally{ restore(); }
  }
  const RNG=makeRng(20260922);
  function randAmps(){ const a=[]; for(let i=0;i<NMAX;i++) a.push(snapAmp(2*AMAX*(RNG()-0.5),A_STEP)); return a; }

  /* ---------- 0. the shared helpers cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(mix('#070b18',mix('#b8ec4c','#cd35c4',0.5),1)!=='rgb(0,0,0)','mix() output is a legal mix() input (not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,
       'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  ok(logTicks(0,10).length===0&&logTicks(-1,10).length===0,'logTicks refuses a non-positive bound (no infinite loop)');
  { const f=tickFmt([0,0.25,0.5]); eq(f(0.25),'0.25','tick labels follow the spacing'); eq(tickFmt([0,2,4])(4),'4','and 2 needs none'); }
  eq(logLab(0.001),'0.001','log labels are plain decimals (no superscript minus on the canvas)');
  eq(logLab(1),'1','log label at 1'); eq(logLab(1e-5),'1e-5','log label below 0.001');

  /* ---------- A. PhET's values, all read out of its build by derive.py ---------- */
  eq(NMAX,REF.MAX_HARMONICS,'11 harmonics (PhET\'s value, derive)');
  eq(AMAX,REF.MAX_AMPLITUDE,'amplitudes to +-1.5 (PhET\'s value, derive)');
  eq(A_STEP,REF.DISCRETE_AMPLITUDE_STEP,'the Discrete amplitude step is 0.05 (PhET\'s value, derive)');
  eq(G_STEP,REF.WAVE_GAME_AMPLITUDE_STEP,'the Wave Game amplitude step is 0.1 (PhET\'s value, derive)');
  eq(N_LEVELS,REF.N_GAME_LEVELS,'five game levels (PhET\'s value, derive)');
  eq(F1,REF.F1_Hz,'f1 = 440 Hz (PhET\'s value, derive)');
  eq(LWAVE,REF.L_m,'L = 1 m (PhET\'s value, derive)');
  rel(TPER,REF.T_ms,1e-15,'T = 1000/f1 ms (derive)');
  rel(K1,REF.k1_rad_per_m,1e-15,'k1 = 2 pi / L (derive)');
  rel(W1,REF.omega1_rad_per_ms,1e-15,'omega1 = 2 pi / T (derive)');
  eq(NPTS,1000,'1000 points per drawn curve (PhET\'s MAX_POINTS_PER_DATA_SET)');
  rel(WP_KMAX,REF.WP_KMAX,1e-15,'the wave-packet k range tops out at 24 pi (derive)');
  rel(WP_K0_DEF,REF.WP_K0_DEFAULT,1e-15,'default centre 12 pi (derive)');
  rel(WP_K0_MIN,REF.WP_K0_MIN,1e-15,'centre from 9 pi (derive)');
  rel(WP_K0_MAX,REF.WP_K0_MAX,1e-15,'centre to 15 pi (derive)');
  rel(WP_SK_DEF,REF.WP_SIGMA_DEFAULT,1e-15,'default width 3 pi (derive)');
  rel(WP_SK_MIN,REF.WP_SIGMA_MIN,1e-15,'width from pi (derive)');
  rel(WP_SK_MAX,REF.WP_SIGMA_MAX,1e-15,'width to 4 pi (derive)');
  for(let i=0;i<4;i++) rel(WP_SPACINGS[i],REF.WP_SPACINGS[i],1e-15,'component spacing '+i+' (derive)');
  ok(GAME_CONTROLS.join(',')==='2,3,5,6,11','PhET\'s default amplitude-control counts per level');
  /* this file's own constants, pinned against absolute numbers: a range that
     only ever appears through its own name cannot be caught any other way */
  eq(SPEC_NS,256,'the spectrum view samples 256 points of one period');
  close(PAIR_K1_MIN,0.4,1e-15,'the transform-pair spacing slider starts at 0.4 rad/m');
  close(PAIR_K1_MAX,TAU,1e-15,'... and ends at 2 pi, PhET\'s widest spacing');
  ok(PAIR_K1_MAX>WP_SPACINGS[3]&&PAIR_K1_MIN<WP_SPACINGS[1],
     'and it spans PhET\'s four fixed spacings');
  eq(HINT_H,18,'18 px are reserved at the canvas bottom for the HTML hint');
  rel(LWAVE/TPER,REF.wave_speed_m_per_ms,1e-15,'a harmonic travels L/T = 0.44 m per ms (derive)');

  /* ---------- B. the presets ARE the classic Fourier series ---------- */
  const PRE=[['square','sin','A_square_sin'],['square','cos','A_square_cos'],
             ['triangle','sin','A_triangle_sin'],['triangle','cos','A_triangle_cos'],
             ['sawtooth','sin','A_sawtooth_sin'],['wavePacket','sin','A_wavePacket_sin'],
             ['sinusoid','sin','A_sinusoid_sin']];
  for(const [nm,se,key] of PRE){
    const a=presetAmps(nm,se,NMAX), r=REF[key];
    let d=0; for(let n=0;n<NMAX;n++) d=Math.max(d,Math.abs(a[n]-r[n]));
    close(d,0,1e-15,nm+' ('+se+') matches the coefficients derive.py got from the waveform itself');
  }
  /* the same coefficients a second way: the projection integral, done by the
     trapezium rule on the ideal waveform.  A jump makes that O(1/ns) rather
     than exact, so the tolerance is the quadrature's, not the formula's. */
  /* the waveform is idealWave(nm, waveSe, .); the basis is trigOf(basisSe, .) —
     the two are separate on purpose, because projecting the sine waveform onto
     the cosine basis is exactly the test that it is odd */
  function projectIdeal(nm,waveSe,basisSe,n,ns){
    let s=0;
    for(let j=0;j<ns;j++){ const u=-PI+TAU*(j+0.5)/ns; s+=idealWave(nm,waveSe,u)*trigOf(basisSe,n*u); }
    return 2*s/ns;
  }
  for(const [nm,se] of [['square','sin'],['triangle','cos'],['sawtooth','sin'],['square','cos'],['triangle','sin']]){
    const a=presetAmps(nm,se,NMAX);
    /* 40000 midpoints, not 200000: the rule converges like 1/ns on a jump, so
       the tolerance is the QUADRATURE's 2e-4 and not the formula's -- and a
       wrong leading coefficient is out by tens of per cent, not by 2e-4 */
    let d=0; for(let n=1;n<=NMAX;n++) d=Math.max(d,Math.abs(a[n-1]-projectIdeal(nm,se,se,n,40000)));
    ok(d<2e-4,nm+' ('+se+') comes back out of its own waveform by quadrature ['+d.toExponential(2)+']');
    /* and the OTHER parity integrates to zero: that is what says the waveform has the symmetry */
    const other=se==='sin'?'cos':'sin';
    let z=0; for(let n=1;n<=NMAX;n++) z=Math.max(z,Math.abs(projectIdeal(nm,se,other,n,40000)));
    ok(z<2e-4,nm+' ('+se+'): its '+other+' coefficients vanish ['+z.toExponential(2)+']');
  }
  /* PhET's wave-packet table and the Gaussian it is */
  close(presetAmps('wavePacket','sin',10)[1],REF.wavepacket_gaussian_N10_n2,1e-15,
        'the wave packet preset is exp(-(n-c)^2/2 sigma^2), c = (N+1)/2, sigma = N/5 (derive)');
  ok(Math.abs(presetAmps('wavePacket','sin',10)[1]-REF.wavepacket_phet_typo_N10_n2)>9e-6,
     'and it differs from PhET\'s own table at N = 10, n = 2 — a transposed digit there, not here (derive)');
  close(REF.wavepacket_table_vs_gaussian,0,6e-7,'every other entry of PhET\'s table is that Gaussian to its printed precision (derive)');
  for(let N=1;N<=NMAX;N++){
    const a=presetAmps('wavePacket','sin',N);
    let sym=0; for(let i=0;i<N;i++) sym=Math.max(sym,Math.abs(a[i]-a[N-1-i]));
    close(sym,0,1e-15,'the wave packet preset is symmetric at N = '+N);
    if(N%2===1) close(a[(N-1)/2],1,1e-15,'... and peaks at exactly 1 for odd N = '+N);
  }
  eq(presetAllowsCos('sawtooth'),false,'PhET refuses a sawtooth built out of cosines');
  ok(presetAllowsCos('square')&&presetAllowsCos('triangle')&&presetAllowsCos('sinusoid'),'the others allow both');
  /* the sign patterns, one by one, so a wrong (-1)^k cannot hide */
  { const q=presetAmps('square','cos',NMAX);
    ok(q[0]>0&&q[2]<0&&q[4]>0&&q[6]<0&&q[8]>0&&q[10]<0,'square (cos): the signs alternate + - + - + -');
    const t=presetAmps('triangle','sin',NMAX);
    ok(t[0]>0&&t[2]<0&&t[4]>0&&t[6]<0&&t[8]>0&&t[10]<0,'triangle (sin): the signs alternate');
    const w=presetAmps('sawtooth','sin',NMAX);
    for(let n=1;n<=NMAX;n++) ok(w[n-1]*Math.pow(-1,n-1)>0,'sawtooth: term '+n+' has sign (-1)^(n-1)');
    for(let n=2;n<=NMAX;n+=2){ eq(presetAmps('square','sin',NMAX)[n-1],0,'square has no even harmonic '+n);
      eq(presetAmps('triangle','cos',NMAX)[n-1],0,'triangle has no even harmonic '+n); }
    ok(presetAmps('sawtooth','sin',NMAX)[1]!==0,'the sawtooth DOES have even harmonics');
  }
  /* idealWave is the waveform those coefficients belong to, checked away from
     the jumps where the series converges pointwise */
  for(const [nm,se] of [['square','sin'],['triangle','cos'],['sawtooth','sin'],['square','cos'],['triangle','sin'],['sinusoid','sin']]){
    const A=presetAmps(nm,se,2001);
    let d=0;
    for(const u of [0.4,1.1,-2.0,2.6,-0.77]){
      if(nm==='square'&&Math.min(Math.abs(u),Math.abs(Math.abs(u)-PI))<0.3) continue;
      d=Math.max(d,Math.abs(seriesSum(A,u,se,2001)-idealWave(nm,se,u)));
    }
    ok(d<0.01,nm+' ('+se+'): 2001 terms reproduce the waveform away from its jumps ['+d.toExponential(2)+']');
  }
  eq(idealWave('square','sin',0.5),1,'the square wave is +1 on the first half period');
  eq(idealWave('square','sin',-0.5),-1,'and -1 on the second');
  close(idealWave('triangle','cos',0),1,1e-15,'the cosine triangle peaks at 1 at u = 0');
  close(idealWave('triangle','sin',PI/2),1,1e-15,'the sine triangle peaks at 1 at u = pi/2');
  close(idealWave('sawtooth','sin',PI-1e-9),1,1e-8,'the sawtooth reaches +1 just before the jump');
  close(idealWave('sawtooth','sin',-PI+1e-9),-1,1e-8,'and -1 just after it');
  close(wrapPi(TAU+0.3),0.3,1e-12,'wrapPi folds a whole turn away');
  close(wrapPi(3*PI+0.3),0.3-PI,1e-12,'wrapPi folds into (-pi, pi]');
  close(wrapPi(-3*PI-0.3),PI-0.3,1e-12,'wrapPi is odd');
  close(wrapPi(PI-1e-9),PI-1e-9,1e-12,'wrapPi keeps a value just inside the interval');
  ok(!isFinite(idealWave('wavePacket','sin',1))&&!isFinite(idealWave('custom','sin',1)),
     'the wave packet and custom have no infinite-harmonics waveform (PhET draws none either)');
  ok(!hasIdeal('wavePacket')&&!hasIdeal('custom')&&hasIdeal('square'),'hasIdeal agrees');
  /* the exact mean squares of the complete waveforms */
  rel(idealMeanSquare('square'),REF.ms_square_exact,1e-15,'<f^2> = 1 for the square wave (derive)');
  rel(idealMeanSquare('triangle'),REF.ms_triangle_exact,1e-15,'<f^2> = 1/3 for the triangle (derive)');
  rel(idealMeanSquare('sawtooth'),REF.ms_sawtooth_exact,1e-15,'<f^2> = 1/3 for the sawtooth (derive)');
  eq(idealMeanSquare('sinusoid'),0.5,'<f^2> = 1/2 for a single sine');
  /* and those are the SUM of the closed forms, which is Parseval on the complete series */
  for(const [nm,se] of [['square','sin'],['triangle','cos'],['sawtooth','sin']]){
    rel(parseval(presetAmps(nm,se,200001),200001),idealMeanSquare(nm),3e-5,
        nm+': (1/2) sum over 200001 terms reaches <f^2>');
  }

  /* ---------- C. the series, the domains, Parseval ---------- */
  close(phaseOf('space',0.25,99),K1*0.25,1e-15,'space: u = 2 pi x / L, and t does not enter');
  close(phaseOf('time',99,0.7),W1*0.7,1e-15,'time: u = 2 pi t / T, and x does not enter');
  close(phaseOf('both',0.25,0.7),K1*0.25-W1*0.7,1e-15,'space & time: u = 2 pi (x/L - t/T)');
  /* the DRAWN abscissa: in the time domain it is t, and handing it to phaseOf
     as x drew a flat line in every time-domain view until the PNG showed it */
  close(phaseAt('time',0.7,99),W1*0.7,1e-15,'the time domain draws against t');
  close(phaseAt('space',0.25,99),K1*0.25,1e-15,'the space domain draws against x');
  close(phaseAt('both',0.25,0.7),K1*0.25-W1*0.7,1e-15,'space & time draws against x at the clock\'s t');
  for(const dm of ['space','time','both']) withState({view:'harm',preset:'square',domain:dm,t:0.3},()=>{
    const M=buildModel();
    let lo=Infinity,hi=-Infinity;
    for(const v of M.sum.ys){ lo=Math.min(lo,v); hi=Math.max(hi,v); }
    ok(hi-lo>1.5,'the '+dm+' domain draws a curve that actually varies ['+fmt(hi-lo,3)+']');
    let hlo=Infinity,hhi=-Infinity;
    for(const v of M.harms[0].ys){ hlo=Math.min(hlo,v); hhi=Math.max(hhi,v); }
    ok(hhi-hlo>2,'... and so does its fundamental ['+fmt(hhi-hlo,3)+']');
    /* the drawn window holds exactly two periods of the fundamental */
    close(M.sum.ys[0],M.sum.ys[NPTS],1e-12,'the '+dm+' window is a whole number of periods');
  });
  close(phaseOf('both',0.25+LWAVE,0.7+TPER),phaseOf('both',0.25,0.7),1e-13,'one wavelength in x and one period in t is the same phase');
  { const A=presetAmps('square','sin',NMAX);
    const v=[0.1,0.25,0.37].map(x=>seriesSum(A,phaseOf('space',x,0),'sin',NMAX));
    for(let i=0;i<3;i++) rel(v[i],REF.sum_square_sin[i],1e-13,'the square sum at x = '+[0.1,0.25,0.37][i]+' m (derive)'); }
  { const A=presetAmps('triangle','cos',NMAX);
    const v=[0,0.13].map(x=>seriesSum(A,phaseOf('space',x,0),'cos',NMAX));
    for(let i=0;i<2;i++) rel(v[i],REF.sum_triangle_cos[i],1e-13,'the triangle sum at x = '+[0,0.13][i]+' m (derive)'); }
  { const A=presetAmps('sawtooth','sin',NMAX);
    const v=[0.2,-0.45].map(x=>seriesSum(A,phaseOf('space',x,0),'sin',NMAX));
    for(let i=0;i<2;i++) rel(v[i],REF.sum_sawtooth_sin[i],1e-13,'the sawtooth sum at x = '+[0.2,-0.45][i]+' m (derive)'); }
  { const A=presetAmps('square','sin',NMAX);
    const v=[0.1,0.25].map(x=>seriesSum(A,phaseOf('both',x,0.7),'sin',NMAX));
    for(let i=0;i<2;i++) rel(v[i],REF.sum_square_xt_t0p7[i],1e-13,'the travelling square sum at t = 0.7 ms (derive)'); }
  /* the space & time sum really travels at L/T, and nowhere else */
  { const A=presetAmps('triangle','sin',NMAX), dt=0.31, dx=(LWAVE/TPER)*dt;
    let d=0;
    for(const x of [-0.4,0,0.17,0.62]) d=Math.max(d,Math.abs(seriesSum(A,phaseOf('both',x+dx,dt),'sin',NMAX)-seriesSum(A,phaseOf('both',x,0),'sin',NMAX)));
    close(d,0,1e-13,'the pattern moves exactly L/T metres per ms'); }
  /* Parseval, both ways, for the presets and for random amplitudes */
  let worstP=0;
  for(const [nm,se] of [['square','sin'],['square','cos'],['triangle','sin'],['triangle','cos'],['sawtooth','sin'],['wavePacket','sin'],['sinusoid','sin']]){
    const A=presetAmps(nm,se,NMAX);
    const d=Math.abs(parseval(A,NMAX)-meanSquareNumeric(A,se,64,NMAX));
    worstP=Math.max(worstP,d);
    ok(d<1e-13,'Parseval holds for '+nm+' ('+se+') ['+d.toExponential(2)+']');
  }
  for(let k=0;k<8;k++){
    const A=randAmps();
    for(const se of ['sin','cos']){
      const d=Math.abs(parseval(A,NMAX)-meanSquareNumeric(A,se,64,NMAX));
      worstP=Math.max(worstP,d);
      ok(d<1e-13,'Parseval holds for random amplitudes '+k+' ('+se+') ['+d.toExponential(2)+']');
    }
  }
  ok(worstP<1e-13,'Parseval residual over every case is '+worstP.toExponential(2));
  { const A=REF.parseval_random_A;
    rel(parseval(A,NMAX),REF.parseval_random_ms,1e-15,'Parseval on derive.py\'s own random amplitudes (derive)'); }
  /* the trapezium rule is EXACT here, so more samples change nothing */
  { const A=randAmps();
    close(meanSquareNumeric(A,'sin',32,NMAX),meanSquareNumeric(A,'sin',4096,NMAX),1e-14,
          '32 samples and 4096 give the same mean square: the quadrature is exact, not converged');
    ok(Math.abs(meanSquareNumeric(A,'sin',16,NMAX)-parseval(A,NMAX))>1e-6,
       '... and 16 samples (below 2N) do NOT, which is what says the bound matters'); }

  /* ---------- D. Gibbs ---------- */
  rel(GIBBS_PEAK,REF.gibbs_peak,1e-15,'(2/pi) Si(pi) (derive, scipy.special.sici)');
  rel(GIBBS_FRACTION,REF.gibbs_fraction_of_jump,1e-15,'the Wilbraham-Gibbs constant, 8.9490 % of the jump (derive)');
  close(GIBBS_FRACTION,(GIBBS_PEAK-1)/2,1e-15,'... which is (peak - 1) / jump with jump = 2');
  for(const [M,key] of [[1,'gibbs_peak_M1'],[2,'gibbs_peak_M2'],[6,'gibbs_peak_M6'],[50,'gibbs_peak_M50'],[400,'gibbs_peak_M400']]){
    rel(squarePeakClosed(M).val,REF[key],1e-14,'the square wave peak at M = '+M+' (derive)');
    close(squarePeakClosed(M).u,PI/(2*M),1e-15,'... at u = pi/2M');
  }
  rel(squarePeakClosed(6).u/TAU,REF.gibbs_x_M6_over_L,1e-15,'x = L/4M at 11 harmonics (derive)');
  eq(oddCount(11),6,'keeping harmonics 1..11 keeps six odd ones');
  eq(oddCount(12),6,'and 1..12 keeps the same six');
  eq(oddCount(1),1,'1..1 keeps one');
  ok(peakWindow('square')[1]===PI/2&&peakWindow('sawtooth')[0]===PI/2&&peakWindow('triangle')[1]===PI,
     'the peak is looked for next to the jump, not over the whole half period');
  /* the closed form is checked against a MEASURED peak of the same partial sum */
  for(const M of [1,2,3,6,12,40]){
    const A=presetAmps('square','sin',2*M);
    const w=peakWindow('square');
    const p=peakOf(u=>seriesSum(A,u,'sin',2*M),w[0],w[1],6000);
    const c=squarePeakClosed(M);
    ok(Math.abs(p.val-c.val)<3e-8,'M = '+M+': the measured peak finds the closed form ['+Math.abs(p.val-c.val).toExponential(2)+']');
    ok(Math.abs(p.u-c.u)<2e-3,'M = '+M+': and its position ['+Math.abs(p.u-c.u).toExponential(2)+']');
  }
  /* the partial sum really is symmetric about pi/2, which is WHY the window
     matters: a scan of the whole half period finds the mirror as often as the ear */
  { const A=presetAmps('square','sin',12);
    let d=0; for(let j=1;j<40;j++){ const u=PI*j/40; d=Math.max(d,Math.abs(seriesSum(A,u,'sin',12)-seriesSum(A,PI-u,'sin',12))); }
    close(d,0,1e-13,'a square wave partial sum is symmetric about u = pi/2 (only odd harmonics)');
    const wide=peakOf(u=>seriesSum(A,u,'sin',12),1e-9,PI-1e-9,6000);
    ok(Math.abs(wide.u-squarePeakClosed(6).u)>1,'... and a whole-half-period scan does land on the mirror'); }
  /* a grid with NO refinement would be much worse: that is what the parabola buys */
  { const A=presetAmps('square','sin',12), c=squarePeakClosed(6);
    let bv=-Infinity;
    for(let j=0;j<=200;j++){ const v=seriesSum(A,1e-9+(PI/2-2e-9)*j/200,'sin',12); if(v>bv) bv=v; }
    const raw=Math.abs(bv-c.val), ref=Math.abs(peakOf(u=>seriesSum(A,u,'sin',12),1e-9,PI/2,200).val-c.val);
    ok(ref<raw/4,'the parabola refinement beats the raw grid argmax by more than 4x ['+raw.toExponential(2)+' vs '+ref.toExponential(2)+']'); }
  /* the approach to the limit is O(1/M^2) */
  { const e=M=>squarePeakClosed(M).val-GIBBS_PEAK;
    rel(e(6)/e(12),REF.gibbs_err_ratio_6_12,1e-9,'the peak approaches the limit as 1/M^2 (derive)');
    ok(Math.abs(e(12)/e(24)-4)<0.02,'... and again between 12 and 24'); }
  ok(squarePeakClosed(400).val>GIBBS_PEAK&&squarePeakClosed(400).val-GIBBS_PEAK<1e-5,
     'at M = 400 the peak is still above the limit, by 1e-6, not zero: the overshoot does not die');
  /* the triangle is continuous, so it never overshoots at all */
  { const A=presetAmps('triangle','cos',41);
    let m=0; for(let j=0;j<=4000;j++) m=Math.max(m,Math.abs(seriesSum(A,PI*j/4000,'cos',41)));
    rel(m,REF.triangle_partial_max_41,1e-12,'the triangle partial sum stays below 1 (derive)');
    ok(m<1,'... strictly below: no Gibbs without a jump'); }
  /* the sawtooth's jump is 2 as well, and shows the same fraction */
  { const w=peakWindow('sawtooth');
    const A=presetAmps('sawtooth','sin',11);
    const p=peakOf(u=>seriesSum(A,u,'sin',11),w[0],w[1],8000);
    rel(p.val,REF.saw_peak_N11,1e-8,'the sawtooth peak at 11 terms (derive)');
    close(p.u,PI*11/12,1e-3,'... at u = pi N/(N+1), the last extremum before the jump');
    const B=presetAmps('sawtooth','sin',1000);
    const q=peakOf(u=>seriesSum(B,u,'sin',1000),w[0],w[1],12000);
    rel(q.val,REF.saw_peak_N1000,1e-6,'and at 1000 terms (derive)');
    ok(Math.abs((q.val-1)/2-GIBBS_FRACTION)<0.001,'... which is the same Wilbraham-Gibbs fraction'); }

  /* ---------- E. truncation ---------- */
  /* the tolerance is 1e-11, not 1e-13: <f^2> - (1/2)sum A^2 is a subtraction of
     nearly equal numbers for the triangle (1/3 against 0.333302), so the
     cancellation, not the formula, sets the last two digits */
  rel(truncationRms('square','sin',11),REF.l2_square_N11,1e-13,'rms error of the 11-term square (derive)');
  rel(truncationRms('triangle','cos',11),REF.l2_triangle_N11,1e-11,'rms error of the 11-term triangle (derive)');
  rel(truncationRms('sawtooth','sin',11),REF.l2_sawtooth_N11,1e-13,'rms error of the 11-term sawtooth (derive)');
  for(const [nm,se] of [['square','sin'],['triangle','cos'],['sawtooth','sin']]){
    let prev=Infinity;
    for(let N=1;N<=60;N++){
      const e=truncationRms(nm,se,N), A=presetAmps(nm,se,N);
      ok(e<=prev,nm+': the rms error never rises at N = '+N);
      /* it falls STRICTLY exactly when the new harmonic carries something --
         a square wave gains nothing at even N, and that is not a failure */
      if(A[N-1]!==0) ok(e<prev,nm+': and falls strictly at N = '+N+', where A_N is not zero');
      prev=e;
    }
    ok(truncationRms(nm,se,4000)<0.02,nm+': and goes to zero');
  }
  /* the same number the slow way: <f^2> minus the captured power, by quadrature */
  { const A=presetAmps('square','sin',11);
    const direct=Math.sqrt(idealMeanSquare('square')-meanSquareNumeric(A,'sin',64,11));
    rel(direct,truncationRms('square','sin',11),1e-13,'the truncation error is <f^2> less the captured power, either way'); }

  /* ---------- F. analysis ---------- */
  { let worstF=0, worstD=0;
    for(let k=0;k<6;k++){
      const A=randAmps();
      for(const se of ['sin','cos']){
        const y=sampleSeries(A,se,SPEC_NS,NMAX);
        const f=analyseFFT(y,NMAX,se), d=analyseDirect(y,NMAX,se);
        for(let n=0;n<NMAX;n++){ worstF=Math.max(worstF,Math.abs(f[n]-A[n])); worstD=Math.max(worstD,Math.abs(f[n]-d[n])); }
      }
    }
    ok(worstF<1e-13,'the FFT returns the amplitudes it was given ['+worstF.toExponential(2)+']');
    ok(worstD<1e-13,'the FFT agrees with the direct DFT it is a fast version of ['+worstD.toExponential(2)+']'); }
  { const A=REF.analysis_A.slice(0,NMAX);
    eq(SPEC_NS,REF.analysis_NS,'256 samples of one period (derive)');
    for(const se of ['sin','cos']){
      const y=sampleSeries(A,se,SPEC_NS,NMAX), f=analyseFFT(y,NMAX,se);
      let d=0; for(let n=0;n<NMAX;n++) d=Math.max(d,Math.abs(f[n]-A[n]));
      ok(d<1e-13,'derive.py\'s own amplitudes come back out of the '+se+' waveform ['+d.toExponential(2)+']'); } }
  { let threw=false; try{ fftRadix2([1,2,3],[0,0,0]); }catch(e){ threw=true; }
    ok(threw,'fftRadix2 throws on a length that is not a power of two rather than returning nonsense');
    threw=false; try{ fftRadix2([1,2],[0]); }catch(e){ threw=true; }
    ok(threw,'... and on mismatched real and imaginary parts'); }
  { /* the FFT against a hand-written DFT of a signal that is NOT a series sum */
    const n=32, re=[], im=[];
    for(let j=0;j<n;j++){ re.push(Math.sin(3.1*j)+0.3*j/n); im.push(0); }
    const R=re.slice(), I=im.slice();
    fftRadix2(R,I);
    let d=0;
    for(let n2=0;n2<n;n2++){
      let sr=0,si=0;
      for(let j=0;j<n;j++){ const a=-TAU*n2*j/n; sr+=re[j]*Math.cos(a); si+=re[j]*Math.sin(a); }
      d=Math.max(d,Math.abs(sr-R[n2]),Math.abs(si-I[n2]));
    }
    ok(d<1e-12,'the radix-2 FFT equals the O(N^2) DFT on an arbitrary signal ['+d.toExponential(2)+']'); }
  { /* a cosine has real coefficients and a sine imaginary ones: the sign convention */
    const y=sampleSeries([0,0,1,0,0,0,0,0,0,0,0],'sin',64,NMAX);
    const f=analyseFFT(y,NMAX,'sin');
    close(f[2],1,1e-13,'a pure third sine is recovered with amplitude +1 (the Im sign is right)');
    const y2=sampleSeries([0,0,1,0,0,0,0,0,0,0,0],'cos',64,NMAX);
    close(analyseFFT(y2,NMAX,'cos')[2],1,1e-13,'and a pure third cosine likewise'); }

  /* ---------- G. the wave packet ---------- */
  rel(wpAmp(WP_K0_DEF,WP_K0_DEF,WP_SK_DEF),REF.wp_Ak_at_k0,1e-14,'A(k0) = 1/(sigma sqrt(2 pi)) (derive)');
  close(wpAmp(WP_K0_DEF+WP_SK_DEF,WP_K0_DEF,WP_SK_DEF)/wpAmp(WP_K0_DEF,WP_K0_DEF,WP_SK_DEF),Math.exp(-0.5),1e-15,
        'A falls to 1/sqrt(e) one standard deviation out');
  rel(wpContinuous(0,WP_K0_DEF,WP_SK_DEF,'cos'),REF.wp_F0,1e-15,'the packet is 1 at the origin (derive)');
  rel(wpContinuous(0.12,WP_K0_DEF,WP_SK_DEF,'cos'),REF.wp_F_0p12,1e-13,'the packet at x = 0.12 m (derive)');
  rel(1/WP_SK_DEF,REF.wp_sigma_x,1e-15,'sigma_x = 1/sigma_k (derive)');
  close((1/WP_SK_DEF)*WP_SK_DEF,REF.wp_uncertainty_product,1e-15,'sigma_x sigma_k = 1 exactly (derive)');
  rel(wpEnvelopeContinuous(1/WP_SK_DEF,WP_SK_DEF),REF.wp_envelope_at_sigma_x,1e-15,'the envelope is 1/sqrt(e) at x = sigma_x (derive)');
  rel(2/WP_SK_DEF,REF.wp_width_indicator,1e-15,'the width marker spans 2 sigma_x (derive)');
  eq(wpComponentCount(PI),REF.wp_n_components_pi,'floor(24 pi / k1) + 1 components at k1 = pi (derive)');
  eq(wpComponentCount(PI/4),REF.wp_n_components_pi_over_4,'... and at k1 = pi/4 (derive)');
  eq(wpComponentCount(0),Infinity,'a spacing of zero means infinitely many');
  { const c=wpComponents(PI,WP_K0_DEF,WP_SK_DEF);
    let s=0,m=0; for(const q of c){ s+=q.a; m=Math.max(m,q.a); }
    rel(s,REF.wp_amp_sum_pi,1e-13,'the plotted amplitudes sum to 1 to the tail (derive)');
    rel(m,REF.wp_amp_peak_pi,1e-13,'the tallest plotted amplitude at k1 = pi (derive)');
    close(c[0].k,0,1e-15,'the first component sits at k = 0');
    close(c[c.length-1].k,PI*(REF.wp_n_components_pi-1),1e-12,'and the last below 24 pi'); }
  /* the exact transform: quadrature over the whole line, in JS */
  { let d=0;
    for(const x of [0,0.037,0.12,-0.25,0.4]) for(const se of ['cos','sin']){
      const lo=WP_K0_DEF-12*WP_SK_DEF, hi=WP_K0_DEF+12*WP_SK_DEF, n=200000;
      let s=0;
      for(let j=0;j<n;j++){ const k=lo+(hi-lo)*(j+0.5)/n; s+=wpAmp(k,WP_K0_DEF,WP_SK_DEF)*trigOf(se,k*x); }
      s*=(hi-lo)/n;
      d=Math.max(d,Math.abs(s-wpContinuous(x,WP_K0_DEF,WP_SK_DEF,se)));
    }
    ok(d<1e-12,'exp(-sigma^2 x^2/2) cos(k0 x) IS the transform of A(k) ['+d.toExponential(2)+']'); }
  /* Poisson: the two-sided discrete sum is the periodised continuous packet */
  { let d=0;
    for(const k1 of [PI,PI/2,PI/4,TAU]) for(const x of [0,0.07,0.31,-0.5]) for(const se of ['cos','sin'])
      d=Math.max(d,Math.abs(wpDiscreteTwoSided(x,k1,WP_K0_DEF,WP_SK_DEF,se)-wpPeriodised(x,k1,WP_K0_DEF,WP_SK_DEF,se,8)));
    ok(d<1e-12,'Poisson: the two-sided sum is the packet repeated every lambda1 ['+d.toExponential(2)+']');
    ok(REF.wp_poisson_residual<1e-12,'... and derive.py found the same in Python (derive)'); }
  /* the truncated one-sided sum is exactly periodic */
  { let d=0;
    for(const k1 of [PI,PI/2,PI/4]){
      const c=wpComponents(k1,WP_K0_DEF,WP_SK_DEF), lam=TAU/k1;
      for(const x of [0,0.13,-0.4]) d=Math.max(d,Math.abs(wpDiscrete(x+lam,c,'cos')-wpDiscrete(x,c,'cos')));
    }
    ok(d<1e-12,'every k_n is a multiple of k1, so the sum repeats every lambda1 exactly ['+d.toExponential(2)+']'); }
  /* what separates PhET's sum from the continuous packet is the Gaussian tail */
  rel(wpTailBound(WP_K0_DEF,WP_SK_DEF),REF.wp_tail_bound,2e-6,'the erfc tail bound at the defaults (derive)');
  { const c=wpComponents(PI/4,WP_K0_DEF,WP_SK_DEF);
    let d=0;
    for(let j=0;j<=200;j++){ const x=-0.4+0.8*j/200; d=Math.max(d,Math.abs(wpDiscrete(x,c,'cos')-wpContinuous(x,WP_K0_DEF,WP_SK_DEF,'cos'))); }
    rel(d,REF.wp_truncation_residual,1e-6,'the measured difference inside one period (derive)');
    ok(d<wpTailBound(WP_K0_DEF,WP_SK_DEF),'... and it is under the bound'); }
  /* the copies are full height where they sit, which is the whole point */
  { const k1=PI, c=wpComponents(k1,WP_K0_DEF,WP_SK_DEF), lam=TAU/k1;
    close(wpDiscrete(lam,c,'cos'),wpDiscrete(0,c,'cos'),1e-12,'the copy at x = lambda1 is as tall as the packet at 0');
    ok(Math.abs(wpContinuous(lam,WP_K0_DEF,WP_SK_DEF,'cos'))<1e-40,'while the continuous packet there is nothing at all');
    close(REF.wp_conv_errs_window3[0],1,1e-4,'so on a 3 m window the difference is the full height 1 (derive)');
    ok(REF.wp_conv_errs_window3[2]<1e-4,'and at a quarter of the spacing the copies have left the window (derive)'); }
  /* the envelope of the discrete sum */
  { const c=wpComponents(PI/4,WP_K0_DEF,WP_SK_DEF);
    let d=0;
    for(let j=0;j<=100;j++){ const x=-0.5+j/100; d=Math.max(d,Math.abs(wpEnvelopeDiscrete(x,c)-wpEnvelopeContinuous(x,WP_SK_DEF))); }
    ok(d<2e-4,'the discrete envelope is the Gaussian envelope ['+d.toExponential(2)+']');
    for(let j=0;j<=40;j++){ const x=-0.5+j/40;
      ok(wpEnvelopeDiscrete(x,c)>=Math.abs(wpDiscrete(x,c,'cos'))-1e-12,'the envelope is never below the wave at x = '+fmt(x,3)); } }
  /* erfcApprox, the one approximation in the file, against known values */
  close(erfcApprox(0),1,1e-7,'erfc(0) = 1');
  close(erfcApprox(1),0.15729920705028513,2e-7,'erfc(1)');
  close(erfcApprox(2),0.004677734981047266,2e-9,'erfc(2)');
  close(erfcApprox(-1),2-0.15729920705028513,2e-7,'erfc(-x) = 2 - erfc(x)');
  close(erfcApprox(4),1.541725790028002e-8,2e-14,'erfc(4)');

  /* ---------- H. the wave game ---------- */
  eq(GAME_CONTROLS.length,N_LEVELS,'one control count per level');
  { const seen={};
    for(let s=1;s<=40;s++) for(let L=1;L<=N_LEVELS;L++){
      const a=gameAmplitudes(L,s*7919+L*104729);
      eq(a.length,NMAX,'a challenge has eleven amplitudes');
      const nz=nonZeroCount(a);
      if(L<N_LEVELS) eq(nz,L,'level '+L+' uses exactly '+L+' harmonics');
      else ok(nz>=5&&nz<=NMAX,'level 5 uses five or more (got '+nz+')');
      for(const v of a){
        ok(Math.abs(v)<=AMAX+1e-12,'every amplitude is inside PhET\'s range');
        ok(Math.abs(v/G_STEP-Math.round(v/G_STEP))<1e-9,'every amplitude is a multiple of '+G_STEP);
      }
      seen[a.join(',')]=(seen[a.join(',')]||0)+1;
    }
    ok(Object.keys(seen).length>150,'the generator does not keep returning the same challenge ('+Object.keys(seen).length+' distinct)'); }
  { const a=gameAmplitudes(3,12345), b=gameAmplitudes(3,12345);
    ok(a.join(',')===b.join(','),'a seed reproduces its challenge exactly');
    ok(gameAmplitudes(3,12346).join(',')!==a.join(','),'and a different seed does not'); }
  eq(REF.game_alphabet_size,30,'thirty legal amplitudes: 0.1 to 1.5 either way, zero excluded (derive)');
  { const A=gameAmplitudes(4,777), B=A.slice();
    ok(gameMatches(A,B),'an exact match is a match');
    B[0]+=1e-9;
    ok(!gameMatches(A,B),'and a difference of 1e-9 is not — PhET checks for equality, not closeness'); }
  eq(gameHarmonicCount(1,()=>0.5),1,'level 1 wants one harmonic');
  eq(gameHarmonicCount(4,()=>0.5),4,'level 4 wants four');
  eq(gameHarmonicCount(5,()=>0),5,'level 5 wants at least five');
  eq(gameHarmonicCount(5,()=>0.999),NMAX,'... and at most eleven');

  /* ---------- I. the controls' arithmetic ---------- */
  close(snapAmp(0.37,A_STEP),0.35,1e-12,'the discrete step snaps 0.37 to 0.35');
  close(snapAmp(0.37,G_STEP),0.4,1e-12,'the game step snaps 0.37 to 0.4');
  close(snapAmp(99,A_STEP),AMAX,1e-12,'and everything is clamped to +-1.5');
  close(snapAmp(-99,A_STEP),-AMAX,1e-12,'at the bottom too');
  close(caliperWidth('space',1),LWAVE,1e-15,'the caliper is L wide for the fundamental');
  close(caliperWidth('space',7),LWAVE/7,1e-15,'and L/7 for the seventh');
  close(caliperWidth('time',4),TPER/4,1e-15,'in the time domain it is T/n');
  { const b=box(100,100,300,200);
    close(barA(b,barY(b,0.65,AMAX),AMAX),0.65,1e-12,'the bar geometry inverts itself');
    close(barA(b,barY(b,-1.2,AMAX),AMAX),-1.2,1e-12,'... below the axis too');
    eq(barHit(b,barX(b,4,11),150,11),4,'a hit on the fourth bar finds the fourth harmonic');
    eq(barHit(b,barX(b,11,11),150,11),11,'and on the eleventh');
    eq(barHit(b,50,150,11),0,'a miss finds nothing'); }

  /* ---------- J. every view draws, cleanly, at every size ---------- */
  const SIZES=[[1400,820],[1100,700],[860,560]];
  const CONFIGS=[
    ['harmonics sine square',{view:'harm',preset:'square',series:'sin',N:11},55],
    ['harmonics cosine triangle',{view:'harm',preset:'triangle',series:'cos',N:7,showInf:true},48],
    ['harmonics sawtooth, time',{view:'harm',preset:'sawtooth',domain:'time',N:11,caliper:true,sel:3},62],
    ['harmonics space & time',{view:'harm',preset:'square',domain:'both',t:0.7,N:5},38],
    ['harmonics one harmonic',{view:'harm',preset:'sinusoid',N:1,showHarm:false},26],
    ['harmonics all zero',{view:'harm',preset:'custom',_amps:new Array(NMAX).fill(0)},52],
    ['harmonics wave packet',{view:'harm',preset:'wavePacket',N:11,showInf:true},58],
    ['convergence square M=6',{view:'conv',convPre:'square',convM:6},42],
    ['convergence square M=1',{view:'conv',convPre:'square',convM:1},40],
    ['convergence square M=128',{view:'conv',convPre:'square',convM:128},42],
    ['convergence triangle',{view:'conv',convPre:'triangle',series:'cos',convM:9},40],
    ['convergence sawtooth',{view:'conv',convPre:'sawtooth',convM:20},40],
    ['convergence sinusoid',{view:'conv',convPre:'sinusoid',convM:3},40],
    ['spectrum square',{view:'spec',preset:'square',N:11},85],
    ['spectrum single sine',{view:'spec',preset:'sinusoid',N:11},86],
    ['spectrum all zero',{view:'spec',preset:'custom',_amps:new Array(NMAX).fill(0)},86],
    ['game level 1',{view:'game',level:1,seed:3,_game:1},46],
    ['game level 5 solved',{view:'game',level:5,seed:9,_game:1,showAns:true},52],
    ['packet default',{view:'pack'},68],
    ['packet continuous',{view:'pack',wpSp:0},36],
    ['packet narrow spacing',{view:'pack',wpSp:1,wpSk:WP_SK_MAX,wpK0:WP_K0_MAX},177],
    ['packet widest packet',{view:'pack',wpSp:3,wpSk:WP_SK_MIN,wpK0:WP_K0_MIN,wpEnv:false,wpWid:false},53],
    ['packet in time',{view:'pack',wpDom:'time'},68],
    ['transform pair default',{view:'pair'},27],
    ['transform pair coarse',{view:'pair',pairK1:PAIR_K1_MAX,pairSk:WP_SK_MIN},30],
    ['transform pair fine',{view:'pair',pairK1:PAIR_K1_MIN,pairSk:WP_SK_MAX},29],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,minFills] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      let M=null;
      try{ M=buildModel(); drawView(c,W,H,M); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text');
      /* the floor counts fills AND strokes: several views here are almost all
         curves, so a fills-only floor is either useless or unmeetable */
      const marks=c.ops.filter(o=>o.op==='fill'||o.op==='stroke').length;
      ok(marks>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance ('+marks+' marks, floor '+minFills+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb;
        const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length&&!leg;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
      /* the readout, the equation bar and the tag are built from the same model */
      const ro=readoutHTML(M), eqb=eqbarHTML(M), tg=tagHTML(M);
      ok(ro.length>200&&!/NaN|undefined/.test(ro),nm+' readout builds clean');
      ok(eqb.length>60&&!/NaN|undefined/.test(eqb),nm+' equation bar builds clean');
      ok(tg.length>10&&!/NaN|undefined/.test(tg),nm+' tag builds clean');
    });
  }

  /* ---------- K. no slider combination produces a non-finite anything ---------- */
  { let bad=0, n=0;
    for(const preset of ['sinusoid','triangle','square','sawtooth','wavePacket'])
      for(const series of ['sin','cos'])
        for(const domain of ['space','time','both'])
          for(const N of [1,4,11]){
            n++;
            const A=presetAmps(preset,series,N);
            for(let j=0;j<=40;j++){
              const x=-1+2*j/40;
              if(!isFinite(seriesSum(A,phaseOf(domain,x,0.31),series,N))) bad++;
            }
            if(!isFinite(parseval(A,N))) bad++;
          }
    eq(bad,0,'every waveform x series x domain x N is finite everywhere ('+n+' combinations)'); }
  { let bad=0, n=0;
    for(let i=0;i<=12;i++) for(let j=0;j<=12;j++) for(const sp of [0,1,2,3]){
      const k0=WP_K0_MIN+(WP_K0_MAX-WP_K0_MIN)*i/12, sk=WP_SK_MIN+(WP_SK_MAX-WP_SK_MIN)*j/12;
      n++;
      const c=wpComponents(WP_SPACINGS[sp],k0,sk);
      for(const q of c) if(!isFinite(q.a)||!isFinite(q.k)) bad++;
      for(const x of [-2,-0.3,0,0.7,2]){
        if(!isFinite(wpDiscrete(x,c,'cos'))) bad++;
        if(!isFinite(wpContinuous(x,k0,sk,'cos'))) bad++;
        if(c.length&&!isFinite(wpEnvelopeDiscrete(x,c))) bad++;
      }
      if(!isFinite(wpTailBound(k0,sk))) bad++;
    }
    eq(bad,0,'every wave-packet slider combination is finite ('+n+' combinations)'); }
  { let bad=0;
    for(let M=1;M<=128;M++){
      const p=squarePeakClosed(M);
      if(!isFinite(p.val)||!isFinite(p.u)) bad++;
      for(const nm of ['square','triangle','sawtooth','sinusoid'])
        for(const se of ['sin','cos']){
          if(nm==='sawtooth'&&se==='cos') continue;
          if(!isFinite(truncationRms(nm,se,M))) bad++;
        }
    }
    eq(bad,0,'every M from 1 to 128 gives finite peaks and errors'); }

  /* ---------- L. the pointer really moves the amplitudes ---------- */
  withState({view:'harm',preset:'square',series:'sin',N:11},()=>{
    const S2=makeScene({getContext:()=>makeShot(1400,820)});
    S2.W=1400; S2.H=820;
    S2.draw();
    ok(GEO.view==='harm'&&!!GEO.bars,'the harmonics view records its bar panel for the pointer');
    const b=GEO.bars, before=AMPS[4];
    const moved=S2.pointer('down',barX(b,5,11),barY(b,0.7,AMAX));
    ok(moved,'a press on the fifth bar changes something');
    close(AMPS[4],0.7,A_STEP/2+1e-12,'... and it is the fifth amplitude, snapped to the step');
    ok(AMPS[4]!==before,'the amplitude really changed');
    eq(ST.sel,5,'the fifth harmonic becomes the selected one');
    eq(ST.preset,'custom','editing by hand makes the waveform custom, as in PhET');
    S2.pointer('move',barX(b,5,11),barY(b,-1.2,AMAX));
    close(AMPS[4],-1.2,A_STEP/2+1e-12,'dragging carries the amplitude with it');
    ok(S2.pointer('up',0,0),'the release ends the drag');
    ok(!S2.pointer('move',barX(b,5,11),barY(b,0.2,AMAX)),'and a move after the release does nothing');
    /* the drag is clamped to PhET's range, not allowed to run off */
    S2.pointer('down',barX(b,2,11),b.y+0.5);
    close(AMPS[1],AMAX,1e-12,'a press at the top of the panel pins the amplitude at +1.5');
    S2.pointer('move',barX(b,2,11),b.y1+200);
    close(AMPS[1],-AMAX,1e-12,'and a drag far below it at -1.5');
    S2.pointer('up',0,0);
    ok(!S2.pointer('down',barX(b,2,11),b.y-200),'a press well above the panel grabs nothing at all');
  });
  withState({view:'harm',preset:'square',caliper:true},()=>{
    const S2=makeScene({getContext:()=>makeShot(1400,820)});
    S2.W=1400; S2.H=820; S2.draw();
    const b=GEO.sum, x0=ST.calX;
    ok(!!b,'the harmonics view records its sum panel');
    ok(S2.pointer('down',b.x+0.7*b.w,(b.y+b.y1)/2),'a press on the sum panel grabs the caliper');
    ok(ST.calX!==x0,'and moves it');
    close(ST.calX,GEO.xa+(GEO.xb-GEO.xa)*0.7,1e-9,'to where the pointer is');
    S2.pointer('up',0,0);
  });
  withState({view:'game',level:2,seed:5,_game:1},()=>{
    const S2=makeScene({getContext:()=>makeShot(1400,820)});
    S2.W=1400; S2.H=820; S2.draw();
    const b=GEO.bars, keep=AMPS.slice();
    S2.pointer('down',barX(b,3,NMAX),barY(b,0.73,AMAX));
    close(GUESS[2],0.7,1e-12,'in the game the bars snap to the 0.1 step, not 0.05');
    eq(ST.preset,DEFAULTS.preset,'and the game does not touch the Discrete waveform');
    eq(AMPS.join(','),keep.join(','),'... nor its amplitudes: the guess is its own array');
    S2.pointer('up',0,0);
  });
  /* the two arrays really are separate, in both directions */
  withState({view:'harm',preset:'square'},()=>{
    const keep=GUESS.slice();
    AMPS[0]=0.25;
    eq(GUESS.join(','),keep.join(','),'editing the Discrete series leaves the guess alone');
    eq(ampArray()[0],0.25,'ampArray picks the Discrete series outside the game');
  });
  withState({view:'game',level:1,seed:2,_game:1},()=>{
    eq(ampArray(),GUESS,'and the guess inside it');
  });
  /* the clock: PhET's step button is 0.05 ms and its play runs 1 ms of model
     time per second of real time, and BOTH only in the space & time domain.
     (Mutation sweep: the 0.05 survived the physics suite until this was added,
     because only the UI drive ever pressed the button.) */
  withState({view:'harm',domain:'both',running:false},()=>{
    const S2=makeScene({getContext:()=>makeShot(800,500)});
    const t0=ST.t;
    S2.stepOnce();
    close(ST.t-t0,0.05,1e-15,'the step button advances t by PhET\'s 0.05 ms');
    ok(S2.step(0.25)===false,'... and a paused clock does not advance at all');
    close(ST.t-t0,0.05,1e-15,'... really not at all');
    ST.running=true;
    ok(S2.step(0.25)===true,'the clock runs in the space & time domain');
    close(ST.t-t0-0.05,0.25,1e-15,'... at 1 ms of model time per second of real time');
    ST.domain='space';
    ok(S2.step(0.25)===false,'and not in the space domain, as in PhET');
    ST.domain='time';
    ok(S2.step(0.25)===false,'nor in the time domain');
  });
  /* the drawing MOVES when an amplitude does — a drag that changes no pixels
     is what three earlier sims shipped (Known-bad) */
  withState({view:'harm',preset:'square',series:'sin',N:11},()=>{
    const S2=makeScene({getContext:()=>makeShot(1400,820)});
    S2.W=1400; S2.H=820;
    const c1=makeShot(1400,820); drawView(c1,1400,820,buildModel());
    const g1=JSON.stringify(c1.ops.filter(o=>o.op!=='text'));
    S2.draw();
    S2.pointer('down',barX(GEO.bars,6,11),barY(GEO.bars,-1.5,AMAX));
    S2.pointer('up',0,0);
    const c2=makeShot(1400,820); drawView(c2,1400,820,buildModel());
    const g2=JSON.stringify(c2.ops.filter(o=>o.op!=='text'));
    ok(g1!==g2,'dragging a bar changes the drawn geometry, not only the state');
  });

  /* ---------- M. the model wiring ---------- */
  withState({view:'harm',preset:'square',series:'sin',N:11},()=>{
    const M=buildModel();
    eq(M.sum.xs.length,NPTS+1,'the sum is drawn from 1001 points');
    close(M.sum.xs[0],-LWAVE,1e-15,'the window starts at -L');
    close(M.sum.xs[NPTS],LWAVE,1e-15,'and ends at +L');
    rel(M.par,parseval(presetAmps('square','sin',11),11),1e-15,'the readout\'s Parseval sum is the model\'s');
    eq(M.nz,6,'the 11-term square wave has six non-zero harmonics');
    ok(M.ideal===null,'the infinite-harmonics curve is off by default');
  });
  withState({view:'harm',preset:'square',showInf:true},()=>{
    ok(buildModel().ideal!==null,'and on when asked for');
  });
  withState({view:'harm',preset:'wavePacket',showInf:true},()=>{
    ok(buildModel().ideal===null,'the wave packet preset has no waveform to converge to, so none is drawn');
  });
  withState({view:'conv',convPre:'square',convM:11},()=>{
    const C=buildModel().C;
    eq(C.odd,6,'keeping 11 harmonics of a square wave keeps six odd ones');
    rel(C.pk.val,REF.gibbs_peak_M6,1e-7,'the convergence view measures that six-term peak (derive)');
    close(C.pk.u,PI/12,2e-3,'... at u = pi/2M with M = 6');
    rel(C.rms,REF.l2_square_N11,1e-13,'and the 11-term rms error (derive)');
    eq(C.jump,2,'the square wave jumps by 2');
    ok(C.closed!==null&&Math.abs(C.closed.val-C.pk.val)<2e-7,'the measured peak and the closed form agree in the view');
  });
  withState({view:'conv',convPre:'sawtooth',series:'cos',convM:11},()=>{
    eq(buildModel().C.series,'sin','a sawtooth is forced back to sines, as in PhET');
  });
  withState({view:'conv',convPre:'triangle',series:'cos',convM:6},()=>{
    eq(buildModel().C.jump,0,'the triangle does not jump');
  });
  withState({view:'spec',preset:'triangle',series:'cos',N:11},()=>{
    const S3=buildModel().S;
    ok(S3.dFFT<1e-13,'the spectrum view recovers the amplitudes');
    ok(S3.dDir<1e-13,'... by two independent transforms that agree');
    close(S3.msPar,S3.msNum,1e-13,'... and Parseval closes in the view as well');
    close(S3.cum[S3.cum.length-1],1,1e-15,'the cumulative power reaches exactly 1');
  });
  withState({view:'pack',wpSp:3},()=>{
    const P=buildModel().P;
    eq(P.n,REF.wp_n_components_pi,'the packet view counts PhET\'s components (derive)');
    close(P.sx*P.sk,1,1e-15,'and its widths multiply to 1');
    close(P.lam1,2,1e-12,'at PhET\'s widest spacing the packet repeats every 2 m');
    eq(P.copies,2,'... so two copies sit at the edges of PhET\'s own 2 m window');
    ok(P.devP<P.tail*1.05,'inside one period the sum sits on the exact packet to within the Gaussian tail');
    ok(P.dev>0.9,'while at the window edge the copy stands at full height');
  });
  withState({view:'pack',wpSp:1},()=>{
    const P=buildModel().P;
    eq(P.copies,0,'at pi/4 spacing the repeats are 8 m away, outside the window');
    ok(P.dev<P.tail*1.05,'and then the whole drawn sum is the exact packet to within the tail');
  });
  withState({view:'pack',wpSp:0},()=>{
    const P=buildModel().P;
    ok(P.cont&&!isFinite(P.n),'spacing zero means a continuous spectrum');
    close(P.dev,0,1e-15,'and then the drawn sum IS the exact packet');
    eq(P.copies,0,'with no repeats at all');
  });
  withState({view:'pair',pairK1:PI},()=>{
    const T=buildModel().T;
    close(T.lam1,2,1e-12,'k1 = pi repeats every 2 m');
    ok(T.devW>0.9,'so a full-height copy is inside the 3 m window');
    ok(T.devP<T.tail*1.05,'while inside one period only the tail is left');
    close(T.prod,1,1e-15,'and the widths still multiply to 1');
  });
  withState({view:'pair',pairK1:PAIR_K1_MIN},()=>{
    ok(buildModel().T.devW<1e-3,'at the finest spacing the copies have left the window');
  });

  /* ---------- N. the presets and the panel agree ---------- */
  withState({preset:'triangle',series:'sin',N:11},()=>{
    applyPreset();
    let d=0; const a=presetAmps('triangle','sin',11);
    for(let i=0;i<NMAX;i++) d=Math.max(d,Math.abs(AMPS[i]-a[i]));
    close(d,0,1e-15,'applyPreset writes the closed form into the eleven amplitudes');
  });
  withState({preset:'custom',_amps:[1,2,3,0,0,0,0,0,0,0,0]},()=>{
    applyPreset();
    eq(AMPS[1],2,'applyPreset leaves a custom set alone');
  });
  withState({preset:'square',series:'sin',N:4},()=>{
    applyPreset();
    eq(AMPS[4],0,'harmonics above N are zero');
    ok(AMPS[2]!==0,'and those below are not');
  });

  restore();
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
