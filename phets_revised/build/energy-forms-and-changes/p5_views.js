
/* ================================================================== *
 *  the analysis views: the heat ledger, the energy flow, equilibrium; *
 *  drawView() and makeScene()                                         *
 * ================================================================== */
/* stageLayout, falling back to no bottom row when the main panel would be
   squeezed below its 80-px floor (the helper clamps it there and the rows
   then overlap: the 560 x 380 sweep found it) */
/* the caption must describe the panels actually drawn (Known-bad: a narrow
   caption described a panel the narrow layout did not draw): caps carries one
   caption per layout -- full (every panel), two (main + one), solo (main only)
   -- and a short one that names no panel */
function layoutFit(ctx,W,H,caps,nB,frac,nBN){
  const pick=n=>n>=nB?caps.full:(n>0?caps.two:caps.solo);
  let n=isNarrow(W)?nBN:nB;
  let L=stageLayout(ctx,W,H,pick(n),caps.short,n,frac,n);
  const want=L.bottom.length?L.capY-16-(stageTop()+30)-Math.max(90,Math.floor((L.capY-16-(stageTop()+30))*frac))-56:L.main.h;
  if(L.bottom.length&&want<100){
    L=stageLayout(ctx,W,H,pick(0),caps.short,0,frac,0);
    /* with no bottom row the helper runs the panel to 16 px above the caption:
       leave the 34 px its tick labels and axis title hang below it */
    L.main=box(L.main.x,L.main.y,L.main.w,Math.max(60,L.main.h-34));
    L.solo=true;
  }
  reserveCaption(L.left,L.capY,L.capTxt,L.capW,ctx);
  return L;
}
function reserveCaption(x,y,txt,w,ctx){ const n=wrapText(ctx,txt,w,CAP_FONT).length; LABELS.push([x,y,x+w,y+n*14]); }
/* a legend only where it fits, and its box registered so later labels avoid it */
function legendFit(ctx,b,items){
  const r=b.h>items.length*15+30&&b.w>120?legendAuto(ctx,b,items):null;
  if(r) LABELS.push([r.x,r.y,r.x1,r.y1]);
  return r;
}
function rangeOf(arrs,pad){
  let lo=Infinity, hi=-Infinity;
  for(const a of arrs) for(const v of a) if(isFinite(v)){ if(v<lo) lo=v; if(v>hi) hi=v; }
  if(!isFinite(lo)){ lo=0; hi=1; }
  if(hi-lo<1e-9){ const m=Math.max(Math.abs(hi),1)*0.05; lo-=m; hi+=m; }
  const p=(hi-lo)*(pad===undefined?0.08:pad); return [lo-p,hi+p];
}
/* ---------------- the heat ledger ---------------- */
const LEDGER_CAPS={
  full:'The bench, recorded since its start (pick a preset or drive a burner on the bench). Top: every body’s temperature. '
    +'Left: the first law as three accounts — what the burners did (orange halo), what the bodies gained (green) and what the room took (cyan); '
    +'gained + took (thin green, on the halo) is the burners’ work to the last digit. Right: each body’s chunks (magenta) against PhET’s map g(E) (green bar): never a whole chunk apart.',
  two:'The bench, recorded since its start (pick a preset or drive a burner on the bench). Top: every body’s temperature. '
    +'Below: the first law as three accounts — what the burners did (orange halo), what the bodies gained (green) and what the room took (cyan); '
    +'gained + took (thin green, on the halo) is the burners’ work to the last digit.',
  solo:'The first law for the bench since its start: what the burners did (orange halo) is what the bodies gained (green) plus what the room took (cyan), to the last digit.',
  short:'The bench since its start: the burners’ work equals what the bodies gained plus what the room took.'};
