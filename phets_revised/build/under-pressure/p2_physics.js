
/* ================================================================== *
 *  the physics: units, the hydrostatic law, the four pools, the       *
 *  chamber's Pascal solve and the paradox vessels.                    *
 *  Every closed form here is re-derived in build/under-pressure/      *
 *  derive.py and pinned to its printed output in selfTest.            *
 * ================================================================== */

/* ---- units: the DEFINITIONS, not rounded conversion factors -------------
   1 atm = 101325 Pa exactly (CGPM 1954).  1 lb = 0.45359237 kg and
   g_n = 9.80665 m/s^2 exactly (1959 international yard and pound), so
   1 lbf = 4.4482216152605 N exactly and 1 in = 0.0254 m exactly, giving
   1 psi = 6894.757293168361 Pa.  PhET 1.1.36 stores 9.8692e-6 atm/Pa and
   1.4504e-4 psi/Pa, which are these rounded; this file does not use them. */
const PA_PER_ATM=101325;
const LB_KG=0.45359237, G_STD=9.80665, INCH_M=0.0254, FT_M=0.3048;
const LBF_N=LB_KG*G_STD;
const PA_PER_PSI=LBF_N/(INCH_M*INCH_M);
const PA_PER_KPA=1000;
const PHET_ATM_PER_PA=9.8692e-6, PHET_PSI_PER_PA=1.4504e-4, PHET_FT_PER_M=3.2808399;

const UNITS={
  metric:     {id:'metric',     name:'kPa', per:PA_PER_KPA, dp:1, len:'m',  lenPer:1,    lenName:'metres'},
  atmosphere: {id:'atmosphere', name:'atm', per:PA_PER_ATM, dp:3, len:'m',  lenPer:1,    lenName:'metres'},
  english:    {id:'english',    name:'psi', per:PA_PER_PSI, dp:2, len:'ft', lenPer:FT_M, lenName:'feet'},
};
function toUnit(pa,u){ return pa/UNITS[u].per; }
function fromUnit(v,u){ return v*UNITS[u].per; }
function toLen(m,u){ return m/UNITS[u].lenPer; }

/* ---- PhET's values, read out of its minified build 1.1.36 -------------- */
const RHO_GASOLINE=700, RHO_WATER=1000, RHO_HONEY=1420;
const G_MARS=3.71, G_EARTH=9.8, G_JUPITER=24.9;
const P_AIR_0=101325;              /* Constants.EARTH_AIR_PRESSURE */
const P_AIR_HI=99490;              /* Constants.EARTH_AIR_PRESSURE_AT_500_FT */
const Y_LAPSE=150;                 /* getStandardAirPressure: linear(0,150,...) */
const LAPSE=(P_AIR_HI-P_AIR_0)/Y_LAPSE;         /* -12.2333... Pa/m */
const POOL_H=3;                    /* Constants.MAX_POOL_HEIGHT */
const DEPTH_OUT=2;                 /* THIS file's out-of-page depth (see header) */
const MYSTERY_RHO=[1700,840,1100];              /* Fluid A, B, C */
const MYSTERY_G=[20,14,6.5];                    /* Planet A, B, C */
const RHO_RANGE=[RHO_GASOLINE,RHO_HONEY], G_RANGE=[G_MARS,G_JUPITER];
/* the isothermal column, for the honesty note: p = p0 exp(-y/Hs) */
const RHO_AIR_ISA=1.225, H_SCALE=P_AIR_0/(RHO_AIR_ISA*G_STD);

/* the air pressure at height y.  PhET's model: a straight line over the first
   150 m, multiplied by g/g_earth (an atmosphere of the same mass per unit
   area under a different gravity).  Exponential truth is in airExact(). */
function airP(y,g,atmosphere){ return atmosphere?(P_AIR_0+LAPSE*y)*(g/G_EARTH):0; }
function airExact(y){ return P_AIR_0*Math.exp(-y/H_SCALE); }

/* p = p_air(at the free surface) + rho g h.  h is measured DOWN from the
   surface; nothing else enters, which is the whole of this sim. */
