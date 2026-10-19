
/* ================================================================== *
 *  the three sky views — PhET's observation window, drawn once as     *
 *  waves, once as photons and once as the bare layer model            *
 * ================================================================== */

/* a caption under a panel, drawn only if it clears the main caption: at 560 x 380 the
   ladder's "Points: the flux system solved" ran into the HTML #hint (Known-bad) */
function capUnder(ctx,x,y,txt,w,limitY){
  const ls=wrapText(ctx,txt,w,SM_FONT).length;
  if(y+ls*14>limitY) return 0;
  return caption(ctx,x,y,txt,w,'#767e92',SM_FONT);
}

/* the stage: the window, a thermometer column, an optional flux panel, a caption */
function skyLayout(ctx,W,H,M,capFull,capShort){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+180);
  const availH=Math.max(120,fit.capY-18-top);
  const span=right-left;
  const showFlux=ST.flux&&span>=620;
  const thermW=Math.min(150,Math.max(96,span*0.13));
  const fluxW=showFlux?Math.min(280,span*0.26):0;
  const winW=span-thermW-fluxW-(showFlux?26:0)-14;
  const win=box(left,top,Math.max(160,winW),availH);
  const therm=box(win.x1+14,top,thermW,availH);
  const flux=showFlux?box(therm.x1+26,top,fluxW,availH):null;
  const exag=(win.h/GH.TOP)/(win.w/GH.SPAN_W);
  return {narrow,left,right,win,therm,flux,showFlux,
          capY:fit.capY,capTxt:fit.txt,capW,exag,top};
}
/* the ground is a band at the bottom of the window, and altitude zero is its TOP surface:
   mapping z = 0 to win.y1 instead drew every low photon inside the soil */
function groundH(win){ return Math.max(10,win.h*0.045); }
function skyMapOf(win){
  const gh=groundH(win), y0=win.y1-gh, hh=win.h-gh;
  return {gh, y0,
          yOf:z=>y0-hh*clamp(z,0,GH.TOP)/GH.TOP,
          xOf:x=>win.x+win.w*(x+GH.SPAN_W/2)/GH.SPAN_W,
          zOf:Y=>GH.TOP*(y0-Y)/hh};
}

/* a wave line drawn as NBAND constant-alpha sub-paths, so one line is a handful of strokes
   rather than a hundred: the display-list capture stays readable and the browser stays fast */
const NBAND=6;
function waveLine(ctx,x,yA,yB,amp,wl,phase,col,alphaAt,lw){
  const dy=yB-yA, n=48;
  for(let b=0;b<NBAND;b++){
    const t0=b/NBAND, t1=(b+1)/NBAND;
    const al=alphaAt((t0+t1)/2);
    if(al<=0.012) continue;
    ctx.beginPath();
    const i0=Math.floor(t0*n), i1=Math.ceil(t1*n);
    for(let i=i0;i<=i1;i++){
      const t=i/n, y=yA+dy*t, xx=x+amp*Math.sin(TAU*(y/wl)+phase);
      if(i===i0) ctx.moveTo(xx,y); else ctx.lineTo(xx,y);
    }
    ctx.strokeStyle=rgba(col,clamp(al,0,1)); ctx.lineWidth=lw||2; ctx.lineJoin='round';
    ctx.stroke();
  }
}
function arrowV(ctx,x,y,dir,col,size){
  const s=size||6;
  ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-s*0.6,y+dir*s); ctx.lineTo(x+s*0.6,y+dir*s);
  ctx.closePath(); ctx.fillStyle=col; ctx.fill();
}

