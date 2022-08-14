#from selenium import webdriver
from seleniumwire import webdriver as WD
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from config import conf
from utils import rand_user_agent


def interceptor(request): 
	del request.headers["user-agent"] # Delete the header first
	request.headers["user-agent"] = rand_user_agent.rand_uagent()
	request.headers["sec-ch-ua"] = conf.sec_ch_ua

def init_chrome(proxy=False, headers=False):
    """
    Basic selenium chrome handler
    """
    _serv = Service(ChromeDriverManager().install())
    _opts = WD.ChromeOptions()
    if proxy:
        _opts = {'proxy':conf.PROXIES}
        #PROXY = conf.PROXIES['https']
        #_opts.add_argument('--proxy-server=%s' % PROXY)
    #if headers:
        #headers = rand_user_agent.rand_uagent()
        #_opts.add_argument("user-agent=%s" % headers)
    
    driver = WD.Chrome(service=_serv, seleniumwire_options=_opts)
    driver.request_interceptor = interceptor
    return driver
