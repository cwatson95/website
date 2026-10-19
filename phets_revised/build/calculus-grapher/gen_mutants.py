#!/usr/bin/env python3
"""Build mutants.json and check every pattern appears EXACTLY ONCE in the
extracted script.  A pattern that matches twice mutates two places silently;
one that matches zero times is a mutant you think you ran and did not
(tools/mutate.py skips it, but only the count in this file makes that
visible before the sweep).

Every mutant here breaks a constant, a sign or an exponent.  None of them
touches a loop condition that has to terminate: a mutant that turns a bounded
loop into an unbounded one outlives the sweep by hours (BRIEF).
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(HERE, '..', '..', 'calculus-grapher.html')

M = [
    # ---------- PhET's constants ----------
    ["NPTS 1251 -> 1201", "const NPTS=1251;", "const NPTS=1201;", "p"],
    ["dx divides by NPTS, not NPTS-1", "const DX=XLEN/(NPTS-1);", "const DX=XLEN/NPTS;", "p"],
    ["TYPICAL_Y 0.1 -> 0.2", "const TYPICAL_Y=0.1*XLEN;", "const TYPICAL_Y=0.2*XLEN;", "p"],
    ["smoothing sigma 0.005 -> 0.01", "const SMOOTH_SIGMA=0.005*XLEN;", "const SMOOTH_SIGMA=0.01*XLEN;", "p"],
    ["edgeSlopeFactor 0.04 -> 0.06", "const EDGE_SLOPE=0.04*XLEN;", "const EDGE_SLOPE=0.06*XLEN;", "p"],
    ["maxTilt 25 -> 40", "const MAX_TILT=25;", "const MAX_TILT=40;", "p"],
    ["default width 0.2 -> 0.25", "W_DEF=0.2*XLEN;", "W_DEF=0.25*XLEN;", "p"],
    ["y range 2 -> 3", "const Y_MIN=-2, Y_MAX=2;", "const Y_MIN=-3, Y_MAX=3;", "p"],
    ["tangent gauge 8 -> 6", "const SLOPE_MAX=8;", "const SLOPE_MAX=6;", "p"],
    ["area gauge 0.8 -> 0.6", "const AREA_MAX=0.8*XLEN*TYPICAL_Y;", "const AREA_MAX=0.6*XLEN*TYPICAL_Y;", "p"],
    ["undo depth 20 -> 10", "const MAX_UNDO=20;", "const MAX_UNDO=10;", "p"],
    ["freeform click width /40 -> /20", "const FREEFORM_W=XLEN/40;", "const FREEFORM_W=XLEN/20;", "p"],
    ["blend threshold 1e-8 -> 1e-5", "const BLEND_EPS=1e-8;", "const BLEND_EPS=1e-5;", "p"],
    ["smooth-point weight 0.999 -> 0.9", "const SMOOTH_W=0.999;", "const SMOOTH_W=0.9;", "p"],
    ["isRegionZero 0.001 -> 0.1", "const REGION_ZERO=0.001;", "const REGION_ZERO=0.1;", "p"],
    ["cell centres at the nodes", "XMID[i]=XG[i]+DX/2;", "XMID[i]=XG[i];", "p"],

    # ---------- the operators ----------
    ["derivative sign flipped", "d[i]=(f[i+1]-f[i])/dx;", "d[i]=(f[i]-f[i+1])/dx;", "p"],
    ["derivative divided by 2 dx", "d[i]=(f[i+1]-f[i])/dx;\n  return d;",
     "d[i]=(f[i+1]-f[i])/(2*dx);\n  return d;", "p"],
    ["trapezium 1/2 -> 1", "F[i]=F[i-1]+0.5*(f[i]+f[i-1])*dx;", "F[i]=F[i-1]+1.0*(f[i]+f[i-1])*dx;", "p"],
    ["trapezium sum -> difference", "F[i]=F[i-1]+0.5*(f[i]+f[i-1])*dx;",
     "F[i]=F[i-1]+0.5*(f[i]-f[i-1])*dx;", "p"],
    ["cell integral halved", "F[i]=F[i-1]+g[i-1]*dx;", "F[i]=F[i-1]+g[i-1]*dx/2;", "p"],
    ["second difference over dx^2", "o[i]=(d[i]-d[i-1])/dx;", "o[i]=(d[i]-d[i-1])/(dx*dx);", "p"],
    ["second difference ends zeroed", "o[0]=o[1]; o[n-1]=o[n-2];", "o[0]=0; o[n-1]=0;", "p"],
    ["PhET's central difference unaveraged", "o[i]=0.5*((f[i]-f[i-1])/dx+(f[i+1]-f[i])/dx);",
     "o[i]=1.0*((f[i]-f[i-1])/dx+(f[i+1]-f[i])/dx);", "p"],
    ["idxAt floors instead of rounding", "return clamp(Math.round(t*(n-1)),0,n-1);",
     "return clamp(Math.floor(t*(n-1)),0,n-1);", "p"],
    ["cellAt rounds instead of flooring", "return clamp(Math.floor((x-XMIN)/dx),0,n-2);",
     "return clamp(Math.round((x-XMIN)/dx),0,n-2);", "p"],

    # ---------- PhET's shapes ----------
    ["hill width w/(2 sqrt2) -> w/(2 sqrt3)", "const sd=w/(2*Math.sqrt(2));", "const sd=w/(2*Math.sqrt(3));", "p"],
    ["hill exponent 2 -> 4", "P=i=>Math.exp(-Math.pow((x[i]-xc)/sd,2));", "P=i=>Math.exp(-Math.pow((x[i]-xc)/sd,4));", "p"],
    ["triangle slope TYPICAL_Y/(w/2) -> /w", "const s=mode==='triangle'?TYPICAL_Y/(w/2):TYPICAL_Y*Math.pow(2/w,2);",
     "const s=mode==='triangle'?TYPICAL_Y/w:TYPICAL_Y*Math.pow(2/w,2);", "p"],
    ["parabola curvature (2/w)^2 -> (2/w)^3", "const s=mode==='triangle'?TYPICAL_Y/(w/2):TYPICAL_Y*Math.pow(2/w,2);",
     "const s=mode==='triangle'?TYPICAL_Y/(w/2):TYPICAL_Y*Math.pow(2/w,3);", "p"],
    ["parabola drawn as a triangle", "? i=>y-sg*s*Math.abs(x[i]-xc)\n      : i=>y-sg*s*Math.pow(x[i]-xc,2);",
     "? i=>y-sg*s*Math.abs(x[i]-xc)\n      : i=>y-sg*s*Math.abs(x[i]-xc);", "p"],
    ["pedestal plateau w-2e -> w-e", "const e=EDGE_SLOPE, s=w-2*e;", "const e=EDGE_SLOPE, s=w-e;", "p"],
    ["pedestal edge quartic -> quadratic", "return Math.exp(-Math.pow((x[i]-cen)/e,4));",
     "return Math.exp(-Math.pow((x[i]-cen)/e,2));", "p"],
    ["sinusoid period halved", "const lam=2*PI*w/W_DEF;", "const lam=PI*w/W_DEF;", "p"],
    ["sinusoid seven half-periods -> five", "const o=lam/2*7, a=lam/8;", "const o=lam/2*5, a=lam/8;", "p"],
    ["sinusoid taper lambda/8 -> lambda/4", "const o=lam/2*7, a=lam/8;", "const o=lam/2*7, a=lam/4;", "p"],
    ["sinusoid cos -> sin", "f[i]=t*(y*Math.cos(k*(xc-xx)))+(1-t)*fs[i];",
     "f[i]=t*(y*Math.sin(k*(xc-xx)))+(1-t)*fs[i];", "p"],
    ["tilt slope taken from the wrong point", "const t=(y-fs[i0])/r;", "const t=(y-fs[0])/r;", "p"],
    ["shift sign flipped", "const delta=y-fs[i0];\n    for(let i=0;i<n;i++) f[i]=fs[i]+delta;",
     "const delta=y+fs[i0];\n    for(let i=0;i<n;i++) f[i]=fs[i]+delta;", "p"],
    ["smoothing window 3 sigma -> 2 sigma", "while((K+1)*dx<=3*sigma) K++;", "while((K+1)*dx<=2*sigma) K++;", "p"],
    ["smoothing exponent -0.5 -> -1", "const kern=t=>w0*Math.exp(-0.5*Math.pow(t/sigma,2));",
     "const kern=t=>w0*Math.exp(-1.0*Math.pow(t/sigma,2));", "p"],
    ["smoothing peak weight sqrt(2 pi) -> sqrt(pi)", "const w0=1/(sigma*Math.sqrt(2*PI));",
     "const w0=1/(sigma*Math.sqrt(PI));", "p"],
    ["freeform interpolation reversed", "f[k]=(1-t)*ya+t*yb;", "f[k]=t*ya+(1-t)*yb;", "p"],

    # ---------- the tools ----------
    ["tangent reads the next cell", "return {i,slope:d[i],y:valueAt(f,x),", "return {i,slope:d[i+1],y:valueAt(f,x),", "p"],
    ["valueAt interpolates over 2 dx", "const i=cellAt(x), t=(x-XG[i])/DX;\n  return f[i]+t*(f[i+1]-f[i]);",
     "const i=cellAt(x), t=(x-XG[i])/(2*DX);\n  return f[i]+t*(f[i+1]-f[i]);", "p"],
    ["integAt drops its half", "return F[i]+0.5*(f[i]+yv)*(t*DX);", "return F[i]+(f[i]+yv)*(t*DX);", "p"],
    ["area zero crossing solved backwards", "if(a*b<0){ const t=a/(a-b); add(0.5*a*(t*DX)); add(0.5*b*((1-t)*DX)); }",
     "if(a*b<0){ const t=b/(a-b); add(0.5*a*(t*DX)); add(0.5*b*((1-t)*DX)); }", "p"],
    ["area triangle halves dropped", "if(a*b<0){ const t=a/(a-b); add(0.5*a*(t*DX)); add(0.5*b*((1-t)*DX)); }",
     "if(a*b<0){ const t=a/(a-b); add(a*(t*DX)); add(b*((1-t)*DX)); }", "p"],
    ["corner limits read the transition cell", "o.left=d[Math.max(o.a-1,0)];", "o.left=d[Math.max(o.a,0)];", "p"],

    # ---------- the closed forms and the quadrature ----------
    ["erf leading 2/sqrt(pi) -> 1/sqrt(pi)", "return 2*z/Math.sqrt(PI)*Math.exp(-z*z)*s;",
     "return z/Math.sqrt(PI)*Math.exp(-z*z)*s;", "p"],
    ["erf series denominator 2n+1 -> 2n-1", "t*=2*z*z/(2*n+1);", "t*=2*z*z/(2*n-1);", "p"],
    ["Gauss-Legendre weight numerator 2 -> 1", "xs[i]=z; ws[i]=2/((1-z*z)*dp*dp);", "xs[i]=z; ws[i]=1/((1-z*z)*dp*dp);", "p"],
    ["quadrature scaled by the panel, not the half-panel",
     "for(let i=0;i<GL.xs.length;i++) acc+=GL.ws[i]*fn(mid+half*GL.xs[i])*half;",
     "for(let i=0;i<GL.xs.length;i++) acc+=GL.ws[i]*fn(mid+half*GL.xs[i])*hstep;", "p"],
    ["closed-form hill exponent 8 -> 4", "const a=8/(w*w), k=0.5*Math.sqrt(PI/a), rt=Math.sqrt(a);",
     "const a=4/(w*w), k=0.5*Math.sqrt(PI/a), rt=Math.sqrt(a);", "p"],
    ["closed-form hill integral loses its half", "const a=8/(w*w), k=0.5*Math.sqrt(PI/a), rt=Math.sqrt(a);",
     "const a=8/(w*w), k=1.0*Math.sqrt(PI/a), rt=Math.sqrt(a);", "p"],
    ["closed-form triangle support |y|/|s| -> 2|y|/|s|",
     "const s=TYPICAL_Y/(w/2)*(y>0?1:-1), r=Math.abs(y)/Math.abs(s);",
     "const s=TYPICAL_Y/(w/2)*(y>0?1:-1), r=2*Math.abs(y)/Math.abs(s);", "p"],
    ["closed-form parabola primitive u^3/3 -> u^3/2", "const prim=u=>y*u-s*u*u*u/3;", "const prim=u=>y*u-s*u*u*u/2;", "p"],
    ["closed-form sinusoid primitive sign", "const prim=z=>-y/k*Math.sin(k*(xc-z));", "const prim=z=>y/k*Math.sin(k*(xc-z));", "p"],
    ["closed-form pedestal edge exponent 4 -> 3",
     "return u<half?1:Math.exp(-Math.pow((u-half)/e,4)); };", "return u<half?1:Math.exp(-Math.pow((u-half)/e,3)); };", "p"],
    ["the refinement ladder skips PhET's own grid", "const GRID_MULTS=[0.25,0.5,1,2,4,8];",
     "const GRID_MULTS=[0.25,0.5,1.5,2,4,8];", "p"],
    ["the default curve's hill moves", "const DEF_RECIPE=[['hill',2.0,3.2,1.6],['triangle',2.4,6.8,-1.2]];",
     "const DEF_RECIPE=[['hill',2.0,3.0,1.6],['triangle',2.4,6.8,-1.2]];", "p"],

    # ---------- the UI ----------
    ["a press on the canvas never marks the frame dirty",
     "      canvas.classList.add('dragging'); dirty=true; syncPanel(); refresh();",
     "      canvas.classList.add('dragging'); syncPanel(); refresh();", "u"],
    ["a drag never marks the frame dirty",
     "      dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model());",
     "      syncPanel(); roEl.innerHTML=readoutHTML(S.model());", "u"],
    ["the scrubbers lose their hit priority", "        const hs=S.hitScrub(x,y);", "        const hs=null&&S.hitScrub(x,y);", "u"],
    ["a scrubber drag lands short", "      ST[key]=v;\n      return true;", "      ST[key]=0.9*v;\n      return true;", "u"],
    ["a drag re-applies to the LIVE curve instead of the saved one",
     "  const out=manipulate(SAVED,SFLAG,mode,w,x,y);", "  const out=manipulate(activeF(),activeC(),mode,w,x,y);", "u"],
    ["nothing is pushed onto the undo stack", "  UNDO.push([activeF().slice(),activeC().slice()]);", "  ;", "u"],
    ["smoothing keeps the old corner flags", "  setActive(out.f,new Uint8Array(NPTS));     /* PhET: every point becomes smooth */",
     "  setActive(out.f,activeC());     /* PhET: every point becomes smooth */", "u"],
    ["reset all leaves the prediction alone", "  PRED=new Float64Array(NPTS); PFLAG=new Uint8Array(NPTS);\n  SAVED=CURVE.slice();",
     "  SAVED=CURVE.slice();", "u"],
    ["the tabs never mark themselves active",
     "    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');", "    ;", "u"],
    ["the width row stays live in shift mode", "    wRow.hidden=(SHAPE_MODES.indexOf(st.mode)<0);", "    wRow.hidden=false;", "u"],
    ["the arrow keys nudge by one cell, not five",
     "      st[key]=clamp(st[key]+(e.key==='ArrowRight'?5*DX:-5*DX),XMIN,XMAX);",
     "      st[key]=clamp(st[key]+(e.key==='ArrowRight'?DX:-DX),XMIN,XMAX);", "u"],
    ["the lay-it-down button ignores the width slider", "      } else applyShape(ST.mode,ST.width,ST.placeX,ST.height);",
     "      } else applyShape(ST.mode,W_DEF,ST.placeX,ST.height);", "u"],
]

src = io.open(SIM, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = []
for label, old, new, suite in M:
    n = src.count(old)
    if n != 1:
        bad.append('%-52s appears %d times' % (label, n))
    if old == new:
        bad.append('%-52s is a no-op' % label)
for b in bad:
    print('BAD  ' + b)
assert not bad, '%d bad patterns' % len(bad)
io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=1))
print('mutants.json: %d mutants (%d physics, %d UI)'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
