from pathlib import Path
import csv
from utils import add_row_to_csv

def read_csv(csv_filepath):
    data_list = []
    # This is where you'd make the change
    with open(csv_filepath, mode='r', encoding='utf-8-sig', newline='') as file: # <-- Key change here!
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list

def generate_image_url(id, batch_id):
    # batch_num = htr_batch_id.split("-")[1]
    # batch_id = f"Correction-{batch_num}"
    base_url = "https://s3.us-east-1.amazonaws.com/monlam.ai.ocr/Marieke/Normalisation/Source/"
    return f"{base_url}{batch_id}/{id}"

def create_new_csv(csv_data):
    ids = []
    images = Path("./cropped_images.txt").read_text().splitlines()
    existing_ids = Path("./all_ids.txt").read_text().splitlines()
    csv_path = Path("Normalisation-7-data.csv")
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, csv_path)
    for item in csv_data:
        id = item['id'].replace("\n", "")
        if id not in images or id in ids or id in existing_ids:
            continue
        ids.append(id)
        batch_id = "Normalisation-7"
        group_id = "1"
        state = "transcribing"
        inference_transcript = item['transcript']
        format = "page"
        image_url = generate_image_url(id, batch_id)
        row = [id, group_id, batch_id, state, inference_transcript, image_url, format]
        add_row_to_csv(row, csv_path)

if __name__ == "__main__":
    csv_path = Path("./Normalisation-7.csv")
    csv_data = read_csv(csv_path)
    create_new_csv(csv_data)
