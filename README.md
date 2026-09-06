# Argus-Panoptes
## ACOUSTICS BASED NON-DESTRUCTIVE STRUCTURAL ANALYSIS AND FLAW DETECTION

Low-cost (Rs.1000-5000) min-max ecosystem: minimum hardware, maximum software.
ESP32 + 4x HC-SR04 linear array (flood-first, phased-focus second) + compliant
contact piezo + material-adaptive AI -> Reflector + Scatter dual pipeline.

### Structure
- `research/` - study material, R&D notes, coupon logs, material library
- `code/fw/esp32_array/` - ESP32 firmware (Mode0 cal, Mode1 flood, Mode2 phased)
- `code/python/` - reflector, scatter, focus law, contact, material cal, fuse report
- `code/app/` - Streamlit dashboard (Cantilever-lite)

### Quick start
1. See `research/array-physics.md` for wavelength limits and claims.
2. Flash `code/fw/esp32_array/esp32_array.ino`, wire Echo via 1k/2k dividers.
3. `pip install -r code/python/requirements.txt`, run flood capture, then
   `python code/python/fuse_report.py --help`.

### Claim
Idea of cracks >=3-5mm open + pre-crack cloudiness via scatter index.
No micron UT claim with 40kHz air array. Lens is ground-truth labeler only.
