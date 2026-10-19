
/* ================================================================== *
 *  state, the per-view model, the readout, the equation bar, the tag  *
 * ================================================================== */
const TABS=[['bound','the boundary'],['wave','the wave'],['prism','the prism'],
            ['fres','the reflected fraction'],['spec','the spectrum'],['bow','the rainbow']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a',
           norm:'#5ac8e0', arc:'#e8843a', axis:'#39506b', edge2:'#2a2f3d',
           sPol:'#b8ec4c', pPol:'#cd35c4', unpol:'#e8843a'};
const RO_W=300;
const HINT_H=18;   /* the house #hint (HTML, bottom:11px) owns the bottom-left */

const PRISMS=[{id:'triangle',name:'triangle'},{id:'trapezoid',name:'trapezoid'},
              {id:'square',name:'square'},{id:'circle',name:'circle'},
              {id:'semicircle',name:'semicircle'}];
const POLS=[{id:'s',name:'s (PhET)'},{id:'p',name:'p'},{id:'unpol',name:'unpolarised'}];

const DEFAULTS={
  view:'bound',
  /* PhET's Intro screen: air above, water below, the laser at 3 pi/4 (45 deg) */
  topSub:'air', topN:1.000293, botSub:'water', botN:PHET.nCustom0,
  angDeg:45, lamNm:PHET.lamRed, white:false, laserOn:true, pol:'s',
  showNormal:true, showAngles:true, showProtractor:false, showMeter:true, paintField:true,
  /* the wave view */
  anim:true, phase:0, waveSpeed:1, showEvanescent:true,
  /* PhET's Prisms screen: air around a glass prism */
  envSub:'air', envN:1.000293, prismSub:'glass', prismN:PHET.nCustom0,
  /* the beam is aimed at the left face at close to the minimum-deviation
     angle, which is the geometry a prism is FOR; the default -7 deg tilt it
     had instead sent the ray into a left-in, right-TIR, bottom-out path that
     is a constant-deviation arrangement and disperses by 0.04 deg, not 1.6 */
  prismId:'triangle', prismRot:0, beamY:-1.6, beamTilt:18.5,
  manyRays:false, showReflections:false, showNormals:false,
  /* the spectrum and the rainbow */
  specSubs:'all', prismApex:60,
  bowK:1, bowKs:'1', bowPol:'unpol', bowRays:true,
};
const ST=Object.assign({},DEFAULTS);

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function clearMemo(){ for(const k in MEMO) delete MEMO[k]; }

/* ---------------------------------------------------- media and colour */
function topIndex(st,lamNm){ return mediumIndex(st.topSub,st.topN,lamNm===undefined?st.lamNm:lamNm); }
function botIndex(st,lamNm){ return mediumIndex(st.botSub,st.botN,lamNm===undefined?st.lamNm:lamNm); }
function envIndex(st,lamNm){ return mediumIndex(st.envSub,st.envN,lamNm===undefined?st.lamNm:lamNm); }
function prismIndex(st,lamNm){ return mediumIndex(st.prismSub,st.prismN,lamNm===undefined?st.lamNm:lamNm); }
/* the name a medium shows; a mystery substance refuses to print its index,
   which is the whole point of it in PhET */
function subLabel(id,n){
  const s=subById(id);
  if(s.mystery) return s.name+' (n = ?)';
  return s.name+' (n = '+fmt(n,4)+')';
}
function isMystery(id){ return !!subById(id).mystery; }
/* a medium's wash: the house cyan, deepening with the index.  Display only. */
function mediumFill(n){ return rgba(COL.struct,clamp(0.05+0.13*(n-1),0.03,0.30)); }
/* the colour of light of this wavelength, at a brightness level */
function wlCss(nm,k){ return cssOfLinear(monoLinear(nm),k===undefined?1:k); }
/* A beam of one wavelength at a power fraction, optionally translucent.
   White light is thirty wavelengths on almost the same path, and an OPAQUE
   stroke means only the last one drawn is ever seen (the lenses.html
   Known-bad): they are drawn at alpha 0.28 so the overlap blends toward white
   and the colours separate exactly where the physics separates them. */
