#!/usr/bin/env python3
"""
Create a stratified validation sample and an Excel/KML worksheet.

Run outside ArcGIS Pro with Python + geopandas + openpyxl:

    python validation_sample.py

Edit CONFIG first.
"""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from shapely.geometry import Point

# ===========================================================================
# CONFIG — EDIT THIS BLOCK
# ===========================================================================
CONFIG = {
    "buildings": r"<PROJECT_DIR>\buildings.gpkg",
    "buildings_layer": "buildings",
    "output_dir": r"<PROJECT_DIR>\validation",
    "n": 100,
    "seed": 2026,
    "id_field": "Building_ID",
    "ward_field": "Ward_Name",
    "size_field": "size_class",  # or compute from area
    "area_field": "area_m2",
    "height_field": "height_m",
    "lat_field": "latitude",
    "lon_field": "longitude",
    "utm_epsg": 32645,
}
# ===========================================================================

OUT = Path(CONFIG["output_dir"])
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    g = gpd.read_file(CONFIG["buildings"], layer=CONFIG["buildings_layer"])
    if g.crs and g.crs.to_epsg() != 4326:
        g = g.to_crs(4326)
    if "size_class" not in g.columns:
        g["size_class"] = pd.cut(
            g[CONFIG["area_field"]],
            bins=[-1, 50, 150, 1e9],
            labels=["small", "medium", "large"],
        ).astype(str)

    cent = g.geometry.centroid
    g["lat"] = cent.y
    g["lon"] = cent.x

    rows = []
    for ward, wg in g.groupby(CONFIG["ward_field"]):
        for size, sg in wg.groupby("size_class"):
            if len(sg) == 0:
                continue
            rows.append(sg.sample(n=1, random_state=CONFIG["seed"]))
    base = pd.concat(rows) if rows else g.head(0)
    base_ids = set(base[CONFIG["id_field"]])
    remaining = CONFIG["n"] - len(base)
    if remaining > 0:
        pool = g[~g[CONFIG["id_field"]].isin(base_ids)]
        extra = pool.sample(n=min(remaining, len(pool)), random_state=CONFIG["seed"])
        sample = pd.concat([base, extra])
    else:
        sample = base.head(CONFIG["n"])
    sample = sample.sample(frac=1, random_state=CONFIG["seed"]).reset_index(drop=True)
    sample["Sample_ID"] = [f"V{i:03d}" for i in range(1, len(sample) + 1)]

    out_rows = []
    for _, r in sample.iterrows():
        out_rows.append(
            {
                "Sample_ID": r["Sample_ID"],
                "Building_ID": r[CONFIG["id_field"]],
                "Ward_Name": r[CONFIG["ward_field"]],
                "size_class": r["size_class"],
                "Latitude": round(float(r["lat"]), 7),
                "Longitude": round(float(r["lon"]), 7),
                "Google_Earth_Link": f"https://earth.google.com/web/search/{r['lat']:.6f},{r['lon']:.6f}",
                "Google_Maps_Link": f"https://www.google.com/maps/@{r['lat']:.6f},{r['lon']:.6f},20z",
                "Imagery_Date": "",
                "GIS_Area_m2": round(float(r[CONFIG["area_field"]]), 2),
                "Google_Area_m2": "",
                "Height_m": round(float(r[CONFIG["height_field"]]), 2),
                "Observed_Floors": "",
                "Observed_Height_m": "",
                "Roof_Type": "",
                "Roof_Condition": "",
                "Obstructions": "",
                "Tree_Shade": "",
                "Neighbor_Shade": "",
                "Existing_PV": "",
                "Usable_Roof_pct": "",
                "Observed_Suitability": "",
                "Confidence": "",
                "Notes": "",
                "Validator": "",
                "Validation_Date": "",
            }
        )
    df = pd.DataFrame(out_rows)
    df.to_csv(OUT / "validation_sample.csv", index=False)
    sample.drop(columns=["geometry"]).to_csv(OUT / "validation_sample_full.csv", index=False)

    # Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Validation_Sample"
    headers = list(df.columns)
    ws.append(headers)
    fill = PatternFill("solid", fgColor="1F4E78")
    font = Font(bold=True, color="FFFFFF")
    thin = Side(style="thin", color="B7B7B7")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = fill
        cell.font = font
        cell.border = border
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for ri, row in df.iterrows():
        for ci, col in enumerate(headers, start=1):
            value = row[col]
            if col == "Observed_Height_m":
                ws.cell(row=ri + 2, column=ci, value=f'=IF(M{ri+2}="","",M{ri+2}*3)')
            elif col in ("Google_Earth_Link", "Google_Maps_Link"):
                cell = ws.cell(row=ri + 2, column=ci, value=str(value))
                cell.hyperlink = str(value)
                cell.font = Font(color="0563C1", underline="single")
            else:
                ws.cell(row=ri + 2, column=ci, value=value)
            ws.cell(row=ri + 2, column=ci).border = border

    widths = {"Sample_ID": 10, "Building_ID": 14, "Ward_Name": 10, "Latitude": 12, "Longitude": 12,
              "Google_Earth_Link": 36, "Google_Maps_Link": 36, "Imagery_Date": 12,
              "GIS_Area_m2": 11, "Google_Area_m2": 11, "Height_m": 10, "Observed_Floors": 12,
              "Observed_Height_m": 13, "Roof_Type": 15, "Roof_Condition": 13, "Obstructions": 15,
              "Tree_Shade": 11, "Neighbor_Shade": 13, "Existing_PV": 10, "Usable_Roof_pct": 13,
              "Observed_Suitability": 17, "Confidence": 10, "Notes": 30, "Validator": 12,
              "Validation_Date": 14}
    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = widths.get(h, 14)
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(df)+1}"

    def dv(col, options):
        idx = headers.index(col) + 1
        d = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
        ws.add_data_validation(d)
        d.add(f"{get_column_letter(idx)}2:{get_column_letter(idx)}{len(df)+1}")

    dv("Roof_Type", ["Flat RCC", "Pitched tile", "Tin/metal", "Other", "Unknown"])
    dv("Roof_Condition", ["Good", "Fair", "Poor", "Unknown"])
    dv("Obstructions", ["None", "Water tank", "Stairwell", "AC units", "Parapet", "Multiple", "Other"])
    dv("Tree_Shade", ["None", "Partial", "Heavy", "Unknown"])
    dv("Neighbor_Shade", ["None", "Partial", "Heavy", "Unknown"])
    dv("Existing_PV", ["Yes", "No", "Unknown"])
    dv("Observed_Suitability", ["Suitable", "Not suitable", "Uncertain"])
    dv("Confidence", ["1", "2", "3", "4", "5"])

    wb.save(OUT / "validation_sample.xlsx")

    # KML
    placemarks = []
    for _, r in df.iterrows():
        desc = f"Building_ID: {r['Building_ID']}<br/>Ward: {r['Ward_Name']}<br/>GIS area: {r['GIS_Area_m2']} m2"
        placemarks.append(
            f"<Placemark><name>{r['Sample_ID']} | {r['Building_ID']}</name>"
            f"<description><![CDATA[{desc}]]></description>"
            f"<Point><coordinates>{r['Longitude']:.7f},{r['Latitude']:.7f},0</coordinates></Point></Placemark>"
        )
    kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>' + "".join(placemarks) + "</Document></kml>"
    (OUT / "validation_sample.kml").write_text(kml, encoding="utf-8")

    log = {
        "seed": CONFIG["seed"],
        "sample_size": len(df),
        "wards": int(df["Ward_Name"].nunique()),
        "size_classes": df["size_class"].value_counts().to_dict(),
    }
    (OUT / "sampling_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
