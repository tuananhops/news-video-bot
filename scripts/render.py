#!/usr/bin/env python3
"""Dựng video 9:16 từ shots.json (không gõ cứng đường dẫn).
shots.json: {"width":720,"height":1280,"fps":30,"font":"<đường dẫn .ttf>","timeline":"timeline.json",
  "shots":[{"type":"image","src":"assets/a.jpg","seg":0,"from":0.0,"to":1.0,"z0":1.0,"z1":1.12,"credit":"Ảnh: ... · CC BY 4.0","text":"CÚM A TĂNG ×7"},
           {"type":"stat","seg":3,"big":"779 CA","sub":"tuần 40"}],
  "captions":true}
- seg: chỉ số câu trong timeline; from/to: phần của câu (0..1) mà cảnh chiếm.
- image = Ken Burns (zoom z0→z1, lia fx0→fx1, fy0→fy1); stat = thẻ nền đen ô đỏ số lớn (tối đa 3 lần/video).
- captions: phụ đề 1–3 chữ trắng đậm viền đen, từ spec.json (--spec)."""
import argparse, json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

YEL, RED, WHITE = (255, 214, 0), (230, 30, 40), (255, 255, 255)

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--shots", required=True); p.add_argument("--spec", help="spec.json để làm phụ đề")
    p.add_argument("--out", default="video.mp4"); p.add_argument("--crf", type=int, default=21)
    p.add_argument("--max-seconds", type=float, help="chỉ dựng N giây đầu (thử nhanh)")
    a = p.parse_args()
    base = os.path.dirname(os.path.abspath(a.shots))
    C = json.load(open(a.shots, encoding="utf-8"))
    W, H, FPS = C.get("width", 720), C.get("height", 1280), C.get("fps", 30)
    tl = json.load(open(os.path.join(base, C.get("timeline", "timeline.json"))))
    st, du, T = tl["starts"], tl["dur"], tl["T"]
    if a.max_seconds: T = min(T, a.max_seconds)
    font_path = C.get("font") or "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fonts = {}
    def F(s):
        if s not in fonts: fonts[s] = ImageFont.truetype(font_path, s)
        return fonts[s]
    imgs = {}
    def img(src):
        if src not in imgs: imgs[src] = Image.open(os.path.join(base, src)).convert("RGB")
        return imgs[src]
    shots = []
    for s in C["shots"]:
        t0 = st[s["seg"]] + du[s["seg"]] * s.get("from", 0.0); t1 = st[s["seg"]] + du[s["seg"]] * s.get("to", 1.0)
        shots.append((t0, t1, s))
    words = []
    if C.get("captions", True) and a.spec:
        lines = [g["line"] for g in json.load(open(a.spec, encoding="utf-8"))["segments"]]
        for i, ln in enumerate(lines):
            w = ln.split(); chunks = [" ".join(w[k:k + 3]) for k in range(0, len(w), 3)]
            for k, c in enumerate(chunks):
                words.append((st[i] + du[i] * k / len(chunks), st[i] + du[i] * (k + 1) / len(chunks), c))
    rng = np.random.default_rng(3)
    dots = [(int(rng.integers(0, W)), int(rng.integers(0, H)), int(rng.integers(8, 16)), rng.random()) for _ in range(70)]
    def center(d, s, y, size, fill, stroke=5):
        f = F(size)
        while d.textlength(s, font=f) > W - 60 and size > 16: size -= 4; f = F(size)
        d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill="black")
    def frame(t):
        cur = next((x for x in shots if x[0] <= t < x[1]), shots[-1]); t0, t1, s = cur
        u = min(1, max(0, (t - t0) / max(1e-6, t1 - t0))); e = u * u * (3 - 2 * u); lt = t - t0
        if s["type"] == "image":
            im = img(s["src"]); iw, ih = im.size
            z = s.get("z0", 1.0) + (s.get("z1", 1.12) - s.get("z0", 1.0)) * e
            fx = s.get("fx0", .5) + (s.get("fx1", .5) - s.get("fx0", .5)) * e; fy = s.get("fy0", .5) + (s.get("fy1", .5) - s.get("fy0", .5)) * e
            sc = max(W / iw, H / ih) * z; cw, ch = W / sc, H / sc; x0, y0 = (iw - cw) * fx, (ih - ch) * fy
            out = im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
            out = Image.blend(out, Image.new("RGB", (W, H)), s.get("dark", 0.2))
            d = ImageDraw.Draw(out)
            if s.get("text"): center(d, s["text"], 180, 84, YEL)
            if s.get("credit"): d.text((16, H - 40), s["credit"], font=F(20), fill=WHITE, stroke_width=2, stroke_fill="black")
        else:
            out = Image.new("RGB", (W, H)); d = ImageDraw.Draw(out)
            for x, y, sz, ph in dots:
                if math.sin(t * 3 + ph * 6) > -0.6: d.rectangle((x, y, x + sz, y + sz), fill=RED)
            pop = int(120 * (1.3 - 0.3 * min(1, lt / 0.2)))
            for k, ln in enumerate(s.get("big", "").split("\n")): center(d, ln, 430 + k * (pop + 10), pop, WHITE, 0)
            if lt > 0.35: center(d, s.get("sub", ""), 600, 34, YEL, 0)
        for w0, w1, c in words:
            if w0 <= t < w1: center(d, c.upper(), int(H * 0.68), 64, WHITE, 6); break
        return out
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
    for k in range(int(T * FPS)): ff.stdin.write(frame(k / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    if ff.returncode: raise SystemExit(ff.returncode)
    print(f"{a.out}: {T:.2f}s, {len(shots)} cảnh")

if __name__ == "__main__":
    main()
