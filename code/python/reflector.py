"""Reflector pipeline: TOF trilateration + weighted fuse + beam heatmap."""
import math
import numpy as np

POS = [0.0, 41.0, 85.0, 130.0]  # mm rail positions

def sound_speed(T=25.0):
    return 331.4 + 0.6 * T

def pair_xy(d1, d2, a):
    """Cosine-rule triangulation. Returns (x, y) or None if impossible."""
    if d1 + d2 <= a or d1 <= 0 or d2 <= 0:
        return None
    cos_t = (d1 * d1 + a * a - d2 * d2) / (2 * d1 * a)
    cos_t = max(-1.0, min(1.0, cos_t))
    theta = math.acos(cos_t)
    return (d1 * math.cos(theta), d1 * math.sin(theta))

def fuse_position(d, pos=POS):
    """nC2 weighted average, weight = baseline. Returns (X, Y, conf)."""
    xs, ys, ws = [], [], []
    n = len(d)
    for i in range(n):
        for j in range(i + 1, n):
            a = pos[j] - pos[i]
            r = pair_xy(d[i], d[j], a)
            if r is None:
                continue
            x = r[0] + pos[i]
            xs.append(x); ys.append(r[1]); ws.append(a)
    if not xs:
        return None
    w = np.array(ws); x = np.average(xs, weights=w); y = np.average(ys, weights=w)
    conf = float(np.sum(w) / (max(pos) - min(pos)) / (len(xs) or 1))
    return (float(x), float(y), min(1.0, conf))

def beam_power(tracks, thetas=range(-90, 91, 5)):
    """Placeholder delay-and-sum power scan. tracks: list of (pos, tof)."""
    # TODO: align envelopes by delay = dot(pos, dir)/c, sum^2
    return {t: 0.0 for t in thetas}

if __name__ == "__main__":
    print(fuse_position([300.0, 305.0, 310.0, 320.0]))