function beamCss(st,nm,power,alpha){
  const lvl=clamp(Math.sqrt(Math.max(power,0)),0,1);
  const v=monoLinear(nm===undefined?st.lamNm:nm);
  const b=[0,1,2].map(i=>Math.round(255*srgbGamma(v[i]*lvl)));
  const a=alpha===undefined?1:alpha;
  return a>=1?'rgb('+b[0]+','+b[1]+','+b[2]+')'
             :'rgba('+b[0]+','+b[1]+','+b[2]+','+fmt(a,3)+')';
}
const WHITE_ALPHA=0.28;
/* PhET stops drawing a reflected ray below 0.005 of the power.  That is a
   decision about the PICTURE, so it lives here where selfTest can ask it,
   not inside the draw call (Known-bad: a number computed inside a draw call
   cannot be tested). */
function drawsReflected(R){ return R>=PHET.drawMin; }
/* the power split that the readout and the ray brightness use */
function powerSplit(f,pol){
  if(pol==='p') return {R:f.Rp,T:f.Tp};
  if(pol==='unpol') return {R:0.5*(f.Rs+f.Rp),T:0.5*(f.Ts+f.Tp)};
  return {R:f.Rs,T:f.Ts};
}

/* ------------------------------------------------ the boundary and wave */
function boundaryModel(st,lamNm){
  const lam=lamNm===undefined?st.lamNm:lamNm;
  const n1=topIndex(st,lam), n2=botIndex(st,lam);
  const th1=clamp(st.angDeg,0,89.999)*DEG;
  const th2=refractAngle(n1,n2,th1);
  const f=fresnel(n1,n2,th1);
  const sp=powerSplit(f,st.pol);
  return {lam:lam,n1:n1,n2:n2,th1:th1,th2:th2,f:f,R:sp.R,T:sp.T,
          tc:criticalAngle(n1,n2),tb:brewster(n1,n2),tir:f.tir,
          dIn:[Math.sin(th1),-Math.cos(th1)],
          dRefl:[Math.sin(th1),Math.cos(th1)],
          dTrans:isFinite(th2)?[Math.sin(th2),-Math.cos(th2)]:null,
          lam1:lambdaIn(lam,n1),lam2:lambdaIn(lam,n2),
          v1:speedIn(n1),v2:speedIn(n2),freq:PHET.c/(lam*NM)};
}

/* ------------------------------------------------------------ the prism */
/* the rays PhET fires: one down the middle, or a fan of five spaced half a
   red wavelength apart across the beam */
function beamOrigins(st){
  const th=st.beamTilt*DEG, d=[Math.cos(th),Math.sin(th)];
  const perp=[-d[1],d[0]];
  const base=[-11.5,st.beamY];
  if(!st.manyRays) return {d:d,origins:[base]};
  const out=[];
  for(let i=PHET.fanLo;i<=PHET.fanHi+1e-9;i+=PHET.fanSpacing)
    out.push([base[0]+perp[0]*i,base[1]+perp[1]*i]);
  return {d:d,origins:out};
}
function prismModel(st){
  const sh=rotShape(prismShape(st.prismId),st.prismRot*DEG);
  const beam=beamOrigins(st);
  const wls=st.white?WHITE_WL:[st.lamNm];
  const bundles=[];
  for(const lam of wls){
    const nOut=envIndex(st,lam), nIn=prismIndex(st,lam);
    for(const o of beam.origins)
      bundles.push({lam:lam,nOut:nOut,nIn:nIn,origin:o,
        tr:traceRay(sh,o,beam.d,nOut,nIn,{reflections:st.showReflections,reach:46})});
  }
  /* grouped by beam origin, so the white-light merge rule can look across
     the thirty wavelengths that share one path */
  const groups=[];
  for(let o=0;o<beam.origins.length;o++){
    const g=bundles.filter((b,i)=>i%beam.origins.length===o);
    groups.push(g);
  }
  return {shape:sh,beam:beam,bundles:bundles,groups:groups,wls:wls,
          nOut:envIndex(st),nIn:prismIndex(st),
          tc:criticalAngle(prismIndex(st),envIndex(st)),
          apex:st.prismId==='triangle'?60*DEG:NaN};
}

