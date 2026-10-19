
/* ================================================================== *
 *  PhET's constants (build 1.4.24: EFACConstants, HeatTransfer-       *
 *  Constants, Beaker, Block, Burner, Air, and the Systems elements).  *
 *  Every name follows PhET's; derive.py is the Python twin.            *
 * ================================================================== */
const T_ROOM=296;                         /* PhET's value: ROOM_TEMPERATURE, K */
const T_FREEZE=273.15;                    /* PhET's value: WATER_FREEZING_POINT_TEMPERATURE */
const T_BOIL={water:373.15, oil:573.15};  /* PhET's values: the beakers' boiling points */
const T_BLOCK_MAX=620;                    /* PhET's value: Block.getEnergyBeyondMaxTemperature */
/* PhET's values: specific heat J/(kg K) and density kg/m^3 */
const MAT_PHET={iron:{c:450,rho:7800}, brick:{c:840,rho:3300}, water:{c:3000,rho:1000}, oil:{c:1411,rho:916}};
/* the real materials, each from its source (see the header):
   iron  NIST-JANAF Fe(cr) Cp(298.15 K) = 25.094 J/(mol K) over IUPAC's 55.845 g/mol; 7874 kg/m^3 at 20 C (Arblaster 2018)
   brick 840 J/(kg K) (Wikipedia's building-materials table); density 1400-2400 (Engineering ToolBox), 1900 the middle
   water NIST Chemistry WebBook (IAPWS-95) at 296 K and 0.101325 MPa: cp 4.18232 J/(g K), 997.577 kg/m^3
   oil   1970 J/(kg K) (Engineering ToolBox, liquids); 911 kg/m^3 (specific gravity 0.911 at 20 C, USDA grading manual) */
const JANAF_FE_CP=25.094, M_FE=55.845;
const MAT_REAL={iron:{c:JANAF_FE_CP/M_FE*1000,rho:7874}, brick:{c:840,rho:1900}, water:{c:4182.32,rho:997.577}, oil:{c:1970,rho:911}};
const MAT_NAME={iron:'iron', brick:'brick', water:'water', oil:'olive oil'};
const BLOCK=0.045;                        /* PhET's value: BLOCK_SURFACE_WIDTH, m */
const BEAKER_W=0.085, BEAKER_H=0.085*1.1; /* PhET's values: the Intro beakers */
const FLUID0=0.5;                         /* PhET's value: INITIAL_FLUID_PROPORTION */
const DISPLACE=120;                       /* PhET's value: fluid proportion per m^2 of block under the surface */
const K_BODY=1000, K_AIR=30;              /* PhET's values: HeatTransferConstants, W/(m K) */
const MAXSTEP=1/60;                       /* PhET's value: MAX_HEAT_EXCHANGE_TIME_STEP */
const DT=1/60;                            /* PhET's value: SIM_TIME_PER_TICK_NORMAL; the remake's fixed step */
const EQ_THRESH=1e-6;                     /* PhET's value: TEMPERATURES_EQUAL_THRESHOLD */
const P_BURN=5e3, P_BURN_AIR=1500;        /* PhET's values: a burner's power into a body / into the air, W */
const BURNER_HALF=0.0375, BURNER_TOP=0.075; /* PhET's values: a burner is 7.5 cm square */
const AIR_W=0.7, AIR_H=0.85;              /* PhET's value: the air's box */
const AIR_M=10*(AIR_W*AIR_H*0.1), AIR_E=1012*AIR_M*T_ROOM, T_AIR=AIR_E/(1012*AIR_M);
/* PhET builds the air's contact area as Bounds2(-w/2, 0, w, h), so its maxX is
   0.7, not 0.35: harmless, since every body sits inside either box */
const AIR_AREA={x0:-AIR_W/2, y0:0, x1:AIR_W, y1:AIR_H, imm:true};
const MAXP=1e4;                           /* PhET's value: MAX_ENERGY_PRODUCTION_RATE, W */
const SPEED_FAST=4;                       /* PhET's value: the fast-forward factor */

