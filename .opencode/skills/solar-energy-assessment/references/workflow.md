# Workflow

Detailed phase-by-phase procedure for a building-level rooftop PV assessment. Adapt paths, dates, thresholds and scenario names to the project.

## Phase 0 — Scope and decisions

Record these in `docs/project_scope.md`:

- study boundary and whether water is excluded;
- pilot area vs whole city;
- target resolution (0.5–2 m; 2 m is a practical city-wide compromise);
- software stack (ArcGIS Pro + Spatial Analyst, QGIS + GRASS, or Python);
- validation design (field, drone, Google Earth, remote sensing only);
- scenarios and thresholds;
- outputs (technical potential only, or economics/policy too);
- data licences and redistribution constraints.

Ask the user before assuming a north-facing exclusion, a minimum roof size, or a fixed performance ratio.

## Phase 1 — Boundary, water and built-up mask

1. Obtain boundary and ward polygons. If using an ArcGIS FeatureServer, query with `f=geojson` and `outSR=4326`.
2. Project to a local projected CRS in metres (UTM zone or national grid).
3. Validate:
   - `geometry.is_valid`;
   - ward count and names;
   - overlaps and gaps;
   - boundary vs ward union symmetric difference.
4. Repair invalid wards (`Repair Geometry` in ArcGIS Pro, `make_valid`/`buffer(0)` in Python), then dissolve repaired wards to the boundary.
5. Remove permanent water polygons (ESA WorldCover class 80, JRC occurrence ≥50%, or local water data) to create a net-land boundary.
6. Compute built-up/tree/cropland fractions for context.
7. Save a QA report with gross area, water area, net land area, ward count, validity and symmetric differences.

**Do not** proceed to mapping with an invalid ward layer. A valid boundary is a prerequisite for credible ward statistics.

## Phase 2 — Building footprints

1. Download the finest available footprints:
   - Google Open Buildings v3 (country/S2 tile);
   - Microsoft GlobalMLBuildingFootprints;
   - OSM/HOT;
   - local cadastre if available.
2. Clip to the boundary plus a small margin.
3. Conflate:
   - use the best source as the primary geometry;
   - add missing polygons from secondary sources;
   - remove duplicates by overlap/IoU;
   - keep `source`, `confidence`, `area_m2`.
4. Create a unique `Building_ID` (e.g., `CITY_000001`).
5. Flag small structures and low-confidence footprints rather than deleting them silently.
6. Correct obvious errors against very-high-resolution imagery for a sample.

## Phase 3 — Heights

1. Obtain per-building heights:
   - GlobalBuildingAtlas LoD1 Parquet (query with DuckDB to avoid downloading the full 5° tile);
   - Open Buildings 2.5D;
   - LiDAR/drone/stereo DSM;
   - OSM `building:levels` as a fallback.
2. Assign heights by largest polygon overlap:
   - spatial join + intersection area;
   - keep the GBA polygon with the largest overlap;
   - fallback to nearest within 15 m;
   - fallback to ward/size median.
3. Retain:
   - `height_m`;
   - `height_var`;
   - `height_source`;
   - `height_confidence` (high/medium/low).
4. Flag blocky high-variance outliers. For the DSM only, cap at a plausible maximum (e.g., 45 m) above the 99.9th percentile. Keep raw heights.
5. Validate against a sample of observed floors/heights.

## Phase 4 — Canopy, DTM and DSM

1. Mosaic canopy tiles (Meta/WRI 1 m or ETH 10 m) and reproject to the analysis grid.
2. Reproject the DTM (Copernicus GLO-30, FABDEM, or LiDAR DTM) to the same grid.
3. Rasterise building footprints with assigned heights.
4. Compute:
   `DSM = DTM + max(building_height, canopy_height)`.
5. Save:
   - `dsm_<city>_<res>m.tif`;
   - `ndsm_<city>_<res>m.tif`;
   - `slope_<city>_<res>m.tif`;
   - `aspect_<city>_<res>m.tif`.
6. QA:
   - same shape/transform/CRS for all rasters;
   - no negative surface heights;
   - building pixels count matches footprint area;
   - canopy fraction is plausible.
7. Document that a LoD1 DSM is flat-topped. It resolves height and shading but not roof pitch.

## Phase 5 — Solar radiation

### ArcGIS Pro

Use `Raster Solar Radiation` (Spatial Analyst).

Typical annual parameters:

- Input surface: DSM.
- Start/end: a representative year, e.g. 1 Jan–31 Dec.
- Time zone: local Windows time-zone name (e.g. `Bangladesh Standard Time`).
- Analysis mask: building footprints (annual) or annual suitable cells (seasonal).
- Slope/aspect: precomputed rasters (performance).
- Diffuse proportion: local diffuse fraction (e.g. 0.55).
- Transmittivity: calibrate to local GHI/GTI (e.g. 0.50).
- Sun map grid level: 6 for ≤4 m cells.
- Target device: GPU then CPU.
- `use_time_interval=False` for a single total; `interval_unit="Day"`, `interval=14` annual / 7 seasonal.
- Output: annual radiation raster (kWh m⁻²).

