
/* ================================================================== *
 *  field lines: the source is axisymmetric, so its lines lie in       *
 *  meridional planes, and the page (z = 0) is one.  Seeds at the      *
 *  mid-plane are spaced in EQUAL FLUX, so between neighbouring lines  *
 *  (as rings round the axis) runs the same flux 2 pi dPsi.  RK4 on    *
 *  B/|B|; the magnet's side wall (the bound current sheet, where B_u  *
 *  jumps by mu0 M) is crossed exactly: each step continues the field  *
 *  of the side it started on, and a step that would cross is cut to   *
 *  land on the wall by secant iteration (derive.py/explore: without   *
 *  this the lines leaving through the wall missed closure by 2%).     *
 * ================================================================== */
const MAG_LINES=10;
/* #emag */
const COIL_LINES=8;
/* #endemag */
function lineSource(kind,N){
  if(kind==='magnet') return {kind, n:MAG_LINES, ru:(r,u)=>solB(r,u,MAG_R,MAG_B), wall:{a:MAG_R,b:MAG_B}, sing:[[MAG_R,MAG_B],[MAG_R,-MAG_B]], aIn:MAG_R, aOut:MAG_R};
/* #emag */
  const xs=coilLoopsX(N);
  return {kind, N, n:COIL_LINES, ru:(r,u)=>coilRU(N,r,u), psi:(r,u)=>coilPsi(N,r,u), wall:null, sing:xs.map(x=>[COIL_A,x]), aIn:COIL_A-WIRE_R, aOut:COIL_A+WIRE_R};
/* #endemag */
}
/* #emag */
/* the coil's flux function is closed form, so after every step its line is pulled back onto
   its own level set by Newton along grad Psi = (rho B_u, -rho B_rho): every vertex then lies on
   Psi = Psi0 to rounding, and the line closes exactly (the magnet's Psi needs a quadrature, so
   its lines rely on RK4 alone, which closes them to ~2e-5 mm) */
function projectPsi(ls,r,u,p0){
  for(let it=0;it<4;it++){
    const p=ls.psi(r,u), B=ls.ru(r,u), gr=r*B[1], gu=-r*B[0], g2=gr*gr+gu*gu;
    if(!(g2>0)) break;
    const d=(p0-p)/g2; r+=d*gr; u+=d*gu;
    if(Math.abs(p0-p)<=1e-15*Math.abs(p0)) break;
  }
  return [r,u];
}
/* #endemag */
const GL24=gaussLegendre(24);
/* the flux function on the mid-plane, Psi(r, 0) = int_0^r B_u(rho, 0) rho drho (unit source) */
function psiMid(ls,r){
/* #emag */
  if(ls.kind==='coil') return coilPsi(ls.N,r,0);
/* #endemag */
  let s=0; for(let i=0;i<24;i++){ const rr=0.5*r*(GL24.x[i]+1); s+=GL24.w[i]*ls.ru(rr,0)[1]*rr; }
  return 0.5*r*s;
}
function bisect(f,lo,hi,n){ let flo=f(lo); for(let i=0;i<(n||200);i++){ const m=0.5*(lo+hi), fm=f(m); if(m<=lo||m>=hi) break; if((fm>0)===(flo>0)){ lo=m; flo=fm; } else hi=m; } return 0.5*(lo+hi); }
function lineSeeds(ls,n){
  const pm=psiMid(ls,ls.aIn), out=[];
  for(let i=1;i<=n;i++){ const t=i*pm/(n+1); out.push({psi:t, r:bisect(r=>psiMid(ls,r)-t,0,ls.aIn)}); }
  return {psiMax:pm, seeds:out};
}
function fieldCont(ls,r,u,r0,u0){
  const B=ls.ru(r,u);
  if(ls.wall){ const a=ls.wall.a, b=ls.wall.b;
    if(Math.abs(u)<b&&Math.abs(u0)<b){ if(r0<a&&r>a) B[1]+=1; else if(r<a&&r0>a) B[1]-=1; } }
  return B;
}
function lineStep(ls,r,u){
  let d=1e9; for(const s of ls.sing) d=Math.min(d,Math.hypot(r-s[0],u-s[1]));
  return Math.max(0.005,Math.min(0.12*d,0.03*Math.hypot(r,u)+1,6));
}
function rk4Line(ls,r,u,h){
  const r0=r, u0=u;
  const f=(rr,uu)=>{ const B=fieldCont(ls,rr,uu,r0,u0), m=Math.hypot(B[0],B[1]); return [B[0]/m,B[1]/m]; };
  const k1=f(r,u), k2=f(r+h/2*k1[0],u+h/2*k1[1]), k3=f(r+h/2*k2[0],u+h/2*k2[1]), k4=f(r+h*k3[0],u+h*k3[1]);
  return [r+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), u+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])];
}
/* one closed line from (r0, 0) inside, forward along B: out, round, back.  Returns the
   polyline (rho, u), where it crossed the mid-plane outside (rOut), the closure error. */
