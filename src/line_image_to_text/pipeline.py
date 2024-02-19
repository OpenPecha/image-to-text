from line_image_to_text.p1_reorganize import process_json_files
from line_image_to_text.p2_download_images_bdrc import download_work_images
from line_image_to_text.p3_reorganise_image import reorganize_cropped_images
from line_image_to_text.p4_rearrange_json import rearrange_json_text
from line_image_to_text.p5_filter_work import filter_line_images
from line_image_to_text.p6_csv_create import create_csv


def pipeline(json_folder_path: str, image_output_folder: str, csv_output_folder: str):
    """this file reorganizes the json files into new sturucture and reorganizes the json files"""
    process_json_files(json_folder_path)
    """ download the images in the folder"""
    download_work_images(json_folder_path)
    image_folder_path = "/home/gangagyatso/Desktop/line_filter/image-to-text/data"
    """ reorganize the images"""

    reorganize_cropped_images(json_folder_path, image_folder_path)

    rearrange_json_text(json_folder_path)

    filter_line_images(json_folder_path)

    create_csv(json_folder_path, image_output_folder, csv_output_folder)


if __name__ == "__main__":
    json_folder_path = "./json_input_folder"
    image_output_folder = "./image_ouput/image"
    csv_output_folder = "./csv_output/csv/csv"
    pipeline(json_folder_path, image_output_folder, csv_output_folder)
