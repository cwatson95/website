
/* ================================================================== *
 *  the 3-D molecule renderer and the two PhET screens                 *
 * ================================================================== */
/* the house #hint (HTML, bottom:11px, 11px type) sits on the last line of a
   caption anchored at H - 12: every caption here ends HINT_H higher, clear of
   it (lineage: build/wave-on-a-string) */
const HINT_H=18;
const TITLE_FONT='italic 13px Georgia, serif', BIG_FONT='italic 20px Georgia, serif', ANG_FONT='11.5px -apple-system, sans-serif';
let PICK=[];            /* the draggable pairs of the last model-view draw: {i, x, y, r, z} */
let HIT=[];             /* the clickable cells of the last table draw: {b, x, e} */
/* a stage with one 3-D box and a measured, bottom-anchored caption */
function stage3D(ctx,W,H,capFull,capShort,minBox){
  const narrow=isNarrow(W), left=20, right=narrow?W-20:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+22;
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+(minBox||240));
  const b=box(left,top,right-left,Math.max(80,fit.capY-14-top));
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,b};
}
function drawCap(ctx,L){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); }
/* the camera distance at which a ball of radius R fills `frac` of the box's smaller
   side: a ball's silhouette is its tangent cone, half-width f R / sqrt(D^2 - R^2)
   (Known-bad: the near-point form f R/(D - R) frames it at 0.82 of the size claimed) */
function fitDist(b,R,frac){
  const f=(b.h/2)/Math.tan(0.78/2), want=frac*Math.min(b.w,b.h)/2;
  return R*Math.sqrt(1+(f/want)*(f/want));
}
function molCam(b,R,zoom,frac){ const C=boxCamera(b,ST.camTheta,ST.camPhi,fitDist(b,R,(frac||0.86)*(zoom||1)),[0,0,0]); C.b=b; return C; }

/* the hull of two circles, a teardrop: root circle (bx,by,r0), bulb (tx,ty,r1).
   The outer tangents have unit normals m = -sin g e +- cos g n, sin g = (r1-r0)/L;
   the bulb's arc sweeps pi + 2g through the far side, the root's pi - 2g. */
function teardropPts(bx,by,r0,tx,ty,r1){
  const dx=tx-bx, dy=ty-by, L=Math.hypot(dx,dy), pts=[];
  if(L<=Math.abs(r1-r0)+1e-6){ for(let k=0;k<28;k++){ const a=TAU*k/28; pts.push([tx+r1*Math.cos(a),ty+r1*Math.sin(a)]); } return pts; }
  const th=Math.atan2(dy,dx), g=Math.asin(clamp((r1-r0)/L,-1,1));
  const N=22, M=8;
  for(let k=0;k<=N;k++){ const a=th+PI/2+g-(PI+2*g)*k/N; pts.push([tx+r1*Math.cos(a),ty+r1*Math.sin(a)]); }
  for(let k=0;k<=M;k++){ const a=th-PI/2-g-(PI-2*g)*k/M; pts.push([bx+r0*Math.cos(a),by+r0*Math.sin(a)]); }
  return pts;
}
function fillPoly(ctx,pts,fill,stroke,lw){
  ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); ctx.closePath();
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1; ctx.stroke(); }
}
function line2(ctx,x0,y0,x1,y1,col,w){ ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1); ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap='round'; ctx.stroke(); ctx.lineCap='butt'; }
/* a shaded ball: base, a lit offset disc, a highlight (amino_acids.html's three discs) */
function ball(ctx,x,y,r,base,cue){
  dot(ctx,x,y,r,shade(base,0.5*cue),null);
  if(r>=3){ dot(ctx,x-0.2*r,y-0.2*r,0.64*r,shade(base,0.8*cue),null); dot(ctx,x-0.34*r,y-0.34*r,0.24*r,mix(shade(base,cue),'#ffffff',0.45),null); }
}

