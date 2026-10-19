/* ================================================================== *
 *  the circuit: PhET's parts and values, the editor's graph            *
 *  operations, and the solver (modified nodal analysis)                *
 * ================================================================== */
/* PhET's values, read from its 1.5.2 build (CCKCConstants, Wire, Fuse,
   LightBulb, ResistorType, Battery, LinearTransientAnalysis, ChargeAnimator) */
const RHO_MIN=1e-10, RHO_MAX=0.0168;        /* wire resistivity range, ohm metres            */
const LEN_PER_UNIT=5e-4;                    /* metres of wire per view unit (Wire.update)    */
const WIRE_AREA=5e-4;                       /* m², WIRE_CROSS_SECTIONAL_AREA                 */
const MIN_WIRE_R=1e-14;                     /* MINIMUM_WIRE_RESISTANCE, ohm                  */
const MIN_R=1.1e-10;                        /* MINIMUM_RESISTANCE: what an exact 0 becomes   */
const BATT_R_MIN=1e-4, BATT_R_MAX=10;       /* battery internal resistance, ohm              */
const FUSE_K=0.06, FUSE_EPS=1e-6;           /* fuse R = 0.06/rating; trips above rating+1e-6 */
const FIRE_I=15, FIRE_R=1e-8;               /* fire: |I| >= 15 A through R >= 1e-8 ohm       */
const B_MULT=0.35, B_PMAX=2000;             /* bulb brightness ln(1+0.35P)/ln(1+0.35·2000)   */
const REAL_COLD=10;                         /* real bulb: 10 + 3|V|/log2(|V|+2)              */
const CHARGE_SEP=28, CHARGE_SPEED=25, CHARGE_FRAC=0.43;  /* units, units/s per A, per frame */
const SNAP_R=30, SOLDER_R=11.2, TAP_PX=15;  /* drop radius, probe-to-vertex radius, tap px   */
const I_READ_MAX=1e10, I_READ_SERIES=1e3;   /* ammeter readouts saturate here                */

/* the parts, in PhET's toolbox order, with PhET's lengths (view units), values,
   ranges and counts.  The bulbs' 100 units between terminals is the remake's:
   PhET's bulb has both terminals on its base. */
const TYPES={
  wire:     {L:0,   name:'wire',             max:50},
  battery:  {L:102, name:'battery',          max:10, E:9,    lo:0,   hi:120,    dp:1, step:0.1},
  bulb:     {L:100, name:'light bulb',       max:10, R:10,   lo:0,   hi:120,    dp:1, step:0.1},
  resistor: {L:110, name:'resistor',         max:10, R:10,   lo:0,   hi:120,    dp:1, step:0.1},
  switch:   {L:112, name:'switch',           max:10},
  fuse:     {L:110, name:'fuse',             max:10, rating:4, lo:0.5, hi:20,   dp:1, step:0.1},
  xbattery: {L:102, name:'extreme battery',  max:4,  E:1000, lo:100, hi:100000, dp:0, step:1},
  xbulb:    {L:100, name:'extreme bulb',     max:4,  R:1000, lo:100, hi:10000,  dp:0, step:1},
  xresistor:{L:110, name:'extreme resistor', max:4,  R:1000, lo:100, hi:10000,  dp:0, step:1},
  bill:     {L:140, name:'dollar bill',      max:1,  R:1e6},
  clip:     {L:75,  name:'paper clip',       max:1,  R:0},
  coin:     {L:85,  name:'coin',             max:1,  R:0},
  eraser:   {L:90,  name:'eraser',           max:1,  R:1e6},
  pencil:   {L:130, name:'pencil',           max:1,  R:25},
  tpencil:  {L:130, name:'thin pencil',      max:1,  R:50},
  rbulb:    {L:100, name:'real bulb',        max:10, R:10},
  ammeter:  {L:121, name:'series ammeter',   max:6,  R:0},
};
const TOOL_ORDER=['wire','battery','bulb','resistor','switch','fuse','xbattery','xbulb','xresistor',
                  'bill','clip','coin','eraser','pencil','tpencil','rbulb','ammeter'];
const isBattery=t=>t==='battery'||t==='xbattery';
const isBulb=t=>t==='bulb'||t==='xbulb'||t==='rbulb';
const isMetal=t=>t==='wire'||t==='coin'||t==='clip';
/* PhET's isFlammable: batteries and every Resistor (household objects are
   resistors); bulbs, wires, fuses, switches and ammeters never burn */
