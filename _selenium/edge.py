from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

def init_edge():
    """
    Basic edge/selenium handler
    """
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    return driver