# Array Physics + Limits

## Wavelength
40kHz air: lambda = 343/40000 = 8.6mm. lambda/2 = 4.3mm for grating-lobe-free.
HC-SR04 dia ~16mm, spacing 41-44mm >> lambda/2 -> sidelobes expected.

## Resolution
- Range ~4mm (bandwidth limited, ring ~1ms)
- Lateral ~15-20deg main lobe with 4 elements
- Blind <2cm, beam 30deg cone, miss between sensors at close range
- Specular dropout on angled smooth metal/glass

## Modes
- Mode0 sequential: TOF trilateration, cm map
- Mode1 flood: 1Tx omni + 4Rx, full-matrix 4x4, no delay debug
- Mode2 phased: delay_m = (max_dist - dist_m)/c,
  dist_m = sqrt((Xm-Xf)^2 + Zf^2), phi = -2pi*dist/c* f
  Outer-first = converging spherical focus at (Xf, Zf 15-40cm).

## Claim cap
Air array = ROI navigator only. Micron cracks need contact + optics.
Document sidelobes, blind wedge, mirror miss in report.
