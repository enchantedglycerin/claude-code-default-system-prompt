#!/usr/bin/env python3
"""Carve the embedded JavaScript bundle out of a Bun-compiled `claude` binary.

Claude Code ships as a Bun standalone executable: the app logic is JavaScript
embedded as *source text* (minified), not native code — so no decompiler is
needed, just extraction. This finds the high-density text region and writes it
to _bundle.js, which analyze.py then reads.

Usage:
  python extract_bundle.py [path-to-claude(.exe)] [-o _bundle.js]

The bundle is Anthropic's code; keep _bundle.js local (don't commit it).
"""
import sys, os, argparse

def find_claude():
    for p in (os.environ.get("CLAUDE_CODE_EXECPATH"),
              os.path.expanduser("~/.local/bin/claude.exe"),
              os.path.expanduser("~/.local/bin/claude")):
        if p and os.path.exists(p):
            return p
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary", nargs="?", default=find_claude())
    ap.add_argument("-o", "--out", default="_bundle.js")
    ap.add_argument("--block", type=int, default=1024*1024)
    a = ap.parse_args()
    if not a.binary or not os.path.exists(a.binary):
        sys.exit("claude binary not found; pass its path explicitly")

    data = open(a.binary, "rb").read()
    B = a.block
    def dens(c): return sum(1 for b in c if 0x20 <= b <= 0x7e or b in (9,10,13)) / max(1, len(c))

    # find the longest contiguous run of high-printable-density blocks (the JS bundle)
    best=(0,0); cur_start=None
    for off in range(0, len(data), B):
        if dens(data[off:off+B]) > 0.95:
            if cur_start is None: cur_start = off
        else:
            if cur_start is not None:
                if off-cur_start > best[1]-best[0]: best=(cur_start, off)
                cur_start=None
    if cur_start is not None and len(data)-cur_start > best[1]-best[0]:
        best=(cur_start, len(data))
    start, end = best
    if start==end:
        sys.exit("no JS text region found — is this a Bun-compiled binary?")
    # widen by one block each side to catch edges
    start=max(0, start-B); end=min(len(data), end+B)
    chunk = data[start:end].decode("latin-1")   # lossless byte->char
    open(a.out, "w", encoding="utf-8", errors="replace").write(chunk)
    print(f"extracted {len(chunk):,} chars from {start//B}MB..{end//B}MB of {os.path.basename(a.binary)} -> {a.out}")

if __name__ == "__main__":
    main()
