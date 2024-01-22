from pathlib import Path
import jsonlines
import requests



def add_to_csv(id, style_id, text, image_url):
    ids = []
    if id in ids:
        return
    if len(style_id) == 0:
        csv_file =  Path(f"./data/csv/not_classified.csv")
    elif style_id[0] == 0:
        csv_file =  Path(f"./data/csv/others.csv")
    elif style_id[0] == 2:
        csv_file =  Path(f"./data/csv/Uchan.csv")
    elif style_id[0] == 1:
        csv_file =  Path(f"./data/csv/Umen.csv")
    with open(csv_file, "a") as f:
        f.write(f"{id},{text},{image_url}\n")
        ids.append(id)


def parse_rechecked_jsonl(jsonl_file):
    """
    Parse rechecked jsonl file to get the text and the label
    """
    with jsonlines.open(jsonl_file) as reader:
        for obj in reader:
            if obj['answer'] == "accept":
                id = obj['id']
                style_id = obj['accept']
                text = obj['user_input']
                image_url = obj['image'].split("?")[0]
                add_to_csv(id, style_id, text, image_url)








if __name__ == "__main__":
    jsonl_files = list(Path(f"./data/rechecked").iterdir())
    for jsonl_file in jsonl_files:
        parse_rechecked_jsonl(jsonl_file)