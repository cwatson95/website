
/* the compass: the damped rotor, its closed forms and its energy ledger */
function testRotor(T){
  const {ok,close,rel}=T;
  close(KAPPA,REF['KAPPA'],0,'kappa = 6.25 /(G s^2): PhET\'s 0.01 /G per frame^2 at 25 frames a second');
  close(GAMMA_C,REF['GAMMA'],0,'gamma = 2 /s: PhET\'s 0.08 per frame');
  close(GAMMA_C*GAMMA_C/(4*KAPPA),REF['rotor.Bcrit'],1e-15,'so the needle is critically damped at 0.16 G and rings above it (python)');
  /* against solve_ivp (DOP853, rtol 1e-12): first with the page's own step rule, then refined */
  for(const tag of ['big','strong','over']){
    for(const t of [0.25,0.5,1,2,4]){
      const r=REF['rotor.'+tag+'.'+t], B=[r[0],0];
      const a={phi:r[1],om:0,W:0}; rotorAdvance(a,()=>B,0,t,KAPPA,r[2]);
      ok(Math.abs(a.phi-r[4])<2e-4,'the rotor at |B| = '+r[0]+' G, released at '+r[1]+' rad, at t = '+t+' s (scipy solve_ivp) ['+Math.abs(a.phi-r[4]).toExponential(1)+' rad]');
      const b={phi:r[1],om:0,W:0}, n=Math.ceil(t*400); for(let i=0;i<n;i++) rotorAdvance(b,()=>B,0,t/n,KAPPA,r[2]);
      ok(Math.abs(b.phi-r[4])<3e-7&&Math.abs(b.om-r[5])<3e-6,'and with finer steps it converges onto it ['+Math.abs(b.phi-r[4]).toExponential(1)+' rad]');
    }
  }
  /* the small-angle closed form, and the integrator agreeing with it where it holds */
  for(const k in REF) if(k.indexOf('rotor.lin.')===0){ const r=REF[k];
    rel(linearNeedle(r[1],Math.sqrt(KAPPA*r[0]),GAMMA_C,r[2]),r[3],1e-13,'the damped-oscillator solution at t = '+r[2]+' s (python)'); }
  { const B=[5,0], th0=1e-3, a={phi:th0,om:0,W:0}, n=1200, t=2;
    for(let i=0;i<n;i++) rotorAdvance(a,()=>B,0,t/n,KAPPA,GAMMA_C);
    const lin=linearNeedle(th0,Math.sqrt(KAPPA*5),GAMMA_C,t);
    ok(Math.abs(a.phi-lin)<1e-7*th0,'released at a milliradian the rotor IS the damped oscillator (off by '+(Math.abs(a.phi-lin)/th0).toExponential(1)+' of the release angle)'); }
  /* the large-amplitude undamped period: 4 K(sin(phi0/2))/omega0 */
  for(const k in REF) if(k.indexOf('rotor.period.')===0){
    const r=REF[k], B=[r[0],0], w0=Math.sqrt(KAPPA*r[0]);
    rel(4*ellK(Math.cos(r[1]/2))/w0,r[2],1e-13,'the pendulum period at '+r[1]+' rad is 4K(sin phi0/2)/omega0 = '+fmt(r[2],6)+' s (scipy ellipk)');
    rel(needleRun(r[0],r[1],0,1).Tbig,r[2],1e-13,'and the view reports that same period off its own model (scipy ellipk)');
    const a={phi:r[1],om:0,W:0}, h=r[2]/4000, zc=[];
    let prev=a.phi;
    for(let i=1;i<=8000&&zc.length<2;i++){ rotorAdvance(a,()=>B,0,h,KAPPA,0); if(prev>0&&a.phi<=0) zc.push((i-prev/(prev-a.phi))*h); prev=a.phi; }
    ok(zc.length===2&&Math.abs((zc[1]-zc[0])/r[2]-1)<1e-6,'and the undamped integration measures it back ['+(zc.length===2?fmt(zc[1]-zc[0],6)+' s':'no crossings')+']');
    rel(r[2]/(2*Math.PI/w0),4*ellK(Math.cos(r[1]/2))/(2*Math.PI),1e-13,'a swing of '+fmt(r[1]*180/Math.PI,0)+' degrees is '+fmt(r[2]/(2*Math.PI/w0),4)+' times slower than a small one');
  }
  /* the ledger: the needle's energy plus the work done against the damping is conserved,
     because both are integrated through the same RK4 stages */
  { const B=[5,0], a={phi:2.5,om:0,W:0}, E0=rotorEnergy(a,B); let worst=0, naive=0, naiveW=0;
    for(let i=0;i<600;i++){ const om0=a.om; rotorAdvance(a,()=>B,0,0.01,KAPPA,GAMMA_C);
      naiveW+=GAMMA_C*(om0*om0+a.om*a.om)/2*0.01;                    /* the ledger kept BESIDE the integrator */
      worst=Math.max(worst,Math.abs(rotorEnergy(a,B)+a.W-E0)/E0); naive=Math.max(naive,Math.abs(rotorEnergy(a,B)+naiveW-E0)/E0); }
    ok(worst<3e-7,'energy + work against the damping is conserved to '+worst.toExponential(1)+' over six seconds');
    ok(naive>100*worst,'a trapezoid ledger kept outside the integrator is '+fmt(naive/worst,0)+'x worse ('+naive.toExponential(1)+'): the work is integrated through the same RK4 stages');
    ok(a.W>0.9*E0,'and by the end the damping has taken essentially all of it ('+fmt(100*a.W/E0,1)+' %)');
    const b={phi:2.5,om:0,W:0}, E1=rotorEnergy(b,B); for(let i=0;i<600;i++) rotorAdvance(b,()=>B,0,0.01,KAPPA,0);
    ok(Math.abs(rotorEnergy(b,B)-E1)/E1<3e-7,'undamped, the energy alone is conserved'); }
  /* the period measured in the needle view, against the damped closed form */
  { const N=needleRun(5,5*Math.PI/180,GAMMA_C,8), w0=Math.sqrt(KAPPA*5), wd=Math.sqrt(w0*w0-GAMMA_C*GAMMA_C/4);
    rel(N.Tmeas,2*Math.PI/wd,2e-3,'the view\'s own measured period at 5 degrees is 2 pi/omega_d');
    rel(N.T0,2*Math.PI/w0,1e-15,'and it reports the small-swing period 2 pi/sqrt(kappa |B|)');
    ok(N.ledger<1e-6,'with its energy ledger clean ('+N.ledger.toExponential(1)+')'); }
  { const a=needleRun(80,Math.PI/3,GAMMA_C,4), b=needleRun(20,Math.PI/3,GAMMA_C,4);
    rel(a.T0/b.T0,0.5,1e-12,'four times the field halves the period: T0 goes as |B|^(-1/2) (Gauss\'s method)'); }
  { const N=needleRun(0.05,Math.PI/3,GAMMA_C,20); ok(!N.under&&!isFinite(N.wd),'below 0.16 G the needle is overdamped and does not ring');
    ok(N.ph.every(v=>v>=-1e-9),'it creeps back without crossing'); }
}
