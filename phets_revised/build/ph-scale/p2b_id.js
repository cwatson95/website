
/* ================================================================== *
 *  which sim this file is.  ph-scale carries PhET's three screens     *
 *  plus two analysis views; ph-scale-basics carries the Macro screen  *
 *  and the analysis that belongs with it (p2b_id.js differs between   *
 *  the two builds and nothing else in the engine does).               *
 * ================================================================== */
const SIMID='ph-scale';
const SIM_NAME='pH Scale';
const SIM_VER='1.7.6';
const TABS=[['beaker','the beaker'],['particles','the particles'],['graph','the graph'],
            ['my','my solution'],['dilution','dilution'],['scale','the scale']];
/* SHOW_CONC: PhET's Basics sim prints only a pH and a volume — no concentrations, no
   moles, no molecule counts — so the readout and the beaker view drop those rows there. */
const SHOW_CONC=true;
