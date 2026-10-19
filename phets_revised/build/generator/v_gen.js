
/* ================================================================== *
 *  the generator screen, and the two views that open it up:           *
 *  the flux and EMF over one turn, and the coil's face                *
 * ================================================================== */
SCREEN_CAP.gen=['The water wheel turns the bar magnet; the pickup coil’s loops are circles perpendicular to the page, drawn in perspective. The flux through them is the area integral of B over the disc, and the EMF is −N dΦ/dt, so the bulb lights only while the magnet TURNS. Needles every 40 mm along B, brightness PhET’s display mapping. Electron speed shows the current, not a drift speed; the drag of the coil on the wheel is PhET’s phenomenological rule.',
  'The wheel turns the magnet; EMF = −N dΦ/dt lights the bulb. Needles along B; electron speed not to scale.'];
const WHEEL_R=150, WHEEL_PAD=8, FAUCET_X=TURB_X-0.75*WHEEL_R, FAUCET_TOP=LAYOUT_H-18, SPOUT_Y=LAYOUT_H-120;
const IND_GAP=92;                                   /* the indicator rides above the coil, as PhET's does */
function indicatorPos(rc){ return {x:PICK_X, y:PICK_Y+rc+IND_GAP}; }
/* the water column's width follows the flow, as PhET's does (its WaterNode is a rectangle
   whose width is the flow rate) */
function waterW(flow){ return 4+46*flow/100; }
/* rectangles as paths, not fillRect: a path is geometry the tests can measure */
function rectPath(ctx,x,y,w,hh){ ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+w,y); ctx.lineTo(x+w,y+hh); ctx.lineTo(x,y+hh); ctx.closePath(); }
function waterHit(){ return TURB_Y+Math.sqrt(Math.max(0,WHEEL_R*WHEEL_R-Math.pow(TURB_X-FAUCET_X,2))); }
function drawFaucet(ctx,map,flow){
  const X=map.X(FAUCET_X), Ytop=map.Y(FAUCET_TOP), Ys=map.Y(SPOUT_Y), w=Math.max(3,26*map.s);
  rectPath(ctx,X-w/2,Ytop,w,Ys-Ytop); ctx.fillStyle='#3a4256'; ctx.fill();
  ctx.strokeStyle='#5c6478'; ctx.lineWidth=1; ctx.stroke();
  rectPath(ctx,X-w*0.85,Ys-w*0.45,w*1.7,w*0.55); ctx.fillStyle='#4a5468'; ctx.fill();
  if(flow>0){
    const ww=Math.max(2,waterW(flow)*map.s);
    rectPath(ctx,X-ww/2,Ys,ww,map.Y(waterHit())-Ys);
    ctx.fillStyle=rgba(COL.water,0.75); ctx.fill();
  }
}
/* the wheel: a rim, eight spokes from the hub and a paddle on each, turning with the magnet */
function drawWheel(ctx,map,th){
  const X=map.X(TURB_X), Y=map.Y(TURB_Y), R=WHEEL_R*map.s;
  ctx.beginPath(); ctx.arc(X,Y,R,0,TAU); ctx.strokeStyle='#4a5468'; ctx.lineWidth=Math.max(2,5*map.s); ctx.stroke();
  ctx.beginPath(); ctx.arc(X,Y,R*0.86,0,TAU); ctx.strokeStyle='#39415a'; ctx.lineWidth=Math.max(1,2*map.s); ctx.stroke();
  for(let k=0;k<8;k++){
    const a=th+k*TAU/8, c=Math.cos(a), s=Math.sin(a);
    ctx.beginPath();
    ctx.moveTo(X+R*0.12*c,Y-R*0.12*s); ctx.lineTo(X+R*0.86*c,Y-R*0.86*s);
    ctx.strokeStyle='#5c6478'; ctx.lineWidth=Math.max(1.5,4*map.s); ctx.stroke();
    /* the paddle itself, across the spoke at the rim */
    const px=X+R*0.93*c, py=Y-R*0.93*s, t=R*0.17;
    ctx.beginPath(); ctx.moveTo(px-t*s,py-t*c); ctx.lineTo(px+t*s,py+t*c);
    ctx.strokeStyle='#6d768c'; ctx.lineWidth=Math.max(2,6*map.s); ctx.stroke();
  }
  dot(ctx,X,Y,Math.max(2,6*map.s),'#8b93a6');
}
/* PhET writes the wheel's speed in its hub (RPMDisplay, one decimal and the unit).  It goes
   on LAST, because the magnet is bolted across the hub and would otherwise cover it. */
