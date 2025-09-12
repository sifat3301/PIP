import os
import cv2
import pytesseract

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
base_frames_dir = os.path.join(parent_dir, "task_1")
frames_dir = os.path.join(base_frames_dir, "stored_frames")


def extract_text_from_frame(frame_path=None):
    frame = cv2.imread(frame_path)
    if frame is None:
        raise ValueError(f"Could not read image: {frame_path}")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

for i in range(len(os.listdir(frames_dir))):
    frame_file = os.listdir(frames_dir)[i]
    frame_path = os.path.join(frames_dir, frame_file)

    print(extract_text_from_frame(frame_path=frame_path))
