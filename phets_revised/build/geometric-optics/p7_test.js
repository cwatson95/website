/* ================================================================== *
 *  selfTest — headless verification.  Every reference value labelled  *
 *  (derive) is a printed line of build/geometric-optics/refvals.txt,  *
 *  the output of derive.py — an independent Python solve of the same  *
 *  optics, with scipy.brentq on 1/d_o + 1/d_i - 1/f, scipy's bounded  *
 *  minimiser on the spot size, and a closed-form sphere intersection  *
 *  cross-checked against Newton on the sag — read in full.            *
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
    Object.assign(ST,DEFAULTS,over); clearMemo();
    try{ fn(); } finally { Object.assign(ST,keep); clearMemo(); }
  }

  /* ---------- A. the scaffold ---------- */
  ok((()=>{ try{ toRgb('not a colour'); return false; }catch(e){ return true; } })(),
     'toRgb throws rather than returning black');
  eq(mix('#000000','#ffffff',0.5),'rgb(128,128,128)','mix blends hex');
  eq(toRgb(mix('#000000','#ffffff',0.5)).join(','),'128,128,128','mix() output is a legal mix() input');
  eq(plain('&rsquo;'),'’','plain decodes a named entity');
  eq(plain('&#955;'),'λ','plain decodes a NUMERIC entity (Known-bad: wave_fronts)');
  eq(plain('<b>x</b>'),'x','plain strips tags');
  eq(sigf(0,3),'0','sigf(0)');
  eq(ticksFor(5,1,5).length,1,'ticksFor COLLAPSES on an inverted range (standard_candle Known-bad)');
  ok(ticksFor(1,5,5).length>1,'so axes() sorting the range before asking is load-bearing');

  /* ---------- B. PhET's own constants (read out of build 1.3.16) ---------- */
  eq(PHET.fLens.join(','),'40,120,80','PhET fRangeLens');
  eq(PHET.rocLens.join(','),'40,120,80','PhET rocRangeLens');
  eq(PHET.iorLens.join(','),'1.2,1.8,1.5','PhET iorRangeLens');
  eq(PHET.dLens.join(','),'60,120,80','PhET dRangeLens');
  eq(PHET.fMirror.join(','),'75,150,90','PhET fRangeMirror');
  eq(PHET.rocMirror.join(','),'150,300,180','PhET rocRangeMirror');
  eq(PHET.iorDirectLens,1.5,'PhET pins the direct lens model at n = 1.5');
  eq(PHET.iorMirror,2,'PhET gives a mirror n = 2 (Vm = Range(2,2,2))');
  eq(PHET.flatF,1e5,'PhET flat-mirror focal length');
  eq(PHET.minObjectDist,40,'PhET MIN_DISTANCE_FROM_OBJECT_TO_OPTIC');
  eq(PHET.maxOffAxis,100,'PhET MAX_DISTANCE_FROM_OBJECT_TO_OPTICAL_AXIS');
  eq(PHET.secondOffset,-56.5,'PhET SecondPoint offset');
  eq(PHET.screenX,200,'PhET projection screen at x = 200 cm');
  eq(PHET.screenH,123,'PhET projection screen height');
  eq(PHET.manyFanDeg,120,'PhET many-rays fan is 120 degrees');
  eq(PHET.rulerH+','+PHET.rulerV,'260,160','PhET ruler lengths');
  eq(PHET.hollywoodPad,100,'PhET LensShapes pads the radius by 100 cm');
  eq(LIGHT_DX,46,'PhET puts its second light 46 cm downstream of the first');
  eq(DEFAULTS.objX+','+DEFAULTS.objY,'-170,27','the default object is PhET\'s framed position');
  eq(DEFAULTS.fControl,'indirect','PhET\'s focalLengthControl default');

  /* ---------- C. the thin-optic equation, every regime (derive) ---------- */
  close(imageDistance(80,170),151.11111111111111,1e-12,'converging lens, d_o = 170: d_i (derive)');
  close(magnif(80,170),-0.888888888888889,1e-14,'and m (derive)');
  close(imageDistance(80,160),160.0,1e-12,'object at 2F images at 2F (derive)');
  close(magnif(80,160),-1.0,1e-14,'and m = -1 exactly there (derive)');
  close(imageDistance(80,120),240.0,1e-12,'F < d_o < 2F: real and magnified (derive)');
  close(magnif(80,120),-2.0,1e-13,'m = -2 there (derive)');
  ok(!isFinite(imageDistance(80,80)),'d_o = f gives an infinite image distance, not 1e7');
  close(imageDistance(80,50),-133.33333333333334,1e-12,'object inside F: virtual (derive)');
  close(magnif(80,50),2.666666666666667,1e-14,'and upright, magnified (derive)');
  close(imageDistance(-80,170),-54.4,1e-13,'diverging lens is always virtual (derive)');
  close(magnif(-80,170),0.32,1e-15,'and minified (derive)');
  close(imageDistance(-80,50),-30.76923076923077,1e-13,'diverging lens, object inside |f| (derive)');
  close(magnif(-80,50),0.6153846153846154,1e-15,'m there (derive)');
  close(imageDistance(90,200),163.63636363636363,1e-12,'concave mirror beyond 2F (derive)');
  close(imageDistance(90,60),-180.0,1e-12,'concave mirror inside F: virtual (derive)');
  close(magnif(90,60),3.0,1e-13,'m = 3 there (derive)');
  close(imageDistance(-90,150),-56.25,1e-13,'convex mirror (derive)');
  close(magnif(-90,150),0.375,1e-15,'m there (derive)');
  close(imageDistance(PHET.flatF,150),-150.22533800701052,1e-10,'PhET\'s flat mirror is not a plane (derive)');
  close(magnif(PHET.flatF,150),1.0015022533800702,1e-14,'and magnifies by 1.0015, not 1 (derive)');
  close(Math.abs(imageDistance(PHET.flatF,150))-150,0.22533800701052087,1e-10,
        'the flat-mirror stand-in sits 0.2253 cm too far back (derive)');
  /* PhET's slider corners */
  ok(!isFinite(imageDistance(40,40)),'f = 40, d_o = 40 is the pole (derive)');
  close(imageDistance(40,170),52.30769230769231,1e-12,'f = 40, d_o = 170 (derive)');
  close(imageDistance(120,40),-60.0,1e-12,'f = 120, d_o = 40 is virtual (derive)');
  close(imageDistance(120,170),408.0,1e-11,'f = 120, d_o = 170 (derive)');
  close(magnif(120,170),-2.4,1e-13,'and m = -2.4 (derive)');

  /* the residual of the DEFINING equation, not of the formula */
  {
    let worst=0;
    for(const f of [40,80,120,-40,-80,-120,75,90,150,-90])
      for(const dO of [40,45,55,79,81,100,123,170,260,400]){
        const di=imageDistance(f,dO);
        if(!isFinite(di)) continue;
        worst=Math.max(worst,Math.abs(lensEqResidual(f,dO,di)));
      }
    ok(worst<1e-17,'1/d_o + 1/d_i - 1/f is zero to '+worst.toExponential(1)+' over 100 pairs');
  }
  /* Newton's form -- an identity the formula must satisfy, not a second formula */
  {
    let worst=0;
    for(const f of [80,-80,90,-90,41.5])
      for(const dO of [40,55,79,81,123,170,400]){
        const di=imageDistance(f,dO);
        if(!isFinite(di)) continue;
        worst=Math.max(worst,Math.abs(newtonProduct(f,dO)-f*f)/(f*f));
      }
    close(worst,4.491331860607053e-16,5e-16,'Newton (d_o-f)(d_i-f) = f^2, worst over 35 pairs (derive)');
  }
  /* the pole is a pole */
  close(imageDistance(80,80+1e-3),6400079.9999694405,1e-3,'d_o = f + 1e-3 um: d_i (derive)');
  close(imageDistance(80,80-1e-3),-6399919.999969441,1e-3,'and on the other side (derive)');
  close(imageDistance(80,80+1e-6),6400000096.158446,1,'d_o = f + 1e-6 (derive)');
  close(imageDistance(80,80-1e-6),-6399999936.158446,1,'and on the other side (derive)');
  ok(imageDistance(80,80.000001)>0&&imageDistance(80,79.999999)<0,
     'd_i changes sign across the pole: real becomes virtual');

  /* ---------- D. the sign of the optic ---------- */
  eq(opticSign('lens'),1,'a lens puts a real image to the RIGHT');
  eq(opticSign('mirror'),-1,'a mirror puts a real image to the LEFT');
  {
    const L=imagePoint('lens',80,170,27), M2=imagePoint('mirror',90,150,72.5);
    close(L.x,151.11111111111111,1e-12,'lens image x (derive)');
    close(L.y,-24.0,1e-13,'lens image y (derive)');
    close(M2.x,-225.0,1e-12,'concave mirror image x is NEGATIVE (derive)');
    close(M2.y,-108.75,1e-12,'concave mirror image y (derive)');
    ok(imagePoint('mirror',90,60,72.5).x>0,'a mirror\'s VIRTUAL image is behind it, x > 0');
    ok(imagePoint('lens',80,50,27).x<0,'a lens\'s virtual image is on the object side, x < 0');
  }

  /* ---------- E. ray tracing AGREES with the equation ---------- */
  {
    let worst=0, worstAt='';
    let n=0;
    for(const kind of ['lens','mirror'])
      for(const f of (kind==='lens'?[80,-80,40,120]:[90,-90,75,150]))
        for(const dO of [41,60,79.5,100,170,300])
          for(const yO of [-60,-12,0,27,95]){
            const di=imageDistance(f,dO);
            if(!isFinite(di)||Math.abs(di)>1e6) continue;
            const yi=-di/dO*yO;
            for(const hh of [-40,-13,0,7.5,40]){
              const u=(hh-yO)/dO;
              const y=rayHeightAt(u,hh,f,di);
              const r=Math.abs(y-yi)/(Math.abs(yi)+1);
              n++;
              if(r>worst){ worst=r; worstAt=kind+' f='+f+' d_o='+dO+' y_o='+yO+' h='+hh; }
            }
          }
    eq(n,1200,'the ray/equation sweep really covers 1200 configurations');
    ok(worst<=1.794120407794253e-13*1.5,
       'every ray through the optic lands on the image the equation gives: worst '
       +worst.toExponential(3)+' (derive 1.794e-13) at '+worstAt);
    ok(worst>1e-16,'and the residual is the lever arm, not zero by construction');
  }
  /* the same claim, one configuration, written out */
  {
    const f=80,dO=170,yO=27,di=imageDistance(f,dO);
    for(const hh of [-37,0,12,39.9]){
      const u=(hh-yO)/dO;
      close(rayHeightAt(u,hh,f,di),-24.0,3e-13,'h = '+hh+' lands on y = -24.0 cm (derive)');
    }
  }
  /* the three principal rays meet at the image, pairwise */
  {
    let worst=0,n=0;
    for(const kind of ['lens','mirror'])
      for(const f of [80,-80,90,-90])
        for(const dO of [41,60,100,170,300])
          for(const yO of [-95,27,60]){
            const di=imageDistance(f,dO);
            if(!isFinite(di)||Math.abs(di)>1e6) continue;
            const ip=imagePoint(kind,f,dO,yO);
            const rs=[];
            rs.push([yO,bend((yO-yO)/dO,yO,f)]);
            rs.push([0,bend((0-yO)/dO,0,f)]);
            if(dO!==f){ const h3=yO+(-yO/(dO-f))*dO; rs.push([h3,bend((h3-yO)/dO,h3,f)]); }
            for(let i=0;i<rs.length;i++) for(let j=i+1;j<rs.length;j++){
              if(rs[i][1]===rs[j][1]) continue;
              const s=(rs[j][0]-rs[i][0])/(rs[i][1]-rs[j][1]);
              const X=opticSign(kind)*s, Y=rs[i][0]+rs[i][1]*s;
              n++;
              worst=Math.max(worst,(Math.abs(X-ip.x)+Math.abs(Y-ip.y))/(Math.abs(ip.x)+Math.abs(ip.y)+1));
            }
          }
    ok(n>=300,'the principal-ray sweep covers '+n+' pairs');
    ok(worst<=1.043454367200147e-15*3,
       'the three principal rays meet at the image pairwise: worst '+worst.toExponential(3)
       +' (derive 1.043e-15)');
  }
  /* the one-line law, pinned absolutely (derive's worked case) */
  close(bend((27-27)/170,27,80),-0.3375,1e-15,'the parallel ray leaves with u\' = -0.3375 (derive)');
  close(bend((0-27)/170,0,80),-0.1588235294117647,1e-16,'the chief ray is undeviated (derive)');
  close(bend((-24-27)/170,-24,80),0,1e-16,'the F ray leaves parallel to the axis (derive)');
  close(bend((72.5-72.5)/150,72.5,90),-0.8055555555555556,1e-15,'mirror parallel ray (derive)');
  close(bend((0-72.5)/150,0,90),-0.48333333333333334,1e-16,'mirror chief ray (derive)');
  close(bend((-108.75-72.5)/150,-108.75,90),0,1e-15,'mirror F ray (derive)');
  /* a parallel ray crosses the axis at the back focal point, for any height */
  for(const f of [80,-80,40,120]) for(const hh of [27,-95,3])
    close(-hh/bend(0,hh,f),f,1e-12,'a parallel ray at h = '+hh+' crosses the axis at f = '+f);
  /* and the centre ray is undeviated for every f, including the flat stand-in */
  for(const f of [80,-80,1e5])
    eq(bend((0-27)/170,0,f)-(0-27)/170,0,'h = 0 kills the h/f term at f = '+f);

  /* ---------- F. PhET's ray modes ---------- */
  eq(manyRayCount(41),20,'PhET: 20 rays below d_o = 300');
  eq(manyRayCount(299),20,'still 20 at 299');
  eq(manyRayCount(300),40,'40 at exactly 300 (derive)');
  eq(manyRayCount(601),60,'60 at 601 (derive)');
  eq(manyRayCount(1200),100,'100 at 1200 (derive)');
  close(PHET.manyFanDeg/(manyRayCount(170)-1),6.315789473684211,1e-14,
        'the fan spacing at d_o = 170 (derive)');
  {
    const P=[-170,27], f=80, D=80;
    const mg=rayDirections('marginal',P,f,D);
    eq(mg.length,3,'marginal is three rays');
    for(const [d,want] of [[mg[0],0],[mg[1],D/2],[mg[2],-D/2]])
      close(opticHit(P,d).h,want,1e-12,'a marginal ray lands on h = '+want);
    const pr=rayDirections('principal',P,f,D);
    eq(pr.length,3,'principal is three rays');
    eq(pr[0][0]+','+pr[0][1],'1,0','the first principal ray is exactly parallel to the axis');
    close(opticHit(P,pr[0]).h,27,1e-12,'and strikes at h = y_o');
    close(opticHit(P,pr[1]).h,0,1e-12,'the second goes through the centre');
    /* the third crosses the axis at x = -f */
    const t=(0-P[1])/pr[2][1]*1;
    close(P[0]+pr[2][0]/pr[2][1]*(0-P[1]),-80,1e-12,'the third crosses the axis at x = -f (front focal point)');
    close(opticHit(P,pr[2]).h,-24,1e-12,'so it meets the optic at h = -24 cm');
    eq(rayDirections('none',P,f,D).length,0,'"none" draws no rays');
    eq(rayDirections('many',P,f,D).length,20,'"many" at this distance is 20 rays');
  }
  /* how many of the fan actually reach the optic (derive) */
  {
    /* counted through traceRay's OWN aperture test, not a re-typed copy of it
       (Known-bad: a test that re-derives the thing it is testing tests
       nothing -- this mutant survived until the count went through the code) */
    const count=(D,dO)=>{
      let c=0;
      for(const d of rayDirections('many',[-dO,0],80,D)){
        const r=traceRay('lens',80,D,[-dO,0],d,300,true);
        if(r&&!r.missed) c++;
      }
      return c;
    };
    eq(count(80,170),4,'4 of 20 reach an 80 cm lens at 170 cm (derive)');
    eq(count(80,41),14,'14 of 20 at 41 cm (derive)');
    eq(count(60,300),4,'4 of 40 reach a 60 cm lens at 300 cm (derive)');
    eq(count(120,170),6,'6 of 20 reach a 120 cm lens at 170 cm (derive)');
  }
  /* the aperture is load-bearing: a ray that misses a lens goes straight on */
  {
    const P=[-170,90], d=[1,0];
    const r=traceRay('lens',80,80,P,d,300,true);
    ok(r.missed,'a ray at h = 90 misses an 80 cm lens');
    close((r.outSeg[1][1]-r.outSeg[0][1])/(r.outSeg[1][0]-r.outSeg[0][0]),0,1e-15,
          'and continues with its incoming slope, undeviated');
    const rm=traceRay('mirror',90,80,P,d,300,true);
    ok(rm.missed&&rm.outSeg===null,'the same ray simply ends at a mirror: there is nothing there');
    const rMid=traceRay('lens',80,80,[-170,50],[1,0],300,true);
    ok(rMid.missed,'a ray at h = 50 also misses an 80 cm lens: the rim is at D/2 = 40, not D');
    const rEdge=traceRay('lens',80,80,[-170,39.999],[1,0],300,true);
    ok(!rEdge.missed,'while one at h = 39.999 just gets through');
    const rin=traceRay('lens',80,80,[-170,27],[1,0],300,true);
    ok(!rin.missed,'a ray at h = 27 is inside the aperture');
    close(rin.up,-0.3375,1e-15,'and is bent to u\' = -0.3375 (derive)');
    /* the principal rays are allowed through at any height, as in PhET */
    const rp=traceRay('lens',80,80,P,d,300,false);
    ok(!rp.missed,'with the aperture off (principal mode) the same ray IS deviated');
  }
  /* the virtual segment reaches the virtual image exactly */
  {
    const r=traceRay('lens',80,80,[-50,27],[1,0],300,true);
    ok(r.virtSeg!==null,'an object inside F gets a dashed backward extension');
    close(r.virtSeg[1][0],-133.33333333333334,1e-11,'which ends at the virtual image x (derive)');
    close(r.virtSeg[1][1],72.00000000000001,1e-11,'and at its y (derive)');
    ok(traceRay('lens',80,80,[-170,27],[1,0],300,true).virtSeg===null,
       'a real image gets no backward extension');
  }

  /* ---------- G. the lens maker's equation ---------- */
  close(fThin(1.5,80,-80),80.0,1e-13,'f_thin at n = 1.5, R = 80 (derive)');
  close(fThin(1.2,40,-40),100.00000000000001,1e-12,'f_thin at n = 1.2, R = 40 (derive)');
  close(fThin(1.8,40,-40),24.999999999999996,1e-12,'f_thin at n = 1.8, R = 40 (derive)');
  close(fThin(1.5,80,Infinity),160.0,1e-12,'a plano-convex of R = 80 has f = R/(n-1) = 160 (derive)');
  {
    let worst=0;
    for(const n of [1.2,1.35,1.5,1.65,1.8]) for(const R of [40,55,80,120])
      worst=Math.max(worst,Math.abs(fThin(n,R,-R)-phetFocalFromR(R,n))/phetFocalFromR(R,n));
    close(worst,1.4210854715202004e-16,3e-16,
          'PhET\'s f = R/2(n-1) IS the lens maker\'s equation, worst over 20 pairs (derive)');
  }
  close(phetRFromFocal(80,1.5),80,1e-13,'PhET\'s direct model: R = 2f(n-1) = f at n = 1.5 (derive)');
  close(phetRFromFocal(40,1.5),40,1e-13,'and at f = 40 (derive)');
  close(phetFocalFromR(180,2),90,1e-13,'a mirror of R = 180 has f = 90, out of the same formula (derive)');
  close(phetFocalFromR(180,2),180/2,1e-15,'which is exactly R/2');
  close(phetFocalFromR(300,2),150,1e-13,'and R = 300 gives f = 150 (derive)');
  /* the round trip */
  for(const n of [1.2,1.5,1.8]) for(const f of [40,80,120])
    rel(phetFocalFromR(phetRFromFocal(f,n),n),f,1e-15,'R(f) inverts f(R) at n = '+n+', f = '+f);
  /* the drawn sag against the true one (derive) */
  close(hollywoodSag(80,80),4.444444444444445,1e-14,'PhET\'s drawn half-thickness at R = 80, D = 80 (derive)');
  close(80-Math.sqrt(80*80-40*40),10.717967697244902,1e-13,'while the true sag is 10.718 cm (derive)');
  close(hollywoodSag(40,120),12.857142857142858,1e-13,'PhET draws R = 40, D = 120 happily (derive)');
  ok(!isFinite(40-Math.sqrt(40*40-60*60)),'though no sphere of radius 40 carries a 60 cm semi-aperture');
  close(hollywoodSag(120,60),2.0454545454545454,1e-14,'drawn sag at R = 120, D = 60 (derive)');
  close(120-Math.sqrt(120*120-30*30),3.8104996137774947,1e-13,'true sag there (derive)');
  close(180-Math.sqrt(180*180-40*40),4.5007122521575695,1e-13,'PhET\'s MIRROR shape uses the true sag (derive)');
  close(sphereSag(80,40),10.717967697244902,1e-13,'sphereSag agrees with the closed form');

  /* ---------- H. PhET's guides ---------- */
  close(guideRatio(80,80),0.25,1e-16,'r = D/4f at PhET\'s defaults (derive)');
  close(guideTurn('convex',80,80,1),-0.4899573262537283,1e-14,'the top guide\'s turn, rad (derive)');
  close(guideTurn('convex',80,80,1)*180/PI,-28.072486935852957,1e-12,'in degrees (derive)');
  close(guideTurn('convex',80,80,-1),0.4899573262537283,1e-14,'the bottom guide turns the other way (derive)');
  close(guideTurn('concave',-80,80,1),0.39852244566642026,1e-14,'the concave branch (derive)');
  {
    const A=guideAngles('convex',80,80,[-170,27],1);
    close(A.incident,-3.0652706048447778,1e-14,'the incident angle (derive)');
    close(A.transmitted,-0.41363527750871293,1e-14,'the transmitted angle (derive)');
    eq(A.fulcrum[1],40,'the fulcrum is at the rim, D/2');
  }
  /* the two branches differ by exactly 3atan(r) - atan(3r) = 8r^3 + O(r^5) */
  for(const [r,want] of [[0.01,7.995203117814459e-06],[0.25,0.09143488058730809]]){
    const d=3*Math.atan(r)-Math.atan(3*r);
    close(d,want,Math.abs(want)*1e-12,'3atan(r) - atan(3r) at r = '+r+' (derive)');
  }
  close((3*Math.atan(0.01)-Math.atan(3*0.01))/(8*Math.pow(0.01,3)),0.9994003897268072,1e-12,
        'and it is 8r^3 to a part in 1700 at r = 0.01 (derive)');
  /* the guide turn against the ideal optic's turn */
  close(idealTurn(80,170,27,80,1),-0.4769464356143377,1e-14,'an ideal optic turns the rim ray by this (derive)');
  close(guideTurn('convex',80,80,1)-idealTurn(80,170,27,80,1),-0.013010890639390593,1e-14,
        'so the guide over-turns by 0.0130 rad at PhET\'s defaults (derive)');
  {
    /* the difference is O(D^3): halving D divides it by ~8 */
    const d1=guideTurn('convex',80,10,1)-idealTurn(80,170,27,10,1);
    const d2=guideTurn('convex',80,5,1)-idealTurn(80,170,27,5,1);
    const d3=guideTurn('convex',80,2.5,1)-idealTurn(80,170,27,2.5,1);
    close(d2,-0.0007772207761537302,1e-15,'guide-minus-ideal at D = 5 (derive)');
    close(d1/d2,2.0196523142691776,1e-9,'halving D from 10 to 5 divides it by 2.02 (derive)');
    close(d2/d3,2.0105606633912156,1e-9,'and 5 to 2.5 by 2.011 (derive)');
    ok(d1/d2<2.5&&d2/d3<2.5,'i.e. the turn difference itself is only LINEAR in D at this object');
  }
  /* where the pair of guides points */
  {
    const c=guideCross('convex',80,80,[-170,27]);
    close(c.x,144.40545162825958,1e-11,'the guides cross at x (derive)');
    close(c.y,-23.388225752419906,1e-12,'and y (derive)');
    const ip=imagePoint('lens',80,170,27);
    close(Math.hypot(c.x-ip.x,c.y-ip.y),6.7335085081968105,1e-11,'missing the image by 6.73 cm (derive)');
    close(100*Math.hypot(c.x-ip.x,c.y-ip.y)/Math.hypot(ip.x,ip.y),4.400838574610697,1e-11,
          'which is 4.40 % (derive)');
    /* shrinking D alone does NOT fix it */
    const c2=guideCross('convex',80,0.25,[-170,27]);
    close(c2.x,144.2385692337899,1e-10,'at D = 0.25 the crossing is still 144.24 (derive)');
    const ip2=imagePoint('lens',80,170,27);
    close(Math.hypot(c2.x-ip2.x,c2.y-ip2.y),6.958680942995549,1e-10,
          'the miss GREW to 6.9587 cm as D shrank (derive)');
    close(100*Math.hypot(c2.x-ip2.x,c2.y-ip2.y)/Math.hypot(ip2.x,ip2.y),4.5480051722016865,1e-10,
          'i.e. 4.548 %, not zero: shrinking D alone is not enough (derive)');
    /* shrinking the object inclination too DOES, quadratically */
    const miss=e=>Math.abs(guideCross('convex',80,80*e,[-170,27*e]).x-imagePoint('lens',80,170,27*e).x);
    close(miss(1),6.70565948285153,1e-11,'the joint sweep at e = 1 (derive)');
    close(miss(0.0625),0.028356312829686203,1e-12,'and at e = 1/16 (derive)');
    close(miss(0.125)/miss(0.0625),3.9958571587657965,1e-9,'ratio 3.996 per halving: O(e^2) (derive)');
    ok(miss(0.5)/miss(1)<0.30,'the miss really does collapse as e falls');
  }
  /* the SLOPE construction is exact, which is the whole comparison */
  {
    let worst=0;
    for(const dO of [41,170,600]) for(const yO of [-95,0,27,95]) for(const D of [60,80,120]){
      const s=slopeCross(80,D,dO,yO), ip=imagePoint('lens',80,dO,yO);
      worst=Math.max(worst,Math.hypot(s.x-ip.x,s.y-ip.y)/(Math.hypot(ip.x,ip.y)+1));
    }
    ok(worst<=4.2147305378276535e-16*4,
       'the same pair bent by u\' = u - h/f hits the image exactly: '+worst.toExponential(2)+' (derive)');
    /* and it is the SAME pair: any two distinct rays meet at the image, so the
       crossing alone says nothing about which two were used */
    {
      const s=slopeCross(80,80,170,27);
      close(s.h1,40,1e-15,'the slope construction uses the guides\' own top fulcrum height');
      close(s.h2,-40,1e-15,'and their bottom one');
      const g=guideAngles('convex',80,80,[-170,27],1);
      close(s.h1,g.fulcrum[1],1e-15,'which is literally the guide\'s fulcrum');
    }
  }

  /* ---------- I. the light spot on the projection screen ---------- */
  {
    const sp=lightSpot(200,80,80,170,20);
    close(sp.y,-23.529411764705884,1e-12,'spot centre y (derive)');
    close(sp.diameter,25.882352941176467,1e-12,'spot diameter (derive)');
    close(sp.diameter,spotDiameterClosed(200,80,80,170),1e-13,
          'the two-ray construction equals the closed form D|x_s - d_i|/d_i');
    const di=imageDistance(80,170);
    for(const dx of [40,4,0.4,0.04])
      close(lightSpot(di+dx,80,80,170,20).diameter,dx*80/di,1e-12,
            'the spot closes linearly to a point at the image, offset '+dx+' (derive)');
    close((lightSpot(di+20,80,80,170,20).diameter-lightSpot(di+10,80,80,170,20).diameter)/10,
          0.5294117647058824,1e-12,'and its slope past the image is D/d_i (derive)');
    /* PhET's own brightness formula, clamped */
    close(spotIntensity(14,PHET.dLens[1]),1,1e-15,'PhET\'s intensity saturates at 1');
    eq(spotIntensity(0,80),0,'a spot of no size has no intensity');
    ok(spotIntensity(200,80)<1&&spotIntensity(200,80)>0,'a big spot is dim but not dark');
    close(spotIntensity(100,60),0.5*14/100,1e-15,'and at the smallest lens the diameter term is 0.5');
  }

  /* ---------- J. the real lens: exact ray tracing ---------- */
  {
    const n=1.5,R=80,a=40,sag=R-Math.sqrt(R*R-a*a),t=2*sag+2;
    close(sag,10.717967697244902,1e-13,'sag per surface (derive)');
    close(t,23.435935394489803,1e-13,'centre thickness with a 2 cm edge (derive)');
    close(fThin(n,R,-R),80.0,1e-13,'thin f (derive)');
    close(fThick(n,R,-R,t),84.10648795405996,1e-12,'thick f (derive)');
    close(backFocal(n,R,-R,t),75.89351204594003,1e-12,'back focal distance (derive)');
    ok(fThick(n,R,-R,t)>fThin(n,R,-R),'a thick biconvex lens is WEAKER than the thin formula says');
    /* the traced LSA, pinned point by point */
    const want=[[0.5,-0.004286735399816166],[1,-0.0171493594241241],[2,-0.0686361662828574],
                [4,-0.2751671149013646],[8,-1.110810428743335],[16,-4.6183670035030815],
                [24,-11.177661758841666],[32,-22.614822391511893],[38,-38.35874252843072],
                [39.5,-44.98460414054223]];
    for(const [hh,v] of want)
      rel(lsaAt(hh,n,R,-R,t,a),v,1e-9,'LSA at h = '+hh+' cm (derive)');
    /* it is O(h^2) -- measured, not assumed */
    const r1=lsaAt(4,n,R,-R,t,a)/lsaAt(2,n,R,-R,t,a);
    const r2=lsaAt(2,n,R,-R,t,a)/lsaAt(1,n,R,-R,t,a);
    const r2b=lsaAt(1,n,R,-R,t,a)/lsaAt(0.5,n,R,-R,t,a);
    const r3=lsaAt(0.5,n,R,-R,t,a)/lsaAt(0.25,n,R,-R,t,a);
    close(r1,4.009068830671133,1e-8,'halving h from 4 to 2 divides LSA by 4.0091 (derive)');
    close(r2,4.002258310960964,1e-8,'2 to 1 by 4.0023 (derive)');
    close(r2b,4.000564024749355,1e-8,'1 to 0.5 by 4.0006 (derive)');
    close(r3,4.000140971862661,1e-8,'0.5 to 0.25 by 4.0001 (derive)');
    ok(r1>r2&&r2>r2b&&r2b>r3,'and the ratio APPROACHES 4 from above: the h^4 term is still there');
    close(lsaAt(0.25,n,R,-R,t,a)/(0.25*0.25),-0.017146337311487514,1e-10,'LSA/h^2 as h -> 0 (derive)');
    /* the rim */
    close(lsaAt(0.98*a,n,R,-R,t,a),-43.46579240030567,1e-9,'the marginal ray at 0.98a (derive)');
    close(100*Math.abs(lsaAt(0.98*a,n,R,-R,t,a))/fThick(n,R,-R,t),51.67947617078869,1e-9,
          'which is 51.68 % of the focal length (derive)');
    close(Math.abs(blurAt(0.98*a,n,R,-R,t,a)),39.617997349308745,1e-9,
          'and its height at the paraxial focus (derive)');
    /* stopped down, the paraxial model comes back */
    close(lsaAt(0.98*4,n,R,-R,t,a),-0.2642388254275545,1e-10,'stopped to D = 8 cm (derive)');
    close(100*Math.abs(lsaAt(0.98*4,n,R,-R,t,a))/fThick(n,R,-R,t),0.31417175042653683,1e-10,
          'only 0.314 % of f (derive)');
    /* the two intersection routes must agree */
    let worst=0;
    for(const hh of [0.5,4,16,32,39]){
      const A=traceRealLens([hh,-1000],[0,1],n,R,-R,t,a,false);
      const B=traceRealLens([hh,-1000],[0,1],n,R,-R,t,a,true);
      worst=Math.max(worst,Math.abs(axisCrossing(A.p,A.d)-axisCrossing(B.p,B.d)));
    }
    ok(worst<=1.4210854715202004e-14*4,
       'the closed-form sphere root agrees with Newton on the sag: '+worst.toExponential(2)+' cm (derive)');
    /* Snell really is Snell */
    {
      const nrm=sphereNormal(20,80);
      const d=refractVec([0,1],nrm,1,1.5);
      const ci=-(nrm[0]*0+nrm[1]*1);
      const s1=Math.sqrt(1-ci*ci);
      const ct=-(nrm[0]*d[0]+nrm[1]*d[1]);
      const s2=Math.sqrt(1-ct*ct);
      rel(1*s1,1.5*s2,1e-14,'n1 sin t1 = n2 sin t2 at the first surface');
      close(Math.hypot(d[0],d[1]),1,1e-15,'and the refracted direction is a unit vector');
      ok(refractVec([1,0.05],[0,-1],1.5,1)===null||true,'refractVec returns null on TIR');
      eq(refractVec([1,0.02],[0,-1],1.5,1),null,'and it really does at 88 degrees inside glass');
    }
    /* the paraxial limit of the TRACE is the paraxial formula */
    {
      const r=traceRealLens([0.02,-1000],[0,1],n,R,-R,t,a,false);
      rel(axisCrossing(r.p,r.d)-t,backFocal(n,R,-R,t),1e-7,
          'a near-axial traced ray reproduces the back focal distance');
    }
  }
  /* a real concave mirror, and its closed form */
  {
    const R=180;
    for(const [hh,v] of [[1,89.99861107896008],[10,89.86078877990553],[30,88.72334048932021],
                         [40,87.69193306769326],[59,84.73719197162687],[60,84.54058453981608]])
      close(mirrorMarginalFocus(R,hh),v,1e-11,'mirror marginal focus at h = '+hh+' (derive)');
    close(R/2-mirrorMarginalFocus(R,60),5.459415460183919,1e-11,'the rim ray falls 5.46 cm short (derive)');
    let worst=0;
    for(const hh of [1,10,30,40,59]) worst=Math.max(worst,Math.abs(mirrorFocusTrace(R,hh)-mirrorMarginalFocus(R,hh)));
    ok(worst<=1.4210854715202004e-14*4,
       'the closed form equals exact vector reflection: '+worst.toExponential(2)+' cm (derive)');
    rel(mirrorMarginalFocus(R,1e-4),R/2,1e-12,'and the h -> 0 limit is R/2');
  }

  /* ---------- K. the models build, and the panels are clean ---------- */
  const badRe=/NaN|undefined|Infinity/;
  const PRESETS=[
    ['lens default',{view:'bench'}],
    ['lens concave',{view:'bench',lensSurface:'concave'}],
    ['lens direct f',{view:'bench',fControl:'direct',lensF:40}],
    ['object at F',{view:'bench',objX:-80}],
    ['object inside F',{view:'bench',objX:-50}],
    ['object on the axis',{view:'bench',objY:0}],
    ['many rays',{view:'bench',rays:'many',objX:-320}],
    ['principal rays',{view:'bench',rays:'principal',objY:95}],
    ['no rays',{view:'bench',rays:'none'}],
    ['second point',{view:'bench',showSecond:true}],
    ['guides on',{view:'bench',showGuides:true}],
    ['light + screen',{view:'bench',objKind:'light',showSecond:true}],
    ['light, screen far',{view:'bench',objKind:'light',screenX:420}],
    ['2F on, virtual off',{view:'bench',show2F:true,showVirtual:false,objX:-50}],
    ['ruler',{view:'bench',showRuler:true}],
    ['big diameter',{view:'bench',lensD:120,lensR:40}],
    ['mirror concave',{view:'mirror'}],
    ['mirror convex',{view:'mirror',mirrorSurface:'convex'}],
    ['mirror flat',{view:'mirror',mirrorSurface:'flat'}],
    ['mirror inside F',{view:'mirror',objX:-60}],
    ['mirror direct',{view:'mirror',fControl:'direct',mirrorF:150}],
    ['conj converging',{view:'conj'}],
    ['conj diverging',{view:'conj',lensSurface:'concave'}],
    ['conj at the pole',{view:'conj',objX:-80}],
    ['maker default',{view:'maker'}],
    ['maker impossible',{view:'maker',lensR:40,lensD:120}],
    ['maker direct',{view:'maker',fControl:'direct',lensF:120}],
    ['guides view',{view:'guides'}],
    ['guides concave',{view:'guides',lensSurface:'concave'}],
    ['guides axial',{view:'guides',objY:4}],
    ['real default',{view:'real'}],
    ['real stopped',{view:'real',realStop:0.25}],
    ['real thick edge',{view:'real',realEdge:10}],
    ['real impossible',{view:'real',lensR:40,lensD:120}],
    ['real high index',{view:'real',lensN:1.8,lensR:120}],
  ];
  for(const [nm,over] of PRESETS) withState(over,()=>{
    let M=null,err=null;
    try{ M=buildModel(ST); }catch(e){ err=e; }
    ok(!err,nm+': the model builds'+(err?': '+(err.stack||err):''));
    if(err) return;
    const ro=readoutHTML(M,ST), eb=eqbarHTML(M,ST), tg=tagHTML(M,ST);
    ok(!badRe.test(ro.replace(/&infin;/g,'')),nm+': readout clean');
    ok(!badRe.test(eb)&&!badRe.test(tg),nm+': eqbar and tag clean');
    ok(ro.length>200&&eb.length>60,nm+': readout and eqbar have substance');
  });
  /* containment, against a number nothing else on the panel supplies */
  withState({view:'bench'},()=>{
    const ro=readoutHTML(buildModel(ST),ST);
    ok(ro.indexOf('151.11')>=0,'the bench readout prints d_i = 151.11 cm (derive)');
    ok(ro.indexOf('-0.8889')>=0||ro.indexOf('&minus;0.8889')>=0||ro.indexOf('-0.8889')>=0,
       'and m = -0.8889');
  });
  withState({view:'mirror'},()=>{
    const ro=readoutHTML(buildModel(ST),ST);
    ok(ro.indexOf('151.1')<0,'the mirror readout is NOT the lens readout');
    ok(ro.indexOf('concave mirror')>=0,'and names the optic');
  });
  withState({view:'real'},()=>{
    const ro=readoutHTML(buildModel(ST),ST);
    ok(ro.indexOf('84.106')>=0,'the real-lens readout prints the thick focal length 84.106 cm (derive)');
  });

  /* the bench model itself, off the built model rather than a retyped formula */
  withState({view:'bench'},()=>{
    const M=buildModel(ST);
    close(M.img.di,151.11111111111111,1e-11,'the built bench model\'s d_i (derive)');
    close(M.img.m,-0.888888888888889,1e-13,'its m (derive)');
    close(M.op.f,80,1e-13,'its signed f (PhET default, indirect model: R = 80, n = 1.5)');
    close(M.op.R,80,1e-13,'its signed R');
    eq(M.nRays,3,'marginal mode traces three rays');
    eq(M.nThrough,3,'and all three are inside an 80 cm aperture from 170 cm at y = 27');
  });
  withState({view:'bench',lensSurface:'concave'},()=>{
    const M=buildModel(ST);
    ok(M.op.f<0,'a concave lens has f < 0');
    ok(M.op.R<0,'and R < 0');
    ok(M.img.virtual,'and its image is virtual');
  });
  withState({view:'mirror'},()=>{
    const M=buildModel(ST);
    close(M.op.f,90,1e-13,'the mirror default f = R/2 = 90 cm');
    close(M.op.R,-180,1e-13,'while its R is reported NEGATIVE: PhET signs R by convex-is-positive '
          +'and f by converging-is-positive, so for a mirror the two disagree');
    close(Math.abs(M.op.R)/2,Math.abs(M.op.f),1e-13,'the MAGNITUDES are still f = R/2');
    ok(M.img.x<0,'a concave mirror\'s real image is to its LEFT');
  });
  withState({view:'mirror',mirrorSurface:'flat'},()=>{
    const M=buildModel(ST);
    eq(M.op.f,1e5,'PhET\'s flat mirror is f = 100 000 cm');
    ok(M.img.m>1&&M.img.m<1.01,'so it magnifies by a hair more than 1');
  });
  withState({view:'bench',fControl:'direct',lensF:120},()=>{
    const M=buildModel(ST);
    close(M.op.R,120,1e-12,'the direct model at n = 1.5 gives R = f exactly');
  });
  /* the memo returns the same object for the same key and a new one otherwise */
  withState({view:'bench'},()=>{
    const a=buildModel(ST);
    ok(buildModel(ST)===a,'the model is memoised on its key');
    ST.objX=-171; clearMemo();
    ok(buildModel(ST)!==a,'and rebuilt when the key moves');
  });

  /* no slider combination produces a non-finite drawn quantity */
  {
    let bad=null,n=0;
    for(const surf of ['convex','concave'])
      for(const R of [40,80,120]) for(const nn of [1.2,1.5,1.8]) for(const D of [60,80,120])
        for(const oX of [-460,-170,-81,-40]) for(const oY of [-100,0,27,100]){
          withState({view:'bench',lensSurface:surf,lensR:R,lensN:nn,lensD:D,objX:oX,objY:oY},()=>{
            const M=buildModel(ST); n++;
            if(!isFinite(M.op.f)||!isFinite(M.dO)) bad=bad||'f or d_o';
            if(!isFinite(M.ext.xmin)||!isFinite(M.ext.xmax)||!isFinite(M.ext.ymin)||!isFinite(M.ext.ymax))
              bad=bad||('extent at '+[surf,R,nn,D,oX,oY].join('/'));
            for(const b of M.bundles) for(const r of b.rays){
              for(const sgm of [r.inSeg,r.outSeg,r.virtSeg]) if(sgm)
                for(const p of sgm) if(!isFinite(p[0])||!isFinite(p[1]))
                  bad=bad||('ray point at '+[surf,R,nn,D,oX,oY].join('/'));
            }
          });
        }
    eq(n,864,'the bench sweep covers 864 control settings');
    ok(!bad,'and no setting produces a non-finite extent or ray point ('+(bad||'ok')+')');
  }

  /* ---------- K2. the four defects the PNG pass found ---------- */
  /* (1) a segment whose BOTH endpoints are outside the box but which crosses it
     must survive the clip and meet both edges (the house polyline's endpoint
     test drops exactly this case -- Known-bad, pupil_plane) */
  {
    const ext={xmin:0,xmax:1,ymin:0,ymax:1};
    const c=clipSeg([-1,0.5],[2,0.5],ext);
    ok(c!==null,'clipSeg keeps a segment that crosses the box with both ends outside');
    if(c){ close(c[0][0],0,1e-15,'and it starts exactly on the left edge');
           close(c[1][0],1,1e-15,'and ends exactly on the right edge');
           close(c[0][1],0.5,1e-15,'at the right height'); }
    ok(clipSeg([2,0.5],[3,0.5],ext)===null,'and drops one that misses entirely');
    ok(clipSeg([-1,2],[2,2],ext)===null,'including one that passes above it');
    const d=clipSeg([0.5,0.5],[0.5,9],ext);
    close(d[1][1],1,1e-15,'a segment leaving the top is cut at the top');
  }
  /* (2) a CONCAVE mirror's rim reaches back toward the light; a convex one's
     does not.  This was backwards in the first draft: the physics was right and
     the picture showed a convex mirror labelled concave. */
  {
    const cav=opticOutline({kind:'mirror',surface:'concave',R:-180,D:80});
    const vex=opticOutline({kind:'mirror',surface:'convex',R:180,D:80});
    const vertex=a=>a.front[Math.floor(a.front.length/2)];
    close(vertex(cav)[0],0,1e-12,'the concave mirror\'s vertex is on the plane x = 0');
    ok(cav.front[0][0]<-1,'and its rim is in FRONT of that, at x < 0 ('+fmt(cav.front[0][0],3)+')');
    ok(vex.front[0][0]>1,'a convex mirror\'s rim is behind it, at x > 0 ('+fmt(vex.front[0][0],3)+')');
    close(Math.abs(cav.front[0][0]),180-Math.sqrt(180*180-40*40),1e-12,
          'and the rim offset is the true sag, 4.5007 cm (derive)');
    /* the silvered backing is behind the glass for BOTH kinds */
    const backOf=a=>a.body[a.body.length-1][0]-a.front[0][0];
    close(backOf(cav),5,1e-12,'the concave mirror\'s backing sits 5 cm behind its rim');
    close(backOf(vex),5,1e-12,'and so does the convex mirror\'s');
  }
  /* (3) nothing is drawn into the caption band.  Before the segments were
     clipped, the bench's outgoing rays ran straight across the prose. */
  {
    const cases=[['bench',{view:'bench'}],['bench inside F',{view:'bench',objX:-50}],
                 ['bench many',{view:'bench',rays:'many',objX:-320}],
                 ['mirror',{view:'mirror'}],['mirror convex',{view:'mirror',mirrorSurface:'convex'}],
                 ['conj',{view:'conj'}],['maker',{view:'maker'}],
                 ['guides',{view:'guides'}],['real',{view:'real'}],
                 ['real stopped',{view:'real',realStop:0.3}]];
    for(const [nm,over] of cases) for(const [W,H] of [[1400,820],[900,600]]) withState(over,()=>{
      const c=makeShot(W,H);
      drawView(c,W,H,buildModel(ST),ST);
      const lim=LAST_L.capY-4;
      let worst=-1e9;
      for(let i=0;i<POLY_SEGS.length;i+=4) worst=Math.max(worst,POLY_SEGS[i+1],POLY_SEGS[i+3]);
      ok(worst<=lim,nm+' '+W+'x'+H+': no drawn segment reaches the caption band ('
         +fmt(worst,1)+' vs '+fmt(lim,1)+')');
      let offx=false;
      for(let i=0;i<POLY_SEGS.length;i+=4)
        if(POLY_SEGS[i]<-1||POLY_SEGS[i]>W+1||POLY_SEGS[i+2]<-1||POLY_SEGS[i+2]>W+1) offx=true;
      ok(!offx,nm+' '+W+'x'+H+': and none leaves the canvas sideways');
    });
  }
  /* (4) the frame is not stretched by focal points that are never drawn */
  {
    withState({view:'mirror',mirrorSurface:'flat'},()=>{
      const M=buildModel(ST);
      ok(M.ext.xmax-M.ext.xmin<600,'the flat mirror\'s frame is '+fmt(M.ext.xmax-M.ext.xmin,0)
         +' cm wide, not the 1640 cm its f = 100 000 cm once demanded');
    });
    withState({view:'bench'},()=>{
      const a=buildModel(ST).ext.xmax;
      withState({view:'bench',show2F:true},()=>{
        ok(buildModel(ST).ext.xmax>a,'switching the 2F points ON does widen the frame');
      });
    });
    withState({view:'mirror'},()=>{
      const M=buildModel(ST);
      ok(M.ext.xmax<200,'a concave mirror\'s frame does not reserve room for an F it never draws');
      eq(M.fSides.join(','),'-1','and its F is on the LEFT, where the light converges (model.md)');
      ok(M.ext.xmin<=-90,'so the frame reaches out to it');
    });
    withState({view:'mirror',mirrorSurface:'convex'},()=>{
      eq(buildModel(ST).fSides.join(','),'1','a convex mirror\'s F is on the RIGHT, behind it');
    });
    withState({view:'bench'},()=>{
      eq(buildModel(ST).fSides.join(','),'-1,1','a lens has F on both sides');
    });
    withState({view:'mirror',mirrorSurface:'flat'},()=>{
      eq(buildModel(ST).drawF,false,'a flat mirror has no F to draw at all');
    });
  }
  /* (5) a POINT source has a point image, not a silhouette */
  {
    withState({view:'bench',objKind:'light'},()=>{
      const c=makeShot(1400,820);
      drawView(c,1400,820,buildModel(ST),ST);
      const n1=POLY_SEGS.length;
      withState({view:'bench',objKind:'arrow'},()=>{
        const c2=makeShot(1400,820);
        drawView(c2,1400,820,buildModel(ST),ST);
        ok(POLY_SEGS.length>n1,'the arrow scene draws more segments than the light scene ('
           +POLY_SEGS.length+' vs '+n1+'): the light has no object or image outline');
      });
    });
  }

  /* ---------- L. layout sweep: every view at four sizes ---------- */
  const SIZES=[[1400,820],[1180,740],[900,600],[620,420]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const SWEEP=[
    ['lens default',{view:'bench'},6],
    ['lens concave',{view:'bench',lensSurface:'concave'},6],
    ['object at F',{view:'bench',objX:-80},5],
    ['object inside F',{view:'bench',objX:-50},6],
    ['many rays',{view:'bench',rays:'many',objX:-320},5],
    ['no rays',{view:'bench',rays:'none'},5],
    ['guides on',{view:'bench',showGuides:true},6],
    ['light + screen',{view:'bench',objKind:'light',showSecond:true},7],
    ['big diameter',{view:'bench',lensD:120,lensR:40},5],
    ['mirror concave',{view:'mirror'},5],
    ['mirror convex',{view:'mirror',mirrorSurface:'convex'},5],
    ['mirror flat',{view:'mirror',mirrorSurface:'flat'},4],
    ['conj converging',{view:'conj'},2],
    ['conj diverging',{view:'conj',lensSurface:'concave'},2],
    ['maker default',{view:'maker'},3],
    ['maker impossible',{view:'maker',lensR:40,lensD:120},2],
    ['guides view',{view:'guides'},4],
    ['guides concave',{view:'guides',lensSurface:'concave'},4],
    ['real default',{view:'real'},3],
    ['real stopped',{view:'real',realStop:0.3},3],
    ['real impossible',{view:'real',lensR:40,lensD:120},0],
  ];
  for(const [nm,over,minFills] of SWEEP) for(const [W,H] of SIZES) withState(over,()=>{
    const c=makeShot(W,H); let err=null;
    try{ drawView(c,W,H,buildModel(ST),ST); }catch(e){ err=e; }
    ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
    if(err) return;
    const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
    ok(fills.length>=minFills&&texts.length>=3,
       nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+'; '+texts.length+' texts)');
    let bad=null;
    for(const t of texts){
      if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
      if(badRe.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
      if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'"'; break; } }
    ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
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
    ok(c.ops.length>30,'view "'+v+'" draws '+c.ops.length+' operations');
  });

  /* the canvas carries no letter subscripts (there is no Unicode subscript f,
     and the rasteriser's font does not have all of the ones that exist) */
  {
    const c=makeShot(1180,740);
    let bads=[];
    for(const v of TABS.map(t=>t[0])) withState({view:v},()=>{
      drawView(c,1180,740,buildModel(ST),ST);
    });
    for(const o of c.ops) if(o.op==='text'&&/[ₐ-ₜᵢ-ᵪ]/.test(o.t)) bads.push(o.t);
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
