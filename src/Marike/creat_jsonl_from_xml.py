from pathlib import Path
from config import PAGE_CROPPING_BUCKET, page_cropping_s3_client
import xml.etree.ElementTree as ET
from PIL import Image
import jsonlines
import pyewts

bucket_name = PAGE_CROPPING_BUCKET
s3 = page_cropping_s3_client

def write_jsonl(final_jsonl, jsonl_path):
    with jsonlines.open(jsonl_path, mode="w") as writer:
        writer.write_all(final_jsonl)


def download_xml(obj_key, output_path):
    s3.download_file(bucket_name, obj_key, output_path)


def parse_xml_and_create_jsonl(xml_paths, output_path):
    final_jsonl = []
    converter = pyewts.pyewts()
    for xml_path in xml_paths:
        xml_data = xml_path.read_text(encoding="utf-8")
        root = ET.fromstring(xml_data)
        namespace = {'page': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}
        page_element = root.find('.//page:Page', namespace)
        image_filename = page_element.get('imageFilename')
        source_image_path = f"./data/image_to_text/images/{image_filename}"
        for textline in root.findall('.//page:TextLine', namespace):
            coords = textline.find('page:Coords', namespace).get('points')
            text = textline.find('page:TextEquiv/page:Unicode', namespace).text.strip()
            line_name = crop_line(source_image_path, coords, output_path)
            line_text = converter.toUnicode(text)
            image_name = line_name
            s3_key = f"Corr1-20230809/lines/{image_name}"
            final_jsonl.append({"id": image_name, "image_url": s3_key, "text": line_text})
    return final_jsonl


def crop_line(source_image_path, coords, output_path):
    filename = (source_image_path.split("/")[-1]).split(".")[0]
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


def create_jsonl(list_path):
    final_jsonl = []
    obj_keys = Path(list_path).read_text().split("\n")
    for obj_key in obj_keys:
        if obj_key.split("/")[1] == "Manual1-20230809":
            image_id = obj_key.split("/")[-1]
            final_jsonl.append({"id": image_id, "image_url": obj_key, "text": "Text Here"})
    write_jsonl(final_jsonl, "./data/image_to_text/Manual1-20230809.jsonl")
            

if __name__ == "__main__":
    create_jsonl(f"data/image_to_text/image_to_text_list.txt")
    # output_path = Path("./data/image_to_text/lines/")
    # xml_paths = list(Path(f"./data/image_to_text/xml/").iterdir())
    # jsonl = parse_xml_and_create_jsonl(xml_paths, output_path)
    # write_jsonl(jsonl, "./data/image_to_text/lines.jsonl")