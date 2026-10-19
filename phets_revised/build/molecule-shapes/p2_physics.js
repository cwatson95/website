
/* ================================================================== *
 *  the model: electron domains on two spheres, repelling as 1/d^2     *
 *  (every function here is twinned in build/molecule-shapes/derive.py *
 *  and pinned against its printed output in selfTest)                 *
 * ================================================================== */
const DEG=Math.PI/180, RAD=180/Math.PI;      /* DEG converts degrees INTO radians (Known-bad: bloch_sphere) */
const EXPN=2;                  /* the pair energy is 1/d^EXPN; derive.py shows 1/d fails the AXE table at rho 0.7 */
const RHO_PHET=7/10;           /* PhET's value: LONE_PAIR_DISTANCE 7 against BONDED_PAIR_DISTANCE 10 */
const RHO_MIN=0.70, RHO_MAX=1.00;
const ETA=0.1, GTOL=1e-13, ITMAX=20000;      /* the relaxation: step, tolerance on the tangential gradient, cap */
const MAXG=6;                  /* PhET's value: at most six pairs round the central atom (maxConnections) */
const TET=Math.acos(-1/3)*RAD; /* the tetrahedral angle, 109.4712206...° */
const SQ3=Math.sqrt(3), T8=Math.sqrt(8/9);

/* the ideal electron geometries, principal axis along z.  LONE PAIRS FILL THE
   FIRST SLOTS: the rule PhET's model notes state (the higher-repulsion slots
   first), which puts them equatorial in the bipyramid and trans in the
   octahedron.  derive.py audits that rule against the energy below. */
const SLOTS={
  1:[[0,0,1]],
  2:[[0,0,1],[0,0,-1]],
  3:[[0,0,1],[SQ3/2,0,-0.5],[-SQ3/2,0,-0.5]],
  4:[[0,0,1],[T8,0,-1/3],[-T8/2,T8*SQ3/2,-1/3],[-T8/2,-T8*SQ3/2,-1/3]],
  5:[[1,0,0],[-0.5,SQ3/2,0],[-0.5,-SQ3/2,0],[0,0,1],[0,0,-1]],
  6:[[0,0,1],[0,0,-1],[1,0,0],[-1,0,0],[0,1,0],[0,-1,0]],
};

/* ---- small linear algebra ---- */
const vdot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const vnorm=a=>{ const l=Math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]); return [a[0]/l,a[1]/l,a[2]/l]; };
const vcross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
/* the angle between two vectors as atan2(|a x b|, a.b): acos is ill-conditioned near 0 and 180°,
   where one ulp of a.b is 1e-6° (twin: derive.pair_angles) */
function angleDeg(a,b){ const c=vcross(a,b); return Math.atan2(Math.sqrt(vdot(c,c)),vdot(a,b))*RAD; }
function matVec(M,v){ return [M[0][0]*v[0]+M[0][1]*v[1]+M[0][2]*v[2],M[1][0]*v[0]+M[1][1]*v[1]+M[1][2]*v[2],M[2][0]*v[0]+M[2][1]*v[1]+M[2][2]*v[2]]; }
function matMul(A,B){ const C=[[0,0,0],[0,0,0],[0,0,0]];
  for(let i=0;i<3;i++) for(let j=0;j<3;j++) C[i][j]=A[i][0]*B[0][j]+A[i][1]*B[1][j]+A[i][2]*B[2][j]; return C; }
/* the rotation taking unit a onto unit b the short way (Rodrigues) */
function rotAtoB(a,b){
  const v=vcross(a,b), c=vdot(a,b);
  if(c<-1+1e-12){ const p=Math.abs(a[0])<0.9?[1,0,0]:[0,1,0], k=vnorm(vcross(a,p));
    return [[2*k[0]*k[0]-1,2*k[0]*k[1],2*k[0]*k[2]],[2*k[1]*k[0],2*k[1]*k[1]-1,2*k[1]*k[2]],[2*k[2]*k[0],2*k[2]*k[1],2*k[2]*k[2]-1]]; }
  const f=1/(1+c), K=[[0,-v[2],v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]], K2=matMul(K,K);
  return [[1+K[0][0]+f*K2[0][0],K[0][1]+f*K2[0][1],K[0][2]+f*K2[0][2]],
          [K[1][0]+f*K2[1][0],1+K[1][1]+f*K2[1][1],K[1][2]+f*K2[1][2]],
          [K[2][0]+f*K2[2][0],K[2][1]+f*K2[2][1],1+K[2][2]+f*K2[2][2]]];
}

