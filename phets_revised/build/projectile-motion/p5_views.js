
/* ================================================================== *
 *  the analysis views: the envelope and the hodograph                  *
 * ================================================================== */
/* stageLayout — buoyancy.html p4 (lineage build_cycloid): the caption is
   measured first and the panels get what is left; the main panel stops
   short of the floating readout */
function stageLayout(ctx,W,H,capFull,capShort,nBottom,bottomFrac,nBottomNarrow){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+30;
  const fit=fitCaption(ctx,W,H,capFull,capShort,capW,top+220);
  const avail=fit.capY-16-top;
  const nB=narrow?(nBottomNarrow===undefined?1:nBottomNarrow):nBottom;
  const out={narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,bottom:[]};
  let mainH=avail;
  if(nB>0){
    const rowH=Math.max(90,Math.floor(avail*bottomFrac));
    mainH=avail-rowH-56;
    const gut=52, span=right-left, w=(span-gut*nB)/nB;
    for(let i=0;i<nB;i++) out.bottom.push(box(left+gut+i*(w+gut),fit.capY-16-rowH+10,w,rowH-34));
  }
  out.main=box(left,top,right-left,Math.max(80,mainH));
  return out;
}
/* a sub-box of b with ONE scale on both axes (the thing drawn is a shape) */
function equalBox(b,xlo,xhi,ylo,yhi){
  const s=Math.min(b.w/(xhi-xlo),b.h/(yhi-ylo)), w=s*(xhi-xlo), hh=s*(yhi-ylo);
  return {bb:box(b.x+(b.w-w)/2,b.y+(b.h-hh)/2,w,hh),s};
}
function marker(ctx,b,xlo,xhi,ylo,yhi,x,y,col,r){
  const X=b.x+b.w*(x-xlo)/(xhi-xlo), Y=b.y1-b.h*(y-ylo)/(yhi-ylo);
  if(X<b.x-0.5||X>b.x1+0.5||Y<b.y-0.5||Y>b.y1+0.5) return null;
  dot(ctx,X,Y,r||4.5,col,'#fff',1);
  return [X,Y];
}
function flightXY(F,i1){ const xs=[], ys=[], n=Math.min(F.t.length-1,i1===undefined?F.t.length-1:i1), st=Math.max(1,Math.ceil(n/700));
  for(let i=0;i<=n;i+=st){ xs.push(F.x[i]); ys.push(F.y[i]); } if(n%st){ xs.push(F.x[n]); ys.push(F.y[n]); } return {xs,ys}; }

