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

    Deliverable.BURN_SEVERITY_MAP: {Dependency.BURN_SEVERITY},

    Deliverable.BURNED_AREA_STATISTICS: {Dependency.BURNED_AREA_STATISTICS},

    # visuals (same data, different representation)
    Deliverable.RGB_PRE_FIRE_VISUAL: {Dependency.RGB_PRE_FIRE},
    Deliverable.RGB_POST_FIRE_VISUAL: {Dependency.RGB_POST_FIRE},
    Deliverable.RBR_VISUAL: {Dependency.RBR},
    Deliverable.DNBR_VISUAL: {Dependency.DNBR},
    Deliverable.BURN_SEVERITY_VISUAL: {Dependency.BURN_SEVERITY},
}
