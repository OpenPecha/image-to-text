import csv
from utils import add_row_to_csv
from pathlib import Path
from HTR.creat_correction_csv import extract_text_with_lines

def create_csv_for_manual(image_paths, csv_path, batch_id, group_id):
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, csv_path)
    for image_path in image_paths:
        id = image_path.name.strip().replace("\n", "")
        if id[-3:] == "xml":
            continue
        xml_path = image_path.with_suffix(".xml")
        state = "transcribing"
        inference_transcript = extract_text_with_lines(xml_path)
        image_url = f"https://s3.us-east-1.amazonaws.com/monlam.ai.ocr/Marieke/Normalisation/Source/{batch_id}/{id}"
        format = "page"
        row = [id, group_id, batch_id, state, inference_transcript,image_url, format]
        add_row_to_csv(row, csv_path)
    
def read_csv(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        return list(reader)

def create_csv_for_manual_2(csv_path, batch_id, group_id, output_csv_path):
    data = read_csv(csv_path)
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, output_csv_path)
    for row in data[1:]:
        id = row[0].strip().replace("\n", "")
        image_url = f"https://s3.us-east-1.amazonaws.com/monlam.ai.ocr/Marieke/Correction-source/Correction-9/{id}"
        format = "page"
        inference_transcript = row[3]
        state = "transcribing"
        new_row = [id, group_id, batch_id, state, inference_transcript,image_url, format]
        add_row_to_csv(new_row, output_csv_path)


def create_manual_data():
    batch_id = "Normalisation-4"
    group_id = 1
    csv_path = Path(f"./{batch_id}.csv")
    output_csv_path = Path(f"./data/{batch_id}-data.csv")
    create_csv_for_manual_2(csv_path, batch_id, group_id, output_csv_path)


if __name__ == "__main__":
    create_manual_data()