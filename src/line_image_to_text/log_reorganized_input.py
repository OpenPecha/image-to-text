import json
import logging
import os


def setup_logging(log_file_path):
    """Set up the logging configuration."""
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s",
    )


def count_files_in_folder(folder_path):
    """Count the number of files in a given folder."""
    return len(
        [
            name
            for name in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, name))
        ]
    )


def count_items_in_json(json_path):
    """Count the number of items in a JSON file."""
    try:
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
        return len(data) if isinstance(data, list) else 0
    except Exception as e:
        logging.error(f"Error reading {json_path}: {e}")
        return 0


def process_work_id_folders(super_folder):
    total_images = 0
    total_json_items = 0
    mismatched_folders = []

    for work_id_folder in os.listdir(super_folder):
        work_id_path = os.path.join(super_folder, work_id_folder)
        if os.path.isdir(work_id_path):
            image_folder = os.path.join(work_id_path, "images")
            json_file = os.path.join(work_id_path, f"{work_id_folder}.json")

            image_count = (
                count_files_in_folder(image_folder)
                if os.path.exists(image_folder)
                else 0
            )
            json_item_count = (
                count_items_in_json(json_file) if os.path.exists(json_file) else 0
            )

            total_images += image_count
            total_json_items += json_item_count

            if image_count != json_item_count:
                mismatch_count = abs(image_count - json_item_count)
                mismatched_folders.append((work_id_folder, mismatch_count))
                mismatch_info = (
                    f"{work_id_folder}: {image_count} images, "
                    f"{json_item_count} JSON: mismatch count {mismatch_count}"
                )
                print(mismatch_info)
                logging.info(mismatch_info)

    return total_images, total_json_items, mismatched_folders


# Example usage
log_file_path = "../../data/input_rearranged/mismatch_log.txt"  # Path to log file
setup_logging(log_file_path)

super_folder = "../../data/input_rearranged"  # Replace with your super folder path
total_images, total_json_items, mismatches = process_work_id_folders(super_folder)
print(f"Total images: {total_images}, Total JSON items: {total_json_items}")

if mismatches:
    print("Mismatch details logged in:", log_file_path)
else:
    print(
        "No mismatches found between image counts and JSON item counts. Log file created."
    )
