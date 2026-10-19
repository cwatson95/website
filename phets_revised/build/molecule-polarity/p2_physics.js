
/* ================================================================== *
 *  the model                                                          *
 *                                                                     *
 *  PhET's frame, kept exactly: +x is to the RIGHT, +y is DOWN, and a   *
 *  positive rotation is CLOCKWISE.  That is also the canvas frame, so  *
 *  model coordinates are drawn without a flip.                         *
 *                                                                     *
 *  Constants are PhET's, read out of build 2.0.2 (MPConstants):        *
 *  ELECTRONEGATIVITY_RANGE (2, 4) with a default of 2 and a 0.2 tick   *
 *  spacing, ATOM_DIAMETER 100, BOND_LENGTH 150, ANGLE_RANGE            *
 *  (-pi, pi), SURFACE_GRADIENT_WIDTH_MULTIPLIER 5.                     *
 * ================================================================== */
const EN_MIN=2, EN_MAX=4, EN_STEP=0.2;
const EN_SPAN=EN_MAX-EN_MIN;                 /* PhET's referenceMagnitude, = 2 */
const ATOM_DIAMETER=100, BOND_LENGTH=150;
const SURF_MULT=5;                           /* PhET's value */
const DIPOLE_REF_LEN=135;                    /* PhET's DipoleNode referenceLength, px */
const BOND_CHAR_BAR=415;                     /* PhET's BondCharacterNode bar width, px */
const EFIELD_K=0.17;                         /* PhET's value: linear(0, 2, 0, 0.17, |mu|) */
const DEBYE_PER_EA=0.208194;                 /* PhET's value: mu[D] = q[e] d[A] / this */

/* PhET's Utils.linear */
function linmap(a1,a2,b1,b2,x){ return (b2-b1)/(a2-a1)*(x-a1)+b1; }
/* PhET's Utils.moduloBetweenDown, used for the e-field's angle bookkeeping */
function normAngle(a,lo){ const L=lo===undefined?0:lo; let x=(a-L)%TAU; if(x<0) x+=TAU; if(x===TAU) x=0; return x+L; }
/* the snap PhET's electronegativity slider applies (constrainValue: roundToInterval 0.2) */
function snapEN(x){ return clamp(Math.round(x/EN_STEP)*EN_STEP,EN_MIN,EN_MAX); }

/* ---------------------------------------------------------------- *
 *  the bond dipole.  PhET builds it as createPolar(|dEN|, ang) with  *
 *  ang the atom1 -> atom2 bond angle, + pi when dEN < 0.  The two    *
 *  branches together are exactly dEN * unit(atom1 -> atom2), which   *
 *  is what this writes; selfTest asserts the two agree everywhere.   *
 * ---------------------------------------------------------------- */
function bondDipole(en1,en2,ang12){ const d=en2-en1; return [d*Math.cos(ang12),d*Math.sin(ang12)]; }
function bondDipolePhet(en1,en2,ang12){
  const d=en2-en1, m=Math.abs(d), a=ang12+(d<0?PI:0);
  return [m*Math.cos(a),m*Math.sin(a)];
}
const vmag=v=>Math.hypot(v[0],v[1]);
const vang=v=>Math.atan2(v[1],v[0]);

/* ---------------------------------------------------------------- *
 *  PhET's DiatomicMolecule: A at theta + pi, B at theta, each        *
 *  BOND_LENGTH/2 from the centre.  Partial charges are PhET's:       *
 *  q_A = +dEN, q_B = -dEN with dEN = EN_B - EN_A, so the more        *
 *  electronegative atom carries the negative charge.                 *
 * ---------------------------------------------------------------- */
function diatomic(enA,enB,theta){
  const r=BOND_LENGTH/2, d=enB-enA;
  const A=[r*Math.cos(theta+PI),r*Math.sin(theta+PI)], B=[r*Math.cos(theta),r*Math.sin(theta)];
  const mu=bondDipole(enA,enB,theta);
  return {A,B,dEN:d,qA:d,qB:-d,mu,mumag:vmag(mu),muang:vang(mu),theta};
}
/* ---------------------------------------------------------------- *
 *  PhET's TriatomicMolecule: B at the centre, A at theta + angAB and *
 *  C at theta + angBC, both BOND_LENGTH away.  Bond AB runs A -> B   *
 *  (direction theta + angAB + pi), bond BC runs B -> C.  Partial     *
 *  charges are PhET's: q_A = EN_B - EN_A, q_C = EN_B - EN_C and      *
 *  q_B = (EN_A - EN_B) + (EN_C - EN_B), so the sum is zero as an     *
 *  identity.  PhET's opening angles are 5pi/6 and pi/6 (120 deg).    *
 * ---------------------------------------------------------------- */
