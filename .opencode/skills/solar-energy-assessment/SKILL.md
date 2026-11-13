---
name: Solar Energy Assessment
description: Plan, execute, validate, and write up a building-level rooftop solar photovoltaic (PV) potential assessment using open geospatial data and GIS, with ArcGIS Pro/Spatial Analyst or open-source alternatives.
license: MIT
compatibility: OpenCode V2
metadata:
  version: 1.0.0
  updated: 2026-11-13
  author: Solar Energy Assessment skill
---

# Solar Energy Assessment

Use this skill to produce a reproducible, building-level rooftop PV potential assessment for a city, district, or campus, from open geospatial data through to a manuscript-ready results package.

## When to use

- Estimating rooftop solar potential for a city, municipality, ward, campus, or neighbourhood.
- Producing building-level capacity and generation estimates, ward summaries, seasonal profiles, and scenario comparisons.
- Validating a remote-sensing building/roof layer and writing a methods/results/discussion section.
- Reusing a proven workflow in a new city where only open data are available.

## When not to use

- Utility-scale, ground-mounted PV siting (different terrain, land-use, and grid constraints).
- Detailed electrical design, inverter sizing, or bankable yield simulation (use PVsyst or similar).
- Regulatory energy yield certification.
- Studies without a boundary and building footprint layer, unless the user accepts a coarse screening approach.

## Non-negotiable principles

1. **Use a fine-resolution DSM, not a 30 m DEM.** Rooftop analysis needs 0.5–2 m cells. A 30 m DEM is only a DTM.
2. **Validate the boundary and wards before mapping.** Repair invalid geometry, check overlaps/gaps, and confirm the boundary excludes water where required.
3. **Document height provenance and confidence.** Open building heights are model products; flag source, variance, and low-confidence cases.
4. **Do not apply a blanket north-facing exclusion without justification.** For flat roofs, panel orientation is a design choice. Treat north exclusion as a scenario, not the base rule.
5. **Benchmark the solar model.** Compare modelled GHI/POA/PVOUT with NASA POWER and Global Solar Atlas/Solargis. Report raw and calibrated results.
6. **Check seasonal outputs for cumulative-start artefacts.** If all seasons start on 1 January, difference consecutive cumulative totals before analysis.
7. **Use a folder for CSV export.** A CSV cannot be stored inside an Esri file geodatabase.
8. **Validate with stratified samples.** Report full-sample and outlier-excluded metrics; never silently delete outliers.
9. **State limitations explicitly.** LoD1 flat roofs, height uncertainty, footprint vintage, missing roof type/use, no ground-truth PV yield, and economic/market potential excluded.
10. **Respect data licences.** Do not redistribute Google Earth imagery; document CC BY, CC BY-NC, ODbL, and other terms.

## Inputs to collect

| Input | Preferred source | Notes |
|---|---|---|
| Boundary and wards | City GIS, ArcGIS FeatureServer, OSM, or official boundary | Validate topology; dissolve wards to boundary |
| Building footprints | Google Open Buildings, Microsoft, OSM/HOT, or local cadastre | Conflate sources; keep confidence/source |
| Building heights | GlobalBuildingAtlas, Open Buildings 2.5D, LiDAR, drone, or stereo DSM | Prefer per-building heights; flag confidence |
| Canopy height | Meta/WRI 1 m, ETH 10 m, or local LiDAR | Tree shading is first-order in tropical cities |
| Bare-earth DTM | Copernicus GLO-30, FABDEM, local LiDAR | 30 m is acceptable for DTM, not DSM |
| Solar benchmarks | NASA POWER, Global Solar Atlas/Solargis, BMD | Use for calibration and validation |
| Local PV parameters | Module datasheets, installer quotes, utility tariffs | Efficiency, PR, costs, net metering |
| Validation imagery | Google Earth, high-resolution satellite, drone | Visual validation only; do not redistribute |

## Workflow

### Phase 0 — Scope and decisions

Ask the user:

