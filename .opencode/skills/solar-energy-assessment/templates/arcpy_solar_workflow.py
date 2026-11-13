#!/usr/bin/env python3
"""
ArcGIS Pro rooftop PV workflow template.

Fill the CONFIG block, then run in the ArcGIS Pro Python window:

    exec(open(r"<PATH>\arcpy_solar_workflow.py").read())

Requires ArcGIS Pro 3.x and the Spatial Analyst extension.

This template implements:
- annual Raster Solar Radiation
- base / tutorial / strict suitability scenarios
- zonal statistics, join, energy calculation
- CSV export to a folder

It deliberately does not hard-code a city or a Windows path.
"""

from __future__ import annotations

import os
import arcpy
from arcpy.sa import Raster, Con, RasterSolarRadiation, ZonalStatisticsAsTable

# ===========================================================================
# CONFIG — EDIT THIS BLOCK
# ===========================================================================
CONFIG = {
    # Geodatabase and inputs
    "gdb": r"<PROJECT_DIR>\<PROJECT>.gdb",
    "dsm": r"<PROJECT_DIR>\dsm_2m.tif",
    "slope": r"<PROJECT_DIR>\slope_2m.tif",
    "aspect": r"<PROJECT_DIR>\aspect_2m.tif",
    "buildings": r"<PROJECT_DIR>\<PROJECT>.gpkg\buildings",
    # Output folder for CSV (never inside a .gdb)
    "csv_folder": r"<PROJECT_DIR>\results\tables",
    # Solar model
    "year": 2025,
    "time_zone": "Bangladesh Standard Time",
    "diffuse": 0.55,
    "transmittivity": 0.50,
    "sunmap_grid_level": 6,
    "target_device": "GPU_THEN_CPU",
    # Energy conversion
    "roof_factor": 0.60,
    "efficiency": 0.216,
    "pr": 0.78,
    "module_area_per_kwp": 4.63,
    "co2_factor": 0.65,
    # Scenarios: name -> (radiation threshold, north_filter)
    "scenarios": {
        "base_1000_no_north": (1000.0, False),
        "tutorial_800_north": (800.0, True),
        "strict_1200_no_north": (1200.0, False),
    },
    # Seasons: name -> (start, end, label)
    "seasons": {
        "winter": ("1/1/{year} 12:00:00 AM", "2/28/{year} 11:30:00 PM", "winter"),
        "premonsoon": ("3/1/{year} 12:00:00 AM", "5/31/{year} 11:30:00 PM", "pre-monsoon"),
        "monsoon": ("6/1/{year} 12:00:00 AM", "9/30/{year} 11:30:00 PM", "monsoon"),
        "postmonsoon": ("10/1/{year} 12:00:00 AM", "12/31/{year} 11:30:00 PM", "post-monsoon"),
    },
    "run_seasons": False,  # set True after the annual run is validated
}
# ===========================================================================


def check_inputs() -> None:
    for key in ("gdb", "dsm", "slope", "aspect", "buildings"):
        if not arcpy.Exists(CONFIG[key]):
            raise FileNotFoundError(f"Missing input: {CONFIG[key]}")
    if arcpy.CheckExtension("Spatial") != "Available":
        raise RuntimeError("Spatial Analyst is not available. Check Project > Licensing.")
    arcpy.CheckOutExtension("Spatial")
    arcpy.env.overwriteOutput = True
    arcpy.env.workspace = CONFIG["gdb"]
    arcpy.env.snapRaster = CONFIG["dsm"]
    arcpy.env.extent = CONFIG["dsm"]
    arcpy.env.cellSize = CONFIG["dsm"]
    arcpy.env.parallelProcessingFactor = "100%"
    os.makedirs(CONFIG["csv_folder"], exist_ok=True)


def run_solar(label: str, start: str, end: str, mask: str, interval: int = 14) -> str:
    out = os.path.join(CONFIG["gdb"], f"solar_{label}")
    if arcpy.Exists(out):
        print("exists:", out)
        return out
    print("Raster Solar Radiation:", label)
    solar = RasterSolarRadiation(
        in_surface_raster=CONFIG["dsm"],
        start_date_time=start,
        end_date_time=end,
        in_analysis_mask=mask,
        in_slope_raster=CONFIG["slope"],
        in_aspect_raster=CONFIG["aspect"],
        time_zone=CONFIG["time_zone"],
        adjust_DST=False,
        use_time_interval=False,
        interval_unit="Day",
        interval=interval,
        neighborhood_distance="2 Meters",
        use_adaptive_neighborhood=False,
        diffuse_model_type="UNIFORM_SKY",
        diffuse_proportion=CONFIG["diffuse"],
        transmittivity=CONFIG["transmittivity"],
        analysis_target_device=CONFIG["target_device"],
        sunmap_grid_level=CONFIG["sunmap_grid_level"],
    )
    solar.save(out)
    return out


