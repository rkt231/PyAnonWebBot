from seleniumwire import webdriver as WD
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.proxy import Proxy, ProxyType
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager

from config import conf
from utils import rand_user_agent


def interceptor(request):
    """
    interceptor is a selenium-wire method to change
    headers dynamically
    """
    del request.headers["user-agent"] # Delete the header first
    request.headers["user-agent"] = rand_user_agent.rand_uagent()
    request.headers["sec-ch-ua"] = conf.sec_ch_ua

def ffx_profile(user_agent):
    """
    A basic function to init a Firefox Profile
    From: https://github.com/pushkarsharma23/Hacker-Tools/blob/main/ShadowCrawler.py
    """
    print("user-agent %s" % user_agent)
    # Creates an instance of the FirefoxProfile class
    profile = FirefoxProfile()
    # Disable CSS Rendering
    profile.set_preference('permissions.default.stylesheet', 2)
    # Disable notifications
    profile.set_preference('dom.webnotifications.enabled','false')
    # Setting timeouts
    profile.set_preference("http.response.timeout", 10)
    profile.set_preference("dom.max_script_run_time", 5)
    # Disable Geo sniff
    profile.set_preference("geo.enabled", False)
    # Disables the automatic loading of images
    profile.set_preference('permissions.default.image', 2)
    # Disables Flash player plugin
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # Overrides the default user agent with the given user agent
    profile.set_preference("general.useragent.override", user_agent)
    # Sets the private browsing mode to start automatically
    profile.set_preference("driver.privatebrowsing.autostart", True)
    # Updates the preferences for the profile
    profile.update_preferences()
    # Returns the created profile
    return profile

def init_firefox(proxy=False, headers=False):
    """
    A basic firefox/selenium handler
    Need to put geckodriver in ~/bin/
    """
    _wire_opts = False
    _serv = Service(GeckoDriverManager(path="~/bin/").install())
    _opts = Options()
    if conf.HEADLESS:
        _opts.add_argument('headless')
    if proxy:
        _wire_opts = {'proxy':conf.PROXIES}
        ##print("Using proxy %s" % conf.PROXIES)
        #firefox_profile.set_preference("network.proxy.type", 1)
        #firefox_profile.set_preference("network.proxy.socks", conf.TOR_PROX_HOST)
        #firefox_profile.set_preference("network.proxy.socks_port", conf.TOR_PORT)
        ##firefox_profile.set_preference("network.proxy.socks_remote_dns", False)
        #firefox_profile.update_preferences()
    if not headers:
        headers = rand_user_agent.rand_uagent()
        _UA = headers['User-Agent']
    else:
        _UA = headers
    _profile = ffx_profile(_UA)
    if not _wire_opts:
        driver = WD.Firefox(service=_serv, options=_opts, firefox_profile=_profile, \
                           executable_path=GeckoDriverManager().install(), \
                           service_args=['--verbose', '--log-path=/tmp/geckodriver.log'])
    else:
        driver = WD.Firefox(service=_serv, seleniumwire_options=_wire_opts, options=_opts, \
                           firefox_profile=_profile, \
                           executable_path=GeckoDriverManager().install(), \
                           service_args=['--verbose', '--log-path=/tmp/geckodriver.log'])
    #driver.request_interceptor = interceptor
    user_agent = driver.execute_script("return navigator.userAgent;")
    print("User agent: %s" % user_agent)
    return driver
