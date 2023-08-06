from contextlib import contextmanager

from eppzy.commands import (
    login, logout, domain_info, contact_info, contact_create, contact_update)
from eppzy.connection import connection
from eppzy.responses import (
    response, greeting, domain_response, contact_info_response,
    contact_create_response)


class Requester:
    def __init__(self, c, greeting):
        self._c = c
        self.greeting = greeting

    def _request(self, cmd_xml, resp_parser=response):
        self._c.send(cmd_xml)
        return resp_parser(self._c.recv())

    def contact_info(self, *a, **k):
        return self._request(
            contact_info(*a, **k),
            contact_info_response)

    def contact_create(self, *a, **k):
        return self._request(
            contact_create(*a, **k),
            contact_create_response)

    def contact_update(self, *a, **k):
        return self._request(contact_update(*a, **k))

    def domain_info(self, domain_name, domain_password=''):
        return self._request(
            domain_info(domain_name, domain_pw=domain_password),
            domain_response)


@contextmanager
def session(host, port, clID, pw):
    with connection(host, port) as c:
        g = greeting(c.recv())
        s = Requester(c, g)
        try:
            s._request(login(clID, pw))
            yield s
        finally:
            s._request(logout())
