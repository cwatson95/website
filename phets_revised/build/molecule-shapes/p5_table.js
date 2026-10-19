
/* ================================================================== *
 *  view: the AXE table                                                *
 * ================================================================== */
/* a display frame for a class: lone pairs' centroid up, then the turn about the
   vertical that keeps EVERY pair furthest from the line of sight, so none hides
   behind the central atom (Known-bad: a default camera pointed along the thing the
   view exists to show).  The reference is the DEFAULT camera, not the current one,
   or the shapes would re-orient while being turned.  Drawing only: angles unchanged. */
function viewDirOf(theta,phi){ return [Math.cos(theta)*Math.cos(phi),Math.sin(theta)*Math.cos(phi),Math.sin(phi)]; }
function displayFrame(U,e){
  let R=[[1,0,0],[0,1,0],[0,0,1]];
  let s=[0,0,0]; for(let k=0;k<e;k++) s=v3.add(s,U[k]);
  if(e&&vdot(s,s)>1e-10) R=rotAtoB(vnorm(s),[0,0,1]);
  const vd=viewDirOf(DEFAULTS.camTheta,DEFAULTS.camPhi);
  let best=null;
  for(let k=0;k<72;k++){
    const a=TAU*k/72, c=Math.cos(a), sn=Math.sin(a), M=matMul([[c,-sn,0],[sn,c,0],[0,0,1]],R);
    let worst=2;
    for(const u of U){ const w=matVec(M,u), cs=Math.abs(vdot(w,vd)); worst=Math.min(worst,Math.sqrt(Math.max(0,1-cs*cs))); }
    if(!best||worst>best.worst+1e-12) best={worst,M};
  }
  return U.map(u=>matVec(best.M,u));
}
const TABLE_CAP=HAS_LP
  ?'Every class of steric number 2 to 6, each relaxed at the ρ of the slider and turned so that its lone pairs point up. A row is one electron geometry; each step to the right swaps a bond for a lone pair, and the shape takes the name of what the atoms alone make. Magenta marks the molecule in the model view; click any shape to build it there. Drag to turn them all.'
  :'The five shapes two to six equal bonds settle into round a central atom, each relaxed to the least repulsion energy: linear, trigonal planar, tetrahedral, trigonal bipyramidal and octahedral. Magenta marks the molecule in the model view; click a shape to build it there. Drag to turn them all.';
const TABLE_CAP_SHORT='Every class relaxed; click a shape to build it, drag to turn them all.';
function tableGeo(ctx,W,H){
  const L=stage3D(ctx,W,H,TABLE_CAP,TABLE_CAP_SHORT,HAS_LP?300:180), b=L.b;
  const rowLab=HAS_LP?(L.narrow?64:118):0, head=HAS_LP?22:0;
  const nr=HAS_LP?5:1, nc=5, cw=(b.w-rowLab)/nc;
  /* one row (Basics) would leave a cell twice as tall as it is wide: cap it and centre it */
  const ch=nr>1?(b.h-head)/nr:Math.min(b.h-head,1.45*cw), top=b.y+head+(nr>1?0:Math.max(0,(b.h-head-ch)/2));
  return {L,b,rowLab,head,cw,ch,nr,nc,top};
}
function tableCell(G,k){ return HAS_LP?box(G.b.x+G.rowLab+k.e*G.cw,G.top+(k.n-2)*G.ch,G.cw,G.ch):box(G.b.x+(k.n-2)*G.cw,G.top,G.cw,G.ch); }
function drawTable(ctx,W,H,M){
  const G=tableGeo(ctx,W,H), b=G.b;
  HIT=[];
  if(HAS_LP){
    for(let e=0;e<=4;e++) lab(ctx,W,H,b.x+G.rowLab+(e+0.5)*G.cw,b.y+4,e===0?'no lone pair':e+' lone pair'+(e>1?'s':''),COL.dim,SM_FONT,'center','top');
    for(let n=2;n<=6;n++){ const y=G.top+(n-2+0.5)*G.ch;
      lab(ctx,W,H,b.x+2,y-8,n+' pairs',COL.text,LAB_FONT,'left','middle');
      if(!G.L.narrow) lab(ctx,W,H,b.x+2,y+8,lowName(LABEL[EL_GEOM[n]]),COL.struct,SM_FONT,'left','middle'); }
  }
  const small=Math.min(G.cw,G.ch)<120;
  for(const k of M.classes){
    const cb=tableCell(G,k), here=(k.x===M.x&&k.e===M.e);
    frame(ctx,box(cb.x+2,cb.y+2,cb.w-4,cb.h-4),here?COL.live:COL.edge);
    if(here) frame(ctx,box(cb.x+3,cb.y+3,cb.w-6,cb.h-6),COL.live);
    HIT.push({b:cb,x:k.x,e:k.e});
    const txtH=small?26:40, gb=box(cb.x+4,cb.y+4,cb.w-8,Math.max(20,cb.h-8-txtH));
    const U=displayFrame(k.U,k.e), C=boxCamera(gb,ST.camTheta,ST.camPhi,fitDist(gb,1.3,0.94),[0,0,0]);
    const atoms=[{p:[0,0,0],r:R_CENTRE,col:COL.centre}], bonds=[], lps=[];
    U.forEach((u,i)=>{ if(i<k.e) lps.push({c:[0,0,0],u,dist:ST.rho,s:1}); else { atoms.push({p:u,r:R_OUTER,col:COL.outer}); bonds.push({a:0,b:atoms.length-1,order:1}); } });
    renderMolecule(ctx,C,{atoms,bonds,lps});
    const d=distinctAngles(k.pairs.map(p=>p.deg).sort((a,b)=>a-b)).filter(o=>o.v<179.95||k.x===2);
    lab(ctx,W,H,cb.x+cb.w/2,cb.y1-(small?16:30),(small?'':axeName(k.x,k.e)+'  ')+lowName(k.names.mol),here?COL.live:COL.text,small?SM_FONT:LAB_FONT,'center','bottom');
    if(!small) lab(ctx,W,H,cb.x+cb.w/2,cb.y1-8,d.slice(0,3).map(o=>fmt(o.v,1)+'°').join('  '),COL.pos,SM_FONT,'center','bottom');
  }
  drawCap(ctx,G.L);
}
function hitAt(x,y){ for(let i=HIT.length-1;i>=0;i--){ const h=HIT[i], bb=h.b; if(x>=bb.x&&x<=bb.x1&&y>=bb.y&&y<=bb.y1) return h; } return null; }

