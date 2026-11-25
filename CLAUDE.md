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

**Vercel CLI**:
```bash
vercel --prod
```

**Vercel UI**: Push to GitHub, import at vercel.com/new
- Framework Preset: Other
- Build Command: (leave empty)
- Output Directory: `.` or (leave empty)

**Custom Domain**: loydl.ch (configured in Vercel dashboard)

## Architecture & Page Structure

Four main pages with shared navigation:

1. **index.html** - Homepage with hero, services overview cards, and CTA buttons
2. **services.html** - Detailed descriptions of all three service areas
3. **ai-solutions.html** - Deep dive into fluxdeck.io platform
4. **contact.html** - Contact form and company info

### Navigation Pattern
- Fixed top navigation bar (`fixed top-0 ... z-50`)
- Responsive: Hidden mobile menu on small screens (`hidden md:flex`)
- Active page indicated with `text-purple-600 font-semibold`
- CTA button styled with `bg-purple-600`

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

The contact form in [contact.html](contact.html) uses Formspree and requires a form ID:

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

To update:
1. Sign up at formspree.io
2. Create new form
3. Replace `YOUR_FORM_ID` in contact.html with actual ID

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

Note: Asset directories are preserved via .gitignore but currently contain no files.

## Outstanding TODOs

From README.md:
- Add real Formspree form ID to contact.html
- Create impressum.html (legal notice - required for German sites)
- Create datenschutz.html (privacy policy - GDPR requirement)
- Add company logo to assets/images/
- Add favicon

## Development Notes

- **No build process**: Edit HTML files directly, changes are immediate
- **No package.json**: TailwindCSS loaded from CDN, no dependencies
- **No transpilation**: Use vanilla ES6 JavaScript that works in modern browsers
- **Mobile-first**: All layouts use responsive Tailwind classes (sm:, md:, lg:)
- **German language**: All content and UI text in German
