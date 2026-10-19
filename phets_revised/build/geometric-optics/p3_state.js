/* ================================================================== *
 *  state, the per-view model, the readout, the equation bar, the tag  *
 * ================================================================== */
const TABS=[['bench','the lens bench'],['mirror','the mirror bench'],
            ['conj','the conjugate curve'],['maker','the lens maker'],
            ['guides','the guides'],['real','the real lens']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a',
           glass:'#2d6f86', glass2:'#3f93ad', ray:'#b8ec4c', virt:'#e8843a',
           obj:'#cd35c4', img:'#5ac8e0', guide:'#e8843a', axis:'#39506b'};
const RO_W=300;
const HINT_H=18;   /* the house #hint (HTML, bottom:11px) owns the bottom-left */

const OBJ_LIST=[{id:'pencil',name:'pencil'},{id:'penguin',name:'penguin'},
                {id:'star',name:'star'},{id:'arrow',name:'arrow'},{id:'light',name:'light'}];
const RAY_LIST=[{id:'marginal',name:'marginal'},{id:'principal',name:'principal'},
                {id:'many',name:'many'},{id:'none',name:'none'}];
const LENS_LIST=[{id:'convex',name:'convex lens'},{id:'concave',name:'concave lens'}];
const MIRROR_LIST=[{id:'concave',name:'concave'},{id:'convex',name:'convex'},{id:'flat',name:'flat'}];
const FCTL_LIST=[{id:'direct',name:'set f directly'},{id:'indirect',name:'set R and n'}];

const DEFAULTS={
  view:'bench',
  /* the optic -- PhET's own defaults and PhET's own two focal-length models */
  lensSurface:'convex', mirrorSurface:'concave', fControl:'indirect',
  lensF:PHET.fLens[2], lensR:PHET.rocLens[2], lensN:PHET.iorLens[2], lensD:PHET.dLens[2],
  mirrorF:PHET.fMirror[2], mirrorR:PHET.rocMirror[2], mirrorD:PHET.dMirror[2],
  /* the object -- PhET's framed-object position on the Lens screen */
  objKind:'pencil', objX:PHET.framedLens[0], objY:PHET.framedLens[1],
  secondOff:PHET.secondOffset,
  /* the drawing */
  rays:'marginal', showF:true, show2F:false, showVirtual:true, showLabels:true,
  showSecond:false, showGuides:false, showRuler:false, screenX:PHET.screenX,
  /* the real lens */
  realEdge:2, realH:0.98, realStop:1.0,
};
const ST=Object.assign({},DEFAULTS);

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function clearMemo(){ for(const k in MEMO) delete MEMO[k]; }

/* ---------------------------------------------- the optic, from the state
   PhET carries TWO focal-length models and keeps them in step: 'direct' sets
   |f| with the index pinned at 1.5, and derives R = 2f(n-1); 'indirect' sets
   |R| and n, and derives |f| = |R|/(2(n-1)).  The sign comes from the surface
   type, never from the slider. */
