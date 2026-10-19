
/* ================================================================== *
 *  drawing helpers shared by the views (y is UP in the world, so the  *
 *  map flips; layouts are built bottom-up from a measured caption)    *
 *  — from projects/simulations/build_buoy/p4_views.js by name,   *
 *  unchanged; its world-map and fluid helpers are left behind              *
 * ================================================================== */
const CAP_FONT='11.5px -apple-system, sans-serif';
const LAB_FONT='11px -apple-system, sans-serif';
const SM_FONT='10.5px -apple-system, sans-serif';
function isNarrow(W){ return W<900; }

function dot(ctx,x,y,r,fill,stroke,lw){
  ctx.beginPath(); ctx.arc(x,y,r,0,TAU);
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1.2; ctx.stroke(); }
}
/* the label registry: the audit's half-pixel overlap rule, shift or drop */
let LABELS=[];
function labFits(bx){
  for(const o of LABELS) if(bx[0]<o[2]-0.5&&bx[2]>o[0]+0.5&&bx[1]<o[3]-0.5&&bx[3]>o[1]+0.5) return false;
  return true;
}
function lab(ctx,W,H,x,y,txt,col,font,align,base){
  ctx.fillStyle=col||'#aeb6c6'; ctx.font=font||LAB_FONT;
  const al=align||'left', bl=base||'middle';
  ctx.textAlign=al; ctx.textBaseline=bl;
  const t=plain(txt), fs=parseFloat((font||LAB_FONT).match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  for(const dy of [0,16,-16,32,-32]){
    let X=x, Y=y+dy;
    if(al==='left') X=clamp(X,2,W-w-2); else if(al==='right') X=clamp(X,w+2,W-2); else X=clamp(X,w/2+2,W-w/2-2);
    Y=clamp(Y,hh,H-hh);
    const lx=al==='center'?X-w/2:(al==='right'?X-w:X);
    const ly=bl==='top'?Y:(bl==='middle'?Y-hh/2:(bl==='bottom'?Y-hh:Y-hh*0.8));
    const bx=[lx,ly,lx+w,ly+hh];
    if(labFits(bx)){ LABELS.push(bx); ctx.fillText(t,X,Y); return true; }
  }
  return false;
}
function titleFor(b,longT,shortT){ return (b.w<330||plain(longT).length*13*0.52+10>b.w)?shortT:longT; }
function axesR(ctx,b,xlo,xhi,ylo,yhi,opt){
  axes(ctx,b,xlo,xhi,ylo,yhi,opt);
  if(opt&&opt.title){ const t=plain(opt.title), w=t.length*13*0.52; LABELS.push([b.x,b.y-9-13*1.15,b.x+w,b.y-9]); }
}
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
function drawCaption(ctx,L){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); }
function marker(ctx,b,xlo,xhi,ylo,yhi,x,y,col){
  const X=b.x+b.w*(x-xlo)/(xhi-xlo), Y=b.y1-b.h*(y-ylo)/(yhi-ylo);
  dot(ctx,clamp(X,b.x,b.x1),clamp(Y,b.y,b.y1),4.5,col||COL.live,'#fff');
}
