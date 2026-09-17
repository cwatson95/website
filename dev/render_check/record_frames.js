// record_frames.js — render synthwave.js frames without a browser.
//
// Loads ../../synthwave.js under deno (no DOM, so its browser boot block is
// skipped), calls Synthwave.drawFrame against a stub 2D context that records
// the display list, and writes one JSON file per frame for rasterise.py.
//
// Usage: deno run --allow-read --allow-write record_frames.js [outdir]

const outdir = Deno.args[0] || 'out';
await Deno.mkdir(outdir, { recursive: true });

const here = new URL('.', import.meta.url).pathname;
const src = await Deno.readTextFile(here + '../../synthwave.js');
(0, eval)(src);

const Synthwave = globalThis.Synthwave;
if (!Synthwave) throw new Error('synthwave.js did not define Synthwave');

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
    beginPath() { ops.push(['beginPath']); },
    moveTo(x, y) { ops.push(['moveTo', x, y]); },
    lineTo(x, y) { ops.push(['lineTo', x, y]); },
    stroke() { ops.push(['stroke']); },
    fillRect(x, y, w, h) { ops.push(['fillRect', x, y, w, h]); },
    createLinearGradient(...c) { return makeGradient('linear', c); },
    createRadialGradient(...c) { return makeGradient('radial', c); }
  };
}

const st = Synthwave.createState(W, H, 20260812);
for (const t of [0, 2.5, 5, 7.5]) {
  const ops = [];
  const ctx = makeCtx(ops);
  Synthwave.drawFrame(ctx, st, t);
  const path = `${outdir}/frame_${t.toFixed(1)}.json`;
  await Deno.writeTextFile(path, JSON.stringify({ w: W, h: H, t, ops }));
  console.log(`${path}: ${ops.length} ops`);
}
