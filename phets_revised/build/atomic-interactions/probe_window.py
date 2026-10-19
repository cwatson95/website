#!/usr/bin/env python3
"""Measure exactly what R_LO_FAC = 0.72 -> 0.50 changes, before deciding
whether the surviving mutant is equivalent or a real hole.

Runs the shipped script and the mutated one under jsc, and for each:
  * the separation an inward drag clamps to, per pair;
  * whether that separation is REACHABLE (does any control reach it);
  * the r at which the drawn potential leaves the top of the plot box;
  * a hash of the full display list of all six views.
"""
import io, os, subprocess, json

D = os.path.dirname(os.path.abspath(__file__)) + '/'
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
HTML = os.path.normpath(D + '../../atomic-interactions.html')
REC = os.path.normpath(D + '../../../../projects/simulations/tools/recorder.js')

src = io.open(HTML, encoding='utf-8').read()
js = src.split('<script>', 1)[1].rsplit('</script>', 1)[0]
i = js.rindex('if(typeof document===')
js = js[:i]
rec = io.open(REC, encoding='utf-8').read()
rec = rec.replace("ObjC.import('Foundation');", '')   # jsc has no ObjC bridge

TAIL = r"""
function h32(s){ let h=2166136261; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619);} return (h>>>0).toString(16); }
const out={lo:R_LO_FAC,hi:R_HI_FAC,pairs:{},views:{}};
for(const p of PAIRS){
  Object.assign(ST,DEFAULTS,{pair:p.key});
  setSep(ST,1);            out.pairs[p.key]={floor:ST.r};
  setSep(ST,1e6);          out.pairs[p.key].ceil=ST.r;
  const P=pairInfo(ST);
  out.pairs[p.key].Vfloor=ljV(out.pairs[p.key].floor,P.sig,P.eps)/P.eps;
  /* the smallest r any control other than the drag can produce */
  let best=Infinity;
  for(let rel=-20;rel<=120;rel+=0.5){ ST.rel=rel; releaseAtom(ST); best=Math.min(best,ST.r); }
  out.pairs[p.key].releaseMin=best;
}
/* where the drawn curve leaves the top of the atoms/well box (V/eps = 2.4) */
Object.assign(ST,DEFAULTS);
{ const P=pairInfo(ST); const u=(4+Math.sqrt(16+4*4*2.4))/8;
  out.clipAt=Math.pow(u,-1/6); out.clipPm=P.sig*Math.pow(u,-1/6); }
const SC=[['atoms',{view:'atoms'}],['atoms_c',{view:'atoms',forces:'components',r:300}],
          ['well',{view:'well'}],['well_o',{view:'well',pair:'OO'}],
          ['motion',{view:'motion'}],['small',{view:'small'}],
          ['pairs',{view:'pairs'}],['step',{view:'steppers'}]];
for(const [n,over] of SC){
  Object.assign(ST,DEFAULTS,over); simReset();
  const rc=makeRecorder(1400,820);
  drawView(rc,1400,820,buildModel());
  out.views[n]={ops:rc.ops.length,hash:h32(JSON.stringify(rc.ops))};
}
print(JSON.stringify(out));
"""


def run(lo):
    body = js.replace('const R_LO_FAC=0.72, R_HI_FAC=3.2;',
                      'const R_LO_FAC=%s, R_HI_FAC=3.2;' % lo)
    assert body != js or lo == '0.72'
    tmp = D + '_out/_win.js'
    io.open(tmp, 'w', encoding='utf-8').write(
        'var console={log:print};\n' + body + '\n' + rec + '\n' + TAIL)
    r = subprocess.run([JSC, tmp], capture_output=True, text=True, timeout=600)
    os.remove(tmp)
    if r.returncode != 0:
        raise SystemExit(r.stdout + r.stderr)
    return json.loads(r.stdout.strip().splitlines()[-1])


a, b = run('0.72'), run('0.50')
print('%-8s %-14s %-14s %-14s %-14s %s' %
      ('pair', 'floor 0.72', 'floor 0.50', 'V/eps 0.72', 'V/eps 0.50', 'lowest r a release can reach'))
for k in a['pairs']:
    pa, pb = a['pairs'][k], b['pairs'][k]
    print('%-8s %-14.6f %-14.6f %-14.4g %-14.4g %.4f / %.4f' %
          (k, pa['floor'], pb['floor'], pa['Vfloor'], pb['Vfloor'],
           pa['releaseMin'], pb['releaseMin']))
print()
print('the drawn curve leaves the top of the box at r/sigma = %.6f (%.4f pm for neon)'
      % (a['clipAt'], a['clipPm']))
print()
print('%-10s %-22s %-22s %s' % ('view', '0.72 ops/hash', '0.50 ops/hash', 'same?'))
same = 0
for k in a['views']:
    va, vb = a['views'][k], b['views'][k]
    eq = (va['hash'] == vb['hash'])
    same += eq
    print('%-10s %-22s %-22s %s' % (k, '%d / %s' % (va['ops'], va['hash']),
                                    '%d / %s' % (vb['ops'], vb['hash']),
                                    'identical' if eq else 'DIFFERENT'))
print('\n%d of %d views draw an identical display list' % (same, len(a['views'])))
