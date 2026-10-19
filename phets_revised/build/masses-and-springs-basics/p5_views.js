
/* ================================================================== *
 *  the analysis views, the dispatcher and the scene                   *
 * ================================================================== */

/* ---- view 4: the period law --------------------------------------- */
const PER_CAP_FULL='T = 2&pi;&radic;(m/k) and nothing else: not the amplitude, not the gravity. The green points are the period MEASURED from the '
  +'drawn motion &mdash; two crossings of the resting point, found by bisecting the same solution the stage integrates &mdash; laid on the orange '
  +'closed form. Below left, the same spring and mass on four gravities: the hanging point moves by the ratio of the g&rsquo;s and the period does '
  +'not move at all. Below right, damping lengthens the period by 1/&radic;(1 &minus; ζ&sup2;), which is second order and so barely shows until '
  +'ζ is large.';
const PER_CAP_SHORT='T = 2&pi;&radic;(m/k): measured against the closed form, and unmoved by gravity.';
/* the four analytic curves are the REFERENCE role, so none of them may take
   the green reserved for the measured points or the magenta for the live one */
const KCOLS={3:'#e8843a',6:'#e0cf4a',9:'#5ac8e0',12:'#9a7fd1'};
function drawPeriod(ctx,W,H,M){
  const P=M.per;
  const L=layoutFor(ctx,W,H,'per');
  const b=L.main, gms=P.ms.map(m=>1000*m);
  let tmax=0; for(const c of P.curves) tmax=Math.max(tmax,Math.max.apply(null,c.T));
  axesR(ctx,b,MASS_G_MIN,MASS_G_MAX,0,tmax*1.06,ax2(b,MASS_G_MIN,MASS_G_MAX,0,tmax*1.06,{xlab:'mass, g',ylab:'period, s',
    title:titleFor(b,'the period against the mass, at the four spring constants PhET&rsquo;s slider marks','the period against the mass')}));
  for(const c of P.curves) polyline(ctx,b,gms,c.T,MASS_G_MIN,MASS_G_MAX,0,tmax*1.06,KCOLS[c.k]||COL.ref,1.8);
  for(const p of P.pts) marker(ctx,b,MASS_G_MIN,MASS_G_MAX,0,tmax*1.06,1000*p.m,p.T,COL.pos);
  marker(ctx,b,MASS_G_MIN,MASS_G_MAX,0,tmax*1.06,1000*P.m,P.T0,COL.live);
  legendAuto(ctx,b,[[KCOLS[3],'k = 3 N/m'],[KCOLS[6],'k = 6'],[KCOLS[9],'k = 9'],
                    [KCOLS[12],'k = 12'],[COL.pos,'measured from the motion, k = '+fmt(P.k,0)],
                    [COL.live,'the setting now']]);
  lab(ctx,W,H,b.x+8,b.y1-8,'worst |measured - 2 pi sqrt(m/k)| = '+sigf(Math.max.apply(null,P.pts.map(p=>Math.abs(p.T-p.T0))),2)+' s',
      COL.dim,SM_FONT,'left','bottom');
  const b0=L.bottom[0];
  if(b0){
    const ymax=Math.max.apply(null,P.planets.map(p=>100*p.ye))*1.25;
    axesR(ctx,b0,0,P.planets.length,0,ymax,ax2(b0,0,P.planets.length,0,ymax,{xticks:[],ylab:'extension, cm',
      title:titleFor(b0,'the same spring on four gravities','four gravities')}));
    const wpx=b0.w/P.planets.length;
    for(let i=0;i<P.planets.length;i++){
      const pl=P.planets[i], X=b0.x+wpx*(i+0.5), hpx=b0.h*100*pl.ye/ymax;
      ctx.fillStyle=rgba(COL.pos,0.45); ctx.fillRect(X-wpx*0.26,b0.y1-hpx,wpx*0.52,hpx);
      ctx.strokeStyle=COL.pos; ctx.lineWidth=1.2; ctx.strokeRect(X-wpx*0.26,b0.y1-hpx,wpx*0.52,hpx);
      lab(ctx,W,H,X,b0.y1-hpx-8,sigf(100*pl.ye,3)+' cm',COL.pos,SM_FONT,'center','bottom');
      lab(ctx,W,H,X,b0.y1+7,pl.name,COL.dim,SM_FONT,'center','top');
    }
    lab(ctx,W,H,b0.x+b0.w/2,b0.y+10,'T = '+sigf(P.planets[0].T,5)+' s on every one of them',COL.ref,LAB_FONT,'center','top');
  }
  const b1=L.bottom[1];
  if(b1){
    axesR(ctx,b1,0,1,1,3.2,ax2(b1,0,1,1,3.2,{xlab:'damping ratio zeta',ylab:'T_d / T',
      title:titleFor(b1,'damping lengthens the period','T_d / T')}));
    ctx.fillStyle=rgba(COL.struct,0.10);
    ctx.fillRect(b1.x,b1.y,b1.w*P.zMaxPhet,b1.h);
    polyline(ctx,b1,P.zs,P.stretch,0,1,1,3.2,COL.ref,1.8);
    marker(ctx,b1,0,1,1,3.2,Math.min(P.zeta,0.999),Math.min(isFinite(P.Td)?P.Td/P.T0:3.2,3.2),COL.live);
    lab(ctx,W,H,b1.x+b1.w*P.zMaxPhet-5,b1.y+12,'PhET reaches zeta = '+sigf(P.zMaxPhet,4),COL.struct,SM_FONT,'right','top');
  }
  drawCaption(ctx,L);
}

