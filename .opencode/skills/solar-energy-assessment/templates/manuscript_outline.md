# Manuscript outline

Use this as a structural template for a rooftop PV assessment paper. Replace bracketed text.

## Title

Rooftop solar photovoltaic potential of [CITY]: a building-level geospatial assessment

## Abstract

- Context: energy demand, renewable targets, data scarcity.
- Objective: estimate technical rooftop PV potential.
- Data and methods: boundary, footprints, heights, canopy, DTM, 2 m DSM, solar model, scenarios, validation.
- Key results: buildings, usable area, MWp, GWh yr⁻¹, CO₂, concentration, seasonal range.
- Caveats: model bias, calibration, flat roofs, validation limits.
- Conclusion and policy relevance.

## Keywords

rooftop solar; urban energy; GIS; building heights; [COUNTRY]; solar radiation modelling; energy transition

## 1. Introduction

1. National energy and climate context.
2. Why city-scale rooftop assessments matter.
3. Data and methodological gaps (coarse DEMs, missing heights, arbitrary north exclusion, uncalibrated models, weak validation).
4. Study objectives.

## 2. Study area and data

### 2.1 Study area

- Location, boundary, wards, area, land cover, climate, solar resource.

### 2.2 Data sources

- Table: dataset, source, resolution, use, licence.
- Boundary, footprints, heights, canopy, DTM, land cover, water, solar benchmarks, validation imagery.

## 3. Methods

### 3.1 Boundary, water and built-up mask

- Topology validation, water removal, net land, land-cover fractions.

### 3.2 Building footprints

- Sources, conflation, unique ID, confidence, completeness.

### 3.3 Building heights

- GBA/Open Buildings/LiDAR, assignment, variance, confidence, cap.

### 3.4 Canopy, DTM and DSM

- Mosaic, reprojection, DSM equation, LoD1 limitation.

### 3.5 Solar radiation

- ArcGIS Raster Solar Radiation parameters, time zone, diffuse/transmittivity, sun map, GPU.
- QGIS/GRASS/Python alternatives.

### 3.6 Suitability scenarios

- Base, tutorial-style, strict, optional economic.
- Flat-roof rationale; north exclusion as scenario.

### 3.7 Energy conversion

- Equations, roof factor, efficiency, PR, module area, CO₂ factor.

### 3.8 Seasonal analysis

- Season definitions, annual suitable mask, cumulative-start correction, benchmark adjustment.

### 3.9 Validation

- Stratified sample, metrics, outliers, what is not validated.

### 3.10 Sensitivity and uncertainty

- Roof factor, efficiency, PR, radiation calibration, combined range.

## 4. Results

### 4.1 Whole-city technical potential

- Buildings, suitable fraction, footprint, suitable/usable area, MWp, GWh, CO₂, PVOUT, POA.
- Raw and benchmark-calibrated.

### 4.2 Ward-wise patterns

- Top/bottom total generation; top/bottom density; correlations; map.
- Policy distinction: aggregate capacity vs intensification.

### 4.3 Seasonal variation

- Corrected model profile; Solargis shares; benchmark-adjusted profile; ward heatmap/maps.

### 4.4 Scenario comparison and north-facing issue

- Base/tutorial/strict; capacity/generation deltas; ward-level north-filter effect.
- Why strict threshold may be non-binding.

### 4.5 Validation

- Area MAPE/RMSE; height RMSE/correlation; full vs robust; roof type/condition; missing data.

### 4.6 Sensitivity and calibration

- One-at-a-time and combined; calibrated central estimate.

### 4.7 Concentration and building-size effects

- Gini; top 1/5/10%; size class shares; height-confidence shares.

## 5. Discussion

### 5.1 Methodological insights

- LoD1 vs pitched roofs.
- North-facing rule.
- Arbitrary thresholds.
- Model bias and seasonal structure.
- Validation.

### 5.2 Comparison with national/regional evidence

- National rooftop potential; city share; order-of-magnitude comparison.
- Differences in boundary, roof factor, thresholds, PR.

### 5.3 Policy implications

- Priority wards for aggregate capacity.
- Dense central wards for intensification.
- Large/medium buildings first; small buildings for equity.
- Grid, net metering, storage, seasonal planning.
- Data investment: heights, roof type, drone/stereo DSM.

### 5.4 Limitations

- Flat roofs, height uncertainty, footprint vintage, roof type/use, model bias, seasonal correction, no ground-truth yield, technical potential only, boundary/licence, CO₂ factor.

### 5.5 Future research

- Drone/stereo DSM; roof/use classification; pyranometer calibration; LCOE/demand; Monte Carlo; other cities.

## 6. Conclusions

- 4–6 numbered conclusions with key numbers and caveats.

## References

- Data sources, methods, national context, validation, policy.

## Figure captions

- Study area; annual potential; ward ranking; seasonal city; seasonal heatmap; scenarios; validation; sensitivity; concentration; workflow; seasonal maps.

## Tables

- Data sources; parameters; whole-city results; seasonal results; top/bottom wards; validation; sensitivity; size/height contributions.

## Data and code availability

- Repository, release asset, licences, Google Earth restriction.

## Acknowledgements

- Boundary authority, data providers, validation support.