function triatomic(enA,enB,enC,angAB,angBC,theta){
  const th=theta||0;
  const A=[BOND_LENGTH*Math.cos(th+angAB),BOND_LENGTH*Math.sin(th+angAB)];
  const C=[BOND_LENGTH*Math.cos(th+angBC),BOND_LENGTH*Math.sin(th+angBC)];
  const muAB=bondDipole(enA,enB,th+angAB+PI), muBC=bondDipole(enB,enC,th+angBC);
  const mu=[muAB[0]+muBC[0],muAB[1]+muBC[1]];
  return {A,B:[0,0],C,muAB,muBC,mu,mumag:vmag(mu),muang:vang(mu),
          qA:enB-enA,qC:enB-enC,qB:(enA-enB)+(enC-enB),
          dAB:enB-enA,dBC:enC-enB,bondAngle:normAngle(angAB-angBC,-PI),theta:th};
}
/* |mu_AB + mu_BC| in closed form.  u(A->B) . u(B->C) = -cos(theta), so
   |mu|^2 = dAB^2 + dBC^2 - 2 dAB dBC cos(theta) with SIGNED delta-ENs.
   Extremes: theta = 180 gives |dAB + dBC| (zero when dBC = -dAB, the
   symmetric case), theta = 0 gives |dAB - dBC|. */
function mumagClosed(dAB,dBC,theta){
  return Math.sqrt(Math.max(0,dAB*dAB+dBC*dBC-2*dAB*dBC*Math.cos(theta)));
}

/* ---------------------------------------------------------------- *
 *  the surfaces.  PhET paints a linear gradient across the two-atom  *
 *  capsule; both the widths and the stops below are its own.         *
 *  Electron density: two stops, BLACK = more density, and the whole  *
 *  surface is NEUTRAL_GRAY when dEN = 0.  Electrostatic potential:   *
 *  three stops, RED = negative potential (the electron-rich end),    *
 *  BLUE = positive, WHITE at the middle for every dEN.               *
 *  PhET draws both at alpha 0.72 over its pale background; the stops *
 *  here are the same and are drawn opaque (said on the canvas).      *
 * ---------------------------------------------------------------- */
const SURF_ALPHA=0.72;                        /* PhET's value, for the note */
const RGB_BLACK=[0,0,0], RGB_WHITE=[255,255,255], RGB_RED=[255,0,0], RGB_BLUE=[0,0,255];
const RGB_GRAY=[128,128,128];                 /* PhET's NEUTRAL_GRAY */
const ROYGB_STOPS=['#FF0000','#FF2000','#FF4000','#FF6000','#FF8000','#FFA000','#FFC000',
  '#FFE000','#FFF000','#FFFF00','#F0F000','#E0FF00','#C0FF00','#A0FF00','#80FF00','#60FF00',
  '#40FF00','#20FF00','#00FF00','#00FF20','#00FF40','#00FF60','#00FF80','#00FFA0','#00FFC0',
  '#00FFE0','#00FFFF','#00E0FF','#00C0FF','#00A0FF','#0080FF','#0060FF','#0040FF','#0020FF','#0000FF'];
