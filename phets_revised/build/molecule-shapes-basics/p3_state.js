
/* ================================================================== *
 *  state, the model view's live molecule, the real view's blend, the  *
 *  relaxation run, the per-view model, readout, eqbar, tag            *
 * ================================================================== */
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           text:'#aeb6c6', centre:'#9a7fd1', outer:'#d8dce6', bond:'#9aa2b4', lp:'#5ac8e0', lpE:'#e9f6fb'};
const RO_W=300;
/* with no lone pairs the least-energy arrangement is just the ideal shape: Basics says so */
const BESTNAME=HAS_LP?'VSEPR':'ideal';
/* CPK-style element colours lifted for a dark background (C, H, N, O, S as amino_acids.html;
   the rest in the same spirit).  Cosmetic: nothing is computed from them. */
const ELCOL={H:'#e8e8ee',C:'#aab2c0',N:'#5f86ff',O:'#ff5a5a',S:'#ffd23f',F:'#9be05a',Cl:'#3fd66a',
             Br:'#c9544c',P:'#ff9a3a',B:'#ffb0a0',Be:'#c8f060',Xe:'#4fb6cc'};
/* drawing radii (fractions of the one drawn bond length).  Cosmetic, like PhET's own
   scaled spheres: the bond angles do not depend on them. */
const ATOM_R={H:0.15,C:0.24,N:0.23,O:0.22,S:0.29,F:0.2,Cl:0.26,Br:0.29,P:0.29,B:0.24,Be:0.25,Xe:0.33};
const R_CENTRE=0.3, R_OUTER=0.2;          /* the model view's A and X */

/* PhET's defaults: lone pairs shown (not in Basics), bond angles and the names hidden,
   outer lone pairs hidden; the first molecule of the list; the real view in "Real". */
const DEFAULTS={view:'model', rho:RHO_PHET, showLP:HAS_LP, showAngles:false, showMolName:false, showElName:false,
                mol:MOL_LIST[0], realMode:'real', showOuterLP:false, camTheta:-1.05, camPhi:0.34, zoom:1};
const ST=Object.assign({},DEFAULTS);
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---------------------------------------------------------------- *
 *  the model view's molecule                                         *
 *  groups: {id, order (0 = lone pair, 1-3 = bond), u (unit vector),  *
 *  rr (the fly-in: drawn radius / rest radius, relaxing to 1)}       *
 * ---------------------------------------------------------------- */
const LIVE={groups:[], nextId:0, held:-1, fitKey:'', fit:null, anim:true, realBlend:0};
function liveCounts(){ let x=0,e=0; for(const g of LIVE.groups){ if(g.order===0) e++; else x++; } return {x,e}; }
function kindsOf(groups){ return groups.map(g=>g.order===0?'lp':'b'); }
function slotKinds(x,e){ const k=[]; for(let i=0;i<e;i++) k.push('lp'); for(let i=0;i<x;i++) k.push('b'); return k; }
function radiiLive(groups,rho){ return groups.map(g=>g.order===0?rho:1); }
/* PhET's opening molecule: two single bonds along (8,0,3) and (2,8,-5), which relax to a line */
function liveInit(){
  LIVE.groups=[]; LIVE.nextId=0; LIVE.held=-1; LIVE.fitKey=''; LIVE.anim=true;
  for(const v of [[8,0,3],[2,8,-5]]) LIVE.groups.push({id:LIVE.nextId++,order:1,u:vnorm(matVec(PHET_TO_WORLD,v)),rr:1});
}
/* can a group of this order be added?  (PhET: six at most; the lone-pair button is
   dead while lone pairs are hidden) */
function canAdd(order){ return LIVE.groups.length<MAXG&&(order!==0||(HAS_LP&&ST.showLP)); }
/* add a group: it arrives in the slot the new equilibrium leaves for it, fitted to
   the groups already there, and flies in from 1.7x its rest radius */
