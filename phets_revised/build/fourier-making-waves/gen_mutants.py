#!/usr/bin/env python3
"""Write mutants.json, checking that every `old` appears EXACTLY ONCE in the
assembled script.  A pattern that matches twice silently mutates two places and
one that matches zero times is a mutant you think you ran and did not.

Coverage: every leading coefficient, every exponent, every sign, every unit,
every PhET constant, the series branches, the normalisations, the estimator
refinements, and eight UI mutants (the dirty flag, the frame clock, the drag
gate, the resize repaint, the chip sync, the tab class, the step button and
the keyboard nudge)."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
JS = io.open(os.path.join(HERE, '_out', 'run.js'), encoding='utf-8').read()

M = [
    # ---- PhET's constants -------------------------------------------------
    ["NMAX 11 -> 10", "const NMAX=11;", "const NMAX=10;", "p"],
    ["AMAX 1.5 -> 1.4", "const AMAX=1.5;", "const AMAX=1.4;", "p"],
    ["discrete step 0.05 -> 0.04", "const A_STEP=0.05;", "const A_STEP=0.04;", "p"],
    ["game step 0.1 -> 0.2", "const G_STEP=0.1;", "const G_STEP=0.2;", "p"],
    ["game levels 5 -> 4", "const N_LEVELS=5;", "const N_LEVELS=4;", "p"],
    ["f1 440 -> 441 Hz", "const F1=440;", "const F1=441;", "p"],
    ["L 1 -> 2 m", "const LWAVE=1;", "const LWAVE=2;", "p"],
    ["T = 1000/f1 -> 100/f1", "const TPER=1000/F1;", "const TPER=100/F1;", "p"],
    ["k1 = 2pi/L -> pi/L", "const K1=TAU/LWAVE;", "const K1=PI/LWAVE;", "p"],
    ["omega1 = 2pi/T -> pi/T", "const W1=TAU/TPER;", "const W1=PI/TPER;", "p"],
    ["points per curve 1000 -> 200", "const NPTS=1000;", "const NPTS=200;", "p"],
    ["wave-packet k range 24pi -> 20pi", "const WP_KMAX=24*PI;", "const WP_KMAX=20*PI;", "p"],
    ["packet centre default 12pi -> 11pi", "WP_K0_DEF=12*PI;", "WP_K0_DEF=11*PI;", "p"],
    ["packet centre floor 9pi -> 8pi", "WP_K0_MIN=9*PI", "WP_K0_MIN=8*PI", "p"],
    ["packet width default 3pi -> 2pi", "WP_SK_DEF=3*PI;", "WP_SK_DEF=2*PI;", "p"],
    ["packet width ceiling 4pi -> 5pi", "WP_SK_MAX=4*PI", "WP_SK_MAX=5*PI", "p"],
    ["component spacings pi/4 -> pi/3", "const WP_SPACINGS=[0,PI/4,PI/2,PI];",
     "const WP_SPACINGS=[0,PI/3,PI/2,PI];", "p"],
    ["PhET's per-level control counts", "const GAME_CONTROLS=[2,3,5,6,NMAX];",
     "const GAME_CONTROLS=[2,3,4,6,NMAX];", "p"],
    # ---- the preset coefficients -----------------------------------------
    ["triangle: drop the alternating sign",
     "? Math.pow(-1,(n-1)/2)*8/(n*n*PI*PI) : 8/(n*n*PI*PI)));",
     "? 8/(n*n*PI*PI) : 8/(n*n*PI*PI)));", "p"],
    ["triangle cosine: leading 8 -> 4",
     "? Math.pow(-1,(n-1)/2)*8/(n*n*PI*PI) : 8/(n*n*PI*PI)));",
     "? Math.pow(-1,(n-1)/2)*8/(n*n*PI*PI) : 4/(n*n*PI*PI)));", "p"],
    ["triangle: n^2 -> n in the denominator", "*8/(n*n*PI*PI)", "*8/(n*PI*PI)", "p"],
    ["square sine: leading 4 -> 8",
     "? 4/(n*PI) : Math.pow(-1,(n-1)/2)*4/(n*PI)));",
     "? 8/(n*PI) : Math.pow(-1,(n-1)/2)*4/(n*PI)));", "p"],
    ["square cosine: drop the alternating sign",
     "? 4/(n*PI) : Math.pow(-1,(n-1)/2)*4/(n*PI)));",
     "? 4/(n*PI) : 4/(n*PI)));", "p"],
    ["sawtooth: drop the alternating sign", "out.push(Math.pow(-1,n-1)*2/(n*PI));",
     "out.push(2/(n*PI));", "p"],
    ["sawtooth: leading 2 -> 4", "out.push(Math.pow(-1,n-1)*2/(n*PI));",
     "out.push(Math.pow(-1,n-1)*4/(n*PI));", "p"],
    ["wave-packet preset: sigma N/5 -> N/4", "const c=(N+1)/2, s=N/5;",
     "const c=(N+1)/2, s=N/4;", "p"],
    ["wave-packet preset: centre (N+1)/2 -> N/2", "const c=(N+1)/2, s=N/5;",
     "const c=N/2, s=N/5;", "p"],
    ["wave-packet preset: drop the 2 in 2 sigma^2",
     "out.push(Math.exp(-(n-c)*(n-c)/(2*s*s))); }",
     "out.push(Math.exp(-(n-c)*(n-c)/(s*s))); }", "p"],
    # ---- the waveforms ----------------------------------------------------
    ["wrapPi: forget to shift back", "return v-PI; }", "return v; }", "p"],
    ["triangle waveform: 2/pi -> 1/pi", "return (2/PI)*Math.asin(", "return (1/PI)*Math.asin(", "p"],
    ["sawtooth waveform: /pi -> /2pi", "return wrapPi(u)/PI;", "return wrapPi(u)/TAU;", "p"],
    ["<f^2> of a sine: 1/2 -> 1/4", "if(name==='sinusoid') return 0.5;",
     "if(name==='sinusoid') return 0.25;", "p"],
    ["<f^2> of a square: 1 -> 2", "if(name==='square') return 1;\n", "if(name==='square') return 2;\n", "p"],
    ["<f^2> of triangle and saw: 1/3 -> 1/4", "return 1/3;\n", "return 1/4;\n", "p"],
    # ---- the domains ------------------------------------------------------
    ["time domain: omega1 t -> 2 omega1 t", "if(domain==='time') return W1*t;",
     "if(domain==='time') return 2*W1*t;", "p"],
    ["space & time: the sign of the travelling term", "return K1*x-W1*t;", "return K1*x+W1*t;", "p"],
    ["space domain: k1 x -> 2 k1 x", "  return K1*x;\n", "  return 2*K1*x;\n", "p"],
    ["sines and cosines swapped", "return series==='sin'?Math.sin(a):Math.cos(a);",
     "return series==='sin'?Math.cos(a):Math.sin(a);", "p"],
    # ---- Parseval and truncation -----------------------------------------
    ["Parseval: drop the 1/2", "  return 0.5*s;\n}", "  return s;\n}", "p"],
    ["truncation: drop the 1/2 on the captured power",
     "return Math.sqrt(Math.max(0,idealMeanSquare(name)-0.5*s));",
     "return Math.sqrt(Math.max(0,idealMeanSquare(name)-s));", "p"],
    # ---- Gibbs ------------------------------------------------------------
    ["Gibbs peak position: pi/2M -> pi/M", "const u=PI/(2*M); let s=0;",
     "const u=PI/M; let s=0;", "p"],
    ["Gibbs sum: leading 4 -> 2", "s+=4/(PI*(2*m-1))*Math.sin((2*m-1)*u);",
     "s+=2/(PI*(2*m-1))*Math.sin((2*m-1)*u);", "p"],
    ["Gibbs sum: odd order 2m-1 -> 2m+1", "s+=4/(PI*(2*m-1))*Math.sin((2*m-1)*u);",
     "s+=4/(PI*(2*m-1))*Math.sin((2*m+1)*u);", "p"],
    ["the Wilbraham-Gibbs limit (2/pi)Si(pi)", "const GIBBS_PEAK=1.1789797444721672;",
     "const GIBBS_PEAK=1.1889797444721672;", "p"],
    ["the Wilbraham-Gibbs fraction 0.08949", "const GIBBS_FRACTION=0.08948987223608362;",
     "const GIBBS_FRACTION=0.09948987223608362;", "p"],
    ["odd-harmonic count: ceil -> floor", "function oddCount(N){ return Math.ceil(N/2); }",
     "function oddCount(N){ return Math.floor(N/2); }", "p"],
    ["the square's peak window widened to the whole half period",
     "if(name==='square') return [1e-9,PI/2];", "if(name==='square') return [1e-9,PI-1e-9];", "p"],
    ["the sawtooth's peak window moved to the wrong side",
     "if(name==='sawtooth') return [PI/2,PI-1e-9];", "if(name==='sawtooth') return [1e-9,PI/2];", "p"],
    ["parabola refinement: the 1/2 in the vertex", "const d=den!==0?0.5*(y0-y2)/den:0;",
     "const d=den!==0?(y0-y2)/den:0;", "p"],
    ["parabola refinement: the 1/4 in the refined height",
     "return {u:us[bi]+d*du, val:y1-0.25*(y0-y2)*d};",
     "return {u:us[bi]+d*du, val:y1-0.5*(y0-y2)*d};", "p"],
    # ---- analysis ---------------------------------------------------------
    ["direct DFT: drop the factor 2", "    out.push(2*s/ns);", "    out.push(s/ns);", "p"],
    ["FFT twiddle: the sign of the angle", "const ang=-TAU/len,", "const ang=TAU/len,", "p"],
    ["FFT: the sign of the imaginary part for sines",
     "out.push(series==='sin'?-2*im[n]/ns:2*re[n]/ns);",
     "out.push(series==='sin'?2*im[n]/ns:2*re[n]/ns);", "p"],
    ["FFT: the factor 2 for cosines",
     "out.push(series==='sin'?-2*im[n]/ns:2*re[n]/ns);",
     "out.push(series==='sin'?-2*im[n]/ns:re[n]/ns);", "p"],
    ["FFT: accept a length that is not a power of two",
     "if(n!==im.length||n<2||(n&(n-1))!==0) throw",
     "if(n!==im.length||n<2||(n&(n-1))!==1) throw", "p"],
    ["the spectrum view's sample count 256 -> 128", "const SPEC_NS=256;", "const SPEC_NS=128;", "p"],
    # ---- the wave packet --------------------------------------------------
    ["A(k): normalisation sqrt(2 pi) -> sqrt(pi)",
     "/(sk*Math.sqrt(TAU)); }", "/(sk*Math.sqrt(PI)); }", "p"],
    ["A(k): drop the 2 in 2 sigma^2",
     "return Math.exp(-(k-k0)*(k-k0)/(2*sk*sk))", "return Math.exp(-(k-k0)*(k-k0)/(sk*sk))", "p"],
    ["component count: floor(kmax/k1)+1 -> floor(kmax/k1)",
     "return k1>0?Math.floor(WP_KMAX/k1)+1:Infinity;", "return k1>0?Math.floor(WP_KMAX/k1):Infinity;", "p"],
    ["component amplitude: forget the k1 weight", "out.push({k,a:wpAmp(k,k0,sk)*k1,n:j});",
     "out.push({k,a:wpAmp(k,k0,sk),n:j});", "p"],
    ["the transform: drop the 2 in sigma^2 x^2 / 2", "const e=Math.exp(-sk*sk*x*x/2);",
     "const e=Math.exp(-sk*sk*x*x);", "p"],
    ["the continuous envelope: /2 -> /4",
     "function wpEnvelopeContinuous(x,sk){ return Math.exp(-sk*sk*x*x/2); }",
     "function wpEnvelopeContinuous(x,sk){ return Math.exp(-sk*sk*x*x/4); }", "p"],
    ["the discrete envelope: drop the sine part", "return Math.sqrt(c*c+s*s);",
     "return Math.sqrt(c*c);", "p"],
    ["the periodisation period: 2pi/k1 -> pi/k1", "const lam=TAU/k1, mm=", "const lam=PI/k1, mm=", "p"],
    ["the tail bound: drop the sqrt(2) in the erfc argument",
     "return 0.5*erfcApprox(k0/(sk*Math.SQRT2))", "return 0.5*erfcApprox(k0/sk)", "p"],
    ["erfc: the Chebyshev variable t = 1/(1+z/2)", "const z=Math.abs(x), t=1/(1+z/2);",
     "const z=Math.abs(x), t=1/(1+z);", "p"],
    ["erfc: the reflection erfc(-x) = 2 - erfc(x)", "return x>=0?ans:2-ans;", "return ans;", "p"],
    ["erfc: the leading -1.26551223", "-1.26551223+t*(1.00002368", "-1.16551223+t*(1.00002368", "p"],
    # ---- the controls' arithmetic ----------------------------------------
    ["the caliper: L/n -> L*n", "return (domain==='time'?TPER:LWAVE)/n; }",
     "return (domain==='time'?TPER:LWAVE)*n; }", "p"],
    ["snapAmp: round -> floor", "return clamp(Math.round(a/step)*step,-AMAX,AMAX);",
     "return clamp(Math.floor(a/step)*step,-AMAX,AMAX);", "p"],
    ["the bar axis: 2*amax -> amax", "return b.y1-b.h*(a+amax)/(2*amax); }",
     "return b.y1-b.h*(a+amax)/(amax); }", "p"],
    ["the bar inverse: drop the factor 2", "return clamp((b.y1-Y)/b.h*2*amax-amax,-amax,amax);",
     "return clamp((b.y1-Y)/b.h*amax-amax,-amax,amax);", "p"],
    ["the bar centres: (n-0.5)/N -> n/N", "return b.x+b.w*(n-0.5)/N; }", "return b.x+b.w*n/N; }", "p"],
    ["the transform-pair spacing floor 0.4", "const PAIR_K1_MIN=0.4,", "const PAIR_K1_MIN=0.8,", "p"],
    ["the transform-pair spacing ceiling 2 pi", "PAIR_K1_MAX=TAU;", "PAIR_K1_MAX=PI;", "p"],
    ["18 px reserved for the HTML hint", "const HINT_H=18;", "const HINT_H=0;", "p"],
    # ---- the game ---------------------------------------------------------
    ["level n asks for n harmonics -> n+1", "return level<N_LEVELS?level:5+Math.floor(rnd()*(NMAX-5+1));",
     "return level<N_LEVELS?level+1:5+Math.floor(rnd()*(NMAX-5+1));", "p"],
    ["level 5's floor of five harmonics", "return level<N_LEVELS?level:5+Math.floor(rnd()*(NMAX-5+1));",
     "return level<N_LEVELS?level:3+Math.floor(rnd()*(NMAX-5+1));", "p"],
    ["the game generator may return a zero amplitude", "if(a===0) a=-G_STEP;", "if(a===0) a=0;", "p"],
    ["the game generator snaps to the wrong step", "a=Math.round(a/G_STEP)*G_STEP;",
     "a=Math.round(a/A_STEP)*A_STEP;", "p"],
    ["a guess counts when it is merely close", "if(Math.abs(guess[i]-answer[i])>0) return false;",
     "if(Math.abs(guess[i]-answer[i])>0.2) return false;", "p"],
    ["the guess and the Discrete series share one array",
     "function ampArray(){ return ST.view==='game'?GUESS:AMPS; }",
     "function ampArray(){ return AMPS; }", "p"],
    ["PhET's step button: 0.05 ms -> 0.1 ms", "stepOnce(){ ST.t+=0.05; },", "stepOnce(){ ST.t+=0.1; },", "p"],
    ["the pointer release does not end the drag",
     "if(kind==='up'){ const was=S.drag; S.drag=null; return !!was; }",
     "if(kind==='up'){ S.drag=null; return false; }", "p"],
    ["a bar drag does not mark the waveform custom",
     "      if(GEO.view!=='game') ST.preset='custom';", "      if(false) ST.preset='custom';", "p"],
    # ---- UI ---------------------------------------------------------------
    ["the frame loop ignores the dirty flag", "if(advanced||dirty){", "if(advanced){", "u"],
    ["the frame clock never advances", "const dtw=last?Math.min((tm-last)/1000,0.05):0;",
     "const dtw=last?Math.min((tm-last)/1000,0):0;", "u"],
    ["the model clock does not run in space & time",
     "if(ST.view==='harm'&&ST.running&&ST.domain==='both'&&dt>0){ ST.t+=dt; return true; }",
     "if(false){ ST.t+=dt; return true; }", "u"],
    ["a pointermove during a drag is ignored",
     "    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;",
     "    return;", "u"],
    ["a resize does not repaint", "window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });",
     "window.addEventListener('resize',()=>{ resize(); });", "u"],
    ["the chips never re-sync", "      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));",
     "      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip');", "u"],
    ["the tab class never changes", "[].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');",
     "[].forEach.call(tabsEl.children,(b,i)=>b.className='');", "u"],
    ["the arrow keys nudge by the wrong step",
     "      const stp=st.view==='game'?G_STEP:A_STEP;\n      ampArray()[st.sel-1]=snapAmp(ampArray()[st.sel-1]+(e.key==='ArrowUp'?stp:-stp),stp);",
     "      const stp=st.view==='game'?G_STEP:A_STEP;\n      ampArray()[st.sel-1]=snapAmp(ampArray()[st.sel-1]+(e.key==='ArrowUp'?2*stp:-2*stp),stp);", "u"],
    ["the waveform chips do not fill the amplitudes",
     "    if(o.id!=='custom') applyPreset();", "    if(false) applyPreset();", "u"],
    ["a slider does not repaint", "      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });",
     "      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; });", "u"],
]

bad = []
for label, old, new, suite in M:
    n = JS.count(old)
    if n != 1:
        bad.append((label, n))
for label, n in bad:
    print('BAD PATTERN (%d matches): %s' % (n, label))
assert not bad, '%d patterns do not appear exactly once' % len(bad)
io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps([[a, b, c, d] for a, b, c, d in M], indent=1) + '\n')
print('mutants.json: %d mutants (%d physics, %d UI)'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
