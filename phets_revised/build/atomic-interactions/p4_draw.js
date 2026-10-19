
/* ================================================================== *
 *  sim-specific drawing: the atom band, the force arrows, the well    *
 *  panel.  Geometry is built by one function that both the drawing    *
 *  and the hit-testing read, so a dragged atom and a drawn atom can   *
 *  never be in different places (waveguides Known-bad).               *
 * ================================================================== */

/* The house #hint (HTML: left 14 px, bottom 11 px) sits exactly on the last
   line of a caption that stageLayout anchors to the canvas bottom, and the
   display-list capture cannot see it because the hint is not canvas.  Every
   view here lays out to H - HINT_H and the layout sweep asserts no canvas text
   enters that corner (wave-on-a-string Known-bad; the fix is
   build/gravity-force-lab/p4_lab.js's). */
const HINT_H=18;
function stageLayoutH(ctx,W,H,capFull,capShort,nB,frac,nBN){
  return stageLayout(ctx,W,H-HINT_H,capFull,capShort,nB,frac,nBN);
}
/* The floating readout covers the top right of the stage (about 317 x 470 px),
   so every view reserves it in the label registry rather than hoping — a
   callout placed there is invisible (standard_candle Known-bad). */
function reserveReadout(W,H){ if(W>=900) LABELS.push([W-13-280-24,0,W,470]); }
/* a legend's own box, registered so lab() dodges it */
function regLegend(r){ if(r) LABELS.push([r.x,r.y,r.x1,r.y1]); }
/* the room a wrapped note needs under a panel whose x-axis label already
   reaches b.y1 + 34 (measure it, never guess: wrapped text has no fixed
   height — adiabatic_expansion Known-bad) */
function noteRoom(ctx,txt,w){ return wrapText(ctx,txt,w,SM_FONT).length*13+46; }
function drawNote(ctx,b,txt){ caption(ctx,b.x,b.y1+38,txt,b.w,'#767e92',SM_FONT); }
/* Reserve room for a wrapped note under a panel and return the shrunken box.
   The shrink has a floor, so on a narrow stage the room asked for may not be
   available; `fits` says whether it was, and drawNoteIf then draws nothing
   rather than printing the note over the stage caption.  A sparse view is not
   a broken view (pulsar Known-bad) — the picture is what matters. */
function noteFit(ctx,limitY,b,txt,shortTxt){
  for(const t of (shortTxt?[txt,shortTxt]:[txt])){
    const lines=wrapText(ctx,t,b.w,SM_FONT).length;
    const nb=box(b.x,b.y,b.w,Math.max(80,b.h-(lines*13+46)));
    if((nb.y1+38+lines*13)<=(limitY-8)) return {b:nb,txt:t,fits:true};
  }
  const lines=wrapText(ctx,shortTxt||txt,b.w,SM_FONT).length;
  return {b:box(b.x,b.y,b.w,Math.max(80,b.h-(lines*13+46))),txt:txt,fits:false};
}
/* the y a note under `main` must stay above: the stage caption when there is
   no bottom row, the bottom row's own title when there is */
function noteLimit(L){
  return L.bottom&&L.bottom.length?L.bottom[0].y-26:L.capY;
}
function drawNoteIf(ctx,N){ if(N.fits) drawNote(ctx,N.b,N.txt); }
/* tick counts derived from the box, not guessed: six y-ticks in a 150-px panel
   put '-1.0' on top of '-0.5' (adiabatic_expansion Known-bad) */
function nyFor(b){ return Math.max(2,Math.min(6,Math.floor(b.h/52))); }
/* A y tick landing exactly on the bottom of the frame puts its label in the
   corner, where the leftmost x-tick label already is — axes() draws both and
   neither knows about the other.  Drop the floor a little when that happens. */
function noCornerTick(lo,hi,ny){
  const t=ticksFor(Math.min(lo,hi),Math.max(lo,hi),ny);
  return (t.length&&Math.abs(t[0]-lo)<0.02*(hi-lo))?lo-0.09*(hi-lo):lo;
}
function nxFor(b){ return Math.max(2,Math.min(6,Math.floor(b.w/115))); }

