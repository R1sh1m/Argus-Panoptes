# Argus-Panoptes Mark-II: BOM, Procurement, Cost & Usability Specification
## Budget-Optimized Hardware Plan & Defect Inspection Scope for BACSE291

**Course:** BACSE291 — Innovative Design Project (Fall 2026–27)  
**Project:** Argus-Panoptes Multimodal Inspection Probe  
**Revision:** v1.0  
**Target:** Low-Cost, Real-World Prototyping in India

---

## 1. Executive Summary

The objective of the **Argus-Panoptes Mark-II** probe is to deliver a practical, handheld, non-destructive testing (NDT) instrument capable of sub-surface void detection and surface distance normalization without expensive industrial equipment or messy ultrasound couplant gels.

To make the system physically buildable within a realistic engineering student budget, this document outlines:
1. **Component sourcing within India** (Robu.in, QuartzComponents, Tanotis, MakerBazar).
2. **Tiered budget configurations** ranging from an ultra-low-cost prototype (< ₹5,000) to a high-precision student tier (~₹10,000).
3. **Rigorous usability assessment**: Physical capabilities and clear detection boundaries for academic review defense.

---

## 2. Component Procurement & Cost Breakdown (INR)

### Component Rationale & Vendor Options

```
+-----------------------------------------------------------------------------------------+
|                                    PROBE HARDWARE STACK                                 |
|                                                                                         |
|  [ mmWave FMCW Radar ]           [ ToF LiDAR ]                   [ 9-DoF IMU ]          |
|  DFRobot C4001 (60 GHz)          Benewake TF-Luna (8m)           Bosch BNO055 /         |
|  or HLK-LD2450 (24 GHz)          850nm Micro-Laser               MPU-6050               |
|  (₹1,100 – ₹4,200)               (₹2,200 – ₹2,600)               (₹220 – ₹2,600)        |
|            |                              |                             |               |
|            +------------------------------+-----------------------------+               |
|                                           |                                             |
|                                           v                                             |
|                             [ ESP32-S3-DevKitC-1 N8R8 ]                                 |
|                             Dual-Core LX7 + 8MB PSRAM                                   |
|                             (₹750 – ₹950)                                               |
|                                           |                                             |
|                                           v                                             |
|                             [ Power & Interface Layer ]                                 |
|                             2S Li-ion / 5V 3A Buck + 0.96" OLED + 3D Shell              |
|                             (₹900 – ₹1,200)                                             |
+-----------------------------------------------------------------------------------------+
```

### Detailed Itemized Cost Matrix

| Item # | Subsystem | Component Description | Primary Indian Source | Estimated Cost (₹) |
|---|---|---|---|---|
| **1** | **Compute & DSP** | **ESP32-S3-DevKitC-1-N8R8**<br>(Xtensa Dual-Core 240MHz, 8MB Octal PSRAM, 8MB Flash) | Robu.in / QuartzComponents | **₹750 – ₹950** |
| **2A** | **Radar (Option A: 60GHz)** | **DFRobot C4001 60 GHz mmWave Radar Module**<br>(4GHz sweep, UART, high axial resolution) | Robu.in / Tanotis / MakerBazar | **₹3,800 – ₹4,500** |
| **2B** | **Radar (Option B: 24GHz)** | **Hi-Link HLK-LD2450 24 GHz FMCW Radar**<br>(Cost-optimized alternative, UART output) | Robu.in / QuartzComponents | **₹1,100 – ₹1,400** |
| **3** | **Surface LiDAR** | **Benewake TF-Luna Micro ToF Distance Sensor**<br>(850nm VCSEL, 8m range, 100Hz UART, 8g weight) | Robu.in / Robokits / Tanotis | **₹2,200 – ₹2,600** |
| **4A** | **Tracking (Option A: 9-Axis)** | **Bosch BNO055 9-DoF Intelligent IMU**<br>(Internal Cortex-M0 fusion, Quaternion out over I2C) | Robu.in / QuartzComponents | **₹2,400 – ₹2,800** |
| **4B** | **Tracking (Option B: 6-Axis)** | **InvenSense MPU-6050 6-Axis IMU**<br>(Budget alternative running Madgwick on ESP32-S3) | Robu.in / QuartzComponents | **₹200 – ₹250** |
| **5** | **On-Probe Display** | **0.96-inch I2C Monochrome OLED Display (SSD1306)**<br>(128x64 pixels, 3.3V logic) | Robu.in / Amazon.in | **₹180 – ₹220** |
| **6** | **Power Supply** | **2x 18650 2600mAh Li-ion Cells + 2S BMS + 5V 3A Buck**<br>(Dedicated clean rail for radar current spikes) | Robu.in / Local electronics market | **₹550 – ₹750** |
| **7** | **Chassis & Hardware** | **3D-Printed Ergonomic Probe Housing + Pushbuttons**<br>(PLA/PETG print from campus 3D lab / local service) | College Innovation Lab | **₹300 – ₹500** |

---

## 3. Recommended Budget Configurations

### Tier 1: The "Sweet Spot" Recommended Build (~₹10,500)
* **Configuration:** ESP32-S3 + DFRobot C4001 (60 GHz) + TF-Luna LiDAR + BNO055 + 2S Battery + OLED + 3D Shell.
* **Total Investment:** **₹10,180 – ₹12,320**
* **Why this is recommended:**
  - 60 GHz wavelength ($\lambda \approx 5\ \text{mm}$) provides superior sub-surface axial resolution ($\approx 1.8\ \text{cm}$ raw Fourier bin, sub-mm phase tracking).
  - BNO055 eliminates drift tuning math from the ESP32.
  - TF-Luna provides ground-truth optical surface distance to isolate internal flaws.

