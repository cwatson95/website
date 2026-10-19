
/* ================================================================== *
 *  views C-F, the dispatch and the scene object                       *
 * ================================================================== */

/* ---------------------------------------------- view C: the press ------- */
const PRESS_CAP_FULL='PhET&rsquo;s chamber pool. Two shafts of very different width, '+fmt(CH_L_W,2)+' m and '
  +fmt(CH_R_W,2)+' m across — '+fmt(CH_A_L,2)+' and '+fmt(CH_A_R,2)+' m² with the '+fmt(DEPTH_OUT,0)+' m out-of-page '
  +'depth this file gives every pool — joined below by a chamber full of fluid. Load the small one and the pressure you '
  +'add, F/A, appears everywhere in the fluid at once, so the large piston feels '+fmt(CH_RATIO,1)+' times the force. '
  +'What you do not get is distance: the small side falls '+fmt(CH_RATIO,1)+' times as far as the large side rises, and '
  +'the work is the same either way. The panel on the right is the whole of it: displacement against load, straight '
  +'lines whose slopes are in the ratio of the areas.';
const PRESS_CAP_SHORT='PhET&rsquo;s chamber pool: Pascal&rsquo;s principle, with the force multiplied by the area ratio '
  +fmt(CH_RATIO,1)+' and the distance divided by it.';

function drawMasses(ctx,W,H,map,M,st){
  const cx=(CH_L_SHAFT.x0+CH_L_SHAFT.x1)/2;
  /* the platform sits on the small column */
  worldPoly(ctx,map,[[CH_L_SHAFT.x0-0.06,M.P.yL],[CH_L_SHAFT.x1+0.06,M.P.yL],
                     [CH_L_SHAFT.x1+0.06,M.P.yL+0.05],[CH_L_SHAFT.x0-0.06,M.P.yL+0.05]],
            '#39405a','#6b7285',1.2);
  let y=M.P.yL+0.05;
  for(const o of M.onMasses){
    worldPoly(ctx,map,[[cx-o.w/2,y],[cx+o.w/2,y],[cx+o.w/2,y+o.h],[cx-o.w/2,y+o.h]],COL.mass,'#0b0f18',1.4);
    /* a label only where the box is tall enough to hold one: at 560 px the
       two 0.25 m masses are 9 px high and their labels sat on each other */
    if(map.Y(y)-map.Y(y+o.h)>=15)
      labFixed(ctx,map.X(cx),map.Y(y+o.h/2),fmt(o.m,0)+' kg','#0b0f18','bold 11px -apple-system, sans-serif','center','middle');
    LABELS.push([map.X(cx-o.w/2),map.Y(y+o.h),map.X(cx+o.w/2),map.Y(y)]);
    y+=o.h;
  }
  if(M.M>0) lab(ctx,W,H,map.X(cx)-map.s*0.30,map.Y(M.P.yL+0.05),fmt(M.M,0)+' kg',COL.mass,SM_FONT,'right');
  else lab(ctx,W,H,map.X(cx),map.Y(M.P.yL+0.30),'nothing on the platform',COL.dim,SM_FONT,'center');
}

