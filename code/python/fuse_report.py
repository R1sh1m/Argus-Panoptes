"""Fuse reflector + scatter + material -> report.json (Cantilever-lite)."""
import json
import argparse
from reflector import fuse_position
from scatter_metric import cloud_index

def fuse(d, z_scores, material="mild-steel"):
    pos = fuse_position(d)
    ci = cloud_index(z_scores)
    reflector_flag = bool(pos and pos[2] > 0.4)
    risk = "HIGH" if ci > 65 or reflector_flag else ("WATCH" if ci > 35 else "OK")
    return {
        "material": material,
        "position_mm": {"x": pos[0], "y": pos[1], "conf": pos[2]} if pos else None,
        "reflector_flag": reflector_flag,
        "cloud_index": round(ci, 1),
        "risk": risk,
    }

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--material", default="mild-steel")
    a = ap.parse_args()
    rep = fuse([300, 305, 310, 320], [0.2, 0.1], a.material)
    Path_out = "report.json"
    with open(Path_out, "w") as f:
        json.dump(rep, f, indent=2)
    print(json.dumps(rep, indent=2))