1. Study boundary: whole city or pilot wards?
2. Resolution: 1 m pilot + 2 m city-wide, or 1 m city-wide?
3. Software: ArcGIS Pro + Spatial Analyst, QGIS/GRASS, or Python?
4. Validation: drone/field sample, Google Earth sample, or remote-sensing only?
5. Scenarios: base, tutorial-style north exclusion, strict threshold, economic screening?
6. Outputs: technical potential only, or also LCOE, demand, and policy analysis?

Read `references/workflow.md` for the detailed sequence.

### Phase 1 — Boundary, water, and built-up mask

- Obtain the boundary and wards; project to a local projected CRS (metres).
- Check validity, overlaps, gaps, and ward count.
- Remove permanent water polygons and create a net-land boundary.
- Compute built-up/tree/cropland fractions for context.
- Save a validation report (`edited_boundary_qa.json` or equivalent).

### Phase 2 — Footprints and heights

- Download the finest available footprints; clip to the boundary.
- Conflate Google/Microsoft/OSM; keep a unique `Building_ID`.
- Assign heights by largest polygon overlap; use nearest/median fallbacks and flag them.
- Retain `height_var`, `height_source`, `height_confidence`.
- Cap implausible outliers for the DSM only; keep raw heights.

### Phase 3 — Canopy, DTM, and 2 m DSM

- Mosaic canopy tiles; reproject to the analysis grid.
- Reproject the DTM to the same grid.
- Rasterise building heights and compute:
  `DSM = DTM + max(building height, canopy height)`.
- Save DSM, nDSM, slope, and aspect.
- Document that a LoD1 DSM is flat-topped and does not resolve roof pitch.

### Phase 4 — Solar radiation

- In ArcGIS Pro: `Raster Solar Radiation` (Spatial Analyst).
- Set the time zone, date range, analysis mask, slope/aspect, diffuse proportion, transmittivity, sun-map grid level, and GPU/CPU target.
- In QGIS/GRASS: use `r.sun` with horizon maps; in Python: `pvlib` for point checks.
- Validate the annual mean against NASA POWER and Solargis.
- Save annual and seasonal rasters.

### Phase 5 — Suitability scenarios

Define at least:

- **Base:** slope ≤45°, radiation ≥ local threshold, no north exclusion.
- **Tutorial-style:** lower threshold + north-facing exclusion (for comparison only).
- **Strict:** higher threshold, no north exclusion.
- **Optional economic:** LCOE ≤ tariff or payback threshold.

Justify thresholds from the local irradiation distribution; do not import mid-latitude defaults blindly.

### Phase 6 — Zonal statistics and energy conversion

- `Zonal Statistics as Table` per building: mean, sum, area, count.
- Join `AREA`, `MEAN`, `SUM`, `COUNT` to a copy of the buildings.
- Add fields: `roof_factor`, `usable_area_m2`, `capacity_kWp`, `incident_MWh`, `elec_MWh`, `co2_t`, `scenario`.
- Use `arcpy.da.UpdateCursor` for calculations when `CalculateField` is unreliable.
- Export CSV to a **folder**, not a geodatabase.

### Phase 7 — Validation and uncertainty

- Draw a stratified random sample (e.g., 100 buildings across wards and size classes).
- Measure footprint area and height in Google Earth or field data.
- Record imagery date, roof type, condition, obstructions, tree/neighbour shade, existing PV, usable-roof percentage, confidence.
- Compute bias, MAE, RMSE, MAPE, median/p95 absolute error, correlation.
- Report full-sample and outlier-excluded metrics; identify likely mismatches.
- Run one-at-a-time and combined sensitivity; Monte Carlo if time permits.

### Phase 8 — Analysis, figures, and manuscript

- Whole-city totals: capacity, generation, CO₂, usable area, PVOUT.
- Ward rankings: total generation and generation density; report both.
- Seasonal profiles: model-derived and benchmark-adjusted.
- Scenario comparison and north-filter effect by ward.
- Concentration: top 1/5/10% building shares; Gini.
- Figures: study area, annual potential, ward ranking, seasonal heatmap/maps, scenarios, validation, sensitivity, concentration, workflow.
- Tables: data sources, parameters, whole-city results, seasons, top/bottom wards, validation, sensitivity, size/height contributions.
- Manuscript: abstract, introduction, study area, methods, results, discussion, limitations, conclusions, references.
- Use `templates/manuscript_outline.md` and `references/figure-style.md`.