def make_suitable(label: str, solar: str, threshold: float, north_filter: bool) -> str:
    out = os.path.join(CONFIG["gdb"], f"suitable_{label}")
    if arcpy.Exists(out):
        print("exists:", out)
        return out
    slope = Raster(CONFIG["slope"])
    aspect = Raster(CONFIG["aspect"])
    rad = Raster(solar)
    condition = (slope <= 45) & (rad >= threshold)
    if north_filter:
        non_north = (aspect == -1) | ((aspect > 22.5) & (aspect < 337.5)) | (slope <= 10)
        condition = condition & non_north
    Con(condition, rad).save(out)
    print("suitable:", out)
    return out


def zonal_and_join(label: str, suitable: str) -> str:
    table = os.path.join(CONFIG["gdb"], f"zonal_{label}")
    if not arcpy.Exists(table):
        ZonalStatisticsAsTable(
            in_zone_data=CONFIG["buildings"],
            zone_field="Building_ID",
            in_value_raster=suitable,
            out_table=table,
            ignore_nodata="DATA",
            statistics_type="ALL",
        )
    out_fc = os.path.join(CONFIG["gdb"], f"buildings_solar_{label}")
    if not arcpy.Exists(out_fc):
        arcpy.management.CopyFeatures(CONFIG["buildings"], out_fc)
        arcpy.management.JoinField(
            out_fc, "Building_ID", table, "Building_ID",
            ["AREA", "MEAN", "SUM", "COUNT"],
        )
    return out_fc


def calculate_energy(fc: str, label: str) -> None:
    fields = [
        ("roof_factor", "DOUBLE"),
        ("usable_area_m2", "DOUBLE"),
        ("capacity_kWp", "DOUBLE"),
        ("incident_MWh", "DOUBLE"),
        ("elec_MWh", "DOUBLE"),
        ("co2_t", "DOUBLE"),
        ("scenario", "TEXT"),
    ]
    existing = {f.name for f in arcpy.ListFields(fc)}
    for name, ftype in fields:
        if name not in existing:
            if ftype == "TEXT":
                arcpy.management.AddField(fc, name, ftype, field_length=60)
            else:
                arcpy.management.AddField(fc, name, ftype)

    cursor_fields = [
        "roof_factor", "usable_area_m2", "capacity_kWp",
        "incident_MWh", "elec_MWh", "co2_t", "scenario",
        "AREA", "MEAN",
    ]
    rf = CONFIG["roof_factor"]
    eta = CONFIG["efficiency"]
    pr = CONFIG["pr"]
    area_per_kwp = CONFIG["module_area_per_kwp"]
    ef = CONFIG["co2_factor"]

    with arcpy.da.UpdateCursor(fc, cursor_fields) as cursor:
        for row in cursor:
            area = row[7] if row[7] is not None else 0.0
            mean = row[8] if row[8] is not None else 0.0
            usable = area * rf
            capacity = usable / area_per_kwp
            incident = usable * mean / 1000.0
            elec = incident * eta * pr
            row[0] = rf
            row[1] = usable
            row[2] = capacity
            row[3] = incident
            row[4] = elec
            row[5] = elec * ef
            row[6] = label
            cursor.updateRow(row)


def export_csv(fc: str, name: str) -> None:
    path = os.path.join(CONFIG["csv_folder"], name)
    if os.path.exists(path):
        os.remove(path)
    arcpy.conversion.TableToTable(fc, CONFIG["csv_folder"], name)
    print("csv:", path)


def main() -> None:
    check_inputs()
    buildings = CONFIG["buildings"]
    year = CONFIG["year"]

    # Annual base run
    annual = run_solar(
        "annual_base",
        f"1/1/{year} 12:00:00 AM",
        f"12/31/{year} 11:30:00 PM",
        buildings,
        interval=14,
    )

    # Scenarios
    for label, (threshold, north) in CONFIG["scenarios"].items():
        suitable = make_suitable(label, annual, threshold, north)
        fc = zonal_and_join(label, suitable)
        calculate_energy(fc, label)
        export_csv(fc, f"solar_summary_{label}.csv")

    # Optional seasonal runs
    if CONFIG["run_seasons"]:
        annual_suitable = os.path.join(CONFIG["gdb"], "suitable_base_1000_no_north")
        if not arcpy.Exists(annual_suitable):
            raise FileNotFoundError(
                "Seasonal runs need the annual suitable raster as mask. "
                "Run the base scenario first."
            )
        for season, (start, end, _) in CONFIG["seasons"].items():
            s = start.format(year=year)
            e = end.format(year=year)
            run_solar(f"season_{season}", s, e, annual_suitable, interval=7)

    print("DONE")


if __name__ == "__main__":
    main()
