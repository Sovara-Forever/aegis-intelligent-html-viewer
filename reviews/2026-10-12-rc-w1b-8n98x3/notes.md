# Review notes: RC W1b (sha ca305a43…61fdc1)

Copied unchanged from the Gate and Epsilon cards.

---
# Nicky Gate: RC style fix pre-paste (2026-10-08)
# Gate: RC style-fix pre-paste, 2026-10-08

Verdict: PASS (Nicky, Gate)

- W1a paste b23e075dd4a19eca0ea1e2b0642b4caaf9f685efa51424e6ae618c4a1d5f2c71 (was 0a7b6d11). The diff vs .pre-rcstyle is styles only: overflow-x:auto to overflow:auto (2), and list-style:none to list-style-type:none (1).
- W1b paste ca305a430eaec07ba5745bf6ec9c3b8c5fd44580263ddd59b3552ee82c61fdc1 (was d0013892). Styles only: overflow (1) and list-style-type (1).
- Both files: 0 non-ASCII, 0 comments.
- SHA256SUMS-weekley-rc-rcstyle-2026-10-08.txt (1af1b34a...) checks 28/28 OK and differs from personfix only on these 2 rows.
- After re-paste: live re-check confirms overflow:auto survives and the page fits a 390px phone width.

## Live re-check after re-paste (7:39 AM ET): PASS
- Live fetch: overflow:auto on both table wrappers, 0 overflow-x, and list-style-type:none survived.
- 1 H1, clean canonical (no query string), 0 mojibake.
- Matches Ruby (rc-w1a-rcstyle-live-check c40ccc76...) and Epsilon (73/80, 390px with no page overflow).

---
# Epsilon: RC style patch co-sign (2026-10-08)
# Epsilon pre-paste co-sign: RC Newell W1a + W1b STYLE PATCH, 2026-10-08

Requested by Ruby at 07:28 ET; audited 07:29–07:36 ET, 10/8. Read-only: hashes, diffs, a local WordPress kses/wpautop simulation, a local headless render, and curl GET on public pages. No CMS, no browser driving, no messages.
Nicky's card (`/workspace/nicky/output/gate-rc-w1a-live-2026-10-08.md`) was treated as a claim and re-run.

```
LABEL: STYLE PATCH (CSS only; 0 words, 0 links, 0 dates, 0 schema changed)
RC W1a   OUTCOME: Swallow  OVERALL: 73/80 (91.3%)  CO-SIGNED paste SHA b23e075dd4a19eca0ea1e2b0642b4caaf9f685efa51424e6ae618c4a1d5f2c71
RC W1b   OUTCOME: Swallow  OVERALL: 73/80 (91.3%)  CO-SIGNED paste SHA ca305a430eaec07ba5745bf6ec9c3b8c5fd44580263ddd59b3552ee82c61fdc1
Unexpected diffs: 0 / 0.   Automatic F: none.   Push rule: met for both.
```

## 1. Hashes [Confirmed]

| File | SHA-256 | Expected |
|---|---|---|
| `/workspace/tmp/blogw1/w1a-…upper-ohio-valley.paste.html.pre-rcstyle` | `0a7b6d11…a84ba39d` | the co-signed W1a ✔ |
| `/workspace/tmp/blogw1/w1b-…weirton-steubenville.paste.html.pre-rcstyle` | `d0013892…7e2443c91` | the co-signed W1b ✔ |
| `rc/w1a-jeep-wrangler-sahara-vs-rubicon-upper-ohio-valley.paste.html` | `b23e075d…5f2c71` | b23e075d ✔ |
| `rc/w1b-jeep-grand-cherokee-vs-grand-cherokee-l-weirton-steubenville.paste.html` | `ca305a43…61fdc1` | ca305a43 ✔ |

- The new list `SHA256SUMS-weekley-rc-rcstyle-2026-10-08.txt` (sha `1af1b34a…`) passes `sha256sum -c` 28/28 OK.
- Diffed against the personfix list, exactly 2 lines change: line 14 (RC W1a paste) and line 19 (RC W1b paste). Nothing else in the list moved. Weekley W1a `81dc51b4`, Weekley W1b `7bd8e74e`, the RC md/sources/gmb/jsonld files and `_build/*` are all unchanged.
- Against the personfix list, only those 2 RC pastes fail, which is expected.

## 2. Diff pre → new [Confirmed]

**W1a** (23,736 → 23,737 B, 50 lines both): lines 5, 16 and 21 change.
- L5, the "In this guide" `<ul>`: `list-style:none` → `list-style-type:none`.
- L16 and L21, the 2 table wrappers: `overflow-x:auto` → `overflow:auto`.

**W1b** (21,428 →21,431 B, 51 lines both): lines 5 and 9 change.
- L5, the TOC `<ul>`: `list-style:none` → `list-style-type:none`.
- L9, the 1 table wrapper: `overflow-x:auto` → `overflow:auto`.

**Proof the swaps are the only change:**
- Applying the two string swaps to the pre file reproduces the new file byte for byte (sha b23e075d / ca305a43).
- Reversing them reproduces the pre file byte for byte.
- So there are 0 text, link, schema, date or attribute changes beyond the 3 and 2 property swaps. Unexpected diffs = 0, which meets the date-patch logic.

## 3. Survival through RC's sanitizer + mobile render

**Model used:**
- WordPress **7.0.7** core, the version in the live RC generator meta. Downloaded from wordpress.org, wp-includes only.
- Run on php 8.4: `wp_kses_post()` on save, then `wptexturize` + `wpautop` on display.
- Harness and outputs are in `/tmp/eps-rcstyle-1008/`.