function surfaceWidth(){ return BOND_LENGTH+2.25*(ATOM_DIAMETER/2)+2.25*(ATOM_DIAMETER/2); }
function lerp3(c0,c1,t){ return [c0[0]+(c1[0]-c0[0])*t,c0[1]+(c1[1]-c0[1])*t,c0[2]+(c1[2]-c0[2])*t]; }
function gradWidth(kind,dEN){
  const W=surfaceWidth(), t=Math.abs(dEN)/EN_SPAN;
  return kind==='density'?linmap(1,0,W,W*SURF_MULT,t):linmap(1,0,W/2,W*SURF_MULT,t);
}
/* the colour PhET's gradient paints at model-x = p along the bond axis */
function surfaceColour(kind,dEN,p){
  if(kind==='density'){
    if(dEN===0) return RGB_GRAY.slice();
    const n=gradWidth('density',dEN), s=clamp((p+n/2)/n,0,1);
    return lerp3(dEN>0?RGB_WHITE:RGB_BLACK,dEN>0?RGB_BLACK:RGB_WHITE,s);
  }
  if(dEN===0) return RGB_WHITE.slice();
  const n=gradWidth('potential',dEN), s=clamp((p+n/2)/n,0,1);
  const a=dEN>0?RGB_BLUE:RGB_RED, l=dEN>0?RGB_RED:RGB_BLUE;
  return s<0.5?lerp3(a,RGB_WHITE,2*s):lerp3(RGB_WHITE,l,2*s-1);
}
/* PhET applies its rainbow preference to the Real Molecules surface only, whose
   per-vertex mesh this file does not carry.  So that the chip means something
   and the key always matches the surface it sits above, the same gradient
   POSITION is re-coloured through PhET's own roygb(e): position s in [0,1] runs
   from positive potential to negative, and PhET's ramp spans e in
   [-0.125, +0.125], so e = (0.5 - s)/4.  Said on the canvas. */
function surfacePos(kind,dEN,p){
  if(dEN===0) return 0.5;
  return clamp((p+gradWidth(kind,dEN)/2)/gradWidth(kind,dEN),0,1);
}
function surfaceColourScheme(kind,dEN,p,scheme){
  if(kind!=='potential'||scheme!=='roygb') return surfaceColour(kind,dEN,p);
  const s=surfacePos(kind,dEN,p);
  return roygb((0.5-(dEN>0?s:1-s))/4);
}
function rgbCss(c){ return 'rgb('+Math.round(c[0])+','+Math.round(c[1])+','+Math.round(c[2])+')'; }
function hexRgb(h){ return [parseInt(h.slice(1,3),16),parseInt(h.slice(3,5),16),parseInt(h.slice(5,7),16)]; }
/* PhET's rainbow mapping of an electrostatic-potential value */
function roygb(e){
  const t=clamp((8*e+1)/2,0,1)*(ROYGB_STOPS.length-1), i=Math.floor(t), n=t-i;
  const lo=hexRgb(ROYGB_STOPS[clamp(i,0,ROYGB_STOPS.length-1)]);
  const hi=hexRgb(ROYGB_STOPS[clamp(i+1,0,ROYGB_STOPS.length-1)]);
  return lerp3(lo,hi,n);
}

/* ---------------------------------------------------------------- *
 *  bond character.  PhET rounds |dEN| to two decimals and then bands *
 *  it at 0.05, 0.4, 0.8, 1.2, 1.6 (its a11y BondCharacter rule).     *
 * ---------------------------------------------------------------- */
const CHAR_BANDS=[[0.05,'nonpolar covalent'],[0.4,'nearly nonpolar covalent'],
  [0.8,'slightly polar covalent'],[1.2,'polar covalent'],[1.6,'slightly ionic'],
  [Infinity,'mostly ionic']];
function bondCharacter(dEN){
  const x=Math.round(Math.abs(dEN)*100)/100;
  for(const [lim,name] of CHAR_BANDS) if(x<=lim) return name;
  return CHAR_BANDS[CHAR_BANDS.length-1][1];
}
/* PhET's polarity band, for the molecular dipole */
const POL_BANDS=[[0.05,'nonpolar'],[0.8,'weakly polar'],[1.6,'polar'],
  [2.4,'moderately polar'],[3.2,'strongly polar'],[Infinity,'very strongly polar']];
function polarityOf(mag){
  const x=Math.round(Math.abs(mag)*100)/100;
  for(const [lim,name] of POL_BANDS) if(x<=lim) return name;
  return POL_BANDS[POL_BANDS.length-1][1];
}
/* PhET's DipoleNode: referenceLength 135 px carries referenceMagnitude 2 */
function dipolePx(mag){ return DIPOLE_REF_LEN*mag/EN_SPAN; }

