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


if __name__ == "__main__":
    main()