
/* field lines: the seeds carry equal flux, the lines close, and each comes back to the
   mid-plane where the flux says it must (brentq on Psi, derive.py) */
function testLines(T,kinds){
  const {ok,close,rel}=T;
  if(kinds.indexOf('magnet')>=0){
    const F=fieldLinesFor('magnet',0), ls=lineSource('magnet',0);
    rel(F.psiMax,REF['lines.mag.psimax'],1e-12,'the flux through the magnet\'s middle, 2 pi x 306.5965 G mm^2 per G (scipy quad)');
    rel(psiMid(ls,MAG_R),F.psiMax,0,'which is Psi at the wall');
    ok(F.lines.length===MAG_LINES,MAG_LINES+' lines a side');
    let wr=0, wc=0, nOk=0, wseed=0, wflux=0;
    F.lines.forEach((l,i)=>{ const r=REF['lines.mag.'+(i+1)];
      wseed=Math.max(wseed,Math.abs(l.r0/r[1]-1)); wr=Math.max(wr,Math.abs(l.rOut/r[2]-1));
      wflux=Math.max(wflux,Math.abs(psiMid(ls,l.r0)/((i+1)*F.psiMax/(MAG_LINES+1))-1));
      if(l.ok){ nOk++; wc=Math.max(wc,l.close); } });
    ok(nOk===MAG_LINES,'every one of them closes on itself ('+nOk+'/'+MAG_LINES+')');
    ok(wc<2e-5,'the worst closure is '+wc.toExponential(2)+' mm, after a loop metres long');
    ok(wseed<1e-10,'the seeds sit where the flux says (scipy brentq) ['+wseed.toExponential(1)+']');
    ok(wflux<1e-12,'and they carry equal flux, Psi_i = i Psi_max/(n+1) ['+wflux.toExponential(1)+']');
    ok(wr<2e-4,'each line crosses the mid-plane outside within '+wr.toExponential(1)+' of brentq on Psi (scipy)');
    const walls=F.lines.map(l=>l.walls);
    ok(walls.slice(0,5).every(w=>w===0)&&walls.slice(5).every(w=>w===2),
       'the inner five leave through the pole faces, the outer five through the side wall, twice each ('+walls.join(',')+')');
    /* the wall crossing is load-bearing: without it the outer lines miss by a hundredfold */
    { const naive={kind:'magnet',ru:ls.ru,wall:null,sing:ls.sing,aIn:ls.aIn,aOut:ls.aOut};
      const l9=traceLine(naive,F.lines[8].r0);
      ok(!l9.ok||l9.close>50*Math.max(wc,1e-9),'and treating the wall as smooth spoils that line ('+(l9.ok?l9.close.toExponential(2)+' mm':'it never closes')+')'); }
  }
/* #emag */
  if(kinds.indexOf('coil')>=0){
    for(const N of [1,2,3,4]){
      const F=fieldLinesFor('coil',N), ls=lineSource('coil',N);
      rel(F.psiMax,REF['lines.coil.'+N+'.psimax'],1e-12,'the coil\'s flux inside '+N+' loop(s), at the wire\'s inner edge (python)');
      let wr=0, wc=0, nOk=0, wpsi=0;
      F.lines.forEach((l,i)=>{ const r=REF['lines.coil.'+N+'.'+(i+1)];
        wr=Math.max(wr,Math.abs(l.rOut/r[2]-1)); if(l.ok){ nOk++; wc=Math.max(wc,l.close); }
        for(let k=0;k<l.pts.length;k+=17) wpsi=Math.max(wpsi,Math.abs(coilPsi(N,l.pts[k][0],l.pts[k][1])/r[0]-1)); });
      ok(nOk===COIL_LINES,'all '+COIL_LINES+' close for N = '+N);
      ok(wpsi<1e-11,'every vertex sits on its own level set of Psi for N = '+N+' ['+wpsi.toExponential(1)+'] (the Newton projection)');
      ok(wc<5e-4,'closure within '+wc.toExponential(2)+' mm for N = '+N);
      ok(wr<1e-4,'and the outer crossings match brentq on the closed-form Psi for N = '+N+' ['+wr.toExponential(1)+']');
    }
  }
/* #endemag */
}