function ledgerGeo(ctx,W,H){ return layoutFit(ctx,W,H-HINT_H,LEDGER_CAPS,2,0.52,1); }
function drawLedger(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  const L=ledgerGeo(ctx,W,H), B=M.B, Hh=B.hist, t=Hh.t, n=t.length;
  const tmax=Math.max(10,n?t[n-1]:0);
  if(L.solo){ drawLedgerAccounts(ctx,L.main,B,Hh,t,tmax); drawCaption(ctx,L); return L; }
  /* temperatures */
  const mb=L.main, Tr=rangeOf(Hh.T.map(a=>a.map(kelvinC)),0.1);
  axesR(ctx,mb,0,tmax,Tr[0],Tr[1],{title:titleFor(mb,'temperatures on the bench, °C, against time, s','temperatures, °C'),xlab:'t, s',xfmt:tickFmt(0,tmax,6),ylab:'°C',ny:4,
    yfmt:v=>fmt(v,Math.abs(Tr[1]-Tr[0])<5?1:0)});
  const idle=Hh.T.every(a=>a.every(v=>Math.abs(v-a[0])<1e-9));
  for(let i=0;i<4;i++) polyline(ctx,mb,t,Hh.T[i].map(kelvinC),0,tmax,Tr[0],Tr[1],COL.body[B.bodies[i].mat],1.8);
  if(idle) lab(ctx,W,H,mb.x+14,mb.y+18,'nothing has happened yet: everything sits at 296 K, the room’s temperature','#8b93a6',LAB_FONT,'left','middle');
  legendFit(ctx,mb,B.bodies.map(b=>[COL.body[b.mat],MAT_NAME[b.mat]]));
  if(L.bottom.length) drawLedgerAccounts(ctx,L.bottom[0],B,Hh,t,tmax);
  if(L.bottom.length>1){
    /* chunks against g(E) */
    const cb=L.bottom[1], gmax=Math.max(8,...M.g.map(v=>v+1),...M.own.map(v=>v+1));
    axesR(ctx,cb,0,4,0,gmax,{title:titleFor(cb,'chunks held (●) and PhET’s map g(E)','chunks and g(E)'),xticks:[],ny:4,yfmt:v=>fmt(v,0)});
    for(let i=0;i<4;i++){
      const X=cb.x+cb.w*(i+0.5)/4, Y=v=>cb.y1-cb.h*v/gmax, bw=Math.max(6,cb.w/14);
      ctx.fillStyle=rgba(COL.pos,0.8); ctx.fillRect(X-bw/2,Y(M.g[i]),bw,cb.y1-Y(M.g[i]));
      dot(ctx,X,Y(M.own[i]),4.5,COL.live,'#fff',1);
      lab(ctx,W,H,X,cb.y1+10,MAT_NAME[B.bodies[i].mat],'#8b93a6',SM_FONT,'center','middle');
    }
  }
  drawCaption(ctx,L);
  return L;
}
/* the three accounts, kJ: what the burners did (a halo), what the bodies
   gained, what the room took, and gained + took drawn thin on the halo */
function drawLedgerAccounts(ctx,eb,B,Hh,t,tmax){
  const dE=t.map((_,k)=>Hh.E.reduce((s,a,i)=>s+a[k]-B.E0[i],0)/1e3), room=Hh.room.map(v=>v/1e3), work=Hh.work.map(v=>v/1e3);
  const sum=dE.map((v,k)=>v+room[k]), Er=rangeOf([dE,room,work],0.1);
  axesR(ctx,eb,0,tmax,Er[0],Er[1],{title:titleFor(eb,'the ledger, kJ: gained + took = done','the ledger, kJ'),xlab:'t, s',xfmt:tickFmt(0,tmax,6),ylab:'kJ',ny:4,yfmt:tickFmt(Er[0],Er[1],4)});
  polyline(ctx,eb,t,work,0,tmax,Er[0],Er[1],rgba(COL.acct.work,0.55),6);
  polyline(ctx,eb,t,dE,0,tmax,Er[0],Er[1],COL.acct.bodies,1.6);
  polyline(ctx,eb,t,room,0,tmax,Er[0],Er[1],COL.acct.room,1.6);
  polyline(ctx,eb,t,sum,0,tmax,Er[0],Er[1],'#e9f7c9',1);
  legendFit(ctx,eb,[[COL.acct.work,'burners did'],[COL.acct.bodies,'bodies gained'],[COL.acct.room,'room took']]);
}
/* ---------------- the energy flow: a Sankey of the chain ---------------- */
const FLOW_CAPS={
  full:'The chain as a Sankey diagram, drawn to scale in power: every band’s width is its watts, and at each element the bands out (to the next element, to a store, as heat) add up to the bands in. '
    +'Below: the ledger since the chain began — IN (orange halo) is OUT + LOST + STORED (thin green) to the last digit.',
  solo:'The chain as a Sankey diagram, drawn to scale in power: every band’s width is its watts, and at each element the bands out (to the next element, to a store, as heat) add up to the bands in.',
  short:'The chain drawn to scale in power: at every element the bands out add up to the band in.'};
