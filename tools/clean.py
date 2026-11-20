#!/usr/bin/env python3
"""Turn a raw `wget --mirror` copy of skainet.io into a static site for GitHub Pages.

Run from the repo root after tools/mirror.sh. Idempotent.
"""
import filecmp
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
ORIGIN = "https://skainet.io"
SKIP_DIRS = {".git", ".github", "tools", "assets"}


def walk():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not (base == ROOT and d in SKIP_DIRS)]
        for name in files:
            yield os.path.join(base, name)


# 1. wget keeps the query string in file names ("be.css?ver=1.css"); drop it.
for path in list(walk()):
    name = os.path.basename(path)
    if "?" not in name:
        continue
    target = os.path.join(os.path.dirname(path), name.split("?", 1)[0])
    if os.path.exists(target) and not filecmp.cmp(path, target, shallow=False):
        print("warning: overwriting differing file", os.path.relpath(target, ROOT))
    os.replace(path, target)

# wget saved two cursor files with a bogus .html suffix.
for path in list(walk()):
    if path.endswith(".cur.html"):
        os.replace(path, path[: -len(".html")])

HEAD_JUNK = re.compile(
    r"<link[^>]+(?:application/rss\+xml|\+oembed|api\.w\.org|wp-json|EditURI|rel=['\"]shortlink['\"])[^>]*>\s*",
    re.I,
)
FORM_SNIPPET = '<script src="{prefix}assets/static-form.js" defer></script>\n'

for path in walk():
    if not path.endswith((".html", ".css")):
        continue
    with open(path, encoding="utf-8", errors="surrogateescape") as fh:
        text = fh.read()
    orig = text

    # 2. references to the renamed files
    text = re.sub(r"%3F[A-Za-z0-9=.]*", "", text)
    text = text.replace(".cur.html", ".cur")

    if path.endswith(".html"):
        rel_dir = os.path.relpath(os.path.dirname(path), ROOT)
        rel_dir = "" if rel_dir == "." else rel_dir.replace(os.sep, "/") + "/"
        prefix = "../" * rel_dir.count("/")

        # 3. WordPress endpoints that do not exist on a static host
        text = HEAD_JUNK.sub("", text)

        # 4. canonical URL points at the real domain
        text = re.sub(
            r'<link rel="canonical" href="[^"]*"\s*/?>',
            '<link rel="canonical" href="%s/%s" />' % (ORIGIN, rel_dir),
            text,
        )

        # 5. directory URLs instead of .../index.html
        def tidy(m):
            target = m.group(2) or "./"
            return '%s="%s%s"' % (m.group(1), target, m.group(3) or "")

        text = re.sub(r'\b(href|action)="((?:\.\./)*(?:[\w-]+/)*)index\.html(#[^"]*)?"', tidy, text)

        # 6. contact form: no PHP backend, hand over to the visitor's mail client
        if "wpcf7-form" in text and "static-form.js" not in text:
            text = text.replace("</body>", FORM_SNIPPET.format(prefix=prefix) + "</body>", 1)

    if text != orig:
        with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
            fh.write(text)

open(os.path.join(ROOT, ".nojekyll"), "a").close()
print("cleaned", ROOT)
