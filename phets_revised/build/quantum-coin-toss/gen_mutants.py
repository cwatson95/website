#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py (every pattern must occur EXACTLY
once in this sim's assembled script).  The engine is shared with
quantum-measurement.html but is re-swept here against THIS file's suite."""
import io, json, os
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
M = [
 # ---- the shared engine, against this file's own suite
 ['mulberry32 increment', "R.s=(R.s+0x6D2B79F5)|0;", "R.s=(R.s+0x6D2B79F3)|0;", 'p'],
 ['mulberry32 first shift 15 -> 16', "let t=Math.imul(R.s^(R.s>>>15),1|R.s);", "let t=Math.imul(R.s^(R.s>>>16),1|R.s);", 'p'],
 ['mulberry32 divisor 2^32 - 1', "return ((t^(t>>>14))>>>0)/4294967296;", "return ((t^(t>>>14))>>>0)/4294967295;", 'p'],
 ['Stirling 1/12n -> 1/10n', "+1/(12*x)-1/(360*x*x*x)", "+1/(10*x)-1/(360*x*x*x)", 'p'],
 ['Stirling sqrt(2 pi n) loses the 2', "0.5*Math.log(2*Math.PI*x)", "0.5*Math.log(Math.PI*x)", 'p'],
 ['pmf exponent k -> k+1', "+k*Math.log(p)+(N-k)*Math.log1p(-p));", "+(k+1)*Math.log(p)+(N-k)*Math.log1p(-p));", 'p'],
 ['binomial sd forgets (1-p)', "function binomSD(N,p){ return Math.sqrt(N*p*(1-p)); }", "function binomSD(N,p){ return Math.sqrt(N*p); }", 'p'],
 ['chi-square bins merged at 4', "if(ce>=5){ bins.push([co,ce]);", "if(ce>=4){ bins.push([co,ce]);", 'p'],
 ['sample variance over M, not M-1', "v:M>1?ss/(M-1):0", "v:M>1?ss/M:0", 'p'],
 ['Wilson-Hilferty 1 + a', "return nu*Math.pow(1-a+z*Math.sqrt(a),3);", "return nu*Math.pow(1+a+z*Math.sqrt(a),3);", 'p'],
 ['a flip takes 1.5 s', "const FLIP_T=1.0;", "const FLIP_T=1.5;", 'p'],
 ['1000 coins instead of 10 000', "const COIN_NS=[10,100,10000];", "const COIN_NS=[10,100,1000];", 'p'],
 ['bias steps of 0.1', "const BIAS_STEP=0.05;", "const BIAS_STEP=0.1;", 'p'],
 ['u < p is TAILS', "const v=rngNext(sc.R)<sc.p?1:0;", "const v=rngNext(sc.R)<sc.p?0:1;", 'p'],
 ['revealing a classical coin re-draws it', "if(c.state==='ready') coinDraw(sc,c);", "if(c.state!=='revealed') coinDraw(sc,c);", 'p'],
 ['a classical flip draws no face', "if(sc.quantum) c.state='ready'; else { coinDraw(sc,c); c.state='hidden'; }", "if(sc.quantum) c.state='ready'; else { c.state='hidden'; }", 'p'],
 ['quantum coins arrive with a face', "c.state=sc.quantum?'ready':(sc.startsHidden?'hidden':'revealed');", "c.state=sc.quantum?'revealed':(sc.startsHidden?'hidden':'revealed');", 'p'],
 ['bias 0.995 counts as up', "function quantumInit(p){ return p>=1?'up'", "function quantumInit(p){ return p>0.99?'up'", 'p'],
 ['the Born rule sign', "function bornP(r,n){ return 0.5*(1+dot3v(r,n)); }", "function bornP(r,n){ return 0.5*(1-dot3v(r,n)); }", 'p'],
 ['a down outcome is left along +n', "return {up, r:up?[n[0],n[1],n[2]]:[-n[0],-n[1],-n[2]]};", "return {up, r:up?[n[0],n[1],n[2]]:[n[0],n[1],n[2]]};", 'p'],
 ['degrees to radians wrong way', "const DEG=Math.PI/180;", "const DEG=180/Math.PI;", 'p'],
 ['the view keeps its captions off the hint band', "const HINT_H=18;", "const HINT_H=0;", 'p'],
 # ---- the hidden difference
 ['the mixture sits at 1 - 2p', "function mixBloch(p){ return [0,0,2*p-1]; }", "function mixBloch(p){ return [0,0,1-2*p]; }", 'p'],
 ['the superposition loses its 2', "function pureBloch(p){ return [2*Math.sqrt(p*(1-p)),0,2*p-1]; }", "function pureBloch(p){ return [Math.sqrt(p*(1-p)),0,2*p-1]; }", 'p'],
 ['the hidden face measured face-on', "function mixPx(p){ return bornP(mixBloch(p),[1,0,0]); }", "function mixPx(p){ return bornP(mixBloch(p),[0,0,1]); }", 'p'],
 ['purity p^2 + (1-p)', "function mixPurity(p){ return p*p+(1-p)*(1-p); }", "function mixPurity(p){ return p*p+(1-p); }", 'p'],
 ['the quantum coin turned face-on for "sideways"', "for(let i=0;i<n;i++) if(measureAlong(R,rq,[1,0,0]).up) qx++;", "for(let i=0;i<n;i++) if(measureAlong(R,rq,[0,0,1]).up) qx++;", 'p'],
 ['the classical faces drawn with 1 - p', "for(let i=0;i<n;i++) if(rngNext(R)<p) cz++;", "for(let i=0;i<n;i++) if(rngNext(R)<1-p) cz++;", 'p'],
 # ---- UI mutants
 ['UI: a click does not dirty the frame', "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel();", "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ syncPanel();", 'u'],
 ['UI: the loop draws only when advancing', "if(advanced||dirty){", "if(advanced){", 'u'],
 ['UI: clicking the coin does nothing', "if(inBox(x,y,G.B)) return coinToggle(sc,sc.single);", "if(inBox(x,y,G.B)) return true;", 'u'],
 ['UI: the panel does not resync when a flip ends', "if(wasBusy&&!busy){ syncPanel();", "if(wasBusy&&!busy){", 'u'],
 ['UI: reset all keeps the scenes', "st.view=v; resetScenes(); for(const k in MEMO)", "st.view=v; for(const k in MEMO)", 'u'],
 ['UI: the quantum tab shows the classical scene', "function sceneOf(v){ return v==='quantum'?COINS.quantum:COINS.classical; }", "function sceneOf(v){ return COINS.classical; }", 'u'],
 ['UI: the flip frames are not advanced', "const sc=sceneOf(ST.view); const a=coinStep(sc,sc.single,dt), b=coinStep(sc,sc.set,dt); return a||b;", "return false;", 'u'],
]
bad = [(m[0], js.count(m[1])) for m in M if js.count(m[1]) != 1]
for lab, n in bad:
    print('PATTERN COUNT %d: %s' % (n, lab))
assert not bad, 'fix the patterns'
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=1, ensure_ascii=False))
print('%d mutants (%d physics, %d UI)' % (len(M), sum(m[3] == 'p' for m in M), sum(m[3] == 'u' for m in M)))