FLOW_CAPS.two=FLOW_CAPS.full;
function flowGeo(ctx,W,H){ return layoutFit(ctx,W,H-HINT_H,FLOW_CAPS,1,0.36,1); }
function band(ctx,x0,y0a,y0b,x1,y1a,y1b,col){
  const N=18; ctx.beginPath();
  for(let k=0;k<=N;k++){ const u=k/N, s=smoothstep(u), x=x0+(x1-x0)*u, y=y0a+(y1a-y0a)*s; if(k===0) ctx.moveTo(x,y); else ctx.lineTo(x,y); }
  for(let k=N;k>=0;k--){ const u=k/N, s=smoothstep(u), x=x0+(x1-x0)*u, y=y0b+(y1b-y0b)*s; ctx.lineTo(x,y); }
  ctx.closePath(); ctx.fillStyle=col; ctx.fill();
}
function flowModel(M){
  const S=M.S, F=M.F, sf=S.src==='sun'?'light':(S.src==='biker'?'chemical':(S.src==='teapot'?'thermal':'mechanical'));
  const outForm=srcForm(S.src), lossForm=S.src==='sun'?'light':'thermal';
  const uOutForm=S.user==='fan'?'mechanical':(S.user==='heater'?'thermal':'light');
  return {sf,outForm,lossForm,uOutForm};
}
function drawFlow(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  const L=flowGeo(ctx,W,H), S=M.S, F=M.F, fm=flowModel(M), mb=L.main;
  frame(ctx,mb,'#242a3a');
  ctx.textAlign='left'; ctx.textBaseline='bottom'; ctx.fillStyle='#aeb6c6'; ctx.font='italic 13px Georgia, serif';
  const title=titleFor(mb,'the chain now, to scale in power (W)','the chain now, W'); ctx.fillText(plain(title),mb.x,mb.y-9);
  LABELS.push([mb.x,mb.y-9-13*1.15,mb.x+plain(title).length*13*0.52,mb.y-9]);
  const pmax=Math.max(MAXP,F.srcIn,1), scale=(mb.h*0.46)/pmax;
  const xs=[mb.x+mb.w*0.14,mb.x+mb.w*0.42,mb.x+mb.w*0.70,mb.x+mb.w*0.94], yc=mb.y+mb.h*0.42, nw=10;
  const names=[srcName(S.src),convName(S.conv),userName(S.user)];
  const hIn=F.srcIn*scale, flows=[];
  /* supply into the source */
  band(ctx,mb.x+8,yc-hIn/2,yc+hIn/2,xs[0],yc-hIn/2,yc+hIn/2,rgba(COL.form[fm.sf],0.55));
  if(F.srcIn>0) lab(ctx,W,H,mb.x+12,yc+hIn/2+10,fmtW(F.srcIn)+(S.src==='biker'?' of food burned':' in'),'#e9edf5',SM_FONT,'left','middle');
  /* one element: in at its left, out = [main, store, loss] stacked at its right */
  function node(ix,inW,mainW,storeW,lossW,mainCol,lossCol,lossName){
    const x=xs[ix], h=Math.max(inW,mainW+Math.max(storeW,0)+lossW)*scale, y0=yc-h/2;
    ctx.fillStyle='#cfd4de'; ctx.fillRect(x-nw/2,y0,nw,Math.max(h,2));
    lab(ctx,W,H,x,y0-12,names[ix]||'','#aeb6c6',SM_FONT,'center','middle');
    let y=y0; const main=[y,y+mainW*scale]; y+=mainW*scale;
    if(storeW>0){ const st=[y,y+storeW*scale]; y+=storeW*scale; band(ctx,x+nw/2,st[0],st[1],x+34,st[0]+14,st[1]+14,rgba(COL.struct,0.55));
      if(storeW>0.01*pmax) lab(ctx,W,H,x+38,st[1]+16,'store +'+fmtW(storeW),COL.struct,SM_FONT,'left','middle'); }
    if(lossW>0){ const ls=[y,y+lossW*scale]; band(ctx,x+nw/2,ls[0],ls[1],x+46,mb.y1-6-(ls[1]-ls[0]),mb.y1-6,rgba(COL.form[lossCol],0.5));
      lab(ctx,W,H,x+48,mb.y1-14-(ls[1]-ls[0]),lossName+' '+fmtW(lossW),rgba(COL.form[lossCol],1),SM_FONT,'left','middle'); }
    if(storeW<-0.01*pmax) lab(ctx,W,H,x-nw,y0+h+10,'from its store '+fmtW(-storeW),COL.struct,SM_FONT,'right','middle');
    return main;
  }
  const s0=node(0,F.srcIn,F.srcOut,F.srcStore,F.srcLoss,fm.outForm,fm.lossForm,S.src==='sun'?'clouds send back':'heat');
  const c0=[yc-F.cIn*scale/2,yc+F.cIn*scale/2];
  band(ctx,xs[0]+nw/2,s0[0],s0[1],xs[1]-nw/2,c0[0],c0[1],rgba(COL.form[fm.outForm],0.55));
  if(F.srcOut>0) lab(ctx,W,H,(xs[0]+xs[1])/2,Math.min(s0[0],c0[0])-10,fmtW(F.srcOut)+' '+fm.outForm,'#e9edf5',SM_FONT,'center','middle');
  const c1=node(1,F.cIn,F.cOut,F.cStore,F.cLoss+F.cMiss,'electrical',F.cMiss>0?fm.outForm:'thermal',F.cMiss>0?'cannot use':'heat');
  const u0=[yc-F.uIn*scale/2,yc+F.uIn*scale/2];
  band(ctx,xs[1]+nw/2,c1[0],c1[1],xs[2]-nw/2,u0[0],u0[1],rgba(COL.form.electrical,0.55));
  if(F.cOut>0) lab(ctx,W,H,(xs[1]+xs[2])/2,Math.min(c1[0],u0[0])-10,fmtW(F.cOut)+' electrical','#e9edf5',SM_FONT,'center','middle');
  const uMain=S.user==='heater'?F.water:F.uOut;
  const u1=node(2,F.uIn,S.user==='heater'?0:F.uOut,S.user==='heater'?F.uStore:0,S.user==='heater'?F.coilLoss+F.waterLoss:F.uLoss,fm.uOutForm,'thermal','heat');
  if(S.user!=='heater'){ band(ctx,xs[2]+nw/2,u1[0],u1[1],xs[3],u1[0],u1[1],rgba(COL.form[fm.uOutForm],0.6));
    if(F.uOut>0) lab(ctx,W,H,xs[3]-4,u1[0]-10,fmtW(F.uOut)+' '+(S.user==='fan'?'wind':'light'),'#e9edf5',SM_FONT,'right','middle'); }
  else if(uMain>0) lab(ctx,W,H,xs[2]+12,yc-F.uIn*scale/2-24,fmtW(F.water)+' into the water','#e9edf5',SM_FONT,'left','middle');
  if(F.srcIn<=0&&F.cIn<=0&&F.uIn<=0) lab(ctx,W,H,mb.x+mb.w/2,mb.y+mb.h*0.2,'no power flows now: set the source going (the panel, or the systems view)','#8b93a6',LAB_FONT,'center','middle');
  if(L.bottom.length){
    const eb=L.bottom[0], H2=S.hist, t=H2.t, tmax=Math.max(10,t.length?t[t.length-1]:0);
    const kin=H2.sup.map(v=>v/1e3), kout=H2.use.map(v=>v/1e3), kl=H2.loss.map(v=>v/1e3), ks=H2.store.map(v=>v/1e3);
    const sum=kout.map((v,k)=>v+kl[k]+ks[k]), R=rangeOf([kin,kout,kl,ks],0.1);
    axesR(ctx,eb,0,tmax,R[0],R[1],{title:titleFor(eb,'the ledger since the chain began, kJ','the ledger, kJ'),xlab:'t, s',xfmt:tickFmt(0,tmax,6),ylab:'kJ',ny:3,yfmt:tickFmt(R[0],R[1],3)});
    polyline(ctx,eb,t,kin,0,tmax,R[0],R[1],rgba(COL.ref,0.55),6);
    polyline(ctx,eb,t,kout,0,tmax,R[0],R[1],COL.form.light,1.4);
    polyline(ctx,eb,t,kl,0,tmax,R[0],R[1],COL.form.thermal,1.4);
    polyline(ctx,eb,t,ks,0,tmax,R[0],R[1],COL.struct,1.4);
    polyline(ctx,eb,t,sum,0,tmax,R[0],R[1],COL.pos,1);
    legendFit(ctx,eb,[[COL.ref,'IN'],[COL.form.light,'OUT'],[COL.form.thermal,'LOST'],[COL.struct,'STORED']]);
  }
  drawCaption(ctx,L);
  return L;
}
/* ---------------- equilibrium ---------------- */
const EQ_TOP='Top: PhET’s stepped model (solid, in each body’s colour) over the exact solution of the linear pair-and-room system (orange halo); the dashed orange line is T_eq = (C₁T₁ + C₂T₂)/(C₁ + C₂).';
const EQ_CAPS={
  full:EQ_TOP+' Bottom left: the steps minus the exact solution in millikelvin — magnified 1000× against the top panel — the price of PhET’s explicit 1/60-s step. Bottom right: the two heat capacities, PhET’s against the real materials.',
  two:EQ_TOP+' Below: the steps minus the exact solution in millikelvin — magnified 1000× against the top panel — the price of PhET’s explicit 1/60-s step.',
  solo:'PhET’s stepped model (solid, in each body’s colour) over the exact solution of the linear pair-and-room system (orange halo); the dashed orange line is T_eq = (C₁T₁ + C₂T₂)/(C₁ + C₂).',
  short:'PhET’s steps (solid) over the exact solution (orange halo); dashed: T_eq.'};
