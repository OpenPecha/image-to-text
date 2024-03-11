import csv
import json
import os
import shutil

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


def count_rows_in_csv(file_path):
    """Counts the number of rows in a CSV file, excluding the header row."""
    with open(file_path, encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)  # Remove this line if your CSV does not have a header
        row_count = sum(1 for row in reader)
    return row_count


def process_volume(volume_path, image_output_folder, csv_output_folder, max_rows=25000):
    os.makedirs(
        os.path.dirname(csv_output_folder), exist_ok=True
    )  # Ensure directory exists
    os.makedirs(
        os.path.dirname(image_output_folder), exist_ok=True
    )  # Ensure directory exists

    csv_created_marker_path = os.path.join(volume_path, ".csv_creteeedssss")
    if os.path.exists(csv_created_marker_path):
        print(f"Skipping already csv created folder: {volume_path}")
        return
    # Extracting volume_id and work_folder_name from the volume_path
    volume_id = os.path.basename(volume_path)
    images_folder_path = os.path.dirname(volume_path)
    work_folder_path = os.path.dirname(images_folder_path)
    work_folder_name = os.path.basename(work_folder_path)

    json_file_name = "invalid_data.json"
    json_file_path = os.path.join(volume_path, json_file_name)
    if not os.path.exists(json_file_path):
        return  # Skip if JSON file does not exist

    json_data = load_json_data(json_file_path)

    batch_num = 1
    for file in os.listdir(os.path.dirname(csv_output_folder)):
        if file.endswith(".csv"):
            batch_num += 1
    batch_num = 1 if batch_num <= 1 else batch_num - 1
    images_batch_folder = f"{image_output_folder}batch_{batch_num}"
    os.makedirs(images_batch_folder, exist_ok=True)
    csv_file_path = f"{csv_output_folder}batch_{batch_num}.csv"
    csv_file = open(
        csv_file_path,
        mode="a+" if os.path.exists(csv_file_path) else "w",
        newline="",
        encoding="utf-8",
    )
    writer = csv.writer(csv_file)
    if os.path.getsize(csv_file_path) == 0:  # If file is new, write the header
        writer.writerow(["source", "line_image_id", "repo_name", "text"])
    row_count = (
        count_rows_in_csv(csv_file_path) if os.path.getsize(csv_file_path) > 0 else 0
    )

    ...
    # Start processing the JSON data
    for line_id in json_data.keys():

        if line_id == "text":  # Skip 'text' key, as it's not an actual data entry
            continue

        line_data = json_data[line_id]  # Get the data for this line

        if row_count >= max_rows:  # Check if we need to start a new batch
            csv_file.close()  # Close the current CSV file before starting a new batch
            batch_num += 1  # Increment batch number for a new batch
            images_batch_folder = f"{image_output_folder}batch_{batch_num}"  # Define new image batch folder
            os.makedirs(
                images_batch_folder, exist_ok=True
            )  # Create the new image batch folder
            csv_file_path = (
                f"{csv_output_folder}batch_{batch_num}.csv"  # Define new CSV file path
            )
            csv_file = open(
                csv_file_path, mode="w", newline="", encoding="utf-8"
            )  # Open new CSV file
            writer = csv.writer(csv_file)  # Create a writer for the new CSV
            writer.writerow(
                ["source", "line_image_id", "repo_name", "text"]
            )  # Write header in new CSV
            row_count = 0  # Reset row count for the new CSV

        # Process and write current line data to CSV
        source = f"{work_folder_name}/{volume_id}/{line_id.split('_')[0]}"
        repo_name = line_data.get("repo_id", "")
        text = line_data.get("rearranged_text", "")
        try:
            tokens = wt.tokenize(text)
            if (
                is_width_greater_than_height(line_data["line_image_coord"])
                and is_valid_text_len(text)
                and not is_non_word_exist(tokens)
                and not is_non_bo_word_exist(tokens)
                and is_tibetan_num_exist(tokens)
            ):
                writer.writerow([source, line_id, repo_name, text])
                row_count += 1  # Increment row count after writing
                # Attempt to copy the associated image to the current image batch folder
                line_image_path = os.path.join(
                    volume_path, line_id.split("_")[0], line_id
                )
                if os.path.exists(line_image_path):
                    try:
                        shutil.copy(line_image_path, images_batch_folder)
                    except Exception as e:
                        print(f"Error copying image: {e}")

        except Exception as error:
            print(f"Error processing {line_id}: {error}")

    csv_file.close()  # Ensure the CSV file is closed after processing all items

    with open(csv_created_marker_path, "w") as file:
        file.write("csv_created")


def process_work_folder(work_folder_path, image_output_folder, csv_output_folder):
    for volume_id in os.listdir(os.path.join(work_folder_path, "image")):
        volume_path = os.path.join(work_folder_path, "image", volume_id)
        process_volume(volume_path, image_output_folder, csv_output_folder)
