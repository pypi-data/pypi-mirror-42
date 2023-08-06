import requests
import atexit
# suppress warnings from verify=False
from requests.packages.urllib3.exceptions import SecurityWarning
requests.packages.urllib3.disable_warnings(SecurityWarning)
from requests.packages.urllib3.util import Retry
from actagm.adapters import AGMAdapter
from actagm.auth import AgmAuth


DEFAULT_SCHEME = "https://"
# number of times to retry 500 status codes
RETRY_500 = 5


def _prep_session(base, adapter):
    """

    :param base: The base address to mount the adapter to (base = scheme + host + '/actifio')
    :param adapter: HTTPAdapter to mount
    :return: Session wth mounted addapter
    """
    s = requests.Session()
    s.mount(base, adapter)
    return s


def _auth_session(base, session, user, password):
    url = base + '/session'
    r = session.post(url, auth=(user, password), verify=False)
    r.raise_for_status()
    sid = r.json()['id']
    session.auth = AgmAuth(sid)


def setup_session(base, user, password, **adapter_kwargs):
    if not adapter_kwargs:
        adapter_kwargs = {'max_retries': Retry(total=RETRY_500, status_forcelist=[500])}
    adapter = AGMAdapter(**adapter_kwargs)

    session = _prep_session(base, adapter)
    _auth_session(base, session, user, password)
    return session


class AgmHelper(object):
    """
    Helper to aid with programmatic AGM connections.

    Example usage:

    | >>> ah = AgmHelper(<dns name or ip address>, <user>, <password>)
    | >>> ah.login()
    | >>> r = ah.get('/cluster')
    | >>> print(r.json())
    """

    def __init__(self, host, user, password, scheme=DEFAULT_SCHEME):
        """
        :param host: dns name or ip address
        :param user: username for AGM BASIC authentication
        :param password: password for AGM BASIC authentication
        :param scheme: scheme to use with host
        """
        self.host = host
        self.user = user
        self.password = password
        self.scheme = scheme
        self.base = self.scheme + self.host + '/actifio'

        self._setup_session()

        # defined in login
        self.sid = None
        self.auth = None

    def _setup_session(self):
        self.s = requests.Session()
        self.a = AGMAdapter(max_retries=Retry(total=RETRY_500, status_forcelist=[500]))
        self.s.mount(self.base, self.a)

    def login(self):
        url = self.base + '/session'
        r = self.s.post(url, auth=(self.user, self.password), verify=False)
        r.raise_for_status()
        self.sid = r.json()['id']
        self._setup_auth(self.sid)
        atexit.register(self.logout, sid=self.sid)

    def _setup_auth(self, sid):
        if not self.auth:
            self.auth = AgmAuth(sid)
            self.s.auth = self.auth
        else:
            self.auth.sid = sid

    def logout(self, sid=None):
        sid = sid if sid is not None else self.sid
        if sid:
            url = self.base + '/session/' + sid
            r = self.s.delete(url)
            sid = None
            try:
                r.raise_for_status()
            except requests.HTTPError:
                # session already ended
                pass

    # Write session-like methods
    def request(self, method, endpoint, *args, **kwargs):
        return self.s.request(method, self.base + endpoint, *args, **kwargs)

    def get(self, endpoint, *args, **kwargs):
        return self.request('get', endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.request('post', endpoint, *args, **kwargs)

    def delete(self, endpoint, *args, **kwargs):
        return self.request('delete', endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        return self.request('put', endpoint, *args, **kwargs)

    def options(self, endpoint, *args, **kwargs):
        return self.request('options', endpoint, *args, **kwargs)

    def head(self, endpoint, *args, **kwargs):
        return self.request('head', endpoint, *args, **kwargs)
