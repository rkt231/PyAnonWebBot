from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def init_firefox(proxy=False, headers=False):
    """
    A basic firefox/selenium handler
    Need to put geckodriver in ~/bin/
    """
    _serv = Service(GeckoDriverManager(path="~/bin/").install())
    _opts = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile()
    if proxy:
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", '127.0.0.1')
        profile.set_preference("network.proxy.socks_port", 9050)
        #profile.set_preference("network.proxy.socks_remote_dns", False)
        profile.update_preferences()
    if headers:
        profile.set_preference("general.useragent.override", headers)
        profile.update_preferences()
    driver = webdriver.Firefox(service=_serv, options=_opts, \
        firefox_profile=profile, executable_path = \
        GeckoDriverManager().install())
    return driver


