# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# Tests Ultralytics Notebooks: https://github.com/ultralytics/notebooks/

from pathlib import Path

import cv2
import pytest

from ultralytics import ASSETS, SAM, YOLO
from ultralytics.data.annotator import auto_annotate
from ultralytics.solutions import AIGym, Heatmap, ObjectCounter, TrackZone
from ultralytics.utils.downloads import safe_download

DEMO_VIDEO = "https://github.com/ultralytics/notebooks/releases/download/v0.0.0/solutions-ci-demo.mp4"
WORKOUT_VIDEO = "https://github.com/ultralytics/assets/releases/download/v0.0.0/Legextension.demo.video.mp4"


def _download_asset(url: str, directory: Path) -> Path:
    """Download a notebook asset into a temporary test directory."""
    return Path(safe_download(url, dir=directory, progress=False))


def _first_frame(video_path: Path):
    """Read a single frame for inexpensive notebook smoke tests."""
    cap = cv2.VideoCapture(str(video_path))
    success, frame = cap.read()
    cap.release()
    assert success, f"Failed to read frame from {video_path}"
    return frame


@pytest.fixture(scope="session")
def notebook_assets(tmp_path_factory):
    """Download shared notebook assets once per test session."""
    assets_dir = tmp_path_factory.mktemp("notebook-assets")
    return {
        "demo_video": _download_asset(DEMO_VIDEO, assets_dir),
        "workout_video": _download_asset(WORKOUT_VIDEO, assets_dir),
    }


@pytest.mark.parametrize(
    ("solution_class", "solution_kwargs", "video_url"),
    [
        (
            ObjectCounter,
            {"model": "yolo26n.pt", "region": [(20, 400), (1080, 400), (1080, 360), (20, 360)]},
            DEMO_VIDEO,
        ),
        (
            TrackZone,
            {"model": "yolo26n.pt", "region": [(20, 400), (1080, 400), (1080, 360), (20, 360)]},
            DEMO_VIDEO,
        ),
        (Heatmap, {"model": "yolo26n.pt", "colormap": cv2.COLORMAP_PARULA}, DEMO_VIDEO),
        (AIGym, {"model": "yolo26n-pose.pt", "kpts": [12, 14, 16]}, WORKOUT_VIDEO),
    ],
)
def test_solution_inference(notebook_assets, solution_class, solution_kwargs, video_url):
    """Smoke-test notebook solution flows using the current YOLO26 models."""
    video_path = notebook_assets["workout_video"] if video_url == WORKOUT_VIDEO else notebook_assets["demo_video"]
    frame = _first_frame(video_path)
    result = solution_class(**solution_kwargs)(frame)
    assert result is not None


def test_export_val_results(tmp_path):
    """Test: notebooks/how-to-export-the-validation-results-into-dataframe-csv-sql-and-other-formats.ipynb."""
    metrics = YOLO("yolo26n.pt").val(data="coco8.yaml", verbose=False)

    metrics_df = metrics.to_df()
    confusion_df = metrics.confusion_matrix.to_df()

    assert len(metrics_df) > 0
    assert len(confusion_df) > 0

    outputs = {
        "validation_results.csv": metrics.to_csv(),
        "validation_results.json": metrics.to_json(),
        "confusion_matrix.csv": metrics.confusion_matrix.to_csv(),
        "confusion_matrix.json": metrics.confusion_matrix.to_json(),
    }

    for name, content in outputs.items():
        output_path = tmp_path / name
        output_path.write_text(content, encoding="utf-8")
        assert output_path.exists()
        assert output_path.stat().st_size > 0


@pytest.mark.slow
def test_sam_inference(tmp_path):
    """Test: notebooks/inference-with-meta-sam-and-sam2-using-ultralytics-python-package.ipynb."""
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()

    sam_model = SAM("sam2.1_b.pt")
    assert sam_model(ASSETS / "bus.jpg")
    assert sam_model(ASSETS / "bus.jpg", points=[34, 714])
    assert sam_model(ASSETS / "bus.jpg", points=[[34, 714], [283, 634]])
    assert sam_model(ASSETS / "bus.jpg", bboxes=[3.83287, 229.3560, 796.2098, 728.4313])

    for image_name in ("bus.jpg", "zidane.jpg"):
        _download_asset(f"https://ultralytics.com/assets/{image_name}", assets_dir)

    output_dir = tmp_path / "auto-annotate"
    auto_annotate(
        data=assets_dir,
        det_model="yolo26n.pt",
        sam_model="sam_b.pt",
        output_dir=output_dir,
    )

    assert list(output_dir.glob("*.txt"))
