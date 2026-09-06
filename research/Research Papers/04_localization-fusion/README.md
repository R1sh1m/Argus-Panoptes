# 04_localization-fusion - citations (no PDFs, methods already in code)
- SonicDisc: 8x HC-SR04 @45deg, ATmega328P, pin-change ISR parallel capture, 8 reads/10ms, I2C out. github.com/platisd/sonicdisc
- Hackster 5x array (Nano) + Hackster 2D tracking (2-4 sensors, cosine rule, nC2 weighted fuse, triangle check). Basis for reflector.py.
- IJARCCE 2025 / IJERT 2018 ultrasonic IPS: anchors + tag, ToF/TDoA multilateration, RF sync, Python trilateration viz, 5cm grid + buzzer/servo demo.
Argus: flood = SonicDisc parallel idea; reflector.py = Hackster fuse; grid eval = IJERT 2x2ft protocol.
