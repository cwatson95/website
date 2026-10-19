
/* ================================================================== *
 *  dispatch, the frame step, the pointer                              *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(isCoinView(M.view)) return drawCoins(ctx,W,H,M);
  if(M.view==='binom') return drawBinom(ctx,W,H,M);
  return drawMix(ctx,W,H,M);
}
function viewGeo(ctx,W,H,M){
  if(isCoinView(M.view)) return coinsLayout(ctx,W,H,M).G;
  if(M.view==='binom') return binomLayout(ctx,W,H,M).G;
  return mixLayout(ctx,W,H,M).G;
}
function inBox(x,y,b,pad){ pad=pad||0; return x>=b.x-pad&&x<=b.x1+pad&&y>=b.y-pad&&y<=b.y1+pad; }
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); return drawView(ctx,S.W,S.H,buildModel()); };
  /* one frame: only a flip moves anything in this sim */
  S.step=function(dtWall){
    const dt=Math.max(0,dtWall||0); if(!(dt>0)) return false;
    T_NOW+=dt;
    if(!isCoinView(ST.view)) return false;
    const sc=sceneOf(ST.view); const a=coinStep(sc,sc.single,dt), b=coinStep(sc,sc.set,dt); return a||b;
  };
  /* the pointer: clicking a coin (or the set) reveals or hides it, as PhET's button does */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(type!=='down'||!isCoinView(ST.view)) return false;
    const sc=sceneOf(ST.view); if(sc.preparing) return false;
    const G=viewGeo(canvas.getContext('2d'),S.W,S.H,buildModel());
    if(inBox(x,y,G.B)) return coinToggle(sc,sc.single);
    if(inBox(x,y,G.C)) return coinToggle(sc,sc.set);
    return false;
  };
  return S;
}