function drawEnv(ctx,W,H,M){
  const Q=M.Env, L=Q.L, E=Q.E, air=E.air, st=ST;
  if(!(L.v0>=0.5)){ const Lz=stageLayout(ctx,W,H,'','',0,0,0);
    lab(ctx,W,H,Lz.left,Lz.main.y+30,'No fan: at an initial speed of '+fmt(L.v0,1)+' m/s every shot just drops from '+fmt(L.h,1)+' m.',COL.dim,LAB_FONT); return; }
  const xmax=Math.max(Q.vopt.R,Q.Rs.reduce((a,b)=>Math.max(a,b),0))*1.05, ymax=Q.Hmax*1.08;
  const capFull='The fan: the same projectile fired every '+FAN_STEP+'° from 0° to 90° at '+fmt(L.v0,1)+' m/s from '+fmt(L.h,1)+' m. '
    +(air?'Faint orange: the shots in vacuum; green: with the air. ':'Every shot is in vacuum (air off). ')
    +'Orange dashed: the parabola of safety y = h + v0²/2g − gx²/2v0², which no vacuum shot crosses; the shots steeper than the best angle touch it once before they land, the flatter ones land first. '
    +'Bold green: the best angle'+(air?' with the air':'')+', '+fmt(Q.opt.th,2)+'°; magenta: your angle, '+fmt(L.th,0)+'°. Both axes of the fan share one scale. Below: the range against the angle.';
  const Ly=stageLayout(ctx,W,H,capFull,'The fan of shots at one speed, the vacuum envelope (dashed), and the range against the angle.',1,0.36,1);
  const EB=equalBox(Ly.main,0,xmax,0,ymax), bb=EB.bb;
  axesR(ctx,bb,0,xmax,0,ymax,{title:titleFor(bb,'every shot at '+fmt(L.v0,1)+' m/s, and the envelope that bounds them','the fan'),xlab:'x (m)',ylab:'y (m)',nx:6,ny:4});
  for(const f of Q.fan){
    if(!air||st.e_vac){ const VP=vacuumPath(L.h,f.th,L.v0,E.g,90); polyline(ctx,bb,VP.xs,VP.ys,0,xmax,0,ymax,air?rgba(COL.ref,0.45):COL.ref,air?1:1.3); }
    if(air&&f.F){ const P=flightXY(f.F); polyline(ctx,bb,P.xs,P.ys,0,xmax,0,ymax,rgba(COL.pos,0.75),1.2); }
  }
  { const xs=[], ys=[]; for(let i=0;i<=160;i++){ const x=Q.vopt.R*i/160; xs.push(x); ys.push(envelopeY(x,L.h,L.v0,E.g)); }
    polyline(ctx,bb,xs,ys,0,xmax,0,ymax,COL.ref,1.8,[7,5]); }
  { if(Q.best){ const P=flightXY(Q.best); polyline(ctx,bb,P.xs,P.ys,0,xmax,0,ymax,COL.pos,2.6); }
    else { const VP=vacuumPath(L.h,Q.opt.th,L.v0,E.g,120); polyline(ctx,bb,VP.xs,VP.ys,0,xmax,0,ymax,COL.pos,2.6); } }
  if(air){ const P=flightXY(Q.cur.F); polyline(ctx,bb,P.xs,P.ys,0,xmax,0,ymax,COL.live,1.8); }
  else { const VP=vacuumPath(L.h,L.th,L.v0,E.g,120); polyline(ctx,bb,VP.xs,VP.ys,0,xmax,0,ymax,COL.live,1.8); }
  legendAuto(ctx,bb,air?[[COL.pos,'with the air'],[COL.ref,'vacuum, and its envelope'],[COL.live,'your angle']]:[[COL.ref,'vacuum shots, envelope'],[COL.pos,'the best angle'],[COL.live,'your angle']]);
  if(Ly.bottom.length){
    const b=Ly.bottom[0], Rmax=Q.vopt.R*1.1;
    axesR(ctx,b,0,90,0,Rmax,{title:titleFor(b,'the range against the launch angle: the best angle falls below 45° with air, or from a height','range vs angle'),xlab:'launch angle (degrees)',ylab:'range (m)',nx:9,ny:4});
    const ths=[], rv=[]; for(let a=0;a<=90;a+=1){ ths.push(a); rv.push(vacuum(L.h,a,L.v0,E.g).R); }
    polyline(ctx,b,ths,rv,0,90,0,Rmax,COL.ref,1.6);
    if(air) polyline(ctx,b,Q.ths,Q.Rs,0,90,0,Rmax,COL.pos,1.8);
    const mv=marker(ctx,b,0,90,0,Rmax,Q.vopt.th,Q.vopt.R,COL.ref);
    if(mv) lab(ctx,W,H,mv[0]+8,mv[1]-10,'vacuum best '+fmt(Q.vopt.th,1)+'°',COL.ref,SM_FONT);
    if(air){ const mo=marker(ctx,b,0,90,0,Rmax,Q.opt.th,Q.opt.R,COL.pos); if(mo) lab(ctx,W,H,mo[0]-8,mo[1]+14,'with air '+fmt(Q.opt.th,1)+'°',COL.pos,SM_FONT,'right'); }
    marker(ctx,b,0,90,0,Rmax,clamp(L.th,0,90),Q.Rcur,COL.live,4);
  }
  caption(ctx,Ly.left,Ly.capY,Ly.capTxt,Ly.capW,'#767e92',CAP_FONT);
}

/* the hodograph's layout: the velocity plane is a SHAPE (one scale on both
   axes) and tall, so it takes the full height on the left and the two time
   plots stack on the right, clear of the readout; a narrow stage keeps the
   plane and the speed below it */