const isFlammable=t=>isBattery(t)||t==='resistor'||t==='xresistor'||t==='bill'||t==='clip'
  ||t==='coin'||t==='eraser'||t==='pencil'||t==='tpencil';
/* whose value the user can edit (PhET: resistors, bulbs, batteries, fuses) */
const isEditable=t=>t==='battery'||t==='xbattery'||t==='bulb'||t==='xbulb'||t==='resistor'||t==='xresistor'||t==='fuse';

function wireR(d,rho){ return Math.max(MIN_WIRE_R,rho*(LEN_PER_UNIT*d)/WIRE_AREA); }
function realBulbR(V){ const a=Math.abs(V); return REAL_COLD+3*a/(Math.log(a+2)/Math.log(2)); }
function brightnessOf(P){ const n=Math.log(1+Math.abs(P)*B_MULT), d=Math.log(1+B_PMAX*B_MULT);
  return clamp(d===0?0:n/d,0,1); }
/* PhET's lit-glass opacity: linear from 0 at brightness 0 to full at 0.5 */
function glowOf(b){ return clamp(2*b,0,1); }
function fuseR(rating){ return FUSE_K/rating; }

/* ---------------- the circuit as data ---------------- */
function newCircuit(){ return {verts:[],els:[],nv:0,ne:0}; }
function makeEl(id,type,a,b,par){
  const T=TYPES[type], el={id,type,a,b};
  if(T.E!==undefined) el.E=T.E;
  if(T.R!==undefined) el.R=T.R;
  if(type==='fuse'){ el.rating=T.rating; el.tripped=false; }
  if(type==='switch') el.closed=false;           /* PhET: a new switch is open */
  if(par) for(const k in par) el[k]=par[k];
  return el;
}
function presetCircuit(key){
  const C=newCircuit(), g=PRESET_GEOM[key];
  if(!g) return C;
  g.verts.forEach((p,k)=>C.verts.push({id:k,x:p[0],y:p[1]}));
  g.els.forEach((e,k)=>C.els.push(makeEl(k,e[0],e[1],e[2],e[3])));
  C.nv=g.verts.length; C.ne=g.els.length;
  return C;
}
function vById(C,id){ for(const v of C.verts) if(v.id===id) return v; return null; }
function elById(C,id){ for(const e of C.els) if(e.id===id) return e; return null; }
function elsAt(C,vid){ return C.els.filter(e=>e.a===vid||e.b===vid); }
function otherEnd(e,vid){ return e.a===vid?e.b:e.a; }
function elLength(C,e){ const A=vById(C,e.a), B=vById(C,e.b); return Math.hypot(B.x-A.x,B.y-A.y); }
function countType(C,t){ let n=0; for(const e of C.els) if(e.type===t) n++; return n; }
function remaining(C,t){ return TYPES[t].max-countType(C,t); }

/* a new part centred at (cx,cy), lying along +x (PhET's "right" orientation):
   start vertex on the left, end on the right -- for a battery the end is +. */
function addElement(C,type,cx,cy){
  if(remaining(C,type)<=0) return null;
  const L=TYPES[type].L||100;                    /* a new wire is 100 long (WIRE_LENGTH) */
  const a={id:C.nv++,x:cx-L/2,y:cy}, b={id:C.nv++,x:cx+L/2,y:cy};
  C.verts.push(a,b);
  const el=makeEl(C.ne++,type,a.id,b.id);
  C.els.push(el);
  return el;
}
/* every vertex joined to vid through FIXED-length parts (not wires): they
   move as one rigid body (PhET's findAllFixedVertices) */
function fixedGroup(C,vid){
  const seen=new Set([vid]), q=[vid];
  while(q.length){ const v=q.pop();
    for(const e of C.els) if(e.type!=='wire'&&(e.a===v||e.b===v)){ const o=otherEnd(e,v); if(!seen.has(o)){ seen.add(o); q.push(o); } } }
  return seen;
}
function neighbours(C,vid){ const s=new Set(); for(const e of C.els){ if(e.a===vid) s.add(e.b); else if(e.b===vid) s.add(e.a); } return s; }
function adjacent(C,v,t){ return C.els.some(e=>(e.a===v&&e.b===t)||(e.a===t&&e.b===v)); }
/* PhET's getDropTarget rules: not itself, not adjacent, not in the dragged
   rigid group, and the two may share no neighbour (that would lay two parts
   on top of each other between the same two points) */