/* ---- view 5: the damping ------------------------------------------ */
const DMP_CAP_FULL='One number decides everything a damped spring does: ζ = b/(2&radic;(km)). Below 1 it oscillates inside an e<sup>&minus;&gamma;t</sup> '
  +'envelope, at exactly 1 it returns in the shortest time without crossing, above 1 it crawls back more slowly than that. Below left is where '
  +'PhET can go: its damping stops at 0.7 N s/m while 2&radic;(km) never falls below 0.7746 over its own masses and springs, so every state it can '
  +'draw is underdamped &mdash; the critical and overdamped curves above are outside its range and are marked so. Below right: released from rest, '
  +'the turning points fall exactly half a damped period apart and the amplitude is multiplied by e<sup>&minus;&delta;/2</sup> at each one.';
const DMP_CAP_SHORT='ζ = b/(2&radic;(km)) decides everything; PhET&rsquo;s own ranges never reach ζ = 1.';
function drawDamping(ctx,W,H,M){
  const D=M.dmp;
  const L=layoutFor(ctx,W,H,'dmp');
  const b=L.main, tmax=D.ts[D.ts.length-1];
  /* no curve ever exceeds u0, so a top band 0.6 u0 deep is always free and
     legendAuto has a corner to sit in rather than dropping the key */
  axesR(ctx,b,0,tmax,-100*D.u0*1.15,100*D.u0*1.6,ax2(b,0,tmax,-100*D.u0*1.15,100*D.u0*1.6,{xlab:'time, s',ylab:'u, cm',
    title:titleFor(b,'the three regimes of m u" + b u\' + k u = 0, all released from rest at the same place','the three regimes')}));
  polyline(ctx,b,[0,tmax],[0,0],0,tmax,-100*D.u0*1.15,100*D.u0*1.6,rgba(COL.dim,0.5),1,[3,4]);
  polyline(ctx,b,D.ts,D.env.map(x=>100*x),0,tmax,-100*D.u0*1.15,100*D.u0*1.6,rgba(COL.pos,0.45),1.1,[5,4]);
  polyline(ctx,b,D.ts,D.env.map(x=>-100*x),0,tmax,-100*D.u0*1.15,100*D.u0*1.6,rgba(COL.pos,0.45),1.1,[5,4]);
  for(const c of D.curves) polyline(ctx,b,D.ts,c.u.map(x=>100*x),0,tmax,-100*D.u0*1.15,100*D.u0*1.6,c.col,1.8);
  legendAuto(ctx,b,D.curves.map(c=>[c.col,c.lab+', b = '+sigf(c.b,3)+(c.b>BMAX?' (beyond PhET)':'')])
    .concat([[rgba(COL.pos,0.45),'envelope e^(-gam t)']]));
  const b0=L.bottom[0];
  if(b0){
    const bmax=4.2, xlo=0.6, xhi=4.0;
    axesR(ctx,b0,xlo,xhi,0,bmax,ax2(b0,xlo,xhi,0,bmax,{xlab:'2 sqrt(km), N s/m',ylab:'damping b, N s/m',
      title:titleFor(b0,'where PhET can go on the damping plane','PhET’s reachable box')}));
    ctx.fillStyle=rgba(COL.struct,0.13);
    ctx.fillRect(b0.x+b0.w*(D.bcMin-xlo)/(xhi-xlo),b0.y1-b0.h*BMAX/bmax,
                 b0.w*(D.bcMax-D.bcMin)/(xhi-xlo),b0.h*BMAX/bmax);
    polyline(ctx,b0,[xlo,xhi],[xlo,xhi],xlo,xhi,0,bmax,COL.ref,1.8);
    polyline(ctx,b0,[xlo,xhi],[BMAX,BMAX],xlo,xhi,0,bmax,COL.struct,1.3,[6,4]);
    marker(ctx,b0,xlo,xhi,0,bmax,D.bc,M.st.zeta*D.bc,COL.live);
    lab(ctx,W,H,b0.x1-6,b0.y1-b0.h*BMAX/bmax-7,'b = 0.7, the top of PhET’s slider',COL.struct,SM_FONT,'right','bottom');
    lab(ctx,W,H,b0.x+b0.w*0.52,b0.y+14,'b = 2 sqrt(km): critical',COL.ref,SM_FONT,'left','top');
  }
  const b1=L.bottom[1];
  if(b1){
    if(isFinite(D.Td)&&D.peaks.length){
      const ns=D.peaks.map(p=>p.n), us=D.peaks.map(p=>100*Math.abs(p.u));
      const an=[]; for(let i=0;i<=50;i++) an.push(5*i/50);
      axesR(ctx,b1,0,5,0,100*D.u0*1.08,ax2(b1,0,5,0,100*D.u0*1.08,{xlab:'whole periods elapsed',ylab:'|u| at the turn, cm',
        title:titleFor(b1,'the amplitude falls by e^(-delta) every period','amplitude per period')}));
      polyline(ctx,b1,an,an.map(n=>100*D.u0*Math.exp(-D.ld*n)),0,5,0,100*D.u0*1.08,COL.ref,1.6);
      for(let i=0;i<ns.length;i++) marker(ctx,b1,0,5,0,100*D.u0*1.08,ns[i],us[i],COL.pos);
      lab(ctx,W,H,b1.x1-6,b1.y+12,'delta = gam T_d = '+sigf(D.ld,4),COL.pos,SM_FONT,'right','top');
    } else {
      axesR(ctx,b1,0,5,0,100*D.u0*1.08,ax2(b1,0,5,0,100*D.u0*1.08,{xlab:'whole periods elapsed',ylab:'|u| at the turn, cm',title:'amplitude per period'}));
      caption(ctx,b1.x+8,b1.y+b1.h/2-14,'zeta >= 1: it never turns, so there is no period to count',b1.w-16,COL.ref,CAP_FONT);
    }
  }
  drawCaption(ctx,L);
}

