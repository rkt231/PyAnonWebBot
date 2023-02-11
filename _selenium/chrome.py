#from selenium import webdriver as WD
from seleniumwire import webdriver as WD
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config import conf
from utils import rand_user_agent


def interceptor(request):
    del request.headers["user-agent"] # Delete the header first
    request.headers["user-agent"] = rand_user_agent.rand_uagent()
    request.headers["sec-ch-ua"] = conf.sec_ch_ua
    return request

def init_chrome(proxy=False, headers=False):
    """
    Basic selenium chrome handler
    """
    _wire_opts = False
    _serv = ChromeService(executable_path=ChromeDriverManager().install())
    _opts = WD.ChromeOptions()
    if conf.HEADLESS:
        _opts.add_argument('headless')
    #_opts.add_argument('--disable-infobars')
    #_opts.add_argument('--disable-dev-shm-usage')
    #_opts.add_argument('--no-sandbox')
    if proxy:
        _wire_opts = {'proxy':conf.PROXIES}
        #PROXY = conf.PROXIES['https']
        #_opts.add_argument('--proxy-server=%s' % PROXY)
    if not headers:
        headers = rand_user_agent.rand_uagent()
    _opts.add_argument("user-agent=%s" % headers)
    if not _wire_opts:
        driver = WD.Chrome(service=_serv, options=_opts, \
                           service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    else:
        driver = WD.Chrome(service=_serv, seleniumwire_options=_wire_opts, options=_opts, \
                           service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    #driver.request_interceptor = interceptor
    user_agent = driver.execute_script("return navigator.userAgent;")
    print("User agent: %s" % user_agent)
    return driver
