
/* ================================================================== *
 *  the two analysis views, the dispatch and the scene                 *
 * ================================================================== */

/* the room an analysis panel keeps below its frame: the axis title (at +21, 12 px tall)
   plus a one- or two-line caption */
const BOTTOM_RESERVE=76;

/* ---- view D: the ladder ------------------------------------------------- */
const CAP_LADDER='The law every screen of this sim obeys. Left: stack N sheets over the ground and the outgoing flux the surface must supply is multiplied by 1 + &Sigma; a/(2&minus;a) &mdash; for perfectly absorbing sheets that is exactly N + 1, so the temperature goes as the fourth root of it. Right: the same law against the absorbance of the sheets, for one, two, three and PhET&rsquo;s twelve. The markers are the stack you have loaded on the other views; the orange line is the real Earth, which is worth about two thirds of one perfect sheet.';
const CAP_LADDER_S='T_s = T_eff[1 + N a/(2 &minus; a)]^(1/4), and (N+1)^(1/4) when a = 1.';
function ladderGeo(ctx,W,H,M){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,CAP_LADDER,CAP_LADDER_S,capW,top+190);
  /* BOTTOM_RESERVE is the axis title (21 + 12 px below the frame) plus the per-panel
     caption; without it the x-axis label sat inside the main caption at every size */
  const availH=Math.max(110,fit.capY-16-top-BOTTOM_RESERVE);
  if(narrow){
    return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,
            A:box(left,top,right-left,availH),B:null};
  }
  const gut=76, w=(right-left-gut)/2;
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,
          A:box(left,top,w,availH),B:box(left+w+gut,top,w,availH)};
}
function viewLadder(ctx,W,H,M){
  const L=M.L, G=ladderGeo(ctx,W,H,M), u=M.unit;
  const TA=L.black.map(r=>r.T), lo=tempIn(TA[0]*0.97,u), hi=tempIn(TA[12]*1.03,u);
  /* panel A: temperature against the number of sheets */
  const A=G.A;
  axesR(ctx,A,0,12,lo,hi,{nx:7,ny:6,xlab:'number of absorbing sheets, N',
    ylab:'surface temperature, '+UNIT_SYM[u],
    title:titleFor(A,'the ladder: T_s = T_eff (N+1)^(1/4)','the ladder'),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  /* the closed form as a continuous curve, and the solve as points on it */
  for(const [aval,col,dash] of [[1,COL.ref,null],[0.5,COL.struct,[6,4]],[0.25,COL.live,[3,3]]]){
    const xs=[], ys=[];
    for(let k=0;k<=240;k++){ const n=12*k/240;
      xs.push(n); ys.push(tempIn(L.T0*Math.pow(1+n*aval/(2-aval),0.25),u)); }
    polyline(ctx,A,xs,ys,0,12,lo,hi,col,aval===1?2:1.5,dash);
  }
  for(const r of L.black){
    const X=A.x+A.w*r.n/12, Y=A.y1-A.h*(tempIn(r.T,u)-lo)/(hi-lo);
    dot(ctx,X,Y,3.6,COL.pos,'#0a0c12',1);
  }
  /* the real Earth.  The LABEL waits until after the legend is placed, and the legend's
     own rectangle is registered, so lab() can dodge it — LEGEND_RECTS is a separate
     registry that the label placer does not read. */
  const yE=A.y1-A.h*(tempIn(L.earth.Ts,u)-lo)/(hi-lo);
  if(yE>A.y&&yE<A.y1){
    ctx.beginPath(); ctx.moveTo(A.x,yE); ctx.lineTo(A.x1,yE);
    ctx.strokeStyle=rgba('#e8843a',0.5); ctx.lineWidth=1.2; ctx.setLineDash([2,4]);
    ctx.stroke(); ctx.setLineDash([]); }
  { const lb=legendAuto(ctx,A,[[COL.pos,'the solve'],[COL.ref,'a = 1, closed form'],
                    [COL.struct,'a = 0.5'],[COL.live,'a = 0.25']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]); }
  if(yE>A.y&&yE<A.y1) lab(ctx,W,H,A.x+6,yE-9,'the real Earth, 288 K','#e8843a',SM_FONT,'left');
  capUnder(ctx,A.x,A.y1+40,'Points: the flux system solved. Curves: T_eff[1 + Na/(2&minus;a)]^(1/4). They agree to 1 part in 10&#185;&#179;.',
           A.w,G.capY-6);
  /* panel B: temperature against absorbance */
  const B=G.B;
  if(B){
    const tops=L.curves.map(c=>c.pts[c.pts.length-1][1]);
    const hiB=tempIn(Math.max.apply(null,tops)*1.02,u), loB=tempIn(L.T0*0.98,u);
    axesR(ctx,B,0,1,loB,hiB,{nx:6,ny:6,xlab:'absorbance a of each sheet',
      ylab:'surface temperature, '+UNIT_SYM[u],
      title:titleFor(B,'and what a sheet&rsquo;s absorbance is worth','absorbance'),
      xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,0)});
    const cols=[COL.pos,COL.struct,COL.live,COL.ref];
    L.curves.forEach((c,i)=>{
      polyline(ctx,B,c.pts.map(p=>p[0]),c.pts.map(p=>tempIn(p[1],u)),0,1,loB,hiB,cols[i],1.8);
      const last=c.pts[c.pts.length-1];
      lab(ctx,W,H,B.x1-8,B.y1-B.h*(tempIn(last[1],u)-loB)/(hiB-loB),'N = '+c.n,cols[i],SM_FONT,'right');
    });
    /* the marker: the stack loaded on the layer-model view */
    if(L.n>0){
      /* read the marker off the model's own solve, never a second one built here: a
         re-derived stack drifts from the one the model prints (drum_head Known-bad) */
      const Ts=tempIn(L.hereCurveT,u);
      marker(ctx,B,0,1,loB,hiB,L.a,Ts,COL.live);
      /* the label goes on whichever side of the marker has room: at a = 1 the marker is
         on the panel's right edge and a left-aligned label runs off it */
      const mX=B.x+B.w*L.a, mY=B.y1-B.h*(Ts-loB)/(hiB-loB);
      const rightSide=L.a<0.6;
      lab(ctx,W,H,mX+(rightSide?9:-9),mY-12,'you: N = '+L.n+', a = '+fmt(L.a,2),
          COL.live,SM_FONT,rightSide?'left':'right');
    }
    /* the Earth's equivalent sheet */
    { const aE=L.earthEqA;
      if(aE>0&&aE<=1){
        const X=B.x+B.w*aE;
        ctx.beginPath(); ctx.moveTo(X,B.y); ctx.lineTo(X,B.y1);
        ctx.strokeStyle=rgba('#e8843a',0.45); ctx.lineWidth=1.2; ctx.setLineDash([3,4]);
        ctx.stroke(); ctx.setLineDash([]);
        lab(ctx,W,H,X-6,B.y1-14,'Earth &asymp; one sheet at a = '+fmt(aE,3),'#e8843a',SM_FONT,'right'); } }
    capUnder(ctx,B.x,B.y1+40,'a = 0 is a bare rock; a = 1 is a perfect sheet. The rise is steep near a = 1 because a sheet that lets even a tenth through loses a tenth of its grip.',
             B.w,G.capY-6);
  }
  caption(ctx,G.left,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
}

/* ---- view E: the record ------------------------------------------------- */
const CAP_RECORD='Where PhET&rsquo;s numbers come from, and what they are worth. The curve is this file&rsquo;s exact solve of PhET&rsquo;s own fit, a_i = 0.85&thinsp;c&thinsp;e^(&minus;z/8400 m) on twelve sheets; the four rings are PhET&rsquo;s dates, and the ice age sits BELOW the curve because PhET whitens its ground as well (albedo 0.225 against 0.2). The fit is a teaching device &mdash; no line strengths, no bands, no water vapour &mdash; and it shows: the absolute level sits about 8.5 K above the real Earth. What PhET did tune is the DIFFERENCES, and those are good: its ice age is 6.3 K below 1750 and its 2020 is 1.3 K above, against about 6 K and 1.2 K observed.';
const CAP_RECORD_S='PhET&rsquo;s concentration fit, solved exactly: the differences are right, the level is 8.5 K high.';
function recordGeo(ctx,W,H,M){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,CAP_RECORD,CAP_RECORD_S,capW,top+190);
  const availH=Math.max(110,fit.capY-16-top);
  const tableH=narrow?0:Math.min(148,availH*0.30);
  const A=box(left,top,right-left,Math.max(120,availH-(tableH?tableH+64:BOTTOM_RESERVE)));
  const T=tableH?box(left,A.y1+64,right-left,tableH):null;
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,A,T};
}
function viewRecord(ctx,W,H,M){
  const R=M.R, G=recordGeo(ctx,W,H,M), u=M.unit, A=G.A;
  const lo=tempIn(R.curve[0][1]*0.985,u), hi=tempIn(R.hottest*1.01,u);
  axesR(ctx,A,0,1,lo,hi,{nx:6,ny:6,xlab:'PhET&rsquo;s greenhouse-gas concentration c',
    ylab:'surface temperature, '+UNIT_SYM[u],
    title:titleFor(A,'PhET&rsquo;s fit, solved exactly','the fit, solved'),
    xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,0)});
  polyline(ctx,A,R.curveCloud.map(p=>p[0]),R.curveCloud.map(p=>tempIn(p[1],u)),0,1,lo,hi,
           COL.struct,1.4,[6,4]);
  polyline(ctx,A,R.curve.map(p=>p[0]),R.curve.map(p=>tempIn(p[1],u)),0,1,lo,hi,COL.pos,2.2);
  /* the real Earth: the line now, its label after the legend has taken its corner */
  const yE=A.y1-A.h*(tempIn(R.earthTs,u)-lo)/(hi-lo);
  if(yE>A.y&&yE<A.y1){
    ctx.beginPath(); ctx.moveTo(A.x,yE); ctx.lineTo(A.x1,yE);
    ctx.strokeStyle=rgba('#e8843a',0.6); ctx.lineWidth=1.4; ctx.setLineDash([3,4]);
    ctx.stroke(); ctx.setLineDash([]); }
  /* PhET's four dates */
  R.rows.forEach((r,k)=>{
    const X=A.x+A.w*r.d.c, Y=A.y1-A.h*(tempIn(r.Ts,u)-lo)/(hi-lo);
    /* the ice age is BELOW the curve because PhET whitens its ground too; draw the gap as
       a connector in the dates' own colour rather than giving it a second colour the
       legend would then share with the cloud curve */
    if(r.d.glacier){
      const Yc=A.y1-A.h*(tempIn(R.iceOnCurve,u)-lo)/(hi-lo);
      ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(X,Yc);
      ctx.strokeStyle=rgba(COL.live,0.55); ctx.lineWidth=1.2; ctx.setLineDash([3,3]);
      ctx.stroke(); ctx.setLineDash([]);
      lab(ctx,W,H,X+8,(Y+Yc)/2,'glaciated ground',rgba(COL.live,0.85),SM_FONT,'left');
    }
    dot(ctx,X,Y,5.2,'rgba(0,0,0,0)',COL.live,2);
    /* 1750 and 1950 are 0.0035 apart in c: alternate the labels or they sit on top of
       each other whatever the registry does about it */
    lab(ctx,W,H,X,Y+(k%2?17:-15),r.d.name,COL.live,SM_FONT,'center');
  });
  /* where the controls are set now */
  { const c=R.here, Ts=solveClosed(concAbsorbance(c,GH.N_CONC),
        (1-concAlbedo())*GH.S_SUN*(ST.cloud?1-CLOUD_REFL:1)).Tg;
    marker(ctx,A,0,1,lo,hi,c,tempIn(Ts,u),COL.pos); }
  { const lb=legendAuto(ctx,A,[[COL.pos,'no cloud'],[COL.struct,'with PhET&rsquo;s cloud'],
                    [COL.live,'PhET&rsquo;s dates'],['#e8843a','the real Earth']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]); }
  if(yE>A.y&&yE<A.y1)
    lab(ctx,W,H,A.x+6,yE-9,'the real Earth, '+plain(tstr(R.earthTs,u,1)),'#e8843a',SM_FONT,'left');
  /* the table of dates */
  if(G.T){
    const T=G.T, cols=['date','c','CO₂ ppm','CH₄ ppb','N₂O ppb','a₁','T surface','vs 1750'];
    const colX=[], n=cols.length;
    for(let i=0;i<n;i++) colX.push(T.x+8+T.w*(i+0.5)/n);
    ctx.font='italic 12px Georgia, serif'; ctx.fillStyle='#aeb6c6';
    ctx.textAlign='left'; ctx.textBaseline='bottom';
    ctx.fillText(plain('PhET’s four dates — the left five columns are PhET’s, the right three are this file’s solve of them'),T.x,T.y-8);
    ctx.font=SM_FONT; ctx.textBaseline='top';
    const rowH=Math.min(24,(T.h-22)/4);
    for(let i=0;i<n;i++){
      ctx.textAlign=i?'right':'left'; ctx.fillStyle='#6f7789';
      ctx.fillText(plain(cols[i]),colX[i],T.y+2);
    }
    ctx.beginPath(); ctx.moveTo(T.x,T.y+20); ctx.lineTo(T.x1,T.y+20);
    ctx.strokeStyle='#242a3a'; ctx.lineWidth=1; ctx.stroke();
    R.rows.forEach((r,k)=>{
      const y=T.y+24+k*rowH;
      const vals=[r.d.name,fmt(r.d.c,4),''+r.d.co2,''+r.d.ch4,''+r.d.n2o,fmt(r.a[0],4),
                  plain(tstr(r.Ts,u,2)),
                  (k===1?'—':plain(dK(r.Ts-R.rows[1].Ts,u,2)))];
      for(let i=0;i<n;i++){
        ctx.textAlign=i?'right':'left';
        ctx.fillStyle=i<5?(i===0?'#aeb6c6':'#8b93a6'):(i===7?COL.live:COL.pos);
        ctx.fillText(plain(vals[i]),colX[i],y);
      }
    });
  }
  caption(ctx,G.left,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
}

