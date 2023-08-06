"""
Top level module used to create an amp object, which represents a project.
"""

import http.client

from si import session

class Amp(object):
    """
    The Amp class, which is used to create an object representing a project.
    """

    def __init__(self, key, domains, **options):
        if not key:
            raise Exception('key value passed into si.Amp.Amp constructor should not be empty')
        if not domains:
            raise Exception('domains value passed into si.Amp.Amp constructor should not be empty')

        # Set all the properties to initial values.
        self._project_key = key
        self._amp_agents = domains
        self._api_path = "/api/core/v2"
        self._user_id = options.get("user_id", None)
        self._builtin_events = options.get("builtin_events", None)
        self._timeout = options.get("timeout", 10.0) # 10 second timeout
        self._verbose = options.get("verbose", False)
        self._use_token = options.get("use_token", True)
        self._session_lifetime = options.get("session_lifetime", 1800)
        self.conns = []

        for amp_agent in self._amp_agents:
            amp_agent_components = amp_agent.split('://')
            first_component = amp_agent_components[0]
            if first_component.lower() == 'https':
                use_https = True
            else:
                use_https = False
            last_component = amp_agent_components[-1]
            host_info = last_component.rsplit(':', 1)
            if len(host_info) == 1:
                host, port = host_info[0], 8100
            else:
                host, port = tuple(host_info)
            if not use_https:
                conn = http.client.HTTPConnection(host, port=int(port), timeout=self._timeout)
            else:
                conn = http.client.HTTPSConnection(host, port=int(port), timeout=self._timeout)
            conn.connect()
            url = '/test/update_from_spa/' + self.key + "?session_life_time=%s" % self._session_lifetime
            conn.request('GET', url)
            response = conn.getresponse()
            if response.getcode() != 200:
                raise Exception('bad response code %s: needs to be 200' % response.getcode())
            text = response.read()
            text = text.decode('utf-8')
            if text != 'Key is known':
                raise Exception('got response text %s. Needs to be "Key is known"' % text)
            self.conns.append(conn)

    def __str__(self):
        return "<Amp project_key:%s>" % self._project_key

    # Start of Amp properties.
    #   api_path
    #   key
    #   domain
    #   user_id
    #   builtin_events
    #   timeout
    #   verbose

    @property
    def api_path(self):
        return self._api_path

    @api_path.setter
    def api_path(self, val):
        """
        Set api_path. Should be a string like "/api/core/v1"
        """
        self._api_path = val

    @property
    def key(self):
        return self._project_key

    @key.setter
    def key(self, val):
        """
        Set key, i.e. the project key.
        """
        self._project_key = val

    @property
    def domains(self):
        return self._amp_agents

    @domains.setter
    def domains(self, val):
        """
        Set domains, i.e. location of servers e.g an array of strings like ["server-0:8100","server-1:8100"]
        """
        self._amp_agents = val

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, val):
        self._user_id = val

    @property
    def builtin_events(self):
        return self._builtin_events

    @builtin_events.setter
    def builtin_events(self, val):
        self._builtin_events = val

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, val):
        """
        Set timeout. Should be in seconds in floating point representation. Default value of 0.2 is 200 milliseconds
        """
        self._timeout = val

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        """
        Set verbose. Should be true or false. Default value is false.
        """
        self._verbose = val

    @property
    def use_token(self):
        return self._use_token

    @use_token.setter
    def use_token(self, val):
        """
        Set use_token. Should be true (use amp tokens) or false (aka "custom"). Default value is true.
        """
        self._use_token = val

    # End of Amp properties.

    def session(self, **options):
        """
        Create a session object for the project represented by the amp object
        """
        return session.Session(amp=self, **options)