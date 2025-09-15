import unittest
from unittest.mock import patch, MagicMock
from .extracted_text_to_llms_response import FrameTextProcessor  # adjust import if needed


class TestFrameTextProcessor(unittest.TestCase):
    def setUp(self):
        self.frames_dir = "/fake/frames"
        self.output_csv = "/fake/output.csv"
        self.processor = FrameTextProcessor(self.frames_dir, self.output_csv)

        # Mock save_results so no actual file is written
        self.processor.save_results = MagicMock()

    @patch("os.listdir", return_value=["frame1.png"])
    @patch("cv2.imread", return_value="fake_image")
    @patch("cv2.cvtColor", return_value="gray_image")
    @patch("pytesseract.image_to_string", return_value="hello")
    def test_process_single_frame(self, mock_pytesseract, mock_cvtColor, mock_imread, mock_listdir):
        # Mock llama._call on the instance
        self.processor.llama._call = MagicMock(return_value="definition of hello")

        self.processor.process_frames(target_frame="frame1.png")

        # Assert llama._call was called once
        self.processor.llama._call.assert_called_once()
        self.assertEqual(len(self.processor.results), 1)
        self.assertEqual(self.processor.results[0]["llama_output"], "definition of hello")

        # Ensure save_results was called
        self.processor.save_results.assert_called_once()

    @patch("os.listdir", return_value=["frame1.png", "frame2.png"])
    @patch("cv2.imread", return_value="fake_image")
    @patch("cv2.cvtColor", return_value="gray_image")
    @patch("pytesseract.image_to_string", return_value="world")
    def test_process_all_frames(self, mock_pytesseract, mock_cvtColor, mock_imread, mock_listdir):
        # Mock llama._call on the instance
        self.processor.llama._call = MagicMock(return_value="definition of world")

        self.processor.process_frames()  # process all

        # Check results
        self.assertEqual(len(self.processor.results), 2)
        for r in self.processor.results:
            self.assertEqual(r["llama_output"], "definition of world")

        # Ensure llama._call was called twice
        self.assertEqual(self.processor.llama._call.call_count, 2)

        # Ensure save_results was called once
        self.processor.save_results.assert_called_once()

    def test_create_strict_system_definition(self):
        prompt = self.processor.create_strict_system_definition("hello")
        self.assertIn("Word: hello", prompt)
        self.assertIn("give its concise definition in English", prompt)

    def test_extract_text_from_frame_with_invalid_image(self):
        with patch("cv2.imread", return_value=None):
            with self.assertRaises(ValueError):
                self.processor.extract_text_from_frame("/fake/path.png")


if __name__ == "__main__":
    unittest.main()
