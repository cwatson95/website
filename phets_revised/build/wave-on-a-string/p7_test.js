
/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (derive) are lines of build/wave-on-a-string/refvals.txt, the      *
 *  printed output of derive.py (an independent Python lattice, the    *
 *  d'Alembert image series, numpy.roots, a dense solve, brute-force   *
 *  runs, scipy minimize_scalar), read in full.                        *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function resetAll(){ liveRestart(); LIVE.sw=0; LIVE.swOn=false; LIVE.arrows=true; reflReset(ST); standReset(ST); }
  /* a configuration: plain keys go into ST; _keys drive the clocks */
  function withState(over,fn){
    const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    Object.assign(ST,DEFAULTS,clean); resetAll();
    if(over._wr!==undefined){ LIVE.wr=over._wr; LIVE.wrPrev=over._wr; }
    if(over._pulse) sendPulse(ST);
    if(over._live) for(let k=0;k<over._live;k++) liveStepOnce(ST,1);
    if(over._acc) LIVE.acc=over._acc*dtOf(ST.tension);
    if(over._refl) for(let k=0;k<over._refl;k++) reflStep(ST);
    if(over._stand) for(let k=0;k<over._stand;k++) standStep(ST);
    if(over._sw!==undefined){ LIVE.sw=over._sw; LIVE.swOn=true; }
    try{ return fn(); } finally{ Object.assign(ST,stSave); resetAll(); }
  }
  /* the JS lattice fed one pulse from rest (the same run derive.py makes) */
  function runPulse(end,A,w,T,nst,a,b,nseg){
    a=a===undefined?1:a; b=b||0; nseg=nseg||NSEG;
    const dt=a*DX/speedOf(T), L=makeLat(nseg), lev=[Array.from(L.cur)];
    for(let k=1;k<=nst;k++){ latStep(L,a,b,end,A*tri(k*dt/w)); lev.push(Array.from(L.cur)); }
    return {lev,dt};
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(mix('#070b18',mix('#b8ec4c','#cd35c4',0.5),1)!=='rgb(0,0,0)','mix() output is a legal mix() input (not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  { const f=tickFmt([0,0.25,0.5]); eq(f(0.25),'0.25','tick labels follow the spacing (0.25 needs two decimals)'); eq(tickFmt([0,2,4])(4),'4','and 2 needs none'); }

  for(const [a,r] of [[[-3,-4],[1,-2]],[[-3,4],[1,2]],[[3,4],[2,1]],[[-4,0],[0,2]],[[5,-12],[3,-2]]]){
    const q=csqrt(a); ok(Math.abs(q[0]-r[0])<1e-15&&Math.abs(q[1]-r[1])<1e-15,'csqrt is the principal root: sqrt('+a+') = '+r+' ['+q+']'); }

  /* ---------- A. PhET's values ---------- */
  eq(NSEG,60,'61 beads: 60 intervals (PhET\'s value)'); eq(DX,0.125,'0.125 cm apart: 10 model units at 80 per cm (PhET\'s value)');
  eq(LSTR,7.5,'7.5 cm of string (derive)'); eq(LLOOSE,7.4375,'the loose end mirrors about 7.4375 cm (derive)');
  eq(VMAX,6.25,'50 steps/s at full tension = 6.25 cm/s (PhET\'s value, derive)'); close(TMIN,0.032,1e-17,'T_min = 0.8/25 = 0.032');
  close(betaOf(0.2),0.02,1e-17,'beta = 0.1 x damping: 0.02 at PhET\'s default 0.2'); eq(SLOW,0.25,'slow motion x0.25 (PhET\'s value)');
  eq(AMAX,1.3,'amplitude and wrench to 1.3 cm (PhET\'s value)'); eq(FMAX,3,'frequency to 3 Hz'); ok(WMIN===0.2&&WMAX===1,'pulse width 0.2..1 s');
  eq(REF_Y0,1.45,'reference line starts 1.45 cm up (PhET\'s value)'); ok(RULER_H===10&&RULER_V===5,'rulers of 10 and 5 cm (PhET\'s value)');
  ok(DEFAULTS.amp===0.75&&DEFAULTS.freq===1.5&&DEFAULTS.pw===0.5&&DEFAULTS.damping===0.2&&DEFAULTS.tension===0.8,'PhET\'s defaults: 0.75 cm, 1.5 Hz, 0.5 s, damping 0.2, full tension');
  ok(DEFAULTS.mode==='manual'&&DEFAULTS.end==='fixed'&&DEFAULTS.running&&DEFAULTS.speed==='normal'&&!DEFAULTS.rulers&&!DEFAULTS.stopwatch&&!DEFAULTS.refline,'PhET starts manual, fixed end, playing, tools hidden');

  /* ---------- B. tension -> speed ---------- */
  for(const [T,v,dt] of [[0.8,6.25,0.02],[0.5,4.941058844013093,0.02529822128134703],[0.2,3.125,0.04],[0.032,1.25,0.1],[0.29,3.762998305872592,0.03321819194149599],[0.53,5.087131436281158,0.02457180467335805]]){
    rel(speedOf(T),v,1e-15,'v(T='+T+') = v_max sqrt(T/T_max) (derive)'); rel(dtOf(T),dt,1e-15,'dt(T='+T+') = dx/v (derive)'); rel(DX/dtOf(T)/speedOf(T),1,1e-15,'alpha = v dt/dx = 1 at T='+T); }
  rel(speedOf(0.4)/speedOf(0.1),2,1e-15,'v is proportional to sqrt(T): quadruple the tension, double the speed');
  rel(phetRate(0.8),50,1e-15,'PhET\'s map: 50 steps/s at 0.8 (derive)'); rel(phetRate(0.5),33.24555320336759,1e-14,'PhET\'s map at 0.5 (derive)'); rel(phetRate(0.2),10,1e-14,'PhET\'s map: 10 steps/s at 0.2 (derive)');
  rel(phetRate(0.8)/phetRate(0.2),5,1e-14,'PhET: 5:1 in speed over 4:1 in tension (derive)'); rel(speedOf(0.8)/speedOf(0.2),2,1e-15,'sqrt(T): 2:1 over the same range (derive)');
  rel(speedOf(TMIN),phetRate(0.2)*DX,1e-14,'the remake\'s slowest string is PhET\'s slowest, 1.25 cm/s');
  rel(keepPerStep(0.02),0.9801960588196068,1e-15,'amplitude kept per step at b = 0.02 (derive)'); rel(keepPerStep(0.02),Math.exp(-Math.atanh(0.02)),1e-15,'= exp(-atanh b) (derive)');
  rel(decayLength(0.02),6.249166577759148,1e-14,'decay length dx/atanh b at 0.02 (derive)'); rel(decayLength(0.1),1.245822163640993,1e-14,'at 0.1 (derive)'); eq(decayLength(0),Infinity,'no damping, no decay');
  rel(2*0.02/dtOf(0.8),2,1e-14,'the damping rate 2b/dt = 2 /s at PhET\'s defaults (derive)');

  /* ---------- C. d'Alembert with images: the lattice is exact ---------- */
  for(const [A,w,T,nst,devs,bad] of [[0.75,0.5,0.8,170,[2.442490654175344e-15,2.831068712794149e-15,6.661338147750939e-16],0.06000000000000155],
                                     [1.1,0.37,0.29,200,[1.06581410364015e-14,9.769962616701378e-15,1.720845688168993e-15],0.1975135737061956]]){
    const v=speedOf(T);
    ENDS.forEach((e,k)=>{
      const R=runPulse(e,A,w,T,nst); let dev=0;
      for(let n=0;n<=nst;n++) for(let i=0;i<=NSEG;i++) dev=Math.max(dev,Math.abs(R.lev[n][i]-imageSeries(e,A,w,v,n*R.dt,i*DX)));
      ok(dev<1e-13,'lattice = d\'Alembert with images, '+e+' A='+A+' w='+w+' T='+T+' (dev '+dev.toExponential(2)+'; derive '+devs[k].toExponential(2)+')');
    });
    const R=runPulse('loose',A,w,T,nst); let dv=0;
    for(let n=0;n<=nst;n++) for(let i=0;i<NSEG;i++){ const t=n*R.dt, x=i*DX;
      if(t<2*LSTR/v) dv=Math.max(dv,Math.abs(R.lev[n][i]-(A*tri((t-x/v)/w)+A*tri((t-(2*LSTR-x)/v)/w)))); }
    rel(dv,bad,1e-9,'the loose end\'s mirror at bead 60 instead of 59.5 is WRONG by this much (derive)');
  }
  { const F=runPulse('fixed',0.75,0.5,0.8,170).lev, Lo=runPulse('loose',0.75,0.5,0.8,170).lev, No=runPulse('none',0.75,0.5,0.8,170).lev;
    rel(F[60][45],0.6000000000000001,1e-14,'fixed: y[45] at step 60 (derive)'); rel(F[40][30],0.6000000000000001,1e-14,'fixed: y[30] at step 40 (derive)'); rel(F[70][57],0.3,1e-13,'fixed: y[57] at step 70, incident + inverted image (derive)');
    let mn=Infinity; for(let n=95;n<=130;n++) mn=Math.min(mn,F[n][30]); rel(mn,-0.72,1e-13,'fixed: the reflection comes back INVERTED, -0.72 at bead 30 (derive)');
    rel(Lo[72][60],1.44,1e-13,'loose: the ring rises to twice the pulse, 1.44, at step 72 (derive)');
    let mx=-Infinity; for(let n=0;n<=170;n++) mx=Math.max(mx,Lo[n][60]); rel(mx,1.44,1e-13,'loose: 1.44 is the ring\'s highest (derive)');
    let mb=-Infinity; for(let n=95;n<=130;n++) mb=Math.max(mb,Lo[n][30]); rel(mb,0.7200000000000002,1e-13,'loose: the reflection comes back UPRIGHT, +0.72 (derive)');
    let mz=0; for(let n=90;n<=170;n++) for(let i=0;i<=NSEG;i++) mz=Math.max(mz,Math.abs(No[n][i])); eq(mz,0,'no end: after the pulse leaves, the string is EXACTLY at rest (derive: 0)');
    rel(0.75*tri(12*0.02/0.5),0.72,1e-15,'the triangle sampled at its apex step is 0.96 A = 0.72 (derive)');
    const F2=runPulse('fixed',1.1,0.37,0.29,200).lev, L2=runPulse('loose',1.1,0.37,0.29,200).lev;
    rel(F2[31][20],0.02735068923188355,1e-12,'incommensurate fixed y[20] step 31 (derive)'); rel(F2[75][51],-1.014918557762845,1e-13,'incommensurate fixed y[51] step 75 (derive)');
    rel(L2[66][60],1.832323541819498,1e-13,'incommensurate loose y[60] step 66 (derive)');
    const C=runPulse('none',0.75,0.5,0.5,60);
    const cen=y=>{ let s=0,m=0; for(let i=0;i<y.length;i++){ s+=y[i]; m+=i*DX*y[i]; } return m/s; };
    rel((cen(C.lev[50])-cen(C.lev[30]))/(20*C.dt),4.941058844013092,1e-12,'the pulse centroid moves at exactly v, T = 0.5 (derive)');
    let first=-1; for(let n=0;n<=60&&first<0;n++) if(C.lev[n][40]!==0) first=n; eq(first,41,'the pulse reaches bead 40 at step 41: one bead per step (derive)'); }
  { const L=makeLat(NSEG); let y71=null;
    for(let k=1;k<=90;k++){ latStep(L,1,0,k<=70?'fixed':'loose',0.75*tri(k*0.02/0.5)); if(k===71) y71=L.cur[59]; }
    rel(y71,0.2400000000000001,1e-13,'switching fixed -> loose mid-run: y[59] one step later (derive)');
    rel(L.cur[59],-1.14,1e-13,'... and at step 90: PhET re-asserts the end on the current level first (derive; without it -1.26)');
    rel(L.cur[40],-0.48,1e-13,'y[40] at step 90 (derive)'); }
  { const p=imageParts('fixed',0.75,0.5,6.25,1.45,7.5); close(p.inc+p.ref,0,1e-15,'the image series holds the clamp at zero'); ok(p.inc>0.7&&p.ref<-0.7,'with the incident apex and its inverted image both there at t = L/v + w/2');
    const q=imageParts('loose',0.75,0.5,6.25,1.45,LLOOSE); ok(q.inc>0&&Math.abs(q.ref-q.inc)<1e-15,'at the loose mirror the image equals the incident'); }
  { const R=withState({view:'refl',_refl:60},()=>({y:REFL.lats.fixed.cur[45],n:REFL.n})); eq(R.n,60,'the demo clock ran 60 steps'); rel(R.y,0.6000000000000001,1e-14,'the reflection demo IS the same lattice: y[45] at step 60 (derive)');
    const S=withState({view:'refl'},()=>reflSummary(ST));
    close(S.fixed.r,-1,1e-12,'the demo measures r = -1 at the clamp'); close(S.loose.r,1,1e-12,'r = +1 at the ring'); close(S.none.r,0,1e-15,'r = 0 with no end');
    ok(S.fixed.dev<1e-13&&S.loose.dev<1e-13&&S.none.dev<1e-13,'and the demo departs from d\'Alembert by < 1e-13 anywhere');
    const n0=withState({view:'refl'},()=>{ const L0=reflLoop(ST); for(let k=0;k<L0+1;k++) reflStep(ST); return REFL.n; }); eq(n0,1,'the demo loops back to step 1 after reflLoop steps'); }

  /* ---------- D. damping: lattice eigenmodes against the closed form ---------- */
  function modeRun(m,a,b,nmax,g0,gm1){
    const kap=m*Math.PI/NSEG, L=makeLat(NSEG);
    for(let i=0;i<=NSEG;i++){ L.prev[i]=Math.sin(kap*i)*gm1; L.cur[i]=Math.sin(kap*i)*g0; }
    L.prev[0]=L.cur[0]=L.prev[NSEG]=L.cur[NSEG]=0;
    const out={0:Array.from(L.cur)};
    for(let n=1;n<=nmax;n++){ latStep(L,a,b,'fixed',0); out[n]=Array.from(L.cur); }
    return {out,kap};
  }
  function modeClosed(kap,a,b,g0,gm1,n){                      /* g_n = c1 z^n + c2 zbar^n, fitted to g_0, g_-1 */
    const r=keepPerStep(b), th=thetaOf(kap,a,b), z=[r*Math.cos(th),r*Math.sin(th)], zb=[z[0],-z[1]];
    const iz=cdiv([1,0],z), izb=cdiv([1,0],zb), det=csub(izb,iz);
    const c1=cdiv(csub(cmul([g0,0],izb),[gm1,0]),det), c2=csub([g0,0],c1);
    let zn=[1,0], zbn=[1,0]; for(let k=0;k<n;k++){ zn=cmul(zn,z); zbn=cmul(zbn,zb); }
    return cadd(cmul(c1,zn),cmul(c2,zbn))[0];
  }
  for(const [m,a,b,g0,gm1,ib,want,th,zabs] of [[3,1,0.02,1,1,10,[[1,0.9758594913630152],[10,0.05094969713420937],[100,-0.1333645990730346],[500,-3.519448272767077e-05]],0.1558114257283117,0.9801960588196068],
      [17,0.6,0.05,1,1,13,[[1,0.745819696719888],[7,-0.5610779159905422],[60,0.05033930820583879],[250,-4.468366739102583e-07]],0.5203593491726836,0.9511897312113418],
      [41,1,0,1,0,9,[[1,-1.089278070030057],[33,-0.7978467731353353],[400,0.06240347311954156]],2.146754979953025,1]]){
    const R=modeRun(m,a,b,want[want.length-1][0],g0,gm1);
    for(const [n,g] of want){
      const gl=R.out[n][ib]/Math.sin(R.kap*ib);
      rel(gl,g,1e-11,'mode m='+m+' a='+a+' b='+b+': g_'+n+' on the lattice (derive)');
      rel(modeClosed(R.kap,a,b,g0,gm1,n),gl,n>100?5e-10:1e-11,'mode m='+m+': g_'+n+' closed form = lattice');
    }
    rel(thetaOf(R.kap,a,b),th,1e-13,'mode m='+m+': theta per step (derive)'); rel(keepPerStep(b),zabs,1e-15,'mode m='+m+': |z| per step (derive)');
  }
  { const R=modeRun(17,0.6,0,300,1,Math.cos(thetaOf(17*Math.PI/NSEG,0.6,0)));
    rel(R.out[300][13]/Math.sin(R.kap*13),0.9497830028392059,1e-12,'a pure cosine mode at a = 0.6 after 300 steps (derive)'); rel(R.out[300][13]/Math.sin(R.kap*13),Math.cos(300*thetaOf(R.kap,0.6,0)),1e-12,'= cos(300 theta) (derive)'); }

  /* ---------- E. the dispersion relation ---------- */
  for(const [kap,a,b,th,wn,vg,vp] of [[1,1,0,0.9999999999999999,0.9999999999999999,1,0.9999999999999999],[2,0.5,0,0.8685118212476725,1.737023642495345,0.5955822502390045,0.8685118212476725],
      [1.5,0.8,0.05,1.152964949175388,1.441206186469234,0.8742020222031517,0.960804124312823],[0.3,1,0.02,0.2993525828002437,0.2993525828002437,1.002298003277742,0.9978419426674789],
      [2.9,0.35,0,0.7096996427648868,2.027713265042534,0.1285090531539653,0.6992114707043221]]){
    const tag='k dx='+kap+' a='+a+' b='+b+': ';
    rel(thetaOf(kap,a,b),th,1e-13,tag+'theta = omega dt (derive; numpy.roots agrees)'); rel(omegaNorm(kap,a,b),wn,1e-13,tag+'omega dx/v (derive)');
    rel(vgOverV(kap,a,b),vg,1e-12,tag+'v_g/v closed form (derive)'); rel(vpOverV(kap,a,b),vp,1e-13,tag+'v_p/v (derive)');
    const hh=1e-5, num=(omegaNorm(kap+hh,a,b)-omegaNorm(kap-hh,a,b))/(2*hh);
    rel(num,vgOverV(kap,a,b),1e-8,tag+'v_g closed form = the numerical derivative');
    const s=Math.sin(kap/2), c=1-2*a*a*s*s, z=[c/(1+b),Math.sqrt(Math.max(0,(1-b)/(1+b)-c*c/((1+b)*(1+b))))];
    const res=cadd(csub(cmul([1+b,0],cmul(z,z)),cmul([2*c,0],z)),[1-b,0]); ok(cabs(res)<1e-14,tag+'the root solves (1+b)z^2 - 2cz + (1-b) = 0'); rel(Math.atan2(z[1],z[0]),th,1e-12,tag+'and its angle is theta');
  }
  eq(thetaOf(0.02,1,0.1),0,'k dx = 0.02 is overdamped at b = 0.1: theta pinned at 0 (derive)'); rel(cutoffKap(0.02),0.02000133357339049,1e-15,'the overdamped cutoff asin(b) (derive)');
  { let worst=0; for(let k=1;k<=400;k++){ const kap=Math.PI*k/400; worst=Math.max(worst,Math.abs(omegaNorm(kap,1,0)-kap)); } ok(worst<2e-12,'alpha = 1, b = 0: omega = vk across the whole zone ('+worst.toExponential(2)+')'); }
  rel(chainOmegaNorm(2),1.682941969615793,1e-15,'the bead chain at k dx = 2 (derive)'); rel(omegaNorm(2,0.02,0),1.683021422840909,1e-12,'the lattice at a = 0.02 (derive)'); rel(omegaNorm(2,0.002,0),1.682942764047706,1e-12,'at a = 0.002 (derive)');
  rel((omegaNorm(2,0.02,0)-chainOmegaNorm(2))/(omegaNorm(2,0.002,0)-chainOmegaNorm(2)),100.0126301597978,1e-6,'a -> 0 approaches the chain as O(a^2): error ratio 100.01 (derive)');
  rel(chainVgOverV(1.2),Math.cos(0.6),1e-15,'the chain\'s group speed cos(k dx/2)');
  { let worst=0; for(let k=1;k<=200;k++){ const kap=Math.PI*k/200; worst=Math.max(worst,Math.abs(omegaNorm(kap,0.05,0)/chainOmegaNorm(kap)-1)); }
    ok(worst<4.5e-4&&worst>3.5e-4,'the drawn bead chain (a = 0.05) is within a^2/6 = 0.04 % of the real chain\'s omega(k) ('+worst.toExponential(2)+')'); } ok(vgOverV(0.02,1,0.1)!==vgOverV(0.02,1,0.1),'no group speed where the mode is overdamped (NaN)');
  { const k=kapFromOmega(1.3,0.7,0.01); rel(omegaNorm(k,0.7,0.01),1.3,1e-12,'kapFromOmega inverts omega(k)'); ok(!isFinite(kapFromOmega(4,1,0)),'and refuses a frequency above the zone'); }

  /* ---------- F. the driven steady state ---------- */
  for(const [end,f,A,b,T,mx,a10,a30,a59,a60,y30,nbf] of [
      ['fixed',1.5,0.75,0.02,0.8,0.7499999999999999,0.4968740451320018,0.3601607805613768,0.08059463095797113,5.721958498152797e-17,[0.3384697245522583,0.1231017197934237],4000],
      ['fixed',1.25,0.75,0.002,0.8,6.266601822410703,6.266601822410703,6.246629908390635,0.9755897045433245,0,[0.03948137798247582,6.246505137530345],0],
      ['loose',7*VMAX/(4*LLOOSE),0.75,0.005,0.8,2.55665442969097,2.471594475305993,1.717515543437851,2.474310257787042,2.474310257787041,[0.2945658117761566,1.692066968084677],0],
      ['none',1.5,0.75,0.02,0.8,0.7499999999999999,0.6142357642551871,0.4187707600906846,0.2307197252676191,0.2307197252676191,[0.3476178029002958,0.233518334641417],4000],
      ['loose',2.37,1.1,0.013,0.53,1.1,0.8612916965524183,0.3711564082046246,0.8334317561615501,0.8334317561615501,[0.130744406964062,0.3473657717723116],8000],
      ['fixed',0.6,0.5,0.1,0.2,0.5,0.2099297686643483,0.03711937375978781,0.001060161728679194,0,[0.01796545862495284,0.03248215209486482],0]]){
    const tag='steady '+end+' f='+fmt(f,4)+' b='+b+' T='+T+': ', Sx=steadyClosed(f,A,b,T,end), Y=Sx.Y;
    rel(steadyMax(Sx),mx,1e-10,tag+'max |Y| (derive)'); rel(cabs(Y[10]),a10,1e-10,tag+'|Y_10| (derive)'); rel(cabs(Y[30]),a30,1e-10,tag+'|Y_30| (derive)'); rel(cabs(Y[59]),a59,1e-10,tag+'|Y_59| (derive)');
    if(a60>1e-12) rel(cabs(Y[60]),a60,1e-10,tag+'|Y_60| (derive)'); else ok(cabs(Y[60])<1e-12,tag+'Y_60 = 0 at the clamp');
    rel(Y[30][0],y30[0],1e-9,tag+'Re Y_30 (derive)'); rel(Y[30][1],y30[1],1e-9,tag+'Im Y_30 (derive)');
    const Z=steadyThomas(f,A,b,T,end); let d=0; for(let i=0;i<=NSEG;i++) d=Math.max(d,cabs(csub(Z[i],Y[i])));
    ok(d<1e-9*Math.max(1,mx),tag+'the tridiagonal solve agrees with the closed form ('+d.toExponential(2)+')');
    if(nbf){ const L=makeLat(NSEG), dt=dtOf(T); let ph=0;
      for(let k=1;k<=nbf;k++){ ph=(ph+TAU*f*dt)%TAU; latStep(L,1,b,end,A*Math.sin(ph)); }
      let e=0; for(let i=0;i<=NSEG;i++) e=Math.max(e,Math.abs(L.cur[i]-cmul(Y[i],[Math.cos(ph),Math.sin(ph)])[1]));
      ok(e<1e-10,tag+'a '+nbf+'-step brute-force run settles onto it ('+e.toExponential(2)+'; derive 8e-13)'); }
    ok(steadyMax(Sx)>=A*(1-1e-12),tag+'the drive point is on the string, so max |Y| >= A');
  }
  rel(resonances('fixed',0.8,3)[0],0.4166666666666667,1e-15,'fixed f_1 = v/2L at full tension (derive)'); rel(resonances('loose',0.8,3)[0],0.2100840336134454,1e-15,'loose f_1 = v/4L\' (derive)');
  rel(resonances('fixed',0.2,3)[0],0.2083333333333333,1e-15,'fixed f_1 at T = 0.2 (derive)'); rel(resonances('loose',0.2,3)[0],0.1050420168067227,1e-15,'loose f_1 at T = 0.2 (derive)');
  eq(resonances('fixed',0.8,3).length,7,'seven fixed-end resonances in PhET\'s 0-3 Hz at full tension'); eq(resonances('none',0.8,3).length,0,'none with no end');
  { const h1=steadyMax(steadyClosed(1.25,0.75,1e-4,0.8,'fixed'))/0.75, h2=steadyMax(steadyClosed(1.25,0.75,1e-5,0.8,'fixed'))/0.75;
    rel(h1,166.6677751882077,1e-8,'at f_3 with b = 1e-4 the peak is 166.67 A (derive)'); rel(h2,1666.666777536687,1e-7,'with b = 1e-5, 1666.7 A (derive)');
    close(h1*NSEG*1e-4,1,1e-4,'the peak height is 1/(N b) as b -> 0'); close(h2*NSEG*1e-5,1,1e-6,'... to O(b)'); }
  for(const [end,fpk,hpk,b] of [['fixed',1.249899492100326,8.355636552961057,0.002],['loose',1.469195697525992,3.41102984339649,0.005]]){
    const g=f=>steadyMax(steadyClosed(f,0.75,b,0.8,end))/0.75;
    rel(g(fpk),hpk,1e-9,end+' b='+b+': the height at scipy\'s peak (derive)'); ok(g(fpk*(1+2e-4))<g(fpk)&&g(fpk*(1-2e-4))<g(fpk),end+': and it is a maximum');
    ok(Math.abs(fpk-resonances(end,0.8,3)[end==='fixed'?2:3])<2e-3,end+': sitting at the closed-form f_n'); }
  { const S1=steadyClosed(1.5,0.75,0.02,0.8,'none'); const r=cabs(cdiv(S1.q,cmul(S1.p,(()=>{ let z=[1,0]; for(let i=0;i<NSEG;i++) z=cmul(z,S1.lam); return z; })())));
    rel(r,0.05399408321884634,1e-10,'the no-end absorber sends back 5.4 % at 1.5 Hz, b = 0.02 (derive: the solve)'); rel(noEndReflection(1.5,0.02,0.8),0.05399408321884638,1e-10,'= the closed form (derive)');
    ok(noEndReflection(1.5,0,0.8)<1e-12,'and exactly nothing at b = 0'); const th=steadyTheta(1.5,0.8); rel(noEndReflection(1.5,0.02,0.8),0.02/(2*Math.sin(th)),0.02,'about b/(2 sin theta)'); }
  eq(JSON.stringify(withState({view:'stand',freq:1.25,damping:0.02},()=>buildModel()).nodes),'[20,40,60]','the third harmonic has its nodes at beads 20, 40 and the clamp');
  eq(withState({view:'stand',end:'none'},()=>buildModel()).nodes.length,0,'a travelling wave has none');
  eq(JSON.stringify(withState({view:'stand',freq:0.4166666666666667,damping:0.02},()=>buildModel()).nodes),'[60]','the first harmonic: one node, the clamp (three beads sit under 15 % beside it)');
  eq(JSON.stringify(withState({view:'stand',freq:0.8333333333333334,damping:0.02},()=>buildModel()).nodes),'[30,60]','the second: the middle and the clamp');
  { const R=withState({view:'stand'},()=>responseCurve(ST)); let lo=Infinity; for(const g of R.gb) lo=Math.min(lo,g);
    ok(lo>=1-1e-12,'the response curve never dips below 1 (the driven bead is on the string)'); eq(R.fn.length,7,'and marks the seven resonances');
    ok(R.g0.filter(g=>!isFinite(g)).length===7,'the undamped curve is left undrawn exactly at the seven f_n'); }
  { const D=steadyClosed(0,0.6,0.02,0.8,'fixed'); ok(D.dc&&Math.abs(D.Y[30][0]-0.3)<1e-15,'f = 0: the frozen oscillator holds a straight line to the clamp'); }

  /* ---------- G. the pulse on the long lattice (the dispersion view) ---------- */
  for(const [a,T,ns,dev,mn,mx,y30] of [[1,0.8,57,6.661338147750939e-16,0,0.72,0],[0.5,0.8,115,0.05330418760197286,-0.02499099445571134,0.7003335327276475,-0.01543613403012915],
      [0.5,0.2,102,0.07004500435025174,-0.03616083772769295,0.6624903538427503,-0.0004551962069355457],[0.05,0.8,1150,0.05211815381002127,-0.02706895059501099,0.6978818461899784,-0.02706895059501099]]){
    const P=longPulse(a,0,0.75,0.5,T,0.75*LSTR), v=speedOf(T), tag='long pulse a='+a+' T='+T+': ';
    eq(P.steps,ns,tag+'steps (derive)');
    let d=0, lo=Infinity, hi=-Infinity; for(let i=0;i<=NSEG;i++){ d=Math.max(d,Math.abs(P.y[i]-0.75*tri((P.t-i*DX/v)/0.5))); lo=Math.min(lo,P.y[i]); hi=Math.max(hi,P.y[i]); }
    if(a===1){ ok(d<1e-14,tag+'keeps its shape exactly ('+d.toExponential(2)+')'); eq(lo,0,tag+'no ripple at all (derive)'); }
    else { rel(d,dev,1e-9,tag+'departs from the exact pulse (derive)'); rel(lo,mn,1e-9,tag+'the trailing ripple (derive)'); }
    rel(hi,mx,1e-12,tag+'the peak (derive)'); if(y30!==0) rel(P.y[30],y30,1e-9,tag+'y[30] (derive)'); else eq(P.y[30],0,tag+'y[30] = 0 (derive)');
  }
  { const D=withState({view:'disp',alpha:0.5},()=>dispModel(ST)); ok(D.dev>0.01&&D.devC>0.01,'the dispersion view: at a = 0.5 and for the chain the pulse is visibly changed');
    const D1=withState({view:'disp'},()=>dispModel(ST)); ok(D1.dev<1e-14,'at PhET\'s a = 1 it is not ('+D1.dev.toExponential(2)+')');
    const D0=withState({view:'disp',damping:0},()=>dispModel(ST)); rel(D0.kOsc,TAU*1.5*DX/6.25,1e-12,'undamped, the oscillator\'s k dx = omega dx/v exactly on the a = 1 lattice');
    const th=TAU*1.5*0.02, b=betaOf(0.2); rel(D1.kOsc,Math.acos(Math.sqrt(1-b*b)*Math.cos(th)),1e-9,'damped, k dx = acos(sqrt(1-b^2) cos omega dt): damping itself disperses');
    ok(D1.kOsc>D0.kOsc,'so the damped wave is slightly shorter, v_p < v');
    rel(D1.fChain,6.25/(Math.PI*DX),1e-15,'a bead chain tops out at v/(pi dx) = 15.9 Hz');
    { const c=makeShot(820,520); withState({view:'disp'},()=>drawView(c,820,520,buildModel())); const tx=c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' ');
      ok(tx.indexOf('group')<0&&tx.indexOf('Right:')<0,'narrow: no word about the speeds panel it does not draw'); }
    const Dh=withState({view:'disp',alpha:0.5},()=>dispModel(ST)); close(Dh.ba,0.01,1e-15,'at a = 0.5 the damping per step halves: the same PHYSICAL damping');
    rel(Dh.om[120],omegaNorm(Dh.K[120],0.5,0.01),1e-15,'and the drawn curve carries it');
    const Du=withState({view:'disp',alpha:0.5,damping:0},()=>dispModel(ST)); rel(omegaNorm(Du.kOsc,0.5,0),TAU*1.5*DX/6.25,1e-12,'the oscillator\'s k on the a = 0.5 lattice gives back its omega');
    ok(Du.kOsc>TAU*1.5*DX/6.25,'and is longer than omega/v: the a < 1 lattice is slow'); rel(D1.fLat,25,1e-15,'the lattice Nyquist at a = 1: v/(2 dx) = 25 Hz'); }

  /* ---------- H. the drivers and the live clock ---------- */
  rel(tri(0.3),0.6,1e-15,'triangle at 0.3 (derive)'); eq(tri(0.5),1,'triangle apex (derive)'); rel(tri(0.8),0.3999999999999999,1e-15,'triangle at 0.8 (derive)'); ok(tri(-0.01)===0&&tri(1.01)===0,'zero outside [0, 1]');
  withState({view:'str',mode:'osc'},()=>{ for(let k=0;k<7;k++) liveStepOnce(ST,1); rel(LIVE.lat.cur[0],0.7264373708464733,1e-12,'the oscillator after 7 steps: A sin(7 x 2 pi f dt) (derive)'); });
  withState({view:'str',mode:'osc'},()=>{ const S=makeScene({getContext:()=>makeShot(1100,712)}); for(let k=0;k<60;k++) S.step(1/60);
    eq(LIVE.lat.steps,50,'one second of frames = 50 lattice steps at full tension'); close(LIVE.t,1,1e-12,'and the lattice clock reads 1 s');
    ST.speed='slow'; for(let k=0;k<240;k++) S.step(1/60); eq(LIVE.lat.steps,100,'slow motion: 240 frames = 1 simulated second = 50 more steps');
    ST.running=false; ok(!S.step(1/60),'paused: the frame does nothing'); eq(LIVE.lat.steps,100,'and no step is taken'); });
  withState({view:'str',mode:'osc',tension:0.2},()=>{ const S=makeScene({getContext:()=>makeShot(1100,712)}); for(let k=0;k<60;k++) S.step(1/60); eq(LIVE.lat.steps,25,'at T = 0.2 the clock runs at 25 steps/s: the tension sets the clock'); });
  withState({view:'str',mode:'pulse'},()=>{
    ok(sendPulse(ST),'the generator sends a pulse'); ok(!sendPulse(ST),'and is busy until it is done');
    for(let k=0;k<24;k++) liveStepOnce(ST,1); ok(LIVE.pulseOn,'still sending at step 24 (w/dt = 25)'); liveStepOnce(ST,1); ok(!LIVE.pulseOn,'done after 25 steps'); ok(sendPulse(ST),'then ready again');
    let first=-1; liveRestart(); sendPulse(ST); for(let n=1;n<=60&&first<0;n++){ liveStepOnce(ST,1); if(LIVE.lat.cur[40]!==0) first=n; } eq(first,41,'the live pulse reaches bead 40 at step 41'); });
  withState({view:'str',mode:'pulse',_live:7},()=>{ LIVE.acc=0.013; ok(sendPulse(ST),'a pulse sent between lattice levels');
    close(LIVE.pulseT0,LIVE.t+0.013,1e-15,'starts NOW, not at the last level'); liveStepOnce(ST,1);
    rel(LIVE.lat.cur[0],0.75*tri(0.007/0.5),1e-9,'so bead 0 first samples the triangle 0.007 s in'); });
  withState({view:'str'},()=>{ ok(!sendPulse(ST),'no pulse outside pulse mode'); LIVE.wrPrev=0; LIVE.wr=1; liveAdvance(ST,0.1);
    eq(LIVE.lat.steps,5,'0.1 s at full tension is 5 steps'); const ys=LIVE.hist.map(r=>r[0]);
    ok(ys.length===5&&[0.2,0.4,0.6,0.8,1].every((v,k)=>Math.abs(ys[k]-v)<1e-9),'the wrench is interpolated across the frame, as PhET\'s ticks do ('+ys.map(v=>fmt(v,3)).join(', ')+')');
    eq(LIVE.wrPrev,1,'and the frame ends where the wrench is'); });
  withState({view:'str',mode:'osc',_live:20},()=>{ const dt=dtOf(ST.tension); LIVE.acc=dt/2; const y=liveDraw(ST);
    ok(Math.abs(LIVE.lat.prev[10]-LIVE.lat.cur[10])>0.01,'bead 10 is behind the front, so its last two levels differ (the probe can see interpolation: '+fmt(Math.abs(LIVE.lat.prev[10]-LIVE.lat.cur[10]),3)+' cm)');
    close(y[10],(LIVE.lat.prev[10]+LIVE.lat.cur[10])/2,1e-15,'the drawn string is halfway between the last two levels (PhET\'s yDraw)');
    rel(y[0],ST.amp*Math.sin(LIVE.phase+TAU*ST.freq*dt/2),1e-12,'while bead 0 sits where the driver is now'); });
  withState({view:'str',mode:'osc',_live:500},()=>{ eq(LIVE.hist.length,HMAX,'the space-time record keeps '+HMAX+' levels'); let inc=true; for(let k=1;k<LIVE.histT.length;k++) if(!(LIVE.histT[k]>LIVE.histT[k-1])) inc=false; ok(inc,'in time order'); });
  withState({view:'str',_live:3},()=>{ LIVE.swOn=true; const S=makeScene({getContext:()=>makeShot(1100,712)}); for(let k=0;k<30;k++) S.step(1/60); close(LIVE.sw,0.5,1e-12,'the stopwatch counts simulated seconds');
    ST.speed='slow'; for(let k=0;k<30;k++) S.step(1/60); close(LIVE.sw,0.625,1e-12,'at a quarter speed in slow motion');
    liveStepButton(ST); close(LIVE.sw,0.645,1e-12,'the step button advances it by one lattice step'); });
  withState({view:'str',mode:'osc',end:'loose',_live:30},()=>{ liveStepButton(ST); eq(LIVE.lat.steps,31,'the step button takes exactly one lattice step'); eq(LIVE.acc,0,'from a clean phase'); });
  withState({view:'stand',freq:1.25,damping:0.02},()=>{ for(let k=0;k<30000;k++) standStep(ST);
    const Sx=steadyClosed(1.25,0.75,betaOf(0.02),0.8,'fixed'); let e=0; for(let i=0;i<=NSEG;i++) e=Math.max(e,Math.abs(STAND.lat.cur[i]-cmul(Sx.Y[i],[Math.cos(STAND.phase),Math.sin(STAND.phase)])[1]));
    ok(e<1e-9,'the standing-wave run from rest settles onto the exact resonant steady state ('+e.toExponential(2)+')'); });

  /* ---------- I. the models, the readouts ---------- */
  const PRESETS={str:[{},{mode:'osc'},{mode:'pulse',_pulse:1,_live:10},{end:'loose'},{end:'none',mode:'osc',_live:80},{stopwatch:true,rulers:true,refline:true}],
                 xt:[{},{mode:'osc',_live:400},{end:'none'}],refl:[{},{_refl:80},{amp:0}],
                 stand:[{},{end:'loose'},{end:'none'},{damping:0},{freq:0}],disp:[{},{alpha:0.5},{alpha:0.05,tension:TMIN,freq:3},{damping:1}]};
  for(const [v] of TABS) for(const over of PRESETS[v]){
    const M=withState(Object.assign({view:v},over),()=>buildModel());
    const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over));
  }
  ok(readoutHTML(withState({view:'str',tension:0.5},()=>buildModel())).indexOf('4.941 cm/s')>=0,'the readout prints v = 4.941 cm/s at T = 0.5 off the model');
  ok(readoutHTML(withState({view:'stand',freq:1.25,damping:0.02},()=>buildModel())).indexOf('8.355')>=0,'the standing-wave readout prints the 8.355 A resonance');
  ok(readoutHTML(withState({view:'refl'},()=>buildModel())).indexOf('-1.000')>=0,'the reflection readout prints r = -1.000 for the clamp');
  ok(readoutHTML(withState({view:'str',end:'none',mode:'osc'},()=>buildModel())).indexOf('0.054')>=0,'the no-end readout prints the 5.4 % leak');
  { const M=withState({view:'str',mode:'osc',freq:1.25,damping:0,_live:3000},()=>buildModel()); ok(M.offScale&&M.maxAbs>YHALF,'undamped at a resonance the string runs off the view, and the model says so ('+fmt(M.maxAbs,2)+' cm)'); }

  /* ---------- J. the pointer ---------- */
  { const shot=makeShot(1100,712), S=makeScene({getContext:()=>shot});
    withState({view:'str',running:false},()=>{
      const G=strGeo(shot,S.W,S.H,buildModel()), map=G.map;
      ok(S.pointer('down',map.X(-0.7),map.Y(0)),'pointer-down on the wrench grabs it'); eq(DRAG.what,'wrench','it is the wrench');
      S.pointer('move',map.X(-0.7),map.Y(0.8)); close(LIVE.wr,0.8,1e-9,'the wrench follows the pointer to 0.8 cm'); ok(ST.running,'and, as in PhET, presses play');
      S.pointer('move',map.X(-0.7),map.Y(5)); eq(LIVE.wr,AMAX,'and stops at 1.3 cm'); ok(S.pointer('up',0,0),'pointer-up releases'); eq(DRAG.what,null,'nothing dragged');
      ok(!S.pointer('down',map.X(4),map.Y(-2)),'a pointer-down on empty string grabs nothing');
      ST.mode='pulse'; ok(S.pointer('down',map.X(-0.9),map.Y(0)),'clicking the generator'); ok(LIVE.pulseOn,'sends a pulse'); S.pointer('up',0,0); ok(!S.pointer('down',map.X(-0.9),map.Y(0)),'and it is busy while sending');
      ST.mode='manual'; ST.rulers=true; ST.refline=true; ST.stopwatch=true;
      ok(S.pointer('down',map.X(ST.rhX+5),map.Y(ST.rhY-0.25)),'grab the horizontal ruler'); eq(DRAG.what,'rh','the horizontal ruler');
      const x0=ST.rhX; S.pointer('move',map.X(ST.rhX+5)+50,map.Y(ST.rhY-0.25)); rel(ST.rhX-x0,50/map.s,1e-9,'it moves with the pointer'); S.pointer('up',0,0);
      ok(S.pointer('down',map.X(ST.rvX+0.25),map.Y(ST.rvY+2)),'grab the vertical ruler'); eq(DRAG.what,'rv','the vertical ruler');
      const y0=ST.rvY; S.pointer('move',map.X(ST.rvX+0.25),map.Y(y0+2)-30); rel(ST.rvY-y0,30/map.s,1e-9,'it moves up with the pointer'); S.pointer('up',0,0);
      ok(S.pointer('down',map.X(3),map.Y(ST.refY)+2),'grab the reference line'); eq(DRAG.what,'ref','the reference line');
      S.pointer('move',map.X(3),map.Y(0.5)+2); close(ST.refY,0.5,1e-9,'it follows to 0.5 cm, keeping the grab offset'); S.pointer('up',0,0);
      const r=swRect(map,ST,S.W,S.H); ok(S.pointer('down',r.x+20,r.y+20),'grab the stopwatch'); eq(DRAG.what,'sw','the stopwatch');
      S.pointer('move',r.x+120,r.y+60); close(map.X(ST.swX),r.x+100,1e-6,'it follows the pointer'); S.pointer('up',0,0);
    });
    withState({view:'stand'},()=>{ const tb=standGeo(shot,S.W,S.H).tb;
      ok(S.pointer('down',tb.x+tb.w*0.5,tb.y+tb.h*0.5),'pointer-down on the response panel'); close(ST.freq,1.5,1e-12,'sets f = 1.5 Hz at mid-panel');
      S.pointer('move',tb.x+tb.w*(1.25/3),tb.y+10); close(ST.freq,1.25,1e-12,'dragging sets f_3 = 1.25 Hz'); S.pointer('up',0,0);
      ok(!S.pointer('down',tb.x+10,tb.y1+40),'below the panel nothing is grabbed'); });
    for(const v of ['xt','refl','disp']) withState({view:v},()=>ok(!S.pointer('down',300,300),'the '+v+' view ignores the pointer'));
  }

  /* ---------- K. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['str manual',{view:'str'},4],['str kink',{view:'str',_wr:1.2,_live:25},4],['str osc',{view:'str',mode:'osc',_live:90,_acc:0.4},5],
    ['str pulse flying',{view:'str',mode:'pulse',_pulse:1,_live:40},5],['str loose tools',{view:'str',mode:'osc',end:'loose',_live:70,rulers:true,stopwatch:true,refline:true,_sw:1.23},9],
    ['str none',{view:'str',mode:'osc',end:'none',_live:120},4],['str offscale',{view:'str',mode:'osc',freq:1.25,damping:0,_live:3000},4],
    ['str slow low T',{view:'str',mode:'osc',tension:TMIN,speed:'slow',_live:40},5],
    ['xt empty',{view:'xt'},1],['xt osc',{view:'xt',mode:'osc',_live:400},6],['xt pulse fixed',{view:'xt',mode:'pulse',_pulse:1,_live:200},4],['xt none',{view:'xt',mode:'osc',end:'none',_live:300},6],
    ['refl start',{view:'refl'},4],['refl 40',{view:'refl',_refl:40},6],['refl 75',{view:'refl',_refl:75},6],['refl 110',{view:'refl',_refl:110},6],['refl flat',{view:'refl',amp:0,_refl:50},4],['refl slow',{view:'refl',tension:TMIN,pw:1,_refl:30},6],
    ['stand default',{view:'stand',_stand:200},4],['stand resonance',{view:'stand',freq:1.25,damping:0.02,_stand:400},4],['stand loose',{view:'stand',end:'loose',freq:1.47,_stand:300},4],
    ['stand none',{view:'stand',end:'none',_stand:200},4],['stand undamped',{view:'stand',damping:0,freq:0.83,_stand:500},4],['stand f0',{view:'stand',freq:0},4],['stand low T',{view:'stand',tension:TMIN,freq:2.9,_stand:100},4],
    ['disp default',{view:'disp'},3],['disp half',{view:'disp',alpha:0.5},3],['disp chain',{view:'disp',alpha:0.05,tension:TMIN,freq:3},3],['disp damped',{view:'disp',damping:1,alpha:0.7},3],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,minFills] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(fills.length>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    });
  }

  Object.assign(ST,stSave); resetAll();
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
