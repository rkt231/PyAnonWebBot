from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from config import conf

def init_chromium(proxy=False, headers=False):
    """
    Basic selenium chromium handler
    """
    _serv = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    _opts = webdriver.ChromeOptions()

    if proxy:
        PROXY = conf.PROXIES['https']
        _opts.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(service=_serv, options=_opts)
    return driver
    
