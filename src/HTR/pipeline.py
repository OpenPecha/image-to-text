from pathlib import Path
from HTR.creat_correction_csv import parse_xml_and_create_jsonl, create_csv_for_correction
from HTR.create_manual_csv import  create_csv_for_manual
from utils import upload_to_s3


def get_xml_paths(source_dir):
    xml_paths = []
    data_paths = list(source_dir.iterdir())
    for data_path in data_paths:
        if data_path.name[-3:] == "xml":
            xml_paths.append(data_path)
    return xml_paths


def upload_line_images(line_dir, batch_id):
    for line_path in line_dir.iterdir():
        image_name = line_path.name
        s3_key = f"Marieke/Correction/{batch_id}/{image_name}"
        upload_to_s3(line_path, s3_key)

def create_correction_data():
    batch_id = "Correction-9"
    line_name = "line-9"
    group_id = 1
    source_dir = Path(f"./data/Marieke/{batch_id}/")
    xml_paths = get_xml_paths(source_dir)
    line_dir = Path(f"./data/Marieke/{line_name}/")
    csv_path = Path(f"./data/{batch_id}.csv")
    correction_jsonl = parse_xml_and_create_jsonl(xml_paths, line_dir, source_dir)
    upload_line_images(line_dir, batch_id)
    create_csv_for_correction(correction_jsonl, csv_path, batch_id, group_id)


def create_manual_data():
    batch_id = "Manual-3"
    group_id = 2
    image_paths = list(Path(f"./data/Marieke/{batch_id}1/").iterdir())
    csv_path = Path(f"./data/{batch_id}.csv")
    create_csv_for_manual(image_paths, csv_path, batch_id, group_id)


if __name__ == "__main__":
    create_correction_data()
    
   