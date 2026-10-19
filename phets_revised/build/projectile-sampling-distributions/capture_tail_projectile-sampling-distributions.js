/* capture tail for projectile-sampling-distributions.html — the display-list
   capture the layout audit and the rasteriser read.  Runs AFTER selfTest
   (run.js runs it on load), so a red suite means no capture, which is
   deliberate.  Never name a helper `run` here: JXA calls a top-level run()
   for you.  One file per canvas size: audit.py takes W and H from the file,
   so mixing sizes in one file reports the small captures as off-canvas. */
ObjC.import('Foundation');
function capWrite(path, obj) {
  const s = JSON.stringify(obj);
  $.NSString.alloc.initWithUTF8String(s)
    .writeToFileAtomicallyEncodingError(path, true, $.NSUTF8StringEncoding, $());
  console.log('wrote ' + path + ', ' + s.length + ' bytes');
}
function capSet(W2, H2, list) {
  const out = { W: W2, H: H2, views: {} };
  for (const cfg of list) {
    applyConfig(cfg);
    const rc = makeRecorder(W2, H2);
    drawView(rc, W2, H2, buildModel());
    out.views[cfg[0].replace(/[^a-z0-9]+/gi, '_')] = rc.ops;
    console.log('  ' + W2 + 'x' + H2 + '  ' + cfg[0] + ': ' + rc.ops.length + ' ops');
  }
  return out;
}
capWrite('_out/display.json', capSet(1400, 820, CONFIGS));
capWrite('_out/display_narrow.json', capSet(560, 380, CONFIGS.filter(
  (c, i) => [0, 6, 10, 15].indexOf(i) >= 0)));
