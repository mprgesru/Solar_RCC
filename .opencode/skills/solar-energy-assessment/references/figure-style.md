# Figure style

## Output formats

- 300 dpi PNG for review and Word.
- Vector PDF for journal submission.
- Keep editable source data and scripts.

## Typography

- Sans-serif: Arial, Helvetica, or DejaVu Sans.
- Base size 8–10 pt; panel titles 10–11 pt bold.
- Use consistent sizes across all figures.
- Use `(a)`, `(b)`, `(c)` panel labels, bold, top-left.

## Colour

- Use a colourblind-friendly palette.
- Sequential maps: `viridis`, `magma`, `YlOrRd`/`YlGnBu` with care.
- Categorical: blue `#2E86AB`, orange `#F18F01`, green `#6BAA75`, red `#C73E1D`, purple `#8E6C8A`, grey `#5C5C5C`.
- Avoid red–green only contrasts.
- Keep zone colours consistent across figures.

## Maps

- Use a projected CRS in metres; equal aspect.
- Show boundary and ward outlines.
- Include a north arrow and scale bar.
- Label wards with short IDs (W1–W30), not long names.
- Use a single shared colour scale for small multiples.
- Mask water/NoData clearly.
- Do not use Google Earth imagery in publication figures.

## Charts

- Remove unnecessary gridlines; keep light horizontal grids for bar charts.
- Put units in axis labels.
- Annotate values on bars when space allows.
- Sort bars meaningfully (by value or geography).
- Use log scales only when the range is very large; label “log scale”.
- Put legends inside the figure or directly below, not overlapping axis labels.

## Captions

A caption should be self-contained:

- what is shown;
- unit;
- period;
- data source;
- any smoothing/calibration;
- panel explanation.

Example:

> **Figure 2.** Annual rooftop potential. (a) Annual generation per suitable building (MWh yr⁻¹, log scale). (b) Ward-level generation density (GWh km⁻² yr⁻¹). Boundaries are the validated RCC wards; values are from the base scenario.

## Figure set for a rooftop PV paper

1. Study area and input data.
2. Annual potential map and ward density.
3. Ward ranking (total and density).
4. Seasonal city variation and model vs benchmark shares.
5. Ward × season heatmap.
6. Scenario comparison and north-filter effect.
7. Validation scatter/error plots.
8. Sensitivity/benchmark calibration.
9. Size/concentration/height-confidence contributions.
10. Workflow diagram.
11. Seasonal ward maps (optional appendix).

## Workflow diagram

- Use a three-column swimlane: Data inputs → Processing → Outputs.
- Number the processing steps.
- Use rounded boxes, a light column background, and thin arrows.
- Avoid text overlapping icons or numbers.
- Add a bottom note with validation, sensitivity and calibration values.