function pressPanel(ctx,W,H,b,M,st){
  const xs=[],dl=[],dr=[],dh=[];
  for(let i=0;i<=60;i++){ const m=CH_MASS_MAX*i/60, P=pascal(m,M.rho,M.g,st.atmosphere);
    xs.push(m); dl.push(P.dL); dr.push(P.dR); dh.push(P.dh); }
  const hi=Math.max(CH_WATER*1.15,Math.max.apply(null,dh)*1.08);
  axesReg(ctx,b,0,CH_MASS_MAX,0,hi,{nx:5,ny:4,xlab:'load on the small piston, kg',ylab:'displacement, m',
    title:titleFor(b,'displacement against load: two straight lines','displacement vs load')});
  polyline(ctx,b,[0,CH_MASS_MAX],[CH_WATER,CH_WATER],0,CH_MASS_MAX,0,hi,rgba(COL.ref,0.8),1.3,[5,4]);
  lab(ctx,W,H,b.x+5,b.y1-b.h*CH_WATER/hi-11,'the shaft bottoms out',COL.ref,SM_FONT,'left');
  polyline(ctx,b,xs,dl,0,CH_MASS_MAX,0,hi,COL.live,1.8);
  polyline(ctx,b,xs,dr,0,CH_MASS_MAX,0,hi,COL.struct,1.8);
  polyline(ctx,b,xs,dh,0,CH_MASS_MAX,0,hi,COL.pos,1.6,[6,3]);
  marker(ctx,b,0,CH_MASS_MAX,0,hi,M.M,M.P.dL,COL.live);
  marker(ctx,b,0,CH_MASS_MAX,0,hi,M.M,M.P.dR,COL.struct);
  legendReg(ctx,b,[[COL.live,'small side falls'],[COL.struct,'large side rises'],
                    [COL.pos,'they separate by Δh']]);
  lab(ctx,W,H,b.x+4,b.y1-8,'slopes in the ratio '+fmt(CH_RATIO,2)+' = A2/A1',COL.pos,SM_FONT,'left');
}

function drawPressView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,PRESS_CAP_FULL,PRESS_CAP_SHORT,0,0);
  const S=splitMain(L,W,0.56,1);
  const map=drawPool(ctx,W,H,S.pool,'chamber',null,M.rho,st,M.P);
  /* the rest level, so the displacement is visible as a displacement */
  seg(ctx,map,[CH_L_SHAFT.x0-0.1,CH_REST],[CH_R_SHAFT.x1+0.1,CH_REST],rgba(COL.ref,0.55),1.2,[4,3]);
  drawGauge(ctx,W,H,map,st.gAx,st.gAy,M.A,'A',COL.live,st);
  drawGauge(ctx,W,H,map,st.gBx,st.gBy,M.B,'B',COL.pos,st);
  drawMasses(ctx,W,H,map,M,st);
  lab(ctx,W,H,map.X(CH_L_SHAFT.x0)-8,map.Y(CH_REST),'rest level',COL.ref,SM_FONT,'right');
  lab(ctx,W,H,map.X((CH_L_SHAFT.x0+CH_L_SHAFT.x1)/2),map.Y(CH_OPEN_BOT)+12,
      'A1 = '+fmt(CH_A_L,2)+' m²',COL.live,SM_FONT,'center');
  lab(ctx,W,H,map.X((CH_R_SHAFT.x0+CH_R_SHAFT.x1)/2),map.Y(CH_OPEN_BOT)+12,
      'A2 = '+fmt(CH_A_R,2)+' m²',COL.struct,SM_FONT,'center');
  if(M.M>0){
    lab(ctx,W,H,map.X(CH_L_SHAFT.x0)-8,map.Y((CH_REST+M.P.yL)/2),'↓ '+fmt(M.P.dL,3)+' m',COL.live,SM_FONT,'right');
    /* inside the stage, not past its right edge: at +8 past the wide shaft it
       landed in the neighbouring panel's y-label gutter */
    lab(ctx,W,H,map.X(CH_R_SHAFT.x0)-8,map.Y((CH_REST+M.P.yR)/2),'↑ '+fmt(M.P.dR,3)+' m',COL.struct,SM_FONT,'right');
  }
  lab(ctx,W,H,map.X(CH_LEFT.x0),map.Y(-POOL_H)+15,
      'true proportion · '+fmt(DEPTH_OUT,0)+' m out of the page',COL.dim,SM_FONT,'left');
  if(M.P.capped) lab(ctx,W,H,map.X((CH_L_SHAFT.x0+CH_R_SHAFT.x1)/2),map.Y(0.42),
    'the small column has bottomed out — capped, not solved',COL.ref,SM_FONT,'center');
  if(S.rows.length) pressPanel(ctx,W,H,S.rows[0],M,st);
  drawCaption(ctx,L);
}