function canConnect(C,v,t,group){
  if(v===t||adjacent(C,v,t)) return false;
  if(group&&group.has(t)) return false;
  if(fixedGroup(C,v).has(t)) return false;
  const nv=neighbours(C,v), nt=neighbours(C,t);
  for(const x of nv) if(nt.has(x)) return false;
  return true;
}
/* the nearest legal (moving vertex, target) pair within the 30-unit drop radius */
function dropTarget(C,moving){
  let best=null;
  const group=new Set(moving);
  for(const vid of moving){ const v=vById(C,vid); if(!v) continue;
    for(const t of C.verts){ if(group.has(t.id)) continue;
      const d=Math.hypot(t.x-v.x,t.y-v.y);
      if(d<SNAP_R&&(!best||d<best.d)&&canConnect(C,vid,t.id,group)) best={src:vid,dst:t.id,d}; } }
  return best;
}
function translateVerts(C,ids,dx,dy){ for(const v of C.verts) if(ids.has(v.id)){ v.x+=dx; v.y+=dy; } }
/* join src onto dst: src's rigid group is carried so that src lands exactly on
   dst, then every part that used src uses dst and src is gone */
function connect(C,src,dst){
  const s=vById(C,src), t=vById(C,dst);
  if(!s||!t) return false;
  translateVerts(C,fixedGroup(C,src),t.x-s.x,t.y-s.y);
  s.x=t.x; s.y=t.y;
  for(const e of C.els){ if(e.a===src) e.a=dst; if(e.b===src) e.b=dst; }
  C.verts=C.verts.filter(v=>v.id!==src);
  return true;
}
/* cut a junction: every part but the first gets its own new vertex, moved a
   little along the part, away from the junction (PhET's scissors button) */
const SPLIT_GAP=24;
function splitVertex(C,vid){
  const v=vById(C,vid), at=elsAt(C,vid);
  if(!v||at.length<2) return false;
  for(let k=1;k<at.length;k++){
    const e=at[k], o=vById(C,otherEnd(e,vid));
    const nv={id:C.nv++,x:v.x,y:v.y};
    C.verts.push(nv);
    if(e.a===vid) e.a=nv.id; else e.b=nv.id;
    const L=Math.hypot(o.x-v.x,o.y-v.y)||1, ux=(o.x-v.x)/L, uy=(o.y-v.y)/L;
    if(e.type==='wire'){ const g=Math.min(SPLIT_GAP,0.4*L); nv.x+=ux*g; nv.y+=uy*g; }
    else translateVerts(C,fixedGroup(C,nv.id),ux*SPLIT_GAP,uy*SPLIT_GAP);
  }
  return true;
}
/* remove a part; any vertex left attached to nothing goes with it */
function deleteElement(C,eid){
  const e=elById(C,eid); if(!e) return false;
  C.els=C.els.filter(x=>x.id!==eid);
  C.verts=C.verts.filter(v=>C.els.some(x=>x.a===v.id||x.b===v.id));
  return true;
}
function reverseBattery(C,eid){ const e=elById(C,eid); if(!e||!isBattery(e.type)) return false; const t=e.a; e.a=e.b; e.b=t; return true; }

/* ---------------- the netlist ---------------- */
/* one branch per traversable part: an open switch or a tripped fuse is not in
   the circuit at all (PhET's isTraversable).  realR freezes real bulbs. */
function netlistOf(C,glob,realR){
  const idx=new Map(); C.verts.forEach((v,k)=>idx.set(v.id,k));
  const br=[], off=[];
  for(const el of C.els){
    if((el.type==='switch'&&!el.closed)||(el.type==='fuse'&&el.tripped)){ off.push(el); continue; }
    let R=0, E=0, kind='R';
    if(isBattery(el.type)){ kind='B'; R=glob.rbat; E=el.E; }
    else if(el.type==='wire') R=wireR(elLength(C,el),glob.rho);
    else if(el.type==='fuse') R=fuseR(el.rating);
    else if(el.type==='switch') R=0;
    else if(el.type==='rbulb') R=realR&&realR.has(el.id)?realR.get(el.id):REAL_COLD;
    else R=el.R;
    if(!(R>0)) R=MIN_R;                          /* PhET: resistance || MINIMUM_RESISTANCE */
    br.push({a:idx.get(el.a),b:idx.get(el.b),R,E,kind,el});
  }
  return {N:C.verts.length,br,off,idx};
}

