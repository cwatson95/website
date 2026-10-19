#!/usr/bin/env python3
"""One mechanical edit, kept as a script so it is reproducible: the eleven
amplitudes were ONE array shared by the Discrete views and the Wave Game, so
GAME.reset() at boot wiped the Discrete preset (the UI drive caught it: A1 was
0 where PhET starts at 1).  They are now two arrays, AMPS and GUESS, with
ampArray() choosing by view -- which is PhET's own arrangement (a fourierSeries
per screen, and answerSeries/guessSeries in the game)."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SUBS = {
    'p5_views.js': [
        ("""    setBar(n,y){
      const step=GEO.view==='game'?G_STEP:A_STEP;
      const a=snapAmp(barA(GEO.bars,y,AMAX),step);
      if(AMPS[n-1]===a) return false;
      AMPS[n-1]=a;
      if(GEO.view!=='game') ST.preset='custom';
      return true;
    },""",
         """    setBar(n,y){
      const step=GEO.view==='game'?G_STEP:A_STEP;
      const a=snapAmp(barA(GEO.bars,y,AMAX),step), arr=ampArray();
      if(arr[n-1]===a) return false;
      arr[n-1]=a;
      if(GEO.view!=='game') ST.preset='custom';
      return true;
    },"""),
    ],
    'p6_boot.js': [
        ("""  /* the amplitude row edits AMPS[sel-1], not a key of ST, so it needs its own
     read-back: the preset chips and the canvas drag both move it */""",
         """  /* the amplitude row edits ampArray()[sel-1], not a key of ST, so it needs
     its own read-back: the preset chips and the canvas drag both move it */"""),
        ("""      inp.setAttribute('step',stp); inp.value=AMPS[st.sel-1];
      val.textContent=fmt(AMPS[st.sel-1],2); };""",
         """      inp.setAttribute('step',stp); inp.value=ampArray()[st.sel-1];
      val.textContent=fmt(ampArray()[st.sel-1],2); };"""),
        ("""      AMPS[st.sel-1]=snapAmp(parseFloat(inp.value),stp);""",
         """      ampArray()[st.sel-1]=snapAmp(parseFloat(inp.value),stp);"""),
        ("""      AMPS[st.sel-1]=snapAmp(AMPS[st.sel-1]+(e.key==='ArrowUp'?stp:-stp),stp);""",
         """      ampArray()[st.sel-1]=snapAmp(ampArray()[st.sel-1]+(e.key==='ArrowUp'?stp:-stp),stp);"""),
        ("""    btn('zero them all',()=>{ setAmps(new Array(NMAX).fill(0)); if(st.view!=='game') st.preset='custom'; }),""",
         """    btn('zero them all',()=>{ setCurrent(new Array(NMAX).fill(0)); if(st.view!=='game') st.preset='custom'; }),"""),
        ("""  gGame.appendChild(h('div',{class:'btnrow'},btn('erase my amplitudes',()=>{ setAmps(new Array(NMAX).fill(0)); })));""",
         """  gGame.appendChild(h('div',{class:'btnrow'},btn('erase my amplitudes',()=>{ setGuess(new Array(NMAX).fill(0)); })));"""),
    ],
    'p7_test.js': [
        ("""  const stSave=Object.assign({},ST), ampSave=AMPS.slice();
  function restore(){ Object.assign(ST,stSave); setAmps(ampSave); }""",
         """  const stSave=Object.assign({},ST), ampSave=AMPS.slice(), guessSave=GUESS.slice();
  function restore(){ Object.assign(ST,stSave); setAmps(ampSave); setGuess(guessSave); }"""),
        ("""    if(over._amps) setAmps(over._amps); else applyPreset();
    if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
      GAME.answer=gameAmplitudes(GAME.level,GAME.seed*7919+GAME.level*104729);
      if(!over._amps) setAmps(new Array(NMAX).fill(0)); }""",
         """    if(over._amps) setAmps(over._amps); else applyPreset();
    if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
      GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
      setGuess(over._guess||(over.showAns?GAME.answer:new Array(NMAX).fill(0))); }"""),
    ],
    'capture_tail_fourier-making-waves.js': [
        ("""  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,GAME.seed*7919+GAME.level*104729);
    if(over._solve) setAmps(GAME.answer.slice()); else setAmps(new Array(NMAX).fill(0)); }""",
         """  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
    setGuess(over._solve?GAME.answer.slice():new Array(NMAX).fill(0)); }"""),
    ],
    'probe_tail.js': [
        ("""  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,GAME.seed*7919+GAME.level*104729);
    if(!over._amps) setAmps(new Array(NMAX).fill(0)); }""",
         """  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
    setGuess(over.showAns?GAME.answer.slice():new Array(NMAX).fill(0)); }"""),
    ],
}
for fn, pairs in SUBS.items():
    p = os.path.join(HERE, fn)
    s = io.open(p, encoding='utf-8').read()
    for a, b in pairs:
        if b in s and a not in s:
            continue                       # already applied
        assert s.count(a) == 1, (fn, a[:60], s.count(a))
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('patched', fn)
