import os

from line_image_to_text.create_csv import process_work_folder
from line_image_to_text.crop_and_reorganize_image import reorganize_cropped_images
from line_image_to_text.download_images_bdrc import download_work_images
from line_image_to_text.filter_work import filter_line_images
from line_image_to_text.ocr_line_image_and_rearrange_json import rearrange_json_text
from line_image_to_text.reorganize_jsons_file import process_json_files


def pipeline(
    input_jsons_folder_path: str, image_output_folder: str, csv_output_folder: str
):
    """this file reorganizes the json files into new sturucture and reorganizes the json files"""
    process_json_files(input_jsons_folder_path)
    """ download the images in the folder"""

    print("processing json files done.")
    for json_folder_path in os.listdir(input_jsons_folder_path):

        json_folder_path = os.path.join(input_jsons_folder_path, json_folder_path)
        download_work_images(json_folder_path)
        print(f"{json_folder_path}: downloading done.")
        image_folder_path = os.path.join("./data")
        # reorganize the image

        reorganize_cropped_images(json_folder_path, image_folder_path)
        print(f"{json_folder_path}: reorganizing cropping image done. ")
        rearrange_json_text(json_folder_path)
        print(f"{json_folder_path}: rearranging text done. ")
        filter_line_images(json_folder_path)
        print(f"{json_folder_path}: filtering line images done. ")
        process_work_folder(json_folder_path, image_output_folder, csv_output_folder)
        print(f"{json_folder_path}: creating csv done.")


if __name__ == "__main__":
    input_jsons_folder_path = "../../json_input_folder"
    image_output_folder = "../../image_ouput/image"
    csv_output_folder = "../../csv_output/csv/csv"
    pipeline(input_jsons_folder_path, image_output_folder, csv_output_folder)
