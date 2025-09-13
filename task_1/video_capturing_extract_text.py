import os
import cv2
import glob
import pytesseract


pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

print(pytesseract.get_tesseract_version())


class VideoPlayer:
    def __init__(self, path: str, save_dir: str = None, interval: int = 10, **kwargs):
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.save_dir = save_dir
        self.interval_type = kwargs.get('interval_type', 'second')
        self.is_persist = kwargs.get('is_persist', False)
        self.interval = 60 * interval if self.interval_type.lower() == 'minutes' else interval
        self.frame_count = 0
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_interval = int(self.fps * self.interval)
        self.max_duration = kwargs.get("max_duration", None)

    def __extract_text_from_frame(self, frame=None, file_path=None):
        if self.is_persist:
            if file_path is None or not os.path.exists(file_path):
                raise ValueError("File path must exist when is_persist=True")
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            if frame is None:
                raise ValueError("Frame must be provided when is_persist=False")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray)
        return text

    def __prepare_save_dir(self):
        if self.is_persist:
            if os.path.exists(self.save_dir):
                files = glob.glob(os.path.join(self.save_dir, "*"))
                for f in files:
                    os.remove(f)
            else:
                os.makedirs(self.save_dir, exist_ok=True)

    def __process_frame(self, frame):
        file_path = None
        if self.is_persist:
            file_path = os.path.join(self.save_dir, f"{self.frame_count}.jpg")
            cv2.imwrite(file_path, frame)

        text = self.__extract_text_from_frame(
            frame=frame if not self.is_persist else None,
            file_path=file_path
        )
        print(f"Frame {self.frame_count} text:\n{text}\n{'-' * 50}")

    def play(self):
        if not self.cap.isOpened():
            print(f"Error: Cannot open video {self.path}")
            return

        print(f"fps: {self.fps}, frame_interval: {self.frame_interval}")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            cv2.imshow("Video", frame)
            if self.frame_count % self.frame_interval == 0:
                self.__process_frame(frame)
            self.frame_count += 1

            if self.max_duration and (self.frame_count / self.fps) >= self.max_duration:
                print(f"Max duration {self.max_duration}s reached, stopping video.")
                break

            if cv2.waitKey(int(1000 / self.fps)) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = "TextBasedExplainerVideo.mp4"
    video_player = VideoPlayer(
        video_path,
        save_dir="stored_frames",
        interval=1,
        is_persist=True,
        interval_type="second",
        max_duration=10
    )
    video_player.play()
