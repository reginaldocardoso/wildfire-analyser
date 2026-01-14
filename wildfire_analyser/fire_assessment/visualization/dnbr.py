import ee


def dnbr_visual(image: ee.Image, roi: ee.Geometry) -> ee.Image:
    styled = image.visualize(
        min=-0.5,
        max=1.0,
        palette=[
            "00FF00",
            "FFFF00",
            "FFA500",
            "FF0000",
            "8B4513",
        ],
    )

    outline = ee.Image().byte().paint(
        featureCollection=ee.FeatureCollection(roi),
        color=1,
        width=2,
    )

    return styled.blend(outline.visualize(palette=["000000"]))
