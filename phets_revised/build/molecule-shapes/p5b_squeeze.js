/* ================================================================== *
 *  view: the squeeze (full only)                                      *
 * ================================================================== */
const SQ_LABEL={AX2E1:'AX₂E bent',AX2E2:'AX₂E₂ bent',AX3E1:'AX₃E pyramid',AX4E1_ax:'AX₄E axial',AX4E1_eq:'AX₄E equatorial',AX3E2_axeq:'AX₃E₂ T',AX5E1_axb:'AX₅E pyramid'};
const SQ_YLO=-10, SQ_YHI=2.5, DB_XLO=-20, DB_XHI=3;
const SQ_CAP='Top: each lone-pair class’s bond angle minus its ideal value, as the lone pairs are pulled in from the bonds’ sphere (ρ = 1, every angle ideal) to PhET’s 0.70. Orange diamonds sit where the model matches a measured molecule; the ones pinned at the left edge need more squeeze than ρ = 0.70 gives, and SF₄’s equatorial −18.4° is off the scale. Bottom: the seven measured angles (orange) against the model at the current ρ (green), both as departures from ideal. Drag across the top panel to set ρ.';
const SQ_CAP_SHORT='Angle minus ideal against ρ (top); the measured molecules against the model (bottom). Drag the top panel to set ρ.';
const SQ_CAP_ONE='Each lone-pair class’s bond angle minus its ideal value against ρ; orange diamonds mark the measured molecules (the readout lists all seven). Drag across the panel to set ρ.';
/* two panels when there is room for both, else the curves alone (a narrow stage keeps
   its one primary panel: Known-bad, two-column layouts collapse) */
