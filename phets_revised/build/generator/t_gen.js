
/* ================================================================== *
 *  the generator suite: the flux through the pickup coil, its Fourier *
 *  series, and the EMF that follows from it.  Reference values from   *
 *  REF (derive.py): scipy dblquad over the disc, numpy's FFT over 256 *
 *  angles, and a bounded maximiser for the peak.                      *
 * ================================================================== */
function testGen(T){
  const {ok,close,rel}=T;
  /* --- the geometry PhET fixes --- */
  { const g=REF['gen.geom'];
    close(TURB_X,g[0],0,'the turbine stands at PhET\'s x = 285 mm (python)'); close(TURB_Y,g[1],0,'y = 243 mm');
    close(PICK_X,g[2],0,'the pickup coil at x = 520 mm'); close(PICK_Y,g[3],0,'y = 243 mm');
    close(PICK_AMAX,g[4],0,'its largest loop is PhET\'s 70685 mm^2'); }
  close(E_FULL,REF['gen.efull'],0,'full scale is PhET\'s 1.2e5 G mm^2 per frame at 25 frames/s = 0.3 mV (python)');
  close(pickRadius(100),Math.sqrt(PICK_AMAX/Math.PI),1e-12,'the largest coil\'s radius is 150 mm ['+fmt(pickRadius(100),4)+']');
  close(PHET_SP,5,0,'PhET samples every magnet-height/10 = 5 mm');

  /* --- the flux: the 16 x 32 disc rule against scipy's dblquad --- */
  for(const pct of [20,50,100]){
    const rc=pickRadius(pct);
    let worst=0, n=0;
    for(let j=0;;j++){ const r=REF['gen.flux.'+pct+'.'+j]; if(!r) break; n++;
      close(rc,r[1],1e-12,pct+' % of the area is a radius of '+fmt(r[1],4)+' mm (python)');
      worst=Math.max(worst,Math.abs(flux1(r[2],rc)-r[3])); }
    ok(n>=6&&worst<1e-10,'the flux through a '+pct+' % coil equals scipy\'s dblquad at all '+n+' angles ['+worst.toExponential(1)+' G mm^2]');
    /* the rule is converged: doubling either direction does not move it */
    const a=flux1(0.9,rc), b=flux1(0.9,rc,32,64);
    rel(a,b,1e-12,'and doubling the 16 x 32 rule to 32 x 64 leaves it alone at '+pct+' %');
  }
  /* --- the Fourier series: only odd cosines survive --- */
  for(const pct of [20,50,100]){
    const ser=fluxSeries(pickRadius(pct)), h=REF['gen.harm.'+pct];
    [1,3,5,7,9,11].forEach((k,i)=>rel(ser.a[k],h[i],2e-9,'a_'+k+' of the '+pct+' % coil is '+sigf(h[i],6)+' G mm^2 (numpy FFT, 256 angles)'));
    let even=0, sin=0;
    for(let k=0;k<=40;k+=2) even=Math.max(even,Math.abs(ser.a[k]));
    for(let k=1;k<=40;k++) sin=Math.max(sin,Math.abs(ser.b[k]));
    ok(even<1e-11&&sin<1e-11,pct+' %: no even harmonics ('+even.toExponential(1)+') and no sine terms ('+sin.toExponential(1)+'): half a turn reverses the magnet, and Phi is even in theta');
    /* the series really is the flux, at angles it was not sampled at */
    let wr=0; for(const t of [0.17,1.04,2.71,4.9]) wr=Math.max(wr,Math.abs(seriesPhi(ser,t)-flux1(t,ser.rc)));
    ok(wr<1e-9,'and it reproduces the flux between its own samples ['+wr.toExponential(1)+' G mm^2]');
    /* its derivative is the derivative (a central difference, independently) */
    let wd=0; for(const t of [0.3,1.2,2.0,5.5]){ const hh=1e-5;
      wd=Math.max(wd,Math.abs(seriesDPhi(ser,t)-(seriesPhi(ser,t+hh)-seriesPhi(ser,t-hh))/(2*hh))); }
    ok(wd<1e-6,'and dPhi/dtheta term by term matches a central difference of it ['+wd.toExponential(1)+']');
  }
  /* --- the peak: NOT at 90 degrees --- */
  for(const pct of [20,50,100]){
    const ser=fluxSeries(pickRadius(pct)), p=REF['gen.peak.'+pct], pk=emfPeak(ser);
    close(pk.th,p[0],1e-6,'the EMF of a '+pct+' % coil peaks at '+fmt(p[0]*R2D,4)+' degrees, not 90 (python, bounded maximiser)');
    rel(pk.val,p[1],1e-9,'with dPhi/dtheta = '+sigf(p[1],6)+' G mm^2/rad there');
    rel(pk.at90,p[2],1e-9,'and '+sigf(p[2],6)+' at 90 degrees, '+fmt(p[2]/p[1],4)+' of the peak');
    ok(pk.th<Math.PI/2-0.1,'the peak stands well before 90 degrees ('+fmt(pk.th*R2D,1)+'), because the flux is not a cosine');
    rel(Math.max.apply(null,ser.F.map(Math.abs)),p[3],1e-9,'the largest flux over the turn is '+sigf(p[3],6)+' G mm^2');
  }
  /* --- PhET's line sample overestimates the flux --- */
  for(const pct of [20,50,100]){
    const rc=pickRadius(pct), r=REF['gen.phet.'+pct];
    rel(fluxPhet1(0,rc),r[0],1e-9,'PhET\'s line sample of the '+pct+' % coil is '+sigf(r[0],6)+' G mm^2 (python)');
    rel(fluxPhet1(0,rc)/flux1(0,rc),r[2],1e-9,'which is '+fmt(r[2],4)+' of the area integral: high by '+fmt(100*(r[2]-1),1)+' %');
    ok(r[2]>1,'the line sample is always the larger: it takes the field off the page to be the field in it');
  }
  /* the ring average is what the area integral weights */
  { const rc=pickRadius(50);
    close(ringBx(0.6,0),pageBx(0.6,0),1e-12,'at the centre the ring average IS the in-page value');
    ok(Math.abs(ringBx(0.6,rc*0.9))<Math.abs(pageBx(0.6,rc*0.9)),'with the magnet turned, the ring average is the smaller towards the rim');
    close(ringBx(0,rc*0.9),pageBx(0,rc*0.9),1e-12,'but with the magnet in line with the coil they are equal at every radius: the field is then a function of the distance from that axis alone');
    /* and the area integral of the ring average IS the flux (the same number by a second route) */
    const G=gaussLegendre(24); let s=0;
    for(let i=0;i<24;i++){ const q=0.5*rc*(G.x[i]+1); s+=0.5*rc*G.w[i]*ringBx(0.6,q,256)*2*Math.PI*q; }
    rel(s,flux1(0.6,rc),1e-9,'and integrating 2 pi s <B_x>(s) ds gives the same flux ['+sigf(s,8)+']'); }
  /* the face view's two curves are the two estimates: their areas are the numbers themselves */
  for(const th of [0,0.9]){
    const rc=pickRadius(50), C=faceIntegrands(th,rc,4001);
    let se=0; for(let i=1;i<C.s.length;i++) se+=0.5*(C.ex[i]+C.ex[i-1])*(C.s[i]-C.s[i-1]);
    rel(se,flux1(th,rc),1e-5,'the exact strip integrand of the coil-face view integrates to the flux at theta = '+th);
    const m=Math.floor(rc/PHET_SP); let sp=0;
    for(let k=-m;k<=m;k++) sp+=chordPhet(th,k*PHET_SP,rc)*PHET_SP;
    rel(sp,fluxPhet1(th,rc),1e-12,'and PhET\'s, summed at its own 5 mm spacing, is PhET\'s own estimate at theta = '+th);
    let above=0, seen=0;
    for(let i=0;i<C.s.length;i++){ if(Math.abs(C.ex[i])<1e-9) continue; seen++; if(Math.abs(C.ph[i])>=Math.abs(C.ex[i])-1e-12) above++; }
    /* in line with the coil the field over the face depends only on the distance from the
       axis, so PhET's strip is the larger at EVERY height; with the magnet turned the field
       swings about near the rim and a few strips go the other way -- but the total still
       comes out high, which is the claim the view makes */
    if(th===0) ok(seen>100&&above===seen,'PhET\'s strip is the larger at every height when the magnet is in line ('+above+' of '+seen+')');
    else ok(seen>100&&above>0.9*seen,'and at nearly every height when it is turned ('+above+' of '+seen+' at theta = '+th+')');
    ok(Math.abs(fluxPhet1(th,rc))>Math.abs(flux1(th,rc)),'the total is the larger either way at theta = '+th
       +' ('+fmt(100*(fluxPhet1(th,rc)/flux1(th,rc)-1),1)+' % high)');
  }

  /* --- Faraday: EMF = -N omega dPhi/dtheta, in volts --- */
  { const rc=pickRadius(50), ser=fluxSeries(rc), pk=emfPeak(ser), v=REF['gen.volts.default'];
    const e=emfOf(ser,pk.th,2,225,2*Math.PI);
    rel(Math.abs(e),v[0],1e-9,'2 loops, 225 G, 60 RPM: the peak EMF is '+sigf(v[0]*1e3,4)+' mV (python)');
    rel(Math.abs(e)/E_FULL,v[1],1e-9,'which is '+fmt(v[1],4)+' of PhET\'s full scale');
    /* linear in N and in omega, and odd in each */
    for(const N of [1,2,3,4]) rel(emfOf(ser,0.8,N,225,3),N*emfOf(ser,0.8,1,225,3),1e-12,'the EMF is N times one loop\'s at N = '+N);
    for(const om of [0.5,2,7.3]) rel(emfOf(ser,0.8,2,225,om),om*emfOf(ser,0.8,2,225,1),1e-12,'and proportional to omega at omega = '+om);
    close(emfOf(ser,0.8,2,225,-3),-emfOf(ser,0.8,2,225,3),0,'turning the wheel the other way reverses it, exactly');
    for(const t of [0,Math.PI]) close(emfOf(ser,t,2,225,3),0,1e-15,'it vanishes at theta = '+fmt(t,3)+', where the flux is stationary');
    /* the phase: the EMF is the NEGATIVE derivative of the flux, by finite difference of Phi */
    let wp=0;
    for(const t of [0.4,1.1,2.6,4.2,5.9]){ const hh=1e-6, N=3, S=180, om=2.1;
      const dP=(fluxOf(ser,t+hh,N,S)-fluxOf(ser,t-hh,N,S))/(2*hh);
      wp=Math.max(wp,Math.abs(emfOf(ser,t,N,S,om)+om*dP)); }
    ok(wp<1e-12,'and it is -N omega dPhi/dtheta at every angle, against a finite difference of Phi itself ['+wp.toExponential(1)+' V]'); }

  /* --- the normalised current, and the clamp that never bites here --- */
  { close(normOf(0.4*E_FULL),0.4,1e-15,'the normalised current is the EMF against PhET\'s full scale');
    close(normOf(3*E_FULL),1,0,'clamped at 1 above it'); close(normOf(-3*E_FULL),-1,0,'and at -1 below');
    let mx=0, at='';
    for(const N of [1,2,3,4]) for(const a of [20,40,60,80,100]){
      const ser=fluxSeries(pickRadius(a)), pk=emfPeak(ser);
      const om=2*Math.PI*genRPM({N,area:a,strength:100,flow:100})/60;
      const v=Math.abs(emfOf(ser,pk.th,N,S_MAX,om));
      if(v>mx){ mx=v; at=N+' loops at '+a+' %'; }
    }
    ok(mx<E_FULL,'no setting of this page\'s sliders reaches full scale ('+fmt(mx/E_FULL,3)+' at most, '+at+'), so the clamp never bites here');
    ok(mx>0.4*E_FULL,'though it comes within reach of it ('+fmt(mx/E_FULL,3)+'), which is what PhET scaled its full scale to'); }

  /* --- PhET's drag on the wheel --- */
  { const d=REF['gen.drag'], dd=REF['gen.drag.default'];
    close(NA_LO,d[0],0,'the smallest coil is 1 x 20 % = 14137 mm^2 of loop (python)');
    close(NA_HI,d[1],0,'the largest 4 x 100 % = 282740');
    close(DRAG_LO,d[2],1e-15,'so the drag runs from 0.01'); close(DRAG_MAX,d[3],0,'to PhET\'s 0.2');
    close(genDrag(2,50,75),dd[0],1e-15,'at the defaults it is '+fmt(dd[0],4));
    close(genRPM({N:2,area:50,strength:75,flow:100}),dd[1],1e-12,'so full flow turns the wheel at '+fmt(dd[1],2)+' RPM');
    close(genRPM({N:2,area:50,strength:75,flow:0}),0,0,'and a closed faucet turns it not at all');
    ok(genDrag(4,100,100)>genDrag(1,20,100),'a bigger coil drags harder');
    close(genDrag(2,50,0),0,0,'and a magnet of no strength drags not at all'); }

  /* --- the whole chain, from the page's own state --- */
  { const st=clone(ST);
    resetState({view:'gen',flow:100,N:3,area:70,pct:60,th:0.7});
    const R=genReadings(genState(ST));
    close(R.rpm,genRPM(genState(ST)),0,'the readings carry the wheel\'s own speed');
    close(R.S,S_MAX*0.6,1e-13,'and the magnet\'s own strength');
    rel(R.Phi,fluxOf(R.ser,0.7,3,180),1e-15,'the flux is the series at the wheel\'s angle, through all 3 loops');
    rel(R.emf,emfOf(R.ser,0.7,3,180,R.omega),1e-15,'and the EMF is Faraday\'s law at that angle');
    close(R.norm,Math.max(-1,Math.min(1,R.emf/E_FULL)),0,'the normalised current is the EMF against full scale, clamped as PhET clamps it');
    /* stepping the page's clock really does integrate the same law */
    const P0=R.Phi, t0=ST.th, dt=1/600;
    stepLive(dt);
    const P1=genReadings(genState(ST)).Phi;
    ok(ST.th>t0,'stepping the clock turns the wheel forwards');
    const mid=emfOf(R.ser,0.5*(t0+ST.th),3,180,R.omega);
    const e1=Math.abs(-(P1-P0)/dt-mid)/Math.abs(mid);
    rel(-(P1-P0)/dt,mid,1e-4,'and -dPhi/dt over that step is the EMF at the midpoint ['+sigf(-(P1-P0)/dt*1e3,6)+' mV]');
    /* the difference is the midpoint rule's own error, second order in the step: halving the
       step must quarter it, which is the check that the EMF really is the derivative */
    resetState({view:'gen',flow:100,N:3,area:70,pct:60,th:0.7});
    const Q0=genReadings(genState(ST)).Phi, s0=ST.th;
    stepLive(dt/2);
    const Q1=genReadings(genState(ST)).Phi;
    const mid2=emfOf(R.ser,0.5*(s0+ST.th),3,180,R.omega);
    const e2=Math.abs(-(Q1-Q0)/(dt/2)-mid2)/Math.abs(mid2);
    ok(Math.abs(e1/e2-4)<0.2,'and halving the step quarters that error, as a midpoint rule must ['+fmt(e1/e2,3)+']');
    resetState(st);
  }
}

