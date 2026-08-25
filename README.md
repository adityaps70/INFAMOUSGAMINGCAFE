# inFAMOUS Gaming Cafe website

A premium, mobile-first React/Vite website for inFAMOUS Gaming Cafe in Lucknow. It is intentionally a **static GitHub Pages site**: there is no server, database, CMS, account system, or payment dependency.

Booking works by preparing a detailed WhatsApp enquiry. Phone, Instagram, and Google Maps actions also open directly from the browser.

## Deploy on GitHub Pages

1. Create a GitHub repository and add this project to it.
2. Push from either `main` or `master` (the included workflow watches both).
3. Open **Settings → Pages → Build and deployment** and choose **GitHub Actions** as the source.
4. Push your current `main` or `master` branch.
5. The workflow in `.github/workflows/deploy-pages.yml` will run:
   - `npm ci`
   - `npm test`
   - `npm run build`
   - deployment of the generated `dist/` folder to GitHub Pages.

`vite.config.ts` deliberately uses `base: "./"`. That keeps built JS, CSS, logo, favicon, and social assets relative, so the same source works at both:

- `https://username.github.io/repository-name/`
- a custom domain connected to the repository later.

`public/.nojekyll` is also preserved so GitHub Pages serves the Vite build without Jekyll processing.

## Run locally

Use Node.js 24 or a compatible current Node release.

```bash
npm ci
npm run dev
```

Then use:

```bash
npm test
npm run build
npm run preview
```

`npm run build` includes `scripts/verify-dist.mjs`, which rejects root-relative built assets and verifies the static files required by GitHub Pages.

## Update cafe details

The main editable business information is deliberately centralized:

- `src/siteData.ts` — phone, address, rating text, certification text, availability wording.
- `src/rates.json` — approved rate-card data.
- `src/experienceData.ts` — experience browser copy and booking intent.
- `src/faqData.ts` — FAQ answers.
- `src/galleryData.ts` — venue-gallery entries.
- `src/links.ts` — Maps, Instagram, phone, and WhatsApp URL construction.

Do not hard-code alternate phone numbers, rates, or Maps URLs inside components. Update the central data modules instead.

## Add authentic venue photos

The gallery currently uses branded non-photographic placeholders rather than fake venue imagery.

To add real photos:

1. Put optimized images in a folder such as `public/gallery/`.
2. Edit `src/galleryData.ts`.
3. Add an `imageSrc` using a relative public path, for example `./gallery/arena.webp`.
4. Add a clear `imageAlt`, for example `PC gaming area inside inFAMOUS Gaming Cafe`.
5. Prefer WebP or AVIF for venue photography and keep each file reasonably compressed.

Because the layout is data-driven, no component rewrite is needed when real media is supplied.

## Connect a custom domain later

1. Follow GitHub Pages' current DNS instructions for the domain or `www` subdomain.
2. In **Settings → Pages → Custom domain**, enter the domain.
3. Add `public/CNAME` containing only that domain before the next build.
4. Enable **Enforce HTTPS** after DNS verification.
5. Once the final public domain exists, replace the relative `./og.png` values in `index.html` with the absolute HTTPS social-preview URL for the most reliable sharing previews.

## Static-site limitations by design

This version does not claim to show live station inventory or instant confirmed reservations. Current availability is confirmed by the cafe through WhatsApp or phone. This keeps the website fast, low-maintenance, and fully compatible with GitHub Pages.

Current contact number: **+91 99183 32386**.
