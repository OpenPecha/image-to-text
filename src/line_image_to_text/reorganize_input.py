import json
import os
import shutil
from typing import Dict, List


def load_json_data(json_path):
    with open(json_path, encoding="utf-8") as file:
        return json.load(file)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def copy_image_to_folder(image_name, source_folders, dest_folder):
    image_found = False
    for folder in source_folders:
        image_path = os.path.join(folder, image_name)
        if os.path.exists(image_path):
            shutil.copy(image_path, dest_folder)
            image_found = True
            break

    if not image_found:
        print(f"Image {image_name} not found in any of the source folders.")


if __name__ == "__main__":
    json_path = "../../data/input/image_coordinates_and_text.json"
    json_data = load_json_data(json_path)

    # Directories where images are stored
    image_folders = [
        "../../data/input/Images_Part_1",
        "../../data/input/Images_Part_2",
        "../../data/input/Images_Part_3",
        "../../data/input/Images_Part_4",
        "../../data/input/Images_Part_5",
    ]

    # Base directory to store new folders and JSON files
    base_directory = "../../data/input_rearranged"

    # Group data by work ID
    work_data: Dict[str, List[Dict]] = {}
    for entry in json_data:
        work_id = entry["book_id"]
        work_data.setdefault(work_id, []).append(entry)

    # Process each work ID
    for work_id, entries in work_data.items():
        work_folder = os.path.join(base_directory, work_id)
        create_folder(work_folder)

        # Create JSON file for each work ID
        json_filename = f"{work_id}.json"
        json_file_path = os.path.join(work_folder, json_filename)
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(entries, json_file, indent=4)

        # Copy images to the work ID folder
        image_folder = os.path.join(work_folder, "images")
        create_folder(image_folder)
        for entry in entries:
            image_name = entry["image_name"]
            copy_image_to_folder(image_name, image_folders, image_folder)

    print("Reorganization complete.")
