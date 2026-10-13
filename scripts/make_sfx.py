#!/usr/bin/env python3
"""Tự tổng hợp SFX (whoosh, ding, hit, riser) bằng numpy — không phụ thuộc giấy phép bên thứ ba."""
import argparse, os
import numpy as np, soundfile as sf
SR = 48000
def env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / r)
def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--out", default="assets"); a = p.parse_args()
    os.makedirs(a.out, exist_ok=True); rng = np.random.default_rng(0); t = lambda s: np.arange(int(SR * s)) / SR
    noise = rng.standard_normal(int(SR * 0.5)); w = np.convolve(noise, np.ones(40) / 40, "same") * np.sin(np.pi * t(0.5) / 0.5) ** 2
    out = {"whoosh": 0.6 * w / np.abs(w).max(), "ding": 0.5 * np.sin(2 * np.pi * 1320 * t(0.8)) * env(int(SR * .8), .002, .25),
           "hit": 0.8 * np.sin(2 * np.pi * 55 * t(0.7)) * env(int(SR * .7), .003, .2),
           "riser": 0.4 * np.sin(2 * np.pi * (200 + 600 * t(1.2)) * t(1.2)) * (t(1.2) / 1.2)}
    for k, v in out.items(): sf.write(os.path.join(a.out, k + ".wav"), v.astype(np.float32), SR)
    print("ok", ", ".join(out))
if __name__ == "__main__":
    main()