/* ---------------- dense linear algebra ---------------- */
/* Gaussian elimination with partial pivoting, then `refine` passes of
   iterative refinement against the untouched matrix */
function gaussSolve(A,z,refine){
  const n=z.length, M=A.map(r=>Float64Array.from(r)), b=Float64Array.from(z), perm=new Int32Array(n);
  for(let i=0;i<n;i++) perm[i]=i;
  for(let c=0;c<n;c++){
    let p=c, best=Math.abs(M[c][c]);
    for(let r=c+1;r<n;r++){ const a=Math.abs(M[r][c]); if(a>best){ best=a; p=r; } }
    if(best===0) throw new Error('singular circuit matrix at column '+c);
    if(p!==c){ const t=M[c]; M[c]=M[p]; M[p]=t; const u=perm[c]; perm[c]=perm[p]; perm[p]=u; }
    const piv=M[c][c], Rc=M[c];
    for(let r=c+1;r<n;r++){ const Rr=M[r], f=Rr[c]/piv; if(f===0) continue;
      Rr[c]=f; for(let k=c+1;k<n;k++) Rr[k]-=f*Rc[k]; }
  }
  const luSolve=rhs=>{ const y=new Float64Array(n);
    for(let i=0;i<n;i++){ let s=rhs[perm[i]]; const Ri=M[i]; for(let k=0;k<i;k++) s-=Ri[k]*y[k]; y[i]=s; }
    for(let i=n-1;i>=0;i--){ let s=y[i]; const Ri=M[i]; for(let k=i+1;k<n;k++) s-=Ri[k]*y[k]; y[i]=s/Ri[i]; }
    return y; };
  const x=luSolve(b);
  for(let it=0;it<(refine||0);it++){
    const r=new Float64Array(n);
    for(let i=0;i<n;i++){ let s=z[i]; const Ai=A[i]; for(let k=0;k<n;k++) s-=Ai[k]*x[k]; r[i]=s; }
    const d=luSolve(r); for(let i=0;i<n;i++) x[i]+=d[i];
  }
  return x;
}

/* ---------------- modified nodal analysis ---------------- */
/* Unknowns: the voltage of every node except one reference per connected
   piece, and the current of EVERY branch.  Rows: Kirchhoff's current law at
   each non-reference node, and each branch's own law
        v_a - v_b - R i = -E        (i flows a -> b through the part)
   divided by max(1,R) so no row carries a coefficient above 1.  A battery's
   EMF raises the potential from a (its - terminal) to b (+).  PhET keeps only
   the batteries' and the zero-resistance parts' currents as unknowns and
   gets every other current as (v_a - v_b)/R; keeping them all makes the
   current law a row of the system, so it closes to rounding error. */
function componentsOf(N,br){
  const par=new Int32Array(N); for(let q=0;q<N;q++) par[q]=q;
  const find=x=>{ while(par[x]!==x){ par[x]=par[par[x]]; x=par[x]; } return x; };
  for(const e of br){ const ra=find(e.a), rb=find(e.b); if(ra!==rb){ if(ra<rb) par[rb]=ra; else par[ra]=rb; } }
  const comp=new Int32Array(N); for(let q=0;q<N;q++) comp[q]=find(q);
  return comp;
}
/* each piece's 0 V: the - terminal of its first battery, else its first node */
function referencesOf(N,br,comp){
  const ref=new Map();
  for(const e of br) if(e.kind==='B'&&!ref.has(comp[e.a])) ref.set(comp[e.a],e.a);
  for(let q=0;q<N;q++) if(!ref.has(comp[q])) ref.set(comp[q],q);
  return ref;
}
function mnaSystem(N,br,opt){
  opt=opt||{};
  const B=br.length, comp=componentsOf(N,br), ref=referencesOf(N,br,comp);
  const isRef=new Uint8Array(N); for(const r of ref.values()) isRef[r]=1;
  const vi=new Int32Array(N).fill(-1); let nv=0;
  for(let q=0;q<N;q++) if(!isRef[q]) vi[q]=nv++;
  const n=nv+B, A=[], z=new Float64Array(n);
  for(let r=0;r<n;r++) A.push(new Float64Array(n));
  br.forEach((e,k)=>{ if(vi[e.a]>=0) A[vi[e.a]][nv+k]+=1; if(vi[e.b]>=0) A[vi[e.b]][nv+k]-=1; });
  if(opt.inj) for(const [node,J] of opt.inj) if(vi[node]>=0) z[vi[node]]+=J;
  br.forEach((e,k)=>{
    const r=nv+k, s=Math.max(1,e.R);
    const E=(opt.zeroE||(opt.only!==undefined&&e.kind==='B'&&k!==opt.only))?0:e.E;
    if(vi[e.a]>=0) A[r][vi[e.a]]+=1/s;
    if(vi[e.b]>=0) A[r][vi[e.b]]-=1/s;
    A[r][nv+k]-=e.R/s;
    z[r]=-E/s;
  });
  return {A,z,n,nv,vi,comp,ref,B};
}
function mnaSolve(N,br,opt){
  const S=mnaSystem(N,br,opt);
  const x=S.n?gaussSolve(S.A,S.z,2):new Float64Array(0);
  const v=new Float64Array(N), i=new Float64Array(S.B);
  for(let q=0;q<N;q++) v[q]=S.vi[q]>=0?x[S.vi[q]]:0;
  for(let k=0;k<S.B;k++) i[k]=x[S.nv+k];
  return {v,i,comp:S.comp,ref:S.ref,nv:S.nv,n:S.n};
}

