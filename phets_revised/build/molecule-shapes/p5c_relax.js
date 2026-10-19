/* ================================================================== *
 *  view: the relaxation                                               *
 * ================================================================== */
const RELAX_CAP=HAS_LP
  ?'Plain gradient descent on the repulsion energy from a random start (new start: the button or space), with no steering toward the VSEPR slots. Left: the pairs of the model view’s molecule gliding over their spheres, magenta trails behind them. Right: how far the energy is above the VSEPR minimum, on a log scale; orange lines mark the other arrangements the pairs can get stuck in. Drag to turn the sphere.'
  :'Plain gradient descent on the repulsion energy from a random start (new start: the button or space). Left: the model view’s bonds gliding over the sphere, magenta trails behind them. Right: how far the energy is above the ideal shape’s, on a log scale: it falls to rounding error, because for two to six equal pairs the ideal shape is the only minimum. Drag to turn the sphere.';
const RELAX_CAP_SHORT='Gradient descent from a random start; right, the energy above the minimum. New start: space.';
const RL_FLOOR=-12, RL_TOP=1;
/* decades on the log axis, thinned when the panel is short */
function relaxTicks(pb){ return pb.h<130?[-12,-6,0]:[-12,-9,-6,-3,0]; }
function pow10(v){ return '10'+(v<0?'⁻':'')+String(Math.abs(v)).split('').map(c=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[+c]).join(''); }
function relaxGeo(ctx,W,H){
  const L=stage3D(ctx,W,H,RELAX_CAP,RELAX_CAP_SHORT,260), b=L.b;
  if(L.narrow){ const h1=Math.floor(b.h*0.55); return {L,sb:box(b.x,b.y,b.w,h1),pb:box(b.x+54,b.y+h1+34,b.w-70,b.h-h1-80)}; }
  const w1=Math.floor(b.w*0.5);
  return {L,sb:box(b.x,b.y,w1,b.h),pb:box(b.x+w1+64,b.y+28,b.w-w1-80,b.h-86)};
}
function drawRelax(ctx,W,H,M){
  const G=relaxGeo(ctx,W,H), sb=G.sb, pb=G.pb;
  frame(ctx,sb,COL.edge);
  if(!RELAX.U){
    lab(ctx,W,H,sb.x+sb.w/2,sb.y+sb.h/2,'fewer than two pairs in the model view: nothing to relax',COL.dim,TITLE_FONT,'center','middle');
    axesR(ctx,pb,0,200,RL_FLOOR,RL_TOP,{yticks:relaxTicks(pb),yfmt:pow10,xfmt:v=>fmt(v,0),xlab:'descent step',ylab:'U − U('+BESTNAME+')',title:titleFor(pb,'the energy above the '+(HAS_LP?'VSEPR minimum':'ideal shape’s'),'U − U('+BESTNAME+')')});
    drawCap(ctx,G.L); return;
  }
  const C=molCam(sb,1.35,ST.zoom), e=RELAX.e;
  /* the spheres the pairs live on */
  for(const [r,al] of (e?[[1,0.35],[ST.rho,0.25]]:[[1,0.35]])){
    for(const ax of [0,1,2]){ const pts=[]; for(let k=0;k<=48;k++){ const t=TAU*k/48, c=Math.cos(t)*r, s=Math.sin(t)*r;
      pts.push(ax===0?[c,s,0]:ax===1?[c,0,s]:[0,c,s]); } poly3(ctx,C,pts,rgba(COL.struct,al*0.5),0.8,null,true); }
  }
  /* the trails */
  for(let i=0;i<RELAX.U.length;i++){ const r=RELAX.R[i], pts=RELAX.trail.map(T=>v3.mul(T[i],r)).concat([v3.mul(RELAX.U[i],r)]);
    if(pts.length>1) poly3(ctx,C,pts,rgba(COL.live,0.7),1.4,null,true); }
  const atoms=[{p:[0,0,0],r:R_CENTRE,col:COL.centre}], bonds=[], lps=[];
  RELAX.U.forEach((u,i)=>{ if(i<e) lps.push({c:[0,0,0],u,dist:ST.rho,s:1}); else { atoms.push({p:u,r:R_OUTER,col:COL.outer}); bonds.push({a:0,b:atoms.length-1,order:1}); } });
  renderMolecule(ctx,C,{atoms,bonds,lps});
  lab(ctx,W,H,sb.x+10,sb.y+10,axeName(RELAX.x,RELAX.e)+'  start '+(RELAX.seed+1)+'  step '+RELAX.step,COL.text,TITLE_FONT,'left','top');
  /* the energy above the VSEPR minimum */
  const Emin=M.eqE, xs=[], ys=[], nh=RELAX.hist.length;
  for(let k=0;k<nh;k++){ xs.push(k); ys.push(Math.log10(Math.max(RELAX.hist[k]-Emin,1e-15))); }
  const xmax=Math.max(200,Math.ceil(nh/100)*100);
  axesR(ctx,pb,0,xmax,RL_FLOOR,RL_TOP,{yticks:relaxTicks(pb),yfmt:pow10,xfmt:v=>fmt(v,0),xlab:'descent step',ylab:'U − U('+BESTNAME+')',
    title:titleFor(pb,'the energy above the '+(HAS_LP?'VSEPR minimum':'ideal shape’s'),'U − U('+BESTNAME+')')});
  const lad=isomerLadder(RELAX.x,RELAX.e,ST.rho);
  lad.forEach((f,i)=>{ if(i===0) return; const y=Math.log10(f.E-Emin);
    polyline(ctx,pb,[0,xmax],[y,y],0,xmax,RL_FLOOR,RL_TOP,rgba(COL.ref,0.8),1.2,[5,4]);
    lab(ctx,W,H,pb.x1-4,pb.y1-pb.h*(y-RL_FLOOR)/(RL_TOP-RL_FLOOR)-4,'isomer '+(i+1),COL.ref,SM_FONT,'right','bottom'); });
  polyline(ctx,pb,xs,ys,0,xmax,RL_FLOOR,RL_TOP,COL.pos,1.8);
  const v=M.verdict;
  if(v) lab(ctx,W,H,pb.x+pb.w/2,pb.y+14,v.rank===0?'reached the '+(HAS_LP?'VSEPR':'ideal')+' shape':v.rank>0?'stuck in isomer '+(v.rank+1)+', a local minimum':'stuck in another local minimum',v.rank===0?COL.pos:COL.ref,LAB_FONT,'center','top');
  lab(ctx,W,H,pb.x+4,pb.y1-6,'rounding error',COL.dim,SM_FONT,'left','bottom');
  drawCap(ctx,G.L);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='model') drawModel(ctx,W,H,M);
  else if(M.view==='real') drawReal(ctx,W,H,M);
  else if(M.view==='table') drawTable(ctx,W,H,M);
  else if(M.view==='squeeze') drawSqueeze(ctx,W,H,M);
  else drawRelax(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712,onView:null};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame: the live molecule in the model view, the Real/Model blend, the descent */
  S.step=function(dt){
    const v=ST.view;
    if(v==='model') return liveStep(dt);
    if(v==='real') return realStep(dt);
    if(v==='relax'){ relaxEnsure(); if(RELAX.done) return false; relaxAdvance(RELAX.step<120?2:12); return true; }
    return false;
  };
  S.resetCam=function(){ ST.camTheta=DEFAULTS.camTheta; ST.camPhi=DEFAULTS.camPhi; ST.zoom=1; };
  S.wheel=function(dy){ if(ST.view==='squeeze'||ST.view==='table') return false; ST.zoom=clamp(ST.zoom*(dy>0?0.93:1.075),0.5,2.5); return true; };
  /* the pointer: grab a pair (model view), set rho (squeeze), click a class (table),
     otherwise turn the camera */
  S.pointer=function(type,x,y){
    const v=ST.view, ctx=canvas.getContext('2d');
    if(type==='down'){
      DRAG.x0=x; DRAG.y0=y; DRAG.lx=x; DRAG.ly=y; DRAG.moved=0;
      if(v==='model'){ let best=null;
        for(const p of PICK){ const d=Math.hypot(x-p.x,y-p.y); if(d<=p.r+6&&(!best||p.z<best.z)) best=p; }
        if(best){ DRAG.what='pair'; LIVE.held=best.i; LIVE.anim=true; return true; } }
      if(v==='squeeze'){ const G=squeezeGeo(ctx,S.W,S.H), b=G.top;
        if(x>=b.x&&x<=b.x1&&y>=b.y&&y<=b.y1){ DRAG.what='rho'; ST.rho=rhoAtX(b,x); LIVE.anim=true; return true; } return false; }
      DRAG.what='orbit'; return true;
    }
    if(type==='move'){
      if(!DRAG.what) return false;
      const dx=x-DRAG.lx, dy=y-DRAG.ly; DRAG.lx=x; DRAG.ly=y; DRAG.moved+=Math.abs(dx)+Math.abs(dy);
      if(DRAG.what==='orbit'){ ST.camTheta-=dx*0.0075; ST.camPhi=clamp(ST.camPhi+dy*0.006,-1.45,1.45); return true; }
      if(DRAG.what==='pair'){ const g=LIVE.groups[LIVE.held]; if(!g) return false;
        g.u=pointerDir(modelGeo(ctx,S.W,S.H).C,x,y,g.order===0?ST.rho:1); LIVE.anim=true; return true; }
      if(DRAG.what==='rho'){ ST.rho=rhoAtX(squeezeGeo(ctx,S.W,S.H).top,x); LIVE.anim=true; return true; }
      return false;
    }
    /* up */
    const had=DRAG.what!==null;
    if(DRAG.what==='pair'){ LIVE.held=-1; LIVE.fitKey=''; LIVE.anim=true; }
    if(DRAG.what==='orbit'&&v==='table'&&DRAG.moved<4){ const h2=hitAt(DRAG.x0,DRAG.y0);
      if(h2){ liveLoad(h2.x,h2.e); DRAG.what=null; if(S.onView) S.onView('model'); else ST.view='model'; return true; } }
    DRAG.what=null;
    return had;
  };
  return S;
}
