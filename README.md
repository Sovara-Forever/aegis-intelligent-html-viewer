# AEGIS — Intelligent HTML Viewer & CMS Content System
## RC Auto Group | Stellantis Dealership Content Platform

**Live App:** Deployed via GitHub Pages  
**Repository:** Sovara-Forever/aegis-intelligent-html-viewer  
**Version:** 3.0 | March 2026

---

## What This Repository Contains

### `/` — Production App (React + Vite)
The AEGIS CMS Landing Page System — a React+Vite single-page application for:
- HTML paste + WYSIWYG side-by-side preview
- Provider-specific CMS transforms (25 providers)
- One-click copy: CMS HTML | Meta Tags | JSON-LD | Instructions | API Recon
- E-E-A-T validation scoring
- Full API Skill.md reference (IF/ELSE recon matrix, 14 format variants)

### `/content/rc-auto-group/` — RC Auto Group Content
- `eeat_article_superior_2026_compass_wv.html` — Production-ready E-E-A-T article (all 5 editorial fixes applied)
- `gmb_post_superior_2026_compass.txt` — GMB companion post (Stellantis-compliant pricing)
- `rc_auto_new_inventory.json` — Verified inventory data (106 vehicles, March 2026)
- `rc_auto_specials.json` — Current incentive programs
- `rc_auto_staff.json` — Staff directory
- `compass_trailhawk_wv.png` — Compliance-approved vehicle image

### `/docs/` — Agent Documentation
- `AGENT_RULES.md` — Complete repeatable E-E-A-T ruleset for all Stellantis dealers
- `shadowforge_bridge.py` — JSON→CSV converter for ShadowForge v2 pipeline

---

## Editorial Fix Log — March 27, 2026

| # | Issue | Risk | Fix Applied |
|---|---|---|---|
| 1 | `<script>` tag in body | 🔴 BLOCKING | Removed entirely |
| 2 | Inventory count without date qualifier | 🟡 CREDIBILITY | Added "as of this writing" + live VLP link |
| 3 | 31-word H2 diluting keyword density | 🟡 SEO | Tightened to keyword-forward version |
| 4 | Hard March 31st expiration date | 🟠 COMPLIANCE | Replaced with rolling-calendar language (Option B) |
| 5 | GMB hardcoded prices without VIN | 🔴 LEGAL | Replaced with range language + VIN routing |

---

## Quick Start — Running the App Locally

```bash
cd aegis-app
npm install
npm run dev
# Opens at http://localhost:5173
```

## Quick Start — ShadowForge Bridge

```bash
python docs/shadowforge_bridge.py -i inventory.json -o output.csv -d "RC Auto Group"
```

---

## Supported CMS Providers (25)

AutoWeb | AutoRevo | CDK Global | Dealer.com | Dealer eProcess | Dealer Essential | Dealer Inspire | Dealer Spike | Dealer Teamwork | DealerFire | DealerMasters (Team MXS) | DealerOn | DealerSocket | DealerX | Dominion Dealer Solutions | Jazel Auto | Motive | Overfuel | Reynolds & Reynolds | Roadster | Shopify | Sincro | Sokal | TeamVelocity | PixelMotion | Other

---

## Compliance

All content follows Stellantis OEM dealer content standards. See `docs/AGENT_RULES.md` for the complete compliance framework.