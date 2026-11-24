#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124 (Python 3.13, stdlib only).

Copies the entry image held beside this file to the output directory as
entry.png. The image itself — a newspaper front page summing up Tuesday
24 November 2026's world news — was drawn by render.py in this repository
and is shipped here as entry.png, so the program needs no network and
writes the same bytes on every run.

Run locally:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

OUTPUT_NAME = "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / OUTPUT_NAME
    shutil.copyfile(src, out_dir / OUTPUT_NAME)


if __name__ == "__main__":
    main()