/* the window itself: sky, ground, cloud, the sheets */
function drawWindow(ctx,W,H,M,L){
  const S=M.S, win=L.win, mp=skyMapOf(win);
  /* the sky, dark above and a little lighter at the ground */
  const NB=10;
  for(let i=0;i<NB;i++){
    const y0=win.y+win.h*i/NB, y1=win.y+win.h*(i+1)/NB;
    ctx.fillStyle=mix(COL.sky0,COL.sky1,(i+0.5)/NB);
    ctx.fillRect(win.x,y0,win.w,y1-y0+0.6);
  }
  /* the ground */
  const gh=mp.gh;
  const glac=S.A.kind==='conc'&&ST.mode==='date'&&currentDate().glacier;
  ctx.fillStyle=glac?COL.glacier:COL.ground;
  ctx.fillRect(win.x,win.y1-gh,win.w,gh);
  ctx.fillStyle=glac?'#eef6fb':'#3f8a44';
  ctx.fillRect(win.x,win.y1-gh,win.w,3);
  /* the sheets */
  for(let i=0;i<S.a.length;i++){
    const y=mp.yOf(S.alt[i]), a=S.a[i];
    if(a<=0){
      if(S.A.kind==='lm'&&ST.sheets){
        ctx.beginPath(); ctx.moveTo(win.x+4,y); ctx.lineTo(win.x1-4,y);
        ctx.strokeStyle=rgba(COL.dim,0.28); ctx.lineWidth=1; ctx.setLineDash([5,5]);
        ctx.stroke(); ctx.setLineDash([]);
      }
      continue;
    }
    const strong=S.A.kind==='lm';
    if(strong||ST.sheets){
      ctx.fillStyle=rgba(COL.sheet,clamp(0.10+0.55*a,0,0.72));
      ctx.fillRect(win.x+4,y-(strong?4:1.6),win.w-8,strong?8:3.2);
    }
  }
  /* the cloud */
  if(S.A.cloud){
    const cx=mp.xOf(GH.CLOUD_X), cy=mp.yOf(GH.CLOUD_Y);
    const rx=win.w*GH.CLOUD_W/GH.SPAN_W/2, ry=win.h*GH.CLOUD_H/GH.TOP/2;
    const pts=[];
    for(let k=0;k<=30;k++){ const th=TAU*k/30; pts.push([cx+rx*Math.cos(th),cy+ry*Math.sin(th)]); }
    ctx.beginPath();
    pts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));
    ctx.closePath(); ctx.fillStyle=rgba(COL.cloud,0.55); ctx.fill();
    ctx.strokeStyle=rgba('#e6eef7',0.5); ctx.lineWidth=1; ctx.stroke();
  }
  /* the sun's disc, in the window's top-left corner */
  if(ST.sun){
    const sx=win.x+win.w*0.09, sy=win.y+win.h*0.055, r=Math.min(16,win.h*0.035);
    dot(ctx,sx,sy,r,COL.sun);
    ctx.strokeStyle=rgba(COL.sun,0.5); ctx.lineWidth=1.4;
    for(let k=0;k<8;k++){ const th=TAU*k/8;
      ctx.beginPath(); ctx.moveTo(sx+r*1.35*Math.cos(th),sy+r*1.35*Math.sin(th));
      ctx.lineTo(sx+r*2.0*Math.cos(th),sy+r*2.0*Math.sin(th)); ctx.stroke(); }
  }
  frame(ctx,win,'#2a3347');
  return {mp,gh};
}

/* the altitude scale down the left edge of the window */
function drawAltAxis(ctx,W,H,L){
  const win=L.win, mp=skyMapOf(win);
  ctx.font=SM_FONT; ctx.textAlign='right'; ctx.textBaseline='middle'; ctx.fillStyle='#6f7789';
  for(let z=0;z<=50;z+=10){
    const y=mp.yOf(z*1000);
    ctx.beginPath(); ctx.moveTo(win.x-5,y); ctx.lineTo(win.x,y);
    ctx.strokeStyle='#2a3347'; ctx.lineWidth=1; ctx.stroke();
    ctx.fillText(z,win.x-8,y);
  }
  ctx.save(); ctx.translate(win.x-38,win.y+win.h/2); ctx.rotate(-PI/2);
  ctx.textAlign='center'; ctx.textBaseline='bottom'; ctx.fillStyle='#8b93a6'; ctx.font=LAB_FONT;
  ctx.fillText('altitude, km',0,0); ctx.restore();
}

