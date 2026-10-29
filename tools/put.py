#!/usr/bin/env python3
"""Commit+push one binary/blob into fofus-storage, print the raw URL.

    put.py <local-file> <repo-path> [--force]

Laws enforced: blob < 95MB; no LFS; allowed roots (products/, designai/, thumbs/).
"""
import subprocess, sys, os, json

def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()

REPO_DIR = os.environ.get("FOFUS_STORAGE_DIR", os.path.join(os.path.expanduser("~"), "fofus-storage"))
ROOTS = ("products/", "designai/", "thumbs/", "docs/")
MAXB = 95 * 1024 * 1024

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    src, rel = sys.argv[1], sys.argv[2]
    force = "--force" in sys.argv
    if not os.path.exists(src): sys.exit(f"no such file: {src}")
    if not rel.startswith(ROOTS):
        sys.exit(f"repo-path must start with one of {ROOTS}")
    sz = os.path.getsize(src)
    if sz > MAXB and not force: sys.exit(f"{sz/1e6:.1f} MB > 95MB cap (use --force at your own risk)")
    dest = os.path.join(REPO_DIR, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and not force: sys.exit(f"exists: {rel} (--force to overwrite)")
    open(dest,"wb").write(open(src,"rb").read())
    sh(f'cd {REPO_DIR} && git add "{rel}" && git commit -q -m "put: {rel} ({sz//1024} KB)" && git push -q origin main')
    url = f"https://raw.githubusercontent.com/reventer-bus/fofus-storage/main/{rel}"
    print(json.dumps({"path": rel, "bytes": sz, "url": url}, indent=1))

if __name__ == "__main__":
    main()
