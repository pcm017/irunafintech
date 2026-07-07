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
  (derived)                     -> blog/tags/<tag>.md           (page) + blog/tags.md (grouped index)
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

# Curated topic-style tags for the grouped tags index (extend over time as
# new recurring themes show up). Anything not in here and not an entity slug
# lands in "Other".
TOPIC_WORDS = {
    "macro", "markets", "fintech", "bfsi", "ai", "tech", "geopolitics",
    "companies", "india", "results", "results-data", "newsletter", "article",
    "report", "banking", "lending", "credit", "rates", "upi", "rbi", "fed",
    "nbfc", "inflation", "crude", "gold", "bonds", "indices", "commodities",
    "cot", "source",
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
TLDR_RE = re.compile(r"##\s*TL;DR\s*\n+(.*?)(?=\n##\s|\Z)", re.DOTALL)
BULLET_RE = re.compile(r"^-\s+(.*)$", re.MULTILINE)


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


def strip_leading_title(body):
    """Remove a leading '# Title' line (it duplicates the frontmatter title,
    which is already rendered by the page/post layout) so it doesn't also
    become the auto-generated excerpt."""
    stripped = body.lstrip("\n")
    lines = stripped.split("\n")
    if lines and lines[0].startswith("# "):
        rest = "\n".join(lines[1:]).lstrip("\n")
        return "\n" + rest
    return body


def extract_excerpt(body, max_len=240):
    """Pull a real summary from the '## TL;DR' bullets for use as an explicit
    post excerpt, instead of letting Jekyll fall back to the first paragraph
    (which used to be the duplicate title)."""
    m = TLDR_RE.search(body)
    if not m:
        return None
    bullets = BULLET_RE.findall(m.group(1))
    if not bullets:
        return None
    text = " ".join(b.strip() for b in bullets[:2])
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0].rstrip(",;: ") + "…"
    return text or None


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


def post_permalink(slug):
    """Mirrors Jekyll's default permalink pattern (/:year/:month/:day/:title/)
    for a post filename shaped YYYY-MM-DD-name.md."""
    date_str = slug[:10]
    parts = date_str.split("-")
    name = slug[11:] if len(slug) > 11 else slug
    if len(parts) == 3:
        yyyy, mm, dd = parts
        return f"/{yyyy}/{mm}/{dd}/{name}/"
    return f"/{slug}/"


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
        clean_body = strip_wikilinks(body)
        clean_body = strip_leading_title(clean_body)
        excerpt = extract_excerpt(clean_body)
        post_fm = {
            "layout": "post",
            "title": title,
            "date": f"{date} 08:00:00 +0530",
            "categories": [source_type],
            "tags": tags,
        }
        if excerpt:
            post_fm["excerpt"] = excerpt
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


def fallback_entries_for_category(category):
    """When an entity category has no standing topic pages yet, fall back to
    listing the most recent source posts whose tags match the category name
    (e.g. category 'fintech-bfsi' -> tags 'fintech' or 'bfsi')."""
    words = set(category.split("-"))
    src_sources_dir = WIKI / "sources"
    if not src_sources_dir.exists():
        return []
    matches = []
    for src in src_sources_dir.glob("*.md"):
        fm, body = split_frontmatter(src.read_text())
        tags = {str(t).lower() for t in (fm.get("tags") or [])}
        if not (tags & words):
            continue
        slug = src.stem
        date_str = str(fm.get("date", slug[:10]))
        title = first_h1(body, slug.replace("-", " ").title())
        matches.append((date_str, title, post_permalink(slug)))
    matches.sort(key=lambda t: t[0], reverse=True)
    return [(title, link) for _, title, link in matches[:10]]