function eqGeo(ctx,W,H){ return layoutFit(ctx,W,H-HINT_H,EQ_CAPS,2,0.4,1); }
function drawEq(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  const Lg=eqGeo(ctx,W,H), R=M.R, L=M.L, st=M.st, P=eqPair(st.eqPair), mb=Lg.main;
  const n1=MAT_NAME[BODY_DEF[P.b1][0]], n2=MAT_NAME[BODY_DEF[P.b2][0]];
  const t=R.t, tmax=t[t.length-1], cut=R.tCap===null?tmax:R.tCap;
  const live=k=>R.tCap===null||t[k]<R.tCap;
  const s1=R.s1.map(kelvinC), s2=R.s2.map(kelvinC), x1=R.x1.map((v,k)=>live(k)?kelvinC(v):NaN), x2=R.x2.map((v,k)=>live(k)?kelvinC(v):NaN);
  const Tr=rangeOf([s1,s2,[kelvinC(L.Teq)],st.eqAir?[kelvinC(T_AIR)]:[]],0.08);
  axesR(ctx,mb,0,tmax,Tr[0],Tr[1],{title:titleFor(mb,P.name+': the two temperatures, °C, against time, s',P.name+', °C'),xlab:'t, s',xfmt:tickFmt(0,tmax,6),ylab:'°C',ny:4,yfmt:v=>fmt(v,0)});
  polyline(ctx,mb,t,x1,0,tmax,Tr[0],Tr[1],rgba(COL.ref,0.5),6);
  polyline(ctx,mb,t,x2,0,tmax,Tr[0],Tr[1],rgba(COL.ref,0.5),6);
  polyline(ctx,mb,[0,tmax],[kelvinC(L.Teq),kelvinC(L.Teq)],0,tmax,Tr[0],Tr[1],COL.ref,1.2,[6,4]);
  if(st.eqAir) polyline(ctx,mb,[0,tmax],[kelvinC(T_AIR),kelvinC(T_AIR)],0,tmax,Tr[0],Tr[1],rgba(COL.struct,0.7),1,[2,4]);
  polyline(ctx,mb,t,s1,0,tmax,Tr[0],Tr[1],COL.body[BODY_DEF[P.b1][0]],1.8);
  polyline(ctx,mb,t,s2,0,tmax,Tr[0],Tr[1],COL.body[BODY_DEF[P.b2][0]],1.8);
  legendFit(ctx,mb,[[COL.body[BODY_DEF[P.b1][0]],n1+' (PhET’s steps)'],[COL.body[BODY_DEF[P.b2][0]],n2+' (PhET’s steps)'],[COL.ref,'exact; T_eq dashed']]);
  if(R.tCap!==null){ const X=mb.x+mb.w*R.tCap/tmax; ctx.fillStyle=rgba(COL.ref,0.08); ctx.fillRect(X,mb.y,mb.x1-X,mb.h);
    const capTxt=mb.w>520?'a cap is reached at '+fmt(R.tCap,2)+' s: past it the linear solution does not apply':'a cap at '+fmt(R.tCap,2)+' s';
    lab(ctx,W,H,Math.min(X+6,mb.x1-capTxt.length*10.5*0.52-4),mb.y1-14,capTxt,COL.ref,SM_FONT,'left','middle'); }
  if(Lg.bottom.length){
    const gb=Lg.bottom[0], d1=[], d2=[];
    for(let k=0;k<t.length;k++){ const ok=live(k); d1.push(ok?(R.s1[k]-R.x1[k])*1000:NaN); d2.push(ok?(R.s2[k]-R.x2[k])*1000:NaN); }
    const Dr=rangeOf([d1.filter(isFinite),d2.filter(isFinite)],0.12);
    axesR(ctx,gb,0,tmax,Dr[0],Dr[1],{title:titleFor(gb,'steps minus exact, mK (×1000)','steps − exact, mK'),xlab:'t, s',xfmt:tickFmt(0,tmax,6),ny:4,yfmt:tickFmt(Dr[0],Dr[1],4)});
    polyline(ctx,gb,t,d1,0,tmax,Dr[0],Dr[1],COL.body[BODY_DEF[P.b1][0]],1.5);
    polyline(ctx,gb,t,d2,0,tmax,Dr[0],Dr[1],COL.body[BODY_DEF[P.b2][0]],1.5);
  }
  if(Lg.bottom.length>1){
    const cb=Lg.bottom[1], Lp=eqLinear(st.eqPair,st.eqT1,st.eqT2,'phet',st.eqAir), Lr=eqLinear(st.eqPair,st.eqT1,st.eqT2,'real',st.eqAir);
    const cmax=Math.max(Lp.C1,Lp.C2,Lr.C1,Lr.C2)*1.15;
    axesR(ctx,cb,0,2,0,cmax,{title:titleFor(cb,'heat capacity C, J/K: PhET’s and real','C, J/K'),xticks:[],ny:4,yfmt:v=>fmt(v,0)});
    [[Lp.C1,Lr.C1,n1],[Lp.C2,Lr.C2,n2]].forEach((c,i)=>{
      const X=cb.x+cb.w*(i+0.5)/2, bw=Math.max(8,cb.w/9), Y=v=>cb.y1-cb.h*v/cmax;
      ctx.fillStyle=rgba(COL.pos,0.85); ctx.fillRect(X-bw-2,Y(c[0]),bw,cb.y1-Y(c[0]));
      ctx.fillStyle=rgba(COL.ref,0.85); ctx.fillRect(X+2,Y(c[1]),bw,cb.y1-Y(c[1]));
      lab(ctx,W,H,X,cb.y1+10,c[2],'#8b93a6',SM_FONT,'center','middle');
    });
    legendFit(ctx,cb,[[COL.pos,'PhET'],[COL.ref,'real']]);
  }
  drawCaption(ctx,Lg);
  return Lg;
}

