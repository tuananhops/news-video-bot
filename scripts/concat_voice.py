#!/usr/bin/env python3
"""Nối a0..aN.wav thành vo.wav và ghi timeline.json (starts, dur, T) cho bước dựng."""
import argparse, json, os, glob, subprocess
from common import duration

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dir", required=True); p.add_argument("--out", default="vo.wav")
    a = p.parse_args()
    n = len(glob.glob(os.path.join(a.dir, "a[0-9]*.wav")))
    files = [os.path.join(a.dir, f"a{i}.wav") for i in range(n)]
    lst = os.path.join(a.dir, "l.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", os.path.join(a.dir, a.out)], check=True)
    d = [duration(f) for f in files]; st = [sum(d[:i]) for i in range(n + 1)]
    json.dump({"starts": st, "dur": d, "T": st[-1]}, open(os.path.join(a.dir, "timeline.json"), "w"))
    print(f"{n} câu, tổng {st[-1]:.2f}s")

if __name__ == "__main__":
    main()