/* the thermometer column: the surface reading, its steady state and the bare-rock value */
function drawThermometer(ctx,W,H,M,L){
  const S=M.S, b=L.therm, u=M.unit;
  const lm=S.A.kind==='lm';
  const lo=lm?120:238, hi=lm?480:316;
  const tubeW=Math.min(26,b.w*0.30), x=b.x+b.w*0.30;
  const top=b.y+28, bot=b.y1-62;
  const yOf=T=>bot-(bot-top)*(clamp(T,lo,hi)-lo)/(hi-lo);
  ctx.fillStyle='#10131b'; ctx.fillRect(x-tubeW/2,top,tubeW,bot-top);
  frame(ctx,box(x-tubeW/2,top,tubeW,bot-top),'#2a3347');
  dot(ctx,x,bot+11,tubeW*0.72,'#1a1f2b','#2a3347',1);
  /* the fill */
  const yT=yOf(S.Tg);
  ctx.fillStyle=COL.pos; ctx.fillRect(x-tubeW/2+3,yT,tubeW-6,bot-yT);
  dot(ctx,x,bot+11,tubeW*0.72-3,COL.pos);
  /* ticks */
  ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillStyle='#6f7789';
  const step=lm?60:20;
  for(let T=Math.ceil(lo/step)*step;T<=hi;T+=step){
    const y=yOf(T);
    ctx.beginPath(); ctx.moveTo(x+tubeW/2,y); ctx.lineTo(x+tubeW/2+4,y);
    ctx.strokeStyle='#2a3347'; ctx.lineWidth=1; ctx.stroke();
    ctx.fillText(fmt(tempIn(T,u),0),x+tubeW/2+6,y);
  }
  /* the exact steady state, and the bare-rock temperature */
  const marks=[[S.Tsteady,COL.ref,'steady'],[S.Teff,'#8b93a6','no gas']];
  for(const [T,c,nm] of marks){
    if(T<lo||T>hi) continue;
    const y=yOf(T);
    ctx.beginPath(); ctx.moveTo(x-tubeW/2-7,y); ctx.lineTo(x+tubeW/2,y);
    ctx.strokeStyle=c; ctx.lineWidth=1.4; ctx.setLineDash([4,3]); ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,x-tubeW/2-9,y,nm,c,SM_FONT,'right');
  }
  ctx.textAlign='center'; ctx.textBaseline='top'; ctx.font='italic 13px Georgia, serif';
  ctx.fillStyle='#aeb6c6'; ctx.fillText('surface',b.x+b.w/2,b.y+4);
  ctx.font='13px -apple-system, sans-serif'; ctx.fillStyle=COL.pos; ctx.textBaseline='top';
  ctx.fillText(plain(tstr(S.Tg,u,1)),b.x+b.w/2,b.y1-28);
  ctx.font=SM_FONT; ctx.fillStyle='#6f7789';
  ctx.fillText(plain('scale '+fmt(tempIn(lo,u),0)+' to '+fmt(tempIn(hi,u),0)+' '+UNIT_SYM[u]),
               b.x+b.w/2,b.y1-13);
}

/* the energy-balance meter at the top of the atmosphere (PhET's "Energy Balance" panel).
   Its rectangle is registered in LABELS before anything else is labelled, so every later
   lab() dodges it: the box is drawn with ctx.fillText, which the registry cannot see, and
   "redirected down" landed under "top of atmosphere" in every size until it was. */
function balanceBox(L){
  const win=L.win, bw=Math.min(154,win.w*0.30), bh=Math.min(104,win.h*0.30);
  /* below this it cannot hold its own labels: the readout still carries every number */
  if(bw<128||bh<76) return null;
  return box(win.x1-bw-10,win.y+10,bw,bh);
}
function reserveBoxes(L){
  const b=ST.balance?balanceBox(L):null;
  if(b) LABELS.push([b.x,b.y,b.x1,b.y1]);
}
function drawBalance(ctx,W,H,M,L){
  const S=M.S, b=balanceBox(L);
  if(!b) return null;
  ctx.fillStyle='rgba(8,10,18,.80)'; ctx.fillRect(b.x,b.y,b.w,b.h);
  frame(ctx,b,'#2a3347');
  const Sin=S.A.Sin, Safter=S.A.Safter===undefined?Sin:S.A.Safter;
  const out=Sin*(S.A.cloud?CLOUD_REFL:0)+Safter*S.albedo+S.Utop;
  const net=Sin-out;
  const mx=Math.max(1,Sin,out);
  const cols=[COL.sun,COL.ir], vals=[Sin,out], names=['in','out'];
  /* the box, top to bottom: title, bars, the bars' names, the net.  Everything is placed
     from the box's own edges, so a narrow window cannot push a label out of it. */
  const barW=Math.min(24,b.w*0.16), gap=Math.min(20,b.w*0.14), x0=b.x+12;
  const base=b.y1-34, top2=b.y+26;
  ctx.font=SM_FONT; ctx.textAlign='center';
  for(let i=0;i<2;i++){
    const hgt=(base-top2)*vals[i]/mx, x=x0+i*(barW+gap);
    ctx.fillStyle=cols[i]; ctx.fillRect(x,base-hgt,barW,hgt);
    ctx.textBaseline='top'; ctx.fillStyle='#8b93a6'; ctx.fillText(names[i],x+barW/2,base+3);
  }
  ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillStyle='#aeb6c6'; ctx.fillText('top of atmosphere',b.x+8,b.y+6);
  ctx.fillStyle=Math.abs(net)<0.5?COL.pos:COL.ref;
  ctx.fillText(plain('net '+(net>=-0.05?'+':'−')+fmt(Math.abs(net),1)+' W/m²'),b.x+8,b.y1-16);
  return {net,out,Sin};
}

