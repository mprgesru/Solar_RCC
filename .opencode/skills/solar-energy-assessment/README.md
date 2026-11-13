# Solar Energy Assessment skill

A reusable OpenCode skill for building-level rooftop solar PV potential assessments.

## What it covers

- boundary/water/built-up masks;
- building footprints and heights;
- canopy, DTM and 2 m DSM;
- ArcGIS Pro `Raster Solar Radiation` (and QGIS/GRASS/Python alternatives);
- base/tutorial/strict scenarios;
- zonal statistics and energy conversion;
- seasonal correction and benchmark calibration;
- 100-building validation;
- whole-city, ward and seasonal analysis;
- publication figures and manuscript structure;
- data licences, QA checklists and reusable prompts.

## Install

### Option A — use it in this repository

The skill is already at:

```text
.opencode/skills/solar-energy-assessment/
```

OpenCode discovers it automatically when working in this repository.

### Option B — copy it into another project

```text
<new-project>/.opencode/skills/solar-energy-assessment/
```

### Option C — reference this repository

In the second project's `opencode.json`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "skills": ["C:/path/to/Solar_RCC/.opencode/skills"]
}
```

`skills` paths are resolved from the active working directory; use an absolute path if needed.

### Option D — global install

```text
~/.config/opencode/skills/solar-energy-assessment/
```

## Use

Mention the skill in a prompt:

```text
@solar-energy-assessment assess rooftop solar potential for <CITY>.
```

Or let OpenCode discover it from the description when the task matches.

## File tree

```text
solar-energy-assessment/
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── references/
│   ├── workflow.md
│   ├── methodology.md
│   ├── data-sources.md
│   ├── qa-checklist.md
│   ├── licenses.md
│   ├── prompt-playbook.md
│   └── figure-style.md
├── templates/
│   ├── arcpy_solar_workflow.py
│   ├── validation_sample.py
│   ├── manuscript_outline.md
│   └── data_manifest.template.csv
├── scripts/
│   ├── validate_geodata.py
│   └── summarize_results.py
└── examples/
    └── rajshahi.md
```

## Version

1.0.0 — 13 November 2026.

## Licence

MIT for the skill files. Dataset licences are documented in `references/licenses.md`.
