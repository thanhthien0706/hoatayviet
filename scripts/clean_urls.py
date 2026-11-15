#!/usr/bin/env python3
"""Rewrite every internal link in site/*.html to a root-absolute clean URL.

    about.html            -> /about
    index.html            -> /
    sp/foo/index.html     -> /sp/foo
    ../../assets/x.css    -> /assets/x.css

Run after build_site.py / build_en.py. Idempotent. Paired with vercel.json
(cleanUrls: true), which serves /about from about.html.
"""
import re
from pathlib import Path
from posixpath import normpath, join

SITE = Path(__file__).resolve().parent.parent / 'site'
ATTR = re.compile(r'(\b(?:href|src|action|data-img)=")([^"]*)(")')
SKIP = ('http:', 'https:', '//', '#', 'mailto:', 'tel:', 'data:', 'javascript:')
JS_CHARS = "'+{<"  # value is a JS string fragment, not a URL


def clean(val, page_dir):
    if not val or val.startswith(SKIP) or any(c in val for c in JS_CHARS):
        return val
    m = re.match(r'([^?#]*)(.*)$', val)
    path, tail = m.group(1), m.group(2)
    if not path:
        return val
    if path.startswith('assets/'):  # data-img values are site-root relative
        path = '/' + path
    if not path.startswith('/'):
        path = normpath(join('/', page_dir, path))
    if path.endswith('index.html'):
        path = path[:-len('index.html')]
    elif path.endswith('.html'):
        path = path[:-len('.html')]
    if len(path) > 1:
        path = path.rstrip('/')
    return (path or '/') + tail


# Inline <script> strings in the search pages.
JS_FIXES = [
    ("fetch('assets/", "fetch('/assets/"),
    ("'sp/' + p.slug + '/index.html'", "'/sp/' + p.slug"),
    ("'product/' + p.slug + '/index.html'", "'/product/' + p.slug"),
    ('<img src="\' + p.thumb', '<img src="/\' + p.thumb'),
    ('data-img="\' + esc(p.thumb)', 'data-img="/\' + esc(p.thumb)'),
]


def main():
    n = 0
    for f in SITE.rglob('*.html'):
        page_dir = str(f.parent.relative_to(SITE)).replace('.', '')
        src = f.read_text(encoding='utf-8')
        out = ATTR.sub(lambda m: m.group(1) + clean(m.group(2), page_dir) + m.group(3), src)
        for a, b in JS_FIXES:
            out = out.replace(a, b)
        if out != src:
            f.write_text(out, encoding='utf-8')
            n += 1
    print('rewrote', n, 'files')


if __name__ == '__main__':
    main()
