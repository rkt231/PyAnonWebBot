from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def init_chrome(proxy=False, headers=False):
    """
    Basic selenium chrome handler
    """
    _serv = Service(ChromeDriverManager().install())
    _opts = webdriver.ChromeOptions()
    if proxy:
        _opts.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(service=_serv, options=_opts)
    return driver
