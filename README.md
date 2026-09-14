# varunsharma.net

Source for [www.varunsharma.net](https://www.varunsharma.net), a statically generated personal website hosted on GitHub Pages with DNS managed by Cloudflare.

## How It Works

The site is built from three main inputs:

- `data.yaml` contains the site's content and configuration.
- `templates/index.html` defines the page markup using Jinja.
- `static/` contains the CSS, JavaScript, icons, images, and resume.

Running `generate.py` renders the site into `dist/`. During a normal build it also fetches metadata for links listed under `posts`; if a fetch fails, the build keeps the values already present in `data.yaml`. The generated directory is ignored by Git because GitHub Actions creates it for every deployment.

## Local Development

Python 3.12 is used by the deployment workflow. Create a virtual environment and install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Build and serve the site:

```sh
python generate.py
python -m http.server 8000 --directory dist
```

Open [http://localhost:8000](http://localhost:8000).

To build without requesting external post metadata, use:

```sh
python generate.py --skip-post-metadata
```

## Updating the Site

Most updates only require changes to `data.yaml`:

- `page` controls the title, canonical URL, and asset paths.
- `deployment.custom_domain` controls the generated GitHub Pages `CNAME` file.
- `basic`, `about`, `experience`, `education`, `skills`, `posts`, and `contact` contain the visible content.
- `assets` maps icons used by the template.

Update `templates/index.html` for markup changes and `static/` for styling, behavior, or media. Run a local build before pushing to verify that the template renders successfully.

Do not edit `dist/` directly. It is deleted and regenerated on every build.

## Deployment

The site is deployed from the `main` branch by `.github/workflows/deploy.yml`. The workflow:

1. Checks out the repository.
2. Sets up Python 3.12 and installs `requirements.txt`.
3. Runs `python generate.py`.
4. Uploads `dist/` as the GitHub Pages artifact.
5. Deploys the artifact with the official GitHub Pages actions.

Push to `main` to deploy, or run **Deploy static site to GitHub Pages** manually from the repository's **Actions** tab.

The repository's **Settings > Pages > Build and deployment** source must be set to **GitHub Actions**. The custom domain should be `www.varunsharma.net`, with **Enforce HTTPS** enabled after GitHub validates the DNS configuration.

## Domain and Cloudflare DNS

Cloudflare is the authoritative DNS provider for `varunsharma.net`. The canonical hostname is `www.varunsharma.net`, configured in `data.yaml`:

```yaml
deployment:
  custom_domain: www.varunsharma.net
```

The generator writes this value to `dist/CNAME`, which tells GitHub Pages which custom domain to serve. Keep the Cloudflare zone and GitHub Pages custom-domain setting aligned with this value.

Configure these records in Cloudflare DNS with **Proxy status** set to **Proxied**:

| Type | Name | Target |
| --- | --- | --- |
| `CNAME` | `www` | `thevarunsharma.github.io` |
| `A` | `@` | `185.199.108.153` |
| `A` | `@` | `185.199.109.153` |
| `A` | `@` | `185.199.110.153` |
| `A` | `@` | `185.199.111.153` |
| `AAAA` | `@` | `2606:50c0:8000::153` |
| `AAAA` | `@` | `2606:50c0:8001::153` |
| `AAAA` | `@` | `2606:50c0:8002::153` |
| `AAAA` | `@` | `2606:50c0:8003::153` |

The apex records allow GitHub Pages to redirect `varunsharma.net` to the canonical `www` hostname. Remove conflicting `A`, `AAAA`, or `CNAME` records for `@` and `www`.

Cloudflare proxies these records in front of GitHub Pages. Use **Full (strict)** under **SSL/TLS > Overview**, enable **Always Use HTTPS** under **SSL/TLS > Edge Certificates**, and keep GitHub Pages' **Enforce HTTPS** option enabled. Do not use Cloudflare's **Flexible** mode.

After changing DNS, confirm that GitHub reports the custom domain as verified under **Settings > Pages**. DNS and certificate changes may take time to propagate.

## Repository Layout

```text
.
├── .github/workflows/deploy.yml
├── data.yaml
├── generate.py
├── requirements.txt
├── static/
├── templates/index.html
└── utils/scrape/
```