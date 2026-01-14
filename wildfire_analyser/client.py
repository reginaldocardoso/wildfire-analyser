import logging
import os
from dotenv import load_dotenv
from pathlib import Path

from wildfire_analyser.fire_assessment.post_fire_assessment import PostFireAssessment
from wildfire_analyser.fire_assessment.deliverables import Deliverable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    gee_key_json = os.getenv("GEE_PRIVATE_KEY_JSON")
    if not gee_key_json:
        raise RuntimeError("GEE_PRIVATE_KEY_JSON not set")

    gcs_bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not gcs_bucket_name:
        raise RuntimeError("GCS_BUCKET_NAME not set")

    # Path to the GeoJSON polygon used as the Region of Interest (ROI)
    geojson_path = os.path.join("polygons", "eejatai.geojson")

    runner = PostFireAssessment(
        gee_key_json=gee_key_json,
        geojson_path=str(geojson_path),
        start_date="2024-09-01",
        end_date="2024-11-08",
        deliverables=[
            Deliverable.RGB_PRE_FIRE,
            Deliverable.RGB_POST_FIRE,
            Deliverable.NBR_PRE_FIRE,
            Deliverable.NBR_POST_FIRE,
            Deliverable.DNBR,
            Deliverable.RBR,
            Deliverable.BURN_SEVERITY_MAP,
            Deliverable.RGB_PRE_FIRE_VISUAL,
            Deliverable.RGB_POST_FIRE_VISUAL,
            Deliverable.DNBR_VISUAL,
            Deliverable.BURN_SEVERITY_VISUAL,
            Deliverable.BURNED_AREA_STATISTICS,
        ],
        gcs_bucket=gcs_bucket_name,
    )

    result = runner.run()

    logger.info("Scientific outputs:")
    for name, item in result["scientific"].items():
        logger.info("  %s -> %s", name, item["url"])

    logger.info("Visual outputs:")
    for name, item in result["visual"].items():
        logger.info("  %s -> %s", name, item["url"])

    logger.info("Statistics:")
    for cls, values in result["statistics"].items():
        logger.info(
            f"{cls:<20} | Area (ha): {values['area_ha']:8.2f} | "
            f"Ratio (%): {values['ratio_percent']:6.2f}"
        )


if __name__ == "__main__":
    main()
