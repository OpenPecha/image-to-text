import json
import os
from typing import Dict, List

import Levenshtein
import pytesseract
from PIL import Image

# Define a threshold for similarity score
SIMILARITY_THRESHOLD = 0.5  # You can adjust this value based on your requirements


def load_json_data(json_path: str) -> List[Dict]:
    try:
        with open(json_path, encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load JSON data: {e}")
        return []


def ocr_process_image(image_path: str) -> str:
    try:
        return pytesseract.image_to_string(Image.open(image_path), lang="bod")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return ""


def find_closest_match(ocr_text, json_entries):
    best_match = ""
    highest_similarity = -1

    for entry in json_entries:
        etext = entry["text"]
        similarity = Levenshtein.ratio(ocr_text, etext)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = etext

    return best_match, highest_similarity


def update_json_entries(image_folder: str, json_data: List[Dict]) -> None:
    for entry in json_data:
        image_path = os.path.join(image_folder, entry["image_name"])
        ocr_text = ocr_process_image(image_path)
        closest_match, similarity_score = find_closest_match(ocr_text, json_data)

        entry["ocr_text"] = ocr_text  # Storing OCR result separately

        # Check if the similarity score is above the threshold
        if similarity_score >= SIMILARITY_THRESHOLD:
            entry["rearranged_text"] = closest_match
        else:
            entry["rearranged_text"] = "no matching text found"

        # Additional logic for low similarity cases can be added here


# Rest of your code remains the same


def save_updated_data(json_data: List[Dict], output_path: str) -> None:
    try:
        # Check if the output_path is a directory
        if os.path.isdir(output_path):
            # If it's a directory, set the file name to output.json within that directory
            output_path = os.path.join(
                output_path, f"rearranged_{os.path.basename(output_path)}.json"
            )

        # Open the file and write the JSON data
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save updated data: {e}")


def process_work_folder(work_folder_path: str):
    # Assuming each work folder contains an image folder and a single JSON file
    image_folder = None
    json_file = None

    for item in os.listdir(work_folder_path):
        item_path = os.path.join(work_folder_path, item)
        if os.path.isdir(item_path):
            image_folder = item_path
        elif item.endswith(".json"):
            json_file = item_path

    if image_folder and json_file:
        json_data = load_json_data(json_file)
        if json_data:
            update_json_entries(image_folder, json_data)
            save_updated_data(json_data, work_folder_path)
    else:
        print(f"Missing image folder or JSON file in {work_folder_path}")


def main():
    super_folder_path = "../../data/input_rearrange"
    for work_folder in os.listdir(super_folder_path):
        work_folder_path = os.path.join(super_folder_path, work_folder)
        if os.path.isdir(work_folder_path):
            process_work_folder(work_folder_path)


if __name__ == "__main__":
    main()