/* ---- the energy and its gradient ----
   x_i = R_i u_i with R = 1 for a bond, rho for a lone pair;
   E = sum_{i<j} |x_i - x_j|^-s,  dE/du_i = R_i sum_j -s (x_i - x_j)|x_i - x_j|^(-s-2) */
function energyOf(U,R,s){
  s=s===undefined?EXPN:s;
  let E=0; const n=U.length;
  for(let i=0;i<n;i++) for(let j=i+1;j<n;j++){
    const dx=R[i]*U[i][0]-R[j]*U[j][0], dy=R[i]*U[i][1]-R[j]*U[j][1], dz=R[i]*U[i][2]-R[j]*U[j][2];
    E+=Math.pow(dx*dx+dy*dy+dz*dz,-s/2);
  }
  return E;
}
function gradOf(U,R,s){
  s=s===undefined?EXPN:s;
  const n=U.length, G=[];
  for(let i=0;i<n;i++){
    let gx=0,gy=0,gz=0;
    for(let j=0;j<n;j++){ if(i===j) continue;
      const dx=R[i]*U[i][0]-R[j]*U[j][0], dy=R[i]*U[i][1]-R[j]*U[j][1], dz=R[i]*U[i][2]-R[j]*U[j][2];
      const w=-s*Math.pow(dx*dx+dy*dy+dz*dz,-s/2-1);
      gx+=w*dx; gy+=w*dy; gz+=w*dz; }
    G.push([R[i]*gx,R[i]*gy,R[i]*gz]);
  }
  return G;
}
/* the part of the gradient that moves u along its sphere */
function tangentOf(U,G){ return G.map((g,i)=>{ const u=U[i], c=vdot(g,u); return [g[0]-c*u[0],g[1]-c*u[1],g[2]-c*u[2]]; }); }
function maxLen(V){ let m=0; for(const v of V) m=Math.max(m,Math.sqrt(vdot(v,v))); return m; }

/* THE RELAXATION (twin of derive.relax_gd): u <- normalise(u - eta grad_t) until
   every tangential gradient is below GTOL.  eta*lambda_max = 0.82 < 2 over every
   class (derive), so the fixed step is stable. */
function relax(U0,R,s,itmax){
  let U=U0.map(vnorm); const cap=itmax||ITMAX; let it=0, m=Infinity;
  for(;it<cap;it++){
    const Gt=tangentOf(U,gradOf(U,R,s));
    m=maxLen(Gt);
    if(m<GTOL) break;
    U=U.map((u,i)=>vnorm([u[0]-ETA*Gt[i][0],u[1]-ETA*Gt[i][1],u[2]-ETA*Gt[i][2]]));
  }
  return {U,it,gmax:m,E:energyOf(U,R,s)};
}
/* radii of a class in slot order: e lone pairs first, then x bonds (or a chosen lone-pair set) */
function radiiOf(x,e,rho,lpSet){
  const out=[]; for(let k=0;k<x+e;k++) out.push((lpSet?lpSet.indexOf(k)>=0:k<e)?rho:1); return out;
}
/* the equilibrium of a class, relaxed from the VSEPR slots (cached per x, e, rho) */
const EQCACHE={};
function equilibrium(x,e,rho){
  const key=x+','+e+','+rho.toFixed(12);
  if(EQCACHE[key]) return EQCACHE[key];
  const n=x+e;
  if(n===0) return (EQCACHE[key]={U:[],R:[],E:0,it:0});
  const r=relax(SLOTS[n].map(v=>v.slice()),radiiOf(x,e,rho));
  return (EQCACHE[key]={U:r.U,R:radiiOf(x,e,rho),E:r.E,it:r.it,gmax:r.gmax});
}
/* every distinct arrangement of e lone pairs over the slots, relaxed: the isomer ladder */
function combos(n,k){ const out=[]; const rec=(s,acc)=>{ if(acc.length===k){ out.push(acc.slice()); return; }
  for(let i=s;i<n;i++){ acc.push(i); rec(i+1,acc); acc.pop(); } }; rec(0,[]); return out; }
