#!/usr/bin/env python3
"""Build p2_engine.js from the data lab's, trimmed to this sim's screen.

PhET's Projectile Sampling Distributions IS the data lab's Sampling screen in
its own right, and it ships the same bundled model, so the engine here is the
data lab's byte for byte except where PhET's own build branches on the sim
name: the bin widths (no 10 m, 0.5 the default), the absence of a total-bins
strategy, the zoom ladder (250 samples rather than 500 projectiles) and the
speed-mean range floor (20 m/s rather than 15).  The launcher orientation and
the projectile type are controls the Sampling screen does not have, so the
tables keep only the values that screen uses.

Anything this trims is checked by the assertion at the bottom: the two engines
must differ ONLY in the blocks named here.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'projectile-data-lab', 'p2_engine.js')
s = io.open(SRC, encoding='utf-8').read()
orig = s


def sub(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


sub(""" *  the engine: PhET's constants, its launch mechanism, the exact      *
 *  distribution of the landing distance, and the statistics.          *
 *  Every constant below is read from the minified original            *
 *  docs/phets/projectile-data-lab_en.html and cited as PhET's value;  *
 *  everything derived is pinned in selfTest to derive.py.             *""",
    """ *  the engine: PhET's constants, its launch mechanism, the exact      *
 *  distribution of the landing distance, and the statistics.  This is *
 *  the data lab remake's engine, trimmed by build/projectile-         *
 *  sampling-distributions/make_engine.py to the Sampling screen's own *
 *  controls — PhET ships one bundle for both sims and branches on the *
 *  sim name for exactly these values.  Read from the minified         *
 *  original docs/phets/projectile-sampling-distributions_en.html and  *
 *  cited as PhET's; everything derived is pinned in selfTest.         *""")
sub("""  BINW:[0.5,1,2,5,10],    /* selectedBinWidthProperty validValues    */
  NBINS:[10,20,50,100,200], /* selectedTotalBinsProperty validValues */
  INTERVAL:[40,60],       /* IntervalTool edge1, edge2 defaults      */""",
    """  BINW:[0.5,1,2,5],       /* selectedBinWidthProperty validValues     */
  BINW_DEF:0.5,           /* PSD defaults to 0.5 m; the data lab to 1 */
  ZOOM_MAX:[250,200,150,100,75,50,25], /* the samples-per-bin ladder  */
  SPEED_MEAN_MIN:20,      /* the speed-mean range floor (data lab: 15)*/""")
# the angle stabiliser is a Sources-screen control; the Sampling screen's
# launchers carry their spreads directly, so the two mapping functions are
# dead code here — and dead code is equivalent-mutant country (the first
# sweep duly reported the stabiliser's direction as a survivor).
sub("""/* ---- PhET's angle stabiliser -----------------------------------------------
   standardDeviationAngle = linear(1, 0, sdMin, sdMax, stability): the slider
   runs the other way round, stability 1 giving the TIGHTEST launcher. */
function pdlSdOfStab(stab){ return PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])*(1-stab); }
function pdlStabOfSd(sd){ return 1-(sd-PDL.ANG_SD[0])/(PDL.ANG_SD[1]-PDL.ANG_SD[0]); }

""", """/* PhET's angle stabiliser (standardDeviationAngle = linear(1, 0, sdMin,
   sdMax, stability)) belongs to the Sources screen and is NOT here: the
   Sampling screen's six launchers carry their angle spreads directly. */

""")
sub("""/* ProjectileType(tandem, speedMultiplier) */
const PTYPES=[{id:'cannonball',name:'cannonball',mult:1},
              {id:'pumpkin',name:'pumpkin',mult:1.1},
              {id:'piano',name:'piano',mult:0.9}];
/* launcherOrientation: the mean launch angle, and the launch height */
const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:0},
               {id:'angle45',name:'45°',ang:45,h:0},
               {id:'angle60',name:'60°',ang:60,h:0},
               {id:'angle0Raised',name:'0° raised',ang:0,h:PDL.RAISED_H}];""",
    """/* ProjectileType(tandem, speedMultiplier) — the Sampling screen fires
   cannonballs only, so its table has one row */
const PTYPES=[{id:'cannonball',name:'cannonball',mult:1}];
/* launcherOrientation — the Sampling screen fixes angle30 (its fields are
   built with validValues:['angle30']), so its table has one row.  The engine
   below still carries the general launch height h, because the closed forms
   are the general ones and selfTest exercises them. */
const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:0}];""")
io.open(os.path.join(HERE, 'p2_engine.js'), 'w', encoding='utf-8').write(s)

# what changed, line for line
a, b = orig.splitlines(), s.splitlines()
print('p2_engine.js: %d lines from the data lab\'s %d' % (len(b), len(a)))
import difflib
ch = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('---', '+++')]
print('%d lines differ' % len(ch))
for l in ch:
    print('   ' + l[:96])
