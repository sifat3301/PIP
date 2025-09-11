import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from task_1.video_capturing_extract_text import VideoPlayer


@pytest.fixture
def dummy_frame():
    """Return a dummy image frame (black image)."""
    return np.zeros((100, 100, 3), dtype=np.uint8)


@pytest.fixture
def tmp_save_dir(tmp_path):
    return str(tmp_path / "frames")


def test_init_params(tmp_save_dir):
    with patch("cv2.VideoCapture", return_value=MagicMock()) as mock_cap:
        vp = VideoPlayer(
            path="TextBasedExplainerVideo.mp4",
            save_dir=tmp_save_dir,
            interval=1,
            is_persist=True,
            interval_type="second",
            max_duration=10
        )
        assert vp.path == "TextBasedExplainerVideo.mp4"
        assert vp.save_dir == tmp_save_dir
        assert vp.is_persist
        assert vp.interval_type == "second"
        assert vp.max_duration == 10
        assert vp.interval == 1
        mock_cap.assert_called_once_with("TextBasedExplainerVideo.mp4")


def test_extract_text_from_frame_with_frame(dummy_frame):
    vp = VideoPlayer("video.mp4", "frames", is_persist=False)
    with patch("pytesseract.image_to_string", return_value="dummy text") as mock_tesseract:
        text = vp._VideoPlayer__extract_text_from_frame(frame=dummy_frame)
        assert text == "dummy text"
        mock_tesseract.assert_called_once()



def test_extract_text_raises_errors():
    vp = VideoPlayer("video.mp4", "frames", is_persist=False)
    # Missing frame
    with pytest.raises(ValueError):
        vp._VideoPlayer__extract_text_from_frame()

    vp_persist = VideoPlayer("video.mp4", "frames", is_persist=True)
    with pytest.raises(ValueError):
        vp_persist._VideoPlayer__extract_text_from_frame(file_path="nonexistent.jpg")


def test_prepare_save_dir_creates_and_cleans(tmp_save_dir):
    os.makedirs(tmp_save_dir, exist_ok=True)
    file_path = os.path.join(tmp_save_dir, "old.jpg")
    open(file_path, "w").close()

    vp = VideoPlayer("video.mp4", tmp_save_dir, is_persist=True)
    vp._VideoPlayer__prepare_save_dir()

    assert os.path.exists(tmp_save_dir)
    assert not os.listdir(tmp_save_dir)


def test_process_frame(tmp_save_dir, dummy_frame):
    vp = VideoPlayer("video.mp4", tmp_save_dir, is_persist=True)
    vp.frame_count = 0
    with patch.object(vp, "_VideoPlayer__extract_text_from_frame", return_value="text") as mock_extract, \
         patch("cv2.imwrite", return_value=True):
        vp._VideoPlayer__process_frame(dummy_frame)
        mock_extract.assert_called_once()


def test_play_video_end_and_max_duration(dummy_frame, tmp_save_dir):
    vp = VideoPlayer("video.mp4", tmp_save_dir, interval=1, max_duration=1)

    # Mock VideoCapture
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.side_effect = [(True, dummy_frame)] * 50 + [(False, None)]
    mock_cap.get.return_value = 25  # fps
    vp.cap = mock_cap
    vp.fps = 25
    vp.frame_interval = 1

    with patch("cv2.imshow"), patch("cv2.waitKey", return_value=-1), \
         patch.object(vp, "_VideoPlayer__process_frame") as mock_process, \
         patch("cv2.destroyAllWindows"):
        vp.play()
        assert vp.frame_count <= 25
        assert mock_process.called


def test_play_video_quit_key(dummy_frame):
    vp = VideoPlayer("video.mp4", "frames", interval=1)

    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.side_effect = [(True, dummy_frame), (True, dummy_frame), (False, None)]
    mock_cap.get.return_value = 30
    vp.cap = mock_cap
    vp.fps = 30
    vp.frame_interval = 1

    # Simulate pressing 'q'
    with patch("cv2.imshow"), patch("cv2.waitKey", return_value=ord('q')), \
         patch.object(vp, "_VideoPlayer__process_frame"):
        vp.play()
        # Should stop immediately after 'q'
        assert vp.frame_count == 0 or vp.frame_count == 1
