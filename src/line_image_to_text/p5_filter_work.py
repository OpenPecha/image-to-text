import json
import os

from botok import WordTokenizer

wt = WordTokenizer()


def load_json_data(json_path):
    with open(json_path, encoding="utf-8") as file:
        return json.load(file)


def is_tibetan_num_exist(tokens):
    return any(token.chunk_type == "NUM" for token in tokens)


def is_width_greater_than_height(crop_coords):
    left, upper, right, lower = crop_coords
    return (right - left) > (lower - upper)


def is_valid_text_len(text):
    return len(text) > 5


def is_non_word_exist(tokens):
    return any(token.pos == "NON_WORD" for token in tokens)


def is_non_bo_word_exist(tokens):
    return any(
        token.chunk_type in ["LATIN", "CJK", "OTHER"] and not token.skrt
        for token in tokens
    )


def filter_and_save_data(volume_path, volume_item):
    valid_data = {}
    invalid_data = {}

    for page_id, page_data in volume_item.items():
        for line_id, line_data in page_data.items():
            if line_id == "text":
                continue
            text = line_data.get("rearranged_text", "")
            try:
                tokens = wt.tokenize(text)
                if (
                    is_width_greater_than_height(line_data["line_image_coord"])
                    and is_valid_text_len(text)
                    and not is_non_word_exist(tokens)
                    and not is_non_bo_word_exist(tokens)
                    and not is_tibetan_num_exist(tokens)
                ):
                    valid_data[line_id] = line_data
                else:
                    invalid_data[line_id] = line_data
            except Exception as error:
                print(f"Error processing {line_id}: {error}")
                invalid_data[line_id] = line_data

    # Save valid and invalid data separately with the same structure as the original JSON
    if valid_data:
        valid_json_path = os.path.join(volume_path, "valid_data.json")
        with open(valid_json_path, "w", encoding="utf-8") as file:
            json.dump(valid_data, file, indent=4)

    if invalid_data:
        invalid_json_path = os.path.join(volume_path, "invalid_data.json")
        with open(invalid_json_path, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file, indent=4)


def process_volume_folder(work_folder_path, volume_id, volume_item):
    volume_path = os.path.join(work_folder_path, "image", volume_id)
    if not os.path.exists(volume_path):
        print(f"Skipping non-existent volume: {volume_id} in {work_folder_path}")
        return

    processed_marker_path = os.path.join(volume_path, ".processed")
    filtered_marker_path = os.path.join(volume_path, ".filter")

    if not os.path.exists(processed_marker_path):
        print(f"Skipping unprocessed volume: {volume_id} in {work_folder_path}")
        return

    if os.path.exists(filtered_marker_path):
        print(f"Skipping already filtered volume: {volume_id} in {work_folder_path}")
        return

    filter_and_save_data(volume_path, volume_item)

    with open(filtered_marker_path, "w") as file:
        file.write("filtered")


def process_work_folder(work_folder_path: str):
    json_file_path = os.path.join(
        work_folder_path, f"{os.path.basename(work_folder_path)}.json"
    )
    if os.path.exists(json_file_path):
        try:
            json_data = load_json_data(json_file_path)
            for volume_id, volume_item in json_data.items():
                process_volume_folder(work_folder_path, volume_id, volume_item)
        except Exception as error:
            print(f"Error processing {json_file_path}: {error}")


def filter_line_images(json_folder_path: str):

    # Navigate through each work folder in super_folder_1
    for work_folder in os.listdir(json_folder_path):
        work_folder_path = os.path.join(json_folder_path, work_folder)
        process_work_folder(work_folder_path)


if __name__ == "__main__":
    json_folder_path = "/media/gangagyatso/media files/third_problem"
    image_folder_path = "/home/gangagyatso/Desktop/project16/data"

    filter_line_images(json_folder_path)