function lensIndex(st){ return st.fControl==='direct'?PHET.iorDirectLens:st.lensN; }
function lensFocal(st){
  const mag=st.fControl==='direct'?st.lensF:phetFocalFromR(st.lensR,lensIndex(st));
  return (st.lensSurface==='convex'?1:-1)*mag;
}
function lensRadius(st){
  const mag=st.fControl==='direct'?phetRFromFocal(st.lensF,lensIndex(st)):st.lensR;
  return (st.lensSurface==='convex'?1:-1)*mag;
}
function mirrorFocal(st){
  if(st.mirrorSurface==='flat') return PHET.flatF;
  const mag=st.fControl==='direct'?st.mirrorF:phetFocalFromR(st.mirrorR,PHET.iorMirror);
  return (st.mirrorSurface==='concave'?1:-1)*mag;
}
function mirrorRadius(st){
  if(st.mirrorSurface==='flat') return PHET.flatR;
  const mag=st.fControl==='direct'?phetRFromFocal(st.mirrorF,PHET.iorMirror):st.mirrorR;
  return (st.mirrorSurface==='convex'?1:-1)*mag;
}
/* the optic the bench views use */
function opticOf(st,kind){
  if(kind==='mirror') return {kind:'mirror',surface:st.mirrorSurface,f:mirrorFocal(st),
    R:mirrorRadius(st),n:PHET.iorMirror,D:st.mirrorD,flat:st.mirrorSurface==='flat'};
  return {kind:'lens',surface:st.lensSurface,f:lensFocal(st),R:lensRadius(st),
    n:lensIndex(st),D:st.lensD,flat:false};
}
/* the object point, with PhET's two constraints applied */
function objectPoint(st){
  return [clamp(st.objX,-460,-PHET.minObjectDist),clamp(st.objY,-PHET.maxOffAxis,PHET.maxOffAxis)];
}
/* PhET's second point of interest rides on the object.  For the light scene
   its two sources are independent and 46 cm apart in x; that offset is PhET's
   (its lights sit at (-170, 20) and (-124, -20)). */
const LIGHT_DX=PHET.light2[0]-PHET.light1[0];
function secondPoint(st){
  const P=objectPoint(st);
  return st.objKind==='light'?[clamp(P[0]+LIGHT_DX,-460,-PHET.minObjectDist),P[1]+st.secondOff]
                             :[P[0],P[1]+st.secondOff];
}

/* ----------------------------------------------------------- the bench */
function benchRays(op,P,mode,reach){
  const out=[];
  for(const d of rayDirections(mode,P,op.f,op.D)){
    const r=traceRay(op.kind,op.f,op.D,P,d,reach,mode!=='principal');
    if(r) out.push(r);
  }
  return out;
}
function benchModel(st,kind){
  const key=[kind,st.lensSurface,st.mirrorSurface,st.fControl,st.lensF,st.lensR,st.lensN,st.lensD,
             st.mirrorF,st.mirrorR,st.mirrorD,st.objKind,st.objX,st.objY,st.secondOff,
             st.rays,st.showSecond,st.showGuides,st.screenX].join('|');
  return memo('bench'+kind,key,()=>{
    const op=opticOf(st,kind), P=objectPoint(st), dO=-P[0];
    const img=imagePoint(kind,op.f,dO,P[1]);
    const light=(kind==='lens'&&st.objKind==='light');
    /* The drawn world: the object, the optic, the focal points THAT ARE DRAWN,
       and the image when it is anywhere near.  Equal aspect (it is a
       construction in which the ray SLOPES have to read correctly), so the
       frame is quoted on the canvas.  Only marks that are drawn go into the
       extent: a flat mirror's f = 100 000 cm once stretched the frame to 1640
       cm for a 170 cm scene and squeezed the whole picture into a corner, and
       a lens's 2F stretched it whenever the 2F points were switched off. */
    const drawF=!op.flat&&isFinite(op.f)&&Math.abs(op.f)<1e4;
    const fa=drawF?Math.abs(op.f):0;
    const fSides=(kind==='lens')?[-1,1]:((op.f>0)?[-1]:[1]);
    let xs=[P[0],0,-opticSign(kind)*90];
    if(drawF) for(const s of fSides){ xs.push(s*fa); if(st.show2F) xs.push(s*2*fa); }
    if(light) xs.push(st.screenX+30);
    if(isFinite(img.x)&&Math.abs(img.x)<700) xs.push(img.x);
    const xmin=Math.min.apply(null,xs)-20, xmax=Math.max.apply(null,xs)+20;
    let ys=[P[1],-P[1],op.D/2,-op.D/2,60,-60];
    if(isFinite(img.y)&&Math.abs(img.y)<260) ys.push(img.y,-img.y);
    if(light) ys.push(PHET.screenH/2,-PHET.screenH/2);
    if(st.showSecond){ const S=secondPoint(st); ys.push(S[1],-S[1]); }
    const ymin=Math.min.apply(null,ys)-10, ymax=Math.max.apply(null,ys)+10;
    const reach=(xmax-xmin)*1.6;
    const pts=[{P:P,tag:1}];
    if(st.showSecond) pts.push({P:secondPoint(st),tag:2});
    const bundles=pts.map(o=>{
      const dOi=-o.P[0];
      return {tag:o.tag,P:o.P,dO:dOi,img:imagePoint(kind,op.f,dOi,o.P[1]),
              rays:benchRays(op,o.P,st.rays,reach),
              spot:light?lightSpot(st.screenX,op.D,op.f,dOi,o.P[1]):null};
    });
    let guides=null;
    if(kind==='lens'&&st.showGuides){
      guides=pts.map(o=>({tag:o.tag,
        top:guideAngles(op.surface,op.f,op.D,o.P,1),
        bot:guideAngles(op.surface,op.f,op.D,o.P,-1),
        cross:guideCross(op.surface,op.f,op.D,o.P)}));
    }
    const offFrame=!isFinite(img.x)||img.x<xmin||img.x>xmax||Math.abs(img.y)>Math.max(-ymin,ymax);
    return {kind:kind,op:op,P:P,dO:dO,img:img,bundles:bundles,guides:guides,light:light,
            drawF:drawF,fSides:fSides,
            screenX:st.screenX,ext:{xmin:xmin,xmax:xmax,ymin:ymin,ymax:ymax},
            offFrame:offFrame,reach:reach,
            nRays:bundles.length?bundles[0].rays.length:0,
            nThrough:bundles.length?bundles[0].rays.filter(r=>!r.missed).length:0,
            resid:isFinite(img.di)?lensEqResidual(op.f,dO,img.di):0,
            newton:isFinite(img.di)?newtonProduct(op.f,dO):NaN};
  });
}

