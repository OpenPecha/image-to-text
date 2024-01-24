import json
import os

from botok import WordTokenizer

wt = WordTokenizer()


def load_json_data(json_path):
    """Load JSON data from the given file path."""
    with open(json_path, encoding="utf-8") as file:
        return json.load(file)


def find_common_images(image_folder, json_data):
    """Find common images in both the folder and the JSON data."""
    json_images = {item["image_name"] for item in json_data}
    folder_images = set(os.listdir(image_folder))
    return json_images.intersection(folder_images)


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


def filter_data(image_folder, json_data):
    valid_pairs = []
    invalid_pairs = []
    common_images = find_common_images(image_folder, json_data)
    print("common files count", len(common_images))

    for entry in json_data:
        image_name = entry["image_name"]
        if image_name not in common_images:
            continue

        image_path = os.path.join(image_folder, image_name)
        try:
            tokens = wt.tokenize(entry["text"])

            # Apply filters
            if (
                os.path.exists(image_path)
                and is_width_greater_than_height(entry["pil_crop_rectangle_coords"])
                and not entry[
                    "has_digit_in_text"
                ]  # gets the boolean value from the json file
                and is_valid_text_len(entry["text"])
                and not non_word_exist(tokens)
                and not non_bo_word_exist(tokens)
            ):
                valid_pairs.append(image_name)
            else:
                invalid_pairs.append(image_name)

        except IndexError:
            print(f"IndexError processing text for image {image_name}. Skipping.")
            invalid_pairs.append(image_name)
        except AttributeError:
            print(f"AttributeError processing text for image {image_name}. Skipping.")
            invalid_pairs.append(image_name)
        except Exception as error:
            print(
                f"Unhandled error processing text for image {image_name}: {error}. Skipping."
            )
            invalid_pairs.append(image_name)

    return valid_pairs, invalid_pairs


def write_pairs_to_json(valid_pairs, invalid_pairs, filename):
    """Write the valid and invalid pairs to a JSON file."""
    data = {"valid_images": valid_pairs, "invalid_images": invalid_pairs}
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    super_folder = "/home/gangagyatso/Desktop/project15"
    json_path = "/home/gangagyatso/Desktop/project15/image_coordinates_and_text.json"
    json_data = load_json_data(json_path)
    all_valid_filtered_data = []
    all_invalid_filtered_data = []
    output_filename = "/home/gangagyatso/Desktop/project15/valid_and_invalid_image.json"

    # Process each subfolder within the super folder
    for folder_name in os.listdir(super_folder):
        subfolder_path = os.path.join(super_folder, folder_name)
        if os.path.isdir(subfolder_path):
            valid_images, invalid_images = filter_data(subfolder_path, json_data)
            all_valid_filtered_data.extend(valid_images)
            all_invalid_filtered_data.extend(invalid_images)

    write_pairs_to_json(
        all_valid_filtered_data, all_invalid_filtered_data, output_filename
    )

    print("Valid images:", len(all_valid_filtered_data))
    print("Invalid images:", len(all_invalid_filtered_data))
    # Process all_filtered_data as needed
