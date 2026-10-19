/* capture tail for center-and-variability.html — the display-list capture the
   layout audit and the rasteriser read.  Runs AFTER selfTest (run.js runs it
   on load), so a red suite means no capture, which is deliberate.  Never name
   a helper `run` here: JXA calls a top-level run() for you.  One file per
   canvas size: audit.py takes W and H from the file, so mixing sizes in one
   file reports the small captures as off-canvas. */
ObjC.import('Foundation');

/* the awkward cases are in here on purpose: an empty field, a field with too
   few kicks for a quartile, the smallest and largest data sets, the far ball */
const CAPCONFIGS=[
  ['kicks',              {view:'kicks'},                                   null],
  ['kicks sorted',       {view:'kicks',mSort:true,mPredict:true},          null],
  ['kicks line plot',    {view:'kicks',mPlot:'line',mKick:'k4'},           null],
  ['kicks empty',        {view:'kicks'},                                   'empty'],
  ['mean and median',    {view:'meanmed'},                                 null],
  ['mean and median 30', {view:'meanmed',aMax:30,aPredMean:true,aPredMed:true}, null],
  ['spread iqr',         {view:'spread'},                                  null],
  ['spread range',       {view:'spread',vMeasure:'range',vMean:true},      null],
  ['spread mad',         {view:'spread',vMeasure:'mad'},                   null],
  ['spread tools',       {view:'spread',vInterval:true,vPointer:true},     null],
  ['spread outlier set', {view:'spread'},                                  'outlier'],
  ['spread four kicks',  {view:'spread'},                                  'four'],
  ['which quartile',     {view:'conv'},                                    null],
  ['which quartile n5',  {view:'conv',cN:5},                               null],
  ['which quartile n29', {view:'conv',cN:29,cKick:'k3'},                   null],
  ['balance far',        {view:'balance',bMove:15},                        null],
  ['balance near',       {view:'balance',bMove:1,bN:25},                   null],
  ['long run 1000',      {view:'longrun'},                                 null],
  ['long run 10',        {view:'longrun',lN:10},                           null],
  ['long run 5000 k1',   {view:'longrun',lN:5000,lKick:'k1'},              null],
];
function capApply(cfg){
  Object.assign(ST,DEFAULTS,cfg[1]);
  resetWorlds();
  const F=curField(ST);
  if(cfg[2]==='empty'&&F) cavFieldClear(F);
  if(cfg[2]==='four'&&F){ cavFieldClear(F); cavFieldBatch(F,4); }
  if(cfg[2]==='outlier'&&F) F.xs=[1,5,6,6,7,7,8,15];
}
function capWrite(path,obj){
  const s=JSON.stringify(obj);
  $.NSString.alloc.initWithUTF8String(s)
    .writeToFileAtomicallyEncodingError(path,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+path+', '+s.length+' bytes');
}
function capSet(W2,H2,list){
  const out={W:W2,H:H2,views:{}};
  for(const cfg of list){
    capApply(cfg);
    const rc=makeRecorder(W2,H2);
    drawView(rc,W2,H2,buildModel(),ST);
    out.views[cfg[0].replace(/[^a-z0-9]+/gi,'_')]=rc.ops;
    console.log('  '+W2+'x'+H2+'  '+cfg[0]+': '+rc.ops.length+' ops');
  }
  return out;
}
capWrite('_out/display.json',capSet(1400,820,CAPCONFIGS));
capWrite('_out/display_narrow.json',capSet(560,380,
  CAPCONFIGS.filter((c,i)=>[0,4,6,12,15,17].indexOf(i)>=0)));