/* ---- the DRAWN generator: the wheel, the water and the voltmeter ----
   The readings could all be right with the picture wrong, so these measure the emitted
   geometry (Known-bad: assert on what is drawn, not only on the model). */
function testGenDrawn(T){
  const {ok,close}=T;
  const map={s:1,X:x=>x,Y:y=>-y};
  /* the wheel's paddles stand at theta + k pi/4 */
  for(const th of [0,0.8,2.5]){
    const c=makeGeomME(); drawWheel(c,map,th);
    const spokes=c.ops.filter(o=>o.stroke==='#5c6478');
    ok(spokes.length===8,'the wheel has eight spokes ('+spokes.length+')');
    const angs=spokes.map(o=>{ const p=o.path[0]; return Math.atan2(-(p[1][1]-p[0][1]),p[1][0]-p[0][0]); });
    let worst=0;
    for(const a of angs){ let d=1e9; for(let k=0;k<8;k++) d=Math.min(d,Math.abs(wrapPi(a-(th+k*Math.PI/4)))); worst=Math.max(worst,d); }
    ok(worst<1e-9,'and they stand at theta + k pi/4 with theta = '+fmt(th,2)+' ['+worst.toExponential(1)+']');
  }
  /* the wheel writes its own speed in the hub, as PhET's does, and only while it turns */
  { const txt=rpm=>{ const c=makeShotMC(1400,820); drawRPM(c,map,rpm);
      return c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' '); };
    ok(txt(0)==='','a wheel at rest writes nothing in its hub');
    ok(txt(57.75).indexOf(fmt(57.75,1))>=0&&txt(57.75).indexOf('RPM')>=0,'a turning one writes its speed to one decimal, with the unit ('+txt(57.75)+')');
    ok(txt(12.3).indexOf('12.3')>=0,'whatever the speed');
    /* and it is painted over the magnet, not under it: the last fill at the hub is its own */
    { const c=makeGeomME(), W=1400, H=820, keep=clone(ST);
      resetState({view:'gen',flow:100,th:0});
      drawGenScreen(c,W,H,buildModel());
      resetState(keep);
      const map2=screenGeo(c,W,H,'gen').map, X=map2.X(TURB_X), Y=map2.Y(TURB_Y);
      let last=null;
      for(const o of c.ops) if(o.fill) for(const sp of o.path){
        const xs=sp.map(q=>q[0]), ys=sp.map(q=>q[1]);
        if(Math.min.apply(null,xs)<=X&&Math.max.apply(null,xs)>=X&&Math.min.apply(null,ys)<=Y&&Math.max.apply(null,ys)>=Y) last=o.fill; }
      ok(last==='rgba(9,12,22,0.9)','the speed disc is the last thing painted at the hub, so the magnet cannot hide it ['+last+']'); } }

  /* the water column: drawn only when the faucet is open, and wider as it opens.  Measured on
     the drawn path, which is the only place the width actually reaches the picture. */
  { const wid=flow=>{ const c=makeGeomME(); drawFaucet(c,map,flow);
      const col=c.ops.filter(o=>o.fill===rgba(COL.water,0.75));
      if(!col.length) return 0;
      const xs=col[0].path[0].map(p=>p[0]);
      return Math.max.apply(null,xs)-Math.min.apply(null,xs); };
    const w=[0,25,50,100].map(wid);
    close(w[0],0,0,'a closed faucet draws no water at all');
    ok(w[3]>w[2]&&w[2]>w[1]&&w[1]>0,'and the column widens with the flow ('+w.map(v=>fmt(v,1)).join(', ')+' mm)');
    close(w[3]-w[1],waterW(100)-waterW(25),1e-9,'in proportion to it: the drawn width is the flow rule itself');
    const c=makeGeomME(); drawFaucet(c,map,60);
    const ys=c.ops.filter(o=>o.fill===rgba(COL.water,0.75))[0].path[0].map(p=>-p[1]);
    const yb=Math.min.apply(null,ys);
    /* where it lands is a property, not a formula: the bottom of the column sits ON the rim */
    close(Math.hypot(FAUCET_X-TURB_X,yb-TURB_Y),WHEEL_R,1e-9,'and it lands on the wheel\'s rim, '+fmt(WHEEL_R,0)+' mm from the hub');
    ok(yb>TURB_Y,'on the upper half of the wheel, where it pushes the paddles down');
    ok(FAUCET_X<TURB_X,'and on the left of it, so the wheel turns the way the angle increases'); }
  /* the drawn coil: its turns are centred on the point the flux is computed for, and the
     electrons ride on those same turns (a coil drawn off its own centre would make every
     number right and the picture a lie) */
  for(const N of [1,2,4]){
    const rc=pickRadius(50), c=makeGeomME();
    drawCoilHalf(c,map,pickLoopsX(N),PICK_X,PICK_Y,rc,PICK_WIRE*2,'front');
    /* a FRONT half runs from its own centre outwards (x from X to X + rx), so the centre is
       its left edge -- the bounding box's middle would be half a turn's width to the right */
    const cen=[];
    for(const o of c.ops) if(o.stroke===COL.copper) for(const sp of o.path){
      const xs=sp.map(q=>q[0]); cen.push(Math.min.apply(null,xs));
    }
    ok(cen.length===N,'the coil draws its '+N+' turn'+(N>1?'s':'')+' ('+cen.length+')');
    if(!cen.length) continue;
    let mean=0; for(const v of cen) mean+=v/cen.length;
    close(mean,PICK_X,1e-9,'centred on the coil at x = '+PICK_X+' mm, where the flux is worked out');
    const e=makeGeomME(); drawElectrons(e,map,pickLoopsX(N),PICK_X,PICK_Y,rc,0.25,4);
    let far=0;
    for(const o of e.ops) if(o.fill===COL.electron) for(const sp of o.path) for(const q of sp){
      let d=1e9; for(const cx of cen) d=Math.min(d,Math.abs(q[0]-cx)); far=Math.max(far,d); }
    /* an electron sits on the front half of its own turn, so at most one turn's drawn
       half-width (COIL_TILT x rc) from that turn's centre, plus its own radius */
    ok(far<=rc*COIL_TILT+4,'and its electrons ride on those turns ['+fmt(far,2)+' mm off at worst, the half-width being '+fmt(rc*COIL_TILT,2)+']');
  }
  /* the indicator stands clear of the coil at every area, whatever its radius */
  for(const a of [20,50,100]){
    const rc=pickRadius(a), P=indicatorPos(rc);
    ok(P.y>PICK_Y+rc,'the indicator rides above the coil at '+a+' % of the area ('+fmt(P.y,0)+' vs its top at '+fmt(PICK_Y+rc,0)+' mm)');
    ok(P.y<LAYOUT_H-40,'and stays on the stage there');
    close(P.x,PICK_X,0,'over the coil\'s own centre');
  }
  /* the voltmeter's needle is the EMF against full scale, x 90 degrees */
  for(const norm of [0,0.4,-0.75,1]){
    const c=makeGeomME(); drawVoltmeter(c,map,500,300,norm*90,norm*E_FULL);
    const nd=c.ops.filter(o=>o.stroke===COL.live)[0];
    ok(!!nd,'the voltmeter draws its needle');
    if(!nd) continue;
    const p=nd.path[0], a=Math.atan2(-(p[1][1]-p[0][1]),p[1][0]-p[0][0]);
    close(a*R2D,90-norm*90,1e-9,'and it stands at '+fmt(90-norm*90,1)+' degrees from +x for EMF/full = '+norm);
  }
  /* the bulb's glass brightens with |EMF| through the named display mapping, and at rest it
     is the unlit colour.  The MODEL brightness is |EMF|/full scale and is asserted above. */
  { const glass=c=>c.ops.filter(o=>o.fill&&o.fill!=='#5c6478'&&o.fill.indexOf('rgba')!==0);
    const shade=b=>{ const c=makeGeomME(); drawBulb(c,map,500,300,b); return glass(c)[0].fill; };
    ok(shade(0)===mix('#1b2130','#ffe38a',0),'the unlit bulb is the dark glass');
    ok(shade(0.81)===mix('#1b2130','#ffe38a',bulbShade(0.81)),'and it mixes towards the lit colour through bulbShade');
    close(bulbShade(0.81),0.9,1e-12,'which is sqrt at 0.81, a display mapping and not the model');
    close(bulbShade(0),0,0,'zero at zero'); close(bulbShade(1),1,0,'and one at full scale');
    ok(bulbShade(0.2)>0.2,'so a fifth of full scale is visible rather than nearly black ('+fmt(bulbShade(0.2),3)+')');
    let mono=true; for(let i=1;i<=20;i++) if(bulbShade(i/20)<=bulbShade((i-1)/20)) mono=false;
    ok(mono,'and it rises all the way'); }
}
