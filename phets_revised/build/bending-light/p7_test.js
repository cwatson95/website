
/* ================================================================== *
 *  selfTest — headless verification.  Every reference value labelled  *
 *  (derive) is a printed line of build/bending-light/refvals.txt, the *
 *  output of derive.py — an independent Python solve of the same      *
 *  optics, with scipy.minimize_scalar on the prism's minimum          *
 *  deviation and on the rainbow's stationary ray — read in full.      *
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
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),
    name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    const keep=Object.assign({},ST);
    Object.assign(ST,over); clearMemo();
    try{ fn(); } finally { Object.assign(ST,keep); clearMemo(); }
  }
  const NA=1.000293, NW=1.333, NG=1.5, ND=2.419, NMB=1.4;

  /* ---------------------------------------------------------- 0. units */
  close(DEG*90,PI/2,1e-15,'DEG turns degrees into radians (90 deg = pi/2)');
  close(RAD*PI/2,90,1e-13,'RAD turns radians into degrees');
  close(DEG*RAD,1,1e-15,'DEG and RAD are inverses');

  /* ------------------------------------------------------ 1. dispersion */
  close(sellmeier(650*NM),1.51452030856478,1e-13,'BK7 at 650 nm (derive)');
  close(sellmeier(587.5618*NM),1.51680003450059,1e-13,'BK7 n_d (derive)');
  close(sellmeier(486.1327*NM),1.52237628973123,1e-13,'BK7 n_F (derive)');
  close(sellmeier(656.2725*NM),1.51432234726137,1e-13,'BK7 n_C (derive)');
  /* SCHOTT publishes n_d and V_d beside the coefficients; reproducing them
     validates the coefficients, the three Fraunhofer lines and the evaluator
     at once (the lenses.html lesson) */
  close(sellmeier(587.5618*NM),1.5168,1e-4,'BK7 n_d against SCHOTT’s published 1.5168');
  const Vd=(sellmeier(587.5618*NM)-1)/(sellmeier(486.1327*NM)-sellmeier(656.2725*NM));
  close(Vd,64.1673362374998,1e-10,'BK7 Abbe number (derive)');
  close(Vd,64.17,0.01,'BK7 Abbe number against SCHOTT’s published 64.17');
  close(airIndex(650*NM),1.00027632405835,1e-14,'air at 650 nm (derive)');
  close(airIndex(589.3*NM),1.00027714731598,1e-14,'air at 589.3 nm (derive)');
  close(airIndex(589.3*NM),1.0002765,1e-6,'air at 589.3 nm against the published 1.0002765');
  close(airIndex(400*NM),1.00028276182348,1e-14,'air at 400 nm (derive)');
  close(blendFraction(NA),3.24280733438869e-05,1e-16,'blend weight, air (derive)');
  close(blendFraction(NW),0.647015202834111,1e-13,'blend weight, water (derive)');
  close(blendFraction(NG),0.971763775557402,1e-13,'blend weight, glass (derive)');
  close(blendFraction(ND),2.75885322665144,1e-13,'blend weight, diamond (derive)');
  close(blendFraction(NMB),0.777303552369802,1e-13,'blend weight, Mystery B (derive)');
  ok(blendFraction(0.5)===0,'a sub-air index clamps the blend weight at zero, as PhET does');
  {
    const lams=[380,400,450,500,550,600,650,700];
    const refW=[1.34544126630196,1.34356688527447,1.33998872871036,1.33746156631717,
                1.33558994026188,1.3341483725286,1.333,1.33205756100781];
    const refG=[1.5186819432583,1.51586736390458,1.51049438468361,1.50669957677505,
                1.50388911819125,1.50172443050126,1.5,1.49858479469578];
    const refD=[2.47202435117973,2.46403586606668,2.44878598851242,2.4380153349235,
                2.43003848655707,2.42389447407538,2.419,2.41498316451161];
    let w=0;
    for(let i=0;i<lams.length;i++){
      w=Math.max(w,Math.abs(indexOf(NW,lams[i])-refW[i]),
                   Math.abs(indexOf(NG,lams[i])-refG[i]),
                   Math.abs(indexOf(ND,lams[i])-refD[i]));
    }
    close(w,0,1e-13,'n(lambda) for water, glass and diamond at eight wavelengths (derive)');
  }
  /* PhET's substance table, pinned entry by entry: a test that only ever
     uses its own literals leaves the table itself unasserted */
  {
    const WANT={air:1.000293,water:1.333,glass:1.5,diamond:2.419,mysteryA:2.419,mysteryB:1.4};
    for(const id in WANT) close(subById(id).n,WANT[id],0,'PhET\u2019s index for '+id);
    eq(SUBS.length,7,'seven substances, PhET\u2019s six plus a custom one');
    eq(subById('custom').n,null,'and the custom one takes its index from the slider');
    ok(subById('mysteryA').mystery&&subById('mysteryB').mystery,'the two mystery ones are marked');
    ok(!subById('diamond').phet,'diamond is marked as NOT in PhET\u2019s own chooser');
    close(PHET.nCustom0,subById('mysteryB').n+1.2,1e-15,
          'PhET builds its custom substance as Mystery B + 1.2 = '+PHET.nCustom0);
    close(PHET.nSliderLo,subById('air').n,0,'and its index slider starts at air');
    close(PHET.nSliderHi,1.6,0,'and stops at 1.6 (PhET\u2019s value)');
  }
  /* by construction n(650) = n_ref EXACTLY — the one identity of the model */
  for(const s of SUBS){
    if(s.n===null) continue;
    eq(indexOf(s.n,PHET.lamRed)-s.n,0,'n('+s.id+', 650 nm) is exactly its stated index');
  }
  close(indexOf(NW,400)-indexOf(NW,700),0.0115093242666571,1e-14,'water dispersion span (derive)');
  close(indexOf(NG,400)-indexOf(NG,700),0.017282569208797,1e-14,'glass dispersion span (derive)');
  close(indexOf(ND,400)-indexOf(ND,700),0.0490527015550648,1e-14,'diamond dispersion span (derive)');
  ok(indexOf(ND,400)>indexOf(ND,700)&&indexOf(NW,400)>indexOf(NW,700),
     'normal dispersion: blue is bent more than red, in every substance');

  /* ----------------------------------------------------------- 2. Snell */
  {
    const THS=[0,5,15,30,45,60,75,89];
    const REF={
      'air-water':[1.000293,1.333,[0,3.74995296733062,11.1991450823223,22.0369018089172,
        32.0472287061937,40.5319390929978,46.4553598194852,48.6157701311494]],
      'water-air':[1.333,1.000293,[0,6.66964676016694,20.1759802443562,41.7825020151092,
        70.4409983823734,NaN,NaN,NaN]],
      'air-glass':[1.000293,1.5,[0,3.33195728318183,9.9388245053715,19.4771560785104,
        28.1344794612608,35.2762612231222,40.1011684104501,41.8175232055019]],
      'glass-air':[1.5,1.000293,[0,7.50977405776715,22.8372506126502,48.5713516270856,
        NaN,NaN,NaN,NaN]],
      'air-diamond':[1.000293,2.419,[0,2.06539948377155,6.14388150713087,11.9324034110216,
        17.001654749303,20.9844504897388,23.5422313683603,24.4218761453148]],
      'diamond-air':[2.419,1.000293,[0,12.167362013248,38.7482668794899,NaN,NaN,NaN,NaN,NaN]],
      'water-glass':[1.333,1.5,[0,4.44214471113417,13.2972988885948,26.380693513073,
        38.9308667181934,50.3186924549269,59.1358526271484,62.6892693024607]],
      'glass-water':[1.5,1.333,[0,5.62831557825094,16.9324613520445,34.2386144250128,
        52.7208598655134,77.0388087755532,NaN,NaN]],
    };
    let worst=0, tirOK=true;
    for(const k in REF){
      const [n1,n2,row]=REF[k];
      for(let i=0;i<THS.length;i++){
        const got=refractAngle(n1,n2,THS[i]*DEG);
        if(isNaN(row[i])){ if(isFinite(got)) tirOK=false; continue; }
        worst=Math.max(worst,Math.abs(got*RAD-row[i]));
      }
    }
    close(worst,0,1e-12,'theta_2 over eight medium pairs x eight angles (derive)');
    ok(tirOK,'and every entry derive.py reports as total internal reflection is NaN here too');
  }
  close(criticalAngle(NW,NA)*RAD,48.6256762914095,1e-12,'critical angle water->air (derive)');
  close(criticalAngle(NG,NA)*RAD,41.8253319987773,1e-12,'critical angle glass->air (derive)');
  close(criticalAngle(ND,NA)*RAD,24.4258393111144,1e-12,'critical angle diamond->air (derive)');
  close(criticalAngle(NG,NW)*RAD,62.7061760793324,1e-12,'critical angle glass->water (derive)');
  ok(!isFinite(criticalAngle(NA,NW))&&!isFinite(criticalAngle(NW,NG)),
     'there is no critical angle entering a denser medium');
  /* AT the critical angle the refracted ray grazes at exactly 90 degrees */
  for(const [nm,n1,n2] of [['water->air',NW,NA],['glass->air',NG,NA],
                           ['diamond->air',ND,NA],['glass->water',NG,NW]]){
    const tc=criticalAngle(n1,n2);
    eq(refractAngle(n1,n2,tc)*RAD-90,0,'theta_2 at the critical angle is exactly 90 deg ('+nm+')');
    ok(!isFinite(refractAngle(n1,n2,tc*(1+1e-12))),'and one part in 10^12 past it there is no ray ('+nm+')');
  }
  /* round trips */
  {
    let worst=0;
    for(const [n1,n2] of [[NA,NW],[NW,NA],[NA,NG],[NG,NA],[NA,ND],[ND,NA],[NW,NG],[NG,NW]])
      for(const t of [0,5,15,30,45,60,75,89]){
        const a=refractAngle(n1,n2,t*DEG);
        if(!isFinite(a)) continue;
        worst=Math.max(worst,Math.abs(refractAngle(n2,n1,a)-t*DEG));
      }
    close(worst,0,1e-14,'every refraction round-trips back to its own angle');
  }
  /* the small-angle limit, asserted by its RATE of approach (Known-bad: never
     assert that a limit is reached exactly when it is reached to O(x)) */
  {
    const r=1/1.5, c3=-(r-r*r*r)/6;
    close(c3,-0.0617283950617284,1e-15,'the exact cubic coefficient -(r-r^3)/6 (derive)');
    for(const th of [1e-4,1e-3,1e-2]){
      const m=(refractAngle(1,1.5,th)-th/1.5)/(th*th*th);
      rel(m,c3,1e-3,'the measured cubic coefficient at theta = '+th);
    }
    ok(Math.abs((refractAngle(1,1.5,1e-2)-1e-2/1.5)/1e-6-c3)
       <Math.abs((refractAngle(1,1.5,1e-1)-1e-1/1.5)/1e-3-c3),
       'and it converges as the angle shrinks');
  }

  /* --------------------------------------------------------- 3. Fresnel */
  for(const [nm,n1,n2,ref] of [['air->water',NA,NW,0.0203322443503111],
                               ['air->glass',NA,NG,0.0399437703674046],
                               ['air->diamond',NA,ND,0.172152283915187],
                               ['water->glass',NW,NG,0.00347487985443108]]){
    close(fresnel(n1,n2,0).Rs,ref,1e-14,'R at normal incidence, '+nm+' (derive)');
    close(fresnel(n1,n2,0).Rs,Math.pow((n1-n2)/(n1+n2),2),1e-16,
          '  and it equals ((n1-n2)/(n1+n2))^2 exactly ('+nm+')');
    close(fresnel(n2,n1,0).Rs,ref,1e-14,'  reversing the pair leaves R(0) unchanged ('+nm+')');
    eq(fresnel(n1,n2,0).Rs,fresnel(n1,n2,0).Rp,'s and p agree at normal incidence ('+nm+')');
  }
  {
    const A=[0,10,30,45,56,60,75,85,89.9];
    const CASES=[['air->water',NA,NW,
      [0.0203322443503111,0.0212850564465698,0.0308759066893597,0.0529000573165104,
       0.091270973207421,0.11491576919278,0.313779900328386,0.673579308431779,0.992105429170503],
      [0.0203322443503111,0.019400363919706,0.0119125074633543,0.00279841606409008,
       0.000609929249185049,0.00431906454504018,0.1107288518744,0.493262131867812,0.986023361688642]],
      ['glass->air',NG,NA,
      [0.0399437703674046,0.0438249415741838,0.105578190319668,1,1,1,1,1,1],
      [0.0399437703674046,0.0362282022278072,0.00461318354733839,1,1,1,1,1,1]],
      ['air->diamond',NA,ND,
      [0.172152283915187,0.176538839998293,0.215392172126553,0.282675526425155,
       0.365954516093724,0.406286263389942,0.62555933713896,0.85360161306339,0.996834360255496],
      [0.172152283915187,0.167798132799359,0.131892287947658,0.0799054532397383,
       0.0324605784618318,0.0165260775410996,0.0355502222699572,0.389740763898647,0.98162827831078]]];
    let w=0;
    for(const [nm,n1,n2,rs,rp] of CASES) for(let i=0;i<A.length;i++){
      const f=fresnel(n1,n2,A[i]*DEG);
      w=Math.max(w,Math.abs(f.Rs-rs[i]),Math.abs(f.Rp-rp[i]));
    }
    close(w,0,1e-13,'R_s and R_p at nine angles for three pairs (derive)');
  }
  /* R + T = 1 exactly, in both polarisations, everywhere */
  {
    let ws=0,wp=0;
    for(const [n1,n2] of [[NA,NW],[NW,NA],[NA,NG],[NG,NA],[NA,ND],[ND,NA],[NW,NG],[NG,NW]])
      for(let i=0;i<=600;i++){
        const f=fresnel(n1,n2,i/600*89.999*DEG);
        ws=Math.max(ws,Math.abs(f.Rs+f.Ts-1)); wp=Math.max(wp,Math.abs(f.Rp+f.Tp-1));
      }
    close(ws,0,5e-15,'R_s + T_s = 1 over eight pairs x 601 angles (derive: 5.6e-16)');
    close(wp,0,5e-15,'R_p + T_p = 1 over eight pairs x 601 angles (derive: 6.7e-16)');
  }
  /* the transmitted power must carry the (n2 c2)/(n1 c1) factor: without it
     nothing adds to one.  Assert the factor is really there. */
  {
    const f=fresnel(NA,NG,50*DEG);
    const naive=f.ts*f.ts;
    ok(Math.abs(f.Ts-naive)>0.1,'T is not |t|^2: the beam-width factor is 0.32 of it here');
    close(f.Ts,(NG*Math.cos(f.th2))/(NA*Math.cos(50*DEG))*f.ts*f.ts,1e-15,'and T is exactly that factor times |t|^2');
  }
  /* Brewster */
  for(const [nm,n1,n2,tb,rs] of [['air->water',NA,NW,53.1151679682992,0.0781199737996813],
                                 ['air->glass',NA,NG,56.302185020193,0.14773701920765],
                                 ['air->diamond',NA,ND,67.5341672844752,0.501192662090117],
                                 ['water->glass',NW,NG,48.373574027842,0.0138034222763187]]){
    close(brewster(n1,n2)*RAD,tb,1e-12,'Brewster angle, '+nm+' (derive)');
    close(fresnel(n1,n2,brewster(n1,n2)).Rp,0,1e-30,'  R_p vanishes there ('+nm+')');
    close(fresnel(n1,n2,brewster(n1,n2)).Rs,rs,1e-14,'  R_s there (derive) ('+nm+')');
    close((brewster(n1,n2)+refractAngle(n1,n2,brewster(n1,n2)))*RAD,90,1e-12,
          '  theta_B + theta_2 = 90 deg exactly ('+nm+')');
    ok(fresnel(n1,n2,brewster(n1,n2)*0.9).Rp>1e-6&&fresnel(n1,n2,brewster(n1,n2)*1.1).Rp>1e-6,
       '  and R_p is nonzero on both sides of it ('+nm+')');
  }
  /* past and at the critical angle */
  for(const [nm,n1,n2] of [['water->air',NW,NA],['glass->air',NG,NA],
                           ['diamond->air',ND,NA],['glass->water',NG,NW]]){
    const tc=criticalAngle(n1,n2);
    const fa=fresnel(n1,n2,tc);
    eq(fa.Rs,1,'R_s = 1 AT the critical angle ('+nm+')');
    eq(fa.Rp,1,'R_p = 1 AT the critical angle ('+nm+')');
    eq(fa.Ts,0,'and nothing is transmitted there ('+nm+')');
    for(const e of [1e-9,0.01,0.2]){
      if(tc+e>=PI/2) continue;
      const f=fresnel(n1,n2,tc+e);
      ok(f.Rs===1&&f.Rp===1&&f.tir,'R = 1 exactly at theta_c + '+e+' ('+nm+')');
    }
    ok(fresnel(n1,n2,tc*0.98).Rs<1,'  but below it R_s is strictly under one ('+nm+')');
  }
  close(fresnel(NA,NW,89.999*DEG).Rs,0.999920744069434,1e-12,'grazing R_s, air->water (derive)');
  close(fresnel(NA,NW,89.999*DEG).Rp,0.999859257825603,1e-12,'grazing R_p, air->water (derive)');
  ok(fresnel(NA,NW,89.999*DEG).Rs<1&&fresnel(NA,NW,89.999*DEG).Rp<1,
     'grazing R approaches one FROM BELOW when there is no critical angle');
  /* the total-internal-reflection phase */
  {
    const REF=[[45,-0.642092519718427,-1.28418503943685],
               [60,-1.67053945036872,-2.37640699742852],
               [80,-2.67121192385416,-2.92926909021594]];
    let w=0;
    for(const [t,ps,pp] of REF){
      const f=fresnel(NG,NA,t*DEG);
      w=Math.max(w,Math.abs(f.phs-ps),Math.abs(f.php-pp));
    }
    close(w,0,1e-13,'the Goos-Hanchen phases of r_s and r_p, glass->air (derive)');
    /* and the complex form agrees with it */
    const f=fresnel(NG,NA,60*DEG), c=fresnelSComplex(NG,NA,60*DEG);
    close(cAbs(c.rRe,c.rIm),1,1e-15,'|r_s| = 1 under total internal reflection');
    close(cArg(c.rRe,c.rIm),f.phs,1e-13,'and its argument is the phase the real form reports');
  }
  /* reversibility: T(1->2 at th1) = T(2->1 at th2) */
  {
    let w=0;
    for(const [n1,n2] of [[NA,NW],[NW,NA],[NA,NG],[NG,NA],[NA,ND],[ND,NA],[NW,NG],[NG,NW]])
      for(let i=0;i<=85;i++){
        const f=fresnel(n1,n2,i*DEG);
        if(f.tir) continue;
        const g=fresnel(n2,n1,f.th2);
        w=Math.max(w,Math.abs(f.Ts-g.Ts),Math.abs(f.Tp-g.Tp));
      }
    close(w,0,1e-13,'T(1->2) = T(2->1) over eight pairs x 86 angles (derive: 4.8e-15)');
  }

  /* ------------------------------------------------------- 4. the wave */
  close(lambdaIn(650,indexOf(NW,650)),487.621905476369,1e-11,'650 nm in water (derive)');
  close(lambdaIn(650,indexOf(NG,650)),433.333333333333,1e-11,'650 nm in glass (derive)');
  close(lambdaIn(650,indexOf(ND,650)),268.706076891277,1e-11,'650 nm in diamond (derive)');
  close(1/indexOf(NW,650),0.750187546886722,1e-14,'v/c in water (derive)');
  close(speedIn(indexOf(NG,650)),199861638.666667,1e-5,'v in glass, m/s (derive)');
  close(PHET.c/(650*NM),461219166153846,1,'the frequency of 650 nm light, Hz (derive)');
  /* the frequency is the same on both sides: v/lambda is invariant */
  for(const n of [NW,NG,ND])
    close(speedIn(indexOf(n,650))/(lambdaIn(650,indexOf(n,650))*NM),PHET.c/(650*NM),1,
          'v/lambda inside the medium is the vacuum frequency (n = '+n+')');
  /* phase matching: lambda1/sin th1 = lambda2/sin th2 -- Snell, restated */
  {
    let w=0;
    for(const [n1,n2] of [[NA,NW],[NW,NA],[NA,NG],[NG,NA],[NA,ND],[ND,NA],[NW,NG],[NG,NW]])
      for(const t of [5,20,40,60,80]){
        const th1=t*DEG, th2=refractAngle(n1,n2,th1);
        if(!isFinite(th2)) continue;
        const a=650/n1/Math.sin(th1), b=650/n2/Math.sin(th2);
        w=Math.max(w,Math.abs(a-b)/a);
      }
    close(w,0,1e-15,'the crest spacing along the boundary matches (derive: 1.8e-16)');
  }
  /* field continuity: 1 + r_s = t_s and the H condition */
  {
    let we=0,wh=0;
    for(const [n1,n2] of [[NA,NW],[NW,NA],[NA,NG],[NG,NA],[NA,ND],[ND,NA],[NW,NG],[NG,NW]])
      for(let i=0;i<=85;i++){
        const th=i*DEG, f=fresnel(n1,n2,th);
        if(f.tir) continue;
        we=Math.max(we,Math.abs(1+f.rs-f.ts));
        wh=Math.max(wh,Math.abs(n1*Math.cos(th)*(1-f.rs)-n2*Math.cos(f.th2)*f.ts));
      }
    close(we,0,1e-14,'1 + r_s = t_s over eight pairs x 86 angles (derive: 2.2e-16)');
    close(wh,0,1e-14,'and the magnetic-field condition too (derive: 4.4e-16)');
  }
  /* the DRAWN field is continuous across the boundary: the same check, on the
     function the wave view actually paints with (a number computed inside a
     draw call cannot be tested -- so waveAt is a model function) */
  {
    let w=0, wt=0;
    for(const [n1,n2] of [[NA,NW],[NG,NA],[NA,ND],[NW,NG]])
      for(const tdeg of [10,35,55,75])
        for(const ph of [0,1.1,2.7,4.9]){
          /* 650 nm is where k0 stops depending on which way the ratio is
             written, so the wavelength is walked across the band here too */
          const Wv=waveState(n1,n2,tdeg*DEG,[380,450,650,700][(tdeg/10|0)%4]);
          for(const x of [-7,-2.3,0,1.8,6.4]){
            w=Math.max(w,Math.abs(waveAt(Wv,x,0,ph)-waveAt(Wv,x,-1e-12,ph)));
            wt=Math.max(wt,Math.abs(waveAt(Wv,x,1e-12,ph)-waveAt(Wv,x,0,ph)));
          }
        }
    close(w,0,1e-9,'the painted field is continuous across y = 0 (16 geometries x 5 places)');
    close(wt,0,1e-9,'  and from above as well');
  }
  /* past the critical angle the transmitted field decays and carries no power */
  {
    const Wv=waveState(NG,NA,60*DEG,650);
    ok(Wv.f.tir,'glass->air at 60 deg is past the critical angle');
    const a0=Math.abs(waveAt(Wv,0,0,0)), a1=Math.abs(waveAt(Wv,0,-3,0));
    ok(a1<a0,'the evanescent field is smaller three wavelengths down');
    /* (the rate itself is pinned absolutely above, against derive.py: a
       comparison of exp(-kappa|y|) with a ratio of waveAt to itself is built
       from the same kappa on both sides and cannot see a wrong one) */
    close(fresnel(NG,NA,60*DEG).Rs,1,0,'while |r| = 1, so no power crosses');
  }
  /* THE WORLD'S WAVENUMBER.  One world unit is one RED wavelength, so a wave
     of vacuum wavelength lam has k0 = 2 pi (650/lam) per unit.  At 650 nm --
     the default, and the only wavelength every wave assertion used to be taken
     at -- that is 2 pi whichever way round the ratio is written, so inverting
     it changed nothing the suite could see.  Same shape as the w = -1
     dark-energy exponent: a parameter has a value at which it stops mattering,
     and a suite that lives there has tested nothing about it. */
  {
    const K0={380:10.7475538149125,400:10.2101761241668,500:8.16814089933346,
              650:6.28318530717959,700:5.83438635666676};
    for(const lam in K0)
      close(waveState(1,1.5,0.5,+lam).k0,K0[lam],1e-12,'k0 per world unit at '+lam+' nm (derive)');
    ok(waveState(1,1.5,0.5,400).k0>waveState(1,1.5,0.5,700).k0,
       'a shorter wavelength has a LARGER wavenumber');
    rel(waveState(1,1.5,0.5,400).k0/waveState(1,1.5,0.5,800).k0,2,1e-14,
        'and halving the wavelength doubles it');
    close(waveState(1,1.5,0.5,PHET.lamRed).k0,TAU,1e-14,
          'at the reference wavelength one world unit IS one wavelength, so k0 = 2 pi');
  }
  /* measured off the drawn field, not re-derived: the crest spacing along the
     boundary and the standing-fringe period in y, both in world units */
  {
    /* two successive upward zero crossings of E(x) at y = 0, bisected */
    const crestSpacing=(W,ph)=>{
      const f=x=>waveAt(W,x,0,ph);
      const up=[]; let prev=f(0);
      for(let i=1;i<=400000&&up.length<3;i++){
        const x=i*1e-4, v=f(x);
        if(prev<0&&v>=0){ let lo=x-1e-4,hi=x;
          for(let b=0;b<80;b++){ const m=0.5*(lo+hi); if(f(m)<0) lo=m; else hi=m; }
          up.push(0.5*(lo+hi)); }
        prev=v;
      }
      return up.length>=2?up[1]-up[0]:NaN;
    };
    const REF=[['air 45 deg, 650 nm',NA,NW,45,650,1.41379931917258],
               ['air 45 deg, 400 nm',NA,NW,45,400,0.870024290533342],
               ['glass 70 deg, 500 nm',NG,NA,70,500,0.543305579385684]];
    for(const [nm,r1,r2,tdeg,lam,want] of REF){
      const W=waveState(indexOf(r1,lam),indexOf(r2,lam),tdeg*DEG,lam);
      rel(crestSpacing(W,0.7),want,1e-9,'measured crest spacing along the boundary, '+nm+' (derive)');
    }
    /* the fringe period of the PAINTED intensity: successive maxima of
       meanIntensity in y, each refined by a parabola through its three
       nearest samples (never quote a sharp extremum off a sample grid) */
    const fringePeriod=W=>{
      const h=2e-4, ys=[];
      let a=meanIntensity(W,0), b=meanIntensity(W,h);
      for(let i=2;i<=60000&&ys.length<3;i++){
        const y=i*h, c=meanIntensity(W,y);
        if(b>a&&b>=c){ const d=(a-c)/(2*(a-2*b+c)); ys.push(y-h+d*h); }
        a=b; b=c;
      }
      return ys.length>=2?ys[1]-ys[0]:NaN;
    };
    const FR=[['air->water 45 deg, 650 nm',NA,NW,45,650,0.706899659586289],
              ['air->water 45 deg, 400 nm',NA,NW,45,400,0.435012145266671],
              ['glass->air 70 deg, 500 nm',NG,NA,70,500,0.746359905612939]];
    for(const [nm,r1,r2,tdeg,lam,want] of FR){
      const W=waveState(indexOf(r1,lam),indexOf(r2,lam),tdeg*DEG,lam);
      rel(fringePeriod(W),want,1e-6,'measured standing-fringe period, '+nm+' (derive)');
    }
  }
  /* THE EVANESCENT DECAY CONSTANT, pinned absolutely and then MEASURED off
     the drawn field.  The old check compared exp(-kappa|y|) against a ratio of
     waveAt to itself -- both sides built from the same kap -- so it could not
     see a wrong one (nor a wrong k0). */
  {
    const KAP={'glass->air 650':[NG,NA,650,[NaN,0.828802699169712,1.08699959178242],
                                 [NaN,124.819469233592,95.1708848759525]],
               'glass->air 450':[NG,NA,450,[NaN,0.84297079271082,1.10099937472429],
                                 [NaN,84.9610983092767,65.049741203793]],
               'water->air 650':[NW,NA,650,[NaN,0.576264404723214,0.850131257382544],
                                 [NaN,179.519526387233,121.687930082991]],
               'diamond->air 650':[ND,NA,650,[1.38751375277905,1.84067505664389,2.16206585469553],
                                   [74.558333423745,56.2025940626119,47.8480860261772]]};
    const TH=[45,60,80];
    for(const nm in KAP){
      const [r1,r2,lam,kaps,lens]=KAP[nm];
      const n1=indexOf(r1,lam), n2=indexOf(r2,lam);
      for(let i=0;i<3;i++){
        if(!isFinite(kaps[i])) continue;
        const W=waveState(n1,n2,TH[i]*DEG,lam);
        ok(W.f.tir,nm+' at '+TH[i]+' deg is past the critical angle');
        rel(W.f.kap,kaps[i],1e-11,nm+' at '+TH[i]+' deg: kappa/k0 (derive)');
        rel(lam/(TAU*W.f.kap),lens[i],1e-11,'  and 1/kappa = '+fmt(lens[i],1)+' nm (derive)');
        /* measured: under total internal reflection the transmitted phase does
           not depend on y at all, so the ratio of the field at two depths is
           exactly exp(kappa dy) and inverting it gives kappa back */
        const e0=waveAt(W,0.31,0,0.4), e3=waveAt(W,0.31,-2.5,0.4);
        rel(Math.log(e0/e3)/2.5,W.k0*kaps[i],1e-9,
            '  and the drawn field decays at exactly that rate ('+nm+', '+TH[i]+' deg)');
      }
    }
    /* the other half of the contract: BELOW the critical angle there is no
       decay at all.  A ratio of the field to itself cannot see this either --
       the painted intensity has to be flat in depth. */
    for(const [r1,r2,tdeg,lam] of [[NA,NW,45,650],[NA,NG,20,450],[NW,NG,60,700]]){
      const W=waveState(indexOf(r1,lam),indexOf(r2,lam),tdeg*DEG,lam);
      ok(!W.f.tir&&W.f.kap===0,'a propagating transmitted wave has kappa exactly zero');
      eq(meanIntensity(W,-0.3),meanIntensity(W,-7.9),
         'and its painted intensity is the same at every depth');
    }
    /* and the readout PRINTS the decay length, so a wrong kappa would be read
       off the panel (fmt renders a non-finite value as an em dash, so a NaN
       scan could never see it) */
    withState({view:'wave',topSub:'glass',botSub:'air',angDeg:60,lamNm:650},()=>{
      const html=readoutHTML(buildModel(ST),ST);
      ok(html.indexOf('124.8')>=0,'the wave readout prints the 124.8 nm decay length');
    });
  }
  close(PHET.maxWaveAngle*RAD,172.998876661801,1e-9,'PhET’s MAX_ANGLE_IN_WAVE_MODE in degrees (derive)');
  /* the painted background is the TIME-AVERAGED intensity: it must agree with
     a direct average of the field the crest lines are drawn from, and it must
     be continuous across the boundary (|1 + r|^2 = |t|^2) */
  {
    let wm=0, wc=0;
    for(const [n1,n2] of [[NA,NW],[NG,NA],[NA,ND],[NW,NG]])
      for(const tdeg of [10,35,55,75]){
        const Wv=waveState(n1,n2,tdeg*DEG,[400,520,650,690][(tdeg/10|0)%4]);
        for(const y of [-2.7,-0.6,0,0.4,1.9,3.3]){
          let sum=0; const NPH=720;
          for(let i=0;i<NPH;i++) { const e=waveAt(Wv,0.37,y,TAU*i/NPH); sum+=e*e; }
          wm=Math.max(wm,Math.abs(sum/NPH-meanIntensity(Wv,y)));
        }
        /* continuity, stated exactly rather than by a finite step: from above
           the value is |1 + r|^2/2 and from below |t|^2/2, and 1 + r = t */
        wc=Math.max(wc,Math.abs(meanIntensity(Wv,0)
                    -0.5*(Wv.f.tRe*Wv.f.tRe+Wv.f.tIm*Wv.f.tIm)));
      }
    close(wm,0,1e-12,'the painted intensity is the average of the drawn field over a cycle');
    close(wc,0,1e-15,'and it is continuous across the boundary, exactly');
    /* the standing pattern is a standing pattern: its fringe spacing is
       lambda_1/(2 cos th_1), which is a statement the picture makes */
    const Wv=waveState(NW,NA,70*DEG,650);
    const ky=Wv.k0*Wv.n1*Math.cos(70*DEG);
    close(meanIntensity(Wv,0),meanIntensity(Wv,PI/ky),1e-12,'the fringes repeat every pi/k_y in y');
    ok(Math.abs(meanIntensity(Wv,0)-meanIntensity(Wv,0.5*PI/ky))>0.5,
       'and they are real fringes, not a flat wash');
  }

  /* ------------------------------------------------------ 5. the prism */
  {
    const t=PHET.prismT, tri=prismShape('triangle');
    close(tri.pts[0][0],-5,1e-15,'PhET’s triangle, x of the left vertex');
    close(tri.pts[0][1],-2.88675134594813,1e-13,'PhET’s triangle, y of the base (-t/2sqrt3)');
    close(tri.pts[2][1],5.77350269189626,1e-13,'PhET’s triangle, y of the apex (t/sqrt3)');
    const sq=prismShape('square');
    close(sq.pts[2][0]-sq.pts[0][0],t,1e-15,'PhET’s square is t across');
    const tz=prismShape('trapezoid');
    close(tz.pts[2][1],4.33012701892219,1e-13,'PhET’s trapezoid, y of the short side (t sqrt3/4)');
    close(prismShape('circle').r,5,1e-15,'PhET’s circle has radius t/2');
    /* the polygons must be wound so that polyHit's normal points OUT */
    for(const id of ['triangle','trapezoid','square']){
      const sh=prismShape(id), c=[0.0,0.0];
      const h=polyHit(c,[1,0],sh.pts);
      ok(h&&h.n[0]>0,'the outward normal of the '+id+' really points outward');
    }
    for(const id of ['triangle','trapezoid','square','circle','semicircle']){
      const sh=prismShape(id);
      const inPt=(id==='semicircle')?[-1,0]:[0,0];
      ok(shapeInside(sh,inPt),'the centre is inside the '+id);
      ok(!shapeInside(sh,[40,40])&&!shapeInside(sh,[-40,0]),'and a far point is outside the '+id);
    }
  }
  /* the tracer against the two-surface closed form, and against minimum
     deviation -- the two routes share no arithmetic, so this is the real test */
  {
    const nEnv=indexOf(NA,650), nGl=indexOf(NG,650), nWa=indexOf(NW,650);
    close(prismMinDeviation(nEnv,nGl,60*DEG)*RAD,37.1427032541713,1e-12,
          'minimum deviation of a 60 deg glass prism (derive)');
    close(prismMinDeviation(nEnv,nWa,60*DEG)*RAD,23.5650040302185,1e-12,
          'minimum deviation of a 60 deg water prism (derive)');
    ok(!isFinite(prismMinDeviation(nEnv,indexOf(ND,650),60*DEG)),
       'a 60 deg diamond prism has no symmetric passage at all');
    close(2*criticalAngle(indexOf(ND,650),nEnv)*RAD,48.8516786222287,1e-12,
          'because 2 theta_c is only 48.85 deg (derive)');
    const REF=[[35,40.9395154251525],[45,37.3408247392829],[55,37.703048679383],[65,40.5546683964733]];
    let w=0;
    for(const [t,d] of REF){
      const got=traceTriangleDeviation(nEnv,nGl,t*DEG);
      w=Math.max(w,Math.abs(got*RAD-d),Math.abs(prismDeviation(nEnv,nGl,60*DEG,t*DEG)*RAD-d));
    }
    close(w,0,1e-11,'the TRACED deviation and the closed form, at four entry angles (derive)');
    const Dm=prismMinDeviation(nEnv,nGl,60*DEG);
    close(traceTriangleDeviation(nEnv,nGl,(60*DEG+Dm)/2)*RAD,Dm*RAD,1e-11,
          'and the traced ray reproduces D_min at the symmetric angle');
    /* off that angle the deviation is LARGER -- it really is a minimum */
    ok(prismDeviation(nEnv,nGl,60*DEG,((60*DEG+Dm)/2)*0.9)>Dm
       &&prismDeviation(nEnv,nGl,60*DEG,((60*DEG+Dm)/2)*1.1)>Dm,
       'and the deviation is larger on both sides of it');
    /* dispersion through the triangle */
    close(prismDeviation(indexOf(NA,400),indexOf(NG,400),60*DEG,45*DEG)*RAD,38.8236148138137,1e-11,
          'deviation of 400 nm through a glass triangle at 45 deg (derive)');
    close(prismDeviation(indexOf(NA,700),indexOf(NG,700),60*DEG,45*DEG)*RAD,37.2107780635166,1e-11,
          'deviation of 700 nm (derive)');
  }
  /* a slab displaces but does not deviate */
  {
    const nEnv=indexOf(NA,650), nGl=indexOf(NG,650);
    const d=[Math.cos(-45*DEG),Math.sin(-45*DEG)];
    const tr=traceRay(prismShape('square'),[-12,10],d,nEnv,nGl,{reflections:false});
    eq(tr.segs.length,3,'a 45 deg ray through the square draws three segments (derive)');
    const ang=Math.atan2(d[0]*tr.exitDir[1]-d[1]*tr.exitDir[0],d[0]*tr.exitDir[0]+d[1]*tr.exitDir[1]);
    close(ang*RAD,0,1e-12,'and leaves exactly parallel to the way it came in (derive)');
    close(slabOffset(nEnv,nGl,45*DEG,10),3.28999905677164,1e-12,'the slab offset at 45 deg (derive)');
    close(slabOffset(nEnv,nGl,20*DEG,10),1.21892785716214,1e-12,'the slab offset at 20 deg (derive)');
    close(slabOffset(nEnv,nGl,70*DEG,10),6.64671385047396,1e-12,'the slab offset at 70 deg (derive)');
  }
  /* the circle: a ray through the centre is undeviated */
  {
    const tr=traceRay(prismShape('circle'),[-9,0],[1,0],indexOf(NA,650),indexOf(NG,650),{reflections:false});
    close(tr.exitDir[0],1,1e-14,'a ray through the centre of the circle leaves undeviated, x (derive)');
    close(tr.exitDir[1],0,1e-14,'  and y (derive)');
    eq(tr.segs.length,3,'  in three segments (derive)');
  }
  /* the semicircle: aimed at the centre, the curved face does nothing and the
     flat face refracts by Snell alone */
  {
    const nEnv=indexOf(NA,650), nGl=indexOf(NG,650);
    const d=[Math.cos(-20*DEG),Math.sin(-20*DEG)];
    const tr=traceRay(prismShape('semicircle'),[-12*d[0],-12*d[1]],d,nEnv,nGl,{reflections:false});
    eq(tr.segs.length,3,'the semicircle aimed at its centre draws three segments (derive)');
    close(Math.atan2(tr.exitDir[1],tr.exitDir[0])*RAD,-30.8558522996784,1e-11,
          'and leaves at the angle Snell gives at the flat face (derive)');
    close(Math.asin(nGl*Math.sin(20*DEG)/nEnv)*RAD,30.8558522996784,1e-12,
          '  which is arcsin(n_glass sin 20 / n_air), independently (derive)');
  }
  /* the traced-ray reference values, with and without the partial reflections */
  {
    const nEnv=indexOf(NA,650);
    const CASES=[['triangle glass 45','triangle',NG,[-12,4],[0.9,-0.2],
                  11,196.482933325611,3.99980921022232,[-0.300226242766432,-0.95386802187428],4,58.8044918893032],
                 ['square glass 30','square',NG,[-12,6],[0.95,-0.35],
                  8,198.290426414828,2.99987246857834,[0.93834311681711,-0.345705358827356],3,57.7367806336872],
                 ['circle water','circle',NW,[-12,2.2],[1,0],
                  6,146.388376242123,2.99913517736292,[0.971761802029967,-0.235963980546758],3,56.9491936889971],
                 ['trapezoid glass','trapezoid',NG,[-14,1.3],[1,-0.12],
                  9,196.360268354132,3.05139998932305,[0.905741390932586,-0.423830783157033],3,58.321627754792],
                 ['semicircle glass','semicircle',NG,[-14,1.3],[1,-0.12],
                  8,184.100090710994,2.9998809744047,[0.98999393976676,-0.141109883513131],3,54.0868669952337]];
    for(const [nm,id,nref,p0,d0,ns,tot,pw,ed,ns2,tot2] of CASES){
      const L=Math.hypot(d0[0],d0[1]), du=[d0[0]/L,d0[1]/L];
      const tr=traceRay(prismShape(id),p0,du,nEnv,indexOf(nref,650),{reflections:true,reach:40});
      eq(tr.segs.length,ns,nm+': segment count (derive)');
      let s=0,p=0;
      for(const g of tr.segs){ s+=Math.hypot(g[2]-g[0],g[3]-g[1]); p+=g[4]; }
      rel(s,tot,1e-11,nm+': total drawn length (derive)');
      rel(p,pw,1e-11,nm+': sum of the branch powers (derive)');
      close(tr.exitDir[0],ed[0],1e-11,nm+': exit direction x (derive)');
      close(tr.exitDir[1],ed[1],1e-11,nm+': exit direction y (derive)');
      const tr2=traceRay(prismShape(id),p0,du,nEnv,indexOf(nref,650),{reflections:false,reach:40});
      eq(tr2.segs.length,ns2,nm+': segment count with the reflections off (derive)');
      let s2=0;
      for(const g of tr2.segs) s2+=Math.hypot(g[2]-g[0],g[3]-g[1]);
      rel(s2,tot2,1e-11,nm+': total length with the reflections off (derive)');
    }
  }
  /* vector Snell is the same law as the scalar one */
  {
    let w=0;
    for(const tdeg of [5,20,40,60,80]) for(const [n1,n2] of [[NA,NG],[NG,NA],[NA,ND]]){
      const nrm=[0,1], th=tdeg*DEG;
      const d=[Math.sin(th),-Math.cos(th)];
      const td=vecRefract(d,nrm,n1,n2);
      const sc=refractAngle(n1,n2,th);
      if(!isFinite(sc)){ ok(td===null,'vector Snell also refuses at '+tdeg+' deg, '+n1+'->'+n2); continue; }
      w=Math.max(w,Math.abs(Math.atan2(td[0],-td[1])-sc));
    }
    close(w,0,1e-14,'vector Snell reproduces the scalar law over 15 cases');
    const r=vecReflect([0.6,-0.8],[0,1]);
    close(r[0],0.6,1e-15,'reflection keeps the tangential component');
    close(r[1],0.8,1e-15,'and flips the normal one');
  }

  /* ----------------------------------------------------- 6. the rainbow */
  {
    close(dropIndex(650),1.3326095454032,1e-12,'the relative index of water at 650 nm (derive)');
    const n=dropIndex(650);
    const REF=[[1,59.4331661544485,137.865078785733,42.1349212142667],
               [2,71.8553075547132,230.788357646205,50.7883576462051],
               [3,76.8543419589106,318.11896230126,138.11896230126]];
    for(const [k,th,D,ang] of REF){
      close(rainTheta(n,k)*RAD,th,1e-11,'k = '+k+': the stationary impact angle (derive)');
      close(rainDev(n,k,rainTheta(n,k))*RAD,D,1e-11,'k = '+k+': the deviation there (derive)');
      close(bowAngle(n,k)*RAD,ang,1e-11,'k = '+k+': the bow’s angular radius (derive)');
      /* the derivative really vanishes there -- the closed form is the
         stationary point, not merely a number near it */
      const h=1e-6, dD=(rainDev(n,k,rainTheta(n,k)+h)-rainDev(n,k,rainTheta(n,k)-h))/(2*h);
      close(dD,0,1e-9,'k = '+k+': dD/dtheta is zero at the closed-form angle');
      /* and it is a MINIMUM: D is larger on both sides */
      const t0=rainTheta(n,k);
      ok(rainDev(n,k,t0*0.9)>rainDev(n,k,t0)&&rainDev(n,k,Math.min(t0*1.1,PI/2-1e-6))>rainDev(n,k,t0),
         'k = '+k+': and it is a minimum, so the rays pile up there');
    }
    const P=[40.6227557074149,41.4904989824113,41.9682064527453,42.1349212142667,42.2721828060137];
    const S=[53.5196234819352,51.9508324808066,51.088888179892,50.7883576462051,50.5410283843716];
    const LS=[400,500,600,650,700];
    let w=0;
    for(let i=0;i<LS.length;i++){
      const m=dropIndex(LS[i]);
      w=Math.max(w,Math.abs(bowAngle(m,1)*RAD-P[i]),Math.abs(bowAngle(m,2)*RAD-S[i]));
    }
    close(w,0,1e-11,'the bow angles of five wavelengths, both orders (derive)');
    ok(P[4]>P[0],'the primary bow puts red OUTSIDE');
    ok(S[4]<S[0],'and the secondary puts it INSIDE — the order really is reversed');
    close(bowAngle(dropIndex(650),2)*RAD-bowAngle(dropIndex(650),1)*RAD,8.65343643193839,1e-11,
          'Alexander’s dark band (derive)');
    /* the exact identities at the stationary ray */
    for(const k of [1,2,3]){
      const m=dropIndex(650), nW=indexOf(NW,650), nA=indexOf(NA,650);
      const th=rainTheta(m,k), thr=Math.asin(nA*Math.sin(th)/nW);
      const f=fresnel(nW,nA,thr);
      close(f.Rs,bowRsExact(k),1e-13,'k = '+k+': R_s at the bounce is exactly (k/(k+2))^2 (derive)');
      close(f.Rp,bowRpExact(k,m),1e-13,'k = '+k+': and R_p matches its closed form (derive)');
    }
    close(bowRsExact(1),1/9,1e-15,'the primary bow’s internal R_s is 1/9 for ANY index');
    close(bowRsExact(2),0.25,1e-15,'and the secondary’s is 1/4');
    /* the s identity is index-independent -- assert that it really is */
    {
      let w2=0;
      for(const nn of [1.2,1.33,1.5,1.8,1.99]){
        const th=rainTheta(nn,1), thr=Math.asin(Math.sin(th)/nn);
        w2=Math.max(w2,Math.abs(fresnel(nn,1,thr).Rs-1/9));
      }
      close(w2,0,1e-14,'  and it holds at five quite different indices');
      /* a drop of index above 2 has NO primary bow: cos^2 theta would exceed 1 */
      ok(!isFinite(rainTheta(2.05,1)),'a drop of index 2.05 has no primary rainbow at all');
      ok(isFinite(rainTheta(2.05,2)),'but it still has a secondary one');
      ok(!isFinite(rainTheta(3.1,2))&&isFinite(rainTheta(3.1,3)),
         'and at index 3.1 the first bow that exists is the third order');
    }
    const nW=indexOf(NW,650), nA=indexOf(NA,650);
    close(bowThroughput(nA,nW,1,rainTheta(dropIndex(650),1),'unpol'),0.0509353184764683,1e-13,
          'the primary bow\u2019s Fresnel throughput (derive)');
    {
      const REF={1:[0.0509353184764683,0.0877914951989026,0.00349936267887175],
                 2:[0.0176713399959417,0.0351562499999999,0.0037680022854167],
                 3:[0.00913153260549255,0.0191102975999998,0.00236526870685464]};
      for(const k of [1,2,3]){
        const th=rainTheta(dropIndex(650),k);
        const got=['unpol','s','p'].map(p=>bowThroughput(nA,nW,k,th,p));
        for(let i=0;i<3;i++) rel(got[i],REF[k][i],1e-11,'k = '+k+' throughput ('+['unpol','s','p'][i]+') (derive)');
        /* the s-polarised throughput of the k-th bow is exact and does not
           depend on the index at all: the entry interface is the same
           interface at the conjugate angle, so it reflects (k/(k+2))^2 too */
        rel(got[1],bowThroughputSExact(k),1e-12,'k = '+k+': and it matches its closed form');
      }
      close(bowThroughputSExact(1),64/729,1e-15,'the primary bow passes exactly 64/729 of s-polarised light');
      close(bowThroughputSExact(2),9/256,1e-15,'and the secondary exactly 9/256');
      {
        let w=0;
        for(const nn of [1.15,1.33,1.5,1.9]){
          const th=rainTheta(nn,1), thr=Math.asin(Math.sin(th)/nn);
          const f1=fresnel(1,nn,th), f2=fresnel(nn,1,thr);
          w=Math.max(w,Math.abs(f1.Ts*f2.Rs*f2.Ts-bowThroughputSExact(1)));
        }
        close(w,0,1e-13,'  and it holds at four quite different indices');
      }
      rel(bowThroughput(nA,nW,1,rainTheta(dropIndex(650),1),'unpol')
          /bowThroughput(nA,nW,2,rainTheta(dropIndex(650),2),'unpol'),
          0.0509353184764683/0.0176713399959417,1e-11,
          'the primary bow is 2.88 times brighter than the secondary (derive)');
    }
    close(Math.asin(nA*Math.sin(rainTheta(dropIndex(650),1))/nW)*RAD,40.2503133807909,1e-11,
          'the internal incidence at the bow (derive)');
    ok(Math.asin(nA*Math.sin(rainTheta(dropIndex(650),1))/nW)<criticalAngle(nW,nA),
       'which is BELOW the critical angle: the bow is a partial reflection');
    close(brewster(nW,nA)*RAD,36.8848320317008,1e-12,'Brewster water->air (derive)');
    /* the EMERGENT ray the view draws is refracted at the exit face, not
       turned through D by hand: assert the two agree, which is the only thing
       that ties the picture to the closed form */
    {
      let wd=0;
      for(const k of [1,2,3]) for(const tdeg of [15,35,59.4331661544485,78]){
        const P2=dropPath(n,k,tdeg*DEG);
        if(P2.tir) continue;
        /* the angle from the incoming direction (1,0) to the emergent one */
        let a=Math.atan2(P2.out[1],P2.out[0]);
        /* D is the total turn; the ray entered above the axis and turns
           clockwise, so the emergent direction is at -D (mod 2 pi) */
        let want=-rainDev(n,k,tdeg*DEG);
        let d=Math.atan2(Math.sin(a-want),Math.cos(a-want));
        wd=Math.max(wd,Math.abs(d));
      }
      close(wd,0,1e-12,'the drawn emergent ray leaves at exactly the deviation rainDev gives');
    }
    /* dropPath draws what rainDev computes */
    {
      let w3=0;
      for(const k of [1,2]) for(const tdeg of [20,40,59.4331661544485,75]){
        const P2=dropPath(n,k,tdeg*DEG);
        /* every point is on the unit circle */
        for(const p of P2.pts) w3=Math.max(w3,Math.abs(Math.hypot(p[0],p[1])-1));
        /* the entry point sits at height sin(theta) */
        w3=Math.max(w3,Math.abs(P2.pts[0][1]-Math.sin(tdeg*DEG)));
        /* and the chord count is k+1 */
        ok(P2.pts.length===k+2,'k = '+k+' at '+tdeg+' deg: the drawn path has '+(k+1)+' chords');
      }
      close(w3,0,1e-14,'every drawn drop path stays on the drop and enters at the right height');
    }
  }

  /* ------------------------------------------------------- 7. colour */
  ok(cmfAt(350)===null&&cmfAt(900)===null,'the colour-matching table refuses arguments outside it');
  {
    const c=cmfAt(555);
    close(c[1],1,1e-9,'ybar peaks at 1 at 555 nm (the CIE table’s own normalisation)');
    ok(cmfAt(500)[1]<1&&cmfAt(600)[1]<1,'and is smaller either side');
    const red=monoLinear(650), blue=monoLinear(450), green=monoLinear(530);
    ok(red[0]>red[1]&&red[0]>red[2],'650 nm is reddest in the red channel');
    ok(blue[2]>blue[0]&&blue[2]>blue[1],'450 nm is bluest in the blue channel');
    ok(green[1]>green[0]&&green[1]>green[2],'530 nm is greenest in the green channel');
    /* Spectral colours lie OUTSIDE the sRGB gamut, so the raw linear triple of
       a single wavelength has a negative channel; monoLinear desaturates by
       lifting the whole triple until the smallest channel is exactly zero.
       Without that lift the negative channel is merely clamped away and every
       spectral colour comes out more saturated than the gamut can show --
       which no assertion on hue, format or brightness can see. */
    let sawNeg=false, worstMin=1;
    for(const nm of [420,470,500,520,560,600,640]){
      const c=cmfAt(nm), raw=xyzToLin(c[0],c[1],c[2]);
      if(Math.min(raw[0],raw[1],raw[2])<0) sawNeg=true;
      const v=monoLinear(nm);
      worstMin=Math.min(worstMin,Math.min(v[0],v[1],v[2]));
      close(Math.max(v[0],v[1],v[2]),1,1e-12,nm+' nm is normalised to its brightest channel');
    }
    ok(sawNeg,'a monochromatic colour really is outside the sRGB gamut');
    close(worstMin,0,1e-15,'and monoLinear lifts it until its smallest channel is exactly zero');
    ok(/^rgb\(\d+,\d+,\d+\)$/.test(cssOfLinear(red,1)),'the colour string is well formed');
    /* well formed is not visible (Known-bad): assert brightness too */
    const bytes=cssOfLinear(red,1).match(/\d+/g).map(Number);
    ok(Math.max(bytes[0],bytes[1],bytes[2])>200,'and it is actually bright');
    const dim=cssOfLinear(red,0.001).match(/\d+/g).map(Number);
    ok(Math.max(dim[0],dim[1],dim[2])<40,'while a faint ray really is faint');
  }
  /* the colours themselves, against derive.py, which parses the very table
     p2_cie.js carries and evaluates it independently in Python */
  {
    const LIN={400:[0.268800784813747,0,1],450:[0.159041536158688,0,1],
               500:[0,1,0.682147531295078],550:[0.0250050387243246,1,0],
               600:[1,0.0878609156416056,0],650:[1,0,0.0820276689661251],
               690:[1,0,0.0915565162437447],700:[1,0,0.0918864450987531]};
    let w=0;
    for(const nm in LIN){ const v=monoLinear(+nm);
      for(let i=0;i<3;i++) w=Math.max(w,Math.abs(v[i]-LIN[nm][i])); }
    close(w,0,1e-12,'monoLinear at eight wavelengths (derive)');
    const CSS={400:'rgb(142,0,255)',450:'rgb(111,0,255)',500:'rgb(0,255,215)',
               550:'rgb(44,255,0)',600:'rgb(255,84,0)',650:'rgb(255,0,81)',
               690:'rgb(255,0,85)',700:'rgb(255,0,85)'};
    let bad=null;
    for(const nm in CSS){ const c=cssOfLinear(monoLinear(+nm),1);
      if(c!==CSS[nm]) bad=bad||(nm+' nm: '+c+' vs '+CSS[nm]); }
    ok(!bad,'the sRGB bytes of eight wavelengths (derive) ('+(bad||'ok')+')');
    eq(cssOfLinear(monoLinear(650),0.25),'rgb(137,0,39)','and a quarter-power red (derive)');
    eq(cssOfLinear(monoLinear(550),0.25),'rgb(18,137,0)','and a quarter-power green (derive)');
    const LEV={400:0.0397994974842648,450:0.389871773792359,500:1,555:1,600:1,
               650:0.654217089351845,700:0.128093715692847};
    let wl=0;
    for(const nm in LEV) wl=Math.max(wl,Math.abs(monoLevel(+nm)-LEV[nm]));
    close(wl,0,1e-12,'monoLevel at seven wavelengths (derive)');
  }
  eq(WHITE_WL.length,30,'PhET\u2019s white light is 30 wavelengths');
  eq(WHITE_WL[0],400,'starting at 400 nm');
  eq(WHITE_WL[WHITE_WL.length-1],690,'and ending at 690 nm (lodash range excludes 700)');

  /* -------------------------------------- 8. the model and the panels */
  {
    const M=buildModel(ST);
    close(M.b.th1*RAD,45,1e-12,'the default state is PhET’s 45 deg of incidence (3 pi/4 laser angle)');
    eq(ST.topSub,'air','above the boundary is air, as PhET’s Intro screen opens');
    eq(ST.botSub,'water','and below it is water');
    close(M.b.n1,indexOf(NA,650),0,'  n1 is air at the laser wavelength');
    close(M.b.n2,indexOf(NW,650),0,'  n2 is water');
    close(M.b.th2*RAD,32.0472287061937,1e-11,'  so the refracted ray leaves at 32.05 deg (derive)');
    close(M.b.R,0.0529000573165104,1e-13,'  and 5.29% comes back, s-polarised (derive)');
    close(M.b.R+M.b.T,1,1e-15,'  with R + T = 1');
  }
  /* the readout says a number, not merely "no NaN" (Known-bad: fmt renders a
     non-finite value as an em dash, so a NaN scan can never see one) */
  {
    const M=buildModel(ST), html=readoutHTML(M,ST);
    ok(html.indexOf('32.05')>=0,'the readout prints the refracted angle 32.05 deg');
    ok(html.indexOf('5.29%')>=0,'and the 5.29% reflected fraction');
    ok(html.indexOf('—')<0||html.indexOf('none')>=0,'and carries no unexplained em dash');
  }
  withState({view:'bow'},()=>{
    const html=readoutHTML(buildModel(ST),ST);
    ok(html.indexOf('42.13')>=0,'the rainbow readout prints the 42.13 deg bow radius');
    ok(html.indexOf('0.11111111')>=0,'and the exact 1/9 reflectance at the bounce');
  });
  withState({view:'spec'},()=>{
    const html=readoutHTML(buildModel(ST),ST);
    ok(html.indexOf('64.1')>=0,'the spectrum readout prints BK7’s Abbe number');
    ok(html.indexOf('2.75')>=0,'and diamond’s blend weight of 2.76');
  });
  /* every view x every preset builds a clean panel */
  {
    const VIEWS=TABS.map(t=>t[0]);
    let bad=null;
    for(const v of VIEWS)
      for(const top of ['air','water','glass','diamond','mysteryA','mysteryB','custom'])
        for(const bot of ['air','water','glass','diamond','custom'])
          for(const a of [0,45,89.9]){
            withState({view:v,topSub:top,botSub:bot,angDeg:a},()=>{
              const M=buildModel(ST);
              const s=readoutHTML(M,ST)+eqbarHTML(M,ST)+tagHTML(M,ST);
              if(/NaN|undefined|Infinity/.test(s)) bad=bad||(v+'/'+top+'/'+bot+'/'+a+': '+s.slice(0,60));
            });
          }
    ok(!bad,'no view x medium x angle puts NaN in a panel ('+(bad||'ok')+')');
  }
  /* no slider corner produces a non-finite model number */
  {
    let bad=null;
    for(const lam of [380,500,650,700])
      for(const n1 of [PHET.nSliderLo,1.4,PHET.nCustom0])
        for(const n2 of [PHET.nSliderLo,1.4,PHET.nCustom0])
          for(const a of [0,30,60,89.9]){
            withState({topSub:'custom',botSub:'custom',topN:n1,botN:n2,lamNm:lam,angDeg:a},()=>{
              const B=boundaryModel(ST);
              const vals=[B.n1,B.n2,B.R,B.T,B.lam1,B.lam2,B.freq,B.f.Rs,B.f.Rp,B.f.Ts,B.f.Tp];
              for(const v of vals) if(!isFinite(v)) bad=bad||(lam+'/'+n1+'/'+n2+'/'+a);
              if(Math.abs(B.R+B.T-1)>1e-12) bad=bad||('R+T at '+lam+'/'+n1+'/'+n2+'/'+a);
            });
          }
    ok(!bad,'no custom-index corner gives a non-finite model value ('+(bad||'ok')+')');
  }
  /* every prism shape x medium traces and terminates */
  {
    let bad=null;
    for(const id of PRISMS.map(p=>p.id))
      for(const sub of ['air','water','glass','diamond','mysteryB'])
        for(const rot of [0,37,-90,180])
          for(const refl of [false,true]){
            withState({view:'prism',prismId:id,prismSub:sub,prismRot:rot,showReflections:refl},()=>{
              const P=buildModel(ST).prism;
              for(const bnd of P.bundles){
                if(bnd.tr.steps>PHET.maxSteps) bad=bad||(id+'/'+sub+'/'+rot+': ran past PhET’s step limit');
                for(const s of bnd.tr.segs)
                  for(const c of s) if(!isFinite(c)) bad=bad||(id+'/'+sub+'/'+rot+': non-finite segment');
              }
            });
          }
    ok(!bad,'every prism shape x medium x rotation traces finitely and stops ('+(bad||'ok')+')');
  }
  /* the white-light merge rule: WHERE the thirty wavelengths still lie within
     a line width of each other the beam is drawn once, in white.  The rule is
     a model function so it can be asserted here rather than only looked at. */
  withState({view:'prism',white:true},()=>{
    const P=buildModel(ST).prism;
    eq(P.groups.length,1,'one beam origin by default, so one white-light group');
    eq(P.groups[0].length,WHITE_WL.length,'and all '+WHITE_WL.length+' wavelengths in it');
    const m=mergeMask(P.groups[0].map(b=>b.tr),24);
    ok(m.length>=3,'the default prism path has at least three segments ('+m.length+')');
    ok(m[0]===true,'the beam ARRIVING at the prism is one line for every wavelength');
    ok(m[m.length-1]===false,'and the beam LEAVING it is not: that is the dispersion');
    /* the rule has to depend on the scale: zoom out far enough and everything merges */
    const m2=mergeMask(P.groups[0].map(b=>b.tr),0.02);
    ok(m2.every(v=>v),'at a small enough scale every segment merges');
    const m3=mergeMask(P.groups[0].map(b=>b.tr),4000);
    ok(!m3[1],'and at a large enough one even the path inside the prism separates');
  });
  /* the default beam is aimed near minimum deviation, where a prism actually
     disperses.  The previous default (-7 deg) put the ray on a left-in,
     right-TIR, bottom-out path whose deviation is nearly achromatic: that is
     real physics, and it is why this file no longer opens on it. */
  withState({view:'prism',white:true},()=>{
    const P=buildModel(ST).prism, g=P.groups[0];
    const a=[], b=[];
    for(const bn of g){ if(bn.tr.exitDir) a.push(Math.atan2(bn.tr.exitDir[1],bn.tr.exitDir[0])); }
    const spread=(Math.max.apply(null,a)-Math.min.apply(null,a))*RAD;
    ok(spread>0.8,'the default prism geometry disperses white light by '+fmt(spread,3)+' deg');
  });
  withState({view:'prism',white:true,beamY:1.3,beamTilt:-7},()=>{
    const g=buildModel(ST).prism.groups[0];
    const a=[];
    for(const bn of g){ if(bn.tr.exitDir) a.push(Math.atan2(bn.tr.exitDir[1],bn.tr.exitDir[0])); }
    const spread=(Math.max.apply(null,a)-Math.min.apply(null,a))*RAD;
    ok(spread<0.1,'while the constant-deviation path disperses by only '+fmt(spread,4)+' deg');
  });
  /* The busiest configurations the controls can reach: 2 500 of them were
     swept and none comes near PhET's 50-step limit, so these two are what
     pin the limit and the branch bookkeeping. */
  {
    const nEnv=indexOf(NA,650);
    const CASES=[['circle glass, y = 3, tilt 10',prismShape('circle'),[-11.5,3],10,NG,20,19,491.692816977193],
                 ['square diamond, y = 1.3, tilt 18.5',prismShape('square'),[-11.5,1.3],18.5,ND,11,11,277.203033350332]];
    for(const [nm,sh,p0,tdeg,nref,steps,ns,tot] of CASES){
      const d=[Math.cos(tdeg*DEG),Math.sin(tdeg*DEG)];
      const tr=traceRay(sh,p0,d,nEnv,indexOf(nref,650),{reflections:true,reach:46});
      eq(tr.steps,steps,nm+': step count (derive)');
      eq(tr.segs.length,ns,nm+': segment count (derive)');
      let L=0; for(const g of tr.segs) L+=Math.hypot(g[2]-g[0],g[3]-g[1]);
      rel(L,tot,1e-11,nm+': total drawn length (derive)');
      ok(tr.steps<PHET.maxSteps,nm+': inside PhET\u2019s limit of '+PHET.maxSteps);
    }
    /* and the MODEL takes the same path, so the view cannot drift from it */
    withState({view:'prism',prismId:'circle',beamY:3,beamTilt:10,showReflections:true},()=>{
      const tr=buildModel(ST).prism.bundles[0].tr;
      eq(tr.steps,20,'the prism view itself takes that path');
      eq(tr.segs.length,19,'and draws those segments');
    });
  }
  /* PhET stops drawing a reflected ray below 0.005 of the power */
  {
    ok(drawsReflected(0.0051)&&!drawsReflected(0.0049),
       'the reflected ray appears exactly at PhET\u2019s 0.005 floor');
    const B=boundaryModel(Object.assign({},DEFAULTS,{angDeg:45}));
    ok(drawsReflected(B.R),'so it IS drawn at the default 45 deg (R = '+fmt(B.R,4)+')');
    ok(B.R<0.2,'and it would NOT be if the floor were 0.2, which nothing else would notice');
    const C=boundaryModel(Object.assign({},DEFAULTS,{topSub:'custom',botSub:'custom',
                                                     topN:1.4,botN:1.4,angDeg:20}));
    ok(!drawsReflected(C.R),'two identical media reflect nothing, and nothing is drawn');
  }
  /* PhET's floors are really applied */
  {
    const tr=traceRay(prismShape('square'),[-12,0],[1,0],indexOf(NA,650),indexOf(NG,650),
                      {reflections:true});
    let lowest=1;
    for(const s of tr.segs) lowest=Math.min(lowest,s[4]);
    ok(lowest>=PHET.powerMin,'no branch below PhET’s power floor of '+PHET.powerMin+' is drawn');
    ok(tr.steps<=PHET.maxSteps,'and the tracer stops at PhET’s '+PHET.maxSteps+' steps');
  }

  /* the drawn worlds really are PhET's, and the clock really is a whole
     number of frames to the cycle (display constants, but printed ones) */
  eq(WORLD.xmax-WORLD.xmin,PHET.modelW,'the boundary world is PhET’s 62 red wavelengths wide');
  close(WORLD.ymax-WORLD.ymin,PHET.modelH,1e-12,'and PhET’s 43.4 tall');
  close(PHET.modelH,0.7*PHET.modelW,1e-12,'which is PhET’s 0.7 aspect exactly');
  close(48*PHASE_STEP,TAU,1e-15,'the wave clock takes exactly 48 frames to a cycle');
  eq(PHET.prismT,10,'the prism prototypes are 10 red wavelengths across (PhET’s value)');
  close(PHET.fanSpacing,0.5,0,'and PhET’s fan is spaced half a red wavelength');
  {
    const B=beamOrigins({beamTilt:0,beamY:0,manyRays:true});
    eq(B.origins.length,5,'which makes five rays, as PhET’s does');
    close(B.origins[1][1]-B.origins[0][1],PHET.fanSpacing,1e-12,'spaced by that amount');
  }

  /* ------------------------------------------- 9. layout, at four sizes */
  const SIZES=[[1180,740],[1400,820],[900,600],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const badRe=/NaN|undefined|Infinity/;
  /* The floors are DERIVED from what each configuration emits (build/
     bending-light/opcount.js prints them), not copied from another sim: a
     ray diagram is a dozen strokes and an op floor tuned on a field map
     would fail it for being efficient (Known-bad).  Counted as fills PLUS
     strokes, because the world views draw almost no fills at all. */
  const SWEEP=[
    ['bound default',{view:'bound'},14],
    ['bound TIR',{view:'bound',topSub:'water',botSub:'air',angDeg:70},14],
    ['bound white',{view:'bound',white:true,showProtractor:true},90],
    ['bound normal incidence',{view:'bound',angDeg:0,showAngles:true},14],
    ['bound laser off',{view:'bound',laserOn:false},7],
    ['wave default',{view:'wave'},130],
    ['wave TIR',{view:'wave',topSub:'glass',botSub:'air',angDeg:60},160],
    ['wave no field',{view:'wave',paintField:false},70],
    ['wave violet',{view:'wave',lamNm:400,angDeg:62,botSub:'diamond'},130],
    ['wave deep red',{view:'wave',lamNm:700,angDeg:15},130],
    ['prism triangle',{view:'prism'},8],
    ['prism white',{view:'prism',white:true,manyRays:true},120],
    ['prism diamond',{view:'prism',prismSub:'diamond',showReflections:true},14],
    ['prism circle',{view:'prism',prismId:'circle',showNormals:true},9],
    ['prism semicircle',{view:'prism',prismId:'semicircle',prismRot:35},8],
    ['fres default',{view:'fres'},28],
    ['fres TIR pair',{view:'fres',topSub:'glass',botSub:'air'},28],
    ['spec default',{view:'spec'},250],
    ['spec steep prism',{view:'spec',prismApex:75,prismSub:'diamond'},150],
    ['bow primary',{view:'bow'},180],
    ['bow secondary',{view:'bow',bowK:2,white:true},900],
  ];
  for(const [nm,over,minFills] of SWEEP) for(const [W,H] of SIZES) withState(over,()=>{
    const c=makeShot(W,H); let err=null;
    try{ drawView(c,W,H,buildModel(ST),ST); }catch(e){ err=e; }
    ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
    if(err) return;
    const texts=c.ops.filter(o=>o.op==='text');
    const draws=c.ops.filter(o=>o.op==='fill'||o.op==='stroke').length;
    ok(draws>=minFills&&texts.length>=3,
       nm+' '+W+'x'+H+' draws substance ('+draws+' draw ops, floor '+minFills+'; '+texts.length+' texts)');
    let bad=null;
    for(const t of texts){
      if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
      if(badRe.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
      if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'"'; break; } }
    ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
    /* the house #hint is HTML at bottom:11px and the capture cannot see it
       (wave-on-a-string Known-bad): reserve the corner */
    const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
    ok(!inHint.length,nm+' '+W+'x'+H+' nothing under the #hint line'
       +(inHint.length?' ("'+inHint[0].t.slice(0,30)+'")':''));
    let hit=null;
    for(let i=0;i<texts.length&&!hit;i++) for(let j=i+1;j<texts.length;j++){
      const a=texts[i].bb,b=texts[j].bb;
      const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
      if(ox>3&&oy>3){ hit='"'+texts[i].t.slice(0,22)+'" vs "'+texts[j].t.slice(0,22)+'"'; break; } }
    ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
  });

  /* every view emits something at the default size */
  for(const v of TABS.map(t=>t[0])) withState({view:v},()=>{
    const c=makeShot(1180,740);
    drawView(c,1180,740,buildModel(ST),ST);
    const tx=c.ops.filter(o=>o.op==='text').length;
    ok(c.ops.length>=18&&tx>=5,'view "'+v+'" draws '+c.ops.length+' operations and '+tx+' labels');
  });
  /* the drawn picture really follows the angle: two angles must differ */
  {
    const sig=a=>{ let s=''; withState({view:'bound',angDeg:a},()=>{
      const c=makeShot(1180,740); drawView(c,1180,740,buildModel(ST),ST);
      s=JSON.stringify(c.ops.filter(o=>o.op!=='text').length)+'|'+
        JSON.stringify(c.ops.filter(o=>o.op==='text').map(o=>o.t).join(';')); }); return s; };
    ok(sig(20)!==sig(60),'the boundary view draws a different picture at 20 and 60 degrees');
  }
  /* the canvas carries no letter subscripts (there is no Unicode subscript f,
     and the rasteriser's font does not have all of the ones that exist) */
  {
    let bads=[];
    for(const v of TABS.map(t=>t[0])) withState({view:v},()=>{
      const c=makeShot(1180,740);
      drawView(c,1180,740,buildModel(ST),ST);
      for(const o of c.ops) if(o.op==='text'&&/[ₐ-ₜᵢ-ᶻ]/.test(o.t)) bads.push(o.t);
    });
    eq(bads.length,0,'no letter subscripts reach the canvas (greenhouse-effect Known-bad)'
       +(bads.length?': '+bads[0]:''));
  }

  Object.assign(ST,stSave); clearMemo();
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
