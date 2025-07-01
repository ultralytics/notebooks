# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# Tests Ultralytics Notebooks: https://github.com/ultralytics/notebooks/

import cv2
import pytest
from ultralytics import YOLO, SAM, ASSETS
from ultralytics.utils.downloads import safe_download
from ultralytics.utils import ROOT
from ultralytics.solutions import ObjectCounter, TrackZone, Heatmap, AIGym

TMP = (ROOT / "../tests/tmp").resolve()  # temp directory for test files

DEMO_VIDEO = "https://github.com/ultralytics/notebooks/releases/download/v0.0.0/solutions-ci-demo.mp4"
WORKOUT_VIDEO = "https://github.com/ultralytics/assets/releases/download/v0.0.0/Legextension.demo.video.mp4"

@pytest.mark.parametrize("solution_class, solution_kwargs, video_source", [
    (ObjectCounter, {"region": [(20, 400), (1080, 400), (1080, 360), (20, 360)]}, DEMO_VIDEO),
    (TrackZone, {"region": [(20, 400), (1080, 400), (1080, 360), (20, 360)]}, DEMO_VIDEO),
    (Heatmap, {"colormap": cv2.COLORMAP_PARULA}, DEMO_VIDEO),
    (AIGym, {"kpts": [12, 14, 16]}, WORKOUT_VIDEO)
])
def test_solution_inference(solution_class, solution_kwargs, video_source):
    """Parameterized test for multiple Ultralytics solution demos."""
    safe_download(video_source)
    source = "Legextension.demo.video.mp4" if solution_class=="AIGym" else "solutions-ci-demo.mp4"
    cap = cv2.VideoCapture(source)
    solution = solution_class(**solution_kwargs)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        _ = solution(frame)  # Run inference
    cap.release()


def test_export_val_results():
    """Test: notebooks/how-to-export-the-validation-results-into-dataframe-csv-sql-and-other-formats.ipynb"""
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


@pytest.mark.slow
def test_sam_inference():
    """Test: notebooks/inference-with-meta-sam-and-sam2-using-ultralytics-python-package.ipynb"""
    from ultralytics.data.annotator import auto_annotate

    model = SAM("sam2.1_b.pt")
    _ = model(ASSETS/"bus.jpg")  # image.
    _ = model(ASSETS/"bus.jpg", points=[34, 714])  # point prompt.
    _ = model(ASSETS/"bus.jpg", points=[[34, 714], [283, 634]]) # multiple points prompt.
    _ = model(ASSETS / "bus.jpg", bboxes=[3.83287, 229.3560, 796.2098, 728.4313])  # bbox prompt.

    for img in ["bus.jpg", "zidane.jpg"]:
        safe_download(f"https://ultralytics.com/assets/{img}", dir="assets")
    auto_annotate(data="/content/assets",  # return the annotation in the Ultralytics YOLO segmentation format.
                  det_model="yolo11x.pt",
                  sam_model="sam_b.pt")
