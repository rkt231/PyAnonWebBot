from selenium import webdriver
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.common.by import By

def init_ie():
    """
    A basic IE/selenium handler
    """
    driver = webdriver.Ie(IEDriverManager().install())
    return driver