**The model is validated against the live site:**
- Running it on the **old** W1a paste reproduces Nicky's live block (`live.html`, sha `7329cfc7…`) byte for byte.
- The only exception is WordPress's display-time `decoding="async"` placement on the 2 staff images, which comes from `wp_filter_content_tags` and isn't simulated. The net live result equals the source.
- The model strips `overflow-x:auto` ×2 and `list-style:none` ×1 exactly as live did, and drops the trailing `;` in style attributes. [Confirmed]

| Run | Survive kses | Declarations lost |
|---|---|---|
| W1a new | `overflow:auto` ×2 and `list-style-type:none` ×1 present after kses+autop | **0** of 179 style attrs |
| W1b new | `overflow:auto` ×1 and `list-style-type:none` ×1 present | **0** of 147 style attrs |

Both properties are on the WP 7.x `safe_style_css` allowlist (kses.php: `overflow`, `list-style-type`). The `list-style` shorthand sits only in `$css_url_data_types`. [Confirmed]

**Headless render:**
- Playwright Chromium, 390×844, isMobile, DPR 2.
- Uses the live RC W1a page template (theme CSS and JS loaded from gorcauto.com), with the post body swapped for the simulated live output.
- W1b has no live page yet, so it was rendered in the same RC post template. [Assumption - Check: W1b will use the same template]

| Render | Document width | Table wrappers (overflow-x / client / scroll) |
|---|---|---|
| W1a old | **535 px** (page overflows; matches Nicky) | no overflow property (stripped) |
| W1a new | **390 px** | auto / 360 / 520, ×2: wrappers scroll, the page does not |
| W1b old | **535 px** | stripped |
| W1b new | **390 px** | auto / 360 / 520, ×1 |

- In the new renders, the TOC list-style-type computes to `none` in all of them.
- Screenshots: `/tmp/eps-rcstyle-1008/w1a-new-390.png` (the table is clipped inside its box at the right edge, so it scrolls) and `w1a-pre-390.png`.
- Note: `overflow:auto` also sets overflow-y:auto. The wrappers have no fixed height, so there's no vertical clipping or second scrollbar; the render shows the full table height.

## 4. Other stripped shorthands [Confirmed]

Both new files have 0 `overflow-x`, 0 `overflow-y` and 0 `list-style:` shorthand.

The properties used (28, the same set in both) are all on the allowlist, and kses removed nothing from either file: background, background-color, border, border-bottom, border-collapse, border-left, border-radius, color, display, font-size, font-style, font-weight, height, line-height, list-style-type, margin(-bottom/-right/-top), min-width, object-fit, overflow, padding(-bottom), text-align, text-decoration, vertical-align, width.

## 5. Live state and re-score

**RC W1a, post 37758, IS live with the old styles.** [Confirmed]
- Curl at 07:35:09 ET returns 200, sha `7329cfc7…`, identical to Nicky's 07:25 fetch.
- article:modified_time is 11:23:24Z (7:23:24 AM ET).
- Our 2 wrappers render as `<div style="margin:0 0 20px 0">` with overflow removed.
- The single `overflow-x` on the page is theme navbar CSS, not our block.

**RC W1b is not live.** Its /2026/10/12/ slug and `?name=` both redirect to the homepage. Publish is set for 10/12.

**Re-score.** The visible text is byte-identical, so 7 of the 8 dimensions carry over from the 10/7 co-sign (Acc 9, Comp 9, Coh 9, Aud 10, Act 9, Ins 9, Prec 9 = 64). Only Presentation was re-scored, for mobile:

| | Presentation | Total |
|---|---|---|
| RC W1a **live now** (old styles) | **7**: at 390px the page is 535 wide and the Rubicon column is cut off | 71/80 (interim; still ≥68, but a known defect) |
| RC W1a **new paste b23e075d** | **9**: tables scroll inside the wrapper; page 390 | **73/80**, Δ 0 vs co-sign, +2 vs live now |
| RC W1b **new paste ca305a43** | **9** | **73/80**, Δ 0 vs co-sign |

Presentation was 9 at the 10/7 co-sign on the assumption that `overflow-x` would survive. The patch makes that assumption true on RC. Not a 10: the tables still need a sideways scroll on phones, which is acceptable but not ideal.

## 6. Label and write-off