/* --------------------------------------------------- the conjugate curve */
function conjModel(st){
  const key=[st.lensSurface,st.fControl,st.lensF,st.lensR,st.lensN,st.objX,st.view].join('|');
  return memo('conj',key,()=>{
    const f=lensFocal(st), P=objectPoint(st), dO=-P[0];
    const xlo=PHET.minObjectDist, xhi=420;
    /* both branches of d_i(d_o), sampled away from the pole at d_o = f */
    const br=[];
    const pole=f>0?f:null;
    const push=(a,b)=>{
      const xs=[],ys=[],ms=[];
      const n=320;
      for(let i=0;i<=n;i++){
        const x=a+(b-a)*i/n;
        const di=imageDistance(f,x);
        xs.push(x); ys.push(di); ms.push(-di/x);
      }
      br.push({xs:xs,ys:ys,ms:ms});
    };
    if(pole!==null&&pole>xlo&&pole<xhi){ push(xlo,pole-1e-3); push(pole+1e-3,xhi); }
    else push(xlo,xhi);
    const di=imageDistance(f,dO);
    return {f:f,dO:dO,di:di,m:-di/dO,branches:br,pole:pole,xlo:xlo,xhi:xhi,
            resid:isFinite(di)?lensEqResidual(f,dO,di):0,
            newton:isFinite(di)?newtonProduct(f,dO):NaN,
            virtual:di<0,inside:pole!==null&&dO<pole};
  });
}