const LADDER={};
function isomerLadder(x,e,rho){
  const key=x+','+e+','+rho.toFixed(12);
  if(LADDER[key]) return LADDER[key];
  const n=x+e, found=[];
  for(const lp of combos(n,e)){
    const r=relax(SLOTS[n].map(v=>v.slice()),radiiOf(x,e,rho,lp));
    if(!found.some(f=>Math.abs(f.E-r.E)<1e-8)) found.push({E:r.E,lp,U:r.U});
  }
  found.sort((a,b)=>a.E-b.E);
  return (LADDER[key]=found);
}

/* ---- Horn's quaternion fit (twin of derive.horn): the rotation R minimising
   sum |R a_k - b_k|^2 is the top eigenvector of a 4x4 built from sum a b^T ---- */
function jacobiEig4(A0){
  const A=A0.map(r=>r.slice()), V=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]];
  for(let sweep=0;sweep<60;sweep++){
    let off=0; for(let i=0;i<4;i++) for(let j=0;j<4;j++) if(i!==j) off+=A[i][j]*A[i][j];
    if(off<1e-30) break;
    for(let p=0;p<3;p++) for(let q=p+1;q<4;q++){
      if(Math.abs(A[p][q])<1e-300) continue;
      const th=(A[q][q]-A[p][p])/(2*A[p][q]);
      const t=(th>=0?1:-1)/(Math.abs(th)+Math.sqrt(th*th+1)), c=1/Math.sqrt(t*t+1), sn=t*c;
      for(let k=0;k<4;k++){ const akp=A[k][p], akq=A[k][q]; A[k][p]=c*akp-sn*akq; A[k][q]=sn*akp+c*akq; }
      for(let k=0;k<4;k++){ const apk=A[p][k], aqk=A[q][k]; A[p][k]=c*apk-sn*aqk; A[q][k]=sn*apk+c*aqk; }
      for(let k=0;k<4;k++){ const vkp=V[k][p], vkq=V[k][q]; V[k][p]=c*vkp-sn*vkq; V[k][q]=sn*vkp+c*vkq; }
    }
  }
  return {ev:[A[0][0],A[1][1],A[2][2],A[3][3]],V};
}
function horn(Asrc,Bdst){
  let Sxx=0,Sxy=0,Sxz=0,Syx=0,Syy=0,Syz=0,Szx=0,Szy=0,Szz=0;
  for(let k=0;k<Asrc.length;k++){ const a=Asrc[k], b=Bdst[k];
    Sxx+=a[0]*b[0]; Sxy+=a[0]*b[1]; Sxz+=a[0]*b[2];
    Syx+=a[1]*b[0]; Syy+=a[1]*b[1]; Syz+=a[1]*b[2];
    Szx+=a[2]*b[0]; Szy+=a[2]*b[1]; Szz+=a[2]*b[2]; }
  const N=[[Sxx+Syy+Szz,Syz-Szy,Szx-Sxz,Sxy-Syx],
           [Syz-Szy,Sxx-Syy-Szz,Sxy+Syx,Szx+Sxz],
           [Szx-Sxz,Sxy+Syx,-Sxx+Syy-Szz,Syz+Szy],
           [Sxy-Syx,Szx+Sxz,Syz+Szy,-Sxx-Syy+Szz]];
  const {ev,V}=jacobiEig4(N);
  let k=0; for(let i=1;i<4;i++) if(ev[i]>ev[k]) k=i;
  const q0=V[0][k], qx=V[1][k], qy=V[2][k], qz=V[3][k];
  return [[q0*q0+qx*qx-qy*qy-qz*qz,2*(qx*qy-q0*qz),2*(qx*qz+q0*qy)],
          [2*(qy*qx+q0*qz),q0*q0-qx*qx+qy*qy-qz*qz,2*(qy*qz-q0*qx)],
          [2*(qz*qx-q0*qy),2*(qz*qy+q0*qx),q0*q0-qx*qx-qy*qy+qz*qz]];
}
function permutations(a){ if(a.length<2) return [a.slice()]; const out=[];
  a.forEach((v,i)=>{ for(const p of permutations(a.slice(0,i).concat(a.slice(i+1)))) out.push([v].concat(p)); }); return out; }