/* ---------------------------------------- the Fresnel curves and sweeps */
const FRES_N=181;
function fresnelCurves(n1,n2){
  const th=[],Rs=[],Rp=[],Ru=[],Ts=[],Tp=[];
  for(let i=0;i<FRES_N;i++){
    const t=i/(FRES_N-1)*(90-1e-4)*DEG;
    const f=fresnel(n1,n2,t);
    th.push(t*RAD); Rs.push(f.Rs); Rp.push(f.Rp); Ru.push(0.5*(f.Rs+f.Rp));
    Ts.push(f.Ts); Tp.push(f.Tp);
  }
  return {th:th,Rs:Rs,Rp:Rp,Ru:Ru,Ts:Ts,Tp:Tp};
}

/* -------------------------------------------------------- the spectrum */
const SPEC_N=121;
function spectrumCurves(st){
  const lam=[],rows={};
  for(let i=0;i<SPEC_N;i++) lam.push(PHET.lamMin+(PHET.lamMax-PHET.lamMin)*i/(SPEC_N-1));
  for(const s of SUBS){
    if(s.id==='custom') continue;
    rows[s.id]=lam.map(l=>indexOf(s.n,l));
  }
  rows.custom=lam.map(l=>indexOf(st.botN,l));
  /* the prism's angular spread: the deviation of each wavelength through an
     apex-angle prism at the angle that minimises the 650 nm deviation */
  const A=st.prismApex*DEG;
  const nRed=prismIndex(st,PHET.lamRed), nEnv=envIndex(st,PHET.lamRed);
  const Dm=prismMinDeviation(nEnv,nRed,A);
  const thIn=isFinite(Dm)?(A+Dm)/2:45*DEG;
  const dev=lam.map(l=>prismDeviation(envIndex(st,l),prismIndex(st,l),A,thIn));
  return {lam:lam,rows:rows,dev:dev,thIn:thIn,A:A,Dmin:Dm};
}

/* --------------------------------------------------------- the rainbow */
const BOW_N=241;
function bowModel(st){
  const nRed=dropIndex(st.lamNm);                 /* the RELATIVE index */
  const nW=indexOf(1.333,st.lamNm), nA=indexOf(1.000293,st.lamNm);
  const th=[],devs={};
  for(let i=0;i<BOW_N;i++) th.push(1e-4+(PI/2-2e-4)*i/(BOW_N-1));
  for(const k of [1,2]) devs[k]=th.map(t=>rainDev(nRed,k,t)*RAD);
  const bows={};
  for(const k of [1,2]){
    bows[k]={ths:{},ang:{}};
    for(const l of [400,450,500,550,600,650,700]){
      const n=dropIndex(l);
      bows[k].ths[l]=rainTheta(n,k);
      bows[k].ang[l]=bowAngle(n,k)*RAD;
    }
  }
  const thStar=rainTheta(nRed,st.bowK);
  return {n:nRed,nW:nW,nA:nA,th:th,devs:devs,bows:bows,thStar:thStar,
          devStar:rainDev(nRed,st.bowK,thStar)*RAD,
          angStar:bowAngle(nRed,st.bowK)*RAD,
          thr:Math.asin(nA*Math.sin(thStar)/nW),
          tc:criticalAngle(nW,nA),
          through:bowThroughput(nA,nW,st.bowK,thStar,st.bowPol),
          Rs:bowRsExact(st.bowK),Rp:bowRpExact(st.bowK,nRed),
          gap:bowAngle(nRed,2)*RAD-bowAngle(nRed,1)*RAD};
}

