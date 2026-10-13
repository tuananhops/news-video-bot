#!/usr/bin/env python3
"""Tạo contact sheet (lưới khung hình) để tự soát bằng mắt trước khi tải lên."""
import argparse, subprocess
from common import duration

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("video"); p.add_argument("--out", default="contact_sheet.jpg")
    p.add_argument("--cols", type=int, default=6); p.add_argument("--rows", type=int, default=4); p.add_argument("--width", type=int, default=240)
    a = p.parse_args()
    n = a.cols * a.rows; fps = n / max(0.1, duration(a.video))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", f"fps={fps:.4f},scale={a.width}:-2,tile={a.cols}x{a.rows}",
                    "-frames:v", "1", a.out], check=True)
    print(a.out)

if __name__ == "__main__":
    main()