### QGIS/GRASS fallback

- `r.horizon` for horizon maps.
- `r.sun` for direct/diffuse/reflected radiation.
- Sum daily/hourly outputs for annual totals.
- Validate against Solargis.

### Python fallback

- `pvlib` for point or roof-plane transposition.
- `pysolar`/`sunposition` for solar geometry.
- `rasterio` + `numpy` for slope/aspect and simple horizon checks.
- Not a substitute for a full urban solar model unless carefully validated.

### QA

- Annual mean POA should be within ~20% of Solargis GTI; if not, calibrate.
- Check north-facing vs south-facing roof values.
- Check shaded vs open roofs.
- Check max values (walls/south-facing surfaces may be high).

## Phase 6 — Suitability and zonal statistics

1. Build suitability rasters:
   - base: slope ≤45°, radiation ≥ threshold, no north exclusion;
   - tutorial: lower threshold + north exclusion;
   - strict: higher threshold, no north exclusion;
   - optional economic: LCOE/payback filter.
2. Use `Con`/Raster Calculator with explicit flat-cell handling:
   `(aspect == -1) | ((aspect > 22.5) & (aspect < 337.5)) | (slope <= 10)`.
3. `Zonal Statistics as Table` per building:
   - zone field: `Building_ID`;
   - value: suitability raster;
   - statistics: `ALL` (at least `AREA`, `MEAN`, `SUM`, `COUNT`).
4. Copy buildings to a result feature class.
5. `Join Field` with `AREA`, `MEAN`, `SUM`, `COUNT`.
6. Add fields and calculate with `UpdateCursor`:
   - `roof_factor` (e.g. 0.60);
   - `usable_area_m2 = AREA × roof_factor`;
   - `capacity_kWp = usable_area_m2 / 4.63` (at 21.6%);
   - `incident_MWh = usable_area_m2 × MEAN / 1000`;
   - `elec_MWh = incident_MWh × η × PR`;
   - `co2_t = elec_MWh × EF`;
   - `scenario`.
7. Export CSV to a folder; never to a `.gdb` path.

## Phase 7 — Seasonal analysis

1. Define seasons, e.g.:
   - winter: Jan–Feb;
   - pre-monsoon: Mar–May;
   - monsoon: Jun–Sep;
   - post-monsoon: Oct–Dec.
2. Use the annual suitable raster as the analysis mask so every season uses the same usable roof area.
3. Run `Raster Solar Radiation` separately for each season.
4. **Check for cumulative outputs.** If all seasonal totals increase monotonically and the last equals the annual total, the runs started on 1 January. Recover seasonal values by differencing consecutive cumulative totals at building level.
5. Sum seasons and compare with annual. Accept ~90–110%; if further off, check dates, mask and time step.
6. Compare seasonal shares with Solargis PVOUT shares. If the model overweights monsoon, construct a benchmark-adjusted seasonal profile using Solargis shares applied to the calibrated annual total.
7. Report both raw-corrected and benchmark-adjusted profiles.

## Phase 8 — Validation

1. Draw a stratified random sample:
   - strata: ward × size class (small/medium/large);
   - base: one per non-empty stratum;
   - extras to reach the target (e.g. 100);
   - record seed and sampling weights.
2. Validate in Google Earth/field:
   - imagery date;
   - footprint area;
   - observed floors/height;
   - roof type and condition;
   - obstructions;
   - tree and neighbour shade;
   - existing PV;
   - usable-roof percentage;
   - suitability;
   - confidence;
   - notes.
3. Compute:
   - area bias, MAE, RMSE, MAPE, median and p95 absolute percentage error;
   - height bias, MAE, RMSE, median/p95 absolute error, correlation;
   - roof-type accuracy/kappa if more than one class;
   - completeness/omission notes.
4. Report full-sample and outlier-excluded metrics. Identify likely wrong-building/measurement mismatches; do not silently delete them.
5. State what the sample does **not** validate (e.g. all roofs flat, shading fields missing).

## Phase 9 — Analysis and manuscript

1. Whole-city totals.
2. Ward table:
   - buildings, suitable buildings, suitable fraction;
   - footprint, suitable/usable area;
   - capacity, generation, CO₂;
   - generation density and capacity density.
3. Seasonal table and ward × season matrix.
4. Scenario comparison and north-filter effect.
5. Sensitivity (roof factor, PR, efficiency, radiation calibration).
6. Concentration (Gini, top shares) and building-size/height-confidence contributions.
7. Figures and tables (see `figure-style.md`).
8. Manuscript outline (see `templates/manuscript_outline.md`).
9. Data and code availability, licences, limitations.

## Phase 10 — Packaging

- Write a data manifest with source, date, resolution, licence and checksum.
- Save scripts and a README with exact run order.
- Provide a small report zip and a full data zip separately.
- For GitHub:
  - commit files <100 MB normally;
  - use release assets up to 2 GB for large packages;
  - remember the web upload limit is 25 MB per file.
- For a Linux agent, upload files or use GitHub; it cannot read a local `C:\` path.
