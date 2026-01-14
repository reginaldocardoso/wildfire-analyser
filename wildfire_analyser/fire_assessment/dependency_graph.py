# wildfire_analyser/fire_assessment/dependency_graph.py

from wildfire_analyser.fire_assessment.dependencies import Dependency


DEPENDENCY_GRAPH = {
    # Ingestion
    Dependency.COLLECTION_GATHERING: set(),

    # Collections
    Dependency.PRE_FIRE_COLLECTION: {Dependency.COLLECTION_GATHERING},
    Dependency.POST_FIRE_COLLECTION: {Dependency.COLLECTION_GATHERING},

    # Mosaics
    Dependency.PRE_FIRE_MOSAIC: {Dependency.PRE_FIRE_COLLECTION},
    Dependency.POST_FIRE_MOSAIC: {Dependency.POST_FIRE_COLLECTION},

    # RGB
    Dependency.RGB_PRE_FIRE: {Dependency.PRE_FIRE_MOSAIC},
    Dependency.RGB_POST_FIRE: {Dependency.POST_FIRE_MOSAIC},

    # NDVI
    Dependency.NDVI_PRE_FIRE: {Dependency.PRE_FIRE_MOSAIC},
    Dependency.NDVI_POST_FIRE: {Dependency.POST_FIRE_MOSAIC},
    Dependency.DNDVI: {
        Dependency.NDVI_PRE_FIRE,
        Dependency.NDVI_POST_FIRE,
    },

    # NBR
    Dependency.NBR_PRE_FIRE: {Dependency.PRE_FIRE_MOSAIC},
    Dependency.NBR_POST_FIRE: {Dependency.POST_FIRE_MOSAIC},
    Dependency.DNBR: {
        Dependency.NBR_PRE_FIRE,
        Dependency.NBR_POST_FIRE,
    },

    # Fire indices
    Dependency.RBR: {
        Dependency.DNBR,
        Dependency.NBR_PRE_FIRE,
    },

    Dependency.BURN_SEVERITY: {
        Dependency.DNBR,
    },

    Dependency.BURNED_AREA_STATISTICS: {
        Dependency.BURN_SEVERITY,
    },
}