/* ---- the renderer: painter's order over balls, half-bonds and lone-pair lobes ----
   mol = {atoms:[{p, r, col, ring}], bonds:[{a, b, order}], lps:[{c, u, dist, s, ring}]} */
function renderMolecule(ctx,C,mol){
  const f=C.B.f, pa=mol.atoms.map(a=>C.P(a.p));
  let z0=Infinity,z1=-Infinity; for(const q of pa) if(q){ z0=Math.min(z0,q.z); z1=Math.max(z1,q.z); }
  const cue=z=>z1>z0?0.62+0.38*clamp((z1-z)/(z1-z0),0,1):1;
  const items=[];
  pa.forEach((q,i)=>{ if(q) items.push({z:q.z,kind:0,i}); });
  mol.bonds.forEach(bd=>{ const A=pa[bd.a], B=pa[bd.b]; if(!A||!B) return;
    items.push({z:(3*A.z+B.z)/4,kind:1,from:bd.a,to:bd.b,bd}); items.push({z:(3*B.z+A.z)/4,kind:1,from:bd.b,to:bd.a,bd}); });
  mol.lps.forEach((lp,k)=>{ const q=C.P(v3.add(lp.c,v3.mul(lp.u,0.62*lp.dist))); if(q) items.push({z:q.z,kind:2,k}); });
  items.sort((a,b)=>b.z-a.z);
  const out={pa,rad:pa.map((q,i)=>q?Math.max(1.5,f*mol.atoms[i].r/q.z):0),lobes:[]};
  for(const it of items){
    if(it.kind===0){ const a=mol.atoms[it.i], q=pa[it.i], r=out.rad[it.i];
      ball(ctx,q.x,q.y,r,a.col,cue(q.z));
      if(a.ring){ ctx.beginPath(); ctx.arc(q.x,q.y,r+3,0,TAU); ctx.strokeStyle=a.ring; ctx.lineWidth=2; ctx.stroke(); }
    } else if(it.kind===1){
      const bd=it.bd, A=pa[it.from], B=pa[it.to], mx=(A.x+B.x)/2, my=(A.y+B.y)/2, c=cue(A.z);
      /* the offsets use the lower-to-higher index direction, so both halves agree */
      const lo=pa[Math.min(bd.a,bd.b)], hi=pa[Math.max(bd.a,bd.b)], Lp=Math.hypot(hi.x-lo.x,hi.y-lo.y)||1;
      const nx=-(hi.y-lo.y)/Lp, ny=(hi.x-lo.x)/Lp, s=f/A.z;
      const k=bd.order, w=k===1?0.08*s:k===2?0.05*s:0.04*s, gap=k===2?0.1*s:0.13*s;
      const offs=k===1?[0]:k===2?[-gap,gap]:[-gap,0,gap];
      for(const o of offs){ line2(ctx,A.x+nx*o,A.y+ny*o,mx+nx*o,my+ny*o,shade(COL.bond,0.72*c),Math.max(1.2,w));
        line2(ctx,A.x+nx*o,A.y+ny*o,mx+nx*o,my+ny*o,shade('#e4e8f0',0.55*c),Math.max(0.6,0.35*w)); }
    } else {
      const lp=mol.lps[it.k], tip=v3.add(lp.c,v3.mul(lp.u,lp.dist)), root=v3.add(lp.c,v3.mul(lp.u,0.1*lp.s));
      const qt=C.P(tip), qb=C.P(root); if(!qt||!qb) continue;
      const r1=f*0.2*lp.s/qt.z, r0=f*0.05*lp.s/qb.z;
      fillPoly(ctx,teardropPts(qb.x,qb.y,r0,qt.x,qt.y,r1),rgba(COL.lp,0.24),rgba(COL.lp,0.72),1);
      const dx=qt.x-qb.x, dy=qt.y-qb.y, L=Math.hypot(dx,dy), nx=L>1?-dy/L:1, ny=L>1?dx/L:0;
      const ex=L>1?dx/L:0, ey=L>1?dy/L:0, er=Math.max(1.4,0.13*r1);
      for(const sg of [-1,1]) dot(ctx,qt.x+sg*0.34*r1*nx+0.15*r1*ex,qt.y+sg*0.34*r1*ny+0.15*r1*ey,er,COL.lpE,null);
      if(lp.ring){ ctx.beginPath(); ctx.arc(qt.x,qt.y,r1+3,0,TAU); ctx.strokeStyle=lp.ring; ctx.lineWidth=2; ctx.stroke(); }
      out.lobes[it.k]={x:qt.x,y:qt.y,r:r1,z:qt.z};
    }
  }
  return out;
}
/* the bond-angle arcs of bond directions B, faded by PhET's rule; labels through the registry */
function drawAngleArcs(ctx,W,H,C,B){
  const nb=B.length, fwd=C.B.fwd, list=[];
  for(let i=0;i<nb;i++) for(let j=i+1;j<nb;j++){
    const deg=angleDeg(B[i],B[j]); let br=arcBrightness(B[i],B[j],fwd,nb);
    if(nb>2&&deg>179) br=0;
    if(br>0.02) list.push({i,j,deg,br});
  }
  list.sort((a,b)=>a.br-b.br);
  const arcPt=(a,b,t,r,semi)=>{ if(semi){ const ang=PI*t; return v3.add(v3.mul(a,r*Math.cos(ang)),v3.mul(semi,r*Math.sin(ang))); }
    return v3.mul(slerp(a,b,t),r); };
  const drawn=[];
  for(const p of list){
    const a=B[p.i], b=B[p.j];
    let semi=null;
    if(p.deg>179){ let q=vcross(fwd,a); if(vdot(q,q)<1e-8) q=vcross([0,0,1],a); if(vdot(q,q)<1e-8) q=[0,1,0]; semi=vnorm(q); }
    const pts=[]; for(let k=0;k<=24;k++){ const q=C.P(arcPt(a,b,k/24,0.42,semi)); if(q) pts.push([q.x,q.y]); }
    const o=C.P([0,0,0]); if(!o||pts.length<2) continue;
    fillPoly(ctx,[[o.x,o.y]].concat(pts),rgba(COL.pos,0.13*p.br),null);
    ctx.beginPath(); pts.forEach((q,k)=>{ if(k===0) ctx.moveTo(q[0],q[1]); else ctx.lineTo(q[0],q[1]); });
    ctx.strokeStyle=rgba(COL.pos,0.85*p.br); ctx.lineWidth=1.6; ctx.stroke();
    drawn.push(p);
  }
  /* labels brightest first, so the registry keeps the ones that read best */
  for(let k=drawn.length-1;k>=0;k--){ const p=drawn[k]; if(p.br<0.45) continue;
    let semi=null; const a=B[p.i], b=B[p.j];
    if(p.deg>179){ let q=vcross(fwd,a); if(vdot(q,q)<1e-8) q=vcross([0,0,1],a); if(vdot(q,q)<1e-8) q=[0,1,0]; semi=vnorm(q); }
    const q=C.P(arcPt(a,b,0.5,0.66,semi)); if(!q) continue;
    lab(ctx,W,H,q.x,q.y,fmt(p.deg,1)+'°',rgba(COL.pos,Math.min(1,0.35+0.65*p.br)),ANG_FONT,'center','middle');
  }
  return drawn;
}
function drawNames(ctx,W,H,b,x,e,showMol,showEl){
  const nm=geomNames(x,e); let y=b.y1-10;
  if(showEl&&HAS_LP){ lab(ctx,W,H,b.x+b.w/2,y,'electron geometry: '+(nm.el||'none'),COL.struct,BIG_FONT,'center','bottom'); y-=30; }
  if(showMol) lab(ctx,W,H,b.x+b.w/2,y,'molecule geometry: '+(nm.mol||'no bonds'),COL.pos,BIG_FONT,'center','bottom');
}

