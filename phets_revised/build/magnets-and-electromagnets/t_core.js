
/* ================================================================== *
 *  selfTest suites, shared by the family.  Reference values labelled  *
 *  (scipy) come from REF: derive.py's printed output, emitted as      *
 *  literals -- dblquad over the current sheet, quad, ellipkm1.        *
 * ================================================================== */
function testCore(T){
  const {ok,close,rel}=T;
  /* cel, K, E against direct quadrature and scipy */
  for(let i=0;;i++){ const r=REF['cel.'+i]; if(!r) break; rel(cel(r[0],r[1],r[2],r[3]),r[4],2e-14,'cel('+r.slice(0,4).join(', ')+') (scipy quad)'); }
  for(const k in REF){ if(k.indexOf('K.')!==0&&k.indexOf('E.')!==0) continue; const r=REF[k];
    rel(k[0]==='K'?ellK(r[0]):ellE(r[0]),r[1],5e-15,k[0]+' at kc = '+r[0]+' (scipy '+(k[0]==='K'?'ellipkm1':'ellipe')+')'); }
  ok(isNaN(cel(0,1,1,1)),'cel refuses kc = 0 (the logarithmic singularity) rather than inventing a value');
  /* Gauss-Legendre: exact to degree 2n-1, and not beyond (so the rule is really the n-point one) */
  for(const n of [16,24]){ const G=gaussLegendre(n), r=REF['gl.err.'+n]; let s=0, s2=0;
    for(let i=0;i<n;i++){ s+=G.w[i]*Math.pow(G.x[i],2*n-2); s2+=G.w[i]*Math.pow(G.x[i],2*n); }
    rel(s,2/(2*n-1),1e-13,n+'-point Gauss-Legendre integrates x^'+(2*n-2)+' exactly');
    if(n===16) rel(s2-2/(2*n+1),r[2],1e-6,'and misses x^'+(2*n)+' by exactly minus the Gauss remainder, '+r[1].toExponential(3)+' (python)');
    else ok(Math.abs(s2-2/(2*n+1))<1e-12,'at n = 24 that remainder ('+r[1].toExponential(2)+') is already down at the rounding level, so nothing is pinned by it'); }

  /* the magnet: the Derby-Olbert closed form against Biot-Savart over the sheet */
  for(let i=0;;i++){ const r=REF['mag.pt.'+i]; if(!r) break; const b=solB(r[0],r[1],MAG_R,MAG_B), n=Math.hypot(r[2],r[3]);
    ok(Math.hypot(b[0]-r[2],b[1]-r[3])<=1e-12*n,'magnet field at (rho, u) = ('+r[0]+', '+r[1]+') equals dblquad over the current sheet (scipy) ['+(Math.hypot(b[0]-r[2],b[1]-r[3])/n).toExponential(1)+']'); }
  for(const k in REF) if(k.indexOf('mag.axis.')===0){ const r=REF[k];
    close(solAxis(r[0],MAG_R,MAG_B),r[1],2e-16,'the on-axis closed form at u = '+r[0]+' (python)');
    close(solB(0,r[0],MAG_R,MAG_B)[1],solAxis(r[0],MAG_R,MAG_B),3e-16,'the general form reduces to it on the axis at u = '+r[0]);
    close(solB(0,r[0],MAG_R,MAG_B)[0],0,0,'and B_rho vanishes on the axis at u = '+r[0]); }
  { const m=REF['mag.geom'];
    close(MAG_L,m[0],0,'the bar is PhET\'s 250 mm long (python)'); close(MAG_R,m[1],0,'and 50 mm across, radius 25');
    close(S_MAX,m[2],0,'with PhET\'s 0-300 G range'); close(MAG_B,MAG_L/2,0,'the half-length is half of it'); }
  close(MU0,REF['MU0'],0,'mu0 = 1.25663706127e-6 N/A^2 (CODATA 2022, NIST)');
  rel(MU0/(4*Math.PI*1e-7),1,1e-9,'which is 4 pi x 1e-7 to nine digits, no longer exactly');
  rel(solB(0,0,MAG_R,MAG_B)[1],REF['mag.centre'],1e-15,'the centre field is cos(alpha) = b/sqrt(b^2 + R^2) of mu0 M (python)');
  rel(solB(0,0,MAG_R,MAG_B)[1],MAG_B/Math.hypot(MAG_B,MAG_R),1e-15,'which is 125/sqrt(125^2 + 25^2) = 0.98058');
  close(solB(0,MAG_B,MAG_R,MAG_B)[1],0.5*(2*MAG_B/Math.hypot(2*MAG_B,MAG_R)),1e-15,'at a pole face the field is half the face-to-face cosine');
  for(const u of [0,80,-110]){ const i=solB(MAG_R*(1-1e-9),u,MAG_R,MAG_B), o=solB(MAG_R*(1+1e-9),u,MAG_R,MAG_B);
    close(i[1]-o[1],1,2e-6,'across the side wall at u = '+u+' B_u jumps by exactly mu0 M (the bound current)');
    close(i[0]-o[0],0,2e-6,'and B_rho is continuous there'); }
  { const on=solB(MAG_R,MAG_B,MAG_R,MAG_B); ok(isFinite(on[0])&&isFinite(on[1])&&Math.hypot(on[0],on[1])>1,'at the rim itself the field is large but finite (nudged off the log singularity)'); }
  for(const [r0,u0] of [[10,40],[60,-90],[30,200]]){ const a=solB(r0,u0,MAG_R,MAG_B), b=solB(r0,-u0,MAG_R,MAG_B);
    close(a[1],b[1],1e-15,'B_u is even in u at ('+r0+', '+u0+')'); close(a[0],-b[0],1e-15,'B_rho is odd in u there'); }
  /* the world frame: rotating the magnet rotates its field; flipping it reverses the field everywhere */
  { const m0={kind:'magnet',x:430,y:333,ang:0,S:225}, th=0.7, m1={kind:'magnet',x:430,y:333,ang:th,S:225};
    for(const [dx,dy] of [[150,40],[-60,90],[20,-200]]){
      const b0=magnetField(m0,430+dx,333+dy,0), px=430+dx*Math.cos(th)-dy*Math.sin(th), py=333+dx*Math.sin(th)+dy*Math.cos(th), b1=magnetField(m1,px,py,0);
      const rx=b0[0]*Math.cos(th)-b0[1]*Math.sin(th), ry=b0[0]*Math.sin(th)+b0[1]*Math.cos(th);
      ok(Math.hypot(b1[0]-rx,b1[1]-ry)<=1e-13*Math.hypot(rx,ry),'a magnet turned by 0.7 rad carries its field round with it ('+dx+', '+dy+')'); }
    const bz=magnetField(m0,500,333,40); ok(Math.abs(bz[2])>0&&Math.abs(magnetField(m0,500,333,0)[2])===0,'off the page the field has a z part; in the page it has none (the page contains the axis)'); }
  for(const tag of ['a','b','flip','inside','nearrim']){ const r=REF['meter.bar.'+tag], src={kind:'magnet',x:430,y:333,ang:r[2],S:225};
    const rd=meterReading(src,r[0],r[1]), B=magnetField(src,r[0],r[1],0), n=Math.hypot(r[3],r[4]);
    ok(rd.Bx===B[0]&&rd.By===B[1]&&rd.B===Math.hypot(B[0],B[1]),'the field meter reads the model itself at its crosshair, bit for bit ('+tag+')');
    ok(Math.hypot(rd.Bx-r[3],rd.By-r[4])<=1e-12*n,'and its B_x, B_y equal derive.py\'s world-frame field at ('+r[0]+', '+r[1]+') (python) ['+(Math.hypot(rd.Bx-r[3],rd.By-r[4])/n).toExponential(1)+']');
    close(rd.ang,Math.atan2(r[4],r[3])*180/Math.PI,1e-12,'and its angle, '+fmt(rd.ang,4)+' degrees'); }
  { const a=REF['meter.bar.a'], f=REF['meter.bar.flip']; close(a[3]+f[3],0,1e-12,'flipped, the reading at (560, 380) is reversed in x (python)'); close(a[4]+f[4],0,1e-12,'and in y'); }
  /* PhET's grid: a sampling of this same field (read from the 1.0.7 build by derive.py) */
  for(const k in REF) if(k.indexOf('phet.sample.')===0){ const r=REF[k], b=solB(r[1],r[0],MAG_R,MAG_B), mine=r[3]===0?b[1]:b[0];
    const tol=k.indexOf('EXTERNAL_NEAR')>0?2.5e-4:(k.indexOf('INTERNAL.10')>0?5e-5:5e-7);
    close(mine,r[2],tol,'PhET\'s grid value '+r[2]+' at ('+r[0]+', '+r[1]+') is this field to '+tol.toExponential(0)+' of mu0 M'); }
  /* the meter's display: PhET's rules (G to 2 decimals, '~ 0 G' below 0.01 G, T in scientific notation) */
  ok(fmtField(17.3975,'G')==='17.40 G','17.3975 G reads "17.40 G"');
  ok(fmtField(0.004,'G')==='~ 0 G'&&fmtField(-0.004,'G')==='~ 0 G','below 0.01 G the meter reads "~ 0 G" (PhET)');
  ok(fmtField(0.05,'G')==='0.05 G'&&fmtField(0.011,'G')==='0.01 G','and just above that threshold it prints the number: 0.05 G, 0.01 G');
  ok(fmtField(0,'G')==='0 G'&&fmtField(0,'T')==='0 T','exactly zero reads 0');
  ok(fmtField(225,'T')==='2.25 × 10^-2 T','225 G reads 2.25 × 10^-2 T');
  ok(fmtField(-0.5,'T')==='-5.00 × 10^-5 T','and signs survive the conversion');
  ok(fmtAngle(83.87771)==='83.88°'&&fmtAngle(NaN)==='—','the angle to two decimals, and a dash where there is no field');
  /* the needle grid: PhET's spacing and brightness rule */
  close(needleAlpha(S_MAX/64),Math.min(1,2*Math.exp(Math.log(1/64)/2.7)),1e-15,'needle brightness 2(|B|/300 G)^(1/2.7) at 300/64 G');
  ok(needleAlpha(300)===1&&needleAlpha(0)===0,'saturating at 1 (it reaches 1 at 300/2^2.7 = '+sigf(300/Math.pow(2,2.7),3)+' G) and 0 without field');
  { const src={kind:'magnet',x:430,y:333,ang:0,S:225}, g=needleGrid(src,0,0,LAYOUT_W,LAYOUT_H);
    ok(g.length===26*15,'one needle every 40 mm over the 1024 x 618 box: 26 x 15 = 390 ('+g.length+')');
    let worst=0; for(const n of g){ const B=magnetField(src,n.x,n.y,0); worst=Math.max(worst,Math.abs(wrapPi(n.ang-Math.atan2(B[1],B[0])))); }
    ok(worst<1e-12,'every needle points along B at its own point'); }
}

