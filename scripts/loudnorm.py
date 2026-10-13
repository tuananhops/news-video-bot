#!/usr/bin/env python3
"""Chuẩn hoá loudness 2 lượt (mặc định -14 LUFS, TP -1.5 dBTP)."""
import argparse
from common import run, measure_loudness

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input"); p.add_argument("output")
    p.add_argument("--lufs", type=float, default=-14.0)
    p.add_argument("--tp", type=float, default=-1.5)
    p.add_argument("--sr", type=int, default=48000)
    a = p.parse_args()
    m = measure_loudness(a.input)
    af = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample={a.sr}")
    run(["ffmpeg", "-v", "error", "-y", "-i", a.input, "-af", af, "-ar", str(a.sr), a.output])
    r = measure_loudness(a.output)
    print(f"{a.output}: {r['input_i']} LUFS, TP {r['input_tp']} dBTP")

if __name__ == "__main__":
    main()
