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

from config import conf

from _selenium import selenium_builder

def parse_args(description):
    """
    A basic parser to handle the bot options
    """
    parser = argparse.ArgumentParser(formatter_class=\
        help_format.BlankLinesHelpFormatter, description=description)

    parser.add_argument('--version', action='version', \
    version='%(prog)s 0.1.1')
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
    parser.add_argument("-sff", "--stop_first_found", help= \
        "Stop search at first item found and dump inner content.", \
        action='store_true')
    parser.add_argument("-sl", "--search_limit", help= \
        "Maximum matches to display. Default is 100.", type=int, default=100)
    parser.add_argument("--norecursive", help= \
        "Display only immediate children.", action='store_true')
    parser.add_argument("-utf8d", "--utf8_decode", help= \
        "Try to decode utf8 content.", action='store_true')
    parser.add_argument("-v", "--value", help="value to send (dict format)", \
        type=str)
    parser.add_argument("--auth_user", help="authenticate with username", \
        type=str)
    parser.add_argument("--auth_pwd", help="authenticate with password", \
        type=str)
    parser.add_argument("--authtype", help="Authentication type: \
        [digest|basic] (needs --auth_user and --auth_pwd)", type=str, \
        choices=['basic','digest'], default='basic')
    parser.add_argument("-mt", "--method", help="Method to use in form. \
        Should be GET or POST. Default is GET.", default="GET", type=str)
    parser.add_argument("-ts", "--tor_static", action='store_true', help = \
        "Use a local tor proxy")
    parser.add_argument("-td", "--tor_dynamic", action='store_true', help = \
        "Use a dynamic IP with Tor and a controller. \n\
        Check /etc/tor/torrc for: \n\
            - port 9051\n\
            - HashedControlPassword \n\
            - CookieAuthentication. \n\
        Else, use socket with port 9050 locally.\n")
    parser.add_argument("-tp", "--tor_password", type=str, help = \
        "Password for the Tor controller (dynamic; needs '-td')")
    parser.add_argument("-SBE", "--selenium_browser_engine", type=str, choices = \
        ["chrome", "chromium", "firefox", "edge", "opera", "IE"], \
        help="Use the corresponding browser engine (it needs to be installed)")
    parser.add_argument("-SA", "--selenium_actions", type=str, help = "A valid list \
        of selenium actions (eg: '[[{\"type\": \"find_element_by_name\", \
        \"value\": \"q\"}, {\"type\": \"send_keys\", \"value\": \"test\"}]]' \
        will result in .find_element_by_name('q').send_keys('test'))")
    parser.add_argument("-SAF", "--selenium_actions_file", type = \
        argparse.FileType('r'), help = "A valid list of selenium actions in a \
        json file (you could take a look at _selenium/examples/*.json)")

    args = parser.parse_args()
    return args

def requests_new(method, url, auth, payload, session, headers, proxies, timeout, \
    authtype, with_session):
    # setup the request
    rq = builder.rq(method, url, auth, payload, session, headers, proxies, \
        timeout)
    if not headers:
        # randomize user_agent
        rq.rand_uagent()
    if auth and authtype:
        rq.authenticate(authtype)

    if with_session:
        rq.get_session()
        rq.prep_and_send()
    else:
        rq.req()
    # parsing options and parse the Web Page
    content = rq.get_content()
    return content

def parse_and_display(tag=None, attrs={}, search_content=None, \
    norecursive=False, limit=100, stop_first_found=False, utf8_decode=False, \
    content=""):
    search_string=""
    recursive=True
    if search_content:
        search_string = re.compile(".*%s.*"%search_content)
    if norecursive:
        recursive=False
    # soup.find() and soup.find_all() may be mixed.
    # maybe that kind of mix will be possible in a future version
    # to stop at first item, we could either use limit=1 or soup.find()
    if stop_first_found:
        results = bs4_parser.bs4_find(content, tag, attrs, recursive, search_string)
    else:
        results = bs4_parser.bs4_find_all(content, tag, attrs, recursive, search_string, limit)
    if results:
        for s in results:
            try_utf8(s, utf8_decode)
    else:
        logging.warning("No Content Found ! Dumping content.\n")
        try_utf8(content, utf8_decode)

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

def try_utf8(content, utf8):
    if utf8:
        try:
            pprint(content.decode("utf-8"))
        except Exception as err:
            logging.warning("Following exception happens while trying to \
decode content (utf-8): %s. \nDumping results:\n" % err)
            pprint(content)
    else:
        pprint(content)

def waiting(min, max):
    """
    A basic sleeping function with a random duration
    between min and max
    If there is no max value min will be used as max
    """
    wait = random.uniform(min, max)
    time.sleep(wait)

def main():
    """
    Parse arguments and call the right methods
    """
    content = ""
    proxies = {}
    payload = {}
    session = ""
    headers = {}
    auth = None
    attrs = {}

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
    if args.tor_dynamic or args.tor_static:
        if args.tor_dynamic and args.tor_password:
            tor_pwd = args.tor_password
            torify(tor_pwd)
        proxies=conf.PROXIES
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
        except (SyntaxError, ValueError) as err:
            raise err
    if args.selenium_browser_engine:
        rq = selenium_builder.Selenium_rq(args.selenium_browser_engine, \
            url, proxies, headers)
        rq.open_url()
        if args.selenium_actions:
            rq.selenium_actions(args.selenium_actions)
        elif args.selenium_actions_file:
            rq.selenium_actions(args.selenium_actions_file)
        else:
            pprint("No action given for Selenium")
    else:
        content = requests_new(method, url, auth, payload, session, headers, \
            proxies, timeout, args.authtype, args.with_session)

    if args.search_element_id:
        attrs["id"] = args.search_element_id
    if args.search_element_name:
        attrs["name"] = args.search_element_name
    if args.search_element_class:
        attrs["class"] = args.search_element_class
    if content:
        parse_and_display(args.search_element_tag, attrs, \
            args.search_content, args.norecursive, args.search_limit, \
            args.stop_first_found, args.utf8_decode, content)


if __name__ == '__main__':
    main()