/* PhET's own formulation, kept as an independent twin for the tests: every
   resistor stamped as a conductance, each battery an ideal source (current
   unknown) in series with its internal resistance through a synthetic node.
   Returns node voltages and currents (v_a - v_b + E)/R. */
function phetSolve(N,br){
  const comp=componentsOf(N,br), ref=referencesOf(N,br,comp);
  const bats=[]; br.forEach((e,k)=>{ if(e.kind==='B') bats.push(k); });
  const NN=N+bats.length;                              /* + one synthetic node per battery */
  const isRef=new Uint8Array(NN); for(const r of ref.values()) isRef[r]=1;
  const vi=new Int32Array(NN).fill(-1); let nv=0;
  for(let q=0;q<NN;q++) if(!isRef[q]) vi[q]=nv++;
  const n=nv+bats.length, A=[], z=new Float64Array(n);
  for(let r=0;r<n;r++) A.push(new Float64Array(n));
  const stampG=(p,q,G)=>{ if(vi[p]>=0){ A[vi[p]][vi[p]]+=G; if(vi[q]>=0) A[vi[p]][vi[q]]-=G; }
                          if(vi[q]>=0){ A[vi[q]][vi[q]]+=G; if(vi[p]>=0) A[vi[q]][vi[p]]-=G; } };
  br.forEach((e,k)=>{ if(e.kind!=='B') stampG(e.a,e.b,1/e.R); });
  bats.forEach((k,j)=>{ const e=br[k], s=N+j, col=nv+j;
    /* ideal source from a to s: v_s - v_a = E, its current j flows a -> s */
    if(vi[e.a]>=0) A[vi[e.a]][col]+=1;
    if(vi[s]>=0) A[vi[s]][col]-=1;
    if(vi[s]>=0) A[col][vi[s]]+=1;
    if(vi[e.a]>=0) A[col][vi[e.a]]-=1;
    z[col]=e.E;
    stampG(s,e.b,1/e.R); });
  const x=n?gaussSolve(A,z,2):new Float64Array(0);
  const v=new Float64Array(N); for(let q=0;q<N;q++) v[q]=vi[q]>=0?x[vi[q]]:0;
  const i=br.map(e=>(v[e.a]-v[e.b]+e.E)/e.R);
  return {v,i,comp,ref};
}

/* ---------------- Kirchhoff, checked on the answer ---------------- */
/* a spanning forest by breadth-first search; every other branch (a chord)
   closes exactly one loop: the fundamental loops, B - N + C of them */
