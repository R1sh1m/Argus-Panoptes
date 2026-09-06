"""Contact piezo acquire: burst, gain auto, coupling QC, rock-sweep."""
# TODO: ESP32 ADC envelope + AD9833 drive. This stub defines the record schema.

def coupling_ok(A0_coupled, A0_air, thresh_dB=6.0):
    import math
    return (20 * math.log10((A0_coupled + 1e-9) / (A0_air + 1e-9))) > thresh_dB

def rock_sweep(read_fn, angles=(-15, -7, 0, 7, 15)):
    """read_fn(angle)-> amplitude. Returns best (angle, amp)."""
    best = (angles[0], -1)
    for a in angles:
        v = read_fn(a)
        if v > best[1]:
            best = (a, v)
    return best

if __name__ == "__main__":
    print(rock_sweep(lambda a: 100 - abs(a)))