/* ---------------------------------------------------------------- *
 *  the field.                                                        *
 *  PhET's plates: NEGATIVE on the left, POSITIVE on the right, so the *
 *  field points in -x.  Its bond-dipole arrow runs from delta+ to     *
 *  delta- (the chemistry convention), which is anti-parallel to the   *
 *  physicist's p = q d; the arrow therefore settles pointing +x, at   *
 *  the positive plate, exactly as PhET drives it.                     *
 *                                                                     *
 *  PhET's rule (MoleculePolarityModel.step): each animation frame the  *
 *  dipole angle moves |linear(0, 2, 0, 0.17, |mu|)| radians toward 0,  *
 *  the short way round, clamped at the target.  It is a constant       *
 *  angular speed and it depends on the frame rate.                     *
 *                                                                      *
 *  The house model is the rigid rotor that rule stands in for:          *
 *      I psi'' = -mu E sin(psi) - b psi',   b = 2 zeta sqrt(I mu E),    *
 *  whose stable equilibrium is psi = 0 and whose energy                 *
 *      W = 1/2 I psi'^2 + mu E (1 - cos psi)                            *
 *  obeys dW/dt = -b psi'^2 <= 0, so it can only fall.                   *
 * ---------------------------------------------------------------- */
const ROTOR_I=1;                              /* dimensionless moment of inertia */
function phetFieldStep(mu){ return Math.abs(linmap(0,EN_SPAN,0,EFIELD_K,mu)); }
/* one animation frame of PhET's rule: psi in, psi out */
function phetAdvance(psi,mu){
  const step=phetFieldStep(mu);
  let p=normAngle(psi);
  if(p===0||step===0) return 0===p?0:p;
  if(p>0&&p<PI){ p-=step; if(p<0) p=0; }
  else { p+=step; if(p>TAU) p=0; }
  return p;
}
function rotorB(zeta,muE){ return 2*zeta*Math.sqrt(ROTOR_I*muE); }
function rotorOmega0(muE){ return Math.sqrt(muE/ROTOR_I); }
function rotorEnergy(psi,w,muE){ return 0.5*ROTOR_I*w*w+muE*(1-Math.cos(psi)); }
/* one fixed-step RK4 step of the rotor */
function rotorStep(psi,w,muE,b,dt){
  const f=(p,v)=>[v,(-muE*Math.sin(p)-b*v)/ROTOR_I];
  const k1=f(psi,w), k2=f(psi+dt/2*k1[0],w+dt/2*k1[1]);
  const k3=f(psi+dt/2*k2[0],w+dt/2*k2[1]), k4=f(psi+dt*k3[0],w+dt*k3[1]);
  return [psi+dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), w+dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])];
}
/* the rotor integrated for a fixed number of steps (tests, the field view) */
function rotorRun(psi0,w0,muE,b,dt,n){
  let p=psi0, w=w0; const out=[[0,p,w]];
  for(let k=0;k<n;k++){ const r=rotorStep(p,w,muE,b,dt); p=r[0]; w=r[1]; out.push([(k+1)*dt,p,w]); }
  return out;
}

/* ---------------------------------------------------------------- *
 *  the real molecules.  MOLDATA is PhET's own table (p2a_data.js).   *
 *  Basic: bond dipole magnitude = |delta EN| with Pauling values,     *
 *  exactly the 2-D rule.  Advanced: |(q1 - q2)/2| * d / 0.208194 in   *
 *  debye from the Hirshfeld charges, and PhET then rescales the drawn *
 *  arrows so that the molecular arrow carries the Psi4 magnitude      *
 *  (getDipoleArrowScale).  Both are PhET's.                           *
 * ---------------------------------------------------------------- */
const PAULING={H:2.20,B:2.04,C:2.55,N:3.04,O:3.44,F:3.98,Cl:3.16};   /* PhET's element table */
const VDW_PM={H:120,B:192,C:170,N:155,O:152,F:147,Cl:175};           /* PhET's element table */
/* CPK-style element colours lifted for a dark background, as in the house
   molecule sims.  Cosmetic: nothing is computed from them. */