function liveAdd(order){
  if(!canAdd(order)) return false;
  const c=liveCounts(), x=c.x+(order?1:0), e=c.e+(order?0:1);
  const eq=equilibrium(x,e,ST.rho);
  const groups=LIVE.groups.concat([{id:LIVE.nextId++,order,u:[0,0,1],rr:1.7}]);
  const U=groups.map(g=>g.u), n=groups.length;
  const f=fitAssign(eq.U,slotKinds(x,e),U,kindsOf(groups),[n-1]);
  groups[n-1].u=vnorm(matVec(f.R,eq.U[f.sigma[n-1]]));
  LIVE.groups=groups; LIVE.fitKey=''; LIVE.anim=true;
  return true;
}
/* remove the most recently added group of this order (PhET) */
function liveRemove(order){
  for(let i=LIVE.groups.length-1;i>=0;i--) if(LIVE.groups[i].order===order){
    LIVE.groups.splice(i,1); LIVE.fitKey=''; LIVE.held=-1; LIVE.anim=true; return true; }
  return false;
}
function liveRemoveAll(){ const had=LIVE.groups.length>0; LIVE.groups=[]; LIVE.fitKey=''; LIVE.held=-1; LIVE.anim=true; return had; }
function liveHasOrder(order){ return LIVE.groups.some(g=>g.order===order); }
/* the target: the equilibrium of this composition at this rho, assigned to the groups
   (re-chosen whenever the composition, rho or a release changes it) and turned onto
   them by the best rotation, refitted every call */
function liveTarget(){
  const {x,e}=liveCounts(), groups=LIVE.groups;
  if(!groups.length) return [];
  const key=x+','+e+','+ST.rho.toFixed(12)+','+groups.map(g=>g.id).join('.');
  const U=groups.map(g=>g.u);
  if(key!==LIVE.fitKey||!LIVE.fit){
    const eq=equilibrium(x,e,ST.rho);
    const f=fitAssign(eq.U,slotKinds(x,e),U,kindsOf(groups));
    LIVE.fit={eq,sigma:f.sigma}; LIVE.fitKey=key;
  }
  const A=U.map((u,i)=>LIVE.fit.eq.U[LIVE.fit.sigma[i]]);
  const R=horn(A,U);
  return A.map(a=>matVec(R,a));
}
/* the display flow: each group slides along its sphere under the repulsion (KAP) and
   is steered to its target (KS).  Both vanish at the equilibrium, so it is where the
   flow ends; within 1e-7 rad of it the groups snap onto it and the loop goes idle. */
