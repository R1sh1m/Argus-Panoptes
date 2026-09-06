# Gecko AIR Notes (geckorobotics.com/air)

AIR = AI + Robotics. Robots collect full-coverage first-order data,
Cantilever fuses + predicts. 2X life, -20% CapEx, -80% reactive.

## Sensing
PAUT Rapid AUT mm wall-thickness, TOFD weld cracks to 20cm, EC TriLat HIC,
cameras + Ouster Rev8 color lidar for digital twin. All co-registered.

## Stack (public signals)
ROS2 + MoveIt + Python/C++ edge, Fulcrum pipeline, Cantilever React/TS +
Unreal 3D, GCP/AWS/Azure + K8s + Terraform, Vertex AI, pytest/CI.

## Argus mapping (Rs.3500 vs millions)
PAUT thickness -> gel depth_um | camera+lidar -> phone+USB scope |
TOKA crawler -> hand-press + HC-SR04 stage | Fulcrum -> Python logger |
Cantilever twin -> Streamlit + report.json | predictive AI -> U-Net-MobileNet + FFT.

Steal architecture (fuse + decide), not sensors.
