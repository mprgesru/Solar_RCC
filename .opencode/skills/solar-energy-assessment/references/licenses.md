# Licences and attribution

This is a practical guide, not legal advice. Check the original licence page before publishing or redistributing data.

## Common dataset licences

| Dataset | Licence | Redistribution | Key conditions |
|---|---|---|---|
| Google Open Buildings | CC BY 4.0 | Yes | Attribution; indicate changes |
| GlobalBuildingAtlas | CC BY-NC 4.0 | Yes, non-commercial | Attribution; no commercial use; cite Zhu et al. (2025) |
| Meta/WRI canopy height | CC BY 4.0 | Yes | Attribution |
| ESA WorldCover | CC BY 4.0 | Yes | Attribution |
| Copernicus DEM | Free, attribution | Yes | Attribution; check ESA terms |
| JRC Global Surface Water | Free, attribution | Yes | Attribution |
| NASA POWER | Public | Yes | Acknowledge NASA |
| Global Solar Atlas / Solargis | Attribution; check terms | Usually yes with attribution | Do not imply Solargis endorsement; check commercial use |
| OpenStreetMap | ODbL | Yes | Attribution; share-alike for derived databases |
| Google Earth / Google Maps imagery | Proprietary | **No** | Visual validation only; do not redistribute imagery |
| Maxar / Planet / commercial VHR | Commercial | No unless licensed | Check licence |
| City boundary from a public dashboard | Often unspecified | Confirm with authority | Public viewing does not automatically mean redistribution rights |

## Recommended attribution text

> Building footprints: Google Open Buildings v3 (CC BY 4.0). Building heights: GlobalBuildingAtlas (CC BY-NC 4.0; Zhu et al., 2025). Canopy height: Meta/WRI (CC BY 4.0). Land cover: ESA WorldCover 2021 (CC BY 4.0). Surface water: JRC Global Surface Water (2021). Terrain: Copernicus DEM GLO-30. Solar resource: NASA POWER and Global Solar Atlas/Solargis. Validation imagery: Google Earth (not redistributed).

## Sharing derived data

- Derived rasters and tables may inherit the most restrictive input licence.
- If GBA (CC BY-NC 4.0) is used, the derived package should be treated as non-commercial.
- If OSM is used, ODbL share-alike may apply to derived databases; consult the ODbL.
- Do not upload Google Earth screenshots or imagery to a public repository.
- For a public repository, include a `DATA_LICENSES.md` with the matrix above.
- For a private repository, still document the licences for internal compliance.

## Code licence

Use MIT for scripts and templates unless the project requires otherwise. Include:

```
MIT License

Copyright (c) <year> <author>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

## Citation guidance

For the GBA:

> Zhu, X. X., Chen, S., Zhang, F., Shi, Y., & Wang, Y. (2025). GlobalBuildingAtlas: an open global and complete dataset of building polygons, heights and LoD1 3D models. Earth System Science Data, 17, 6647–6668. https://doi.org/10.5194/essd-17-6647-2025

For the canopy:

> Lang, N., Jetz, W., Schindler, K., & Wegner, J. D. (2023). A high-resolution canopy height model of the Earth. Nature Ecology & Evolution. https://doi.org/10.1038/s41559-023-02206-6

For Open Buildings:

> Sirko, W., et al. (2023). High-resolution building and road detection from Sentinel-2. arXiv:2310.11622.
