# AEGIS AGENT PROTOCOL — E-E-A-T CONTENT RULES FOR STELLANTIS DEALERSHIPS
## Version 3.0 | Updated: March 2026 | Applies to: All Stellantis OEM Dealers

---

## SCOPE

This document defines the complete, repeatable ruleset for any AI agent producing E-E-A-T web content, GMB posts, email articles, and CMS landing pages for Stellantis-franchised dealerships (Chrysler, Dodge, Jeep, RAM, FIAT, Alfa Romeo, Maserati). These rules apply regardless of dealer, platform, or content type.

---

## PART 1 — STRUCTURAL CONTENT RULES (ALL FORMATS)

### Rule 1 — NO H1 IN BODY CONTENT
The `<h1>` tag is **never** used in CMS body content blocks. The page title rendered by the CMS theme is the H1. Placing an H1 in body content creates duplicate heading hierarchy and breaks SERP signals on DealerOn, PixelMotion, Dealer.com, and all Stellantis-approved platforms.

**VIOLATION:** `<h1>2026 Jeep Compass in West Virginia</h1>`  
**CORRECT:** `<h2>2026 Jeep Compass in West Virginia</h2>` (or H3 for DealerOn — see Rule 6)

---

### Rule 2 — NO HARDCODED PRICES WITHOUT VIN ATTRIBUTION
Prices may only appear in content when:
1. The VIN is explicitly stated inline (e.g., "VIN: 3C4NJDBN5TT160093")
2. Range language is used instead (e.g., "from the mid-$20s")
3. The price is followed by the standard disclaimer reference (*See dealer for details)

**VIOLATION (GMB/social without VIN):** `2026 Compass Latitude Altitude — $24,844`  
**CORRECT (GMB/social):** `2026 Compass Latitude Altitude — from the mid-$20s* (VIN available, call for details)`  
**CORRECT (article with VIN):** `2026 Compass Latitude Altitude 4x4 (VIN: 3C4NJDBN5TT160093) — $24,844`

---

### Rule 3 — NO SCRIPT TAGS IN CMS BODY CONTENT
Script tags (`<script>`, `<noscript>`) are **never** placed in article body HTML. They belong in:
- Global site `<head>` (via theme admin)
- Footer injection field (via CMS global settings)
- Google Tag Manager container (preferred)

Any script tag in body content on PixelMotion, DealerOn, or Dealer.com will either be stripped by the sanitizer or execute in an isolated context and break page render.

---

### Rule 4 — rtrvr ATTRIBUTES REQUIRED (DealerOn + PixelMotion)
All block-level elements and anchor tags in DealerOn and PixelMotion content must carry retargeting attributes:

**Block elements** (`p`, `h2`, `h3`, `h4`, `ul`, `ol`, `li`, `div`, `article`, `section`):
```html
rtrvr-ls="12~ow,13~lc,15~ow,16~hs,47~lc" rtrvr-ro="42"
```

**Anchor elements** (`a`):
```html
rtrvr-ls="0~hs,3~1,12~lc,13~lc,15~lc,38~lc,39~lc,47~lc" rtrvr-ro="50"
```

Omitting rtrvr attributes causes retargeting audience data loss. The AEGIS transformer auto-injects these when DealerOn or PixelMotion is selected.

---

### Rule 5 — NO JSON-LD IN CMS BODY CONTENT
Structured data (`<script type="application/ld+json">`) is **never** placed in article body content. It belongs in:
- The CMS theme's head injection field
- A dedicated schema widget (DealerOn Schema Block)
- The page's SEO settings panel

JSON-LD in body content on DealerOn causes the CMS to render it as visible text.

---

### Rule 6 — DealerOn H2 FLOAT BUG — MANDATORY FIX
On DealerOn specifically, `<h2>` tags inside content blocks acquire `position:fixed` behavior during scroll — they lock to the viewport and follow the user down the page. This is a known DealerOn rendering engine bug present in all versions through 2026.

