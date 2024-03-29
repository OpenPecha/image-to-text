import contextlib
import json
import os

from bdrc_images_and_ocr_downloader.download import download_images
from bdrc_images_and_ocr_downloader.work_info import get_hash, get_s3_folder_prefix


def construct_s3_key(work_id, image_group_id, image_file_name):
    hash_prefix = get_hash(work_id)
    s3key, image_group_suffix = get_s3_folder_prefix(
        work_id=work_id, image_group_lname=image_group_id
    )

    s3_key = f"Works/{hash_prefix}/{work_id}/images/{work_id}-{image_group_suffix}/{image_file_name}"
    return s3_key


def download_work_images(json_folder_path: str):
    # Integrate downloading into the workflow
    work_folder = json_folder_path.split("/")[-1]
    work_folder_path = json_folder_path

    if os.path.isdir(work_folder_path):
        json_file_path = os.path.join(work_folder_path, work_folder + ".json")
        if not os.path.exists(json_file_path):
            print(f"JSON file does not exist: {json_file_path}")

        with open(json_file_path) as json_file:
            data = json.load(json_file)
            s3_keys = []

            for volume_id, volume_item in data.items():
                # Construct the S3 key for each image based on item data
                work_id = work_folder  # Assuming 'book_id' is used as 'work_id'
                image_group_id = (
                    volume_id  # Assuming 'volume' refers to 'image_group_id'
                )
                for image_name in volume_item.keys():
                    image_file_name = image_name  # Assuming this is the image file name
                    s3_key = construct_s3_key(work_id, image_group_id, image_file_name)
                    s3_keys.append(s3_key)
                # Download images
            with contextlib.redirect_stdout(open(os.devnull, "w")):
                download_images(s3_keys)


if __name__ == "__main__":
    json_folder_path = "/media/gangagyatso/media files/third_problem"
    download_work_images(json_folder_path)
