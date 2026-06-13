## Learned User Preferences

- Prefer JetBrains Mono for body copy across the site (not Inter).
- Prefer square-dimension images on home page rows (not landscape).
- Edit site copy in `content/COPY.md` and `content/BLOG_POSTS.md`, then run `python3 scripts/build-copy.py` — not direct HTML edits for copy.
- Reuse the COPY.md master-copy workflow on future static sites via the `static-site-copy` Cursor skill at `~/.cursor/skills/static-site-copy/`.
- Do not edit plan files when implementing attached plans.
- Complete all existing plan todos in order; mark them in_progress/completed rather than recreating them.

## Learned Workspace Facts

- IRIS Research Lab static site: plain HTML/CSS at `langsford_crimson_website` (no framework or SSG).
- Master copy: `content/COPY.md` synced to HTML via `scripts/build-copy.py` and `<!-- copy:... -->` markers.
- Blog articles: `content/BLOG_POSTS.md` (YAML frontmatter + body) generates `blog/*.html`.
- Typography: Redaction 35 display headings (self-hosted woff2), JetBrains Mono body, dark-mode-first (`#0a0a0a` bg, `#6c5ce7` accent).
- Nav labels: HOME, IRIS, RESEARCH, BLOG, CONTACT; RESEARCH page holds the curated releases table.
- IRIS page uses Blake Laocoön ghost background (`assets/images/iris-bg-blake.png`).
- Home page rows use square images in `assets/images/`: fractal-eye, fractal-island, elite_sq.
- Deploy via `.github/workflows/deploy.yml` (GitHub Pages or Cloudflare Pages).
- Sibling reference project `stevelangsfordbeale_website` (Next.js) is a separate repo, not in this workspace.
