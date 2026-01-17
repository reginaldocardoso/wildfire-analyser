# wildfire_analyser/fire_assessment/deliverables.py

from enum import Enum, auto


class Deliverable(Enum):
    # ─────────────────────────────
    # Científicos (GeoTIFF)
    # ─────────────────────────────
    RGB_PRE_FIRE = auto()
    RGB_POST_FIRE = auto()

    NDVI_PRE_FIRE = auto()
    NDVI_POST_FIRE = auto()
    DNDVI = auto()

    NBR_PRE_FIRE = auto()
    NBR_POST_FIRE = auto()
    DNBR = auto()

    RBR = auto()

    DNBR_SEVERITY_MAP = auto()

    # ─────────────────────────────
    # Estatísticas
    # ─────────────────────────────
    DNBR_AREA_STATISTICS = auto()
    DNDVI_AREA_STATISTICS = auto()
    RBR_AREA_STATISTICS = auto()

    # ─────────────────────────────
    # Visuais (JPEG / Thumbnail)
    # ─────────────────────────────
    RGB_PRE_FIRE_VISUAL = auto()
    RGB_POST_FIRE_VISUAL = auto()
    DNDVI_VISUAL = auto()
    DNBR_VISUAL = auto()
    RBR_VISUAL = auto()
    DNBR_SEVERITY_VISUAL = auto()
