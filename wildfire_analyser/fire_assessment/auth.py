# wildfire_analyser/fire_assessment/auth.py

import ee
import os
import json
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile


def authenticate_gee(env_path: str | None = None) -> None:
    """
    Authenticate Google Earth Engine using a service account JSON
    stored in the GEE_PRIVATE_KEY_JSON environment variable.
    """
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

    gee_key_json = os.getenv("GEE_PRIVATE_KEY_JSON")
    if not gee_key_json:
        raise RuntimeError("GEE_PRIVATE_KEY_JSON not found in environment")

    try:
        key_dict = json.loads(gee_key_json)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid GEE_PRIVATE_KEY_JSON format") from e

    try:
        with NamedTemporaryFile(mode="w+", suffix=".json") as f:
            json.dump(key_dict, f)
            f.flush()
            credentials = ee.ServiceAccountCredentials(
                key_dict["client_email"], f.name
            )
            ee.Initialize(credentials)
    except Exception as e:
        raise RuntimeError("Failed to authenticate with Google Earth Engine") from e
