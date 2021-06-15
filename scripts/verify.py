#!/usr/bin/env python3
"""pathvariance quality gate.

Standard library only. Run from the project root:

    python scripts/verify.py

Exit code is 0 when every check passes and 1 when any check fails. One line is
printed per check, followed by a summary line. The checks encode the lessons in
_standards/LESSONS.md that can be verified mechanically:

  1. Every .svg under docs/assets/ parses as XML.
  2. No .svg contains feGaussianBlur, feDropShadow, or feTurbulence.
  3. No XML comment in any .svg contains the illegal double hyphen sequence.
  4. No tracked text file contains the em dash character U+2014 or its numeric
     or named HTML entity forms.
  5. README.md contains no pandoc style image attribute block.
  6. README.md contains none of the banned marketing terms.
  7. Every .svg under docs/assets/ carries a viewBox, role="img", a <title>,
     and a <desc>.
  8. No two text labels sharing a baseline in any .svg overlap.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"

TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".svg", ".yml", ".yaml", ".toml", ".cfg", ".ini",
    ".cff", ".sh", ".editorconfig", ".gitattributes", ".gitignore", ".json",
    "",
}

SKIP_DIRS = {
    "__pycache__", ".git", ".venv", "build", "dist", ".mypy_cache",
    ".pytest_cache", ".egg-info",
}

BANNED_FILTERS = ("feGaussianBlur", "feDropShadow", "feTurbulence")

BANNED_MARKETING = [
    "blazing", "blazingly", "cutting-edge", "cutting edge", "state-of-the-art",
    "state of the art", "world-class", "world class", "revolutionary",
    "game-changing", "game changing", "seamless", "seamlessly", "effortless",
    "effortlessly", "lightning-fast", "lightning fast", "supercharge",
    "supercharged", "next-generation", "next generation", "best-in-class",
    "unparalleled", "unrivaled", "unrivalled", "turnkey", "synergy",
    "leverage the power", "one-stop", "ai powered", "ai-powered",
    "enterprise-grade", "production ready", "battle tested", "robust and",
]

# Built from parts so this file does not match its own em dash sweep.
EM_DASH_FORMS = (
    "\u2014",
    "&#" + "8212;",
    "&" + "mdash;",
)

WIDTH_SANS = 0.58