function drawRPM(ctx,map,rpm){
  if(!(rpm>0)) return;
  const X=map.X(TURB_X), Y=map.Y(TURB_Y), r=Math.max(16,27*map.s), fs=Math.max(9,13*map.s);
  dot(ctx,X,Y,r,'rgba(9,12,22,0.9)','#5c6478',1.2);
  ctx.font='600 '+fs.toFixed(1)+'px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillStyle='#e9ecf2'; ctx.fillText(fmt(rpm,1),X,Y-fs*0.42);
  ctx.font=(fs*0.72).toFixed(1)+'px -apple-system, sans-serif'; ctx.fillStyle='#aeb6c6'; ctx.fillText('RPM',X,Y+fs*0.62);
  LABELS.push([X-r,Y-r,X+r,Y+r]);
}
/* where each indicator takes its two wires, in world coordinates */
function indTerminals(st,rc){
  const P=indicatorPos(rc), d=st.indicator==='bulb'?16:30, y=P.y-(st.indicator==='bulb'?50:26);
  return {x:P.x, y, dx:d};
}
/* the pickup coil's leads run up to whichever indicator is chosen (drawn before the coil's
   front turns, so they come out from behind it) */
function drawLeads(ctx,map,rc){
  const T=indTerminals(ST,rc), xs=pickLoopsX(ST.N);
  const lx=PICK_X+xs[0]-8, rx=PICK_X+xs[xs.length-1]+8, top=PICK_Y+rc*0.72;
  ctx.beginPath();
  for(const [x,tx] of [[lx,T.x-T.dx],[rx,T.x+T.dx]]){
    ctx.moveTo(map.X(x),map.Y(top)); ctx.lineTo(map.X(x),map.Y(T.y)); ctx.lineTo(map.X(tx),map.Y(T.y));
  }
  ctx.strokeStyle=COL.copper; ctx.lineWidth=Math.max(1.5,4*map.s); ctx.lineJoin='round'; ctx.stroke();
}
function drawGenScreen(ctx,W,H,M){
  const st=ST, G=screenGeo(ctx,W,H,'gen'), map=G.map, R=M.R, rc=R.rc, xs=pickLoopsX(st.N);
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  screenBack(ctx,W,H,G);
  if(st.genMeter){ const mb=meterBodyBox(map,st.genM.x,st.genM.y); LABELS.push([mb.bx,mb.by,mb.bx+mb.bw,mb.by+mb.bh]); }
  if(st.genField&&M.src.S>0) drawNeedleField(ctx,map,needleGrid(M.src,0,0,LAYOUT_W,LAYOUT_H));
  drawFaucet(ctx,map,st.flow);
  drawWheel(ctx,map,st.th);
  drawBarMagnet(ctx,map,M.src,{seeInside:st.seeInside});
  drawRPM(ctx,map,R.rpm);
  /* the coil: back halves, the leads, the front halves and the electrons on them, and the
     indicator last of all, so nothing is drawn across its face */
  drawCoilHalf(ctx,map,xs,PICK_X,PICK_Y,rc,PICK_WIRE*2,'back');
  drawLeads(ctx,map,rc);
  drawCoilHalf(ctx,map,xs,PICK_X,PICK_Y,rc,PICK_WIRE*2,'front');
  if(st.electrons&&Math.abs(R.norm)>1e-9) drawElectrons(ctx,map,xs,PICK_X,PICK_Y,rc,LIVE.ePhase,4);
  const P=indicatorPos(rc);
  if(st.indicator==='bulb') drawBulb(ctx,map,P.x,P.y,Math.min(1,R.bulb));
  else drawVoltmeter(ctx,map,P.x,P.y,R.needle,R.emf);
  if(st.genCompass) drawCompass(ctx,map,st.genC.x,st.genC.y,M.rot.phi);
  if(st.genMeter) drawFieldMeter(ctx,map,st.genM.x,st.genM.y,M.meter,st.units);
  if(st.flow===0) lab(ctx,W,H,map.X(TURB_X),map.Y(TURB_Y-WHEEL_R-26),'the faucet is closed: nothing turns, so no EMF',COL.dim,SM_FONT,'center','middle');
  else if(M.src.S===0) lab(ctx,W,H,map.X(TURB_X),map.Y(TURB_Y-WHEEL_R-26),'strength 0: no field, so no flux and no EMF',COL.dim,SM_FONT,'center','middle');
  screenCaption(ctx,G);
  return G;
}
/* what the pointer can take hold of here: the two tools.  The magnet is not draggable --
   it is bolted to the wheel, as PhET's is. */
