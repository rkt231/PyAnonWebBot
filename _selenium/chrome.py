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
        PROXY = "socks5://127.0.0.1:9050"
        _opts.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(service=_serv, options=_opts)
    return driver