/* -------------------------------------------- view D: the mystery ------- */
const MY_CAP_FULL='PhET&rsquo;s mystery pool. Either the fluid or the planet is hidden, and one gauge reading is all you '
  +'are given — but everything else in p = p_atm + ρgh is known, so the unknown comes out by division. The panel on the '
  +'right draws what each of PhET&rsquo;s three candidates would read at every depth: three straight lines through the '
  +'same intercept when the fluid is the unknown, three lines through different intercepts when the planet is, because '
  +'PhET scales the air pressure by g/g_earth as well. At zero depth the three fluids are genuinely indistinguishable, '
  +'and this file says so rather than pretending otherwise.';
const MY_CAP_SHORT='PhET&rsquo;s mystery pool: one reading, three candidates, and the depth at which they separate.';

function mysteryPanel(ctx,W,H,b,M,st){
  const u=UNITS[st.units];
  /* The three candidates differ by a few kPa on top of an atmosphere, so an
     axis from zero draws them on top of each other and the view cannot show
     the one thing it exists to show (Known-bad: a default that hides the
     effect is a defect).  Fit the axis to the fan and SAY that it is not
     zero-based, which is the house rule for any scale distortion. */
  let lo=Infinity, hi=-Infinity;
  for(const c of M.cands) for(const d of [0,M.level]){
    const v=toUnit(pressureAt(d,c.rho,c.g,M.ySurf,st.atmosphere),st.units);
    lo=Math.min(lo,v); hi=Math.max(hi,v);
  }
  const pad=Math.max((hi-lo)*0.12,Math.abs(hi)*1e-3+1e-9);
  lo-=pad; hi+=pad;
  axesReg(ctx,b,lo,hi,M.level,0,{nx:4,ny:4,xlab:'pressure, '+u.name,ylab:'depth, m',
    xfmt:t=>fmt(t,u.dp===1?1:(u.dp===3?3:2)),
    title:titleFor(b,'what each candidate would read',(st.myMode==='fluid'?'three fluids':'three planets'))});
  const cols=[COL.pos,COL.struct,COL.ref];
  M.cands.forEach((c,i)=>{
    const xs=[],ys=[];
    for(let k=0;k<=40;k++){ const d=M.level*k/40;
      xs.push(toUnit(pressureAt(d,c.rho,c.g,M.ySurf,st.atmosphere),st.units)); ys.push(d); }
    polyline(ctx,b,xs,ys,lo,hi,M.level,0,cols[i],i===st.myWhich&&st.myReveal?2.4:1.6,
             i===st.myWhich&&st.myReveal?null:[6,3]);
  });
  marker(ctx,b,lo,hi,M.level,0,toUnit(M.p,st.units),M.d,COL.live);
  {
    const MX=b.x+b.w*(toUnit(M.p,st.units)-lo)/(hi-lo), flip=(MX>b.x+b.w*0.62);
    lab(ctx,W,H,MX+(flip?-9:9),b.y1-b.h*(M.level-M.d)/(M.level||1),'the gauge',COL.live,SM_FONT,flip?'right':'left');
  }
  legendReg(ctx,b,M.cands.map((c,i)=>[cols[i],(st.myMode==='fluid'?'Fluid ':'Planet ')+c.label]));
  /* both notes go down AFTER the legend, so they dodge its registered box */
  lab(ctx,W,H,b.x+4,b.y1-8,M.unique?('separated by '+pStr(M.sep,st,4)):'not separated at this depth',
      M.unique?COL.pos:COL.ref,SM_FONT,'left');
  lab(ctx,W,H,b.x1-4,b.y1-8,'the axis starts at '+fmt(lo,u.dp)+' '+u.name+', not at zero',COL.ref,SM_FONT,'right');
}

