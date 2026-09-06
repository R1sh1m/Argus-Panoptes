# Research Papers Index (open-only)

## 01_gelsight/ - Argus-Touch
| File | Paper | License | Derive for Argus |
|---|---|---|---|
| Yuan2017-GelSight-Review.pdf (26MB) | Yuan/Dong/Adelson Sensors 2017 | CC-BY MDPI | Photometric-stereo + Poisson, 20-30um, C310 @640x480 -> `gel_recon.py` |
| Dong2017-Improved-GelSight.pdf | Dong et al. arXiv:1708.00922 | arXiv open | Lambertian dome gel, uniform LED fix |
| Luo2019-LowCost-GelSight.pdf | Luo ViTac ICRA19 workshop | Workshop open | Cosmetic sponge skips degassing, C270 focus hack, UV markers |
| Dannoruwa2023-LowCost-Gelsight.pdf | Dannoruwa IPSL 2023 pp.54-63 | Open proceedings | 6.4x8.9x3.8cm box, 6-image capture, coin test, 66.67% |
| Wedge2021-GelSight-Wedge.pdf | GelSight Wedge ICRA21 | Open MIT | 1-2 light recon on curves, ball cal 2.4mm + Hough |

## 02_air-ultrasound-array/ - linear array + flood/phased
| File | Paper | License | Derive |
|---|---|---|---|
| Allevato2019-3D-Imaging-40kHz.pdf | Allevato et al. ICA2019 | Open DEGA | Waveguide lambda/2=4.3mm, DAS+Hilbert -> B/C-scan, FoV +-50deg 0.5-6m |
| Marzo2017-TinyLev.pdf | Marzo et al. APL 2017 via arXiv:1708.08711 | CC-BY / arXiv | Murata vs Ningbo phase SD 14deg = 3% loss, 20V, 4mm particle |
| Allevato2023-PhD-Thesis.url | Allevato PhD TUD 2023 doi:10.26083/tuprints-00024425 | Link only (landing is HTML) | Spiral 2.3deg vs rect 12deg, MEMS-mic + 1 PUT 30Hz cost trick |

## 03_contact-UT-EC-NDT/ - idea-of-cracks numbers
| File | Paper | License | Derive |
|---|---|---|---|
| Santos2023-UT-EC-Pipes.pdf (13MB) | Santos et al. Sensors 2023 | CC-BY MDPI | PAUT volume + PCB EC 25-turn coils, focal laws, temp 1%/55C |
| Tunukovic2026-Dual-UT-EC-WAAM.pdf | Tunukovic et al. NDTEI 2026 | Open Strathprints | PAUT dead-zone + EC array complement, pixel/feature/symbol fusion |
| Mohseni2020-Automated-EC-Steel.pdf | Mohseni et al. J NDE 2020 | Open PDF via Springer | Nortec 500S split-D 500kHz-3MHz, lift-off 30um, POD MIL-1823A |
| Rau2016-Turbine-EC-Rayleigh.url | Rau et al. WCNDT2016 | Link only (ndt.net 401 on curl) | 200um flaw target, 25MHz Rayleigh 191x74um @26dB - download manually if needed |

## 04_localization-fusion/ - citations only
- SonicDisc (8x HC-SR04 I2C scanner) - github.com/platisd/sonicdisc - sequential vs parallel capture
- Hackster 5x HC-SR04 array + 2D triangulation (cosine rule, nC2 weighted fuse)
- IJARCCE/IJERT ultrasonic IPS (TDOA multilateration, grid matrix)

## Copyright rule
Open/CC-BY/arXiv/NDT.net-open only in git. Paywalled IEEE -> citation, no PDF.