/* the flux meter: the exact upward, downward and net infrared flux against altitude */
function drawFluxPanel(ctx,W,H,M,L){
  const S=M.S, b=L.flux;
  if(!b) return;
  const n=S.a.length;
  const zs=[0].concat(S.alt), Us=S.Ul, Ds=S.Dl;
  const hiF=Math.max(1,S.s.Eg*1.06,S.Ul[0]*1.06);
  const pb=box(b.x,b.y+16,b.w,b.h-106);
  axesR(ctx,pb,0,hiF,0,GH.TOP/1000,{nx:4,ny:6,xlab:'infrared flux, W/m²',ylab:'altitude, km',
        title:titleFor(pb,'the flux meter','flux'),
        xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  /* the profiles are piecewise constant between sheets: draw them as staircases */
  const stair=(vals)=>{
    const xs=[], ys=[];
    for(let i=0;i<vals.length;i++){
      const zlo=zs[i]/1000, zhi=(i+1<zs.length?zs[i+1]:GH.TOP)/1000;
      xs.push(vals[i],vals[i]); ys.push(zlo,zhi);
    }
    return [xs,ys];
  };
  const [ux,uy]=stair(Us), [dx,dy]=stair(Ds);
  const netX=Us.map((u,i)=>u-Ds[i]);
  const [nx2,ny2]=stair(netX);
  const [sx2,sy2]=stair(S.Us);
  polyline(ctx,pb,sx2,sy2,0,hiF,0,GH.TOP/1000,rgba(COL.ref,0.55),2.6);
  polyline(ctx,pb,dx,dy,0,hiF,0,GH.TOP/1000,COL.live,1.8);
  polyline(ctx,pb,ux,uy,0,hiF,0,GH.TOP/1000,COL.pos,2);
  polyline(ctx,pb,nx2,ny2,0,hiF,0,GH.TOP/1000,COL.ref,1.6,[5,4]);
  legendAuto(ctx,pb,[[COL.pos,'up, now'],[COL.live,'down, now'],
                     [rgba(COL.ref,0.55),'up, exact'],[COL.ref,'net']]);
  /* capUnder, not caption: the panel is narrow and this wraps to three lines there, which
     ran into the main caption at 1180 x 760 and 760 x 520 until the room was measured */
  capUnder(ctx,b.x,pb.y1+40,'Settled, the net is the same at every height — and the exact profile lies under the live one.',
           b.w,L.capY-6);
}

/* PhET's flux-meter sensor: a draggable bar across the window reading the exact fluxes */
function drawProbe(ctx,W,H,M,L){
  const S=M.S, win=L.win, mp=skyMapOf(win), y=mp.yOf(S.probe.z);
  ctx.beginPath(); ctx.moveTo(win.x,y); ctx.lineTo(win.x1,y);
  ctx.strokeStyle=rgba(COL.live,0.85); ctx.lineWidth=1.6; ctx.setLineDash([7,4]);
  ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle=COL.live; ctx.fillRect(win.x-6,y-5,12,10);
  lab(ctx,W,H,win.x1-6,y-12,fmt(S.probe.z/1000,1)+' km · up '+fmt(S.probe.U,1)
      +' · down '+fmt(S.probe.D,1),COL.live,SM_FONT,'right');
}

/* ---- view A: the waves -------------------------------------------------- */
const CAP_WAVES='PhET&rsquo;s Waves screen. Sunlight (yellow) crosses the greenhouse gas untouched and warms the ground; the ground sends infrared (red) back up, and every sheet that catches some of it radiates half of that back down. The brightness of each infrared band is the flux the exact solve carries at that height, not a decoration: it steps down at every sheet, and the step is F&thinsp;a/(2&minus;a) &mdash; a few per cent per sheet at PhET&rsquo;s concentrations, which is what the flux meter is for.';
const CAP_WAVES_S='Sunlight down, infrared up; the infrared brightness is the exact transmitted flux.';
function viewWaves(ctx,W,H,M){
  const L=skyLayout(ctx,W,H,M,CAP_WAVES,CAP_WAVES_S);
  const S=M.S, {mp,gh}=drawWindow(ctx,W,H,M,L), win=L.win;
  reserveBoxes(L);
  const ph=(S.t*3)%1*TAU;
  const yGround=win.y1-gh;
  /* sunlight: four lines down the left half */
  if(ST.sun){
    const amp=Math.min(7,win.w*0.012), wl=Math.max(22,win.h*0.075);
    for(let k=0;k<4;k++){
      const x=win.x+win.w*(0.08+0.09*k);
      waveLine(ctx,x,win.y+4,yGround,amp,wl,ph+k*1.1,COL.sun,
        t=>{ const z=GH.TOP*(1-t);
             if(S.A.cloud&&z<GH.CLOUD_Y&&Math.abs(GH.SPAN_W*(0.08+0.09*k)-GH.SPAN_W/2-GH.CLOUD_X)<GH.CLOUD_W/2)
               return 0.75*(1-CLOUD_REFL);
             return 0.75; });
    }
    /* the part the ground throws back */
    if(S.albedo>0.001){
      const x=win.x+win.w*0.40;
      waveLine(ctx,x,yGround,win.y+4,Math.min(5,win.w*0.009),Math.max(20,win.h*0.07),ph,
               COL.sun,()=>0.22+0.5*S.albedo,1.4);
      arrowV(ctx,x,win.y+8,1,rgba(COL.sun,0.7),5);
      lab(ctx,W,H,x+8,win.y+20,fmt(100*S.albedo,0)+' % reflected',rgba(COL.sun,0.85),SM_FONT,'left');
    }
  }
  /* infrared: upward bands on the right, downward beside them */
  const Eg=Math.max(S.Ul[0],S.s.Eg,1e-9);
  const upAlpha=t=>{ const z=GH.TOP*(1-t); return 0.15+0.72*fluxAt(S,z,true)/Eg; };
  const dnAlpha=t=>{ const z=GH.TOP*(1-t); return 0.10+0.72*fluxAt(S,z,false)/Eg; };
  const amp2=Math.min(7,win.w*0.012), wl2=Math.max(20,win.h*0.062);
  for(let k=0;k<3;k++){
    const x=win.x+win.w*(0.54+0.075*k);
    waveLine(ctx,x,yGround,win.y+4,amp2,wl2,ph+k*0.9,COL.ir,upAlpha,2.2);
    arrowV(ctx,x,win.y+8,1,rgba(COL.ir,0.85),5);
  }
  for(let k=0;k<3;k++){
    const x=win.x+win.w*(0.80+0.06*k);
    waveLine(ctx,x,win.y+4,yGround,amp2,wl2,ph+k*1.3+2,COL.ir,dnAlpha,1.8);
    arrowV(ctx,x,yGround-4,-1,rgba(COL.ir,0.8),5);
  }
  lab(ctx,W,H,win.x+win.w*0.545,yGround-14,'infrared out',rgba(COL.ir,0.95),SM_FONT,'left');
  lab(ctx,W,H,win.x+win.w*0.80,win.y+win.h*0.52,'redirected down',rgba(COL.ir,0.8),SM_FONT,'left');
  if(ST.sun) lab(ctx,W,H,win.x+win.w*0.08,win.y+win.h*0.30,'sunlight',rgba(COL.sun,0.9),SM_FONT,'left');
  drawProbe(ctx,W,H,M,L);
  drawAltAxis(ctx,W,H,L);
  if(ST.balance) drawBalance(ctx,W,H,M,L);
  drawThermometer(ctx,W,H,M,L);
  if(L.showFlux) drawFluxPanel(ctx,W,H,M,L);
  lab(ctx,W,H,win.x+6,mp.y0-5,'vertical scale ×'+fmt(L.exag,2)+' the horizontal',
      '#8b93a6',SM_FONT,'left','bottom');
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}
/* the exact flux at a height, from the steady solve (piecewise constant between sheets) */
function fluxAt(S,z,up){
  const zs=S.alt;
  let i=0;
  while(i<zs.length&&z>=zs[i]) i++;
  return up?S.Ul[i]:S.Dl[i];
}

/* ---- view B: the photons ------------------------------------------------ */
const CAP_PHOTONS='PhET&rsquo;s Photons screen, one photon at a time. Yellow photons fall from the sun and are absorbed by the ground or bounced off it; red infrared photons leave the ground at &sigma;T&#8308;/7.8 per second and, on crossing a sheet, are absorbed with probability a and later sent off again up or down at even odds. A seeded generator drives all of it, so the picture is the same every run &mdash; and the chance a photon ever reaches space is the flux ratio F/&sigma;T_s&#8308;, which the panel measures.';
const CAP_PHOTONS_S='Photons absorbed with probability a, re-emitted up or down at even odds.';
function viewPhotons(ctx,W,H,M){
  const L=skyLayout(ctx,W,H,M,CAP_PHOTONS,CAP_PHOTONS_S);
  const S=M.S, {mp,gh}=drawWindow(ctx,W,H,M,L), win=L.win;
  reserveBoxes(L);
  const r=Math.max(2,Math.min(3.6,win.w*0.0045));
  for(const p of S.photons){
    const x=mp.xOf(p.x), y=mp.yOf(p.y)-(p.ir?0:0);
    if(y<win.y-2||y>win.y1+2) continue;
    if(p.hold>0){ dot(ctx,x,y,r*1.5,rgba(COL.ir,0.35)); dot(ctx,x,y,r,COL.ir); }
    else dot(ctx,x,y,r,p.ir?COL.ir:COL.sun);
  }
  drawProbe(ctx,W,H,M,L);
  drawAltAxis(ctx,W,H,L);
  /* the measured statistics, on the window */
  const mcb=box(win.x+8,win.y+8,Math.min(216,win.w*0.42),58);
  LABELS.push([mcb.x,mcb.y,mcb.x1,mcb.y1]);
  ctx.fillStyle='rgba(8,10,18,.94)'; ctx.fillRect(mcb.x,mcb.y,mcb.w,mcb.h);
  frame(ctx,mcb,'#2a3347');
  ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillStyle='#aeb6c6'; ctx.fillText(plain('escape chance of an IR photon'),mcb.x+7,mcb.y+6);
  ctx.fillStyle=COL.ref; ctx.fillText(plain('exact  '+fmt(100*S.pExact,3)+' %'),mcb.x+7,mcb.y+22);
  ctx.fillStyle=COL.pos;
  ctx.fillText(plain('measured  '+fmt(100*S.mc.p,3)+' % ('+S.mc.m+' walks)'),mcb.x+7,mcb.y+38);
  if(ST.balance) drawBalance(ctx,W,H,M,L);
  drawThermometer(ctx,W,H,M,L);
  if(L.showFlux) drawFluxPanel(ctx,W,H,M,L);
  lab(ctx,W,H,win.x+6,mp.y0-5,(ST.morePhotons?'every simulated photon drawn':
      'one photon in '+GH.SHOW_ONE_IN+' drawn (PhET)')
      +' · vertical scale ×'+fmt(L.exag,2),'#8b93a6',SM_FONT,'left','bottom');
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}

/* ---- view C: the layers ------------------------------------------------- */
const CAP_LAYERS='PhET&rsquo;s Layer Model screen, with the sheets made explicit. Each is a sheet of glass: transparent to sunlight, absorbing a fraction a of the infrared crossing it, and radiating away exactly what it absorbs &mdash; half up and half down. Because each sheet balances, the NET upward flux is the same at every height, so the upward flux simply steps down by F&thinsp;a/(2&minus;a) at each sheet and the surface has to be hotter by the same total.';
const CAP_LAYERS_S='Sheets of glass: each radiates away what it absorbs, half up and half down.';
function viewLayers(ctx,W,H,M){
  const L=skyLayout(ctx,W,H,M,CAP_LAYERS,CAP_LAYERS_S);
  const S=M.S, {mp,gh}=drawWindow(ctx,W,H,M,L), win=L.win;
  reserveBoxes(L);
  const yGround=win.y1-gh, ph=(S.t*3)%1*TAU;
  if(ST.sun){
    const amp=Math.min(6,win.w*0.011), wl=Math.max(22,win.h*0.075);
    for(let k=0;k<3;k++)
      waveLine(ctx,win.x+win.w*(0.09+0.075*k),win.y+4,yGround,amp,wl,ph+k*1.1,COL.sun,()=>0.7);
  }
  /* between each pair of levels, the up and down arrows with their flux written on them */
  const zs=[0].concat(S.alt), n=S.a.length;
  const xu=win.x+win.w*0.52, xd=win.x+win.w*0.70;
  for(let i=0;i<=n;i++){
    const zlo=zs[i], zhi=i<n?zs[i+1]:GH.TOP;
    const y0=mp.yOf(zlo), y1=mp.yOf(zhi), ym=(y0+y1)/2;
    if(y0-y1<16) continue;
    const U=S.Ul[i], D=S.Dl[i], Eg=Math.max(S.Ul[0],S.s.Eg,1e-9);
    ctx.beginPath(); ctx.moveTo(xu,y0-3); ctx.lineTo(xu,y1+7);
    ctx.strokeStyle=rgba(COL.pos,clamp(0.22+0.7*U/Eg,0,1)); ctx.lineWidth=3; ctx.stroke();
    arrowV(ctx,xu,y1+3,1,rgba(COL.pos,clamp(0.3+0.7*U/Eg,0,1)),6);
    lab(ctx,W,H,xu+9,ym,fmt(U,1),COL.pos,SM_FONT,'left');
    if(D>0.05){
      ctx.beginPath(); ctx.moveTo(xd,y1+3); ctx.lineTo(xd,y0-7);
      ctx.strokeStyle=rgba(COL.live,clamp(0.22+0.7*D/Eg,0,1)); ctx.lineWidth=3; ctx.stroke();
      arrowV(ctx,xd,y0-3,-1,rgba(COL.live,clamp(0.3+0.7*D/Eg,0,1)),6);
      lab(ctx,W,H,xd+9,ym,fmt(D,1),COL.live,SM_FONT,'left');
    }
  }
  /* the sheets' own temperatures */
  for(let i=0;i<n;i++){
    if(S.a[i]<=0) continue;
    const y=mp.yOf(S.alt[i]);
    const T=ST.kirch?S.Skirch[i]:S.Ssteady[i];
    const live=ST.kirch&&S.a[i]>0?S.A.th.T[i]*Math.pow(S.a[i],-0.25):S.A.th.T[i];
    lab(ctx,W,H,win.x+10,y-11,'sheet '+(i+1)+'  '+plain(tstr(live,M.unit,1)),
        '#dff3fa',SM_FONT,'left');
    if(Math.abs(live-T)>0.05)
      lab(ctx,W,H,win.x+10,y+11,'steady '+plain(tstr(T,M.unit,1)),rgba(COL.ref,0.95),SM_FONT,'left');
  }
  if(n>0&&S.A.nActive===0) lab(ctx,W,H,win.x+win.w/2,yGround-34,
      'no absorbing sheets: a bare rock','#aeb6c6',LAB_FONT,'center');
  drawProbe(ctx,W,H,M,L);
  drawAltAxis(ctx,W,H,L);
  if(ST.balance) drawBalance(ctx,W,H,M,L);
  drawThermometer(ctx,W,H,M,L);
  if(L.showFlux) drawFluxPanel(ctx,W,H,M,L);
  lab(ctx,W,H,win.x+6,mp.y0-5,'flux in W/m² · vertical scale ×'+fmt(L.exag,2),
      '#8b93a6',SM_FONT,'left','bottom');
  caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}