/* ---------------- dispatch and the scene ---------------- */
function drawView(ctx,W,H,M){
  ctx.clearRect(0,0,W,H);
  if(M.view==='bench') return drawBench(ctx,W,H,M);
  if(M.view==='sys') return drawSystems(ctx,W,H,M);
  if(M.view==='ledger') return drawLedger(ctx,W,H,M);
  if(M.view==='flow') return drawFlow(ctx,W,H,M);
  return drawEq(ctx,W,H,M);
}
function viewModel(){ const M=buildModel(); M.dragLever=DRAG.what==='lever'?DRAG.k:null; M.dragThermo=DRAG.what==='therm'?DRAG.k:null; return M; }
function makeScene(canvas){
  const S={st:ST,W:1400,H:820,geo:null};
  S.model=()=>viewModel();
  S.draw=()=>{ const ctx=canvas.getContext('2d'); S.geo=drawView(ctx,S.W,S.H,S.model()); return S.geo; };
  S.step=dtw=>{
    if(!ST.running) return false;
    if(ST.view==='bench'||ST.view==='ledger') return benchAdvance(BENCH,ST,dtw)>0;
    if(ST.view==='sys'||ST.view==='flow') return sysAdvance(SYS,ST,dtw)>0;
    return false;
  };
  /* the bench's pointer: a burner's lever, a thermometer, a body (and whatever
     sits on it); every other view ignores the pointer */
  S.pointer=(kind,px,py)=>{
    if(ST.view!=='bench') return false;
    if(!S.geo||!S.geo.map) S.draw();
    const map=S.geo.map, wx=map.wx(px), wy=map.wy(py), B=BENCH;
    if(kind==='down'){
      for(let k=0;k<2;k++){ const l=burnerLevels(ST)[k], kn=leverPos(k,l);
        if(Math.abs(px-map.X(kn.x))<=12&&Math.abs(py-map.Y(kn.y))<=9){ DRAG.what='lever'; DRAG.k=k; return true; } }
      const tk=thermoPick(B,wx,wy);
      if(tk>=0){ const p=thermoTip(B,B.therm[tk]); DRAG.what='therm'; DRAG.k=tk; DRAG.off=[p.x-wx,p.y-wy];
        const th=B.therm[tk]; th.att=null; th.x=p.x; th.y=p.y; th.tray=false; return true; }
      const i=benchPick(B,wx,wy);
      if(i>=0&&benchGrab(B,i,wx,wy)){ DRAG.what='body'; DRAG.k=i; return true; }
      return false;
    }
    if(kind==='move'){
      if(DRAG.what==='lever'){ const l=leverLevel(wy);
        if(ST.link){ ST.lev0=l; ST.lev1=l; } else if(DRAG.k===0) ST.lev0=l; else ST.lev1=l; return true; }
      if(DRAG.what==='therm'){ const th=B.therm[DRAG.k]; th.x=clamp(wx+DRAG.off[0],BENCH_EXT.xmin,BENCH_EXT.xmax); th.y=clamp(wy+DRAG.off[1],BENCH_EXT.ymin,BENCH_EXT.ymax-THERMO_H); return true; }
      if(DRAG.what==='body'){ benchMoveHeld(B,wx,wy); return true; }
      return false;
    }
    if(kind==='up'){
      const was=DRAG.what;
      if(was==='therm') thermoDrop(B,DRAG.k);
      if(was==='body') benchDrop(B);
      DRAG.what=null; DRAG.k=null;
      return was!==null;
    }
    return false;
  };
  return S;
}
