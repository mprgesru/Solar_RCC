# Solar_RCC

Rajshahi rooftop solar PV assessment and a reusable OpenCode skill for building-level solar potential analysis.

## Contents

| Path | Description |
|---|---|
| `.opencode/skills/solar-energy-assessment/` | Reusable skill for city-scale rooftop PV assessments |
| `Rajshahi_Solar.gdb/` | Validated RCC boundary and 30 wards (`main_rcc_boundary`, `main_rcc_wards`) |
| `validation_sample_100.csv` | 100-building validation sample |

## Solar Energy Assessment skill

Start with:

```text
.opencode/skills/solar-energy-assessment/SKILL.md
```

The skill covers:

- boundary/water/built-up masks and topology QA;
- building footprints, heights and confidence flags;
- canopy, DTM and 2 m DSM construction;
- ArcGIS Pro `Raster Solar Radiation` and open-source alternatives;
- base/tutorial/strict scenarios;
- zonal statistics and energy conversion;
- seasonal correction and benchmark calibration;
- 100-building validation;
- whole-city, ward and seasonal analysis;
- publication figures and manuscript structure;
- data licences, QA checklists and reusable prompts.

### Use in another project

Copy the folder:

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

## Results

The manuscript, figures, tables and data package are in the release:

```
https://github.com/mprgesru/Solar_RCC/releases/tag/RCC_Solar-results
```

Headline result: 509.5 MWp technical capacity, 821.2 GWh yr⁻¹ uncalibrated, 727.3 GWh yr⁻¹ benchmark-calibrated, and 0.47–0.53 Mt CO₂ yr⁻¹.

## Licence

Skill files: MIT. Dataset licences are documented in
`.opencode/skills/solar-energy-assessment/references/licenses.md`.
Google Earth imagery is not redistributed.
