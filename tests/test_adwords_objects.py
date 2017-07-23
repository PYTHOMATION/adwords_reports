def test_account():
    from freedan import Account, AccountLabel
    import tests.init_native_adwords_objects as init_native_adwords_objects

    ad_account = init_native_adwords_objects.account()
    account = Account.from_ad_account(ad_account=ad_account)
    assert account.name == "Test1"
    assert account.id == "302-203-1203"
    assert account.currency == "CAD"
    assert account.time_zone == "America/Vancouver"
    assert not account.is_mcc
    assert not account.is_test
    assert account.labels == [AccountLabel(name="test1", label_id=0),
                              AccountLabel(name="this_is_a_label", label_id=1)]