/* ----------------------------------------------------------- the model */
function buildModel(st){
  st=st||ST;
  const key=[st.view,st.topSub,st.topN,st.botSub,st.botN,st.angDeg,st.lamNm,st.white,st.bowRays,st.paintField,st.phase,
             st.laserOn,st.pol,st.envSub,st.envN,st.prismSub,st.prismN,st.prismId,
             st.prismRot,st.beamY,st.beamTilt,st.manyRays,st.showReflections,
             st.prismApex,st.bowK,st.bowPol].join('|');
  return memo('model',key,()=>{
    const M={view:st.view};
    M.b=boundaryModel(st);
    /* the expensive parts are lazy: a sweep that never opens the prism view
       must not pay for a trace (Known-bad: a slow suite is one that does not
       get mutation-tested) */
    let _p=null,_f=null,_s=null,_w=null;
    Object.defineProperty(M,'prism',{get(){ return _p||(_p=prismModel(st)); }});
    Object.defineProperty(M,'fres',{get(){ return _f||(_f=fresnelCurves(M.b.n1,M.b.n2)); }});
    Object.defineProperty(M,'spec',{get(){ return _s||(_s=spectrumCurves(st)); }});
    Object.defineProperty(M,'bow',{get(){ return _w||(_w=bowModel(st)); }});
    M.wave=waveState(M.b.n1,M.b.n2,M.b.th1,M.b.lam);
    return M;
  });
}

