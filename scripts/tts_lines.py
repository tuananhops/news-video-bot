#!/usr/bin/env python3
"""Tạo giọng clone OmniVoice TỪNG CÂU MỘT (không batch), kiểm bằng ASR, tạo lại câu lỗi với seed khác.
Đầu ra trong --out: o{i}.wav (thô), a{i}.wav (48 kHz, có đệm 0.15 s), asrqc.json.
--dry-run: không nạp model, sinh tiếng bíp thay giọng để thử đường ống."""
import argparse, json, os, subprocess
import numpy as np, soundfile as sf
from asr_check import score, load_model, transcribe

SR = 24000

def trim(a, th=0.012):
    idx = np.where(np.abs(a) > th)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 1200] if len(idx) else a

def squeeze(a, max_pause_s=0.3):
    w = 480; n = len(a) // w; e = np.sqrt(np.mean(a[: n * w].reshape(n, w) ** 2, 1)); keep = []; run = 0
    lim = int(max_pause_s * SR / w)
    for k in range(n):
        run = run + 1 if e[k] < 0.006 else 0
        if run <= lim: keep.append(a[k * w:(k + 1) * w])
    return np.concatenate(keep + [a[n * w:]])

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--spec", required=True); p.add_argument("--out", required=True)
    p.add_argument("--voice-prompt", help="file VoiceClonePrompt (.pt) đã tạo từ giọng mẫu được phép dùng")
    p.add_argument("--model-id", default="k2-fsa/OmniVoice")
    p.add_argument("--seed", type=int, default=1234); p.add_argument("--steps", type=int, default=16)
    p.add_argument("--retry-steps", type=int, default=32); p.add_argument("--retries", type=int, default=3)
    p.add_argument("--tempo", type=float, default=1.0, help="atempo áp lên mỗi câu (1.0–1.2)")
    p.add_argument("--asr-model", default="small"); p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lines = [g["line"] for g in json.load(open(a.spec, encoding="utf-8"))["segments"]]
    if a.dry_run:
        def gen(i, seed, steps):
            t = np.arange(int(SR * (0.3 + 0.06 * len(lines[i].split())))) / SR
            return (0.3 * np.sin(2 * np.pi * (220 + 20 * i) * t)).astype(np.float32)
        check = lambda i: {"ok": True, "dry_run": True}
    else:
        import torch
        from omnivoice import OmniVoice, VoiceClonePrompt
        if not a.voice_prompt: p.error("--voice-prompt bắt buộc khi không --dry-run")
        model = OmniVoice.from_pretrained(a.model_id, device_map="cpu", dtype=torch.float32)
        prompt = VoiceClonePrompt.load(a.voice_prompt)
        asr = load_model(a.asr_model, 2)
        def gen(i, seed, steps):
            torch.manual_seed(seed)
            return np.asarray(model.generate(text=lines[i], voice_clone_prompt=prompt, num_step=steps)[0], np.float32)
        check = lambda i: score(lines[i], transcribe(asr, f"{a.out}/o{i}.wav"))
    log, unresolved = {}, []
    for i in range(len(lines)):
        for att in range(a.retries + 1):
            seed = a.seed + 101 * att
            sf.write(f"{a.out}/o{i}.wav", squeeze(trim(gen(i, seed, a.steps if att == 0 else a.retry_steps))), SR)
            r = check(i); log.setdefault(i, []).append({"seed": seed, **r})
            if r["ok"]: break
        else:
            unresolved.append(i)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{a.out}/o{i}.wav", "-af", f"atempo={a.tempo:.3f},apad=pad_dur=0.15",
                        "-ar", "48000", "-ac", "1", f"{a.out}/a{i}.wav"], check=True)
        print(f"câu {i}: {'OK' if i not in unresolved else 'LỖI'} sau {len(log[i])} lần", flush=True)
    json.dump({"log": log, "unresolved": unresolved}, open(f"{a.out}/asrqc.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if unresolved:
        print("Câu chưa đạt (sửa chữ/viết lại rồi chạy lại):", unresolved); raise SystemExit(2)

if __name__ == "__main__":
    main()