/* n boxes side by side inside b (stacked when b is too narrow to split) */
function splitRow(b,n,gut){
  const g=gut===undefined?54:gut;
  if(n<=1) return [b];
  if(b.w<300*n){
    /* stacked: the gap must clear the upper panel's x-tick labels AND axis
       title (34 px) plus the lower panel's own title (14 px) */
    const hh=(b.h-64*(n-1))/n, out=[];
    for(let i=0;i<n;i++) out.push(box(b.x,b.y+i*(hh+64),b.w,hh));
    return out;
  }
  const w=(b.w-g*(n-1))/n, out=[];
  for(let i=0;i<n;i++) out.push(box(b.x+i*(w+g),b.y,w,b.h));
  return out;
}

/* a shaded sphere, drawn as concentric arcs so the display-list recorder sees
   real geometry (it has no ellipse() and does not carry a scaled arc through
   restore()) */
function drawAtom(ctx,cx,cy,R,col,sym,dim){
  const n=7;
  for(let i=n;i>=1;i--){
    const t=i/n, rr=R*t;
    ctx.beginPath();
    ctx.arc(cx-R*0.22*(1-t),cy-R*0.24*(1-t),rr,0,TAU);
    ctx.fillStyle=shade(col,dim?0.20+0.30*(1-t):0.30+0.55*(1-t));
    ctx.fill();
  }
  ctx.beginPath(); ctx.arc(cx,cy,R,0,TAU);
  ctx.strokeStyle=dim?rgba(col,0.35):rgba(col,0.85); ctx.lineWidth=1.2; ctx.stroke();
  if(sym&&R>11){
    ctx.fillStyle='#0a0c12'; ctx.font='bold '+Math.min(17,Math.max(9,R*0.5))+'px -apple-system, sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(sym,cx,cy);
  }
}

/* One force arrow, horizontal, with its own head.  `px` is pixels per pN and
   `cap` the longest arrow the stage can hold; a capped arrow gets a chevron at
   its tip, because a clipped bar that looks like a short one is a lie about
   the number (the waterfall lesson, on an arrow). */
function forceArrow(ctx,x,y,F,px,col,cap){
  const L=F*px, C=cap||300;
  if(Math.abs(L)<1.5) return 0;
  const s=L>0?1:-1, cut=Math.abs(L)>C, Lc=Math.min(Math.abs(L),C)*s;
  ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+Lc,y);
  const hh=Math.min(10,Math.abs(Lc)*0.45);
  ctx.moveTo(x+Lc,y); ctx.lineTo(x+Lc-hh*s,y-hh*0.55);
  ctx.moveTo(x+Lc,y); ctx.lineTo(x+Lc-hh*s,y+hh*0.55);
  if(cut) for(const d of [5,10]){
    ctx.moveTo(x+Lc+d*s,y-6); ctx.lineTo(x+Lc+(d+4)*s,y); ctx.lineTo(x+Lc+d*s,y+6); }
  ctx.strokeStyle=col; ctx.lineWidth=2.2; ctx.lineCap='round'; ctx.stroke();
  ctx.lineCap='butt';
  return cut?NaN:Lc;
}

/* The geometry of the two-atoms view.  Returns the boxes, the shared r->x
   mapping, the drawn atom radii and the factor by which they had to be
   reduced (printed on the canvas whenever it is not 1). */