/* ================================================================== *
 *  the readout                                                        *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function row(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function pct(x){ return fmt(100*x,2)+'%'; }

function boundReadout(M,st){
  const B=M.b;
  let s='<div class="rname">the boundary<small>PhET&rsquo;s Intro screen</small></div><table>';
  s+=hd('the media');
  s+=row('above',isMystery(st.topSub)?'Mystery A or B':fmt(B.n1,5));
  s+=row('below',isMystery(st.botSub)?'Mystery A or B':fmt(B.n2,5));
  s+=hd('angles');
  s+=row('incidence &theta;<sub>1</sub>',fmt(st.angDeg,2)+'&deg;');
  s+=row('reflection',fmt(st.angDeg,2)+'&deg;');
  s+=row('refraction &theta;<sub>2</sub>',isFinite(B.th2)?fmt(B.th2*RAD,2)+'&deg;':'none',
         isFinite(B.th2)?'good':'bad');
  s+=row('critical angle',isFinite(B.tc)?fmt(B.tc*RAD,2)+'&deg;':'&mdash;');
  s+=row('Brewster angle',fmt(B.tb*RAD,2)+'&deg;');
  s+=hd('the power, '+(st.pol==='s'?'s-polarised':st.pol==='p'?'p-polarised':'unpolarised'));
  s+=row('reflected R',pct(B.R),B.R>0.5?'bad':'');
  s+=row('transmitted T',pct(B.T),'good');
  s+=row('R + T',fmt(B.R+B.T,10),'good');
  s+=hd('inside the media');
  s+=row('&lambda; above',fmt(B.lam1,1)+' nm');
  s+=row('&lambda; below',fmt(B.lam2,1)+' nm');
  s+=row('v above',fmt(1/B.n1,4)+' c');
  s+=row('v below',fmt(1/B.n2,4)+' c');
  s+='</table>';
  s+='<div class="note">'+(B.tir
      ? '<b>Total internal reflection.</b> Past '+fmt(B.tc*RAD,2)+'&deg; there is no angle whose sine is '
        +'n<sub>1</sub>sin&theta;<sub>1</sub>/n<sub>2</sub>, so the whole beam comes back.'
      : 'PhET&rsquo;s intensity meter reads the <b>s</b>-polarised reflectance; the chips switch it to p '
        +'or to the unpolarised average, which is what an ordinary lamp gives.')+'</div>';
  return s;
}
function waveReadout(M,st){
  const B=M.b, W=M.wave;
  const rA=cAbs(W.f.rRe,W.f.rIm), tA=cAbs(W.f.tRe,W.f.tIm);
  let s='<div class="rname">the wave<small>PhET&rsquo;s wave view and More Tools</small></div><table>';
  s+=hd('the meters');
  s+=row('speed above',fmt(1/B.n1,4)+' c');
  s+=row('speed below',fmt(1/B.n2,4)+' c');
  s+=row('&lambda; above',fmt(B.lam1,1)+' nm');
  s+=row('&lambda; below',fmt(B.lam2,1)+' nm');
  s+=row('frequency',sigf(B.freq,5)+' Hz','good');
  s+=hd('the field, s-polarised');
  s+=row('|r|',fmt(rA,5));
  s+=row('|t|',fmt(tA,5));
  s+=row('1 + r &minus; t',fmt(W.f.rRe+1-W.f.tRe,10),'good');
  s+=row('crest spacing along y = 0',fmt(B.lam1/Math.max(Math.sin(B.th1),1e-9),1)+' nm');
  s+=row('same, from below',isFinite(B.th2)?fmt(B.lam2/Math.max(Math.sin(B.th2),1e-9),1)+' nm':'&mdash;','good');
  if(B.tir){
    s+=hd('the evanescent tail');
    s+=row('decay length 1/&kappa;',fmt(B.lam/(TAU*W.f.kap),1)+' nm','bad');
    s+=row('phase of r',fmt(cArg(W.f.rRe,W.f.rIm),4)+' rad');
  }
  s+='</table>';
  s+='<div class="note">The frequency is the same on both sides &mdash; it is set by the source. '
    +'What changes is the speed, and therefore the wavelength. '
    +(B.tir?'<b>Past the critical angle</b> the field does not stop at the boundary: it leaks in and dies '
            +'exponentially, carrying no power away. PhET draws nothing there.'
           :'The crest spacing along the boundary is the same measured from either side. That single '
            +'sentence is Snell&rsquo;s law.')+'</div>';
  return s;
}
function prismReadout(M,st){
  const P=M.prism;
  const nSegs=P.bundles.reduce((a,b)=>a+b.tr.segs.length,0);
  let s='<div class="rname">the prism<small>PhET&rsquo;s Prisms screen</small></div><table>';
  s+=hd('the optics');
  s+=row('environment',isMystery(st.envSub)?'Mystery A or B':fmt(P.nOut,5));
  s+=row('prism',isMystery(st.prismSub)?'Mystery A or B':fmt(P.nIn,5));
  s+=row('critical angle',isFinite(P.tc)?fmt(P.tc*RAD,2)+'&deg;':'&mdash;');
  s+=row('rays traced',P.bundles.length);
  s+=row('segments drawn',nSegs,nSegs>0?'good':'bad');
  if(st.prismId==='triangle'){
    const Dm=prismMinDeviation(P.nOut,P.nIn,P.apex);
    s+=hd('the equilateral prism');
    s+=row('apex angle A','60.00&deg;');
    s+=row('minimum deviation',isFinite(Dm)?fmt(Dm*RAD,3)+'&deg;':'trapped',isFinite(Dm)?'good':'bad');
    s+=row('at &theta;<sub>1</sub>',isFinite(Dm)?fmt((P.apex+Dm)/2*RAD,3)+'&deg;':'&mdash;');
    s+=row('2&theta;<sub>c</sub> (the apex it can pass)',
           isFinite(P.tc)?fmt(2*P.tc*RAD,2)+'&deg;':'&mdash;',
           isFinite(P.tc)&&2*P.tc<P.apex?'bad':'good');
  }
  if(st.white){
    const d4=prismDeviation(envIndex(st,400),prismIndex(st,400),60*DEG,45*DEG);
    const d7=prismDeviation(envIndex(st,700),prismIndex(st,700),60*DEG,45*DEG);
    s+=hd('dispersion at 45&deg; through 60&deg;');
    s+=row('400 nm',isFinite(d4)?fmt(d4*RAD,3)+'&deg;':'trapped');
    s+=row('700 nm',isFinite(d7)?fmt(d7*RAD,3)+'&deg;':'trapped');
    s+=row('spread',isFinite(d4)&&isFinite(d7)?fmt((d4-d7)*RAD,3)+'&deg;':'&mdash;','good');
  }
  s+='</table>';
  s+='<div class="note">Every face is met with the exact intersection and vector Snell. '
    +'PhET&rsquo;s own limits are kept: at most '+PHET.maxSteps+' segments, and a branch is dropped once '
    +'its power falls below '+PHET.powerMin+'.</div>';
  return s;
}
function fresReadout(M,st){
  const B=M.b;
  let s='<div class="rname">the reflected fraction<small>the Fresnel equations, drawn</small></div><table>';
  s+=hd('at &theta;<sub>1</sub> = '+fmt(st.angDeg,2)+'&deg;');
  s+=row('R<sub>s</sub>',pct(B.f.Rs));
  s+=row('R<sub>p</sub>',pct(B.f.Rp));
  s+=row('R unpolarised',pct(0.5*(B.f.Rs+B.f.Rp)));
  s+=row('T<sub>s</sub>',pct(B.f.Ts));
  s+=row('T<sub>p</sub>',pct(B.f.Tp));
  s+=row('R<sub>s</sub> + T<sub>s</sub> &minus; 1',fmt(B.f.Rs+B.f.Ts-1,12),'good');
  s+=row('R<sub>p</sub> + T<sub>p</sub> &minus; 1',fmt(B.f.Rp+B.f.Tp-1,12),'good');
  s+=hd('the two special angles');
  s+=row('Brewster &theta;<sub>B</sub>',fmt(B.tb*RAD,3)+'&deg;');
  s+=row('R<sub>p</sub> there',sigf(fresnel(B.n1,B.n2,B.tb).Rp,3),'good');
  s+=row('&theta;<sub>B</sub> + &theta;<sub>2</sub>',
         fmt((B.tb+refractAngle(B.n1,B.n2,B.tb))*RAD,8)+'&deg;','good');
  s+=row('critical &theta;<sub>c</sub>',isFinite(B.tc)?fmt(B.tc*RAD,3)+'&deg;':'&mdash; (n<sub>2</sub> &gt; n<sub>1</sub>)');
  s+=row('R at &theta;<sub>c</sub>',isFinite(B.tc)?fmt(fresnel(B.n1,B.n2,B.tc).Rs,10):'&mdash;',
         isFinite(B.tc)?'good':'');
  s+=row('R at 0&deg;',pct(fresnel(B.n1,B.n2,0).Rs));
  s+=row('((n<sub>1</sub>&minus;n<sub>2</sub>)/(n<sub>1</sub>+n<sub>2</sub>))<sup>2</sup>',
         pct(Math.pow((B.n1-B.n2)/(B.n1+B.n2),2)),'good');
  s+='</table>';
  s+='<div class="note">R + T = 1 is not an approximation and not a normalisation: it is what the '
    +'boundary conditions give, once the transmitted power is counted with the factor '
    +'(n<sub>2</sub> cos&theta;<sub>2</sub>)/(n<sub>1</sub> cos&theta;<sub>1</sub>) that the change of '
    +'beam width and speed demands.</div>';
  return s;
}
function specReadout(M,st){
  const S=M.spec;
  let s='<div class="rname">the spectrum<small>PhET&rsquo;s dispersion model</small></div><table>';
  s+=hd('index at 400 / 650 / 700 nm');
  for(const id of ['water','glass','diamond']){
    const n=subById(id).n;
    s+=row(id,fmt(indexOf(n,400),4)+' / '+fmt(indexOf(n,650),4)+' / '+fmt(indexOf(n,700),4));
  }
  s+=hd('the blend');
  s+=row('BK7 at 650 nm',fmt(sellmeier(650*NM),6));
  s+=row('air at 650 nm',fmt(airIndex(650*NM),8));
  s+=row('BK7 n<sub>d</sub>',fmt(sellmeier(587.5618*NM),6),'good');
  s+=row('BK7 Abbe V<sub>d</sub>',fmt((sellmeier(587.5618*NM)-1)/(sellmeier(486.1327*NM)-sellmeier(656.2725*NM)),4),'good');
  s+=row('blend weight, glass',fmt(blendFraction(1.5),6));
  s+=row('blend weight, diamond',fmt(blendFraction(2.419),6),'bad');
  s+=hd('a '+fmt(st.prismApex,0)+'&deg; prism');
  s+=row('entry angle',fmt(S.thIn*RAD,3)+'&deg;');
  const d4=S.dev[fnIdx(S.lam,400)], d7=S.dev[fnIdx(S.lam,700)];
  s+=row('deviation at 400 nm',isFinite(d4)?fmt(d4*RAD,3)+'&deg;':'trapped',isFinite(d4)?'':'bad');
  s+=row('deviation at 700 nm',isFinite(d7)?fmt(d7*RAD,3)+'&deg;':'trapped',isFinite(d7)?'':'bad');
  s+=row('violet &minus; red',isFinite(d4)&&isFinite(d7)?fmt((d4-d7)*RAD,3)+'&deg;':'&mdash;','good');
  s+='</table>';
  s+='<div class="note">PhET&rsquo;s dispersion is <b>not</b> a fit to each material. It is one curve &mdash; '
    +'BK7 glass &mdash; blended with air so that the result passes through the index you asked for at '
    +'650 nm. Diamond needs a weight of '+fmt(blendFraction(2.419),3)+', i.e. nearly three times BK7&rsquo;s '
    +'own dispersion, so its spread is a model, not a measurement.</div>';
  return s;
}
function fnIdx(arr,x){ let bi=0,bd=Infinity; for(let i=0;i<arr.length;i++){ const d=Math.abs(arr[i]-x); if(d<bd){bd=d;bi=i;} } return bi; }

function bowReadout(M,st){
  const W=M.bow;
  let s='<div class="rname">the rainbow<small>Descartes&rsquo; stationary deviation</small></div><table>';
  s+=hd('the drop');
  s+=row('water, relative index',fmt(W.n,6));
  s+=row('internal reflections k',st.bowK);
  s+=hd('the stationary ray');
  s+=row('impact angle &theta;<sub>i</sub>',fmt(W.thStar*RAD,4)+'&deg;');
  s+=row('deviation D',fmt(W.devStar,4)+'&deg;');
  s+=row('bow radius |180 &minus; D|',fmt(W.angStar,4)+'&deg;','good');
  s+=row('internal incidence',fmt(W.thr*RAD,3)+'&deg;');
  s+=row('critical angle',fmt(W.tc*RAD,3)+'&deg;',W.thr<W.tc?'bad':'good');
  s+=hd('the colours');
  s+=row('primary, 400 nm',fmt(W.bows[1].ang[400],3)+'&deg;');
  s+=row('primary, 700 nm',fmt(W.bows[1].ang[700],3)+'&deg;');
  s+=row('secondary, 400 nm',fmt(W.bows[2].ang[400],3)+'&deg;');
  s+=row('secondary, 700 nm',fmt(W.bows[2].ang[700],3)+'&deg;');
  s+=row('Alexander&rsquo;s band',fmt(W.gap,3)+'&deg;','good');
  s+=hd('how much light');
  s+=row('throughput ('+st.bowPol+')',pct(W.through),'bad');
  s+=row('R at the bounce, s',fmt(W.Rs,8),'good');
  s+=row('  = (k/(k+2))<sup>2</sup>, for any n',fmt(Math.pow(st.bowK/(st.bowK+2),2),8),'good');
  s+=row('R at the bounce, p',fmt(W.Rp,8));
  s+='</table>';
  s+='<div class="note">The internal bounce happens <b>below</b> the critical angle, so it is a partial '
    +'reflection of a few per cent &mdash; which is why a rainbow is faint. It is also close to '
    +'Brewster&rsquo;s angle, which is why it is strongly polarised.</div>';
  return s;
}
function readoutHTML(M,st){
  st=st||ST;
  if(st.view==='bound') return boundReadout(M,st);
  if(st.view==='wave') return waveReadout(M,st);
  if(st.view==='prism') return prismReadout(M,st);
  if(st.view==='fres') return fresReadout(M,st);
  if(st.view==='spec') return specReadout(M,st);
  return bowReadout(M,st);
}

/* ================================================================== *
 *  the equation bar and the tag                                       *
 * ================================================================== */