const FLOW={RATE:1.8, KAP:1, KS:3, SUB:0.03, SNAP:1e-7};
function liveStep(dt){
  const groups=LIVE.groups;
  let moved=false;
  for(const g of groups) if(g.rr!==1){ g.rr=1+(g.rr-1)*Math.exp(-8*dt); if(Math.abs(g.rr-1)<1e-4) g.rr=1; moved=true; }
  if(!LIVE.anim||groups.length===0){ LIVE.anim=moved; return moved; }
  const R=radiiLive(groups,ST.rho);
  const h=FLOW.RATE*Math.min(dt,0.05), nsub=Math.max(1,Math.ceil(h/FLOW.SUB)), hs=h/nsub;
  for(let s=0;s<nsub;s++){
    const U=groups.map(g=>g.u), T=liveTarget(), Gt=tangentOf(U,gradOf(U,R));
    for(let i=0;i<groups.length;i++){ if(i===LIVE.held) continue;
      const u=U[i], d=[T[i][0]-u[0],T[i][1]-u[1],T[i][2]-u[2]], c=vdot(d,u);
      const st=[-FLOW.KAP*Gt[i][0]+FLOW.KS*(d[0]-c*u[0]),-FLOW.KAP*Gt[i][1]+FLOW.KS*(d[1]-c*u[1]),-FLOW.KAP*Gt[i][2]+FLOW.KS*(d[2]-c*u[2])];
      groups[i].u=vnorm([u[0]+hs*st[0],u[1]+hs*st[1],u[2]+hs*st[2]]);
    }
  }
  const T=liveTarget(); let dev=0;
  groups.forEach((g,i)=>{ dev=Math.max(dev,Math.acos(clamp(vdot(g.u,T[i]),-1,1))); });
  if(dev<FLOW.SNAP&&LIVE.held<0){ groups.forEach((g,i)=>g.u=T[i]); if(!moved) LIVE.anim=false; }
  return true;
}
/* the flow run to completion (tests, captures, the table's click) */
function liveSettle(maxFrames){ for(let k=0;k<(maxFrames||4000)&&(LIVE.anim||LIVE.groups.some(g=>g.rr!==1));k++) liveStep(1/60); }
/* load a class into the model: x single bonds and e lone pairs at its equilibrium */
function liveLoad(x,e){
  const eq=equilibrium(x,e,ST.rho), U=displayFrame(eq.U,e);
  LIVE.groups=U.map((u,i)=>({id:LIVE.nextId++,order:i<e?0:1,u:u.slice(),rr:1}));
  LIVE.fitKey=''; LIVE.held=-1; LIVE.anim=true;
}
/* the bond angles of a set of directions: every pair of bonds */
function bondPairs(B){ const out=[]; for(let i=0;i<B.length;i++) for(let j=i+1;j<B.length;j++) out.push({i,j,deg:angleDeg(B[i],B[j])}); return out; }
/* which angle arcs read from where the camera is: PhET's brightness rule, |(u_i x u_j) . view|
   mapped between PhET's per-bond-count thresholds; two bonds always show */
const ARC_LO=[0,0,0,0.1,0.35,0.45,0.5], ARC_HI=[0,0,0,0.5,0.55,0.65,0.75];   /* PhET's values */
function arcBrightness(a,b,fwd,nb){
  if(nb<=2) return 1;
  const n=Math.abs(vdot(vcross(a,b),fwd)), lo=ARC_LO[nb], hi=ARC_HI[nb];
  return clamp((n-lo)/(hi-lo),0,1);
}

/* ---------------------------------------------------------------- *
 *  named angles: the ones the measured molecules test, read off the  *
 *  class's equilibrium by slot (twin of derive.named_angles)          *
 * ---------------------------------------------------------------- */
const NAMED={AX2E1:[2,1,1,2,120],AX2E2:[2,2,2,3,TET],AX3E1:[3,1,1,2,TET],AX4E1_ax:[4,1,3,4,180],AX4E1_eq:[4,1,1,2,120],
  AX4E1_axeq:[4,1,1,3,90],AX3E2_axeq:[3,2,2,3,90],AX3E2_ax:[3,2,3,4,180],AX5E1_axb:[5,1,1,2,90],AX5E1_bb:[5,1,2,4,90],
  AX3E3_short:[3,3,3,4,90],AX3E3_ax:[3,3,4,5,180],AX2E3:[2,3,3,4,180],AX4E2:[4,2,2,4,90],AX2E4:[2,4,4,5,180]};
function namedAngle(key,rho){ const [x,e,i,j]=NAMED[key], U=equilibrium(x,e,rho).U; return angleDeg(U[i],U[j]); }
/* the measured angles, each READ OFF PhET's geometry by bond index (never retyped) */
const COMPARE=[
  {mol:'SO2',key:'AX2E1',bi:[0,1],what:'O–S–O'},
  {mol:'H2O',key:'AX2E2',bi:[0,1],what:'H–O–H'},
  {mol:'NH3',key:'AX3E1',bi:[0,1],what:'H–N–H'},
  {mol:'SF4',key:'AX4E1_ax',bi:[0,1],what:'F–S–F axial'},
  {mol:'SF4',key:'AX4E1_eq',bi:[2,3],what:'F–S–F equatorial'},
  {mol:'ClF3',key:'AX3E2_axeq',bi:[0,1],what:'F–Cl–F'},
  {mol:'BrF5',key:'AX5E1_axb',bi:[0,1],what:'F–Br–F'},
];
function measured(c){ const g=realGeometry(c.mol); return angleDeg(g.B[c.bi[0]],g.B[c.bi[1]]); }
/* the rho at which the model's angle equals a target, on [RHO_MIN, RHO_MAX]: bracketed on
   the 0.01 grid, then bisected on the relaxation itself (null when the model never gets there) */
