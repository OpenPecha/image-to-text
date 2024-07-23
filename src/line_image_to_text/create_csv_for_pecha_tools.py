from pathlib import Path
import csv
from utils import add_row_to_csv


def create_new_csv_for_pecha_tools(csv_path):
    batch_name = csv_path.stem
    if batch_name == "batch_1":
        return
    output_path = Path(f"./data/numbers/{batch_name}.csv")
    batch_id = f"{batch_name}"
    add_row_to_csv(["id", "group_id", "batch_id", "state", "inference_transcript", "url"], output_path)
    with open(csv_path, "r") as f:
        reader = list(csv.reader(f))
        for row in reader[1:]:
            id = row[1]
            url = f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka_numbers/images/{batch_name}/{id}"
            group_id = 11
            state = "transcribing"
            inference_transcript = row[3]
            new_row = [id, group_id, batch_id, state, inference_transcript, url]
            add_row_to_csv(new_row, output_path)


def main():
    csv_paths = list(Path("data/norbuketaka").iterdir())
    for csv_path in csv_paths:
        if csv_path.stem == "batch_3":
            create_new_csv_for_pecha_tools(csv_path)

def create_csv_from_transcription():
    batch_id = "batch25"
    output_path = Path(f"./data/{batch_id}.csv")
    add_row_to_csv(["id", "group_id", "batch_id", "state", "inference_transcript", "url"], output_path)
    txt_paths = list(Path("data/transcriptions/").iterdir())
    for txt_path in txt_paths:
        image_name = txt_path.name
        text = txt_path.read_text(encoding='utf-8')
        id = image_name.split(".")[0]
        url = f"https://s3.amazonaws.com/monlam.ai.ocr/line_to_text/{batch_id}/{id}.jpg"
        group_id = 11
        state = "transcribing"
        inference_transcript = text
        new_row = [id, group_id, batch_id, state, inference_transcript, url]
        add_row_to_csv(new_row, output_path)



if __name__ == "__main__":
    create_csv_from_transcription()



