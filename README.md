# Patterns in Code and Culture: Notes of a Self-Aware Engineer

A static personal blog and engineering notebook serving thoughts across systems, networking, agriculture/AI, and philosophy.

---

## 🛠️ Build Requirements & Setup

This repository uses a zero-framework, static-first architecture. HTML post generation and index updates are powered by a lightweight Python build script.

### Prerequisites
- **Python 3.8+**
- **Python `markdown` package**:
  ```bash
  pip install markdown
  ```

---

## 🚀 How to Build the Blog

1. Add or edit a Markdown file in `content/notes/published/my-note.md` with standard YAML frontmatter:
   ```yaml
   ---
   title: "My Note Title"
   slug: "my-note-title"
   date: "2026-09-22"
   pillar: "student-to-systems"
   tags: ["systems", "linux", "c++"]
   summary: "Short excerpt for the post card."
   status: "published"
   ---

   # My Note Title
   Note content in standard Markdown...
   ```

2. Run the build script:
   ```bash
   python3 scripts/build_blog.py
   ```

3. The build script automatically:
   - Renders HTML post files into `content/posts/<slug>.html`.
   - Formats `YYYY-MM-DD` dates into readable display strings.
   - Updates pillar-grouped section blocks in `blog.html` between `<!-- POSTS:START -->` and `<!-- POSTS:END -->`.

---

## 📂 Architecture & Routing

- **Structural Shell Pages**: `index.html`, `about.html`, `pillars.html`, `blog.html`, `now.html`, `404.html`, `post-template.html`.
- **Primary Content Index**: `blog.html` contains pillar section anchors (`#student-to-systems`, `#fields-to-models`, `#beyond-the-herd`, `#working-memory`).
- **Post Pages**: Served directly from `content/posts/<slug>.html`.

---

## 📖 Operational & Git Workflow

For detailed instructions on authoring posts, managing Docker infrastructure, pushing Git feature branches/PRs, and managing submodules under the umbrella workspace, see **[WORKFLOW.md](WORKFLOW.md)**.