/* ================================================================== *
 *  view: the model (PhET's Model screen)                              *
 * ================================================================== */
const MODEL_CAP=HAS_LP
  ?'The central atom A and its electron pairs, relaxed to the least repulsion energy: bonds as grey sticks (one, two or three for the bond order) ending in an atom, lone pairs as cyan lobes holding two electrons. Every bond is drawn at one length and every lone pair at ρ of it, the radius the model puts it at. Drag a pair round the atom and let go: it slides back. Drag anywhere else to turn the molecule.'
  :'The central atom A and its bonds, relaxed to the least repulsion energy: grey sticks (one, two or three for the bond order) ending in an atom, every bond drawn at one length. Drag an atom round the centre and let go: it slides back. Drag anywhere else to turn the molecule.';
const MODEL_CAP_SHORT='Relaxed to the least repulsion energy; every bond at one length. Drag a pair to move it, elsewhere to turn.';
function modelGeo(ctx,W,H){ const L=stage3D(ctx,W,H,MODEL_CAP,MODEL_CAP_SHORT,260); return {L,C:molCam(L.b,1.32,ST.zoom)}; }
function modelMolecule(){
  const atoms=[{p:[0,0,0],r:R_CENTRE,col:COL.centre}], bonds=[], lps=[], gi=[];
  LIVE.groups.forEach((g,i)=>{
    if(g.order>0){ atoms.push({p:v3.mul(g.u,g.rr),r:R_OUTER,col:COL.outer,ring:i===LIVE.held?COL.live:null});
      bonds.push({a:0,b:atoms.length-1,order:g.order}); gi.push({i,atom:atoms.length-1}); }
    else if(ST.showLP){ lps.push({c:[0,0,0],u:g.u,dist:ST.rho*g.rr,s:1,ring:i===LIVE.held?COL.live:null}); gi.push({i,lp:lps.length-1}); }
  });
  return {atoms,bonds,lps,gi};
}
function drawModel(ctx,W,H,M){
  const {L,C}=modelGeo(ctx,W,H), b=L.b;
  frame(ctx,b,COL.edge);
  const mol=modelMolecule(), R=renderMolecule(ctx,C,mol);
  PICK=[];
  for(const g of mol.gi){
    if(g.atom!==undefined){ const q=R.pa[g.atom]; if(q) PICK.push({i:g.i,x:q.x,y:q.y,r:R.rad[g.atom],z:q.z}); }
    else { const lb=R.lobes[g.lp]; if(lb) PICK.push({i:g.i,x:lb.x,y:lb.y,r:lb.r,z:lb.z}); }
  }
  if(ST.showAngles) drawAngleArcs(ctx,W,H,C,LIVE.groups.filter(g=>g.order>0).map(g=>g.u));
  if(!LIVE.groups.length) lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.3,'no pairs: add a bond'+(HAS_LP?' or a lone pair':''),COL.dim,TITLE_FONT,'center','middle');
  lab(ctx,W,H,b.x+10,b.y+10,axeName(M.x,M.e)+(M.names.mol?'  '+lowName(M.names.mol):''),COL.text,TITLE_FONT,'left','top');
  if(HAS_LP&&M.e&&!ST.showLP) lab(ctx,W,H,b.x+10,b.y+30,M.e+' lone pair'+(M.e>1?'s':'')+' hidden (still pushing)',COL.dim,SM_FONT,'left','top');
  drawNames(ctx,W,H,b,M.x,M.e,ST.showMolName,ST.showElName);
  drawCap(ctx,L);
}
/* the pointer's direction on a sphere of radius Rs about the origin: the near
   intersection of the eye ray, or (off the silhouette) the ray's closest point */
