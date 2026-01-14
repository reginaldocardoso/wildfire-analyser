from wildfire_analyser.fire_assessment.deliverables import Deliverable
from wildfire_analyser.fire_assessment.visualization.rgb import (
    rgb_pre_fire_visual,
    rgb_post_fire_visual,
)
from wildfire_analyser.fire_assessment.visualization.dnbr import dnbr_visual
from wildfire_analyser.fire_assessment.visualization.burn_severity import (
    burn_severity_visual,
)

VISUAL_RENDERERS = {
    Deliverable.RGB_PRE_FIRE_VISUAL: rgb_pre_fire_visual,
    Deliverable.RGB_POST_FIRE_VISUAL: rgb_post_fire_visual,
    Deliverable.DNBR_VISUAL: dnbr_visual,
    Deliverable.BURN_SEVERITY_VISUAL: burn_severity_visual,
}