/* ------------------------------------------------------- the lens maker */
function makerModel(st){
  const key=[st.lensSurface,st.fControl,st.lensF,st.lensR,st.lensN,st.lensD].join('|');
  return memo('maker',key,()=>{
    const n=lensIndex(st), R=Math.abs(lensRadius(st)), D=st.lensD;
    const f=phetFocalFromR(R,n);
    /* the contour f = const in the (n, R) plane is the straight line
       R = 2 f (n - 1) -- which is why it is worth drawing */
    const levels=[40,60,80,100,120,160,220,300];
    const cons=levels.map(fv=>{
      const xs=[],ys=[];
      for(let i=0;i<=60;i++){
        const nn=PHET.iorLens[0]+(PHET.iorLens[1]-PHET.iorLens[0])*i/60;
        xs.push(nn); ys.push(phetRFromFocal(fv,nn));
      }
      return {f:fv,xs:xs,ys:ys};
    });
    const a=D/2;
    const sagTrue=(a<=R)?R-Math.sqrt(R*R-a*a):NaN;
    const sagDrawn=hollywoodSag(R,D);
    return {n:n,R:R,D:D,f:f,contours:cons,levels:levels,
            sagTrue:sagTrue,sagDrawn:sagDrawn,
            exists:isFinite(sagTrue),
            fThin:fThin(n,R,-R),
            fMax:phetFocalFromR(PHET.rocLens[1],PHET.iorLens[0]),
            fMin:phetFocalFromR(PHET.rocLens[0],PHET.iorLens[1])};
  });
}

/* ------------------------------------------------------------ the guides */
function guidesModel(st){
  const key=[st.lensSurface,st.fControl,st.lensF,st.lensR,st.lensN,st.lensD,st.objX,st.objY].join('|');
  return memo('guides',key,()=>{
    const f=lensFocal(st), D=st.lensD, P=objectPoint(st), surf=st.lensSurface;
    const dO=-P[0];
    const img=imagePoint('lens',f,dO,P[1]);
    const top=guideAngles(surf,f,D,P,1), bot=guideAngles(surf,f,D,P,-1);
    const cross=guideCross(surf,f,D,P);
    const slope=slopeCross(f,D,dO,P[1]);
    const miss=Math.hypot(cross.x-img.x,cross.y-img.y);
    /* the joint limit: shrink the lens AND the object's inclination together.
       The miss is O(e^2), which is measured here rather than asserted. */
    const es=[],ms=[];
    for(let i=0;i<=40;i++){
      const e=Math.pow(10,-2+2*i/40);
      const c=guideCross(surf,f,D*e,[P[0],P[1]*e]);
      const im=imagePoint('lens',f,dO,P[1]*e);
      es.push(e); ms.push(Math.abs(c.x-im.x));
    }
    return {f:f,D:D,P:P,dO:dO,img:img,top:top,bot:bot,cross:cross,slope:slope,
            miss:miss,missPct:100*miss/Math.hypot(img.x,img.y),
            r:guideRatio(f,D),turn:guideTurn(surf,f,D,1),
            ideal:idealTurn(f,dO,P[1],D,1),
            slopeMiss:Math.hypot(slope.x-img.x,slope.y-img.y),
            es:es,ms:ms,surface:surf};
  });
}

