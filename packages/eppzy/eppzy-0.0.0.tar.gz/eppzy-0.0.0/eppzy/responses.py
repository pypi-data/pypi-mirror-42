import xml.etree.ElementTree as ET
from collections import namedtuple


class UnexpectedServerMessageType(Exception):
    pass


class MissingResult(Exception):
    pass


class ErrorResponse(Exception):
    pass


def _se(e, name):
    return e.find('{urn:ietf:params:xml:ns:epp-1.0}' + name)


def greeting(xml):
    e = ET.fromstring(xml)
    g = _se(e, 'greeting')
    if g:
        return {
            'svID': _se(g, 'svID').text
        }
    else:
        raise UnexpectedServerMessageType(xml.decode('utf8'))


Response = namedtuple('Response', ('code', 'msg', 'data'))


def response(xml):
    e = ET.fromstring(xml)
    resp = _se(e, 'response')
    if resp:
        result = _se(resp, 'result')
        if result:
            code = result.get('code')
            r = Response(
                result.get('code'),
                _se(result, 'msg').text.strip(),
                resp)
            if code in {'1000', '1500'}:
                return r
            else:
                raise ErrorResponse(r)
        else:
            raise MissingResult(xml.decode('utf8'))
    else:
        raise UnexpectedServerMessageType(xml.decode('utf8'))


def _dse(e, match):
    return e.find('{urn:ietf:params:xml:ns:domain-1.0}' + match)


def domain_response(xml):
    r = response(xml)
    i = _dse(_se(r.data, 'resData'), 'infData')
    return r._replace(data={
        'name': _dse(i, 'name').text,
        'roid': _dse(i, 'roid').text,
        'registrant': _dse(i, 'registrant').text
    })


def _cse(e, match):
    return e.find('{urn:ietf:params:xml:ns:contact-1.0}' + match)


def contact_info_response(xml):
    r = response(xml)
    i = _cse(_se(r.data, 'resData'), 'infData')
    pi = _cse(i, 'postalInfo')
    a = _cse(pi, 'addr')
    return r._replace(data={
        'id': _cse(i, 'id').text,
        'roid': _cse(i, 'roid').text,
        'name': _cse(pi, 'name').text,
        'org': _cse(pi, 'org').text,
        'street': _cse(a, 'street').text,
        'city': _cse(a, 'city').text,
        'state_or_province': _cse(a, 'sp').text,
        'country_code': _cse(a, 'cc').text,
        'voice': _cse(i, 'voice').text,
        'email': _cse(i, 'email').text
    })


def contact_create_response(xml):
    r = response(xml)
    crData = _cse(_se(r.data, 'resData'), 'creData')
    return r._replace(data={
        'id': _cse(crData, 'id').text,
        'date': _cse(crData, 'crDate').text
    })
