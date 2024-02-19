import json
import os

from PIL import Image


def get_suffix(image_group_lname):
    pre, rest = image_group_lname[0], image_group_lname[1:]
    if pre == "I" and rest.isdigit() and len(rest) == 4:
        suffix = rest
    else:
        suffix = image_group_lname
    return suffix


def crop_image(image_path, crop_coords):
    try:
        with Image.open(image_path) as img:
            width, height = img.size  # type: ignore
            print(f"Image dimensions: {width}x{height}")
            print(f"Cropping with coordinates: {crop_coords}")

            # Ensure crop coordinates are within image dimensions
            left, top, right, bottom = crop_coords
            left = max(0, min(left, width - 1))
            top = max(0, min(top, height - 1))
            right = max(left + 1, min(right, width))
            bottom = max(top + 1, min(bottom, height))

            # Crop the image
            cropped_img = img.crop((left, top, right, bottom))  # type: ignore
            return cropped_img
    except Exception as e:
        print(f"Error cropping image {image_path}: {e}")
        return None


def reorganize_cropped_images(json_folder_path: str, image_folder_path: str):

    # Navigate through each work folder in super_folder_1
    for work_folder in os.listdir(json_folder_path):
        work_folder_path = os.path.join(json_folder_path, work_folder)

        json_file_path = os.path.join(work_folder_path, work_folder + ".json")
        if not os.path.exists(json_file_path):
            continue  # Skip if JSON file does not exist

        with open(json_file_path) as json_file:
            data = json.load(json_file)

        for volume_id, volume_item in data.items():
            work_id = work_folder
            image_folder_volume_path = os.path.join(
                work_folder_path, "image", volume_id
            )
            os.makedirs(image_folder_volume_path, exist_ok=True)

            csv_created_marker_path = os.path.join(image_folder_volume_path, ".cs")
            if os.path.exists(csv_created_marker_path):
                print(
                    f"Skipping already csv created folder: {image_folder_volume_path}"
                )
                continue

            for page_id, page_data in volume_item.items():
                for line_image_id, line_image_data in page_data.items():
                    if line_image_id == "text":
                        continue
                    coords = line_image_data.get("line_image_coord", [])

                    image_group_suffix = get_suffix(volume_id)
                    origin_image_folder = f"{work_id}-{image_group_suffix}"
                    origin_image_path = os.path.join(
                        image_folder_path,
                        work_folder,
                        origin_image_folder,
                        "images",
                        page_id,
                    )

                    if not os.path.exists(origin_image_path):
                        print(f"Origin image does not exist: {origin_image_path}")
                        continue

                    line_image_folder_path = os.path.join(
                        work_folder_path, "image", volume_id, page_id.split(".")[0]
                    )
                    os.makedirs(line_image_folder_path, exist_ok=True)

                    cropped_image_path = os.path.join(
                        line_image_folder_path, line_image_id
                    )

                    if os.path.exists(cropped_image_path):
                        # print(f"cropped image does already exist: {cropped_image_path}")
                        continue

                    cropped_image = crop_image(origin_image_path, coords)
                    if cropped_image is not None:
                        try:
                            cropped_image.save(cropped_image_path)
                            print(f"Image successfully saved to {cropped_image_path}")
                        except OSError as e:
                            print(f"Failed to save image. OSError: {e}")
                        except Exception as e:
                            print(
                                f"An unexpected error occurred while saving the image: {e}"
                            )


if __name__ == "__main__":
    # Define paths to the super folders
    json_folder_path = "/media/gangagyatso/media files/third_problem"
    image_folder_path = "/home/gangagyatso/Desktop/project16/data"
