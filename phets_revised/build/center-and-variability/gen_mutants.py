#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write mutants.json for center-and-variability.html, checking that every
`old` string occurs EXACTLY ONCE in the built file's script.  mutate.py skips
a pattern that matches zero or two times, and a skipped mutant is one you
believe you ran and did not — so the check belongs here, before the sweep.

Covers, as the PLAYBOOK asks: every leading coefficient, every exponent, every
sign, every convention constant read out of PhET's build, the branch joins
(the odd/even split, the five-kick floor, the closed interval ends), the
random stream, and the UI's dirty flags, snaps, clamps and panel wiring.

    python3 gen_mutants.py         (writes mutants.json, verifies, prints)
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, '..', '..', 'center-and-variability.html'))

M = [
    # ---- PhET's constants, read out of its build --------------------------
    ['PHYSICAL_RANGE max 15 -> 14', 'VMIN:1, VMAX:15', 'VMIN:1, VMAX:14', 'p'],
    ['PHYSICAL_RANGE min 1 -> 2', 'VMIN:1, VMAX:15,', 'VMIN:2, VMAX:15,', 'p'],
    ['VARIABILITY_DRAG_RANGE top 16 -> 15', 'DRAG_LO:0, DRAG_HI:16', 'DRAG_LO:0, DRAG_HI:15', 'p'],
    ['VARIABILITY_DRAG_RANGE floor 0 -> 1', 'DRAG_LO:0, DRAG_HI:16,', 'DRAG_LO:1, DRAG_HI:16,', 'p'],
    ['the five-kick floor for quartiles -> four', 'MIN_KICKS_IQR:5', 'MIN_KICKS_IQR:4', 'p'],
    ["PhET's MAD rounding step 0.1 -> 0.2", 'MAD_STEP:0.1', 'MAD_STEP:0.2', 'p'],
    ['the predict-median snap 0.5 -> 1', 'MEDIAN_SNAP:0.5', 'MEDIAN_SNAP:1', 'p'],
    ['the outlier fence 1.5 -> 2.0 x IQR', 'FENCE:1.5', 'FENCE:2', 'p'],
    ['MAX_KICKS_VALUES top 30 -> 35', 'MAX_KICKS:[5,10,15,20,25,30]', 'MAX_KICKS:[5,10,15,20,25,35]', 'p'],
    ['the Median screen cap 15 -> 20', 'MAX_KICKS_MEDIAN:[5,10,15]', 'MAX_KICKS_MEDIAN:[5,10,20]', 'p'],
    ["kicker 1's peak weight 32 -> 30",
     'K1:[0,0,0,1,3,12,20,32,20,12,3,1,0,0,0]', 'K1:[0,0,0,1,3,12,20,30,20,12,3,1,0,0,0]', 'p'],
    ["kicker 2's tail weight 3 -> 4",
     'K2:[3,5,10,10,25,32,45,65,45,32,25,10,10,5,3]', 'K2:[4,5,10,10,25,32,45,65,45,32,25,10,10,5,3]', 'p'],
    ["kicker 3's peak weight 45 -> 40",
     'K3:[10,25,45,30,18,12,10,5,4,4,4,4,4,4,4]', 'K3:[10,25,40,30,18,12,10,5,4,4,4,4,4,4,4]', 'p'],
    ['kicker 4 is no longer kicker 3 reversed',
     'CAV.K4=CAV.K3.slice().reverse();', 'CAV.K4=CAV.K3.slice();', 'p'],

    # ---- PhET's rounding --------------------------------------------------
    ['roundSymmetric loses its away-from-zero sign',
     'function cavRoundSym(x){ return (x<0?-1:1)*Math.round(Math.abs(x)); }',
     'function cavRoundSym(x){ return Math.round(x); }', 'p'],
    ['roundToInterval multiplies where it should divide',
     'return parseFloat((cavRoundSym(v/iv)*iv).toFixed(cavDecPlaces(iv)));',
     'return parseFloat((cavRoundSym(v*iv)*iv).toFixed(cavDecPlaces(iv)));', 'p'],
    ['numberOfDecimalPlaces off by one',
     'return s.split(\'.\')[1].length;', 'return s.split(\'.\')[1].length+1;', 'p'],

    # ---- the median's two branches ---------------------------------------
    ['the odd-count middle index moves by one',
     'if(n%2===1) return [a[(n-1)/2]];', 'if(n%2===1) return [a[(n-3)/2]];', 'p'],
    ['the even-count pair becomes the same element twice',
     'if(n%2===0&&n>=2) return [a[(n-2)/2],a[n/2]];',
     'if(n%2===0&&n>=2) return [a[(n-2)/2],a[n/2-1]];', 'p'],

    # ---- the quartile rule, the file's headline claim ---------------------
    ["the exclusive split becomes INCLUSIVE (PhET's rule -> Tukey's)",
     'const lower=a.slice(0,t), upper=a.slice(n%2!==0?t+1:t);',
     'const lower=a.slice(0,t+(n%2!==0?1:0)), upper=a.slice(n%2!==0?t:t);', 'p'],
    ['the halves are split at ceil(n/2) instead of floor',
     'const t=Math.floor(n/2);\n  const lower=a.slice(0,t)',
     'const t=Math.ceil(n/2);\n  const lower=a.slice(0,t)', 'p'],
    ['the IQR is Q1 - Q3 instead of Q3 - Q1',
     'return {q1,q3,iqr:q3-q1,lower,upper};', 'return {q1,q3,iqr:q1-q3,lower,upper};', 'p'],
    ["Tukey's hinges become the exclusive split",
     'const t=Math.ceil(n/2);\n  const med=', 'const t=Math.floor(n/2);\n  const med=', 'p'],
    ['Hyndman-Fan type 5 loses its half', 'else if(type===5) h=n*p+0.5;', 'else if(type===5) h=n*p+0.25;', 'p'],
    ['Hyndman-Fan type 6 gets n+2 instead of n+1', 'else if(type===6) h=(n+1)*p;', 'else if(type===6) h=(n+2)*p;', 'p'],
    ['Hyndman-Fan type 7 loses its +1', 'else if(type===7) h=(n-1)*p+1;', 'else if(type===7) h=(n-1)*p;', 'p'],
    ['the quantile interpolation drops its fractional part',
     'return a[lo-1]+fr*(a[hi-1]-a[lo-1]);', 'return a[lo-1];', 'p'],

    # ---- range, MAD, sd, the box plot, the interval tool -------------------
    ['the range becomes max + min', 'return hi-lo;\n}', 'return hi+lo;\n}', 'p'],
    ['the MAD drops its absolute value',
     'let s=0; for(const v of xs) s+=Math.abs(v-m);\n  return s/xs.length;',
     'let s=0; for(const v of xs) s+=(v-m);\n  return s/xs.length;', 'p'],
    ['the MAD divides by n - 1',
     'for(const v of xs) s+=Math.abs(v-m);\n  return s/xs.length;',
     'for(const v of xs) s+=Math.abs(v-m);\n  return s/(xs.length-1);', 'p'],
    ["PhET's MAD loses its per-deviation rounding",
     'for(const v of xs) s+=cavRoundToInterval(Math.abs(v-m),CAV.MAD_STEP);',
     'for(const v of xs) s+=Math.abs(v-m);', 'p'],
    ["PhET's MAD loses its final rounding",
     'return cavRoundToInterval(s/xs.length,CAV.MAD_STEP);', 'return s/xs.length;', 'p'],
    ['the standard deviation ignores its ddof', 'return Math.sqrt(s/(n-d));', 'return Math.sqrt(s/n);', 'p'],
    ['the box-plot fences use Q1 instead of the IQR',
     'const lo=q.q1-CAV.FENCE*q.iqr, hi=q.q3+CAV.FENCE*q.iqr;',
     'const lo=q.q1-CAV.FENCE*q.q1, hi=q.q3+CAV.FENCE*q.q3;', 'p'],
    ['the whiskers exclude the points ON the fences',
     'const inl=xs.filter(v=>v>=lo&&v<=hi);', 'const inl=xs.filter(v=>v>lo&&v<hi);', 'p'],
    ['the interval tool opens both of its ends',
     'let k=0; for(const v of xs) if(v>=a&&v<=b) k++;',
     'let k=0; for(const v of xs) if(v>a&&v<b) k++;', 'p'],
    ['the interval tool stops ordering its handles',
     'const a=Math.min(lo,hi), b=Math.max(lo,hi);\n  let k=0;',
     'const a=lo, b=hi;\n  let k=0;', 'p'],

    # ---- the balance point ------------------------------------------------
    ['the moment from below is scaled by 0.9', 'if(v<c) neg+=c-v; else pos+=v-c;',
     'if(v<c) neg+=0.9*(c-v); else pos+=v-c;', 'p'],
    ['the squared loss becomes a cubed one', 'for(const v of xs){ const d=v-c; s+=d*d; }',
     'for(const v of xs){ const d=v-c; s+=d*d*d; }', 'p'],
    ['the absolute loss drops its absolute value',
     'function cavAbsLoss(xs,c){ let s=0; for(const v of xs) s+=Math.abs(v-c); return s; }',
     'function cavAbsLoss(xs,c){ let s=0; for(const v of xs) s+=(v-c); return s; }', 'p'],

    # ---- the random stream and PhET's sampler ------------------------------
    ["mulberry32's increment moves by one", '0x6D2B79F5', '0x6D2B79F4', 'p'],
    ["mulberry32's first shift 15 -> 16", 'Math.imul(a^(a>>>15),a|1)', 'Math.imul(a^(a>>>16),a|1)', 'p'],
    ["mulberry32's divisor loses one", '/4294967296;', '/4294967295;', 'p'],
    ["sampleProbabilities loses valuesRange.min", 'if(s>=t) return i+CAV.VMIN;', 'if(s>=t) return i;', 'p'],
    ['the sampler draws from 0.9 of the weight total', 'const t=S*rng.next();', 'const t=S*rng.next()*0.9;', 'p'],
    ['the sampler compares the wrong way round', 'for(let i=0;i<w.length;i++){ s+=w[i]; if(s>=t)',
     'for(let i=0;i<w.length;i++){ s+=w[i]; if(s<=t)', 'p'],

    # ---- the population statistics -----------------------------------------
    ['the population mean is 1 % high', 'let mean=0; for(let i=0;i<w.length;i++) mean+=p[i]*xs[i];',
     'let mean=0; for(let i=0;i<w.length;i++) mean+=1.01*p[i]*xs[i];', 'p'],
    ['the population variance loses a factor of the deviation', 'vr+=p[i]*d*d; mad+=p[i]*Math.abs(d); sk+=p[i]*d*d*d;',
     'vr+=p[i]*d; mad+=p[i]*Math.abs(d); sk+=p[i]*d*d*d;', 'p'],
    ['the population skewness loses a factor of the deviation', 'sk+=p[i]*d*d*d;\n  }', 'sk+=p[i]*d*d;\n  }', 'p'],
    ['the population quantile crosses its target too late', 'if(c>=target-1e-15) return xs[i];',
     'if(c>=target+0.1) return xs[i];', 'p'],
    ['g(c) = E|X - c| drops its absolute value',
     'let s=0; for(let i=0;i<P.xs.length;i++) s+=P.p[i]*Math.abs(P.xs[i]-c);',
     'let s=0; for(let i=0;i<P.xs.length;i++) s+=P.p[i]*(P.xs[i]-c);', 'p'],

    # ---- the seeds and the stacking ---------------------------------------
    ["the kicks view's seed moves by one", 'kicks:31771', 'kicks:31772', 'p'],
    ["the spread view's per-kicker seed offset moves by one",
     'return SEEDS.spread+KICKERS.findIndex(k=>k.id===kick)+1;',
     'return SEEDS.spread+KICKERS.findIndex(k=>k.id===kick)+2;', 'p'],
    ['a dragged ball floors instead of rounding',
     'function cavSnapValue(x){ return clamp(cavRoundSym(x),CAV.VMIN,CAV.VMAX); }',
     'function cavSnapValue(x){ return clamp(Math.floor(x),CAV.VMIN,CAV.VMAX); }', 'p'],
    ['the dot plot stacks two rows at a time', 'const k=seen[v]||0; out.push(k); seen[v]=k+1;',
     'const k=seen[v]||0; out.push(k); seen[v]=k+2;', 'p'],
    ['the tallest-stack count is one too many', 'const k=(seen[v]||0)+1; seen[v]=k; if(k>mx) mx=k;',
     'const k=(seen[v]||0)+2; seen[v]=k; if(k>mx) mx=k;', 'p'],
    ['the flight time at 1 m loses a tenth', 'T_FLY:[0.9,1.5]', 'T_FLY:[0.8,1.5]', 'p'],
    ['the flight arc peaks at the wrong height', 'APEX:0.42', 'APEX:0.5', 'p'],
    ['the flight arc is no longer a parabola through both ends',
     'return [b.d*u, 4*CAV.APEX*b.d*u*(1-u)];', 'return [b.d*u, 4*CAV.APEX*b.d*u];', 'p'],

    # ---- the UI -----------------------------------------------------------
    ['the pointer drag forgets its dirty flag',
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=false;", 'u'],
    # The old 'a slider forgets to repaint' mutant is gone with its target: the
    # `dirty=true` beside a refresh() was redundant (refresh() draws
    # unconditionally), so deleting it changed nothing and the mutant survived
    # the full sweep.  The flag is now only where it is load-bearing, and the
    # thing that actually paints is mutated instead.
    ['refresh() stops drawing the canvas',
     "      physEl.innerHTML=DERIV[st.view]||'';\n      S.draw();",
     "      physEl.innerHTML=DERIV[st.view]||'';", 'u'],
    # a regression guard for the drift the survivor sweep exposed: the hit test
    # and the drawing must keep taking the number line's y from one place
    ['the number line moves back to where the hit test used to think it was',
     'function nlLineY(b){ return b.y1-NL_BELOW; }',
     'function nlLineY(b){ return b.y1-22; }', 'p'],
    ['a dragged ball stops snapping to a whole metre',
     'const nv=cavSnapValue(v);\n        if(F.xs[DRAG.idx]===nv) return false;',
     'const nv=clamp(v,CAV.VMIN,CAV.VMAX);\n        if(F.xs[DRAG.idx]===nv) return false;', 'u'],
    ['the interval handle stops clamping to the drag range',
     'const cl=clamp(v,CAV.DRAG_LO,CAV.DRAG_HI);', 'const cl=v;', 'u'],
    ['the predict-median thumb stops snapping to half a metre',
     "if(DRAG.what==='predMed'){\n        const s2=cavRoundToInterval(clamp(v,CAV.VMIN,CAV.VMAX),CAV.MEDIAN_SNAP);",
     "if(DRAG.what==='predMed'){\n        const s2=clamp(v,CAV.VMIN,CAV.VMAX);", 'u'],
    ['kick 5 queues only one kick', 'F.queue+=n; F.sinceKick=CAV.STACK_T;',
     'F.queue+=1; F.sinceKick=CAV.STACK_T;', 'u'],
    ['the field lets one more ball in than its limit',
     'if(F.xs.length+F.air.length>=F.max) return null;',
     'if(F.xs.length+F.air.length>F.max) return null;', 'u'],
    ['a landed ball never joins the data set', 'if(b.t>=b.T) F.xs.push(b.d); else keep.push(b);',
     'if(b.t>=b.T*2) F.xs.push(b.d); else keep.push(b);', 'u'],
    ['the number keys all go to the first view',
     "else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);",
     "else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[0][0]);", 'u'],
    ['reset keeps the kicker it was on',
     "for(const k in DEFAULTS) if(k!=='view') st[k]=DEFAULTS[k];",
     "for(const k in DEFAULTS) if(k!=='view'&&k!=='mKick') st[k]=DEFAULTS[k];", 'u'],
    ['reset stops rebuilding the fields', 'st.view=v; resetWorlds();', 'st.view=v;', 'u'],
    ['the kicks group is shown on every view', "gK.hidden=(v!=='kicks');", 'gK.hidden=false;', 'u'],
    ['the prediction slider is live even when the prediction is off',
     'if(rows.mPredVal) rows.mPredVal.row.hidden=!st.mPredict;',
     'if(rows.mPredVal) rows.mPredVal.row.hidden=false;', 'u'],
    ['the field hit test grabs a ball from anywhere',
     'if(d<Math.max(G.br+5,10)&&d<bestD){ best=i; bestD=d; }',
     'if(d<400&&d<bestD){ best=i; bestD=d; }', 'u'],
]


def main():
    s = io.open(SIM, encoding='utf-8').read()
    js = s.split('<script>', 1)[1].rsplit('</script>', 1)[0]
    bad = []
    for label, old, new, suite in M:
        n = js.count(old)
        if n != 1:
            bad.append('%-56s matches %d times' % (label, n))
        if old == new:
            bad.append('%-56s old == new' % label)
    io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
        json.dumps(M, ensure_ascii=False, indent=0))
    print('%d mutants (%d physics, %d UI)'
          % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
    if bad:
        print('PROBLEMS — mutate.py would SKIP these:')
        for b in bad:
            print('  ' + b)
        raise SystemExit(1)
    print('every `old` occurs exactly once in the built file')


if __name__ == '__main__':
    main()