const RHOFIT={};
function rhoFit(key,target){
  const k=key+'|'+target.toFixed(12);
  if(RHOFIT[k]!==undefined) return RHOFIT[k];
  const f=r=>namedAngle(key,r)-target;
  let out=null;
  for(let i=0;i<SQ_RHO.length-1&&out===null;i++){
    let a=SQ_RHO[i], b=SQ_RHO[i+1], fa=f(a), fb=f(b);
    if(fa===0){ out=a; break; }
    if(fa*fb<0){ for(let it=0;it<48;it++){ const m=(a+b)/2, fm=f(m); if(fa*fm<=0){ b=m; fb=fm; } else { a=m; fa=fm; } } out=(a+b)/2; }
  }
  return (RHOFIT[k]=out);
}
function compareRows(rho){
  return COMPARE.map(c=>{ const ideal=NAMED[c.key][4], meas=measured(c), model=namedAngle(c.key,rho);
    return {c,ideal,meas,model,agree:(meas-ideal)*(model-ideal)>0,rfit:rhoFit(c.key,meas)}; });
}
/* the squeeze curves: every named angle on rho = 0.70 ... 1.00 */
const SQ_RHO=[]; for(let k=0;k<=30;k++) SQ_RHO.push(Math.round((0.70+0.01*k)*100)/100);
const SQ_KEYS=['AX2E1','AX2E2','AX3E1','AX4E1_ax','AX4E1_eq','AX3E2_axeq','AX5E1_axb'];
function squeezeCurves(){
  return memo('sq','grid',()=>{ const out={}; for(const k of SQ_KEYS) out[k]=SQ_RHO.map(r=>namedAngle(k,r)-NAMED[k][4]); return out; });
}

/* ---------------------------------------------------------------- *
 *  the real view: Real and Model blended (0 = measured, 1 = model)   *
 * ---------------------------------------------------------------- */
function realTarget(){ return ST.realMode==='model'?1:0; }
function realStep(dt){
  const tg=realTarget(), b=LIVE.realBlend;
  if(b===tg) return false;
  let nb=b+(tg-b)*(1-Math.exp(-6*dt));
  if(Math.abs(tg-nb)<1e-3) nb=tg;
  LIVE.realBlend=nb; return true;
}
function slerp(a,b,t){
  const c=clamp(vdot(a,b),-1,1), om=Math.acos(c);
  if(om<1e-9) return a.slice();
  const s=Math.sin(om), wa=Math.sin((1-t)*om)/s, wb=Math.sin(t*om)/s;
  return vnorm([wa*a[0]+wb*b[0],wa*a[1]+wb*b[1],wa*a[2]+wb*b[2]]);
}
function realShown(id,rho,blend){
  const g=realGeometry(id), m=memo('mreal',id+'|'+rho.toFixed(12),()=>modelOfReal(id,rho));
  return {B:g.B.map((u,i)=>slerp(u,m.B[i],blend)), LP:g.LP.map((u,k)=>slerp(u,m.LP[k],blend)), g, m};
}

/* ---------------------------------------------------------------- *
 *  the relaxation view: pure gradient descent from a random start    *
 * ---------------------------------------------------------------- */
