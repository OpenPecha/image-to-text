from pathlib import Path
import csv
from utils import get_image_name, add_row_to_csv


def get_csv_data(batch_id):
    with open(f'./data/{batch_id}_DB.csv', newline='') as csvfile:
        csv_list = list(csv.reader(csvfile, delimiter=','))
        image_list = []
        for row in csv_list[1:]:
            image_name = row[0]
            image_list.append(image_name)
    return image_list

def get_images(image_keys):
    image_names = []
    for image_key in image_keys[1:]:
        image_name = image_key.split("/")[-1]
        image_names.append(image_name)
    return image_names


def filter_images(prefix, batch_id):
    remaining_images = []
    image_keys = get_image_name(prefix)
    image_names = get_images(image_keys)
    db_data = get_csv_data(batch_id)
    for image_name in image_names:
        if image_name in db_data:
            continue
        else:
            remaining_images.append(image_name)
    return remaining_images



def get_csv(image_list, batch_id):
    csv_path = Path(f"./{batch_id}.csv")
    headers = ["id","group_id","batch_id","state","inference_transcript","url"]
    add_row_to_csv(headers, csv_path)
    for image_name in image_list:
        id = image_name
        group_id = "12"
        state = "transcribing"
        inference_transcript = ""
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/OCR/line_to_text/{batch_id}/{image_name}"
        batch_id = batch_id
        row = [id, group_id, batch_id, state, inference_transcript, image_url]
        add_row_to_csv(row, csv_path)


def main():
    batch_id = "batch28"
    prefix = f"line_to_text/{batch_id}/"
    remaining_images = filter_images(prefix, batch_id)
    get_csv(remaining_images, batch_id)


if __name__ == "__main__":
    main()