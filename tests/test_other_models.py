#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_standard_upload_chunking():
    from freedan import StandardUploader

    vals = list(range(100))
    chunks = list(StandardUploader.chunks(vals, 15))
    assert len(chunks) == 7
    assert [len(chunk) for chunk in chunks] == [15 if i <= 5 else 10 for i in range(7)]


def test_close_variant():
    from freedan import TextHandler
    cv = TextHandler("hott'-hü")
    assert cv.decoded == "hott'-hu"
    assert cv.without_punctuation == "hott hü"
    assert cv.standardized == "hott hu"
    assert cv.variations == {"hott'-hü", "hott'-hu", "hott hü", "hott hu"}

    assert TextHandler.remove_forbidden_adwords_chars({"asd(s)ad", "{asd(s)ad"}) == {"asdsad"}
    assert TextHandler.remove_double_white_space("    qweq asd  qqr") == "qweq asd qqr"
    assert TextHandler.remove_punctuation("madrid a gasteiz / vitoria") == "madrid a gasteiz vitoria"
    assert TextHandler.remove_forbidden_adwords_chars("madrid a gasteiz / vitoria") == "madrid a gasteiz / vitoria"


def test_drive_a1_notation():
    from freedan import Drive
    drive = Drive()

    test_values = [[0, 4], [1, 4], [2, "as"]]
    a1 = drive.a1_notation(test_values, "test")
    assert a1 == "test!A1:B"
