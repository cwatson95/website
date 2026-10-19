/* a scratch tail for bringing the parts up: build every view's model and draw it
   into the recording context, and print a few numbers */
const S0=makeScene({getContext:()=>makeShot(1400,820)});
runFor(120);
for(const [k,name] of TABS){
  ST.view=k;
  const M=buildModel();
  if(k==='law'){ let guard=0; while(M.X.pending&&guard++<10){ ST.view=k; } }
  const rc=makeShot(1400,820);
  drawView(rc,1400,820,buildModel());
  const texts=rc.ops.filter(o=>o.op==='text');
  console.log(k+': ops '+rc.ops.length+', texts '+texts.length+', nfront '+M.g.nfront
    +', lam '+M.lam.toFixed(6)+', Nl '+M.Nl.toFixed(4)+', listener u '+M.listener.u.toFixed(5)
    +', amp '+M.listener.amp.toFixed(5));
  const bad=texts.filter(t=>/NaN|undefined|Infinity/.test(t.t));
  if(bad.length) console.log('   BAD TEXT: '+bad.slice(0,5).map(t=>t.t).join(' | '));
  const ent=texts.filter(t=>/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test(t.t));
  if(ent.length) console.log('   ENTITY: '+ent.slice(0,5).map(t=>t.t).join(' | '));
}
ST.view='law';
let n=0;
while(n<8){ const M=buildModel(); if(!M.X.pending) break; n++; }
const ML=buildModel();
for(const r of ML.X.rows) if(r.m) console.log('law '+r.f+' Hz: lam '+r.m.lam.toFixed(6)+' err '+(100*r.m.err).toFixed(4)+' %, pexp '+r.m.pexp.toFixed(4));
console.log('readout/eqbar/tag build: '+[readoutHTML(ML).length,eqbarHTML(ML).length,tagHTML(ML).length].join(' / '));