function drawMysteryView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,MY_CAP_FULL,MY_CAP_SHORT,0,0);
  const S=splitMain(L,W,0.52,1);
  const map=drawPool(ctx,W,H,S.pool,'square',M.ySurf,st.myReveal?M.rho:1050,st,null);
  drawPlumbing(ctx,W,H,map,'square',st);
  const gx=(SQ_X0+SQ_X1)/2, gy=M.ySurf-M.d;
  const G={p:M.p,wet:M.d<=M.level,out:false,depth:M.d,surf:M.ySurf};
  seg(ctx,map,[SQ_X0,gy],[SQ_X1,gy],rgba(COL.live,0.30),1,[4,4]);
  drawGauge(ctx,W,H,map,gx,gy,G,'gauge',COL.live,st);
  lab(ctx,W,H,map.X((SQ_X0+SQ_X1)/2),map.Y(M.ySurf)-13,
      st.myReveal?(st.myMode==='fluid'?'Fluid '+'ABC'[st.myWhich]+' · '+sigf(M.rho,4)+' kg/m³'
                                      :'Planet '+'ABC'[st.myWhich]+' · g = '+sigf(M.g,3)+' m/s²')
                 :(st.myMode==='fluid'?'an unknown fluid':'an unknown planet'),
      st.myReveal?COL.live:COL.dim,SM_FONT,'center');
  lab(ctx,W,H,map.X(SQ_X0)-6,map.Y(gy),fmt(M.d,2)+' m down',COL.live,SM_FONT,'right');
  lab(ctx,W,H,map.X(SQ_X0),map.Y(-POOL_H)+15,
      st.myMode==='fluid'?('g is given: '+fmt(st.grav,2)+' m/s²'):('the fluid is given: '+sigf(st.rho,4)+' kg/m³'),
      COL.ref,SM_FONT,'left');
  if(M.degenerate) lab(ctx,W,H,map.X((SQ_X0+SQ_X1)/2),map.Y(0.40),
    'at zero depth every fluid reads the same — lower the gauge',COL.ref,SM_FONT,'center');
  if(S.rows.length) mysteryPanel(ctx,W,H,S.rows[0],M,st);
  drawCaption(ctx,L);
}

/* -------------------------------------------- view E: the paradox ------- */
const PAR_CAP_FULL='Four vessels with the same base, filled to the same depth with the same fluid. They hold 3.1 to 8.4 '
  +'cubic metres — the heaviest is '+fmt(8.4/3.1,2)+' times the lightest — and the force on every one of those bases is '
  +'identical, because the force is p times the area and p is ρgh. That is the hydrostatic paradox. The difference goes '
  +'into the slanted walls: where a vessel widens with height the walls hold part of the fluid up, where it narrows they '
  +'push down, and in both cases by exactly W − F_base. This view computes that wall force by integrating ∫p w′(y) D dy '
  +'over the walls WITHOUT using the force balance, so the agreement below is a check and not a definition.';
const PAR_CAP_SHORT='Four vessels, one base, one depth, weights 2.7 apart — and one base force. The slanted walls carry '
  +'the difference.';

