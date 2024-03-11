import os
from multiprocessing import Pool

from line_image_to_text.create_csv import process_work_folder
from line_image_to_text.crop_and_reorganize_image import reorganize_cropped_images
from line_image_to_text.download_images_bdrc import download_work_images
from line_image_to_text.filter_work import filter_line_images
from line_image_to_text.ocr_line_image_and_rearrange_json import rearrange_json_text
from line_image_to_text.reorganize_jsons_file import process_json_files


def process_json_folder(json_folder_path, image_output_folder, csv_output_folder):
    """Process a single JSON folder."""
    download_work_images(json_folder_path)
    print(f"{json_folder_path}: downloading done.")
    image_folder_path = os.path.join("./data")
    # Reorganize the image
    reorganize_cropped_images(json_folder_path, image_folder_path)
    print(f"{json_folder_path}: reorganizing cropping image done.")
    rearrange_json_text(json_folder_path)
    print(f"{json_folder_path}: rearranging text done.")
    filter_line_images(json_folder_path)
    print(f"{json_folder_path}: filtering line images done.")
    process_work_folder(json_folder_path, image_output_folder, csv_output_folder)
    print(f"{json_folder_path}: creating csv done.")


def pipeline(
    input_jsons_folder_path: str, image_output_folder: str, csv_output_folder: str
):
    """Reorganize json files and process them in parallel using multiprocessing."""
    process_json_files(input_jsons_folder_path)
    print("Processing JSON files done.")
    json_folder_paths = os.listdir(input_jsons_folder_path)

    # Prepare arguments for each process
    args = [
        (
            os.path.join(input_jsons_folder_path, json_folder_path),
            image_output_folder,
            csv_output_folder,
        )
        for json_folder_path in json_folder_paths
    ]

    # Number of processes
    num_processes = 2  # You can adjust this based on your system's capabilities

    # Create a pool of workers and distribute the tasks
    with Pool(processes=num_processes) as pool:
        pool.starmap(process_json_folder, args)


if __name__ == "__main__":
    input_jsons_folder_path = "../../json_input_folder"
    image_output_folder = "../../image_ouput/image"
    csv_output_folder = "../../csv_output/csv/csv"
    pipeline(input_jsons_folder_path, image_output_folder, csv_output_folder)
