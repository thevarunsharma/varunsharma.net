# varunsharma.net

Static version of `varunsharma.net`, migrated from the existing Flask application. Production does not run Flask: `data.yaml` plus Jinja templates are rendered into static HTML by `generate.py`, then deployed through GitHub Pages.

## Repository Structure

```text
varunsharma.net/
├── data.yaml
├── generate.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   ├── icons/
│   ├── media/
│   └── scripts/
└── .github/
    └── workflows/
        └── deploy.yml
```

Generated output is written to `dist/` and is intentionally ignored by Git.

## Local Development

Create a virtual environment if desired, then install dependencies:

```sh
python -m pip install -r requirements.txt
```

Generate and serve the site locally:

```sh
python generate.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`.

For offline template-only checks, skip fetching external post metadata:

```sh
python generate.py --skip-post-metadata
```

## Content Editing

Most website content lives in `data.yaml`:

- `page`: title, canonical URL, local CSS/JS/icon paths
- `deployment`: GitHub Pages custom domain
- `basic`: profile, contact, resume, social links
- `about`, `experience`, `education`, `skills`, `posts`, `contact`: page content
- `assets`: local icon paths used by the template

Changing `data.yaml` and pushing to `main` triggers GitHub Actions, regenerates `dist/`, and deploys the updated static site.

## GitHub Pages Deployment

1. Create a new GitHub repository named `varunsharma.net`.
2. Push this repository to GitHub with `main` as the default branch.
3. In GitHub, go to `Settings` -> `Pages`.
4. Set `Build and deployment` source to `GitHub Actions`.
5. Push to `main` or run the `Deploy static site to GitHub Pages` workflow manually.

The workflow checks out the repository, installs dependencies from `requirements.txt`, runs `python generate.py`, uploads `dist/`, and deploys it with the official GitHub Pages actions.

## Custom Domain and DNS

The existing project context uses `https://www.varunsharma.net/`, so `data.yaml` currently sets:

```yaml
deployment:
  custom_domain: www.varunsharma.net
```

`generate.py` writes that value to `dist/CNAME`, so the deployed artifact includes the required GitHub Pages `CNAME` file. Keep the generated `CNAME` in the deployed artifact; do not hand-edit `dist/`.

Prefer `www.varunsharma.net` as the canonical GitHub Pages hostname and redirect the apex domain to `www` where your DNS provider supports it. This keeps DNS simple because `www` can be a CNAME.

Required DNS records for GitHub Pages are typically:

```text
www.varunsharma.net.  CNAME  thevarunsharma.github.io.
varunsharma.net.      A      185.199.108.153
varunsharma.net.      A      185.199.109.153
varunsharma.net.      A      185.199.110.153
varunsharma.net.      A      185.199.111.153
varunsharma.net.      AAAA   2606:50c0:8000::153
varunsharma.net.      AAAA   2606:50c0:8001::153
varunsharma.net.      AAAA   2606:50c0:8002::153
varunsharma.net.      AAAA   2606:50c0:8003::153
```

If GitHub username or organization differs from `thevarunsharma`, replace `thevarunsharma.github.io.` with the correct Pages hostname shown by GitHub.

The existing DNS config in the Flask repository points `www` and apex traffic at Azure Front Door. Move those records to GitHub Pages only when you are ready to cut over. After GitHub validates the domain, enable `Enforce HTTPS` in `Settings` -> `Pages`.

## Flask Migration Notes

Inspection of the source Flask repository found:

- Routes: a single `/` route in `app.py`.
- Templates: one Jinja template, `templates/index.html`; no inheritance or includes.
- Data source: `config.yaml`, passed into the template after post metadata enrichment.
- Static assets: CSS, JavaScript, icons, profile image, and resume under `static/`.
- Flask-specific template functionality: none found in the template; no `url_for()` usage.
- JavaScript behavior: sidebar toggle, tab navigation, and blog text clamping; no backend/API calls.
- Backend/API/database dependencies: no database and no runtime API endpoints. The only backend behavior was build-time-compatible scraping of Open Graph metadata for posts.

The old `utils/scrape` package has been copied into this repository and reused by `generate.py` for post metadata enrichment. It runs during the GitHub Actions build, so the generated website still does not require Flask in production. If a post cannot be fetched during a build, generation continues with the values already present in `data.yaml`.