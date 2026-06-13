# IRIS Research Lab

Static website for IRIS Research Lab — cognitive science for machine learning.

## Pages

| Page | File |
|------|------|
| Home | `index.html` |
| IRIS | `iris.html` |
| Projects | `projects.html` |
| Blog | `blog.html` |
| Blog posts | `blog/*.html` (generated) |
| Contact | `contact.html` |

## Editing site copy

All live copy lives in **[content/COPY.md](content/COPY.md)** and **[content/BLOG_POSTS.md](content/BLOG_POSTS.md)** — edit those files, then sync to HTML:

```bash
python3 scripts/build-copy.py
```

See the **static-site-copy** Cursor skill (`~/.cursor/skills/static-site-copy/`) for the full COPY.md format and how to reuse this pattern on other static sites.

**Format:**
- `## page / section` headings divide content by page
- `@key: value` lines set metadata (titles, URLs, images)
- Plain text below metadata is body copy (blank line between paragraphs)
- Markdown tables hold lists (research releases, blog index, IRIS links)
- Full blog articles: YAML frontmatter + body in `BLOG_POSTS.md` → `blog/slug.html`

You can edit HTML directly for layout tweaks, but copy changes should go through `COPY.md` / `BLOG_POSTS.md` so nothing drifts out of sync.

## Local preview

From the project root:

```bash
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080).

## Deploy to GitHub Pages

1. Create a GitHub repository and push this folder.
2. In repo **Settings → Pages**, set source to **GitHub Actions**.
3. Push to `main` — the workflow in `.github/workflows/deploy.yml` publishes automatically.

For a custom domain (e.g. `iris-lab.dev`), add a `CNAME` record pointing to `<username>.github.io` and configure the domain in GitHub Pages settings.

## Pixelcastle retro theme (alternate branch)

Branch `design/pixelcastle-retro` adds an 8-bit inspired layout using the **Pixelcastle** display font (`fonts/Pixelcastle.otf`, OFL licensed).

Preview locally on that branch:

```bash
git checkout design/pixelcastle-retro
python3 -m http.server 8080
```

Pages load `styles.css` plus `theme-pixelcastle.css`. Home uses a Quick Answers card grid; Projects uses a Changelog stack; blog cards use double-line retro frames.

## Deploy to Cloudflare Pages

1. Connect the GitHub repo in Cloudflare Pages, or upload the folder directly.
2. Build command: *(none)*
3. Output directory: `/` (project root)

## Stack

- Plain HTML, one CSS file (`styles.css`), minimal JS (`script.js`)
- [Redaction 35](https://fontsource.org/fonts/redaction-35) (OFL-1.1, self-hosted)
- JetBrains Mono via Google Fonts (body + UI)
- Dark mode first, no build step required

## License

Site content © Stephen Langsford Beale 2026. Redaction 35 font licensed under SIL Open Font License 1.1.
