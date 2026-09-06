# code/
- `fw/esp32_array/esp32_array.ino` flash first, CMD CAL/FLOOD/FOCUS over Serial.
- `python/requirements.txt` pip install, then reflector/scatter/focus stubs.
- `app/streamlit_app.py` run `streamlit run code/app/streamlit_app.py`.
Echo wiring: 5V Echo -> 1k/2k divider -> ESP32 GPIO. Never 5V direct.