DRAG_CANDS.gen=(st,map,X,Y)=>[{k:'genM',on:st.genMeter,hit:p=>hitMeter(map,p,X,Y),mx:10,my:10},
                              {k:'genC',on:st.genCompass,hit:p=>hitCompass(map,p,X,Y),mx:10,my:10}];

/* ---------------- flux and EMF over one turn ---------------- */
const FLUX_CAP=['Top: the flux through all N loops as the wheel turns one revolution, against the single cosine a₁cos θ that a far-off magnet would give (orange dashed) — the magnet is close, so the flux is flat-topped and its higher harmonics matter. Below: the EMF that follows, −N ω dΦ/dθ. It is zero where the flux is stationary, and its peak stands well before 90°, marked; a pure cosine flux would peak exactly at 90°. Only odd harmonics appear, because half a turn reverses the magnet.',
  'Φ(θ) over one turn against the first harmonic alone (orange), and the EMF −Nω dΦ/dθ below it, whose peak is not at 90°.'];
function fluxGeo(ctx,W,H){ return stageLayoutH(ctx,W,H,FLUX_CAP[0],FLUX_CAP[1],1,0.46,1); }
/* with the faucet closed there is no EMF at any angle; the shape is still worth drawing, so
   the lower panel then shows what full flow WOULD give, and says so */