/* dot's Utils.roundSymmetric and Utils.linear */
function roundSym(v){ const a=Math.floor(Math.abs(v)+0.5); return v<0?-a:a; }
function linearMap(a1,a2,b1,b2,a3){ return (b2-b1)/(a2-a1)*(a3-a1)+b1; }

/* the energy-chunk map: PhET anchors it on the brick, 1.25 chunks at 0 C and
   2.4 at room temperature, and uses it for every body */
const QB=3300*Math.pow(0.045,3)*840*273.15, ZB=3300*Math.pow(0.045,3)*840*296;
function gChunks(E){ return linearMap(QB,ZB,1.25,2.4,E); }
function fChunks(n){ return linearMap(1.25,2.4,QB,ZB,n); }
const EPC=fChunks(2)-fChunks(1);          /* PhET's ENERGY_PER_CHUNK, 5019.022 J */
function nChunks(E){ return Math.max(roundSym(gChunks(E)),0); }

/* PhET's six ground spots: burners on 2 and 3, the bodies on the others */
const SPOT_GAP=(0.568-0.085)/(6-1);
const SPOTS=[0,1,2,3,4,5].map(r=>roundSym(1e3*(SPOT_GAP*r+(0.0425-0.284)))/1e3);

/* ---- the Systems screen (PhET's values unless marked) ---- */
const OMEGA_MAX=3*Math.PI;                /* the crank's top speed, rad/s */
const CRANK_ACC=Math.PI/2;                /* rad/s^2 */
const FOOD_CHUNKS=21;                     /* INITIAL_NUMBER_OF_ENERGY_CHUNKS */
const FOOD0=FOOD_CHUNKS*EPC;
const BIKE_LOAD=MAXP, BIKE_FREE=MAXP/5;   /* chemical power at full crank with a load / without */
const BIKE_MECH=5/6;                      /* five chunks in six reach the pedals (one in six is body heat) */
const FALL_STEPS=24;                      /* the faucet's 400 ms delay, in 1/60-s steps */
const TAU_K=10;                           /* the teapot's energy-production rate decays 0.1 per second */
const STEAM=0.8;                          /* 80 % of the teapot's heat chunks become steam */
const KETTLE_CUT=30;                      /* W: PhET stops the steam below this with the burner off */
const GEN_R=0.039;                        /* the generator wheel's radius, m */
const TAU_W=5/3;                          /* the wheel: dw/dt = (r - 3w)/5 */
/* the wheel's efficiency at PhET's nominal 60 frames/s: w settles at
   0.039 x 0.5 x (P/60)/3 and the output is 10 kW x w/(pi/2): 13/(6 pi) */
const ETA_W=(GEN_R*0.5*(1/60)/3)*MAXP/(Math.PI/2);
const ETA_PANEL=0.68;
const HEAT_MAXP=5e3, HEAT_RAMP=0.5;       /* the beaker heater: W into the water at full heat; heat per second */
const HB_W=0.075, HB_H=0.0825;            /* the heater's beaker */
const HB_M=Math.PI*Math.pow(HB_W/2,2)*HB_H*FLUID0*MAT_PHET.water.rho;
const HB_C=HB_M*MAT_PHET.water.c;
const HB_L=2*HB_W+2*HB_H*FLUID0;          /* its perimeter to the air */
const LIGHT_FRAC={incandescent:0.65, fluorescent:0.8};   /* 35 % / 20 % of chunks radiate as heat */
const FAN_W=0.0051, FAN_MIN=4, FAN_ACC=4*Math.PI;       /* rad/s per watt; stalls below 4 rad/s; rad/s^2 */
const FAN_HEAT=1/14;                      /* PhET's counter at full power: 13 chunks of wind, then 1 of heat */
function sunFrac(c){ const i=1-c; return i===0?0:0.1+0.9*i; }
const CHUNK_V=0.04;                       /* ENERGY_CHUNK_VELOCITY, m/s */
