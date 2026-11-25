# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Corporate website for LOYDL Unternehmensberatung showcasing three service areas:
- IT Consulting & Training (Business Analysis, Domain Modelling, IT Architecture)
- Business Process Automation (Camunda BPM, Workflow Automation)
- AI Communication Solutions (fluxdeck.io KI-Telefonie Platform)

**Key Characteristic**: Zero-build-step static site. No npm, webpack, or build tooling required.

## Tech Stack

- **Frontend**: Plain HTML5 with TailwindCSS loaded via CDN (`https://cdn.tailwindcss.com`)
- **JavaScript**: Vanilla JS only (no framework, no bundler)
- **Deployment**: Vercel (consistent with fluxdeck.io)
- **Forms**: Formspree for contact form
- **Language**: German (UI and content)

## Local Development

No build step needed. Simply open HTML files directly or use a local server:

```bash
# Option 1: Open directly
open index.html

# Option 2: Python simple server (recommended for testing)
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## Deployment

- **Vercel-Projekt:** `loydl-website` im Team `haraldloydlloydlchs-projects`, verbunden mit `github.com/hloydl/loydl-website` (seit 25.11.2026).
- **Jeder Push nach `main`** löst ein Production-Deployment aus.
- **Vorschau:** https://loydl-website-haraldloydlloydlchs-projects.vercel.app — nur mit Vercel-Login sichtbar (Deployment Protection).
- **Kein öffentlicher `.vercel.app`-Alias:** `loydl-website.vercel.app` wurde am 25.11.2026 aus dem Projekt entfernt, weil die Vercel-Protection diese Domain nicht schützt. Nicht wieder hinzufügen.
- **loydl.ch** zeigt noch auf die WordPress-Site bei Hostpoint. Umstellung = Domain in Vercel eintragen + DNS bei Hostpoint ändern.
- Framework Preset: Other, kein Build Command.

## Architecture & Page Structure

Sieben Seiten mit gemeinsamer Navigation:

1. **index.html** - Homepage with hero, services overview cards, and CTA buttons
2. **services.html** - Detailed descriptions of all three service areas
3. **ai-solutions.html** - Deep dive into fluxdeck.io platform
4. **about.html** - Über mich (Profil Harald Loydl)
5. **contact.html** - Contact form and company info
6. **impressum.html** - Impressum (Schweizer Recht, UID CHE-110.533.965)
7. **datenschutz.html** - Datenschutzerklärung (Vercel, Formspree)

### Navigation Pattern
- Fixed top navigation bar (`fixed top-0 ... z-50`)
- Desktop-Links in `hidden md:flex`, Burger-Button `#menu-button` + `#mobile-menu` unter `md`, Inline-Script im `<nav>`
- Der `<nav>`-Block ist auf allen 7 Seiten identisch, nur der aktive Link unterscheidet sich (`text-purple-600 font-semibold` + `aria-current="page"`). Änderungen an der Navigation immer in allen 7 Dateien.
- Reihenfolge: Home · Services · AI Solutions · Über mich · Kontakt (CTA `bg-purple-600`)
- Überschriften auf 375 px Breite prüfen: lange deutsche Wörter (`Unternehmensberatung`, `Datenschutzerklärung`) laufen bei `text-4xl` und größer über den Rand.

### Styling Conventions

**Brand Colors** (defined in README, used throughout):
- Primary gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Purple-600: `#9333ea` (CTAs, active states)
- Background: `bg-gray-50`

**Custom CSS Classes**:
- `.gradient-bg` - Purple gradient for hero sections
- `.feature-card` - Service cards with hover transform effect

**TailwindCSS via CDN**: All styles use Tailwind utility classes. No custom CSS files.

## Contact Form Configuration

The contact form in [contact.html](contact.html) uses Formspree, form ID `xwprrgjl`.

## Important Relationships

- **fluxdeck.io**: External platform (https://www.fluxdeck.io) - LOYDL's AI telephony product
- Links to fluxdeck.io appear in navigation and throughout AI Solutions page
- Both sites deployed on Vercel for consistency

## Assets Structure

```
assets/
├── images/     # Logos, photos, graphics (currently empty)
└── videos/     # Optional video content (currently empty)
```

Note: Asset directories are preserved via `.gitkeep` but currently contain no files.

## Outstanding TODOs

Stand 25.11.2026:
- Add company logo to assets/images/
- Add favicon
- `datenschutz.html` erwähnt `cdn.tailwindcss.com` nicht (IP-Übermittlung an Dritte)
- Tailwind Play-CDN ist laut Tailwind nicht für Produktion gedacht (Konsolen-Warnung)
- Livegang: Domain `loydl.ch` von Hostpoint/WordPress auf Vercel umstellen

## Development Notes

- **No build process**: Edit HTML files directly, changes are immediate
- **No package.json**: TailwindCSS loaded from CDN, no dependencies
- **No transpilation**: Use vanilla ES6 JavaScript that works in modern browsers
- **Mobile-first**: All layouts use responsive Tailwind classes (sm:, md:, lg:)
- **German language**: All content and UI text in German