/* the best rotation AND assignment of slots E (kinds kE) onto current directions
   U (kinds kU): a lone pair only ever takes a lone-pair slot, a bond a bond slot
   (every bond order alike, as in PhET).  `skip` lists current entries left out of
   the residual (a newly added group).  Returns {res, sigma, R}: sigma[i] is the
   slot of current entry i. */
function fitAssign(E,kE,U,kU,skip){
  const kinds=['lp','b'], best={res:Infinity,sigma:null,R:null};
  const cur={}, slot={};
  for(const k of kinds){ cur[k]=[]; slot[k]=[]; }
  kU.forEach((k,i)=>cur[k].push(i)); kE.forEach((k,i)=>slot[k].push(i));
  for(const k of kinds) if(cur[k].length!==slot[k].length) throw new Error('fitAssign: kinds differ');
  const PL=permutations(slot.lp), PB=permutations(slot.b);
  const sk=skip||[];
  for(const pl of PL) for(const pb of PB){
    const sigma=new Array(U.length);
    cur.lp.forEach((i,j)=>sigma[i]=pl[j]); cur.b.forEach((i,j)=>sigma[i]=pb[j]);
    const A=[],B=[];
    for(let i=0;i<U.length;i++) if(sk.indexOf(i)<0){ A.push(E[sigma[i]]); B.push(U[i]); }
    const R=A.length?horn(A,B):[[1,0,0],[0,1,0],[0,0,1]];
    let res=0; for(let k=0;k<A.length;k++){ const r=matVec(R,A[k]); res+=(r[0]-B[k][0])**2+(r[1]-B[k][1])**2+(r[2]-B[k][2])**2; }
    if(res<best.res-1e-12){ best.res=res; best.sigma=sigma; best.R=R; }
  }
  return best;
}

/* ---- mulberry32 (the house PRNG; twin in derive.py) and random directions ---- */
function mulberry32(seed){
  let a=seed|0;
  return function(){ a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; };
}
function randomDirs(rnd,n){ const out=[];
  for(let k=0;k<n;k++){ const z=2*rnd()-1, ph=2*Math.PI*rnd(), r=Math.sqrt(Math.max(0,1-z*z)); out.push([r*Math.cos(ph),r*Math.sin(ph),z]); }
  return out; }

/* ---- the AXE table: PhET's getConfiguration rules (build 1.6.19), PhET's English labels ---- */
function molGeometry(x,e){
  if(x===0) return 'empty'; if(x===1) return 'diatomic';
  if(x===2) return (e===0||e===3||e===4)?'linear':'bent';
  if(x===3) return ['trigonalPlanar','trigonalPyramidal','tShaped','tShaped'][e];
  if(x===4) return ['tetrahedral','seesaw','squarePlanar'][e];
  if(x===5) return ['trigonalBipyramidal','squarePyramidal'][e];
  return 'octahedral';
}
const EL_GEOM=['empty','diatomic','linear','trigonalPlanar','tetrahedral','trigonalBipyramidal','octahedral'];
const LABEL={empty:'',diatomic:'Linear',linear:'Linear',bent:'Bent',trigonalPlanar:'Trigonal Planar',
  trigonalPyramidal:'Trigonal Pyramidal',tShaped:'T-shaped',tetrahedral:'Tetrahedral',seesaw:'Seesaw',
  squarePlanar:'Square Planar',trigonalBipyramidal:'Trigonal Bipyramidal',squarePyramidal:'Square Pyramidal',octahedral:'Octahedral'};