const ELCOL={H:'#e8e8ee',B:'#ffb0a0',C:'#aab2c0',N:'#5f86ff',O:'#ff5a5a',F:'#9be05a',Cl:'#3fd66a'};
const v3sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
const v3len=a=>Math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2]);
const v3scale=(a,s)=>[a[0]*s,a[1]*s,a[2]*s];
const v3plus=(a,b)=>[a[0]+b[0],a[1]+b[1],a[2]+b[2]];
const REALCACHE={};
function realMol(sym){
  if(REALCACHE[sym]) return REALCACHE[sym];
  const m=MOLDATA[sym], n=m.syms.length;
  const out={sym,name:m.name,syms:m.syms,pos:m.pos,bonds:m.bonds,q:m.q,
             psi4:m.psi4,psi4mag:v3len(m.psi4),
             radii:m.syms.map(s=>0.25*VDW_PM[s]/100)};      /* PhET's getDisplayRadius */
  const basic=[], adv=[], lengths=[];
  for(const [ia,ib] of m.bonds){
    const d=v3sub(m.pos[ib],m.pos[ia]), L=v3len(d), u=v3scale(d,1/L);
    lengths.push(L);
    const dEN=PAULING[m.syms[ib]]-PAULING[m.syms[ia]];
    basic.push(v3scale(dEN>=0?u:v3scale(u,-1),Math.abs(dEN)));
    const dq=(m.q[ia]-m.q[ib])/2, ma=Math.abs(dq*(L/DEBYE_PER_EA));
    adv.push(v3scale(dq>=0?u:v3scale(u,-1),ma));
  }
  out.lengths=lengths; out.bondDipolesBasic=basic; out.bondDipolesAdv=adv;
  out.sumBasic=basic.reduce(v3plus,[0,0,0]); out.sumAdv=adv.reduce(v3plus,[0,0,0]);
  out.sumBasicMag=v3len(out.sumBasic); out.sumAdvMag=v3len(out.sumAdv);
  /* PhET's getDipoleArrowScale */
  out.arrowScaleAdv=out.sumAdvMag<=1e-5?0.25:out.psi4mag/out.sumAdvMag*3*0.25;
  out.arrowScaleBasic=0.75;
  /* the central atom is the most-bonded one (PhET's getCentralAtom) */
  let best=0, bn=-1;
  for(let i=0;i<n;i++){ const c=m.bonds.filter(b=>b[0]===i||b[1]===i).length; if(c>bn){ bn=c; best=i; } }
  out.centre=best;
  out.neighbours=m.bonds.filter(b=>b[0]===best||b[1]===best).map(b=>b[0]===best?b[1]:b[0]);
  out.angles=[];
  for(let i=0;i<out.neighbours.length;i++) for(let j=i+1;j<out.neighbours.length;j++)
    out.angles.push(angle3(m.pos[best],m.pos[out.neighbours[i]],m.pos[out.neighbours[j]]));
  out.angles.sort((a,b)=>a-b);
  out.extent=Math.max.apply(null,m.pos.map((p,i)=>v3len(p)+out.radii[i]));
  out.centroid=v3scale(m.pos.reduce(v3plus,[0,0,0]),1/n);
  out.extentC=Math.max.apply(null,m.pos.map((p,i)=>v3len(v3sub(p,out.centroid))+out.radii[i]));
  /* the mean direction from the central atom to its neighbours: the molecular
     dipole must point AWAY from it, toward the electron-rich end */
  out.meanBond=out.neighbours.length
    ? v3scale(out.neighbours.map(j=>{ const d=v3sub(m.pos[j],m.pos[best]); return v3scale(d,1/v3len(d)); })
        .reduce(v3plus,[0,0,0]),1/out.neighbours.length)
    : [0,0,0];
  REALCACHE[sym]=out;
  return out;
}
function angle3(c,a,b){
  const u=v3sub(a,c), v=v3sub(b,c);
  return Math.acos(clamp((u[0]*v[0]+u[1]*v[1]+u[2]*v[2])/(v3len(u)*v3len(v)),-1,1))*180/PI;
}
/* the molecular dipole the Real Molecules screen DRAWS: the vector sum of the
   bond dipoles in both modes (PhET's computeMolecularDipoleFromBondDipoleVectorSum),
   with the advanced arrows scaled so the drawn length carries the Psi4 magnitude */
function realDipoles(sym,advanced){
  const r=realMol(sym);
  const bd=advanced?r.bondDipolesAdv:r.bondDipolesBasic;
  const sum=advanced?r.sumAdv:r.sumBasic;
  const scale=advanced?r.arrowScaleAdv:r.arrowScaleBasic;
  return {bd,sum,mag:advanced?r.sumAdvMag:r.sumBasicMag,scale,
          shown:advanced?r.psi4mag:r.sumBasicMag,unit:advanced?'D':'&Delta;EN'};
}
function measuredOf(sym){ return MEASURED[sym]||null; }
