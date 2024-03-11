from botok import WordTokenizer

from line_image_to_text.filter_work import (
    is_non_bo_word_exist,
    is_non_word_exist,
    is_tibetan_num_exist,
    is_valid_text_len,
    is_width_greater_than_height,
    load_json_data,
)

wt = WordTokenizer()
text1 = "༢༡༦༩དག་པ་ས་གསུམ་དུ་གནས་པ་དང་།"
text3 = "བཀྲས་"
text4 = "བོདཡིག་སྤྱ"
text5 = "བོད་ཡིག་སྤྱ is good"


def test_tibetan_num_exist():
    token = wt.tokenize(text1)
    assert is_tibetan_num_exist(token) is True


def test_is_width_greater_than_height():
    data = load_json_data("./tests/test_data/test_image/test_image.json")
    crop_coords1 = data[0]["pil_crop_rectangle_coords"]
    crop_coords2 = data[1]["pil_crop_rectangle_coords"]
    assert is_width_greater_than_height(crop_coords1) is True
    assert is_width_greater_than_height(crop_coords2) is False


def test_is_valid_text_len():
    token = wt.tokenize(text3)
    assert is_valid_text_len(token) is False


def test_non_word_exist():
    token = wt.tokenize(text4)
    assert is_non_word_exist(token) is True


def test_non_bo_word_exist():
    token = wt.tokenize(text5)
    assert is_non_bo_word_exist(token) is True
