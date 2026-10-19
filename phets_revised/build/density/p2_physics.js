/* ================================================================== *
 *  the physics — the pool, Archimedes on a cube, the pressure on the  *
 *  faces, and PhET's measured data.  Nothing here touches a canvas.   *
 *  y is UP in every world coordinate; the views flip.                 *
 *  build/density/derive.py is the Python twin of every function here. *
 * ================================================================== */
const DEG=PI/180;                 /* multiply DEGREES by this to get radians (asserted: 90 DEG = pi/2) */
const G=9.8;                      /* PhET's gEarth, m/s^2 (standard gravity is 9.80665) */
const G_STD=9.80665;
const LITERS=1000;                /* litres in a cubic metre — PhET's LITERS_IN_CUBIC_METER */

/* PhET's pool: Bounds3(-0.45, -0.15/0.9/0.4, -0.2, 0.45, 0, 0.2), read out of
   density_en.html.  y = 0 is ground level and the floor is at -POOL_H; the
   expressions are PhET's own, so the arithmetic rounds identically. */
const POOL_W=0.9, POOL_D=0.4, POOL_H=0.15/0.9/0.4;
const A_POOL=POOL_W*POOL_D;                 /* 0.36 m^2 of free surface */
const V_POOL=A_POOL*POOL_H;                 /* 0.15 m^3 = 150 L */
const VF0=0.1;                              /* PhET's DESIRED_STARTING_POOL_VOLUME, m^3 */
/* PhET's scale: SCALE_WIDTH 0.15, SCALE_HEIGHT 0.06, 0.2 deep -> 1.8 L displaced */
const SCALE_W=0.15, SCALE_H=0.06, SCALE_D=0.2, SCALE_V=SCALE_W*SCALE_H*SCALE_D;
/* PhET's cube limits: MIN_VOLUME 0.001, MAX_VOLUME 0.01 m^3; mass 0.1-27 kg */
const VMIN_L=1, VMAX_L=10, MMIN=0.1, MMAX=27, MMIN_CUSTOM=0.5;

/* --------------------------------------------------------------------------
   PhET's material densities, kg/m^3, read out of density_en.html (Material.js)
   — "phet" — beside the handbook value from Wikipedia's "Densities of various
   materials" table, fetched 2026-09-21 — "ref".  ref:null means that table
   carries no row for the material at all, which is said rather than guessed.
   note: where PhET's number is a teaching choice rather than a measurement.
   -------------------------------------------------------------------------- */
