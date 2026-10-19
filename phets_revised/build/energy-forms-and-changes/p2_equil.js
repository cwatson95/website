
/* ================================================================== *
 *  equilibrium: one pair of bodies in contact, PhET's stepped model   *
 *  against the exact solution of the linear pair-and-room system      *
 * ================================================================== */
/* body 1 is always a block, started hot; body 2 is its partner */
const EQ_PAIRS=[{id:'iron-water',name:'iron in water',b1:0,b2:2,how:'in'},{id:'brick-water',name:'brick in water',b1:1,b2:2,how:'in'},
                {id:'iron-oil',name:'iron in oil',b1:0,b2:3,how:'in'},{id:'brick-iron',name:'brick on iron',b1:0,b2:1,how:'on'},
                {id:'water-iron',name:'water on iron',b1:0,b2:2,how:'under'}];
const EQ_MATS=[{id:'phet',name:'PhET’s materials'},{id:'real',name:'real materials'}];
function eqPair(id){ return EQ_PAIRS.find(p=>p.id===id); }
/* the two bodies, placed as the bench would place them: a block 1 mm inside a
   beaker, a block on a block, a beaker on a block (all on the ground) */
function eqBodies(pairId,T1,T2,mats){
  const P=eqPair(pairId), M=mats==='real'?MAT_REAL:MAT_PHET;
  const a=makeBody(P.b1,M), b=makeBody(P.b2,M);
  a.x=SPOTS[4]; b.x=SPOTS[4];            /* the water beaker's home spot, as in derive.py */
  if(P.how==='in'){ b.y=0; a.y=0.001; }
  else { a.y=0; b.y=BLOCK; }
  a.E=a.m*a.c*T1; b.E=b.m*b.c*T2;
  return [a,b];
}
/* PhET's step on just these two: displacement, the pair (block first), then
   the room for whichever is not immersed */
function eqStepOnce(bodies,air){
  const [a,b]=bodies;
  if(b.kind==='beaker'){
    const fx0=b.x-b.w/2, fx1=fx0+b.w, fy0=b.y, fy1=fy0+b.h*b.f, bb=bodyBounds(a);
    const ix0=Math.max(bb.x0,fx0), ix1=Math.min(bb.x1,fx1), iy0=Math.max(bb.y0,fy0), iy1=Math.min(bb.y1,fy1);
    const area=(ix1-ix0>=0&&iy1-iy0>=0)?(ix1-ix0)*(iy1-iy0):0;
    b.f=Math.min(FLUID0+DISPLACE*area,1);
  }
  exchange(a,b,DT);
  let room=0;
  if(air) for(const x of bodies) if(!isImmersed(bodies,x)) room+=airExchange(x,DT);
  return room;
}
/* the linear system C T' = -K T + a T_air, its conductances read off the geometry
   AFTER the displacement has settled (the stepped run settles it in one step) */
function eqLinear(pairId,T1,T2,mats,air){
  const bodies=eqBodies(pairId,T1,T2,mats);
  const [a,b]=bodies;
  /* a block 1 mm up in a half-full beaker is wholly under: one update gives 0.5 + 120 x 0.045^2 */
  if(b.kind==='beaker'&&eqPair(pairId).how==='in') b.f=Math.min(FLUID0+DISPLACE*BLOCK*BLOCK,1);
  const G=K_BODY*contactLen(bodyArea(a),bodyArea(b));
  const imm=isImmersed(bodies,a);
  const a1=air&&!imm?K_AIR*contactLen(AIR_AREA,bodyArea(a)):0, a2=air?K_AIR*contactLen(AIR_AREA,bodyArea(b)):0;
  const C1=a.m*a.c, C2=b.m*b.c;
  const M=[[-(G+a1)/C1,G/C1],[G/C2,-(G+a2)/C2]];
  const Teq=(C1*T1+C2*T2)/(C1+C2);
  const Tss=(a1+a2)>0?[T_AIR,T_AIR]:[Teq,Teq];
  /* the conserved mean with the room shut out: T_eq = (C1 T1 + C2 T2)/(C1 + C2) */
  return {G,a1,a2,C1,C2,M,Teq,Tss,T0:[T1,T2],tau:1/(G*(1/C1+1/C2)),cap1:bodyCap(a),cap2:bodyCap(b),imm};
}
/* exp(Mt) for a 2x2 matrix with real eigenvalues (M = C^-1 K, K symmetric):
   e^{st}[cosh(qt) I + sinh(qt)/q (M - sI)], s = tr/2, q = sqrt(s^2 - det) */
function expm2(M,t){
  const s=(M[0][0]+M[1][1])/2, det=M[0][0]*M[1][1]-M[0][1]*M[1][0], q2=s*s-det;
  const q=Math.sqrt(Math.max(q2,0)), e=Math.exp(s*t), ch=Math.cosh(q*t);
  const sh=q>1e-300?Math.sinh(q*t)/q:t;
  return [[e*(ch+sh*(M[0][0]-s)),e*sh*M[0][1]],[e*sh*M[1][0],e*(ch+sh*(M[1][1]-s))]];
}
function eqEigen(M){
  const s=(M[0][0]+M[1][1])/2, det=M[0][0]*M[1][1]-M[0][1]*M[1][0], q=Math.sqrt(Math.max(s*s-det,0));
  return [s+q,s-q];
}
function eqExact(L,t){
  const E=expm2(L.M,t), u0=[L.T0[0]-L.Tss[0],L.T0[1]-L.Tss[1]];
  return [L.Tss[0]+E[0][0]*u0[0]+E[0][1]*u0[1], L.Tss[1]+E[1][0]*u0[0]+E[1][1]*u0[1]];
}
/* the whole run the view draws: n steps of PhET's model, and the exact
   solution at the same instants, up to the first cap (past it the linear
   solution no longer applies: a beaker boils, a block reaches 620 K) */
function eqRun(pairId,T1,T2,mats,air,tWin){
  const L=eqLinear(pairId,T1,T2,mats,air), bodies=eqBodies(pairId,T1,T2,mats);
  const n=Math.max(2,Math.round(tWin/DT));
  const t=[0], s1=[bodyT(bodies[0])], s2=[bodyT(bodies[1])], x1=[T1], x2=[T2];
  let tCap=null, room=0, E0=bodies[0].E+bodies[1].E;
  for(let k=1;k<=n;k++){
    room+=eqStepOnce(bodies,air);
    t.push(k*DT); s1.push(bodyT(bodies[0])); s2.push(bodyT(bodies[1]));
    const ex=eqExact(L,k*DT); x1.push(ex[0]); x2.push(ex[1]);
    if(tCap===null&&(bodyTraw(bodies[0])>=L.cap1-1e-9||bodyTraw(bodies[1])>=L.cap2-1e-9||bodyBeyond(bodies[0])>0||bodyBeyond(bodies[1])>0)) tCap=k*DT;
  }
  const E1=bodies[0].E+bodies[1].E;
  return {L,t,s1,s2,x1,x2,tCap,resid:E1-E0+room,room,bodies};
}
function eqWindow(L){ const ev=eqEigen(L.M), fast=-1/ev[1]; return Math.min(Math.max(8*fast,4),60); }
