from tqdm import tqdm
from pathlib import Path
from utils import is_archived
from config import MONLAM_AI_OCR_BUCKET, monlam_ai_ocr_s3_client


s3_client = monlam_ai_ocr_s3_client
bucket_name = MONLAM_AI_OCR_BUCKET

def upload_images_to_s3_bucket(image_paths, prefix):

    # Wrap the iterdir() with tqdm for a progress bar
    for image_path in tqdm(list(image_paths.iterdir()), desc="Uploading images"):
        image_name = image_path.name
        image_key = f"{prefix}/{image_name}"
        if is_archived(image_key, s3_client, bucket_name):
            continue
        s3_client.upload_file(str(image_path), bucket_name, image_key)

def main():
    prefix = "line_to_text/batch2"
    image_paths = Path(f"./data/images/batch2/")
    upload_images_to_s3_bucket(image_paths, prefix)

if __name__ == "__main__":
    main()
