
/* ================================================================== *
 *  dispatch, the frame step, the pointer                              *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  const f={coins:drawCoins,photons:drawPhotons,spins:drawSpins,bloch:drawBloch,born:drawBorn,binom:drawBinom}[M.view];
  return f(ctx,W,H,M);
}
/* the geometry of the current view, for hit tests (the SAME functions the
   drawing uses, so a click lands where the picture is) */
function viewGeo(ctx,W,H,M){
  if(M.view==='coins') return coinsLayout(ctx,W,H,M).G;
  if(M.view==='photons') return photonsGeo(ctx,W,H,photonsCaption(M));
  if(M.view==='spins') return spinsGeo(ctx,W,H,spinsCaption(M));
  if(M.view==='bloch') return blochLayout(ctx,W,H,M).G;
  if(M.view==='born') return bornLayout(ctx,W,H,M).G;
  return binomLayout(ctx,W,H,M).G;
}
function inBox(x,y,b,pad){ pad=pad||0; return x>=b.x-pad&&x<=b.x1+pad&&y>=b.y-pad&&y<=b.y1+pad; }
function dialAngle(D,x,y){ const a=Math.atan2(D.cy-y,Math.abs(x-D.cx))/DEG; return clamp(Math.round(Math.abs(a)/PH.CUSTOM_STEP)*PH.CUSTOM_STEP,0,90); }
function discA2(D,x,y){ const th=Math.atan2(Math.abs(x-D.cx),D.cy-y); return snapBias(Math.pow(Math.cos(th/2),2)); }
function orbit(dx,dy){ CAM.theta-=dx*0.008; CAM.phi=clamp(CAM.phi+dy*0.008,-1.45,1.45); }
function resetCam(){ CAM.theta=CAM_HOME.theta; CAM.phi=CAM_HOME.phi; }
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); return drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame of dtWall seconds; true when something on the current view moved */
  S.step=function(dtWall){
    const dt=Math.max(0,dtWall||0); if(!(dt>0)) return false;
    T_NOW+=dt;
    const v=ST.view;
    if(v==='coins'){ const sc=COINS[ST.coinScene]; const a=coinStep(sc,sc.single,dt), b=coinStep(sc,sc.set,dt); return a||b; }
    if(!ST.running) return false;
    if(v==='photons'){ const ps=PHOT[ST.phMode], had=ps.photons.length>0; photonAdvance(ps,ST,dt*simFactor(ST)); return had||ps.photons.length>0||ST.phMode==='many'; }
    if(v==='spins'){ const had=SGS.parts.length>0; sgAdvance(SGS,ST,dt); return had||SGS.parts.length>0||ST.sgMode==='continuous'; }
    if(v==='bloch') return blochAdvance(BLO,ST,dt);
    return false;
  };
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const ctx=canvas.getContext('2d'), M=buildModel(), G=viewGeo(ctx,S.W,S.H,M), v=ST.view;
    if(v==='coins'){
      if(type!=='down') return false;
      const sc=COINS[ST.coinScene]; if(sc.preparing) return false;
      if(inBox(x,y,G.B)) return coinToggle(sc,sc.single);
      if(inBox(x,y,G.C)) return coinToggle(sc,sc.set);
      return false;
    }
    if(v==='photons'){
      const D=G.dial, map=G.map;
      if(type==='down'){
        if(Math.hypot(x-D.cx,y-D.cy)<=D.r+10){ DRAG.what='dial'; ST.phPreset='custom'; ST.phCustom=dialAngle(D,x,y); photonAfterAngle(); return true; }
        if(ST.phMode==='single'&&x>=map.X(-0.21)&&x<=map.X(-0.145)&&y>=map.Y(0.03)&&y<=map.Y(-0.03)){ photonEmit(PHOT.single,ST,0); ST.running=true; return true; }
        return false;
      }
      if(type==='move'&&DRAG.what==='dial'){ const a=dialAngle(D,x,y); if(a!==ST.phCustom){ ST.phCustom=a; photonAfterAngle(); } return true; }
      return false;
    }
    if(v==='spins'){
      const map=G.map, D=G.disc, m=M.S;
      if(type==='down'){
        if(ST.sgExp==='custom'&&D.show&&Math.hypot(x-D.cx,y-D.cy)<=D.r+8){ DRAG.what='disc'; ST.sgA2=discA2(D,x,y); sgAfterChange(); return true; }
        if(ST.sgMode==='single'&&x>=map.X(-0.95)&&x<=map.X(0)&&y>=map.Y(0.36)&&y<=map.Y(-0.36)){ sgShoot(SGS,ST); ST.running=true; return true; }
        if(ST.sgExp==='custom') for(const mg of sgMagnetBoxes(map,m,ST)) if(mg.show&&inBox(x,y,mg.b)){
          if(mg.k===0) ST.sgC1=ST.sgC1==='z'?'x':'z'; else ST.sgC2=ST.sgC2==='z'?'x':'z';
          sgAfterChange(); return true; }
        return false;
      }
      if(type==='move'&&DRAG.what==='disc'){ const a=discA2(D,x,y); if(a!==ST.sgA2){ ST.sgA2=a; sgAfterChange(); } return true; }
      return false;
    }
    if(v==='bloch'){
      if(type==='down'){ DRAG.what='cam'; DRAG.x=x; DRAG.y=y; return true; }
      if(type==='move'&&DRAG.what==='cam'){ orbit(x-DRAG.x,y-DRAG.y); DRAG.x=x; DRAG.y=y; return true; }
      return false;
    }
    if(v==='born'){
      const set=(what,xx)=>{ if(what==='bornTh') ST.bornTh=clamp(Math.round((xx-G.A.x)/G.A.w*180),0,180);
        else if(what==='bornAlpha') ST.bornAlpha=clamp(Math.round((xx-G.B.x)/G.B.w*180),0,180);
        else ST.bornN=clamp(Math.round((xx-G.C.x)/G.C.w*64),1,64); };
      if(type==='down'){
        const what=inBox(x,y,G.A)?'bornTh':(inBox(x,y,G.B)?'bornAlpha':(inBox(x,y,G.C)?'bornN':null));
        if(!what) return false; DRAG.what=what; set(what,x); return true;
      }
      if(type==='move'&&DRAG.what&&DRAG.what.indexOf('born')===0){ set(DRAG.what,x); return true; }
      return false;
    }
    return false;
  };
  return S;
}
/* PhET: a new polarization in single-photon mode resets the counts and clears the photons */
function photonAfterAngle(){ if(ST.phMode==='single'){ photonCounts(PHOT.single); photonClear(PHOT.single); } }
/* PhET: any change to the experiment re-prepares (clears the particles and the counts) */
function sgAfterChange(){ sgClear(SGS); sgResetCounts(SGS); }
