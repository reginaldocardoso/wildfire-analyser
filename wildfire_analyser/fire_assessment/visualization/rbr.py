import ee

def rbr_visual(image: ee.Image, roi: ee.Geometry) -> ee.Image:
    # Classificação por faixas (paper-style)
    classified = (
        ee.Image(0)  # Unburned
        .where(image.gte(0.10).And(image.lt(0.27)), 1)   # Low
        .where(image.gte(0.27).And(image.lt(0.44)), 2)  # Moderate
        .where(image.gte(0.44).And(image.lt(0.66)), 3)  # High
        .where(image.gte(0.66), 4)                      # Very High
    )

    styled = classified.visualize(
        min=0,
        max=4,
        palette=[
            "00FF00",  # Unburned
            "FFFF00",  # Low
            "FFA500",  # Moderate
            "FF0000",  # High
            "8B4513",  # Very High
        ],
    )

    outline = ee.Image().byte().paint(
        ee.FeatureCollection(roi),
        color=1,
        width=2,
    )

    return styled.blend(outline.visualize(palette=["000000"]))
