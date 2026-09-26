# KII'26 Website — README

This is a single self-contained page (`index.html`) built from your Stitch
design. No build step, no framework, no install — just HTML, Tailwind
(loaded from a CDN), and a little vanilla JavaScript.

## Files in this folder

| File | What it is |
|---|---|
| `index.html` | The whole website |
| `favicon.png` | Placeholder browser-tab icon — **replace with your real logo** |
| `logo-navbar.png` | Placeholder logo shown top-left in the navbar — **replace** |
| `hero-banner.png` | Placeholder graphic shown in the hero section — **replace** |
| `DESIGN.md` | Stitch's design-system reference (colors, type) — for reference only, not used by the live page |

To swap an image, just replace the file with your real one **using the exact
same filename**. No code changes needed.

## Two bugs from the Stitch export that were fixed here

1. **The "View Problem Statements" buttons on all 7 Research Circle cards
   did nothing.** Stitch generated buttons that called a JavaScript function
   (`toggleCircleAccordion`) that was never actually defined anywhere in the
   exported code. This is now fixed near the bottom of the file (search for
   `toggleCircleAccordion`).
2. **The page's `<head>` was empty** — all the font links, Tailwind config,
   and styles had been dumped into the `<body>` instead. Browsers mostly
   tolerate this, but it's invalid and can cause flaky font/style loading.
   Fixed — everything now lives in a proper `<head>`.

## How to edit things

Everything is plain text inside the HTML — search for the words you see on
the page and edit them directly. A few things are made deliberately easy to
find:

- **Add the 105 problem statements**: search the file for `PROBLEM STATEMENT`.
  Each of the 105 placeholder slots (15 per Research Circle × 7 circles) has
  its own comment right above it, e.g.:
  ```html
  <!-- PROBLEM STATEMENT 1 — replace title + description below with the real one -->
  <div ...><span ...>Problem Statement 1 — [Title placeholder]</span>
  <span ...>[Add problem statement description here]</span></div>
  ```
  Just replace `[Title placeholder]` and `[Add problem statement description
  here]` with the real text for that slot.

- **Change the registration form link**: search for `REGISTRATION_FORM_URL`
  near the bottom of the file. It's one line:
  ```js
  const REGISTRATION_FORM_URL = "https://forms.cloud.microsoft/r/8vwUR24YmA";
  ```
  Change the URL and **all 5** Register buttons on the page (navbar, mobile
  menu, hero, the big Register section, footer) update automatically.

- **Every major section is labeled** with a big comment block, e.g.:
  ```html
  <!-- ============================================================
       SECTION: RESEARCH CIRCLES — 7 circles x 15 problem-statement
       placeholders (105 total)
  ============================================================ -->
  ```
  Search for `SECTION:` to jump between them, or just use your editor's
  outline/minimap.

## Previewing locally before you deploy

You don't need a server for this, but if double-clicking the file causes any
issues, run this from inside the folder and open the printed address:

```bash
python3 -m http.server 8000
```

## Deploying to Vercel

Two ways to do it — pick whichever is easier for your team:

### Option A — Drag and drop (fastest, good for a one-off)
1. Go to [vercel.com](https://vercel.com) and sign in (GitHub/Google/email).
2. From the dashboard, choose **Add New → Project**, then look for the
   drag-and-drop upload option.
3. Drag this whole folder in and deploy.
4. Vercel gives you a live URL immediately (e.g. `kii26.vercel.app`), and
   you can attach a custom domain later from the project settings if the
   college gives you one.

### Option B — Connect a GitHub repo (recommended for a club — lets next
year's team update the site easily, and every push auto-deploys)
1. Create a new GitHub repository and push this folder to it.
2. In Vercel: **Add New → Project → Import Git Repository**, select the repo.
3. Framework preset: choose **Other** (it's a plain static site, no build
   command needed).
4. Deploy. From then on, any push to the repo's main branch redeploys the
   site automatically.

Either way, hosting is free on Vercel's default plan for a site like this.

## Next steps / open items

- [ ] Swap `favicon.png`, `logo-navbar.png`, `hero-banner.png` for real assets
- [ ] Fill in all 105 problem statements (search `PROBLEM STATEMENT`)
- [ ] Double-check the registration form link is the final one before go-live
- [ ] Deploy to Vercel and share the live link
