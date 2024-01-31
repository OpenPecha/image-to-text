from pathlib import Path
from fast_antx.core import transfer


def transfer_line_annotations(source_text, target_text):
    patterns = ['line_break', "(\n)"]
    new_text = transfer(source_text, patterns, target_text)
    Path(f"./data//NyGB/new_text.txt").write_text(new_text, encoding="utf-8")

if __name__ == "__main__":
    source_text = Path("./data/NyGB/OCR_v003.txt").read_text(encoding="utf-8")
    target_text = Path("./data/NyGB/cleaned_v003.txt").read_text(encoding="utf-8")
    transfer_line_annotations(source_text, target_text)