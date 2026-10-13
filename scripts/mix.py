#!/usr/bin/env python3
"""Trộn giọng + nhạc nền (ducking) + SFX, chuẩn hoá -14 LUFS rồi ghép vào video.
mix.json: {"voice":"vo.wav","music":"assets/music.ogg","music_start":0,"music_gain":0.22,
           "sfx":[{"file":"assets/whoosh.wav","t":3.9,"gain":0.35}]}"""
import argparse, json, os, subprocess
from common import duration, measure_loudness

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True); p.add_argument("--video", required=True); p.add_argument("--out", default="final.mp4")
    p.add_argument("--lufs", type=float, default=-14); p.add_argument("--tp", type=float, default=-1.5)
    a = p.parse_args()
    base = os.path.dirname(os.path.abspath(a.config)); C = json.load(open(a.config, encoding="utf-8"))
    P = lambda f: os.path.join(base, f)
    T = duration(P(C["voice"])); inp = ["-i", P(C["voice"])]; fc = ["[0:a]aresample=48000,asplit[v1][v2]"]; mixin = ["[v1]"]
    if C.get("music"):
        inp += ["-ss", str(C.get("music_start", 0)), "-i", P(C["music"])]
        fc += [f"[1:a]aresample=48000,volume={C.get('music_gain', 0.22)},afade=t=in:d=0.5,afade=t=out:st={max(0, T - 1.5)}:d=1.5[m]",
               "[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md]"]; mixin.append("[md]")
    else:
        fc[0] = "[0:a]aresample=48000[v1]"
    off = 2 if C.get("music") else 1
    for k, s in enumerate(C.get("sfx", [])):
        inp += ["-i", P(s["file"])]; ms = int(s["t"] * 1000)
        fc.append(f"[{off + k}:a]aresample=48000,volume={s.get('gain', 0.3)},adelay={ms}|{ms},apad[s{k}]"); mixin.append(f"[s{k}]")
    fc.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first[mx]")
    raw = P("mix_raw.wav"); out_wav = P("mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[mx]", "-t", str(T), "-ac", "2", "-ar", "48000", raw], check=True)
    m = measure_loudness(raw)
    af = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", "48000", out_wav], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", out_wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out], check=True)
    print("ok", a.out)

if __name__ == "__main__":
    main()