function vesselLayout(){
  const gap=0.62; let x=gap/2; const out=[];
  for(const v of VESSELS){
    let wmax=0;
    for(const pt of v.prof) wmax=Math.max(wmax,pt[1]);
    out.push({v:v,cx:x+wmax/2,wmax:wmax});
    x+=wmax+gap;
  }
  return {items:out,total:x+gap/2};
}
function vesselPoly(prof,H){
  const pts=[];
  for(let i=0;i<prof.length;i++) pts.push([-profW(prof,prof[i][0])/2,prof[i][0]]);
  for(let i=prof.length-1;i>=0;i--) pts.push([profW(prof,prof[i][0])/2,prof[i][0]]);
  return pts;
}
function fluidPoly(prof,H,hFill){
  const pts=[]; const ys=[0];
  for(const pt of prof) if(pt[0]>0&&pt[0]<hFill) ys.push(pt[0]);
  ys.push(hFill);
  for(const y of ys) pts.push([-profW(prof,y)/2,y]);
  for(let i=ys.length-1;i>=0;i--) pts.push([profW(prof,ys[i])/2,ys[i]]);
  return pts;
}
function drawParadoxView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,PAR_CAP_FULL,PAR_CAP_SHORT,1,0.36);
  const VL=vesselLayout();
  const E={xmin:0,xmax:VL.total,ymin:-0.45,ymax:PAR_H+0.55};
  const map=worldFitUp(L.main,E,0.02);
  seg(ctx,map,[E.xmin,0],[E.xmax,0],rgba('#5b6480',0.8),1.4);
  const col=fluidColour(M.rho);
  const Fref=Math.max.apply(null,M.rows.map(r=>Math.max(r.W,r.Fbase)));
  const alen=0.85;
  VL.items.forEach((it,i)=>{
    const r=M.rows[i], on=(it.v.id===st.parPick);
    const P=vesselPoly(it.v.prof,PAR_H).map(q=>[q[0]+it.cx,q[1]]);
    const F=fluidPoly(it.v.prof,PAR_H,M.H).map(q=>[q[0]+it.cx,q[1]]);
    worldPoly(ctx,map,F,rgba(col,0.30),null);
    worldPoly(ctx,map,P,null,on?COL.live:rgba(COL.struct,0.6),on?2:1.3);
    /* the base, drawn thick: it is the same in every vessel */
    seg(ctx,map,[it.cx-profW(it.v.prof,0)/2,0],[it.cx+profW(it.v.prof,0)/2,0],COL.pos,3.2);
    /* the surface */
    seg(ctx,map,[it.cx-profW(it.v.prof,M.H)/2,M.H],[it.cx+profW(it.v.prof,M.H)/2,M.H],rgba(col,0.95),1.8);
    /* the two arrows get their own columns: drawn on the same vertical they
       cross each other in the flared and stepped vessels and the picture
       reads as one muddle */
    /* the offset has to fit the NARROWEST of the two heights the arrows are
       anchored at, or the tapered vessel's weight arrow hangs outside its own
       wall */
    const off=Math.min(0.30,0.26*Math.min(profW(it.v.prof,0),profW(it.v.prof,PAR_H*0.98)));
    arrowW(ctx,map,[it.cx-off,0.03],[0,alen*r.Fbase/Fref],COL.pos,2.2);
    /* the weight arrow hangs from the TOP OF THE VESSEL, not from the fluid
       surface: anchored at the surface it runs out through the base whenever
       the fluid is shallower than the arrow is long */
    arrowW(ctx,map,[it.cx+off,PAR_H*0.98],[0,-alen*r.W/Fref],COL.ref,2.2);
    labFixed(ctx,map.X(it.cx),map.Y(PAR_H+0.34),it.v.name,on?COL.live:'#aeb6c6',
             on?'bold 12px -apple-system, sans-serif':'12px -apple-system, sans-serif','center','middle');
    /* the two label rows are 0.20 m apart, which is under a line height once
       the stage drops below about 700 px: drop the subtitle rather than
       stack it on the name */
    if(map.s*0.20>=15)
      labFixed(ctx,map.X(it.cx),map.Y(PAR_H+0.14),fmt(1000*r.V,0)+' L · F/W '+fmt(r.ratio,2),
               COL.dim,SM_FONT,'center','middle');
    else lab(ctx,W,H,map.X(it.cx),map.Y(PAR_H+0.10),fmt(1000*r.V,0)+' L',COL.dim,SM_FONT,'center');
    lab(ctx,W,H,map.X(it.cx),map.Y(-0.22),fmt(r.Fbase/1000,1)+' kN',COL.pos,SM_FONT,'center');
  });
  seg(ctx,map,[E.xmin,M.H],[E.xmax,M.H],rgba(col,0.28),1,[5,4]);
  /* at the left end this label runs straight into the first vessel; the right
     end of the waterline is clear at every depth */
  lab(ctx,W,H,map.X(E.xmax)-3,map.Y(M.H)+12,'the same depth, '+fmt(M.H,2)+' m',col,SM_FONT,'right');
  lab(ctx,W,H,map.X(E.xmax)-3,map.Y(PAR_H+0.50),'green up = force on the base · orange down = weight of fluid',
      COL.dim,SM_FONT,'right');
  /* the bar panel */
  if(L.bottom.length){
    const b=L.bottom[0];
    const hi=Math.max.apply(null,M.rows.map(r=>Math.max(r.W,r.Fbase)))*1.14/1000;
    axesReg(ctx,b,0,4,0,hi,{nx:4,ny:4,ylab:'kN',xticks:[],
      title:titleFor(b,'weight of fluid (orange) against force on the base (green), kN','weight vs base force')});
    M.rows.forEach((r,i)=>{
      const x0=b.x+b.w*(i+0.16)/4, bw=b.w*0.30/4;
      const yW=b.y1-b.h*(r.W/1000)/hi, yF=b.y1-b.h*(r.Fbase/1000)/hi;
      ctx.fillStyle=rgba(COL.ref,0.55); ctx.fillRect(x0,yW,bw,b.y1-yW);
      ctx.fillStyle=rgba(COL.pos,0.65); ctx.fillRect(x0+bw+3,yF,bw,b.y1-yF);
      labFixed(ctx,x0+bw+1.5,b.y1+11,r.name,r.id===st.parPick?COL.live:COL.dim,SM_FONT,'center','top');
      labFixed(ctx,x0+bw/2,yW-8,fmt(r.W/1000,1),COL.ref,SM_FONT,'center','middle');
      labFixed(ctx,x0+bw*1.5+3,yF-8,fmt(r.Fbase/1000,1),COL.pos,SM_FONT,'center','middle');
    });
    lab(ctx,W,H,b.x1-4,b.y+12,'the green bars are identical; the orange ones differ by '+fmt(M.spread,2)+'×',
        COL.pos,SM_FONT,'right');
  }
  drawCaption(ctx,L);
}

