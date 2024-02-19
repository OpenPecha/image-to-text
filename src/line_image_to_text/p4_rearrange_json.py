import json
import os
from typing import Dict

import Levenshtein
import pytesseract
from PIL import Image

# Define a threshold for similarity score
SIMILARITY_THRESHOLD = 0.5


def load_json_data(json_path: str) -> Dict:
    try:
        with open(json_path, encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load JSON data: {e}")
        return {}


def ocr_process_image(image_path: str) -> str:
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang="bod")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""


def find_closest_match(ocr_text, texts):
    best_match = ""
    highest_similarity = -1
    for etext in texts:
        similarity = Levenshtein.ratio(ocr_text, etext)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = etext
    return best_match, highest_similarity


def save_json_data(json_data: Dict, output_path: str) -> None:
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save updated data: {e}")


def update_json_entries(
    volume_path: str, page_id: str, page_data: Dict, texts: list
) -> None:
    for line_id, line_data in page_data.items():
        if line_id == "text":
            continue  # Skip the 'text' key

        line_image_path = os.path.join(volume_path, page_id.split(".")[0], line_id)
        ocr_text = ocr_process_image(line_image_path)
        closest_match, similarity_score = find_closest_match(ocr_text, texts)

        # Update the JSON data with OCR result and closest match
        line_data["ocr_text"] = ocr_text
        if similarity_score >= SIMILARITY_THRESHOLD:
            line_data["rearranged_text"] = closest_match
        else:
            line_data["rearranged_text"] = "no matching text found"


def process_volume_folder(work_folder_path: str, volume_id: str, volume_item: Dict):
    volume_path = os.path.join(work_folder_path, "image", volume_id)
    processed_marker_path = os.path.join(volume_path, ".processed")

    if not os.path.exists(volume_path):
        print(
            f"Skipping unorganized processed volume: {volume_id} in {work_folder_path}"
        )
        return

    if os.path.exists(processed_marker_path):
        print(f"Skipping already processed volume: {volume_id} in {work_folder_path}")
        return

    for page_id, page_data in volume_item.items():
        if page_id == "text":
            continue
        texts = page_data.get("text", [])
        update_json_entries(volume_path, page_id, page_data, texts)

    json_file_path = os.path.join(
        work_folder_path, f"{os.path.basename(work_folder_path)}.json"
    )
    json_data = load_json_data(json_file_path)  # Load the most current JSON data
    json_data[volume_id] = volume_item  # Update the specific volume data
    save_json_data(json_data, json_file_path)  # Save the entire JSON data back to file

    with open(processed_marker_path, "w") as file:
        file.write("Processed")


def process_work_folder(work_folder_path: str):
    json_file_path = os.path.join(
        work_folder_path, f"{os.path.basename(work_folder_path)}.json"
    )
    if os.path.exists(json_file_path):
        json_data = load_json_data(json_file_path)
        for volume_id, volume_item in json_data.items():
            process_volume_folder(work_folder_path, volume_id, volume_item)
            # Save updated volume_item back to JSON file


def rearrange_json_text(json_folder_path: str):

    # Navigate through each work folder in super_folder_1
    for work_folder in os.listdir(json_folder_path):
        work_folder_path = os.path.join(json_folder_path, work_folder)
        process_work_folder(work_folder_path)


if __name__ == "__main__":
    json_folder_path = "/media/gangagyatso/media files/third_problem"
    image_folder_path = "/home/gangagyatso/Desktop/project16/data"
    rearrange_json_text(json_folder_path)