function cycleBasis(N,br){
  const adj=[]; for(let q=0;q<N;q++) adj.push([]);
  br.forEach((e,k)=>{ adj[e.a].push([e.b,k]); adj[e.b].push([e.a,k]); });
  const par=new Int32Array(N).fill(-2), pk=new Int32Array(N).fill(-1), depth=new Int32Array(N), tree=new Uint8Array(br.length);
  for(let r=0;r<N;r++){ if(par[r]!==-2) continue; par[r]=-1; const q=[r];
    for(let h=0;h<q.length;h++){ const u=q[h];
      for(const [w,k] of adj[u]) if(par[w]===-2){ par[w]=u; pk[w]=k; depth[w]=depth[u]+1; tree[k]=1; q.push(w); } } }
  const loops=[];
  br.forEach((e,k)=>{ if(tree[k]) return;
    /* chord a -> b, then the tree path back from b to a; s = +1 when the loop
       runs through a branch from its a to its b */
    const up=[], down=[]; let x=e.b, y=e.a;
    while(depth[x]>depth[y]){ up.push(x); x=par[x]; }
    while(depth[y]>depth[x]){ down.push(y); y=par[y]; }
    while(x!==y){ up.push(x); x=par[x]; down.push(y); y=par[y]; }
    const L=[{k,s:1}];
    for(const u of up){ const kk=pk[u]; L.push({k:kk,s:br[kk].a===u?1:-1}); }
    for(let j=down.length-1;j>=0;j--){ const u=down[j], kk=pk[u]; L.push({k:kk,s:br[kk].b===u?1:-1}); }
    loops.push(L); });
  return {tree,loops,par,pk};
}
/* the law residuals of a solution, on the ANSWER (not assumed): the current
   law at every node and the voltage law round every fundamental loop, each
   part's drop taken from its own law R i - E.  Both are measured against the
   scale of the connected piece they sit in -- its largest current, its
   largest voltage, EMF or drop -- because that is the ruler rounding error
   is made on: a dangling part carrying 1e-30 A is not "100 % off", and a
   loop of 1e-10-ohm parts at 9 V cannot close better than 9 V's last bit. */
function kirchhoff(N,br,sol,basis){
  const comp=sol.comp, Isc=new Map(), Vsc=new Map();
  const up=(m,c,x)=>{ if(!(m.get(c)>=x)) m.set(c,x); };
  br.forEach((e,k)=>{ const c=comp[e.a]; up(Isc,c,Math.abs(sol.i[k])); up(Vsc,c,Math.max(Math.abs(e.E),Math.abs(e.R*sol.i[k]))); });
  for(let q=0;q<N;q++) up(Vsc,comp[q],Math.abs(sol.v[q]));
  const sum=new Float64Array(N);
  br.forEach((e,k)=>{ const c=sol.i[k]; sum[e.a]+=c; sum[e.b]-=c; });
  let kcl=0, kclAbs=0;
  for(let q=0;q<N;q++){ const s=Math.abs(sum[q]), m=Isc.get(comp[q])||0;
    kclAbs=Math.max(kclAbs,s); if(m>0) kcl=Math.max(kcl,s/m); else if(s>0) kcl=Infinity; }
  let kvl=0, kvlAbs=0; const per=[];
  for(const L of basis.loops){ let s=0;
    for(const {k,s:sg} of L){ const e=br[k]; s+=sg*(e.R*sol.i[k]-e.E); }
    const m=Vsc.get(comp[br[L[0].k].a])||0;
    per.push({sum:s,scale:m}); kvlAbs=Math.max(kvlAbs,Math.abs(s)); if(m>0) kvl=Math.max(kvl,Math.abs(s)/m); else if(s!==0) kvl=Infinity; }
  return {kcl,kclAbs,kvl,kvlAbs,node:sum,per,Isc,Vsc};
}

/* ---------------- the whole circuit, solved ---------------- */
/* Real bulbs are iterated to their fixed point (PhET stops after ten
   passes); a fuse carrying more than its rating trips and the circuit is
   solved again without it, until nothing more trips.  Tripping is a state
   change of the part, as in PhET: it stays blown until repaired. */
