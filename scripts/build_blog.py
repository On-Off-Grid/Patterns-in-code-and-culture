#!/usr/bin/env python3
"""
Blog Builder for Patterns in Code and Culture
---------------------------------------------
Reads Markdown notes from `content/notes/published/`, compiles them into HTML
pages in `content/posts/`, and updates pillar-grouped post sections in `blog.html`.

Dependencies:
    - Python 3.8+ (standard library)
    - markdown (pip install markdown)

Usage:
    python3 scripts/build_blog.py
"""

import argparse
from datetime import datetime
import json
import re
from pathlib import Path
import markdown

# Core Pillars Configuration
PILLARS = {
    "student-to-systems": {
        "title": "From student to systems",
        "description": "Notes from the path through Tech/IT, AI, research, tools, and systems thinking."
    },
    "fields-to-models": {
        "title": "From fields to models",
        "description": "Observations from agriculture, startup realities, and farming technology."
    },
    "beyond-the-herd": {
        "title": "Beyond the herd",
        "description": "Reflections on society, psychology, human behavior, and technology."
    },
    "working-memory": {
        "title": "Working memory",
        "description": "A meta-journal for preserving ideas, tracking mindset shifts, and revisited lessons."
    }
}

def format_date(date_str: str) -> str:
    """Formats YYYY-MM-DD string to a readable date (e.g. '2026-06-15' -> 'June 15, 2026')."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return date_str

def parse_frontmatter(file_content: str):
    """
    Manually parses a constrained YAML frontmatter header (--- ... ---) using stdlib string methods.
    Returns a tuple of (metadata_dict, body_markdown).
    """
    if not file_content.startswith("---"):
        return {}, file_content

    parts = file_content.split("---", 2)
    if len(parts) < 3:
        return {}, file_content

    header_text = parts[1].strip()
    body_text = parts[2].strip()

    metadata = {}
    for line in header_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            # Simple string / JSON array parsing for frontmatter fields
            if val.startswith("[") and val.endswith("]"):
                try:
                    val = json.loads(val.replace("'", '"'))
                except Exception:
                    val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
            elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            metadata[key] = val

    return metadata, body_text

def build_post_html(meta: dict, body_html: str, template: str) -> str:
    """Renders the HTML content for an individual post using post-template.html."""
    pillar_slug = meta.get("pillar", "working-memory")
    pillar_info = PILLARS.get(pillar_slug, PILLARS["working-memory"])
    formatted_date = format_date(meta.get("date", ""))

    rendered = template
    rendered = rendered.replace("{{title}}", meta.get("title", "Untitled"))
    rendered = rendered.replace("{{summary}}", meta.get("summary", ""))
    rendered = rendered.replace("{{date}}", formatted_date)
    rendered = rendered.replace("{{pillar_name}}", pillar_info["title"])
    rendered = rendered.replace("{{pillar_slug}}", pillar_slug)
    rendered = rendered.replace("{{content}}", body_html)

    return rendered

def build_index_sections(posts_by_pillar: dict) -> str:
    """Generates pillar-grouped HTML section blocks for injection into blog.html."""
    sections_html = []

    for pillar_slug, pillar_info in PILLARS.items():
        posts = posts_by_pillar.get(pillar_slug, [])

        section_markup = [
            f'    <section class="section" id="{pillar_slug}">',
            '      <div class="container">',
            f'        <p class="section-label">{pillar_info["title"]}</p>',
            f'        <p class="section-text" style="margin-bottom: 1.5rem;">{pillar_info["description"]}</p>'
        ]

        if posts:
            section_markup.append('        <div class="pillars-grid">')
            for p in posts:
                tags_str = " ".join([f"#{t}" for t in p.get("tags", [])])
                formatted_date = format_date(p.get("date", ""))
                card = (
                    '          <article class="pillar-card">\n'
                    f'            <p class="pillar-number">{formatted_date}</p>\n'
                    f'            <h3><a href="/content/posts/{p.get("slug")}.html" style="text-decoration: underline; color: inherit;">{p.get("title")}</a></h3>\n'
                    f'            <p>{p.get("summary", "")}</p>\n'
                    f'            <div class="card-meta" style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.8;">\n'
                    f'              <span>{tags_str}</span>\n'
                    '            </div>\n'
                    '          </article>'
                )
                section_markup.append(card)
            section_markup.append('        </div>')
        else:
            section_markup.append('        <p style="opacity: 0.7; font-style: italic;">No posts published in this pillar yet.</p>')

        section_markup.append('      </div>')
        section_markup.append('    </section>')

        sections_html.append("\n".join(section_markup))

    return "\n\n".join(sections_html)

def update_blog_index(blog_html_path: Path, sections_content: str):
    """Updates only the content inside <!-- POSTS:START --> and <!-- POSTS:END --> in blog.html."""
    content = blog_html_path.read_text(encoding="utf-8")

    pattern = r"(<!-- POSTS:START -->)(.*?)(<!-- POSTS:END -->)"
    replacement = f"\\1\n    <!-- Generated by scripts/build_blog.py — Do not edit inside this block manually -->\n{sections_content}\n    \\3"

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
    if count == 0:
        raise ValueError("Could not find <!-- POSTS:START --> and <!-- POSTS:END --> markers in blog.html")

    blog_html_path.write_text(new_content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Build Patterns in Code and Culture static blog.")
    parser.add_argument("--root", type=str, default=".", help="Root path of the repository")
    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if (root_path / "Patterns-in-code-and-culture").exists():
        base_dir = root_path / "Patterns-in-code-and-culture"
    else:
        base_dir = root_path

    published_dir = base_dir / "content" / "notes" / "published"
    posts_output_dir = base_dir / "content" / "posts"
    template_path = base_dir / "post-template.html"
    blog_html_path = base_dir / "blog.html"

    posts_output_dir.mkdir(parents=True, exist_ok=True)
    template_content = template_path.read_text(encoding="utf-8")

    posts_by_pillar = {p: [] for p in PILLARS.keys()}

    # Parse and compile published markdown notes
    md_files = list(published_dir.glob("*.md"))
    print(f"[BUILD] Found {len(md_files)} published note(s) in {published_dir}")

    for md_file in md_files:
        raw_text = md_file.read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(raw_text)

        if meta.get("status") != "published":
            continue

        slug = meta.get("slug", md_file.stem)
        meta["slug"] = slug

        # Convert Markdown body to HTML
        body_html = markdown.markdown(
            body_md,
            extensions=["fenced_code", "tables", "footnotes", "attr_list"]
        )

        # Build individual HTML post
        post_html = build_post_html(meta, body_html, template_content)
        output_post_path = posts_output_dir / f"{slug}.html"
        output_post_path.write_text(post_html, encoding="utf-8")
        print(f"[BUILD] Rendered post -> {output_post_path.relative_to(base_dir)}")

        pillar = meta.get("pillar", "working-memory")
        if pillar in posts_by_pillar:
            posts_by_pillar[pillar].append(meta)
        else:
            posts_by_pillar["working-memory"].append(meta)

    # Update blog.html index
    sections_html = build_index_sections(posts_by_pillar)
    update_blog_index(blog_html_path, sections_html)
    print(f"[BUILD] Updated master index -> {blog_html_path.relative_to(base_dir)}")
    print("[BUILD] Blog build completed successfully!")

if __name__ == "__main__":
    main()
