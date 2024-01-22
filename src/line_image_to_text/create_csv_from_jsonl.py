from pathlib import Path
import jsonlines
import csv


transcriber_id_to_annotators_map = {
    

    "ngawangsamten1989@gmail.com": 15,
    "dhondup995@gmail.com": 16,
    "dhekharwork123@gmail.com": 19,
    "khedup62@gmail.com": 14,
    "thubsamtharchin1982@gmail.com": 17,
    "tenzintherchen154@gmail.com": 20,
    "kungachoden1983@gmail.com" : 22,
    "tsedhak123@gmail.com": 23,
    "dhephala@gmail.com": 24,
    "tthegchok1985@gmail.com": 27,
    "Kungalhundup1959@gamil.com": 26,
    "dakar": 19
}


def add_row_to_csv(row, csv_path):
    if Path(csv_path).exists():
        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    else:
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)


def get_transcriber_id(obj):
    annotator_name = obj["_annotator_id"].split("-")[1]
    transcriber_id = transcriber_id_to_annotators_map[annotator_name]
    return int(transcriber_id)

def get_image_url(image_name, batch_id):
    image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/line_to_text/{batch_id}/{image_name}"
    return image_url


def parse_jsonl_and_create_csv(jsonl_path, csv_path):
    headers = ["id","group_id","batch_id","state","inference_transcript","transcript","url", "transcriber_id"]
    add_row_to_csv(headers, csv_path)
    ids = []
    with jsonlines.open(jsonl_path) as reader:
        for obj in reader:
            id = obj["id"]
            if id in ids:
                continue
            if obj["answer"] == "accept":
                state = "submitted"
            else:
                state = "trashed"
            group_id = 9
            batch_id = "batch19"
            inference_transcript = ""
            transcript = obj["user_input"]
            image_url = get_image_url(obj["image"], batch_id)
            transcriber_id = get_transcriber_id(obj)
            row = [id, group_id, batch_id, state, inference_transcript, transcript, image_url, transcriber_id]
            add_row_to_csv(row, csv_path)
            row = []
            ids.append(id)



def create_csv():
    batch_id = "batch22"
    group_id = 8
    ids = []
    csv_path = f"./data/line_to_text_{batch_id}.csv"
    image_paths = Path(f"./data/images/{batch_id}").iterdir()
    headers = ["id","group_id","batch_id","state","inference_transcript","url"]
    add_row_to_csv(headers, csv_path)
    ids = []
    for iamge_path in image_paths:
        id = iamge_path.name
        if id in ids:
            continue
        state = "transcribing"
        inference_transcript = ""
        image_url = get_image_url(id, batch_id)
        row = [id, group_id, batch_id, state, inference_transcript, image_url]
        add_row_to_csv(row, csv_path)
        row = []
        ids.append(id)

        
if __name__ == "__main__":
    create_csv()
    # jsonl_path = "./data/line_to_text_batch19.jsonl"
    # csv_path = "./data/line_to_text_batch19.csv"
    # parse_jsonl_and_create_csv(jsonl_path, csv_path)