function solveCircuit(C,glob){
  const trips=[];
  for(let round=0;round<60;round++){
    const realR=new Map();
    let net=netlistOf(C,glob,realR), sol=mnaSolve(net.N,net.br), passes=0;
    const reals=[]; net.br.forEach((e,k)=>{ if(e.el.type==='rbulb') reals.push(k); });
    if(reals.length){
      for(passes=1;passes<=200;passes++){
        let dmax=0;
        for(const k of reals){ const e=net.br[k], Rn=realBulbR(sol.v[e.a]-sol.v[e.b]);
          dmax=Math.max(dmax,Math.abs(Rn-e.R)/Rn); realR.set(e.el.id,Rn); }
        net=netlistOf(C,glob,realR); sol=mnaSolve(net.N,net.br);
        if(dmax<=1e-14) break;
      }
    }
    let blew=false;
    net.br.forEach((e,k)=>{ if(e.el.type==='fuse'&&Math.abs(sol.i[k])>e.el.rating+FUSE_EPS){ e.el.tripped=true; blew=true; trips.push(e.el.id); } });
    if(!blew) return packSolution(C,glob,net,sol,passes,trips,realR);
  }
  throw new Error('fuses kept tripping');
}
function packSolution(C,glob,net,sol,passes,trips,realR){
  const V=new Map(), comp=new Map(), I=new Map(), R=new Map(), P=new Map(), bright=new Map(), fire=new Set(), onK=new Map();
  C.verts.forEach((v,k)=>{ V.set(v.id,sol.v[k]); comp.set(v.id,sol.comp[k]); });
  net.br.forEach((e,k)=>{ const c=sol.i[k]; I.set(e.el.id,c); R.set(e.el.id,e.R); onK.set(e.el.id,k);
    if(e.kind==='B'){ P.set(e.el.id,{emf:e.E*c,loss:c*c*e.R}); }
    else P.set(e.el.id,c*c*e.R);
    if(isBulb(e.el.type)) bright.set(e.el.id,brightnessOf(c*c*e.R));
    if(isFlammable(e.el.type)&&Math.abs(c)>=FIRE_I&&e.R>=FIRE_R) fire.add(e.el.id); });
  for(const el of net.off){ I.set(el.id,0); R.set(el.id,Infinity); P.set(el.id,0); if(isBulb(el.type)) bright.set(el.id,0); }
  const basis=cycleBasis(net.N,net.br), law=kirchhoff(net.N,net.br,sol,basis);
  const ncomp=new Set(sol.comp).size;
  let Imax=0; for(const c of sol.i) Imax=Math.max(Imax,Math.abs(c));
  return {V,comp,I,R,P,bright,fire,onK,net,sol,basis,law,passes,trips,realR,
    nodes:net.N,branches:net.br.length,comps:ncomp,loops:net.br.length-net.N+ncomp,Imax};
}

/* ---------------- what the meters read ---------------- */
function segDist(px,py,ax,ay,bx,by){
  const dx=bx-ax, dy=by-ay, L2=dx*dx+dy*dy;
  let t=L2>0?((px-ax)*dx+(py-ay)*dy)/L2:0; t=clamp(t,0,1);
  return {d:Math.hypot(px-ax-t*dx,py-ay-t*dy),t};
}
const METAL_HALF=9, SWITCH_HALF=13;
/* PhET's getVoltageConnection: a probe within the solder radius of a vertex
   reads that vertex; on a metal part (wire, coin, paper clip) it reads the
   voltage interpolated along the part; on a switch, the side it touches;
   anywhere else (a battery's or a resistor's body) nothing */
function probeConnection(C,SOL,x,y){
  let best=null;
  for(const v of C.verts){ const d=Math.hypot(v.x-x,v.y-y); if(d<=SOLDER_R&&(!best||d<best.d)) best={d,vid:v.id,V:SOL.V.get(v.id)}; }
  if(best) return best;
  for(const e of C.els){ if(!isMetal(e.type)) continue;
    const A=vById(C,e.a), B=vById(C,e.b), s=segDist(x,y,A.x,A.y,B.x,B.y);
    if(s.d<=METAL_HALF) return {d:s.d,vid:e.a,el:e.id,t:s.t,V:lerp(SOL.V.get(e.a),SOL.V.get(e.b),s.t)}; }
  for(const e of C.els){ if(e.type!=='switch') continue;
    const A=vById(C,e.a), B=vById(C,e.b), s=segDist(x,y,A.x,A.y,B.x,B.y);
    if(s.d<=SWITCH_HALF){ const vid=s.t<0.5?e.a:e.b; return {d:s.d,vid,el:e.id,V:SOL.V.get(vid)}; } }
  return null;
}
/* the voltmeter: red minus black, and only when the two probes touch parts of
   one connected circuit (PhET's areVerticesElectricallyConnected) */
