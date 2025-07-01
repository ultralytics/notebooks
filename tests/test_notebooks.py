import pytest
from ultralytics import YOLO, SAM, ASSETS

# Test: notebooks/how-to-export-the-validation-results-into-dataframe-csv-sql-and-other-formats.ipynb
def export_val_results():
    model = YOLO("yolo11n.pt")
    metrics = model.val(data="coco8.yaml", verbose=True)
    metrics.to_df()
    metrics.to_csv()
    metrics.to_html()
    metrics.to_sql()
    metrics.to_json()
    metrics.confusion_matrix.to_df()
    metrics.confusion_matrix.to_html()
    metrics.confusion_matrix.to_sql()
    metrics.confusion_matrix.to_xml()
    metrics.confusion_matrix.to_json()
    with open("validation_results.html", "w") as f:
        f.write(metrics.to_xml())
    with open("confusion_matrix.csv", "w") as f:
        f.write(metrics.confusion_matrix.to_csv())


# Test: notebooks/inference-with-meta-sam-and-sam2-using-ultralytics-python-package.ipynb
@pytest.mark.slow
def test_sam_inference():
    from ultralytics.data.annotator import auto_annotate
    from ultralytics.utils.downloads import safe_download

    model = SAM("sam2.1_b.pt")
    _ = model()  # image.
    _ = model("https://ultralytics.com/images/bus.jpg",  # bbox prompt.
                    bboxes=[3.8328723907470703, 229.35601806640625,
                            796.2098999023438, 728.4313354492188])
    _ = model("https://ultralytics.com/images/bus.jpg", points=[34, 714])  # Point prompt.
    _ = model("https://ultralytics.com/images/bus.jpg", points=[[34, 714], [283, 634]]) # Multiple points prompt.

    for img in ["bus.jpg", "zidane.jpg"]:
        safe_download(f"https://ultralytics.com/assets/{img}", dir="assets")
    auto_annotate(data="/content/assets",  # return the annotation in the Ultralytics YOLO segmentation format.
                  det_model="yolo11x.pt",
                  sam_model="sam_b.pt")


# Test: