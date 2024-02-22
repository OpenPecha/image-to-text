from pathlib import Path
from utils import list_obj_keys
from config import MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client

s3_client = monlam_ai_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET


def download_images(scan_id, obj_keys):
    for obj_key in obj_keys:
        image_name = obj_key.split("/")[-1]
        output_path = Path(f"./data/{scan_id}")
        output_path.mkdir(parents=True, exist_ok=True)
        image_path = output_path/image_name
        if image_path.exists():
            continue
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=obj_key)
            image_data = response['Body'].read()
            with open(image_path, 'wb') as f:
                f.write(image_data)
        except Exception as e:
            print(f"Error: {e}")


def get_images_from_s3(batch_name):
    obj_keys = list_obj_keys(prefix=f"line_to_text/{batch_name}", s3_client=s3_client, bucket_name=bucket_name)
    download_images(batch_name, obj_keys)

if __name__ == "__main__":
    batch_name = "batch18"
    get_images_from_s3(batch_name)