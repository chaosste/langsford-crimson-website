#!/usr/bin/env python3
"""Sync content/COPY.md into the static HTML pages."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
COPY_FILE = ROOT / "content" / "COPY.md"
BLOG_POSTS_FILE = ROOT / "content" / "BLOG_POSTS.md"
BLOG_DIR = ROOT / "blog"


def clean_value(value: str) -> str:
    """Strip markdown links and surrounding whitespace from metadata/table cells."""
    value = value.strip()
    match = re.search(r"\[[^\]]*\]\(([^)]+)\)", value)
    if match:
        url = match.group(1).strip()
        if url.startswith("mailto:"):
            return url[len("mailto:") :]
        return url
    return value


def parse_meta_lines(line: str, meta: dict[str, str]) -> None:
    """Parse one or more @key: value pairs from a line."""
    if "@" not in line or ":" not in line:
        return
    for part in re.split(r"(?=@[\w-]+:)", line):
        part = part.strip()
        if not part.startswith("@") or ":" not in part:
            continue
        key, value = part[1:].split(":", 1)
        meta[key.strip()] = clean_value(value)


def parse_copy_md(text: str) -> dict[str, dict]:
    sections: dict[str, dict] = {}
    chunks = re.split(r"\n---+\n", text)

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk.startswith("## "):
            continue

        lines = chunk.splitlines()
        heading = lines[0].replace("## ", "").strip()
        meta: dict[str, str] = {}
        body_paragraphs: list[str] = []
        current_para: list[str] = []
        table: list[list[str]] | None = None

        for line in lines[1:]:
            if line.strip().startswith("@"):
                parse_meta_lines(line, meta)
            elif line.startswith("|"):
                if table is None:
                    table = []
                if re.match(r"^\|\s*[-:]+\s*\|", line):
                    continue
                cells = [clean_value(cell.strip()) for cell in line.strip("|").split("|")]
                if cells and cells[0].lower() in {"label", "title", "date"}:
                    continue
                table.append(cells)
            elif not line.strip():
                if current_para:
                    body_paragraphs.append("\n".join(current_para))
                    current_para = []
            elif line.strip():
                current_para.append(line.strip())

        if current_para:
            body_paragraphs.append("\n".join(current_para))

        sections[heading] = {
            "meta": meta,
            "body": "\n\n".join(body_paragraphs).strip(),
            "paragraphs": body_paragraphs,
            "table": table or [],
        }

    return sections


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def external_link_attrs(href: str) -> str:
    if href.startswith("http"):
        return ' rel="noopener noreferrer"'
    return ""


def normalize_href(href: str) -> str:
    href = href.strip().lstrip("/")
    if href.startswith("http"):
        return href
    return "/".join(quote(part, safe="") for part in href.split("/"))


def replace_marker(content: str, marker_id: str, replacement: str) -> str:
    pattern = (
        rf"(<!-- copy:{re.escape(marker_id)} -->)"
        rf"[\s\S]*?"
        rf"(<!-- /copy:{re.escape(marker_id)} -->)"
    )
    match = re.search(pattern, content)
    if not match:
        raise ValueError(f"Missing copy markers for: {marker_id}")
    return content[: match.start()] + match.group(1) + replacement + match.group(2) + content[match.end() :]


def replace_meta(content: str, meta: dict[str, str]) -> str:
    if "title" in meta:
        content = re.sub(r"<title>.*?</title>", f"<title>{esc(meta['title'])}</title>", content)
    if "description" in meta:
        content = re.sub(
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{esc(meta["description"])}">',
            content,
        )
    if "og-title" in meta:
        content = re.sub(
            r'<meta property="og:title" content=".*?">',
            f'<meta property="og:title" content="{esc(meta["og-title"])}">',
            content,
        )
    if "og-description" in meta:
        content = re.sub(
            r'<meta property="og:description" content=".*?">',
            f'<meta property="og:description" content="{esc(meta["og-description"])}">',
            content,
        )
    return content


def render_home_section(section: dict) -> str:
    meta = section["meta"]
    tag = meta.get("heading-tag", "h2")
    heading = esc(meta["heading"])
    image = esc(meta["image"])
    body = esc(section["body"])
    return (
        f'\n          <article class="retro-card retro-frame">\n'
        f'            <figure class="retro-card__media">\n'
        f'              <img class="retro-card__image" src="{image}" alt="" width="400" height="400">\n'
        f"            </figure>\n"
        f'            <{tag} class="retro-card__title">{heading}</{tag}>\n'
        f'            <p class="retro-card__body">{body}</p>\n'
        f"          </article>"
    )


def render_project_entries(table: list[list[str]]) -> str:
    entries = []
    last_index = len(table) - 1
    for index, (title, description, link_text, link_href) in enumerate(table):
        link_href = normalize_href(link_href)
        ext = external_link_attrs(link_href)
        badge = (
            '            <span class="retro-tag">Latest</span>\n'
            if index == 0
            else ""
        )
        block = (
            '          <article class="changelog-card retro-frame">\n'
            f"{badge}"
            '            <div class="changelog-card__header">\n'
            f'              <h2 class="changelog-card__title">{esc(title)}</h2>\n'
            "            </div>\n"
            '            <div class="changelog-card__content">\n'
            f'              <p class="changelog-card__description">{esc(description)}</p>\n'
            f'              <a class="changelog-card__link" href="{esc(link_href)}"{ext}>{esc(link_text)}</a>\n'
            "            </div>\n"
            "          </article>"
        )
        entries.append(block)
        if index < last_index:
            entries.append('          <hr class="pixel-divider changelog-separator">')
    return "\n" + "\n".join(entries) + "\n        "


def render_iris_links(table: list[list[str]]) -> str:
    items = []
    for row in table:
        label, href, title = row
        title_attr = f' title="{esc(title)}"' if title else ""
        ext = external_link_attrs(href)
        items.append(
            f'          <li><a href="{esc(href)}"{title_attr}{ext}>{esc(label)}</a></li>'
        )
    return "\n" + "\n".join(items) + "\n        "


def render_research_rows(table: list[list[str]]) -> str:
    rows = []
    for title, description, link_text, link_href in table:
        link_href = normalize_href(link_href)
        ext = external_link_attrs(link_href)
        rows.append(
            "              <tr>\n"
            f"                <td>{esc(title)}</td>\n"
            f"                <td>{esc(description)}</td>\n"
            f'                <td><a href="{esc(link_href)}"{ext}>{esc(link_text)}</a></td>\n'
            "              </tr>"
        )
    return "\n" + "\n".join(rows) + "\n            "


def render_blog_posts(table: list[list[str]]) -> str:
    cards = []
    for date, title, excerpt, href in table:
        cards.append(
            '          <article class="blog-card">\n'
            '            <div class="blog-card-inner retro-frame">\n'
            '            <div class="blog-card-header">\n'
            f'              <h2 class="blog-card-title">{esc(title)}</h2>\n'
            f'              <time class="blog-card-date" datetime="{esc(date)}">{esc(date)}</time>\n'
            "            </div>\n"
            f'            <p class="blog-card-excerpt">{esc(excerpt)}</p>\n'
            f'            <a class="blog-card-link" href="{esc(href)}">Read →</a>\n'
            "            </div>\n"
            "          </article>"
        )
    return "\n\n" + "\n\n".join(cards) + "\n        "


def render_footer(section: dict) -> str:
    meta = section["meta"]
    email = meta.get("email", "")
    if not email:
        raise ValueError("global / footer is missing @email (use its own line, e.g. @email: steve@example.com)")
    return (
        f'\n        <p>&copy; {esc(meta["copyright"])}</p>\n'
        f'        <p class="footer-links">\n'
        f'          <a href="mailto:{esc(email)}">{esc(email)}</a>\n'
        f'          <span class="footer-sep">·</span>\n'
        f'          <a href="{esc(meta["linkedin"])}" rel="noopener noreferrer">{esc(meta["linkedin-label"])}</a>\n'
        f'          <span class="footer-sep">·</span>\n'
        f'          <a href="{esc(meta["github"])}" rel="noopener noreferrer">{esc(meta["github-label"])}</a>\n'
        f"        </p>\n      "
    )


def render_contact_body(section: dict) -> str:
    return "".join(f'\n          <p class="body-copy">{esc(p)}</p>' for p in section["paragraphs"]) + "\n        "


def render_contact_credentials(section: dict) -> str:
    return "".join(f"\n            <p>{esc(p)}</p>" for p in section["paragraphs"]) + "\n          "


def render_iris_body(section: dict) -> str:
    return "".join(f'\n        <p class="body-copy">{esc(p)}</p>' for p in section["paragraphs"]) + "\n        "


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug


def parse_yaml_value(raw: str) -> str:
    raw = raw.strip()
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    return raw


def parse_blog_posts_file(text: str) -> list[dict]:
    posts: list[dict] = []
    for frontmatter, body in re.findall(
        r"^---\s*\n(.*?)\n---\s*\n(.*?)(?=^---\s*\n|\Z)",
        text,
        flags=re.DOTALL | re.MULTILINE,
    ):
        meta: dict[str, str | list[str]] = {}
        for line in frontmatter.strip().splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "tags":
                tags = re.findall(r"[\w-]+", value)
                meta[key] = tags
            else:
                meta[key] = parse_yaml_value(value)

        if "title" not in meta:
            continue

        posts.append(
            {
                "title": str(meta["title"]),
                "date": str(meta.get("date", "")),
                "tags": meta.get("tags", []),
                "body": body.strip(),
                "slug": slugify(str(meta["title"])),
            }
        )
    return posts


def inline_markdown(text: str) -> str:
    parts: list[str] = []
    for index, segment in enumerate(re.split(r"\*([^*]+)\*", text)):
        if index % 2 == 1:
            parts.append(f"<em>{esc(segment)}</em>")
        else:
            parts.append(esc(segment))
    return "".join(parts)


def render_blog_body_html(body: str) -> str:
    blocks: list[str] = []
    for paragraph in body.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if paragraph.startswith("$$") and paragraph.endswith("$$"):
            formula = paragraph[2:-2].strip()
            blocks.append(f'          <pre class="blog-formula">{esc(formula)}</pre>')
            continue
        blocks.append(f'          <p class="body-copy">{inline_markdown(paragraph)}</p>')
    return "\n".join(blocks) + "\n"


def render_blog_tags(tags: list[str]) -> str:
    if not tags:
        return ""
    items = "".join(f'<li class="blog-post__tag">{esc(tag)}</li>' for tag in tags)
    return f'\n            <ul class="blog-post__tags">{items}</ul>'


def render_blog_post_page(post: dict, footer_html: str) -> str:
    title = post["title"]
    date = post["date"]
    description = post["body"].split("\n\n")[0][:160]
    tags_html = render_blog_tags(post["tags"])  # type: ignore[arg-type]
    body_html = render_blog_body_html(post["body"])

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} — IRIS Research Lab</title>
  <meta name="description" content="{esc(description)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="article">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="../theme-pixelcastle.css">
</head>
<body class="theme-pixelcastle">
  <div class="site-wrapper">
    <header class="site-header">
      <div class="container">
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
        <nav id="site-nav" class="site-nav" aria-label="Main">
          <a href="../index.html">Home</a>
          <a href="../iris.html">IRIS</a>
          <a href="../projects.html">Projects</a>
          <a href="../blog.html" aria-current="page">Blog</a>
          <a href="../contact.html">Contact</a>
        </nav>
      </div>
    </header>

    <main>
      <div class="container">
        <article class="blog-post">
          <a class="blog-post__back" href="../blog.html">← Blog</a>
          <header class="blog-post__header">
            <h1 class="blog-post__title">{esc(title)}</h1>
            <div class="blog-post__meta">
              <time datetime="{esc(date)}">{esc(date)}</time>{tags_html}
            </div>
          </header>
          <div class="blog-post__body">
{body_html}
          </div>
        </article>
      </div>
    </main>

    <footer class="site-footer">
      <div class="container footer-inner">{footer_html}
      </div>
    </footer>
  </div>
  <script src="../script.js"></script>
</body>
</html>
"""


