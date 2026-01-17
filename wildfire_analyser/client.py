import logging
import os
from dotenv import load_dotenv
import argparse
from pathlib import Path

from wildfire_analyser.fire_assessment.post_fire_assessment import PostFireAssessment
from wildfire_analyser.fire_assessment.deliverables import Deliverable


# ─────────────────────────────
# Logging setup
# ─────────────────────────────

LOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"

root_handler = logging.StreamHandler()
root_handler.setFormatter(logging.Formatter(LOG_FORMAT))

root_logger = logging.getLogger()
if not root_logger.handlers:
    root_logger.addHandler(root_handler)

# Root quiet by default (library logs controlled separately)
root_logger.setLevel(logging.WARNING)

# Client logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Library logger (controlled via verbose flag)
lib_logger = logging.getLogger("wildfire_analyser")
lib_logger.setLevel(logging.WARNING)
lib_logger.propagate = True


# ─────────────────────────────
# Paper preset definition
# ─────────────────────────────

PAPER_PRESETS = {
    "PAPER_DENIZ_FUSUN_RAMAZAN": {
        "deliverables": [
            Deliverable.DNBR_VISUAL,
            Deliverable.DNDVI_VISUAL,
            Deliverable.RBR_VISUAL,
            Deliverable.DNBR_AREA_STATISTICS,
            Deliverable.DNDVI_AREA_STATISTICS,
            Deliverable.RBR_AREA_STATISTICS,
        ],
        "runs": [
            {
                "name": "Area 1 – July Fire",
                "roi": "polygons/canakkale_aoi_1.geojson",
                "start_date": "2023-07-01",
                "end_date": "2023-07-21",
                "days_before_after": 1,
            },
            {
                "name": "Area 2 – August Fire",
                "roi": "polygons/canakkale_aoi_2.geojson",
                "start_date": "2023-07-31",
                "end_date": "2023-08-30",
                "days_before_after": 1,
            },
        ],
    }
}


# ─────────────────────────────
# Main
# ─────────────────────────────

def main():
    try:
        load_dotenv()

        gee_key_json = os.getenv("GEE_PRIVATE_KEY_JSON")
        if not gee_key_json:
            raise RuntimeError("GEE_PRIVATE_KEY_JSON not set")

        gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
        if not gcs_bucket_name:
            raise RuntimeError("GCS_BUCKET_NAME not set")

        parser = argparse.ArgumentParser(
            description="Post-fire assessment using Google Earth Engine"
        )

        parser.add_argument("--roi", help="Path to ROI GeoJSON file")
        parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
        parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")

        parser.add_argument(
            "--deliverables",
            nargs="+",
            help=(
                "List of deliverables to generate OR a paper preset name. "
                "Example: --deliverables DNBR_VISUAL "
                "or --deliverables PAPER_DENIZ_FUSUN_RAMAZAN"
            ),
        )

        parser.add_argument(
            "--days-before-after",
            type=int,
            default=30,
            help="Number of days before and after the event date (default: 30)",
        )

        args = parser.parse_args()

        # ─────────────────────────────
        # PAPER PRESET MODE
        # ─────────────────────────────

        if (
            args.deliverables
            and len(args.deliverables) == 1
            and args.deliverables[0].upper() in PAPER_PRESETS
        ):
            preset_name = args.deliverables[0].upper()
            preset = PAPER_PRESETS[preset_name]

            logger.info("Running paper preset: %s", preset_name)

            runs = preset.get("runs")
            if not runs:
                raise RuntimeError(
                    f"Paper preset '{preset_name}' has no runs configured"
                )

            logger.info("Number of runs: %d", len(runs))

            for cfg in runs:
                logger.info("────────────────────────────────────")
                logger.info("Processing %s", cfg["name"])

                roi_path = Path(cfg["roi"]).expanduser().resolve()
                if not roi_path.exists():
                    raise FileNotFoundError(f"GeoJSON not found: {roi_path}")

                runner = PostFireAssessment(
                    gee_key_json=gee_key_json,
                    geojson_path=str(roi_path),
                    start_date=cfg["start_date"],
                    end_date=cfg["end_date"],
                    days_before_after=cfg["days_before_after"],
                    deliverables=preset["deliverables"],
                    gcs_bucket=gcs_bucket_name,
                    verbose=True,
                )

                result = runner.run()

                logger.info("Visual outputs:")
                for name, item in result["visual"].items():
                    logger.info("  %s -> %s", name, item["url"])

                logger.info("Statistics:")
                for stat_name, stat_value in result["statistics"].items():
                    logger.info("  %s:", stat_name)
                    for cls, values in stat_value.items():
                        logger.info(
                            "    %-20s | Area (ha): %8.2f | Ratio (%%): %6.2f",
                            cls,
                            values["area_ha"],
                            values["ratio_percent"],
                        )

            return  # ⬅️ IMPORTANT: stop execution here

        # ─────────────────────────────
        # NORMAL MODE
        # ─────────────────────────────

        if args.deliverables:
            try:
                deliverables = [Deliverable[name.upper()] for name in args.deliverables]
            except KeyError as e:
                valid = ", ".join(d.name for d in Deliverable)
                raise ValueError(
                    f"Invalid deliverable '{e.args[0]}'. "
                    f"Valid options are: {valid}"
                )
        else:
            deliverables = list(Deliverable)

        if not args.roi or not args.start_date or not args.end_date:
            raise ValueError("--roi, --start-date and --end-date are required")

        geojson_path = Path(args.roi).expanduser().resolve()
        if not geojson_path.exists():
            raise FileNotFoundError(f"GeoJSON not found: {geojson_path}")

        runner = PostFireAssessment(
            gee_key_json=gee_key_json,
            geojson_path=str(geojson_path),
            start_date=args.start_date,
            end_date=args.end_date,
            days_before_after=args.days_before_after,
            deliverables=deliverables,
            gcs_bucket=gcs_bucket_name,
            verbose=True,
        )

        result = runner.run()

        logger.info("Visual outputs:")
        for name, item in result["visual"].items():
            logger.info("  %s -> %s", name, item["url"])

        logger.info("Statistics:")
        for stat_name, stat_value in result["statistics"].items():
            logger.info("  %s:", stat_name)
            for cls, values in stat_value.items():
                logger.info(
                    "    %-20s | Area (ha): %8.2f | Ratio (%%): %6.2f",
                    cls,
                    values["area_ha"],
                    values["ratio_percent"],
                )

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        logger.error(str(e))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
