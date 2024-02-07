import csv
import json
import os
import shutil


# Function to load JSON data
def load_json_data(file_path):
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


# Function to write data to CSV and organize images
def process_data(super_folder, base_filename, images_base_folder, max_rows=25000):
    batch_num = 1
    row_count = 0
    csv_file_path = f"{base_filename}_batch_{batch_num}.csv"
    images_batch_folder = f"{images_base_folder}_batch_{batch_num}"

    os.makedirs(images_batch_folder, exist_ok=True)

    for root, dirs, files in os.walk(super_folder):
        for name in files:
            if name.startswith("valid"):  # Process files that begin with 'valid'

                json_data = load_json_data(os.path.join(root, name))
                images_folder = "images"  # Path to images folder
                # Ensure the directory for the CSV file exists
                os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

                with open(
                    csv_file_path, mode="a", newline="", encoding="utf-8"
                ) as csv_file:
                    writer = csv.writer(csv_file)
                    if batch_num == 1 and row_count == 0:
                        writer.writerow(
                            ["source", "line_image_id", "repo_name", "text"]
                        )

                    for item in json_data:
                        if row_count >= max_rows:
                            batch_num += 1
                            csv_file_path = f"{base_filename}_batch_{batch_num}.csv"
                            images_batch_folder = (
                                f"{images_base_folder}_batch_{batch_num}"
                            )
                            os.makedirs(images_batch_folder, exist_ok=True)
                            row_count = 0

                            csv_file.close()
                            # Ensure the directory for the CSV file exists
                            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
                            csv_file = open(
                                csv_file_path, mode="w", newline="", encoding="utf-8"
                            )
                            writer = csv.writer(csv_file)
                            writer.writerow(
                                ["source", "line_image_id", "repo_name", "text"]
                            )

                        source = (
                            f'{item["book_id"]}/{item["volume"]}/{item["origin_image"]}'
                        )
                        line_image_id = item["image_name"]
                        repo_name = item["repo_id"]
                        text = item.get("rearranged_text", "")
                        writer.writerow([source, line_image_id, repo_name, text])

                        # Copy image to batch folder
                        img_path = os.path.join(root, images_folder, line_image_id)
                        shutil.copy(img_path, images_batch_folder)
                        row_count += 1


# Example usage
super_folder = "/home/gangagyatso/Desktop/project16/image-to-text/data/input_rearranged"
base_filename = (
    "/home/gangagyatso/Desktop/project16/image-to-text/data/output/csv/image"
)
images_base_folder = (
    "/home/gangagyatso/Desktop/project16/image-to-text/data/output/images/image"
)
process_data(super_folder, base_filename, images_base_folder)
