from pathlib import Path
from fast_antx.core import transfer
from utils import write_csv


def transfer_line_annotations(source_text, target_text):
    # patterns = [['page_break', "($)"], ['line_break', "(\n)"]]
    patterns = [['page_break', "($)"]]
    new_text = transfer(source_text, patterns, target_text)
    # text_with_page = new_text.replace("$", "\n\n")
    Path(f"./data//NyGB/new_v003.txt").write_text(new_text, encoding="utf-8")
    return new_text


def create_page_texts(text, vol):
    pages = text.split("$")
    for i, page in enumerate(pages, 1):
        Path(f"./data/NyGB/page_texts/{vol}_{i}.txt").write_text(page, encoding="utf-8")

def create_line_text_csv(page_text_dir):
    line_csv = []
    page_paths = sorted(page_text_dir.iterdir(), key=lambda x: int((x.stem).split("_")[-1]))
    for page_path in page_paths:
        page_name = page_path.stem
        page_text_lines = page_path.read_text(encoding='utf-8').splitlines()
        for line_num, line_text in enumerate(page_text_lines, 1):
            line_name = f"{page_name}_{line_num:02}"
            new_line = [line_name,line_text]
            line_csv.append(new_line)
    write_csv(line_csv, f"./data/csv/line_{vol}.csv")


if __name__ == "__main__":
    vol = "v003"
    source_text = Path(f"./data/NyGB/OCR_{vol}.txt").read_text(encoding="utf-8").replace("\n\n", "$")
    target_text = Path(f"./data/NyGB/clean_{vol}.txt").read_text(encoding="utf-8").replace("\n", "")
    new_text = transfer_line_annotations(source_text, target_text)
    create_page_texts(new_text, vol)
    create_line_text_csv(Path(f"./data/NyGB/page_texts/"))