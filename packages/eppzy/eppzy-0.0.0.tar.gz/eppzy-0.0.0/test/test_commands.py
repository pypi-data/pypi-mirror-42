from eppzy.commands import contact_info


def test_contact_info():
    assert b'passable' in contact_info('conid', 'passable')
