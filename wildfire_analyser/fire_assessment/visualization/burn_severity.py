import ee


def burn_severity_visual(image: ee.Image, roi: ee.Geometry) -> ee.Image:
    styled = image.visualize(
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
        featureCollection=ee.FeatureCollection(roi),
        color=1,
        width=2,
    )

    return styled.blend(outline.visualize(palette=["000000"]))
