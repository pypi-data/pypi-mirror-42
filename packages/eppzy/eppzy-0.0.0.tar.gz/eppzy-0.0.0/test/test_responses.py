from os.path import dirname, join

from eppzy.responses import contact_info_response


def data_file_contents(relpath):
    p = join(dirname(__file__), relpath)
    with open(p) as f:
        return f.read()


def test_contact_info_response():
    r = contact_info_response(data_file_contents(
        'rfc5733/contact_info_example.xml'))
    assert r.data['name'] == 'John Doe'
