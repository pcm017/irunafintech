#!/usr/bin/env python3
"""
wiki_to_blog.py — converts macro_wiki content into a Jekyll blog (GitHub Pages).

Run from the macro_wiki root:
    python3 blog/scripts/wiki_to_blog.py [--all]

Without --all: only converts source pages / entity pages that are newer than
the corresponding output file (or don't have one yet) — i.e. incremental,
safe to run every night after the compile stage.

With --all: reconverts everything (full rebuild / backfill).

Outputs:
  wiki/overview.md              -> blog/overview.md            (page)
  wiki/sources/*.md             -> blog/_posts/YYYY-MM-DD-*.md  (post, one per source)
  wiki/companies/*.md           -> blog/companies/<slug>.md     (page) + blog/companies.md (index)
  wiki/macro/*.md               -> blog/macro/<slug>.md         (page) + blog/macro.md (index)
  wiki/markets/*.md             -> blog/markets/<slug>.md       (page) + blog/markets.md (index)
  wiki/fintech-bfsi/*.md        -> blog/fintech-bfsi/<slug>.md  (page) + blog/fintech-bfsi.md (index)
  wiki/ai-tech/*.md             -> blog/ai-tech/<slug>.md       (page) + blog/ai-tech.md (index)
  wiki/geopolitics/*.md         -> blog/geopolitics/<slug>.md   (page) + blog/geopolitics.md (index)
"""

import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # macro_wiki/
WIKI = ROOT / "wiki"
BLOG = ROOT / "blog"

ENTITY_DIRS = {
    "companies": "Companies",
    "macro": "Macro",
    "markets": "Markets",
    "fintech-bfsi": "Fintech / BFSI",
    "ai-tech": "AI & Tech",
    "geopolitics": "Geopolitics",
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def split_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_raw, body = m.groups()
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, body


def strip_wikilinks(body):
    def repl(match):
        target = match.group(1)
        label = target.split("/")[-1].replace(".md", "").replace("-", " ")
        return f"*{label}*"
    return WIKILINK_RE.sub(repl, body)


def first_h1(body, fallback):
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def slugify(name):
    return re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-").replace("_", "-"))


def yaml_dump(d):
    return yaml.safe_dump(d, sort_keys=False, allow_unicode=True).strip()


def needs_rebuild(src_path, out_path, force):
    if force or not out_path.exists():
        return True
    return src_path.stat().st_mtime > out_path.stat().st_mtime


def convert_sources(force):
    src_dir = WIKI / "sources"
    out_dir = BLOG / "_posts"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in sorted(src_dir.glob("*.md")):
        fm, body = split_frontmatter(src.read_text())
        date = str(fm.get("date", src.name[:10]))
        slug = src.stem
        out_path = out_dir / f"{slug}.md"
        if not needs_rebuild(src, out_path, force):
            continue
        title = first_h1(body, slug.replace("-", " ").title())
        tags = fm.get("tags", []) or []
        source_type = fm.get("type") or fm.get("source_type") or "source"
        post_fm = {
            "layout": "post",
            "title": title,
            "date": f"{date} 08:00:00 +0530",
            "categories": [source_type],
            "tags": tags,
        }
        clean_body = strip_wikilinks(body)
        out_path.write_text(f"---\n{yaml_dump(post_fm)}\n---\n{clean_body}")
        count += 1
    print(f"  sources -> posts: {count} written")


def convert_overview(force):
    src = WIKI / "overview.md"
    out_path = BLOG / "overview.md"
    if not src.exists() or not needs_rebuild(src, out_path, force):
        print("  overview.md: skipped (up to date)")
        return
    fm, body = split_frontmatter(src.read_text())
    page_fm = {"layout": "page", "title": "Macro Overview", "permalink": "/overview/"}
    clean_body = strip_wikilinks(body)
    out_path.write_text(f"---\n{yaml_dump(page_fm)}\n---\n{clean_body}")
    print("  overview.md: written")


def convert_entities(force):
    for category in ENTITY_DIRS:
        src_dir = WIKI / category
        if not src_dir.exists():
            continue
        out_dir = BLOG / category
        out_dir.mkdir(parents=True, exist_ok=True)
        entries = []
        count = 0
        for src in sorted(src_dir.glob("*.md")):
            fm, body = split_frontmatter(src.read_text())
            slug = src.stem
            out_path = out_dir / f"{slug}.md"
            title = first_h1(body, slug.replace("-", " ").title())
            entries.append((title, f"/{category}/{slug}/"))
            if needs_rebuild(src, out_path, force):
                page_fm = {
                    "layout": "page",
                    "title": title,
                    "permalink": f"/{category}/{slug}/",
                }
                clean_body = strip_wikilinks(body)
                out_path.write_text(f"---\n{yaml_dump(page_fm)}\n---\n{clean_body}")
                count += 1
        # write/refresh the category index page every run (cheap, keeps list current)
        index_path = BLOG / f"{category}.md"
        index_fm = {
            "layout": "page",
            "title": ENTITY_DIRS[category],
            "permalink": f"/{category}/",
        }
        lines = [f"- [{title}]({{{{ '{link}' | relative_url }}}})" for title, link in entries]
        index_body = f"\n## {ENTITY_DIRS[category]}\n\n" + "\n".join(lines) + "\n"
        index_path.write_text(f"---\n{yaml_dump(index_fm)}\n---\n{index_body}")
        print(f"  {category}: {count} pages written, index refreshed ({len(entries)} entries)")


def main():
    force = "--all" in sys.argv
    print(f"Converting wiki -> blog (force={force})")
    convert_overview(force)
    convert_sources(force)
    convert_entities(force)
    print("Done.")


if __name__ == "__main__":
    main()