function atomsGeom(ctx,W,H,M){
  const P=M.P, st=M.st;
  const L=stageLayoutH(ctx,W,H,ATOMS_CAP_FULL,ATOMS_CAP_SHORT,0,0,0);
  const b=L.main;
  const xHi=P.rHi;
  const gx=b.x+58, gw=Math.max(120,b.x1-gx-14);
  const X=r=>gx+gw*(r-xLoRef.v)/(xHi-xLoRef.v),
        wx=px=>xLoRef.v+(px-gx)*(xHi-xLoRef.v)/gw;
  const xLoRef={v:0};
  /* The axis starts a little LEFT of zero so the pinned atom, whose centre is
     r = 0, is drawn whole instead of half off the stage.  Its left edge is the
     drawn radius, which depends on the scale, which depends on the span — two
     passes are enough, since each only shrinks the atom. */
  const rBig=Math.max(P.rA,P.rB);
  let xLo=0, sx=gw/(xHi-xLo), bandH=0, fac=1;
  for(let pass=0;pass<3;pass++){
    sx=gw/(xHi-xLo);
    bandH=clamp(2*rBig*sx+78,92,Math.max(92,0.44*b.h));
    /* the two force labels sit 13 and 27 px above the atom, so the half-band
       has to hold the radius AND 36 px of label */
    fac=Math.min(1,(bandH/2-36)/Math.max(1e-9,rBig*sx));
    xLo=-1.06*P.rA*fac;
  }
  const band={x:gx,y:b.y,w:gw,h:bandH,y1:b.y+bandH,cy:b.y+bandH*0.5};
  /* the note is built here, not in the drawing, because its wrapped height
     decides how much room the graph gets */
  const apx=arrowScale(P,gw), acap=Math.min(300,0.36*gw);
  let note='the atoms are drawn to the r axis of the graph'
    +(fac<0.995?', reduced x'+fmt(fac,2)+' to fit the band':'')
    +' · V leaves the top of the box below r/σ ≈ 0.90';
  let short='atoms to the r axis'+(fac<0.995?' x'+fmt(fac,2):'');
  if(st.forces==='hidden'){ note+=' · forces hidden, as PhET starts them'; }
  else { note+=' · force arrows: 1 pN = '+fmt(apx,1)+' px, cut off at '
           +fmt(acap,0)+' px with a chevron';
         short+=' · 1 pN = '+fmt(apx,1)+' px'; }
  const top=b.y+bandH+16;
  const N=noteFit(ctx,noteLimit(L),box(gx,top,gw,Math.max(90,b.y1-top)),note,short);
  xLoRef.v=xLo;
  return {L,b,band,gb:N.b,note:N,X,wx,sx,fac,xHi,xLo,apx,
          arrowCap:acap,
          rA:P.rA*sx*fac,rB:P.rB*sx*fac};
}

/* the caption text lives here so the geometry function can measure it */
const ATOMS_CAP_FULL='The two atoms sit on the same horizontal scale as the curve below them, so the movable atom’s centre is directly above its own point on the potential. Drag it. The curve is the Lennard-Jones potential for the pair; the magenta rule marks the current separation and the dot marks V(r) there. Where the curve slopes down to the right the atoms attract, where it slopes up they repel, and at the bottom — the dashed line at r_min = 2^(1/6) sigma — the force is exactly zero. Forces are drawn as arrows on the movable atom to the printed scale; PhET draws them the same way and lets you show the two halves separately.';
const ATOMS_CAP_SHORT='Two atoms and their Lennard-Jones potential on one r axis. Drag the right-hand atom; the arrows are the force to the printed scale.';
const WELL_CAP_FULL='The same well, and beneath it the force it produces. F(r) = -dV/dr is the slope of the curve above, turned upside down: it crosses zero exactly at the bottom of the well, it is most negative (most attractive) at the inflection of V, and it rises without bound as the atoms are pushed together. The residual panel is the closed-form force minus a Richardson-extrapolated central difference of V, divided by the force scale 24 eps/r — it is machine noise, which is what “the force is exactly minus the derivative” looks like when you check it numerically.';
const WELL_CAP_SHORT='V(r) above, F(r) = -dV/dr below, and the residual between the closed-form force and a numerical derivative of V.';
const MOTION_CAP_FULL='Release the movable atom and the well does the rest. The trace is r(t); the dashed rules are the two turning points, where the potential curve rises to meet the total energy, and they are exact — with u = (sigma/r)^6 the condition V(r) = E is a quadratic whose roots satisfy u_in + u_out = 1. The ledger underneath is the energy: kinetic and potential trade back and forth while their sum stays flat, to the integrator’s accuracy. The phase portrait closes on itself for a bound orbit and runs away past the separatrix E = 0.';
const MOTION_CAP_SHORT='r(t) with its exact turning points, the energy ledger, and the phase portrait with the E = 0 separatrix.';
const SMALL_CAP_FULL='Every smooth minimum is a parabola close enough in, and this is how close. The orange curve is the harmonic approximation -eps + V″(r_min)(r - r_min)²/2 through the bottom of the well; the period of a small oscillation is 2 pi / sqrt(V″(r_min)/mu), with mu the mass of whatever is actually free to move. The panel underneath measures how fast the true period leaves that value as the amplitude grows: the points are the regularised quadrature, the orange line is Landau’s anharmonic prediction T = T0 [1 + (91/4) a²/r_min²] for this well, and the two agree to a part in 10^5 until the orbit is a tenth of r_min wide.';
const SMALL_CAP_SHORT='The harmonic fit at the bottom of the well, and how fast the real period leaves 2 pi / omega as the amplitude grows.';
const PAIRS_CAP_FULL='Every pair PhET offers, on one axis, in PhET’s own parameters (solid) and in the literature’s (dashed). PhET’s sigma is systematically the literature r_min rather than the literature sigma, because PhET sets sigma to twice the van der Waals radius and that radius is measured at the bottom of the well, a factor 2^(1/6) = 1.1225 further out. Neon and argon land within 2% of the literature r_min and 10% away from the literature sigma. The oxygen pair matches neither: PhET’s own States-of-Matter constants carry 113 K and 365 pm for O2, while this screen uses 1000 K and 200 pm.';
const PAIRS_CAP_SHORT='PhET’s seven wells against the literature, the combining rules, and what PhET’s sigma really is.';
const STEP_CAP_FULL='The same release, integrated three ways. The left panel is the worst excursion of the total energy over exactly one period, against the step size, on log-log axes: the slope is the order of the method, and the fitted slopes are printed. The right panel runs at a fixed 1 fs step and watches the error for twenty periods. Velocity Verlet and semi-implicit Euler are symplectic, so their energy error oscillates and never grows; forward Euler is not, and its error grows without bound whatever the step size. PhET uses semi-implicit Euler; this sim uses velocity Verlet.';
const STEP_CAP_SHORT='Energy error against step size (the order) and against time (the boundedness), for three integrators.';

