from pathlib import Path
import jsonlines
import os


def create_text_file(jsonl_path, text_file_path):
    text_file_path.mkdir(parents=True, exist_ok=True)
    with jsonlines.open(jsonl_path) as reader:
        for line in reader:
            if line["answer"] == "accept":
                if line["user_input"] == "":
                    continue
                image_name = line["id"].split(".")[0]
                text = line["user_input"]
                with open(text_file_path/f"{image_name}.txt", "w") as writer:
                    writer.write(text)

if __name__ == "__main__":
    jsonl_paths = Path(f"./data/line_image_to_text/reviewed/").iterdir()
    for jsonl_path in jsonl_paths:
        batch = jsonl_path.name.split("_")[-1].split(".")[0]
        create_text_file(jsonl_path, Path(f"./data/line_image_to_text/text_files/{batch}/"))