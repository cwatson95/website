
/* the current loop, the coil and its supplies */
function testCoil(T){
  const {ok,close,rel}=T;
  for(let i=0;;i++){ const r=REF['loop.pt.'+i]; if(!r) break; const b=loopB(r[0],r[1],COIL_A), n=Math.hypot(r[2],r[3]);
    ok(Math.hypot(b[0]-r[2],b[1]-r[3])<=1e-13*n,'loop field at (rho, z) = ('+r[0]+', '+r[1]+') equals the cancellation-free brute force (scipy) ['+(Math.hypot(b[0]-r[2],b[1]-r[3])/n).toExponential(1)+']');
    if(r[0]>0.1) rel(b[2],r[4],1e-12,'and its flux function Psi there (scipy quad of A_phi)'); }
  for(const k in REF) if(k.indexOf('loop.axis.')===0){ const r=REF[k];
    close(loopAxis(r[0],COIL_A),r[1],1e-18,'the loop on its axis at z = '+r[0]+' is a^2/2(a^2+z^2)^(3/2) (python)');
    close(loopB(0,r[0],COIL_A)[1],r[1],1e-17,'and the general form gives the same there');
    close(loopB(0,r[0],COIL_A)[0],0,0,'with no radial part on the axis'); }
  /* the textbook K,E form of B_rho cancels near the axis: the reason this page uses cel.
     Asserted BOTH ways, so neither the fix nor its reason can be quietly dropped. */
  { const rho=1e-6, z=20, D=(COIL_A+rho)*(COIL_A+rho)+z*z, d2=(COIL_A-rho)*(COIL_A-rho)+z*z, kc=Math.sqrt(d2/D);
    const direct=z/(2*Math.PI*rho*Math.sqrt(D))*(-cel(kc,1,1,1)+(COIL_A*COIL_A+rho*rho+z*z)/d2*cel(kc,1,1,kc*kc));
    const exact=REF['loop.pt.1'][2];
    ok(Math.abs(direct/exact-1)>0.05,'the textbook K,E form for B_rho is '+fmt(100*Math.abs(direct/exact-1),1)+' % wrong at rho = 1e-6 a (scipy): it is not used');
    rel(loopB(rho,z,COIL_A)[0],exact,1e-8,'the cel form is right there'); }
  /* Psi is the flux: int_0^r B_z rho drho over the loop's own plane */
  { const G=gaussLegendre(24);
    for(const r of [10,30,42]){ let s=0; for(let i=0;i<24;i++){ const x=0.5*r*(G.x[i]+1); s+=G.w[i]*loopB(x,0,COIL_A)[1]*x; }
      rel(loopB(r,0,COIL_A)[2],0.5*r*s,1e-12,'Psi('+r+', 0) is the quadrature of B_z rho drho inside it'); } }
  /* the coil: PhET's calibration, computed rather than typed */
  rel(I_MAX,REF['coil.Imax'],1e-14,'the full current, 704.02 A, makes PhET\'s 300 G at the centre of 4 loops (python)');
  for(const N of [1,2,3,4]){ const c={kind:'coil',x:0,y:0,N,I:I_MAX};
    rel(coilField(c,0,0,0)[0],REF['coil.centre.'+N],1e-12,'the centre field of '+N+' loop(s) at full current is '+fmt(REF['coil.centre.'+N],4)+' G (python)'); }
  close(coilField({kind:'coil',x:0,y:0,N:4,I:I_MAX},0,0,0)[0],S_MAX,1e-11,'which is exactly PhET\'s maximum at 4 loops');
  ok(coilField({kind:'coil',x:0,y:0,N:4,I:I_MAX},0,0,0)[0]/coilField({kind:'coil',x:0,y:0,N:1,I:I_MAX},0,0,0)[0]<4,
     'the exact 4-loop coil is 3.39x the single loop at its centre, not 4x: the outer loops are further away (PhET scales it as N)');
  for(const tag of ['a','above','b','centre1']){ const r=REF['meter.em.'+tag], c={kind:'coil',x:400,y:218,N:r[2],I:r[3]};
    const rd=meterReading(c,r[0],r[1]), n=Math.hypot(r[4],r[5])||1;
    ok(Math.hypot(rd.Bx-r[4],rd.By-r[5])<=1e-12*n,'the meter on the coil at ('+r[0]+', '+r[1]+'), N = '+r[2]+', reads derive.py\'s field (python) ['+(Math.hypot(rd.Bx-r[4],rd.By-r[5])/n).toExponential(1)+']'); }
  close(coilField({kind:'coil',x:400,y:218,N:4,I:I_MAX},400,330,0)[1],0,0,'straight above the coil\'s centre the field is along the axis only');
  { const p=coilField({kind:'coil',x:0,y:0,N:3,I:5},30,40,0), m=coilField({kind:'coil',x:0,y:0,N:3,I:-5},30,40,0);
    ok(p[0]===-m[0]&&p[1]===-m[1],'reversing the current reverses the field exactly'); }
  ok(inWire({kind:'coil',x:0,y:0,N:1,I:1},0,COIL_A+3)&&!inWire({kind:'coil',x:0,y:0,N:1,I:1},0,COIL_A-12),'the page knows when the meter is inside the drawn wire');
  /* the continuous-solenoid limit: the loop sum is the midpoint rule for the sheet, O(pitch^2) */
  { const l=64, errs=[];
    for(const N of [4,8,16,32]){ const r=REF['coil.midpt.'+N], p=l/N; let s=0;
      for(let k=0;k<N;k++) s+=loopAxis((k-(N-1)/2)*p,COIL_A); s*=p;
      rel(s,r[1],1e-13,N+' loops over a 64-mm sheet sum to '+fmt(r[1],8)+' (python)'); errs.push(Math.abs(s-r[2])); }
    const ratios=[errs[0]/errs[1],errs[1]/errs[2],errs[2]/errs[3]];
    ok(Math.abs(ratios[2]-4)<0.005&&Math.abs(ratios[0]-4)>Math.abs(ratios[1]-4)&&Math.abs(ratios[1]-4)>Math.abs(ratios[2]-4),
       'halving the pitch quarters the error: '+ratios.map(r=>fmt(r,4)).join(', ')+' -> 4, the midpoint rule\'s O(p^2)');
    rel(REF['coil.midpt.32'][2],solAxis(0,COIL_A,l/2),1e-15,'and the sheet it tends to is the finite solenoid\'s closed form'); }
  /* the supplies */
  close(supplyCurrent({kind:'dc',V:5},0),I_MAX/2,1e-12,'the battery at half its voltage drives half the current');
  close(supplyCurrent({kind:'dc',V:-10},0),-I_MAX,1e-12,'and reversed at -10 V');
  { const s={kind:'ac',pk:50,fp:50}, f=acFreq(s), R=REF['supply'];
    close(DC_VMAX,R[0],0,'the battery runs to +-10 V (PhET, python)');
    close(AC_VMAX,R[1],0,'the AC supply to 110 V (PhET, python)');
    close(AC_F100,R[2],0,'at 1.25 Hz for 100 % frequency (PhET, python)');
    close(f,0.625,1e-15,'so at 50 % it runs at 0.625 Hz');
    close(supplyVoltage(s,1/(4*0.625)),55,1e-12,'and its peak is 55 V');
    { const g=REF['coil.geom'];
      close(COIL_A,g[0],0,'the coil radius is PhET\'s 50 mm (loop area 7854 mm^2)');
      close(COIL_PITCH,g[1],0,'its wire is 16 mm wide, so the turns sit 16 mm apart');
      close(WIRE_R,g[2],0,'half of that is the wire radius'); close(COIL_NMAX,g[3],0,'and there are up to 4 loops'); }
    close(supplyVoltage(s,0),0,1e-13,'starting at zero volts');
    close(supplyVoltage(s,1/(4*f)),55,1e-12,'reaching its peak, 55 V, a quarter period later');
    close(supplyVoltage(s,3/(4*f)),-55,1e-12,'and its trough three quarters in');
    close(supplyCurrent(s,1/(4*f)),I_MAX*0.5,1e-12,'the current follows the voltage, scaled by the supply\'s own full scale (PhET)');
    close(supplyCurrent({kind:'dc',V:10},0),I_MAX,1e-12,'the battery at its own full 10 V drives the full current');
    close(supplyVoltage(s,1/f),supplyVoltage(s,0),1e-12,'and it repeats each period'); }
}