## Output contract

A complete assessment should deliver:

1. Analysis-ready boundary/wards and a QA report.
2. Building-level table with source/height/confidence flags.
3. 2 m DSM, slope, aspect, annual and seasonal radiation rasters.
4. Suitability scenarios and building-level energy table.
5. Ward and seasonal summaries.
6. Validation metrics and outlier notes.
7. Publication figures (300 dpi PNG + PDF) and tables.
8. A manuscript draft with limitations and data/licence statements.
9. A reproducible data manifest and scripts.

## Quality gates

Stop and fix before writing the manuscript if:

- The boundary or wards are invalid, overlap, or contain major gaps.
- Building heights are missing for >10% of suitable buildings without flags.
- The DSM is coarser than 5 m or built from a 30 m DEM.
- Annual mean POA differs from the local benchmark by >20% without explanation.
- Seasonal totals sum to more than ~110% or less than ~90% of the annual total (check cumulative-start artefacts).
- Zonal output has duplicate `Building_ID`s or missing `AREA`/`MEAN` for most buildings.
- Validation MAPE >15% or height RMSE >5 m without a documented reason.
- The manuscript reports only the raw model without benchmark calibration or uncertainty.

## Common pitfalls

| Pitfall | Fix |
|---|---|
| 30 m SRTM/Copernicus DEM used as DSM | Use a 2 m DSM from building heights + canopy + DTM |
| Shape integrity error in ArcGIS Pro | Repair geometry, dissolve repaired wards, export to file GDB |
| `Feature Class To Feature Class` not found | Use `Copy Features` or right-click → Data → Export Features |
| `CalculateField` fails | Use `arcpy.da.UpdateCursor` |
| CSV export path inside `.gdb` | Export to a folder path |
| Seasonal totals cumulative | Difference consecutive cumulative runs |
| North-facing roofs excluded everywhere | Treat as scenario; flat roofs can use tilted racks |
| Model 10–20% above Solargis | Report calibration factor and calibrated result |
| GitHub 25 MB upload limit | Use release assets or split archives |
| Local `C:\` path inaccessible to a Linux agent | Upload files or use GitHub release assets |

## Reuse in another project

Copy the skill folder:

```text
<new-project>/.opencode/skills/solar-energy-assessment/
```

Or point the new project to this repository:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["C:/path/to/Solar_RCC/.opencode/skills"]
}
```

Or install globally:

```text
~/.config/opencode/skills/solar-energy-assessment/
```

## References

Read only what the task needs:

- `references/workflow.md` — detailed phase-by-phase procedure.
- `references/methodology.md` — equations, parameters, scenarios, calibration, validation.
- `references/data-sources.md` — datasets, URLs, resolutions, licences.
- `references/qa-checklist.md` — boundary, raster, building, solar, CSV, figure checks.
- `references/licenses.md` — redistribution rules and attribution.
- `references/prompt-playbook.md` — reusable prompts for each phase.
- `references/figure-style.md` — publication figure standards.
- `templates/arcpy_solar_workflow.py` — generic ArcGIS Pro workflow.
- `templates/validation_sample.py` — stratified validation sample and Excel/KML.
- `templates/manuscript_outline.md` — article structure.
- `templates/data_manifest.template.csv` — manifest columns.
- `scripts/validate_geodata.py` — generic geodata QA.
- `scripts/summarize_results.py` — generic whole-city/ward/seasonal summaries.
- `examples/rajshahi.md` — Rajshahi case study and release link.

## Example

The Rajshahi case study (2026) used 30 wards, 106,134 Google Open Buildings footprints, GBA heights, Meta/WRI canopy, Copernicus DTM, a 2 m DSM, and a 100-building validation sample. Headline results: 509.5 MWp, 821.2 GWh yr⁻¹ uncalibrated, 727.3 GWh yr⁻¹ benchmark-calibrated. See `examples/rajshahi.md` and the GitHub release.
