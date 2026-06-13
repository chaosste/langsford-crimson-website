## Learned User Preferences

- Prefer JetBrains Mono for body copy across the site (not Inter).
- Prefer square-dimension images on home page rows (not landscape).
- Edit site copy in `content/COPY.md` and `content/BLOG_POSTS.md`, then run `python3 scripts/build-copy.py` — not direct HTML edits for copy.
- Reuse the COPY.md master-copy workflow on future static sites via the `static-site-copy` Cursor skill at `~/.cursor/skills/static-site-copy/`.
- Do not edit plan files when implementing attached plans.
- Complete all existing plan todos in order; mark them in_progress/completed rather than recreating them.
- Use Pixelcastle for main display headers site-wide; IRIS page uses Redaction 35 instead.
- Sub-headers and H1 use JetBrains Mono (body font), not Pixelcastle.
- NeoVim/hacker green palette on all pages except IRIS page, which keeps the purple tint from the main-branch Redaction 35 theme.

## Learned Workspace Facts

- Albion Research static site: plain HTML/CSS at `langsford_crimson_website` (no framework or SSG).
- Master copy: `content/COPY.md` synced to HTML via `scripts/build-copy.py` and `<!-- copy:... -->` markers.
- Blog articles: `content/BLOG_POSTS.md` (YAML frontmatter + body) generates `blog/*.html`.
- Typography: Pixelcastle display headings + JetBrains Mono body/sub-headers on most pages; IRIS page uses Redaction 35 headings with purple-tint body text (`#6c5ce7`).
- Retro theme overlay: `theme-pixelcastle.css` (hacker green palette) applied via `body.theme-pixelcastle` on all pages.
- Nav labels: Home, IRIS, Projects, Blog, Contact; Projects page lists downloadable PDFs in `assets/pdfs/`.
- IRIS page uses Blake Laocoön ghost background (`assets/images/iris-bg-blake.png`), solid nav strip, spaced body copy.
- Home page rows use square images in `assets/images/`: fractal-eye, fractal-island, elite_sq, home-cognitive-science.
- Deploy via `.github/workflows/deploy.yml` (GitHub Pages or Cloudflare Pages).
- Sibling reference project `stevelangsfordbeale_website` (Next.js) is a separate repo, not in this workspace.