### Tier 2: The "Ultra-Budget Prototype" (< ₹5,500)
* **Configuration:** ESP32-S3 + HLK-LD2450 (24 GHz) + TF-Luna LiDAR + MPU-6050 + USB Power Bank + OLED.
* **Total Investment:** **₹4,830 – ₹5,420**
* **Engineering Tradeoffs:**
  - 24 GHz wavelength ($\lambda \approx 12.5\ \text{mm}$) has lower axial resolution, but penetrates deeply into drywall, wood, and thick composite slabs.
  - MPU-6050 requires running an open-source Madgwick filter on ESP32-S3 Core 0 to compute orientation quaternions.

### Tier 3: Industrial Lab / Sponsored Build (~₹35,000+)
* **Configuration:** Texas Instruments IWR6843AOPEVM + DCA1000EVM Real-Time Raw ADC Capture Board + ESP32-S3 Host.
* **Note:** Only feasible if sponsored by a university research lab or departmental grant.

---

## 4. Real-World Usability & Inspection Matrix

In an academic review or viva panel, examiners evaluate whether students understand the physical boundaries of their chosen sensors.

### 4.1 Target Material Suitability Matrix

| Material Type | Penetration Ability | Primary Target Defects | Expected Performance |
|---|---|---|---|
| **Fiberglass Composites (GFRP)** | **Excellent (3–10 cm)** | Delaminations, resin starvation, dry spots | **High.** Non-contact detection without couplant gel. |
| **Drywall & Gypsum Board** | **Excellent (10–30 cm)** | Stud location, hidden PVC pipes, water leakage | **High.** Instant detection through painted drywall. |
| **Hardwood & Engineered Wood** | **Good (5–15 cm)** | Internal termite hollows, rot, foreign inclusions | **High.** Strong dielectric contrast between wood & air. |
| **Cast Acrylic / Epoxy / Plastics** | **Excellent (5–20 cm)** | Air bubbles, shrinkage cavities, density changes | **High.** Clean interface reflections at void boundaries. |
| **Dry Mortar & Concrete Slabs** | **Moderate (5–12 cm)** | Rebar embedment depth, internal voids | **Moderate.** Attenuation increases with moisture content. |
| **Structural Steel & Aluminum** | **Zero Penetration (Surface only)** | Paint thickness, surface pittings | **Surface Only.** EM waves reflect completely ($R \approx 1$) at conductors. |

### 4.2 Key Advantages Over Traditional Methods
1. **Completely Couplant-Free:** Traditional contact ultrasonic testing (UT) requires grease, honey, or ultrasonic gel. This probe operates 5–15 cm away in free air.
2. **Immune to Surface Vibration & Tilt:** The BNO055 tracks hand tilt in real time, allowing software to apply Snell's Law angle correction and project reflections into true vertical depth.
3. **Optically Gated Surface Isolation:** TF-Luna laser distance measurement prevents the outer surface reflection from masking defects located immediately beneath the skin.

---

## 5. Review Panel / Viva Defense FAQ

**Q1: Why not use 40 kHz airborne ultrasound like the original baseline?**  
*Answer:* Airborne 40 kHz ultrasound suffers from severe acoustic impedance mismatch ($Z_{air} \approx 415\ \text{Pa}\cdot\text{s/m}$ vs $Z_{solid} > 10^6\ \text{Pa}\cdot\text{s/m}$), reflecting $>99.99\%$ of incident energy at the surface. 60 GHz electromagnetic waves cross dielectric boundaries with low insertion loss, enabling internal sub-surface penetration.

**Q2: Can this probe inspect internal cracks inside solid steel?**  
*Answer:* No. Electromagnetic radiation at microwave frequencies cannot penetrate electrical conductors due to the skin effect ($\delta < 0.5\ \mu\text{m}$ in steel at 60 GHz). For solid metals, the probe detects surface topography and coating thickness, while internal metal flaws require contact ultrasound or eddy current testing.

**Q3: How does the LiDAR assist the radar?**  
*Answer:* The radar suffers from near-field mutual coupling and a large front-surface dielectric echo. The co-axial LiDAR measures the optical surface distance $d_{surface}$ with millimeter precision. The microcontroller firmware then programmatically masks out all radar returns before $d_{surface}$, calculating true defect depth as $z_{defect} = \frac{d_{radar} - d_{surface}}{\sqrt{\epsilon_r}}$.

---

## 6. Physical Prototyping Roadmap

1. **Sprint 1 (Week 1–2):** Order ESP32-S3, TF-Luna, and chosen radar module from Robu.in. Validate concurrent dual-UART data ingestion on breadboard.
2. **Sprint 2 (Week 3–4):** Wire the BNO055 over I2C. Build the timestamped FreeRTOS binary aggregator task.
3. **Sprint 3 (Week 5–6):** Fabricate test coupons (15 mm PMMA plate with 3 mm blind drilled holes; drywall panel with embedded PVC pipe).
4. **Sprint 4 (Week 7–8):** Design and 3D print the handheld casing. Connect the OLED screen to display live distance, depth, and status.
5. **Sprint 5 (Week 9–10):** Stream live data to the Streamlit dashboard (`code/app/`) for real-time 2D/3D visualization during the project demonstration.