function squeezeGeo(ctx,W,H){
  const narrow=isNarrow(W), left=narrow?64:150, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-20));
  const top=stageTop()+44;
  let fit=fitCaption(ctx,W,H-HINT_H,SQ_CAP,SQ_CAP_SHORT,capW,top+340);
  let avail=fit.capY-44-top;          /* 44: the lower axis's ticks and title clear the caption */
  if(avail<300){ fit=fitCaption(ctx,W,H-HINT_H,SQ_CAP_ONE,SQ_CAP_ONE,capW,top+120); avail=fit.capY-44-top;
    return {fit,capW,narrow,two:false,top:box(left,top,right-left,Math.max(60,avail)),bot:null}; }
  const h1=Math.floor((avail-70)*0.56), h2=avail-70-h1;
  return {fit,capW,narrow,two:true,top:box(left,top,right-left,h1),bot:box(left,top+h1+70,right-left,h2)};
}
function rhoAtX(b,x){ return Math.round(clamp(RHO_MIN+(x-b.x)/b.w*(RHO_MAX-RHO_MIN),RHO_MIN,RHO_MAX)*100)/100; }
function drawSqueeze(ctx,W,H,M){
  const G=squeezeGeo(ctx,W,H), tb=G.top, bb=G.bot, cv=M.curves;
  axesR(ctx,tb,RHO_MIN,RHO_MAX,SQ_YLO,SQ_YHI,{xticks:[0.70,0.75,0.80,0.85,0.90,0.95,1.00],xfmt:v=>fmt(v,2),yticks:[-10,-8,-6,-4,-2,0,2],yfmt:v=>(v>0?'+':v<0?'−':'')+Math.abs(v)+'°',
    xlab:'ρ, the lone pairs’ radius (PhET’s 0.70 at the left, a lone pair = a bond at 1)',title:titleFor(tb,'how far pulling the lone pairs in bends each bond angle (degrees from ideal)','angle − ideal against ρ')});
  polyline(ctx,tb,[RHO_MIN,RHO_MAX],[0,0],RHO_MIN,RHO_MAX,SQ_YLO,SQ_YHI,rgba(COL.dim,0.7),1,[4,4]);
  SQ_KEYS.forEach((k,i)=>{
    const col=k==='AX4E1_eq'?'#e0f28c':mix(COL.pos,'#ffffff',0.08*i);
    polyline(ctx,tb,SQ_RHO,cv[k],RHO_MIN,RHO_MAX,SQ_YLO,SQ_YHI,col,1.8);
  });
  /* labels at the left end, through the registry */
  SQ_KEYS.forEach(k=>{ const y0=cv[k][0], Y=tb.y1-tb.h*(y0-SQ_YLO)/(SQ_YHI-SQ_YLO);
    if(!G.narrow) lab(ctx,W,H,tb.x-34,Y,SQ_LABEL[k],COL.pos,SM_FONT,'right','middle'); });
  /* the measured molecules: on the curve where the model matches, or pinned left */
  for(const r of M.rows){
    const dm=r.meas-r.ideal, px=r.rfit===null?RHO_MIN:r.rfit;
    const X=tb.x+tb.w*(px-RHO_MIN)/(RHO_MAX-RHO_MIN), Yr=tb.y1-tb.h*(dm-SQ_YLO)/(SQ_YHI-SQ_YLO), Y=clamp(Yr,tb.y+4,tb.y1-4);
    diamond(ctx,X,Y,5,COL.ref,'#fff');
    if(Yr>tb.y1){ line2(ctx,X,tb.y1-4,X,tb.y1+6,COL.ref,1.5); lab(ctx,W,H,X+9,tb.y1-12,formulaText(r.c.mol)+' '+r.c.what+': '+fmt(dm,1)+'°, off the scale',COL.ref,SM_FONT,'left','middle'); }
    else lab(ctx,W,H,X+8,Y-9,formulaText(r.c.mol),COL.ref,SM_FONT,'left','bottom');
  }
  const Xr=tb.x+tb.w*(ST.rho-RHO_MIN)/(RHO_MAX-RHO_MIN);
  line2(ctx,Xr,tb.y,Xr,tb.y1,rgba(COL.live,0.85),1.6);
  SQ_KEYS.forEach(k=>{ const i=Math.round((ST.rho-RHO_MIN)*100), y0=cv[k][clamp(i,0,SQ_RHO.length-1)];
    dot(ctx,Xr,tb.y1-tb.h*(clamp(y0,SQ_YLO,SQ_YHI)-SQ_YLO)/(SQ_YHI-SQ_YLO),3.2,COL.live,null); });
  lab(ctx,W,H,Xr+(Xr>tb.x+tb.w*0.8?-6:6),tb.y+6,'ρ = '+fmt(ST.rho,2),COL.live,LAB_FONT,Xr>tb.x+tb.w*0.8?'right':'left','top');
  /* the dumbbells */
  if(!G.two){ caption(ctx,20,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT); return; }
  const n=M.rows.length, rh=bb.h/n;
  axesR(ctx,bb,DB_XLO,DB_XHI,0,n,{xticks:[-20,-15,-10,-5,0],xfmt:v=>(v<0?'−':'')+Math.abs(v)+'°',yticks:[],xlab:'measured (orange) and model at ρ = '+fmt(ST.rho,2)+' (green), minus ideal',
    title:titleFor(bb,'seven measured angles against the model','measured against the model')});
  polyline(ctx,bb,[0,0],[0,n],DB_XLO,DB_XHI,0,n,rgba(COL.dim,0.7),1,[4,4]);
  M.rows.forEach((r,i)=>{
    const Y=bb.y+rh*(i+0.5), xm=bb.x+bb.w*(r.meas-r.ideal-DB_XLO)/(DB_XHI-DB_XLO), xo=bb.x+bb.w*(r.model-r.ideal-DB_XLO)/(DB_XHI-DB_XLO);
    line2(ctx,xm,Y,xo,Y,rgba(r.agree?COL.pos:COL.ref,0.45),2);
    diamond(ctx,xm,Y,5,COL.ref,'#fff'); dot(ctx,xo,Y,4.5,COL.pos,'#10131b',1);
    if(!G.narrow) lab(ctx,W,H,bb.x-8,Y,formulaText(r.c.mol)+' '+r.c.what,r.agree?COL.text:COL.ref,SM_FONT,'right','middle');
    else lab(ctx,W,H,bb.x-6,Y,formulaText(r.c.mol),r.agree?COL.text:COL.ref,SM_FONT,'right','middle');
  });
  const bad=M.rows.filter(r=>!r.agree);
  if(bad.length){ const r=bad[0], Y=bb.y+rh*(M.rows.indexOf(r)+0.5), xo=bb.x+bb.w*(r.model-r.ideal-DB_XLO)/(DB_XHI-DB_XLO);
    lab(ctx,W,H,xo+10,Y+12,'opposite ways: the model opens it',COL.ref,SM_FONT,'left','top'); }
  caption(ctx,20,G.fit.capY,G.fit.txt,G.fit.capW,'#767e92',CAP_FONT);
}
function diamond(ctx,x,y,r,fill,stroke){
  ctx.beginPath(); ctx.moveTo(x,y-r); ctx.lineTo(x+r,y); ctx.lineTo(x,y+r); ctx.lineTo(x-r,y); ctx.closePath();
  ctx.fillStyle=fill; ctx.fill(); if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=1; ctx.stroke(); }
}