function pressureAt(depth,rho,g,ySurf,atmosphere){
  return airP(ySurf===undefined?0:ySurf,g,atmosphere)+rho*g*depth;
}
/* the inverses the mystery scene needs */
function rhoFromReading(p,g,depth,ySurf,atmosphere){
  return (p-airP(ySurf===undefined?0:ySurf,g,atmosphere))/(g*depth);
}
function gFromReading(p,rho,depth,ySurf,atmosphere){
  const yS=(ySurf===undefined?0:ySurf);
  return p/((atmosphere?(P_AIR_0+LAPSE*yS)/G_EARTH:0)+rho*depth);
}

/* ================================================================== *
 *  the pools.  PhET's world: metres, y up, y = 0 the ground, the pool *
 *  floor at y = -3.  Widths are cross-sections; areas carry DEPTH_OUT.*
 * ================================================================== */

/* ---- the square pool (PhET's SquarePoolModel) -------------------------- */
const SQ_X0=2.3, SQ_X1=6.0;
const SQ_W=SQ_X1-SQ_X0, SQ_A=SQ_W*DEPTH_OUT, SQ_VMAX=SQ_A*POOL_H;

/* ---- the trapezoid pool (PhET's TrapezoidPoolModel) --------------------
   widthTop 0.7, widthBottom 3.15, centres 3.2 and 3.2 + 3.22.  The two
   chambers taper equally and oppositely, so their widths SUM to a constant
   3.85 m at every height -- which is why the level is linear in the volume
   above the floor channel.  PhET's own bottom chamber stops at x = 6.0 while
   its right chamber's foot is at 6.07, leaving a 7 cm wedge that its
   isPointInsidePool reports as OUTSIDE the pool; this file runs the channel to
   6.2 so the fluid is one connected body at every height. */
const TZ_WTOP=0.7, TZ_WBOT=3.15, TZ_CTOP=3.2, TZ_SEP=3.22;
const TZ_CHAN={x0:4.0, x1:6.2, t1:0.21};
const TZ_CHAN_PHET_X1=6.0;
const TZ_WSUM=TZ_WTOP+TZ_WBOT;
function tzLeft(t){
  const a=TZ_CTOP-TZ_WBOT/2, b=TZ_CTOP-TZ_WTOP/2;
  const c=TZ_CTOP+TZ_WBOT/2, d=TZ_CTOP+TZ_WTOP/2;
  return [a+(b-a)*t/POOL_H, c+(d-c)*t/POOL_H];
}
function tzRight(t){
  const m=TZ_CTOP+TZ_SEP;
  const a=m-TZ_WTOP/2, b=m-TZ_WBOT/2;
  const c=m+TZ_WTOP/2, d=m+TZ_WBOT/2;
  return [a+(b-a)*t/POOL_H, c+(d-c)*t/POOL_H];
}
const TZ_WCHAN=tzRight(0)[1]-tzLeft(0)[0];      /* 5.145 m, constant over the band */
const TZ_VCHAN=TZ_WCHAN*TZ_CHAN.t1*DEPTH_OUT;
const TZ_VMAX=TZ_VCHAN+TZ_WSUM*(POOL_H-TZ_CHAN.t1)*DEPTH_OUT;
function tzWidth(t){
  if(t<0||t>POOL_H) return 0;
  return t<TZ_CHAN.t1?TZ_WCHAN:TZ_WSUM;
}
function tzVolume(t){
  t=clamp(t,0,POOL_H);
  return t<=TZ_CHAN.t1?TZ_WCHAN*t*DEPTH_OUT
                      :TZ_VCHAN+TZ_WSUM*(t-TZ_CHAN.t1)*DEPTH_OUT;
}
function tzLevel(V){
  V=clamp(V,0,TZ_VMAX);
  return V<=TZ_VCHAN?V/(TZ_WCHAN*DEPTH_OUT)
                    :TZ_CHAN.t1+(V-TZ_VCHAN)/(TZ_WSUM*DEPTH_OUT);
}
function tzInside(x,y){
  const t=y+POOL_H;
  if(t<0||t>POOL_H) return false;
  if(t<=TZ_CHAN.t1&&x>=TZ_CHAN.x0&&x<=TZ_CHAN.x1) return true;
  const L=tzLeft(t), R=tzRight(t);
  return (x>=L[0]&&x<=L[1])||(x>=R[0]&&x<=R[1]);
}

