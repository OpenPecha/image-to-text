from pathlib import Path
import jsonlines
import csv
from config import MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client

s3_client = monlam_ai_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

def write_jsonl(jsonl, jsonl_path):
    with jsonlines.open(jsonl_path, mode='w') as writer:
        writer.write_all(jsonl)

def write_csv(csv, csv_path):
    with open(csv_path, mode='w') as writer:
        writer.write_all(csv)


def create_jsonl(batch_name, image_paths, jsonl_path):
    final_jsonl = []
    for image_path in list(image_paths.iterdir()):
        image_id = image_path.stem
        image_name = image_path.name
        image_key = f"line_to_text/{batch_name}/{image_name}"
        final_jsonl.append({"id":image_id, "image_url": image_key, "user_input": ""})
    write_jsonl(final_jsonl, jsonl_path)


def get_new_url(image_url):
    new_image_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": image_url},
        ExpiresIn=31536000
    )
    return new_image_url


def create_csv(batch_name, image_paths, csv_path):
    for image_path in list(image_paths.iterdir()):
        image_id = image_path.stem
        image_name = image_path.name
        image_key = f"line_to_text/{batch_name}/{image_name}"
        image_url = get_new_url(image_key)
        text = ""
        line = [image_id,image_url,text]
        with open(csv_path,'a') as f:
            writer = csv.writer(f)
            writer.writerow(line)

def make_line_to_text_jsonl(batch_names):
    for batch_name in batch_names:
        image_paths = Path(f"./data/images/{batch_name}/")
        jsonl_path = Path(f"./data/jsonl/{batch_name}.jsonl")
        create_jsonl(batch_name,image_paths, jsonl_path)

def make_line_to_text_csv(batch_names):
    for batch_name in batch_names:
        image_paths = Path(f"data/images/{batch_name}/")
        csv_path = Path(f"data/csv/{batch_name}.csv")
        create_csv(batch_name, image_paths, csv_path)


def main():
    format = "csv"
    batch_names = ["batch21"]
    if format == "jsonl":
        make_line_to_text_jsonl(batch_names)
    else:
        make_line_to_text_csv(batch_names)

if __name__ == "__main__":
    main()