const RELAX={seed:0, key:'', U:null, R:null, x:0, e:0, step:0, hist:[], done:false, trail:[]};
const RELAX_SEED0=20260918, RELAX_STEPS=3, RELAX_DONE=1e-10;
function relaxKey(){ const c=liveCounts(); return c.x+','+c.e+','+ST.rho.toFixed(12)+','+RELAX.seed; }
function relaxReset(){
  const c=liveCounts(), n=c.x+c.e;
  RELAX.key=relaxKey(); RELAX.x=c.x; RELAX.e=c.e; RELAX.step=0; RELAX.hist=[]; RELAX.trail=[]; RELAX.done=false;
  if(n<2){ RELAX.U=null; RELAX.R=null; RELAX.done=true; return; }
  const rnd=mulberry32(RELAX_SEED0+7919*RELAX.seed);
  RELAX.U=randomDirs(rnd,n); RELAX.R=radiiOf(c.x,c.e,ST.rho);
  RELAX.hist.push(energyOf(RELAX.U,RELAX.R)); RELAX.trail.push(RELAX.U.map(u=>u.slice()));
}
function relaxEnsure(){ if(RELAX.key!==relaxKey()) relaxReset(); }
/* k steps of the same descent as relax(); done when every tangential gradient < 1e-10 */
function relaxAdvance(k){
  relaxEnsure();
  if(RELAX.done) return false;
  for(let s=0;s<k;s++){
    const Gt=tangentOf(RELAX.U,gradOf(RELAX.U,RELAX.R));
    if(maxLen(Gt)<RELAX_DONE){ RELAX.done=true; break; }
    RELAX.U=RELAX.U.map((u,i)=>vnorm([u[0]-ETA*Gt[i][0],u[1]-ETA*Gt[i][1],u[2]-ETA*Gt[i][2]]));
    RELAX.step++; RELAX.hist.push(energyOf(RELAX.U,RELAX.R));
    if(RELAX.step%6===0){ RELAX.trail.push(RELAX.U.map(u=>u.slice())); if(RELAX.trail.length>60) RELAX.trail.shift(); }
  }
  return true;
}
function relaxRun(maxSteps){ relaxEnsure(); let n=0; while(!RELAX.done&&n<(maxSteps||40000)){ relaxAdvance(50); n+=50; } }
/* which arrangement the run is in: the isomer whose energy it matches (after it settles) */
function relaxVerdict(){
  if(!RELAX.U) return null;
  const lad=isomerLadder(RELAX.x,RELAX.e,ST.rho), E=RELAX.hist[RELAX.hist.length-1];
  let k=-1; lad.forEach((f,i)=>{ if(Math.abs(f.E-E)<1e-7*Math.max(1,f.E)) k=i; });
  return {ladder:lad, E, rank:k, vsepr:Math.abs(lad[0].E-equilibrium(RELAX.x,RELAX.e,ST.rho).E)<1e-8};
}

/* ---------------------------------------------------------------- *
 *  the AXE table: steric numbers 2-6, x >= 2                          *
 * ---------------------------------------------------------------- */
function tableClasses(){
  const out=[];
  for(let n=2;n<=6;n++) for(let e=0;e<=(HAS_LP?n-2:0);e++) out.push({x:n-e,e,n});
  return out;
}

/* ---------------------------------------------------------------- *
 *  the per-view model                                                *
 * ---------------------------------------------------------------- */
