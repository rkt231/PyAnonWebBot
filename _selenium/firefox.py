from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


def init_firefox():
    """
    A basic firefox/selenium handler
    Need to put geckodriver in ~/bin/
    """
    _serv = Service(GeckoDriverManager(path="~/bin/").install())
    _opts = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=_serv, options=_opts, \
        executable_path = GeckoDriverManager().install())
    return driver

