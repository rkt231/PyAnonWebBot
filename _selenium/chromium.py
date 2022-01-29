from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

def init_chromium():
    """
    Basic selenium chromium handler
    """
    _serv = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    _opts = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=_serv, options=_opts)
    return driver
    
