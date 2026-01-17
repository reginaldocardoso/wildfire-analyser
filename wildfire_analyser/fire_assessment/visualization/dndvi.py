import ee

def dndvi_visual(image: ee.Image, roi: ee.Geometry) -> ee.Image:
    # Tabela 5 — dNDVI (paper)
    classified = (
        ee.Image(0)  # Unburned (< 0.07)
        .where(image.gte(0.10).And(image.lt(0.20)), 1)   # Low
        .where(image.gte(0.20).And(image.lt(0.33)), 2)   # Moderate
        .where(image.gte(0.33).And(image.lt(0.44)), 3)   # High
        .where(image.gte(0.45), 4)                       # Very High
    )

    styled = classified.visualize(
        min=0,
        max=4,
        palette=[
            "36a402",  # Unburned 
            "fbfb01",  # Low
            "feb012",  # Moderate
            "f50003",  # High
            "6a044d",  # Very High
        ],
    )

    outline = ee.Image().byte().paint(
        ee.FeatureCollection(roi),
        color=1,
        width=2,
    )

    return styled.blend(outline.visualize(palette=["000000"]))
