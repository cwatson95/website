/* synthwave.js — homepage background.
 *
 * Layout after watermarked_preview.mp4 (flat perspective grid floor, wireframe
 * mountains at the horizon, starfield sky); palette sampled from
 * example_wave.mp4 (azure ramp #123a63 -> #0b5a94 -> #1089c4 -> #1bbeeb ->
 * #7deeff over a deep navy sky), with the background pulled darker than the
 * video per README ("soft dark violet/blue"). No libraries; runs over file://.
 *
 * The drawing core (createState / drawFrame) never touches the DOM, so
 * dev/render_check/ can load this file under deno, record the display list
 * from a stub context, and rasterise it with matplotlib — there is no
 * headless browser on this machine.
 */
(function (global) {
  'use strict';

  /* ---------- deterministic noise ---------- */

  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hash2(ix, iz) {
    var n = (ix * 374761393 + iz * 668265263) | 0;
    n = Math.imul(n ^ (n >>> 13), 1274126177);
    n ^= n >>> 16;
    return (n >>> 0) / 4294967296;
  }

  function smooth(f) { return f * f * (3 - 2 * f); }

  function noise2(x, z) {
    var ix = Math.floor(x), iz = Math.floor(z);
    var fx = smooth(x - ix), fz = smooth(z - iz);
    var a = hash2(ix, iz), b = hash2(ix + 1, iz);
    var c = hash2(ix, iz + 1), d = hash2(ix + 1, iz + 1);
    return a + (b - a) * fx + (c - a) * fz + (a - b - c + d) * fx * fz;
  }

  function fbm(x, z) {
    return 0.68 * noise2(x, z) + 0.32 * noise2(x * 2.17 + 13.7, z * 2.17 + 91.3);
  }

  function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }

  /* ---------- palette (sampled from example_wave.mp4) ---------- */

  var SKY_TOP = 'rgb(6,9,24)';      // video sky is #123453..#173f65; ours is darker
  var SKY_HOR = 'rgb(13,36,64)';
  var GROUND_TOP = 'rgb(8,29,50)';
  var GROUND_BOT = 'rgb(3,6,12)';
  var RAMP = [                       // ridge energy ramp, valley -> hot crest
    [18, 58, 99],                    // #123a63
    [11, 90, 148],                   // #0b5a94
    [16, 137, 196],                  // #1089c4
    [27, 190, 235],                  // #1bbeeb
    [125, 238, 255]                  // #7deeff
  ];

  function rampColor(s) {
    var p = clamp01(s) * (RAMP.length - 1);
    var i = Math.min(RAMP.length - 2, Math.floor(p)), f = p - i;
    var A = RAMP[i], B = RAMP[i + 1];
    return [
      Math.round(A[0] + (B[0] - A[0]) * f),
      Math.round(A[1] + (B[1] - A[1]) * f),
      Math.round(A[2] + (B[2] - A[2]) * f)
    ];
  }

  // Batched-stroke colour buckets: one beginPath/stroke per bucket per pass.
  var NB = 24;
  var MESH_COLORS = [], DOT_COLORS = [], FLOOR_COLORS = [];
  (function () {
    var k, s, c;
    for (k = 0; k < NB; k++) {
      s = k / (NB - 1);
      c = rampColor(s);
      MESH_COLORS.push('rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (0.10 + 0.85 * s).toFixed(3) + ')');
      DOT_COLORS.push('rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (0.25 + 0.7 * s).toFixed(3) + ')');
    }
    for (k = 0; k < 10; k++) {
      s = k / 9;
      c = [Math.round(16 + 30 * s), Math.round(137 + 59 * s), Math.round(196 + 48 * s)];
      FLOOR_COLORS.push('rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (0.06 + 0.5 * s).toFixed(3) + ')');
    }
  })();

  /* ---------- state ---------- */

  function createState(w, h, seed) {
    var st = { w: w, h: h, seed: (seed || 1) >>> 0 };
    st.horizonY = Math.round(h * 0.50);
    st.f = 0.75 * h;                 // focal length in px; camera height = 1 world unit
    st.cx = w / 2;
    st.ridge = { rows: 18, cols: 96, zNear: 6, zFar: 26, yRef: 3.6 };
    var rng = mulberry32(st.seed ^ 0x9E3779B9);
    var n = Math.max(90, Math.min(230, Math.round(w * h / 8500)));
    st.stars = [];
    for (var i = 0; i < n; i++) {
      st.stars.push({
        x: rng() * w,
        y: rng() * st.horizonY * 0.94,
        s: 0.7 + 1.7 * Math.pow(rng(), 2),
        base: 0.28 + 0.6 * rng(),
        ph: 6.2832 * rng(),
        sp: 0.25 + 0.5 * rng(),
        fl: rng() < 0.06
      });
    }
    return st;
  }

  /* ---------- ridge (the undulating example_wave element) ---------- */

  function ridgeHeight(u, z, t) {
    // u in [-1,1] across the screen, z = world depth, t = seconds
    var nx = u * 4.2, nz = z * 0.26;
    var v = 0.78 * fbm(nx, nz + t * 0.045)            // slow drift = the undulation
          + 0.22 * fbm(nx * 2.3 + 7.7, nz * 2.3 - t * 0.06);
    var envEdge = 0.72 + 0.5 * noise2(u * 1.35 + 40.2, 3.7); // width-wise variety
    var dip = 1 - 0.28 * Math.exp(-(u * u) / 0.3025);  // soften the centre for the title
    var depth = 0.55 + 0.45 * (z - 6) / 20;            // taller toward the back
    var au = Math.abs(u);                              // tame lone spikes at the screen edges
    var edgeFall = au > 0.82 ? 1 - 0.5 * smooth((au - 0.82) / 0.18) : 1;
    var y = 5.6 * v * envEdge * dip * depth * edgeFall;
    if (y > 4.4) y = 4.4 + 0.45 * (y - 4.4);           // soft knee: broad massifs, no spires
    y *= 0.94 + 0.06 * Math.sin(0.35 * t + u * 1.7 + z * 0.13); // slow breathing swell
    return y;
  }

  function drawRidge(ctx, st, t) {
    var R = st.ridge, rows = R.rows, cols = R.cols;
    var buckets = [], dots = [[], [], []];
    var k, r, i;
    for (k = 0; k < NB; k++) buckets.push([]);

    // vertex grid: P[r] = flat [sx, sy, e] per column; r=0 is the far row
    var P = [];
    for (r = 0; r < rows; r++) {
      var fz = r / (rows - 1);
      var z = R.zFar + (R.zNear - R.zFar) * fz;
      var fade = 0.35 + 0.65 * fz;                     // haze on the far rows
      var row = [];
      for (i = 0; i < cols; i++) {
        var u = -1 + 2 * i / (cols - 1);
        var y = ridgeHeight(u, z, t);
        var sx = st.cx + 0.62 * st.w * u;              // screen-uniform column fan
        var sy = st.horizonY + st.f * (1 - y) / z;
        var e = clamp01(0.16 + 0.9 * y / R.yRef) * fade;
        row.push(sx, sy, e);
      }
      P.push(row);
    }

    function seg(x1, y1, e1, x2, y2, e2) {
      var b = Math.min(NB - 1, Math.floor((e1 + e2) * 0.5 * NB));
      var arr = buckets[b];
      arr.push(x1, y1, x2, y2);
    }

    for (r = 0; r < rows; r++) {
      var A = P[r], B = r + 1 < rows ? P[r + 1] : null;
      for (i = 0; i < cols; i++) {
        var ax = A[3 * i], ay = A[3 * i + 1], ae = A[3 * i + 2];
        if (i + 1 < cols) seg(ax, ay, ae, A[3 * i + 3], A[3 * i + 4], A[3 * i + 5]);
        if (B) {
          seg(ax, ay, ae, B[3 * i], B[3 * i + 1], B[3 * i + 2]);
          if (i + 1 < cols) {                          // one diagonal -> triangle mesh
            seg(ax, ay, ae, B[3 * i + 3], B[3 * i + 4], B[3 * i + 5]);
          }
        }
        if (ae > 0.46) {                               // glowing vertex dots on crests
          dots[ae > 0.78 ? 2 : ae > 0.62 ? 1 : 0].push(ax, ay);
        }
      }
    }

    ctx.lineWidth = 1;
    for (k = 0; k < NB; k++) {
      var b = buckets[k];
      if (!b.length) continue;
      ctx.strokeStyle = MESH_COLORS[k];
      ctx.beginPath();
      for (i = 0; i < b.length; i += 4) {
        ctx.moveTo(b[i], b[i + 1]);
        ctx.lineTo(b[i + 2], b[i + 3]);
      }
      ctx.stroke();
    }
    var DOT_SIZE = [1.6, 2.1, 2.6];
    var DOT_IDX = [Math.floor(NB * 0.62), Math.floor(NB * 0.78), NB - 1];
    for (k = 0; k < 3; k++) {
      var d = dots[k], sz = DOT_SIZE[k];
      if (!d.length) continue;
      ctx.fillStyle = DOT_COLORS[DOT_IDX[k]];
      for (i = 0; i < d.length; i += 2) {
        ctx.fillRect(d[i] - sz / 2, d[i + 1] - sz / 2, sz, sz);
      }
    }
  }

  /* ---------- flat synthwave floor grid ---------- */

  function drawFloor(ctx, st, t) {
    var f = st.f, hy = st.horizonY, w = st.w, h = st.h;
    var i;

    // radial verticals through the vanishing point (straight rays on screen),
    // in two alpha bands so they fade toward the horizon instead of crowding
    // into a bright wedge at the vanishing point
    var gs = 0.11;                                     // world spacing between rays
    var count = Math.ceil(0.68 * w / (gs * (h - hy)));
    var split = hy + 0.2 * (h - hy);
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(16,137,196,0.11)';
    ctx.beginPath();
    for (i = -count; i <= count; i++) {
      ctx.moveTo(st.cx + i * gs * 6, hy + 6);
      ctx.lineTo(st.cx + i * gs * (split - hy), split);
    }
    ctx.stroke();
    ctx.strokeStyle = 'rgba(16,137,196,0.30)';
    ctx.beginPath();
    for (i = -count; i <= count; i++) {
      ctx.moveTo(st.cx + i * gs * (split - hy), split);
      ctx.lineTo(st.cx + i * gs * (h - hy), h);
    }
    ctx.stroke();

    // horizontals scrolling slowly toward the viewer
    var G = 1.16, z0 = 1.12, phase = (t * 0.42) % 1;
    var lines = [];
    for (i = 0; i < 10; i++) lines.push([]);
    for (var kk = 0; kk < 40; kk++) {
      var z = z0 * Math.pow(G, kk - phase);
      var sy = hy + f / z;
      if (sy > h + 2) continue;
      if (sy < hy + 2) break;
      var s = clamp01((sy - hy) / (h - hy));
      lines[Math.min(9, Math.floor(Math.pow(s, 0.75) * 10))].push(sy);
    }
    for (i = 0; i < 10; i++) {
      var L = lines[i];
      if (!L.length) continue;
      ctx.strokeStyle = FLOOR_COLORS[i];
      ctx.lineWidth = i > 6 ? 1.4 : 1;
      ctx.beginPath();
      for (var j = 0; j < L.length; j++) {
        ctx.moveTo(0, L[j]);
        ctx.lineTo(w, L[j]);
      }
      ctx.stroke();
    }
  }

  /* ---------- stars ---------- */

  function drawStars(ctx, st, t) {
    for (var i = 0; i < st.stars.length; i++) {
      var S = st.stars[i];
      var a = S.base * (0.55 + 0.45 * Math.sin(S.sp * t + S.ph));
      if (a < 0.04) continue;
      ctx.fillStyle = 'rgba(159,216,255,' + a.toFixed(3) + ')';
      ctx.fillRect(S.x - S.s / 2, S.y - S.s / 2, S.s, S.s);
      if (S.fl) {                                      // faint cross flare, a few stars
        ctx.fillStyle = 'rgba(159,216,255,' + (a * 0.3).toFixed(3) + ')';
        ctx.fillRect(S.x - 3 * S.s, S.y - 0.5, 6 * S.s, 1);
        ctx.fillRect(S.x - 0.5, S.y - 3 * S.s, 1, 6 * S.s);
      }
    }
  }

  /* ---------- frame ---------- */

  function drawFrame(ctx, st, t) {
    var w = st.w, h = st.h, hy = st.horizonY;
    var g;

    g = ctx.createLinearGradient(0, 0, 0, hy);
    g.addColorStop(0, SKY_TOP);
    g.addColorStop(1, SKY_HOR);
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, hy);

    g = ctx.createLinearGradient(0, hy, 0, h);
    g.addColorStop(0, GROUND_TOP);
    g.addColorStop(1, GROUND_BOT);
    ctx.fillStyle = g;
    ctx.fillRect(0, hy, w, h - hy);

    drawStars(ctx, st, t);

    // ambient bloom behind the ridge (the wave video's soft glow)
    g = ctx.createRadialGradient(st.cx, hy - 0.04 * h, 0, st.cx, hy - 0.04 * h, 0.58 * w);
    g.addColorStop(0, 'rgba(16,137,196,0.22)');
    g.addColorStop(1, 'rgba(16,137,196,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, hy + 0.1 * h);

    drawRidge(ctx, st, t);
    drawFloor(ctx, st, t);

    // horizon glow band ties ridge base and floor together
    g = ctx.createLinearGradient(0, hy - 0.06 * h, 0, hy + 0.2 * h);
    g.addColorStop(0, 'rgba(16,137,196,0)');
    g.addColorStop(0.32, 'rgba(27,190,235,0.30)');
    g.addColorStop(1, 'rgba(16,137,196,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, hy - 0.06 * h, w, 0.26 * h);

    // vignette, as in the wave video's corners
    g = ctx.createRadialGradient(st.cx, 0.5 * h, 0.32 * Math.min(w, h), st.cx, 0.5 * h, 0.85 * Math.max(w, h));
    g.addColorStop(0, 'rgba(4,7,15,0)');
    g.addColorStop(1, 'rgba(4,7,15,0.5)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
  }

  global.Synthwave = {
    createState: createState,
    drawFrame: drawFrame,
    palette: { ramp: RAMP, skyTop: SKY_TOP, skyHorizon: SKY_HOR }
  };

  /* ---------- browser boot (skipped under deno / render_check) ---------- */

  if (!global.document || !global.requestAnimationFrame) return;

  function boot() {
    var cv = global.document.getElementById('bg');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var st = null, dpr = 1, raf = 0, last = null, acc = 0;

    var reduced = false;
    try {
      reduced = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) { /* matchMedia unavailable: keep animating */ }

    function resize() {
      dpr = Math.min(global.devicePixelRatio || 1, 2);
      var w = global.innerWidth, h = global.innerHeight;
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
      cv.style.width = w + 'px';
      cv.style.height = h + 'px';
      st = createState(w, h, 20260812);
      if (reduced) still();
    }

    function still() {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      drawFrame(ctx, st, 2.7);
    }

    function frame(ms) {
      if (last !== null) acc += Math.min(ms - last, 100); // clamp tab-away jumps
      last = ms;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      drawFrame(ctx, st, acc / 1000);
      raf = global.requestAnimationFrame(frame);
    }

    resize();
    if (reduced) {
      still();
    } else {
      raf = global.requestAnimationFrame(frame);
    }

    global.addEventListener('resize', resize);
    global.document.addEventListener('visibilitychange', function () {
      if (reduced) return;
      if (global.document.hidden) {
        global.cancelAnimationFrame(raf);
        last = null;
      } else {
        raf = global.requestAnimationFrame(frame);
      }
    });
  }

  if (global.document.readyState === 'loading') {
    global.document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : globalThis);