const MATERIALS=[
  {id:'styrofoam',name:'styrofoam', phet:150,   ref:75,     col:'#e4e7ee', note:'real expanded polystyrene is nearer 75'},
  {id:'wood',     name:'wood',      phet:400,   ref:700,    col:'#a97c4a', note:'400 is pine (373); seasoned wood is 700'},
  {id:'apple',    name:'apple',     phet:832,   ref:null,   col:'#c0452f', note:null},
  {id:'ice',      name:'ice',       phet:919,   ref:916.7,  col:'#bfe3ff', note:null},
  {id:'human',    name:'human',     phet:950,   ref:null,   col:'#d8a184', note:null},
  {id:'water',    name:'water',     phet:1000,  ref:1000,   col:'#4d8fb8', note:null},
  {id:'seawater', name:'seawater',  phet:1029,  ref:1030,   col:'#2f7f96', note:null},
  {id:'pvc',      name:'PVC',       phet:1440,  ref:1175,   col:'#d3d6dc', note:'1175 is Wikipedia’s generic plastic'},
  {id:'honey',    name:'honey',     phet:1440,  ref:null,   col:'#c98b1d', note:null},
  {id:'sand',     name:'sand',      phet:1442,  ref:1600,   col:'#c7b083', note:null},
  {id:'brick',    name:'brick',     phet:2000,  ref:null,   col:'#9c4b34', note:null},
  {id:'aluminum', name:'aluminium', phet:2700,  ref:2700,   col:'#b9bec9', note:null},
  {id:'glass',    name:'glass',     phet:2700,  ref:2500,   col:'#9fd2d8', note:'PhET reuses aluminium’s 2700'},
  {id:'concrete', name:'concrete',  phet:3150,  ref:2400,   col:'#8d8f93', note:'ordinary concrete is 2400'},
  {id:'diamond',  name:'diamond',   phet:3510,  ref:3500,   col:'#dff3ff', note:null},
  {id:'titanium', name:'titanium',  phet:4500,  ref:4540,   col:'#8d949e', note:null},
  {id:'pyrite',   name:'pyrite',    phet:5010,  ref:null,   col:'#c5a94e', note:null},
  {id:'steel',    name:'steel',     phet:7800,  ref:7850,   col:'#8e939c', note:null},
  {id:'copper',   name:'copper',    phet:8960,  ref:8940,   col:'#c47a45', note:null},
  {id:'silver',   name:'silver',    phet:10490, ref:10500,  col:'#c8ccd6', note:null},
  {id:'lead',     name:'lead',      phet:11342, ref:11340,  col:'#6f7683', note:null},
  {id:'mercury',  name:'mercury',   phet:13593, ref:13546,  col:'#b0b6c2', note:null},
  {id:'tantalum', name:'tantalum',  phet:16650, ref:16600,  col:'#7e8590', note:null},
  {id:'gold',     name:'gold',      phet:19320, ref:19320,  col:'#d9b44a', note:null},
  {id:'platinum', name:'platinum',  phet:21450, ref:21450,  col:'#cfd4de', note:null},
  {id:'gasoline', name:'gasoline',  phet:680,   ref:null,   col:'#d8c65a', note:null},
  {id:'oil',      name:'oil',       phet:920,   ref:920,    col:'#a08a3a', note:null},
  {id:'air',      name:'air',       phet:1.2,   ref:1.2,    col:'#2a3346', note:null},
];
const MAT={}; MATERIALS.forEach(m=>{ MAT[m.id]=m; });
function matRho(id,custom){ if(id==='custom') return custom; const m=MAT[id]; if(!m) throw new Error('unknown material '+id); return m.phet; }
function matName(id){ return id==='custom'?'custom':MAT[id].name; }
function matColor(id,custom){
  if(id!=='custom') return MAT[id].col;
  /* PhET shades its custom material from black to white by density; keep the
     same idea on a cyan-to-white ramp so it never collides with a real one */
  const t=clamp((Math.log(custom/100)/Math.log(200)),0,1);
  return mix('#3d5d75','#e8eef5',t);
}
/* PhET's Intro/Explore material list (SIMPLE_MASS_MATERIALS + custom) */
const SIMPLE_MATS=['styrofoam','wood','ice','pvc','brick','aluminum'];
/* PhET's Density Mystery density table (DENSITY_MYSTERY_SCREEN_MATERIALS) */
const DENSITY_TABLE=['wood','gasoline','apple','ice','human','water','glass',
                     'diamond','titanium','steel','copper','lead','gold'];
/* PhET's Buoyancy fluid list (BUOYANCY_FLUID_MATERIALS) */
const BUOY_FLUIDS=['gasoline','oil','water','seawater','honey','mercury'];

/* ------------------------------------------------------------------ the cube */
function cubeSide(V){ return Math.pow(V,1/3); }        /* PhET's Cube.boundsFromVolume */
/* the volume of a cube of volume V, bottom at yb, lying below yw.  Saturates at
   V EXACTLY, not at s^3: s = V^(1/3) is inexact in binary, and s*s*s misses V
   by an ulp, which shows up as a submerged fraction of 1.0000000000000004. */
function cubeBelow(V,yb,yw){
  const s=cubeSide(V);
  if(yw>=yb+s) return V;
  if(yw<=yb) return 0;
  return s*s*(yw-yb);
}

/* ------------------------------------------------------------- the free surface
   A block is in one of four states at a trial surface yw:
     held   the user holds it, its bottom pinned (never below its support)
     float  rho_b < rho_f AND the floating draft clears its support
     rest   sitting on its support (the pool floor, or the pool scale)
     out    not in the pool at all
   The switch between float and rest is continuous: at the moment the floating
   draft just reaches the support, s^2 d = V rho_b/rho_f, the two agree. */
function blockState(b,yw,rhoF){
  const s=cubeSide(b.V);
  if(b.inPool===false) return {Vsub:0,yb:(b.yb===undefined?0:b.yb),mode:'out',s:s};
  const sup=(b.support===undefined?-POOL_H:b.support);
  if(b.held!==undefined&&b.held!==null){
    const yb=Math.max(b.held,sup);
    return {Vsub:cubeBelow(b.V,yb,yw),yb:yb,mode:'held',s:s};
  }
  if(b.rho<rhoF){
    const d=s*b.rho/rhoF, yb=yw-d;
    if(yb>=sup) return {Vsub:b.V*b.rho/rhoF,yb:yb,mode:'float',s:s};
  }
  return {Vsub:cubeBelow(b.V,sup,yw),yb:sup,mode:'rest',s:s};
}
function obstacleVolume(obs,yw){
  let t=0;
  for(const o of obs) t+=o.a*clamp(yw-o.y0,0,o.h);
  return t;
}
/* G(yw) = (pool volume below yw) - (every solid below yw).  Non-decreasing
   wherever the blocked plan area stays below A_POOL; selfTest sweeps it. */