/* ---- the chamber pool (PhET's ChamberPoolModel) ------------------------ */
const CH_L_W=0.5, CH_R_W=2.3;                   /* PhET's u and h */
const CH_A_L=CH_L_W*DEPTH_OUT, CH_A_R=CH_R_W*DEPTH_OUT;
const CH_RATIO=CH_A_R/CH_A_L;                   /* 4.6 exactly */
const CH_OPEN_BOT=-1.7;                         /* -(MAX_POOL_HEIGHT - 1.3) */
const CH_WATER=1.0;                             /* PhET's leftWaterHeight = 2.3 - 1.3 */
const CH_REST=CH_OPEN_BOT+CH_WATER;             /* both surfaces at rest: y = -0.7 */
const CH_LEFT={x0:1.55, x1:4.35};               /* PhET's leftChamber */
const CH_RIGHT={x0:6.27, x1:7.37};              /* PhET's rightChamber */
const CH_L_SHAFT={x0:2.7, x1:3.2};              /* PhET's leftOpening,  width 0.5 */
const CH_R_SHAFT={x0:5.67, x1:7.97};            /* PhET's rightOpening, width 2.3 */
const CH_MASSES=[{id:'m500',m:500,w:0.5,h:0.5},
                 {id:'m250a',m:250,w:0.5,h:0.25},
                 {id:'m250b',m:250,w:0.5,h:0.25}];
const CH_MASS_MAX=CH_MASSES.reduce((t,o)=>t+o.m,0);

/* Pascal.  dp = F/A_left is the SAME everywhere in the connected fluid.
   Matching the pressure at one point by the two routes gives
   dp = (rho g + lambda) dh with lambda = d(p_air)/dy, and because
   dp = Mg/A_left and lambda = LAPSE g/g_earth both carry g, g cancels:

        dh = M / (A_left (rho + LAPSE/g_earth))       atmosphere on
        dh = M / (A_left rho)                          atmosphere off

   i.e. the air subtracts its own 1.2483 kg/m^3 from the fluid's density.
   Volume conservation splits dh in inverse proportion to the two areas. */
function rhoEff(rho,atmosphere){ return rho+(atmosphere?LAPSE/G_EARTH:0); }
function pascal(M,rho,g,atmosphere){
  const dp=M*g/CH_A_L;
  const dhRaw=M/(CH_A_L*rhoEff(rho,atmosphere));
  /* the left column cannot fall below the foot of its shaft */
  const dLraw=dhRaw*CH_A_R/(CH_A_L+CH_A_R);
  const capped=dLraw>CH_WATER;
  const dL=capped?CH_WATER:dLraw;
  const dR=dL*CH_A_L/CH_A_R;
  return {dp:dp, dh:dL+dR, dhRaw:dhRaw, dL:dL, dR:dR, capped:capped,
          yL:CH_REST-dL, yR:CH_REST+dR,
          Fin:M*g, Fout:dp*CH_A_R, mult:CH_RATIO,
          Mmax:CH_WATER*(CH_A_L+CH_A_R)/CH_A_R*CH_A_L*rhoEff(rho,atmosphere)};
}
/* the pressure anywhere in or above the chamber pool */
function chamberPressure(x,y,P,rho,g,atmosphere){
  const inL=(x>=CH_L_SHAFT.x0&&x<=CH_L_SHAFT.x1);
  const inR=(x>=CH_R_SHAFT.x0&&x<=CH_R_SHAFT.x1);
  const inBody=(y<=CH_OPEN_BOT&&y>=-POOL_H&&
                ((x>=CH_LEFT.x0&&x<=CH_LEFT.x1)||(x>=CH_RIGHT.x0&&x<=CH_RIGHT.x1)||
                 (x>=CH_LEFT.x1&&x<=CH_RIGHT.x0&&y<=-2.25&&y>=-2.75)));
  /* above the ground it is air everywhere, as in PhET */
  if(y>0) return {p:airP(y,g,atmosphere),wet:false,out:false,surf:null,side:'air'};
  if(y>CH_OPEN_BOT){
    if(inL&&y<=P.yL) return {p:airP(P.yL,g,atmosphere)+P.dp+rho*g*(P.yL-y),wet:true,out:false,surf:P.yL,side:'left'};
    if(inR&&y<=P.yR) return {p:airP(P.yR,g,atmosphere)+rho*g*(P.yR-y),wet:true,out:false,surf:P.yR,side:'right'};
    if(inL||inR) return {p:airP(y,g,atmosphere),wet:false,out:false,surf:null,side:'air'};
    return {p:0,wet:false,out:true,surf:null,side:'ground'};   /* solid, between the shafts */
  }
  if(!inBody) return {p:0,wet:false,out:true,surf:null,side:'ground'};
  return {p:airP(P.yR,g,atmosphere)+rho*g*(P.yR-y),wet:true,out:false,surf:P.yR,side:'body'};
}

