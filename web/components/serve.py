#!/usr/bin/env python3
"""Serve the component explorer and keep components.json in step with the tree.

    python3 web/components/serve.py

Inside the container this is the entrypoint. Mount the repo at /src.
"""

import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import update

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("HUMANITY_ROOT", HERE.parent.parent)).resolve()
OUT = HERE / "components.json"
PORT = int(os.environ.get("PORT", "8080"))


def refresh():
    update.write(ROOT, OUT)


def watch():
    while True:
        try:
            refresh()
        except Exception as exc:
            print(exc, flush=True)
        time.sleep(2)


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    os.chdir(HERE)
    refresh()
    threading.Thread(target=watch, daemon=True).start()
    print(f"Humanity Pro components at http://127.0.0.1:{PORT}/", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