/* ---- the DRAWN needles, not just the model ----
   A sign slip in the drawing code would leave every number right and every needle backwards,
   and no assertion on the model could see it (Known-bad: assert on the objects the view
   draws).  These capture the emitted geometry and measure where the north half points. */
function makeGeomME(){
  const ops=[]; let path=[], cur=null; const st={fill:'#000'};
  const c={ops, save(){},restore(){},setTransform(){},translate(){},rotate(){},scale(){},setLineDash(){},
    beginPath(){ path=[]; cur=null; }, moveTo(x,y){ cur=[[x,y]]; path.push(cur); },
    lineTo(x,y){ if(!cur){ cur=[[x,y]]; path.push(cur); } else cur.push([x,y]); },
    closePath(){}, rect(){},
    arc(x,y,r,a0,a1){ const pts=[]; for(let i=0;i<=24;i++){ const t=a0+(a1-a0)*i/24; pts.push([x+r*Math.cos(t),y+r*Math.sin(t)]); } cur=pts; path.push(pts); },
    fill(){ if(path.length) ops.push({fill:st.fill,path:JSON.parse(JSON.stringify(path))}); },
    stroke(){ if(path.length) ops.push({stroke:st.strokeStyle,path:JSON.parse(JSON.stringify(path))}); },
    clip(){}, fillRect(){}, strokeRect(){}, clearRect(){}, fillText(){}, strokeText(){},
    measureText(t){ return {width:(''+t).length*5}; }, createLinearGradient(){ return {addColorStop(){}}; }};
  Object.defineProperty(c,'fillStyle',{get:()=>st.fill,set:v=>st.fill=''+v});
  Object.defineProperty(c,'strokeStyle',{get:()=>st.strokeStyle,set:v=>st.strokeStyle=''+v});
  for(const k of ['lineWidth','globalAlpha','font','textAlign','textBaseline','lineJoin','lineCap']){
    let v; Object.defineProperty(c,k,{get:()=>v,set:x=>v=x}); }
  return c;
}
function testDrawnNeedles(T){
  const {ok,close}=T;
  const src={kind:'magnet',x:430,y:333,ang:0,S:225}, map={s:1,X:x=>x,Y:y=>-y};
  const tipAngle=(c,cx,cy)=>{
    const tri=c.ops.filter(o=>o.fill===COL.north)[0];
    let far=null, d=-1;
    for(const p of tri.path[0]){ const dd=Math.hypot(p[0]-cx,p[1]+cy); if(dd>d){ d=dd; far=p; } }
    return Math.atan2(-(far[1]+cy),far[0]-cx);
  };
  for(const [px,py] of [[625,218],[300,420],[700,333],[430,150]]){
    const B=magnetField(src,px,py,0), th=Math.atan2(B[1],B[0]);
    const c=makeGeomME(); drawCompass(c,map,px,py,th);
    close(wrapPi(tipAngle(c,px,py)-th),0,1e-9,'the drawn compass needle at ('+px+', '+py+') has its north half along B');
  }
  const g=needleGrid(src,0,0,LAYOUT_W,LAYOUT_H);
  let worst=0;
  for(const n of g){ if(n.alpha<0.02) continue; const c=makeGeomME(); drawNeedleField(c,map,[n]);
    worst=Math.max(worst,Math.abs(wrapPi(tipAngle(c,n.x,n.y)-n.ang))); }
  ok(worst<1e-9,'and all '+g.length+' drawn field needles point along B where they stand ['+worst.toExponential(1)+']');
  /* the field itself, once, against the compass rose: N of the magnet the field runs back
     from north to south, so a needle above the bar points the OTHER way to the bar's own north */
  const above=magnetField(src,430,420,0);
  ok(above[0]<0&&Math.abs(above[1])<1e-9,'above the middle of the bar the field points from its north end back to its south');
  const beyond=magnetField(src,700,333,0);
  ok(beyond[0]>0&&Math.abs(beyond[1])<1e-9,'and beyond the north end it points away from the magnet');
}

