from line_image_to_text.rearrange_input import load_json_data, process_work_folder


def test_process_work_folder():
    process_work_folder("./tests/test_data/work")
    data = load_json_data("./tests/test_data/work/rearranged_work.json")
    assert data[0]["rearranged_text"] == "ཁམས་སྒོམ་སྡེ་ནང་ཆེན་པའི་དགོན་ཁག་རྣམས་ཀྱི་"
    assert data[1]["rearranged_text"] == "བྱུང་བ་ཕྱོགས་བསྒྲིགས་རིན་ཆེན་སྒྲོམ་བརྒྱ་"
    assert (
        data[2]["rearranged_text"]
        == "ཝུའུ་ཧྲིང་ལོས།(ཁུལ་ཨུའི་རྒྱུན་ཨུ། རྫོང་ཨུ་ཧྲུའུ་ཅི)"
    )
    assert (
        data[3]["rearranged_text"]
        == "པད་མཆོག (རྫོང་དམངས་ཆེན་ཨུ་ཡོན་ལྷན་ཁང་གི་ཀྲུའུ་རིན）"
    )
    assert (
        data[4]["rearranged_text"]
        == "ཡོན་ཏན། (རྫོང་ཨུ་ཧྲུའུ་ཅི་གཞོན་པ། རྫོང་སྲིད་གཞུང་གི་རྫོང་གཙོ)"
    )
    assert (
        data[5]["rearranged_text"]
        == "ཀུན་དགའ་རྣམ་རྒྱལ། (རྫོང་ཨུ་རྒྱུན་ཨུ། སྒྲིག་ཨུ་ཧྲུའུ་ཅི)"
    )
    assert data[6]["rearranged_text"] == "ཨུ་ཡོན།"
    assert data[7]["rearranged_text"] == "no matching text found"
