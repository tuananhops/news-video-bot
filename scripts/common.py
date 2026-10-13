"""Hàm dùng chung: gọi ffmpeg/ffprobe, đọc cấu hình JSON."""
import json, subprocess

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)

def duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out)

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def measure_loudness(path):
    """Trả về dict loudnorm (input_i, input_tp, ...) của file âm thanh/video."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return json.loads(r[r.rfind("{"): r.rfind("}") + 1])