function netFluid(yw,blocks,obs,rhoF){
  let t=A_POOL*Math.max(0,yw+POOL_H);
  for(const b of blocks) t-=blockState(b,yw,rhoF).Vsub;
  return t-obstacleVolume(obs,yw);
}
/* the SMALLEST yw with G(yw) >= Vf.  The infimum is the physics: a body that
   spans the pool's cross-section makes G flat, and the surface then sits at the
   bottom of the flat stretch with the surplus fluid above the body, not inside
   it.  Bisection keeps the invariant G(lo) < Vf <= G(hi). */
function poolLevel(blocks,obs,rhoF,Vf,nit){
  let sumV=0; for(const b of blocks) sumV+=b.V;
  let lo=-POOL_H, hi=-POOL_H+(Vf+sumV+obstacleVolume(obs,1e9))/A_POOL+1;
  const n=nit||80;
  for(let i=0;i<n;i++){
    const mid=0.5*(lo+hi);
    if(netFluid(mid,blocks,obs,rhoF)<Vf) lo=mid; else hi=mid;
  }
  return 0.5*(lo+hi);
}
/* the whole configuration: the level, then every block's state and forces */
function solvePool(blocks,rhoF,obs,Vf){
  obs=obs||[]; Vf=(Vf===undefined?VF0:Vf);
  const yw=poolLevel(blocks,obs,rhoF,Vf);
  const out={yw:yw,rhoF:rhoF,blocks:[]};
  for(const b of blocks){
    const st=blockState(b,yw,rhoF), m=b.rho*b.V, W=m*G, Fb=rhoF*G*st.Vsub;
    /* no clamp: a block only ever rests when the upthrust cannot lift it, so
       W - Fb >= 0 is a property of the solve rather than something to enforce.
       A Math.max(0, .) here was provably unreachable — dead code that mutation
       testing correctly reported as an equivalent mutant — and selfTest now
       sweeps the property instead. */
    const N=(st.mode==='rest')?(W-Fb):0;
    const hand=(st.mode==='held')?(W-Fb):0;
    out.blocks.push({V:b.V,rho:b.rho,s:st.s,m:m,Vsub:st.Vsub,yb:st.yb,mode:st.mode,
                     W:W,Fb:Fb,N:N,hand:hand,frac:st.Vsub/b.V,
                     x:(b.x===undefined?0:b.x),tag:b.tag,mat:b.mat,col:b.col});
  }
  return out;
}

/* --------------------------------------------------- Archimedes, closed form */
function floatDraft(V,rho,rhoF){ return cubeSide(V)*rho/rhoF; }    /* d = s rho_b/rho_f */
function submergedFraction(rho,rhoF){ return Math.min(1,rho/rhoF); }
function apparentWeight(V,rho,rhoF,Vsub){ return rho*V*G-rhoF*G*(Vsub===undefined?V:Vsub); }
function riseFloating(m,rhoF){ return m/(rhoF*A_POOL); }           /* its own MASS / (rho_f A) */
function riseSunk(V){ return V/A_POOL; }                           /* its own VOLUME / A */

/* ------------------------------------- the force, from the pressure on the faces
   p = rho g (yw - y), gauge (PhET ignores air buoyancy: the "vacuum
   assumption" of its model.md).  The bottom face pushes up, the top face down,
   and the four side faces cancel in pairs.  Returned per face so a view can
   draw them. */
function cubeFaceForces(V,yb,yw,rhoF){
  const s=cubeSide(V), yt=yb+s, A=s*s;
  const pBot=yb<yw?rhoF*G*(yw-yb):0, pTop=yt<yw?rhoF*G*(yw-yt):0;
  /* one side face: p integrated over the submerged strip, exact (p is linear) */
  const yl=Math.min(yw,yt), dsub=Math.max(0,yl-yb);
  const side=rhoF*G*(yw-0.5*(yb+yl))*s*dsub;
  return {pBot:pBot,pTop:pTop,A:A,Fbot:pBot*A,Ftop:pTop*A,net:(pBot-pTop)*A,
          side:side,sideSum:side-side,dBot:Math.max(0,yw-yb),dTop:Math.max(0,yw-yt)};
}
/* --- the 2-D route: the same force taken edge by edge round the polygon ------
   (the closed forms are build_buoy/p2_physics.js's, reused here) */
