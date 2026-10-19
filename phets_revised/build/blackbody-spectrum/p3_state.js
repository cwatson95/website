
/* ================================================================== *
 *  state, the per-view model, readout, eqbar, tag                     *
 * ================================================================== */
const TABS=[['spec','the spectrum'],['star','the star'],['peak','the peak'],['total','the total'],['limits','the limits']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a', wien:'#7fb3ff', bg:'#070b18'};
const RO_W=300;
/* PhET's defaults: the Sun, 3 µm × 100 MW/m²/µm, all three checkboxes off, no saved curves.
   The Graph Values point sits at the peak (gvNm is reset to it whenever T changes). */
const DEFAULTS={view:'spec', T:T_DEFAULT, ix:IX_DEFAULT, iy:IY_DEFAULT,
                gv:false, labels:false, inten:false, gvNm:peakNm(T_DEFAULT), gvCue:true,
                rj:true, wien:true};
const ST=Object.assign({},DEFAULTS);
const SAVED=[];                                     /* saved temperatures, oldest first, at most MAX_SAVED */
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---- the actions every control goes through ---------------------------------------------------- */
function setT(T){ ST.T=snapT(T); ST.gvNm=peakNm(ST.T); }              /* PhET: a new T sends the point to the peak */
function zoomX(dir){ ST.ix=clamp(ST.ix+dir,0,ZOOM_X.length-1); }        /* dir +1 zooms OUT (a longer axis) */
function zoomY(dir){ ST.iy=clamp(ST.iy+dir,0,ZOOM_Y.length-1); }
function fitAxes(){ const f=fitZoom(ST.T); ST.ix=f[0]; ST.iy=f[1]; }
function saveCurve(){ SAVED.push(ST.T); while(SAVED.length>MAX_SAVED) SAVED.shift(); }
function eraseSaved(){ SAVED.length=0; }
function setGraphValues(on){ ST.gv=!!on; ST.gvNm=peakNm(ST.T); }     /* PhET: toggling it also re-centres on the peak */
function resetAll(){ const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v; ST.gvNm=peakNm(ST.T); SAVED.length=0; }

/* ---- the curves ---------------------------------------------------------------------------------- */
const N_CURVE=600;
/* samples of M_λ on [0, xmaxNm], the exact peak inserted: x in µm, y in MW/m²/µm */
function curveSamples(T,xmaxNm){
  const xs=[], ys=[], lp=peakNm(T); let put=!(lp>0&&lp<xmaxNm);
  for(let i=0;i<=N_CURVE;i++){
    const L=xmaxNm*i/N_CURVE;
    if(!put&&L>lp){ xs.push(lp/1000); ys.push(specPow(lp,T)); put=true; }
    xs.push(L/1000); ys.push(L>0?specPow(L,T):0);
  }
  return {xs,ys};
}
/* log-spaced samples between two wavelengths (nm), for the log–log views */
function logSamples(fn,loNm,hiNm,n){
  const xs=[], ys=[], a=Math.log(loNm), b=Math.log(hiNm);
  for(let i=0;i<=n;i++){ const L=Math.exp(a+(b-a)*i/n); xs.push(L/1000); ys.push(fn(L)); }
  return {xs,ys};
}
function tempLabel(T){ const p=presetAt(T); return fmt(T,0)+' K'+(p?' — '+p.name:''); }

/* ---- the models -------------------------------------------------------------------------------- */
function specModel(st){
  const T=st.T, xmax=ZOOM_X[st.ix], ymax=ZOOM_Y[st.iy], lm=peakNm(T), Mp=peakPow(T);
  const saved=SAVED.map((Ts,i)=>({T:Ts, newest:i===SAVED.length-1, c:curveSamples(Ts,xmax), lm:peakNm(Ts), Mp:peakPow(Ts)}));
  const gvM=specPow(st.gvNm,T);
  return {T,xmax,ymax,lm,Mp,I:intensity(T),c:curveSamples(T,xmax),saved,
          gv:{on:st.gv,nm:st.gvNm,M:gvM,inside:st.gvNm<=xmax,above:gvM>ymax,cue:st.gvCue},
          win:fracBelow(xmax,T),over:Mp>ymax,tiny:Mp<ymax/100,peakIn:lm<=xmax,fit:fitZoom(T),
          ph:photometer(T),halo:[haloRadius(T),haloAlpha(T)],cie:bbBytes(T),glow:glowLevel(T),
          canInX:st.ix>0,canOutX:st.ix<ZOOM_X.length-1,canInY:st.iy>0,canOutY:st.iy<ZOOM_Y.length-1};
}
/* the colour of every temperature on the thermometer, both ways (memoised: it does not depend on T) */
function colourStrips(){
  return memo('strips','all',()=>{
    const Ts=[], ph=[], cie=[], glow=[], phCss=[], cieCss=[];
    for(let T=T_MIN;T<=T_MAX;T+=T_SNAP){
      const p=photometer(T), gl=glowLevel(T);
      Ts.push(T); ph.push(p); cie.push(bbBytes(T)); glow.push(gl);
      phCss.push('rgb('+p.join(',')+')'); cieCss.push(cssOfLinear(bbLinear(T),gl));
    }
    return {Ts,ph,cie,glow,phCss,cieCss};
  });
}
function starModel(st){
  const T=st.T, xy=chroma(T), b=bbBytes(T);
  return {T,ph:photometer(T),phRaw:photometerRaw(T),r:phRenorm(T),halo:[haloRadius(T),haloAlpha(T)],
          xy,cie:b,hex:hexOfBytes(b),glow:glowLevel(T),eff:efficacy(T),strips:colourStrips(),
          lamCh:PH_LAM.map(l=>specPow(l,T))};
}
function peakModel(st){
  const T=st.T, lm=peakNm(T), Mp=peakPow(T);
  const fam=PRESETS.map(p=>({T:p.T,name:p.name,lm:peakNm(p.T),Mp:peakPow(p.T),
    c:logSamples(L=>specPow(L,p.T),50,2e5,320)}));
  const cur={T,lm,Mp,c:logSamples(L=>specPow(L,T),50,2e5,320)};
  /* the universal curve: M/M_peak against λ/λ_max, for the current T and each preset */
  const uni=[T].concat(PRESETS.map(p=>p.T)).map(Tu=>{ const l0=peakNm(Tu), m0=peakPow(Tu), xs=[], ys=[];
    for(let i=1;i<=400;i++){ const u=5*i/400; xs.push(u); ys.push(specPow(u*l0,Tu)/m0); } return {T:Tu,xs,ys}; });
  return {T,lm,Mp,fam,cur,uni,nu:NU_PER_T*T,lamNu:C_LIGHT/(NU_PER_T*T)/NM,kpk:K_PEAK};
}
function totalModel(st){
  const T=st.T, I=intensity(T);
  const curve=memo('sbcurve','all',()=>logSamples(TT=>intensity(TT),T_MIN,T_MAX,200));   /* x = T/1000 */
  const budget=memo('budget','all',()=>{ const Ts=[], f=BANDS.map(()=>[]);
    for(let TT=T_MIN;TT<=T_MAX;TT+=T_SNAP){ Ts.push(TT); BANDS.forEach((bd,i)=>f[i].push(bandFrac(bd.lo,bd.hi,TT))); }
    return {Ts,f}; });
  return {T,I,quad:totalByQuadrature(T),bands:BANDS.map(bd=>bandFrac(bd.lo,bd.hi,T)),curve,budget,
          win:fracBelow(ZOOM_X[st.ix],T),xmax:ZOOM_X[st.ix]};
}
/* x where Rayleigh–Jeans is 1 % high: (eˣ − 1)/x = 1.01, by bisection */
const X_RJ1=(function(){ let lo=1e-6, hi=1; for(let i=0;i<100;i++){ const m=0.5*(lo+hi); if(rjRatio(m)<1.01) lo=m; else hi=m; } return 0.5*(lo+hi); })();
const X_W1=Math.log(100);                                   /* 1 − e^−x = 0.99 */
function limitsModel(st){
  const T=st.T, lo=10, hi=1e6;
  const pl=logSamples(L=>specPow(L,T),lo,hi,420), rj=logSamples(L=>rjExitance(L*NM,T)*TO_DISP,lo,hi,420),
        wi=logSamples(L=>wienExitance(L*NM,T)*TO_DISP,lo,hi,420);
  const ratios=memo('ratios','all',()=>{ const xs=[], r=[], w=[];
    for(let i=0;i<=300;i++){ const x=Math.pow(10,-3+i*(Math.log10(30)+3)/300); xs.push(x); r.push(rjRatio(x)); w.push(wienRatio(x)); }
    return {xs,r,w}; });
  return {T,lm:peakNm(T),Mp:peakPow(T),pl,rj,wi,ratios,lamRJ1:C2/(X_RJ1*T)/NM,lamW1:C2/(X_W1*T)/NM,
          rjPeak:rjRatio(X5),wPeak:wienRatio(X5)};
}
function buildModel(){
  const st=ST, view=st.view;
  const M={view,st,T:st.T};
  if(view==='spec') M.S=specModel(st);
  else if(view==='star') M.C=starModel(st);
  else if(view==='peak') M.P=peakModel(st);
  else if(view==='total') M.O=totalModel(st);
  else M.L=limitsModel(st);
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
const SUPS={'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','-':'⁻'};
function supNum(n){ return String(n).split('').map(ch=>SUPS[ch]||ch).join(''); }
/* significant figures, with a ×10ⁿ exponent outside 10⁻³ … 10⁵ */
function sci(x,n){
  if(!isFinite(x)) return '—';
  if(x===0) return '0';
  n=n||3;
  const e=Math.floor(Math.log10(Math.abs(x)));
  if(e>=-3&&e<5) return sigf(x,n);
  let m=x/Math.pow(10,e), ms=m.toFixed(n-1), ee=e;
  if(Math.abs(+ms)>=10){ ms=(m/10).toFixed(n-1); ee=e+1; }
  return ms+'×10'+supNum(ee);
}
function um(nm,n){ return sigf(nm/1000,n||4)+' µm'; }
function pct(f){ return f>=0.9995&&f<1 ? '> 99.9 %' : (f<5e-4&&f>0 ? '< 0.05 %' : sigf(100*f,3)+' %'); }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function swatch(bytes){ return '<i style="display:inline-block;width:10px;height:10px;border-radius:2px;vertical-align:-1px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.25);background:rgb('+bytes.join(',')+')"></i>'; }
function readoutHTML(M){
  const st=M.st, T=M.T, p=presetAt(T);
  let s='<div class="rname">'+fmt(T,0)+' K<small>'+(p?p.name+' · ':'')+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='spec'){
    const S=M.S;
    s+=hd('Wien: the peak')+rrow('&lambda;<sub>max</sub> = b/T',um(S.lm)+' ('+sigf(S.lm,4)+' nm)')+rrow('M<sub>&lambda;</sub> at the peak',sci(S.Mp,4)+' MW/m&sup2;/&micro;m',S.over?'bad':'');
    s+=hd('Stefan&ndash;Boltzmann: the area')+rrow('intensity &sigma;T&#8308;',sci(S.I,3)+' W/m&sup2;',st.inten?'good':'')
      +rrow('inside 0&ndash;'+axisMax(S.xmax/1000)+' &micro;m',pct(S.win));
    if(S.gv.on) s+=hd('graph values')+rrow('wavelength',um(S.gv.nm))+rrow('spectral power density',sci(S.gv.M,4)+' MW/m&sup2;/&micro;m','good')
      +(S.gv.inside?'':rrow('the point','beyond the axis: zoom out','bad'));
    s+=hd('the axes')+rrow('wavelength',' 0&ndash;'+axisMax(S.xmax/1000)+' &micro;m')+rrow('power',' 0&ndash;'+axisMax(S.ymax)+' MW/m&sup2;/&micro;m');
    if(SAVED.length){ s+=hd('saved curves'); S.saved.slice().reverse().forEach((c,i)=>{ s+=rrow((i===0?'newer (solid)':'older (dashed)'),fmt(c.T,0)+' K, peak '+um(c.lm,3)); }); }
    s+=hd('the colour')+rrow('PhET photometer R G B',S.ph.join(' '))+rrow('true colour (CIE 1931)',swatch(S.cie)+' '+hexOfBytes(S.cie));
  }
  else if(M.view==='star'){
    const C=M.C;
    s+=hd('PhET&rsquo;s photometer')+rrow('M at 650, 550, 450 nm',C.lamCh.map(v=>sci(v,3)).join(', '))
      +rrow('r = 0.02&radic;(T &minus; 798 K)',sigf(C.r,4),C.r<1?'bad':'')+rrow('channels R G B',C.ph.join(' '))
      +rrow('star colour',swatch(C.ph)+' '+hexOfBytes(C.ph))+rrow('halo radius, opacity',sigf(C.halo[0],3)+' px, '+sigf(C.halo[1],3));
    s+=hd('CIE 1931 colorimetry')+rrow('chromaticity x, y',fmt(C.xy[0],4)+', '+fmt(C.xy[1],4),'good')+rrow('sRGB',swatch(C.cie)+' '+C.hex,'good')
      +rrow('glow (log luminance)',sigf(C.glow,3))+rrow('luminous efficacy',sigf(C.eff,3)+' lm/W');
  }
  else if(M.view==='peak'){
    const P=M.P;
    s+=hd('Wien&rsquo;s law')+rrow('&lambda;<sub>max</sub>',um(P.lm)+' ('+sigf(P.lm,4)+' nm)','good')+rrow('&lambda;<sub>max</sub> T = b',sigf(B_WIEN*1e3,7)+' mm&middot;K')
      +rrow('x&#8325; = 5(1 &minus; e<sup>&minus;x&#8325;</sup>)',fmt(X5,9))+rrow('peak height M(&lambda;<sub>max</sub>)',sci(P.Mp,4)+' MW/m&sup2;/&micro;m')
      +rrow('&hellip; / T&#8309;',sci(P.kpk*TO_DISP,5)+' MW/m&sup2;/&micro;m/K&#8309;');
    s+=hd('the other peak')+rrow('&nu;<sub>max</sub> = x&#8323;kT/h',sci(P.nu,4)+' Hz')+rrow('c/&nu;<sub>max</sub>',um(P.lamNu),'bad')
      +rrow('&hellip; = (x&#8325;/x&#8323;) &lambda;<sub>max</sub>',fmt(X5/X3,4)+' &lambda;<sub>max</sub>');
  }
  else if(M.view==='total'){
    const O=M.O;
    s+=hd('Stefan&ndash;Boltzmann')+rrow('&sigma;T&#8308;',sci(O.I,5)+' W/m&sup2;','good')+rrow('&int; M<sub>&lambda;</sub> d&lambda; (Gauss&ndash;Legendre)',sci(O.quad,5)+' W/m&sup2;')
      +rrow('&sigma;',sci(SIGMA,10)+' W/m&sup2;/K&#8308;');
    s+=hd('where the power goes'); BANDS.forEach((bd,i)=>{ s+=rrow(bd.name,pct(O.bands[i])); });
    s+=rrow('inside the spectrum&rsquo;s 0&ndash;'+axisMax(O.xmax/1000)+' &micro;m',pct(O.win));
  }
  else {
    const L=M.L;
    s+=hd('at the peak, x = x&#8325; = '+fmt(X5,3))+rrow('Rayleigh&ndash;Jeans / Planck',sigf(L.rjPeak,4),'bad')+rrow('Wien / Planck',sigf(L.wPeak,5),'good');
    s+=hd('within 1 % of Planck')+rrow('Rayleigh&ndash;Jeans, &lambda; &gt;',um(L.lamRJ1,4))+rrow('Wien, &lambda; &lt;',um(L.lamW1,4))
      +rrow('&int; M<sub>RJ</sub> d&lambda;','&infin; (the ultraviolet catastrophe)','bad');
  }
  s+='</table><div class="note">h, c, k exact (SI 2019); &sigma;, b, c&#8321;, c&#8322; derived; colour from the CIE&rsquo;s own 1931 table. Everything is pinned in selfTest to build/blackbody-spectrum/derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='spec') return E('<span class="hl">M<sub>&lambda;</sub>(T) = '+'2&pi;hc&sup2; / &lambda;<sup>5</sup> &middot; 1 / (e<sup>hc/&lambda;kT</sup> &minus; 1)</span> &nbsp;&middot;&nbsp; &lambda;<sub>max</sub> = b/T &nbsp;&middot;&nbsp; &int; M<sub>&lambda;</sub> d&lambda; = &sigma;T&#8308;',
    'Planck&rsquo;s law: the power a black surface at temperature T radiates, per square metre and per micrometre of wavelength (&pi; times the radiance)');
  if(M.view==='star') return E('c<sub>R,G,B</sub> = 255 &middot; min(1, 0.02&radic;(T &minus; 798 K)) &middot; M(650 | 550 | 450 nm) / max &nbsp;&nbsp;<span class="rm">vs</span>&nbsp;&nbsp; <span class="hl">(X, Y, Z) = &int; M<sub>&lambda;</sub> (x&#772;, y&#772;, z&#772;) d&lambda;</span>',
    'PhET&rsquo;s photometer samples the curve at three wavelengths; the eye weighs all of it with three broad, overlapping sensitivities');
  if(M.view==='peak') return E('<span class="hl">&lambda;<sub>max</sub> T = b = hc / x&#8325;k = '+sigf(B_WIEN*1e3,7)+' mm&middot;K</span>, &nbsp; x&#8325; = 5(1 &minus; e<sup>&minus;x&#8325;</sup>) = '+fmt(X5,6)+' &nbsp;&middot;&nbsp; M(&lambda;<sub>max</sub>) &prop; T&#8309;',
    'Wien&rsquo;s displacement law: a hotter body peaks at a shorter wavelength, and every curve is the same shape stretched by 1/T and raised by T&#8309;');
  if(M.view==='total') return E('<span class="hl">&int;<sub>0</sub><sup>&infin;</sup> M<sub>&lambda;</sub> d&lambda; = &sigma;T&#8308;</span>, &nbsp; &sigma; = 2&pi;&#8309;k&#8308; / 15h&sup3;c&sup2; &nbsp;&middot;&nbsp; F(&lambda;T) = (15/&pi;&#8308;) &int;<sub>x</sub><sup>&infin;</sup> t&sup3; dt / (e<sup>t</sup> &minus; 1), x = hc/&lambda;kT',
    'the Stefan&ndash;Boltzmann law: double the temperature and a body radiates sixteen times the power; F is the share below a wavelength');
  return E('M<sub>RJ</sub> = 2&pi;ckT / &lambda;&#8308; &nbsp;&middot;&nbsp; M<sub>W</sub> = (2&pi;hc&sup2;/&lambda;<sup>5</sup>) e<sup>&minus;hc/&lambda;kT</sup> &nbsp;&middot;&nbsp; <span class="hl">M<sub>RJ</sub>/M = (e<sup>x</sup> &minus; 1)/x, &nbsp; M<sub>W</sub>/M = 1 &minus; e<sup>&minus;x</sup></span>',
    'Planck&rsquo;s law holds both older laws: Rayleigh&ndash;Jeans where hc/&lambda;kT &#8810; 1 (and infinite in total), Wien&rsquo;s where it is large');
}
function tagHTML(M){
  const T=M.T, p=presetAt(T), lab=TABS.find(t=>t[0]===M.view)[1];
  return '<b>'+lab+'</b> — '+fmt(T,0)+' K'+(p?', '+p.name:'');
}