function shownOmega(F){ return F.rd.omega>0?{om:F.rd.omega,live:true}:{om:2*Math.PI*RPM_MAX*(1-F.rd.drag)/60,live:false}; }
function drawFluxView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const L=fluxGeo(ctx,W,H), b=L.main, b2=L.bottom[0], F=M.fx, S=shownOmega(F);
  const deg=F.th.map(t=>t*R2D);
  /* --- the flux --- */
  /* microwebers: at 1e-6 Wb every tick label rounds to 0.0000 (tickFmt stops at four places) */
  const phi=F.phi.map(v=>v*1e6), one=F.one.map(v=>v*1e6);
  let lo=0, hi=0; for(const v of phi.concat(one)){ lo=Math.min(lo,v); hi=Math.max(hi,v); }
  if(!(hi>lo)){ hi=1e-3; lo=-1e-3; }
  const pd=0.12*(hi-lo);
  /* no x label on the upper panel: it shares the lower one's axis, and the house layout
     leaves the lower panel's title exactly where an upper x label would sit */
  axesQ(ctx,b,0,360,lo-pd,hi+pd,{ylab:'Φ through N loops, μWb',
    title:'the flux through the pickup coil, one turn of the wheel',nx:8,ny:6});
  polyline(ctx,b,deg,one,0,360,lo-pd,hi+pd,COL.ref,1.3,[6,4]);
  polyline(ctx,b,deg,phi,0,360,lo-pd,hi+pd,COL.north,2);
  const Xd=d=>b.x+b.w*d/360, Yv=(v,bb,l2,h2)=>bb.y1-bb.h*(v-l2)/(h2-l2);
  /* where the wheel stands now */
  const thd=wrap2pi(ST.th)*R2D;
  ctx.setLineDash([3,4]); ctx.strokeStyle=rgba(COL.live,0.5); ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(Xd(thd),b.y); ctx.lineTo(Xd(thd),b.y1); ctx.stroke(); ctx.setLineDash([]);
  dot(ctx,Xd(thd),Yv(F.rd.Phi*1e6,b,lo-pd,hi+pd),Math.max(2.5,3.5),COL.live);
  legendAuto(ctx,b,[[COL.north,'Φ(θ), the area integral'],[COL.ref,'a₁cos θ, the first harmonic alone'],[COL.live,'where the wheel stands']]);
  /* --- the EMF --- */
  /* the same law at whichever omega is being shown: EMF = -N omega dPhi/dtheta */
  const mv=F.th.map(t=>emfOf(F.rd.ser,t,F.g.N,F.rd.S,S.om)*1e3);
  const oneMv=F.th.map(t=>F.g.N*F.rd.S*F.a1*S.om*Math.sin(t)*WB_PER_G_MM2*1e3);
  let l2=0, h2=0; for(const v of mv.concat(oneMv)){ l2=Math.min(l2,v); h2=Math.max(h2,v); }
  if(!(h2>l2)){ h2=1e-3; l2=-1e-3; }
  const pd2=0.12*(h2-l2);
  axesQ(ctx,b2,0,360,l2-pd2,h2+pd2,{xlab:'magnet angle θ, degrees',ylab:'EMF, mV',
    title:S.live?'the EMF, −N ω dΦ/dθ, at '+fmt(F.rd.rpm,1)+' RPM':'the EMF at full flow: '+fmt(RPM_MAX*(1-F.rd.drag),1)+' RPM',nx:8,ny:6});
  polyline(ctx,b2,deg,oneMv,0,360,l2-pd2,h2+pd2,COL.ref,1.3,[6,4]);
  polyline(ctx,b2,deg,mv,0,360,l2-pd2,h2+pd2,S.live?COL.north:COL.dim,2,S.live?null:[7,5]);
  /* the peak, and 90 degrees, which is NOT where it is */
  const pkd=F.pk.th*R2D;
  for(const [d,col,txt] of [[pkd,COL.struct,'peak at '+fmt(pkd,1)+'°'],[90,'#5c6478','90°']]){
    ctx.setLineDash([3,4]); ctx.strokeStyle=col; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(Xd(d)-b.x+b2.x,b2.y); ctx.lineTo(Xd(d)-b.x+b2.x,b2.y1); ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,Xd(d)-b.x+b2.x+4,b2.y+11,txt,col,SM_FONT,'left','middle');
  }
  legendAuto(ctx,b2,[[S.live?COL.north:COL.dim,S.live?'EMF = −N ω dΦ/dθ':'EMF at full flow (the wheel is still)'],[COL.ref,'the first harmonic alone']]);
  if(F.rd.S===0){
    lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2-20,'strength 0: no field, so no flux through the coil',COL.dim,LAB_FONT,'center','middle');
    lab(ctx,W,H,b2.x+b2.w/2,b2.y+b2.h/2-14,'and nothing for its change to induce',COL.dim,LAB_FONT,'center','middle');
  }
  drawCaption(ctx,L);
}

/* ---------------- the coil's face ---------------- */
const FACE_CAP=['Top: the two ways of adding the field over the coil’s face, strip by strip up its vertical diameter — the AREA under each curve is that estimate of the flux through one loop. Green is the true strip, B_x integrated along the chord, off the page as well as in it. Cyan is PhET’s: the in-page value B_x(y, 0) carried across the whole chord (the dots are its own samples, every 5 mm). Cyan runs above green because the field is weaker off the page than in it, so the flux comes out high. Below: the ratio of the two estimates across the area slider — worse for a bigger coil, which reaches further from the magnet.',
  'The two flux integrands strip by strip up the coil’s diameter — the area under each is that estimate of the flux. PhET’s (cyan) runs high; below, the ratio across the area slider.'];
