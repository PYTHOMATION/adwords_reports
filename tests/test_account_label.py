from tests import fix_client, fix_account_label, fix_adwords_account_service, fix_adwords_account_label  # is used


def test_init(fix_account_label):
    assert fix_account_label.name == "unused"
    assert fix_account_label.id == 123


def test_from_adwords_account_label(fix_adwords_account_label):
    from adwords_reports.account_label import AccountLabel

    label = AccountLabel.from_ad_account_label(fix_adwords_account_label)
    assert label.name == "unused"
    assert label.id == 123


def test_repr(fix_account_label):
    assert str(fix_account_label) == "unused (123)"