**FIX:** Convert all `<h2>` → `<h3>` for DealerOn content.  
The AEGIS CMS Output transformer performs this conversion automatically when DealerOn is selected.

---

### Rule 7 — ALWAYS VALIDATE COMPETITOR DATA
All competitor claims (pricing comparisons, feature comparisons) must be validated against the most recent ShadowForge CSV before publication. Never compare to a competitor's claimed price without a source timestamp.

---

## PART 2 — E-E-A-T AUTHORSHIP REQUIREMENTS

Every article must include:

1. **Identified Author** — Full name, title, and years of experience
2. **Author's Direct Phone** — `tel:` linked, formatted as (XXX) XXX-XXXX
3. **Dealer Name + Address** — Full street address, city, state, ZIP
4. **Publication Context** — "As of [month/year]" or "at time of writing"
5. **Staff Corroboration** — At least one other named staff member cited (e.g., service director, finance manager)
6. **Local Geography** — Minimum 3 named local roads, towns, or regional landmarks
7. **Inventory Specificity** — Minimum 1 VIN-level price point OR verified inventory count with date qualifier

### Author Byline Format (Required)
```html
<p rtrvr-ls="12~ow,13~lc,15~ow,16~hs,47~lc" rtrvr-ro="42" 
   style="font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#b5001e;">
  BY [FULL NAME] &nbsp;|&nbsp; [TITLE] &nbsp;|&nbsp; [DEALER NAME] &nbsp;|&nbsp; [X]+ YEARS SERVING [REGION]
</p>
```

---

## PART 3 — INCENTIVE & PRICING COMPLIANCE (STELLANTIS OEM STANDARD)

### 3.1 — Evergreen Incentive Language (Preferred)
Always use rolling-calendar language instead of hard expiration dates in long-form content:

**AVOID:**
> "The March 31st deadline on the Stellantis incentives is real..."

**USE:**
> "Stellantis incentive programs on the Compass run on a rolling monthly calendar — verify current offer codes with our team before your visit, as these programs reset and change monthly."

### 3.2 — Incentive Code Citation Format
When citing Stellantis offer codes, always pair with disclaimer:
```
$1,000 US Retail Bonus Cash (offer code 26CTA1, subject to program availability — verify with dealer)
```

### 3.3 — Finance/Lease Disclosure Requirements
Every mention of APR or lease payment requires:
- "for qualified buyers" or "for qualified lessees"
- "through [lender name]"
- "subject to credit approval"
- Mileage overage rate for leases ($0.25/mile standard)
- "Tax, title, license extra"

### 3.4 — VIN-Specific vs. General Pricing Rules
| Content Type | VIN Required | Price Format |
|---|---|---|
| Article (long-form) | YES — inline | Exact $ with VIN cited |
| GMB Post | NO (VIN not visible) | Range language only |
| Social Media | NO | Range language only |
| Inventory VLP | YES (system-generated) | Exact $ acceptable |
| Email Subject Line | NO | Range language only |
| SMS/Text | NO | Range language only |

---

## PART 4 — STELLANTIS STANDARD DISCLAIMER BLOCK

The following disclaimer must appear at the bottom of every published article. It is the OEM-approved universal disclosure for Stellantis dealership content:

