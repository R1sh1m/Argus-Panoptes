"""Transmit focus delay law for linear array (spherical converging)."""
import math

POS = [0.0, 41.0, 85.0, 130.0]

def focus_delays(Xf=65.0, Zf=300.0, c_mm_us=0.343, pos=POS):
    dists = [math.hypot(x - Xf, Zf) for x in pos]
    mx = max(dists)
    delays = [(mx - d) / c_mm_us for d in dists]  # us, outer-first
    phases = [(-2 * math.pi * d / 8.6) % (2 * math.pi) for d in dists]
    return {"dists": dists, "delays_us": delays, "phases_rad": phases}

if __name__ == "__main__":
    print(focus_delays())
