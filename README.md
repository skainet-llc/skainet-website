# skainet-website

Website of skAInet, served with GitHub Pages:
<https://skainet.io/>

Hand-written static HTML in the visual language of the WITNESS landing page
(Biryani, `#262626` / `#E83B3B`, square shapes). No build step, no tracking, no external requests.

## Layout

- `index.html`, `services/`, `about/`, `contact/`, `imprint/`, `privacy/`: the six pages.
  Header and footer are repeated in each file, so change them in all six.
- `assets/css/style.css`: all styles
- `assets/js/main.js`: mobile menu and background-video control
- `assets/video/`: background videos (720p, no audio) with poster stills
- `assets/img/`, `assets/logos/`, `assets/fonts/`: images, reference logos, Biryani

All links are relative, so the site works under the project path and under a custom domain.

## Background videos

Home uses `pcb.mp4`, Services uses `inventor.mp4` and `tabea.mp4`. They play muted and looped,
only while visible, stay paused for visitors who prefer reduced motion, and each has a pause button.

## History

The first commits hold a static mirror of the former WordPress site, kept for reference.

A push to `main` deploys through `.github/workflows/pages.yml`.