function buildModel(){
  const st=ST, M={st, view:st.view, rho:st.rho};
  const c=liveCounts(); M.x=c.x; M.e=c.e; M.names=geomNames(c.x,c.e);
  if(st.view==='model'){
    const B=LIVE.groups.filter(g=>g.order>0).map(g=>g.u);
    M.pairs=bondPairs(B);
    M.eq=equilibrium(c.x,c.e,st.rho);
    M.eqPairs=bondPairs(M.eq.U.slice(c.e));
    M.ideal=idealBondAngles(c.x,c.e);
    M.E=energyOf(LIVE.groups.map(g=>g.u),radiiLive(LIVE.groups,st.rho));
    M.settled=!LIVE.anim;
  } else if(st.view==='real'){
    M.id=st.mol; M.shown=realShown(st.mol,st.rho,LIVE.realBlend);
    const g=M.shown.g; M.rx=g.x; M.re=g.e; M.rnames=geomNames(g.x,g.e);
    M.realDistinct=distinctAngles(g.angles); M.modelDistinct=distinctAngles(M.shown.m.angles);
    M.ideal=idealBondAngles(g.x,g.e);
    M.pairs=bondPairs(M.shown.B);
  } else if(st.view==='table'){
    M.classes=tableClasses().map(k=>{ const eq=equilibrium(k.x,k.e,st.rho);
      return Object.assign({},k,{U:eq.U,names:geomNames(k.x,k.e),pairs:bondPairs(eq.U.slice(k.e)),ideal:idealBondAngles(k.x,k.e)}); });
  } else if(st.view==='squeeze'){
    M.curves=squeezeCurves(); M.rows=compareRows(st.rho);
  } else if(st.view==='relax'){
    relaxEnsure(); M.verdict=RELAX.done?relaxVerdict():null;
    M.eqE=RELAX.U?equilibrium(RELAX.x,RELAX.e,st.rho).E:NaN;
  }
  return M;
}

/* ---------------------------------------------------------------- *
 *  readout / eqbar / tag                                             *
 * ---------------------------------------------------------------- */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function axeHTML(x,e){ return (x?'AX'+(x!==1?'<sub>'+x+'</sub>':''):'A')+(e?'E'+(e>1?'<sub>'+e+'</sub>':''):''); }
