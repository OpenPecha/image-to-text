from pathlib import Path
from utils import add_row_to_csv


def create_csv(image_paths, csv_path, batch_id, group_id):
    headers = ["id","group_id","batch_id","state","inference_transcript","url"]
    add_row_to_csv(headers, csv_path)
    for image_path in image_paths:
        id = image_path.name
        state = "transcribing"
        inference_transcript = ""
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/line_to_text/{batch_id}/{id}"
        row = [id, group_id, batch_id, state, inference_transcript, image_url]
        add_row_to_csv(row, csv_path)




def main():
    image_paths = list(Path("/Users/tashitsering/Desktop/lines/batch32").iterdir())
    batch_id = "batch32"
    group_id = 12
    csv_path = Path(f"./data/{batch_id}.csv")
    create_csv(image_paths, csv_path, batch_id, group_id)


if __name__ == "__main__":
    main()