def convert_entities(force):
    for category in ENTITY_DIRS:
        src_dir = WIKI / category
        out_dir = BLOG / category
        entries = []
        count = 0
        if src_dir.exists():
            out_dir.mkdir(parents=True, exist_ok=True)
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

        used_fallback = False
        if not entries:
            entries = fallback_entries_for_category(category)
            used_fallback = True

        index_path = BLOG / f"{category}.md"
        index_fm = {
            "layout": "page",
            "title": ENTITY_DIRS[category],
            "permalink": f"/{category}/",
        }
        if entries:
            lines = [f"- [{title}]({{{{ '{link}' | relative_url }}}})" for title, link in entries]
            note = (
                "*No standing topic pages yet — showing the most recent related posts.*\n\n"
                if used_fallback else ""
            )
            index_body = f"\n## {ENTITY_DIRS[category]}\n\n{note}" + "\n".join(lines) + "\n"
        else:
            index_body = f"\n## {ENTITY_DIRS[category]}\n\n*No content yet.*\n"
        index_path.write_text(f"---\n{yaml_dump(index_fm)}\n---\n{index_body}")
        tag = "  [fallback]" if used_fallback else ""
        print(f"  {category}: {count} pages written, index refreshed ({len(entries)} entries){tag}")


def collect_entity_slugs():
    slugs = set()
    for category in ENTITY_DIRS:
        src_dir = WIKI / category
        if not src_dir.exists():
            continue
        for src in src_dir.glob("*.md"):
            slugs.add(src.stem)
    return slugs


def generate_tags(force):
    posts_dir = BLOG / "_posts"
    if not posts_dir.exists():
        print("  tags: skipped (no posts)")
        return

    tag_posts = {}
    for post in sorted(posts_dir.glob("*.md")):
        fm, _ = split_frontmatter(post.read_text())
        title = fm.get("title", post.stem)
        date = str(fm.get("date", post.stem[:10]))[:10]
        tags = fm.get("tags", []) or []
        link = post_permalink(post.stem)
        for tag in tags:
            t = slugify(str(tag))
            if not t:
                continue
            tag_posts.setdefault(t, []).append((date, title, link))

    entity_slugs = collect_entity_slugs()
    out_dir = BLOG / "tags"
    out_dir.mkdir(parents=True, exist_ok=True)

    companies_bucket, topics_bucket, other_bucket = [], [], []

    for tag, posts in sorted(tag_posts.items()):
        posts.sort(key=lambda p: p[0], reverse=True)
        tag_fm = {"layout": "page", "title": f"Tag: {tag}", "permalink": f"/tags/{tag}/"}
        lines = [f"- {date} — [{title}]({{{{ '{link}' | relative_url }}}})" for date, title, link in posts]
        body = f"\n## Tag: {tag}\n\n" + "\n".join(lines) + "\n"
        (out_dir / f"{tag}.md").write_text(f"---\n{yaml_dump(tag_fm)}\n---\n{body}")

        if tag in entity_slugs:
            companies_bucket.append((tag, len(posts)))
        elif tag in TOPIC_WORDS:
            topics_bucket.append((tag, len(posts)))
        else:
            other_bucket.append((tag, len(posts)))

    def fmt_bucket(bucket):
        if not bucket:
            return "*none yet*"
        return "\n".join(
            f"- [{tag}]({{{{ '/tags/{tag}/' | relative_url }}}}) ({count})"
            for tag, count in sorted(bucket)
        )

    index_fm = {"layout": "page", "title": "Tags", "permalink": "/tags/"}
    index_body = (
        "\n## Tags\n\n"
        "Browse posts by company/entity, recurring topic, or everything else.\n\n"
        "### Companies & Entities\n\n" + fmt_bucket(companies_bucket) + "\n\n"
        "### Topics\n\n" + fmt_bucket(topics_bucket) + "\n\n"
        "### Other\n\n" + fmt_bucket(other_bucket) + "\n"
    )
    (BLOG / "tags.md").write_text(f"---\n{yaml_dump(index_fm)}\n---\n{index_body}")
    print(f"  tags: {len(tag_posts)} tag pages written")


def main():
    force = "--all" in sys.argv
    print(f"Converting wiki -> blog (force={force})")
    convert_overview(force)
    convert_sources(force)
    convert_entities(force)
    generate_tags(force)
    print("Done.")


if __name__ == "__main__":
    main()
