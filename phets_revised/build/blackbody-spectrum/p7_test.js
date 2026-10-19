
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST), savedSave=SAVED.slice();
  function withState(over,fn,saved){
    Object.assign(ST,DEFAULTS,over); ST.gvNm=over.gvNm!==undefined?over.gvNm:peakNm(ST.T);
    SAVED.length=0; if(saved) for(const T of saved) SAVED.push(T);
    try{ return fn(); } finally{ Object.assign(ST,stSave); SAVED.length=0; for(const T of savedSave) SAVED.push(T); }
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  eq(toRgb('rgb(12,34,56)').join(','),'12,34,56','toRgb reads mix()’s own rgb() output');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  eq(logTicks(0,10).length,0,'a non-positive log bound returns no ticks instead of looping');

  /* ---------- A. the constants (scipy.constants, CODATA 2022) ---------- */
  eq(H_PLANCK,6.62607015e-34,'h exact (SI 2019)'); eq(C_LIGHT,299792458,'c exact'); eq(K_BOLTZ,1.380649e-23,'k exact');
  rel(C1,3.7417718521927573e-16,1e-15,'c1 = 2 pi h c^2 (scipy first radiation constant)');
  rel(C2,0.014387768775039337,1e-15,'c2 = hc/k (scipy second radiation constant)');
  rel(SIGMA,5.6703744191844314e-08,1e-15,'sigma = 2 pi^5 k^4/(15 h^3 c^2) (scipy Stefan_Boltzmann)');
  rel(X5,4.965114231744276,1e-15,'x5 = 5 + W0(-5 e^-5) (scipy lambertw; decimal Newton agrees)');
  rel(X3,2.8214393721220787,1e-15,'x3 = 3 + W0(-3 e^-3) (scipy lambertw)');
  close(X5-5*(1-Math.exp(-X5)),0,1e-15,'x5 satisfies its own equation'); close(X3-3*(1-Math.exp(-X3)),0,1e-15,'and x3 its');
  rel(B_WIEN,0.0028977719551851727,1e-15,'b = hc/(x5 k) (scipy Wien wavelength displacement)');
  rel(NU_PER_T,58789257576.468254,1e-15,'nu_max/T = x3 k/h (scipy Wien frequency displacement)');
  rel(K_PEAK,1.2866941473091524e-05,1e-14,'K_peak = 2 pi k^5 x5^5 / (h^4 c^3 (e^x5 - 1)) (derive)');
  rel(PI4_15,6.493939402266828,1e-15,'pi^4/15 = int t^3/(e^t - 1) (scipy quad)');
  /* PhET's own constants, as the header states them */
  close(3.74192e-16/C1-1,3.9593e-05,5e-9,'PhET c1 is 4.0e-5 above 2 pi h c^2 (derive)');
  close(14387700e-9/C2-1,-4.7801e-06,5e-10,'PhET c2 is 4.8e-6 below hc/k (derive)');
  close(5.670373e-8/SIGMA-1,-2.5028e-07,5e-11,'PhET sigma is 2.5e-7 low (derive)');
  close(2897773e-9/B_WIEN-1,3.6056e-07,5e-11,'PhET b is 3.6e-7 high (derive)');

  /* ---------- B. Planck's law against 50-digit decimal arithmetic ---------- */
  const PL=[[10,200,0],[100,200,1.4016771987289822e-305],[380,200,2.8620546825134977e-78],[450,200,7.5669233697133133e-66],[500,200,3.9168904307788716e-59],
    [550,200,1.1653557673020855e-53],[650,200,2.7727199901619645e-45],[780,200,1.142704316119176e-37],[1000,200,2.1401015135101908e-29],[3000,200,5.9327591831607802e-11],
    [10000,200,2.8128032835450544e-06],[48000,200,4.2246770629552968e-07],[100000,200,3.5528417369295389e-08],
    [10,250,0],[100,250,4.2848326800065906e-243],[380,250,7.9464692255645699e-62],[450,250,5.8148486547128314e-52],[500,250,1.2302647900866799e-46],
    [550,250,2.6755901908435637e-42],[650,250,1.1376977911399561e-35],[780,250,1.1718390123353436e-29],[1000,250,3.7928263547329429e-23],[3000,250,7.1795890117163733e-09],
    [10000,250,1.1886206567001928e-05],[48000,250,6.3386218053228419e-07],[100000,250,4.80923783218195e-08],
    [10,3000,1.9444246002586817e-196],[100,3000,5.5545474868114833e-14],[380,3000,0.15595357277920377],[450,3000,0.47696362211074411],[500,3000,0.81765710350502607],
    [550,3000,1.2143608706804889],[650,3000,2.0156180877049281],[780,3000,2.7747365885174249],[1000,3000,3.1177270203730347],[3000,3000,0.39019374675394625],
    [10000,3000,0.0060800726258637789],[48000,3000,1.3975367776845612e-05],[100000,3000,7.6163917457769251e-07],
    [10,5800,6.9155356204173882e-96],[100,5800,0.00063059737061745393],[380,5800,69.136773867236244],[450,5800,82.167248468185804],[500,5800,84.452920857153799],
    [550,5800,82.656913209161175],[650,5800,72.567178515756382],[780,5800,56.214638141952101],[1000,5800,34.174471504948421],[3000,5800,1.1972050401681467],
    [10000,5800,0.013290222658203612],[48000,5800,2.76870289543434e-05],[100000,5800,1.4897522487556708e-06],
    [10,9950,5.9401174666484219e-51],[100,9950,19.640353695888621],[380,9950,1074.781317081427],[450,9950,849.7754907417085],[500,9950,703.11005270846874],
    [550,9950,578.06640094022748],[650,9950,390.89072942555259],[780,9950,240.69566117096505],[1000,9950,115.26886102829474],[3000,9950,2.486339740909592],
    [10000,9950,0.024050770380081042],[48000,9950,4.8015778121105107e-05],[100000,9950,2.5689945736378891e-06],
    [10,11000,5.8650534899927556e-45],[100,11000,78.090405388963731],[380,11000,1561.0622668036024],[450,11000,1172.4592895527435],[500,11000,944.27225645730243],
    [550,11000,759.81715744494852],[650,11000,497.63873572916083],[780,11000,298.00400006930431],[1000,11000,138.65136171547076],[3000,11000,2.8176204192909591],
    [10000,11000,0.026777165287540438],[48000,11000,5.3159512036259852e-05],[100000,11000,2.8420597433092276e-06]];
  { let worst=0, nOK=0;
    for(const [L,T,ref] of PL){
      const v=specPow(L,T), x=xOf(L,T);
      if(ref<1e-300){ ok(v===0||v<1e-300,'M('+L+' nm, '+T+' K) underflows to 0 (x = '+fmt(x,0)+')'); continue; }
      const r=Math.abs(v/ref-1); worst=Math.max(worst,r/Math.max(10,x));
      if(r<=1e-14*Math.max(10,x)) nOK++; else ok(false,'M('+L+' nm, '+T+' K) = '+v+' vs '+ref+' (decimal)');
    }
    eq(nOK,PL.length-3,'75 values of M_lambda equal the 50-digit decimal ones to 1e-14 x max(10, hc/lamkT) (worst '+worst.toExponential(2)+')'); }
  eq(specPow(0,5800),0,'M(0) = 0'); eq(exitance(500e-9,0),0,'T = 0 radiates nothing');
  { const T=300, lam=C2/(T*1e-3);       /* x = 1e-3: the Rayleigh–Jeans end, where only expm1 keeps digits */
    const r=exitance(lam,T)/rjExitance(lam,T), x=1e-3;
    close(r,1-x/2+x*x/12,2e-15,'x = 1e-3: M/M_RJ = x/(e^x - 1) = 1 - x/2 + x^2/12 (two-term expansion, O(x^4))');
    ok(Math.abs(r-1)>4e-4,'and it is NOT 1: the departure is x/2 = 5e-4, a real O(x) term'); }
  { const T=5800, L=200e-9, x=C2/(L*T);    /* the Wien end: dropping the -1 changes M by e^-x */
    close(exitance(L,T)/wienExitance(L,T),1/(1-Math.exp(-x)),1e-15,'x = 12.4: M/M_Wien = 1/(1 - e^-x)'); }

  /* ---------- C. Wien ---------- */
  for(const [T,lm,Mp] of [[250,11591.087820740689,1.256537253231594e-05],[3000,965.92398506172412,3.12666677796124],[5800,499.61585434227118,84.453041193235066],
      [9950,291.23336233016812,1254.8468628124645],[200,14488.859775925863,4.1174212713892857e-06],[11000,263.43381410774293,2072.2337911828631]]){
    rel(peakNm(T),lm,1e-14,'lambda_max at '+T+' K (derive)'); rel(peakPow(T),Mp,1e-13,'peak height at '+T+' K (derive; decimal agrees)');
    rel(peakPowT5(T),peakPow(T),1e-13,'K_peak T^5 = M(lambda_max) at '+T+' K: the second route');
  }
  { /* the peak found on the curve itself, by golden-section search — no Wien constant used */
    const T=5800, f=L=>-specPow(L,T); let a=300, b=800; const g=(Math.sqrt(5)-1)/2;
    let c=b-g*(b-a), d=a+g*(b-a);
    for(let i=0;i<80;i++){ if(f(c)<f(d)){ b=d; } else { a=c; } c=b-g*(b-a); d=a+g*(b-a); }
    rel((a+b)/2,499.61585434227118,5e-8,'golden-section argmax of the curve = b/T at 5800 K (to the flatness of a maximum)'); }
  rel(NU_PER_T*5800,340977693943515.88,1e-14,'nu_max at 5800 K (derive)');
  rel(C_LIGHT/(NU_PER_T*5800)/NM,879.21428094842372,1e-14,'c/nu_max at 5800 K = 879.2 nm, not 499.6 (derive)');
  rel(X3/X5,0.5682526605497431,1e-14,'lambda_max nu_max / c = x3/x5 (derive)');
  { const shape=u=>specPow(u*peakNm(4321),4321)/peakPow(4321);
    const bis=(lo,hi,up)=>{ for(let i=0;i<200;i++){ const m=(lo+hi)/2; if((shape(m)<0.5)===up) lo=m; else hi=m; } return (lo+hi)/2; };
    rel(bis(0.3,1,true),0.61323368060735495,1e-12,'half maximum below the peak, 0.613 lambda_max, found at 4321 K (derive)');
    rel(bis(1,5,false),1.8169998026431176,1e-12,'half maximum above, 1.817 lambda_max (derive)'); }
  { let same=true; const u=2.2;
    for(const T of [200,777,5800,11000]) if(Math.abs(specPow(u*peakNm(T),T)/peakPow(T)-specPow(u*peakNm(3000),3000)/peakPow(3000))>1e-13) same=false;
    ok(same,'M/M_peak at lambda = 2.2 lambda_max is the same at every temperature: one universal curve'); }

  /* ---------- D. Stefan–Boltzmann ---------- */
  for(const [T,I] of [[250,221.49900074939185],[3000,4593003.2795393895],[5800,64168769.433202945],[9950,555781465.53203952],[200,90.725990706950896],[11000,830199518.71279263]]){
    rel(intensity(T),I,1e-15,'sigma T^4 at '+T+' K (derive; scipy quad agrees to 4e-16)');
    rel(totalByQuadrature(T),I,2e-14,'the 1024-point Gauss-Legendre integral of the curve at '+T+' K = sigma T^4');
  }
  eq(intensity(2000)/intensity(1000),16,'double T, sixteen times the power');
  { let s=0; for(let i=0;i<GL16.w.length;i++) s+=GL16.w[i]; close(s,2,1e-14,'Gauss-Legendre weights sum to 2');
    let m=0; for(let i=0;i<GL16.x.length;i++) m+=GL16.w[i]*Math.pow(GL16.x[i],30); close(m,2/31,1e-14,'and integrate x^30 exactly (degree 31)'); }

  /* ---------- E. the band fractions: two series and their join ---------- */
  for(const [k,v] of [[0,1],[1,-0.5],[2,1/12],[4,-1/720],[6,1/30240],[8,-1/1209600],[10,1/47900160],[20,-2.1748686985580619e-16],[40,-2.36502241570063e-32]])
    rel(BERN_A[k],v,2e-13,'a_'+k+' = B_'+k+'/'+k+'! from power-series division (exact rational, derive)');
  close(BERN_A[3],0,1e-17,'a_3 = 0 (odd Bernoulli numbers vanish)');
  const FX=[[0.001,3.3320834999999982e-10,0.99999999994868938],[0.01,3.320849999980159e-07,0.99999994886231924],[0.1,0.00032099998016240375,0.99995056929849846],
    [0.5,0.034373457040676403,0.99470684049982394],[1,0.22480518802593821,0.96538230893447119],[1.5,0.61549498283947068,0.90522009142484128],
    [1.999,1.1750906706033146,0.81904810041911891],[2,1.1763425966069978,0.81885531666704903],[2.001,1.1775949526990686,0.8186624666857828],
    [3,2.5522184532908021,0.60698455972658083],[5,4.8998921583305819,0.24546691079066979],[10,6.4319218967818301,0.009550059161831867]];
  for(const [x,hd,fb] of FX){
    if(x<=3) rel(headSeries(x),hd,x<=2?2e-15:5e-14,'head series at x = '+x+' (exact rationals; quad agrees)');
    if(x>=1) close(PI4_15-tailSeries(x),hd,1e-15*PI4_15,'tail series at x = '+x+' (50-digit series; a difference of O(6.5) numbers)');
    rel(fracBelow(C2/(x*1000*NM*1),1000),fb,1e-14,'F(x = '+x+') through fracBelow (derive)');
  }
  for(const [x,tl] of [[5,1.5940472439362472],[10,0.062017505484999298],[20,1.9222318701195232e-05],[50,2.5614955230869607e-17],[100,3.8339326213429296e-38],
      [300,1.4040071771477729e-123],[700,3.3964042488284712e-296]])
    rel(tailSeries(x),tl,1e-13,'tail series at x = '+x+' (50-digit decimal)');
  eq(tailSeries(800),0,'past x = 745 the tail is exactly 0');
  /* the join: each branch where the other is used, at a tolerance only the right branch meets */
  close(headSeries(1.999)+tailSeries(1.999),PI4_15,5e-15,'head + tail = pi^4/15 just below the join');
  close(headSeries(2.001)+tailSeries(2.001),PI4_15,5e-15,'and just above it');
  ok(Math.abs(headSeries(7.5)-(PI4_15-tailSeries(7.5)))>1e-3,'the head series has failed by x = 7.5 (radius 2 pi): the join cannot move up past it');
  ok(Math.abs(tailSeries(0.002)-(PI4_15-headSeries(0.002)))>1e-10,'and the capped tail series has failed by x = 0.002: nor down below it');
  eq(fracBelow(0,5800),0,'nothing below 0 nm'); eq(fracAbove(0,5800),1,'everything above it');
  close(fracBelow(1e12,5800),1,1e-15,'everything below a kilometre');
  for(const [T,xr,uv,vis,ir,far] of [[250,0,9.1822038416470576e-61,5.8264838321409986e-28,0.99216589510094144,0.0078341048990585097],
      [3000,8.8826310779204274e-202,0.0013069052956699871,0.12669583238092633,0.87199170128103454,5.5610423691183971e-06],
      [5800,4.3974341266354599e-102,0.1016317601569131,0.46631284203741985,0.4320546215201847,7.7628548235064554e-07],
      [9950,7.5467774496592871e-58,0.43968985154490081,0.40659235354065371,0.15371764055798748,1.5435645799215148e-07],
      [200,0,6.4335414887093252e-77,1.1005996744445027e-35,0.9855538386660655,0.014446161333934547],
      [11000,5.5269720803783761e-52,0.5125926719617766,0.36462279409076875,0.12278441964879989,1.1429865472746461e-07]]){
    const got=BANDS.map(bd=>bandFrac(bd.lo,bd.hi,T));
    [xr,uv,vis,ir,far].forEach((v,i)=>{ if(v===0) ok(got[i]<1e-300,BANDS[i].name+' at '+T+' K is nothing (derive)'); else rel(got[i],v,v<1e-20?2e-13:5e-15,BANDS[i].name+' share at '+T+' K (derive, 50-digit)'); });
    close(got.reduce((a,b)=>a+b,0),1,2e-15,'the five bands add to 1 at '+T+' K');
  }
  rel(bandFrac(380,780,3000),0.1266958323809263,1e-13,'visible share at 3000 K = scipy quad of the curve (derive)');
  rel(bandFrac(380,780,5800),0.46631284203741985,1e-13,'visible share at 5800 K = scipy quad (derive)');
  for(const [T,vals] of [[250,[3.42034004156147e-29,2.04650401808914e-13,5.94858205194054e-06,0.0128500798613373,0.273229259957232,0.737789418018918,0.945053269119389]],
      [3000,[0.110310417267128,0.564303395949809,0.889989383274643,0.98081238947488,0.997188224804136,0.999620282234733,0.999950693562118]],
      [5800,[0.540803319460647,0.881052192170343,0.978994154689102,0.996903928854699,0.999580739245757,0.999945486236506,0.999993051308683]],
      [9950,[0.83255933427014,0.968525797145016,0.995224357232656,0.999344347953479,0.999914180510666,0.999989025023556,0.999998612465717]]])
    ZOOM_X.forEach((z,i)=>rel(fracBelow(z,T),vals[i],2e-13,'share of sigma T^4 inside 0-'+z+' nm at '+T+' K (derive)'));

  /* ---------- F. colorimetry: the CIE's own table ---------- */
  eq(CIE1931.length,95,'95 rows of the CIE table'); eq(CIE1931[0][0],360,'from 360 nm'); eq(CIE1931[94][0],830,'to 830 nm');
  { let steps=true; for(let i=1;i<CIE1931.length;i++) if(CIE1931[i][0]-CIE1931[i-1][0]!==5) steps=false; ok(steps,'every 5 nm');
    let X=0,Y=0,Z=0; for(const r of CIE1931){ X+=r[1]; Y+=r[2]; Z+=r[3]; }
    rel(X*5,106.865699943105,1e-13,'sum of xbar x 5 nm (derive from the CSV)'); rel(Y*5,106.85703925234998,1e-13,'sum of ybar x 5 nm (derive)'); rel(Z*5,106.89332154494998,1e-13,'sum of zbar x 5 nm (derive)'); }
  { const r=CIE1931.find(q=>q[0]===555); rel(r[2],1,1e-12,'ybar(555 nm) = 1.000000, the table row'); }
  const CH=[[800,0.681334738777667,0.317930991675008,3.72097505122571e-05,[255,0,0]],[1000,0.65275080858364,0.344461590087379,0.0123592498011946,[255,23,0]],
    [1500,0.585717831163533,0.393121453563272,35.6030213649031,[255,102,0]],[2000,0.526677308244141,0.413297199107361,2133.17179646733,[255,139,22]],
    [2500,0.476994319687044,0.4136755411297,25867.6451786036,[255,164,73]],[3000,0.436930774697901,0.404074069608543,138994.474802072,[255,184,109]],
    [4000,0.380439140070968,0.376746638426686,1162835.60115394,[255,211,165]],[5000,0.345100661670466,0.351607510055682,4223024.78660672,[255,230,208]],
    [5800,0.325982050676987,0.335318336039096,8668401.41025197,[255,241,235]],[6500,0.313525224670251,0.323627285858578,14132671.1673983,[255,248,254]],
    [8000,0.295186272657197,0.304763792097154,30578887.5941449,[227,231,255]],[9950,0.280910792508036,0.288614128363655,60135259.202381,[205,217,255]],
    [11000,0.275714030549718,0.282393526670432,79061943.3206782,[198,212,255]]];
  for(const [T,x,y,Yv,rgb] of CH){
    const c=chroma(T); close(c[0],x,1e-12,'x at '+T+' K (derive, CIE table)'); close(c[1],y,1e-12,'y at '+T+' K (derive)');
    rel(bbXYZ(T)[1],Yv,1e-12,'Y at '+T+' K (derive)'); eq(bbBytes(T).join(','),rgb.join(','),'sRGB bytes at '+T+' K (derive)');
  }
  { const lin=bbLinear(5800); rel(lin[1],0.879456404169,1e-10,'linear green at 5800 K (derive)'); rel(lin[2],0.827193577034,1e-10,'linear blue (derive)'); eq(lin[0],1,'red is the largest'); }
  /* the chain against the CIE's own Illuminant A: Planck at 2848 K x c2/1.435e-2 */
  { const TA=2848*C2/1.435e-2; rel(TA,2855.4958516593747,1e-14,'Illuminant A is a Planck body at 2855.496 K (derive; the fit to the CIE table agrees to 3e-8)');
    const c=chroma(TA); close(c[0],0.44757329319030936,1e-12,'its x, 5-nm sums (derive)'); close(c[1],0.4074395226431754,1e-12,'its y (derive)');
    close(c[0],0.4475735140989105,5e-7,'within 5e-7 of the x the CIE A table itself gives (CIE)'); close(c[1],0.40743944430666068,5e-7,'and the y (CIE)'); }
  close(SRGB_M[0][0]*0.95047+SRGB_M[0][1]*1+SRGB_M[0][2]*1.08883,1,1e-5,'the sRGB matrix maps D65 white to r = 1');
  close(srgbGamma(0.5),0.7353569830524495,1e-12,'the sRGB transfer curve at 0.5'); close(srgbGamma(1),1,1e-15,'and 1 -> 1'); eq(srgbGamma(-1),0,'clamped below');
  for(const [nm,r,g,b] of [[450,0.159041536159,0,1],[460,0.0630581662206,0,1],[550,0.0250050387243,1,0],[580,1,0.494858899489,0],[640,1,0,0.073728762523],[700,1,0,0.0918864450988]]){
    const v=monoLinear(nm); close(v[0],r,1e-11,nm+' nm: linear r (derive)'); close(v[1],g,1e-11,nm+' nm: g (derive)'); close(v[2],b,1e-11,nm+' nm: b (derive)'); }
  eq(monoLinear(4600).join(','),'0,0,0','4600 (angstroms fed to a nanometre helper) is black, not red');
  eq(monoLinear(0.46).join(','),'0,0,0','0.46 (micrometres) is black too');
  eq(monoLevel(900),0,'no light outside the table');
  close(monoLevel(700),Math.sqrt(4*0.004102),1e-12,'the band fades as sqrt(4 ybar): at 700 nm ybar = 0.004102 (the CIE row)'); eq(monoLevel(555),1,'full at 555 nm');
  { const v=monoLinear(552.5), a=monoLinear(550), b=monoLinear(555); ok(v[0]>Math.min(a[0],b[0])-1e-12&&v[0]<Math.max(a[0],b[0])+1e-12,'552.5 nm interpolates between its rows'); }
  for(const [T,e] of [[3000,20.6690961255607],[5800,92.2647919774293],[9950,73.9002370219532],[11000,65.0437708898556],[6500,95.3629757605143]])
    rel(efficacy(T),e,1e-12,'luminous efficacy at '+T+' K (derive)');
  { let a=4000, b=9000; const g=(Math.sqrt(5)-1)/2; let c=b-g*(b-a), d=a+g*(b-a);
    for(let i=0;i<60;i++){ if(efficacy(c)>efficacy(d)) b=d; else a=c; c=b-g*(b-a); d=a+g*(b-a); }
    close((a+b)/2,6627.8318225858293,0.5,'the most efficacious blackbody is at 6628 K (derive)'); rel(efficacy((a+b)/2),95.428620905689868,1e-9,'at 95.43 lm/W (derive)'); }
  for(const [T,ly] of [[800,-11.5795674959786],[1000,-9.05823214396099],[2000,-3.82119842104318],[3000,-2.00722671723982],[5800,-0.212285239990177],[11000,0.747743230868433]])
    close(glowLevel(T),clamp(1+ly/12,0,1),1e-12,'glow level at '+T+' K from log10 Y/Y(6500) (derive)');
  eq(glowLevel(200),0,'200 K does not glow');

  /* ---------- G. PhET's photometer, reproduced ---------- */
  for(const [T,r,rgb,raw,hr,ha] of [[200,0,[0,0,0],[0,0,0],5,0],[798,0,[0,0,0],[0,0,0],5,0],
      [800,0.0282842712474619,[7,0,0],[7.212489168,0.1086521451,0.0002069982459],6.34350288425,0.00848528137424],
      [1000,0.284253408071038,[72,2,0],[72.48461906,2.986476025,0.02433615129],18.5020368834,0.0852760224213],
      [2000,0.693397432934389,[176,54,8],[176.8163454,54.49413837,8.124016647],37.9363780644,0.20801922988],
      [3000,0.938509456532005,[239,144,56],[239.3199114,144.1844255,56.63121029],49.5791991853,0.28155283696],
      [3298,1,[255,173,81],[255,173.3608618,81.10747651],52.5,0.3],
      [4000,1.13172434806361,[254,214,136],[255,214.4084915,136.5674534],58.756906533,0.339517304419],
      [5800,1.41449637680695,[223,255,253],[223.8727507,255,253.489364],72.1885778983,0.424348913042],
      [9950,1.91332171889622,[117,173,255],[117.2982006,173.4657375,255],95.8827816476,0.573996515669],
      [11000,2.02009900747463,[108,165,254],[108.232225,165.2538189,255],100.954702855,0.606029702242]]){
    close(phRenorm(T),r,1e-13,'PhET ramp r at '+T+' K (derive)');
    const pr=photometerRaw(T), pf=photometer(T);
    for(let c=0;c<3;c++){
      if(raw[c]===0) eq(pr[c],0,'channel '+c+' dark at '+T+' K'); else rel(pr[c],raw[c],2e-9,'channel '+'RGB'[c]+' before the floor at '+T+' K (derive)');
      if(raw[c]===255) ok(pf[c]===254||pf[c]===255,'the brightest channel at '+T+' K floors to 254 or 255 ('+pf[c]+'): 255·v/v is not always 255 in floating point, in PhET too');
      else eq(pf[c],rgb[c],'channel '+'RGB'[c]+' at '+T+' K (derive)');
    }
    rel(haloRadius(T),hr,1e-11,'halo radius at '+T+' K (derive)'); close(haloAlpha(T),ha,1e-12,'halo opacity at '+T+' K (derive)');
  }
  { const p=photometer(5800), c=bbBytes(5800);
    ok(p[2]>p[0]&&c[0]>c[2],'the finding: PhET’s photometer paints the Sun bluish (B > R), colorimetry warm (R > B)');
    const p3=photometer(3000), c3=bbBytes(3000);
    ok(p3[2]<c3[2]&&p3[1]<c3[1],'and a 3000 K filament deeper orange than the eye sees'); }

  /* ---------- H. the classical limits ---------- */
  for(const [x,rj,w] of [[1e-3,1.0005001667083417,0.00099950016662500845],[1e-2,1.0050167084168058,0.0099501662508319471],[0.1,1.0517091807564762,0.095162581964040427],
      [1,1.7182818284590453,0.63212055882855767],[X5,28.664984318811157,0.99302284634885529],[10,2202.5465794806719,0.99995460007023751],[30,356215819384.11542,0.99999999999990641]]){
    rel(rjRatio(x),rj,1e-14,'RJ/Planck at x = '+fmt(x,4)+' (derive)'); rel(wienRatio(x),w,1e-14,'Wien/Planck at x = '+fmt(x,4)+' (derive)'); }
  for(const [L,T] of [[500,5800],[20000,250],[3000,11000],[100000,3000]]){
    const x=xOf(L,T);
    rel(rjExitance(L*NM,T)/exitance(L*NM,T),rjRatio(x),1e-13,'the laws divided = (e^x - 1)/x at '+L+' nm, '+T+' K (two routes)');
    rel(wienExitance(L*NM,T)/exitance(L*NM,T),wienRatio(x),1e-13,'Wien over Planck = 1 - e^-x there (two routes)'); }
  rel(X_RJ1,0.019867767798097204,1e-12,'Rayleigh-Jeans is 1 % high at x = 0.019868 (derive brentq)'); rel(X_W1,4.6051701859880918,1e-15,'Wien 1 % low at x = ln 100');
  { const Lm=withState({view:'limits',T:5800},()=>limitsModel(ST));
    rel(Lm.lamRJ1/1000,124.85800186558778,1e-12,'at 5800 K, RJ within 1 % only beyond 124.9 um (derive)'); rel(Lm.lamW1/1000,0.53866625740512863,1e-12,'Wien within 1 % below 0.539 um (derive)'); }

  /* ---------- I. the state and PhET's controls ---------- */
  eq(snapT(5823),5800,'the thermometer snaps to 50 K'); eq(snapT(5826),5850,'rounding up'); eq(snapT(0),200,'clamped at 200 K'); eq(snapT(1e6),11000,'and 11000 K');
  eq(ZOOM_X.join(','),'750,1500,3000,6000,12000,24000,48000','the wavelength ladder, x2 (PhET)');
  rel(ZOOM_Y[0],1.024e-5,1e-12,'the power ladder starts at 1.024e-5 (PhET)'); eq(ZOOM_Y[IY_DEFAULT],100,'defaults to 100'); eq(ZOOM_Y[12],2500,'ends at 2500');
  for(let i=1;i<ZOOM_Y.length;i++) if(Math.abs(ZOOM_Y[i]/ZOOM_Y[i-1]-5)>1e-12) ok(false,'the power ladder steps x5');
  /* 4500 K separates the factor 5 from 4: 5 lambda_max = 3220 nm needs the 6-um axis, 4 lambda_max would fit 3 um
     (at every preset the two round up to the same ladder value, so the presets alone pin nothing) */
  for(const [T,ix,iy] of [[5800,2,10],[250,6,1],[3000,3,8],[9950,1,12],[200,6,0],[11000,1,12],[4500,3,10]]){
    const f=fitZoom(T); eq(f.join(','),ix+','+iy,'fit the axes at '+T+' K');
    ok(ZOOM_X[f[0]]>=5*peakNm(T)||f[0]===6,'  the fitted wavelength axis shows 5 lambda_max'); ok(ZOOM_Y[f[1]]>=peakPow(T),'  and the fitted power axis the peak'); }
  withState({},()=>{
    setT(3000); rel(ST.gvNm,peakNm(3000),1e-15,'a new temperature sends Graph Values to the peak (PhET)');
    ST.gvNm=2000; setGraphValues(true); rel(ST.gvNm,peakNm(3000),1e-15,'so does switching Graph Values on');
    zoomX(-1); zoomX(-1); zoomX(-1); eq(ST.ix,0,'wavelength zoom-in stops at 750 nm'); for(let i=0;i<9;i++) zoomX(1); eq(ST.ix,6,'zoom-out at 48 um');
    for(let i=0;i<20;i++) zoomY(-1); eq(ST.iy,0,'power zoom-in stops at 1.024e-5'); for(let i=0;i<20;i++) zoomY(1); eq(ST.iy,12,'zoom-out at 2500');
    setT(9950); fitAxes(); eq(ST.ix+','+ST.iy,'1,12','fit the axes on Sirius A');
    saveCurve(); setT(3000); saveCurve(); setT(250); saveCurve(); eq(SAVED.join(','),'3000,250','PhET keeps the two newest saved curves');
    eraseSaved(); eq(SAVED.length,0,'erase clears them');
    /* reset: disturb EVERY kind of state first */
    ST.view='star'; setT(700); ST.ix=5; ST.iy=3; ST.gv=true; ST.labels=true; ST.inten=true; ST.gvCue=false; ST.rj=false; ST.wien=false; ST.gvNm=123; saveCurve();
    resetAll();
    ok(ST.T===5800&&ST.ix===2&&ST.iy===10&&!ST.gv&&!ST.labels&&!ST.inten&&ST.gvCue&&ST.rj&&ST.wien&&SAVED.length===0,'reset all restores T, both zooms, the checkboxes, the cue and the saved curves');
    eq(ST.view,'star','and keeps the view'); rel(ST.gvNm,peakNm(5800),1e-15,'with Graph Values back on the peak');
  });

  /* ---------- J. the models, the readouts ---------- */
  for(const [v] of TABS) for(const over of [{},{T:200},{T:11000},{T:250,gv:true,labels:true,inten:true,ix:0,iy:0},{T:9950,gv:true,gvNm:40000,ix:6,iy:0}])
    withState(Object.assign({view:v},over),()=>{ const M=buildModel(); const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
      ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over)); },[3000,250]);
  withState({view:'spec'},()=>{ const h2=readoutHTML(buildModel()); ok(h2.indexOf('6.42×10⁷')>=0,'the spectrum readout prints sigma T^4 = 6.42x10^7 W/m^2 off the model'); ok(h2.indexOf('0.4996 µm')>=0,'and lambda_max = 0.4996 um'); });
  withState({view:'spec',gv:true,gvNm:1000},()=>{ ok(readoutHTML(buildModel()).indexOf('34.17')>=0,'Graph Values at 1 um prints M = 34.17'); });
  withState({view:'star'},()=>{ const h2=readoutHTML(buildModel()); ok(h2.indexOf('0.3260, 0.3353')>=0,'the star readout prints the chromaticity'); ok(h2.indexOf('#fff1eb')>=0,'and the sRGB colour'); ok(h2.indexOf('223 255 253')>=0,'and PhET’s channels'); });
  withState({view:'peak'},()=>{ ok(readoutHTML(buildModel()).indexOf('2.897772')>=0,'the peak readout prints b = 2.897772 mm K'); });
  withState({view:'total'},()=>{ ok(readoutHTML(buildModel()).indexOf('46.6 %')>=0,'the total readout prints the Sun’s 46.6 % visible'); });
  withState({view:'limits'},()=>{ ok(readoutHTML(buildModel()).indexOf('28.66')>=0,'the limits readout prints RJ 28.66x too high at the peak'); });
  eq(sci(64168769.43,3),'6.42×10⁷','sci() uses superscript exponents'); eq(sci(9.996e7,3),'1.00×10⁸','and carries 9.996 up to 1.00'); eq(sci(84.45,3),'84.5','plain in the middle');

  /* ---------- K. what the spectrum view draws, measured on the drawing ---------- */
  withState({view:'spec',labels:true,gv:true,gvNm:1000},()=>{
    const shot=makeShot(1400,820), M=buildModel(); drawView(shot,1400,820,M);
    const g=SPEC_LAST.g, b=g.b, X=nm=>b.x+b.w*nm/M.S.xmax, Y=v=>b.y1-b.h*v/M.S.ymax;
    close(SPEC_LAST.band[0],X(380),1e-9,'the rainbow starts at 380 nm on the axis (a unit check on the band)'); close(SPEC_LAST.band[1],X(780),1e-9,'and ends at 780 nm');
    close(SPEC_LAST.peak[0],X(peakNm(5800)),1e-9,'Wien’s diamond sits at lambda_max'); close(SPEC_LAST.peak[1],Y(peakPow(5800)),1e-9,'at the peak height');
    close(SPEC_LAST.curveTop,Y(peakPow(5800)),1e-9,'the drawn curve reaches exactly the peak (the peak sample is inserted)');
    close(SPEC_LAST.gv[0],X(1000),1e-9,'the Graph Values point sits at 1 um'); close(SPEC_LAST.gv[1],Y(specPow(1000,5800)),1e-9,'on the curve');
    eq(SPEC_LAST.bands.join(','),'uv,vis,ir','labels at 3 um: ultraviolet, visible, infrared (the X-ray band is under 20 px)');
  });
  withState({view:'spec',labels:true,ix:0},()=>{ drawView(makeShot(1400,820),1400,820,buildModel()); eq(SPEC_LAST.bands.join(','),'uv,vis','at 750 nm: ultraviolet and visible'); });
  withState({view:'spec',labels:true,ix:6},()=>{ drawView(makeShot(1400,820),1400,820,buildModel()); eq(SPEC_LAST.bands.join(','),'ir','at 48 um only the infrared is 20 px wide'); });
  withState({view:'spec',gv:true,gvNm:800,ix:0},()=>{ drawView(makeShot(1400,820),1400,820,buildModel()); eq(SPEC_LAST.gv,null,'Graph Values just past the 750 nm axis (at 800 nm) is hidden, as PhET’s'); });
  withState({view:'spec',gv:true,gvNm:750,ix:0},()=>{ drawView(makeShot(1400,820),1400,820,buildModel()); ok(SPEC_LAST.gv!==null,'and at the axis end (750 nm) it is drawn'); });
  withState({view:'spec',T:9950,gv:true},()=>{ const M=buildModel(); ok(M.S.over&&M.S.gv.above,'Sirius A overflows the default axis'); drawView(makeShot(1400,820),1400,820,M); eq(SPEC_LAST.gv,null,'and its point, above the axis, is hidden'); });
  withState({view:'spec',T:250},()=>{ const M=buildModel(); ok(M.S.tiny&&!M.S.peakIn,'the Earth at the default zoom: too small and past the axis'); ok(specWarning(M.S).indexOf('beyond this axis')>=0,'the canvas says to zoom out'); });
  withState({view:'spec',T:3000},()=>{ const M=buildModel(); ok(!M.S.tiny&&M.S.peakIn&&!M.S.over,'the light bulb (peak 3.1 of 100) is neither tiny (< 1 %) nor off the axis'); eq(specWarning(M.S),'','so no warning'); });
  withState({view:'spec',T:1500},()=>{ const M=buildModel(); ok(M.S.tiny,'1500 K peaks at '+sigf(M.S.Mp,3)+', under 1 % of 100: tiny'); ok(specWarning(M.S).indexOf('under 1 %')>=0,'and the canvas says so'); });
  withState({view:'spec'},()=>{ ok(readoutHTML(buildModel()).indexOf('97.9 %')>=0,'the readout prints the 97.9 % of sigma T^4 inside 0-3 um'); });
  eq(axisMax(3),'3','axis maxima print as PhET’s ladder values: 3'); eq(axisMax(0.75),'0.75','0.75'); eq(axisMax(ZOOM_Y[1]),'5.12×10⁻⁵','5.12x10^-5'); eq(axisMax(ZOOM_Y[0]),'1.024×10⁻⁵','1.024x10^-5'); eq(axisMax(ZOOM_Y[3]),'0.00128','0.00128');

  /* ---------- L. the scene and the pointer ---------- */
  withState({view:'spec'},()=>{
    const shot=makeShot(1400,820), S=makeScene({getContext:()=>shot}); S.W=1400; S.H=820;
    const g=specGeo(shot,1400,820,buildModel()), th=g.th;
    ok(!!th,'the thermometer is drawn at 1400 x 820');
    ok(S.pointer('down',th.x+6,thermoY(th,3000)),'pointer-down on the thermometer grabs it'); eq(ST.T,3000,'and sets 3000 K'); eq(DRAG.what,'thermo','it is the thermometer');
    S.pointer('move',th.x+6,thermoY(th,9950)); eq(ST.T,9950,'dragging sets 9950 K');
    S.pointer('move',th.x+6,thermoY(th,9971)); eq(ST.T,9950,'and snaps to 50 K');
    S.pointer('move',th.x+6,th.yTop-200); eq(ST.T,11000,'clamped at 11000 K'); S.pointer('move',th.x+6,th.bulbY+300); eq(ST.T,200,'and 200 K');
    ok(S.pointer('up',0,0),'pointer-up releases'); eq(DRAG.what,null,'nothing dragged');
    setT(5800); ST.gv=true; ST.gvNm=peakNm(5800);
    const M=buildModel(), b=specGeo(shot,1400,820,M).b, gx=b.x+b.w*ST.gvNm/M.S.xmax, gy=b.y1-b.h*M.S.gv.M/M.S.ymax;
    ok(S.pointer('down',gx+3,gy-2),'pointer-down on the Graph Values point grabs it'); eq(DRAG.what,'gv','it is the point');
    S.pointer('move',b.x+b.w/3+3,gy); rel(ST.gvNm,1000,1e-9,'dragged to 1 um along the curve');
    S.pointer('move',b.x1+400,gy); eq(ST.gvNm,M.S.xmax,'clamped at the axis end'); S.pointer('move',b.x-400,gy); eq(ST.gvNm,0,'and at 0');
    ok(ST.gvCue,'the cue arrows show until the first drag ends'); S.pointer('up',0,0); ok(!ST.gvCue,'then hide, as PhET’s');
    ok(!S.pointer('down',b.x+b.w*0.9,b.y+20),'a pointer-down on empty plot grabs nothing');
    ST.view='peak'; ok(!S.pointer('down',th.x+6,thermoY(th,3000)),'the other views ignore the pointer');
  });

  /* ---------- M. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  /* substance floors per configuration, [fills + strokes, curve segments, texts]: 80 % of the least that
     configuration emits at any of the four sizes (set_floors.py from a SUB diagnostic run) — derived,
     not copied; a view that legitimately draws little (a curve off the top of the axis) has a low floor */
  const CONFIGS=[
    ['spec default',{view:'spec'},null,[76,480,12]],['spec all on',{view:'spec',gv:true,labels:true,inten:true,gvNm:1500},[3000,9950],[88,1294,16]],
    ['spec earth',{view:'spec',T:250},null,[73,480,12]],['spec earth fitted',{view:'spec',T:250,ix:6,iy:1,gv:true,labels:true,inten:true},[200],[28,961,16]],
    ['spec sirius 750',{view:'spec',T:9950,ix:0,labels:true,gv:true},null,[213,78,15]],['spec 11000 zoomed in',{view:'spec',T:11000,iy:0,labels:true,inten:true},null,[80,6,16]],
    ['spec 200 max zoom',{view:'spec',T:200,ix:6,iy:0,gv:true,labels:true},[11000],[27,481,15]],['spec gv past',{view:'spec',gv:true,gvNm:2000,ix:0},[5800],[212,961,12]],
    ['star default',{view:'star'},null,[368,0,12]],['star 200',{view:'star',T:200},null,[368,0,12]],['star 800',{view:'star',T:800},null,[368,0,12]],['star 3000',{view:'star',T:3000},null,[368,0,12]],['star 11000',{view:'star',T:11000},null,[368,0,12]],
    ['peak default',{view:'peak'},null,[23,1120,16]],['peak 200',{view:'peak',T:200},null,[23,982,16]],['peak 11000',{view:'peak',T:11000},null,[23,1128,16]],
    ['total default',{view:'total'},null,[22,160,20]],['total 200',{view:'total',T:200},null,[22,160,20]],['total 11000',{view:'total',T:11000},null,[22,160,20]],
    ['limits default',{view:'limits'},null,[15,676,16]],['limits no rj',{view:'limits',rj:false},null,[13,473,14]],['limits none',{view:'limits',rj:false,wien:false},null,[12,251,13]],
    ['limits 200',{view:'limits',T:200},null,[14,504,15]],['limits 11000',{view:'limits',T:11000},null,[15,655,16]]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const SUB_DIAG=(typeof SUB_DIAG_ON!=='undefined');
  for(const [nm,over,saved,minFills] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), marks=c.ops.filter(o=>o.op==='fill'||o.op==='stroke').length, segs=POLY_SEGS.length/4;
      if(SUB_DIAG) console.log('SUB '+nm+' '+W+'x'+H+' marks '+marks+' segs '+segs+' texts '+texts.length);
      ok(marks>=minFills[0]&&segs>=minFills[1]&&texts.length>=minFills[2],nm+' '+W+'x'+H+' draws substance ('+marks+' marks, '+segs+' curve segments, '+texts.length+' texts; floors '+minFills.join('/')+')');
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
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    },saved);
  }

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