function voltmeterReading(C,SOL,red,black){
  const r=probeConnection(C,SOL,red[0],red[1]), b=probeConnection(C,SOL,black[0],black[1]);
  if(!r||!b) return {V:null,r,b};
  if(SOL.comp.get(r.vid)!==SOL.comp.get(b.vid)) return {V:null,r,b,apart:true};
  return {V:r.V-b.V,r,b};
}
/* the non-contact ammeter reads the current of the part under its ring:
   fixed parts first, then wires (PhET's getCurrent) */
const RING_HALF=14;
function ammeterReading(C,SOL,x,y){
  for(const wantWire of [false,true]){
    let hit=null;
    for(const e of C.els){ if((e.type==='wire')!==wantWire) continue;
      const A=vById(C,e.a), B=vById(C,e.b), s=segDist(x,y,A.x,A.y,B.x,B.y);
      if(s.d<=RING_HALF&&(!hit||s.d<hit.d)) hit={d:s.d,el:e.id}; }
    if(hit) return {el:hit.el,I:SOL.I.get(hit.el)};
  }
  return null;
}
/* a series ammeter reads only when both of its ends are joined to something */
function seriesReading(C,SOL,e){
  if(elsAt(C,e.a).length<2||elsAt(C,e.b).length<2) return null;
  return SOL.I.get(e.id);
}
function currentText(I,series){
  if(I===null||I===undefined||!isFinite(I)) return '—';
  const cap=series?I_READ_SERIES:I_READ_MAX;
  if(Math.abs(I)>cap) return '> 10^'+(series?3:10);
  return Math.abs(I).toFixed(2)+' A';       /* PhET: magnitude, METER_PRECISION = 2 */
}
function voltageText(V){ return V===null||V===undefined||!isFinite(V)?'—':V.toFixed(2)+' V'; }

/* ---------------- the rest of the circuit, seen from one part ---------------- */
/* V_oc: the voltage (v_a - v_b) the rest makes across the part's terminals
   with the part taken out; R_th: the voltage per ampere pushed in at a and
   drawn out at b with every EMF zeroed.  Real bulbs elsewhere are frozen at
   their present resistance (a non-linear part has no Thevenin equivalent;
   this is its tangent at the operating point). */
function theveninOf(SOL,eid){
  const k=SOL.onK.get(eid); if(k===undefined) return null;
  const br=SOL.net.br, e=br[k], rest=br.slice(0,k).concat(br.slice(k+1)), N=SOL.net.N;
  const comp=componentsOf(N,rest);
  if(comp[e.a]!==comp[e.b]) return {open:true,e,k};
  const s1=mnaSolve(N,rest), Voc=s1.v[e.a]-s1.v[e.b];
  const s2=mnaSolve(N,rest,{inj:[[e.a,1],[e.b,-1]],zeroE:true}), Rth=s2.v[e.a]-s2.v[e.b];
  return {open:false,e,k,Voc,Rth,E:e.E,R:e.R,i:SOL.sol.i[k]};
}
/* superposition: each battery alone, the others' EMFs zeroed and their
   internal resistances kept */
function superpose(SOL){
  const br=SOL.net.br, N=SOL.net.N, bats=[];
  br.forEach((e,k)=>{ if(e.kind==='B') bats.push(k); });
  const parts=bats.map(kb=>mnaSolve(N,br,{only:kb}).i);
  return {bats,parts};
}

/* ---------------- the charges ---------------- */
/* PhET's layoutCharges: ceil((L-28)/28) charges evenly from 14 to L-14
   (one in the middle when that is one or none) */
function chargeLayout(L){
  const s=L-CHARGE_SEP, o=Math.ceil(s/CHARGE_SEP);
  if(o<=1) return [L/2];
  const a=s/(o-1), out=[];
  for(let l=0;l<o;l++) out.push(14+l*a);
  return out;
}
/* where a part's charges sit, along it from its start: the layout slid by
   the part's phase -- forwards for conventional (positive) charge, backwards
   for electrons, which drift against the current -- and wrapped round */
function chargePositions(L,phase,carrier){
  const ph=carrier==='electrons'?-phase:phase;
  return chargeLayout(L).map(p0=>((p0+ph)%L+L)%L);
}
/* the animation slows when the largest current would move a charge more than
   0.43 of the charge spacing in a 1/30-s frame (PhET's speed limit) */
function chargeScale(Imax){ const n=CHARGE_SPEED*Imax/30, cap=CHARGE_FRAC*CHARGE_SEP; return n>=cap?cap/n:1; }