function geomNames(x,e){ return {mol:LABEL[molGeometry(x,e)], el:LABEL[EL_GEOM[x+e]]}; }
/* the ideal bond angles a class inherits from its electron geometry (what rho = 1 gives) */
function idealBondAngles(x,e){ const n=x+e; if(x<2) return [];
  const S=SLOTS[n], out=[]; for(let i=e;i<n;i++) for(let j=i+1;j<n;j++) out.push(angleDeg(S[i],S[j])); return out.sort((a,b)=>a-b); }
function subN(k){ const D='₀₁₂₃₄₅₆₇₈₉'; return String(k).split('').map(c=>D[+c]).join(''); }
/* AX with the counts as subscripts; a central atom with no bonds is just A */
function axeName(x,e){ return (x?'AX'+(x!==1?subN(x):''):'A')+(e?'E'+(e>1?subN(e):''):''); }

/* ---- PhET's real molecules (RealMoleculeShape, build 1.6.19): the primary numbers
   verbatim (bond lengths in angstroms, the angles the constructor is given), the
   directions built from them as PhET's constructor builds them.  PhET's model notes:
   "Data is pulled from a mix of PubChem and/or reconstructed from the best known
   bond angles."  PhET draws every bond of a molecule at one length; so does this file. ---- */
const PHET_UP=-19.471220333;              /* PhET's value: its tetrahedron's elevation, degrees */
const PHET_NH3_POLAR=1.202623030417028;   /* PhET's value: NH3's H polar angle, radians (H-N-H = 107.8°) */
function phetTetra(){ const up=PHET_UP*DEG, v=[[0,0,1]];
  for(let k=0;k<3;k++){ const a=2*Math.PI*k/3; v.push([Math.cos(a)*Math.cos(up),Math.sin(a)*Math.cos(up),Math.sin(up)]); } return v; }
function realMolecules(){
  const t3=2*Math.PI/3, s=Math.sin, c=Math.cos, M={};
  const add=(id,centre,clp,L,outer,olp,order,bonds)=>{ M[id]={id,centre,clp,L,outer,olp,order,
    bonds:bonds.map(([v,l])=>({u:vnorm(v),L:l}))}; };
  add('BeCl2','Be',0,1.8,'Cl',3,1,[[[1,0,0],1.8],[[-1,0,0],1.8]]);
  add('BF3','B',0,1.313,'F',3,1,[0,1,2].map(k=>[[c(k*t3),s(k*t3),0],1.313]));
  let t=84.8*DEG;
  add('BrF5','Br',1,1.774,'F',3,1,[[[0,-1,0],1.689],[[s(t),-c(t),0],1.774],[[0,-c(t),s(t)],1.774],[[-s(t),-c(t),0],1.774],[[0,-c(t),-s(t)],1.774]]);
  add('CH4','C',0,1.087,'H',0,1,phetTetra().map(v=>[v,1.087]));
  t=87.5*DEG;
  add('ClF3','Cl',2,1.698,'F',3,1,[[[0,-1,0],1.598],[[s(t),-c(t),0],1.698],[[-s(t),-c(t),0],1.698]]);
  add('CO2','C',0,1.163,'O',2,2,[[[-1,0,0],1.163],[[1,0,0],1.163]]);
  t=104.5/2*DEG;
  add('H2O','O',2,0.957,'H',0,1,[[[s(t),-c(t),0],0.957],[[-s(t),-c(t),0],0.957]]);
  const th=PHET_NH3_POLAR;
  add('NH3','N',1,1.017,'H',0,1,[0,1,2].map(k=>[[s(th)*c(k*t3),-c(th),s(th)*s(k*t3)],1.017]));
  add('PCl5','P',0,2.02,'Cl',3,1,[[[1,0,0],2.14],[[-1,0,0],2.14]].concat([0,1,2].map(k=>[[0,c(k*t3),s(k*t3)],2.02])));
  const ta=173.1/2*DEG, te=101.6/2*DEG;
  add('SF4','S',1,1.595,'F',3,1,[[[s(ta),-c(ta),0],1.646],[[-s(ta),-c(ta),0],1.646],[[0,-c(te),s(te)],1.545],[[0,-c(te),-s(te)],1.545]]);
  add('SF6','S',0,1.564,'F',3,1,[[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]].map(v=>[v,1.564]));
  t=119/2*DEG;
  add('SO2','S',1,1.431,'O',2,2,[[[s(t),-c(t),0],1.431],[[-s(t),-c(t),0],1.431]]);
  add('XeF2','Xe',3,1.977,'F',3,1,[[[1,0,0],1.977],[[-1,0,0],1.977]]);
  add('XeF4','Xe',2,1.953,'F',3,1,[[[1,0,0],1.953],[[-1,0,0],1.953],[[0,0,1],1.953],[[0,0,-1],1.953]]);
  return M;
}
const REAL=realMolecules();
/* PhET's lists: the Real Molecules screen of Molecule Shapes, and of Molecule Shapes: Basics */
const FULL_LIST=['H2O','CO2','SO2','XeF2','BF3','ClF3','NH3','CH4','SF4','XeF4','BrF5','PCl5','SF6'];
const BASICS_LIST=['BeCl2','BF3','CH4','PCl5','SF6'];
/* PhET's molecules stand with their lone pairs up +y; the world here is z-up */
const PHET_TO_WORLD=[[1,0,0],[0,0,-1],[0,1,0]];
function formulaHTML(id){ return id.replace(/(\d)/g,'<sub>$1</sub>'); }
function formulaText(id){ return id.replace(/(\d)/g,d=>subN(+d)); }
/* a real molecule in world coordinates: bond directions, and its central lone pairs
   placed as PhET places them: the ideal bond slots Horn-fitted onto the real bonds
   (best assignment), the ideal lone-pair slots carried along by the same rotation */