/* --------------------------------------------- view F: the column ------- */
const COL_CAP_FULL='The whole simulation is one straight line. Pressure against depth has intercept p_atm and slope ρg, '
  +'and every control in this file moves exactly one of those two: the fluid slider tilts the line, the gravity slider '
  +'tilts it too and lifts the intercept with it, and the atmosphere switch drops the intercept to zero. Changing the '
  +'units does not move the line at all — it relabels the axis, which is why the three scales are drawn underneath on '
  +'one picture. The conversions are the exact definitions: 1 atm = 101325 Pa, 1 psi = (0.45359237 kg × 9.80665) / '
  +'(0.0254 m)² = 6894.757293 Pa, so 1 atm = 14.69594878 psi.';
const COL_CAP_SHORT='Pressure against depth is a straight line: intercept p_atm, slope ρg — and three names for every '
  +'number on it.';

function drawColumnView(ctx,W,H,M,st){
  const L=layout(ctx,W,H,COL_CAP_FULL,COL_CAP_SHORT,1,0.30);
  const u=UNITS[st.units], b=L.main;
  let hi=0;
  for(const ln of M.lines) hi=Math.max(hi,toUnit(pressureAt(POOL_H,ln.rho,M.g,0,st.atmosphere),st.units));
  hi=Math.max(hi,toUnit(pressureAt(POOL_H,st.rho,M.g,0,st.atmosphere),st.units))*1.08;
  /* the title names the three fluids only when the three fluids are drawn: a
     title for a curve that is not there is a false statement about the
     picture (Known-bad, the isenthalp legend) */
  axesReg(ctx,b,0,POOL_H,0,hi,{nx:5,ny:5,xlab:'depth below the surface, m',ylab:'pressure, '+u.name,
    title:titleFor(b,'p = p_atm + ρgh, on '+gName(M.g)+(st.colAll?', for PhET’s three named fluids':', for the fluid on the slider'),
                   'p against depth')});
  polyline(ctx,b,[0,POOL_H],[toUnit(M.p0,st.units),toUnit(M.p0,st.units)],0,POOL_H,0,hi,rgba(COL.ref,0.8),1.4,[5,4]);
  lab(ctx,W,H,b.x1-4,b.y1-b.h*toUnit(M.p0,st.units)/hi-11,'p_atm = '+pStr(M.p0,st),COL.ref,SM_FONT,'right');
  const cols=[COL.struct,COL.pos,COL.gold];
  if(st.colAll) M.lines.forEach((ln,i)=>{
    const xs=[],ys=[];
    for(let k=0;k<=40;k++){ const d=POOL_H*k/40; xs.push(d);
      ys.push(toUnit(pressureAt(d,ln.rho,M.g,0,st.atmosphere),st.units)); }
    polyline(ctx,b,xs,ys,0,POOL_H,0,hi,cols[i],1.5,[6,3]);
  });
  {
    const xs=[],ys=[];
    for(let k=0;k<=60;k++){ const d=POOL_H*k/60; xs.push(d);
      ys.push(toUnit(pressureAt(d,st.rho,M.g,0,st.atmosphere),st.units)); }
    polyline(ctx,b,xs,ys,0,POOL_H,0,hi,COL.live,2.2);
  }
  marker(ctx,b,0,POOL_H,0,hi,M.d,toUnit(M.here.p,st.units),COL.live);
  /* the readout panel floats over the top right of the stage, so a callout
     placed to the RIGHT of a marker in the last third of the plot lands
     underneath it (Known-bad: audit.py's under-readout report) -- flip it */
  {
    /* above the marker, not beside it: beside it the label lay along the very
       curve it is labelling and along the water line beneath it */
    const MX=b.x+b.w*M.d/POOL_H, MY=b.y1-b.h*toUnit(M.here.p,st.units)/hi;
    const flip=(MX>b.x+b.w*0.62);
    lab(ctx,W,H,MX+(flip?-6:6),MY-14,fmt(M.d,2)+' m → '+pStr(M.here.p,st),COL.live,SM_FONT,flip?'right':'left');
  }
  legendReg(ctx,b,(st.colAll?M.lines.map((ln,i)=>[cols[i],ln.name+' '+sigf(ln.rho,4)]):[])
                   .concat([[COL.live,'the slider: '+sigf(st.rho,4)+' kg/m³']]));
  /* the three scales, one pressure */
  if(L.bottom.length){
    const bb=L.bottom[0];
    const pmax=fromUnit(hi,st.units);
    /* three rules need about 30 px each: a tick label sits 12 px under its own
       rule and the next rule's NAME sits on the following line, so on a short
       stage they interleave (found by tools/audit.py on the 820 x 520 capture,
       which the 1400 px one cannot see).  Where there is no room, draw the
       scale the reader has actually chosen and say so. */
    const allNames=['metric','atmosphere','english'];
    const roomy=(bb.h/allNames.length)>=30;
    const names=roomy?allNames:[st.units];
    const rows=names.length, gapY=bb.h/rows;
    lab(ctx,W,H,bb.x,bb.y-12,
        roomy?titleFor(bb,'the same pressure on all three scales — the axis is relabelled, not moved','three scales, one pressure')
             :'one scale — the stage is too short for all three',
        '#aeb6c6','13px Georgia, serif','left');
    /* the scale NAMES get a gutter of their own: at 820 px "psi" sat on the
       first tick label of its own rule (found by tools/audit.py on the narrow
       capture, which the 1400 px one cannot see) */
    const gx=bb.x+54, gw=Math.max(60,bb.x1-gx);
    names.forEach((n,i)=>{
      const uu=UNITS[n], Y=bb.y+gapY*(i+0.45);
      ctx.beginPath(); ctx.moveTo(gx,Y); ctx.lineTo(gx+gw,Y);
      ctx.strokeStyle=rgba(COL.struct,0.55); ctx.lineWidth=1.2; ctx.stroke();
      POLY_SEGS.push(gx,Y,gx+gw,Y);
      const tk=ticksFor(0,pmax/uu.per,6);
      for(const t of tk){
        const X=gx+gw*(t*uu.per)/pmax;
        if(X<gx-0.5||X>gx+gw+0.5) continue;
        ctx.beginPath(); ctx.moveTo(X,Y-4); ctx.lineTo(X,Y+4);
        ctx.strokeStyle=rgba(COL.struct,0.7); ctx.lineWidth=1; ctx.stroke();
        labFixed(ctx,X,Y+12,fmt(t,uu.dp===3?2:(uu.dp===1?0:1)),'#6f7789',SM_FONT,'center','middle');
      }
      labFixed(ctx,gx-16,Y,uu.name,n===st.units?COL.pos:COL.dim,
               n===st.units?'bold 11px -apple-system, sans-serif':LAB_FONT,'right','middle');
      const XM=gx+gw*M.here.p/pmax;
      if(XM>=gx&&XM<=gx+gw){
        dot(ctx,XM,Y,4,COL.live,'#fff',1.2);
        if(i===0) lab(ctx,W,H,XM+(XM>gx+gw*0.62?-8:8),Y-12,fmt(toUnit(M.here.p,n),uu.dp)+' '+uu.name,
                      COL.live,SM_FONT,XM>gx+gw*0.62?'right':'left');
      }
    });
  }
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  dispatch, and the scene object                                     *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(st.view==='pool') drawPoolView(ctx,W,H,M,st);
  else if(st.view==='shapes') drawShapesView(ctx,W,H,M,st);
  else if(st.view==='press') drawPressView(ctx,W,H,M,st);
  else if(st.view==='mystery') drawMysteryView(ctx,W,H,M,st);
  else if(st.view==='paradox') drawParadoxView(ctx,W,H,M,st);
  else drawColumnView(ctx,W,H,M,st);
}

