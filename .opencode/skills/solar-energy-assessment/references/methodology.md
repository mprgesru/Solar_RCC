# Methodology

## 1. Study area and boundary

Use a locally projected CRS in metres (UTM zone or national grid). Report:

- gross boundary area;
- permanent water area;
- net land area;
- built-up, tree, cropland and bare fractions;
- ward count and zone count.

Validate topology before analysis. Dissolve repaired wards to a boundary; do not use a ward layer with self-intersections.

## 2. Building footprints

- Primary source: Google Open Buildings v3 (CC BY 4.0), Microsoft (ODbL), OSM (ODbL), or local cadastre.
- Conflate sources; keep a unique `Building_ID`.
- Keep `source`, `confidence`, `area_m2`.
- Flag small structures and low-confidence footprints.

## 3. Building heights

Prefer per-building heights:

- GlobalBuildingAtlas LoD1 (CC BY-NC 4.0);
- Open Buildings 2.5D (4 m);
- LiDAR/drone/stereo DSM;
- OSM `building:levels × 3 m` as fallback.

Assign by largest polygon overlap. Fallbacks:

1. nearest GBA within 15 m;
2. ward × size-class median.

Retain `height_m`, `height_var`, `height_source`, `height_confidence`.

Cap DSM heights at a plausible maximum (e.g. 45 m) only if blocky high-variance outliers are present. Keep raw `height_m`.

## 4. 3D surface

**DSM = DTM + max(building height, canopy height)**

- DTM: Copernicus GLO-30, FABDEM, or LiDAR DTM.
- Canopy: Meta/WRI 1 m or ETH 10 m.
- Resolution: 0.5–2 m. Use 2 m for city-wide work unless a pilot justifies 1 m.
- Slope/aspect from the DSM.

A LoD1 DSM is flat-topped. It captures height, footprint, and shading, but not roof pitch. Slope/aspect at building edges is dominated by vertical walls; do not use raw slope to exclude roofs.

## 5. Solar radiation

ArcGIS Pro `Raster Solar Radiation` computes incoming insolation per cell.

Parameters to report:

| Parameter | Typical value | Notes |
|---|---|---|
| Surface | 2 m DSM | projected CRS, metres |
| Period | 1 Jan–31 Dec (representative year) | TMY or long-term average preferred |
| Time zone | local Windows name (e.g. Bangladesh Standard Time) | UTC+6 for Bangladesh |
| Analysis mask | buildings (annual); annual suitable cells (seasonal) | mask limits output, not shading |
| Slope/aspect | precomputed | improves performance |
| Diffuse proportion | local diffuse fraction (e.g. 0.55) | 0.3 is a mid-latitude/clear-sky default |
| Transmittivity | calibrate to local GHI/GTI (e.g. 0.50) | inverse relationship with diffuse |
| Sun map grid level | 6 for ≤4 m cells | 5 for >4 m |
| Time interval | annual: 14 days; seasonal: 7 days | `use_time_interval=False` for a single total |

Output units: kWh m⁻² per period.

### Model calibration

Compare modelled annual GHI/POA/PVOUT with:

- NASA POWER;
- Global Solar Atlas/Solargis;
- BMD or a local pyranometer.

If the model is high by a factor *f* = PVOUT_model / PVOUT_benchmark, report:

- raw generation;
- calibrated generation = raw / *f*;
- calibrated CO₂ = raw CO₂ / *f*.

Do not hide the raw model. Report both and label the calibrated result as a central estimate.

## 6. Suitability scenarios

### Base (recommended primary)

- slope ≤45°;
- annual radiation ≥ local threshold (e.g. 1,000 kWh m⁻²);
- no north-facing exclusion.

### Tutorial-style (comparison)

- slope ≤45°;
- radiation ≥800 kWh m⁻²;
- north exclusion:
  - exclude aspects 337.5°–22.5°;
  - retain flat cells (aspect = −1);
  - retain slope ≤10° cells.

### Strict

- slope ≤45°;
- radiation ≥1,200 kWh m⁻²;
- no north exclusion.

### Optional economic

- LCOE ≤ retail tariff or payback ≤ target;
- or radiation ≥ a distribution-derived threshold.

## 7. Energy conversion

For each building:

**A_usable = A_suitable × f_roof**

**P_kWp = A_usable / A_module_per_kWp**

**E_inc = A_usable × H_POA / 1000**  (MWh)

**E_AC = E_inc × η × PR**

**CO₂ = E_AC × EF**

Typical values:

| Parameter | Base | Range |
|---|---:|---:|
| Roof factor `f_roof` | 0.60 | 0.45–0.75 |
| Module efficiency `η` | 0.216 | 0.19–0.23 |
| Performance ratio `PR` | 0.78 | 0.72–0.83 |
| Module area per kWp | 4.63 m² kWp⁻¹ | depends on efficiency |
| Grid emission factor `EF` | 0.65 t CO₂ MWh⁻¹ | use national factor |

**A_usable** accounts for parapets, stairwells, water tanks, AC units, setbacks, and row spacing.

## 8. Seasonal analysis

Define seasons consistently, e.g.:

- winter: Jan–Feb;
- pre-monsoon: Mar–May;
- monsoon: Jun–Sep;
- post-monsoon: Oct–Dec.

Use the annual suitable raster as the seasonal analysis mask so the usable area is constant.

### Cumulative-start check

If seasonal totals increase monotonically and the last equals the annual total, the runs started on 1 January. Recover season-specific values:

**E_winter = E_Jan–Feb**

**E_pre = E_Jan–May − E_Jan–Feb**

**E_monsoon = E_Jan–Sep − E_Jan–May**

**E_post = E_Jan–Dec − E_Jan–Sep**

Check that the seasonal sum is ~90–110% of the annual total.

### Benchmark adjustment

If model seasonal shares differ strongly from Solargis PVOUT shares:

**E_season,adjusted = E_annual,calibrated × share_Solargis,season**

Report both the corrected model and the benchmark-adjusted profile.

## 9. Validation metrics

For footprint area:

- bias = mean(Google − GIS);
- MAE = mean(|difference|);
- RMSE = sqrt(mean(difference²));
- MAPE = mean(|difference| / Google × 100);
- median and p95 absolute percentage error.

For height:

- bias, MAE, RMSE, median/p95 absolute error;
- Pearson correlation.

For roof type:

- confusion matrix;
- overall accuracy;
- Cohen's kappa (if more than one class).

Report full-sample and outlier-excluded metrics. Identify outliers by ID and explain why.

## 10. Sensitivity

One-at-a-time and combined:

- roof factor 0.45/0.60/0.75;
- efficiency 0.19/0.216/0.23;
- PR 0.72/0.78/0.83;
- radiation calibration factor;
- optional Monte Carlo for P10/P50/P90.

## 11. Limitations to state

1. LoD1 flat roofs; no roof pitch.
2. Height uncertainty and capped outliers.
3. Footprint vintage and completeness.
4. Roof type/use not available city-wide.
5. Solar-model bias; benchmark calibration is a uniform scaling, not physical calibration.
6. Seasonal model bias; cumulative correction is a workaround.
7. No ground-truth PV yield.
8. Technical potential only; no LCOE, tariffs, ownership, structural or market constraints.
9. Boundary/licence limitations.
10. CO₂ factor assumption.
