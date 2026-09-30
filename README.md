# Kumaraguru Intra Ideathon'26 (KII'26) — Problem Statement Portal & Website

Static, responsive, offline-ready Problem Statement Portal and Landing Page for **Kumaraguru Intra Ideathon'26**, organized by **Ré – Centre for Exploratory Research**, Kumaraguru College of Technology.

---

## 1. Domain Problem Statement Counts

The portal hosts exactly **75 problem statements across 5 research domains** (exactly 15 challenges per domain):

| Domain | Problem Statement Range | Count | Primary Requester |
|---|---|---|---|
| **Automotive** | `KII26101` – `KII26115` | **15** | Automotive Research Team |
| **Bioscience** | `KII26201` – `KII26215` | **15** | Ré Bioscience |
| **Education** | `KII26301` – `KII26315` | **15** | Ré Research Cell & Faculty |
| **Renewable Energy** | `KII26401` – `KII26415` | **15** | Ré Forum |
| **Textile** | `KII26501` – `KII26515` | **15** | Ré Research Cell & Faculty |
| **Total** | | **75** | |

*Special Statuses in Textile:*
- `KII26511` – `KII26514`: `draft` (rendered with amber *"Draft — pending confirmation"* badge)
- `KII26515`: `placeholder` (rendered with dashed border and *"Statement awaiting submission"* note)

---

## 2. Project Architecture & Files

```
├── index.html                  # Portal Vite entry point
├── landing.html                # Original Ideathon landing page (preserved & linked)
├── package.json                # Project dependencies & scripts
├── vite.config.js              # Vite bundler configuration
├── scripts/
│   └── validate.js             # Data validation script (npm run validate)
├── public/                     # Static assets (favicons, logos, landing.html)
└── src/
    ├── main.jsx                # React root mount
    ├── App.jsx                 # Portal application layout & state
    ├── styles.css              # Custom styling, design tokens & print stylesheet
    ├── components/
    │   ├── DomainTabs.jsx      # Domain tabs with icons & counts (15 each)
    │   ├── ProblemCard.jsx     # Section 3 detail card & summary list card
    │   ├── SearchBar.jsx       # Multi-field search across code, title, scope, etc.
    │   ├── TagFilter.jsx       # Topic tag filter chips
    │   └── BookmarksPanel.jsx  # Saved problems drawer (persisted in localStorage)
    └── data/
        └── problems.json       # All 75 problem statement records (parsed verbatim)
```

---

## 3. Quickstart & Run Instructions

### Prerequisites
- Node.js (v18+ recommended; tested on v24)
- npm (v9+; tested on v11)

### Development Server
Start the local Vite development server:
```bash
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

### Data Validation
Run the built-in validation script to verify that all 75 problem statements strictly adhere to the schema, that every domain has exactly 15 records, that codes are unique, and that no required fields are missing:
```bash
npm run validate
```

### Production Build
Compile and bundle the production-ready static assets:
```bash
npm run build
```
The output will be placed in the `dist/` directory, ready to deploy to Vercel, Netlify, GitHub Pages, or any static web server.

### Local Preview of Production Bundle
Preview the production build locally:
```bash
npm run preview
```
Open [http://localhost:4173](http://localhost:4173).

---

## 4. Key Portal Features

1. **Section 3 Compliant Card Layout**:
   - Monospace Navy Code Badge (`Problem statement code: KII26xxx`)
   - Tag Chip & Draft/Placeholder Indicators
   - Large Bold Navy Title (`#0B2A6B`)
   - `Requested by:` metadata line
   - `CONTEXT & CORE CHALLENGE` rounded box with Crimson Info Icon & heading
   - Two-column responsive row:
     - Left: `TECHNICAL SCOPE & REQUIREMENTS` (bulleted list)
     - Right: `EXPECTED DELIVERABLES` (paragraphs, grey text)
   - Suggested Branches chips (where applicable, e.g. Automotive)
   - Sticky footer with Bookmark toggle pill

2. **Search & Tag Filtering**:
   - Deep search across code, title, tag, context, scope, and deliverables
   - Toggle to search within the active domain or across all 75 statements
   - Dynamic tag filter chips derived from active domain problem tags

3. **Persistent Bookmarks**:
   - Bookmark any problem statement from summary or detail views
   - Saved statements persist across browser sessions using `localStorage`
   - Slide-over "Saved" panel with count, item preview, and "Clear all" action

4. **Deep Linking via URL Hash**:
   - Direct URLs like `http://localhost:5173/#KII26101` open the problem detail view directly
   - Browser forward/backward navigation handles history states seamlessly

5. **Print & PDF Export**:
   - Dedicated `@media print` stylesheet formatted to print one clean problem statement card per page
   - Dedicated "Print / Save PDF" action button in detail view

6. **Landing Page Integration**:
   - The original event landing page remains intact and accessible at `/landing.html`
   - The portal header includes a direct navigation link back to the Ideathon Home page