/* The axis view draws two dashed verticals and calls them the pole faces.  Nothing pinned
   them until a mutant moved them to half their distance and survived, so the check is on the
   DRAWN lines: the vertical strokes that span the plot box must stand exactly where x = +-b
   maps to (Known-bad: if a mutant can only be caught by looking at the picture, the quantity
   is in the wrong layer -- so this measures the picture). */
const MARK_COL='#39415a';
function testAxisMarks(T){
  const {ok,close}=T;
  const W=1400, H=820, c=makeGeomME();
  const M=buildModel();
  drawAxisView(c,W,H,M);
  const L=axisGeo(c,W,H,M), b=L.main, xr=ANA_SRC[M.as.kind].axisRange;
  const X=x=>b.x+b.w*(x+xr)/(2*xr);
  const verts=[];
  for(const o of c.ops){
    if(o.stroke!==MARK_COL) continue;                                      /* the marks' own colour, not the grid's */
    for(const sp of o.path){
      if(sp.length!==2) continue;
      if(Math.abs(sp[0][0]-sp[1][0])>0.01) continue;                       /* vertical */
      if(Math.abs(Math.abs(sp[0][1]-sp[1][1])-b.h)>1.5) continue;          /* full height */
      verts.push(sp[0][0]);
    }
  }
  const want=ANA_SRC[M.as.kind].axisMarks(M.as).map(X);
  ok(verts.length===want.length,'the axis view draws one full-height mark per feature it names ('+verts.length+' of '+want.length+')');
  let worst=0;
  for(const w of want){ let d=1e9; for(const v of verts) d=Math.min(d,Math.abs(v-w)); worst=Math.max(worst,d); }
  ok(worst<0.5,'and each stands where its own x maps to, to half a pixel ['+fmt(worst,3)+']');
  if(M.as.kind==='magnet'){
    /* mu0 H equals B outside and B - mu0 M inside, so it jumps at each face.  It is drawn in
       three pieces for exactly that reason: no segment of it may straddle a face, or the
       picture would draw a line down the discontinuity and call it a field. */
    const xd=px=>(px-b.x)/b.w*2*xr-xr;
    let straddle=0, hseg=0;
    for(const o of c.ops){ if(o.stroke!==COL.struct) continue;
      for(const sp of o.path) for(let i2=1;i2<sp.length;i2++){ hseg++;
        const a2=xd(sp[i2-1][0]), b2=xd(sp[i2][0]);
        for(const face of [-MAG_B,MAG_B]) if((a2-face)*(b2-face)<0) straddle++; } }
    ok(hseg>50&&straddle===0,'no piece of the mu0 H curve crosses a pole face ('+hseg+' segments, '+straddle+' straddling)');
    close(want.length,2,0,'for the magnet that is two marks: the pole faces');
    close(Math.abs(ANA_SRC.magnet.axisMarks(M.as)[0]),MAG_B,0,'at x = -125 mm');
    close(ANA_SRC.magnet.axisMarks(M.as)[1],MAG_B,0,'and +125 mm, the faces themselves');
  }
}

/* ---- the captions say what is drawn, and only that ----
   Known-bad (the far view, and again the lines view): a caption that describes what a
   checkbox has switched off.  These draw the view through the page's own shot context and
   read the text that reaches the canvas. */
function testCaptions(T,withState){
  const {ok}=T;
  /* each page names its own shot context (makeShotME / makeShotMC); take whichever is here */
  const shot=(typeof makeShotMC!=='undefined')?makeShotMC:makeShotME;
  const drawn=()=>{ const c=shot(1400,820); drawView(c,1400,820,buildModel());
    return c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' '); };
  withState({view:'lines',bound:true},()=>ok(/bound current/.test(drawn()),'with the bound current drawn, the lines caption names it'));
  withState({view:'lines',bound:false},()=>ok(!/bound current/.test(drawn()),'and with it switched off, the caption does not'));
  withState({view:'axis',axisH:true},()=>ok(/\u03bc\u2080H/.test(drawn()),'with mu0 H drawn, the axis caption explains it'));
  withState({view:'axis',axisH:false},()=>{ const t=drawn();
    ok(!/\u03bc\u2080H/.test(t),'and with it switched off, the caption is about B alone');
    ok(/dipole/.test(t),'while still saying what the orange curve is'); });
}
