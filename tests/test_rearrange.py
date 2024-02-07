from line_image_to_text.rearrange_input import load_json_data, process_work_folder


def test_process_work_folder():
    process_work_folder("./tests/test_data/work")
    data = load_json_data("./tests/test_data/work/rearranged_work.json")
    for item in data:
        if item["image_name"] == "I01JW1270005_0.jpg":
            assert (
                item["rearranged_text"] == "ཁམས་སྒོམ་སྡེ་ནང་ཆེན་པའི་དགོན་ཁག་རྣམས་ཀྱི་"
            )
        if item["image_name"] == "I01JW1270005_1.jpg":
            assert item["rearranged_text"] == "བྱུང་བ་ཕྱོགས་བསྒྲིགས་རིན་ཆེན་སྒྲོམ་བརྒྱ་"
        if item["image_name"] == "I01JW1270006_1.jpg":
            assert (
                item["rearranged_text"]
                == "ཝུའུ་ཧྲིང་ལོས།(ཁུལ་ཨུའི་རྒྱུན་ཨུ། རྫོང་ཨུ་ཧྲུའུ་ཅི)"
            )
        if item["image_name"] == "I01JW1270006_2.jpg":
            assert (
                item["rearranged_text"]
                == "པད་མཆོག (རྫོང་དམངས་ཆེན་ཨུ་ཡོན་ལྷན་ཁང་གི་ཀྲུའུ་རིན）"
            )
        if item["image_name"] == "I01JW1270006_3.jpg":
            assert (
                item["rearranged_text"]
                == "ཡོན་ཏན། (རྫོང་ཨུ་ཧྲུའུ་ཅི་གཞོན་པ། རྫོང་སྲིད་གཞུང་གི་རྫོང་གཙོ)"
            )
        if item["image_name"] == "I01JW1270006_4.jpg":
            assert (
                item["rearranged_text"]
                == "ཀུན་དགའ་རྣམ་རྒྱལ། (རྫོང་ཨུ་རྒྱུན་ཨུ། སྒྲིག་ཨུ་ཧྲུའུ་ཅི)"
            )
        if item["image_name"] == "I01JW1270006_12.jpg":
            assert item["rearranged_text"] == "ཨུ་ཡོན།"
        if item["image_name"] == "I1KG90740015_0.jpg":
            assert item["rearranged_text"] == "no matching text found"
