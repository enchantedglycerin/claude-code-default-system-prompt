#!/usr/bin/env python3
r"""
generate_default_prompt.py  —  Auto-capture Claude Code's CURRENT default system prompt.

Instead of hardcoding anything, this spins up a tiny local endpoint, points a real
`claude` run at it via ANTHROPIC_BASE_URL, lets claude.exe assemble & send its real
request, captures the `system` field, and writes it out. Because it captures live in
the CURRENT working directory, paths are always correct for wherever you run it — no
hardcoded project dir, and it tracks Claude Code version upgrades automatically.

    python generate_default_prompt.py                     # interactive (cli) prompt -> claude_default_system_prompt.md
    python generate_default_prompt.py --mode print        # -p / SDK entrypoint (leaner; no PTY needed)
    python generate_default_prompt.py --identity          # also prepend the "You are Claude Code" identity line
    python generate_default_prompt.py --genericize        # replace machine/session paths with <PLACEHOLDERS>
    python generate_default_prompt.py --raw request.json  # also dump the full captured request

Notes:
  * Nothing is sent to Anthropic — the request is redirected to a localhost logger that
    returns an error, so no tokens are spent and no model reply is produced.
  * interactive mode needs pywinpty:  pip install pywinpty
  * The `# Scratchpad Directory` section contains a per-SESSION path; on reuse it is
    stale. Use --genericize (or delete that section) if you'll feed the file later.
"""
import argparse, http.server, socketserver, threading, json, gzip, os, re, sys, time


def make_handler(state):
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _read(self):
            n = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(n) if n else b""
            if self.headers.get("Content-Encoding", "").lower() == "gzip":
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass
            return raw

        def _json(self, code, obj):
            b = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)

        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

        def do_POST(self):
            raw = self._read()
            try:
                body = json.loads(raw.decode("utf-8", "replace"))
            except Exception:
                body = {}
            sysf = body.get("system")
            # Boot-time quota/health checks have no real system field -> answer 200 so the TUI proceeds.
            if not (isinstance(sysf, (list, str)) and len(sysf) > 0):
                self._json(200, {"id": "m", "type": "message", "role": "assistant",
                                 "model": body.get("model", "claude"),
                                 "content": [{"type": "text", "text": "ok"}],
                                 "stop_reason": "end_turn", "stop_sequence": None,
                                 "usage": {"input_tokens": 1, "output_tokens": 1}})
                return
            # Real conversation request WITH a system field -> capture it, then 400 to stop.
            if not state["captured"]:
                state["body"] = body
                state["captured"] = True
                state["event"].set()
            self._json(400, {"type": "error",
                             "error": {"type": "invalid_request_error", "message": "captured"}})
    return H


def _write(proc, s):
    try:
        proc.write(s)
    except Exception:
        pass


def capture(mode="interactive", timeout=60):
    state = {"captured": False, "body": None, "event": threading.Event()}
    httpd = socketserver.TCPServer(("127.0.0.1", 0), make_handler(state))
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    env = {k: v for k, v in os.environ.items()
           if not (k.startswith("CLAUDE") or k.startswith("ANTHROPIC")
                   or k in ("AI_AGENT", "CLAUDECODE"))}
    env["ANTHROPIC_BASE_URL"] = f"http://127.0.0.1:{port}"
    cwd = os.getcwd()
    probe = "hi"

    try:
        if mode == "interactive":
            try:
                from winpty import PtyProcess
            except ImportError:
                print("ERROR: interactive mode needs pywinpty.  pip install pywinpty  "
                      "(or use --mode print)", file=sys.stderr)
                sys.exit(2)
            proc = PtyProcess.spawn(["claude", probe], cwd=cwd, env=env, dimensions=(40, 120))
            start = time.time(); step = 0
            while time.time() - start < timeout and not state["captured"]:
                try:
                    proc.read(4096)
                except EOFError:
                    break
                except Exception:
                    pass
                el = time.time() - start
                if el > 4 and step == 0:
                    _write(proc, "\r"); step = 1           # dismiss any trust/onboarding prompt
                elif el > 8 and step == 1:
                    _write(proc, "hi\r"); step = 2          # submit a message
                elif el > 14 and step == 2:
                    _write(proc, "\r"); step = 3
                time.sleep(0.3)
            try:
                proc.terminate(force=True)
            except Exception:
                pass
        else:  # print / SDK entrypoint — no PTY needed (leaner prompt, no Scratchpad section)
            import subprocess
            try:
                subprocess.run(["claude", "-p", probe], cwd=cwd, env=env,
                               stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=timeout)
            except Exception:
                pass
        state["event"].wait(2)
    finally:
        httpd.shutdown()
    return state["body"]


