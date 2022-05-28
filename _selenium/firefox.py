from selenium import webdriver
#from seleniumwire import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import conf


def init_firefox(proxy=False, headers=False):
    """
    A basic firefox/selenium handler
    Need to put geckodriver in ~/bin/
    """
    _serv = Service(GeckoDriverManager(path="~/bin/").install())
    _opts = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile()
    if proxy:
        print("Using proxy %s" % conf.PROXIES)
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", conf.TOR_PROX_HOST)
        profile.set_preference("network.proxy.socks_port", conf.TOR_PORT)        
        #profile.set_preference("network.proxy.socks_remote_dns", False)
        profile.update_preferences()
    if headers:
        profile.set_preference("general.useragent.override", headers)
        profile.update_preferences()
    driver = webdriver.Firefox(service=_serv, options=_opts, \
        firefox_profile=profile, executable_path = \
        GeckoDriverManager().install())
    return driver


