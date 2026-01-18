import ee


def dnbr_severity_visual(image: ee.Image, roi: ee.Geometry) -> ee.Image:
    styled = image.visualize(
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
        featureCollection=ee.FeatureCollection(roi),
        color=1,
        width=2,
    )

    return styled.blend(outline.visualize(palette=["000000"]))
