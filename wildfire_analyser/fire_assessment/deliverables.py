# wildfire_analyser/fire_assessment/deliverables.py

from enum import Enum, auto


class Deliverable(Enum):
    # ─────────────────────────────
    # Científicos (GeoTIFF)
    # ─────────────────────────────
    RGB_PRE_FIRE = auto()
    RGB_POST_FIRE = auto()

    NBR_PRE_FIRE = auto()
    NBR_POST_FIRE = auto()

    DNBR = auto()
    RBR = auto()

    BURN_SEVERITY_MAP = auto()

    # ─────────────────────────────
    # Estatísticas
    # ─────────────────────────────
    BURNED_AREA_STATISTICS = auto()

    # ─────────────────────────────
    # Visuais (JPEG / Thumbnail)
    # ─────────────────────────────
    RGB_PRE_FIRE_VISUAL = auto()
    RGB_POST_FIRE_VISUAL = auto()

    DNBR_VISUAL = auto()
    BURN_SEVERITY_VISUAL = auto()
