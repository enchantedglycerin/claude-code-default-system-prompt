#!/usr/bin/env python3
"""Analyze the extracted Claude Code JS bundle (_bundle.js).

Usage:
  python analyze.py <search-string> [before] [after]   # beautify region around a match
  python analyze.py --all <search-string>              # list all match offsets (context)
  python analyze.py --fn <name>                        # extract & beautify a whole function by name

Beautify-on-demand: the bundle is one big minified blob, so we locate a symbol,
carve the enclosing region, and run it through jsbeautifier to read it as real code.
"""
import sys, jsbeautifier

SRC = open("_bundle.js", encoding="utf-8", errors="replace").read()

def offsets(needle, mx=25):
    out=[]; s=0
    while True:
        i=SRC.find(needle,s)
        if i<0: break
        out.append(i); s=i+1
        if len(out)>=mx: break
    return out

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    if a[0] == "--all":
        needle=a[1]; hits=offsets(needle)
        print(f"{len(hits)} match(es) for {needle!r}:")
        for i in hits:
            ctx = SRC[i-40:i+60].replace("\n"," ")
            print(f"  @{i}: ...{ctx}...")
        return
    if a[0] == "--fn":
        name=a[1]
        import re as _re
        m=_re.search(r'function '+_re.escape(name)+r'\s*\(', SRC)
        if not m:
            m=_re.search(_re.escape(name)+r'\s*=\s*(?:async\s*)?(?:function)?\s*\([^)]*\)\s*=>?\s*\{', SRC)
        if not m:
            print("function not found"); return
        # find first { after the signature, then balance braces (best-effort)
        j=SRC.find("{", m.start()); depth=0; k=j
        while k < len(SRC):
            c=SRC[k]
            if c=="{": depth+=1
            elif c=="}":
                depth-=1
                if depth==0: k+=1; break
            k+=1
        opts=jsbeautifier.default_options(); opts.indent_size=2; opts.max_preserve_newlines=2
        print(f"// ===== function {name} @ offset {m.start()} ({k-m.start()} chars) =====")
        print(jsbeautifier.beautify(SRC[m.start():k], opts))
        return
    needle=a[0]
    before=int(a[1]) if len(a)>1 else 1600
    after=int(a[2]) if len(a)>2 else 2600
    hits=offsets(needle,5)
    if not hits:
        print("not found"); return
    opts=jsbeautifier.default_options(); opts.indent_size=2; opts.max_preserve_newlines=2
    for i in hits[:1]:
        region=SRC[max(0,i-before):i+after]
        print(f"// ===== region around offset {i} (in-bundle) =====")
        print(jsbeautifier.beautify(region, opts))

if __name__=="__main__":
    main()
