import os
import cv2
import pytesseract
import pandas as pd
import argparse
from .llama_service import LLaMAWrapper

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


class FrameTextProcessor:
    def __init__(self, frames_dir: str, output_csv: str, llama_endpoint: str = "http://localhost:11434/api/generate"):
        self.frames_dir = frames_dir
        self.output_csv = output_csv
        self.llama = LLaMAWrapper(endpoint=llama_endpoint)
        self.results = []

    def extract_text_from_frame(self, frame_path: str) -> str:
        frame = cv2.imread(frame_path)
        if frame is None:
            raise ValueError(f"Could not read image: {frame_path}")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text

    def create_strict_system_definition(self, extracted_text: str, language: str = "English") -> str:
        word = extracted_text.strip() if extracted_text else "Nothing"
        prompt = (
            f"Instruction: You are only allowed to provide the definition of the given word.\n"
            f"- If the word is understood, give its concise definition in {language}.\n"
            f"- If the word is not understood, return `Nothing`.\n"
            f"- If the word does not exist in an English dictionary, return `Nothing`.\n"
            f"- If the word is `Nothing`, return `Nothing`.\n"
            f"- Do not add anything before the definition; only output the definition itself.\n"
            f"- Never ask questions or provide extra explanations.\n\n"
            f"Word: {word}"
        )
        return prompt

    def process_frames(self, target_frame: str = "all"):
        frame_files = os.listdir(self.frames_dir)
        if target_frame != "all":
            frame_files = [target_frame] if target_frame in frame_files else []
            if not frame_files:
                print(f"Frame '{target_frame}' not found in {self.frames_dir}")
                return

        for frame_file in frame_files:
            frame_path = os.path.join(self.frames_dir, frame_file)
            extracted_text = self.extract_text_from_frame(frame_path)
            prompt = self.create_strict_system_definition(extracted_text)
            llama_response = self.llama._call(prompt)
            self.results.append({
                "filename": frame_file,
                "extracted_text": extracted_text,
                "llama_output": llama_response
            })
            print(f"Processed {frame_file}: {llama_response[:100]}...")  # first 100 chars

        self.save_results()

    def save_results(self):
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_csv, index=False, encoding="utf-8")
        print(f"\nAll results saved to {self.output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process frames and extract text using LLaMA.")
    parser.add_argument(
        "--frame",
        type=str,
        default="all",
        help="Specify a single frame to process, or 'all' to process all frames (default: all)"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="English",
        help="Specify the language of the extracted text. (default: English)"
    )
    args = parser.parse_args()

    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    frames_dir = os.path.join(parent_dir, "task_1", "stored_frames")
    output_csv = os.path.join(parent_dir, "llama_output.csv")

    processor = FrameTextProcessor(frames_dir, output_csv)
    processor.process_frames(target_frame=args.frame)
