#!/usr/bin/env python3
"""Kiểm tra trùng chủ đề với manifest (CSV: id,title,url,entities,date). Trùng nếu: cùng URL, hoặc
trùng ≥ --min-entities thực thể (tên riêng/con số), hoặc tiêu đề giống ≥ --title-sim.
Dùng: dedupe.py --manifest manifest.csv --title "..." --url "..." --entities "WWF;73%;Living Planet"
Mã thoát 1 nếu nghi trùng. --add để ghi chủ đề vào manifest khi không trùng."""
import argparse, csv, difflib, os, re, sys
from datetime import date

def toks(s): return set(re.findall(r"\w+", s.lower()))
def ents(s): return {e.strip().lower() for e in s.split(";") if e.strip()}
def canon(u): return re.sub(r"^https?://(www\.)?|[?#].*$|/$", "", u.strip().lower())

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifest", required=True); p.add_argument("--title", required=True)
    p.add_argument("--url", default=""); p.add_argument("--entities", default=""); p.add_argument("--id", default="")
    p.add_argument("--min-entities", type=int, default=2); p.add_argument("--title-sim", type=float, default=0.6)
    p.add_argument("--add", action="store_true")
    a = p.parse_args()
    rows = list(csv.DictReader(open(a.manifest, encoding="utf-8"))) if os.path.exists(a.manifest) else []
    hits = []
    for r in rows:
        why = []
        if a.url and r.get("url") and canon(a.url) == canon(r["url"]): why.append("cùng URL")
        common = ents(a.entities) & ents(r.get("entities", ""))
        if len(common) >= a.min_entities: why.append("thực thể chung: " + ", ".join(sorted(common)))
        sim = difflib.SequenceMatcher(None, sorted(toks(a.title)), sorted(toks(r.get("title", "")))).ratio()
        if sim >= a.title_sim: why.append(f"tiêu đề giống {sim:.2f}")
        if why: hits.append((r.get("id"), r.get("title"), why))
    for h in hits: print(f"NGHI TRÙNG {h[0]}: {h[1]} -> {'; '.join(h[2])}")
    if hits: sys.exit(1)
    print("Không trùng.")
    if a.add:
        new = not os.path.exists(a.manifest)
        with open(a.manifest, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new: w.writerow(["id", "title", "url", "entities", "date"])
            w.writerow([a.id, a.title, a.url, a.entities, date.today().isoformat()])

if __name__ == "__main__":
    main()