```html
<!-- STELLANTIS OEM COMPLIANCE DISCLAIMER — DO NOT REMOVE -->
<div rtrvr-ls="12~ow,13~lc,15~ow,16~hs,47~lc" rtrvr-ro="42" 
     style="background:#f0f0f0;border-top:2px solid #b5001e;padding:16px 20px;
            margin:20px 0 0 0;font-family:Arial,sans-serif;font-size:11px;
            color:#555;line-height:1.6;">
  <p rtrvr-ls="12~ow,13~lc,15~ow,16~hs,47~lc" rtrvr-ro="42" 
     style="margin:0 0 6px 0;font-weight:700;text-transform:uppercase;
            letter-spacing:0.05em;color:#333;">
    Stellantis Incentive & Pricing Compliance Disclosure
  </p>
  <p rtrvr-ls="12~ow,13~lc,15~ow,16~hs,47~lc" rtrvr-ro="42" style="margin:0;">
    All advertised prices apply to specific in-stock VINs identified herein and include 
    all applicable manufacturer and dealer incentives in effect at time of publication. 
    Prices and incentive programs are subject to change or expiration without notice. 
    Stellantis factory incentive programs (Bonus Cash, APR offers, Lease programs) operate 
    on a rolling monthly calendar and may be modified, extended, or discontinued by 
    Stellantis at any time. Finance and lease offers require credit approval through 
    Stellantis Financial Services or an approved lender; not all buyers will qualify. 
    Lease offers based on MSRP of specific VIN; acquisition fee, tax, title, license, 
    and registration not included; $0.25/mile charge applies above contracted annual 
    mileage. Dealer Assistance amounts vary by vehicle and cannot be combined with all 
    offers. EPA fuel economy estimates for comparison purposes; actual mileage varies 
    with conditions, driving habits, and vehicle load. Inventory subject to prior sale. 
    All specifications cited from Stellantis media publications and subject to change. 
    [DEALER NAME] is an authorized Stellantis retailer. This content was authored by 
    dealership personnel and represents the experience and opinion of [DEALER NAME] staff; 
    it is not an official Stellantis communication.
  </p>
</div>
<!-- END STELLANTIS COMPLIANCE DISCLAIMER -->
```

---

## PART 5 — FAQ SECTION REQUIREMENTS

Every E-E-A-T article must include a FAQ section with minimum 4 questions. FAQ rules:

1. Questions must reflect **real customer queries** (search-intent driven)
2. Answers must be **specific to this dealer** — not generic brand answers
3. At least one FAQ answer must include a **direct phone number** (`tel:` linked)
4. At least one FAQ must address **a known limitation** of the vehicle honestly
5. Questions use `<p>` with `font-weight:700` styling — never `<h4>` or `<dt>`

---

## PART 6 — INVENTORY COUNT PROTOCOL

When citing inventory counts in articles or GMB posts:

```html
<!-- REQUIRED FORMAT: -->
we have <strong>[N] [Model] models in stock as of this writing 
(inventory updates daily — verify live count at 
<a href="[VLP URL]" [rtrvr attrs]>[dealer domain]</a>)</strong>
```

**Never cite a raw inventory number without:**
- "as of this writing" qualifier
- A live VLP link for verification
- Date of last ShadowForge CSV sync noted in article metadata

---

## PART 7 — GMB POST COMPLIANCE RULES

1. **Max 1,500 characters** for "What's New" post type
2. **No hardcoded prices** without visible VIN — use range language
3. **Stellantis incentive codes** must be paired with "verify with dealer" language
4. **No people in images** — FTC/Google Business Profile policy
5. **No dealer logos in images** — Google policy for automotive
6. **No license plates in images** — privacy compliance
7. **CTA button** must route to phone call ("Call Now") or verified VLP URL
8. **Disclaimer** must appear at end of post text (abbreviated Stellantis standard)

---

## PART 8 — COMPLIANCE RISK MATRIX

