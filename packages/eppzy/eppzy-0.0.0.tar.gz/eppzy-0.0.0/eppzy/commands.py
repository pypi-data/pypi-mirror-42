import xml.etree.ElementTree as ET
from collections import defaultdict
from functools import wraps


def _epp():
    return ET.Element('epp', attrib={
        'xmlns': 'urn:ietf:params:xml:ns:epp-1.0',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd'})


def _cmd(name, *, xmlns=None):
    def w(f):
        if xmlns:
            se = lambda e, tag, *a, **k: ET.SubElement(
                e, xmlns + ':' + tag, *a, **k)
            ns_attrib = {'xmlns:' + xmlns: xmlns_map[xmlns]}
        else:
            se = ET.SubElement
            ns_attrib = {}

        @wraps(f)
        def wrapper(*a, **k):
            e = _epp()
            c = ET.SubElement(e, 'command')
            n = ET.SubElement(c, name)
            if xmlns:
                n = se(n, name, attrib=ns_attrib)
            f(n, se, *a, **k)
            return ET.tostring(e, encoding='UTF8')
        return wrapper
    return w


xmlns_map = {
    'domain': 'urn:ietf:params:xml:ns:domain-1.0',
    'contact': 'urn:ietf:params:xml:ns:contact-1.0',
    'host': 'urn:ietf:params:xml:ns:host-1.0',
}


@_cmd('login')
def login(l, se, clID, pw):
    se(l, 'clID').text = clID
    se(l, 'pw').text = pw
    opts = se(l, 'options')
    se(opts, 'version').text = '1.0'
    se(opts, 'lang').text = 'en'
    svcs = se(l, 'svcs')
    for objUri in xmlns_map.values():
        se(svcs, 'objURI').text = objUri


@_cmd('logout')
def logout(e, se):
    pass


@_cmd('info', xmlns='domain')
def domain_info(d, se, domain_name, domain_pw=''):
    se(d, 'name', attrib={'hosts': 'all'}).text = domain_name
    ai = se(d, 'authInfo')
    se(ai, 'pw').text = domain_pw


@_cmd('info', xmlns='contact')
def contact_info(c, se, contact_id, password):
    se(c, 'id').text = contact_id
    se(se(c, 'authInfo'), 'pw').text = password


@_cmd('create', xmlns='contact')
def contact_create(
        c, se, contact_id, name, org, street, city, state_or_province,
        postcode, country_code, voice, fax, email, password):
    se(c, 'id').text = contact_id
    p = se(c, 'postalInfo', attrib={'type': 'loc'})
    se(p, 'name').text = name
    se(p, 'org').text = org
    a = se(p, 'addr')
    se(a, 'street').text = street
    se(a, 'city').text = city
    se(a, 'sp').text = state_or_province
    se(a, 'pc').text = postcode
    se(a, 'cc').text = country_code
    se(c, 'voice').text = voice
    se(c, 'email').text = email
    se(c, 'fax').text = fax
    se(se(c, 'authInfo'), 'pw').text = password


def _get_ots(se, root_elem):
    built_nodes = defaultdict(dict)

    def _ots(parent_elem, val, name, *subnames):
        if val is not None:
            if subnames:
                kids = built_nodes[id(parent_elem)]
                if type(name) is tuple:
                    name, attrib = name
                else:
                    attrib = {}
                n = kids.get(name)
                if not n:
                    n = kids[name] = se(parent_elem, name, attrib=attrib)
                _ots(n, val, *subnames)
            else:
                se(parent_elem, name).text = val
    return lambda v, *ns: _ots(root_elem, v, *ns)


@_cmd('update', xmlns='contact')
def contact_update(
        c, se, contact_id, name=None, org=None, street=None, city=None,
        state_or_province=None, postcode=None, country_code=None, voice=None,
        fax=None, email=None, password=None):
    se(c, 'id').text = contact_id
    chg = se(c, 'chg')
    o = _get_ots(se, chg)
    pi = ('postalInfo', {'type': 'loc'})
    o(name, pi, 'name')
    o(org, pi, 'org')
    o(street, pi, 'addr', 'street')
    o(city, pi, 'addr', 'street')
    o(state_or_province, pi, 'addr', 'sp')
    o(postcode, pi, 'addr', 'pc')
    o(country_code, pi, 'addr', 'cc')
    o(voice, 'voice')
    o(fax, 'fax')
    o(email, 'email')
    o(password, 'authInfo', 'pw')