def build_blog_posts(footer_html: str) -> None:
    if not BLOG_POSTS_FILE.exists():
        return

    BLOG_DIR.mkdir(exist_ok=True)
    posts = parse_blog_posts_file(BLOG_POSTS_FILE.read_text(encoding="utf-8"))
    generated_slugs: set[str] = set()

    for post in posts:
        slug = post["slug"]
        generated_slugs.add(slug)
        output = BLOG_DIR / f"{slug}.html"
        output.write_text(render_blog_post_page(post, footer_html), encoding="utf-8")

    for existing in BLOG_DIR.glob("*.html"):
        if existing.stem not in generated_slugs:
            existing.unlink()

    print(f"Generated {len(posts)} blog posts in blog/")


def build() -> None:
    sections = parse_copy_md(COPY_FILE.read_text(encoding="utf-8"))
    footer = render_footer(sections["global / footer"])

    pages = {
        "index.html": lambda content: replace_meta(
            content,
            sections["index / meta"],
        ),
        "iris.html": lambda content: replace_meta(content, sections["iris / meta"]),
        "projects.html": lambda content: replace_meta(content, sections["projects / meta"]),
        "blog.html": lambda content: replace_meta(content, sections["blog / meta"]),
        "contact.html": lambda content: replace_meta(content, sections["contact / meta"]),
    }

    index = ROOT / "index.html"
    index_content = index.read_text(encoding="utf-8")
    index_content = pages["index.html"](index_content)
    index_content = replace_marker(
        index_content,
        "index/sections",
        render_home_section(sections["index / section-1"])
        + render_home_section(sections["index / section-2"])
        + render_home_section(sections["index / section-3"]),
    )
    index.write_text(replace_marker(index_content, "global/footer", footer), encoding="utf-8")

    iris = ROOT / "iris.html"
    iris_header = sections["iris / header"]["meta"]
    iris_content = pages["iris.html"](iris.read_text(encoding="utf-8"))
    iris_content = replace_marker(
        iris_content,
        "iris/header",
        (
            f'\n        <h1 class="display-title">{esc(iris_header["title"])}</h1>\n'
            f'        <span class="mono-label">{esc(iris_header["subtitle"])}</span>\n        '
        ),
    )
    iris_content = replace_marker(iris_content, "iris/body", render_iris_body(sections["iris / body"]))
    iris_content = replace_marker(
        iris_content,
        "iris/links",
        render_iris_links(sections["iris / links"]["table"]),
    )
    iris.write_text(replace_marker(iris_content, "global/footer", footer), encoding="utf-8")

    projects = ROOT / "projects.html"
    projects_content = pages["projects.html"](projects.read_text(encoding="utf-8"))
    projects_content = replace_marker(
        projects_content,
        "projects/heading",
        (
            f'\n        <header class="page-hero">\n'
            f'          <h1 class="page-title">{esc(sections["projects / page"]["meta"]["heading"])}</h1>\n'
            f'          <p class="page-subtitle">Proposals, reports, and downloadable PDFs</p>\n'
            f"        </header>\n        "
        ),
    )
    projects_content = replace_marker(
        projects_content,
        "projects/rows",
        render_project_entries(sections["projects / releases"]["table"]),
    )
    projects.write_text(replace_marker(projects_content, "global/footer", footer), encoding="utf-8")

    blog = ROOT / "blog.html"
    blog_content = pages["blog.html"](blog.read_text(encoding="utf-8"))
    blog_content = replace_marker(
        blog_content,
        "blog/heading",
        (
            f'\n        <header class="page-hero">\n'
            f'          <h1 class="page-title">{esc(sections["blog / page"]["meta"]["heading"])}</h1>\n'
            f'          <p class="page-subtitle">Research notes — no scrolling through walls of text</p>\n'
            f"        </header>\n        "
        ),
    )
    blog_content = replace_marker(
        blog_content,
        "blog/posts",
        render_blog_posts(sections["blog / posts"]["table"]),
    )
    blog.write_text(replace_marker(blog_content, "global/footer", footer), encoding="utf-8")

    contact = ROOT / "contact.html"
    contact_links = sections["contact / links"]["meta"]
    email = contact_links.get("email", "")
    if not email:
        raise ValueError("contact / links is missing @email")
    contact_content = pages["contact.html"](contact.read_text(encoding="utf-8"))
    contact_content = replace_marker(
        contact_content,
        "contact/header",
        f'\n          <h1 class="display-title">{esc(sections["contact / header"]["meta"]["name"])}</h1>\n\n          ',
    )
    contact_content = replace_marker(
        contact_content,
        "contact/links",
        (
            f'\n          <ul class="contact-list">\n'
            f'            <li><a href="mailto:{esc(email)}">{esc(email)}</a></li>\n'
            f'            <li><a href="{esc(contact_links["linkedin"])}" rel="noopener noreferrer">{esc(contact_links["linkedin-label"])}</a></li>\n'
            f'            <li><a href="{esc(contact_links["github"])}" rel="noopener noreferrer">{esc(contact_links["github-label"])}</a></li>\n'
            f"          </ul>\n\n          "
        ),
    )
    contact_content = replace_marker(
        contact_content,
        "contact/body",
        render_contact_body(sections["contact / body"]),
    )
    contact_content = replace_marker(
        contact_content,
        "contact/credentials",
        render_contact_credentials(sections["contact / credentials"]),
    )
    contact.write_text(replace_marker(contact_content, "global/footer", footer), encoding="utf-8")

    build_blog_posts(footer)

    print("Updated HTML from content/COPY.md")


if __name__ == "__main__":
    try:
        build()
    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
