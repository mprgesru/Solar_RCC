# QA checklist

Use this before analysis, before manuscript writing, and before packaging.

## 1. Boundary and wards

- [ ] Projected CRS in metres.
- [ ] One boundary polygon (or multipolygon) and 30/expected ward count.
- [ ] Every ward geometry valid (`is_valid`).
- [ ] No self-intersections, duplicate vertices, or unclosed rings.
- [ ] Ward names and zone names complete.
- [ ] Ward union ≈ boundary (report symmetric difference).
- [ ] No unintended overlaps or gaps.
- [ ] Water polygons removed where the study area is net land.
- [ ] Gross area, water area, net land area and built-up/tree fractions recorded.
- [ ] Boundary source, date and licence documented.

**Common fix:** `Repair Geometry` (ArcGIS Pro), `make_valid`, `buffer(0)`, dissolve repaired wards, export to file geodatabase.

## 2. Building footprints

- [ ] Unique `Building_ID`; no duplicates.
- [ ] Valid geometries; no empty/null.
- [ ] Footprint area positive; compare to source `area_in_meters`.
- [ ] Confidence/source preserved.
- [ ] Small structures flagged, not silently deleted.
- [ ] Footprint completeness checked against imagery for a sample.
- [ ] Buildings outside net land flagged (`inside_land`).

## 3. Heights

- [ ] Height assigned for >90% of buildings (or flagged).
- [ ] `height_source` and `height_confidence` populated.
- [ ] `height_var` retained.
- [ ] Outliers inspected; cap documented (e.g. 45 m) and raw heights retained.
- [ ] Height sample validated against floors/observed height.
- [ ] Median/p90 heights plausible for the city.

## 4. Rasters

- [ ] DSM, nDSM, slope, aspect, canopy and building height share shape, transform, CRS.
- [ ] Cell size 0.5–2 m (not 30 m).
- [ ] No negative surface heights.
- [ ] Building pixel count ≈ footprint area / cell area.
- [ ] Canopy fraction plausible for the city.
- [ ] Slope/aspect edges not used as roof pitch without caveat.
- [ ] NoData handled consistently.

## 5. Solar radiation

- [ ] Time zone correct (e.g. Bangladesh Standard Time, UTC+6).
- [ ] Date range correct; total span ≤1 year.
- [ ] Analysis mask correct; annual vs seasonal masks documented.
- [ ] Diffuse proportion/transmittivity justified.
- [ ] Sun map grid level appropriate.
- [ ] GPU/CPU target documented.
- [ ] Annual mean POA within ~20% of Solargis GTI.
- [ ] PVOUT within ~15% of Solargis PVOUT or calibration reported.
- [ ] North-facing and shaded roofs lower than south/open roofs.
- [ ] No all-zero or all-NoData output.

## 6. Suitability and zonal statistics

- [ ] Slope threshold applied.
- [ ] Radiation threshold justified from local distribution.
- [ ] Flat cells (aspect = −1) handled explicitly.
- [ ] North exclusion only as a scenario, not the base, unless justified.
- [ ] `AREA`, `MEAN`, `SUM`, `COUNT` present.
- [ ] `AREA` in m² (projected CRS).
- [ ] `MEAN` in kWh m⁻² period⁻¹.
- [ ] Duplicate/missing zones checked.
- [ ] Buildings with no suitable cells are retained with null/zero, not dropped.

## 7. Energy table

- [ ] `roof_factor`, `usable_area_m2`, `capacity_kWp`, `incident_MWh`, `elec_MWh`, `co2_t`, `scenario` present.
- [ ] `capacity_kWp` ≤ footprint area / module area per kWp.
- [ ] No negative generation.
- [ ] No absurd outliers; top 20 inspected.
- [ ] CSV exported to a folder, not inside a `.gdb`.
- [ ] Row count equals buildings (or documented subset).

## 8. Seasonal

- [ ] Four seasons cover the year without gaps/overlaps.
- [ ] Same annual suitable mask used.
- [ ] Seasonal totals not cumulative; check monotonic increase.
- [ ] Seasonal sum 90–110% of annual.
- [ ] Model shares compared with Solargis.
- [ ] Benchmark-adjusted profile constructed if needed.
- [ ] Both raw-corrected and adjusted profiles reported.

## 9. Validation

- [ ] Stratified sample with recorded seed.
- [ ] All wards represented (or coverage documented).
- [ ] Imagery date recorded.
- [ ] Footprint area measured on nadir imagery.
- [ ] Height/floors recorded.
- [ ] Roof type, condition, obstructions, shade, existing PV, usable %.
- [ ] Confidence and notes.
- [ ] Area MAPE and height RMSE computed.
- [ ] Full-sample and outlier-excluded metrics reported.
- [ ] Outliers identified by ID; no silent deletion.
- [ ] What the sample does not validate is stated.

## 10. Figures

- [ ] 300 dpi PNG and vector PDF.
- [ ] Consistent fonts, colours, panel labels.
- [ ] Scale bar and north arrow on maps.
- [ ] Ward labels legible.
- [ ] Colourblind-friendly palette.
- [ ] Units in axis labels and colourbars.
- [ ] Captions self-contained.
- [ ] No Google Earth imagery redistributed.

## 11. Manuscript

- [ ] Abstract contains data, methods, key numbers, and caveat.
- [ ] Study area and data sources documented.
- [ ] Methods reproducible (parameters, equations, thresholds).
- [ ] Model bias and calibration reported.
- [ ] Seasonal artifact/correction reported.
- [ ] Validation metrics and limitations.
- [ ] Discussion links results to policy and literature.
- [ ] Conclusions do not overclaim.
- [ ] References verified.
- [ ] Data/code availability and licences.
- [ ] Author contributions, funding, conflicts.

## 12. Packaging

- [ ] Data manifest with source, date, resolution, licence, checksum.
- [ ] Scripts and exact run order.
- [ ] README with key numbers and caveats.
- [ ] Small report zip and full data zip separate.
- [ ] GitHub file sizes: <100 MB normal commit; release assets up to 2 GB; web upload 25 MB.
- [ ] No credentials, tokens, or private data.