function traceLine(ls,r0,maxN){
  maxN=maxN||20000;
  const pts=[[r0,0]]; let r=r0, u=0, rOut=null, walls=0;
  /* #emag */
  const p0=ls.psi?ls.psi(r0,0):null;
  /* #endemag */
  for(let n=0;n<maxN;n++){
    const h=lineStep(ls,r,u);
    let nx=rk4Line(ls,r,u,h);
    if(ls.wall){ const a=ls.wall.a, b=ls.wall.b;
      if((Math.abs(u)<b||Math.abs(nx[1])<b)&&(r-a)*(nx[0]-a)<0){
        let h0=0, f0=r-a, h1=h, f1=nx[0]-a, m=nx;
        for(let it=0;it<60;it++){
          const hm=h1-f1*(h1-h0)/(f1-f0); m=rk4Line(ls,r,u,hm); const fm=m[0]-a;
          h0=h1; f0=f1; h1=hm; f1=fm; if(Math.abs(fm)<1e-12) break;
        }
        nx=m;
        if(Math.abs(nx[1])<b){ walls++; nx=[a+(r<a?1e-9:-1e-9),nx[1]]; }
      }
    }
    /* #emag */
    if(p0!==null) nx=projectPsi(ls,nx[0],nx[1],p0);
    /* #endemag */
    /* the line crosses the mid-plane at right angles (B_rho vanishes there by symmetry), so r
       is quadratic in u about the crossing: a parabola through the two vertices either side and
       the one before them beats linear interpolation by ~3 decades */
    if(u>0&&nx[1]<=0&&rOut===null&&r>ls.aOut){ rOut=crossR(pts,r,u,nx); }
    if(rOut!==null&&u<0&&nx[1]>=0&&r<ls.aIn){ const re=crossR(pts,r,u,nx); pts.push([re,0]);
      return {pts, rOut, close:Math.abs(re-r0), steps:n+1, walls, ok:true}; }
    r=nx[0]; u=nx[1]; pts.push([r,u]);
    if(Math.hypot(r,u)>2e5) return {pts, rOut, close:NaN, steps:n+1, walls, ok:false};
  }
  return {pts, rOut, close:NaN, steps:maxN, walls, ok:false};
}
/* r at u = 0 from the parabola through (u_prev, r_prev), (u, r) and (u_next, r_next) */
function crossR(pts,r,u,nx){
  const p=pts.length>1?pts[pts.length-2]:null;
  if(!p||p[1]===u||p[1]===nx[1]) return r+(u/(u-nx[1]))*(nx[0]-r);
  const x0=p[1], y0=p[0], x1=u, y1=r, x2=nx[1], y2=nx[0];
  return y0*(0-x1)*(0-x2)/((x0-x1)*(x0-x2))+y1*(0-x0)*(0-x2)/((x1-x0)*(x1-x2))+y2*(0-x0)*(0-x1)/((x2-x0)*(x2-x1));
}
const LINE_CACHE={};
function fieldLinesFor(kind,N){
  const key=kind==='magnet'?'magnet':'coil'+N;
  if(LINE_CACHE[key]) return LINE_CACHE[key];
  const ls=lineSource(kind,N), sd=lineSeeds(ls,ls.n);
  const lines=sd.seeds.map(s=>{ const L=traceLine(ls,s.r); L.psi=s.psi; L.r0=s.r; return L; });
  return (LINE_CACHE[key]={kind,N,psiMax:sd.psiMax,lines});
}
