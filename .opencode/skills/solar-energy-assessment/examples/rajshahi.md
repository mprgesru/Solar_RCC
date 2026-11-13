# Rajshahi case study

This skill was developed from a building-level rooftop PV assessment of Rajshahi City Corporation (RCC), Bangladesh, completed in November 2026.

## Study area

- RCC, north-western Bangladesh (24.37°N, 88.60°E).
- 30 wards, 6 zones.
- Validated built-up boundary: 46.23 km² gross; 45.44 km² net land; 0.79 km² permanent water.
- WorldCover: 18.36 km² built-up (39.7%), 20.14 km² tree cover (43.6%), 5.23 km² cropland.

## Data

- RCC ward/zone boundaries from the RCC EPI Digital Microplanning ArcGIS FeatureServer.
- Google Open Buildings v3 (106,134 buildings inside RCC).
- GlobalBuildingAtlas LoD1 heights (89,052 GBA buildings; 106,084 matched by largest overlap).
- Meta/WRI 1 m canopy height.
- Copernicus DEM GLO-30.
- ESA WorldCover 2021 and JRC Global Surface Water 2021.
- NASA POWER and Global Solar Atlas/Solargis.
- 100-building Google Earth validation sample across all 30 wards.

## Method

- 2 m DSM = DTM + max(building height, canopy height).
- ArcGIS Pro `Raster Solar Radiation`, annual 2025, Bangladesh Standard Time, diffuse 0.55, transmittivity 0.50, sun map 6, GPU then CPU.
- Base scenario: slope ≤45°, radiation ≥1,000 kWh m⁻², no north exclusion.
- Tutorial: ≥800 kWh m⁻² + north exclusion.
- Strict: ≥1,200 kWh m⁻², no north exclusion.
- Roof factor 0.60; 21.6% efficiency; PR 0.78; 4.63 m² kWp⁻¹; CO₂ 0.65 t MWh⁻¹.
- Seasonal runs corrected by differencing cumulative outputs; benchmark-adjusted profile using Solargis shares.
- Sensitivity on roof factor, efficiency, PR and radiation calibration.

## Headline results

| Metric | Value |
|---|---:|
| Buildings in net-land area | 105,873 |
| Buildings with suitable cells | 90,807 (85.8%) |
| Footprint area | 8.59 km² |
| Suitable roof area | 3.93 km² |
| Usable roof area | 2.36 km² |
| Installed capacity | 509.5 MWp |
| Generation, uncalibrated | 821.2 GWh yr⁻¹ |
| Generation, benchmark-calibrated | 727.3 GWh yr⁻¹ |
| CO₂, uncalibrated | 0.534 Mt yr⁻¹ |
| CO₂, calibrated | 0.473 Mt yr⁻¹ |
| PVOUT, model | 1,611.9 kWh kWp⁻¹ yr⁻¹ |
| PVOUT, Solargis | 1,427.6 kWh kWp⁻¹ yr⁻¹ |
| Top 5 wards' share | 35.2% |
| Top 10% buildings' share | 40.9% |
| Gini coefficient | 0.553 |
| Tutorial scenario | 782.8 GWh (−4.7%) |
| Strict scenario | 820.2 GWh (−0.12%) |

## Key lessons

- A valid boundary is essential. Ward 18 had a self-intersection; repairing it changed no building's ward but fixed the maps.
- The 2 m DSM is a LoD1 flat-top surface. It is appropriate for flat RCC roofs but not for pitched/tin roofs.
- A blanket north-facing exclusion reduced generation by 4.7%, but the effect varied from 1.4% to 9.3% by ward. It should be a scenario, not the base rule.
- The strict 1,200 kWh m⁻² threshold was almost non-binding; the mean irradiation on suitable cells was about 2,015 kWh m⁻². Economic thresholds are more meaningful.
- The raw ArcGIS model was 12.9% above the Solargis PVOUT. Benchmark calibration reduced the annual estimate to 727 GWh.
- The delivered seasonal runs were cumulative from 1 January. Differencing recovered season-specific values; the model still overestimated monsoon by 39% relative to Solargis, so a benchmark-adjusted profile was also reported.
- Robust validation: footprint-area MAPE 3.7%, height RMSE 1.27 m after excluding two outliers. All 100 sampled roofs were flat RCC, so pitched/tin roofs and shading were not validated.

## Links

- Manuscript and report: GitHub release `RCC_Solar-results` in `https://github.com/mprgesru/Solar_RCC`.
- Data package: `solar_summary.zip` release asset.
- Code: project scripts and this skill.
