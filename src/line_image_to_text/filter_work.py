import json
import os
import shutil

from botok import WordTokenizer

wt = WordTokenizer()


def tibetan_num_exist(tokens):
    for token in tokens:
        if token.chunk_type == "NUM":
            return True
    return False


def load_json_data(json_path):
    """Load JSON data from the given file path."""
    with open(json_path, encoding="utf-8") as file:
        return json.load(file)


def is_width_greater_than_height(crop_coords):
    """Check if the width of the area defined by crop_coords is greater than its height."""
    left, upper, right, lower = crop_coords
    width = right - left
    height = lower - upper
    return width > height


def is_valid_text_len(text):
    if len(text) > 5:
        return True
    return False


def non_word_exist(tokens):
    for token in tokens:
        if token.pos == "NON_WORD":
            return True
    return False


def non_bo_word_exist(tokens):
    for token in tokens:
        if token.chunk_type in ["LATIN", "CJK", "OTHER"] and (
            token.chunk_type != "OTHER" or not token.skrt
        ):
            return True
    return False


def move_invalid_image(image_path, invalid_folder):
    if not os.path.exists(invalid_folder):
        os.makedirs(invalid_folder)
    shutil.move(image_path, invalid_folder)


def filter_data(image_folder, json_data, work_id_folder):
    valid_pairs = []
    invalid_pairs = []  # Store invalid entries
    invalid_folder = os.path.join(work_id_folder, "invalid_images")

    for entry in json_data:
        image_name = entry["image_name"]
        image_path = os.path.join(image_folder, image_name)

        try:
            tokens = wt.tokenize(entry["rearranged_text"])
            # Apply filters
            if (
                os.path.exists(image_path)
                and is_width_greater_than_height(entry["pil_crop_rectangle_coords"])
                and not entry["has_digit_in_text"]
                and is_valid_text_len(entry["rearranged_text"])
                and not non_word_exist(tokens)
                and not non_bo_word_exist(tokens)
                and not tibetan_num_exist(tokens)
            ):
                valid_pairs.append(entry)
            else:
                move_invalid_image(image_path, invalid_folder)
                invalid_pairs.append(entry)  # Add entry to invalid list

        except Exception as error:
            print(
                f"Error processing image {image_name}: {error}. Moving to invalid folder."
            )
            move_invalid_image(image_path, invalid_folder)
            invalid_pairs.append(entry)

    # Write invalid entries to a separate JSON file
    if invalid_pairs:
        invalid_json_path = os.path.join(
            work_id_folder, f"invalid_{os.path.basename(work_id_folder)}.json"
        )
        with open(invalid_json_path, "w", encoding="utf-8") as json_file:
            json.dump(invalid_pairs, json_file, indent=4)

    if valid_pairs:
        valid_json_path = os.path.join(
            work_id_folder, f"valid_{os.path.basename(work_id_folder)}.json"
        )
        with open(valid_json_path, "w", encoding="utf-8") as json_file:
            json.dump(valid_pairs, json_file, indent=4)


def process_work_id_folder(work_id_folder):
    json_file_path = os.path.join(
        work_id_folder, f"rearranged_{os.path.basename(work_id_folder)}.json"
    )
    image_folder = os.path.join(work_id_folder, "images")

    if os.path.exists(json_file_path) and os.path.isdir(image_folder):
        json_data = load_json_data(json_file_path)
        filter_data(image_folder, json_data, work_id_folder)
    else:
        print(f"Missing JSON file or image folder in {work_id_folder}")


if __name__ == "__main__":
    super_folder = (
        "/home/gangagyatso/Desktop/project18/monlam_ocr/data/input_rearranged"
    )

    for work_id in os.listdir(super_folder):
        work_id_path = os.path.join(super_folder, work_id)
        if os.path.isdir(work_id_path):
            process_work_id_folder(work_id_path)

    print("Filtering complete.")
