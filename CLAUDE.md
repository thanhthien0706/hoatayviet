# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static clone of hoatayviet.net (Vietnamese model-ship shop): hand-written HTML/CSS/JS, no framework, no package manager, no tests. Python 3 scripts (stdlib only) generate most of `site/`.

## Commands

Run all commands from the repo root (scripts use paths relative to it, e.g. `_raw/products.json`, `site/`).

```bash
python scripts/build_site.py     # regenerate all pages in site/ from _raw/*.json
python scripts/check_site.py     # verify every href/src in site/ resolves (the only "test")
cd site && python -m http.server 8900   # serve at http://127.0.0.1:8900/index.html
```

There is no lint or unit-test setup. After changing templates or CSS, rebuild and run `check_site.py`.

## Architecture

- **`site/` is mostly generated output.** `scripts/build_site.py` is the single source of truth for page HTML: header/footer/nav, home, category (`danh-muc/<slug>/`), product (`sp/<slug>/`), `san-pham.html`, `tim-kiem.html`, and stub pages (gioi-thieu, lien-he, huong-dan*, gio-hang, tai-khoan, tin-tuc). Edit the Python templates, not the generated HTML, or changes are overwritten on the next build. It also writes a slimmed `site/assets/data/products.json` for client-side search.
- **Hand-edited assets:** `site/assets/css/style.css` (tokens first, then components) and `site/assets/js/main.js` (sticky header, slider, menus, search, gallery) are not generated.
- **Build inputs:** `_raw/products.json` and `_raw/home_sections.json` are the only tracked data the build needs. The rest of `_raw/` and `_mirror/` are gitignored and rebuildable.
- **Data pipeline (rarely rerun):** `mirror.py` → `parse_home.py` (home sections + cards) · `crawl_products.py` (Wayback Machine, since the origin returns HTTP 500 for everything but the home page) → `parse_products.py` → `download_product_images.py` (live CDN). `cssgrep.py` extracts rules from the original 441KB stylesheet for reference.
- Categories are defined in the `CATEGORIES` list in `build_site.py`; the nav (`MAIN_NAV`, `GUIDE_SUB`) and contact constants live in the same file. Relative link prefixes (`prefix`/`{p}`) are computed per page depth.

## Fidelity rules

The goal is pixel-accurate cloning, so original bugs are reproduced on purpose (e.g. white-on-white header icons and invisible mobile hamburger). Before "fixing" visual oddities, read `docs/research/KNOWN_ISSUES.md` (each bug has its repair documented). `docs/research/DESIGN_TOKENS.md` and `BEHAVIORS.md` hold measured colours, breakpoints and interaction triggers; README.md has the measured layout numbers to preserve (e.g. header 200×100 logo, top bar 36px, sticky thresholds 280/37). The only intentional deviation is loading Roboto / Roboto Condensed webfonts.
