"""Scatter metrics: cloudiness proxies for sub-wavelength damage."""
import math

def ut_scatter(A, A0, width, width0, echo2=None, echo1=None):
    """Returns dict of dB drop, broadening, echo ratio."""
    out = {}
    out["A_drop_dB"] = 20 * math.log10((A + 1e-9) / (A0 + 1e-9))
    out["width_ratio"] = width / (width0 + 1e-9)
    if echo1 and echo2:
        out["A2_A1"] = echo2 / (echo1 + 1e-9)
    return out

def cloud_index(z_scores, weights=None):
    """Weighted mean of z-scores vs good coupon -> 0-100."""
    if not z_scores:
        return 0.0
    if weights is None:
        weights = [1.0] * len(z_scores)
    m = sum(z * w for z, w in zip(z_scores, weights)) / (sum(weights) or 1)
    return max(0.0, min(100.0, 50.0 + 15.0 * m))

if __name__ == "__main__":
    print(ut_scatter(A=300, A0=900, width=1.4, width0=1.0))
    print(cloud_index([2.0, 1.5, 2.5]))