/* lower case for a name inside a sentence, but T-shaped keeps its T */
function lowName(s){ return s==='T-shaped'?s:s.toLowerCase(); }
function degs(v){ return fmt(v,1)+'&deg;'; }
function degs3(v){ return fmt(v,3)+'&deg;'; }
function angleList(d){ return d.map(o=>(o.n>1?o.n+'&times; ':'')+degs(o.v)).join(', '); }
function rhoTxt(r){ return fmt(r,2)+(Math.abs(r-RHO_PHET)<1e-9?' (PhET&rsquo;s)':''); }
function readoutHTML(M){
  const st=M.st;
  let h='';
  if(M.view==='model'){
    const nm=M.names;
    h+='<div class="rname">'+axeHTML(M.x,M.e)+(nm.mol?' &mdash; '+lowName(nm.mol):'')+'<small>'
      +(M.x+M.e?'electron geometry '+lowName(nm.el):'add a bond or a lone pair')+(HAS_LP?' &middot; &rho; = '+rhoTxt(st.rho):'')+'</small></div><table>';
    h+=hd('the pairs')+rrow('bonds (single, double, triple)',M.x+' ('+[1,2,3].map(o=>LIVE.groups.filter(g=>g.order===o).length).join(', ')+')');
    if(HAS_LP) h+=rrow('lone pairs',M.e);
    h+=rrow('steric number x + e',M.x+M.e);
    if(M.x>=2){
      h+=hd('bond angles');
      h+=rrow('this model',angleList(distinctAngles(M.eqPairs.map(p=>p.deg).sort((a,b)=>a-b))),'good');
      h+=rrow('ideal '+lowName(nm.el),angleList(distinctAngles(M.ideal)));
    }
    h+=hd('the repulsion')+rrow('energy U (units of 1/bond&sup2;)',M.x+M.e>1?fmt(M.E,6):'&mdash;')
      +rrow('state',M.x+M.e===0?'empty':M.settled?'at its minimum':'relaxing','good');
    h+='</table><div class="note">'+(HAS_LP
      ?'Bonds sit on the unit sphere, lone pairs nearer the nucleus at &rho;; every pair repels as 1/d&sup2;. The drawn shape is the least-energy arrangement. At &rho; = 1 a lone pair acts as a bond and every angle is the ideal one.'
      :'Every bond repels every other as 1/d&sup2; on the unit sphere, and the drawn shape is the least-energy arrangement: exactly the ideal angles.')+'</div>';
  } else if(M.view==='real'){
    const g=M.shown.g, nm=M.rnames, m=REAL[M.id];
    h+='<div class="rname">'+formulaHTML(M.id)+' &mdash; '+lowName(nm.mol)+'<small>'+axeHTML(g.x,g.e)+' &middot; electron geometry '+lowName(nm.el)
      +' &middot; '+(ST.realMode==='model'?'the model':'measured')+'</small></div><table>';
    if(g.x>=2){
      h+=hd('bond angles')+rrow('measured (PhET&rsquo;s data)',angleList(M.realDistinct),'good');
      if(HAS_LP) h+=rrow('this model, &rho; = '+fmt(st.rho,2),angleList(M.modelDistinct));
      h+=rrow('ideal '+lowName(nm.el),angleList(distinctAngles(M.ideal)));
    }
    const Ls=distinctAngles(m.bonds.map(b=>b.L).sort((a,b)=>a-b));
    h+=hd('bond lengths (PhET&rsquo;s data)')+rrow(m.centre+'&ndash;'+m.outer,Ls.map(o=>(o.n>1?o.n+'&times; ':'')+fmt(o.v,3)+' &Aring;').join(', '));
    if(HAS_LP) h+=rrow('lone pairs on '+m.centre+' / on each '+m.outer,g.e+' / '+m.olp);
    h+='</table><div class="note">Angles and lengths are PhET&rsquo;s table (PubChem and the best known bond angles, its notes say). '
      +'Every bond is drawn at one length, as PhET draws them'+(HAS_LP?'; the central lone pairs sit where the ideal slots put them once the ideal bonds are fitted onto the real ones.':'.')+'</div>';
  } else if(M.view==='table'){
    h+='<div class="rname">The AXE table<small>'+(HAS_LP?'x bonds and e lone pairs round A, at &rho; = '+rhoTxt(st.rho):'x bonds round A, nothing else')+'</small></div><table>';
    h+=hd('steric number x + e &rarr; electron geometry');
    for(let n=2;n<=6;n++) h+=rrow(n,lowName(LABEL[EL_GEOM[n]]));
    h+=hd('the model now')+rrow(axeHTML(M.x,M.e),M.names.mol?lowName(M.names.mol):'&mdash;','good');
    h+='</table><div class="note">'+(HAS_LP
      ?'The electron geometry counts every pair; the molecule geometry names only where the atoms are. Lone pairs take the equatorial slots of the bipyramid and the trans slots of the octahedron, and in this model that is also the least-energy choice for every class at every &rho; on the slider (derive.py).'
      :'Five shapes from one rule: bonds spread as far apart as they can on a sphere. Click a shape to build it.')+'</div>';
  } else if(M.view==='squeeze'){
    h+='<div class="rname">The squeeze<small>model angle &minus; ideal against &rho;; &rho; = '+rhoTxt(st.rho)+'</small></div><table>';
    h+=hd('molecule: measured / model / ideal');
    for(const r of M.rows) h+=rrow(formulaHTML(r.c.mol)+' '+r.c.what,fmt(r.meas,1)+' / '+fmt(r.model,1)+' / '+fmt(r.ideal,1),r.agree?'good':'bad');
    const nA=M.rows.filter(r=>r.agree).length;
    h+='</table><div class="note">Green: the model bends the angle the way the molecule does ('+nA+' of '+M.rows.length+'). SF<sub>4</sub>&rsquo;s equatorial angle is the exception: point pairs open it past 120&deg;, the real molecule closes it to 101.6&deg;.</div>';
  } else if(M.view==='relax'){
    const v=M.verdict;
    h+='<div class="rname">The relaxation<small>'+axeHTML(RELAX.x,RELAX.e)+' from random start '+(RELAX.seed+1)+(HAS_LP?', &rho; = '+fmt(st.rho,2):'')+'</small></div><table>';
    if(!RELAX.U) h+=rrow('pairs','fewer than two: nothing to relax');
    else {
      const E=RELAX.hist[RELAX.hist.length-1];
      h+=hd('the descent')+rrow('steps',RELAX.step)+rrow('energy U',fmt(E,8))+rrow('U &minus; U('+BESTNAME+')',sigf(E-M.eqE,3));
      if(v){ h+=hd('arrangements, least energy first');
        v.ladder.forEach((f,i)=>{ h+=rrow((i===0?BESTNAME+' ':'isomer '+(i+1)+' ')+(i===v.rank?'&larr; here':''),fmt(f.E,6),i===v.rank?(i===0?'good':'bad'):''); });
        if(v.rank<0) h+=rrow('this run &larr; here','a minimum no slot arrangement reaches','bad'); }
      else h+=rrow('state','descending','good');
    }
    h+='</table><div class="note">Plain gradient descent on U from a random start, no steering. '
      +(HAS_LP?'It can stall in a higher local minimum; the model view avoids that by starting from the VSEPR slots.':'For two to six equal pairs it always ends in the ideal shape.')+'</div>';
  }
  return h;
}
function eqbarHTML(M){
  const v=M.view;
  if(v==='model') return '<span class="lhs">U</span> = &Sigma;<sub>i&lt;j</sub> 1 / |R<sub>i</sub><b>u</b><sub>i</sub> &minus; R<sub>j</sub><b>u</b><sub>j</sub>|&sup2;'
    +(HAS_LP?', &nbsp; R = 1 for a bond, <span class="hl">&rho;</span> for a lone pair':'')
    +'<span class="sm">the drawn shape is the arrangement of least energy'+(HAS_LP?'; lone pairs sit nearer the nucleus, so they push harder':'')+'</span>';
  if(v==='real') return '<span class="lhs">&theta;<sub>ij</sub></span> = arccos(<b>u</b><sub>i</sub> &middot; <b>u</b><sub>j</sub>)'
    +'<span class="sm">every bond angle is read off PhET&rsquo;s measured geometry'+(HAS_LP?'; the Model chip swaps in the least-energy arrangement':'')+'</span>';
  if(v==='table') return '<span class="lhs">steric number</span> = x + e &nbsp;&rarr;&nbsp; <span class="hl">electron geometry</span>; &nbsp; x &nbsp;&rarr;&nbsp; <span class="hl2">molecule geometry</span>'
    +'<span class="sm">the pairs fix the arrangement, the atoms alone give it its name</span>';
  if(v==='squeeze') return '<span class="lhs">&Delta;&theta;(&rho;)</span> = &theta;<sub>model</sub>(&rho;) &minus; &theta;<sub>ideal</sub>, &nbsp; &Delta;&theta;(1) = 0'
    +'<span class="sm">how far pulling the lone pairs in bends each bond angle, beside the measured molecules</span>';
  return '<b>u</b><sub>i</sub> &larr; normalise(<b>u</b><sub>i</sub> &minus; &eta; &nabla;<sub>t</sub>U), &nbsp; &eta; = 0.1'
    +'<span class="sm">downhill on the sphere until no pair feels a sideways push</span>';
}
function tagHTML(M){
  const v=M.view;
  if(v==='model') return '<b>'+axeHTML(M.x,M.e)+'</b> '+(M.names.mol?lowName(M.names.mol):'no bonds');
  if(v==='real') return '<b>'+formulaHTML(M.id)+'</b> '+(ST.realMode==='model'?'the model':'measured');
  if(v==='table') return '<b>'+M.classes.length+'</b> shapes'+(HAS_LP?' at &rho; = '+fmt(M.rho,2):'');
  if(v==='squeeze') return '<b>7</b> measured angles against the model';
  return '<b>'+axeHTML(RELAX.x,RELAX.e)+'</b> start '+(RELAX.seed+1);
}
