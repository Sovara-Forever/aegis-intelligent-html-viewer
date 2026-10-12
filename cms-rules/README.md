# CMS rules (editable)

One JSON file per CMS. Field names match the provider list compiled into the AEGIS app bundle
(`id`, `label`, `cms_notes`, `allowed_tags`, `forbidden_tags`, `h2_float_risk`, `json_ld_in_cms`, ...),
plus a new `render_rules` block used by `review-kit/review.js` to show a "CMS-saved" approximation.

`render_rules` keys:
- `wpautop` (bool): wrap blank-line-separated text in `<p>`, single newlines in text become `<br>`.
- `wptexturize` (list of `{pattern, replace}` regex swaps), e.g. `4x4` -> `4×4`.
- `strip_json_ld` (bool): remove `<script type="application/ld+json">`.
- `strip_css` (list): inline-style properties removed exactly by name (`list-style` does not remove `list-style-type`).
- `keep_css` (list): documentation of what survives.
- `flag_tags` (list): tags shown as warnings in the review.

`stores.<store>.render_rules` overrides the CMS defaults for one store (e.g. RC on Pixel Motion).
To add a rule: edit the JSON, commit to main; Pages redeploys. No build step.
The preview is an approximation of the CMS, not the CMS itself. Always confirm on the live page.
