# skainet-website

Static copy of the WordPress site at <https://skainet.io>, served with GitHub Pages:
<https://skainet-llc.github.io/skainet-website/>

## Layout

- `index.html`, `about/`, `contact/`, `imprint/`, `privacy/`, `services/`: the six pages
- `wp-content/`, `wp-includes/`: theme, plugin and media files the pages load
- `assets/static-form.js`: replaces the Contact Form 7 backend. Submitting the form opens
  the visitor's mail client with a message to `info@skainet.io`
- `tools/mirror.sh`: re-fetches the live site with `wget` and runs `tools/clean.py`
- `tools/clean.py`: strips query strings from file names, removes links to WordPress
  endpoints, sets the canonical URL to `https://skainet.io/...` and adds the form script

All links are relative, so the site works under the project path and under a custom domain.

## Update from the live site

```sh
tools/mirror.sh
git add -A && git commit -m "Refresh mirror" && git push
```

A push to `main` deploys through `.github/workflows/pages.yml`.
