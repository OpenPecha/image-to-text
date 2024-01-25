from pathlib import Path
import subprocess


def get_image_names_from_cleaned_text(batch_name):
    cleaned_data_path = Path(f"./data/lhasa_kangyur/{batch_name}/cleaned")
    cleaned_text_files = []
    for file in cleaned_data_path.iterdir():
        if file.is_file():
            cleaned_text_files.append(file.stem)
    return cleaned_text_files

def remove_text_that_are_not_cleaned(cleaned_text_files, batch_name):
    inference_path = Path(f"./data/lhasa_kangyur/{batch_name}/inference/")
    for file in inference_path.iterdir():
        if file.is_file():
            filename = file.stem.split("jpg")[0][:-1] + file.stem.split("jpg")[-1]
            if filename not in cleaned_text_files:
                file.unlink()

def remove_images_that_are_not_cleaned(cleaned_text_files, batch_name):
    images_path = Path(f"./data/lhasa_kangyur/{batch_name}/images/")
    for file in images_path.iterdir():
        if file.is_file():
            if file.stem not in cleaned_text_files:
                file.unlink()

def update_text_file_name(batch_name):
    output_path = Path(f"./data/lhasa_kangyur/{batch_name}/transcription")
    output_path.mkdir(parents=True, exist_ok=True)
    inference_path = Path(f"./data/lhasa_kangyur/{batch_name}/inference")
    for file in inference_path.iterdir():
        if file.is_file():
            filename = file.stem.split("jpg")[0][:-1] + file.stem.split("jpg")[-1]
            new_filename = filename + ".txt"
            if Path(output_path / new_filename).exists():
                print("file exists")
            else:
                subprocess.run(["cp", str(file), str(output_path / new_filename)])



if __name__ == "__main__":
    for file_path in Path("./data/lhasa_kangyur").iterdir():
        batch_name  = file_path.stem
        update_text_file_name(batch_name)
    #     cleaned_text_files = get_image_names_from_cleaned_text(batch_name)
    #     remove_text_that_are_not_cleaned(cleaned_text_files, batch_name)
    #     remove_images_that_are_not_cleaned(cleaned_text_files, batch_name)