function clipBelow(poly,w){
  const out=[], n=poly.length;
  for(let i=0;i<n;i++){
    const a=poly[i], b=poly[(i+1)%n], ain=a[1]<=w, bin=b[1]<=w;
    if(ain) out.push([a[0],a[1]]);
    if(ain!==bin){ const t=(w-a[1])/(b[1]-a[1]); out.push([a[0]+(b[0]-a[0])*t,w]); }
  }
  return out;
}
function polyArea(poly){ let s=0; const n=poly.length;
  for(let i=0;i<n;i++){ const a=poly[i], b=poly[(i+1)%n]; s+=a[0]*b[1]-b[0]*a[1]; } return 0.5*s; }
function polyCentroid(poly){
  const A=polyArea(poly); if(Math.abs(A)<1e-300) return [0,0];
  let cx=0, cy=0; const n=poly.length;
  for(let i=0;i<n;i++){ const a=poly[i], b=poly[(i+1)%n], cr=a[0]*b[1]-b[0]*a[1]; cx+=(a[0]+b[0])*cr; cy+=(a[1]+b[1])*cr; }
  return [cx/(6*A),cy/(6*A)];
}
/* p is linear along a straight edge, so the edge force is p(mid) L exactly; the
   outward normal of a CCW edge (dx, dy) is (dy, -dx)/L and the fluid pushes
   inward, F = -p n L.  Per unit depth. */
function edgeForces(sub,w,rhoF){
  const n=sub.length, F=[], tot=[0,0];
  for(let i=0;i<n;i++){
    const a=sub[i], b=sub[(i+1)%n], dx=b[0]-a[0], dy=b[1]-a[1];
    const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2], p=rhoF*G*(w-mid[1]);
    const fx=-p*dy, fy=p*dx;
    F.push({fx:fx,fy:fy,a:a,b:b,p:p}); tot[0]+=fx; tot[1]+=fy;
  }
  return {F:F,tot:tot};
}
/* the independent route the tests use: subdivide every edge and sum p n ds */
function finePerimeter(poly,w,rhoF,nsub){
  nsub=nsub||2000; const tot=[0,0], n=poly.length;
  for(let i=0;i<n;i++){ const a=poly[i], b=poly[(i+1)%n], dx=b[0]-a[0], dy=b[1]-a[1];
    for(let k=0;k<nsub;k++){ const t=(k+0.5)/nsub, y=a[1]+dy*t, p=rhoF*G*Math.max(0,w-y);
      tot[0]+=-p*dy/nsub; tot[1]+=p*dx/nsub; } }
  return tot;
}
function cubePoly(V,yb,xc){
  const s=cubeSide(V), x=(xc===undefined?0:xc);
  return [[x-s/2,yb],[x+s/2,yb],[x+s/2,yb+s],[x-s/2,yb+s]];
}

/* ------------------------------------------------------------ PhET's screens */
/* Density, Compare screen (DensityCompareModel): four cubes, and the matched
   quantity on a slider.  Volumes and masses are PhET's own cubesData. */
const DENS_CUBES=[
  {tag:'B',tagV:'A',tagD:'B',mv:0.01,   vm:8,dv:0.006,col:'#d8c14a'},
  {tag:'A',tagV:'C',tagD:'A',mv:0.005,  vm:6,dv:0.004,col:'#4f8fd0'},
  {tag:'C',tagV:'D',tagD:'C',mv:0.0025, vm:4,dv:0.002,col:'#6fbf5a'},
  {tag:'D',tagV:'B',tagD:'D',mv:0.00125,vm:2,dv:0.001,col:'#d05a4f'},
];
const DENS_SAME_MASS=5, DENS_SAME_VOL=0.005, DENS_SAME_RHO=500;
const DENS_MASS_RANGE=[1,10], DENS_VOL_RANGE=[0.001,0.01], DENS_RHO_RANGE=[100,2000];
/* Buoyancy: Basics, Compare screen (BuoyancyCompareModel): two cubes, brick and
   wood, same mass 4 kg, same density 400 = PhET's WOOD */
const BB_CUBES=[
  {tag:'A',tagV:'A',tagD:'A',mv:0.002,vm:10,dv:0.005,col:'#c08a3c'},
  {tag:'B',tagV:'B',tagD:'B',mv:0.01, vm:2, dv:0.01, col:'#4f8fd0'},
];
const BB_SAME_MASS=4, BB_SAME_VOL=0.005, BB_SAME_RHO=400;
const BB_RHO_RANGE=[100,3000];

