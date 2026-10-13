#!/usr/bin/env python3
"""So lời nhận dạng (faster-whisper) với câu kịch bản cho từng file câu.
Dùng: asr_check.py --spec spec.json --wav-pattern 'o{i}.wav' [--lines 0 3]
In JSON {i: {sim, cover, len_ratio, ok, hyp}}."""
import argparse, json, re, difflib, subprocess
import numpy as np

NUM = set("không một hai ba bốn năm sáu bảy tám chín mười mươi mốt lăm tư trăm nghìn ngàn triệu tỷ tỉ linh lẻ phẩy phần".split())

def norm(s):
    s = s.lower().replace("-", " ")
    s = re.sub(r"(\d)[.,](\d)", r"\1\2", s)
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in s.split() if w not in NUM and not w.isdigit()]

def score(ref, hyp):
    r, h = norm(ref), norm(hyp)
    sm = difflib.SequenceMatcher(None, r, h, autojunk=False)
    cover = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(r))
    lr = len(h) / max(1, len(r))
    return {"sim": round(sm.ratio(), 2), "cover": round(cover, 2), "len_ratio": round(lr, 2),
            "ok": cover >= 0.5 and 0.6 <= lr <= 1.5, "hyp": hyp}

def load_model(name, threads):
    from faster_whisper import WhisperModel
    return WhisperModel(name, device="cpu", compute_type="int8", cpu_threads=threads)

def transcribe(model, wav):
    x = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]), np.float32)
    segs, _ = model.transcribe(x, language="vi", beam_size=5, condition_on_previous_text=False)
    return " ".join(s.text for s in segs)

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--spec", required=True, help="spec.json có segments[].line")
    p.add_argument("--wav-pattern", default="o{i}.wav")
    p.add_argument("--lines", type=int, nargs="*", help="chỉ kiểm các câu này")
    p.add_argument("--model", default="small"); p.add_argument("--threads", type=int, default=2)
    p.add_argument("--hyp-json", help="bỏ qua ASR, đọc lời nhận dạng sẵn {i: text} (để test)")
    a = p.parse_args()
    lines = [g["line"] for g in json.load(open(a.spec, encoding="utf-8"))["segments"]]
    idx = a.lines if a.lines else range(len(lines))
    if a.hyp_json:
        hyps = {int(k): v for k, v in json.load(open(a.hyp_json, encoding="utf-8")).items()}
    else:
        m = load_model(a.model, a.threads)
        hyps = {i: transcribe(m, a.wav_pattern.format(i=i)) for i in idx}
    print(json.dumps({i: score(lines[i], hyps[i]) for i in idx}, ensure_ascii=False))

if __name__ == "__main__":
    main()
