#!/usr/bin/env python3
"""QC kỹ thuật: loudness (mặc định -14±0.5 LUFS), true peak ≤ -1 dBTP, dung lượng < 100 MB,
độ phân giải 720x1280, thời lượng, và (tuỳ chọn) asrqc.json không còn câu lỗi. Mã thoát 0 = đạt."""
import argparse, json, os, subprocess
from common import measure_loudness

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file"); p.add_argument("--lufs", type=float, default=-14); p.add_argument("--lufs-tol", type=float, default=0.5)
    p.add_argument("--max-tp", type=float, default=-1.0); p.add_argument("--max-mb", type=float, default=100)
    p.add_argument("--size", default="720x1280", help="WxH, 'none' để bỏ qua (file chỉ có âm thanh)")
    p.add_argument("--min-sec", type=float, default=0); p.add_argument("--max-sec", type=float, default=9999)
    p.add_argument("--asrqc", help="asrqc.json từ tts_lines.py")
    a = p.parse_args()
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", a.file]))
    dur = float(info["format"]["duration"]); mb = os.path.getsize(a.file) / 1e6; L = measure_loudness(a.file)
    I, TP = float(L["input_i"]), float(L["input_tp"])
    checks = {"loudness": abs(I - a.lufs) <= a.lufs_tol, "true_peak": TP <= a.max_tp, "size_mb": mb < a.max_mb,
              "duration": a.min_sec <= dur <= a.max_sec}
    if a.size != "none":
        v = [s for s in info["streams"] if s["codec_type"] == "video"]
        checks["resolution"] = bool(v) and f"{v[0]['width']}x{v[0]['height']}" == a.size
    if a.asrqc: checks["asr"] = not json.load(open(a.asrqc))["unresolved"]
    res = {"file": a.file, "lufs": I, "tp": TP, "mb": round(mb, 2), "sec": round(dur, 2), "checks": checks, "pass": all(checks.values())}
    print(json.dumps(res, ensure_ascii=False)); raise SystemExit(0 if res["pass"] else 1)

if __name__ == "__main__":
    main()