/* one set of compare blocks at the current slider values */
function compareBlocks(cubes,mode,mass,volM3,rho){
  return cubes.map((c,i)=>{
    if(mode==='mass')   return {tag:c.tag, V:c.mv,  rho:mass/c.mv,        col:c.col,idx:i};
    if(mode==='volume') return {tag:c.tagV,V:volM3, rho:c.vm/volM3,       col:c.col,idx:i};
    return                     {tag:c.tagD,V:c.dv,  rho:rho,              col:c.col,idx:i};
  });
}

/* Density, Mystery screen: PhET's three fixed sets.  'V' rows are built from a
   volume, 'M' rows from a mass; the density is the other factor. */
const MYSTERY_SETS={
  'set 1':[['D','V',0.005, 1000],['B','V',0.001,400],['E','V',0.007,400],
           ['C','V',0.001,19320],['A','V',0.0055,3510]],
  'set 2':[['D','M',18,4500],['A','M',18,11340],['E','V',0.005,8960],
           ['C','M',2.7,2700],['B','M',10.8,2700]],
  'set 3':[['E','M',6,950],['B','M',6,1000],['D','M',2,400],
           ['C','M',23.4,7800],['A','M',2.85,950]],
};
const MYSTERY_COLS={'set 1':['#d05a4f','#4f8fd0','#6fbf5a','#d8c14a','#9b6bd0'],
                    'set 2':['#d489a8','#d88b3c','#a58ed0','#8fc97a','#9a7550'],
                    'set 3':['#e2e6ec','#9aa2b1','#d0b44a','#e0b394','#8d4a4a']};
const MYSTERY_LIST=['set 1','set 2','set 3','shuffled'];
function mysterySet(name,seed){
  if(name==='shuffled') return shuffledMystery(seed);
  const cols=MYSTERY_COLS[name];
  return MYSTERY_SETS[name].map((r,i)=>{
    const V=(r[1]==='V')?r[2]:r[2]/r[3];
    return {tag:r[0],V:V,rho:r[3],m:r[3]*V,col:cols[i],idx:i};
  });
}
/* PhET's RANDOM set draws five of the thirteen table materials and five
   volumes (three from 1-6 L, two from 7-10 L, sorted).  Here the draw comes
   from a seeded generator so that a capture, a test and the browser all see the
   same set for a given seed, and the refresh button simply advances it. */
function lcg(seed){ let s=(seed>>>0)||1; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function shuffleWith(rnd,arr){ const a=arr.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); const t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
function shuffledMystery(seed){
  const rnd=lcg(seed), mats=shuffleWith(rnd,DENSITY_TABLE).slice(0,5);
  const lo=shuffleWith(rnd,[1,2,3,4,5,6]).slice(0,3), hi=shuffleWith(rnd,[7,8,9,10]).slice(0,2);
  const vols=lo.concat(hi).sort((a,b)=>a-b);
  const tags=['A','B','C','D','E'], cols=MYSTERY_COLS['set 1'].concat(MYSTERY_COLS['set 2']);
  return mats.map((mid,i)=>({tag:tags[i],V:vols[i]/LITERS,rho:MAT[mid].phet,
                             m:MAT[mid].phet*vols[i]/LITERS,col:cols[i],idx:i,truth:mid}));
}
/* two decimals, rounded half away from zero, which is what the sim prints */
function disp2(x){ return Math.floor(Math.abs(x)*100+0.5)/100*(x<0?-1:1); }
/* the identification a student can make from the printed numbers alone */
function identify(mDisp,VdispL){
  const rho=mDisp/VdispL*LITERS;
  const d=DENSITY_TABLE.map(k=>({id:k,e:Math.abs(MAT[k].phet-rho)/MAT[k].phet}))
                       .sort((a,b)=>a.e-b.e);
  return {rho:rho,id:d[0].id,err:d[0].e,gap:d[1].e};
}

/* -------------------------------------------- PhET's mass / volume coupling
   Non-custom: the density is fixed, so V = m/rho and the mass slider's enabled
   range is the volume range mapped through rho and clipped to 0.1-27 kg.
   Custom: the two are free and moving either one sets rho = m/V. */
function massRangeFor(rho,custom){
  if(custom) return [MMIN_CUSTOM,MMAX];
  return [clamp(rho*VMIN_L/LITERS,MMIN,MMAX),clamp(rho*VMAX_L/LITERS,MMIN,MMAX)];
}