function faceGeo(ctx,W,H){ return stageLayoutH(ctx,W,H,FACE_CAP[0],FACE_CAP[1],1,0.46,1); }
function drawFaceView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const L=faceGeo(ctx,W,H), b=L.main, b2=L.bottom[0], C=M.fc, S=C.rd.S;
  const ex=C.ex.map(v=>v*S), ph=C.ph.map(v=>v*S);
  let lo=0, hi=0; for(const v of ex.concat(ph)){ lo=Math.min(lo,v); hi=Math.max(hi,v); }
  if(!(hi>lo)){ hi=1; lo=-1; }
  const pd=0.12*(hi-lo);
  axesQ(ctx,b,-C.rc,C.rc,lo-pd,hi+pd,{ylab:'flux per mm of height, G·mm',
    title:'adding the field over the coil’s face (mm up its diameter), magnet at '+fmt(wrap2pi(ST.th)*R2D,0)+'°',nx:8,ny:6});
  polyline(ctx,b,C.s,ph,-C.rc,C.rc,lo-pd,hi+pd,COL.struct,1.5);
  polyline(ctx,b,C.s,ex,-C.rc,C.rc,lo-pd,hi+pd,COL.north,2);
  const X=x=>b.x+b.w*(x+C.rc)/(2*C.rc), Y=v=>b.y1-b.h*(v-(lo-pd))/((hi+pd)-(lo-pd));
  if(ST.phetCmp) for(const p of C.sp) dot(ctx,X(p.s),Y(p.p*S),Math.max(1.8,2.6),COL.struct,'#070b18',0.8);
  legendAuto(ctx,b,[[COL.north,'exact: B'+String.fromCharCode(8339)+' integrated along the chord'],[COL.struct,'PhET: the in-page value across the chord']]);
  /* the ratio across the slider */
  const pct=C.ratios.map(r=>100*(r-1));
  let l2=0, h2=0; for(const v of pct){ l2=Math.min(l2,v); h2=Math.max(h2,v); }
  const pd2=Math.max(1,0.15*(h2-l2));
  axesQ(ctx,b2,PICK_AMIN_PCT,100,l2-pd2,h2+pd2,{xlab:'loop area, % of PhET’s maximum',ylab:'line sample − 1, %',
    title:'PhET’s line sample, against the area integral',nx:6,ny:5});
  const X2=p=>b2.x+b2.w*(p-PICK_AMIN_PCT)/(100-PICK_AMIN_PCT), Y2=v=>b2.y1-b2.h*(v-(l2-pd2))/((h2+pd2)-(l2-pd2));
  ctx.beginPath(); ctx.moveTo(b2.x,Y2(0)); ctx.lineTo(b2.x1,Y2(0)); ctx.strokeStyle=COL.ref; ctx.lineWidth=1.2; ctx.setLineDash([6,4]); ctx.stroke(); ctx.setLineDash([]);
  polyline(ctx,b2,C.pcts,pct,PICK_AMIN_PCT,100,l2-pd2,h2+pd2,COL.north,2);
  /* the marker carries no text: chasing it with a label walks it into the y-tick gutter
     (Known-bad -- a label that moves with the data must be placed, not attached).  The
     readout prints the number. */
  dot(ctx,X2(ST.area),Y2(100*(C.ratio-1)),Math.max(2.5,3.5),COL.live);
  legendAuto(ctx,b2,[[COL.north,'PhET’s estimate / the area integral − 1'],[COL.ref,'no error']]);
  if(S===0) lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2-20,'strength 0: no field over the coil’s face',COL.dim,LAB_FONT,'center','middle');
  drawCaption(ctx,L);
}
