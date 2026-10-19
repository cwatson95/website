
/* the far field: the dipole limit taken numerically, and the octupole approach */
function testFar(T,kinds){
  const {ok,close,rel}=T;
  if(kinds.indexOf('magnet')>=0){
    rel(MAG_DIP,REF['mag.dip'],1e-15,'mu0 m/4pi of the bar is S R^2 L/4 per gauss of strength (python)');
    rel(MAG_DIP*4/Math.PI/(MAG_R*MAG_R*MAG_L),1/Math.PI*1,1e-15,'i.e. mu0 m = S pi R^2 L = mu0 M V');
    for(const [where,key] of [['axis','mag.far.axis'],['bis','mag.far.bis']]){
      const d=dipoleLimit('magnet',0,where), r=REF[key];
      rel(d.f1,r[0],1e-13,'r^3 B/dipole at 2 m on the '+where+' (python)');
      rel(d.f2,r[1],1e-13,'at 4 m'); rel(d.f4,r[2],1e-13,'at 8 m');
      close(d.lim,1,1e-8,'and extrapolated (Richardson, the 1/r^2 and 1/r^4 terms removed) it is 1 to '+Math.abs(d.lim-1).toExponential(1)+' on the '+where);
      ok(Math.abs(d.f1-1)>1e-3,'the raw ratio at 2 m is still '+fmt(100*(d.f1-1),3)+' % off, so the limit is doing work');
      const meas=octMeasured('magnet',0,where), cf=octCoef('magnet',0,where);
      rel(cf,REF['mag.oct'][where==='axis'?0:1],1e-14,'the octupole coefficient in closed form on the '+where+', 2(b^2 - 3R^2/4) x '+(where==='axis'?1:-0.75)+' (python)');
      rel(meas,cf,1e-5,'and the approach measured from the exact field gives it back ['+fmt(meas,3)+' vs '+fmt(cf,3)+' mm^2]');
    }
    for(const k in REF) if(k.indexOf('mag.dev.')===0){ const r=REF[k];
      close(farRatio('magnet',0,r[0],'axis')-1,r[1],1e-9,'the departure from the dipole at r = '+r[0]+' mm on the axis is '+sigf(r[1],4)+' (python)');
      close(farRatio('magnet',0,r[0],'bis')-1,r[2],1e-9,'and '+sigf(r[2],4)+' on the bisector'); }
    ok(farRatio('magnet',0,300,'axis')>1&&farRatio('magnet',0,300,'bis')<1,
       'near the magnet the axis reads above the dipole and the bisector below it, as the octupole\'s signs say');
  }
/* #emag */
  if(kinds.indexOf('coil')>=0){
    for(const N of [1,4]){
      close(coilDip(N),N*COIL_A*COIL_A/4,0,'mu0 m/4pi of '+N+' loop(s) is N a^2/4 per unit mu0 I (m = N I pi a^2)');
      for(const where of ['axis','bis']){
        close(dipoleLimit('coil',N,where).lim,1,1e-9,'the '+N+'-loop coil tends to its own point dipole on the '+where);
        rel(octMeasured('coil',N,where),octCoef('coil',N,where),1e-5,'and its octupole coefficient on the '+where+' is 6<x^2> - 3a^2/2 (times -3/4 on the bisector)');
      }
      close(octCoef('coil',N,'axis'),(N===1?-1.5*COIL_A*COIL_A:6*(64+576)/2-1.5*COIL_A*COIL_A),1e-9,'which is '+(N===1?'-3a^2/2 for one loop':'-1830 mm^2 for four at pitch 16'));
    }
  }
/* #endemag */
}
