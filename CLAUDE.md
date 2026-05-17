# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

An Astro 5 + MDX site that renders a single-page academic research project page. All content lives in `src/paper.mdx`; the layout is `src/pages/index.astro`.

## Commands

```bash
npm run dev          # dev server → http://localhost:4321
npm run build        # typecheck (astro check) + build → ./dist/
npm run check        # typecheck only
npm run lint         # ESLint
npm run format:fix   # Prettier --write
npm run all:fix      # check + lint:fix + format:fix
```

There are no tests. `npm run build` is the full validation pass.

## Non-obvious conventions

**Content model:** `src/pages/index.astro` imports both `Content` and `frontmatter` from `src/paper.mdx`. Frontmatter keys (`title`, `authors`, `favicon`, `conference`, `notes`, `links`, `description`, `thumbnail`, `theme`) are typed in the layout file itself.

**Theming:** `data-theme` on `<html>` (set from the `theme` frontmatter field) drives Tailwind's `dark:` variant — not `prefers-color-scheme` — unless `theme: device` is set.

**PDF images:** `Picture.astro` accepts a string PDF path (relative to `src/pages/`) and converts page 1 to PNG at 4× scale via `src/lib/render-pdf.ts` during build. In dev it reads from `../dist/_astro/`; in prod from `_astro/`.

**Public asset URLs:** Always prefix with `import.meta.env.BASE_URL` (the layout exposes it as `prefix`). Hardcoded paths break GitHub Pages deployment.

**React components:** Require a `client:*` hydration directive at the usage site in MDX (e.g., `<Comparison client:idle>`).

**Icons:** `astro-icon` with Iconify. Pre-installed sets: `academicons`, `ri`. To add another: `npm install @iconify-json/<set>`.

**Citations:** Put BibTeX entries in `bibliography.bib`; reference them in MDX with standard citation syntax — `rehype-citation` handles rendering.

**Deploy:** Pushing to `main` builds and deploys via `.github/workflows/astro.yml` (GitHub Pages). CI uses Node 20; local docs recommend Node 24.
