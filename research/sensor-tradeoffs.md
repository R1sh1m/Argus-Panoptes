# Sensor Tradeoffs (metal/glass cracks)

## Tier-1 Lens (USB scope 50-200x, oblique) - resolves 10-20um
Scan full area. Fails on mirror/rust/paint/closed cracks.

## Tier-1 Touch (gel + RGB) - ~16um depth, ~30um lateral
Press suspects. Complements bloom areas. Plane-remove 1st order.

## Chem (penetrant + 365nm UV) - Rs.600 highest ROI
Turns 10um open crack into mm indication.

## Tier-2 EC stretch (500kHz-1MHz pencil coil + GMR)
Closed/under-paint/subsurface 0.1-0.5mm. Null on good, Vpp+phase = crack.

## Tier-2 Contact piezo (1MHz disc + silicone pad + honey)
Pitch-catch along surface for curves >=25mm dia. Rock +/-15deg, pick max A0.
Glass: shorter burst 2-3 cycles, lower drive (long ring).

## Skip
Air UT for micron imaging. 5-25MHz PAUT (needs 100V + FPGA, out of budget).
Borrow lab for one validation day if available.

## Pipeline
clean -> penetrant -> lens scan -> touch-press -> EC/contact sweep ->
AI super-res + U-Net -> report.json
