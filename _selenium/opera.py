from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.common.by import By

def init_opera():
    """
    Basic selenium opera handler
    """
    driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    return driver