/* ---- view 6: the energy ------------------------------------------- */
const ENG_CAP_FULL='The lab spring let go from its unstretched end, followed for three periods. Kinetic energy, the energy stored in the spring '
  +'and the height gravity has yet to take &mdash; measured from the bottom of the swing, so none of the three is ever negative &mdash; trade back '
  +'and forth; the damper takes the rest, at b v&sup2; a second. The white line is their sum, flat to the last digit because the propagator is the '
  +'closed form, and equal to 2(mg)&sup2;/k. At the resting point the spring has stored exactly half of what gravity has given up.';
const ENG_CAP_SHORT='Three periods of the lab spring: the four shares, and their sum flat to the last digit at 2(mg)&sup2;/k.';
function drawEnergy(ctx,W,H,M){
  const E=M.eng;
  const L=layoutFor(ctx,W,H,'eng');
  const b=L.main, tmax=E.ts[E.ts.length-1];
  const mJ=a=>a.map(v=>1000*v);
  let lo=0, hi=0;
  for(const a of [E.KE,E.PEe,E.PEg,E.TH,E.TOT]) for(const v of a){ if(1000*v<lo) lo=1000*v; if(1000*v>hi) hi=1000*v; }
  /* a wide band above the curves, so the legend has a corner to sit in
     (Known-bad: legendAuto draws nothing rather than lying, and then the key
     for five curves is simply missing) */
  const pad=0.09*(hi-lo), padT=0.55*(hi-lo);
  lo=lo-pad; hi=hi+padT;
  const pad0=0;
  axesR(ctx,b,0,tmax,lo-pad0,hi+pad0,ax2(b,0,tmax,lo-pad0,hi+pad0,{xlab:'time, s',ylab:'energy, mJ',
    title:titleFor(b,'the four shares and their sum, three periods from the unstretched end','the four shares and their sum')}));
  polyline(ctx,b,[0,tmax],[0,0],0,tmax,lo-pad0,hi+pad0,rgba(COL.dim,0.45),1,[3,4]);
  polyline(ctx,b,E.ts,mJ(E.PEe),0,tmax,lo-pad0,hi+pad0,COL.pel,1.7);
  polyline(ctx,b,E.ts,mJ(E.PEg),0,tmax,lo-pad0,hi+pad0,COL.pgr,1.7);
  polyline(ctx,b,E.ts,mJ(E.KE),0,tmax,lo-pad0,hi+pad0,COL.ke,1.7);
  polyline(ctx,b,E.ts,mJ(E.TH),0,tmax,lo-pad0,hi+pad0,COL.th,1.7);
  polyline(ctx,b,E.ts,mJ(E.TOT),0,tmax,lo-pad0,hi+pad0,COL.tot,2.1,[9,4]);
  legendAuto(ctx,b,[[COL.ke,'kinetic'],[COL.pel,'elastic'],[COL.pgr,'gravitational'],
                    [COL.th,'thermal (the damper)'],[COL.tot,'their sum, '+sigf(E.Etot,5)+' J']]);
  const b0=L.bottom[0], sp=M.springs[0];
  if(b0){
    const bars=[{n:'kinetic',v:sp.on?1000*sp.KE:0,c:COL.ke},{n:'elastic',v:sp.on?1000*sp.PEe:0,c:COL.pel},
                {n:'gravity',v:sp.on?1000*sp.PEg:0,c:COL.pgr},{n:'thermal',v:sp.on?1000*sp.Eth:0,c:COL.th},
                {n:'sum',v:sp.on?1000*(sp.KE+sp.PEe+sp.PEg+sp.Eth):0,c:COL.tot}];
    let blo=0,bhi=0; for(const x of bars){ if(x.v<blo) blo=x.v; if(x.v>bhi) bhi=x.v; }
    const span=Math.max(1e-6,bhi-blo)*1.25, base=blo-0.1*span;
    axesR(ctx,b0,0,bars.length,base,base+span,ax2(b0,0,bars.length,base,base+span,{xticks:[],ylab:'energy, mJ',
      title:titleFor(b0,'the shares at this instant','now')}));
    const wpx=b0.w/bars.length, Y0=b0.y1-b0.h*(0-base)/span;
    for(let i=0;i<bars.length;i++){
      const X=b0.x+wpx*(i+0.5), Y=b0.y1-b0.h*(bars[i].v-base)/span;
      ctx.fillStyle=rgba(bars[i].c,0.42); ctx.fillRect(X-wpx*0.24,Math.min(Y,Y0),wpx*0.48,Math.abs(Y-Y0));
      ctx.strokeStyle=bars[i].c; ctx.lineWidth=1.2; ctx.strokeRect(X-wpx*0.24,Math.min(Y,Y0),wpx*0.48,Math.abs(Y-Y0));
      lab(ctx,W,H,X,b0.y1+7,bars[i].n,COL.dim,SM_FONT,'center','top');
    }
    ctx.strokeStyle=rgba(COL.dim,0.5); ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(b0.x,Y0); ctx.lineTo(b0.x1,Y0); ctx.stroke();
  }
  const b1=L.bottom[1];
  if(b1){
    const m=E.m, k=E.k, bb=E.b, u0=-E.ye, Td=periodD(m,k,bb), ld=logDec(m,k,bb);
    const nmax=6, ns=[], Es=[], an=[], ae=[];
    const E0=energyU(m,k,u0,0);
    for(let n=0;n<=nmax;n++){ const t=n*Td/2, r=prop(m,k,bb,u0,0,t);
      ns.push(n/2); Es.push(1000*energyU(m,k,r[0],r[1])); }
    for(let i=0;i<=60;i++){ const n=nmax*i/60; an.push(n/2); ae.push(1000*E0*Math.exp(-ld*n)); }
    const Emax=1000*E0*1.08;
    axesR(ctx,b1,0,nmax/2,0,Emax,ax2(b1,0,nmax/2,0,Emax,{xlab:'whole periods elapsed',ylab:'E at the turn, mJ',
      title:titleFor(b1,'the energy at each turning point, exactly E0 e^(-n delta)','energy per turn')}));
    polyline(ctx,b1,an,ae,0,nmax/2,0,Emax,COL.ref,1.6);
    for(let i=0;i<ns.length;i++) marker(ctx,b1,0,nmax/2,0,Emax,ns[i],Es[i],COL.pos);
    lab(ctx,W,H,b1.x1-6,b1.y+12,bb>0?'delta = '+sigf(ld,4)+', kept per period e^(-2 delta) = '+sigf(Math.exp(-2*ld),3)
      :'no damping: every turn is the same height',COL.pos,SM_FONT,'right','top');
  }
  drawCaption(ctx,L);
}

