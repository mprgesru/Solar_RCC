#!/usr/bin/env python3
"""
Generic geodata QA for a rooftop PV assessment.

Example:
    python validate_geodata.py \
        --boundary boundary.gpkg --boundary-layer rcc_boundary \
        --wards wards.gpkg --wards-layer rcc_wards \
        --buildings buildings.gpkg --buildings-layer buildings \
        --dsm dsm_2m.tif --slope slope_2m.tif --aspect aspect_2m.tif \
        --id-field Building_ID --height-field height_m
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import shapely


def load(path: str, layer: str | None = None) -> gpd.GeoDataFrame:
    return gpd.read_file(path, layer=layer) if layer else gpd.read_file(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boundary", required=True)
    ap.add_argument("--boundary-layer", default=None)
    ap.add_argument("--wards", required=True)
    ap.add_argument("--wards-layer", default=None)
    ap.add_argument("--buildings", required=True)
    ap.add_argument("--buildings-layer", default=None)
    ap.add_argument("--dsm", required=True)
    ap.add_argument("--slope", default=None)
    ap.add_argument("--aspect", default=None)
    ap.add_argument("--id-field", default="Building_ID")
    ap.add_argument("--height-field", default="height_m")
    ap.add_argument("--out", default="qa_report.json")
    args = ap.parse_args()

    issues: list[str] = []
    report: dict = {}

    boundary = load(args.boundary, args.boundary_layer)
    wards = load(args.wards, args.wards_layer)
    buildings = load(args.buildings, args.buildings_layer)

    if boundary.crs is None or not boundary.crs.is_projected:
        issues.append("boundary is not in a projected CRS")
    if wards.crs is None or not wards.crs.is_projected:
        issues.append("wards are not in a projected CRS")
    if buildings.crs is None or not buildings.crs.is_projected:
        issues.append("buildings are not in a projected CRS")

    if not wards.geometry.is_valid.all():
        issues.append(f"invalid ward geometries: {int((~wards.geometry.is_valid).sum())}")
    if wards.geometry.is_empty.any():
        issues.append("empty ward geometries")
    if buildings.geometry.is_valid.sum() != len(buildings):
        issues.append(f"invalid building geometries: {int((~buildings.geometry.is_valid).sum())}")
    if buildings[args.id_field].duplicated().any():
        issues.append("duplicate Building_ID values")

    ward_union = wards.geometry.union_all()
    boundary_geom = boundary.geometry.union_all()
    symdiff = boundary_geom.symmetric_difference(ward_union).area / 1e6
    if symdiff > 0.02 * (boundary_geom.area / 1e6):
        issues.append(f"boundary/ward union symmetric difference is large: {symdiff:.4f} km2")

    height_missing = int(buildings[args.height_field].isna().sum()) if args.height_field in buildings.columns else len(buildings)
    if args.height_field not in buildings.columns:
        issues.append(f"missing height field: {args.height_field}")
    elif height_missing / max(len(buildings), 1) > 0.10:
        issues.append(f"height missing for {height_missing}/{len(buildings)} buildings")

    report["boundary"] = {
        "count": int(len(boundary)),
        "area_km2": round(float(boundary_geom.area / 1e6), 4),
        "valid": bool(boundary.geometry.is_valid.all()),
    }
    report["wards"] = {
        "count": int(len(wards)),
        "area_km2": round(float(wards.geometry.area.sum() / 1e6), 4),
        "union_km2": round(float(ward_union.area / 1e6), 4),
        "valid": bool(wards.geometry.is_valid.all()),
        "boundary_symdiff_km2": round(float(symdiff), 6),
    }
    report["buildings"] = {
        "count": int(len(buildings)),
        "footprint_km2": round(float(buildings.geometry.area.sum() / 1e6), 4),
        "duplicate_ids": int(buildings[args.id_field].duplicated().sum()),
        "invalid_geometry": int((~buildings.geometry.is_valid).sum()),
        "height_missing": height_missing,
        "height_p50": round(float(buildings[args.height_field].median()), 2) if args.height_field in buildings.columns else None,
    }

    rasters = {}
    ref = None
    for label, path in (("dsm", args.dsm), ("slope", args.slope), ("aspect", args.aspect)):
        if not path:
            continue
        with rasterio.open(path) as src:
            info = {
                "crs": str(src.crs),
                "shape": [src.height, src.width],
                "res": [round(v, 3) for v in src.res],
                "valid_fraction": None,
            }
            arr = src.read(1, out_shape=(min(512, src.height), min(512, src.width)))
            info["sample_min"] = float(np.nanmin(arr))
            info["sample_max"] = float(np.nanmax(arr))
            rasters[label] = info
            if not src.crs or not src.crs.is_projected:
                issues.append(f"{label} is not in a projected CRS")
            if ref is None:
                ref = (src.shape, src.transform, src.crs)
            elif (src.shape, src.transform, src.crs) != ref:
                issues.append(f"{label} grid does not match the DSM")
            if label == "dsm" and info["sample_min"] < -5:
                issues.append("DSM contains implausibly negative elevations")

    report["rasters"] = rasters
    report["issues"] = issues
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
