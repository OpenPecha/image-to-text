from utils import add_row_to_csv


def create_csv_for_manual(image_paths, csv_path, batch_id, group_id):
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, csv_path)
    for image_path in image_paths:
        id = image_path.name
        state = "transcribing"
        inference_transcript = ""
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/Marieke/Manual/{batch_id}/{id}"
        format = "page"
        row = [id, group_id, batch_id, state, inference_transcript,image_url, format]
        add_row_to_csv(row, csv_path)

