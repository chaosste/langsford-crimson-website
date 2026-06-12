# IRIS Research Lab

Static website for IRIS Research Lab — cognitive science for machine learning.

## Pages

| Page | File |
|------|------|
| Home | `index.html` |
| IRIS | `iris.html` |
| Research | `research.html` |
| Blog | `blog.html` |
| Contact | `contact.html` |

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