/* ----------------------------------------------------------- the real lens */
function realModel(st){
  const key=[st.fControl,st.lensF,st.lensR,st.lensN,st.lensD,st.realEdge,st.realH,st.realStop].join('|');
  return memo('real',key,()=>{
    const n=lensIndex(st), R=Math.abs(lensRadius(st)), D=st.lensD;
    const a=D/2;
    const exists=(a<R);
    const sag=exists?R-Math.sqrt(R*R-a*a):NaN;
    const t=exists?2*sag+st.realEdge:NaN;
    const semi=a;
    const stopA=a*st.realStop;
    const out={n:n,R:R,D:D,a:a,semi:semi,sag:sag,t:t,exists:exists,stop:stopA};
    if(!exists) return out;
    out.fThin=fThin(n,R,-R);
    out.fThick=fThick(n,R,-R,t);
    out.bfd=backFocal(n,R,-R,t);
    out.zPar=t+out.bfd;
    /* the traced fan: rays entering parallel to the axis */
    const hs=[],ls=[],bl=[];
    const NH=48;
    for(let i=1;i<=NH;i++){
      const hh=stopA*i/NH;
      const L=lsaAt(hh,n,R,-R,t,semi);
      if(!isFinite(L)) continue;
      hs.push(hh); ls.push(L); bl.push(blurAt(hh,n,R,-R,t,semi));
    }
    out.hs=hs; out.ls=ls; out.blur=bl;
    out.hMark=stopA*clamp(st.realH,0.02,1);
    out.lsaMark=lsaAt(out.hMark,n,R,-R,t,semi);
    out.blurMark=blurAt(out.hMark,n,R,-R,t,semi);
    out.lsaRim=ls.length?ls[ls.length-1]:NaN;
    out.pctF=100*Math.abs(out.lsaRim)/out.fThick;
    /* the coefficient of the h^2 law, measured at a small height */
    const hsm=stopA*0.02;
    out.c2=lsaAt(hsm,n,R,-R,t,semi)/(hsm*hsm);
    out.ratio=lsaAt(hsm*2,n,R,-R,t,semi)/lsaAt(hsm,n,R,-R,t,semi);
    /* the drawn ray bundle */
    const fan=[];
    const NF=11;
    for(let i=0;i<NF;i++){
      const hh=stopA*(-1+2*i/(NF-1));
      if(Math.abs(hh)<1e-9) continue;
      const r=traceRealLens([hh,-1.6*R],[0,1],n,R,-R,t,semi,false);
      if(r===null) continue;
      const zEnd=out.zPar+Math.max(30,Math.abs(out.lsaRim)*1.4);
      const s=(zEnd-r.p[1])/r.d[1];
      fan.push({pts:r.pts.concat([[r.p[0]+s*r.d[0],zEnd]]),h:hh,
                z:axisCrossing(r.p,r.d)});
    }
    out.fan=fan;
    out.zEnd=out.zPar+Math.max(30,Math.abs(out.lsaRim)*1.4);
    /* the same lens as a mirror of the same radius, for contrast */
    out.mirrorPar=Math.abs(R)/2;
    out.mirrorRim=mirrorMarginalFocus(R,Math.min(stopA,0.999*R));
    return out;
  });
}

