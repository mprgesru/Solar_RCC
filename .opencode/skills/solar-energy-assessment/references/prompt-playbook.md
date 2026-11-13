# Prompt playbook

Reusable prompts for each phase. Replace `<CITY>`, `<PATH>`, `<YEAR>`, `<RESOLUTION>` and thresholds with project values.

## Phase 0 — Scope

```text
We are assessing rooftop solar potential for <CITY>. Ask me the minimum questions needed about boundary, resolution, software, validation, scenarios and outputs, then propose a short protocol.
```

```text
Read this tutorial: <URL>. Summarise the inputs, tools and suitability criteria, and explain which parts must be adapted for a tropical South Asian city.
```

```text
Based on the available data, propose a whole-city vs pilot-ward design, a 1 m vs 2 m resolution trade-off, and a validation strategy.
```

## Phase 1 — Boundary

```text
Find the city boundary and ward layer behind this ArcGIS dashboard: <URL>. Check whether the layers are public, query them as GeoJSON, and report the ward count, area, and topology.
```

```text
Check the boundary and ward files for validity, overlaps, gaps, self-intersections, duplicate vertices and area consistency. Repair if needed and report the before/after areas.
```

```text
The RCC boundary should exclude river water bodies and focus on the built-up area. Propose how to create a net-land boundary and a built-up mask, and list the data needed.
```

## Phase 2 — Footprints

```text
Download or query the best open building footprints for <CITY>. Clip to the boundary, conflate Google/Microsoft/OSM, and report building count, footprint area, confidence distribution and completeness caveats.
```

```text
Create a unique Building_ID and a data dictionary for the footprint layer. Flag small structures and low-confidence polygons rather than deleting them.
```

## Phase 3 — Heights

```text
Extract GlobalBuildingAtlas heights for <CITY> without downloading the full 4 GB Parquet tile. Use DuckDB or an equivalent remote query, then assign heights by largest overlap and flag fallbacks.
```

```text
Assess the height distribution and outliers. Propose a defensible cap for the DSM, retaining raw heights and documenting the choice.
```

## Phase 4 — DSM

```text
Build a 2 m DSM from building footprints, GBA heights, Meta/WRI canopy and Copernicus DTM. Report the grid, DTM/canopy/building/DSM ranges, and the limitations of a LoD1 flat-top surface.
```

```text
Check that all rasters share CRS, extent, shape and transform. Compute slope/aspect and explain why edge pixels dominate the slope distribution.
```

## Phase 5 — Solar

```text
Write an ArcPy script for annual Raster Solar Radiation using <PATH> DSM, slope and aspect, buildings as the analysis mask, <TIMEZONE>, diffuse <VALUE>, transmittivity <VALUE>, sun map grid level 6, and GPU then CPU.
```

```text
The model gives a mean POA of <VALUE> kWh/m2 and PVOUT of <VALUE> kWh/kWp, compared with Solargis <VALUE>. Diagnose the bias and propose calibration or season-specific parameters.
```

## Phase 6 — Suitability and energy

```text
Create base, tutorial-style and strict suitability scenarios. Use slope <=45, radiation thresholds <VALUES>, and handle flat cells (aspect = -1) explicitly. Explain why a blanket north-facing exclusion may be inappropriate for flat roofs.
```

```text
Write an ArcPy workflow for zonal statistics, join, field calculation and CSV export. Use UpdateCursor for calculations and export CSV to a folder, not a geodatabase.
```

```text
The CalculateField tool fails after adding fields. Replace it with a robust UpdateCursor calculation and explain the likely cause.
```

## Phase 7 — Seasonal

```text
Run four seasonal Raster Solar Radiation periods using the annual suitable raster as the mask. Check whether the outputs are cumulative from 1 January and correct them by differencing if needed.
```

```text
Compare the corrected seasonal shares with Solargis PVOUT shares. If the model overweights monsoon, construct a benchmark-adjusted seasonal profile and explain both.
```

## Phase 8 — Validation

```text
Create a stratified random 100-building validation sample across all wards and three size classes. Produce an Excel worksheet with dropdowns, a KML, a GeoPackage and a sampling log.
```

```text
Compute area bias/MAE/RMSE/MAPE and height RMSE/correlation. Report full-sample and outlier-excluded metrics, and explain what the sample does not validate.
```

## Phase 9 — Analysis

```text
Analyze the building-level results for the whole city and by ward. Report capacity, generation, PVOUT, density, suitable fraction, top/bottom wards, concentration (Gini, top shares) and building-size/height-confidence contributions.
```

```text
Compare base/tutorial/strict scenarios. Quantify the north-facing exclusion effect by ward and explain why the strict threshold may be non-binding.
```

```text
Produce publication figures: study area, annual potential, ward ranking, seasonal heatmap/maps, scenario comparison, validation, sensitivity, concentration, workflow. Save 300 dpi PNG and PDF.
```

## Phase 10 — Manuscript

```text
Write a research article with abstract, introduction, study area, data, methods, results, discussion, limitations, conclusions and references. Include all methodological caveats: LoD1 flat roofs, height uncertainty, model bias, seasonal cumulative correction, validation gaps and no economic potential.
```

```text
Turn the results into a Word manuscript with embedded figures and tables. Add figure captions and a data/code availability statement.
```

```text
Review the manuscript for overclaiming. Separate technical potential from economic/market potential, and label calibrated vs uncalibrated results.
```

## Packaging and reuse

```text
Create a data manifest, checksums, README and a small report zip plus a full data zip. Respect GitHub file-size limits.
```

```text
Package this workflow as a reusable OpenCode skill with SKILL.md, references, templates and scripts. Keep it data-agnostic and link to the case study.
```