/* ================================================================== *
 *  the hydrostatic paradox: four vessels, one base, one depth         *
 * ================================================================== */
const PAR_H=2.0, PAR_WB=1.2;
const VESSELS=[
  {id:'straight',name:'straight',prof:[[0,PAR_WB],[PAR_H,PAR_WB]]},
  {id:'flared',  name:'flared',  prof:[[0,PAR_WB],[PAR_H,3.0]]},
  {id:'tapered', name:'tapered', prof:[[0,PAR_WB],[PAR_H,0.35]]},
  /* named for the shape it IS: a narrow cylinder that steps out to a wide one.
     It was called "flask" until the PNG pass, where a flask's narrow NECK is
     at the top and this one's is at the bottom -- a caption contradicting its
     own picture (Known-bad). */
  {id:'stepped', name:'stepped', prof:[[0,PAR_WB],[0.55*PAR_H,PAR_WB],[0.62*PAR_H,2.6],[PAR_H,2.6]]},
];
function profW(prof,y){
  if(y<=prof[0][0]) return prof[0][1];
  for(let i=0;i<prof.length-1;i++){
    const [y0,w0]=prof[i], [y1,w1]=prof[i+1];
    if(y<=y1) return y1===y0?w0:w0+(w1-w0)*(y-y0)/(y1-y0);
  }
  return prof[prof.length-1][1];
}
/* the trapezium rule is EXACT on a piecewise-linear profile */
function profVolume(prof,H,depth){
  depth=depth===undefined?DEPTH_OUT:depth;
  let V=0;
  for(let i=0;i<prof.length-1;i++){
    const [y0]=prof[i], [y1]=prof[i+1];
    if(y1<=0||y0>=H) continue;
    const a=Math.max(y0,0), b=Math.min(y1,H);
    V+=0.5*(profW(prof,a)+profW(prof,b))*(b-a)*depth;
  }
  return V;
}
/* the VERTICAL component of the pressure the side walls exert on the fluid,
   integrated directly: int p(y) w'(y) D dy with gauge p = rho g (H - y).
   Each wall contributes p w'/2 and there are two of them.  This is computed
   WITHOUT the force balance, so comparing it against W - F_base is a check. */
function profWallVertical(prof,H,rho,g,depth){
  depth=depth===undefined?DEPTH_OUT:depth;
  let F=0;
  for(let i=0;i<prof.length-1;i++){
    const [y0,w0]=prof[i], [y1,w1]=prof[i+1];
    if(y1<=y0||y1<=0||y0>=H) continue;
    const a=Math.max(y0,0), b=Math.min(y1,H), k=(w1-w0)/(y1-y0);
    F+=rho*g*k*depth*((H*b-b*b/2)-(H*a-a*a/2));
  }
  return F;
}
/* a brute-force check of the same integral, for selfTest */
function profWallVerticalSum(prof,H,rho,g,n,depth){
  depth=depth===undefined?DEPTH_OUT:depth;
  let F=0; const dy=H/n;
  for(let i=0;i<n;i++){
    const ya=i*dy, yb=(i+1)*dy, ym=(ya+yb)/2;
    F+=rho*g*(H-ym)*(profW(prof,yb)-profW(prof,ya))*depth;
  }
  return F;
}
function vesselStats(v,rho,g,H){
  H=H===undefined?PAR_H:H;
  const V=profVolume(v.prof,H), W=rho*g*V;
  const pBase=rho*g*H, Abase=profW(v.prof,0)*DEPTH_OUT, Fbase=pBase*Abase;
  const Fwall=profWallVertical(v.prof,H,rho,g);
  return {id:v.id,name:v.name,V:V,W:W,pBase:pBase,Abase:Abase,Fbase:Fbase,
          Fwall:Fwall,ratio:Fbase/W,resid:Math.abs(Fwall-(W-Fbase))};
}