function eqbarHTML(M,st){
  st=st||ST;
  if(st.view==='bound')
    return '<span class="lhs">n<sub>1</sub> sin&theta;<sub>1</sub></span> = '
      +'<span class="hl">n<sub>2</sub> sin&theta;<sub>2</sub></span>'
      +'<span class="sm">Snell&rsquo;s law &mdash; and where n<sub>1</sub>sin&theta;<sub>1</sub> exceeds '
      +'n<sub>2</sub> there is no &theta;<sub>2</sub> at all, which is total internal reflection</span>';
  if(st.view==='wave')
    return '<span class="lhs">&lambda;<sub>1</sub>/sin&theta;<sub>1</sub></span> = '
      +'<span class="hl">&lambda;<sub>2</sub>/sin&theta;<sub>2</sub></span>'
      +' &nbsp;&nbsp;&nbsp; <span class="lhs">&lambda;</span> = <span class="hl2">&lambda;<sub>0</sub>/n</span>'
      +'<span class="sm">the crests have to meet along the boundary. Put &lambda; = &lambda;<sub>0</sub>/n '
      +'into the left-hand statement and Snell&rsquo;s law falls out of it</span>';
  if(st.view==='prism')
    return '<span class="lhs">n = </span><span class="hl">sin((A + D<sub>min</sub>)/2) / sin(A/2)</span>'
      +'<span class="sm">the minimum-deviation law: the traced ray reproduces it to '
      +'6&times;10<sup>&minus;15</sup> degrees, which is how the tracer is checked</span>';
  if(st.view==='fres')
    return '<span class="lhs">R<sub>s</sub></span> = <span class="hl">'
      +'((n<sub>1</sub>cos&theta;<sub>1</sub> &minus; n<sub>2</sub>cos&theta;<sub>2</sub>) / '
      +'(n<sub>1</sub>cos&theta;<sub>1</sub> + n<sub>2</sub>cos&theta;<sub>2</sub>))<sup>2</sup></span>'
      +' &nbsp;&nbsp; <span class="lhs">R + T</span> = <span class="hl2">1</span>'
      +'<span class="sm">the Fresnel equations. R<sub>p</sub> swaps the two indices in the numerator, '
      +'which is why it can vanish and R<sub>s</sub> cannot</span>';
  if(st.view==='spec')
    return '<span class="lhs">n<sup>2</sup>(&lambda;)</span> = <span class="hl">1 + &Sigma; '
      +'B<sub>i</sub>&lambda;<sup>2</sup>/(&lambda;<sup>2</sup> &minus; C<sub>i</sub>)</span>'
      +'<span class="sm">Sellmeier for BK7, blended with Edlen&rsquo;s air so that the curve passes '
      +'through the stated index at 650 nm &mdash; PhET&rsquo;s model, exactly</span>';
  return '<span class="lhs">cos<sup>2</sup>&theta;<sub>i</sub></span> = '
    +'<span class="hl">(n<sup>2</sup> &minus; 1)/(k<sup>2</sup> + 2k)</span>'
    +'<span class="sm">where the deviation stops changing with the impact parameter, so rays pile up: '
    +'42.08&deg; for one internal reflection, 50.89&deg; for two</span>';
}
function tagHTML(M,st){
  st=st||ST;
  if(st.view==='bound') return '<b>the boundary</b> &mdash; PhET&rsquo;s Intro screen';
  if(st.view==='wave') return '<b>the wave</b> &mdash; the same picture, as a field';
  if(st.view==='prism') return '<b>the prism</b> &mdash; PhET&rsquo;s Prisms screen';
  if(st.view==='fres') return '<b>the reflected fraction</b> &mdash; Fresnel, drawn';
  if(st.view==='spec') return '<b>the spectrum</b> &mdash; where the colours come from';
  return '<b>the rainbow</b> &mdash; what the whole file is for';
}
