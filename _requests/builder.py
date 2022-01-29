import logging
import requests
from requests_html import HTMLSession
from random_user_agent.user_agent import UserAgent

"""
This class is a wrapper around requests and requests_html objects
"""

class rq:
    method = 'GET'
    url = ""
    auth = None
    payload = {}
    session = True
    headers = {}
    proxies = {}
    timeout = 15
    Rq_obj = ""
    output = ""
    authtype = ""

    def __init__(self, method, url, auth, payload, session, headers, proxies, \
        timeout):
        self.method = method
        self.url = url
        self.auth = auth
        self.payload = payload
        self.session = session
        self.headers = headers
        self.proxies = proxies
        self.timeout = timeout
        self.Rq_obj = ""
        self.output = ""
        self.authtype = ""
    
    def authenticate(self, authtype):
        self.authtype = authtype
        # https://www.programcreek.com/python/example/53012/requests.auth.HTTPDigestAuth
        if authtype == "basic":
            self.auth = requests.auth.HTTPBasicAuth(self.auth[0], self.auth[1])
        elif authtype == "digest":
            self.auth = requests.auth.HTTPDigestAuth(self.auth[0], self.auth[1])
        else:
            logging.info("No authentication method given")

    def get_session(self):
        try:
            self.session = HTMLSession()
        except requests.exceptions.RequestException as e:
            print(e)
    
    def prep_and_send(self):
        self.build_Rq_obj()
        prepped = self.session.prepare_request(self.Rq_obj)
        self.output = self.session.send(prepped,
            proxies=self.proxies,
            timeout=self.timeout
        )

    def rand_uagent(self):
        """
        From https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
        """
        user_agent_rotator = UserAgent(limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        self.headers = {'User-Agent': user_agent}
    
    def req(self):
        self.output = requests.request(self.method, self.url, \
            headers=self.headers, data=self.payload, auth=self.auth, \
            proxies=self.proxies, timeout=self.timeout)

    def build_Rq_obj(self):
        """
        requests has a requests.Request object.
        It differs from requests.requests method.
        Moreover, there is no proxies or timeout arg.
        Those args need to be given to session.send() method.
        """
        self.Rq_obj = requests.Request(self.method, self.url, \
            headers=self.headers, data=self.payload, auth=self.auth)
    
    def get_content(self):
        return self.output.content
    