function buildModel(st){
  st=st||ST;
  if(st.view==='bench') return benchModel(st,'lens');
  if(st.view==='mirror') return benchModel(st,'mirror');
  if(st.view==='conj') return conjModel(st);
  if(st.view==='maker') return makerModel(st);
  if(st.view==='guides') return guidesModel(st);
  return realModel(st);
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function row(l,v,cls){ return '<tr><td>'+l+'</td><td class="v'+(cls?' '+cls:'')+'">'+v+'</td></tr>'; }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function cm(x,n){ return isFinite(x)?(sigf(x,n===undefined?4:n)+' cm'):'&infin;'; }
function deg(x){ return isFinite(x)?(fmt(x*180/PI,2)+'&deg;'):'&mdash;'; }
function surfName(m){
  if(m.kind==='mirror') return m.op.surface==='flat'?'flat mirror'
    :(m.op.surface==='concave'?'concave mirror':'convex mirror');
  return m.op.surface==='convex'?'convex lens':'concave lens';
}
function benchReadout(M,st){
  const o=M.op, img=M.img;
  let s='<div class="rname">'+surfName(M)+'<small>'+(o.f>0?'converging':'diverging')
    +' &nbsp;|&nbsp; f = '+cm(o.f,4)+'</small></div><table>';
  s+=hd('the optic');
  s+=row('focal length f',cm(o.f,4));
  s+=row('radius R',o.flat?'&infin; (PhET: '+cm(o.R,4)+')':cm(o.R,4));
  s+=row('index n',fmt(o.n,2)+(M.kind==='mirror'?' (PhET&rsquo;s stand-in)':''));
  s+=row('diameter D',cm(o.D,3));
  s+=hd('the object');
  s+=row('d<sub>o</sub>',cm(M.dO,4));
  s+=row('height y<sub>o</sub>',cm(M.P[1],3));
  s+=hd('the image');
  s+=row('d<sub>i</sub>',isFinite(img.di)?cm(img.di,5):'&infin;',isFinite(img.di)?'':'bad');
  s+=row('magnification m',isFinite(img.m)?fmt(img.m,4):'&infin;',img.m<0?'':'good');
  s+=row('kind',isFinite(img.di)?(img.virtual?'virtual, upright':'real, inverted')
    :'at infinity', img.virtual?'bad':'good');
  s+=row('image height',isFinite(img.y)?cm(img.y,4):'&infin;');
  s+=row('at x =',isFinite(img.x)?cm(img.x,5):'&infin;');
  s+=hd('the check');
  s+=row('1/d<sub>o</sub> + 1/d<sub>i</sub> &minus; 1/f',isFinite(img.di)?M.resid.toExponential(1):'0','good');
  s+=row('(d<sub>o</sub>&minus;f)(d<sub>i</sub>&minus;f)',isFinite(M.newton)?sigf(M.newton,6):'&mdash;');
  s+=row('f<sup>2</sup>',sigf(o.f*o.f,6));
  s+=row('rays through the optic',M.nThrough+' of '+M.nRays);
  s+='</table>';
  if(M.light&&M.bundles[0].spot){
    const sp=M.bundles[0].spot;
    s+='<div class="note"><b>light spot</b> '+cm(sp.diameter,3)+' across at y = '+cm(sp.y,3)
      +'. The screen is a geometric shadow &mdash; the brightness PhET prints is its own formula, not radiometry.</div>';
  }
  s+='<div class="note">'+(M.offFrame?'<b>the image is off the frame.</b> ':'')
    +'Sign convention: d<sub>i</sub> &gt; 0 is a real image &mdash; to the <b>right</b> of a lens, '
    +'to the <b>left</b> of a mirror. m &lt; 0 is inverted.</div>';
  return s;
}
function conjReadout(M){
  let s='<div class="rname">the conjugate curve<small>d<sub>i</sub> = f d<sub>o</sub> / (d<sub>o</sub> &minus; f)</small></div><table>';
  s+=hd('this optic');
  s+=row('f',cm(M.f,4));
  s+=row('pole at d<sub>o</sub> =',M.pole===null?'none (diverging)':cm(M.pole,4));
  s+=hd('the live point');
  s+=row('d<sub>o</sub>',cm(M.dO,5));
  s+=row('d<sub>i</sub>',isFinite(M.di)?cm(M.di,5):'&infin;');
  s+=row('m',isFinite(M.m)?fmt(M.m,4):'&infin;');
  s+=row('branch',M.virtual?'virtual':'real',M.virtual?'bad':'good');
  s+=hd('the identities');
  s+=row('1/d<sub>o</sub>+1/d<sub>i</sub>&minus;1/f',isFinite(M.di)?M.resid.toExponential(1):'0','good');
  s+=row('(d<sub>o</sub>&minus;f)(d<sub>i</sub>&minus;f)',isFinite(M.newton)?sigf(M.newton,8):'&mdash;');
  s+=row('f<sup>2</sup>',sigf(M.f*M.f,8));
  s+='</table><div class="note">The curve is a rectangular hyperbola with asymptotes '
    +'d<sub>o</sub> = f and d<sub>i</sub> = f. Newton&rsquo;s form says exactly that: the two '
    +'distances measured <b>from the focal points</b> multiply to f<sup>2</sup>.</div>';
  return s;
}
function makerReadout(M,st){
  let s='<div class="rname">the lens maker<small>f = R / 2(n &minus; 1)</small></div><table>';
  s+=hd('this lens');
  s+=row('index n',fmt(M.n,3));
  s+=row('radius |R|',cm(M.R,4));
  s+=row('focal length |f|',cm(M.f,5));
  s+=row('from 1/f = (n&minus;1)(1/R<sub>1</sub>&minus;1/R<sub>2</sub>)',cm(M.fThin,5),'good');
  s+=row('diameter D',cm(M.D,3));
  s+=hd('what PhET draws');
  s+=row('drawn half-thickness',cm(M.sagDrawn,4),'bad');
  s+=row('true sag of that surface',M.exists?cm(M.sagTrue,4):'does not exist',M.exists?'':'bad');
  s+=row('f/number f/D',fmt(M.f/M.D,3));
  s+=hd('PhET&rsquo;s reachable range');
  s+=row('|f| at n=1.2, R=120',cm(M.fMax,5));
  s+=row('|f| at n=1.8, R=40',cm(M.fMin,5));
  s+='</table><div class="note"><b>Its artwork is not its model.</b> PhET draws the lens with a '
    +'softened sag (D/2)<sup>2</sup>/2(|R|+100), so the shape on screen belongs to no lens in '
    +'particular &mdash; and at R = 40, D = 120 it draws a lens whose surfaces could not meet.</div>';
  return s;
}
function guidesReadout(M){
  let s='<div class="rname">the guides<small>PhET&rsquo;s own construction</small></div><table>';
  s+=hd('the hinge');
  s+=row('r = D/4f',fmt(M.r,5));
  s+=row('the guide&rsquo;s turn',deg(M.turn));
  s+=row('an ideal optic&rsquo;s turn',deg(M.ideal),'good');
  s+=row('difference',deg(M.turn-M.ideal),'bad');
  s+=hd('where they point');
  s+=row('guides cross at x',cm(M.cross.x,5),'bad');
  s+=row('the image is at x',cm(M.img.x,5),'good');
  s+=row('miss',cm(M.miss,3)+' ('+fmt(M.missPct,2)+'%)','bad');
  s+=hd('the slope construction');
  s+=row('same pair, u&prime; = u &minus; h/f',cm(M.slope.x,6),'good');
  s+=row('its miss',M.slopeMiss.toExponential(1)+' cm','good');
  s+='</table><div class="note">PhET turns each arm through a <b>fixed angle</b> where a thin '
    +'optic changes a <b>slope</b>. tan(a+da) = tan a + da(1+tan<sup>2</sup>a), so the two agree '
    +'only when every angle in the picture is small &mdash; shrinking the lens alone leaves the '
    +'miss at 4.5%.</div>';
  return s;
}
function realReadout(M,st){
  if(!M.exists) return '<div class="rname">the real lens<small>this one cannot be built</small></div>'
    +'<div class="note">A sphere of radius '+cm(M.R,4)+' cannot carry a semi-aperture of '
    +cm(M.a,3)+'. PhET&rsquo;s artwork draws it anyway; a ray tracer refuses.</div>';
  let s='<div class="rname">the real lens<small>two spheres, exact Snell at each</small></div><table>';
  s+=hd('the glass');
  s+=row('index n',fmt(M.n,3));
  s+=row('R<sub>1</sub>, R<sub>2</sub>',sigf(M.R,4)+', &minus;'+sigf(M.R,4)+' cm');
  s+=row('sag per surface',cm(M.sag,4));
  s+=row('centre thickness',cm(M.t,4));
  s+=row('semi-aperture',cm(M.stop,4));
  s+=hd('focal lengths');
  s+=row('thin f',cm(M.fThin,5));
  s+=row('thick f',cm(M.fThick,5),'good');
  s+=row('back focal distance',cm(M.bfd,5));
  s+=hd('spherical aberration');
  s+=row('LSA at h = '+sigf(M.hMark,3)+' cm',cm(M.lsaMark,4),'bad');
  s+=row('LSA at the rim',cm(M.lsaRim,4),'bad');
  s+=row('as a fraction of f',fmt(M.pctF,2)+' %','bad');
  s+=row('blur at the paraxial focus',cm(Math.abs(M.blurMark),4));
  s+=row('LSA/h<sup>2</sup> as h&rarr;0',sigf(M.c2,5)+' cm<sup>&minus;1</sup>');
  s+=row('ratio on doubling h',fmt(M.ratio,4)+' (4 = h<sup>2</sup>)','good');
  s+='</table><div class="note">The ideal optic of the other five views has none of this: its '
    +'focus does not depend on where the ray struck it. Here the rim ray crosses '
    +cm(Math.abs(M.lsaRim),3)+' short of the paraxial focus.</div>';
  return s;
}
function readoutHTML(M,st){
  st=st||ST;
  if(st.view==='bench'||st.view==='mirror') return benchReadout(M,st);
  if(st.view==='conj') return conjReadout(M);
  if(st.view==='maker') return makerReadout(M,st);
  if(st.view==='guides') return guidesReadout(M);
  return realReadout(M,st);
}

function eqbarHTML(M,st){
  st=st||ST;
  const E=(lhs,rhs,sm)=>'<span class="lhs">'+lhs+'</span> = <span class="hl">'+rhs+'</span>'
    +'<span class="sm">'+sm+'</span>';
  if(st.view==='bench'||st.view==='mirror')
    return '<span class="lhs">1/d<sub>o</sub> + 1/d<sub>i</sub></span> = <span class="hl">1/f</span>'
      +' &nbsp;&nbsp;&nbsp; <span class="lhs">m</span> = <span class="hl2">&minus;d<sub>i</sub>/d<sub>o</sub></span>'
      +'<span class="sm">the thin-optic equation and its magnification &mdash; exact, not approximated, '
      +'and every drawn ray is bent by u&prime; = u &minus; h/f so that it lands on the image the '
      +'equation gives</span>';
  if(st.view==='conj')
    return E('(d<sub>o</sub> &minus; f)(d<sub>i</sub> &minus; f)','f<sup>2</sup>',
      'Newton&rsquo;s form of the same equation: measure both distances from the focal points and '
      +'their product is f<sup>2</sup>, which is why the curve is a rectangular hyperbola');
  if(st.view==='maker')
    return '<span class="lhs">1/f</span> = <span class="hl">(n &minus; 1)(1/R<sub>1</sub> &minus; 1/R<sub>2</sub>)</span>'
      +' &nbsp;&rarr;&nbsp; <span class="hl2">f = R / 2(n &minus; 1)</span>'
      +'<span class="sm">the lens maker&rsquo;s equation; PhET gives both surfaces the same radius, '
      +'so it collapses to the right-hand form &mdash; and gives a mirror n = 2 so that f = R/2 falls '
      +'out of it too</span>';
  if(st.view==='guides')
    return '<span class="lhs">&theta;<sub>out</sub></span> = <span class="hl">&theta;<sub>in</sub> + &pi; '
      +'&minus; s&middot;2 arctan(D/4f)</span>'
      +'<span class="sm">PhET&rsquo;s guide turns the ray through a fixed angle; the thin optic changes '
      +'its slope by &minus;h/f. The two agree to second order and no further</span>';
  return '<span class="lhs">LSA(h)</span> &asymp; <span class="hl">&minus;C h<sup>2</sup></span>'
    +' &nbsp;&nbsp;&nbsp; <span class="lhs">n<sub>1</sub> sin&theta;<sub>1</sub></span> = '
    +'<span class="hl2">n<sub>2</sub> sin&theta;<sub>2</sub></span>'
    +'<span class="sm">Snell exactly, at two real spherical surfaces: the focus walks in as h<sup>2</sup>, '
    +'which is the third-order aberration the paraxial model throws away</span>';
}

function tagHTML(M,st){
  st=st||ST;
  if(st.view==='bench') return '<b>the lens bench</b> &mdash; PhET&rsquo;s Lens screen';
  if(st.view==='mirror') return '<b>the mirror bench</b> &mdash; PhET&rsquo;s Mirror screen';
  if(st.view==='conj') return '<b>the conjugate curve</b> &mdash; the law, drawn';
  if(st.view==='maker') return '<b>the lens maker</b> &mdash; where f comes from';
  if(st.view==='guides') return '<b>the guides</b> &mdash; PhET&rsquo;s own construction, measured';
  return '<b>the real lens</b> &mdash; the same glass, traced exactly';
}