/* which scene each view draws its pool in (the pointer needs the same map) */
function sceneOf(view){
  if(view==='shapes') return 'trapezoid';
  if(view==='press') return 'chamber';
  if(view==='pool'||view==='mystery') return 'square';
  return null;
}
/* the map a scene view is drawn with, rebuilt for the pointer.  It must use
   the SAME layout call as the view, or a drag lands somewhere else. */
function stageMap(ctx,W,H,st){
  const sc=sceneOf(st.view);
  if(!sc||st.view==='mystery') return null;
  const caps={pool:[POOL_CAP_FULL,POOL_CAP_SHORT,0.56],
              shapes:[SHAPE_CAP_FULL,SHAPE_CAP_SHORT,0.58],
              press:[PRESS_CAP_FULL,PRESS_CAP_SHORT,0.56]}[st.view];
  const L=stageLayout(ctx,W,H-HINT_H,caps[0],caps[1],0,0);
  const S=splitMain({main:L.main},W,caps[2],1);
  return worldFitUp(S.pool,extentFor(sc),0.05);
}
const GRAB={what:null,dx:0,dy:0};

function makeScene(canvas){
  const S={st:ST,W:1180,H:740};
  S.model=()=>buildModel(ST);
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel(ST),ST); };
  /* nothing animates: this file solves the static problem exactly */
  S.step=function(){ return false; };
  /* the pointer: drag either gauge anywhere on a scene stage */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=GRAB.what!==null; GRAB.what=null; return had; }
    const ctx=canvas.getContext('2d'), map=stageMap(ctx,S.W,S.H,ST);
    if(!map) return false;
    if(type==='down'){
      const cands=[['B',ST.gBx,ST.gBy],['A',ST.gAx,ST.gAy]];
      for(const [tag,gx,gy] of cands){
        const dx=x-map.X(gx), dy=y-map.Y(gy);
        if(dx*dx+dy*dy<=26*26){ GRAB.what=tag; GRAB.dx=gx-map.wx(x); GRAB.dy=gy-map.wy(y); return true; }
      }
      return false;
    }
    if(type==='move'&&GRAB.what){
      const E=extentFor(sceneOf(ST.view));
      const wx=clamp(map.wx(x)+GRAB.dx,E.xmin,E.xmax), wy=clamp(map.wy(y)+GRAB.dy,E.ymin,E.ymax);
      if(GRAB.what==='A'){ ST.gAx=wx; ST.gAy=wy; } else { ST.gBx=wx; ST.gBy=wy; }
      clearAll();
      return true;
    }
    return false;
  };
  return S;
}
