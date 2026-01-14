import ee
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import uuid

from wildfire_analyser.fire_assessment.auth import authenticate_gee
from wildfire_analyser.fire_assessment.resolver import (
    DAGExecutionContext,
    execute_dag,
)
from wildfire_analyser.fire_assessment.deliverables import Deliverable
from wildfire_analyser.fire_assessment.visualization import VISUAL_RENDERERS
from wildfire_analyser.fire_assessment.exporters.gcs import (
    export_geotiff_to_gcs,
    get_visual_thumbnail_url,
)


class PostFireAssessment:

    DEFAULT_SCALE = 10

    def __init__(
        self,
        gee_key_json: str,
        geojson_path: str,
        start_date: str,
        end_date: str,
        deliverables: List[Deliverable],
        cloud_threshold: int = 70,
        days_before_after: int = 30,
        gcs_bucket: str | None = None,
    ):
        authenticate_gee(gee_key_json)

        self.roi = self._load_geojson(Path(geojson_path))
        self.deliverables = deliverables
        self.bucket = gcs_bucket

        self.context = DAGExecutionContext(
            roi=self.roi,
            start_date=start_date,
            end_date=end_date,
            cloud_threshold=cloud_threshold,
            days_before_after=days_before_after,
        )

    def run(self) -> Dict[str, Any]:
        outputs = execute_dag(self.deliverables, self.context)

        result = {
            "scientific": {},
            "visual": {},
            "statistics": {},
        }

        for d, value in outputs.items():

            if d == Deliverable.BURNED_AREA_STATISTICS:
                result["statistics"] = value
                continue

            if d in VISUAL_RENDERERS:
                vis = VISUAL_RENDERERS[d](value, self.roi)
                result["visual"][d.name] = {
                    "url": get_visual_thumbnail_url(vis, self.roi)
                }
                continue

            if self.bucket:
                object_name = self._generate_object_name(
                    deliverable=d.name.lower(),
                    start_date=self.context.inputs["start_date"],
                    end_date=self.context.inputs["end_date"],
                )

                url = export_geotiff_to_gcs(
                    image=value,
                    roi=self.roi,
                    bucket=self.bucket,
                    object_name=object_name,
                    scale=self.DEFAULT_SCALE,
                )

                result["scientific"][d.name] = {"url": url}

        return result

    @staticmethod
    def _load_geojson(path: Path) -> ee.Geometry:
        import json
        with open(path) as f:
            geojson = json.load(f)
        return ee.Geometry(geojson["features"][0]["geometry"])
    
    @staticmethod
    def _generate_object_name(
        deliverable: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """
        Generate a unique object name for exports.
        """
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        uid = uuid.uuid4().hex[:8]

        start_norm = start_date.replace("-", "_")
        end_norm = end_date.replace("-", "_")

        return f"{deliverable}_{start_norm}_{end_norm}_{ts}_{uid}"
        