def test_micro_to_reg():
    from adwords_reports.micro_amounts import micro_to_reg

    assert micro_to_reg(23000000) == 23.0


def test_micro_to_reg_rounding():
    from adwords_reports.micro_amounts import micro_to_reg

    assert micro_to_reg(1111111) == 1.11


def test_micro_to_reg_too_small():
    from adwords_reports.micro_amounts import micro_to_reg

    assert micro_to_reg(100) == 0.0


def test_reg_to_micro():
    from adwords_reports.micro_amounts import reg_to_micro

    assert reg_to_micro(1.11) == 1110000


def test_reg_to_micro_rounding():
    from adwords_reports.micro_amounts import reg_to_micro

    assert reg_to_micro(1.1111) == 1110000


def test_reg_to_micro_too_small():
    from adwords_reports.micro_amounts import reg_to_micro

    assert reg_to_micro(0.003) == 0


def test_reg_and_micro_reg():
    from adwords_reports.micro_amounts import reg_and_micro

    assert reg_and_micro(1.11) == (1.11, 1110000)


def test_reg_and_micro_micro():
    from adwords_reports.micro_amounts import reg_and_micro

    assert reg_and_micro(100000) == (0.10, 100000)
