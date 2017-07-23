#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_close_variant():
    from freedan import TextHandler

    # general
    cv = TextHandler("hott'-hü")
    assert cv.decoded == "hott'-hu"
    assert cv.without_punctuation == "hott hü"
    assert cv.standardized == "hott hu"
    assert cv.variations == {"hott'-hü", "hott'-hu", "hott hü", "hott hu"}

    # some methods
    assert TextHandler.remove_forbidden_adwords_chars({"asd(s)ad", "{asd(s)ad"}) == {"asdsad"}
    assert TextHandler.remove_double_white_space("    qweq asd  qqr") == "qweq asd qqr"
    assert TextHandler.remove_punctuation("madrid a gasteiz / vitoria") == "madrid a gasteiz vitoria"
    assert TextHandler.remove_forbidden_adwords_chars("madrid a gasteiz / vitoria") == "madrid a gasteiz / vitoria"

    # dash brain fuck
    assert TextHandler.replace_dashes("a–a—a−a-a") == "a a a a a"
