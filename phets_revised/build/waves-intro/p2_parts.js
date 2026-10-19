
/* ================================================================== *
 *  the colour of a wavelength, extracted BY NAME and unchanged from   *
 *  build/wave-interference/p2_ext.js (the sRGB matrix and transfer,   *
 *  themselves extracted there from projects/simulations/diffraction   *
 *  .html) and p2_optics.js (the CIE 1931 table -> linear sRGB,        *
 *  desaturated into gamut).  make_parts.py; nothing retyped.          *
 * ================================================================== */
const SRGB_M=[[ 3.2406,-1.5372,-0.4986],
              [-0.9689, 1.8758, 0.0415],
              [ 0.0557,-0.2040, 1.0570]];
function srgbGamma(u){
  u=clamp(u,0,1);
  return u<=0.0031308 ? 12.92*u : 1.055*Math.pow(u,1/2.4)-0.055;
}
function cieAt(nm){
  const T=CIE1931, x=clamp((nm-T[0][0])/5,0,T.length-1), i=Math.min(T.length-2,Math.floor(x)), f=x-i;
  return [T[i][1]+(T[i+1][1]-T[i][1])*f, T[i][2]+(T[i+1][2]-T[i][2])*f, T[i][3]+(T[i+1][3]-T[i][3])*f];
}
function specLinear(nm){
  const c=cieAt(nm);
  if(c[0]+c[1]+c[2]<1e-9) return [0,0,0];
  let r=SRGB_M[0][0]*c[0]+SRGB_M[0][1]*c[1]+SRGB_M[0][2]*c[2];
  let g=SRGB_M[1][0]*c[0]+SRGB_M[1][1]*c[1]+SRGB_M[1][2]*c[2];
  let b=SRGB_M[2][0]*c[0]+SRGB_M[2][1]*c[1]+SRGB_M[2][2]*c[2];
  const lo=Math.min(r,g,b); if(lo<0){ r-=lo; g-=lo; b-=lo; }
  const hi=Math.max(r,g,b,1e-12);
  return [r/hi,g/hi,b/hi];
}
function specCss(nm,I){
  const c=specLinear(nm), t=clamp(I,0,1);
  return 'rgb('+Math.round(255*srgbGamma(c[0]*t))+','+Math.round(255*srgbGamma(c[1]*t))+','+Math.round(255*srgbGamma(c[2]*t))+')';
}