function pointerDir(C,px,py,Rs){
  const B=C.B, cam=C.cam, f=B.f;
  const sx=(px-(C.b?C.b.x:0)-cam.W/2)/f, sy=-(py-(C.b?C.b.y:0)-cam.H/2)/f;
  const d=vnorm([B.fwd[0]+sx*B.right[0]+sy*B.up[0],B.fwd[1]+sx*B.right[1]+sy*B.up[1],B.fwd[2]+sx*B.right[2]+sy*B.up[2]]);
  const E=B.eye, ed=vdot(E,d), disc=ed*ed-(vdot(E,E)-Rs*Rs);
  const t=disc>=0?-ed-Math.sqrt(disc):-ed;
  return vnorm([E[0]+t*d[0],E[1]+t*d[1],E[2]+t*d[2]]);
}

/* ================================================================== *
 *  view: real molecules (PhET's second screen)                        *
 * ================================================================== */
const REAL_CAP=HAS_LP
  ?'A molecule from PhET’s table, its atoms where the measured bond angles put them. Every bond is drawn at one length (the measured lengths are in the readout). The central lone pairs sit where the ideal slots put them once the ideal bonds are fitted onto the real ones; the outer atoms’ own lone pairs are drawn but push on nothing. The Model chip turns the same molecule into the model’s least-energy shape. Drag to turn it.'
  :'A molecule from PhET’s table, its atoms where the measured bond angles put them, every bond drawn at one length (the measured lengths are in the readout). None of these five has a lone pair on its central atom, so the measured shape is the ideal one. Drag to turn it.';
