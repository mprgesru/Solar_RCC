#!/usr/bin/env python3
"""
Generic summary of building-level rooftop PV results.

Example:
    python summarize_results.py \
        --input base=base.csv \
        --input winter=winter.csv \
        --input premonsoon=premonsoon.csv \
        --out-dir summaries

The script expects columns such as Building_ID, Ward_Name, area_m2,
AREA, MEAN, usable_area_m2, capacity_kWp, elec_MWh, co2_t.
Override names with the CLI options if needed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def gini(x: np.ndarray) -> float:
    x = np.sort(np.asarray(x, dtype=float))
    n = len(x)
    if n == 0 or x.sum() == 0:
        return float("nan")
    cum = np.cumsum(x)
    return float((n + 1 - 2 * np.sum(cum) / cum[-1]) / n)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", action="append", required=True, help="label=path.csv")
    ap.add_argument("--out-dir", default="summaries")
    ap.add_argument("--ward-field", default="Ward_Name")
    ap.add_argument("--area-field", default="area_m2")
    ap.add_argument("--suitable-area-field", default="AREA")
    ap.add_argument("--mean-field", default="MEAN")
    ap.add_argument("--usable-field", default="usable_area_m2")
    ap.add_argument("--capacity-field", default="capacity_kWp")
    ap.add_argument("--generation-field", default="elec_MWh")
    ap.add_argument("--co2-field", default="co2_t")
    ap.add_argument("--id-field", default="Building_ID")
    args = ap.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    ward_rows = []
    first = None
    for item in args.input:
        label, path = item.split("=", 1)
        df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
        if first is None:
            first = df
        suitable = df[df[args.suitable_area_field].notna() & (df[args.suitable_area_field] > 0)]
        summary_rows.append(
            {
                "period": label,
                "buildings_total": len(df),
                "buildings_suitable": len(suitable),
                "suitable_fraction_pct": 100 * len(suitable) / max(len(df), 1),
                "footprint_km2": df[args.area_field].sum() / 1e6,
                "suitable_area_km2": suitable[args.suitable_area_field].sum() / 1e6,
                "usable_area_km2": suitable[args.usable_field].sum() / 1e6,
                "capacity_MWp": suitable[args.capacity_field].sum() / 1000,
                "generation_GWh": suitable[args.generation_field].sum() / 1000,
                "co2_Mt": suitable[args.co2_field].sum() / 1e6,
                "pvout_kwh_kwp": suitable[args.generation_field].sum() * 1000 / max(suitable[args.capacity_field].sum(), 1e-9),
                "mean_poa_kwh_m2": (suitable[args.mean_field]).mean(),
            }
        )
        if args.ward_field in df.columns:
            for ward, g in df.groupby(args.ward_field):
                s = g[g[args.suitable_area_field].notna() & (g[args.suitable_area_field] > 0)]
                ward_rows.append(
                    {
                        "period": label,
                        "ward": ward,
                        "buildings": len(g),
                        "buildings_suitable": len(s),
                        "footprint_km2": g[args.area_field].sum() / 1e6,
                        "usable_area_km2": s[args.usable_field].sum() / 1e6,
                        "capacity_MWp": s[args.capacity_field].sum() / 1000,
                        "generation_GWh": s[args.generation_field].sum() / 1000,
                        "co2_Mt": s[args.co2_field].sum() / 1e6,
                    }
                )

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out / "period_summary.csv", index=False)
    print(summary.to_string(index=False))

    if ward_rows:
        pd.DataFrame(ward_rows).to_csv(out / "ward_summary.csv", index=False)

    if first is not None:
        e = first.loc[
            first[args.suitable_area_field].notna() & (first[args.suitable_area_field] > 0),
            args.generation_field,
        ].sort_values(ascending=False).to_numpy()
        if len(e):
            n = len(e)
            concentration = {
                "gini": gini(e),
                "top_1pct_share_pct": 100 * e[: max(1, int(0.01 * n))].sum() / e.sum(),
                "top_5pct_share_pct": 100 * e[: max(1, int(0.05 * n))].sum() / e.sum(),
                "top_10pct_share_pct": 100 * e[: max(1, int(0.10 * n))].sum() / e.sum(),
                "median_building_MWh": float(np.median(e)),
                "mean_building_MWh": float(np.mean(e)),
            }
            (out / "concentration.json").write_text(json.dumps(concentration, indent=2), encoding="utf-8")
            print(json.dumps(concentration, indent=2))


if __name__ == "__main__":
    main()
