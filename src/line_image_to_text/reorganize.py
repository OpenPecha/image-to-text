import glob
import json
import os
import shutil  # Import shutil for copying files


def process_json_files(folder_path):
    # Iterate through each JSON file in the folder
    for json_file in glob.glob(os.path.join(folder_path, "*.json")):
        with open(json_file, encoding="utf-8") as file:
            data = json.load(file)

        if not data:  # Skip empty files or files with no data
            continue

        # Assume all items in a file have the same book_id, get book_id from the first item
        book_id = data[0].get("book_id", "default_book_id")
        work_folder_name = book_id  # Use book_id as the folder name
        work_folder_path = os.path.join(folder_path, work_folder_name)

        # Create the work folder if it doesn't exist
        os.makedirs(work_folder_path, exist_ok=True)

        new_data = []  # List to hold the reformatted data

        for item in data:
            origin_image = item.get("origin_image")
            volume = item.get("volume")
            book_id = item.get("book_id")
            repo_id = item.get("repo_id")
            rectangles = item.get("rectangles", [])
            text_lines = item.get("text", [])
            base_name, original_ext = os.path.splitext(origin_image)

            for i, rectangle in enumerate(rectangles):
                image_name = f"{base_name}_{i}{original_ext}"  # Use original extension
                pil_coords = (
                    item.get("pil_crop_rectangle_coords", [])[i]
                    if i < len(item.get("pil_crop_rectangle_coords", []))
                    else []
                )
                text = text_lines[i] if i < len(text_lines) else ""

                new_item = {
                    "rectangle_coords": rectangle,
                    "pil_crop_rectangle_coords": pil_coords,
                    "origin_image": origin_image,
                    "image_name": image_name,
                    "has_digit_in_text": any(char.isdigit() for char in text),
                    "volume": volume,
                    "book_id": book_id,
                    "repo_id": repo_id,
                    "text": text,
                }

                new_data.append(new_item)

            # Handle case where there are more text lines than rectangles
            image_size = len(rectangles)
            for extra_text in text_lines[image_size:]:
                extra_item = new_item.copy()  # Copy the last item
                extra_item["text"] = extra_text  # Update the text
                new_data.append(extra_item)

        # Define the new file name and path
        new_file_name = f"{work_folder_name}.json"
        new_file_path = os.path.join(work_folder_path, new_file_name)

        # Write the new data to the new JSON file within the work folder
        with open(new_file_path, "w", encoding="utf-8") as new_file:
            json.dump(new_data, new_file, ensure_ascii=False, indent=4)

        # Move the original JSON file to the work folder
        original_file_new_path = os.path.join(
            work_folder_path, os.path.basename(json_file)
        )
        shutil.move(json_file, original_file_new_path)


# Example usage
folder_path = "../../data/third_problem"
process_json_files(folder_path)
