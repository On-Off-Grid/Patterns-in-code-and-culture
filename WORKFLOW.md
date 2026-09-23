# Operational & Git Workflow Guide

This document outlines the step-by-step procedures for managing **Patterns in Code and Culture**, serving content via **Inception**, and maintaining Git repositories both individually and under the umbrella workspace.

---

## 1. Content Authoring & Publishing Workflow

### A. Writing & Publishing a New Note
1. **Create Source Markdown File**:
   Add a new file in `content/notes/published/my-note-slug.md`.
2. **Add Frontmatter Header**:
   ```yaml
   ---
   title: "Title of My Note"
   slug: "my-note-slug"
   date: "YYYY-MM-DD"
   pillar: "student-to-systems"
   tags: ["systems", "linux", "c++"]
   summary: "A short 1-2 sentence summary of what this note is about."
   status: "published"
   ---

   # Title of My Note

   Write your article in standard Markdown...
   ```
   *Available Pillars*: `student-to-systems` | `fields-to-models` | `beyond-the-herd` | `working-memory`
3. **Compile HTML Posts & Update Index**:
   ```bash
   python3 scripts/build_blog.py
   ```
   *What happens automatically*:
   - Generates `content/posts/my-note-slug.html`.
   - Formats `YYYY-MM-DD` date into readable display strings.
   - Injects card entry into `blog.html` under the matching `#student-to-systems` section.

### B. Updating Hand-Edited Structural Pages
- **Current Focus Log**: Edit `now.html` directly.
- **About / Pillars Overview**: Edit `about.html` or `pillars.html` directly.
- **Site Styling**: Edit `assets/css/styles.css`.

---

## 2. Local Infrastructure Workflow (`inception`)

### A. Starting & Stopping the Stack
```bash
cd /home/souhail/Desktop/Desktop/PORTFOLIO/inception

# Start the stack (Nginx + WordPress + MariaDB)
make up

# View container status
make status

# View live Nginx / PHP / MariaDB logs
make logs

# Stop the stack
make stop
```

### B. Accessing the Local Site
- Main Static Site: `https://souichou.42.fr` or `https://localhost`
- WordPress Admin (if enabled): `https://souichou.42.fr/wp-admin`

---

## 3. Individual Repository Git & PR Workflow

Always use feature branches and Pull Requests (PRs) when pushing changes.

### Step 1: Create a Feature Branch
```bash
cd /home/souhail/Desktop/Desktop/PORTFOLIO/Patterns-in-code-and-culture

git checkout main
git pull origin main
git checkout -b feature/my-new-post
```

### Step 2: Stage and Commit Changes
```bash
# Check modified files
git status

# Stage content changes
git add content/notes/published/my-note-slug.md content/posts/my-note-slug.html blog.html
git commit -m "feat(blog): add note on debugging Linux memory leaks"
```

### Step 3: Push & Review Pull Request (PR)
```bash
git push -u origin feature/my-new-post
```
1. Open `https://github.com/On-Off-Grid/Patterns-in-code-and-culture/pulls`.
2. Click **Create Pull Request**, review the diff, and click **Merge**.

### Step 4: Sync Local Main Branch
```bash
git checkout main
git pull origin main
git branch -d feature/my-new-post
```

---

## 4. Umbrella Workspace Management (`PORTFOLIO`)

Your main `/PORTFOLIO` folder holds multiple repositories (`Patterns-in-code-and-culture`, `inception`, `CPPS`, `philosophers`, etc.).

### Option A: Standalone Multi-Repo Pattern (Recommended Default)
Each folder maintains its own independent `.git` directory.

#### Status Check Across All Repos
Run from `/PORTFOLIO` root:
```bash
for d in */; do
  if [ -d "$d/.git" ]; then
    echo "=== 📂 Repo: $d ==="
    git -C "$d" status -s
  fi
done
```

---

### Option B: Git Submodule Pattern (Umbrella Workspace)
If you track all sub-projects under a master `/PORTFOLIO` Git repository:

#### 1. Adding a Submodule to Parent Repo
```bash
cd /home/souhail/Desktop/Desktop/PORTFOLIO
git init  # If parent is not yet initialized

git submodule add git@github.com:On-Off-Grid/Patterns-in-code-and-culture.git Patterns-in-code-and-culture
git submodule add git@github.com:On-Off-Grid/inception.git inception
git submodule add git@github.com:On-Off-Grid/CPPS.git CPPS
git submodule add git@github.com:On-Off-Grid/Philo_lakhar.git philosophers

git commit -m "chore: add project submodules"
```

#### 2. Cloning an Umbrella Repo with Submodules
```bash
git clone --recursive <parent-repo-url>
# OR if already cloned without submodules:
git submodule update --init --recursive
```

#### 3. Updating All Submodules to Latest Remote Commits
```bash
git submodule update --remote --merge
```

#### 4. Committing Submodule Pointer Updates in Parent Repo
When you push a commit inside a submodule (`Patterns-in-code-and-culture`), the parent `PORTFOLIO` repo notices the updated commit hash:
```bash
cd /home/souhail/Desktop/Desktop/PORTFOLIO
git add Patterns-in-code-and-culture
git commit -m "chore: update Patterns-in-code-and-culture submodule reference"
git push origin main
```