/* the well panel: V/eps against r, with the three landmarks */
function drawWellPanel(ctx,bx,M,opt){
  const P=M.P, C=M.C||wellCurve(P,240), o=opt||{};
  const ylo=o.ylo===undefined?-1.32:o.ylo, yhi=o.yhi===undefined?2.4:o.yhi;
  const xlo=o.xlo===undefined?0:o.xlo, xhi=o.xhi===undefined?P.rHi:o.xhi;
  axesR(ctx,bx,xlo,xhi,ylo,yhi,{xlab:'separation r, pm',ylab:'V(r) / ε',
    title:o.title,nx:nxFor(bx),ny:nyFor(bx),xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  /* zero line and the well floor */
  polyline(ctx,bx,[xlo,xhi],[0,0],xlo,xhi,ylo,yhi,'#3a4152',1,[3,4]);
  polyline(ctx,bx,[xlo,xhi],[-1,-1],xlo,xhi,ylo,yhi,rgba(COL.struct,0.35),1,[3,4]);
  polyline(ctx,bx,C.xs,C.ys,xlo,xhi,ylo,yhi,COL.pos,2);
  const Xof=r=>bx.x+bx.w*(r-xlo)/(xhi-xlo), Yof=v=>bx.y1-bx.h*(v-ylo)/(yhi-ylo);
  /* sigma: the zero crossing */
  if(P.sig>=xlo&&P.sig<=xhi){
    polyline(ctx,bx,[P.sig,P.sig],[ylo,0],xlo,xhi,ylo,yhi,rgba(COL.struct,0.5),1,[2,3]);
    dot(ctx,Xof(P.sig),Yof(0),3.4,COL.struct,'#0a0c12',1);
  }
  /* r_min: the bottom */
  if(P.rmin>=xlo&&P.rmin<=xhi){
    polyline(ctx,bx,[P.rmin,P.rmin],[ylo,-1],xlo,xhi,ylo,yhi,rgba(COL.struct,0.5),1,[2,3]);
    dot(ctx,Xof(P.rmin),Yof(-1),3.4,COL.struct,'#0a0c12',1);
  }
  return {Xof,Yof,xlo,xhi,ylo,yhi};
}
