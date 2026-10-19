
const R = mulberry32(20260922);
print('rng first: ' + [R(), R(), R()].map(x => x.toFixed(12)).join(' '));
for (const m of ['CO', 'N2', 'O2', 'CO2', 'H2O', 'O3', 'NO2', 'CH4']) {
  const M = normalModes(m);
  print(m + ': ' + M.map(x => x.nu.toFixed(2) + '(' + x.sym + (x.active ? ',IR' : ',--') + ')').join(' '));
}
for (const md of normalModes('CO2')) {
  print('  CO2 ' + md.nu.toFixed(3) + '  chi=' + inversionChi('CO2', md.d) +
        '  d=' + JSON.stringify(md.d.map(p => p.map(v => +v.toFixed(5)))));
}
print('B2 H2O exact ' + JSON.stringify(bentB2Exact('H2O').map(p => p.map(v => +v.toFixed(6)))));
for (const m of ['H2O', 'O3', 'NO2']) {
  const ex = bentB2Exact(m);
  const got = normalModes(m).filter(o => Math.abs(o.d[1][1]) < 1e-7 && Math.abs(o.d[1][0]) > 1e-3)[0];
  const s = Math.sign(got.d[0][0]);
  let e = 0;
  for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++) e = Math.max(e, Math.abs(s * got.d[i][k] - ex[i][k]));
  print('  ' + m + ' B2 err ' + e.toExponential(3) + '  nu ' + got.nu.toFixed(3));
}
print('Be CO ' + BeFromGeometry('CO').toFixed(9) + ' N2 ' + BeFromGeometry('N2').toFixed(9) +
      ' O2 ' + BeFromGeometry('O2').toFixed(9));
print('planck peak ' + planckPeakCm(288).toFixed(6));
print('SB ' + planckBand(1, 6000, 288, 400000).toFixed(6) + ' vs ' +
      (5.670374419e-8 * Math.pow(288, 4)).toFixed(6));
print('window frac ' + (planckBand(1e4 / 13, 1e4 / 8, 288, 20000) / planckBand(1, 6000, 288, 400000)).toFixed(9));
print('absorbed ' + ensembleAbsorb(77003, 20000, 0.5));
const hh = ensembleHold(77004, 20000);
print('hold ' + hh.mean.toFixed(12) + ' sd ' + hh.sd.toFixed(12));
const dd = ensembleDirection(77005, 20000, 12);
print('cos ' + dd.cos.toFixed(12) + ' sin ' + dd.sin.toFixed(12) + ' chi2 ' + dd.chi2.toFixed(4));
print('clockwise ' + (ensembleAbsorb(77006, 20000, 0.5) / 20000).toFixed(6));
print('biased ' + (ensembleAbsorb(77003, 20000, 0.52) / 20000).toFixed(6));
const D = dutyCycle();
print('duty ' + JSON.stringify(D));
/* a short chamber run */
const ch = newChamber(4242, 'CO2', 'infrared');
chamberSetSource(ch, true);
let n = 0;
while (ch.t < 60) { chamberStep(ch, 1 / 60, false); n++; }
print('chamber: fired ' + ch.fired + ' absorbed ' + ch.absorbed + ' passed ' + ch.passed +
      ' reemitted ' + ch.reemitted + ' duty ' + (ch.busyTime / ch.liveTime).toFixed(4));
const ch2 = newChamber(99, 'O3', 'ultraviolet');
chamberSetSource(ch2, true);
while (ch2.t < 20 && ch2.state !== 'broken') chamberStep(ch2, 1 / 60, false);
print('O3 UV: state ' + ch2.state + ' at t=' + ch2.t.toFixed(3) + ' frags ' +
      (ch2.frags ? ch2.frags.map(f => f.mol).join('+') : 'none'));
print('bands: ' + BANDS.map(b => b + '=' + (bandOf(PHET.lam[b]) || 'NONE')).join(' '));
for (const b of BANDS) print('  ' + b + ' E=' + PHOTON[b].E_eV.toExponential(9) + ' eV  nubar=' +
                             PHOTON[b].nubar.toExponential(6));
