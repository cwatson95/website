
/* ================================================================== *
 *  special functions and sRGB, extracted by name and unchanged from   *
 *  projects/simulations/diffraction.html (make_ext.py): Bessel J0/J1  *
 *  (series below 17, Hankel asymptotic above), sinc^2 and the Airy   *
 *  pattern with their small-argument series, the sRGB matrix and     *
 *  transfer curve.  Asserted here against scipy (refvals.txt).        *
 * ================================================================== */
const J_SPLIT=17.0;
function besselAsym(nu,x){
  const mu=4*nu*nu, w=8*x;
  /* t_j = prod_{i<=j} (mu - (2i-1)^2) / (j! w^j); even j build P, odd j build Q,
     each with its own alternating sign. */
  let P=1, Q=0, t=1;
  for(let j=1;j<=8;j++){
    t*=(mu-(2*j-1)*(2*j-1))/(j*w);
    if(j%2===0) P+=(((j/2)%2)?-1:1)*t;
    else        Q+=((((j-1)/2)%2)?-1:1)*t;
  }
  const chi=x-(2*nu+1)*PI/4;
  return Math.sqrt(2/(PI*x))*(P*Math.cos(chi)-Q*Math.sin(chi));
}
function besselJ0(x){
  x=Math.abs(x);
  if(x<J_SPLIT){
    const y=x*x/4; let term=1, s=1;
    for(let k=1;k<80;k++){ term*=-y/(k*k); s+=term;
      if(Math.abs(term)<1e-18*Math.abs(s)) break; }
    return s;
  }
  return besselAsym(0,x);
}
function besselJ1(x){
  const sg=x<0?-1:1; x=Math.abs(x);
  if(x<J_SPLIT){
    const y=x*x/4; let term=1, s=1;
    for(let k=1;k<80;k++){ term*=-y/(k*(k+1)); s+=term;
      if(Math.abs(term)<1e-18*Math.abs(s)) break; }
    return sg*(x/2)*s;
  }
  return sg*besselAsym(1,x);
}
function sinc2(b){
  const ab=Math.abs(b);
  if(ab<1e-4){ const b2=b*b; return 1-b2/3+2*b2*b2/45; }
  const s=Math.sin(b)/b; return s*s;
}
function gratingFactor(g,N){
  if(N<=1) return 1;
  const sg=Math.sin(g);
  if(Math.abs(sg)<1e-5) return 1-(N*N-1)*sg*sg/3;
  const r=Math.sin(N*g)/sg;
  return r*r/(N*N);
}
function airyI(v){
  const av=Math.abs(v);
  if(av<1e-4){ const v2=v*v; return 1-v2/4+v2*v2/12; }
  const t=2*besselJ1(v)/v; return t*t;
}
const SRGB_M=[[ 3.2406,-1.5372,-0.4986],
              [-0.9689, 1.8758, 0.0415],
              [ 0.0557,-0.2040, 1.0570]];
function srgbGamma(u){
  u=clamp(u,0,1);
  return u<=0.0031308 ? 12.92*u : 1.055*Math.pow(u,1/2.4)-0.055;
}
