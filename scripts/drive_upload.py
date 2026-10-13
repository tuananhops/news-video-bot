#!/usr/bin/env python3
"""Tải video lên thư mục Google Drive, hoặc chuyển file lỗi sang thư mục rác (KHÔNG BAO GIỜ xoá).
Cấu hình qua biến môi trường (không gõ cứng ID):
  GOOGLE_APPLICATION_CREDENTIALS = file service-account JSON (hoặc dùng connector Drive của bot)
  DRIVE_FOLDER_ID = <DRIVE_FOLDER_ID>      thư mục chính
  DRIVE_TRASH_FOLDER_ID = <TRASH_FOLDER_ID> thư mục rác
Dùng: drive_upload.py upload final.mp4 [--name N001_...mp4] | drive_upload.py trash <FILE_ID>
--dry-run: chỉ in việc sẽ làm. Giới hạn: từ chối file ≥ 100 MB."""
import argparse, os, sys

def svc():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    cred = service_account.Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
                                                                 scopes=["https://www.googleapis.com/auth/drive"])
    return build("drive", "v3", credentials=cred)

def need(var, dry):
    v = os.environ.get(var)
    if not v and not dry: sys.exit(f"Thiếu biến môi trường {var}")
    return v or f"<{var}>"

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("upload"); u.add_argument("file"); u.add_argument("--name")
    t = sub.add_parser("trash", help="chuyển file sang thư mục rác"); t.add_argument("file_id")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    if a.cmd == "upload":
        folder = need("DRIVE_FOLDER_ID", a.dry_run); mb = os.path.getsize(a.file) / 1e6
        if mb >= 100: sys.exit(f"{a.file} {mb:.1f} MB ≥ 100 MB: nén lại (CRF cao hơn) trước khi tải")
        name = a.name or os.path.basename(a.file)
        if a.dry_run: print(f"[dry-run] upload {a.file} ({mb:.1f} MB) as {name} -> {folder}"); return
        from googleapiclient.http import MediaFileUpload
        r = svc().files().create(body={"name": name, "parents": [folder]}, media_body=MediaFileUpload(a.file, resumable=True),
                                 fields="id,name", supportsAllDrives=True).execute()
        print("uploaded", r["id"], r["name"])
    else:
        trash = need("DRIVE_TRASH_FOLDER_ID", a.dry_run)
        if a.dry_run: print(f"[dry-run] move {a.file_id} -> {trash} (không xoá)"); return
        s = svc(); f = s.files().get(fileId=a.file_id, fields="parents", supportsAllDrives=True).execute()
        s.files().update(fileId=a.file_id, addParents=trash, removeParents=",".join(f.get("parents", [])), supportsAllDrives=True).execute()
        print("moved to trash folder", a.file_id)

if __name__ == "__main__":
    main()
