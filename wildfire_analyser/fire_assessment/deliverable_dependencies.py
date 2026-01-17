from wildfire_analyser.fire_assessment.deliverables import Deliverable
from wildfire_analyser.fire_assessment.dependencies import Dependency

DELIVERABLE_DEPENDENCIES = {
    Deliverable.RGB_PRE_FIRE: {Dependency.RGB_PRE_FIRE},
    Deliverable.RGB_POST_FIRE: {Dependency.RGB_POST_FIRE},

    Deliverable.NDVI_PRE_FIRE: {Dependency.NDVI_PRE_FIRE},
    Deliverable.NDVI_POST_FIRE: {Dependency.NDVI_POST_FIRE},
    Deliverable.DNDVI: {Dependency.DNDVI},

    Deliverable.NBR_PRE_FIRE: {Dependency.NBR_PRE_FIRE},
    Deliverable.NBR_POST_FIRE: {Dependency.NBR_POST_FIRE},
    Deliverable.DNBR: {Dependency.DNBR},

    Deliverable.RBR: {Dependency.RBR},

    Deliverable.DNBR_SEVERITY_MAP: {Dependency.DNBR_SEVERITY},

    Deliverable.DNBR_AREA_STATISTICS: {Dependency.DNBR_AREA_STATISTICS},
    Deliverable.DNDVI_AREA_STATISTICS: {Dependency.DNDVI_AREA_STATISTICS},
    Deliverable.RBR_AREA_STATISTICS: {Dependency.RBR_AREA_STATISTICS},

    # visuals (same data, different representation)
    Deliverable.RGB_PRE_FIRE_VISUAL: {Dependency.RGB_PRE_FIRE},
    Deliverable.RGB_POST_FIRE_VISUAL: {Dependency.RGB_POST_FIRE},
    Deliverable.DNDVI_VISUAL: {Dependency.DNDVI},
    Deliverable.RBR_VISUAL: {Dependency.RBR},
    Deliverable.DNBR_VISUAL: {Dependency.DNBR},
    Deliverable.DNBR_SEVERITY_VISUAL: {Dependency.DNBR_SEVERITY},
}
