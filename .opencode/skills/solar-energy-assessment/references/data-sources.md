# Data sources

Use the finest, most recent open data available. Record the source, date, resolution, licence and preprocessing for every dataset.

## Boundaries and administrative units

| Source | Use | Access | Licence |
|---|---|---|---|
| City corporation / municipality GIS | Official boundary, wards | Local GIS office or open data portal | Check with authority |
| ArcGIS FeatureServer / dashboard | Operational ward boundaries | ArcGIS REST query (`f=geojson`, `outSR=4326`) | Public dashboard; confirm redistribution |
| OpenStreetMap | Boundary and ward polygons | https://www.openstreetmap.org | ODbL |
| HDX / OCHA admin boundaries | District/upazila context | https://data.humdata.org | Check dataset |

**Always validate topology** and dissolve repaired wards to the boundary.

## Building footprints

| Source | Resolution / format | Access | Licence |
|---|---|---|---|
| Google Open Buildings v3 | AI-derived polygons, ~0.5–2 m source imagery; CSV/S2 tiles | https://sites.research.google/gr/open-buildings/ | CC BY 4.0 |
| Open Buildings 2.5D Temporal | 4 m height/presence, 2016–2023 | https://sites.research.google/gr/open-buildings/temporal | CC BY 4.0 |
| Microsoft GlobalMLBuildingFootprints | Polygons | https://github.com/microsoft/GlobalMLBuildingFootprints | ODbL |
| OSM / HOT | Polygons, attributes | https://data.humdata.org / Geofabrik | ODbL |
| Local cadastre | Authoritative footprints | City authority | Check |

Conflate sources; keep a unique ID and confidence.

## Building heights / 3D

| Source | Resolution | Access | Licence |
|---|---|---|---|
| GlobalBuildingAtlas LoD1 | 3 m height raster; per-building LoD1 | https://github.com/zhu-xlab/GlobalBuildingAtlas | CC BY-NC 4.0 |
| Open Buildings 2.5D | 4 m | Google Earth Engine / GCS | CC BY 4.0 |
| LiDAR / drone / stereo DSM | 0.05–1 m | Local survey | Check |
| OSM `building:levels` | Attribute | OSM | ODbL |

GBA Parquet tiles can be queried remotely with DuckDB (`read_parquet`) using a bbox filter; avoid downloading a 4 GB tile when only a city is needed.

## Canopy and vegetation

| Source | Resolution | Access | Licence |
|---|---|---|---|
| Meta/WRI global canopy height | 1 m | AWS Open Data (`dataforgood-fb-data`) | CC BY 4.0 |
| ETH Global Canopy Height 2020 | 10 m | https://langnico.github.io/globalcanopyheight | CC BY 4.0 |
| Local LiDAR | <1 m | Local survey | Check |

Tree shading is a first-order control in tropical and subtropical cities. Do not omit canopy.

## Terrain

| Source | Resolution | Access | Licence |
|---|---|---|---|
| Copernicus DEM GLO-30 | 30 m | https://dataspace.copernicus.eu / AWS | Free, attribution |
| FABDEM | 30 m | University of Bristol | Check non-commercial terms |
| SRTM | 30 m | NASA/USGS | Public |
| LiDAR DTM | <1 m | Local survey | Check |

A 30 m DEM is a DTM only. It is not a rooftop DSM.

## Land cover and water

| Source | Resolution | Access | Licence |
|---|---|---|---|
| ESA WorldCover 2021 | 10 m | https://esa-worldcover.org | CC BY 4.0 |
| JRC Global Surface Water 2021 | 30 m | https://global-surface-water.appspot.com | Free, attribution |
| Local land-use maps | Varies | City/planning authority | Check |

## Solar resource and benchmarks

| Source | Data | Access | Licence |
|---|---|---|---|
| NASA POWER | GHI, DNI, DHI, temperature, climatology | https://power.larc.nasa.gov | Public |
| Global Solar Atlas / Solargis | GHI, DNI, DIF, GTI, PVOUT, optimum tilt | https://globalsolaratlas.info | Attribution; check terms |
| PVGIS | PVOUT, monthly profiles | https://re.jrc.ec.europa.eu/pvg_tools/ | Free, attribution |
| BMD / local station | Sunshine, temperature, radiation | Bangladesh Meteorological Department | Check |
| Local pyranometer | Ground truth | Research/utility station | Check |

Use at least two independent sources for calibration/validation.

## Validation imagery

| Source | Use | Restriction |
|---|---|---|
| Google Earth / Google Maps | Footprint, roof type, height, obstructions | Do not redistribute imagery; record date |
| Maxar / Planet / high-resolution satellite | Visual validation | Licence-dependent |
| Drone/UAV | DSM and roof validation | CAAB permission/no-fly zones |
| Street View | Facade/floor counting | Coverage-dependent |

## Typical city data checklist

- [ ] Official boundary and wards (validated topology)
- [ ] Building footprints (conflated, unique ID)
- [ ] Building heights (per building, confidence flags)
- [ ] Canopy height
- [ ] DTM
- [ ] Land cover / water
- [ ] NASA POWER + Global Solar Atlas/Solargis
- [ ] Local module/inverter/tariff data
- [ ] Validation imagery/sample
- [ ] Data licences and attribution text
