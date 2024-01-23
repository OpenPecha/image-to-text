import json
import os


def load_json_data(json_path):
    """Load JSON data from the given file path."""
    with open(json_path, encoding="utf-8") as file:
        return json.load(file)


def find_common_images(image_folder, json_data):
    """Find common images in both the folder and the JSON data."""
    json_images = {item["image_name"] for item in json_data}
    folder_images = set(os.listdir(image_folder))
    return json_images.intersection(folder_images)


def is_valid_image(image_path):
    pass


def non_word_exist(text):
    pass


def non_bo_word_exist(text):
    pass


def filter_data(image_folder, json_data):
    """Filter images based on dimensions, digit presence in text, and text length."""
    valid_pairs = []
    common_images = find_common_images(image_folder, json_data)

    for entry in json_data:
        image_name = entry["image_name"]
        if image_name not in common_images:
            continue

        image_path = os.path.join(image_folder, image_name)
        # Apply filters
        if (
            is_valid_image(image_path)
            and not entry["has_digit_in_text"]
            and len(entry["text"]) > 6
        ):
            if not non_word_exist(entry["text"]) and not non_bo_word_exist(
                entry["text"]
            ):
                valid_pairs.append((image_path, entry["text"]))

    return valid_pairs


# Example usage
image_folder = "/path/to/image/folder"
json_path = "/path/to/json/file.json"

json_data = load_json_data(json_path)
filtered_data = filter_data(image_folder, json_data)

# Process filtered_data as needed
