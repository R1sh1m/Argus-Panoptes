"""Material cal: 10s fingerprint on good spot -> research/materials.json."""
import json
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "research" / "materials.json"

def fingerprint(samples):
    """samples: list of amplitudes. Returns {A0, noise} stub."""
    import statistics
    m = statistics.mean(samples)
    s = statistics.pstdev(samples) if len(samples) > 1 else 0.0
    return {"A0_ref": m, "noise": s}

def save_cal(material, fp):
    lib = json.loads(LIB.read_text()) if LIB.exists() else {}
    lib.setdefault(material, {}).update(fp)
    LIB.write_text(json.dumps(lib, indent=2))
    return lib[material]

if __name__ == "__main__":
    print("TODO: capture 10s good-spot amplitudes, then save_cal()")