| Issue | Risk Level | Type | Auto-Fixed by AEGIS |
|---|---|---|---|
| `<script>` in body content | 🔴 BLOCKING | CMS/Technical | ✅ Yes |
| `<h1>` in body content | 🔴 BLOCKING | SEO/Structure | ✅ Yes (strips) |
| JSON-LD in body | 🔴 BLOCKING | Technical | ✅ Yes (strips) |
| Hardcoded price without VIN (GMB) | 🔴 LEGAL | Stellantis FTC | ❌ Manual fix |
| Hard expiration date in long content | 🟠 COMPLIANCE | Stellantis | ❌ Manual fix |
| Missing disclaimer block | 🟠 COMPLIANCE | Stellantis OEM | ⚠️ Validated |
| Missing rtrvr attributes | 🟡 DATA LOSS | Retargeting | ✅ Yes (injects) |
| DealerOn H2 float | 🟡 UX | CMS Render Bug | ✅ Yes (H2→H3) |
| Missing author byline | 🟡 E-E-A-T | Google Quality | ⚠️ Validated |
| Inventory count without date qualifier | 🟡 CREDIBILITY | Brand | ❌ Manual fix |
| Missing FAQ section | 🟡 E-E-A-T | Google Quality | ⚠️ Validated |
| Missing staff corroboration | 🟡 E-E-A-T | Google Quality | ⚠️ Validated |

---

## PART 9 — PROVIDER-SPECIFIC RULES QUICK REFERENCE

| Provider | H1 | H2 | Script | Tables | rtrvr | JSON-LD in Body |
|---|---|---|---|---|---|---|
| DealerOn | ❌ | ⚠️→H3 | ❌ | ❌ | ✅ Required | ❌ |
| PixelMotion | ❌ | ✅ | ❌ | ✅ | ✅ Required | ❌ |
| Dealer.com | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| CDK Global | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ OK |
| Dealer Inspire | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| DealerSocket | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ OK |
| Sincro | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| TeamVelocity | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Roadster | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## PART 10 — READY-TO-PUBLISH CHECKLIST

Before any Stellantis dealership article publishes, confirm:

- [ ] No `<script>` tags in body HTML
- [ ] No `<h1>` tags anywhere in body HTML
- [ ] No JSON-LD in body content (head injection only)
- [ ] DealerOn: All H2 converted to H3
- [ ] rtrvr attributes on all block elements (if DealerOn/PixelMotion)
- [ ] rtrvr attributes on all anchor elements (if DealerOn/PixelMotion)
- [ ] All prices either VIN-attributed OR in range language
- [ ] Incentive expiration language is evergreen (rolling calendar) OR publication date noted
- [ ] Author byline present with full name, title, phone
- [ ] Minimum 2 named staff members cited
- [ ] Minimum 3 local geographic references
- [ ] FAQ section with minimum 4 questions
- [ ] At least 1 VIN-level price OR verified inventory count with date qualifier
- [ ] All phone numbers as `tel:` links with rtrvr attributes
- [ ] Stellantis Standard Disclaimer block present at article bottom
- [ ] GMB post uses range language (no hardcoded prices without VIN)
- [ ] GMB disclaimer includes "VIN available, call for details"
- [ ] Inventory count includes "as of this writing" qualifier + VLP link
- [ ] Image: no people, no dealer logos, no license plates

---

## PART 11 — SHADOWFORGE INTEGRATION RULES

When using ShadowForge v2 data as article source:

1. Always note the CSV extraction date in article metadata comments
2. Cross-reference inventory count against live VLP before citing in article
3. VIN prices from CSV are valid for 72 hours — regenerate if older
4. Lead score "deep_discount" (>20% off MSRP) = safe to cite as strong value
5. Lead score "hot_deal" (15-20% off) = cite as competitive pricing
6. Urgency_Flag = TRUE in CSV → use rolling-calendar language, not hard date

### ShadowForge Bridge CLI
```bash
# Convert any JSON inventory to canonical CSV
python shadowforge_bridge.py -i inventory.json -o csv_inputs/out.csv -d "Dealer Name"

# Supported input formats (auto-detected):
# TYPESENSE_RESPONSE, ALGOLIA_RESPONSE, PIXELMOTION_VLP,
# STANDARD_VEHICLE, JSONLD_SCHEMA, WORDPRESS_ACF, SHADOWFORGE_CANONICAL
```

---

*This document is maintained in the AEGIS Intelligent HTML Viewer repository.*  
*Repository: Sovara-Forever/aegis-intelligent-html-viewer*  
*Last updated: March 2026*