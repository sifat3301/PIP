import os
import cv2
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
import pandas as pd
from llama_service import LLaMAWrapper

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
frames_dir = os.path.join(parent_dir, "task_1", "stored_frames")
output_csv = os.path.join(parent_dir, "llama_output.csv")


def extract_text_from_frame(frame_path: str) -> str:
    frame = cv2.imread(frame_path)
    if frame is None:
        raise ValueError(f"Could not read image: {frame_path}")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text


def create_strict_system_definition(extracted_text: str, language: str="English"):
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


# LLAMA which is run on my machine
llama = LLaMAWrapper(endpoint="http://localhost:11434/api/generate")

results = []

for frame_file in os.listdir(frames_dir):
    frame_path = os.path.join(frames_dir, frame_file)
    extracted_text = extract_text_from_frame(frame_path)
    language = 'English'
    prompt = create_strict_system_definition(extracted_text, language)
    llama_response = llama._call(prompt)
    results.append({
        "filename": frame_file,
        "extracted_text": extracted_text,
        "llama_output": llama_response
    })
    print(f"Processed {frame_file}: {llama_response[:100]}...")  # first 100 chars

# --- Save results to CSV ---
df = pd.DataFrame(results)
df.to_csv(output_csv, index=False, encoding="utf-8")
print(f"\nAll results saved to {output_csv}")