/* ---- dispatch ------------------------------------------------------ *
 * one layout per view, used by the drawing AND by the pointer hit-test,
 * so the two cannot drift apart (waveguides.html, Known-bad)            */
function viewCaps(v){
  if(v==='bnc') return [BNC_CAP_FULL,BNC_CAP_SHORT,1,0.38];
  if(v==='lab') return [LAB_CAP_FULL,LAB_CAP_SHORT,1,0.38];
  if(v==='per') return [PER_CAP_FULL,PER_CAP_SHORT,2,0.40];
  if(v==='dmp') return [DMP_CAP_FULL,DMP_CAP_SHORT,2,0.40];
  if(v==='eng') return [ENG_CAP_FULL,ENG_CAP_SHORT,2,0.40];
  return [STR_CAP_FULL,STR_CAP_SHORT,1,0.34];
}
function layoutFor(ctx,W,H,v){
  if(v==='str'||v==='bnc'||v==='lab') return splitLayout(ctx,W,H,v);
  const a=viewCaps(v);
  return stageLayout(ctx,W,H-HINT_H,a[0],a[1],a[2],a[3],1);
}
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  const v=M.view;
  if(v==='str') drawStretch(ctx,W,H,M);
  else if(v==='bnc') drawBounce(ctx,W,H,M);
  else if(v==='lab') drawLab(ctx,W,H,M);
  else if(v==='per') drawPeriod(ctx,W,H,M);
  else if(v==='dmp') drawDamping(ctx,W,H,M);
  else drawEnergy(ctx,W,H,M);
}

