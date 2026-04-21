#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageStat

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"
OPT_DIR = IMAGES_DIR / "optimized"
AMENITIES_HTML = ROOT / "amenities.html"

# Map card titles in amenities.html -> list of keyword patterns to search in images/
CATEGORIES: Dict[str, List[str]] = {
    "Indoor pool with retractable roof": [r"pool"],
    "Fitness": [r"gym"],
    "Tennis & pickleball courts": [r"tennis"],
    "Basketball court": [r"basketball"],
    "Studios": [r"club"],
    "Golf Simulator": [r"golf"],
    # Include playground in kids programming candidates
    "Social life & kids programming": [r"pond|fountain|splash\s*pad|kids|playground"],
    "Social clubs & resident activities": [r"social|event|dance|party"],
    # Add lobby/building keywords for membership card
    "On-site conveniences": [r"salon|dry\s*clean|retail|shopping|store|arcade"],
    "Membership & access": [r"lobby|building|tower|entrance"],
    "Sauna/Steam Rooms": [r"sauna|steam"],
    "Locker room showers": [r"shower"],
    "Vanity & prep area": [r"sink|vanity"],
}

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}


def find_candidates(keywords: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in IMAGES_DIR.iterdir():
        if not p.is_file():
            continue
        if p.suffix not in EXTS:
            continue
        name = p.name.lower()
        for kw in keywords:
            if re.search(kw, name, flags=re.IGNORECASE):
                files.append(p)
                break
    return files


def image_score(path: Path) -> float:
    try:
        im = Image.open(path).convert("RGB")
    except Exception:
        return -1.0

    w, h = im.size
    landscape_bonus = 0.0
    if w >= h:
        landscape_bonus = 0.08

    g = im.convert("L")
    stat = ImageStat.Stat(g)
    mean = stat.mean[0] / 255.0
    stddev = stat.stddev[0] / 255.0  # proxy for contrast

    # Edge variance as a proxy for sharpness
    edges = g.filter(ImageFilter.FIND_EDGES)
    sharp = ImageStat.Stat(edges).var[0] / (255.0 * 255.0)

    # Clipping penalty
    hist = g.histogram()
    total = sum(hist)
    low_clip = sum(hist[:6]) / total if total > 0 else 0
    high_clip = sum(hist[-6:]) / total if total > 0 else 0
    clip_penalty = (low_clip + high_clip)

    # Target mid brightness ~0.5
    bright_penalty = abs(mean - 0.5)

    # Weighted score
    score = (
        0.55 * sharp +
        0.30 * stddev +
        0.10 * landscape_bonus -
        0.08 * clip_penalty -
        0.12 * bright_penalty
    )
    return float(score)


def enhance_and_save(src: Path, out: Path, max_w: int = 1600) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    # Resize to max width
    w, h = im.size
    if w > max_w:
        new_h = int(h * (max_w / w))
        im = im.resize((max_w, new_h), Image.LANCZOS)
    # Auto-contrast and gentle enhancements
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = ImageEnhance.Sharpness(im).enhance(1.10)
    # Save as high-quality JPEG
    out = out.with_suffix('.jpg')
    im.save(out, format='JPEG', quality=88, optimize=True, progressive=True)


def select_best_for_category(keywords: List[str]) -> Tuple[Path, float]:
    cands = find_candidates(keywords)
    if not cands:
        return (None, -1.0)
    best = None
    best_score = -999.0
    for p in cands:
        s = image_score(p)
        if s > best_score:
            best, best_score = p, s
    return (best, best_score)


def update_amenities_html(mapping: Dict[str, str]) -> None:
    html = AMENITIES_HTML.read_text(encoding='utf-8')
    # For each card title, update the first <img ... src="..."> that appears after the title's enclosing <article>
    for title, rel_path in mapping.items():
        if not rel_path:
            continue
        # Build a regex to find the article with this h2 title and replace the src within its first <img ...>
        # Pattern: <article ...> ... <h2 class="card__title">{title}</h2> ... <img ... src="...">
        # We search within a small window around the title to avoid cross-article matches
        pattern = re.compile(
            r"(<article[^>]*>.*?<div class=\"card__image\">\s*<img\s+[^>]*src=\")([^\"]+)(\"[^>]*>.*?<h2[^>]*>\s*" + re.escape(title) + r"\s*</h2>)",
            re.DOTALL | re.IGNORECASE,
        )
        def repl(m):
            return m.group(1) + rel_path + m.group(3)
        new_html, n = pattern.subn(repl, html, count=1)
        if n == 0:
            # Try alternative order: title appears before image
            pattern2 = re.compile(
                r"(<article[^>]*>.*?<h2[^>]*>\s*" + re.escape(title) + r"\s*</h2>.*?<div class=\"card__image\">\s*<img\s+[^>]*src=\")([^\"]+)(\")",
                re.DOTALL | re.IGNORECASE,
            )
            new_html, n = pattern2.subn(lambda m: m.group(1) + rel_path + m.group(3), html, count=1)
        if n > 0:
            html = new_html
        else:
            print(f"WARN: Could not update image for '{title}'")
    AMENITIES_HTML.write_text(html, encoding='utf-8')


def main():
    results: Dict[str, str] = {}
    print("Scanning and selecting best images...")
    for title, kws in CATEGORIES.items():
        best, score = select_best_for_category(kws)
        if best is None:
            print(f"- {title}: no candidates found for keywords={kws}")
            results[title] = None
            continue
        # Save enhanced optimized version
        safe_name = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        out_path = OPT_DIR / f"{safe_name}.jpg"
        enhance_and_save(best, out_path)
        rel = os.path.relpath(out_path, ROOT)
        results[title] = rel
        print(f"- {title}: {best.name} (score={score:.3f}) -> {rel}")

    # Update amenities.html
    update_amenities_html(results)
    print("Updated amenities.html with optimized image selections.")


if __name__ == "__main__":
    main()
