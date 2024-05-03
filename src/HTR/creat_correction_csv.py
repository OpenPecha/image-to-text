from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
import pyewts
from utils import add_row_to_csv


def parse_xml_and_create_jsonl(xml_paths, line_dir, source_dir):
    final_jsonl = []
    converter = pyewts.pyewts()
    for xml_path in xml_paths:
        xml_data = xml_path.read_text(encoding="utf-8")
        root = ET.fromstring(xml_data)
        namespace = {'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}
        page_element = root.find('.//page:Page', namespace)
        image_filename = page_element.get('imageFilename')
        source_image_path = source_dir / image_filename
        for textline in root.findall('.//page:TextLine', namespace):
            coords = textline.find('page:Coords', namespace).get('points')
            try:
                text = textline.find('page:TextEquiv/page:Unicode', namespace).text.strip()
                line_text = converter.toUnicode(text)
            except:
                line_text = ""
            line_name = crop_line(source_image_path, coords, line_dir)
            image_name = line_name
            final_jsonl.append({"id": image_name, "text": line_text})
    return final_jsonl


def crop_line(source_image_path, coords, output_path):
    filename = (source_image_path.name).split(".")[0]
    source_image = Image.open(source_image_path)
    coords_list = [int(point) for pair in coords.split() for point in pair.split(',')]
    min_x = min(coords_list[::2])
    min_y = min(coords_list[1::2])
    max_x = max(coords_list[::2])
    max_y = max(coords_list[1::2])
    line_image = source_image.crop((min_x, min_y, max_x, max_y))
    output_filename = Path(f"{output_path}/{filename}_{min_x}_{min_y}_{max_x}_{max_y}.jpg")
    try:
        line_image.save(output_filename, format="JPEG")
    except:
        rgb_line_image = line_image.convert("RGB")
        rgb_line_image.save(output_filename, format="JPEG")
    return output_filename.name


def create_csv_for_correction(correction_jsonl, csv_path, batch_id, group_id):
    headers = ["id","group_id","batch_id","state","inference_transcript","url","format"]
    add_row_to_csv(headers, csv_path)
    ids = []
    for obj in correction_jsonl:
        id = obj["id"]
        state = "transcribing"
        inference_transcript = obj["text"]
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/Marieke/Correction/{batch_id}/{id}"
        format = "line"
        row = [id, group_id, batch_id, state, inference_transcript, image_url, format]
        add_row_to_csv(row, csv_path)
        row = []