function hodoLayout(ctx,W,H,capFull,capShort){
  if(isNarrow(W)) return stageLayout(ctx,W,H,capFull,capShort,1,0.36,1);
  const left=56, right=W-RO_W-44, top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H,capFull,capShort,capW,top+300);
  const bot=fit.capY-44, span=right-left, wMain=Math.floor(0.46*span);
  const rx=left+wMain+76, rw=right-rx, gap=70, hh=(bot-top-gap)/2;
  return {narrow:false,left,right,capY:fit.capY,capTxt:fit.txt,capW,main:box(left,top,wMain,bot-top),
          bottom:[box(rx,top,rw,hh),box(rx,top+hh+gap,rw,hh)]};
}
function drawHodo(ctx,W,H,M){
  const Q=M.Hodo, L=Q.L, E=Q.E, F=Q.F, C=Q.C, vt=Q.vt, th=L.th*DEG, air=E.air;
  const G2=C||F, n=G2.t.length, iL=F.landI;
  let vxmax=0, vymin=0, vymax=0;
  for(let i=0;i<n;i++){ vxmax=Math.max(vxmax,G2.vx[i]); vymin=Math.min(vymin,G2.vy[i]); vymax=Math.max(vymax,G2.vy[i]); }
  if(Q.reach) vymin=Math.min(vymin,-vt);
  const pad=0.08*Math.max(vxmax,vymax-vymin,1);
  let xlo=-pad, xhi=vxmax+pad, ylo=vymin-pad; const yhi=Math.max(vymax,0)+pad;
  /* one scale on both axes, but never a sliver: a vertical launch has vx = 0
     throughout and would get a window a few pixels wide (the layout sweep) */
  if(xhi-xlo<0.45*(yhi-ylo)) xhi=xlo+0.45*(yhi-ylo);
  if(yhi-ylo<0.3*(xhi-xlo)) ylo=yhi-0.3*(xhi-xlo);
  const capFull='The hodograph: the tip of the velocity vector (vx, vy) through the flight, both axes to the same scale. '
    +(air?'Green: RK4, bright to the landing'+(C?', dim where the shot flies on past the ground as if off a cliff':'')+'; orange dashed: the exact curve u(φ) of quadratic drag, which it must follow; it ends at (0, −v_t) = (0, −'+sigf(vt,3)+' m/s)'
         +(Q.reach?'':', out of reach here: the approach would take about 3v_t/g = '+sigf(3*vt/E.g,3)+' s')+'. Faint orange: the same shot in vacuum, a vertical line, because gravity changes only vy.'
         :'In vacuum it is a vertical line: gravity changes only vy, at g = '+sigf(E.g,4)+' m/s² per second. Switch the air on to bend it.')
    +' Below: the speed against time, and the energy per kilogram — kinetic plus potential, what the air has taken, and their sum, which must stay flat.';
  const Ly=hodoLayout(ctx,W,H,capFull,'The velocity through the flight; the speed; the energy ledger.');
  const EB=equalBox(Ly.main,xlo,xhi,ylo,yhi), bb=EB.bb;
  axesR(ctx,bb,xlo,xhi,ylo,yhi,{title:titleFor(bb,'the velocity (vx, vy) through the flight','the hodograph'),xlab:'vx (m/s)',ylab:'vy (m/s)',nx:5,ny:5});
  polyline(ctx,bb,[xlo,xhi],[0,0],xlo,xhi,ylo,yhi,'#39404f',1,[2,3]);
  polyline(ctx,bb,[0,0],[ylo,yhi],xlo,xhi,ylo,yhi,'#39404f',1,[2,3]);
  if(air){ const u0=L.v0*Math.cos(th), V=vacuum(L.h,L.th,L.v0,E.g);
    polyline(ctx,bb,[u0,u0],[L.v0*Math.sin(th),C?Math.min(V.vy,ylo):V.vy],xlo,xhi,ylo,yhi,rgba(COL.ref,0.4),1.2); }
  polyline(ctx,bb,Q.ex.map(p=>p[0]),Q.ex.map(p=>p[1]),xlo,xhi,ylo,yhi,COL.ref,1.8,[6,5]);
  { const a=[], b=[]; for(let i=0;i<=iL;i+=Math.max(1,Math.ceil(iL/600))){ a.push(F.vx[i]); b.push(F.vy[i]); } a.push(F.vx[iL]); b.push(F.vy[iL]);
    polyline(ctx,bb,a,b,xlo,xhi,ylo,yhi,COL.pos,2.2); }
  if(C){ const j0=C.landI, a=[], b=[]; const stp=Math.max(1,Math.ceil((C.t.length-j0)/600));
    for(let i=j0;i<C.t.length;i+=stp){ a.push(C.vx[i]); b.push(C.vy[i]); }
    polyline(ctx,bb,a,b,xlo,xhi,ylo,yhi,rgba(COL.pos,0.45),1.6); }
  const pL=marker(ctx,bb,xlo,xhi,ylo,yhi,F.vx[iL],F.vy[iL],COL.live);
  if(pL){ const O=[bb.x+bb.w*(0-xlo)/(xhi-xlo),bb.y1-bb.h*(0-ylo)/(yhi-ylo)];
    ctx.strokeStyle=rgba(COL.live,0.7); ctx.lineWidth=1; ctx.setLineDash([3,3]); ctx.beginPath(); ctx.moveTo(O[0],O[1]); ctx.lineTo(pL[0],pL[1]); ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,pL[0]+9,pL[1]+2,'lands: '+sigf(F.vL,3)+' m/s, '+fmt(F.angL,1)+'° down',COL.live,SM_FONT); }
  const p0=marker(ctx,bb,xlo,xhi,ylo,yhi,L.v0*Math.cos(th),L.v0*Math.sin(th),COL.struct,3.5);
  if(p0) lab(ctx,W,H,p0[0]+8,p0[1]-8,'launch',COL.struct,SM_FONT);
  if(Q.reach&&-vt>=ylo){ const pt=marker(ctx,bb,xlo,xhi,ylo,yhi,0,-vt,COL.ref,4); if(pt) lab(ctx,W,H,pt[0]+9,pt[1],'(0, −v_t)',COL.ref,SM_FONT); }
  else if(air) lab(ctx,W,H,bb.x+8,bb.y1-12,'v_t = '+sigf(vt,3)+' m/s: off this plot',COL.ref,SM_FONT);
  legendAuto(ctx,bb,air?[[COL.pos,'RK4'],[COL.ref,'exact hodograph'],[COL.live,'landing']]:[[COL.pos,'RK4'],[COL.ref,'exact: vx = const']]);
  const tEnd=G2.t[n-1];
  if(Ly.bottom.length>0){
    const b=Ly.bottom[0], sp=[], ts=[], stp=Math.max(1,Math.ceil(n/500));
    for(let i=0;i<n;i+=stp){ ts.push(G2.t[i]); sp.push(Math.sqrt(G2.vx[i]*G2.vx[i]+G2.vy[i]*G2.vy[i])); }
    const smax=Math.max(sp.reduce((a,c)=>Math.max(a,c),0),Q.reach?vt:0)*1.12||1;
    axesR(ctx,b,0,tEnd,0,smax,{title:titleFor(b,'the speed |v| against time','speed'),xlab:'t (s)',ylab:'m/s',nx:5,ny:4});
    if(isFinite(vt)&&vt<=smax) polyline(ctx,b,[0,tEnd],[vt,vt],0,tEnd,0,smax,COL.ref,1.2,[5,4]);
    const k1=ts.findIndex(t=>t>F.T);
    polyline(ctx,b,k1<0?ts:ts.slice(0,k1+1),k1<0?sp:sp.slice(0,k1+1),0,tEnd,0,smax,COL.pos,1.8);
    if(k1>0) polyline(ctx,b,ts.slice(k1),sp.slice(k1),0,tEnd,0,smax,rgba(COL.pos,0.45),1.4);
    marker(ctx,b,0,tEnd,0,smax,F.T,F.vL,COL.live,3.5);
  }
  if(Ly.bottom.length>1){
    const b=Ly.bottom[1], ts=[], ep=[], ww=[], sm=[], stp=Math.max(1,Math.ceil(n/500)), e0=Q.led.e0;
    for(let i=0;i<n;i+=stp){ const e=0.5*(G2.vx[i]*G2.vx[i]+G2.vy[i]*G2.vy[i])+E.g*G2.y[i]; ts.push(G2.t[i]); ep.push(e); ww.push(G2.w[i]); sm.push(e+G2.w[i]); }
    let lo=0, hi=e0; for(let i=0;i<ep.length;i++){ lo=Math.min(lo,ep[i]); hi=Math.max(hi,ep[i],ww[i]); }
    const pad2=0.08*(hi-lo||1);
    axesR(ctx,b,0,tEnd,lo-pad2,hi+pad2,{title:titleFor(b,'energy per kilogram: e_k + g y, the air’s share w, and their sum','energy per kg'),xlab:'t (s)',ylab:'J/kg',nx:5,ny:4});
    polyline(ctx,b,ts,sm,0,tEnd,lo-pad2,hi+pad2,COL.ref,1.6,[6,4]);
    polyline(ctx,b,ts,ep,0,tEnd,lo-pad2,hi+pad2,COL.pos,1.8);
    polyline(ctx,b,ts,ww,0,tEnd,lo-pad2,hi+pad2,COL.live,1.6);
    legendAuto(ctx,b,[[COL.pos,'e_k + g y'],[COL.live,'w, taken by the air'],[COL.ref,'the sum']]);
  }
  caption(ctx,Ly.left,Ly.capY,Ly.capTxt,Ly.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle=COL.sky; ctx.fillRect(0,0,W,H);
  if(isScene(M.view)) drawScene(ctx,W,H,M);
  else if(M.view==='env') drawEnv(ctx,W,H,M);
  else drawHodo(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of the current scene's clock (1/60 s, x 0.33 in slow motion);
     true when something was in the air, which is what makes the loop repaint */
  S.dt=function(){ return FRAME_DT*(ST.speed==='slow'?SLOW:1); };
  S.step=function(){
    if(!ST.running||!isScene(ST.view)) return false;
    return advance(ST.view,S.dt());
  };
  /* the pointer: in a scene, the probe, the tape's two ends, the target, the
     barrel (aim) and the pedestal (height), in that order; the analysis views
     take no pointer and no wheel */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const v=ST.view; if(!isScene(v)) return false;
    const ctx=canvas.getContext('2d'), M=buildModel(), G=sceneGeo(ctx,S.W,S.H,M), map=G.map, sc=SCN[v], p=PFX[v];
    const wx=map.wx(x), wy=map.wy(y), b=G.b;
    if(type==='down'){
      if(ST.probe&&Math.hypot(x-map.X(sc.probe.x),y-map.Y(sc.probe.y))<=14){ DRAG.what='probe'; DRAG.dx=wx-sc.probe.x; DRAG.dy=wy-sc.probe.y; return true; }
      if(ST.tape){ const T=sc.tape;
        if(Math.hypot(x-map.X(T.x1),y-map.Y(T.y1))<=11){ DRAG.what='tip'; DRAG.dx=wx-T.x1; DRAG.dy=wy-T.y1; return true; }
        if(Math.hypot(x-map.X(T.x0),y-map.Y(T.y0))<=11){ DRAG.what='base'; DRAG.dx=wx-T.x0; DRAG.dy=wy-T.y0; return true; } }
      const Xt=map.X(ST[p+'tgt']), hw=TARGET_W/2*map.s;
      if(x>=Xt-hw-4&&x<=Xt+hw+4&&y>=map.Y0-16&&y<=map.Y0+10){ DRAG.what='target'; DRAG.dx=wx-ST[p+'tgt']; return true; }
      const bx=G.muz[0]-G.piv[0], by=G.muz[1]-G.piv[1], u=((x-G.piv[0])*bx+(y-G.piv[1])*by)/(bx*bx+by*by);
      if(u>0.3&&u<=1.15&&Math.hypot(x-G.piv[0]-u*bx,y-G.piv[1]-u*by)<=G.wb/2+5){ DRAG.what='barrel'; return true; }
      const rp=Math.max(8,0.35*map.s)+6;
      if((Math.abs(x-G.piv[0])<=G.pedW/2+6&&y>=G.piv[1]-6&&y<=map.Y0+4)||Math.hypot(x-G.piv[0],y-G.piv[1])<=rp){
        DRAG.what='height'; DRAG.dy=wy-ST[p+'h']; return true; }
      return false;
    }
    if(type!=='move'||!DRAG.what) return false;
    const xa=map.wx(b.x), xb=map.wx(b.x1), yb=map.wy(b.y);
    if(DRAG.what==='barrel') ST[p+'th']=clamp(Math.round(Math.atan2(wy-ST[p+'h'],wx)*RAD),LIM.th[0],LIM.th[1]);
    else if(DRAG.what==='height') ST[p+'h']=clamp(Math.round((wy-DRAG.dy)*10)/10,LIM.h[0],LIM.h[1]);
    else if(DRAG.what==='target') ST[p+'tgt']=clamp(Math.round((wx-DRAG.dx)*10)/10,0,Math.max(1,Math.floor(xb-2)));
    else if(DRAG.what==='probe'){ sc.probe.x=clamp(wx-DRAG.dx,xa,xb); sc.probe.y=clamp(wy-DRAG.dy,0,yb); }
    else { const T=sc.tape, X=clamp(wx-DRAG.dx,xa,xb), Y=clamp(wy-DRAG.dy,0,yb);
      if(DRAG.what==='tip'){ T.x1=X; T.y1=Y; } else { T.x0=X; T.y0=Y; } }
    return true;
  };
  /* the wheel zooms a scene about the cannon, within PhET's 0.25..2 */
  S.wheel=function(dy){
    if(!isScene(ST.view)) return false;
    const z=clamp(ST.zoom*Math.exp(-dy*0.0015),ZOOM[0],ZOOM[1]);
    if(z===ST.zoom) return false;
    ST.zoom=z; return true;
  };
  return S;
}