/* ---- dispatch ----------------------------------------------------------- */
function drawView(rc,W,H,M){
  POLY_SEGS=[]; LEGEND_RECTS=[]; LABELS=[];
  /* The floating readout covers the top-right of the stage — about 336 px wide and up to
     548 tall — and it is HTML, so nothing on the canvas can see it.  Register it as an
     occupied label box so lab() dodges it (Known-bad: text placed at the top right of a
     plot box is text placed underneath the readout).  On a narrow stage the layout
     deliberately runs the panels under it, and tools/audit.py reports that as advisory. */
  if(W>=900) LABELS.push([W-336,0,W,Math.min(548,H)]);
  rc.fillStyle='#070b18'; rc.fillRect(0,0,W,H);
  const m=M||buildModel();
  if(m.view==='waves') viewWaves(rc,W,H,m);
  else if(m.view==='photons') viewPhotons(rc,W,H,m);
  else if(m.view==='layers') viewLayers(rc,W,H,m);
  else if(m.view==='ladder') viewLadder(rc,W,H,m);
  else viewRecord(rc,W,H,m);
}

/* ---- the scene ---------------------------------------------------------- */
function makeScene(canvas){
  const S={W:0,H:0,
    model(){ return buildModel(); },
    draw(){
      /* fetch the context INSIDE the draw: a context cached at boot writes into a recorder
         the DOM-stub harness has already thrown away (Known-bad, polyhedra.html) */
      const rc=canvas.getContext('2d');
      drawView(rc,S.W,S.H,S.model());
    },
    step(){ return stepFrame(); },
    pointer(kind,x,y){
      if(!SKY_VIEWS[ST.view]) return false;
      const rc=canvas.getContext('2d');
      const L=skyLayout(rc,S.W,S.H,S.model(),CAP_WAVES,CAP_WAVES_S);
      const win=L.win, mp=skyMapOf(win);
      if(kind==='down'){
        const yP=mp.yOf(PROBE.z);
        if(x>=win.x-10&&x<=win.x1+10&&Math.abs(y-yP)<=14){ DRAG.what='probe'; return true; }
        return false;
      }
      if(kind==='move'&&DRAG.what==='probe'){
        PROBE.z=clamp(mp.zOf(y),0,GH.TOP);
        return true;
      }
      if(kind==='up'&&DRAG.what){ DRAG.what=null; return true; }
      return false;
    }};
  return S;
}
