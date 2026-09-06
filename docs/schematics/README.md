# Schematics — correctness record

Interactive: `argus-system.html` (self-contained, offline, 5 tabs).
Assumption: ESP32-DevKitC V4 38-pin + classic 5V HC-SR04.

## Internet assets used
- Espressif DevKitC V4 schematic PDF + J2/J3 pin tables (input-only 34/35 honored)
- WROOM-32 datasheet (3.3V limits, strapping)
- HC-SR04 datasheets: electronicoscaldas / electroschematics / handsontec
  (5V, 10µs Trig, 8×40kHz, Echo us/58=cm, 2-400cm ±3mm, 15°/30°, 60ms cycle)
- KiCad 8 official symbols only (no AI-drawn parts)

## Pin contract (matches firmware + code)
TRIG {25,26,27,14} OUT · ECHO {34,35,32,33} IN · POS {0,41,85,130}mm
Echo: 5V → 1k → GPIO tap + 2k → GND = 3.33V. Never 5V direct.
Temp: DS18B20 DQ → GPIO15 + 4.7k → 3V3. Power: 5V 2A star GND.

## PNG export
Open HTML in Chromium → tab → screenshot/SVG print to PNG for report.
Vector source = single file, no divergence.
