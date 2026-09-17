// record_teaching.js — headless frames for teaching_network.js.
//
// Same stub-context display-list pattern as record_frames.js, plus the ops
// the network page uses: arc/fill (orbs), fillText/font (labels). Records an
// overview pair (glimmer check), a mid-glide frame, and the arrival at CM-22
// (the continuity-equation bridge node).
//
// Usage: deno run --allow-read --allow-write record_teaching.js [outdir]

const outdir = Deno.args[0] || 'out';
await Deno.mkdir(outdir, { recursive: true });

const here = new URL('.', import.meta.url).pathname;
const src = await Deno.readTextFile(here + '../../teaching_network.js');
(0, eval)(src);

const TN = globalThis.TeachingNetwork;
if (!TN) throw new Error('teaching_network.js did not define TeachingNetwork');

const W = 1280, H = 720;

function makeGradient(kind, coords) {
  return {
    __grad: kind,
    coords,
    stops: [],
    addColorStop(off, col) { this.stops.push([off, col]); }
  };
}

function makeCtx(ops) {
  return {
    set fillStyle(v) { ops.push(['fillStyle', typeof v === 'object' ? v : String(v)]); },
    set strokeStyle(v) { ops.push(['strokeStyle', String(v)]); },
    set lineWidth(v) { ops.push(['lineWidth', v]); },
    set font(v) { ops.push(['font', String(v)]); },
    set textAlign(v) { ops.push(['textAlign', String(v)]); },
    set textBaseline(v) { ops.push(['textBaseline', String(v)]); },
    beginPath() { ops.push(['beginPath']); },
    moveTo(x, y) { ops.push(['moveTo', x, y]); },
    lineTo(x, y) { ops.push(['lineTo', x, y]); },
    arc(x, y, r, a0, a1) { ops.push(['arc', x, y, r]); },
    fill() { ops.push(['fill']); },
    stroke() { ops.push(['stroke']); },
    fillRect(x, y, w, h) { ops.push(['fillRect', x, y, w, h]); },
    fillText(s, x, y) { ops.push(['fillText', String(s), x, y]); },
    createLinearGradient(...c) { return makeGradient('linear', c); },
    createRadialGradient(...c) { return makeGradient('radial', c); }
  };
}

const st = TN.createState(W, H, 20260812);

let target = -1;
for (let i = 0; i < st.nodes.length; i++) {
  if (st.nodes[i].id === 'CM-22') target = i;
}
if (target < 0) throw new Error('CM-22 not found in DATA');

const shots = [
  ['overview_a', 0.4, null],
  ['overview_b', 4.4, null],
  ['glide_mid', 5.55, () => TN.travelTo(st, target, 5.0)],
  ['arrived', 6.6, null]
];

for (const [name, t, setup] of shots) {
  if (setup) setup();
  const ops = [];
  TN.drawFrame(makeCtx(ops), st, t);
  const path = `${outdir}/net_${name}.json`;
  await Deno.writeTextFile(path, JSON.stringify({ w: W, h: H, t, ops }));
  console.log(`${path}: ${ops.length} ops`);
}
