
/* ================================================================== *
 *  selfTest — headless verification.  REF is refvals.json, the        *
 *  printed output of build/molecule-shapes/derive.py (a Python twin   *
 *  of every function, scipy BFGS, Horn against scipy's align_vectors, *
 *  a Hessian audit), copied by gen_ref.py.  "(python)" marks a value  *
 *  from that output; "(exact)" a closed form.                         *
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
    beginPath(){ pend=null; }, moveTo(){ if(!pend) pend={n:0}; }, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle}); },
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
  const ANG=(U,idx)=>{ const out=[]; for(let a=0;a<idx.length;a++) for(let b=a+1;b<idx.length;b++) out.push(angleDeg(U[idx[a]],U[idx[b]])); return out.sort((p,q)=>p-q); };
  const range=(a,b)=>{ const o=[]; for(let i=a;i<b;i++) o.push(i); return o; };
  const maxDiff=(A,B)=>{ if(A.length!==B.length) return Infinity; let m=0; for(let i=0;i<A.length;i++) m=Math.max(m,Math.abs(A[i]-B[i])); return m; };
  function resetAll(){ liveInit(); LIVE.realBlend=0; RELAX.seed=0; RELAX.key=''; }
  /* a configuration: plain keys go into ST; _keys drive the live molecule and the runs */
  function withState(over,fn){
    const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    Object.assign(ST,DEFAULTS,clean); resetAll();
    if(over._empty) liveRemoveAll();
    if(over._load) liveLoad(over._load[0],over._load[1]);
    if(over._add) for(const o of over._add) liveAdd(o);
    if(over._settle!==false) liveSettle();
    if(over._blend!==undefined) LIVE.realBlend=over._blend;
    if(over._seed!==undefined) RELAX.seed=over._seed;
    if(over._run!==undefined){ relaxEnsure(); if(over._run==='all') relaxRun(); else for(let k=0;k<over._run;k++) relaxAdvance(1); }
    try{ return fn(); } finally{ Object.assign(ST,stSave); resetAll(); }
  }

  /* ---------- A. constants, the ideal geometries, the energy ---------- */
  close(90*DEG,Math.PI/2,1e-15,'DEG converts degrees INTO radians (exact)');
  close(RAD*Math.PI,180,1e-12,'RAD converts radians into degrees (exact)');
  close(TET,REF.ideal.tet_deg,1e-12,'the tetrahedral angle arccos(-1/3) (python)');
  close(TET,109.47122063449069,1e-12,'= 109.4712206345° (exact)');
  eq(RHO_PHET,0.7,"PhET's lone pairs at 7 against bonds at 10");
  eq(MAXG,6,"PhET's maxConnections"); eq(EXPN,2,'the pair energy is 1/d²');
  const IDEAL={2:[180],3:[120,120,120],4:[TET,TET,TET,TET,TET,TET],5:[90,90,90,90,90,90,120,120,120,180],6:[90,90,90,90,90,90,90,90,90,90,90,90,180,180,180]};
  const EXACTE={2:1/4,3:1,4:9/4,5:17/4,6:27/4};
  for(let n=1;n<=6;n++){ let um=0; for(const u of SLOTS[n]) um=Math.max(um,Math.abs(Math.sqrt(vdot(u,u))-1)); ok(um<1e-15,'slot vectors of '+n+' are unit ('+um.toExponential(1)+')'); }
  for(let n=2;n<=6;n++){
    close(maxDiff(ANG(SLOTS[n],range(0,n)),IDEAL[n]),0,1e-12,'the ideal angles of '+n+' slots (exact)');
    const ones=SLOTS[n].map(()=>1);
    close(energyOf(SLOTS[n],ones),REF.ideal['E'+n],1e-12,'U of '+n+' equal pairs at the slots (python)');
    close(energyOf(SLOTS[n],ones),EXACTE[n],1e-12,'= '+EXACTE[n]+' (exact: sum of 1/(2-2cos t))');
    close(energyOf(SLOTS[n],ones,1),REF.ideal['E'+n+'_coulomb'],1e-12,'the Coulomb 1/d energy of '+n+' (python)');
  }
  close(energyOf([[1,0,0],[0,1,0]],[1,1]),REF.pins.E_two_90,1e-15,'two pairs at 90°: U = 1/2 (python)');
  close(energyOf([[1,0,0],[0,1,0]],[0.7,1]),1/1.49,1e-15,'a lone pair at rho 0.7 and a bond at 90°: U = 1/1.49 (exact)');
  close(energyOf([[1,0,0],[0,1,0]],[0.7,1]),REF.pins.E_two_90_rho,1e-15,'(python)');
  close(energyOf([[0,0,1],[0,0,1]],[0.7,1]),1/0.09,1e-12,'a lone pair under a bond: d = 0.3, U = 1/0.09 (exact)');
  { /* the gradient against a central difference (unnormalised coordinates) */
    const rnd=mulberry32(5), U=randomDirs(rnd,5), R=[0.7,0.7,1,1,1], G=gradOf(U,R); let err=0;
    for(let i=0;i<5;i++) for(let k=0;k<3;k++){ const Up=U.map(u=>u.slice()), Um=U.map(u=>u.slice()); Up[i][k]+=1e-6; Um[i][k]-=1e-6;
      err=Math.max(err,Math.abs((energyOf(Up,R)-energyOf(Um,R))/2e-6-G[i][k])); }
    ok(err<2e-6,'the gradient matches a central difference ('+err.toExponential(2)+')');
    const G1=gradOf(U,R,1); let err1=0;
    for(let i=0;i<5;i++) for(let k=0;k<3;k++){ const Up=U.map(u=>u.slice()), Um=U.map(u=>u.slice()); Up[i][k]+=1e-6; Um[i][k]-=1e-6;
      err1=Math.max(err1,Math.abs((energyOf(Up,R,1)-energyOf(Um,R,1))/2e-6-G1[i][k])); }
    ok(err1<2e-6,'and for the exponent 1 ('+err1.toExponential(2)+')');
    const Gt=tangentOf(U,G); let tm=0; Gt.forEach((g,i)=>{ tm=Math.max(tm,Math.abs(vdot(g,U[i]))); });
    ok(tm<1e-12,'the tangential part is perpendicular to u ('+tm.toExponential(1)+')');
  }

  /* ---------- B. every class, the GD twin against derive ---------- */
  for(const rs of ['0.70','0.85','1.00']){ const rho=parseFloat(rs);
    for(const key in REF.eq[rs]){ const m=/AX(\d)E(\d)/.exec(key), x=+m[1], e=+m[2], R=REF.eq[rs][key];
      const E=equilibrium(x,e,rho);
      close(E.E,R.E,1e-11*Math.max(1,R.E),key+' at rho '+rs+': U (python)');
      close(maxDiff(ANG(E.U,range(e,x+e)),R.bb),0,1e-8,key+' at rho '+rs+': bond angles (python)');
      const lb=[]; for(let i=0;i<e;i++) for(let j=e;j<x+e;j++) lb.push(angleDeg(E.U[i],E.U[j])); lb.sort((p,q)=>p-q);
      close(maxDiff(lb,R.lb),0,1e-8,key+' at rho '+rs+': lone pair-bond angles (python)');
      close(maxDiff(ANG(E.U,range(0,e)),R.ll),0,1e-8,key+' at rho '+rs+': lone pair-lone pair angles (python)');
      ok(Math.abs(E.it-R.it)<=3,key+' at rho '+rs+': '+E.it+' steps, the twin took '+R.it);
      ok(E.gmax<GTOL,key+' converged ('+E.gmax.toExponential(1)+')');
    }
  }
  ok(ETA*REF.gd.lam_max<2,'the fixed step is stable: eta lambda_max = '+fmt(ETA*REF.gd.lam_max,3)+' < 2 (python)');

  /* ---------- C. random starts: plain descent lands on the ideal shape ---------- */
  { const r0=mulberry32(20260918); REF.prng.first4.forEach((v,i)=>close(r0(),v,0,'mulberry32(20260918) draw '+i+' (python)')); }
  for(const r of REF.random){
    const U0=randomDirs(mulberry32(r.seed),r.n);
    close(maxDiff(U0[0],r.U0),0,1e-15,'random start '+r.seed+' (N = '+r.n+') is the twin\'s');
    const q=relax(U0,U0.map(()=>1));
    close(maxDiff(ANG(q.U,range(0,r.n)),IDEAL[r.n]),0,1e-8,'N = '+r.n+', seed '+r.seed+': the ideal shape from a random start (exact)');
    close(q.E,EXACTE[r.n],1e-12,'N = '+r.n+', seed '+r.seed+': U reaches its closed form (exact)');
    ok(Math.abs(q.it-r.it)<=3,'N = '+r.n+', seed '+r.seed+': '+q.it+' steps, the twin took '+r.it);
  }

  /* ---------- D. the named angles, the directions, rho = 1 ---------- */
  for(const rs of ['0.70','0.85','1.00']) for(const k in REF.named[rs]) close(namedAngle(k,parseFloat(rs)),REF.named[rs][k],1e-8,k+' at rho '+rs+' (python)');
  /* the ideal each named angle is measured against must be that pair of slots' own
     angle -- nothing else pins it, and only the squeeze view would ever show it wrong */
  for(const k in NAMED){ const x=NAMED[k][0], e=NAMED[k][1], i=NAMED[k][2], j=NAMED[k][3], ideal=NAMED[k][4];
    close(ideal,angleDeg(SLOTS[x+e][i],SLOTS[x+e][j]),1e-9,k+': its ideal is the angle those two slots make'); }
  const n7=k=>namedAngle(k,0.70);
  ok(n7('AX2E1')<120,'AX₂E bends below 120° (SO₂ 119)');
  ok(n7('AX2E2')<TET,'AX₂E₂ bends below tetrahedral (H₂O 104.5)');
  ok(n7('AX3E1')<TET,'AX₃E closes below tetrahedral (NH₃ 107.8)');
  ok(n7('AX4E1_ax')<180,'the seesaw\'s axial pair bends away from the lone pair (SF₄ 173.1)');
  ok(n7('AX3E2_axeq')<90,'the T-shape\'s arms close below 90° (ClF₃ 87.5)');
  ok(n7('AX5E1_axb')<90,'the square pyramid\'s base tilts below 90° (BrF₅ 84.8)');
  ok(n7('AX4E1_eq')>120,'and the model OPENS the seesaw\'s equatorial pair (SF₄ closes it to 101.6): the stated failure');
  close(n7('AX2E3'),180,1e-9,'AX₂E₃ stays exactly linear (symmetry)'); close(n7('AX4E2'),90,1e-9,'AX₄E₂ stays exactly square'); close(n7('AX2E4'),180,1e-9,'AX₂E₄ stays exactly linear');
  for(let n=2;n<=6;n++) for(let e=0;e<=n-2;e++){ const x=n-e;
    close(maxDiff(ANG(equilibrium(x,e,1).U,range(e,n)),idealBondAngles(x,e)),0,1e-9,'AX'+x+'E'+e+' at rho = 1 is its ideal shape (exact)'); }
  for(const k in REF.approach){ const [x,e,i,j]=NAMED[k==='AX4E1'?'AX4E1_ax':k==='AX3E2'?'AX3E2_axeq':k==='AX5E1'?'AX5E1_axb':k].slice(0,4);
    const a=r=>angleDeg(equilibrium(x,e,r).U[i],equilibrium(x,e,r).U[j])-angleDeg(equilibrium(x,e,1).U[i],equilibrium(x,e,1).U[j]);
    const ratio=a(0.98)/a(0.99);
    close(ratio,REF.approach[k].ratio,1e-6,k+': the approach to rho = 1, ratio '+fmt(ratio,4)+' (python)');
    ok(Math.abs(ratio-2)<0.05,k+': the departure is linear in 1 - rho'); }
  /* the squeeze curves the view draws, against the twin */
  { const cv=squeezeCurves(); for(const k of SQ_KEYS){ let m=0; REF.curves[k].forEach((v,i)=>{ m=Math.max(m,Math.abs(cv[k][i]+NAMED[k][4]-v)); }); ok(m<1e-8,'the '+k+' curve on 31 rho (python, '+m.toExponential(1)+')'); } }

  /* ---------- E. the audit in miniature: the VSEPR arrangement is the least ---------- */
  for(const rho of [0.70,0.99]) for(let n=3;n<=6;n++) for(let e=1;e<=n-1;e++){ const x=n-e;
    const lad=isomerLadder(x,e,rho), E0=equilibrium(x,e,rho).E, key='AX'+x+'E'+e;
    close(lad[0].E,E0,1e-9*E0,key+' at rho '+rho+': the VSEPR arrangement is the least of '+lad.length);
    ok(lad.slice(1).every(f=>f.E>E0+1e-6),key+' at rho '+rho+': every other arrangement is higher');
    /* the count matters at both rho: near 1 the gaps fall to 1e-4, where a loose
       dedup tolerance would silently merge two arrangements into one */
    const LR=(rho>0.9?REF.ladder99:REF.ladder)[key];
    if(LR){ eq(lad.length,LR.length,key+' at rho '+rho+': '+lad.length+' distinct arrangements (python)');
      close(maxDiff(lad.map(f=>f.E),LR),0,1e-8,key+' at rho '+rho+': their energies (python)'); } }
  for(const k in REF.ladder){ const m=/AX(\d)E(\d)/.exec(k), lad=isomerLadder(+m[1],+m[2],0.70);
    eq(lad.length,REF.ladder[k].length,k+': '+lad.length+' distinct arrangements (python)');
    close(maxDiff(lad.map(f=>f.E),REF.ladder[k]),0,1e-8,k+': their energies (python)'); }
  for(const rs in REF.audit) if(parseFloat(rs)>=RHO_MIN-1e-9) ok(Object.values(REF.audit[rs]).every(v=>v.ok),'derive.py\'s audit passes every class at rho '+rs+' (python)');
  ok(!Object.values(REF.audit['0.60']).every(v=>v.ok),'and fails below the slider, at rho 0.60 (python: AX₂E₄ goes bent)');
  { /* why 1/d^2: Coulomb's 1/d at rho 0.7 makes ClF3 trigonal planar */
    const T=relax(SLOTS[5].map(v=>v.slice()),radiiOf(3,2,0.7,[0,1]),1), P=relax(SLOTS[5].map(v=>v.slice()),radiiOf(3,2,0.7,[3,4]),1);
    close(T.E,REF.coulomb.AX3E2_T,1e-9,'Coulomb, AX₃E₂ lone pairs equatorial (python)'); close(P.E,REF.coulomb.AX3E2_planar,1e-9,'Coulomb, lone pairs axial (python)');
    ok(P.E<T.E,'under Coulomb 1/d the trigonal-planar arrangement wins: the reason for 1/d²');
    const T2=relax(SLOTS[5].map(v=>v.slice()),radiiOf(3,2,0.7,[0,1])), P2=relax(SLOTS[5].map(v=>v.slice()),radiiOf(3,2,0.7,[3,4]));
    close(T2.E,REF.coulomb.AX3E2_T_d2,1e-9,'1/d², T-shaped (python)'); close(P2.E,REF.coulomb.AX3E2_planar_d2,1e-9,'1/d², planar (python)'); ok(T2.E<P2.E,'under 1/d² the T-shape wins'); }

  /* ---------- F. Horn, Jacobi, the assignment, rotAtoB ---------- */
  { const A=SLOTS[6], perm=REF.horn.perm, Rt=REF.horn.Rt, Ap=perm.map(p=>A[p]), B=Ap.map(a=>matVec(Rt,a));
    const R=horn(Ap,B); let m=0; for(let i=0;i<3;i++) for(let j=0;j<3;j++) m=Math.max(m,Math.abs(R[i][j]-Rt[i][j]));
    ok(m<1e-12,'Horn recovers a known rotation (scipy, '+m.toExponential(1)+')');
    const det=R[0][0]*(R[1][1]*R[2][2]-R[1][2]*R[2][1])-R[0][1]*(R[1][0]*R[2][2]-R[1][2]*R[2][0])+R[0][2]*(R[1][0]*R[2][1]-R[1][1]*R[2][0]);
    close(det,1,1e-12,'a proper rotation: det = +1');
    const f=fitAssign(A,A.map(()=>'b'),B,B.map(()=>'b')); ok(f.res<1e-20,'fitAssign fits the permuted octahedron exactly ('+f.res.toExponential(1)+')');
    const N=REF.horn.noisy, Rn=horn(SLOTS[4],N.B); let mn=0; for(let i=0;i<3;i++) for(let j=0;j<3;j++) mn=Math.max(mn,Math.abs(Rn[i][j]-N.R[i][j]));
    ok(mn<1e-10,'Horn on a noisy tetrahedron matches scipy align_vectors ('+mn.toExponential(1)+')');
    const J=jacobiEig4([[4,1,0,0],[1,4,0,0],[0,0,2,1],[0,0,1,2]]); const ev=J.ev.slice().sort((p,q)=>p-q);
    close(maxDiff(ev,[1,3,3,5]),0,1e-12,'Jacobi: eigenvalues 1, 3, 3, 5 (exact)');
    /* a lone pair only ever takes a lone-pair slot */
    const E=equilibrium(3,2,0.7), kE=slotKinds(3,2), idx=[4,2,0,3,1], U=idx.map(i=>matVec(Rt,E.U[i])), kU=idx.map(i=>kE[i]);
    const g=fitAssign(E.U,kE,U,kU); ok(g.res<1e-20,'the assignment recovers a shuffled AX₃E₂ exactly');
    ok(g.sigma.every((s2,i)=>kE[s2]===kU[i]),'and every lone pair sits in a lone-pair slot');
    for(const [a,b] of [[[1,0,0],[0,1,0]],[[0,0,1],vnorm([1,2,-2])],[[0,0,1],[0,0,-1]],[vnorm([1,1,1]),vnorm([-1,-1,-1])]]){
      const Rr=rotAtoB(a,b), v=matVec(Rr,a); close(maxDiff(v,b),0,1e-12,'rotAtoB takes a onto b ('+a.map(z=>fmt(z,2))+')');
      const c0=matVec(Rr,[1,0,0]), c1=matVec(Rr,[0,1,0]); close(vdot(c0,c1),0,1e-12,'and is orthogonal'); } }

  /* ---------- G. the AXE names: PhET's rules ---------- */
  for(const k in REF.names){ const [x,e]=k.split(',').map(Number); eq(molGeometry(x,e),REF.names[k][0],'the molecule geometry of AX'+x+'E'+e+' (python)'); eq(EL_GEOM[x+e],REF.names[k][1],'its electron geometry (python)'); }
  eq(LABEL.tShaped,'T-shaped',"PhET's label"); eq(LABEL.trigonalBipyramidal,'Trigonal Bipyramidal',"PhET's label"); eq(geomNames(2,2).mol,'Bent','water is bent'); eq(geomNames(4,1).mol,'Seesaw','SF₄ is a seesaw');
  eq(axeName(2,2),'AX₂E₂','axeName'); eq(axeName(1,3),'AXE₃','axeName drops a 1'); eq(axeName(4,0),'AX₄','axeName with no lone pair');

  /* ---------- H. PhET's real molecules ---------- */
  eq(FULL_LIST.length,13,"PhET's list for Molecule Shapes"); eq(FULL_LIST[0],'H2O','it opens on water'); eq(BASICS_LIST.join(),'BeCl2,BF3,CH4,PCl5,SF6',"and Basics' five");
  eq(MOL_LIST,VARIANT==='basics'?BASICS_LIST:FULL_LIST,'the variant uses its own list');
  for(const id in REF.real){ const g=realGeometry(id), R=REF.real[id];
    eq(g.x,R.x,id+': '+R.x+' bonds'); eq(g.e,R.e,id+': '+R.e+' lone pairs on the centre'); eq(molGeometry(g.x,g.e),R.geom,id+' is '+R.geom); eq(EL_GEOM[g.x+g.e],R.elgeom,id+'\'s electron geometry');
    const d=distinctAngles(g.angles,1e-10).map(o=>o.v); close(maxDiff(d,R.distinct),0,1e-8,id+': the measured angles (python)');
    const lpb=[]; g.LP.forEach(l=>g.B.forEach(b=>lpb.push(angleDeg(l,b)))); lpb.sort((p,q)=>p-q);
    close(maxDiff(lpb,R.lpb),0,1e-8,id+': the lone pairs placed by the Horn fit (python)');
    close(g.fitRes,R.fitres,1e-10,id+': the fit residual (python)');
    const mo=modelOfReal(id,0.7); close(maxDiff(mo.angles,R.model_bb),0,1e-8,id+': the model at rho 0.70 (python)');
    close(maxDiff(REAL[id].bonds.map(b=>b.L),R.lengths),0,0,id+': PhET\'s bond lengths, verbatim');
    eq(REAL[id].order,R.order,id+': PhET\'s bond order '+R.order); eq(REAL[id].olp,R.olp,id+': '+R.olp+' lone pairs on each '+R.outer);
    eq(REAL[id].centre+REAL[id].outer,R.centre+R.outer,id+': its elements');
    const olp=REAL[id].olp, ol=outerLonePairs(g.B[0],olp); eq(ol.length,olp,id+': '+olp+' outer lone pairs');
    const want=olp===3?TET:olp===2?120:null; if(want) ol.forEach(w=>close(angleDeg(w,[-g.B[0][0],-g.B[0][1],-g.B[0][2]]),want,1e-9,id+': an outer lone pair at '+fmt(want,2)+'° from its bond'));
  }
  close(REF.real_named.NH3,107.8,1e-10,'PhET\'s NH₃ polar angle encodes H-N-H = 107.8° (python)');
  close(distinctAngles(realGeometry('NH3').angles)[0].v,107.8,1e-10,'and the JS reads 107.8°');
  close(realGeometry('H2O').angles[0],104.5,1e-10,'H₂O is 104.5° (PhET\'s value)');
  ok(Math.abs(realGeometry('CH4').angles[0]-TET)>1e-8,'PhET\'s rounded elevation makes CH₄ not quite ideal (python: 109.471220333°)');
  for(const [id,lo,hi] of [['PCl5',2.02,2.14],['SF4',1.545,1.646],['ClF3',1.598,1.698],['BrF5',1.689,1.774]]){
    const L=REAL[id].bonds.map(b=>b.L); close(Math.min.apply(0,L),lo,0,id+' shortest bond '+lo+' Å'); close(Math.max.apply(0,L),hi,0,id+' longest bond '+hi+' Å'); }
  { const rows=compareRows(0.70);
    REF.compare.forEach((c,i)=>{ const r=rows[i];
      close(r.meas,c.meas,1e-10,c.mol+' '+c.key+': measured '+c.meas+' (python)');
      close(r.model,c.model,1e-8,c.mol+' '+c.key+': model at 0.70 (python)');
      eq(r.agree,c.agree,c.mol+' '+c.key+': same direction '+c.agree+' (python)');
      if(c.rfit===null) ok(r.rfit===null,c.mol+' '+c.key+': no rho on the slider reaches it');
      else close(r.rfit,c.rfit,1e-7,c.mol+' '+c.key+': the rho that fits (python brentq)'); });
    eq(rows.filter(r=>r.agree).length,6,'the model bends six of the seven measured angles the right way'); }

  /* ---------- I. the model view's molecule ---------- */
  withState({},()=>{
    eq(LIVE.groups.length,2,"PhET's opening molecule has two single bonds");
    close(angleDeg(LIVE.groups[0].u,LIVE.groups[1].u),180,1e-9,'they relax into a line');
    ok(!LIVE.anim,'and the flow goes idle');
    const cam=[Math.cos(ST.camTheta)*Math.cos(ST.camPhi),Math.sin(ST.camTheta)*Math.cos(ST.camPhi),Math.sin(ST.camPhi)];
    const c=Math.abs(vdot(cam,LIVE.groups[0].u)); ok(c<Math.cos(30*DEG),'the default camera is not looking down the molecule (|cos| = '+fmt(c,3)+')');
    ok(liveAdd(1),'add a single bond'); liveSettle(); close(maxDiff(ANG(LIVE.groups.map(g=>g.u),[0,1,2]),[120,120,120]),0,1e-9,'three bonds: trigonal planar');
    if(HAS_LP){
      ok(liveAdd(0),'add a lone pair'); liveSettle();
      close(angleDeg(LIVE.groups[0].u,LIVE.groups[1].u),REF.named['0.70'].AX3E1,1e-8,'AX₃E: the trigonal pyramid at the model angle (python)');
      ok(!LIVE.anim,'settled'); ST.rho=0.85; LIVE.anim=true; liveSettle();
      close(angleDeg(LIVE.groups[0].u,LIVE.groups[1].u),REF.named['0.85'].AX3E1,1e-8,'moving rho re-relaxes it (python, 0.85)');
      ST.rho=0.70; LIVE.anim=true; liveSettle();
      ok(liveAdd(2)&&liveAdd(3),'up to six pairs');
    } else {
      ok(!canAdd(0)&&!liveAdd(0),'Basics refuses lone pairs outright (PhET has no lone-pair button)');
      ok(liveAdd(2)&&liveAdd(3)&&liveAdd(1),'up to six bonds');
    }
    eq(LIVE.groups.length,6,'six'); ok(!liveAdd(1)&&!canAdd(1)&&!canAdd(0),'a seventh is refused (PhET)');
    liveSettle(); const bi=LIVE.groups.map((g,i)=>g.order?i:-1).filter(i=>i>=0), li=LIVE.groups.map((g,i)=>g.order?-1:i).filter(i=>i>=0);
    eq(bi.length+'+'+li.length,HAS_LP?'5+1':'6+0',HAS_LP?'AX₅E':'AX₆');
    close(maxDiff(ANG(LIVE.groups.map(g=>g.u),bi),HAS_LP?ANG(equilibrium(5,1,0.7).U,[1,2,3,4,5]):ANG(equilibrium(6,0,0.7).U,[0,1,2,3,4,5])),0,1e-8,
      (HAS_LP?'the square pyramid':'the octahedron')+', whatever the bond orders (python angles via the equilibrium)');
    const singles=LIVE.groups.filter(g=>g.order===1), lastSingle=Math.max.apply(0,singles.map(g=>g.id));
    ok(liveRemove(1),'remove a single bond');
    ok(!LIVE.groups.some(g=>g.id===lastSingle)&&LIVE.groups.filter(g=>g.order===1).length===singles.length-1,
      'the LAST single bond added went, and only it (PhET)');
    ok(liveRemove(2),'remove the double bond'); ok(!liveHasOrder(2),'no double bond left'); ok(!liveRemove(2),'removing a missing kind does nothing');
    if(HAS_LP){ ST.showLP=false; ok(!canAdd(0)&&!liveAdd(0),'hidden lone pairs cannot be added (PhET)'); ST.showLP=true; }
    ok(liveRemoveAll(),'remove all'); eq(LIVE.groups.length,0,'nothing left'); ok(!liveRemoveAll(),'a second remove all has nothing to do');
    liveStep(1/60); ok(!LIVE.anim,'an empty molecule is idle');
  });
  withState({_load:HAS_LP?[2,2]:[4,0]},()=>{
    const B0=LIVE.groups.map((g,i)=>g.order?i:-1).filter(i=>i>=0);
    close(angleDeg(LIVE.groups[B0[0]].u,LIVE.groups[B0[1]].u),HAS_LP?REF.named['0.70'].AX2E2:TET,1e-9,'a loaded '+(HAS_LP?'AX₂E₂':'AX₄')+' sits at its equilibrium');
    /* drag the first bond round, hold it, then let go: it slides back */
    const S=makeScene({getContext:()=>makeShot(1100,712)}); S.W=1100; S.H=712;
    S.draw(); const bi=B0[0], p=PICK.find(q=>q.i===bi);
    ok(!!p,'the bond can be picked'); ok(S.pointer('down',p.x,p.y),'pointer-down on it grabs it'); eq(LIVE.held,bi,'it is held');
    const u0=LIVE.groups[bi].u.slice(); S.pointer('move',p.x+60,p.y-40); ok(angleDeg(u0,LIVE.groups[bi].u)>5,'it follows the pointer');
    for(let k=0;k<30;k++) liveStep(1/60); ok(LIVE.anim,'the others keep moving while it is held');
    ok(S.pointer('up',0,0),'pointer-up releases'); eq(LIVE.held,-1,'released'); liveSettle();
    close(angleDeg(LIVE.groups[B0[0]].u,LIVE.groups[B0[1]].u),HAS_LP?REF.named['0.70'].AX2E2:TET,1e-8,'and the molecule relaxes back to its angle');
    /* pointerDir round trip: the projected position of a direction maps back to it */
    const C=modelGeo(makeShot(1100,712),1100,712).C, u=vnorm([0.3,-0.8,0.5]), q=C.P(u);
    const back=pointerDir(C,q.x,q.y,1); close(maxDiff(back,u),0,1e-9,'pointerDir inverts the projection on the near side');
    const far=pointerDir(C,C.b.x+2,C.b.y+2,1); close(vdot(far,far),1,1e-12,'off the silhouette it still returns a unit vector');
  });
  if(HAS_LP) withState({_load:[4,1]},()=>{ ok(liveAdd(0)===true,'AX₄E + a lone pair'); liveSettle();
    const li=LIVE.groups.map((g,i)=>g.order?-1:i).filter(i=>i>=0); close(angleDeg(LIVE.groups[li[0]].u,LIVE.groups[li[1]].u),180,1e-8,'the two lone pairs end trans: square planar'); });

  withState({_load:[4,2]},()=>{
    /* the steering earns its keep here: put the two lone pairs CIS by hand -- a true
       local minimum of the repulsion (derive: 65 of 100 random starts end there) --
       and the flow must still come back to the VSEPR trans arrangement */
    const li=LIVE.groups.map((g,i)=>g.order?-1:i).filter(i=>i>=0), bi=LIVE.groups.map((g,i)=>g.order?i:-1).filter(i=>i>=0);
    const lad=isomerLadder(4,2,0.70);
    ok(lad.length===2&&lad[1].E>lad[0].E,'AX₄E₂ has a second arrangement, higher in energy');
    const iso=lad[1], lpIdx=iso.lp, bIdx=[0,1,2,3,4,5].filter(i=>lpIdx.indexOf(i)<0);  /* its lone pairs sit in ITS slots */
    LIVE.groups[li[0]].u=iso.U[lpIdx[0]].slice(); LIVE.groups[li[1]].u=iso.U[lpIdx[1]].slice();
    bi.forEach((g,k)=>LIVE.groups[g].u=iso.U[bIdx[k]].slice());
    const cisAng=angleDeg(LIVE.groups[li[0]].u,LIVE.groups[li[1]].u);
    ok(cisAng<150,'the lone pairs start cis ('+fmt(cisAng,1)+'°, not trans)');
    LIVE.fitKey=''; LIVE.anim=true; liveSettle();
    close(angleDeg(LIVE.groups[li[0]].u,LIVE.groups[li[1]].u),180,1e-7,'and the steered flow brings them back trans: square planar');
    close(energyOf(LIVE.groups.map(g=>g.u),radiiLive(LIVE.groups,0.70)),lad[0].E,1e-9,'at the VSEPR energy, not the cis one'); });

  /* ---------- J. the real view's Real / Model blend ---------- */
  withState({view:'real',mol:'H2O',realMode:'model'},()=>{
    let n=0; while(realStep(1/60)&&n<600) n++; eq(LIVE.realBlend,1,'the blend reaches the model'); ok(n>5,'over '+n+' frames, not in one');
    const sh=realShown('H2O',ST.rho,1); close(angleDeg(sh.B[0],sh.B[1]),REF.named['0.70'].AX2E2,1e-8,'the model water (python)');
    const s0=realShown('H2O',ST.rho,0); close(angleDeg(s0.B[0],s0.B[1]),104.5,1e-10,'the measured water');
    ST.realMode='real'; n=0; while(realStep(1/60)&&n<600) n++; eq(LIVE.realBlend,0,'and back'); ok(!realStep(1/60),'then idle'); });

  /* ---------- K. the relaxation view ---------- */
  for(const key of ['AX4E2','AX2E3','AX4E1','AX5E0']){ const m=/AX(\d)E(\d)/.exec(key), x=+m[1], e=+m[2], R=REF.starts[key];
    for(const s of R.first.slice(0,4)) withState({view:'relax',_load:[x,e],_seed:s.seed,_run:'all'},()=>{
      close(RELAX.hist[RELAX.hist.length-1],s.E,1e-8*Math.max(1,s.E),key+' start '+s.seed+': the final U (python)');
      ok(Math.abs(RELAX.step-s.it)<=3,key+' start '+s.seed+': '+RELAX.step+' steps (python '+s.it+')');
      const v=relaxVerdict(); eq(v.rank,s.rank,key+' start '+s.seed+': it ends in arrangement '+s.rank+' (python)'); ok(v.vsepr,'the ladder\'s least is the VSEPR arrangement'); }); }
  ok(REF.starts.AX4E2.count[1]>50,'derive: most random AX₄E₂ starts stall cis ('+REF.starts.AX4E2.count[1]+' of 100)');
  ok(REF.starts.AX6E0.count[0]===100&&REF.starts.AX5E0.count[0]===100,'derive: every equal-pair start reaches the ideal shape');
  withState({view:'relax',_load:[1,0]},()=>{ relaxEnsure(); ok(RELAX.U===null&&RELAX.done,'fewer than two pairs: nothing to relax'); });
  withState({view:'relax',_load:[3,1],_seed:0,_run:10},()=>{ const k0=RELAX.key; ST.rho=0.9; relaxEnsure(); ok(RELAX.key!==k0&&RELAX.step===0,'changing rho restarts the descent'); });

  /* ---------- K2. the drawing geometry that carries meaning ---------- */
  { /* the camera fitter frames what it claims: a ball of radius R fills `frac` of the box */
    const b=box(0,0,900,600), R=1.32, frac=0.86, D=fitDist(b,R,frac), f=(b.h/2)/Math.tan(0.78/2);
    close(2*f*R/Math.sqrt(D*D-R*R),frac*Math.min(b.w,b.h),1e-9,'fitDist frames the silhouette at the fraction it claims (exact tangent cone)');
    ok(D>fitDist(b,R,frac*2)&&fitDist(b,R,frac)<fitDist(b,2*R,frac)*1.0001,'a bigger ball or a wider fraction moves the camera the right way');
    const C=boxCamera(b,0.3,0.2,D,[0,0,0]), q0=C.P([0,0,0]);
    close(q0.x,b.x+b.w/2,1e-9,'the target projects to the box centre'); close(q0.y,b.y+b.h/2,1e-9,'in both axes'); }
  { /* the lone-pair lobe: the hull of a root circle and a bulb */
    const P=teardropPts(100,100,3,200,100,20);        /* 23 points on the bulb, then 9 on the root */
    let db=0, dr=0;
    for(let i=0;i<23;i++) db=Math.max(db,Math.abs(Math.hypot(P[i][0]-200,P[i][1]-100)-20));
    for(let i=23;i<P.length;i++) dr=Math.max(dr,Math.abs(Math.hypot(P[i][0]-100,P[i][1]-100)-3));
    close(db,0,1e-9,'the teardrop\'s bulb arc lies on the bulb circle'); close(dr,0,1e-9,'and its root arc on the root circle');
    ok(P[11][0]>200&&P[0][0]<200,'the bulb arc sweeps round the far side (its middle is the far point)');
    ok(P.length>20,'as a polygon, not an ellipse (the recorder has no ellipse: Known-bad)');
    const Q=teardropPts(100,100,3,101,100,20); let qm=0; for(const p of Q) qm=Math.max(qm,Math.hypot(p[0]-101,p[1]-100));
    close(qm,20,1e-9,'end-on (the root inside the bulb) it is the bulb circle'); }
  { /* PhET stands its molecules with the lone pairs up; the world here is z-up */
    const g=realGeometry('H2O'); ok(g.LP[0][2]>0.5&&g.LP[1][2]>0.5,'water\'s lone pairs point up in the world frame');
    ok(g.B[0][2]<0&&g.B[1][2]<0,'and its hydrogens down');
    const det=PHET_TO_WORLD[0][0]*(PHET_TO_WORLD[1][1]*PHET_TO_WORLD[2][2]-PHET_TO_WORLD[1][2]*PHET_TO_WORLD[2][1])
      -PHET_TO_WORLD[0][1]*(PHET_TO_WORLD[1][0]*PHET_TO_WORLD[2][2]-PHET_TO_WORLD[1][2]*PHET_TO_WORLD[2][0])
      +PHET_TO_WORLD[0][2]*(PHET_TO_WORLD[1][0]*PHET_TO_WORLD[2][1]-PHET_TO_WORLD[1][1]*PHET_TO_WORLD[2][0]);
    close(det,1,1e-12,'the map is a rotation, not a reflection: no molecule is mirrored'); }
  { /* the display frame keeps every pair off the default line of sight */
    const vd=viewDirOf(DEFAULTS.camTheta,DEFAULTS.camPhi);
    for(let n=2;n<=6;n++) for(let e=0;e<=(HAS_LP?n-2:0);e++){ const x=n-e, U=displayFrame(equilibrium(x,e,0.70).U,e);
      /* the pair CLOSEST to the line of sight is the one that would hide: take the max */
      let worst=0; for(const u of U) worst=Math.max(worst,Math.abs(angleDeg(u,vd)-90));
      ok(worst<72,'AX'+x+'E'+e+': every pair is at least '+fmt(90-worst,0)+'° off the default line of sight');
      if(e) ok(U.slice(0,e).reduce((a,u)=>a+u[2],0)>-1e-9,'and its lone pairs are up'); } }

  { /* a double bond draws two sticks, a triple three: the order reaches the picture */
    const shot=makeShot(900,600), C=molCam(box(0,0,900,600),1.32,1);
    const strokes=o=>{ const c=makeShot(900,600);
      renderMolecule(c,C,{atoms:[{p:[0,0,0],r:R_CENTRE,col:COL.centre},{p:[1,0,0],r:R_OUTER,col:COL.outer}],bonds:[{a:0,b:1,order:o}],lps:[]});
      return c.ops.filter(x=>x.op==='stroke').length; };
    const s1=strokes(1), s2=strokes(2), s3=strokes(3);
    ok(s2>s1&&s3>s2,'one, two and three sticks for the bond order ('+s1+', '+s2+', '+s3+' strokes)');
    ok(shot.ops.length===0,'(the probe drew into its own recorder)'); }
  { /* the flow's two terms: the steering fixes WHERE it ends, the repulsion only the path */
    const path=kap=>{ ST.rho=0.70; liveLoad(3,1); const g=LIVE.groups;
      g[1].u=vnorm([g[1].u[0]+0.35,g[1].u[1]-0.3,g[1].u[2]+0.2]);       /* nudge it off the equilibrium */
      LIVE.fitKey=''; LIVE.anim=true; const keep=FLOW.KAP; FLOW.KAP=kap;
      let len=0, prev=g.map(q=>q.u.slice());
      for(let k=0;k<40;k++){ liveStep(1/60); LIVE.groups.forEach((q,i)=>{ len+=angleDeg(prev[i],q.u); prev[i]=q.u.slice(); }); }
      liveSettle(); const end=angleDeg(LIVE.groups[1].u,LIVE.groups[2].u); FLOW.KAP=keep; return {len,end}; };
    const withRep=path(FLOW.KAP), without=path(0);
    ok(Math.abs(withRep.len-without.len)>1,'the repulsion changes the path the pairs take ('+fmt(withRep.len,1)+'° against '+fmt(without.len,1)+'°)');
    close(withRep.end,without.end,1e-7,'but not where they end: the steering fixes that');
    close(withRep.end,REF.named['0.70'].AX3E1,1e-7,'at the model angle either way (python)'); }

  /* ---------- L. PhET's arc rule ---------- */
  close(arcBrightness([1,0,0],[0,1,0],[0,0,1],2),1,0,'two bonds always show');
  close(arcBrightness([1,0,0],[0,1,0],[0,0,1],4),1,0,'an arc facing the camera is full');
  close(arcBrightness([1,0,0],[0,1,0],[1,0,0],4),0,0,'an arc seen edge-on vanishes');
  close(arcBrightness([1,0,0],[0,1,0],vnorm([0,1,0.5]),4),(0.5/Math.sqrt(1.25)-0.35)/(0.55-0.35),1e-12,'in between: (|n.v| - 0.35)/(0.55 - 0.35) for four bonds (PhET\'s thresholds)');
  close(arcBrightness([1,0,0],[0,1,0],vnorm([0,1,1]),6),(Math.SQRT1_2-0.5)/0.25,1e-12,'and (|n.v| - 0.5)/0.25 for six');
  close(arcBrightness([1,0,0],[0,1,0],vnorm([0,1,2]),6),1,0,'clamped at full above the upper threshold');
  close(arcBrightness([1,0,0],[0,1,0],vnorm([0,1,0.2]),3),clamp((0.2/Math.sqrt(1.04)-0.1)/0.4,0,1),1e-12,'and (|n.v| - 0.1)/0.4 for three');

  /* ---------- M. the panels ---------- */
  const PRESETS={model:[{},{_load:[2,2]},{_load:[6,0],showAngles:true},{_empty:true},{_load:[1,4]},{_load:[3,2],rho:1}],
                 real:(VARIANT==='basics'?BASICS_LIST:FULL_LIST).map(id=>({mol:id})).concat([{mol:MOL_LIST[0],realMode:'model',_blend:1}]),
                 table:[{},{rho:0.85}],squeeze:[{},{rho:1},{rho:0.83}],relax:[{},{_load:[4,2],_seed:2,_run:'all'},{_load:[1,0]}]};
  for(const [v] of TABS) for(const over of PRESETS[v]){
    const M=withState(Object.assign({view:v},over),()=>{ const M2=buildModel(); return {html:readoutHTML(M2)+eqbarHTML(M2)+tagHTML(M2)}; });
    ok(M.html.indexOf('NaN')<0&&M.html.indexOf('undefined')<0&&M.html.indexOf('Infinity')<0,'panels clean for '+v+' '+JSON.stringify(over));
  }
  ok(withState({view:'model',_load:[2,2]},()=>readoutHTML(buildModel())).indexOf('105.1&deg;')>=0,'the model readout prints water\'s 105.1° off the model');
  ok(withState({view:'real',mol:'NH3'},()=>readoutHTML(buildModel())).indexOf('107.8&deg;')>=0,'the real readout prints NH₃\'s 107.8°');
  ok(withState({view:'real',mol:'PCl5'},()=>readoutHTML(buildModel())).indexOf('2.140 &Aring;')>=0,'and PCl₅\'s 2.140 Å axial bonds');
  if(HAS_LP) ok(withState({view:'squeeze'},()=>readoutHTML(buildModel())).indexOf('101.6 / 121.2')>=0,'the squeeze readout prints SF₄\'s 101.6 against the model\'s 121.2');

  /* ---------- N. the pointer through the scene ---------- */
  { const shot=makeShot(1100,712), S=makeScene({getContext:()=>shot}); S.W=1100; S.H=712;
    withState({view:'model'},()=>{ S.draw(); const t0=ST.camTheta, p0=ST.camPhi;
      ok(S.pointer('down',60,640)&&DRAG.what==='orbit','pointer-down on empty stage starts a turn');
      S.pointer('move',160,640); close(ST.camTheta,t0-100*0.0075,1e-12,'a horizontal drag turns theta'); close(ST.camPhi,p0,0,'and not phi');
      S.pointer('move',160,700); close(ST.camPhi,p0+60*0.006,1e-12,'a vertical drag turns phi'); S.pointer('up',0,0);
      ok(S.wheel(-100)&&ST.zoom>1,'the wheel zooms in'); });
    if(HAS_LP) withState({view:'squeeze'},()=>{ const b=squeezeGeo(shot,1100,712).top;
      ok(S.pointer('down',b.x+b.w*0.5,b.y+b.h*0.5),'pointer-down on the top panel'); close(ST.rho,0.85,1e-12,'sets rho = 0.85 at mid-panel');
      S.pointer('move',b.x+b.w*(0.13/0.3),b.y+10); close(ST.rho,0.83,1e-12,'dragging sets rho = 0.83');
      /* off a step: the drag snaps to the slider's 0.01, so the cache keeps 31 values */
      S.pointer('move',b.x+b.w*0.37,b.y+10); close(ST.rho,0.81,1e-12,'and snaps 0.8110 to 0.81'); S.pointer('up',0,0);
      ok(!S.pointer('down',b.x-40,b.y1+40),'outside it nothing is grabbed'); });
    withState({view:'table'},()=>{ S.draw(); const cell=HIT.find(h=>h.x===4&&h.e===(HAS_LP?1:0));
      ok(!!cell,'the table has the cell'); S.pointer('down',cell.b.x+cell.b.w/2,cell.b.y+cell.b.h/2); ok(S.pointer('up',0,0),'a click on it');
      eq(ST.view,'model','switches to the model view'); const c=liveCounts(); eq(c.x+','+c.e,HAS_LP?'4,1':'4,0','with that class built'); });
    withState({view:'table'},()=>{ S.draw(); const cell=HIT[0], t0=ST.camTheta; S.pointer('down',cell.b.x+5,cell.b.y+5); S.pointer('move',cell.b.x+65,cell.b.y+5); S.pointer('up',0,0);
      eq(ST.view,'table','a drag on the table is a turn, not a click'); ok(ST.camTheta!==t0,'and it turns the shapes'); });
  }

  /* ---------- O. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['model default',{view:'model'},8],['model water angles names',{view:'model',_load:[2,2],showAngles:true,showMolName:true,showElName:true},10],
    ['model octahedral angles',{view:'model',_load:[6,0],showAngles:true,showMolName:true},12],['model seesaw',{view:'model',_load:[4,1],showAngles:true},10],
    ['model empty',{view:'model',_empty:true},1],['model diatomic',{view:'model',_load:[1,3],showElName:true,showMolName:true},4],['model zoomed',{view:'model',_load:[3,2],zoom:2.5,showAngles:true},6],
    ['model mixed orders',{view:'model',_add:[2,3,0]},8],
    ['real first',{view:'real'},6],['real angles',{view:'real',mol:MOL_LIST[MOL_LIST.length-1],showAngles:true,showMolName:true,showElName:true,showOuterLP:true},10],
    ['real model mode',{view:'real',mol:MOL_LIST[1],realMode:'model',_blend:1,showAngles:true},6],['real mid blend',{view:'real',mol:MOL_LIST[2],_blend:0.5},6],
    ['table',{view:'table'},20],['table rho 1',{view:'table',rho:1},20],
    ['relax start',{view:'relax',_load:[4,2],_seed:2},6],['relax stuck',{view:'relax',_load:[4,2],_seed:2,_run:'all'},6],['relax ideal',{view:'relax',_load:[6,0],_run:'all'},6],['relax empty',{view:'relax',_load:[1,0]},1],
  ];
  /* squeeze floor 15: the one-panel mode of a short stage draws the background, seven diamonds and seven rho dots */
  if(HAS_LP) CONFIGS.push(['squeeze',{view:'squeeze'},15],['squeeze rho 1',{view:'squeeze',rho:1},15],['squeeze mid',{view:'squeeze',rho:0.83},15],
    ['real SF4 model outer',{view:'real',mol:'SF4',realMode:'model',_blend:1,showAngles:true,showOuterLP:true,showMolName:true,showElName:true},10]);
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
      const blank=fills.filter(f=>f.style&&/NaN/.test(f.style)); ok(!blank.length,nm+' '+W+'x'+H+' no NaN colours');
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