**STYLE PATCH.** Words, links, dates and schema are unchanged. RC still has no body JSON-LD (`rc/w1a…jsonld.html` `a4c6f959` stays held for Val's duplicate-@id fix, as before).

**Write-off coverage:**
- The verbatim source (`wiki/rules/sean-approval-2026-10-07-batched-list.md`, item 2: "Ruby pastes blogs into Pixel Motion and DealerOn without a separate write-off for each post. Each paste has to pass Gate first, Epsilon co-signs, and Ruby checks the live page after"; Sean "yes…" ~5:33 AM 10/7) and `candidate-rules.md` l.36–41 cover **blog pastes** with those 3 conditions.
- Neither text mentions re-pastes or edits to an already-live post. [Gap Identified]
- My reading: a re-paste of the same post, same words, styles only, is still "a paste" and falls under item 2 if Gate passes, this co-sign holds, and Ruby runs a live check. So no new write-off is needed. [Assumption - Check]
- [Bias]: Sean's "yes" names no item numbers; the family read it as items 1–4 (file note l.45). If Sean wants re-pastes of live posts handled separately, that's his call.

## Blockers

**None** for the co-sign.

## Conditions and notes for Ruby

1. **Re-paste W1a into the existing post 37758, code mode, whole file b23e075d.**
   - Do not change the slug, publish date (2026-10-08) or title fields. WordPress will move article:modified_time; that's expected.
   - Then: Gate delta re-check → Epsilon live co-sign → Ruby live check, which must include the 390px mobile width, not only the text.
2. **W1b:** on 10/12, paste `ca305a43` in place of `d0013892`. No other change. Gate needs a delta pass on the new SHA before the paste. This card covers the Epsilon side.
3. **Shared builder (process risk, not a blocker):**
   - The fix was made in `_build/lib.py` (sha `f8f2d331…`; pre copy `0a56d2c3…`). `weekley.py`, `rc.py`, `holman.py`, `genford.py`, `moses.py` and `mchugh.py` all import it.
   - `lib.py` is in no SHA256SUMS list.
   - A rebuild of Weekley would now change Weekley W1b (`7bd8e74e`, co-signed, not live) and the Weekley W1a source (`81dc51b4`, live baseline), and would void their co-signs.
   - Weekley keeps `overflow-x` (Nicky checked live at 7:22), so there's no need to rebuild Weekley. Either don't rebuild, or re-co-sign. Consider adding `lib.py` to the next list.
4. Nicky's card is reproduced in full: strip set, line targets, 535px at 390, safe_style_css. Her "Next" line still says the support@ confirm "waits on Sean's write-off", which is stale wording; see §6.

---
# Epsilon: Week-1 blogs Weekley + RC co-sign (2026-10-07)
# Epsilon pre-paste co-sign: Week-1 Pixel Motion blogs (Weekley W1a/W1b, RC Newell W1a/W1b), 2026-10-07

Seat: Epsilon (auditor). READ-ONLY run, ~6:00-6:10 AM ET Wed 10/7. No CMS, no browser, no messages. Read-only curl only. Surface: `blog`, so it's scored on the protocol v2.5 /80 scale (amendment 2026-09-07 keeps /80 for blog).
Requested by Ruby (10/7, after Nicky's Re-Gate 2 PASS at 5:59 AM ET). Locked list: `SHA256SUMS-weekley-rc-metafix-2026-10-07.txt` (28 lines).

## OUTCOME

```
LIST CO-SIGN: WITHHELD. Weekley W1a and W1b are Gargles (a written entity lock is broken in the body JSON-LD). RC W1a and RC W1b are Swallows and are co-signed one post at a time.

Weekley W1a   OUTCOME: Gargle   OVERALL: 68/80 (85.0%)
Weekley W1b   OUTCOME: Gargle   OVERALL: 68/80 (85.0%)
RC W1a        OUTCOME: Swallow  OVERALL: 73/80 (91.3%)   CO-SIGNED for paste SHA 0a7b6d11...a84ba39d
RC W1b        OUTCOME: Swallow  OVERALL: 73/80 (91.3%)   CO-SIGNED for paste SHA d0013892...7e2443c91
Automatic F: none on any of the 4.
LINK: cards/carsignment-blogs-week1-2026-10-07/epsilon-cosign-week1-blogs-weekley-rc-2026-10-07.md
DOORS FOR SEAN: (1) Weekley blog entity: rebuild to /#dealer (my default) or put a written blog exception on file. (2) Optional: split the paste so RC goes now and Weekley follows after its rebuild + re-Gate.
REWRITE NOTES FOR RUBY: Weekley org_id -> /#dealer; fix the Weekley footer county line; optional wording on W1b's Sahara "(Convenience Group)". Details below.
```

**Line one (amendment 10-05 rule 1, keywords first):** all 4 packs carry keywords [Confirmed]. Each .md has a "Focus keywords" row (5-6 terms, on topic), and the same string is the BlogPosting `keywords` value. Pixel Motion blog posts do have a Meta Keyword field: the live RC 6/9 blog renders `<meta name="keywords" content="jeep wrangler near weirton wv">` [Confirmed]. Paste path: Meta Keyword ← the md "Focus keywords" row. No Automatic F.

---

## Authority check (amendment 10-05 rule 5)
- **Standing write-off: WRITTEN [Confirmed].** It is in `/workspace/ruby-channel/wiki/rules/candidate-rules.md` line 36, section "2026-10-07 — Blog paste standing write-off (APPROVED by Sean 2026-10-07, 5:33 AM ET, "yes" to Sarean's batched list item 2)". File mtime 05:34 ET. Terms: Gate first, then Epsilon co-sign, then Ruby's character-by-character live check, then a proof row. Holman and GenFord stay with Sean.
- **Whose words:** the rule text is **Ruby's record (paraphrase), not Sean's verbatim.** Sean's verbatim is only "yes" to item 2 of a batched list. The original wording of that list item is not saved anywhere on the box [Assumption - Check]. It attributes Sean, with a date and time, so it meets rule 5. It also changes no SCORECARD lock, so the stricter half of rule 5 doesn't apply.
- Optional for Sean: one line confirming the paraphrase matches what he said yes to would close the provenance caveat. This does not block anything.

## Inputs read
- Canon: `wiki/auditor/response-audit-protocol-v2.5.md`, plus amendments 2026-09-07, 2026-09-14 (entity lock) and 2026-10-05.
- Skill `audit-ruby-write-up-pass-through`, plus the format and Meta-field rules from `phase-1-blog-alchemist` and `pixel-motion-custom-html-page`.
- Gate card `/workspace/nicky/output/gate-week1-blogs-weekley-rc-2026-10-07.md` (first pass, Re-Gate 1, Re-Gate 2).
- INDEX.md, the drive-time proof .md, all 3 Maps PNGs (opened as images), and all 20 post files.
- Live curls (06:01 ET): Weekley homepage, live Weekley 4310, RC homepage. Gate's saved live pulls: Weekley Gladiator 6/3, RC 6/9, RC 3/11.

---

## Per-check evidence (all 4)

### 1. Hashes and hygiene [Confirmed]
- I ran `sha256sum -c SHA256SUMS-weekley-rc-metafix-2026-10-07.txt` from `cards/carsignment-blogs-week1-2026-10-07/`: **28/28 OK** (06:0x ET).
- All 4 paste SHAs equal Ruby's stated values and Nicky's Re-Gate 2 table:
  - Weekley W1a `2790b9fe...4bb05b`
  - Weekley W1b `378806c6...38dd31`
  - RC W1a `0a7b6d11...a84ba39d`
  - RC W1b `d0013892...7e2443c91`
- In the 4 paste files:
  - 0 non-ASCII bytes and 0 mojibake. Apostrophes and dashes are HTML entities.
  - 0 HTML comments.
  - 0 unfilled tokens: `{{ }}`, `[TOKEN]`, TODO, XXX, lorem, [VERIFY] and `RC_DRIVE_*` all return 0.
  - 0 internal-voice words. Grep for gate, epsilon, ruby, nicky, swallow, gargle, gag, lick, sarean, grok, draft, verify, internal, write-off and osrm returns 0 in the pastes and GMB files.

### 2. Meta [Confirmed]
| Post | Title tag | Meta desc | Keywords | H1 = headline = WebPage name |
|---|---|---|---|---|
| Weekley W1a | 49 | 135 | 6 terms, GC trims | yes (71) |
| Weekley W1b | **53** | 127 | 6 terms, Wrangler | yes (96) |
| RC W1a | 45 | **128** ✔ | 5 terms, Sahara vs Rubicon (no "jeep wrangler trims") | yes (104) |
| RC W1b | 44 | 130 | 5 terms, GC vs GC L | yes (97) |

RC W1a meta = 128 chars, and it is identical in the md and in the BlogPosting `description`. Metas run 127-135, which is under the factory skill's 150-160 guideline but within the ≤155 rule Gate applied. That is a style note only, not a deduction.

### 3. Facts
- **Specs [Confirmed by spot-check against Gate's saved Stellantis PDFs].** I checked these against 27221 and 27222 myself:
  - Sahara heated front seats, heated wheel and remote start are all "S".
  - Sport has 17x7.5 steel wheels, and 245/75R17 all-season is standard on Sport/Sport S.
  - Rubicon has LT285/70R17 BFG KO2.
  - Willys "33-inch mud-terrain" and rock rails are listed.
  - The Rubicon "33-inch" wording matches Stellantis's own wording for the same 285/70R17 size.
- All other spec numbers are [Confirmed per Gate first pass], with sources opened 10/7.
- **No invention.** There are no prices except the 2027 MSRP pair ($41,515 entry, $57,895 Overland incl. $1,995 destination), which is sourced to PR Newswire 8/12/2026 and labeled "national figures ... not Weekley pricing". There are no VINs, no awards and no aggregateRating/stars in any graph. Lot lines are dated 10/7 and use threshold ("models") language [Confirmed].
- **Drive times match the PNGs [Confirmed, opened all 3].**
  - Weirton→845 Washington St: "via WV-2 N, 22 min, 16.4 miles". Copy: "about 22 minutes from Weirton up WV-2 North".
  - Steubenville: "via WV-2 N, 35 min, 21.9 miles". Copy: "about 35 minutes ... via WV-2 North".
  - Pittsburgh: "via I-376 W and US-30 W, 55 min, 41.9 miles"; the runner-up is US-22 W at 59 min. Copy: "under an hour ... via I-376 West and US-30 West".
  - The copy is identical in the RC W1a and W1b bodies, and the RC W1b GMB has the Weirton line.
  - PNG mtimes are 05:54 ET. The screenshots show no clock, so that time comes from the file mtime [Confirmed by mtime].
- **Weekley drive copy.** "From Mansfield that's about 23 minutes ... from Mount Vernon about 25" is word for word from **live 4310** [Confirmed by curl 06:01]. I-71 Exit 165 (SR-97) at Bellville is [Confirmed by Gate]. It is not on 4310 but is consistent with the I-71 exit listing.
- **NAP [Confirmed].**
  - Weekley: 50 Main St, Butler, OH 44822, (567) 430-2908, name "Weekley Chrysler Dodge Jeep Co". All three match live 4310 (text plus the `/#dealer` node).
  - RC: 845 Washington St, Newell, WV 26050, (304) 714-2632. Matches the RC homepage.
- **[Gap Identified] Weekley footer geography (both Weekley pastes).**
  - Text: "Serving Butler, Mansfield, Mount Vernon, Ashland and Loudonville **across Richland and Knox counties**."
  - Ashland and Loudonville are in Ashland County, not Richland or Knox.
  - Location: W1a paste line 59, W1b paste line 48. Source: `_build/dealers.py` line 7 (WEEKLEY `geo`).
  - The live 7/29 Weekley blog says "Butler, OH, Mansfield, Ashland, Mount Vernon, and the broader Richland and Knox County area"; the new line drops "broader" and adds Loudonville. It's minor, but it's a false statement on a client page.
- **[Assumption - Check] soft voice claims** (dealer voice, no deduction beyond Accuracy -1 on RC):
  - RC W1a: "Most of our Weirton and Steubenville buyers drive WV-2, US-22 or the Pittsburgh commute five days" (paste line 8).
  - "the question we hear most" (Weekley W1a, RC W1a).
  - These are acceptable dealer voice but unsourced.
- **[Additional Info] Weekley W1b wording (paste line 14).** "Sahara standard: ... heated front seats and wheel with remote start (Convenience Group)." The feature sheet marks the content "S" on Sahara, so it's true. The "(Convenience Group)" note reads like a paid package. Optional: drop the parenthetical.

### 4. Links and UTM [Confirmed]
- I ran curl `-I -L` on all **41 unique http(s) URLs** in the 4 pastes at ~06:01 ET: **41/41 200, 0 redirects, 0 non-200s.**
- No cross-store links:
  - Weekley pastes link only weekleychryslerdodgejeep.com plus Stellantis Media, CNBC and PR Newswire.
  - RC pastes link only gorcauto.com plus Stellantis Media, CNBC and PR Newswire.
- `tel:` numbers are the store numbers.
- The paste bodies carry no UTM, which is correct. The GMB UTMs are:
  - Weekley W1a `grand_cherokee_trims_order`
  - Weekley W1b `jeep_wrangler_buyers_guide`
  - **RC W1a `jeep_wrangler_sahara_vs_rubicon` ✔**
  - RC W1b `grand_cherokee_vs_grand_cherokee_l`
  - All use source=google, medium=organic, and base = the intended URL = the JSON-LD url.
- The GMB target URLs will 404 until each post is published on its dated path. That is expected and not tested as a failure.

### 5. Schema
- **Weekley JSON-LD parses [Confirmed]:**
  - Graph: AutoDealer, Person x2, WebPage, BlogPosting, FAQPage, BreadcrumbList.
  - The paste's script equals the .jsonld.html file (parsed-JSON equality).
  - FAQ 6/6 word for word against the visible H3+p.
  - datePublished = dateModified = byline `<time>`: 2026-10-08 (W1a) and 2026-10-12 (W1b). These are sane, but **future-dated** (see the paste path).
  - No aggregateRating, no Offer.
- **BLOCKER (both Weekley posts): the entity lock is broken [Confirmed].**
  - Every dealer reference is `https://www.weekleychryslerdodgejeep.com#organization` (4 per file): W1a paste lines 67/75/85/116, W1b paste lines 56/64/74/105, and lines 7/15/25/56 of each Weekley .jsonld.html. There is **0 `#dealer`**.
  - Source: `_build/dealers.py` line 5, WEEKLEY `org_id='https://www.weekleychryslerdodgejeep.com#organization'`.
  - The lock (amendment 2026-09-14; week-learn 09-14 and 10-05; T7375 card) is **Weekley `#dealer` only; RC `#organization` only; never clone the other rooftop's rule.** Pointing Weekley at `#organization` follows the RC pattern.
  - Live precedent: the Weekley Gladiator blog (6/3) body graph uses `https://www.weekleychryslerdodgejeep.com/#dealer` ×3, and live 4310 uses `/#dealer` ×12 [Confirmed, 06:01 curl].
  - So these blogs would publish under a different dealer entity than every other custom Weekley graph.
  - This is **not invention**: `#organization` is Weekley's real theme node. It is also not an Automatic F, because no wrong-rooftop entity is minted. The T7375 precedent scores an entity-lock miss as an Error with a schema deduction, so I score it as a **Gargle**, not a Gag.
- **RC [Confirmed]:**
  - **0 `<script>`, 0 `@context` in either RC paste**, so the plan holds and the JSON-LD stays off the page.
  - The RC .jsonld.html files use `https://www.gorcauto.com#organization` only, with 0 `#dealer`, which honors the RC lock. They parse, FAQ is 6/6 word for word, and dates are 10/08 and 10/12.
  - **[Gap Identified, not a Gag] Duplicate RC AutoDealer.** It's live on the RC homepage: `https://www.gorcauto.com/#organization` ×2 (slash) next to the platform node `https://www.gorcauto.com#organization` ×1 [Confirmed by curl at 06:01]. Val must choose or merge before hosting. Per rule 6, the missing schema on these RC posts is a Gap, not a Gag.

### 6. Pixel Motion safety [Confirmed]
- 0 blank lines in any paste, and every non-script line starts with a block tag (p, div, h1-h3, ul). That gives wpautop nothing to break into stray `<p>`/`<br>`.
- 0 `class=`, 0 `font-family`, 0 `<style>`, 0 iframe/form/input/button, 0 `&nbsp;`. Divs are balanced (14/14, 14/14, 13/13, 12/12), and there is one H1 each.
- Inline `style=` attributes are allowed by the blog format.
- RC has 2 staff `<img>` (both 200). The Weekley script block is multi-line JSON. The live Gladiator post shows that Pixel Motion keeps a multi-line body ld+json with no `<br>` injected.
- **[Gap Identified, site-side, FYI]** The live Gladiator body JSON-LD itself fails to parse (a trailing comma at line 95). That's pre-existing and not from this pack, but Weekley blog schema on that post is currently invalid.

### 7. Gate's PASS card vs the files
They line up on: SHAs (28/28), mechanics, FAQ parity, dates, RC 0 scripts, the drive-time screenshots, the RC W1a meta (128) and campaign, links (41 @ 200), NAP, staff, and no invented specs.

What Gate passed that I would not:
1. **Weekley dealer `@id`.** Gate checked that `#organization` matches the live theme node ("nothing invented") but did not check it against the written Weekley `#dealer` lock or the live Gladiator/4310 `/#dealer` precedent. **This is the blocker.**
2. **Weekley footer counties** ("Ashland and Loudonville across Richland and Knox counties"). Missed.
3. **Gate's numbers.** Re-Gate 1 says the title tags are "49/47/45/44 ... unchanged", but Weekley W1b's title tag is **53** after the optional retitle (INDEX and md both say 53). It's still within ≤55, so it's a record error only.
4. Gate's first pass called the Gladiator body JSON-LD "retained", but it doesn't parse (it's still present). FYI only.

---

## Scores (protocol v2.5, 8 dims × 10)

| Dim | Weekley W1a | Weekley W1b | RC W1a | RC W1b |
|---|---|---|---|---|
| Accuracy | 8 (footer counties) | 8 (footer counties) | 9 (soft "most of our buyers") | 9 |
| Completeness | 9 | 9 | 9 (schema held for Val, a Gap) | 9 (same) |
| Coherence | 9 | 9 | 9 | 9 |
| Audience EXTERNAL | 10 | 10 | 10 | 10 |
| Actionability | 9 | 9 | 9 | 9 |
| Insight | 8 | 8 | 9 | 9 |
| Presentation | 9 | 9 | 9 | 9 |
| Precision | 6 (entity lock ×4, footer) | 6 (entity lock ×4, footer, Convenience Group note) | 9 | 9 |
| **Total** | **68/80 (85.0%)** | **68/80 (85.0%)** | **73/80 (91.3%)** | **73/80 (91.3%)** |
| **Verdict** | **Gargle** | **Gargle** | **Swallow** | **Swallow** |

Benchmark: RC is at the clean-blog bar. Weekley content is equally strong; only the entity lock and one footer line keep it from a Swallow.

## Blockers (exact)
1. **Weekley entity lock (Error, both Weekley posts).** `_build/dealers.py` line 5 sets `org_id` to `...com#organization`. That renders into W1a paste lines 67/75/85/116, W1b paste lines 56/64/74/105, and lines 7/15/25/56 of each .jsonld.html.
2. **Weekley footer county line (Error, minor, both Weekley posts).** `_build/dealers.py` line 7 (`geo`), rendered at W1a paste line 59 and W1b paste line 48.
No blockers on RC.

## Rewrite notes for Ruby (Weekley only; nothing invented)
1. Set WEEKLEY `org_id` to **`https://www.weekleychryslerdodgejeep.com/#dealer`** (with the slash), matching live 4310 and the live Gladiator blog. Copy the node fields from **live 4310**, without inventing any:
   - `"name":"Weekley Chrysler Dodge Jeep Co"`
   - `"url":"https://www.weekleychryslerdodgejeep.com/"`
   - `"telephone":"+1-567-430-2908"`
   - address `50 Main St, Butler, OH 44822, US`
   - Leaving the AutoDealer as an @id-only stub is acceptable. Target: `#dealer` ≥1 and `#organization` 0 in both Weekley files.
   - Alternative: Sean writes a Weekley blog-lane exception ("blogs reference theme `#organization`") into `candidate-rules.md`, and I re-score with no rebuild. Until one of the two happens, there's no co-sign (rule 5: Epsilon doesn't amend a lock without a written ruling).
2. Footer: change to "Serving Butler, Mansfield, Mount Vernon, Ashland and Loudonville across Richland, Knox and Ashland counties." Or reuse the live 7/29 wording: "...and the broader Richland and Knox County area" (dropping Loudonville).
3. Optional, Weekley W1b paste line 14: drop "(Convenience Group)" or say "(the Convenience Group content is standard on Sahara)".
4. Rebuild `build.py weekley` only. Confirm the RC paste/jsonld/gmb SHAs are **unchanged**. Publish a new SHA list, have Nicky re-Gate the Weekley rows, then send it back to me for a quick re-co-sign. Expected Weekley re-score: Swallow at about 73/80 if only these change.

## Required paste path (amendment 10-05 rule 7)
Both stores use Pixel Motion, the post editor in the **Text/Source tab only**. Never open Visual, before or after the paste. Do no find/replace, and don't pretty-print. Run `sha256sum -c` right before you paste. Do not paste the .md, .jsonld.html (RC), .sources.md or .gmb.txt into the body.

| Post | Body (Text tab) | Title field | Meta Title | Meta Description | Meta Keyword | Slug | Publish date (must match URL path and schema) |
|---|---|---|---|---|---|---|---|
| RC W1a | whole `rc/w1a-jeep-wrangler-sahara-vs-rubicon-upper-ohio-valley.paste.html` (SHA `0a7b6d11...`), 0 script | md "CMS Title / H1" | md "SEO title tag" (45) | md "Meta description" (128) | md "Focus keywords" | `jeep-wrangler-sahara-vs-rubicon-upper-ohio-valley` | **2026-10-08** |
| RC W1b | whole `rc/w1b-jeep-grand-cherokee-vs-grand-cherokee-l-weirton-steubenville.paste.html` (SHA `d0013892...`), 0 script | md H1 | md (44) | md (130) | md Focus keywords | `jeep-grand-cherokee-vs-grand-cherokee-l-weirton-steubenville` | **2026-10-12** |
| Weekley W1a *(after rebuild + re-co-sign)* | whole rebuilt `weekley/w1a-...paste.html`, body + one script block, pasted as one | md H1 | md (49) | md (135) | md Focus keywords | `jeep-grand-cherokee-trims-in-order-butler-oh` | **2026-10-08** |
| Weekley W1b *(after rebuild + re-co-sign)* | whole rebuilt `weekley/w1b-...paste.html`, body + one script block | md H1 | md (53) | md (127) | md Focus keywords | `jeep-wrangler-buyers-guide-north-central-ohio` | **2026-10-12** |

- **Dates:** schedule each post for its planned date, or publish it on that date. The JSON-LD `@id`/`url`, the byline `<time>`, and the GMB UTM base all hard-code `/2026/10/08/` or `/2026/10/12/`. Publishing today (10/7) would move the URL and future-date the schema. If a date slips, rebuild with the new date. A rebuild means new SHAs and a re-Gate.
- **Images:** set no featured image unless the dealer supplies a photo. Do not generate one.
- **RC .jsonld.html:** goes to Val only after she resolves the duplicate AutoDealer `@id`. Not part of this paste.
- **GMB posts:** these are a separate GBP action after the post is live on the dated URL. They are not covered by this co-sign or by the blog paste write-off.
- **After the paste:** Ruby runs the character-by-character live check and adds a proof row per the standing write-off (live URL, saved HTML, validator, Gate PASS, Epsilon score).

## Sean checklist (short; this goes to Sean because Weekley sits at ≥85% with a Gargle)
1. **Weekley blog entity.** OK Ruby's rebuild to `/#dealer` (my default; it matches live 4310 and the Gladiator blog), or write an exception if you want blogs to point at the theme's `#organization`. Why: it's a written lock, and Gate didn't catch it.
2. **Split the paste?** RC W1a and W1b are co-signed now. Say whether RC goes ahead alone today, or all four wait for the Weekley re-Gate. The standing write-off is per post, so splitting fits it.
3. Optional, one line: confirm Ruby's wording of the 5:33 AM standing write-off matches what you said yes to. The original list text isn't saved.

## Errors
- **E1 (pack, Weekley W1a/W1b): entity lock broken.** The graph uses `#organization` ×4 and `#dealer` ×0, against the written Weekley `#dealer` lock. It comes from `_build/dealers.py` line 5. Blocks a Weekley Swallow. [Confirmed]
- **E2 (pack, Weekley W1a/W1b): footer geography.** It says "Ashland and Loudonville across Richland and Knox counties", but both are in Ashland County. [Confirmed]
- **E3 (Gate record):** Re-Gate 1 states Weekley W1b's title tag is 47 "unchanged", but it is 53. Within limits. Record error only. [Confirmed]
- **E4 (Gate scope):** the entity check compared against the live theme node, not against the written per-rooftop lock (the amendment-09-14 pattern). [Confirmed]
- FYI, not pack Errors:
  - The RC duplicate AutoDealer `@id` on the live homepage (Gap for Val).
  - The live Weekley Gladiator body JSON-LD doesn't parse (trailing comma).
  - INDEX.md still says RC W1a meta = 130 (noted by Gate). These items are not in the SHA list.

Tags used: [Confirmed] [Assumption - Check] [Gap Identified] [Additional Info]. No CMS. No Chrome. No messages sent. Nothing else edited.

---

# Re-co-sign 2026-10-07 (Weekley W1a + W1b rebuild)

Seat: Epsilon. READ-ONLY. Checks ran 06:17-06:25 ET. The card write-up was delayed by a box outage (~06:25-07:05 ET), and the list re-check ran at 07:05 ET. No CMS, no browser, no messages.
Inputs: Ruby's rebuild (10/7 06:16 ET), Nicky Re-Gate 4 PASS (`/workspace/nicky/output/gate-week1-blogs-weekley-rc-2026-10-07.md`), the list `SHA256SUMS-weekley-rc-personfix-2026-10-07.txt` (28 lines), and the backups in `/workspace/tmp/blogw1/` (`.pre-epsfix`, `.pre-person`).

## OUTCOME

```
Weekley W1a   OUTCOME: Swallow  OVERALL: 72/80 (90.0%)   CO-SIGNED paste SHA 81dc51b407b8d1a59914e7f6a4381c634275358aa91bf4ef940bea6cb4d9718a
Weekley W1b   OUTCOME: Swallow  OVERALL: 71/80 (88.8%)   CO-SIGNED paste SHA 7bd8e74e2f1a3f8df2b3a3c388c05e19c81b1f066e5dcd5d591381e385c42990
RC W1a / RC W1b: still co-signed from the first pass (0a7b6d11... / d0013892...). The RC paste bytes are unchanged [Confirmed 07:05].
Automatic F: none. Errors in the paste files: 0.
All four Week-1 Pixel Motion posts are now co-signed one post at a time.
DOORS FOR SEAN: none required (both Weekley posts are Swallows at >=85%). One housekeeping item for Ruby below.
REWRITE NOTES FOR RUBY: restore the two Weekley sources.md files and the personfix list (housekeeping; no paste file is affected).
```

## Evidence (06:17-06:25 ET, from my run)
- **List:** `sha256sum -c SHA256SUMS-weekley-rc-personfix-2026-10-07.txt` returned 28/28 OK at ~06:18.
  - Compared with the metafix list I audited, only `_build/dealers.py` and the 8 Weekley paste/jsonld/md/sources.md files changed.
  - The RC files and the Weekley gmb files are unchanged (gmb `41a99128...`, `3fb57d17...`).
- **Diff against the audited files.** The `.pre-epsfix` backups hash to the SHAs I audited (`2790b9fe...`, `378806c6...`), and the diff contains only the allowed changes:
  1. The dealer reference: `...com#organization` → `https://www.weekleychryslerdodgejeep.com/#dealer`, with full node fields (name "Weekley Chrysler Dodge Jeep Co", url, `+1-567-430-2908`, 50 Main St, Butler, OH 44822, US). These match the live 4310 `/#dealer` node field for field [Confirmed by curl].
  2. The footer: "Serving Butler and Mansfield in Richland County, Mount Vernon in Knox County, Ashland in Ashland County, and Loudonville in Ashland and Holmes counties." (W1a line 59, W1b line 48).
  3. Person @ids: `/#author-erik-schneeg` and `/#owner-matt-weekley`. Live 4310 uses exactly these two [Confirmed by curl].
  - There are no other diffs and no link changes, so no re-check of links was needed.
- **Schema [Confirmed]:**
  - The JSON-LD parses, and paste == .jsonld.html in parsed JSON.
  - `/#dealer` ×4, `#organization` 0, `com#author-` 0, bare `.com#` 0.
  - FAQ 6/6 word for word.
  - Date paths: W1a only `/2026/10/08/` (datePublished = dateModified = byline 2026-10-08). W1b only `/2026/10/12/` (2026-10-12).
- **Hygiene [Confirmed]:** 0 non-ASCII bytes, 0 HTML comments, 0 unfilled tokens. The block-tag line structure is unchanged, so it stays Text-tab safe.
- **Footer counties [Confirmed, Wikipedia, 10/7]:**
  - Butler: "a village in Richland County" (infobox County: Richland).
  - Mansfield: "a city in Richland County ... county seat".
  - Mount Vernon: "a city in Knox County".
  - Ashland: "a city in Ashland County".
  - Loudonville: "a village in Ashland and Holmes counties".
  - All five are true. Error E2 from the first pass is closed.
- **Error E1 (entity lock) is closed.** The Weekley `#dealer` lock now holds.

## Re-check at 07:05 ET, after the outage (state of the box)
- **`SHA256SUMS-weekley-rc-personfix-2026-10-07.txt` is no longer on disk** [Confirmed]. The box came back with files restored around 06:17:45 ET: every file in this folder carries that mtime, and the folder also holds a `SHA256SUMS-weekley-rc-epsfix-2026-10-07.txt`.
- I rebuilt the personfix list from the metafix list plus the 9 personfix hashes I recorded at 06:18 (kept at `/tmp/personfix-reconstructed.txt`, scratch). Result: **26/28 OK, 2 FAILED**:
  - `weekley/w1a-...sources.md`: now `7426ea6e...` (the **pre-epsfix** version) instead of `de6b8d79...`.
  - `weekley/w1b-...sources.md`: now `28fce7c2...` (pre-epsfix) instead of `5f8d96b6...`.
  - These two files have lost the "Footer county pairing" Wikipedia section.
- **Every co-signed paste file is byte-identical to what I audited:**
  - W1a paste `81dc51b4...`, W1b paste `7bd8e74e...`.
  - jsonld `95c8a39f...` and `674602d4...`.
  - md `472c1109...` and `83f7231b...`.
  - `_build/dealers.py` `1349db2c...`.
  - RC pastes `0a7b6d11...` and `d0013892...`.
- **Impact:** none on the paste. sources.md is never pasted. It does break the list check (2/28) and drops the written county sources from the pack.
- **Housekeeping for Ruby, not a blocker:**
  - Restore both sources.md files to `de6b8d79...` and `5f8d96b6...` (add back the Wikipedia county section).
  - Restore or re-issue the personfix list. If it's re-issued with different bytes, the Gate needs the new list. The co-sign stays tied to the paste SHAs above.

## Scores (protocol v2.5)
| Dim | W1a | W1b |
|---|---|---|
| Accuracy | 9 | 9 |
| Completeness | 9 | 9 |
| Coherence | 9 | 9 |
| Audience EXTERNAL | 10 | 10 |
| Actionability | 9 | 9 |
| Insight | 8 | 8 |
| Presentation | 9 | 9 |
| Precision | 9 | 8 (the optional "(Convenience Group)" wording at paste line 14 is unchanged) |
| **Total** | **72/80 (90.0%)** | **71/80 (88.8%)** |

## Notes (non-blocking)
- **[Additional Info] jobTitle.** The two person @ids match live 4310, but the jobTitle differs:
  - 4310: Erik "Sales Consultant", Matt "Owner".
  - Blogs: "Sales" and "Owner / Sales". The blogs match the live staff page.
  - Same entity, slightly different titles. Align them on the next 4310 refresh or blog rebuild if Sean cares. Not a co-sign issue.
- **[Assumption - Check]** I did not re-read Nicky's Re-Gate 4 section line by line after the restore. My verdict rests on my own checks above.

## Required paste path (unchanged)
- Pixel Motion post editor, **Text/Source tab only**. Never open Visual, no find/replace. Run `sha256sum` on each paste file right before the paste: W1a `81dc51b4...`, W1b `7bd8e74e...`.
- **Body:** the whole `weekley/<post>.paste.html`, body plus its one `<script type="application/ld+json">`, pasted as one block.
- **Fields from the md:** Title ← "CMS Title / H1". Meta Title ← "SEO title tag" (W1a 49, W1b 53). Meta Description ← "Meta description" (W1a 135, W1b 127). Meta Keyword ← "Focus keywords". Slug ← md Slug.
- **Publish date must equal the URL date:** W1a **2026-10-08**, W1b **2026-10-12**. Schema `@id`/`url`, byline `<time>`, and the GMB UTM base all hard-code these dates. If a date slips, rebuild, then re-Gate and re-co-sign.
- No featured image unless the dealer supplies one. GMB posts are a separate action after go-live.
- After the paste: Ruby's character-by-character live check, plus a proof row under the 10/7 standing write-off.

## Errors (this pass)
- None in the co-signed files.
- Process FYI: the 06:25-07:05 box outage/restore reverted 2 non-paste files and removed the personfix list (see above). [Confirmed]
