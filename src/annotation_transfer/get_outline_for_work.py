from pathlib import Path
import requests
from rdflib import Graph, Namespace
from openpecha.buda import api as buda_api


BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")


def get_s3_img_list(img_group, scan_id):
    img_list =  buda_api.get_image_list_s3(scan_id, img_group)
    return img_list


def get_page_info(g, location_id):
    page_info = {}
    page_start_ids = g.objects(BDR[location_id], BDO["contentLocationPage"])
    for page_start_id in page_start_ids:
        start_page = get_id(page_start_id)
        page_info['start_page'] = start_page
    page_end_ids = g.objects(BDR[location_id], BDO["contentLocationEndPage"])
    for page_end_id in page_end_ids:
        end_page = get_id(page_end_id)
        page_info['end_page'] = end_page
    return page_info



def get_location_info(g, part_id, img_list):
    ttl = get_ttl(part_id[1:])
    g = parse_ttl(ttl)
    content_location_ids = g.objects(BDR[part_id], BDO["contentLocation"])
    for content_location_id in content_location_ids:
        location_id = get_id(content_location_id)
        location_info = get_page_info(g, location_id)
    return location_info


def get_parts_info(g, part_ids, volume_id, image_group_id, scan_id):
    location_infos = []
    img_list = get_s3_img_list(image_group_id, scan_id)
    for part_id in part_ids:
        if part_id.split("_")[1] == volume_id:
            location_info = get_location_info(g, part_id, img_list)
            location_infos.append(location_info)
    return location_infos
            


def get_id(uri):
    return str(uri).split("/")[-1]


def get_part_ids(g, work_id):
    part_ids = []
    parts = g.objects(BDR[work_id], BDO["hasPart"])
    for part in parts:
        part_id = get_id(part)
        part_ids.append(part_id)
    return part_ids

def get_ttl(id):
    id = F"M{id}"
    try:
        ttl = requests.get(f"https://ldspdi.bdrc.io/resource/{id}.ttl")
        return ttl
    except:
        print(' TTL not Found!!!')
        return None
    

def parse_ttl(ttl):
    try:
        g = Graph()
        g.parse(data=ttl.text, format="ttl")
    except:
        print('Error parsing TTL')
        g = None
    return g
   
    
def get_ttl(scan_id):
    work_id = F"M{scan_id}"
    try:
        ttl = requests.get(f"https://ldspdi.bdrc.io/resource/{work_id}.ttl")
        return ttl
    except:
        print(' TTL not Found!!!')
        return None


def get_outline_for_work(scan_id):
    image_group_id = "I1KG81275"
    volume_id = 3
    info = {}
    ttl = get_ttl(scan_id)
    g = parse_ttl(ttl)
    if g:
        part_ids = get_part_ids(g, f"M{scan_id}")
        info = get_parts_info(g, part_ids, f"{volume_id:04}", image_group_id, scan_id)
    return info


def main():
    scan_id = "W2PD17382"
    outline = get_outline_for_work(scan_id)

if __name__ == "__main__":
    main()