# wildfire_analyser/fire_assessment/dependencies.py

from enum import Enum, auto


class Dependency(Enum):
    # ─────────────────────────────
    # Data ingestion
    # ─────────────────────────────
    COLLECTION_GATHERING = auto()

    # ─────────────────────────────
    # Temporal collections
    # ─────────────────────────────
    PRE_FIRE_COLLECTION = auto()
    POST_FIRE_COLLECTION = auto()

    # ─────────────────────────────
    # Mosaics
    # ─────────────────────────────
    PRE_FIRE_MOSAIC = auto()
    POST_FIRE_MOSAIC = auto()

    # ─────────────────────────────
    # RGB
    # ─────────────────────────────
    RGB_PRE_FIRE = auto()
    RGB_POST_FIRE = auto()

    # ─────────────────────────────
    # NBR / NDVI / RBR
    # ─────────────────────────────
    NBR_PRE_FIRE = auto()
    NBR_POST_FIRE = auto()
    DNBR = auto()

    NDVI_PRE_FIRE = auto()
    NDVI_POST_FIRE = auto()
    DNDVI = auto()

    RBR = auto()

    # ─────────────────────────────
    # Fire metrics
    # ─────────────────────────────
    DNBR_AREA_STATISTICS = auto()
    DNDVI_AREA_STATISTICS = auto()
    RBR_AREA_STATISTICS = auto()
