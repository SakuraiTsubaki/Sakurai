#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import deque
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE_HOST = "www.pokemon.co.jp"
SEEDS = [
    "https://www.pokemon.co.jp/ex/winds_waves/ja/",
    "https://www.pokemon.co.jp/ex/winds_waves/ja/pokemon/",
    "https://www.pokemon.co.jp/ex/winds_waves/ja/pokemon/202602_01/",
    "https://www.pokemon.co.jp/ex/winds_waves/ja/pokemon/202602_02/",
    "https://www.pokemon.co.jp/ex/winds_waves/ja/pokemon/202602_03/",
    "https://www.pokemon.co.jp/ex/winds_waves/ja/pokemon/202602_04/",
]
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif")
TEXT_EXTS = (".css", ".js")
UA = "Mozilla/5.0 Generation-X-source-census/1.0"

ATTR_RE = re.compile(r'''(?:src|href|srcset)\s*=\s*["']([^"']+)["']''', re.I)
URL_RE = re.compile(r'''url\(\s*["']?([^)'"\s]+)''', re.I)
ABS_RE = re.compile(r'''https?://[^\s"'<>]+''', re.I)
REL_ASSET_RE = re.compile(r'''(?:\.\.?/|/)[^\s"'<>\)]+\.(?:png|jpe?g|webp|svg|gif|css|js)(?:\?[^\s"'<>\)]*)?''', re.I)


def fetch(url: str, max_bytes: int | None = None):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as r:
        data = r.read() if max_bytes is None else r.read(max_bytes)
        return data, dict(r.headers), r.geturl()


def normalize(candidate: str, base: str) -> str | None:
    candidate = unescape(candidate.strip())
    if not candidate or candidate.startswith(("data:", "javascript:", "mailto:", "#")):
        return None
    if "," in candidate and "srcset" not in candidate:
        # Keep ordinary URLs containing commas intact; srcset splitting is handled by caller.
        pass
    url = urljoin(base, candidate)
    p = urlparse(url)
    if p.scheme not in ("http", "https") or p.netloc != BASE_HOST:
        return None
    return url


def extract_urls(text: str, base: str):
    out = set()
    for raw in ATTR_RE.findall(text):
        for part in raw.split(","):
            token = part.strip().split()[0] if part.strip() else ""
            u = normalize(token, base)
            if u:
                out.add(u)
    for raw in URL_RE.findall(text):
        u = normalize(raw, base)
        if u:
            out.add(u)
    for raw in ABS_RE.findall(text):
        u = normalize(raw.rstrip(".,;"), base)
        if u:
            out.add(u)
    for raw in REL_ASSET_RE.findall(text):
        u = normalize(raw, base)
        if u:
            out.add(u)
    return out


def path_ext(url: str) -> str:
    return Path(urlparse(url).path).suffix.lower()


def main():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("official_visual_source_crawl.json")
    queue = deque((u, 0, None) for u in SEEDS)
    visited_text = set()
    discovered_assets: dict[str, set[str]] = {}
    fetch_errors = []

    while queue:
        url, depth, parent = queue.popleft()
        if url in visited_text or depth > 2:
            continue
        visited_text.add(url)
        try:
            data, headers, final_url = fetch(url)
            text = data.decode("utf-8", errors="replace")
        except Exception as exc:
            fetch_errors.append({"url": url, "error": repr(exc)})
            continue

        for found in sorted(extract_urls(text, final_url)):
            ext = path_ext(found)
            if ext in IMAGE_EXTS:
                discovered_assets.setdefault(found, set()).add(final_url)
            elif ext in TEXT_EXTS and depth < 2:
                queue.append((found, depth + 1, final_url))

    assets = []
    for url in sorted(discovered_assets):
        rec = {
            "url": url,
            "referrers": sorted(discovered_assets[url]),
            "extension": path_ext(url),
            "status": "discovered",
        }
        try:
            prefix, headers, final_url = fetch(url, max_bytes=64)
            rec.update({
                "status": "reachable",
                "final_url": final_url,
                "content_type": headers.get("Content-Type"),
                "content_length_header": headers.get("Content-Length"),
                "etag": headers.get("ETag"),
                "last_modified": headers.get("Last-Modified"),
                "first_64_bytes_sha256": hashlib.sha256(prefix).hexdigest(),
            })
            if prefix.startswith(b"\x89PNG\r\n\x1a\n") and len(prefix) >= 24:
                rec["png_ihdr"] = {
                    "width": int.from_bytes(prefix[16:20], "big"),
                    "height": int.from_bytes(prefix[20:24], "big"),
                }
        except Exception as exc:
            rec.update({"status": "error", "error": repr(exc)})
        assets.append(rec)

    keywords = ["101", "102", "103", "104", "pikachu", "kaze", "nami", "pokemon", "202602"]
    likely_relevant = [
        a for a in assets
        if any(k.lower() in a["url"].lower() for k in keywords)
    ]

    payload = {
        "schema_version": 1,
        "research_date": str(date.today()),
        "authority": "The Pokémon Company / Pokémon Japan",
        "host": BASE_HOST,
        "seed_pages": SEEDS,
        "visited_text_resources": sorted(visited_text),
        "asset_count": len(assets),
        "assets": assets,
        "likely_battle_source_candidates": likely_relevant,
        "fetch_errors": fetch_errors,
        "note": "Discovery inventory only. URL presence does not imply native game-internal sprite provenance.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"asset_count": len(assets), "likely_candidates": len(likely_relevant), "errors": len(fetch_errors)}, indent=2))


if __name__ == "__main__":
    main()
