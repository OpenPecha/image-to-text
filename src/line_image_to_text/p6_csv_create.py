import csv
import json
import os
import shutil


def load_json_data(file_path):
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def count_rows_in_csv(file_path):
    """Counts the number of rows in a CSV file, excluding the header row."""
    with open(file_path, encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)  # Remove this line if your CSV does not have a header
        row_count = sum(1 for row in reader)
    return row_count


def process_volume(volume_path, image_output_folder, csv_output_folder):
    os.makedirs(
        os.path.dirname(csv_output_folder), exist_ok=True
    )  # Ensure directory exists
    os.makedirs(
        os.path.dirname(image_output_folder), exist_ok=True
    )  # Ensure directory exists

    csv_created_marker_path = os.path.join(volume_path, ".cs")
    if os.path.exists(csv_created_marker_path):
        print(f"Skipping already csv created folder: {volume_path}")
        return
    # Extracting volume_id and work_folder_name from the volume_path
    volume_id = os.path.basename(volume_path)
    images_folder_path = os.path.dirname(volume_path)
    work_folder_path = os.path.dirname(images_folder_path)
    work_folder_name = os.path.basename(work_folder_path)

    json_file_name = "valid_data.json"
    json_file_path = os.path.join(volume_path, json_file_name)
    if not os.path.exists(json_file_path):
        return  # Skip if JSON file does not exist

    json_data = load_json_data(json_file_path)

    csv_file_path = f"{csv_output_folder}-{work_folder_name}.csv"
    csv_file = open(
        csv_file_path,
        mode="a+" if os.path.exists(csv_file_path) else "w",
        newline="",
        encoding="utf-8",
    )
    writer = csv.writer(csv_file)

    images_batch_folder = f"{image_output_folder}-{work_folder_name}"
    os.makedirs(images_batch_folder, exist_ok=True)

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

        # Process and write current line data to CSV
        source = f"{work_folder_name}/{volume_id}/{line_id.split('_')[0]}"
        repo_name = line_data.get("repo_id", "")
        text = line_data.get("rearranged_text", "")
        writer.writerow([source, line_id, repo_name, text])
        row_count += 1  # Increment row count after writing

        # Attempt to copy the associated image to the current image batch folder
        line_image_path = os.path.join(volume_path, line_id.split("_")[0], line_id)
        if os.path.exists(line_image_path):
            try:
                shutil.copy(line_image_path, images_batch_folder)
            except Exception as e:
                print(f"Error copying image: {e}")

    csv_file.close()  # Ensure the CSV file is closed after processing all items

    with open(csv_created_marker_path, "w") as file:
        file.write("csv_created")


def process_work_folder(work_folder_path, image_output_folder, csv_output_folder):
    for volume_id in os.listdir(os.path.join(work_folder_path, "image")):
        volume_path = os.path.join(work_folder_path, "image", volume_id)
        process_volume(volume_path, image_output_folder, csv_output_folder)


def create_csv(
    json_folder_path: str,
    image_output_folder: str,
    csv_output_folder: str,
):

    # Integrate downloading into the workflow
    work_folder_path = json_folder_path
    process_work_folder(work_folder_path, image_output_folder, csv_output_folder)


if __name__ == "__main__":
    json_folder_path = "/media/gangagyatso/media files/third_problem"
    image_output_folder = "/media/gangagyatso/docs/output2/images/image"
    csv_output_folder = "/media/gangagyatso/docs/output2/csv/csv"
    create_csv(json_folder_path, image_output_folder, csv_output_folder)
