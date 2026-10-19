/* ================================================================== *
 *  drawing helpers, extracted verbatim from the landed                *
 *  models-of-the-hydrogen-atom build by extract_helpers.py: this is    *
 *  where this collection keeps its accumulated layout fixes (the       *
 *  bottom-up stage layout, the label registry and its half-pixel       *
 *  overlap rule, the #hint reservation, the axis clearances).          *
 * ================================================================== */
/* the floating readout covers the top right of the stage (about 300 x 550),
   and the HTML #hint owns the bottom-left corner (bottom:11px, 11px type), so
   every view keeps canvas text out of both (Known-bad, twice). */
const HINT_W = 340, HINT_H = 27;
function usableW(W){ return Math.max(320, W - RO_W - 34); }

/* lay the stage out from the BOTTOM up: measure the caption first, give the
   picture whatever is left (Known-bad: wrapped text has no fixed height).
   The HTML #hint is drawn at bottom:11px in 11 px type and the canvas capture
   cannot see it, so the caption's LAST line has to clear it: HINT_H of extra
   bottom margin, asserted in selfTest (Known-bad, wave-on-a-string). */
function layout(ctx, W, H, full, short){
  /* a narrow stage has to keep 300 px for the picture, or the long caption
     eats the stack and the bottom panel's axis title lands on it */
  /* the caption is capped at the USABLE width, which is the part of the stage
     the floating readout does not cover; at the full stage width it ran under
     the readout at every size below 1400 px */
  const f = fitCaption(ctx, W, H - HINT_H, full, short, usableW(W),
                       stageTop() + (narrowStage(W) ? 300 : 120));
  return {top: stageTop(), capY: f.capY, capW: f.capW, txt: f.txt,
          bot: f.capY - 12, W, H};
}
/* a stage narrower than this cannot carry two panels side by side (the
   floating readout already owns 300 px of it) — every two-panel view stacks
   instead (Known-bad: two-column layouts collapse below ~430 px of column) */
function narrowStage(W){ return usableW(W) < 430; }
/* axes() puts tick labels at +5 and the x-axis title at +21 below the
   frame, in 11 px type: 38 px of clearance under every plot box. */
const AXIS_BOT = 38;
/* how many y ticks a panel of this height can label without the labels
   touching: a 10.5 px label is ~12 px tall, so five ticks need 60 px of frame
   (Known-bad: tick label size follows the tick SPACING) */
function nyFor(h){ return h < 90 ? 2 : (h < 140 ? 3 : 5); }
function drawCaption(ctx, L){
  const lines = wrapText(ctx, L.txt, L.capW, '11.5px -apple-system, sans-serif');
  LABEL_RECTS.push({x: 18, y: L.capY, w: L.capW, h: lines.length * 14});
  caption(ctx, 18, L.capY, L.txt, L.capW, '#767e92');
}
/* two stacked panels that ALWAYS leave AXIS_BOT under the lower one: the
   square shrinks until the plot below it fits, rather than the plot's height
   being clamped and its x-axis title pushed onto the caption */
function stackFit(top, bot, gap, share){
  let side = Math.max(90, Math.min((bot - top) * (share || 0.46), bot - top));
  let bh = bot - AXIS_BOT - (top + side + gap);
  if(bh < 72){ side = Math.max(70, side - (72 - bh)); bh = bot - AXIS_BOT - (top + side + gap); }
  return {side, bh: Math.max(46, bh)};
}
function panelTitle(ctx, b, t){
  LABEL_RECTS.push(labelRect(ctx, b.x, b.y - 9, t, 'italic 13px Georgia, serif', 'left', 'bottom'));
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom'; ctx.fillStyle = '#aeb6c6';
  ctx.font = 'italic 13px Georgia, serif';
  ctx.fillText(plain(t), b.x, b.y - 9);
}
/* every label this file draws records its rectangle; labelIfClear() then
   refuses to draw one that would land on an existing rectangle, so a crowded
   picture DROPS labels instead of stacking them.  Cleared per draw. */
let LABEL_RECTS = [];
function labelRect(ctx, x, y, t, font, align, base){
  ctx.font = font || '11px -apple-system, sans-serif';
  const w = ctx.measureText(plain(t)).width;
  const mm = /([\d.]+)px/.exec(ctx.font), fs = mm ? parseFloat(mm[1]) : 10, fh = fs * 1.15;
  const lx = align === 'center' ? x - w / 2 : (align === 'right' ? x - w : x);
  const ly = base === 'top' ? y : (base === 'middle' ? y - fh / 2
    : (base === 'bottom' ? y - fh : y - fh * 0.8));
  return {x: lx, y: ly, w, h: fh};
}
/* half a pixel, which is tools/audit.py's threshold.  A 2 px tolerance passed
   the inline sweep and failed the audit on the same picture (Known-bad), and a
   2 px graze is visible antialiased smear on canvas. */
function rectsHit(a, b){
  return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > 0.5
      && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > 0.5;
}
function label(ctx, x, y, t, col, font, align, base){
  LABEL_RECTS.push(labelRect(ctx, x, y, t, font, align, base));
  ctx.fillStyle = col || '#8b93a6';
  ctx.font = font || '11px -apple-system, sans-serif';
  ctx.textAlign = align || 'left'; ctx.textBaseline = base || 'top';
  ctx.fillText(plain(t), x, y);
}
function labelIfClear(ctx, x, y, t, col, font, align, base){
  const r = labelRect(ctx, x, y, t, font, align, base);
  for(const q of LABEL_RECTS) if(rectsHit(r, q)) return false;
  /* the shared legendBox() draws its own text and records it in LEGEND_RECTS,
     not in the label registry — check both, or a dodging label lands on a
     legend (a z score did exactly that at 820x520) */
  for(const q of LEGEND_RECTS) if(rectsHit(r, q)) return false;
  label(ctx, x, y, t, col, font, align, base);
  return true;
}
/* a label beside a vertical rule on a ruler-style strip: it picks the side
   with room INSIDE the panel first (a label that only dodges what it collides
   with still runs off the canvas -- "PhET's atomic-scale caption" ended at
   x = 597 on a 560 px stage), then falls back to the other side, then is
   dropped. */
function sideLabel(ctx, b, x, y, t, col){
  const w = labelRect(ctx, x, y, t, '10px -apple-system, sans-serif', 'left', 'top').w;
  const leftFirst = (x + 4 + w > b.x + b.w);
  const a = leftFirst ? ['right', 'left'] : ['left', 'right'];
  for(const al of a){
    const xx = al === 'left' ? x + 4 : x - 4;
    if(al === 'left' && xx + w > b.x + b.w) continue;
    if(al === 'right' && xx - w < b.x) continue;
    if(labelIfClear(ctx, xx, y, t, col, '10px -apple-system, sans-serif', al, 'top')) return true;
  }
  return false;
}
function disc(ctx, x, y, r, col){
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
}
function ring(ctx, x, y, r, col, lw, dash){
  ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = lw || 1;
  if(dash) ctx.setLineDash(dash);
  ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); ctx.restore();
}
