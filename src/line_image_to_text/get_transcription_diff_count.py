from pathlib import Path
import csv
import jsonlines
import json



def get_diff_percentage(jsonl_dict, csv_dict, batch_id):
    total_count = len(csv_dict)
    diff_count = 0
    for key in csv_dict.keys():
        if csv_dict[key] != jsonl_dict[key]:
            diff_count += 1
            dict = {
                'id': key,
                '1st-reviewed': jsonl_dict[key],
                '2nd-reviewed': csv_dict[key],
                'batch_id': batch_id
            }
            with open(f'./data/monlam/diff.json', 'a') as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)
                f.write('\n')
    percentage = (diff_count / total_count) * 100
    print(f'Batch ID: {batch_id} - {diff_count}/{total_count} ({percentage}%)')



def get_csv_dict(csv_path):
    csv_dict = {}
    with open(csv_path, newline='') as csvfile:
        reader = list(csvfile)
        for row in reader:
            column = row.split(',')
            id = column[0]
            transcription = column[2].removesuffix('\r\n')
            csv_dict[id] = transcription
    return csv_dict


def get_jsonl_dict(csv_dict, batch_id):
    jsonl_dict = {}
    keys = list(csv_dict.keys())
    with jsonlines.open(f'./data/monlam/jsonl/{batch_id}.jsonl') as reader:
        for obj in reader:
            id = f"{obj['id']}.jpg"
            if id in keys:
                jsonl_dict[id] = obj['user_input']
    return jsonl_dict
    

def main():
    csv_paths = list(Path(f"./data/monlam/csv/").iterdir())
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        csv_dict = get_csv_dict(csv_path)
        jsonl_dict = get_jsonl_dict(csv_dict, batch_id)
        get_diff_percentage(jsonl_dict, csv_dict, batch_id)



if __name__ == "__main__":
    main()