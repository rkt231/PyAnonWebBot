#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from stem import Signal
from stem.control import Controller
from _requests import builder

from pprint import pprint
import argparse
from utils import bs4_parser, help_format
import random
import time
import re
import logging
import ast

# Tor default local proxy
PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

def parse_args(description):
    """
    A basic parser to handle the bot options
    """
    parser = argparse.ArgumentParser(formatter_class=\
        help_format.BlankLinesHelpFormatter, description=description)
    parser.add_argument("-m", "--min", help="minimum time (seconds) to wait \
    between two queries. Default is 1 second.", type=int, default=1)
    parser.add_argument("-M", "--max", help="Maximum time (seconds) to wait \
    between two queries. Default is 2 seconds.", type=int, default=2)
    parser.add_argument("-t", "--timeout", help="Timeout (seconds) for \
    query. Default is 15 seconds.", type=int, default=15)
    parser.add_argument("-ws", "--with_session", help="Set it if you need a \
    session", action='store_true')
    parser.add_argument("-H", "--headers", help="Use a defined header. Default \
    is to use a random header.", type=str)
    subparsers = parser.add_subparsers(help='using an ip changer', dest='m_ip')
    tor = subparsers.add_parser('tor', help="use tor")
    tor.add_argument("-td", "--t_dynamic", action='store_true', help = \
        "Use a dynamic IP with a controller. \n\
        Check /etc/tor/torrc for: \n\
            - port 9051\n\
            - HashedControlPassword \n\
            - CookieAuthentication. \n\
        Else, use socket with port 9050 locally.\n")
    tor.add_argument("-tp", "--t_password", type=str, help = \
        "Password for tor controller (dynamic)")
    parser.add_argument("-u", "--url", help="URL to use", type=str, \
        required=True)
    parser.add_argument("-se_t", "--search_element_tag", help= \
        "Search element by tag", type=str)
    parser.add_argument("-se_n", "--search_element_name", help= \
        "Search element by name", type=str)
    parser.add_argument("-se_i", "--search_element_id", help= \
        "Search element by id", type=str)
    parser.add_argument("-se_c", "--search_element_class", help= \
        "Search elements by class", type=str)
    parser.add_argument("-sc", "--search_content", help= \
        "Text to search in HTML DOM.", type=str)
    parser.add_argument("-sl", "--search_limit", help= \
        "Maximum matches to display. Default is 100.", type=int, default=100)
    parser.add_argument("--norecursive", help= \
        "Display only immediate children.", action='store_true')
    parser.add_argument("-v", "--value", help="value to send (dict format)", \
        type=str)
    parser.add_argument("--auth_user", help="Basic auth (user)", \
        type=str)
    parser.add_argument("--auth_pwd", help="Basic auth (password)", \
        type=str)
    parser.add_argument("-mt", "--method", help="Method to use in form. \
        Should be GET or POST. Default is GET.", default="GET", type=str)
    args = parser.parse_args()
    return args

def torify(pwd):
    """
    Tor function to connect to the local proxy.
    It allows to get a dynamic tor IP.
    
    From:
    - https://www.tutorialguruji.com/python/making-a-request-using-requests-get-through-tor-proxies-but-the-code-is-not-responding/
    - https://sylvaindurand.org/use-tor-with-python/
    ... And do not forget to set a hashed pwd:
    - https://stackoverflow.com/questions/66128553/tor-stem-not-finding-the-cookie-control-authentication-file
    """
    with Controller.from_port(port = 9051) as c:
        c.authenticate(pwd)
        c.signal(Signal.NEWNYM)

def waiting(min, max):
    """
    A basic sleeping function with a random duration
    between min and max
    If there is no max value min will be used as max
    """
    wait = random.uniform(min, max)
    time.sleep(wait)

def main():
    proxies = {}
    payload = {}
    session = ""
    headers = {}
    auth = ""
    attrs = {}
    tag = None
    search_string = None
    recursive = True
    limit = 100

    description="This program allows you to send values using POST method \n\
        or retrieve and parse Web content from a webpage using GET method. \n\
        You can also send POST values and parse the return.\n\
        This code wraps python requests, requests_html, beautifulsoup, \n\
        random_user_agent, and some other useful libs.\n\
        Additional anonymization process may be used with tor.\n\
        If you want to use tor you will need a hashed password,\n\
        generated with \"tor --hash-password mypassword\"\
        Note that no author can be held liable of what you do with this \n\
        program.\n"

    args = parse_args(description)
    
    if args.url:
        if not re.search("^http(s)?://.*", args.url):
            raise Exception("Sorry, your URL is not valid")
    else:
        raise Exception("Sorry, you must supply an URL")
    url = args.url

    if args.method == "POST" or args.method == "post":
        method="POST"
    else:
        method="GET"
    
    waiting(args.min, args.max)
    
    if args.value:
        payload=args.value
    if args.m_ip:
        if args.t_dynamic and args.t_password:
            tor_pwd = args.t_password
            torify(tor_pwd)
        proxies=PROXIES
    
    if args.timeout:
        timeout = args.timeout
    else:
        timeout = 15
    if args.auth_user and args.auth_pwd:
        auth=(args.auth_user, args.auth_pwd)
    if args.headers:
        headers = args.headers
        try:
            headers = ast.literal_eval(headers)
        except (SyntaxError, ValueError) as e:
            raise e
    
    # setup the request
    rq = builder.rq(method, url, auth, payload, session, headers, proxies, \
        timeout)
    if not headers:
        # randomize user_agent
        rq.rand_uagent()

    if args.with_session:
        rq.get_session()
        rq.prep_and_send()
    else:
        rq.req()
    
    # parsing options and parse the Web Page
    content = rq.get_content()
    if args.search_element_tag:
        tag = args.search_element_tag
    if args.search_element_id:
        attrs["id"] = args.search_element_id
    if args.search_element_name:
        attrs["name"] = args.search_element_name
    if args.search_element_class:
        attrs["class"] = args.search_element_class
    if args.search_content:
        search_string = re.compile(".*%s.*"%args.search_content)
    if args.norecursive:
        recursive=False
    if args.search_limit:
        limit = args.search_limit
    results = bs4_parser.bs4_find_all(content, tag, attrs, recursive, search_string, limit)
    if results:
        for s in results:
            pprint(s)
    else:
        logging.warning("No Content Found !\nDumping content.\n")
        pprint(content)

if __name__ == '__main__':
    main()