def genericize(text):
    """Replace machine/session-specific tokens with clearly-labeled placeholders."""
    up = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    for form in {up, up.replace("\\", "/")}:
        text = text.replace(form, "<USERPROFILE>")
    cwd = os.getcwd()
    for form in {cwd, cwd.replace("\\", "/")}:
        text = text.replace(form, "<PROJECT_DIR>")
    # any remaining C:\Users\<name> style
    text = re.sub(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\"'\s]+", "<USERPROFILE>", text)
    # session UUID (scratchpad) and the mangled project key
    text = re.sub(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                  "<SESSION_ID>", text)
    text = re.sub(r"C--[A-Za-z0-9._-]+", "<PROJECT_KEY>", text)
    return text


def main():
    ap = argparse.ArgumentParser(description="Auto-capture Claude Code's current default system prompt.")
    ap.add_argument("--mode", choices=["interactive", "print"], default="interactive",
                    help="interactive = full 'cli' prompt (needs pywinpty); print = leaner SDK prompt")
    ap.add_argument("--out", default="claude_default_system_prompt.md", help="output file")
    ap.add_argument("--identity", action="store_true",
                    help="prepend the 'You are Claude Code' identity line "
                         "(omit it for --system-prompt-file, where it is auto-added)")
    ap.add_argument("--genericize", action="store_true",
                    help="replace machine/session paths with <PLACEHOLDERS>")
    ap.add_argument("--raw", metavar="FILE", help="also dump the full captured request JSON")
    ap.add_argument("--timeout", type=int, default=60)
    args = ap.parse_args()

    print(f"Capturing live default prompt (mode={args.mode}, cwd={os.getcwd()}) ...", file=sys.stderr)
    body = capture(mode=args.mode, timeout=args.timeout)
    if not body:
        print("ERROR: no request captured. Is `claude` on PATH and logged in? "
              "Try a longer --timeout, or --mode print.", file=sys.stderr)
        sys.exit(1)

    if args.raw:
        with open(args.raw, "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=2)

    sysf = body["system"]
    if not isinstance(sysf, list):
        print("ERROR: unexpected system field shape.", file=sys.stderr)
        sys.exit(1)

    header = sysf[0].get("text", "") if sysf else ""
    ver = re.search(r"cc_version=([^\s;]+)", header)
    ep = re.search(r"cc_entrypoint=([^\s;]+)", header)
    identity = sysf[1]["text"] if len(sysf) > 1 else ""
    prompt_body = sysf[2]["text"] if len(sysf) > 2 else (sysf[1]["text"] if len(sysf) > 1 else "")

    out = (identity + "\n" + prompt_body) if args.identity else prompt_body
    if args.genericize:
        out = genericize(out)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)

    headers = re.findall(r"(?m)^# .+$", prompt_body)
    print(f"  version   : {ver.group(1) if ver else '?'}", file=sys.stderr)
    print(f"  entrypoint: {ep.group(1) if ep else '?'}", file=sys.stderr)
    print(f"  model     : {body.get('model')}", file=sys.stderr)
    print(f"  tools     : {len(body.get('tools', []))} (sent separately, not in this file)", file=sys.stderr)
    print(f"  identity  : {'included' if args.identity else 'omitted (auto-added under --system-prompt)'}", file=sys.stderr)
    print(f"  sections  : {headers}", file=sys.stderr)
    print(f"  wrote     : {args.out}  ({len(out)} chars, ~{len(out)//4} tokens)", file=sys.stderr)
    if any('Scratchpad' in h for h in headers) and not args.genericize:
        print("  NOTE      : '# Scratchpad Directory' holds a per-session path; "
              "use --genericize or delete it before reusing the file.", file=sys.stderr)


if __name__ == "__main__":
    main()