const REALGEOM={};
function realGeometry(id){
  if(REALGEOM[id]) return REALGEOM[id];
  const m=REAL[id], x=m.bonds.length, e=m.clp, n=x+e;
  const B=m.bonds.map(b=>matVec(PHET_TO_WORLD,b.u));
  const Sb=SLOTS[n].slice(e), kb=B.map(()=>'b');
  const fit=fitAssign(Sb,kb,B,kb);
  const LP=[]; for(let k=0;k<e;k++) LP.push(vnorm(matVec(fit.R,SLOTS[n][k])));
  const ang=[]; for(let i=0;i<x;i++) for(let j=i+1;j<x;j++) ang.push(angleDeg(B[i],B[j]));
  return (REALGEOM[id]={id,x,e,B,LP,angles:ang.sort((a,b)=>a-b),fitRes:fit.res});
}
/* the model's version of the same molecule: the equilibrium of its class at rho,
   turned (best rotation and assignment) onto the real bonds */
function modelOfReal(id,rho){
  const g=realGeometry(id), x=g.x, e=g.e, eq=equilibrium(x,e,rho);
  const Eb=eq.U.slice(e), kb=g.B.map(()=>'b');
  const fit=fitAssign(Eb,kb,g.B,kb);
  const B=g.B.map((u,i)=>vnorm(matVec(fit.R,Eb[fit.sigma[i]])));
  const LP=[]; for(let k=0;k<e;k++) LP.push(vnorm(matVec(fit.R,eq.U[k])));
  const ang=[]; for(let i=0;i<x;i++) for(let j=i+1;j<x;j++) ang.push(angleDeg(B[i],B[j]));
  return {B,LP,angles:ang.sort((a,b)=>a-b),fitRes:fit.res};
}
/* distinct values of a sorted angle list (to 1e-6 deg), with their counts */
function distinctAngles(a,tol){ const t=tol||1e-6, out=[]; for(const v of a){ const d=out.find(o=>Math.abs(o.v-v)<t); if(d) d.n++; else out.push({v,n:1}); } return out; }
/* an outer atom's own lone pairs: the local geometry of one bond plus k pairs (steric
   number 1 + k), its last slot turned onto the bond back to the centre */
function outerLonePairs(u,k){
  if(!k) return [];
  const S=SLOTS[k+1], R=rotAtoB(S[k],[-u[0],-u[1],-u[2]]);
  const out=[]; for(let i=0;i<k;i++) out.push(vnorm(matVec(R,S[i])));
  return out;
}
