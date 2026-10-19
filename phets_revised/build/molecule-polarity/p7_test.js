
/* ================================================================== *
 *  selfTest — headless verification.  REF is refvals.json, the        *
 *  printed output of build/molecule-polarity/derive.py (a Python twin  *
 *  of every formula here, with scipy's adaptive solver beside its      *
 *  RK4), copied in by gen_ref.py.  "(python)" marks a value from that  *
 *  output, "(scipy)" one scipy itself produced, "(exact)" a closed     *
 *  form, "(PhET)" a constant read out of PhET's own build.             *
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
    beginPath(){ pend=null; }, moveTo(){ if(!pend) pend={n:0}; }, lineTo(){ if(!pend) pend={n:0}; },
    closePath(){}, rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle}); },
    stroke(){ ops.push({op:'stroke',style:ctx.strokeStyle}); }, clip(){},
    fillRect(x,y,w,hh){ const c=app(x,y), d=app(x+w,y+hh);
      ops.push({op:'fill',n:1,bb:[Math.min(c[0],d[0]),Math.min(c[1],d[1]),Math.max(c[0],d[0]),Math.max(c[1],d[1])],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke',style:ctx.strokeStyle}); }, clearRect(){},
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
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>{ st2.font=v; }});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>{ st2.align=v; }});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>{ st2.base=v; }});
  ctx.fillStyle='#000'; ctx.strokeStyle='#000'; ctx.lineWidth=1; ctx.lineCap='butt'; ctx.lineJoin='miter';
  ctx.globalAlpha=1;
  return ctx;
}

function selfTest(){
  const T0=Date.now();
  let pass=0, fail=0;
  function ok(c,n){ if(c) pass++; else { fail++; console.log('FAIL — '+n); } }
  function close(a,b,tol,n){ const d=Math.abs(a-b);
    ok(isFinite(d)&&d<=tol,n+'  ('+a+' vs '+b+', |d| '+d+' > '+tol+')'); }
  function rel(a,b,rt,n){ const d=Math.abs(a-b)/Math.max(1e-300,Math.abs(b));
    ok(isFinite(d)&&d<=rt,n+'  ('+a+' vs '+b+', rel '+d+' > '+rt+')'); }
  const stSave=Object.assign({},ST);
  function withState(o,fn){ const s=Object.assign({},ST); Object.assign(ST,o); try{ fn(); } finally{ Object.assign(ST,s); } }
  function resetAll(){ Object.assign(ST,DEFAULTS); fieldReset(); for(const k in MEMO) delete MEMO[k]; }
  resetAll();

  /* ============================ 1. PhET's constants ================= */
  ok(EN_MIN===2&&EN_MAX===4,'(PhET) the electronegativity range is 2 to 4');
  close(EN_STEP,0.2,0,'(PhET) the slider snaps to 0.2');
  ok(ATOM_DIAMETER===100&&BOND_LENGTH===150,'(PhET) ATOM_DIAMETER 100, BOND_LENGTH 150');
  ok(BOND_LENGTH>ATOM_DIAMETER,'(PhET) PhET asserts the bond is longer than an atom is wide');
  close(SURF_MULT,5,0,'(PhET) SURFACE_GRADIENT_WIDTH_MULTIPLIER is 5');
  close(DIPOLE_REF_LEN,135,0,'(PhET) the dipole reference length is 135 px');
  close(BOND_CHAR_BAR,415,0,'(PhET) the bond-character bar is 415 px');
  close(EFIELD_K,0.17,0,'(PhET) the e-field rotation constant is 0.17');
  close(SURF_ALPHA,0.72,0,'(PhET) the surface alpha is 0.72');
  close(DEBYE_PER_EA,0.208194,0,'(PhET) the debye in e.angstrom is 0.208194');
  ok(ROYGB_STOPS.length===35,'(PhET) the rainbow ramp has 35 stops');
  ok(ROYGB_STOPS[0]==='#FF0000'&&ROYGB_STOPS[34]==='#0000FF','(PhET) the rainbow runs red to blue');
  ok(REF.roygbStops.join()===ROYGB_STOPS.join(),'(python) every rainbow stop matches the twin');
  close(snapEN(2.31),2.4,1e-12,'(PhET) 2.31 snaps to 2.4');
  close(snapEN(2.29),2.2,1e-12,'(PhET) 2.29 snaps to 2.2');
  close(snapEN(9),EN_MAX,0,'the snap clamps at the top of the range');
  close(snapEN(-1),EN_MIN,0,'the snap clamps at the bottom of the range');
  close(PAULING.O,3.44,0,'(PhET) Pauling EN of oxygen is 3.44');
  close(PAULING.H,2.20,0,'(PhET) Pauling EN of hydrogen is 2.20');
  close(PAULING.F,3.98,0,'(PhET) Pauling EN of fluorine is 3.98');
  close(VDW_PM.H,120,0,'(PhET) the van der Waals radius of H is 120 pm');
  close(realMol('H2O').radii[0],0.25*152/100,1e-15,'(PhET) the display radius is a quarter of the vdW radius');

  /* ============================ 2. the bond dipole ================== */
  { let worst=0;
    for(let i=0;i<=10;i++) for(let j=0;j<=10;j++) for(let k=0;k<13;k++){
      const e1=EN_MIN+0.2*i, e2=EN_MIN+0.2*j, a=-PI+TAU*k/12;
      const p=bondDipolePhet(e1,e2,a), q=bondDipole(e1,e2,a);
      worst=Math.max(worst,Math.hypot(p[0]-q[0],p[1]-q[1]));
    }
    close(worst,REF.bondDipoleBranchMax,5e-16,'(python) PhET\'s two-branch dipole equals dEN*u over 1573 cases');
    ok(worst<1e-14,'and the two forms agree to machine precision');
  }
  { const d=diatomic(2,3,0), R=REF.diatomicDefault;
    close(d.mumag,R.mumag,1e-15,'(python) the default diatomic |mu|');
    close(d.muang,R.muang,1e-15,'(python) the default diatomic dipole angle');
    close(d.qA,R.qA,1e-15,'(python) q(A) = +dEN');
    close(d.qB,R.qB,1e-15,'(python) q(B) = -dEN');
    close(d.A[0],R.Ax,1e-12,'(python) atom A sits at -BOND_LENGTH/2');
    close(d.B[0],R.Bx,1e-12,'(python) atom B sits at +BOND_LENGTH/2');
    ok(d.qA>0&&d.qB<0,'(exact) the more electronegative atom carries the negative charge');
    close(Math.hypot(d.B[0]-d.A[0],d.B[1]-d.A[1]),BOND_LENGTH,1e-12,'(exact) the drawn bond is BOND_LENGTH long');
  }
  { /* the sign flips with the difference, and vanishes when it is zero */
    close(diatomic(3,2,0).mumag,1,1e-15,'|mu| does not care which way dEN points');
    close(Math.abs(diatomic(3,2,0).muang),PI,1e-15,'but the dipole does: it reverses');
    close(diatomic(3,3,0).mumag,0,0,'(exact) equal electronegativities give no dipole at all');
    close(diatomic(3,3,0).qA,0,0,'(exact) and no partial charge');
  }
  { const t=triatomic(2,3,2,5*PI/6,PI/6,0), R=REF.triatomicDefault;
    close(Math.abs(t.bondAngle)*180/PI,R.bondangleDeg,1e-12,'(python) PhET opens the triatomic at 120 deg');
    close(t.mumag,R.mumag,1e-14,'(python) the default triatomic |mu|');
    close(t.muang,R.muang,1e-14,'(python) the default triatomic dipole angle');
    close(t.qA,R.qA,1e-15,'(python) q(A) on the triatomic');
    close(t.qB,R.qB,1e-15,'(python) q(B) on the triatomic');
    close(t.qC,R.qC,1e-15,'(python) q(C) on the triatomic');
    close(t.muAB[0],R.muABx,1e-14,'(python) the AB bond dipole, x');
    close(t.muAB[1],R.muABy,1e-14,'(python) the AB bond dipole, y');
    close(t.muBC[0],R.muBCx,1e-14,'(python) the BC bond dipole, x');
    close(t.muBC[1],R.muBCy,1e-14,'(python) the BC bond dipole, y');
    close(v3len([t.A[0],t.A[1],0]),BOND_LENGTH,1e-12,'(exact) A sits one bond length from B');
    close(v3len([t.C[0],t.C[1],0]),BOND_LENGTH,1e-12,'(exact) C sits one bond length from B');
  }
  { let worstq=0;
    for(let i=0;i<=10;i++) for(let j=0;j<=10;j++) for(let k=0;k<=10;k++){
      const t=triatomic(EN_MIN+0.2*i,EN_MIN+0.2*j,EN_MIN+0.2*k,5*PI/6,PI/6,0);
      worstq=Math.max(worstq,Math.abs(t.qA+t.qB+t.qC));
    }
    close(worstq,REF.chargeSumMax,0,'(python) the triatomic is neutral over the whole 11^3 grid');
  }

  /* ============================ 3. the vector sum =================== */
  { let worst=0, n=0;
    for(let i=0;i<=10;i+=2) for(let j=0;j<=10;j+=2) for(let k=0;k<=10;k+=2) for(let m=0;m<36;m++){
      const th=PI*(m+0.5)/36;
      const t=triatomic(EN_MIN+0.2*i,EN_MIN+0.2*j,EN_MIN+0.2*k,th,0,0);
      worst=Math.max(worst,Math.abs(mumagClosed(t.dAB,t.dBC,th)-t.mumag)); n++;
    }
    ok(worst<=Math.max(1e-14,REF.closedFormMax*4),
       '(python) the closed form matches the componentwise sum over '+n+' cases ('+worst+')');
  }
  { let worst=0;
    for(let i=0;i<=10;i++) for(let j=0;j<=10;j++)
      worst=Math.max(worst,triatomic(EN_MIN+0.2*i,EN_MIN+0.2*j,EN_MIN+0.2*i,PI,0,0).mumag);
    close(worst,REF.cancelMax,1e-15,'(python) a symmetric triatomic at 180 deg cancels to 7e-16');
    ok(worst<1e-14,'(exact) the cancellation is exact, not merely small');
  }
  { let worst=0;
    for(let i=0;i<=10;i++) for(let j=0;j<=10;j++) for(let m=0;m<=180;m+=5){
      const th=m*PI/180, d=Math.abs((EN_MIN+0.2*j)-(EN_MIN+0.2*i));
      worst=Math.max(worst,Math.abs(2*d*Math.abs(Math.cos(th/2))-triatomic(EN_MIN+0.2*i,EN_MIN+0.2*j,EN_MIN+0.2*i,th,0,0).mumag));
    }
    ok(worst<=Math.max(1e-14,REF.symLawMax*4),'(python) |mu| = 2|dEN| |cos(theta/2)| for the symmetric case ('+worst+')');
  }
  { const R=REF.sumCurve_2_34_2;
    for(const [deg,val] of R){
      const t=triatomic(2,3.4,2,deg*PI/180,0,0);
      close(t.mumag,val,1e-13,'(python) |mu| at theta = '+deg+' deg for EN 2/3.4/2');
    }
  }
  { const t=triatomic(2,3.4,2.6,120*PI/180,0,0), R=REF.asym_2_34_26_120;
    close(t.mumag,R.mumag,1e-13,'(python) the asymmetric |mu| at 120 deg');
    close(mumagClosed(t.dAB,t.dBC,PI),REF.asymMinLaw,1e-14,'(exact) at 180 deg the sum is |dAB + dBC|');
    close(mumagClosed(t.dAB,t.dBC,0),Math.abs(t.dAB-t.dBC),1e-14,'(exact) at 0 deg it is |dAB - dBC|');
    let lo=Infinity;
    for(let m=0;m<=3600;m++) lo=Math.min(lo,mumagClosed(t.dAB,t.dBC,m*PI/1800));
    close(lo,REF.asymMinLaw,1e-12,'(python) and a brute-force scan finds no smaller value');
  }
  { /* rotating the molecule turns the dipole rigidly and leaves the charges alone */
    const a=triatomic(2,3.4,2.6,5*PI/6,PI/6,0), b2=triatomic(2,3.4,2.6,5*PI/6,PI/6,0.7);
    close(b2.mumag,a.mumag,1e-14,'(exact) a rotation does not change |mu|');
    close(normAngle(b2.muang-a.muang,-PI),0.7,1e-14,'(exact) it rotates the dipole by exactly the same angle');
    close(b2.qA,a.qA,0,'(exact) and leaves the partial charges alone');
  }

  /* ============================ 4. the surfaces ===================== */
  close(surfaceWidth(),REF.surfaceWidth,0,'(python) the surface width is 375');
  close(surfaceWidth(),BOND_LENGTH+2*2.25*ATOM_DIAMETER/2,0,'(exact) = bond + 2 x 2.25 r, PhET\'s own form');
  for(const k in REF.gradientWidths){
    const [kind,d]=k.split('_');
    close(gradWidth(kind,parseFloat(d)),REF.gradientWidths[k],1e-10,'(python) gradient width, '+k);
  }
  close(gradWidth('density',2),surfaceWidth(),1e-12,'(exact) at dEN = 2 the density gradient is exactly the surface width');
  close(gradWidth('potential',2),surfaceWidth()/2,1e-12,'(exact) and the potential gradient is half of it');
  close(gradWidth('density',0),surfaceWidth()*SURF_MULT,1e-12,'(exact) at dEN = 0 it is five times the width, so the surface reads neutral');
  { let bad=0, n=0;
    for(const k in REF.surfaceSamples){
      const [kind,d,p]=k.split('|'), c=surfaceColour(kind,parseFloat(d),parseFloat(p)), R=REF.surfaceSamples[k];
      n++;
      for(let i=0;i<3;i++) if(Math.abs(c[i]-R[i])>1e-9) bad++;
    }
    ok(bad===0,'(python) all '+n+' surface gradient samples match the twin ('+bad+' channels off)');
  }
  { const W=surfaceWidth();
    const b2=surfaceColour('potential',2,W/2), a2=surfaceColour('potential',2,-W/2);
    ok(b2[0]>250&&b2[2]<5,'(PhET) the more electronegative end of the potential surface is RED');
    ok(a2[2]>250&&a2[0]<5,'(PhET) and the other end is BLUE');
    const flip=surfaceColour('potential',-2,W/2);
    ok(flip[2]>250&&flip[0]<5,'(exact) reversing dEN swaps the two ends');
    const dB=surfaceColour('density',2,W/2), dA=surfaceColour('density',2,-W/2);
    ok(dB[0]<5&&dA[0]>250,'(PhET) black is MORE electron density, at the electronegative end');
    const g=surfaceColour('density',0,0);
    ok(g[0]===128&&g[1]===128&&g[2]===128,'(PhET) dEN = 0 paints the whole density surface neutral grey');
    let worstMid=0;
    for(let d=-20;d<=20;d++) worstMid=Math.max(worstMid,Math.abs(surfaceColour('potential',d/10,0)[0]-255));
    close(worstMid,REF.potentialMidMax,0,'(python) the potential surface is white at its midpoint for every dEN');
    ok(surfaceColour('potential',0,-W/2)[0]===255,'(PhET) dEN = 0 paints the whole potential surface white');
  }
  { /* the rainbow re-colouring of the same gradient POSITION (a house addition,
       because PhET ships the rainbow only for a surface mesh this file does not
       carry): the RWB path must be untouched, and the ends must still read
       red = negative, blue = positive */
    const W=surfaceWidth(); let worst=0;
    for(let d=-20;d<=20;d++) for(let k=-2;k<=2;k++){
      const a=surfaceColourScheme('potential',d/10,k*W/4,'rwb'), b2=surfaceColour('potential',d/10,k*W/4);
      for(let i=0;i<3;i++) worst=Math.max(worst,Math.abs(a[i]-b2[i]));
    }
    close(worst,0,0,'the rwb scheme is PhET\'s surfaceColour, unchanged');
    const rb=surfaceColourScheme('potential',2,W/2,'roygb'), rl=surfaceColourScheme('potential',2,-W/2,'roygb');
    ok(rb[0]>250&&rb[2]<5,'the rainbow surface is RED at the electronegative end');
    ok(rl[2]>250&&rl[0]<5,'and BLUE at the other');
    const rmid=surfaceColourScheme('potential',2,0,'roygb'), r0=roygb(0);
    close(rmid[0],r0[0],1e-9,'its midpoint is PhET\'s neutral rainbow colour');
    const rf=surfaceColourScheme('potential',-2,W/2,'roygb');
    ok(rf[2]>250&&rf[0]<5,'and reversing dEN swaps the rainbow ends too');
    close(surfacePos('potential',1,0),0.5,1e-15,'(exact) the gradient position is 0.5 at the middle');
    close(surfacePos('potential',0,123),0.5,0,'(exact) and 0.5 everywhere when dEN = 0');
    ok(surfacePos('potential',1,10)>surfacePos('potential',1,-10),'(exact) and it increases along the bond axis');
    /* surfacePos is a FRACTION, and at |dEN| = 2 the potential gradient (187.5)
       is half the surface it is painted across (375), so the raw ratio really
       does leave [0, 1] on the drawn domain: -0.5 at one end, 1.5 at the other.
       Assert the clamp at the limits, past the limits, and over every sample
       drawSurface takes -- against absolute numbers, off the model function. */
    close(surfacePos('potential',2,-W/2),0,0,'(exact) the position is exactly 0 at the low end');
    close(surfacePos('potential',2,W/2),1,0,'(exact) and exactly 1 at the high end');
    close(surfacePos('potential',2,-1e6),0,0,'(exact) and it is clamped, not extrapolated, far below');
    close(surfacePos('potential',2,1e6),1,0,'(exact) and far above');
    close(surfacePos('density',-2,-1e6),0,0,'(exact) the density surface clamps the same way');
    close(surfacePos('density',-2,1e6),1,0,'(exact) at both ends');
    { const R2=2.25*ATOM_DIAMETER/2, xa=-BOND_LENGTH/2-R2, xb=BOND_LENGTH/2+R2;
      const rawPos=(kind,dEN,p)=>dEN===0?0.5:(p+gradWidth(kind,dEN)/2)/gradWidth(kind,dEN);
      let lo=Infinity, hi=-Infinity, rlo=Infinity, rhi=-Infinity, nOut=0, nTot=0, worstCol=0;
      for(let d=-20;d<=20;d++) for(let k=0;k<=400;k++){
        const dEN=d/10, p=xa+(xb-xa)*k/400, v=surfacePos('potential',dEN,p), r=rawPos('potential',dEN,p);
        lo=Math.min(lo,v); hi=Math.max(hi,v); rlo=Math.min(rlo,r); rhi=Math.max(rhi,r);
        nTot++; if(r<0||r>1) nOut++;
        /* the clamp is redundant for the PICTURE, because PhET's own roygb()
           clamps (8e+1)/2 downstream.  That is why breaking it is invisible to
           any colour check, so the invariance is asserted DELIBERATELY here
           rather than left as a blind spot (Known-bad: a quantity every
           observable is invariant to cannot be reached through those
           observables). */
        const a2=surfaceColourScheme('potential',dEN,p,'roygb');
        const b3=roygb((0.5-(dEN>0?r:1-r))/4);
        for(let i=0;i<3;i++) worstCol=Math.max(worstCol,Math.abs(a2[i]-b3[i]));
      }
      ok(lo===0&&hi===1,'the clamped position spans exactly [0, 1] over the drawn domain ('+lo+' .. '+hi+')');
      close(rlo,-0.5,1e-12,'(exact) and the UNCLAMPED ratio reaches -0.5 there, so the clamp is load-bearing');
      close(rhi,1.5,1e-12,'(exact) and 1.5 at the other end');
      ok(nOut===660&&nTot===16441,'660 of '+nTot+' samples are outside [0, 1] without it (got '+nOut+')');
      close(worstCol,0,0,'but the drawn rainbow colour is INVARIANT to the clamp: PhET\'s roygb clamps downstream');
    }
    ok(surfaceColourScheme('density',2,0,'roygb')[0]===surfaceColour('density',2,0)[0],
       'the rainbow scheme never touches the electron-density surface');
  }
  { let bad=0;
    for(const k in REF.roygbSamples){ const c=roygb(parseFloat(k)), R=REF.roygbSamples[k];
      for(let i=0;i<3;i++) if(Math.abs(c[i]-R[i])>1e-9) bad++; }
    ok(bad===0,'(python) PhET\'s rainbow mapping matches the twin at seven potentials');
    const lo=roygb(-1), hi=roygb(1);
    ok(lo[0]===255&&lo[2]===0,'(PhET) a very negative potential is red');
    ok(hi[2]===255&&hi[0]===0,'(PhET) a very positive one is blue');
  }

  /* ============================ 5. bond character =================== */
  for(const k in REF.bondCharacter)
    ok(bondCharacter(parseFloat(k))===REF.bondCharacter[k],'(python) bond character at dEN = '+k);
  ok(bondCharacter(0.404)===REF.bondCharacterRounding[0]&&bondCharacter(0.405)===REF.bondCharacterRounding[1],
     '(PhET) |dEN| is rounded to 2 dp BEFORE the band is chosen');
  ok(bondCharacter(-1.5)===bondCharacter(1.5),'(exact) bond character depends on |dEN| only');
  for(const k in REF.dipolePx) close(dipolePx(parseFloat(k)),REF.dipolePx[k],1e-12,'(python) arrow length at |mu| = '+k);
  close(dipolePx(EN_SPAN),DIPOLE_REF_LEN,0,'(PhET) |mu| = 2 draws PhET\'s reference 135 px');
  close(dipolePx(0),0,0,'(exact) no dipole draws no arrow');
  ok(polarityOf(0)==='nonpolar'&&polarityOf(0.5)==='weakly polar'&&polarityOf(1.2)==='polar'&&polarityOf(2)==='moderately polar','(PhET) the six molecular-polarity bands');

  /* ============================ 6. the field ======================== */
  for(const mu of [0.4,1,2]){
    close(phetFieldStep(mu),REF['phetStepSize_'+mu.toFixed(1)],1e-15,'(python) PhET\'s step per frame at |mu| = '+mu);
    let p=normAngle(150*PI/180), n=0;
    while(p!==0&&n<100000){ p=phetAdvance(p,mu); n++; }
    ok(n===REF['phetSteps_'+mu.toFixed(1)],'(python) PhET takes '+REF['phetSteps_'+mu.toFixed(1)]+' frames from 150 deg at |mu| = '+mu+' (got '+n+')');
  }
  { let p=normAngle(210*PI/180); const first=phetAdvance(p,2);
    ok((first>p?1:-1)===REF.phetDir_210,'(python) from 210 deg PhET goes the SHORT way (psi increases)');
    let n=0; while(p!==0&&n<100000){ p=phetAdvance(p,2); n++; }
    ok(n===REF.phetSteps_210,'(python) and arrives in '+REF.phetSteps_210+' frames');
  }
  close(phetFieldStep(0),0,0,'(exact) with no dipole PhET\'s rule does not move the molecule');
  { const muE=1;
    close(rotorOmega0(muE),REF.rotorOmega0,1e-14,'(python) omega_0 = sqrt(muE/I)');
    close(2*Math.sqrt(ROTOR_I*muE),REF.rotorBcrit,1e-14,'(python) the critical damping');
    close(rotorB(1,muE),REF.rotorBcrit,1e-14,'(exact) zeta = 1 IS the critical damping');
    for(const z of ['0.2','0.7','1.0','2.0']){
      const R=REF.rotorTraces[z], b=rotorB(parseFloat(z),muE);
      close(b,R.b,1e-14,'(python) b at zeta = '+z);
      const tr=rotorRun(150*PI/180,0,muE,b,0.002,15000);
      close(tr[tr.length-1][1],R.psiEnd,1e-9,'(python) psi(30 s) at zeta = '+z);
      close(tr[500][1],R.psi_at_1s,1e-10,'(python) psi(1 s) at zeta = '+z);
      close(tr[1500][1],R.psi_at_3s,1e-10,'(python) psi(3 s) at zeta = '+z);
      /* the energy is a Lyapunov function: it can only fall */
      let rise=0, E0=rotorEnergy(tr[0][1],tr[0][2],muE);
      for(let i=1;i<tr.length;i++){ const E=rotorEnergy(tr[i][1],tr[i][2],muE); rise=Math.max(rise,E-E0); E0=E; }
      ok(rise<1e-12,'(exact) the rotor energy never rises at zeta = '+z+' ('+rise+')');
      let cross=0; for(let i=1;i<tr.length;i++) if(tr[i-1][1]*tr[i][1]<0) cross++;
      ok(cross===REF['rotorCrossings_'+z],'(python) zero crossings at zeta = '+z+': '+cross+' vs '+REF['rotorCrossings_'+z]);
      ok(parseFloat(z)<1?cross>0:cross===0,'(exact) only an under-damped rotor overshoots (zeta = '+z+')');
    }
    { const tr=rotorRun(PI,0,muE,2,0.002,2000);
      close(tr[tr.length-1][1]-PI,REF.rotorUnstable,1e-14,'(python) psi = pi is an equilibrium: nothing moves');
      const tr2=rotorRun(PI-1e-3,0,muE,2,0.002,15000);
      close(tr2[tr2.length-1][1],REF.rotorNearUnstable,1e-9,'(python) a thousandth of a radian off it, the rotor falls to psi = 0');
      ok(Math.abs(tr2[tr2.length-1][1])<1e-3,'(exact) the unstable equilibrium is unstable');
    }
    if(REF['rotorScipy_0.2']){
      for(const z of ['0.2','1.0']){
        const R=REF['rotorScipy_'+z]; if(!R) continue;
        const tr=rotorRun(150*PI/180,0,muE,rotorB(parseFloat(z),muE),0.002,1500);
        close(tr[tr.length-1][1],R.scipy,4e-11,'(scipy) the RK4 matches scipy\'s adaptive solver at t = 3 s, zeta '+z);
      }
    }
    { const R=REF.rotorLinear, z=0.2, b=rotorB(z,muE), w0=rotorOmega0(muE);
      const wd=w0*Math.sqrt(1-z*z);
      close(wd,R.wd,1e-14,'(python) the damped frequency omega_d');
      const tr=rotorRun(1e-4,0,muE,b,0.0005,4000);
      const num=[tr[1000][1],tr[2000][1],tr[4000][1]];
      for(let i=0;i<3;i++) rel(num[i],R.num[i],1e-9,'(python) the small-angle orbit at t = '+[0.5,1,2][i]+' s');
      for(let i=0;i<3;i++) rel(num[i],R.lin[i],2e-8,'(exact) and it reproduces the linearised solution there');
    }
  }
  { /* the live field: the sim's own stepper reaches PhET's equilibrium */
    withState({view:'two',enA:2,enB:4,field:true,fieldMode:'rotor',fieldE:1,zeta:0.7},()=>{
      fieldReset(); setFieldPsi(150*PI/180);
      close(fieldPsi(),150*PI/180,1e-12,'setFieldPsi/fieldPsi round-trip');
      let n=0; while(!FIELD.idle&&n<40000){ fieldStep(1/60); n++; }
      ok(FIELD.idle&&n<40000,'the rotor reaches alignment from 150 deg ('+n+' frames)');
      close(fieldPsi(),0,1e-6,'and the dipole ends pointing at the positive plate');
      close(FIELD.w,0,1e-6,'with no angular velocity left');
    });
    withState({view:'two',enA:2,enB:4,field:true,fieldMode:'phet'},()=>{
      fieldReset(); setFieldPsi(150*PI/180);
      let n=0; while(!FIELD.idle&&n<40000){ fieldStep(1/60); n++; }
      ok(FIELD.idle,'PhET\'s rule also reaches alignment');
      close(fieldPsi(),0,1e-12,'and lands exactly on zero, as PhET clamps it');
      ok(n<=REF['phetSteps_2.0']+2,'in PhET\'s own frame count ('+n+' vs '+REF['phetSteps_2.0']+')');
    });
    withState({view:'two',enA:3,enB:3,field:true,fieldMode:'rotor'},()=>{
      fieldReset();
      ok(fieldStep(1/60)===false,'with no dipole nothing turns');
    });
    withState({view:'three',enA:2,enB:3,enC:2,angAB:PI,angBC:0,field:true,fieldMode:'rotor'},()=>{
      fieldReset();
      ok(fieldStep(1/60)===false,'and a linear symmetric triatomic, whose dipole is exactly zero, does not turn either');
    });
  }
  { /* the field-view traces agree with the standalone integrator */
    withState({view:'field',enA:2,enB:4,enC:2,fieldE:1,zeta:0.7,psi0:150},()=>{
      for(const k in MEMO) delete MEMO[k];
      const M=buildModel();
      close(M.omega0,Math.sqrt(M.muE/ROTOR_I),1e-14,'the field view quotes omega_0 from the model');
      ok(M.settle!==null&&M.settle>0,'and a finite settling time ('+M.settle+')');
      const tr=M.traces.live;
      ok(Math.abs(tr.ys[tr.ys.length-1])<0.5,'the live trace has arrived by the end of the window');
      ok(M.traces.phet.ys.length===Math.round(FV.T*60)+1,'PhET\'s staircase is sampled at 60 fps');
    });
  }

  /* ============================ 7. the real molecules =============== */
  ok(MOLORDER.length===19,'(PhET) nineteen real molecules');
  { let bad=0;
    for(const s of MOLORDER){
      const r=realMol(s), R=REF.realDerived[s];
      if(Math.abs(r.psi4mag-R.psi4mag)>1e-12) bad++;
      close(r.psi4mag,R.psi4mag,1e-12,'(python) |mu| Psi4, '+s);
      close(r.sumBasicMag,R.basic,1e-12,'(python) the basic vector sum, '+s);
      close(r.sumAdvMag,R.adv,1e-12,'(python) the advanced vector sum, '+s);
      rel(r.arrowScaleAdv,R.scale,1e-8,'(python) PhET\'s arrow scale, '+s);
      for(let i=0;i<R.lengths.length;i++) close(r.lengths[i],R.lengths[i],1e-12,'(python) bond length '+i+', '+s);
    }
    ok(bad===0,'every molecule\'s Psi4 magnitude matches the twin');
  }
  { let worst=0;
    for(const s of MOLORDER) worst=Math.max(worst,Math.abs(realMol(s).q.reduce((a,b2)=>a+b2,0)));
    close(worst,REF.hirshfeldSumMax,1e-12,'(python) the Hirshfeld charges sum to zero on every molecule');
  }
  for(const s in REF.realAngles){
    const a=realMol(s).angles, R=REF.realAngles[s];
    ok(a.length===R.length,'(python) '+s+' has '+R.length+' bond angles at its central atom');
    for(let i=0;i<Math.min(a.length,R.length);i++) close(a[i],R[i],1e-5,'(python) '+s+' angle '+i);
  }
  { const R=REF.realAngleGaps;
    for(const s in R){
      const a=realMol(s).angles;
      const near=a.reduce((p,c)=>Math.abs(c-R[s].known)<Math.abs(p-R[s].known)?c:p,a[0]);
      close(near-R[s].known,R[s].diff,1e-5,'(python) PhET\'s stored '+R[s].name+' minus the reference value, '+s);
    }
    ok(Math.abs(R.NH3.diff)>10,'(CCCBDB) PhET\'s stored ammonia angle is more than 10 deg too narrow');
    ok(Math.abs(R.H2O.diff)>6,'(CCCBDB) and its water angle more than 6 deg too narrow');
    ok(Math.abs(R.CH4.diff)<0.01&&Math.abs(R.CO2.diff)<1e-9,'(exact) while the symmetric ones are right to the last digit');
  }
  { const R=REF.waterDetail, w=realMol('H2O');
    close(w.lengths[0],R.bondLength,1e-12,'(python) the O-H bond length PhET stores');
    close(w.angles[0],R.angleDeg,1e-9,'(python) and the H-O-H angle it implies');
    close(w.q[0],R.qO,1e-12,'(python) the Hirshfeld charge on oxygen');
    close(v3len(w.bondDipolesAdv[0]),R.bondDipoleAdv,1e-12,'(python) water\'s advanced bond dipole, debye');
    close(w.sumAdvMag,R.sumAdv,1e-12,'(python) their vector sum');
    close(R.law,2*R.bondDipoleAdv*Math.cos(R.angleDeg*PI/360),1e-9,'(exact) which is 2 mu cos(theta/2) to 1e-9');
    ok(R.psi4>R.sumAdv,'(python) and Psi4\'s own dipole is larger than the bond-dipole sum, which is why PhET rescales the arrows');
  }
  { const R=REF.symmetricSumAdv;
    for(const s in R) close(realMol(s).sumAdvMag,R[s],1e-12,'(python) the symmetric set cancels, '+s);
    let worst=0; for(const s in R) worst=Math.max(worst,realMol(s).sumAdvMag);
    ok(worst<2e-3,'(exact) every symmetric molecule\'s bond dipoles cancel to better than 0.002 D');
    ok(realMol('O3').sumBasicMag===0,'(exact) ozone has dEN = 0 on both bonds, so basic mode calls it non-polar');
  }
  { /* WHERE the molecular dipole points, in 3-D, so this is a statement about
       the model and not about the camera: toward the electron-rich end. */
    const dotv=(a,b2)=>a[0]*b2[0]+a[1]*b2[1]+a[2]*b2[2];
    for(const sy of ['H2O','NH3','HF','CH3F','HCN','CH2O']){
      const r=realMol(sy);
      let lo=0; for(let i=1;i<r.q.length;i++) if(r.q[i]<r.q[lo]) lo=i;
      const u=v3sub(r.pos[lo],r.centroid), nu=v3len(u);
      const d=dotv(r.sumAdv,v3scale(u,1/Math.max(1e-12,nu)));
      ok(d>0.2*r.sumAdvMag,'(exact) '+sy+'\'s molecular dipole points at its most negative atom ('+r.syms[lo]+', '+d+')');
    }
    { const r=realMol('CHCl3'), h=r.syms.indexOf('H'), c=r.centre;
      const u=v3sub(r.pos[h],r.pos[c]);
      const d=dotv(r.sumAdv,v3scale(u,1/v3len(u)));
      ok(d<-0.5*r.sumAdvMag,'(exact) chloroform\'s dipole runs from the H toward the three chlorines ('+d+')'); }
    { const r=realMol('H2O'), d=dotv(r.sumAdv,r.meanBond);
      ok(d<0,'(exact) and water\'s points away from its hydrogens ('+d+')'); }
  }
  { const d=realDipoles('H2O',true), db=realDipoles('H2O',false);
    close(d.scale,realMol('H2O').arrowScaleAdv,0,'the advanced arrow scale comes off the model');
    close(db.scale,0.75,0,'(PhET) the basic arrow scale is 0.75');
    ok(d.bd.length===2&&db.bd.length===2,'water has two bond dipoles in both modes');
    ok(d.unit==='D','and advanced mode is in debye');
  }

  /* ============================ 8. the atlas ======================== */
  { const R=REF.measured;
    for(const s in R){
      const m=measuredOf(s);
      ok(m!==null,'(CCCBDB) a measured value for '+s);
      if(m){ close(m[0],R[s][0],0,'(CCCBDB) the measured |mu| of '+s); ok(m[1]===R[s][1],'(CCCBDB) and its source code for '+s); }
    }
    ok(measuredOf('BH3')===null,'(CCCBDB) borane is absent from the table, and is not faked as zero');
    const st2=atlasStats();
    close(st2.mae,REF.atlasMAE,1e-12,'(python) the mean |Psi4 - measured|');
    close(Math.abs(st2.worst.diff),REF.atlasWorst,1e-12,'(python) the worst molecule\'s difference');
    ok(st2.n===18,'18 of the 19 molecules have a measured value');
    ok(st2.zero.join()===REF.zeroSet.join(),'(python) the non-polar set is exactly '+REF.zeroSet.join(', '));
    ok(st2.zero.length===9,'nine molecules are non-polar');
  }
  { /* Spearman, implemented here and pinned against the twin's own ranking */
    const polar=REF.polarSet;
    const sp=(xs,ys)=>{
      const rank=v=>{ const o=v.map((x,i)=>i).sort((a,b2)=>v[a]-v[b2]), r=new Array(v.length);
        let i=0; while(i<o.length){ let j=i; while(j+1<o.length&&v[o[j+1]]===v[o[i]]) j++;
          const av=(i+j)/2+1; for(let k=i;k<=j;k++) r[o[k]]=av; i=j+1; } return r; };
      const rx=rank(xs), ry=rank(ys), n=xs.length;
      const mx=rx.reduce((a,b2)=>a+b2,0)/n, my=ry.reduce((a,b2)=>a+b2,0)/n;
      let num=0, dx=0, dy=0;
      for(let i=0;i<n;i++){ num+=(rx[i]-mx)*(ry[i]-my); dx+=(rx[i]-mx)**2; dy+=(ry[i]-my)**2; }
      return num/Math.sqrt(dx*dy);
    };
    const ys=polar.map(s=>measuredOf(s)[0]);
    close(sp(polar.map(s=>realMol(s).sumBasicMag),ys),REF.spearmanBasic,1e-12,'(python) the basic model\'s rank correlation');
    close(sp(polar.map(s=>realMol(s).psi4mag),ys),REF.spearmanAdv,1e-12,'(python) and the quantum column\'s');
    ok(REF.spearmanAdv>REF.spearmanBasic,'(python) the quantum column orders the polar molecules far better');
  }

  /* ============================ 9. the UI model ===================== */
  { withState({angAB:5*PI/6,angBC:PI/6},()=>{
      for(const d of [0,30,104.5,120,179.5,180]){
        setBondAngleDeg(d);
        close(Math.abs(normAngle(ST.angAB-ST.angBC,-PI))*180/PI,d===180?180:d,1e-9,'setBondAngleDeg round-trips at '+d);
      }
    });
    withState({dipoleDir:'negpos'},()=>{
      const m=diatomic(2,4,0), s=shownDipole(m.mu);
      close(Math.abs(vang(s)),PI,1e-12,'(PhET) the negative-to-positive preference reverses every arrow');
      close(vmag(s),m.mumag,1e-15,'and changes nothing about its length');
    });
  }

  /* ============================ 10. the drawings ==================== */
  const SIZES=[[1100,712],[1440,860],[860,620]];
  const CONFIGS=[
    ['two default',{view:'two'},50],
    ['two max dEN + surface',{view:'two',enA:2,enB:4,surface:'potential',showCharges:true},180],
    ['two density surface',{view:'two',enA:4,enB:2,surface:'density',showCharges:true},180],
    ['two zero dEN',{view:'two',enA:3,enB:3,surface:'potential',showCharges:true},180],
    ['two field on',{view:'two',enA:2,enB:3.4,field:true,showCharges:true,showBondChar:true},70],
    ['two rainbow key',{view:'two',enA:2,enB:3.2,surface:'potential',surfColor:'roygb'},180],
    ['three default',{view:'three'},26],
    ['three linear',{view:'three',angAB:PI,angBC:0,showCharges:true},26],
    ['three asymmetric',{view:'three',enA:2,enB:3.4,enC:2.6,showCharges:true,showMolDipole:true},28],
    ['three field',{view:'three',field:true,enB:4},40],
    ['real water basic',{view:'real',mol:'H2O',realMode:'basic'},30],
    ['real water advanced',{view:'real',mol:'H2O',realMode:'advanced',showCharges:true},32],
    ['real CO2',{view:'real',mol:'CO2',realMode:'advanced',showCharges:true},36],
    ['real borane',{view:'real',mol:'BH3',realMode:'advanced'},36],
    ['real chloroform',{view:'real',mol:'CHCl3',realMode:'advanced',showCharges:true},50],
    ['sum default',{view:'sum'},50],
    ['sum asymmetric',{view:'sum',enC:2.6},48],
    ['sum flat',{view:'sum',enA:3,enB:3,enC:3},48],
    ['field default',{view:'field'},52],
    ['field underdamped',{view:'field',zeta:0.2,psi0:-150},58],
    ['field no dipole',{view:'field',enA:3,enB:3,enC:3},48],
    ['atlas',{view:'atlas'},130],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,minOps] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      for(const k in MEMO) delete MEMO[k];
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(c.ops.length>=minOps&&texts.length>=1&&fills.length>=1,
         nm+' '+W+'x'+H+' draws substance ('+c.ops.length+' ops, '+fills.length+' fills, '+texts.length+' texts; floor '+minOps+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'
        +(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b2=texts[j2].bb;
        const ox=Math.min(a[2],b2[2])-Math.max(a[0],b2[0]), oy=Math.min(a[3],b2[3])-Math.max(a[1],b2[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      const nanc=fills.filter(f=>f.style&&/NaN/.test(f.style));
      ok(!nanc.length,nm+' '+W+'x'+H+' no NaN colours');
    });
  }
  /* the panels build clean for every view and every preset */
  { let bad=null;
    for(const [v] of TABS) for(const mol of MOLORDER) for(const mode of ['basic','advanced']){
      withState({view:v,mol,realMode:mode},()=>{
        const M=buildModel();
        for(const s of [readoutHTML(M),eqbarHTML(M),tagHTML(M)])
          if(/NaN|undefined|Infinity/.test(s)) bad=bad||(v+'/'+mol+'/'+mode+': '+s.slice(0,60));
      });
    }
    ok(!bad,'every view x molecule x mode builds a clean readout, eqbar and tag ('+(bad||'ok')+')');
  }
  { let bad=null;
    for(let a=EN_MIN;a<=EN_MAX+1e-9;a+=0.2) for(let b2=EN_MIN;b2<=EN_MAX+1e-9;b2+=0.2)
      for(const deg of [0,45,90,120,180]){
        withState({view:'three',enA:a,enB:b2,enC:a,angAB:deg*PI/180,angBC:0},()=>{
          const M=buildModel();
          if(!isFinite(M.m.mumag)||!isFinite(M.closed)||!isFinite(M.m.qB)) bad=bad||(a+'/'+b2+'/'+deg);
        });
      }
    ok(!bad,'no electronegativity and angle combination gives a non-finite value ('+(bad||'ok')+')');
  }
  { /* the bond-character bar never runs past its ends */
    let bad=null;
    for(let a=EN_MIN;a<=EN_MAX+1e-9;a+=0.2) for(let b2=EN_MIN;b2<=EN_MAX+1e-9;b2+=0.2){
      const f=Math.abs(b2-a)/EN_SPAN; if(f<0||f>1+1e-12) bad=a+'/'+b2;
    }
    ok(!bad,'the bond-character pointer stays on its bar');
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