const REAL_CAP_SHORT='PhET’s measured geometry, every bond at one length. Drag to turn it.';
function realGeo(ctx,W,H){ const L=stage3D(ctx,W,H,REAL_CAP,REAL_CAP_SHORT,260); return {L,C:molCam(L.b,1.45,ST.zoom)}; }
function drawReal(ctx,W,H,M){
  const {L,C}=realGeo(ctx,W,H), b=L.b, m=REAL[M.id], sh=M.shown, bl=LIVE.realBlend;
  frame(ctx,b,COL.edge);
  const atoms=[{p:[0,0,0],r:ATOM_R[m.centre],col:ELCOL[m.centre]}], bonds=[], lps=[];
  sh.B.forEach(u=>{ atoms.push({p:u,r:ATOM_R[m.outer],col:ELCOL[m.outer]}); bonds.push({a:0,b:atoms.length-1,order:m.order}); });
  if(ST.showLP){
    sh.LP.forEach(u=>lps.push({c:[0,0,0],u,dist:RHO_PHET+(ST.rho-RHO_PHET)*bl,s:1}));
    if(ST.showOuterLP) sh.B.forEach(u=>{ for(const w of outerLonePairs(u,m.olp)) lps.push({c:u,u:w,dist:0.36,s:0.55}); });
  }
  renderMolecule(ctx,C,{atoms,bonds,lps});
  if(ST.showAngles) drawAngleArcs(ctx,W,H,C,sh.B);
  lab(ctx,W,H,b.x+10,b.y+10,formulaText(M.id)+'   '+(bl<0.02?'measured':bl>0.98?'the model at ρ = '+fmt(ST.rho,2):'measured → the model, '+fmt(100*bl,0)+' %'),bl<0.5?COL.ref:COL.pos,BIG_FONT,'left','top');
  lab(ctx,W,H,b.x+10,b.y+38,axeName(M.rx,M.re)+'  '+lowName(M.rnames.mol),COL.text,TITLE_FONT,'left','top');
  const key=[m.centre,m.outer].concat(HAS_LP&&ST.showLP&&M.re?['lone pair']:[]);
  let X=b.x+12; const Y=b.y+64;
  for(const k of key){ if(k==='lone pair') dot(ctx,X+5,Y,4.5,rgba(COL.lp,0.5),COL.lp,1); else dot(ctx,X+5,Y,4.5,ELCOL[k],null);
    lab(ctx,W,H,X+14,Y,k,COL.dim,SM_FONT,'left','middle'); X+=k.length*6+34; }
  drawNames(ctx,W,H,b,M.rx,M.re,ST.showMolName,ST.showElName);
  drawCap(ctx,L);
}
