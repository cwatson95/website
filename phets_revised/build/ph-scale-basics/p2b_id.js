
/* ================================================================== *
 *  which sim this file is.  ph-scale-basics carries PhET's ONE screen *
 *  (Macro) and the analysis that belongs with it; this part and the   *
 *  head, the boot and the suite are all that differ from ph-scale,    *
 *  which supplies the chemistry, the state and the shared views by    *
 *  path (SHA-pinned in assemble.py).                                  *
 * ================================================================== */
const SIMID='ph-scale-basics';
const SIM_NAME='pH Scale: Basics';
const SIM_VER='1.7.5';
const TABS=[['beaker','the beaker'],['liquids','the liquids'],
            ['dilution','dilution'],['scale','the scale']];
/* PhET's Basics sim prints only a pH and a volume — no concentrations, no moles, no
   molecule counts — so the beaker readout drops those rows.  The scale view keeps them,
   because the two concentrations are what that view exists to explain. */
const SHOW_CONC=false;