function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame: only the three PhET screens and the energy view carry a clock */
  S.step=function(dtWall){
    if(!ST.running) return false;
    if(!liveViews(ST.view)) return false;
    const dts=(dtWall||0)*(ST.speed==='slow'?SLOW:1);
    if(!(dts>0)) return false;
    advance(ST,dts);
    return true;
  };
  /* the pointer: PhET's own three draggables — the hanging mass, the movable
     reference line and the ruler */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null;
      if(DRAG.what==='mass'){ LIVE.slot[DRAG.sp].v=0; }
      DRAG.what=null; return had; }
    if(ST.view!=='str'&&ST.view!=='bnc'&&ST.view!=='lab') return false;
    const ctx=canvas.getContext('2d'), M=buildModel();
    const L=layoutFor(ctx,S.W,S.H,ST.view);
    const map=stageMap(M,L.main), wy=map.wy(y), wx=map.wx(x);
    if(type==='down'){
      if(ST.ruler&&wx>=ST.rulerX&&wx<=ST.rulerX+RULER_W&&wy<=ST.rulerY&&wy>=ST.rulerY-RULER_L){
        DRAG.what='ruler'; DRAG.ox=ST.rulerX-wx; DRAG.oy=ST.rulerY-wy; return true; }
      if(ST.movLine&&Math.abs(y-map.Y(ST.movY))<=7){ DRAG.what='movline'; DRAG.oy=ST.movY-wy; return true; }
      for(const s of M.springs){
        if(!s.on) continue;
        const r=massRectPx(map,s);
        if(x>=r.x-3&&x<=r.x1+3&&y>=r.y-3&&y<=r.y1+3){
          DRAG.what='mass'; DRAG.sp=s.i; DRAG.oy=s.bottom-wy; return true; }
      }
      return false;
    }
    if(type==='move'){
      if(DRAG.what==='ruler'){ ST.rulerX=clamp(wx+DRAG.ox,0.15,2.0); ST.rulerY=clamp(wy+DRAG.oy,0.2,CEILING_Y+0.05); return true; }
      if(DRAG.what==='movline'){ ST.movY=clamp(wy+DRAG.oy,FLOOR_Y,CEILING_Y); return true; }
      if(DRAG.what==='mass'){
        const bot=wy+DRAG.oy;
        LIVE.slot[DRAG.sp].y=clamp(CEILING_Y-L0-bot,-0.12,1.55);
        LIVE.slot[DRAG.sp].v=0;
        return true;
      }
    }
    return false;
  };
  return S;
}
